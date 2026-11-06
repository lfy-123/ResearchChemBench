"""Filter rejected reasoning on every request of a recovered Codex session.

The controller activates recovery after an explicit provider rejection. This
transport only filters subsequent requests; it never retries, rewrites responses,
or modifies the SDK's saved history. The frozen upstream configuration stays intact.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import threading
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx

from .codex_history import plaintext_history_items, session_home
from .recovery import RunRecoveryError


_HOP_HEADERS = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
                "te", "trailer", "transfer-encoding", "upgrade"}


class CodexHistoryTransport:
    def __init__(self, runner, store):
        self.runner, self.store = runner, store
        self.token = secrets.token_urlsafe(32)
        self.api_key = os.environ.get("RCB_CODEX_API_KEY", "")
        self.server = self.client = self.thread = None
        self.base_url = None

    def start(self):
        session_home(self.store)  # Validate the active copy before serving it.
        if not self.store.get_record("history_recovery", "active"):
            raise RunRecoveryError("history_transport_requires_recovery")
        provider = hashlib.sha256(json.dumps([self.runner.codex_base_url, self.runner.codex_model]).encode()).hexdigest()
        saved = self.store.get_record("history_transport", "active")
        if saved and saved.get("provider_sha256") != provider:
            raise RunRecoveryError("history_transport_provider_changed")
        transport = self

        class Handler(BaseHTTPRequestHandler):
            # HTTP/1.0 closes each downstream response; upstream SSE chunks can
            # stream immediately without buffering or a fabricated content length.
            def log_message(self, *args):
                pass

            def do_POST(self):
                transport.forward(self)

            def do_GET(self):
                transport.forward(self)

        self.client = httpx.Client(follow_redirects=False)
        try:
            self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            self.server.daemon_threads = True
            self.server.block_on_close = False
            self.base_url = f"http://127.0.0.1:{self.server.server_port}/v1"
            record = saved or {
                "mode": "continuous_plaintext_requests", "version": 1,
                "provider_sha256": provider, "activated_at": datetime.now(timezone.utc).isoformat(),
                "original_history_preserved": True, "tool_history_preserved": True,
                "internal_reasoning_replayed": False,
            }
            records = [("history_transport", "active", record)]
            error = self.store.get_record("history_recovery", "error") or {}
            if error.get("message") == "plaintext_history_fallback_already_used":
                records += [("history_transport", "previous_error", error), ("history_recovery", "error", None)]
            self.store.put_records(records)
            self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
            self.thread.start()
        except BaseException:
            self.close()
            raise
        return self

    @staticmethod
    def error(handler, status, code):
        raw = json.dumps({"error": {"code": code, "message": code}}).encode()
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(raw)))
        handler.end_headers()
        handler.wfile.write(raw)

    def forward(self, handler):
        if not hmac.compare_digest(handler.headers.get("Authorization", ""), "Bearer " + self.token):
            return self.error(handler, 401, "unauthorized")
        path = handler.path.removeprefix("/v1/")
        if (handler.command, path) not in {("POST", "responses"), ("POST", "responses/compact"), ("GET", "models")}:
            return self.error(handler, 404, "unsupported_history_transport_route")
        started = False
        try:
            timeout = min(600, self.runner.remaining_run_timeout_seconds())
            if not self.api_key:
                raise RunRecoveryError("history_transport_missing_api_key")
            raw = b""
            if handler.command == "POST":
                if handler.headers.get("Content-Encoding", "identity") != "identity" or handler.headers.get("Transfer-Encoding"):
                    raise RunRecoveryError("history_transport_unsupported_request_encoding")
                size = int(handler.headers.get("Content-Length", "0"))
                if size <= 0:
                    raise ValueError("missing request body")
                handler.connection.settimeout(min(30, timeout))
                original = handler.rfile.read(size)
                body = json.loads(original)
                if body.get("model") != self.runner.codex_model:
                    raise RunRecoveryError("history_transport_model_changed")
                if body.get("previous_response_id") or body.get("conversation"):
                    raise RunRecoveryError("history_recovery_requires_expanded_input")
                removed = 0
                if not isinstance(body.get("input"), str):
                    body["input"], removed = plaintext_history_items(body.get("input"))
                raw = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode() if removed else original
                # Store counts and hashes only, never credentials or request contents.
                self.store.put_record("history_transport_request", uuid.uuid4().hex, {
                    "attempt_id": self.runner.attempt_id, "path": path,
                    "at": datetime.now(timezone.utc).isoformat(), "removed_reasoning_count": removed,
                    "original_sha256": hashlib.sha256(original).hexdigest(),
                    "forwarded_sha256": hashlib.sha256(raw).hexdigest(),
                })
            excluded = _HOP_HEADERS | {"host", "authorization", "content-length"}
            excluded |= {v.strip().lower() for v in handler.headers.get("Connection", "").split(",")}
            headers = {k: v for k, v in handler.headers.items() if k.lower() not in excluded}
            headers["Authorization"] = "Bearer " + self.api_key
            with self.client.stream(handler.command, self.runner.codex_base_url.rstrip("/") + "/" + path,
                                    content=raw, headers=headers, timeout=httpx.Timeout(timeout, connect=min(30, timeout))) as upstream:
                handler.send_response(upstream.status_code)
                for key, value in upstream.headers.multi_items():
                    if key.lower() not in _HOP_HEADERS:
                        handler.send_header(key, value)
                handler.end_headers()
                started = True
                for chunk in upstream.iter_raw():
                    self.runner.remaining_run_timeout_seconds()
                    handler.wfile.write(chunk)
                    handler.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as exc:
            # A partially delivered stream must simply end, never be replayed.
            if not started:
                code = str(exc) if isinstance(exc, RunRecoveryError) else "history_transport_request_failed"
                self.error(handler, 400 if isinstance(exc, (RunRecoveryError, ValueError)) else 502, code)

    def close(self):
        if self.thread:
            self.server.shutdown()
            self.thread.join(timeout=2)
        if self.server:
            self.server.server_close()
        if self.client:
            self.client.close()

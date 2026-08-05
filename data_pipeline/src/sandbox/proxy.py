from __future__ import annotations

import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from src.sandbox.control import OpenSandboxClient, SandboxError

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}


class SandboxProxyServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        *,
        client: OpenSandboxClient,
        remote_port: int,
        request_timeout: float,
    ) -> None:
        self.client = client
        self.remote_port = remote_port
        self.request_timeout = request_timeout
        super().__init__(address, SandboxProxyHandler)


class SandboxProxyHandler(BaseHTTPRequestHandler):
    server: SandboxProxyServer

    def log_message(self, format: str, *args: Any) -> None:
        print(f"sandbox-local-proxy: {format % args}", file=sys.stderr, flush=True)

    def _forward(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.casefold() not in HOP_BY_HOP_HEADERS | {"host", "content-length"}
        }
        try:
            status, response_headers, payload = self.server.client.proxy_bytes(
                self.command,
                port=self.server.remote_port,
                suffix=self.path.lstrip("/"),
                body=body,
                headers=headers,
                timeout=self.server.request_timeout,
            )
        except SandboxError as exc:
            payload = str(exc).encode("utf-8", errors="replace")
            self.send_response(HTTPStatus.BAD_GATEWAY)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_response(status)
        for key, value in response_headers.items():
            if key.casefold() in HOP_BY_HOP_HEADERS | {"content-length"}:
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = _forward
    do_POST = _forward
    do_PUT = _forward
    do_PATCH = _forward
    do_DELETE = _forward
    do_HEAD = _forward
    do_OPTIONS = _forward


class LocalSandboxProxy:
    def __init__(
        self,
        client: OpenSandboxClient,
        *,
        remote_port: int,
        request_timeout: float = 1200,
    ) -> None:
        self.server = SandboxProxyServer(
            ("127.0.0.1", 0),
            client=client,
            remote_port=remote_port,
            request_timeout=request_timeout,
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def start(self) -> LocalSandboxProxy:
        self.thread.start()
        return self

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


__all__ = ["LocalSandboxProxy"]

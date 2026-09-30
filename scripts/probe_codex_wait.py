"""Isolated Codex/MCP wait probe. No chemistry jobs or existing sessions are used.

Credentials are read only from RCB_CODEX_API_KEY (or --env-file). The loopback
proxy records request timestamps and tool names, never headers or prompt bodies.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def append_event(destination, **event):
    with Path(destination).open("a") as stream:
        stream.write(json.dumps({"time": time.time(), **event}) + "\n")


def serve_tool(seconds, output):
    import anyio
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("rcb_wait")

    @mcp.tool()
    async def wait_for_event() -> dict:
        """Wait for a controlled event. Keep this call pending until it completes."""
        append_event(output / "tool_events.jsonl", event="start")
        try:
            await anyio.sleep(seconds)
        except BaseException:
            append_event(output / "tool_events.jsonl", event="cancelled")
            raise
        append_event(output / "tool_events.jsonl", event="finished")
        return {"status": "completed", "value": "event-ready"}

    mcp.run()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["provider_default", "direct"], default="direct")
    parser.add_argument("--namespace", default="mcp__rcb_wait")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--codex", default="codex")
    args = parser.parse_args(argv)
    args.output = args.output.resolve()
    if args.serve:
        serve_tool(args.seconds, args.output)
        return 0
    args.output.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env["NO_PROXY"] = env["no_proxy"] = "127.0.0.1,localhost"
    if args.env_file:
        from dotenv import dotenv_values
        env.update({k: v for k, v in dotenv_values(args.env_file).items()
                    if k.startswith("RCB_CODEX_") and v is not None})
    if not env.get("RCB_CODEX_API_KEY") or not env.get("RCB_CODEX_BASE_URL"):
        parser.error("RCB_CODEX_API_KEY and RCB_CODEX_BASE_URL are required")
    base = env["RCB_CODEX_BASE_URL"].rstrip("/")
    if not base.endswith("/v1"):
        base += "/v1"
    events = args.output / "requests.jsonl"

    class Proxy(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_):
            pass

        def log_error(self, format, *values):
            append_event(events, event="http_error", request_line=self.requestline, detail=format % values)

        def do_GET(self):
            append_event(events, event="get", path=self.path)
            self.send_error(426, "Use HTTP Responses streaming")

        def do_POST(self):
            import requests
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            try:
                data = json.loads(body)
                names = [t.get("name", t.get("type")) for t in data.get("tools", [])]
            except (ValueError, TypeError):
                names = []
            append_event(events, event="request", path=self.path, tools=names)
            try:
                with requests.post(base + self.path.removeprefix("/v1"), data=body,
                                   headers={"Authorization": "Bearer " + env["RCB_CODEX_API_KEY"],
                                            "Content-Type": "application/json"},
                                   stream=True, timeout=(30, 300)) as response:
                    self.send_response(response.status_code)
                    self.send_header("Content-Type", response.headers.get("Content-Type", "text/event-stream"))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    for chunk in response.iter_content(chunk_size=1024):
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    append_event(events, event="response_end", status=response.status_code)
            except Exception as exc:
                append_event(events, event="proxy_error", error=type(exc).__name__)
            self.close_connection = True

    server = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    codex_home = args.output / "codex"
    codex_home.mkdir()
    env["CODEX_HOME"] = str(codex_home)
    workspace = args.output / "workspace"
    workspace.mkdir()
    model = env.get("RCB_CODEX_MODEL", "gpt-5.6-sol")
    effort = env.get("RCB_CODEX_REASONING_EFFORT", "high")
    settings = {
        "model": model, "model_reasoning_effort": effort,
        "model_provider": "rcb", "model_providers.rcb.name": "RCB wait probe",
        "model_providers.rcb.base_url": f"http://127.0.0.1:{server.server_port}/v1",
        "model_providers.rcb.env_key": "RCB_CODEX_API_KEY",
        "model_providers.rcb.wire_api": "responses",
        "model_providers.rcb.supports_websockets": False,
        "model_providers.rcb.request_max_retries": 0,
        "features.enable_request_compression": False,
        "approval_policy": "never", "sandbox_mode": "workspace-write",
        "mcp_servers.rcb_wait.command": sys.executable,
        "mcp_servers.rcb_wait.args": [str(Path(__file__).resolve()), "--serve", "--seconds", str(args.seconds), "--output", str(args.output)],
        "mcp_servers.rcb_wait.required": True,
        "mcp_servers.rcb_wait.default_tools_approval_mode": "approve",
        "mcp_servers.rcb_wait.tool_timeout_sec": int(args.seconds + 300),
    }
    if args.mode == "direct":
        settings["features.code_mode.direct_only_tool_namespaces"] = [args.namespace]
    command = [args.codex, "exec", "--ignore-user-config", "--skip-git-repo-check", "--json", "-C", str(workspace)]
    for key, value in settings.items():
        command += ["-c", key + "=" + json.dumps(value)]
    command.append("Call rcb_wait.wait_for_event exactly once and wait for its real result. Do not use other tools. Once complete, answer with its value only.")
    version = subprocess.check_output([args.codex, "--version"], text=True).strip()
    (args.output / "config.json").write_text(json.dumps({"cli_version": version, "model": model, "effort": effort, "mode": args.mode, "namespace": args.namespace, "seconds": args.seconds}, indent=2))
    with (args.output / "stdout.jsonl").open("w") as out, (args.output / "stderr.log").open("w") as err:
        process = subprocess.Popen(command, env=env, stdout=out, stderr=err, start_new_session=True)
        try:
            code = process.wait(timeout=args.seconds + 300)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124
    server.shutdown()
    request_events = [json.loads(line) for line in events.read_text().splitlines()] if events.exists() else []
    tool_path = args.output / "tool_events.jsonl"
    tool_events = [json.loads(line) for line in tool_path.read_text().splitlines()] if tool_path.exists() else []
    starts = [e["time"] for e in tool_events if e["event"] == "start"]
    ends = [e["time"] for e in tool_events if e["event"] == "finished"]
    during = sum(e["event"] == "request" and starts[0] < e["time"] < ends[-1] for e in request_events) if starts and ends else None
    summary = {"exit_code": code, "request_count": sum(e["event"] == "request" for e in request_events),
               "tool_starts": len(starts), "tool_completions": len(ends), "requests_during_wait": during}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

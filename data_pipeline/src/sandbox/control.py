from __future__ import annotations

import http.client
import json
import ssl
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote, urlencode, urlsplit


class SandboxError(RuntimeError):
    """One OpenSandbox control-plane or proxy operation failed."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        response: str = "",
        retryable: bool = True,
    ) -> None:
        self.status = status
        self.response = response
        self.retryable = retryable
        super().__init__(message)


class OpenSandboxClient:
    """Small standard-library OpenSandbox client bound to one instance."""

    def __init__(
        self,
        *,
        base_url: str,
        project: str,
        api_key: str,
        sandbox_id: str = "",
        command_port: int = 44772,
        rpc_port: int = 44773,
    ) -> None:
        parsed = urlsplit(base_url.rstrip("/"))
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError(f"invalid OpenSandbox base URL: {base_url!r}")
        if not project or not api_key:
            raise ValueError("OpenSandbox project and API key are required")
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port
        self.base_path = parsed.path.rstrip("/")
        self.project = project
        self.api_key = api_key
        self.sandbox_id = sandbox_id
        self.command_port = int(command_port)
        self.rpc_port = int(rpc_port)
        self._access_token = ""

    def for_sandbox(self, sandbox_id: str) -> OpenSandboxClient:
        return OpenSandboxClient(
            base_url=f"{self.scheme}://{self.host}"
            + (f":{self.port}" if self.port else "")
            + self.base_path,
            project=self.project,
            api_key=self.api_key,
            sandbox_id=sandbox_id,
            command_port=self.command_port,
            rpc_port=self.rpc_port,
        )

    def _connection(self, timeout: float) -> http.client.HTTPConnection:
        if self.scheme == "https":
            return http.client.HTTPSConnection(
                self.host,
                self.port,
                timeout=timeout,
                context=ssl.create_default_context(),
            )
        return http.client.HTTPConnection(self.host, self.port, timeout=timeout)

    def _path(self, suffix: str) -> str:
        return f"{self.base_path}{suffix}"

    def request_bytes(
        self,
        method: str,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: bytes | None = None,
        timeout: float = 30.0,
    ) -> tuple[int, dict[str, str], bytes]:
        connection = self._connection(timeout)
        try:
            connection.request(method, self._path(path), body=body, headers=dict(headers or {}))
            response = connection.getresponse()
            payload = response.read()
            response_headers = {key.casefold(): value for key, value in response.getheaders()}
            return response.status, response_headers, payload
        except (OSError, http.client.HTTPException) as exc:
            raise SandboxError(f"OpenSandbox request failed: {method} {path}: {exc}") from exc
        finally:
            connection.close()

    @staticmethod
    def decode_json(payload: bytes, *, context: str) -> dict[str, Any]:
        try:
            value = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SandboxError(
                f"{context} returned invalid JSON",
                response=payload[-2000:].decode("utf-8", errors="replace"),
            ) from exc
        if not isinstance(value, dict):
            raise SandboxError(f"{context} did not return a JSON object")
        return value

    def management_json(
        self,
        method: str,
        suffix: str,
        *,
        payload: Mapping[str, Any] | None = None,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        separator = "&" if "?" in suffix else "?"
        path = f"{suffix}{separator}{urlencode({'project': self.project})}"
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"OPEN-SANDBOX-API-KEY": self.api_key}
        if body is not None:
            headers["Content-Type"] = "application/json"
        status, _headers, response = self.request_bytes(
            method, path, headers=headers, body=body, timeout=timeout
        )
        if status < 200 or status >= 300:
            text = response.decode("utf-8", errors="replace")
            raise SandboxError(
                f"OpenSandbox management API returned HTTP {status}: {method} {suffix}",
                status=status,
                response=text[-4000:],
                retryable=status >= 500 or status in {408, 409, 429},
            )
        if not response:
            return {}
        return self.decode_json(response, context=f"{method} {suffix}")

    def detail(self) -> dict[str, Any]:
        self._require_sandbox()
        return self.management_json("GET", f"/v1/sandboxes/{quote(self.sandbox_id)}")

    def access_token(self, *, refresh: bool = False) -> str:
        if self._access_token and not refresh:
            return self._access_token
        detail = self.detail()
        token = str(
            detail.get("accessToken") or (detail.get("endpoints") or {}).get("accessToken") or ""
        )
        if not token:
            raise SandboxError(f"Sandbox {self.sandbox_id} did not return an access token")
        self._access_token = token
        return token

    def proxy_bytes(
        self,
        method: str,
        *,
        port: int,
        suffix: str,
        body: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 30.0,
        refresh_token: bool = False,
    ) -> tuple[int, dict[str, str], bytes]:
        self._require_sandbox()
        token = self.access_token(refresh=refresh_token)
        path = f"/v1/sandboxes/{quote(self.sandbox_id)}/proxy/{int(port)}/{suffix.lstrip('/')}"
        request_headers = {
            str(key): str(value)
            for key, value in (headers or {}).items()
            if str(key).casefold() not in {"host", "content-length", "connection"}
        }
        request_headers["X-Sandbox-Access-Token"] = token
        status, response_headers, response = self.request_bytes(
            method,
            path,
            headers=request_headers,
            body=body,
            timeout=timeout,
        )
        if status in {401, 403} and not refresh_token:
            return self.proxy_bytes(
                method,
                port=port,
                suffix=suffix,
                body=body,
                headers=headers,
                timeout=timeout,
                refresh_token=True,
            )
        return status, response_headers, response

    def proxy_json(
        self,
        method: str,
        *,
        port: int,
        suffix: str,
        payload: Mapping[str, Any] | None = None,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json"} if body is not None else {}
        status, _headers, response = self.proxy_bytes(
            method,
            port=port,
            suffix=suffix,
            body=body,
            headers=headers,
            timeout=timeout,
        )
        if status < 200 or status >= 300:
            raise SandboxError(
                f"Sandbox proxy returned HTTP {status}: {method} {suffix}",
                status=status,
                response=response[-4000:].decode("utf-8", errors="replace"),
                retryable=status >= 500 or status in {408, 409, 429},
            )
        return self.decode_json(response, context=f"sandbox proxy {method} {suffix}")

    def run_command(self, command: str, *, timeout: float = 60.0) -> dict[str, Any]:
        status, _headers, response = self.proxy_bytes(
            "POST",
            port=self.command_port,
            suffix="command",
            body=json.dumps({"command": command}, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        text = response.decode("utf-8", errors="replace")
        if status < 200 or status >= 300:
            raise SandboxError(
                f"Sandbox command API returned HTTP {status}",
                status=status,
                response=text[-4000:],
            )
        stdout: list[str] = []
        stderr: list[str] = []
        error: dict[str, Any] | None = None
        for line in text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            if event.get("type") == "stdout":
                stdout.append(str(event.get("text") or ""))
            elif event.get("type") == "stderr":
                stderr.append(str(event.get("text") or ""))
            elif event.get("type") == "error":
                error = dict(event.get("error") or {})
        return {
            "status": "failed" if error else "success",
            "stdout": "\n".join(stdout),
            "stderr": "\n".join(stderr),
            "error": error,
        }

    def download(self, *, port: int, suffix: str, destination: Path, timeout: float = 3600) -> None:
        status, _headers, payload = self.proxy_bytes(
            "GET", port=port, suffix=suffix, timeout=timeout
        )
        if status < 200 or status >= 300:
            raise SandboxError(
                f"Sandbox download returned HTTP {status}",
                status=status,
                response=payload[-4000:].decode("utf-8", errors="replace"),
            )
        destination.write_bytes(payload)

    def _require_sandbox(self) -> None:
        if not self.sandbox_id:
            raise ValueError("this OpenSandbox operation requires a sandbox_id")


__all__ = ["OpenSandboxClient", "SandboxError"]

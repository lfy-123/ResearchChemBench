"""OpenSandbox control-plane, command, and worker-RPC client.

The distributed scheduler remains transport-agnostic.  This module implements
only the remote I/O boundary used by OpenSandbox workers; the existing SSH path
continues to use its current subprocess-based launcher.
"""

from __future__ import annotations

import http.client
import json
import os
import shlex
import ssl
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote, urlencode, urlsplit


class SandboxTransportError(RuntimeError):
    """One OpenSandbox control-plane or RPC operation failed."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        response: str = "",
        retryable: bool = True,
    ):
        self.status = status
        self.response = response
        self.retryable = retryable
        super().__init__(message)


class OpenSandboxClient:
    """Small standard-library client bound to one sandbox instance."""

    def __init__(
        self,
        *,
        base_url: str,
        project: str,
        api_key: str,
        sandbox_id: str,
        command_port: int = 44772,
        rpc_port: int = 44773,
        project_root: str = "",
        remote_job_root: str = "/tmp/researchchembench/jobs",
    ):
        parsed = urlsplit(base_url.rstrip("/"))
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError(f"invalid OpenSandbox base URL: {base_url!r}")
        if not project or not sandbox_id or not api_key:
            raise ValueError("OpenSandbox project, sandbox_id, and API key are required")
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port
        self.base_path = parsed.path.rstrip("/")
        self.project = project
        self.api_key = api_key
        self.sandbox_id = sandbox_id
        self.command_port = int(command_port)
        self.rpc_port = int(rpc_port)
        self.project_root = project_root
        self.remote_job_root = remote_job_root.rstrip("/")
        self._access_token = ""

    @classmethod
    def from_worker(cls, worker: Any) -> "OpenSandboxClient":
        key_env = str(worker.sandbox_api_key_env or "RCB_SANDBOX_API_KEY")
        api_key = os.environ.get(key_env, "").strip()
        if not api_key:
            raise SandboxTransportError(
                f"OpenSandbox API key environment variable is missing: {key_env}",
                retryable=False,
            )
        return cls(
            base_url=worker.sandbox_api_base,
            project=worker.sandbox_project,
            api_key=api_key,
            sandbox_id=worker.sandbox_id,
            command_port=worker.sandbox_command_port,
            rpc_port=worker.sandbox_rpc_port,
            project_root=worker.sandbox_project_root,
            remote_job_root=worker.sandbox_remote_job_root,
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

    def _request_bytes(
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
            raise SandboxTransportError(
                f"OpenSandbox request failed: {method} {path}: {exc}"
            ) from exc
        finally:
            connection.close()

    @staticmethod
    def _decode_json(payload: bytes, *, context: str) -> dict[str, Any]:
        try:
            value = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SandboxTransportError(
                f"{context} returned invalid JSON",
                response=payload[-2000:].decode("utf-8", errors="replace"),
            ) from exc
        if not isinstance(value, dict):
            raise SandboxTransportError(f"{context} did not return a JSON object")
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
        status, _headers, response = self._request_bytes(
            method, path, headers=headers, body=body, timeout=timeout
        )
        if status < 200 or status >= 300:
            text = response.decode("utf-8", errors="replace")
            raise SandboxTransportError(
                f"OpenSandbox management API returned HTTP {status}: {method} {suffix}",
                status=status,
                response=text[-4000:],
                retryable=status >= 500 or status in {408, 409, 429},
            )
        if not response:
            return {}
        return self._decode_json(response, context=f"{method} {suffix}")

    def detail(self) -> dict[str, Any]:
        return self.management_json("GET", f"/v1/sandboxes/{quote(self.sandbox_id)}")

    def access_token(self, *, refresh: bool = False) -> str:
        if self._access_token and not refresh:
            return self._access_token
        detail = self.detail()
        token = str(
            detail.get("accessToken")
            or (detail.get("endpoints") or {}).get("accessToken")
            or ""
        )
        if not token:
            raise SandboxTransportError(
                f"Sandbox {self.sandbox_id} did not return an access token"
            )
        self._access_token = token
        return token

    def _proxy_bytes(
        self,
        method: str,
        *,
        port: int,
        suffix: str,
        body: bytes | None = None,
        content_type: str = "application/json",
        timeout: float = 30.0,
        refresh_token: bool = False,
    ) -> tuple[int, dict[str, str], bytes]:
        token = self.access_token(refresh=refresh_token)
        path = (
            f"/v1/sandboxes/{quote(self.sandbox_id)}/proxy/{int(port)}"
            f"/{suffix.lstrip('/')}"
        )
        headers = {"X-Sandbox-Access-Token": token}
        if body is not None:
            headers["Content-Type"] = content_type
        status, response_headers, response = self._request_bytes(
            method, path, headers=headers, body=body, timeout=timeout
        )
        if status in {401, 403} and not refresh_token:
            return self._proxy_bytes(
                method,
                port=port,
                suffix=suffix,
                body=body,
                content_type=content_type,
                timeout=timeout,
                refresh_token=True,
            )
        return status, response_headers, response

    def run_command(self, command: str, *, timeout: float = 60.0) -> dict[str, Any]:
        body = json.dumps({"command": command}, ensure_ascii=False).encode("utf-8")
        status, _headers, response = self._proxy_bytes(
            "POST",
            port=self.command_port,
            suffix="command",
            body=body,
            timeout=timeout,
        )
        text = response.decode("utf-8", errors="replace")
        if status < 200 or status >= 300:
            raise SandboxTransportError(
                f"Sandbox command API returned HTTP {status}",
                status=status,
                response=text[-4000:],
                retryable=status >= 500 or status in {408, 409, 429},
            )
        events: list[dict[str, Any]] = []
        stdout: list[str] = []
        stderr: list[str] = []
        error: dict[str, Any] | None = None
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            events.append(event)
            event_type = str(event.get("type") or "")
            if event_type == "stdout":
                stdout.append(str(event.get("text") or ""))
            elif event_type == "stderr":
                stderr.append(str(event.get("text") or ""))
            elif event_type == "error":
                error = dict(event.get("error") or {})
        return {
            "status": "failed" if error is not None else "success",
            "stdout": "\n".join(stdout),
            "stderr": "\n".join(stderr),
            "error": error,
            "events": events,
        }

    def rpc_json(
        self,
        method: str,
        suffix: str,
        *,
        payload: Mapping[str, Any] | None = None,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        status, _headers, response = self._proxy_bytes(
            method,
            port=self.rpc_port,
            suffix=suffix,
            body=body,
            timeout=timeout,
        )
        if status < 200 or status >= 300:
            text = response.decode("utf-8", errors="replace")
            raise SandboxTransportError(
                f"Sandbox RPC returned HTTP {status}: {method} {suffix}",
                status=status,
                response=text[-4000:],
                retryable=status >= 500 or status in {408, 409, 429},
            )
        return self._decode_json(response, context=f"sandbox RPC {method} {suffix}")

    def health(self, *, timeout: float = 10.0) -> dict[str, Any]:
        return self.rpc_json("GET", "health", timeout=timeout)

    def ensure_rpc(self, *, timeout: float = 45.0) -> dict[str, Any]:
        try:
            value = self.health(timeout=5.0)
            if value.get("status") == "success":
                return value
        except SandboxTransportError:
            pass
        if not self.project_root:
            raise SandboxTransportError(
                "sandbox inventory is missing sandbox_project_root",
                retryable=False,
            )
        framework_python = str(
            Path(self.project_root) / ".envs" / "researchchembench" / "bin" / "python"
        )
        log_path = f"/tmp/researchchembench-rpc-{self.rpc_port}.log"
        command = (
            f"cd {shlex.quote(self.project_root)} && "
            "PYTHONDONTWRITEBYTECODE=1 nohup "
            f"{shlex.quote(framework_python)} -m researchchem_toolbox.sandbox_worker_rpc "
            f"--host 0.0.0.0 --port {self.rpc_port} "
            f"--job-root {shlex.quote(self.remote_job_root)} "
            f">{shlex.quote(log_path)} 2>&1 </dev/null &"
        )
        result = self.run_command(command, timeout=30.0)
        if result["status"] != "success":
            raise SandboxTransportError(
                f"failed to start sandbox worker RPC: {result.get('error')}",
                response=result.get("stderr", ""),
            )
        deadline = time.monotonic() + timeout
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                value = self.health(timeout=5.0)
                if value.get("status") == "success":
                    return value
            except SandboxTransportError as exc:
                last_error = exc
            time.sleep(1.0)
        raise SandboxTransportError(
            f"sandbox worker RPC did not become healthy: {last_error}"
        )

    def run_action(
        self, envelope: Mapping[str, Any], *, timeout_seconds: int
    ) -> dict[str, Any]:
        self.ensure_rpc()
        action_id = str(envelope.get("distributed_reservation_id") or "")
        workspace_raw = str(
            (dict(envelope.get("environment") or {})).get(
                "RESEARCHCHEMBENCH_WORKSPACE", ""
            )
        )
        if action_id:
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                self._action_input_archive(
                    dict(envelope.get("payload") or {}),
                    workspace=Path(workspace_raw) if workspace_raw else None,
                    destination=Path(handle.name),
                )
                self._upload_archive(
                    f"v1/actions/{quote(action_id)}/stage", Path(handle.name)
                )
        result = self.rpc_json(
            "POST",
            "v1/actions/run",
            payload={"envelope": dict(envelope), "timeout_seconds": timeout_seconds},
            timeout=float(timeout_seconds + 45),
        )
        action = dict(result.pop("_sandbox_action", {}) or {})
        action_id = str(action.get("action_id") or action_id)
        artifacts = [dict(item) for item in result.get("artifact_files") or []]
        if action_id and artifacts and workspace_raw:
            destination = (
                Path(workspace_raw).resolve()
                / "outputs"
                / "sandbox_actions"
                / action_id
            )
            destination.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                self._download_archive_with_retry(
                    f"v1/actions/{quote(action_id)}/archive", Path(handle.name)
                )
                with tarfile.open(handle.name, "r:gz") as archive:
                    root = destination.resolve()
                    for member in archive.getmembers():
                        if member.issym() or member.islnk():
                            raise SandboxTransportError("sandbox Action archive contains links")
                        target = (destination / member.name).resolve()
                        if target != root and root not in target.parents:
                            raise SandboxTransportError(
                                f"sandbox Action archive escapes destination: {member.name}"
                            )
                    archive.extractall(destination)
            for item in artifacts:
                item["path"] = str((destination / str(item["path"])).resolve())
            result["artifact_files"] = artifacts
        if action_id and (not artifacts or workspace_raw):
            try:
                self.rpc_json("DELETE", f"v1/actions/{quote(action_id)}")
            except SandboxTransportError:
                pass
        return result

    @staticmethod
    def _action_input_archive(
        payload: Mapping[str, Any], *, workspace: Path | None, destination: Path
    ) -> None:
        paths: set[Path] = set()
        root = workspace.expanduser().resolve() if workspace else None

        def collect(value: Any) -> None:
            if isinstance(value, Mapping):
                for item in value.values():
                    collect(item)
                return
            if isinstance(value, (list, tuple)):
                for item in value:
                    collect(item)
                return
            if root is None or not isinstance(value, str) or not value.strip():
                return
            candidate = Path(value).expanduser()
            if not candidate.is_absolute():
                candidate = root / candidate
            resolved = candidate.resolve(strict=False)
            try:
                resolved.relative_to(root)
            except ValueError:
                return
            if resolved.exists() and not resolved.is_symlink():
                paths.add(resolved)

        collect(payload)
        selected: list[Path] = []
        for path in sorted(paths, key=lambda item: (len(item.parts), str(item))):
            if any(parent == path or parent in path.parents for parent in selected):
                continue
            selected.append(path)
        with tarfile.open(destination, "w:gz", dereference=True) as archive:
            if root is None:
                return
            for path in selected:
                archive.add(path, arcname=str(path.relative_to(root)), recursive=True)

    def _upload_archive(
        self,
        suffix: str,
        archive_path: Path,
        *,
        refresh_token: bool = False,
    ) -> dict[str, Any]:
        self.ensure_rpc()
        token = self.access_token(refresh=refresh_token)
        path = self._path(
            f"/v1/sandboxes/{quote(self.sandbox_id)}/proxy/{self.rpc_port}/{suffix}"
        )
        size = archive_path.stat().st_size
        connection = self._connection(max(60.0, size / (4 * 1024 * 1024)))
        try:
            connection.putrequest("POST", path)
            connection.putheader("X-Sandbox-Access-Token", token)
            connection.putheader("Content-Type", "application/gzip")
            connection.putheader("Content-Length", str(size))
            connection.endheaders()
            with archive_path.open("rb") as handle:
                while chunk := handle.read(1024 * 1024):
                    connection.send(chunk)
            response = connection.getresponse()
            payload = response.read()
            if response.status in {401, 403} and not refresh_token:
                return self._upload_archive(
                    suffix, archive_path, refresh_token=True
                )
            if response.status < 200 or response.status >= 300:
                raise SandboxTransportError(
                    f"sandbox job upload returned HTTP {response.status}",
                    status=response.status,
                    response=payload[-4000:].decode("utf-8", errors="replace"),
                )
            return self._decode_json(payload, context="sandbox job upload")
        except (OSError, http.client.HTTPException) as exc:
            if isinstance(exc, SandboxTransportError):
                raise
            raise SandboxTransportError(f"sandbox job upload failed: {exc}") from exc
        finally:
            connection.close()

    def upload_job_archive(self, job_id: str, archive_path: Path) -> dict[str, Any]:
        return self._upload_archive(
            f"v1/jobs/{quote(job_id)}/stage", archive_path
        )

    def start_job(
        self,
        job_id: str,
        *,
        specification: Mapping[str, Any],
        environment: Mapping[str, str],
    ) -> dict[str, Any]:
        return self.rpc_json(
            "POST",
            f"v1/jobs/{quote(job_id)}/start",
            payload={
                "specification": dict(specification),
                "environment": dict(environment),
            },
            timeout=45.0,
        )

    def job_status(self, job_id: str) -> dict[str, Any]:
        return self.rpc_json("GET", f"v1/jobs/{quote(job_id)}/status", timeout=20.0)

    def cancel_job(self, job_id: str) -> dict[str, Any]:
        return self.rpc_json("POST", f"v1/jobs/{quote(job_id)}/cancel", payload={})

    def delete_job(self, job_id: str) -> dict[str, Any]:
        return self.rpc_json("DELETE", f"v1/jobs/{quote(job_id)}", timeout=30.0)

    def _download_archive(
        self,
        suffix: str,
        destination: Path,
        *,
        refresh_token: bool = False,
    ) -> None:
        token = self.access_token(refresh=refresh_token)
        path = self._path(
            f"/v1/sandboxes/{quote(self.sandbox_id)}/proxy/{self.rpc_port}"
            f"/{suffix.lstrip('/')}"
        )
        connection = self._connection(3600.0)
        try:
            connection.request(
                "GET", path, headers={"X-Sandbox-Access-Token": token}
            )
            response = connection.getresponse()
            if response.status in {401, 403} and not refresh_token:
                response.read()
                self._download_archive(
                    suffix, destination, refresh_token=True
                )
                return
            if response.status < 200 or response.status >= 300:
                payload = response.read()
                raise SandboxTransportError(
                    f"sandbox job archive returned HTTP {response.status}",
                    status=response.status,
                    response=payload[-4000:].decode("utf-8", errors="replace"),
                    retryable=response.status >= 500
                    or response.status in {408, 409, 429},
                )
            with destination.open("wb") as handle:
                while chunk := response.read(1024 * 1024):
                    handle.write(chunk)
        except (OSError, http.client.HTTPException) as exc:
            if isinstance(exc, SandboxTransportError):
                raise
            raise SandboxTransportError(f"sandbox job download failed: {exc}") from exc
        finally:
            connection.close()

    def _download_archive_with_retry(
        self,
        suffix: str,
        destination: Path,
        *,
        attempts: int = 3,
    ) -> None:
        """Download one archive with bounded retries for transient transport errors."""

        last_error: SandboxTransportError | None = None
        for attempt in range(max(1, attempts)):
            try:
                self._download_archive(suffix, destination)
                return
            except SandboxTransportError as exc:
                last_error = exc
                if not exc.retryable or attempt + 1 >= max(1, attempts):
                    raise
                self._access_token = ""
                time.sleep(float(2**attempt))
        if last_error is not None:  # pragma: no cover - loop always returns or raises
            raise last_error

    def download_job_archive(self, job_id: str, destination: Path) -> None:
        self._download_archive_with_retry(
            f"v1/jobs/{quote(job_id)}/archive", destination
        )


__all__ = ["OpenSandboxClient", "SandboxTransportError"]

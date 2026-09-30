"""HTTP worker service for OpenSandbox distributed compute instances."""

from __future__ import annotations

from chemistry_toolbox.src.execution_states import TERMINAL_STATES

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit




def _safe_job_id(value: str) -> str:
    if not value or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-" for character in value):
        raise ValueError("job_id may contain only letters, digits, dot, underscore, and dash")
    return value


def _safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.getmembers():
        if member.issym() or member.islnk():
            raise ValueError("job archive may not contain links")
        target = (destination / member.name).resolve()
        if target != root and root not in target.parents:
            raise ValueError(f"job archive path escapes destination: {member.name}")
    archive.extractall(destination)


def _add_archive_tree(
    archive: tarfile.TarFile,
    path: Path,
    *,
    root: Path,
    arcname: str,
    directory_stack: tuple[Path, ...] = (),
) -> None:
    """Add a tree while dereferencing safe links and omitting broken links."""

    source = path
    if path.is_symlink():
        try:
            source = path.resolve(strict=True)
        except FileNotFoundError:
            return
        if source != root and root not in source.parents:
            raise ValueError(f"archive link escapes directory: {path}")
    if source.is_dir():
        resolved = source.resolve()
        if resolved in directory_stack:
            raise ValueError(f"archive contains a directory-link cycle: {path}")
        archive.add(source, arcname=arcname, recursive=False)
        stack = (*directory_stack, resolved)
        for child in sorted(source.iterdir()):
            _add_archive_tree(
                archive,
                child,
                root=root,
                arcname=f"{arcname}/{child.name}",
                directory_stack=stack,
            )
        return
    archive.add(source, arcname=arcname, recursive=False)


class SandboxWorkerServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], job_root: Path):
        self.job_root = job_root.resolve()
        self.job_root.mkdir(parents=True, exist_ok=True)
        self.action_root = self.job_root.parent / "actions"
        self.action_root.mkdir(parents=True, exist_ok=True)
        super().__init__(address, SandboxWorkerHandler)


class SandboxWorkerHandler(BaseHTTPRequestHandler):
    server: SandboxWorkerServer

    def log_message(self, format: str, *args: Any) -> None:
        print(f"sandbox-worker-rpc: {format % args}", file=sys.stderr, flush=True)

    def _json(self, status: int, value: dict[str, Any]) -> None:
        payload = json.dumps(value, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _error(self, status: int, code: str, message: str) -> None:
        self._json(status, {"status": "failed", "error": {"code": code, "message": message}})

    def _body(self) -> bytes:
        length = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(length)

    def _request_json(self) -> dict[str, Any]:
        value = json.loads(self._body().decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("request body must be a JSON object")
        return value

    def _segments(self) -> list[str]:
        return [unquote(item) for item in urlsplit(self.path).path.split("/") if item]

    def _job_directory(self, job_id: str) -> Path:
        return self.server.job_root / _safe_job_id(job_id)

    def do_GET(self) -> None:  # noqa: N802
        try:
            segments = self._segments()
            if segments == ["health"]:
                self._json(
                    HTTPStatus.OK,
                    {
                        "status": "success",
                        "service": "researchchembench-sandbox-worker",
                        "pid": os.getpid(),
                        "job_root": str(self.server.job_root),
                    },
                )
                return
            if len(segments) == 4 and segments[:2] == ["v1", "actions"]:
                action_id, operation = segments[2], segments[3]
                directory = self.server.action_root / _safe_job_id(action_id)
                if operation == "archive":
                    if not directory.is_dir():
                        self._error(HTTPStatus.NOT_FOUND, "action_missing", action_id)
                        return
                    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                        with tarfile.open(
                            handle.name, "w:gz", dereference=True
                        ) as archive:
                            for name in ("outputs", "external_artifacts"):
                                child = directory / name
                                if child.exists():
                                    _add_archive_tree(
                                        archive,
                                        child,
                                        root=directory.resolve(),
                                        arcname=child.name,
                                    )
                        size = Path(handle.name).stat().st_size
                        self.send_response(HTTPStatus.OK)
                        self.send_header("Content-Type", "application/gzip")
                        self.send_header("Content-Length", str(size))
                        self.end_headers()
                        handle.seek(0)
                        shutil.copyfileobj(handle, self.wfile, length=1024 * 1024)
                    return
            if len(segments) == 4 and segments[:2] == ["v1", "jobs"]:
                job_id, operation = segments[2], segments[3]
                directory = self._job_directory(job_id)
                if operation == "status":
                    path = directory / "status.json"
                    if not path.is_file():
                        self._error(HTTPStatus.NOT_FOUND, "job_status_missing", job_id)
                        return
                    value = json.loads(path.read_text(encoding="utf-8"))
                    def tail(name: str, limit: int = 8000) -> str:
                        candidate = directory / name
                        if not candidate.is_file():
                            return ""
                        with candidate.open("rb") as handle:
                            size = candidate.stat().st_size
                            handle.seek(max(0, size - limit))
                            return handle.read().decode("utf-8", errors="replace")

                    self._json(
                        HTTPStatus.OK,
                        {
                            "status": "success",
                            "job": value,
                            "stdout_tail": tail("stdout.log"),
                            "stderr_tail": tail("stderr.log"),
                        },
                    )
                    return
                if operation == "archive":
                    if not directory.is_dir():
                        self._error(HTTPStatus.NOT_FOUND, "job_missing", job_id)
                        return
                    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                        with tarfile.open(
                            handle.name, "w:gz", dereference=True
                        ) as archive:
                            for child in sorted(directory.iterdir()):
                                _add_archive_tree(
                                    archive,
                                    child,
                                    root=directory.resolve(),
                                    arcname=child.name,
                                )
                        size = Path(handle.name).stat().st_size
                        self.send_response(HTTPStatus.OK)
                        self.send_header("Content-Type", "application/gzip")
                        self.send_header("Content-Length", str(size))
                        self.end_headers()
                        handle.seek(0)
                        shutil.copyfileobj(handle, self.wfile, length=1024 * 1024)
                    return
            self._error(HTTPStatus.NOT_FOUND, "not_found", self.path)
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "rpc_exception", str(exc))

    def do_POST(self) -> None:  # noqa: N802
        try:
            segments = self._segments()
            if segments == ["v1", "actions", "run"]:
                value = self._request_json()
                envelope = dict(value["envelope"])
                timeout_seconds = max(1, int(value.get("timeout_seconds") or 60))
                project_root = Path(str(envelope["project_root"])).resolve()
                action_id = _safe_job_id(
                    str(envelope.get("distributed_reservation_id") or "action")
                )
                action_directory = self.server.action_root / action_id
                (action_directory / "outputs").mkdir(parents=True, exist_ok=True)
                environment = dict(envelope.get("environment") or {})
                environment["RESEARCHCHEMBENCH_WORKSPACE"] = str(action_directory)
                envelope["environment"] = environment
                completed = subprocess.run(
                    [sys.executable, "-m", "chemistry_toolbox.src.remote_worker_launcher"],
                    input=json.dumps(envelope, ensure_ascii=False),
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=timeout_seconds + 30,
                    check=False,
                    cwd=project_root,
                )
                try:
                    result = json.loads(completed.stdout.strip().splitlines()[-1])
                except (json.JSONDecodeError, IndexError):
                    result = {
                        "status": "failed",
                        "error": {
                            "code": "invalid_remote_worker_response",
                            "message": "Remote Action launcher returned invalid JSON",
                            "stdout": completed.stdout[-2000:],
                            "stderr": completed.stderr[-2000:],
                        },
                        "retryable": True,
                    }
                if completed.stderr.strip():
                    result.setdefault("worker_stderr", completed.stderr[-4000:])
                result.setdefault("worker_returncode", completed.returncode)
                rewritten_artifacts = []
                for index, item in enumerate(result.get("artifact_files") or []):
                    record = dict(item)
                    raw_path = Path(str(record.get("path") or ""))
                    if not raw_path.is_absolute():
                        raw_path = action_directory / raw_path
                    try:
                        relative = raw_path.resolve().relative_to(action_directory.resolve())
                    except (OSError, ValueError):
                        if raw_path.is_file():
                            target = action_directory / "external_artifacts" / f"{index}-{raw_path.name}"
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(raw_path, target)
                            relative = target.relative_to(action_directory)
                        else:
                            continue
                    record["path"] = str(relative)
                    rewritten_artifacts.append(record)
                result["artifact_files"] = rewritten_artifacts
                result["_sandbox_action"] = {
                    "action_id": action_id,
                    "has_archive": bool(rewritten_artifacts),
                }
                self._json(HTTPStatus.OK, result)
                return
            if (
                len(segments) == 4
                and segments[:2] == ["v1", "actions"]
                and segments[3] == "stage"
            ):
                action_id = segments[2]
                directory = self.server.action_root / _safe_job_id(action_id)
                if directory.exists():
                    shutil.rmtree(directory)
                directory.mkdir(parents=True)
                with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                    remaining = int(self.headers.get("Content-Length") or 0)
                    while remaining > 0:
                        chunk = self.rfile.read(min(1024 * 1024, remaining))
                        if not chunk:
                            raise ValueError("Action archive upload ended early")
                        handle.write(chunk)
                        remaining -= len(chunk)
                    handle.flush()
                    with tarfile.open(handle.name, "r:gz") as archive:
                        _safe_extract(archive, directory)
                self._json(
                    HTTPStatus.OK,
                    {
                        "status": "success",
                        "action_id": action_id,
                        "action_directory": str(directory),
                    },
                )
                return
            if len(segments) == 4 and segments[:2] == ["v1", "jobs"]:
                job_id, operation = segments[2], segments[3]
                directory = self._job_directory(job_id)
                if operation == "stage":
                    if directory.exists():
                        shutil.rmtree(directory)
                    directory.mkdir(parents=True)
                    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                        remaining = int(self.headers.get("Content-Length") or 0)
                        while remaining > 0:
                            chunk = self.rfile.read(min(1024 * 1024, remaining))
                            if not chunk:
                                raise ValueError("job archive upload ended early")
                            handle.write(chunk)
                            remaining -= len(chunk)
                        handle.flush()
                        with tarfile.open(handle.name, "r:gz") as archive:
                            _safe_extract(archive, directory)
                    self._json(
                        HTTPStatus.OK,
                        {"status": "success", "job_id": job_id, "job_directory": str(directory)},
                    )
                    return
                if operation == "start":
                    value = self._request_json()
                    if not directory.is_dir():
                        self._error(HTTPStatus.NOT_FOUND, "job_missing", job_id)
                        return
                    specification = dict(value["specification"])
                    environment = {
                        str(key): str(item)
                        for key, item in dict(value.get("environment") or {}).items()
                    }
                    spec_path = directory / "sandbox_supervisor_spec.json"
                    spec_path.write_text(
                        json.dumps(specification, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    envelope = {
                        "schema_version": 1,
                        "spec_path": str(spec_path),
                        "job_directory": str(directory),
                        "environment": environment,
                    }
                    completed = subprocess.run(
                        [sys.executable, "-m", "chemistry_toolbox.mcp.remote_job_launcher"],
                        input=json.dumps(envelope, ensure_ascii=False),
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=30,
                        check=False,
                        cwd=directory,
                    )
                    try:
                        result = json.loads(completed.stdout.strip().splitlines()[-1])
                    except (json.JSONDecodeError, IndexError):
                        result = {
                            "status": "failed",
                            "error": completed.stderr[-2000:] or "invalid launcher response",
                        }
                    self._json(
                        HTTPStatus.OK if result.get("status") == "success" else HTTPStatus.BAD_GATEWAY,
                        result,
                    )
                    return
                if operation == "cancel":
                    if not directory.is_dir():
                        self._error(HTTPStatus.NOT_FOUND, "job_missing", job_id)
                        return
                    (directory / "cancel_requested").write_text("cancelled\n", encoding="utf-8")
                    self._json(HTTPStatus.OK, {"status": "success", "job_id": job_id})
                    return
            self._error(HTTPStatus.NOT_FOUND, "not_found", self.path)
        except subprocess.TimeoutExpired as exc:
            self._error(HTTPStatus.GATEWAY_TIMEOUT, "remote_timeout", str(exc))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
            self._error(HTTPStatus.BAD_REQUEST, "invalid_request", str(exc))
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "rpc_exception", str(exc))

    def do_DELETE(self) -> None:  # noqa: N802
        try:
            segments = self._segments()
            if len(segments) == 3 and segments[:2] == ["v1", "actions"]:
                action_id = segments[2]
                directory = self.server.action_root / _safe_job_id(action_id)
                if directory.exists():
                    shutil.rmtree(directory)
                self._json(HTTPStatus.OK, {"status": "success", "action_id": action_id})
                return
            if len(segments) == 3 and segments[:2] == ["v1", "jobs"]:
                job_id = segments[2]
                directory = self._job_directory(job_id)
                if directory.exists():
                    status_path = directory / "status.json"
                    if status_path.is_file():
                        status = json.loads(status_path.read_text(encoding="utf-8"))
                        if str(status.get("status") or "") not in TERMINAL_STATES:
                            self._error(HTTPStatus.CONFLICT, "job_not_terminal", job_id)
                            return
                    shutil.rmtree(directory)
                self._json(HTTPStatus.OK, {"status": "success", "job_id": job_id})
                return
            self._error(HTTPStatus.NOT_FOUND, "not_found", self.path)
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "rpc_exception", str(exc))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=44773)
    parser.add_argument("--job-root", type=Path, default=Path("/tmp/researchchembench/jobs"))
    args = parser.parse_args(argv)
    server = SandboxWorkerServer((args.host, args.port), args.job_root)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["SandboxWorkerServer", "main"]

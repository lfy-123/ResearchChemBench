from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import threading
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml

DATA_PIPELINE_ROOT = Path(__file__).resolve().parents[2]
SAFE_IDENTIFIER = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-")
SERVICE_DEFINITIONS = {
    "grobid": {
        "distribution": DATA_PIPELINE_ROOT
        / "third_party/grobid/grobid-service/build/distributions/grobid-service-0.9.0.zip",
        "directory": "grobid-service-0.9.0",
        "executable": "grobid-service",
        "config": DATA_PIPELINE_ROOT / ".model_cache/grobid-home/config/grobid.yaml",
        "port": 8070,
        "health": "/api/isalive",
    },
    "softcite": {
        "distribution": DATA_PIPELINE_ROOT / "third_party/software-mentions/build/distributions/"
        "software-mentions-0.9.0-SNAPSHOT.zip",
        "directory": "software-mentions-0.9.0-SNAPSHOT",
        "executable": "software-mentions",
        "config": DATA_PIPELINE_ROOT / ".model_cache/config/software-mentions.yml",
        "port": 8060,
        "health": "/service/isalive",
    },
    "quantities": {
        "distribution": DATA_PIPELINE_ROOT / "third_party/grobid-quantities/build/distributions/"
        "grobid-quantities-0.9.0-SNAPSHOT.zip",
        "directory": "grobid-quantities-0.9.0-SNAPSHOT",
        "executable": "grobid-quantities",
        "config": DATA_PIPELINE_ROOT / ".model_cache/config/grobid-quantities.yml",
        "port": 8062,
        "health": "/service/isalive",
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_identifier(value: str, *, label: str = "identifier") -> str:
    if not value or any(character not in SAFE_IDENTIFIER for character in value):
        raise ValueError(f"{label} contains unsupported characters")
    return value


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _tail(path: Path, limit: int = 20000) -> str:
    if not path.is_file():
        return ""
    with path.open("rb") as handle:
        size = path.stat().st_size
        handle.seek(max(0, size - limit))
        return handle.read().decode("utf-8", errors="replace")


def _safe_zip_extract(archive_path: Path, destination: Path) -> None:
    root = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"distribution archive escapes destination: {member.filename}")
        archive.extractall(destination)


def _add_tree(archive: tarfile.TarFile, path: Path, *, root: Path, arcname: str) -> None:
    source = path.resolve(strict=True) if path.is_symlink() else path
    resolved_root = root.resolve()
    resolved_source = source.resolve()
    if resolved_source != resolved_root and resolved_root not in resolved_source.parents:
        raise ValueError(f"archive path escapes job directory: {path}")
    if source.is_dir():
        archive.add(source, arcname=arcname, recursive=False)
        for child in sorted(source.iterdir()):
            _add_tree(archive, child, root=root, arcname=f"{arcname}/{child.name}")
        return
    archive.add(source, arcname=arcname, recursive=False)


class PipelineSandboxServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], runtime_root: Path) -> None:
        self.runtime_root = runtime_root.resolve()
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        self.services: dict[str, subprocess.Popen[Any]] = {}
        self.service_logs: dict[str, Path] = {}
        self.service_lock = threading.RLock()
        super().__init__(address, PipelineSandboxHandler)

    def service_status(self, name: str) -> dict[str, Any]:
        definition = SERVICE_DEFINITIONS[name]
        with self.service_lock:
            process = self.services.get(name)
        alive = _http_alive(int(definition["port"]), str(definition["health"]))
        return {
            "status": "success",
            "service": name,
            "running": process is not None and process.poll() is None,
            "healthy": alive,
            "pid": process.pid if process is not None and process.poll() is None else None,
            "return_code": process.poll() if process is not None else None,
            "log_path": str(self.service_logs.get(name) or ""),
        }

    def start_service(self, name: str, environment: dict[str, str]) -> dict[str, Any]:
        if name not in SERVICE_DEFINITIONS:
            raise ValueError(f"unknown service: {name}")
        status = self.service_status(name)
        if status["healthy"]:
            return status
        definition = SERVICE_DEFINITIONS[name]
        with self.service_lock:
            previous = self.services.get(name)
            if previous is not None and previous.poll() is None:
                return self.service_status(name)
            runtime = self._prepare_service(name)
            log_path = runtime / "service.log"
            log_handle = log_path.open("ab", buffering=0)
            env = self._service_environment(environment)
            executable = (
                runtime / str(definition["directory"]) / "bin" / str(definition["executable"])
            )
            config_path = runtime / "service-config.yml"
            process = subprocess.Popen(
                [str(executable), "server", str(config_path)],
                cwd=runtime,
                env=env,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            log_handle.close()
            self.services[name] = process
            self.service_logs[name] = log_path
        timeout = 1200 if name == "softcite" else 600
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if _http_alive(int(definition["port"]), str(definition["health"])):
                return self.service_status(name)
            if process.poll() is not None:
                raise RuntimeError(
                    f"{name} exited with code {process.returncode}: {_tail(log_path, 8000)}"
                )
            time.sleep(2)
        self.stop_service(name)
        raise TimeoutError(f"{name} did not become healthy within {timeout}s")

    def stop_service(self, name: str) -> dict[str, Any]:
        if name not in SERVICE_DEFINITIONS:
            raise ValueError(f"unknown service: {name}")
        with self.service_lock:
            process = self.services.get(name)
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=10)
        with self.service_lock:
            self.services.pop(name, None)
        return {"status": "success", "service": name, "running": False, "healthy": False}

    def _prepare_service(self, name: str) -> Path:
        definition = SERVICE_DEFINITIONS[name]
        distribution = Path(definition["distribution"])
        config_source = Path(definition["config"])
        if not distribution.is_file():
            raise FileNotFoundError(f"service distribution is missing: {distribution}")
        if not config_source.is_file():
            raise FileNotFoundError(f"service config is missing: {config_source}")
        runtime = self.runtime_root / "services" / name
        executable = runtime / str(definition["directory"]) / "bin" / str(definition["executable"])
        if not executable.is_file():
            shutil.rmtree(runtime, ignore_errors=True)
            runtime.mkdir(parents=True, exist_ok=True)
            _safe_zip_extract(distribution, runtime)
        executable.chmod(executable.stat().st_mode | 0o100)
        config = yaml.safe_load(config_source.read_text(encoding="utf-8")) or {}
        self._rewrite_service_config(name, config, runtime)
        (runtime / "tmp").mkdir(parents=True, exist_ok=True)
        (runtime / "logs").mkdir(parents=True, exist_ok=True)
        (runtime / "service-config.yml").write_text(
            yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        self._ensure_local_jdk()
        return runtime

    def _rewrite_service_config(self, name: str, config: dict[str, Any], runtime: Path) -> None:
        grobid_home = str((DATA_PIPELINE_ROOT / ".model_cache/grobid-home").resolve())
        if name == "grobid":
            grobid = config.setdefault("grobid", {})
            grobid["grobidHome"] = grobid_home
            grobid["temp"] = str(runtime / "tmp")
            (grobid.setdefault("delft", {}))["install"] = str(
                (DATA_PIPELINE_ROOT / "third_party/delft").resolve()
            )
            return
        config["grobidHome"] = grobid_home
        if name == "softcite":
            config["corpusPath"] = str(
                (DATA_PIPELINE_ROOT / "third_party/software-mentions/resources/dataset").resolve()
            )
            config["tmpPath"] = str(runtime / "tmp")
            config["pub2teiPath"] = str((DATA_PIPELINE_ROOT / "third_party/Pub2TEI").resolve())
            _rewrite_file_appenders(config.get("logging"), runtime / "logs")
        elif name == "quantities":
            config["cleanlpModelPath"] = str(
                (DATA_PIPELINE_ROOT / ".model_cache/grobid-quantities/clearnlp-models").resolve()
            )
            _rewrite_file_appenders(config.get("logging"), runtime / "logs")

    def _ensure_local_jdk(self) -> Path:
        source = DATA_PIPELINE_ROOT / ".envs/researchchem-data-pipeline/lib/jvm"
        destination = self.runtime_root / "jdk"
        java = destination / "bin/java"
        if java.is_file():
            return destination
        if not (source / "bin/java").is_file():
            raise FileNotFoundError(f"OpenJDK runtime is missing: {source}")
        temporary = self.runtime_root / "jdk.tmp"
        shutil.rmtree(temporary, ignore_errors=True)
        shutil.copytree(source, temporary, symlinks=False)
        if destination.exists():
            shutil.rmtree(destination)
        os.replace(temporary, destination)
        return destination

    def _service_environment(self, extra: dict[str, str]) -> dict[str, str]:
        prefix = DATA_PIPELINE_ROOT / ".envs/researchchem-data-pipeline"
        jdk = self.runtime_root / "jdk"
        environment = os.environ.copy()
        environment.update({str(key): str(value) for key, value in extra.items()})
        environment.update(
            {
                "JAVA_HOME": str(jdk),
                "GROBID_JAVA_HOME": str(jdk),
                "CONDA_PREFIX": str(prefix),
                "PATH": f"{jdk / 'bin'}:{prefix / 'bin'}:{environment.get('PATH', '')}",
                "PYTHONPATH": os.pathsep.join(
                    [
                        str(DATA_PIPELINE_ROOT / "third_party/delft"),
                        str(prefix / "lib/python3.11/site-packages"),
                        environment.get("PYTHONPATH", ""),
                    ]
                ).strip(os.pathsep),
                "LD_LIBRARY_PATH": os.pathsep.join(
                    [
                        str(jdk / "lib/server"),
                        str(prefix / "lib"),
                        environment.get("LD_LIBRARY_PATH", ""),
                    ]
                ).strip(os.pathsep),
                "TMPDIR": str(self.runtime_root / "tmp"),
            }
        )
        Path(environment["TMPDIR"]).mkdir(parents=True, exist_ok=True)
        return environment

    def start_mineru_job(self, job_id: str, value: dict[str, Any]) -> dict[str, Any]:
        job_id = _safe_identifier(job_id, label="job_id")
        job_root = self.runtime_root / "mineru-jobs" / job_id
        status_path = job_root / "status.json"
        if status_path.is_file():
            current = json.loads(status_path.read_text(encoding="utf-8"))
            if current.get("status") in {"queued", "running"}:
                return {"status": "success", "job": current}
        job_root.mkdir(parents=True, exist_ok=True)
        specification = dict(value)
        _atomic_json(
            status_path,
            {"status": "queued", "job_id": job_id, "created_at": _now()},
        )
        thread = threading.Thread(
            target=self._run_mineru_job,
            args=(job_id, specification),
            daemon=True,
        )
        thread.start()
        return {"status": "success", "job": {"status": "queued", "job_id": job_id}}

    def _run_mineru_job(self, job_id: str, value: dict[str, Any]) -> None:
        job_root = self.runtime_root / "mineru-jobs" / job_id
        status_path = job_root / "status.json"
        output = job_root / "output"
        output.mkdir(parents=True, exist_ok=True)
        source = Path(str(value["source_path"])).expanduser().resolve()
        if not source.is_file():
            _atomic_json(status_path, {"status": "failed", "error": f"missing input: {source}"})
            return
        prefix = DATA_PIPELINE_ROOT / ".envs/researchchem-data-pipeline"
        command = str(value.get("command") or "mineru")
        executable = Path(command)
        if not executable.is_absolute():
            executable = prefix / "bin" / command
        cli = [
            str(executable),
            "-p",
            str(source),
            "-o",
            str(output),
            "-m",
            str(value.get("method") or "auto"),
        ]
        if value.get("backend"):
            cli.extend(["-b", str(value["backend"])])
        cli.extend(str(item) for item in value.get("extra_args") or [])
        environment = os.environ.copy()
        environment.update(
            {str(key): str(item) for key, item in (value.get("environment") or {}).items()}
        )
        environment["CONDA_PREFIX"] = str(prefix)
        environment["PATH"] = f"{prefix / 'bin'}:{environment.get('PATH', '')}"
        environment["LD_LIBRARY_PATH"] = os.pathsep.join(
            [str(prefix / "lib"), environment.get("LD_LIBRARY_PATH", "")]
        ).strip(os.pathsep)
        started = time.monotonic()
        _atomic_json(
            status_path,
            {"status": "running", "job_id": job_id, "started_at": _now(), "command": cli},
        )
        try:
            with (
                (job_root / "stdout.log").open("wb") as stdout,
                (job_root / "stderr.log").open("wb") as stderr,
            ):
                completed = subprocess.run(
                    cli,
                    stdout=stdout,
                    stderr=stderr,
                    timeout=int(value.get("timeout_seconds") or 3600),
                    check=False,
                    env=environment,
                    cwd=str(DATA_PIPELINE_ROOT / ".model_cache"),
                )
            status = "success" if completed.returncode == 0 else "failed"
            error = None if completed.returncode == 0 else f"MinerU exited {completed.returncode}"
            _atomic_json(
                status_path,
                {
                    "status": status,
                    "job_id": job_id,
                    "return_code": completed.returncode,
                    "error": error,
                    "finished_at": _now(),
                    "duration_seconds": round(time.monotonic() - started, 3),
                },
            )
        except subprocess.TimeoutExpired as exc:
            _atomic_json(
                status_path,
                {
                    "status": "timeout",
                    "job_id": job_id,
                    "error": str(exc),
                    "finished_at": _now(),
                    "duration_seconds": round(time.monotonic() - started, 3),
                },
            )
        except Exception as exc:
            _atomic_json(
                status_path,
                {
                    "status": "failed",
                    "job_id": job_id,
                    "error": f"{type(exc).__name__}: {exc}",
                    "finished_at": _now(),
                    "duration_seconds": round(time.monotonic() - started, 3),
                },
            )


class PipelineSandboxHandler(BaseHTTPRequestHandler):
    server: PipelineSandboxServer

    def log_message(self, format: str, *args: Any) -> None:
        print(f"data-pipeline-sandbox-worker: {format % args}", file=sys.stderr, flush=True)

    def _segments(self) -> list[str]:
        return [unquote(item) for item in urlsplit(self.path).path.split("/") if item]

    def _body_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        value = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        if not isinstance(value, dict):
            raise ValueError("request body must be a JSON object")
        return value

    def _json(self, status: int, value: dict[str, Any]) -> None:
        payload = json.dumps(value, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _error(self, status: int, code: str, message: str) -> None:
        self._json(status, {"status": "failed", "error": {"code": code, "message": message}})

    def do_GET(self) -> None:  # noqa: N802
        try:
            segments = self._segments()
            if segments == ["health"]:
                self._json(
                    HTTPStatus.OK,
                    {
                        "status": "success",
                        "service": "researchchem-data-pipeline-sandbox-worker",
                        "pid": os.getpid(),
                        "runtime_root": str(self.server.runtime_root),
                    },
                )
                return
            if len(segments) == 4 and segments[:2] == ["v1", "services"]:
                name, operation = segments[2], segments[3]
                if name not in SERVICE_DEFINITIONS:
                    self._error(HTTPStatus.NOT_FOUND, "unknown_service", name)
                    return
                if operation == "status":
                    self._json(HTTPStatus.OK, self.server.service_status(name))
                    return
                if operation == "logs":
                    log_path = self.server.service_logs.get(name)
                    self._json(
                        HTTPStatus.OK,
                        {
                            "status": "success",
                            "service": name,
                            "log": _tail(log_path) if log_path else "",
                        },
                    )
                    return
            if len(segments) == 5 and segments[:3] == ["v1", "mineru", "jobs"]:
                job_id, operation = segments[3], segments[4]
                job_root = self.server.runtime_root / "mineru-jobs" / _safe_identifier(job_id)
                if operation == "status":
                    status_path = job_root / "status.json"
                    if not status_path.is_file():
                        self._error(HTTPStatus.NOT_FOUND, "job_missing", job_id)
                        return
                    self._json(
                        HTTPStatus.OK,
                        {
                            "status": "success",
                            "job": json.loads(status_path.read_text(encoding="utf-8")),
                            "stdout_tail": _tail(job_root / "stdout.log", 8000),
                            "stderr_tail": _tail(job_root / "stderr.log", 8000),
                        },
                    )
                    return
                if operation == "archive":
                    output = job_root / "output"
                    if not output.is_dir():
                        self._error(HTTPStatus.NOT_FOUND, "job_output_missing", job_id)
                        return
                    archive_path = job_root / "output.tar.gz"
                    with tarfile.open(archive_path, "w:gz", dereference=True) as archive:
                        _add_tree(archive, output, root=job_root, arcname="output")
                    payload_size = archive_path.stat().st_size
                    self.send_response(HTTPStatus.OK)
                    self.send_header("Content-Type", "application/gzip")
                    self.send_header("Content-Length", str(payload_size))
                    self.end_headers()
                    with archive_path.open("rb") as handle:
                        shutil.copyfileobj(handle, self.wfile, length=1024 * 1024)
                    return
            self._error(HTTPStatus.NOT_FOUND, "not_found", self.path)
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "worker_exception", str(exc))

    def do_POST(self) -> None:  # noqa: N802
        try:
            segments = self._segments()
            if len(segments) == 4 and segments[:2] == ["v1", "services"]:
                name, operation = segments[2], segments[3]
                value = self._body_json()
                if operation == "start":
                    self._json(
                        HTTPStatus.OK,
                        self.server.start_service(
                            name,
                            {
                                str(key): str(item)
                                for key, item in (value.get("environment") or {}).items()
                            },
                        ),
                    )
                    return
                if operation == "stop":
                    self._json(HTTPStatus.OK, self.server.stop_service(name))
                    return
            if len(segments) == 5 and segments[:3] == ["v1", "mineru", "jobs"]:
                job_id, operation = segments[3], segments[4]
                if operation == "start":
                    self._json(
                        HTTPStatus.ACCEPTED,
                        self.server.start_mineru_job(job_id, self._body_json()),
                    )
                    return
            self._error(HTTPStatus.NOT_FOUND, "not_found", self.path)
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "worker_exception", str(exc))

    def do_DELETE(self) -> None:  # noqa: N802
        try:
            segments = self._segments()
            if len(segments) == 4 and segments[:3] == ["v1", "mineru", "jobs"]:
                job_id = _safe_identifier(segments[3])
                shutil.rmtree(self.server.runtime_root / "mineru-jobs" / job_id, ignore_errors=True)
                self._json(HTTPStatus.OK, {"status": "success", "job_id": job_id})
                return
            self._error(HTTPStatus.NOT_FOUND, "not_found", self.path)
        except Exception as exc:
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "worker_exception", str(exc))


def _rewrite_file_appenders(logging: Any, log_root: Path) -> None:
    if not isinstance(logging, dict):
        return
    for index, appender in enumerate(logging.get("appenders") or []):
        if not isinstance(appender, dict) or appender.get("type") != "file":
            continue
        appender["currentLogFilename"] = str(log_root / f"application-{index}.log")
        if appender.get("archivedLogFilenamePattern"):
            appender["archivedLogFilenamePattern"] = str(
                log_root / f"application-{index}-%d.log.gz"
            )


def _http_alive(port: int, path: str) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=3) as response:
            payload = response.read().decode("utf-8", errors="replace").strip().casefold()
            return response.status == 200 and payload in {"true", "ok"}
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=44773)
    parser.add_argument("--runtime-root", type=Path, required=True)
    args = parser.parse_args(argv)
    server = PipelineSandboxServer((args.host, args.port), args.runtime_root)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for name in list(server.services):
            server.stop_service(name)
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

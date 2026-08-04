from __future__ import annotations

import contextlib
import os
import shlex
import signal
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterator


class ManagedServiceError(RuntimeError):
    pass


def service_is_alive(base_url: str, path: str, timeout_seconds: int = 5) -> bool:
    try:
        with urllib.request.urlopen(
            f"{base_url.rstrip('/')}/{path.lstrip('/')}", timeout=timeout_seconds
        ) as response:
            payload = response.read().decode("utf-8", errors="replace").strip().casefold()
            return response.status == 200 and payload == "true"
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False


@contextlib.contextmanager
def managed_service(
    config: dict[str, Any],
    *,
    service_name: str,
    health_path: str = "/service/isalive",
) -> Iterator[None]:
    base_url = str(config["base_url"])
    if service_is_alive(base_url, health_path):
        yield
        return
    if not config.get("auto_start", True):
        raise ManagedServiceError(f"{service_name} is not reachable at {base_url}")

    working_directory = Path(config["working_directory"]).expanduser().resolve()
    if not working_directory.is_dir():
        raise ManagedServiceError(
            f"{service_name} working directory does not exist: {working_directory}"
        )
    raw_command = config.get("start_command") or ["./gradlew", "--no-daemon", "run"]
    command = shlex.split(raw_command) if isinstance(raw_command, str) else list(raw_command)
    log_path = Path(config["service_log"]).expanduser().resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    environment = os.environ.copy()
    environment.update(
        {str(key): str(value) for key, value in (config.get("environment") or {}).items()}
    )
    java_home = config.get("java_home") or environment.get("GROBID_JAVA_HOME")
    if java_home:
        environment["JAVA_HOME"] = str(java_home)
        environment["PATH"] = f"{Path(java_home) / 'bin'}:{environment.get('PATH', '')}"

    log_handle = log_path.open("a", encoding="utf-8")
    process = subprocess.Popen(
        command,
        cwd=working_directory,
        env=environment,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    startup_timeout = int(config.get("startup_timeout_seconds", 600))
    deadline = time.monotonic() + startup_timeout
    try:
        while time.monotonic() < deadline:
            if service_is_alive(base_url, health_path):
                yield
                return
            if process.poll() is not None:
                raise ManagedServiceError(
                    f"{service_name} exited with code {process.returncode}; inspect {log_path}"
                )
            time.sleep(2)
        raise ManagedServiceError(
            f"{service_name} did not become ready within {startup_timeout}s; inspect {log_path}"
        )
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=10)
        log_handle.close()

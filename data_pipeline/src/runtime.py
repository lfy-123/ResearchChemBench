from __future__ import annotations

import contextlib
import os
import subprocess
import threading
import time
import urllib.error
import urllib.request
import warnings
from pathlib import Path
from typing import Any, Iterator

from src.contracts import read_json


class ManagedScreeningServiceError(RuntimeError):
    """The run-scoped screening endpoint could not be recovered."""


class ManagedScreeningServiceGuard:
    """Rate-limited health checks and serialized recovery for one managed worker."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = dict(config)
        self._lock = threading.Lock()
        self._last_check = 0.0
        self._interval = max(1.0, float(config.get("health_check_interval_seconds", 15)))
        self._timeout = max(1.0, float(config.get("health_check_timeout_seconds", 5)))

    def ensure_healthy(self) -> None:
        now = time.monotonic()
        if now - self._last_check < self._interval:
            return
        with self._lock:
            now = time.monotonic()
            if now - self._last_check < self._interval:
                return
            if not self._healthy():
                self._recover_locked()
            self._last_check = time.monotonic()

    def recover(self) -> None:
        with self._lock:
            if self._healthy():
                self._last_check = time.monotonic()
                return
            self._recover_locked()
            self._last_check = time.monotonic()

    def _recover_locked(self) -> None:
        manager = Path(str(self.config["manager_script"])).expanduser().resolve()
        state_file = Path(str(self.config["state_file"])).expanduser().resolve()
        try:
            result = subprocess.run(
                ["bash", str(manager), "recover-screening", "--state", str(state_file)],
                check=False,
                capture_output=True,
                text=True,
                timeout=max(
                    30.0, float(self.config.get("health_recovery_timeout_seconds", 1800))
                ),
            )
        except subprocess.TimeoutExpired as exc:
            raise ManagedScreeningServiceError(
                "managed screening service recovery timed out"
            ) from exc
        if result.returncode or not self._healthy():
            detail = (result.stderr or result.stdout or "health check still failing").strip()
            raise ManagedScreeningServiceError(
                f"managed screening service recovery failed: {detail[:1000]}"
            )

    def _healthy(self) -> bool:
        base_url = str(self.config.get("base_url") or "").rstrip("/")
        if not base_url:
            return False
        request = urllib.request.Request(
            f"{base_url}/models",
            headers={"Authorization": f"Bearer {self._api_key()}"},
        )
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with opener.open(request, timeout=self._timeout) as response:
                return 200 <= int(response.status) < 300
        except (OSError, TimeoutError, urllib.error.URLError, urllib.error.HTTPError):
            return False

    def _api_key(self) -> str:
        key_name = str(self.config.get("api_key_env") or "RCB_SCREENING_API_KEY")
        return os.environ.get(key_name, "EMPTY")


def ensure_managed_screening_worker(model_config: dict[str, Any]) -> None:
    """Create or health-check the run-scoped screening worker."""

    config = dict(model_config)
    if not config.get("managed_rlaunch"):
        return
    manager = Path(str(config["manager_script"])).expanduser().resolve()
    state_file = Path(str(config["state_file"])).expanduser().resolve()
    if not manager.is_file():
        raise FileNotFoundError(f"screening model manager does not exist: {manager}")
    if state_file.is_file():
        state = read_json(state_file)
        service = str(state.get("service") or "screening")
        if service != "screening":
            subprocess.run(
                ["bash", str(manager), "start-screening", "--state", str(state_file)],
                check=True,
            )
            return
        status = subprocess.run(
            ["bash", str(manager), "status", "--state", str(state_file)],
            check=False,
            capture_output=True,
            text=True,
        )
        if status.returncode == 0:
            return
        cleanup = subprocess.run(
            ["bash", str(manager), "stop", "--state", str(state_file)], check=False
        )
        if cleanup.returncode or state_file.exists():
            raise RuntimeError(
                "screening worker state exists but is not healthy and could not be "
                f"cleaned safely: {state_file}"
            )
    subprocess.run(_start_command(config, manager, state_file), check=True)


def stop_managed_screening_worker(model_config: dict[str, Any]) -> None:
    config = dict(model_config)
    if not config.get("managed_rlaunch"):
        return
    manager = Path(str(config["manager_script"])).expanduser().resolve()
    state_file = Path(str(config["state_file"])).expanduser().resolve()
    result = subprocess.run(["bash", str(manager), "stop", "--state", str(state_file)], check=False)
    if result.returncode:
        warnings.warn(
            f"screening worker cleanup failed; run: bash {manager} stop --state {state_file}",
            RuntimeWarning,
            stacklevel=2,
        )


def _start_command(config: dict[str, Any], manager: Path, state_file: Path) -> list[str]:
    command = [
        "bash",
        str(manager),
        "start",
        "--state",
        str(state_file),
        "--cpu",
        str(config.get("cpu", 16)),
        "--memory",
        str(config.get("memory_mib", 196000)),
        "--charged-group",
        str(config.get("charged_group", "ai4chem_gpu")),
        "--positive-tag",
        str(config.get("positive_tag", "")),
        "--image",
        str(config.get("image", "")),
    ]
    if config.get("skip_bootstrap"):
        command.append("--skip-bootstrap")
    if config.get("skip_download"):
        command.append("--skip-download")
    if config.get("existing_worker"):
        command.extend(["--existing-worker", str(config["existing_worker"])])
    return command


@contextlib.contextmanager
def screening_model_runtime(
    model_config: dict[str, Any], *, preserve_worker: bool = False
) -> Iterator[dict[str, Any]]:
    """Start one managed screening worker for both Stage03 and Stage04."""

    config = dict(model_config)
    if not config.get("managed_rlaunch"):
        yield config
        return
    state_file = Path(str(config["state_file"])).expanduser().resolve()
    ensure_managed_screening_worker(config)
    state = read_json(state_file)
    config["base_url"] = state["base_url"]
    config["model"] = state["model"]
    key_name = str(config.get("api_key_env") or "RCB_SCREENING_API_KEY")
    previous_key = os.environ.get(key_name)
    os.environ[key_name] = str(state.get("api_key") or "EMPTY")
    config["_managed_service_guard"] = ManagedScreeningServiceGuard(config)
    try:
        yield config
    finally:
        if previous_key is None:
            os.environ.pop(key_name, None)
        else:
            os.environ[key_name] = previous_key
        if preserve_worker:
            _manager_action(config, "release-screening")
        else:
            stop_managed_screening_worker(config)


def start_managed_mineru_service(
    model_config: dict[str, Any], mineru_config: dict[str, Any]
) -> dict[str, Any]:
    """Replace Qwen with a persistent MinerU API on the same rlaunch worker."""

    if not model_config.get("managed_rlaunch"):
        return dict(mineru_config)
    manager = Path(str(model_config["manager_script"])).expanduser().resolve()
    state_file = Path(str(model_config["state_file"])).expanduser().resolve()
    command = [
        "bash",
        str(manager),
        "start-mineru",
        "--state",
        str(state_file),
        "--mineru-env",
        str(mineru_config.get("gpu_env_dir")),
        "--mineru-config",
        str((mineru_config.get("environment") or {}).get("MINERU_TOOLS_CONFIG_JSON")),
        "--mineru-concurrency",
        str(mineru_config.get("api_concurrency", 3)),
    ]
    subprocess.run(command, check=True)
    state = read_json(state_file)
    updated = dict(mineru_config)
    updated["api_url"] = state["base_url"]
    extra_args = list(updated.get("extra_args") or [])
    if "--api-url" not in extra_args:
        extra_args.extend(["--api-url", state["base_url"]])
    updated["extra_args"] = extra_args
    updated["execution"] = "managed_gpu"
    return updated


def _manager_action(config: dict[str, Any], action: str) -> None:
    manager = Path(str(config["manager_script"])).expanduser().resolve()
    state_file = Path(str(config["state_file"])).expanduser().resolve()
    subprocess.run(["bash", str(manager), action, "--state", str(state_file)], check=True)

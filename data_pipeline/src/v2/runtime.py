from __future__ import annotations

import contextlib
import os
import subprocess
import warnings
from pathlib import Path
from typing import Any, Iterator

from src.v2.contracts import read_json


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

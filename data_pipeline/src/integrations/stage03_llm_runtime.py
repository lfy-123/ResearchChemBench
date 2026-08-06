from __future__ import annotations

import contextlib
import os
import subprocess
from pathlib import Path
from typing import Any, Iterator

from src.core.io import read_json
from src.core.logging import pipeline_logger


@contextlib.contextmanager
def stage03_llm_runtime(config: dict[str, Any]) -> Iterator[dict[str, Any]]:
    stage = config.get("stage03_computation_relevance") or {}
    llm = stage.get("llm") or {}
    if not stage.get("use_llm") or not llm.get("enabled"):
        yield config
        return

    if not llm.get("managed_rlaunch"):
        llm["api_key"] = os.environ.get(str(llm.get("api_key_env") or ""), "EMPTY")
        yield config
        return

    manager = Path(str(llm["manager_script"])).expanduser().resolve()
    state_file = Path(str(llm["state_file"])).expanduser().resolve()
    if not manager.is_file():
        raise FileNotFoundError(f"Stage 03 LLM manager script does not exist: {manager}")
    try:
        command = [
            "bash",
            str(manager),
            "start",
            "--state",
            str(state_file),
            "--cpu",
            str(llm.get("cpu", 16)),
            "--memory",
            str(llm.get("memory_mib", 196000)),
            "--charged-group",
            str(llm.get("charged_group", "ai4chem_gpu")),
            "--positive-tag",
            str(llm.get("positive_tag", "h200")),
            "--image",
            str(llm.get("image", "")),
        ]
        if llm.get("skip_bootstrap"):
            command.append("--skip-bootstrap")
        if llm.get("skip_download"):
            command.append("--skip-download")
        pipeline_logger().info("STAGE03 LLM WORKER START | state=%s", state_file)
        subprocess.run(command, check=True)
        state_value = read_json(state_file)
        llm["base_url"] = state_value["base_url"]
        llm["api_key"] = state_value["api_key"]
        llm["model"] = state_value["model"]
        llm["worker_token"] = state_value["worker_token"]
        pipeline_logger().info(
            "STAGE03 LLM WORKER READY | worker=%s | base_url=%s",
            state_value["worker_token"],
            state_value["base_url"],
        )
    except Exception as exc:
        if llm.get("required"):
            raise
        pipeline_logger().exception(
            "STAGE03 managed LLM startup failed; continuing with rule fallback: %s", exc
        )
        if state_file.is_file():
            subprocess.run(
                ["bash", str(manager), "stop", "--state", str(state_file)], check=False
            )
        llm["enabled"] = False
        yield config
        return

    try:
        yield config
    finally:
        pipeline_logger().info("STAGE03 LLM WORKER STOP | state=%s", state_file)
        result = subprocess.run(
            ["bash", str(manager), "stop", "--state", str(state_file)], check=False
        )
        if result.returncode:
            pipeline_logger().error(
                "STAGE03 LLM worker cleanup failed; retry with: bash %s stop --state %s",
                manager,
                state_file,
            )


__all__ = ["stage03_llm_runtime"]

"""Workspace construction and external agent CLI execution."""

from __future__ import annotations

import subprocess
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.catalog import (
    resolve_tool_discovery_mode,
)
from chemistry_toolbox.src.distributed_pool import pool_snapshot

from ..repository import load_task_info, load_task_text
from ..settings import (
    AGENT_PRESETS,
    DEFAULT_AGENT_TIMEOUT_SECONDS,
    DEFAULT_AVAILABLE_CPU_CORES,
    DEFAULT_AVAILABLE_GPU_COUNT,
    DEFAULT_AVAILABLE_MEMORY_MB,
    DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
    DEFAULT_EXECUTION_MODE,
    DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
    DEFAULT_JOB_EVENT_MAX_BATCH_SECONDS,
    DEFAULT_JOB_EVENT_SETTLE_SECONDS,
    DEFAULT_JOB_FAILURE_TAIL_CHARS,
    DEFAULT_JOB_INTERNAL_POLL_INTERVAL_SECONDS,
    DEFAULT_JOB_WAIT_HEARTBEAT_SECONDS,
    DEFAULT_LIVE_PROGRESS,
    DEFAULT_MAX_TURNS,
    DEFAULT_MCP_TOOL_TIMEOUT_MS,
    DEFAULT_PROGRESS_CONSOLE,
    DEFAULT_PROGRESS_MAX_CHARS,
    TASKS_DIR,
    WORKSPACES_DIR,
)
from .agent_adapter import AgentAdapterMixin
from .lifecycle import RunLifecycleMixin
from .workspace import WorkspaceLifecycleMixin


class TaskRunner(
    WorkspaceLifecycleMixin,
    AgentAdapterMixin,
    RunLifecycleMixin,
):
    """Set up one benchmark workspace and run one configured agent."""

    def __init__(
        self,
        task_id: str,
        *,
        agent_key: str = "mock",
        workspace_root: Path | None = None,
        timeout_seconds: int = DEFAULT_AGENT_TIMEOUT_SECONDS,
        compute_action_timeout_seconds: int = DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
        fast_action_timeout_seconds: int = DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
        mcp_tool_timeout_ms: int = DEFAULT_MCP_TOOL_TIMEOUT_MS,
        available_cpu_cores: int = DEFAULT_AVAILABLE_CPU_CORES,
        available_memory_mb: int = DEFAULT_AVAILABLE_MEMORY_MB,
        available_gpu_count: int = DEFAULT_AVAILABLE_GPU_COUNT,
        job_event_settle_seconds: int = DEFAULT_JOB_EVENT_SETTLE_SECONDS,
        job_event_max_batch_seconds: int = DEFAULT_JOB_EVENT_MAX_BATCH_SECONDS,
        job_wait_heartbeat_seconds: int | None = None,
        job_internal_poll_interval_seconds: int = DEFAULT_JOB_INTERNAL_POLL_INTERVAL_SECONDS,
        job_failure_tail_chars: int = DEFAULT_JOB_FAILURE_TAIL_CHARS,
        max_turns: int = DEFAULT_MAX_TURNS,
        tool_discovery_mode: str | None = None,
        live_progress: bool = DEFAULT_LIVE_PROGRESS,
        progress_console: bool = DEFAULT_PROGRESS_CONSOLE,
        progress_max_chars: int = DEFAULT_PROGRESS_MAX_CHARS,
        execution_mode: str = DEFAULT_EXECUTION_MODE,
    ):
        if agent_key not in AGENT_PRESETS:
            raise ValueError(f"Unknown agent preset: {agent_key}")
        self.task_id = task_id
        self.task_dir = TASKS_DIR / task_id
        self.task_info = load_task_info(task_id)
        self.task_text = load_task_text(task_id)
        self.agent_key = agent_key
        self.agent = AGENT_PRESETS[agent_key]
        self.agent_name = self.agent["label"]
        self.timeout_seconds = timeout_seconds
        self.compute_action_timeout_seconds = int(compute_action_timeout_seconds)
        self.fast_action_timeout_seconds = int(fast_action_timeout_seconds)
        self.mcp_tool_timeout_ms = int(mcp_tool_timeout_ms)
        self.available_cpu_cores = int(available_cpu_cores)
        self.available_memory_mb = int(available_memory_mb)
        self.available_gpu_count = int(available_gpu_count)
        self.job_event_settle_seconds = int(job_event_settle_seconds)
        self.job_event_max_batch_seconds = int(job_event_max_batch_seconds)
        self.job_wait_heartbeat_seconds = int(
            job_wait_heartbeat_seconds
            if job_wait_heartbeat_seconds is not None
            else min(
                DEFAULT_JOB_WAIT_HEARTBEAT_SECONDS,
                max(1, (self.mcp_tool_timeout_ms // 1000) - 1),
            )
        )
        self.job_internal_poll_interval_seconds = int(job_internal_poll_interval_seconds)
        self.job_failure_tail_chars = int(job_failure_tail_chars)
        self.execution_mode = str(execution_mode).strip().casefold()
        if self.execution_mode not in {"local", "distributed"}:
            raise ValueError("execution_mode must be local or distributed")
        if self.available_cpu_cores < 1:
            raise ValueError("available_cpu_cores must be positive")
        if self.available_memory_mb < 128:
            raise ValueError("available_memory_mb must be >= 128")
        if self.available_gpu_count < 0:
            raise ValueError("available_gpu_count must be non-negative")
        if min(
            self.job_event_settle_seconds,
            self.job_event_max_batch_seconds,
            self.job_wait_heartbeat_seconds,
            self.job_internal_poll_interval_seconds,
            self.job_failure_tail_chars,
        ) < 1:
            raise ValueError("job supervision settings must be positive")
        if self.job_event_max_batch_seconds < self.job_event_settle_seconds:
            raise ValueError(
                "job_event_max_batch_seconds must be >= job_event_settle_seconds"
            )
        if self.job_wait_heartbeat_seconds < self.job_event_max_batch_seconds:
            raise ValueError(
                "job_wait_heartbeat_seconds must be >= job_event_max_batch_seconds"
            )
        self.max_turns = max_turns
        self.tool_discovery_mode = resolve_tool_discovery_mode(tool_discovery_mode)
        self.live_progress = bool(live_progress)
        self.progress_console = bool(progress_console)
        self.progress_max_chars = max(80, int(progress_max_chars))
        self.timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.run_id = f"{task_id}_{agent_key}_{self.timestamp}_{uuid.uuid4().hex[:6]}"
        root = Path(workspace_root) if workspace_root else WORKSPACES_DIR
        self.workspace = root / self.run_id
        self.meta_path = self.workspace / "_meta.json"
        self.output_path = self.workspace / "_agent_output.jsonl"
        self.instructions_path = self.workspace / "INSTRUCTIONS.md"
        self.final_message_path = self.workspace / "_final_message.txt"
        self.process: subprocess.Popen[str] | None = None
        self.process_group_id: int | None = None
        self.thread: threading.Thread | None = None
        self._stop_requested = False
        self._opencode_runtime_database: Path | None = None

    def resource_budget_record(self) -> dict[str, Any]:
        if self.execution_mode == "distributed":
            snapshot = pool_snapshot()
            return {
                "cpu_cores": snapshot["maximum_cpu_cores_per_job"],
                "memory_mb": snapshot["maximum_memory_mb_per_job"],
                "gpu_count": max(
                    (
                        worker["capacity"]["gpu_count"]
                        for worker in snapshot["workers"]
                    ),
                    default=0,
                ),
                "source": "distributed_compute_pool",
                "agent_controllable": False,
                "scope": "per_job_on_one_compute_worker",
                **snapshot,
            }
        return {
            "cpu_cores": self.available_cpu_cores,
            "memory_mb": self.available_memory_mb,
            "gpu_count": self.available_gpu_count,
            "source": "evaluation_policy",
            "agent_controllable": False,
            "scope": "per_task",
        }

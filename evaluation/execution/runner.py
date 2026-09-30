"""Workspace construction and external agent CLI execution."""

from __future__ import annotations

import os
import subprocess
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.catalog import (
    resolve_tool_discovery_mode,
)
from chemistry_toolbox.src.distributed_pool import pool_snapshot

from ..repository import (
    TaskRepository,
    load_task_info,
    load_task_package,
    load_task_text,
)
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
    WORKSPACES_DIR,
)
from .agent_adapter import AgentAdapterMixin
from .lifecycle import RunLifecycleMixin
from .recovery import (
    ControllerLock,
    RunRecoveryError,
    canonical_config_hash,
    load_run_manifest,
    write_run_manifest,
)
from .workspace import WorkspaceLifecycleMixin


class TaskRunner(
    WorkspaceLifecycleMixin,
    AgentAdapterMixin,
    RunLifecycleMixin,
):
    """Set up one benchmark workspace and run one configured agent."""

    def __init__(
        self,
        paper_id: str,
        *,
        task_type: str = "autonomous_research",
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
        recovery_enabled: bool | None = None,
        resume: bool | None = None,
        resume_policy: dict | None = None,
        task_roots: list[str] | None = None,
        task_repository: TaskRepository | None = None,
        agent_definition: dict | None = None,
        codex_model: str | None = None,
        codex_base_url: str | None = None,
        codex_reasoning_effort: str | None = None,
        max_tokens: int | None = None,
        model_wait_strategy: str = "provider_default",
        feedback_schema_version: int = 2,
        native_input_validation_policy: str = "advisory",
        archive_policy: str = "indexed",
        progress_interval: int = 5,
        _saved_identity: dict | None = None,
    ):
        if agent_definition is not None:
            from ..agent_plugins.registry import validate_external_definition
            agent_definition = validate_external_definition(agent_key, agent_definition, config_dir=Path.cwd())
        elif agent_key not in AGENT_PRESETS:
            raise ValueError(f"Unknown agent preset: {agent_key}")
        if task_repository is not None and task_roots is not None:
            raise ValueError("task_repository and task_roots cannot both be supplied")
        self.paper_id = paper_id
        self.task_type = task_type
        self.task_repository = task_repository if task_repository is not None else TaskRepository(task_roots)
        self.task_package = load_task_package(
            paper_id=paper_id,
            task_type=task_type,
            repository=self.task_repository,
        )
        self._task_source = None
        if task_repository is not None:
            self._task_source = {
                "kind": "final_verified" if hasattr(task_repository, "_approved_final_directories") else "explicit_repository",
                "directory": str(self.task_package.directory),
                "package_content_sha256": self.task_package.package_content_sha256,
            }
        self.task_dir = self.task_package.directory
        self.task_info = load_task_info(
            paper_id=paper_id,
            task_type=task_type,
            repository=self.task_repository,
        )
        self.task_text = load_task_text(
            paper_id=paper_id,
            task_type=task_type,
            repository=self.task_repository,
        )
        self.agent_key = agent_key
        self.agent = agent_definition if agent_definition is not None else dict(AGENT_PRESETS[agent_key])
        self.recovery_enabled = (self.agent.get("kind") == "codex" and execution_mode == "local") if recovery_enabled is None else bool(recovery_enabled)
        from .resume_policy import validate_policy
        if resume is not None and not isinstance(resume, bool):
            raise ValueError("resume must be a boolean")
        self.resume_enabled = resume
        self.resume_policy = validate_policy(resume_policy) if resume_policy is not None else None
        if resume:
            if self.agent.get("kind") not in {"codex", "mock"} or execution_mode != "local":
                raise ValueError("resume_unsupported")
            self.recovery_enabled = True
        self._frozen_config = (_saved_identity or {}).get("config")
        saved_config = (_saved_identity or {}).get("config", {})
        self.model_wait_strategy = model_wait_strategy
        self.feedback_schema_version = feedback_schema_version if not _saved_identity else saved_config.get("feedback_schema_version", 1)
        self.native_input_validation_policy = native_input_validation_policy if not _saved_identity else saved_config.get("native_input_validation_policy", "legacy")
        self.archive_policy = archive_policy if not _saved_identity else saved_config.get("archive_policy", "legacy")
        self.progress_interval = int(progress_interval)
        if model_wait_strategy not in {"provider_default", "host_event_wait"}:
            raise ValueError("unsupported model_wait_strategy")
        if self.feedback_schema_version not in {1, 2} or self.native_input_validation_policy not in {"legacy", "advisory"}:
            raise ValueError("unsupported feedback or native input policy")
        if self.archive_policy not in {"legacy", "indexed"} or self.progress_interval < 1:
            raise ValueError("invalid archive_policy or progress_interval")
        self._wait_capability = None
        self._provider_diagnostics = None
        self.max_tokens = max_tokens
        self.codex_model = codex_model or os.environ.get("RCB_CODEX_MODEL", "gpt-5.6-sol")
        self.codex_base_url = codex_base_url or os.environ.get("RCB_CODEX_BASE_URL", "https://api.openai.com/v1")
        from urllib.parse import urlsplit
        parsed = urlsplit(self.codex_base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Codex base URL must be an HTTP(S) URL without embedded credentials")
        if not parsed.path:
            self.codex_base_url = self.codex_base_url.rstrip("/") + "/v1"
        self.codex_reasoning_effort = codex_reasoning_effort or os.environ.get("RCB_CODEX_REASONING_EFFORT", "high")
        if self.agent.get("kind") == "codex":
            self.agent["model"] = self.codex_model
            self.agent["executable"] = os.environ.get("RCB_CODEX_EXECUTABLE", self.agent.get("executable", "codex"))
            from .wait_policy import probe_cli
            self._provider_diagnostics = probe_cli(self.agent["executable"])
            self.agent["executable"] = self._provider_diagnostics["resolved_executable"]
        self.agent_name = self.agent["label"]
        self.timeout_seconds = timeout_seconds
        self.compute_action_timeout_seconds = int(compute_action_timeout_seconds)
        self.fast_action_timeout_seconds = int(fast_action_timeout_seconds)
        self.mcp_tool_timeout_ms = int(mcp_tool_timeout_ms)
        if self.model_wait_strategy == "host_event_wait":
            if self.agent.get("kind") != "codex":
                raise ValueError("host_event_wait currently requires the verified Codex adapter")
            from .wait_policy import codex_wait_capability
            self._wait_capability = codex_wait_capability(self.agent["executable"], diagnostics=self._provider_diagnostics)
            if self.mcp_tool_timeout_ms < (self.timeout_seconds + 60) * 1000:
                raise ValueError("host_event_wait requires mcp_tool_timeout_ms >= (timeout_seconds + 60) * 1000")
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
        if int(timeout_seconds) < 1 or int(max_turns) < 1 or (max_tokens is not None and int(max_tokens) < 1):
            raise ValueError("run timeout, turn budget and token budget must be positive")
        self.max_turns = max_turns
        self.tool_discovery_mode = resolve_tool_discovery_mode(tool_discovery_mode)
        self.live_progress = bool(live_progress)
        self.progress_console = bool(progress_console)
        self.progress_max_chars = max(80, int(progress_max_chars))
        self.timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.run_id = (
            _saved_identity["run_id"] if _saved_identity else f"{task_type}-{paper_id}-{agent_key}-{self.timestamp}-{uuid.uuid4().hex[:6]}"
        )
        root = Path(workspace_root) if workspace_root else WORKSPACES_DIR
        if _saved_identity:
            self.run_id = _saved_identity["run_id"]
            self.timestamp = _saved_identity["timestamp"]
        self.workspace = root / self.run_id
        self.electronic_state_policy = (_saved_identity.get("electronic_state_policy", "legacy") if _saved_identity
                                        else os.environ.get("RESEARCHCHEMBENCH_ELECTRONIC_STATE_POLICY", "strict"))
        if self.electronic_state_policy not in {"strict", "legacy"}:
            raise ValueError("electronic_state_policy must be strict or legacy")
        self.meta_path = self.workspace / "_meta.json"
        self.output_path = self.workspace / "_agent_output.jsonl"
        self.instructions_path = self.workspace / "INSTRUCTIONS.md"
        self.final_message_path = self.workspace / "_final_message.txt"
        self.process: subprocess.Popen[str] | None = None
        self.process_group_id: int | None = None
        self.thread: threading.Thread | None = None
        self._stop_requested = False
        self._opencode_runtime_database: Path | None = None
        self.public_task_files: list[str] = []
        self.attempt_id = "attempt_0001"
        self.first_started_at: str | None = None
        self.deadline_at: str | None = None
        self._restored = False
        self._resume_session_id: str | None = None
        self._recovery_notice: str | None = None
        self._recovery_reconciliation: dict[str, Any] | None = None
        self._controller_lock: ControllerLock | None = None
        self._turn_sequence = 0
        self._provider_cli_version = None
        if self.recovery_enabled and self.execution_mode != "local":
            raise ValueError("recovery supports local execution only")
        if self.agent.get("kind") == "external":
            from ..agent_plugins.external import preflight_external
            preflight_external(self)

    def _run_config(self) -> dict[str, Any]:
        if self._frozen_config is not None:
            return dict(self._frozen_config)
        config = {
            "paper_id": self.paper_id,
            "task_type": self.task_type,
            "agent_key": self.agent_key,
            "timeout_seconds": self.timeout_seconds,
            "compute_action_timeout_seconds": self.compute_action_timeout_seconds,
            "fast_action_timeout_seconds": self.fast_action_timeout_seconds,
            "mcp_tool_timeout_ms": self.mcp_tool_timeout_ms,
            "available_cpu_cores": self.available_cpu_cores,
            "available_memory_mb": self.available_memory_mb,
            "available_gpu_count": self.available_gpu_count,
            "max_turns": self.max_turns,
            "tool_discovery_mode": self.tool_discovery_mode,
            "execution_mode": self.execution_mode,
            "recovery_enabled": self.recovery_enabled,
            "max_tokens": self.max_tokens,
            "codex_model": self.codex_model,
            "codex_base_url": self.codex_base_url,
            "codex_reasoning_effort": self.codex_reasoning_effort,
            "model_wait_strategy": self.model_wait_strategy,
            "feedback_schema_version": self.feedback_schema_version,
            "native_input_validation_policy": self.native_input_validation_policy,
            "archive_policy": self.archive_policy,
            "progress_interval": self.progress_interval,
            "job_event_settle_seconds": self.job_event_settle_seconds,
            "job_event_max_batch_seconds": self.job_event_max_batch_seconds,
            "job_wait_heartbeat_seconds": self.job_wait_heartbeat_seconds,
            "job_internal_poll_interval_seconds": self.job_internal_poll_interval_seconds,
            "job_failure_tail_chars": self.job_failure_tail_chars,
            "live_progress": self.live_progress,
            "progress_console": self.progress_console,
            "progress_max_chars": self.progress_max_chars,
        }
        if self.agent.get("kind") == "external":
            config["agent_definition"] = self.agent
        return config

    def _run_manifest(self) -> dict[str, Any]:
        config = self._run_config()
        manifest = {
            "schema_version": 1,
            "run_id": self.run_id,
            "electronic_state_policy": self.electronic_state_policy,
            "paper_id": self.paper_id,
            "task_type": self.task_type,
            "workspace": str(self.workspace.resolve()),
            "timestamp": self.timestamp,
            "agent_key": self.agent_key,
            "agent_kind": self.agent.get("kind"),
            "git_discovery_boundary": {"policy": "workspace-v1", "workspace": str(self.workspace.resolve()),
                                       "ceiling_parent": str(self.workspace.resolve().parent)},
            "config": config,
            "config_hash": canonical_config_hash(config),
            "task_package_content_sha256": self.task_package.package_content_sha256,
            "first_started_at": self.first_started_at,
            "deadline_at": self.deadline_at,
            "attempt_id": self.attempt_id,
            "provider_session_id": self._resume_session_id,
            "run_state": "recovering" if self._restored else "running",
        }
        if self.agent.get("kind") == "external":
            manifest.update(agent_protocol="rcb-agent-request-v1", execution_backend=self.agent["execution_backend"],
                            model_budget_enforcement=self.agent["model_budget_enforcement"])
        if self._task_source is not None:
            manifest["task_source"] = self._task_source
        return manifest

    def _persist_run_manifest(self, **extra: Any) -> None:
        from .recovery import persist_runner
        persist_runner(self, extra)

    @classmethod
    def create(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            runner = cls(**args[0], **kwargs)
        else:
            runner = cls(*args, **kwargs)
        runner.setup_workspace()
        return runner

    def remaining_run_timeout_seconds(self) -> int:
        if not self.deadline_at:
            return max(1, int(self.timeout_seconds))
        try:
            deadline = datetime.fromisoformat(self.deadline_at).timestamp()
        except ValueError as exc:
            raise RunRecoveryError("invalid run deadline") from exc
        remaining = int(deadline - datetime.now(timezone.utc).timestamp())
        if remaining <= 0:
            raise RunRecoveryError("benchmark run deadline has expired")
        return min(max(1, int(self.timeout_seconds)), remaining)

    @classmethod
    def restore(cls, run_id: str, recovery_root: Path | None = None, *, timeout_seconds: int | None = None) -> "TaskRunner":
        """Load an existing run without creating a new workspace or run ID."""

        from .recovery import restore_runner
        return restore_runner(cls, run_id, recovery_root, timeout_seconds=timeout_seconds)

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

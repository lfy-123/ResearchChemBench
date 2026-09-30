"""Persistent benchmark-run identity and conservative controller locks."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import shutil

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.recovery_io import atomic_json, control_directory, file_hash, process_identity


class RunRecoveryError(RuntimeError):
    """The saved run cannot be resumed without risking a new benchmark run."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_config_hash(config: dict[str, Any]) -> str:
    encoded = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def run_manifest_path(workspace: Path) -> Path:
    return control_directory(workspace, Path(workspace).name) / "run.json"


def write_run_manifest(workspace: Path, record: dict[str, Any]) -> Path:
    path = run_manifest_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(path, record)
    return path


def load_run_manifest(workspace: Path) -> dict[str, Any]:
    store = ExecutionStore.open_existing(workspace, run_id=Path(workspace).name)
    if store:
        manifest = store.get_record("run", "manifest")
        if manifest:
            return manifest
    path = run_manifest_path(workspace)
    if not path.is_file():
        path = Path(workspace) / "recovery" / "run.json"
    if not path.is_file():
        raise RunRecoveryError(f"run manifest does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RunRecoveryError(f"cannot read run manifest {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RunRecoveryError(f"run manifest must be a JSON object: {path}")
    return value


def runner_store(runner):
    return ExecutionStore(runner.workspace, run_id=runner.run_id)


def cli_version(runner):
    if runner.agent.get("kind") == "mock":
        return "mock-provider-v2"
    from .wait_policy import probe_cli
    if not runner._provider_diagnostics:
        runner._provider_diagnostics = probe_cli(runner.agent["executable"])
    runner.agent["executable"] = runner._provider_diagnostics["resolved_executable"]
    return runner._provider_diagnostics["stdout"]


def freeze_task_snapshot(runner):
    store = runner_store(runner)
    snapshot = store.directory / "task_snapshot" / runner.task_type / runner.paper_id
    shutil.copytree(runner.task_dir, snapshot)
    from ..repository import TaskRepository
    # Repository construction validates the copied package manifest.
    runner.task_repository = TaskRepository([snapshot.parent.parent])
    runner.task_dir = snapshot


def freeze_runner(runner):
    freeze_task_snapshot(runner)
    store = runner_store(runner)
    runner._provider_cli_version = cli_version(runner)
    store.put_record("preflight", "provider", runner._provider_diagnostics or {"cli_version": runner._provider_cli_version})
    from .resume_policy import configure
    configure(store, runner.resume_enabled, runner.resume_policy)
    files = [*runner.public_task_files, "INSTRUCTIONS.md", "_toolbox_catalog.json"]
    store.put_record("frozen", "files", {p: file_hash(runner.workspace / p) for p in files}, immutable=True)
    store.put_record("frozen", "adapter", {
        "cli_version": runner._provider_cli_version,
        "mcp_hash": canonical_config_hash(runner._mcp_server_specs()),
        "sandbox": "workspace-write", "cwd": str(runner.workspace.resolve()),
        "executable": runner.agent.get("executable"),
        "wait_capability": runner._wait_capability,
    }, immutable=True)


def persist_runner(runner, extra):
    from .codex_history import history_metadata, session_home
    store = runner_store(runner)
    previous = store.get_record("run", "manifest", {})
    attempt = extra.pop("_attempt_record", None)
    record = {**previous, **runner._run_manifest(), **extra}
    record["schema_version"] = 2
    record["recovery_enabled"] = runner.recovery_enabled
    if runner.agent.get("kind") != "external":
        record["session_store_path"] = str(session_home(store))
        record.update(history_metadata(store))
    record["provider_cli_version"] = runner._provider_cli_version
    record["task_snapshot_root"] = str(store.directory / "task_snapshot")
    store.put_records([("run", "manifest", record)] + ([("attempt", attempt["attempt_id"], attempt)] if attempt else []))
    write_run_manifest(runner.workspace, record)
    # Read-only compatibility projection; never used as recovery authority.
    atomic_json(runner.workspace / "recovery" / "run.json", record)


def locate_workspace(root: Path, run_id: str) -> Path:
    ExecutionStore._validate_run_id(run_id)
    candidates = [root, root / run_id, root / "runs" / run_id]
    for pattern in ("*/", "cli_runs/*/", "runs/*/", "runs/cli_runs/*/"):
        candidates += list(root.glob(pattern + run_id))
    matches = {path.resolve() for path in candidates if path.name == run_id and
               (run_manifest_path(path).is_file() or (path / "recovery" / "run.json").is_file())}
    if len(matches) > 1:
        raise RunRecoveryError(f"ambiguous run {run_id!r}; provide its exact workspace: {sorted(map(str, matches))}")
    if matches:
        return next(iter(matches))
    raise RunRecoveryError(f"run {run_id!r} was not found under {root}")


def validate_session(runner):
    store = runner_store(runner)
    session_id = runner._resume_session_id
    if not session_id:
        raise RunRecoveryError("provider_session_missing; refusing to create a new conversation")
    if runner.agent.get("kind") == "mock":
        if store.get_record("mock_session", session_id): return
        raise RunRecoveryError("provider_session_missing")
    if runner.agent.get("kind") != "codex":
        raise RunRecoveryError("resume_unsupported")
    from .codex_history import session_home, session_rollout
    session_rollout(session_home(store), session_id, runner.workspace)


def _extended_deadline(manifest, control, timeout_seconds):
    """An operator may extend time, but cannot reset another exhausted budget."""
    if manifest["run_state"] in {"completed", "failed", "cancelled"}:
        raise RunRecoveryError("run_is_terminal")
    if control.get("command") == "cancel" and control.get("reason") != "deadline":
        raise RunRecoveryError("run_cancelled_or_usage_budget_exhausted")
    if type(timeout_seconds) is not int or timeout_seconds <= manifest["config"]["timeout_seconds"]:
        raise RunRecoveryError("timeout_extension_must_increase_total_budget")
    now = datetime.now(timezone.utc)
    if manifest["run_state"] == "budget_exhausted" and datetime.fromisoformat(manifest["deadline_at"]) > now:
        raise RunRecoveryError("only_expired_wall_budget_can_be_reopened")
    deadline = datetime.fromisoformat(manifest["first_started_at"]) + timedelta(seconds=timeout_seconds)
    if deadline <= now:
        raise RunRecoveryError("extended_run_deadline_expired")
    return deadline.isoformat()


def _extend_wall_budget(runner, store, manifest, timeout_seconds):
    """Update all deadline authorities together, with the job manager stopped."""
    import uuid
    from chemistry_toolbox.src.execution_states import TERMINAL_STATES
    from chemistry_toolbox.src.recovery_io import file_lock
    try:
        # Exclude both a running manager and a concurrent manager launch. Otherwise
        # a tick that read the old deadline could cancel the newly restored Agent.
        with file_lock(store.directory / "manager_start.lock", blocking=False), file_lock(store.directory / "manager.lock", blocking=False):
            current = store.get_record("run", "manifest")
            if current != manifest:
                raise RunRecoveryError("run_changed_during_budget_extension; retry resume")
            control = store.get_record("control", "current", {})
            deadline = _extended_deadline(current, control, timeout_seconds)
            if any(job["state"] not in TERMINAL_STATES for job in store.list_jobs()):
                raise RunRecoveryError("budget_extension_requires_no_active_or_uncertain_jobs")
            totals = store.usage()
            if totals["turns"] >= runner.max_turns or (runner.max_tokens and totals["input_tokens"] + totals["output_tokens"] >= runner.max_tokens):
                raise RunRecoveryError("run_usage_budget_exhausted")
            runner.timeout_seconds = timeout_seconds
            runner.deadline_at = deadline
            if runner.model_wait_strategy == "host_event_wait":
                runner.mcp_tool_timeout_ms = max(runner.mcp_tool_timeout_ms, (timeout_seconds + 60) * 1000)
            runner._frozen_config = {**current["config"], "timeout_seconds": timeout_seconds,
                                     "mcp_tool_timeout_ms": runner.mcp_tool_timeout_ms}
            adapter = store.get_record("frozen", "adapter")
            updated_adapter = {**adapter, "mcp_hash": canonical_config_hash(runner._mcp_server_specs())}
            updated = {**current, **runner._run_manifest(), "schema_version": 2, "run_state": "recovering", "termination": None, "error": None}
            manager = store.get_record("manager", "config", {})
            manager = {**manager, "environment": {**manager.get("environment", {}), "RESEARCHCHEMBENCH_RUN_DEADLINE": deadline}}
            audit = {"at": _now(), "source": "operator_resume", "previous_state": current["run_state"],
                     "previous_control": control, "old_timeout_seconds": current["config"]["timeout_seconds"],
                     "timeout_seconds": timeout_seconds, "old_deadline_at": current["deadline_at"], "deadline_at": deadline,
                     "old_config_hash": current["config_hash"], "config_hash": updated["config_hash"],
                     "old_mcp_hash": adapter["mcp_hash"], "mcp_hash": updated_adapter["mcp_hash"]}
            store.put_records([("run", "manifest", updated), ("frozen", "adapter", updated_adapter),
                               ("manager", "config", manager), ("budget_extension", uuid.uuid4().hex, audit),
                               ("control", "current", {"command": "resume", "at": _now(), "source": "operator_budget_extension"})])
    except BlockingIOError as exc:
        raise RunRecoveryError("budget_extension_requires_idle_manager; retry after it stops") from exc


def restore_runner(cls, run_id, recovery_root, *, timeout_seconds=None):
    from ..settings import WORKSPACES_DIR
    workspace = locate_workspace(Path(recovery_root or WORKSPACES_DIR).resolve(), run_id)
    lock = ControllerLock(control_directory(workspace, run_id) / "controller.lock")
    lock.acquire()
    try:
        store = ExecutionStore(workspace, run_id=run_id)
        manifest = store.get_record("run", "manifest")
        if not manifest or manifest.get("schema_version") != 2 or not manifest.get("recovery_enabled"):
            raise RunRecoveryError("legacy_run_not_resumable")
        control = store.get_record("control", "current", {})
        if timeout_seconds is not None:
            _extended_deadline(manifest, control, timeout_seconds)
        elif manifest["run_state"] in {"completed", "failed", "cancelled", "budget_exhausted"}:
            raise RunRecoveryError("run_is_terminal")
        if timeout_seconds is None and control.get("command") == "cancel":
            raise RunRecoveryError("run_cancelled")
        if manifest.get("agent_kind") not in {"codex", "mock"}:
            raise RunRecoveryError("resume_unsupported")
        agent = store.get_record("agent", "identity", {})
        identity = process_identity(agent.get("pid"), agent)
        if agent.get("pid") and identity.get("host") != agent.get("host"):
            raise RunRecoveryError("original_agent_host_unverified")
        if identity.get("verified"):
            raise RunRecoveryError("original_agent_still_running; pause before resuming")
        config = manifest["config"]
        if canonical_config_hash(config) != manifest["config_hash"]:
            raise RunRecoveryError("configuration_hash_mismatch")
        for variable, name in (("RCB_CODEX_MODEL", "codex_model"), ("RCB_CODEX_REASONING_EFFORT", "codex_reasoning_effort"), ("RCB_CODEX_BASE_URL", "codex_base_url")):
            if manifest.get("agent_kind") != "codex": break
            current_value = os.environ.get(variable)
            if name == "codex_base_url" and current_value:
                from urllib.parse import urlsplit
                if not urlsplit(current_value).path: current_value = current_value.rstrip("/") + "/v1"
            if current_value and current_value != config[name]:
                raise RunRecoveryError("provider_configuration_drift: " + variable)
        runner = cls(**config, workspace_root=workspace.parent, task_roots=[manifest["task_snapshot_root"]], _saved_identity=manifest)
        runner.first_started_at = manifest["first_started_at"]
        runner.deadline_at = manifest["deadline_at"]
        runner._provider_cli_version = cli_version(runner)
        if timeout_seconds is None:
            runner.remaining_run_timeout_seconds()
        verify_frozen_runner(runner, store=store, manifest=manifest, refresh_probe=False)
        runner._resume_session_id = manifest.get("provider_session_id")
        runner.attempt_id = manifest.get("attempt_id", "attempt_0001")
        validate_session(runner)
        reconcile_usage(runner)
        if timeout_seconds is not None:
            _extend_wall_budget(runner, store, manifest, timeout_seconds)
        for attempt_id, attempt in store.records("attempt").items():
            if not attempt.get("end_at"):
                store.put_record("attempt", attempt_id, {**attempt, "end_reason": "controller_interrupted", "reconciled_at": _now(), "interrupted": True})
        runner._restored = True
        runner._controller_lock = lock
        runner._recovery_notice = "Resume this original session and run. Query saved submissions and jobs before further work. Infrastructure interruption does not authorize resubmission."
        store.put_record("controller", "identity", process_identity(os.getpid()))
        if store.get_record("control", "current", {}).get("command") == "cancel":
            raise RunRecoveryError("run_cancelled")
        store.put_record("control", "current", {"command": "resume", "at": _now(), "source": "operator_resume"})
        runner._persist_run_manifest(run_state="recovering")
        return runner
    except BaseException as exc:
        try:
            if "store" in locals():
                import uuid
                store.put_record("recovery_error", uuid.uuid4().hex, {"at": _now(), "reason": str(exc)})
        finally:
            lock.release()
        raise


class ControllerLock:
    """Advisory single-controller lock for one run on the local host."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._handle = None

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = self.path.open("a+", encoding="utf-8")
        try:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (ImportError, BlockingIOError, OSError) as exc:
            handle.close()
            raise RunRecoveryError(f"another controller owns {self.path}") from exc
        handle.seek(0)
        handle.truncate()
        handle.write(json.dumps({"pid": os.getpid(), "acquired_at": _now()}) + "\n")
        handle.flush()
        self._handle = handle

    def release(self) -> None:
        if self._handle is None:
            return
        try:
            import fcntl

            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        finally:
            self._handle.close()
            self._handle = None

    def __enter__(self) -> "ControllerLock":
        self.acquire()
        return self

    def __exit__(self, _type, _value, _traceback) -> None:
        self.release()


__all__ = [
    "ControllerLock",
    "RunRecoveryError",
    "canonical_config_hash",
    "load_run_manifest",
    "run_manifest_path",
    "write_run_manifest",
]


def reconcile_usage(runner):
    """Use the same incremental ingestion on recovery and ordinary execution."""
    from .usage_accounting import refresh_usage
    return refresh_usage(runner, force=True)


def verify_frozen_runner(runner, *, store=None, manifest=None, refresh_probe=True):
    store = store or runner_store(runner)
    manifest = manifest or store.get_record("run", "manifest", {})
    frozen = store.get_record("frozen", "adapter")
    if refresh_probe and runner.agent.get("kind") != "mock":
        from .wait_policy import probe_cli
        runner._provider_diagnostics = probe_cli(runner.agent["executable"])
        runner._provider_cli_version = cli_version(runner)
    if frozen.get("wait_capability") != runner._wait_capability:
        raise RunRecoveryError("provider_wait_capability_drift")
    actual = {"cli_version": runner._provider_cli_version,
              "mcp_hash": canonical_config_hash(runner._mcp_server_specs()),
              "executable": runner.agent.get("executable")}
    expected = {"cli_version": frozen["cli_version"], "mcp_hash": frozen["mcp_hash"],
                "executable": shutil.which(frozen["executable"]) if frozen["executable"] else None}
    differences = {key: {"saved": expected[key], "current": value} for key, value in actual.items() if value != expected[key]}
    if differences:
        raise RunRecoveryError("provider_or_mcp_configuration_drift: " + json.dumps(differences, ensure_ascii=False))
    if runner.task_package.package_content_sha256 != manifest["task_package_content_sha256"]:
        raise RunRecoveryError("task_snapshot_hash_mismatch")
    workspace = runner.workspace
    for name, expected in store.get_record("frozen", "files").items():
        if not (workspace / name).is_file() or file_hash(workspace / name) != expected:
            raise RunRecoveryError("frozen_input_modified: " + name)

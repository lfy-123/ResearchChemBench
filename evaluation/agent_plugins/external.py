"""Launch an external system without importing its dependencies into the runner."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from .registry import AgentConfigError, evaluator_environment, sensitive_name

BASE_ENVIRONMENT = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TZ", "SYSTEMROOT", "LD_LIBRARY_PATH", "SSL_CERT_FILE", "SSL_CERT_DIR")


def preflight_external(runner) -> None:
    if runner.recovery_enabled or runner.resume_enabled:
        raise AgentConfigError("external_resume_unsupported: external agents do not use the Codex recovery lifecycle")
    if runner.execution_mode != "local":
        raise AgentConfigError("external_execution_mode_unsupported: only local is currently validated")
    if runner.model_wait_strategy != "provider_default":
        raise AgentConfigError("external_wait_strategy_unsupported")
    command = runner.agent["command"]
    executable = shutil.which(command[0])
    if not executable:
        raise AgentConfigError(f"External executable not found or not executable: {command[0]}")
    # Keep venv symlinks intact: resolving them can select a different Python environment.
    command[0] = os.path.abspath(executable)
    missing = [name for name in runner.agent["env_allowlist"] if name not in os.environ]
    if missing:
        raise AgentConfigError(f"Required external environment variables are unset: {missing}")


def build_external_argv(definition, request_path: Path) -> list[str]:
    return [*definition["command"], "--request", str(request_path.absolute())]


def build_external_environment(runner, definition) -> dict[str, str]:
    env = {name: os.environ[name] for name in BASE_ENVIRONMENT if name in os.environ}
    env.setdefault("PATH", os.defpath)
    env.update({name: os.environ[name] for name in definition["env_allowlist"] if name in os.environ})
    home = runner.workspace / "_agent_protocol" / "home"
    home.mkdir(parents=True, exist_ok=True)
    env.update(HOME=str(home), XDG_CONFIG_HOME=str(home / ".config"),
               XDG_CACHE_HOME=str(home / ".cache"), XDG_DATA_HOME=str(home / ".local/share"),
               PYTHONUNBUFFERED="1", GIT_CEILING_DIRECTORIES=str(runner.workspace.parent),
               RCB_AGENT_REQUEST=str(runner.workspace / "_agent_protocol/request.json"))
    # Tool credentials are transported in the environment, never embedded in JSON.
    for spec in runner._mcp_server_specs():
        for name, value in spec.get("environment", {}).items():
            if sensitive_name(name) and not evaluator_environment(name):
                env[name] = str(value)
    return env


def finalize_external_jobs(runner, *, reason, grace_seconds=7.0):
    """Close submission admission and drain evaluator-owned work before archival."""
    import time
    from chemistry_toolbox.mcp.job_manager import JobManager
    from chemistry_toolbox.src.execution_states import ACTIVE_STATES, TERMINAL_STATES

    manager = JobManager(runner.workspace, run_id=runner.run_id)
    initial = manager.reconcile()
    control = manager.store.get_record("control", "current", {})
    if control.get("command") != "cancel":
        manager.store.put_record("control", "current", {"command": "finalize", "reason": reason})
    # Retain evidence of active work even if the daemon cancels it immediately
    # after admission closes. A quick cancellation must not turn an early exit
    # into a valid completion.
    after_close = manager.reconcile()
    seen = {item["entity_id"] for item in initial["results"]}
    initial["results"].extend(item for item in after_close["results"] if item["entity_id"] not in seen)
    states = [item["state"] for item in initial["results"]]
    initial["summary"] = {"total": len(states), "active": sum(s in ACTIVE_STATES for s in states),
                          "terminal": sum(s in TERMINAL_STATES for s in states),
                          "needs_reconciliation": states.count("needs_reconciliation")}
    errors = []
    for row in manager.store.list_jobs():
        if row["state"] not in TERMINAL_STATES:
            try:
                manager.cancel_entity(row["entity_id"], row["entity_type"],
                                      reason="deadline" if reason == "timeout" else "cancel")
            except Exception as exc:
                errors.append(f"{row['entity_id']}: {type(exc).__name__}: {exc}")
    deadline = time.monotonic() + grace_seconds
    final = manager.reconcile()
    while (final["summary"]["active"] or final["summary"]["needs_reconciliation"]) and time.monotonic() < deadline:
        time.sleep(0.1)
        final = manager.reconcile()
    return {"reason": reason, "initial_reconciliation": initial,
            "final_reconciliation": final, "errors": errors}

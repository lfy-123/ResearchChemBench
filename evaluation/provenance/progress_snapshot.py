"""Read-only progress shared by CLI, Web and the controller's cached snapshot."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import time

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.recovery_io import atomic_json, control_directory
from .evidence_archive import audit_directory, read_json
from .results import read_scoring_status


class JsonlCursor:
    """Byte cursor: incomplete final records are retried, rotation is detected."""
    def __init__(self):
        self.offset = 0
        self.identity = None
        self.pending = b""
        self.generation = 0
        self.skipped_records = 0
        self.skipping = False

    def read(self, path, max_bytes=1024 * 1024):
        path = Path(path)
        if not path.is_file(): return []
        stat = path.stat()
        identity = (stat.st_dev, stat.st_ino)
        if identity != self.identity or stat.st_size < self.offset:
            self.offset = 0
            self.pending = b""
            self.generation += 1
            self.skipped_records = 0
            self.skipping = False
        self.identity = identity
        result = []
        with path.open("rb") as stream:
            stream.seek(self.offset)
            data = stream.read(max_bytes)
            self.offset = stream.tell()
            parts = data.split(b"\n")
            for position, chunk in enumerate(parts):
                complete = position < len(parts) - 1
                if not self.skipping:
                    self.pending += chunk
                    if len(self.pending) > 16 * 1024 * 1024:
                        self.pending = b""
                        self.skipping = True
                        self.skipped_records += 1
                if complete:
                    if not self.skipping:
                        result.append(self.pending.decode(errors="replace").rstrip("\r"))
                    self.pending = b""
                    self.skipping = False
        return result


_TRACE_CACHE = {}


def _tool_counts(workspace):
    path = workspace / "_tool_call_events.jsonl"
    key = str(path)
    cursor, events, identity = _TRACE_CACHE.get(key, (JsonlCursor(), {}, None))
    lines = cursor.read(path)
    if identity != cursor.generation: events = {}
    for line in lines:
        try: event = json.loads(line)
        except ValueError: continue
        if event.get("sequence") is not None: events[event["sequence"]] = event
    _TRACE_CACHE[key] = (cursor, events, cursor.generation)
    if len(_TRACE_CACHE) > 128:
        _TRACE_CACHE.pop(next(iter(_TRACE_CACHE)))
    return {"tool_call_count": len(events) if path.exists() and not cursor.skipped_records else None,
            "active_tools": [{k: e.get(k) for k in ("sequence", "tool", "at")} for e in events.values() if e.get("phase") == "started"],
            "recent_tool_event": max((e.get("at", "") for e in events.values()), default=None),
            "tool_trace_skipped_records": cursor.skipped_records,
            "tool_trace_backlog_bytes": max(0, path.stat().st_size - cursor.offset) if path.exists() else 0}


def build_progress_snapshot(workspace, *, controller_observed=False):
    workspace = Path(workspace).resolve()
    meta = read_json(workspace / "_meta.json")
    run_id = meta.get("run_id", workspace.name)
    control = control_directory(workspace, run_id)
    jobs, usage, manifest, errors = [], meta.get("usage_details", {}), {}, []
    controller, policy, retry, attempts = {}, {}, {}, {}
    history = {k: meta.get(k) for k in ("recovery_mode", "history_recovery", "history_recovery_error")}
    if (control / "execution.sqlite3").is_file() or (workspace.parent / "control/execution.sqlite3").is_file():
        try:
            store = ExecutionStore.open_existing(workspace)
            jobs = store.list_jobs()
            usage = store.usage_details()
            manifest = store.get_record("run", "manifest", {})
            controller = store.get_record("controller", "identity", {})
            policy = store.get_record("resume", "policy", {})
            retry = store.get_record("resume", "state", {})
            attempts = store.records("attempt")
            from ..execution.codex_history import history_metadata
            history = history_metadata(store)
        except Exception as exc:
            errors.append(str(exc))
    if usage.get("accounting_status") == "unavailable":
        usage = {**usage, **{key: None for key in ("input_tokens", "output_tokens", "total_tokens", "input_total_tokens", "agent_completed_turns")}}
    counts = Counter(j["state"] for j in jobs if j["entity_type"] == "job")
    tools = _tool_counts(workspace)
    state = manifest.get("run_state") or meta.get("status", "unknown")
    from chemistry_toolbox.src.recovery_io import process_identity
    controller_state = process_identity(controller.get("pid"), controller)
    controller_alive = controller_state.get("verified", False)
    scoring = read_scoring_status(workspace)
    active = state in {"running", "recovering", "ready"}
    phase = "waiting_for_compute" if active and any(e.get("tool") in {"wait_execution_jobs", "wait_execution_events"} for e in tools["active_tools"]) else state
    if controller_alive and retry.get("next_retry_at"):
        phase = "judge_waiting_for_provider" if retry.get("stage") == "judge" else "waiting_for_provider"
    cached = read_json(audit_directory(workspace) / "progress.json")
    heartbeat = datetime.now(timezone.utc).isoformat() if controller_observed else cached.get("controller_observed_at")
    heartbeat_age = None
    if heartbeat:
        try: heartbeat_age = max(0, time.time() - datetime.fromisoformat(heartbeat).timestamp())
        except ValueError: errors.append("invalid_controller_heartbeat")
    stale_reasons = ["read_error"] if errors else []
    if active and heartbeat_age is not None and heartbeat_age > 60:
        stale_reasons.append("controller_heartbeat_old")
    if tools["tool_trace_backlog_bytes"]: stale_reasons.append("tool_trace_backlog")
    if tools["tool_trace_skipped_records"]: stale_reasons.append("oversized_tool_event")
    result = {"schema_version": 2, "run_id": run_id, "observed_at": datetime.now(timezone.utc).isoformat(),
              "run_status": state, "phase": phase, "stale": bool(stale_reasons), "stale_reasons": stale_reasons,
              "controller_observed_at": heartbeat, "controller_heartbeat_age_seconds": heartbeat_age,
              "errors": errors, "usage": usage, "controller_alive": controller_alive,
              "controller_identity": controller, "resume_policy": policy, "retry": retry,
              "error": scoring.get("provider_error") if state == "completed" else manifest.get("error", meta.get("error")), "last_failure": manifest.get("last_failure"),
              "attempt_count": len(attempts), **history,
              "manual_resume_count": sum(a.get("start_reason") in {"resume", "manual_resume"} for a in attempts.values()),
              "automatic_resume_count": retry.get("automatic_attempts", 0),
              "budget": {"max_tokens": manifest.get("config", {}).get("max_tokens"),
                         "max_completed_provider_turns": manifest.get("config", {}).get("max_turns")},
              "jobs": {"total": sum(counts.values()), "by_state": dict(counts)}, **tools,
              "tool_round_count": usage.get("tool_round_count"), "agent_completed_turns": usage.get("agent_completed_turns"),
              "model_request_count": usage.get("model_request_count"), "report_exists": (workspace / "report/report.md").is_file(),
              "score_exists": (workspace / "_score.json").is_file(), "completion_percentage": None,
              "archive": meta.get("archive"), "judge_usage": scoring["judge_usage"], "scoring": scoring}
    deadline = manifest.get("deadline_at") or meta.get("deadline_at")
    started = manifest.get("first_started_at") or meta.get("first_started_at")
    clock_time = time.time()
    finalized = state in {"completed", "failed", "cancelled", "timeout", "budget_exhausted", "stopped"}
    elapsed = manifest.get("run_elapsed_seconds", meta.get("run_elapsed_seconds"))
    if elapsed is None and not meta.get("recovery_enabled"):
        elapsed = meta.get("duration_seconds")
    if finalized and started and elapsed is not None:
        clock_time = datetime.fromisoformat(started).timestamp() + float(elapsed)
    result["time_basis"] = "finalization" if finalized else "current_wall_clock"
    if deadline:
        result["remaining_seconds"] = max(0, int(datetime.fromisoformat(deadline).timestamp() - clock_time)) if not finalized or elapsed is not None else None
    if started:
        result["elapsed_seconds"] = max(0, int(clock_time - datetime.fromisoformat(started).timestamp())) if not finalized or elapsed is not None else None
    durations = [max(0, (a.get("end_at") or time.time()) - a["process_started_at"])
                 for a in attempts.values() if a.get("process_started_at") and not a.get("interrupted")]
    complete_times = len(durations) == len(attempts)
    result["agent_process_seconds"] = round(sum(durations), 3) if complete_times else None
    result["agent_paused_seconds"] = max(0, result.get("elapsed_seconds", 0) - sum(durations)) if complete_times and result.get("elapsed_seconds") is not None else None
    return result


def write_progress_snapshot(runner, *, force=False):
    now = time.monotonic()
    if not force and now - getattr(runner, "_last_progress_snapshot", -100) < runner.progress_interval:
        return
    runner._last_progress_snapshot = now
    try:
        value = build_progress_snapshot(runner.workspace, controller_observed=True)
        atomic_json(audit_directory(runner.workspace) / "progress.json", value)
        runner._progress_snapshot_error = None
        return value
    except (OSError, ValueError) as exc:
        # Monitoring must not interrupt an otherwise healthy scientific run.
        runner._progress_snapshot_error = str(exc)


def format_progress_summary(value):
    def count(number): return "unknown" if number is None else f"{number:,}"
    usage = value.get("usage") or {}
    return "\n".join([
        f"Run: {value['run_id']} | {value['run_status']} | phase={value['phase']} | stale={value['stale']}",
        "Tokens: input=" + count(usage.get("input_total_tokens", usage.get("input_tokens")))
            + " cached(subset)=" + count(usage.get("cached_input_tokens")) + " output=" + count(usage.get("output_tokens")),
        "Activity: requests=" + count(value.get("model_request_count")) + " completed_turns=" + count(value.get("agent_completed_turns"))
            + " tools=" + count(value.get("tool_call_count")) + " tool_rounds=" + count(value.get("tool_round_count")),
        f"Jobs: {value['jobs']['total']} {json.dumps(value['jobs']['by_state'], ensure_ascii=False)} | report={value['report_exists']} score={value['score_exists']}",
        f"Evaluation: {value.get('scoring', {}).get('evaluation_status', 'unknown')} | latest={value.get('scoring', {}).get('latest_attempt')} | published={value.get('scoring', {}).get('published_score')}",
        f"Controller: alive={value.get('controller_alive')} | auto_resume={value.get('resume_policy', {}).get('enabled', False)} | retries={value.get('retry', {}).get('automatic_attempts', 0)} | next_retry_at={value.get('retry', {}).get('next_retry_at') if value.get('controller_alive') else 'controller_stopped'} | retry_stop={value.get('retry', {}).get('stop_reason')}",
        f"History recovery: mode={value.get('recovery_mode') or 'native'} | error={json.dumps(value.get('history_recovery_error'), ensure_ascii=False)}",
        f"Attempts: total={value.get('attempt_count')} manual_resume={value.get('manual_resume_count')} automatic_resume={value.get('automatic_resume_count')} | agent_process={count(value.get('agent_process_seconds'))}s paused={count(value.get('agent_paused_seconds'))}s | token_budget={value.get('budget', {}).get('max_tokens') or 'unlimited'}",
        f"Error: {json.dumps(value.get('error'), ensure_ascii=False)}",
        f"Time ({value.get('time_basis', 'unknown')}): elapsed={count(value.get('elapsed_seconds'))}s remaining={count(value.get('remaining_seconds'))}s",
    ])


def batch_is_active(directory):
    """A results projection alone never proves that supervision has ended."""
    directory = Path(directory)
    planned = read_json(directory / "planned_runs.json").get("runs", [])
    rows = read_json(directory / "eval_report.json").get("runs", [])
    workspaces = [path.parent for path in directory.glob("*/_meta.json")]
    for workspace in workspaces:
        snapshot = build_progress_snapshot(workspace)
        if snapshot["controller_alive"]:
            return True
        if snapshot["run_status"] in {"running", "recovering", "ready"}:
            return True
        if snapshot["scoring"]["evaluation_status"] in {"preparing", "judging", "interpreting"}:
            return True
    return len(rows) < len(planned) or not (rows or workspaces)

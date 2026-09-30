"""RunController for persistent jobs and exact provider-session recovery."""
from __future__ import annotations

import json
import os
import queue
import sqlite3
import subprocess
import threading
import time
from datetime import datetime, timezone

from chemistry_toolbox.mcp.job_manager import JobManager, ensure_manager
from chemistry_toolbox.src.recovery_io import process_identity
from .recovery import ControllerLock, RunRecoveryError, runner_store, validate_session
from .progress import LiveProgressReporter
from ..provenance.results import write_workspace_results
from ..provenance.execution_audit import execution_submission_audit
from .usage_accounting import refresh_usage, record_turn
from .provider_errors import ProviderFailure, is_encrypted_history_error, normalize_error
from .codex_history import activate_plaintext_fallback, history_metadata, session_home
from .resume_policy import configure, retry_delay


def record_usage(runner, event):
    if event.get("type") != "turn.completed": return
    runner._turn_sequence += 1
    event_id = event.get("turn_id") or event.get("id") or (runner.attempt_id + ":" + str(runner._turn_sequence))
    record_turn(runner_store(runner), runner._resume_session_id, event_id, event)


from .output_contract import validate_submission


def _run_attempt(runner):
    store = runner_store(runner)
    reporter = None
    attempt = None
    started = time.time()
    exit_code, termination, error = -1, "infrastructure_exit", None
    failures = ProviderFailure()
    try:
        current = store.get_record("run", "manifest", {})
        if current.get("run_state") in {"completed", "failed", "cancelled", "budget_exhausted"}:
            raise RunRecoveryError("run_is_terminal")
        runner.remaining_run_timeout_seconds()
        control = store.get_record("control", "current", {})
        if control.get("command") == "cancel":
            termination = "budget_exhausted" if control.get("reason") in {"deadline", "usage_budget"} else "cancelled"
            raise RunRecoveryError("run_cancelled")
        if control.get("command") == "pause":
            termination = "pause"
            raise RunRecoveryError("run_paused")
        if runner._stop_requested:
            termination = "cancelled"
            raise RunRecoveryError("run_cancelled")
        if runner._restored:
            from .recovery import verify_frozen_runner
            verify_frozen_runner(runner, refresh_probe=runner._attempt_start_reason in {"automatic_resume", "plaintext_history_resume"})
            validate_session(runner)
        store.put_record("manager", "config", {"environment": {
            **runner._mcp_environment(),
            "RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT": os.environ.get("RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT", str(store.directory.parent / ("host_" + __import__('socket').gethostname())))
        }}, immutable=True)
        manager = JobManager(runner.workspace, run_id=runner.run_id)
        reconciliation = manager.reconcile()
        if reconciliation["summary"]["needs_reconciliation"]:
            raise RunRecoveryError("job_identity_requires_reconciliation")
        refresh_usage(runner, force=True)
        totals = store.usage()
        if totals["turns"] >= runner.max_turns or (runner.max_tokens and totals["input_tokens"] + totals["output_tokens"] >= runner.max_tokens):
            raise RunRecoveryError("run_usage_budget_exhausted")
        if runner._restored:
            runner._recovery_notice = (
                "Resume this original session and run. Query saved submissions and jobs before further work. "
                "Infrastructure interruption does not authorize resubmission.\nConfirmed job summary: "
                + json.dumps(reconciliation["summary"])
                + "\nCurrent run deadline (UTC): " + runner.deadline_at)
            if store.get_record("history_recovery", "active"):
                runner._recovery_notice += (
                    "\nCompatibility recovery: the provider rejected the historical encrypted reasoning. "
                    "That internal reasoning was removed from a separate copy of this same session. "
                    "Readable messages, tool calls/results, files and saved jobs are retained; the original history is backed up. "
                    "Recheck relevant evidence as needed and query existing jobs before submitting anything.")
        ensure_manager(store)
        runner.attempt_id = f"attempt_{len(store.records('attempt')) + 1:04d}"
        attempt_directory = store.directory / "attempts" / runner.attempt_id
        runner.final_message_path = attempt_directory / "final_message.txt"
        attempt = {"attempt_id": runner.attempt_id, "start_at": started, "start_reason": runner._attempt_start_reason,
                   "recovery_source_attempt": current.get("attempt_id") if runner._restored else None,
                   "provider_session_id": runner._resume_session_id, "log_path": str(attempt_directory / "agent.jsonl"),
                   "raw_event_offset": runner.output_path.stat().st_size if runner.output_path.exists() else 0,
                   "cwd": str(runner.workspace), "provider_cli_version": runner._provider_cli_version, "startup_status": "prepared",
                   "session_store_path": str(session_home(store)), **history_metadata(store),
                   "failure_source": current.get("error") or current.get("last_failure")}
        runner._persist_run_manifest(run_state="running", phase="agent_running", error=None, provider_diagnostics=runner._provider_diagnostics, _attempt_record=attempt)
        attempt_directory.mkdir(parents=True, exist_ok=False)
        argv = runner.build_agent_argv()
        runner._write_meta("running", {"recovery_enabled": True, "agent_command": runner.command_preview()})
        reporter = LiveProgressReporter(runner.workspace, runner.run_id, enabled=runner.live_progress, console=runner.progress_console, max_chars=runner.progress_max_chars)
        reporter.emit("ATTEMPT_START", attempt_id=runner.attempt_id, resumed=runner._restored)
        runner.process = subprocess.Popen(argv, cwd=runner.workspace, env=runner._agent_environment(), stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1, start_new_session=True)
        attempt.update(startup_status="started", process_started_at=time.time(), pid=runner.process.pid)
        store.put_record("attempt", runner.attempt_id, attempt)
        runner.process_group_id = runner.process.pid
        store.put_record("agent", "identity", {**process_identity(runner.process.pid), "agent_token": runner._mcp_environment()["RCB_AGENT_RUN_TOKEN"]})
        lines = queue.Queue()
        def reader():
            try:
                for line in runner.process.stdout: lines.put(line)
            finally: lines.put(None)
        thread = threading.Thread(target=reader, daemon=True)
        thread.start()
        final_event, drain_deadline = False, None
        with runner.output_path.open("a") as combined, (attempt_directory / "agent.jsonl").open("a") as output:
            while True:
                control = store.get_record("control", "current", {})
                refresh_usage(runner)
                from ..provenance.progress_snapshot import write_progress_snapshot
                write_progress_snapshot(runner)
                totals = store.usage()
                expired = time.time() >= datetime.fromisoformat(runner.deadline_at).timestamp()
                budget_used = totals["turns"] >= runner.max_turns or (runner.max_tokens and totals["input_tokens"] + totals["output_tokens"] >= runner.max_tokens)
                if expired or budget_used or runner._stop_requested or control.get("command") in {"pause", "cancel"}:
                    termination = "budget_exhausted" if expired or budget_used else "pause" if control.get("command") == "pause" else "cancelled"
                    runner._terminate_process_tree()
                    break
                try: line = lines.get(timeout=0.2)
                except queue.Empty:
                    if runner.process.poll() is not None:
                        if drain_deadline is None: drain_deadline = time.time() + 1
                        if time.time() > drain_deadline:
                            runner._terminate_process_tree()
                            break
                    continue
                if line is None: break
                combined.write(line); combined.flush()
                output.write(line); output.flush()
                event = runner.capture_provider_event(line)
                failures.observe(event, {"path": str(attempt_directory / "agent.jsonl"), "offset": output.tell() - len(line.encode("utf-8"))})
                record_usage(runner, event)
                final_event = final_event or event.get("type") == "turn.completed"
                reporter.handle_agent_line(line)
            os.fsync(output.fileno()); os.fsync(combined.fileno())
        try: exit_code = runner.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            runner._terminate_process_tree(force=True)
            exit_code = runner.process.wait(timeout=5)
        control = store.get_record("control", "current", {})
        if termination == "infrastructure_exit" and control.get("command") in {"pause", "cancel"}:
            termination = "pause" if control["command"] == "pause" else "budget_exhausted" if control.get("reason") in {"deadline", "usage_budget"} else "cancelled"
        if termination == "infrastructure_exit" and exit_code == 0 and final_event and not failures.final:
            termination = "agent_completed"
        if termination == "infrastructure_exit":
            error = failures.failure(exit_code)
            error["event_ref"] = error.get("event_ref") or {"path": str(attempt_directory / "agent.jsonl")}
    except Exception as exc:
        error = None if termination in {"pause", "cancelled"} else normalize_error(exc, source="controller")
        runner._terminate_process_tree()
        if runner.process and runner.process.poll() is None:
            try: runner.process.wait(timeout=5)
            except subprocess.TimeoutExpired: runner._terminate_process_tree(force=True)
        if isinstance(exc, RunRecoveryError) and termination not in {"pause", "cancelled", "budget_exhausted"}:
            termination = "budget_exhausted" if "expired" in str(exc) or "budget_exhausted" in str(exc) else "recovery_blocked"
    finally:
        try:
            refresh_usage(runner, force=True)
            status = {"infrastructure_exit": "suspended_infrastructure", "pause": "suspended_infrastructure", "cancelled": "cancelled",
                      "budget_exhausted": "budget_exhausted", "recovery_blocked": "recovery_blocked"}.get(termination, "finalizing")
            manager = JobManager(runner.workspace, run_id=runner.run_id)
            if termination in {"agent_completed", "cancelled", "budget_exhausted"}:
                store.put_record("control", "current", {"command": "finalize" if termination == "agent_completed" else "cancel", "reason": termination})
                ensure_manager(store)
                for job in store.list_jobs():
                    manager.cancel_entity(job["entity_id"], job["entity_type"], reason="deadline" if termination == "budget_exhausted" else "cancel")
                finish_deadline = time.time() + 8
                while time.time() < finish_deadline:
                    facts = manager.reconcile()
                    if not facts["summary"]["active"]: break
                    time.sleep(0.2)
            facts = manager.reconcile()
            submission_validation = validate_submission(runner) if termination == "agent_completed" else None
            deliverables = submission_validation["checked_files"] if submission_validation else []
            report_exists = any(v["file"] == "report/report.md" and v["satisfied"] for v in deliverables)
            submission_findings = submission_validation["errors"] if submission_validation else []
            if termination == "agent_completed":
                if facts["summary"]["needs_reconciliation"] or facts["summary"]["active"]:
                    status = "recovery_blocked"
                else:
                    status = "completed" if submission_validation["valid"] else "failed"
            if attempt:
                if attempt["startup_status"] == "prepared":
                    attempt["startup_status"] = "launch_failed"
                attempt.update(end_at=time.time(), end_reason=termination, provider_session_id=runner._resume_session_id,
                               exit_code=exit_code, usage_total=store.usage(), error=error)
                store.put_record("attempt", runner.attempt_id, attempt)
            from ..provenance.trace import load_tool_trace, process_metrics
            from ..provenance.model_io import export_model_io_trace
            metrics = process_metrics(load_tool_trace(runner.workspace), workspace=runner.workspace)
            try:
                model_io = export_model_io_trace(runner.workspace)
            except Exception as exc:
                model_io = {"error": str(exc)}
            metadata = {**metrics, "model_io_trace": model_io, "termination": termination, "exit_code": exit_code, "error": error, "recovery_enabled": True,
                        "execution_submission_audit": execution_submission_audit(runner.workspace, store),
                        "report_exists": report_exists, "required_deliverable_status": deliverables, "submission_findings": submission_findings, "submission_validation": submission_validation, "execution_reconciliation": facts,
                        "usage": store.usage(), "usage_details": store.usage_details(), "attempts": list(store.records("attempt").values()),
                        "recovery_count": max(0, len(store.records("attempt")) - 1),
                        "duration_seconds": round(time.time() - started, 3), "run_elapsed_seconds": round(time.time() - datetime.fromisoformat(runner.first_started_at).timestamp(), 3)}
            last = error or store.get_record("run", "manifest", {}).get("last_failure")
            if last and termination == "agent_completed":
                last = {**last, "resolved_at": datetime.now(timezone.utc).isoformat()}
            metadata["last_failure"] = last
            runner._persist_run_manifest(run_state=status, phase=status, **metadata)
            runner._write_meta(status, metadata)
            write_workspace_results(runner.workspace)
            runner._finalize_evidence(status, metadata)
            if reporter: reporter.emit("ATTEMPT_END", status=status, termination=termination)
        finally:
            if reporter: reporter.close()
    return json.loads(runner.meta_path.read_text())


def _cooldown(runner, state):
    """Host-only wait: persist progress and honor controls without model requests."""
    from ..provenance.progress_snapshot import write_progress_snapshot
    store = runner_store(runner)
    deadline = datetime.fromisoformat(runner.deadline_at).timestamp()
    until = state["next_retry_at"]
    while time.time() < until:
        control = store.get_record("control", "current", {})
        if runner._stop_requested or control.get("command") in {"pause", "cancel"} or time.time() >= deadline:
            return False
        write_progress_snapshot(runner)
        time.sleep(min(0.5, max(0, until - time.time()), max(0, deadline - time.time())))
    return True


def run_managed(runner):
    if not runner.workspace.exists():
        runner.setup_workspace()
    store = runner_store(runner)
    lock = runner._controller_lock or ControllerLock(store.directory / "controller.lock")
    if runner._controller_lock is None:
        lock.acquire()
    runner._controller_lock = lock
    store.put_record("controller", "identity", process_identity(os.getpid()))
    try:
        current = store.get_record("run", "manifest", {})
        if current.get("run_state") in {"completed", "failed", "cancelled", "budget_exhausted"}:
            raise RunRecoveryError("run_is_terminal")
        policy = configure(store, runner.resume_enabled, runner.resume_policy)
        state = store.get_record("resume", "state", {})
        if not policy["enabled"] and state.get("next_retry_at"):
            state.update(next_retry_at=None, stop_reason="disabled_by_operator")
            store.put_record("resume", "state", state)
        runner._attempt_start_reason = "manual_resume" if runner._restored else "create"
        # An interrupted cooling interval cannot be bypassed or charged twice.
        pending = bool(policy["enabled"] and state.get("next_retry_at"))
        while True:
            if pending:
                runner._persist_run_manifest(run_state="suspended_infrastructure", phase="waiting_for_provider")
                if not _cooldown(runner, state):
                    state.update(next_retry_at=None, stop_reason="control_or_deadline")
                    store.put_record("resume", "state", state)
                    return _run_attempt(runner)  # prechecks finalize without launching a provider
                state.update(automatic_attempts=state.get("automatic_attempts", 0) + 1, next_retry_at=None)
                store.put_record("resume", "state", state)
                runner._restored = True
                runner._attempt_start_reason = "automatic_resume"
            result = _run_attempt(runner)
            if result["status"] != "suspended_infrastructure" or result.get("termination") != "infrastructure_exit":
                return result
            failure = result.get("error") or {}
            if (policy["enabled"] and runner.agent.get("kind") == "codex"
                    and failure.get("source") == "agent" and is_encrypted_history_error(failure)):
                try:
                    activate_plaintext_fallback(runner, failure, policy, state)
                except (RunRecoveryError, OSError, ValueError, sqlite3.Error) as exc:
                    # Preserve the API failure as well as the reason a safe copy
                    # could not be activated. Never turn this into a retry loop.
                    reason = normalize_error(exc, source="history_recovery")
                    state.update(next_retry_at=None, stop_reason=reason["message"])
                    store.put_records([("history_recovery", "error", reason), ("resume", "state", state)])
                    result.update(history_metadata(store))
                    runner._persist_run_manifest(run_state=result["status"], **history_metadata(store))
                    runner._write_meta(result["status"], result)
                    write_workspace_results(runner.workspace)
                    runner._finalize_evidence(result["status"], result)
                    return result
                runner._restored = True
                runner._attempt_start_reason = "plaintext_history_resume"
                pending = False
                continue
            delay, reason = retry_delay(result.get("error"), policy, state)
            if delay is None:
                state.update(next_retry_at=None, stop_reason=reason)
                store.put_record("resume", "state", state)
                return result
            # Refuse a retry before sleeping if no original conversation can be verified.
            try:
                validate_session(runner)
            except RunRecoveryError as exc:
                error = normalize_error(exc, source="controller")
                runner._persist_run_manifest(run_state="recovery_blocked", error=error)
                runner._write_meta("recovery_blocked", {**result, "status": "recovery_blocked", "error": error})
                return {**result, "status": "recovery_blocked", "error": error}
            # Reserve the entire scheduled delay durably. A crash or manual restart
            # never replenishes the wait budget or shortens Retry-After.
            state.update(stage="agent", next_retry_at=time.time() + delay,
                         wait_budget_used_seconds=state.get("wait_budget_used_seconds", 0) + delay,
                         stop_reason=None)
            store.put_record("resume", "state", state)
            pending = True
    finally:
        store.put_record("controller", "identity", {})
        lock.release()
        runner._controller_lock = None
        from ..provenance.progress_snapshot import write_progress_snapshot
        write_progress_snapshot(runner, force=True)

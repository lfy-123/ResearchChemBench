"""Recover a completed Codex handoff without restarting the research."""
from __future__ import annotations

import json
import os
import signal
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.execution_states import TERMINAL_STATES
from chemistry_toolbox.src.recovery_io import atomic_json, file_hash, process_identity, signal_identity
from .codex_history import session_home, session_rollout
from .output_contract import validate_saved_submission
from .recovery import ControllerLock, RunRecoveryError, write_run_manifest


def _prepare(workspace, store):
    meta = json.loads((workspace / "_meta.json").read_text())
    manifest = store.get_record("run", "manifest", {})
    if manifest.get("agent_kind") != "codex" or manifest.get("run_state") not in {
            "running", "finalizing", "suspended_infrastructure"}:
        raise RunRecoveryError("finalization_requires_unfinished_codex_handoff")
    if store.get_record("control", "current", {}).get("command") in {"pause", "cancel"}:
        raise RunRecoveryError("run_explicitly_stopped")
    live = []
    for namespace in ("controller", "agent"):
        saved = store.get_record(namespace, "identity", {})
        owner = {key: saved[key] for key in ("host", "boot_id", "pid", "start_ticks", "pgid") if key in saved}
        # Shared files and locally absent PIDs do not prove remote process exit.
        if owner.get("host") != socket.gethostname():
            raise RunRecoveryError(f"original_{namespace}_host_unverified: {owner.get('host')}")
        if not all(key in owner for key in ("pid", "boot_id", "start_ticks")):
            raise RunRecoveryError(f"original_{namespace}_identity_incomplete")
        if process_identity(owner.get("pid"), owner)["verified"]:
            if owner["pid"] == os.getpid():
                raise RunRecoveryError("cannot_retire_current_process")
            live.append({"role": namespace, "identity": owner})
    if any(j["state"] not in TERMINAL_STATES for j in store.list_jobs()):
        raise RunRecoveryError("jobs_not_terminal")
    frozen = store.get_record("frozen", "files", {})
    if not frozen:
        raise RunRecoveryError("frozen_inputs_missing")
    for name, digest in frozen.items():
        if file_hash(workspace / name) != digest:
            raise RunRecoveryError(f"frozen_input_modified: {name}")
    attempt = store.get_record("attempt", manifest["attempt_id"], {})
    path = session_rollout(session_home(store), manifest.get("provider_session_id"), workspace)
    completion, line_number = None, 0
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            if line.strip():
                completion = json.loads(line)
    if not completion or completion.get("type") != "event_msg" or completion.get("payload", {}).get("type") != "task_complete":
        raise RunRecoveryError("native_session_has_no_final_completion")
    ended = datetime.fromisoformat(completion["timestamp"].replace("Z", "+00:00")).timestamp()
    if ended < attempt["start_at"] or ended > datetime.fromisoformat(manifest["deadline_at"]).timestamp():
        raise RunRecoveryError("completion_outside_recorded_attempt_budget")
    task = store.directory / "task_snapshot" / meta["task_type"] / meta["paper_id"]
    if not task.is_dir():
        raise RunRecoveryError("original_task_snapshot_unavailable")
    validation = validate_saved_submission(workspace, task)
    result = {"status": "completed" if validation["valid"] else "failed", "applied": False,
              "submission_validation": validation, "remaining_processes": live, "automatic_restart": False,
              "completion_source": {"path": str(path), "line": line_number,
                                    "timestamp": completion["timestamp"], "sha256": file_hash(path)}}
    return meta, manifest, attempt, ended, result


def finalize_completed(workspace, *, apply=False, stop_completed_processes=False):
    workspace = Path(workspace).resolve()
    store = ExecutionStore.open_existing(workspace)
    if store is None:
        raise RunRecoveryError("finalization_requires_saved_control_records")
    previous = store.get_record("repair", "native_completion")
    if not previous and store.get_record("run", "manifest", {}).get("run_state") == "completed" and json.loads(
            (workspace / "_meta.json").read_text()).get("status") == "completed":
        return {"status": "completed", "applied": False, "already_finalized": True, "automatic_restart": False}
    if not previous:
        meta, manifest, attempt, ended, result = _prepare(workspace, store)
        if not apply:
            return result
        live = result["remaining_processes"]
        if live and not stop_completed_processes:
            raise RunRecoveryError("completed_processes_still_running; inspect preview and use --stop-completed-processes")
        if live:
            store = ExecutionStore(workspace, run_id=store.run_id)
            store.put_record("repair", "completed_process_retirement", result)
            # Only explicitly requested, identity-verified remnants of a completed
            # turn are retired. Never signal process groups or scientific workers.
            for owner in live:
                identity = owner["identity"]
                if process_identity(identity["pid"], identity)["verified"] and not signal_identity(identity, signal.SIGKILL):
                    raise RunRecoveryError("completed_process_retirement_failed")
            deadline = time.monotonic() + 3
            while any(process_identity(x["identity"]["pid"], x["identity"])["verified"] for x in live):
                if time.monotonic() >= deadline:
                    raise RunRecoveryError("completed_processes_not_stopped")
                time.sleep(0.05)
            result["retired_processes"] = live
            result["remaining_processes"] = []
    with ControllerLock(store.directory / "controller.lock"):
        previous = store.get_record("repair", "native_completion")
        if previous:
            meta = json.loads((workspace / "_meta.json").read_text())
            manifest = store.get_record("run", "manifest", {})
            if meta not in (previous["before_meta"], previous["after_meta"]) or manifest not in (
                    previous["before_manifest"], previous["after_manifest"]):
                raise RunRecoveryError("run_changed_since_finalization")
            updated, updated_manifest = previous["after_meta"], previous["after_manifest"]
        else:
            checked = _prepare(workspace, store)
            if checked[4]["remaining_processes"] or checked[:3] != (meta, manifest, attempt) or checked[4]["completion_source"] != result["completion_source"]:
                raise RunRecoveryError("run_changed_during_finalization")
            store = ExecutionStore(workspace, run_id=store.run_id)
            from .usage_accounting import ingest_file
            from ..provenance.trace import load_tool_trace, process_metrics
            path = Path(result["completion_source"]["path"])
            ingest_file(store, path, session_id=manifest["provider_session_id"], max_bytes=max(1, path.stat().st_size))
            attempt_id = manifest["attempt_id"]
            finished = {**attempt, "end_at": ended, "end_reason": "agent_completed", "exit_code": None,
                        "completion_source": result["completion_source"], "usage_total": store.usage()}
            validation, status = result["submission_validation"], result["status"]
            updated = {**meta, **process_metrics(load_tool_trace(workspace), workspace=workspace),
                       "status": status, "termination": "agent_completed", "exit_code": None, "error": None,
                       "submission_validation": validation, "submission_findings": validation["errors"],
                       "required_deliverable_status": validation["checked_files"],
                       "report_exists": (workspace / "report/report.md").is_file(),
                       "usage": store.usage(), "usage_details": store.usage_details(),
                       "duration_seconds": ended - attempt["start_at"],
                       "run_elapsed_seconds": ended - datetime.fromisoformat(manifest["first_started_at"]).timestamp(),
                       "attempts": [finished if key == attempt_id else value for key, value in store.records("attempt").items()],
                       "status_correction": "recorded_native_completion", "completion_source": result["completion_source"]}
            updated_manifest = {**manifest, **updated, "run_state": status, "phase": status}
            previous = {"at": datetime.now(timezone.utc).isoformat(), "before_meta": meta, "after_meta": updated,
                        "before_manifest": manifest, "after_manifest": updated_manifest, "before_attempt": attempt,
                        "before_control": store.get_record("control", "current"), "result": result}
            store.put_records([("repair", "native_completion", previous), ("attempt", attempt_id, finished)])
        if apply:
            store = ExecutionStore(workspace, run_id=store.run_id)
            store.put_records([("run", "manifest", updated_manifest),
                               ("control", "current", {"command": "finalize", "reason": "recorded_native_completion"})])
            atomic_json(workspace / "_meta.json", updated)
            write_run_manifest(workspace, updated_manifest)
            from ..provenance.results import write_workspace_results
            from .control import refresh_batch
            write_workspace_results(workspace)
            refresh_batch(workspace, store)
        return {**previous["result"], "applied": apply}

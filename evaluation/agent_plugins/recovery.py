"""Explicit checkpoint recovery for opt-in external agents, not Codex sessions."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import uuid

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.recovery_io import atomic_json, file_hash, file_lock, process_identity
from evaluation.execution.recovery import canonical_config_hash, load_run_manifest


def inspect_external_resume(workspace, *, extra_calls=0, timeout_seconds=None):
    workspace = Path(workspace).resolve(strict=True)
    manifest = load_run_manifest(workspace)
    config = manifest["config"]
    definition = config.get("agent_definition") or {}
    if definition.get("resume_protocol") != "arche-checkpoint-v1":
        raise ValueError("external_resume_unsupported: this run has no validated checkpoint protocol")
    if manifest.get("run_state") == "completed":
        raise ValueError("run is already completed; resume would repeat completed work")
    if canonical_config_hash(config) != manifest["config_hash"]:
        raise ValueError("frozen configuration hash mismatch")
    if type(extra_calls) is not int or extra_calls < 0 or (timeout_seconds is not None and (type(timeout_seconds) is not int or timeout_seconds < 1)):
        raise ValueError("extra_calls must be nonnegative and resume timeout positive")
    store = ExecutionStore.open_existing(workspace, run_id=manifest["run_id"])
    if store is None:
        raise ValueError("original execution ledger is missing")
    with file_lock(workspace / "recovery/controller.lock", blocking=False):
        pass
    for kind in ("controller", "agent"):
        saved = store.get_record(kind, "identity", {})
        if kind == "controller" and manifest.get("run_state") in {"failed", "cancelled", "budget_exhausted"}:
            continue
        if saved and process_identity(saved.get("pid"), saved).get("verified"):
            raise ValueError("original " + kind + " is still running")
    frozen = store.get_record("frozen", "external_agent", {})
    if not frozen:
        raise ValueError("external protocol checkpoint missing")
    for name, sha in frozen["files"].items():
        if file_hash(workspace / name) != sha:
            raise ValueError("frozen public protocol changed: " + name)
    for name, sha in frozen["command_files"].items():
        if file_hash(Path(name)) != sha:
            raise ValueError("external command changed since checkpoint: " + name)
    # Adapter-owned mechanical verification, imported without native model/runtime
    # initialization. The protocol explicitly declares the supported adapter.
    adapter = Path(__file__).resolve().parents[2] / "custom_agents/Arche-Harness/benchmark_adapter"
    if str(adapter) not in sys.path:
        sys.path.insert(0, str(adapter))
    from rcb_adapter.contract import PublicRequest
    from rcb_adapter.recovery import check_adapter_checkpoint, coordinator_lock
    request = PublicRequest(workspace / "_agent_protocol/request.json")
    with coordinator_lock(request):
        checkpoint = check_adapter_checkpoint(request)
    previous = store.get_record("external_resume", "current", {})
    max_turns = int(previous.get("max_turns", config["max_turns"])) + extra_calls
    budget = json.loads((request.root / "model_budget.json").read_text())
    token_limit = config.get("max_tokens")
    if token_limit and (budget["calls_without_usage"] or budget["observed_input_tokens"] + budget["observed_output_tokens"] >= token_limit):
        raise ValueError("saved token budget is exhausted or has unknown usage; extra calls do not override it")
    used = budget["counted_calls"] + budget.get("inflight_calls", 0)
    deadline = (datetime.now(timezone.utc) + timedelta(seconds=timeout_seconds)).isoformat() if timeout_seconds else manifest["deadline_at"]
    return {"status": "resume_ready" if used < max_turns and datetime.fromisoformat(deadline) > datetime.now(timezone.utc) else "resume_needs_budget",
            "protocol": "arche-checkpoint-v1", "run_id": manifest["run_id"], "workspace": str(workspace),
            "deadline_at": deadline, "max_turns": max_turns, "counted_or_reserved_calls": used,
            "extra_calls": extra_calls, "timeout_seconds": timeout_seconds, "checkpoint": checkpoint,
            "original_manifest": manifest}


def resume_external(workspace, *, extra_calls=0, timeout_seconds=None, check=False):
    from evaluation.execution.runner import TaskRunner
    workspace = Path(workspace).resolve(strict=True)
    with file_lock(workspace / "recovery/external_resume.lock", blocking=False):
        ready = inspect_external_resume(workspace, extra_calls=extra_calls, timeout_seconds=timeout_seconds)
        manifest = ready.pop("original_manifest")
        if check:
            return ready
        if ready["status"] != "resume_ready":
            raise ValueError("resume needs remaining calls and time; provide --extra-calls / --resume-timeout")
        store = ExecutionStore(workspace, run_id=ready["run_id"])
        config = dict(manifest["config"])
        runner = TaskRunner(**config, workspace_root=workspace.parent,
                            task_roots=[manifest["task_snapshot_root"]], _saved_identity=manifest)
        if runner.task_package.package_content_sha256 != manifest["task_package_content_sha256"]:
            raise ValueError("frozen task snapshot changed")
        runner.public_task_files = list(json.loads((workspace / "_agent_protocol/request.json").read_text())["public_input_files"])
        runner.first_started_at = manifest["first_started_at"]
        runner.deadline_at = ready["deadline_at"]
        runner.max_turns = ready["max_turns"]
        runner._restored = True
        number = len(store.records("external_resume_attempt")) + 1
        runner.attempt_id = f"external_resume_{number:04d}_{uuid.uuid4().hex[:8]}"
        context_path = workspace / "_agent_protocol" / "resume_attempts" / (runner.attempt_id + ".json")
        context = {**ready, "attempt_id": runner.attempt_id, "previous_deadline_at": manifest["deadline_at"],
                   "previous_run_state": manifest["run_state"], "created_at": datetime.now(timezone.utc).isoformat()}
        # Coordinate deadline changes with the same manager locks as Codex's
        # operator recovery. Cancelled/failed jobs stay terminal and are never reset.
        with ExitStack() as stack:
            if timeout_seconds is not None:
                stack.enter_context(file_lock(store.directory / "manager_start.lock", blocking=False))
                stack.enter_context(file_lock(store.directory / "manager.lock", blocking=False))
                from chemistry_toolbox.src.execution_states import TERMINAL_STATES
                if any(row["state"] not in TERMINAL_STATES for row in store.list_jobs()):
                    raise ValueError("deadline extension requires original computations to reach terminal state first")
            if store.get_record("run", "manifest") != manifest:
                raise ValueError("run changed during resume preparation")
            import shutil
            history = workspace / "outputs/arche/resume_attempts" / runner.attempt_id
            history.mkdir(parents=True, exist_ok=False)
            for name in ("model_budget.json", "adapter_outcome.json", "application_result.json", "budget_stop.json"):
                source = workspace / "outputs/arche" / name
                if source.is_file():
                    shutil.copy2(source, history / name)
            for name in ("_meta.json", "results.json"):
                source = workspace / name
                if source.is_file():
                    shutil.copy2(source, history / name)
            atomic_json(context_path, context)
            context_path.chmod(0o444)
            store.put_records([
                ("external_resume_attempt", runner.attempt_id, context),
                ("external_resume", "current", context),
                ("control", "current", {"command": "resume", "source": "operator_external_resume"}),
                ("run", "manifest", {**manifest, "run_state": "recovering", "deadline_at": ready["deadline_at"], "attempt_id": runner.attempt_id}),
            ])
        runner._external_resume_context = context_path
        # Keep the original external request and tool configuration immutable.
        try:
            result = runner.run()
        finally:
            store.put_record("external_resume_attempt", runner.attempt_id, {**context, "finished_at": datetime.now(timezone.utc).isoformat()})
        return {"status": result["status"], "workspace": str(workspace), "attempt_id": runner.attempt_id}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--extra-calls", type=int, default=0)
    parser.add_argument("--resume-timeout", type=int)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--score", action="store_true")
    args = parser.parse_args()
    try:
        result = resume_external(args.workspace, extra_calls=args.extra_calls, timeout_seconds=args.resume_timeout, check=args.check)
        if not args.check and args.score and result["status"] == "completed":
            from evaluation.scoring.service import score_workspace
            score = score_workspace(Path(args.workspace))
            result["scoring_status"] = score["status"]
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] in {"completed", "resume_ready"} and result.get("scoring_status", "scored") == "scored" else 2
    except (ValueError, RuntimeError, OSError) as exc:
        print(json.dumps({"status": "resume_blocked", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

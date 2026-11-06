"""Explicit Codex/Claude host migration after the operator confirms the source stopped."""
from __future__ import annotations

import argparse
import copy
from contextlib import ExitStack
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import uuid

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.execution_states import TERMINAL_STATES
from chemistry_toolbox.src.recovery_io import atomic_json, file_hash, file_lock
from .codex_history import session_home, session_rollout
from .recovery import RunRecoveryError, canonical_config_hash
from .wait_policy import probe_cli


def _destination_adapter(workspace, store, manifest, provider):
    """Authenticate old MCP settings before rebinding host-only environment."""
    from .runner import TaskRunner
    runner = TaskRunner(**manifest["config"], workspace_root=workspace.parent,
                        task_roots=[manifest["task_snapshot_root"]], _saved_identity=manifest)
    runner.first_started_at = manifest["first_started_at"]
    runner.deadline_at = manifest["deadline_at"]
    if manifest["agent_kind"] == "claude":
        runner._agent_environment()
    old = store.get_record("frozen", "adapter")
    if runner._wait_capability != old["wait_capability"] or provider["stdout"] != old["cli_version"]:
        raise RunRecoveryError("provider_wait_capability_drift")
    if runner.task_package.package_content_sha256 != manifest["task_package_content_sha256"]:
        raise RunRecoveryError("task_snapshot_hash_mismatch")
    current = runner._mcp_server_specs()
    new_hash = canonical_config_hash(current)
    if new_hash != old["mcp_hash"]:
        saved = json.loads((workspace / ".mcp.json").read_text())["mcpServers"]
        reconstructed = copy.deepcopy(current)
        for server in reconstructed:
            environment = saved[server["name"]]["env"]
            pool_key = "RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT"
            if environment.get(pool_key) != server["environment"].get(pool_key):
                source_host = store.get_record("agent", "identity")["host"]
                if (environment.get(pool_key) != str(store.directory.parent / ("host_" + source_host))
                        or server["environment"].get(pool_key) != str(store.directory.parent / ("host_" + socket.gethostname()))):
                    raise RunRecoveryError("host_migration_custom_resource_pool_changed")
            for key in ("PATH", "LD_LIBRARY_PATH", "RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT"):
                if key in environment:
                    server["environment"][key] = environment[key]
                else:
                    server["environment"].pop(key, None)
        if canonical_config_hash(reconstructed) != old["mcp_hash"]:
            raise RunRecoveryError("host_migration_non_host_mcp_configuration_drift")
    return {**old, "mcp_hash": new_hash}


def migrate_codex_run(workspace, from_host, *, apply=False):
    """Keep the native session/results; never relaunch interrupted computations.

    --from-host is the operator's assertion that this exact instance stopped.
    A missing PID on the destination is not evidence about the source machine.
    """
    workspace = Path(workspace).resolve(strict=True)
    store = ExecutionStore.open_existing(workspace, run_id=workspace.name)
    if store is None:
        raise RunRecoveryError("host_migration_requires_execution_ledger")
    target = socket.gethostname()
    if not from_host or from_host == target:
        raise RunRecoveryError("host_migration_requires_different_original_host")
    with ExitStack() as locks:
        for name in ("host_migration.lock", "controller.lock", "manager_start.lock", "manager.lock", "reconcile.lock"):
            try:
                locks.enter_context(file_lock(store.directory / name, blocking=False))
            except BlockingIOError as exc:
                raise RunRecoveryError("host_migration_requires_idle_run: " + name) from exc
        manifest = store.get_record("run", "manifest", {})
        if (manifest.get("agent_kind") not in {"codex", "claude"} or not manifest.get("recovery_enabled")
                or manifest.get("config", {}).get("execution_mode") != "local"):
            raise RunRecoveryError("host_migration_requires_recoverable_local_codex_or_claude")
        if manifest.get("run_id") != workspace.name or manifest.get("run_state") not in {
            "running", "recovering", "suspended_infrastructure", "paused",
        }:
            raise RunRecoveryError("host_migration_requires_unfinished_run")
        if store.get_record("control", "current", {}).get("command") == "cancel":
            raise RunRecoveryError("host_migration_does_not_reopen_cancelled_run")
        identities = {kind: store.get_record(kind, "identity", {}) for kind in ("agent", "controller", "manager")}
        previous = store.get_record("host_migration", "current", {})
        if (previous.get("from_host") == from_host and previous.get("to_host") == target
                and identities["agent"].get("host") == target):
            return {"status": "host_migration_already_applied", "audit_directory": previous["audit_directory"]}
        if identities["agent"].get("host") != from_host:
            raise RunRecoveryError("host_migration_source_mismatch: " + str(identities["agent"].get("host")))
        if any(v.get("host") not in {None, from_host} for v in identities.values()):
            raise RunRecoveryError("host_migration_conflicting_process_owner")
        if canonical_config_hash(manifest["config"]) != manifest.get("config_hash"):
            raise RunRecoveryError("configuration_hash_mismatch")
        if datetime.fromisoformat(manifest["deadline_at"]) <= datetime.now(timezone.utc):
            raise RunRecoveryError("host_migration_deadline_expired; migration does not reset time")
        frozen = store.get_record("frozen", "files", {})
        if not frozen:
            raise RunRecoveryError("host_migration_frozen_inputs_missing")
        for name, sha in frozen.items():
            path = workspace / name
            if not path.resolve().is_relative_to(workspace) or not path.is_file() or file_hash(path) != sha:
                raise RunRecoveryError("frozen_input_modified: " + name)
        if manifest["agent_kind"] == "claude":
            from types import SimpleNamespace
            from .claude_adapter import session_path
            session_path(SimpleNamespace(workspace=workspace, run_id=workspace.name,
                         _resume_session_id=manifest.get("provider_session_id")), required=True)
        else:
            session_rollout(session_home(store), manifest.get("provider_session_id"), workspace)
        adapter = store.get_record("frozen", "adapter", {})
        executable = os.environ.get("RCB_" + manifest["agent_kind"].upper() + "_EXECUTABLE") or adapter.get("executable")
        if not executable or not adapter.get("cli_version"):
            raise RunRecoveryError("host_migration_provider_checkpoint_missing")
        provider = probe_cli(executable)
        if provider["stdout"] != adapter["cli_version"]:
            raise RunRecoveryError("host_migration_requires_matching_cli: saved=" + adapter["cli_version"]
                                   + "; current=" + provider["stdout"])
        if provider["resolved_executable"] != shutil.which(adapter["executable"]):
            raise RunRecoveryError("host_migration_provider_executable_changed")
        destination_adapter = _destination_adapter(workspace, store, manifest, provider)

        # Inspect every proposed transition before changing any job. A genuine
        # supervisor completion, authenticated by its launch token, wins over
        # the stale running row. Otherwise interruption is cancellation, not a
        # successful scientific result. Completed jobs are never rewritten.
        changes = []
        for job in store.list_jobs():
            if job["run_id"] != workspace.name:
                raise RunRecoveryError("host_migration_job_run_mismatch")
            if job["state"] in TERMINAL_STATES:
                continue
            if job["entity_type"] != "job":
                raise RunRecoveryError("host_migration_active_batch_requires_reconciliation")
            facts = json.loads(job["state_json"])
            claim = store.get_record("launch_claim", job["entity_id"], {})
            owners = [facts.get("supervisor_identity", {}), facts.get("child_identity", {}), claim.get("identity", {})]
            if any(owner.get("host") not in {None, from_host} for owner in owners):
                raise RunRecoveryError("host_migration_conflicting_job_owner: " + job["entity_id"])
            terminal_path = store.directory / "terminal" / (job["entity_id"] + ".json")
            terminal = None
            if terminal_path.exists():
                terminal = json.loads(terminal_path.read_text())
                if (not isinstance(terminal, dict) or terminal.get("status") not in TERMINAL_STATES
                        or terminal.get("job_id") != job["entity_id"] or not facts.get("launch_token")
                        or terminal.get("launch_token") != facts["launch_token"]):
                    raise RunRecoveryError("host_migration_invalid_terminal_record: " + job["entity_id"])
            changes.append({"job_id": job["entity_id"], "previous_state": job["state"],
                            "state": terminal["status"] if terminal else "cancelled", "terminal": terminal})

        result = {"status": "host_migration_ready", "run_id": workspace.name,
                  "from_host": from_host, "to_host": target, "operator_asserted_source_stopped": True,
                  "job_changes": [{k: v for k, v in row.items() if k != "terminal"} for row in changes],
                  "session_preserved": True, "automatic_restarts": 0, "model_requests_started": False}
        if not apply:
            return result
        store = ExecutionStore(workspace, run_id=workspace.name)
        migration_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:8]
        audit = store.directory / "host_migrations" / migration_id
        audit.mkdir(parents=True, mode=0o700)
        backup = audit / "execution.sqlite3"
        backup.touch(mode=0o600)
        with store._connect() as source, sqlite3.connect(backup) as destination:
            source.backup(destination)
        record = {**result, "migration_id": migration_id, "audit_directory": str(audit),
                  "at": datetime.now(timezone.utc).isoformat(), "previous_identities": identities, "status": "prepared",
                  "previous_adapter": adapter, "destination_adapter": destination_adapter}
        atomic_json(audit / "migration.json", record)
        # A crash before the final ownership commit leaves the old identity;
        # retrying with the same source safely finishes any remaining changes.
        for row in changes:
            job_id = row["job_id"]
            status = row["terminal"] or {
                "job_id": job_id, "status": "cancelled", "finished_at": record["at"],
                "error": "Original host stopped; no terminal completion record. Partial files are preserved; inspect them before submitting any continuation.",
                "termination_source": "operator_host_migration", "migration_id": migration_id,
            }
            store.record_job_state(job_id, row["state"], expected_state=row["previous_state"],
                                   event_type="operator_host_migration", state_payload={
                                       "status": status, "reason": "source_host_stopped" if row["terminal"] is None else "saved_terminal_record",
                                       "migration_id": migration_id, "automatic_restart": False})
        record["status"] = "applied"
        owner = {"host": target, "pid": None, "migration_id": migration_id, "reason": "source_host_stopped"}
        store.put_records([
            ("host_migration", "current", record), ("host_migration_history", migration_id, record),
            ("frozen", "adapter", destination_adapter),
            *[(kind, "identity", owner) for kind in identities],
            ("run", "manifest", {**manifest, "run_state": "suspended_infrastructure", "host_migration_id": migration_id}),
        ])
        atomic_json(audit / "migration.json", record)
        return {**result, "status": "host_migration_applied", "audit_directory": str(audit)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--from-host", required=True, help="Exact original hostname; asserts that its instance has stopped.")
    parser.add_argument("--apply", action="store_true", help="Apply the audited migration; default only checks.")
    args = parser.parse_args()
    try:
        print(json.dumps(migrate_codex_run(args.workspace, args.from_host, apply=args.apply), ensure_ascii=False))
        return 0
    except (RunRecoveryError, OSError, ValueError, sqlite3.Error) as exc:
        print(json.dumps({"status": "host_migration_blocked", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

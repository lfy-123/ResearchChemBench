"""Use the configured API when resuming stopped, unscored benchmark runs.

Only provider addresses change. Tasks, model choices, sessions, budgets and job
states are retained. A private journal makes interrupted publication replayable.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import socket
from urllib.parse import urlsplit
import uuid

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.execution_states import TERMINAL_STATES
from chemistry_toolbox.src.recovery_io import atomic_json, file_lock, process_identity
from .recovery import RunRecoveryError, canonical_config_hash, _cancelled_resume_allowed


def read_json(path):
    return json.loads(Path(path).read_text()) if Path(path).is_file() else None


def provider_hash(base, model):
    return hashlib.sha256(json.dumps([base, model]).encode()).hexdigest()


def normalize_base(value):
    value = value.rstrip("/")
    parsed = urlsplit(value)
    if (parsed.scheme not in {"http", "https"} or not parsed.hostname or
            parsed.username or parsed.password or parsed.query or parsed.fragment or
            any(c.isspace() for c in value)):
        raise RunRecoveryError("invalid_provider_url")
    parsed.port
    return value if parsed.path else value + "/v1"


def check_idle(case, workspace, store, *, from_host=None, resume_cancelled=False):
    manifest = store.get_record("run", "manifest", {})
    identities = [store.get_record(kind, "identity", {}) for kind in ("agent", "controller")]
    identities += [read_json(case / ".runtime/launcher_identity.json") or {},
                   read_json(case / "launch/evaluator_identity.json") or {}]
    submission = read_json(case / "submission.json") or {}
    if submission.get("resume_log"):
        log = Path(submission["resume_log"]).resolve()
        if not log.is_relative_to(case):
            raise RunRecoveryError("resume_log_outside_case")
        identities.append(read_json(log.parent / "evaluator_identity.json") or {})
    settings = read_json(case / "test_settings.json") or {}
    owners = {i["host"] for i in identities if i.get("host")}
    if settings.get("host"):
        owners.add(settings["host"])
    local_host = socket.gethostname()
    if from_host == local_host:
        raise RunRecoveryError("source_host_must_differ_from_current_host")
    allowed_hosts = {local_host, from_host} if from_host else {local_host}
    if not owners or not owners.issubset(allowed_hosts):
        raise RunRecoveryError("run_api_migration_on_original_host: " + ", ".join(sorted(owners)))
    for identity in identities:
        if identity.get("pid") and process_identity(identity["pid"], identity).get("verified"):
            raise RunRecoveryError("api_migration_requires_stopped_agent_and_controller")
    allowed = {"failed"} if manifest.get("agent_kind") == "external" else {"suspended_infrastructure", "paused"}
    if resume_cancelled:
        if manifest.get("agent_kind") != "codex" or not _cancelled_resume_allowed(manifest, store.get_record("control", "current", {})):
            raise RunRecoveryError("resume_cancelled_requires_cancelled_run; usage budgets cannot be reopened")
        allowed.add("cancelled")
    if from_host:
        # The existing --migrate-from-host option asserts that the source has
        # stopped. Its native host-migration step still reconciles jobs/ownership.
        allowed |= {"running", "recovering", "starting"}
    if manifest.get("run_state") not in allowed:
        raise RunRecoveryError("api_migration_requires_failed_arche_or_suspended_codex")
    # A paused Codex can resume while its independently managed computations
    # continue. Changing API addresses does not change their specs or budgets.
    if (resume_cancelled or (not from_host and manifest.get("agent_kind") != "codex")) and any(job["state"] not in TERMINAL_STATES for job in store.list_jobs()):
        raise RunRecoveryError("api_migration_requires_no_active_or_uncertain_jobs")
    if datetime.fromisoformat(manifest["deadline_at"]) <= datetime.now(timezone.utc) + timedelta(seconds=60):
        raise RunRecoveryError("api_migration_requires_remaining_walltime")
    if any((workspace / name).exists() for name in ("_score.json", "_scoring_attempt.json")):
        raise RunRecoveryError("api_migration_requires_scoring_not_started")
    if canonical_config_hash(manifest["config"]) != manifest.get("config_hash"):
        raise RunRecoveryError("configuration_hash_mismatch")
    return manifest


def build_plan(case, workspace, store, base, model):
    manifest = store.get_record("run", "manifest")
    old_base = manifest["config"]["codex_base_url"]
    if manifest["config"]["codex_model"] != model:
        raise RunRecoveryError("api_migration_cannot_change_model")
    records, files = [], []

    def record(namespace, key, updated):
        previous = store.get_record(namespace, key)
        if previous != updated:
            records.append({"namespace": namespace, "key": key, "before": previous, "after": updated})

    def file(path, updated):
        previous = read_json(path)
        if previous != updated:
            files.append({"path": str(path), "before": previous, "after": updated,
                          "mode": path.stat().st_mode & 0o777 if path.exists() else 0o600})

    updated = copy.deepcopy(manifest)
    updated["config"]["codex_base_url"] = base
    updated["config_hash"] = canonical_config_hash(updated["config"])
    record("run", "manifest", updated)
    origin = store.get_record("batch", "origin")
    if origin:
        origin = copy.deepcopy(origin)
        if origin["config"]["judge"]["model"] != model:
            raise RunRecoveryError("api_migration_cannot_change_judge_model")
        origin["config"]["codex_base_url"] = base
        origin["config"]["judge"]["base_url"] = base
        record("batch", "origin", origin)

    if manifest.get("agent_kind") == "codex":
        from .codex_history import session_home, session_rollout
        if not origin or not store.get_record("history_recovery", "active"):
            raise RunRecoveryError("api_migration_requires_saved_judge_and_plaintext_recovery")
        session_rollout(session_home(store), manifest["provider_session_id"], workspace)
        transport = store.get_record("history_transport", "active")
        if not transport or transport.get("provider_sha256") != provider_hash(old_base, model):
            raise RunRecoveryError("history_transport_provider_checkpoint_mismatch")
        record("history_transport", "active", {**transport, "provider_sha256": provider_hash(base, model)})
    elif manifest.get("agent_kind") == "external":
        if manifest["config"].get("agent_definition", {}).get("resume_protocol") != "arche-checkpoint-v1":
            raise RunRecoveryError("api_migration_unsupported_external_agent")
        path = case / "test_settings.json"
        snapshot = read_json(path)
        settings = snapshot["settings"]
        if settings["MODEL"] != model or (settings.get("JUDGE_MODEL") or model) != model:
            raise RunRecoveryError("api_migration_cannot_change_arche_models")
        if settings["BASE_URL"] != old_base:
            raise RunRecoveryError("arche_provider_checkpoint_mismatch")
        settings.update(BASE_URL=base, JUDGE_BASE_URL=base)
        file(path, snapshot)
        path = store.directory / "arche_transport.json"
        bindings = read_json(path)
        providers = bindings["policy"]["providers"]
        if not providers or any(p != {"base": old_base, "model": model} for p in providers.values()):
            raise RunRecoveryError("arche_provider_bindings_mismatch")
        for provider in providers.values():
            provider["base"] = base
        file(path, bindings)
        path = workspace / "outputs/arche/model_history_recovery.json"
        history = read_json(path)
        if history:
            accepted = {provider_hash(old_base, model), provider_hash(base, model)}
            # Earlier migrations updated routing but omitted this checkpoint.
            # Only accept a prior provider proved by this run's applied journal.
            for audit in store.records("api_migration").values():
                if (audit.get("status"), audit.get("workspace"), audit.get("to_base_url"), audit.get("model")) == (
                        "applied", str(workspace), old_base, model):
                    accepted.add(provider_hash(audit["from_base_url"], model))
            for role, saved in history.items():
                if (role not in providers or saved.get("mode") != "plaintext_history"
                        or saved.get("provider_sha256") not in accepted):
                    raise RunRecoveryError("arche_history_provider_checkpoint_mismatch")
                saved["provider_sha256"] = provider_hash(base, model)
            file(path, history)
    else:
        raise RunRecoveryError("api_migration_unsupported_agent")
    # These mirrors are diagnostic projections; the SQLite manifest is authority.
    file(store.directory / "run.json", updated)
    file(workspace / "recovery/run.json", updated)
    return {"id": uuid.uuid4().hex, "status": "prepared", "at": datetime.now(timezone.utc).isoformat(),
            "workspace": str(workspace), "from_base_url": old_base, "to_base_url": base,
            "model": model, "records": records, "files": files}


def publish(store, plan, journal):
    # Accept only a complete old/new value, including after a process interruption.
    for item in plan["records"]:
        if store.get_record(item["namespace"], item["key"]) not in (item["before"], item["after"]):
            raise RunRecoveryError("api_migration_record_changed_since_preparation")
    for item in plan["files"]:
        if read_json(item["path"]) not in (item["before"], item["after"]):
            raise RunRecoveryError("api_migration_file_changed_since_preparation")
    for item in plan["files"]:
        path = Path(item["path"])
        atomic_json(path, item["after"])
        path.chmod(item["mode"])
    store.put_records([(i["namespace"], i["key"], i["after"]) for i in plan["records"]] + [
        ("api_migration", plan["id"], {**{k: v for k, v in plan.items() if k not in {"records", "files"}},
                                      "status": "applied"})])
    atomic_json(journal, {**plan, "status": "applied"})
    journal.chmod(0o600)


def api_is_current(case, workspace, store, base):
    """Do not impose migration-only requirements on ordinary same-API resume."""
    manifest = store.get_record("run", "manifest", {})
    if manifest.get("config", {}).get("codex_base_url") != base:
        return False
    origin = store.get_record("batch", "origin") or {}
    if manifest.get("agent_kind") == "codex":
        return origin.get("config", {}).get("judge", {}).get("base_url") == base
    settings = (read_json(case / "test_settings.json") or {}).get("settings", {})
    providers = (read_json(store.directory / "arche_transport.json") or {}).get("policy", {}).get("providers", {})
    history = read_json(workspace / "outputs/arche/model_history_recovery.json") or {}
    history_current = all(saved.get("provider_sha256") == provider_hash(base, manifest["config"]["codex_model"])
                          for saved in history.values())
    return (settings.get("BASE_URL") == base and (settings.get("JUDGE_BASE_URL") or base) == base
            and bool(providers) and all(p.get("base") == base for p in providers.values()) and history_current)


def migrate(case, base, model, *, apply=False, from_host=None, resume_cancelled=False):
    base = normalize_base(base)
    case = Path(case).resolve(strict=True)
    runs = [p.parent for p in case.glob("runs/cli_runs/batch_*/autonomous_research-*/_meta.json")]
    if len(runs) != 1 or not (case / "submission.json").is_file():
        raise RunRecoveryError("api_migration_requires_one_original_case")
    workspace = runs[0].resolve()
    if not workspace.is_relative_to(case):
        raise RunRecoveryError("workspace_outside_case")
    store = ExecutionStore.open_existing(workspace)
    if store is None:
        raise RunRecoveryError("original_execution_ledger_missing")
    pending = [(p, read_json(p)) for p in (store.directory / "api_migrations").glob("*.json")]
    pending = [(p, v) for p, v in pending if v.get("status") == "prepared"]
    if not pending:
        score = read_json(workspace / "_score.json") or {}
        if store.get_record("run", "manifest", {}).get("run_state") == "completed" and score.get("status") == "scored":
            return {"status": "already_scored", "automatic_restart": False}
        if api_is_current(case, workspace, store, base):
            return {"status": "api_already_current", "base_url": base, "model": model}
    with ExitStack() as stack:
        # An idle Codex manager may stay alive while suspended. It does not use
        # provider settings; keep its deadline/job authority and process untouched.
        for path in [case / ".runtime/launch.lock", store.directory / "controller.lock",
                     workspace / "recovery/external_resume.lock", workspace / "recovery/controller.lock",
                     store.directory / "arche_coordinator.lock", store.directory / "manager_start.lock"]:
            stack.enter_context(file_lock(path, blocking=False))
        if resume_cancelled:
            stack.enter_context(file_lock(store.directory / "manager.lock", blocking=False))
        check_idle(case, workspace, store, from_host=from_host, resume_cancelled=resume_cancelled)
        pending = [(p, read_json(p)) for p in (store.directory / "api_migrations").glob("*.json")]
        pending = [(p, v) for p, v in pending if v.get("status") == "prepared"]
        if len(pending) > 1:
            raise RunRecoveryError("multiple_pending_api_migrations")
        if pending:
            journal, plan = pending[0]
            if (plan["workspace"], plan["to_base_url"], plan["model"]) != (str(workspace), base, model):
                raise RunRecoveryError("finish_previous_api_migration_first")
        else:
            plan = build_plan(case, workspace, store, base, model)
            journal = store.directory / "api_migrations" / (plan["id"] + ".json")
        if not plan["records"] and not plan["files"]:
            return {"status": "api_already_current", "base_url": base, "model": model}
        if apply:
            journal.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            if not pending:
                atomic_json(journal, plan)
                journal.chmod(0o600)
            writer = ExecutionStore(workspace, run_id=workspace.name)
            publish(writer, plan, journal)
        return {"status": "api_migration_applied" if apply else "api_migration_ready",
                "from_base_url": plan["from_base_url"], "base_url": base, "model": model,
                "audit_file": str(journal) if apply else None, "automatic_restart": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--from-host", help="Existing host-migration assertion: the source host has stopped.")
    parser.add_argument("--resume-cancelled", action="store_true", help="Preserve the existing explicit cancelled-run recovery checks.")
    args = parser.parse_args()
    try:
        print(json.dumps(migrate(args.case, args.base_url, args.model, apply=args.apply,
                                 from_host=args.from_host, resume_cancelled=args.resume_cancelled), ensure_ascii=False))
        return 0
    except (RunRecoveryError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "api_migration_blocked", "error": str(exc), "automatic_restart": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

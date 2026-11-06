"""Audited recovery copies for rejected Codex reasoning history.

The original CODEX_HOME is retained. Only a complete, validated copy becomes
active; tool outputs and opaque compaction state are never silently discarded.
Automatic recovery makes one copy by default; explicit repair permits further
generations within the existing retry budget. Once active, the request transport
also filters newly accumulated encrypted reasoning on every subsequent request.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
import uuid
from contextlib import closing
from datetime import datetime, timezone

from chemistry_toolbox.src.recovery_io import atomic_json, file_hash, process_identity
from .recovery import RunRecoveryError


def history_metadata(store):
    record = store.get_record("history_recovery", "active")
    return {"recovery_mode": "plaintext_history" if record else "native",
            "history_recovery": record,
            "history_transport": store.get_record("history_transport", "active"),
            "history_recovery_error": store.get_record("history_recovery", "error")}


def session_home(store):
    record = store.get_record("history_recovery", "active")
    generation = record.get("generation", 1) if isinstance(record, dict) else 1
    if type(generation) is not int or generation < 1:
        raise RunRecoveryError("history_recovery_store_invalid")
    name = "codex_plaintext" if generation == 1 else f"codex_plaintext_{generation:04d}"
    home = store.directory / (name if record is not None else "codex")
    if record is not None and (not isinstance(record, dict) or record.get("mode") != "plaintext_history" or
                              record.get("session_store_path") != str(home.resolve()) or not home.is_dir()):
        raise RunRecoveryError("history_recovery_store_invalid")
    if home.is_symlink():
        raise RunRecoveryError("provider_session_store_symlink")
    return home


def session_rollout(home, session_id, workspace):
    try:
        uuid.UUID(session_id)
    except (ValueError, TypeError, AttributeError) as exc:
        raise RunRecoveryError("provider_session_id_invalid") from exc
    matches = [p for p in (Path(home) / "sessions").rglob("*.jsonl") if session_id in p.name]
    if len(matches) != 1:
        raise RunRecoveryError("provider_session_file_missing_or_ambiguous")
    path = matches[0]
    if path.is_symlink() or not path.resolve().is_relative_to(Path(home).resolve()):
        raise RunRecoveryError("provider_session_path_invalid")
    try:
        with path.open("rb") as handle:
            event = json.loads(handle.readline())
        payload = event["payload"]
        if event.get("type") != "session_meta" or payload.get("id") != session_id or Path(payload.get("cwd", "")).resolve() != Path(workspace).resolve():
            raise ValueError("identity mismatch")
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        raise RunRecoveryError("provider_session_file_missing_or_cwd_mismatch") from exc
    return path


def _contains_cipher(value):
    if isinstance(value, dict):
        return bool(value.get("encrypted_content")) or any(_contains_cipher(v) for v in value.values())
    return isinstance(value, list) and any(_contains_cipher(v) for v in value)


def is_encrypted_reasoning_item(item):
    """The only provider history record supported by plaintext recovery."""
    return isinstance(item, dict) and item.get("type") == "reasoning" and bool(item.get("encrypted_content"))


def plaintext_history_items(items):
    """Copy expanded Responses history without altering ordinary messages/tools."""
    if not isinstance(items, list):
        raise RunRecoveryError("history_recovery_requires_expanded_input")
    retained, removed = [], 0
    for item in items:
        if not isinstance(item, dict) or item.get("type") == "item_reference":
            raise RunRecoveryError("history_recovery_requires_expanded_input")
        if is_encrypted_reasoning_item(item):
            removed += 1
        elif _contains_cipher(item):
            raise RunRecoveryError("history_recovery_unsupported_encrypted_record")
        else:
            retained.append(item)
    return retained, removed


def copy_plaintext_history(source_home, destination, session_id, workspace):
    """Prepare a resume-compatible copy without writing to the source home."""
    source_home, destination = Path(source_home).resolve(), Path(destination)
    if destination.is_symlink() or destination.resolve().is_relative_to(source_home):
        raise RunRecoveryError("history_recovery_destination_invalid")
    destination = destination.resolve()
    source = session_rollout(source_home, session_id, workspace)
    digest = file_hash(source)
    # Recover a crash after publishing the copy but before committing its ledger
    # pointer. Never overwrite an existing, possibly used compatibility session.
    if destination.exists():
        marker = destination / "history_recovery.json"
        record = json.loads(marker.read_text()) if marker.is_file() else {}
        if (not isinstance(record, dict) or record.get("mode") != "plaintext_history"
                or record.get("session_store_path") != str(destination)
                or record.get("source_sha256") != digest or record.get("provider_session_id") != session_id
                or record.get("source_rollout") != str(source)):
            raise RunRecoveryError("history_recovery_copy_conflict")
        target = session_rollout(destination, session_id, workspace)
        if file_hash(target) != record.get("initial_copy_sha256"):
            raise RunRecoveryError("history_recovery_copy_already_modified")
        return record
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".codex_plaintext-", suffix=".tmp", dir=destination.parent))
    try:
        target = staging / source.relative_to(source_home)
        target.parent.mkdir(parents=True)
        removed, kept = [], 0
        with source.open("rb") as original, target.open("xb") as output:
            os.chmod(target, 0o600)
            for number, line in enumerate(original, 1):
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict) or not line.endswith(b"\n"):
                        raise ValueError("invalid JSONL record")
                except (ValueError, UnicodeError) as exc:
                    raise RunRecoveryError(f"history_recovery_malformed_record: line {number}") from exc
                payload = event.get("payload", {})
                if event.get("type") == "session_meta" and (
                        not isinstance(payload, dict) or payload.get("id") != session_id
                        or payload.get("cwd") != str(Path(workspace).resolve())):
                    raise RunRecoveryError(f"history_recovery_session_identity_mismatch: line {number}")
                if event.get("type") == "response_item" and is_encrypted_reasoning_item(payload):
                    removed.append({"line": number, "id": payload.get("id")})
                    continue
                if _contains_cipher(event):
                    raise RunRecoveryError(f"history_recovery_unsupported_encrypted_record: line {number}")
                output.write(line)
                kept += 1
            output.flush()
            os.fsync(output.fileno())
        if not removed:
            raise RunRecoveryError("history_recovery_no_encrypted_reasoning")
        database = source_home / "state_5.sqlite"
        if not database.is_file() or database.is_symlink():
            raise RunRecoveryError("history_recovery_state_db_missing")
        # Copy the SQLite snapshot, not live WAL files or history projections.
        # Codex rebuilds its history projection from the sanitized rollout.
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as src:
            with closing(sqlite3.connect(staging / database.name)) as dst, dst:
                src.backup(dst)
                updated = dst.execute("UPDATE threads SET rollout_path=? WHERE id=? AND cwd=?",
                    (str(destination / source.relative_to(source_home)), session_id, str(Path(workspace).resolve())))
                if updated.rowcount != 1:
                    raise RunRecoveryError("history_recovery_state_db_identity_mismatch")
                if dst.execute("SELECT COUNT(*) FROM threads WHERE id != ?", (session_id,)).fetchone()[0]:
                    # Linked child sessions need their own verified copy path;
                    # never silently discard them or point back to the backup.
                    raise RunRecoveryError("history_recovery_multiple_threads_unsupported")
        if file_hash(source) != digest:
            raise RunRecoveryError("history_recovery_source_changed")
        record = {"mode": "plaintext_history", "created_at": datetime.now(timezone.utc).isoformat(),
                  "provider_session_id": session_id, "source_rollout": str(source),
                  "original_session_store_path": str(source_home), "session_store_path": str(destination),
                  "source_sha256": digest, "initial_copy_sha256": file_hash(target),
                  "removed_reasoning_records": removed, "removed_reasoning_count": len(removed),
                  "retained_record_count": kept, "original_history_preserved": True,
                  "internal_reasoning_preserved": False, "tool_history_preserved": True}
        atomic_json(staging / "history_recovery.json", record)
        os.rename(staging, destination)
        descriptor = os.open(destination.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        return record
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def prepare_history_repair(runner, store, error, policy, state):
    """Prepare a new generation; keep all previous copies and ledger pointers."""
    from .provider_errors import is_encrypted_history_error
    if runner.agent.get("kind") != "codex" or not is_encrypted_history_error(error):
        raise RunRecoveryError("history_repair_requires_encrypted_history_error")
    if state.get("automatic_attempts", 0) >= policy["limits"]["max_attempts"]:
        raise RunRecoveryError("automatic_attempt_limit")
    previous = store.get_record("history_recovery", "active")
    source = session_home(store)
    generation = previous.get("generation", 1) + 1 if previous else 1
    name = "codex_plaintext" if generation == 1 else f"codex_plaintext_{generation:04d}"
    record = copy_plaintext_history(source, store.directory / name, runner._resume_session_id, runner.workspace)
    return {**record, "generation": generation, "source_attempt_id": runner.attempt_id,
            "failure": error, "source": "operator_repair" if getattr(runner, "_repair_history", False) else "automatic_fallback"}


def commit_history_repair(store, record, state):
    previous = store.get_record("history_recovery", "active")
    next_state = {**state, "automatic_attempts": state.get("automatic_attempts", 0) + 1,
                  "next_retry_at": None, "stop_reason": None, "stage": "agent"}
    records = [("history_recovery", "active", record), ("history_recovery", "error", None),
               ("history_recovery_generation", str(record["generation"]), record),
               ("resume", "state", next_state)]
    if previous:
        records.append(("history_recovery_generation", str(previous.get("generation", 1)), previous))
    store.put_records(records)
    state.update(next_state)


def activate_plaintext_fallback(runner, error, policy, state):
    """Called only after a failed attempt while holding the controller lock."""
    from .provider_errors import is_encrypted_history_error
    from .recovery import runner_store
    if not policy["enabled"] or not is_encrypted_history_error(error) or runner.agent.get("kind") != "codex":
        raise RunRecoveryError("history_recovery_not_applicable")
    store = runner_store(runner)
    if store.get_record("history_recovery", "active") and not getattr(runner, "_repair_history", False):
        raise RunRecoveryError("plaintext_history_fallback_already_used")
    if state.get("automatic_attempts", 0) >= policy["limits"]["max_attempts"]:
        raise RunRecoveryError("automatic_attempt_limit")
    if not runner._controller_lock or runner._controller_lock._handle is None:
        raise RunRecoveryError("history_recovery_requires_controller_lock")
    runner.remaining_run_timeout_seconds()
    if runner._stop_requested or store.get_record("control", "current", {}).get("command") in {"pause", "cancel"}:
        raise RunRecoveryError("history_recovery_control_stopped")
    agent = store.get_record("agent", "identity", {})
    identity = process_identity(agent.get("pid"), agent)
    if agent.get("pid") and (identity.get("host") != agent.get("host") or identity.get("alive")):
        raise RunRecoveryError("history_recovery_agent_not_stopped")
    totals = store.usage()
    if totals["turns"] >= runner.max_turns or (runner.max_tokens and totals["input_tokens"] + totals["output_tokens"] >= runner.max_tokens):
        raise RunRecoveryError("run_usage_budget_exhausted")
    record = prepare_history_repair(runner, store, error, policy, state)
    commit_history_repair(store, record, state)
    return record

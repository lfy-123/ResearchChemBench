from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from chemistry_toolbox.mcp import job_manager, managed_supervisor, open_execution
from chemistry_toolbox.mcp.job_manager import JobManager
from chemistry_toolbox.src.recovery_io import atomic_json, process_identity


IDENTITY = {"host": "fixture", "boot_id": "boot", "pid": 123, "start_ticks": 456}


@pytest.fixture
def manager(tmp_path, monkeypatch):
    value = JobManager(tmp_path / "workspace", run_id="reconcile-test")
    monkeypatch.setattr(job_manager, "token_processes", lambda token: [])
    monkeypatch.setattr(value, "_index_result", lambda job_id: {})
    monkeypatch.setattr(job_manager, "process_identity", lambda pid, expected: {
        **expected, "verified": pid == IDENTITY["pid"] and expected.get("start_ticks") == IDENTITY["start_ticks"]})
    return value


def launched(manager, *, claim=True):
    store = manager.store
    job = store.accept_submission(submission_key="one", entity_type="job", request={},
        spec={"job_type": "native_software"}).entity_id
    store.record_job_state(job, "launching", state_payload={"launch_token": "original", "launch_time": 0})
    if claim:
        store.put_record("launch_claim", job, {"launch_token": "original", "identity": IDENTITY}, immutable=True)
        store.record_job_state(job, "running", state_payload={"supervisor_identity": IDENTITY})
    return job


def test_stale_listing_cannot_overwrite_registered_owner(manager, monkeypatch):
    job = launched(manager, claim=False)
    stale = manager.store.list_jobs()
    manager.store.put_record("launch_claim", job, {"launch_token": "original", "identity": IDENTITY})
    manager.store.record_job_state(job, "running", state_payload={"supervisor_identity": IDENTITY})
    monkeypatch.setattr(manager.store, "list_jobs", lambda: stale)
    assert manager.reconcile()["results"][0]["state"] == "running"
    assert manager.store.get_job(job)["state"] == "running"


@pytest.mark.parametrize("new_state", ["running", "cancel_requested", "partial_success"])
def test_state_or_identity_update_during_probe_wins(manager, monkeypatch, new_state):
    job = launched(manager)
    def race(pid, expected):
        manager.store.record_job_state(job, new_state, state_payload={"child_identity": {"pid": 789}})
        return {"verified": False, "reason": "process_missing"}
    monkeypatch.setattr(job_manager, "process_identity", race)
    assert manager.reconcile_job(job)["state"] == new_state
    facts = json.loads(manager.store.get_job(job)["state_json"])
    assert "reason" not in facts


def test_snapshot_guard_detects_identity_change_even_at_same_timestamp(manager):
    job = launched(manager)
    row = manager.store.get_job(job)
    manager.store.record_job_state(job, "running", state_payload={"child_identity": {"pid": 789}})
    with manager.store._connect() as connection:
        connection.execute("UPDATE jobs SET updated_at=? WHERE entity_id=?", (row["updated_at"], job))
    manager.store.record_job_state(job, "needs_reconciliation", expected_snapshot=row,
                                   state_payload={"reason": "stale"})
    assert manager.store.get_job(job)["state"] == "running"


def test_wait_status_recovers_original_verified_owner(manager, monkeypatch):
    job = launched(manager)
    manager.store.record_job_state(job, "needs_reconciliation", state_payload={"reason": "owner_unverified"})
    monkeypatch.setattr(open_execution, "execution_store", lambda: manager.store)
    _, status = open_execution._read_status(job)
    assert status["status"] == "running"
    assert status["reconciliation_reason"] is None
    assert len(manager.store.list_submissions()) == 1
    assert len(manager.store.records("launch_claim")) == 1


@pytest.mark.parametrize("reason", ["launch_exception", "terminal_record_invalid", "launch_identity_mismatch"])
def test_verified_owner_does_not_clear_unrelated_block(manager, reason):
    job = launched(manager)
    manager.store.record_job_state(job, "needs_reconciliation", state_payload={"reason": reason})
    assert manager.reconcile_job(job)["state"] == "needs_reconciliation"
    assert json.loads(manager.store.get_job(job)["state_json"])["reason"] == reason


def test_cancellation_and_native_error_are_not_restored_to_running(manager):
    job = launched(manager)
    manager.store.record_job_state(job, "needs_reconciliation", state_payload={
        "reason": "owner_unverified", "status": {"error": {"code": "surviving_descendants"}}})
    assert manager.reconcile_job(job)["state"] == "needs_reconciliation"
    manager.store.record_job_state(job, "cancel_requested", state_payload={"cancel_reason": "cancel"})
    assert manager.reconcile_job(job)["state"] == "cancel_requested"


def test_live_child_without_original_owner_stays_blocked(manager, monkeypatch):
    job = launched(manager)
    monkeypatch.setattr(job_manager, "process_identity", lambda *args: {"verified": False})
    monkeypatch.setattr(job_manager, "token_processes", lambda token: [{"pid": 789, "verified": True}])
    assert manager.reconcile_job(job)["state"] == "needs_reconciliation"
    assert json.loads(manager.store.get_job(job)["state_json"])["survivors"][0]["pid"] == 789
    assert len(manager.store.records("launch_claim")) == 1


@pytest.mark.parametrize("mismatch", ["token", "pid_reuse"])
def test_mismatched_launch_identity_cannot_be_restored(manager, mismatch):
    job = launched(manager)
    payload = {"reason": "owner_unverified"}
    if mismatch == "token":
        payload["launch_token"] = "different"
    else:
        payload["supervisor_identity"] = {**IDENTITY, "start_ticks": 999}
    manager.store.record_job_state(job, "needs_reconciliation", state_payload=payload)
    row = manager.reconcile_job(job)
    assert row["state"] == "needs_reconciliation"
    assert json.loads(row["state_json"])["reason"] == "launch_identity_mismatch"


@pytest.mark.parametrize("receipt", ["valid", "wrong_token", "wrong_job", "corrupt"])
def test_terminal_receipt_precedes_owner_probe_and_checks_identity(manager, monkeypatch, receipt):
    job = launched(manager)
    terminal = {"job_id": job, "status": "partial_success", "launch_token": "original"}
    if receipt == "wrong_token": terminal["launch_token"] = "other"
    if receipt == "wrong_job": terminal["job_id"] = "other"
    path = manager.store.directory / "terminal" / (job + ".json")
    atomic_json(path, terminal)
    if receipt == "corrupt": path.write_text("{broken")
    monkeypatch.setattr(job_manager, "process_identity", lambda *args: pytest.fail("terminal must be handled first"))
    row = manager.reconcile_job(job)
    assert row["state"] == ("partial_success" if receipt == "valid" else "needs_reconciliation")
    if receipt != "valid":
        assert json.loads(row["state_json"])["reason"] == "terminal_record_invalid"


def test_delayed_original_supervisor_claims_once_after_start_grace(manager, monkeypatch):
    job = launched(manager, claim=False)
    assert manager.reconcile_job(job)["state"] == "needs_reconciliation"
    spec_path = manager.store.directory / "spec.json"
    atomic_json(spec_path, {"workspace": str(manager.workspace), "run_id": manager.run_id, "job_id": job,
                           "launch_token": "original", "status_path": str(manager._directory(job) / "status.json")})
    calls = []
    monkeypatch.setattr(managed_supervisor, "supervise", lambda path: calls.append(path) or 0)
    assert managed_supervisor.main(spec_path) == 0
    assert managed_supervisor.main(spec_path) == 75
    assert len(calls) == 1


def test_supervisor_registration_cannot_override_concurrent_cancel(manager, monkeypatch):
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    job = launched(manager, claim=False)
    spec_path = manager.store.directory / "spec.json"
    atomic_json(spec_path, {"workspace": str(manager.workspace), "run_id": manager.run_id, "job_id": job,
                           "launch_token": "original", "status_path": str(manager._directory(job) / "status.json")})
    original = ExecutionStore.record_job_state
    def cancelling(store, entity_id, state, **kwargs):
        if state == "running":
            original(store, entity_id, "cancel_requested", state_payload={"cancel_reason": "cancel"})
        return original(store, entity_id, state, **kwargs)
    monkeypatch.setattr(ExecutionStore, "record_job_state", cancelling)
    monkeypatch.setattr(managed_supervisor, "supervise", lambda path: pytest.fail("cancelled job launched"))
    assert managed_supervisor.main(spec_path) == 0
    assert manager.store.get_job(job)["state"] == "cancelled"


def test_process_identity_checks_launch_token_without_exposing_environment():
    identity = process_identity(os.getpid())
    assert identity["verified"]
    probe = process_identity(os.getpid(), {**identity, "launch_token": "not-this-process-token"})
    assert not probe["verified"]
    assert probe["reason"] == "launch_token_unverified"

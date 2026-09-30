from __future__ import annotations

from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_models import (
    ExecutionSubmissionLookupRequest,
    NativeJobRequest,
)
from chemistry_toolbox.mcp.execution_store import (
    ExecutionStore,
    SubmissionConflict,
)


def test_submission_receipt_is_replayed_for_identical_request(tmp_path: Path) -> None:
    store = ExecutionStore(tmp_path, run_id="run_test")

    first = store.accept_submission(
        submission_key="candidate_01_opt",
        entity_type="job",
        request={"command": ["mock-program", "input.inp"]},
        input_manifest=[{"target_path": "input.inp", "sha256": "abc"}],
    )
    replay = store.accept_submission(
        submission_key="candidate_01_opt",
        entity_type="job",
        request={"command": ["mock-program", "input.inp"]},
        input_manifest=[{"target_path": "input.inp", "sha256": "abc"}],
    )

    assert replay.replayed is True
    assert replay.entity_id == first.entity_id
    assert replay.receipt_id == first.receipt_id
    assert len(store.list_jobs()) == 1


def test_submission_key_conflict_does_not_create_second_job(tmp_path: Path) -> None:
    store = ExecutionStore(tmp_path, run_id="run_test")
    store.accept_submission(
        submission_key="candidate_01_opt",
        entity_type="job",
        request={"method": "wb97xd"},
    )

    with pytest.raises(SubmissionConflict):
        store.accept_submission(
            submission_key="candidate_01_opt",
            entity_type="job",
            request={"method": "pbe0"},
        )

    assert len(store.list_jobs()) == 1


def test_job_state_and_lookup_preserve_run_scope(tmp_path: Path) -> None:
    store = ExecutionStore(tmp_path, run_id="run_test")
    receipt = store.accept_submission(
        submission_key="batch_01",
        entity_type="batch",
        request={"items": ["a", "b"]},
    )

    store.record_job_state(receipt.entity_id, "queued")
    state = store.record_job_state(
        receipt.entity_id,
        "launching",
        state_payload={"supervisor_pid": 1234},
    )
    record = store.get_submission("batch_01")

    assert state["state"] == "launching"
    assert record is not None
    assert record["job"]["state"] == "launching"
    assert record["job"]["state_json"]


def test_request_models_validate_stable_submission_keys() -> None:
    request = NativeJobRequest(
        software_id="orca",
        executable="orca",
        submission_key="candidate_01:v1",
    )
    assert request.submission_key == "candidate_01:v1"
    assert ExecutionSubmissionLookupRequest(submission_key="candidate_01:v1")

    with pytest.raises(ValueError):
        NativeJobRequest(
            software_id="orca",
            executable="orca",
            submission_key="../relaunch",
        )


def test_future_schema_is_rejected_without_rewriting_it(tmp_path):
    import sqlite3
    store = ExecutionStore(tmp_path, run_id='schema-test')
    with sqlite3.connect(store.path) as connection:
        connection.execute("UPDATE store_meta SET value='999' WHERE key='schema_version'")
    with pytest.raises(ValueError, match='newer'):
        ExecutionStore(tmp_path, run_id='schema-test')
    with sqlite3.connect(store.path) as connection:
        assert connection.execute("SELECT value FROM store_meta WHERE key='schema_version'").fetchone()[0] == '999'


def test_run_scope_and_store_location_are_isolated(tmp_path):
    first = ExecutionStore(tmp_path / 'one',run_id='same-id')
    second = ExecutionStore(tmp_path / 'two',run_id='same-id')
    first.accept_submission(submission_key='same-key',entity_type='job',request={'method':'a'})
    assert second.get_submission('same-key') is None
    assert not first.path.is_relative_to(first.root)

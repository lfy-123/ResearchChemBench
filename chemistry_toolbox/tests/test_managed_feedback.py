import json
import sys

import pytest

from chemistry_toolbox.mcp.action_result_io import save_action_result, read_action_result
from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.mcp.execution_models import JobCollectRequest, JobStatusRequest
from chemistry_toolbox.mcp.job_manager import JobManager
from chemistry_toolbox.mcp.open_execution import collect_execution_job, get_execution_job, _collect_terminal_job


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_RUN_ID", "feedback")
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "local")
    monkeypatch.setenv("RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT", str(tmp_path / "pool"))
    return ExecutionStore(tmp_path, run_id="feedback")


def make_job(store, state="failed", action="calculate_energy"):
    spec = {"job_type": "predefined_action", "action_id": action, "action_request": {"inputs": {}},
            "result_contract_version": 1, "resource_limits": {}}
    receipt = store.accept_submission(submission_key=action, entity_type="job", request={"action": action}, spec=spec)
    job_id = receipt.entity_id
    directory = store.root / "outputs" / "execution_jobs" / job_id
    directory.mkdir(parents=True)
    store.record_job_state(job_id, "running", state_payload={"launch_token": "fixture"})
    error = None if state in {"success", "partial_success"} else {"code": "backend_runtime_error", "message": "native .sccnotconverged marker"}
    status = {"job_id": job_id, "job_type": "predefined_action", "status": state,
              "return_code": 0 if error is None else 1, "error": error}
    store.record_job_state(job_id, state, state_payload={"status": status})
    result = {"status": state, "action": action, "action_version": "1", "backend": "fixture", "requested_backend": "fixture",
              "selection_source": "agent", "error": error, "warnings": ["scientific validation not performed"]}
    return job_id, directory, status, result


@pytest.mark.parametrize("state", ["success", "partial_success", "failed", "invalid_request", "unsupported", "unavailable", "timeout", "cancelled"])
@pytest.mark.parametrize("action", ["calculate_energy", "cluster_conformers"])
def test_wait_get_collect_share_result_facts(store, state, action):
    job, directory, status, result = make_job(store, state, action)
    save_action_result(store, job, "fixture", result)
    collected = collect_execution_job(JobCollectRequest(job_id=job))
    queried = get_execution_job(JobStatusRequest(job_id=job))
    waited = _collect_terminal_job({"directory": directory, "status_record": status, "status": state, "worker_id": None},
                                    previous_status="running", failure_tail_chars=100)
    assert queried["execution_feedback"] == waited["execution_feedback"] == collected["execution_feedback"]
    assert waited["execution_feedback"]["action_status"] == state
    assert collected["action_result"]["warnings"] == result["warnings"]
    assert json.loads((store.root / collected["full_result_ref"]["path"]).read_text()) == result


def test_missing_then_corrupt_then_ready_changes_revision_not_job(store):
    job, _, _, result = make_job(store)
    first = collect_execution_job(JobCollectRequest(job_id=job))
    assert first["ready"] is False and first["result_state"] == "missing"
    assert collect_execution_job(JobCollectRequest(job_id=job))["result_receipt_id"] == first["result_receipt_id"]
    target = store.directory / "action_results" / (job + ".envelope.json")
    target.parent.mkdir(exist_ok=True)
    target.write_text("{")
    broken = collect_execution_job(JobCollectRequest(job_id=job))
    assert broken["result_state"] == "corrupt"
    save_action_result(store, job, "fixture", result)
    ready = collect_execution_job(JobCollectRequest(job_id=job))
    assert ready["ready"] and ready["terminal_revision"] == 3
    assert len(store.list_jobs()) == 1
    assert collect_execution_job(JobCollectRequest(job_id=job))["result_receipt_id"] == ready["result_receipt_id"]


def test_wrong_launch_result_is_rejected(store):
    job, _, _, result = make_job(store)
    save_action_result(store, job, "different-launch", result)
    value, error = read_action_result(store, job)
    assert value is None and error["code"] == "result_corrupt"


def test_explicit_versions_do_not_hide_unrequested_details(store, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION", "2")
    job, _, _, result = make_job(store)
    save_action_result(store, job, "fixture", result)
    first = collect_execution_job(JobCollectRequest(job_id=job))
    version = first["result_version"]
    assert "action_result" in first
    unchanged = collect_execution_job(JobCollectRequest(job_id=job, known_result_version=version))
    assert unchanged["unchanged"] is True
    assert get_execution_job(JobStatusRequest(job_id=job, known_result_version=version))["unchanged"] is True
    assert "action_result" in collect_execution_job(JobCollectRequest(job_id=job, known_result_version="older"))
    assert "action_result" in collect_execution_job(JobCollectRequest(job_id=job))


def test_collection_pagination_covers_all_results_without_rewriting_receipt():
    from chemistry_toolbox.mcp.execution_feedback import page_collection
    value = {"outputs": [{"path": str(i)} for i in range(7)],
             "artifact_manifest": [{"path": str(i)} for i in range(4)]}
    first = page_collection(value, JobCollectRequest(job_id="job_" + "a" * 32, max_files=3))
    second = page_collection(value, JobCollectRequest(job_id="job_" + "a" * 32, max_files=3, file_offset=3))
    last = page_collection(value, JobCollectRequest(job_id="job_" + "a" * 32, max_files=3, file_offset=6))
    assert first["outputs"] + second["outputs"] + last["outputs"] == value["outputs"]
    assert first["pagination"]["outputs"]["next_offset"] == 3
    assert last["pagination"]["outputs"]["next_offset"] is None
    assert first["artifact_manifest"] + second["artifact_manifest"] == value["artifact_manifest"]


def test_terminal_batch_delivers_late_result_update(store):
    child_spec={"job_type":"predefined_action","action_id":"calculate_energy","action_request":{"inputs":{}},
                "result_contract_version":1,"resource_limits":{}}
    batch=store.accept_submission(submission_key="batch",entity_type="batch",entity_prefix="batch",request={},
                                 spec={"job_type":"batch","children":[{"item_id":"a","spec":child_spec}],"budget":{}}).entity_id
    manager=JobManager(store.root,run_id=store.run_id)
    manager._batch(store.get_job(batch),store.spec(batch))
    job=store.get_record("batch_items",batch)["a"]
    manager._directory(job).mkdir(parents=True,exist_ok=True)
    store.record_job_state(job,"running",state_payload={"launch_token":"fixture"})
    store.record_job_state(job,"failed",state_payload={"status":{"job_id":job,"status":"failed","job_type":"predefined_action"}})
    manager.reconcile()
    first=store.get_record("batch_feedback_events",batch)
    assert len(first)==1 and first[0]["type"]=="item_finished"
    save_action_result(store,job,"fixture",{"status":"failed","action":"calculate_energy","action_version":"1",
                       "requested_backend":"fixture","backend":"fixture","selection_source":"agent",
                       "error":{"code":"failure","message":"late specific diagnostic"}})
    manager.reconcile();manager.reconcile()
    events=store.get_record("batch_feedback_events",batch)
    assert [e["sequence"] for e in events]==[1,2]
    assert events[1]["type"]=="result_updated"
    assert json.loads((store.root / "outputs" / "action_batches" / batch / "status.json").read_text())["last_sequence"] == 2
    assert events[1]["execution_feedback"]["diagnostic"]["message"]=="late specific diagnostic"
    assert len(store.list_jobs())==2


def test_nonzero_action_worker_keeps_invalid_request(managed):
    from chemistry_toolbox.mcp.managed_execution import accept
    from chemistry_toolbox.tests.test_job_manager import until
    (managed.workspace / "_toolbox_catalog.json").write_text(json.dumps({"catalog_hash": "fixture"}))
    spec = {"job_type": "predefined_action", "action_id": "fixture_unknown_action", "action_request": {"inputs": {}},
            "result_contract_version": 1, "runtime": "core", "command": [], "stdin_target": None,
            "resource_limits": {"cpu_cores": 1, "memory_mb": 256, "gpu_count": 0, "walltime_seconds": 10}}
    receipt = accept(spec, {"action": "fixture_unknown_action"}, "invalid-action", [], [])
    row = until(lambda: (r if r["state"] in {"invalid_request", "failed"} else None)
                if (r := managed.store.get_job(receipt["job_id"])) else None)
    assert row["state"] == "invalid_request"
    assert json.loads(row["state_json"])["status"]["return_code"] == 1


from chemistry_toolbox.tests.test_job_manager import managed  # Real isolated CPU/manager fixture.

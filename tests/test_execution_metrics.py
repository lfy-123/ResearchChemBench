import json
import shutil

import pytest

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.execution_states import KNOWN_STATES
from evaluation.provenance.results import build_workspace_results
from evaluation.provenance.trace import process_metrics


def event(tool, result, **request):
    return {"tool": tool, "status": result.get("status", "success"),
            "result_preview": result, "arguments": {"request": request}}


def batch_submit(batch="batch_a", items=("a", "b", "c")):
    return event("submit_action_batch_async", {"status": "success", "batch_id": batch, "batch_status": "queued"},
                 action_id="calculate_energy", items=[{"item_id": item} for item in items])


def assert_partition(metrics, *, success=0, partial=0, failed=0, active=0, unknown=0):
    expected = dict(successful=success, partial=partial, failed=failed, active=active, unknown=unknown)
    assert {key: metrics[key + "_managed_scientific_calls"] for key in expected} == expected
    assert metrics["managed_scientific_attempt_count"] == sum(expected.values())


def test_batch_pages_and_receipt_retries_count_children_once():
    first = event("wait_execution_events", {"status": "success", "newly_terminal_items": [
        {"batch_id": "batch_a", "item_id": "a", "status": "success"}],
        "running_items": [{"batch_id": "batch_a", "item_id": "b", "status": "running"}],
        "queued_items": [{"batch_id": "batch_a", "item_id": "c", "status": "queued"}]})
    second = event("wait_execution_events", {"status": "success", "newly_terminal_items": [
        {"batch_id": "batch_a", "item_id": "a", "job_id": "job_a", "status": "success"},
        {"batch_id": "batch_a", "item_id": "b", "job_id": "job_b", "status": "partial_success"},
        {"batch_id": "batch_a", "item_id": "c", "job_id": "job_c", "status": "failed"}]})
    metrics = process_metrics([batch_submit(), batch_submit(), first, second, second,
                              event("collect_execution_job", {"status": "success", "job_id": "job_b", "job_status": "partial_success"})])
    assert_partition(metrics, success=1, partial=1, failed=1)
    assert metrics["submission_accepted_count"] == 1
    assert metrics["execution_job_count"] == 3
    assert metrics["ledger_final_job_states"] == {}
    assert set(metrics["agent_observed_job_states"]) == {"job_a", "job_b", "job_c"}


def test_batch_item_ids_are_scoped_and_unobserved_items_remain_active():
    metrics = process_metrics([batch_submit("batch_a", ("a",)), batch_submit("batch_b", ("a",)),
        event("wait_execution_events", {"status": "success", "newly_terminal_items": [
            {"batch_id": "batch_b", "item_id": "a", "status": "failed"}]})])
    assert_partition(metrics, failed=1, active=1)
    assert metrics["submission_accepted_count"] == 2
    assert len(metrics["agent_observed_job_states"]) == 1


def test_internal_legacy_batch_trace_is_not_double_counted_as_synchronous():
    child = event("calculate_energy", {"status": "partial_success"})
    child["arguments"].update(entrypoint="submit_action_batch_async", batch_id="batch_a", batch_item_id="a")
    metrics = process_metrics([batch_submit(items=("a",)), child, event("wait_execution_events", {
        "status": "success", "newly_terminal_items": [{"batch_id": "batch_a", "item_id": "a", "status": "partial_success"}]})])
    assert_partition(metrics, partial=1)
    assert metrics["submission_accepted_count"] == 1


def test_polling_transport_status_never_becomes_execution_status():
    submit = event("submit_native_job", {"status": "success", "job_id": "job_a", "job_status": "running"})
    for status in ("success", "failed", "invalid_request", "not_found"):
        metrics = process_metrics([submit, event("get_execution_job", {"status": status}, job_id="job_a")])
        assert_partition(metrics, active=1)
        assert metrics["agent_observed_job_states"] == {"job_a": "running"}


@pytest.mark.parametrize("state", sorted(KNOWN_STATES))
def test_shared_states_form_disjoint_categories(state):
    from chemistry_toolbox.src.execution_states import ACTIVE_STATES, TERMINAL_STATES
    metrics = process_metrics([event("calculate_energy", {"status": "success", "job_id": "job_a", "job_status": state})])
    expected = ("success" if state == "success" else "partial" if state == "partial_success" else
                "failed" if state in TERMINAL_STATES else "active" if state in ACTIVE_STATES else "unknown")
    assert_partition(metrics, **{expected: 1})
    assert sum(metrics[key] for key in (
        "successful_execution_job_count", "partial_execution_job_count", "failed_execution_job_count",
        "timeout_execution_job_count", "cancelled_execution_job_count", "rejected_execution_job_count",
        "active_execution_job_count", "unknown_execution_job_count")) == metrics["execution_job_count"]


def test_synchronous_partial_and_request_rejections_have_distinct_counts():
    metrics = process_metrics([event("calculate_energy", {"status": "partial_success"}),
        event("calculate_energy", {"status": "invalid_request"}),
        event("submit_action_batch_async", {"status": "unavailable"}),
        event("submit_native_job", {"status": "failed", "error": {"code": "transport_error"}})])
    assert_partition(metrics, partial=1)
    assert metrics["submission_rejected_count"] == 2
    assert metrics["submission_unconfirmed_count"] == 1


def test_lost_response_lookup_establishes_the_original_attempt():
    metrics = process_metrics([event("submit_native_job", {"status": "failed"}, submission_key="same"), event("lookup_execution_submission", {
        "status": "success", "submission": {"entity_type": "job", "entity_id": "job_a", "state": "accepted",
        "request": {"job_type": "native_software"}, "job": {"entity_id": "job_a", "state": "failed"}}}, submission_key="same")])
    assert_partition(metrics, failed=1)
    assert metrics["submission_accepted_count"] == 1
    assert metrics["submission_unconfirmed_count"] == 0


def test_batch_parent_lookup_keeps_items_and_is_not_an_execution_job():
    metrics = process_metrics([batch_submit(items=("a",)), event("lookup_execution_submission", {
        "status": "success", "batch_id": "batch_a", "submission": {
            "entity_type": "batch", "entity_id": "batch_a", "state": "accepted",
            "job": {"entity_id": "batch_a", "state": "success"}}}),
        event("get_execution_job", {"status": "success", "job": {"job_id": "batch_a", "status": "success"}})])
    assert metrics["execution_job_count"] == 1
    assert_partition(metrics, active=1)
    assert metrics["submission_accepted_count"] == 1


def test_lost_program_response_can_be_accounted_from_ledger_only(tmp_path):
    (tmp_path / "_meta.json").write_text(json.dumps({"run_id": "program"}))
    store = ExecutionStore(tmp_path, run_id="program")
    receipt = store.accept_submission(submission_key="one", entity_type="job", request={},
                                     spec={"job_type": "programmable_analysis"})
    store.record_job_state(receipt.entity_id, "success")
    metrics = process_metrics([], workspace=tmp_path)
    assert_partition(metrics, success=1)
    assert metrics["agent_observed_job_states"] == {}
    assert metrics["ledger_final_job_states"] == {receipt.entity_id: "success"}


def test_feedback_and_lookup_of_a_child_do_not_create_another_submission():
    metrics = process_metrics([batch_submit(items=("a",)), event("wait_execution_events", {
        "status": "success", "newly_terminal_items": [{"batch_id": "batch_a", "item_id": "a",
        "execution_feedback": {"job_id": "job_a", "job_status": "partial_success", "action": "calculate_energy"}}]}),
        event("lookup_execution_submission", {"status": "success", "submission": {
            "entity_type": "job", "entity_id": "job_a", "job": {"entity_id": "job_a", "state": "queued"}}})])
    assert_partition(metrics, partial=1)
    assert metrics["submission_accepted_count"] == 1
    assert metrics["execution_state_conflicts"][0]["resolved_state"] == "partial_success"


def test_invalid_action_arguments_are_rejections_and_future_states_are_unknown():
    metrics = process_metrics([event("submit_action_batch_async", {"status": "invalid_request"}, action_id=[]),
        event("submit_analysis_program", {"status": "success", "job_id": "job_a", "job_status": "future_state"})])
    assert_partition(metrics, unknown=1)
    assert metrics["submission_rejected_count"] == 1


@pytest.mark.parametrize("portable", [False, True])
def test_ledger_replay_resolves_old_batch_ids_without_writing_or_claiming_agent_saw_it(tmp_path, portable):
    root = tmp_path / "live"
    root.mkdir()
    (root / "_meta.json").write_text(json.dumps({"run_id": "test"}))
    store = ExecutionStore(root, run_id="test")
    request = {"action_id": "calculate_energy", "items": [{"item_id": "a"}, {"item_id": "b"}]}
    parent = store.accept_submission(submission_key="batch", entity_type="batch", request=request)
    child_a = store.accept_submission(submission_key="child-a", entity_type="job",
        request={"batch_id": parent.entity_id, "item_id": "a"},
        spec={"parent_batch": parent.entity_id, "job_type": "predefined_action", "action_id": "calculate_energy"})
    child_b = store.accept_submission(submission_key="child-b", entity_type="job",
        request={"batch_id": parent.entity_id, "item_id": "b"},
        spec={"parent_batch": parent.entity_id, "job_type": "predefined_action", "action_id": "calculate_energy"})
    store.record_job_state(child_a.entity_id, "success")
    store.record_job_state(child_b.entity_id, "partial_success")
    trace = [batch_submit(parent.entity_id, ("a", "b")), event("wait_execution_events", {
        "status": "success", "running_items": [{"batch_id": parent.entity_id, "item_id": "a", "status": "running"}]})]
    if portable:
        archive = tmp_path / "archive"
        shutil.copytree(root, archive / "workspace")
        (archive / "control").mkdir()
        shutil.copyfile(store.path, archive / "control/execution.sqlite3")
        root = archive / "workspace"
    before = {p: p.read_bytes() for p in root.parent.rglob("*") if p.is_file()}
    metrics = process_metrics(trace, workspace=root)
    assert_partition(metrics, success=1, partial=1)
    assert metrics["submission_accepted_count"] == 1
    assert metrics["agent_observed_job_states"] == {child_a.entity_id: "running"}
    assert metrics["ledger_final_job_states"] == {child_a.entity_id: "success", child_b.entity_id: "partial_success"}
    assert metrics["execution_state_conflicts"][0]["ledger_state"] == "success"
    assert before == {p: p.read_bytes() for p in root.parent.rglob("*") if p.is_file()}


def test_results_zero_values_override_stale_metadata(tmp_path):
    (tmp_path / "_meta.json").write_text(json.dumps({"successful_managed_scientific_calls": 9,
        "failed_managed_scientific_calls": 5, "tool_call_count": 100}))
    trace = event("submit_native_job", {"status": "success", "job_id": "job_a", "job_status": "queued"})
    (tmp_path / "_tool_trace.jsonl").write_text(json.dumps(trace) + "\n")
    tools = build_workspace_results(tmp_path)["tools"]
    assert tools["calls"] == 1
    assert tools["successful_managed_scientific_calls"] == tools["failed_managed_scientific_calls"] == 0
    assert tools["active_managed_scientific_calls"] == 1

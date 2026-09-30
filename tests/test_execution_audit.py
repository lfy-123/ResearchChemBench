import json
import pytest

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.mcp.tracing import execute_traced
from chemistry_toolbox.mcp.managed_execution import submission_response
from evaluation.provenance.execution_audit import execution_submission_audit
from evaluation.provenance.trace import process_metrics
from evaluation.scoring.policies import _managed_computation_cap


def test_audit_separates_request_acceptance_and_response(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    store = ExecutionStore(tmp_path, run_id="audit")
    def accepted(key):
        receipt = store.accept_submission(submission_key=key, entity_type="job", request={})
        return submission_response(store, receipt)
    execute_traced("submit_native_job", {"request":{"submission_key":"recorded"}}, lambda: accepted("recorded"), capture_artifacts=False)
    accepted("lost-response")
    with (tmp_path/"_tool_call_events.jsonl").open("a") as stream:
        for sequence, key in ((2,"lost-response"), (3,"never-accepted")):
            stream.write(json.dumps({"sequence":sequence,"tool":"submit_native_job","phase":"started","at":"fixture-time","arguments":{"request":{"submission_key":key}}})+'\n')
    (tmp_path/"_agent_output.jsonl").write_text('\n'.join(json.dumps(item) for item in [
        {"type":"item.started", "item":{"id":"call_1","type":"mcp_tool_call","tool":"submit_native_job","arguments":{"request":{"submission_key":"client-only"}}}},
        {"type":"item.started", "item":{"id":"call_2","type":"mcp_tool_call","tool":"submit_native_job","arguments":{"request":{"submission_key":"recorded"}}}},
        {"type":"item.completed", "item":{"type":"agent_message","text":"I submitted 999 jobs"}},
    ]))
    audit = execution_submission_audit(tmp_path, store)
    assert audit['accepted_submission_count'] == 2
    assert audit['request_attempt_count'] == 4
    assert audit['accepted_response_unconfirmed_count'] == 1
    assert audit['unconfirmed_request_count'] == 2
    states = {item['submission_key']:item['outcome'] for item in audit['request_attempts']}
    assert states == {'recorded':'accepted_response_recorded','lost-response':'accepted_response_unconfirmed',
                      'never-accepted':'acceptance_unconfirmed','client-only':'acceptance_unconfirmed'}


def test_async_action_receipt_is_not_counted_as_a_completed_calculation():
    event = {'tool':'calculate_energy','status':'success', 'result_preview':json.dumps({'status':'success','job_id':'job_a','job_status':'queued'})}
    metrics = process_metrics([event])
    assert metrics['successful_managed_scientific_calls'] == 0
    assert metrics['active_managed_scientific_calls'] == 1
    event['result_preview'] = json.dumps({'status':'partial_success','job_id':'job_a','job_status':'partial_success'})
    metrics = process_metrics([event])
    assert metrics['partial_execution_job_count'] == 1
    assert metrics['active_managed_scientific_calls'] == 0


def test_partial_managed_execution_is_not_treated_as_full_success_for_cap():
    cap, reason = _managed_computation_cap(
        {"required": True, "minimum_successful_scientific_calls": 1},
        {
            "managed_scientific_attempt_count": 1,
            "successful_managed_scientific_calls": 0,
            "partial_managed_scientific_calls": 1,
        },
    )
    assert cap == 70.0
    assert "partial" in reason


@pytest.mark.parametrize("tool", ["submit_native_job", "execute_action", "submit_action_batch"])
def test_invalid_client_arguments_do_not_break_final_audit(tmp_path, tool):
    store = ExecutionStore(tmp_path, run_id='invalid-client')
    (tmp_path/'_agent_output.jsonl').write_text(json.dumps({
        'type':'item.started', 'item':{'type':'mcp_tool_call','tool':tool,
                                     'arguments':{'request':{'submission_key':[]}}},
    }))
    audit = execution_submission_audit(tmp_path, store)
    assert audit['accepted_submission_count'] == 0
    assert audit['unconfirmed_request_count'] == 1

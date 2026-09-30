import json

import pytest

from chemistry_toolbox.src.execution_feedback import execution_feedback, diagnostic
from chemistry_toolbox.mcp.result_transport import compact_action_result


@pytest.mark.parametrize("action", ["calculate_energy", "find_transition_state", "cluster_conformers"])
@pytest.mark.parametrize("state", ["success", "partial_success", "failed", "invalid_request", "unsupported", "unavailable", "timeout", "cancelled"])
def test_action_feedback_keeps_outcome_and_error(action, state):
    error = None if state in {"success", "partial_success"} else {"code": "fixture", "message": "specific cause"}
    result = {"action": action, "backend": "fixture", "status": state, "error": error, "warnings": ["some evidence"]}
    view = execution_feedback(status={"job_id": "job_fixture", "status": state, "error": error}, action_result=result)
    assert view["terminal"] is True
    assert view["action_status"] == state
    assert view["warnings"] == ["some evidence"]
    if error:
        assert view["diagnostic"]["message"] == "specific cause"
    assert view["scientific_validation_status"] == "not_checked"


def test_compact_preserves_complete_nested_diagnostic(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    result = {"action": "anything", "status": "failed", "error": {"code": "backend_runtime_error",
        "message": "xTB .sccnotconverged", "nested": {str(i): "诊断" * 10000 for i in range(40)}},
        "warnings": ["warning" * 1000] * 100, "output_artifacts": [{"semantic_type": "BackendDiagnostic", "path": "outputs/error.json"}]}
    value = compact_action_result(result)
    assert value["execution_feedback"]["diagnostic"]["category"] == "numerical_nonconvergence"
    assert value["artifact_handoff"]["primary_output"] is None
    assert len(json.dumps(value).encode()) < 65000
    ref = value["transport"]["full_result_ref"]
    assert json.loads((tmp_path / ref["path"]).read_text()) == result
    assert compact_action_result(result)["transport"]["full_result_ref"] == ref


def test_unknown_exit_does_not_invent_chemistry_and_cancel_wins():
    result = {"status": "failed", "error": {"code": "x", "message": ".sccnotconverged"}}
    view = execution_feedback(status={"status": "cancelled", "error": {"code": "cancelled", "message": "user cancelled"}}, action_result=result)
    assert view["diagnostic"]["category"] == "cancelled"
    assert view["action_error"]["message"] == ".sccnotconverged"
    assert diagnostic({"code": "nonzero_exit", "message": "exit 1"}, status="failed", source="process")["category"] == "unknown"


def test_multi_job_response_retains_errors_and_retrieval_handles():
    from chemistry_toolbox.mcp.result_transport import bound_terminal_items
    items=[]
    for i in range(32):
        view=execution_feedback(status={"job_id":f"job_{i}","status":"failed"},
            action_result={"status":"failed","action":"fixture","error":{"code":"specific_cause","message":"detail "*20000}},
            record={"full_result_ref":{"path":f"outputs/result_{i}.json"},"result_state":"ready"})
        items.append({"job_id":f"job_{i}","status":"failed","execution_feedback":view,"result":{"error":{"code":"specific_cause","message":"detail "*20000}}})
    output=bound_terminal_items(items)
    assert len(json.dumps(output,ensure_ascii=False).encode())<128000
    assert len(output)==32
    assert all(v["execution_feedback"]["diagnostic"]["code"]=="specific_cause" for v in output)
    assert all(v["execution_feedback"]["full_result_ref"]["path"] for v in output)

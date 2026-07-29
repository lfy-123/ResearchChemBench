import json
from pathlib import Path

from evaluation.trace import load_native_agent_trace, process_metrics


def _tool_part(call_id: str, tool: str, *, status: str = "completed"):
    return {
        "type": "tool",
        "tool": tool,
        "callID": call_id,
        "state": {
            "status": status,
            "input": {"command": f"run {tool}"},
            "output": f"{tool} output",
            "metadata": {"exit": 0},
            "time": {"start": 1000, "end": 1500},
        },
    }


def test_native_trace_includes_child_sessions_and_deduplicates_primary(tmp_path: Path):
    workspace = tmp_path / "run"
    workspace.mkdir()
    primary = _tool_part("call-primary", "bash")
    child = _tool_part("call-child", "read")
    invalid = _tool_part("call-invalid", "invalid")
    records = [
        {
            "record_type": "model_step",
            "session_id": "primary",
            "session_step_index": 1,
            "message_id": "message-primary",
            "output": {"parts": [primary]},
        },
        {
            "record_type": "model_step",
            "session_id": "child",
            "session_step_index": 1,
            "message_id": "message-child",
            "output": {"parts": [child, invalid]},
        },
    ]
    (workspace / "_model_io.jsonl").write_text(
        "\n".join(json.dumps(record) for record in records) + "\n"
    )
    (workspace / "_agent_output.jsonl").write_text(
        json.dumps(
            {
                "type": "tool_use",
                "sessionID": "primary",
                "messageID": "message-primary",
                "part": primary,
            }
        )
        + "\n"
    )

    events = load_native_agent_trace(workspace)

    assert len(events) == 3
    assert [event["call_id"] for event in events] == [
        "call-primary",
        "call-child",
        "call-invalid",
    ]
    assert events[1]["session_id"] == "child"
    assert events[1]["source"] == "model_io"
    assert events[2]["status"] == "failed"


def test_process_metrics_count_unmanaged_interpreter_shell_calls(tmp_path: Path):
    workspace = tmp_path / "run"
    workspace.mkdir()
    python_call = _tool_part("call-python", "bash")
    python_call["state"]["input"] = {
        "command": "python3 <<'PY'\nprint(2 + 2)\nPY"
    }
    file_call = _tool_part("call-file", "bash")
    file_call["state"]["input"] = {"command": "wc -l outputs/result.csv"}
    julia_call = _tool_part("call-julia", "bash")
    julia_call["state"]["input"] = {"command": "julia code/fit.jl"}
    record = {
        "record_type": "model_step",
        "session_id": "primary",
        "session_step_index": 1,
        "message_id": "message-primary",
        "output": {"parts": [python_call, file_call, julia_call]},
    }
    (workspace / "_model_io.jsonl").write_text(json.dumps(record) + "\n")

    metrics = process_metrics([], workspace=workspace)

    assert metrics["unmanaged_interpreter_shell_call_count"] == 2
    assert metrics["unmanaged_python_shell_call_count"] == 1
    assert metrics["unmanaged_other_interpreter_shell_call_count"] == 1


def test_process_metrics_count_discovery_bytes_and_semantic_status(tmp_path: Path):
    workspace = tmp_path / "run"
    results = workspace / "_tool_results"
    results.mkdir(parents=True)
    search_result = {
        "status": "success",
        "retrieval": {"mode": "hybrid", "semantic_status": "available"},
        "category_filter_advisory": {
            "code": "exact_match_outside_requested_category"
        },
        "actions": [{"action_id": "optimize_geometry"}],
    }
    inspect_result = {
        "status": "success",
        "action": {"action_id": "optimize_geometry"},
    }
    (results / "0001_search_actions.json").write_text(
        json.dumps(search_result), encoding="utf-8"
    )
    (results / "0002_inspect_action.json").write_text(
        json.dumps(inspect_result), encoding="utf-8"
    )
    events = [
        {
            "tool": "search_actions",
            "status": "success",
            "result_path": "_tool_results/0001_search_actions.json",
        },
        {
            "tool": "inspect_action",
            "status": "success",
            "result_path": "_tool_results/0002_inspect_action.json",
        },
    ]

    metrics = process_metrics(events, workspace=workspace)

    assert metrics["search_actions_call_count"] == 1
    assert metrics["hybrid_search_call_count"] == 1
    assert metrics["semantic_search_available_count"] == 1
    assert metrics["semantic_search_degraded_count"] == 0
    assert metrics["category_filter_advisory_count"] == 1
    assert metrics["discovery_result_bytes"] > 0
    assert metrics["inspect_action_result_bytes"] > 0

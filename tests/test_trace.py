import json
from pathlib import Path

from evaluation.trace import load_native_agent_trace


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

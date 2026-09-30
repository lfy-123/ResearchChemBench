import json

from evaluation.provenance.agent_events import event_capture_summary, load_agent_events
from evaluation.provenance.trace import load_native_agent_trace
from evaluation.provenance.model_io import export_model_io_trace


def test_codex_call_identity_scope_unknown_events_and_model_io(tmp_path):
    def item(phase, id, kind="command_execution", **extra):
        return {"type": "item." + phase, "item": {"id": id, "type": kind, "status": "completed" if phase == "completed" else "in_progress", **extra}}
    events = [{"type": "thread.started", "thread_id": "s"}, {"type": "turn.started"},
              item("started", "i", command="same"), item("completed", "i", command="same", exit_code=0),
              item("completed", "i", command="same", exit_code=0),
              item("completed", "j", command="same", exit_code=1),
              item("completed", "k", kind="mcp_tool_call", tool="wait"),
              item("completed", "l", kind="file_change", changes=[]),
              {"type": "turn.completed", "usage": {}}, {"type": "future", "extra": 1},
              {"type": "thread.started", "thread_id": "s"}, {"type": "turn.started"},
              item("completed", "i", command="same", exit_code=0)]
    (tmp_path / "_agent_output.jsonl").write_text("\n".join(map(json.dumps, events)) + "\nnon-json diagnostic\n")
    native = load_native_agent_trace(tmp_path)
    assert len(native) == 4
    assert [e["status"] for e in native] == ["success", "failed", "success", "success"]
    capture = event_capture_summary(load_agent_events(tmp_path))
    assert capture["unparsed_event_count"] == 2
    assert capture["model_api_request_count"] is None
    summary = export_model_io_trace(tmp_path)
    assert summary["model_step_count"] is None
    assert summary["event_capture"]["completed_native_call_count"] == 4
    assert len(load_native_agent_trace(tmp_path)) == 4


def test_other_provider_events_remain_observable(tmp_path):
    (tmp_path / "_agent_output.jsonl").write_text(json.dumps({"type": "assistant", "message": {"content": "answer"}}) + "\n" + json.dumps({"type": "new_mock_event"}))
    values = load_agent_events(tmp_path)
    assert values[0]["provider"] == "claude" and values[0]["text"] == "answer"
    assert values[1]["kind"] == "unparsed"

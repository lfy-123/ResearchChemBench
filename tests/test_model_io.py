import json
import sqlite3
from pathlib import Path

from evaluation.provenance.model_io import export_model_io_trace


def _insert(connection, table, values):
    placeholders = ", ".join("?" for _ in values)
    connection.execute(
        f"INSERT INTO {table} VALUES ({placeholders})",
        tuple(values),
    )


def test_opencode_model_io_export_is_event_sourced_and_redacted(tmp_path: Path):
    workspace = tmp_path / "run"
    database_dir = workspace / "_opencode"
    database_dir.mkdir(parents=True)
    (workspace / "INSTRUCTIONS.md").write_text("Initial scientific task\n")
    (workspace / "_toolbox_catalog.json").write_text("{}\n")
    (workspace / "opencode.json").write_text("{}\n")
    (workspace / "_agent_output.jsonl").write_text("")

    connection = sqlite3.connect(database_dir / "opencode.db")
    connection.execute(
        "CREATE TABLE session (id TEXT, parent_id TEXT, title TEXT, directory TEXT, "
        "agent TEXT, model TEXT, time_created INTEGER, time_updated INTEGER)"
    )
    connection.execute(
        "CREATE TABLE message (id TEXT, session_id TEXT, time_created INTEGER, data TEXT)"
    )
    connection.execute(
        "CREATE TABLE part (id TEXT, message_id TEXT, time_created INTEGER, data TEXT)"
    )
    _insert(
        connection,
        "message",
        ("user-1", "main", 1, json.dumps({"role": "user", "time": {"created": 1}})),
    )
    _insert(
        connection,
        "part",
        ("part-u", "user-1", 1, json.dumps({"type": "text", "text": "task"})),
    )
    _insert(
        connection,
        "message",
        (
            "assistant-1",
            "main",
            2,
            json.dumps(
                {
                    "role": "assistant",
                    "parentID": "user-1",
                    "providerID": "gateway",
                    "modelID": "model",
                    "tokens": {"total": 10},
                }
            ),
        ),
    )
    _insert(
        connection,
        "part",
        (
            "part-a1",
            "assistant-1",
            2,
            json.dumps(
                {
                    "type": "tool",
                    "tool": "bash",
                    "state": {
                        "input": {"command": "echo $OPENAI_API_KEY"},
                        "output": "OPENAI_API_KEY=sk-super-secret-token",
                    },
                }
            ),
        ),
    )
    _insert(
        connection,
        "message",
        (
            "assistant-2",
            "main",
            3,
            json.dumps(
                {
                    "role": "assistant",
                    "parentID": "assistant-1",
                    "providerID": "gateway",
                    "modelID": "model",
                    "tokens": {"total": 5},
                }
            ),
        ),
    )
    _insert(
        connection,
        "session",
        ("main", None, "Primary", str(workspace), None, None, 1, 3),
    )
    _insert(
        connection,
        "session",
        ("child", "main", "Subagent", str(workspace), None, None, 4, 5),
    )
    _insert(
        connection,
        "part",
        (
            "part-a2",
            "assistant-2",
            3,
            json.dumps({"type": "text", "text": "final answer"}),
        ),
    )
    _insert(
        connection,
        "message",
        ("child-user", "child", 4, json.dumps({"role": "user"})),
    )
    _insert(
        connection,
        "part",
        ("part-cu", "child-user", 4, json.dumps({"type": "text", "text": "subtask"})),
    )
    _insert(
        connection,
        "message",
        (
            "child-assistant",
            "child",
            5,
            json.dumps(
                {
                    "role": "assistant",
                    "parentID": "child-user",
                    "providerID": "gateway",
                    "modelID": "model",
                }
            ),
        ),
    )
    _insert(
        connection,
        "part",
        (
            "part-ca",
            "child-assistant",
            5,
            json.dumps({"type": "text", "text": "subtask result"}),
        ),
    )
    connection.commit()
    connection.close()

    summary = export_model_io_trace(workspace)
    lines = (workspace / "_model_io.jsonl").read_text().splitlines()
    records = [json.loads(line) for line in lines]

    assert summary["model_step_count"] == 3
    assert summary["session_count"] == 2
    assert records[0]["record_type"] == "trajectory_manifest"
    steps = [record for record in records if record["record_type"] == "model_step"]
    assert steps[0]["input"]["new_context_refs_since_previous_step"] == [
        "input_message:user-1"
    ]
    assert steps[1]["input"]["new_context_refs_since_previous_step"] == [
        "model_step:1:output"
    ]
    assert steps[1]["output"]["parts"][0]["text"] == "final answer"
    child_step = next(step for step in steps if step["session_id"] == "child")
    assert child_step["parent_session_id"] == "main"
    assert child_step["input"]["context_refs"] == ["input_message:child-user"]
    assert child_step["input"]["new_context_refs_since_previous_step"] == [
        "input_message:child-user"
    ]
    serialized = (workspace / "_model_io.jsonl").read_text()
    assert "sk-super-secret-token" not in serialized
    assert "OPENAI_API_KEY=<redacted>" in serialized

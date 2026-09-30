import json
from pathlib import Path

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from evaluation.provenance.progress_snapshot import build_progress_snapshot, JsonlCursor
from evaluation.execution.usage_accounting import ingest_file


def test_status_never_initializes_or_mutates_database(tmp_path, monkeypatch):
    workspace = tmp_path / "run"
    workspace.mkdir()
    (workspace / "_meta.json").write_text('{"run_id":"run","status":"suspended_infrastructure"}')
    store = ExecutionStore(workspace, run_id="run")
    before = store.path.read_bytes()
    def fail(*args, **kwargs): raise AssertionError("read path must not migrate DB")
    monkeypatch.setattr(ExecutionStore, "_initialize", fail)
    result = build_progress_snapshot(workspace)
    assert result["run_status"] == "suspended_infrastructure"
    assert result["completion_percentage"] is None
    assert store.path.read_bytes() == before


def test_incremental_cursor_handles_partial_unicode_and_rotation(tmp_path):
    path = tmp_path / "log"
    path.write_bytes('甲\n乙'.encode())
    cursor = JsonlCursor()
    assert cursor.read(path) == ["甲"]
    with path.open("ab") as stream: stream.write(b"\n")
    assert cursor.read(path) == ["乙"]
    assert cursor.read(path) == []
    path.unlink()
    path.write_text("new\n")
    assert cursor.read(path) == ["new"]


def test_usage_identity_and_banner_are_distinct(tmp_path):
    store = ExecutionStore(tmp_path, run_id="usage")
    path = tmp_path / "stdout"
    path.write_text('Codex starting\n{"broken\n')
    value = ingest_file(store, path, session_id="s", kind="stdout")
    assert value["non_event_lines"] == 1 and value["malformed_events"] == 1
    native = tmp_path / "native.jsonl"
    event = {"type":"event_msg", "payload":{"type":"token_count", "info": {
        "request_id":"r1", "total_token_usage":{"input_tokens":10,"output_tokens":2}}}}
    native.write_text(json.dumps(event)+"\n"+json.dumps(event)+"\n")
    ingest_file(store, native, session_id="s")
    assert store.usage_details()["model_request_count"] == 1
    assert store.usage_details()["observable_model_steps"] == 1
    assert store.usage_details()["cached_input_tokens"] is None


def test_tool_calls_and_rounds_are_not_confused(tmp_path):
    (tmp_path / "_meta.json").write_text('{"run_id":"progress","status":"running"}')
    (tmp_path / "_tool_call_events.jsonl").write_text('\n'.join(json.dumps(e) for e in [
        {"sequence":1,"tool":"submit_native_job","phase":"started"},
        {"sequence":1,"tool":"submit_native_job","phase":"finished"},
        {"sequence":2,"tool":"wait_execution_jobs","phase":"started"}])+"\n")
    result = build_progress_snapshot(tmp_path)
    assert result["tool_call_count"] == 2
    assert result["tool_round_count"] is None
    assert result["phase"] == "waiting_for_compute"


def test_suspended_run_is_not_shown_as_live_wait_and_old_heartbeat_is_visible(tmp_path):
    from evaluation.provenance.evidence_archive import audit_directory
    root = audit_directory(tmp_path)
    root.mkdir(parents=True)
    (root / "progress.json").write_text('{"controller_observed_at":"2020-01-01T00:00:00+00:00"}')
    (tmp_path / "_meta.json").write_text('{"status":"running"}')
    (tmp_path / "_tool_call_events.jsonl").write_text('{"sequence":1,"tool":"wait_execution_jobs","phase":"started"}\n')
    assert "controller_heartbeat_old" in build_progress_snapshot(tmp_path)["stale_reasons"]
    (tmp_path / "_meta.json").write_text('{"status":"suspended_infrastructure"}')
    assert build_progress_snapshot(tmp_path)["phase"] == "suspended_infrastructure"


def test_cursor_limits_work_per_poll_without_losing_large_records(tmp_path):
    path = tmp_path / "events"
    path.write_bytes(b"x" * 100 + b"\nnext\n")
    cursor = JsonlCursor()
    assert cursor.read(path, max_bytes=40) == []
    assert cursor.offset == 40
    assert cursor.read(path, max_bytes=40) == []
    assert cursor.read(path, max_bytes=40) == ["x" * 100, "next"]


def test_finalized_elapsed_time_does_not_grow_after_completion(tmp_path):
    (tmp_path / "_meta.json").write_text(json.dumps({"status":"completed", "recovery_enabled":True,
        "first_started_at":"2020-01-01T00:00:00+00:00", "deadline_at":"2020-01-01T00:10:00+00:00", "run_elapsed_seconds":45}))
    progress = build_progress_snapshot(tmp_path)
    assert progress["elapsed_seconds"] == 45
    assert progress["remaining_seconds"] == 555
    assert progress["time_basis"] == "finalization"


def test_web_progress_and_finished_stream_are_read_only_and_drain_large_logs(tmp_path, monkeypatch):
    from evaluation.web import server
    (tmp_path / "_meta.json").write_text('{"run_id":"web","status":"timeout"}')
    (tmp_path / "_agent_output.jsonl").write_text(('x' * 1024 + '\n') * 1100 + 'final-event\n')
    monkeypatch.setattr(server, "get_run_workspace", lambda run_id: tmp_path)
    def fail(*args, **kwargs): raise AssertionError("read-only Web access must not start a process or initialize a database")
    monkeypatch.setattr(ExecutionStore, "_initialize", fail)
    monkeypatch.setattr("subprocess.Popen", fail)
    client = server.app.test_client()
    response = client.get('/api/runs/web/progress')
    assert response.status_code == 200 and response.json["run_status"] == "timeout"
    response = client.get('/api/runs/web/stream')
    assert 'final-event' in response.text
    assert '"status": "timeout"' in response.text

import json
from types import SimpleNamespace

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from evaluation.execution.usage_accounting import ingest_file, record_turn, refresh_usage


def token(input_tokens=10, output_tokens=3, **extra):
    return {"type":"event_msg","timestamp":"2026-09-16T01:00:00Z","payload":{"type":"token_count", "info":{
        "total_token_usage":{"input_tokens":input_tokens,"output_tokens":output_tokens,"cached_input_tokens":8,
                             "reasoning_output_tokens":2, **extra}}}}


def append(path, event):
    with path.open("a") as f:f.write(json.dumps(event)+"\n")


def test_missing_provider_counter_is_unknown_not_invented_zero(tmp_path):
    store = ExecutionStore(tmp_path, run_id="partial")
    record_turn(store, "session", "turn", {"usage":{"input_tokens":12}})
    details = store.usage_details()
    assert details["input_tokens"] == 12
    assert details["output_tokens"] is None and details["total_tokens"] is None
    assert details["accounting_status"] == "partial"
    assert store.usage() == {"input_tokens":12, "output_tokens":0, "turns":1}


def test_live_long_turn_duplicate_cancel_and_resume_share_counters(tmp_path):
    store=ExecutionStore(tmp_path,run_id="usage")
    p=store.directory / "codex" / "sessions" / "rollout-s.jsonl";p.parent.mkdir(parents=True)
    append(p, token())
    runner=SimpleNamespace(workspace=tmp_path,run_id="usage",_resume_session_id="s")
    refresh_usage(runner,force=True)
    assert store.usage()=={"input_tokens":10,"output_tokens":3,"turns":0}
    append(p,token(100,8,cached_input_tokens=80))
    # Even an overlapping/cumulative stdout summary cannot double native usage.
    record_turn(store,"s","t1",{"usage":{"input_tokens":100,"output_tokens":8}})
    record_turn(store,"s","t2",{"usage":{"input_tokens":100,"output_tokens":8}})
    refresh_usage(runner,force=True)
    refresh_usage(runner,force=True)
    assert store.usage()=={"input_tokens":100,"output_tokens":8,"turns":2}
    detail=store.usage_details()
    assert detail["cached_input_tokens"]==80 and detail["total_tokens"]==108
    assert detail["reasoning_output_tokens"]==2 and detail["cache_write_input_tokens"] is None


def test_incomplete_lines_replayed_without_loss_or_double_count(tmp_path):
    store=ExecutionStore(tmp_path,run_id="usage");p=tmp_path/"s.jsonl"
    p.write_text(json.dumps(token())[:50])
    ingest_file(store,p,session_id="s")
    assert store.usage_details()["accounting_status"]=="partial"
    with p.open("a") as f:f.write(json.dumps(token())[50:]+"\n")
    ingest_file(store,p,session_id="s")
    assert store.usage()["input_tokens"]==10
    append(p,token())
    ingest_file(store,p,session_id="s")
    assert store.usage()["input_tokens"]==10


def test_reset_needs_explicit_epoch_and_rotation_does_not_add(tmp_path):
    store=ExecutionStore(tmp_path,run_id="usage");p=tmp_path/"s.jsonl"
    append(p,token(100,10));ingest_file(store,p,session_id="s")
    append(p,token(2,1));ingest_file(store,p,session_id="s")
    assert store.usage()["input_tokens"]==100
    assert store.usage_details()["accounting_status"]=="partial"
    event=token(2,1);event["payload"]["info"]["counter_epoch"]="explicit-new-epoch"
    append(p,event);ingest_file(store,p,session_id="s")
    assert store.usage()["input_tokens"]==102
    q=tmp_path/"copy.jsonl";q.write_bytes(p.read_bytes());ingest_file(store,q,session_id="s")
    assert store.usage()["input_tokens"]==102
    p.write_text(json.dumps(token(1,1))+"\n");ingest_file(store,p,session_id="s")
    assert store.usage()["input_tokens"]==102


def test_multiple_sessions_and_mismatched_identity(tmp_path):
    store=ExecutionStore(tmp_path,run_id="usage")
    for s in ("s1","s2"):
        p=tmp_path/(s+".jsonl");append(p,token());ingest_file(store,p,session_id=s)
    assert store.usage()["input_tokens"]==20
    p=tmp_path/"wrong.jsonl"
    append(p,{"type":"session_meta","payload":{"id":"unrelated"}});append(p,token(10000))
    ingest_file(store,p,session_id="s3")
    ingest_file(store,p,session_id="s3")
    assert store.usage()["input_tokens"]==20
    assert store.usage_details()["accounting_status"]=="partial"


def test_stdout_cursor_replays_stable_turn_identity(tmp_path):
    store=ExecutionStore(tmp_path,run_id="usage");p=tmp_path/"agent.jsonl"
    append(p,{"type":"turn.completed","usage":{"input_tokens":5,"output_tokens":2}})
    for _ in range(3):ingest_file(store,p,session_id="s",kind="stdout",attempt_id="a1")
    assert store.usage()=={"input_tokens":5,"output_tokens":2,"turns":1}
    assert store.usage_details()["cached_input_tokens"] is None


def test_large_incomplete_line_has_bounded_incremental_skip(tmp_path):
    store = ExecutionStore(tmp_path, run_id="usage")
    path = tmp_path / "s.jsonl"
    budget = 2 * 1024 * 1024
    path.write_bytes(b"x" * (budget * 3 + 100))
    previous = 0
    for _ in range(4):
        value = ingest_file(store, path, session_id="s", max_bytes=budget)
        assert 0 < value["offset"] - previous <= budget
        previous = value["offset"]
    assert value["skipping_oversize"] and value["oversize_events"] == 1
    with path.open("ab") as handle:
        handle.write(b"\n" + json.dumps(token(321, 12)).encode() + b"\n")
    value = ingest_file(store, path, session_id="s", max_bytes=budget)
    assert not value["skipping_oversize"]
    assert store.usage()["input_tokens"] == 321
    assert store.usage_details()["accounting_status"] == "partial"


def test_usage_report_does_not_invent_first_step_or_cache_counts(tmp_path):
    from evaluation.provenance.token_usage import workspace_token_usage, compare_token_usage, _markdown
    (tmp_path / "_meta.json").write_text(json.dumps({"recovery_enabled": True, "run_id": "usage"}))
    store = ExecutionStore(tmp_path, run_id="usage")
    record_turn(store, "s", "t", {"usage": {"input_tokens": 5, "output_tokens": 2}})
    view = workspace_token_usage(tmp_path)
    assert view["first_model_step_tokens"]["total"] is None
    assert view["tokens"]["cache_read"] is None and view["model_step_count"] is None
    assert "First model step total | unavailable | unavailable" in _markdown(compare_token_usage(tmp_path, tmp_path))


def test_legacy_usage_preserves_unknowns_and_does_not_double_count_reasoning(tmp_path):
    import sqlite3
    from evaluation.provenance.token_usage import workspace_token_usage
    (tmp_path / "_opencode").mkdir()
    with sqlite3.connect(tmp_path / "_opencode/opencode.db") as connection:
        connection.execute("CREATE TABLE message(id TEXT, session_id TEXT, time_created INTEGER, data TEXT)")
        connection.execute("INSERT INTO message VALUES(?,?,?,?)", ("a", "session", 1, json.dumps({"role": "assistant", "tokens": {
            "total": 125, "input": 70, "output": 25, "reasoning": 10, "cache": {"read": 30, "write": 0}}})))
    first = workspace_token_usage(tmp_path)
    assert first["tokens"] == {"total": 125, "input": 100, "output": 25, "reasoning": 10, "cache_read": 30, "cache_write": 0}
    with sqlite3.connect(tmp_path / "_opencode/opencode.db") as connection:
        connection.execute("INSERT INTO message VALUES(?,?,?,?)", ("b", "session", 2, json.dumps({"role": "assistant", "tokens": {"output": 5}})))
    second = workspace_token_usage(tmp_path)
    assert second["tokens"]["total"] is None and second["tokens"]["input"] is None
    assert second["tokens"]["cache_read"] is None and second["tokens"]["output"] == 30
    assert second["usage_details"]["accounting_status"] == "partial"

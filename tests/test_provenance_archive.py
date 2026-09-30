from __future__ import annotations

import json
import sqlite3
import shutil

from chemistry_toolbox.mcp.execution_store import ExecutionStore

from evaluation.provenance.results import build_workspace_results
from evaluation.provenance.token_usage import workspace_token_usage


def test_portable_archive_replay_reads_control_db_without_creating_runtime_state(tmp_path):
    archive = tmp_path / "archive"
    workspace = archive / "workspace"
    control = archive / "control"
    workspace.mkdir(parents=True)
    control.mkdir()
    (workspace / "_meta.json").write_text(
        json.dumps({"run_id": "archive-run", "paper_id": "paper", "task_type": "autonomous_research"})
    )
    (workspace / "_tool_trace.jsonl").write_text("\n")
    database = control / "execution.sqlite3"
    connection = sqlite3.connect(database)
    connection.execute("CREATE TABLE records (namespace TEXT NOT NULL, key TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(namespace, key))")
    connection.execute(
        "INSERT INTO records VALUES (?, ?, ?)",
        ("usage", "session:1", json.dumps({"session_id": "session", "input_tokens": 12, "output_tokens": 3, "turns": 1})),
    )
    connection.commit()
    connection.close()

    usage = workspace_token_usage(workspace)
    result = build_workspace_results(workspace)

    assert usage["source"] == "portable_control_archive"
    assert usage["tokens"]["total"] == 15
    assert result["tokens"]["agent"]["tokens"]["total"] == 15
    assert not (workspace / ".rcb_recovery").exists()
    assert not (archive / ".rcb_recovery").exists()
    assert usage['tokens']['cache_read'] is None


def test_portable_usage_matches_live_native_counters_and_preserves_missing_fields(tmp_path):
    workspace = tmp_path / 'live'
    workspace.mkdir()
    (workspace / '_meta.json').write_text(json.dumps({'run_id': 'usage-test', 'recovery_enabled': True}))
    store = ExecutionStore(workspace, run_id='usage-test')
    store.put_record('usage', 'session:1', {'session_id': 'session', 'input_tokens': 100, 'output_tokens': 20, 'turns': 1})
    store.put_record('usage_stream', 'native', {
        'kind': 'native', 'session_id': 'session',
        'segments': {'0': {'input_tokens': 100, 'output_tokens': 20, 'cached_input_tokens': 60, 'reasoning_output_tokens': 10}},
    })
    archive = tmp_path / 'portable'
    shutil.copytree(workspace, archive / 'workspace')
    (archive / 'control').mkdir()
    shutil.copyfile(store.path, archive / 'control/execution.sqlite3')
    before = {p: p.read_bytes() for p in archive.rglob('*') if p.is_file()}
    live = workspace_token_usage(workspace)
    portable = workspace_token_usage(archive / 'workspace')
    assert portable['usage_details'] == live['usage_details']
    assert portable['tokens'] == {'input': 100, 'output': 20, 'total': 120, 'cache_read': 60, 'reasoning': 10, 'cache_write': None}
    assert before == {p: p.read_bytes() for p in archive.rglob('*') if p.is_file()}
    assert not (archive / '.rcb_recovery').exists()

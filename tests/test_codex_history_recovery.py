"""Encrypted-history recovery uses real files and isolated provider processes."""
import json
import os
from pathlib import Path
import signal
import sqlite3
import sys
from types import SimpleNamespace
import uuid

import pytest

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.recovery_io import process_identity
from evaluation.execution.codex_history import (
    activate_plaintext_fallback, copy_plaintext_history, session_home, session_rollout,
)
from evaluation.execution.provider_errors import is_encrypted_history_error, normalize_error
from evaluation.execution.recovery import ControllerLock, RunRecoveryError, runner_store, validate_session
from evaluation.execution.runner import TaskRunner
from evaluation.execution.usage_accounting import refresh_usage
from evaluation.provenance.progress_snapshot import build_progress_snapshot, format_progress_summary
from evaluation.provenance.results import build_workspace_results
from test_task_package_v19 import package
from test_usage_accounting import token


def seed_history(home, workspace, session=None):
    session = session or str(uuid.uuid4())
    path = home / 'sessions/2026/09/18' / f'rollout-{session}.jsonl'
    path.parent.mkdir(parents=True)
    events = [
        {'type': 'session_meta', 'payload': {'id': session, 'cwd': str(workspace.resolve())}},
        {'type': 'response_item', 'payload': {'type': 'message', 'role': 'user', 'content': 'Continue research.'}},
        {'type': 'response_item', 'payload': {'type': 'reasoning', 'id': 'rs_old', 'encrypted_content': 'opaque'}},
        {'type': 'response_item', 'payload': {'type': 'reasoning', 'summary': ['Visible summary']}},
        {'type': 'response_item', 'payload': {'type': 'function_call', 'call_id': 'call_saved', 'name': 'submit_job', 'arguments': '{}'}},
        {'type': 'response_item', 'payload': {'type': 'function_call_output', 'call_id': 'call_saved',
            'output': '{"job_id":"job_saved","receipt":"receipt_saved","encrypted_content":"literal tool text"}'}},
        token(100, 20, cached_input_tokens=80),
    ]
    path.write_bytes(b''.join(json.dumps(e, ensure_ascii=False).encode() + b'\n' for e in events))
    with sqlite3.connect(home / 'state_5.sqlite') as db:
        db.execute('CREATE TABLE threads(id TEXT PRIMARY KEY, rollout_path TEXT, cwd TEXT)')
        db.execute('INSERT INTO threads VALUES(?,?,?)', (session, str(path), str(workspace.resolve())))
    return session, path


@pytest.mark.parametrize('value', [
    {'error': {'code': 'invalid_encrypted_content', 'message': 'Cannot replay reasoning'}},
    {'message': 'stream disconnected before completion: Encrypted content could not be decrypted or parsed.'},
    {'message': 'stream disconnected: The encrypted content for item rs_123 could not be verified.'},
])
def test_replay_error_is_not_a_network_retry(value):
    error = normalize_error(value, source='agent')
    assert error['category'] == 'configuration' and not error['retryable']
    assert is_encrypted_history_error(error)
    assert 'http_status' not in error
    if 'error' not in value:
        assert error['code'] is None


@pytest.mark.parametrize('value', [
    {'message': 'stream disconnected before completion'},
    {'message': 'tool log mentions encrypted_content'},
    {'status_code': 401, 'message': 'invalid_encrypted_content'},
    {'error': {'code': 'insufficient_quota', 'message': 'invalid_encrypted_content'}},
])
def test_unrelated_or_auth_failure_never_triggers_plaintext(value):
    assert not is_encrypted_history_error(normalize_error(value, source='agent'))


def test_copy_preserves_original_and_all_non_reasoning_bytes(tmp_path):
    source, dest = tmp_path / 'codex', tmp_path / 'copy'
    session, original = seed_history(source, tmp_path)
    before = original.read_bytes()
    db_before = (source / 'state_5.sqlite').read_bytes()
    (source / 'history.sqlite').write_text('stale projection must not be copied')
    record = copy_plaintext_history(source, dest, session, tmp_path)
    copied = session_rollout(dest, session, tmp_path)
    assert original.read_bytes() == before and (source / 'state_5.sqlite').read_bytes() == db_before
    assert copied.read_bytes() == b''.join(line for line in before.splitlines(keepends=True) if b'rs_old' not in line)
    assert record['removed_reasoning_count'] == 1 and record['tool_history_preserved']
    assert not (dest / 'history.sqlite').exists()
    assert dest.stat().st_mode & 0o777 == 0o700
    with sqlite3.connect(dest / 'state_5.sqlite') as db:
        assert db.execute('SELECT rollout_path FROM threads WHERE id=?', (session,)).fetchone()[0] == str(copied)
    # Retry publication after a crash is safe only while this copy is unused.
    assert copy_plaintext_history(source, dest, session, tmp_path) == record
    with copied.open('a') as stream:
        stream.write('{}\n')
    with pytest.raises(RunRecoveryError, match='already_modified'):
        copy_plaintext_history(source, dest, session, tmp_path)


@pytest.mark.parametrize('extra,reason', [
    (b'{broken}\n', 'malformed_record'), (b'{}', 'malformed_record'),
    (b'{"type":"compacted","payload":{"replacement_history":[{"encrypted_content":"opaque"}]}}\n', 'unsupported_encrypted_record'),
    (b'{"type":"response_item","payload":{"type":"function_call_output","encrypted_content":"opaque"}}\n', 'unsupported_encrypted_record'),
])
def test_invalid_or_unsupported_record_leaves_source_unchanged(tmp_path, extra, reason):
    source, dest = tmp_path / 'codex', tmp_path / 'copy'
    session, original = seed_history(source, tmp_path)
    with original.open('ab') as stream:
        stream.write(extra)
    before = original.read_bytes()
    with pytest.raises(RunRecoveryError, match=reason):
        copy_plaintext_history(source, dest, session, tmp_path)
    assert original.read_bytes() == before and not dest.exists()
    assert not list(tmp_path.glob('.codex_plaintext-*.tmp'))


@pytest.mark.parametrize('problem,reason', [
    ('cwd', 'cwd_mismatch'), ('db_identity', 'state_db_identity_mismatch'),
    ('source_change', 'source_changed'), ('no_cipher', 'no_encrypted_reasoning'),
    ('ambiguous', 'ambiguous'), ('db_missing', 'state_db_missing'),
    ('child_thread', 'multiple_threads_unsupported'),
])
def test_copy_rejects_unverifiable_history(tmp_path, monkeypatch, problem, reason):
    import evaluation.execution.codex_history as history
    source, dest = tmp_path / 'codex', tmp_path / 'copy'
    session, original = seed_history(source, tmp_path)
    if problem == 'cwd':
        lines = original.read_text().splitlines()
        lines[0] = json.dumps({'type': 'session_meta', 'payload': {'id': session, 'cwd': '/wrong'}})
        original.write_text('\n'.join(lines) + '\n')
    elif problem == 'db_identity':
        with sqlite3.connect(source / 'state_5.sqlite') as db:
            db.execute('UPDATE threads SET cwd=?', ('/wrong',))
    elif problem == 'source_change':
        real = history.file_hash
        count = 0
        def changed(path):
            nonlocal count
            count += 1
            return real(path) if count == 1 else 'concurrently-changed'
        monkeypatch.setattr(history, 'file_hash', changed)
    elif problem == 'no_cipher':
        original.write_bytes(b''.join(line for line in original.read_bytes().splitlines(keepends=True) if b'rs_old' not in line))
    elif problem == 'ambiguous':
        (original.parent / f'duplicate-{session}.jsonl').write_bytes(original.read_bytes())
    elif problem == 'db_missing':
        (source / 'state_5.sqlite').unlink()
    elif problem == 'child_thread':
        with sqlite3.connect(source / 'state_5.sqlite') as db:
            db.execute('INSERT INTO threads VALUES(?,?,?)', (str(uuid.uuid4()), '/child/rollout.jsonl', str(tmp_path)))
    before = original.read_bytes()
    with pytest.raises(RunRecoveryError, match=reason):
        copy_plaintext_history(source, dest, session, tmp_path)
    assert original.read_bytes() == before and not dest.exists()


@pytest.fixture
def codex_runner(tmp_path, monkeypatch):
    script = tmp_path / 'fixture_codex'
    script.write_text(f'#!{sys.executable}\n' + '''import json, os, sys
from pathlib import Path
if '--version' in sys.argv:
    print('codex-cli 0.155.0 fixture')
    sys.exit(0)
from chemistry_toolbox.mcp.execution_store import ExecutionStore
workspace = Path.cwd()
store = ExecutionStore(workspace, run_id=workspace.name)
session = sys.argv[sys.argv.index('resume') + 1]
home = Path(os.environ['CODEX_HOME'])
path = next((home/'sessions').rglob('*' + session + '.jsonl'))
events = [json.loads(line) for line in path.read_text().splitlines()]
assert events[0]['payload']['id'] == session
assert events[0]['payload']['cwd'] == str(workspace)
n = store.get_record('test', 'calls', 0) + 1
store.put_record('test', 'calls', n)
store.put_record('test_prompt', str(n), sys.argv[-1])
print(json.dumps({'type':'thread.started','thread_id':session}), flush=True)
mode = store.get_record('test', 'mode', '')
encrypted = any(e.get('payload', {}).get('encrypted_content') for e in events)
if mode != 'accept_native' and (encrypted or mode == 'reject_always'):
    print(json.dumps({'type':'turn.failed','error':{'message':'stream disconnected before completion: Encrypted content could not be decrypted or parsed.'}}), flush=True)
    sys.exit(1)
with path.open('a') as stream:
    stream.write(json.dumps({'type':'response_item','payload':{'type':'reasoning','id':'rs_new','encrypted_content':'new-valid-cipher'}}) + '\\n')
    stream.write(json.dumps({'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'input_tokens':120,'output_tokens':25,'cached_input_tokens':90}}}}) + '\\n')
if mode == 'pause_after_copy':
    store.put_record('control','current',{'command':'pause'})
    sys.exit(1)
(workspace/'report/report.md').write_text('Fixture computation report')
(workspace/'report/results.json').write_text('{"barrier":12.3,"conclusion":"path A"}')
print(json.dumps({'type':'turn.completed','turn_id':'final','usage':{'input_tokens':120,'output_tokens':25}}), flush=True)
''')
    script.chmod(0o755)
    monkeypatch.setenv('RCB_CODEX_EXECUTABLE', str(script))
    monkeypatch.setenv('RCB_CODEX_BASE_URL', 'http://unused.invalid/v1')
    values = []
    def create(paper='paper_fixture', task_type='autonomous_research', resume=True):
        root = tmp_path / paper / 'tasks'
        package(root, paper_id=paper, task_type=task_type)
        runner = TaskRunner(paper, task_type=task_type, task_roots=[str(root)], workspace_root=tmp_path / paper / 'runs',
                            agent_key='codex', recovery_enabled=True, resume=resume, timeout_seconds=300,
                            available_cpu_cores=1, available_memory_mb=512, live_progress=False,
                            resume_policy={'max_attempts': 3})
        runner.setup_workspace()
        store = runner_store(runner)
        runner._resume_session_id, _ = seed_history(session_home(store), runner.workspace)
        runner._persist_run_manifest(run_state='suspended_infrastructure')
        runner = TaskRunner.restore(runner.run_id, runner.workspace.parent)
        values.append(runner)
        return runner
    yield create
    for runner in values:
        if runner._controller_lock:
            runner._controller_lock.release()
        owner = runner_store(runner).get_record('manager', 'identity', {})
        if process_identity(owner.get('pid'), owner).get('verified'):
            try:
                os.kill(owner['pid'], signal.SIGTERM)
            except ProcessLookupError:
                pass


@pytest.mark.parametrize('paper,task_type', [('paper_fixture', 'autonomous_research'), ('paper_other', 'paper_reproduction')])
def test_controller_fallback_keeps_session_jobs_budget_usage_and_marks_results(codex_runner, paper, task_type):
    runner = codex_runner(paper, task_type)
    store = runner_store(runner)
    original = session_rollout(session_home(store), runner._resume_session_id, runner.workspace)
    before = original.read_bytes()
    manifest = store.get_record('run', 'manifest')
    receipt = store.accept_submission(submission_key='saved', entity_type='job', request={}, spec={})
    store.record_job_state(receipt.entity_id, 'queued')
    store.record_job_state(receipt.entity_id, 'success')
    store.put_record('result', receipt.entity_id, {'result_state': 'ready', 'result_receipt_id': 'saved-result'})
    result = runner.run()
    assert result['status'] == 'completed', result.get('error')
    assert original.read_bytes() == before
    assert store.get_submission('saved')['receipt_id'] == receipt.receipt_id and len(store.list_jobs()) == 1
    assert store.get_record('result', receipt.entity_id)['result_receipt_id'] == 'saved-result'
    saved = store.get_record('run', 'manifest')
    assert (saved['provider_session_id'], saved['config_hash'], saved['deadline_at']) == (manifest['provider_session_id'], manifest['config_hash'], manifest['deadline_at'])
    attempts = list(store.records('attempt').values())
    assert [a['start_reason'] for a in attempts] == ['manual_resume', 'plaintext_history_resume']
    assert [a['recovery_mode'] for a in attempts] == ['native', 'plaintext_history']
    assert attempts[0]['error']['category'] == 'configuration'
    assert store.get_record('resume', 'state')['automatic_attempts'] == 1
    assert store.usage() == {'input_tokens': 120, 'output_tokens': 25, 'turns': 1}
    assert store.usage_details()['cached_input_tokens'] == 90
    assert 'internal reasoning was removed' in store.get_record('test_prompt', '2')
    snapshot = build_progress_snapshot(runner.workspace)
    assert 'mode=plaintext_history' in format_progress_summary(snapshot)
    for record in (result, saved, snapshot, build_workspace_results(runner.workspace)['run']):
        assert record['recovery_mode'] == 'plaintext_history'
        assert record['history_recovery']['source_attempt_id'] == 'attempt_0001'
        assert record['history_recovery']['removed_reasoning_count'] == 1
    from evaluation.provenance.evidence_archive import export_run_archive
    archive = runner.workspace.parent / 'export'
    export_run_archive(runner.workspace, archive)
    archived = json.loads((archive / 'workspace/_meta.json').read_text())
    assert archived['history_recovery'] == result['history_recovery']


@pytest.mark.parametrize('mode,resume,count,status', [
    ('accept_native', True, 1, 'completed'), ('', False, 1, 'suspended_infrastructure'),
    ('reject_always', True, 2, 'suspended_infrastructure'),
])
def test_normal_resume_disable_and_second_failure(codex_runner, mode, resume, count, status):
    runner = codex_runner(resume=resume)
    store = runner_store(runner)
    store.put_record('test', 'mode', mode)
    assert runner.run()['status'] == status
    assert store.get_record('test', 'calls') == count
    if mode == 'reject_always':
        assert store.get_record('history_recovery', 'error')['message'] == 'plaintext_history_fallback_already_used'
    else:
        assert not store.get_record('history_recovery', 'active')
        assert not (store.directory / 'codex_plaintext').exists()


def test_later_restore_uses_copy_and_preserves_new_reasoning(codex_runner):
    runner = codex_runner()
    store = runner_store(runner)
    store.put_record('test', 'mode', 'pause_after_copy')
    assert runner.run()['status'] == 'suspended_infrastructure'
    copied = session_rollout(session_home(store), runner._resume_session_id, runner.workspace)
    assert b'new-valid-cipher' in copied.read_bytes()
    store.put_record('test', 'mode', 'accept_native')
    restored = TaskRunner.restore(runner.run_id, runner.workspace.parent)
    assert restored._agent_environment()['CODEX_HOME'] == str(store.directory / 'codex_plaintext')
    validate_session(restored)
    assert restored.run()['status'] == 'completed'
    assert b'new-valid-cipher' in copied.read_bytes()
    assert store.get_record('resume', 'state')['automatic_attempts'] == 1
    assert len(store.records('attempt')) == 3
    assert store.usage()['input_tokens'] == 120


def test_incomplete_active_copy_does_not_revert_to_original(codex_runner):
    runner = codex_runner()
    store = runner_store(runner)
    store.put_record('history_recovery', 'active', {'mode': 'plaintext_history',
                     'session_store_path': str(store.directory / 'codex_plaintext')})
    with pytest.raises(RunRecoveryError, match='store_invalid'):
        runner._agent_environment()
    with pytest.raises(RunRecoveryError, match='store_invalid'):
        validate_session(runner)
    assert build_workspace_results(runner.workspace)['run']['recovery_mode'] == 'plaintext_history'
    assert not (store.directory / 'codex_plaintext').exists()


def test_failed_copy_records_reason_without_a_retry(codex_runner):
    runner = codex_runner()
    store = runner_store(runner)
    (session_home(store) / 'state_5.sqlite').unlink()
    result = runner.run()
    assert result['status'] == 'suspended_infrastructure'
    assert result['error']['category'] == 'configuration'
    assert result['history_recovery_error']['message'] == 'history_recovery_state_db_missing'
    assert not store.get_record('history_recovery', 'active')
    assert store.get_record('test', 'calls') == 1


@pytest.mark.parametrize('stop,reason', [
    ('pause', 'control_stopped'), ('cancel', 'control_stopped'), ('tokens', 'budget_exhausted'),
    ('turns', 'budget_exhausted'), ('deadline', 'deadline_expired'), ('attempts', 'attempt_limit'),
    ('lock', 'requires_controller_lock'), ('alive', 'agent_not_stopped'),
])
def test_fallback_honors_existing_controller_guards(tmp_path, stop, reason):
    store = ExecutionStore(tmp_path, run_id='guard')
    session, path = seed_history(session_home(store), tmp_path)
    before = path.read_bytes()
    def deadline():
        if stop == 'deadline':
            raise RunRecoveryError('run_deadline_expired')
        return 100
    with ControllerLock(store.directory / 'controller.lock') as lock:
        runner = SimpleNamespace(workspace=tmp_path, run_id='guard', agent={'kind': 'codex'},
                                 _controller_lock=None if stop == 'lock' else lock, _stop_requested=False,
                                 remaining_run_timeout_seconds=deadline, max_turns=1, max_tokens=1,
                                 _resume_session_id=session, attempt_id='attempt_0001')
        if stop in {'pause', 'cancel'}:
            store.put_record('control', 'current', {'command': stop})
        if stop == 'tokens':
            refresh_usage(runner, force=True)
        if stop == 'turns':
            store.put_record('usage', 't', {'session_id': session, 'turns': 1, 'input_tokens': 0, 'output_tokens': 0})
        if stop == 'alive':
            store.put_record('agent', 'identity', process_identity(os.getpid()))
        state = {'automatic_attempts': 1 if stop == 'attempts' else 0}
        with pytest.raises(RunRecoveryError, match=reason):
            activate_plaintext_fallback(runner, normalize_error({'message': 'invalid_encrypted_content'}, source='agent'),
                                        {'enabled': True, 'limits': {'max_attempts': 1}}, state)
    assert path.read_bytes() == before and not store.get_record('history_recovery', 'active')
    assert not (store.directory / 'codex_plaintext').exists()

"""Fault injection across processes; no provider API or chemistry workload."""
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from chemistry_toolbox.src.recovery_io import process_identity, atomic_json
from evaluation.execution.provider_errors import normalize_error, ProviderFailure
from evaluation.execution.recovery import runner_store, RunRecoveryError, canonical_config_hash
from evaluation.execution.resume_policy import configure, retry_delay, execution_exit_code
from evaluation.execution.runner import TaskRunner
from evaluation.provenance.progress_snapshot import build_progress_snapshot, batch_is_active
from test_task_package_v19 import package


@pytest.mark.parametrize('value,category,retry', [
    ({'error': {'code': 'insufficient_quota', 'message': 'rate limit exceeded'}, 'status_code': 429}, 'quota', False),
    ({'message': 'rate limit exceeded'}, 'rate_limit', True),
    ({'status_code': 429}, 'unknown_provider_failure', False),
    ({'status_code': 401}, 'authentication', False),
    ({'status_code': 503}, 'service_unavailable', True),
    ({'error': {'code': 'context_length_exceeded'}}, 'context_length', False),
    ({'message': 'model_not_found'}, 'configuration', False),
    (ConnectionError('lost'), 'network', True),
    ('unexpected exit', 'unknown_provider_failure', False),
])
def test_error_classification(value, category, retry):
    error = normalize_error(value, source='test')
    assert error['category'] == category and error['retryable'] == retry
    if not isinstance(value, dict) or 'status_code' not in value:
        assert 'http_status' not in error


def test_error_evidence_redaction_and_warning_not_terminal(monkeypatch):
    monkeypatch.setenv('JUDGE_API_KEY', 'fixture-secret-long')
    f = ProviderFailure()
    f.observe({'type': 'error', 'message': 'rate limit exceeded fixture-secret-long sk-fakevalue'}, 'line1')
    assert f.final is None
    f.observe({'type': 'turn.failed', 'error': {'message': 'rate limit exceeded'}}, 'line2')
    result = f.failure(1)
    assert result['occurrences'] == 2 and result['event_ref'] == 'line2'
    assert result['first_event_ref'] == 'line1'
    assert 'secret' not in json.dumps(result)
    e = normalize_error({'status_code': 429, 'message': 'rate limit exceeded', 'headers': {'Retry-After': '12', 'X-Request-ID': 'req-1'}}, source='test')
    assert e['retry_after_seconds'] == 12 and e['request_id'] == 'req-1'


@pytest.fixture
def make_runner(tmp_path, monkeypatch):
    values = []
    script = tmp_path / 'provider.py'
    script.write_text('''import json, sys, uuid
from pathlib import Path
from chemistry_toolbox.mcp.execution_store import ExecutionStore
workspace = Path(sys.argv[1])
store = ExecutionStore(workspace, run_id=workspace.name)
m = store.get_record('run', 'manifest')
session = m.get('provider_session_id') or str(uuid.uuid4())
store.put_record('mock_session', session, {'cwd': str(workspace)}, immutable=True)
print(json.dumps({'type':'thread.started','thread_id':session}), flush=True)
n = store.get_record('test', 'calls', 0) + 1
store.put_record('test', 'calls', n)
count = store.get_record('test', 'failures', 2)
if n <= count:
    print(json.dumps({'type':'error','message':'Reconnecting: rate limit exceeded'}), flush=True)
    print(json.dumps({'type':'turn.failed','error':{'message':'rate limit exceeded'}}), flush=True)
    sys.exit(1)
(workspace/'report/report.md').write_text('Fixture computation report')
(workspace/'report/results.json').write_text('{"barrier":12.3,"conclusion":"path A"}')
print(json.dumps({'type':'turn.completed','turn_id':'final','usage':{'input_tokens':7,'output_tokens':3}}), flush=True)
''')
    monkeypatch.setattr(TaskRunner, 'build_agent_argv', lambda self: [sys.executable, str(script), str(self.workspace)])
    def create(paper='paper_fixture', resume=True):
        root = tmp_path / paper / 'tasks'
        task_type = 'paper_reproduction' if paper == 'paper_other' else 'autonomous_research'
        package(root, paper_id=paper, task_type=task_type)
        r = TaskRunner(paper, task_type=task_type, task_roots=[str(root)], workspace_root=tmp_path / paper / 'runs', agent_key='mock',
                       recovery_enabled=True, resume=resume, timeout_seconds=90, live_progress=False,
                       available_cpu_cores=1, available_memory_mb=512,
                       resume_policy={'initial_delay_seconds': .12, 'max_delay_seconds': .2, 'max_wait_seconds': 5, 'max_attempts': 3})
        r.setup_workspace()
        values.append(r)
        return r
    yield create
    for r in values:
        if r._controller_lock:
            r._controller_lock.release()
        owner = runner_store(r).get_record('manager', 'identity', {})
        if process_identity(owner.get('pid'), owner).get('verified'):
            try: os.kill(owner['pid'], signal.SIGTERM)
            except ProcessLookupError: pass


@pytest.mark.parametrize('paper', ['paper_fixture', 'paper_other'])
def test_transient_recovery_reuses_session_receipts_and_budget(make_runner, monkeypatch, paper):
    from evaluation.execution import recovery_lifecycle as life
    r = make_runner(paper)
    store = runner_store(r)
    receipt = store.accept_submission(submission_key='saved-job', entity_type='job', request={'same': 1}, spec={})
    store.record_job_state(receipt.entity_id, 'queued')
    store.record_job_state(receipt.entity_id, 'success')
    store.put_record('result', receipt.entity_id, {'result_state': 'ready', 'result_receipt_id': 'saved-result'})
    frozen = store.get_record('run', 'manifest')
    sleeps = []
    cooldown = life._cooldown
    def observed(runner, state):
        before = store.get_record('test', 'calls')
        snapshot = build_progress_snapshot(r.workspace)
        assert snapshot['controller_alive'] and snapshot['phase'] == 'waiting_for_provider'
        with pytest.raises(RunRecoveryError, match='another controller'):
            TaskRunner.restore(r.run_id, r.workspace.parent)
        assert cooldown(runner, state)
        assert store.get_record('test', 'calls') == before
        sleeps.append(before)
        return True
    monkeypatch.setattr(life, '_cooldown', observed)
    result = r.run()
    assert result['status'] == 'completed', result.get('error')
    assert sleeps == [1, 2]
    attempts = list(store.records('attempt').values())
    assert len({a['provider_session_id'] for a in attempts}) == 1
    assert [a['recovery_source_attempt'] for a in attempts] == [None, 'attempt_0001', 'attempt_0002']
    assert [a['start_reason'] for a in attempts] == ['create', 'automatic_resume', 'automatic_resume']
    assert store.get_record('resume', 'state')['automatic_attempts'] == 2
    assert store.get_submission('saved-job')['receipt_id'] == receipt.receipt_id
    assert len(store.list_jobs()) == 1
    assert store.get_record('result', receipt.entity_id)['result_receipt_id'] == 'saved-result'
    assert store.usage() == {'input_tokens': 7, 'output_tokens': 3, 'turns': 1}
    after = store.get_record('run', 'manifest')
    assert after['config_hash'] == frozen['config_hash'] and after['deadline_at'] == frozen['deadline_at']
    assert after['error'] is None and after['last_failure']['resolved_at']


@pytest.mark.parametrize('mode,status', [('pause', 'suspended_infrastructure'), ('cancel', 'cancelled'), ('deadline', 'budget_exhausted')])
def test_cooling_interrupt_never_launches_again(make_runner, monkeypatch, mode, status):
    from evaluation.execution import recovery_lifecycle as life
    r = make_runner()
    store = runner_store(r)
    real = life._cooldown
    def interrupt(runner, state):
        if mode == 'deadline':
            runner.deadline_at = datetime.fromtimestamp(time.time() - 1, timezone.utc).isoformat()
        else:
            store.put_record('control', 'current', {'command': mode})
        return real(runner, state)
    monkeypatch.setattr(life, '_cooldown', interrupt)
    result = r.run()
    assert result['status'] == status
    assert store.get_record('test', 'calls') == 1
    assert len(store.records('attempt')) == 1


def test_no_resume_and_manual_resume_do_not_reset_retry_or_frozen_config(make_runner):
    r = make_runner(resume=False)
    assert r.run()['status'] == 'suspended_infrastructure'
    store = runner_store(r)
    saved = store.get_record('run', 'manifest')
    # Historical scientific configs without fields introduced later stay byte-equivalent.
    saved['config'].pop('progress_interval')
    saved['config_hash'] = canonical_config_hash(saved['config'])
    store.put_record('run', 'manifest', saved)
    store.put_record('resume', 'state', {'automatic_attempts': 3, 'wait_budget_used_seconds': 2})
    restored = TaskRunner.restore(r.run_id, r.workspace.parent)
    restored.resume_enabled = True
    result = restored.run()
    assert result['status'] == 'suspended_infrastructure'
    assert store.get_record('test', 'calls') == 2
    assert store.get_record('resume', 'state')['automatic_attempts'] == 3
    assert store.get_record('resume', 'state')['wait_budget_used_seconds'] == 2
    assert store.get_record('run', 'manifest')['config'] == saved['config']
    assert store.records('attempt')['attempt_0002']['recovery_source_attempt'] == 'attempt_0001'
    assert store.records('attempt')['attempt_0002']['start_reason'] == 'manual_resume'


def test_manifest_overrides_stale_projection_and_results_dont_end_follow(make_runner):
    r = make_runner(resume=False)
    r.run()
    store = runner_store(r)
    store.put_record('controller', 'identity', process_identity(os.getpid()))
    r._persist_run_manifest(run_state='suspended_infrastructure')
    store.put_record('resume', 'state', {'next_retry_at': time.time() + 60})
    (r.workspace.parent / 'results.json').write_text('{}')
    snapshot = build_progress_snapshot(r.workspace)
    assert snapshot['run_status'] == 'suspended_infrastructure' and snapshot['phase'] == 'waiting_for_provider'
    assert batch_is_active(r.workspace.parent)
    store.put_record('controller', 'identity', {})


@pytest.mark.parametrize('status,expected', [('completed', 0), ('failed', 1), ('cancelled', 1), ('budget_exhausted', 1),
                                           ('recovery_blocked', 2), ('preflight_failed', 2), ('suspended_infrastructure', 3)])
def test_exit_codes(status, expected):
    assert execution_exit_code(status) == expected
    assert execution_exit_code('completed', 'in_doubt') == 4


def test_constructor_failure_and_other_tasks_are_reported(tmp_path, monkeypatch):
    from evaluation import cli
    from evaluation.execution.wait_policy import ProviderPreflightError
    monkeypatch.setattr(cli, 'WORKSPACES_DIR', tmp_path / 'runs')
    from evaluation import repository
    root = tmp_path / 'tasks'
    for paper in ('paper_one', 'paper_two'):
        package(root, paper_id=paper)
    monkeypatch.setattr(repository, 'TASK_ROOTS', [root])
    monkeypatch.setattr(cli, 'TaskRunner', lambda *a, **k: (_ for _ in ()).throw(
        ProviderPreflightError('provider_version_unrecognized', {'stdout': 'strange-version', 'stderr': '', 'host': 'test'})))
    cfg = tmp_path / 'config.json'
    cfg.write_text(json.dumps({'agents': ['mock'], 'tasks': [{'paper_id': p, 'task_type': 'autonomous_research'}
        for p in ('paper_one', 'paper_two')], 'judge': {'enabled': False}}))
    assert cli.run_eval(cfg) == 2
    batch = next((tmp_path / 'runs/cli_runs').iterdir())
    report = json.loads((batch / 'eval_report.json').read_text())
    assert len(report['runs']) == 2
    assert all(row['status'] == 'preflight_failed' and row['provider_diagnostics']['stdout'] == 'strange-version' for row in report['runs'])
    assert json.loads((batch / 'results.json').read_text())['summary']['preflight_failed'] == 2
    assert not batch_is_active(batch)


def test_probe_distinguishes_missing_and_bad_version(tmp_path):
    from evaluation.execution.wait_policy import probe_cli, codex_wait_capability, ProviderPreflightError
    with pytest.raises(ProviderPreflightError, match='executable_missing'):
        probe_cli(str(tmp_path / 'absent'))
    exe = tmp_path / 'fake-codex'
    exe.write_text('#!/bin/sh\necho wrong-version\necho diagnostic >&2\n')
    exe.chmod(0o755)
    diag = probe_cli(str(exe))
    assert diag['returncode'] == 0 and diag['stderr'] == 'diagnostic' and not diag['api_verified']
    with pytest.raises(ProviderPreflightError, match='version_unrecognized'):
        codex_wait_capability(str(exe), diagnostics=diag)


def test_retry_after_not_shortened_and_wait_budget_is_bounded():
    policy = {'enabled': True, 'limits': {'max_attempts': 2, 'max_wait_seconds': 70, 'initial_delay_seconds': 1, 'max_delay_seconds': 2}}
    error = {'retryable': True, 'retry_after_seconds': 60}
    assert retry_delay(error, policy, {})[0] == 60
    assert retry_delay(error, policy, {'wait_budget_used_seconds': 15}) == (None, 'automatic_wait_limit')


@pytest.mark.parametrize('failure', ['rate_limit', 'in_doubt'])
def test_whole_evaluation_resume_only_scores_and_replays_saved_result(make_runner, monkeypatch, failure):
    from evaluation.execution.control import main, resume_scoring
    from evaluation.scoring import service
    from test_judging import fixture_verdict
    r = make_runner(resume=False)
    store = runner_store(r)
    store.put_record('test', 'failures', 0)
    assert r.run()['status'] == 'completed'
    config = {'judge': {'enabled': True}}
    store.put_record('batch', 'origin', {'directory': str(r.workspace.parent), 'config': config})
    calls = []
    def judge(prompt, **kwargs):
        calls.append(1)
        if len(calls) == 1:
            if failure == 'in_doubt':
                raise TimeoutError('lost response')
            raise RuntimeError('rate limit exceeded')
        return fixture_verdict(json.loads(prompt))
    monkeypatch.setattr(service, '_default_judge_call', judge)
    initial = resume_scoring(r.workspace, config)
    assert initial['evaluation_status'] == ('in_doubt' if failure == 'in_doubt' else 'suspended_infrastructure')
    monkeypatch.setattr(TaskRunner, 'restore', lambda *a, **k: pytest.fail('Agent already completed'))
    argv = ['resume', '--run-root', str(r.workspace.parent), '--run-id', r.run_id, '--resume']
    if failure == 'in_doubt':
        assert main(argv) == 4
        assert len(calls) == 1
        argv += ['--retry-in-doubt']
    assert main(argv) == 0
    assert len(calls) == 2 and store.get_record('test', 'calls') == 1
    saved = json.loads((r.workspace / '_score.json').read_text())
    assert saved['score_id'] == initial['score_id']
    assert main(argv) == 0
    assert len(calls) == 2
    assert len(store.records('attempt')) == 1


def test_judge_automatic_rate_limit_cools_without_new_agent(make_runner, monkeypatch):
    from evaluation.execution.control import resume_scoring
    from evaluation.scoring import service
    from test_judging import fixture_verdict
    r = make_runner()
    store = runner_store(r)
    store.put_record('test', 'failures', 0)
    assert r.run()['status'] == 'completed'
    calls = []
    def judge(prompt, **kwargs):
        calls.append(time.monotonic())
        if len(calls) < 3:
            raise RuntimeError('rate limit exceeded')
        return fixture_verdict(json.loads(prompt))
    monkeypatch.setattr(service, '_default_judge_call', judge)
    result = resume_scoring(r.workspace, {'judge': {'enabled': True}})
    assert result['evaluation_status'] == 'scored', result
    assert len(calls) == 3 and calls[1] - calls[0] >= .12
    assert store.get_record('test', 'calls') == 1
    assert store.get_record('resume', 'state')['automatic_attempts'] == 2


def test_resume_flags_conflict_and_explicit_identity():
    from evaluation.cli import main
    for args in (['--resume', '--no-resume'], ['--resume', '--run-id', 'run'], ['--resume', '--run-root', '/tmp']):
        with pytest.raises(SystemExit) as stopped:
            main(args)
        assert stopped.value.code == 2


def test_unsupported_auto_resume_and_default_codex_checkpoint(tmp_path, monkeypatch):
    root = tmp_path / 'tasks'
    package(root)
    common = {'task_roots': [str(root)], 'workspace_root': tmp_path / 'runs'}
    with pytest.raises(ValueError, match='resume_unsupported'):
        TaskRunner('paper_fixture', agent_key='mock', execution_mode='distributed', resume=True, **common)
    monkeypatch.setattr('evaluation.execution.wait_policy.probe_cli', lambda exe: {'stdout': 'codex-cli 0.154.0', 'resolved_executable': '/fake/codex'})
    r = TaskRunner('paper_fixture', agent_key='codex', resume=False, **common)
    assert r.recovery_enabled and r.resume_enabled is False
    assert r.agent['executable'] == '/fake/codex'


def test_interrupted_cooldown_keeps_schedule_and_counter(make_runner, monkeypatch):
    from evaluation.execution import recovery_lifecycle as life
    r = make_runner()
    store = runner_store(r)
    real = life._cooldown
    monkeypatch.setattr(life, '_cooldown', lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        r.run()
    state = store.get_record('resume', 'state')
    assert state['next_retry_at'] and state.get('automatic_attempts', 0) == 0
    reserved = state['wait_budget_used_seconds']
    monkeypatch.setattr(life, '_cooldown', real)
    restored = TaskRunner.restore(r.run_id, r.workspace.parent)
    assert restored.run()['status'] == 'completed'
    state = store.get_record('resume', 'state')
    assert state['automatic_attempts'] == 2
    assert reserved < state['wait_budget_used_seconds'] <= reserved + .2
    assert len(store.records('attempt')) == 3


def test_launch_failure_has_attempt_and_does_not_reuse_id(make_runner, monkeypatch):
    r = make_runner()
    store = runner_store(r)
    # Startup failure is durably distinguishable from a provider which ran then failed.
    monkeypatch.setattr(r, 'build_agent_argv', lambda: ['/definitely/missing/provider'])
    result = r.run()
    attempt = store.records('attempt')['attempt_0001']
    assert result['status'] == 'suspended_infrastructure'
    assert attempt['startup_status'] == 'launch_failed' and 'process_started_at' not in attempt
    assert attempt['recovery_source_attempt'] is None
    assert store.get_record('run', 'manifest')['attempt_id'] == attempt['attempt_id']
    assert not store.get_record('test', 'calls')


def test_dry_run_performs_local_preflight_without_launch(tmp_path, monkeypatch):
    from evaluation import cli, repository
    root = tmp_path / 'tasks'
    package(root)
    monkeypatch.setattr(repository, 'TASK_ROOTS', [root])
    monkeypatch.setattr(cli, 'WORKSPACES_DIR', tmp_path / 'runs')
    monkeypatch.setenv('RCB_CODEX_EXECUTABLE', '/definitely/missing/codex')
    cfg = tmp_path / 'config.json'
    cfg.write_text(json.dumps({'agents': ['codex'], 'tasks': [{'paper_id': 'paper_fixture', 'task_type': 'autonomous_research'}], 'judge': {'enabled': False}}))
    monkeypatch.setattr(TaskRunner, 'run', lambda *a: pytest.fail('dry-run cannot launch Agent'))
    assert cli.run_eval(cfg, dry_run=True) == 2
    batch = next((tmp_path / 'runs/cli_runs').iterdir())
    row = json.loads((batch / 'eval_report.json').read_text())['runs'][0]
    assert row['provider_diagnostics']['failure_reason'] == 'provider_executable_missing'
    assert row['api_verified'] is False and row['run_id'] is None


def test_setup_failure_has_durable_preflight_state(tmp_path, monkeypatch):
    from evaluation import cli, repository
    root = tmp_path / 'tasks'
    package(root)
    monkeypatch.setattr(repository, 'TASK_ROOTS', [root])
    monkeypatch.setattr(cli, 'WORKSPACES_DIR', tmp_path / 'runs')
    def broken_setup(self):
        self.workspace.mkdir(parents=True)
        raise OSError('fixture task materialization failure')
    monkeypatch.setattr(TaskRunner, 'setup_workspace', broken_setup)
    cfg = tmp_path / 'config.json'
    cfg.write_text(json.dumps({'agents': ['mock'], 'tasks': [{'paper_id': 'paper_fixture', 'task_type': 'autonomous_research'}], 'recovery_enabled': True, 'judge': {'enabled': False}}))
    assert cli.run_eval(cfg) == 2
    batch = next((tmp_path / 'runs/cli_runs').iterdir())
    row = json.loads((batch / 'eval_report.json').read_text())['runs'][0]
    assert row['status'] == 'preflight_failed' and row['phase'] == 'preflight'
    assert build_progress_snapshot(row['workspace'])['run_status'] == 'preflight_failed'


def test_string_wrapped_api_error_retains_exact_code_without_invented_http():
    event = {'type': 'turn.failed', 'error': {'message': json.dumps({'error': {
        'message': 'The encrypted content could not be decrypted or parsed.',
        'type': 'invalid_request_error', 'code': 'invalid_encrypted_content'}})}}
    error = normalize_error(event, source='agent')
    assert error['code'] == 'invalid_encrypted_content'
    assert error['category'] == 'configuration' and not error['retryable']
    assert error['message'] == 'The encrypted content could not be decrypted or parsed.'
    assert 'http_status' not in error and 'retry_after_seconds' not in error


def test_http_and_error_code_take_precedence_over_incidental_message():
    error = normalize_error({'status_code': 401, 'message': 'network timeout while authenticating'}, source='test')
    assert error['category'] == 'authentication' and not error['retryable']
    error = normalize_error({'status_code': 503, 'error': {'type': 'invalid_request_error', 'message': 'invalid request at gateway'}}, source='test')
    assert error['category'] == 'service_unavailable' and error['retryable']

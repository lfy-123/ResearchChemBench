"""External process protocol and legacy compatibility, without model calls."""

import json
import os
import sys
from pathlib import Path

import pytest

from evaluation.agent_plugins.registry import AgentConfigError, resolve_agent_definitions
from evaluation.agent_plugins.protocol import EVENT_VERSION, external_usage, normalize_external_event
from evaluation.execution.runner import TaskRunner
from evaluation.execution.recovery import runner_store
from evaluation.provenance.agent_events import load_agent_events
from evaluation.provenance.evidence_archive import export_run_archive
from evaluation.provenance.results import build_workspace_results
from evaluation.repository import TaskRepository
from evaluation.schemas.eval_config import resolve_specs, resolve_task_repository, load_yaml, EvalConfigError
from evaluation.settings import AGENT_PRESETS
from test_task_package_v19 import package


def make_runner(tmp_path, source, **kwargs):
    tasks = tmp_path / 'tasks'
    package(tasks)
    script = tmp_path / 'agent with spaces.py'
    script.write_text(source)
    return TaskRunner('paper_fixture', agent_key='my_agent',
                      agent_definition={'command': [sys.executable, str(script)]},
                      task_repository=TaskRepository([tasks]), workspace_root=tmp_path / 'runs',
                      live_progress=False, progress_console=False, **kwargs)


WRAPPER = '''
import argparse, json, os
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--request'); args=p.parse_args()
r=json.loads(Path(args.request).read_text())
w=Path(r['workspace'])
assert Path.cwd()==w
assert 'evaluation' not in r['public_input_files']
assert not any(k.startswith('JUDGE') for k in os.environ)
assert r['protocol']=='rcb-agent-request-v1'
assert Path(r['tools']['config_file']).is_file()
(w/'report/report.md').write_text('Fixture: no claim of a real scientific calculation.')
(w/'report/results.json').write_text(json.dumps({'barrier': 2, 'conclusion': 'fixture'}))
print('ordinary text log')
print(json.dumps({'type': 'thread.started', 'thread_id': 'internal-session'}))
for role in ('planner', 'reviewer'):
    print(json.dumps({'protocol':'rcb-agent-event-v1','run_id':r['run_id'],
        'event_id':'usage-1','agent_id':role,'session_id':'one','event':'usage',
        'usage':{'mode':'delta','input_tokens':10,'output_tokens':5}}))
'''


def test_process_submission_events_and_archive(tmp_path, monkeypatch):
    monkeypatch.setenv('JUDGE_API_KEY', 'not-for-agent')
    runner = make_runner(tmp_path, WRAPPER)
    result = runner.run()
    assert result['status'] == 'completed'
    assert result['provider_session_id'] is None
    assert result['model_io_trace']['capture_mode'] == 'external_agent_reported_events'
    assert not runner.recovery_enabled
    assert not (runner.workspace / '.mcp.json').exists()
    assert not (runner.workspace / 'opencode.json').exists()
    request = json.loads((runner.workspace / '_agent_protocol/request.json').read_text())
    assert request['public_input_files'] == ['data/inputs/system.xyz', 'submission_schema.json', 'task.md']
    assert str(tmp_path / 'tasks') not in json.dumps(request)
    frozen = runner_store(runner).get_record('frozen', 'external_agent')
    assert frozen['files']['_agent_protocol/request.json']
    assert 'session_store_path' not in runner_store(runner).get_record('run', 'manifest')
    summary = build_workspace_results(runner.workspace)
    assert summary['tokens']['agent']['tokens']['total'] == 30
    assert summary['tokens']['agent']['coverage'] == 'unknown'
    assert summary['agent']['execution_backend'] == 'benchmark'
    events = load_agent_events(runner.workspace)
    assert {e['agent_id'] for e in events if e['kind'] == 'usage'} == {'planner', 'reviewer'}
    index = export_run_archive(runner.workspace, tmp_path / 'archive')
    assert index['verification']['state'] == 'complete'
    assert (tmp_path / 'archive/workspace/_agent_protocol/request.json').is_file()
    assert not (tmp_path / 'archive/workspace/_agent_protocol/home').exists()


@pytest.mark.parametrize('source', ["print('done')", WRAPPER + '\nraise SystemExit(7)',
                                  WRAPPER + "\n(w/'submission_schema.json').chmod(0o644)\n(w/'submission_schema.json').write_text('{}')",
                                  WRAPPER + "\nPath(args.request).chmod(0o644)\nPath(args.request).write_text('{}')"])
def test_false_completion_rejected(tmp_path, source):
    runner = make_runner(tmp_path, source)
    assert runner.run()['status'] == 'failed'


def test_timeout_terminates_external_process(tmp_path):
    from datetime import datetime, timedelta, timezone
    runner = make_runner(tmp_path, 'import time\ntime.sleep(60)', timeout_seconds=60)
    runner.setup_workspace()
    runner.deadline_at = (datetime.now(timezone.utc) + timedelta(seconds=2)).isoformat()
    meta = runner.run()
    assert meta['status'] == 'failed' and meta['termination'] == 'timeout'
    assert runner.process.poll() is not None


def test_external_operator_cancellation(tmp_path):
    import threading
    runner = make_runner(tmp_path, 'import time\ntime.sleep(60)', timeout_seconds=60)
    runner.setup_workspace()
    timer = threading.Timer(1, lambda: runner_store(runner).put_record(
        'control', 'current', {'command': 'cancel', 'source': 'operator_cli'}))
    timer.start()
    try:
        meta = runner.run()
    finally:
        timer.cancel()
        timer.join()
    assert meta['status'] == 'failed' and meta['termination'] == 'stopped'
    assert runner.process.poll() is not None


def test_external_exit_cleans_child_holding_stdout(tmp_path):
    import time
    from chemistry_toolbox.src.recovery_io import process_identity
    source = WRAPPER + '''
import subprocess, sys, time
child_code = "import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); print('child-ready',flush=True); time.sleep(60)"
child = subprocess.Popen([sys.executable, '-c', child_code])
(w/'outputs/child_pid.txt').write_text(str(child.pid))
time.sleep(0.3)
'''
    runner = make_runner(tmp_path, source, timeout_seconds=20)
    meta = runner.run()
    assert meta['status'] == 'completed', meta
    pid = int((runner.workspace / 'outputs/child_pid.txt').read_text())
    for _ in range(20):
        if not process_identity(pid).get('verified'):
            break
        time.sleep(0.05)
    assert not process_identity(pid).get('verified')


def test_conflicting_usage_events_remain_visible(tmp_path):
    (tmp_path / '_meta.json').write_text(json.dumps({'agent_kind': 'external', 'run_id': 'r'}))
    event = {'protocol': EVENT_VERSION, 'run_id': 'r', 'agent_id': 'a', 'event_id': '1',
             'event': 'usage', 'usage': {'mode': 'delta', 'input_tokens': 4, 'output_tokens': 2}}
    conflict = {**event, 'usage': {**event['usage'], 'input_tokens': 9}}
    (tmp_path / '_agent_output.jsonl').write_text('\n'.join(map(json.dumps, [event, event, conflict])))
    events = load_agent_events(tmp_path)
    assert len(events) == 2
    assert external_usage(events)['accounting_status'] == 'conflicting'
    assert external_usage(events)['tokens']['total'] is None


@pytest.mark.parametrize('kwargs', [{'resume': True}, {'recovery_enabled': True},
                                   {'execution_mode': 'distributed'}, {'model_wait_strategy': 'host_event_wait'}])
def test_unsupported_capabilities_fail_before_launch(tmp_path, kwargs):
    with pytest.raises(ValueError):
        make_runner(tmp_path, WRAPPER, **kwargs)
    assert not (tmp_path / 'runs').exists()


@pytest.mark.parametrize('definition', [
    {'command': 'python agent.py'}, {'command': []}, {'command': ['python', '--request', 'elsewhere']},
    {'command': ['python'], 'env_allowlist': ['JUDGE_API_KEY']},
    {'command': ['python'], 'env_allowlist': ['RESEARCHCHEMBENCH_TASK_ROOTS']},
    {'command': ['python'], 'options': {'api_key': 'do-not-store'}},
    {'command': ['python'], 'execution_backend': 'unregistered'},
    {'command': ['python'], 'model_budget_enforcement': 'hard'},
    {'command': ['python'], 'unknown': True},
])
def test_invalid_definitions(definition, tmp_path):
    with pytest.raises(AgentConfigError):
        resolve_agent_definitions({'agent_definitions': {'custom': definition}}, config_dir=tmp_path)


def test_registry_is_local_and_preserves_executable_symlink(tmp_path):
    python = tmp_path / 'python'
    python.symlink_to(sys.executable)
    before = json.dumps(AGENT_PRESETS, sort_keys=True)
    registry = resolve_agent_definitions({'agent_definitions': {'my_agent': {'command': ['./python']}}}, config_dir=tmp_path)
    assert registry['my_agent']['command'] == [str(python)]
    registry['codex']['label'] = 'changed in local copy'
    assert json.dumps(AGENT_PRESETS, sort_keys=True) == before
    assert 'my_agent' not in resolve_agent_definitions({}, config_dir=tmp_path)
    with pytest.raises(AgentConfigError, match='override'):
        resolve_agent_definitions({'agent_definitions': {'codex': {'command': ['python']}}}, config_dir=tmp_path)


def test_duplicate_yaml_registration_rejected(tmp_path):
    path = tmp_path / 'duplicate.yaml'
    path.write_text('agent_definitions:\n  team: {command: [one]}\n  team: {command: [two]}\n')
    with pytest.raises(EvalConfigError, match='Duplicate agent'):
        load_yaml(path)


def test_environment_is_scoped_and_empty_usage_unknown(tmp_path, monkeypatch):
    monkeypatch.setenv('JUDGE_OTHER_SECRET', 'private')
    monkeypatch.setenv('UNLISTED_MODEL_KEY', 'private')
    runner = make_runner(tmp_path, 'print("hello")')
    runner.setup_workspace()
    env = runner._agent_environment()
    assert 'JUDGE_OTHER_SECRET' not in env and 'UNLISTED_MODEL_KEY' not in env
    assert env['HOME'].startswith(str(runner.workspace))
    assert external_usage([])['tokens']['total'] is None


def test_usage_delta_snapshot_and_conflicting_modes():
    def event(i, mode, count):
        return normalize_external_event({'protocol': EVENT_VERSION, 'run_id': 'r', 'agent_id': 'a',
                                         'event_id': str(i), 'event': 'usage', 'session_id': 's',
                                         'usage': {'mode': mode, 'input_tokens': count, 'output_tokens': count}})
    assert external_usage([event(1, 'delta', 3), event(1, 'delta', 3), event(2, 'delta', 2)])['tokens']['total'] == 10
    assert external_usage([event(1, 'cumulative', 3), event(2, 'cumulative', 5)])['tokens']['total'] == 10
    assert external_usage([event(1, 'delta', 3), event(2, 'cumulative', 5)])['accounting_status'] == 'conflicting'


def test_final_repository_selected_consistently(tmp_path):
    source = package(tmp_path / 'tasks')
    final = tmp_path / 'tasks/final_verified_autonomous_research/paper_fixture'
    final.parent.mkdir()
    source.rename(final)
    # Default discovery would encounter this invalid, unrelated package.
    broken = tmp_path / 'tasks/autonomous_research/paper_bad'
    broken.mkdir()
    config = {'task_source': {'kind': 'final_verified', 'root': 'tasks'},
              'tasks': [{'paper_id': 'paper_fixture', 'task_type': 'autonomous_research'}],
              'agents': ['mock', 'external_test']}
    registry = resolve_agent_definitions({'agent_definitions': {'external_test': {'command': [sys.executable]}}}, config_dir=tmp_path)
    repo = resolve_task_repository(config, config_dir=tmp_path)
    specs = resolve_specs(config, agent_registry=registry, task_repository=repo)
    assert [s.agent_key for s in specs] == ['mock', 'external_test']
    runner = TaskRunner('paper_fixture', task_repository=repo, workspace_root=tmp_path / 'runs')
    assert runner.task_dir == final
    runner.setup_workspace()
    assert runner._run_manifest()['task_source']['kind'] == 'final_verified'
    assert runner._run_manifest()['task_source']['directory'] == str(final)
    assert runner.task_dir != final  # All later scoring reads the frozen selected package.
    assert runner.task_package.package_content_sha256 == repo.get(paper_id='paper_fixture', task_type='autonomous_research').package_content_sha256
    with pytest.raises(ValueError, match='both'):
        TaskRunner('paper_fixture', task_repository=repo, task_roots=[str(tmp_path)])
    with pytest.raises(EvalConfigError, match='explicit'):
        resolve_task_repository({**config, 'tasks': 'all'}, config_dir=tmp_path)


def test_cli_mixed_batch_uses_final_source(tmp_path, monkeypatch):
    import yaml
    from evaluation import cli
    source = package(tmp_path / 'tasks')
    final = tmp_path / 'tasks/final_verified_autonomous_research/paper_fixture'
    final.parent.mkdir()
    source.rename(final)
    script = tmp_path / 'wrapper.py'
    script.write_text(WRAPPER)
    config = {'agents': ['mock', 'custom'], 'agent_definitions': {'custom': {'command': [sys.executable, str(script)]}},
              'task_source': {'kind': 'final_verified', 'root': 'tasks'},
              'tasks': [{'paper_id': 'paper_fixture', 'task_type': 'autonomous_research'}],
              'live_progress': False, 'judge': {'enabled': False}}
    config_path = tmp_path / 'batch.yaml'
    config_path.write_text(yaml.safe_dump(config))
    monkeypatch.setattr(cli, 'WORKSPACES_DIR', tmp_path / 'runs')
    assert cli.run_eval(config_path, dry_run=True) == 0
    report = json.loads(next((tmp_path / 'runs/cli_runs').glob('*/eval_report.json')).read_text())
    assert {row['agent_key'] for row in report['runs']} == {'mock', 'custom'}
    assert all(row['status'] == 'preflight_ready' for row in report['runs'])
    # Select a custom definition using the existing CLI entrypoint.
    assert cli.main([str(config_path), '--agent', 'custom', '--no-score']) == 0
    reports = [json.loads(p.read_text()) for p in (tmp_path / 'runs/cli_runs').glob('*/eval_report.json')]
    assert any(len(r['runs']) == 1 and r['runs'][0]['status'] == 'completed' for r in reports)


def test_external_uses_existing_scoring_and_portable_archive(tmp_path, monkeypatch):
    import shutil
    from evaluation.provenance.evidence_archive import open_archive
    from evaluation.scoring.service import score_workspace
    from evaluation.scoring.evidence import build_evidence_bundle
    from test_judging import fixture_verdict
    runner = make_runner(tmp_path, WRAPPER, archive_policy='legacy')
    assert runner.run()['status'] == 'completed'
    calls = []
    def judge(prompt):
        payload = json.loads(prompt)
        calls.append(payload)
        return fixture_verdict(payload)
    live = score_workspace(runner.workspace, judge_call=judge, publish=False, output_dir=tmp_path / 'live_score')
    assert live['status'] == 'scored', live
    assert live['score'] == 25
    assert live['task_package_content_sha256'] == runner.task_package.package_content_sha256
    export_run_archive(runner.workspace, tmp_path / 'archive')
    shutil.rmtree(runner.workspace)
    shutil.rmtree(runner_store(runner).directory)
    shutil.rmtree(tmp_path / 'tasks')
    archive = open_archive(tmp_path / 'archive')
    monkeypatch.setattr('subprocess.Popen', lambda *a, **k: pytest.fail('offline scoring must not start an agent or service'))
    replay = score_workspace(tmp_path / 'archive/workspace', judge_call=judge, publish=False,
        output_dir=tmp_path / 'offline_score', evidence_index=archive,
        evidence_bundle=build_evidence_bundle(archive))
    assert replay['status'] == 'scored', replay
    assert replay['score'] == live['score']
    assert replay['process_metrics'] == live['process_metrics']
    assert calls[0]['task_contract'] == calls[1]['task_contract']
    assert build_workspace_results(tmp_path / 'archive/workspace')['tokens']['agent']['tokens']['total'] == 30


@pytest.mark.parametrize('defect', ['failed', 'unknown_backend', 'unvalidated'])
def test_external_scoring_requires_finalization(tmp_path, defect):
    from evaluation.scoring.service import score_workspace
    runner = make_runner(tmp_path, WRAPPER)
    runner.setup_workspace()
    meta = json.loads(runner.meta_path.read_text())
    meta.update(status='completed', external_protocol_validation={'valid': True})
    if defect == 'failed':
        meta['status'] = 'failed'
    elif defect == 'unknown_backend':
        meta['execution_backend'] = 'arche_minichem'
    else:
        meta['external_protocol_validation'] = {'valid': False}
    runner.meta_path.write_text(json.dumps(meta))
    result = score_workspace(runner.workspace, publish=False, output_dir=tmp_path / 'score',
                             judge_call=lambda p: pytest.fail('unvalidated external run reached the judge'))
    assert result['status'] == 'needs_review'
    assert result['score'] is None


def test_two_tool_clients_share_one_resource_budget(tmp_path):
    import subprocess
    runner = make_runner(tmp_path, WRAPPER, available_cpu_cores=1, available_memory_mb=512)
    runner.setup_workspace()
    environment = {**os.environ, **runner._mcp_environment()}
    environment.pop('RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT', None)
    reserve = '''
from chemistry_toolbox.src.resource_budget import reserve_resources
reservation=reserve_resources({'cpu_cores':1,'memory_mb':128,'gpu_count':0}, kind='test', label='role')
print('reserved', flush=True)
input()
reservation.release()
'''
    first = subprocess.Popen([sys.executable, '-c', reserve], env=environment, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        assert first.stdout.readline().strip() == 'reserved'
        second = subprocess.run([sys.executable, '-c', reserve], env=environment, input='\n', capture_output=True, text=True, timeout=15)
        assert second.returncode != 0 and 'aggregate active-job' in second.stderr
    finally:
        first.communicate('\n', timeout=15)

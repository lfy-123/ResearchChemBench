from __future__ import annotations
import json
import os
import signal
import uuid
from pathlib import Path

import pytest
from test_task_package_v19 import package
from evaluation.execution.runner import TaskRunner
from evaluation.execution.recovery import RunRecoveryError, runner_store, restore_runner
from evaluation.execution.recovery_lifecycle import record_usage
from chemistry_toolbox.src.recovery_io import process_identity


@pytest.fixture
def runner(tmp_path, monkeypatch):
    task_root = tmp_path/'tasks'; package(task_root)
    monkeypatch.setenv('RCB_MOCK_DISCONNECT_ONCE','1')
    value = TaskRunner('paper_fixture',task_type='autonomous_research',agent_key='mock',task_roots=[str(task_root)],
                       workspace_root=tmp_path/'runs',recovery_enabled=True,live_progress=False,
                       timeout_seconds=90,available_cpu_cores=1,available_memory_mb=512)
    yield value
    if value._controller_lock: value._controller_lock.release()
    if value.workspace.exists():
        owner = runner_store(value).get_record('manager','identity',{})
        if process_identity(owner.get('pid'),owner)['verified']:
            try: os.kill(owner['pid'],signal.SIGTERM)
            except ProcessLookupError: pass


def test_missing_session_and_double_controller_are_blocked(runner):
    assert runner.run()['status'] == 'suspended_infrastructure'
    store = runner_store(runner)
    restored = TaskRunner.restore(runner.run_id, runner.workspace.parent)
    try:
        with pytest.raises(RunRecoveryError, match='another controller'):
            TaskRunner.restore(runner.run_id, runner.workspace.parent)
    finally: restored._controller_lock.release()
    runner._resume_session_id = None
    runner._persist_run_manifest(run_state='suspended_infrastructure')
    with pytest.raises(RunRecoveryError, match='session_missing'):
        TaskRunner.restore(runner.run_id, runner.workspace.parent)
    assert len(store.records('attempt')) == 1


def test_restore_uses_frozen_task_and_rejects_workspace_drift(runner):
    runner.run()
    # Mutable source repository is not consulted during restore.
    for root in runner.task_repository.roots:
        assert 'task_snapshot' in str(root)
    path = runner.workspace/'task.md'
    path.chmod(0o644); path.write_text('changed')
    with pytest.raises(RunRecoveryError, match='frozen_input_modified'):
        TaskRunner.restore(runner.run_id,runner.workspace.parent)


def test_expired_budget_and_terminal_runs_do_not_restart(runner):
    runner.run()
    runner.deadline_at = '2020-01-01T00:00:00+00:00'
    runner._persist_run_manifest(run_state='suspended_infrastructure')
    with pytest.raises(RunRecoveryError, match='expired'):
        TaskRunner.restore(runner.run_id,runner.workspace.parent)
    runner._persist_run_manifest(run_state='completed')
    with pytest.raises(RunRecoveryError, match='terminal'):
        runner.run()
    assert runner_store(runner).get_record('run','manifest')['run_state'] == 'completed'


def expired_run(runner):
    """Prepare a stopped, expired run with a real mock-provider session."""
    import time
    from datetime import datetime, timedelta, timezone
    from evaluation.execution.recovery import canonical_config_hash
    assert runner.run()['status'] == 'suspended_infrastructure'
    store = runner_store(runner)
    runner.first_started_at = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
    runner.deadline_at = (datetime.fromisoformat(runner.first_started_at) + timedelta(seconds=90)).isoformat()
    runner._persist_run_manifest(run_state='budget_exhausted', termination='budget_exhausted')
    store.put_record('control', 'current', {'command': 'cancel', 'reason': 'deadline'})
    adapter = store.get_record('frozen', 'adapter')
    store.put_record('frozen', 'adapter', {**adapter, 'mcp_hash': canonical_config_hash(runner._mcp_server_specs())})
    # Let the manager observe terminal state and release its lifetime lock.
    for _ in range(100):
        identity = store.get_record('manager', 'identity', {})
        if not process_identity(identity.get('pid'), identity)['verified']:
            break
        time.sleep(.1)
    else:
        pytest.fail('expired fixture manager did not stop')
    return store


def test_explicit_extension_preserves_session_jobs_and_original_start(runner, monkeypatch):
    from datetime import datetime
    from evaluation.execution.recovery import canonical_config_hash, verify_frozen_runner
    store = expired_run(runner)
    receipt = store.accept_submission(submission_key='previous-calculation', entity_type='job', request={'command': 'fixture'})
    store.record_job_state(receipt.entity_id, 'timeout')
    before = store.get_record('run', 'manifest')
    jobs, submissions, attempts, usage = store.list_jobs(), store.list_submissions(), store.records('attempt'), store.usage()
    with pytest.raises(RunRecoveryError, match='terminal'):
        TaskRunner.restore(runner.run_id, runner.workspace.parent)
    restored = TaskRunner.restore(runner.run_id, runner.workspace.parent, timeout_seconds=3600)
    try:
        after = store.get_record('run', 'manifest')
        assert after['schema_version'] == 2
        assert after['first_started_at'] == before['first_started_at']
        assert after['provider_session_id'] == before['provider_session_id']
        assert restored.workspace == runner.workspace and after['attempt_id'] == before['attempt_id']
        assert (datetime.fromisoformat(after['deadline_at']) - datetime.fromisoformat(after['first_started_at'])).total_seconds() == 3600
        assert after['config']['timeout_seconds'] == 3600
        assert after['config_hash'] == canonical_config_hash(after['config'])
        assert store.get_record('manager', 'config')['environment']['RESEARCHCHEMBENCH_RUN_DEADLINE'] == after['deadline_at']
        assert (store.list_jobs(), store.list_submissions(), store.records('attempt'), store.usage()) == (jobs, submissions, attempts, usage)
        assert len(store.records('budget_extension')) == 1
        verify_frozen_runner(restored)
        restored._controller_lock.release()
        # Future ordinary resumes must accept the updated frozen configuration.
        restored = TaskRunner.restore(runner.run_id, runner.workspace.parent)
        assert restored.deadline_at == after['deadline_at']
        (runner.workspace / 'report').mkdir(exist_ok=True)
        (runner.workspace / 'report/results.json').write_text('{"barrier":12.3,"conclusion":"path A"}')
        (runner.workspace / 'report/report.md').write_text('Mock provider output for the recovery test.')
        monkeypatch.delenv('RCB_MOCK_DISCONNECT_ONCE')
        assert restored.run()['status'] == 'completed'
        assert store.get_job(receipt.entity_id)['state'] == 'timeout'
        assert len(store.list_submissions()) == len(submissions)
    finally:
        if restored._controller_lock:
            restored._controller_lock.release()


@pytest.mark.parametrize('defect,reason', [
    ('cancel', 'cancelled'), ('usage', 'usage_budget_exhausted'), ('active_job', 'active_or_uncertain_jobs'),
    ('input', 'frozen_input_modified'), ('manager', 'idle_manager'),
])
def test_extension_never_bypasses_other_recovery_guards(runner, defect, reason):
    from contextlib import nullcontext
    from chemistry_toolbox.src.recovery_io import file_lock
    store = expired_run(runner)
    if defect == 'cancel':
        store.put_record('control', 'current', {'command': 'cancel', 'source': 'operator_cli'})
    elif defect == 'usage':
        store.put_record('usage', 'limit', {'turns': runner.max_turns})
    elif defect == 'active_job':
        store.accept_submission(submission_key='unsettled-calculation', entity_type='job', request={})
    elif defect == 'input':
        path = runner.workspace / 'task.md'
        path.chmod(0o644)
        path.write_text('changed')
    before = store.get_record('run', 'manifest')
    with file_lock(store.directory / 'manager.lock') if defect == 'manager' else nullcontext():
        with pytest.raises(RunRecoveryError, match=reason):
            TaskRunner.restore(runner.run_id, runner.workspace.parent, timeout_seconds=3600)
    assert store.get_record('run', 'manifest') == before
    assert not store.records('budget_extension')


@pytest.mark.parametrize('timeout', [0, 89, 90, 91])
def test_extension_requires_larger_unexpired_total_budget(timeout):
    from datetime import datetime, timedelta, timezone
    from evaluation.execution.recovery import _extended_deadline
    first = datetime.now(timezone.utc) - timedelta(seconds=120)
    manifest = {'run_state': 'budget_exhausted', 'config': {'timeout_seconds': 90},
                'first_started_at': first.isoformat(), 'deadline_at': (first + timedelta(seconds=90)).isoformat()}
    with pytest.raises(RunRecoveryError, match='increase_total_budget|deadline_expired'):
        _extended_deadline(manifest, {'command': 'cancel', 'reason': 'deadline'}, timeout)


def test_usage_event_identity_deduplicates_replay(runner):
    runner.setup_workspace()
    runner._resume_session_id = str(uuid.uuid4())
    event = {'type':'turn.completed','turn_id':'t1','usage':{'input_tokens':10,'output_tokens':3}}
    record_usage(runner,event)
    runner.attempt_id='attempt_0002'
    record_usage(runner,event)
    assert runner_store(runner).usage() == {'input_tokens':10,'output_tokens':3,'turns':1}


@pytest.mark.parametrize("stop_mode,expected", [("budget","budget_exhausted"),("api_error","suspended_infrastructure"),("cancel","cancelled")])
def test_native_usage_is_recorded_before_turn_completion(runner, monkeypatch, stop_mode, expected):
    import sys
    runner.max_tokens = 20 if stop_mode == "budget" else None
    runner.setup_workspace()
    session=str(uuid.uuid4())
    path=runner_store(runner).directory/"codex"/"sessions"/(session+".jsonl")
    path.parent.mkdir(parents=True,exist_ok=True)
    events=[{"type":"session_meta","payload":{"id":session,"cwd":str(runner.workspace)}},
            {"type":"event_msg","timestamp":"2026-09-16T01:00:00Z","payload":{"type":"token_count","info":{
                "total_token_usage":{"input_tokens":50,"output_tokens":5,"cached_input_tokens":40}}}}]
    script=runner.workspace/"fixture_usage_agent.py"
    program="import json,time,sys\nfrom pathlib import Path\n"
    program+=f"print(json.dumps({{'type':'thread.started','thread_id':{session!r}}}),flush=True)\n"
    program+=f"Path({str(path)!r}).write_text({''.join(json.dumps(e)+chr(10) for e in events)!r})\n"
    if stop_mode=="api_error":program+="sys.exit(1)\n"
    elif stop_mode=="cancel":
        program+="from chemistry_toolbox.mcp.execution_store import ExecutionStore\n"
        program+=f"ExecutionStore(Path({str(runner.workspace)!r}),run_id={runner.run_id!r}).put_record('control','current',{{'command':'cancel'}})\n"
        program+="time.sleep(20)\n"
    else:program+="time.sleep(20)\n"
    script.write_text(program)
    monkeypatch.setattr(runner,"build_agent_argv",lambda:[sys.executable,str(script)])
    result=runner.run()
    assert result["status"]==expected
    assert result["usage"]=={"input_tokens":50,"output_tokens":5,"turns":0}
    assert result["usage_details"]["cached_input_tokens"]==40
    assert result["exit_code"] is not None


def test_status_is_read_only(runner, capsys):
    runner.run()
    from scripts.manage_evaluation_run import main
    store = runner_store(runner)
    before = (store.path.stat().st_mtime_ns, store.path.read_bytes())
    assert main(['status','--run-root',str(runner.workspace.parent),'--run-id',runner.run_id]) == 0
    assert json.loads(capsys.readouterr().out)['result']['recovery_capability']
    assert (store.path.stat().st_mtime_ns,store.path.read_bytes()) == before


def test_codex_exact_resume_preserves_provider_and_sandbox(runner, monkeypatch):
    runner.setup_workspace()
    runner.agent.update(kind='codex',executable='codex')
    runner._resume_session_id = str(uuid.uuid4())
    runner._recovery_notice = 'Query original jobs.'
    argv = runner.build_agent_argv()
    assert argv[:4] == ['codex','exec','resume',runner._resume_session_id]
    assert '--last' not in argv and '--ephemeral' not in argv
    assert 'sandbox_mode="workspace-write"' in argv
    assert 'model="gpt-5.6-sol"' in argv
    assert 'model_reasoning_effort="high"' in argv
    assert 'approval_policy="never"' in argv
    for spec in runner._mcp_server_specs():
        assert spec['default_tools_approval_mode'] == 'approve'
        assert f'mcp_servers.{spec["name"]}.default_tools_approval_mode="approve"' in argv
    runner._resume_session_id = None
    create_argv = runner.build_agent_argv()
    assert create_argv[:2] == ['codex', 'exec']
    assert 'sandbox_mode="workspace-write"' in create_argv
    for spec in runner._mcp_server_specs():
        assert f'mcp_servers.{spec["name"]}.default_tools_approval_mode="approve"' in create_argv
    runner._resume_session_id = argv[3]
    assert not any('sk-' in argument for argument in argv)
    wrong = json.dumps({'type':'thread.started','thread_id':str(uuid.uuid4())})
    with pytest.raises(RunRecoveryError,match='different_session'):
        runner.capture_provider_event(wrong)


def test_changed_mcp_approval_policy_blocks_restore(runner, monkeypatch):
    assert runner.run()['status'] == 'suspended_infrastructure'
    original = TaskRunner._mcp_server_specs

    def changed_specs(self):
        specs = original(self)
        for spec in specs:
            spec['default_tools_approval_mode'] = 'prompt'
        return specs

    monkeypatch.setattr(TaskRunner, '_mcp_server_specs', changed_specs)
    with pytest.raises(RunRecoveryError, match='provider_or_mcp_configuration_drift'):
        TaskRunner.restore(runner.run_id, runner.workspace.parent)


def test_pause_and_cancel_control_the_original_agent(runner, monkeypatch):
    import threading
    import time
    from scripts.manage_evaluation_run import main
    monkeypatch.setenv('RCB_MOCK_SLEEP_SECONDS','20')
    results=[]
    thread=threading.Thread(target=lambda: results.append(runner.run()))
    thread.start()
    deadline=time.time()+30
    while time.time()<deadline:
        if runner.workspace.exists() and runner_store(runner).get_record('run','manifest',{}).get('provider_session_id'): break
        time.sleep(.1)
    else: pytest.fail('mock Agent did not publish its session')
    assert main(['pause','--run-root',str(runner.workspace.parent),'--run-id',runner.run_id]) == 0
    thread.join(timeout=15)
    assert not thread.is_alive()
    assert results[0]['status'] == 'suspended_infrastructure'
    assert results[0]['termination'] == 'pause'
    original_id=results[0]['provider_session_id']
    restored=TaskRunner.restore(runner.run_id,runner.workspace.parent)
    try:
        assert restored._resume_session_id==original_id
    finally: restored._controller_lock.release()
    assert main(['cancel','--run-root',str(runner.workspace.parent),'--run-id',runner.run_id]) == 0
    assert runner_store(runner).get_record('control','current')['command']=='cancel'


def test_saved_codex_rollout_is_required(runner):
    from evaluation.execution.recovery import validate_session
    runner.setup_workspace()
    runner.agent.update(kind='codex',executable='codex')
    runner._resume_session_id=str(uuid.uuid4())
    with pytest.raises(RunRecoveryError,match='session_file_missing'):
        validate_session(runner)
    root=runner_store(runner).directory/'codex/sessions'; root.mkdir(parents=True)
    path=root/(runner._resume_session_id+'.jsonl')
    path.write_text(json.dumps({'type':'session_meta','payload':{'id':runner._resume_session_id,'cwd':str(runner.workspace)}})+'\n')
    validate_session(runner)
    path.write_text(json.dumps({'type':'session_meta','payload':{'id':runner._resume_session_id,'cwd':'/wrong'}})+'\n')
    with pytest.raises(RunRecoveryError,match='cwd_mismatch'):
        validate_session(runner)


def test_cancelled_run_cannot_be_resumed(runner):
    runner.run()
    runner_store(runner).put_record('control','current',{'command':'cancel'})
    with pytest.raises(RunRecoveryError,match='cancelled|terminal'):
        TaskRunner.restore(runner.run_id,runner.workspace.parent)


def test_resumed_judge_uses_frozen_responses_configuration(monkeypatch):
    from types import SimpleNamespace
    from evaluation.scoring import service
    import openai
    monkeypatch.setenv('RCB_TEST_CREDENTIAL','fixture-credential')
    for variable in ('JUDGE_API_KEY','JUDGE_API_BASE','JUDGE_MODEL_NAME','JUDGE_REASONING_EFFORT','JUDGE_WIRE_API'):
        monkeypatch.setenv(variable,'stale')
    service.apply_judge_configuration({'judge':{'model':'gpt-5.6-sol','base_url':'http://localhost/v1',
        'reasoning_effort':'high','wire_api':'responses','api_key_env':'RCB_TEST_CREDENTIAL'}})
    calls=[]
    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(output_text='{}',usage=SimpleNamespace(input_tokens=7,output_tokens=3,total_tokens=10))
    class Client:
        def __init__(self, **kwargs):
            assert kwargs['api_key']=='fixture-credential'
            assert kwargs['base_url']=='http://localhost/v1'
            self.responses=SimpleNamespace(create=create)
        def __enter__(self): return self
        def __exit__(self,*args): pass
    monkeypatch.setattr(openai,'OpenAI',Client)
    result=service._default_judge_call('fixture')
    assert calls[0]['model']=='gpt-5.6-sol'
    assert calls[0]['reasoning']=={'effort':'high'}
    assert result['_judge_usage']['total_tokens']==10

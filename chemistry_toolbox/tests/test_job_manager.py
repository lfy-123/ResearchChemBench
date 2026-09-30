from __future__ import annotations
import json
import os
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.mcp.job_manager import JobManager, ensure_manager
from chemistry_toolbox.mcp.managed_execution import freeze_files
from chemistry_toolbox.mcp.open_execution import _start_job, collect_execution_job, lookup_execution_submission
from chemistry_toolbox.mcp.execution_models import JobCollectRequest, ExecutionSubmissionLookupRequest
from chemistry_toolbox.src.recovery_io import process_identity, token_processes


def until(predicate, seconds=15):
    deadline = time.time() + seconds
    while time.time() < deadline:
        result = predicate()
        if result: return result
        time.sleep(.1)
    raise AssertionError('condition did not become true')


@pytest.fixture
def managed(tmp_path, monkeypatch):
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    for key, value in {
        'RESEARCHCHEMBENCH_WORKSPACE': str(workspace), 'RESEARCHCHEM_MCP_WORKSPACE': str(workspace),
        'RESEARCHCHEMBENCH_RUN_ID': 'test', 'RESEARCHCHEMBENCH_RECOVERY_ENABLED': '1',
        'RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES': '1', 'RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB': '512',
        'RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT': str(tmp_path / 'pool'),
        'RESEARCHCHEMBENCH_EXECUTION_MODE': 'local',
    }.items(): monkeypatch.setenv(key, value)
    monkeypatch.delenv('RESEARCHCHEMBENCH_RUN_DEADLINE', raising=False)
    manager = JobManager(workspace, run_id='test')
    yield manager
    for row in manager.store.list_jobs(): manager.cancel_entity(row['entity_id'], row['entity_type'])
    for row in manager.store.list_jobs():
        token = json.loads(row['state_json']).get('launch_token')
        if token:
            for identity in token_processes(token):
                try: os.kill(identity['pid'], signal.SIGKILL)
                except ProcessLookupError: pass
    identity = manager.store.get_record('manager', 'identity', {})
    if process_identity(identity.get('pid'), identity)['verified']:
        os.kill(identity['pid'], signal.SIGTERM)


def submit(key, delay=.5):
    return _start_job(job_type='native_software', runtime='core',
        command=[sys.executable, '-c', f'import time;print("launched",flush=True);time.sleep({delay})'],
        stdin_target=None, staged_inputs=[], resource_limits={'cpu_cores':1,'memory_mb':128,'gpu_count':0,'walltime_seconds':20},
        metadata={}, submission_key=key)


def test_queue_response_loss_manager_restart_and_stable_collection(managed):
    first = submit('first', 2)
    job = first['job_id']
    until(lambda: json.loads(managed.store.get_job(job)['state_json']).get('child_identity'))
    second = submit('second', .2)
    assert managed.store.get_job(second['job_id'])['state'] == 'queued'
    identity = managed.store.get_record('manager', 'identity')
    os.kill(identity['pid'], signal.SIGKILL)
    until(lambda: not process_identity(identity['pid'], identity)['verified'])
    ensure_manager(managed.store)
    replay = submit('first', 2)
    assert replay['job_id'] == job
    assert replay['receipt']['receipt_id'] == first['receipt']['receipt_id']
    until(lambda: managed.store.get_job(second['job_id'])['state'] == 'success')
    assert (managed._directory(job) / 'stdout.log').read_text().count('launched') == 1
    lookup = lookup_execution_submission(ExecutionSubmissionLookupRequest(submission_key='first'))
    assert job in json.dumps(lookup)
    result = collect_execution_job(JobCollectRequest(job_id=job))
    (managed._directory(job) / 'stdout.log').write_text('modified after collection')
    assert collect_execution_job(JobCollectRequest(job_id=job)) == result
    assert managed.store.get_record('delivery', job)['state'] == 'delivery_intent'


def test_post_accept_wakeup_failure_keeps_receipt_and_replays_once(managed, monkeypatch):
    import chemistry_toolbox.mcp.job_manager as module
    def unavailable(_store):
        raise OSError("fixture manager startup failure")
    with monkeypatch.context() as patch:
        patch.setattr(module, 'ensure_manager', unavailable)
        first = submit('wakeup-loss', .1)
    assert first['submission_status'] == 'accepted'
    assert first['job_status'] == 'queued'
    assert first['scheduling']['status'] == 'deferred'
    lookup = lookup_execution_submission(ExecutionSubmissionLookupRequest(submission_key='wakeup-loss'))
    assert first['receipt']['receipt_id'] in json.dumps(lookup)
    second = submit('wakeup-loss', .1)
    assert second['receipt']['receipt_id'] == first['receipt']['receipt_id']
    assert second['replayed'] is True
    job = first['job_id']
    until(lambda: managed.store.get_job(job)['state'] == 'success')
    assert len(managed.store.list_submissions()) == 1
    assert (managed._directory(job)/'stdout.log').read_text().count('launched') == 1


def test_concurrent_submissions_accept_once(managed):
    def accept(_): return managed.store.accept_submission(submission_key='concurrent', entity_type='job', request={'x':1})
    with ThreadPoolExecutor(6) as pool: receipts = list(pool.map(accept, range(12)))
    assert len({r.entity_id for r in receipts}) == 1
    assert sum(not r.replayed for r in receipts) == 1


def test_ambiguous_launch_never_restarts_or_releases_reservation(managed):
    receipt = managed.store.accept_submission(submission_key='ambiguous', entity_type='job', request={}, spec={'job_type':'native_software'})
    reservation = managed.store.directory / 'reserved.json'
    reservation.write_text('{}')
    managed.store.record_job_state(receipt.entity_id, 'launching', state_payload={'launch_token':'never-claimed','launch_time':0,'reservation_path':str(reservation)})
    for _ in range(3): result = managed.reconcile()
    assert result['summary']['needs_reconciliation'] == 1
    assert reservation.exists()
    assert not managed.store.get_record('launch_claim', receipt.entity_id)


def test_dead_supervisor_live_child_is_cancelled_without_resubmission(managed):
    job = submit('orphan', 15)['job_id']
    facts = until(lambda: (value if value.get('child_identity') else None) if (value := json.loads(managed.store.get_job(job)['state_json'])) else None)
    owner, child = facts['supervisor_identity'], facts['child_identity']
    os.kill(owner['pid'], signal.SIGKILL)
    until(lambda: not process_identity(owner['pid'], owner)['verified'])
    assert process_identity(child['pid'], child)['verified']
    until(lambda: managed.reconcile()['summary']['needs_reconciliation'])
    assert Path(facts['reservation_path']).exists()
    managed.cancel_entity(job)
    until(lambda: not process_identity(child['pid'], child)['verified'])
    assert len(managed.store.records('launch_claim')) == 1


def test_pid_reuse_is_never_signalled(managed):
    receipt = managed.store.accept_submission(submission_key='pid-reuse', entity_type='job', request={})
    identity = process_identity(os.getpid())
    wrong = {**identity, 'start_ticks':identity['start_ticks'] + 1}
    assert not process_identity(os.getpid(), wrong)['verified']
    managed.store.record_job_state(receipt.entity_id, 'queued')
    managed.store.record_job_state(receipt.entity_id, 'launching', state_payload={'supervisor_identity':wrong})
    assert managed.cancel_entity(receipt.entity_id)['signalled'] is False


def test_snapshot_hashes_frozen_copy_and_detects_toctou(managed, monkeypatch):
    path = managed.workspace / 'input.txt'; path.write_text('original')
    frozen, manifest = freeze_files(managed.store, [{'source_path':'input.txt','target_path':'input.txt'}])
    path.write_text('later')
    assert Path(frozen[0]['snapshot_path']).read_text() == 'original'
    import chemistry_toolbox.mcp.managed_execution as module
    copy = module.shutil.copyfileobj
    def changing(src, dst):
        copy(src, dst); path.write_text('concurrent mutation')
    monkeypatch.setattr(module.shutil, 'copyfileobj', changing)
    with pytest.raises(ValueError, match='input_changed'):
        freeze_files(managed.store, [{'source_path':'input.txt','target_path':'input.txt'}])


def test_terminal_state_cannot_regress(managed):
    receipt = managed.store.accept_submission(submission_key='state', entity_type='job', request={})
    managed.store.record_job_state(receipt.entity_id, 'failed')
    managed.store.record_job_state(receipt.entity_id, 'running')
    assert managed.store.get_job(receipt.entity_id)['state'] == 'failed'


def test_run_deadline_stops_child_even_when_manager_is_down(managed, monkeypatch):
    from datetime import datetime, timezone, timedelta
    monkeypatch.setenv('RESEARCHCHEMBENCH_RUN_DEADLINE', (datetime.now(timezone.utc) + timedelta(seconds=3)).isoformat())
    job = submit('deadline', 15)['job_id']
    until(lambda: json.loads(managed.store.get_job(job)['state_json']).get('child_identity'))
    manager_identity = managed.store.get_record('manager', 'identity')
    os.kill(manager_identity['pid'], signal.SIGKILL)
    until(lambda: managed.store.get_job(job)['state'] == 'timeout', seconds=8)
    ensure_manager(managed.store)
    until(lambda: not Path(json.loads(managed.store.get_job(job)['state_json'])['reservation_path']).exists())


def test_batch_item_mapping_and_events_survive_manager_restart(managed, monkeypatch):
    from chemistry_toolbox.mcp.discovery_models import ActionBatchRequest, ExecutionEventWaitRequest
    from chemistry_toolbox.mcp.async_action_tools import submit_action_batch_async, _read_events
    from chemistry_toolbox.mcp import managed_execution
    def mock_action_spec(action_id, request):
        # A real local process replaces only the scientific backend in this
        # fault fixture; acceptance, item mapping, queue and supervisor are real.
        label = request['inputs']['label']
        return {'job_type':'native_software','runtime':'core','command':[sys.executable,'-c',f'import time;print({label!r},flush=True);time.sleep(1.5)'],
                'stdin_target':None,'metadata':{},'resource_limits':{'cpu_cores':1,'memory_mb':128,'gpu_count':0,'walltime_seconds':10}}, [], []
    monkeypatch.setattr(managed_execution, 'action_spec', mock_action_spec)
    request = ActionBatchRequest(action_id='calculate_energy', backend_id='ase_emt', submission_key='batch1',
        items=[{'item_id':name,'inputs':{'label':name},'resource_limits':{'cpu_cores':1,'memory_mb':128}} for name in ('a','b','c')])
    batch = submit_action_batch_async(request)['batch_id']
    mapping = until(lambda: managed.store.get_record('batch_items', batch))
    until(lambda: managed.store.get_job(mapping['a'])['state'] == 'success' and managed.store.get_job(mapping['b'])['state'] == 'running')
    owner = managed.store.get_record('manager','identity'); os.kill(owner['pid'], signal.SIGKILL)
    until(lambda: not process_identity(owner['pid'],owner)['verified'])
    assert submit_action_batch_async(request)['batch_id'] == batch
    until(lambda: managed.store.get_job(batch)['state'] == 'success')
    assert managed.store.get_record('batch_items',batch) == mapping
    status = json.loads((managed.workspace / 'outputs/action_batches' / batch / 'status.json').read_text())
    assert len(status['events']) == 3
    assert [e['sequence'] for e in status['events']] == [1,2,3]
    for label, job in mapping.items():
        assert (managed._directory(job)/'stdout.log').read_text().strip() == label
    result = _read_events(ExecutionEventWaitRequest(batch_ids=[batch]), policy={'settle_seconds':1,'max_batch_seconds':1,'heartbeat_seconds':2,'poll_interval_seconds':1,'failure_tail_chars':100})
    assert result['status'] == 'success'
    assert {item['item_id']: item['job_id'] for item in result['newly_terminal_items']} == mapping
    assert all(item['batch_id'] == batch for item in result['state_transitions'])
    from evaluation.provenance.trace import load_tool_trace, process_metrics
    events = load_tool_trace(managed.workspace)
    events.append({'tool': 'wait_execution_events', 'status': 'success', 'result_preview': result})
    metrics = process_metrics(events, workspace=managed.workspace)
    assert metrics['managed_scientific_attempt_count'] == 3
    assert metrics['successful_managed_scientific_calls'] == 3
    assert metrics['submission_accepted_count'] == 1
    assert set(metrics['agent_observed_job_states']) == set(mapping.values())


def test_observation_requires_exact_result_receipt(managed):
    from chemistry_toolbox.mcp.open_tools import acknowledge_execution_result
    from chemistry_toolbox.mcp.execution_models import ExecutionResultObservationRequest
    job = submit('observe', .1)['job_id']
    until(lambda: managed.store.get_job(job)['state'] == 'success')
    result = collect_execution_job(JobCollectRequest(job_id=job))
    receipt = result['result_receipt_id']
    assert acknowledge_execution_result(ExecutionResultObservationRequest(job_id=job,result_receipt_id='result_'+'0'*32))['status'] == 'invalid_request'
    assert acknowledge_execution_result(ExecutionResultObservationRequest(job_id=job,result_receipt_id=receipt))['observed']
    assert managed.store.get_record('observation',job)['state'] == 'observed'


def test_cancel_between_reservation_and_launch_does_not_leak_resources(managed, monkeypatch):
    import chemistry_toolbox.mcp.job_manager as module
    from chemistry_toolbox.src.resource_budget import active_resource_usage
    spec = {'job_type':'native_software','resource_limits':{'cpu_cores':1,'memory_mb':128,'gpu_count':0},'command':[]}
    receipt = managed.store.accept_submission(submission_key='cancel-race',entity_type='job',request={},spec=spec)
    reserve = module.reserve_resources
    def cancel_during_reservation(*args, **kwargs):
        lease = reserve(*args, **kwargs)
        managed.store.record_job_state(receipt.entity_id,'cancelled')
        return lease
    monkeypatch.setattr(module,'reserve_resources',cancel_during_reservation)
    managed._dispatch(managed.store.get_job(receipt.entity_id))
    assert active_resource_usage()['cpu_cores'] == 0
    assert not managed.store.get_record('launch_claim',receipt.entity_id)


def test_workspace_status_is_not_terminal_authority(managed):
    receipt = managed.store.accept_submission(submission_key='projection',entity_type='job',request={},spec={})
    managed.store.record_job_state(receipt.entity_id,'launching',state_payload={'launch_token':'unknown','launch_time':0})
    directory = managed._directory(receipt.entity_id); directory.mkdir(parents=True)
    (directory/'status.json').write_text('{"status":"success"}')
    assert managed.reconcile()['summary']['needs_reconciliation'] == 1


def test_batch_cancel_waits_for_child_termination(managed):
    from chemistry_toolbox.src.resource_budget import resource_budget_record
    child = {'job_type':'native_software','runtime':'core','command':[sys.executable,'-c','import time; time.sleep(12)'],
             'metadata':{},'resource_limits':{'cpu_cores':1,'memory_mb':128,'gpu_count':0,'walltime_seconds':20},'frozen_inputs':[]}
    receipt = managed.store.accept_submission(submission_key='cancel-batch',entity_type='batch',entity_prefix='batch',request={},
        spec={'job_type':'batch','budget':resource_budget_record(),'children':[{'item_id':name,'spec':child} for name in ('a','b')]})
    ensure_manager(managed.store)
    mapping = until(lambda: managed.store.get_record('batch_items',receipt.entity_id))
    until(lambda: managed.store.get_job(mapping['a'])['state']=='running')
    managed.cancel_entity(receipt.entity_id,'batch')
    until(lambda: managed.store.get_job(receipt.entity_id)['state']=='cancelled')
    assert all(managed.store.get_job(job)['state']=='cancelled' for job in mapping.values())

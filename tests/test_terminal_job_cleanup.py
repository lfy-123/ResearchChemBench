import json
from types import SimpleNamespace

from evaluation.execution.lifecycle import RunLifecycleMixin


def test_ordinary_finalization_leaves_terminal_jobs_untouched(tmp_path):
    for index, state in enumerate(['partial_success', 'invalid_request', 'unsupported', 'unavailable']):
        path = tmp_path/'outputs/execution_jobs'/f'job_{index}'/'status.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'status':state}))
    runner = SimpleNamespace(workspace=tmp_path, recovery_enabled=False)
    result = RunLifecycleMixin._cancel_workspace_execution_jobs(runner, reason='fixture')
    assert result['already_terminal_jobs'] == 4
    assert result['active_jobs'] == result['cancelled_jobs'] == 0
    assert not list(tmp_path.rglob('cancel_requested'))


def test_cleanup_reports_unknown_state_instead_of_assuming_a_live_job(tmp_path):
    path = tmp_path/'outputs/execution_jobs/job_unknown/status.json'
    path.parent.mkdir(parents=True)
    path.write_text('{"status":"unrecognized"}')
    runner = SimpleNamespace(workspace=tmp_path, recovery_enabled=False)
    result = RunLifecycleMixin._cancel_workspace_execution_jobs(runner, reason='fixture')
    assert result['active_jobs'] == 0
    assert result['errors'][0]['stage'] == 'state_validation'
    assert json.loads(path.read_text())['status'] == 'unrecognized'

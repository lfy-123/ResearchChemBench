"""Cold-process pilot checks without a provider API or chemistry workload."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_task_package_v19 import package


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('extra,forwarded', [([], []), (['--timeout-seconds', '345600'], ['--timeout-seconds', '345600'])])
def test_pilot_resume_only_forwards_explicit_wall_budget(monkeypatch, tmp_path, extra, forwarded):
    from evaluation import pilot
    from evaluation.execution import control
    calls = []
    monkeypatch.setattr(control, 'main', lambda values: calls.append(values) or 0)
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', '--run-root', str(tmp_path), '--run-id', 'saved', *extra])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 0
    assert calls == [['resume', '--resume', '--run-root', str(tmp_path), '--run-id', 'saved', *forwarded]]


@pytest.mark.parametrize("explicit_output", [False, True])
@pytest.mark.parametrize("mode,paper_ids,corrupt", [
    ("autonomous_research", ["paper_alpha"], False),
    ("autonomous_research", ["paper_beta"], False),
    ("autonomous_research", ["paper_broken"], True),
    ("autonomous_research", ["paper_beta", "paper_alpha"], False),
    ("paper_reproduction", ["paper_beta", "paper_alpha"], False),
    ("autonomous_research", ["paper_alpha", "paper_broken"], True),
    ("paper_reproduction", ["paper_alpha", "paper_broken"], True),
])
def test_pilot_uses_selected_snapshot_in_fresh_process(tmp_path, mode, paper_ids, corrupt, explicit_output):
    project = tmp_path / "project"
    for paper_id in paper_ids:
        source = package(project / "tasks", paper_id=paper_id, task_type=mode)
        final = project / "tasks" / f"final_verified_{mode}" / paper_id
        final.parent.mkdir(parents=True, exist_ok=True)
        source.rename(final)
    if corrupt:
        (final / "agent_input/task.md").write_text("Changed without updating the manifest")

    # If settings are imported before the pilot configures its snapshot, this
    # unrelated package blocks startup and creates the wrong workspace root.
    unrelated = project / "tasks/autonomous_research/paper_unrelated"
    unrelated.mkdir(parents=True)
    (unrelated / "task_info.json").write_text("{}")
    stale_workspaces = tmp_path / "unselected-workspaces"
    output = tmp_path / "pilot-output" if explicit_output else project / "workspaces/codex_gpt56"
    calls = tmp_path / "provider-calls.jsonl"
    executable = tmp_path / "fake-codex"
    executable.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "with open(os.environ['PILOT_TEST_CALLS'], 'a') as handle:\n"
        "    handle.write(json.dumps(sys.argv[1:]) + '\\n')\n"
        "if sys.argv[1:] != ['--version']:\n"
        "    raise SystemExit('dry-run launched the Agent')\n"
        "print('codex-cli 0.154.0')\n"
    )
    executable.chmod(0o755)
    # Each batch child must load the pilot from this isolated project while
    # sharing the real implementation of the remaining evaluation modules.
    module = project / "evaluation"
    module.mkdir()
    (module / "__init__.py").write_text(f"__path__.append({str(ROOT / 'evaluation')!r})\n")
    shutil.copy2(ROOT / "evaluation/pilot.py", module / "pilot.py")
    if explicit_output:
        # An explicit new destination must override automatic discovery, even
        # when an existing unfinished run of the same paper is present.
        for paper_id in paper_ids:
            saved_pilot_run(project, paper=paper_id, mode=mode)
    (project / "sitecustomize.py").write_text(
        "import sys\n"
        "def no_network(event, args):\n"
        "    if event == 'socket.connect':\n"
        "        raise RuntimeError('dry-run attempted a network connection')\n"
        "sys.addaudithook(no_network)\n"
    )
    env = {**os.environ,
           "PYTHONPATH": os.pathsep.join((str(project), str(ROOT))),
           "RESEARCHCHEMBENCH_TASKS_DIR": str(project / "tasks"),
           "RESEARCHCHEMBENCH_TASK_ROOTS": str(project / "tasks"),
           "RESEARCHCHEMBENCH_WORKSPACES_DIR": str(stale_workspaces),
           "RCB_CODEX_EXECUTABLE": str(executable),
           "RCB_CODEX_API_KEY": "pilot-test-placeholder",
           "RCB_CODEX_BASE_URL": "http://127.0.0.1:1/v1",
           "RCB_CODEX_MODEL": "gpt-5.6-sol",
           "RCB_CODEX_REASONING_EFFORT": "high",
           "PILOT_TEST_CALLS": str(calls)}
    result = subprocess.run(
        [sys.executable, "-m", "evaluation.pilot", "--mode", mode, *paper_ids,
         "--resume", "--retry-in-doubt", "--dry-run", *(["--output-dir", str(output)] if explicit_output else [])],
        cwd=project, env=env, capture_output=True, text=True, timeout=60,
    )
    assert not stale_workspaces.exists(), result.stdout + result.stderr
    assert "paper_unrelated" not in result.stdout + result.stderr
    directories = [output] if explicit_output and len(paper_ids) == 1 else sorted(output.glob("paper_*"))
    if corrupt and len(paper_ids) > 1:
        assert result.returncode == 2
        assert "manifest_entries_mismatch" in result.stderr
        assert not output.exists()
        assert not calls.exists()  # All task packages are checked before the first launch.
    elif corrupt:
        assert result.returncode == 2
        assert len(directories) == 1
        submission = json.loads((directories[0] / "submission.json").read_text())
        assert submission["status"] == "preflight_failed"
        assert "manifest_entries_mismatch" in submission["error"]["message"]
        assert str(directories[0] / "task_snapshot") in submission["error"]["message"]
        assert not calls.exists()
    else:
        assert result.returncode == 0, result.stdout + result.stderr
        assert len(directories) == len(paper_ids)
        observed = []
        for directory in directories:
            settings = json.loads((directory / 'test_settings.json').read_text())
            assert len(settings['tasks']) == 1
            task = settings['tasks'][0]
            paper = task['paper_id']
            observed.append(paper)
            if not explicit_output or len(paper_ids) > 1:
                assert re.fullmatch(rf"{paper}_\d{{8}}_\d{{6}}_[a-f0-9]{{6}}", directory.name)
            reports = list((directory / "runs/cli_runs").glob("batch_*/eval_report.json"))
            assert len(reports) == 1
            report = json.loads(reports[0].read_text())
            assert report["config"]["resume"] is True
            assert report["config"]["judge"]["retry_in_doubt"] is True
            assert report["config"]["judge"]["max_in_doubt_retries"] == 1
            assert report["config"]["max_concurrent_runs"] == 1
            assert report["config"]["timeout_seconds"] == 345600
            assert report["config"]["tasks"] == [{"paper_id": paper, "task_type": mode}]
            assert [(row["task_type"], row["paper_id"], row["status"]) for row in report["runs"]] == [
                (mode, paper, "preflight_ready")]
            assert report["runs"][0]["api_verified"] is False and report["runs"][0]["workspace"] is None
            assert Path(task['source_task']).parent.name == f'final_verified_{mode}'
            assert Path(task['staged_task']).parent == directory / 'task_snapshot' / mode
        assert sorted(observed) == sorted(paper_ids)
        assert all(json.loads(line) == ["--version"] for line in calls.read_text().splitlines())


@pytest.mark.parametrize('first_exit,expected_exit,interrupted', [
    (0, 0, False), (4, 4, False), (-15, 143, True),
    ('interrupt', 130, True), ('terminate', 143, True),
])
def test_batch_waits_for_judge_and_stops_on_interrupt(tmp_path, first_exit, expected_exit, interrupted):
    project = tmp_path / 'project with spaces'
    module = project / 'evaluation'
    module.mkdir(parents=True)
    (module / '__init__.py').write_text('')
    # A small child replaces the API workload. It records Agent/Judge ordering,
    # and supports a real parent interrupt to exercise graceful queue shutdown.
    (module / 'pilot.py').write_text('''
import argparse, json, os, signal, sys, time
from pathlib import Path
args = sys.argv[1:]
parser = argparse.ArgumentParser()
parser.add_argument('paper')
for name in ('mode', 'output-dir', 'timeout-seconds', 'job-timeout-seconds', 'max-tokens', 'cpu-cores', 'memory-mb'):
    parser.add_argument('--' + name)
for name in ('resume', 'no-resume', 'dry-run', 'no-score'):
    parser.add_argument('--' + name, action='store_true')
parsed = parser.parse_args()
paper = parsed.paper
output = Path(parsed.output_dir)
output.mkdir(parents=True, exist_ok=False)
(output / 'arguments.json').write_text(json.dumps(args))
def record(stage):
    with Path('events.jsonl').open('a') as handle:
        handle.write(json.dumps([paper, stage]) + '\\n')
record('agent_start')
first_exit = json.loads(Path('first_exit.json').read_text()) if paper == 'paper_beta' else 0
if first_exit in ('interrupt', 'terminate'):
    def stop(*_):
        record('stopped')
        raise SystemExit(0)
    signal.signal(signal.SIGINT, stop)
    os.kill(os.getppid(), signal.SIGINT if first_exit == 'interrupt' else signal.SIGTERM)
    time.sleep(10)
    raise SystemExit('parent failed to forward interrupt')
if first_exit < 0:
    os.kill(os.getpid(), -first_exit)
record('agent_end')
record('judge_start')
time.sleep(0.05)
record('judge_end')
raise SystemExit(first_exit)
''')
    (project / 'first_exit.json').write_text(json.dumps(first_exit))
    args = SimpleNamespace(
        paper_ids=['paper_beta', 'paper_alpha'], mode='paper_reproduction', output_dir=None,
        dry_run=False, no_score=False, resume_enabled=True, timeout_seconds=123,
        job_timeout_seconds=60, max_tokens=456, cpu_cores=2, memory_mb=512,
        run_root=None, run_id=None,
    )
    parent = '''
import json, sys
from pathlib import Path
from types import SimpleNamespace
from evaluation.pilot import _run_sequential
raise SystemExit(_run_sequential(Path(sys.argv[1]), SimpleNamespace(**json.loads(sys.argv[2]))))
'''
    result = subprocess.run([sys.executable, '-c', parent, str(project), json.dumps(vars(args))],
                            cwd=ROOT, capture_output=True, text=True, timeout=30)
    assert result.returncode == expected_exit, result.stdout + result.stderr
    events = [json.loads(line) for line in (project / 'events.jsonl').read_text().splitlines()]
    if interrupted:
        assert all(paper == 'paper_beta' for paper, stage in events)
        if first_exit in ('interrupt', 'terminate'):
            assert events[-1] == ['paper_beta', 'stopped']
    else:
        assert events == [[paper, stage] for paper in args.paper_ids
                          for stage in ['agent_start', 'agent_end', 'judge_start', 'judge_end']]
    outputs = list((project / 'workspaces/codex_gpt56').iterdir())
    assert len(outputs) == (1 if interrupted else 2)
    for output in outputs:
        assert re.fullmatch(r'paper_(alpha|beta)_\d{8}_\d{6}_[a-f0-9]{6}', output.name)
        argv = json.loads((output / 'arguments.json').read_text())
        assert '--resume' in argv and '--no-score' not in argv and '--dry-run' not in argv
        for option, value in [('mode', 'paper_reproduction'), ('timeout-seconds', '123'),
                              ('job-timeout-seconds', '60'), ('max-tokens', '456'),
                              ('cpu-cores', '2'), ('memory-mb', '512')]:
            assert argv[argv.index('--' + option) + 1] == value


@pytest.mark.parametrize('arguments,diagnostic', [
    ([], 'at least one PAPER_ID'),
    (['--resume'], 'at least one PAPER_ID'),
    (['paper_alpha', 'paper_alpha'], 'Duplicate paper IDs'),
    (['../paper_alpha'], 'paper_<identifier>'),
    (['--mode', 'hold_verified_autonomous_research', 'paper_alpha'], 'invalid choice'),
    (['paper_alpha'], 'Final verified task not found'),
])
def test_invalid_or_hold_only_selection_creates_no_submission(tmp_path, monkeypatch, capsys, arguments, diagnostic):
    from evaluation import pilot
    monkeypatch.setattr(pilot, '__file__', str(tmp_path / 'evaluation/pilot.py'))
    # A task in the hold directory must never become an implicit fallback.
    held = tmp_path / 'tasks/hold_verified_autonomous_research/paper_alpha'
    held.mkdir(parents=True)
    (held / 'task_info.json').write_text('{}')
    output = tmp_path / 'output'
    monkeypatch.setattr(sys, 'argv', ['pilot', *arguments, '--dry-run', '--output-dir', str(output)])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 2
    assert diagnostic in capsys.readouterr().err
    assert not output.exists()


def test_existing_run_rejects_wrong_mode_without_changing_directory(tmp_path, monkeypatch):
    from evaluation import pilot
    from evaluation.execution import control, recovery
    monkeypatch.setattr(control, 'main', lambda *a: pytest.fail('must validate saved identity first'))
    monkeypatch.setattr(recovery, 'locate_workspace', lambda *a: tmp_path)
    monkeypatch.setattr(recovery, 'load_run_manifest', lambda *a: {'paper_id': 'paper_alpha', 'task_type': 'paper_reproduction'})
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', '--run-root', str(tmp_path), '--run-id', 'saved',
                                    '--mode', 'autonomous_research', 'paper_alpha'])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 2
    assert not list(tmp_path.iterdir())


def saved_pilot_run(project, *, paper='paper_alpha', mode='autonomous_research',
                    stamp='20260925_143450', suffix='saved', state='suspended_infrastructure'):
    """A portable saved identity; never starts an Agent or creates live controls."""
    from datetime import datetime, timezone
    run_id = f'{mode}-{paper}-codex-{stamp}-{suffix}'
    workspace = project / 'workspaces/codex_gpt56' / f'{paper}_{stamp}_{suffix}' / 'runs/cli_runs' / f'batch_{stamp}_{suffix}' / run_id
    (workspace / 'recovery').mkdir(parents=True)
    identity = {'run_id': run_id, 'paper_id': paper, 'task_type': mode, 'agent_key': 'codex',
                'timestamp': stamp, 'first_started_at': datetime.strptime(stamp, '%Y%m%d_%H%M%S').replace(tzinfo=timezone.utc).isoformat()}
    (workspace / '_meta.json').write_text(json.dumps({**identity, 'status': state}))
    (workspace / 'recovery/run.json').write_text(json.dumps({**identity, 'run_state': state,
        'schema_version': 2, 'agent_kind': 'codex', 'recovery_enabled': True,
        'config': {'timeout_seconds': 345600, 'execution_mode': 'local'}}))
    return workspace


def test_latest_run_uses_start_time_and_exact_identity_not_mtime(tmp_path):
    from evaluation.pilot import _latest_run
    older = saved_pilot_run(tmp_path)
    latest = saved_pilot_run(tmp_path, stamp='20260928_053052', state='running')
    saved_pilot_run(tmp_path, paper='paper_alphabet', stamp='20260929_000000')
    saved_pilot_run(tmp_path, mode='paper_reproduction', stamp='20260929_000000')
    # Touching an old run's output must not make it the latest evaluation.
    os.utime(older / '_meta.json', (2000000000, 2000000000))
    os.utime(latest / '_meta.json', (1, 1))
    # A newer dry-run has no actual run/session to resume.
    (tmp_path / 'workspaces/codex_gpt56/paper_alpha_20260929_120000_preview').mkdir()
    assert _latest_run(tmp_path, 'paper_alpha', 'autonomous_research') == latest
    assert _latest_run(tmp_path, 'paper_missing', 'autonomous_research') is None
    meta = json.loads((older / '_meta.json').read_text())
    meta.pop('first_started_at')
    (older / '_meta.json').write_text(json.dumps(meta))
    assert _latest_run(tmp_path, 'paper_alpha', 'autonomous_research') == latest


@pytest.mark.parametrize('defect', ['ambiguous', 'missing_meta', 'bad_identity', 'bad_json', 'missing_manifest'])
def test_auto_resume_refuses_uncertain_latest_without_fallback(tmp_path, monkeypatch, capsys, defect):
    from evaluation import pilot
    from evaluation.execution import control
    saved_pilot_run(tmp_path)
    latest = saved_pilot_run(tmp_path, stamp='20260928_053052')
    if defect == 'ambiguous':
        saved_pilot_run(tmp_path, stamp='20260928_053052', suffix='second')
    elif defect == 'missing_meta':
        (latest / '_meta.json').unlink()
    elif defect == 'bad_identity':
        meta = json.loads((latest / '_meta.json').read_text())
        meta['paper_id'] = 'paper_other'
        (latest / '_meta.json').write_text(json.dumps(meta))
    elif defect == 'bad_json':
        (latest / '_meta.json').write_text('{')
    else:
        (latest / 'recovery/run.json').unlink()
    before = sorted(str(p) for p in tmp_path.rglob('*'))
    monkeypatch.setattr(pilot, '__file__', str(tmp_path / 'evaluation/pilot.py'))
    monkeypatch.setattr(control, 'main', lambda *a: pytest.fail('must not resume older run'))
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', 'paper_alpha'])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 2
    assert capsys.readouterr().err
    assert before == sorted(str(p) for p in tmp_path.rglob('*'))


@pytest.mark.parametrize('extra,forwarded', [
    ([], []),
    (['--timeout-seconds', '345600'], []),
    (['--timeout-seconds=691200'], ['--timeout-seconds', '691200']),
    (['--no-score', '--retry-in-doubt'], ['--no-score', '--retry-in-doubt']),
])
@pytest.mark.parametrize('control_exit', [0, 2])
def test_auto_resume_routes_latest_and_preserves_saved_budget(tmp_path, monkeypatch, extra, forwarded, control_exit):
    from evaluation import pilot
    from evaluation.execution import control
    saved_pilot_run(tmp_path)
    latest = saved_pilot_run(tmp_path, stamp='20260928_053052')
    before = sorted(str(p) for p in tmp_path.rglob('*'))
    calls = []
    monkeypatch.setattr(pilot, '__file__', str(tmp_path / 'evaluation/pilot.py'))
    monkeypatch.setattr(control, 'main', lambda values: calls.append(values) or control_exit)
    # No current task package or API environment is needed to locate a frozen run.
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', 'paper_alpha', *extra])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == control_exit
    assert calls == [['resume', '--resume', '--run-root', str(latest), '--run-id', latest.name, *forwarded]]
    assert before == sorted(str(p) for p in tmp_path.rglob('*'))


@pytest.mark.parametrize('state,score_status,extra,expected', [
    ('suspended_infrastructure', None, ['--dry-run'], 'resume_preview'),
    ('completed', 'scored', [], 'Skipping'),
    ('completed', None, ['--no-score'], 'Skipping'),
])
def test_auto_resume_preview_and_finished_runs_are_read_only(tmp_path, monkeypatch, capsys, state, score_status, extra, expected):
    from evaluation import pilot
    from evaluation.execution import control
    workspace = saved_pilot_run(tmp_path, state=state)
    if score_status:
        (workspace / '_score.json').write_text(json.dumps({'evaluation_status': score_status, 'score': 81}))
    before = {str(p): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    monkeypatch.setattr(pilot, '__file__', str(tmp_path / 'evaluation/pilot.py'))
    monkeypatch.setattr(control, 'main', lambda *a: pytest.fail('must not start Agent or Judge'))
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', 'paper_alpha', *extra])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 0
    assert expected in capsys.readouterr().out
    assert before == {str(p): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


@pytest.mark.parametrize('scoring_status', [None, 'suspended_infrastructure', 'in_doubt'])
def test_auto_resume_completed_agent_continues_scoring(tmp_path, monkeypatch, scoring_status):
    from evaluation import pilot
    from evaluation.execution import control
    workspace = saved_pilot_run(tmp_path, state='completed')
    if scoring_status:
        # A later unfinished Judge attempt takes precedence over a published score.
        (workspace / '_score.json').write_text(json.dumps({'evaluation_status': 'scored', 'score': 81}))
        (workspace / '_scoring_attempt.json').write_text(json.dumps({'evaluation_status': scoring_status}))
    calls = []
    monkeypatch.setattr(pilot, '__file__', str(tmp_path / 'evaluation/pilot.py'))
    monkeypatch.setattr(control, 'main', lambda values: calls.append(values) or 0)
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', 'paper_alpha'])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 0
    assert calls == [['resume', '--resume', '--run-root', str(workspace), '--run-id', workspace.name]]


@pytest.mark.parametrize('option,value', [('cpu-cores', '2'), ('memory-mb', '1024'), ('job-timeout-seconds', '60'), ('max-tokens', '100')])
def test_auto_resume_rejects_changes_to_frozen_resources(tmp_path, monkeypatch, option, value):
    from evaluation import pilot
    from evaluation.execution import control
    saved_pilot_run(tmp_path)
    monkeypatch.setattr(pilot, '__file__', str(tmp_path / 'evaluation/pilot.py'))
    monkeypatch.setattr(control, 'main', lambda *a: pytest.fail('must retain original resources'))
    monkeypatch.setattr(sys, 'argv', ['pilot', '--resume', 'paper_alpha', '--' + option, value])
    with pytest.raises(SystemExit) as stopped:
        pilot.main()
    assert stopped.value.code == 2


def test_mixed_batch_resumes_starts_and_skips_without_resetting_saved_options(tmp_path, monkeypatch):
    from evaluation import pilot
    resumed = saved_pilot_run(tmp_path)
    done = saved_pilot_run(tmp_path, paper='paper_done', state='completed')
    (done / '_score.json').write_text('{"evaluation_status": "scored"}')
    calls = []

    class Child:
        def __init__(self, command, **kwargs):
            calls.append(command)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def wait(self):
            return 2 if '--run-id' in calls[-1] else 0

    monkeypatch.setattr(subprocess, 'Popen', Child)
    args = SimpleNamespace(paper_ids=['paper_alpha', 'paper_new', 'paper_done'], mode='autonomous_research',
        output_dir=None, dry_run=False, no_score=False, retry_in_doubt=False, resume_enabled=True,
        timeout_seconds=345600, job_timeout_seconds=86400, max_tokens=None, cpu_cores=48, memory_mb=204800,
        run_root=None, run_id=None)
    assert pilot._run_sequential(tmp_path, args, explicit_options={'--timeout-seconds'}) == 2
    assert len(calls) == 2
    assert calls[0] == [sys.executable, '-m', 'evaluation.pilot', '--resume', '--run-root', str(resumed), '--run-id', resumed.name]
    assert 'paper_new' in calls[1] and '--output-dir' in calls[1]
    assert '--timeout-seconds' in calls[1] and '--cpu-cores' in calls[1]
    assert '--run-id' not in calls[1]


@pytest.mark.parametrize('resume_enabled', [None, False])
def test_batch_without_resume_starts_new_even_with_saved_runs(tmp_path, monkeypatch, resume_enabled):
    from evaluation import pilot
    saved_pilot_run(tmp_path)
    calls = []

    class Child:
        def __init__(self, command, **kwargs):
            calls.append(command)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def wait(self):
            return 0

    monkeypatch.setattr(subprocess, 'Popen', Child)
    args = SimpleNamespace(paper_ids=['paper_alpha'], mode='autonomous_research',
        output_dir=None, dry_run=False, no_score=False, retry_in_doubt=False, resume_enabled=resume_enabled,
        timeout_seconds=345600, job_timeout_seconds=86400, max_tokens=None, cpu_cores=48, memory_mb=204800,
        run_root=None, run_id=None)
    assert pilot._run_sequential(tmp_path, args) == 0
    assert len(calls) == 1 and '--run-id' not in calls[0] and '--output-dir' in calls[0]


def test_auto_resume_dispatch_in_fresh_batch_children(tmp_path):
    """Real parent/child entrypoints route mixed work without provider calls."""
    project = tmp_path / 'project'
    old = saved_pilot_run(project, paper='paper_old')
    done = saved_pilot_run(project, paper='paper_done', state='completed')
    (done / '_score.json').write_text('{"evaluation_status": "scored"}')
    source = package(project / 'tasks', paper_id='paper_new', task_type='autonomous_research')
    final = project / 'tasks/final_verified_autonomous_research/paper_new'
    final.parent.mkdir(parents=True)
    source.rename(final)
    module = project / 'evaluation'
    module.mkdir()
    (module / '__init__.py').write_text(f'__path__.append({str(ROOT / "evaluation")!r})\n')
    shutil.copy2(ROOT / 'evaluation/pilot.py', module / 'pilot.py')
    execution = module / 'execution'
    execution.mkdir()
    (execution / '__init__.py').write_text(f'__path__.append({str(ROOT / "evaluation/execution")!r})\n')
    (execution / 'control.py').write_text('''
import json
from pathlib import Path
def main(values):
    with Path('calls.jsonl').open('a') as stream:
        stream.write(json.dumps({'kind': 'resume', 'values': values}) + '\\n')
    return 2  # A blocked resume must not replace this run or stop later papers.
''')
    (module / 'cli.py').write_text('''
import json
from pathlib import Path
def run_eval(config_path, **kwargs):
    config = json.loads(config_path.read_text())
    with Path('calls.jsonl').open('a') as stream:
        stream.write(json.dumps({'kind': 'new', 'config': config}) + '\\n')
    batch = config_path.parent / 'runs/cli_runs/batch_fixture'
    batch.mkdir(parents=True)
    (batch / 'eval_report.json').write_text(json.dumps({'runs': [{'score': 81}]}))
    return 0
''')
    (project / 'sitecustomize.py').write_text(
        "import sys\n"
        "def no_network(event, args):\n"
        "    if event == 'socket.connect':\n"
        "        raise RuntimeError('dispatch test attempted a network connection')\n"
        "sys.addaudithook(no_network)\n")
    env = {**os.environ, 'PYTHONPATH': os.pathsep.join((str(project), str(ROOT))),
           'RCB_CODEX_API_KEY': 'test-placeholder', 'RCB_CODEX_BASE_URL': 'http://127.0.0.1:1/v1',
           'RCB_CODEX_MODEL': 'gpt-5.6-sol', 'RCB_CODEX_REASONING_EFFORT': 'high'}
    result = subprocess.run([sys.executable, '-m', 'evaluation.pilot', '--resume', '--timeout-seconds', '345600',
                             'paper_old', 'paper_new', 'paper_done'],
                            cwd=project, env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 2, result.stdout + result.stderr
    calls = [json.loads(line) for line in (project / 'calls.jsonl').read_text().splitlines()]
    assert [call['kind'] for call in calls] == ['resume', 'new']
    assert calls[0]['values'] == ['resume', '--resume', '--run-root', str(old), '--run-id', old.name]
    assert calls[1]['config']['tasks'] == [{'paper_id': 'paper_new', 'task_type': 'autonomous_research'}]
    assert calls[1]['config']['resume'] is True
    assert len(list((project / 'workspaces/codex_gpt56').iterdir())) == 3
    assert 'Skipping paper_done' in result.stdout

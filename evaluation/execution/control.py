#!/usr/bin/env python3
"""Inspect or control one existing run without creating a replacement session."""
from __future__ import annotations
import argparse
import json
import os
import signal
import time
from datetime import datetime, timezone
from types import SimpleNamespace
from pathlib import Path

from chemistry_toolbox.mcp.job_manager import JobManager, ensure_manager
from chemistry_toolbox.src.recovery_io import file_lock, process_identity
from evaluation.execution.recovery import ControllerLock, RunRecoveryError, load_run_manifest, locate_workspace
from evaluation.execution.runner import TaskRunner
from ..settings import DEFAULT_LIVE_PROGRESS, DEFAULT_PROGRESS_CONSOLE
from .resume_policy import add_resume_arguments, add_repair_arguments, configure, retry_delay, execution_exit_code, policy_overrides


def refresh_batch(workspace, store):
    origin = store.get_record('batch', 'origin')
    if not origin: return
    from evaluation.provenance.results import run_completion_status, write_batch_results
    directory = Path(origin['directory'])
    with file_lock(store.directory.parent / 'batch_results.lock'):
        report_path = directory / 'eval_report.json'
        if report_path.is_file():
            report = json.loads(report_path.read_text())
            meta = json.loads((workspace / '_meta.json').read_text())
            score = json.loads((workspace / '_score.json').read_text()) if (workspace / '_score.json').is_file() else {}
            manifest = store.get_record('run', 'manifest', {})
            from evaluation.provenance.results import read_scoring_status
            scoring = read_scoring_status(workspace)
            for row in report.get('runs', []):
                if row.get('run_id') == store.run_id or row.get('workspace') == str(workspace):
                    row.update(status=manifest.get('run_state', meta['status']), error=manifest.get('error'), evaluation_status=scoring['evaluation_status'], score_error=scoring.get('evaluation_reason'), termination=meta.get('termination'), duration_seconds=meta.get('run_elapsed_seconds'),
                               completion_status=run_completion_status({**meta, **manifest}),
                               score=score.get('score'), score_max=score.get('score_max'), normalized_score=score.get('normalized_score'))
            from evaluation.cli import _write_batch_report
            _write_batch_report(directory, report['runs'], origin['config'])
        write_batch_results(directory, config=origin['config'])


def resume_scoring(workspace, config, *, resume_enabled=None, resume_policy=None):
    """Resume the native Judge session independently of the research session."""
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    from evaluation.scoring.service import apply_judge_configuration, score_workspace, read_json, SCORING_IMPLEMENTATION
    from .recovery_lifecycle import _cooldown
    from .progress import LiveProgressReporter
    store = ExecutionStore(workspace, run_id=Path(workspace).name)
    with ControllerLock(store.directory / "controller.lock"):
        manifest = store.get_record("run", "manifest", {})
        if manifest and manifest.get("run_state") != "completed":
            raise RunRecoveryError("agent_not_completed")
        store.put_record("controller", "identity", process_identity(os.getpid()))
        display = {**manifest.get("config", {}), **config}
        reporter = LiveProgressReporter(Path(workspace), Path(workspace).name,
            enabled=display.get("live_progress", DEFAULT_LIVE_PROGRESS),
            console=display.get("progress_console", DEFAULT_PROGRESS_CONSOLE))
        reporter.emit("JUDGE_START")
        result = {}
        try:
            apply_judge_configuration(config)
            policy = configure(store, resume_enabled, resume_policy)
            state = store.get_record("resume", "state", {})
            context = SimpleNamespace(workspace=Path(workspace), run_id=store.run_id,
                deadline_at=manifest.get("deadline_at"), _stop_requested=False, progress_interval=5)
            while True:
                latest = read_json(Path(workspace) / "_scoring_attempt.json")
                kwargs = {}
                if latest:
                    directory = latest.get("scoring_directory")
                    saved = read_json(Path(directory) / "config.json") if directory else {}
                    if saved.get("scoring_implementation") != SCORING_IMPLEMENTATION:
                        raise RunRecoveryError("Create a new native Judge scoring version; old API scoring cannot resume")
                    kwargs = {"output_dir": directory, "resume": True}
                result = score_workspace(workspace, **kwargs)
                store.put_record("evaluation", "current", result)
                if result.get("evaluation_status") != "suspended_infrastructure":
                    return result
                delay, reason = retry_delay(result.get("provider_error"), policy, state)
                if delay is None or not context.deadline_at:
                    return result
                state.update(stage="judge", next_retry_at=time.time() + delay,
                    wait_budget_used_seconds=state.get("wait_budget_used_seconds", 0) + delay, stop_reason=None)
                store.put_record("resume", "state", state)
                if not _cooldown(context, state):
                    return result
                state.update(next_retry_at=None, automatic_attempts=state.get("automatic_attempts", 0) + 1)
                store.put_record("resume", "state", state)
        finally:
            store.put_record("controller", "identity", {})
            reporter.emit("JUDGE_END", status=result.get("evaluation_status", "interrupted"),
                          score=result.get("score"), error=result.get("error"))
            reporter.close()


def revalidate(workspace, *, apply=False):
    """Repair a proven format-only finalization failure; never launch a process."""
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    from chemistry_toolbox.src.execution_states import TERMINAL_STATES
    from chemistry_toolbox.src.recovery_io import atomic_json
    from .output_contract import validate_saved_submission
    from .recovery import write_run_manifest
    from ..provenance.results import write_workspace_results
    workspace = Path(workspace).resolve()
    store = ExecutionStore.open_existing(workspace)
    if store is None:
        raise RunRecoveryError("revalidation_requires_saved_control_records")
    with ControllerLock(store.directory / 'controller.lock'):
        meta = json.loads((workspace / '_meta.json').read_text())
        manifest = store.get_record('run', 'manifest', {})
        previous = store.get_record('repair', 'submission_validation')
        if previous and apply:
            # Finish an interrupted publication from the same audited decision.
            if meta not in (previous['before_meta'], previous['after_meta']) or manifest not in (previous['before_manifest'], previous['after_manifest']):
                raise RunRecoveryError('run_changed_since_revalidation')
            updated, updated_manifest = previous['after_meta'], previous['after_manifest']
        else:
            if meta.get('status') != 'failed' or manifest.get('run_state') != 'failed':
                raise RunRecoveryError('revalidation_requires_failed_terminal_run')
            if meta.get('exit_code') != 0 or meta.get('termination') not in {'agent_completed', 'process_exit'} or meta.get('error'):
                raise RunRecoveryError('failure_not_proven_to_be_submission_only')
            if meta.get('agent_kind') == 'external' and meta.get('external_protocol_validation', {}).get('valid') is not True:
                raise RunRecoveryError('external_protocol_validation_failed')
            if any(j.get('state') not in TERMINAL_STATES for j in store.list_jobs()):
                raise RunRecoveryError('jobs_not_terminal')
            facts = meta.get('execution_reconciliation', {})
            summary = facts.get('summary', {})
            if facts.get('status') != 'success' or summary.get('active') != 0 or summary.get('needs_reconciliation') != 0:
                raise RunRecoveryError('finalization_was_not_reconciled')
            task = store.directory / 'task_snapshot' / meta['task_type'] / meta['paper_id']
            if not task.is_dir():
                raise RunRecoveryError('original_task_snapshot_unavailable')
            validation = validate_saved_submission(workspace, task)
            # The legacy global report rule is a saved finalization fact. Do not
            # manufacture evidence of compliance if its old observation is absent.
            valid = validation['valid'] and meta.get('report_exists') is True
            result = {'valid': valid, 'applied': False, 'submission_validation': validation,
                      'previous_status': meta['status'], 'proposed_status': 'completed' if valid else 'failed'}
            if not apply or not valid:
                return result
            updated = {**meta, 'status': 'completed', 'submission_validation': validation,
                       'submission_findings': validation['errors'], 'required_deliverable_status': validation['checked_files'],
                       'status_correction': 'public_submission_revalidation'}
            updated_manifest = {**manifest, 'run_state': 'completed', 'phase': 'completed',
                                'status_correction': 'public_submission_revalidation'}
        writer = ExecutionStore(workspace, run_id=store.run_id)
        if not previous:
            writer.put_record('repair', 'submission_validation', {
                'at': datetime.now(timezone.utc).isoformat(), 'before_meta': meta, 'before_manifest': manifest,
                'after_meta': updated, 'after_manifest': updated_manifest}, immutable=True)
        atomic_json(workspace / '_meta.json', updated)
        writer.put_record('run', 'manifest', updated_manifest)
        write_run_manifest(workspace, updated_manifest)
        atomic_json(workspace / 'recovery/run.json', updated_manifest)
        write_workspace_results(workspace)
        refresh_batch(workspace, writer)
        return {'valid': True, 'applied': True, 'status': 'completed', 'submission_validation': updated['submission_validation']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('status','reconcile','resume','pause','cancel','revalidate','finalize'))
    parser.add_argument('--apply', action='store_true', help='Apply a verified revalidation/finalization; otherwise preview.')
    parser.add_argument('--stop-completed-processes', action='store_true', help='With finalize --apply, retire verified controller/CLI remnants only after native completion and terminal jobs are proven.')
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--run-root', '--recovery-root', dest='run_root', type=Path, required=True)
    parser.add_argument('--no-score', action='store_true')
    parser.add_argument('--human', action='store_true', help='Read-only compact progress for status; default remains JSON')
    parser.add_argument('--json', action='store_true', help='Explicit JSON output (default)')
    add_resume_arguments(parser)
    add_repair_arguments(parser)
    parser.add_argument('--timeout-seconds', type=int, help='Explicitly extend the saved total wall-time budget, measured from the original start. Requires an idle job manager and no active jobs.')
    args = parser.parse_args(argv)
    if args.apply and args.command not in {'revalidate', 'finalize'}:
        parser.error('--apply requires revalidate or finalize')
    if args.stop_completed_processes and (args.command != 'finalize' or not args.apply):
        parser.error('--stop-completed-processes requires finalize --apply')
    if args.command != 'resume' and (args.resume_enabled is not None or args.timeout_seconds is not None or args.repair_history or args.resume_cancelled or policy_overrides(args)):
        parser.error('resume policy flags require the resume command')
    if (args.repair_history or args.resume_cancelled) and args.resume_enabled is not True:
        parser.error('--repair-history and --resume-cancelled require --resume')
    try:
        workspace = locate_workspace(args.run_root.expanduser().resolve(), args.run_id)
        manifest = load_run_manifest(workspace)
        if args.command == 'finalize':
            from .finalization_recovery import finalize_completed
            result = finalize_completed(workspace, apply=args.apply, stop_completed_processes=args.stop_completed_processes)
            if args.apply and result['status'] == 'completed' and not args.no_score:
                from chemistry_toolbox.mcp.execution_store import ExecutionStore
                store = ExecutionStore.open_existing(workspace)
                config = store.get_record('batch', 'origin', {}).get('config', {})
                if config.get('judge', {}).get('enabled', False):
                    result['score'] = resume_scoring(workspace, config)
                    result['evaluation_status'] = result['score'].get('evaluation_status', 'unknown')
                    refresh_batch(workspace, store)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return execution_exit_code(result['status'], result.get('evaluation_status')) if args.apply else 0
        if args.command == 'revalidate':
            print(json.dumps(revalidate(workspace, apply=args.apply), ensure_ascii=False, indent=2))
            return 0
        if args.command == 'status':
            from chemistry_toolbox.mcp.execution_store import ExecutionStore
            from evaluation.provenance.progress_snapshot import build_progress_snapshot, format_progress_summary
            snapshot = build_progress_snapshot(workspace)
            if args.human and not args.json:
                print(format_progress_summary(snapshot))
                return 0
            if not manifest.get('recovery_enabled'):
                print(json.dumps({'manifest':manifest,'recovery_capability':False, 'progress':snapshot}, ensure_ascii=False, indent=2))
                return 0
            store = ExecutionStore(workspace, run_id=args.run_id, read_only=True)
            result = {'status':'success', 'jobs':store.list_jobs(), 'control':store.get_record('control','current'),
                      'attempts':store.records('attempt'), 'usage':store.usage(), 'recovery_capability':True,
                      'progress':snapshot}
            print(json.dumps({'manifest':manifest, 'result':result}, ensure_ascii=False, indent=2))
            return 0
        manager = JobManager(workspace, run_id=args.run_id)
        store = manager.store
        if args.command == 'reconcile':
            ensure_manager(store)
            with file_lock(store.directory / 'reconcile.lock'):
                result = manager.reconcile()
        elif args.command in {'pause','cancel'}:
            if args.command == 'pause' and manifest.get('agent_kind') == 'external':
                raise RunRecoveryError('external_pause_unsupported; use cancel to stop the run')
            store.put_record('control','current', {'command':args.command,'source':'operator_cli'})
            ensure_manager(store)
            result = {'status':'success','run_id':args.run_id,'control':args.command,'accepted':True}
        else:
            if args.resume_enabled and (manifest.get('agent_kind') not in {'codex', 'mock', 'gemini', 'claude'} or manifest.get('config', {}).get('execution_mode') != 'local'):
                raise RunRecoveryError('resume_unsupported')
            if args.timeout_seconds is None and not (args.repair_history or args.resume_cancelled) and manifest.get('run_state') in {'completed', 'failed', 'cancelled', 'budget_exhausted'}:
                result = {**manifest, 'status': manifest['run_state']}
            else:
                repair = {name: True for name in ('repair_history', 'resume_cancelled') if getattr(args, name)}
                runner = TaskRunner.restore(args.run_id, recovery_root=args.run_root, timeout_seconds=args.timeout_seconds, **repair)
                runner.resume_enabled = args.resume_enabled
                if policy_overrides(args):
                    runner.resume_policy = {**store.get_record("resume", "policy", {}).get("limits", {}), **policy_overrides(args)}
                previous_sigint = signal.signal(signal.SIGINT, lambda *_: runner.request_stop())
                try:
                    result = runner.run()
                finally:
                    signal.signal(signal.SIGINT, previous_sigint)
            origin = store.get_record('batch','origin', {})
            if result['status'] == 'completed' and not args.no_score and origin.get('config',{}).get('judge',{}).get('enabled',False):
                score = resume_scoring(workspace, origin['config'], resume_enabled=args.resume_enabled, resume_policy=policy_overrides(args))
                result.update(score=score, evaluation_status=score.get('evaluation_status', 'unknown'))
            refresh_batch(workspace, store)
        print(json.dumps({'manifest':load_run_manifest(workspace), 'result':result}, ensure_ascii=False, indent=2))
        return execution_exit_code(result.get('status'), result.get('evaluation_status')) if args.command == 'resume' else 0
    except (RunRecoveryError, ValueError, OSError) as exc:
        print(json.dumps({'status':'recovery_blocked','error':str(exc),'automatic_restart':False}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Inspect or control one existing run without creating a replacement session."""
from __future__ import annotations
import argparse
import json
import os
import time
from datetime import datetime, timezone
from types import SimpleNamespace
from pathlib import Path

from chemistry_toolbox.mcp.job_manager import JobManager, ensure_manager
from chemistry_toolbox.src.recovery_io import file_lock, process_identity
from evaluation.execution.recovery import ControllerLock, RunRecoveryError, load_run_manifest, locate_workspace
from evaluation.execution.runner import TaskRunner
from .resume_policy import add_resume_arguments, configure, retry_delay, execution_exit_code


def refresh_batch(workspace, store):
    origin = store.get_record('batch', 'origin')
    if not origin: return
    from evaluation.provenance.results import write_batch_results
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
                               score=score.get('score'), score_max=score.get('score_max'), normalized_score=score.get('normalized_score'))
            from evaluation.cli import _write_batch_report
            _write_batch_report(directory, report['runs'], origin['config'])
        write_batch_results(directory, config=origin['config'])


def resume_scoring(workspace, config, *, resume_enabled=None, retry_in_doubt=None):
    """Continue the recorded scoring version, holding one controller across cooling."""
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    from evaluation.scoring.service import apply_judge_configuration, score_workspace, read_json
    from .recovery_lifecycle import _cooldown
    store = ExecutionStore(workspace, run_id=Path(workspace).name)
    with ControllerLock(store.directory / "controller.lock"):
        manifest = store.get_record("run", "manifest", {})
        if manifest and manifest.get("run_state") != "completed":
            raise RunRecoveryError("agent_not_completed")
        store.put_record("controller", "identity", process_identity(os.getpid()))
        try:
            policy = configure(store, resume_enabled)
            retry_policy = store.get_record("evaluation", "retry_policy", {})
            allow_ambiguous = retry_in_doubt if retry_in_doubt is not None else retry_policy.get("retry_in_doubt", config.get("judge", {}).get("retry_in_doubt", False))
            maximum_ambiguous = config.get("judge", {}).get("max_in_doubt_retries", 1)
            if not isinstance(allow_ambiguous, bool) or isinstance(maximum_ambiguous, bool) or not isinstance(maximum_ambiguous, int) or maximum_ambiguous < 0:
                raise ValueError("Invalid Judge retry policy")
            store.put_record("evaluation", "retry_policy", {"retry_in_doubt": allow_ambiguous, "max_in_doubt_retries": maximum_ambiguous})
            manual_retry = retry_in_doubt is True
            apply_judge_configuration(config)
            state = store.get_record("resume", "state", {})
            if not policy["enabled"] and state.get("next_retry_at"):
                state.update(next_retry_at=None, stop_reason="disabled_by_operator")
                store.put_record("resume", "state", state)
            context = SimpleNamespace(workspace=Path(workspace), run_id=store.run_id,
                                      deadline_at=manifest.get("deadline_at"), _stop_requested=False, progress_interval=5)
            pending = policy["enabled"] and state.get("stage") == "judge" and state.get("next_retry_at")
            while True:
                scheduled_ambiguous = False
                if pending:
                    if not _cooldown(context, state):
                        state.update(next_retry_at=None, stop_reason="control_or_deadline")
                        store.put_record("resume", "state", state)
                        return {"evaluation_status": "suspended_infrastructure", "error": "Judge retry stopped by control or original deadline"}
                    scheduled_ambiguous = bool(state.get("judge_retry_in_doubt")) and allow_ambiguous
                    state.update(next_retry_at=None, judge_retry_in_doubt=False,
                                 automatic_attempts=state.get("automatic_attempts", 0) + 1)
                    store.put_record("resume", "state", state)
                latest = read_json(Path(workspace) / "_scoring_attempt.json") or read_json(Path(workspace) / "_score.json")
                kwargs = {}
                if latest:
                    directory = latest.get("scoring_directory")
                    if not directory or not latest.get("score_id"):
                        raise RunRecoveryError("scoring_identity_missing; specify an explicit scoring version")
                    saved = read_json(Path(directory) / "config.json")
                    if saved.get("score_id") != latest["score_id"] or saved.get("run_id") != store.run_id:
                        raise RunRecoveryError("scoring_identity_mismatch")
                    kwargs = {"output_dir": directory, "resume": True, "budget": saved["budget"],
                              "rules_root": saved.get("rules_root"), "evidence_max_chars": saved["evidence_max_chars"]}
                result = score_workspace(workspace, retry_in_doubt=manual_retry or scheduled_ambiguous, **kwargs)
                manual_retry = False
                store.put_record("evaluation", "current", result)
                ambiguous = result.get("evaluation_status") == "in_doubt"
                if ambiguous and (not allow_ambiguous or state.get("judge_in_doubt_retries", 0) >= maximum_ambiguous):
                    state.update(next_retry_at=None, stop_reason="ambiguous_retry_not_enabled" if not allow_ambiguous else "ambiguous_retry_limit")
                    store.put_record("resume", "state", state)
                    return result
                if result.get("evaluation_status") not in {"suspended_infrastructure", "in_doubt"}:
                    return result
                # A killed client may leave a request with no response or provider
                # exception. Explicit ambiguity permission also covers that case.
                retry_error = result.get("provider_error") or ({"retryable": True} if ambiguous else None)
                delay, reason = retry_delay(retry_error, policy, state)
                if delay is None:
                    state.update(next_retry_at=None, stop_reason=reason)
                    store.put_record("resume", "state", state)
                    return result
                if not context.deadline_at:
                    return result
                state.update(stage="judge", next_retry_at=time.time() + delay,
                             judge_retry_in_doubt=ambiguous,
                             judge_in_doubt_retries=state.get("judge_in_doubt_retries", 0) + int(ambiguous),
                             wait_budget_used_seconds=state.get("wait_budget_used_seconds", 0) + delay, stop_reason=None)
                store.put_record("resume", "state", state)
                pending = True
        finally:
            store.put_record("controller", "identity", {})


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
    parser.add_argument('command', choices=('status','reconcile','resume','pause','cancel','revalidate'))
    parser.add_argument('--apply', action='store_true', help='Apply a proven submission-only correction; revalidate otherwise previews.')
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--run-root', '--recovery-root', dest='run_root', type=Path, required=True)
    parser.add_argument('--no-score', action='store_true')
    parser.add_argument('--human', action='store_true', help='Read-only compact progress for status; default remains JSON')
    parser.add_argument('--json', action='store_true', help='Explicit JSON output (default)')
    add_resume_arguments(parser)
    parser.add_argument('--retry-in-doubt', action='store_true', default=None, help='Explicitly permit retrying an uncertain Judge request.')
    parser.add_argument('--timeout-seconds', type=int, help='Explicitly extend the saved total wall-time budget, measured from the original start. Requires an idle job manager and no active jobs.')
    args = parser.parse_args(argv)
    if args.apply and args.command != 'revalidate':
        parser.error('--apply requires revalidate')
    if args.command != 'resume' and (args.resume_enabled is not None or args.retry_in_doubt or args.timeout_seconds is not None):
        parser.error('resume policy flags require the resume command')
    try:
        workspace = locate_workspace(args.run_root.expanduser().resolve(), args.run_id)
        manifest = load_run_manifest(workspace)
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
            if args.resume_enabled and (manifest.get('agent_kind') not in {'codex', 'mock'} or manifest.get('config', {}).get('execution_mode') != 'local'):
                raise RunRecoveryError('resume_unsupported')
            if args.timeout_seconds is None and manifest.get('run_state') in {'completed', 'failed', 'cancelled', 'budget_exhausted'}:
                result = {**manifest, 'status': manifest['run_state']}
            else:
                runner = TaskRunner.restore(args.run_id, recovery_root=args.run_root, timeout_seconds=args.timeout_seconds)
                runner.resume_enabled = args.resume_enabled
                result = runner.run()
            origin = store.get_record('batch','origin', {})
            if result['status'] == 'completed' and not args.no_score and origin.get('config',{}).get('judge',{}).get('enabled',False):
                score = resume_scoring(workspace, origin['config'], resume_enabled=args.resume_enabled, retry_in_doubt=args.retry_in_doubt)
                result.update(score=score, evaluation_status=score.get('evaluation_status', 'unknown'))
            refresh_batch(workspace, store)
        print(json.dumps({'manifest':load_run_manifest(workspace), 'result':result}, ensure_ascii=False, indent=2))
        return execution_exit_code(result.get('status'), result.get('evaluation_status')) if args.command == 'resume' else 0
    except (RunRecoveryError, ValueError, OSError) as exc:
        print(json.dumps({'status':'recovery_blocked','error':str(exc),'automatic_restart':False}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

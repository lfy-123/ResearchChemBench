"""CLI for single-task and batch ResearchChemBench agent evaluation."""

from __future__ import annotations

import argparse
import json
import signal
import statistics
from collections import Counter
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from chemistry_toolbox.src.catalog import resolve_tool_discovery_mode

from .execution.progress import progress_timestamp
from .execution.runner import TaskRunner
from .execution.provider_errors import normalize_error
from .execution.resume_policy import add_resume_arguments, execution_exit_code
from .provenance.results import write_batch_results
from .schemas.eval_config import EvalConfigError, RunSpec, load_yaml, resolve_specs, resolve_task_repository
from .settings import (
    AGENT_PRESETS,
    DEFAULT_AGENT_TIMEOUT_SECONDS,
    DEFAULT_AVAILABLE_CPU_CORES,
    DEFAULT_AVAILABLE_GPU_COUNT,
    DEFAULT_AVAILABLE_MEMORY_MB,
    DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
    DEFAULT_EXECUTION_MODE,
    DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
    DEFAULT_JOB_EVENT_MAX_BATCH_SECONDS,
    DEFAULT_JOB_EVENT_SETTLE_SECONDS,
    DEFAULT_JOB_FAILURE_TAIL_CHARS,
    DEFAULT_JOB_INTERNAL_POLL_INTERVAL_SECONDS,
    DEFAULT_JOB_WAIT_HEARTBEAT_SECONDS,
    DEFAULT_LIVE_PROGRESS,
    DEFAULT_MAX_TURNS,
    DEFAULT_MCP_TOOL_TIMEOUT_MS,
    DEFAULT_PROGRESS_CONSOLE,
    DEFAULT_PROGRESS_MAX_CHARS,
    WORKSPACES_DIR,
)

_load_yaml = load_yaml


def _log(message: str, *, stream=None) -> None:
    """Print one timestamped batch-level line."""

    print(
        f"[RCB][{progress_timestamp()}][BATCH] {message}",
        file=stream if stream is not None else sys.stdout,
        flush=True,
    )


def _normalize_bool(value: Any, *, name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in {0, 1}:
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise EvalConfigError(f"{name} must be a boolean")


def _positive_integer(value: Any, *, name: str) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise EvalConfigError(f"{name} must be an integer") from exc
    if normalized < 1:
        raise EvalConfigError(f"{name} must be positive")
    return normalized


def _nonnegative_integer(value: Any, *, name: str) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise EvalConfigError(f"{name} must be an integer") from exc
    if normalized < 0:
        raise EvalConfigError(f"{name} must be non-negative")
    return normalized


def _write_batch_report(batch_dir: Path, rows: list[dict[str, Any]], config: dict) -> Path:
    scores = [float(row["score"]) for row in rows if row.get("score") is not None]
    normalized_scores = [
        float(row["normalized_score"])
        for row in rows
        if row.get("normalized_score") is not None
    ]
    score_maxima = {
        float(row["score_max"])
        for row in rows
        if row.get("score") is not None and row.get("score_max") is not None
    }
    summary = {
        "runs": len(rows),
        "completed": sum(row.get("status") == "completed" for row in rows),
        "failed": sum(row.get("status") == "failed" for row in rows),
        **{state: sum(row.get("status") == state for row in rows) for state in (
            "suspended_infrastructure", "recovery_blocked", "cancelled", "budget_exhausted")},
        "scored": len(scores),
        "score_coverage": {"scored": len(scores), "total": len(rows)},
        "evaluation_states": dict(Counter(row.get("evaluation_status", "not_started") for row in rows)),
        "unscored_reasons": dict(Counter(row.get("score_error") or row.get("evaluation_status", "not_started")
                                         for row in rows if row.get("score") is None)),
        "mean_score": statistics.mean(scores) if scores and len(score_maxima) == 1 else None,
        "score_max": next(iter(score_maxima)) if len(score_maxima) == 1 else None,
        "mean_normalized_score": (
            statistics.mean(normalized_scores) if normalized_scores else None
        ),
        "pass_rate": (
            statistics.mean(scores)
            if scores and score_maxima == {1.0}
            else None
        ),
    }
    json_path = batch_dir / "eval_report.json"
    json_path.write_text(
        json.dumps({"config": config, "summary": summary, "runs": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# ResearchChemBench Evaluation Report",
        "",
        f"- Runs: {summary['runs']}",
        f"- Completed: {summary['completed']}",
        f"- Failed: {summary['failed']}",
        f"- Scored: {summary['scored']}/{summary['runs']}",
        f"- Unscored reasons: {json.dumps(summary['unscored_reasons'], ensure_ascii=False)}",
        f"- Mean score: {summary['mean_score'] if summary['mean_score'] is not None else 'N/A'}",
        f"- Score maximum: {summary['score_max'] if summary['score_max'] is not None else 'mixed/N/A'}",
        f"- Mean normalized score: {summary['mean_normalized_score'] if normalized_scores else 'N/A'}",
        "",
        "| Task | Agent | Repeat | Status | Score | Duration (s) | Run ID |",
        "|---|---|---:|---|---:|---:|---|",
    ]
    for row in rows:
        score_text = (
            ""
            if row.get("score") is None
            else f"{row['score']}/{row.get('score_max', 1)}"
        )
        lines.append(
        f"| {row['task_type']}/{row['paper_id']} | {row['agent_key']} | {row['repeat']} | "
            f"{row['status']} | {score_text} | "
            f"{row.get('duration_seconds', '')} | {row['run_id']} |"
        )
    markdown_path = batch_dir / "eval_report.md"
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return markdown_path


def run_eval(config_path: Path, *, dry_run: bool = False, no_score: bool = False, resume: bool | None = None,
             agent_key: str | None = None) -> int:
    config = _load_yaml(config_path)
    if agent_key is not None:
        config["agents"] = [agent_key]
    if resume is not None:
        config["resume"] = resume
    config.setdefault("judge", {}).setdefault("enabled", True)
    if no_score:
        config["judge"]["enabled"] = False
    from .scoring.service import apply_judge_configuration
    apply_judge_configuration(config)
    discovery_mode = resolve_tool_discovery_mode(config.get("tool_discovery_mode"))
    from .agent_plugins.registry import AgentConfigError, resolve_agent_definitions
    from .repository import TaskRepositoryError
    try:
        registry = resolve_agent_definitions(config, config_dir=config_path.resolve().parent)
        task_repository = resolve_task_repository(config, config_dir=config_path.resolve().parent)
        specs = resolve_specs(config, agent_registry=registry, task_repository=task_repository)
    except (AgentConfigError, TaskRepositoryError) as exc:
        raise EvalConfigError(str(exc)) from exc
    workers = int(config.get("max_concurrent_runs", 1))
    if workers < 1:
        raise EvalConfigError("max_concurrent_runs must be >= 1")
    live_progress = _normalize_bool(
        config.get("live_progress", DEFAULT_LIVE_PROGRESS),
        name="live_progress",
    )
    progress_console = _normalize_bool(
        config.get("progress_console", DEFAULT_PROGRESS_CONSOLE),
        name="progress_console",
    )
    try:
        progress_max_chars = int(
            config.get("progress_max_chars", DEFAULT_PROGRESS_MAX_CHARS)
        )
    except (TypeError, ValueError) as exc:
        raise EvalConfigError("progress_max_chars must be an integer") from exc
    if progress_max_chars < 80:
        raise EvalConfigError("progress_max_chars must be >= 80")
    agent_timeout_seconds = _positive_integer(
        config.get("timeout_seconds", DEFAULT_AGENT_TIMEOUT_SECONDS),
        name="timeout_seconds",
    )
    compute_action_timeout_seconds = _positive_integer(
        config.get(
            "compute_action_timeout_seconds",
            DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
        ),
        name="compute_action_timeout_seconds",
    )
    fast_action_timeout_seconds = _positive_integer(
        config.get("fast_action_timeout_seconds", DEFAULT_FAST_ACTION_TIMEOUT_SECONDS),
        name="fast_action_timeout_seconds",
    )
    mcp_tool_timeout_seconds = _positive_integer(
        config.get(
            "mcp_tool_timeout_seconds",
            (DEFAULT_MCP_TOOL_TIMEOUT_MS + 999) // 1000,
        ),
        name="mcp_tool_timeout_seconds",
    )
    available_cpu_cores = _positive_integer(
        config.get("available_cpu_cores", DEFAULT_AVAILABLE_CPU_CORES),
        name="available_cpu_cores",
    )
    available_memory_mb = _positive_integer(
        config.get("available_memory_mb", DEFAULT_AVAILABLE_MEMORY_MB),
        name="available_memory_mb",
    )
    if available_memory_mb < 128:
        raise EvalConfigError("available_memory_mb must be >= 128")
    available_gpu_count = _nonnegative_integer(
        config.get("available_gpu_count", DEFAULT_AVAILABLE_GPU_COUNT),
        name="available_gpu_count",
    )
    job_event_settle_seconds = _positive_integer(
        config.get("job_event_settle_seconds", DEFAULT_JOB_EVENT_SETTLE_SECONDS),
        name="job_event_settle_seconds",
    )
    job_event_max_batch_seconds = _positive_integer(
        config.get(
            "job_event_max_batch_seconds", DEFAULT_JOB_EVENT_MAX_BATCH_SECONDS
        ),
        name="job_event_max_batch_seconds",
    )
    default_job_wait_heartbeat_seconds = min(
        DEFAULT_JOB_WAIT_HEARTBEAT_SECONDS, mcp_tool_timeout_seconds - 1
    )
    job_wait_heartbeat_seconds = _positive_integer(
        config.get(
            "job_wait_heartbeat_seconds", default_job_wait_heartbeat_seconds
        ),
        name="job_wait_heartbeat_seconds",
    )
    job_internal_poll_interval_seconds = _positive_integer(
        config.get(
            "job_internal_poll_interval_seconds",
            DEFAULT_JOB_INTERNAL_POLL_INTERVAL_SECONDS,
        ),
        name="job_internal_poll_interval_seconds",
    )
    job_failure_tail_chars = _positive_integer(
        config.get("job_failure_tail_chars", DEFAULT_JOB_FAILURE_TAIL_CHARS),
        name="job_failure_tail_chars",
    )
    execution_mode = str(config.get("execution_mode", DEFAULT_EXECUTION_MODE)).strip().casefold()
    if execution_mode not in {"local", "distributed"}:
        raise EvalConfigError("execution_mode must be local or distributed")
    if fast_action_timeout_seconds > compute_action_timeout_seconds:
        raise EvalConfigError(
            "fast_action_timeout_seconds cannot exceed compute_action_timeout_seconds"
        )
    if mcp_tool_timeout_seconds <= compute_action_timeout_seconds:
        raise EvalConfigError(
            "mcp_tool_timeout_seconds must exceed compute_action_timeout_seconds"
        )
    if job_event_max_batch_seconds < job_event_settle_seconds:
        raise EvalConfigError(
            "job_event_max_batch_seconds must be >= job_event_settle_seconds"
        )
    if job_wait_heartbeat_seconds < job_event_max_batch_seconds:
        raise EvalConfigError(
            "job_wait_heartbeat_seconds must be >= job_event_max_batch_seconds"
        )
    if mcp_tool_timeout_seconds <= job_wait_heartbeat_seconds:
        raise EvalConfigError(
            "mcp_tool_timeout_seconds must exceed job_wait_heartbeat_seconds"
        )
    if dry_run:
        _log("Local preflight only; API availability and balance are unverified.")
    batch_id = (
        "batch_"
        + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + "_"
        + uuid.uuid4().hex[:6]
    )
    batch_dir = WORKSPACES_DIR / "cli_runs" / batch_id
    batch_dir.mkdir(parents=True, exist_ok=False)
    active: list[TaskRunner] = []
    stop_requested = threading.Event()

    def stop_active(_signum=None, _frame=None):
        stop_requested.set()
        for runner in list(active):
            runner.request_stop()

    previous_sigint = signal.signal(signal.SIGINT, stop_active)

    def failure_row(spec, exc, runner=None):
        from .execution.recovery import load_run_manifest
        started = runner is not None and runner.process is not None
        manifest = {}
        if runner and runner.workspace.exists():
            try:
                manifest = load_run_manifest(runner.workspace)
            except (ValueError, OSError, RuntimeError):
                pass
        completed = manifest.get("run_state") == "completed"
        status = "completed" if completed else "failed" if started else "preflight_failed"
        phase = "judge" if completed else "execution" if started else "preflight"
        error = normalize_error(exc, source=phase)
        if runner and runner.workspace.exists() and not completed:
            # A partially materialized workspace must not remain deceptively ready.
            try:
                runner._persist_run_manifest(run_state=status, error=error, phase=phase)
                runner._write_meta(status, {"error": error, "phase": phase})
            except (ValueError, OSError):
                pass  # The batch record below still preserves the original failure.
        return {"paper_id": spec.paper_id, "task_type": spec.task_type, "agent_key": spec.agent_key,
                "repeat": spec.repeat, "run_id": runner.run_id if runner else None,
                "workspace": str(runner.workspace) if runner and runner.meta_path.exists() else None,
                "status": status, "phase": phase, "evaluation_status": "needs_review" if completed else "not_started",
                "score": None, "error": error, "score_error": error["message"] if completed else "", "api_verified": False,
                "provider_diagnostics": getattr(exc, "diagnostics", getattr(runner, "_provider_diagnostics", None))}

    from chemistry_toolbox.src.recovery_io import atomic_json
    atomic_json(batch_dir / "planned_runs.json", {"created_at": datetime.now(timezone.utc).isoformat(), "config_source": str(config_path), "phase": "preflight", "api_verified": False, "runs": [vars(spec) for spec in specs]})
    def run_one(spec: RunSpec) -> dict[str, Any]:
        runner = None
        try:
            runner = TaskRunner(
                spec.paper_id,
                task_type=spec.task_type,
                agent_key=spec.agent_key,
                **({"agent_definition": registry[spec.agent_key]} if registry[spec.agent_key].get("kind") == "external" else {}),
                **({"task_repository": task_repository} if task_repository is not None else {}),
                workspace_root=batch_dir,
                timeout_seconds=agent_timeout_seconds,
                compute_action_timeout_seconds=compute_action_timeout_seconds,
                fast_action_timeout_seconds=fast_action_timeout_seconds,
                mcp_tool_timeout_ms=mcp_tool_timeout_seconds * 1000,
                available_cpu_cores=available_cpu_cores,
                available_memory_mb=available_memory_mb,
                available_gpu_count=available_gpu_count,
                job_event_settle_seconds=job_event_settle_seconds,
                job_event_max_batch_seconds=job_event_max_batch_seconds,
                job_wait_heartbeat_seconds=job_wait_heartbeat_seconds,
                job_internal_poll_interval_seconds=job_internal_poll_interval_seconds,
                job_failure_tail_chars=job_failure_tail_chars,
                max_turns=int(config.get("max_turns", DEFAULT_MAX_TURNS)),
                tool_discovery_mode=discovery_mode,
                live_progress=live_progress,
                progress_console=progress_console,
                progress_max_chars=progress_max_chars,
                execution_mode=execution_mode,
                recovery_enabled=_normalize_bool(config["recovery_enabled"], name="recovery_enabled") if "recovery_enabled" in config else None,
                resume=_normalize_bool(config.get("resume", False), name="resume"),
                resume_policy=config.get("resume_policy"),
                codex_model=config.get("codex_model"),
                codex_base_url=config.get("codex_base_url"),
                codex_reasoning_effort=config.get("codex_reasoning_effort"),
                max_tokens=config.get("max_tokens"),
                model_wait_strategy=config.get("model_wait_strategy", "provider_default"),
                feedback_schema_version=int(config.get("feedback_schema_version", 2)),
                native_input_validation_policy=config.get("native_input_validation_policy", "advisory"),
                archive_policy=config.get("archive_policy", "indexed"),
                progress_interval=int(config.get("progress_interval", 5)),
            )
            active.append(runner)
            if dry_run:
                return {"paper_id": spec.paper_id, "task_type": spec.task_type, "agent_key": spec.agent_key,
                        "repeat": spec.repeat, "run_id": None, "workspace": None, "status": "preflight_ready",
                        "api_verified": False, "provider_diagnostics": runner._provider_diagnostics}
            if runner.recovery_enabled:
                runner.setup_workspace()
                from .execution.recovery import runner_store
                runner_store(runner).put_record("batch", "origin", {"directory": str(batch_dir), "config": config}, immutable=True)
            meta = runner.run()
            score = None
            score_max = None
            normalized_score = None
            criteria = []
            objective_issue_flags = []
            judge_consistency_warnings = []
            score_error = ""
            evaluation_status = "not_started"
            if meta.get("status") == "completed" and not no_score and config.get("judge", {}).get("enabled", True):
                from .execution.control import resume_scoring
                score_result = resume_scoring(runner.workspace, config)
                evaluation_status = score_result.get("evaluation_status", "unknown")
                if score_result.get("error"):
                    score_error = str(score_result["error"])
                else:
                    score = score_result.get("score")
                    score_max = score_result.get("score_max")
                    normalized_score = score_result.get("normalized_score")
                    criteria = score_result.get("criteria", [])
                    objective_issue_flags = score_result.get(
                        "objective_issue_flags", []
                    )
                    judge_consistency_warnings = score_result.get(
                        "judge_consistency_warnings", []
                    )
            return {
                "paper_id": spec.paper_id,
                "task_type": spec.task_type,
                "agent_key": spec.agent_key,
                "repeat": spec.repeat,
                "run_id": runner.run_id,
                "status": meta.get("status", "failed"),
                "score": score,
                "evaluation_status": evaluation_status,
                "score_max": score_max,
                "normalized_score": normalized_score,
                "criteria": criteria,
                "objective_issue_flags": objective_issue_flags,
                "judge_consistency_warnings": judge_consistency_warnings,
                "score_error": score_error,
                "duration_seconds": meta.get("duration_seconds"),
                "error": meta.get("error"),
                "workspace": str(runner.workspace),
            }
        except Exception as exc:
            return failure_row(spec, exc, runner)
        finally:
            if runner in active:
                active.remove(runner)

    rows: list[dict[str, Any]] = []
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures: dict[Any, RunSpec] = {}
            next_spec_index = 0

            def submit_next() -> bool:
                nonlocal next_spec_index
                if stop_requested.is_set() or next_spec_index >= len(specs):
                    return False
                spec = specs[next_spec_index]
                next_spec_index += 1
                futures[executor.submit(run_one, spec)] = spec
                return True

            for _ in range(min(workers, len(specs))):
                submit_next()
            while futures:
                future = next(as_completed(tuple(futures)))
                spec = futures.pop(future)
                try:
                    row = future.result()
                except Exception as exc:
                    row = failure_row(spec, exc)
                rows.append(row)
                _write_batch_report(batch_dir, rows, config)
                _log(
                    f"[{len(rows)}/{len(specs)}] {row['task_type']}/{row['paper_id']} "
                    f"{row['agent_key']} "
                    f"status={row['status']} score={row.get('score')} run={row['run_id']}"
                )
                _log(
                    f"workspace={row['workspace']} "
                    + (
                        f"progress_log={row['workspace']}/_live_progress.log"
                        if live_progress
                        else "progress_log=disabled"
                    )
                )
                submit_next()
            if stop_requested.is_set():
                for spec in specs[next_spec_index:]:
                    rows.append(
                        {
                            "paper_id": spec.paper_id,
                            "task_type": spec.task_type,
                            "agent_key": spec.agent_key,
                            "repeat": spec.repeat,
                            "run_id": None,
                            "status": "cancelled",
                            "score": None,
                            "score_max": None,
                            "normalized_score": None,
                            "criteria": [],
                            "objective_issue_flags": [],
                            "judge_consistency_warnings": [],
                            "score_error": "batch stop requested before run started",
                            "duration_seconds": 0.0,
                            "workspace": None,
                        }
                    )
                    _log(
                        f"skipped={spec.task_type}/{spec.paper_id} "
                        f"agent={spec.agent_key} repeat={spec.repeat} "
                        "reason=batch_stop_requested"
                    )
    finally:
        signal.signal(signal.SIGINT, previous_sigint)

    rows.sort(
        key=lambda row: (
            row["task_type"], row["paper_id"], row["agent_key"], row["repeat"]
        )
    )
    report = _write_batch_report(batch_dir, rows, config)
    write_batch_results(batch_dir, config=config)
    _log(f"Batch directory: {batch_dir}")
    _log(f"Evaluation report: {report}")
    _log(f"Results summary: {batch_dir / 'results.json'}")
    if dry_run:
        return 0 if all(row["status"] == "preflight_ready" for row in rows) else 2
    codes = [execution_exit_code(row["status"], row.get("evaluation_status")) for row in rows]
    return next((code for code in (2, 1, 3, 4) if code in codes), 0)


def main(argv: list[str] | None = None) -> int:
    values = list(argv if argv is not None else sys.argv[1:])
    if values and values[0] in {"status", "reconcile", "resume", "pause", "cancel"}:
        from .execution.control import main as manage
        return manage(values)
    if values and values[0] == "create":
        argv = values[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, nargs="?")
    parser.add_argument("--paper-id")
    parser.add_argument("--task-type")
    parser.add_argument("--agent", help="Built-in agent or an agent_definitions key in CONFIG")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-score", action="store_true")
    add_resume_arguments(parser)
    parser.add_argument('--run-root', type=Path)
    parser.add_argument('--run-id')
    args = parser.parse_args(argv)
    if args.run_root is not None or args.run_id is not None:
        if not (args.run_root and args.run_id) or args.resume_enabled is not True:
            parser.error('Existing run requires --resume, --run-root and --run-id')
        if args.config or args.paper_id or args.task_type or args.agent or args.dry_run:
            parser.error('Existing run cannot be combined with new-run configuration')
        from .execution.control import main as manage
        return manage(['resume', '--resume', '--run-root', str(args.run_root), '--run-id', args.run_id]
                      + (['--no-score'] if args.no_score else []))

    temporary: Path | None = None
    if args.config:
        config_path = args.config.resolve()
    elif args.paper_id and args.task_type and args.agent:
        if args.agent not in AGENT_PRESETS:
            parser.error("custom agents require a CONFIG containing agent_definitions")
        WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
        temporary = WORKSPACES_DIR / f".single_run_config_{uuid.uuid4().hex[:8]}.yaml"
        temporary.write_text(
            yaml.safe_dump(
                {
                    "name": "single_run",
                    "agents": [args.agent],
                    "tasks": [
                        {"paper_id": args.paper_id, "task_type": args.task_type}
                    ],
                    "repeats": 1,
                    "max_concurrent_runs": 1,
                    "judge": {"enabled": not args.no_score},
                }
            ),
            encoding="utf-8",
        )
        config_path = temporary
    else:
        parser.error(
            "provide CONFIG or --paper-id, --task-type and --agent"
        )

    try:
        return run_eval(config_path, dry_run=args.dry_run, no_score=args.no_score, resume=args.resume_enabled,
                        **({"agent_key": args.agent} if args.config and args.agent else {}))
    except EvalConfigError as exc:
        _log(f"Configuration error: {exc}", stream=sys.stderr)
        return 2
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())

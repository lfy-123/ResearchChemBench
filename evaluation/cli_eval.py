"""CLI for single-task and batch ResearchChemBench agent evaluation."""

from __future__ import annotations

import argparse
import json
import signal
import statistics
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from researchchem_toolbox.catalog import resolve_tool_discovery_mode

from .config import (
    AGENT_PRESETS,
    DEFAULT_AVAILABLE_CPU_CORES,
    DEFAULT_AVAILABLE_GPU_COUNT,
    DEFAULT_AVAILABLE_MEMORY_MB,
    DEFAULT_AGENT_TIMEOUT_SECONDS,
    DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
    DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
    DEFAULT_LIVE_PROGRESS,
    DEFAULT_MCP_TOOL_TIMEOUT_MS,
    DEFAULT_MAX_TURNS,
    DEFAULT_PROGRESS_CONSOLE,
    DEFAULT_PROGRESS_MAX_CHARS,
    WORKSPACES_DIR,
)
from .live_progress import progress_timestamp
from .results import write_batch_results
from .run_task import TaskRunner
from .score import score_workspace
from .utils import list_tasks


class EvalConfigError(ValueError):
    """Raised for invalid batch evaluation configuration."""


@dataclass(frozen=True)
class RunSpec:
    task_id: str
    agent_key: str
    repeat: int


def _log(message: str, *, stream=None) -> None:
    """Print one timestamped batch-level line."""

    print(
        f"[RCB][{progress_timestamp()}][BATCH] {message}",
        file=stream if stream is not None else sys.stdout,
        flush=True,
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError as exc:
        raise EvalConfigError(f"Config not found: {path}") from exc
    if not isinstance(value, dict):
        raise EvalConfigError("Evaluation config must be a YAML mapping")
    return value


def _normalize_list(value: Any, *, name: str) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise EvalConfigError(f"{name} must be a string or list of strings")


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


def resolve_specs(config: dict[str, Any]) -> list[RunSpec]:
    agents = _normalize_list(config.get("agents", ["mock"]), name="agents")
    for agent in agents:
        if agent not in AGENT_PRESETS:
            raise EvalConfigError(f"Unknown agent {agent!r}; valid: {sorted(AGENT_PRESETS)}")

    raw_tasks = config.get("tasks", "all")
    tasks = list_tasks() if raw_tasks == "all" else _normalize_list(raw_tasks, name="tasks")
    known_tasks = set(list_tasks())
    unknown = [task for task in tasks if task not in known_tasks]
    if unknown:
        raise EvalConfigError(f"Unknown tasks: {unknown}")

    repeats = int(config.get("repeats", 1))
    if repeats < 1:
        raise EvalConfigError("repeats must be >= 1")
    return [
        RunSpec(task, agent, repeat)
        for task in tasks
        for agent in agents
        for repeat in range(1, repeats + 1)
    ]


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
        "failed": sum(row.get("status") != "completed" for row in rows),
        "scored": len(scores),
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
        f"- Scored: {summary['scored']}",
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
            f"| {row['task_id']} | {row['agent_key']} | {row['repeat']} | "
            f"{row['status']} | {score_text} | "
            f"{row.get('duration_seconds', '')} | {row['run_id']} |"
        )
    markdown_path = batch_dir / "eval_report.md"
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return markdown_path


def run_eval(config_path: Path, *, dry_run: bool = False, no_score: bool = False) -> int:
    config = _load_yaml(config_path)
    discovery_mode = resolve_tool_discovery_mode(config.get("tool_discovery_mode"))
    specs = resolve_specs(config)
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
    if fast_action_timeout_seconds > compute_action_timeout_seconds:
        raise EvalConfigError(
            "fast_action_timeout_seconds cannot exceed compute_action_timeout_seconds"
        )
    if mcp_tool_timeout_seconds <= compute_action_timeout_seconds:
        raise EvalConfigError(
            "mcp_tool_timeout_seconds must exceed compute_action_timeout_seconds"
        )
    if dry_run:
        _log(f"Config: {config_path}")
        _log(f"Planned runs: {len(specs)}")
        _log(f"Max concurrent runs: {workers}")
        _log(f"Tool discovery mode: {discovery_mode}")
        _log(f"Live progress: {live_progress}")
        _log(f"Progress console: {progress_console}")
        _log(f"Progress max chars: {progress_max_chars}")
        _log(
            "Timeouts: "
            f"fast_action={fast_action_timeout_seconds}s "
            f"compute_action={compute_action_timeout_seconds}s "
            f"mcp_tool={mcp_tool_timeout_seconds}s "
            f"agent={agent_timeout_seconds}s"
        )
        _log(
            "Per-task resource budget: "
            f"cpu={available_cpu_cores} "
            f"memory={available_memory_mb}MiB "
            f"gpu={available_gpu_count}"
        )
        for spec in specs:
            _log(f"run={spec.task_id} agent={spec.agent_key} repeat={spec.repeat}")
        return 0

    batch_id = (
        "batch_"
        + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + "_"
        + uuid.uuid4().hex[:6]
    )
    batch_dir = WORKSPACES_DIR / "cli_runs" / batch_id
    batch_dir.mkdir(parents=True, exist_ok=False)
    active: list[TaskRunner] = []

    def stop_active(_signum=None, _frame=None):
        for runner in list(active):
            runner.request_stop()

    previous_sigint = signal.signal(signal.SIGINT, stop_active)

    def run_one(spec: RunSpec) -> dict[str, Any]:
        runner = TaskRunner(
            spec.task_id,
            agent_key=spec.agent_key,
            workspace_root=batch_dir,
            timeout_seconds=agent_timeout_seconds,
            compute_action_timeout_seconds=compute_action_timeout_seconds,
            fast_action_timeout_seconds=fast_action_timeout_seconds,
            mcp_tool_timeout_ms=mcp_tool_timeout_seconds * 1000,
            available_cpu_cores=available_cpu_cores,
            available_memory_mb=available_memory_mb,
            available_gpu_count=available_gpu_count,
            max_turns=int(config.get("max_turns", DEFAULT_MAX_TURNS)),
            tool_discovery_mode=discovery_mode,
            live_progress=live_progress,
            progress_console=progress_console,
            progress_max_chars=progress_max_chars,
        )
        active.append(runner)
        try:
            meta = runner.run()
            score = None
            score_max = None
            normalized_score = None
            criteria = []
            objective_issue_flags = []
            judge_consistency_warnings = []
            score_error = ""
            if meta.get("status") == "completed" and not no_score and config.get("judge", {}).get("enabled", True):
                score_result = score_workspace(runner.workspace)
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
                "task_id": spec.task_id,
                "agent_key": spec.agent_key,
                "repeat": spec.repeat,
                "run_id": runner.run_id,
                "status": meta.get("status", "failed"),
                "score": score,
                "score_max": score_max,
                "normalized_score": normalized_score,
                "criteria": criteria,
                "objective_issue_flags": objective_issue_flags,
                "judge_consistency_warnings": judge_consistency_warnings,
                "score_error": score_error,
                "duration_seconds": meta.get("duration_seconds"),
                "workspace": str(runner.workspace),
            }
        except Exception as exc:
            return {
                "task_id": spec.task_id,
                "agent_key": spec.agent_key,
                "repeat": spec.repeat,
                "run_id": runner.run_id,
                "status": "failed",
                "score": None,
                "score_max": None,
                "normalized_score": None,
                "criteria": [],
                "objective_issue_flags": [],
                "judge_consistency_warnings": [],
                "score_error": f"{type(exc).__name__}: {exc}",
                "duration_seconds": None,
                "workspace": str(runner.workspace),
            }
        finally:
            if runner in active:
                active.remove(runner)

    rows: list[dict[str, Any]] = []
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(run_one, spec) for spec in specs]
            for future in as_completed(futures):
                row = future.result()
                rows.append(row)
                _log(
                    f"[{len(rows)}/{len(specs)}] {row['task_id']} {row['agent_key']} "
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
    finally:
        signal.signal(signal.SIGINT, previous_sigint)

    rows.sort(key=lambda row: (row["task_id"], row["agent_key"], row["repeat"]))
    report = _write_batch_report(batch_dir, rows, config)
    write_batch_results(batch_dir, config=config)
    _log(f"Batch directory: {batch_dir}")
    _log(f"Evaluation report: {report}")
    _log(f"Results summary: {batch_dir / 'results.json'}")
    return 0 if all(row["status"] == "completed" for row in rows) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, nargs="?")
    parser.add_argument("--task")
    parser.add_argument("--agent", choices=sorted(AGENT_PRESETS))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-score", action="store_true")
    args = parser.parse_args(argv)

    temporary: Path | None = None
    if args.config:
        config_path = args.config.resolve()
    elif args.task and args.agent:
        temporary = WORKSPACES_DIR / f".single_run_config_{uuid.uuid4().hex[:8]}.yaml"
        temporary.write_text(
            yaml.safe_dump(
                {
                    "name": "single_run",
                    "agents": [args.agent],
                    "tasks": [args.task],
                    "repeats": 1,
                    "max_concurrent_runs": 1,
                    "judge": {"enabled": not args.no_score},
                }
            ),
            encoding="utf-8",
        )
        config_path = temporary
    else:
        parser.error("provide CONFIG or both --task and --agent")

    try:
        return run_eval(config_path, dry_run=args.dry_run, no_score=args.no_score)
    except EvalConfigError as exc:
        _log(f"Configuration error: {exc}", stream=sys.stderr)
        return 2
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())

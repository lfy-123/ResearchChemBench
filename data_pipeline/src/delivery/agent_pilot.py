from __future__ import annotations

import statistics
import sys
from pathlib import Path
from typing import Any

from src.core.paths import DEFAULT_BENCHMARK_ROOT


def run_agent_pilot(
    task_dir: str | Path,
    workspace_root: str | Path,
    config: dict[str, Any],
    *,
    benchmark_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run configured parent-benchmark agents before human task approval.

    The task stays in the pipeline staging directory. Solver and judge credentials
    are inherited from the environment used by the parent ResearchChemBench runner.
    """

    task_dir = Path(task_dir).resolve()
    workspace_root = Path(workspace_root).resolve()
    benchmark = Path(benchmark_root).resolve() if benchmark_root else DEFAULT_BENCHMARK_ROOT
    root = str(benchmark)
    if root not in sys.path:
        sys.path.insert(0, root)

    import evaluation.run_task as run_task
    import evaluation.score as score
    import evaluation.utils as utils

    agents = config.get("agents") or []
    if not agents:
        raise ValueError("agent pilot config requires a non-empty agents list")
    scoring_enabled = bool(config.get("score", True))
    old_run_tasks = run_task.TASKS_DIR
    old_utils_tasks = utils.TASKS_DIR
    run_task.TASKS_DIR = task_dir.parent
    utils.TASKS_DIR = task_dir.parent
    runs: list[dict[str, Any]] = []
    try:
        for specification in agents:
            agent_key = str(specification["agent_key"])
            repeats = max(1, int(specification.get("repeats", 1)))
            for repeat in range(repeats):
                record: dict[str, Any] = {
                    "agent_key": agent_key,
                    "repeat": repeat + 1,
                }
                try:
                    runner = run_task.TaskRunner(
                        task_dir.name,
                        agent_key=agent_key,
                        workspace_root=workspace_root,
                        timeout_seconds=int(specification.get("timeout_seconds", 14_400)),
                        max_turns=int(specification.get("max_turns", 100)),
                        live_progress=False,
                        progress_console=False,
                    )
                    meta = runner.run()
                    record.update(
                        {
                            "run_id": runner.run_id,
                            "workspace": str(runner.workspace),
                            "status": meta.get("status"),
                            "exit_code": meta.get("exit_code"),
                            "duration_seconds": meta.get("duration_seconds"),
                            "required_deliverable_status": meta.get(
                                "required_deliverable_status", []
                            ),
                        }
                    )
                    if scoring_enabled and meta.get("status") == "completed":
                        scored = score.score_workspace(runner.workspace)
                        record["score"] = scored
                        record["normalized_score"] = scored.get("normalized_score")
                        if scored.get("error"):
                            record["score_error"] = scored["error"]
                except Exception as exc:
                    record.update(
                        {
                            "status": "pilot_error",
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
                runs.append(record)
    finally:
        run_task.TASKS_DIR = old_run_tasks
        utils.TASKS_DIR = old_utils_tasks

    return {
        "task_id": task_dir.name,
        "scoring_enabled": scoring_enabled,
        "runs": runs,
        "summary": _pilot_summary(runs, config),
    }


def _pilot_summary(runs: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    completed = [item for item in runs if item.get("status") == "completed"]
    scores = [
        float(item["normalized_score"]) for item in runs if item.get("normalized_score") is not None
    ]
    easy_threshold = float(config.get("too_easy_threshold", 0.85))
    hard_threshold = float(config.get("potentially_infeasible_threshold", 0.15))
    easy_fraction = float(config.get("too_easy_fraction", 0.67))
    if not scores:
        decision = "incomplete_no_valid_scores"
        reasons = [
            "configure a real solver and judge model before using the pilot as a quality gate"
        ]
    else:
        fraction_easy = sum(score >= easy_threshold for score in scores) / len(scores)
        if fraction_easy >= easy_fraction:
            decision = "review_too_easy"
            reasons = [f"{fraction_easy:.0%} of valid runs scored at least {easy_threshold:.2f}"]
        elif max(scores) <= hard_threshold:
            decision = "review_potentially_infeasible"
            reasons = [f"all valid runs scored at most {hard_threshold:.2f}"]
        else:
            decision = "pass_to_human_review"
            reasons = []
    return {
        "decision": decision,
        "reasons": reasons,
        "attempted_runs": len(runs),
        "completed_runs": len(completed),
        "valid_scores": len(scores),
        "minimum_normalized_score": min(scores) if scores else None,
        "median_normalized_score": statistics.median(scores) if scores else None,
        "maximum_normalized_score": max(scores) if scores else None,
        "score_range": (max(scores) - min(scores)) if scores else None,
    }

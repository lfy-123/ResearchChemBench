"""Stable machine-readable summaries for completed benchmark runs and batches."""

from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .token_usage import workspace_token_usage


RESULTS_SCHEMA_VERSION = 1


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _agent_usage(workspace: Path) -> dict[str, Any]:
    try:
        usage = workspace_token_usage(workspace)
    except (FileNotFoundError, OSError, ValueError):
        return {
            "available": False,
            "model_step_count": 0,
            "session_count": 0,
            "cost": 0.0,
            "tokens": {
                "input": 0,
                "cache_read": 0,
                "cache_write": 0,
                "output": 0,
                "reasoning": 0,
                "total": 0,
            },
        }
    return {
        "available": True,
        "model_step_count": usage.get("model_step_count", 0),
        "session_count": usage.get("session_count", 0),
        "cost": usage.get("cost", 0.0),
        "tokens": usage.get("tokens", {}),
    }


def build_workspace_results(workspace: str | Path) -> dict[str, Any]:
    """Build one complete summary from immutable run artifacts."""

    root = Path(workspace).expanduser().resolve()
    meta = _load_json(root / "_meta.json")
    score = _load_json(root / "_score.json")
    agent_usage = _agent_usage(root)
    agent_tokens = dict(agent_usage.get("tokens") or {})
    judge_usage = dict(score.get("judge_usage") or {})
    judge_tokens = {
        "input": int(judge_usage.get("prompt_tokens") or 0),
        "output": int(judge_usage.get("completion_tokens") or 0),
        "total": int(judge_usage.get("total_tokens") or 0),
    }
    agent_total = int(agent_tokens.get("total") or 0)
    judge_total = judge_tokens["total"]
    score_summary = {
        "available": bool(score),
        "total": score.get("score"),
        "maximum": score.get("score_max"),
        "normalized": score.get("normalized_score"),
        "research_process": score.get("research_process_score"),
        "scientific_conclusion": score.get("scientific_conclusion_score"),
        "criteria": score.get("criteria", []),
        "scientific_conclusions": score.get("scientific_conclusions", []),
        "critical_failures": score.get("critical_failures", []),
        "evidence_gate_failures": score.get("evidence_gate_failures", []),
        "objective_issue_flags": score.get("objective_issue_flags", []),
        "judge_consistency_warnings": score.get("judge_consistency_warnings", []),
        "applied_score_cap": score.get("applied_score_cap"),
        "rationale": score.get("rationale"),
        "error": score.get("error") or score.get("parse_error"),
    }
    tools = {
        "calls": int(meta.get("tool_call_count") or 0),
        "successful_calls": int(meta.get("successful_tool_calls") or 0),
        "failed_calls": int(meta.get("failed_tool_calls") or 0),
        "runtime_seconds": float(meta.get("tool_runtime_seconds") or 0.0),
        "tools_used": meta.get("tools_used", []),
        "catalog_discovery_calls": int(meta.get("catalog_discovery_call_count") or 0),
        "predefined_action_calls": int(meta.get("predefined_action_call_count") or 0),
        "open_execution_calls": int(meta.get("open_execution_call_count") or 0),
        "managed_scientific_attempts": int(
            meta.get("managed_scientific_attempt_count") or 0
        ),
        "successful_managed_scientific_calls": int(
            meta.get("successful_managed_scientific_calls") or 0
        ),
        "failed_managed_scientific_calls": int(
            meta.get("failed_managed_scientific_calls") or 0
        ),
        "incomplete_managed_scientific_calls": int(
            meta.get("incomplete_managed_scientific_calls") or 0
        ),
    }
    return {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "result_type": "researchchembench_run",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": {
            "id": meta.get("task_id", score.get("task_id", "")),
            "category": meta.get("category", ""),
            "scientific_mode": meta.get("scientific_mode", ""),
            "evaluation_mode": score.get("evaluation_mode", ""),
            "evaluation_profile": score.get("evaluation_profile", ""),
        },
        "run": {
            "id": meta.get("run_id", root.name),
            "workspace": str(root),
            "status": meta.get("status", "unknown"),
            "termination": meta.get("termination"),
            "exit_code": meta.get("exit_code"),
            "duration_seconds": meta.get("duration_seconds"),
            "report_exists": bool(meta.get("report_exists")),
            "background_job_cleanup": meta.get("background_job_cleanup"),
        },
        "agent": {
            "framework": meta.get("agent_key", score.get("agent_key", "")),
            "name": meta.get("agent_name", score.get("agent_name", "")),
            "model": meta.get("model") or meta.get("configured_agent_model", ""),
            "tool_discovery_mode": meta.get("tool_discovery_mode", ""),
        },
        "judge": {
            "model": score.get("judge_model") or meta.get("configured_judge_model", ""),
            "scored_at": score.get("scored_at"),
            "usage": judge_tokens,
        },
        "score": score_summary,
        "tools": tools,
        "tokens": {
            "agent": agent_usage,
            "judge": judge_tokens,
            "combined": {
                "total": agent_total + judge_total,
                "agent_total": agent_total,
                "judge_total": judge_total,
            },
        },
        "artifacts": {
            "meta": "_meta.json",
            "score": "_score.json" if score else None,
            "score_history": (
                "_score_history.jsonl"
                if (root / "_score_history.jsonl").is_file()
                else None
            ),
            "live_progress": (
                "_live_progress.log" if (root / "_live_progress.log").is_file() else None
            ),
            "model_io": "_model_io.jsonl" if (root / "_model_io.jsonl").is_file() else None,
            "tool_trace": "_tool_trace.jsonl" if (root / "_tool_trace.jsonl").is_file() else None,
            "report": "report/report.md" if (root / "report/report.md").is_file() else None,
        },
    }


def write_workspace_results(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace).expanduser().resolve()
    result = build_workspace_results(root)
    _atomic_json(root / "results.json", result)
    return result


def write_batch_results(
    batch_dir: str | Path,
    *,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Aggregate every per-run results.json in one completed CLI batch."""

    root = Path(batch_dir).expanduser().resolve()
    runs = []
    for workspace in sorted(path for path in root.iterdir() if path.is_dir()):
        runs.append(write_workspace_results(workspace))
    scores = [
        float(item["score"]["total"])
        for item in runs
        if item["score"]["total"] is not None
    ]
    normalized = [
        float(item["score"]["normalized"])
        for item in runs
        if item["score"]["normalized"] is not None
    ]
    result = {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "result_type": "researchchembench_batch",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "batch_directory": str(root),
        "config": config,
        "summary": {
            "runs": len(runs),
            "completed": sum(item["run"]["status"] == "completed" for item in runs),
            "failed": sum(item["run"]["status"] != "completed" for item in runs),
            "scored": len(scores),
            "mean_score": statistics.mean(scores) if scores else None,
            "mean_normalized_score": statistics.mean(normalized) if normalized else None,
            "duration_seconds_sum": sum(
                float(item["run"]["duration_seconds"] or 0.0) for item in runs
            ),
            "tool_calls": sum(item["tools"]["calls"] for item in runs),
            "failed_tool_calls": sum(item["tools"]["failed_calls"] for item in runs),
            "agent_tokens": sum(
                int(item["tokens"]["combined"]["agent_total"]) for item in runs
            ),
            "judge_tokens": sum(
                int(item["tokens"]["combined"]["judge_total"]) for item in runs
            ),
            "combined_tokens": sum(
                int(item["tokens"]["combined"]["total"]) for item in runs
            ),
        },
        "runs": runs,
    }
    _atomic_json(root / "results.json", result)
    return result


__all__ = [
    "build_workspace_results",
    "write_batch_results",
    "write_workspace_results",
]

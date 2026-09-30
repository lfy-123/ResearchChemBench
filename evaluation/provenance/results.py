"""Stable machine-readable summaries for completed benchmark runs and batches."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .token_usage import workspace_token_usage
from .trace import canonical_tool_trace_metadata, load_tool_trace, process_metrics

RESULTS_SCHEMA_VERSION = 3


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
    if _load_json(workspace / "_meta.json").get("agent_kind") == "external":
        from ..agent_plugins.protocol import external_usage
        from .agent_events import load_agent_events
        return external_usage(load_agent_events(workspace))
    try:
        usage = workspace_token_usage(workspace)
    except (FileNotFoundError, OSError, ValueError):
        return {
            "available": False,
            "model_step_count": None,
            "session_count": None,
            "cost": None,
            "tokens": {
                "input": None,
                "cache_read": None,
                "cache_write": None,
                "output": None,
                "reasoning": None,
                "total": None,
            },
        }
    return {
        "available": usage.get("usage_details", {}).get("accounting_status") != "unavailable",
        "model_step_count": usage.get("model_step_count"),
        "session_count": usage.get("session_count"),
        "cost": usage.get("cost") if usage.get("cost_available", True) else None,
        "tokens": usage.get("tokens", {}),
    }


def read_scoring_status(workspace):
    """One read-only interpretation for reports, CLI and Web, including old runs."""
    workspace = Path(workspace)
    published = _load_json(workspace / "_score.json")
    latest = _load_json(workspace / "_scoring_attempt.json") or published
    if latest.get("evaluation_status") == "preparing" and latest.get("scoring_directory"):
        state = _load_json(Path(latest["scoring_directory"]) / "state.json")
        latest = {**latest, **state, "evaluation_status": state.get("status", "preparing")}
    status = latest.get("evaluation_status") or latest.get("status") or (
        "judge_error" if latest.get("error") or latest.get("parse_error") else "scored" if latest else "not_started")
    return {"evaluation_status": status, "evaluation_reason": latest.get("evaluation_reason") or latest.get("error"),
            "provider_error": latest.get("provider_error"),
            "latest_attempt": latest.get("score_id"), "published_score": published.get("score_id"),
            "submission_status": latest.get("submission_status", "unknown"),
            "agent_declared_outcome": latest.get("agent_declared_outcome"),
            "evaluated_outcome": latest.get("evaluated_outcome", "undetermined"),
            "judge_usage": latest.get("judge_usage"), "evidence_coverage": latest.get("evidence_coverage"),
            "validation": "current" if latest.get("score_id") else "legacy_unvalidated" if latest else "unavailable"}


def _known_sum(values):
    values = list(values)
    return None if any(v is None for v in values) else sum(values)


def build_workspace_results(workspace: str | Path) -> dict[str, Any]:
    """Build one complete summary from immutable run artifacts."""

    root = Path(workspace).expanduser().resolve()
    meta = _load_json(root / "_meta.json")
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    history = {}
    try:
        store = ExecutionStore.open_existing(root)
        manifest = store.get_record("run", "manifest", {}) if store else {}
        if store and meta.get("agent_kind") != "external":
            from ..execution.codex_history import history_metadata
            history = history_metadata(store)
    except (OSError, ValueError, FileNotFoundError):
        manifest = {}
    if manifest:
        meta = {**meta, **manifest, "status": manifest.get("run_state", meta.get("status"))}
    meta.update(history)
    score = _load_json(root / "_score.json")
    scoring = read_scoring_status(root)
    events = load_tool_trace(root)
    process = process_metrics(events, workspace=root)
    agent_usage = _agent_usage(root)
    agent_tokens = dict(agent_usage.get("tokens") or {})
    judge_usage = dict(scoring.get("judge_usage") or {})
    judge_tokens = {
        "input": judge_usage.get("prompt_tokens"),
        "output": judge_usage.get("completion_tokens"),
        "total": judge_usage.get("total_tokens"),
        "cache_read": judge_usage.get("cached_input_tokens"),
        "reasoning": judge_usage.get("reasoning_output_tokens"),
        "request_count": judge_usage.get("request_count"),
    }
    agent_total = agent_tokens.get("total")
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
        "score_id": score.get("score_id"),
    }
    # Current facts, including zero counts, supersede cached metadata/old scores.
    tools = {label: process[key] for label, key in {
        "calls": "tool_call_count", "successful_calls": "successful_tool_calls",
        "failed_calls": "failed_tool_calls", "runtime_seconds": "tool_runtime_seconds",
        "tools_used": "tools_used", "catalog_discovery_calls": "catalog_discovery_call_count",
        "predefined_action_calls": "predefined_action_call_count", "open_execution_calls": "open_execution_call_count",
        "managed_scientific_attempts": "managed_scientific_attempt_count",
        "resource_budget_rejections": "resource_budget_rejection_count",
        **{key: key for key in (
            "successful_managed_scientific_calls", "partial_managed_scientific_calls",
            "failed_managed_scientific_calls", "active_managed_scientific_calls", "unknown_managed_scientific_calls",
            "submission_accepted_count", "submission_rejected_count", "submission_unconfirmed_count",
            "execution_job_count", "successful_execution_job_count", "partial_execution_job_count",
            "failed_execution_job_count", "timeout_execution_job_count", "cancelled_execution_job_count",
            "active_execution_job_count", "unknown_execution_job_count", "rejected_execution_job_count",
        )},
    }.items()}
    canonical_trace = canonical_tool_trace_metadata(root)
    return {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "result_type": "researchchembench_run",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": {
            "paper_id": meta.get("paper_id", score.get("paper_id", "")),
            "task_type": meta.get("task_type", score.get("task_type", "")),
            "category": meta.get("category", ""),
            "type": score.get("task_type") or meta.get("task_type", ""),
            "package_format": score.get("task_package_format")
            or meta.get("task_package_format", ""),
            "package_content_sha256": score.get("task_package_content_sha256")
            or meta.get("task_package_content_sha256", ""),
            "reference_schema": score.get("reference_schema")
            or meta.get("reference_schema", ""),
            "scientific_mode": meta.get("scientific_mode", ""),
            "evaluation_mode": score.get("evaluation_mode", ""),
            "evaluation_profile": score.get("evaluation_profile", ""),
        },
        "run": {
            "id": meta.get("run_id", root.name),
            "workspace": str(root),
            "status": meta.get("status", "unknown"),
            "error": meta.get("error"),
            "last_failure": meta.get("last_failure"),
            "termination": meta.get("termination"),
            "exit_code": meta.get("exit_code"),
            "duration_seconds": meta.get("duration_seconds"),
            "report_exists": bool(meta.get("report_exists")),
            "background_job_cleanup": meta.get("background_job_cleanup"),
            "recovery_enabled": meta.get("recovery_enabled", False),
            "recovery_count": meta.get("recovery_count", 0),
            "recovery_mode": meta.get("recovery_mode", "native"),
            "history_recovery": meta.get("history_recovery"),
            "history_recovery_error": meta.get("history_recovery_error"),
            "provider_session_id": meta.get("provider_session_id"),
            "attempts": meta.get("attempts", []),
            "execution_reconciliation": meta.get("execution_reconciliation"),
            "cumulative_usage": meta.get("usage"),
            "run_elapsed_seconds": meta.get("run_elapsed_seconds"),
            "timeout_policy": meta.get("timeout_policy", {}),
            "resource_budget": meta.get("resource_budget", {}),
        },
        "agent": {
            "framework": meta.get("agent_key", score.get("agent_key", "")),
            "name": meta.get("agent_name", score.get("agent_name", "")),
            "model": meta.get("model") or meta.get("configured_agent_model", ""),
            "tool_discovery_mode": meta.get("tool_discovery_mode", ""),
            **({"kind": "external", "protocol": meta.get("agent_protocol"),
                "execution_backend": meta.get("execution_backend"),
                "model_budget_enforcement": meta.get("model_budget_enforcement")}
               if meta.get("agent_kind") == "external" else {}),
        },
        "judge": {
            "model": score.get("judge_model") or meta.get("configured_judge_model", ""),
            "scored_at": score.get("scored_at"),
            "evaluator_adapter_id": score.get("evaluator_adapter_id", ""),
            "evaluation_policy_id": score.get("evaluation_policy_id", ""),
            "usage": judge_tokens,
        },
        "score": score_summary,
        "scoring": scoring,
        "tools": tools,
        "process_metrics": process,
        "tokens": {
            "agent": agent_usage,
            "judge": judge_tokens,
            "combined": {
                "total": _known_sum((agent_total, judge_total)),
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
            "canonical_tool_trace": canonical_trace,
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
    for workspace in sorted(path for path in root.iterdir() if path.is_dir() and (path / "_meta.json").is_file()):
        runs.append(write_workspace_results(workspace))
    unstarted = [row for row in _load_json(root / "eval_report.json").get("runs", []) if not row.get("workspace")]
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
        "unstarted_runs": unstarted,
        "summary": {
            "runs": len(runs) + len(unstarted),
            "preflight_failed": sum(row.get("status") == "preflight_failed" for row in unstarted),
            "completed": sum(item["run"]["status"] == "completed" for item in runs),
            "failed": sum(item["run"]["status"] == "failed" for item in runs),
            "unfinished_or_unsuccessful": sum(item["run"]["status"] != "completed" for item in runs),
            **{state: sum(item["run"]["status"] == state for item in runs) for state in (
                "suspended_infrastructure", "recovery_blocked", "cancelled", "budget_exhausted")},
            "scored": len(scores),
            "score_coverage": {"scored": len(scores), "total": len(runs)},
            "evaluation_states": dict(Counter(item["scoring"]["evaluation_status"] for item in runs)),
            "unscored_reasons": dict(Counter(item["scoring"].get("evaluation_reason") or item["scoring"]["evaluation_status"]
                                             for item in runs if item["score"]["total"] is None)),
            "mean_score": statistics.mean(scores) if scores else None,
            "mean_normalized_score": statistics.mean(normalized) if normalized else None,
            "duration_seconds_sum": sum(
                float(item["run"]["duration_seconds"] or 0.0) for item in runs
            ),
            "tool_calls": sum(item["tools"]["calls"] for item in runs),
            "failed_tool_calls": sum(item["tools"]["failed_calls"] for item in runs),
            "agent_tokens": _known_sum(
                item["tokens"]["combined"]["agent_total"] for item in runs
            ),
            "judge_tokens": _known_sum(
                item["tokens"]["combined"]["judge_total"] for item in runs
            ),
            "combined_tokens": _known_sum(
                item["tokens"]["combined"]["total"] for item in runs
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

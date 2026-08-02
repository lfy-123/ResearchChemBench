from __future__ import annotations

import json
from typing import Any

MODE_THRESHOLDS = {
    "paper_reproduction": 70,
    "conclusion_guided_reconstruction": 70,
    "autonomous_research": 70,
    "mechanistic_rule_discovery": 75,
}


def score_record(record: dict[str, Any], mode: str) -> dict[str, Any]:
    dimensions: dict[str, float] = {}
    dimensions["problem_definition"] = _binary(record.get("central_problem"), 10)
    dimensions["input_availability"] = _scaled_len(record.get("inputs", []), 2, 10)
    dimensions["output_verifiability"] = _scaled_len(record.get("expected_outputs", []), 2, 10)
    dimensions["evidence_density"] = _scaled_len(record.get("evidence", []), 4, 15)
    dimensions["tool_orchestration"] = _scaled_len(
        list(
            {_stable_value(value) for value in record.get("tools", []) + record.get("methods", [])}
        ),
        2,
        10,
    )
    dimensions["runtime_feasibility"] = _runtime_score(record.get("runtime", {}), 5)

    hard_failures: list[str] = []
    if mode == "autonomous_research":
        dimensions["open_research_space"] = _scaled_len(record.get("hypotheses", []), 2, 15)
        dimensions["decision_points"] = _scaled_len(record.get("workflow", []), 3, 15)
        dimensions["novelty_boundary"] = _binary(record.get("novelty_boundary"), 10)
        if not record.get("inputs"):
            hard_failures.append("autonomous task has no agent-visible starting inputs")
    elif mode == "paper_reproduction":
        dimensions["method_specificity"] = _scaled_len(record.get("methods", []), 2, 15)
        dimensions["workflow_specificity"] = _scaled_len(record.get("workflow", []), 3, 15)
        dimensions["reference_outputs"] = _scaled_len(record.get("reference_results", []), 2, 10)
        if not record.get("methods") or not record.get("workflow"):
            hard_failures.append(
                "reproduction task lacks a sufficiently explicit method or workflow"
            )
    elif mode == "conclusion_guided_reconstruction":
        dimensions["target_conclusion_richness"] = _scaled_len(
            record.get("reference_results", []), 2, 15
        )
        dimensions["alternative_verification_routes"] = _scaled_len(
            record.get("methods", []), 2, 15
        )
        dimensions["evidence_linkage"] = _scaled_len(record.get("evidence", []), 4, 10)
        if not record.get("reference_results"):
            hard_failures.append("conclusion-guided task lacks a source-grounded target conclusion")
        if not record.get("inputs"):
            hard_failures.append("conclusion-guided task has no agent-visible starting inputs")
    elif mode == "mechanistic_rule_discovery":
        dimensions["competing_hypotheses"] = _scaled_len(record.get("hypotheses", []), 3, 15)
        dimensions["discriminative_evidence"] = _scaled_len(
            [
                item
                for item in record.get("evidence", [])
                if item.get("relation") in {"supports", "refutes"}
            ],
            3,
            15,
        )
        dimensions["negative_evidence"] = _scaled_len(record.get("negative_evidence", []), 1, 10)
        dimensions["cross_system_coverage"] = min(
            10.0,
            float((record.get("information_richness") or {}).get("comparable_system_count", 0)),
        )
        if (record.get("information_richness") or {}).get("comparable_system_count", 0) < 2:
            hard_failures.append("rule-discovery task lacks multiple comparable systems")
    else:
        raise ValueError(f"Unknown task mode: {mode}")

    score = round(sum(dimensions.values()), 1)
    threshold = MODE_THRESHOLDS[mode]
    return {
        "mode": mode,
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold and not hard_failures,
        "dimensions": dimensions,
        "hard_failures": hard_failures,
        "expert_review_required": True,
    }


def _binary(value: Any, weight: float) -> float:
    return weight if value else 0.0


def _scaled_len(value: list[Any], target: int, weight: float) -> float:
    return round(weight * min(1.0, len(value) / max(1, target)), 1)


def _runtime_score(runtime: dict[str, Any], weight: float) -> float:
    hours = runtime.get("estimated_walltime_hours")
    if hours is None:
        return weight * 0.4
    if hours <= 4:
        return weight
    if runtime.get("cache_policy") in {"hybrid", "precomputed"}:
        return weight
    if hours <= 24:
        return weight * 0.6
    return weight * 0.2


def _stable_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)

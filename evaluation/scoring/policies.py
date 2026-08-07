"""Deterministic normalization, evidence gates, and score-cap policies."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _parse_judge_json(text: str, *, score_max: int = 1) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.DOTALL)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise
        value = json.loads(match.group(0))
    raw_score = float(value.get("score", 0))
    if score_max == 1:
        score: int | float = 1 if raw_score == 1 else 0
    else:
        score = round(min(float(score_max), max(0.0, raw_score)), 2)
    return {
        "score": score,
        "score_max": score_max,
        "criteria": value.get("criteria", []),
        "process_criteria": value.get("process_criteria", []),
        "scientific_conclusions": value.get("scientific_conclusions", []),
        "research_process_score": value.get("research_process_score"),
        "scientific_conclusion_score": value.get("scientific_conclusion_score"),
        "submission_validity": value.get("submission_validity"),
        "critical_failures": value.get("critical_failures", []),
        "evidence_gate_failures": value.get("evidence_gate_failures"),
        "objective_issue_flags": value.get("objective_issue_flags", []),
        "reference_conclusion_status": value.get("reference_conclusion_status"),
        "rationale": str(value.get("rationale", "")),
    }


def _normalize_rubric_verdict(
    verdict: dict[str, Any],
    rubric: list[dict[str, Any]],
    *,
    score_max: int,
    allow_total_fallback: bool = True,
) -> dict[str, Any]:
    """Clamp criterion scores and derive a reproducible total when supplied."""

    warnings: list[str] = []
    reported = verdict.get("criteria")
    if not isinstance(reported, list) or not reported:
        if allow_total_fallback:
            raw_score = float(verdict.get("score", 0))
            warnings.append(
                "Judge omitted criterion-level scores; retained its clamped total."
            )
            return {
                "score": round(min(float(score_max), max(0.0, raw_score)), 2),
                "criteria": [],
                "warnings": warnings,
            }
        warnings.append(
            "Judge omitted required criterion-level scores; scored every criterion as zero."
        )
        reported = []

    by_id: dict[str, dict[str, Any]] = {}
    for item in reported:
        if not isinstance(item, dict):
            warnings.append("Ignored a non-object rubric criterion from the judge.")
            continue
        criterion_id = str(item.get("id") or "").strip()
        if not criterion_id:
            warnings.append("Ignored a judge criterion without an id.")
            continue
        if criterion_id in by_id:
            warnings.append(f"Ignored duplicate judge criterion {criterion_id!r}.")
            continue
        by_id[criterion_id] = item

    normalized: list[dict[str, Any]] = []
    for specification in rubric:
        criterion_id = str(specification["id"])
        maximum = float(specification["max_score"])
        item = by_id.get(criterion_id)
        if item is None:
            score = 0.0
            rationale = "Judge omitted this required criterion."
            warnings.append(f"Judge omitted required criterion {criterion_id!r}.")
        else:
            try:
                raw_score = float(item.get("score", 0))
            except (TypeError, ValueError):
                raw_score = 0.0
                warnings.append(f"Judge returned a non-numeric score for {criterion_id!r}.")
            score = min(maximum, max(0.0, raw_score))
            rationale = str(item.get("rationale", ""))
            if abs(score - raw_score) > 1e-9:
                warnings.append(f"Clamped out-of-range score for criterion {criterion_id!r}.")
        normalized.append(
            {
                "id": criterion_id,
                "score": round(score, 2),
                "max_score": maximum,
                "rationale": rationale,
            }
        )
    total = round(sum(float(item["score"]) for item in normalized), 2)
    try:
        claimed_total = float(verdict.get("score", total))
    except (TypeError, ValueError):
        claimed_total = total
        warnings.append("Judge returned a non-numeric total score.")
    if abs(claimed_total - total) > 0.01:
        warnings.append(
            f"Replaced inconsistent judge total {claimed_total:g} with criterion sum {total:g}."
        )
    unknown_ids = sorted(set(by_id) - {str(item["id"]) for item in rubric})
    if unknown_ids:
        warnings.append(f"Ignored unknown judge criteria: {', '.join(unknown_ids)}.")
    return {"score": total, "criteria": normalized, "warnings": warnings}


def _normalize_scientific_conclusions(
    verdict: dict[str, Any],
    rubric: list[dict[str, Any]],
) -> dict[str, Any]:
    """Normalize weighted hidden claims while preserving evidence-status labels."""

    reported = verdict.get("scientific_conclusions")
    normalized = _normalize_rubric_verdict(
        {
            "criteria": reported,
            "score": verdict.get("scientific_conclusion_score"),
        },
        rubric,
        score_max=100,
        allow_total_fallback=False,
    )
    evidence_by_id: dict[str, str] = {}
    if isinstance(reported, list):
        for item in reported:
            if not isinstance(item, dict):
                continue
            claim_id = str(item.get("id") or "").strip()
            status = str(item.get("evidence_status") or "").strip().casefold()
            if claim_id and status in {
                "supported",
                "partially_supported",
                "unsupported",
                "contradicted",
            }:
                evidence_by_id[claim_id] = status
    normalized["criteria"] = [
        {
            **item,
            "evidence_status": evidence_by_id.get(item["id"], "unspecified"),
        }
        for item in normalized["criteria"]
    ]
    return normalized


def _managed_computation_cap(
    policy: dict[str, Any],
    metrics: dict[str, Any],
) -> tuple[float | None, str | None]:
    """Return an objective score cap for tasks that require managed computation."""

    if not policy or policy.get("required") is not True:
        return None, None
    attempts = int(metrics.get("managed_scientific_attempt_count", 0) or 0)
    successes = int(metrics.get("successful_managed_scientific_calls", 0) or 0)
    minimum = int(policy.get("minimum_successful_scientific_calls", 1) or 1)
    if attempts == 0:
        return float(policy.get("score_cap_without_managed_attempt", 20)), (
            "No managed Chemistry MCP scientific execution was attempted."
        )
    if successes == 0:
        return float(policy.get("score_cap_without_successful_managed_call", 40)), (
            "Managed scientific execution was attempted, but no managed scientific call succeeded."
        )
    if successes < minimum:
        return float(policy.get("score_cap_below_minimum_successes", 70)), (
            f"Only {successes} managed scientific calls succeeded; the task requires at least "
            f"{minimum} for uncapped process credit."
        )
    return None, None


def _evidence_gate_cap(
    policy: dict[str, Any],
    reported_failures: Any,
) -> tuple[float | None, str | None, list[str], list[str]]:
    """Translate judge-reported task evidence failures into a reproducible cap."""

    gates = policy.get("gates", []) if isinstance(policy, dict) else []
    if not gates:
        return None, None, [], []
    warnings: list[str] = []
    if not isinstance(reported_failures, list):
        warnings.append(
            "Judge omitted evidence_gate_failures; no evidence-gate cap was applied."
        )
        return None, None, [], warnings

    gate_by_id = {
        str(item.get("id") or "").strip(): item
        for item in gates
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    }
    failures: list[str] = []
    for value in reported_failures:
        gate_id = str(value or "").strip()
        if not gate_id or gate_id in failures:
            continue
        if gate_id not in gate_by_id:
            warnings.append(f"Ignored unknown evidence-gate id {gate_id!r}.")
            continue
        failures.append(gate_id)
    if not failures:
        return None, None, [], warnings

    cap = min(
        float(gate_by_id[gate_id].get("score_cap_if_failed", 100))
        for gate_id in failures
    )
    return (
        cap,
        "Failed required evidence gates: " + ", ".join(failures) + ".",
        failures,
        warnings,
    )


def _nested_value(value: Any, dotted_path: str) -> Any:
    current = value
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _structured_conclusion_mismatches(
    workspace: Path,
    policy: dict[str, Any],
) -> list[str]:
    """Return explicit submitted JSON fields that declare reproduction failure."""

    mismatches: list[str] = []
    specifications = policy.get("structured_match_fields", [])
    if not isinstance(specifications, list):
        return mismatches
    for specification in specifications:
        if not isinstance(specification, dict):
            continue
        relative = str(specification.get("path") or "").strip()
        field = str(specification.get("field") or "").strip()
        path = (workspace / relative).resolve()
        try:
            path.relative_to(workspace)
        except ValueError:
            continue
        if not relative or not field or not path.is_file() or path.suffix.casefold() != ".json":
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if _nested_value(value, field) is False:
            mismatches.append(f"{relative}:{field}=false")
    return mismatches


def _reference_conclusion_cap(
    policy: dict[str, Any],
    reported_status: Any,
    *,
    structured_mismatches: list[str],
) -> tuple[
    float | None,
    str | None,
    str,
    str | None,
    float | None,
    list[str],
]:
    """Apply the strict main-conclusion gate used by reproduction tasks."""

    if not policy or policy.get("required") is not True:
        return None, None, "not_applicable", None, None, []
    warnings: list[str] = []
    status = str(reported_status or "").strip().casefold()
    if structured_mismatches:
        if status == "matched":
            warnings.append(
                "Overrode the judge's matched status because a submitted structured "
                "artifact explicitly records that the paper conclusion was not recovered."
            )
        status = "not_matched"
    elif status not in {"matched", "not_matched", "uncertain"}:
        status = "omitted"
        warnings.append(
            "Judge omitted or invalidated reference_conclusion_status; treated it as omitted."
        )
    if status == "matched":
        return None, None, status, None, None, warnings

    suffix = {
        "not_matched": "not_matched",
        "uncertain": "uncertain",
        "omitted": "omitted",
    }[status]
    default_cap = {"not_matched": 45, "uncertain": 60, "omitted": 45}[status]
    default_criterion_cap = {"not_matched": 0, "uncertain": 15, "omitted": 0}[status]
    cap = float(policy.get(f"score_cap_if_{suffix}", default_cap))
    criterion_id = str(policy.get("criterion_id") or "").strip() or None
    criterion_cap = float(
        policy.get(
            f"max_criterion_score_if_{suffix}", default_criterion_cap
        )
    )
    reason = (
        f"Reference conclusion status is {status}; the configured scientific-outcome "
        "gate does not award full task-completion credit without a matched main conclusion."
    )
    if structured_mismatches:
        reason += " Explicit mismatch evidence: " + ", ".join(structured_mismatches) + "."
    return cap, reason, status, criterion_id, criterion_cap, warnings


def _apply_criterion_score_limit(
    criteria: list[dict[str, Any]],
    *,
    criterion_id: str | None,
    maximum_score: float | None,
) -> tuple[list[dict[str, Any]], bool]:
    if not criterion_id or maximum_score is None:
        return criteria, False
    changed = False
    adjusted: list[dict[str, Any]] = []
    for item in criteria:
        if item.get("id") != criterion_id:
            adjusted.append(item)
            continue
        score = float(item.get("score", 0))
        limited = min(score, maximum_score)
        changed = changed or limited < score
        adjusted.append({**item, "score": round(limited, 2)})
    return adjusted, changed


def _apply_rubric_score_cap(
    score: float,
    criteria: list[dict[str, Any]],
    *,
    cap: float | None,
) -> tuple[float, list[dict[str, Any]]]:
    if cap is None or score <= cap:
        return score, criteria
    if not criteria or score <= 0:
        return round(cap, 2), criteria
    scale = cap / score
    adjusted = [
        {**item, "score": round(float(item.get("score", 0)) * scale, 2)}
        for item in criteria
    ]
    rounded_total = round(sum(float(item["score"]) for item in adjusted), 2)
    difference = round(cap - rounded_total, 2)
    if adjusted and difference:
        adjusted[-1]["score"] = round(
            max(0.0, min(float(adjusted[-1]["max_score"]), float(adjusted[-1]["score"]) + difference)),
            2,
        )
    return round(cap, 2), adjusted

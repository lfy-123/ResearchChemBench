"""Deterministic normalization, evidence gates, and score-cap policies."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _parse_judge_json(text: str, *, allow_duplicate_reads=False, diagnostics=None) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.DOTALL)
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError(f"Non-finite JSON constant: {value}")
    decoder = json.JSONDecoder(object_pairs_hook=unique, parse_constant=invalid_constant)
    if not allow_duplicate_reads:
        value = decoder.decode(cleaned)
    else:
        values, position = [], 0
        while position < len(cleaned):
            position += len(cleaned[position:]) - len(cleaned[position:].lstrip())
            if position == len(cleaned):
                break
            if len(values) >= 8:
                raise ValueError("Too many JSON objects in Judge response")
            value, position = decoder.raw_decode(cleaned, position)
            values.append(value)
        if not values:
            raise ValueError("Empty Judge response")
        value = values[0]
        if len(values) > 1:
            canonical = lambda v: json.dumps(v, sort_keys=True, ensure_ascii=False)
            if (not isinstance(value, dict) or value.get("type") != "evidence_request"
                    or not isinstance(value.get("reads"), list) or not value["reads"]
                    or any(not isinstance(r, dict) or not isinstance(r.get("ref"), str) for r in value["reads"])
                    or any(canonical(v) != canonical(value) for v in values[1:])):
                raise ValueError("Multiple JSON objects are only accepted for identical evidence requests")
            if diagnostics is not None:
                diagnostics["duplicate_evidence_requests"] = len(values)
    if not isinstance(value, dict):
        raise ValueError("Judge response must be a JSON object")
    return value


def parse_judge_response(response, *, diagnostics):
    if response.get("response_status") not in (None, "completed") or response.get("finish_reason") not in (None, "stop"):
        raise ValueError("Judge response is incomplete: " + str(response.get("incomplete_details") or response.get("finish_reason") or response.get("response_status")))
    messages = response.get("output_messages", [])
    if any(m.get("status") not in (None, "completed") for m in messages):
        raise ValueError("Judge message is incomplete")
    texts = ["".join(c.get("text", "") for c in m["content"] if c["type"] == "output_text") for m in messages]
    texts = [t for t in texts if t.strip()]
    if len(texts) > 1:
        # Each message must be complete: do not join fragments from different messages.
        for text in texts:
            _parse_judge_json(text, allow_duplicate_reads=True)
    return _parse_judge_json("".join(texts) if texts else response["raw_text"],
                             allow_duplicate_reads=True, diagnostics=diagnostics)


class JudgeContractError(ValueError):
    """A bounded collection of actionable structural errors, never a score."""
    def __init__(self):
        self.errors, self.truncated = [], False
        super().__init__("Invalid Judge response contract")

    def add(self, path, message, **details):
        error = {"response_path": path, "message": str(message)[:1800], **details}
        if len(self.errors) >= 20 or len(json.dumps(self.errors + [error], ensure_ascii=False)) > 6000:
            self.truncated = True
        else:
            self.errors.append(error)

    def __str__(self):
        return json.dumps({"errors": self.errors, "errors_truncated": self.truncated}, ensure_ascii=False)


def _finite_score(value, maximum):
    import math
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError("Judge score must be a finite number")
    if not 0 <= value <= maximum:
        raise ValueError("Judge score is outside the authored range")
    return round(value, 2)


def _normalize_rubric_verdict(verdict, rubric, *, score_max):
    """Validate every authored criterion; never invent a missing score."""
    reported = verdict.get("criteria")
    if not isinstance(reported, list):
        raise ValueError("Judge omitted required criterion scores")
    ids = [item.get("id") for item in reported if isinstance(item, dict)]
    if len(ids) != len(reported) or len(ids) != len(set(ids)) or set(ids) != {r["id"] for r in rubric}:
        raise ValueError("Judge criterion IDs must match the authored rubric exactly")
    by_id = {item["id"]: item for item in reported}
    normalized = []
    for spec in rubric:
        item = by_id[spec["id"]]
        if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
            raise ValueError("Every criterion needs a rationale")
        if "max_score" in item and item["max_score"] != spec["max_score"]:
            raise ValueError("Judge cannot change a criterion maximum")
        normalized.append({**item, "score": _finite_score(item.get("score"), spec["max_score"]),
                           "max_score": spec["max_score"]})
    total = round(sum(item["score"] for item in normalized), 2)
    warnings = []
    if verdict.get("score") is not None:
        claimed = _finite_score(verdict["score"], score_max)
        if abs(claimed - total) > 0.01 + 1e-9:
            raise ValueError("Judge total conflicts with criterion scores")
        if claimed != total:
            warnings.append("Rounded total to the sum of criterion scores.")
    return {"score": total, "criteria": normalized, "warnings": warnings}


def _normalize_scientific_conclusions(verdict, rubric, *, enforce_evidence_consistency=False):
    normalized = _normalize_rubric_verdict(
        {"criteria": verdict.get("scientific_conclusions"), "score": verdict.get("scientific_conclusion_score")},
        rubric, score_max=100)
    for item in normalized["criteria"]:
        if item.get("evidence_status") not in {"supported", "partially_supported", "unsupported", "contradicted"}:
            raise ValueError("Invalid scientific evidence_status")
        if (enforce_evidence_consistency
                and item["evidence_status"] in {"unsupported", "contradicted"}
                and item["score"] > 0):
            raise ValueError("Unsupported or contradicted submitted claim cannot receive positive scientific credit")
    return normalized


def _check_citation(citation, check, item):
    try:
        check(citation)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        raise ValueError(
            f"Invalid citation in {item.get('id', item.get('rule_id', 'verdict'))!r}: "
            f"{json.dumps(citation, ensure_ascii=False)[:1200]}: {exc}. "
            "Use an existing reference/selector; omit selector or use an empty string for the whole file. "
            "JSON Pointer '/' selects an empty key, not the root. Preserve other valid citations."
        ) from exc


def validate_judge_verdict(verdict, truth, *, citation_check, rules=()):
    """Structural and deterministic checks only; the Judge owns scientific semantics."""
    if not isinstance(verdict.get("rationale"), str) or not verdict["rationale"].strip():
        raise ValueError("Judge rationale is required")
    if "unresolved_disposition" in verdict and verdict["unresolved_disposition"] not in {"scorable", "needs_review"}:
        raise ValueError("Invalid unresolved_disposition")
    mode = truth.get("evaluation_mode", "binary")
    items = []
    if mode == "dual_axis_100":
        if verdict.get("submission_validity") not in {"valid", "invalid_submission", "not_scorable_objective"}:
            raise ValueError("Invalid submission_validity")
        _normalize_rubric_verdict(
            {"criteria": verdict.get("process_criteria"), "score": verdict.get("research_process_score")},
            truth["scoring_rubric"], score_max=100)
        _normalize_scientific_conclusions(
            verdict, truth["scientific_conclusion_rubric"],
            enforce_evidence_consistency=truth.get("dual_axis_scoring_policy", {}).get(
                "enforce_evidence_score_consistency", False
            ),
        )
        items = [(f"/{name}/{i}", item) for name in ("process_criteria", "scientific_conclusions")
                 for i, item in enumerate(verdict[name])]
    elif mode == "rubric_100":
        _normalize_rubric_verdict(verdict, truth["scoring_rubric"], score_max=100)
        items = [(f"/criteria/{i}", item) for i, item in enumerate(verdict["criteria"])]
    else:
        _finite_score(verdict.get("score"), 1)
        if verdict["score"] not in {0, 1}:
            raise ValueError("Binary score must be 0 or 1")
    errors = JudgeContractError()
    def citations_for(item, path, *, required):
        citations = item.get("citations")
        if citations is None and not required:
            return
        if not isinstance(citations, list) or (required and not citations):
            errors.add(path + "/citations", f"Scored item {item.get('id', item.get('rule_id', 'verdict'))!r} requires {'nonempty ' if required else ''}citations: [{{'ref': 'registered evidence reference'}}]")
            return
        for i, citation in enumerate(citations):
            try:
                _check_citation(citation, citation_check, item)
            except ValueError as exc:
                details = {k: str(citation[k])[:800] for k in ("ref", "pointer", "selector") if isinstance(citation, dict) and k in citation}
                details.update(getattr(exc.__cause__, "details", {}))
                errors.add(f"{path}/citations/{i}", exc, **details)
    for path, item in items or [("", verdict)]:
        citations_for(item, path, required=True)
    if rules:
        dispositions = verdict.get("rule_assessments")
        if not isinstance(dispositions, list):
            raise ValueError("Judge must account for all authored rules")
        ids = [r.get("rule_id") for r in dispositions if isinstance(r, dict)]
        if len(ids) != len(dispositions) or len(set(ids)) != len(ids) or set(ids) != {r["rule_id"] for r in rules}:
            raise ValueError("rule_assessments must cover the authored rules exactly")
        checks = {r["rule_id"]: r for r in rules}
        for i, item in enumerate(dispositions):
            state = item.get("assessment")
            if state not in {"pass", "fail", "partial", "not_applicable", "unresolved"}:
                raise ValueError("Unknown rule assessment")
            if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
                raise ValueError("Rule assessment needs a rationale")
            citations_for(item, f"/rule_assessments/{i}", required=False)
            check = checks[item["rule_id"]]
            reported = item.get("numeric_check")
            acknowledged = reported.get("assessment") if isinstance(reported, dict) else reported
            expected = check["assessment"]
            if expected in {"pass", "fail"} and acknowledged != expected:
                errors.add(f"/rule_assessments/{i}/numeric_check",
                    f"Rule {item['rule_id']!r}: numeric_check must be {expected!r} "
                    f"(or an object with assessment={expected!r}); received {repr(reported)[:160]}"
                )
    if errors.errors or errors.truncated:
        raise errors
    return verdict


def _managed_computation_cap(
    policy: dict[str, Any],
    metrics: dict[str, Any],
) -> tuple[float | None, str | None]:
    """Return an objective score cap for tasks that require managed computation."""

    if not policy or policy.get("required") is not True:
        return None, None
    attempts = int(metrics.get("managed_scientific_attempt_count", 0) or 0)
    successes = int(metrics.get("successful_managed_scientific_calls", 0) or 0)
    partials = int(metrics.get("partial_managed_scientific_calls", 0) or 0)
    minimum = int(policy.get("minimum_successful_scientific_calls", 1) or 1)
    if attempts == 0:
        return float(policy.get("score_cap_without_managed_attempt", 20)), (
            "No managed Chemistry MCP scientific execution was attempted."
        )
    if successes == 0:
        if partials:
            return float(policy.get("score_cap_below_minimum_successes", 70)), (
                f"Managed scientific execution produced {partials} partial result(s), but no fully successful call."
            )
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

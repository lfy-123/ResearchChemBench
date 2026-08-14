from __future__ import annotations

from typing import Any

WORKFLOW_CONTRACT_VERSION = "stage02-confirmed-workflows/v1"

WORKFLOW_VERIFICATION_AXES = (
    "author_performed_computation",
    "identifiable_chemical_system",
    "actual_chemical_calculation_or_simulation",
    "generated_chemical_output",
    "scientific_use_of_output",
    "nontrivial_workflow",
)


def sanitize_workflow_candidates(
    response: dict[str, Any],
    *,
    valid_ids: set[str],
    computational_ids: set[str],
    limit: int = 3,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate Stage02 discovery candidates while preserving legacy responses."""

    warnings: list[dict[str, Any]] = []
    raw_candidates = response.get("workflow_candidates")
    if not isinstance(raw_candidates, list):
        raw_candidates = _legacy_candidates(response)
        if raw_candidates:
            warnings.append(
                {
                    "field": "workflow_candidates",
                    "reason": "legacy_single_workflow_adapted",
                }
            )

    output: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(raw_candidates[: max(1, int(limit))]):
        if not isinstance(raw, dict):
            warnings.append(
                {
                    "field": f"workflow_candidates[{index}]",
                    "reason": "candidate_not_object",
                }
            )
            continue
        workflow_id = _workflow_id(raw.get("workflow_id"), index, seen_ids)
        seen_ids.add(workflow_id)
        unknown_ids: set[str] = set()
        evidence_ids = _validated_ids(raw.get("evidence_ids"), valid_ids, unknown_ids)
        steps: list[dict[str, Any]] = []
        seen_steps: set[str] = set()
        for step_index, item in enumerate((raw.get("steps") or [])[:6]):
            if not isinstance(item, dict):
                continue
            action = _text(item.get("action"), 400)
            generated_output = _text(item.get("generated_output"), 400)
            if not action:
                continue
            step_id = _step_id(item.get("step_id"), step_index, seen_steps)
            seen_steps.add(step_id)
            step_evidence = _validated_ids(item.get("evidence_ids"), valid_ids, unknown_ids)
            steps.append(
                {
                    "step_id": step_id,
                    "action": action,
                    "generated_output": generated_output,
                    "evidence_ids": step_evidence,
                }
            )
            evidence_ids.extend(step_evidence)
        evidence_ids = list(dict.fromkeys(evidence_ids))
        if unknown_ids:
            warnings.append(
                {
                    "field": f"workflow_candidates[{index}].evidence_ids",
                    "reason": "unknown_evidence_ids",
                    "values": sorted(unknown_ids)[:12],
                }
            )
        if not steps or not (set(evidence_ids) & computational_ids):
            warnings.append(
                {
                    "field": f"workflow_candidates[{index}]",
                    "reason": "missing_steps_or_computational_evidence",
                }
            )
            continue
        output.append(
            {
                "workflow_id": workflow_id,
                "chemical_system": _text(
                    raw.get("chemical_system") or raw.get("computational_input"), 500
                ),
                "scientific_output": _text(
                    raw.get("scientific_output") or raw.get("generated_output"), 500
                ),
                "scientific_use": _text(raw.get("scientific_use"), 500),
                "steps": steps,
                "evidence_ids": evidence_ids[:16],
            }
        )
    return output, warnings


def sanitize_workflow_verifications(
    response: dict[str, Any],
    *,
    candidates: list[dict[str, Any]],
    valid_ids: set[str],
    computational_ids: set[str],
    minimum_confidence: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate all discovered workflows and return the confirmed subset."""

    raw_rows = response.get("workflow_verifications")
    if not isinstance(raw_rows, list):
        raw_rows = response.get("candidate_verifications")
    legacy = not isinstance(raw_rows, list)
    if legacy:
        raw_rows = [_legacy_verification(response, candidates[0])] if candidates else []

    by_id = {
        str(row.get("workflow_id") or ""): row
        for row in raw_rows
        if isinstance(row, dict) and row.get("workflow_id")
    }
    warnings: list[dict[str, Any]] = []
    verifications: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        workflow_id = str(candidate["workflow_id"])
        raw = by_id.get(workflow_id)
        if raw is None and legacy and index == 0 and raw_rows:
            raw = raw_rows[0]
        if not isinstance(raw, dict):
            verifications.append(
                {
                    "workflow_id": workflow_id,
                    "confirmed": False,
                    "status": "missing_verification",
                    "evidence_ids": [],
                    "computational_evidence_ids": [],
                    "confidence": 0.0,
                }
            )
            continue
        unknown_ids: set[str] = set()
        evidence_ids = _validated_ids(raw.get("evidence_ids"), valid_ids, unknown_ids)
        cited_computational = _validated_ids(
            raw.get("computational_evidence_ids"), valid_ids, unknown_ids
        )
        cited_computational = [
            value for value in cited_computational if value in computational_ids
        ]
        if not cited_computational:
            cited_computational = [
                value
                for value in evidence_ids
                if value in computational_ids
            ]
        axes = {
            axis: _axis_value(raw, axis)
            for axis in WORKFLOW_VERIFICATION_AXES
        }
        experimental_only = _choice(
            raw.get("experimental_data_analysis_only"), {"yes", "no", "uncertain"}
        )
        confidence = _confidence(raw.get("confidence"))
        is_confirmed = (
            all(value == "yes" for value in axes.values())
            and experimental_only == "no"
            and confidence >= minimum_confidence
            and bool(cited_computational)
            and not unknown_ids
        )
        status = "confirmed" if is_confirmed else "rejected_or_unresolved"
        row = {
            "workflow_id": workflow_id,
            **axes,
            "experimental_data_analysis_only": experimental_only,
            "confirmed": is_confirmed,
            "status": status,
            "evidence_ids": list(dict.fromkeys(evidence_ids))[:16],
            "computational_evidence_ids": list(dict.fromkeys(cited_computational))[:12],
            "rationale": _text(raw.get("rationale"), 800),
            "confidence": confidence,
        }
        if unknown_ids:
            warnings.append(
                {
                    "field": f"workflow_verifications[{index}].evidence_ids",
                    "reason": "unknown_evidence_ids",
                    "values": sorted(unknown_ids)[:12],
                }
            )
        verifications.append(row)
        if is_confirmed:
            confirmed.append(
                {
                    **candidate,
                    "verification_evidence_ids": row["evidence_ids"],
                    "verification_confidence": confidence,
                }
            )
    return verifications, confirmed, warnings


def compact_candidate_skeletons(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove first-call conclusions while retaining the workflow identities to verify."""

    return [
        {
            "workflow_id": row["workflow_id"],
            "chemical_system": row.get("chemical_system"),
            "scientific_output": row.get("scientific_output"),
            "scientific_use": row.get("scientific_use"),
            "steps": row.get("steps") or [],
            "evidence_ids": row.get("evidence_ids") or [],
        }
        for row in candidates[:3]
    ]


def _legacy_candidates(response: dict[str, Any]) -> list[dict[str, Any]]:
    steps = response.get("computational_workflow_steps")
    if not isinstance(steps, list) or not steps:
        return []
    outputs = [
        str(step.get("generated_output") or "").strip()
        for step in steps
        if isinstance(step, dict) and step.get("generated_output")
    ]
    return [
        {
            "workflow_id": "wf1",
            "chemical_system": response.get("central_scientific_question") or "",
            "scientific_output": "; ".join(outputs),
            "scientific_use": response.get("primary_contribution") or "",
            "steps": steps,
            "evidence_ids": response.get("evidence_ids") or [],
        }
    ]


def _legacy_verification(
    response: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    return {
        "workflow_id": candidate["workflow_id"],
        "author_performed_computation": response.get("author_performed_computation"),
        "identifiable_chemical_system": response.get("identifiable_chemical_model"),
        "actual_chemical_calculation_or_simulation": response.get(
            "actual_chemical_calculation_or_simulation"
        ),
        "generated_chemical_output": response.get("generated_chemical_output"),
        "scientific_use_of_output": response.get(
            "scientific_use_of_computational_output"
        ),
        "nontrivial_workflow": response.get("nontrivial_computational_workflow"),
        "experimental_data_analysis_only": response.get("experimental_data_analysis_only"),
        "evidence_ids": response.get("evidence_ids") or [],
        "computational_evidence_ids": response.get("computational_evidence_ids") or [],
        "rationale": response.get("rationale"),
        "confidence": response.get("confidence"),
    }


def _axis_value(raw: dict[str, Any], axis: str) -> str:
    aliases = {
        "identifiable_chemical_system": "identifiable_chemical_model",
        "scientific_use_of_output": "scientific_use_of_computational_output",
        "nontrivial_workflow": "nontrivial_computational_workflow",
    }
    return _choice(raw.get(axis, raw.get(aliases.get(axis, ""))), {"yes", "no", "uncertain"})


def _workflow_id(value: Any, index: int, seen: set[str]) -> str:
    base = _text(value, 80) or f"wf{index + 1}"
    if base not in seen:
        return base
    suffix = 2
    while f"{base}-{suffix}" in seen:
        suffix += 1
    return f"{base}-{suffix}"


def _step_id(value: Any, index: int, seen: set[str]) -> str:
    base = _text(value, 80) or f"s{index + 1}"
    if base not in seen:
        return base
    suffix = 2
    while f"{base}-{suffix}" in seen:
        suffix += 1
    return f"{base}-{suffix}"


def _validated_ids(value: Any, valid_ids: set[str], unknown: set[str]) -> list[str]:
    values = value if isinstance(value, list) else []
    normalized = list(dict.fromkeys(str(item) for item in values if str(item)))
    unknown.update(item for item in normalized if item not in valid_ids)
    return [item for item in normalized if item in valid_ids]


def _choice(value: Any, allowed: set[str]) -> str:
    normalized = str(value or "").strip().casefold()
    return normalized if normalized in allowed else "uncertain"


def _confidence(value: Any) -> float:
    labels = {"low": 0.35, "medium": 0.65, "high": 0.9}
    if isinstance(value, str) and value.casefold() in labels:
        return labels[value.casefold()]
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _text(value: Any, limit: int) -> str:
    return str(value or "").strip()[:limit]


__all__ = [
    "WORKFLOW_CONTRACT_VERSION",
    "WORKFLOW_VERIFICATION_AXES",
    "compact_candidate_skeletons",
    "sanitize_workflow_candidates",
    "sanitize_workflow_verifications",
]

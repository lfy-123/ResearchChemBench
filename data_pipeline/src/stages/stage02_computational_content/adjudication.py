from __future__ import annotations

from typing import Any

PASS_DECISIONS = {
    "computational_content_confirmed",
    "computational_primary_mixed_confirmed",
}
SEMANTIC_DECISIONS = {
    *PASS_DECISIONS,
    "experimental_primary_computational_support",
    "computational_content_not_found",
    "uncertain",
}
ARTICLE_ROLES = {"original_research", "review", "correction", "editorial", "unknown"}


def sanitize_classification(
    response: dict[str, Any],
    *,
    valid_ids: set[str],
    computational_ids: set[str],
    deterministic_experiment_ids: set[str],
    minimum_confidence: float,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    """Validate cited evidence and derive the final decision from fixed criteria."""

    warnings: list[dict[str, Any]] = []
    review_reasons: list[str] = []
    sanitized = dict(response) if isinstance(response, dict) else {}
    proposed = str(sanitized.get("decision") or "uncertain")
    if proposed not in SEMANTIC_DECISIONS:
        warnings.append({"field": "decision", "reason": "invalid_decision"})
        proposed = "uncertain"

    sanitized["article_role"] = _choice(sanitized.get("article_role"), ARTICLE_ROLES, "unknown")
    for field in (
        "performed_computation",
        "complete_computational_workflow",
        "author_performed_experiments",
    ):
        sanitized[field] = _choice(sanitized.get(field), {"yes", "no", "uncertain"}, "uncertain")
    sanitized["computation_role"] = _choice(
        sanitized.get("computation_role"),
        {"primary", "supporting", "background_only", "none", "uncertain"},
        "uncertain",
    )
    sanitized["study_mode"] = _choice(
        sanitized.get("study_mode"),
        {
            "pure_computational",
            "mixed_computational_experimental",
            "experimental_with_computational_support",
            "noncomputational",
            "uncertain",
        },
        "uncertain",
    )
    sanitized["counterfactual_without_computation"] = _choice(
        sanitized.get("counterfactual_without_computation"),
        {"main_claim_fails", "partly_survives", "main_claim_survives", "uncertain"},
        "uncertain",
    )
    sanitized["counterfactual_without_experiments"] = _choice(
        sanitized.get("counterfactual_without_experiments"),
        {"main_claim_fails", "partly_survives", "main_claim_survives", "uncertain"},
        "uncertain",
    )
    confidence = _confidence_number(sanitized.get("confidence"))
    sanitized["confidence"] = confidence

    unknown_ids: set[str] = set()
    for field in ("evidence_ids", "experimental_evidence_ids", "conflicting_evidence_ids"):
        values, unknown = _validated_ids(sanitized.get(field), valid_ids)
        sanitized[field] = values
        unknown_ids.update(unknown)
    if unknown_ids:
        warnings.append(
            {
                "field": "evidence_ids",
                "reason": "unknown_evidence_ids",
                "values": sorted(unknown_ids)[:12],
            }
        )
        review_reasons.append("unknown_evidence_ids")

    claims = _sanitize_claims(sanitized.get("central_claims"), valid_ids, unknown_ids)
    workflow = _sanitize_workflow(
        sanitized.get("computational_workflow_steps"), valid_ids, unknown_ids
    )
    experiments = _sanitize_contributions(
        sanitized.get("experimental_contributions"), valid_ids, unknown_ids
    )
    sanitized["central_claims"] = claims
    sanitized["computational_workflow_steps"] = workflow
    sanitized["experimental_contributions"] = experiments
    if unknown_ids and "unknown_evidence_ids" not in review_reasons:
        review_reasons.append("unknown_evidence_ids")

    # Model-selected blocks are useful evidence pointers, but only the independent
    # full-text attribution scan can establish that this paper's authors did lab work.
    verified_experiment_ids = deterministic_experiment_ids
    model_experiment = sanitized["author_performed_experiments"]
    if verified_experiment_ids:
        if model_experiment == "no":
            review_reasons.append("model_missed_verified_author_experiment")
        sanitized["author_performed_experiments"] = "yes"
    elif model_experiment == "yes":
        sanitized["author_performed_experiments"] = "uncertain"
        review_reasons.append("author_experiment_without_valid_evidence")

    computation_required_claims = [
        claim
        for claim in claims
        if claim.get("computation_required") is True
        and set(claim.get("evidence_ids") or []) & computational_ids
    ]
    workflow_has_evidence = bool(workflow) and all(
        set(step.get("evidence_ids") or []) & computational_ids and step.get("generated_output")
        for step in workflow
    )
    top_level_computational_evidence = set(sanitized["evidence_ids"]) & computational_ids
    computation_complete = (
        sanitized["performed_computation"] == "yes"
        and sanitized["complete_computational_workflow"] == "yes"
        and bool(top_level_computational_evidence)
        and workflow_has_evidence
    )
    computation_central = (
        computation_complete
        and sanitized["computation_role"] == "primary"
        and bool(computation_required_claims)
        and sanitized["counterfactual_without_computation"] == "main_claim_fails"
    )
    has_author_experiments = sanitized["author_performed_experiments"] == "yes"
    high_confidence = confidence >= minimum_confidence

    if sanitized["article_role"] != "original_research":
        decision = (
            "uncertain"
            if sanitized["article_role"] == "unknown"
            else "computational_content_not_found"
        )
    elif not computation_complete:
        if sanitized["performed_computation"] == "no" and high_confidence:
            decision = "computational_content_not_found"
        elif sanitized["complete_computational_workflow"] == "no" and high_confidence:
            decision = "computational_content_not_found"
        else:
            decision = "uncertain"
    elif not has_author_experiments:
        if (
            sanitized["author_performed_experiments"] == "no"
            and computation_central
            and high_confidence
        ):
            decision = "computational_content_confirmed"
        else:
            decision = "uncertain"
    elif computation_central and high_confidence:
        decision = "computational_primary_mixed_confirmed"
    elif (
        high_confidence
        and sanitized["computation_role"] in {"supporting", "background_only"}
        and sanitized["counterfactual_without_computation"] == "main_claim_survives"
    ):
        decision = "experimental_primary_computational_support"
    else:
        decision = "uncertain"

    if confidence < minimum_confidence and decision != "computational_content_not_found":
        review_reasons.append("confidence_below_threshold")
    if computation_complete and not computation_required_claims:
        review_reasons.append("no_computation_required_central_claim")
    if computation_complete and sanitized["counterfactual_without_computation"] == "uncertain":
        review_reasons.append("computation_counterfactual_uncertain")
    if proposed != decision:
        warnings.append(
            {
                "field": "decision",
                "reason": "deterministic_decision_override",
                "model_decision": proposed,
                "derived_decision": decision,
            }
        )
        if decision == "uncertain" or decision in PASS_DECISIONS or proposed in PASS_DECISIONS:
            review_reasons.append("model_and_contract_disagree")

    sanitized["decision"] = decision
    sanitized["passed"] = decision in PASS_DECISIONS
    sanitized["verification"] = {
        "computation_complete": computation_complete,
        "computation_central": computation_central,
        "verified_author_experiment_ids": sorted(verified_experiment_ids),
        "computation_required_claims": len(computation_required_claims),
        "validated_computational_evidence_ids": sorted(top_level_computational_evidence),
        "minimum_confidence": minimum_confidence,
    }
    return sanitized, warnings, list(dict.fromkeys(review_reasons))


def should_review(decision: str, reasons: list[str]) -> bool:
    if not reasons:
        return False
    if decision == "computational_content_not_found" and set(reasons) <= {
        "confidence_below_threshold"
    }:
        return False
    return decision == "uncertain" or any(
        reason
        in {
            "model_missed_verified_author_experiment",
            "author_experiment_without_valid_evidence",
            "no_computation_required_central_claim",
            "computation_counterfactual_uncertain",
            "model_and_contract_disagree",
            "unknown_evidence_ids",
        }
        for reason in reasons
    )


def _sanitize_claims(
    value: Any, valid_ids: set[str], unknown_ids: set[str]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict):
            continue
        evidence_ids, unknown = _validated_ids(item.get("evidence_ids"), valid_ids)
        unknown_ids.update(unknown)
        statement = str(item.get("statement") or item.get("claim") or "").strip()[:800]
        if not statement:
            continue
        output.append(
            {
                "statement": statement,
                "computation_required": item.get("computation_required") is True,
                "experiment_required": item.get("experiment_required") is True,
                "evidence_ids": evidence_ids,
            }
        )
    return output[:2]


def _sanitize_workflow(
    value: Any, valid_ids: set[str], unknown_ids: set[str]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, item in enumerate(value if isinstance(value, list) else []):
        if not isinstance(item, dict):
            continue
        evidence_ids, unknown = _validated_ids(item.get("evidence_ids"), valid_ids)
        unknown_ids.update(unknown)
        action = str(item.get("action") or "").strip()[:400]
        output_text = str(item.get("generated_output") or "").strip()[:400]
        if not action:
            continue
        output.append(
            {
                "step_id": str(item.get("step_id") or f"step_{index + 1}")[:80],
                "action": action,
                "generated_output": output_text,
                "evidence_ids": evidence_ids,
            }
        )
    return output[:3]


def _sanitize_contributions(
    value: Any, valid_ids: set[str], unknown_ids: set[str]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict):
            continue
        evidence_ids, unknown = _validated_ids(item.get("evidence_ids"), valid_ids)
        unknown_ids.update(unknown)
        statement = str(item.get("statement") or "").strip()[:800]
        if statement:
            output.append({"statement": statement, "evidence_ids": evidence_ids})
    return output[:2]


def _validated_ids(value: Any, valid_ids: set[str]) -> tuple[list[str], set[str]]:
    values = value if isinstance(value, list) else []
    normalized = list(dict.fromkeys(str(item) for item in values if str(item)))
    return [item for item in normalized if item in valid_ids], {
        item for item in normalized if item not in valid_ids
    }


def _choice(value: Any, allowed: set[str], default: str) -> str:
    normalized = str(value or "").strip()
    return normalized if normalized in allowed else default


def _confidence_number(value: Any) -> float:
    labels = {"low": 0.35, "medium": 0.65, "high": 0.9}
    if isinstance(value, str) and value.casefold() in labels:
        return labels[value.casefold()]
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


__all__ = ["PASS_DECISIONS", "SEMANTIC_DECISIONS", "sanitize_classification", "should_review"]

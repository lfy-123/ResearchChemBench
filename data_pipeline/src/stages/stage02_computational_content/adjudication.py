from __future__ import annotations

from typing import Any

PASS_DECISIONS = {
    "computational_content_confirmed",
    "computational_primary_mixed_confirmed",
    "computational_experimental_co_primary_confirmed",
    "experimental_primary_benchmarkable_computation",
}
NON_ORIGINAL_ARTICLE_ROLES = {"review", "correction", "editorial"}
SEMANTIC_DECISIONS = {
    *PASS_DECISIONS,
    "computational_workflow_not_benchmarkable",
    "computational_content_not_found",
    "non_original_article",
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

    sanitized["article_role"] = _article_role(sanitized.get("article_role"))
    for field in (
        "performed_computation",
        "complete_computational_workflow",
        "benchmarkable_computational_workflow",
        "author_performed_experiments",
    ):
        sanitized[field] = _choice(sanitized.get(field), {"yes", "no", "uncertain"}, "uncertain")
    sanitized["computation_role"] = _choice(
        sanitized.get("computation_role"),
        {"primary", "co_primary", "supporting", "background_only", "none", "uncertain"},
        "uncertain",
    )
    sanitized["evidence_direction"] = _choice(
        sanitized.get("evidence_direction"),
        {
            "pure_computation",
            "computation_predicts_then_experiment_validates",
            "experiment_observes_then_computation_explains",
            "co_equal",
            "none",
            "uncertain",
        },
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

    model_experiment_ids = set(sanitized["experimental_evidence_ids"])
    for contribution in experiments:
        model_experiment_ids.update(contribution.get("evidence_ids") or [])
    # The deterministic scan is deliberately high precision and therefore incomplete.
    # A model may also establish author experiments by citing packet evidence in a
    # structured experimental contribution; uncited assertions remain unresolved.
    verified_experiment_ids = set(deterministic_experiment_ids)
    model_experiment = sanitized["author_performed_experiments"]
    if model_experiment == "yes" and model_experiment_ids:
        verified_experiment_ids.update(model_experiment_ids)
    if deterministic_experiment_ids:
        if model_experiment == "no":
            review_reasons.append("model_missed_verified_author_experiment")
        sanitized["author_performed_experiments"] = "yes"
    elif model_experiment == "yes" and not model_experiment_ids:
        sanitized["author_performed_experiments"] = "uncertain"
        review_reasons.append("author_experiment_without_valid_evidence")

    computation_required_claims = [
        claim
        for claim in claims
        if claim.get("computation_required") is True
        and set(claim.get("evidence_ids") or []) & computational_ids
    ]
    workflow_has_evidence = bool(workflow) and all(
        step.get("evidence_ids") and step.get("generated_output")
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
        and sanitized["computation_role"] in {"primary", "co_primary"}
        and sanitized["counterfactual_without_computation"] == "main_claim_fails"
    )
    workflow_benchmarkable = sanitized["benchmarkable_computational_workflow"] == "yes"
    evidence_direction = sanitized["evidence_direction"]
    has_author_experiments = sanitized["author_performed_experiments"] == "yes"
    high_confidence = confidence >= minimum_confidence

    if sanitized["article_role"] in NON_ORIGINAL_ARTICLE_ROLES:
        decision = "non_original_article"
    elif sanitized["article_role"] != "original_research":
        decision = "uncertain"
    elif sanitized["performed_computation"] == "no" and high_confidence:
        decision = "computational_content_not_found"
    elif not computation_complete:
        if sanitized["complete_computational_workflow"] == "no" and high_confidence:
            decision = "computational_workflow_not_benchmarkable"
        else:
            decision = "uncertain"
    elif not workflow_benchmarkable:
        if sanitized["benchmarkable_computational_workflow"] == "no" and high_confidence:
            decision = "computational_workflow_not_benchmarkable"
        else:
            decision = "uncertain"
    elif not has_author_experiments:
        if (
            sanitized["author_performed_experiments"] == "no"
            and evidence_direction == "pure_computation"
            and high_confidence
        ):
            decision = "computational_content_confirmed"
        else:
            decision = "uncertain"
    elif not high_confidence:
        decision = "uncertain"
    elif evidence_direction == "co_equal":
        decision = "computational_experimental_co_primary_confirmed"
    elif evidence_direction == "computation_predicts_then_experiment_validates":
        decision = "computational_primary_mixed_confirmed"
    elif evidence_direction == "experiment_observes_then_computation_explains":
        decision = "experimental_primary_benchmarkable_computation"
    elif sanitized["computation_role"] == "co_primary":
        decision = "computational_experimental_co_primary_confirmed"
    elif sanitized["computation_role"] == "primary":
        decision = "computational_primary_mixed_confirmed"
    elif sanitized["computation_role"] == "supporting":
        decision = "experimental_primary_benchmarkable_computation"
    else:
        decision = "uncertain"

    if confidence < minimum_confidence and decision != "computational_content_not_found":
        review_reasons.append("confidence_below_threshold")
    if computation_complete and sanitized["benchmarkable_computational_workflow"] == "uncertain":
        review_reasons.append("benchmarkable_workflow_uncertain")
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
        "workflow_benchmarkable": workflow_benchmarkable,
        "computation_central": computation_central,
        "evidence_direction": evidence_direction,
        "verified_author_experiment_ids": sorted(verified_experiment_ids),
        "model_cited_author_experiment_ids": sorted(model_experiment_ids),
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
            "benchmarkable_workflow_uncertain",
            "model_and_contract_disagree",
            "unknown_evidence_ids",
        }
        for reason in reasons
    )


def apply_pass_verification(
    candidate: dict[str, Any],
    verification: dict[str, Any],
    *,
    valid_ids: set[str],
    computational_ids: set[str],
    experimental_candidate_ids: set[str],
    minimum_confidence: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Verify that a proposed Pass contains an evidenced benchmarkable workflow."""

    output = dict(candidate)
    locked_article_role = _article_role(candidate.get("article_role"))
    output["article_role"] = locked_article_role
    warnings: list[dict[str, Any]] = []
    raw = dict(verification) if isinstance(verification, dict) else {}
    proposed_decision = _choice(raw.get("decision"), SEMANTIC_DECISIONS, "uncertain")
    decision = proposed_decision
    author_computation = _choice(
        raw.get("author_performed_computation"), {"yes", "no", "uncertain"}, "uncertain"
    )
    complete_workflow = _choice(
        raw.get("complete_computational_workflow"), {"yes", "no", "uncertain"}, "uncertain"
    )
    workflow_axes = {
        field: _choice(raw.get(field), {"yes", "no", "uncertain"}, "uncertain")
        for field in (
            "identifiable_chemical_model",
            "actual_chemical_calculation_or_simulation",
            "generated_chemical_output",
            "scientific_use_of_computational_output",
            "nontrivial_computational_workflow",
            "experimental_data_analysis_only",
        )
    }
    author_experiments = _choice(
        raw.get("author_performed_experiments"), {"yes", "no", "uncertain"}, "uncertain"
    )
    evidence_ids, unknown = _validated_ids(raw.get("evidence_ids"), valid_ids)
    computation_evidence_ids, unknown_computation = _validated_ids(
        raw.get("computational_evidence_ids"), valid_ids
    )
    experiment_evidence_ids, unknown_experiment = _validated_ids(
        raw.get("experimental_evidence_ids"), valid_ids
    )
    unknown.update(unknown_computation)
    unknown.update(unknown_experiment)
    confidence = _confidence_number(raw.get("confidence"))
    computation_evidence_ids = [
        value for value in computation_evidence_ids if value in computational_ids
    ]
    candidate_computation_ids = {
        str(value)
        for value in ((candidate.get("verification") or {}).get(
            "validated_computational_evidence_ids"
        ) or [])
        if str(value) in computational_ids
    }
    effective_computation_ids = set(computation_evidence_ids) or candidate_computation_ids
    # Experimental candidate extraction is intentionally high precision and incomplete.
    # Any source-valid model citation may establish the author-experiment axis.
    experiment_evidence_ids = list(dict.fromkeys(experiment_evidence_ids))
    if unknown:
        warnings.append(
            {
                "field": "pass_verification.evidence_ids",
                "reason": "unknown_evidence_ids",
                "values": sorted(unknown)[:12],
            }
        )

    positive_workflow_axes = (
        "identifiable_chemical_model",
        "actual_chemical_calculation_or_simulation",
        "generated_chemical_output",
        "scientific_use_of_computational_output",
        "nontrivial_computational_workflow",
    )
    workflow_facts_confirmed = all(
        workflow_axes[field] == "yes" for field in positive_workflow_axes
    )
    workflow_facts_rejected = (
        any(workflow_axes[field] == "no" for field in positive_workflow_axes)
        or workflow_axes["experimental_data_analysis_only"] == "yes"
    )
    structured_pass_facts = (
        confidence >= minimum_confidence
        and author_computation == "yes"
        and complete_workflow == "yes"
        and workflow_facts_confirmed
        and workflow_axes["experimental_data_analysis_only"] == "no"
        and bool(effective_computation_ids)
    )
    if confidence >= minimum_confidence and author_computation == "no":
        decision = "computational_content_not_found"
    elif (
        confidence >= minimum_confidence
        and author_computation == "yes"
        and (complete_workflow == "no" or workflow_facts_rejected)
    ):
        decision = "computational_workflow_not_benchmarkable"
    elif structured_pass_facts and author_experiments == "no":
        decision = "computational_content_confirmed"
        if proposed_decision != decision:
            warnings.append(
                {
                    "field": "pass_verification.decision",
                    "reason": "pass_label_repaired_from_author_experiment_axis",
                    "model_decision": proposed_decision,
                    "derived_decision": decision,
                }
            )
    elif structured_pass_facts and author_experiments == "yes":
        candidate_decision = str(candidate.get("decision") or "")
        if proposed_decision in PASS_DECISIONS - {"computational_content_confirmed"}:
            decision = proposed_decision
        elif candidate_decision in PASS_DECISIONS - {"computational_content_confirmed"}:
            decision = candidate_decision
        else:
            direction = str(candidate.get("evidence_direction") or "")
            if direction == "co_equal":
                decision = "computational_experimental_co_primary_confirmed"
            elif direction == "computation_predicts_then_experiment_validates":
                decision = "computational_primary_mixed_confirmed"
            else:
                decision = "experimental_primary_benchmarkable_computation"
    elif structured_pass_facts:
        candidate_decision = str(candidate.get("decision") or "")
        if candidate_decision in PASS_DECISIONS:
            decision = candidate_decision
        elif candidate.get("author_performed_experiments") == "no":
            decision = "computational_content_confirmed"
        elif candidate.get("author_performed_experiments") == "yes":
            direction = str(candidate.get("evidence_direction") or "")
            if direction == "co_equal":
                decision = "computational_experimental_co_primary_confirmed"
            elif direction == "computation_predicts_then_experiment_validates":
                decision = "computational_primary_mixed_confirmed"
            else:
                decision = "experimental_primary_benchmarkable_computation"
        else:
            decision = "uncertain"
    elif decision in PASS_DECISIONS and author_experiments == "no":
        original_decision = decision
        decision = "computational_content_confirmed"
        if original_decision != decision:
            warnings.append(
                {
                    "field": "pass_verification.decision",
                    "reason": "pass_label_repaired_from_author_experiment_axis",
                    "model_decision": original_decision,
                    "derived_decision": decision,
                }
            )
    elif decision == "computational_content_confirmed" and author_experiments == "yes":
        candidate_decision = str(candidate.get("decision") or "")
        decision = (
            candidate_decision
            if candidate_decision in PASS_DECISIONS
            and candidate_decision != "computational_content_confirmed"
            else "uncertain"
        )

    pass_contract_ok = (
        decision in PASS_DECISIONS
        and structured_pass_facts
    )

    if decision in PASS_DECISIONS and (
        not pass_contract_ok or confidence < minimum_confidence
    ):
        warnings.append(
            {
                "field": "pass_verification.decision",
                "reason": "pass_verification_contract_unmet",
                "model_decision": decision,
            }
        )
        decision = "uncertain"
    elif confidence < minimum_confidence:
        decision = "uncertain"

    # The discovery call owns article type. The verifier may validate only
    # the frozen computation candidate and cannot promote a review or an
    # unresolved article type to original research.
    if locked_article_role in NON_ORIGINAL_ARTICLE_ROLES:
        if decision != "non_original_article":
            warnings.append(
                {
                    "field": "pass_verification.article_role",
                    "reason": "non_original_article_lock_applied",
                    "locked_article_role": locked_article_role,
                    "verifier_decision": decision,
                }
            )
        decision = "non_original_article"
    elif locked_article_role != "original_research":
        if decision in PASS_DECISIONS:
            warnings.append(
                {
                    "field": "pass_verification.article_role",
                    "reason": "unknown_article_role_cannot_pass",
                    "verifier_decision": decision,
                }
            )
        decision = "uncertain"

    output["decision"] = decision
    output["passed"] = decision in PASS_DECISIONS
    if decision == "computational_content_confirmed":
        output.update(
            {
                "performed_computation": "yes",
                "complete_computational_workflow": "yes",
                "benchmarkable_computational_workflow": "yes",
                "author_performed_experiments": "no",
                "computation_role": "primary",
                "evidence_direction": "pure_computation",
                "study_mode": "pure_computational",
                "counterfactual_without_computation": "main_claim_fails",
            }
        )
    elif decision == "computational_primary_mixed_confirmed":
        output.update(
            {
                "performed_computation": "yes",
                "complete_computational_workflow": "yes",
                "benchmarkable_computational_workflow": "yes",
                "author_performed_experiments": "yes",
                "computation_role": "primary",
                "evidence_direction": "computation_predicts_then_experiment_validates",
                "study_mode": "mixed_computational_experimental",
                "counterfactual_without_computation": "main_claim_fails",
            }
        )
    elif decision == "computational_experimental_co_primary_confirmed":
        output.update(
            {
                "performed_computation": "yes",
                "complete_computational_workflow": "yes",
                "benchmarkable_computational_workflow": "yes",
                "author_performed_experiments": "yes",
                "computation_role": "co_primary",
                "evidence_direction": "co_equal",
                "study_mode": "mixed_computational_experimental",
            }
        )
    elif decision == "experimental_primary_benchmarkable_computation":
        output.update(
            {
                "performed_computation": "yes",
                "complete_computational_workflow": "yes",
                "benchmarkable_computational_workflow": "yes",
                "author_performed_experiments": "yes",
                "computation_role": "supporting",
                "evidence_direction": "experiment_observes_then_computation_explains",
                "study_mode": "experimental_with_computational_support",
                "counterfactual_without_computation": "main_claim_survives",
            }
        )
    elif decision == "computational_workflow_not_benchmarkable":
        output.update(
            {
                "benchmarkable_computational_workflow": "no",
                "computation_role": "supporting",
            }
        )
    elif decision == "computational_content_not_found":
        output.update(
            {
                "complete_computational_workflow": "no",
                "computation_role": "none",
                "evidence_direction": "none",
                "study_mode": "noncomputational",
            }
        )
    elif decision == "non_original_article":
        output.update(
            {
                "performed_computation": "no",
                "complete_computational_workflow": "no",
                "benchmarkable_computational_workflow": "no",
                "computation_role": "background_only",
                "evidence_direction": "none",
                "study_mode": "noncomputational",
            }
        )

    output["evidence_ids"] = list(
        dict.fromkeys([*(output.get("evidence_ids") or []), *evidence_ids])
    )
    output["pass_verification"] = {
        "locked_article_role": locked_article_role,
        "proposed_decision": proposed_decision,
        "decision": decision,
        "author_performed_computation": author_computation,
        "complete_computational_workflow": complete_workflow,
        **workflow_axes,
        "author_performed_experiments": author_experiments,
        "computational_input": str(raw.get("computational_input") or "").strip()[:400],
        "computational_operation": str(raw.get("computational_operation") or "").strip()[:400],
        "generated_output": str(raw.get("generated_output") or "").strip()[:400],
        "scientific_use": str(raw.get("scientific_use") or "").strip()[:400],
        "evidence_ids": evidence_ids,
        "computational_evidence_ids": sorted(effective_computation_ids),
        "model_cited_computational_evidence_ids": computation_evidence_ids,
        "experimental_evidence_ids": experiment_evidence_ids,
        "rationale": str(raw.get("rationale") or "").strip()[:800],
        "confidence": confidence,
        "contract_ok": pass_contract_ok if decision in PASS_DECISIONS else True,
    }
    return output, warnings


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
    return output[:1]


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
    return output[:2]


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
    return output[:1]


def _validated_ids(value: Any, valid_ids: set[str]) -> tuple[list[str], set[str]]:
    values = value if isinstance(value, list) else []
    normalized = list(dict.fromkeys(str(item) for item in values if str(item)))
    return [item for item in normalized if item in valid_ids], {
        item for item in normalized if item not in valid_ids
    }


def _choice(value: Any, allowed: set[str], default: str) -> str:
    normalized = str(value or "").strip()
    return normalized if normalized in allowed else default


def _article_role(value: Any) -> str:
    normalized = (
        str(value or "").strip().casefold().replace("-", "_").replace(" ", "_")
    )
    aliases = {
        "review_article": "review",
        "systematic_review": "review",
        "mini_review": "review",
        "minireview": "review",
        "perspective": "review",
        "viewpoint": "editorial",
        "commentary": "editorial",
        "opinion": "editorial",
        "corrigendum": "correction",
        "erratum": "correction",
        "retraction": "correction",
    }
    normalized = aliases.get(normalized, normalized)
    return normalized if normalized in ARTICLE_ROLES else "unknown"


def _confidence_number(value: Any) -> float:
    labels = {"low": 0.35, "medium": 0.65, "high": 0.9}
    if isinstance(value, str) and value.casefold() in labels:
        return labels[value.casefold()]
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


__all__ = [
    "ARTICLE_ROLES",
    "NON_ORIGINAL_ARTICLE_ROLES",
    "PASS_DECISIONS",
    "SEMANTIC_DECISIONS",
    "apply_pass_verification",
    "sanitize_classification",
    "should_review",
]

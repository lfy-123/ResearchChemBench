from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from src.contracts import (
    decision_counts,
    read_json,
    read_jsonl,
    record_header,
    write_json,
    write_jsonl,
)
from src.core.concurrency import ordered_parallel_map
from src.prompts import (
    STAGE05_ROUTER_SYSTEM,
    STAGE05_ROUTER_VERSION,
    STAGE05_SYSTEM,
    STAGE05_VERSION,
    TASK_DIRECTION_GUIDANCE,
    TASK_DIRECTIONS,
)
from src.stages.stage03_toolbox_resource_gate.stage import (
    _merge_detection_aliases,
    find_software_mentions,
    resolve_software,
)

AUDIT_DIMENSIONS = (
    "scientific_significance",
    "workflow_completeness",
    "input_assets",
    "parameters",
    "ground_truth",
    "software",
    "cost",
    "leakage_risk",
)
RECOVERABLE_DIMENSIONS = {"input_assets", "parameters", "ground_truth"}
SOURCE_EVIDENCE_DIMENSIONS = {
    "scientific_significance",
    "workflow_completeness",
    "input_assets",
    "parameters",
    "ground_truth",
}
RECOVERY_TYPES = {
    "evidence_extraction",
    "format_conversion",
    "evidence_verification",
    "evidence_anchored_construction",
    "explicit_identifier_retrieval",
    "normalized_protocol",
}
BUILDER_ROUTES = {"exact_reproduction", "evidence_recovery", "normalized_reconstruction"}
HARD_BLOCKER_CODES = {
    "no_substantive_computation",
    "essential_software_uncovered",
    "no_machine_scoreable_target",
    "task_defining_identity_missing",
    "bespoke_author_asset_unavailable",
    "hidden_target_required_for_input",
    "cost_exceeds_budget",
}
MINIMUM_SCIENTIFIC_STEPS = 2


def run_stage05(
    *,
    stage04_records,
    documents,
    config,
    router_model,
    auditor_model,
    workspace: Path,
    run_id: str,
    router_checkpoints: dict[str, dict[str, Any]] | None = None,
    auditor_checkpoints: dict[str, dict[str, Any]] | None = None,
    on_router_result=None,
    on_auditor_result=None,
    on_result=None,
):
    stage_root = workspace / "stage_05_benchmark_suitability"
    by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass":
            by_paper.setdefault(document["paper_id"], []).append(document)
    eligible = [row for row in stage04_records if row.get("passed")]
    toolbox_profile = (
        read_json(config["toolbox_capabilities"])
        if config.get("toolbox_capabilities")
        else {}
    )
    software_aliases = (
        read_json(config["software_aliases"]) if config.get("software_aliases") else {}
    )
    external_aliases = (
        read_json(config["external_software_aliases"])
        if config.get("external_software_aliases")
        else {}
    )

    def assess(record):
        paper_id = record["paper_id"]
        route_response = None
        route_audit = None
        evidence_route = None
        route_warnings = []
        response = None
        audit = None
        response_attempts = []
        try:
            blocks = [
                block
                for document in by_paper.get(paper_id, [])
                for block in read_jsonl(document["content_blocks_path"])
            ]
            document_rows = by_paper.get(paper_id, [])
            document_inventory = _document_inventory(document_rows)
            software_facts, stage05_software_lookup = _stage05_software_context(
                blocks,
                record,
                aliases=software_aliases,
                external_aliases=external_aliases,
                profile=toolbox_profile,
            )
            index_blocks = _router_index_blocks(
                blocks,
                record,
                int(config.get("router_index_characters", 60000)),
            )
            router_packet = {
                "paper_id": paper_id,
                "taxonomy": list(TASK_DIRECTIONS),
                "taxonomy_scope": TASK_DIRECTION_GUIDANCE,
                "documents": document_inventory,
                "stage03_workflows": _without_evidence_ids(
                    record.get("workflow_inventory") or []
                ),
                "software_coverage_facts": software_facts,
                "index_blocks": index_blocks,
                "requirements": {
                    "candidate_limit": int(config.get("router_candidate_limit", 3)),
                    "high_recall_routing_only": True,
                },
            }
            checkpoint = (router_checkpoints or {}).get(paper_id) or {}
            if checkpoint.get("router_response") and checkpoint.get("evidence_route"):
                route_response = checkpoint["router_response"]
                route_audit = checkpoint.get("router_audit") or {"cache": "resume_store"}
                evidence_route = checkpoint["evidence_route"]
                route_warnings = list(checkpoint.get("route_validation_warnings") or [])
            else:
                route_response, route_audit = router_model.call_json(
                    namespace="stage05a_evidence_router",
                    record_id=paper_id,
                    prompt_version=STAGE05_ROUTER_VERSION,
                    system_prompt=STAGE05_ROUTER_SYSTEM,
                    user_content=json.dumps(router_packet, ensure_ascii=False),
                    max_tokens=int(config.get("router_max_tokens", 3072)),
                )
                evidence_route, route_warnings = _sanitize_evidence_route(
                    route_response,
                    {str(block["evidence_id"]) for block in index_blocks},
                    candidate_limit=int(config.get("router_candidate_limit", 3)),
                )
                if on_router_result is not None:
                    on_router_result(
                        record,
                        {
                            "paper_id": paper_id,
                            "processing_status": "completed",
                            "decision": "router_completed",
                            "passed": True,
                            "evidence_route": evidence_route,
                            "router_response": route_response,
                            "router_audit": route_audit,
                            "route_validation_warnings": route_warnings,
                        },
                    )
            evidence_blocks = _auditor_evidence_blocks(
                blocks,
                evidence_route,
                int(config.get("auditor_evidence_characters", 90000)),
            )
            packet = {
                "paper_id": paper_id,
                "taxonomy": list(TASK_DIRECTIONS),
                "taxonomy_scope": TASK_DIRECTION_GUIDANCE,
                "documents": document_inventory,
                "evidence_route": evidence_route,
                "route_validation_warnings": route_warnings,
                "stage04": _without_evidence_ids(
                    {
                        key: record.get(key)
                        for key in (
                            "workflow_inventory",
                            "software_mappings",
                            "resource_profile",
                            "toolbox_profile_id",
                            "toolbox_catalog_hash",
                        )
                    }
                ),
                "software_coverage_facts": software_facts,
                "evidence_blocks": evidence_blocks,
                "requirements": {
                    "minimum_dependent_steps": MINIMUM_SCIENTIFIC_STEPS,
                    "candidate_limit": int(config.get("candidate_limit", 1)),
                },
                "evidence_contract": {
                    "source": "stage04_mineru_deep_normalization",
                    "cite_only_evidence_block_ids_from_this_packet": True,
                },
            }
            auditor_checkpoint = (auditor_checkpoints or {}).get(paper_id) or {}
            if auditor_checkpoint.get("model_response"):
                response = auditor_checkpoint["model_response"]
                audit = auditor_checkpoint.get("model_audit") or {"cache": "resume_store"}
                response_attempts = list(
                    auditor_checkpoint.get("model_response_attempts")
                    or [{"response": response, "audit": audit}]
                )
                contract_retry_performed = bool(
                    auditor_checkpoint.get("contract_retry_performed", False)
                )
            else:
                response, audit = auditor_model.call_json(
                    namespace="stage05b_candidate_auditor",
                    record_id=paper_id,
                    prompt_version=STAGE05_VERSION,
                    system_prompt=STAGE05_SYSTEM,
                    user_content=json.dumps(packet, ensure_ascii=False),
                    max_tokens=int(config.get("auditor_max_tokens", 16000)),
                )
                response_attempts = [{"response": response, "audit": audit}]
                contract_retry_performed = False
                if on_auditor_result is not None:
                    on_auditor_result(
                        record,
                        _auditor_checkpoint_row(
                            paper_id,
                            response,
                            audit,
                            response_attempts,
                            contract_retry_performed=False,
                        ),
                    )
            evidence_ids = {str(block["evidence_id"]) for block in evidence_blocks}
            candidate_limit = int(config.get("candidate_limit", 1))
            evidence_text_by_id = {
                str(block["evidence_id"]): str(block.get("text") or "")
                for block in evidence_blocks
            }
            candidates, validation_rejections = _validate_candidates(
                response,
                evidence_ids,
                record,
                candidate_limit=candidate_limit,
                evidence_text_by_id=evidence_text_by_id,
                software_lookup_override=stage05_software_lookup,
            )
            validation_rejections.extend(
                _response_contract_rejections(response, record, evidence_ids)
            )
            validation_rejections.extend(_software_fact_contradictions(response, record))
            if (
                _contract_retry_needed(validation_rejections)
                and bool(config.get("contract_retry", True))
                and not contract_retry_performed
            ):
                original_decision = str(response.get("decision") or "").casefold()
                retry_response, retry_audit = auditor_model.call_json(
                    namespace="stage05b_candidate_auditor_contract_retry",
                    record_id=f"{paper_id}-contract-retry",
                    prompt_version=f"{STAGE05_VERSION}-contract-retry-v1",
                    system_prompt=(
                        f"{STAGE05_SYSTEM}\nYour previous response failed deterministic schema "
                        "validation. Return a corrected complete JSON object. Use one exact taxonomy "
                        "identifier for task_direction, a workflow dependency graph, arrays for validation_gates, "
                        "scoring_metrics, required_software, and evidence_ids; include estimated_cost "
                        "and all eight audit_dimensions; include builder_route, a recovery plan for "
                        "review candidates, and evidence-backed hard_blockers for reject; preserve "
                        "pass/needs_builder_review/reject "
                        "semantics and include review fields; treat software_coverage_facts as immutable; "
                        "and cite only evidence "
                        "IDs present in evidence_blocks. Do not change the scientific conclusion merely "
                        "to avoid a validation error."
                    ),
                    user_content=json.dumps(
                        {
                            **packet,
                            "previous_response": response,
                            "validation_rejections": validation_rejections,
                        },
                        ensure_ascii=False,
                    ),
                    max_tokens=int(config.get("auditor_max_tokens", 16000)),
                    thinking="disabled",
                )
                response_attempts.append({"response": retry_response, "audit": retry_audit})
                contract_retry_performed = True
                retry_decision = str(retry_response.get("decision") or "").casefold()
                if retry_decision == original_decision:
                    response, audit = retry_response, retry_audit
                if on_auditor_result is not None:
                    on_auditor_result(
                        record,
                        _auditor_checkpoint_row(
                            paper_id,
                            response,
                            audit,
                            response_attempts,
                            contract_retry_performed=True,
                        ),
                    )
                candidates, validation_rejections = _validate_candidates(
                    response,
                    evidence_ids,
                    record,
                    candidate_limit=candidate_limit,
                    evidence_text_by_id=evidence_text_by_id,
                    software_lookup_override=stage05_software_lookup,
                )
                validation_rejections.extend(
                    _response_contract_rejections(response, record, evidence_ids)
                )
                validation_rejections.extend(_software_fact_contradictions(response, record))
            has_response_contradiction = any(
                row.get("candidate_id") in {"response-software-facts", "response-contract"}
                for row in validation_rejections
            )
            requested_decision = str(response.get("decision") or "").casefold()
            if (
                candidates
                and requested_decision in {"pass", "needs_builder_review"}
                and not has_response_contradiction
            ):
                decision = requested_decision
            elif requested_decision == "reject":
                decision = "reject"
            elif requested_decision in {"pass", "needs_builder_review"}:
                # A candidate that still violates the deterministic contract after
                # one repair attempt has not passed this gate.
                decision = "reject"
            else:
                decision = "contract_invalid"
            abstention_reasons = response.get("abstention_reasons") or []
            if decision == "contract_invalid" and not abstention_reasons:
                abstention_reasons = [
                    f"{item['candidate_id']}: {', '.join(item['reasons'])}"
                    for item in validation_rejections
                ] or ["model_pass_without_valid_candidate"]
            return {
                **record_header(run_id=run_id, stage="stage05", paper_id=paper_id),
                "processing_status": "completed",
                "decision": decision,
                "passed": decision in {"pass", "needs_builder_review"},
                "candidates": candidates,
                "abstention_reasons": abstention_reasons,
                "review_dimensions": _string_list(response.get("review_dimensions")),
                "review_reasons": _string_list(response.get("review_reasons")),
                "validation_rejections": validation_rejections,
                "model_response": response,
                "model_response_attempts": response_attempts,
                "model_audit": audit,
                "evidence_route": evidence_route,
                "router_response": route_response,
                "router_audit": route_audit,
                "route_validation_warnings": route_warnings,
            }
        except Exception as exc:
            return {
                **record_header(run_id=run_id, stage="stage05", paper_id=paper_id),
                "processing_status": "failed",
                "decision": "processing_failed",
                "passed": False,
                "candidates": [],
                "error": {"error_type": type(exc).__name__, "message": str(exc)},
                "evidence_route": evidence_route,
                "router_response": route_response,
                "router_audit": route_audit,
                "route_validation_warnings": route_warnings,
            }

    records = ordered_parallel_map(
        assess,
        eligible,
        max_workers=int(config.get("workers", auditor_model.config.get("workers", 1))),
        on_complete=(
            (lambda _completed, _total, _index, source, result: on_result(source, result))
            if on_result is not None
            else None
        ),
    )
    candidates = [
        {"paper_id": row["paper_id"], **candidate}
        for row in records
        for candidate in row.get("candidates") or []
    ]
    write_jsonl(stage_root / "evidence_routes.jsonl", [
        {
            "paper_id": row["paper_id"],
            "evidence_route": row.get("evidence_route"),
            "router_response": row.get("router_response"),
            "router_audit": row.get("router_audit"),
            "validation_warnings": row.get("route_validation_warnings") or [],
        }
        for row in records
    ])
    write_jsonl(stage_root / "candidate_audits.jsonl", [
        {
            "paper_id": row["paper_id"],
            "decision": row.get("decision"),
            "model_response": row.get("model_response"),
            "model_response_attempts": row.get("model_response_attempts") or [],
            "validation_rejections": row.get("validation_rejections") or [],
        }
        for row in records
    ])
    write_jsonl(stage_root / "contract_errors.jsonl", [
        {"paper_id": row["paper_id"], "validation_rejections": row["validation_rejections"]}
        for row in records
        if row.get("validation_rejections")
    ])
    write_jsonl(stage_root / "decisions.jsonl", records)
    write_jsonl(stage_root / "candidates.jsonl", candidates)
    write_jsonl(
        stage_root / "abstentions.jsonl", [row for row in records if not row["passed"]]
    )
    summary = {
        **record_header(run_id=run_id, stage="stage05"),
        "papers": len(records),
        "decisions": decision_counts(records),
        "passed": sum(row["passed"] for row in records),
        "processing_errors": sum(row["processing_status"] == "failed" for row in records),
        "run_status": (
            "infrastructure_failed"
            if records and all(row["processing_status"] == "failed" for row in records)
            else "completed_with_errors"
            if any(row["processing_status"] == "failed" for row in records)
            else "completed"
        ),
        "candidates": len(candidates),
        "router_model_role": router_model.role,
        "router_model": router_model.model,
        "model_role": auditor_model.role,
        "model": auditor_model.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "candidates": candidates, "summary": summary}


def _auditor_checkpoint_row(
    paper_id,
    response,
    audit,
    response_attempts,
    *,
    contract_retry_performed,
):
    return {
        "paper_id": paper_id,
        "processing_status": "completed",
        "decision": "auditor_completed",
        "passed": True,
        "model_response": response,
        "model_audit": audit,
        "model_response_attempts": response_attempts,
        "contract_retry_performed": bool(contract_retry_performed),
    }


def _contract_retry_needed(rejections):
    """Retry malformed JSON contracts, never a scientific or recoverability rejection."""

    retryable = {
        "candidate_not_an_object",
        "invalid_task_direction",
        "invalid_builder_route",
        "invalid_ground_truth_level",
        "invalid_audit_dimensions",
        "unknown_or_missing_mineru_evidence_ids",
        "required_software_missing",
        "missing_required_scientific_fields",
        "invalid_decision",
        "pass_response_has_blockers",
        "pass_response_has_review_items",
        "builder_review_missing_review_items",
        "invalid_builder_review_dimensions",
        "reject_missing_blocking_dimensions",
        "invalid_blocking_dimensions",
        "software_dimension_and_blocking_software_disagree",
        "reject_response_has_review_items",
        "reject_missing_hard_blockers",
        "invalid_hard_blocker",
        "hard_blocker_evidence_invalid",
    }
    prefixes = (
        "invalid_audit_dimension:",
        "audit_dimension_evidence_invalid:",
        "audit_dimension_missing_fields_required:",
        "blocking_software_not_in_uncovered_facts:",
    )
    reasons = [
        str(reason)
        for item in rejections
        for reason in (item.get("reasons") or [])
    ]
    return bool(reasons) and all(
        reason in retryable or reason.startswith(prefixes) for reason in reasons
    )


def _validate_candidates(
    response,
    evidence_ids,
    stage04,
    *,
    candidate_limit=3,
    evidence_text_by_id=None,
    software_lookup_override=None,
):
    output: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    software_lookup = software_lookup_override or _covered_software_lookup(stage04)
    for index, candidate in enumerate((response.get("candidates") or [])[:candidate_limit]):
        if not isinstance(candidate, dict):
            rejected.append(
                {
                    "candidate_id": f"candidate-{index + 1}",
                    "reasons": ["candidate_not_an_object"],
                }
            )
            continue
        normalized = dict(candidate)
        candidate_id = str(
            candidate.get("candidate_id") or f"{stage04['paper_id']}-candidate-{index + 1}"
        )
        reasons: list[str] = []
        direction = candidate.get("task_direction") or candidate.get("direction")
        if direction not in TASK_DIRECTIONS:
            reasons.append("invalid_task_direction")
        normalized["task_direction"] = direction
        normalized.pop("direction", None)
        builder_route = str(candidate.get("builder_route") or "").casefold()
        normalized["builder_route"] = builder_route
        if builder_route not in BUILDER_ROUTES:
            reasons.append("invalid_builder_route")
        for field in ("validation_gates", "scoring_metrics", "evidence_ids"):
            normalized[field] = _string_list(candidate.get(field))
        normalized["workflow_steps"] = _workflow_steps(candidate.get("workflow_steps"))
        graph_errors = _workflow_graph_errors(normalized["workflow_steps"], evidence_ids)
        if graph_errors:
            reasons.extend(graph_errors)
        if not normalized["validation_gates"] or not normalized["scoring_metrics"]:
            reasons.append("incomplete_workflow_validation_or_scoring")
        if candidate.get("ground_truth_level") not in {"A", "B", "C", "D"}:
            reasons.append("invalid_ground_truth_level")
        estimated_cost = candidate.get("estimated_cost")
        if not _valid_estimated_cost(estimated_cost, stage04):
            reasons.append("cost_estimate_missing_invalid_or_over_budget")
        audit_dimensions, dimension_errors = _audit_dimensions(
            candidate.get("audit_dimensions"), evidence_ids
        )
        normalized["audit_dimensions"] = audit_dimensions
        reasons.extend(dimension_errors)
        buildability = {
            key: (audit_dimensions.get(key) or {}).get("state")
            for key in ("input_assets", "parameters", "ground_truth", "software", "cost")
        }
        normalized["buildability_checks"] = buildability
        if not dimension_errors:
            decision = str(response.get("decision") or "").casefold()
            states = {key: value["state"] for key, value in audit_dimensions.items()}
            if decision == "pass" and any(value != "confirmed" for value in states.values()):
                reasons.append("pass_requires_confirmed_audit_dimensions")
            if decision == "pass" and builder_route != "exact_reproduction":
                reasons.append("pass_requires_exact_reproduction_route")
            if decision == "needs_builder_review":
                uncertain = {key for key, value in states.items() if value == "uncertain"}
                recovery_plan, recovery_errors = _recoverability_plan(
                    candidate.get("recoverability_plan"),
                    uncertain,
                    evidence_ids,
                    evidence_text_by_id or {},
                )
                normalized["recoverability_plan"] = recovery_plan
                reasons.extend(recovery_errors)
                expected_route = (
                    "normalized_reconstruction"
                    if any(
                        item.get("resolution_type") == "normalized_protocol"
                        or item.get("assumptions")
                        for item in recovery_plan.values()
                    )
                    else "evidence_recovery"
                )
                # Route is derived from the validated recovery plan. Treat a model's
                # stale route label as metadata normalization, not scientific rejection.
                builder_route = expected_route
                normalized["builder_route"] = expected_route
                if (
                    not uncertain
                    or uncertain - RECOVERABLE_DIMENSIONS
                    or any(value == "failed" for value in states.values())
                    or any(
                        states[key] != "confirmed"
                        for key in (
                            "scientific_significance",
                            "workflow_completeness",
                            "software",
                            "cost",
                            "leakage_risk",
                        )
                    )
                ):
                    reasons.append("builder_review_requirements_not_met")
        if not all(
            candidate.get(key)
            for key in (
                "scientific_question",
                "claim_reference",
                "public_input_requirements",
                "hidden_targets",
                "significance_rationale",
            )
        ):
            reasons.append("missing_required_scientific_fields")
        cited = set(normalized["evidence_ids"])
        resolved_cited, unknown_cited = _resolve_evidence_ids(cited, evidence_ids)
        normalized["evidence_ids"] = sorted(resolved_cited)
        if not cited or unknown_cited:
            reasons.append("unknown_or_missing_mineru_evidence_ids")
        required = _software_list(candidate.get("required_software"))
        normalized_required = []
        unknown_software = []
        for name in required:
            identifier = software_lookup.get(_software_key(name))
            if identifier:
                normalized_required.append(identifier)
            else:
                unknown_software.append(name)
        if not required:
            reasons.append("required_software_missing")
        if unknown_software:
            reasons.append("required_software_not_stage04_covered")
        normalized["required_software"] = list(dict.fromkeys(normalized_required))
        normalized["candidate_id"] = candidate_id
        if reasons:
            rejected.append(
                {
                    "candidate_id": candidate_id,
                    "reasons": list(dict.fromkeys(reasons)),
                    "unknown_software": unknown_software,
                    "unknown_evidence_ids": sorted(unknown_cited),
                }
            )
            continue
        output.append(normalized)
    return output, rejected


def _workflow_steps(value):
    if not isinstance(value, list):
        return []
    output = []
    for item in value:
        if not isinstance(item, dict):
            continue
        output.append(
            {
                "step_id": str(item.get("step_id") or "").strip(),
                "action": str(item.get("action") or "").strip(),
                "depends_on": _string_list(item.get("depends_on")),
                "input_artifact": str(item.get("input_artifact") or "").strip(),
                "output_artifact": str(item.get("output_artifact") or "").strip(),
                "software": str(item.get("software") or "").strip(),
                "method_parameters": item.get("method_parameters")
                if isinstance(item.get("method_parameters"), dict)
                else {},
                "evidence_ids": _string_list(item.get("evidence_ids")),
            }
        )
    return output


def _workflow_graph_errors(steps, evidence_ids):
    reasons = []
    if len(steps) < MINIMUM_SCIENTIFIC_STEPS:
        return ["workflow_graph_requires_two_scientific_steps"]
    step_ids = [step["step_id"] for step in steps]
    if any(not value for value in step_ids) or len(set(step_ids)) != len(step_ids):
        reasons.append("workflow_graph_step_ids_invalid")
    known = set(step_ids)
    previous = set()
    adjacency = {step_id: set() for step_id in step_ids}
    has_edge = False
    for step in steps:
        if not all(
            step.get(key)
            for key in ("action", "input_artifact", "output_artifact", "evidence_ids")
        ):
            reasons.append("workflow_graph_step_fields_missing")
            break
        dependencies = set(step["depends_on"])
        has_edge = has_edge or bool(dependencies)
        if dependencies - previous or step["step_id"] in dependencies:
            reasons.append("workflow_graph_dependency_invalid")
            break
        for dependency in dependencies:
            adjacency[step["step_id"]].add(dependency)
            adjacency[dependency].add(step["step_id"])
        resolved, unknown = _resolve_evidence_ids(step["evidence_ids"], evidence_ids)
        step["evidence_ids"] = sorted(resolved)
        if not resolved:
            reasons.append("workflow_graph_unknown_evidence_ids")
            break
        previous.add(step["step_id"])
    if not has_edge:
        reasons.append("workflow_graph_missing_dependency_edge")
    if step_ids and not reasons:
        visited = set()
        pending = [step_ids[0]]
        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            pending.extend(adjacency[current] - visited)
        if visited != known:
            reasons.append("workflow_graph_disconnected_step")
    return list(dict.fromkeys(reasons))


def _audit_dimensions(value, evidence_ids):
    if not isinstance(value, dict) or set(value) != set(AUDIT_DIMENSIONS):
        return {}, ["invalid_audit_dimensions"]
    output = {}
    reasons = []
    for key in AUDIT_DIMENSIONS:
        item = value.get(key)
        if not isinstance(item, dict):
            reasons.append("invalid_audit_dimensions")
            continue
        state = str(item.get("state") or "").casefold()
        support = str(item.get("support") or "").strip()
        missing_fields = _string_list(item.get("missing_fields"))
        cited = _string_list(item.get("evidence_ids"))
        resolved, unknown = _resolve_evidence_ids(cited, evidence_ids)
        output[key] = {
            "state": state,
            "support": support,
            "missing_fields": missing_fields,
            "evidence_ids": sorted(resolved),
        }
        if state not in {"confirmed", "uncertain", "failed"} or not support:
            reasons.append(f"invalid_audit_dimension:{key}")
        if state in {"confirmed", "failed"} and key in SOURCE_EVIDENCE_DIMENSIONS and not resolved:
            reasons.append(f"audit_dimension_evidence_invalid:{key}")
        if state == "uncertain" and not missing_fields:
            reasons.append(f"audit_dimension_missing_fields_required:{key}")
    return output, list(dict.fromkeys(reasons))


def _recoverability_plan(value, uncertain_dimensions, evidence_ids, evidence_text_by_id):
    if not isinstance(value, dict) or set(value) != set(uncertain_dimensions):
        return {}, ["invalid_recoverability_plan_dimensions"]
    output = {}
    reasons = []
    for dimension in sorted(uncertain_dimensions):
        item = value.get(dimension)
        if not isinstance(item, dict):
            reasons.append(f"invalid_recoverability_plan:{dimension}")
            continue
        resolution_type = str(item.get("resolution_type") or "").strip()
        procedure = str(item.get("procedure") or "").strip()
        cited = _string_list(item.get("source_evidence_ids"))
        resolved, _ = _resolve_evidence_ids(cited, evidence_ids)
        assumptions = _string_list(item.get("assumptions"))
        target_independent = item.get("target_independent") is True
        identifier_kind = str(item.get("identifier_kind") or "").strip()
        identifier_value = str(item.get("identifier_value") or "").strip()
        protocol_id = str(item.get("protocol_id") or "").strip()
        if resolution_type == "normalized_protocol" and not protocol_id:
            # There is one versioned protocol in the current contract. Normalize a
            # missing constant instead of turning a model formatting omission into
            # a scientific rejection; Stage06 still receives the explicit ID.
            protocol_id = "researchchembench_normalized_v1"
        output[dimension] = {
            "resolution_type": resolution_type,
            "procedure": procedure,
            "source_evidence_ids": sorted(resolved),
            "target_independent": target_independent,
            "assumptions": assumptions,
            "identifier_kind": identifier_kind or None,
            "identifier_value": identifier_value or None,
            "protocol_id": protocol_id or None,
        }
        subjective_language = _target_guided_recovery_language(procedure)
        if resolution_type != "normalized_protocol" and not assumptions:
            subjective_language.extend(_subjective_recovery_language(procedure))
        type_mismatch = _recovery_type_mismatch(resolution_type, procedure)
        figure_coordinate_recovery = _figure_coordinate_recovery(procedure)
        identifier_valid = True
        if resolution_type == "explicit_identifier_retrieval":
            cited_text = "\n".join(
                evidence_text_by_id.get(evidence_id, "") for evidence_id in resolved
            )
            identifier_valid = bool(
                identifier_kind
                and identifier_value
                and identifier_value.casefold() in cited_text.casefold()
                and _looks_like_explicit_identifier(identifier_kind, identifier_value)
            )
        assumptions_valid = not assumptions or resolution_type in {
            "evidence_anchored_construction",
            "normalized_protocol",
        }
        normalized_protocol_valid = resolution_type != "normalized_protocol" or not (
            _normalized_protocol_errors(protocol_id, assumptions)
        )
        anchored_assumptions_valid = resolution_type != "evidence_anchored_construction" or not (
            _task_defining_assumption_errors([procedure, *assumptions])
        )
        if (
            resolution_type not in RECOVERY_TYPES
            or not procedure
            or not resolved
            or not target_independent
            or not assumptions_valid
            or subjective_language
            or type_mismatch
            or figure_coordinate_recovery
            or not identifier_valid
            or not normalized_protocol_valid
            or not anchored_assumptions_valid
        ):
            reasons.append(f"invalid_recoverability_plan:{dimension}")
    return output, reasons


def _subjective_recovery_language(procedure):
    """Catch procedures that leave scientific choices to defaults or hidden targets."""

    text = str(procedure or "").casefold()
    markers = (
        "reasonable number",
        "reasonable value",
        "reasonable bounds",
        "physically reasonable",
        "typical ",
        "standard practice",
        "standard crystallographic",
        "standard bulk",
        "as is customary",
        "common practice",
        "chemical intuition",
        "plausible model",
        "if not specified",
        "if unavailable",
        "adjust ",
        "match the hidden",
        "reproduces the reported",
        "agreement with the published",
        "fit to the target",
        "choose the value closest",
        "select the value closest",
    )
    return [marker for marker in markers if marker in text]


def _target_guided_recovery_language(procedure):
    text = str(procedure or "").casefold()
    markers = (
        "match the hidden",
        "match reported",
        "matching the reported",
        "reproduces the reported",
        "agreement with the published",
        "compare to the reported",
        "compared to the reported",
        "consistent with the reported",
        "fit to the target",
        "choose the value closest",
        "select the value closest",
    )
    return [marker for marker in markers if marker in text]


def _normalized_protocol_errors(protocol_id, assumptions):
    if protocol_id != "researchchembench_normalized_v1" or not assumptions:
        return ["normalized_protocol_identity_or_assumptions_missing"]
    return _task_defining_assumption_errors(assumptions)


def _task_defining_assumption_errors(assumptions):
    forbidden = (
        "charge",
        "multiplicity",
        "composition",
        "chemical identity",
        "structure identity",
        "defect placement",
        "defect configuration",
        "vacancy position",
        "exact position",
        "reaction path",
        "force field",
        "force-field",
        "stoichiometry",
        "morphology",
        "interface registry",
        "grain boundary",
        "gb model",
        "gb interface",
        "equilibrated configuration",
        "author-generated",
        "neutral form",
        "ionic form",
        "reasonable arrangement",
        "reasonable geometry",
        "chemical intuition",
        "manual placement",
        "manual docking",
        "cluster is represented",
        "represented by a small cluster",
        "cluster size",
        "cluster stoichiometry",
        "cluster geometry",
        "random insertion",
        "randomly insert",
        "representative configuration",
        "select representative",
        "select three structures",
        "similar one",
        "most common interpretation",
        "or alternative",
        "if evidence indicates otherwise",
        "reasonable choice",
        "exact metric",
        "metric used by the authors",
        "longest dimension or volume",
    )
    errors = []
    for assumption in assumptions:
        text = str(assumption).casefold()
        errors.extend(marker for marker in forbidden if marker in text)
        if any(
            marker in text
            for marker in (
                "may need to be chosen",
                "needs to be chosen",
                "need to be inferred",
                "may need to be inferred",
            )
        ):
            errors.append("unresolved task-defining choice")
        if "adsorption site" in text and not any(
            marker in text
            for marker in (
                "enumerat",
                "all ",
                "high-symmetry",
                "high symmetry",
                "top, bridge, hollow",
            )
        ):
            errors.append("adsorption site")
        if "termination" in text and not any(
            marker in text
            for marker in (
                "symmetric slab",
                "both sides equivalent",
                "reported termination",
                "specified termination",
            )
        ):
            errors.append("termination")
        if "orientation" in text and not any(
            marker in text for marker in ("enumerat", "all ", "reported", "described")
        ):
            errors.append("orientation")
        if "protonation" in text and not any(
            marker in text for marker in ("as depicted", "reported", "specified", "explicit")
        ):
            errors.append("protonation")
    return list(dict.fromkeys(errors))


def _recovery_type_mismatch(resolution_type, procedure):
    if resolution_type == "evidence_anchored_construction":
        return False
    text = str(procedure or "").casefold()
    construction_objects = (
        "slab",
        "structural model",
        "defect model",
        "configuration",
        "force field",
        "force-field",
        "simulation box",
        "supercell",
    )
    construction_verbs = ("construct", "build", "reconstruct", "create")
    return any(verb in text for verb in construction_verbs) and any(
        obj in text for obj in construction_objects
    )


def _figure_coordinate_recovery(procedure):
    text = str(procedure or "").casefold()
    return "coordinate" in text and any(
        marker in text for marker in ("from figure", "from the figure", "from figures")
    )


def _looks_like_explicit_identifier(kind, value):
    kind = str(kind).casefold().replace(" ", "_")
    value = str(value).strip()
    if kind in {"smiles", "inchi"}:
        return len(value) >= 3
    patterns = {
        "doi": r"^10\.\d{4,9}/\S+$",
        "ccdc": r"^(?:ccdc\s*)?\d{5,9}$",
        "icsd": r"^(?:icsd\s*)?\d{3,9}$",
        "cod": r"^(?:cod\s*)?\d{5,9}$",
        "pubchem_cid": r"^(?:cid\s*)?\d+$",
        "materials_project": r"^mp-\d+$",
    }
    pattern = patterns.get(kind)
    return bool(pattern and re.fullmatch(pattern, value, re.IGNORECASE))


def _valid_estimated_cost(value, stage04):
    if not isinstance(value, dict) or not str(value.get("basis") or "").strip():
        return False
    if value.get("confidence") not in {"high", "medium"}:
        return False
    numeric = {}
    for key in ("runtime_hours", "cpu_cores", "gpus", "job_count"):
        raw = value.get(key)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or raw < 0:
            return False
        numeric[key] = float(raw)
    if numeric["runtime_hours"] <= 0 or numeric["cpu_cores"] <= 0 or numeric["job_count"] <= 0:
        return False
    budget = (stage04.get("resource_profile") or {}).get("budget") or {}
    comparisons = {
        "runtime_hours": numeric["runtime_hours"],
        "cpu_cores": numeric["cpu_cores"],
        "gpus": numeric["gpus"],
        "job_count": numeric["job_count"],
        "core_hours": numeric["runtime_hours"] * numeric["cpu_cores"],
        "gpu_hours": numeric["runtime_hours"] * numeric["gpus"],
    }
    return not any(
        key in budget and float(budget[key]) < amount for key, amount in comparisons.items()
    )


def _covered_software_lookup(stage04):
    lookup: dict[str, str] = {}
    for row in stage04.get("software_mappings") or []:
        if not _is_required_software_mapping(row) or not row.get("catalog_present"):
            continue
        identifier = str(
            row.get("normalized_identifier")
            or row.get("normalized_backend")
            or row.get("raw_name")
            or ""
        )
        if not identifier:
            continue
        for value in (
            identifier,
            row.get("normalized_backend"),
            row.get("raw_name"),
        ):
            if value:
                lookup[_software_key(value)] = identifier
    return lookup


def _stage05_software_context(blocks, stage04, *, aliases, external_aliases, profile):
    """Use MinerU text to resolve Stage03 inventory gaps without changing old facts."""

    facts = _software_coverage_facts(stage04)
    lookup = _covered_software_lookup(stage04)
    if not aliases or not profile:
        facts["mineru_catalog_mentions"] = []
        return facts, lookup
    detected = find_software_mentions(
        blocks,
        _merge_detection_aliases(aliases, external_aliases),
    )
    synthetic_mentions = [
        {
            "raw_name": row.get("raw_name"),
            "entity_type": "program",
            "role": "unknown",
            "actual_use": True,
            "workflow_ids": [],
            "evidence_ids": [row.get("evidence_id")],
        }
        for row in detected
        if row.get("raw_name") and row.get("evidence_id")
    ]
    mappings = resolve_software(
        synthetic_mentions,
        aliases,
        profile,
        external_aliases=external_aliases,
    )
    mention_facts = []
    for mapping in mappings:
        mention_facts.append(
            {
                "paper_name": mapping.get("raw_name"),
                "toolbox_identifier": mapping.get("normalized_identifier"),
                "coverage_state": mapping.get("coverage_state"),
                "name_resolution": mapping.get("name_resolution"),
                "evidence_ids": mapping.get("evidence_ids") or [],
                "candidate_only": True,
            }
        )
        if mapping.get("catalog_present"):
            identifier = str(mapping.get("normalized_identifier") or "")
            for value in (mapping.get("raw_name"), identifier):
                if value and identifier:
                    lookup[_software_key(value)] = identifier
    facts["mineru_catalog_mentions"] = mention_facts
    facts["rule"] += (
        " MinerU catalog mentions are high-recall candidates, not proof of workflow use; "
        "the auditor must bind a cited mention to the candidate workflow."
    )
    return facts, lookup


def _software_coverage_facts(stage04):
    covered, uncovered, unconfirmed = [], [], []
    for row in stage04.get("software_mappings") or []:
        if not _is_required_software_mapping(row):
            continue
        fact = {
            "paper_name": row.get("raw_name"),
            "toolbox_identifier": row.get("normalized_identifier")
            or row.get("normalized_backend"),
            "role": row.get("role"),
            "workflow_ids": _string_list(row.get("workflow_ids")),
        }
        state = str(row.get("coverage_state") or "")
        if row.get("catalog_present"):
            covered.append(fact)
        elif state == "uncovered" or row.get("external_identifier"):
            uncovered.append(fact)
        else:
            unconfirmed.append(fact)
    return {
        "covered_required_software": covered,
        "uncovered_required_software": uncovered,
        "unconfirmed_required_software": unconfirmed,
        "inventory_status": stage04.get("coverage_decision"),
        "workflow_coverage_results": stage04.get("workflow_coverage_results") or [],
        "rule": (
            "Only uncovered_required_software may be reported as absent from the toolbox. "
            "A covered entry may still be unusable for a non-software reason, but must not be "
            "described as missing from the catalog. Unconfirmed entries are not uncovered."
        ),
    }


def _is_required_software_mapping(row):
    if row.get("actual_use") is False:
        return False
    return str(row.get("role") or "unknown").casefold() not in {
        "background",
        "instrumentation",
        "optional_auxiliary",
        "visualization",
    }


def _software_fact_contradictions(response, stage04):
    blocking = _software_list(response.get("blocking_software"))
    if not blocking:
        return []
    if str(response.get("decision") or "").casefold() in {"pass", "needs_builder_review"}:
        return [
            {
                "candidate_id": "response-software-facts",
                "reasons": ["pass_response_has_blocking_software"],
            }
        ]
    uncovered = {
        _software_key(value)
        for row in _software_coverage_facts(stage04)["uncovered_required_software"]
        for value in (row.get("paper_name"), row.get("toolbox_identifier"))
        if value
    }
    invalid = [name for name in blocking if _software_key(name) not in uncovered]
    if not invalid:
        return []
    return [
        {
            "candidate_id": "response-software-facts",
            "reasons": [f"blocking_software_not_in_uncovered_facts:{name}" for name in invalid],
        }
    ]


def _response_contract_rejections(response, stage04, evidence_ids=None):
    decision = str(response.get("decision") or "").casefold()
    dimensions = _string_list(response.get("blocking_dimensions"))
    review_dimensions = _string_list(response.get("review_dimensions"))
    review_reasons = _string_list(response.get("review_reasons"))
    allowed = {
        "input_assets",
        "parameters",
        "ground_truth",
        "software",
        "cost",
        "scientific_significance",
        "workflow_completeness",
        "leakage_risk",
    }
    blocking_software = _software_list(response.get("blocking_software"))
    inventory_unconfirmed = (
        _software_coverage_facts(stage04).get("inventory_status")
        == "software_inventory_unconfirmed"
    )
    reasons = []
    if decision not in {"pass", "needs_builder_review", "reject"}:
        reasons.append("invalid_decision")
    if decision in {"pass", "needs_builder_review"} and (dimensions or blocking_software):
        reasons.append("pass_response_has_blockers")
    if decision == "pass" and (review_dimensions or review_reasons):
        reasons.append("pass_response_has_review_items")
    if decision == "needs_builder_review":
        if not review_dimensions or not review_reasons:
            reasons.append("builder_review_missing_review_items")
        if set(review_dimensions) - {"input_assets", "parameters", "ground_truth"}:
            reasons.append("invalid_builder_review_dimensions")
    if decision == "reject":
        if not dimensions:
            reasons.append("reject_missing_blocking_dimensions")
        if set(dimensions) - allowed:
            reasons.append("invalid_blocking_dimensions")
        if blocking_software and "software" not in dimensions:
            reasons.append("software_dimension_and_blocking_software_disagree")
        if "software" in dimensions and not (blocking_software or inventory_unconfirmed):
            reasons.append("software_dimension_and_blocking_software_disagree")
        if review_dimensions or review_reasons:
            reasons.append("reject_response_has_review_items")
        if evidence_ids is not None:
            reasons.extend(_hard_blocker_errors(response.get("hard_blockers"), evidence_ids))
    if not reasons:
        return []
    return [{"candidate_id": "response-contract", "reasons": reasons}]


def _hard_blocker_errors(value, evidence_ids):
    if not isinstance(value, list) or not value:
        return ["reject_missing_hard_blockers"]
    reasons = []
    for item in value:
        if not isinstance(item, dict):
            reasons.append("invalid_hard_blocker")
            continue
        code = str(item.get("code") or "").casefold()
        dimension = str(item.get("dimension") or "").casefold()
        rationale = str(item.get("reason") or "").strip()
        cited = _string_list(item.get("evidence_ids"))
        resolved, unknown = _resolve_evidence_ids(cited, evidence_ids)
        if code not in HARD_BLOCKER_CODES or dimension not in AUDIT_DIMENSIONS or not rationale:
            reasons.append("invalid_hard_blocker")
        if code not in {"essential_software_uncovered", "cost_exceeds_budget"} and (
            not resolved or unknown
        ):
            reasons.append("hard_blocker_evidence_invalid")
    return list(dict.fromkeys(reasons))


def _software_list(value):
    values = _string_list(value)
    output = []
    for item in values:
        output.extend(part.strip() for part in re.split(r"[,;]", item) if part.strip())
    return list(dict.fromkeys(output))


def _resolve_evidence_ids(cited, available):
    """Resolve exact IDs or a model-shortened ID with one unique hash suffix."""

    available = {str(value) for value in available}
    resolved, unknown = set(), set()
    for value in {str(item) for item in cited}:
        if value in available:
            resolved.add(value)
            continue
        matches = [candidate for candidate in available if candidate.startswith(f"{value}_")]
        if len(matches) == 1:
            resolved.add(matches[0])
        else:
            unknown.add(value)
    return resolved, unknown


def _string_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _software_key(value):
    return re.sub(r"[^a-z0-9+]", "", str(value).casefold())


def _without_evidence_ids(value):
    if isinstance(value, dict):
        return {
            key: _without_evidence_ids(item) for key, item in value.items() if key != "evidence_ids"
        }
    if isinstance(value, list):
        return [_without_evidence_ids(item) for item in value]
    return value


def _document_inventory(documents):
    return [
        {
            "document_id": document.get("document_id"),
            "document_role": document.get("document_role"),
            "title": document.get("title"),
            "selected_parser": document.get("selected_parser"),
            "source_name": Path(str(document.get("source_path") or "")).name,
        }
        for document in documents
    ]


def _router_index_blocks(blocks, stage04, limit):
    """Build a broad, balanced index while prioritizing dynamically known software."""

    selected = _bounded_by_document(blocks, limit)
    selected_ids = {str(block.get("evidence_id")) for block in selected}
    names = {
        str(value).casefold()
        for row in stage04.get("software_mappings") or []
        for value in (
            row.get("raw_name"),
            row.get("normalized_identifier"),
            row.get("normalized_backend"),
        )
        if value and len(str(value).strip()) >= 3
    }
    if not names:
        return selected

    remaining = max(0, int(limit) - sum(len(str(row.get("text") or "")) for row in selected))
    for block in blocks:
        if remaining <= 0:
            break
        evidence_id = str(block.get("evidence_id"))
        text = str(block.get("text") or "")
        if evidence_id in selected_ids or not any(name in text.casefold() for name in names):
            continue
        compact = _compact_block(block)
        if len(text) > remaining:
            compact["text"] = text[:remaining]
            compact["selection_note"] = "text_truncated_for_stage05_router_index"
        selected.append(compact)
        selected_ids.add(evidence_id)
        remaining -= len(str(compact.get("text") or ""))
    return selected


def _sanitize_evidence_route(response, available_ids, *, candidate_limit):
    decision = str(response.get("decision") or "").casefold()
    if decision not in {"computational_candidates_found", "no_candidate_located"}:
        decision = "no_candidate_located"
    coverage = str(response.get("coverage_status") or "").casefold()
    if coverage not in {"complete", "partial"}:
        coverage = "partial"
    warnings = []
    clusters = []
    for index, raw in enumerate((response.get("workflow_clusters") or [])[:candidate_limit]):
        if not isinstance(raw, dict):
            warnings.append(f"workflow_cluster_{index + 1}_not_object")
            continue
        cluster = {
            "candidate_id": str(raw.get("candidate_id") or f"candidate-{index + 1}"),
            "task_directions": [
                value for value in _string_list(raw.get("task_directions")) if value in TASK_DIRECTIONS
            ],
            "scientific_question": str(raw.get("scientific_question") or "").strip(),
            "related_section_ranges": _string_list(raw.get("related_section_ranges")),
            "missing_evidence": _string_list(raw.get("missing_evidence")),
        }
        for field in (
            "method_evidence_ids",
            "input_evidence_ids",
            "parameter_evidence_ids",
            "result_evidence_ids",
            "claim_evidence_ids",
            "cost_evidence_ids",
        ):
            cited = _string_list(raw.get(field))
            resolved, unknown = _resolve_evidence_ids(cited, available_ids)
            cluster[field] = sorted(resolved)
            if unknown:
                warnings.append(
                    f"{cluster['candidate_id']}:{field}:unknown:{','.join(sorted(unknown))}"
                )
        clusters.append(cluster)
    if decision == "computational_candidates_found" and not clusters:
        warnings.append("candidate_decision_without_valid_clusters")
    return (
        {
            "decision": decision,
            "coverage_status": coverage,
            "workflow_clusters": clusters,
            "unresolved_locations": _string_list(response.get("unresolved_locations")),
            "rationale": str(response.get("rationale") or "").strip(),
            "confidence": str(response.get("confidence") or "").casefold(),
        },
        warnings,
    )


def _auditor_evidence_blocks(blocks, route, limit):
    """Expand routed evidence to neighboring and same-section MinerU blocks."""

    if not blocks or limit <= 0:
        return []
    cited = list(
        dict.fromkeys(
            evidence_id
            for cluster in route.get("workflow_clusters") or []
            for field in (
                "method_evidence_ids",
                "input_evidence_ids",
                "parameter_evidence_ids",
                "result_evidence_ids",
                "claim_evidence_ids",
                "cost_evidence_ids",
            )
            for evidence_id in cluster.get(field) or []
        )
    )
    index_by_id = {str(block.get("evidence_id")): index for index, block in enumerate(blocks)}
    priority = []

    def add(index):
        if 0 <= index < len(blocks) and index not in priority:
            priority.append(index)

    routed_sections = set()
    for evidence_id in cited:
        index = index_by_id.get(str(evidence_id))
        if index is None:
            continue
        for neighbor in range(index - 2, index + 3):
            if (
                0 <= neighbor < len(blocks)
                and blocks[neighbor].get("document_id") == blocks[index].get("document_id")
            ):
                add(neighbor)
        section = tuple(str(item) for item in (blocks[index].get("section_path") or []) if item)
        if section:
            routed_sections.add((str(blocks[index].get("document_id") or ""), section))
    for index, block in enumerate(blocks):
        section = tuple(str(item) for item in (block.get("section_path") or []) if item)
        if section and (str(block.get("document_id") or ""), section) in routed_sections:
            add(index)

    fallback = _bounded_by_document(blocks, limit)
    fallback_ids = [str(block.get("evidence_id")) for block in fallback]
    for evidence_id in fallback_ids:
        index = index_by_id.get(evidence_id)
        if index is not None:
            add(index)

    selected = []
    used = 0
    max_block_characters = max(1024, min(20000, int(limit) // 5))
    for index in priority:
        compact = _compact_block(blocks[index])
        text = str(compact.get("text") or "")
        available = int(limit) - used
        if available <= 0:
            break
        if len(text) > min(available, max_block_characters):
            text = text[: min(available, max_block_characters)]
            compact["text"] = text
            compact["selection_note"] = "text_truncated_for_stage05_auditor_packet"
        selected.append(compact)
        used += len(text)
    return selected


_STAGE05_RELEVANCE_PATTERNS = (
    re.compile(
        r"\b(comput(?:ational|ation)|theoretic|simulation|method(?:s|ology)?|model(?:ling|ing)?|"
        r"density functional|dft|tddft|ab initio|molecular dynamics|monte carlo|kinetic|"
        r"transition state|reaction path|free energy|adsorption|electronic structure)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(cartesian|coordinate|geometry|structure|cif|xyz|poscar|smiles|unit cell|"
        r"lattice|force field|parameter|basis set|functional|pseudopotential|k[- ]?point)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(result|discussion|conclusion|energy|barrier|frequency|spectrum|trajectory|"
        r"selectivity|mechanism|rate constant|descriptor|validation|agreement|error)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(cpu|gpu|core|memory|wall ?time|runtime|node|hour|day|step|window|replica|"
        r"configuration|structure|calculation|job)\b",
        re.IGNORECASE,
    ),
)


def _compact_block(block):
    return {
        key: block.get(key)
        for key in ("evidence_id", "document_id", "page", "section_path", "text")
    }


def _block_relevance(block):
    text = " ".join(
        [
            *[str(item) for item in (block.get("section_path") or [])],
            str(block.get("text") or ""),
        ]
    )
    return sum(bool(pattern.search(text)) for pattern in _STAGE05_RELEVANCE_PATTERNS)


def _select_document_blocks(blocks, limit):
    """Select a bounded, auditable cross-section of one MinerU document."""

    if not blocks or limit <= 0:
        return []
    max_block_characters = max(512, min(12000, int(limit) // 4))
    compact = []
    for block in blocks:
        value = _compact_block(block)
        text = str(value.get("text") or "")
        if len(text) > max_block_characters:
            value["text"] = text[:max_block_characters]
            value["selection_note"] = "text_truncated_for_stage05_packet"
        compact.append(value)
    sizes = [len(str(block.get("text") or "")) for block in compact]
    priority: list[int] = []

    def prioritize(index):
        if 0 <= index < len(compact) and index not in priority:
            priority.append(index)

    # Give the title/abstract a small guaranteed allocation, then prioritize
    # method/result evidence before less informative document edges.
    lead_count = min(4, len(compact))
    for index in range(lead_count):
        prioritize(index)

    ranked = sorted(
        range(len(compact)),
        key=lambda index: (_block_relevance(compact[index]), sizes[index]),
        reverse=True,
    )
    for index in ranked:
        if _block_relevance(compact[index]) <= 0:
            break
        for neighbor in (index - 1, index, index + 1):
            prioritize(neighbor)

    edge_count = min(8, len(compact))
    for index in range(lead_count, edge_count):
        prioritize(index)
    for index in range(max(0, len(compact) - edge_count), len(compact)):
        prioritize(index)

    # Fill remaining space with evenly distributed blocks so an unusual method
    # description that lacks familiar keywords is not systematically omitted.
    sample_count = min(len(compact), max(8, int(math.sqrt(len(compact)) * 3)))
    if sample_count > 1:
        for position in range(sample_count):
            prioritize(round(position * (len(compact) - 1) / (sample_count - 1)))

    selected: set[int] = set()
    size = 0
    for index in priority:
        text_size = sizes[index]
        if size + text_size <= int(limit):
            selected.add(index)
            size += text_size
    return [compact[index] for index in sorted(selected)]


def _bounded_by_document(blocks, limit):
    by_document: dict[str, list[dict]] = {}
    for block in blocks:
        document_id = str(block.get("document_id") or "unknown")
        by_document.setdefault(document_id, []).append(block)
    if not by_document:
        return []
    per_document = max(1, int(limit) // len(by_document))
    return [
        block
        for document_blocks in by_document.values()
        for block in _select_document_blocks(document_blocks, per_document)
    ]

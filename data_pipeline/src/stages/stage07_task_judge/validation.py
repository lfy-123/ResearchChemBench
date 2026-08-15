from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.contracts import read_json
from src.stages.stage06_task_builder.validation import validate_task_pair

OUTCOME_TYPES = {
    "needs_software",
    "task_missing_data",
    "task_missing_ground_truth",
    "workflow_incomplete",
    "task_cost_too_high",
    "acceptance_rule_invalid",
    "mode_isolation_violation",
    "mode_pair_inconsistent",
    "provenance_incomplete",
    "toolbox_capability_unknown",
}


def deterministic_stage07_audit(pair_root: Path) -> dict[str, Any]:
    pair_audit = validate_task_pair(pair_root)
    outcomes: list[dict[str, Any]] = []
    for finding in pair_audit["findings"]:
        outcome_type = _finding_outcome_type(finding)
        outcomes.append(
            {
                "type": outcome_type,
                "severity": "blocking",
                "scope": _finding_scope(finding),
                "details": finding,
                "evidence_refs": [],
                "source": "deterministic",
            }
        )
    toolbox_path = pair_root / "toolbox_requirements.json"
    if toolbox_path.is_file():
        for requirement in read_json(toolbox_path):
            if not isinstance(requirement, dict):
                continue
            status = _toolbox_status(requirement)
            if status not in {"missing", "unknown", "incompatible"}:
                continue
            outcome_type = "toolbox_capability_unknown" if status == "unknown" else "needs_software"
            outcomes.append(
                {
                    "type": outcome_type,
                    "severity": "blocking" if requirement.get("blocking_now", True) else "major",
                    "scope": "both_modes",
                    "details": str(
                        requirement.get("suggested_action")
                        or requirement.get("requirement")
                        or requirement.get("capability")
                        or requirement.get("software")
                        or status
                    ),
                    "evidence_refs": requirement.get("evidence_ids") or [],
                    "source": "stage06_toolbox_requirement",
                }
            )
    return {
        "passed": not outcomes,
        "findings": pair_audit["findings"],
        "outcomes": _deduplicate_outcomes(outcomes),
        "pair_audit": pair_audit,
    }


_FINDING_OUTCOME_BY_CODE = {
    "missing_public_file": "task_missing_data",
    "inputs_directory_missing": "task_missing_data",
    "required_deliverables_missing": "task_missing_data",
    "task_spec_input_missing": "task_missing_data",
    "task_spec_input_path_invalid": "task_missing_data",
    "public_boundary_conditions_missing": "task_missing_data",
    "public_boundary_condition_invalid": "task_missing_data",
    "public_boundary_condition_name_missing": "task_missing_data",
    "public_boundary_condition_value_missing": "task_missing_data",
    "task_expected_boundary_conditions_missing": "task_missing_data",
    "task_instruction_boundary_missing": "task_missing_data",
    "task_instruction_boundary_conflict": "task_missing_data",
    "task_boundary_conditions_not_frozen_from_public_basis": "task_missing_data",
    "missing_ground_truth_common": "task_missing_ground_truth",
    "hidden_ground_truth_empty": "task_missing_ground_truth",
    "ground_truth_answer_missing": "task_missing_ground_truth",
    "ground_truth_not_scored": "task_missing_ground_truth",
    "ground_truth_profile_missing": "acceptance_rule_invalid",
    "acceptance_profile_ids_invalid": "acceptance_rule_invalid",
    "acceptance_profile_not_item_specific": "acceptance_rule_invalid",
    "invalid_acceptance_profile": "acceptance_rule_invalid",
    "numeric_acceptance_target_or_unit_missing": "acceptance_rule_invalid",
    "numeric_acceptance_tolerance_missing": "acceptance_rule_invalid",
    "categorical_acceptance_target_missing": "acceptance_rule_invalid",
    "ranking_acceptance_contract_missing": "acceptance_rule_invalid",
    "trend_acceptance_contract_missing": "acceptance_rule_invalid",
    "structure_acceptance_contract_missing": "acceptance_rule_invalid",
    "semantic_acceptance_contract_missing": "acceptance_rule_invalid",
    "artifact_acceptance_contract_missing": "acceptance_rule_invalid",
    "process_rubric_empty": "acceptance_rule_invalid",
    "process_rubric_criterion_invalid": "acceptance_rule_invalid",
    "process_rubric_total_invalid": "acceptance_rule_invalid",
    "conclusion_rubric_empty": "acceptance_rule_invalid",
    "conclusion_rubric_criterion_invalid": "acceptance_rule_invalid",
    "conclusion_rubric_total_invalid": "acceptance_rule_invalid",
    "hidden_answer_leakage": "mode_isolation_violation",
    "hidden_conclusion_leakage": "mode_isolation_violation",
    "autonomous_route_disclosure": "mode_isolation_violation",
    "autonomous_reproduction_file_present": "mode_isolation_violation",
    "mode_input_assets_differ": "mode_pair_inconsistent",
    "mode_submission_contract_differs": "mode_pair_inconsistent",
    "mode_pair_task_info_differs": "mode_pair_inconsistent",
    "mode_pair_task_spec_differs": "mode_pair_inconsistent",
    "mode_workflow_scope_not_frozen": "mode_pair_inconsistent",
    "mode_complexity_profile_not_frozen": "mode_pair_inconsistent",
    "missing_pair_metadata": "provenance_incomplete",
    "autonomous_copy_provenance_missing": "provenance_incomplete",
    "reproduction_copy_provenance_missing": "provenance_incomplete",
    "scope_underselected": "workflow_incomplete",
    "task_not_challenging": "workflow_incomplete",
}


def _finding_outcome_type(finding: str) -> str:
    code = str(finding).split(":", 1)[0]
    if code in _FINDING_OUTCOME_BY_CODE:
        return _FINDING_OUTCOME_BY_CODE[code]
    explicit_prefixes = (
        (("process_rubric_", "conclusion_rubric_", "acceptance_", "ground_truth_numeric_", "ground_truth_semantic_", "ground_truth_ranking_", "ground_truth_submission_"), "acceptance_rule_invalid"),
        (("hidden_answer_", "hidden_conclusion_", "autonomous_route_"), "mode_isolation_violation"),
        (("mode_pair_", "mode_input_", "mode_submission_"), "mode_pair_inconsistent"),
        (("workflow_scope_", "complexity_", "scientific_core_", "estimated_tool_"), "workflow_incomplete"),
    )
    return next(
        (
            outcome
            for prefixes, outcome in explicit_prefixes
            if any(code.startswith(prefix) for prefix in prefixes)
        ),
        "workflow_incomplete",
    )


def validate_agent_audit(response: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    summary = response.get("audit_summary")
    outcomes = response.get("outcomes") or []
    if summary == "passed_audit" and outcomes:
        findings.append("passed_audit_has_outcomes")
    if summary == "issues_found" and not outcomes:
        findings.append("issues_found_without_outcomes")
    if _contains_placeholder(response.get("toolbox_assessment")):
        findings.append("toolbox_assessment_placeholder")
    if _contains_placeholder(response.get("cost_assessment")):
        findings.append("cost_assessment_placeholder")
    if _contains_placeholder(response.get("rationale")):
        findings.append("audit_rationale_placeholder")
    for outcome in outcomes:
        if outcome.get("type") not in OUTCOME_TYPES:
            findings.append(f"invalid_outcome_type:{outcome.get('type')}")
        if outcome.get("severity") not in {"blocking", "major", "minor"}:
            findings.append(f"invalid_outcome_severity:{outcome.get('type')}")
        if outcome.get("scope") not in {
            "both_modes",
            "autonomous_research",
            "paper_reproduction",
            "hidden_reference",
            "provenance",
        }:
            findings.append(f"invalid_outcome_scope:{outcome.get('type')}")
        if not str(outcome.get("details") or "").strip():
            findings.append(f"outcome_details_missing:{outcome.get('type')}")
    return sorted(set(findings))


def _contains_placeholder(value: Any) -> bool:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True).casefold()
    return any(token in serialized for token in ("agent_required", "todo", "replace_me"))


def merge_audit_outcomes(
    deterministic: list[dict[str, Any]], model_outcomes: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    normalized = []
    for source, rows in (("deterministic", deterministic), ("agent", model_outcomes)):
        for row in rows:
            item = dict(row)
            item.setdefault("source", source)
            item.setdefault("evidence_refs", [])
            if source == "agent":
                item = _normalize_agent_toolbox_outcome(item)
            normalized.append(item)
    return _deduplicate_outcomes(normalized)


def _toolbox_status(requirement: dict[str, Any]) -> str:
    raw = str(
        requirement.get("status") or requirement.get("availability") or "unknown"
    ).casefold()
    aliases = {
        "available": "available",
        "installed": "available",
        "present": "available",
        "supported": "available",
        "declared_supported": "available",
        "missing": "missing",
        "absent": "missing",
        "not_installed": "missing",
        "incompatible": "incompatible",
        "unsupported": "incompatible",
        "unknown": "unknown",
        "unverified": "unknown",
        "not_evaluated": "unknown",
    }
    return aliases.get(raw, "unknown")


def _normalize_agent_toolbox_outcome(item: dict[str, Any]) -> dict[str, Any]:
    if item.get("type") != "needs_software":
        return item
    details = str(item.get("details") or "").casefold()
    unknown_markers = (
        "unknown",
        "unverified",
        "not verified",
        "not confirmed",
        "cannot verify",
        "cannot be verified",
        "does not document",
    )
    explicit_absence_markers = (
        "software is absent",
        "software is missing",
        "not installed",
        "explicitly unsupported",
        "incompatible",
    )
    if any(marker in details for marker in unknown_markers) and not any(
        marker in details for marker in explicit_absence_markers
    ):
        item["type"] = "toolbox_capability_unknown"
    return item


def _finding_scope(finding: str) -> str:
    if "autonomous" in finding:
        return "autonomous_research"
    if "reproduction" in finding:
        return "paper_reproduction"
    if "hidden" in finding or "ground_truth" in finding or "rubric" in finding:
        return "hidden_reference"
    if "metadata" in finding or "provenance" in finding:
        return "provenance"
    return "both_modes"


def _deduplicate_outcomes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        if any(_same_outcome(existing, row) for existing in output):
            continue
        output.append(row)
    return output


def _same_outcome(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if (left.get("type"), left.get("scope")) != (right.get("type"), right.get("scope")):
        return False
    left_details = str(left.get("details") or "").strip()
    right_details = str(right.get("details") or "").strip()
    if left_details == right_details:
        return True
    left_evidence = {
        str(value)
        for value in left.get("evidence_refs") or []
        if str(value).startswith(("ev_", "derived_"))
    }
    right_evidence = {
        str(value)
        for value in right.get("evidence_refs") or []
        if str(value).startswith(("ev_", "derived_"))
    }
    return bool(left_evidence & right_evidence)

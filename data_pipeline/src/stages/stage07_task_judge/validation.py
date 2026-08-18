from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.contracts import read_json
from src.core.toolbox_inventory import installed_software_inventory
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


def deterministic_stage07_audit(
    pair_root: Path, *, toolbox_snapshot: dict[str, Any] | None = None
) -> dict[str, Any]:
    pair_audit = validate_task_pair(pair_root)
    pair_audit["findings"] = sorted(
        set(pair_audit.get("findings") or [])
        | set(final_task_pair_integrity_findings(pair_root))
    )
    pair_audit["passed"] = not pair_audit["findings"]
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
    toolbox = installed_software_inventory(toolbox_snapshot or {})
    toolbox_path = pair_root / "toolbox_requirements.json"
    requirements = read_json(toolbox_path) if toolbox_path.is_file() else []
    reconciled_requirements, software_gaps = reconcile_toolbox_requirements(
        requirements, toolbox
    )
    if toolbox_path.is_file() and reconciled_requirements != requirements:
        toolbox_path.write_text(
            json.dumps(reconciled_requirements, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if toolbox_path.is_file():
        for requirement in reconciled_requirements:
            if not isinstance(requirement, dict):
                continue
            status = _toolbox_status(requirement)
            if status not in {"missing", "unknown", "incompatible"}:
                continue
            outcome_type = "toolbox_capability_unknown" if status == "unknown" else "needs_software"
            outcomes.append(
                {
                    "type": outcome_type,
                    "severity": "minor",
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
        "passed": bool(pair_audit.get("passed")),
        "findings": pair_audit["findings"],
        "outcomes": _deduplicate_outcomes(outcomes),
        "pair_audit": pair_audit,
        "toolbox_status": (
            "unknown"
            if not (toolbox.get("installed_software") or [])
            else ("needs_software" if software_gaps else "available")
        ),
        "required_additions": software_gaps,
    }


def _normalize_software_token(value: Any) -> str:
    """Normalize software family names while deliberately ignoring versions."""

    token = re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())
    token = re.sub(r"(?<=gaussian)(?:0?\d+)$", "", token)
    token = re.sub(r"(?<=cp2k)(?:\d+)$", "", token)
    token = re.sub(r"(?<=orca)(?:\d+)$", "", token)
    return token


def _software_token_variants(value: Any) -> set[str]:
    raw = str(value or "").strip().casefold()
    if not raw:
        return set()
    versionless = re.sub(
        r"\b(?:version|release|revision|rev|ver|v)?\s*\d+(?:[._-]\d+)*(?:[a-z]\d*)?\b",
        " ",
        raw,
    )
    return {
        token
        for token in (
            _normalize_software_token(raw),
            _normalize_software_token(versionless),
        )
        if token
    }


def software_matches_installed(name: Any, toolbox: dict[str, Any]) -> dict[str, Any] | None:
    requested = _software_token_variants(name)
    if not requested:
        return None
    inventory = toolbox.get("installed_software") or []
    for row in inventory:
        if not isinstance(row, dict):
            continue
        values = [row.get("software_id"), row.get("display_name"), *(row.get("aliases") or [])]
        available = set().union(*(_software_token_variants(value) for value in values))
        if requested & available:
            return row
        # Some citations attach a release directly to the family name (for
        # example VASP6 or CP2K2025). Versions are deliberately irrelevant to
        # Stage06/07 inventory matching.
        if any(
            len(base) >= 4
            and candidate.startswith(base)
            and re.fullmatch(r"v?\d+[a-z0-9]*", candidate[len(base) :])
            for candidate in requested
            for base in available
        ):
            return row
    if requested & {"g09", "g16", "gaussian09", "gaussian16", "gaussian"}:
        for row in inventory:
            if _normalize_software_token(row.get("software_id")) == "gaussian":
                return row
    return None


def reconcile_toolbox_requirements(
    requirements: Any, toolbox: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Resolve requirement names against installed software, without version checks."""

    normalized: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    inventory_available = bool(toolbox.get("installed_software") or [])
    rows = requirements if isinstance(requirements, list) else []
    for raw in rows:
        if not isinstance(raw, dict):
            continue
        item = dict(raw)
        name = item.get("software") or item.get("tool") or item.get("software_id") or item.get(
            "normalized_backend"
        )
        match = software_matches_installed(name, toolbox) if inventory_available else None
        if match is not None:
            # The file is a gap list, not an inventory.  A matched installed
            # program therefore has no entry in the normalized artifact.
            continue
        elif inventory_available and str(name or "").strip():
            item["status"] = "missing"
            gaps.append(
                {
                    "software": str(name),
                    "matched": False,
                    "details": (
                        f"Required software family '{name}' is absent from the installed "
                        "software inventory; software versions are not compared."
                    ),
                    "evidence_ids": item.get("evidence_ids") or [],
                }
            )
        else:
            item["status"] = "unknown"
        normalized.append(item)
    return normalized, gaps


def collect_referenced_evidence_ids(value: Any) -> set[str]:
    """Collect evidence references from structured task artifacts only."""

    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"evidence_id", "evidence_ids", "source_evidence_ids", "evidence_refs"}:
                if isinstance(item, str):
                    found.add(item)
                elif isinstance(item, list):
                    found.update(str(entry) for entry in item if isinstance(entry, str) and entry)
            found.update(collect_referenced_evidence_ids(item))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_referenced_evidence_ids(item))
    return found


def final_task_pair_integrity_findings(pair_root: Path) -> list[str]:
    evidence_path = pair_root / "evidence_index.json"
    if not evidence_path.is_file():
        return ["missing_pair_metadata:evidence_index.json"]
    try:
        evidence_rows = read_json(evidence_path)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return ["evidence_index_unreadable"]
    known = {
        str(row.get("evidence_id"))
        for row in evidence_rows
        if isinstance(row, dict) and row.get("evidence_id")
    }
    referenced: set[str] = set()
    for path in pair_root.rglob("*.json"):
        if path == evidence_path or "/." in path.as_posix():
            continue
        try:
            referenced.update(collect_referenced_evidence_ids(read_json(path)))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
    return [f"evidence_id_unknown:{identifier}" for identifier in sorted(referenced - known)]


_FINDING_OUTCOME_BY_CODE = {
    "missing_public_file": "task_missing_data",
    "inputs_directory_missing": "task_missing_data",
    "required_deliverables_missing": "task_missing_data",
    "task_spec_input_missing": "task_missing_data",
    "task_spec_input_path_invalid": "task_missing_data",
    "input_asset_empty": "task_missing_data",
    "input_asset_unreadable": "task_missing_data",
    "input_asset_placeholder": "task_missing_data",
    "input_asset_all_null_or_empty": "task_missing_data",
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
    "ground_truth_answer_placeholder": "task_missing_ground_truth",
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
        (("evidence_id_unknown", "evidence_index_"), "provenance_incomplete"),
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

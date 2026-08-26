from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from src.contracts import read_json, write_json

_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))
from researchchembench_contracts import schema_path_status
from researchchembench_contracts import process_rubric_container_findings
from src.stages.evaluator_reference import minimal_evaluator_findings, read_split_reference

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

_TASK_MODES = ("autonomous_research", "paper_reproduction")
_MODE_ALIASES = {
    "autonomous": "autonomous_research",
    "autonomous_research": "autonomous_research",
    "open_discovery": "autonomous_research",
    "reproduction": "paper_reproduction",
    "paper_reproduction": "paper_reproduction",
    "guided_reproduction": "paper_reproduction",
}


def validate_stage07_transport_contract(
    pair_root: Path, *, paper_id: str | None = None
) -> dict[str, Any]:
    """Validate the canonical pair without mutating or projecting any file."""
    findings: list[str] = []
    if paper_id:
        info_path = pair_root / "paper_info.json"
        if info_path.is_file():
            info = read_json(info_path)
            if isinstance(info, dict) and str(info.get("paper_id") or "") != paper_id:
                findings.append("paper_id_mismatch:paper_info")
    if read_split_reference(pair_root) is None:
        findings.append("evaluator_reference_missing")
    for mode in _TASK_MODES:
        root = pair_root / mode
        if not root.is_dir():
            findings.append(f"missing_mode_directory:{mode}")
            continue
        for filename in ("task_info.json", "task_spec.json", "submission_contract.json"):
            path = root / filename
            if not path.is_file():
                findings.append(f"missing_required_file:{mode}/{filename}")
                continue
            try:
                value = read_json(path)
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                findings.append(f"unreadable_mode_json:{mode}/{filename}")
                continue
            if filename in {"task_info.json", "task_spec.json"} and isinstance(value, dict):
                if paper_id and value.get("paper_id") != paper_id:
                    findings.append(f"paper_id_mismatch:{mode}")
                expected_mode = mode
                if value.get("mode") != expected_mode or value.get("scientific_mode") != expected_mode:
                    findings.append(f"mode_contract_mismatch:{mode}")
    return {"records": [], "new_records": [], "findings": sorted(set(findings))}

def stage07_mechanical_pre_publish_check(
    pair_root: Path, *, paper_id: str | None = None
) -> dict[str, Any]:
    """Validate the canonical Stage07 transport and split evaluator contract."""
    findings: list[str] = []
    diagnostics: list[str] = []
    required_modes = ("paper_reproduction", "autonomous_research")
    mode_values: dict[str, dict[str, Any]] = {}
    for mode in required_modes:
        root = pair_root / mode
        if not root.is_dir():
            findings.append(f"missing_mode_directory:{mode}")
            continue
        required_files = (
            "task.md", "task_info.json", "task_spec.json",
            "submission_contract.json", "process_rubric.json",
        )
        missing = [name for name in required_files if not (root / name).is_file()]
        findings.extend(f"missing_required_file:{mode}/{name}" for name in missing)
        if missing:
            continue
        try:
            info = read_json(root / "task_info.json")
            spec = read_json(root / "task_spec.json")
            submission = read_json(root / "submission_contract.json")
            rubric = read_json(root / "process_rubric.json")
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            findings.append(f"unreadable_mode_json:{mode}:{type(exc).__name__}")
            continue
        mode_values[mode] = {"info": info, "spec": spec, "submission": submission}
        expected_task_mode = "guided_reproduction" if mode == "paper_reproduction" else "open_discovery"
        if paper_id and info.get("paper_id") != paper_id:
            findings.append(f"paper_id_mismatch:{mode}")
        if info.get("task_id") not in (None, "", info.get("paper_id")):
            findings.append(f"task_id_not_equal_paper_id:{mode}")
        if info.get("mode") != mode or info.get("scientific_mode") != mode:
            findings.append(f"mode_contract_mismatch:{mode}")
        if info.get("task_mode") != expected_task_mode:
            findings.append(f"task_mode_contract_mismatch:{mode}")
        if spec.get("mode") != mode or spec.get("scientific_mode") != mode:
            findings.append(f"task_spec_mode_mismatch:{mode}")
        required = submission.get("required_files")
        if not isinstance(required, list) or not required:
            findings.append(f"submission_required_files_missing:{mode}")
        else:
            for rel in required:
                if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts or "\\" in rel:
                    findings.append(f"unsafe_required_path:{mode}:{rel}")
        if not isinstance(submission.get("results_schema"), dict):
            findings.append(f"submission_results_schema_missing:{mode}")
        rubric_findings = process_rubric_container_findings(rubric)
        findings.extend(f"{item}:{mode}" for item in rubric_findings if item != "process_rubric_empty")
        if mode == "paper_reproduction":
            route = [
                row for row in (rubric if isinstance(rubric, list) else [])
                if isinstance(row, dict) and str(row.get("criterion_type") or "").casefold() == "route_fidelity"
            ]
            if len(route) != 1:
                findings.append("reproduction_route_fidelity_criterion_missing")
        # Stage07 audits the exact files delivered by Stage06.  It must not
        # rewrite aliases or project a compatibility contract before checking.
        if (root / "hidden_reference").exists():
            findings.append(f"hidden_reference_in_public_mode:{mode}")
    if set(mode_values) == set(required_modes):
        ids = {str(mode_values[mode]["info"].get("paper_id") or "") for mode in required_modes}
        if len(ids) != 1:
            findings.append("mode_pair_identity_mismatch:paper_id")
    split_dir = pair_root / "evaluator_reference"
    required_split_files = (
        "reference_key_points.json", "reference_conclusions.json", "scoring_rules.json",
        "evidence_map.json", "critical_failures.json",
    )
    split_reference = read_split_reference(pair_root)
    missing_split = [name for name in required_split_files if not (split_dir / name).is_file()]
    if split_reference is None or missing_split:
        findings.append("evaluator_reference_missing")
        findings.extend(f"evaluator_reference_file_missing:{name}" for name in missing_split)
        evaluator = {"status": "failed", "findings": ["evaluator_reference_missing"], "diagnostics": []}
    else:
        evaluator_findings = minimal_evaluator_findings(pair_root)
        evaluator = {
            "status": "passed" if not evaluator_findings else "failed",
            "findings": sorted(set(evaluator_findings)),
            "diagnostics": [],
        }
        findings.extend(evaluator_findings)
    return {
        "mechanical_pre_publish_status": "passed" if not findings else "failed",
        "schema_load_diagnostic": evaluator["status"],
        "findings": sorted(set(findings)),
        "diagnostics": diagnostics,
        "evaluator": evaluator,
        "normalization_records": [],
    }



def _submission_contract_shape(value: Any) -> Any:
    """Return the mode-neutral structural shape of a submission contract.

    Autonomous conversion may rename result keys and neutralize labels.  The
    mechanical gate therefore compares required paths and schema structure,
    not mode-specific answer-bearing strings.
    """

    if isinstance(value, dict):
        shaped: dict[str, Any] = {}
        for key, item in value.items():
            if key in {"task_id", "paper_id", "mode", "scientific_mode"}:
                continue
            if key in {"required_files", "submission_path"}:
                # Each mode may use a neutral filename or a mode-specific
                # submission directory.  Those paths are validated within the
                # mode; literal cross-mode comparison is an unsafe disclosure
                # heuristic and creates false mechanical failures.
                continue
            elif key in {"result_schema", "results_schema"}:
                # The autonomous converter may neutralize answer-bearing field
                # names. Compare the JSON contract's type/cardinality shape,
                # not literal property names.
                shaped["results_schema"] = _result_schema_shape(item)
            else:
                shaped[key] = _submission_contract_shape(item)
        return shaped
    if isinstance(value, list):
        return [_submission_contract_shape(item) for item in value]
    return value


def _result_schema_shape(value: Any) -> Any:
    """Return a mode-neutral result-schema shape for the mechanical gate."""

    if not isinstance(value, dict):
        return {"type": type(value).__name__}
    result: dict[str, Any] = {"type": value.get("type", "object")}
    required = value.get("required")
    if isinstance(required, list):
        result["required_count"] = len(required)
    properties = value.get("properties")
    if isinstance(properties, dict):
        result["property_shapes"] = sorted(
            (_result_schema_shape(item) for item in properties.values()),
            key=lambda item: json.dumps(item, sort_keys=True),
        )
    items = value.get("items")
    if items is not None:
        result["items"] = _result_schema_shape(items)
    return result


def _string_list(value: Any) -> list[str]:
    """Normalize a scalar-or-array contract field without interpreting science."""

    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _jsonpath_tokens(value: Any) -> list[str | int] | None:
    """Parse the small JSONPath subset used by task submission bindings."""

    path = str(value or "").strip()
    # The Stage06 contract also permits a compact dotted field mapping (for
    # example ``frontier_orbitals.gap_ev``) in addition to JSONPath.  Treat it
    # as the equivalent ``$.frontier_orbitals.gap_ev`` selector for the
    # transport diagnostic; the evaluator still owns semantic scoring.
    if path and not path.startswith("$") and re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*", path
    ):
        return path.split(".")
    if path == "\u0024":
        return []
    if not path.startswith("\u0024"):
        return None
    tail = path[1:]
    tokens: list[str | int] = []
    position = 0
    token_pattern = re.compile(
        r"(?:\.([A-Za-z_][A-Za-z0-9_-]*)|\[(\*|\d+|['\"][^'\"]+['\"])\])"
    )
    while position < len(tail):
        match = token_pattern.match(tail, position)
        if match is None:
            return None
        dotted, bracket = match.groups()
        if dotted is not None:
            tokens.append(dotted)
        elif bracket == "*":
            tokens.append("*")
        elif bracket.isdigit():
            tokens.append(int(bracket))
        else:
            tokens.append(bracket[1:-1])
        position = match.end()
    return tokens


def _schema_path_status(schema: Any, tokens: list[str | int]) -> str:
    """Backward-compatible alias to the shared Task Package schema resolver."""

    return schema_path_status(schema, tokens)


def published_bundle_mechanical_check(bundle_root: Path) -> dict[str, Any]:
    """Check the final public bundle without judging its science."""

    findings: list[str] = []
    if not bundle_root.is_dir():
        return {"status": "failed", "findings": ["published_bundle_missing"]}
    # v8 publishes a Task Package v1.  Reuse its canonical structural/hash
    # validator instead of requiring the retired task_spec/submission_contract
    # files that belonged to the private audited tree.
    if (bundle_root / "package_manifest.json").is_file():
        # Keep this public helper usable when callers import validation.py
        # directly, without first importing package.py (which normally inserts
        # the repository root into sys.path as a side effect).
        import sys

        repo_root = Path(__file__).resolve().parents[4]
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        from researchchembench_contracts import validate_task_package

        package_report = validate_task_package(bundle_root)
        findings.extend(package_report.findings)
        return {
            "status": "passed" if not findings else "failed",
            "findings": sorted(set(findings)),
        }
    if (bundle_root / "hidden_reference").exists():
        findings.append("published_hidden_reference_present")
    forbidden = {"workspace", "source_materials", "handoff", "staging", "conversion_packet"}
    for path in bundle_root.rglob("*"):
        if path.is_dir() and path.name in forbidden:
            findings.append(f"published_internal_directory:{path.name}")
        if path.is_file() and path.suffix.casefold() == ".json":
            try:
                read_json(path)
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                findings.append(f"published_json_unreadable:{path.relative_to(bundle_root)}:{type(exc).__name__}")
    for name in ("task.md", "task_info.json", "task_spec.json", "submission_contract.json"):
        if not (bundle_root / name).is_file():
            findings.append(f"published_required_file_missing:{name}")
    return {"status": "passed" if not findings else "failed", "findings": sorted(set(findings))}


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

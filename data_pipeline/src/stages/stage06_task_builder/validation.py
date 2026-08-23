from __future__ import annotations

import json
import hashlib
import math
import re
import sys
from pathlib import Path
from typing import Any

from src.agents.workspace import directory_manifest, validate_relative_path
from src.contracts import canonical_hash, read_json, write_json

ACCEPTANCE_TYPES = {
    "numeric_tolerance",
    "categorical",
    "ranking",
    "trend",
    "structure_identity",
    "geometry_metric",
    "mechanism_claim",
    "semantic_propositions",
    "artifact_validation",
}
WORKFLOW_SCOPE_KINDS = {
    "full_paper_core_workflow",
    "core_scientific_subworkflow",
    # Legacy spellings remain readable during migration. New prompts emit only
    # the two objective-centered kinds above.
    "full_paper_computational_workflow",
    "major_paper_workflow",
    "partial_computational_subworkflow",
}
TASK_PAIR_CONTRACT_VERSION = "researchchembench.task-pair-contract.v2"
DEFAULT_RESULT_SCHEMA = {
    "type": "object",
    "description": "Structured report/results.json submitted by the evaluated agent.",
    "additionalProperties": True,
}
SCIENTIFIC_FAILURE_CODES = {
    "no_author_performed_computation",
    "missing_core_input",
    "incomplete_computational_process",
    "missing_ground_truth",
    "source_evidence_insufficient",
    "resource_infeasible",
    "no_complete_nontrivial_workflow",
    "benchmark_not_challenging",
}

TASK_MODES = ("autonomous_research", "paper_reproduction")
MODE_ALIASES = {
    "autonomous": "autonomous_research",
    "autonomous_research": "autonomous_research",
    "open_discovery": "autonomous_research",
    "reproduction": "paper_reproduction",
    "paper_reproduction": "paper_reproduction",
    "guided_reproduction": "paper_reproduction",
}


def normalize_mode_scope(value: Any) -> list[str] | None:
    """Normalize an optional Ground Truth/profile applicability list."""

    if value is None:
        return list(TASK_MODES)
    raw = [value] if isinstance(value, str) else value
    if not isinstance(raw, (list, tuple, set)):
        return None
    normalized: list[str] = []
    for item in raw:
        key = str(item or "").strip().casefold()
        mapped = MODE_ALIASES.get(key)
        if mapped and mapped not in normalized:
            normalized.append(mapped)
        elif key:
            return None
    if not normalized:
        return None
    return [mode for mode in TASK_MODES if mode in normalized]


def acceptance_profile_type_findings(
    profile: dict[str, Any], *, identifier: str | None = None
) -> list[str]:
    """Validate only the typed shape of one acceptance profile.

    This helper deliberately does not compare a target with a paper value or decide
    whether a scientific claim is important.  It checks that a profile has enough
    typed data for a downstream evaluator to interpret it.  A vector-valued numeric
    target may use an explicit ``numeric_tolerances`` map (for example one tolerance
    per reported quantity) instead of a single scalar tolerance and unit; the map is
    accepted only when every entry is a finite non-negative number.
    """

    identifier = str(identifier or profile.get("acceptance_profile_id") or "missing")
    profile_type = str(profile.get("type") or "")
    findings: list[str] = []
    if profile_type not in ACCEPTANCE_TYPES:
        findings.append(f"invalid_acceptance_profile:{identifier}")
    elif profile_type == "numeric_tolerance":
        target_present = profile.get("target") is not None
        unit_present = bool(str(profile.get("unit") or "").strip())
        raw_vector_tolerances = profile.get("numeric_tolerances")
        vector_tolerances_valid = isinstance(raw_vector_tolerances, dict) and bool(
            raw_vector_tolerances
        )
        if vector_tolerances_valid:
            for key, value in raw_vector_tolerances.items():
                if (
                    not str(key).strip()
                    or not isinstance(value, (int, float))
                    or isinstance(value, bool)
                    or not math.isfinite(float(value))
                    or float(value) < 0
                ):
                    vector_tolerances_valid = False
                    break
        if not target_present or not (unit_present or vector_tolerances_valid):
            findings.append(f"numeric_acceptance_target_or_unit_missing:{identifier}")
        scalar_tolerance_present = False
        for key in ("absolute_tolerance", "relative_tolerance"):
            value = profile.get(key)
            if value is None:
                continue
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(float(value))
                or float(value) < 0
            ):
                findings.append(f"numeric_acceptance_tolerance_invalid:{identifier}:{key}")
            else:
                scalar_tolerance_present = True
        if not scalar_tolerance_present and not vector_tolerances_valid:
            findings.append(f"numeric_acceptance_tolerance_missing:{identifier}")
    elif profile_type == "categorical" and profile.get("target") is None:
        findings.append(f"categorical_acceptance_target_missing:{identifier}")
    elif profile_type == "ranking" and not (
        profile.get("target_order") or profile.get("required_pairwise_relations")
    ):
        findings.append(f"ranking_acceptance_contract_missing:{identifier}")
    elif profile_type == "trend" and not profile.get("required_trends"):
        findings.append(f"trend_acceptance_contract_missing:{identifier}")
    elif profile_type in {"structure_identity", "geometry_metric"} and not (
        profile.get("target") or profile.get("metrics")
    ):
        findings.append(f"structure_acceptance_contract_missing:{identifier}")
    elif profile_type in {"mechanism_claim", "semantic_propositions"} and not profile.get(
        "required_propositions"
    ):
        findings.append(f"semantic_acceptance_contract_missing:{identifier}")
    elif profile_type == "artifact_validation" and not profile.get("required_artifacts"):
        findings.append(f"artifact_acceptance_contract_missing:{identifier}")
    return findings


def canonicalize_complexity_profile(profile: Any) -> dict[str, Any]:
    """Keep only the small, task-level complexity contract.

    Workflow topology belongs to ``workflow_steps`` and process metadata belongs to the
    process rubric.  This helper deliberately does not synthesize counts or aliases.
    """

    value = dict(profile) if isinstance(profile, dict) else {}
    output = {
        key: value[key]
        for key in ("level", "rationale", "estimated_tool_calls")
        if key in value
    }
    if isinstance(output.get("estimated_tool_calls"), dict):
        calls = output["estimated_tool_calls"]
        output["estimated_tool_calls"] = {
            key: calls[key] for key in ("min", "typical") if key in calls
        }
    return output


def normalize_scientific_requirements(value: Any) -> list[str]:
    """Project agent-friendly requirement records onto the evaluator's string contract.

    Agents may use a useful ``{"id": ..., "requirement": ...}`` record while drafting a
    task.  ``TaskInfo`` intentionally exposes only a compact list of requirement strings;
    this projection carries the scientific wording forward without making the transport
    schema a second scientific rubric.  It is mechanical normalization, not validation.
    """

    if not isinstance(value, list):
        return []
    normalized: list[str] = []
    for item in value:
        if isinstance(item, str):
            text = item.strip()
        elif isinstance(item, dict):
            text = str(
                item.get("requirement")
                or item.get("description")
                or item.get("text")
                or ""
            ).strip()
        else:
            text = str(item).strip()
        if text:
            normalized.append(text)
    return normalized


def normalize_required_deliverables(
    value: Any, *, fallback_paths: list[str] | None = None
) -> list[dict[str, Any]]:
    """Project common deliverable spellings onto the evaluator object contract.

    Agents sometimes emit the compact ``["report/results.json", ...]`` form,
    while ``TaskInfo`` requires ``RequiredDeliverable`` objects.  This helper
    only normalizes that transport representation; it does not add or remove
    scientific outputs and leaves malformed entries out for the validator to
    report rather than inventing a path.
    """

    raw = value if isinstance(value, list) else []
    fallback = [
        str(path).strip()
        for path in (fallback_paths or [])
        if isinstance(path, str) and str(path).strip()
    ]
    # A common Agent/schema drift is to put scientific result labels (for
    # example ``HOMO_energy``) in this file-path field.  When every item is a
    # bare label and the submission contract declares real artifact paths, the
    # contract paths are authoritative.  Keep the scientific labels in the
    # task's result schema/report rather than pretending them to be files.
    raw_strings = [item.strip() for item in raw if isinstance(item, str) and item.strip()]
    if (
        fallback
        and raw_strings
        and len(raw_strings) == len(raw)
        and not any("/" in item or "." in item for item in raw_strings)
        and any(path not in raw_strings for path in fallback)
    ):
        raw = fallback
    normalized: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, str):
            path = item.strip()
            if not path:
                continue
            normalized.append(
                {
                    "path": path,
                    "description": "Required task artifact.",
                    "allow_empty": False,
                }
            )
            continue
        if not isinstance(item, dict):
            continue
        path = item.get("path") or item.get("file")
        if not isinstance(path, str) or not path.strip():
            continue
        row = dict(item)
        row["path"] = path.strip()
        row.setdefault("description", "Required task artifact.")
        row.setdefault("allow_empty", False)
        normalized.append(row)
    return normalized


def normalize_task_data_files(value: Any) -> list[dict[str, Any]]:
    """Fill evaluator-required display names without changing data semantics.

    ``TaskInfo.data`` is transport metadata for public assets.  Agents sometimes
    provide only ``path`` and ``description`` even though the evaluator's
    ``DataFile`` schema requires ``name``.  The basename of the declared path is
    a deterministic presentation label; deriving it here neither adds an input
    nor interprets scientific content.
    """

    if not isinstance(value, list):
        return []
    normalized: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        row = dict(item)
        path = str(row.get("path") or "").strip()
        name = str(row.get("name") or "").strip()
        if not name and path:
            name = Path(path).name or path
        if name:
            row["name"] = name
        normalized.append(row)
    return normalized


def canonicalize_mode_task_contract(
    task_root: Path,
    *,
    expected_mode: str,
    task_pair_id: str | None = None,
) -> list[str]:
    """Apply the non-scientific mode/ID contract to an Agent-delivered task tree.

    This is deliberately a transport normalization, not a scientific validator.  It repairs
    fields that the Evaluator treats as enums and keeps the public task ID stable across Agent
    rewrites.  Any missing files or malformed JSON are returned as mechanical findings.
    """

    expected_mode = str(expected_mode)
    if expected_mode not in {"autonomous_research", "paper_reproduction"}:
        return [f"unsupported_mode:{expected_mode}"]
    expected_task_mode = (
        "open_discovery" if expected_mode == "autonomous_research" else "guided_reproduction"
    )
    suffix = "_autonomous" if expected_mode == "autonomous_research" else "_reproduction"
    # task_info is a deliberately compact projection and may omit both
    # workflow_scope and method_constraints.  Read the sibling task_spec once
    # so both files receive the same derived disclosure metadata.
    peer_scope: dict[str, Any] = {}
    peer_method_constraints: Any = None
    peer_spec_path = task_root / "task_spec.json"
    if expected_mode == "autonomous_research" and peer_spec_path.is_file():
        try:
            peer_spec = read_json(peer_spec_path)
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            peer_spec = {}
        if isinstance(peer_spec, dict):
            candidate_scope = peer_spec.get("workflow_scope")
            if isinstance(candidate_scope, dict):
                peer_scope = candidate_scope
            peer_method_constraints = peer_spec.get("method_constraints") or peer_spec.get(
                "public_method_constraints"
            )
    findings: list[str] = []
    for name in ("task_info.json", "task_spec.json"):
        path = task_root / name
        if not path.is_file():
            findings.append(f"missing_public_file:{name}")
            continue
        try:
            value = read_json(path)
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            findings.append(f"unreadable_public_file:{name}:{type(exc).__name__}")
            continue
        if not isinstance(value, dict):
            findings.append(f"public_file_not_object:{name}")
            continue
        pair_id = str(task_pair_id or value.get("task_pair_id") or "").strip()
        if not pair_id:
            findings.append(f"task_pair_id_missing:{name}")
            continue
        canonical_id = f"{pair_id}{suffix}"
        # Evaluator metadata needs a stable provenance key, but the public task
        # must not expose a DOI/title.  Derive the same anonymous key for both
        # modes from the pair identity and keep full provenance in paper_info.
        value["source_id"] = anonymous_source_id(pair_id)
        value["task_pair_id"] = pair_id
        value["task_id"] = canonical_id
        value["mode"] = expected_mode
        value["scientific_mode"] = expected_mode
        value["task_mode"] = expected_task_mode
        if expected_mode == "autonomous_research":
            scope = value.get("workflow_scope")
            if not isinstance(scope, dict):
                scope = peer_scope
            scope_value = (
                scope.get("autonomy_scope")
                if isinstance(scope, dict)
                else None
            )
            # ``task_info.json`` is intentionally a compact projection and
            # therefore often does not carry the full workflow_scope object.
            # A non-empty method_constraints list is the authoritative public
            # signal that the autonomous task is method-constrained.  Do not
            # silently relabel such a task as method discovery merely because
            # the scope projection is absent.
            public_method_constraints = (
                value.get("method_constraints")
                or value.get("public_method_constraints")
                or peer_method_constraints
            )
            has_public_method_constraints = isinstance(
                public_method_constraints, list
            ) and any(str(item).strip() for item in public_method_constraints)
            value["method_disclosure"] = (
                "public_scientific_method_constraints"
                if (
                    scope_value == "fixed_input_method_constrained_workflow"
                    or has_public_method_constraints
                )
                else "no_paper_method"
            )
            value["pathway_disclosure"] = "public_problem_only"
        elif expected_mode == "paper_reproduction":
            value["method_disclosure"] = "paper_route_disclosed"
            value["pathway_disclosure"] = "paper_route_disclosed"
        if isinstance(value.get("complexity_profile"), dict):
            value["complexity_profile"] = canonicalize_complexity_profile(
                value["complexity_profile"]
            )
        if name == "task_info.json" and "scientific_requirements" in value:
            value["scientific_requirements"] = normalize_scientific_requirements(
                value.get("scientific_requirements")
            )
        if name == "task_info.json":
            if "data" in value:
                value["data"] = normalize_task_data_files(value.get("data"))
            raw_deliverables = value.get("required_deliverables")
            if not isinstance(raw_deliverables, list) or not raw_deliverables:
                raw_deliverables = value.get("deliverables")
            if isinstance(raw_deliverables, list):
                submission_paths: list[str] = []
                submission_path = task_root / "submission_contract.json"
                if submission_path.is_file():
                    try:
                        submission_value = read_json(submission_path)
                    except (OSError, TypeError, ValueError, json.JSONDecodeError):
                        submission_value = {}
                    if isinstance(submission_value, dict):
                        submission_paths = [
                            str(path)
                            for path in submission_value.get("required_files") or []
                            if isinstance(path, str)
                        ]
                value["required_deliverables"] = normalize_required_deliverables(
                    raw_deliverables, fallback_paths=submission_paths
                )
                value.pop("deliverables", None)
        write_json(path, value)
    return sorted(set(findings))


def anonymous_source_id(task_pair_id: str) -> str:
    """Return a stable public provenance key without publishing paper identity."""

    digest = hashlib.sha256(str(task_pair_id).encode("utf-8")).hexdigest()[:20]
    return f"rcb-source-{digest}"


def canonical_task_pair_id(paper_id: str) -> str:
    """Return the deterministic pair identity used by newly built task pairs."""

    value = re.sub(r"[^A-Za-z0-9._-]+", "_", str(paper_id).strip()).strip("._-")
    if not value:
        value = "paper"
    return f"{value}_task_pair"


def normalize_submission_contract(value: Any) -> dict[str, Any]:
    """Normalize transport fields shared by both modes.

    The result schema is intentionally permissive: it declares that the
    evaluator expects a JSON object while leaving scientific result keys to the
    task's acceptance profiles.  This closes the evaluator contract without
    inventing a paper-specific output schema.
    """

    output = dict(value) if isinstance(value, dict) else {}
    # Agents and older drafts used several names for the same transport-level
    # deliverable list.  Normalize those aliases without interpreting the
    # scientific meaning of any result field.
    raw_paths = output.get("required_files")
    if not isinstance(raw_paths, list) or not raw_paths:
        raw_paths = []
        for key in ("required_file", "submission_file", "primary_file"):
            candidate = output.get(key)
            if isinstance(candidate, str):
                raw_paths.append(candidate)
            elif isinstance(candidate, list):
                raw_paths.extend(candidate)
        for key in ("required_artifacts", "artifact_paths"):
            candidate = output.get(key)
            if isinstance(candidate, dict):
                candidate = list(candidate.values())
            if isinstance(candidate, (list, tuple)):
                for item in candidate:
                    if isinstance(item, dict):
                        raw_paths.append(item.get("path") or item.get("file"))
                    else:
                        raw_paths.append(item)
    normalized_paths: list[str] = []
    for raw_path in raw_paths:
        if isinstance(raw_path, dict):
            raw_path = raw_path.get("path") or raw_path.get("file")
        if not isinstance(raw_path, str):
            continue
        path = raw_path.strip().replace("\\", "/")
        if path and path not in normalized_paths:
            normalized_paths.append(path)
    if normalized_paths:
        output["required_files"] = normalized_paths
    output.setdefault("schema_version", "researchchembench.submission.v1")
    output.setdefault("results_schema", json.loads(json.dumps(DEFAULT_RESULT_SCHEMA)))
    return output


def normalize_process_rubric_contract(value: Any) -> Any:
    """Project harmless rubric container wrappers to the evaluator list shape.

    This helper does not invent criteria or change scores. It only removes a
    serialization wrapper used by older Agent drafts around the same criteria.
    """

    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("criteria", "items", "rubric"):
            rows = value.get(key)
            if isinstance(rows, list):
                return rows
    return value


def validate_scientific_review(review: dict[str, Any], evidence_ids: set[str]) -> list[str]:
    findings: list[str] = []
    if _contains_review_placeholder(review):
        findings.append("scientific_review_contains_placeholder")
    if review.get("decision") == "scientific_reject":
        if not review.get("reject_reasons"):
            findings.append("scientific_reject_missing_reasons")
        return findings
    if review.get("decision") != "candidate_ready":
        return ["invalid_review_decision"]
    for field in (
        "task_pair_id",
        "selected_candidate_id",
        "scientific_question",
        "public_scientific_question",
        "task_direction",
        "category",
        "workflow_summary",
    ):
        if not str(review.get(field) or "").strip():
            findings.append(f"missing_{field}")
    steps = review.get("workflow_steps") or []
    step_ids = {
        str(step.get("step_id") or "") for step in steps if isinstance(step, dict)
    }
    if not steps or "" in step_ids:
        findings.append("workflow_steps_incomplete")
    for step in steps:
        if not isinstance(step, dict):
            findings.append("workflow_step_invalid")
            continue
        for dependency in step.get("depends_on") or []:
            if dependency not in step_ids:
                findings.append(f"unknown_workflow_dependency:{dependency}")
        if not step.get("output_artifacts"):
            findings.append(f"workflow_step_missing_output:{step.get('step_id')}")
        findings.extend(_unknown_evidence(step.get("evidence_ids"), evidence_ids, "workflow"))
    public_basis = review.get("public_task_basis") or {}
    completeness = public_basis.get("input_completeness") or {}
    if completeness.get("status") != "confirmed":
        findings.append("public_input_completeness_not_confirmed")
    if completeness.get("unresolved_fields"):
        findings.append("public_input_fields_unresolved")
    if not completeness.get("closed_fields"):
        findings.append("public_input_closed_fields_missing")
    boundary_conditions = public_basis.get("boundary_conditions")
    findings.extend(
        _public_boundary_contract_findings(boundary_conditions, evidence_ids=evidence_ids)
    )
    findings.extend(
        _route_boundary_coverage_findings(
            review,
            boundary_conditions=boundary_conditions,
        )
    )
    assets = public_basis.get("input_assets") or []
    if not assets:
        findings.append("public_input_assets_missing")
    for asset in assets:
        if not isinstance(asset, dict):
            findings.append("public_input_asset_invalid")
            continue
        try:
            public_path = validate_relative_path(str(asset.get("path") or ""))
        except ValueError:
            findings.append("public_input_asset_path_invalid")
            public_path = ""
        if public_path.startswith(("outputs/", "private_input/", "hidden_reference/")):
            findings.append(f"public_input_asset_path_not_logical:{public_path}")
        if asset.get("content") is None:
            findings.append(f"public_input_asset_content_missing:{asset.get('path')}")
        provenance = asset.get("provenance") or {}
        if provenance.get("kind") not in {"source_copy", "deterministic_transform"}:
            findings.append(f"public_input_asset_provenance_invalid:{asset.get('path')}")
        if not str(provenance.get("derivation") or "").strip():
            findings.append(f"public_input_asset_derivation_missing:{asset.get('path')}")
        if provenance.get("introduced_values") not in ([], None):
            findings.append(f"public_input_asset_introduces_values:{asset.get('path')}")
        findings.extend(
            _unknown_evidence(asset.get("source_evidence_ids"), evidence_ids, "public_asset")
        )
    paper_route = review.get("paper_route") or {}
    route_completeness = paper_route.get("route_completeness") or {}
    if route_completeness.get("status") != "confirmed":
        findings.append("paper_route_completeness_not_confirmed")
    if route_completeness.get("unresolved_fields"):
        findings.append("paper_route_fields_unresolved")
    if not route_completeness.get("closed_fields"):
        findings.append("paper_route_closed_fields_missing")
    disclosures = paper_route.get("autonomous_forbidden_disclosures") or []
    if not isinstance(disclosures, list) or not disclosures:
        findings.append("paper_route_forbidden_disclosures_missing")
    truths = review.get("ground_truth_items") or []
    if not truths:
        findings.append("ground_truth_items_missing")
    for truth in truths:
        if not isinstance(truth, dict):
            findings.append("ground_truth_item_invalid")
            continue
        if truth.get("acceptance_type") not in ACCEPTANCE_TYPES:
            findings.append(f"invalid_acceptance_type:{truth.get('ground_truth_id')}")
        if truth.get("evidence_grade") not in {"A", "B", "C", "D"}:
            findings.append(f"invalid_evidence_grade:{truth.get('ground_truth_id')}")
        if truth.get("claim_role") not in {"intermediate", "final"}:
            findings.append(f"invalid_claim_role:{truth.get('ground_truth_id')}")
        if truth.get("canonical_answer") in (None, "", [], {}) and not truth.get(
            "required_propositions"
        ):
            findings.append(f"ground_truth_answer_missing:{truth.get('ground_truth_id')}")
        findings.extend(_unknown_evidence(truth.get("evidence_ids"), evidence_ids, "ground_truth"))
    findings.extend(validate_ground_truth_consistency(truths))
    findings.extend(_review_disclosure_findings(review))
    evidence_map = review.get("evidence_map") or []
    if not evidence_map:
        findings.append("evidence_map_missing")
    findings.extend(
        _unknown_evidence(
            _evidence_map_ids(evidence_map, known_evidence_ids=evidence_ids),
            evidence_ids,
            "evidence_map",
        )
    )
    for requirement in review.get("toolbox_requirements") or []:
        if not isinstance(requirement, dict):
            findings.append("toolbox_requirement_invalid")
            continue
        status = requirement.get("status")
        if status not in {"available", "missing", "incompatible", "unknown"}:
            findings.append("toolbox_requirement_status_invalid")
        if not str(
            requirement.get("software")
            or requirement.get("tool")
            or requirement.get("normalized_backend")
            or ""
        ).strip():
            findings.append("toolbox_requirement_software_missing")
    return sorted(set(findings))


def validate_workflow_review(
    review: dict[str, Any], evidence_ids: set[str]
) -> list[str]:
    """Validate full-paper-first selection and either success or scientific failure."""

    findings: list[str] = []
    decision = review.get("decision")
    for field in (
        "paper_workflow_inventory_complete",
        "full_paper_workflow_checked",
        "alternative_scope_search_complete",
    ):
        if review.get(field) is not True:
            findings.append(f"workflow_review_{field}_false")
    if not isinstance(review.get("workflow_inventory"), list):
        findings.append("workflow_inventory_invalid")
    evidence_map = review.get("evidence_map") or []
    findings.extend(
        _unknown_evidence(
            _evidence_map_ids(evidence_map, known_evidence_ids=evidence_ids),
            evidence_ids,
            "workflow_review",
        )
    )
    # New reviews should carry the comparison, but legacy scientific-reject receipts may
    # predate this advisory field.  Validate it when present without turning a missing
    # explanatory record into a code-side scientific verdict.
    if review.get("representativeness_review") is not None:
        findings.extend(
            validate_representativeness_review(
                review.get("representativeness_review"), evidence_ids
            )
        )
    if decision == "scientific_not_constructible":
        failure_code = str(review.get("failure_code") or "")
        if failure_code not in SCIENTIFIC_FAILURE_CODES:
            findings.append(f"scientific_failure_code_invalid:{failure_code or 'missing'}")
        reasons = review.get("failure_reasons") or []
        if not reasons:
            findings.append("scientific_failure_reasons_missing")
        for index, reason in enumerate(reasons):
            if not isinstance(reason, dict):
                findings.append(f"scientific_failure_reason_invalid:{index}")
                continue
            if not str(reason.get("scope_attempted") or "").strip():
                findings.append(f"scientific_failure_scope_missing:{index}")
            reason_code = str(reason.get("code") or "")
            if reason_code not in SCIENTIFIC_FAILURE_CODES:
                findings.append(f"scientific_failure_reason_code_invalid:{index}:{reason_code}")
            if not str(reason.get("details") or "").strip():
                findings.append(f"scientific_failure_details_missing:{index}")
            if not reason.get("checked_sources"):
                findings.append(f"scientific_failure_checked_sources_missing:{index}")
            findings.extend(
                _unknown_evidence(
                    reason.get("evidence_ids"), evidence_ids, f"scientific_failure:{index}"
                )
            )
        return sorted(set(findings))
    if decision != "candidate_ready":
        findings.append("workflow_review_decision_invalid")
        return sorted(set(findings))
    compatibility_review = dict(review)
    compatibility_review["decision"] = "candidate_ready"
    compatibility_review["reject_reasons"] = []
    findings.extend(validate_scientific_review(compatibility_review, evidence_ids))
    findings.extend(validate_workflow_scope(review.get("workflow_scope") or {}, evidence_ids))
    findings.extend(
        validate_complexity_profile(
            review.get("complexity_profile") or {},
            workflow_steps=review.get("workflow_steps") or [],
        )
    )
    if review.get("failure_code") or review.get("failure_reasons"):
        findings.append("ready_workflow_contains_failure_contract")
    return sorted(set(findings))


def validate_representativeness_review(
    value: Any, evidence_ids: set[str]
) -> list[str]:
    """Validate the shape/provenance of the Agent's scope comparison only.

    This deliberately does not score scientific centrality or inspect paper-specific
    terminology.  The comparison is evidence supplied to Stage07, while the scientific
    judgment remains with the Agents.
    """

    if not isinstance(value, dict):
        return ["representativeness_review_missing"]
    findings: list[str] = []
    claims = value.get("paper_computational_claims")
    candidates = value.get("candidate_workflows")
    if not isinstance(claims, list) or not claims:
        findings.append("representativeness_claims_missing")
    if not isinstance(candidates, list) or not candidates:
        findings.append("representativeness_candidates_missing")
    if not str(value.get("selected_workflow_id") or "").strip():
        findings.append("representativeness_selected_workflow_missing")
    if not str(value.get("selection_rationale") or "").strip():
        findings.append("representativeness_selection_rationale_missing")
    if "omitted_claims" not in value:
        findings.append("representativeness_omitted_claims_missing")
    for index, candidate in enumerate(candidates if isinstance(candidates, list) else []):
        if not isinstance(candidate, dict):
            findings.append(f"representativeness_candidate_invalid:{index}")
            continue
        if not str(candidate.get("workflow_id") or "").strip():
            findings.append(f"representativeness_candidate_id_missing:{index}")
        if not str(candidate.get("scope_kind") or "").strip():
            findings.append(f"representativeness_candidate_scope_missing:{index}")
        if "claim_coverage" not in candidate:
            findings.append(f"representativeness_candidate_coverage_missing:{index}")
        # These are evidence-record fields, not a code-side centrality score.  Requiring
        # their presence keeps the Stage07 audit from receiving a bare list of easy-to-
        # package workflows with no closure, resource, or toolbox context.  Values remain
        # free-form because the scientific interpretation belongs to the Agents.
        if "closure" not in candidate:
            findings.append(f"representativeness_candidate_closure_missing:{index}")
        if not any(
            key in candidate
            for key in ("cost", "resource_assessment", "estimated_cost")
        ):
            findings.append(f"representativeness_candidate_resource_observation_missing:{index}")
        if not any(
            key in candidate
            for key in ("software_gap_status", "toolbox_status", "software_status")
        ):
            findings.append(f"representativeness_candidate_software_status_missing:{index}")
    for index, claim in enumerate(claims if isinstance(claims, list) else []):
        if not isinstance(claim, dict):
            findings.append(f"representativeness_claim_invalid:{index}")
            continue
        if not str(claim.get("claim_id") or "").strip():
            findings.append(f"representativeness_claim_id_missing:{index}")
        if "coverage" not in claim:
            findings.append(f"representativeness_claim_coverage_missing:{index}")
    findings.extend(
        _unknown_evidence(
            _evidence_map_ids(value, known_evidence_ids=evidence_ids),
            evidence_ids,
            "representativeness_review",
        )
    )
    return sorted(set(findings))


def validate_workflow_scope(scope: Any, evidence_ids: set[str]) -> list[str]:
    if not isinstance(scope, dict):
        return ["workflow_scope_invalid"]
    findings: list[str] = []
    kind = str(scope.get("kind") or "")
    if kind not in WORKFLOW_SCOPE_KINDS:
        findings.append(f"workflow_scope_kind_invalid:{kind or 'missing'}")
    if not scope.get("included_workflow_ids"):
        findings.append("workflow_scope_included_workflows_missing")
    if not scope.get("included_claim_ids"):
        findings.append("workflow_scope_included_claims_missing")
    if not str(scope.get("selection_rationale") or "").strip():
        findings.append("workflow_scope_selection_rationale_missing")
    if kind not in {"full_paper_core_workflow", "full_paper_computational_workflow"} and not scope.get(
        "larger_scope_failure_reasons"
    ):
        findings.append("workflow_scope_larger_scope_reason_missing")
    if kind == "core_scientific_subworkflow":
        for field in (
            "central_scientific_question",
            "supported_primary_claims",
            "parent_workflow_position",
            "why_not_full_workflow",
        ):
            if scope.get(field) in (None, "", [], {}):
                findings.append(f"core_subworkflow_{field}_missing")
    findings.extend(
        _unknown_evidence(scope.get("scope_evidence_ids"), evidence_ids, "workflow_scope")
    )
    return sorted(set(findings))


def classify_task_pair_findings(findings: Any) -> dict[str, list[str]]:
    """Classify findings without turning the orchestrator into a scientific judge."""

    categories: dict[str, list[str]] = {
        "hard_mechanical": [],
        "disclosure_semantic": [],
        "agent_scientific": [],
        "resource_advisory": [],
    }
    disclosure_prefixes = (
        "hidden_answer_leakage",
        "hidden_conclusion_leakage",
        "autonomous_route_disclosure",
        "review_public_route_disclosure",
        "review_public_answer_leakage",
        "review_public_conclusion_leakage",
        "review_paper_route_answer_leakage",
        "review_paper_route_conclusion_leakage",
        "review_reproduction_route_uses_hidden_result",
    )
    scientific_prefixes = (
        "task_not_challenging",
        "scope_underselected",
        "resource_infeasible",
        "benchmark_not_challenging",
    )
    resource_prefixes = ("toolbox_", "software_", "resource_", "cost_")
    for raw in findings if isinstance(findings, list) else []:
        finding = str(raw)
        code = finding.split(":", 1)[0]
        if code.startswith(disclosure_prefixes):
            categories["disclosure_semantic"].append(finding)
        elif code.startswith(scientific_prefixes):
            categories["agent_scientific"].append(finding)
        elif code.startswith(resource_prefixes):
            categories["resource_advisory"].append(finding)
        else:
            categories["hard_mechanical"].append(finding)
    return {key: sorted(set(value)) for key, value in categories.items()}


def task_pair_contract_report(pair_root: Path) -> dict[str, Any]:
    """Return the versioned prepublish report shared by Stage06 and Stage07."""

    audit = validate_task_pair(pair_root)
    categories = classify_task_pair_findings(audit.get("findings") or [])
    evaluator_findings = [
        finding
        for finding in categories["hard_mechanical"]
        if finding.startswith(("evaluation_task_info_invalid", "evaluation_ground_truth_invalid"))
    ]
    return {
        "schema_version": TASK_PAIR_CONTRACT_VERSION,
        "pair_root_name": pair_root.name,
        "contract_status": "passed" if not categories["hard_mechanical"] else "findings",
        "disclosure_status": "passed" if not categories["disclosure_semantic"] else "needs_review",
        "schema_load_diagnostic": "failed" if evaluator_findings else "passed",
        "finding_counts": {key: len(value) for key, value in categories.items()},
        "findings": categories,
        "validator": audit,
    }


def validate_complexity_profile(
    profile: Any, *, workflow_steps: Any
) -> list[str]:
    del workflow_steps
    if not isinstance(profile, dict):
        return ["complexity_profile_invalid"]
    findings: list[str] = []
    level = str(profile.get("level") or "")
    if level not in {"medium", "high"}:
        findings.append(
            "task_not_challenging"
            if level == "low_complexity_trivial"
            else f"complexity_level_invalid:{level or 'missing'}"
        )
    if not str(profile.get("rationale") or "").strip():
        findings.append("complexity_rationale_missing")
    calls = profile.get("estimated_tool_calls")
    if calls is not None:
        if not isinstance(calls, dict):
            findings.append("complexity_tool_call_estimate_invalid")
        else:
            minimum = calls.get("min")
            typical = calls.get("typical")
            if not all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in (minimum, typical)):
                findings.append("complexity_tool_call_estimate_invalid")
            elif typical < minimum:
                findings.append("complexity_tool_call_estimates_inverted")
    return sorted(set(findings))


def _contains_review_placeholder(value: Any) -> bool:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True).casefold()
    placeholder_values = (
        '"key": "value"',
        '"reject reasons"',
        '"scientific question"',
        '"public scientific question"',
        '"task pair id"',
        '"task direction"',
        '"workflow summary"',
        '"stage05 candidate disposition"',
    )
    return any(token in serialized for token in placeholder_values)


def _evidence_map_ids(
    value: Any, *, known_evidence_ids: set[str] | None = None
) -> list[str]:
    """Collect evidence references recursively without assuming an ID prefix."""

    known = known_evidence_ids or set()
    output: list[str] = []

    def add(candidate: Any) -> None:
        if candidate in (None, ""):
            return
        identifier = str(candidate)
        if identifier not in output:
            output.append(identifier)

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            add(node.get("evidence_id"))
            evidence_ids = node.get("evidence_ids")
            if isinstance(evidence_ids, (list, tuple, set)):
                for identifier in evidence_ids:
                    add(identifier)
            elif evidence_ids not in (None, ""):
                add(evidence_ids)
            for key, nested in node.items():
                if str(key) in known:
                    add(key)
                if key not in {"evidence_id", "evidence_ids"}:
                    visit(nested)
            return
        if isinstance(node, (list, tuple, set)):
            for nested in node:
                if isinstance(nested, str) and nested in known:
                    add(nested)
                else:
                    visit(nested)

    visit(value)
    return output


def _public_boundary_contract_findings(
    value: Any, *, evidence_ids: set[str]
) -> list[str]:
    if not isinstance(value, list) or not value:
        return ["public_boundary_conditions_missing"]
    findings: list[str] = []
    for index, row in enumerate(value):
        if not isinstance(row, dict):
            findings.append(f"public_boundary_condition_invalid:{index}")
            continue
        name = str(row.get("name") or row.get("condition") or row.get("type") or "").strip()
        if not name:
            findings.append(f"public_boundary_condition_name_missing:{index}")
        if row.get("value") in (None, "", [], {}):
            findings.append(f"public_boundary_condition_value_missing:{index}")
        findings.extend(
            _unknown_evidence(
                row.get("evidence_ids"),
                evidence_ids,
                f"public_boundary_condition:{index}",
            )
        )
    return findings


def _route_boundary_coverage_findings(
    review: dict[str, Any], *, boundary_conditions: Any
) -> list[str]:
    public_conditions = [
        row for row in boundary_conditions or [] if isinstance(row, dict)
    ]
    periodic_target = any(
        _boundary_kind(str(row.get("name") or row.get("condition") or row.get("type") or ""))
        == "periodic"
        and _periodic_boundary_enabled(row.get("value"))
        for row in public_conditions
    )
    findings: list[str] = []
    for name, value in _route_boundary_parameters(review):
        kind = _boundary_kind(name)
        if kind is None or (kind == "multiplicity" and periodic_target):
            continue
        aliases = {_normalize_text(alias) for alias in _boundary_value_aliases(name, value)}
        aliases.discard("")
        if not aliases:
            continue
        matching_conditions = [
            row
            for row in public_conditions
            if _boundary_kind(
                str(row.get("name") or row.get("condition") or row.get("type") or "")
            )
            == kind
        ]
        disclosed = any(
            _boundary_values_equivalent(
                name,
                value,
                str(
                    row.get("name")
                    or row.get("condition")
                    or row.get("type")
                    or kind
                ),
                row.get("value"),
            )
            for row in matching_conditions
        )
        if not disclosed:
            findings.append(
                f"public_boundary_not_disclosed:{name}:{sorted(aliases)[0]}"
            )
    return sorted(set(findings))


def _boundary_kind(name: str) -> str | None:
    normalized = name.casefold().replace("-", "_").replace(" ", "_")
    aliases = (
        (("solvent", "solvation", "medium", "environment"), "medium"),
        (("temperature",), "temperature"),
        (("pressure",), "pressure"),
        (("multiplicity",), "multiplicity"),
        (("protonation",), "protonation"),
        (("periodic", "boundary"), "periodic"),
        (("ensemble",), "ensemble"),
        (("electric_field",), "electric_field"),
        (("charge",), "charge"),
    )
    matched = next(
        (kind for markers, kind in aliases if any(marker in normalized for marker in markers)),
        None,
    )
    if matched is not None:
        return matched
    return "ph" if re.search(r"(?:^|_)ph(?:_|$)", normalized) else None


def _periodic_boundary_enabled(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = _normalize_text(str(value or ""))
    return bool(
        normalized
        and "periodic" in normalized
        and not re.search(r"\b(?:non periodic|nonperiodic|finite|isolated)\b", normalized)
    )


def _boundary_values_equivalent(
    left_name: str, left_value: Any, right_name: str, right_value: Any
) -> bool:
    left_aliases = {
        _normalize_text(alias)
        for alias in _boundary_value_aliases(left_name, left_value)
        if _normalize_text(alias)
    }
    right_aliases = {
        _normalize_text(alias)
        for alias in _boundary_value_aliases(right_name, right_value)
        if _normalize_text(alias)
    }
    if left_aliases & right_aliases:
        return True
    left_number = _first_numeric_value(left_value)
    right_number = _first_numeric_value(right_value)
    return (
        left_number is not None
        and right_number is not None
        and math.isclose(left_number, right_number, rel_tol=1e-9, abs_tol=1e-9)
    )


def _first_numeric_value(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"(?<![A-Za-z0-9.])[+-]?\d+(?:\.\d+)?", str(value or ""))
    return float(match.group(0)) if match else None


def _route_boundary_parameters(review: dict[str, Any]) -> list[tuple[str, Any]]:
    markers = (
        "solvent",
        "solvation",
        "medium",
        "temperature",
        "pressure",
        "ph",
        "charge",
        "multiplicity",
        "protonation",
        "periodic",
        "boundary",
        "ensemble",
        "electric_field",
    )
    values: list[tuple[str, Any]] = []

    def visit(value: Any, key: str = "") -> None:
        if isinstance(value, dict):
            for nested_key, nested in value.items():
                visit(nested, str(nested_key))
            return
        if isinstance(value, list):
            for nested in value:
                visit(nested, key)
            return
        normalized_key = key.casefold().replace("-", "_")
        if any(marker in normalized_key for marker in markers) and value not in (None, ""):
            values.append((normalized_key, value))

    for step in review.get("workflow_steps") or []:
        if isinstance(step, dict):
            visit(step.get("method_parameters") or {})
    paper_route = review.get("paper_route") or {}
    for key in ("route_steps", "workflow_steps", "steps"):
        for step in paper_route.get(key) or []:
            if isinstance(step, dict):
                visit(step.get("method_parameters") or {})
    return values


def _boundary_value_aliases(name: str, value: Any) -> list[str]:
    if isinstance(value, bool):
        return []
    raw = str(value).strip()
    if not raw:
        return []
    normalized_name = name.casefold()
    normalized_raw = _normalize_text(raw)
    if "charge" in normalized_name and (
        raw in {"0", "+0", "0.0"} or "neutral" in normalized_raw
    ):
        return ["neutral", "charge 0"]
    if "multiplicity" in normalized_name and (
        raw in {"1", "1.0"} or "singlet" in normalized_raw
    ):
        return ["singlet", "multiplicity 1"]
    if any(marker in normalized_name for marker in ("solvent", "solvation", "medium")):
        candidate = (
            re.split(r"[=:]", raw)[-1]
            if re.search(r"[=:]", raw)
            else re.split(r"[,;(]", raw, maxsplit=1)[0]
        )
        candidate = re.sub(
            r"\b(?:pcm|cpcm|smd|cosmo|implicit|explicit|solvent|solvation|target|chemical|medium|environment)\b",
            " ",
            candidate,
            flags=re.IGNORECASE,
        )
        candidate = _normalize_text(candidate)
        return [candidate] if len(candidate) >= 3 else []
    if "periodic" in normalized_name:
        if re.search(r"\b(?:non periodic|finite|isolated)\b", normalized_raw):
            return ["non-periodic", "finite"]
        if "periodic" in normalized_raw:
            return ["periodic"]
    return [normalized_raw] if len(normalized_raw) >= 3 else []


def _allowed_public_boundary_aliases(boundary_conditions: Any) -> set[str]:
    aliases: set[str] = set()
    for index, row in enumerate(boundary_conditions or []):
        if not isinstance(row, dict):
            continue
        name = str(row.get("name") or row.get("condition") or row.get("type") or index)
        aliases.update(
            _normalize_text(alias)
            for alias in _boundary_value_aliases(name, row.get("value"))
            if _normalize_text(alias)
        )
    return aliases


def _public_method_constraint_text(method_constraints: Any) -> str:
    """Return normalized text for method constraints explicitly exposed as science inputs.

    A constrained autonomous task may intentionally disclose a functional, basis, or other
    method variable.  Those tokens are public by contract and must not be treated as leaked
    author-route implementation merely because the same token occurs in the reproduction route.
    """

    values: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for nested in value.values():
                visit(nested)
        elif isinstance(value, list):
            for nested in value:
                visit(nested)
        elif isinstance(value, str) and value.strip():
            values.append(value)

    visit(method_constraints)
    return _normalize_text("\n".join(values))


def validate_task_boundary_conditions(
    task_root: Path, *, expected_conditions: Any
) -> list[str]:
    if not isinstance(expected_conditions, list) or not expected_conditions:
        return ["task_expected_boundary_conditions_missing"]
    try:
        spec = read_json(task_root / "task_spec.json")
        task_text = (task_root / "task.md").read_text(
            encoding="utf-8", errors="replace"
        )
    except (OSError, json.JSONDecodeError) as exc:
        return [f"task_boundary_artifact_unreadable:{type(exc).__name__}"]
    findings: list[str] = []
    if spec.get("boundary_conditions") != expected_conditions:
        findings.append("task_boundary_conditions_not_frozen_from_public_basis")
    normalized_task = _normalize_text(task_text)
    for index, row in enumerate(expected_conditions):
        if not isinstance(row, dict):
            continue
        name = str(row.get("name") or row.get("condition") or row.get("type") or index)
        aliases = _boundary_value_aliases(name, row.get("value"))
        if aliases and not any(_route_token_present(alias, normalized_task) for alias in aliases):
            findings.append(f"task_instruction_boundary_missing:{name}:{aliases[0]}")
        if any(marker in name.casefold() for marker in ("solvent", "medium", "environment")):
            value_text = _normalize_text(str(row.get("value") or ""))
            if value_text not in {"", "gas", "gas phase", "vacuum", "none"} and (
                _declares_conflicting_medium(normalized_task)
            ):
                findings.append(f"task_instruction_boundary_conflict:{name}")
    return sorted(set(findings))


def _declares_conflicting_medium(normalized_task: str) -> bool:
    patterns = (
        r"\b(?:use|using|assume|assuming|model|modeling|run|running|treat|treating|set)\b.{0,32}\b(?:gas phase|vacuum|no solvent)\b",
        r"\b(?:solvent|medium|environment)\s*(?:is|as|to|=|:)\s*(?:gas|gas phase|vacuum|none)\b",
        r"\bin (?:the )?(?:gas phase|vacuum)\b",
    )
    return any(re.search(pattern, normalized_task) for pattern in patterns)


def validate_autonomous_route_isolation(
    task_root: Path,
    *,
    paper_route: dict[str, Any],
    allowed_boundary_conditions: Any,
    allowed_method_constraints: Any = None,
) -> list[str]:
    public_text = _normalize_text(
        "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in task_root.rglob("*")
            if path.is_file()
            and path.suffix.casefold() in {".md", ".json", ".txt", ".csv", ".tsv"}
        )
    )
    allowed_boundary_aliases = _allowed_public_boundary_aliases(
        allowed_boundary_conditions
    )
    allowed_method_text = _public_method_constraint_text(allowed_method_constraints)
    declared_tokens = paper_route.get("autonomous_forbidden_disclosures") or []
    route_tokens = {
        _normalize_text(str(token))
        for token in [*declared_tokens, *_structured_route_tokens(paper_route)]
        if _normalize_text(str(token))
    }
    findings = []
    for token in sorted(route_tokens):
        if token in allowed_boundary_aliases or (
            allowed_method_text and _route_token_present(token, allowed_method_text)
        ):
            continue
        if _route_token_present(token, public_text):
            findings.append(f"autonomous_route_disclosure:{token}")
    return findings


def validate_mode_task(task_root: Path, *, expected_mode: str) -> list[str]:
    findings: list[str] = []
    required = [
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    ]
    for name in required:
        if not (task_root / name).is_file():
            findings.append(f"missing_public_file:{name}")
    if findings:
        return findings
    task_info = read_json(task_root / "task_info.json")
    task_spec = read_json(task_root / "task_spec.json")
    submission_contract = read_json(task_root / "submission_contract.json")
    findings.extend(_evaluation_task_info_findings(task_info))
    expected_task_mode = (
        "open_discovery" if expected_mode == "autonomous_research" else "guided_reproduction"
    )
    if task_info.get("task_mode") != expected_task_mode:
        findings.append("task_mode_mismatch")
    if task_info.get("mode") != expected_mode:
        findings.append("task_info_mode_mismatch")
    if task_info.get("scientific_mode") != expected_mode:
        findings.append("task_info_scientific_mode_mismatch")
    suffix = "_autonomous" if expected_mode == "autonomous_research" else "_reproduction"
    task_id = str(task_info.get("task_id") or "")
    if not task_id.endswith(suffix):
        findings.append("task_id_mode_suffix_mismatch")
    if task_spec.get("mode") != expected_mode:
        findings.append("task_spec_mode_mismatch")
    if task_spec.get("task_mode") != expected_task_mode:
        findings.append("task_spec_task_mode_mismatch")
    if task_spec.get("scientific_mode") != expected_mode:
        findings.append("task_spec_scientific_mode_mismatch")
    if task_spec.get("task_id") != task_id:
        findings.append("task_spec_task_id_mismatch")
    if not str(task_info.get("task_pair_id") or "").strip():
        findings.append("task_info_task_pair_id_missing")
    if task_spec.get("task_pair_id") != task_info.get("task_pair_id"):
        findings.append("task_spec_task_pair_id_mismatch")
    scientific_question = str(task_spec.get("scientific_question") or "").strip()
    task_info_question = str(task_info.get("scientific_question") or "").strip()
    if not scientific_question:
        findings.append("task_spec_scientific_question_missing")
    if not task_info_question:
        findings.append("task_info_scientific_question_missing")
    elif scientific_question and task_info_question != scientific_question:
        findings.append("task_info_spec_scientific_question_mismatch")
    task_markdown = task_root / "task.md"
    if not task_markdown.read_text(encoding="utf-8", errors="strict").strip():
        findings.append("task_instruction_missing")
    if not task_info.get("required_deliverables"):
        findings.append("required_deliverables_missing")
    else:
        deliverable_paths: list[str] = []
        for deliverable in task_info.get("required_deliverables") or []:
            try:
                path = validate_relative_path(str(deliverable.get("path") or ""))
            except (AttributeError, ValueError):
                findings.append("required_deliverable_path_invalid")
                continue
            deliverable_paths.append(path)
        contract_paths = submission_contract.get("required_files") or []
        if sorted(deliverable_paths) != sorted(str(path) for path in contract_paths):
            findings.append("submission_contract_deliverables_mismatch")
    rubric = read_json(task_root / "process_rubric.json")
    # The pipeline defines process Key Points, but does not prescribe a scoring
    # scale or weighting policy.  A downstream evaluator may attach weights.
    findings.extend(validate_rubric(rubric, expected_total=None, label="process"))
    input_root = task_root / "data" / "inputs"
    if not input_root.is_dir():
        findings.append("inputs_directory_missing")
    else:
        for asset in task_spec.get("input_assets") or []:
            try:
                relative = validate_relative_path(str(asset.get("path") or ""))
            except (AttributeError, ValueError):
                findings.append("task_spec_input_path_invalid")
                continue
            relative = relative.removeprefix("data/inputs/").removeprefix("inputs/")
            asset_path = input_root / relative
            if not asset_path.is_file():
                findings.append(f"task_spec_input_missing:{relative}")
                continue
            findings.extend(_input_asset_integrity_findings(asset_path, relative))
    public_runtime_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in task_root.rglob("*")
        if path.is_file() and path.suffix.casefold() in {".md", ".json", ".txt"}
    )
    if "task/inputs" in public_runtime_text or "task/outputs" in public_runtime_text:
        findings.append("construction_workspace_path_leaked")
    if "inputs/documents/" in public_runtime_text or "outputs/public_inputs/" in public_runtime_text:
        findings.append("construction_source_path_leaked")
    if expected_mode == "paper_reproduction":
        for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
            if not (task_root / name).is_file():
                findings.append(f"missing_reproduction_file:{name}")
        route_criteria = [
            row
            for row in rubric
            if isinstance(row, dict)
            and str(row.get("criterion_type") or "").casefold() == "route_fidelity"
        ]
        if not route_criteria:
            findings.append("reproduction_route_fidelity_rubric_missing")
        required_files = {
            str(path) for path in submission_contract.get("required_files") or []
        }
        for criterion in route_criteria:
            evidence_artifacts = criterion.get("evidence_artifacts") or []
            if isinstance(evidence_artifacts, str):
                evidence_artifacts = [evidence_artifacts]
            if not evidence_artifacts:
                findings.append("reproduction_route_fidelity_evidence_missing")
            for artifact_path in evidence_artifacts:
                if str(artifact_path) not in required_files:
                    findings.append(
                        "reproduction_route_fidelity_evidence_not_required:"
                        f"{artifact_path}"
                    )
    return findings


def validate_hidden_reference(
    hidden: dict[str, Any],
    *,
    expected_ground_truth_items: list[dict[str, Any]] | None = None,
    submission_contract: dict[str, Any] | None = None,
) -> list[str]:
    findings: list[str] = []
    if hidden.get("status") != "ready":
        return ["hidden_reference_not_ready"]
    profiles = hidden.get("acceptance_profiles") or []
    profile_ids = [row.get("acceptance_profile_id") for row in profiles]
    if not profiles or None in profile_ids or len(profile_ids) != len(set(profile_ids)):
        findings.append("acceptance_profile_ids_invalid")
    for profile in profiles:
        if profile.get("type") not in ACCEPTANCE_TYPES:
            findings.append(f"invalid_acceptance_profile:{profile.get('acceptance_profile_id')}")
        findings.extend(
            _acceptance_profile_findings(
                profile,
                submission_contract=submission_contract,
            )
        )
    truths = hidden.get("ground_truth_items") or []
    if not truths:
        findings.append("hidden_ground_truth_empty")
    truth_ids = [row.get("ground_truth_id") for row in truths]
    if None in truth_ids or len(truth_ids) != len(set(truth_ids)):
        findings.append("ground_truth_ids_invalid")
    profile_owners: dict[str, list[str]] = {}
    profiles_by_id = {
        str(row.get("acceptance_profile_id")): row
        for row in profiles
        if isinstance(row, dict) and row.get("acceptance_profile_id")
    }
    for truth in truths:
        ground_truth_id = str(truth.get("ground_truth_id") or "missing")
        profile_id = truth.get("acceptance_profile_id")
        if profile_id not in profile_ids:
            findings.append(f"ground_truth_profile_missing:{truth.get('ground_truth_id')}")
        else:
            profile_owners.setdefault(str(profile_id), []).append(ground_truth_id)
        if truth.get("evidence_grade") not in {"A", "B", "C", "D"}:
            findings.append(f"hidden_evidence_grade_invalid:{truth.get('ground_truth_id')}")
        if truth.get("claim_role") not in {"intermediate", "final"}:
            findings.append(f"hidden_claim_role_invalid:{truth.get('ground_truth_id')}")
        if _contains_scoring_placeholder(
            {
                "canonical_answer": truth.get("canonical_answer"),
                "required_propositions": truth.get("required_propositions"),
            }
        ):
            findings.append(f"ground_truth_answer_placeholder:{ground_truth_id}")
        raw_truth_scope = truth.get("applies_to_modes")
        truth_scope = normalize_mode_scope(raw_truth_scope)
        if truth_scope is None:
            findings.append(f"ground_truth_mode_scope_invalid:{truth.get('ground_truth_id')}")
        profile = profiles_by_id.get(str(profile_id))
        if profile is not None:
            raw_profile_scope = profile.get("applies_to_modes")
            profile_scope = normalize_mode_scope(raw_profile_scope)
            if profile_scope is None:
                findings.append(
                    f"acceptance_profile_mode_scope_invalid:{profile.get('acceptance_profile_id')}"
                )
            elif (
                truth_scope is not None
                and "applies_to_modes" in profile
                and set(truth_scope) != set(profile_scope)
            ):
                findings.append(
                    f"ground_truth_profile_mode_scope_mismatch:{ground_truth_id}"
                )
            findings.extend(_ground_truth_profile_consistency_findings(truth, profile))
    findings.extend(validate_ground_truth_consistency(truths))
    for profile_id in profile_ids:
        if len(profile_owners.get(str(profile_id), [])) != 1:
            findings.append(f"acceptance_profile_not_item_specific:{profile_id}")
    if expected_ground_truth_items is not None:
        findings.extend(_frozen_ground_truth_findings(truths, expected_ground_truth_items))

    rubric = hidden.get("scientific_conclusion_rubric") or []
    covered_truth_ids: set[str] = set()
    for criterion in rubric:
        if not isinstance(criterion, dict):
            continue
        criterion_id = str(criterion.get("id") or "missing")
        if _contains_scoring_placeholder(
            {
                "statement": criterion.get("statement"),
                "acceptance_rule": criterion.get("acceptance_rule"),
            }
        ):
            findings.append(f"conclusion_rubric_placeholder:{criterion_id}")
        criterion_truth_ids = criterion.get("ground_truth_ids") or []
        criterion_profile_ids = criterion.get("acceptance_profile_ids") or []
        if not criterion_truth_ids:
            findings.append(f"conclusion_rubric_ground_truth_refs_missing:{criterion_id}")
        if not criterion_profile_ids:
            findings.append(f"conclusion_rubric_profile_refs_missing:{criterion_id}")
        for ground_truth_id in criterion_truth_ids:
            if ground_truth_id not in truth_ids:
                findings.append(
                    f"conclusion_rubric_ground_truth_ref_unknown:{criterion_id}:{ground_truth_id}"
                )
            else:
                covered_truth_ids.add(str(ground_truth_id))
        for profile_id in criterion_profile_ids:
            if profile_id not in profile_ids:
                findings.append(
                    f"conclusion_rubric_profile_ref_unknown:{criterion_id}:{profile_id}"
                )
        expected_profiles = {
            str(truth.get("acceptance_profile_id"))
            for truth in truths
            if truth.get("ground_truth_id") in criterion_truth_ids
        }
        if expected_profiles and not expected_profiles.issubset(set(criterion_profile_ids)):
            findings.append(f"conclusion_rubric_profile_ref_mismatch:{criterion_id}")
    for ground_truth_id in set(str(value) for value in truth_ids if value):
        if ground_truth_id not in covered_truth_ids:
            findings.append(f"ground_truth_not_scored:{ground_truth_id}")
    findings.extend(
        validate_rubric(
            rubric,
            expected_total=None,
            label="conclusion",
            require_conclusion_fields=True,
        )
    )
    if _contains_scoring_placeholder(hidden.get("summary")):
        findings.append("hidden_summary_placeholder")
    return sorted(set(findings))


def validate_ground_truth_consistency(truths: Any) -> list[str]:
    """Catch deterministic numeric/text contradictions before model-based auditing."""

    findings: list[str] = []
    for truth in truths if isinstance(truths, list) else []:
        if not isinstance(truth, dict):
            continue
        identifier = str(truth.get("ground_truth_id") or "missing")
        required = {
            _normalize_text(_proposition_text(row))
            for row in truth.get("required_propositions") or []
            if _normalize_text(_proposition_text(row))
        }
        forbidden = {
            _normalize_text(_proposition_text(row))
            for row in truth.get("forbidden_contradictions") or []
            if _normalize_text(_proposition_text(row))
        }
        if required & forbidden:
            findings.append(f"ground_truth_required_forbidden_conflict:{identifier}")
        canonical = truth.get("canonical_answer")
        if isinstance(canonical, str):
            normalized_canonical = _normalize_text(canonical)
            if normalized_canonical and normalized_canonical in forbidden:
                findings.append(f"ground_truth_canonical_forbidden_conflict:{identifier}")
        for key, number in _numeric_ground_truth_values(canonical):
            key_text = _normalize_text(key.replace("_", " ").replace("-", " "))
            if not key_text:
                continue
            for proposition in required:
                if key_text not in proposition:
                    continue
                if number < 0 and re.search(r"\b(?:positive|greater than zero|above zero)\b", proposition):
                    findings.append(f"ground_truth_numeric_text_sign_conflict:{identifier}:{key}")
                if number > 0 and re.search(r"\b(?:negative|less than zero|below zero)\b", proposition):
                    findings.append(f"ground_truth_numeric_text_sign_conflict:{identifier}:{key}")
    return sorted(set(findings))


def _ground_truth_profile_consistency_findings(
    truth: dict[str, Any], profile: dict[str, Any]
) -> list[str]:
    identifier = str(truth.get("ground_truth_id") or "missing")
    profile_type = str(profile.get("type") or "")
    canonical = truth.get("canonical_answer")
    findings: list[str] = []
    if profile_type == "numeric_tolerance":
        numeric_values = _numeric_ground_truth_values(canonical)
        target = profile.get("target")
        if len(numeric_values) == 1 and isinstance(target, (int, float)):
            if not math.isclose(float(numeric_values[0][1]), float(target), rel_tol=1e-12, abs_tol=1e-12):
                findings.append(f"ground_truth_numeric_profile_conflict:{identifier}")
    elif profile_type == "categorical" and profile.get("target") != canonical:
        findings.append(f"ground_truth_categorical_profile_conflict:{identifier}")
    elif profile_type == "ranking" and isinstance(canonical, list):
        target_order = profile.get("target_order")
        if target_order is not None and target_order != canonical:
            findings.append(f"ground_truth_ranking_profile_conflict:{identifier}")
    elif profile_type in {"mechanism_claim", "semantic_propositions"}:
        truth_required = {
            _normalize_text(_proposition_text(row))
            for row in truth.get("required_propositions") or []
        }
        profile_required = {
            _normalize_text(_proposition_text(row))
            for row in profile.get("required_propositions") or []
        }
        if truth_required and profile_required and truth_required != profile_required:
            findings.append(f"ground_truth_semantic_profile_conflict:{identifier}")
    binding = profile.get("submission_binding") or {}
    projection = binding.get("canonical_projection")
    if projection is not None:
        # Textual conclusions are intentionally represented twice: the human-readable
        # canonical answer lives on the Ground Truth item, while the submission
        # binding stores the machine-checkable proposition set.  Comparing those
        # JSON shapes directly rejects valid semantic answers.
        if profile_type in {"mechanism_claim", "semantic_propositions"}:
            profile_required = {
                _normalize_text(_proposition_text(row))
                for row in profile.get("required_propositions") or []
                if _normalize_text(_proposition_text(row))
            }
            profile_forbidden = {
                _normalize_text(_proposition_text(row))
                for row in profile.get("forbidden_contradictions") or []
                if _normalize_text(_proposition_text(row))
            }
            projected_required = {
                _normalize_text(_proposition_text(row))
                for row in (projection.get("required_propositions") or [])
                if _normalize_text(_proposition_text(row))
            } if isinstance(projection, dict) else set()
            projected_forbidden = {
                _normalize_text(_proposition_text(row))
                for row in (projection.get("forbidden_contradictions") or [])
                if _normalize_text(_proposition_text(row))
            } if isinstance(projection, dict) else set()
            truth_required = {
                _normalize_text(_proposition_text(row))
                for row in truth.get("required_propositions") or []
                if _normalize_text(_proposition_text(row))
            }
            truth_forbidden = {
                _normalize_text(_proposition_text(row))
                for row in truth.get("forbidden_contradictions") or []
                if _normalize_text(_proposition_text(row))
            }
            if truth_required != profile_required or truth_forbidden != profile_forbidden:
                findings.append(f"ground_truth_submission_projection_conflict:{identifier}")
            if isinstance(projection, dict) and (
                ("required_propositions" in projection and projected_required != truth_required)
                or ("forbidden_contradictions" in projection and projected_forbidden != truth_forbidden)
            ):
                findings.append(f"ground_truth_submission_projection_conflict:{identifier}")
        elif not _canonical_projection_matches(canonical, projection):
            findings.append(f"ground_truth_submission_projection_conflict:{identifier}")
    return findings


def _numeric_ground_truth_values(value: Any) -> list[tuple[str, float]]:
    if isinstance(value, bool):
        return []
    if isinstance(value, (int, float)):
        return [("value", float(value))]
    if not isinstance(value, dict):
        return []
    return [
        (str(key), float(nested))
        for key, nested in value.items()
        if isinstance(nested, (int, float)) and not isinstance(nested, bool)
    ]


def _proposition_text(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("statement") or value.get("text") or "")
    return str(value or "")


def _canonical_projection_matches(canonical: Any, projection: Any) -> bool:
    if canonical == projection:
        return True
    if isinstance(canonical, dict) and isinstance(projection, dict):
        return all(key in projection and projection[key] == value for key, value in canonical.items())
    numeric = _numeric_ground_truth_values(canonical)
    return len(numeric) == 1 and isinstance(projection, (int, float)) and math.isclose(
        numeric[0][1], float(projection), rel_tol=1e-12, abs_tol=1e-12
    )


def _frozen_ground_truth_findings(
    actual: list[dict[str, Any]], expected: list[dict[str, Any]]
) -> list[str]:
    findings: list[str] = []
    actual_by_id = {str(row.get("ground_truth_id")): row for row in actual}
    expected_by_id = {str(row.get("ground_truth_id")): row for row in expected}
    if set(actual_by_id) != set(expected_by_id):
        findings.append("hidden_ground_truth_target_set_changed")
    frozen_fields = (
        "kind",
        "canonical_answer",
        "required_propositions",
        "forbidden_contradictions",
        "acceptance_type",
        "acceptance_parameters",
        "evidence_grade",
        "evidence_ids",
        "claim_role",
    )
    for ground_truth_id in sorted(set(actual_by_id) & set(expected_by_id)):
        for field in frozen_fields:
            if actual_by_id[ground_truth_id].get(field) != expected_by_id[ground_truth_id].get(
                field
            ):
                findings.append(f"hidden_ground_truth_frozen_field_changed:{ground_truth_id}:{field}")
    return findings


def validate_task_pair(pair_root: Path) -> dict[str, Any]:
    findings: list[str] = []
    autonomous = pair_root / "autonomous_research"
    reproduction = pair_root / "paper_reproduction"
    hidden_root = pair_root / "hidden_reference"
    construction_path = pair_root / "construction_record.json"
    construction = read_json(construction_path) if construction_path.is_file() else {}
    single_agent_pair = construction.get("mode_generation_strategy") == "single_agent"
    findings.extend(validate_mode_task(autonomous, expected_mode="autonomous_research"))
    findings.extend(validate_mode_task(reproduction, expected_mode="paper_reproduction"))
    for name in ("paper_info.json", "evidence_index.json", "source_manifest.json"):
        if not (pair_root / name).is_file():
            findings.append(f"missing_pair_metadata:{name}")
    workflow_review_path = pair_root / "workflow_review.json"
    if single_agent_pair and not workflow_review_path.is_file():
        findings.append("missing_pair_metadata:workflow_review.json")
    if workflow_review_path.is_file():
        workflow_review = read_json(workflow_review_path)
        evidence_path = pair_root / "evidence_index.json"
        evidence_ids = {
            str(row.get("evidence_id"))
            for row in (read_json(evidence_path) if evidence_path.is_file() else [])
            if isinstance(row, dict) and row.get("evidence_id")
        }
        findings.extend(
            validate_workflow_scope(
                workflow_review.get("workflow_scope") or {}, evidence_ids
            )
        )
        findings.extend(
            validate_complexity_profile(
                workflow_review.get("complexity_profile") or {},
                workflow_steps=workflow_review.get("workflow_steps") or [],
            )
        )
        for field in (
            "paper_workflow_inventory_complete",
            "full_paper_workflow_checked",
            "alternative_scope_search_complete",
        ):
            if workflow_review.get(field) is not True:
                findings.append(f"workflow_review_{field}_false")
    common_path = hidden_root / "ground_truth_common.json"
    if not common_path.is_file():
        findings.append("missing_ground_truth_common")
    else:
        hidden = read_json(common_path)
        submission_path = autonomous / "submission_contract.json"
        findings.extend(
            validate_hidden_reference(
                hidden,
                submission_contract=(
                    read_json(submission_path) if submission_path.is_file() else None
                ),
            )
        )
        findings.extend(_evaluation_ground_truth_findings(pair_root, hidden))
    autonomous_inputs = directory_manifest(autonomous / "data")
    reproduction_inputs = directory_manifest(reproduction / "data")
    if autonomous_inputs["content_hash"] != reproduction_inputs["content_hash"]:
        findings.append("mode_input_assets_differ")
    # Mode-specific result paths/field names are allowed.  Each mode's
    # contract is checked independently and hidden bindings are checked against
    # the mode they apply to; literal cross-mode equality would reject valid
    # autonomous neutralization.
    findings.extend(_pair_identity_findings(autonomous, reproduction))
    findings.extend(_derived_copy_findings(autonomous, reproduction))
    findings.extend(_autonomous_copy_integrity_findings(autonomous, reproduction))
    disclosure_path = hidden_root / "disclosure_contract.json"
    if disclosure_path.is_file():
        disclosure = read_json(disclosure_path)
        autonomous_allowed = disclosure.get("autonomous_allowed") or {}
        public_basis = autonomous_allowed.get("public_task_basis") or {}
        expected_boundaries = public_basis.get("boundary_conditions")
        findings.extend(
            validate_task_boundary_conditions(
                autonomous,
                expected_conditions=expected_boundaries,
            )
        )
        findings.extend(
            validate_task_boundary_conditions(
                reproduction,
                expected_conditions=expected_boundaries,
            )
        )
        reproduction_allowed = disclosure.get("reproduction_additional_allowed") or {}
        findings.extend(
            validate_autonomous_route_isolation(
                autonomous,
                paper_route=reproduction_allowed.get("paper_route") or {},
                allowed_boundary_conditions=expected_boundaries,
                allowed_method_constraints=public_basis.get("method_constraints")
                or public_basis.get("public_method_constraints"),
            )
        )
    if common_path.is_file():
        findings.extend(_leakage_findings(pair_root, read_json(common_path)))
    return {
        "passed": not findings,
        "findings": sorted(set(findings)),
        "autonomous_input_hash": autonomous_inputs["content_hash"],
        "reproduction_input_hash": reproduction_inputs["content_hash"],
    }


def validate_task_pair_draft(
    pair_root: Path,
    *,
    review: dict[str, Any],
) -> list[str]:
    """Validate Agent staging output before orchestrator metadata is materialized."""

    findings: list[str] = []
    autonomous = pair_root / "autonomous_research"
    reproduction = pair_root / "paper_reproduction"
    hidden_root = pair_root / "hidden_reference"
    findings.extend(validate_mode_task(autonomous, expected_mode="autonomous_research"))
    findings.extend(validate_mode_task(reproduction, expected_mode="paper_reproduction"))
    hidden_path = hidden_root / "ground_truth_common.json"
    if not hidden_path.is_file():
        findings.append("missing_ground_truth_common")
    elif (autonomous / "submission_contract.json").is_file():
        findings.extend(
            validate_hidden_reference(
                read_json(hidden_path),
                expected_ground_truth_items=review.get("ground_truth_items") or [],
                submission_contract=read_json(autonomous / "submission_contract.json"),
            )
        )
    if (autonomous / "data").is_dir() and (reproduction / "data").is_dir():
        if directory_manifest(autonomous / "data")["content_hash"] != directory_manifest(
            reproduction / "data"
        )["content_hash"]:
            findings.append("mode_input_assets_differ")
    # Do not require literal submission-contract equality between modes.
    # Autonomous conversion may legitimately rename artifacts and fields.
    findings.extend(_pair_identity_findings(autonomous, reproduction))
    findings.extend(_derived_copy_findings(autonomous, reproduction))
    findings.extend(_autonomous_copy_integrity_findings(autonomous, reproduction))
    public_basis = review.get("public_task_basis") or {}
    boundary_conditions = public_basis.get("boundary_conditions")
    findings.extend(
        validate_task_boundary_conditions(
            autonomous, expected_conditions=boundary_conditions
        )
    )
    findings.extend(
        validate_task_boundary_conditions(
            reproduction, expected_conditions=boundary_conditions
        )
    )
    findings.extend(
        validate_autonomous_route_isolation(
            autonomous,
            paper_route=review.get("paper_route") or {},
            allowed_boundary_conditions=boundary_conditions,
            allowed_method_constraints=(review.get("public_task_basis") or {}).get(
                "method_constraints"
            )
            or (review.get("public_task_basis") or {}).get("public_method_constraints"),
        )
    )
    expected_scope = dict(review.get("workflow_scope") or {})
    # Legacy reviews omitted the autonomous scope.  Pair normalization writes
    # the explicit method-discovery default, so compare against that canonical
    # transport projection rather than treating the added metadata as drift.
    expected_scope.setdefault("autonomy_scope", "fixed_input_method_discovery")
    expected_complexity = review.get("complexity_profile") or {}
    for mode_root in (autonomous, reproduction):
        for file_name in ("task_info.json", "task_spec.json"):
            path = mode_root / file_name
            if not path.is_file():
                continue
            value = read_json(path)
            if value.get("workflow_scope") != expected_scope:
                findings.append(f"mode_workflow_scope_not_frozen:{mode_root.name}:{file_name}")
            if value.get("complexity_profile") != expected_complexity:
                findings.append(
                    f"mode_complexity_profile_not_frozen:{mode_root.name}:{file_name}"
                )
    for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
        if (autonomous / name).exists():
            findings.append(f"autonomous_reproduction_file_present:{name}")
    return sorted(set(findings))


def validate_rubric(
    rubric: Any,
    *,
    expected_total: float | None,
    label: str,
    require_conclusion_fields: bool = False,
) -> list[str]:
    findings: list[str] = []
    if not isinstance(rubric, list) or not rubric:
        return [f"{label}_rubric_empty"]
    ids: list[str] = []
    total = 0.0
    for row in rubric:
        if not isinstance(row, dict):
            findings.append(f"{label}_rubric_criterion_invalid")
            continue
        criterion_id = str(row.get("id") or "").strip()
        score_declared = any(
            key in row and row.get(key) not in (None, "")
            for key in ("max_score", "max_points", "points", "weight")
        )
        try:
            maximum = float(
                row.get("max_score", row.get("max_points", row.get("points", row.get("weight", 0))))
                or 0
            )
        except (TypeError, ValueError):
            maximum = 0.0
        if not criterion_id or (score_declared and maximum <= 0):
            findings.append(f"{label}_rubric_criterion_invalid")
        ids.append(criterion_id)
        total += maximum
        if require_conclusion_fields and (
            not str(row.get("statement") or "").strip()
            or not str(row.get("acceptance_rule") or "").strip()
            or not row.get("required_evidence")
        ):
            findings.append(f"{label}_rubric_contract_incomplete:{criterion_id}")
    if len(ids) != len(set(ids)):
        findings.append(f"{label}_rubric_ids_not_unique")
    if expected_total is not None and not math.isclose(total, expected_total, abs_tol=1e-8):
        findings.append(f"{label}_rubric_total_is_{total:g}")
    return findings


def _review_disclosure_findings(review: dict[str, Any]) -> list[str]:
    public_payload = {
        "public_scientific_question": review.get("public_scientific_question"),
        "public_task_basis": _without_asset_content(review.get("public_task_basis") or {}),
    }
    public_text = _normalize_text(json.dumps(public_payload, ensure_ascii=False, sort_keys=True))
    raw_route_text = json.dumps(
        {
            "paper_route": review.get("paper_route") or {},
            "workflow_steps": review.get("workflow_steps") or [],
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    route_text = _normalize_text(raw_route_text)
    complete_public_text = _normalize_text(
        json.dumps(
            {
                "public_scientific_question": review.get("public_scientific_question"),
                "public_task_basis": review.get("public_task_basis") or {},
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    findings: list[str] = []
    paper_route = review.get("paper_route") or {}
    declared_tokens = paper_route.get("autonomous_forbidden_disclosures") or []
    route_tokens = {
        _normalize_text(str(token))
        for token in [*declared_tokens, *_structured_route_tokens(paper_route)]
        if _normalize_text(str(token))
    }
    allowed_boundary_aliases = _allowed_public_boundary_aliases(
        (review.get("public_task_basis") or {}).get("boundary_conditions") or []
    )
    for token in sorted(route_tokens):
        if token in allowed_boundary_aliases:
            continue
        if _route_token_present(token, complete_public_text):
            findings.append(f"review_public_route_disclosure:{token}")
    result_directive_patterns = (
        r"\b(?:compare|comparison|agreement|match)\b.{0,120}\b(?:table|figure|fig)\s+[a-z0-9.-]+.{0,40}\b(?:value|result|trend)",
        r"\b(?:compare|match)\b.{0,120}\b(?:against|with|to)\b.{0,40}\b(?:paper|published|table|figure|fig)\b",
        r"\bagreement\b.{0,80}\b(?:with|to)\b.{0,40}\b(?:paper|published|table|figure|fig)\b",
        r"\b(?:verify|confirm)\b.{0,120}\b(?:paper[- ]reported|published|expected)\b.{0,80}\b(?:lowest|ordering|favou?red|matched|mismatched|efficient|inefficient)\b",
    )
    if any(
        re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        for text in _string_leaves(
            {
                "paper_route": review.get("paper_route") or {},
                "workflow_steps": review.get("workflow_steps") or [],
            }
        )
        for pattern in result_directive_patterns
    ):
        findings.append("review_reproduction_route_uses_hidden_result")
    for truth in review.get("ground_truth_items") or []:
        if not isinstance(truth, dict):
            findings.append("review_ground_truth_item_invalid")
            continue
        identifier = str(truth.get("ground_truth_id") or "unknown")
        tokens = _review_sensitive_values(truth.get("canonical_answer"))
        if any(_sensitive_value_present(token, public_text) for token in tokens):
            findings.append(f"review_public_answer_leakage:{identifier}")
        if any(_sensitive_value_present(token, route_text) for token in tokens):
            findings.append(f"review_paper_route_answer_leakage:{identifier}")
        propositions = truth.get("required_propositions") or []
        for proposition in propositions:
            text = proposition.get("statement") if isinstance(proposition, dict) else proposition
            normalized = _normalize_text(str(text or ""))
            if len(normalized) < 48:
                continue
            if normalized in public_text:
                findings.append(f"review_public_conclusion_leakage:{identifier}")
            if normalized in route_text:
                findings.append(f"review_paper_route_conclusion_leakage:{identifier}")
    return findings


def _string_leaves(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [text for nested in value.values() for text in _string_leaves(nested)]
    if isinstance(value, list):
        return [text for nested in value for text in _string_leaves(nested)]
    return [value] if isinstance(value, str) else []


def _structured_route_tokens(route: dict[str, Any]) -> list[str]:
    output: list[str] = []
    route_fields = {
        "software",
        "program",
        "package",
        "functional",
        "basis",
        "basis_set",
        "method",
        "level_of_theory",
        "ground_state",
        "excited_state",
        "force_field",
    }

    def visit(value: Any, key: str = "") -> None:
        normalized_key = key.casefold().replace("-", "_")
        if isinstance(value, dict):
            for nested_key, nested in value.items():
                visit(nested, str(nested_key))
            return
        if isinstance(value, list):
            for nested in value:
                visit(nested, key)
            return
        if normalized_key not in route_fields or not isinstance(value, str):
            return
        raw = value.strip()
        if not raw:
            return
        if normalized_key in {"software", "program", "package"}:
            output.append(raw)
            output.extend(re.findall(r"[A-Za-z][A-Za-z0-9+.-]{3,}", raw))
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9+().-]{2,}", raw):
            if any(character.isdigit() for character in token) or token.isupper():
                output.append(token)

    visit(route)
    return output


def _route_token_present(token: str, normalized_public: str) -> bool:
    normalized = _normalize_text(token)
    short_route_tokens = {"c2v", "dft", "md", "neb", "pcm", "smd"}
    if len(normalized) < 4 and normalized not in short_route_tokens:
        return False
    return bool(
        re.search(
            rf"(?<![a-z0-9]){re.escape(normalized)}(?![a-z0-9])",
            normalized_public,
        )
    )


def _without_asset_content(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_asset_content(nested)
            for key, nested in value.items()
            if key not in {"content", "content_path"}
        }
    if isinstance(value, list):
        return [_without_asset_content(item) for item in value]
    return value


def _review_sensitive_values(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, dict):
        for nested in value.values():
            output.extend(_review_sensitive_values(nested))
    elif isinstance(value, list):
        for nested in value:
            output.extend(_review_sensitive_values(nested))
    elif isinstance(value, float):
        output.append(str(value))
    elif isinstance(value, int) and len(str(value).lstrip("+-")) >= 3:
        output.append(str(value))
    elif isinstance(value, str) and len(_normalize_text(value)) >= 48:
        output.append(value)
    return output


def _pair_identity_findings(autonomous: Path, reproduction: Path) -> list[str]:
    findings: list[str] = []
    try:
        a_info = read_json(autonomous / "task_info.json")
        r_info = read_json(reproduction / "task_info.json")
        a_spec = read_json(autonomous / "task_spec.json")
        r_spec = read_json(reproduction / "task_spec.json")
    except (OSError, json.JSONDecodeError):
        return ["mode_pair_json_unreadable"]
    for field in (
        "source_id",
        "category",
        "benchmark_family",
        "data",
        "archive_extractions",
        "workflow_scope",
        "complexity_profile",
    ):
        if a_info.get(field) != r_info.get(field):
            findings.append(f"mode_pair_task_info_differs:{field}")
    for field in (
        "task_pair_id",
        "scientific_question",
        "target_definition",
        "input_assets",
        "boundary_conditions",
        "workflow_scope",
        "complexity_profile",
    ):
        if a_spec.get(field) != r_spec.get(field):
            findings.append(f"mode_pair_task_spec_differs:{field}")
    return findings


def _autonomous_copy_integrity_findings(
    autonomous: Path, reproduction: Path
) -> list[str]:
    if not (autonomous / "derived_from.json").is_file():
        return []
    editable = {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "process_rubric.json",
    }
    generated = {"derived_from.json", "conversion_contract.json", "public_manifest.json"}
    reproduction_only = {"paper_route.md", "workflow_spec.json", "route_evidence_map.json"}
    before = {
        row["path"]: row["sha256"]
        for row in directory_manifest(reproduction).get("files") or []
        if row["path"] != "public_manifest.json"
    }
    after = {
        row["path"]: row["sha256"]
        for row in directory_manifest(autonomous).get("files") or []
        if row["path"] != "public_manifest.json"
    }
    findings: list[str] = []
    for path, digest in before.items():
        if path in editable or path in reproduction_only:
            continue
        if after.get(path) != digest:
            findings.append(f"autonomous_immutable_file_changed:{path}")
    allowed_after = (set(before) - reproduction_only) | editable | generated
    for path in sorted(set(after) - allowed_after):
        findings.append(f"autonomous_unauthorized_file_added:{path}")
    return findings


def _derived_copy_findings(autonomous: Path, reproduction: Path) -> list[str]:
    autonomous_path = autonomous / "derived_from.json"
    if autonomous_path.is_file():
        value = read_json(autonomous_path)
        findings: list[str] = []
        if value.get("derived_from_mode") != "paper_reproduction":
            findings.append("autonomous_copy_source_invalid")
        expected_hash = _stable_mode_tree_hash(
            reproduction, excluded={"public_manifest.json"}
        )
        if value.get("base_manifest_hash") != expected_hash:
            findings.append("autonomous_base_manifest_hash_mismatch")
        allowed = {
            "task.md",
            "task_info.json",
            "task_spec.json",
            "process_rubric.json",
        }
        if set(value.get("editable_files") or []) != allowed:
            findings.append("autonomous_copy_edit_allowlist_invalid")
        return findings

    # Current task bundles intentionally contain no source/derivation contract: those
    # files disclose construction history and are not evaluation inputs.  Pair-level
    # ``conversion_report.json`` is optional audit metadata, so absence of a mode-local
    # provenance file is not a validation failure.  Keep the old compatibility branch
    # only when a legacy file is actually present.
    reproduction_path = reproduction / "derived_from.json"
    if not reproduction_path.is_file():
        return []
    value = read_json(reproduction_path)
    findings = []
    if value.get("derived_from_mode") != "autonomous_research":
        findings.append("reproduction_copy_source_invalid")
    if value.get("base_manifest_hash") != directory_manifest(autonomous)["content_hash"]:
        findings.append("reproduction_base_manifest_hash_mismatch")
    return findings


def _stable_mode_tree_hash(root: Path, *, excluded: set[str]) -> str:
    manifest = directory_manifest(root)
    files = [
        {"path": row["path"], "sha256": row["sha256"]}
        for row in manifest.get("files") or []
        if row.get("path") not in excluded
    ]
    return canonical_hash(files)


def _acceptance_profile_findings(
    profile: dict[str, Any],
    *,
    submission_contract: dict[str, Any] | None = None,
    required_binding_modes: set[str] | None = None,
) -> list[str]:
    identifier = str(profile.get("acceptance_profile_id") or "missing")
    profile_type = profile.get("type")
    findings = acceptance_profile_type_findings(profile, identifier=identifier)
    if submission_contract is not None:
        findings.extend(
            _submission_binding_findings(
                profile,
                submission_contract=submission_contract,
                identifier=identifier,
                required_binding_modes=required_binding_modes,
            )
        )
    return findings


def hidden_reference_transport_findings(
    hidden: Any,
    *,
    require_ready_ground_truth: bool = False,
) -> list[str]:
    """Check hidden-contract ownership and mode scope before syntax projection.

    This is deliberately a transport check.  It does not inspect a target value,
    scientific proposition, unit, or comparison semantics.  It exists before the
    alias normalizer so malformed ownership cannot be hidden by a lossy projection.
    ``require_ready_ground_truth`` is used at Stage06/07 production boundaries;
    older lightweight fixtures without a ready status remain compatible.
    """

    if not isinstance(hidden, dict):
        return ["hidden_reference_transport_not_object"]
    # A few evaluator/gate callers intentionally use a minimal legacy envelope
    # while constructing a task (for example ``expected_result`` only).  The
    # ownership contract becomes authoritative only once the hidden artifact
    # explicitly declares ``status=ready``.  Keep those draft/legacy envelopes
    # observationally compatible; the production Stage06/07 paths invoke this
    # function with ``require_ready_ground_truth=True`` and therefore still
    # enforce every finding on a ready contract.
    if require_ready_ground_truth and hidden.get("status") != "ready":
        return []
    raw_truths = hidden.get("ground_truth_items")
    raw_profiles = hidden.get("acceptance_profiles")
    findings: list[str] = []
    if not isinstance(raw_truths, list):
        findings.append("hidden_ground_truth_items_not_array")
        raw_truths = []
    if not isinstance(raw_profiles, list):
        findings.append("hidden_reference_profiles_not_array")
        raw_profiles = []
    truths = [row for row in raw_truths if isinstance(row, dict)]
    profiles = [row for row in raw_profiles if isinstance(row, dict)]
    if any(not isinstance(row, dict) for row in raw_truths):
        findings.append("hidden_ground_truth_item_not_object")
    if any(not isinstance(row, dict) for row in raw_profiles):
        findings.append("hidden_reference_profile_not_object")
    authoritative_ownership = bool(truths) or (
        require_ready_ground_truth and hidden.get("status") == "ready"
    )
    if require_ready_ground_truth and hidden.get("status") == "ready" and not truths:
        findings.append("hidden_ground_truth_empty")

    truth_refs: dict[str, list[str]] = {}
    truth_scopes: dict[str, list[str]] = {}
    for index, truth in enumerate(truths, start=1):
        truth_id = str(truth.get("ground_truth_id") or f"missing-{index}")
        raw_reference = str(
            truth.get("acceptance_profile_id")
            or truth.get("acceptance_profile")
            or ""
        ).strip()
        if authoritative_ownership and not raw_reference:
            findings.append(f"ground_truth_profile_missing:{truth_id}")
        if raw_reference:
            truth_refs.setdefault(raw_reference, []).append(truth_id)
        scope = normalize_mode_scope(truth.get("applies_to_modes"))
        if scope is None and "applies_to_modes" in truth:
            findings.append(f"ground_truth_mode_scope_invalid:{truth_id}")
        elif scope is not None:
            truth_scopes[truth_id] = scope

    profile_ids: dict[str, list[dict[str, Any]]] = {}
    for profile in profiles:
        profile_id = str(
            profile.get("acceptance_profile_id") or profile.get("profile_id") or ""
        ).strip()
        if not profile_id:
            findings.append("acceptance_profile_id_missing")
            continue
        profile_ids.setdefault(profile_id, []).append(profile)
        scope = normalize_mode_scope(profile.get("applies_to_modes"))
        if scope is None and "applies_to_modes" in profile:
            findings.append(f"acceptance_profile_mode_scope_invalid:{profile_id}")
        shared = profile.get("submission_binding")
        has_mode_matrix = any(
            isinstance(profile.get(key), dict)
            for key in ("mode_submission_bindings", "submission_bindings_by_mode")
        )
        # A profile must have exactly one binding source.  Even a legacy
        # nested mode map under ``submission_binding`` is ambiguous when a
        # canonical mode matrix is also present: the two maps can disagree and
        # the normalizer would otherwise silently choose one.
        if has_mode_matrix and isinstance(shared, dict):
            findings.append(f"acceptance_submission_binding_ambiguous:{profile_id}")

    if authoritative_ownership:
        for profile_id, rows in profile_ids.items():
            if len(rows) != 1:
                findings.append(f"acceptance_profile_not_item_specific:{profile_id}")
            if profile_id not in truth_refs:
                findings.append(f"acceptance_profile_orphan:{profile_id}")
        for profile_id, owners in truth_refs.items():
            if len(owners) != 1:
                findings.append(f"acceptance_profile_not_item_specific:{profile_id}")
            if profile_id not in profile_ids:
                for truth_id in owners:
                    findings.append(f"ground_truth_profile_missing:{truth_id}")
                continue
            profile = profile_ids[profile_id][0]
            profile_scope = normalize_mode_scope(profile.get("applies_to_modes"))
            if profile_scope is None:
                continue
            # A profile without an explicit scope inherits its owner's scope
            # during the normalizer.  Once both sides explicitly declare a
            # scope, they must describe the same public modes; allowing a
            # profile to cover extra modes would make the evaluator inspect a
            # binding for which no Ground Truth exists.
            if "applies_to_modes" not in profile:
                continue
            for truth_id in owners:
                truth_scope = truth_scopes.get(truth_id)
                if truth_scope is not None and set(truth_scope) != set(profile_scope):
                    findings.append(f"ground_truth_profile_mode_scope_mismatch:{truth_id}")
    return sorted(set(findings))


def _submission_binding_findings(
    profile: dict[str, Any],
    *,
    submission_contract: dict[str, Any],
    identifier: str,
    required_binding_modes: set[str] | None = None,
) -> list[str]:
    findings: list[str] = []
    required_paths = {
        str(value)
        for value in submission_contract.get("required_files") or []
        if str(value)
    }
    mode_bindings: dict[str, dict[str, Any]] = {}
    for key in ("mode_submission_bindings", "submission_bindings_by_mode"):
        candidate = profile.get(key)
        if isinstance(candidate, dict):
            mode_bindings.update(
                {
                    mode: value
                    for raw_mode, value in candidate.items()
                    if (mode := MODE_ALIASES.get(str(raw_mode).casefold()))
                    and isinstance(value, dict)
                }
            )
            break
    shared = profile.get("submission_binding")
    if isinstance(shared, dict) and any(
        key in shared
        for key in (
            "autonomous_research",
            "paper_reproduction",
            "autonomous",
            "reproduction",
            "open_discovery",
            "guided_reproduction",
        )
    ):
        mode_bindings.update(
            {
                mode: value
                for raw_mode, value in shared.items()
                if (mode := MODE_ALIASES.get(str(raw_mode).casefold()))
                and isinstance(value, dict)
            }
        )
        shared = None

    if mode_bindings:
        scope = normalize_mode_scope(profile.get("applies_to_modes"))
        if scope is None:
            findings.append(f"acceptance_profile_mode_scope_invalid:{identifier}")
            scope = list(TASK_MODES)
        for mode in scope:
            binding = mode_bindings.get(mode)
            if not isinstance(binding, dict) or not binding:
                if required_binding_modes is None or mode in required_binding_modes:
                    findings.append(f"acceptance_submission_binding_missing:{identifier}:{mode}")
                continue
            # A mode matrix may legitimately point at a different required
            # artifact in the other public mode.  Validate path safety here;
            # Stage07's mode-aware gate checks the actual mode contract.
            findings.extend(
                _binding_shape_findings(
                    binding,
                    identifier=f"{identifier}:{mode}",
                    required_paths=None,
                )
            )
        return findings

    if not isinstance(shared, dict) or not shared:
        return [f"acceptance_submission_binding_missing:{identifier}"]
    findings.extend(
        _binding_shape_findings(
            shared,
            identifier=identifier,
            required_paths=required_paths,
        )
    )
    return findings


def _binding_shape_findings(
    binding: dict[str, Any],
    *,
    identifier: str,
    required_paths: set[str] | None,
) -> list[str]:
    findings: list[str] = []
    if _contains_scoring_placeholder(binding):
        findings.append(f"acceptance_submission_binding_placeholder:{identifier}")
    artifact_paths = binding.get("artifact_paths") or []
    if isinstance(artifact_paths, str):
        artifact_paths = [artifact_paths]
    if not artifact_paths:
        findings.append(f"acceptance_submission_artifacts_missing:{identifier}")
    for artifact_path in artifact_paths:
        try:
            normalized = validate_relative_path(str(artifact_path))
        except ValueError:
            findings.append(f"acceptance_submission_artifact_invalid:{identifier}")
            continue
        if required_paths is not None and normalized not in required_paths:
            findings.append(
                f"acceptance_submission_artifact_not_required:{identifier}:{normalized}"
            )
    observed_fields = binding.get("observed_fields") or []
    if isinstance(observed_fields, str):
        observed_fields = [observed_fields]
    if not observed_fields or not all(str(value).strip() for value in observed_fields):
        findings.append(f"acceptance_submission_fields_missing:{identifier}")
    if "canonical_projection" not in binding or binding.get("canonical_projection") is None:
        findings.append(f"acceptance_submission_projection_missing:{identifier}")
    if not str(binding.get("comparison") or "").strip():
        findings.append(f"acceptance_submission_comparison_missing:{identifier}")
    return findings


def _contains_scoring_placeholder(value: Any) -> bool:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True).casefold()
    return any(
        token in serialized
        for token in (
            "agent_required",
            "todo",
            "replace_me",
            "must be extracted",
            "extract from the si",
            "extract from si",
            "to be provided",
            "to be determined",
            "pending extraction",
            "not yet extracted",
            "fill in later",
        )
    )


def _input_asset_integrity_findings(path: Path, relative: str) -> list[str]:
    """Perform format-neutral checks for empty and obvious placeholder inputs.

    This intentionally does not attempt to interpret chemistry.  It only prevents a
    non-empty placeholder file or an all-null JSON payload from satisfying the
    public-input file-existence contract.
    """

    findings: list[str] = []
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return [f"input_asset_unreadable:{relative}:{type(exc).__name__}"]
    if not raw.strip():
        return [f"input_asset_empty:{relative}"]
    text = raw.decode("utf-8", errors="replace")
    normalized = text.casefold()
    placeholder_tokens = (
        "[smiles string for",
        "[table ",
        "must be extracted",
        "extract from the si",
        "to be provided",
        "tbd",
        "replace_me",
        "pending extraction",
    )
    if any(token in normalized for token in placeholder_tokens):
        findings.append(f"input_asset_placeholder:{relative}")
    if path.suffix.casefold() == ".json":
        try:
            value = json.loads(text)
        except (TypeError, ValueError, json.JSONDecodeError):
            return findings
        if not _contains_meaningful_input_value(value):
            findings.append(f"input_asset_all_null_or_empty:{relative}")
    return findings


def _contains_meaningful_input_value(value: Any) -> bool:
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if not normalized:
            return False
        return not any(
            token in normalized
            for token in (
                "must be extracted",
                "extract from the si",
                "to be provided",
                "tbd",
                "replace_me",
                "pending extraction",
            )
        )
    if isinstance(value, dict):
        return any(_contains_meaningful_input_value(item) for item in value.values())
    if isinstance(value, (list, tuple, set)):
        return any(_contains_meaningful_input_value(item) for item in value)
    return True


def _evaluation_task_info_findings(task_info: dict[str, Any]) -> list[str]:
    try:
        TaskInfo, _ = _evaluation_models()
        TaskInfo.model_validate(task_info)
    except Exception as exc:
        return [f"evaluation_task_info_invalid:{type(exc).__name__}:{str(exc)[:500]}"]
    return []


def _evaluation_ground_truth_findings(
    pair_root: Path, hidden: dict[str, Any]
) -> list[str]:
    try:
        _, GroundTruth = _evaluation_models()
        common = {
            "expected_tool_calls": [],
            "expected_result": hidden.get("expected_result") or {},
            "scientific_conclusion_rubric": hidden.get("scientific_conclusion_rubric") or [],
            "critical_failures": evaluation_critical_failures(hidden),
            "reference_evidence": evaluation_reference_evidence(hidden),
            "evidence_gate_policy": hidden.get("evidence_gate_policy") or {},
            "managed_computation_policy": hidden.get("managed_computation_policy") or {},
        }
        # Scoring policy belongs to the downstream evaluator.  Preserve an
        # explicitly supplied policy for backward-compatible packages, but do
        # not invent ``dual_axis_100`` (or any other scale) during synthesis.
        for key in ("evaluation_mode", "score_max", "dual_axis_scoring_policy"):
            if key in hidden:
                common[key] = hidden[key]
        for mode, profile in (
            ("autonomous_research", "autonomous_discovery"),
            ("paper_reproduction", "paper_reproduction"),
        ):
            GroundTruth.model_validate(
                {
                    **common,
                    "evaluation_profile": profile,
                    "scoring_rubric": read_json(pair_root / mode / "process_rubric.json"),
                }
            )
    except Exception as exc:
        return [f"evaluation_ground_truth_invalid:{type(exc).__name__}:{str(exc)[:500]}"]
    return []


def evaluation_critical_failures(hidden: dict[str, Any]) -> list[str]:
    """Project rich private failure records into the current evaluator schema."""

    output: list[str] = []
    for item in hidden.get("critical_failures") or []:
        if isinstance(item, str):
            value = item.strip()
        elif isinstance(item, dict):
            identifier = str(item.get("id") or item.get("failure_id") or "").strip()
            description = str(
                item.get("description") or item.get("statement") or item.get("rule") or ""
            ).strip()
            value = f"{identifier}: {description}" if identifier and description else (
                description or identifier
            )
        else:
            value = str(item).strip()
        if value:
            output.append(value)
    return output


def evaluation_reference_evidence(hidden: dict[str, Any]) -> dict[str, Any]:
    """Expose typed Ground Truth to the evaluator without moving it into public tasks."""

    existing = hidden.get("reference_evidence")
    if isinstance(existing, dict):
        output = dict(existing)
    elif existing in (None, "", [], {}):
        output = {}
    else:
        output = {"legacy_reference_evidence": existing}
    output["ground_truth_items"] = hidden.get("ground_truth_items") or []
    output["acceptance_profiles"] = hidden.get("acceptance_profiles") or []
    return output


def _evaluation_models():
    benchmark_root = Path(__file__).resolve().parents[4]
    if str(benchmark_root) not in sys.path:
        sys.path.insert(0, str(benchmark_root))
    from evaluation.schemas.task import GroundTruth, TaskInfo

    return TaskInfo, GroundTruth


def _leakage_findings(pair_root: Path, hidden: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    public_by_mode = {
        mode: _normalize_text(
            "\n".join(
                path.read_text(encoding="utf-8", errors="replace")
                for path in (pair_root / mode).rglob("*")
                if path.is_file()
                and path.suffix.casefold() in {".md", ".json", ".txt", ".csv", ".tsv"}
            )
        )
        for mode in ("autonomous_research", "paper_reproduction")
    }
    disclosure_path = pair_root / "hidden_reference" / "disclosure_contract.json"
    disclosure = read_json(disclosure_path) if disclosure_path.is_file() else {}
    allowed_public = _normalize_text(
        json.dumps(disclosure.get("autonomous_allowed") or {}, ensure_ascii=False)
    )
    allowed_reproduction = _normalize_text(
        json.dumps(
            disclosure.get("reproduction_additional_allowed") or {}, ensure_ascii=False
        )
    )
    for truth in hidden.get("ground_truth_items") or []:
        identifier = truth.get("ground_truth_id") or "unknown"
        canonical = truth.get("canonical_answer")
        for token in _sensitive_values(canonical):
            if not token or _sensitive_value_present(token, allowed_public):
                continue
            if _sensitive_value_present(token, public_by_mode["autonomous_research"]):
                findings.append(f"hidden_answer_leakage:autonomous_research:{identifier}")
                break
            if _sensitive_value_present(token, allowed_reproduction):
                continue
            if _sensitive_value_present(token, public_by_mode["paper_reproduction"]):
                findings.append(f"hidden_answer_leakage:paper_reproduction:{identifier}")
                break
        for proposition in truth.get("required_propositions") or []:
            text = proposition.get("statement") if isinstance(proposition, dict) else proposition
            normalized = _normalize_text(str(text or ""))
            if len(normalized) < 48:
                continue
            for mode, public_text in public_by_mode.items():
                if normalized in public_text:
                    findings.append(f"hidden_conclusion_leakage:{mode}:{identifier}")
                    break
    return findings


def _sensitive_values(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            output.extend(_sensitive_values(item))
    elif isinstance(value, list):
        for item in value:
            output.extend(_sensitive_values(item))
    elif isinstance(value, (int, float)):
        token = str(value)
        # Very short integers occur throughout chemical inputs and identifiers;
        # they are not distinctive enough for a deterministic leakage verdict.
        if isinstance(value, float) or len(token.lstrip("+-")) >= 3:
            output.append(token)
    elif isinstance(value, str):
        normalized = value.strip()
        if len(normalized) >= 20 or re.search(r"\d", normalized):
            output.append(normalized)
    return output


def _normalize_text(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9.+-]+", " ", value.casefold()).split())


def _sensitive_value_present(token: str, normalized_public: str) -> bool:
    normalized = _normalize_text(token)
    if not normalized:
        return False
    if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", normalized):
        return bool(
            re.search(
                rf"(?<![a-z0-9.]){re.escape(normalized)}(?![a-z0-9.])",
                normalized_public,
            )
        )
    return len(normalized) >= 20 and normalized in normalized_public


def _unknown_evidence(values: Any, evidence_ids: set[str], label: str) -> list[str]:
    if not isinstance(values, list) or not values:
        return [f"{label}_evidence_missing"]
    return [f"{label}_evidence_unknown:{value}" for value in values if value not in evidence_ids]

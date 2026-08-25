#!/usr/bin/env python3
"""Small, read-only Stage06/07 self-check tool.

The tool is intentionally self contained so an Agent can run it from an isolated
workspace without importing the pipeline.  It checks transport and public-surface
contracts only; scientific scope, answers, and paper importance remain Agent
responsibilities.  The orchestrator uses the same phase-specific validators for
the final check.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import stat
import sys
from pathlib import Path
from typing import Any

try:
    from src.stages.evaluator_reference import minimal_evaluator_findings as _shared_minimal_evaluator_findings
except ImportError:  # Installed next to this script in an isolated Agent workspace.
    try:
        from evaluator_reference import minimal_evaluator_findings as _shared_minimal_evaluator_findings
    except ImportError:
        _shared_minimal_evaluator_findings = None


MODES = ("paper_reproduction", "autonomous_research")
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
MODE_ALIASES = {
    "paper_reproduction": "paper_reproduction",
    "reproduction": "paper_reproduction",
    "guided_reproduction": "paper_reproduction",
    "autonomous_research": "autonomous_research",
    "autonomous": "autonomous_research",
    "open_discovery": "autonomous_research",
}
REPRODUCTION_FILES = (
    "task.md",
    "task_info.json",
    "task_spec.json",
    "submission_contract.json",
    "process_rubric.json",
    "paper_route.md",
    "workflow_spec.json",
    "route_evidence_map.json",
)
CORE_FILES = (
    "task.md",
    "task_info.json",
    "task_spec.json",
    "submission_contract.json",
    "process_rubric.json",
)

# Files that define the task package itself.  They are inputs to the evaluated
# Agent/evaluator protocol, not artifacts the evaluated Agent should be asked to
# submit.  Keep this list to exact root-relative paths: a benchmark may
# legitimately request a similarly named file below a report directory.
PACKAGE_INTERNAL_SUBMISSION_FILES = frozenset(
    {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
        "paper_route.md",
        "workflow_spec.json",
        "route_evidence_map.json",
        "public_manifest.json",
        "derived_from.json",
        "conversion_contract.json",
        "conversion_report.json",
    }
)

# These are framework/protocol markers, rather than molecule, paper, or answer
# keywords.  They catch accidental disclosure of the construction protocol in
# autonomous instructions without attempting to infer a scientific answer.
_PROTOCOL_MARKERS = (
    re.compile(r"conversion[_ -]?packet", re.I),
    re.compile(r"(?:phase[_ -]?gate|recovery_context|construction_contract)", re.I),
    re.compile(r"(?:paper_route\.md|workflow_spec\.json|route_evidence_map\.json)", re.I),
    re.compile(r"(?:task_info\.json|task_spec\.json|submission_contract\.json|process_rubric\.json)", re.I),
    re.compile(r"inputs/tools", re.I),
)

_V13_REFERENCE_DIR = "evaluator_reference"
_V13_PRIMARY_REFERENCE_FILES = (
    "reference_key_points.json",
    "reference_conclusions.json",
    "scoring_rules.json",
)
_V13_REFERENCE_MODES = frozenset({"paper_reproduction", "autonomous_research"})
_V15_RULE_TYPES = frozenset({"numeric", "ordering", "condition", "semantic"})
_PLACEHOLDER_STATEMENT_MARKERS = (
    "agent_required",
    "todo",
    "<placeholder>",
    "<fill",
    "reference scientific result ",
    "replace this scaffold",
    "replace the scaffold",
)
GATE_CHECKER_VERSION = "stage06-07-gate-v16"
PHASE_ALIASES = {
    "synthesis": "stage06a",
    "autonomous_conversion": "stage06b",
    "final_package": "stage07a",
}


def _has_evaluator_value(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _is_evaluator_placeholder(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip().casefold()
    return any(marker in text for marker in _PLACEHOLDER_STATEMENT_MARKERS)


def _numeric_evaluator_value(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _tolerance_evaluator_value(value: Any) -> bool:
    if _numeric_evaluator_value(value):
        return float(value) >= 0
    return isinstance(value, dict) and bool(value) and all(
        _numeric_evaluator_value(item) and float(item) >= 0 for item in value.values()
    )


def _is_blocking_finding(value: str) -> bool:
    """Classify v15 completeness findings; policy quality is outside scope."""

    # v15 requires a usable rule, so missing references, expected values and
    # bindings are blocking.  Only explicitly named quality diagnostics (if a
    # future caller emits them) remain non-blocking.
    return not str(value).startswith("scoring_rule_quality_")


def _is_identity_key(key: str) -> bool:
    """Return whether a JSON key is a paper/task identity field.

    Evaluator-local identifiers deliberately do not belong to this set.
    ``task_id`` remains a transport field for old TaskInfo consumers, but its
    value must equal ``paper_id``; it is not a second identity.
    """

    return key in {
        "paper_id",
        "task_id",
        "objective_id",
        "task_family_id",
        "original_task_pair_id",
        "final_task_pair_id",
    }


def _identity_findings(root: Path, findings: list[str]) -> None:
    """Check transport identity consistency without inspecting evaluator IDs."""

    values: list[tuple[str, str]] = []
    for path in root.rglob("*.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
        stack: list[tuple[Any, str]] = [(value, "")]
        while stack:
            current, location = stack.pop()
            if isinstance(current, dict):
                for key, item in current.items():
                    child = f"{location}.{key}" if location else str(key)
                    if key in {"paper_id", "task_id", "objective_id", "task_family_id"}:
                        text = str(item or "").strip()
                        if text:
                            values.append((child, text))
                    if isinstance(item, (dict, list)):
                        stack.append((item, child))
            elif isinstance(current, list):
                for index, item in enumerate(current):
                    if isinstance(item, (dict, list)):
                        stack.append((item, f"{location}[{index}]"))
    if not values:
        findings.append("paper_id_missing")
        return
    canonical = values[0][1]
    for location, value in values:
        if value != canonical:
            findings.append(f"paper_id_mismatch:{location}")
        # The shared TaskInfoV1 transport contract still has a
        # task_family_id field, but v14 requires it to carry the same value as
        # paper_id.  It is therefore not a second identity and must not block.
        if location.rsplit(".", 1)[-1] == "objective_id":
            findings.append(f"legacy_identity_field:{location}")
        if location.rsplit(".", 1)[-1] == "task_id" and value != canonical:
            findings.append(f"task_id_not_equal_paper_id:{location}")


def _v13_evaluator_reference_findings(root: Path, findings: list[str]) -> None:
    """Check split evaluator files through the shared v15 contract."""

    directory = root / _V13_REFERENCE_DIR
    if not directory.is_dir():
        return
    if _shared_minimal_evaluator_findings is not None:
        findings.extend(_shared_minimal_evaluator_findings(root))
        return
    # A conclusion may cite required submission artifacts (for example
    # ``report/results.json``) as the place where the evaluated Agent must
    # demonstrate the conclusion.  Those are not source-evidence IDs and are
    # validated against the mode submission contracts, not evidence_map.json.
    declared_submission_artifacts: set[str] = set()
    for mode in _V13_REFERENCE_MODES:
        contract_path = root / mode / "submission_contract.json"
        if contract_path.is_file():
            try:
                contract = json.loads(contract_path.read_text(encoding="utf-8"))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                contract = None
            if isinstance(contract, dict):
                declared_submission_artifacts.update(
                    str(item).strip()
                    for item in contract.get("required_files") or []
                    if isinstance(item, str) and item.strip()
                )
    parsed: dict[str, Any] = {}
    for filename in _V13_PRIMARY_REFERENCE_FILES:
        path = directory / filename
        if not path.is_file():
            findings.append(f"evaluator_reference_file_missing:{filename}")
            continue
        value = _json(path, findings)
        if not isinstance(value, dict):
            findings.append(f"evaluator_reference_not_object:{filename}")
            continue
        parsed[filename] = value
    for filename in ("evidence_map.json", "critical_failures.json"):
        path = directory / filename
        if not path.is_file():
            findings.append(f"evaluator_reference_file_missing:{filename}")
            continue
        value = _json(path, findings)
        if not isinstance(value, dict):
            findings.append(f"evaluator_reference_not_object:{filename}")
            continue
        parsed[filename] = value
    key_payload = parsed.get("reference_key_points.json") or {}
    conclusion_payload = parsed.get("reference_conclusions.json") or {}
    rules_payload = parsed.get("scoring_rules.json") or {}
    key_raw = key_payload.get("items") if isinstance(key_payload, dict) else None
    conclusion_raw = (
        conclusion_payload.get("items")
        if isinstance(conclusion_payload, dict)
        else None
    )
    rules_raw = rules_payload.get("rules") if isinstance(rules_payload, dict) else None
    if not isinstance(key_raw, list):
        findings.append("reference_key_points_items_invalid")
        key_raw = []
    if not isinstance(conclusion_raw, list):
        findings.append("reference_conclusions_items_invalid")
        conclusion_raw = []
    if not isinstance(rules_raw, list):
        findings.append("scoring_rule_items_invalid")
        rules_raw = []
    key_items = [
        row
        for row in key_raw
        if isinstance(row, dict)
    ]
    conclusion_items = [
        row
        for row in conclusion_raw
        if isinstance(row, dict)
    ]
    rules = [
        row
        for row in rules_raw
        if isinstance(row, dict)
    ]
    key_ids = {str(row.get("key_point_id") or "").strip() for row in key_items}
    key_ids.discard("")
    conclusion_ids = {
        str(row.get("conclusion_id") or "").strip() for row in conclusion_items
    }
    conclusion_ids.discard("")
    if not key_items:
        findings.append("reference_key_points_empty")
    if not conclusion_items:
        findings.append("reference_conclusions_empty")
    if not any(
        isinstance(row, dict)
        and str(row.get("claim_role") or "").strip().casefold() == "final"
        for row in conclusion_items
    ):
        findings.append("reference_final_conclusion_missing")
    if len(key_ids) != len(key_items):
        findings.append("reference_key_points_ids_invalid")
    if not any(
        str(row.get("claim_role") or "").strip().casefold() == "final"
        for row in conclusion_items
    ):
        findings.append("reference_final_conclusion_missing")

    evidence_payload: Any = parsed.get("evidence_map.json")
    referenced_evidence: list[tuple[str, str]] = []
    for row in key_items:
        identifier = str(row.get("key_point_id") or "").strip() or "missing"
        statement = str(row.get("statement") or "").strip()
        if not statement or _is_evaluator_placeholder(statement):
            findings.append(f"reference_key_point_statement_invalid:{identifier}")
        if not _has_evaluator_value(row.get("expected", row.get("reference_value"))):
            findings.append(f"reference_key_point_expected_missing:{identifier}")
        evidence = _strings(row.get("evidence_ids"))
        if not evidence:
            findings.append(f"reference_key_point_evidence_missing:{identifier}")
        referenced_evidence.extend((f"key_point:{identifier}", value) for value in evidence)
        scope = _strings(row.get("applies_to_modes"))
        if scope and any(value not in _V13_REFERENCE_MODES for value in scope):
            findings.append(f"reference_key_point_mode_scope_invalid:{identifier}")
    for row in conclusion_items:
        identifier = str(row.get("conclusion_id") or "").strip() or "missing"
        statement = str(row.get("statement") or "").strip()
        if not statement or _is_evaluator_placeholder(statement):
            findings.append(f"reference_conclusion_statement_invalid:{identifier}")
        if not _has_evaluator_value(row.get("expected", row.get("reference_value"))):
            findings.append(f"reference_conclusion_expected_missing:{identifier}")
        if not _strings(row.get("supporting_key_point_ids")):
            findings.append(f"reference_conclusion_key_points_missing:{identifier}")
        evidence = _strings(row.get("evidence_ids"))
        if not evidence:
            findings.append(f"reference_conclusion_evidence_missing:{identifier}")
        referenced_evidence.extend((f"conclusion:{identifier}", value) for value in evidence)
        for key_id in _strings(row.get("supporting_key_point_ids")):
            if key_id not in key_ids:
                findings.append(f"reference_conclusion_key_point_missing:{identifier}:{key_id}")
        scope = _strings(row.get("applies_to_modes"))
        if scope and any(value not in _V13_REFERENCE_MODES for value in scope):
            findings.append(f"reference_conclusion_mode_scope_invalid:{identifier}")
    if referenced_evidence:
        if not isinstance(evidence_payload, dict):
            findings.append("evidence_map_missing")
        else:
            evidence_rows = evidence_payload.get("evidence")
            if not isinstance(evidence_rows, list):
                findings.append("evidence_map_items_invalid")
            else:
                evidence_ids = {
                    str(row.get("evidence_id") or "").strip()
                    for row in evidence_rows
                    if isinstance(row, dict) and str(row.get("evidence_id") or "").strip()
                }
                # The pair-level evidence_index is the canonical immutable
                # source index.  An authored split map may be a compact subset
                # of that index; IDs that are present in the canonical index
                # are still valid source references.
                index_path = root / "evidence_index.json"
                if index_path.is_file():
                    try:
                        index_rows = json.loads(index_path.read_text(encoding="utf-8"))
                    except (OSError, ValueError, TypeError, json.JSONDecodeError):
                        index_rows = []
                    if isinstance(index_rows, list):
                        evidence_ids.update(
                            str(row.get("evidence_id") or "").strip()
                            for row in index_rows
                            if isinstance(row, dict) and str(row.get("evidence_id") or "").strip()
                        )
                for owner, evidence_id in referenced_evidence:
                    if (
                        owner.startswith("conclusion:")
                        and evidence_id in declared_submission_artifacts
                    ):
                        continue
                    if evidence_id not in evidence_ids:
                        findings.append(f"reference_evidence_missing:{owner}:{evidence_id}")
    seen_rules: set[str] = set()
    referenced_items: set[str] = set()
    for row in rules:
        rule_id = str(row.get("rule_id") or "").strip()
        reference_id = str(row.get("reference_id") or "").strip()
        if not rule_id or rule_id in seen_rules:
            findings.append(f"scoring_rule_id_invalid:{rule_id or 'missing'}")
        seen_rules.add(rule_id)
        if reference_id and reference_id not in key_ids and reference_id not in conclusion_ids:
            findings.append(
                f"scoring_rule_reference_missing:{rule_id or 'missing'}:{reference_id}"
            )
        if reference_id:
            referenced_items.add(reference_id)
        else:
            findings.append(f"scoring_rule_reference_blank:{rule_id or 'missing'}")
        evaluation_type = str(
            row.get("type") or row.get("evaluation_type") or ""
        ).strip().casefold()
        evaluation_type = {
            "numeric_tolerance": "numeric",
            "ranking": "ordering",
            "trend": "semantic",
            "semantic_propositions": "semantic",
            "mechanism_claim": "semantic",
        }.get(evaluation_type, evaluation_type)
        if evaluation_type not in _V15_RULE_TYPES:
            findings.append(f"scoring_rule_type_missing:{rule_id or 'missing'}")
        if evaluation_type == "numeric":
            if not _numeric_evaluator_value(row.get("target")):
                findings.append(f"scoring_rule_missing_target:{rule_id or 'missing'}")
            if not str(row.get("unit") or "").strip():
                findings.append(f"scoring_rule_missing_unit:{rule_id or 'missing'}")
            tolerance = row.get("tolerance")
            if tolerance is None:
                tolerance = row.get("numeric_tolerances")
            if tolerance is None:
                tolerance = row.get("absolute_tolerance")
            if not _tolerance_evaluator_value(tolerance):
                findings.append(
                    f"scoring_rule_missing_numeric_tolerance:{rule_id or 'missing'}"
                )
        elif not _has_evaluator_value(row.get("expected", row.get("target"))):
            findings.append(f"scoring_rule_expected_missing:{rule_id or 'missing'}")
        binding = row.get("binding") or row.get("submission_binding")
        if not isinstance(binding, dict) or not binding:
            findings.append(f"scoring_rule_binding_missing:{rule_id or 'missing'}")
        else:
            artifacts = _binding_artifacts(binding)
            fields = _binding_fields(binding)
            if not artifacts or not fields:
                findings.append(f"scoring_rule_binding_incomplete:{rule_id or 'missing'}")
            for artifact in artifacts:
                normalized = _safe_relative_path(artifact)
                if normalized is None:
                    findings.append(f"scoring_rule_binding_path_invalid:{rule_id or 'missing'}:{artifact}")
                elif declared_submission_artifacts and normalized not in declared_submission_artifacts:
                    findings.append(f"scoring_rule_binding_path_not_required:{rule_id or 'missing'}:{normalized}")
    for reference_id in sorted((key_ids | conclusion_ids) - referenced_items):
        findings.append(f"scoring_rule_missing_for_reference:{reference_id}")
    for row in rules:
        rule_id = str(row.get("rule_id") or "").strip() or "missing"
        reference_id = str(row.get("reference_id") or "").strip()
        if reference_id and reference_id not in key_ids and reference_id not in conclusion_ids:
            findings.append(f"scoring_rule_orphan:{rule_id}")


def _json(path: Path, findings: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        findings.append(f"json_unreadable:{path.name}:{type(exc).__name__}")
        return None


def _required_files(root: Path, names: tuple[str, ...], findings: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for name in names:
        path = root / name
        if not path.is_file():
            findings.append(f"required_file_missing:{path.relative_to(root.parent).as_posix()}")
            continue
        if path.suffix == ".json":
            value = _json(path, findings)
            if value is not None:
                parsed[name] = value
    task = root / "task.md"
    if task.is_file() and not task.read_text(encoding="utf-8", errors="replace").strip():
        findings.append(f"task_instruction_empty:{root.name}")
    return parsed


def _paths(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    result: set[str] = set()
    for item in value:
        if isinstance(item, str) and item.strip():
            result.add(item.strip().replace("\\", "/"))
        elif isinstance(item, dict):
            raw = item.get("path") or item.get("file")
            if isinstance(raw, str) and raw.strip():
                result.add(raw.strip().replace("\\", "/"))
    return result


def _conversion_renamed_paths(root: Path) -> dict[str, str]:
    """Read optional converter rename metadata for non-mutating path checks."""

    report_path = root / "conversion_report.json"
    if not report_path.is_file():
        return {}
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return {}
    mapping: dict[str, str] = {}
    for row in report.get("renamed_files") or [] if isinstance(report, dict) else []:
        old = new = ""
        if isinstance(row, (list, tuple)) and len(row) == 2:
            old, new = (str(item) for item in row)
        elif isinstance(row, str):
            # Compact prose receipts commonly use ``old -> new``.  Accept only
            # one explicit arrow so unrelated diagnostic prose can never be
            # interpreted as a path rewrite.
            parts = re.split(r"\s*(?:->|→)\s*", row.strip())
            if len(parts) == 2:
                old, new = parts
        elif isinstance(row, dict):
            # Agents have historically emitted both the compact pair form and
            # an explicit object form.  They carry the same transport fact; a
            # Gate must not treat the representation choice as a missing input.
            old = row.get("from") or row.get("old") or row.get("source") or row.get("source_path") or row.get("old_path") or ""
            new = row.get("to") or row.get("new") or row.get("destination") or row.get("public_path") or row.get("new_path") or ""
        old, new = (str(item).replace("\\", "/").strip() for item in (old, new))
        if old and new:
            mapping[old] = new
    return mapping


def _safe_relative_path(value: Any) -> str | None:
    text = str(value or "").strip().replace("\\", "/")
    if not text or text.startswith("/") or ".." in Path(text).parts:
        return None
    return text


def _strings(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _profile_type(profile: dict[str, Any]) -> str:
    raw = str(
        profile.get("type")
        or profile.get("acceptance_type")
        or profile.get("kind")
        or ""
    ).strip().casefold()
    return {
        "numeric": "numeric_tolerance",
        "number": "numeric_tolerance",
        "numerical_value": "numeric_tolerance",
        "numeric_value": "numeric_tolerance",
        "numeric_final_result": "numeric_tolerance",
        "numeric_intermediate_result": "numeric_tolerance",
        "semantic": "semantic_propositions",
        "text": "semantic_propositions",
        "textual_final_conclusion": "semantic_propositions",
        "textual_intermediate_conclusion": "semantic_propositions",
    }.get(raw, raw)


def _mode_scope(value: Any) -> list[str] | None:
    if value is None:
        return list(MODES)
    rows = value if isinstance(value, list) else [value]
    normalized = [MODE_ALIASES.get(str(item).strip().casefold()) for item in rows]
    if not normalized or any(item is None for item in normalized):
        return None
    return list(dict.fromkeys(str(item) for item in normalized))


def _binding_fields(binding: dict[str, Any]) -> list[str]:
    fields = _strings(
        binding.get("observed_fields")
        or binding.get("observed_field")
        or binding.get("fields")
        or binding.get("field")
        or binding.get("result_fields")
        or binding.get("result_field")
        or binding.get("json_paths")
        or binding.get("json_path")
    )
    if not fields:
        fields = _strings(binding.get("target_fields"))
    return fields


def _binding_artifacts(binding: dict[str, Any]) -> list[str]:
    raw = (
        binding.get("artifact_paths")
        or binding.get("artifact_path")
        or binding.get("artifacts")
        or binding.get("artifact")
    )
    rows = raw if isinstance(raw, list) else [raw]
    output: list[str] = []
    for row in rows:
        value = row.get("path") or row.get("file") if isinstance(row, dict) else row
        text = str(value or "").strip()
        if text and text not in output:
            output.append(text)
    return output


def _canonical_binding(binding: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    """Return the deterministic transport shape used for equality checks.

    This is intentionally smaller than an evaluator.  It projects aliases and
    a comparison that is already uniquely named by the typed profile, but it
    never invents an answer, tolerance, proposition, selector, or artifact.
    """

    output = {
        "artifact_paths": _binding_artifacts(binding),
        "observed_fields": _binding_fields(binding),
        "comparison": str(
            binding.get("comparison")
            or binding.get("comparison_type")
            or _profile_type(profile)
            or ""
        ).strip(),
        "document_binding": bool(
            binding.get("document_binding")
            or binding.get("document_target") is not None
            or any(field in {"document", "report", "text"} for field in _binding_fields(binding))
        ),
    }
    projection = binding.get("canonical_projection", binding.get("projection"))
    if projection is not None:
        output["canonical_projection"] = projection
    return output


def acceptance_profile_type_findings(
    profile: dict[str, Any], *, identifier: str | None = None
) -> list[str]:
    """Validate the evaluator-visible typed profile without judging science."""

    identifier = str(
        identifier
        or profile.get("acceptance_profile_id")
        or profile.get("profile_id")
        or "missing"
    )
    findings: list[str] = []
    kind = _profile_type(profile)
    parameters = profile.get("parameters")
    if not isinstance(parameters, dict):
        # ``acceptance_parameters`` is the serialized Ground Truth spelling;
        # ``parameters`` is the normalized evaluator spelling.  They are the
        # same contract namespace and must be checked identically.
        parameters = (
            profile.get("acceptance_parameters")
            if isinstance(profile.get("acceptance_parameters"), dict)
            else {}
        )
    if kind not in ACCEPTANCE_TYPES:
        findings.append(f"invalid_acceptance_profile:{identifier}")
    elif kind == "numeric_tolerance":
        target = profile.get("target")
        unit = profile.get("unit", parameters.get("unit"))
        vector = profile.get(
            "numeric_tolerances", parameters.get("numeric_tolerances")
        )
        vector_valid = isinstance(vector, dict) and bool(vector) and all(
            str(key).strip()
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(float(value))
            and float(value) >= 0
            for key, value in (vector.items() if isinstance(vector, dict) else [])
        )
        if target is None or not (str(unit or "").strip() or vector_valid):
            findings.append(f"numeric_acceptance_target_or_unit_missing:{identifier}")
        scalar_valid = False
        # ``tolerance`` is the legacy absolute-tolerance alias.  A few older
        # drafts retained a human-readable placeholder in that field while
        # also carrying the real numeric value in ``absolute_tolerance`` or
        # ``relative_tolerance``.  The explicit numeric namespace is
        # authoritative in that case; validating the stale alias as though it
        # were the active value creates a false Gate failure after a valid
        # profile has already been normalized.  If no explicit scalar exists,
        # retain the legacy alias and validate it normally.
        explicit_scalar_present = any(
            profile.get(key) is not None or parameters.get(key) is not None
            for key in ("absolute_tolerance", "relative_tolerance")
        )
        scalar_keys = (
            ("absolute_tolerance", "relative_tolerance")
            if explicit_scalar_present
            else ("tolerance",)
        )
        for key in scalar_keys:
            value = profile.get(key, parameters.get(key))
            if value is None:
                continue
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(float(value))
                or float(value) < 0
            ):
                findings.append(
                    f"numeric_acceptance_tolerance_invalid:{identifier}:{key}"
                )
            else:
                scalar_valid = True
        if not scalar_valid and not vector_valid:
            findings.append(f"numeric_acceptance_tolerance_missing:{identifier}")
    elif kind in {"semantic_propositions", "mechanism_claim"}:
        if not _strings(profile.get("required_propositions")):
            findings.append(f"semantic_acceptance_contract_missing:{identifier}")
    elif kind == "trend":
        if not _strings(profile.get("required_trends")):
            findings.append(f"trend_acceptance_contract_missing:{identifier}")
    elif kind == "ranking":
        if not (
            profile.get("target_order")
            or profile.get("required_pairwise_relations")
        ):
            findings.append(f"ranking_acceptance_contract_missing:{identifier}")
    elif kind == "categorical" and profile.get("target") is None:
        findings.append(f"categorical_acceptance_target_missing:{identifier}")
    elif kind in {"structure_identity", "geometry_metric"} and not (
        profile.get("target") or profile.get("metrics")
    ):
        findings.append(f"structure_acceptance_contract_missing:{identifier}")
    elif kind == "artifact_validation":
        if not _strings(profile.get("required_artifacts")):
            findings.append(f"artifact_acceptance_contract_missing:{identifier}")
    return findings


def _binding_requires_projection(
    binding: dict[str, Any], profile: dict[str, Any]
) -> bool:
    if binding.get("projection_required") is True:
        return True
    mapping = str(
        binding.get("mapping_type")
        or binding.get("mapping_kind")
        or binding.get("transformation")
        or ""
    ).strip().casefold()
    if mapping and mapping not in {"identity", "direct", "none"}:
        return True
    canonical = _canonical_binding(binding, profile)
    return bool(
        canonical.get("document_binding")
        and _profile_type(profile)
        not in {"semantic_propositions", "mechanism_claim", "artifact_validation"}
    )


def _binding_findings(
    binding: dict[str, Any],
    *,
    profile: dict[str, Any],
    identifier: str,
    required_paths: set[str],
) -> list[str]:
    findings: list[str] = []
    canonical = _canonical_binding(binding, profile)
    artifacts = canonical["artifact_paths"]
    fields = canonical["observed_fields"]
    if not artifacts:
        findings.append(f"acceptance_submission_artifacts_missing:{identifier}")
    for artifact in artifacts:
        normalized = _safe_relative_path(artifact)
        if normalized is None:
            findings.append(f"acceptance_submission_artifact_invalid:{identifier}")
        elif required_paths and normalized not in required_paths:
            findings.append(
                f"acceptance_submission_artifact_not_required:{identifier}:{normalized}"
            )
    if not fields:
        findings.append(f"acceptance_submission_fields_missing:{identifier}")
    if not canonical["comparison"]:
        findings.append(f"acceptance_submission_comparison_missing:{identifier}")
    if _binding_requires_projection(binding, profile) and canonical.get("canonical_projection") is None:
        findings.append(f"acceptance_submission_projection_missing:{identifier}")
    return findings


def _profile_binding_findings(
    profile: dict[str, Any],
    *,
    required_paths_by_mode: dict[str, set[str]],
    required_modes: set[str],
) -> list[str]:
    identifier = str(profile.get("acceptance_profile_id") or profile.get("profile_id") or "missing")
    findings = acceptance_profile_type_findings(profile, identifier=identifier)
    scope = _mode_scope(profile.get("applies_to_modes"))
    if scope is None:
        return [*findings, f"acceptance_profile_mode_scope_invalid:{identifier}"]
    applicable = set(scope) & required_modes
    matrices = [
        profile.get(key)
        for key in ("mode_submission_bindings", "submission_bindings_by_mode")
        if isinstance(profile.get(key), dict)
    ]
    matrix: dict[str, dict[str, Any]] = {}
    if matrices:
        for raw_mode, binding in matrices[0].items():
            mode = MODE_ALIASES.get(str(raw_mode).strip().casefold())
            if mode and isinstance(binding, dict):
                matrix[mode] = binding
    shared = profile.get("submission_binding")
    if isinstance(shared, dict) and any(
        MODE_ALIASES.get(str(key).strip().casefold()) for key in shared
    ) and not _binding_artifacts(shared):
        for raw_mode, binding in shared.items():
            mode = MODE_ALIASES.get(str(raw_mode).strip().casefold())
            if mode and isinstance(binding, dict):
                matrix[mode] = binding
        shared = None
    if matrix and isinstance(shared, dict):
        shared_canonical = _canonical_binding(shared, profile)
        complete_equivalent = applicable.issubset(matrix) and all(
            _canonical_binding(matrix[mode], profile) == shared_canonical
            for mode in applicable
        )
        if not complete_equivalent:
            findings.append(f"acceptance_submission_binding_ambiguous:{identifier}")
    if matrix:
        for mode in sorted(applicable):
            binding = matrix.get(mode)
            if not isinstance(binding, dict) or not binding:
                findings.append(f"acceptance_submission_binding_missing:{identifier}:{mode}")
                continue
            findings.extend(
                _binding_findings(
                    binding,
                    profile=profile,
                    identifier=f"{identifier}:{mode}",
                    required_paths=required_paths_by_mode.get(mode, set()),
                )
            )
        return findings
    if not isinstance(shared, dict) or not shared:
        findings.append(f"acceptance_submission_binding_missing:{identifier}")
        return findings
    for mode in sorted(applicable or required_modes):
        findings.extend(
            _binding_findings(
                shared,
                profile=profile,
                identifier=identifier,
                required_paths=required_paths_by_mode.get(mode, set()),
            )
        )
    return findings


def _hidden_contract_findings(
    hidden: dict[str, Any],
    *,
    required_paths_by_mode: dict[str, set[str]],
    required_modes: set[str],
) -> list[str]:
    findings: list[str] = []
    truths = hidden.get("ground_truth_items")
    profiles = hidden.get("acceptance_profiles")
    if not isinstance(truths, list) or not truths:
        findings.append("hidden_ground_truth_items_missing")
        truths = []
    if not isinstance(profiles, list) or not profiles:
        findings.append("acceptance_profiles_missing")
        profiles = []
    profile_rows = [row for row in profiles if isinstance(row, dict)]
    profile_ids = [
        str(row.get("acceptance_profile_id") or row.get("profile_id") or "")
        for row in profile_rows
    ]
    if any(not value for value in profile_ids) or len(profile_ids) != len(set(profile_ids)):
        findings.append("acceptance_profile_ids_invalid")
    owners: dict[str, list[str]] = {}
    for index, truth in enumerate(truths, start=1):
        if not isinstance(truth, dict):
            findings.append("hidden_ground_truth_item_not_object")
            continue
        truth_id = str(truth.get("ground_truth_id") or f"missing-{index}")
        profile_id = str(
            truth.get("acceptance_profile_id") or truth.get("acceptance_profile") or ""
        )
        if not profile_id:
            findings.append(f"ground_truth_profile_missing:{truth_id}")
        else:
            owners.setdefault(profile_id, []).append(truth_id)
    for profile_id in profile_ids:
        if profile_id and len(owners.get(profile_id, [])) != 1:
            findings.append(f"acceptance_profile_not_item_specific:{profile_id}")
    for profile_id, truth_ids in owners.items():
        if profile_id not in profile_ids:
            findings.extend(f"ground_truth_profile_missing:{truth_id}" for truth_id in truth_ids)
    for profile in profile_rows:
        findings.extend(
            _profile_binding_findings(
                profile,
                required_paths_by_mode=required_paths_by_mode,
                required_modes=required_modes,
            )
        )
    return findings


def _route_fidelity_findings(
    root: Path, parsed: dict[str, Any], findings: list[str]
) -> None:
    rubric = parsed.get("process_rubric.json")
    if isinstance(rubric, dict):
        wrappers = [rubric.get(key) for key in ("criteria", "items", "rubric", "key_points")]
        rubric = next((value for value in wrappers if isinstance(value, list)), rubric)
    if not isinstance(rubric, list):
        findings.append(f"process_rubric_not_array:{root.name}")
        return
    routes = [
        row
        for row in rubric
        if isinstance(row, dict)
        and str(row.get("criterion_type") or "").casefold() == "route_fidelity"
    ]
    if len(routes) != 1:
        findings.append("reproduction_route_fidelity_criterion_missing")
        return
    submission = parsed.get("submission_contract.json")
    required = _paths(submission.get("required_files")) if isinstance(submission, dict) else set()
    evidence = _strings(routes[0].get("evidence_artifacts"))
    if not evidence:
        findings.append("reproduction_route_fidelity_evidence_missing")
    for artifact in evidence:
        normalized = _safe_relative_path(artifact)
        if normalized is None:
            findings.append(f"reproduction_route_fidelity_evidence_invalid:{artifact}")
        elif normalized not in required:
            findings.append(f"reproduction_route_fidelity_evidence_not_required:{normalized}")


def _deliverable_findings(root: Path, parsed: dict[str, Any], findings: list[str]) -> None:
    info = parsed.get("task_info.json")
    submission = parsed.get("submission_contract.json")
    if not isinstance(info, dict) or not isinstance(submission, dict):
        return
    declared = _paths(info.get("required_deliverables"))
    required = _paths(submission.get("required_files"))
    if not required:
        findings.append(f"submission_required_files_missing:{root.name}")
    for path in sorted(required):
        normalized = path.removeprefix("./")
        if normalized in PACKAGE_INTERNAL_SUBMISSION_FILES:
            findings.append(
                f"submission_required_file_is_package_internal:{root.name}:{normalized}"
            )
    if declared != required:
        missing = sorted(declared - required)
        extra = sorted(required - declared)
        findings.append(
            "deliverables_submission_mismatch:"
            f"{root.name}:declared_missing={','.join(missing) or '-'}:"
            f"required_missing={','.join(extra) or '-'}"
        )


def _input_findings(root: Path, parsed: dict[str, Any], findings: list[str]) -> None:
    spec = parsed.get("task_spec.json")
    input_root = root / "data" / "inputs"
    if not input_root.is_dir():
        findings.append(f"input_directory_missing:{root.name}")
        return
    if not isinstance(spec, dict):
        return
    assets = spec.get("input_assets") or []
    if not isinstance(assets, list):
        findings.append(f"input_assets_not_array:{root.name}")
        return
    renamed_paths = _conversion_renamed_paths(root.parent)
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            findings.append(f"input_asset_not_object:{root.name}:{index}")
            continue
        raw = str(asset.get("path") or "").replace("\\", "/")
        if not raw or raw.startswith("/") or ".." in Path(raw).parts:
            findings.append(f"input_asset_path_invalid:{root.name}:{index}")
            continue
        for prefix in ("data/inputs/", "inputs/"):
            if raw.startswith(prefix):
                raw = raw[len(prefix) :]
                break
        if not (input_root / raw).is_file():
            renamed = renamed_paths.get(f"data/inputs/{raw}") or renamed_paths.get(raw)
            if renamed:
                renamed_relative = renamed.removeprefix("data/inputs/").removeprefix("inputs/")
                if (input_root / renamed_relative).is_file():
                    continue
            findings.append(f"input_asset_missing:{root.name}:{raw}")
        findings.extend(_declared_asset_format_findings(input_root / raw, root.name, raw))


def _declared_asset_format_findings(path: Path, mode_name: str, relative: str) -> list[str]:
    """Run small format readers for declared assets; never infer their chemistry."""

    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        return [f"input_asset_unreadable:{mode_name}:{relative}:{type(exc).__name__}"]
    if not text.strip():
        return [f"input_asset_empty:{mode_name}:{relative}"]
    suffix = path.suffix.casefold()
    if suffix == ".json":
        try:
            json.loads(text)
        except (ValueError, TypeError, json.JSONDecodeError):
            return [f"input_asset_json_invalid:{mode_name}:{relative}"]
    elif suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        try:
            rows = list(csv.reader(text.splitlines(), delimiter=delimiter, strict=True))
        except csv.Error:
            return [f"input_asset_table_invalid:{mode_name}:{relative}"]
        widths = {len(row) for row in rows if row}
        if not widths or len(widths) != 1:
            return [f"input_asset_table_invalid:{mode_name}:{relative}"]
    elif suffix == ".xyz":
        lines = text.splitlines()
        cursor = 0
        frames = 0
        while cursor < len(lines):
            if not lines[cursor].strip():
                cursor += 1
                continue
            try:
                atom_count = int(lines[cursor].strip())
            except ValueError:
                return [f"input_asset_xyz_header_invalid:{mode_name}:{relative}"]
            if atom_count <= 0 or cursor + atom_count + 2 > len(lines):
                return [f"input_asset_xyz_record_incomplete:{mode_name}:{relative}"]
            for row in lines[cursor + 2 : cursor + 2 + atom_count]:
                columns = row.split()
                if len(columns) < 4 or not re.fullmatch(r"(?:[A-Z][a-z]?|\d+)", columns[0]):
                    return [f"input_asset_xyz_atom_row_invalid:{mode_name}:{relative}"]
                try:
                    coordinates = [float(value) for value in columns[1:4]]
                except ValueError:
                    return [f"input_asset_xyz_coordinate_invalid:{mode_name}:{relative}"]
                if not all(math.isfinite(value) for value in coordinates):
                    return [f"input_asset_xyz_coordinate_invalid:{mode_name}:{relative}"]
            frames += 1
            cursor += atom_count + 2
        if not frames:
            return [f"input_asset_xyz_empty:{mode_name}:{relative}"]
    elif suffix in {".cif", ".vasp", ".poscar"} or path.name.casefold() in {"poscar", "contcar"}:
        if len([line for line in text.splitlines() if line.strip()]) < 2:
            return [f"input_asset_structure_too_short:{mode_name}:{relative}"]
    return []


_PUBLIC_PRIVATE_KEYS = frozenset(
    {
        "workflow_scope",
        "complexity_profile",
        "ground_truth_items",
        "canonical_answer",
        "acceptance_parameters",
        "acceptance_profiles",
        "scoring_rules",
        "reference_value",
        "public_to_private_asset_map",
    }
)


def _public_surface_findings(root: Path, findings: list[str]) -> None:
    """Reject private evaluator metadata and generated placeholders in public files."""

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in {".json", ".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            continue
        lowered = text.casefold()
        if any(marker in lowered for marker in _PLACEHOLDER_STATEMENT_MARKERS):
            findings.append(f"public_placeholder:{root.name}:{path.relative_to(root).as_posix()}")
        if path.suffix.casefold() != ".json":
            continue
        try:
            value = json.loads(text)
        except (ValueError, TypeError, json.JSONDecodeError):
            continue
        stack = [value]
        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                for key, nested in current.items():
                    if key in _PUBLIC_PRIVATE_KEYS:
                        findings.append(
                            f"public_private_field_present:{root.name}:{path.name}:{key}"
                        )
                    if isinstance(nested, (dict, list)):
                        stack.append(nested)
            elif isinstance(current, list):
                stack.extend(item for item in current if isinstance(item, (dict, list)))


def _mode_contract(root: Path, mode: str, findings: list[str]) -> dict[str, Any]:
    parsed = _required_files(root, REPRODUCTION_FILES if mode == "paper_reproduction" else CORE_FILES, findings)
    _deliverable_findings(root, parsed, findings)
    _input_findings(root, parsed, findings)
    _public_surface_findings(root, findings)
    info = parsed.get("task_info.json")
    spec = parsed.get("task_spec.json")
    expected_task_mode = "guided_reproduction" if mode == "paper_reproduction" else "open_discovery"
    mode_aliases = {
        "paper_reproduction": {"paper_reproduction", "reproduction", "guided_reproduction"},
        "autonomous_research": {"autonomous_research", "autonomous", "open_discovery"},
    }
    if isinstance(info, dict):
        if any(
            value not in (None, "") and str(value) not in mode_aliases[mode]
            for value in (info.get("mode"), info.get("scientific_mode"))
        ):
            findings.append(f"mode_contract_mismatch:{root.name}")
        if info.get("task_mode") not in (None, "", expected_task_mode, *mode_aliases[mode]):
            findings.append(f"task_mode_contract_mismatch:{root.name}")
        if not str(info.get("paper_id") or "").strip():
            findings.append(f"paper_id_missing:{root.name}")
        if info.get("task_id") not in (None, "", info.get("paper_id")):
            findings.append(f"task_id_not_equal_paper_id:{root.name}")
        if "objective_id" in info:
            findings.append(f"legacy_identity_field:{root.name}")
        if info.get("task_family_id") not in (None, "", info.get("paper_id")):
            findings.append(f"task_family_id_not_equal_paper_id:{root.name}")
    if isinstance(spec, dict):
        allowed = mode_aliases[mode]
        if any(
            value not in (None, "") and str(value) not in allowed
            for value in (spec.get("mode"), spec.get("scientific_mode"))
        ):
            findings.append(f"task_spec_mode_mismatch:{root.name}")
    rubric = parsed.get("process_rubric.json")
    if isinstance(rubric, dict):
        wrappers = [
            rubric.get(key) for key in ("criteria", "items", "rubric", "key_points")
        ]
        rubric = next((value for value in wrappers if isinstance(value, list)), rubric)
    if rubric is not None and not isinstance(rubric, list):
        findings.append(f"process_rubric_not_array:{root.name}")
    submission = parsed.get("submission_contract.json")
    if isinstance(submission, dict) and not isinstance(
        submission.get("results_schema", submission.get("result_schema")), dict
    ):
        findings.append(f"submission_results_schema_missing:{root.name}")
    if mode == "paper_reproduction":
        _route_fidelity_findings(root, parsed, findings)
    return parsed


def _stage06a(root: Path, findings: list[str]) -> None:
    receipt_path = root / "construction_receipt.json"
    receipt = _json(receipt_path, findings) if receipt_path.is_file() else None
    if not receipt_path.is_file():
        findings.append("construction_receipt_missing")
    if isinstance(receipt, dict) and receipt.get("decision") == "scientific_not_constructible":
        # A negative scientific receipt has no success-tree obligation. Keep
        # this failure-only scope small, but reject a partially emitted mode
        # tree so an Agent cannot hide a half-written task behind a rejection.
        for mode in MODES:
            mode_root = root / mode
            if mode_root.is_dir() and any(
                path.is_file() or path.is_symlink() for path in mode_root.rglob("*")
            ):
                findings.append(f"stage06a_negative_contains_mode_tree:{mode}")
        return
    reproduction = root / "paper_reproduction"
    parsed = _mode_contract(reproduction, "paper_reproduction", findings) if reproduction.is_dir() else {}
    if not reproduction.is_dir():
        findings.append("mode_directory_missing:paper_reproduction")
    review_path = root / "workflow_review.json"
    review = _json(review_path, findings) if review_path.is_file() else None
    if not review_path.is_file():
        findings.append("workflow_review_missing")
    elif isinstance(review, dict) and review.get("decision") != "candidate_ready":
        findings.append("workflow_review_not_candidate_ready")
    for name in ("workflow_completeness_check.json", "public_to_private_asset_map.json", "toolbox_requirements.json"):
        path = root / name
        if not path.is_file():
            findings.append(f"handoff_file_missing:{name}")
        else:
            _json(path, findings)
    split_reference = root / _V13_REFERENCE_DIR
    if split_reference.is_dir():
        # v13 makes the split reference files authoritative.  Keep the legacy
        # envelope optional for compatibility, and do not re-run its stricter
        # acceptance-profile policy checks here.
        _v13_evaluator_reference_findings(root, findings)
        evidence = split_reference / "evidence_map.json"
        if evidence.is_file():
            _json(evidence, findings)
    else:
        hidden = root / "hidden_reference" / "ground_truth_common.json"
        evidence = root / "hidden_reference" / "private_evidence_map.json"
        value = _json(hidden, findings) if hidden.is_file() else None
        if not hidden.is_file():
            findings.append("hidden_reference_missing")
        elif not isinstance(value, dict):
            findings.append("hidden_reference_not_object")
        elif value.get("status") != "ready":
            findings.append("hidden_reference_not_ready")
        elif not any(isinstance(item, dict) and item.get("claim_role") == "final" for item in value.get("ground_truth_items") or []):
            findings.append("final_claim_missing")
            findings.append("stage06a_final_claim_missing")
        if isinstance(value, dict) and not isinstance(value.get("acceptance_profiles"), list):
            findings.append("acceptance_profiles_missing")
        if isinstance(value, dict) and not isinstance(value.get("scientific_conclusion_rubric"), list):
            findings.append("conclusion_key_points_missing")
        if not evidence.is_file():
            findings.append("private_evidence_map_missing")
        else:
            _json(evidence, findings)
        if isinstance(value, dict):
            submission = parsed.get("submission_contract.json")
            required = _paths(submission.get("required_files")) if isinstance(submission, dict) else set()
            findings.extend(
                _hidden_contract_findings(
                    value,
                    required_paths_by_mode={"paper_reproduction": required},
                    required_modes={"paper_reproduction"},
                )
            )


def _autonomous_leaks(root: Path, findings: list[str]) -> None:
    task = root / "task.md"
    if task.is_file():
        text = task.read_text(encoding="utf-8", errors="replace")
        for marker in _PROTOCOL_MARKERS:
            if marker.search(text):
                findings.append(f"autonomous_protocol_marker:{marker.pattern}")
    for path in root.rglob("*"):
        if path.is_dir() and path.name in {"paper_reproduction", "conversion_packet", "hidden_reference", "source_materials", "stage06_candidate"}:
            findings.append(f"autonomous_forbidden_directory:{path.relative_to(root).as_posix()}")
        if path.is_file() and path.name in {"paper_route.md", "workflow_spec.json", "route_evidence_map.json"}:
            findings.append(f"autonomous_forbidden_route_file:{path.relative_to(root).as_posix()}")
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Internal IDs/protocol names in metadata are transport leakage; this
        # intentionally does not inspect numeric values or chemistry labels.
        if re.search(r"\bgt_[A-Za-z0-9_.-]+\b|canonical_answer|acceptance_profile_id", text):
            findings.append(f"autonomous_internal_scoring_marker:{path.relative_to(root).as_posix()}")


def _stage06b(root: Path, findings: list[str]) -> None:
    autonomous = root / "autonomous_research"
    if not autonomous.is_dir():
        findings.append("autonomous_directory_missing")
        return
    parsed = _mode_contract(autonomous, "autonomous_research", findings)
    _autonomous_leaks(autonomous, findings)
    del parsed


def _stage07a(root: Path, findings: list[str]) -> None:
    pair = root / "task_pair"
    if not pair.is_dir():
        findings.append("task_pair_missing")
        return
    parsed_by_mode: dict[str, dict[str, Any]] = {}
    for mode in MODES:
        mode_root = pair / mode
        if not mode_root.is_dir():
            findings.append(f"mode_directory_missing:{mode}")
            findings.append(f"stage07a_mode_missing:{mode}")
            continue
        parsed_by_mode[mode] = _mode_contract(mode_root, mode, findings)
    split_reference = pair / _V13_REFERENCE_DIR
    if split_reference.is_dir():
        # The split files carry the v13 scientific reference.  Their scoring
        # policy findings are warnings; public mode closure above remains
        # blocking.
        _v13_evaluator_reference_findings(pair, findings)
    else:
        hidden = pair / "hidden_reference" / "ground_truth_common.json"
        value = _json(hidden, findings) if hidden.is_file() else None
        if not hidden.is_file():
            findings.append("hidden_reference_missing")
            findings.append("stage07a_hidden_reference_missing")
        elif not isinstance(value, dict):
            findings.append("hidden_reference_not_object")
        elif value.get("status") != "ready":
            findings.append("hidden_reference_not_ready")
        elif not isinstance(value.get("ground_truth_items"), list) or not value.get("ground_truth_items"):
            findings.append("ground_truth_items_missing")
        if isinstance(value, dict):
            required_paths = {
                mode: _paths(parsed.get("submission_contract.json", {}).get("required_files"))
                if isinstance(parsed.get("submission_contract.json"), dict)
                else set()
                for mode, parsed in parsed_by_mode.items()
            }
            findings.extend(
                _hidden_contract_findings(
                    value,
                    required_paths_by_mode=required_paths,
                    required_modes=set(MODES),
                )
            )


def snapshot_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        return digest.hexdigest()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in {
            "agent_self_check_report.json",
            "external_phase_gate_report.json",
            "phase_gate_report.json",
        }:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def write_final_self_check_report(
    *,
    phase: str,
    outputs: Path,
    report_root: Path | None = None,
    pre_normalization: dict[str, Any] | None = None,
    findings: list[str] | None = None,
    normalization_findings: list[str] | None = None,
) -> dict[str, Any]:
    """Persist the self-check for the final public snapshot.

    Agents run the standalone checker before the orchestrator applies harmless
    path/ID canonicalization.  The final self-check must therefore be evaluated
    again after normalization and must retain the original report as evidence,
    rather than pretending both checks examined the same tree.
    """

    final = run(phase, outputs)
    if findings is not None:
        final["findings"] = sorted(set(str(item) for item in findings if str(item).strip()))
        final["blocking_findings"] = [
            item for item in final["findings"] if _is_blocking_finding(item)
        ]
        final["diagnostics"] = [
            item for item in final["findings"] if not _is_blocking_finding(item)
        ]
        final["status"] = (
            "passed"
            if not final["blocking_findings"]
            else "failed"
        )
    final["authority"] = "agent_self_check"
    final["snapshot_stage"] = "post_normalization"
    final["normalization_findings"] = sorted(
        set(str(item) for item in (normalization_findings or []) if str(item).strip())
    )
    final["pre_normalization"] = pre_normalization
    final["snapshot_parity"] = bool(
        isinstance(pre_normalization, dict)
        and pre_normalization.get("snapshot_sha256") == final.get("snapshot_sha256")
    )
    # A mock/legacy harness that never ran the Agent self-check must not gain a
    # fabricated self-check report.  In production ``pre_normalization`` is the
    # standalone tool's report and therefore triggers the merged final report.
    if isinstance(pre_normalization, dict):
        target_root = report_root or outputs.parent
        report_path = target_root / "agent_self_check_report.json"
        temporary = report_path.with_name(f".{report_path.name}.tmp")
        temporary.write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(report_path)
    return final


def run(phase: str, root: Path) -> dict[str, Any]:
    phase = PHASE_ALIASES.get(phase, phase)
    findings: list[str] = []
    if not root.is_dir():
        findings.append("root_missing")
    elif phase == "stage06a":
        receipt_path = root / "construction_receipt.json"
        negative = False
        if receipt_path.is_file():
            try:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                negative = isinstance(receipt, dict) and receipt.get("decision") == "scientific_not_constructible"
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                pass
        if not negative:
            _identity_findings(root, findings)
        _stage06a(root, findings)
    elif phase == "stage06b":
        _identity_findings(root, findings)
        _stage06b(root, findings)
    elif phase == "stage07a":
        _identity_findings(root, findings)
        _stage07a(root, findings)
    else:
        findings.append(f"unsupported_phase:{phase}")
    findings = sorted(set(findings))
    blocking_findings = [item for item in findings if _is_blocking_finding(item)]
    diagnostics = [item for item in findings if not _is_blocking_finding(item)]
    return {
        "schema_version": "stage06-07-phase-gate/v3",
        "authority": "shared_contract_core",
        "checker_version": GATE_CHECKER_VERSION,
        "status": (
            "passed"
            if not blocking_findings
            else "failed"
        ),
        "phase": phase,
        "findings": findings,
        "blocking_findings": blocking_findings,
        "diagnostics": diagnostics,
        "snapshot_sha256": snapshot_sha256(root),
    }


def install_phase_gate_tool(destination: Path) -> Path:
    """Install the CLI and its shared evaluator checker for Agent self-checks."""

    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "phase_gate.py"
    source = Path(__file__).resolve()
    if source != target:
        shutil.copyfile(source, target)
    evaluator_source = Path(__file__).with_name("evaluator_reference.py").resolve()
    evaluator_target = destination / "evaluator_reference.py"
    if evaluator_source != evaluator_target:
        shutil.copyfile(evaluator_source, evaluator_target)
    target.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    evaluator_target.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Stage06/07 phase self-check")
    parser.add_argument(
        "--phase",
        required=True,
        choices=("stage06a", "stage06b", "stage07a", *PHASE_ALIASES),
    )
    parser.add_argument("--root", default="outputs", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run(args.phase, args.root)
    except Exception as exc:  # tool errors are distinct from contract findings
        report = {"status": "tool_error", "phase": args.phase, "findings": [f"tool_error:{type(exc).__name__}:{exc}"]}
        print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
        return 2
    report["authority"] = "agent_self_check"
    report_path = args.root.resolve().parent / "agent_self_check_report.json"
    temporary = report_path.with_name(f".{report_path.name}.tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(report_path)
    print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Stage06/07 split evaluator-reference transport helpers.

The scientific reference and the scoring policy are deliberately stored as
separate files in v13.  The legacy ``ground_truth_common.json`` envelope is
still readable and can be materialized as a compatibility view for older
validators and Task Package v1 consumers.

This module does not decide scientific correctness or tolerance values.  It
only preserves authored fields, derives transport aliases, and reports missing
cross-file references.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

REFERENCE_DIRNAME = "evaluator_reference"
REFERENCE_KEY_POINTS = "reference_key_points.json"
REFERENCE_CONCLUSIONS = "reference_conclusions.json"
SCORING_RULES = "scoring_rules.json"
EVIDENCE_MAP = "evidence_map.json"
CRITICAL_FAILURES = "critical_failures.json"
REFERENCE_FILES = (
    REFERENCE_KEY_POINTS,
    REFERENCE_CONCLUSIONS,
    SCORING_RULES,
    EVIDENCE_MAP,
    CRITICAL_FAILURES,
)
REFERENCE_MODES = frozenset({"paper_reproduction", "autonomous_research"})


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def _strings(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _scope(value: Any) -> list[str]:
    return _strings(value)


def _truth_id(row: dict[str, Any], index: int) -> str:
    return str(
        row.get("ground_truth_id")
        or row.get("item_id")
        or row.get("answer_id")
        or f"kp_{index}"
    ).strip()


def _statement(row: dict[str, Any], identifier: str) -> str:
    value = row.get("statement") or row.get("description") or row.get("claim")
    if isinstance(value, str) and value.strip():
        return value.strip()
    canonical = row.get("canonical_answer")
    if isinstance(canonical, str) and canonical.strip():
        return canonical.strip()
    return f"Reference scientific result {identifier}."


MINIMAL_RULE_TYPES = frozenset({"numeric", "ordering", "condition", "semantic"})
_PLACEHOLDER_RE = re.compile(
    r"^(?:reference\s+scientific\s+result|report\s+(?:the|this)\s+result|check\s+whether|(?:gt|kp|claim)[_-][\w.-]+\s+evaluated\s+scientific\s+result)\b",
    re.IGNORECASE,
)


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _has_value(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _numeric_value(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _tolerance_value(value: Any) -> bool:
    if _numeric_value(value):
        return float(value) >= 0
    if isinstance(value, dict) and value:
        return all(_numeric_value(item) and float(item) >= 0 for item in value.values())
    return False


def _rule_type(rule: dict[str, Any]) -> str:
    value = rule.get("type") or rule.get("evaluation_type") or rule.get("acceptance_type")
    aliases = {
        "numeric_tolerance": "numeric",
        "number": "numeric",
        "ranking": "ordering",
        "trend": "semantic",
        "semantic_propositions": "semantic",
        "mechanism_claim": "semantic",
    }
    return aliases.get(str(value or "").strip().casefold(), str(value or "").strip().casefold())


def _rule_binding(rule: dict[str, Any]) -> Any:
    return rule.get("binding") or rule.get("submission_binding")


def _binding_values(binding: dict[str, Any]) -> tuple[list[str], list[str]]:
    artifacts = binding.get("artifact_paths") or binding.get("artifact_path") or binding.get("artifacts")
    fields = binding.get("fields") or binding.get("field") or binding.get("observed_fields")
    if isinstance(artifacts, str):
        artifacts = [artifacts]
    if isinstance(fields, str):
        fields = [fields]
    return _strings(artifacts), _strings(fields)


def _required_submission_paths(root: Path) -> set[str]:
    paths: set[str] = set()
    for mode in REFERENCE_MODES:
        path = root / mode / "submission_contract.json"
        if not path.is_file():
            continue
        try:
            contract = read_json_file(path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
        if isinstance(contract, dict):
            for value in contract.get("required_files") or []:
                if isinstance(value, str) and value.strip():
                    paths.add(value.replace("\\", "/").removeprefix("./"))
    return paths


def minimal_evaluator_findings(root: Path) -> list[str]:
    """Validate the v15 evaluator contract shared by self-check and Gate.

    This checks completeness and transport usability only.  It deliberately
    does not grade scientific answers or decide whether a tolerance is optimal.
    """

    directory = root / REFERENCE_DIRNAME
    if not directory.is_dir():
        return []
    findings: list[str] = []
    documents: dict[str, Any] = {}
    filenames = REFERENCE_FILES
    for filename in filenames:
        path = directory / filename
        if not path.is_file():
            findings.append(f"evaluator_reference_file_missing:{filename}")
            continue
        try:
            value = read_json_file(path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            findings.append(f"evaluator_reference_json_unreadable:{filename}:{type(exc).__name__}")
            continue
        if not isinstance(value, dict):
            findings.append(f"evaluator_reference_not_object:{filename}")
            continue
        documents[filename] = value

    key_items = documents.get(REFERENCE_KEY_POINTS, {}).get("items")
    conclusion_items = documents.get(REFERENCE_CONCLUSIONS, {}).get("items")
    rules = documents.get(SCORING_RULES, {}).get("rules")
    evidence_rows = documents.get(EVIDENCE_MAP, {}).get("evidence")
    if not isinstance(key_items, list):
        findings.append("reference_key_points_items_invalid")
        key_items = []
    if not isinstance(conclusion_items, list):
        findings.append("reference_conclusions_items_invalid")
        conclusion_items = []
    if not isinstance(rules, list):
        findings.append("scoring_rule_items_invalid")
        rules = []
    if not isinstance(evidence_rows, list):
        findings.append("evidence_map_items_invalid")
        evidence_rows = []
    if not isinstance(documents.get(CRITICAL_FAILURES, {}).get("items"), list):
        findings.append("critical_failures_items_invalid")

    key_ids = {str(row.get("key_point_id") or "").strip() for row in key_items if isinstance(row, dict)}
    conclusion_ids = {str(row.get("conclusion_id") or "").strip() for row in conclusion_items if isinstance(row, dict)}
    key_ids.discard("")
    conclusion_ids.discard("")
    if not key_items:
        findings.append("reference_key_points_empty")
    if not conclusion_items:
        findings.append("reference_conclusions_empty")
    if not any(
        isinstance(row, dict) and str(row.get("claim_role") or "").strip().casefold() == "final"
        for row in conclusion_items
    ):
        findings.append("reference_final_conclusion_missing")
    if len(key_ids) != len(key_items):
        findings.append("reference_key_points_ids_invalid")
    if len(conclusion_ids) != len(conclusion_items):
        findings.append("reference_conclusions_ids_invalid")

    evidence_ids = {
        str(row.get("evidence_id") or "").strip()
        for row in evidence_rows
        if isinstance(row, dict) and str(row.get("evidence_id") or "").strip()
    }
    index_path = root / "evidence_index.json"
    if index_path.is_file():
        try:
            index_rows = read_json_file(index_path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            index_rows = []
        if isinstance(index_rows, list):
            evidence_ids.update(
                str(row.get("evidence_id") or "").strip()
                for row in index_rows
                if isinstance(row, dict) and str(row.get("evidence_id") or "").strip()
            )
    required_paths = _required_submission_paths(root)
    for row in key_items:
        if not isinstance(row, dict):
            findings.append("reference_key_point_not_object")
            continue
        identifier = str(row.get("key_point_id") or "").strip() or "missing"
        if not _nonempty_text(row.get("statement")) or _PLACEHOLDER_RE.search(str(row.get("statement") or "")):
            findings.append(f"reference_key_point_statement_invalid:{identifier}")
        if not _has_value(row.get("expected", row.get("reference_value"))):
            findings.append(f"reference_key_point_expected_missing:{identifier}")
        if not _strings(row.get("evidence_ids")):
            findings.append(f"reference_key_point_evidence_missing:{identifier}")
        for evidence_id in _strings(row.get("evidence_ids")):
            if evidence_id not in evidence_ids:
                findings.append(f"reference_evidence_missing:key_point:{identifier}:{evidence_id}")
    for row in conclusion_items:
        if not isinstance(row, dict):
            findings.append("reference_conclusion_not_object")
            continue
        identifier = str(row.get("conclusion_id") or "").strip() or "missing"
        if not _nonempty_text(row.get("statement")) or _PLACEHOLDER_RE.search(str(row.get("statement") or "")):
            findings.append(f"reference_conclusion_statement_invalid:{identifier}")
        if not _has_value(row.get("expected", row.get("reference_value"))):
            findings.append(f"reference_conclusion_expected_missing:{identifier}")
        supports = _strings(row.get("supporting_key_point_ids"))
        if not supports:
            findings.append(f"reference_conclusion_key_points_missing:{identifier}")
        for key_id in supports:
            if key_id not in key_ids:
                findings.append(f"reference_conclusion_key_point_missing:{identifier}:{key_id}")
        if not _strings(row.get("evidence_ids")):
            findings.append(f"reference_conclusion_evidence_missing:{identifier}")
        for evidence_id in _strings(row.get("evidence_ids")):
            if evidence_id not in evidence_ids and evidence_id not in required_paths:
                findings.append(f"reference_evidence_missing:conclusion:{identifier}:{evidence_id}")

    seen_rules: set[str] = set()
    covered: set[str] = set()
    for row in rules:
        if not isinstance(row, dict):
            findings.append("scoring_rule_not_object")
            continue
        rule_id = str(row.get("rule_id") or "").strip() or "missing"
        reference_id = str(row.get("reference_id") or "").strip()
        if rule_id in seen_rules:
            findings.append(f"scoring_rule_id_invalid:{rule_id}")
        seen_rules.add(rule_id)
        if not reference_id:
            findings.append(f"scoring_rule_reference_blank:{rule_id}")
        elif reference_id not in key_ids and reference_id not in conclusion_ids:
            findings.append(f"scoring_rule_reference_missing:{rule_id}:{reference_id}")
        else:
            covered.add(reference_id)
        kind = _rule_type(row)
        if kind not in MINIMAL_RULE_TYPES:
            findings.append(f"scoring_rule_type_invalid:{rule_id}")
        if kind == "numeric":
            if not _numeric_value(row.get("target")):
                findings.append(f"scoring_rule_missing_target:{rule_id}")
            if not _nonempty_text(row.get("unit")):
                findings.append(f"scoring_rule_missing_unit:{rule_id}")
            tolerance = row.get("tolerance")
            if tolerance is None:
                tolerance = row.get("numeric_tolerances")
            if tolerance is None:
                tolerance = row.get("absolute_tolerance")
            if not _tolerance_value(tolerance):
                findings.append(f"scoring_rule_missing_numeric_tolerance:{rule_id}")
        elif not _has_value(row.get("expected", row.get("target"))):
            findings.append(f"scoring_rule_expected_missing:{rule_id}")
        if reference_id in key_ids or reference_id in conclusion_ids:
            reference_rows = key_items if reference_id in key_ids else conclusion_items
            reference = next(
                item for item in reference_rows
                if isinstance(item, dict) and str(item.get("key_point_id") or item.get("conclusion_id") or "").strip() == reference_id
            )
            reference_expected = reference.get("expected", reference.get("reference_value"))
            numeric_reference = _numeric_value(reference_expected) or (
                isinstance(reference_expected, dict)
                and bool(reference_expected)
                and all(_numeric_value(value) for value in reference_expected.values())
            )
            if numeric_reference and kind != "numeric":
                findings.append(f"scoring_rule_numeric_type_required:{rule_id}")
            if kind == "semantic" and isinstance(row.get("expected"), dict):
                if not _strings(row["expected"].get("required")) and not _strings(row["expected"].get("forbidden")):
                    findings.append(f"scoring_rule_semantic_expected_invalid:{rule_id}")
            if kind == "semantic" and _PLACEHOLDER_RE.search(str(row.get("expected") or "")):
                findings.append(f"scoring_rule_expected_placeholder:{rule_id}")
        binding = _rule_binding(row)
        if not isinstance(binding, dict) or not binding:
            findings.append(f"scoring_rule_binding_missing:{rule_id}")
            continue
        artifacts, fields = _binding_values(binding)
        if not artifacts or not fields:
            findings.append(f"scoring_rule_binding_incomplete:{rule_id}")
        for artifact in artifacts:
            normalized = artifact.replace("\\", "/").removeprefix("./")
            if normalized.startswith("/") or ".." in Path(normalized).parts:
                findings.append(f"scoring_rule_binding_path_invalid:{rule_id}:{artifact}")
            elif required_paths and normalized not in required_paths:
                findings.append(f"scoring_rule_binding_path_not_required:{rule_id}:{normalized}")
    for reference_id in sorted((key_ids | conclusion_ids) - covered):
        findings.append(f"scoring_rule_missing_for_reference:{reference_id}")
    return sorted(set(findings))


def split_legacy_reference(hidden: dict[str, Any]) -> dict[str, Any]:
    """Project a legacy hidden envelope into v13 split files.

    The projection is transport-only.  It does not invent tolerance values,
    score weights, or bindings.  Existing authored profile fields are copied
    into ``scoring_rules`` for later human editing.
    """

    hidden = hidden if isinstance(hidden, dict) else {}
    truths = [
        row for row in hidden.get("ground_truth_items") or [] if isinstance(row, dict)
    ]
    profiles = [
        row
        for row in (hidden.get("scoring_rules") or hidden.get("acceptance_profiles") or [])
        if isinstance(row, dict)
    ]
    profiles_by_id = {
        str(row.get("rule_id") or row.get("profile_id") or "").strip(): row
        for row in profiles
        if str(row.get("rule_id") or row.get("profile_id") or "").strip()
    }
    truth_by_id: dict[str, dict[str, Any]] = {}
    key_points: list[dict[str, Any]] = []
    for index, truth in enumerate(truths, start=1):
        identifier = _truth_id(truth, index)
        truth_by_id[identifier] = truth
        item: dict[str, Any] = {
            "key_point_id": identifier,
            "kind": str(
                truth.get("kind") or truth.get("type") or "scientific_result"
            ),
            "statement": _statement(truth, identifier),
            "claim_role": str(truth.get("claim_role") or "intermediate"),
            "evidence_ids": _strings(truth.get("evidence_ids")),
            "evidence_grade": str(truth.get("evidence_grade") or ""),
            "applies_to_modes": _scope(truth.get("applies_to_modes")),
        }
        if "canonical_answer" in truth:
            item["reference_value"] = _copy(truth.get("canonical_answer"))
            item["expected"] = _copy(truth.get("canonical_answer"))
        if truth.get("unit") is not None:
            item["unit"] = truth.get("unit")
        if truth.get("rule_id"):
            item["source_rule_id"] = str(
                truth.get("rule_id")
            )
        key_points.append(item)

    conclusions: list[dict[str, Any]] = []
    rubric = [
        row
        for row in hidden.get("scientific_conclusion_rubric") or []
        if isinstance(row, dict)
    ]
    covered: set[str] = set()
    for index, row in enumerate(rubric, start=1):
        refs = [
            value
            for value in _strings(row.get("ground_truth_ids") or row.get("answer_ids"))
            if value in truth_by_id
        ]
        if not refs:
            continue
        identifier = str(
            row.get("conclusion_id") or row.get("id") or f"fc_{index}"
        ).strip()
        conclusions.append(
            {
                "conclusion_id": identifier,
                "statement": row.get("statement") or row.get("claim") or identifier,
                "expected": _copy(row.get("expected", row.get("canonical_answer", row.get("claim")))) if row.get("expected", row.get("canonical_answer", row.get("claim"))) is not None else None,
                "claim_role": "final",
                "supporting_key_point_ids": refs,
                "evidence_ids": _strings(row.get("evidence_ids") or row.get("required_evidence")),
                "applies_to_modes": _scope(row.get("applies_to_modes")),
            }
        )
        covered.update(refs)
    for truth_id, truth in truth_by_id.items():
        if str(truth.get("claim_role") or "").casefold() != "final" or truth_id in covered:
            continue
        conclusions.append(
            {
                "conclusion_id": f"fc_{truth_id}",
                "statement": _statement(truth, truth_id),
                "expected": _copy(truth.get("canonical_answer")) if truth.get("canonical_answer") is not None else _statement(truth, truth_id),
                "claim_role": "final",
                "supporting_key_point_ids": [truth_id],
                "evidence_ids": _strings(truth.get("evidence_ids")),
                "applies_to_modes": _scope(truth.get("applies_to_modes")),
            }
        )

    rules: list[dict[str, Any]] = []
    truth_profile_ids = {
        identifier: str(
            truth.get("rule_id") or ""
        ).strip()
        for identifier, truth in truth_by_id.items()
    }
    for index, profile in enumerate(profiles, start=1):
        profile_id = str(
            profile.get("rule_id") or profile.get("profile_id") or f"rule_{index}"
        ).strip()
        reference_id = next(
            (truth_id for truth_id, owner in truth_profile_ids.items() if owner == profile_id),
            str(profile.get("answer_id") or profile.get("ground_truth_id") or "").strip(),
        )
        rule: dict[str, Any] = {
            "rule_id": profile_id,
            "reference_id": reference_id,
            "type": {
                "numeric_tolerance": "numeric",
                "ranking": "ordering",
                "trend": "semantic",
                "semantic_propositions": "semantic",
                "mechanism_claim": "semantic",
            }.get(str(profile.get("type") or profile.get("acceptance_type") or "").strip().casefold(), str(profile.get("type") or profile.get("acceptance_type") or "").strip().casefold()),
            "evaluation_type": str(
                profile.get("type") or profile.get("acceptance_type") or ""
            ),
        }
        for key in (
            "target",
            "unit",
            "comparison",
            "comparison_type",
            "numeric_tolerances",
            "tolerance",
            "absolute_tolerance",
            "relative_tolerance",
            "required_propositions",
            "forbidden_contradictions",
            "submission_binding",
            "mode_submission_bindings",
            "description",
        ):
            if key in profile:
                rule[key] = _copy(profile[key])
        parameters = profile.get("parameters") or profile.get("acceptance_parameters")
        if isinstance(parameters, dict):
            for key in (
                "target",
                "unit",
                "comparison",
                "numeric_tolerances",
                "tolerance",
                "absolute_tolerance",
                "relative_tolerance",
                "required_propositions",
                "forbidden_contradictions",
            ):
                if key not in rule and key in parameters:
                    rule[key] = _copy(parameters[key])
        if "absolute_tolerance" in rule and "tolerance" not in rule:
            rule["tolerance"] = _copy(rule["absolute_tolerance"])
        if "submission_binding" in rule and "binding" not in rule:
            rule["binding"] = _copy(rule["submission_binding"])
        if rule.get("type") == "semantic" and "expected" not in rule:
            rule["expected"] = _copy(rule.get("required_propositions") or rule.get("description") or "semantic result")
        rules.append(rule)

    evidence = hidden.get("reference_evidence")
    if not isinstance(evidence, dict):
        evidence = hidden.get("private_evidence_map")
    if not isinstance(evidence, dict):
        evidence = {"evidence": []}
    critical = hidden.get("critical_failures")
    if not isinstance(critical, list):
        critical = []
    return {
        "reference_key_points": {
            "schema_version": "reference-key-points/v1",
            "paper_id": hidden.get("paper_id"),
            "items": key_points,
        },
        "reference_conclusions": {
            "schema_version": "reference-conclusions/v1",
            "paper_id": hidden.get("paper_id"),
            "items": conclusions,
        },
        "scoring_rules": {
            "schema_version": "scoring-rules/v1",
            "paper_id": hidden.get("paper_id"),
            "rules": rules,
        },
        "evidence_map": _copy(evidence),
        "critical_failures": {
            "schema_version": "critical-failures/v1",
            "paper_id": hidden.get("paper_id"),
            "items": _copy(critical),
        },
    }


def legacy_reference_from_split(split: dict[str, Any]) -> dict[str, Any]:
    """Build a compatibility hidden envelope from split reference files."""

    key_doc = split.get("reference_key_points") or {}
    conclusion_doc = split.get("reference_conclusions") or {}
    rules_doc = split.get("scoring_rules") or {}
    key_items = [row for row in key_doc.get("items") or [] if isinstance(row, dict)]
    conclusion_items = [
        row for row in conclusion_doc.get("items") or [] if isinstance(row, dict)
    ]
    rules = [row for row in rules_doc.get("rules") or [] if isinstance(row, dict)]
    rules_by_reference = {
        str(row.get("reference_id") or "").strip(): row
        for row in rules
        if str(row.get("reference_id") or "").strip()
    }
    truths: list[dict[str, Any]] = []
    for row in key_items:
        identifier = str(row.get("key_point_id") or "").strip()
        if not identifier:
            continue
        rule = rules_by_reference.get(identifier) or {}
        truth: dict[str, Any] = {
            "ground_truth_id": identifier,
            "item_id": identifier,
            "kind": row.get("kind") or "scientific_result",
            "canonical_answer": _copy(row.get("reference_value")),
            "description": row.get("statement") or identifier,
            "evidence_ids": _strings(row.get("evidence_ids")),
            "evidence_grade": row.get("evidence_grade") or "",
            "claim_role": row.get("claim_role") or "intermediate",
            "rule_id": rule.get("rule_id") or f"rule_{identifier}",
            "applies_to_modes": _scope(row.get("applies_to_modes")),
        }
        if row.get("unit") is not None:
            truth["unit"] = row.get("unit")
        truths.append(truth)
    profiles: list[dict[str, Any]] = []
    for row in rules:
        rule_id = str(row.get("rule_id") or "").strip()
        if not rule_id:
            continue
        profile = {
            "rule_id": rule_id,
            "type": row.get("evaluation_type") or "",
            "description": row.get("description") or "",
        }
        for key in (
            "target",
            "unit",
            "comparison",
            "numeric_tolerances",
            "tolerance",
            "absolute_tolerance",
            "relative_tolerance",
            "required_propositions",
            "forbidden_contradictions",
            "submission_binding",
            "mode_submission_bindings",
        ):
            if key in row:
                profile[key] = _copy(row[key])
        profiles.append(profile)
    rubric = []
    for row in conclusion_items:
        rubric.append(
            {
                "id": row.get("conclusion_id"),
                "statement": row.get("statement"),
                "ground_truth_ids": _strings(row.get("supporting_key_point_ids")),
                "required_evidence": _strings(row.get("evidence_ids")),
            }
        )
    return {
        "status": "ready",
        "paper_id": key_doc.get("paper_id") or conclusion_doc.get("paper_id"),
        "ground_truth_items": truths,
        "acceptance_profiles": profiles,
        "scientific_conclusion_rubric": rubric,
        "critical_failures": (split.get("critical_failures") or {}).get("items") or [],
        "reference_evidence": _copy(split.get("evidence_map") or {}),
        "summary": "Compatibility view generated from v13 split evaluator reference files.",
    }


def read_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_split_reference(root: Path) -> dict[str, Any] | None:
    """Read split files when all primary files are present and parseable."""

    directory = root / REFERENCE_DIRNAME
    if not directory.is_dir():
        return None
    values: dict[str, Any] = {}
    mapping = {
        "reference_key_points": REFERENCE_KEY_POINTS,
        "reference_conclusions": REFERENCE_CONCLUSIONS,
        "scoring_rules": SCORING_RULES,
        "evidence_map": EVIDENCE_MAP,
        "critical_failures": CRITICAL_FAILURES,
    }
    primary = ("reference_key_points", "reference_conclusions", "scoring_rules")
    for key, filename in mapping.items():
        path = directory / filename
        if not path.is_file():
            if key in primary:
                return None
            continue
        value = read_json_file(path)
        if not isinstance(value, dict):
            return None
        values[key] = value
    values.setdefault("evidence_map", {"evidence": []})
    values.setdefault("critical_failures", {"items": []})
    return values


def materialize_split_reference(root: Path, hidden: dict[str, Any]) -> dict[str, Any]:
    """Write split reference files alongside the legacy envelope."""

    split = split_legacy_reference(hidden)
    directory = root / REFERENCE_DIRNAME
    directory.mkdir(parents=True, exist_ok=True)
    mapping = {
        "reference_key_points": REFERENCE_KEY_POINTS,
        "reference_conclusions": REFERENCE_CONCLUSIONS,
        "scoring_rules": SCORING_RULES,
        "evidence_map": EVIDENCE_MAP,
        "critical_failures": CRITICAL_FAILURES,
    }
    for key, filename in mapping.items():
        (directory / filename).write_text(
            json.dumps(split[key], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return split


def evaluator_reference_findings(root: Path) -> tuple[list[str], list[str]]:
    """Return v15 blocking findings and optional quality diagnostics."""

    if not (root / REFERENCE_DIRNAME).is_dir():
        return [], []
    return minimal_evaluator_findings(root), []
def is_blocking_finding(finding: str) -> bool:
    """Classify shared Gate findings without introducing a new business label."""

    return not str(finding).startswith("scoring_rule_quality_")

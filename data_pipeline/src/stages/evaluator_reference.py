"""Canonical split evaluator reference helpers for Stage06/07.

The five split files are the only evaluator contract.  This module validates
their structure and cross-file references without choosing scientific answers
or tolerance values.
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
_PLACEHOLDER_MARKERS = (
    "agent_required",
    "todo",
    "<placeholder>",
    "<fill",
    "reference scientific result ",
)


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_placeholder(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip().casefold()
    return any(marker in text for marker in _PLACEHOLDER_MARKERS)


def _has_value(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _expected_value(row: dict[str, Any]) -> Any:
    value = row.get("expected")
    return row.get("reference_value") if value is None else value


def _numeric_scalar(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _numeric_value(value: Any) -> bool:
    """Return whether value is a non-empty tree containing only finite numbers."""

    if _numeric_scalar(value):
        return True
    if isinstance(value, list) and value:
        return all(_numeric_value(item) for item in value)
    if isinstance(value, dict) and value:
        return all(str(key).strip() and _numeric_value(item) for key, item in value.items())
    return False


def _tolerance_value(value: Any) -> bool:
    if _numeric_scalar(value):
        return float(value) >= 0
    if isinstance(value, (list, dict)) and value:
        items = value if isinstance(value, list) else value.values()
        return all(_tolerance_value(item) for item in items)
    return False


def _numeric_shape(value: Any) -> Any:
    if _numeric_scalar(value):
        return "number"
    if isinstance(value, list):
        return ("list", tuple(_numeric_shape(item) for item in value))
    if isinstance(value, dict):
        return (
            "map",
            tuple((str(key), _numeric_shape(item)) for key, item in sorted(value.items())),
        )
    return None


def _numeric_values_equal(left: Any, right: Any) -> bool:
    if _numeric_scalar(left) and _numeric_scalar(right):
        return float(left) == float(right)
    if isinstance(left, list) and isinstance(right, list) and len(left) == len(right):
        return all(_numeric_values_equal(a, b) for a, b in zip(left, right))
    if isinstance(left, dict) and isinstance(right, dict) and left.keys() == right.keys():
        return all(_numeric_values_equal(left[key], right[key]) for key in left)
    return False


def _projection(rule: dict[str, Any], binding: Any) -> Any:
    sources = (rule, binding if isinstance(binding, dict) else {})
    for source in sources:
        for key in ("canonical_projection", "projection", "aggregation", "aggregate"):
            if _has_value(source.get(key)):
                return source[key]
    return None


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


def _submission_schemas(root: Path) -> dict[str, list[dict[str, Any]]]:
    schemas: dict[str, list[dict[str, Any]]] = {}
    for mode in REFERENCE_MODES:
        path = root / mode / "submission_contract.json"
        if not path.is_file():
            continue
        try:
            contract = read_json_file(path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
        if not isinstance(contract, dict):
            continue
        schema = contract.get("results_schema") or contract.get("result_schema")
        result_path = str(contract.get("submission_path") or "report/results.json")
        if isinstance(schema, dict):
            schemas.setdefault(result_path, []).append(schema)
    return schemas


def _selector_schema_known(schema: dict[str, Any], selector: str) -> bool | None:
    """Return False only when a declared closed JSON schema disproves a selector."""

    if selector == "document":
        return True
    if not selector.startswith("$"):
        return False
    tail = selector[1:]
    token_pattern = re.compile(
        r"\.([A-Za-z_][A-Za-z0-9_]*)|\[['\"]([^'\"]+)['\"]\]|\[(\d+)\]"
    )
    matches = list(token_pattern.finditer(tail))
    if "".join(match.group(0) for match in matches) != tail:
        return False
    keys = [left or right for left, right, index in (match.groups() for match in matches) if not index]
    if not keys:
        return None
    current: Any = schema
    for key in keys:
        if not isinstance(current, dict):
            return None
        properties = current.get("properties")
        if isinstance(properties, dict) and key in properties:
            current = properties[key]
            continue
        if current.get("additionalProperties") is False:
            return False
        return None
    return True


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
    submission_schemas = _submission_schemas(root)
    for row in key_items:
        if not isinstance(row, dict):
            findings.append("reference_key_point_not_object")
            continue
        identifier = str(row.get("key_point_id") or "").strip() or "missing"
        if not _nonempty_text(row.get("statement")) or _is_placeholder(row.get("statement")):
            findings.append(f"reference_key_point_statement_invalid:{identifier}")
        if not _has_value(_expected_value(row)):
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
        if not _nonempty_text(row.get("statement")) or _is_placeholder(row.get("statement")):
            findings.append(f"reference_conclusion_statement_invalid:{identifier}")
        if not _has_value(_expected_value(row)):
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

    references = {
        str(row.get("key_point_id") or "").strip(): row
        for row in key_items
        if isinstance(row, dict) and str(row.get("key_point_id") or "").strip()
    }
    references.update(
        {
            str(row.get("conclusion_id") or "").strip(): row
            for row in conclusion_items
            if isinstance(row, dict) and str(row.get("conclusion_id") or "").strip()
        }
    )
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
        binding = _rule_binding(row)
        projection = _projection(row, binding)
        reference_value = _expected_value(references.get(reference_id, {}))
        numeric_reference = _numeric_value(reference_value)
        if numeric_reference and kind != "numeric" and projection is None:
            findings.append(
                f"scoring_rule_numeric_reference_type_mismatch:{rule_id}:{kind or 'missing'}"
            )
        if kind == "numeric":
            if not _numeric_value(row.get("target")):
                findings.append(f"scoring_rule_missing_target:{rule_id}")
            if not _has_value(row.get("unit")):
                findings.append(f"scoring_rule_missing_unit:{rule_id}")
            tolerance = row.get("tolerance")
            if tolerance is None:
                tolerance = row.get("numeric_tolerances")
            if tolerance is None:
                tolerance = row.get("absolute_tolerance")
            if not _has_value(tolerance):
                findings.append(f"scoring_rule_missing_numeric_tolerance:{rule_id}")
            elif not _tolerance_value(tolerance):
                findings.append(f"scoring_rule_quality_tolerance_format:{rule_id}")
        elif not _has_value(row.get("expected") if row.get("expected") is not None else row.get("target")):
            findings.append(f"scoring_rule_expected_missing:{rule_id}")
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
        if fields and not all(field == "document" or field.startswith("$") for field in fields):
            findings.append(f"scoring_rule_binding_field_invalid:{rule_id}")
        for artifact in artifacts:
            normalized = artifact.replace("\\", "/").removeprefix("./")
            for schema in submission_schemas.get(normalized, []):
                for field in fields:
                    if _selector_schema_known(schema, field) is False:
                        findings.append(f"scoring_rule_binding_field_not_declared:{rule_id}:{field}")
        comparison = binding.get("comparison") or row.get("comparison")
        if not _nonempty_text(comparison):
            findings.append(f"scoring_rule_comparison_missing:{rule_id}")
        target = row.get("target")
        if kind == "numeric" and projection is None:
            if len(fields) > 1 and _numeric_scalar(target):
                findings.append(
                    f"scoring_rule_multifield_scalar_target_without_projection:{rule_id}"
                )
            if numeric_reference and _numeric_value(target):
                if _numeric_shape(target) != _numeric_shape(reference_value):
                    findings.append(
                        f"scoring_rule_target_reference_shape_mismatch:{rule_id}"
                    )
                elif not _numeric_values_equal(target, reference_value):
                    findings.append(
                        f"scoring_rule_target_reference_value_mismatch:{rule_id}"
                    )
    for reference_id in sorted((key_ids | conclusion_ids) - covered):
        findings.append(f"scoring_rule_missing_for_reference:{reference_id}")
    return sorted(set(findings))


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


def evaluator_reference_findings(root: Path) -> tuple[list[str], list[str]]:
    """Return v15 blocking findings and optional quality diagnostics."""

    if not (root / REFERENCE_DIRNAME).is_dir():
        return [], []
    findings = minimal_evaluator_findings(root)
    return (
        [finding for finding in findings if is_blocking_finding(finding)],
        [finding for finding in findings if not is_blocking_finding(finding)],
    )
def is_blocking_finding(finding: str) -> bool:
    """Classify shared Gate findings without introducing a new business label."""

    return not str(finding).startswith("scoring_rule_quality_")

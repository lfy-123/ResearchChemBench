"""Authored rule associations and deliberately conservative numerical checks."""
from __future__ import annotations

import math

from jsonpath_ng import parse


def associate_rules(reference):
    conclusions = reference["reference_conclusions.json"]["items"]
    points = {p["key_point_id"]: p for p in reference["reference_key_points.json"]["items"]}
    table = []
    for rule in reference["scoring_rules.json"]["rules"]:
        target = rule["reference_id"]
        direct = [c["conclusion_id"] for c in conclusions if c["conclusion_id"] == target]
        supporting = [c["conclusion_id"] for c in conclusions if target in c.get("supporting_key_point_ids", [])]
        table.append({"rule_id": rule["rule_id"], "rule": rule,
                      "conclusion_ids": list(dict.fromkeys(direct + supporting)),
                      "association": "direct" if direct else "supporting" if supporting else "standalone",
                      "key_point": points.get(target),
                      "diagnostic": None if direct or target in points else "unresolved_reference"})
    return table


def rule_table(truth):
    if truth.get("rule_table"):
        return truth["rule_table"]
    reference = truth.get("reference_evidence")
    if isinstance(reference, dict) and "scoring_rules.json" in reference:
        return associate_rules(reference)
    return []


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_rule(entry, documents):
    """Documents are keyed by authored artifact path, already read by the host.

    A unit declared for one bound scalar defines that field's unit; no conversion
    or identity inference is performed. This is not a scientific score.
    """
    rule = entry["rule"]
    result = {"rule_id": entry["rule_id"], "assessment": "requires_semantic_review",
              "reason": "authored_semantics", "sources": []}
    binding = rule.get("binding", {})
    paths, fields = binding.get("artifact_paths", []), binding.get("fields", [])
    if rule.get("type") != "numeric" or len(paths) != 1 or len(fields) != 1 or "*" in fields[0]:
        return result
    for owner in (rule, binding, entry.get("key_point") or {}):
        if any(owner.get(k) not in (None, "", {}) for k in ("applicability", "applies_when", "condition")):
            return {**result, "reason": "conditional_rule"}
    operation = binding.get("comparison")
    if operation not in {"absolute difference", "absolute_difference"}:
        return {**result, "reason": "unsupported_comparison"}
    # Only a literal, unqualified unit is suitable for this minimal checker.
    if rule.get("unit") not in {"kcal/mol", "kJ/mol", "hartree", "eV", "angstrom", "degree", "cm^-1", "Debye", "dimensionless"}:
        return {**result, "reason": "unit_requires_review"}
    target, tolerance = rule.get("target"), rule.get("tolerance")
    if not _number(target) or not _number(tolerance) or tolerance < 0:
        return {**result, "reason": "target_or_tolerance_requires_review"}
    path = paths[0]
    result["sources"] = [{"ref": "workspace/" + path, "selector": fields[0]}]
    if path not in documents:
        return {**result, "assessment": "missing_value", "reason": "document_not_submitted"}
    try:
        matches = parse(fields[0]).find(documents[path])
    except Exception as exc:
        return {**result, "reason": "unsupported_selector", "diagnostic": str(exc)}
    if not matches or (len(matches) == 1 and matches[0].value is None):
        return {**result, "assessment": "missing_value", "reason": "bound_value_not_submitted"}
    if len(matches) != 1 or not _number(matches[0].value):
        return {**result, "reason": "not_one_finite_scalar"}
    value = matches[0].value
    return {**result, "assessment": "pass" if abs(value - target) <= tolerance else "fail",
            "reason": "absolute_difference", "observed": value, "target": target,
            "tolerance": tolerance, "unit": rule["unit"], "difference": abs(value - target),
            "boundary": "Bound submitted scalar only; physical identity and computational support require review."}

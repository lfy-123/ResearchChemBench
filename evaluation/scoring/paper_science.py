"""Opt-in paper-result scoring: authored binary items, unchanged numeric tolerances."""
from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import hashlib
import json
import math

MODE = "paper_science_100"
POLICY_ID = "paper_science_v2"

SYSTEM_PROMPT = """You evaluate achievement of PAPER SCIENTIFIC RESULTS, policy paper_science_v2.
Only the versioned scientific_conclusion_rubric awards points. Each item is all-or-nothing.
Compare intermediate computed results and final conclusions with the item's explicit paper
target and cited source evidence. Matching a different, internally coherent result is not
achievement of the paper target. Uncertainty, effort, tool counts, good prose and failure
explanations do not earn points. Do not score the research process or invent partial credit.

For each item first establish molecular/step identity, physical quantity, charge/spin, units,
reference state and any task-required validation. Then verify genuine, relevant managed
calculation evidence. A copied target, nearby number, filename or successful unrelated job
is insufficient. Different valid software/methods are allowed unless the task requires them.
Do not identify structures by candidate names or by which energy is closest to the target.

Pass only when ALL requirements of that item and its linked rules are met. For numeric
rules copy the observed value from cited submitted evidence in the rule's unit, documenting
any conversion. The host compares it against the EXISTING target/tolerance; never replace,
fit, widen, or invent those values. This protocol uses absolute scalar tolerances.
For a final-conclusion item, the final deliverable must actually select/state the paper
conclusion with supporting evidence. Merely calculating that candidate is insufficient.
Use fail for a wrong, out-of-tolerance or scientifically unsupported result; missing for
an uncomputed/absent result. Both earn zero. Failures of one item do not erase other items.
An unfinished scientific question still receives an item-by-item score. Retrieve available
evidence before declaring it unavailable. For unsupported or disputed items award no credit
and explain the limitation; preserve independently supported items and the fixed weights.
Record input/reference concerns in objective_issue_flags with citations and affected item IDs.
For unresolved rule assessments include unresolved_disposition="scorable" and unresolved_rationale.

Return scientific_conclusions with exactly one entry per item, and rule_assessments for
every authored rule. Numeric_results must include every linked numeric rule for a passed
item; its observed value must have a source citation. Use actual task/rules citations for
the reference and workspace/job evidence for the submission. Do not return scores/weights.
No criterion-level partial or not_applicable disposition is permitted. Return one JSON:
{"scientific_conclusions":[{"id":"...","assessment":"pass|fail|missing",
"evidence_status":"supported|partially_supported|unsupported|contradicted",
"rationale":"explicit comparison with the paper target and evidence",
"citations":[{"ref":"..."}],
"numeric_results":[{"rule_id":"...","observed":0.0,"unit":"...",
"citations":[{"ref":"..."}]}]}],
"rule_assessments":[{"rule_id":"...","assessment":"pass|fail|partial|not_applicable|unresolved",
"rationale":"...","citations":[{"ref":"..."}]}],
"submission_validity":"valid|invalid_submission",
"objective_issue_flags":[],"critical_failures":[],"rationale":"..."}.
invalid_submission is reserved for fabricated evidence/hidden-answer leakage. Suspected
benchmark defects belong in objective_issue_flags, not a refusal to score the submission.
"""


def rubric_hash(document):
    return hashlib.sha256(json.dumps(document, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def numeric_comparison(observed, target, tolerance):
    difference = abs(Decimal(str(observed)) - Decimal(str(target)))
    return {"difference": float(difference), "matched": difference <= Decimal(str(tolerance))}


def apply_rubric(truth, document, *, paper_id, task_type, package_hash):
    """Overlay a private checklist without mutating task files or legacy contracts."""
    identity = {"policy_id": POLICY_ID, "paper_id": paper_id, "task_type": task_type,
                "task_package_content_sha256": package_hash}
    if not isinstance(document, dict) or set(document) != {*identity, "items"}:
        raise ValueError("V2 checklist requires policy_id, paper_id, task_type, task_package_content_sha256 and items")
    if any(document[k] != v for k, v in identity.items()):
        raise ValueError("V2 checklist does not match the selected task identity/version")
    return with_rubric(truth, document["items"])


def with_rubric(truth, items):
    """Build the same contract for a task-native rubric or an external checklist."""
    from ..contracts.scientific_rubric import scientific_rubric
    from ..schemas.task import GroundTruth

    if not isinstance(items, list) or not items:
        raise ValueError("V2 checklist items must be nonempty")
    reference = truth["reference_evidence"]
    rules = {r["rule_id"]: r for r in reference["scoring_rules.json"]["rules"]}
    evidence_ids = {e["evidence_id"] for e in reference["evidence_map.json"]["evidence"]}
    rubric = []
    for item in items:
        fields = {"id", "kind", "max_score", "expected", "rule_ids", "evidence_ids"}
        if not isinstance(item, dict) or set(item) != fields:
            raise ValueError("V2 item requires exactly id/kind/max_score/expected/rule_ids/evidence_ids")
        if item["kind"] not in {"intermediate", "conclusion"}:
            raise ValueError("V2 item kind must be intermediate or conclusion")
        sources = item["evidence_ids"]
        if (not isinstance(sources, list) or not sources or
                any(not isinstance(s, str) or s not in evidence_ids for s in sources) or
                len(sources) != len(set(sources))):
            raise ValueError("V2 item must cite existing, unique paper evidence IDs")
        rubric.append({"id": item["id"], "max_score": item["max_score"],
                       "description": item["expected"], "rule_ids": item["rule_ids"]})
    scientific_rubric({"rules": list(rules.values()), "scientific_rubric": rubric})
    if {i["kind"] for i in items} != {"intermediate", "conclusion"}:
        raise ValueError("V2 requires both intermediate result and final conclusion items")
    for rid in {r for item in items for r in item["rule_ids"]}:
        rule = rules[rid]
        if rule["type"] == "numeric" and (
                not _finite(rule.get("target")) or not _finite(rule.get("tolerance")) or
                rule["tolerance"] < 0 or not isinstance(rule.get("unit"), str) or not rule["unit"].strip()):
            raise ValueError(f"V2 needs an existing scalar target, unit and absolute tolerance: {rid}")
    result = deepcopy(truth)
    result.update(evaluation_mode=MODE, scoring_rubric=[], dual_axis_scoring_policy={},
                  scientific_conclusion_rubric=[{**item, "statement": item["expected"],
                      "acceptance_rule": {"rule_ids": item["rule_ids"]}} for item in items],
                  judge_instructions="Award only achieved paper-result items; host sums fixed weights. "
                      + reference["scoring_rules.json"].get("scientific_requirements", ""))
    return GroundTruth.model_validate(result).model_dump(mode="json")


def normalize_verdict(verdict, truth, checks=()):
    """Validate binary judgments and compute scores; never let the Judge set points."""
    forbidden = {"score", "scientific_conclusion_score", "research_process_score", "process_criteria", "criteria"}
    if forbidden.intersection(verdict):
        raise ValueError("V2 Judge returns assessments, not scores or process criteria")
    if verdict.get("submission_validity") not in {"valid", "invalid_submission", "not_scorable_objective"}:
        raise ValueError("Invalid submission_validity")
    items = verdict.get("scientific_conclusions")
    specs = truth["scientific_conclusion_rubric"]
    if not isinstance(items, list) or any(not isinstance(i, dict) or not isinstance(i.get("id"), str) for i in items):
        raise ValueError("V2 scientific_conclusions must contain item objects with IDs")
    by_id = {i["id"]: i for i in items}
    if len(by_id) != len(items) or set(by_id) != {s["id"] for s in specs}:
        raise ValueError("V2 verdict must contain every checklist item exactly once")
    rules = {r["rule_id"]: r["rule"] for r in truth["rule_table"]}
    assessments = verdict.get("rule_assessments")
    if not isinstance(assessments, list) or any(
            not isinstance(r, dict) or not isinstance(r.get("rule_id"), str) for r in assessments):
        raise ValueError("V2 rule_assessments must be objects with rule IDs")
    dispositions = {r["rule_id"]: r.get("assessment") for r in assessments}
    if len(dispositions) != len(assessments) or set(dispositions) != set(rules):
        raise ValueError("V2 verdict must assess every authored rule exactly once")
    checked = {r["rule_id"]: r["assessment"] for r in checks}
    normalized = []
    for spec in specs:
        item = by_id[spec["id"]]
        if "score" in item or "max_score" in item:
            raise ValueError("V2 item scores and weights are host-owned")
        if item.get("assessment") not in {"pass", "fail", "missing"}:
            raise ValueError("V2 item assessment must be pass, fail or missing")
        if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
            raise ValueError("V2 item comparison rationale is required")
        if item.get("evidence_status") not in {"supported", "partially_supported", "unsupported", "contradicted"}:
            raise ValueError("V2 item evidence_status is required")
        passed = item["assessment"] == "pass"
        if passed and (item["evidence_status"] != "supported" or any(
                dispositions.get(r) != "pass" or checked.get(r) in {"fail", "missing_value"}
                for r in spec["rule_ids"])):
            raise ValueError("V2 passed item requires supported evidence and all linked rules passing")
        numeric = {rid: rules[rid] for rid in spec["rule_ids"] if rules[rid]["type"] == "numeric"}
        readings = item.get("numeric_results", [])
        if not isinstance(readings, list):
            raise ValueError("V2 numeric_results must be a list")
        seen, comparisons = set(), []
        for row in readings:
            if not isinstance(row, dict) or not isinstance(row.get("rule_id"), str):
                raise ValueError("V2 numeric result requires a rule_id")
            rid = row["rule_id"]
            if rid not in numeric or rid in seen:
                raise ValueError("V2 numeric result rule must be linked and unique")
            seen.add(rid)
            rule = numeric[rid]
            if not _finite(row.get("observed")) or row.get("unit") != rule["unit"]:
                raise ValueError("V2 numeric result requires a finite value in the authored unit")
            comparison = numeric_comparison(row["observed"], rule["target"], rule["tolerance"])
            if passed and not comparison["matched"]:
                raise ValueError(f"V2 passed item is outside the existing tolerance: {rid}")
            comparisons.append({**row, "target": rule["target"], "tolerance": rule["tolerance"],
                                **comparison})
        if passed and seen != set(numeric):
            raise ValueError("V2 passed item must report every linked numeric result")
        normalized.append({**item, "kind": spec["kind"], "max_score": spec["max_score"],
                           "score": spec["max_score"] if passed else 0, "numeric_results": comparisons})
    total = float(sum((Decimal(str(i["score"])) for i in normalized), Decimal(0)))
    return {"score": total, "criteria": normalized}

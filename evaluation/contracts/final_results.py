"""V3 final-outcome rubric contract, independent of V1/V2 scoring semantics."""
from __future__ import annotations

from decimal import Decimal
import math

POLICY_ID = "paper_science_v3"
MODE = "final_results_100"
ITEM_FIELDS = {
    "id", "kind", "max_score", "description", "rule_ids", "evidence_ids",
    "allow_need_review", "review_triggers", "required_for_success",
}


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value, *, empty=False):
    return (isinstance(value, list) and (empty or bool(value))
            and all(nonblank(v) for v in value) and len(set(value)) == len(value))


def validate_rubric(document):
    """Each independently scored final outcome owns exactly one authored rule."""
    if document.get("scoring_policy") != POLICY_ID:
        raise ValueError("V3 scoring_policy must be paper_science_v3")
    rules = document.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("V3 requires nonempty rules")
    by_rule = {}
    for rule in rules:
        if not isinstance(rule, dict) or not nonblank(rule.get("rule_id")):
            raise ValueError("V3 rule requires a rule_id")
        if rule["rule_id"] in by_rule:
            raise ValueError("V3 duplicate rule_id")
        if rule.get("type") not in {"numeric", "semantic", "ordering", "condition"}:
            raise ValueError("V3 unknown rule type")
        if not nonblank(rule.get("expected")):
            raise ValueError("V3 rule requires an explicit final-outcome criterion")
        if rule["type"] == "numeric" and (
            not finite_number(rule.get("target")) or not finite_number(rule.get("tolerance"))
            or rule["tolerance"] < 0 or not nonblank(rule.get("unit"))
        ):
            raise ValueError("V3 numeric rule requires a finite target, nonnegative tolerance and unit")
        by_rule[rule["rule_id"]] = rule
    items = document.get("scientific_rubric")
    if not isinstance(items, list) or not items:
        raise ValueError("V3 requires a nonempty final-outcome rubric")
    ids, used, total = set(), set(), Decimal(0)
    for item in items:
        if not isinstance(item, dict) or set(item) != ITEM_FIELDS:
            raise ValueError("V3 rubric fields must be exactly " + "/".join(sorted(ITEM_FIELDS)))
        if not nonblank(item["id"]) or item["id"] in ids:
            raise ValueError("V3 outcome IDs must be nonempty and unique")
        if item["kind"] != "conclusion":
            raise ValueError("V3 scores final conclusions only")
        if not nonblank(item["description"]):
            raise ValueError("V3 outcome description is required")
        if not finite_number(item["max_score"]) or item["max_score"] <= 0:
            raise ValueError("V3 weights must be finite and positive")
        if not string_list(item["evidence_ids"]):
            raise ValueError("V3 requires unique source evidence_ids")
        links = item["rule_ids"]
        if not string_list(links) or len(links) != 1 or links[0] not in by_rule or links[0] in used:
            raise ValueError("V3 each final outcome must own exactly one distinct known rule")
        if type(item["allow_need_review"]) is not bool or type(item["required_for_success"]) is not bool:
            raise ValueError("V3 review/success flags must be booleans")
        triggers = item["review_triggers"]
        if not string_list(triggers, empty=not item["allow_need_review"]):
            raise ValueError("V3 reviewable outcomes require concrete unique review_triggers")
        if not item["allow_need_review"] and triggers:
            raise ValueError("V3 binary outcomes cannot have review triggers")
        if by_rule[links[0]]["type"] == "numeric" and item["allow_need_review"]:
            raise ValueError("V3 hard numeric windows are binary; need_review cannot bypass them")
        ids.add(item["id"])
        used.add(links[0])
        total += Decimal(str(item["max_score"]))
    if used != set(by_rule):
        raise ValueError("V3 contains unscored/orphan rules")
    if abs(total - Decimal(100)) > Decimal("1e-9"):
        raise ValueError("V3 final-outcome weights must sum to 100")
    if not any(i["required_for_success"] for i in items):
        raise ValueError("V3 requires at least one core outcome for whole-case success")
    return items

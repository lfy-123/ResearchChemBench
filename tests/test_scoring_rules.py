import copy
import json
from pathlib import Path

from evaluation.scoring.adapters import _runtime_contract
from evaluation.scoring.rules import associate_rules, check_rule


def test_all_current_final_contracts_preserve_every_authored_rule():
    packages = sorted(Path("tasks").glob("final_verified_*/*/evaluation/scoring_rules.json"))
    assert packages
    standalone = 0
    for path in packages:
        root = path.parent.parent
        reference = {p.name: json.loads(p.read_text()) for p in path.parent.glob("*.json")}
        submission = json.loads((root / "agent_input/submission_schema.json").read_text())
        mode = "paper_reproduction" if "paper_reproduction" in str(root) else "autonomous_research"
        truth = _runtime_contract(task_type=mode, reference=reference, submission=submission)
        table = truth["rule_table"]
        assert [r["rule"] for r in table] == reference["scoring_rules.json"]["rules"]
        standalone += sum(r["association"] == "standalone" for r in table)
        assert sum(r["max_score"] for r in truth["scientific_conclusion_rubric"]) == 100
        for conclusion in truth["scientific_conclusion_rubric"]:
            assert json.loads(conclusion["acceptance_rule"]) == [r["rule"] for r in table if conclusion["id"] in r["conclusion_ids"]]
    assert standalone > 0


def numeric(**changes):
    rule = {"rule_id": "n", "type": "numeric", "target": 2.0, "tolerance": 0.5,
            "unit": "kcal/mol", "binding": {"artifact_paths": ["report/result.json"],
            "fields": ["$.value"], "comparison": "absolute difference"}, **changes}
    return {"rule_id": "n", "rule": rule}


def test_scalar_checks_are_facts_not_scoring_or_identity_selection():
    entry = numeric()
    assert check_rule(entry, {"report/result.json": {"value": 2.5}})["assessment"] == "pass"
    assert check_rule(entry, {"report/result.json": {"value": -2}})["assessment"] == "fail"
    assert check_rule(entry, {"report/result.json": {"value": None}})["assessment"] == "missing_value"
    for value in (True, float("nan"), float("inf"), [2.0, 3.0]):
        assert check_rule(entry, {"report/result.json": {"value": value}})["assessment"] == "requires_semantic_review"
    for modified in (numeric(applies_when={"$.status": "completed"}), numeric(unit="V vs Fc/Fc+"), numeric(tolerance="expert")):
        assert check_rule(modified, {"report/result.json": {"value": 2}})["assessment"] == "requires_semantic_review"
    modified = copy.deepcopy(entry)
    modified["rule"]["binding"]["fields"] = ["$.values[*]"]
    assert check_rule(modified, {"report/result.json": {"values": [2, 3]}})["assessment"] == "requires_semantic_review"


def test_shared_and_standalone_rules_preserve_unknown_fields():
    reference = {"reference_conclusions.json": {"items": [
        {"conclusion_id": "a", "supporting_key_point_ids": ["p"]},
        {"conclusion_id": "b", "supporting_key_point_ids": ["p"]}]},
        "reference_key_points.json": {"items": [{"key_point_id": "p"}, {"key_point_id": "q"}]},
        "scoring_rules.json": {"rules": [{"rule_id": "r", "reference_id": "p", "future": 42},
                                        {"rule_id": "s", "reference_id": "q"}]}}
    table = associate_rules(reference)
    assert table[0]["conclusion_ids"] == ["a", "b"]
    assert table[0]["rule"]["future"] == 42
    assert table[1]["association"] == "standalone" and table[1]["diagnostic"] is None

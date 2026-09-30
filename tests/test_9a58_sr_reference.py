"""Regression checks for the approved benchmark-computed S2–S4 Sr references.

No quantum calculation is launched; these test package/scoring wiring only.
"""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from evaluation.contracts import validate_task_package
from evaluation.scoring.adapters import _runtime_contract
from evaluation.scoring.rules import associate_rules, check_rule

ROOT = Path(__file__).resolve().parents[1]
PAPER = "paper_9a58a1fa6ed7d780"


@pytest.fixture(params=[("autonomous_research", "ar"), ("paper_reproduction", "pr")])
def case(request):
    mode, prefix = request.param
    package = ROOT / "tasks" / f"final_verified_{mode}" / PAPER
    reference = {name: json.loads((package / "evaluation" / name).read_text()) for name in (
        "reference_key_points.json", "reference_conclusions.json", "scoring_rules.json",
        "evidence_map.json", "critical_failures.json")}
    schema = json.loads((package / "agent_input/submission_schema.json").read_text())
    return mode, prefix, package, reference, schema


def test_package_and_runtime(case):
    mode, prefix, package, reference, schema = case
    validation = validate_task_package(package)
    assert validation.status == "passed", validation.findings
    runtime = _runtime_contract(task_type=mode, reference=reference, submission=schema)
    rules = runtime["scientific_conclusion_rubric"][0]["acceptance_rule"]
    for suffix in (6, 7, 8):
        assert f"{prefix}_r{suffix}" in rules
    assert len(reference["reference_conclusions.json"]["items"]) == 1
    assert next(r for r in reference["scoring_rules.json"]["rules"]
                if r["rule_id"] == f"{prefix}_r5")["reference_id"] == f"{prefix}_final"


def test_computed_values_and_SI_disagreement(case):
    _, prefix, _, reference, _ = case
    source = ROOT / "docs/verification/group_1" / PAPER / "artifacts/hole_electron_fullcoeff_20260918/results.json"
    actual = json.loads(source.read_text())["states"]
    document = {"hole_electron": actual}
    for entry in associate_rules(reference):
        if entry["rule"]["reference_id"] != f"{prefix}_high_state_sr":
            continue
        assert check_rule(entry, {"report/results.json": document})["assessment"] == "pass"
        state = int(entry["rule_id"].split("_r")[1]) - 4
        assert entry["rule"]["target"] == actual[state - 1]["Sr"]
        wrong = json.loads(json.dumps(document))
        wrong["hole_electron"][state - 1]["Sr"] = {2: .795, 3: .919, 4: .913}[state]
        assert check_rule(entry, {"report/results.json": wrong})["assessment"] == "fail"
        missing = {"hole_electron": []}
        assert check_rule(entry, {"report/results.json": missing})["assessment"] == "missing_value"


def test_state_identity_schema(case):
    _, _, _, _, schema = case
    for defs in (schema["$defs"], schema["result_schema"]["$defs"]):
        for name, count in (("hole_electron", 4), ("states", 6)):
            validator = Draft202012Validator({"$defs": defs, "$ref": f"#/$defs/{name}"})
            rows = [dict(state=i, energy_ev=1., wavelength_nm=500., oscillator_strength=.1,
                         D_angstrom=0., Sr=.5, H_angstrom=3., t_angstrom=-3., HDI=5., EDI=5.)
                    for i in range(1, count + 1)]
            assert not list(validator.iter_errors(rows))
            rows[1]["state"] = 3
            assert list(validator.iter_errors(rows)), "Duplicate/mismatched root must be rejected"


def test_private_numbers_stay_private(case):
    _, _, package, _, _ = case
    for path in (package / "agent_input").rglob("*"):
        if path.is_file():
            text = path.read_text()
            for target in ("0.91366", "0.74133", "0.74956"):
                assert target not in text, path

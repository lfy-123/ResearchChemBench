"""Static contract regressions; these tests do not certify quantum convergence."""
from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MODES = ("autonomous_research", "paper_reproduction")


def package(mode: str, paper: str) -> Path:
    return ROOT / "tasks" / f"final_verified_{mode}" / paper


def read(path: Path):
    return json.loads(path.read_text())


@pytest.mark.parametrize("mode", MODES)
def test_12a_uses_the_identity_of_successful_verification(mode):
    p = package(mode, "paper_98b6f8a0352f72c2")
    identity = read(p / "agent_input/data/inputs/compound_12a.json")
    historical = read(ROOT / "docs/verification/group_6/paper_98b6f8a0352f72c2/report/results.json")
    assert identity["smiles"] == historical["system"]["connectivity"]
    assert identity["formula"] == historical["system"]["formula"] == "C24H19N3"
    assert "C21H18N2" not in json.dumps(identity)


@pytest.mark.parametrize("mode", MODES)
def test_51_balanced_endpoint_is_required_and_available(mode):
    # Held at the user's request; retain contract checks without re-enrolling it.
    p = ROOT / "tasks" / f"hold_verified_{mode}" / "paper_51a03695e1ccb105"
    assert not package(mode, "paper_51a03695e1ccb105").exists()
    schema = read(p / "agent_input/submission_schema.json")["result_schema"]["properties"]["states"]
    states = read(ROOT / "docs/verification/group_3/paper_51a03695e1ccb105/report/results.json")["states"]
    assert "coproduct" in schema["required"]
    assert states["product"]["charge"] == 0
    assert states["coproduct"]["charge"] == -1
    # Test the new endpoint requirement, not an invented autonomous narrative.
    Draft202012Validator(schema["properties"]["coproduct"]).validate(states["coproduct"])
    assert list(Draft202012Validator(schema).iter_errors({k: v for k, v in states.items() if k != "coproduct"}))
    assert "$.states.coproduct" in json.dumps(read(p / "evaluation/scoring_rules.json"))


@pytest.mark.parametrize("mode,prefix", zip(MODES, ("ar", "pr")))
def test_9d_identity_specific_energies_and_three_member_normalization(mode, prefix):
    p = package(mode, "paper_9d091f4337662e78")
    rules = read(p / "evaluation/scoring_rules.json")["rules"]
    energies = [r for r in rules if r["rule_id"].startswith(prefix + "_r3_energy")]
    assert sorted(r["target"] for r in energies) == [0.0, 0.680486100, 0.771969325]
    assert all(r["tolerance"] == 0.5 for r in energies)
    for r in energies:
        assert "$.conformers[*].id" in r["binding"]["fields"]
    population = next(r for r in rules if r["rule_id"] == prefix + "_r3_population")
    assert "16-conformer" in population["expected"]
    assert "5 percentage points" not in population["expected"]
    historical = read(ROOT / "docs/verification/group_3/paper_9d091f4337662e78/report/results.json")
    # This is arithmetic replay of existing observations, not chemistry recomputation.
    values = historical["conformers"]
    weights = [math.exp(-r["relative_gibbs_kcal_mol"] / (0.00198720425864083 * 298.15)) for r in values]
    for r, w in zip(values, weights):
        assert 100 * w / sum(weights) == pytest.approx(r["population_percent"], abs=1e-4)
    assert sum(r["population_percent"] for r in values) == pytest.approx(100)


@pytest.mark.parametrize("mode", MODES)
def test_fda_cis_six_bonds_are_public_and_bound_to_the_metric(mode):
    p = package(mode, "paper_fda8b9b53f8276db")
    definition = read(p / "agent_input/data/inputs/ccdc_record.json")
    # The approved final task now uses the published cis/six-pair definition.
    # Keep this contract check independent of untracked calculation archives.
    experimental = read(p / "agent_input/data/inputs/experimental_bonds.json")["bonds"]
    pairs = {frozenset(v) for v in definition["comparison_bonds"]}
    assert len(pairs) == 6
    assert pairs == {frozenset(r["atoms"]) for r in experimental}
    assert "cis local-minimum" in definition["target_conformer"]
    task = (p / "agent_input/task.md").read_text()
    assert all("-".join(v) in task for v in definition["comparison_bonds"])
    r = next(r for r in read(p / "evaluation/scoring_rules.json")["rules"] if r["type"] == "numeric")
    assert r["target"] == 0.004 and r["tolerance"] == 0.01
    assert "$.bond_comparison" in r["binding"]["fields"]
    selected = "selected_result" if mode == "autonomous_research" else "optimization"
    assert f"$.{selected}.conformer" in r["binding"]["fields"]
    schema = read(p / "agent_input/submission_schema.json")["result_schema"]
    assert "conformer" in schema["properties"][selected]["required"]


@pytest.mark.parametrize("mode", MODES)
def test_430_complete_result_can_include_both_shifts_and_diagnostics(mode):
    p = package(mode, "paper_430b9cbe83c2c203")
    validator = Draft202012Validator(read(p / "agent_input/submission_schema.json")["result_schema"])
    historical = read(ROOT / "docs/verification/group_4/paper_430b9cbe83c2c203/report/results.json")
    validator.validate(historical)
    missing_shifts = deepcopy(historical)
    del missing_shifts["conformers"][0]["shifts_ppm"]
    assert list(validator.iter_errors(missing_shifts))


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("paper", ("paper_430b9cbe83c2c203", "paper_9d091f4337662e78"))
def test_replacement_structures_have_graph_based_preparation_not_a_quantum_result(mode, paper):
    p = package(mode, paper)
    definition = read(p / "agent_input/data/inputs/starting_geometry_definition.json")
    preparation = read(p / "evaluation/task_provenance/independent_starter_preparation.json")
    for key in ("source_coordinate_template", "energy_ranking", "quantum_calculation", "force_field_minimization"):
        assert preparation[key] is False
    for name in definition["conformers"]:
        lines = (p / "agent_input/data/inputs" / name).read_text().splitlines()
        assert int(lines[0]) == definition["atom_count"] == len(lines) - 2
        assert "unoptimized" in lines[1] and "SI Table" not in lines[1]
        assert preparation["structures"][name]["validation"]["formula"] == definition["formula"]
    reference = (p / "evaluation/verified_computation_reference.md").read_text()
    assert "no calculation from those new starters was performed" in reference


@pytest.mark.parametrize("mode", MODES)
def test_e2d_transition_state_boundary_is_consistent(mode):
    p = package(mode, "paper_e2d9397dff2a3f0f")
    task = (p / "agent_input/task.md").read_text()
    assert "no TS coordinate is public" in task
    assert "independently generated TS" in task
    assert "do not copy an author/SI TS coordinate" in task
    assert "target.xyz" not in task
    assert (p / "evaluation/author_results/target_author_ts.xyz").is_file()
    reference = (p / "agent_input/data/inputs/reference.xyz").read_text()
    assert "SI coordinate table" not in reference
    assert "reference-side starter" in reference


@pytest.mark.parametrize("mode", MODES)
def test_fcc_schema_keeps_frequency_values_at_the_correct_schema_level(mode):
    p = package(mode, "paper_fcc3c7f2c46a0fbe")
    schema = read(p / "agent_input/submission_schema.json")
    result = schema["result_schema"]
    frequencies = result["properties"]["frequency_validation"]["properties"]["frequencies_cm-1"]
    assert frequencies["items"] == {"type": "number"}
    assert "oneOf" in result
    assert "oneOf" not in frequencies

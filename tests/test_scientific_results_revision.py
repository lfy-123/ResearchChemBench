"""Offline contract regressions; synthetic fixtures are not chemistry validation."""
from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path

import pytest
from jsonpath_ng import parse
from jsonschema import validators

from evaluation.contracts import validate_task_package
from evaluation.repository import (
    DuplicateTaskError, InvalidTaskPackageError, TaskRepository, materialize_agent_files,
)
from evaluation.scoring.adapters import EvaluatorReferenceInvalid, _runtime_contract, load_runtime_evaluation
from evaluation.scoring.dual_axis import RESULTS_POLICY_ID, dual_axis_policy, process_rubric
from evaluation.scoring.policies import validate_judge_verdict
from evaluation.scoring.rules import check_rule
from evaluation.scoring.service import _aggregate, _system_prompt
from evaluation.scoring.judging import ScoringBudget
from test_task_package_v19 import package, refresh_manifest

ROOT = Path(__file__).resolve().parents[1]
MODES = ("autonomous_research", "paper_reproduction")
PACKAGES = sorted((ROOT / "tasks").glob("final_verified_*/*/agent_input/task.md"))
PACKAGES = [p.parent.parent for p in PACKAGES] + [
    ROOT / "tasks" / f"hold_verified_{mode}" / "paper_4fa592965be9841e" for mode in MODES
]
COMMENTARY = ("limitation", "caveat", "disclaimer")


def read(path):
    return json.loads(path.read_text())


def schema(paper, mode, *, stage="final"):
    s = read(ROOT / "tasks" / f"{stage}_verified_{mode}" / paper / "agent_input/submission_schema.json")
    return s.get("result_schema", s)


def dictionaries(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from dictionaries(item)
    elif isinstance(value, list):
        for item in value:
            yield from dictionaries(item)


@pytest.mark.parametrize("root", PACKAGES, ids=lambda p: p.parent.name + "/" + p.name)
def test_numeric_targets_and_tolerances_preserved_except_approved_sign_corrections(root):
    original = root.relative_to(ROOT).as_posix().replace("hold_verified_", "final_verified_")
    before = json.loads(subprocess.check_output([
        "git", "show", "46bef5e99489643fa994211b5bbcf2cc508822bd:" + original + "/evaluation/scoring_rules.json"
    ], cwd=ROOT))
    after = read(root / "evaluation/scoring_rules.json")
    old = {r["rule_id"]: r for r in before["rules"] if r["type"] == "numeric"}
    new = {r["rule_id"]: r for r in after["rules"] if r["type"] == "numeric"}
    assert old.keys() == new.keys()
    for rid, rule in old.items():
        assert rule.get("tolerance") == new[rid].get("tolerance")
        changed_sign = (
            root.name == "paper_0de37d01e35c27df" and rule.get("target") == 0.073
        ) or (root.name == "paper_2f302589e5e9e420" and rid == "r_result_percent")
        assert new[rid].get("target") == (-rule["target"] if changed_sign else rule.get("target"))
        if root.name == "paper_2f302589e5e9e420" and rid == "r_result_percent":
            assert new[rid]["unit"] == "percentage points; signed EPI2-minus-EPI1 change"
        else:
            assert rule.get("unit") == new[rid].get("unit")
    old_conclusions = json.loads(subprocess.check_output([
        "git", "show", "46bef5e99489643fa994211b5bbcf2cc508822bd:" + original + "/evaluation/reference_conclusions.json"
    ], cwd=ROOT))["items"]
    old_limited = {k for c in old_conclusions if c.get("claim_role") == "limitation"
                   for k in c.get("supporting_key_point_ids", [])}
    old_core = {k for c in old_conclusions if c.get("claim_role") != "limitation"
                for k in c.get("supporting_key_point_ids", [])}
    new_core = {k for c in read(root / "evaluation/reference_conclusions.json")["items"]
                for k in c.get("supporting_key_point_ids", [])}
    assert old_limited - old_core <= new_core


@pytest.mark.parametrize("root", PACKAGES, ids=lambda p: p.parent.name + "/" + p.name)
def test_revised_packages_keep_scientific_rules_without_mandatory_disclaimers(root):
    report = validate_task_package(root)
    assert report.status == "passed", report.findings
    s = read(root / "agent_input/submission_schema.json")
    for definition in (s, s.get("result_schema", s)):
        validators.validator_for(definition).check_schema(definition)
    for node in dictionaries(s):
        assert not any(any(word in key.lower() for word in COMMENTARY) for key in node.get("required", []))
    reference = {p.name: read(p) for p in (root / "evaluation").glob("*.json")}
    conclusions = reference["reference_conclusions.json"]["items"]
    points = reference["reference_key_points.json"]["items"]
    ids = {c["conclusion_id"] for c in conclusions} | {p["key_point_id"] for p in points}
    assert all(c.get("claim_role") != "limitation" for c in conclusions)
    for rule in reference["scoring_rules.json"]["rules"]:
        assert rule["reference_id"] in ids
        for field in rule["binding"]["fields"]:
            assert "[]" not in field
            assert not any(word in field.lower() for word in COMMENTARY)
            if field.startswith("$"):
                parse(field)
    mode = read(root / "task_info.json")["task_type"]
    truth = _runtime_contract(task_type=mode, reference=reference, submission=s)
    assert truth["dual_axis_scoring_policy"]["policy_id"] == RESULTS_POLICY_ID
    assert sum(c["max_score"] for c in truth["scientific_conclusion_rubric"]) == 100
    if len(conclusions) == 1:
        assert truth["scientific_conclusion_rubric"][0]["max_score"] == 100
    assert all(r["diagnostic"] is None for r in truth["rule_table"])


def fixture_truth_and_verdict(policy, evidence_status="supported", score=100):
    truth = {
        "evaluation_mode": "dual_axis_100", "evaluation_profile": "autonomous_discovery",
        "dual_axis_scoring_policy": policy,
        "scoring_rubric": [{"id": "p", "max_score": 100}],
        "scientific_conclusion_rubric": [{"id": "s", "max_score": 100}],
    }
    item = {"id": "p", "score": 100, "rationale": "Synthetic evidence fixture.",
            "citations": [{"ref": "task/contract"}]}
    verdict = {"process_criteria": [item], "scientific_conclusions": [
        {**item, "id": "s", "score": score, "evidence_status": evidence_status}],
        "submission_validity": "valid", "rationale": "Synthetic fixture, not chemical evidence."}
    return truth, verdict


@pytest.mark.parametrize("status", ["unsupported", "contradicted"])
def test_new_policy_rejects_scientific_credit_without_support_in_both_paths(status, tmp_path):
    truth, verdict = fixture_truth_and_verdict(dual_axis_policy(scientific_results=True), status)
    with pytest.raises(ValueError, match="cannot receive positive"):
        validate_judge_verdict(verdict, truth, citation_check=lambda c: None)
    with pytest.raises(ValueError, match="cannot receive positive"):
        _aggregate(verdict, truth, tmp_path, {})
    verdict["scientific_conclusions"][0]["score"] = 0
    validate_judge_verdict(verdict, truth, citation_check=lambda c: None)


def test_supported_alternative_is_not_automatically_contradicted():
    truth, verdict = fixture_truth_and_verdict(dual_axis_policy(scientific_results=True))
    verdict["scientific_conclusions"][0]["rationale"] = "Evidence supports the task-permitted alternative interpretation."
    validate_judge_verdict(verdict, truth, citation_check=lambda c: None)
    system = _system_prompt(truth, ScoringBudget())
    assert "not automatically 'contradicted'" in system
    assert "Optional analyses may be omitted" in system
    assert "not criteria" in system


def test_legacy_policy_and_process_weights_are_unchanged():
    truth, verdict = fixture_truth_and_verdict(dual_axis_policy(), "contradicted")
    validate_judge_verdict(verdict, truth, citation_check=lambda c: None)
    assert truth["dual_axis_scoring_policy"]["policy_id"] == "dual_axis_100.v1"
    assert "scientific_results.v1" not in _system_prompt(truth, ScoringBudget())
    for mode in (False, True):
        old = process_rubric(reproduction=mode)
        new = process_rubric(reproduction=mode, scientific_results=True)
        assert [(r["id"], r["max_score"]) for r in old] == [(r["id"], r["max_score"]) for r in new]
    assert dual_axis_policy()["formula"] == dual_axis_policy(scientific_results=True)["formula"]


def test_unknown_policy_cannot_silently_use_legacy(tmp_path):
    p = package(tmp_path)
    ref = {f.name: read(f) for f in (p / "evaluation").glob("*.json")}
    ref["scoring_rules.json"]["scoring_policy"] = "misspelled-policy"
    with pytest.raises(EvaluatorReferenceInvalid, match="unknown authored"):
        _runtime_contract(task_type="autonomous_research", reference=ref,
                          submission=read(p / "agent_input/submission_schema.json"))


def test_final_loader_selects_only_approved_versions_and_public_files(tmp_path):
    canonical = package(tmp_path)
    final = tmp_path / "final_verified_autonomous_research" / canonical.name
    final.parent.mkdir()
    import shutil
    shutil.copytree(canonical, final)
    (final / "agent_input/task.md").write_text("Final version fixture")
    for name in ("author_results/answer.xyz", "task_provenance/repair.json", "verified_computation_reference.md"):
        p = final / "evaluation" / name
        p.parent.mkdir(exist_ok=True)
        p.write_text("private fixture")
    (final / "paper_route.md").write_text("private route fixture")
    rules = read(final / "evaluation/scoring_rules.json")
    rules["scoring_policy"] = RESULTS_POLICY_ID
    (final / "evaluation/scoring_rules.json").write_text(json.dumps(rules))
    refresh_manifest(final)
    key = ("autonomous_research", "paper_fixture")
    repository = TaskRepository.from_final(tmp_path, approved_tasks=[key])
    assert repository.get(task_type=key[0], paper_id=key[1]).directory == final
    assert TaskRepository.from_final(tmp_path, approved_tasks=[]).list() == []
    assert TaskRepository([tmp_path]).get(task_type=key[0], paper_id=key[1]).directory == canonical
    assert load_runtime_evaluation(task_type=key[0], paper_id=key[1], repository=repository).policy_id == RESULTS_POLICY_ID
    copied = materialize_agent_files(task_type=key[0], paper_id=key[1], repository=repository,
                                     destination=tmp_path / "workspace")
    assert set(copied) == {str(f.relative_to(final / "agent_input")) for f in (final / "agent_input").rglob("*") if f.is_file()}
    assert not (tmp_path / "workspace/evaluation").exists()
    assert not (tmp_path / "workspace/paper_route.md").exists()
    with pytest.raises(DuplicateTaskError):
        TaskRepository.from_final(tmp_path, approved_tasks=[key, key])
    for bad in [("hold_verified_autonomous_research", "paper_fixture"),
                ("autonomous_research", "../paper_fixture"), ("paper_reproduction", "paper_missing")]:
        with pytest.raises(InvalidTaskPackageError):
            TaskRepository.from_final(tmp_path, approved_tasks=[bad])
    alias = tmp_path / "final_verified_autonomous_research/paper_alias"
    alias.symlink_to(final, target_is_directory=True)
    with pytest.raises(InvalidTaskPackageError):
        TaskRepository.from_final(tmp_path, approved_tasks=[("autonomous_research", "paper_alias")])


def test_array_binding_does_not_become_first_item_or_automatic_success():
    values = {"objects": [{"id": "a", "value": 1}, {"id": "b", "value": 8}]}
    assert [m.value for m in parse("$.objects[*].value").find(values)] == [1, 8]
    entry = {"rule_id": "synthetic", "rule": {"rule_id": "synthetic", "type": "numeric",
             "target": 1, "tolerance": 0.1, "unit": "eV",
             "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.objects[*].value"],
                         "comparison": "absolute_difference"}}}
    for doc in [values, {"objects": []}, {"objects": [{"value": None}]}]:
        assert check_rule(entry, {"report/results.json": doc})["assessment"] != "pass"
    entry["rule"]["binding"]["fields"] = ["$.value"]
    for doc in [{}, {"value": None}]:
        assert check_rule(entry, {"report/results.json": doc})["assessment"] == "missing_value"


@pytest.mark.parametrize("mode", MODES)
def test_signed_dipole_result_optional_esp_and_truthful_failure(mode):
    s = schema("paper_2f302589e5e9e420", mode)
    v = validators.validator_for(s)(s)
    data = {"status": "complete", "fragments": [{"id": i, "validated": True, "dipole_debye": d,
            "validation_evidence": "synthetic", "optimization_evidence": "synthetic", "property_evidence": "synthetic"}
            for i, d in [("EPI1", 2.0), ("EPI2", 1.8)]],
            "method": {k: "synthetic" for k in ("software", "model", "optimization_protocol", "minimum_test")},
            "percent_change_ePI2_vs_EPI1": -10.0, "conclusion": "synthetic",
            "candidate_records": [{"candidate_id": i, "fragment_id": i, "generation_rationale": "synthetic",
                 "energy": -1, "validation_evidence": "synthetic", "advanced": True} for i in ("EPI1", "EPI2")],
            "comparison_basis": "synthetic", "evidence_files": ["synthetic.log"]}
    v.validate(data)  # No ESP, generic uncertainty essay, or limitations.
    v.validate({**data, "auxiliary_exploration": {"other_method": "synthetic"}})
    for modify in (lambda d: d["fragments"][1].update(id="EPI1"),
                   lambda d: d["fragments"][0].update(dipole_debye=None),
                   lambda d: d["fragments"][0].update(validated=False)):
        invalid = copy.deepcopy(data); modify(invalid)
        assert not v.is_valid(invalid)
    partial = copy.deepcopy(data)
    partial.update(status="bounded_failure", percent_change_ePI2_vs_EPI1=None, failure_details="synthetic failed property")
    partial["fragments"][0].update(validated=False, dipole_debye=None)
    v.validate(partial)
    del partial["failure_details"]
    assert not v.is_valid(partial)


@pytest.mark.parametrize("mode", MODES)
def test_numerical_and_conformer_success_failure_branches_do_not_overlap(mode):
    for paper, stage in (("paper_63a9254b8e68a23c", "final"), ("paper_641a923cbe5bbc48", "hold")):
        if stage == "hold":
            held = ROOT / "tasks" / f"hold_verified_{mode}" / paper
            assert validate_task_package(held).status == "passed"
            with pytest.raises(InvalidTaskPackageError, match="invalid_final_directory"):
                TaskRepository.from_final(ROOT / "tasks", approved_tasks=[(mode, paper)])
        s = schema(paper, mode, stage=stage)
        v = validators.validator_for(s)(s)
        # Minimal synthetic shape fixture; actual scientific validity belongs to the evaluator.
        def minimal(node):
            props = node.get("properties", {})
            if node.get("type") == "object" or "required" in node:
                return {k: minimal(props.get(k, {})) for k in node.get("required", [])}
            if "enum" in node: return node["enum"][0]
            if node.get("type") == "array": return [minimal(node.get("items", {})) for _ in range(node.get("minItems", 0))]
            if node.get("type") == "number": return 1.0
            if node.get("type") == "boolean": return True
            return "synthetic"
        success = minimal(s["oneOf"][0]); v.validate(success)
        failure = minimal(s["oneOf"][1]); v.validate(failure)
        required_result = "radius_nm" if "63a" in paper else "comparison"
        del success[required_result]
        assert not v.is_valid(success)


@pytest.mark.parametrize("mode", MODES)
def test_ts_completed_branch_cannot_hide_missing_barrier_or_wrong_frequency(mode):
    s = schema("paper_e2d9397dff2a3f0f", mode)
    v = validators.validator_for(s)(s)
    data = {"status": "completed", "system": {"charge": 1, "multiplicity": 1,
            "reference_structure": "synthetic", "target_structure": "synthetic"},
            "method": {"software": "synthetic", "electronic_structure": "synthetic", "solvent": "acetonitrile",
                       "temperature_K": 298.15, "barrier_equation": "synthetic"},
            "structures": {k: {"optimized": True, "imaginary_frequency_count": n, "evidence": "synthetic"}
                           for k, n in [("reference", 0), ("target", 1)]},
            "barrier": {"value_kcal_mol": 12.0, "evidence": "synthetic", "mode_assignment": "synthetic N-O"}}
    v.validate(data)
    wrong = copy.deepcopy(data); wrong["structures"]["target"]["imaginary_frequency_count"] = 0
    assert not v.is_valid(wrong)
    partial = copy.deepcopy(data); partial["barrier"]["value_kcal_mol"] = None
    assert not v.is_valid(partial)
    partial.update(status="bounded_failure", failure={"diagnostics": "synthetic", "attempted_steps": "synthetic"})
    v.validate(partial)


@pytest.mark.parametrize("mode", MODES)
def test_optional_hypotheses_do_not_replace_soc_state_results(mode):
    s = schema("paper_84efbea3ab8e6e20", mode)
    if mode == "autonomous_research":
        assert "hypotheses" not in s["required"]
        assert "minItems" not in s["properties"]["hypotheses"]
    mol = s["properties"]["molecules"]["items"]
    success = next(b for b in mol["oneOf"] if b["properties"]["outcome"]["const"] == "success")
    assert {"soc_pairs", "state_character"}.issubset(success["required"])


def test_correct_mnh2_identity_and_no_wrong_isomer_verification_claim():
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    root = ROOT / "tasks/hold_verified_paper_reproduction/paper_6943bfe5eeaa42b8"
    assert not (ROOT / "tasks/final_verified_paper_reproduction/paper_6943bfe5eeaa42b8").exists()
    identity = read(root / "agent_input/data/inputs/m_nh2_identity.json")
    mol = Chem.MolFromSmiles(identity["connectivity_smiles"])
    assert rdMolDescriptors.CalcMolFormula(mol) == "C16H16N2O2"
    assert sorted(map(len, mol.GetRingInfo().AtomRings())) == [6, 6, 6]
    archive = (root / "evaluation/verified_computation_reference.md").read_text()
    assert "NOT_RELEASE_READY" in archive
    assert "NOT_VERIFIED_FOR_PAPER_OBJECT" in archive


@pytest.mark.parametrize("mode", MODES)
def test_ferrocene_identity_and_experimental_only_absorption_inputs(mode):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    root = ROOT / "tasks" / f"final_verified_{mode}"
    species = read(root / "paper_60f4c45810428116/agent_input/data/inputs/species.json")
    for row in species["species"]:
        if row["id"] not in ("ferrocene", "ferrocenium"):
            continue
        mol = Chem.MolFromSmiles(row["smiles"])
        assert mol is not None
        assert rdMolDescriptors.CalcMolFormula(mol).rstrip("+") == "C10H10Fe"
        assert Chem.GetFormalCharge(mol) == row["formal_charge"]
    observation = read(root / "paper_2f2aa11ea61a32bb/agent_input/data/inputs/experimental_absorption.json")
    text = json.dumps(observation).lower()
    assert all(str(x) in text for x in (345, 375, 383, 381, 339))
    assert "toluene" in text
    assert not any(word in text for word in ("computed_nm", "td_energy_ev", "optimized_xyz"))

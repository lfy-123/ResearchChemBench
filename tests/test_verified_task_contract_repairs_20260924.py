"""Promoted-package contract regressions, not new scientific calculations.

Scientific evidence remains in the original group outputs. Mutated copies below
are deliberately incomplete format fixtures, never replacement reference data.
"""

import copy
import json
from collections import Counter
from pathlib import Path

import pytest
from jsonschema import validators

from chemistry_toolbox.src.output_contract import validate_output_contract
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository
from evaluation.scoring.adapters import load_runtime_evaluation


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "tasks"
MODES = ("autonomous_research", "paper_reproduction")
DBC = "paper_35a6749f3bae345b"
REPAIRED = [(mode, paper) for mode in MODES for paper in (
    DBC, "paper_9455a82229de2427", "paper_3d1d9b7f6df049da"
)] + [("paper_reproduction", "paper_ffa556cc3acdf0bc")]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def package(mode, paper=DBC):
    return BASE / f"final_verified_{mode}" / paper


@pytest.fixture(scope="module")
def historical_dbc_result():
    # Read-only successful author-informed computation, not a blind AR trial.
    return read(ROOT / f"docs/verification/group_2/{DBC}/report/results.json")


def check_submission(tmp_path, mode, document, expected):
    payload = (package(mode) / "agent_input/submission_schema.json").read_bytes()
    schema = json.loads(payload)["result_schema"]
    validator = validators.validator_for(schema)
    validator.check_schema(schema)
    assert validator(schema).is_valid(document) is expected
    report = tmp_path / "report"
    report.mkdir(exist_ok=True)
    result = report / "results.json"
    result.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    before = result.read_bytes()
    outcome = validate_output_contract(tmp_path, payload)
    assert outcome["valid"] is expected, outcome
    assert result.read_bytes() == before


@pytest.mark.parametrize("mode", MODES)
def test_historical_complete_result_still_submits(tmp_path, mode, historical_dbc_result):
    check_submission(tmp_path, mode, historical_dbc_result, True)


@pytest.mark.parametrize("mode", MODES)
def test_complete_without_disclaimer_with_failed_extra_attempt_submits(
    tmp_path, mode, historical_dbc_result
):
    document = copy.deepcopy(historical_dbc_result)
    document.pop("limitations", None)
    document["attempts"] = [{
        "status": "failed", "reason": "SYNTHETIC: an earlier optional attempt failed"
    }]
    check_submission(tmp_path, mode, document, True)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("molecule_index", (0, 1))
def test_validated_cannot_replace_orbital_findings_with_failure(
    tmp_path, mode, molecule_index, historical_dbc_result
):
    document = copy.deepcopy(historical_dbc_result)
    document["molecules"][molecule_index]["orbital_evidence"] = {
        "failure_report": "SYNTHETIC: orbital analysis did not complete"
    }
    assert document["status"] == "validated"
    check_submission(tmp_path, mode, document, False)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("molecule_index", (0, 1))
@pytest.mark.parametrize("field", (
    "criterion", "HOMO", "LUMO", "S0_evidence", "S1_evidence"
))
@pytest.mark.parametrize("bad_value", ("", " \t\n", None, "__MISSING__"))
def test_validated_requires_each_nonblank_evidence_field(
    tmp_path, mode, molecule_index, field, bad_value, historical_dbc_result
):
    document = copy.deepcopy(historical_dbc_result)
    molecule = document["molecules"][molecule_index]
    if field.endswith("_evidence"):
        parent = molecule["state_checks"][field[:2]]
        key = "evidence"
    else:
        parent = molecule["orbital_evidence"]
        key = field
    if bad_value == "__MISSING__":
        del parent[key]
    else:
        parent[key] = bad_value
    check_submission(tmp_path, mode, document, False)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("molecule_index", (0, 1))
def test_detailed_partial_orbital_failure_remains_submittable(
    tmp_path, mode, molecule_index, historical_dbc_result
):
    document = copy.deepcopy(historical_dbc_result)
    document["status"] = "bounded_failure"
    molecule = document["molecules"][molecule_index]
    molecule["outcome"] = "bounded_failure"
    molecule["orbital_evidence"] = {
        "failure_report": "SYNTHETIC: orbital analysis did not complete"
    }
    document["conclusion"] = "SYNTHETIC: partial results; no full completion claim"
    check_submission(tmp_path, mode, document, True)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("with_partial", (False, True))
def test_compact_failure_needs_no_invented_results(
    tmp_path, mode, with_partial, historical_dbc_result
):
    document = {
        "status": "bounded_failure",
        "failure_report": {
            "reason": "SYNTHETIC: incomplete calculation",
            "missing_endpoint": "Required orbital analysis unavailable",
            "completed_artifacts": [],
        },
    }
    if with_partial:
        document["partial_results"] = {
            "molecules": [copy.deepcopy(historical_dbc_result["molecules"][0])]
        }
    check_submission(tmp_path, mode, document, True)


@pytest.mark.parametrize("mode", MODES)
def test_reaction_metadata_matches_optional_ts_boundary(mode):
    root = package(mode, "paper_9455a82229de2427")
    description = read(root / "task_info.json")["difficulty_reasons"][0]
    assert "at least two distinct product candidates" in description
    assert "validate minima" in description
    assert "0 K reaction energies" in description
    assert "Intermediate and transition-state calculations are optional" in description
    assert "any that are claimed require corresponding validation" in description
    assert "TS/intermediate calculations are optional" in (root / "agent_input/task.md").read_text()


@pytest.mark.parametrize("mode", MODES)
def test_ih_source_summary_lists_all_four_existing_targets(mode):
    root = package(mode, "paper_3d1d9b7f6df049da")
    evidence = read(root / "evaluation/evidence_map.json")["evidence"]
    entry = next(item for item in evidence if item["source"] == "SI Table S3a")
    # Directly checked against original SI PDF p21, Table S3a rows 4--7.
    frequencies = [49.9, 54.9, 65.2, 68.9]
    assert entry["text"] == "Ih " + ",".join(map(str, frequencies)) + " cm-1"
    rules = read(root / "evaluation/scoring_rules.json")["rules"]
    assert any(rule.get("target") == frequencies for rule in rules)


def test_nmr_metadata_matches_four_mapped_conformers():
    root = package("paper_reproduction", "paper_ffa556cc3acdf0bc")
    description = read(root / "task_info.json")["data"][0]["description"]
    assert "two relative-configuration candidates with two conformers each" in description
    assert "four complete XYZ geometries" in description
    inputs = root / "agent_input/data/inputs"
    records = read(inputs / "carbon_label_mapping.json")["records"]
    assert Counter(record["candidate_id"] for record in records) == {
        "candidate_A": 2, "candidate_B": 2
    }
    assert len({record["file"] for record in records}) == 4
    for record in records:
        xyz = inputs / record["file"]
        assert xyz.is_file() and int(xyz.read_text().splitlines()[0]) == 81
        assert len(record["carbon_label_to_xyz_atom_1based"]) == 30


@pytest.fixture(scope="module")
def repository():
    return TaskRepository.from_final(BASE, approved_tasks=REPAIRED)


@pytest.mark.parametrize(("mode", "paper"), REPAIRED)
def test_repaired_package_and_runtime_load(mode, paper, repository):
    result = validate_task_package(package(mode, paper))
    assert result.status == "passed", result.findings
    runtime = load_runtime_evaluation(paper_id=paper, task_type=mode, repository=repository)
    assert runtime.policy_id == "dual_axis_100.scientific_results.v1"

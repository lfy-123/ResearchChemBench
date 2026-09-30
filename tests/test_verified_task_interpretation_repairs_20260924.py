"""Offline regressions for three confirmed inconsistencies, now in final.

Historical computations are read-only. Reindexing and arithmetic below are
test-only transformations, not new quantum calculations or LLM-judge tests.
"""

import copy
import itertools
import json
from pathlib import Path

import pytest
from jsonpath_ng import parse
from jsonschema import validators

from chemistry_toolbox.src.output_contract import validate_output_contract
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository
from evaluation.scoring.adapters import load_runtime_evaluation


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "tasks"
MODES = ("autonomous_research", "paper_reproduction")
TIN = "paper_a21b91f97ce3c68f"
CY2 = "paper_e0791c047a731974"
NMR = "paper_ffa556cc3acdf0bc"
PACKAGES = [(mode, paper) for mode in MODES for paper in (TIN, CY2)] + [
    ("paper_reproduction", NMR)
]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def package(mode, paper):
    return BASE / f"final_verified_{mode}" / paper


def historical(paper):
    return read(ROOT / "docs/verification/group_4" / paper / "report/results.json")


def check_output(tmp_path, mode, paper, document, expected):
    payload = (package(mode, paper) / "agent_input/submission_schema.json").read_bytes()
    schema = json.loads(payload)["result_schema"]
    validator = validators.validator_for(schema)
    validator.check_schema(schema)
    assert validator(schema).is_valid(document) is expected
    report = tmp_path / "report"
    report.mkdir(exist_ok=True)
    path = report / "results.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    before = path.read_bytes()
    result = validate_output_contract(tmp_path, payload)
    assert result["valid"] is expected, result
    assert path.read_bytes() == before


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("paper", (TIN, CY2))
def test_historical_results_remain_submittable(tmp_path, mode, paper):
    # Format acceptance does not endorse the old Cy2 mechanistic prose.
    document = historical(paper)
    document.pop("limitations", None)
    check_output(tmp_path, mode, paper, document, True)


@pytest.mark.parametrize("mode", MODES)
def test_tin_reordering_is_mapped_back_without_changing_science(tmp_path, mode):
    source = historical(TIN)
    working = copy.deepcopy(source)
    mapping = {i: 62 if i == 1 else i - 1 for i in range(1, 63)}
    inverse = {value: key for key, value in mapping.items()}
    working["atom_mapping"] = [
        {"original": original, "working": new} for original, new in mapping.items()
    ]
    for pair in working["sn_bu_pairs"]:
        pair["sn_atom_index"] = mapping[pair["sn_atom_index"]]
        pair["carbon_atom_index"] = mapping[pair["carbon_atom_index"]]
    # A working index is not the now-explicit public reporting index.
    check_output(tmp_path, mode, TIN, working, False)
    for pair in working["sn_bu_pairs"]:
        pair["sn_atom_index"] = inverse[pair["sn_atom_index"]]
        pair["carbon_atom_index"] = inverse[pair["carbon_atom_index"]]
    assert working["sn_bu_pairs"] == source["sn_bu_pairs"]
    assert working["mean_coupling_hz"] == source["mean_coupling_hz"]
    check_output(tmp_path, mode, TIN, working, True)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("order", list(itertools.permutations(range(3))))
def test_tin_pair_array_order_does_not_change_identity(tmp_path, mode, order):
    document = historical(TIN)
    document["sn_bu_pairs"] = [document["sn_bu_pairs"][i] for i in order]
    check_output(tmp_path, mode, TIN, document, True)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("mutation", ("duplicate", "missing", "wrong_carbon"))
def test_tin_incomplete_or_wrong_pairs_still_rejected(tmp_path, mode, mutation):
    document = historical(TIN)
    if mutation == "duplicate":
        document["sn_bu_pairs"][1] = copy.deepcopy(document["sn_bu_pairs"][0])
    elif mutation == "missing":
        document["sn_bu_pairs"].pop()
    else:
        document["sn_bu_pairs"][0]["carbon_atom_index"] = 8
    check_output(tmp_path, mode, TIN, document, False)


@pytest.mark.parametrize("mode", MODES)
def test_tin_instruction_and_schema_describe_same_indices(mode):
    root = package(mode, TIN)
    task = (root / "agent_input/task.md").read_text()
    schema = (root / "agent_input/submission_schema.json").read_text()
    assert "or report a complete remapping" not in task
    assert "Atom order is fixed." not in task
    assert "Calculation programs may reorder atoms" in task
    assert "original 1-based indices" in task and "original 1-based indices" in schema
    assert "Sn=1 and butyl carbons=2,3,7" in task
    rules = read(root / "evaluation/scoring_rules.json")["rules"]
    pair_rule = next(rule for rule in rules if rule["rule_id"].endswith("_pairs"))
    assert "Program-internal reordering is allowed" in pair_rule["expected"]


@pytest.mark.parametrize("mode", MODES)
def test_cy2_energy_only_interpretation_without_optional_diagnostic(tmp_path, mode):
    document = historical(CY2)
    vertical = document["observables"]["vertical"]
    s1, t1, t2 = [vertical[state]["energy_eV"] for state in ("s1", "t1", "t2")]
    assert s1 - t1 == pytest.approx(0.8354)
    assert t2 - s1 == pytest.approx(0.2311)
    # Read-only arithmetic from recorded energies, not a new computation.
    document["validation"]["checks"] = (
        f"T1<S1<T2; S1-T1={s1-t1:.4f} eV; T2-S1={t2-s1:.4f} eV."
    )
    document["conclusion"] = (
        "The validated Cy2 energies put T2 above S1 with a smaller separation "
        "than S1-T1; the separately relaxed T1 electronic gap is reported."
    )
    document.pop("limitations", None)
    check_output(tmp_path, mode, CY2, document, True)
    document["attempts"] = [{"status": "failed", "reason": "SYNTHETIC extra attempt"}]
    check_output(tmp_path, mode, CY2, document, True)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("missing", ("s1", "t1", "t2", "adiabatic_t1"))
def test_cy2_complete_still_requires_all_four_energies(tmp_path, mode, missing):
    document = historical(CY2)
    parent = document["observables"] if missing == "adiabatic_t1" else document["observables"]["vertical"]
    del parent[missing]
    check_output(tmp_path, mode, CY2, document, False)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("paper", (TIN, CY2))
def test_compact_failure_requires_no_invented_results(tmp_path, mode, paper):
    document = {
        "status": "bounded_failure",
        "failure_report": {
            "reason": "SYNTHETIC format-only early failure",
            "missing_endpoint": "Calculation has no endpoint",
            "completed_artifacts": [],
        },
    }
    check_output(tmp_path, mode, paper, document, True)


@pytest.mark.parametrize("mode", MODES)
def test_cy2_scope_and_source_attribution_are_consistent(mode):
    root = package(mode, CY2)
    task = (root / "agent_input/task.md").read_text()
    route = (root / "paper_route.md").read_text()
    reference = (root / "evaluation/verified_computation_reference.md").read_text()
    assert "the inequality 2×T1>S1" not in task
    assert "optional Cy2 diagnostic" in task
    assert "S1−T1 and T2−S1" in task
    assert "Gaussian 16 unrestricted DFT (UDFT)" in route
    assert "The archived verification used TD(Triplets" in route
    assert "rubrene 湮灭剂" in reference
    assert "S1−T1=.8354 eV" in reference
    assert "历史解释不再用作当前结论的证明" in reference
    rules = read(root / "evaluation/scoring_rules.json")["rules"]
    final_rule = next(rule for rule in rules if rule["rule_id"].endswith("_s7"))
    assert "no independent score" in final_rule["expected"]
    assert "generic limitation statement" in final_rule["expected"]
    assert "$.observables" in final_rule["binding"]["fields"]
    conclusion = read(root / "evaluation/reference_conclusions.json")["items"][0]
    assert "vertical S1/T1/T2 ordering" in conclusion["statement"]
    assert len(conclusion["supporting_key_point_ids"]) == 4
    # Source values and results remain private; AR gets no author mechanism.
    public = task + (root / "agent_input/submission_schema.json").read_text()
    for private_value in ("1.8909", "1.0556", "2.1221", "1.010301083", "0.8354", "0.2311"):
        assert private_value not in public
    if mode == "autonomous_research":
        assert "authors propose" not in task.lower()
        assert "rubrene" not in public.lower()


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("paper", (TIN, CY2))
def test_numeric_targets_and_successful_result_comparison_unchanged(mode, paper):
    rules = read(package(mode, paper) / "evaluation/scoring_rules.json")["rules"]
    numeric = [rule for rule in rules if rule["type"] == "numeric"]
    source = historical(paper)
    expected = [(-217, 15)] if paper == TIN else [
        (1.8909, 0.15), (1.0556, 0.15), (2.1221, 0.15), (1.09, 0.15)
    ]
    assert [(rule["target"], rule["tolerance"]) for rule in numeric] == expected
    for rule in numeric:
        if paper == TIN:
            value = sum(pair["coupling_hz"] for pair in source["sn_bu_pairs"]) / 3
            assert value == pytest.approx(source["mean_coupling_hz"])
        else:
            field = rule["binding"]["fields"][0]
            value = parse(field).find(source)[0].value
        assert abs(value - rule["target"]) <= rule["tolerance"]


def test_nmr_reference_names_the_actual_primary_branch_and_reuse():
    root = package("paper_reproduction", NMR)
    reference = (root / "evaluation/verified_computation_reference.md").read_text()
    source = read(ROOT / "docs/verification/group_4" / NMR / "provenance/carbon_mapping_20260918/dp4_results.json")
    assert source["primary_TMS_calibration"]["C_shielding_ppm"] == 188.48755
    assert "**188.48755 ppm**" in reference
    assert "**189.1954 ppm**" in reference
    assert "author_standard_computed" in reference and "primary_TMS_calibration" in reference
    assert "不是从这些 M06 输出重新串接" in reference
    branches = {row["weight_energy"]: row for row in source["author_standard_computed"]}
    for weighting in ("E", "G"):
        probabilities = branches[weighting]["probabilities"]["DP4"]
        assert sum(probabilities[key] for key in ("A_8R_percent", "B_8S_percent")) == pytest.approx(100)
        assert f'{probabilities["B_8S_percent"]:.9f}%' in reference
        assert probabilities["B_8S_percent"] > probabilities["A_8R_percent"]


@pytest.mark.parametrize(("mode", "paper"), PACKAGES)
def test_modified_packages_and_runtime_load(mode, paper):
    root = package(mode, paper)
    result = validate_task_package(root)
    assert result.status == "passed", result.findings
    repository = TaskRepository.from_final(BASE, approved_tasks=PACKAGES)
    runtime = load_runtime_evaluation(paper_id=paper, task_type=mode, repository=repository)
    assert runtime.policy_id == "dual_axis_100.scientific_results.v1"

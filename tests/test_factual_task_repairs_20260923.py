"""Source-backed data regressions; no paper-specific production scoring logic."""
from pathlib import Path
import json

import pytest

from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository
from evaluation.scoring.adapters import load_runtime_evaluation


ROOT = Path(__file__).resolve().parents[1]
MODES = ("autonomous_research", "paper_reproduction")
REPAIRED = ("paper_0a62b797f51de2c0", "paper_9aa6d5655edfeb52",
            "paper_fcc3c7f2c46a0fbe", "paper_98b6f8a0352f72c2",
            "paper_46f6118697c6397c", "paper_3c058fa17fa7c54e",
            "paper_f9d09d28c7d9adaa", "paper_fda8b9b53f8276db")


def package(mode, paper):
    return ROOT / "tasks" / f"final_verified_{mode}" / paper


def read(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("paper", REPAIRED)
def test_repaired_package_and_runtime_load(mode, paper):
    root = package(mode, paper)
    result = validate_task_package(root)
    assert result.status == "passed", result.findings
    load_runtime_evaluation(paper_id=paper, task_type=mode,
                            repository=TaskRepository.from_final(
                                ROOT / "tasks", approved_tasks=[(mode, paper)]))


@pytest.mark.parametrize("mode", MODES)
def test_0a62_identity_property_stage_and_surface_are_distinct(mode):
    root = package(mode, REPAIRED[0])
    text = (root / "evaluation/verified_computation_reference.md").read_text()
    result = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
    rows = {r["id"]: r for r in result["molecules"]}
    for identity, final, initial, source in (
        ("M-Th-0CN", 1.1570, 1.1334, "M-Th-0CN"),
        ("M-Th-1CN", 3.3674, 3.3406, "M-Th-2CN"),
        ("M-Th-2CN", 5.9387, 5.9017, "M-Th-1CN"),
    ):
        row = rows[identity]
        assert row["dipole"]["value"] == final
        assert row["source_label"] == source
        assert source in row["dipole"]["source_log"]
        assert result["property_stage_correction"]["previous_initial_geometry_dipoles"][identity]["value"] == initial
        assert "0.001 a.u." in row["esp"]["definition"]
        assert "0.15 Bohr" in row["esp"]["definition"]
    assert result["comparison"]["author_route_dipole_totals_debye"] == [1.1744, 3.3867, 6.0547]
    assert read(root / "evaluation/identity_correction.json")["paper_reference"]["dipoles_debye"] == [0.5921, 4.1644, 6.6147]
    assert "0.15 a.u. Multiwfn surface" not in text
    assert "symmetry/geometry effect" not in text
    other_prefix = "ar_rule" if mode == "paper_reproduction" else "pr_rule"
    assert other_prefix not in text


@pytest.mark.parametrize("mode", MODES)
def test_4b_graph_matches_si_selectors_not_only_formula(mode):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors

    root = package(mode, REPAIRED[2])
    data = read(root / "agent_input/data/inputs/compound_4b.json")
    mol = Chem.MolFromSmiles(data["smiles"])
    assert rdMolDescriptors.CalcMolFormula(mol) == data["formula"]
    labels = {name: int(index) - 1 for index, name in data["smiles_atom_labels"].items()}
    assert len(labels) == mol.GetNumAtoms()
    for name, i in labels.items():
        assert mol.GetAtomWithIdx(i).GetSymbol() == name.rstrip("0123456789")
    geometry = read(root / "agent_input/data/inputs/geometry_comparison.json")
    for records in geometry.values():
        if not isinstance(records, list):
            continue
        for record in records:
            names = record["atoms"].split("-")
            assert all(mol.GetBondBetweenAtoms(labels[a], labels[b]) is not None
                       for a, b in zip(names, names[1:])), record["atoms"]
    for a, b in (("C7", "O1"), ("C1", "S3"), ("C3", "C4")):
        assert mol.GetBondBetweenAtoms(labels[a], labels[b]).GetBondType() == Chem.BondType.DOUBLE
    assert mol.GetBondBetweenAtoms(labels["C3"], labels["C4"]).GetStereo() == Chem.BondStereo.STEREOE
    assert mol.GetBondBetweenAtoms(labels["C7"], labels["S1"]) is None


@pytest.mark.parametrize("mode", MODES)
def test_9aa6_route_agrees_with_existing_lowest_state_target(mode):
    root = package(mode, REPAIRED[1])
    route = (root / "paper_route.md").read_text()
    assert "Excited State 1 as S1 = 3.8591 eV" in route
    assert "Excited State 2 is a different, higher root at 4.1762 eV" in route
    rules = read(root / "evaluation/scoring_rules.json")["rules"]
    assert any(r.get("target") == 3.8591 for r in rules)


@pytest.mark.parametrize("mode", MODES)
def test_98b6_lifetime_is_derived_and_target_unchanged(mode):
    root = package(mode, REPAIRED[3])
    tau_ns = 1.4999e9 / (0.64 * (3.65 * 8065.544005) ** 2)
    assert tau_ns == pytest.approx(2.70, abs=0.01)
    points = read(root / "evaluation/reference_key_points.json")["items"]
    point = next(p for p in points if p["key_point_id"].endswith("result_3"))
    assert "not an exact SI Table S1 quotation" in point["expected"]
    assert all("36d362" not in e for e in point["evidence_ids"])


@pytest.mark.parametrize("mode", MODES)
def test_46f6_keeps_si_targets_and_tolerances_for_the_same_state(mode):
    root = package(mode, "paper_46f6118697c6397c")
    rules = read(root / "evaluation/scoring_rules.json")["rules"]
    energy = next(r for r in rules if r["rule_id"].endswith("_energy"))
    oscillator = next(r for r in rules if r["rule_id"].endswith("_osc"))
    assert (energy["target"], energy["tolerance"]) == (3.8436, 0.15)
    assert (oscillator["target"], oscillator["tolerance"]) == (0.4243, 0.05)
    assert 1239.841984 / energy["target"] == pytest.approx(322.58, abs=0.01)
    assert all(r.get("target") != 4.33 for r in rules)
    evidence = {e["evidence_id"]: e["source"]
                for e in read(root / "evaluation/evidence_map.json")["evidence"]}
    for rule in (energy, oscillator):
        point = next(p for p in read(root / "evaluation/reference_key_points.json")["items"]
                     if p["key_point_id"] == rule["reference_id"])
        assert any("Table S3" in evidence[e] and "S5" in evidence[e]
                   for e in point["evidence_ids"])


@pytest.mark.parametrize("mode", MODES)
def test_3c058_uses_spin_labelled_figure_reference_without_exposing_answers(mode):
    root = package(mode, "paper_3c058fa17fa7c54e")
    points = read(root / "evaluation/reference_key_points.json")["items"]
    energies = next(p for p in points if p["key_point_id"] == "kp_energies")
    assert "An-sigma-Ph 3.1457/1.7347" in energies["expected"]
    assert "An-sigma-DA 2.9835/1.7284" in energies["expected"]
    evidence = {e["evidence_id"]: e["source"]
                for e in read(root / "evaluation/evidence_map.json")["evidence"]}
    assert any("Figure 2" in evidence[e] for e in energies["evidence_ids"])
    for name, s1, t1, gap, margin in (
        ("Ph", 3.1457, 1.7347, 1.4110, .3237),
        ("DA", 2.9835, 1.7284, 1.2551, .4733),
    ):
        assert s1 - t1 == pytest.approx(gap)
        assert 2 * t1 - s1 == pytest.approx(margin)
        for path in (root / "agent_input").rglob("*"):
            if path.is_file():
                assert str(s1) not in path.read_text(), (name, path)


@pytest.mark.parametrize("mode", MODES)
def test_f9_graph_selectors_are_complete_and_survive_atom_reordering(mode):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors

    data = read(package(mode, "paper_f9d09d28c7d9adaa") /
                "agent_input/data/inputs/compound_definitions.json")
    for record in data["compounds"]:
        original = Chem.MolFromSmiles(record["atom_mapped_smiles"])
        for mol in (original, Chem.RenumberAtoms(original, list(reversed(range(original.GetNumAtoms()))))):
            assert rdMolDescriptors.CalcMolFormula(mol) == record["formula"]
            ids = {a.GetAtomMapNum(): a.GetIdx() for a in mol.GetAtoms()}
            assert len(ids) == mol.GetNumAtoms() and 0 not in ids
            fragments = record["ifct_fragment_heavy_atom_map_ids"]
            assert len(fragments) == 3
            assert sorted(sum(fragments.values(), [])) == sorted(ids)
            alpha = record["alpha3_atom_map_ids"]
            assert all(mol.GetBondBetweenAtoms(ids[a], ids[b])
                       for a, b in zip(alpha, alpha[1:]))
            assert {mol.GetAtomWithIdx(ids[a]).GetSymbol() for a in alpha[1:3]} == {"N", "C"}
            planes = record["beta1_plane_atom_map_ids"]
            if record["id"].endswith("Fy"):
                rings = {frozenset(ring) for ring in Chem.GetSymmSSSR(mol)}
                assert len(planes) == 2
                assert all(len(group) == 6 and frozenset(ids[a] for a in group) in rings for group in planes)
                assert not set(planes[0]) & set(planes[1])
            else:
                assert planes is None


def _f9_format_example(root):
    """Format-only fixture. Actual scientific outputs are checked separately."""
    records = []
    for definition in read(root / "agent_input/data/inputs/compound_definitions.json")["compounds"]:
        record = {
            "id": definition["id"], "status": "complete",
            "method": {"software": "fixture", "method": "fixture", "basis": "fixture", "charge": 0,
                       "multiplicity": 1, "structure_provenance": "fixture"},
            "convergence": {"optimized": True, "evidence": "fixture.log", "termination_record": "fixture"},
            "dihedrals": {"alpha3": {"signed_value_deg": 89., "value_deg": 89., "atom_indices": definition["alpha3_atom_map_ids"]},
                          "beta1": None},
            "orbital_localization": {"fragment_definitions": {}, "homo_fragments": {}, "lumo_fragments": {}},
            "validation": {"type": "fixture", "evidence": "fixture.log"},
            "atom_mapping_file": "mapping.json",
            "excited_state": {"state_index": 1, "spin": "singlet", "method": "fixture", "energy_eV": 3.,
                              "oscillator_strength": 0., "geometry_file": "geometry.xyz",
                              "state_assignment_evidence": "fixture.log", "calculation_files": ["fixture.log"],
                              "nto": {"state_index": 1, "weights": [1.], "orbital_file": "nto.mwfn", "hole_index": 1,
                                      "electron_index": 2, "fragment_populations": [{}, {}], "evidence": "nto.log"},
                              "ifct": {"state_index": 1, "partition_method": "fixture", "fragment_definitions": {},
                                       "ct_percent": 40., "le_percent": 60., "transfer_matrix_file": "matrix.json", "evidence": "ifct.log"}},
        }
        if definition["beta1_plane_atom_map_ids"]:
            record["dihedrals"]["beta1"] = {"value_deg": 89., "plane_atom_indices": definition["beta1_plane_atom_map_ids"],
                                            "plane_fit_rms_A": [0.001, 0.001]}
        records.append(record)
    return {"status": "complete", "compounds": records,
            "comparisons": [{"pair": pair, "finding": "fixture", "evidence": "fixture.log"}
                            for pair in ("MeAC–TfAC", "MeACFy–TfACFy", "MeAC–MeACFy", "TfAC–TfACFy")],
            "conclusion": "Format-only example; this does not certify scientific correctness."}


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("defect", ("missing_s1", "missing_ifct", "wrong_root", "wrong_nto_root", "torsion_for_plane", "null_fy_plane", "duplicate_id", "incomplete_member"))
def test_f9_public_contract_rejects_incomplete_or_mismatched_s1_records(tmp_path, mode, defect):
    from chemistry_toolbox.src.output_contract import validate_output_contract

    root = package(mode, "paper_f9d09d28c7d9adaa")
    report = _f9_format_example(root)
    (tmp_path / "report").mkdir()
    output = tmp_path / "report/results.json"
    contract = (root / "agent_input/submission_schema.json").read_bytes()
    output.write_text(json.dumps(report))
    assert validate_output_contract(tmp_path, contract)["valid"]
    rows = report["compounds"]
    if defect == "missing_s1":
        del rows[0]["excited_state"]
    elif defect == "missing_ifct":
        del rows[0]["excited_state"]["ifct"]
    elif defect == "wrong_root":
        rows[0]["excited_state"]["state_index"] = 2
    elif defect == "wrong_nto_root":
        rows[0]["excited_state"]["nto"]["state_index"] = 2
    elif defect == "torsion_for_plane":
        rows[2]["dihedrals"]["beta1"] = {"signed_value_deg": 167., "value_deg": 167., "atom_indices": [1, 2, 3, 4]}
    elif defect == "null_fy_plane":
        rows[2]["dihedrals"]["beta1"] = None
    elif defect == "duplicate_id":
        rows[1]["id"] = rows[0]["id"]
    else:
        rows[0] = {"id": "MeAC", "status": "bounded_failure", "failure": dict.fromkeys(
            ("stage", "evidence", "attempted_remedies", "bounded_conclusion"), "fixture")}
    output.write_text(json.dumps(report))
    assert not validate_output_contract(tmp_path, contract)["valid"]
    if defect == "incomplete_member":
        report.update(status="bounded_failure", failure_summary="S1 unavailable for MeAC")
        output.write_text(json.dumps(report))
        assert validate_output_contract(tmp_path, contract)["valid"]


@pytest.mark.parametrize("mode", MODES)
def test_fda8_six_public_experimental_pairs_match_source_regression(mode):
    import numpy as np

    root = package(mode, "paper_fda8b9b53f8276db")
    inputs = root / "agent_input/data/inputs"
    rows = read(inputs / "experimental_bonds.json")["bonds"]
    pairs = ["-".join(r["atoms"]) for r in rows]
    assert pairs == ["C1-C2", "C2-C3", "N1-C1", "N2-C2", "N3-C3", "C1-C10"]
    assert ["-".join(pair) for pair in read(inputs / "ccdc_record.json")["comparison_bonds"]] == pairs
    assert all(set(row) == {"atoms", "experimental_length"} for row in rows)
    exp = np.array([r["experimental_length"] for r in rows])
    theory = np.array([1.489, 1.426, 1.339, 1.316, 1.310, 1.399])
    fit = np.polyfit(exp, theory, 1)
    r2 = 1 - np.sum((theory - np.polyval(fit, exp)) ** 2) / np.sum((theory - theory.mean()) ** 2)
    assert np.sqrt(np.mean((theory - exp) ** 2)) == pytest.approx(.004062019202)
    assert fit == pytest.approx([1.04674618488, -.064676401801])
    assert r2 == pytest.approx(.998042651229)
    rules = read(root / "evaluation/scoring_rules.json")["rules"]
    rmse = next(r for r in rules if r["reference_id"].endswith("result_geometry"))
    assert (rmse["target"], rmse["unit"]) == (.004, "Å")
    schema = read(root / "agent_input/submission_schema.json")["result_schema"]
    selected = "selected_result" if mode == "autonomous_research" else "optimization"
    assert "conformer" in schema["properties"][selected]["required"]

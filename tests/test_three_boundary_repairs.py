"""Contract and existing-output arithmetic checks, not new quantum validation.

Submission fixtures below test JSON shape only; they are never archived as real
agent computations or used to claim a successful autonomous trajectory.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from collections import Counter
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
from jsonschema import Draft202012Validator

from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository, materialize_agent_files

ROOT = Path(__file__).resolve().parents[1]
MODES = ("autonomous_research", "paper_reproduction")
PAPERS = ("paper_1b285cf9f763f2cf", "paper_534ae3b6e2fb695f", "paper_b815e2622b0d6085")
spec = importlib.util.spec_from_file_location("three_boundary_replay", ROOT / "scripts/replay_three_boundary_observables.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


def package(mode, paper):
    candidates = [ROOT / "tasks" / f"{stage}_verified_{mode}" / paper for stage in ("final", "hold")]
    present = [path for path in candidates if path.is_dir()]
    assert len(present) == 1, f"Expected exactly one maintained package: {candidates}"
    return present[0]


def read(path):
    return json.loads(path.read_text())


def repair_record(p):
    # Final maintenance records moved under task_provenance; the older held
    # package retains its original layout.
    current = p / "evaluation/task_provenance/boundary_repair_evidence.json"
    return current if current.is_file() else p / "evaluation/boundary_repair_evidence.json"


def assert_json_close(actual, expected, path="$", *, atol=1e-12):
    """Compare replay archives without requiring binary-identical float output.

    The replay parses text files independently from the archived JSON.  Tiny
    last-bit differences are expected, while keys, list lengths and all
    nonnumeric values must remain exact.
    """
    if isinstance(actual, dict) and isinstance(expected, dict):
        assert set(actual) == set(expected), path
        for key in actual:
            assert_json_close(actual[key], expected[key], f"{path}.{key}", atol=atol)
    elif isinstance(actual, list) and isinstance(expected, list):
        assert len(actual) == len(expected), path
        for i, (left, right) in enumerate(zip(actual, expected)):
            assert_json_close(left, right, f"{path}[{i}]", atol=atol)
    elif isinstance(actual, (int, float)) and isinstance(expected, (int, float)) \
            and not isinstance(actual, bool) and not isinstance(expected, bool):
        assert actual == pytest.approx(expected, abs=atol, rel=1e-12), path
    else:
        assert actual == expected, path


def validator(mode, paper):
    return Draft202012Validator(read(package(mode, paper) / "agent_input/submission_schema.json")["result_schema"])


@pytest.fixture(scope="module")
def replays():
    return {PAPERS[0]: replay.replay_spinel(), PAPERS[1]: replay.replay_diamines(), PAPERS[2]: replay.replay_bands()}


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("paper", PAPERS)
def test_six_packages_are_valid_and_materialize_only_public_files(mode, paper, tmp_path):
    source = package(mode, paper)
    target = tmp_path / "tasks" / mode / paper
    shutil.copytree(source, target)
    checked = validate_task_package(target)
    assert checked.status == "passed", checked.findings
    Draft202012Validator.check_schema(read(target / "agent_input/submission_schema.json")["result_schema"])
    repo = TaskRepository(roots=[tmp_path / "tasks"])
    files = materialize_agent_files(paper_id=paper, task_type=mode, destination=tmp_path / "agent", repository=repo)
    expected = sorted(str(p.relative_to(source / "agent_input")) for p in (source / "agent_input").rglob("*") if p.is_file())
    assert sorted(files) == expected
    assert not any("evaluation" in x or "paper_route" in x or "reference" in x for x in files)
    assert not (tmp_path / "agent/evaluation").exists()
    # All rule references and evidence references resolve inside the evaluator.
    kp = read(source / "evaluation/reference_key_points.json")["items"]
    conclusions = read(source / "evaluation/reference_conclusions.json")["items"]
    refs = {i["key_point_id"] for i in kp} | {i["conclusion_id"] for i in conclusions}
    evidence = {i["evidence_id"] for i in read(source / "evaluation/evidence_map.json")["evidence"]}
    assert all(set(i["evidence_ids"]) <= evidence for i in kp + conclusions)
    assert all(r["reference_id"] in refs for r in read(source / "evaluation/scoring_rules.json")["rules"])


@pytest.mark.parametrize("paper", PAPERS)
def test_replay_archive_is_real_existing_output_not_a_new_calculation(paper, replays):
    for mode in MODES:
        p = package(mode, paper)
        record = read(repair_record(p))
        assert record["new_quantum_calculations"] is False
        assert record["agent_visible"] is False
        for key, value in replays[paper].items():
            assert_json_close(json.loads(json.dumps(record[key])), json.loads(json.dumps(value)))
        reference = (p / "evaluation/verified_computation_reference.md").read_text()
        assert "Approved boundary repair" in reference
        assert "Historical status" in reference


@pytest.mark.parametrize("mode", MODES)
def test_spinel_host_is_unoptimized_complete_and_has_no_dopant_assignment(mode):
    p = package(mode, PAPERS[0])
    definition = read(p / "agent_input/data/inputs/system_spec.json")
    rows = [line.split() for line in (p / "agent_input/data/inputs/host_initial.cif").read_text().splitlines()]
    rows = [r for r in rows if len(r) == 6 and r[1] in ("Zn", "Al", "O")]
    assert Counter(r[1] for r in rows) == {"Zn": 8, "Al": 16, "O": 32}
    source = ROOT / "docs/verification/group_5" / PAPERS[0] / "provenance/qzcli_hpc/uc1_spinel_relax_u036_retry/1"
    elements, coords, cell = replay.poscar(source / "POSCAR")
    assert [r[1] for r in rows] == ["Al" if e == "Fe" else e for e in elements]
    np.testing.assert_allclose(np.array([r[2:5] for r in rows], dtype=float) @ cell, coords, atol=1e-9)
    _, optimized, _ = replay.poscar(source / "CONTCAR")
    assert not np.allclose(optimized, coords, atol=1e-5)
    assert definition["relaxation_boundary"]["fixed_cell"] is True
    assert definition["electronic_boundary"]["total_cell_charge"] == 0
    assert [s["nominal_ionic_charge_sum"] for s in definition["states"]] == [0, 0, 2]
    assert all(sum(s["element_counts"].values()) == 56 and s["element_counts"]["Fe"] == 1 for s in definition["states"])


def test_spinel_full_shells_are_not_target_nearest_angles():
    states = replay.replay_spinel(full_geometry=True)["states"]
    for state in states:
        assert len(state["geometry"]) == 24
        for center in state["geometry"]:
            n = center["nominal_shell_size"]
            assert len(center["neighbors"]) == n
            assert len(center["angles"]) == n * (n - 1) // 2
            assert all(len(a["endpoint_images"]) == 2 for a in center["angles"])
            assert center["next_neighbor_distance_A"] >= max(a["distance_A"] for a in center["neighbors"])


@pytest.mark.parametrize("paper,extractor", [
    (PAPERS[0], replay.release_spinel_details),
    (PAPERS[1], replay.release_diamine_details),
    (PAPERS[2], replay.release_band_details),
])
def test_release_reconciliation_reextracts_existing_outputs(paper, extractor):
    actual = json.loads(json.dumps(extractor()))
    for mode in MODES:
        recorded = read(repair_record(package(mode, paper)))["release_reconciliation"]
        assert_json_close(actual, recorded)
    if paper == PAPERS[0]:
        for state in actual["states"]:
            assert len({m["host_label"] for m in state["retained_atom_mapping"]}) == 56
            assert sum(len(c["neighbors"]) for c in state["geometry"]) == 128
            assert sum(len(c["angles"]) for c in state["geometry"]) == 288
            assert state["validation"]["maximum_force_norm_eV_A"] < 0.03
    elif paper == PAPERS[1]:
        for molecule in actual["molecules"]:
            assert molecule["mapping_check"]["distance_graph_matches"]
            assert len(molecule["plane_fits"]) == 2
            assert all(0 < plane["rms_residual_A"] < 0.01 for plane in molecule["plane_fits"])
            assert molecule["optimization"]["frequency_validation"]["imaginary_count"] == 0
            assert molecule["multiwfn"]["probes"]["Nminus1"]["charge"] == 1
            assert all(p["same_neutral_geometry"] for p in molecule["multiwfn"]["probes"].values())
    else:
        for crystal in actual["objects"].values():
            assert crystal["candidate_edge"]["leading_group"] == "framework:Pb:p"
            assert crystal["all_lower_band_edges"]
            assert all(r["leading_group"] != "framework:Pb:p" for r in crystal["all_lower_band_edges"])
            assert "cross_mesh_state_identity_not_independently_verified" in crystal["assignment_status"]
            assert not crystal["raw_validation"]["stability_3x3"]["projection_present"]
            assert all(r["electronic_convergence_recorded"] for r in crystal["raw_validation"].values())
            assert "organic:Br:p" in crystal["candidate_edge"]["normalized_component_orbital_groups"] or \
                   any(key.startswith("organic:Cl:") or key.startswith("organic:I:") for key in crystal["candidate_edge"]["normalized_component_orbital_groups"])


@pytest.mark.parametrize("mode", MODES)
def test_diamine_atom_maps_define_real_rings_amines_and_bonded_torsions(mode):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors

    p = package(mode, PAPERS[1])
    molecules = read(p / "agent_input/data/inputs/monomers.json")["molecules"]
    for m in molecules:
        mol = Chem.MolFromSmiles(m["atom_mapped_smiles"])
        assert rdMolDescriptors.CalcMolFormula(mol) == m["formula"]
        lookup = {a.GetAtomMapNum(): a.GetIdx() for a in mol.GetAtoms()}
        assert set(m["amine_atom_map_ids"]) == {a.GetAtomMapNum() for a in mol.GetAtoms() if a.GetSymbol() == "N"}
        if m["id"] == "TMC":
            continue
        ring_sets = {frozenset(mol.GetAtomWithIdx(i).GetAtomMapNum() for i in r) for r in mol.GetRingInfo().AtomRings()}
        assert all(frozenset(r) in ring_sets for r in m["ring_atom_map_ids"])
        for path in m["linker_torsion_atom_map_ids"]:
            assert all(mol.GetBondBetweenAtoms(lookup[a], lookup[b]) for a, b in zip(path, path[1:]))
        if m["id"] == "PFMB":
            assert m["linker_torsion_atom_map_ids"] == [[2, 3, 12, 13]]
            assert mol.GetBondBetweenAtoms(lookup[4], lookup[12]) is None


def diamine_fixture(mode, replays):
    definitions = {m["id"]: m for m in read(package(mode, PAPERS[1]) / "agent_input/data/inputs/monomers.json")["molecules"]}
    rows = []
    for actual in replays[PAPERS[1]]["molecules"]:
        name = actual["molecule_id"]
        rows.append({"id": name, "status": "complete", "charge": 0, "multiplicity": 1,
                     "homo_eV": actual["homo_eV"], "global_nucleophilicity_eV": actual["global_nucleophilicity_eV"],
                     "global_reference_homo_eV": -9.1212, "global_index_convention": "fixed_TCE_B3LYP_reference",
                     "primary_model": "gas_B3LYP_TZVP_on_B3LYP_D3BJ_SVP",
                     "local_descriptors": [{"name": "test fixture", "definition": "shape only", "unit": "e*eV", "evidence": "fixture only",
                                            "site_values": [{"atom_map_id": i, "value": 0.1} for i in definitions[name]["amine_atom_map_ids"]]}],
                     "ring_plane_angle_deg": actual["ring_plane_angle_deg"], "plane_fit_residuals_A": [0, 0],
                     "linker_torsions": actual["linker_torsions"], "geometry_artifact": "fixture.xyz", "atom_mapping": "fixture only",
                     "validation_evidence": "schema fixture, not a real submission", "diagnostics": {}})
    rows.append({"id": "TMC", "status": "context_only", "charge": 0, "multiplicity": 1, "context": "reaction context"})
    return {"status": "complete", "methods": {k: "schema fixture" for k in ("software_or_code", "level_or_model", "charge_multiplicity", "conformer_strategy", "descriptor_definitions")},
            "molecules": rows, "ordering": "fixture", "validation": "fixture", "conclusion": "fixture"}


@pytest.mark.parametrize("mode", MODES)
def test_diamine_schema_separates_indices_enforces_ids_and_allows_diagnostics(mode, replays):
    v = validator(mode, PAPERS[1]); value = diamine_fixture(mode, replays)
    v.validate(value)
    missing = deepcopy(value); del missing["molecules"][0]["global_nucleophilicity_eV"]
    assert list(v.iter_errors(missing))  # a local descriptor cannot fill this field
    duplicate = deepcopy(value); duplicate["molecules"][1] = duplicate["molecules"][0]
    assert list(v.iter_errors(duplicate))
    missing_site = deepcopy(value); missing_site["molecules"][0]["local_descriptors"][0]["site_values"].pop()
    assert list(v.iter_errors(missing_site))
    bounded = deepcopy(value); bounded["status"] = "bounded_failure"; bounded["failure_reason"] = "fixture"
    bounded["molecules"][0] = {"id": "ODA", "charge": 0, "multiplicity": 1, "status": "bounded_failure", "failure_reason": "fixture", "attempted_evidence": "fixture", "scientific_consequence": "fixture"}
    v.validate(bounded)
    bounded["status"] = "complete"
    assert list(v.iter_errors(bounded))


@pytest.mark.parametrize("mode", MODES)
def test_global_numeric_rules_are_identity_specific_and_do_not_score_local_values(mode):
    rules = read(package(mode, PAPERS[1]) / "evaluation/scoring_rules.json")["rules"]
    numeric = [r for r in rules if r["type"] == "numeric"]
    assert sorted(r["target"] for r in numeric) == [3.56, 3.68, 4.26]
    assert {r["tolerance"] for r in numeric} == ({0.7} if mode == "autonomous_research" else {0.5})
    assert all("$.molecules[*].id" in r["binding"]["fields"] for r in numeric)
    assert all("global_nucleophilicity_eV" in json.dumps(r["binding"]) and "descriptor_value" not in json.dumps(r) for r in numeric)


def gap_fixture(gap):
    return {"gap_eV": gap, "minimum_same_k_gap_eV": gap, "vbm_energy_eV": 0, "conduction_edge_energy_eV": gap,
            "vbm_kpoints": [[0.5, 0, 0]], "conduction_edge_kpoints": [[0.5, 0, 0]], "directness": "direct",
            "sampling_scope": "fixture sampled mesh", "spin_treatment": "fixture", "degeneracy_tolerance_eV": 1e-5,
            "band_evidence": "fixture only", "stability": {"setting_change": "fixture", "primary_value_eV": gap,
            "check_value_eV": gap + 0.01, "signed_change_eV": 0.01, "absolute_change_eV": 0.01,
            "same_k_signed_change_eV": 0.01, "same_k_absolute_change_eV": 0.01, "evidence": "fixture"}}


def band_fixture():
    objects = {}
    for name in ("cl_crystal", "br_crystal", "i_crystal"):
        objects[name] = {"object_id": name, "compound": "fixture", "status": "complete", "validation_evidence": "fixture",
                         "orbital_evidence": "fixture", "optical_allowedness": {"status": "not_established", "evidence": "not calculated", "scope": "fixture"},
                         "scalar_relativistic": {"functional": "HSE06", "relativistic_treatment": "scalar_relativistic_without_SOC", "settings": "fixture",
                         "fundamental": {"status": "computed", **gap_fixture(3.1)},
                         "framework_interband": {"assignment_status": "supported", **gap_fixture(4.6),
                         "assignment_criterion": "fixture", "component_atom_mapping": "fixture", "assignment_evidence": "fixture", "lower_candidate_analysis": "fixture"}}}
    return {"objects": objects, "method": {"summary": "fixture", "settings": "fixture", "artifacts": ["fixture"]},
            "validation": {"status": "fixture", "evidence": "fixture", "coverage": "fixture"},
            "structural_comparison": {"descriptor": "fixture", "sign_convention": "fixture", "evidence": "fixture"}, "conclusion": "fixture", "limitations": "fixture"}


@pytest.mark.parametrize("mode", MODES)
def test_band_schema_separates_quantities_soc_and_success_status(mode):
    v = validator(mode, PAPERS[2]); value = band_fixture(); v.validate(value)
    missing = deepcopy(value); del missing["objects"]["cl_crystal"]["scalar_relativistic"]["fundamental"]
    assert list(v.iter_errors(missing))
    wrong_soc = deepcopy(value); wrong_soc["objects"]["cl_crystal"]["scalar_relativistic"]["relativistic_treatment"] = "SOC"
    assert list(v.iter_errors(wrong_soc))
    negative = deepcopy(value); negative["objects"]["cl_crystal"]["scalar_relativistic"]["fundamental"]["stability"]["absolute_change_eV"] = -0.01
    assert list(v.iter_errors(negative))
    unsupported = deepcopy(value); unsupported["objects"]["cl_crystal"]["optical_allowedness"]["status"] = "supported_allowed"
    assert list(v.iter_errors(unsupported))  # requires actual transition definition/evidence
    bounded = deepcopy(value); row = bounded["objects"]["cl_crystal"]
    row["scalar_relativistic"]["framework_interband"] = {"assignment_status": "ambiguous", "assignment_evidence": "fixture", "limitation": "fixture"}
    assert list(v.iter_errors(bounded))
    row.update(status="bounded_failure", failure_reason="fixture", attempted_evidence="fixture", scientific_consequence="fixture")
    v.validate(bounded)


def test_edge_replay_is_not_gamma_test_or_same_k_substitution():
    rows = [{"spin": 1, "band": b, "k": k, "energy_eV": energy, "occupation": occ}
            for k, v, c in [([0, 0, 0], -0.1, 3.0), ([0.5, 0, 0], 0.0, 2.9)]
            for b, energy, occ in [(1, v, 1), (2, c, 0)]]
    direct = replay.summarize_edges(rows, 1)
    assert direct["directness_on_sampled_mesh"] == "direct"
    assert direct["edge_gap_eV"] == pytest.approx(2.9)
    rows[1]["energy_eV"] = 2.8
    indirect = replay.summarize_edges(rows, 1)
    assert indirect["directness_on_sampled_mesh"] == "indirect"
    assert indirect["edge_gap_eV"] == pytest.approx(2.8)
    assert indirect["minimum_same_k_gap_eV"] == pytest.approx(2.9)
    rows[0]["energy_eV"] = 0.0
    # Degenerate VBM contains Gamma even if the first chosen row changes order.
    assert replay.summarize_edges(list(reversed(rows)), 1)["directness_on_sampled_mesh"] == "direct"
    assert replay.k_key([1, -0.5, -1e-15]) == replay.k_key([0, 0.5, 0])


def test_existing_projection_evidence_supports_character_not_optical_claim(replays):
    for label, item in replays[PAPERS[2]]["objects"].items():
        projection = item["component_projection_check"]
        assert len(projection["organic_atom_indices_1based"]) == 48
        assert len(projection["framework_atom_indices_1based"]) == 16
        low = projection["lowest_ten_unoccupied_bands"]
        for band in map(str, range(125, 133)):
            groups = low[band]["minimum_energy_record"]["normalized_element_orbital_groups"]
            assert max(groups, key=groups.get) == "C_p"
        edge = low["133"]["minimum_energy_record"]
        assert max(edge["normalized_element_orbital_groups"], key=edge["normalized_element_orbital_groups"].get) == "Pb_p"
        if label == "I":
            assert edge["normalized_framework_weight"] < 0.5  # mixed, not a hidden majority cutoff
        assert "not optical allowedness" in projection["scope"]
    iodine = replays[PAPERS[2]]["objects"]["I"]["parent_2x2"]["combined_spin_legacy_candidate"]
    assert iodine["edge_gap_eV"] == pytest.approx(4.460078, abs=1e-6)
    assert iodine["minimum_same_k_gap_eV"] == pytest.approx(4.488663, abs=1e-6)


@pytest.mark.parametrize("mode", MODES)
def test_band_targets_bind_only_assigned_scalar_framework_edges(mode):
    p = package(mode, PAPERS[2]); numeric = [r for r in read(p / "evaluation/scoring_rules.json")["rules"] if r["type"] == "numeric"]
    assert sorted(r["target"] for r in numeric) == [4.44, 4.63, 4.64]
    assert all(r["tolerance"] == 0.15 for r in numeric)
    assert all(any(f.endswith(".scalar_relativistic.framework_interband.gap_eV") for f in r["binding"]["fields"]) for r in numeric)
    assert all("not fundamental" in r["binding"]["comparison"] for r in numeric)
    public = (p / "agent_input/task.md").read_text() + (p / "agent_input/data/inputs/electronic_observables.json").read_text()
    assert all(token not in public for token in ("4.63", "4.64", "4.44", "band 133", "band 125"))


@pytest.mark.parametrize("paper", PAPERS)
def test_input_data_equal_across_modes_but_author_guidance_only_in_pr(paper):
    ar, pr = (package(mode, paper) for mode in MODES)
    for path in (ar / "agent_input/data").rglob("*"):
        if path.is_file():
            assert path.read_bytes() == (pr / path.relative_to(ar)).read_bytes()
    assert "# Author-provided scientific guidance" not in (ar / "agent_input/task.md").read_text()
    assert "# Author-provided scientific guidance" in (pr / "agent_input/task.md").read_text()

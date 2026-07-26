import hashlib
import json
from pathlib import Path

from evaluation.config import TASKS_DIR
from evaluation.utils import list_tasks, load_ground_truth, load_task_info


TASK_IDS = [
    "GEOM_Hierarchical_Conformer_Reranking_Reproduction",
    "Electron_Flexible_Ensemble_Surface_Reproduction",
    "PV_Protonation_Barrier_Trend_Reproduction",
    "BaO_Phase_Crossover_And_5d_Bonding_Reproduction",
    "PV_CC_CO_Pathway_Selectivity_Reproduction",
    "NHC_Adsorption_Decomposition_Bonding_Reproduction",
]


def test_multisoftware_reproduction_tasks_are_complete_and_hashed():
    available = set(list_tasks())
    for task_id in TASK_IDS:
        assert "Reproduction" in task_id
        assert task_id in available
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        data_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        manifest_path = data_root / "input_manifest.json"
        assert info["task_id"] == task_id
        assert info["task_mode"] == "guided_reproduction"
        assert info["scientific_mode"] == "guided_reproduction"
        assert info["method_disclosure"] == "paper_reconstructed_protocol"
        assert info["required_deliverables"]
        assert truth["evaluation_profile"] == "paper_reproduction"
        assert truth["evaluation_mode"] == "rubric_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        rubric = {item["id"]: item for item in truth["scoring_rubric"]}
        assert rubric["paper_conclusion_agreement"]["max_score"] == 55
        assert truth["reference_conclusion_gate_policy"]["required"] is True
        assert truth["expected_structured_output"] == [
            item["path"] for item in info["required_deliverables"]
        ]
        assert data_root.is_dir()
        assert manifest_path.is_file()
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        assert not any(
            path.suffix.casefold()
            in {".zip", ".log", ".out", ".gbw", ".wfn", ".wfx", ".wavecar"}
            for path in data_root.rglob("*")
            if path.is_file()
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["task_id"] == task_id
        assert manifest["paper_result_values_in_visible_inputs"] == 0
        assert manifest["completed_quantum_outputs"] == 0
        assert manifest["software_stage_count"] >= 4
        assert truth["reference_evidence"]["input_manifest_sha256"] == hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        for record in manifest["files"]:
            path = data_root / record["path"]
            assert path.is_file()
            assert path.stat().st_size == record["size_bytes"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


def test_hidden_numerical_targets_are_not_visible():
    hidden_markers = {
        "GEOM_Hierarchical_Conformer_Reranking_Reproduction": [
            "26.50143932748048",
            '"reference_major_conformer_count": 7',
        ],
        "Electron_Flexible_Ensemble_Surface_Reproduction": [
            "157.1994",
            "159.8",
            "149.2",
        ],
        "PV_Protonation_Barrier_Trend_Reproduction": [
            '"P0": 30',
            '"P1": 20',
            '"P2": 14',
        ],
        "BaO_Phase_Crossover_And_5d_Bonding_Reproduction": [
            '"paper_transition_pressures_gpa"',
            "5.13",
            "3.35",
        ],
        "PV_CC_CO_Pathway_Selectivity_Reproduction": [
            '"paper_cc_barrier_kcal_mol"',
            '"paper_co_barrier_kcal_mol"',
        ],
        "NHC_Adsorption_Decomposition_Bonding_Reproduction": [
            "-3.349",
            "-2.441",
            '"binding_energy_kcal_mol"',
        ],
    }
    for task_id, markers in hidden_markers.items():
        task_root = TASKS_DIR / task_id
        data_root = task_root / "data" / "benchmark_data"
        visible = json.dumps(load_task_info(task_id), ensure_ascii=False) + "\n"
        visible += "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in data_root.rglob("*")
            if path.is_file()
            and path.suffix.casefold() in {".json", ".md", ".txt", ".csv"}
        )
        for marker in markers:
            assert marker not in visible


def test_task_specific_input_contracts():
    geom = json.loads(
        (
            TASKS_DIR
            / TASK_IDS[0]
            / "data/benchmark_data/molecular_systems.json"
        ).read_text(encoding="utf-8")
    )
    assert list(geom["systems"]) == ["GEOM-C3"]
    geom_truth = load_ground_truth(TASK_IDS[0])["expected_result"]
    assert "reference_xtb_top_conformer_index" not in geom_truth
    assert "reference_free_energy_top_conformer_index" not in geom_truth
    assert geom_truth["scoped_acceptance_target"]["exact_file_order_index_required"] is False

    electron_root = TASKS_DIR / TASK_IDS[1] / "data/benchmark_data"
    assert len(list(electron_root.glob("published_conformers/ISO-M6/*.xyz"))) == 25
    electron_truth = load_ground_truth(TASK_IDS[1])["expected_result"]
    assert electron_truth["scoped_acceptance_target"]["exact_full_25_conformer_aggregate_required"] is False

    pv_protonation = json.loads(
        (
            TASKS_DIR
            / TASK_IDS[2]
            / "data/benchmark_data/candidate_manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert pv_protonation["candidate_count"] == 66
    assert {item["system"] for item in pv_protonation["candidates"]} == {
        "P0",
        "P1",
        "P2",
    }

    bao = json.loads(
        (
            TASKS_DIR
            / TASK_IDS[3]
            / "data/benchmark_data/phase_volume_grid.json"
        ).read_text(encoding="utf-8")
    )
    assert bao["phases"] == ["B1", "B8", "dB2"]
    assert len(bao["structures"]) == 15

    pv_selectivity = json.loads(
        (
            TASKS_DIR
            / TASK_IDS[4]
            / "data/benchmark_data/candidate_manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert pv_selectivity["candidate_count"] == 24
    assert {item["system"] for item in pv_selectivity["candidates"]} == {"P2"}

    nhc = json.loads(
        (
            TASKS_DIR
            / TASK_IDS[5]
            / "data/benchmark_data/system_manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert set(nhc["systems"]) == {"NHC1", "NHC4"}
    assert nhc["systems"]["NHC1"]["metal_atom_count"] == 48
    assert nhc["systems"]["NHC4"]["metal_atom_count"] == 36
    assert nhc["systems"]["NHC1"]["adsorbate_atom_count"] == 9
    assert nhc["systems"]["NHC4"]["adsorbate_atom_count"] == 15


def test_multisoftware_protocols_name_multiple_backends():
    for task_id in TASK_IDS:
        protocol_path = (
            TASKS_DIR / task_id / "data/benchmark_data/computational_protocol.json"
        )
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        assert protocol["result_values_included"] is False
        assert len(protocol["software_dag"]) >= 4

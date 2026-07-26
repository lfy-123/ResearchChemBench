import hashlib
import json
import re
from pathlib import Path

from evaluation.config import TASKS_DIR
from evaluation.utils import list_tasks, load_ground_truth, load_task_info


TASK_IDS = [
    "GEOM_Hierarchical_Conformer_Reranking",
    "Electron_Flexible_Ensemble_Surface",
    "PV_Protonation_Barrier_Trend",
    "BaO_Phase_Crossover_And_5d_Bonding",
    "PV_CC_CO_Pathway_Selectivity",
    "NHC_Adsorption_Decomposition_Bonding",
]

REPRO_IDS = [f"{task_id}_Reproduction" for task_id in TASK_IDS]


def visible_text(task_id: str) -> str:
    root = TASKS_DIR / task_id
    text = json.dumps(load_task_info(task_id), ensure_ascii=False) + "\n"
    for path in (root / "data" / "benchmark_data").rglob("*"):
        if path.is_file():
            text += path.read_text(encoding="utf-8", errors="ignore") + "\n"
    return text


def test_autonomous_tasks_are_complete_paired_and_hashed():
    available = set(list_tasks())
    for task_id, repro_id in zip(TASK_IDS, REPRO_IDS, strict=True):
        assert task_id in available
        assert repro_id in available
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        data_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        manifest_path = data_root / "input_manifest.json"

        assert info["task_id"] == task_id
        assert info["task_mode"] == "open_discovery"
        assert info["scientific_mode"] == "focused_open_discovery"
        assert info["method_disclosure"] == "none"
        assert info["pathway_disclosure"] == "none"
        assert info["required_deliverables"]
        assert truth["evaluation_profile"] == "autonomous_discovery"
        assert truth["evaluation_mode"] == "rubric_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        assert truth["reference_conclusion_gate_policy"] == {}
        assert truth["reference_evidence"]["paired_reproduction_task_id"] == repro_id
        assert truth["expected_structured_output"] == [
            item["path"] for item in info["required_deliverables"]
        ]

        assert data_root.is_dir()
        assert manifest_path.is_file()
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        assert not (data_root / "computational_protocol.json").exists()
        assert not (data_root / "workflow_requirements.json").exists()
        assert not any(
            path.suffix.casefold()
            in {".zip", ".log", ".out", ".gbw", ".wfn", ".wfx", ".wavecar"}
            for path in data_root.rglob("*")
            if path.is_file()
        )

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["task_id"] == task_id
        assert "paired_reproduction_task_id" not in manifest
        assert manifest["task_mode"] == "open_discovery"
        assert manifest["method_disclosure"] == "none"
        assert manifest["pathway_disclosure"] == "none"
        assert manifest["paper_result_values_in_visible_inputs"] == 0
        assert manifest["paper_protocol_files_in_visible_inputs"] == 0
        assert manifest["author_stationary_points_in_visible_inputs"] == 0
        assert manifest["completed_quantum_outputs"] == 0
        assert truth["reference_evidence"]["input_manifest_sha256"] == hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        for record in manifest["files"]:
            path = data_root / record["path"]
            assert path.is_file()
            assert path.stat().st_size == record["size_bytes"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


def test_visible_inputs_do_not_disclose_paper_route_or_targets():
    prohibited_literals = [
        "_Reproduction",
        "ORCA",
        "CREST",
        "LOBSTER",
        "GoodVibes",
        "RDKit",
        "ETKDG",
        "GFN2-xTB",
        "r2SCAN-3c",
        "DLPNO",
        "Gaussian",
        "Multiwfn",
        "0.0016",
        "157.1994",
        "26.50143932748048",
        "paper_cc_barrier_kcal_mol",
        "paper_transition_pressures_gpa",
        "published_adsorbed_start",
    ]
    doi_pattern = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
    for task_id in TASK_IDS:
        text = visible_text(task_id)
        assert not doi_pattern.search(text)
        for marker in prohibited_literals:
            assert marker not in text


def test_task_specific_autonomous_input_contracts():
    geom_root = TASKS_DIR / TASK_IDS[0] / "data" / "benchmark_data"
    geom = json.loads((geom_root / "molecular_systems.json").read_text(encoding="utf-8"))
    assert list(geom["systems"]) == ["GEOM-C3"]
    assert not list(geom_root.rglob("*.xyz"))

    electron_root = TASKS_DIR / TASK_IDS[1] / "data" / "benchmark_data"
    electron = json.loads((electron_root / "molecular_systems.json").read_text(encoding="utf-8"))
    assert list(electron["systems"]) == ["ISO-M6"]
    assert electron["systems"]["ISO-M6"]["experimental_te_surface_angstrom2"] == 156.507
    assert not list(electron_root.rglob("*.xyz"))

    protonation_root = TASKS_DIR / TASK_IDS[2] / "data" / "benchmark_data"
    protonation_xyz = sorted(protonation_root.glob("initial_structures/*/*.xyz"))
    assert len(protonation_xyz) == 9
    assert {path.parent.name for path in protonation_xyz} == {"P0", "P1", "P2"}
    assert all("geometry_status=unoptimized" in path.read_text(encoding="utf-8").splitlines()[1] for path in protonation_xyz)
    assert not (protonation_root / "candidate_manifest.json").exists()

    bao_root = TASKS_DIR / TASK_IDS[3] / "data" / "benchmark_data"
    phase_manifest = json.loads((bao_root / "candidate_phase_manifest.json").read_text(encoding="utf-8"))
    assert phase_manifest["phase_labels_are_opaque"] is True
    assert phase_manifest["investigation_pressure_range_gpa"] == [0.0, 80.0]
    assert len(list(bao_root.glob("candidate_phases/*.vasp"))) == 3
    assert not (bao_root / "phase_volume_grid.json").exists()
    assert all(
        path.read_text(encoding="utf-8").splitlines()[0].startswith("BaO opaque candidate phase_")
        for path in bao_root.glob("candidate_phases/*.vasp")
    )

    selectivity_root = TASKS_DIR / TASK_IDS[4] / "data" / "benchmark_data"
    selectivity_xyz = sorted(selectivity_root.glob("initial_structures/P2/*.xyz"))
    measurements = json.loads(
        (selectivity_root / "experimental_measurements" / "measurements.json").read_text(encoding="utf-8")
    )
    assert len(selectivity_xyz) == 3
    assert len(measurements["measurements"]) == 4
    assert not (selectivity_root / "candidate_manifest.json").exists()

    nhc_root = TASKS_DIR / TASK_IDS[5] / "data" / "benchmark_data"
    nhc = json.loads((nhc_root / "system_manifest.json").read_text(encoding="utf-8"))
    assert set(nhc["systems"]) == {"NHC1", "NHC4"}
    assert nhc["adsorption_structures_supplied"] == 0
    assert len(list(nhc_root.glob("clean_surfaces/*.vasp"))) == 2
    assert len(list(nhc_root.glob("ligand_seeds/*.xyz"))) == 2
    assert not (nhc_root / "adsorbed_structures").exists()


def test_release_status_matches_known_toolbox_boundaries():
    statuses = {
        task_id: load_ground_truth(task_id)["current_toolbox_feasibility_baseline"]["status"]
        for task_id in TASK_IDS
    }
    assert statuses[TASK_IDS[0]] == "pre_release_pilot_ready"
    assert statuses[TASK_IDS[1]] == "pre_release_pilot_ready"
    assert statuses[TASK_IDS[2]] == "pre_release_blocked"
    assert statuses[TASK_IDS[3]] == "pre_release_split_recommended"
    assert statuses[TASK_IDS[4]] == "pre_release_blocked"
    assert statuses[TASK_IDS[5]] == "pre_release_blocked"

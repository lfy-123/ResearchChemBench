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
RAW_OUTPUT_AUTONOMOUS_TASKS = {"PV_Protonation_Barrier_Trend"}
TEXT_SUFFIXES = {".json", ".md", ".txt", ".csv"}


def visible_text(task_id: str) -> str:
    root = TASKS_DIR / task_id
    text = json.dumps(load_task_info(task_id), ensure_ascii=False) + "\n"
    for path in (root / "data" / "benchmark_data").rglob("*"):
        if path.is_file() and path.suffix.casefold() in TEXT_SUFFIXES:
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
        assert any(
            "server resources allow" in item
            for item in info["scientific_requirements"]
        )
        assert truth["evaluation_profile"] == "autonomous_discovery"
        assert truth["evaluation_mode"] == "dual_axis_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        rubric = {item["id"]: item["max_score"] for item in truth["scoring_rubric"]}
        assert rubric["problem_framing_and_route_design"] == 20
        assert rubric["resource_and_search_efficiency"] == 10
        assert len(truth["scientific_conclusion_rubric"]) == 3
        assert sum(
            item["max_score"]
            for item in truth["scientific_conclusion_rubric"]
        ) == 100
        assert truth["reference_conclusion_gate_policy"] == {}
        assert truth["evidence_gate_policy"] == {}
        assert truth["expected_result"]["scientific_acceptance_contract"][
            "required_findings"
        ]
        assert truth["reference_evidence"]["paired_reproduction_task_id"] == repro_id
        assert truth["expected_structured_output"] == [
            item["path"] for item in info["required_deliverables"]
        ]

        assert data_root.is_dir()
        assert manifest_path.is_file()
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        assert not (data_root / "computational_protocol.json").exists()
        assert not (data_root / "workflow_requirements.json").exists()
        forbidden_suffixes = {".log", ".out", ".gbw", ".wfn", ".wfx", ".wavecar"}
        if task_id not in RAW_OUTPUT_AUTONOMOUS_TASKS:
            forbidden_suffixes.add(".zip")
        assert not any(
            path.suffix.casefold() in forbidden_suffixes
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
        if task_id in RAW_OUTPUT_AUTONOMOUS_TASKS:
            assert info["archive_extractions"]
            assert manifest["author_stationary_points_in_visible_inputs"] == "contained_in_author_archives"
            assert manifest["completed_quantum_outputs"] == "official_author_archives"
        else:
            assert info["archive_extractions"] == []
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


def test_dual_axis_autonomous_tasks_have_multiple_hidden_paper_claims():
    expected_claim_ids = {
        "GEOM_Hierarchical_Conformer_Reranking": {
            "major_basin_coverage",
            "quantum_ranking_reorder",
            "thermochemical_population_change",
        },
        "Electron_Flexible_Ensemble_Surface": {
            "conformer_surface_variation",
            "thermal_ensemble_reduces_single_structure_bias",
            "blind_surface_prediction_scale",
        },
        "PV_Protonation_Barrier_Trend": {
            "successive_protonation_barrier_order",
            "stepwise_barrier_reduction_scale",
            "exergonic_profiles_distinct_from_kinetic_trend",
        },
        "BaO_Phase_Crossover_And_5d_Bonding": {
            "bao_phase_sequence",
            "bao_first_transition_pressure",
            "bao_second_transition_pressure",
        },
        "PV_CC_CO_Pathway_Selectivity": {
            "two_valid_competing_paths",
            "cc_kinetic_preference",
            "co_accessible_minor_path",
        },
        "NHC_Adsorption_Decomposition_Bonding": {
            "nhc_adsorption_order_and_scale",
            "nhc_local_pd_c_bonding_order",
            "nhc_deformation_moderates_total_binding",
        },
    }
    for task_id, expected_ids in expected_claim_ids.items():
        truth = load_ground_truth(task_id)
        assert {
            item["id"] for item in truth["scientific_conclusion_rubric"]
        } == expected_ids


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
        "156.507",
        "26.50143932748048",
        "paper_cc_barrier_kcal_mol",
        "paper_transition_pressures_gpa",
        "published_adsorbed_start",
    ]
    doi_pattern = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
    for task_id in TASK_IDS:
        text = visible_text(task_id)
        if task_id not in RAW_OUTPUT_AUTONOMOUS_TASKS:
            assert not doi_pattern.search(text)
        for marker in prohibited_literals:
            if task_id in RAW_OUTPUT_AUTONOMOUS_TASKS and marker in {
                "ORCA",
                "Gaussian",
            }:
                continue
            assert marker not in text


def test_task_specific_autonomous_input_contracts():
    geom_root = TASKS_DIR / TASK_IDS[0] / "data" / "benchmark_data"
    geom = json.loads((geom_root / "molecular_systems.json").read_text(encoding="utf-8"))
    assert list(geom["systems"]) == ["GEOM-C3"]
    assert not list(geom_root.rglob("*.xyz"))

    electron_root = TASKS_DIR / TASK_IDS[1] / "data" / "benchmark_data"
    electron = json.loads((electron_root / "molecular_systems.json").read_text(encoding="utf-8"))
    assert list(electron["systems"]) == ["ISO-M6"]
    assert "experimental_te_surface_angstrom2" not in electron["systems"]["ISO-M6"]
    electron_manifest = json.loads((electron_root / "input_manifest.json").read_text(encoding="utf-8"))
    assert electron_manifest["visible_experimental_measurement_count"] == 0
    assert not list(electron_root.rglob("*.xyz"))

    protonation_root = TASKS_DIR / TASK_IDS[2] / "data" / "benchmark_data"
    protonation = json.loads(
        (protonation_root / "candidate_manifest.json").read_text(encoding="utf-8")
    )
    assert protonation["candidate_count"] == 66
    assert {item["system"] for item in protonation["candidates"]} == {"P0", "P1", "P2"}
    assert len(list(protonation_root.glob("author_outputs/*.zip"))) == 3
    assert not (protonation_root / "initial_structures").exists()

    bao_root = TASKS_DIR / TASK_IDS[3] / "data" / "benchmark_data"
    phase_manifest = json.loads((bao_root / "phase_volume_grid.json").read_text(encoding="utf-8"))
    assert phase_manifest["phases"] == ["B1", "B8", "dB2"]
    assert len(phase_manifest["structures"]) == 15
    assert len(list(bao_root.glob("volume_structures/**/*.vasp"))) == 15
    assert not (bao_root / "candidate_phase_manifest.json").exists()

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
    assert statuses[TASK_IDS[2]] == "validated_for_evaluation"
    assert statuses[TASK_IDS[3]] == "validated_for_evaluation"
    assert statuses[TASK_IDS[4]] == "pre_release_blocked"
    assert statuses[TASK_IDS[5]] == "pre_release_native_oracle_required"


def test_validated_dual_track_pairs_share_data_and_scientific_targets():
    guided_only = {
        "computational_protocol.json",
        "workflow_requirements.json",
        "reaction_definitions.json",
    }
    for task_id in ("PV_Protonation_Barrier_Trend", "BaO_Phase_Crossover_And_5d_Bonding"):
        repro_id = f"{task_id}_Reproduction"
        open_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        repro_root = TASKS_DIR / repro_id / "data" / "benchmark_data"

        def shared_hashes(root: Path) -> dict[str, str]:
            return {
                path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in root.rglob("*")
                if path.is_file()
                and path.name not in {"README.md", "input_manifest.json"}
                and path.name not in guided_only
            }

        assert shared_hashes(open_root) == shared_hashes(repro_root)
        assert load_task_info(task_id)["required_deliverables"] == load_task_info(repro_id)["required_deliverables"]
        open_rubric = load_ground_truth(task_id)["scientific_conclusion_rubric"]
        repro_rubric = load_ground_truth(repro_id)["scientific_conclusion_rubric"]
        assert [(item["id"], item["max_score"]) for item in open_rubric] == [
            (item["id"], item["max_score"]) for item in repro_rubric
        ]

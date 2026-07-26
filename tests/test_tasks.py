import hashlib
import json
import re
from pathlib import Path

from evaluation.config import TASKS_DIR
from evaluation.run_task import TaskRunner
from evaluation.utils import list_tasks, load_ground_truth, load_task_info


def test_all_chemgraph_tasks_were_imported():
    tasks = list_tasks()
    chemgraph_tasks = [task for task in tasks if task.startswith("ChemGraph_")]
    assert len(chemgraph_tasks) == 40
    assert chemgraph_tasks[0] == "ChemGraph_001"
    assert chemgraph_tasks[-1] == "ChemGraph_040"


def test_heterobiaryl_dual_track_tasks_use_complete_100_point_rubrics():
    all_heterobiaryl = [task for task in list_tasks() if task.startswith("Heterobiaryl_PV_")]
    open_tasks = [task for task in all_heterobiaryl if "_Reproduction_" not in task]
    reproduction_tasks = [task for task in all_heterobiaryl if "_Reproduction_" in task]
    assert open_tasks == [
        "Heterobiaryl_PV_01_Protonation",
        "Heterobiaryl_PV_02_CC_Selectivity",
        "Heterobiaryl_PV_03_CC_vs_CO",
        "Heterobiaryl_PV_04_Coupling_Mechanism",
        "Heterobiaryl_PV_05_Rate_Determining_Step",
        "Heterobiaryl_PV_06_End_to_End",
    ]
    assert reproduction_tasks == [
        "Heterobiaryl_PV_Reproduction_01_Protonation",
        "Heterobiaryl_PV_Reproduction_02_CC_Selectivity",
        "Heterobiaryl_PV_Reproduction_03_CC_vs_CO",
        "Heterobiaryl_PV_Reproduction_04_Coupling_Mechanism",
        "Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step",
        "Heterobiaryl_PV_Reproduction_06_End_to_End",
    ]
    forbidden_open_terms = {
        "gaussian",
        "orca",
        "goodvibes",
        "xtb",
        "wb97xd",
        "dlpno",
        "growing string",
        "freezing string",
        "10.1126/science.aas8961",
        "ts-i",
        "int-iii",
    }
    input_contracts = {
        "Heterobiaryl_PV_01_Protonation": (["P0", "P1", "P2"], []),
        "Heterobiaryl_PV_02_CC_Selectivity": (["P0", "P1", "P2"], []),
        "Heterobiaryl_PV_03_CC_vs_CO": (["P2"], ["E02", "E10", "E11", "E12"]),
        "Heterobiaryl_PV_04_Coupling_Mechanism": (["P0", "P1", "P2"], []),
        "Heterobiaryl_PV_05_Rate_Determining_Step": (
            ["P2"],
            ["E01", "E02", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12"],
        ),
        "Heterobiaryl_PV_06_End_to_End": (
            ["P0", "P1", "P2"],
            ["E01", "E02", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12"],
        ),
    }
    shared_seed_hashes = {}
    for task_id in open_tasks:
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        visible_protocol = json.dumps(
            {
                "task": info["task"],
                "scientific_mode": info["scientific_mode"],
                "scientific_mode_description": info[
                    "scientific_mode_description"
                ],
                "scientific_requirements": info["scientific_requirements"],
                "required_deliverables": info["required_deliverables"],
            },
            ensure_ascii=False,
        ).casefold()
        data_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        visible_text = visible_protocol + "\n" + "\n".join(
            path.read_text(encoding="utf-8", errors="ignore").casefold()
            for path in data_root.rglob("*")
            if path.is_file() and path.suffix.casefold() in {".json", ".md", ".txt"}
        )
        for term in forbidden_open_terms:
            assert term not in visible_text
        assert info["benchmark_family"] == "heterobiaryl_pv"
        assert info["task_mode"] == "open_discovery"
        assert info["method_disclosure"] == "none"
        assert info["pathway_disclosure"] == "none"
        assert not (data_root / "computational_protocol.json").exists()
        assert not (data_root / "reaction_definitions.json").exists()
        assert not (data_root / "workflow_requirements.json").exists()
        assert truth["evaluation_mode"] == "rubric_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        assert info["archive_extractions"] == []
        assert data_root.is_dir()
        assert not data_root.is_symlink()
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        assert not any(path.suffix.casefold() == ".zip" for path in data_root.rglob("*"))
        manifest = json.loads(
            (data_root / "input_manifest.json").read_text(encoding="utf-8")
        )
        expected_states, expected_measurement_ids = input_contracts[task_id]
        expected_seed_count = 3 * len(expected_states)
        assert manifest["unoptimized_seed_count"] == expected_seed_count
        assert manifest["states"] == expected_states
        assert manifest["measurement_ids"] == expected_measurement_ids
        assert len(list(data_root.glob("initial_structures/*/*.xyz"))) == expected_seed_count
        assert manifest["completed_computational_outputs"] == 0
        assert manifest["optimized_stationary_points"] == 0
        assert manifest["transition_states"] == 0
        assert manifest["reaction_path_outputs"] == 0
        assert manifest["reference_answers"] == 0
        for record in manifest["files"]:
            path = data_root / record["path"]
            assert path.stat().st_size == record["size_bytes"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        manifest_sha = hashlib.sha256(
            (data_root / "input_manifest.json").read_bytes()
        ).hexdigest()
        assert truth["reference_evidence"]["input_manifest_sha256"] == manifest_sha
        systems = json.loads(
            (data_root / "molecular_systems.json").read_text(encoding="utf-8")
        )["systems"]
        expected_system_values = {
            "P0": (48, 0, "C23H21N2OP"),
            "P1": (49, 1, "C23H22N2OP"),
            "P2": (50, 2, "C23H23N2OP"),
        }
        for state in expected_states:
            atom_count, charge, formula = expected_system_values[state]
            assert systems[state]["atom_count"] == atom_count
            assert systems[state]["charge"] == charge
            assert systems[state]["multiplicity"] == 1
            assert systems[state]["formula"] == formula
        for record in manifest["seed_records"]:
            previous = shared_seed_hashes.setdefault(record["seed_id"], record["sha256"])
            assert record["sha256"] == previous
        measurement_path = data_root / "experimental_measurements" / "measurements.json"
        assert not (data_root / "experimental_measurements" / "measurements.csv").exists()
        if expected_measurement_ids:
            measurements = json.loads(measurement_path.read_text(encoding="utf-8"))
            assert [item["measurement_id"] for item in measurements["measurements"]] == expected_measurement_ids
        else:
            assert not measurement_path.exists()
        assert truth["evidence_gate_policy"]["judge_must_assess_all"] is True
        assert truth["evidence_gate_policy"]["gates"]
        expected_paths = [item["path"] for item in info["required_deliverables"]]
        assert truth["expected_structured_output"] == expected_paths

    for task_id in open_tasks[:5]:
        assert load_task_info(task_id)["scientific_mode"] == "focused_open_discovery"
    q6 = load_task_info(open_tasks[5])
    assert q6["scientific_mode"] == "independent_open_discovery"
    assert len(q6["scientific_requirements"]) >= 7
    assert {item["path"] for item in q6["required_deliverables"]} == {
        "report/research_plan.json",
        "report/stationary_points.csv",
        "report/energy_profile.csv",
        "report/mechanism_evidence.json",
        "report/failure_log.jsonl",
        "report/final_answer.json",
        "report/report.md",
    }

    open_by_suffix = {task.split("Heterobiaryl_PV_", 1)[1]: task for task in open_tasks}
    for task_id in reproduction_tasks:
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        assert info["benchmark_family"] == "heterobiaryl_pv"
        assert info["task_mode"] == "guided_reproduction"
        assert info["scientific_mode"] == "guided_reproduction"
        assert info["method_disclosure"] == "paper_reconstructed_protocol"
        assert info["pathway_disclosure"] == "mapped_candidate_routes"
        assert truth["evaluation_mode"] == "rubric_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        assert truth["reference_evidence"]["task_mode"] == "guided_reproduction"
        baseline = truth["current_toolbox_reproduction_baseline"]
        assert baseline["status"] == "assessed_post_repair"
        assert baseline["classification"] in {
            "solvable",
            "partially_solvable",
            "not_solvable",
        }
        assert baseline["major_paper_conclusion_reproduced_in_this_audit"] is False
        assert baseline["unresolved_requirements"]
        data_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        protocol_path = data_root / "computational_protocol.json"
        paths_path = data_root / "reaction_definitions.json"
        workflow_path = data_root / "workflow_requirements.json"
        assert protocol_path.is_file()
        assert paths_path.is_file()
        assert workflow_path.is_file()
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        definitions = json.loads(paths_path.read_text(encoding="utf-8"))
        assert protocol["geometry_and_frequency"]["reference_method"] == "wB97XD"
        assert protocol["high_level_single_points"]["method"] == "DLPNO-CCSD(T)"
        assert protocol["mechanism_analysis"]["nbo_required"] is False
        assert definitions["result_values_included"] is False
        assert definitions["author_coordinates_included"] is False
        assert definitions["paths"]
        assert not any(path.suffix.casefold() in {".log", ".out", ".zip"} for path in data_root.rglob("*"))
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        manifest_path = data_root / "input_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["task_mode"] == "guided_reproduction"
        assert manifest["published_numerical_results"] == 0
        assert manifest["author_coordinates"] == 0
        assert truth["reference_evidence"]["input_manifest_sha256"] == hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        for record in manifest["files"]:
            path = data_root / record["path"]
            assert path.stat().st_size == record["size_bytes"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        visible_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore").casefold()
            for path in data_root.rglob("*")
            if path.is_file() and path.suffix.casefold() in {".json", ".md", ".txt"}
        )
        for leaked_result in (
            "bipy_dg_dagger",
            "phpy_dg_dagger",
            "delta_delta_g_dagger",
            "paper_published_target",
            "correct barrier",
            "reference barrier",
        ):
            assert leaked_result not in visible_text
        suffix = task_id.split("Heterobiaryl_PV_Reproduction_", 1)[1]
        open_id = open_by_suffix[suffix]
        open_root = TASKS_DIR / open_id / "data" / "benchmark_data"
        for xyz in data_root.glob("initial_structures/*/*.xyz"):
            assert hashlib.sha256(xyz.read_bytes()).hexdigest() == hashlib.sha256(
                (open_root / xyz.relative_to(data_root)).read_bytes()
            ).hexdigest()


def test_electron_isodensity_dual_track_tasks_are_decontaminated_and_complete():
    open_tasks = [
        "Electron_Isodensity_01_Method_Selection",
        "Electron_Isodensity_02_Conformer_Effects",
        "Electron_Isodensity_03_Cutoff_Calibration",
        "Electron_Isodensity_04_Blind_Prediction",
        "Electron_Isodensity_05_End_to_End",
    ]
    reproduction_tasks = [
        "Electron_Isodensity_Reproduction_01_Method_Selection",
        "Electron_Isodensity_Reproduction_02_Conformer_Effects",
        "Electron_Isodensity_Reproduction_03_Cutoff_Calibration",
        "Electron_Isodensity_Reproduction_04_Blind_Prediction",
        "Electron_Isodensity_Reproduction_05_End_to_End",
    ]
    assert [task for task in list_tasks() if task.startswith("Electron_Isodensity_")] == [
        open_tasks[0],
        open_tasks[1],
        open_tasks[2],
        open_tasks[3],
        open_tasks[4],
        reproduction_tasks[0],
        reproduction_tasks[1],
        reproduction_tasks[2],
        reproduction_tasks[3],
        reproduction_tasks[4],
    ]

    molecule_contracts = {
        "01_Method_Selection": (["ISO-M1", "ISO-M2", "ISO-M3"], [], 3),
        "02_Conformer_Effects": (["ISO-M5", "ISO-M6"], ["TE-ISO-M5", "TE-ISO-M6"], 28),
        "03_Cutoff_Calibration": (
            ["ISO-M1", "ISO-M2", "ISO-M3", "ISO-M5", "ISO-M6", "ISO-M7"],
            ["TE-ISO-M1", "TE-ISO-M2", "TE-ISO-M3", "TE-ISO-M5", "TE-ISO-M6", "TE-ISO-M7"],
            34,
        ),
        "04_Blind_Prediction": (
            ["ISO-M1", "ISO-M2", "ISO-M3", "ISO-M4"],
            ["TE-ISO-M1", "TE-ISO-M2", "TE-ISO-M3"],
            4,
        ),
        "05_End_to_End": (
            ["ISO-M1", "ISO-M2", "ISO-M3", "ISO-M4", "ISO-M5", "ISO-M6", "ISO-M7"],
            ["TE-ISO-M1", "TE-ISO-M2", "TE-ISO-M3", "TE-ISO-M5", "TE-ISO-M6", "TE-ISO-M7"],
            35,
        ),
    }
    forbidden_open_terms = {
        "orca",
        "multiwfn",
        "crest",
        "xtb",
        "pbe",
        "b3lyp",
        "dsd-pbep86",
        "ccsd",
        "def2",
        "marching tetrahedra",
        "0.0016",
        "0.0008",
        "0.0025",
        "10.1038/s41467-024-50408-8",
    }
    formula_contract = {
        "ISO-M1": ("C2H6", 8),
        "ISO-M2": ("C4H4O", 9),
        "ISO-M3": ("C5H5N", 11),
        "ISO-M4": ("C4H8O", 13),
        "ISO-M5": ("C4H8O2", 14),
        "ISO-M6": ("C5H12S", 18),
        "ISO-M7": ("C6H10O", 17),
    }

    for task_id in open_tasks:
        suffix = task_id.split("Electron_Isodensity_", 1)[1]
        expected_molecules, expected_measurements, _ = molecule_contracts[suffix]
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        data_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        assert info["benchmark_family"] == "electron_isodensity_surface"
        assert info["task_mode"] == "open_discovery"
        assert info["method_disclosure"] == "none"
        assert info["pathway_disclosure"] == "none"
        assert info["archive_extractions"] == []
        assert truth["evaluation_mode"] == (
            "dual_axis_100" if suffix == "04_Blind_Prediction" else "rubric_100"
        )
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        if suffix == "04_Blind_Prediction":
            assert len(truth["scientific_conclusion_rubric"]) == 3
            assert sum(
                item["max_score"]
                for item in truth["scientific_conclusion_rubric"]
            ) == 100
        assert truth["expected_structured_output"] == [
            item["path"] for item in info["required_deliverables"]
        ]
        assert not (data_root / "computational_protocol.json").exists()
        assert not (data_root / "workflow_requirements.json").exists()
        assert not (data_root / "initial_structures").exists()
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        assert not any(path.suffix.casefold() == ".zip" for path in data_root.rglob("*"))
        visible_text = json.dumps(info, ensure_ascii=False).casefold() + "\n" + "\n".join(
            path.read_text(encoding="utf-8", errors="ignore").casefold()
            for path in data_root.rglob("*")
            if path.is_file() and path.suffix.casefold() in {".json", ".md", ".txt"}
        )
        for term in forbidden_open_terms:
            assert term not in visible_text
        manifest_path = data_root / "input_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["molecule_ids"] == expected_molecules
        assert manifest["visible_te_measurement_ids"] == expected_measurements
        assert manifest["published_conformer_count"] == 0
        assert manifest["author_quantum_outputs"] == 0
        assert manifest["author_wavefunctions"] == 0
        assert manifest["author_surface_results"] == 0
        assert manifest["published_optimal_cutoff_values"] == 0
        assert truth["reference_evidence"]["input_manifest_sha256"] == hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        for record in manifest["files"]:
            path = data_root / record["path"]
            assert path.stat().st_size == record["size_bytes"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        systems = json.loads((data_root / "molecular_systems.json").read_text(encoding="utf-8"))["systems"]
        assert list(systems) == expected_molecules
        for molecule_id in expected_molecules:
            formula, atom_count = formula_contract[molecule_id]
            assert systems[molecule_id]["formula"] == formula
            assert systems[molecule_id]["atom_count"] == atom_count
            assert systems[molecule_id]["charge"] == 0
            assert systems[molecule_id]["multiplicity"] == 1
        measurement_path = data_root / "experimental_measurements" / "te_surfaces.json"
        if expected_measurements:
            measurements = json.loads(measurement_path.read_text(encoding="utf-8"))
            assert [item["measurement_id"] for item in measurements["measurements"]] == expected_measurements
            assert not any(item["molecule_id"] == "ISO-M4" for item in measurements["measurements"])
        else:
            assert not measurement_path.exists()
        if suffix == "04_Blind_Prediction":
            deliverable_paths = {
                item["path"] for item in info["required_deliverables"]
            }
            assert "report/calibration_lock.json" in deliverable_paths
            requirements = "\n".join(info["scientific_requirements"])
            assert "before the first ISO-M4" in requirements
            assert "leave-one-out" in requirements
            assert "substantial CPU parallelism" in requirements
            assert set(truth["expected_result"]) == {
                "held_out_molecule_id",
                "hidden_experimental_te_surface_angstrom2",
                "reference_use_policy",
            }
            assert truth["expected_result"]["held_out_molecule_id"] == "ISO-M4"
            assert (
                truth["expected_result"]["hidden_experimental_te_surface_angstrom2"]
                == 110.538
            )
            assert "post-hoc" in truth["expected_result"]["reference_use_policy"]
            assert "paper_iso_surface_0_0016_angstrom2" not in truth[
                "expected_result"
            ]
            assert "full_credit_relative_error_to_paper_percent" not in truth[
                "expected_result"
            ]
            assert "paper_reference" not in truth["reference_evidence"]
            assert "hidden_posthoc_reference" in truth["reference_evidence"]
            assert truth["evidence_gate_policy"] == {}
            claim_ids = {
                item["id"] for item in truth["scientific_conclusion_rubric"]
            }
            assert "blind_prediction_accuracy" in claim_ids
            assert "calibration_robustness" in claim_ids
            baseline = truth["current_toolbox_feasibility_baseline"]
            assert baseline["classification"] == "solvable"
            assert baseline["unresolved_requirements"] == []
            assert any(
                "calculate_electron_isodensity_surface" in item
                for item in baseline["verified_components"]
            )

    open_by_suffix = {task.split("Electron_Isodensity_", 1)[1]: task for task in open_tasks}
    for task_id in reproduction_tasks:
        suffix = task_id.split("Electron_Isodensity_Reproduction_", 1)[1]
        expected_molecules, expected_measurements, expected_conformers = molecule_contracts[suffix]
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        data_root = TASKS_DIR / task_id / "data" / "benchmark_data"
        assert info["benchmark_family"] == "electron_isodensity_surface"
        assert info["task_mode"] == "guided_reproduction"
        assert info["method_disclosure"] == "paper_reconstructed_protocol"
        assert info["pathway_disclosure"] == "paper_execution_route"
        assert truth["evaluation_mode"] == (
            "dual_axis_100" if suffix == "04_Blind_Prediction" else "rubric_100"
        )
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        if suffix == "04_Blind_Prediction":
            assert len(truth["scientific_conclusion_rubric"]) == 3
            assert sum(
                item["max_score"]
                for item in truth["scientific_conclusion_rubric"]
            ) == 100
        protocol = json.loads((data_root / "computational_protocol.json").read_text(encoding="utf-8"))
        assert protocol["paper_doi"] == "10.1038/s41467-024-50408-8"
        assert protocol["production_density"]["method"] == "DSD-PBEP86"
        assert protocol["production_density"]["orbital_basis"] == "def2-QZVPD"
        assert protocol["surface_analysis"]["density_cutoff_start_au"] == 0.0008
        assert protocol["surface_analysis"]["density_cutoff_stop_au"] == 0.0025
        assert protocol["surface_analysis"]["density_cutoff_step_au"] == 0.0001
        assert protocol["result_values_included"] is False
        assert protocol["author_wavefunctions_included"] is False
        assert protocol["author_quantum_outputs_included"] is False
        assert (data_root / "workflow_requirements.json").is_file()
        assert (data_root / "author_input_templates" / "orca_input.in").is_file()
        assert (data_root / "author_input_templates" / "Multiwfn.in").is_file()
        assert (data_root / "author_input_templates" / "orca_6_compatible.in").is_file()
        assert (data_root / "author_input_templates" / "ccsd_density_orca_6.in").is_file()
        assert (data_root / "author_input_templates" / "orca_plot_ccsd_density.menu").is_file()
        assert (data_root / "author_input_templates" / "Multiwfn_2026_surface_area.menu").is_file()
        assert (
            data_root / "author_input_templates" / "Multiwfn_2026_external_grid_surface.menu"
        ).is_file()
        assert not any(path.is_symlink() for path in data_root.rglob("*"))
        assert not any(path.suffix.casefold() in {".zip", ".gbw", ".wfn", ".wfx", ".out", ".log"} for path in data_root.rglob("*"))
        manifest_path = data_root / "input_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["molecule_ids"] == expected_molecules
        assert manifest["visible_te_measurement_ids"] == expected_measurements
        assert manifest["published_conformer_count"] == expected_conformers
        assert len(manifest["published_conformer_records"]) == expected_conformers
        assert manifest["author_quantum_outputs"] == 0
        assert manifest["author_wavefunctions"] == 0
        assert manifest["author_surface_results"] == 0
        assert manifest["published_optimal_cutoff_values"] == (
            1 if suffix == "04_Blind_Prediction" else 0
        )
        if suffix == "04_Blind_Prediction":
            assert protocol["surface_analysis"]["locked_production_cutoff_au"] == 0.0016
        assert truth["reference_evidence"]["input_manifest_sha256"] == hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        for record in manifest["files"]:
            path = data_root / record["path"]
            assert path.stat().st_size == record["size_bytes"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        for record in manifest["published_conformer_records"]:
            xyz = data_root / record["path"]
            assert int(xyz.read_text(encoding="utf-8").splitlines()[0]) == record["atom_count"]
            assert hashlib.sha256(xyz.read_bytes()).hexdigest() == record["sha256"]
        open_root = TASKS_DIR / open_by_suffix[suffix] / "data" / "benchmark_data"
        assert hashlib.sha256((data_root / "molecular_systems.json").read_bytes()).hexdigest() == hashlib.sha256(
            (open_root / "molecular_systems.json").read_bytes()
        ).hexdigest()
        reproduction_measurements = data_root / "experimental_measurements" / "te_surfaces.json"
        open_measurements = open_root / "experimental_measurements" / "te_surfaces.json"
        if expected_measurements:
            assert hashlib.sha256(reproduction_measurements.read_bytes()).hexdigest() == hashlib.sha256(
                open_measurements.read_bytes()
            ).hexdigest()


def test_dual_track_evaluation_profiles_separate_discovery_from_reproduction():
    task_ids = [
        task
        for task in list_tasks()
        if task.startswith("Electron_Isodensity_")
        or task.startswith("Heterobiaryl_PV_")
    ]
    assert len(task_ids) == 22
    for task_id in task_ids:
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        rubric = {item["id"]: item["max_score"] for item in truth["scoring_rubric"]}
        is_electron_q4 = task_id in {
            "Electron_Isodensity_04_Blind_Prediction",
            "Electron_Isodensity_Reproduction_04_Blind_Prediction",
        }
        if is_electron_q4:
            assert truth["evaluation_mode"] == "dual_axis_100"
            assert len(truth["scientific_conclusion_rubric"]) == 3
            assert truth["reference_conclusion_gate_policy"] == {}
            assert truth["evidence_gate_policy"] == {}
            if info["task_mode"] == "guided_reproduction":
                assert rubric["protocol_interpretation_and_execution_plan"] == 20
            else:
                assert rubric["problem_framing_and_route_design"] == 20
            continue
        if info["task_mode"] == "guided_reproduction":
            assert truth["evaluation_profile"] == "paper_reproduction"
            assert rubric["paper_conclusion_agreement"] == 55
            assert sum(rubric.values()) == 100
            gate = truth["reference_conclusion_gate_policy"]
            assert gate["required"] is True
            assert gate["criterion_id"] == "paper_conclusion_agreement"
            assert gate["score_cap_if_not_matched"] <= 45
        else:
            assert info["task_mode"] == "open_discovery"
            assert truth["evaluation_profile"] == "autonomous_discovery"
            assert "paper_conclusion_agreement" not in rubric
            assert rubric["autonomous_method_and_route_design"] == 25
            assert truth["reference_conclusion_gate_policy"] == {}

    q1_info = load_task_info(
        "Electron_Isodensity_Reproduction_01_Method_Selection"
    )
    q1_requirements = "\n".join(q1_info["scientific_requirements"])
    assert "300^3" in q1_requirements
    assert "walltime_seconds" in q1_requirements
    assert "strict_electron_count_validation" in q1_requirements
    assert "single-process" in q1_requirements


def test_q6_instruction_rendering_exposes_evidence_contract_without_fixed_workflow(
    tmp_path: Path,
):
    runner = TaskRunner(
        "Heterobiaryl_PV_06_End_to_End",
        agent_key="mock",
        workspace_root=tmp_path,
    )
    instructions = runner._build_instructions()
    assert "`independent_open_discovery`" in instructions
    assert "all nine unoptimized seeds" in instructions
    assert "report/stationary_points.csv" in instructions
    assert "report/final_answer.json" in instructions
    assert "not a prescribed calculation sequence" in instructions


def test_task_and_ground_truth_are_separate():
    info = load_task_info("ChemGraph_001")
    truth = load_ground_truth("ChemGraph_001")
    assert info["category"] == "smiles_lookup"
    assert truth["expected_tool_calls"][0]["molecule_name_to_smiles"]["name"] == "sulfur dioxide"
    assert (TASKS_DIR / "ChemGraph_001" / "target_study" / "ground_truth.json").is_file()

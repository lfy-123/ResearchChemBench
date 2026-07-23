#!/usr/bin/env python3
"""Build the guided-reproduction Heterobiaryl P(V) task track.

The existing six tasks remain open-discovery benchmarks.  This builder copies
their decontaminated raw inputs and adds paper-reconstructed protocols and
atom-mapped pathway definitions to a second, guided-reproduction track.  It
never copies author optimized coordinates, transition states, energies, IRCs,
or published numerical answers into agent-visible data.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = PROJECT_ROOT / "tasks"

OPEN_TASKS = [
    "Heterobiaryl_PV_01_Protonation",
    "Heterobiaryl_PV_02_CC_Selectivity",
    "Heterobiaryl_PV_03_CC_vs_CO",
    "Heterobiaryl_PV_04_Coupling_Mechanism",
    "Heterobiaryl_PV_05_Rate_Determining_Step",
    "Heterobiaryl_PV_06_End_to_End",
]

REPRODUCTION_TASKS = [
    "Heterobiaryl_PV_Reproduction_01_Protonation",
    "Heterobiaryl_PV_Reproduction_02_CC_Selectivity",
    "Heterobiaryl_PV_Reproduction_03_CC_vs_CO",
    "Heterobiaryl_PV_Reproduction_04_Coupling_Mechanism",
    "Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step",
    "Heterobiaryl_PV_Reproduction_06_End_to_End",
]

TASK_KEYS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]

ATOM_LABELS = {
    "indexing": "zero_based",
    "methoxy_carbon": 0,
    "methoxy_oxygen": 1,
    "phosphorus": 2,
    "phenyl_ipso_carbons": [3, 9],
    "pyridyl_ipso_carbons": [15, 21],
    "pyridyl_nitrogens": [18, 24],
}

COMPUTATIONAL_PROTOCOL = {
    "schema_version": 1,
    "protocol_type": "paper_reconstructed_guided_reproduction",
    "result_values_included": False,
    "author_coordinates_included": False,
    "stationary_points_included": False,
    "geometry_and_frequency": {
        "reference_software": "Gaussian",
        "reference_method": "wB97XD",
        "basis": "6-31+G(d)",
        "solvation_model": "SMD",
        "solvent": "Ethanol",
        "minimum_route_requirements": [
            "geometry optimization",
            "frequency calculation",
            "stable minima have no chemically significant imaginary frequency",
        ],
        "transition_state_route_requirements": [
            "transition-state optimization with an initial Hessian",
            "one chemically relevant imaginary frequency",
            "forward and reverse IRC or an equivalent direct connectivity test",
        ],
        "reference_route_notes": {
            "minima": "opt=(maxcycles=200) scrf=(solvent=ethanol,smd) freq=noraman",
            "transition_states": "opt=(calcfc,ts,noeigentest,maxcycle=600) scrf=(solvent=ethanol,smd) freq=noraman",
        },
    },
    "large_basis_dft_check": {
        "reference_software": "Gaussian",
        "method": "wB97XD",
        "basis": "def2-QZVPP",
        "solvation_model": "SMD",
        "solvent": "Ethanol",
        "calculation": "single_point",
    },
    "high_level_single_points": {
        "reference_software": "ORCA 4.0.1.2",
        "deployed_software_may_be_newer": True,
        "method": "DLPNO-CCSD(T)",
        "basis_sets": ["cc-pVDZ", "cc-pVTZ"],
        "target_combination": "cc-pV(DT)Z extrapolation",
        "solvation": "use the paper-consistent solvent treatment recorded in the generated input and output",
        "require_same_settings_across_competing_paths": True,
    },
    "thermochemistry": {
        "reference_software": "GoodVibes 2.0.1",
        "deployed_software": "GoodVibes 4.3",
        "temperature_kelvin": 353.15,
        "standard_state": "1 mol/L solution",
        "solvent": "Ethanol",
        "requirements": [
            "record low-frequency and quasi-harmonic settings",
            "record frequency and zero-point scale factors",
            "combine thermal corrections with explicitly matched high-level single-point outputs",
            "keep paper-published values separate from values recomputed with the deployed versions",
        ],
    },
    "mechanism_analysis": {
        "nbo_required": False,
        "accepted_equivalent_evidence": [
            "forming and breaking bond distances along the IRC",
            "Wiberg or Mayer bond-order changes",
            "oxygen atomic-charge changes",
            "optional electron-density or bond-critical-point analysis",
        ],
        "claim_boundary": "Equivalent evidence may establish limited direct oxygen involvement but must not be reported as an exact NBO lone-pair occupation.",
    },
    "version_policy": {
        "published_values": "not included; compare only after scoring",
        "current_toolbox_values": "primary reproducible calculation output",
        "exact_numeric_identity_required": False,
        "required": "stationarity, connectivity, consistent conditions, pathway ordering, provenance, and an explanation of version-dependent deviations",
    },
}


PATHS: dict[str, dict[str, Any]] = {
    "P0_PyPy": {
        "state": "P0",
        "path_family": "pyridyl_pyridyl_C_C",
        "forming_bonds": [[15, 21]],
        "breaking_bonds": [[2, 21]],
        "retained_bonds_to_monitor": [[2, 15], [2, 1], [2, 3], [2, 9]],
        "donor": {"ligand": "pyridyl_C21", "starting_role": "apical"},
        "acceptor": {"ligand": "pyridyl_C15", "starting_role": "equatorial"},
    },
    "P1_PyPy": {
        "state": "P1",
        "path_family": "pyridyl_pyridyl_C_C",
        "forming_bonds": [[15, 21]],
        "breaking_bonds": [[2, 21]],
        "retained_bonds_to_monitor": [[2, 15], [2, 1], [2, 3], [2, 9]],
        "donor": {"ligand": "pyridyl_C21", "starting_role": "apical"},
        "acceptor": {"ligand": "pyridyl_C15", "starting_role": "equatorial"},
    },
    "P2_PyPy": {
        "state": "P2",
        "path_family": "pyridyl_pyridyl_C_C",
        "forming_bonds": [[15, 21]],
        "breaking_bonds": [[2, 21]],
        "retained_bonds_to_monitor": [[2, 15], [2, 1], [2, 3], [2, 9]],
        "donor": {"ligand": "pyridyl_C21", "starting_role": "apical"},
        "acceptor": {"ligand": "pyridyl_C15", "starting_role": "equatorial"},
    },
    "P0_PhPy_py_donor": {
        "state": "P0",
        "path_family": "phenyl_pyridyl_C_C",
        "forming_bonds": [[3, 21]],
        "breaking_bonds": [[2, 21]],
        "donor": {"ligand": "pyridyl_C21", "starting_role": "apical"},
        "acceptor": {"ligand": "phenyl_C3", "starting_role": "equatorial"},
    },
    "P1_PhPy_py_donor": {
        "state": "P1",
        "path_family": "phenyl_pyridyl_C_C",
        "forming_bonds": [[3, 21]],
        "breaking_bonds": [[2, 21]],
        "donor": {"ligand": "pyridyl_C21", "starting_role": "apical"},
        "acceptor": {"ligand": "phenyl_C3", "starting_role": "equatorial"},
    },
    "P2_PhPy_py_donor": {
        "state": "P2",
        "path_family": "phenyl_pyridyl_C_C",
        "forming_bonds": [[3, 21]],
        "breaking_bonds": [[2, 21]],
        "donor": {"ligand": "pyridyl_C21", "starting_role": "apical"},
        "acceptor": {"ligand": "phenyl_C3", "starting_role": "equatorial"},
    },
    "P2_PhPy_ph_donor_control": {
        "state": "P2",
        "path_family": "phenyl_pyridyl_C_C_control_direction",
        "forming_bonds": [[3, 15]],
        "breaking_bonds": [[2, 3]],
        "donor": {"ligand": "phenyl_C3", "starting_role": "apical"},
        "acceptor": {"ligand": "pyridyl_C15", "starting_role": "equatorial"},
        "role": "control candidate used to test donor-direction sensitivity rather than an assumed answer",
    },
    "P2_CO": {
        "state": "P2",
        "path_family": "alkoxy_pyridyl_C_O",
        "forming_bonds": [[1, 15]],
        "breaking_bonds": [[2, 1]],
        "retained_bonds_to_monitor": [[2, 15], [2, 21], [2, 3], [2, 9]],
        "donor": {"ligand": "methoxy_O1", "starting_role": "apical_candidate"},
        "acceptor": {"ligand": "pyridyl_C15", "starting_role": "equatorial_candidate"},
        "symmetry_related_candidate": {"forming_bonds": [[1, 21]], "breaking_bonds": [[2, 1]]},
    },
    "P2_PyPy_concerted_control": {
        "state": "P2",
        "path_family": "concerted_two_P_C_cleavage_control",
        "forming_bonds": [[15, 21]],
        "breaking_bonds": [[2, 15], [2, 21]],
        "role": "explicit alternative that must be tested rather than assumed to be viable",
    },
}


PATH_IDS = {
    "Q1": ["P0_PyPy", "P1_PyPy", "P2_PyPy"],
    "Q2": [
        "P0_PyPy", "P1_PyPy", "P2_PyPy",
        "P0_PhPy_py_donor", "P1_PhPy_py_donor", "P2_PhPy_py_donor",
        "P2_PhPy_ph_donor_control",
    ],
    "Q3": ["P2_PyPy", "P2_CO"],
    "Q4": ["P2_PyPy", "P2_PyPy_concerted_control"],
    "Q5": ["P2_PyPy"],
    "Q6": list(PATHS),
}


REPRODUCTION_PROMPTS = {
    "Q1": "Using the supplied paper-reconstructed computational protocol and mapped pyridyl-pyridyl pathway definitions, reproduce the protonation-state activation-free-energy comparison for P0, P1, and P2. Independently generate every geometry, stationary point, frequency, IRC, electronic energy, and thermochemical result in this run. Follow the supplied method hierarchy where the deployed software supports it, document any necessary version-compatible substitution, and keep paper-published targets separate from newly recomputed values.",
    "Q2": "Using the supplied protocol and mapped pyridyl-pyridyl and phenyl-pyridyl pathway definitions, reproduce the paper's carbon-carbon chemoselectivity analysis across P0, P1, and P2. Validate all stationary points and connectivity, use common numerical conditions for competing paths, test the supplied donor-direction control candidate, and determine whether the recomputed selectivity is kinetic or product-thermodynamic without reading any hidden reference result.",
    "Q3": "Using the supplied protocol and mapped P2 pyridyl-pyridyl and alkoxy-pyridyl pathways, reproduce the comparison between carbon-carbon and carbon-oxygen coupling. The alkoxy pathway forms O-C while breaking P-O; do not substitute a different bond-edit hypothesis. Generate and validate both pathways under common conditions, retain failed searches, and compare newly computed barriers or defensible bounds without using a published value as calculation evidence.",
    "Q4": "Reproduce the paper's reaction-coordinate analysis using the supplied P2 stepwise pathway and concerted control definition. Locate and validate the key transition region, run bidirectional connectivity tests, search for a post-coupling dearomatized minimum, and quantify axial P-C cleavage, C-C formation, retained equatorial bonds, and oxygen involvement. NBO is not required: use the supplied equivalent geometry, bond-order, charge, and optional density criteria, and do not report them as exact NBO occupations.",
    "Q5": "Reproduce the paper's experimental-computational rate-determining-step argument using the supplied protocol, P2 ligand-coupling route, and public relative-rate, NMR, product, and ethoxide observations. Recompute the downstream ligand-coupling evidence, then separately assign the rate-determining, selectivity-determining, and strongly irreversible stages. The public source package has no time-resolved kinetic traces or raw NMR FIDs; do not invent uncertainties or claim that non-detection proves absence. An alcohol-addition transition-state calculation is an optional extension, not a required reconstruction of the published analysis.",
    "Q6": "Perform a guided end-to-end reproduction using the supplied paper-reconstructed protocol, mapped pathway set, experimental observations, and evidence gates. Recompute protonation effects, pyridyl-pyridyl versus phenyl-pyridyl selectivity, carbon-carbon versus carbon-oxygen competition, the key reaction-coordinate mechanism, and the experimental-computational kinetic-role assignment. Generate all numerical and structural evidence in this run, preserve failures, and report paper-published targets separately from current-toolbox values.",
}


REPRODUCTION_REQUIREMENTS = {
    "Q1": [
        "Apply the supplied geometry/frequency, high-level single-point, and thermochemistry hierarchy consistently to P0, P1, and P2.",
        "Validate every reported transition state by a target imaginary mode and forward/reverse connectivity.",
        "Report current-toolbox activation free energies and their protonation trend separately from hidden paper-published comparison values.",
    ],
    "Q2": [
        "Use the supplied mapped Py-Py and Ph-Py definitions and common conditions across every comparison.",
        "Validate both reactant and transition-state references; a scan maximum alone is not a barrier.",
        "Test the supplied donor-direction control and explain rejected or higher-cost pathway hypotheses.",
    ],
    "Q3": [
        "Use the supplied C-O definition that forms O-C and breaks P-O, including the symmetry-related candidate when needed.",
        "Produce same-condition validated barriers or explicit reproducible bounds for both C-C and C-O.",
        "Do not infer the quantitative barrier difference from the measurement table.",
    ],
    "Q4": [
        "Validate the stepwise candidate and actively test the supplied concerted control path.",
        "Search for and frequency-check a dearomatized post-coupling minimum.",
        "Use NBO-free equivalent geometry, Wiberg/Mayer bond-order, oxygen-charge, and optional density evidence without claiming exact lone-pair occupations.",
    ],
    "Q5": [
        "Recompute at least the supplied P2 downstream ligand-coupling path using validated stationary-point evidence.",
        "Use the public relative rates, NMR non-detection, product selectivity, and ethoxide observations with their stated limitations.",
        "Do not fabricate time-series uncertainty; separate rate control, selectivity control, and irreversibility.",
    ],
    "Q6": [
        "Execute the supplied protocol hierarchy for all core pathway families or retain a documented failed attempt and defensible bound.",
        "Require stationarity and connectivity before including a state in the final profile.",
        "Use one 353.15 K, 1 M main profile and keep version/method sensitivities separate.",
        "Complete the NBO-free reaction-coordinate analysis and the experimental-computational kinetic-role integration.",
    ],
}


WORKFLOW_STAGES = [
    "audit molecular identity, charge, multiplicity, atom mapping, and seed quality",
    "enumerate or screen coordination isomers and conformers without using author coordinates",
    "generate a double-ended path or controlled reaction-coordinate scan from the supplied endpoints/bond edits",
    "refine candidate transition states",
    "calculate Hessians and classify normal modes",
    "trace forward and reverse connectivity and optimize the endpoints",
    "perform paper-level or documented version-compatible electronic-structure refinement",
    "derive 353.15 K, 1 M thermochemistry with matched single-point corrections",
    "analyze pathway ordering and NBO-free reaction-coordinate evidence",
    "integrate calculations with only the supplied public experimental observations",
]


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_files(root: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "input_manifest.json":
            records.append(
                {
                    "path": str(path.relative_to(root)),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    return records


def guided_rubric(task_key: str) -> list[dict[str, Any]]:
    common = [
        {"id": "protocol_fidelity", "max_score": 15, "criterion": "Uses the supplied paper-reconstructed method hierarchy or documents a scientifically controlled version-compatible substitution."},
        {"id": "managed_execution", "max_score": 15, "criterion": "Runs traceable predefined Actions, native software, or Agent-authored programs and preserves retries and failures."},
        {"id": "stationary_point_validation", "max_score": 20, "criterion": "Every profile minimum and transition-state claim has appropriate Hessian/mode evidence; transition states also have direct connectivity evidence."},
        {"id": "common_condition_profile", "max_score": 20, "criterion": "Builds a comparable 353.15 K, 1 M profile with matched electronic and thermal references and no hidden-value substitution."},
        {"id": "task_conclusion", "max_score": 20, "criterion": f"Reproduces the main scientific conclusion for {task_key} from newly generated evidence and explains version-dependent numerical differences."},
        {"id": "provenance_and_limits", "max_score": 10, "criterion": "Links claims to artifacts, separates paper targets from recomputation, and states unresolved branches and unavailable raw experimental uncertainty."},
    ]
    return common


def update_open_metadata() -> None:
    for task_id in OPEN_TASKS:
        path = TASKS_ROOT / task_id / "task_info.json"
        info = json.loads(path.read_text(encoding="utf-8"))
        info["benchmark_family"] = "heterobiaryl_pv"
        info["task_mode"] = "open_discovery"
        info["method_disclosure"] = "none"
        info["pathway_disclosure"] = "none"
        path.write_bytes(json_bytes(info))


def build_one(open_task: str, reproduction_task: str, task_key: str, stage_root: Path) -> Path:
    source = TASKS_ROOT / open_task
    target = stage_root / reproduction_task
    shutil.copytree(source, target)

    data_root = target / "data" / "benchmark_data"
    (data_root / "computational_protocol.json").write_bytes(json_bytes(COMPUTATIONAL_PROTOCOL))
    selected_paths = {path_id: deepcopy(PATHS[path_id]) for path_id in PATH_IDS[task_key]}
    (data_root / "reaction_definitions.json").write_bytes(
        json_bytes(
            {
                "schema_version": 1,
                "task_id": reproduction_task,
                "atom_labels": ATOM_LABELS,
                "result_values_included": False,
                "author_coordinates_included": False,
                "paths": selected_paths,
            }
        )
    )
    (data_root / "workflow_requirements.json").write_bytes(
        json_bytes(
            {
                "schema_version": 1,
                "mode": "guided_reproduction",
                "required_stages": WORKFLOW_STAGES,
                "failure_policy": "Retain failed searches and do not replace missing evidence with paper-published numerical values.",
                "nbo_policy": "NBO is optional; equivalent bond-order, charge, geometry, and optional density evidence is accepted.",
            }
        )
    )
    readme = data_root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\n## Guided-reproduction additions\n\n"
        + "This copied raw-input set additionally contains a paper-reconstructed computational protocol, mapped pathway definitions, and workflow requirements. These files disclose methods and candidate routes but contain no published barrier, pathway ranking, author stationary-point coordinate, author IRC, or reference answer. Every numerical result must be regenerated.\n",
        encoding="utf-8",
    )

    manifest_path = data_root / "input_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["task_id"] = reproduction_task
    manifest["task_mode"] = "guided_reproduction"
    manifest["method_protocol_files"] = ["computational_protocol.json"]
    manifest["reaction_definition_files"] = ["reaction_definitions.json"]
    manifest["workflow_requirement_files"] = ["workflow_requirements.json"]
    manifest["published_numerical_results"] = 0
    manifest["author_coordinates"] = 0
    manifest["files"] = public_files(data_root)
    manifest_path.write_bytes(json_bytes(manifest))

    info_path = target / "task_info.json"
    info = json.loads(info_path.read_text(encoding="utf-8"))
    info.update(
        {
            "task_id": reproduction_task,
            "source_id": "heterobiaryl_pv_2018_guided_reproduction",
            "benchmark_family": "heterobiaryl_pv",
            "task_mode": "guided_reproduction",
            "method_disclosure": "paper_reconstructed_protocol",
            "pathway_disclosure": "mapped_candidate_routes",
            "scientific_mode": "guided_reproduction",
            "scientific_mode_description": "The paper-reconstructed method hierarchy and candidate reaction routes are supplied. The Agent must execute, debug, validate, and report the reproduction without reading hidden results or author stationary points.",
            "task": REPRODUCTION_PROMPTS[task_key],
            "scientific_requirements": REPRODUCTION_REQUIREMENTS[task_key],
            "archive_extractions": [],
        }
    )
    info["data"] = [
        {
            "name": "Guided Heterobiaryl P(V) reproduction inputs",
            "path": "data/benchmark_data",
            "type": "directory",
            "description": "Decontaminated raw structures and measurements copied from the open-discovery task, plus a paper-reconstructed method protocol, mapped candidate pathways, and workflow requirements. No author stationary point, calculation output, published numerical result, or reference answer is visible.",
        }
    ]
    info_path.write_bytes(json_bytes(info))

    truth_path = target / "target_study" / "ground_truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    truth["evaluation_mode"] = "rubric_100"
    truth["score_max"] = 100
    truth["scoring_rubric"] = guided_rubric(task_key)
    truth["judge_instructions"] = (
        "This is a guided paper-reproduction task. Methods and mapped candidate routes are public, "
        "but all numerical, structural, stationarity, connectivity, and thermochemical evidence must "
        "be newly generated. Accept predefined Actions, managed native jobs, and managed Agent-authored "
        "programs. Score protocol fidelity, scientific validation, troubleshooting, common-condition "
        "comparability, and provenance. Do not reward copying a paper-published number without a new artifact."
    )
    truth["current_toolbox_reproduction_baseline"] = {
        "status": "pending_post_repair_baseline",
        "software_family": ["Gaussian 16", "ORCA 6.1.1", "GoodVibes 4.3"],
        "temperature_kelvin": 353.15,
        "standard_state_mol_l": 1.0,
    }
    evidence = truth.setdefault("reference_evidence", {})
    evidence["task_mode"] = "guided_reproduction"
    evidence["method_protocol_public"] = True
    evidence["mapped_candidate_routes_public"] = True
    evidence["published_reference_is_hidden_comparison_only"] = True
    evidence["input_manifest_sha256"] = sha256(manifest_path)
    truth_path.write_bytes(json_bytes(truth))
    return target


def main() -> int:
    update_open_metadata()
    built: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="heterobiaryl_dual_track_") as temporary:
        stage_root = Path(temporary)
        for open_task, reproduction_task, task_key in zip(OPEN_TASKS, REPRODUCTION_TASKS, TASK_KEYS):
            staged = build_one(open_task, reproduction_task, task_key, stage_root)
            final = TASKS_ROOT / reproduction_task
            if final.exists():
                shutil.rmtree(final)
            shutil.copytree(staged, final)
            manifest = final / "data" / "benchmark_data" / "input_manifest.json"
            built[reproduction_task] = {
                "source_open_task": open_task,
                "input_manifest_sha256": sha256(manifest),
                "path_ids": PATH_IDS[task_key],
            }
    print(json.dumps(built, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

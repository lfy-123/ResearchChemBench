#!/usr/bin/env python3
"""Build the guided-reproduction Heterobiaryl P(V) task track.

The existing six tasks remain open-discovery benchmarks. Selected guided tasks
also expose the author's public Zenodo quantum-output archives so the benchmark
tests reproducible validation and thermochemical reanalysis instead of an
unbounded rediscovery of every stationary point.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.dual_axis import dual_axis_policy, process_rubric

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

AUTHOR_OUTPUT_ROOT = (
    TASKS_ROOT
    / "_heterobiaryl_pv_shared"
    / "reference"
    / "author_computational_outputs"
)
AUTHOR_OUTPUT_ARCHIVES = {
    "P0": "Int-I_unprotonated.zip",
    "P1": "Int-I_H_plus.zip",
    "P2": "Int-I_2H_2plus.zip",
}
TASK_AUTHOR_OUTPUT_STATES = {
    "Q1": ("P0", "P1", "P2"),
    "Q2": ("P0", "P1", "P2"),
    "Q3": ("P2",),
    "Q5": ("P2",),
}

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
        "solvation_model": "SMD",
        "solvent": "Ethanol",
        "reference_orca_route": "! CPCM DLPNO-CCSD(T) Extrapolate(2/3,cc) RIJCOSX GRIDX5 TightSCF KDIIS; %cpcm smd true; solvent Ethanol",
        "version_compatibility_note": "Translate the ORCA 4 route to valid ORCA 6.1.1 syntax while preserving SMD ethanol, DLPNO-CCSD(T), cc-pVDZ/cc-pVTZ 2/3 extrapolation, SCF tightness, and common settings across paths.",
        "require_same_settings_across_competing_paths": True,
    },
    "thermochemistry": {
        "reference_software": "GoodVibes 2.0.1",
        "deployed_software": "GoodVibes 4.3",
        "temperature_kelvin": 353.15,
        "standard_state": "1 mol/L solution",
        "solvent": "Ethanol",
        "quasi_harmonic_entropy_model": "Grimme",
        "quasi_harmonic_cutoff_wavenumber_cm-1": 100.0,
        "small_imaginary_frequency_inversion_threshold_cm-1": -5.0,
        "single_point_suffix": "DLPNO",
        "paper_related_example_command": "goodvibes *.log --spc DLPNO --pes <profile.yaml> -t 353.15 --imag --invertifreq -5 --media ethanol -c 1",
        "requirements": [
            "record low-frequency and quasi-harmonic settings",
            "record frequency and zero-point scale factors; the accessible paper text and public example do not uniquely recover a paper-era scale factor, so do not invent one",
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
    "Q1": "Using the supplied author-deposited Gaussian frequency outputs and ORCA DLPNO-CCSD(T) single-point outputs, independently reanalyze the pyridyl-pyridyl activation free energies for P0, P1, and P2. Validate file matching and stationary-point character, apply one 353.15 K and 1 M ethanol GoodVibes convention, and reproduce the protonation trend without presenting publication values as calculations from this run.",
    "Q2": "Using the supplied author-deposited Gaussian and ORCA raw outputs, independently reconstruct the pyridyl-pyridyl and phenyl-pyridyl carbon-carbon free-energy profiles for P0, P1, and P2. Use a common initial-state reference for each protonation state, distinguish kinetic barriers from product thermodynamics, and report both the reanalysis and its provenance.",
    "Q3": "Reproduce the evidence-supported P2 carbon-carbon versus carbon-oxygen comparison. Recompute and validate the pyridyl-pyridyl C-C barrier from the supplied author raw outputs, audit the archive for a C-O transition state, and compare the recomputed C-C result with the explicitly supplied publication-reported C-O benchmark. The C-O value must remain labeled literature evidence because the public author archive does not contain its frequency, IRC, or DLPNO files.",
    "Q4": "Reproduce the paper's reaction-coordinate analysis using the supplied P2 stepwise pathway and concerted control definition. Locate and validate the key transition region, run bidirectional connectivity tests, search for a post-coupling dearomatized minimum, and quantify axial P-C cleavage, C-C formation, retained equatorial bonds, and oxygen involvement. NBO is not required: use the supplied equivalent geometry, bond-order, charge, and optional density criteria, and do not report them as exact NBO occupations.",
    "Q5": "Reproduce the paper's experimental-computational rate-determining-step argument using the supplied P2 author raw outputs and public relative-rate, NMR, product, and ethoxide observations. Reconstruct the full Int-I to TS-I to Int-II to TS-II to Int-III ligand-coupling profile, then separately assign the rate-determining, selectivity-determining, and strongly irreversible stages. Do not claim that the downstream profile alone calculates the alcohol-addition barrier.",
    "Q6": "Perform a guided end-to-end reproduction using the supplied paper-reconstructed protocol, mapped pathway set, experimental observations, and evidence gates. Recompute protonation effects, pyridyl-pyridyl versus phenyl-pyridyl selectivity, carbon-carbon versus carbon-oxygen competition, the key reaction-coordinate mechanism, and the experimental-computational kinetic-role assignment. Generate all numerical and structural evidence in this run, preserve failures, and report paper-published targets separately from current-toolbox values.",
}


REPRODUCTION_REQUIREMENTS = {
    "Q1": [
        "Apply the supplied geometry/frequency, high-level single-point, and thermochemistry hierarchy consistently to P0, P1, and P2.",
        "Validate every barrier-defining supplied transition state by its frequency output and forming/breaking-bond geometry.",
        "Report newly generated GoodVibes activation free energies and their protonation trend separately from publication comparison values.",
    ],
    "Q2": [
        "Use the supplied mapped Py-Py and Ph-Py definitions and common conditions across every comparison.",
        "Validate reactant, transition-state, and product output identities before constructing each profile.",
        "Use a shared Int-I reference within each protonation state and explain the difference between common-reference and path-local zeroing.",
    ],
    "Q3": [
        "Recompute the P2 C-C barrier from supplied Gaussian and matched DLPNO outputs and verify the TS-I forming bond.",
        "Audit the supplied P2 archive and explicitly report that it contains no independently reanalyzable C-O transition-state output when that remains the case.",
        "Treat the publication-reported 18 kcal/mol C-O barrier as literature evidence, not as a newly computed result.",
    ],
    "Q4": [
        "Validate the stepwise candidate and actively test the supplied concerted control path.",
        "Search for and frequency-check a dearomatized post-coupling minimum.",
        "Use NBO-free equivalent geometry, Wiberg/Mayer bond-order, oxygen-charge, and optional density evidence without claiming exact lone-pair occupations.",
    ],
    "Q5": [
        "Reanalyze the supplied P2 Int-I, TS-I, Int-II, TS-II, and Int-III outputs with matched stationary-point evidence.",
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


BASELINE_COMMON = {
    "assessment_date": "2026-07-23",
    "status": "assessed_post_repair",
    "classification": "partially_solvable",
    "major_paper_conclusion_reproduced_in_this_audit": False,
    "evidence_level": "real_backend_smokes_and_action_validation_without_a_complete_PV_paper_level_profile",
    "software_family": [
        "Gaussian 16 C.01",
        "ORCA 6.1.1",
        "GoodVibes 4.3",
        "pysisyphus 1.0.0",
        "xTB",
    ],
    "verified_shared_capabilities": [
        "native Gaussian execution is installed for optimization, frequencies, transition-state searches, and IRC jobs",
        "ORCA SMD input generation was repaired and a real SMD-ethanol calculation terminated normally",
        "ORCA accepted 2, 4, 8, 16, 32, and 48 CPU cores in real calculations with consistent energies",
        "real pysisyphus/xTB NEB, growing-string, freezing-string, and relaxed-scan calculations produced saved paths",
        "reaction-path validation, reaction-coordinate analysis, and coordination-isomer enumeration are available as deterministic Actions",
        "GoodVibes thermochemistry Actions have existing successful real-software smoke evidence",
        "Agent-authored managed programs may call the installed native software when a typed Action is not sufficiently expressive",
    ],
    "resource_guidance": {
        "server_logical_cpu_cores": 54,
        "toolbox_per_job_cpu_core_cap": 48,
        "observed_small_ORCA_HF_sweet_spot_cores": 32,
        "recommendation": "Benchmark 24-32 cores first for large molecular jobs; use up to 48 only after method- and system-specific scaling evidence, and reserve cores for the operating system and monitoring.",
    },
    "actual_run_evidence_root": "docs/check/heterobiaryl_toolbox_repair",
}


REPRODUCTION_BASELINES = {
    "Q1": {
        "capability_if_protocol_is_disclosed": "supported_in_principle_but_not_yet_demonstrated_end_to_end",
        "supported_scope": "The installed native programs and repaired Actions can generate and validate candidate P0/P1/P2 paths and assemble 353.15 K, 1 M thermochemistry.",
        "unresolved_requirements": [
            "No P0/P1/P2 paper-level reactant/TS set was optimized and frequency-checked during this audit.",
            "No bidirectional connectivity and matched SMD-DLPNO-CCSD(T)/cc-pV(DT)Z profile was completed for the three charge states.",
            "Therefore the published protonation barrier trend has not been independently reproduced from current-task inputs.",
        ],
    },
    "Q2": {
        "capability_if_protocol_is_disclosed": "supported_in_principle_but_requires_a_large_multi_path_campaign",
        "supported_scope": "The toolbox can search mapped Py-Py and Ph-Py paths, validate stationary points, calculate products, and compare common-condition free energies.",
        "unresolved_requirements": [
            "Validated Py-Py and Ph-Py reactant, transition-state, and product sets were not generated for all P0/P1/P2 states.",
            "The donor-direction control and coordination/conformer alternatives remain unrefined at the paper level.",
            "Neither kinetic nor product-thermodynamic selectivity has yet been reproduced with complete matched evidence.",
        ],
    },
    "Q3": {
        "capability_if_protocol_is_disclosed": "supported_in_principle_with_endpoint_generation_and_transition_state_work",
        "supported_scope": "Mapped C-C and C-O bond changes, double-ended path search, relaxed scans, native TS/IRC, ORCA refinement, and thermochemistry are available.",
        "unresolved_requirements": [
            "The public input deliberately contains no author product or transition-state coordinates; the C-O product/endpoints must be generated from the supplied bond edit.",
            "No first-order C-O saddle or bidirectional connectivity was established for the P2 system in this audit.",
            "A same-condition quantitative C-C versus C-O barrier difference has not been recomputed.",
        ],
    },
    "Q4": {
        "capability_if_protocol_is_disclosed": "path_screening_supported_but_full_mechanistic_proof_not_yet_completed",
        "supported_scope": "The repaired path/scan Actions can test stepwise and concerted candidates; native Hessian/IRC and NBO-free bond-order, charge, geometry, and density analyses can supply validation evidence.",
        "unresolved_requirements": [
            "No P(V) transition state was refined to a single target imaginary mode and connected in both directions during this audit.",
            "The dearomatized post-coupling minimum and the concerted control path remain unverified.",
            "NBO is not a blocker, but equivalent electronic evidence still must be calculated on the validated P(V) coordinate.",
        ],
    },
    "Q5": {
        "capability_if_protocol_is_disclosed": "computational_downstream_test_supported_but_the_full_kinetic_assignment_remains_evidence_limited",
        "supported_scope": "The toolbox can regress the supplied relative-rate series, recompute a P2 ligand-coupling path, and integrate reported product/NMR/ethoxide observations with explicit limitations.",
        "unresolved_requirements": [
            "The public package contains reported measurements but no time-resolved kinetic traces, raw NMR FIDs, or uncertainty-bearing primary rate data.",
            "It also lacks a fully specified alcohol-addition reaction system/path, so an independent comparison of every candidate rate-controlling elementary step is not currently defined.",
            "A downstream P2 coupling profile was not completed at the paper level in this audit; the rate-, selectivity-, and irreversibility assignments therefore remain partial rather than fully reproduced.",
        ],
    },
    "Q6": {
        "capability_if_protocol_is_disclosed": "all_required_software_families_are_present_but_the_full_campaign_is_not_yet_executed",
        "supported_scope": "The guided track now exposes the complete method hierarchy and mapped candidate set, and the toolbox supports the constituent screening, path, stationary-point, electronic-energy, thermochemistry, and analysis stages.",
        "unresolved_requirements": [
            "The complete P0/P1/P2 and Py-Py/Ph-Py/C-O stationary-point network has not been generated and validated.",
            "Q5 retains primary experimental-data and full reaction-network limitations.",
            "Consequently no complete end-to-end paper-level free-energy surface or integrated mechanism was independently reproduced in this audit.",
        ],
    },
}


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


def write_readme_section(path: Path, heading: str, body: str) -> None:
    marker = f"\n## {heading}\n"
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(
        text + f"\n## {heading}\n\n{body.rstrip()}\n",
        encoding="utf-8",
    )


def scientific_conclusion_rubric(task_key: str) -> list[dict[str, Any]]:
    rubrics = {
        "Q1": [
            {
                "id": "successive_protonation_barrier_order",
                "max_score": 40,
                "statement": "Comparable kinetic evidence establishes the pyridyl-pyridyl coupling-barrier order P0 > P1 > P2.",
                "acceptance_rule": "Require validated or defensibly bounded P0, P1, and P2 activation free energies under one thermochemical and reference-state convention.",
                "required_evidence": ["P0/P1/P2 pathway evidence", "common free-energy convention", "stationary-point or controlled-bound validation"],
            },
            {
                "id": "stepwise_barrier_reduction_scale",
                "max_score": 35,
                "statement": "The first and second protonations successively lower the barrier on the paper scale of approximately 10 and 6 kcal/mol.",
                "acceptance_rule": "Full credit requires the correct direction and approximate relative scale; partial credit is available when uncertainty preserves only the qualitative trend.",
                "required_evidence": ["three comparable barriers", "barrier-difference analysis", "uncertainty or sensitivity analysis"],
            },
            {
                "id": "protonation_kinetic_conclusion",
                "max_score": 25,
                "statement": "Successive protonation promotes pyridyl-pyridyl coupling primarily by lowering its kinetic barrier.",
                "acceptance_rule": "Require an evidence-linked kinetic interpretation that is not inferred solely from copied reference values.",
                "required_evidence": ["activation-free-energy trend", "alternative explanation check", "artifact-linked conclusion"],
            },
        ],
        "Q2": [
            {
                "id": "pypy_over_phpy_barrier_preference",
                "max_score": 40,
                "statement": "Pyridyl-pyridyl coupling has a lower activation barrier than phenyl-pyridyl coupling for P0, P1, and P2.",
                "acceptance_rule": "Require common-reference profiles for both coupling families in all three protonation states; full credit should recover the paper ordering and approximate barrier separations.",
                "required_evidence": ["P0/P1/P2 Py-Py profiles", "P0/P1/P2 Ph-Py profiles", "common-reference comparison"],
            },
            {
                "id": "kinetic_selectivity_assignment",
                "max_score": 35,
                "statement": "The pyridyl-pyridyl product preference is primarily kinetic rather than a consequence of product thermodynamics.",
                "acceptance_rule": "Require activation and reaction free energies to be analyzed separately and compared under consistent conditions.",
                "required_evidence": ["activation free energies", "reaction free energies", "kinetic-versus-thermodynamic interpretation"],
            },
            {
                "id": "protonation_dependence_of_selectivity",
                "max_score": 25,
                "statement": "Protonation lowers both pathway barriers while retaining a kinetic preference for pyridyl-pyridyl coupling.",
                "acceptance_rule": "Require the cross-state trend to be supported by validated numerical profiles rather than a single-state comparison.",
                "required_evidence": ["cross-state barrier trends", "pathway identity validation", "uncertainty analysis"],
            },
        ],
        "Q3": [
            {
                "id": "cc_over_co_barrier_preference",
                "max_score": 45,
                "statement": "For P2, carbon-carbon coupling is kinetically favored over carbon-oxygen coupling.",
                "acceptance_rule": "Require a validated C-C barrier and a defensible C-O comparison under a clearly stated evidence boundary.",
                "required_evidence": ["P2 C-C barrier evidence", "P2 C-O evidence or explicit publication benchmark", "comparable conditions"],
            },
            {
                "id": "cc_co_barrier_difference",
                "max_score": 35,
                "statement": "The P2 C-O barrier is about 4 kcal/mol higher than the C-C barrier, on the paper scale of about 18 versus 14 kcal/mol.",
                "acceptance_rule": "Full credit requires the correct sign and approximate magnitude, with any publication-only C-O value labeled separately from recomputation.",
                "required_evidence": ["barrier-difference calculation", "source labeling", "uncertainty discussion"],
            },
            {
                "id": "minor_co_pathway_plausibility",
                "max_score": 20,
                "statement": "C-C is preferred, but the modest barrier separation leaves minor C-O coupling chemically plausible.",
                "acceptance_rule": "Require a quantitative selectivity interpretation that does not incorrectly rule out the higher-barrier pathway.",
                "required_evidence": ["barrier separation", "temperature-aware interpretation", "scope limitation"],
            },
        ],
        "Q4": [
            {
                "id": "stepwise_asynchronous_mechanism",
                "max_score": 40,
                "statement": "Ligand coupling proceeds by a stepwise, asynchronous apical-to-equatorial C-C coupling mechanism rather than a fully concerted two-bond cleavage.",
                "acceptance_rule": "Require reaction-coordinate evidence that distinguishes the stepwise path from the concerted control.",
                "required_evidence": ["validated transition region", "concerted-path control", "forming and breaking bond evolution"],
            },
            {
                "id": "dearomatized_intermediate_and_connectivity",
                "max_score": 35,
                "statement": "The key coupling transition region connects to a dearomatized post-coupling intermediate.",
                "acceptance_rule": "Require one target imaginary mode plus forward/reverse connectivity or equivalent direct endpoint validation and an optimized intermediate.",
                "required_evidence": ["frequency evidence", "bidirectional connectivity", "dearomatized minimum"],
            },
            {
                "id": "limited_oxygen_participation",
                "max_score": 25,
                "statement": "Oxygen electronic participation changes little along the key coupling coordinate.",
                "acceptance_rule": "Accept NBO or equivalent bond-order, charge, geometry, or density evidence, but do not accept an unsupported exact lone-pair occupation claim.",
                "required_evidence": ["oxygen-sensitive electronic descriptor", "coordinate comparison", "method-bound interpretation"],
            },
        ],
        "Q5": [
            {
                "id": "alcohol_addition_rate_determining",
                "max_score": 40,
                "statement": "Alcohol addition at phosphonium phosphorus before ligand coupling is the overall rate-determining step.",
                "acceptance_rule": "Require integration of the experimental substituent-rate trend with the downstream computational profile, while acknowledging that the downstream profile alone does not calculate the alcohol-addition barrier.",
                "required_evidence": ["relative-rate analysis", "experimental observations", "scope-aware kinetic inference"],
            },
            {
                "id": "ligand_coupling_selectivity_determining",
                "max_score": 35,
                "statement": "Intramolecular P(V) ligand coupling is the selectivity-determining stage.",
                "acceptance_rule": "Require a validated coupling profile and a clear distinction between selectivity control and overall rate control.",
                "required_evidence": ["Int-I through coupling profile", "pathway comparison", "separate kinetic-role assignment"],
            },
            {
                "id": "post_coupling_collapse_irreversible",
                "max_score": 25,
                "statement": "Collapse of the dearomatized post-coupling intermediate to product is strongly irreversible.",
                "acceptance_rule": "Require thermochemical and experimental evidence supporting a strongly downhill post-coupling stage.",
                "required_evidence": ["post-coupling free-energy change", "product or ethoxide observation", "reversibility interpretation"],
            },
        ],
        "Q6": [
            {"id": "active_protonation_state", "max_score": 20, "statement": "The doubly protonated P2 state is the most kinetically competent coupling state.", "acceptance_rule": "Require comparable P0/P1/P2 evidence recovering the protonation-dependent barrier trend.", "required_evidence": ["P0/P1/P2 profiles", "common reference convention"]},
            {"id": "preferred_cc_path", "max_score": 20, "statement": "Pyridyl-pyridyl C-C coupling is preferred over phenyl-pyridyl C-C and P2 C-O alternatives.", "acceptance_rule": "Require matched pathway comparisons that separate kinetic and thermodynamic selectivity.", "required_evidence": ["Py-Py profile", "Ph-Py profile", "C-O comparison"]},
            {"id": "integrated_coupling_mechanism", "max_score": 20, "statement": "The preferred path is stepwise, asynchronous apical-to-equatorial coupling through a dearomatized intermediate.", "acceptance_rule": "Require stationary-point, connectivity, and bond-reorganization evidence.", "required_evidence": ["frequency and connectivity", "dearomatized intermediate", "coordinate analysis"]},
            {"id": "integrated_kinetic_roles", "max_score": 25, "statement": "Alcohol addition is rate-determining, ligand coupling is selectivity-determining, and post-coupling collapse is strongly irreversible.", "acceptance_rule": "Require the three kinetic roles to be assigned separately from combined experimental and computational evidence.", "required_evidence": ["relative rates", "coupling profile", "post-coupling evidence"]},
            {"id": "coherent_end_to_end_model", "max_score": 15, "statement": "The protonation, chemoselectivity, mechanism, and kinetic-role results form one internally consistent reaction model.", "acceptance_rule": "Require conflicts, missing branches, and uncertainty to be reconciled rather than merely listing the component conclusions.", "required_evidence": ["integrated profile", "cross-claim consistency", "limitations and uncertainty"]},
        ],
    }
    return deepcopy(rubrics[task_key])


def update_open_metadata() -> None:
    for task_id in OPEN_TASKS:
        path = TASKS_ROOT / task_id / "task_info.json"
        info = json.loads(path.read_text(encoding="utf-8"))
        info["benchmark_family"] = "heterobiaryl_pv"
        info["task_mode"] = "open_discovery"
        info["method_disclosure"] = "none"
        info["pathway_disclosure"] = "none"
        path.write_bytes(json_bytes(info))
        truth_path = TASKS_ROOT / task_id / "target_study" / "ground_truth.json"
        truth = json.loads(truth_path.read_text(encoding="utf-8"))
        task_key = TASK_KEYS[OPEN_TASKS.index(task_id)]
        truth["evaluation_mode"] = "dual_axis_100"
        truth["evaluation_profile"] = "autonomous_discovery"
        truth["score_max"] = 100
        truth["scoring_rubric"] = process_rubric(reproduction=False)
        truth["scientific_conclusion_rubric"] = scientific_conclusion_rubric(task_key)
        truth["dual_axis_scoring_policy"] = dual_axis_policy()
        truth["reference_conclusion_gate_policy"] = {}
        truth["judge_instructions"] = (
            "Score each task-level scientific conclusion from newly generated evidence, then "
            "score autonomous research-process quality separately. Do not require the paper "
            "method or route, and do not let a good process excuse a wrong conclusion. The "
            "scorer applies the multiplicative dual-axis formula."
        )
        truth_path.write_bytes(json_bytes(truth))


AUTONOMOUS_REANALYSIS_PROMPTS = {
    "Q2": (
        "Using the supplied P0, P1, and P2 completed quantum-chemistry output archives, "
        "independently determine whether pyridyl-pyridyl coupling is preferred over "
        "phenyl-pyridyl coupling for kinetic or thermodynamic reasons. Infer and validate "
        "the file groupings, stationary-point identities, reference states, thermochemical "
        "analysis, and uncertainty treatment without a disclosed paper route."
    ),
    "Q5": (
        "Use the supplied P2 completed quantum-chemistry output archive and experimental "
        "measurements to independently test the most likely rate-determining step under "
        "acidic ethanol conditions. Choose and validate the output analysis and kinetic "
        "reasoning workflow, then distinguish the rate-determining, selectivity-determining, "
        "and strongly irreversible stages without a disclosed paper route."
    ),
}


AUTONOMOUS_REANALYSIS_REQUIREMENTS = {
    "Q2": [
        "Predeclare an independent archive audit, file-matching, stationary-point validation, thermochemistry, and profile-alignment plan.",
        "Validate identity, charge, multiplicity, convergence, frequencies, and the forming-bond geometry before using any output.",
        "Compare Py-Py and Ph-Py activation and reaction free energies for P0, P1, and P2 under one 353.15 K, 1 M ethanol convention.",
        "Use a shared initial-state reference within each protonation state and keep kinetic and thermodynamic selectivity separate.",
        "Treat supplied outputs as source data and every numerical conclusion as a newly generated analysis result with provenance.",
        "When server resources allow, parallelize independent validation and analysis stages without oversubscribing the host.",
    ],
    "Q5": [
        "Predeclare competing rate-control hypotheses and an independent output-validation and thermochemistry plan.",
        "Infer and validate the P2 reactant, transition-state, intermediate, and product output identities before constructing any downstream profile.",
        "Quantify the experimental substituent-rate trend and keep measurements, computations, and inference explicitly separate.",
        "Assign rate control, selectivity control, and irreversibility separately and retain falsifiable alternatives.",
        "Do not claim that the downstream coupling profile directly computes an unobserved alcohol-addition barrier.",
        "When server resources allow, parallelize independent validation and analysis stages without oversubscribing the host.",
    ],
}


def align_open_author_output_inputs(task_id: str, task_key: str) -> None:
    data_root = TASKS_ROOT / task_id / "data" / "benchmark_data"
    states = TASK_AUTHOR_OUTPUT_STATES[task_key]
    archive_records = []
    for state in states:
        filename = AUTHOR_OUTPUT_ARCHIVES[state]
        source = AUTHOR_OUTPUT_ROOT / filename
        destination = data_root / "author_outputs" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        archive_records.append(
            {
                "state": state,
                "path": str(destination.relative_to(data_root)),
                "size_bytes": destination.stat().st_size,
                "sha256": sha256(destination),
                "source_doi": "10.5281/zenodo.1439888",
            }
        )
    (data_root / "author_output_manifest.json").write_bytes(
        json_bytes({"archives": archive_records})
    )
    readme = data_root / "README.md"
    write_readme_section(
        readme,
        "Shared completed-output inputs",
        "This autonomous task receives the same completed author output archives as its guided counterpart. Select the validation, matching, thermochemistry, profile construction, and uncertainty route independently; no paper protocol or mapped reaction route is supplied.",
    )

    info_path = TASKS_ROOT / task_id / "task_info.json"
    info = json.loads(info_path.read_text(encoding="utf-8"))
    info["task"] = AUTONOMOUS_REANALYSIS_PROMPTS[task_key]
    info["scientific_requirements"] = AUTONOMOUS_REANALYSIS_REQUIREMENTS[task_key]
    info["scientific_mode_description"] = (
        "The scientific question and completed raw outputs are fixed, but no paper "
        "analysis method, file grouping, reference construction, or interpretation route is disclosed."
    )
    info["archive_extractions"] = [
        {
            "source": f"benchmark_data/{record['path']}",
            "format": "zip",
            "destination": f"benchmark_data/extracted_author_outputs/{record['state']}",
            "sha256": record["sha256"],
        }
        for record in archive_records
    ]
    info["data"][0]["description"] = (
        "Initial structures, molecular identities, physical conditions, applicable experimental measurements, "
        "and the same completed author-output archives as the guided track; no paper protocol, mapped route, or reference answer."
    )
    info_path.write_bytes(json_bytes(info))

    manifest_path = data_root / "input_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["completed_computational_outputs"] = "contained_in_author_archives"
    manifest["optimized_stationary_points"] = "contained_in_author_archives"
    manifest["transition_states"] = "contained_in_author_archives"
    manifest["reaction_path_outputs"] = "stationary_point_profiles_contained_in_author_archives"
    manifest["author_output_archives"] = archive_records
    manifest["files"] = public_files(data_root)
    manifest_path.write_bytes(json_bytes(manifest))

    truth_path = TASKS_ROOT / task_id / "target_study" / "ground_truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    truth["current_toolbox_feasibility_baseline"] = {
        "assessment_date": "2026-07-28",
        "status": "validated_for_evaluation",
        "classification": "solvable",
        "paired_reproduction_reference_run_complete": True,
        "validated_artifact_root": "workspaces/paper_reproduction_recovery_20260727/pv",
        "known_limitations": [],
    }
    evidence = truth.setdefault("reference_evidence", {})
    evidence["source_boundary"] = (
        "Both tracks receive the same completed author outputs and experimental inputs; "
        "only the guided track receives the paper-reconstructed method and mapped route."
    )
    evidence["author_raw_outputs_public"] = True
    evidence["author_output_archives"] = archive_records
    evidence["input_manifest_sha256"] = sha256(manifest_path)
    truth_path.write_bytes(json_bytes(truth))


def build_one(open_task: str, reproduction_task: str, task_key: str, stage_root: Path) -> Path:
    source = TASKS_ROOT / open_task
    target = stage_root / reproduction_task
    shutil.copytree(source, target)

    data_root = target / "data" / "benchmark_data"
    author_states = TASK_AUTHOR_OUTPUT_STATES.get(task_key, ())
    protocol = deepcopy(COMPUTATIONAL_PROTOCOL)
    if author_states:
        protocol.update(
            {
                "protocol_type": "author_raw_output_reanalysis",
                "author_coordinates_included": True,
                "stationary_points_included": True,
                "author_quantum_outputs_included": True,
                "data_source": {
                    "doi": "10.5281/zenodo.1439888",
                    "states": list(author_states),
                    "contents": "Gaussian wB97XD frequency outputs and ORCA DLPNO-CCSD(T) single-point outputs",
                },
            }
        )
        protocol["geometry_and_frequency"]["required_operation"] = (
            "parse and independently validate the supplied completed outputs; rerunning "
            "the expensive optimizations is optional"
        )
        protocol["thermochemistry"]["toolbox_media_solvent"] = "ethanol"
    (data_root / "computational_protocol.json").write_bytes(json_bytes(protocol))

    archive_records = []
    for state in author_states:
        filename = AUTHOR_OUTPUT_ARCHIVES[state]
        source_archive = AUTHOR_OUTPUT_ROOT / filename
        destination_archive = data_root / "author_outputs" / filename
        destination_archive.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_archive, destination_archive)
        archive_records.append(
            {
                "state": state,
                "path": str(destination_archive.relative_to(data_root)),
                "sha256": sha256(destination_archive),
                "source_doi": "10.5281/zenodo.1439888",
            }
        )

    if task_key == "Q3":
        protocol["result_values_included"] = True
        (data_root / "publication_evidence.json").write_bytes(
            json_bytes(
                {
                    "paper_doi": "10.1126/science.aas8961",
                    "evidence_scope": "Figure S8 comparison reported by the publication",
                    "reported_activation_free_energies_kcal_mol": {
                        "P2_pyridyl_pyridyl_C_C": 14.0,
                        "P2_carbon_oxygen": 18.0,
                    },
                    "reported_delta_delta_g_dagger_co_minus_cc_kcal_mol": 4.0,
                    "public_archive_boundary": (
                        "Zenodo record 1439888 contains reanalyzable P2 C-C TS-I outputs "
                        "but no identified C-O TS frequency, IRC, or matched DLPNO output."
                    ),
                    "use_policy": (
                        "Recompute C-C from raw outputs; use 18 kcal/mol only as an "
                        "explicitly labeled publication benchmark."
                    ),
                }
            )
        )
    selected_paths = {path_id: deepcopy(PATHS[path_id]) for path_id in PATH_IDS[task_key]}
    (data_root / "reaction_definitions.json").write_bytes(
        json_bytes(
            {
                "schema_version": 1,
                "task_id": reproduction_task,
                "atom_labels": ATOM_LABELS,
                "result_values_included": task_key == "Q3",
                "author_coordinates_included": bool(author_states),
                "paths": selected_paths,
            }
        )
    )
    required_stages = WORKFLOW_STAGES
    if author_states:
        required_stages = [
            "verify archive hashes and extract the supplied author raw outputs",
            "pair each Gaussian frequency output with its matched ORCA DLPNO output",
            "validate molecular identity, charge, multiplicity, convergence, and stationary-point type",
            "validate barrier-defining forming and breaking bonds from the output geometry",
            "run GoodVibes at 353.15 K and 1 M with matched DLPNO corrections",
            "construct common-reference free-energy profiles and quantify uncertainty",
            "separate recomputed values from publication-reported evidence",
        ]
        if task_key == "Q3":
            required_stages.append("audit the public archive for the absent C-O stationary-point evidence")
        if task_key == "Q5":
            required_stages.append("integrate the P2 profile with the supplied kinetic and product observations")
    (data_root / "workflow_requirements.json").write_bytes(
        json_bytes(
            {
                "schema_version": 1,
                "mode": "guided_reproduction",
                "required_stages": required_stages,
                "failure_policy": "Retain failed analyses and never present a publication-only value as a calculation from this run.",
                "nbo_policy": "NBO is optional; equivalent bond-order, charge, geometry, and optional density evidence is accepted.",
                "author_output_archives": archive_records,
            }
        )
    )
    readme = data_root / "README.md"
    write_readme_section(
        readme,
        "Guided-reproduction additions",
        (
            "This task includes the author-deposited Gaussian frequency and ORCA DLPNO raw-output archives from Zenodo record 1439888. Independently parse, validate, and reanalyze those outputs; do not describe the publication's tabulated values as newly calculated.\n"
            if author_states
            else "This copied raw-input set contains a paper-reconstructed protocol and mapped routes but no author quantum outputs. Every numerical result must be regenerated.\n"
        ),
    )

    manifest_path = data_root / "input_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["task_id"] = reproduction_task
    manifest["task_mode"] = "guided_reproduction"
    manifest["method_protocol_files"] = ["computational_protocol.json"]
    manifest["reaction_definition_files"] = ["reaction_definitions.json"]
    manifest["workflow_requirement_files"] = ["workflow_requirements.json"]
    manifest["published_numerical_results"] = 2 if task_key == "Q3" else 0
    manifest["author_coordinates"] = int(bool(author_states))
    manifest["author_output_archives"] = archive_records
    manifest["completed_computational_outputs"] = "contained_in_author_archives" if author_states else 0
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
            "pathway_disclosure": "author_output_reanalysis" if author_states else "mapped_candidate_routes",
            "scientific_mode": "guided_reproduction",
            "scientific_mode_description": (
                "Author-deposited raw quantum-chemistry outputs and a paper-reconstructed analysis protocol are supplied. The Agent must independently validate and reanalyze them, create new managed analysis artifacts, and keep publication-only evidence separate."
                if author_states
                else "The paper-reconstructed method hierarchy and candidate reaction routes are supplied. The Agent must execute, debug, validate, and report the reproduction without reading hidden results."
            ),
            "task": REPRODUCTION_PROMPTS[task_key],
            "scientific_requirements": REPRODUCTION_REQUIREMENTS[task_key],
            "archive_extractions": [
                {
                    "source": f"benchmark_data/{record['path']}",
                    "format": "zip",
                    "destination": f"benchmark_data/extracted_author_outputs/{record['state']}",
                    "sha256": record["sha256"],
                }
                for record in archive_records
            ],
        }
    )
    info["data"] = [
        {
            "name": "Guided Heterobiaryl P(V) reproduction inputs",
            "path": "data/benchmark_data",
            "type": "directory",
            "description": (
                "Paper-reconstructed protocol and mapped pathways plus author-deposited Gaussian frequency and ORCA DLPNO raw outputs for independent validation and thermochemical reanalysis."
                if author_states
                else "Decontaminated raw structures and measurements plus a paper-reconstructed method protocol and mapped candidate pathways."
            ),
        }
    ]
    info_path.write_bytes(json_bytes(info))

    truth_path = target / "target_study" / "ground_truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    truth["evaluation_mode"] = "dual_axis_100"
    truth["evaluation_profile"] = "paper_reproduction"
    truth["score_max"] = 100
    truth["scoring_rubric"] = process_rubric(reproduction=True)
    truth["scientific_conclusion_rubric"] = scientific_conclusion_rubric(task_key)
    truth["dual_axis_scoring_policy"] = dual_axis_policy()
    truth["judge_instructions"] = (
        "Score each paper conclusion from newly generated evidence, then score reproduction-process "
        "quality separately. Methods, mapped routes, and selected author raw outputs are public, but "
        "publication values must not be presented as new calculations. The scorer applies the "
        "multiplicative dual-axis formula."
    )
    truth["reference_conclusion_gate_policy"] = {}
    truth["current_toolbox_reproduction_baseline"] = {
        **deepcopy(BASELINE_COMMON),
        **deepcopy(REPRODUCTION_BASELINES[task_key]),
        **(
            {
                "assessment_date": "2026-07-27",
                "status": "validated_author_output_reanalysis",
                "classification": "solvable",
                "major_paper_conclusion_reproduced_in_this_audit": True,
                "evidence_level": "toolbox_GoodVibes_reanalysis_of_author_Gaussian_and_ORCA_outputs",
                "validated_artifact_root": "workspaces/paper_reproduction_recovery_20260727/pv",
                "unresolved_requirements": (
                    [
                        "The public archive does not contain the C-O transition-state frequency, IRC, or matched DLPNO output; the C-O value is therefore publication evidence only."
                    ]
                    if task_key == "Q3"
                    else []
                ),
            }
            if author_states
            else {}
        ),
        "temperature_kelvin": 353.15,
        "standard_state_mol_l": 1.0,
    }
    evidence = truth.setdefault("reference_evidence", {})
    evidence["task_mode"] = "guided_reproduction"
    evidence["method_protocol_public"] = True
    evidence["mapped_candidate_routes_public"] = True
    evidence["published_reference_is_hidden_comparison_only"] = task_key != "Q3"
    evidence["author_raw_outputs_public"] = bool(author_states)
    evidence["author_output_archives"] = archive_records
    public_contract = evidence.setdefault("public_input_contract", {})
    if author_states:
        public_contract.update(
            {
                "completed_computational_outputs": "contained_in_author_archives",
                "optimized_stationary_points": "contained_in_author_archives",
                "raw_quantum_output_archives": len(archive_records),
            }
        )
    truth["critical_failures"] = [
        item
        for item in truth.get("critical_failures", [])
        if item != "The source publication or hidden reference material is searched or accessed."
    ]
    if task_key == "Q3":
        truth["expected_result"]["evidence_boundary"] = (
            "C-C is recomputed from supplied raw outputs; C-O=18 kcal/mol is publication-reported only."
        )
        truth["evidence_gate_policy"]["gates"] = [
            {
                "id": "cc_branch_reanalyzed",
                "score_cap_if_failed": 55,
                "requirement": "The C-C barrier is independently regenerated from the supplied Gaussian and matched DLPNO outputs with TS geometry/frequency validation.",
            },
            {
                "id": "co_evidence_boundary",
                "score_cap_if_failed": 60,
                "requirement": "The report identifies that the public archive lacks a C-O stationary-point package and labels 18 kcal/mol as publication evidence rather than a new computation.",
            },
            {
                "id": "comparison_provenance",
                "score_cap_if_failed": 70,
                "requirement": "The approximately 4 kcal/mol comparison keeps recomputed and literature-only quantities visibly distinct.",
            },
        ]
        truth["managed_computation_policy"]["minimum_successful_scientific_calls"] = 1
    evidence["input_manifest_sha256"] = sha256(manifest_path)
    truth_path.write_bytes(json_bytes(truth))
    return target


def main() -> int:
    update_open_metadata()
    align_open_author_output_inputs("Heterobiaryl_PV_02_CC_Selectivity", "Q2")
    align_open_author_output_inputs("Heterobiaryl_PV_05_Rate_Determining_Step", "Q5")
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

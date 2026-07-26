#!/usr/bin/env python3
"""Build autonomous-discovery counterparts for six reproduction tasks.

Visible inputs contain the scientific question, raw identities/structures, and
experimental conditions only.  They deliberately omit the paper protocol,
software DAG, author conformers, stationary-point candidates, optimized
adsorption geometries, and numerical paper conclusions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "tasks"
REPRO_IDS = (
    "GEOM_Hierarchical_Conformer_Reranking_Reproduction",
    "Electron_Flexible_Ensemble_Surface_Reproduction",
    "PV_Protonation_Barrier_Trend_Reproduction",
    "BaO_Phase_Crossover_And_5d_Bonding_Reproduction",
    "PV_CC_CO_Pathway_Selectivity_Reproduction",
    "NHC_Adsorption_Decomposition_Bonding_Reproduction",
)
TASK_IDS = tuple(task_id.removesuffix("_Reproduction") for task_id in REPRO_IDS)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_xyz_with_comment(source: Path, destination: Path, comment: str) -> None:
    lines = source.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        raise ValueError(f"Invalid XYZ file: {source}")
    lines[1] = comment
    write_text(destination, "\n".join(lines))


def copy_poscar_with_title(source: Path, destination: Path, title: str) -> None:
    lines = source.read_text(encoding="utf-8").splitlines()
    if len(lines) < 8:
        raise ValueError(f"Invalid POSCAR file: {source}")
    lines[0] = title
    write_text(destination, "\n".join(lines))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_task_root(task_id: str, force: bool) -> Path:
    root = TASKS_ROOT / task_id
    if root.exists():
        if not force:
            raise FileExistsError(f"{root} already exists; rerun with --force")
        shutil.rmtree(root)
    (root / "data" / "benchmark_data").mkdir(parents=True)
    (root / "target_study").mkdir(parents=True)
    return root


def file_record(data_root: Path, path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(data_root).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def common_deliverables(specific: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "path": "report/research_plan.json",
            "description": "Initial hypotheses, method alternatives, budgets, validation gates, stopping rules, and dated revisions.",
        },
        {
            "path": "report/tool_trace.jsonl",
            "description": "One provenance record for every real chemistry-software invocation.",
        },
        {
            "path": "report/evidence_summary.json",
            "description": "Claim-to-artifact map separating calculation, experiment, inference, and uncertainty.",
        },
        {
            "path": "report/failure_log.jsonl",
            "description": "Failed, rejected, retried, or inconclusive branches and their scientific consequence.",
            "allow_empty": True,
        },
        *specific,
        {
            "path": "report/report.md",
            "description": "Final artifact-linked scientific report with limitations and unresolved uncertainty.",
        },
    ]


def common_rubric() -> list[dict[str, Any]]:
    return [
        {
            "id": "scientific_problem_framing",
            "max_score": 15,
            "description": "Defines testable hypotheses, decision criteria, resource tiers, alternatives, and stopping rules without relying on a disclosed paper route.",
        },
        {
            "id": "autonomous_method_and_route_design",
            "max_score": 25,
            "description": "Independently selects defensible structures, software, methods, sampling, numerical controls, and fallback routes appropriate to the question.",
        },
        {
            "id": "adaptive_managed_execution",
            "max_score": 25,
            "description": "Executes real managed calculations, passes artifacts correctly, diagnoses failures, and revises the workflow without importing hidden results.",
        },
        {
            "id": "validation_and_falsification",
            "max_score": 20,
            "description": "Tests convergence, numerical sensitivity, chemical validity, competing explanations, uncertainty, and whether the evidence is sufficient for each claim.",
        },
        {
            "id": "defensible_scientific_conclusion",
            "max_score": 15,
            "description": "Draws a traceable conclusion from newly generated evidence. Hidden paper agreement is diagnostic, not a mandatory conclusion gate.",
        },
    ]


def task_info(
    *,
    task_id: str,
    source_id: str,
    category: str,
    benchmark_family: str,
    task: str,
    requirements: list[str],
    deliverables: list[dict[str, Any]],
    data_description: str,
) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "source_id": source_id,
        "category": category,
        "task": task,
        "scientific_mode": "focused_open_discovery",
        "scientific_mode_description": (
            "The scientific question and raw input boundary are fixed, but no paper method, "
            "software sequence, parameter protocol, candidate pathway, or stopping route is disclosed."
        ),
        "scientific_requirements": requirements,
        "required_deliverables": deliverables,
        "data": [
            {
                "name": "Autonomous multi-software research inputs",
                "path": "data/benchmark_data",
                "type": "directory",
                "description": data_description,
            }
        ],
        "archive_extractions": [],
        "benchmark_family": benchmark_family,
        "task_mode": "open_discovery",
        "method_disclosure": "none",
        "pathway_disclosure": "none",
    }


def ground_truth(
    *,
    task_id: str,
    paired_reproduction_task_id: str,
    expected_tool_calls: list[dict[str, Any]],
    hidden_reference: dict[str, Any],
    deliverables: list[dict[str, Any]],
    critical_failures: list[str],
    gates: list[dict[str, Any]],
    feasibility: dict[str, Any],
) -> dict[str, Any]:
    return {
        "expected_tool_calls": expected_tool_calls,
        "expected_result": {
            "hidden_posthoc_reference": hidden_reference,
            "reference_use_policy": (
                "Use the hidden paper result only after assessing autonomous planning, execution, "
                "validation, and evidence quality. Agreement is not required."
            ),
        },
        "expected_structured_output": [item["path"] for item in deliverables],
        "evaluation_mode": "rubric_100",
        "score_max": 100,
        "scoring_rubric": common_rubric(),
        "critical_failures": critical_failures,
        "judge_instructions": (
            "This is an autonomous-discovery evaluation. Reward independent hypothesis formation, "
            "method and route selection, adaptive managed execution, validation, falsification, and "
            "an evidence-bound conclusion. Do not require agreement with the hidden paper route or conclusion."
        ),
        "reference_evidence": {
            "task_id": task_id,
            "paired_reproduction_task_id": paired_reproduction_task_id,
            "task_mode": "open_discovery",
            "input_manifest_sha256": "PENDING",
            "hidden_posthoc_reference": hidden_reference,
            "source_boundary": (
                "Paper protocols, author intermediates, completed calculations, and numerical conclusions are evaluator-only."
            ),
            "reference_use_policy": (
                "Assess autonomous scientific process first; use the hidden reference only to diagnose scientific agreement or productive disagreement."
            ),
        },
        "managed_computation_policy": {
            "required": True,
            "allow_direct_native_software_execution": True,
            "parallel_execution_allowed": True,
            "do_not_fabricate_on_timeout": True,
            "require_workspace_confined_artifacts": True,
            "minimum_successful_scientific_calls": 2,
            "score_cap_without_managed_attempt": 20,
            "score_cap_without_successful_managed_call": 40,
        },
        "evidence_gate_policy": {"judge_must_assess_all": True, "gates": gates},
        "current_toolbox_feasibility_baseline": feasibility,
        "evaluation_profile": "autonomous_discovery",
        "reference_conclusion_gate_policy": {},
    }


def finalize_task(
    *,
    task_id: str,
    paired_reproduction_task_id: str,
    info: dict[str, Any],
    truth: dict[str, Any],
    metadata: dict[str, Any],
) -> None:
    root = TASKS_ROOT / task_id
    data_root = root / "data" / "benchmark_data"
    files = [
        file_record(data_root, path)
        for path in sorted(data_root.rglob("*"))
        if path.is_file() and path.name != "input_manifest.json"
    ]
    manifest = {
        "task_id": task_id,
        "task_mode": "open_discovery",
        "method_disclosure": "none",
        "pathway_disclosure": "none",
        "paper_result_values_in_visible_inputs": 0,
        "paper_protocol_files_in_visible_inputs": 0,
        "author_stationary_points_in_visible_inputs": 0,
        "completed_quantum_outputs": 0,
        "files": files,
        **metadata,
    }
    manifest_path = data_root / "input_manifest.json"
    write_json(manifest_path, manifest)
    truth["reference_evidence"]["input_manifest_sha256"] = sha256(manifest_path)
    write_json(root / "task_info.json", info)
    write_json(root / "target_study" / "ground_truth.json", truth)


def repro_truth(repro_id: str) -> dict[str, Any]:
    return json.loads(
        (TASKS_ROOT / repro_id / "target_study" / "ground_truth.json").read_text(encoding="utf-8")
    )


def build_geom(force: bool) -> None:
    task_id, repro_id = TASK_IDS[0], REPRO_IDS[0]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    write_text(
        data / "README.md",
        """# Autonomous conformer-energy investigation

Determine whether a low-cost conformer search gives a reliable thermally relevant
ranking for the supplied flexible molecule. Only molecular identity and physical
conditions are supplied. Choose the search, refinement, thermochemistry, alignment,
validation, and stopping strategy independently. No source-paper protocol,
conformers, software route, or result is included.
""",
    )
    write_json(
        data / "molecular_systems.json",
        {
            "systems": {
                "GEOM-C3": {
                    "smiles": "Nc1ncccc1NCc1ccccc1",
                    "charge": 0,
                    "multiplicity": 1,
                    "solvent": "water",
                    "temperature_kelvin": 298.15,
                }
            }
        },
    )
    deliverables = common_deliverables(
        [
            {"path": "report/conformer_lineage.csv", "description": "Generated conformers, identity checks, clustering, and parent lineage."},
            {"path": "report/ranking_comparison.csv", "description": "Aligned low-cost and refined energy/free-energy rankings with uncertainty."},
            {"path": "report/ensemble_conclusion.json", "description": "Dominant basins, population coverage, ranking stability, and stopping justification."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="geom_2022_autonomous_conformer_question",
        category="autonomous_conformer_search_and_reranking",
        benchmark_family="geom_conformer",
        task=(
            "Starting only from the supplied GEOM-C3 molecular identity and aqueous 298.15 K conditions, "
            "independently investigate whether an affordable conformer-search energy ranking is reliable "
            "for predicting the thermally important conformers. Generate the ensemble, choose validation "
            "and refinement levels, align structures across stages, quantify ranking/population changes, "
            "and state what can and cannot be concluded within the computational budget."
        ),
        requirements=[
            "Write competing hypotheses and a staged sampling/refinement plan before calculations.",
            "Generate structures in this run; no hidden or publication conformer may be imported.",
            "Preserve connectivity, atom mapping, and lineage when comparing rankings.",
            "Use calculation-backed convergence or population-coverage evidence to justify stopping.",
            "Test whether the main ranking conclusion survives at least one reasonable method or sampling perturbation.",
        ],
        deliverables=deliverables,
        data_description="One molecular identity and physical conditions; no conformers, protocol, software route, or reference energies.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "conformer_generation_or_search", "required": True},
            {"class": "energy_or_free_energy_refinement", "required": True},
            {"class": "structure_alignment_and_statistics", "required": True},
        ],
        hidden_reference=hidden,
        deliverables=deliverables,
        critical_failures=[
            "No real conformer search or generation was executed.",
            "Rankings were compared without identity-preserving structural alignment.",
            "Hidden/reference conformers or populations were presented as newly generated.",
            "A dominant-population claim relies only on unvalidated file order or a single unconverged search.",
        ],
        gates=[
            {"id": "real_search", "description": "A real multi-conformer search was executed.", "score_cap_if_failed": 35},
            {"id": "identity_and_lineage", "description": "Compared conformers retain connectivity and traceable lineage.", "score_cap_if_failed": 55},
            {"id": "independent_refinement", "description": "At least one higher-confidence calculation tests the low-cost ranking.", "score_cap_if_failed": 65},
        ],
        feasibility={
            "status": "pre_release_pilot_ready",
            "classification": "solvable_after_oracle_tolerance_calibration",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": ["Regenerated ensembles are stochastic; score basin coverage and ranking changes, not an exact legacy conformer count."],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"molecule_ids": ["GEOM-C3"], "starting_structure_count": 0})


def build_electron(force: bool) -> None:
    task_id, repro_id = TASK_IDS[1], REPRO_IDS[1]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    write_text(
        data / "README.md",
        """# Autonomous flexible-molecule surface investigation

Investigate how conformational flexibility affects an electron-density-derived
molecular surface for 1-pentanethiol and whether an ensemble treatment improves
agreement with the supplied experimental TE area. Only identity and experiment are
visible. Generate all structures and choose all electronic, numerical, and
statistical methods independently.
""",
    )
    write_json(
        data / "molecular_systems.json",
        {
            "systems": {
                "ISO-M6": {
                    "name": "1-pentanethiol",
                    "smiles": "CCCCCS",
                    "formula": "C5H12S",
                    "charge": 0,
                    "multiplicity": 1,
                    "experimental_te_surface_angstrom2": 156.507,
                    "temperature_kelvin": 298.15,
                }
            },
            "experimental_value_scope": "raw comparison target; not a computational protocol",
        },
    )
    deliverables = common_deliverables(
        [
            {"path": "report/conformer_sampling.csv", "description": "Generated conformers, clustering, energies, validation, and selection decisions."},
            {"path": "report/surface_evidence.csv", "description": "Per-conformer density/surface provenance and numerical controls."},
            {"path": "report/ensemble_surface.json", "description": "Single-structure and ensemble estimates, sensitivity, experiment comparison, and uncertainty."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="electron_isodensity_2024_autonomous_flexibility_question",
        category="autonomous_conformer_and_molecular_surface",
        benchmark_family="electron_isodensity_surface",
        task=(
            "Using only the supplied 1-pentanethiol identity and experimental TE surface area, independently "
            "determine whether conformational flexibility materially changes an electron-density-derived "
            "molecular surface and whether a thermally weighted ensemble is more defensible than a single "
            "structure. Generate all conformers, choose the density and isosurface methodology, validate "
            "numerical settings, quantify truncation and weighting uncertainty, and compare with experiment."
        ),
        requirements=[
            "Predeclare the conformer, electronic-density, surface-definition, and uncertainty plan before inspecting final agreement with experiment.",
            "Generate and validate multiple conformers in this run; do not import author conformers.",
            "Every reported surface must trace to a real wavefunction/density artifact and surface calculation.",
            "Test sensitivity to conformer truncation and at least one numerical surface control.",
            "Separate agreement with experiment from evidence that the chosen computational definition is physically appropriate.",
        ],
        deliverables=deliverables,
        data_description="One flexible molecule identity and its experimental TE surface area; no conformers, cutoff, density method, grid, or paper value.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "conformer_generation_or_search", "required": True},
            {"class": "electronic_structure_or_density", "required": True},
            {"class": "electron_isodensity_surface", "required": True},
            {"class": "ensemble_and_sensitivity_analysis", "required": True},
        ],
        hidden_reference=hidden,
        deliverables=deliverables,
        critical_failures=[
            "No real electronic-structure calculation was executed.",
            "No real electron-density isosurface calculation was executed.",
            "Publication conformers or hidden surface values were used as newly generated evidence.",
            "A single-conformer result was labeled an ensemble without computed weights.",
        ],
        gates=[
            {"id": "real_density_and_surface", "description": "New density and isosurface artifacts support the numerical results.", "score_cap_if_failed": 40},
            {"id": "independent_conformer_sampling", "description": "Multiple conformers were generated without author coordinates.", "score_cap_if_failed": 55},
            {"id": "ensemble_validity", "description": "Weights, normalization, truncation, and numerical sensitivity are addressed.", "score_cap_if_failed": 70},
        ],
        feasibility={
            "status": "pre_release_pilot_ready",
            "classification": "solvable",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": ["The paired reproduction task must lock its grid settings and regenerate a subset-specific oracle before formal ranking."],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"molecule_ids": ["ISO-M6"], "starting_structure_count": 0, "visible_experimental_measurement_count": 1})


def copy_pv_open_inputs(source_task: str, data: Path, include_measurements: bool) -> dict[str, Any]:
    source = TASKS_ROOT / source_task / "data" / "benchmark_data"
    copy_file(source / "conditions.json", data / "conditions.json")
    source_systems = json.loads((source / "molecular_systems.json").read_text(encoding="utf-8"))
    systems = source_systems["systems"]
    for record in systems.values():
        record.pop("generation_random_seed", None)
    write_json(
        data / "molecular_systems.json",
        {
            "schema_version": 1,
            "coordinate_status": "independent unoptimized embeddings with no stationary-point meaning",
            "atom_map": source_systems["atom_map"],
            "systems": systems,
        },
    )
    structures = []
    for path in sorted((source / "initial_structures").rglob("*.xyz")):
        destination = data / "initial_structures" / path.relative_to(source / "initial_structures")
        system_id = path.parent.name
        seed_id = path.stem
        copy_xyz_with_comment(
            path,
            destination,
            f"seed_id={seed_id} system={system_id} geometry_status=unoptimized charge_and_multiplicity_in_molecular_systems_json",
        )
        structures.append(destination.relative_to(data).as_posix())
    measurement_count = 0
    if include_measurements:
        measurement_source = source / "experimental_measurements" / "measurements.json"
        measurements = json.loads(measurement_source.read_text(encoding="utf-8"))
        measurements["data_type"] = "curated experimental measurements and non-detections"
        for measurement in measurements["measurements"]:
            measurement["measurement_scope"] = "experimental_measurement_or_non_detection"
        write_json(data / "experimental_measurements" / "measurements.json", measurements)
        measurement_count = len(measurements["measurements"])
    return {"starting_structures": structures, "measurement_count": measurement_count}


def build_pv_protonation(force: bool) -> None:
    task_id, repro_id = TASK_IDS[2], REPRO_IDS[2]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    records = copy_pv_open_inputs("Heterobiaryl_PV_01_Protonation", data, include_measurements=False)
    write_text(
        data / "README.md",
        """# Autonomous protonation-effect mechanism investigation

Determine whether and how protonation changes the kinetically relevant ligand-
coupling pathway for P0, P1, and P2 under the supplied conditions. The XYZ files are
independent unoptimized embeddings of reactant identities, not minima,
intermediates, transition states, or paper structures. Select all methods, pathway
hypotheses, validation tests, and stopping rules independently.
""",
    )
    deliverables = common_deliverables(
        [
            {"path": "report/state_screening.csv", "description": "P0/P1/P2 seed, protonation, conformer, and intermediate screening decisions."},
            {"path": "report/pathway_evidence.json", "description": "Per-state endpoints, bond changes, path/TS attempts, validation, and uncertainty."},
            {"path": "report/protonation_comparison.csv", "description": "Comparable energetic results or controlled bounds across P0/P1/P2."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="heterobiaryl_pv_2018_autonomous_protonation_question",
        category="autonomous_reaction_mechanism_and_protonation",
        benchmark_family="heterobiaryl_pv",
        task=(
            "For the supplied neutral, singly protonated, and doubly protonated P(V) reactant identities, "
            "independently determine whether protonation changes the kinetically relevant heterobiaryl "
            "coupling barrier under acidic ethanol conditions. Propose plausible mechanisms, generate and "
            "validate the needed intermediates and transition-path evidence, use comparable conventions "
            "across charge states, and report a trend only to the precision supported by new calculations."
        ),
        requirements=[
            "Write alternative mechanistic hypotheses and a comparable P0/P1/P2 protocol before pathway searches.",
            "Treat every supplied XYZ as an unoptimized reactant seed, never as a stationary point.",
            "A precise barrier requires a validated first-order saddle and connection evidence; otherwise report only a reproducible bracket or bound.",
            "Keep solvation, temperature, standard state, electronic treatment, and reference definitions comparable across protonation states.",
            "Preserve failed searches and explain whether missing evidence weakens or prevents a protonation-trend conclusion.",
        ],
        deliverables=deliverables,
        data_description="Nine unoptimized P0/P1/P2 reactant embeddings, molecular identities, atom mapping, and physical conditions; no intermediates, TS candidates, pathway labels, software route, or barriers.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "reactant_or_intermediate_screening", "required": True},
            {"class": "reaction_path_or_transition_state_search", "required": True},
            {"class": "frequency_and_connectivity_validation", "required": True},
            {"class": "comparable_free_energy_analysis", "required": True},
        ],
        hidden_reference=hidden,
        deliverables=deliverables,
        critical_failures=[
            "A supplied seed is described as an optimized minimum or transition state without a new calculation.",
            "A precise barrier is reported without first-order saddle and connection evidence.",
            "P0/P1/P2 comparisons mix incompatible references, conditions, or energy conventions.",
            "Hidden stationary points or literature barriers are presented as newly generated.",
        ],
        gates=[
            {"id": "state_comparability", "description": "All three protonation states use comparable conditions and references.", "score_cap_if_failed": 60},
            {"id": "pathway_validity", "description": "Claims are supported by validated paths/TSs or explicitly limited controlled bounds.", "score_cap_if_failed": 55},
            {"id": "three_state_evidence", "description": "Each state has a new managed computational attempt and an evidence-status conclusion.", "score_cap_if_failed": 70},
        ],
        feasibility={
            "status": "pre_release_blocked",
            "classification": "partially_solvable",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": [
                "The toolbox can attempt searches, but no curated closed reactant-TS-product mapping exists for all three states.",
                "This task must not enter formal model ranking until a feasible oracle route or defensible bound-based rubric is validated.",
            ],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"states": ["P0", "P1", "P2"], "starting_structure_count": len(records["starting_structures"]), "visible_experimental_measurement_count": 0})


def build_bao(force: bool) -> None:
    task_id, repro_id = TASK_IDS[3], REPRO_IDS[3]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    source_root = (
        TASKS_ROOT
        / "ResearchChemBench_Paper_Datasets"
        / "02_Guided_Paper_Reproduction_Benchmark"
        / "BaO_High_Pressure_Reproduction"
        / "01_agent_tasks_and_data"
        / "task_inputs"
        / "phase_structures"
    )
    phase_files = {
        "phase_A": "BaO_B1_Fm-3m.vasp",
        "phase_B": "BaO_B8_P63mmc.vasp",
        "phase_C": "BaO_dB2_P4nmm.vasp",
    }
    phase_records = []
    for public_id, filename in phase_files.items():
        destination = data / "candidate_phases" / f"{public_id}.vasp"
        copy_poscar_with_title(source_root / filename, destination, f"BaO opaque candidate {public_id}")
        phase_records.append({"phase_id": public_id, "path": destination.relative_to(data).as_posix()})
    write_text(
        data / "README.md",
        """# Autonomous BaO high-pressure investigation

Determine the pressure-dependent stability sequence among three supplied BaO
candidate crystals and investigate which electronic/bonding descriptors, if any,
provide a defensible explanation. The structures are unlabeled candidates. Choose
the pressure grid, relaxation strategy, convergence controls, thermodynamic model,
and optional bonding analysis independently. No paper protocol or result is visible.
""",
    )
    write_json(
        data / "candidate_phase_manifest.json",
        {
            "compound": "BaO",
            "candidate_phases": phase_records,
            "investigation_pressure_range_gpa": [0.0, 80.0],
            "phase_labels_are_opaque": True,
            "normalization_required": "per BaO formula unit",
        },
    )
    deliverables = common_deliverables(
        [
            {"path": "report/periodic_calculations.csv", "description": "Structures, pressures/volumes, convergence, energies, volumes, and stresses."},
            {"path": "report/phase_stability.json", "description": "Stable sequence, crossover estimates, interpolation uncertainty, and structural checks."},
            {"path": "report/bonding_hypotheses.json", "description": "Chosen electronic/bonding descriptors, validation, alternatives, and causal limitations."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="bao_2025_autonomous_high_pressure_question",
        category="autonomous_high_pressure_phase_and_bonding",
        benchmark_family="bao_high_pressure",
        task=(
            "Using the three supplied opaque BaO crystal candidates, independently determine the stable "
            "phase sequence between 0 and 80 GPa and estimate any crossover pressures. Then investigate "
            "whether an electronic-structure or bonding analysis can explain the observed structural "
            "preference, while distinguishing descriptive correlation from causal evidence."
        ),
        requirements=[
            "Choose and justify a pressure/volume sampling and refinement strategy with adaptive crossover refinement.",
            "Use compatible periodic settings and normalize energies/enthalpies per BaO formula unit.",
            "Validate structural identity after relaxation and do not silently compare collapsed phases.",
            "Quantify convergence and interpolation uncertainty for every crossover claim.",
            "Any orbital/bonding interpretation must be quality-gated and may not by itself prove energetic causation.",
        ],
        deliverables=deliverables,
        data_description="Three opaque BaO candidate crystal seeds and a 0-80 GPa investigation range; no volume grid, protocol, phase sequence, bonding basis, or transition pressure.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "periodic_relaxation_or_equation_of_state", "required": True},
            {"class": "enthalpy_and_crossover_analysis", "required": True},
            {"class": "optional_periodic_bonding_analysis", "required": False},
        ],
        hidden_reference=hidden,
        deliverables=deliverables,
        critical_failures=[
            "No real periodic electronic-structure calculation was executed.",
            "Energies or enthalpies were compared without formula-unit normalization.",
            "A relaxed structure changed phase identity but was retained without disclosure.",
            "Literature transition pressures or bonding values were presented as new results.",
        ],
        gates=[
            {"id": "periodic_evidence", "description": "New converged periodic calculations support the stability analysis.", "score_cap_if_failed": 35},
            {"id": "thermodynamic_consistency", "description": "Pressure/volume, PV units, references, and normalization are consistent.", "score_cap_if_failed": 55},
            {"id": "phase_identity", "description": "Relaxed candidates remain distinguishable or transformations are explicitly analyzed.", "score_cap_if_failed": 65},
        ],
        feasibility={
            "status": "pre_release_split_recommended",
            "classification": "phase_stability_solvable_bonding_blocked",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": [
                "The phase-stability part can be piloted after locking pseudopotentials and convergence settings.",
                "Fresh LOBSTER generation remains blocked by the POTCAR/native-job staging gap; bonding is optional and cannot be a hard completion gate yet.",
            ],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"compound": "BaO", "candidate_phase_count": 3, "starting_structure_count": 3})


def build_pv_selectivity(force: bool) -> None:
    task_id, repro_id = TASK_IDS[4], REPRO_IDS[4]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    records = copy_pv_open_inputs("Heterobiaryl_PV_03_CC_vs_CO", data, include_measurements=True)
    write_text(
        data / "README.md",
        """# Autonomous competing-pathway investigation

Independently compare carbon-carbon and carbon-oxygen coupling for the supplied P2
reactant under the stated conditions. The three XYZ files are unoptimized reactant
embeddings, not pathway endpoints or transition states. Experimental observations
are constraints, not computed barriers. Propose, generate, test, and revise both
pathway hypotheses without consulting the source publication.
""",
    )
    deliverables = common_deliverables(
        [
            {"path": "report/pathway_hypotheses.json", "description": "Atom-mapped C-C and C-O hypotheses, endpoints, alternatives, and falsification criteria."},
            {"path": "report/pathway_validation.json", "description": "Searches, scans/images, stationary-point tests, connectivity evidence, and failed branches."},
            {"path": "report/selectivity_comparison.json", "description": "Comparable barriers or controlled bounds, product prediction, experiment cross-check, and uncertainty."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="heterobiaryl_pv_2018_autonomous_cc_co_question",
        category="autonomous_competing_reaction_pathways",
        benchmark_family="heterobiaryl_pv",
        task=(
            "For the supplied doubly protonated P(V) reactant under acidic ethanol conditions, independently "
            "compare pyridyl-pyridyl carbon-carbon coupling with competitive carbon-oxygen coupling. Generate "
            "both pathway hypotheses and required structures, validate any transition-state claims, treat "
            "both paths comparably, and predict dominant/minor chemistry using new computation plus the "
            "supplied experimental constraints."
        ),
        requirements=[
            "Predeclare distinct atom-mapped C-C and C-O hypotheses, alternatives, validation tests, and stopping rules.",
            "Treat supplied XYZ files only as unoptimized reactant seeds.",
            "A path maximum is not a transition state without a relevant single imaginary mode and connection evidence.",
            "Compare the two paths with compatible electronic, solvation, thermal, standard-state, and reference conventions.",
            "If a path remains unresolved, report only a reproducible bracket/bound and preserve the failed attempts.",
        ],
        deliverables=deliverables,
        data_description="Three unoptimized P2 reactant embeddings, atom mapping, conditions, and four experimental observations; no products, pathway endpoints, TS candidates, software route, or barriers.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "reaction_path_or_coordinate_search", "required": True},
            {"class": "stationary_point_and_frequency_validation", "required": True},
            {"class": "comparable_kinetic_analysis", "required": True},
        ],
        hidden_reference=hidden,
        deliverables=deliverables,
        critical_failures=[
            "Only one competing pathway was attempted without a justified bound for the other.",
            "A supplied seed or path maximum was reported as a validated transition state.",
            "C-C and C-O results use incompatible reference or thermochemical conventions.",
            "Hidden/literature barriers were presented as new calculations.",
        ],
        gates=[
            {"id": "two_path_attempt", "description": "Both C-C and C-O hypotheses receive new managed computational tests.", "score_cap_if_failed": 55},
            {"id": "ts_or_bound_validity", "description": "Precise barriers are validated; otherwise conclusions are limited to controlled bounds.", "score_cap_if_failed": 60},
            {"id": "path_comparability", "description": "The two paths use compatible energetic and thermochemical conventions.", "score_cap_if_failed": 70},
        ],
        feasibility={
            "status": "pre_release_blocked",
            "classification": "partially_solvable",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": [
                "No curated pair of C-C/C-O endpoints and atom mappings has yet been reference-validated.",
                "The public pysisyphus ethanol-solvation contract is inconsistent with an older smoke record and must be reconciled.",
            ],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"states": ["P2"], "starting_structure_count": len(records["starting_structures"]), "visible_experimental_measurement_count": records["measurement_count"]})


def build_nhc(force: bool) -> None:
    task_id, repro_id = TASK_IDS[5], REPRO_IDS[5]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    repro_data = TASKS_ROOT / repro_id / "data" / "benchmark_data"
    systems: dict[str, Any] = {}
    for system_id in ("NHC1", "NHC4"):
        slab_source = repro_data / "clean_slabs" / f"{system_id}_matched_clean_slab.vasp"
        ligand_source = repro_data / "isolated_nhc_seeds" / f"{system_id}_detached_seed.xyz"
        slab_destination = data / "clean_surfaces" / f"surface_{system_id}.vasp"
        ligand_destination = data / "ligand_seeds" / f"ligand_{system_id}.xyz"
        copy_poscar_with_title(slab_source, slab_destination, f"Matched clean PdCu(111) surface for {system_id}")
        copy_xyz_with_comment(
            ligand_source,
            ligand_destination,
            f"{system_id} isolated neutral singlet ligand seed; unoptimized for this task",
        )
        systems[system_id] = {
            "clean_surface": slab_destination.relative_to(data).as_posix(),
            "isolated_ligand_seed": ligand_destination.relative_to(data).as_posix(),
            "charge": 0,
            "multiplicity": 1,
        }
    write_text(
        data / "README.md",
        """# Autonomous NHC/PdCu(111) adsorption investigation

Determine how two supplied NHC ligands adsorb on their matched PdCu(111) surfaces
and whether local metal-carbon bonding alone explains their relative adsorption
energetics. Only clean surfaces and isolated ligand seeds are supplied. Generate
adsorption sites/orientations and choose relaxation, reference, decomposition, and
bonding analyses independently. No optimized adsorbed structure is included.
""",
    )
    write_json(
        data / "system_manifest.json",
        {
            "systems": systems,
            "surface_and_ligand_pairs_are_matched": True,
            "adsorption_structures_supplied": 0,
            "binding_energy_sign_convention": "must be declared by the agent",
        },
    )
    deliverables = common_deliverables(
        [
            {"path": "report/adsorption_search.csv", "description": "Generated sites/orientations, screening, relaxation, identity, and convergence evidence."},
            {"path": "report/reference_energies.csv", "description": "Matched adsorbed, clean-surface, isolated-ligand, and optional frozen-fragment energies."},
            {"path": "report/adsorption_interpretation.json", "description": "Relative adsorption, deformation/interaction analysis, bonding evidence, and uncertainty."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="nhc_pdcu111_2025_autonomous_adsorption_question",
        category="autonomous_surface_adsorption_and_bonding",
        benchmark_family="nhc_pdcu111",
        task=(
            "Using only the two matched clean PdCu(111) surfaces and isolated NHC ligand seeds, independently "
            "determine plausible adsorption structures and compare the adsorption energetics of NHC1 and NHC4. "
            "Investigate whether local Pd-C bonding descriptors alone explain the total-energy difference, "
            "or whether geometry deformation and reference-state contributions are required."
        ),
        requirements=[
            "Generate and compare multiple physically distinct adsorption sites/orientations for each ligand.",
            "Use each ligand with its own matched clean-surface cell and compatible periodic settings.",
            "Declare and algebraically validate all adsorption, interaction, and deformation energy definitions.",
            "Respect surface-layer constraints and document which atoms were allowed to relax.",
            "Quality-gate any bonding analysis and distinguish local bond descriptors from total adsorption energetics.",
        ],
        deliverables=deliverables,
        data_description="Two matched clean PdCu(111) surfaces and two isolated ligand seeds; no adsorbed geometry, adsorption site, prescribed software route, computational protocol, or reference values.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "adsorption_structure_generation", "required": True},
            {"class": "periodic_relaxation_and_energy", "required": True},
            {"class": "matched_reference_or_energy_decomposition", "required": True},
            {"class": "optional_periodic_bonding_analysis", "required": False},
        ],
        hidden_reference=hidden,
        deliverables=deliverables,
        critical_failures=[
            "A hidden/published adsorbed structure was used as an independently generated result.",
            "Adsorption energies used unmatched surface cells or incompatible reference settings.",
            "No real periodic electronic-structure calculation was executed.",
            "Local bond metrics were treated as identical to total adsorption energy without decomposition or caveat.",
        ],
        gates=[
            {"id": "independent_adsorption_search", "description": "Multiple adsorption candidates were generated from clean surface and ligand inputs.", "score_cap_if_failed": 45},
            {"id": "matched_references", "description": "Adsorption comparisons use matched cells and compatible settings.", "score_cap_if_failed": 55},
            {"id": "constraint_and_geometry_validity", "description": "Relaxation constraints and final adsorption identity are verified.", "score_cap_if_failed": 65},
        ],
        feasibility={
            "status": "pre_release_blocked",
            "classification": "toolbox_gap",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": [
                "The public toolbox lacks a validated adsorption-placement workflow for these systems.",
                "VASP Selective Dynamics and POTCAR-to-native staging are not yet sufficient for the requested production protocol.",
                "Fresh LOBSTER generation remains blocked; bonding must remain optional until repaired.",
            ],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"system_ids": ["NHC1", "NHC4"], "clean_surface_count": 2, "isolated_ligand_seed_count": 2, "adsorbed_structure_count": 0})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="replace only the six generated autonomous task directories")
    args = parser.parse_args()
    build_geom(args.force)
    build_electron(args.force)
    build_pv_protonation(args.force)
    build_bao(args.force)
    build_pv_selectivity(args.force)
    build_nhc(args.force)
    print("Built autonomous tasks:")
    for task_id in TASK_IDS:
        print(f"- {task_id}")


if __name__ == "__main__":
    main()

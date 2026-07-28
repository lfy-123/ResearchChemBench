#!/usr/bin/env python3
"""Build six multi-software guided paper-reproduction tasks.

The generated tasks deliberately expose structures and paper-reconstructed methods,
but never expose paper result values. Hidden numerical targets live only under each
task's target_study directory.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.dual_axis import dual_axis_policy, process_rubric

TASKS_ROOT = ROOT / "tasks"
PAPER_ROOT = (
    TASKS_ROOT
    / "ResearchChemBench_Paper_Datasets"
    / "02_Guided_Paper_Reproduction_Benchmark"
)
PV_AUTHOR_OUTPUT_ROOT = (
    TASKS_ROOT
    / "_heterobiaryl_pv_shared"
    / "reference"
    / "author_computational_outputs"
)
PV_AUTHOR_OUTPUT_ARCHIVES = {
    "P0": "Int-I_unprotonated.zip",
    "P1": "Int-I_H_plus.zip",
    "P2": "Int-I_2H_2plus.zip",
}


TASK_IDS = (
    "GEOM_Hierarchical_Conformer_Reranking_Reproduction",
    "Electron_Flexible_Ensemble_Surface_Reproduction",
    "PV_Protonation_Barrier_Trend_Reproduction",
    "BaO_Phase_Crossover_And_5d_Bonding_Reproduction",
    "PV_CC_CO_Pathway_Selectivity_Reproduction",
    "NHC_Adsorption_Decomposition_Bonding_Reproduction",
)


SCIENTIFIC_CONCLUSION_RUBRICS: dict[str, list[dict[str, Any]]] = {
    "Electron_Flexible_Ensemble_Surface_Reproduction": [
        {
            "id": "conformer_surface_variation",
            "max_score": 35,
            "statement": "New density-isosurface calculations show that distinct ISO-M6 conformers have materially different molecular surface areas.",
            "acceptance_rule": "The conformer range or dispersion must exceed demonstrated grid/integration uncertainty and derive from valid per-conformer density artifacts; exact paper example values are not mandatory.",
            "required_evidence": ["multiple validated conformers", "per-conformer density and surface artifacts", "numerical surface sensitivity"],
        },
        {
            "id": "thermal_ensemble_reduces_single_structure_bias",
            "max_score": 35,
            "statement": "A normalized thermally weighted conformer ensemble is more defensible than an arbitrary single-conformer surface and reduces single-structure selection bias.",
            "acceptance_rule": "Require a converged or sensitivity-bounded conformer set and traceable thermal weights. Electronic-energy-only weights receive partial rather than full credit unless the approximation is quantitatively bounded.",
            "required_evidence": ["weighting energies or free energies", "normalization", "conformer truncation and weighting sensitivity"],
        },
        {
            "id": "paper_scale_ensemble_surface",
            "max_score": 30,
            "statement": "The recomputed ISO-M6 ensemble surface is consistent with the paper-scale result near 157.1994 A^2 and the TE reference 156.507 A^2 under the disclosed reproduction definition.",
            "acceptance_rule": "Full credit when the new estimate and uncertainty are compatible with the paper/TE neighborhood; partial credit for a justified controlled subset or protocol deviation that preserves the qualitative conclusion.",
            "required_evidence": ["new ensemble surface", "uncertainty or sensitivity interval", "post-computation reference comparison"],
        },
    ],
    "PV_Protonation_Barrier_Trend_Reproduction": [
        {
            "id": "successive_protonation_barrier_order",
            "max_score": 40,
            "statement": "The recomputed ligand-coupling activation free energies reproduce the P0 > P1 > P2 barrier order.",
            "acceptance_rule": "Require independent validation and GoodVibes reanalysis of the supplied author Gaussian frequency and ORCA DLPNO outputs under one 353.15 K, 1 M ethanol convention.",
            "required_evidence": ["validated P0/P1/P2 author outputs", "matched high-level energies", "aligned activation free energies"],
        },
        {
            "id": "stepwise_barrier_reduction_scale",
            "max_score": 35,
            "statement": "The recomputed barriers are compatible with the paper-scale 30, 20, and 14 kcal/mol values and show a large first reduction followed by a smaller second reduction.",
            "acceptance_rule": "Full credit requires uncertainty-compatible agreement with all three paper barriers and both reductions; controlled protocol deviations or incomplete candidate coverage receive partial credit only when the direction remains supported.",
            "required_evidence": ["three newly computed barrier values", "paper-versus-recomputation deviations", "candidate and low-frequency sensitivity"],
        },
        {
            "id": "exergonic_profiles_distinct_from_kinetic_trend",
            "max_score": 25,
            "statement": "All three coupling profiles remain strongly exergonic on a similar scale, so protonation primarily changes the kinetic barrier rather than reaction thermodynamics.",
            "acceptance_rule": "Require consistently referenced reaction free energies for P0, P1, and P2 from the supplied outputs; barrier ordering alone cannot receive this credit.",
            "required_evidence": ["reactant and product free energies for all states", "common thermochemical treatment", "kinetic-versus-thermodynamic interpretation"],
        },
    ],
    "BaO_Phase_Crossover_And_5d_Bonding_Reproduction": [
        {
            "id": "bao_phase_sequence",
            "max_score": 40,
            "statement": "The reconstructed VASP/EOS workflow reproduces the B1 -> B8 -> dB2 stability sequence over 0-80 GPa.",
            "acceptance_rule": "Require converged, consistently normalized calculations for all three supplied phases and phase-identity checks after relaxation or internal-coordinate refinement.",
            "required_evidence": ["new VASP E(V) data", "per-formula-unit normalization", "phase enthalpy comparison"],
        },
        {
            "id": "bao_first_transition_pressure",
            "max_score": 30,
            "statement": "Adaptive EOS/enthalpy analysis reproduces the B1 to B8 crossover within 6-12 GPa.",
            "acceptance_rule": "Require a refined crossing inside the interval with fit, convergence, and interpolation uncertainty; a copied value or unrefined grid endpoint receives no credit.",
            "required_evidence": ["physical EOS or controlled alternative", "refined B1-B8 crossing", "fit and convergence uncertainty"],
        },
        {
            "id": "bao_second_transition_pressure",
            "max_score": 30,
            "statement": "Adaptive EOS/enthalpy analysis reproduces the B8 to dB2 crossover within 20-30 GPa.",
            "acceptance_rule": "Require a refined crossing inside the interval with fixed-volume internal-coordinate relaxation and numerical uncertainty; a copied value or unrelaxed dB2 grid receives no credit.",
            "required_evidence": ["relaxed B8/dB2 E(V) data", "refined B8-dB2 crossing", "fit and convergence uncertainty"],
        },
    ],
    "PV_CC_CO_Pathway_Selectivity_Reproduction": [
        {
            "id": "validated_cc_reanalysis",
            "max_score": 30,
            "statement": "The P2 C-C barrier is independently regenerated from the supplied author Gaussian and ORCA outputs and the transition-state geometry is verified as C-C forming.",
            "acceptance_rule": "Require matched output parsing, one significant target imaginary frequency, forming-bond geometry, and a 353.15 K, 1 M GoodVibes barrier.",
            "required_evidence": ["validated C-C transition state", "matched DLPNO correction", "recomputed C-C barrier"],
        },
        {
            "id": "cc_preference_and_delta_delta_g",
            "max_score": 45,
            "statement": "The evidence-supported comparison reproduces C-C as kinetically preferred, with the publication-reported C-O barrier higher by approximately 4 kcal/mol.",
            "acceptance_rule": "Require a recomputed C-C barrier near 14 kcal/mol, an explicitly publication-labeled C-O value near 18 kcal/mol, and a provenance-correct approximately 4 kcal/mol comparison.",
            "required_evidence": ["new C-C activation free energy", "publication C-O evidence", "delta-delta-G with provenance"],
        },
        {
            "id": "co_archive_boundary",
            "max_score": 25,
            "statement": "The analysis correctly identifies that the public author archive does not contain the paper's C-O stationary-point package and therefore does not misrepresent the 18 kcal/mol value as a fresh calculation.",
            "acceptance_rule": "Require an archive audit, explicit missing-data statement, and a bounded conclusion consistent with the publication and supplied experiment.",
            "required_evidence": ["archive audit", "missing C-O raw-output statement", "experimental cross-check"],
        },
    ],
    "NHC_Adsorption_Decomposition_Bonding_Reproduction": [
        {
            "id": "nhc_published_metric_reanalysis",
            "max_score": 35,
            "statement": "Independent analysis of the supplied SI structures and paper table reproduces NHC4 as only modestly more strongly bound than NHC1.",
            "acceptance_rule": "Require structure-derived Pd-C distances, explicit 48-versus-36 metal-atom cell accounting, and calculations performed from the supplied table values rather than unlabelled copied prose.",
            "required_evidence": ["parsed SI structures", "cell and atom-count audit", "binding-energy comparison"],
        },
        {
            "id": "nhc_local_bonding_reproduction",
            "max_score": 35,
            "statement": "The supplied LOBSTER metrics and structure-derived distances reproduce the stronger and shorter local Pd-C bond for NHC4 than NHC1.",
            "acceptance_rule": "Require explicit provenance to the paper/SI table, distance verification from coordinates, ICOHP/ICOBI comparison, and spilling-quality qualification. Values must remain labeled publication outputs, not fresh LOBSTER calculations.",
            "required_evidence": ["Pd-C distances", "published ICOHP/ICOBI comparison", "projection-quality metrics"],
        },
        {
            "id": "nhc_decomposition_interpretation",
            "max_score": 30,
            "statement": "The reanalysis shows that pairwise Pd-C ICOHP is not a total adsorption energy and that deformation and lateral terms must be considered with the binding energies.",
            "acceptance_rule": "Require arithmetic from the supplied deformation and lateral terms, conversion of the ICOHP difference only as a clearly labeled scale diagnostic, and a scientifically correct local-versus-total interpretation.",
            "required_evidence": ["deformation-term arithmetic", "lateral-interaction comparison", "local-versus-total energy analysis"],
        },
    ],
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_pv_author_archives(data: Path, states: tuple[str, ...]) -> list[dict[str, Any]]:
    records = []
    for state in states:
        filename = PV_AUTHOR_OUTPUT_ARCHIVES[state]
        source = PV_AUTHOR_OUTPUT_ROOT / filename
        destination = data / "author_outputs" / filename
        copy_file(source, destination)
        records.append(
            {
                "state": state,
                "path": destination.relative_to(data).as_posix(),
                "size_bytes": destination.stat().st_size,
                "sha256": sha256(destination),
                "source_doi": "10.5281/zenodo.1439888",
            }
        )
    return records


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(data_root: Path, path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(data_root).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def common_rubric() -> list[dict[str, Any]]:
    return [
        {
            "id": "paper_conclusion_agreement",
            "max_score": 55,
            "description": (
                "Newly generated evidence recovers the scoped paper conclusion. "
                "A conflicting ranking, phase sequence, barrier trend, selectivity, "
                "ensemble effect, or bonding interpretation is not a reproduction."
            ),
        },
        {
            "id": "multisoftware_orchestration",
            "max_score": 15,
            "description": (
                "Correctly composes the required software stages, passes artifacts "
                "between them, and respects dependency, retry, and stopping logic."
            ),
        },
        {
            "id": "intermediate_evidence_validity",
            "max_score": 15,
            "description": (
                "Validates chemical identity, convergence, stationary-point type, "
                "wavefunction or periodic-output quality, and rejects invalid branches."
            ),
        },
        {
            "id": "protocol_fidelity",
            "max_score": 5,
            "description": (
                "Follows the supplied paper-reconstructed protocol and clearly labels "
                "any controlled, version-compatible substitution."
            ),
        },
        {
            "id": "numerical_and_statistical_quality",
            "max_score": 5,
            "description": (
                "Uses consistent units, reference states, normalization, statistics, "
                "and uncertainty estimates."
            ),
        },
        {
            "id": "provenance_and_uncertainty",
            "max_score": 5,
            "description": (
                "Links every conclusion to artifacts and separates computation, paper "
                "targets, inference, failures, and unresolved uncertainty."
            ),
        },
    ]


def common_deliverables(specific: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "path": "report/research_plan.json",
            "description": "Initial hypotheses, software DAG, budgets, gates, and stopping rules.",
        },
        {
            "path": "report/tool_trace.jsonl",
            "description": "One provenance record for every chemistry-software invocation.",
        },
        {
            "path": "report/failure_log.jsonl",
            "description": "Failed, rejected, retried, or inconclusive branches.",
            "allow_empty": True,
        },
        *specific,
        {
            "path": "report/report.md",
            "description": "Artifact-linked paper-reproduction report and uncertainty analysis.",
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
) -> dict[str, Any]:
    requirements = list(requirements)
    if not any("server resources allow" in item for item in requirements):
        requirements.append(
            "When server resources allow, parallelize independent calculations and use substantial CPU and memory resources without oversubscribing the host."
        )
    return {
        "task_id": task_id,
        "source_id": source_id,
        "category": category,
        "task": task,
        "scientific_mode": "guided_reproduction",
        "scientific_mode_description": (
            "A scoped part of a published research workflow is supplied. The agent must "
            "orchestrate multiple chemistry programs, validate intermediate artifacts, "
            "and recover the paper conclusion from newly generated evidence."
        ),
        "scientific_requirements": requirements,
        "required_deliverables": deliverables,
        "data": [
            {
                "name": "Guided multi-software reproduction inputs",
                "path": "data/benchmark_data",
                "type": "directory",
                "description": (
                    "Visible structures, protocol, workflow gates, and manifests. No paper "
                    "result values or completed quantum-chemistry outputs are included."
                ),
            }
        ],
        "archive_extractions": [],
        "benchmark_family": benchmark_family,
        "task_mode": "guided_reproduction",
        "method_disclosure": "paper_reconstructed_protocol",
        "pathway_disclosure": "scoped_execution_route",
    }


def ground_truth(
    *,
    task_id: str,
    paper_doi: str,
    expected_tool_calls: list[dict[str, Any]],
    expected_result: dict[str, Any],
    deliverables: list[dict[str, Any]],
    critical_failures: list[str],
    gates: list[dict[str, Any]],
    baseline: dict[str, Any],
    scientific_conclusion_rubric: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if scientific_conclusion_rubric is None:
        scientific_conclusion_rubric = SCIENTIFIC_CONCLUSION_RUBRICS.get(task_id)
    dual_axis = bool(scientific_conclusion_rubric)
    result = {
        "expected_tool_calls": expected_tool_calls,
        "expected_result": expected_result,
        "expected_structured_output": [item["path"] for item in deliverables],
        "evaluation_mode": "dual_axis_100" if dual_axis else "rubric_100",
        "score_max": 100,
        "scoring_rubric": (
            process_rubric(reproduction=True) if dual_axis else common_rubric()
        ),
        **(
            {
                "scientific_conclusion_rubric": scientific_conclusion_rubric,
                "dual_axis_scoring_policy": dual_axis_policy(),
            }
            if dual_axis
            else {}
        ),
        "critical_failures": critical_failures,
        "judge_instructions": (
            "Evaluate every hidden paper claim independently from newly generated evidence, "
            "then evaluate reproduction-process quality separately. Do not copy conclusion "
            "deficiencies into the process axis or use process quality to excuse a wrong claim. "
            "The scorer applies the multiplicative formula."
            if dual_axis
            else (
                "Evaluate this as a multi-software paper reproduction. Do not award conclusion "
                "credit for copied paper values, invalid intermediates, or numerically plausible "
                "results unsupported by artifacts from this run. The paper-conclusion criterion is "
                "the majority of the score. Apply every evidence gate."
            )
        ),
        "reference_evidence": {
            "paper_doi": paper_doi,
            "task_id": task_id,
            "task_mode": "guided_reproduction",
            "input_manifest_sha256": "PENDING",
            "paper_reference": expected_result,
            "source_boundary": (
                "Paper numerical targets and reference-run results are evaluator-only."
            ),
        },
        "managed_computation_policy": {
            "allow_direct_native_software_execution": True,
            "parallel_execution_allowed": True,
            "do_not_fabricate_on_timeout": True,
            "require_workspace_confined_artifacts": True,
        },
        "evidence_gate_policy": (
            {} if dual_axis else {"judge_must_assess_all": True, "gates": gates}
        ),
        "current_toolbox_reproduction_baseline": baseline,
        "evaluation_profile": "paper_reproduction",
        "reference_conclusion_gate_policy": (
            {}
            if dual_axis
            else {
                "required": True,
                "criterion_id": "paper_conclusion_agreement",
                "score_cap_if_not_matched": 50,
                "score_cap_if_uncertain": 65,
                "score_cap_if_omitted": 50,
                "max_criterion_score_if_not_matched": 0,
                "max_criterion_score_if_uncertain": 12,
                "max_criterion_score_if_omitted": 0,
            }
        ),
    }
    return result


def read_xyz_atom_count(path: Path) -> int:
    return int(path.read_text(encoding="utf-8").splitlines()[0].strip())


def scaled_poscar(source: Path, destination: Path, volume_ratio: float) -> None:
    lines = source.read_text(encoding="utf-8").splitlines()
    linear = volume_ratio ** (1.0 / 3.0)
    for index in (2, 3, 4):
        values = [float(item) * linear for item in lines[index].split()]
        lines[index] = "  " + "  ".join(f"{value:.12f}" for value in values)
    lines[0] = f"{lines[0]} | volume_ratio={volume_ratio:.3f}"
    write_text(destination, "\n".join(lines))


def clean_slab_poscar(source: Path, destination: Path, metal_species_count: int = 2) -> dict[str, Any]:
    lines = source.read_text(encoding="utf-8").splitlines()
    species = lines[5].split()
    counts = [int(value) for value in lines[6].split()]
    coordinate_line = 7
    selective = lines[coordinate_line].strip().lower().startswith("s")
    if selective:
        coordinate_line += 1
    coordinate_mode = lines[coordinate_line]
    coordinate_start = coordinate_line + 1
    metal_count = sum(counts[:metal_species_count])
    header = lines[:5] + [
        "  " + "  ".join(species[:metal_species_count]),
        "  " + "  ".join(str(value) for value in counts[:metal_species_count]),
    ]
    if selective:
        header.append("Selective dynamics")
    header.append(coordinate_mode)
    coordinates = lines[coordinate_start : coordinate_start + metal_count]
    header[0] = f"Clean slab extracted from {source.name}"
    write_text(destination, "\n".join(header + coordinates))
    return {
        "metal_atom_count": metal_count,
        "adsorbate_atom_count": sum(counts[metal_species_count:]),
        "metal_atom_indices_1based": [1, metal_count],
        "adsorbate_atom_indices_1based": [metal_count + 1, sum(counts)],
        "species": species,
        "counts": counts,
    }


def finalize_task(
    *,
    task_id: str,
    info: dict[str, Any],
    truth: dict[str, Any],
    manifest_metadata: dict[str, Any],
    paper_result_values_in_visible_inputs: int = 0,
    completed_quantum_outputs: int | str = 0,
) -> None:
    task_root = TASKS_ROOT / task_id
    data_root = task_root / "data" / "benchmark_data"
    files = [
        file_record(data_root, path)
        for path in sorted(data_root.rglob("*"))
        if path.is_file() and path.name != "input_manifest.json"
    ]
    manifest = {
        "task_id": task_id,
        "task_mode": "guided_reproduction",
        "paper_result_values_in_visible_inputs": paper_result_values_in_visible_inputs,
        "completed_quantum_outputs": completed_quantum_outputs,
        "files": files,
        **manifest_metadata,
    }
    manifest_path = data_root / "input_manifest.json"
    write_json(manifest_path, manifest)
    truth["reference_evidence"]["input_manifest_sha256"] = sha256(manifest_path)
    write_json(task_root / "task_info.json", info)
    write_json(task_root / "target_study" / "ground_truth.json", truth)


def prepare_task_root(task_id: str, force: bool) -> Path:
    task_root = TASKS_ROOT / task_id
    if task_root.exists():
        if not force:
            raise FileExistsError(f"{task_root} already exists; rerun with --force")
        shutil.rmtree(task_root)
    (task_root / "data" / "benchmark_data").mkdir(parents=True)
    (task_root / "target_study").mkdir(parents=True)
    return task_root


def build_geom(force: bool) -> None:
    task_id = TASK_IDS[0]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    deliverables = common_deliverables(
        [
            {"path": "report/stage_summary.csv", "description": "Counts and failures by software stage."},
            {"path": "report/conformer_lineage.csv", "description": "Atom-mapped lineage from RDKit through quantum refinement."},
            {"path": "report/energy_ranking.csv", "description": "Aligned xTB, electronic-energy, and free-energy rankings."},
            {"path": "report/ensemble.json", "description": "Final relative free energies, weights, and population coverage."},
        ]
    )
    write_text(
        data / "README.md",
        """# GEOM hierarchical conformer reranking reproduction

Starting only from the supplied GEOM-C3 SMILES, reconstruct a thermally relevant
conformer ensemble. Use RDKit for diverse embedding and clustering, xTB/CREST for
low-cost exploration, ORCA for r2SCAN-3c/C-PCM(water) refinement and Hessians, and
GoodVibes for 298.15 K thermochemistry. The paper result values are hidden.

Paper: 10.1038/s41597-022-01288-4.
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
    write_json(
        data / "computational_protocol.json",
        {
            "paper_doi": "10.1038/s41597-022-01288-4",
            "software_dag": ["RDKit", "xTB", "CREST", "ORCA", "GoodVibes"],
            "rdkit": {"method": "ETKDG", "random_seeds": [17, 23, 41, 73], "max_embeddings_per_seed": 50, "preoptimization": "MMFF94s"},
            "initial_clustering": {"heavy_atom_rmsd_cutoff_angstrom": 0.5},
            "xtb_crest": {"method": "GFN2-xTB", "solvation_model": "ALPB", "solvent": "water", "energy_window_kcal_mol": 6.0},
            "quantum_refinement": {"backend": "ORCA", "method": "r2SCAN-3c", "solvation_model": "CPCM", "solvent": "water", "require_hessian": True},
            "thermochemistry": {"backend": "GoodVibes", "temperature_kelvin": 298.15, "population_normalization_required": True},
            "result_values_included": False,
        },
    )
    write_json(
        data / "workflow_requirements.json",
        {
            "required_stages": ["embedding", "force_field_preoptimization", "low_cost_search", "identity_aware_clustering", "quantum_refinement", "frequency_validation", "thermochemical_ensemble", "ranking_comparison"],
            "required_statistics": ["Spearman rank correlation", "Top-1 change", "Top-k overlap", "population coverage"],
            "hard_gates": ["No connectivity-changing conformer may enter the aligned ranking.", "Every final conformer must have an atom-mapped parent lineage.", "Significant imaginary frequencies must be reported and handled before population analysis."],
            "budget_rule": "The agent may limit ORCA refinement, but must justify the rule and estimate missed population.",
        },
    )
    info = task_info(
        task_id=task_id,
        source_id="geom_2022_energy_annotated_conformations",
        category="conformer_search_and_quantum_refinement",
        benchmark_family="geom_conformer_reproduction",
        task=("Starting from GEOM-C3 SMILES, orchestrate RDKit, xTB/CREST, ORCA, and GoodVibes to reconstruct the major conformer basins and test whether low-cost ranking agrees with the quantum free-energy ranking. Recover the paper conclusion that low-cost search provides coverage but quantum refinement can change the dominant conformer and populations."),
        requirements=["Run at least four distinct software stages from the supplied DAG.", "Preserve atom mapping and conformer lineage across every stage.", "Compare aligned rankings by atom-mapped structural basins; never compare unrelated file-order indices.", "Report how refinement-budget truncation affects the conclusion.", "When server resources allow, parallelize independent conformers and use substantial CPU resources without oversubscribing the host."],
        deliverables=deliverables,
    )
    truth = ground_truth(
        task_id=task_id,
        paper_doi="10.1038/s41597-022-01288-4",
        expected_tool_calls=[{"class": "conformer_generation", "backend_examples": ["rdkit_etkdg", "crest"]}, {"class": "geometry_optimization", "backend_examples": ["xtb", "orca"]}, {"class": "frequency_and_thermochemistry", "backend_examples": ["orca", "goodvibes"]}, {"class": "structure_alignment_and_statistics", "backend_examples": ["rdkit", "internal_statistics"]}],
        expected_result={"reference_molecule": "GEOM-C3", "scoped_acceptance_target": {"low_cost_search_covers_multiple_major_basins": True, "quantum_refinement_materially_changes_an_aligned_ranking_or_population_distribution": True, "exact_generated_conformer_count_required": False, "exact_file_order_index_required": False}, "conformer_identity_policy": "Match regenerated conformers as atom-mapped structural basins using connectivity, symmetry-aware heavy-atom alignment, and torsion fingerprints. File order and generated conformer indices have no scientific identity.", "paper_reference_diagnostics": {"reference_major_conformer_count": 7, "reference_lowest_free_energy_population_percent": 26.50143932748048, "paper_dataset_xtb_vs_r2scan3c_mae_kcal_mol": 1.96, "paper_dataset_mean_spearman": 0.39, "use_policy": "Diagnostic context only; regenerated stochastic ensembles are not required to reproduce these exact scalar values."}, "paper_conclusion": "GFN2-xTB/CREST covers major basins at low cost, but quantum refinement and thermochemistry can reorder conformers and materially change populations."},
        deliverables=deliverables,
        critical_failures=["No real conformer search was executed.", "No quantum refinement or Hessian evidence was generated.", "Rankings were compared without atom-mapped alignment.", "Reference conformers or hidden populations were presented as newly generated."],
        gates=[{"id": "real_multistage_search", "description": "At least RDKit, one xTB/CREST stage, ORCA, and thermochemistry were executed.", "score_cap_if_failed": 45}, {"id": "identity_and_lineage", "description": "Final conformers have valid connectivity and traceable parents.", "score_cap_if_failed": 55}, {"id": "frequency_validity", "description": "Final population analysis handles significant imaginary modes.", "score_cap_if_failed": 65}],
        scientific_conclusion_rubric=[
            {"id": "major_basin_coverage", "max_score": 30, "statement": "The low-cost RDKit/xTB/CREST stage recovers multiple major chemically valid conformer basins for GEOM-C3.", "acceptance_rule": "Require new identity-preserving search and clustering evidence covering multiple major basins; exact legacy conformer count and file order are not required.", "required_evidence": ["managed conformer search", "connectivity and lineage checks", "basin or clustering summary"]},
            {"id": "quantum_ranking_reorder", "max_score": 35, "statement": "Aligned higher-level quantum refinement materially changes the low-cost conformer ranking or dominant-basin assignment.", "acceptance_rule": "Require an atom-mapped aligned comparison supported by newly computed quantum energies; paper-dataset diagnostics are context rather than exact task targets.", "required_evidence": ["new quantum refinement", "identity-preserving alignment", "ranking statistic or dominant-basin comparison"]},
            {"id": "thermochemical_population_change", "max_score": 35, "statement": "Validated thermochemistry changes or materially sharpens the population distribution relative to the low-cost electronic-energy ranking.", "acceptance_rule": "Require frequency-validated thermal free energies and normalized populations. Exact legacy population is not required, but electronic-energy-only Boltzmann weights cannot receive full credit.", "required_evidence": ["frequency or Hessian validation", "thermal free energies at 298.15 K", "normalized population comparison"]},
        ],
        baseline={"status": "components_available_reference_run_required", "classification": "solvable", "major_paper_conclusion_reproduced_in_this_audit": False, "installed_software": ["RDKit", "xTB 6.7.1", "CREST 3.0.2", "ORCA 6.1.1", "GoodVibes 4.3.0"], "verified_components": ["RDKit and CREST conformer Actions", "xTB and ORCA optimization/Hessian Actions", "GoodVibes ensemble analysis"], "unresolved_requirements": ["A fresh end-to-end oracle run is required to set benchmark-specific numerical tolerances for the regenerated ensemble."]},
    )
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"molecule_ids": ["GEOM-C3"], "starting_structures": 0, "software_stage_count": 5})


def build_electron(force: bool) -> None:
    task_id = TASK_IDS[1]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    source_root = PAPER_ROOT / "Electron_Isodensity_Surface_Reproduction" / "01_agent_tasks_and_data" / "task_inputs" / "published_conformer_seeds" / "ISO-M6"
    destination_root = data / "published_conformers" / "ISO-M6"
    records = []
    for source in sorted(source_root.glob("*.xyz")):
        destination = destination_root / source.name
        copy_file(source, destination)
        records.append({"conformer_id": source.stem, "path": destination.relative_to(data).as_posix(), "atom_count": read_xyz_atom_count(destination)})
    deliverables = common_deliverables(
        [
            {"path": "report/conformer_selection.csv", "description": "Low-cost energies, clusters, and high-level selection decisions."},
            {"path": "report/thermochemical_weights.csv", "description": "Validated free energies and normalized weights."},
            {"path": "report/conformer_surfaces.csv", "description": "Density provenance and isodensity surface for each refined conformer."},
            {"path": "report/ensemble_surface.json", "description": "Lowest-conformer, ensemble, truncation, and uncertainty results."},
        ]
    )
    write_text(data / "README.md", """# Flexible-conformer electron-isodensity reproduction

Use the 25 published ISO-M6 conformers as a search pool. RDKit and xTB/CREST must
validate and cluster the pool; select 4-6 conformers for high-level refinement using
both energy and structural diversity. Obtain thermochemical weights, generate the
paper production density with ORCA, export a wavefunction, and calculate surfaces
with Multiwfn. Paper surface values are hidden.

Paper: 10.1038/s41467-024-50408-8.
""")
    write_json(data / "molecular_systems.json", {"systems": {"ISO-M6": {"name": "1-pentanethiol", "formula": "C5H12S", "charge": 0, "multiplicity": 1, "published_conformer_count": 25}}, "conformers": records})
    write_json(data / "computational_protocol.json", {"paper_doi": "10.1038/s41467-024-50408-8", "software_dag": ["RDKit", "xTB/CREST", "ORCA thermochemistry", "GoodVibes", "ORCA density export", "Multiwfn"], "screening": {"method": "GFN2-xTB", "allowed_solvation": ["gas", "ALPB"], "selection_count_min": 4, "selection_count_max": 6, "must_include_energy_and_diversity": True}, "weight_refinement": {"recommended_method": "r2SCAN-3c", "temperature_kelvin": 298.15, "backend": "ORCA+GoodVibes", "benchmark_defined_substitution": True}, "production_density": {"method": "DSD-PBEP86-D3BJ", "orbital_basis": "def2-QZVPD", "auxiliary_basis": "def2-TZVPD/C", "frozen_core": False, "pmodel": True, "scf_convergence": "VeryTightSCF", "stability_analysis": True, "density_type": "relaxed_mp2"}, "surface_analysis": {"backend": "Multiwfn", "locked_cutoff_au": 0.0016, "require_identical_grid_settings": True}, "result_values_included": False})
    write_json(data / "workflow_requirements.json", {"required_stages": ["identity_validation", "low_cost_energy_screen", "RMSD_or_dihedral_clustering", "budgeted_high_level_selection", "frequency_or_weight_validation", "correlated_density", "wavefunction_export", "isodensity_surface", "Boltzmann_aggregation"], "hard_gates": ["Weights must be derived from one declared energy/free-energy convention and sum to one.", "The density artifact must be relaxed_mp2 from the selected production method.", "Every surface must be linked to its wavefunction and conformer.", "The ensemble must include a truncation-sensitivity estimate."], "paper_scope_note": "This scoped subset tests conformer sensitivity. It must not claim to recalibrate the paper-wide density cutoff."})
    info = task_info(task_id=task_id, source_id="electron_isodensity_2024_flexible_ensemble", category="conformer_ensemble_electron_density_surface", benchmark_family="electron_isodensity_surface", task=("Orchestrate conformer validation and screening, thermochemical weighting, correlated-density generation, wavefunction conversion, and Multiwfn surface analysis for ISO-M6. Reproduce the paper conclusion that flexible conformers have materially different electron-isodensity surface areas and that an ensemble is scientifically preferable to an arbitrary single conformer."), requirements=["Use at least four different software backends, including ORCA and Multiwfn.", "Select 4-6 high-level conformers using both energy and structural diversity.", "Use the locked paper cutoff 0.0016 a.u.; do not recalibrate it on ISO-M6.", "Quantify conformer truncation uncertainty and compare ensemble with the lowest-free-energy conformer.", "Treat this as a scoped 4-6-conformer reproduction: do not claim exact reproduction of the paper's full 25-conformer aggregate.", "When server resources allow, run independent conformer calculations concurrently and use substantial CPU resources without oversubscribing the host."], deliverables=deliverables)
    truth = ground_truth(task_id=task_id, paper_doi="10.1038/s41467-024-50408-8", expected_tool_calls=[{"class": "conformer_validation_and_clustering", "backend_examples": ["rdkit", "crest"]}, {"class": "low_cost_energy", "backend_examples": ["xtb"]}, {"class": "thermochemistry", "backend_examples": ["orca", "goodvibes"]}, {"class": "correlated_density_and_export", "backend_examples": ["orca"]}, {"class": "electron_isodensity_surface", "backend_examples": ["multiwfn"]}], expected_result={"molecule_id": "ISO-M6", "scoped_acceptance_target": {"multiple_conformers_show_materially_different_newly_computed_surfaces": True, "a_traceable_thermally_weighted_ensemble_reduces_arbitrary_single_conformer_choice": True, "exact_full_25_conformer_aggregate_required": False}, "paper_reference_diagnostics": {"paper_published_conformer_count": 25, "paper_ensemble_surface_angstrom2": 157.1994, "paper_example_individual_surfaces_angstrom2": [159.8, 149.2], "paper_te_surface_angstrom2": 156.507, "use_policy": "Diagnostic comparison only for this 4-6-conformer controlled reproduction; exact equality is not required."}, "paper_conclusion": "For a flexible molecule, conformer-dependent surface areas differ materially; Boltzmann ensemble treatment reduces arbitrary single-conformer bias."}, deliverables=deliverables, critical_failures=["No real correlated-density calculation was executed.", "No real Multiwfn surface analysis was executed.", "Weights from mixed or undeclared energy conventions were combined.", "Paper surface values were copied as computed outputs."], gates=[{"id": "multisoftware_chain", "description": "Screening, thermochemistry, density export, and surface analysis all have real artifacts.", "score_cap_if_failed": 45}, {"id": "density_provenance", "description": "Each surface derives from the required relaxed double-hybrid density.", "score_cap_if_failed": 50}, {"id": "weight_validity", "description": "Weights use one convention, sum to one, and exclude invalid structures explicitly.", "score_cap_if_failed": 60}, {"id": "conformer_sensitivity", "description": "The conclusion is supported by newly computed conformer-level dispersion rather than paper examples.", "score_cap_if_failed": 55}], baseline={"status": "objective_components_verified_reference_run_required", "classification": "solvable", "major_paper_conclusion_reproduced_in_this_audit": False, "installed_software": ["RDKit", "xTB 6.7.1", "CREST 3.0.2", "ORCA 6.1.1", "GoodVibes 4.3.0", "Multiwfn 2026.7.15"], "verified_components": ["ORCA relaxed double-hybrid density", "WFN export", "Multiwfn isodensity surface", "GoodVibes ensemble analysis"], "unresolved_requirements": ["The paper does not uniquely specify the conformer weighting energy; this task declares r2SCAN-3c thermochemistry as a benchmark-defined controlled substitution.", "A fresh oracle run is required to set subset-specific surface and truncation tolerances."]})
    truth.update(
        {
            "evaluation_mode": "dual_axis_100",
            "scoring_rubric": process_rubric(reproduction=True),
            "scientific_conclusion_rubric": [
                {"id": "conformer_surface_variation", "max_score": 35, "statement": "New density-isosurface calculations show that distinct ISO-M6 conformers have materially different molecular surface areas.", "acceptance_rule": "The conformer range or dispersion must exceed demonstrated grid/integration uncertainty and derive from valid per-conformer density artifacts; exact paper example values are not mandatory.", "required_evidence": ["multiple validated conformers", "per-conformer density and surface artifacts", "numerical surface sensitivity"]},
                {"id": "thermal_ensemble_reduces_single_structure_bias", "max_score": 35, "statement": "A normalized thermally weighted conformer ensemble is more defensible than an arbitrary single-conformer surface and reduces single-structure selection bias.", "acceptance_rule": "Require a converged or sensitivity-bounded conformer set and traceable thermal weights. Electronic-energy-only weights receive partial rather than full credit unless the approximation is quantitatively bounded.", "required_evidence": ["weighting energies or free energies", "normalization", "conformer truncation and weighting sensitivity"]},
                {"id": "paper_scale_ensemble_surface", "max_score": 30, "statement": "The recomputed ISO-M6 ensemble surface is consistent with the paper-scale result near 157.1994 A^2 and the TE reference 156.507 A^2 under the disclosed reproduction definition.", "acceptance_rule": "Full credit when the new estimate and uncertainty are compatible with the paper/TE neighborhood; partial credit for a justified controlled subset or protocol deviation that preserves the qualitative conclusion.", "required_evidence": ["new ensemble surface", "uncertainty or sensitivity interval", "post-computation reference comparison"]},
            ],
            "dual_axis_scoring_policy": dual_axis_policy(),
            "judge_instructions": "Score the three hidden paper claims and the reproduction process independently; the scorer applies the multiplicative formula.",
            "evidence_gate_policy": {},
            "reference_conclusion_gate_policy": {},
        }
    )
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"molecule_ids": ["ISO-M6"], "published_conformer_count": len(records), "high_level_selection_count_range": [4, 6], "software_stage_count": 6})


def load_pv_candidates() -> list[dict[str, str]]:
    manifest = PAPER_ROOT / "Heterobiaryl_PV_Reproduction" / "01_agent_tasks_and_data" / "task_inputs" / "labeled_reproduction_structures.csv"
    with manifest.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_pv_candidates(data: Path, rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    source_root = PAPER_ROOT / "Heterobiaryl_PV_Reproduction" / "01_agent_tasks_and_data" / "task_inputs"
    records = []
    for row in rows:
        source = source_root / row["structure_file"]
        destination = data / "candidate_structures" / row["system"] / source.name
        copy_file(source, destination)
        records.append({"candidate_id": row["candidate_id"], "system": row["system"], "assigned_stage": row["assigned_stage"], "assigned_pathway": row["assigned_pathway"], "charge": int(row["charge"]), "multiplicity": int(row["multiplicity"]), "atom_count": read_xyz_atom_count(destination), "structure_file": destination.relative_to(data).as_posix()})
    return records


def pv_protocol() -> dict[str, Any]:
    return {"paper_doi": "10.1126/science.aas8961", "software_dag": ["RDKit/cclib", "Gaussian", "ORCA", "GoodVibes", "pysisyphus as needed"], "geometry_and_frequency": {"backend": "Gaussian 16", "method": "wB97XD", "basis": "6-31+G(d)", "solvation_model": "SMD", "solvent": "ethanol", "stable_point_imaginary_modes": 0, "transition_state_meaningful_imaginary_modes": 1}, "high_level_single_points": {"backend": "ORCA", "method": "DLPNO-CCSD(T)", "basis_pair": ["cc-pVDZ", "cc-pVTZ"], "target_interpretation": "cc-pV(DT)Z-compatible composite"}, "thermochemistry": {"backend": "GoodVibes", "temperature_kelvin": 353.15, "concentration_molar": 1.0, "solvent": "ethanol", "quasiharmonic_low_frequency_treatment": True}, "result_values_included": False, "author_quantum_outputs_included": False}


def build_pv_protonation(force: bool) -> None:
    task_id = TASK_IDS[2]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    records = copy_pv_candidates(data, load_pv_candidates())
    archive_records = copy_pv_author_archives(data, ("P0", "P1", "P2"))
    deliverables = common_deliverables([{"path": "report/candidate_screening.csv", "description": "Candidate selection, rejection, and stage assignment evidence."}, {"path": "report/stationary_point_validation.csv", "description": "Convergence and imaginary-mode validation."}, {"path": "report/protonation_profiles.csv", "description": "P0/P1/P2 electronic, thermal, and relative free energies."}, {"path": "report/barrier_trend.json", "description": "Barrier trend, sensitivity, and conclusion."}])
    write_text(data / "README.md", """# P(V) protonation-barrier reproduction

The task supplies the author's public Gaussian frequency and ORCA DLPNO output
archives for P0, P1, and P2, together with mapped candidate structures. Verify the
archive hashes, independently validate and match the raw outputs, and use GoodVibes
to regenerate the 353.15 K, 1 M activation-free-energy trend. Expensive stationary-
point rediscovery is optional rather than required.

Paper: 10.1126/science.aas8961.
""")
    write_json(data / "candidate_manifest.json", {"candidate_count": len(records), "candidates": records})
    protocol = pv_protocol()
    protocol.update({"mode": "author_raw_output_reanalysis", "author_quantum_outputs_included": True, "author_output_archives": archive_records})
    protocol["thermochemistry"]["media_solvent"] = "ethanol"
    write_json(data / "computational_protocol.json", protocol)
    write_json(data / "workflow_requirements.json", {"required_stages": ["archive_hash_validation", "Gaussian_ORCA_file_matching", "stationary_point_and_frequency_validation", "GoodVibes_353K_1M_reanalysis", "common_reference_profile_alignment", "full_profile_reaction_thermodynamics", "protonation_trend_analysis"], "hard_gates": ["Every precise barrier and reaction free energy must trace to supplied frequency outputs and matched DLPNO outputs.", "All three states must use one thermochemical convention.", "Publication values must not be presented as the new GoodVibes output."], "author_output_archives": archive_records})
    info = task_info(task_id=task_id, source_id="heterobiaryl_pv_2019_protonation_barriers", category="reaction_mechanism_and_thermochemistry", benchmark_family="heterobiaryl_pv", task="Independently validate and reanalyze the supplied author Gaussian and ORCA raw outputs for P0, P1, and P2 with GoodVibes. Reproduce the successive-protonation barrier trend under one 353.15 K, 1 M ethanol convention and distinguish the kinetic change from the reaction-free-energy trend.", requirements=["Verify all three archive hashes and output identities.", "Validate barrier- and reaction-energy-defining frequencies and matched DLPNO corrections.", "Use a common initial-state reference within each protonation state.", "Report activation and reaction free energies plus newly generated GoodVibes values separately from publication targets."], deliverables=deliverables)
    info["archive_extractions"] = [{"source": f"benchmark_data/{record['path']}", "format": "zip", "destination": f"benchmark_data/extracted_author_outputs/{record['state']}", "sha256": record["sha256"]} for record in archive_records]
    info["data"][0]["description"] = "Mapped candidates plus author-deposited Gaussian frequency and ORCA DLPNO raw-output archives from Zenodo 1439888."
    truth = ground_truth(task_id=task_id, paper_doi="10.1126/science.aas8961", expected_tool_calls=[{"class": "structure_and_output_validation", "backend_examples": ["cclib"]}, {"class": "thermochemical_profile", "backend_examples": ["goodvibes"]}], expected_result={"energy_unit": "kcal/mol", "paper_barriers": {"P0": 30, "P1": 20, "P2": 14}, "validated_reanalysis_barriers": {"P0": 30.9134, "P1": 19.8135, "P2": 14.3004}, "validated_reanalysis_reaction_free_energies": {"P0": -32.38, "P1": -30.53, "P2": -31.35}, "paper_conclusion": "Successive N-protonation lowers the BiPy coupling barrier by about 10 and then 6 kcal/mol while all three profiles remain similarly exergonic."}, deliverables=deliverables, critical_failures=["No managed GoodVibes reanalysis was executed.", "Gaussian and ORCA outputs were mismatched.", "Candidate stages or protonation states were mixed in one profile.", "Paper barriers were copied as recomputed values."], gates=[], baseline={"status": "validated_reproduction", "classification": "solvable", "major_paper_conclusion_reproduced_in_this_audit": True, "installed_software": ["cclib", "GoodVibes 4.3.0"], "verified_components": ["author output archive recovery", "stationary-point geometry and frequency audit", "GoodVibes barriers 30.9134, 19.8135, and 14.3004 kcal/mol", "full-profile reaction free energies near -32.38, -30.53, and -31.35 kcal/mol"], "validated_artifact_root": "workspaces/paper_reproduction_recovery_20260727/pv", "unresolved_requirements": []})
    truth["reference_evidence"]["source_boundary"] = "Author raw outputs are visible for independent reanalysis; publication targets remain evaluator-side comparison values."
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"candidate_count": len(records), "states": ["P0", "P1", "P2"], "software_stage_count": 2, "author_output_archives": archive_records}, completed_quantum_outputs="contained_in_author_archives")


def build_bao(force: bool) -> None:
    task_id = TASK_IDS[3]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    source_root = PAPER_ROOT / "BaO_High_Pressure_Reproduction" / "01_agent_tasks_and_data" / "task_inputs" / "phase_structures"
    phases = {"B1": source_root / "BaO_B1_Fm-3m.vasp", "B8": source_root / "BaO_B8_P63mmc.vasp", "dB2": source_root / "BaO_dB2_P4nmm.vasp"}
    ratios = [0.82, 0.88, 0.94, 1.0, 1.06]
    structures = []
    for phase, source in phases.items():
        for ratio in ratios:
            destination = data / "volume_structures" / phase / f"BaO_{phase}_V{ratio:.2f}.vasp"
            scaled_poscar(source, destination, ratio)
            structures.append({"phase": phase, "volume_ratio": ratio, "path": destination.relative_to(data).as_posix()})
    deliverables = common_deliverables([
        {"path": "report/structure_validation.csv", "description": "Space group, normalization, volume, and structural checks."},
        {"path": "report/eos_points.csv", "description": "VASP energies, stresses, convergence, and per-formula-unit normalization."},
        {"path": "report/phase_enthalpy.csv", "description": "Fitted enthalpy curves and adaptive crossover evidence."},
        {"path": "report/phase_conclusion.json", "description": "Phase sequence, transition estimates, and numerical uncertainty."},
    ])
    write_text(data / "README.md", """# BaO phase-crossover reproduction

Validate the supplied B1, B8, and dB2 volume grids, compute consistent PBE
energies and stresses with VASP, fit E(V), derive H(P), and refine the phase
crossings. This benchmark is intentionally limited to the phase-stability
conclusion because the paper's custom La-5d-on-Ba LOBSTER basis was not
published and cannot support a fully reproducible scored ablation.

Paper: 10.1002/chem.202501536.
""")
    write_json(data / "phase_volume_grid.json", {"compound": "BaO", "phases": ["B1", "B8", "dB2"], "volume_ratios": ratios, "structures": structures, "normalization": "per BaO formula unit"})
    write_json(data / "computational_protocol.json", {
        "paper_doi": "10.1002/chem.202501536",
        "software_dag": ["pymatgen/spglib", "VASP", "SciPy/internal EOS fitting"],
        "vasp": {"xc": "PBE", "encut_ev": 600, "paw_family": "vasp_paw_pbe_54", "k_points": {"B1": [5, 5, 5], "B8": [7, 7, 4], "dB2": [4, 4, 8]}, "required_outputs": ["energy", "stress", "volume", "convergence"]},
        "eos": {"allowed_models": ["Birch-Murnaghan", "Vinet"], "pressure_range_gpa": [0, 80], "adaptive_refinement_minimum_new_points": 3, "internal_coordinate_relaxation_required_for_B8_and_dB2": True},
        "scope_exclusion": "Ba 5d projection ablation is excluded because the complete custom basis is not public.",
        "result_values_included": False,
    })
    write_json(data / "workflow_requirements.json", {
        "required_stages": ["symmetry_and_formula_validation", "VASP_volume_grid", "fixed_volume_internal_coordinate_relaxation", "convergence_and_stress_check", "EOS_model_comparison", "enthalpy_minimization", "adaptive_crossing_refinement"],
        "hard_gates": ["All energies must be normalized per BaO formula unit.", "B8 and dB2 internal coordinates must be relaxed at fixed volume before final EOS fitting.", "A grid endpoint may not be reported as a transition pressure without refinement or uncertainty."],
    })
    info = task_info(
        task_id=task_id,
        source_id="bao_high_pressure_polymorphism_2025",
        category="high_pressure_phase_stability",
        benchmark_family="bao_high_pressure",
        task="Orchestrate crystal validation, VASP volume-grid calculations, fixed-volume internal relaxation, EOS/enthalpy analysis, and adaptive crossover refinement. Reproduce the BaO B1 to B8 to dB2 stability sequence and both paper-scale transition-pressure neighborhoods.",
        requirements=["Use all three phases and compute a traceable E(V) dataset with VASP.", "Relax B8 and dB2 internal coordinates at fixed volume before final EOS fitting.", "Fit at least one physical EOS and assess fit sensitivity.", "Refine both crossings and report convergence, fitting, and interpolation uncertainty."],
        deliverables=deliverables,
    )
    info["data"][0]["description"] = "Visible phase-volume structures and paper-reconstructed phase-stability protocol. Transition pressures remain evaluator-side targets."
    truth = ground_truth(
        task_id=task_id,
        paper_doi="10.1002/chem.202501536",
        expected_tool_calls=[{"class": "crystal_validation", "backend_examples": ["pymatgen", "spglib"]}, {"class": "periodic_electronic_structure", "backend_examples": ["vasp"]}, {"class": "equation_of_state_and_enthalpy", "backend_examples": ["scipy", "internal_statistics"]}],
        expected_result={"paper_phase_sequence": ["B1", "B8", "dB2"], "paper_transition_pressures_gpa": [8, 25], "benchmark_acceptance_intervals_gpa": [[6, 12], [20, 30]], "validated_reference_crossings_gpa": [6.0234, 28.9091], "paper_conclusion": "BaO follows the B1 to B8 to dB2 stability sequence over 0-80 GPa.", "scope_boundary": "The unpublished custom Ba 5d projection basis is outside this scored task."},
        deliverables=deliverables,
        critical_failures=["No real periodic DFT calculation was executed.", "Energies from different formula-unit normalizations were compared.", "Transition pressures were copied from the paper or assigned from grid endpoints.", "B8 or dB2 was used in the final EOS without required fixed-volume internal-coordinate relaxation."],
        gates=[],
        baseline={"status": "validated_reproduction", "classification": "solvable", "major_paper_conclusion_reproduced_in_this_audit": True, "installed_software": ["pymatgen", "spglib", "VASP 6.3.2", "SciPy"], "verified_components": ["15 VASP phase-volume calculations", "10 fixed-volume B8/dB2 internal relaxations", "Birch-Murnaghan EOS and enthalpy crossings at 6.023 and 28.909 GPa"], "validated_artifact_root": "workspaces/manual_reproduction_validation_20260727/bao", "unresolved_requirements": []},
    )
    truth["reference_evidence"]["source_boundary"] = "Phase sequence and transition targets are evaluator-side; the unpublished 5d projection basis is excluded from the task."
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"compound": "BaO", "phases": list(phases), "volume_structure_count": len(structures), "software_stage_count": 3, "publication_evidence_files": []})


def build_pv_selectivity(force: bool) -> None:
    task_id = TASK_IDS[4]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    rows = [row for row in load_pv_candidates() if row["system"] == "P2"]
    records = copy_pv_candidates(data, rows)
    archive_records = copy_pv_author_archives(data, ("P2",))
    source_experiment = PAPER_ROOT / "Heterobiaryl_PV_Reproduction" / "01_agent_tasks_and_data" / "experimental_evidence" / "experimental_observations.json"
    copy_file(source_experiment, data / "experimental_observations.json")
    deliverables = common_deliverables([{"path": "report/pathway_screening.csv", "description": "P2 C-C and C-O candidate/path decisions."}, {"path": "report/path_validation.json", "description": "Endpoint, image-continuity, imaginary-mode, and IRC evidence."}, {"path": "report/competing_profiles.csv", "description": "Aligned C-C and C-O free-energy profiles."}, {"path": "report/selectivity_conclusion.json", "description": "Delta-delta-G, estimated rate ratio, experimental consistency, and uncertainty."}])
    write_text(data / "README.md", """# P(V) C-C versus C-O pathway-selectivity reproduction

Reanalyze the supplied official P2 author-output archive to reproduce the validated
pyridyl-pyridyl C-C free-energy barrier. Compare it with the source-labeled C-O
barrier reported in the paper and explain the resulting selectivity. The public
author archive contains five C-C TS-I candidates but no C-O transition-state output,
so the C-O value is publication evidence rather than a fresh calculation.

Paper: 10.1126/science.aas8961.
""")
    write_json(data / "candidate_manifest.json", {"candidate_count": len(records), "state": "P2", "candidates": records})
    write_json(data / "author_output_manifest.json", {"archives": archive_records})
    write_json(data / "publication_evidence.json", {
        "paper_doi": "10.1126/science.aas8961",
        "state": "P2",
        "barriers_kcal_mol": {"C-C": 14.0, "C-O": 18.0},
        "delta_delta_g_dagger_C-O_minus_C-C_kcal_mol": 4.0,
        "source_boundary": "The C-O value is a reported publication result. No C-O transition-state output is present in the public Zenodo author archive.",
    })
    protocol = pv_protocol()
    protocol["mode"] = "author_output_reanalysis_with_publication_comparator"
    protocol["result_values_included"] = True
    protocol["thermochemistry"]["media_solvent"] = "ethanol"
    protocol["path_search"] = {
        "backend": "pysisyphus",
        "low_cost_calculator": "GFN2-xTB",
        "solvation_model": "ALPB",
        "solvent": "methanol",
        "version_compatibility_note": (
            "xTB 6.7 has no ALPB ethanol parameters. Use ALPB methanol only as a "
            "low-cost protic-solvent path-search proxy; all formal Gaussian/ORCA/GoodVibes "
            "barriers remain evaluated with the disclosed ethanol convention."
        ),
        "accepted_methods": ["NEB", "growing string", "relaxed coordinate scan", "IRC from validated TS"],
    }
    write_json(data / "computational_protocol.json", protocol)
    write_json(data / "workflow_requirements.json", {
        "required_stages": ["author_archive_hash_validation", "Gaussian_frequency_parsing", "ORCA_single_point_parsing", "GoodVibes_C-C_profile", "publication_C-O_evidence_audit", "kinetic_selectivity_analysis", "experimental_cross_check"],
        "hard_gates": ["The P2 C-C barrier must be recomputed from the supplied Gaussian and ORCA outputs.", "The C-C profile must use a single disclosed reference and thermochemical convention.", "The publication C-O barrier must remain labeled as literature evidence because its raw TS output is absent.", "Archive filenames or configuration labels must not be interpreted as proof of C-O connectivity."],
        "rate_ratio_note": "Any Eyring ratio is an inference with equal-prefactor assumptions, not a directly measured product ratio.",
    })
    info = task_info(
        task_id=task_id,
        source_id="heterobiaryl_pv_2019_cc_co_selectivity",
        category="author_output_thermochemistry_and_evidence_audit",
        benchmark_family="heterobiaryl_pv",
        task="Use the official P2 author-output archive to reproduce the validated pyridyl-pyridyl C-C barrier, then compare it with the explicitly source-labeled publication C-O barrier and reproduce the conclusion that C-C coupling is kinetically preferred.",
        requirements=["Validate and extract the supplied P2 author archive.", "Recompute the C-C barrier from Gaussian frequencies and ORCA single-point outputs using the disclosed ethanol thermochemistry.", "Treat the 18 kcal/mol C-O barrier as publication evidence, not a fresh result.", "Audit the public archive and report that it contains no C-O transition-state output."],
        deliverables=deliverables,
    )
    info["data"][0]["description"] = "Official P2 author computational outputs, candidate structures, experimental observations, and a source-labeled publication C-O comparator."
    info["archive_extractions"] = [{"source": f"benchmark_data/{record['path']}", "format": "zip", "destination": f"benchmark_data/extracted_author_outputs/{record['state']}", "sha256": record["sha256"]} for record in archive_records]
    truth = ground_truth(
        task_id=task_id,
        paper_doi="10.1126/science.aas8961",
        expected_tool_calls=[{"class": "archive_and_output_validation", "backend_examples": ["internal_file_parser"]}, {"class": "stationary_point_frequency", "backend_examples": ["gaussian output parser"]}, {"class": "high_level_single_point", "backend_examples": ["orca output parser"]}, {"class": "thermochemical_selectivity", "backend_examples": ["goodvibes"]}],
        expected_result={"state": "P2", "paper_cc_barrier_kcal_mol": 14.0, "validated_author_output_cc_barrier_kcal_mol": 14.3004, "paper_co_barrier_kcal_mol": 18.0, "paper_delta_delta_g_dagger_co_minus_cc_kcal_mol": 4.0, "raw_output_boundary": "C-O TS output absent from public author archive", "paper_conclusion": "C-C coupling is kinetically preferred; C-O is accessible but suppressed under the standard acidic ethanol conditions."},
        deliverables=deliverables,
        critical_failures=["No managed P2 author-output analysis was executed.", "The publication C-O barrier was presented as a fresh calculation.", "A filename or configuration label was treated as proof of C-O connectivity.", "The C-C barrier used inconsistent references or thermochemistry."],
        gates=[{"id": "cc_author_output_reanalysis", "description": "The C-C barrier is recomputed from the supplied author outputs.", "score_cap_if_failed": 50}, {"id": "co_source_boundary", "description": "The C-O comparator remains explicitly labeled publication evidence.", "score_cap_if_failed": 60}, {"id": "archive_connectivity_audit", "description": "The absence of a public C-O TS output is correctly reported.", "score_cap_if_failed": 70}],
        baseline={"status": "validated_reproduction", "classification": "solvable", "major_paper_conclusion_reproduced_in_this_audit": True, "installed_software": ["Gaussian output parser", "ORCA output parser", "GoodVibes 4.3.0"], "verified_components": ["Official P2 Zenodo archive hash and contents", "P2 C-C common-reference barrier of 14.3004 kcal/mol", "public archive connectivity audit", "paper C-O comparator and experimental consistency"], "validated_artifact_root": "workspaces/paper_reproduction_recovery_20260727/pv", "unresolved_requirements": ["A fresh C-O barrier cannot be required unless a C-O TS output or a fully specified starting path is added."]},
    )
    truth["reference_evidence"]["source_boundary"] = "C-C is recomputed from visible author outputs; C-O=18 kcal/mol is visible publication evidence and must stay labeled as such."
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"candidate_count": len(records), "states": ["P2"], "experimental_observation_file_count": 1, "author_archive_count": len(archive_records), "publication_evidence_files": ["publication_evidence.json"], "software_stage_count": 4}, paper_result_values_in_visible_inputs=2, completed_quantum_outputs="official_P2_author_archive")


def build_nhc(force: bool) -> None:
    task_id = TASK_IDS[5]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    source_root = PAPER_ROOT / "NHC_PdCu111_Reproduction" / "01_agent_tasks_and_data" / "task_inputs"
    systems = {}
    for system_id in ("NHC1", "NHC4"):
        ads_source = source_root / "published_adsorbed_starting_structures" / f"{system_id}_published_adsorbed_start.vasp"
        mol_source = source_root / "isolated_nhc_seeds" / f"{system_id}_detached_seed.xyz"
        ads_destination = data / "adsorbed_structures" / ads_source.name
        mol_destination = data / "isolated_nhc_seeds" / mol_source.name
        slab_destination = data / "clean_slabs" / f"{system_id}_matched_clean_slab.vasp"
        copy_file(ads_source, ads_destination)
        copy_file(mol_source, mol_destination)
        fragments = clean_slab_poscar(ads_source, slab_destination)
        systems[system_id] = {"adsorbed_structure": ads_destination.relative_to(data).as_posix(), "isolated_seed": mol_destination.relative_to(data).as_posix(), "matched_clean_slab": slab_destination.relative_to(data).as_posix(), **fragments}
    deliverables = common_deliverables([
        {"path": "report/structure_validation.csv", "description": "Cell, metal-atom count, Pd site, constraints, and coordinate-derived Pd-C distances."},
        {"path": "report/energy_components.csv", "description": "Transcribed publication metrics with source labels and computed differences."},
        {"path": "report/binding_decomposition.json", "description": "Adsorbate/surface deformation sums, lateral terms, and local-versus-total comparison."},
        {"path": "report/lobster_bonding.csv", "description": "Publication ICOHP/ICOBI, charge, and spilling evidence with explicit provenance."},
        {"path": "report/adsorption_conclusion.json", "description": "Joint energetic and bonding interpretation."},
    ])
    write_text(data / "README.md", """# NHC/PdCu(111) adsorption decomposition and bonding reproduction

For NHC1 and NHC4, independently validate the published SI structures, metal-atom
counts, cells, and Pd-C distances. Reanalyze the supplied paper Table 3/Table 4 and
SI spilling values to quantify binding, deformation, lateral, ICOHP, and ICOBI
differences. Keep publication outputs labeled as such. A new 9x9x1 VASP-to-LOBSTER
campaign is an optional extension rather than a requirement for this bounded task.

Paper: 10.1021/acsomega.4c11197.
""")
    write_json(data / "system_manifest.json", {"systems": systems, "binding_energy_sign": "negative is favorable"})
    write_json(data / "paper_reference_metrics.json", {
        "paper_doi": "10.1021/acsomega.4c11197",
        "source_tables": ["Table 3", "Table 4", "Supporting Information charge-spilling table"],
        "units": {"energy": "kcal/mol", "icohp": "eV", "distance": "angstrom", "spilling": "percent"},
        "systems": {
            "NHC1": {"binding_energy": -43.0, "adsorbate_deformation": 0.68, "surface_deformation": 1.61, "lateral_interaction": -0.27, "pd_c_distance": 2.061, "icobi": 0.774, "icohp": -2.441, "lowdin_adsorbate_charge": -0.87, "absolute_charge_spilling": 1.84},
            "NHC4": {"binding_energy": -44.1, "adsorbate_deformation": 0.86, "surface_deformation": 1.16, "lateral_interaction": -0.08, "pd_c_distance": 2.043, "icobi": 1.050, "icohp": -3.349, "lowdin_adsorbate_charge": -1.42, "absolute_charge_spilling": 1.80},
        },
        "use_policy": "These are publication outputs for independent arithmetic and structure-consistency analysis, not fresh VASP or LOBSTER results.",
    })
    write_json(data / "computational_protocol.json", {
        "paper_doi": "10.1021/acsomega.4c11197",
        "mode": "published_structure_and_metric_reanalysis",
        "required_dag": ["periodic structure parsing", "Pd-C distance and cell audit", "publication table arithmetic", "local-versus-total bonding interpretation"],
        "paper_vasp_context": {"functional": "optPBE-vdW", "encut_ev": 500, "k_points": [9, 9, 1], "relaxation": "adsorbate and top metal layer; bottom two layers fixed"},
        "paper_lobster_context": {"metrics": ["ICOHP", "ICOBI", "Lowdin charge", "absolute charge spilling"], "preferred_spilling_threshold_percent": 2.0},
        "optional_extension": "Fresh matched-cell VASP and LOBSTER calculations may be added, but are not required for this bounded reproduction.",
        "result_values_included": True,
    })
    write_json(data / "workflow_requirements.json", {
        "required_stages": ["cell_and_atom_count_validation", "coordinate_derived_Pd_C_distance", "paper_metric_source_validation", "deformation_and_lateral_term_arithmetic", "ICOHP_ICOBI_and_spilling_comparison", "joint_local_versus_total_interpretation"],
        "hard_gates": ["NHC1 and NHC4 must retain their published 48- and 36-metal-atom cells, respectively.", "Pd-C distances must be measured from the supplied coordinates rather than copied from the metric table.", "Paper metrics must remain labeled publication outputs.", "ICOHP is a pairwise bonding descriptor and must not be treated as the total adsorption energy.", "Spilling quality must accompany every LOBSTER interpretation."],
    })
    info = task_info(
        task_id=task_id,
        source_id="nhc_pdcu111_2025_adsorption",
        category="surface_adsorption_structure_and_bonding_reanalysis",
        benchmark_family="nhc_pdcu111",
        task="Independently validate the supplied NHC1 and NHC4 SI structures, reproduce their Pd-C distances and cell-size provenance, and reanalyze the supplied publication binding, deformation, lateral, ICOHP, ICOBI, charge, and spilling metrics. Reproduce the conclusion that NHC4 has a stronger local Pd-C bond while the total adsorption-energy difference remains modest and cannot be inferred from pairwise ICOHP alone.",
        requirements=["Measure Pd-C distances and audit atom counts from both supplied structures.", "Compute binding, deformation, lateral, ICOHP, ICOBI, charge, and spilling differences from the supplied source-labeled metrics.", "Keep publication outputs separate from any optional fresh calculations.", "Explain the local-bond versus total-adsorption distinction without comparing raw total energies across the different cells."],
        deliverables=deliverables,
    )
    info["data"][0]["description"] = "Published SI structures for NHC1/NHC4 plus source-labeled Table 3/Table 4 and SI spilling metrics for independent structural and arithmetic reanalysis."
    truth = ground_truth(
        task_id=task_id,
        paper_doi="10.1021/acsomega.4c11197",
        expected_tool_calls=[{"class": "periodic_structure_validation", "backend_examples": ["pymatgen", "ASE"]}, {"class": "geometry_measurement", "backend_examples": ["pymatgen", "ASE"]}, {"class": "energy_and_bonding_reanalysis", "backend_examples": ["internal_statistics"]}],
        expected_result={"systems": {"NHC1": {"metal_atom_count": 48, "binding_energy_kcal_mol": -43.0, "adsorbate_deformation_kcal_mol": 0.68, "surface_deformation_kcal_mol": 1.61, "lateral_interaction_kcal_mol": -0.27, "pd_c_angstrom": 2.061, "icobi": 0.774, "icohp_ev": -2.441, "charge_spilling_percent": 1.84}, "NHC4": {"metal_atom_count": 36, "binding_energy_kcal_mol": -44.1, "adsorbate_deformation_kcal_mol": 0.86, "surface_deformation_kcal_mol": 1.16, "lateral_interaction_kcal_mol": -0.08, "pd_c_angstrom": 2.043, "icobi": 1.05, "icohp_ev": -3.349, "charge_spilling_percent": 1.8}}, "derived_comparison": {"binding_energy_difference_NHC4_minus_NHC1_kcal_mol": -1.1, "deformation_sum_NHC1_kcal_mol": 2.29, "deformation_sum_NHC4_kcal_mol": 2.02, "icohp_difference_NHC4_minus_NHC1_ev": -0.908}, "paper_conclusion": "NHC4 has stronger local Pd-C bonding indicators than NHC1, while the total binding-energy difference is modest and must be interpreted with deformation, lateral, and other total-energy contributions."},
        deliverables=deliverables,
        critical_failures=["No managed structure parsing or quantitative analysis was executed.", "The 48-atom NHC1 and 36-atom NHC4 surface cells were treated as one identical raw-energy reference.", "Publication metrics were presented as fresh VASP or LOBSTER calculations.", "Pairwise ICOHP was equated with total adsorption energy."],
        gates=[],
        baseline={"status": "validated_reproduction", "classification": "solvable", "major_paper_conclusion_reproduced_in_this_audit": True, "installed_software": ["pymatgen", "ASE", "VASP 6.3.2", "LOBSTER 5.1.0"], "verified_components": ["SI structure parsing", "NHC1/NHC4 metal-atom count audit", "coordinate-derived Pd-C distances of 2.057 and 2.043 A", "paper Table 3/Table 4 arithmetic"], "validated_artifact_root": "workspaces/paper_reproduction_recovery_20260727/nhc", "unresolved_requirements": ["A fresh full 9x9x1 optPBE-vdW VASP-to-LOBSTER chain remains a high-budget optional extension."]},
    )
    truth["reference_evidence"]["source_boundary"] = "The visible metric file contains publication outputs for reanalysis; they must not be called fresh DFT or LOBSTER results."
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"system_ids": ["NHC1", "NHC4"], "adsorbed_structure_count": 2, "clean_slab_count": 2, "isolated_seed_count": 2, "software_stage_count": 3, "publication_evidence_files": ["paper_reference_metrics.json"]}, paper_result_values_in_visible_inputs=16, completed_quantum_outputs="published_SI_structures_and_metrics")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="replace only the six generated task directories")
    args = parser.parse_args()
    build_geom(args.force)
    build_electron(args.force)
    build_pv_protonation(args.force)
    build_bao(args.force)
    build_pv_selectivity(args.force)
    build_nhc(args.force)
    print("Built tasks:")
    for task_id in TASK_IDS:
        print(f"- {task_id}")


if __name__ == "__main__":
    main()

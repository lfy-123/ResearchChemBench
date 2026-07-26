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
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "tasks"
PAPER_ROOT = (
    TASKS_ROOT
    / "ResearchChemBench_Paper_Datasets"
    / "02_Guided_Paper_Reproduction_Benchmark"
)


TASK_IDS = (
    "GEOM_Hierarchical_Conformer_Reranking_Reproduction",
    "Electron_Flexible_Ensemble_Surface_Reproduction",
    "PV_Protonation_Barrier_Trend_Reproduction",
    "BaO_Phase_Crossover_And_5d_Bonding_Reproduction",
    "PV_CC_CO_Pathway_Selectivity_Reproduction",
    "NHC_Adsorption_Decomposition_Bonding_Reproduction",
)


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
) -> dict[str, Any]:
    return {
        "expected_tool_calls": expected_tool_calls,
        "expected_result": expected_result,
        "expected_structured_output": [item["path"] for item in deliverables],
        "evaluation_mode": "rubric_100",
        "score_max": 100,
        "scoring_rubric": common_rubric(),
        "critical_failures": critical_failures,
        "judge_instructions": (
            "Evaluate this as a multi-software paper reproduction. Do not award conclusion "
            "credit for copied paper values, invalid intermediates, or numerically plausible "
            "results unsupported by artifacts from this run. The paper-conclusion criterion is "
            "the majority of the score. Apply every evidence gate."
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
        "evidence_gate_policy": {"judge_must_assess_all": True, "gates": gates},
        "current_toolbox_reproduction_baseline": baseline,
        "evaluation_profile": "paper_reproduction",
        "reference_conclusion_gate_policy": {
            "required": True,
            "criterion_id": "paper_conclusion_agreement",
            "score_cap_if_not_matched": 50,
            "score_cap_if_uncertain": 65,
            "score_cap_if_omitted": 50,
            "max_criterion_score_if_not_matched": 0,
            "max_criterion_score_if_uncertain": 12,
            "max_criterion_score_if_omitted": 0,
        },
    }


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
        "paper_result_values_in_visible_inputs": 0,
        "completed_quantum_outputs": 0,
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
    deliverables = common_deliverables([{"path": "report/candidate_screening.csv", "description": "Candidate selection, rejection, and stage assignment evidence."}, {"path": "report/stationary_point_validation.csv", "description": "Convergence and imaginary-mode validation."}, {"path": "report/protonation_profiles.csv", "description": "P0/P1/P2 electronic, thermal, and relative free energies."}, {"path": "report/barrier_trend.json", "description": "Barrier trend, sensitivity, and conclusion."}])
    write_text(data / "README.md", """# P(V) protonation-barrier reproduction

The supplied XYZ files are published-coordinate candidates labeled by protonation
state and stationary-point stage. Screen candidates rather than calculating all of
them blindly. Revalidate selected stationary points, compute consistent high-level
single points, assemble 353.15 K free-energy profiles, and test whether successive
protonation lowers the ligand-coupling barrier. Numerical paper barriers are hidden.

Paper: 10.1126/science.aas8961.
""")
    write_json(data / "candidate_manifest.json", {"candidate_count": len(records), "candidates": records})
    write_json(data / "computational_protocol.json", pv_protocol())
    write_json(data / "workflow_requirements.json", {"required_stages": ["candidate_screening", "identity_and_charge_validation", "stationary_point_hessian", "high_level_single_points", "GoodVibes_thermochemistry", "profile_alignment", "protonation_trend_analysis"], "hard_gates": ["A TS without exactly one chemically relevant significant imaginary mode may not define a formal barrier.", "All three protonation profiles must use the same thermochemical convention.", "File matching between frequency and single-point calculations must be explicit.", "The agent must separate a paper-published trend from any benchmark-compatible substitution."], "budget_rule": "Use labels and low-cost screening to select a bounded consistent path; report excluded candidates and sensitivity."})
    info = task_info(task_id=task_id, source_id="heterobiaryl_pv_2019_protonation_barriers", category="reaction_mechanism_and_thermochemistry", benchmark_family="heterobiaryl_pv", task=("From the supplied P0/P1/P2 candidate structures, orchestrate candidate screening, Gaussian stationary-point validation, ORCA high-level single points, and GoodVibes thermochemistry to reconstruct comparable ligand-coupling free-energy profiles and reproduce the conclusion that successive protonation lowers the coupling barrier."), requirements=["Use candidates from all three protonation states and justify a consistent pathway alignment.", "Generate new frequency or Hessian evidence for every barrier-defining stationary point.", "Use ORCA high-level single points and GoodVibes rather than manually adding paper values.", "Report whether the trend survives reasonable low-frequency and candidate-selection sensitivity tests."], deliverables=deliverables)
    truth = ground_truth(task_id=task_id, paper_doi="10.1126/science.aas8961", expected_tool_calls=[{"class": "structure_and_output_validation", "backend_examples": ["rdkit", "cclib"]}, {"class": "stationary_point_frequency", "backend_examples": ["gaussian"]}, {"class": "high_level_single_point", "backend_examples": ["orca"]}, {"class": "thermochemical_profile", "backend_examples": ["goodvibes"]}], expected_result={"energy_unit": "kcal/mol", "paper_barriers": {"P0": 30, "P1": 20, "P2": 14}, "paper_reaction_free_energies": {"P0": -39, "P1": -37, "P2": -38}, "paper_conclusion": "Successive N-protonation lowers the BiPy coupling barrier by about 10 and then 6 kcal/mol."}, deliverables=deliverables, critical_failures=["No real Hessian/frequency validation was executed.", "No ORCA high-level single-point evidence was generated.", "Candidate stages or protonation states were mixed in one profile.", "Paper barriers were copied as recomputed values."], gates=[{"id": "stationary_point_validity", "description": "Barrier-defining TS and minima pass frequency gates.", "score_cap_if_failed": 45}, {"id": "profile_consistency", "description": "P0/P1/P2 use aligned stages and one thermochemical convention.", "score_cap_if_failed": 55}, {"id": "high_level_energy_evidence", "description": "Selected stationary points have traceable ORCA single points.", "score_cap_if_failed": 60}], baseline={"status": "partially_solvable_reference_run_required", "classification": "partially_solvable", "major_paper_conclusion_reproduced_in_this_audit": False, "installed_software": ["RDKit", "cclib", "Gaussian 16", "ORCA 6.1.1", "GoodVibes 4.3.0", "pysisyphus 1.0.0"], "verified_components": ["Gaussian energy/Hessian Actions", "ORCA molecular energy Actions", "GoodVibes profile Actions", "pysisyphus reaction-path smoke tests"], "unresolved_requirements": ["The public candidate collection is not a complete one-to-one set of paper main-path minima and transition states.", "A curated oracle path mapping and fresh composite-energy run are required before production scoring tolerances are activated."]})
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"candidate_count": len(records), "states": ["P0", "P1", "P2"], "software_stage_count": 5})


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
    deliverables = common_deliverables([{"path": "report/structure_validation.csv", "description": "Space group, normalization, volume, and structural checks."}, {"path": "report/eos_points.csv", "description": "VASP energies, stresses, convergence, and per-formula-unit normalization."}, {"path": "report/phase_enthalpy.csv", "description": "Fitted enthalpy curves and adaptive crossover evidence."}, {"path": "report/lobster_ablation.json", "description": "With/without Ba 5d spilling and bonding analysis."}, {"path": "report/phase_conclusion.json", "description": "Phase sequence, transition estimates, bonding interpretation, and uncertainty."}])
    write_text(data / "README.md", """# BaO phase-crossover and 5d-bonding reproduction

Validate the supplied B1, B8, and dB2 volume grids with pymatgen/spglib, compute
consistent PBE energies and stresses with VASP, fit E(V), derive H(P), and refine any
phase-crossing interval. On a representative converged B8 or dB2 wavefunction, run
paired LOBSTER projections with and without Ba 5d functions. Paper transition and
bonding numbers are hidden.

Paper: 10.1002/chem.202501536.
""")
    write_json(data / "phase_volume_grid.json", {"compound": "BaO", "phases": ["B1", "B8", "dB2"], "volume_ratios": ratios, "structures": structures, "normalization": "per BaO formula unit"})
    write_json(data / "computational_protocol.json", {"paper_doi": "10.1002/chem.202501536", "software_dag": ["pymatgen/spglib", "VASP", "SciPy/internal EOS fitting", "LOBSTER"], "vasp": {"xc": "PBE", "encut_ev": 600, "paw_family": "vasp_paw_pbe_54", "k_points": {"B1": [5, 5, 5], "B8": [7, 7, 4], "dB2": [4, 4, 8]}, "required_outputs": ["energy", "stress", "volume", "convergence", "wavefunction_for_selected_ablation"]}, "eos": {"allowed_models": ["Birch-Murnaghan", "Vinet"], "pressure_range_gpa": [0, 80], "adaptive_refinement_minimum_new_points": 3}, "lobster_ablation": {"paired_same_wavefunction": True, "control_projection": "Ba s,p plus O basis without explicit Ba 5d", "expanded_projection": "same basis plus Ba 5d", "compare": ["absolute_charge_spilling", "total_charge_spilling", "Ba-O ICOHP", "Ba 5d PDOS"]}, "result_values_included": False})
    write_json(data / "workflow_requirements.json", {"required_stages": ["symmetry_and_formula_validation", "VASP_volume_grid", "convergence_and_stress_check", "EOS_model_comparison", "enthalpy_minimization", "adaptive_crossing_refinement", "paired_LOBSTER_projection", "causal_interpretation"], "hard_gates": ["All energies must be normalized per BaO formula unit.", "A grid endpoint may not be reported as a transition pressure without refinement or uncertainty.", "The two LOBSTER projections must use the same VASP wavefunction.", "Spilling quality must be reported before interpreting ICOHP or PDOS."], "native_layer_note": "The current public LOBSTER Actions parse outputs. Generating new LOBSTER outputs requires the toolbox native-job layer until a dedicated run Action is added."})
    info = task_info(task_id=task_id, source_id="bao_high_pressure_polymorphism_2025", category="high_pressure_phase_stability_and_bonding", benchmark_family="bao_high_pressure", task=("Orchestrate crystal validation, VASP volume-grid calculations, EOS/enthalpy analysis, adaptive crossover refinement, and paired LOBSTER projection analysis to reproduce the BaO B1 to B8 to dB2 high-pressure sequence and test the role of Ba 5d functions in the bonding interpretation."), requirements=["Use all three phases and compute a traceable E(V) dataset with VASP.", "Fit at least one physical EOS and assess fit sensitivity.", "Adaptively refine every detected enthalpy crossing.", "Run paired LOBSTER projections on the same wavefunction and gate bonding conclusions on spilling quality."], deliverables=deliverables)
    truth = ground_truth(task_id=task_id, paper_doi="10.1002/chem.202501536", expected_tool_calls=[{"class": "crystal_validation", "backend_examples": ["pymatgen", "spglib"]}, {"class": "periodic_electronic_structure", "backend_examples": ["vasp"]}, {"class": "equation_of_state_and_enthalpy", "backend_examples": ["scipy", "internal_statistics"]}, {"class": "periodic_bonding_projection", "backend_examples": ["lobster"]}], expected_result={"paper_phase_sequence": ["B1", "B8", "dB2"], "paper_transition_pressures_gpa": [8, 25], "first_transition_reference_interval_gpa": [8, 10], "paper_projection_ablation": {"BaO_without_5d_max_spilling_percent": 5.13, "BaO_with_5d_max_spilling_percent": 3.35, "with_d_icohp_ev_range": [-3, -1], "without_d_icohp_magnitude_ev": 0.5}, "paper_conclusion": "Ba 5d-O covalency selectively contributes to stabilization of the denser B8 and dB2 phases."}, deliverables=deliverables, critical_failures=["No real periodic DFT calculation was executed.", "Energies from different formula-unit normalizations were compared.", "Transition pressures were copied from the paper or assigned from grid endpoints.", "LOBSTER results from different parent wavefunctions were compared."], gates=[{"id": "periodic_evidence", "description": "Each reported phase has converged VASP energy/stress evidence.", "score_cap_if_failed": 40}, {"id": "eos_and_crossing", "description": "Transitions follow from fitted/refined enthalpy crossings with uncertainty.", "score_cap_if_failed": 55}, {"id": "projection_ablation", "description": "Ba 5d attribution is supported by a paired same-wavefunction LOBSTER comparison.", "score_cap_if_failed": 70}, {"id": "spilling_quality", "description": "Bonding interpretation is qualified by charge/total spilling.", "score_cap_if_failed": 75}], baseline={"status": "partially_solvable_reference_run_required", "classification": "partially_solvable", "major_paper_conclusion_reproduced_in_this_audit": False, "installed_software": ["pymatgen", "spglib", "VASP 6.3.2", "LOBSTER 5.1.0", "SciPy"], "verified_components": ["VASP periodic energy/force/stress/relaxation Actions", "pymatgen symmetry Actions", "LOBSTER COHP/PDOS/spilling parsers"], "unresolved_requirements": ["The VASP Action does not expose direct target-pressure relaxation; this task uses a controlled E(V)-EOS-H(P) route.", "New LOBSTER calculations currently require the native-job layer.", "A production-cost oracle run is required before numerical tolerances are finalized."]})
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"compound": "BaO", "phases": list(phases), "volume_structure_count": len(structures), "software_stage_count": 4})


def build_pv_selectivity(force: bool) -> None:
    task_id = TASK_IDS[4]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    rows = [row for row in load_pv_candidates() if row["system"] == "P2"]
    records = copy_pv_candidates(data, rows)
    source_experiment = PAPER_ROOT / "Heterobiaryl_PV_Reproduction" / "01_agent_tasks_and_data" / "experimental_evidence" / "experimental_observations.json"
    copy_file(source_experiment, data / "experimental_observations.json")
    deliverables = common_deliverables([{"path": "report/pathway_screening.csv", "description": "P2 C-C and C-O candidate/path decisions."}, {"path": "report/path_validation.json", "description": "Endpoint, image-continuity, imaginary-mode, and IRC evidence."}, {"path": "report/competing_profiles.csv", "description": "Aligned C-C and C-O free-energy profiles."}, {"path": "report/selectivity_conclusion.json", "description": "Delta-delta-G, estimated rate ratio, experimental consistency, and uncertainty."}])
    write_text(data / "README.md", """# P(V) C-C versus C-O pathway-selectivity reproduction

Use the supplied P2 candidate structures and experimental observations to build and
validate one pyridyl-pyridyl C-C path and one competing C-O path. Use low-cost path
search only to generate or validate connectivity, then validate barrier-defining
stationary points, recompute high-level energies, and compare free-energy barriers.
Paper barrier values are hidden.

Paper: 10.1126/science.aas8961.
""")
    write_json(data / "candidate_manifest.json", {"candidate_count": len(records), "state": "P2", "candidates": records})
    protocol = pv_protocol()
    protocol["path_search"] = {"backend": "pysisyphus", "low_cost_calculator": "GFN2-xTB", "solvation": "ALPB ethanol", "accepted_methods": ["NEB", "growing string", "relaxed coordinate scan", "IRC from validated TS"]}
    write_json(data / "computational_protocol.json", protocol)
    write_json(data / "workflow_requirements.json", {"required_stages": ["route_candidate_selection", "low_cost_path_continuity", "transition_state_frequency_validation", "forward_reverse_connection_check", "ORCA_high_level_single_points", "GoodVibes_profiles", "kinetic_selectivity_analysis", "experimental_cross_check"], "hard_gates": ["The highest path image alone is not a validated transition state.", "Each formal TS must have one chemically relevant significant imaginary mode.", "C-C and C-O profiles must use the same reference and thermochemical convention.", "A pathway with wrong endpoint connectivity cannot support selectivity credit."], "rate_ratio_note": "Any Eyring ratio is an inference with equal-prefactor assumptions, not a directly measured product ratio."})
    info = task_info(task_id=task_id, source_id="heterobiaryl_pv_2019_cc_co_selectivity", category="reaction_path_and_kinetic_selectivity", benchmark_family="heterobiaryl_pv", task=("Orchestrate P2 pathway screening, pysisyphus/xTB path validation, Gaussian stationary-point validation, ORCA high-level single points, and GoodVibes profiles to reproduce the paper conclusion that pyridyl-pyridyl C-C coupling is kinetically preferred over the competing C-O pathway."), requirements=["Construct and validate both a C-C and a C-O path.", "Do not equate a path maximum with a transition state without Hessian evidence.", "Use identical thermochemical settings and reference states for both paths.", "Integrate the supplied experiments as supporting evidence without using them as computed barriers."], deliverables=deliverables)
    truth = ground_truth(task_id=task_id, paper_doi="10.1126/science.aas8961", expected_tool_calls=[{"class": "reaction_path_search", "backend_examples": ["pysisyphus", "xtb"]}, {"class": "stationary_point_frequency", "backend_examples": ["gaussian"]}, {"class": "high_level_single_point", "backend_examples": ["orca"]}, {"class": "thermochemical_selectivity", "backend_examples": ["goodvibes"]}], expected_result={"state": "P2", "paper_cc_barrier_kcal_mol": 14, "paper_co_barrier_kcal_mol": 18, "paper_delta_delta_g_dagger_co_minus_cc_kcal_mol": 4, "paper_conclusion": "C-C coupling is kinetically preferred; C-O is accessible but suppressed under the standard acidic ethanol conditions."}, deliverables=deliverables, critical_failures=["Only one pathway was computed.", "A path maximum was reported as a TS without frequency validation.", "The two barriers use inconsistent references or thermochemistry.", "Paper barriers were copied as newly calculated values."], gates=[{"id": "two_valid_paths", "description": "Both C-C and C-O paths have connectivity and endpoint evidence.", "score_cap_if_failed": 45}, {"id": "ts_validation", "description": "Barrier-defining structures pass frequency and connection checks.", "score_cap_if_failed": 50}, {"id": "common_energy_model", "description": "Both profiles use identical energy and thermochemical treatment.", "score_cap_if_failed": 60}], baseline={"status": "partially_solvable_reference_run_required", "classification": "partially_solvable", "major_paper_conclusion_reproduced_in_this_audit": False, "installed_software": ["pysisyphus 1.0.0", "xTB 6.7.1", "Gaussian 16", "ORCA 6.1.1", "GoodVibes 4.3.0"], "verified_components": ["Real pysisyphus/xTB NEB and scan smokes", "Gaussian Hessian Actions", "ORCA energy Actions", "GoodVibes selectivity/profile Actions"], "unresolved_requirements": ["The visible P2 candidates do not constitute a prevalidated one-to-one pair of the paper main C-C and C-O paths.", "A curated oracle mapping and full path reference run are required before production scoring."]})
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"candidate_count": len(records), "states": ["P2"], "experimental_observation_file_count": 1, "software_stage_count": 5})


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
    deliverables = common_deliverables([{"path": "report/structure_validation.csv", "description": "Cell, layer, Pd-site, constraints, distances, and RMSD checks."}, {"path": "report/energy_components.csv", "description": "Composite, clean-slab, isolated, and frozen-fragment energies."}, {"path": "report/binding_decomposition.json", "description": "Binding, surface deformation, NHC deformation, and interaction terms."}, {"path": "report/lobster_bonding.csv", "description": "Pd-C ICOHP/ICOBI, PDOS, charge, and spilling evidence."}, {"path": "report/adsorption_conclusion.json", "description": "Joint energetic and bonding interpretation."}])
    write_text(data / "README.md", """# NHC/PdCu(111) adsorption decomposition and bonding reproduction

For NHC1 and NHC4, validate the published adsorbed cells and matched clean slabs,
relax the required reference systems consistently, construct frozen fragments from
the final adsorbed geometries, decompose adsorption energy, and analyze Pd-C bonding
with LOBSTER. The task tests whether stronger local bonding metrics are interpreted
together with molecular and surface deformation costs. Paper values are hidden.

Paper: 10.1021/acsomega.4c11197.
""")
    write_json(data / "system_manifest.json", {"systems": systems, "binding_energy_sign": "negative is favorable"})
    write_json(data / "computational_protocol.json", {"paper_doi": "10.1021/acsomega.4c11197", "software_dag": ["pymatgen", "VASP", "LOBSTER", "internal energy decomposition"], "vasp": {"functional": "optPBE-vdW", "encut_ev": 500, "k_points": [9, 9, 1], "dipole_correction_axis": 3, "relaxation": "adsorbate and top metal layer; bottom two layers fixed", "additional_incar_guidance": {"GGA": "OR", "LUSE_VDW": True, "AGGAC": 0.0, "LASPH": True}}, "energy_definitions": {"binding": "E_adsorbed - E_relaxed_surface - E_relaxed_NHC", "surface_deformation": "E_frozen_surface_at_ads_geometry - E_relaxed_surface", "nhc_deformation": "E_frozen_NHC_at_ads_geometry - E_relaxed_NHC", "interaction": "E_adsorbed - E_frozen_surface_at_ads_geometry - E_frozen_NHC_at_ads_geometry"}, "lobster": {"metrics": ["ICOHP", "ICOBI", "PDOS", "Lowdin charge", "absolute and total spilling"], "preferred_spilling_threshold_percent": 2.0}, "result_values_included": False})
    write_json(data / "workflow_requirements.json", {"required_stages": ["cell_and_layer_validation", "adsorbed_relaxation", "matched_clean_slab_reference", "isolated_NHC_relaxation", "frozen_fragment_extraction", "energy_decomposition", "LOBSTER_generation_and_quality_gate", "joint_interpretation"], "hard_gates": ["Each adsorbate must use its own matched cell and clean-slab reference.", "Frozen and relaxed fragments must not be interchanged.", "All energy components must share compatible pseudopotentials, cutoffs, and electronic settings.", "Pd-C pairs must be selected from the final geometry using a recorded distance rule.", "LOBSTER bonding conclusions must be qualified by spilling."], "native_layer_note": "Generating fresh LOBSTER outputs currently requires the toolbox native-job layer; public LOBSTER Actions parse and validate the resulting files."})
    info = task_info(task_id=task_id, source_id="nhc_pdcu111_2025_adsorption", category="surface_adsorption_energy_decomposition_and_bonding", benchmark_family="nhc_pdcu111", task=("Orchestrate periodic structure validation, VASP relaxation and matched reference calculations, frozen-fragment adsorption-energy decomposition, and LOBSTER Pd-C bonding analysis for NHC1 and NHC4. Reproduce the paper conclusion that local Pd-C bonding strength alone does not determine the full adsorption-energy difference because deformation and reference-state contributions also matter."), requirements=["Use matched cells and clean surfaces for both adsorbates.", "Compute all binding and deformation components rather than reporting only one adsorption energy.", "Generate and quality-gate LOBSTER evidence for a distance-selected Pd-C pair.", "Explain agreement or tension between total adsorption energetics and local ICOHP/ICOBI metrics."], deliverables=deliverables)
    truth = ground_truth(task_id=task_id, paper_doi="10.1021/acsomega.4c11197", expected_tool_calls=[{"class": "periodic_structure_validation", "backend_examples": ["pymatgen"]}, {"class": "periodic_relaxation_and_energy", "backend_examples": ["vasp"]}, {"class": "periodic_bonding", "backend_examples": ["lobster"]}, {"class": "energy_decomposition", "backend_examples": ["internal_statistics"]}], expected_result={"systems": {"NHC1": {"binding_energy_kcal_mol": -43.0, "pd_c_angstrom": 2.061, "icobi": 0.774, "icohp_ev": -2.441, "charge_spilling_percent": 1.84}, "NHC4": {"binding_energy_kcal_mol": -44.1, "pd_c_angstrom": 2.043, "icobi": 1.05, "icohp_ev": -3.349, "charge_spilling_percent": 1.8}}, "paper_conclusion": "NHC4 has stronger local Pd-C bonding indicators than NHC1, while the total binding-energy difference is moderated by deformation and other energetic contributions."}, deliverables=deliverables, critical_failures=["No real periodic DFT calculation was executed.", "Adsorption energies used unmatched cells or reference states.", "Frozen fragments were confused with relaxed references.", "LOBSTER values were copied from the paper or interpreted without spilling evidence."], gates=[{"id": "matched_reference_states", "description": "Both systems use compatible adsorbed, slab, molecule, and frozen-fragment references.", "score_cap_if_failed": 45}, {"id": "complete_decomposition", "description": "Binding, deformation, and interaction terms close algebraically.", "score_cap_if_failed": 55}, {"id": "lobster_quality", "description": "Pd-C bonding metrics derive from valid outputs with acceptable or qualified spilling.", "score_cap_if_failed": 65}], baseline={"status": "partially_solvable_reference_run_required", "classification": "partially_solvable", "major_paper_conclusion_reproduced_in_this_audit": False, "installed_software": ["pymatgen", "VASP 6.3.2", "LOBSTER 5.1.0"], "verified_components": ["VASP periodic energy/force/stress/relaxation Actions", "LOBSTER COHP/COBI/PDOS/spilling parsers", "Published adsorbed and isolated structures are available"], "unresolved_requirements": ["The optPBE-vdW settings require a production reference run through the VASP additional-INCAR contract.", "Fresh LOBSTER generation requires the native-job layer.", "The two published systems use different surface-cell sizes and must be assessed with matched per-system references rather than direct raw-energy subtraction."]})
    finalize_task(task_id=task_id, info=info, truth=truth, manifest_metadata={"system_ids": ["NHC1", "NHC4"], "adsorbed_structure_count": 2, "clean_slab_count": 2, "isolated_seed_count": 2, "software_stage_count": 4})


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

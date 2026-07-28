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
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.dual_axis import dual_axis_policy, process_rubric

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


SCIENTIFIC_CONCLUSION_RUBRICS: dict[str, list[dict[str, Any]]] = {
    "PV_Protonation_Barrier_Trend": [
        {
            "id": "successive_protonation_barrier_order",
            "max_score": 40,
            "statement": "Comparable new kinetic evidence establishes the coupling-barrier order P0 > P1 > P2.",
            "acceptance_rule": "Require validated transition states and connection evidence, or controlled bounds that resolve all three states under one energy, solvation, temperature, standard-state, and reference convention.",
            "required_evidence": ["new P0/P1/P2 pathway calculations", "first-order saddle and connection validation or controlled bounds", "common free-energy convention"],
        },
        {
            "id": "stepwise_barrier_reduction_scale",
            "max_score": 35,
            "statement": "The first protonation causes a large barrier reduction and the second causes an additional smaller reduction, consistent with the paper-scale approximately 10 and 6 kcal/mol changes.",
            "acceptance_rule": "Full credit requires newly computed reductions with the correct direction and relative scale; partial credit is available when uncertainty preserves the qualitative successive lowering but not both magnitudes.",
            "required_evidence": ["three comparable activation free energies", "difference and uncertainty analysis", "candidate or conformer sensitivity"],
        },
        {
            "id": "exergonic_profiles_distinct_from_kinetic_trend",
            "max_score": 25,
            "statement": "All three coupling profiles remain strongly exergonic on a similar scale, so the protonation effect is primarily a kinetic-barrier trend rather than a large change in reaction thermodynamics.",
            "acceptance_rule": "Require newly computed, consistently referenced reaction free energies for P0, P1, and P2; barrier ordering alone cannot receive this credit.",
            "required_evidence": ["reactant and product free energies for all states", "common thermochemical treatment", "kinetic-versus-thermodynamic interpretation"],
        },
    ],
    "BaO_Phase_Crossover_And_5d_Bonding": [
        {
            "id": "bao_phase_sequence",
            "max_score": 40,
            "statement": "New periodic enthalpy calculations recover the B1 -> B8 -> dB2 stability sequence between 0 and 80 GPa.",
            "acceptance_rule": "Require converged per-formula-unit periodic energies, preserved phase identities, and enthalpy comparison over the pressure interval; labels may be decoded only from the supplied structures and new calculations.",
            "required_evidence": ["new periodic energy or stress calculations for all candidates", "formula-unit normalization", "phase-identity validation"],
        },
        {
            "id": "bao_first_transition_pressure",
            "max_score": 30,
            "statement": "The independently computed B1 to B8 crossover falls within 6-12 GPa.",
            "acceptance_rule": "Require a refined crossing with convergence, EOS/interpolation, and model uncertainty; copied values or grid endpoints receive no credit.",
            "required_evidence": ["EOS or equivalent enthalpy interpolation", "refined B1-B8 crossing", "numerical uncertainty"],
        },
        {
            "id": "bao_second_transition_pressure",
            "max_score": 30,
            "statement": "The independently computed B8 to dB2 crossover falls within 20-30 GPa.",
            "acceptance_rule": "Require fixed-volume internal-coordinate relaxation, a refined crossing, and numerical uncertainty; copied values or an unrelaxed dB2 grid receive no credit.",
            "required_evidence": ["relaxed B8/dB2 energy-volume data", "refined B8-dB2 crossing", "numerical uncertainty"],
        },
    ],
    "PV_CC_CO_Pathway_Selectivity": [
        {
            "id": "two_valid_competing_paths",
            "max_score": 30,
            "statement": "Both the pyridyl-pyridyl C-C and competing C-O pathways are represented by chemically valid, comparably treated paths.",
            "acceptance_rule": "Require endpoint connectivity, atom identity, path continuity, and transition-state/connection validation for both paths, or explicit controlled bounds when one formal TS remains unresolved.",
            "required_evidence": ["new C-C path evidence", "new C-O path evidence", "stationary-point and connection checks"],
        },
        {
            "id": "cc_kinetic_preference",
            "max_score": 45,
            "statement": "The new free-energy comparison establishes C-C coupling as kinetically preferred, with C-O higher by a paper-scale value near 4 kcal/mol.",
            "acceptance_rule": "Full credit requires compatible activation free energies whose uncertainty preserves a positive C-O minus C-C difference near the reference scale; a qualitative guess without two computed paths receives no credit.",
            "required_evidence": ["two comparable activation free energies", "delta-delta-G and uncertainty", "common solvation and thermochemistry"],
        },
        {
            "id": "co_accessible_minor_path",
            "max_score": 25,
            "statement": "C-O coupling remains an accessible but suppressed minor route, consistent with the experimental constraints rather than being chemically impossible.",
            "acceptance_rule": "Require a finite validated C-O path or defensible bound plus a clearly labeled kinetic/selectivity inference; experimental observations may support but not replace computation.",
            "required_evidence": ["finite C-O pathway evidence", "rate/selectivity interpretation", "experimental cross-check separated from computed barriers"],
        },
    ],
    "NHC_Adsorption_Decomposition_Bonding": [
        {
            "id": "nhc_adsorption_order_and_scale",
            "max_score": 35,
            "statement": "Matched-reference periodic calculations find NHC4 only modestly more strongly adsorbed overall than NHC1.",
            "acceptance_rule": "Require independently generated adsorption candidates, converged matched-cell reference energies, and uncertainty that resolves the ordering without comparing raw energies from different cells.",
            "required_evidence": ["new adsorption searches and relaxations", "matched slab and ligand references", "relative adsorption energy and uncertainty"],
        },
        {
            "id": "nhc_local_pd_c_bonding_order",
            "max_score": 35,
            "statement": "Quality-gated local Pd-C metrics show stronger bonding for NHC4 than NHC1.",
            "acceptance_rule": "Require distance-selected Pd-C pairs and fresh validated bonding descriptors, such as shorter Pd-C distance together with stronger ICOHP/ICOBI or a scientifically equivalent analysis; copied paper values receive no credit.",
            "required_evidence": ["final-geometry Pd-C distances", "fresh local bonding descriptors", "projection quality or equivalent validation"],
        },
        {
            "id": "nhc_deformation_moderates_total_binding",
            "max_score": 30,
            "statement": "Surface/ligand deformation and other reference-state contributions moderate the total adsorption-energy difference, so local Pd-C strength alone does not determine binding.",
            "acceptance_rule": "Require an algebraically closed decomposition or an equivalent controlled energy analysis that separates local interaction from deformation/reference contributions.",
            "required_evidence": ["frozen and relaxed fragment energies", "closed energy decomposition", "joint local-bonding versus total-energy interpretation"],
        },
    ],
}


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
            "id": "hidden_scientific_conclusion_recovery",
            "max_score": 50,
            "description": "Recovers every evaluator-only task-level scientific finding from newly generated evidence. The paper route is not required, but a conflicting or unsupported scientific outcome is not successful task completion.",
        },
        {
            "id": "autonomous_method_and_route_design",
            "max_score": 20,
            "description": "Independently frames competing hypotheses and selects defensible structures, software, methods, sampling, numerical controls, fallback routes, and stopping rules without a disclosed paper route.",
        },
        {
            "id": "adaptive_managed_execution",
            "max_score": 10,
            "description": "Executes real managed calculations, passes artifacts correctly, diagnoses failures, and revises the workflow without importing hidden results.",
        },
        {
            "id": "validation_and_falsification",
            "max_score": 15,
            "description": "Tests convergence, numerical sensitivity, chemical validity, competing explanations, uncertainty, and whether the evidence is sufficient for each claim.",
        },
        {
            "id": "provenance_and_uncertainty",
            "max_score": 5,
            "description": "Links claims to managed artifacts and clearly separates calculations, experimental constraints, inference, failed branches, uncertainty, and unresolved limitations.",
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
    archive_extractions: list[dict[str, Any]] | None = None,
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
        "archive_extractions": archive_extractions or [],
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
    scientific_acceptance_contract: dict[str, Any],
    deliverables: list[dict[str, Any]],
    critical_failures: list[str],
    gates: list[dict[str, Any]],
    feasibility: dict[str, Any],
    scientific_conclusion_rubric: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if scientific_conclusion_rubric is None:
        scientific_conclusion_rubric = SCIENTIFIC_CONCLUSION_RUBRICS.get(task_id)
    dual_axis = bool(scientific_conclusion_rubric)
    result = {
        "expected_tool_calls": expected_tool_calls,
        "expected_result": {
            "hidden_posthoc_reference": hidden_reference,
            "scientific_acceptance_contract": scientific_acceptance_contract,
            "reference_use_policy": (
                "Keep the paper method and route hidden from the Agent. Use the evaluator-only "
                "scientific acceptance contract as a mandatory outcome gate after checking that "
                "the conclusion is supported by newly generated evidence."
            ),
        },
        "expected_structured_output": [item["path"] for item in deliverables],
        "evaluation_mode": "dual_axis_100" if dual_axis else "rubric_100",
        "score_max": 100,
        "scoring_rubric": (
            process_rubric(reproduction=False) if dual_axis else common_rubric()
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
            "Score every hidden paper claim independently from newly generated evidence, then "
            "score autonomous research-process quality separately. Do not require the paper route, "
            "and do not let a good process excuse a wrong conclusion. The scorer applies the "
            "multiplicative formula."
            if dual_axis
            else (
                "This is a strict autonomous-discovery evaluation. The Agent receives no paper method "
                "or route and may use any scientifically valid workflow, but high task-completion credit "
                "requires recovering every finding in the hidden scientific acceptance contract from new "
                "managed evidence. Do not reward an opposite or indeterminate conclusion as successful "
                "discovery merely because the tool sequence is plausible. Apply every evidence gate and "
                "the reference-conclusion score cap."
            )
        ),
        "reference_evidence": {
            "task_id": task_id,
            "paired_reproduction_task_id": paired_reproduction_task_id,
            "task_mode": "open_discovery",
            "input_manifest_sha256": "PENDING",
            "hidden_posthoc_reference": hidden_reference,
            "scientific_acceptance_contract": scientific_acceptance_contract,
            "source_boundary": (
                "Paper protocols, author intermediates, completed calculations, and numerical conclusions are evaluator-only."
            ),
            "reference_use_policy": (
                "The route remains evaluator-only and is never required. The task-level scientific "
                "outcome is mandatory for high credit and must be supported by independent calculations."
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
        "evidence_gate_policy": (
            {} if dual_axis else {"judge_must_assess_all": True, "gates": gates}
        ),
        "current_toolbox_feasibility_baseline": feasibility,
        "evaluation_profile": "autonomous_discovery",
        "reference_conclusion_gate_policy": (
            {}
            if dual_axis
            else {
                "required": True,
                "criterion_id": "hidden_scientific_conclusion_recovery",
                "score_cap_if_not_matched": 40,
                "score_cap_if_uncertain": 60,
                "score_cap_if_omitted": 35,
                "max_criterion_score_if_not_matched": 0,
                "max_criterion_score_if_uncertain": 20,
                "max_criterion_score_if_omitted": 0,
            }
        ),
    }
    return result


def finalize_task(
    *,
    task_id: str,
    paired_reproduction_task_id: str,
    info: dict[str, Any],
    truth: dict[str, Any],
    metadata: dict[str, Any],
    author_stationary_points_in_visible_inputs: int | str = 0,
    completed_quantum_outputs: int | str = 0,
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
        "author_stationary_points_in_visible_inputs": author_stationary_points_in_visible_inputs,
        "completed_quantum_outputs": completed_quantum_outputs,
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


def repro_info(repro_id: str) -> dict[str, Any]:
    return json.loads(
        (TASKS_ROOT / repro_id / "task_info.json").read_text(encoding="utf-8")
    )


def copy_reproduction_data_without_route(repro_id: str, data: Path) -> None:
    source = TASKS_ROOT / repro_id / "data" / "benchmark_data"
    excluded = {
        "README.md",
        "input_manifest.json",
        "computational_protocol.json",
        "workflow_requirements.json",
        "reaction_definitions.json",
    }
    for path in sorted(source.rglob("*")):
        if path.is_file() and path.name not in excluded:
            copy_file(path, data / path.relative_to(source))


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
            "When server resources allow, parallelize independent conformers and use substantial CPU resources without oversubscribing the host.",
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
        scientific_acceptance_contract={
            "required_findings": [
                "The low-cost search recovers multiple thermally relevant structural basins rather than one arbitrary geometry.",
                "After identity-preserving alignment, higher-confidence quantum refinement and thermochemical treatment materially change at least one ranking or population conclusion relative to the low-cost ranking.",
            ],
            "not_required": [
                "The paper's exact generated conformer count, file indices, or rounded population values.",
                "The paper's exact software sequence when an independently valid alternative establishes the same findings.",
            ],
            "decision_rule": "Both required findings must be supported by new calculations; otherwise reference_conclusion_status is uncertain or not_matched.",
        },
        scientific_conclusion_rubric=[
            {"id": "major_basin_coverage", "max_score": 30, "statement": "The independently chosen low-cost search recovers multiple major chemically valid conformer basins for GEOM-C3.", "acceptance_rule": "Require new identity-preserving search and clustering evidence; exact paper conformer count and route are not required.", "required_evidence": ["managed conformer search", "connectivity and lineage checks", "basin or clustering summary"]},
            {"id": "quantum_ranking_reorder", "max_score": 35, "statement": "Aligned higher-confidence quantum refinement materially changes the low-cost conformer ranking or dominant-basin assignment.", "acceptance_rule": "Require an atom-mapped comparison supported by newly computed quantum energies and a ranking statistic or dominant-basin change.", "required_evidence": ["new quantum refinement", "identity-preserving alignment", "ranking statistic or dominant-basin comparison"]},
            {"id": "thermochemical_population_change", "max_score": 35, "statement": "Validated thermochemistry changes or materially sharpens the population distribution relative to the low-cost electronic-energy ranking.", "acceptance_rule": "Require frequency-validated thermal free energies and normalized populations. Electronic-energy-only weights receive partial rather than full credit.", "required_evidence": ["frequency or Hessian validation", "thermal free energies at 298.15 K", "normalized population comparison"]},
        ],
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
            {"id": "sampling_coverage_and_convergence", "description": "The search covers multiple distinct basins and has a calculation-backed coverage or convergence check; a single search pass without a stopping justification is insufficient.", "score_cap_if_failed": 70},
            {"id": "thermochemical_population_validity", "description": "Any 298.15 K population claim is supported by computed thermochemical free energies or is explicitly limited to a validated electronic-energy proxy with sensitivity bounds.", "score_cap_if_failed": 65},
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
molecular surface for 1-pentanethiol and whether an ensemble treatment is more
defensible than an arbitrary single conformer. The experimental TE value is held
back for evaluator-only posthoc comparison. Generate all structures, choose all
electronic, numerical, and statistical methods independently, and make a blind
surface prediction with uncertainty.
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
                    "temperature_kelvin": 298.15,
                }
            },
            "experimental_value_scope": "withheld evaluator-only blind target",
        },
    )
    deliverables = common_deliverables(
        [
            {"path": "report/conformer_sampling.csv", "description": "Generated conformers, clustering, energies, validation, and selection decisions."},
            {"path": "report/surface_evidence.csv", "description": "Per-conformer density/surface provenance and numerical controls."},
            {"path": "report/ensemble_surface.json", "description": "Single-structure and ensemble estimates, blind prediction, sensitivity, and uncertainty."},
        ]
    )
    info = task_info(
        task_id=task_id,
        source_id="electron_isodensity_2024_autonomous_flexibility_question",
        category="autonomous_conformer_and_molecular_surface",
        benchmark_family="electron_isodensity_surface",
        task=(
            "Using only the supplied 1-pentanethiol identity, independently "
            "determine whether conformational flexibility materially changes an electron-density-derived "
            "molecular surface and whether a thermally weighted ensemble is more defensible than a single "
            "structure. Generate all conformers, choose the density and isosurface methodology, validate "
            "numerical settings, quantify truncation and weighting uncertainty, and make a blind surface "
            "prediction for evaluator-only posthoc comparison with experiment."
        ),
        requirements=[
            "Predeclare the conformer, electronic-density, surface-definition, calibration, and uncertainty plan before production calculations.",
            "Generate and validate multiple conformers in this run; do not import author conformers.",
            "Every reported surface must trace to a real wavefunction/density artifact and surface calculation.",
            "Test sensitivity to conformer truncation and at least one numerical surface control.",
            "Do not infer or tune against the withheld ISO-M6 experimental value; justify the computational definition independently.",
            "When server resources allow, run independent conformer calculations concurrently and use substantial CPU resources without oversubscribing the host.",
        ],
        deliverables=deliverables,
        data_description="One flexible molecule identity; no experimental target, conformers, cutoff, density method, grid, or paper value.",
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
        scientific_acceptance_contract={
            "required_findings": [
                "New per-conformer density-isosurface calculations show a conformer effect that is material relative to the measured numerical/grid sensitivity.",
                "A traceable thermally weighted ensemble reduces dependence on an arbitrary single conformer and is therefore the more defensible reported estimate.",
            ],
            "not_required": [
                "The paper's exact 25-conformer aggregate or exact individual surface values.",
                "The paper's exact density method, cutoff, or software route when an independently validated definition establishes the same findings.",
            ],
            "decision_rule": "Both flexibility and ensemble findings must be supported by new density/surface artifacts and weighting evidence; numerical proximity alone is insufficient.",
        },
        scientific_conclusion_rubric=[
            {"id": "conformer_surface_variation", "max_score": 40, "statement": "New density-isosurface calculations show that distinct ISO-M6 conformers have materially different molecular surface areas.", "acceptance_rule": "The conformer dispersion must exceed demonstrated numerical integration uncertainty and derive from valid per-conformer density artifacts.", "required_evidence": ["multiple independently generated conformers", "per-conformer density and surface artifacts", "grid or numerical sensitivity"]},
            {"id": "thermal_ensemble_reduces_single_structure_bias", "max_score": 40, "statement": "A normalized thermally weighted conformer ensemble is more defensible than an arbitrary single-conformer surface and reduces selection bias.", "acceptance_rule": "Require a converged or sensitivity-bounded conformer set and traceable weights. Electronic-energy-only weights receive partial rather than full credit unless quantitatively bounded.", "required_evidence": ["weighting energies or free energies", "normalization", "conformer-space and weighting sensitivity"]},
            {"id": "blind_surface_prediction_scale", "max_score": 20, "statement": "The independently selected workflow predicts an ISO-M6 ensemble surface compatible with the hidden paper/TE neighborhood near 157 A^2.", "acceptance_rule": "Full credit when the new estimate or uncertainty interval is within 5 percent of the paper/TE neighborhood; partial credit within 10 percent when the discrepancy is scientifically analyzed without post-hoc tuning.", "required_evidence": ["prediction fixed before hidden comparison", "new ensemble surface", "uncertainty and post-hoc reference comparison"]},
        ],
        deliverables=deliverables,
        critical_failures=[
            "No real electronic-structure calculation was executed.",
            "No real electron-density isosurface calculation was executed.",
            "Publication conformers or hidden surface values were used as newly generated evidence.",
            "A single-conformer result was labeled an ensemble without computed weights.",
            "The withheld ISO-M6 experimental value was inferred or imported and used to tune the surface definition.",
        ],
        gates=[
            {"id": "real_density_and_surface", "description": "New density and isosurface artifacts support the numerical results.", "score_cap_if_failed": 40},
            {"id": "independent_conformer_sampling", "description": "Multiple conformers were generated without author coordinates.", "score_cap_if_failed": 55},
            {"id": "surface_materiality_vs_numerics", "description": "The claimed conformer effect is larger than and distinguished from cutoff/grid or integration uncertainty.", "score_cap_if_failed": 65},
            {"id": "ensemble_validity", "description": "Weights, normalization, conformer truncation/convergence, and weighting sensitivity are computed and addressed; an electronic-energy proxy must be labeled and bounded rather than presented as exact thermal free energy.", "score_cap_if_failed": 65},
        ],
        feasibility={
            "status": "pre_release_pilot_ready",
            "classification": "solvable",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": ["The paired reproduction task must lock its grid settings and regenerate a subset-specific oracle before formal ranking.", "The experimental TE value is intentionally evaluator-only to preserve blind-method selection."],
        },
    )
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"molecule_ids": ["ISO-M6"], "starting_structure_count": 0, "visible_experimental_measurement_count": 0})


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
    copy_reproduction_data_without_route(repro_id, data)
    write_text(
        data / "README.md",
        """# Autonomous protonation-effect output analysis

The P0, P1, and P2 author-output archives and candidate coordinates are supplied to
both tracks. Independently determine a defensible validation, file-matching,
thermochemistry, reference-state, and uncertainty workflow. No paper protocol or
preselected reaction-profile construction is disclosed in this autonomous track.
""",
    )
    reproduction_info = repro_info(repro_id)
    deliverables = reproduction_info["required_deliverables"]
    info = task_info(
        task_id=task_id,
        source_id="heterobiaryl_pv_2018_autonomous_author_output_analysis",
        category="autonomous_author_output_thermochemistry",
        benchmark_family="heterobiaryl_pv",
        task=(
            "Using the supplied P0, P1, and P2 completed author quantum-chemistry output archives, independently "
            "determine whether successive protonation changes the kinetically relevant pyridyl-pyridyl "
            "coupling barrier under acidic ethanol conditions. Infer and validate file identities, choose "
            "a consistent thermochemical and reference-state analysis, quantify uncertainty, and distinguish "
            "kinetic barrier changes from reaction thermodynamics."
        ),
        requirements=[
            "Choose and record an independent archive-validation, output-matching, thermochemistry, and profile-alignment plan before numerical analysis.",
            "Validate molecular identity, charge, multiplicity, convergence, and stationary-point character before using any output.",
            "Use one internally consistent 353.15 K, 1 M ethanol convention and one disclosed reference definition across P0, P1, and P2.",
            "Separate newly generated analysis results from filenames, supplied raw outputs, and evaluator-only paper targets.",
            "Preserve parsing, matching, and validation failures and quantify their consequence for the final trend.",
        ],
        deliverables=deliverables,
        data_description="The same P0/P1/P2 author-output archives, candidate coordinates, identities, and physical conditions as the guided track; no paper protocol, route definition, or target values.",
        archive_extractions=reproduction_info["archive_extractions"],
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "archive_and_output_validation", "required": True},
            {"class": "frequency_and_stationary_point_validation", "required": True},
            {"class": "high_level_single_point_matching", "required": True},
            {"class": "comparable_thermochemical_profile_analysis", "required": True},
        ],
        hidden_reference=hidden,
        scientific_acceptance_contract={
            "required_findings": [
                "Independent reanalysis of the supplied raw outputs establishes the P0 > P1 > P2 coupling-barrier order.",
                "The first protonation gives a large reduction and the second gives an additional smaller reduction under one consistent convention.",
                "Reaction thermodynamics are reported separately from the kinetic trend.",
            ],
            "not_required": [
                "Exact reproduction of 30, 20, and 14 kcal/mol when an independently valid route recovers the same robust trend.",
            ],
            "decision_rule": "All three states require validated, matched raw-output evidence and one comparable analysis convention strong enough to determine the ordering.",
        },
        deliverables=deliverables,
        critical_failures=[
            "No managed author-output validation or thermochemical analysis was executed.",
            "A precise barrier is reported without frequency, geometry, and matched single-point validation.",
            "P0/P1/P2 comparisons mix incompatible references, conditions, or energy conventions.",
            "Evaluator-only paper values are presented as newly generated analysis results.",
        ],
        gates=[
            {"id": "state_comparability", "description": "All three protonation states use comparable conditions and references.", "score_cap_if_failed": 60},
            {"id": "pathway_validity", "description": "Claims are supported by validated paths/TSs or explicitly limited controlled bounds.", "score_cap_if_failed": 55},
            {"id": "three_state_evidence", "description": "Each state has a new managed computational attempt and an evidence-status conclusion.", "score_cap_if_failed": 70},
            {"id": "barrier_trend_resolution", "description": "Validated comparable evidence is strong enough to determine the P0 > P1 > P2 barrier ordering rather than merely proposing it.", "score_cap_if_failed": 50},
        ],
        feasibility={
            "status": "validated_for_evaluation",
            "classification": "solvable",
            "paired_reproduction_reference_run_complete": True,
            "known_limitations": [],
        },
    )
    truth["reference_evidence"]["source_boundary"] = "Both tracks receive the same author raw outputs; only the guided track receives the paper-reconstructed method and route."
    finalize_task(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        info=info,
        truth=truth,
        metadata={"states": ["P0", "P1", "P2"], "author_archive_count": 3, "candidate_count": 66, "visible_experimental_measurement_count": 0},
        author_stationary_points_in_visible_inputs="contained_in_author_archives",
        completed_quantum_outputs="official_author_archives",
    )


def build_bao(force: bool) -> None:
    task_id, repro_id = TASK_IDS[3], REPRO_IDS[3]
    root = prepare_task_root(task_id, force)
    data = root / "data" / "benchmark_data"
    copy_reproduction_data_without_route(repro_id, data)
    write_text(
        data / "README.md",
        """# Autonomous BaO phase-crossover investigation

The same B1, B8, and dB2 volume structures are supplied to both tracks. Choose the
periodic electronic-structure method, relaxation strategy, convergence controls,
EOS/enthalpy analysis, adaptive refinement, and uncertainty treatment independently.
No paper computational protocol or prescribed analysis route is disclosed here.
""",
    )
    deliverables = repro_info(repro_id)["required_deliverables"]
    info = task_info(
        task_id=task_id,
        source_id="bao_2025_autonomous_phase_crossover",
        category="autonomous_high_pressure_phase_stability",
        benchmark_family="bao_high_pressure",
        task=(
            "Using the supplied B1, B8, and dB2 BaO phase-volume structures, independently determine the "
            "stable phase sequence between 0 and 80 GPa and estimate both crossover pressures. Select "
            "and validate the periodic electronic-structure, relaxation, EOS/enthalpy, refinement, and "
            "uncertainty workflow without a disclosed paper method."
        ),
        requirements=[
            "Choose and justify the periodic method, volume sampling, relaxation, and adaptive crossover strategy.",
            "Use compatible periodic settings and normalize energies/enthalpies per BaO formula unit.",
            "Validate structural identity after relaxation and do not silently compare collapsed phases.",
            "Quantify convergence and interpolation uncertainty for every crossover claim.",
            "Use fixed-volume internal-coordinate relaxation where required by residual-force checks.",
        ],
        deliverables=deliverables,
        data_description="The same B1, B8, and dB2 phase-volume structures and pressure range as the guided track; no paper method, EOS route, or transition pressure.",
    )
    hidden = repro_truth(repro_id)["expected_result"]
    truth = ground_truth(
        task_id=task_id,
        paired_reproduction_task_id=repro_id,
        expected_tool_calls=[
            {"class": "periodic_relaxation_or_equation_of_state", "required": True},
            {"class": "enthalpy_and_crossover_analysis", "required": True},
        ],
        hidden_reference=hidden,
        scientific_acceptance_contract={
            "required_findings": [
                "The newly calculated enthalpy curves recover the B1 -> B8 -> dB2 stability sequence over 0-80 GPa with crossovers in the neighborhoods of the paper transitions.",
            ],
            "not_required": [
                "Exact 8 and 25 GPa crossing values when convergence and interpolation uncertainty overlap the reference neighborhoods.",
            ],
            "decision_rule": "Full conclusion credit requires the complete three-phase sequence and both refined transition-pressure intervals.",
        },
        deliverables=deliverables,
        critical_failures=[
            "No real periodic electronic-structure calculation was executed.",
            "Energies or enthalpies were compared without formula-unit normalization.",
            "A relaxed structure changed phase identity but was retained without disclosure.",
            "Literature transition pressures or bonding values were presented as new results.",
            "B8 or dB2 was used in the final EOS without required fixed-volume internal-coordinate relaxation.",
        ],
        gates=[
            {"id": "periodic_evidence", "description": "New converged periodic calculations support the stability analysis.", "score_cap_if_failed": 35},
            {"id": "thermodynamic_consistency", "description": "Pressure/volume, PV units, references, and normalization are consistent.", "score_cap_if_failed": 55},
            {"id": "phase_identity", "description": "Relaxed candidates remain distinguishable or transformations are explicitly analyzed.", "score_cap_if_failed": 65},
            {"id": "phase_sequence_resolution", "description": "Sampling and interpolation resolve both stability crossovers with quantified convergence uncertainty.", "score_cap_if_failed": 55},
        ],
        feasibility={
            "status": "validated_for_evaluation",
            "classification": "solvable",
            "paired_reproduction_reference_run_complete": True,
            "known_limitations": [],
        },
    )
    truth["reference_evidence"]["source_boundary"] = "Both tracks receive the same phase-volume structures; only the guided track receives the paper-reconstructed periodic method and EOS route."
    finalize_task(task_id=task_id, paired_reproduction_task_id=repro_id, info=info, truth=truth, metadata={"compound": "BaO", "phases": ["B1", "B8", "dB2"], "volume_structure_count": 15})


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
        scientific_acceptance_contract={
            "required_findings": [
                "Comparable validated kinetic evidence shows C-C coupling is preferred over C-O coupling for P2 under the stated conditions.",
                "C-O remains a plausible accessible minor pathway rather than being treated as impossible solely because it is disfavored.",
            ],
            "not_required": [
                "Exact 14 and 18 kcal/mol barriers when controlled uncertainty still preserves the C-C preference.",
            ],
            "decision_rule": "Both pathways must be tested comparably and the selectivity direction must follow from validated transition states or controlled bounds.",
        },
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
            {"id": "selectivity_direction_resolution", "description": "The new comparable evidence actually resolves C-C as kinetically preferred while retaining C-O as accessible, rather than only listing possible paths.", "score_cap_if_failed": 50},
        ],
        feasibility={
            "status": "pre_release_blocked",
            "classification": "partially_solvable",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": [
                "No curated pair of C-C/C-O endpoints and atom mappings has yet been reference-validated.",
                "xTB 6.7 does not parameterize ALPB ethanol; an independently chosen low-cost solvent proxy must be treated only as a search approximation before ethanol-level validation.",
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
        scientific_acceptance_contract={
            "required_findings": [
                "New matched-reference adsorption calculations recover NHC4 as only modestly more strongly bound overall than NHC1.",
                "Quality-gated local Pd-C descriptors are stronger for NHC4, while deformation and other energetic contributions moderate the total adsorption-energy difference.",
            ],
            "not_required": [
                "Exact paper binding energies, bond lengths, ICOBI, or ICOHP values when the same ordering and decomposition conclusion are robust.",
            ],
            "decision_rule": "Full conclusion credit requires the adsorption ordering, local-bonding ordering, and the distinction between local bonding and total-energy decomposition.",
        },
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
            {"id": "adsorption_order_and_decomposition", "description": "Fresh matched calculations resolve the NHC4/NHC1 adsorption ordering and quantify deformation or equivalent nonlocal energetic contributions.", "score_cap_if_failed": 55},
            {"id": "bonding_vs_total_energy_interpretation", "description": "Quality-gated local Pd-C descriptors are compared without equating them to total adsorption energy.", "score_cap_if_failed": 65},
        ],
        feasibility={
            "status": "pre_release_native_oracle_required",
            "classification": "conditionally_solvable_with_native_execution",
            "paired_reproduction_reference_run_complete": False,
            "known_limitations": [
                "Adsorption placement and Selective Dynamics are not covered by dedicated public Actions, but may be implemented through the allowed direct programming/native VASP layer.",
                "Fresh LOBSTER generation is available through direct native execution; public LOBSTER Actions parse and quality-gate the generated outputs.",
                "A fresh adsorption-search and decomposition Gold Run is still required before formal ranking.",
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

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from src.core.io import read_json, sha256_file, stable_id, write_json
from src.core.models import selected_task_type
from src.core.paths import DEFAULT_BENCHMARK_ROOT
from src.core.runtime import normalize_runtime
from src.curation.package_validation import (
    package_readiness,
    package_value,
)
from src.curation.quality_score import score_record

MODE_SPEC = {
    "paper_reproduction": {
        "task_mode": "guided_reproduction",
        "scientific_mode": "paper_reproduction",
        "evaluation_profile": "paper_reproduction",
        "reproduction": True,
    },
    "conclusion_guided_reconstruction": {
        "task_mode": "open_discovery",
        "scientific_mode": "conclusion_guided_reconstruction",
        "evaluation_profile": "autonomous_discovery",
        "reproduction": False,
    },
    "autonomous_research": {
        "task_mode": "open_discovery",
        "scientific_mode": "autonomous_research",
        "evaluation_profile": "autonomous_discovery",
        "reproduction": False,
    },
    "mechanistic_rule_discovery": {
        "task_mode": "open_discovery",
        "scientific_mode": "mechanistic_rule_discovery",
        "evaluation_profile": "autonomous_discovery",
        "reproduction": False,
    },
}

DEFAULT_DELIVERABLES = {
    "autonomous_research": [
        (
            "report/research_plan.json",
            "Initial and revised hypotheses, staged route, budgets, validation gates, and stopping rules.",
        ),
        (
            "report/calculation_inventory.csv",
            "Every attempted scientific calculation with inputs, method, status, outputs, and artifact paths.",
        ),
        (
            "report/evidence_graph.json",
            "Claim-to-evidence graph separating observations, new computations, inference, and uncertainty.",
        ),
        (
            "report/failure_log.jsonl",
            "Failed or inconclusive branches, diagnosis, retained artifacts, and replanning consequences.",
        ),
        (
            "report/final_answer.json",
            "Machine-readable scientific conclusions, confidence, evidence links, and unresolved questions.",
        ),
        ("report/report.md", "Human-readable artifact-linked scientific report."),
    ],
    "paper_reproduction": [
        (
            "report/execution_plan.json",
            "Dependency-aware interpretation of the supplied route, resources, validation gates, and stopping rules.",
        ),
        (
            "report/calculation_inventory.csv",
            "Every reproduction calculation with parameters, status, outputs, deviations, and artifact paths.",
        ),
        (
            "report/reference_comparison.json",
            "Post-computation comparison against the hidden reference targets with tolerances and uncertainty.",
        ),
        (
            "report/failure_log.jsonl",
            "Failed or inconclusive stages, diagnosis, controlled recovery, and retained artifacts.",
        ),
        (
            "report/final_answer.json",
            "Machine-readable reproduced results, deviations, confidence, and evidence links.",
        ),
        ("report/report.md", "Human-readable artifact-linked reproduction report."),
    ],
    "conclusion_guided_reconstruction": [
        (
            "report/verification_plan.json",
            "Independent verification strategy, alternatives, decision criteria, and validation gates.",
        ),
        (
            "report/calculation_inventory.csv",
            "Every attempted verification calculation with inputs, method, status, outputs, and artifact paths.",
        ),
        (
            "report/evidence_graph.json",
            "Claim-to-evidence graph distinguishing supplied conclusion, new evidence, inference, and uncertainty.",
        ),
        (
            "report/failure_log.jsonl",
            "Failed or inconclusive verification branches and controlled recovery.",
        ),
        (
            "report/final_answer.json",
            "Machine-readable verdict on the disclosed conclusion with evidence links and uncertainty.",
        ),
        ("report/report.md", "Human-readable artifact-linked verification report."),
    ],
    "mechanistic_rule_discovery": [
        (
            "report/research_plan.json",
            "Descriptor candidates, comparison design, held-out protocol, budgets, and stopping rules.",
        ),
        (
            "report/system_features.csv",
            "System-level structures, descriptors, outcomes, provenance, and validation status.",
        ),
        (
            "report/calculation_inventory.csv",
            "Every attempted calculation with species identities, method, status, result, and artifact paths.",
        ),
        (
            "report/heldout_predictions.json",
            "Predictions for hidden systems with confidence and no post-hoc use of held-out outcomes.",
        ),
        (
            "report/failure_log.jsonl",
            "Failed descriptors, unstable relationships, and applicability-limit evidence.",
        ),
        (
            "report/final_answer.json",
            "Machine-readable rule, mechanistic interpretation, held-out performance, and failure boundary.",
        ),
        ("report/report.md", "Human-readable artifact-linked rule-discovery report."),
    ],
}

AUTONOMOUS_PROCESS_RUBRIC = [
    {
        "id": "problem_framing_and_route_design",
        "max_score": 20,
        "description": "Independently defines hypotheses, alternatives, decision criteria, a staged route, budgets, and stopping rules.",
    },
    {
        "id": "method_and_tool_selection",
        "max_score": 15,
        "description": "Selects chemically appropriate structures, software, methods, parameters, controls, and fallback routes.",
    },
    {
        "id": "managed_execution_and_artifact_flow",
        "max_score": 15,
        "description": "Executes real managed scientific calculations and passes identities, structures, parameters, and artifacts correctly between stages.",
    },
    {
        "id": "validation_falsification_and_uncertainty",
        "max_score": 20,
        "description": "Tests convergence, chemical validity, alternatives, evidence sufficiency, numerical sensitivity, and uncertainty.",
    },
    {
        "id": "failure_diagnosis_and_adaptation",
        "max_score": 10,
        "description": "Diagnoses failed or inconclusive calls and adapts without fabricating or laundering results.",
    },
    {
        "id": "resource_and_search_efficiency",
        "max_score": 10,
        "description": "Uses resources, search breadth, numerical resolution, parallelism, and stopping decisions efficiently.",
    },
    {
        "id": "provenance_reporting_and_reproducibility",
        "max_score": 10,
        "description": "Links claims to managed artifacts and reports assumptions, failures, units, uncertainty, and reproducible parameters.",
    },
]

REPRODUCTION_PROCESS_RUBRIC = [
    {
        "id": "protocol_interpretation_and_execution_plan",
        "max_score": 20,
        "description": "Correctly interprets the supplied method and route, dependencies, budgets, validation gates, and stopping rules.",
    },
    {
        "id": "method_parameter_and_structure_fidelity",
        "max_score": 15,
        "description": "Uses supplied identities, methods, parameters, reference states, and controlled substitutions faithfully.",
    },
    {
        "id": "managed_recomputation_and_artifact_flow",
        "max_score": 15,
        "description": "Recomputes the required evidence through managed execution and passes artifacts correctly across the workflow.",
    },
    {
        "id": "validation_numerical_quality_and_uncertainty",
        "max_score": 20,
        "description": "Validates convergence, identities, stationary points or states, numerical quality, uncertainty, and comparison tolerances.",
    },
    {
        "id": "failure_diagnosis_and_protocol_recovery",
        "max_score": 10,
        "description": "Diagnoses failures, makes controlled recovery choices, and records unavoidable protocol deviations.",
    },
    {
        "id": "resource_and_execution_efficiency",
        "max_score": 10,
        "description": "Uses resources, parallelism, retries, numerical settings, and stopping decisions efficiently while preserving protocol validity.",
    },
    {
        "id": "provenance_reporting_and_reproducibility",
        "max_score": 10,
        "description": "Separates reference targets from recomputation and links conclusions, deviations, failures, and uncertainty to artifacts.",
    },
]

DUAL_AXIS_POLICY = {
    "formula": "scientific_conclusion_score * research_process_score / 100",
    "scientific_conclusion_score_max": 100,
    "research_process_score_max": 100,
    "final_score_max": 100,
    "unsupported_claim_policy": "A conclusion copied, guessed, or asserted without newly generated valid evidence receives no scientific-conclusion credit.",
    "objective_failure_policy": "A demonstrated benchmark input, framework, backend, or infrastructure failure may make the run not_scorable_objective; agent-selected invalid inputs or resource limits do not.",
    "invalid_submission_policy": "Fabricated evidence, hidden-answer leakage, or paper values presented as new calculations make the final score zero.",
}


def build_dataset(
    records: list[dict[str, Any]],
    output_dir: str | Path,
    allow_failed_quality: bool = False,
    split_salt: str = "researchchembench-v1",
    *,
    benchmark_root: str | Path | None = None,
    require_reference_run: bool = False,
) -> dict[str, Any]:
    """Build complete ResearchChemBench-native packages in a staging directory."""

    root = Path(output_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    _remove_previous_generated_tasks(root)
    benchmark = Path(benchmark_root).resolve() if benchmark_root else DEFAULT_BENCHMARK_ROOT
    tasks: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for record in records:
        mode = selected_task_type(record)
        if not mode:
            skipped.append(
                {"paper_id": record.get("paper_id"), "reason": "missing selected_task_type"}
            )
            continue
        quality = score_record(record, mode)
        readiness = package_readiness(record, mode)
        reference_ready = (record.get("reference_run") or {}).get("status") == "validated"
        if (
            (not quality["passed"] and not allow_failed_quality)
            or not readiness["passed"]
            or (require_reference_run and not reference_ready)
        ):
            skipped.append(
                {
                    "paper_id": record.get("paper_id"),
                    "task_type": mode,
                    "quality": quality,
                    "package_readiness": readiness,
                    "reference_run_required": require_reference_run,
                    "reference_run_ready": reference_ready,
                }
            )
            continue
        tasks.append(build_task(record, mode, root, quality, split_salt, benchmark))
    manifest = {
        "dataset": "ResearchChemBench",
        "pipeline_format": "researchchembench_native_v1",
        "version": "0.3.0",
        "task_count": len(tasks),
        "paper_count": len({task["source_group_id"] for task in tasks}),
        "tasks": tasks,
        "skipped": skipped,
        "split_policy": "sha256(source study id + split salt); one formal task is generated per study",
        "release_ready": bool(tasks) and all(task["reference_run_ready"] for task in tasks),
    }
    write_json(root / "_pipeline_manifest.json", manifest)
    return manifest


def build_task(
    record: dict[str, Any],
    mode: str,
    root: Path,
    quality: dict[str, Any],
    split_salt: str,
    benchmark_root: Path,
) -> dict[str, Any]:
    package = record["benchmark_package"]
    task_id = (
        package_value(package, "task_id", mode)
        or package_value(package, "task_ids", mode)
        or _default_task_id(record, mode)
    )
    task_id = _safe_task_id(task_id)
    split = assign_split(record["paper_id"], split_salt)
    task_dir = root / task_id
    if task_dir.exists():
        shutil.rmtree(task_dir)
    data_root = task_dir / "data" / "benchmark_data"
    target_root = task_dir / "target_study"
    data_root.mkdir(parents=True)
    target_root.mkdir(parents=True)

    materialized = _materialize_public_inputs(record, mode, data_root)
    manifest = _write_input_manifest(record, mode, data_root, materialized)
    task_info = _build_task_info(record, mode, task_id, data_root, manifest)
    ground_truth = _build_ground_truth(record, mode, data_root, manifest, quality)

    _validate_against_benchmark_schema(task_info, ground_truth, benchmark_root)
    _assert_no_public_leakage(record, mode, task_info, data_root)
    write_json(task_dir / "task_info.json", task_info)
    write_json(target_root / "ground_truth.json", ground_truth)

    return {
        "task_id": task_id,
        "source_group_id": stable_id("source", record["paper_id"]),
        "task_type": mode,
        "mode": mode,
        "benchmark_task_mode": MODE_SPEC[mode]["task_mode"],
        "split": split,
        "path": task_id,
        "quality_score": quality["score"],
        "reference_run_ready": (record.get("reference_run") or {}).get("status") == "validated",
        "runtime": normalize_runtime(record.get("runtime")),
        "input_files": len(manifest["files"]),
    }


def _materialize_public_inputs(record: dict[str, Any], mode: str, destination: Path) -> list[str]:
    package = record["benchmark_package"]
    public_inputs = package.get("public_inputs") or {}
    written: list[str] = []

    structured = {
        "reaction.json": public_inputs.get("reaction") or {"inputs": record.get("inputs", [])},
        "molecular_systems.json": public_inputs.get("molecular_systems") or [],
        "experimental_observations.json": public_inputs.get("observations")
        or {
            "observations": _public_evidence(record),
            "controls": record.get("controls", []),
        },
        "target_conclusion.json": (
            {
                "target_conclusion": public_inputs.get("target_conclusion")
                or public_inputs.get("disclosed_conclusion")
            }
            if public_inputs.get("target_conclusion") or public_inputs.get("disclosed_conclusion")
            else None
        ),
        "training_systems.json": public_inputs.get("training_systems") or None,
        "heldout_systems.json": public_inputs.get("heldout_systems") or None,
    }
    for filename, value in structured.items():
        if value:
            write_json(destination / filename, value)
            written.append(filename)

    if mode == "paper_reproduction":
        protocol = package.get("method_protocol") or record.get("public_method_protocol")
        write_json(destination / "method_protocol.json", protocol)
        written.append("method_protocol.json")

    for relative, value in (public_inputs.get("files") or {}).items():
        target = _safe_destination(destination, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, (dict, list)):
            write_json(target, value)
        else:
            target.write_text(str(value).rstrip() + "\n", encoding="utf-8")
        written.append(target.relative_to(destination).as_posix())

    visible_by_type = (record.get("assets") or {}).get("visible_data") or {}
    visible = list(visible_by_type.get("all", [])) + list(visible_by_type.get(mode, []))
    for raw_path in visible:
        source = Path(raw_path)
        if not source.exists():
            raise FileNotFoundError(f"registered visible input does not exist: {source}")
        target = destination / "source_files" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
            written.extend(
                path.relative_to(destination).as_posix()
                for path in target.rglob("*")
                if path.is_file()
            )
        else:
            shutil.copy2(source, target)
            written.append(target.relative_to(destination).as_posix())

    readme = _render_data_readme(record, mode, written)
    (destination / "README.md").write_text(readme, encoding="utf-8")
    written.append("README.md")
    return sorted(set(written))


def _write_input_manifest(
    record: dict[str, Any],
    mode: str,
    data_root: Path,
    materialized: list[str],
) -> dict[str, Any]:
    package = record["benchmark_package"]
    manifest = {
        "task_mode": MODE_SPEC[mode]["task_mode"],
        "scientific_mode": MODE_SPEC[mode]["scientific_mode"],
        "pipeline_task_type": mode,
        "runtime": normalize_runtime(record.get("runtime")),
        "source_id": stable_id("source", record["paper_id"]),
        "files": [_file_record(data_root, data_root / path) for path in materialized],
        "completed_computational_outputs": 0,
        "optimized_stationary_points": 0,
        "transition_states": 0,
        "reaction_path_outputs": 0,
        "reference_answers": 0,
        "author_coordinates": 0,
        "published_numerical_results": 0,
        "disclosure": (
            "The paper-derived route and method are provided, but author numerical outputs and conclusions are hidden."
            if mode == "paper_reproduction"
            else (
                "The target conclusion is disclosed, while the paper route and author computational outputs are hidden."
                if mode == "conclusion_guided_reconstruction"
                else (
                    "Training systems and held-out prediction targets are disclosed; the inferred rule and held-out outcomes are hidden."
                    if mode == "mechanistic_rule_discovery"
                    else "Only starting identities, reaction facts, conditions, and experimental observations are provided. The paper route, computed outputs, and conclusions are hidden."
                )
            )
        ),
        **(package.get("manifest_metadata") or {}),
    }
    write_json(data_root / "input_manifest.json", manifest)
    return manifest


def _build_task_info(
    record: dict[str, Any],
    mode: str,
    task_id: str,
    data_root: Path,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    package = record["benchmark_package"]
    spec = MODE_SPEC[mode]
    candidate = (record.get("task_candidates") or {}).get(mode, {})
    override = (record.get("mode_overrides") or {}).get(mode, {})
    question = (
        candidate.get("question") or override.get("central_problem") or record["central_problem"]
    )
    task_text = (
        package_value(package, "task_instruction", mode)
        or package_value(package, "task_instructions", mode)
        or question
    )
    deliverables = package_value(package, "required_deliverables", mode)
    if not deliverables:
        deliverables = [
            {
                "path": path,
                "description": description,
                **({"allow_empty": True} if path.endswith("failure_log.jsonl") else {}),
            }
            for path, description in DEFAULT_DELIVERABLES[mode]
        ]
    description = {
        "paper_reproduction": "The paper-derived route and method are disclosed, but numerical targets remain hidden and must be regenerated through managed computation.",
        "conclusion_guided_reconstruction": "The target conclusion and starting evidence are disclosed; the agent must independently design and execute a valid verification route.",
        "autonomous_research": "The scientific objective and starting evidence are fixed; the agent must independently formulate, execute, validate, and revise the research route.",
        "mechanistic_rule_discovery": "Comparable systems are disclosed; the agent must infer an interpretable rule and test it on held-out systems.",
    }[mode]
    scientific_requirements = package_value(package, "scientific_requirements", mode)
    return {
        "task_id": task_id,
        "source_id": stable_id("source", record["paper_id"]),
        "category": package.get("category", "end_to_end_scientific_investigation"),
        "task": task_text,
        "scientific_mode": spec["scientific_mode"],
        "scientific_mode_description": description,
        "scientific_requirements": scientific_requirements,
        "required_deliverables": deliverables,
        "data": [
            {
                "name": package.get("input_name", "ResearchChemBench task inputs"),
                "path": "data/benchmark_data",
                "type": "directory",
                "description": f"{len(manifest['files'])} hashed solver-visible files. No hidden reference answer or author computational output is included.",
            }
        ],
        "benchmark_family": package.get(
            "benchmark_family", "ResearchChemBench literature-derived tasks"
        ),
        "task_mode": spec["task_mode"],
        "method_disclosure": (
            "Paper-derived method parameters and workflow are supplied in data/benchmark_data/method_protocol.json."
            if mode == "paper_reproduction"
            else "No paper method or preferred computational route is disclosed."
        ),
        "pathway_disclosure": (
            "The workflow stages are disclosed; the preferred mechanism and numerical results are not."
            if mode == "paper_reproduction"
            else (
                "The target conclusion is disclosed, but the verification route and paper outputs are not."
                if mode == "conclusion_guided_reconstruction"
                else "No preferred pathway, mechanism, rule, or hypothesis ranking is disclosed."
            )
        ),
    }


def _build_ground_truth(
    record: dict[str, Any],
    mode: str,
    data_root: Path,
    manifest: dict[str, Any],
    quality: dict[str, Any],
) -> dict[str, Any]:
    package = record["benchmark_package"]
    hidden = package["ground_truth"]
    manifest_path = data_root / "input_manifest.json"
    hidden_files = []
    for raw in (record.get("assets") or {}).get("hidden_reference_files", []):
        path = Path(raw)
        if path.exists():
            hidden_files.append(
                {"name": path.name, "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
            )
    evidence_policy = hidden.get("evidence_gate_policy") or {
        "judge_must_assess_all": True,
        "gates": hidden.get("evidence_gates", []),
    }
    managed_policy = hidden.get("managed_computation_policy") or {
        "required": True,
        "minimum_successful_scientific_calls": 3,
        "score_cap_without_managed_attempt": 20,
        "score_cap_without_successful_managed_call": 40,
        "score_cap_below_minimum_successes": 70,
    }
    reference_evidence = deepcopy(hidden.get("reference_evidence") or {})
    reference_evidence.update(
        {
            "source_id": stable_id("source", record["paper_id"]),
            "input_manifest_sha256": sha256_file(manifest_path),
            "hidden_reference_files": hidden_files,
            "pipeline_quality_score": quality["score"],
        }
    )
    return {
        "expected_tool_calls": hidden.get("expected_tool_calls", []),
        "expected_result": hidden["expected_result"],
        "expected_structured_output": hidden.get("expected_structured_output"),
        "evaluation_mode": "dual_axis_100",
        "evaluation_profile": MODE_SPEC[mode]["evaluation_profile"],
        "score_max": 100,
        "scoring_rubric": deepcopy(
            REPRODUCTION_PROCESS_RUBRIC
            if MODE_SPEC[mode]["reproduction"]
            else AUTONOMOUS_PROCESS_RUBRIC
        ),
        "scientific_conclusion_rubric": hidden["scientific_conclusion_rubric"],
        "dual_axis_scoring_policy": deepcopy(DUAL_AXIS_POLICY),
        "critical_failures": hidden.get("critical_failures", []),
        "judge_instructions": hidden.get(
            "judge_instructions",
            "Score only artifact-supported conclusions. Treat the supplied experimental observations as inputs, not as newly computed evidence. Apply every task-specific evidence gate before assigning the final multiplicative score.",
        ),
        "reference_evidence": reference_evidence,
        "managed_computation_policy": managed_policy,
        "evidence_gate_policy": evidence_policy,
        "reference_conclusion_gate_policy": hidden.get("reference_conclusion_gate_policy", {}),
        "current_toolbox_feasibility_baseline": hidden.get(
            "current_toolbox_feasibility_baseline", {}
        ),
        "current_toolbox_reproduction_baseline": hidden.get(
            "current_toolbox_reproduction_baseline", {}
        ),
    }


def _validate_against_benchmark_schema(
    task_info: dict[str, Any], ground_truth: dict[str, Any], benchmark_root: Path
) -> None:
    root = str(benchmark_root)
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        from evaluation.task_schema import GroundTruth, TaskInfo
    except ImportError as exc:
        raise RuntimeError(
            f"cannot import ResearchChemBench evaluator schema from {benchmark_root}"
        ) from exc
    TaskInfo.model_validate(task_info)
    GroundTruth.model_validate(ground_truth)


def _assert_no_public_leakage(
    record: dict[str, Any], mode: str, task_info: dict[str, Any], data_root: Path
) -> None:
    text_chunks = [json.dumps(task_info, ensure_ascii=False)]
    for path in data_root.rglob("*"):
        if path.is_file():
            try:
                text_chunks.append(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue
    public = "\n".join(text_chunks).casefold()
    leaks = [
        str(marker)
        for marker in (package_value(record["benchmark_package"], "leakage_markers", mode) or [])
        if str(marker).casefold() in public
    ]
    if leaks:
        raise ValueError(f"{mode} public package leaks hidden markers: {', '.join(leaks)}")


def _render_data_readme(record: dict[str, Any], mode: str, files: list[str]) -> str:
    disclosure = (
        "The method protocol is supplied for guided reproduction. Numerical paper results, author outputs, and the preferred conclusion are withheld."
        if mode == "paper_reproduction"
        else (
            "The target conclusion and starting evidence are supplied, but the paper route and computed outputs are withheld."
            if mode == "conclusion_guided_reconstruction"
            else "The files contain only permitted starting identities, conditions, observations, or training-system data. Paper methods, hidden results, and the preferred conclusion or rule are withheld."
        )
    )
    listing = "\n".join(f"- `{path}`" for path in sorted(files))
    return (
        "# Benchmark Inputs\n\n"
        f"{disclosure}\n\n"
        "## Files\n\n"
        f"{listing}\n\n"
        "Treat molecular identities, charges, multiplicities, units, and atom mappings as part of the input contract. "
        "Do not modify the supplied files; write all generated artifacts under `report/` or tool-managed output directories.\n"
    )


def _public_evidence(record: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            key: value
            for key, value in item.items()
            if key not in {"relation", "target_hypothesis", "gold_role"}
        }
        for item in record.get("evidence", [])
        if item.get("visibility", "private") == "public"
    ]


def _file_record(root: Path, path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def _safe_destination(root: Path, relative: str) -> Path:
    if not relative or "\\" in relative or "\x00" in relative:
        raise ValueError(f"unsafe generated file path: {relative!r}")
    destination = (root / relative).resolve()
    destination.relative_to(root.resolve())
    return destination


def _safe_task_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_.-")
    if not normalized:
        raise ValueError("empty task id")
    return normalized


def _default_task_id(record: dict[str, Any], mode: str) -> str:
    suffix = {
        "paper_reproduction": "Guided_Reproduction",
        "conclusion_guided_reconstruction": "Conclusion_Guided",
        "autonomous_research": "Autonomous_Research",
        "mechanistic_rule_discovery": "Rule_Discovery",
    }[mode]
    return f"RCB_{stable_id('', record['paper_id'], mode).strip('_')}_{suffix}"


def assign_split(paper_id: str, salt: str) -> str:
    bucket = int(hashlib.sha256(f"{salt}:{paper_id}".encode()).hexdigest()[:8], 16) % 100
    if bucket < 70:
        return "train"
    if bucket < 85:
        return "validation"
    return "test"


def _remove_previous_generated_tasks(root: Path) -> None:
    manifest_path = root / "_pipeline_manifest.json"
    if not manifest_path.is_file():
        return
    try:
        previous = read_json(manifest_path)
    except (OSError, ValueError):
        return
    for item in previous.get("tasks", []):
        relative = item.get("path")
        if not relative:
            continue
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        if candidate.is_dir():
            shutil.rmtree(candidate)

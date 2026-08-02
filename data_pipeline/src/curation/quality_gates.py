from __future__ import annotations

import json
from collections import Counter
from typing import Any

from src.core.models import selected_task_type, task_types_for_record
from src.curation.availability import assess_asset_availability
from src.curation.package_validation import package_readiness
from src.curation.task_candidates import generate_task_candidates
from src.curation.toolbox import assess_toolbox_coverage

DEFAULTS = {
    "reproduction_direct_pass": 0.8,
    "research_direct_pass": 0.5,
    "capability_pass": 0.8,
    "max_live_walltime_hours": 12.0,
    "question_pass_score": 85.0,
    "question_reject_score": 55.0,
}


def gate_scientific_records(
    records: list[dict[str, Any]],
    toolbox_profile: dict[str, Any] | None,
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    cfg = {**DEFAULTS, **(config or {})}
    output = []
    for record in records:
        enriched = dict(record)
        coverage = assess_toolbox_coverage(enriched, toolbox_profile)
        availability = assess_asset_availability(
            enriched,
            verify_urls=cfg.get("verify_asset_urls", False),
            url_timeout_seconds=cfg.get("url_timeout_seconds", 6.0),
            max_urls=cfg.get("max_asset_urls", 8),
        )
        candidates = generate_task_candidates(enriched)
        mode_reports = {}
        for mode in task_types_for_record(enriched):
            gates = [
                _gate_record_schema(enriched),
                _gate_mode_toolbox(mode, coverage, cfg),
                _gate_mode_data(mode, availability, enriched),
                _gate_method_and_workflow(mode, enriched),
                _gate_evaluator(mode, enriched),
                _gate_reference_run(enriched),
                _gate_runtime(enriched, cfg),
                _gate_question(candidates.get(mode, {}), cfg),
                _gate_leakage_and_difficulty(mode, enriched, candidates.get(mode, {})),
                _gate_complete_package(mode, enriched),
            ]
            mode_reports[mode] = {
                "decision": _aggregate_decision(gates),
                "gates": gates,
                "blocking_gates": [
                    gate["gate_id"] for gate in gates if gate["decision"] == "reject"
                ],
                "review_gates": [gate["gate_id"] for gate in gates if gate["decision"] == "review"],
            }
        enriched["toolbox_coverage"] = coverage
        enriched["asset_availability"] = availability
        enriched["task_candidates"] = candidates
        enriched["quality_funnel"] = {
            "status": "deterministic_complete",
            "mode_reports": mode_reports,
            "selected_task_type": selected_task_type(enriched),
            "accepted_task_types": [
                mode for mode, report in mode_reports.items() if report["decision"] == "pass"
            ],
            "review_task_types": [
                mode for mode, report in mode_reports.items() if report["decision"] == "review"
            ],
            "rejected_task_types": [
                mode for mode, report in mode_reports.items() if report["decision"] == "reject"
            ],
        }
        output.append(enriched)
    return output


def apply_ensemble_results(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for record in records:
        updated = dict(record)
        funnel = dict(updated.get("quality_funnel") or {})
        mode_reports = {
            mode: dict(report) for mode, report in (funnel.get("mode_reports") or {}).items()
        }
        reviews = (updated.get("model_ensemble") or {}).get("mode_reviews", {})
        for mode, review in reviews.items():
            if mode not in mode_reports or review.get("status") != "complete":
                continue
            gate = {
                "gate_id": "G9_model_consensus",
                "name": "multi-model independent quality consensus",
                "decision": review.get("decision", "review"),
                "score": review.get("median_score", 0.0),
                "reasons": review.get("issues", []),
                "evidence": {
                    "completed_reviewers": review.get("completed_reviewers", 0),
                    "decision_counts": review.get("decision_counts", {}),
                    "score_range": review.get("score_range"),
                    "vetoes": review.get("vetoes", []),
                },
            }
            gates = list(mode_reports[mode].get("gates", [])) + [gate]
            mode_reports[mode]["gates"] = gates
            mode_reports[mode]["decision"] = _aggregate_decision(gates)
            mode_reports[mode]["blocking_gates"] = [
                g["gate_id"] for g in gates if g["decision"] == "reject"
            ]
            mode_reports[mode]["review_gates"] = [
                g["gate_id"] for g in gates if g["decision"] == "review"
            ]
        funnel["mode_reports"] = mode_reports
        funnel["accepted_task_types"] = [
            mode for mode, report in mode_reports.items() if report["decision"] == "pass"
        ]
        funnel["review_task_types"] = [
            mode for mode, report in mode_reports.items() if report["decision"] == "review"
        ]
        funnel["rejected_task_types"] = [
            mode for mode, report in mode_reports.items() if report["decision"] == "reject"
        ]
        funnel["status"] = (
            "ensemble_complete" if reviews else funnel.get("status", "deterministic_complete")
        )
        updated["quality_funnel"] = funnel
        output.append(updated)
    return output


def quality_funnel_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = Counter()
    gate_outcomes = Counter()
    toolbox_failures = Counter()
    for record in records:
        funnel = record.get("quality_funnel") or {}
        for mode, report in (funnel.get("mode_reports") or {}).items():
            decisions[f"{mode}:{report.get('decision', 'unknown')}"] += 1
            for gate in report.get("gates", []):
                gate_outcomes[f"{gate.get('gate_id')}:{gate.get('decision')}"] += 1
        coverage = record.get("toolbox_coverage") or {}
        toolbox_failures.update(coverage.get("unavailable", []))
        toolbox_failures.update(coverage.get("unknown", []))
    return {
        "records": len(records),
        "mode_decisions": dict(decisions),
        "gate_outcomes": dict(gate_outcomes),
        "uncovered_or_unavailable_software": dict(toolbox_failures),
    }


def _gate_record_schema(record: dict[str, Any]) -> dict[str, Any]:
    validation = record.get("schema_validation") or {}
    decision = "pass" if validation.get("passed") else "reject"
    return _gate(
        "G0_schema",
        "structured record schema",
        decision,
        100 if decision == "pass" else 0,
        validation.get("errors", []),
    )


def _gate_mode_toolbox(mode: str, coverage: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    direct = coverage.get("direct_coverage", 0.0)
    capability = coverage.get("capability_coverage", 0.0)
    blocked = coverage.get("unavailable", [])
    priority_match = bool(coverage.get("priority_matches")) and coverage.get(
        "preserve_priority_matches", True
    )
    threshold = (
        cfg["reproduction_direct_pass"]
        if mode == "paper_reproduction"
        else cfg["research_direct_pass"]
    )
    if priority_match:
        decision = (
            "pass" if direct >= threshold or capability >= cfg["capability_pass"] else "review"
        )
    elif blocked and direct < threshold and capability < cfg["capability_pass"]:
        decision = "review"
    elif direct >= threshold or capability >= cfg["capability_pass"]:
        decision = "pass"
    else:
        decision = "review"
    reasons = []
    if blocked:
        reasons.append("unavailable: " + ", ".join(blocked))
    if coverage.get("unknown"):
        reasons.append("unknown: " + ", ".join(coverage["unknown"]))
    if coverage.get("functional_validation_pending"):
        reasons.append(
            "mapped but requires task-level functional validation: "
            + ", ".join(coverage["functional_validation_pending"])
        )
    return _gate(
        "G1_toolbox_coverage",
        "software and functional capability coverage",
        decision,
        100 * max(direct, capability),
        reasons,
        coverage,
    )


def _gate_mode_data(
    mode: str,
    availability: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    assessment = (availability.get("mode_assessment") or {}).get(mode, {})
    public_inputs = (record.get("benchmark_package") or {}).get("public_inputs") or {}
    generated_input_count = _materializable_public_inputs(public_inputs)
    visible_count = int(assessment.get("visible_file_count") or 0)
    materialized_record_count = int(assessment.get("materialized_input_count") or 0)
    reconstructible_record_count = int(assessment.get("reconstructible_input_count") or 0)
    materializable = visible_count > 0 or materialized_record_count > 0 or generated_input_count > 0
    availability_state = availability.get("availability_state", "pending_discovery")
    reasons = []
    if not assessment.get("structured_input_count"):
        reasons.append("no structured starting inputs have yet been extracted")
    if not materializable:
        reasons.append(
            f"no copyable or generated agent-visible input package is currently materialized for {mode}"
        )
    if reconstructible_record_count and not materializable:
        reasons.append(
            "starting inputs are described as reconstructible but have not been materialized"
        )
    if availability_state in {
        "pending_discovery",
        "pending_acquisition",
        "unresolved_after_discovery",
    }:
        reasons.append(availability.get("status_note", "external asset resolution is pending"))
    if not assessment.get("reference_evidence_count"):
        reasons.append("hidden reference evidence is missing")
    if availability_state in {"confirmed_unavailable", "access_restricted"}:
        decision = "reject"
    elif (
        availability_state == "validated"
        and materializable
        and assessment.get("reference_evidence_count")
    ):
        decision = "pass"
    else:
        decision = "review"
    evidence = {
        **assessment,
        "generated_materializable_inputs": generated_input_count,
        "materializable": materializable,
        "availability_state": availability_state,
    }
    return _gate(
        "G2_data_availability",
        "open and reconstructible task inputs",
        decision,
        assessment.get("score", 0),
        reasons,
        evidence,
    )


def _gate_method_and_workflow(mode: str, record: dict[str, Any]) -> dict[str, Any]:
    methods = len(record.get("methods", []))
    workflow = len(record.get("workflow", []))
    if mode == "paper_reproduction":
        score = min(100.0, methods * 20 + workflow * 12)
        decision = "pass" if methods >= 2 and workflow >= 3 else "review"
    elif mode == "autonomous_research":
        score = min(
            100.0, methods * 12 + workflow * 14 + len(record.get("expected_outputs", [])) * 10
        )
        decision = "pass" if workflow >= 3 and record.get("expected_outputs") else "review"
    elif mode == "conclusion_guided_reconstruction":
        score = min(
            100.0, methods * 12 + workflow * 10 + len(record.get("reference_results", [])) * 18
        )
        decision = "pass" if methods and record.get("reference_results") else "review"
    else:
        systems = int((record.get("information_richness") or {}).get("comparable_system_count", 0))
        score = min(100.0, systems * 10 + workflow * 8 + len(record.get("evidence", [])) * 5)
        decision = "pass" if systems >= 3 and record.get("evidence") else "review"
    return _gate(
        "G3_protocol_extractability",
        "method parameters and workflow extractability",
        decision,
        score,
        [] if decision == "pass" else ["record needs a more explicit executable workflow"],
    )


def _gate_evaluator(mode: str, record: dict[str, Any]) -> dict[str, Any]:
    expected = len(record.get("expected_outputs", []))
    evidence = len(record.get("evidence", []))
    references = len(record.get("reference_results", []))
    relations = sum(
        1 for item in record.get("evidence", []) if item.get("relation") in {"supports", "refutes"}
    )
    score = min(100.0, expected * 15 + evidence * 5 + references * 15 + relations * 5)
    if mode == "mechanistic_rule_discovery":
        systems = int((record.get("information_richness") or {}).get("comparable_system_count", 0))
        decision = "pass" if expected and references and systems >= 3 else "review"
    else:
        decision = "pass" if expected and evidence >= 2 and references else "review"
    if not expected and not evidence and not references:
        decision = "reject"
    return _gate(
        "G4_evaluator_constructability",
        "automatic and process-level evaluator constructability",
        decision,
        score,
        [] if decision == "pass" else ["gold outputs or discriminative evidence are incomplete"],
    )


def _gate_runtime(record: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    runtime = record.get("runtime") or {}
    hours = runtime.get("measured_walltime_hours")
    if hours is None:
        hours = runtime.get("estimated_walltime_hours")
    cache = runtime.get("cache_policy")
    if hours is None:
        return _gate(
            "G5_runtime",
            "bounded runtime and cache policy",
            "review",
            30,
            ["walltime is not estimated"],
            runtime,
        )
    if hours <= cfg["max_live_walltime_hours"] or cache in {"hybrid", "precomputed"}:
        return _gate("G5_runtime", "bounded runtime and cache policy", "pass", 100, [], runtime)
    if hours <= 48:
        return _gate(
            "G5_runtime",
            "bounded runtime and cache policy",
            "review",
            50,
            ["long task requires checkpointing or cached expensive jobs"],
            runtime,
        )
    return _gate(
        "G5_runtime",
        "bounded runtime and cache policy",
        "reject",
        0,
        ["runtime exceeds budget without a cache policy"],
        runtime,
    )


def _gate_reference_run(record: dict[str, Any]) -> dict[str, Any]:
    reference = record.get("reference_run") or {}
    status = reference.get("status")
    artifacts = reference.get("artifacts") or []
    artifacts_verified = bool(artifacts) and all(
        item.get("exists") is True and item.get("sha256") for item in artifacts
    )
    if status == "validated" and artifacts_verified and not reference.get("validation_failures"):
        return _gate(
            "G5_reference_run",
            "real reference execution and artifact validation",
            "pass",
            100,
            [],
            reference,
        )
    if status in {"failed", "invalid"}:
        return _gate(
            "G5_reference_run",
            "real reference execution and artifact validation",
            "reject",
            0,
            ["reference execution failed or produced invalid artifacts"],
            reference,
        )
    return _gate(
        "G5_reference_run",
        "real reference execution and artifact validation",
        "review",
        30,
        ["one real reference execution is required before release"],
        reference,
    )


def _gate_question(candidate: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    quality = candidate.get("quality") or {}
    score = quality.get("score", 0.0)
    if score >= cfg["question_pass_score"]:
        decision = "pass"
    elif score < cfg["question_reject_score"]:
        decision = "reject"
    else:
        decision = "review"
    return _gate(
        "G6_question_quality",
        "generated scientific question quality",
        decision,
        score,
        quality.get("failed_checks", []),
        quality,
    )


def _gate_leakage_and_difficulty(
    mode: str, record: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    quality = candidate.get("quality") or {}
    checks = quality.get("checks") or {}
    hard_leak = not checks.get("no_exact_gold_number", True)
    source_leak = not checks.get("no_source_identity", True)
    tools = len(
        {_stable_value(value) for value in record.get("tools", []) + record.get("methods", [])}
    )
    workflow = len(record.get("workflow", []))
    hypotheses = len(record.get("hypotheses", []))
    complexity = (
        tools
        + workflow
        + (hypotheses if mode in {"autonomous_research", "mechanistic_rule_discovery"} else 0)
    )
    if hard_leak:
        decision = "reject"
    elif source_leak or complexity < 3:
        decision = "review"
    else:
        decision = "pass"
    reasons = []
    if hard_leak:
        reasons.append("question exposes a private numeric result")
    if source_leak:
        reasons.append("question repeats source-paper identity")
    if complexity < 3:
        reasons.append("task may be too shallow to discriminate strong agents")
    return _gate(
        "G7_leakage_difficulty",
        "answer leakage, shortcuts, and task difficulty",
        decision,
        min(100, complexity * 12),
        reasons,
        {"complexity_signal": complexity},
    )


def _stable_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _materializable_public_inputs(public_inputs: dict[str, Any]) -> int:
    count = 0
    files = public_inputs.get("files") or {}
    if isinstance(files, dict):
        count += sum(1 for value in files.values() if _inline_file_content(value))
    for field in ("reaction", "molecular_systems", "training_systems", "heldout_systems"):
        value = public_inputs.get(field)
        items = value if isinstance(value, list) else [value] if isinstance(value, dict) else []
        count += sum(
            1
            for item in items
            if isinstance(item, dict)
            and any(
                item.get(key)
                for key in (
                    "smiles",
                    "inchi",
                    "coordinates",
                    "xyz",
                    "cif",
                    "structure",
                    "stoichiometry",
                )
            )
        )
    return count


def _inline_file_content(value: Any) -> bool:
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        descriptive = {"description", "path", "file_id", "name", "availability", "status"}
        return bool(set(value) - descriptive)
    if not isinstance(value, str) or not value.strip():
        return False
    lower = value.casefold()
    description_markers = (
        "file with columns",
        "directory containing",
        "not provided",
        "downloadable",
        "must be constructed",
    )
    return "\n" in value or not any(marker in lower for marker in description_markers)


def _gate_complete_package(mode: str, record: dict[str, Any]) -> dict[str, Any]:
    package = record.get("benchmark_package") or {}
    public_inputs = package.get("public_inputs") or {}
    rubric = (package.get("ground_truth") or {}).get("scientific_conclusion_rubric") or []
    readiness = package_readiness(record, mode)
    missing = readiness["errors"]
    if not missing:
        return _gate(
            "G8_complete_package",
            "complete ResearchChemBench evaluation suite",
            "pass",
            100,
            [],
            {
                "public_input_sections": sorted(
                    key for key, value in public_inputs.items() if value
                ),
                "rubric_items": len(rubric),
            },
        )
    # Missing package fields are a curation requirement, not evidence that the
    # source paper itself is unusable. The strict builder still refuses to emit
    # a task until every field passes package_readiness().
    decision = "review"
    score = max(0, 100 - 15 * len(missing))
    return _gate(
        "G8_complete_package",
        "complete ResearchChemBench evaluation suite",
        decision,
        score,
        missing,
        {"missing": missing},
    )


def _gate(
    gate_id: str,
    name: str,
    decision: str,
    score: float,
    reasons: list[str],
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "name": name,
        "decision": decision,
        "score": round(float(score), 1),
        "reasons": reasons,
        "evidence": evidence or {},
    }


def _aggregate_decision(gates: list[dict[str, Any]]) -> str:
    decisions = {gate.get("decision") for gate in gates}
    if "reject" in decisions:
        return "reject"
    if "review" in decisions:
        return "review"
    return "pass"

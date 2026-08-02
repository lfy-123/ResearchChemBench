from __future__ import annotations

import json
import os
import statistics
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.core.logging import log_progress
from src.core.models import task_types_for_record
from src.curation.llm_client import call_json_chat

REVIEW_DIMENSIONS = (
    "scientific_grounding",
    "tool_and_data_feasibility",
    "question_clarity",
    "difficulty_and_nontriviality",
    "evaluation_verifiability",
    "leakage_resistance",
)

VETO_LABELS = {
    "unsupported_scientific_claim",
    "tool_unavailable",
    "data_unavailable",
    "not_evaluable",
    "answer_leakage",
    "scientifically_invalid",
}

ROLE_GUIDANCE = {
    "scientific_grounding": (
        "Focus on whether every public fact, hidden finding, numerical range, and mechanistic claim is "
        "traceable to supplied evidence. Flag invented chemistry and conclusions stronger than the source."
    ),
    "tool_data_feasibility": (
        "Focus on whether the solver-visible inputs are real and sufficient, and whether required operations "
        "are covered by the configured chemistry toolbox. Distinguish described data from materialized files."
    ),
    "evaluation_design": (
        "Focus on whether the question is unambiguous and the hidden reference, 3-10 scoring findings, "
        "acceptance rules, tolerances, and alternative valid routes make the task objectively scoreable."
    ),
    "leakage_difficulty": (
        "Focus on answer leakage, paper fingerprints, triviality, and whether the task requires meaningful "
        "planning or computation rather than retrieval or copying. Do not reject merely because the paper is published."
    ),
}


def review_with_ensemble(
    records: list[dict[str, Any]],
    config: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    config = config or {}
    if not config.get("enabled", False):
        return [
            {
                **record,
                "model_ensemble": {
                    "status": "disabled",
                    "mode_reviews": {},
                    "note": "Enable after configuring independent OpenAI-compatible reviewers or offline verdict files.",
                },
            }
            for record in records
        ]

    output = []
    reviewers = config.get("reviewers", [])
    total = len(records)
    for index, record in enumerate(records, start=1):
        mode_reviews = {}
        for mode in task_types_for_record(record):
            verdicts = []
            failures = []
            max_workers = max(1, min(int(config.get("max_workers", 1)), len(reviewers) or 1))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_reviewers = {
                    executor.submit(_run_reviewer, record, mode, reviewer, config): reviewer
                    for reviewer in reviewers
                }
                for future in as_completed(future_reviewers):
                    reviewer = future_reviewers[future]
                    try:
                        verdicts.append(future.result())
                    except Exception as exc:
                        failures.append(
                            {
                                "reviewer": reviewer.get("name", reviewer.get("model")),
                                "error": str(exc),
                            }
                        )
            mode_reviews[mode] = _aggregate(verdicts, failures, config)
        updated = dict(record)
        updated["model_ensemble"] = {
            "status": "complete" if mode_reviews else "unavailable",
            "mode_reviews": mode_reviews,
            "reviewer_count": len(reviewers),
        }
        output.append(updated)
        log_progress(
            "stage_16_model_ensemble",
            index,
            total,
            record.get("paper_id", str(index)),
            status=updated["model_ensemble"]["status"],
        )
    return output


def ensemble_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = Counter()
    decisions = Counter()
    failures = 0
    for record in records:
        ensemble = record.get("model_ensemble") or {}
        statuses[ensemble.get("status", "unknown")] += 1
        for mode, review in (ensemble.get("mode_reviews") or {}).items():
            decisions[f"{mode}:{review.get('decision', 'unknown')}"] += 1
            failures += len(review.get("failures", []))
    return {
        "records": len(records),
        "statuses": dict(statuses),
        "mode_decisions": dict(decisions),
        "reviewer_failures": failures,
    }


def _run_reviewer(
    record: dict[str, Any],
    mode: str,
    reviewer: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    name = reviewer.get("name") or reviewer.get("model")
    offline_dir = reviewer.get("offline_verdict_dir") or config.get("offline_verdict_dir")
    if offline_dir:
        path = Path(offline_dir) / f"{record['paper_id']}__{mode}__{name}.json"
        if path.exists():
            verdict = json.loads(path.read_text(encoding="utf-8"))
            normalized = _normalize_verdict(
                verdict, name, reviewer.get("role", "general"), "offline_file"
            )
            return _reconcile_candidate_verdict(normalized, record)

    api_key = reviewer.get("api_key")
    if not api_key and reviewer.get("api_key_env"):
        api_key = os.environ.get(reviewer["api_key_env"])
    if not api_key:
        api_key = os.environ.get("RCB_LLM_API_KEY")
    if not api_key:
        raise ValueError(f"missing API key for reviewer {name}")

    model = reviewer["model"]
    base_url = reviewer.get("base_url", "https://api.openai.com/v1").rstrip("/")
    verdict, metadata = call_json_chat(
        model=model,
        base_url=base_url,
        api_key=api_key,
        system_prompt=_system_prompt(reviewer.get("role", "general")),
        user_content=json.dumps(_review_packet(record, mode), ensure_ascii=False),
        timeout_seconds=float(reviewer.get("timeout_seconds", 300)),
        max_tokens=reviewer.get("max_tokens"),
        retries=int(reviewer.get("retries", config.get("retries", 2))),
        thinking=reviewer.get("thinking", config.get("thinking")),
    )
    normalized = _normalize_verdict(verdict, name, reviewer.get("role", "general"), "api")
    normalized["llm_call"] = metadata
    return _reconcile_candidate_verdict(normalized, record)


def _aggregate(
    verdicts: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    minimum = config.get("minimum_completed_reviewers", 3)
    if len(verdicts) < minimum:
        return {
            "status": "incomplete",
            "decision": "review",
            "completed_reviewers": len(verdicts),
            "failures": failures,
            "verdicts": verdicts,
            "issues": [f"only {len(verdicts)} independent reviewers completed; need {minimum}"],
        }
    scores = [item["score"] for item in verdicts]
    decisions = Counter(item["decision"] for item in verdicts)
    vetoes = sorted(
        {veto for item in verdicts for veto in item.get("vetoes", []) if veto in VETO_LABELS}
    )
    median = statistics.median(scores)
    score_range = max(scores) - min(scores)
    pass_quorum = config.get("pass_quorum", 0.67)
    reject_quorum = config.get("reject_quorum", 0.5)
    max_disagreement = config.get("max_score_range", 30)
    min_median = config.get("minimum_median_score", 75)
    if vetoes or decisions["reject"] / len(verdicts) >= reject_quorum:
        decision = "reject"
    elif (
        decisions["pass"] / len(verdicts) >= pass_quorum
        and median >= min_median
        and score_range <= max_disagreement
    ):
        decision = "pass"
    else:
        decision = "review"
    issues = list(dict.fromkeys(issue for item in verdicts for issue in item.get("issues", [])))
    if score_range > max_disagreement:
        issues.append("large cross-model disagreement")
    return {
        "status": "complete",
        "decision": decision,
        "completed_reviewers": len(verdicts),
        "median_score": round(float(median), 1),
        "score_range": round(float(score_range), 1),
        "decision_counts": dict(decisions),
        "vetoes": vetoes,
        "issues": issues,
        "failures": failures,
        "verdicts": verdicts,
    }


def _reconcile_candidate_verdict(verdict: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    """Prevent candidate-stage unknowns from being promoted to factual vetoes."""

    reconciled = dict(verdict)
    asset_state = str(
        (record.get("asset_availability") or {}).get("availability_state") or "pending_discovery"
    )
    coverage = record.get("toolbox_coverage") or {}
    coverage_state = str(coverage.get("coverage_state") or "")
    kept = []
    downgraded = []
    for veto in verdict.get("vetoes", []):
        if veto == "data_unavailable" and asset_state not in {
            "confirmed_unavailable",
            "access_restricted",
        }:
            downgraded.append(
                f"data availability is {asset_state}; acquisition/discovery is pending rather than confirmed unavailable"
            )
            continue
        if veto == "tool_unavailable" and coverage_state != "confirmed_unavailable":
            downgraded.append(
                "tool coverage is not confirmed unavailable; task-level functional validation is pending"
            )
            continue
        kept.append(veto)
    reconciled["vetoes"] = kept
    reconciled["issues"] = list(dict.fromkeys(verdict.get("issues", []) + downgraded))
    if (
        verdict.get("decision") == "reject"
        and downgraded
        and not kept
        and verdict.get("role") == "tool_data_feasibility"
    ):
        reconciled["decision"] = "review"
    return reconciled


def _normalize_verdict(
    verdict: dict[str, Any], reviewer: str, role: str, source: str
) -> dict[str, Any]:
    decision = verdict.get("decision", "review")
    if decision not in {"pass", "review", "reject"}:
        decision = "review"
    dimensions = {
        name: max(0, min(100, float((verdict.get("dimensions") or {}).get(name, 0))))
        for name in REVIEW_DIMENSIONS
    }
    score = verdict.get("score")
    if score is None:
        score = sum(dimensions.values()) / len(dimensions)
    return {
        "reviewer": reviewer,
        "role": role,
        "source": source,
        "decision": decision,
        "score": round(max(0, min(100, float(score))), 1),
        "confidence": round(max(0, min(1, float(verdict.get("confidence", 0.5)))), 2),
        "dimensions": dimensions,
        "issues": [str(value) for value in verdict.get("issues", [])],
        "vetoes": [str(value) for value in verdict.get("vetoes", [])],
        "evidence_refs": [str(value) for value in verdict.get("evidence_refs", [])],
    }


def _review_packet(record: dict[str, Any], mode: str) -> dict[str, Any]:
    candidate = (record.get("task_candidates") or {}).get(mode, {})
    package = record.get("benchmark_package") or {}
    solver_visible_package = {
        key: value
        for key, value in package.items()
        if key not in {"ground_truth", "leakage_markers"}
    }
    return {
        "mode": mode,
        "question": candidate.get("question"),
        "central_problem": record.get("central_problem"),
        "inputs": record.get("inputs", []),
        "expected_outputs": record.get("expected_outputs", []),
        "methods": record.get("methods", []),
        "workflow": record.get("workflow", []),
        "hypotheses": record.get("hypotheses", []),
        "controls": record.get("controls", []),
        "evidence": record.get("evidence", []),
        "runtime": record.get("runtime", {}),
        "toolbox_coverage": record.get("toolbox_coverage", {}),
        "asset_availability": record.get("asset_availability", {}),
        "solver_visible_package": solver_visible_package,
        "reviewer_only_hidden_reference": {
            "ground_truth": package.get("ground_truth", {}),
            "leakage_markers": package.get("leakage_markers", []),
        },
        "visibility_policy": {
            "paper_pdf_visible_to_solver": False,
            "ground_truth_visible_to_solver": False,
            "leakage_markers_visible_to_solver": False,
            "internet_access": False,
        },
        "deterministic_report": (record.get("quality_funnel") or {})
        .get("mode_reports", {})
        .get(mode, {}),
    }


def _system_prompt(role: str) -> str:
    return f"""You are an independent benchmark-data reviewer with the role '{role}'.
Role-specific focus: {ROLE_GUIDANCE.get(role, "Perform a balanced end-to-end review.")}
Assess one ResearchChemBench task candidate before external-asset acquisition and reference execution.
Reject unsupported chemistry, confirmed-unavailable required tools/data, intrinsically unscorable hidden
references, direct answer leakage, or scientifically invalid protocols. Use review, not reject, when assets
are pending_discovery, pending_acquisition, acquired_unvalidated, or unresolved_after_discovery; these
states mean the current run only received PDFs and has not established that open data are unavailable.
Use data_unavailable only when asset_availability.availability_state is confirmed_unavailable or
access_restricted. Use tool_unavailable only when toolbox_coverage.coverage_state is
confirmed_unavailable and no covered functional alternative exists. Unknown runtime or missing reference
runs are release work items and should normally receive review rather than reject.
The reviewer_only_hidden_reference and leakage_markers are intentionally visible to you but are never
shown to the solver. The source paper is also not solver-visible and the evaluation has no internet access.
Do not flag leakage merely because hidden reference values come from a published paper. Flag leakage only
when solver_visible_package, question, or other public inputs reveal the hidden answer or source identity.
Do not reward polished wording when evidence is absent. Score these dimensions from 0 to 100:
{", ".join(REVIEW_DIMENSIONS)}.
Return JSON only with keys: decision (pass/review/reject), score, confidence, dimensions,
issues, vetoes, evidence_refs. Allowed vetoes are: {", ".join(sorted(VETO_LABELS))}.
Use evidence_refs to point to supplied record fields; do not invent facts."""

"""LLM judges for rubric-based ResearchChemBench scientific tasks."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from ..execution.progress import append_progress_event
from ..provenance.results import write_workspace_results
from ..provenance.trace import (
    canonical_tool_trace_metadata,
    load_native_agent_trace,
    load_tool_trace,
    normalized_tool_calls,
    process_metrics,
)
from ..repository import get_run_workspace, load_task_package
from ..settings import JUDGE_API_BASE, JUDGE_API_KEY, JUDGE_MODEL_NAME
from .policies import (
    _apply_criterion_score_limit,
    _apply_rubric_score_cap,
    _evidence_gate_cap,
    _managed_computation_cap,
    _normalize_rubric_verdict,
    _normalize_scientific_conclusions,
    _parse_judge_json,
    _reference_conclusion_cap,
    _structured_conclusion_mismatches,
)
from .prompts import (
    AUTONOMOUS_DISCOVERY_JUDGE_PROMPT,
    DUAL_AXIS_JUDGE_SYSTEM_PROMPT,
    JUDGE_SYSTEM_PROMPT,
    JUDGE_USER_TEMPLATE,
    PAPER_REPRODUCTION_JUDGE_PROMPT,
    RUBRIC_JUDGE_SYSTEM_PROMPT,
    RUBRIC_JUDGE_USER_TEMPLATE,
    STRICT_AUTONOMOUS_DISCOVERY_JUDGE_PROMPT,
)
from .adapters import EvaluatorAdapterError, RuntimeEvaluation, load_runtime_evaluation


def _default_judge_call(
    prompt: str,
    *,
    system_prompt: str = JUDGE_SYSTEM_PROMPT,
    score_max: int = 1,
) -> dict[str, Any]:
    from openai import OpenAI

    api_key = os.environ.get("JUDGE_API_KEY", JUDGE_API_KEY)
    api_base = os.environ.get("JUDGE_API_BASE", JUDGE_API_BASE)
    model = os.environ.get("JUDGE_MODEL_NAME", JUDGE_MODEL_NAME)
    if not api_key or not api_base or not model:
        raise RuntimeError(
            "Judge configuration missing: set JUDGE_API_KEY, JUDGE_API_BASE, and JUDGE_MODEL_NAME"
        )
    client = OpenAI(api_key=api_key, base_url=api_base)
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    verdict = _parse_judge_json(
        response.choices[0].message.content or "", score_max=score_max
    )
    verdict["_judge_model"] = model
    usage = getattr(response, "usage", None)
    if usage is not None:
        verdict["_judge_usage"] = {
            "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
            "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
            "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
        }
    return verdict


def _compact_value(value: Any, *, depth: int = 0) -> Any:
    if depth >= 4:
        return "<nested value omitted>"
    if isinstance(value, dict):
        items = list(value.items())
        compact = {
            str(key): _compact_value(item, depth=depth + 1)
            for key, item in items[:30]
        }
        if len(items) > 30:
            compact["_omitted_keys"] = len(items) - 30
        return compact
    if isinstance(value, list):
        values = [_compact_value(item, depth=depth + 1) for item in value[:20]]
        if len(value) > 20:
            values.append(f"<{len(value) - 20} additional items omitted>")
        return values
    if isinstance(value, str) and len(value) > 1000:
        return value[:1000] + "…<truncated>"
    return value


def _tool_events_for_judge(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = events[:250]
    values = []
    for event in selected:
        request = event.get("arguments", {}).get("request", {})
        values.append(
            {
                "sequence": event.get("sequence"),
                "tool": event.get("tool"),
                "status": event.get("status"),
                "duration_seconds": event.get("duration_seconds"),
                "backend_id": request.get("backend_id"),
                "component_backends": _compact_value(
                    request.get("component_backends", {})
                ),
                "inputs": _compact_value(request.get("inputs", {})),
                "method_spec": _compact_value(request.get("method_spec", {})),
                "action_settings": _compact_value(
                    request.get("action_settings", {})
                ),
                "resource_limits": _compact_value(
                    request.get("resource_limits", {})
                ),
                "result_path": event.get("result_path"),
                "result_preview": _compact_value(event.get("result_preview", "")),
                "error": _compact_value(event.get("error")),
            }
        )
    if len(events) > len(selected):
        values.append({"omitted_tool_events": len(events) - len(selected)})
    return values


def _native_events_for_judge(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = events[:250]
    values = [
        {
            "sequence": event.get("sequence"),
            "source": event.get("source"),
            "session_id": event.get("session_id"),
            "session_step_index": event.get("session_step_index"),
            "tool": event.get("tool"),
            "status": event.get("status"),
            "duration_seconds": event.get("duration_seconds"),
            "arguments": _compact_value(event.get("arguments", {})),
            "result_preview": _compact_value(event.get("result_preview", "")),
            "exit_code": event.get("exit_code"),
            "error": _compact_value(event.get("error")),
            "managed_scientific_evidence": False,
            "evidence_boundary": (
                "OpenCode built-in only; may prepare/inspect/write but cannot establish managed "
                "scientific computation, even if the command launches chemistry software."
            ),
        }
        for event in selected
    ]
    if len(events) > len(selected):
        values.append({"omitted_native_events": len(events) - len(selected)})
    return values


def _submission_artifacts(workspace: Path) -> list[dict[str, str]]:
    allowed_suffixes = {
        ".csv", ".ipynb", ".jl", ".json", ".jsonl", ".md", ".py", ".r",
        ".sh", ".tsv", ".txt", ".yaml", ".yml",
    }
    values: list[dict[str, str]] = []
    total = 0
    for root_name in ("report", "outputs", "code"):
        root = workspace / root_name
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.casefold() not in allowed_suffixes:
                continue
            relative = path.relative_to(workspace).as_posix()
            if relative == "report/report.md" or path.stat().st_size > 100_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            remaining = 250_000 - total
            if remaining <= 0:
                return values
            content = text[: min(50_000, remaining)]
            values.append({"path": relative, "content": content})
            total += len(content)
            if len(values) >= 40:
                return values
    return values


def score_workspace(
    workspace: str | Path,
    *,
    judge_call: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    workspace = Path(workspace).resolve()
    meta_path = workspace / "_meta.json"
    if not meta_path.is_file():
        return {"error": "Run metadata not found"}
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    paper_id = str(meta.get("paper_id") or "")
    task_type = str(meta.get("task_type") or "")
    if not paper_id or not task_type:
        return {"error": "Run metadata missing paper_id or task_type"}
    report_path = workspace / "report" / "report.md"
    if not report_path.is_file() or not report_path.read_text(encoding="utf-8").strip():
        return {"error": "No non-empty report/report.md found"}

    try:
        package = load_task_package(paper_id=paper_id, task_type=task_type)
        runtime_evaluation = load_runtime_evaluation(
            paper_id=paper_id, task_type=task_type
        )
    except (EvaluatorAdapterError, FileNotFoundError, ValueError) as exc:
        return {
            "error": f"Evaluator contract unavailable: {type(exc).__name__}: {exc}",
            "paper_id": paper_id,
            "task_type": task_type,
        }
    truth = runtime_evaluation.ground_truth
    report = report_path.read_text(encoding="utf-8", errors="replace")
    try:
        events = load_tool_trace(workspace, strict=True)
    except ValueError as exc:
        return {"error": str(exc), "paper_id": paper_id, "task_type": task_type}
    canonical_trace = canonical_tool_trace_metadata(workspace)
    native_events = load_native_agent_trace(workspace)
    actual_calls = normalized_tool_calls(events)
    evaluation_mode = truth.get("evaluation_mode", "binary")
    score_max = int(
        truth.get("score_max")
        or (100 if evaluation_mode in {"rubric_100", "dual_axis_100"} else 1)
    )
    metrics = process_metrics(events, workspace=workspace)
    metrics.update(
        {
            "canonical_tool_trace": canonical_trace,
            "native_execution_event_count": len(native_events),
            "successful_native_events": sum(
                event.get("status") == "success" for event in native_events
            ),
            "failed_native_events": sum(
                event.get("status") != "success" for event in native_events
            ),
            "native_runtime_seconds": round(
                sum(
                    float(event.get("duration_seconds", 0) or 0)
                    for event in native_events
                ),
                6,
            ),
            "native_tools_used": [event.get("tool") for event in native_events],
        }
    )
    if evaluation_mode in {"rubric_100", "dual_axis_100"}:
        evaluation_profile = str(truth.get("evaluation_profile") or "").strip()
        prompt = RUBRIC_JUDGE_USER_TEMPLATE.format(
            query=meta.get("query") or meta.get("task") or f"{task_type}/{paper_id}",
            agent_visible_protocol=json.dumps(
                {
                    "scientific_mode": meta.get("scientific_mode", ""),
                    "scientific_mode_description": meta.get(
                        "scientific_mode_description", ""
                    ),
                    "scientific_requirements": meta.get(
                        "scientific_requirements", []
                    ),
                    "required_deliverables": meta.get(
                        "required_deliverables", []
                    ),
                    "required_deliverable_status": meta.get(
                        "required_deliverable_status", []
                    ),
                },
                indent=2,
                ensure_ascii=False,
            ),
            expected_result=json.dumps(
                truth.get("expected_result", ""), indent=2, ensure_ascii=False
            ),
            evaluation_profile=evaluation_profile or "unspecified",
            reference_conclusion_gate_policy=json.dumps(
                truth.get("reference_conclusion_gate_policy", {}),
                indent=2,
                ensure_ascii=False,
            ),
            reference_evidence=json.dumps(
                truth.get("reference_evidence"), indent=2, ensure_ascii=False
            ),
            scoring_rubric=json.dumps(
                truth.get("scoring_rubric", []), indent=2, ensure_ascii=False
            ),
            scientific_conclusion_rubric=json.dumps(
                truth.get("scientific_conclusion_rubric", []),
                indent=2,
                ensure_ascii=False,
            ),
            dual_axis_scoring_policy=json.dumps(
                truth.get("dual_axis_scoring_policy", {}),
                indent=2,
                ensure_ascii=False,
            ),
            critical_failures=json.dumps(
                truth.get("critical_failures", []), indent=2, ensure_ascii=False
            ),
            judge_instructions=truth.get("judge_instructions", ""),
            managed_computation_policy=json.dumps(
                truth.get("managed_computation_policy", {}), indent=2, ensure_ascii=False
            ),
            evidence_gate_policy=json.dumps(
                truth.get("evidence_gate_policy", {}), indent=2, ensure_ascii=False
            ),
            process_metrics=json.dumps(metrics, indent=2, ensure_ascii=False),
            actual_tool_events=json.dumps(
                _tool_events_for_judge(events), indent=2, ensure_ascii=False
            ),
            native_execution_events=json.dumps(
                _native_events_for_judge(native_events), indent=2, ensure_ascii=False
            ),
            actual_report=report,
            submission_artifacts=json.dumps(
                _submission_artifacts(workspace), indent=2, ensure_ascii=False
            ),
        )
        system_prompt = (
            DUAL_AXIS_JUDGE_SYSTEM_PROMPT
            if evaluation_mode == "dual_axis_100"
            else RUBRIC_JUDGE_SYSTEM_PROMPT
        )
        if (
            evaluation_mode != "dual_axis_100"
            and evaluation_profile == "autonomous_discovery"
        ):
            conclusion_policy = truth.get("reference_conclusion_gate_policy", {})
            if conclusion_policy.get("required") is True:
                system_prompt += STRICT_AUTONOMOUS_DISCOVERY_JUDGE_PROMPT
            else:
                system_prompt += AUTONOMOUS_DISCOVERY_JUDGE_PROMPT
        elif (
            evaluation_mode != "dual_axis_100"
            and evaluation_profile == "paper_reproduction"
        ):
            system_prompt += PAPER_REPRODUCTION_JUDGE_PROMPT
    else:
        prompt = JUDGE_USER_TEMPLATE.format(
            query=meta.get("query") or meta.get("task") or f"{task_type}/{paper_id}",
            expected_tool_calls=json.dumps(
                truth.get("expected_tool_calls", []), indent=2, ensure_ascii=False
            ),
            expected_result=json.dumps(
                truth.get("expected_result", ""), indent=2, ensure_ascii=False
            ),
            actual_tool_calls=json.dumps(actual_calls, indent=2, ensure_ascii=False),
            actual_report=report,
        )
        system_prompt = JUDGE_SYSTEM_PROMPT
    run_id = str(meta.get("run_id") or workspace.name)
    progress_enabled = bool(meta.get("live_progress", False))
    progress_console = bool(meta.get("progress_console", False))
    try:
        progress_max_chars = max(80, int(meta.get("progress_max_chars", 600)))
    except (TypeError, ValueError):
        progress_max_chars = 600
    judge_model = (
        getattr(judge_call, "__name__", "injected_judge")
        if judge_call is not None
        else os.environ.get("JUDGE_MODEL_NAME", JUDGE_MODEL_NAME)
    )
    append_progress_event(
        workspace,
        run_id,
        "JUDGE_INPUT",
        enabled=progress_enabled,
        console=progress_console,
        max_chars=progress_max_chars,
        model=judge_model,
        system=system_prompt,
        prompt=prompt,
    )
    raw_verdict: dict[str, Any] = {}
    try:
        raw_verdict = (
            judge_call(prompt)
            if judge_call is not None
            else _default_judge_call(
                prompt, system_prompt=system_prompt, score_max=score_max
            )
        )
        append_progress_event(
            workspace,
            run_id,
            "JUDGE_OUTPUT",
            enabled=progress_enabled,
            console=progress_console,
            max_chars=progress_max_chars,
            model=raw_verdict.get("_judge_model") or judge_model,
            verdict=raw_verdict,
        )
        if evaluation_mode == "dual_axis_100":
            process_rubric = _normalize_rubric_verdict(
                {
                    "criteria": raw_verdict.get("process_criteria"),
                    "score": raw_verdict.get("research_process_score"),
                },
                truth.get("scoring_rubric", []),
                score_max=100,
                allow_total_fallback=False,
            )
            conclusion_rubric = _normalize_scientific_conclusions(
                raw_verdict,
                truth.get("scientific_conclusion_rubric", []),
            )
            research_process_score = float(process_rubric["score"])
            scientific_conclusion_score = float(conclusion_rubric["score"])
            criteria = process_rubric["criteria"]
            scientific_conclusions = conclusion_rubric["criteria"]
            consistency_warnings = [
                *process_rubric["warnings"],
                *conclusion_rubric["warnings"],
            ]
            submission_validity = str(
                raw_verdict.get("submission_validity") or "valid"
            ).strip().casefold()
            if submission_validity not in {
                "valid",
                "invalid_submission",
                "not_scorable_objective",
            }:
                consistency_warnings.append(
                    "Judge returned an invalid submission_validity; treated it as valid."
                )
                submission_validity = "valid"
            if submission_validity == "invalid_submission":
                score = 0.0
            elif submission_validity == "not_scorable_objective":
                score = None
            else:
                score = round(
                    scientific_conclusion_score * research_process_score / 100.0,
                    2,
                )
            score_cap = None
            score_cap_reason = None
            evidence_gate_cap = None
            evidence_gate_cap_reason = None
            evidence_gate_failures = []
            conclusion_cap = None
            conclusion_cap_reason = None
            reference_conclusion_status = "multi_claim_scored"
            structured_mismatches = []
            applied_score_cap = None
        elif evaluation_mode == "rubric_100":
            normalized_rubric = _normalize_rubric_verdict(
                raw_verdict,
                truth.get("scoring_rubric", []),
                score_max=score_max,
            )
            score = normalized_rubric["score"]
            criteria = normalized_rubric["criteria"]
            consistency_warnings = normalized_rubric["warnings"]
            score_cap, score_cap_reason = _managed_computation_cap(
                truth.get("managed_computation_policy", {}), metrics
            )
            (
                evidence_gate_cap,
                evidence_gate_cap_reason,
                evidence_gate_failures,
                evidence_gate_warnings,
            ) = _evidence_gate_cap(
                truth.get("evidence_gate_policy", {}),
                raw_verdict.get("evidence_gate_failures"),
            )
            consistency_warnings.extend(evidence_gate_warnings)
            conclusion_policy = truth.get(
                "reference_conclusion_gate_policy", {}
            )
            structured_mismatches = _structured_conclusion_mismatches(
                workspace, conclusion_policy
            )
            (
                conclusion_cap,
                conclusion_cap_reason,
                reference_conclusion_status,
                conclusion_criterion_id,
                conclusion_criterion_cap,
                conclusion_warnings,
            ) = _reference_conclusion_cap(
                conclusion_policy,
                raw_verdict.get("reference_conclusion_status"),
                structured_mismatches=structured_mismatches,
            )
            consistency_warnings.extend(conclusion_warnings)
            criteria, conclusion_criterion_limited = _apply_criterion_score_limit(
                criteria,
                criterion_id=conclusion_criterion_id,
                maximum_score=conclusion_criterion_cap,
            )
            if conclusion_criterion_limited:
                score = round(
                    sum(float(item.get("score", 0)) for item in criteria), 2
                )
                consistency_warnings.append(
                    "Limited reference-conclusion criterion credit according to the "
                    f"{reference_conclusion_status} conclusion status."
                )
            applicable_caps = [
                value
                for value in (score_cap, evidence_gate_cap, conclusion_cap)
                if value is not None
            ]
            applied_score_cap = min(applicable_caps) if applicable_caps else None
            score, criteria = _apply_rubric_score_cap(
                float(score), criteria, cap=applied_score_cap
            )
            if score_cap_reason and score_cap is not None:
                consistency_warnings.append(
                    f"Applied managed-computation score cap {score_cap:g}: {score_cap_reason}"
                )
            if evidence_gate_cap_reason and evidence_gate_cap is not None:
                consistency_warnings.append(
                    f"Applied evidence-gate score cap {evidence_gate_cap:g}: "
                    f"{evidence_gate_cap_reason}"
                )
            if conclusion_cap_reason and conclusion_cap is not None:
                consistency_warnings.append(
                    f"Applied reference-conclusion score cap {conclusion_cap:g}: "
                    f"{conclusion_cap_reason}"
                )
            research_process_score = None
            scientific_conclusion_score = None
            scientific_conclusions = []
            submission_validity = "valid"
        else:
            raw_score = float(raw_verdict.get("score", 0))
            score = 1 if raw_score == 1 else 0
            criteria = []
            consistency_warnings = []
            score_cap = None
            score_cap_reason = None
            evidence_gate_cap = None
            evidence_gate_cap_reason = None
            evidence_gate_failures = []
            conclusion_cap = None
            conclusion_cap_reason = None
            reference_conclusion_status = "not_applicable"
            structured_mismatches = []
            applied_score_cap = None
            research_process_score = None
            scientific_conclusion_score = None
            scientific_conclusions = []
            submission_validity = "valid"
        verdict = {
            "score": score,
            "score_max": score_max,
            "criteria": criteria,
            "research_process_score": research_process_score,
            "scientific_conclusion_score": scientific_conclusion_score,
            "scientific_conclusions": scientific_conclusions,
            "submission_validity": submission_validity,
            "critical_failures": raw_verdict.get("critical_failures", []),
            "evidence_gate_failures": evidence_gate_failures,
            "objective_issue_flags": raw_verdict.get("objective_issue_flags", []),
            "judge_consistency_warnings": consistency_warnings,
            "rationale": str(raw_verdict.get("rationale", "")),
            "parse_error": None,
            "managed_computation_score_cap": score_cap,
            "managed_computation_score_cap_reason": score_cap_reason,
            "evidence_gate_score_cap": evidence_gate_cap,
            "evidence_gate_score_cap_reason": evidence_gate_cap_reason,
            "reference_conclusion_status": reference_conclusion_status,
            "reference_conclusion_score_cap": conclusion_cap,
            "reference_conclusion_score_cap_reason": conclusion_cap_reason,
            "structured_conclusion_mismatches": structured_mismatches,
            "applied_score_cap": applied_score_cap,
        }
    except Exception as exc:
        verdict = {
            "score": None,
            "score_max": score_max,
            "criteria": [],
            "research_process_score": None,
            "scientific_conclusion_score": None,
            "scientific_conclusions": [],
            "submission_validity": "unknown",
            "critical_failures": [],
            "evidence_gate_failures": [],
            "objective_issue_flags": [],
            "judge_consistency_warnings": [],
            "rationale": f"Judge evaluation failed: {exc}",
            "parse_error": f"{type(exc).__name__}: {exc}",
            "managed_computation_score_cap": None,
            "managed_computation_score_cap_reason": None,
            "evidence_gate_score_cap": None,
            "evidence_gate_score_cap_reason": None,
            "reference_conclusion_status": "unknown",
            "reference_conclusion_score_cap": None,
            "reference_conclusion_score_cap_reason": None,
            "structured_conclusion_mismatches": [],
            "applied_score_cap": None,
        }
        append_progress_event(
            workspace,
            run_id,
            "JUDGE_ERROR",
            enabled=progress_enabled,
            console=progress_console,
            max_chars=progress_max_chars,
            model=judge_model,
            error=f"{type(exc).__name__}: {exc}",
        )

    result = {
        "run_id": meta.get("run_id", workspace.name),
        "paper_id": paper_id,
        "agent_key": meta.get("agent_key", ""),
        "agent_name": meta.get("agent_name", ""),
        "tool_discovery_mode": meta.get("tool_discovery_mode", "legacy_full"),
        "query": meta.get("query", ""),
        "expected_tool_calls": truth.get("expected_tool_calls", []),
        "actual_tool_calls": actual_calls,
        "evaluation_mode": evaluation_mode,
        "evaluation_profile": truth.get("evaluation_profile", ""),
        "task_type": runtime_evaluation.task_type,
        "task_package_content_sha256": runtime_evaluation.package_content_sha256,
        "evaluator_adapter_id": runtime_evaluation.adapter_id,
        "evaluation_policy_id": runtime_evaluation.policy_id,
        "score": verdict["score"],
        "score_max": verdict["score_max"],
        "normalized_score": (
            None
            if verdict["score"] is None
            else round(float(verdict["score"]) / float(verdict["score_max"]), 6)
        ),
        "criteria": verdict["criteria"],
        "research_process_score": verdict["research_process_score"],
        "scientific_conclusion_score": verdict["scientific_conclusion_score"],
        "scientific_conclusions": verdict["scientific_conclusions"],
        "dual_axis_scoring_policy": truth.get("dual_axis_scoring_policy", {}),
        "submission_validity": verdict["submission_validity"],
        "critical_failures": verdict["critical_failures"],
        "evidence_gate_policy": truth.get("evidence_gate_policy", {}),
        "evidence_gate_failures": verdict["evidence_gate_failures"],
        "objective_issue_flags": verdict["objective_issue_flags"],
        "judge_consistency_warnings": verdict["judge_consistency_warnings"],
        "managed_computation_policy": truth.get("managed_computation_policy", {}),
        "managed_computation_score_cap": verdict["managed_computation_score_cap"],
        "managed_computation_score_cap_reason": verdict[
            "managed_computation_score_cap_reason"
        ],
        "evidence_gate_score_cap": verdict["evidence_gate_score_cap"],
        "evidence_gate_score_cap_reason": verdict[
            "evidence_gate_score_cap_reason"
        ],
        "reference_conclusion_gate_policy": truth.get(
            "reference_conclusion_gate_policy", {}
        ),
        "reference_conclusion_status": verdict["reference_conclusion_status"],
        "reference_conclusion_score_cap": verdict[
            "reference_conclusion_score_cap"
        ],
        "reference_conclusion_score_cap_reason": verdict[
            "reference_conclusion_score_cap_reason"
        ],
        "structured_conclusion_mismatches": verdict[
            "structured_conclusion_mismatches"
        ],
        "applied_score_cap": verdict["applied_score_cap"],
        "rationale": verdict["rationale"],
        "parse_error": verdict["parse_error"],
        "process_metrics": metrics,
        "judge_model": str(raw_verdict.get("_judge_model", "")),
        "judge_usage": raw_verdict.get("_judge_usage"),
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }
    if verdict["parse_error"]:
        result["error"] = verdict["parse_error"]
    score_path = workspace / "_score.json"
    history_path = workspace / "_score_history.jsonl"
    if score_path.is_file() and not history_path.exists():
        try:
            previous = json.loads(score_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            previous = None
        if isinstance(previous, dict):
            previous = {
                **previous,
                "history_source": "pre_history_score_snapshot",
                "history_recorded_at": datetime.now(timezone.utc).isoformat(),
            }
            with history_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(previous, ensure_ascii=False) + "\n")
    score_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    history_record = {**result, "history_source": "judge_call"}
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(history_record, ensure_ascii=False) + "\n")
    write_workspace_results(workspace)
    append_progress_event(
        workspace,
        run_id,
        "SCORE_RESULT",
        enabled=progress_enabled,
        console=progress_console,
        max_chars=progress_max_chars,
        score=result.get("score"),
        score_max=result.get("score_max"),
        normalized_score=result.get("normalized_score"),
        error=result.get("error"),
    )
    return result


def score_run(run_id: str) -> dict[str, Any]:
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return {"error": "Workspace not found"}
    return score_workspace(workspace)

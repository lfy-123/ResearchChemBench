"""LLM judges for ChemGraph-style answers and rubric-based scientific tasks."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .config import JUDGE_API_BASE, JUDGE_API_KEY, JUDGE_MODEL_NAME
from .trace import (
    load_native_agent_trace,
    load_tool_trace,
    normalized_tool_calls,
    process_metrics,
)
from .utils import get_run_workspace, load_ground_truth


JUDGE_SYSTEM_PROMPT = """You are an expert evaluator for a computational chemistry agent.

The tested agent receives a natural-language chemistry task and autonomously calls tools for molecule lookup, coordinate generation, ASE simulations, result extraction, and arithmetic.

Decide whether the agent is correct by comparing BOTH its observable tool-call sequence and its final report with the expected ground truth.

Rules:
- Return score 1 only when the key chemistry result is correct and the logical tool dependency chain is substantially correct.
- Numeric values should match within 5 percent relative tolerance unless the expected value is exactly zero.
- Units, calculator type, model/method, driver, temperature, molecule identity, SMILES, and reaction stoichiometry are key details.
- Optional defaults, harmless extra calls, file naming differences, formatting, and rounding are acceptable.
- A missing tool call may be acceptable only when the final answer is correct and the observable process still preserves the necessary dependency chain.
- Return score 0 for missing/incorrect key results, fabricated values, wrong calculators or drivers, wrong chemical identities, or failed computations without a meaningful answer.

Respond with one JSON object only: {"score": 0 or 1, "rationale": "brief explanation"}.
"""

RUBRIC_JUDGE_SYSTEM_PROMPT = """You are an expert evaluator of an autonomous computational-chemistry investigation.

Score the submission against the supplied 100-point rubric. Evaluate scientific validity, evidence provenance, uncertainty handling, and the observable computation trace. Do not require exact tool names or a unique call order when an alternative process preserves the scientific dependencies. The benchmark has three valid execution layers: predefined Chemistry MCP Actions, native software/shell execution, and Agent-authored analysis code. A result supported by observable native commands, code, outputs, and submitted artifacts is not fabricated merely because an MCP call failed. Distinguish an agent mistake from an objective framework, unavailable-data, or backend failure. Never reward a paper value that appears without supporting evidence from the supplied data or an independently documented calculation.

Rules:
- Award each criterion no more than its declared maximum and make criterion scores sum to the total score.
- Apply critical failures only when the trace/report actually demonstrates them.
- Published rounded targets and benchmark recomputations may differ; use the reference evidence and tolerances stated in the rubric.
- Failed calls are not automatically wrong: judge whether the agent diagnosed them, preserved provenance, and reached a defensible conclusion.
- A scientifically cautious statement that the supplied evidence is insufficient is better than a fabricated precise number.
- objective_issue_flags must identify only failures outside the agent's scientific choices, such as malformed inputs, framework exceptions, backend adapter defects, missing declared files, or infrastructure timeouts.
- Do not mark an objective issue merely because a call has status invalid_request, failed, or backend_exception. Classify the cause shown by the request and error message.
- These are agent-side mistakes, not objective issues, when the relevant requirement was exposed in the tool schema or task protocol: omitted required fields; an explicitly chosen array/time/resource limit that is too small; a path outside the workspace; a nonexistent path invented by the agent; malformed tool-call JSON produced by the model; wrong native CLI syntax; wrong charge/multiplicity formatting; or an incompatible scientific method/input selected by the agent.
- A backend exception is an objective issue only when the observable trace supports that a schema-valid, scientifically compatible request failed because of adapter/runtime behavior rather than an agent-selected input or limit. A missing declared file means a file promised by the benchmark is absent, not that the agent referenced the wrong location.
- Recovery on a later call does not convert the earlier agent-side invalid request into a framework issue. Conversely, an infrastructure or adapter defect may still be flagged even when the agent successfully works around it.
- Before calling any conclusion correct, cross-check it against the explicit fields in the reference answer. A coherent narrative is not evidence that a conflicting mechanistic assignment is correct.
- Compare rate-determining, selectivity-determining, and irreversible steps separately when the reference distinguishes them. Do not state that the Agent separated these roles if its report conflates them or assigns any role to a different elementary step than the reference.
- Keep criterion rationales internally consistent with critical_failures and the total: do not refer to an applied critical failure that is absent from critical_failures, and do not praise a conclusion that another criterion identifies as contrary to the reference.

Respond with one JSON object only:
{"score": 0-100, "score_max": 100, "criteria": [{"id": "...", "score": 0, "max_score": 0, "rationale": "..."}], "critical_failures": [], "objective_issue_flags": [], "rationale": "concise overall assessment"}.
"""

JUDGE_USER_TEMPLATE = """## Query
{query}

## Expected tool calls
{expected_tool_calls}

## Expected result
{expected_result}

## Agent tool calls
{actual_tool_calls}

## Agent final report
{actual_report}
"""

RUBRIC_JUDGE_USER_TEMPLATE = """## Scientific task
{query}

## Reference answer and numerical evidence
{expected_result}

## Additional reference evidence
{reference_evidence}

## Scoring rubric
{scoring_rubric}

## Critical failures
{critical_failures}

## Task-specific judge instructions
{judge_instructions}

## Observable process metrics
{process_metrics}

## Observable tool events, including failures
{actual_tool_events}

## Observable native shell, file, and Agent-authored code events
{native_execution_events}

## Agent final report
{actual_report}

## Additional submitted text/JSON/CSV artifacts
{submission_artifacts}
"""


def _parse_judge_json(text: str, *, score_max: int = 1) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.DOTALL)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise
        value = json.loads(match.group(0))
    raw_score = float(value.get("score", 0))
    if score_max == 1:
        score: int | float = 1 if raw_score == 1 else 0
    else:
        score = round(min(float(score_max), max(0.0, raw_score)), 2)
    return {
        "score": score,
        "score_max": score_max,
        "criteria": value.get("criteria", []),
        "critical_failures": value.get("critical_failures", []),
        "objective_issue_flags": value.get("objective_issue_flags", []),
        "rationale": str(value.get("rationale", "")),
    }


def _normalize_rubric_verdict(
    verdict: dict[str, Any],
    rubric: list[dict[str, Any]],
    *,
    score_max: int,
) -> dict[str, Any]:
    """Clamp criterion scores and derive a reproducible total when supplied."""

    warnings: list[str] = []
    reported = verdict.get("criteria")
    if not isinstance(reported, list) or not reported:
        raw_score = float(verdict.get("score", 0))
        warnings.append("Judge omitted criterion-level scores; retained its clamped total.")
        return {
            "score": round(min(float(score_max), max(0.0, raw_score)), 2),
            "criteria": [],
            "warnings": warnings,
        }

    by_id: dict[str, dict[str, Any]] = {}
    for item in reported:
        if not isinstance(item, dict):
            warnings.append("Ignored a non-object rubric criterion from the judge.")
            continue
        criterion_id = str(item.get("id") or "").strip()
        if not criterion_id:
            warnings.append("Ignored a judge criterion without an id.")
            continue
        if criterion_id in by_id:
            warnings.append(f"Ignored duplicate judge criterion {criterion_id!r}.")
            continue
        by_id[criterion_id] = item

    normalized: list[dict[str, Any]] = []
    for specification in rubric:
        criterion_id = str(specification["id"])
        maximum = float(specification["max_score"])
        item = by_id.get(criterion_id)
        if item is None:
            score = 0.0
            rationale = "Judge omitted this required criterion."
            warnings.append(f"Judge omitted required criterion {criterion_id!r}.")
        else:
            try:
                raw_score = float(item.get("score", 0))
            except (TypeError, ValueError):
                raw_score = 0.0
                warnings.append(f"Judge returned a non-numeric score for {criterion_id!r}.")
            score = min(maximum, max(0.0, raw_score))
            rationale = str(item.get("rationale", ""))
            if abs(score - raw_score) > 1e-9:
                warnings.append(f"Clamped out-of-range score for criterion {criterion_id!r}.")
        normalized.append(
            {
                "id": criterion_id,
                "score": round(score, 2),
                "max_score": maximum,
                "rationale": rationale,
            }
        )
    total = round(sum(float(item["score"]) for item in normalized), 2)
    try:
        claimed_total = float(verdict.get("score", total))
    except (TypeError, ValueError):
        claimed_total = total
        warnings.append("Judge returned a non-numeric total score.")
    if abs(claimed_total - total) > 0.01:
        warnings.append(
            f"Replaced inconsistent judge total {claimed_total:g} with criterion sum {total:g}."
        )
    unknown_ids = sorted(set(by_id) - {str(item["id"]) for item in rubric})
    if unknown_ids:
        warnings.append(f"Ignored unknown judge criteria: {', '.join(unknown_ids)}.")
    return {"score": total, "criteria": normalized, "warnings": warnings}


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
            "tool": event.get("tool"),
            "status": event.get("status"),
            "duration_seconds": event.get("duration_seconds"),
            "arguments": _compact_value(event.get("arguments", {})),
            "result_preview": _compact_value(event.get("result_preview", "")),
            "exit_code": event.get("exit_code"),
            "error": _compact_value(event.get("error")),
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
    task_id = meta.get("task_id", "")
    if not task_id:
        return {"error": "Run metadata missing task_id"}
    report_path = workspace / "report" / "report.md"
    if not report_path.is_file() or not report_path.read_text(encoding="utf-8").strip():
        return {"error": "No non-empty report/report.md found"}

    truth = load_ground_truth(task_id)
    report = report_path.read_text(encoding="utf-8", errors="replace")
    events = load_tool_trace(workspace)
    native_events = load_native_agent_trace(workspace)
    actual_calls = normalized_tool_calls(events)
    evaluation_mode = truth.get("evaluation_mode", "binary")
    score_max = int(truth.get("score_max") or (100 if evaluation_mode == "rubric_100" else 1))
    metrics = process_metrics(events)
    metrics.update(
        {
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
    if evaluation_mode == "rubric_100":
        prompt = RUBRIC_JUDGE_USER_TEMPLATE.format(
            query=meta.get("query") or meta.get("task") or task_id,
            expected_result=json.dumps(
                truth.get("expected_result", ""), indent=2, ensure_ascii=False
            ),
            reference_evidence=json.dumps(
                truth.get("reference_evidence"), indent=2, ensure_ascii=False
            ),
            scoring_rubric=json.dumps(
                truth.get("scoring_rubric", []), indent=2, ensure_ascii=False
            ),
            critical_failures=json.dumps(
                truth.get("critical_failures", []), indent=2, ensure_ascii=False
            ),
            judge_instructions=truth.get("judge_instructions", ""),
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
        system_prompt = RUBRIC_JUDGE_SYSTEM_PROMPT
    else:
        prompt = JUDGE_USER_TEMPLATE.format(
            query=meta.get("query") or meta.get("task") or task_id,
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
    raw_verdict: dict[str, Any] = {}
    try:
        raw_verdict = (
            judge_call(prompt)
            if judge_call is not None
            else _default_judge_call(
                prompt, system_prompt=system_prompt, score_max=score_max
            )
        )
        if evaluation_mode == "rubric_100":
            normalized_rubric = _normalize_rubric_verdict(
                raw_verdict,
                truth.get("scoring_rubric", []),
                score_max=score_max,
            )
            score = normalized_rubric["score"]
            criteria = normalized_rubric["criteria"]
            consistency_warnings = normalized_rubric["warnings"]
        else:
            raw_score = float(raw_verdict.get("score", 0))
            score = 1 if raw_score == 1 else 0
            criteria = []
            consistency_warnings = []
        verdict = {
            "score": score,
            "score_max": score_max,
            "criteria": criteria,
            "critical_failures": raw_verdict.get("critical_failures", []),
            "objective_issue_flags": raw_verdict.get("objective_issue_flags", []),
            "judge_consistency_warnings": consistency_warnings,
            "rationale": str(raw_verdict.get("rationale", "")),
            "parse_error": None,
        }
    except Exception as exc:
        verdict = {
            "score": None,
            "score_max": score_max,
            "criteria": [],
            "critical_failures": [],
            "objective_issue_flags": [],
            "judge_consistency_warnings": [],
            "rationale": f"Judge evaluation failed: {exc}",
            "parse_error": f"{type(exc).__name__}: {exc}",
        }

    result = {
        "run_id": meta.get("run_id", workspace.name),
        "task_id": task_id,
        "agent_key": meta.get("agent_key", ""),
        "agent_name": meta.get("agent_name", ""),
        "query": meta.get("query", ""),
        "expected_tool_calls": truth.get("expected_tool_calls", []),
        "actual_tool_calls": actual_calls,
        "expected_result": truth.get("expected_result", ""),
        "evaluation_mode": evaluation_mode,
        "score": verdict["score"],
        "score_max": verdict["score_max"],
        "normalized_score": (
            None
            if verdict["score"] is None
            else round(float(verdict["score"]) / float(verdict["score_max"]), 6)
        ),
        "criteria": verdict["criteria"],
        "critical_failures": verdict["critical_failures"],
        "objective_issue_flags": verdict["objective_issue_flags"],
        "judge_consistency_warnings": verdict["judge_consistency_warnings"],
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
    return result


def score_run(run_id: str) -> dict[str, Any]:
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return {"error": "Workspace not found"}
    return score_workspace(workspace)

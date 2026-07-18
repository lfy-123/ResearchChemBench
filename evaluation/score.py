"""ChemGraph-style LLM judge for final answers and observable tool calls."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Callable

from .config import JUDGE_API_BASE, JUDGE_API_KEY, JUDGE_MODEL_NAME
from .trace import load_tool_trace, normalized_tool_calls, process_metrics
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


def _parse_judge_json(text: str) -> dict[str, Any]:
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
    score = int(value.get("score", 0))
    return {"score": 1 if score == 1 else 0, "rationale": str(value.get("rationale", ""))}


def _default_judge_call(prompt: str) -> dict[str, Any]:
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
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return _parse_judge_json(response.choices[0].message.content or "")


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
    actual_calls = normalized_tool_calls(events)
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
    caller = judge_call or _default_judge_call
    try:
        verdict = caller(prompt)
        verdict = {
            "score": 1 if int(verdict.get("score", 0)) == 1 else 0,
            "rationale": str(verdict.get("rationale", "")),
            "parse_error": None,
        }
    except Exception as exc:
        verdict = {
            "score": None,
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
        "score": verdict["score"],
        "rationale": verdict["rationale"],
        "parse_error": verdict["parse_error"],
        "process_metrics": process_metrics(events),
    }
    if verdict["parse_error"]:
        result["error"] = verdict["parse_error"]
    (workspace / "_score.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result


def score_run(run_id: str) -> dict[str, Any]:
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return {"error": "Workspace not found"}
    return score_workspace(workspace)

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from src.core.logging import log_progress
from src.core.models import (
    TASK_TYPES,
    normalize_task_type,
    selected_task_type,
    validate_scientific_record,
)
from src.curation.llm_client import call_json_chat

SELECTION_PROMPT = """You select exactly one ResearchChemBench task type for one computational-chemistry study.
Choose the task that is most scientifically representative, executable with the available inputs and toolbox,
and objectively scoreable from the richest source evidence. Do not prefer openness or difficulty by default.

Task types:
- paper_reproduction: methods, parameters, workflow order, and real starting inputs are the richest evidence;
  the route is disclosed and numerical results/conclusions are hidden.
- conclusion_guided_reconstruction: a clear paper conclusion and supporting evidence are rich enough to disclose
  the target claim while hiding the route; more than one scientifically valid verification route can exist.
- autonomous_research: starting inputs and observations are sufficient, the route and conclusion can both be
  hidden, and finite-budget calculations can discriminate hypotheses or recover a defensible finding.
- mechanistic_rule_discovery: multiple comparable systems and descriptor/outcome data support abstraction of a
  rule, with at least one system or subset suitable for held-out prediction.

Evaluate method_parameter_richness, materialized_input_richness, conclusion_richness, quantitative_result_richness,
competing_hypothesis_richness, multi_system_richness, heldout_prediction_feasibility, toolbox_coverage,
runtime_feasibility, and evaluator_constructability. Return JSON only with:
selected_task_type, selection_reason, rejected_task_types, task_scores (0-100), decisive_evidence, missing_information.
"""


def select_task_types(
    records: list[dict[str, Any]], config: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    config = config or {}
    output: list[dict[str, Any]] = []
    total = len(records)
    for index, record in enumerate(records, start=1):
        updated = dict(record)
        existing = selected_task_type(record)
        if existing and record.get("selection_reason"):
            result = _normalize_selection(
                {
                    "selected_task_type": existing,
                    "selection_reason": record["selection_reason"],
                    "rejected_task_types": record.get("rejected_task_types", []),
                    "task_scores": record.get("task_selection_scores", {}),
                    "decisive_evidence": record.get("task_selection_evidence", []),
                    "missing_information": record.get("task_selection_missing", []),
                },
                record,
            )
            source = "curator_supplied"
        else:
            try:
                result, source = _select_one(record, config)
            except Exception as exc:
                if not config.get("allow_deterministic_fallback", True):
                    updated["task_selection"] = {
                        "status": "failed",
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                    output.append(updated)
                    log_progress(
                        "stage_12_task_selection",
                        index,
                        total,
                        record.get("paper_id", str(index)),
                        status="failed",
                    )
                    continue
                result = deterministic_selection(record)
                source = f"deterministic_fallback_after_{type(exc).__name__}"
        updated.update(
            {
                "selected_task_type": result["selected_task_type"],
                "selection_reason": result["selection_reason"],
                "rejected_task_types": result["rejected_task_types"],
                "task_selection_scores": result["task_scores"],
                "task_selection_evidence": result["decisive_evidence"],
                "task_selection_missing": result["missing_information"],
                "task_selection": {
                    "status": "complete",
                    "source": source,
                    **({"llm_call": result["llm_call"]} if result.get("llm_call") else {}),
                },
            }
        )
        updated.pop("task_modes", None)
        errors = validate_scientific_record(updated)
        updated["schema_validation"] = {"passed": not errors, "errors": errors}
        output.append(updated)
        log_progress(
            "stage_12_task_selection",
            index,
            total,
            record.get("paper_id", str(index)),
            status=(updated.get("task_selection") or {}).get("status"),
        )
    return output


def selection_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    status = Counter(
        (item.get("task_selection") or {}).get("status", "missing") for item in records
    )
    selected = Counter(item.get("selected_task_type", "unselected") for item in records)
    sources = Counter(
        (item.get("task_selection") or {}).get("source", "unknown") for item in records
    )
    return {
        "records": len(records),
        "statuses": dict(status),
        "selected_task_types": dict(selected),
        "sources": dict(sources),
    }


def deterministic_selection(record: dict[str, Any]) -> dict[str, Any]:
    richness = record.get("information_richness") or {}
    preliminary = (
        (record.get("source_classification") or {}).get("task_suitability_scores")
        or (record.get("source_classification") or {}).get("constructability_scores")
        or {}
    )
    inputs = len(record.get("inputs", []))
    methods = len(record.get("methods", []))
    workflow = len(record.get("workflow", []))
    evidence = len(record.get("evidence", [])) + len(record.get("reference_results", []))
    hypotheses = len(record.get("hypotheses", []))
    systems = int(richness.get("comparable_system_count") or 0)
    scores = {
        "paper_reproduction": _bounded(
            preliminary.get("paper_reproduction", 0)
            + 5 * min(methods, 4)
            + 4 * min(workflow, 5)
            + 6 * min(inputs, 3)
        ),
        "conclusion_guided_reconstruction": _bounded(
            preliminary.get("conclusion_guided_reconstruction", 0)
            + 5 * min(evidence, 6)
            + 4 * min(inputs, 3)
            + 5 * min(hypotheses, 3)
        ),
        "autonomous_research": _bounded(
            preliminary.get("autonomous_research", 0)
            + 6 * min(inputs, 3)
            + 6 * min(hypotheses, 4)
            + 4 * min(evidence, 5)
        ),
        "mechanistic_rule_discovery": _bounded(
            preliminary.get("mechanistic_rule_discovery", 0)
            + 8 * min(systems, 5)
            + 4 * min(evidence, 5)
        ),
    }
    selected = max(TASK_TYPES, key=lambda item: (scores[item], -TASK_TYPES.index(item)))
    evidence_notes = [
        f"methods={methods}, workflow_steps={workflow}, materialized_inputs={inputs}",
        f"evidence_units={evidence}, competing_hypotheses={hypotheses}, comparable_systems={systems}",
    ]
    return _normalize_selection(
        {
            "selected_task_type": selected,
            "selection_reason": (
                f"Deterministic evidence-richness fallback selected {selected} because it had the highest "
                "combined constructability and source-information score."
            ),
            "rejected_task_types": [item for item in TASK_TYPES if item != selected],
            "task_scores": scores,
            "decisive_evidence": evidence_notes,
            "missing_information": [],
        },
        record,
    )


def _select_one(record: dict[str, Any], config: dict[str, Any]) -> tuple[dict[str, Any], str]:
    cache_dir = config.get("cache_dir")
    if cache_dir:
        path = Path(cache_dir).expanduser() / f"{record['paper_id']}.json"
        if path.is_file():
            cached = json.loads(path.read_text(encoding="utf-8"))
            normalized = _normalize_selection(cached, record)
            if cached.get("llm_call"):
                normalized["llm_call"] = cached["llm_call"]
            return normalized, "api_cache"
    offline_dir = config.get("offline_selection_dir")
    if offline_dir:
        path = Path(offline_dir).expanduser() / f"{record['paper_id']}.json"
        if path.is_file():
            return _normalize_selection(
                json.loads(path.read_text(encoding="utf-8")), record
            ), "offline_file"

    if not config.get("enabled", False):
        return deterministic_selection(record), "deterministic"

    api_key = config.get("api_key")
    if not api_key and config.get("api_key_env"):
        api_key = os.environ.get(config["api_key_env"])
    api_key = api_key or os.environ.get("RCB_LLM_API_KEY")
    if not api_key:
        raise ValueError("missing task-selection API key")
    model = str(config["model"])
    base_url = str(config.get("base_url", "https://api.openai.com/v1")).rstrip("/")
    value, metadata = call_json_chat(
        model=model,
        base_url=base_url,
        api_key=api_key,
        system_prompt=SELECTION_PROMPT,
        user_content=json.dumps(_selection_packet(record), ensure_ascii=False),
        timeout_seconds=float(config.get("timeout_seconds", 300)),
        max_tokens=config.get("max_tokens"),
        retries=int(config.get("retries", 2)),
        thinking=config.get("thinking"),
    )
    normalized = _normalize_selection(value, record)
    normalized["llm_call"] = metadata
    if cache_dir:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return normalized, f"api:{model}"


def _selection_packet(record: dict[str, Any]) -> dict[str, Any]:
    source_excerpt = ""
    for raw in (record.get("assets") or {}).get("text", []):
        path = Path(raw)
        if path.is_file():
            source_excerpt += path.read_text(encoding="utf-8", errors="replace")[:40_000]
            if len(source_excerpt) >= 40_000:
                break
    return {
        "paper_id": record.get("paper_id"),
        "paper": record.get("paper", {}),
        "central_problem": record.get("central_problem"),
        "inputs": record.get("inputs", []),
        "methods": record.get("methods", []),
        "workflow": record.get("workflow", []),
        "expected_outputs": record.get("expected_outputs", []),
        "reference_results": record.get("reference_results", []),
        "evidence": record.get("evidence", []),
        "hypotheses": record.get("hypotheses", []),
        "controls": record.get("controls", []),
        "information_richness": record.get("information_richness", {}),
        "source_classification": record.get("source_classification", {}),
        "toolbox_coverage": record.get("toolbox_coverage", {})
        or record.get("software_coverage", {}),
        "resource_limits": record.get("resource_limits", {}),
        "asset_availability": record.get("asset_availability", {}),
        "runtime": record.get("runtime", {}),
        "source_excerpt": source_excerpt[:40_000],
    }


def _normalize_selection(value: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    selected = normalize_task_type(value.get("selected_task_type"))
    if not selected:
        raise ValueError(f"invalid selected_task_type: {value.get('selected_task_type')!r}")
    scores = {}
    for task_type in TASK_TYPES:
        try:
            scores[task_type] = _bounded(float((value.get("task_scores") or {}).get(task_type, 0)))
        except (TypeError, ValueError):
            scores[task_type] = 0.0
    rejected = [
        normalized
        for item in value.get("rejected_task_types", [])
        if (normalized := normalize_task_type(item)) and normalized != selected
    ]
    rejected = list(dict.fromkeys(rejected + [item for item in TASK_TYPES if item != selected]))
    reason = str(value.get("selection_reason") or "").strip()
    if not reason:
        reason = f"Selected {selected} as the most executable and evidence-rich task type."
    return {
        "selected_task_type": selected,
        "selection_reason": reason,
        "rejected_task_types": rejected,
        "task_scores": scores,
        "decisive_evidence": [str(item) for item in value.get("decisive_evidence", [])],
        "missing_information": [str(item) for item in value.get("missing_information", [])],
    }


def _bounded(value: float) -> float:
    return round(max(0.0, min(100.0, float(value))), 1)

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.core.io import write_json
from src.core.logging import log_progress
from src.ingestion.grobid_quantities import GrobidQuantitiesClient
from src.ingestion.tei import read_tei_paragraphs, sentence_windows

RESOURCE_TERMS = re.compile(
    r"\b(?:cpu|gpu|core|cores|processor|processors|node|nodes|memory|ram|wall[- ]?time|"
    r"runtime|elapsed|hours?|hrs?|days?|minutes?|mins?|a100|h100|v100)\b",
    re.I,
)
PLATFORM_ONLY = re.compile(
    r"\b(?:cluster|supercomputer|facility|platform)\b.{0,50}\b(?:provides|supports|offers|has|"
    r"capacity|equipped)\b",
    re.I,
)
ACTUAL_USE = re.compile(
    r"\b(?:we|our|calculation|calculations|simulation|simulations|job|jobs|run|runs|ran|used|using|"
    r"employed|performed|executed|completed|took|required|allocated|utilized)\b",
    re.I,
)
COMPUTATION_CUE = re.compile(
    r"\b(?:computational|calculation|calculations|simulation|simulations|job|jobs|cpu|gpu|"
    r"cores?|processors?|nodes?|memory|ram|wall[- ]?time|runtime|elapsed|allocated)\b",
    re.I,
)
CPU_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?:physical\s+)?(?:cpu\s*)?(?:cores?|processors?|cpus?)\b",
    re.I,
)
GPU_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?:x\s*)?(?:(?:nvidia\s+)?(?:a100|h100|v100)\s*)?gpus?\b|"
    r"\bgpus?\s*(?:x|:)\s*(?P<value_after>\d+(?:\.\d+)?)",
    re.I,
)
MEMORY_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>mb|mib|gb|gib|tb|tib)\b"
    r"(?=.{0,35}\b(?:memory|ram)\b)|"
    r"\b(?:memory|ram)\b.{0,20}(?P<value_after>\d+(?:\.\d+)?)\s*"
    r"(?P<unit_after>mb|mib|gb|gib|tb|tib)\b",
    re.I,
)
TIME_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>seconds?|secs?|minutes?|mins?|hours?|hrs?|days?)\b",
    re.I,
)
TIME_CONTEXT = re.compile(
    r"\b(?:wall[- ]?time|runtime|elapsed|completed\s+in|took|ran\s+for|run\s+for|"
    r"cpu\s+time|gpu\s+time|required|performed|within|for)\b",
    re.I,
)
PHYSICAL_DURATION = re.compile(
    r"\b(?:trajectory|timestep|time\s+step|simulation\s+time|production\s+run)\b",
    re.I,
)


def assess_resource_limits(
    documents: list[dict[str, Any]],
    client: GrobidQuantitiesClient,
    limits: dict[str, Any],
    *,
    output_dir: str | Path,
) -> list[dict[str, Any]]:
    root = Path(output_dir).expanduser().resolve()
    raw_dir = root / "grobid_quantities_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    service_version = client.version()
    output: list[dict[str, Any]] = []

    for index, document in enumerate(documents, start=1):
        completeness = document.get("computation_completeness") or {}
        if completeness and not completeness.get("passed", False):
            output.append(document)
            continue
        contexts = _recall_contexts(document["grobid_tei_path"])
        raw_results = []
        mentions = []
        for context in contexts:
            raw = client.process_text(context["text"])
            raw_results.append({"context": context, "response": raw})
            mentions.extend(_keyword_mentions(context))
            mentions.extend(_quantity_mentions(context, raw))
        raw_path = raw_dir / f"{document['document_id']}.json"
        write_json(raw_path, raw_results)
        merged = _merge_mentions(mentions)
        explicit = [item for item in merged if item["binding"] == "actual_computation"]
        exceeded = [item for item in explicit if _exceeds(item, limits)]
        ambiguous = [item for item in merged if item["binding"] != "actual_computation"]
        if exceeded:
            decision, status, passed = "exceeds_limit", "reject", False
        elif explicit:
            decision, status, passed = "within_limit", "pass", True
        elif ambiguous:
            decision, status, passed = "ambiguous", "pass", True
        else:
            decision, status, passed = "no_explicit_resource", "pass", True
        routing = dict(document.get("pipeline_routing") or {})
        routing.update(
            {
                "stage_05": decision,
                "continue": passed,
                "stopped_at": None if passed else "stage_05_resource_limits",
                "stop_reason": None if passed else "explicit_resource_exceeds_limit",
            }
        )
        record = {
            **document,
            "resource_limits": {
                "status": status,
                "decision": decision,
                "passed": passed,
                "configured_limits": limits,
                "resource_mentions": merged,
                "exceeded_resources": exceeded,
                "recalled_context_count": len(contexts),
                "service_version": service_version,
                "grobid_quantities_raw_path": str(raw_path),
            },
            "pipeline_routing": routing,
        }
        output.append(record)
        log_progress(
            "stage_05_resource_limits",
            index,
            len(documents),
            document.get("title") or document["paper_id"],
            status=decision,
        )
    return output


def resource_limits_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    relevant = [item for item in records if item.get("resource_limits")]
    decisions: dict[str, int] = {}
    for item in relevant:
        decision = item["resource_limits"]["decision"]
        decisions[decision] = decisions.get(decision, 0) + 1
    return {"documents": len(relevant), "decisions": decisions}


def _recall_contexts(tei_path: str | Path) -> list[dict[str, Any]]:
    output = []
    for paragraph in read_tei_paragraphs(tei_path):
        for sentence in sentence_windows(paragraph):
            if RESOURCE_TERMS.search(sentence["text"]):
                output.append(sentence)
    return output


def _keyword_mentions(context: dict[str, Any]) -> list[dict[str, Any]]:
    text = context["text"]
    output = []
    binding = _resource_binding(text)
    for match in CPU_PATTERN.finditer(text):
        output.append(_mention("cpu_cores", float(match.group("value")), "cores", match, context, binding, "keyword"))
    for match in GPU_PATTERN.finditer(text):
        value = match.group("value") or match.group("value_after")
        output.append(_mention("gpus", float(value), "gpu", match, context, binding, "keyword"))
    for match in MEMORY_PATTERN.finditer(text):
        value = match.group("value") or match.group("value_after")
        unit = match.group("unit") or match.group("unit_after")
        output.append(_mention("memory_gb", _memory_gb(float(value), unit), "GB", match, context, binding, "keyword"))
    for match in TIME_PATTERN.finditer(text):
        window = text[max(0, match.start() - 55) : min(len(text), match.end() + 55)]
        if TIME_CONTEXT.search(window) and not PHYSICAL_DURATION.search(window):
            output.append(_mention("runtime_hours", _hours(float(match.group("value")), match.group("unit")), "hours", match, context, binding, "keyword"))
    return output


def _quantity_mentions(context: dict[str, Any], raw: dict[str, Any]) -> list[dict[str, Any]]:
    text = context["text"]
    binding = _resource_binding(text)
    output = []
    for measurement in raw.get("measurements") or []:
        quantity = measurement.get("quantity") or {}
        unit = quantity.get("rawUnit") or quantity.get("parsedUnit") or {}
        unit_type = str(unit.get("type") or quantity.get("type") or "").casefold()
        raw_unit = str(unit.get("name") or "").casefold()
        value = ((quantity.get("parsedValue") or {}).get("numeric"))
        if value is None:
            continue
        if unit_type == "time" and TIME_CONTEXT.search(text) and not PHYSICAL_DURATION.search(text):
            normalized = quantity.get("normalizedQuantity")
            hours = float(normalized) / 3600 if normalized is not None else _hours(float(value), raw_unit)
            output.append(_simple_mention("runtime_hours", hours, "hours", context, binding, "grobid_quantities", measurement))
    return output


def _resource_binding(text: str) -> str:
    if PLATFORM_ONLY.search(text) and not ACTUAL_USE.search(text):
        return "platform_only"
    if COMPUTATION_CUE.search(text) and ACTUAL_USE.search(text):
        return "actual_computation"
    return "ambiguous"


def _mention(
    resource: str,
    value: float,
    unit: str,
    match: re.Match[str],
    context: dict[str, Any],
    binding: str,
    source: str,
) -> dict[str, Any]:
    return _simple_mention(resource, value, unit, context, binding, source, {"raw": match.group(0)})


def _simple_mention(
    resource: str,
    value: float,
    unit: str,
    context: dict[str, Any],
    binding: str,
    source: str,
    raw: dict[str, Any],
) -> dict[str, Any]:
    return {
        "resource": resource,
        "value": value,
        "unit": unit,
        "binding": binding,
        "source": source,
        "evidence": context["text"],
        "section": context.get("section"),
        "paragraph_index": context.get("paragraph_index"),
        "raw_extraction": raw,
    }


def _merge_mentions(mentions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: dict[tuple[str, float, str], dict[str, Any]] = {}
    for item in mentions:
        key = (item["resource"], round(float(item["value"]), 6), item["evidence"])
        current = output.get(key)
        if current is None:
            output[key] = item
        elif current["source"] != item["source"]:
            current["source"] = "keyword+grobid_quantities"
    return list(output.values())


def _exceeds(mention: dict[str, Any], limits: dict[str, Any]) -> bool:
    mapping = {
        "cpu_cores": "cpu_cores",
        "gpus": "gpus",
        "memory_gb": "memory_gb",
        "runtime_hours": "runtime_hours",
    }
    limit = limits.get(mapping[mention["resource"]])
    return limit is not None and float(mention["value"]) > float(limit)


def _memory_gb(value: float, unit: str) -> float:
    factors = {"mb": 0.001, "mib": 1 / 1024, "gb": 1, "gib": 1.073741824, "tb": 1000, "tib": 1099.511628}
    return value * factors[unit.casefold()]


def _hours(value: float, unit: str) -> float:
    normalized = unit.casefold()
    if normalized.startswith("sec") or normalized == "s":
        return value / 3600
    if normalized.startswith("min"):
        return value / 60
    if normalized.startswith("day") or normalized == "d":
        return value * 24
    return value

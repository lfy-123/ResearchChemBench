from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Callable

from src.core.concurrency import ordered_parallel_map
from src.core.io import write_json, write_jsonl
from src.core.logging import log_progress
from src.integrations.grobid_quantities import GrobidQuantitiesClient
from src.integrations.llm_client import call_json_chat
from src.integrations.tei import read_tei_paragraphs, sentence_windows

PROMPT_VERSION = "stage04-resource-interpretation-v1"
RESOURCE_TYPES = {"cpu_cores", "gpus", "memory_gb", "runtime_hours"}
AGGREGATE_TYPES = {"cpu_hours", "core_hours", "gpu_hours", "node_hours"}
RELATIONS = {"exact", "approximately", "greater_than", "less_than", "range"}
SCOPES = {"single_job", "aggregate_study", "unknown"}
CONFIDENCE = {"high", "medium", "low"}
RESOURCE_TERMS = re.compile(
    r"\b(?:cpu|gpu|processors?|nodes?|memory|ram|wall[- ]?time|runtime|elapsed|"
    r"core[- ]?hours?|cpu[- ]?hours?|gpu[- ]?hours?|clusters?|supercomputers?|"
    r"computing (?:center|centre|facility)|a100|h100|v100)\b",
    re.I,
)
CPU_HINT = re.compile(
    r"(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?:-|\s)\s*(?:cpu\s*)?cores?\b(?!\s*[- ]?hours?)",
    re.I,
)
CPU_COUNT_HINT = re.compile(
    r"\b(?:core count|number of cores|cores? used)\D{0,20}(?P<value>\d[\d,]*(?:\.\d+)?)\b",
    re.I,
)
GPU_HINT = re.compile(
    r"(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?:x\s*)?(?:(?:nvidia\s+)?(?:a100|h100|v100)\s*)?gpus?\b",
    re.I,
)
MEMORY_HINT = re.compile(
    r"(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>mb|mib|gb|gib|tb|tib)\s*(?:of\s+)?(?:memory|ram)\b|"
    r"(?:memory|ram)\D{0,20}(?P<value_after>\d[\d,]*(?:\.\d+)?)\s*"
    r"(?P<unit_after>mb|mib|gb|gib|tb|tib)\b",
    re.I,
)
TIME_HINT = re.compile(
    r"(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?:wall\s+)?"
    r"(?P<unit>seconds?|minutes?|hours?|days?)\b",
    re.I,
)
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")

ModelCaller = Callable[..., tuple[dict[str, Any], dict[str, Any]]]


def assess_resource_limits(
    documents: list[dict[str, Any]],
    client: GrobidQuantitiesClient,
    limits: dict[str, Any],
    interpretation_config: dict[str, Any],
    *,
    output_dir: str | Path,
    model_caller: ModelCaller = call_json_chat,
    workers: int = 1,
) -> list[dict[str, Any]]:
    root = Path(output_dir).expanduser().resolve()
    raw_dir = root / "grobid_quantities_raw"
    input_dir = root / "model_inputs"
    response_dir = root / "model_responses"
    for directory in (raw_dir, input_dir, response_dir):
        directory.mkdir(parents=True, exist_ok=True)
    api_key = _require_model_config(interpretation_config)
    service_version = client.version()

    def assess(document: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        contexts = _recall_contexts(document["grobid_tei_path"])
        recalled_row = {
            "document_id": document["document_id"],
            "title": document.get("title"),
            "contexts": contexts,
        }
        raw_results = [
            {
                "context": context,
                "keyword_hints": _keyword_hints(context["text"]),
                "response": client.process_text(context["text"]),
            }
            for context in contexts
        ]
        raw_path = raw_dir / f"{document['document_id']}.json"
        write_json(raw_path, raw_results)
        input_path = input_dir / f"{document['document_id']}.txt"
        packet = _build_packet(document, raw_results, limits)
        input_path.write_text(packet, encoding="utf-8")

        if contexts:
            try:
                structured, audit = _call_and_validate(
                    model_caller, packet, contexts, interpretation_config, api_key
                )
            except Exception as exc:
                write_json(
                    response_dir / f"{document['document_id']}.error.json",
                    {"error_type": type(exc).__name__, "message": str(exc)},
                )
                raise
            response_path = response_dir / f"{document['document_id']}.json"
            write_json(response_path, {"response": structured, "audit": audit})
            model_audit = {key: item for key, item in audit.items() if key != "raw_content"}
        else:
            structured = _empty_result()
            response_path = None
            model_audit = None

        comparable = [
            item
            for item in structured["resource_records"]
            if item["actual_computation"] and item["scope"] == "single_job"
        ]
        exceeded = [item for item in comparable if _exceeds(item, limits)]
        has_structured_signal = any(
            structured[key]
            for key in (
                "resource_records",
                "aggregate_resources",
                "platform_mentions",
                "physical_simulation_durations",
                "unresolved_mentions",
            )
        )
        if exceeded:
            decision, status, passed = "exceeds_limit", "reject", False
        elif comparable:
            decision, status, passed = "within_limit", "pass", True
        elif has_structured_signal:
            decision, status, passed = "ambiguous", "pass", True
        else:
            decision, status, passed = "no_explicit_resource", "pass", True

        routing = dict(document.get("pipeline_routing") or {})
        routing.update(
            {
                "stage_04": decision,
                "continue": passed,
                "stopped_at": None if passed else "stage_04_resource_limits",
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
                "resource_records": structured["resource_records"],
                "aggregate_resources": structured["aggregate_resources"],
                "platform_mentions": structured["platform_mentions"],
                "physical_simulation_durations": structured["physical_simulation_durations"],
                "unresolved_mentions": structured["unresolved_mentions"],
                "exceeded_resources": exceeded,
                "recalled_context_count": len(contexts),
                "prompt_version": PROMPT_VERSION,
                "model_input_path": str(input_path),
                "model_response_path": str(response_path) if response_path else None,
                "model_audit": model_audit,
                "service_version": service_version,
                "grobid_quantities_raw_path": str(raw_path),
            },
            "pipeline_routing": routing,
        }
        return record, recalled_row

    assessed = ordered_parallel_map(
        assess,
        documents,
        max_workers=workers,
        on_complete=lambda completed, total, _index, document, result: log_progress(
            "stage_04_resource_limits",
            completed,
            total,
            document.get("title") or document["paper_id"],
            status=(result[0].get("resource_limits") or {}).get("decision"),
        ),
    )
    output = [record for record, _recalled in assessed]
    recalled_rows = [recalled for _record, recalled in assessed]
    write_jsonl(root / "recalled_contexts.jsonl", recalled_rows)
    write_jsonl(
        root / "structured_resource_documents.jsonl",
        [
            {
                "document_id": item["document_id"],
                "title": item.get("title"),
                **{
                    key: value
                    for key, value in item["resource_limits"].items()
                    if key
                    in {
                        "resource_records",
                        "aggregate_resources",
                        "platform_mentions",
                        "physical_simulation_durations",
                        "unresolved_mentions",
                    }
                },
            }
            for item in output
        ],
    )
    return output


def resource_limits_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    decisions: dict[str, int] = {}
    prompt_tokens = completion_tokens = 0
    for item in records:
        result = item.get("resource_limits") or {}
        if not result:
            continue
        decision = result["decision"]
        decisions[decision] = decisions.get(decision, 0) + 1
        usage = (result.get("model_audit") or {}).get("usage") or {}
        prompt_tokens += int(usage.get("prompt_tokens") or 0)
        completion_tokens += int(usage.get("completion_tokens") or 0)
    return {
        "documents": sum(decisions.values()),
        "decisions": decisions,
        "model_usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


def bypass_resource_limits(
    documents: list[dict[str, Any]], limits: dict[str, Any]
) -> list[dict[str, Any]]:
    output = []
    for index, document in enumerate(documents, start=1):
        routing = dict(document.get("pipeline_routing") or {})
        routing.update(
            {"stage_04": "skipped", "continue": True, "stopped_at": None, "stop_reason": None}
        )
        output.append(
            {
                **document,
                "resource_limits": {
                    "status": "skipped",
                    "decision": "skipped",
                    "passed": True,
                    "skipped": True,
                    "configured_limits": limits,
                    "resource_records": [],
                    "aggregate_resources": [],
                    "platform_mentions": [],
                    "physical_simulation_durations": [],
                    "unresolved_mentions": [],
                    "exceeded_resources": [],
                    "recalled_context_count": 0,
                    "model_audit": None,
                },
                "pipeline_routing": routing,
            }
        )
        log_progress(
            "stage_04_resource_limits",
            index,
            len(documents),
            document.get("title") or document["paper_id"],
            status="skipped",
        )
    return output


def _recall_contexts(tei_path: str | Path) -> list[dict[str, Any]]:
    return [
        sentence
        for paragraph in read_tei_paragraphs(tei_path)
        for sentence in sentence_windows(paragraph)
        if (
            RESOURCE_TERMS.search(sentence["text"])
            or CPU_HINT.search(sentence["text"])
            or CPU_COUNT_HINT.search(sentence["text"])
            or TIME_HINT.search(sentence["text"])
        )
    ]


def _keyword_hints(text: str) -> list[dict[str, Any]]:
    output = []
    for resource, pattern in (("cpu_cores", CPU_HINT), ("gpus", GPU_HINT)):
        for match in pattern.finditer(text):
            output.append({"resource_type": resource, "raw": match.group(0)})
    for match in CPU_COUNT_HINT.finditer(text):
        output.append({"resource_type": "cpu_cores", "raw": match.group(0)})
    for match in MEMORY_HINT.finditer(text):
        output.append({"resource_type": "memory", "raw": match.group(0)})
    for match in TIME_HINT.finditer(text):
        output.append({"resource_type": "time", "raw": match.group(0)})
    return output


def _build_packet(
    document: dict[str, Any],
    raw_results: list[dict[str, Any]],
    limits: dict[str, Any],
) -> str:
    payload = {
        "prompt_version": PROMPT_VERSION,
        "title": document.get("title", ""),
        "limits": limits,
        "candidate_contexts": [
            {
                "context": {
                    key: item["context"].get(key)
                    for key in ("text", "section", "paragraph_index", "sentence_index")
                },
                "keyword_hints": item["keyword_hints"],
                "grobid_measurements": [
                    _compact_measurement(measurement)
                    for measurement in item["response"].get("measurements") or []
                ],
            }
            for item in raw_results
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _compact_measurement(measurement: dict[str, Any]) -> dict[str, Any]:
    quantity = measurement.get("quantity") or {}
    raw_unit = quantity.get("rawUnit") or {}
    return {
        "measurement_raw": measurement.get("measurementRaw"),
        "raw_value": quantity.get("rawValue"),
        "numeric_value": (quantity.get("parsedValue") or {}).get("numeric"),
        "raw_unit": raw_unit.get("name"),
        "unit_type": raw_unit.get("type") or quantity.get("type"),
        "normalized_quantity": quantity.get("normalizedQuantity"),
        "quantified": (measurement.get("quantified") or {}).get("rawName"),
    }


def _require_model_config(config: dict[str, Any]) -> str:
    if not config.get("enabled", True):
        raise RuntimeError("Resource interpretation model is disabled")
    api_key = config.get("api_key")
    if not api_key and config.get("api_key_env"):
        api_key = os.environ.get(str(config["api_key_env"]))
    api_key = api_key or os.environ.get("RCB_LLM_API_KEY")
    missing = [key for key in ("base_url", "model") if not config.get(key)]
    if not api_key:
        missing.append("api_key")
    if missing:
        raise RuntimeError(f"Resource interpretation model is not configured: {', '.join(missing)}")
    return str(api_key)


def _call_and_validate(
    model_caller: ModelCaller,
    packet: str,
    contexts: list[dict[str, Any]],
    config: dict[str, Any],
    api_key: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validation_retries = int(config.get("validation_retries", 1))
    last_error: Exception | None = None
    for attempt in range(validation_retries + 1):
        content = packet
        if last_error:
            content += (
                f"\n\nPrevious response was invalid: {last_error}. Return corrected JSON only."
            )
        value, audit = model_caller(
            model=str(config["model"]),
            base_url=str(config["base_url"]),
            api_key=api_key,
            system_prompt=_system_prompt(),
            user_content=content,
            timeout_seconds=float(config.get("timeout_seconds", 180)),
            max_tokens=int(config.get("max_tokens", 3000)),
            retries=int(config.get("retries", 1)),
            thinking=config.get("thinking"),
        )
        if audit.get("finish_reason") == "length":
            last_error = ValueError("model output reached max_tokens")
            continue
        try:
            structured = _validate_model_result(value, contexts)
            return structured, {**audit, "validation_attempts": attempt + 1}
        except ValueError as exc:
            last_error = exc
    raise ValueError(f"Resource model returned invalid structured data: {last_error}")


def _validate_model_result(value: dict[str, Any], contexts: list[dict[str, Any]]) -> dict[str, Any]:
    evidence_texts = {re.sub(r"\s+", " ", item["text"]).strip() for item in contexts}
    output = _empty_result()
    for field in output:
        items = value.get(field, [])
        if not isinstance(items, list):
            raise ValueError(f"{field} must be a list")
        output[field] = items
    for item in output["resource_records"]:
        _validate_resource_record(item, evidence_texts, RESOURCE_TYPES)
    for item in output["aggregate_resources"]:
        _validate_resource_record(item, evidence_texts, AGGREGATE_TYPES)
    output["platform_mentions"] = [
        _normalize_platform(item, evidence_texts) for item in output["platform_mentions"]
    ]
    output["unresolved_mentions"] = [
        _normalize_unresolved(item, evidence_texts) for item in output["unresolved_mentions"]
    ]
    output["physical_simulation_durations"] = [
        _normalize_physical_duration(item, evidence_texts)
        for item in output["physical_simulation_durations"]
    ]
    return output


def _validate_resource_record(item: Any, evidence_texts: set[str], allowed_types: set[str]) -> None:
    if not isinstance(item, dict):
        raise ValueError("resource records must be objects")
    if item.get("resource_type") not in allowed_types:
        raise ValueError("invalid resource_type")
    if not isinstance(item.get("value"), (int, float)) or item["value"] < 0:
        raise ValueError("resource value must be non-negative")
    if item.get("relation") not in RELATIONS or item.get("scope") not in SCOPES:
        raise ValueError("invalid relation or scope")
    if not isinstance(item.get("actual_computation"), bool):
        raise ValueError("actual_computation must be boolean")
    if item.get("confidence") not in CONFIDENCE:
        raise ValueError("invalid confidence")
    if not _valid_evidence(item.get("evidence"), evidence_texts):
        raise ValueError("resource evidence must exactly match a candidate context")
    if not _value_supported_by_evidence(item):
        raise ValueError(f"resource value is not supported by its evidence: {item}")
    if item.get("upper_value") is not None and not isinstance(item["upper_value"], (int, float)):
        raise ValueError("upper_value must be numeric")


def _valid_evidence(evidence: Any, texts: set[str]) -> bool:
    return isinstance(evidence, str) and re.sub(r"\s+", " ", evidence).strip() in texts


def _normalize_platform(item: Any, texts: set[str]) -> dict[str, str]:
    if not isinstance(item, dict):
        raise ValueError("platform mentions must be objects")
    evidence = item.get("evidence") or item.get("context")
    name = item.get("name") or item.get("platform")
    if not isinstance(name, str) or not _valid_evidence(evidence, texts):
        raise ValueError("platform mentions require name and exact evidence")
    return {"name": name, "evidence": evidence}


def _normalize_unresolved(item: Any, texts: set[str]) -> dict[str, str]:
    if not isinstance(item, dict):
        raise ValueError("unresolved mentions must be objects")
    evidence = item.get("evidence") or item.get("text")
    reason = item.get("reason")
    if not isinstance(reason, str) or not _valid_evidence(evidence, texts):
        raise ValueError("unresolved mentions require reason and exact evidence")
    return {"evidence": evidence, "reason": reason}


def _normalize_physical_duration(item: Any, texts: set[str]) -> dict[str, Any]:
    if not isinstance(item, dict) or not _valid_evidence(item.get("evidence"), texts):
        raise ValueError("physical durations require exact evidence")
    if not isinstance(item.get("value"), (int, float)) or not isinstance(item.get("unit"), str):
        raise ValueError("physical durations require numeric value and unit")
    return {"value": item["value"], "unit": item["unit"], "evidence": item["evidence"]}


def _value_supported_by_evidence(item: dict[str, Any]) -> bool:
    evidence = item["evidence"]
    target = float(item["value"])
    resource_type = item["resource_type"]
    if resource_type == "cpu_cores":
        candidates = [_number(match.group("value")) for match in CPU_HINT.finditer(evidence)]
        candidates.extend(
            _number(match.group("value")) for match in CPU_COUNT_HINT.finditer(evidence)
        )
    elif resource_type == "gpus":
        candidates = [_number(match.group("value")) for match in GPU_HINT.finditer(evidence)]
    elif resource_type == "memory_gb":
        candidates = []
        for match in MEMORY_HINT.finditer(evidence):
            value = _number(match.group("value") or match.group("value_after"))
            unit = (match.group("unit") or match.group("unit_after")).casefold()
            candidates.append(value * _memory_factor(unit))
    elif resource_type == "runtime_hours":
        candidates = _runtime_candidates(evidence)
    else:
        candidates = _aggregate_candidates(evidence)
    return any(abs(candidate - target) <= max(1e-6, abs(target) * 1e-6) for candidate in candidates)


def _runtime_candidates(evidence: str) -> list[float]:
    candidates = []
    matches = list(TIME_HINT.finditer(evidence))
    for match in matches:
        candidates.append(_hours(_number(match.group("value")), match.group("unit")))
    for left, right in zip(matches, matches[1:], strict=False):
        between = evidence[left.end() : right.start()]
        if re.fullmatch(r"\s*(?:,?\s*and\s+|,\s*)", between, re.I):
            candidates.append(
                _hours(_number(left.group("value")), left.group("unit"))
                + _hours(_number(right.group("value")), right.group("unit"))
            )
    return candidates


def _aggregate_candidates(evidence: str) -> list[float]:
    output = []
    for match in NUMBER.finditer(evidence):
        multiplier_text = evidence[match.end() : match.end() + 12].casefold()
        multiplier = 1_000_000_000 if "billion" in multiplier_text else 1
        if "million" in multiplier_text:
            multiplier = 1_000_000
        elif "thousand" in multiplier_text:
            multiplier = 1_000
        output.append(_number(match.group(0)) * multiplier)
    return output


def _number(value: str) -> float:
    return float(value.replace(",", ""))


def _memory_factor(unit: str) -> float:
    return {
        "mb": 0.001,
        "mib": 1 / 1024,
        "gb": 1,
        "gib": 1.073741824,
        "tb": 1000,
        "tib": 1099.511628,
    }[unit]


def _hours(value: float, unit: str) -> float:
    normalized = unit.casefold()
    if normalized.startswith("second"):
        return value / 3600
    if normalized.startswith("minute"):
        return value / 60
    if normalized.startswith("day"):
        return value * 24
    return value


def _exceeds(item: dict[str, Any], limits: dict[str, Any]) -> bool:
    limit = limits.get(item["resource_type"])
    if limit is None or item["relation"] == "less_than":
        return False
    value = float(item["value"])
    if item["relation"] == "greater_than":
        return value >= float(limit)
    if item["relation"] == "range":
        return value > float(limit)
    return value > float(limit)


def _empty_result() -> dict[str, list[Any]]:
    return {
        "resource_records": [],
        "aggregate_resources": [],
        "platform_mentions": [],
        "physical_simulation_durations": [],
        "unresolved_mentions": [],
    }


def _system_prompt() -> str:
    return """You extract explicitly reported computing resources from chemistry papers.
Return one JSON object with exactly these list fields: resource_records, aggregate_resources,
platform_mentions, physical_simulation_durations, unresolved_mentions.

Each resource record must contain resource_type (cpu_cores, gpus, memory_gb, runtime_hours),
value normalized to cores, GPU count, GB, or hours, relation (exact, approximately,
greater_than, less_than, range), scope (single_job, aggregate_study, unknown),
actual_computation (boolean), confidence (high, medium, low), and evidence copied exactly from
one candidate context. A range may include upper_value.

Never infer unreported resources. Do not treat CPU model numbers such as Xeon Gold 6230 as
core counts. Put CPU-hours, core-hours, GPU-hours, and node-hours in aggregate_resources using
resource_type cpu_hours, core_hours, gpu_hours, or node_hours. Put molecular-dynamics physical durations such as ns, ps,
or fs in physical_simulation_durations, not runtime_hours. Platform names alone do not imply
resource quantities. Combine durations such as 1 day and 4 hours into 28 runtime_hours.
Only report resources used by this paper's actual computations; keep background or facility
capacity statements unresolved or mark actual_computation false.

Platform records must use {"name": string, "evidence": exact candidate context}.
Physical-duration records must use {"value": number, "unit": string, "evidence": exact context}.
Unresolved records must use {"evidence": exact candidate context, "reason": string}."""

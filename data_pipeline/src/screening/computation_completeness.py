from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

from src.core.io import write_json
from src.core.logging import log_progress
from src.curation.llm_client import call_json_chat
from src.ingestion.tei import read_tei_paragraphs

PROMPT_VERSION = "stage04-computation-completeness-v1"
SECTION_TERMS = {
    "method": (
        "computational",
        "calculation",
        "method",
        "simulation",
        "theoretical",
        "density functional",
    ),
    "result": ("result", "discussion", "analysis", "mechanism", "energy", "structure"),
    "conclusion": ("conclusion", "summary", "outlook"),
}

ModelCaller = Callable[..., tuple[dict[str, Any], dict[str, Any]]]


def assess_computation_completeness(
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    *,
    output_dir: str | Path,
    model_caller: ModelCaller = call_json_chat,
) -> list[dict[str, Any]]:
    root = Path(output_dir).expanduser().resolve()
    input_dir = root / "model_inputs"
    response_dir = root / "model_responses"
    input_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)
    configured, skip_reason, api_key = _configuration_state(config)
    output: list[dict[str, Any]] = []

    for index, document in enumerate(documents, start=1):
        if (document.get("software_coverage") or {}).get("decision") != "direct_covered":
            output.append(document)
            continue
        packet = build_computation_packet(
            document,
            max_paragraphs=int(config.get("max_paragraphs", 24)),
            max_chars=int(config.get("max_source_chars", 30_000)),
        )
        input_path = input_dir / f"{document['document_id']}.txt"
        input_path.write_text(packet, encoding="utf-8")
        if not configured:
            record = _with_result(
                document,
                status="skipped",
                decision="skipped",
                passed=True,
                reason=skip_reason,
                input_path=input_path,
            )
        else:
            try:
                value, audit = model_caller(
                    model=str(config["model"]),
                    base_url=str(config["base_url"]),
                    api_key=str(api_key),
                    system_prompt=_system_prompt(),
                    user_content=packet,
                    timeout_seconds=float(config.get("timeout_seconds", 900)),
                    max_tokens=int(config.get("max_tokens", 1800)),
                    retries=int(config.get("retries", 2)),
                    thinking=config.get("thinking"),
                )
                normalized = _validate_model_result(value)
                response_path = response_dir / f"{document['document_id']}.json"
                write_json(response_path, {"response": normalized, "audit": audit})
                decision = normalized["decision"]
                passed = decision == "complete"
                record = _with_result(
                    document,
                    status="pass" if passed else "reject",
                    decision=decision,
                    passed=passed,
                    reason=normalized["reason"],
                    input_path=input_path,
                    response_path=response_path,
                    model_result=normalized,
                    model_audit={key: value for key, value in audit.items() if key != "raw_content"},
                )
            except Exception as exc:  # API and malformed responses intentionally skip this gate.
                error_path = response_dir / f"{document['document_id']}.error.json"
                write_json(error_path, {"error_type": type(exc).__name__, "message": str(exc)})
                record = _with_result(
                    document,
                    status="skipped_error",
                    decision="skipped",
                    passed=True,
                    reason=f"model_call_failed: {type(exc).__name__}: {exc}",
                    input_path=input_path,
                    response_path=error_path,
                )
        output.append(record)
        result = record["computation_completeness"]
        log_progress(
            "stage_04_computation_completeness",
            index,
            len(documents),
            document.get("title") or document["paper_id"],
            status=result["status"],
        )
    return output


def build_computation_packet(
    document: dict[str, Any], *, max_paragraphs: int = 24, max_chars: int = 30_000
) -> str:
    paragraphs = read_tei_paragraphs(document["grobid_tei_path"])
    selected: list[dict[str, Any]] = []
    seen: set[int] = set()
    software_evidence = [
        item.get("evidence", "")
        for item in (document.get("software_coverage") or {}).get("core_software", [])
        if item.get("evidence")
    ]
    for category in ("method", "result", "conclusion"):
        terms = SECTION_TERMS[category]
        for paragraph in paragraphs:
            haystack = f"{paragraph.get('section', '')} {paragraph['text']}".casefold()
            if paragraph["paragraph_index"] not in seen and any(term in haystack for term in terms):
                selected.append({**paragraph, "category": category})
                seen.add(paragraph["paragraph_index"])
                if len(selected) >= max_paragraphs:
                    break
        if len(selected) >= max_paragraphs:
            break
    if not selected:
        selected = [{**item, "category": "body"} for item in paragraphs[:max_paragraphs]]
    lines = [
        f"PROMPT_VERSION: {PROMPT_VERSION}",
        f"TITLE: {document.get('title', '')}",
        f"ABSTRACT: {document.get('abstract', '')}",
        "CORE_SOFTWARE_EVIDENCE:",
        *[f"- {item}" for item in software_evidence],
        "SELECTED_TEI_EVIDENCE:",
    ]
    for item in selected:
        lines.append(
            f"[{item['category']} | {item.get('section') or 'unheaded'} | "
            f"paragraph {item['paragraph_index']}] {item['text']}"
        )
    return "\n".join(lines)[:max_chars]


def computation_completeness_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    relevant = [item for item in records if item.get("computation_completeness")]
    statuses: dict[str, int] = {}
    decisions: dict[str, int] = {}
    for item in relevant:
        result = item["computation_completeness"]
        statuses[result["status"]] = statuses.get(result["status"], 0) + 1
        decisions[result["decision"]] = decisions.get(result["decision"], 0) + 1
    return {"documents": len(relevant), "statuses": statuses, "decisions": decisions}


def _configuration_state(config: dict[str, Any]) -> tuple[bool, str, str | None]:
    if not config.get("enabled", False):
        return False, "model_not_enabled", None
    api_key = config.get("api_key")
    if not api_key and config.get("api_key_env"):
        api_key = os.environ.get(str(config["api_key_env"]))
    api_key = api_key or os.environ.get("RCB_LLM_API_KEY")
    missing = [name for name in ("base_url", "model") if not config.get(name)]
    if not api_key:
        missing.append("api_key")
    if missing:
        return False, f"model_not_configured: {', '.join(missing)}", None
    return True, "", str(api_key)


def _validate_model_result(value: dict[str, Any]) -> dict[str, Any]:
    decision = str(value.get("decision", "")).casefold()
    if decision not in {"complete", "incomplete", "uncertain"}:
        raise ValueError("decision must be complete, incomplete, or uncertain")
    fields = (
        "has_computational_object",
        "has_method_setup",
        "has_software_execution",
        "has_computational_results",
        "has_interpretation_or_conclusion",
    )
    for field in fields:
        if not isinstance(value.get(field), bool):
            raise ValueError(f"{field} must be boolean")
    if decision == "complete" and not all(value[field] for field in fields):
        decision = "uncertain"
    evidence = value.get("evidence")
    if not isinstance(evidence, list) or not all(isinstance(item, str) for item in evidence):
        raise ValueError("evidence must be a list of strings")
    reason = value.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    return {**value, "decision": decision, "evidence": evidence, "reason": reason.strip()}


def _with_result(
    document: dict[str, Any],
    *,
    status: str,
    decision: str,
    passed: bool,
    reason: str,
    input_path: Path,
    response_path: Path | None = None,
    model_result: dict[str, Any] | None = None,
    model_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    routing = dict(document.get("pipeline_routing") or {})
    routing.update(
        {
            "stage_04": decision,
            "stage_05": "pending" if passed else "not_run",
            "continue": passed,
            "stopped_at": None if passed else "stage_04_computation_completeness",
            "stop_reason": None if passed else f"computation_{decision}",
        }
    )
    return {
        **document,
        "computation_completeness": {
            "status": status,
            "decision": decision,
            "passed": passed,
            "reason": reason,
            "prompt_version": PROMPT_VERSION,
            "model_input_path": str(input_path),
            "model_response_path": str(response_path) if response_path else None,
            "model_result": model_result,
            "model_audit": model_audit,
        },
        "pipeline_routing": routing,
    }


def _system_prompt() -> str:
    schema = {
        "decision": "complete | incomplete | uncertain",
        "has_computational_object": True,
        "has_method_setup": True,
        "has_software_execution": True,
        "has_computational_results": True,
        "has_interpretation_or_conclusion": True,
        "evidence": ["short source-grounded evidence"],
        "reason": "short reason",
    }
    return (
        "Judge only whether the paper contains a complete, independently constructable "
        "computational chemistry process: a defined object/input, method setup, actual software "
        "execution, computational results, and interpretation or conclusion. Background-only, "
        "incidental, or incomplete calculations are incomplete. Use uncertain when evidence is "
        "insufficient. Return exactly one JSON object matching this schema: "
        + json.dumps(schema)
    )

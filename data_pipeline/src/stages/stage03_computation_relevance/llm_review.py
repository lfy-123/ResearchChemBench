from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from pathlib import Path
from typing import Any

from src.core.concurrency import ordered_parallel_map
from src.core.io import read_json, write_json
from src.core.logging import log_progress, pipeline_logger
from src.integrations.llm_client import call_json_chat

PROMPT_VERSION = "stage03-computation-review-v1"
SYSTEM_PROMPT = """You screen scientific papers for computational chemistry work.
Decide whether the authors of THIS paper actually executed a computational chemistry process.
Do not count calculations only cited from earlier work, generic method background, experimental arithmetic,
data plotting, or software mentioned without use. Reviews and perspectives pass only when their authors report
new computations performed in this paper. A passing computation may be primary or scientifically supporting.
Use only the supplied excerpts. Return one JSON object and no prose with exactly these fields:
performed_computation: yes, no, or uncertain;
article_role: original_research, review, correction, editorial, or unknown;
computation_role: primary, supporting, background_only, or none;
method_families: array of strings;
author_execution_evidence: array of objects with excerpt_id, quote, and reason;
confidence: number from 0 to 1;
reason: short string.
For yes, quote at least one supplied excerpt that attributes execution to this paper's authors. If the evidence
does not establish the executing authors, return uncertain rather than guessing."""


def apply_llm_review(
    records: list[dict[str, Any]],
    *,
    config: dict[str, Any],
    cache_dir: str | Path,
) -> list[dict[str, Any]]:
    if not config.get("enabled", False):
        return [_not_requested(record, "disabled") for record in records]

    strict = bool(config.get("strict", False))
    requested = [
        index for index, record in enumerate(records) if _needs_review(record, config)
    ]
    requested_set = set(requested)
    if not requested:
        return [_not_requested(record, "clear_rule_decision") for record in records]
    if not _service_ready(config):
        pipeline_logger().warning(
            "STAGE03 LLM unavailable; falling back to rule decisions for %d papers", len(requested)
        )
        return [
            _fallback(record, "service_unavailable", strict=strict)
            if index in requested_set
            else _not_requested(record, "clear_rule_decision")
            for index, record in enumerate(records)
        ]

    output = list(records)
    review_items = [(index, records[index]) for index in requested]
    cache_root = Path(cache_dir)
    cache_root.mkdir(parents=True, exist_ok=True)

    def review(item: tuple[int, dict[str, Any]]) -> tuple[int, dict[str, Any]]:
        index, record = item
        try:
            return index, _review_one(record, config=config, cache_dir=cache_root)
        except Exception as exc:
            pipeline_logger().warning(
                "STAGE03 LLM fallback | paper=%s | error=%s: %s",
                record.get("paper_id"),
                type(exc).__name__,
                exc,
            )
            return index, _fallback(
                record, f"{type(exc).__name__}: {exc}", strict=strict
            )

    reviewed = ordered_parallel_map(
        review,
        review_items,
        max_workers=int(config.get("concurrency", 16)),
        on_complete=lambda completed, total, _index, item, result: log_progress(
            "stage_03_llm_review",
            completed,
            total,
            str(item[1].get("paper_id")),
            status=(result[1].get("llm_computation_review") or {}).get("status"),
        ),
    )
    for index, record in reviewed:
        output[index] = record
    for index, record in enumerate(output):
        if index not in requested_set:
            output[index] = _not_requested(record, "clear_rule_decision")
    return output


def build_review_prompt(
    record: dict[str, Any], *, max_chars: int = 24_000
) -> tuple[str, dict[str, str]]:
    relevance = record.get("computation_relevance") or {}
    excerpts: list[dict[str, Any]] = []
    source_map: dict[str, str] = {}
    opening = _opening_excerpt(record, 4_000)
    if opening:
        excerpts.append({"excerpt_id": "opening", "section": "opening", "text": opening})
        source_map["opening"] = opening
    evidence = [
        *(relevance.get("evidence") or []),
        *(relevance.get("excluded_evidence") or []),
    ]
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(evidence, start=1):
        snippet = str(item.get("snippet") or "").strip()
        if not snippet:
            continue
        key = (str(item.get("document_id") or ""), _normalize(snippet))
        if key in seen:
            continue
        seen.add(key)
        excerpt_id = f"e{index:03d}"
        value = {
            "excerpt_id": excerpt_id,
            "document_role": item.get("document_role"),
            "section": item.get("section"),
            "evidence_type": item.get("evidence_type"),
            "excluded_by_rule": bool(item.get("excluded")),
            "text": snippet[:700],
        }
        excerpts.append(value)
        source_map[excerpt_id] = str(value["text"])
        if len(excerpts) >= 30:
            break
    payload = {
        "prompt_version": PROMPT_VERSION,
        "paper": {
            "paper_id": record.get("paper_id"),
            "doi": record.get("doi"),
            "title": record.get("title"),
            "journal": record.get("journal_name"),
        },
        "rule_assessment": {
            "decision": relevance.get("decision"),
            "score": relevance.get("score"),
            "article_role_hint": relevance.get("article_role"),
            "method_families": relevance.get("method_families") or [],
            "evidence_types": relevance.get("evidence_types") or [],
        },
        "excerpts": excerpts,
    }
    while True:
        content = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        if len(content) <= max_chars or len(payload["excerpts"]) <= 1:
            break
        removed = payload["excerpts"].pop()
        source_map.pop(str(removed["excerpt_id"]), None)
    return content[:max_chars], source_map


def _review_one(
    record: dict[str, Any], *, config: dict[str, Any], cache_dir: Path
) -> dict[str, Any]:
    user_content, source_map = build_review_prompt(
        record, max_chars=int(config.get("max_prompt_chars", 24_000))
    )
    max_tokens = int(config.get("max_tokens", 1024))
    thinking = str(config.get("thinking") or "") or None
    digest = hashlib.sha256(
        json.dumps(
            {
                "prompt_version": PROMPT_VERSION,
                "model": config["model"],
                "max_tokens": max_tokens,
                "thinking": thinking,
                "system": SYSTEM_PROMPT,
                "user": user_content,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    cache_path = cache_dir / f"{digest}.json"
    if cache_path.is_file():
        cached = read_json(cache_path)
        response = cached["response"]
        audit = cached["audit"]
        cache_hit = True
    else:
        response, audit = call_json_chat(
            model=str(config["model"]),
            base_url=str(config["base_url"]),
            api_key=str(config.get("api_key") or "EMPTY"),
            system_prompt=SYSTEM_PROMPT,
            user_content=user_content,
            timeout_seconds=float(config.get("timeout_seconds", 300)),
            max_tokens=max_tokens,
            retries=int(config.get("retries", 2)),
            thinking=thinking,
        )
        write_json(
            cache_path,
            {
                "schema_version": 1,
                "prompt_version": PROMPT_VERSION,
                "request_hash": digest,
                "response": response,
                "audit": audit,
            },
        )
        cache_hit = False
    if audit.get("finish_reason") == "length":
        raise ValueError("model response reached the output token limit")
    required_fields = {
        "performed_computation",
        "article_role",
        "computation_role",
        "method_families",
        "author_execution_evidence",
        "confidence",
        "reason",
    }
    missing_fields = sorted(required_fields - response.keys())
    if missing_fields:
        raise ValueError(f"model response is missing required fields: {missing_fields}")
    validated = _validate_response(response, source_map)
    return _apply_decision(
        record,
        validated,
        config=config,
        request_hash=digest,
        cache_path=cache_path,
        cache_hit=cache_hit,
        audit=audit,
    )


def _validate_response(value: dict[str, Any], source_map: dict[str, str]) -> dict[str, Any]:
    performed = str(value.get("performed_computation") or "uncertain").casefold()
    if performed not in {"yes", "no", "uncertain"}:
        performed = "uncertain"
    role = str(value.get("article_role") or "unknown").casefold()
    if role not in {"original_research", "review", "correction", "editorial", "unknown"}:
        role = "unknown"
    computation_role = str(value.get("computation_role") or "none").casefold()
    if computation_role not in {"primary", "supporting", "background_only", "none"}:
        computation_role = "none"
    verified: list[dict[str, str]] = []
    for raw in value.get("author_execution_evidence") or []:
        if not isinstance(raw, dict):
            continue
        excerpt_id = str(raw.get("excerpt_id") or "")
        quote = str(raw.get("quote") or "").strip()
        source = source_map.get(excerpt_id, "")
        if len(_normalize(quote)) >= 12 and _normalize(quote) in _normalize(source):
            verified.append(
                {
                    "excerpt_id": excerpt_id,
                    "quote": quote,
                    "reason": str(raw.get("reason") or "")[:500],
                }
            )
    if performed == "yes" and not verified:
        performed = "uncertain"
    try:
        confidence = min(1.0, max(0.0, float(value.get("confidence", 0.0))))
    except (TypeError, ValueError):
        confidence = 0.0
    return {
        "performed_computation": performed,
        "article_role": role,
        "computation_role": computation_role,
        "method_families": [str(item) for item in value.get("method_families") or []][:20],
        "author_execution_evidence": verified,
        "confidence": confidence,
        "reason": str(value.get("reason") or "")[:1000],
    }


def _apply_decision(
    record: dict[str, Any],
    review: dict[str, Any],
    *,
    config: dict[str, Any],
    request_hash: str,
    cache_path: Path,
    cache_hit: bool,
    audit: dict[str, Any],
) -> dict[str, Any]:
    original = str((record.get("computation_relevance") or {}).get("decision"))
    performed = review["performed_computation"]
    strict = bool(config.get("strict", False))
    minimum_confidence = float(config.get("minimum_confidence", 0.85 if strict else 0.7))
    allowed_article_roles = set(
        config.get("allowed_article_roles")
        or (["original_research"] if strict else ["original_research", "unknown"])
    )
    allowed_computation_roles = set(
        config.get("allowed_computation_roles") or ["primary", "supporting"]
    )
    confirmed = (
        performed == "yes"
        and review["confidence"] >= minimum_confidence
        and review["article_role"] in allowed_article_roles
        and review["computation_role"] in allowed_computation_roles
        and bool(review["author_execution_evidence"])
    )
    if confirmed:
        decision = "strong_candidate" if review["confidence"] >= 0.7 else "weak_candidate"
    elif performed == "no":
        decision = "not_computational"
    elif strict:
        decision = "llm_unconfirmed"
    else:
        decision = original
    relevance = {
        **(record.get("computation_relevance") or {}),
        "decision": decision,
        "used_llm": True,
        "rule_decision": original,
        "llm_decision": performed,
        "article_role": review["article_role"],
    }
    return {
        **record,
        "computation_relevance": relevance,
        "llm_computation_review": {
            "status": (
                "completed"
                if confirmed or performed == "no"
                else "strict_rejected"
                if strict
                else "uncertain_rule_fallback"
            ),
            **review,
            "prompt_version": PROMPT_VERSION,
            "request_hash": request_hash,
            "cache_path": str(cache_path),
            "cache_hit": cache_hit,
            "duration_seconds": audit.get("duration_seconds"),
            "usage": audit.get("usage") or {},
            "model_returned": audit.get("model_returned"),
        },
        "pipeline_routing": {
            "stage_03": decision,
            "continue": decision in {"strong_candidate", "weak_candidate", "rule_error"},
            "stop_reason": (
                None
                if decision in {"strong_candidate", "weak_candidate", "rule_error"}
                else "llm_confirmation_required"
                if decision == "llm_unconfirmed"
                else "no_computation_evidence"
            ),
        },
    }


def _needs_review(record: dict[str, Any], config: dict[str, Any]) -> bool:
    relevance = record.get("computation_relevance") or {}
    decision = relevance.get("decision")
    role = relevance.get("article_role")
    if bool(config.get("review_all_candidates", config.get("strict", False))):
        return decision in {"strong_candidate", "weak_candidate", "rule_error"}
    if decision == "rule_error":
        return True
    if role in {"review", "perspective", "unknown_nonresearch"}:
        return True
    if decision == "weak_candidate":
        return True
    if decision == "not_computational":
        return bool(relevance.get("method_families")) or float(relevance.get("score") or 0) >= 2
    return False


def _service_ready(config: dict[str, Any]) -> bool:
    request = urllib.request.Request(
        f"{str(config['base_url']).rstrip('/')}/models",
        headers={"Authorization": f"Bearer {config.get('api_key') or 'EMPTY'}"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=float(config.get("health_timeout_seconds", 15))
        ) as response:
            return response.status == 200
    except Exception as exc:
        pipeline_logger().warning("STAGE03 LLM health check failed: %s", exc)
        return False


def _not_requested(record: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        **record,
        "llm_computation_review": {"status": "not_requested", "reason": reason},
    }


def _fallback(
    record: dict[str, Any], error: str, *, strict: bool = False
) -> dict[str, Any]:
    if strict:
        original = str((record.get("computation_relevance") or {}).get("decision"))
        return {
            **record,
            "computation_relevance": {
                **(record.get("computation_relevance") or {}),
                "decision": "llm_unconfirmed",
                "rule_decision": original,
                "used_llm": False,
            },
            "llm_computation_review": {
                "status": "rule_fallback",
                "error": error,
                "prompt_version": PROMPT_VERSION,
            },
            "pipeline_routing": {
                "stage_03": "llm_unconfirmed",
                "continue": False,
                "stop_reason": "llm_confirmation_required",
            },
        }
    return {
        **record,
        "llm_computation_review": {
            "status": "rule_fallback",
            "error": error,
            "prompt_version": PROMPT_VERSION,
        },
    }


def _opening_excerpt(record: dict[str, Any], limit: int) -> str:
    for document in record.get("main_documents") or []:
        path = document.get("text_path")
        if path and Path(path).is_file():
            text = Path(path).read_text(encoding="utf-8", errors="replace")
            return " ".join(text[:limit].split())
    return ""


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


__all__ = ["PROMPT_VERSION", "apply_llm_review", "build_review_prompt"]

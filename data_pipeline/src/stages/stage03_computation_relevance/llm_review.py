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

PROMPT_VERSION = "stage03-pure-computation-review-v2"
SYSTEM_PROMPT = """You screen scientific papers for computational chemistry work.
Decide whether THIS paper is a pure computational chemistry study, rather than an experimental study with
supporting calculations. A pure computational study may compare against experiments reported by other papers,
but the authors of THIS paper must not synthesize, fabricate, measure, assay, characterize, or otherwise perform
new laboratory experiments for the reported study.
Do not count calculations only cited from earlier work, generic method background, experimental arithmetic,
data plotting, or software mentioned without use. Reviews and perspectives pass only when their authors report
new computations performed in this paper. Extract every named program, package, workflow engine, and custom code
that the authors actually use to produce or analyze the central computational results. Do not list theories,
functionals, basis sets, databases, plotting-only tools, or software mentioned only as comparison/background.
Use only the supplied excerpts. Return one JSON object and no prose with exactly these fields:
performed_computation: yes, no, or uncertain;
article_role: original_research, review, correction, editorial, or unknown;
computation_role: primary, supporting, background_only, or none;
study_mode: pure_computational, mixed_computational_experimental, experimental_with_computational_support,
noncomputational, or uncertain;
author_performed_experiments: yes, no, or uncertain;
method_families: array of strings;
required_software: array of objects with name, purpose, excerpt_id, and quote;
software_inventory_complete: yes, no, or uncertain;
author_execution_evidence: array of objects with excerpt_id, quote, and reason;
author_experiment_evidence: array of objects with excerpt_id, quote, and reason;
confidence: number from 0 to 1;
reason: short string.
For yes, quote at least one supplied excerpt that attributes execution to this paper's authors. If the evidence
does not establish the executing authors, return uncertain rather than guessing. Mark software_inventory_complete
yes only when the supplied excerpts identify all software needed for the central computational workflow."""

_EXPERIMENT_PATTERNS = (
    r"\bexperimental\s+(?:section|details?|methods?|procedures?)\b",
    r"\b(?:synthesis|synthesized|synthesised|fabricat(?:ed|ion)|prepared)\b",
    r"\b(?:measur(?:ed|ement)|characteri[sz](?:ed|ation)|spectroscop(?:y|ic))\b",
    r"\b(?:assay|cell\s+culture|in\s+vitro|in\s+vivo|electrochemical\s+(?:test|measurement))\b",
    r"\b(?:flow|batch|fixed[- ]bed)\s+reactor\b",
)
_SOFTWARE_PATTERNS = (
    r"\b(?:software|program|package|code|implementation|workflow)\b",
    r"\b(?:calculations?|simulations?)\b.{0,100}\b(?:using|with|via|implemented\s+in)\b",
    r"\b(?:using|with|via|implemented\s+in)\b.{0,100}\b(?:calculations?|simulations?)\b",
)


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
    _append_targeted_excerpts(
        record,
        excerpts,
        source_map,
        patterns=_EXPERIMENT_PATTERNS,
        prefix="x",
        evidence_type="possible_author_experiment",
        limit=10,
    )
    _append_targeted_excerpts(
        record,
        excerpts,
        source_map,
        patterns=_SOFTWARE_PATTERNS,
        prefix="s",
        evidence_type="possible_workflow_software",
        limit=12,
    )
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
    max_tokens = int(config.get("max_tokens", 2048))
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
        "study_mode",
        "author_performed_experiments",
        "method_families",
        "required_software",
        "software_inventory_complete",
        "author_execution_evidence",
        "author_experiment_evidence",
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
    study_mode = str(value.get("study_mode") or "uncertain").casefold()
    if study_mode not in {
        "pure_computational",
        "mixed_computational_experimental",
        "experimental_with_computational_support",
        "noncomputational",
        "uncertain",
    }:
        study_mode = "uncertain"
    experiments = str(value.get("author_performed_experiments") or "uncertain").casefold()
    if experiments not in {"yes", "no", "uncertain"}:
        experiments = "uncertain"
    inventory_complete = str(value.get("software_inventory_complete") or "uncertain").casefold()
    if inventory_complete not in {"yes", "no", "uncertain"}:
        inventory_complete = "uncertain"
    verified = _verified_evidence(value.get("author_execution_evidence"), source_map)
    experiment_evidence = _verified_evidence(
        value.get("author_experiment_evidence"), source_map
    )
    required_software: list[dict[str, str]] = []
    for raw in value.get("required_software") or []:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name") or "").strip()
        excerpt_id = str(raw.get("excerpt_id") or "")
        quote = str(raw.get("quote") or "").strip()
        source = source_map.get(excerpt_id, "")
        if (
            name
            and len(_normalize(quote)) >= 12
            and _normalize(quote) in _normalize(source)
        ):
            required_software.append(
                {
                    "name": name[:200],
                    "purpose": str(raw.get("purpose") or "")[:500],
                    "excerpt_id": excerpt_id,
                    "quote": quote,
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
        "study_mode": study_mode,
        "author_performed_experiments": experiments,
        "method_families": [str(item) for item in value.get("method_families") or []][:20],
        "required_software": required_software[:30],
        "software_inventory_complete": inventory_complete,
        "author_execution_evidence": verified,
        "author_experiment_evidence": experiment_evidence,
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
        config.get("allowed_computation_roles")
        or (["primary"] if strict else ["primary", "supporting"])
    )
    required_study_modes = set(
        config.get("required_study_modes")
        or (["pure_computational"] if strict else [review["study_mode"]])
    )
    allowed_experiment_values = set(
        config.get("allowed_author_performed_experiments")
        or (["no"] if strict else ["yes", "no", "uncertain"])
    )
    confirmed = (
        performed == "yes"
        and review["confidence"] >= minimum_confidence
        and review["article_role"] in allowed_article_roles
        and review["computation_role"] in allowed_computation_roles
        and review["study_mode"] in required_study_modes
        and review["author_performed_experiments"] in allowed_experiment_values
        and bool(review["author_execution_evidence"])
    )
    if confirmed:
        decision = "strong_candidate" if review["confidence"] >= 0.7 else "weak_candidate"
    elif performed == "no":
        decision = "not_computational"
    elif (
        review["study_mode"]
        in {"mixed_computational_experimental", "experimental_with_computational_support"}
        and review["author_performed_experiments"] == "yes"
    ):
        decision = "not_pure_computational"
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
        "study_mode": review["study_mode"],
        "computation_role": review["computation_role"],
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
                else "mixed_or_experimental_study"
                if decision == "not_pure_computational"
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


def _append_targeted_excerpts(
    record: dict[str, Any],
    excerpts: list[dict[str, Any]],
    source_map: dict[str, str],
    *,
    patterns: tuple[str, ...],
    prefix: str,
    evidence_type: str,
    limit: int,
) -> None:
    combined = re.compile("|".join(f"(?:{pattern})" for pattern in patterns), re.I)
    seen: set[str] = set()
    count = 0
    documents = [
        *(record.get("main_documents") or []),
        *(record.get("supplementary_documents") or []),
    ]
    for document in documents:
        path = document.get("text_path")
        if not path or not Path(path).is_file():
            continue
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        for match in combined.finditer(text):
            start = max(0, match.start() - 280)
            end = min(len(text), match.end() + 420)
            snippet = " ".join(text[start:end].split())
            key = _normalize(snippet)
            if len(key) < 40 or key in seen:
                continue
            seen.add(key)
            count += 1
            excerpt_id = f"{prefix}{count:03d}"
            value = {
                "excerpt_id": excerpt_id,
                "document_role": document.get("document_role"),
                "section": evidence_type,
                "evidence_type": evidence_type,
                "text": snippet[:700],
            }
            excerpts.append(value)
            source_map[excerpt_id] = str(value["text"])
            if count >= limit:
                return


def _verified_evidence(
    values: Any, source_map: dict[str, str]
) -> list[dict[str, str]]:
    verified: list[dict[str, str]] = []
    for raw in values or []:
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
    return verified


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


__all__ = ["PROMPT_VERSION", "apply_llm_review", "build_review_prompt"]

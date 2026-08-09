from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.core.concurrency import ordered_parallel_map
from src.v2.contracts import decision_counts, read_jsonl, record_header, write_json, write_jsonl
from src.v2.model_client import RoleModelClient
from src.v2.prompts import (
    STAGE03_MAP_SYSTEM,
    STAGE03_MAP_VERSION,
    STAGE03_REDUCE_SYSTEM,
    STAGE03_REDUCE_VERSION,
)

COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION = "v2-stage02-computational-content-20260810-r3-domain-boundaries"
STAGE03_IMPLEMENTATION_VERSION = COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION

DECISIONS = {
    "computational_content_confirmed",
    "not_pure_computational",
    "computational_content_not_found",
    "background_only",
    "non_original_article",
    "uncertain",
}


def run_computational_content_screening(
    *,
    papers: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    model: RoleModelClient,
    workspace: Path,
    run_id: str,
) -> dict[str, Any]:
    stage_root = workspace / "stage_02_computational_content"
    document_by_id = {row["document_id"]: row for row in documents if row.get("decision") == "pass"}
    eligible = [row for row in papers if _is_stage03_eligible(row)]

    def review(
        paper: dict[str, Any],
    ) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
        try:
            source_blocks = [
                block
                for document_id in paper.get("document_ids") or []
                if document_id in document_by_id
                for block in read_jsonl(document_by_id[document_id]["content_blocks_path"])
            ]
            article_guard = _non_original_article_guard(paper, source_blocks)
            if article_guard:
                record = {
                    **record_header(run_id=run_id, stage="stage02", paper_id=paper["paper_id"]),
                    "title": paper.get("title"),
                    "doi": paper.get("doi"),
                    "journal_name": paper.get("journal_name"),
                    "article_url": paper.get("article_url"),
                    "processing_status": "completed",
                    "decision": "non_original_article",
                    "passed": False,
                    "review": article_guard,
                    "validated_evidence": [],
                    "validated_author_experiment_evidence": [],
                    "skipped_nonsemantic_blocks": 0,
                    "reduce_validation_warnings": [],
                    "model_audit": {"model_called": False, "deterministic_guard": True},
                }
                return record, [], []
            blocks = [block for block in source_blocks if not _is_atomic_coordinate_dump(block)]
            skipped_nonsemantic_blocks = len(source_blocks) - len(blocks)
            chunks, skipped_coordinate_segments = _chunks_with_stats(
                blocks,
                int(
                    config.get(
                        "chunk_payload_bytes",
                        config.get("chunk_bytes", config.get("chunk_characters", 9000)),
                    )
                ),
            )
            skipped_nonsemantic_blocks += skipped_coordinate_segments
            chunk_reviews: list[dict[str, Any]] = []
            validated_evidence: list[dict[str, Any]] = []
            deterministic_experiments = _find_deterministic_author_experiments(blocks)
            validated_experiments: list[dict[str, Any]] = list(deterministic_experiments)
            for index, chunk in enumerate(chunks):
                payload = {
                    "paper_id": paper["paper_id"],
                    "paper_metadata": _paper_metadata(paper),
                    "chunk_index": index,
                    "blocks": chunk,
                }
                response, audit = _call_complete_json(
                    model,
                    namespace="stage03_map",
                    record_id=f"{paper['paper_id']}-{index:04d}",
                    prompt_version=STAGE03_MAP_VERSION,
                    system_prompt=STAGE03_MAP_SYSTEM,
                    user_content=json.dumps(payload, ensure_ascii=False),
                    max_tokens=int(config.get("map_max_tokens", 2048)),
                )
                evidence = _validate_map(response, chunk)
                experiments = _validate_experiment_map(
                    response.get("author_experiment_evidence"), chunk
                )
                validated_evidence.extend(evidence)
                validated_experiments.extend(experiments)
                chunk_reviews.append(
                    {
                        "paper_id": paper["paper_id"],
                        "chunk_index": index,
                        "response": response,
                        "validated_evidence": evidence,
                        "validated_experiments": experiments,
                        "model_audit": audit,
                    }
                )
            validated_experiments = _deduplicate_quoted_evidence(validated_experiments)
            reduce_payload = {
                "paper_id": paper["paper_id"],
                "paper_metadata": _paper_metadata(paper),
                "validated_computational_evidence": _reduce_evidence_packet(
                    validated_evidence,
                    max_items=int(config.get("reduce_max_evidence", 12)),
                    max_quote_characters=int(config.get("reduce_max_quote_characters", 300)),
                ),
                "validated_author_experiment_evidence": _reduce_experiment_packet(
                    validated_experiments,
                    max_items=int(config.get("reduce_max_experiment_evidence", 12)),
                    max_quote_characters=int(config.get("reduce_max_quote_characters", 300)),
                ),
                "chunk_summaries": [_compact_chunk_review(item) for item in chunk_reviews],
            }
            response, audit = _call_complete_json(
                model,
                namespace="stage03_reduce",
                record_id=paper["paper_id"],
                prompt_version=STAGE03_REDUCE_VERSION,
                system_prompt=STAGE03_REDUCE_SYSTEM,
                user_content=json.dumps(reduce_payload, ensure_ascii=False),
                max_tokens=int(config.get("reduce_max_tokens", 2048)),
            )
            valid_ids = {item["evidence_id"] for item in validated_evidence}
            experiment_ids = {item["evidence_id"] for item in validated_experiments}
            response, reduce_warnings = _sanitize_reduce_response(
                response,
                valid_ids,
                experiment_ids=experiment_ids,
                strict_pure=bool(config.get("strict_pure_computational", True)),
                minimum_confidence=float(config.get("minimum_confidence", 0.75)),
            )
            decision = str(response.get("decision") or "uncertain")
            if decision not in DECISIONS:
                raise ValueError(f"invalid Stage03 decision: {decision}")
            for retry in range(int(config.get("uncertain_retries", 1))):
                if decision != "uncertain":
                    break
                response, audit = _call_complete_json(
                    model,
                    namespace="stage03_reduce_retry",
                    record_id=f"{paper['paper_id']}-retry-{retry + 1}",
                    prompt_version=STAGE03_REDUCE_VERSION,
                    system_prompt=STAGE03_REDUCE_SYSTEM,
                    user_content=json.dumps(
                        {
                            **reduce_payload,
                            "review_instruction": (
                                "The previous adjudication or deterministic evidence audit was uncertain. "
                                "Recheck whether any quote proves physical laboratory work by the current "
                                "authors. Simulations, calculated spectra, external structures, and comparison "
                                "to existing experimental data are not author laboratory experiments."
                            ),
                        },
                        ensure_ascii=False,
                    ),
                    max_tokens=int(config.get("reduce_max_tokens", 2048)),
                )
                response, retry_warnings = _sanitize_reduce_response(
                    response,
                    valid_ids,
                    experiment_ids=experiment_ids,
                    strict_pure=bool(config.get("strict_pure_computational", True)),
                    minimum_confidence=float(config.get("minimum_confidence", 0.75)),
                )
                reduce_warnings.extend(retry_warnings)
                decision = str(response.get("decision") or "uncertain")
                if decision not in DECISIONS:
                    raise ValueError(f"invalid Stage03 retry decision: {decision}")
            decision = str(response.get("decision") or "uncertain")
            record = {
                **record_header(run_id=run_id, stage="stage02", paper_id=paper["paper_id"]),
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "journal_name": paper.get("journal_name"),
                "article_url": paper.get("article_url"),
                "processing_status": "completed",
                "decision": decision,
                "passed": decision == "computational_content_confirmed",
                "review": response,
                "validated_evidence": validated_evidence,
                "validated_author_experiment_evidence": validated_experiments,
                "skipped_nonsemantic_blocks": skipped_nonsemantic_blocks,
                "reduce_validation_warnings": reduce_warnings,
                "model_audit": audit,
            }
            return record, chunk_reviews, []
        except Exception as exc:
            error = {
                "paper_id": paper["paper_id"],
                "error_type": type(exc).__name__,
                "message": str(exc),
            }
            record = {
                **record_header(run_id=run_id, stage="stage02", paper_id=paper["paper_id"]),
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "journal_name": paper.get("journal_name"),
                "article_url": paper.get("article_url"),
                "processing_status": "failed",
                "decision": "processing_failed",
                "passed": False,
                "error": error,
            }
            return record, [], [error]

    reviewed = ordered_parallel_map(
        review, eligible, max_workers=int(config.get("workers", model.config.get("workers", 1)))
    )
    records = [item[0] for item in reviewed]
    chunk_rows = [row for item in reviewed for row in item[1]]
    errors = [row for item in reviewed for row in item[2]]
    write_jsonl(stage_root / "decisions.jsonl", records)
    write_jsonl(stage_root / "chunk_reviews.jsonl", chunk_rows)
    write_jsonl(stage_root / "processing_errors.jsonl", errors)
    write_jsonl(
        stage_root / "rejected.jsonl",
        [
            row
            for row in records
            if row["decision"]
            in {
                "not_pure_computational",
                "computational_content_not_found",
                "background_only",
                "non_original_article",
            }
        ],
    )
    write_jsonl(
        stage_root / "held.jsonl",
        [row for row in records if row["decision"] in {"uncertain", "processing_failed"}],
    )
    summary = {
        **record_header(run_id=run_id, stage="stage02"),
        "input_papers": len(papers),
        "eligible_papers": len(eligible),
        "ineligible_papers": len(papers) - len(eligible),
        "papers": len(records),
        "decisions": decision_counts(records),
        "passed": sum(row["passed"] for row in records),
        "processing_errors": len(errors),
        "model_role": model.role,
        "model": model.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _is_stage03_eligible(paper: dict[str, Any]) -> bool:
    """Reject legacy Stage02 rows that passed with only a subset of known SI parsed."""
    if paper.get("decision") != "pass" or paper.get("main_parse_ok") is not True:
        return False
    if paper.get("partial_si_parse", False):
        return False
    if paper.get("package_status") == "complete_with_si":
        return paper.get("supplementary_parse_ok") is True
    return paper.get("supplementary_parse_ok") is not False


_NON_ORIGINAL_TITLE_RE = re.compile(
    r"^\s*(?P<role>correction|corrigendum|erratum|retraction|editorial|commentary)\b",
    re.IGNORECASE,
)
_NON_ORIGINAL_TEXT_PATTERNS = (
    (
        "review",
        re.compile(
            r"\b(?:in|for)\s+this\s+(?:brief\s+|short\s+)?review\b|"
            r"\bthis\s+review\s+(?:summarizes|surveys|discusses|covers|highlights)\b|"
            r"\bwe\s+(?:herein\s+)?highlight\s+the\s+advances\s+that\s+have\s+been\s+made\b",
            re.IGNORECASE,
        ),
    ),
    (
        "perspective",
        re.compile(
            r"\bin\s+this\s+perspective\b|"
            r"\bthis\s+perspective\s+(?:explores|discusses|summarizes|highlights)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "commentary",
        re.compile(
            r"\b(?:[A-Z][A-Za-z-]+(?:,\s*[A-Z][A-Za-z-]+)*,?\s+and\s+)?"
            r"colleagues\s+report\s+in\s+(?:Nature|Science|Cell|Chem)\b|"
            r"\brecently\s+in\s+(?:the\s+)?Journal\s+of\s+the\s+American\s+Chemical\s+Society,"
            r".{0,240}\b(?:co-?workers?|colleagues)\s+reported\b|"
            r"\bthis\s+commentary\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
)


def _paper_metadata(paper: dict[str, Any]) -> dict[str, Any]:
    return {
        key: paper.get(key)
        for key in ("title", "doi", "journal_name", "article_url")
        if paper.get(key)
    }


def _non_original_article_guard(
    paper: dict[str, Any], blocks: list[dict[str, Any]]
) -> dict[str, Any] | None:
    title = str(paper.get("title") or "").strip()
    title_match = _NON_ORIGINAL_TITLE_RE.search(title)
    if title_match:
        role = title_match.group("role").casefold()
        return _non_original_review(role, title, "title")

    front_text = "\n".join(str(block.get("text") or "") for block in blocks[:8])[:12000]
    for role, pattern in _NON_ORIGINAL_TEXT_PATTERNS:
        match = pattern.search(front_text)
        if match:
            return _non_original_review(role, match.group(0), "front_matter")
    return None


def _non_original_review(role: str, quote: str, source: str) -> dict[str, Any]:
    normalized_role = "editorial" if role in {"editorial", "commentary"} else role
    return {
        "decision": "non_original_article",
        "article_role": normalized_role,
        "performed_computation": "uncertain",
        "computation_role": "background_only",
        "study_mode": "noncomputational",
        "author_performed_experiments": "uncertain",
        "workflow_complete": "no",
        "method_families": [],
        "computational_actions": [],
        "software_clues": [],
        "resource_clues": [],
        "evidence_ids": [],
        "experimental_evidence_ids": [],
        "conflicting_evidence_ids": [],
        "article_type_evidence": {"source": source, "exact_quote": quote[:500]},
        "rationale": f"Deterministic article-type guard identified a {role} article.",
        "confidence": "high",
    }


_DETERMINISTIC_LAB_ACTION_RE = re.compile(
    r"\b(?:experiments?|measurements?)\s+(?:were|was)\s+"
    r"(?:performed|conducted|carried\s+out)|"
    r"\b(?:spectra|images?|micrographs?)\s+(?:were|was)\s+"
    r"(?:recorded|measured|acquired|collected)|"
    r"\bwe\s+(?:synthesi[sz]ed|prepared|fabricated|purified|isolated|grew|measured|"
    r"recorded|acquired|collected|characteri[sz]ed|tested|assayed|irradiated)\b|"
    r"\bin\s+this\s+study,?\s+we\s+combine\b.{0,180}\bexperimental\s+methods?\b",
    re.IGNORECASE,
)
_SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")


def _find_deterministic_author_experiments(
    blocks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Recall explicit current-author laboratory work independently of the LLM."""

    output: list[dict[str, Any]] = []
    for block in blocks:
        text = str(block.get("text") or "")
        sentences = _SENTENCE_BOUNDARY_RE.split(" ".join(text.split()))
        for index, sentence in enumerate(sentences):
            quote = sentence.strip()
            if not quote or not _DETERMINISTIC_LAB_ACTION_RE.search(quote):
                continue
            attribution_context = " ".join(sentences[max(0, index - 2) : index + 1])
            if _EXTERNAL_EXPERIMENT_RE.search(attribution_context):
                continue
            if not _LABORATORY_TECHNIQUE_RE.search(quote):
                continue
            item = {
                "evidence_id": str(block.get("evidence_id") or ""),
                "exact_quote": quote[:500],
                "experiment_type": "physical laboratory measurement or preparation",
                "attribution": "this_paper",
                "confidence": "high",
                "source": "deterministic_full_text_scan",
            }
            if _is_explicit_author_laboratory_evidence(item):
                output.append(item)
    return _deduplicate_quoted_evidence(output)


def _deduplicate_quoted_evidence(
    values: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in values:
        key = (str(item.get("evidence_id") or ""), str(item.get("exact_quote") or ""))
        if not all(key) or key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def _chunks(blocks: list[dict[str, Any]], limit: int) -> list[list[dict[str, Any]]]:
    chunks, _skipped = _chunks_with_stats(blocks, limit)
    return chunks


def _chunks_with_stats(
    blocks: list[dict[str, Any]], limit: int
) -> tuple[list[list[dict[str, Any]]], int]:
    if limit < 1:
        raise ValueError("Stage03 chunk character limit must be positive")
    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    size = 0
    skipped_coordinate_segments = 0
    for block in blocks:
        compact = {
            key: block.get(key)
            for key in ("evidence_id", "document_id", "page", "section_path", "block_type", "text")
        }
        text = str(compact.get("text") or "")
        segments = _split_text_by_utf8_bytes(text, limit)
        for segment_index, segment in enumerate(segments):
            if _is_atomic_coordinate_dump({"text": segment}):
                segment = _strip_atomic_coordinate_sequences(segment)
                skipped_coordinate_segments += 1
                if len(segment.split()) < 4:
                    continue
            segmented = {
                **compact,
                "text": segment,
                "segment_index": segment_index,
                "segment_count": len(segments),
            }
            block_size = len(
                json.dumps(segmented, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            )
            if current and size + block_size > limit:
                chunks.append(current)
                current, size = [], 0
            current.append(segmented)
            size += block_size
    if current:
        chunks.append(current)
    return chunks, skipped_coordinate_segments


def _call_complete_json(
    model: RoleModelClient,
    *,
    namespace: str,
    record_id: str,
    prompt_version: str,
    system_prompt: str,
    user_content: str,
    max_tokens: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    response, audit = model.call_json(
        namespace=namespace,
        record_id=record_id,
        prompt_version=prompt_version,
        system_prompt=system_prompt,
        user_content=user_content,
        max_tokens=max_tokens,
    )
    if audit.get("finish_reason") != "length":
        return response, audit

    retry_response, retry_audit = model.call_json(
        namespace=f"{namespace}_complete_retry",
        record_id=f"{record_id}-complete-retry",
        prompt_version=f"{prompt_version}-complete-retry-v1",
        system_prompt=(
            f"{system_prompt}\nThe previous response was truncated. Return a complete, compact JSON "
            "object. Use at most two items in every evidence array and shorten non-quote strings."
        ),
        user_content=user_content,
        max_tokens=max(max_tokens, 3072),
    )
    if retry_audit.get("finish_reason") == "length":
        retry_response, final_audit = model.call_json(
            namespace=f"{namespace}_essential_retry",
            record_id=f"{record_id}-essential-retry",
            prompt_version=f"{prompt_version}-essential-retry-v1",
            system_prompt=(
                "Extract only decisive evidence from the supplied paper chunk. Return compact JSON "
                "with keys has_computational_evidence, evidence, author_experiment_evidence, "
                "background_only_evidence, conflicts. Evidence may contain at most one computation "
                "item and one physical laboratory item. A laboratory item requires real samples and "
                "physical work by this paper's authors; DFT, MD, simulations, calculated spectra, "
                "external structures, and existing databases are not laboratory work. Copy one exact "
                "quote of at most 160 characters per item. Use empty arrays when absent. Return only "
                "one complete JSON object."
            ),
            user_content=user_content,
            max_tokens=max(max_tokens, 3072),
        )
        if final_audit.get("finish_reason") == "length":
            raise ValueError(f"{namespace} response remained truncated after essential retry")
        retry_audit = {
            **final_audit,
            "truncation_retry_count": 2,
        }
    return retry_response, {
        **retry_audit,
        "truncation_retry": True,
        "truncation_retry_count": retry_audit.get("truncation_retry_count", 1),
        "initial_finish_reason": "length",
        "initial_request_hash": audit.get("request_hash"),
    }


def _split_text_by_utf8_bytes(text: str, limit: int) -> list[str]:
    if not text:
        return [""]
    segments: list[str] = []
    current: list[str] = []
    size = 0
    for character in text:
        character_size = len(character.encode("utf-8"))
        if current and size + character_size > limit:
            segments.append("".join(current))
            current, size = [], 0
        current.append(character)
        size += character_size
    if current:
        segments.append("".join(current))
    return segments


_NUMBER_TOKEN_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?$")
_ATOM_TOKEN_RE = re.compile(r"^(?:[A-Z][a-z]?|[A-Z][a-z]?\d+)$")
_COORDINATE_NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?"
_ATOMIC_COORDINATE_RUN_RE = re.compile(
    rf"(?:\b[A-Z][a-z]?\s+{_COORDINATE_NUMBER}\s+{_COORDINATE_NUMBER}\s+"
    rf"{_COORDINATE_NUMBER}(?:\s+|$)){{12,}}"
)


def _is_atomic_coordinate_dump(block: dict[str, Any]) -> bool:
    text = str(block.get("text") or "")
    if len(text) < 500:
        return False
    tokens = text.split()
    if len(tokens) < 80:
        return False
    numeric = sum(bool(_NUMBER_TOKEN_RE.fullmatch(token.rstrip(",;"))) for token in tokens)
    if numeric / len(tokens) < 0.65:
        return False
    labels = [
        token.rstrip(",;:")
        for token in tokens
        if not _NUMBER_TOKEN_RE.fullmatch(token.rstrip(",;"))
    ]
    if not labels:
        return False
    atom_labels = sum(bool(_ATOM_TOKEN_RE.fullmatch(token)) for token in labels)
    return atom_labels / len(labels) >= 0.8


def _strip_atomic_coordinate_sequences(text: str) -> str:
    return " ".join(_ATOMIC_COORDINATE_RUN_RE.sub(" ", text).split())


def _reduce_evidence_packet(
    evidence: list[dict[str, Any]],
    *,
    max_items: int,
    max_quote_characters: int,
) -> list[dict[str, Any]]:
    confidence_order = {"high": 0, "medium": 1, "low": 2}
    ranked = sorted(
        enumerate(evidence),
        key=lambda pair: (
            confidence_order.get(str(pair[1].get("confidence") or "low"), 3),
            pair[0],
        ),
    )
    selected = [item for _index, item in ranked[: max(1, max_items)]]
    return [
        {
            "evidence_id": item.get("evidence_id"),
            "exact_quote": str(item.get("exact_quote") or "")[: max(1, max_quote_characters)],
            "method_family": str(item.get("method_family") or "")[:120],
            "action": str(item.get("action") or "")[:240],
            "software_clues": _compact_string_list(item.get("software_clues"), 8, 80),
            "result_clues": _compact_string_list(item.get("result_clues"), 4, 120),
            "confidence": item.get("confidence"),
        }
        for item in selected
    ]


def _reduce_experiment_packet(
    evidence: list[dict[str, Any]],
    *,
    max_items: int,
    max_quote_characters: int,
) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": item.get("evidence_id"),
            "exact_quote": str(item.get("exact_quote") or "")[: max(1, max_quote_characters)],
            "experiment_type": str(item.get("experiment_type") or "")[:120],
            "attribution": str(item.get("attribution") or "unclear")[:40],
            "confidence": item.get("confidence"),
        }
        for item in evidence[: max(1, max_items)]
    ]


def _compact_string_list(value: Any, max_items: int, max_characters: int) -> list[str]:
    if isinstance(value, list):
        values = value
    elif value is None or value == "":
        values = []
    else:
        values = [value]
    return [str(item)[:max_characters] for item in values[:max_items]]


def _compact_chunk_review(review: dict[str, Any]) -> dict[str, Any]:
    response = review.get("response") or {}
    return {
        "chunk_index": review.get("chunk_index"),
        "has_computational_evidence": bool(response.get("has_computational_evidence")),
        "validated_evidence_count": len(review.get("validated_evidence") or []),
        "validated_experiment_count": len(review.get("validated_experiments") or []),
        "background_only_count": len(response.get("background_only_evidence") or []),
        "conflict_count": len(response.get("conflicts") or []),
    }


def _sanitize_reduce_response(
    response: dict[str, Any],
    valid_ids: set[str],
    *,
    experiment_ids: set[str] | None = None,
    strict_pure: bool = False,
    minimum_confidence: float = 0.75,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sanitized = dict(response)
    warnings: list[dict[str, Any]] = []
    experiment_ids = experiment_ids or set()
    id_fields = {
        "evidence_ids": valid_ids,
        "experimental_evidence_ids": experiment_ids,
        "conflicting_evidence_ids": valid_ids | experiment_ids,
    }
    for field, allowed_ids in id_fields.items():
        raw = response.get(field) or []
        values = raw if isinstance(raw, list) else []
        known = _deduplicate([str(item) for item in values if str(item) in allowed_ids], 24)
        unknown = [str(item) for item in values if str(item) not in allowed_ids]
        sanitized[field] = known
        if unknown:
            warnings.append({"field": field, "reason": "unknown_evidence_ids", "values": unknown})
    for field in (
        "method_families",
        "computational_actions",
        "software_clues",
        "resource_clues",
    ):
        sanitized[field] = _deduplicate_string_values(response.get(field), 24, 160)

    if (
        sanitized.get("decision") == "computational_content_confirmed"
        and not sanitized["evidence_ids"]
    ):
        sanitized["decision"] = "uncertain"
        sanitized["confidence"] = "low"
        warnings.append(
            {
                "field": "decision",
                "reason": "confirmed_without_validated_evidence_downgraded",
            }
        )
    actual_computation = sanitized.get("performed_computation") == "yes"
    if actual_computation and _lacks_target_chemistry_computation(sanitized):
        sanitized["performed_computation"] = "no"
        sanitized["computation_role"] = "none"
        sanitized["study_mode"] = "noncomputational"
        sanitized["workflow_complete"] = "no"
        actual_computation = False
        warnings.append(
            {
                "field": "performed_computation",
                "reason": "target_computational_chemistry_evidence_missing",
            }
        )
    verified_author_experiments = bool(experiment_ids)
    if not actual_computation:
        if sanitized.get("decision") in {
            "computational_content_confirmed",
            "not_pure_computational",
        }:
            sanitized["decision"] = "computational_content_not_found"
            sanitized["computation_role"] = "none"
            sanitized["study_mode"] = "noncomputational"
            sanitized["workflow_complete"] = "no"
            warnings.append(
                {
                    "field": "decision",
                    "reason": "noncomputational_record_normalized",
                }
            )
    elif verified_author_experiments:
        sanitized["author_performed_experiments"] = "yes"
        sanitized["study_mode"] = (
            "mixed_computational_experimental"
            if sanitized.get("computation_role") == "primary"
            else "experimental_with_computational_support"
        )
        if strict_pure:
            sanitized["decision"] = "not_pure_computational"
            warnings.append(
                {
                    "field": "decision",
                    "reason": "verified_author_laboratory_evidence_rejects_pure_computation",
                }
            )
    elif sanitized.get("author_performed_experiments") == "yes" or (
        actual_computation
        and (
            sanitized.get("decision") == "not_pure_computational"
            or sanitized.get("study_mode")
            in {"mixed_computational_experimental", "experimental_with_computational_support"}
        )
    ):
        sanitized["author_performed_experiments"] = "uncertain"
        sanitized["study_mode"] = "uncertain"
        sanitized["decision"] = "uncertain"
        warnings.append(
            {
                "field": "author_performed_experiments",
                "reason": "author_experiment_claim_without_verified_laboratory_evidence",
            }
        )
    if strict_pure and sanitized.get("decision") == "computational_content_confirmed":
        confidence = _confidence_number(sanitized.get("confidence"))
        strict_requirements = {
            "article_role": sanitized.get("article_role") == "original_research",
            "performed_computation": sanitized.get("performed_computation") == "yes",
            "computation_role": sanitized.get("computation_role") == "primary",
            "study_mode": sanitized.get("study_mode") == "pure_computational",
            "author_performed_experiments": sanitized.get("author_performed_experiments") == "no",
            "workflow_complete": sanitized.get("workflow_complete") == "yes",
            "minimum_confidence": confidence >= minimum_confidence,
            "no_validated_author_experiment_evidence": not experiment_ids,
        }
        failed = [name for name, passed in strict_requirements.items() if not passed]
        if failed:
            mixed_or_supporting = (
                sanitized.get("study_mode")
                in {
                    "mixed_computational_experimental",
                    "experimental_with_computational_support",
                }
                or sanitized.get("computation_role") == "supporting"
            )
            sanitized["decision"] = (
                "not_pure_computational"
                if actual_computation and mixed_or_supporting
                else "uncertain"
            )
            warnings.append(
                {
                    "field": "decision",
                    "reason": "strict_pure_computational_requirements_failed",
                    "requirements": failed,
                }
            )
    return sanitized, warnings


def _deduplicate(values: list[str], max_items: int) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.strip().casefold()
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(value.strip())
        if len(output) >= max_items:
            break
    return output


def _deduplicate_string_values(value: Any, max_items: int, max_characters: int) -> list[str]:
    values = value if isinstance(value, list) else ([] if value in (None, "") else [value])
    return _deduplicate([str(item)[:max_characters] for item in values], max_items)


def _confidence_number(value: Any) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    mapping = {"high": 0.9, "medium": 0.6, "low": 0.3}
    return mapping.get(str(value or "").casefold(), 0.0)


_TARGET_CHEMISTRY_COMPUTATION_RE = re.compile(
    r"\b(?:dft|density functional|ab initio|quantum chem|electronic structure|"
    r"molecular dynamics|atomistic simulation|\bmd\b|qm/mm|monte carlo(?!\s+tree)|"
    r"force field|phonon|vibrational calculation|thermal transport|transition state|"
    r"reaction path|reaction dynamics|quantum dynamics|quasi[- ]classical traject|"
    r"potential energy surface|free[- ]energy|metadynamics|umbrella sampling|"
    r"microkinetic|kinetic model|master equation|rrkm|rate constant|molecular docking|"
    r"tight[- ]binding|wave function|coupled cluster|excited state|tddft|"
    r"thermochemistry|conformer|energy decomposition|electron density|qtaim|bader|"
    r"high[- ]pressure phase|phase stability)\b",
    re.IGNORECASE,
)


def _lacks_target_chemistry_computation(response: dict[str, Any]) -> bool:
    """Require a positive computational-chemistry workflow, independent of product names."""

    descriptors = [
        *(response.get("method_families") or []),
        *(response.get("computational_actions") or []),
        *(response.get("software_clues") or []),
    ]
    text = re.sub(r"[_-]+", " ", " ".join(str(item) for item in descriptors)).strip()
    if not text:
        return False
    return not bool(_TARGET_CHEMISTRY_COMPUTATION_RE.search(text))


def _validate_map(response: dict[str, Any], blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in _validate_quoted_items(response.get("evidence"), blocks)
        if str(item.get("attribution") or "").casefold() == "this_paper"
    ]


def _validate_experiment_map(value: Any, blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in _validate_quoted_items(value, blocks)
        if str(item.get("attribution") or "").casefold() == "this_paper"
        and _is_explicit_author_laboratory_evidence(item)
        and not _has_external_experiment_context(item, blocks)
    ]


def _has_external_experiment_context(
    item: dict[str, Any], blocks: list[dict[str, Any]]
) -> bool:
    evidence_id = str(item.get("evidence_id") or "")
    quote = str(item.get("exact_quote") or "")
    for block in blocks:
        if str(block.get("evidence_id") or "") != evidence_id:
            continue
        text = " ".join(str(block.get("text") or "").split())
        index = text.find(quote)
        if index >= 0 and _EXTERNAL_EXPERIMENT_RE.search(text[max(0, index - 500) : index]):
            return True
    return False


_COMPUTATIONAL_OPERATION_RE = re.compile(
    r"\b(?:dft|density functional|ab initio|molecular dynamics|\bmd\b|qm/mm|monte carlo|"
    r"simulation|simulated|computational|calculated|computed|predicted|phonon|trajectory|"
    r"free[- ]energy|machine learning|screening|geometry optimization|transition state|"
    r"electronic structure|model(?:ing|ling)?)\b",
    re.IGNORECASE,
)
_EXTERNAL_EXPERIMENT_RE = re.compile(
    r"\b(?:published|previously reported|previous study|taken from|reported by|et al\.|"
    r"database|pdb(?: id)?|"
    r"coworkers?|colleagues|adapted with permission|existing experimental|reference data|"
    r"starts? from|originates? from|derived from)\b",
    re.IGNORECASE,
)
_LABORATORY_ACTION_RE = re.compile(
    r"\b(?:synthesi[sz](?:e|ed|ing|is)|prepared|fabricated|purified|isolated|grew|grown|"
    r"measur(?:e|ed|ing)|recorded|acquired|collected|characteri[sz](?:e|ed|ing)|tested|"
    r"assayed|incubated|cultured|irradiated|electrodeposited|added|stirred|heated|washed|"
    r"centrifuged|filtered|dried|conducted|carried\s+out|performed\s+(?:an?\s+)?"
    r"(?:experiment|measurement|spectroscop|microscop|diffraction|electrochem)|"
    r"(?:experiments?|measurements?)\s+(?:were|was)\s+"
    r"(?:performed|conducted|carried\s+out)|"
    r"combine(?:d|s|ing)?\b.{0,120}\bexperimental\s+methods?)\b",
    re.IGNORECASE,
)
_LABORATORY_TECHNIQUE_RE = re.compile(
    r"\b(?:synthesis|fabrication|purification|isolation|nmr|spectroscopy|spectrometer|"
    r"microscopy|microscope|diffraction|crystallography|xrd|pxrd|xps|xas|xanes|exafs|"
    r"rixs|raman|ftir|infrared|epr|esr|mass spectrometry|hrms|chromatography|hplc|gc-ms|"
    r"calorimetry|scattering|langmuir|voltammetry|electrochemistry|electrochemical|"
    r"battery|assay|cell culture|microscopy|"
    r"catalytic activity|reaction screening|substrate scope|physical testing)\b",
    re.IGNORECASE,
)
_STRONG_LABORATORY_TYPE_RE = re.compile(
    r"\b(?:synthesis|fabrication|purification|isolation|nmr|spectroscopy|microscopy|"
    r"xps|xas|xanes|exafs|rixs|raman|ftir|infrared|epr|esr|mass spectrometry|hrms|"
    r"chromatography|hplc|gc-ms|calorimetry|scattering|langmuir|voltammetry|"
    r"electrochemistry|electrochemical|battery|"
    r"assay|cell culture|magnetometry|magnetization measurement|catalytic activity|"
    r"reaction screening|substrate scope|physical testing)\b",
    re.IGNORECASE,
)


def _is_explicit_author_laboratory_evidence(item: dict[str, Any]) -> bool:
    experiment_type = str(item.get("experiment_type") or "")
    quote = str(item.get("exact_quote") or "")
    combined = f"{experiment_type} {quote}"
    if _EXTERNAL_EXPERIMENT_RE.search(quote):
        return False
    explicit_action = bool(_LABORATORY_ACTION_RE.search(quote))
    laboratory_context = bool(_LABORATORY_TECHNIQUE_RE.search(combined))
    if _COMPUTATIONAL_OPERATION_RE.search(combined) and not _LABORATORY_ACTION_RE.search(quote):
        return False
    return explicit_action and laboratory_context


def _validate_quoted_items(value: Any, blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source = {str(block["evidence_id"]): str(block.get("text") or "") for block in blocks}
    output = []
    evidence = value or []
    if not isinstance(evidence, list):
        return output
    for item in evidence:
        if not isinstance(item, dict):
            continue
        evidence_id = str(item.get("evidence_id") or "")
        quote = str(item.get("exact_quote") or "").strip()
        if evidence_id in source and quote and quote in source[evidence_id]:
            output.append(item)
    return output

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9+.\-]{2,}", re.I)


def assess_deep_parse_quality(
    documents: list[dict[str, Any]],
    results: list[dict[str, Any]],
    *,
    min_title_recall: float = 0.7,
    min_grobid_vocab_recall: float = 0.65,
    min_key_term_coverage: float = 0.5,
    min_length_ratio: float = 0.25,
    max_length_ratio: float = 2.5,
) -> list[dict[str, Any]]:
    document_map = {item["paper_id"]: item for item in documents}
    output: list[dict[str, Any]] = []
    for result in results:
        record = dict(result)
        document = document_map.get(result["paper_id"], {})
        quality = _assess_one(
            document,
            result,
            min_title_recall=min_title_recall,
            min_grobid_vocab_recall=min_grobid_vocab_recall,
            min_key_term_coverage=min_key_term_coverage,
            min_length_ratio=min_length_ratio,
            max_length_ratio=max_length_ratio,
        )
        record["deep_parse_quality"] = quality
        output.append(record)
    return output


def deep_quality_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "documents": len(results),
        "passed": sum(
            1 for item in results if (item.get("deep_parse_quality") or {}).get("passed")
        ),
        "failed": sum(
            1 for item in results if not (item.get("deep_parse_quality") or {}).get("passed")
        ),
        "fallback_to_grobid_text": [
            item["paper_id"]
            for item in results
            if not (item.get("deep_parse_quality") or {}).get("passed")
        ],
    }


def _assess_one(
    document: dict[str, Any],
    result: dict[str, Any],
    **thresholds: float,
) -> dict[str, Any]:
    markdown_path = result.get("markdown_path")
    grobid_path = document.get("text_path")
    markdown = _read_text(markdown_path)
    grobid_text = _read_text(grobid_path)
    markdown_tokens = _tokens(markdown)
    grobid_tokens = _tokens(grobid_text)
    title_tokens = _tokens(document.get("title", ""))
    has_grobid_text = len(grobid_text) >= 1000

    title_recall = _recall(title_tokens, markdown_tokens)
    grobid_vocab_recall = _recall(grobid_tokens, markdown_tokens)
    length_ratio = len(markdown) / max(1, len(grobid_text))
    classification = document.get("corpus_classification") or {}
    key_terms = classification.get("software", []) + classification.get("methods", [])
    normalized_markdown = _normalize_phrase(markdown)
    matched_terms = [term for term in key_terms if _normalize_phrase(term) in normalized_markdown]
    key_term_coverage = len(matched_terms) / max(1, len(key_terms)) if key_terms else 1.0
    expected_pages = document.get("page_count")
    parsed_pages = result.get("structured_pages")

    checks = {
        "mineru_status": result.get("status") in {"success", "reused"},
        "output_valid": bool(result.get("valid")),
        "page_count": expected_pages is None or parsed_pages == expected_pages,
        "title_recall": title_recall >= thresholds["min_title_recall"],
        "grobid_vocab_recall": (
            not has_grobid_text or grobid_vocab_recall >= thresholds["min_grobid_vocab_recall"]
        ),
        "key_term_coverage": key_term_coverage >= thresholds["min_key_term_coverage"],
        "length_ratio": (
            not has_grobid_text
            or (thresholds["min_length_ratio"] <= length_ratio <= thresholds["max_length_ratio"])
        ),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    return {
        "passed": not failed_checks,
        "failed_checks": failed_checks,
        "metrics": {
            "expected_pages": expected_pages,
            "parsed_pages": parsed_pages,
            "markdown_characters": len(markdown),
            "grobid_text_characters": len(grobid_text),
            "grobid_text_available": has_grobid_text,
            "length_ratio": round(length_ratio, 3),
            "title_recall": round(title_recall, 3),
            "grobid_vocab_recall": round(grobid_vocab_recall, 3),
            "key_term_coverage": round(key_term_coverage, 3),
            "matched_key_terms": matched_terms,
            "expected_key_terms": key_terms,
        },
        "checks": checks,
        "fallback": "none" if not failed_checks else "grobid_text",
    }


def _read_text(value: str | None) -> str:
    if not value:
        return ""
    path = Path(value)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _tokens(value: str) -> set[str]:
    return {token.casefold() for token in TOKEN_PATTERN.findall(value)}


def _recall(expected: set[str], observed: set[str]) -> float:
    if not expected:
        return 1.0
    return len(expected & observed) / len(expected)


def _normalize_phrase(value: str) -> str:
    return re.sub(r"[^a-z0-9+]+", " ", value.casefold()).strip()

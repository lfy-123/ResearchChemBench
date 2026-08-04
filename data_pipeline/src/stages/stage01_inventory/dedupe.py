from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from src.core.io import normalize_title, stable_id


def deduplicate(
    records: list[dict[str, Any]], fuzzy_threshold: float = 0.97
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    doi_index: dict[str, int] = {}
    title_index: dict[str, int] = {}

    for record in records:
        doi = _normalize_doi(record.get("doi"))
        title_key = normalize_title(record.get("title", ""))
        match = doi_index.get(doi) if doi else None
        if match is None:
            match = title_index.get(title_key)
        if match is None and title_key:
            match = _fuzzy_match(title_key, groups, fuzzy_threshold)

        if match is None:
            merged = dict(record)
            merged["paper_id"] = merged.get("paper_id") or stable_id("paper", doi or "", title_key)
            merged["doi"] = doi or None
            merged["query_ids"] = _as_unique_list(record.get("query_ids"), record.get("query_id"))
            merged["seed_ids"] = _as_unique_list(record.get("seed_ids"), record.get("seed_id"))
            merged["query_tiers"] = _as_unique_list(
                record.get("query_tiers"), record.get("query_tier")
            )
            merged["retrieval_sources"] = _as_unique_list(
                record.get("retrieval_sources"), record.get("retrieval_source")
            )
            for transient in ("query_id", "seed_id", "query_tier", "retrieval_source"):
                merged.pop(transient, None)
            groups.append(merged)
            match = len(groups) - 1
        else:
            groups[match] = _merge(groups[match], record)

        if doi:
            doi_index[doi] = match
        if title_key:
            title_index[title_key] = match

    return groups


def _merge(base: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for field in ("abstract", "url", "pdf_url", "venue", "year", "authors", "open_access"):
        if not merged.get(field) and record.get(field):
            merged[field] = record[field]
    merged["query_ids"] = _as_unique_list(merged.get("query_ids"), record.get("query_id"))
    merged["seed_ids"] = _as_unique_list(
        merged.get("seed_ids"), *(record.get("seed_ids") or []), record.get("seed_id")
    )
    merged["query_tiers"] = _as_unique_list(merged.get("query_tiers"), record.get("query_tier"))
    merged["retrieval_sources"] = _as_unique_list(
        merged.get("retrieval_sources"), record.get("retrieval_source")
    )
    scores = [
        score
        for score in (merged.get("retrieval_score"), record.get("retrieval_score"))
        if score is not None
    ]
    if scores:
        merged["retrieval_score"] = max(scores)
    return merged


def _fuzzy_match(title_key: str, groups: list[dict[str, Any]], threshold: float) -> int | None:
    for index, group in enumerate(groups):
        existing = normalize_title(group.get("title", ""))
        if existing and SequenceMatcher(None, title_key, existing).ratio() >= threshold:
            return index
    return None


def _normalize_doi(value: Any) -> str:
    if not value:
        return ""
    return str(value).casefold().strip().removeprefix("https://doi.org/").removeprefix("doi:")


def _as_unique_list(existing: Any, *values: Any) -> list[Any]:
    output: list[Any] = []
    if isinstance(existing, list):
        output.extend(existing)
    elif existing:
        output.append(existing)
    for value in values:
        if value is None:
            continue
        if isinstance(value, list):
            output.extend(value)
        else:
            output.append(value)
    return list(dict.fromkeys(output))

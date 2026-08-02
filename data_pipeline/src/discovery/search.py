from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from typing import Any

from src.core.io import normalize_title, stable_id

OPENALEX_URL = "https://api.openalex.org/works"


def search_openalex(
    queries: list[dict[str, Any]],
    per_query: int = 20,
    mailto: str | None = None,
    delay_seconds: float = 0.1,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for query in queries:
        params = {
            "search": query["query"],
            "per-page": str(per_query),
            "select": (
                "id,doi,title,display_name,publication_year,publication_date,"
                "authorships,primary_location,open_access,best_oa_location,"
                "abstract_inverted_index,cited_by_count,type"
            ),
        }
        if mailto:
            params["mailto"] = mailto
        url = f"{OPENALEX_URL}?{urllib.parse.urlencode(params)}"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": f"ResearchChemBench/0.1 ({mailto or 'no-email'})"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
        for work in payload.get("results", []):
            records.append(_openalex_record(work, query))
        if delay_seconds:
            time.sleep(delay_seconds)
    return records


def search_offline(
    queries: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    min_overlap: float = 0.08,
    per_query: int = 50,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for query in queries:
        scored: list[tuple[float, dict[str, Any]]] = []
        for candidate in candidates:
            declared = set(candidate.get("seed_ids", []))
            if declared and query["seed_id"] not in declared:
                continue
            text = f"{candidate.get('title', '')} {candidate.get('abstract', '')}"
            score = token_overlap(query["query"], text)
            if score >= min_overlap or query["seed_id"] in declared:
                scored.append((score, candidate))
        for score, candidate in sorted(scored, key=lambda item: item[0], reverse=True)[:per_query]:
            record = dict(candidate)
            record.setdefault(
                "paper_id",
                stable_id("paper", record.get("doi", ""), record.get("title", "")),
            )
            record["query_id"] = query["query_id"]
            record["seed_id"] = query["seed_id"]
            record["query_tier"] = query["tier"]
            record["retrieval_score"] = round(score, 4)
            record["retrieval_source"] = "offline"
            output.append(record)
    return output


def token_overlap(query: str, document: str) -> float:
    query_tokens = set(normalize_title(query).split())
    document_tokens = set(normalize_title(document).split())
    if not query_tokens:
        return 0.0
    return len(query_tokens & document_tokens) / len(query_tokens)


def _openalex_record(work: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    title = work.get("display_name") or work.get("title") or "Untitled"
    authors = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        if author.get("display_name"):
            authors.append(author["display_name"])
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    best_oa = work.get("best_oa_location") or {}
    return {
        "paper_id": stable_id("paper", work.get("id", ""), work.get("doi", ""), title),
        "external_ids": {"openalex": work.get("id")},
        "doi": (work.get("doi") or "").removeprefix("https://doi.org/") or None,
        "title": title,
        "abstract": _reconstruct_abstract(work.get("abstract_inverted_index")),
        "authors": authors,
        "year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "venue": source.get("display_name"),
        "url": best_oa.get("landing_page_url") or primary_location.get("landing_page_url"),
        "pdf_url": best_oa.get("pdf_url"),
        "open_access": work.get("open_access") or {},
        "cited_by_count": work.get("cited_by_count", 0),
        "work_type": work.get("type"),
        "query_id": query["query_id"],
        "seed_id": query["seed_id"],
        "query_tier": query["tier"],
        "retrieval_source": "openalex",
        "retrieval_score": None,
    }


def _reconstruct_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positions: dict[int, str] = {}
    for word, offsets in index.items():
        for offset in offsets:
            positions[offset] = word
    return " ".join(positions[position] for position in sorted(positions))


def retrieval_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_source: dict[str, int] = defaultdict(int)
    by_tier: dict[str, int] = defaultdict(int)
    for record in records:
        by_source[record.get("retrieval_source", "unknown")] += 1
        by_tier[record.get("query_tier", "unknown")] += 1
    return {
        "retrieved_rows": len(records),
        "by_source": dict(sorted(by_source.items())),
        "by_query_tier": dict(sorted(by_tier.items())),
    }

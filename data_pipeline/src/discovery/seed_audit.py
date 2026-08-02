from __future__ import annotations

from collections import Counter
from typing import Any

from src.core.io import normalize_title


def audit_seed_coverage(
    documents: list[dict[str, Any]],
    seeds: list[dict[str, Any]],
    match_threshold: float = 0.12,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    seed_profiles = {seed["seed_id"]: _seed_profile(seed) for seed in seeds}
    enriched: list[dict[str, Any]] = []
    seed_counts = Counter()
    uncovered_domains = Counter()
    uncovered_software = Counter()

    for document in documents:
        classification = document.get("corpus_classification") or {}
        document_tokens = set(
            normalize_title(
                " ".join(
                    [
                        document.get("title", ""),
                        document.get("abstract", ""),
                        " ".join(classification.get("domains", [])),
                        " ".join(classification.get("methods", [])),
                        " ".join(classification.get("software", [])),
                    ]
                )
            ).split()
        )
        matches = []
        relevance_decision = classification.get("relevance_decision")
        for seed_id, profile in seed_profiles.items():
            overlap = document_tokens & profile["all_tokens"]
            anchor_overlap = document_tokens & profile["anchor_tokens"]
            score = len(overlap) / max(1, len(profile["all_tokens"]))
            if relevance_decision != "reject" and anchor_overlap and score >= match_threshold:
                matches.append({"seed_id": seed_id, "score": round(score, 3)})
                seed_counts[seed_id] += 1
        matches.sort(key=lambda item: item["score"], reverse=True)
        record = dict(document)
        record["seed_guidance"] = {
            "matches": matches,
            "coverage_role": (
                "out_of_scope"
                if relevance_decision == "reject"
                else "covered"
                if matches
                else "new_capability_candidate"
            ),
        }
        if not matches and classification.get("relevance_decision") == "pass":
            uncovered_domains.update(classification.get("domains", []))
            uncovered_software.update(classification.get("software", []))
        enriched.append(record)

    summary = {
        "seed_count": len(seeds),
        "covered_documents": sum(1 for item in enriched if item["seed_guidance"]["matches"]),
        "new_capability_documents": sum(
            1
            for item in enriched
            if item["seed_guidance"]["coverage_role"] == "new_capability_candidate"
            and (item.get("corpus_classification") or {}).get("relevance_decision") == "pass"
        ),
        "documents_per_seed": dict(seed_counts),
        "uncovered_domains": dict(uncovered_domains),
        "uncovered_software": dict(uncovered_software),
    }
    return enriched, summary


def _seed_profile(seed: dict[str, Any]) -> dict[str, set[str]]:
    facets = seed.get("facets", {})
    parts = [seed.get("title", ""), seed.get("scientific_objective", "")]
    for key in ("phenomena", "systems", "methods", "evidence"):
        value = facets.get(key, [])
        parts.extend(value if isinstance(value, list) else [str(value)])
    anchor_parts = [seed.get("title", "")]
    for key in ("phenomena", "systems"):
        value = facets.get(key, [])
        anchor_parts.extend(value if isinstance(value, list) else [str(value)])
    stopwords = {
        "a",
        "an",
        "and",
        "as",
        "by",
        "for",
        "from",
        "in",
        "of",
        "on",
        "or",
        "the",
        "to",
        "using",
        "with",
        "calculation",
        "calculations",
        "chemistry",
        "computation",
        "computational",
        "discover",
        "mechanism",
        "reaction",
        "study",
    }
    all_tokens = set(normalize_title(" ".join(parts)).split()) - stopwords
    anchor_tokens = set(normalize_title(" ".join(anchor_parts)).split()) - stopwords
    return {"all_tokens": all_tokens, "anchor_tokens": anchor_tokens}

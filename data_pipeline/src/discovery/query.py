from __future__ import annotations

from itertools import product
from typing import Any

from src.core.io import stable_id
from src.core.models import QUERY_TIERS, normalize_task_type, validate_seed

MODE_TERMS = {
    "paper_reproduction": (
        "computational reproducibility",
        "supporting information calculations",
        "open data computational chemistry",
    ),
    "conclusion_guided_reconstruction": (
        "computational conclusion verification",
        "independent mechanistic validation",
        "evidence-based reconstruction",
    ),
    "autonomous_research": (
        "computational chemistry workflow",
        "multi-method computational study",
        "mechanistic investigation",
    ),
    "mechanistic_rule_discovery": (
        "reaction mechanism",
        "descriptor relationship",
        "held-out prediction",
    ),
}


def expand_seed(seed: dict[str, Any], max_per_tier: int = 12) -> list[dict[str, Any]]:
    errors = validate_seed(seed)
    if errors:
        raise ValueError(f"Invalid seed {seed.get('seed_id', '<unknown>')}: {'; '.join(errors)}")

    facets = seed["facets"]
    phenomena = _values(facets, "phenomena") or [seed["scientific_objective"]]
    systems = _values(facets, "systems") or [""]
    methods = _values(facets, "methods") or ["computational chemistry"]
    evidence = _values(facets, "evidence") or ["quantitative evidence"]
    exclusions = [item.casefold() for item in _values(facets, "exclude_terms")]

    generated: dict[str, list[str]] = {tier: [] for tier in QUERY_TIERS}
    for phenomenon, system in product(phenomena, systems):
        generated["broad"].append(_join(phenomenon, system))

    for phenomenon, system, method in product(phenomena, systems, methods):
        generated["medium"].append(_join(phenomenon, system, method))

    normalized_modes = [normalize_task_type(mode) for mode in seed["task_modes"]]
    mode_terms = [term for mode in normalized_modes if mode for term in MODE_TERMS[mode]]
    for phenomenon, system, method, signal in product(
        phenomena, systems, methods, evidence + mode_terms
    ):
        generated["narrow"].append(_join(phenomenon, system, method, signal))

    records: list[dict[str, Any]] = []
    for tier in QUERY_TIERS:
        seen: set[str] = set()
        for query in generated[tier]:
            key = query.casefold()
            if not query or key in seen or any(term in key for term in exclusions):
                continue
            seen.add(key)
            records.append(
                {
                    "query_id": stable_id("qry", seed["seed_id"], tier, query),
                    "seed_id": seed["seed_id"],
                    "tier": tier,
                    "query": query,
                    "task_modes": [mode for mode in normalized_modes if mode],
                    "scientific_objective": seed["scientific_objective"],
                    "provenance": {"generator": "src.discovery.query.expand_seed"},
                }
            )
            if len(seen) >= max_per_tier:
                break
    return records


def expand_seeds(seeds: list[dict[str, Any]], max_per_tier: int = 12) -> list[dict[str, Any]]:
    return [record for seed in seeds for record in expand_seed(seed, max_per_tier)]


def _values(facets: dict[str, Any], key: str) -> list[str]:
    value = facets.get(key, [])
    if isinstance(value, str):
        value = [value]
    return [str(item).strip() for item in value if str(item).strip()]


def _join(*parts: str) -> str:
    return " ".join(part.strip() for part in parts if part.strip())

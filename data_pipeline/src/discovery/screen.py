from __future__ import annotations

from typing import Any

from src.core.models import normalize_task_type
from src.discovery.search import token_overlap

CHEMISTRY_TERMS = {
    "reaction",
    "molecule",
    "molecular",
    "catalyst",
    "catalytic",
    "chemical",
    "chemistry",
    "energy",
    "transition state",
    "dft",
    "density functional",
    "molecular dynamics",
    "spectroscopy",
    "solvent",
    "free energy",
    "mechanism",
    "conformer",
    "quantum",
    "kinetic",
    "thermodynamic",
    "excited state",
}

MODE_TERMS = {
    "paper_reproduction": {
        "dataset",
        "code",
        "supporting information",
        "repository",
        "benchmark",
        "calculation",
        "simulation",
        "method",
        "protocol",
    },
    "conclusion_guided_reconstruction": {
        "conclusion",
        "validation",
        "evidence",
        "comparison",
        "verification",
        "calculation",
        "mechanism",
    },
    "autonomous_research": {
        "investigate",
        "discover",
        "screening",
        "prediction",
        "optimization",
        "workflow",
        "multi-scale",
        "multiscale",
        "simulation",
        "mechanism",
    },
    "mechanistic_rule_discovery": {
        "mechanism",
        "pathway",
        "transition state",
        "intermediate",
        "radical",
        "descriptor",
        "correlation",
        "trend",
        "held-out",
        "prediction",
    },
}


def screen_papers(
    papers: list[dict[str, Any]],
    seeds: list[dict[str, Any]],
    threshold: float = 35.0,
) -> list[dict[str, Any]]:
    seed_map = {seed["seed_id"]: seed for seed in seeds}
    output: list[dict[str, Any]] = []
    for paper in papers:
        text = f"{paper.get('title', '')}. {paper.get('abstract', '')}".casefold()
        seed_scores = []
        requested_modes: set[str] = set()
        for seed_id in paper.get("seed_ids", []):
            seed = seed_map.get(seed_id)
            if not seed:
                continue
            seed_scores.append(token_overlap(seed["scientific_objective"], text))
            requested_modes.update(
                normalized
                for value in seed.get("task_modes", [])
                if (normalized := normalize_task_type(value))
            )
        relevance = max(seed_scores or [0.0])
        chemistry_hits = _count_hits(text, CHEMISTRY_TERMS)
        chemistry_score = min(1.0, chemistry_hits / 4)
        metadata_score = (
            sum(1 for field in ("title", "abstract", "year", "authors", "url") if paper.get(field))
            / 5
        )
        access_score = (
            1.0 if paper.get("pdf_url") or (paper.get("open_access") or {}).get("is_oa") else 0.35
        )

        mode_scores: dict[str, float] = {}
        eligible_modes: list[str] = []
        for mode in sorted(requested_modes):
            signal = min(1.0, _count_hits(text, MODE_TERMS[mode]) / 3)
            score = 100 * (
                0.25 * relevance + 0.25 * chemistry_score + 0.35 * signal + 0.15 * metadata_score
            )
            mode_scores[mode] = round(score, 1)
            if score >= threshold:
                eligible_modes.append(mode)

        overall = max(mode_scores.values(), default=100 * (0.5 * relevance + 0.5 * chemistry_score))
        hard_failures = []
        if chemistry_hits == 0:
            hard_failures.append("no computational chemistry signal in title or abstract")
        if not paper.get("title"):
            hard_failures.append("missing title")
        decision = "pass" if eligible_modes and not hard_failures else "review"
        output.append(
            {
                **paper,
                "screening": {
                    "decision": decision,
                    "overall_score": round(overall, 1),
                    "task_type_scores": mode_scores,
                    "eligible_task_types": eligible_modes,
                    "mode_scores": mode_scores,
                    "eligible_modes": eligible_modes,
                    "features": {
                        "seed_relevance": round(relevance, 3),
                        "chemistry_signal": round(chemistry_score, 3),
                        "metadata_completeness": round(metadata_score, 3),
                        "accessibility": round(access_score, 3),
                    },
                    "hard_failures": hard_failures,
                    "review_required": decision != "pass" or access_score < 1,
                },
            }
        )
    return output


def _count_hits(text: str, terms: set[str]) -> int:
    return sum(1 for term in terms if term in text)

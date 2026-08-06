#!/usr/bin/env python3
"""Evaluate Action retrieval with a small versioned English query set."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
for path in (TOOLBOX_ROOT / "src", TOOLBOX_ROOT.parent):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chemistry_toolbox.src.catalog import catalog_snapshot
from chemistry_toolbox.src.discovery import search_actions


DEFAULT_QUERIES = TOOLBOX_ROOT / "config" / "action_search_evaluation.json"


def evaluate(query_path: Path, *, retrieval_mode: str = "hybrid", cutoff: int = 5):
    cases = json.loads(query_path.read_text(encoding="utf-8"))
    snapshot = catalog_snapshot(include_health=False, discovery_mode="progressive")
    rows = []
    for case in cases:
        relevant = set(case["relevant"])
        result = search_actions(
            query=case["query"],
            retrieval_mode=retrieval_mode,
            limit=cutoff,
            snapshot=snapshot,
        )
        ranked = [item["action_id"] for item in result["actions"]]
        hits = [index for index, item in enumerate(ranked, start=1) if item in relevant]
        ideal_length = min(len(relevant), cutoff)
        dcg = sum(1.0 / math.log2(index + 1.0) for index in hits)
        ideal_dcg = sum(1.0 / math.log2(index + 1.0) for index in range(1, ideal_length + 1))
        rows.append(
            {
                "query": case["query"],
                "relevant": sorted(relevant),
                "ranked": ranked,
                "hit_at_1": bool(ranked and ranked[0] in relevant),
                "recall_at_k": len(hits) / len(relevant),
                "precision_at_k": len(hits) / cutoff,
                "reciprocal_rank": 1.0 / hits[0] if hits else 0.0,
                "ndcg_at_k": dcg / ideal_dcg if ideal_dcg else 0.0,
            }
        )
    count = len(rows)
    metrics = {
        "query_count": count,
        "cutoff": cutoff,
        "retrieval_mode": retrieval_mode,
        "hit_at_1": sum(row["hit_at_1"] for row in rows) / count,
        "recall_at_k": sum(row["recall_at_k"] for row in rows) / count,
        "precision_at_k": sum(row["precision_at_k"] for row in rows) / count,
        "mean_reciprocal_rank": sum(row["reciprocal_rank"] for row in rows) / count,
        "ndcg_at_k": sum(row["ndcg_at_k"] for row in rows) / count,
    }
    return {"metrics": metrics, "cases": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--mode", choices=("lexical", "hybrid"), default="hybrid")
    parser.add_argument("--cutoff", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(args.queries, retrieval_mode=args.mode, cutoff=args.cutoff)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result["metrics"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

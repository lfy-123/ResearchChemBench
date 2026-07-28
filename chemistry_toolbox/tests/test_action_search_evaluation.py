from __future__ import annotations

import importlib.util
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = TOOLBOX_ROOT / "scripts" / "evaluate_action_search.py"


def _load_evaluator():
    spec = importlib.util.spec_from_file_location("evaluate_action_search", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_versioned_action_queries_meet_lexical_quality_floor() -> None:
    evaluator = _load_evaluator()
    result = evaluator.evaluate(
        evaluator.DEFAULT_QUERIES, retrieval_mode="lexical", cutoff=5
    )
    metrics = result["metrics"]
    assert metrics["hit_at_1"] >= 0.90
    assert metrics["recall_at_k"] >= 0.95
    assert metrics["mean_reciprocal_rank"] >= 0.95
    assert metrics["ndcg_at_k"] >= 0.95


def test_versioned_action_queries_meet_hybrid_quality_floor() -> None:
    evaluator = _load_evaluator()
    result = evaluator.evaluate(
        evaluator.DEFAULT_QUERIES, retrieval_mode="hybrid", cutoff=5
    )
    metrics = result["metrics"]
    assert metrics["hit_at_1"] >= 0.90
    assert metrics["recall_at_k"] >= 0.95
    assert metrics["mean_reciprocal_rank"] >= 0.95
    assert metrics["ndcg_at_k"] >= 0.95

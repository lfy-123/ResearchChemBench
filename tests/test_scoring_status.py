import json

from evaluation.provenance.results import build_workspace_results, read_scoring_status, write_batch_results
from evaluation.provenance.progress_snapshot import build_progress_snapshot


def test_failed_latest_attempt_preserves_published_score_and_unknown_usage(tmp_path):
    (tmp_path / "_meta.json").write_text('{"status":"completed"}')
    (tmp_path / "_score.json").write_text('{"score":25,"score_max":100,"score_id":"old","normalized_score":0.25}')
    (tmp_path / "_scoring_attempt.json").write_text(json.dumps({"score_id": "new", "status": "needs_review", "error": "budget",
        "submission_status": "valid", "agent_declared_outcome": "task_specific_outcome", "judge_usage": {"total_tokens": None}}))
    result = build_workspace_results(tmp_path)
    assert result["score"]["total"] == 25 and result["score"]["score_id"] == "old"
    assert result["scoring"]["latest_attempt"] == "new" and result["scoring"]["published_score"] == "old"
    assert result["scoring"]["agent_declared_outcome"] == "task_specific_outcome"
    assert result["tokens"]["judge"]["total"] is None and result["tokens"]["combined"]["total"] is None
    assert build_progress_snapshot(tmp_path)["scoring"] == read_scoring_status(tmp_path)
    assert result["run"]["status"] == "completed"


def test_batch_coverage_includes_unscored_and_does_not_invent_zero_usage(tmp_path):
    for name in ("a", "b"):
        root = tmp_path / name
        root.mkdir()
        (root / "_meta.json").write_text('{"status":"completed"}')
    (tmp_path / "a/_score.json").write_text('{"score":0,"normalized_score":0}')
    result = write_batch_results(tmp_path, config={})
    assert result["summary"]["score_coverage"] == {"scored": 1, "total": 2}
    assert result["summary"]["mean_score"] == 0
    assert result["summary"]["agent_tokens"] is None
    assert result["summary"]["unscored_reasons"] == {"not_started": 1}

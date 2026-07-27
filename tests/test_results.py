import json
from pathlib import Path

from evaluation.results import write_workspace_results
from evaluation.run_task import TaskRunner
from evaluation.score import score_workspace


def test_run_results_exist_before_and_after_scoring(tmp_path: Path, monkeypatch):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    meta = runner.run()
    assert meta["status"] == "completed"

    initial = json.loads((runner.workspace / "results.json").read_text())
    assert initial["run"]["status"] == "completed"
    assert initial["agent"]["framework"] == "mock"
    assert initial["score"]["available"] is False
    assert initial["tokens"]["agent"]["available"] is False

    monkeypatch.setattr(
        "evaluation.results.workspace_token_usage",
        lambda _workspace: {
            "model_step_count": 4,
            "session_count": 1,
            "cost": 0.25,
            "tokens": {
                "input": 100,
                "cache_read": 200,
                "cache_write": 10,
                "output": 30,
                "reasoning": 5,
                "total": 345,
            },
        },
    )
    scored = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {"score": 1, "rationale": "correct"},
    )
    assert scored["score"] == 1

    result = json.loads((runner.workspace / "results.json").read_text())
    assert result["score"]["available"] is True
    assert result["score"]["total"] == 1
    assert result["score"]["maximum"] == 1
    assert result["tokens"]["agent"]["tokens"] == {
        "input": 100,
        "cache_read": 200,
        "cache_write": 10,
        "output": 30,
        "reasoning": 5,
        "total": 345,
    }
    assert result["tokens"]["combined"]["total"] == 345
    assert result["tools"]["calls"] == meta["tool_call_count"]


def test_results_can_be_regenerated_from_existing_artifacts(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    (runner.workspace / "results.json").unlink()

    result = write_workspace_results(runner.workspace)

    assert result["task"]["id"] == "ChemGraph_001"
    assert (runner.workspace / "results.json").is_file()

from pathlib import Path

from evaluation.run_task import TaskRunner
from evaluation.score import score_workspace


def test_score_workspace_with_injected_judge(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    meta = runner.run()
    assert meta["status"] == "completed"

    result = score_workspace(
        runner.workspace,
        judge_call=lambda prompt: {
            "score": 1,
            "rationale": "Injected test judge",
        },
    )
    assert result["score"] == 1
    assert result["task_id"] == "ChemGraph_001"
    assert (runner.workspace / "_score.json").is_file()


def test_judge_failure_is_not_counted_as_zero_score(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.run()

    def unavailable(_prompt: str):
        raise RuntimeError("judge unavailable")

    result = score_workspace(runner.workspace, judge_call=unavailable)
    assert result["score"] is None
    assert "error" in result
    assert "judge unavailable" in result["parse_error"]

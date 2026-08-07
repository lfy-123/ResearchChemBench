import json
from pathlib import Path

from evaluation.provenance.results import write_workspace_results
from evaluation.execution.runner import TaskRunner
from evaluation.scoring.service import score_workspace
from evaluation.repository import load_ground_truth


def _full_credit_dual_axis_verdict(task_id: str) -> dict:
    truth = load_ground_truth(task_id)
    return {
        "scientific_conclusions": [
            {
                "id": item["id"],
                "score": item["max_score"],
                "max_score": item["max_score"],
                "evidence_status": "supported",
                "rationale": "correct",
            }
            for item in truth["scientific_conclusion_rubric"]
        ],
        "scientific_conclusion_score": 100,
        "process_criteria": [
            {
                "id": item["id"],
                "score": item["max_score"],
                "max_score": item["max_score"],
                "rationale": "correct",
            }
            for item in truth["scoring_rubric"]
        ],
        "research_process_score": 100,
        "submission_validity": "valid",
        "critical_failures": [],
        "objective_issue_flags": [],
        "rationale": "correct",
    }


def test_run_results_exist_before_and_after_scoring(tmp_path: Path, monkeypatch):
    task_id = "Electron_Isodensity_Reproduction_01_Method_Selection"
    runner = TaskRunner(
        task_id,
        agent_key="mock",
        workspace_root=tmp_path,
        available_cpu_cores=6,
        available_memory_mb=12288,
        available_gpu_count=0,
    )
    meta = runner.run()
    assert meta["status"] == "completed"

    initial = json.loads((runner.workspace / "results.json").read_text())
    assert initial["run"]["status"] == "completed"
    assert initial["agent"]["framework"] == "mock"
    assert initial["score"]["available"] is False
    assert initial["tokens"]["agent"]["available"] is False
    assert initial["run"]["resource_budget"] == {
        "cpu_cores": 6,
        "memory_mb": 12288,
        "gpu_count": 0,
        "source": "evaluation_policy",
        "agent_controllable": False,
        "scope": "per_task",
    }

    monkeypatch.setattr(
        "evaluation.provenance.results.workspace_token_usage",
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
        judge_call=lambda _prompt: _full_credit_dual_axis_verdict(task_id),
    )
    assert scored["score"] == 100

    result = json.loads((runner.workspace / "results.json").read_text())
    assert result["score"]["available"] is True
    assert result["score"]["total"] == 100
    assert result["score"]["maximum"] == 100
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
    assert result["artifacts"]["canonical_tool_trace"] is None


def test_results_can_be_regenerated_from_existing_artifacts(tmp_path: Path):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    (runner.workspace / "results.json").unlink()

    result = write_workspace_results(runner.workspace)

    assert result["task"]["id"] == "Electron_Isodensity_Reproduction_01_Method_Selection"
    assert (runner.workspace / "results.json").is_file()


def test_results_record_canonical_trace_integrity(tmp_path: Path):
    workspace = tmp_path / "run"
    workspace.mkdir()
    (workspace / "_meta.json").write_text(
        json.dumps({"task_id": "Electron_Isodensity_Reproduction_01_Method_Selection", "status": "completed"}),
        encoding="utf-8",
    )
    (workspace / "_tool_trace.jsonl").write_text(
        json.dumps({"tool": "search_actions", "status": "success"}) + "\n",
        encoding="utf-8",
    )

    result = write_workspace_results(workspace)

    trace = result["artifacts"]["canonical_tool_trace"]
    assert trace["path"] == "_tool_trace.jsonl"
    assert trace["event_count"] == 1
    assert trace["invalid_line_count"] == 0
    assert len(trace["sha256"]) == 64


def test_results_expose_process_metrics(tmp_path: Path):
    workspace = tmp_path / "run"
    workspace.mkdir()
    (workspace / "_meta.json").write_text("{}", encoding="utf-8")
    expected = {
        "job_context_compliant_job_count": 2,
        "semantic_search_available_count": 3,
        "discovery_result_bytes": 4096,
    }
    (workspace / "_score.json").write_text(
        json.dumps({"process_metrics": expected}), encoding="utf-8"
    )

    result = write_workspace_results(workspace)

    assert result["process_metrics"] == expected

import json
from pathlib import Path

from evaluation.run_task import TaskRunner
from evaluation.score import RUBRIC_JUDGE_SYSTEM_PROMPT, score_workspace


def test_rubric_judge_prompt_distinguishes_agent_request_errors():
    assert "omitted required fields" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "path outside the workspace" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "malformed tool-call JSON" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "wrong native CLI syntax" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "does not convert the earlier agent-side invalid request" in (
        RUBRIC_JUDGE_SYSTEM_PROMPT
    )
    assert "cross-check it against the explicit fields" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "rate-determining, selectivity-determining" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "internally consistent with critical_failures" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "Built-in shell and file tools" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "never managed scientific execution" in RUBRIC_JUDGE_SYSTEM_PROMPT
    assert "Unrelated successful managed calls cannot launder" in (
        RUBRIC_JUDGE_SYSTEM_PROMPT
    )


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
    history = (runner.workspace / "_score_history.jsonl").read_text().splitlines()
    assert len(history) == 1
    assert json.loads(history[0])["history_source"] == "judge_call"

    second = score_workspace(
        runner.workspace,
        judge_call=lambda prompt: {
            "score": 0,
            "rationale": "Second injected test judge",
        },
    )
    assert second["score"] == 0
    history = (runner.workspace / "_score_history.jsonl").read_text().splitlines()
    assert len(history) == 2
    assert [json.loads(line)["score"] for line in history] == [1, 0]
    progress = (runner.workspace / "_live_progress.log").read_text(encoding="utf-8")
    assert progress.count("[JUDGE_INPUT]") == 2
    assert progress.count("[JUDGE_OUTPUT]") == 2
    assert progress.count("[SCORE_RESULT]") == 2


def test_judge_failure_is_not_counted_as_zero_score(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.run()

    def unavailable(_prompt: str):
        raise RuntimeError("judge unavailable")

    result = score_workspace(runner.workspace, judge_call=unavailable)
    assert result["score"] is None
    assert "error" in result
    assert "judge unavailable" in result["parse_error"]


def test_rubric_score_is_derived_from_clamped_criterion_scores(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    rubric_truth = {
        "expected_tool_calls": [],
        "expected_result": {"answer": "reference"},
        "evaluation_mode": "rubric_100",
        "score_max": 100,
        "scoring_rubric": [
            {"id": "science", "max_score": 60, "criterion": "Scientific result"},
            {"id": "process", "max_score": 40, "criterion": "Scientific process"},
        ],
        "critical_failures": [],
        "judge_instructions": "",
        "reference_evidence": {},
    }
    monkeypatch.setattr("evaluation.score.load_ground_truth", lambda _task_id: rubric_truth)
    native_event = {
        "type": "tool_use",
        "part": {
            "type": "tool",
            "tool": "bash",
            "state": {
                "status": "completed",
                "input": {"command": "python code/analyze.py"},
                "output": "computed barrier = 12.3 kcal/mol",
                "metadata": {"exit": 0},
                "time": {"start": 1000, "end": 2500},
            },
        },
    }
    with runner.output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(native_event) + "\n")
    (runner.workspace / "code" / "analyze.py").write_text(
        "print('independent scientific analysis')\n", encoding="utf-8"
    )

    captured_prompt = ""

    def rubric_judge(prompt: str):
        nonlocal captured_prompt
        captured_prompt = prompt
        return {
            "score": 99,
            "criteria": [
                {"id": "science", "score": 70, "max_score": 60, "rationale": "high"},
                {"id": "process", "score": 25, "max_score": 40, "rationale": "partial"},
            ],
            "critical_failures": [],
            "objective_issue_flags": [],
            "rationale": "Injected rubric judge",
        }

    result = score_workspace(
        runner.workspace,
        judge_call=rubric_judge,
    )

    assert result["score"] == 85
    assert result["score_max"] == 100
    assert result["normalized_score"] == 0.85
    assert [item["score"] for item in result["criteria"]] == [60, 25]
    assert result["judge_consistency_warnings"]
    assert "python code/analyze.py" in captured_prompt
    assert "computed barrier = 12.3 kcal/mol" in captured_prompt
    assert "independent scientific analysis" in captured_prompt
    assert "UNMANAGED native shell/file events" in captured_prompt
    assert '"managed_scientific_evidence": false' in captured_prompt
    assert result["process_metrics"]["native_execution_event_count"] == 1
    assert result["process_metrics"]["successful_native_events"] == 1


def test_managed_computation_policy_caps_narrative_only_rubric_score(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    rubric_truth = {
        "expected_tool_calls": [],
        "expected_result": {"answer": "reference"},
        "evaluation_mode": "rubric_100",
        "score_max": 100,
        "scoring_rubric": [
            {"id": "science", "max_score": 60, "criterion": "Scientific result"},
            {"id": "process", "max_score": 40, "criterion": "Scientific process"},
        ],
        "critical_failures": [],
        "judge_instructions": "",
        "reference_evidence": {},
        "managed_computation_policy": {
            "required": True,
            "minimum_successful_scientific_calls": 2,
            "score_cap_without_managed_attempt": 20,
        },
    }
    monkeypatch.setattr("evaluation.score.load_ground_truth", lambda _task_id: rubric_truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "score": 90,
            "criteria": [
                {"id": "science", "score": 55, "max_score": 60, "rationale": "narrative"},
                {"id": "process", "score": 35, "max_score": 40, "rationale": "narrative"},
            ],
            "critical_failures": [],
            "objective_issue_flags": [],
            "rationale": "No managed computation, despite a plausible report.",
        },
    )

    assert result["score"] == 20
    assert sum(item["score"] for item in result["criteria"]) == 20
    assert result["managed_computation_score_cap"] == 20
    assert result["process_metrics"]["managed_scientific_attempt_count"] == 0


def test_evidence_gate_policy_caps_scientifically_unvalidated_high_score(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    rubric_truth = {
        "expected_tool_calls": [],
        "expected_result": {"answer": "reference"},
        "evaluation_mode": "rubric_100",
        "score_max": 100,
        "scoring_rubric": [
            {"id": "science", "max_score": 60, "criterion": "Scientific result"},
            {"id": "process", "max_score": 40, "criterion": "Scientific process"},
        ],
        "critical_failures": [],
        "judge_instructions": "",
        "reference_evidence": {},
        "evidence_gate_policy": {
            "judge_must_assess_all": True,
            "gates": [
                {
                    "id": "validated_transition_state",
                    "score_cap_if_failed": 55,
                    "requirement": "Exactly one target imaginary mode and connectivity.",
                }
            ],
        },
    }
    monkeypatch.setattr("evaluation.score.load_ground_truth", lambda _task_id: rubric_truth)
    captured_prompt = ""

    def judge(prompt: str):
        nonlocal captured_prompt
        captured_prompt = prompt
        return {
            "score": 95,
            "criteria": [
                {"id": "science", "score": 57, "max_score": 60, "rationale": "high"},
                {"id": "process", "score": 38, "max_score": 40, "rationale": "high"},
            ],
            "critical_failures": [],
            "evidence_gate_failures": ["validated_transition_state"],
            "objective_issue_flags": [],
            "rationale": "A higher-order saddle was overclaimed.",
        }

    result = score_workspace(runner.workspace, judge_call=judge)

    assert result["score"] == 55
    assert sum(item["score"] for item in result["criteria"]) == 55
    assert result["evidence_gate_failures"] == ["validated_transition_state"]
    assert result["evidence_gate_score_cap"] == 55
    assert result["applied_score_cap"] == 55
    assert "Evidence-gate policy" in captured_prompt
    assert "Exactly one target imaginary mode" in captured_prompt

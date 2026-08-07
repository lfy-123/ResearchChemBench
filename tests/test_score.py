import json
from pathlib import Path

from evaluation.execution.runner import TaskRunner
from evaluation.scoring.service import RUBRIC_JUDGE_SYSTEM_PROMPT, score_workspace
from evaluation.repository import load_ground_truth


def _full_credit_dual_axis_verdict(task_id: str, rationale: str) -> dict:
    truth = load_ground_truth(task_id)
    return {
        "scientific_conclusions": [
            {
                "id": item["id"],
                "score": item["max_score"],
                "max_score": item["max_score"],
                "evidence_status": "supported",
                "rationale": rationale,
            }
            for item in truth["scientific_conclusion_rubric"]
        ],
        "scientific_conclusion_score": 100,
        "process_criteria": [
            {
                "id": item["id"],
                "score": item["max_score"],
                "max_score": item["max_score"],
                "rationale": rationale,
            }
            for item in truth["scoring_rubric"]
        ],
        "research_process_score": 100,
        "submission_validity": "valid",
        "critical_failures": [],
        "objective_issue_flags": [],
        "rationale": rationale,
    }


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
    task_id = "Electron_Isodensity_Reproduction_01_Method_Selection"
    runner = TaskRunner(task_id, agent_key="mock", workspace_root=tmp_path)
    meta = runner.run()
    assert meta["status"] == "completed"

    result = score_workspace(
        runner.workspace,
        judge_call=lambda prompt: _full_credit_dual_axis_verdict(
            task_id, "Injected test judge"
        ),
    )
    assert result["score"] == 100
    assert result["task_id"] == task_id
    assert (runner.workspace / "_score.json").is_file()
    history = (runner.workspace / "_score_history.jsonl").read_text().splitlines()
    assert len(history) == 1
    assert json.loads(history[0])["history_source"] == "judge_call"

    zero_verdict = _full_credit_dual_axis_verdict(task_id, "Second injected test judge")
    for key in ("scientific_conclusions", "process_criteria"):
        for item in zero_verdict[key]:
            item["score"] = 0
    zero_verdict["scientific_conclusion_score"] = 0
    zero_verdict["research_process_score"] = 0
    second = score_workspace(runner.workspace, judge_call=lambda prompt: zero_verdict)
    assert second["score"] == 0
    history = (runner.workspace / "_score_history.jsonl").read_text().splitlines()
    assert len(history) == 2
    assert [json.loads(line)["score"] for line in history] == [100, 0]
    progress = (runner.workspace / "_live_progress.log").read_text(encoding="utf-8")
    assert progress.count("[JUDGE_INPUT]") == 2
    assert progress.count("[JUDGE_OUTPUT]") == 2
    assert progress.count("[SCORE_RESULT]") == 2


def test_judge_failure_is_not_counted_as_zero_score(tmp_path: Path):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
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
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
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
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: rubric_truth)
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
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
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
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: rubric_truth)

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
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
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
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: rubric_truth)
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


def test_paper_reproduction_mismatch_cannot_receive_self_awarded_full_score(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    (runner.workspace / "report" / "method_comparison.json").write_text(
        json.dumps({"production_method": {"recovered": False}}),
        encoding="utf-8",
    )
    rubric = [
        {"id": "paper_conclusion_agreement", "max_score": 55},
        {"id": "protocol_fidelity", "max_score": 20},
        {"id": "managed_recomputation", "max_score": 10},
        {"id": "numerical_and_validation_quality", "max_score": 10},
        {"id": "provenance_and_uncertainty", "max_score": 5},
    ]
    truth = {
        "expected_tool_calls": [],
        "expected_result": {"paper_conclusion": "DSD-PBEP86 is best"},
        "evaluation_mode": "rubric_100",
        "evaluation_profile": "paper_reproduction",
        "score_max": 100,
        "scoring_rubric": rubric,
        "critical_failures": [],
        "judge_instructions": "Strict reproduction.",
        "reference_evidence": {},
        "reference_conclusion_gate_policy": {
            "required": True,
            "criterion_id": "paper_conclusion_agreement",
            "score_cap_if_not_matched": 45,
            "max_criterion_score_if_not_matched": 0,
            "structured_match_fields": [
                {
                    "path": "report/method_comparison.json",
                    "field": "production_method.recovered",
                }
            ],
        },
    }
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "score": 100,
            "criteria": [
                {
                    "id": item["id"],
                    "score": item["max_score"],
                    "max_score": item["max_score"],
                    "rationale": "Agent self-reported full reproduction.",
                }
                for item in rubric
            ],
            "critical_failures": [],
            "evidence_gate_failures": [],
            "objective_issue_flags": [],
            "reference_conclusion_status": "matched",
            "rationale": "Incorrectly self-awarded 100.",
        },
    )

    assert result["score"] == 45
    assert result["reference_conclusion_status"] == "not_matched"
    assert result["reference_conclusion_score_cap"] == 45
    assert result["structured_conclusion_mismatches"]
    conclusion = next(
        item
        for item in result["criteria"]
        if item["id"] == "paper_conclusion_agreement"
    )
    assert conclusion["score"] == 0


def test_autonomous_discovery_is_not_capped_for_a_reference_disagreement(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    rubric = [
        {"id": "autonomous_method_and_route_design", "max_score": 50},
        {"id": "defensible_scientific_conclusion", "max_score": 50},
    ]
    truth = {
        "expected_tool_calls": [],
        "expected_result": {"paper_conclusion": "reference differs"},
        "evaluation_mode": "rubric_100",
        "evaluation_profile": "autonomous_discovery",
        "score_max": 100,
        "scoring_rubric": rubric,
        "critical_failures": [],
        "judge_instructions": "Independent discovery.",
        "reference_evidence": {},
        "reference_conclusion_gate_policy": {},
    }
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "score": 100,
            "criteria": [
                {"id": item["id"], "score": 50, "max_score": 50, "rationale": "valid"}
                for item in rubric
            ],
            "critical_failures": [],
            "evidence_gate_failures": [],
            "objective_issue_flags": [],
            "reference_conclusion_status": "not_matched",
            "rationale": "Independent conclusion is well supported.",
        },
    )

    assert result["score"] == 100
    assert result["reference_conclusion_status"] == "not_applicable"
    assert result["reference_conclusion_score_cap"] is None


def test_strict_autonomous_discovery_caps_a_hidden_scientific_outcome_mismatch(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    rubric = [
        {"id": "hidden_scientific_conclusion_recovery", "max_score": 50},
        {"id": "autonomous_method_and_route_design", "max_score": 20},
        {"id": "adaptive_managed_execution", "max_score": 10},
        {"id": "validation_and_falsification", "max_score": 15},
        {"id": "provenance_and_uncertainty", "max_score": 5},
    ]
    truth = {
        "expected_tool_calls": [],
        "expected_result": {
            "scientific_acceptance_contract": {
                "required_findings": ["The refined ranking reverses the low-cost ranking."]
            }
        },
        "evaluation_mode": "rubric_100",
        "evaluation_profile": "autonomous_discovery",
        "score_max": 100,
        "scoring_rubric": rubric,
        "critical_failures": [],
        "judge_instructions": "Strict hidden scientific outcome.",
        "reference_evidence": {},
        "reference_conclusion_gate_policy": {
            "required": True,
            "criterion_id": "hidden_scientific_conclusion_recovery",
            "score_cap_if_not_matched": 40,
            "max_criterion_score_if_not_matched": 0,
        },
    }
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "score": 100,
            "criteria": [
                {
                    "id": item["id"],
                    "score": item["max_score"],
                    "max_score": item["max_score"],
                    "rationale": "The workflow was coherent.",
                }
                for item in rubric
            ],
            "critical_failures": [],
            "evidence_gate_failures": [],
            "objective_issue_flags": [],
            "reference_conclusion_status": "not_matched",
            "rationale": "The independently generated conclusion is opposite to the target.",
        },
    )

    assert result["score"] == 40
    assert result["reference_conclusion_status"] == "not_matched"
    assert result["reference_conclusion_score_cap"] == 40
    conclusion = next(
        item
        for item in result["criteria"]
        if item["id"] == "hidden_scientific_conclusion_recovery"
    )
    assert conclusion["score"] == 0


def test_dual_axis_score_multiplies_conclusion_and_process_scores(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    process_rubric = [
        {"id": "route_design", "max_score": 40},
        {"id": "execution_quality", "max_score": 60},
    ]
    conclusion_rubric = [
        {"id": "claim_a", "max_score": 30, "statement": "Claim A"},
        {"id": "claim_b", "max_score": 70, "statement": "Claim B"},
    ]
    truth = {
        "expected_tool_calls": [],
        "expected_result": {},
        "evaluation_mode": "dual_axis_100",
        "evaluation_profile": "autonomous_discovery",
        "score_max": 100,
        "scoring_rubric": process_rubric,
        "scientific_conclusion_rubric": conclusion_rubric,
        "dual_axis_scoring_policy": {
            "formula": "scientific_conclusion_score * research_process_score / 100"
        },
        "critical_failures": [],
        "judge_instructions": "Dual axis.",
        "reference_evidence": {},
        "managed_computation_policy": {},
        "evidence_gate_policy": {},
        "reference_conclusion_gate_policy": {},
    }
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "scientific_conclusions": [
                {
                    "id": "claim_a",
                    "score": 30,
                    "max_score": 30,
                    "evidence_status": "supported",
                    "rationale": "Recovered.",
                },
                {
                    "id": "claim_b",
                    "score": 30,
                    "max_score": 70,
                    "evidence_status": "partially_supported",
                    "rationale": "Only partial evidence.",
                },
            ],
            "scientific_conclusion_score": 99,
            "process_criteria": [
                {"id": "route_design", "score": 35, "max_score": 40, "rationale": "good"},
                {"id": "execution_quality", "score": 55, "max_score": 60, "rationale": "good"},
            ],
            "research_process_score": 100,
            "submission_validity": "valid",
            "critical_failures": [],
            "objective_issue_flags": [],
            "rationale": "Independent axis evaluation.",
        },
    )

    assert result["scientific_conclusion_score"] == 60
    assert result["research_process_score"] == 90
    assert result["score"] == 54
    assert result["reference_conclusion_score_cap"] is None
    assert result["applied_score_cap"] is None
    assert result["scientific_conclusions"][1]["evidence_status"] == "partially_supported"
    assert any(
        "Replaced inconsistent judge total" in warning
        for warning in result["judge_consistency_warnings"]
    )


def test_dual_axis_invalid_submission_forces_zero_without_task_specific_cap(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    truth = {
        "expected_tool_calls": [],
        "expected_result": {},
        "evaluation_mode": "dual_axis_100",
        "evaluation_profile": "paper_reproduction",
        "score_max": 100,
        "scoring_rubric": [{"id": "process", "max_score": 100}],
        "scientific_conclusion_rubric": [
            {"id": "claim", "max_score": 100, "statement": "Claim"}
        ],
        "dual_axis_scoring_policy": {
            "formula": "scientific_conclusion_score * research_process_score / 100"
        },
        "critical_failures": [],
        "judge_instructions": "Dual axis.",
        "reference_evidence": {},
        "managed_computation_policy": {},
        "evidence_gate_policy": {},
        "reference_conclusion_gate_policy": {},
    }
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "scientific_conclusions": [
                {"id": "claim", "score": 100, "max_score": 100, "evidence_status": "supported", "rationale": "copied"}
            ],
            "process_criteria": [
                {"id": "process", "score": 100, "max_score": 100, "rationale": "copied"}
            ],
            "submission_validity": "invalid_submission",
            "critical_failures": ["hidden answer leakage"],
            "objective_issue_flags": [],
            "rationale": "Reference values were presented as new calculations.",
        },
    )

    assert result["scientific_conclusion_score"] == 100
    assert result["research_process_score"] == 100
    assert result["submission_validity"] == "invalid_submission"
    assert result["score"] == 0


def test_dual_axis_requires_itemized_scores_instead_of_trusting_axis_totals(
    tmp_path: Path, monkeypatch
):
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="mock", workspace_root=tmp_path)
    runner.run()
    truth = {
        "expected_tool_calls": [],
        "expected_result": {},
        "evaluation_mode": "dual_axis_100",
        "evaluation_profile": "autonomous_discovery",
        "score_max": 100,
        "scoring_rubric": [{"id": "process", "max_score": 100}],
        "scientific_conclusion_rubric": [
            {"id": "claim", "max_score": 100, "statement": "Claim"}
        ],
        "dual_axis_scoring_policy": {
            "formula": "scientific_conclusion_score * research_process_score / 100"
        },
        "critical_failures": [],
        "judge_instructions": "Dual axis.",
        "reference_evidence": {},
        "managed_computation_policy": {},
        "evidence_gate_policy": {},
        "reference_conclusion_gate_policy": {},
    }
    monkeypatch.setattr("evaluation.scoring.service.load_ground_truth", lambda _task_id: truth)

    result = score_workspace(
        runner.workspace,
        judge_call=lambda _prompt: {
            "scientific_conclusion_score": 100,
            "research_process_score": 100,
            "submission_validity": "valid",
            "critical_failures": [],
            "objective_issue_flags": [],
            "rationale": "Axis totals without required itemized evidence.",
        },
    )

    assert result["scientific_conclusion_score"] == 0
    assert result["research_process_score"] == 0
    assert result["score"] == 0
    assert len(result["scientific_conclusions"]) == 1
    assert len(result["criteria"]) == 1

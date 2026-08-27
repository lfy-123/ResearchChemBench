from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.agents import AgentExecutionError, AgentRunResult
from src.contracts import write_json
from src.stages.phase_gate import run as run_gate
from src.stages.stage06_task_builder.prompts import final_task_synthesis_instructions
from src.stages.stage06_task_builder.stage import _run_synthesis_agent
from src.stages.stage07_task_judge.prompts import final_task_audit_instructions
from src.stages.stage07_task_judge.validation import external_audit_gate


PAPER_ID = "paper_fixture23"


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _semantic_mode(root: Path, mode: str) -> None:
    directory = root / mode
    _write(directory / "task.md", "# Task\n\nDetermine the supported mechanism.\n")
    _write(directory / "data/inputs/reactant.xyz", "1\nreactant\nH 0 0 0\n")
    _write(
        directory / "task_info.json",
        {
            "paper_id": PAPER_ID,
            "task_type": mode,
            "title": "Mechanism study",
            "category": "reaction_mechanism",
            "paper": {"title": "", "doi": "", "journal": "", "publication_date": ""},
            "data": [{"path": "data/inputs", "description": "Reactant"}],
            "required_deliverables": [
                {"path": "report/results.json", "description": "Evidence and conclusion"}
            ],
        },
    )
    _write(
        directory / "submission_schema.json",
        {
            "required_files": ["report/results.json"],
            "primary_result_file": "report/results.json",
            "result_schema": {
                "type": "object",
                "properties": {
                    "evidence": {"type": "object"},
                    "conclusion": {"type": "object"},
                },
                "required": ["evidence", "conclusion"],
                "additionalProperties": False,
            },
        },
    )
    evaluator = root / "evaluator_reference" / mode
    common = {"paper_id": PAPER_ID}
    _write(
        evaluator / "reference_key_points.json",
        {
            **common,
            "items": [
                {
                    "key_point_id": "kp_evidence",
                    "statement": "The claimed pathway is supported by a connected stationary-point chain.",
                    "expected": "The submitted evidence connects the proposed reactant, saddle, and product.",
                    "evidence_ids": ["ev1"],
                }
            ],
        },
    )
    _write(
        evaluator / "reference_conclusions.json",
        {
            **common,
            "items": [
                {
                    "conclusion_id": "con_mechanism",
                    "statement": "Mechanistic conclusion",
                    "expected": "Path A is supported within the stated search scope.",
                    "supporting_key_point_ids": ["kp_evidence"],
                    "evidence_ids": ["ev1"],
                    "claim_role": "final",
                }
            ],
        },
    )
    _write(
        evaluator / "scoring_rules.json",
        {
            **common,
            "rules": [
                {
                    "rule_id": "rule_evidence",
                    "reference_id": "kp_evidence",
                    "type": "condition",
                    "expected": "A connected and validated stationary-point chain is reported.",
                    "binding": {
                        "artifact_paths": ["report/results.json"],
                        "fields": ["$.evidence"],
                        "comparison": "compare submitted validation evidence",
                    },
                },
                {
                    "rule_id": "rule_conclusion",
                    "reference_id": "con_mechanism",
                    "type": "semantic",
                    "expected": "Path A is supported within the stated scope and limitations.",
                    "binding": {
                        "artifact_paths": ["report/results.json"],
                        "fields": ["$.conclusion", "$.evidence"],
                        "comparison": "compare conclusion and its supporting evidence",
                    },
                },
            ],
        },
    )
    _write(
        evaluator / "evidence_map.json",
        {**common, "evidence": [{"evidence_id": "ev1", "source": "Main article results"}]},
    )
    _write(
        evaluator / "critical_failures.json",
        {**common, "items": [{"id": "cf1", "description": "No validation evidence"}]},
    )


def _semantic_pair(root: Path) -> Path:
    _write(
        root / "workflow_review.json",
        {
            "decision": "candidate_ready",
            "paper_id": PAPER_ID,
            "scientific_core": {"objective": "mechanism"},
            "paper_route": {"scientific_route": "Path A"},
            "input_closure": {"status": "passed", "verified": ["reactant.xyz"]},
        },
    )
    _semantic_mode(root, "paper_reproduction")
    _semantic_mode(root, "autonomous_research")
    return root


def test_semantic_and_condition_only_evaluator_passes_common_gate(tmp_path: Path) -> None:
    root = _semantic_pair(tmp_path)
    self_report = run_gate("synthesis", root)
    external_report = external_audit_gate(root)
    assert self_report["status"] == external_report["status"] == "passed"
    assert self_report["findings"] == external_report["findings"] == []


def test_numeric_binding_must_reach_a_numeric_leaf(tmp_path: Path) -> None:
    root = _semantic_pair(tmp_path)
    mode = "paper_reproduction"
    schema_path = root / mode / "submission_schema.json"
    schema = json.loads(schema_path.read_text())
    schema["result_schema"]["properties"]["values"] = {
        "type": "array",
        "items": {"type": "number"},
    }
    schema["result_schema"]["required"].append("values")
    _write(schema_path, schema)
    rules_path = root / "evaluator_reference" / mode / "scoring_rules.json"
    rules = json.loads(rules_path.read_text())
    rules["rules"][0] = {
        "rule_id": "rule_numeric",
        "reference_id": "kp_evidence",
        "type": "numeric",
        "target": 1.0,
        "unit": "kcal/mol",
        "tolerance": 0.2,
        "binding": {
            "artifact_paths": ["report/results.json"],
            "fields": ["$.values"],
            "comparison": "absolute difference",
        },
    }
    _write(rules_path, rules)
    report = run_gate("synthesis", root, mode=mode)
    assert f"{mode}:numeric_rule_binding_not_numeric_leaf:rule_numeric" in report["findings"]

    rules["rules"][0]["binding"]["fields"] = ["$.values[*]"]
    _write(rules_path, rules)
    report = run_gate("synthesis", root, mode=mode)
    assert report["status"] == "passed"


def test_v23_prompts_define_progress_and_answer_inversion_boundaries() -> None:
    synthesis = final_task_synthesis_instructions(paper_id=PAPER_ID, snapshot_hash="abc")
    assert synthesis.index("**A. Scientific closure.**") < synthesis.index(
        "**B. Paper reproduction.**"
    )
    assert synthesis.index("**B. Paper reproduction.**") < synthesis.index(
        "**C. Autonomous research.**"
    )
    assert synthesis.index("**C. Autonomous research.**") < synthesis.index(
        "**D. Terminal receipt.**"
    )
    assert "do not repeat the same `find`, `ls`, `pwd`" in synthesis
    assert "does not need a numeric rule" in synthesis
    assert "rule weight, total\nscore, or pass threshold" in synthesis

    audit = final_task_audit_instructions(paper_id=PAPER_ID)
    assert "answer-inversion audit" in audit
    assert "performs no calculation" in audit
    assert "Do not require a numeric rule" in audit
    assert "which candidate wins" in audit


class _FakeHarness:
    model = "fixture-model"

    def __init__(self, *, write_receipt: bool = True) -> None:
        self.write_receipt = write_receipt
        self.request = None

    def run(self, request):
        self.request = request
        review = {
            "decision": "scientific_not_constructible",
            "paper_id": PAPER_ID,
            "scientific_core": {"objective": "fixture"},
            "paper_route": {"scientific_route": "fixture"},
            "input_closure": {"status": "failed", "unresolved": ["input"]},
        }
        receipt = {
            "decision": "scientific_not_constructible",
            "paper_id": PAPER_ID,
            "artifact_path": "outputs/workflow_review.json",
            "summary": "Essential input is not uniquely specified.",
        }
        write_json(request.workspace / "outputs/workflow_review.json", review)
        if self.write_receipt:
            write_json(request.workspace / "outputs/construction_receipt.json", receipt)
        return AgentRunResult(
            status="completed",
            response=receipt,
            harness="fake",
            model=self.model,
            phase=request.phase,
            attempt_id="attempt-fixture",
            started_at="2026-08-27T00:00:00Z",
            duration_seconds=0.0,
            command=[],
            exit_code=0,
            workspace=str(request.workspace),
        )


def test_stage06_receipt_is_not_a_bridge_completion_artifact(tmp_path: Path) -> None:
    source = tmp_path / "snapshot"
    _write(source / "upstream_hints.json", {})
    harness = _FakeHarness()
    receipt, _, _ = _run_synthesis_agent(
        harness=harness,
        stage_root=tmp_path / "stage06",
        paper_id=PAPER_ID,
        snapshot={"root": source, "snapshot_hash": "abc"},
        config={"synthesis_max_tool_calls": 180},
    )
    assert receipt["decision"] == "scientific_not_constructible"
    assert harness.request.metadata["structured_artifact_path"] == "outputs/construction_receipt.json"
    assert len(harness.request.metadata["structured_artifact_required_files"]) == 16
    assert harness.request.metadata["finalization_reserve"] == 6


def test_stage06_requires_the_terminal_receipt_file(tmp_path: Path) -> None:
    source = tmp_path / "snapshot"
    _write(source / "upstream_hints.json", {})
    with pytest.raises(AgentExecutionError, match="construction_receipt.json"):
        _run_synthesis_agent(
            harness=_FakeHarness(write_receipt=False),
            stage_root=tmp_path / "stage06",
            paper_id=PAPER_ID,
            snapshot={"root": source, "snapshot_hash": "abc"},
            config={"synthesis_max_tool_calls": 180},
        )

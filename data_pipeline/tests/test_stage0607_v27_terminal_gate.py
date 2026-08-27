from __future__ import annotations

import json
from pathlib import Path

from src.stages import phase_gate


def _review_with_failed_scientific_labels() -> dict:
    return {
        "decision": "candidate_ready",
        "paper_id": "paper_fixture",
        "scientific_core": {"objective": "fixture"},
        "paper_route": {"summary": "private"},
        "reference_results": {"summary": "private"},
        "feasibility": {
            "objective": {"status": "failed"},
            "public_inputs": {"status": "failed", "unresolved_essential_inputs": []},
            "evaluation": {"status": "failed"},
            "reproducible_investigation": {"status": "failed"},
            "modes": {
                "paper_reproduction": {"status": "feasible"},
                "autonomous_research": {"status": "feasible"},
            },
            "release_modes": ["paper_reproduction", "autonomous_research"],
        },
        "task_quality": {
            name: {"status": "failed"}
            for name in (
                "instruction_completeness",
                "input_completeness",
                "process_keypoints",
                "final_conclusions",
                "mode_separation",
            )
        },
    }


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        value if isinstance(value, str) else json.dumps(value), encoding="utf-8"
    )


def _write_complete_mode(root: Path, mode: str) -> None:
    _write(
        root / mode / "task.md",
        """# Task
## Scientific objective
Determine the reaction barrier and preferred pathway.
## Public inputs and scientific boundaries
Use data/reactant.xyz; charge and multiplicity are explicit.
## Required scientific validation/investigation
Validate the stationary point and compare both pathways. The calculation is complete when both checks pass; stop when coverage is exhausted.
## Deliverables
Submit report/results.json with the barrier and conclusion.
""",
    )
    _write(root / mode / "data/reactant.xyz", "1\nreactant\nH 0 0 0\n")
    _write(
        root / mode / "task_info.json",
        {
            "paper_id": "paper_fixture",
            "task_type": mode,
            "title": "Fixture barrier task",
            "category": "reaction",
            "paper": {"title": "Fixture", "doi": "", "journal": "", "publication_date": ""},
            "data": [{"path": "data", "description": "Reactant input"}],
            "required_deliverables": [{"path": "report/results.json", "description": "Results"}],
            "difficulty": "easy",
            "difficulty_reasons": ["Fixed direct calculation."],
        },
    )
    _write(
        root / mode / "submission_schema.json",
        {
            "required_files": ["report/results.json"],
            "primary_result_file": "report/results.json",
            "result_schema": {
                "type": "object",
                "properties": {"barrier": {"type": "number"}, "conclusion": {"type": "string"}},
                "required": ["barrier", "conclusion"],
            },
        },
    )
    evaluation = root / "evaluator_reference" / mode
    common = {"paper_id": "paper_fixture"}
    _write(evaluation / "reference_key_points.json", {**common, "items": [{"key_point_id": "kp1", "key_point_type": "process", "statement": "Validate stationary point", "expected": "validated", "evidence_ids": ["ev1"]}]})
    _write(evaluation / "reference_conclusions.json", {**common, "items": [{"conclusion_id": "c1", "statement": "Preferred pathway", "expected": "path A", "supporting_key_point_ids": ["kp1"], "evidence_ids": ["ev1"], "claim_role": "final"}]})
    _write(evaluation / "scoring_rules.json", {**common, "rules": [{"rule_id": "r1", "reference_id": "kp1", "type": "semantic", "expected": "validated", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic"}}, {"rule_id": "r2", "reference_id": "c1", "type": "semantic", "expected": "path A", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic"}}]})
    _write(evaluation / "evidence_map.json", {**common, "evidence": [{"evidence_id": "ev1", "source": "fixture"}]})
    _write(evaluation / "critical_failures.json", {**common, "items": [{"failure_id": "f1", "condition": "No result", "severity": "critical"}]})


def test_mechanical_gate_does_not_scientifically_reject(monkeypatch, tmp_path) -> None:
    _write_complete_mode(tmp_path, "paper_reproduction")
    _write_complete_mode(tmp_path, "autonomous_research")
    (tmp_path / "paper_route.md").write_text("private\n", encoding="utf-8")
    (tmp_path / "workflow_review.json").write_text(
        json.dumps(_review_with_failed_scientific_labels()), encoding="utf-8"
    )
    monkeypatch.setattr(phase_gate, "_mode_findings", lambda *args, **kwargs: ([], []))

    report = phase_gate.validate(tmp_path)

    assert report["status"] == "passed"
    assert any(item.startswith("feasibility_") for item in report["diagnostics"])
    assert any(item.startswith("workflow_review_task_quality") for item in report["diagnostics"])


def test_scientific_rejection_review_is_a_valid_terminal_gate(tmp_path) -> None:
    review = {
        "decision": "scientific_not_constructible",
        "paper_id": "paper_fixture",
    }
    (tmp_path / "workflow_review.json").write_text(
        json.dumps(review), encoding="utf-8"
    )

    report = phase_gate.validate(tmp_path)

    assert report["status"] == "passed"
    assert report["findings"] == []


def test_invalid_workflow_decision_is_a_protocol_failure(tmp_path) -> None:
    (tmp_path / "workflow_review.json").write_text(
        json.dumps({"decision": "audited_with_repairs", "paper_id": "paper_fixture"}),
        encoding="utf-8",
    )
    report = phase_gate.validate(tmp_path)
    assert report["status"] == "failed"
    assert "workflow_review_decision_invalid:audited_with_repairs" in report["findings"]

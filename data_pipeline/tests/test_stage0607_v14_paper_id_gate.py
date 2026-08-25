from __future__ import annotations

import json
from pathlib import Path

from src.stages.phase_gate import run
from src.stages.stage06_task_builder.validation import canonical_task_pair_id
from src.stages.stage06_task_builder.stage import _publish_provisional_not_constructible


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(json.dumps(value), encoding="utf-8")


def _mode(root: Path, mode: str) -> None:
    _write(root / "task.md", "# Task\nCompute and report the result.\n")
    _write(
        root / "task_info.json",
        {
            "paper_id": "paper_v14",
            "task_id": "paper_v14",
            "mode": mode,
            "scientific_mode": mode,
            "task_mode": "guided_reproduction" if mode == "paper_reproduction" else "open_discovery",
            "required_deliverables": [{"path": "report/results.json"}],
        },
    )
    _write(
        root / "task_spec.json",
        {
            "paper_id": "paper_v14",
            "task_id": "paper_v14",
            "mode": mode,
            "scientific_mode": mode,
            "input_assets": [{"path": "data/inputs/input.xyz"}],
        },
    )
    _write(
        root / "submission_contract.json",
        {"required_files": ["report/results.json"], "results_schema": {"type": "object"}},
    )
    rubric = [{"id": "science", "description": "Compute"}]
    if mode == "paper_reproduction":
        rubric.append(
            {
                "id": "route",
                "criterion_type": "route_fidelity",
                "evidence_artifacts": ["report/results.json"],
            }
        )
        _write(root / "paper_route.md", "# Route\n")
        _write(root / "workflow_spec.json", {"steps": []})
        _write(root / "route_evidence_map.json", {})
    _write(root / "process_rubric.json", rubric)
    _write(root / "data/inputs/input.xyz", "1\ninput\nH 0 0 0\n")


def _pair(tmp_path: Path) -> Path:
    pair = tmp_path / "outputs" / "task_pair"
    _mode(pair / "paper_reproduction", "paper_reproduction")
    _mode(pair / "autonomous_research", "autonomous_research")
    ref = pair / "evaluator_reference"
    _write(
        ref / "reference_key_points.json",
        {
            "paper_id": "paper_v14",
            "items": [
                {
                    "key_point_id": "kp-1",
                    "statement": "A key point",
                    "claim_role": "intermediate",
                    "evidence_ids": ["ev-1"],
                }
            ],
        },
    )
    _write(
        ref / "reference_conclusions.json",
        {
            "paper_id": "paper_v14",
            "items": [
                {
                    "conclusion_id": "conc-1",
                    "statement": "Final conclusion",
                    "claim_role": "final",
                    "supporting_key_point_ids": ["kp-1"],
                    "evidence_ids": ["ev-1"],
                }
            ],
        },
    )
    _write(
        ref / "scoring_rules.json",
        {
            "paper_id": "paper_v14",
            "rules": [
                {
                    "rule_id": "rule-1",
                    "reference_id": "kp-1",
                    "evaluation_type": "semantic_propositions",
                }
            ],
        },
    )
    _write(ref / "evidence_map.json", {"paper_id": "paper_v14", "evidence": [{"evidence_id": "ev-1"}]})
    _write(ref / "critical_failures.json", {"paper_id": "paper_v14", "items": []})
    return pair.parent


def test_same_snapshot_has_same_gate_and_keyword_diagnostics(tmp_path: Path) -> None:
    outputs = _pair(tmp_path)
    self_report = run("stage07a", outputs)
    external_report = run("stage07a", outputs)
    assert self_report["checker_version"] == "stage06-07-gate-v16"
    assert self_report["blocking_findings"] == external_report["blocking_findings"]
    assert not any("keywords" in item for item in self_report["findings"])
    assert "scoring_rule_binding_missing:rule-1" in self_report["blocking_findings"]
    assert self_report["status"] == "failed"


def test_invalid_scientific_reference_still_blocks(tmp_path: Path) -> None:
    outputs = _pair(tmp_path)
    path = outputs / "task_pair" / "evaluator_reference" / "evidence_map.json"
    _write(path, {"paper_id": "paper_v14", "evidence": []})
    report = run("stage07a", outputs)
    assert report["status"] == "failed"
    assert any(item.startswith("reference_evidence_missing:") for item in report["blocking_findings"])


def test_canonical_identity_is_the_paper_id() -> None:
    assert canonical_task_pair_id("paper_abc") == "paper_abc"


def test_scientific_negative_ignores_truncated_success_review(tmp_path: Path) -> None:
    outputs = tmp_path / "agent_outputs"
    outputs.mkdir()
    receipt = {
        "decision": "scientific_not_constructible",
        "failure_code": "missing_source_controlling_input",
        "failure_reasons": [],
    }
    _write(outputs / "construction_receipt.json", receipt)
    (outputs / "workflow_review.json").write_text('{"decision":', encoding="utf-8")
    result = _publish_provisional_not_constructible(
        stage_root=tmp_path / "stage",
        run_id="run",
        paper_id="paper_abc",
        candidate_id="candidate-1",
        receipt=receipt,
        review={},
        agent_audit={},
        outputs=outputs,
        snapshot={"root": str(tmp_path / "snapshot"), "snapshot_hash": "hash"},
        documents=[],
    )
    assert result["decision"] == "provisional_not_constructible"
    assert result["retryable"] is False

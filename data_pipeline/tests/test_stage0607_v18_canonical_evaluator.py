from __future__ import annotations

import json
from pathlib import Path

from src.stages.evaluator_reference import evaluator_reference_findings, read_split_reference
from src.stages.stage07_task_judge.validation import stage07_mechanical_pre_publish_check


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _split(root: Path, *, complete: bool = True) -> None:
    base = root / "evaluator_reference"
    _write(base / "reference_key_points.json", {
        "paper_id": "paper-1",
        "items": [{
            "key_point_id": "kp-1", "statement": "Barrier is 24.3 kcal/mol.",
            "reference_value": 24.3, "expected": 24.3,
            "claim_role": "final", "evidence_ids": ["ev-1"], "unit": "kcal/mol",
        }],
    })
    _write(base / "reference_conclusions.json", {
        "paper_id": "paper-1",
        "items": [{
            "conclusion_id": "conclusion-1", "statement": "The barrier is 24.3 kcal/mol.",
            "expected": "The barrier is 24.3 kcal/mol.", "claim_role": "final",
            "supporting_key_point_ids": ["kp-1"], "evidence_ids": ["ev-1"],
        }],
    })
    _write(base / "scoring_rules.json", {
        "paper_id": "paper-1",
        "rules": [{
            "rule_id": "rule-1", "reference_id": "kp-1", "type": "numeric",
            "target": 24.3, "unit": "kcal/mol", "tolerance": 1.0,
            "comparison": "absolute_difference",
            "binding": {"artifact_paths": ["report/results.json"],
                        "fields": ["$.barrier"], "comparison": "absolute_difference"},
        }, {
            "rule_id": "rule-2", "reference_id": "conclusion-1", "type": "semantic",
            "expected": "The barrier is 24.3 kcal/mol.", "comparison": "semantic_match",
            "binding": {"artifact_paths": ["report/results.json"],
                        "fields": ["document"], "comparison": "semantic_match"},
        }] if complete else [],
    })
    _write(base / "evidence_map.json", {"paper_id": "paper-1", "evidence": [{"evidence_id": "ev-1"}]})
    _write(base / "critical_failures.json", {"paper_id": "paper-1", "items": ["fabrication"]})


def test_split_reference_is_the_only_readable_contract(tmp_path: Path) -> None:
    _split(tmp_path)
    loaded = read_split_reference(tmp_path)
    assert loaded is not None
    assert not (tmp_path / "reference.json").exists()
    assert not (tmp_path / "hidden_reference" / "ground_truth_common.json").exists()
    blocking, warnings = evaluator_reference_findings(tmp_path)
    assert blocking == []
    assert warnings == []


def test_incomplete_rule_is_blocking_but_no_legacy_projection_is_created(tmp_path: Path) -> None:
    _split(tmp_path, complete=False)
    blocking, _ = evaluator_reference_findings(tmp_path)
    assert "scoring_rule_missing_for_reference:kp-1" in blocking
    assert not (tmp_path / "reference.json").exists()


def test_mechanical_gate_requires_all_five_split_files(tmp_path: Path) -> None:
    _split(tmp_path)
    (tmp_path / "evaluator_reference" / "critical_failures.json").unlink()
    report = stage07_mechanical_pre_publish_check(tmp_path, paper_id="paper-1")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "evaluator_reference_missing" in report["findings"]

from __future__ import annotations

import json
from pathlib import Path

from src.stages.evaluator_reference import minimal_evaluator_findings
from src.stages.phase_gate import run


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf-8")


def _package(tmp_path: Path, *, rule_overrides: dict | None = None) -> Path:
    pair = tmp_path / "task_pair"
    for mode in ("paper_reproduction", "autonomous_research"):
        root = pair / mode
        _write(root / "task.md", "# Task\nCompute the result.\n")
        _write(root / "task_info.json", {"paper_id": "paper-v15", "task_id": "paper-v15", "mode": mode, "scientific_mode": mode, "task_mode": "guided_reproduction" if mode == "paper_reproduction" else "open_discovery", "required_deliverables": [{"path": "report/results.json"}]})
        _write(root / "task_spec.json", {"paper_id": "paper-v15", "task_id": "paper-v15", "mode": mode, "scientific_mode": mode, "input_assets": []})
        _write(root / "submission_contract.json", {"required_files": ["report/results.json"], "results_schema": {"type": "object"}})
        rubric = [{"id": "science", "description": "Compute"}]
        if mode == "paper_reproduction":
            rubric.append({"id": "route", "criterion_type": "route_fidelity", "evidence_artifacts": ["report/results.json"]})
            _write(root / "paper_route.md", "# Route\n")
            _write(root / "workflow_spec.json", {"steps": []})
            _write(root / "route_evidence_map.json", {})
        _write(root / "process_rubric.json", rubric)
    ref = pair / "evaluator_reference"
    _write(ref / "reference_key_points.json", {"paper_id": "paper-v15", "items": [{"key_point_id": "kp-energy", "statement": "Barrier is 12.5 kcal/mol.", "expected": 12.5, "unit": "kcal/mol", "evidence_ids": ["ev-1"]}]})
    _write(ref / "reference_conclusions.json", {"paper_id": "paper-v15", "items": [{"conclusion_id": "conc-order", "statement": "The lower barrier is preferred.", "expected": {"ordering": ["path-a", "path-b"]}, "supporting_key_point_ids": ["kp-energy"], "evidence_ids": ["ev-1"], "claim_role": "final"}]})
    rule = {"rule_id": "rule-energy", "reference_id": "kp-energy", "type": "numeric", "target": 12.5, "unit": "kcal/mol", "tolerance": {"absolute": 0.37}, "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.barrier"]}}
    rule.update(rule_overrides or {})
    _write(ref / "scoring_rules.json", {"paper_id": "paper-v15", "rules": [rule, {"rule_id": "rule-order", "reference_id": "conc-order", "type": "ordering", "expected": {"ordering": ["path-a", "path-b"]}, "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.ordering"]}}]})
    _write(ref / "evidence_map.json", {"paper_id": "paper-v15", "evidence": [{"evidence_id": "ev-1", "description": "Paper result"}]})
    _write(ref / "critical_failures.json", {"paper_id": "paper-v15", "items": []})
    return pair


def test_complete_minimal_rules_pass_and_tolerance_is_not_scored(tmp_path: Path) -> None:
    assert minimal_evaluator_findings(_package(tmp_path)) == []


def test_numeric_contract_is_blocking_when_required_fields_are_missing(tmp_path: Path) -> None:
    findings = minimal_evaluator_findings(_package(tmp_path, rule_overrides={"tolerance": None, "target": None, "unit": ""}))
    assert "scoring_rule_missing_target:rule-energy" in findings
    assert "scoring_rule_missing_unit:rule-energy" in findings
    assert "scoring_rule_missing_numeric_tolerance:rule-energy" in findings


def test_self_check_and_external_gate_share_blocking_findings(tmp_path: Path) -> None:
    pair = _package(tmp_path, rule_overrides={"binding": None})
    root = pair.parent
    self_report = run("stage07a", root)
    external_report = run("stage07a", root)
    assert self_report["blocking_findings"] == external_report["blocking_findings"]
    assert "scoring_rule_binding_missing:rule-energy" in self_report["blocking_findings"]


def test_keywords_are_not_required(tmp_path: Path) -> None:
    assert not any("keywords" in item for item in minimal_evaluator_findings(_package(tmp_path)))


def test_condition_and_semantic_rules_are_supported_without_extra_types(tmp_path: Path) -> None:
    pair = _package(tmp_path)
    path = pair / "evaluator_reference" / "scoring_rules.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    value["rules"][0] = {
        "rule_id": "rule-energy",
        "reference_id": "kp-energy",
        "type": "condition",
        "expected": {"converged": True, "imaginary_frequency_count": 0},
        "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.validation"]},
    }
    value["rules"][1]["type"] = "semantic"
    value["rules"][1]["expected"] = {"required": ["lower barrier is preferred"]}
    _write(path, value)
    assert minimal_evaluator_findings(pair) == []


def test_placeholder_reference_is_blocking(tmp_path: Path) -> None:
    pair = _package(tmp_path)
    path = pair / "evaluator_reference" / "reference_key_points.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    value["items"][0]["statement"] = "Reference scientific result kp-energy."
    _write(path, value)
    assert "reference_key_point_statement_invalid:kp-energy" in minimal_evaluator_findings(pair)

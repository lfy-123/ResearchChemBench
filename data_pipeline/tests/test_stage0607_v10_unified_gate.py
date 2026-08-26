from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.stages.evaluator_reference import evaluator_reference_findings
from src.stages.phase_gate import run
from src.stages.stage06_task_builder.bootstrap_task_pair import safe_path
from src.stages.stage06_task_builder.stage import _stage06a_phase_gate_findings
from src.stages.stage07_task_judge.validation import stage07_mechanical_pre_publish_check


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf-8")


def _evaluator(root: Path, *, complete: bool = True) -> None:
    base = root / "evaluator_reference"
    _write(base / "reference_key_points.json", {"paper_id": "paper-1", "items": [{
        "key_point_id": "kp-1", "statement": "Barrier is 24.3 kcal/mol.", "expected": 24.3,
        "evidence_ids": ["ev-1"], "claim_role": "intermediate"}]})
    _write(base / "reference_conclusions.json", {"paper_id": "paper-1", "items": [{
        "conclusion_id": "c-1", "statement": "The barrier is 24.3 kcal/mol.",
        "expected": "The barrier is 24.3 kcal/mol.", "claim_role": "final",
        "supporting_key_point_ids": ["kp-1"], "evidence_ids": ["ev-1"]}]})
    rules = [{"rule_id": "r-1", "reference_id": "kp-1", "type": "numeric", "target": 24.3,
        "unit": "kcal/mol", "tolerance": 1.0, "comparison": "absolute_difference",
        "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.barrier"], "comparison": "absolute_difference"}},
        {"rule_id": "r-2", "reference_id": "c-1", "type": "semantic",
        "expected": "The barrier is 24.3 kcal/mol.", "comparison": "semantic_match",
        "binding": {"artifact_paths": ["report/results.json"], "fields": ["document"], "comparison": "semantic_match"}}]
    _write(base / "scoring_rules.json", {"paper_id": "paper-1", "rules": rules if complete else []})
    _write(base / "evidence_map.json", {"evidence": [{"evidence_id": "ev-1"}]})
    _write(base / "critical_failures.json", {"items": ["no convergence"]})


def _mode(root: Path, mode: str) -> None:
    task_mode = "guided_reproduction" if mode == "paper_reproduction" else "open_discovery"
    _write(root / "task.md", "# Task\nCompute the requested result.\n")
    _write(root / "task_info.json", {"paper_id": "paper-1", "task_id": "paper-1", "task_family_id": "paper-1",
        "mode": mode, "scientific_mode": mode, "task_mode": task_mode})
    _write(root / "task_spec.json", {"paper_id": "paper-1", "task_id": "paper-1", "mode": mode,
        "scientific_mode": mode, "input_assets": [{"path": "data/inputs/input.xyz"}]})
    _write(root / "submission_contract.json", {"required_files": ["report/results.json"],
        "results_schema": {"type": "object", "properties": {"barrier": {"type": "number"}}}})
    rubric = [{"id": "science", "description": "Compute and report the result."}]
    if mode == "paper_reproduction":
        rubric.append({"id": "paper_route_fidelity", "criterion_type": "route_fidelity",
            "description": "Report the executed route.", "evidence_artifacts": ["report/results.json"]})
    _write(root / "process_rubric.json", rubric)
    _write(root / "data/inputs/input.xyz", "1\ninput\nH 0 0 0\n")
    if mode == "paper_reproduction":
        _write(root / "paper_route.md", "# Route\n")
        _write(root / "workflow_spec.json", {"steps": []})
        _write(root / "route_evidence_map.json", {})


def _pair(tmp_path: Path) -> Path:
    pair = tmp_path / "task_pair"
    _mode(pair / "paper_reproduction", "paper_reproduction")
    _mode(pair / "autonomous_research", "autonomous_research")
    _evaluator(pair)
    _write(pair / "construction_receipt.json", {"decision": "constructed"})
    _write(pair / "workflow_review.json", {"decision": "candidate_ready"})
    for name in ("workflow_completeness_check.json", "public_to_private_asset_map.json", "toolbox_requirements.json"):
        _write(pair / name, {})
    return pair


def test_bootstrap_public_input_path_is_relative_to_input_root() -> None:
    assert safe_path("data/inputs/input.xyz") == "input.xyz"
    assert safe_path("inputs/public_inputs/nested/input.xyz") == "nested/input.xyz"


def test_shared_gate_requires_complete_split_evaluator(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    assert evaluator_reference_findings(pair) == ([], [])
    (pair / "evaluator_reference/scoring_rules.json").unlink()
    blocking, _ = evaluator_reference_findings(pair)
    assert "evaluator_reference_file_missing:scoring_rules.json" in blocking


def test_stage06a_and_stage07a_use_same_evaluator_findings(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    stage06_report = run("stage06a", pair)
    stage07_root = tmp_path / "stage07"
    shutil.copytree(pair, stage07_root / "task_pair")
    stage07_report = run("stage07a", stage07_root)
    assert set(stage06_report["blocking_findings"]) <= set(stage07_report["blocking_findings"])


def test_stage06a_receipt_is_checked_only_after_agent_self_check(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    (pair / "construction_receipt.json").unlink()

    self_check = run("stage06a", pair)
    assert "construction_receipt_missing" not in self_check["findings"]

    workspace = tmp_path / "workspace"
    shutil.copytree(pair, workspace / "outputs")
    external_findings = _stage06a_phase_gate_findings({}, workspace)
    assert "construction_receipt_missing" in external_findings


def test_hidden_reference_is_not_a_valid_current_contract(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    _write(pair / "hidden_reference/ground_truth_common.json", {})
    assert "legacy_hidden_reference_forbidden" in run("stage07a", tmp_path)["findings"]


def test_stage07_mechanical_check_requires_both_modes_and_split_files(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    assert stage07_mechanical_pre_publish_check(pair, paper_id="paper-1")["mechanical_pre_publish_status"] == "passed"
    (pair / "evaluator_reference/critical_failures.json").unlink()
    report = stage07_mechanical_pre_publish_check(pair, paper_id="paper-1")
    assert report["mechanical_pre_publish_status"] == "failed"

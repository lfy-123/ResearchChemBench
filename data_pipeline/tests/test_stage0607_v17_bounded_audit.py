from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from src.agents.schemas import STAGE07_AUDIT_SCHEMA
from src.stages.evaluator_reference import minimal_evaluator_findings
from src.stages.stage06_task_builder.prompts import task_pair_builder_instructions
from src.stages.stage06_task_builder.stage import _artifact_delivery_failure
from src.stages.stage07_task_judge.prompts import audit_instructions
from src.stages.stage07_task_judge.stage import (
    STAGE07_ELIGIBLE_STAGE06_DECISIONS,
    _approved_receipt_contract_findings,
)
from src.stages.stage07_task_judge.package import _task_info


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _evaluator(
    tmp_path: Path,
    *,
    reference: object,
    rule_type: str = "numeric",
    target: object = None,
    fields: list[str] | None = None,
    projection: object = None,
) -> Path:
    root = tmp_path / "task_pair"
    directory = root / "evaluator_reference"
    _write(
        directory / "reference_key_points.json",
        {
            "items": [
                {
                    "key_point_id": "kp-1",
                    "statement": "Computed values for the selected systems.",
                    "expected": reference,
                    "evidence_ids": ["ev-1"],
                }
            ]
        },
    )
    _write(
        directory / "reference_conclusions.json",
        {
            "items": [
                {
                    "conclusion_id": "final-1",
                    "statement": "The selected calculation supports the final claim.",
                    "expected": {"supported": True},
                    "claim_role": "final",
                    "supporting_key_point_ids": ["kp-1"],
                    "evidence_ids": ["ev-1"],
                }
            ]
        },
    )
    binding = {
        "artifact_paths": ["report/results.json"],
        "fields": fields or ["$.value"],
        "comparison": "authored_comparison",
    }
    if projection is not None:
        binding["canonical_projection"] = projection
    rule = {
        "rule_id": "rule-1",
        "reference_id": "kp-1",
        "type": rule_type,
        "binding": binding,
    }
    if rule_type == "numeric":
        rule.update({"target": reference if target is None else target, "unit": "eV", "tolerance": 0.1})
    else:
        rule["expected"] = "projected scientific result"
    _write(
        directory / "scoring_rules.json",
        {
            "rules": [
                rule,
                {
                    "rule_id": "rule-final",
                    "reference_id": "final-1",
                    "type": "condition",
                    "expected": {"supported": True},
                    "binding": {
                        "artifact_paths": ["report/results.json"],
                        "fields": ["$.supported"],
                        "comparison": "authored_condition",
                    },
                },
            ]
        },
    )
    _write(directory / "evidence_map.json", {"evidence": [{"evidence_id": "ev-1"}]})
    _write(directory / "critical_failures.json", {"items": []})
    return root


def test_stage07_only_accepts_constructed_candidates() -> None:
    assert STAGE07_ELIGIBLE_STAGE06_DECISIONS == {
        "provisional_constructed",
        "constructed",
    }
    assert "provisional_not_constructible" not in STAGE07_ELIGIBLE_STAGE06_DECISIONS


def test_stage07_schema_has_no_workflow_redesign_success() -> None:
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            {
                "audit_decision": "approved_after_workflow_redesign",
                "artifact_path": "outputs/task_pair",
                "summary": "redesigned",
            },
            STAGE07_AUDIT_SCHEMA,
        )


def test_stage07_prompt_is_bounded_and_audits_inputs_and_evaluator() -> None:
    prompt = audit_instructions(
        paper_id="paper-v17",
        task_pair_id="paper-v17",
        manifest_hash="hash",
        max_tool_calls=80,
        finalization_reserve=12,
    )
    assert "Do not search for a replacement workflow" in prompt
    assert "construct a new task from the paper" in prompt
    assert "transcribe\n  connectivity from Figure 1" in prompt
    assert "EVALUATOR CROSSWALK" in prompt
    assert "scalar target bound to multiple" in prompt


def test_numeric_map_cannot_be_hidden_in_semantic_rule(tmp_path: Path) -> None:
    root = _evaluator(
        tmp_path,
        reference={"system_A": 0.19, "system_B": 0.45},
        rule_type="semantic",
    )
    assert (
        "scoring_rule_numeric_reference_type_mismatch:rule-1:semantic"
        in minimal_evaluator_findings(root)
    )


def test_multifield_scalar_target_requires_projection(tmp_path: Path) -> None:
    root = _evaluator(
        tmp_path,
        reference={"system_A": 0.19, "system_B": 0.45},
        target=0.32,
        fields=["$.system_A", "$.system_B"],
    )
    findings = minimal_evaluator_findings(root)
    assert "scoring_rule_multifield_scalar_target_without_projection:rule-1" in findings
    assert "scoring_rule_target_reference_shape_mismatch:rule-1" in findings


def test_explicit_projection_allows_scalar_aggregate(tmp_path: Path) -> None:
    root = _evaluator(
        tmp_path,
        reference={"system_A": 0.19, "system_B": 0.45},
        target=0.32,
        fields=["$.system_A", "$.system_B"],
        projection={"operation": "mean", "inputs": ["$.system_A", "$.system_B"]},
    )
    findings = minimal_evaluator_findings(root)
    assert not any("multifield_scalar" in item for item in findings)
    assert not any("target_reference_" in item for item in findings)


def test_direct_numeric_target_must_match_reference(tmp_path: Path) -> None:
    root = _evaluator(tmp_path, reference=[3.04, 3.17], target=[3.04, 3.20])
    assert (
        "scoring_rule_target_reference_value_mismatch:rule-1"
        in minimal_evaluator_findings(root)
    )


def test_execution_incomplete_is_delivery_failure_not_science_rejection() -> None:
    record = _artifact_delivery_failure(
        "run-v17",
        "paper-v17",
        "candidate-v17",
        "execution_artifact_incomplete",
        "task files were not completed",
    )
    assert record["decision"] == "artifact_delivery_failure_retryable"
    assert record["handoff_ready"] is False
    assert record["processing_status"] == "failed"


def test_stage07_receipt_does_not_require_alternative_workflow_inventory() -> None:
    response = {
        "audit_decision": "approved",
        "source_stage06_decision": "constructed",
        "paper_id": "paper-v17",
        "artifact_path": "outputs/task_pair",
        "selected_workflow_preserved": True,
        "repairs": [],
        "remaining_issues": [],
        "toolbox_status": "available",
        "execution_readiness": "ready",
        "required_additions": [],
        "resource_status": "feasible",
        "representativeness_audit": {
            "paper_claims_checked": [],
            "selected_scope_kind": "core_scientific_subworkflow",
            "coverage_summary": [],
            "rationale": "The selected objective directly supports the claim.",
            "ultimate_claim_dependency": {
                "advertised_conclusion": "Final claim",
                "direct_computational_evidence": [],
                "supporting_only_evidence": [],
                "selected_workflow_position": "direct",
            },
        },
        "scientific_audit_table": [
            {"check": name, "status": "closed"}
            for name in (
                "objective_scope",
                "inputs_and_boundaries",
                "evaluator_crosswalk",
                "actions_artifacts_validation",
                "mode_equivalence",
                "autonomous_disclosure",
            )
        ],
        "scientific_decision": "approved",
        "contract_status": "passed",
        "disclosure_status": "passed",
        "schema_load_diagnostic": "passed",
        "summary": "approved",
    }
    assert _approved_receipt_contract_findings(response) == []


def test_synthesis_prioritizes_deliverable_before_optional_review_detail() -> None:
    prompt = task_pair_builder_instructions(paper_id="paper-v17", snapshot_hash="hash")
    assert "task pair is the primary deliverable" in prompt
    assert "Do not expand this review into a long narrative" in prompt
    assert "do not repeat `pwd`, broad `ls`/`find`" in prompt


def test_task_package_projects_private_data_annotations_to_taskinfo_fields() -> None:
    value = _task_info(
        source_info={
            "paper_id": "paper-v17",
            "category": "chemistry",
            "data": [
                {
                    "name": "input.xyz",
                    "path": "data/inputs/input.xyz",
                    "role": "input_geometry",
                    "source_evidence_ids": ["ev-1"],
                }
            ],
        },
        task_text="Compute the requested result.",
        task_id="paper-v17",
        task_family_id="paper-v17",
        task_type="autonomous_research",
        runtime_readiness="ready",
        toolbox_requirements=[],
        required_deliverables=[{"path": "report/results.json"}],
    )
    assert value["data"] == [
        {
            "name": "input.xyz",
            "path": "data/inputs/input.xyz",
            "type": "",
            "description": "",
        }
    ]

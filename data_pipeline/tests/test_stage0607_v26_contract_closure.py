from __future__ import annotations

from src.stages.phase_gate import _numeric_target_usable, _schema_selector_target
from src.stages.stage06_task_builder.prompts import (
    STAGE06_SYNTHESIS_PROMPT_VERSION,
    final_task_synthesis_instructions,
)
from src.stages.stage07_task_judge.prompts import (
    STAGE07_AUDIT_PROMPT_VERSION,
    final_task_audit_instructions,
)


PAPER_ID = "paper_v26fixture"


def _branched_result_schema(keyword: str = "oneOf") -> dict:
    return {
        "type": "object",
        "properties": {
            "completion_status": {"type": "string"},
            "systems": {
                "type": "object",
                "properties": {
                    "system_a": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number"},
                            "note": {"type": "string"},
                            "optional_value": {"type": "number"},
                        },
                        "required": ["value", "note"],
                    }
                },
                "required": ["system_a"],
            },
            "failure": {
                "type": "object",
                "properties": {
                    "stage": {"type": "string"},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["stage", "evidence"],
            },
        },
        "required": ["completion_status"],
        keyword: [
            {
                "properties": {"completion_status": {"const": "completed"}},
                "required": ["systems"],
            },
            {
                "properties": {"completion_status": {"const": "bounded_failure"}},
                "required": ["failure"],
            },
        ],
    }


def test_v26_stage06_prompt_requires_truthful_outcomes_and_object_identity() -> None:
    prompt = final_task_synthesis_instructions(
        paper_id=PAPER_ID, snapshot_hash="fixture"
    )
    assert STAGE06_SYNTHESIS_PROMPT_VERSION.startswith("v26-")
    assert "Every outcome explicitly allowed by `task.md` must be representable" in prompt
    assert "bounded failure, partial discovery or an alternative validation method" in prompt
    assert "fixed known set" in prompt
    assert "Wildcards are" in prompt and "aggregate comparisons" in prompt
    assert "Do not copy the" in prompt
    assert "reproduction evaluator into autonomous research unchanged" in prompt


def test_v26_stage07_prompt_defines_final_contract_closure_audit() -> None:
    prompt = final_task_audit_instructions(paper_id=PAPER_ID)
    assert STAGE07_AUDIT_PROMPT_VERSION.startswith("v26-")
    assert "final scientific-quality and evaluation-contract auditor" in prompt
    assert "Task to schema" in prompt
    assert "Schema to evaluator" in prompt
    assert "Object identity" in prompt
    assert "Public labels" in prompt
    assert "Mode-specific fairness" in prompt
    assert "reverse fairness check" in prompt
    assert "Do not approve from a repair summary alone" in prompt
    assert "not a fallback task builder" in prompt


def test_oneof_success_binding_is_required_in_its_applicable_branch() -> None:
    represented, target, required = _schema_selector_target(
        _branched_result_schema(), "$.systems.system_a.value"
    )
    assert represented is True
    assert required is True
    assert _numeric_target_usable(target) is True


def test_anyof_success_binding_is_required_in_its_applicable_branch() -> None:
    represented, target, required = _schema_selector_target(
        _branched_result_schema("anyOf"), "$.systems.system_a.value"
    )
    assert represented is True
    assert required is True
    assert _numeric_target_usable(target) is True


def test_branch_selector_still_rejects_missing_or_never_required_fields() -> None:
    schema = _branched_result_schema()
    represented, _target, required = _schema_selector_target(
        schema, "$.systems.system_a.missing"
    )
    assert represented is False
    assert required is False

    represented, target, required = _schema_selector_target(
        schema, "$.systems.system_a.optional_value"
    )
    assert represented is True
    assert required is False
    assert _numeric_target_usable(target) is True


def test_branch_selector_preserves_explicit_non_numeric_leaf() -> None:
    represented, target, required = _schema_selector_target(
        _branched_result_schema(), "$.systems.system_a.note"
    )
    assert represented is True
    assert required is True
    assert _numeric_target_usable(target) is False


def test_simple_required_selector_behavior_is_unchanged() -> None:
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "properties": {"value": {"type": "number"}},
                "required": ["value"],
            }
        },
        "required": ["result"],
    }
    represented, target, required = _schema_selector_target(
        schema, "$.result.value"
    )
    assert represented is True
    assert required is True
    assert _numeric_target_usable(target) is True

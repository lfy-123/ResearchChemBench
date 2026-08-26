from __future__ import annotations

from typing import Any


def object_schema(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }


STRING = {"type": "string"}
STRING_ARRAY = {"type": "array", "items": STRING}
EMPTY_STRING_ARRAY = {"type": "array", "items": STRING, "default": []}
OBJECT = {"type": "object", "additionalProperties": True}
OBJECT_ARRAY = {"type": "array", "items": OBJECT}


STAGE06_TASK_PAIR_BUILDER_SCHEMA = object_schema(
    [
        "decision",
        "paper_id",
        "artifact_path",
        "summary",
    ],
    {
        "decision": {"enum": ["constructed", "scientific_not_constructible"]},
        "paper_id": STRING,
        "artifact_path": STRING,
        "milestones": OBJECT,
        "workflow_scope_kind": {
            "enum": [
                "full_paper_core_workflow",
                "core_scientific_subworkflow",
                "full_paper_computational_workflow",
                "major_paper_workflow",
                "partial_computational_subworkflow",
                "none",
            ]
        },
        "complexity_profile": OBJECT,
        "failure_code": STRING,
        "failure_reasons": OBJECT_ARRAY,
        "summary": STRING,
        "objective_id": STRING,
        "task_family": STRING,
    },
)


STAGE06_WORKFLOW_REVIEW_SCHEMA = object_schema(
    [
        "decision",
        "paper_id",
        "paper_workflow_inventory_complete",
        "full_paper_workflow_checked",
        "alternative_scope_search_complete",
        "workflow_inventory",
        "workflow_scope",
        "complexity_profile",
        "evidence_map",
        "toolbox_requirements",
        "resource_assessment",
        "failure_code",
        "failure_reasons",
        "warnings",
    ],
    {
        "decision": {"enum": ["candidate_ready", "scientific_not_constructible"]},
        "paper_id": STRING,
        "paper_workflow_inventory_complete": {"type": "boolean"},
        "full_paper_workflow_checked": {"type": "boolean"},
        "alternative_scope_search_complete": {"type": "boolean"},
        "workflow_inventory": OBJECT_ARRAY,
        "workflow_scope": OBJECT,
        "complexity_profile": OBJECT,
        "representativeness_review": OBJECT,
        "execution_readiness": {
            "enum": ["ready", "conditional", "unknown"]
        },
        "selected_candidate_id": {"type": "string", "default": ""},
        "stage05_candidate_disposition": {"type": "string", "default": ""},
        "scientific_question": {"type": "string", "default": ""},
        "public_scientific_question": {"type": "string", "default": ""},
        "task_direction": {"type": "string", "default": ""},
        "category": {"type": "string", "default": ""},
        "workflow_summary": {"type": "string", "default": ""},
        "workflow_steps": {"type": "array", "items": OBJECT, "default": []},
        "public_task_basis": {"type": "object", "additionalProperties": True, "default": {}},
        "paper_route": {"type": "object", "additionalProperties": True, "default": {}},
        "ground_truth_items": {"type": "array", "items": OBJECT, "default": []},
        "evidence_map": {"oneOf": [OBJECT, OBJECT_ARRAY]},
        "toolbox_requirements": OBJECT_ARRAY,
        "resource_assessment": OBJECT,
        "failure_code": STRING,
        "failure_reasons": OBJECT_ARRAY,
        "warnings": EMPTY_STRING_ARRAY,
        "workflow_completeness_check": OBJECT,
        "public_to_private_asset_map": {"oneOf": [OBJECT, OBJECT_ARRAY]},
        "objective_card": OBJECT,
        "key_points": OBJECT_ARRAY,
        "conversion_manifest": OBJECT,
    },
)


STAGE06_AUTONOMOUS_CONVERTER_SCHEMA = object_schema(
    ["status", "artifact_path", "summary"],
    {
        "status": {"enum": ["converted", "conversion_uncertain", "objective_consistency_error"]},
        "artifact_path": STRING,
        "summary": STRING,
        "conversion_report": OBJECT,
        "invalid_reasons": EMPTY_STRING_ARRAY,
    },
)


STAGE06_REVIEW_SCHEMA = object_schema(
    [
        "decision",
        "paper_id",
        "selected_candidate_id",
        "stage05_candidate_disposition",
        "scientific_question",
        "public_scientific_question",
        "task_direction",
        "category",
        "workflow_summary",
        "workflow_steps",
        "public_task_basis",
        "paper_route",
        "ground_truth_items",
        "evidence_map",
        "toolbox_requirements",
        "resource_assessment",
        "reject_reasons",
        "warnings",
    ],
    {
        "decision": {"enum": ["candidate_ready", "scientific_reject"]},
        "paper_id": STRING,
        "artifact_path": STRING,
        "selected_candidate_id": {"type": "string", "default": ""},
        "stage05_candidate_disposition": {"type": "string", "default": ""},
        "scientific_question": STRING,
        "public_scientific_question": STRING,
        "task_direction": {"type": "string", "default": ""},
        "category": {"type": "string", "default": ""},
        "workflow_summary": STRING,
        "workflow_steps": OBJECT_ARRAY,
        "public_task_basis": OBJECT,
        "paper_route": OBJECT,
        "ground_truth_items": OBJECT_ARRAY,
        "evidence_map": {"oneOf": [OBJECT, OBJECT_ARRAY]},
        "toolbox_requirements": OBJECT_ARRAY,
        "resource_assessment": OBJECT,
        "reject_reasons": EMPTY_STRING_ARRAY,
        "warnings": EMPTY_STRING_ARRAY,
        "workflow_completeness_check": OBJECT,
        "public_to_private_asset_map": {"oneOf": [OBJECT, OBJECT_ARRAY]},
    },
)


STAGE06_AUTONOMOUS_SCHEMA = object_schema(
    ["status"],
    {
        "status": {"enum": ["ready", "invalid"]},
        "artifact_path": STRING,
        "summary": STRING,
        "invalid_reasons": EMPTY_STRING_ARRAY,
    },
)


STAGE06_REPRODUCTION_SCHEMA = object_schema(
    ["status", "modified_files", "route_disclosure_summary"],
    {
        "status": {"enum": ["ready", "invalid"]},
        "artifact_path": STRING,
        "modified_files": STRING_ARRAY,
        "route_disclosure_summary": STRING,
        "invalid_reasons": EMPTY_STRING_ARRAY,
    },
)


STAGE06_HIDDEN_SCHEMA = object_schema(
    ["status"],
    {
        "status": {"enum": ["ready", "invalid"]},
        "artifact_path": STRING,
        "paper_id": STRING,
        "expected_result": OBJECT,
        "ground_truth_items": OBJECT_ARRAY,
        "acceptance_profiles": OBJECT_ARRAY,
        "scientific_conclusion_rubric": OBJECT_ARRAY,
        "critical_failures": {
            "type": "array",
            "items": {"oneOf": [STRING, OBJECT]},
        },
        "summary": STRING,
        "invalid_reasons": EMPTY_STRING_ARRAY,
    },
)


# v13 split evaluator-reference files.  Scientific reference schemas are
# intentionally narrower than the scoring-policy schema.  The latter accepts
# draft fields because Gate validates its content as non-blocking policy
# findings rather than as a scientific construction decision.
STAGE06_REFERENCE_KEY_POINTS_SCHEMA = object_schema(
    ["items"],
    {
        "schema_version": STRING,
        "paper_id": STRING,
        "items": OBJECT_ARRAY,
    },
)


STAGE06_REFERENCE_CONCLUSIONS_SCHEMA = object_schema(
    ["items"],
    {
        "schema_version": STRING,
        "paper_id": STRING,
        "items": OBJECT_ARRAY,
    },
)


STAGE06_SCORING_RULES_SCHEMA = object_schema(
    ["rules"],
    {
        "schema_version": STRING,
        "paper_id": STRING,
        "rules": OBJECT_ARRAY,
    },
)


STAGE06_EVIDENCE_MAP_SCHEMA = object_schema(
    [],
    {
        "schema_version": STRING,
        "paper_id": STRING,
        "evidence": OBJECT_ARRAY,
    },
)


STAGE06_CRITICAL_FAILURES_SCHEMA = object_schema(
    [],
    {
        "schema_version": STRING,
        "paper_id": STRING,
        "items": {"type": "array", "items": {"oneOf": [STRING, OBJECT]}},
    },
)


STAGE07_AUDIT_SCHEMA = object_schema(
    [
        "audit_decision",
        "artifact_path",
        "summary",
    ],
    {
        "audit_decision": {
            "enum": [
                "approved",
                "approved_with_repairs",
                "rejected_scientific_unrepairable",
                "objective_failure_retryable",
            ]
        },
        "source_stage06_decision": {
            "enum": [
                "provisional_constructed",
                "constructed",
            ]
        },
        "paper_id": STRING,
        "artifact_path": STRING,
        "selected_workflow_preserved": {"type": "boolean"},
        "repair_origin": {"type": "string", "default": ""},
        "repairs": OBJECT_ARRAY,
        "remaining_issues": OBJECT_ARRAY,
        "toolbox_status": {
            "enum": ["available", "needs_software", "unknown"]
        },
        "required_additions": OBJECT_ARRAY,
        "resource_status": {
            "enum": ["feasible", "high_cost", "infeasible", "uncertain"]
        },
        "representativeness_audit": OBJECT,
        "execution_readiness": {
            "enum": ["ready", "conditional", "unknown"]
        },
        "scientific_decision": STRING,
        "contract_status": {"enum": ["passed", "findings", "not_applicable"]},
        "disclosure_status": {"enum": ["passed", "needs_review", "not_applicable"]},
        "schema_load_diagnostic": {"enum": ["passed", "failed", "not_run"]},
        "summary": STRING,
        "scientific_audit_table": OBJECT_ARRAY,
    },
)


AGENT_SUMMARY_SCHEMA = object_schema(
    ["status"],
    {"status": STRING, "details": OBJECT},
)

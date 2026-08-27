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
OBJECT_ARRAY = {"type": "array", "items": {"type": "object"}}


TASK_MODES = {"enum": ["autonomous_research", "paper_reproduction"]}


STAGE06_SYNTHESIS_SCHEMA = object_schema(
    ["decision", "paper_id", "artifact_path", "release_modes", "summary"],
    {
        "decision": {"enum": ["constructed", "scientific_not_constructible"]},
        "paper_id": STRING,
        "artifact_path": STRING,
        "release_modes": {"type": "array", "items": TASK_MODES, "uniqueItems": True},
        "milestones": {"type": "object"},
        "failure_code": STRING,
        "failure_reasons": OBJECT_ARRAY,
        "summary": STRING,
    },
)


STAGE07_AUDIT_SCHEMA = object_schema(
    [
        "audit_decision",
        "paper_id",
        "artifact_path",
        "release_modes",
        "selected_workflow_preserved",
        "repairs",
        "remaining_issues",
        "scientific_audit",
        "summary",
    ],
    {
        "audit_decision": {
            "enum": [
                "approved",
                "approved_with_repairs",
                "rejected_scientific_unrepairable",
                "technical_blocked",
            ]
        },
        "paper_id": STRING,
        "artifact_path": STRING,
        "release_modes": {"type": "array", "items": TASK_MODES, "uniqueItems": True},
        "selected_workflow_preserved": {"type": "boolean"},
        "repairs": OBJECT_ARRAY,
        "remaining_issues": OBJECT_ARRAY,
        "scientific_audit": {"type": "object"},
        "summary": STRING,
    },
)


__all__ = ["STAGE06_SYNTHESIS_SCHEMA", "STAGE07_AUDIT_SCHEMA"]

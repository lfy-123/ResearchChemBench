from __future__ import annotations

BUILDER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "decision",
        "summary",
        "scientific_record",
        "task",
        "hidden_reference",
        "scoring_rubric",
        "evidence_map",
    ],
    "properties": {
        "decision": {"enum": ["candidate", "abstain"]},
        "summary": {"type": "string", "minLength": 1},
        "abstain_reasons": {"type": "array", "items": {"type": "string"}},
        "scientific_record": {
            "type": "object",
            "required": [
                "computational_object",
                "software",
                "methods",
                "inputs",
                "outputs",
                "workflow",
            ],
            "properties": {
                "computational_object": {"type": "string"},
                "software": {"type": "array", "items": {"type": "string"}},
                "methods": {"type": "array", "items": {"type": "string"}},
                "inputs": {"type": "array", "items": {"type": "string"}},
                "outputs": {"type": "array", "items": {"type": "string"}},
                "workflow": {"type": "array", "items": {"type": "string"}},
            },
        },
        "task": {
            "type": "object",
            "required": [
                "title",
                "objective",
                "instructions",
                "allowed_software",
                "allowed_actions",
                "public_asset_ids",
                "expected_deliverables",
                "resource_requirements",
                "known_limitations",
            ],
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "objective": {"type": "string", "minLength": 1},
                "instructions": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                "allowed_software": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                "allowed_actions": {"type": "array", "items": {"type": "string"}},
                "public_asset_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                "expected_deliverables": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"},
                },
                "resource_requirements": {"type": "object"},
                "known_limitations": {"type": "array", "items": {"type": "string"}},
            },
        },
        "hidden_reference": {
            "type": "object",
            "required": ["expected_results", "grading_notes"],
            "properties": {
                "expected_results": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                "grading_notes": {"type": "array", "items": {"type": "string"}},
            },
        },
        "scoring_rubric": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["criterion", "points", "method"],
                "properties": {
                    "criterion": {"type": "string"},
                    "points": {"type": "number", "minimum": 0, "maximum": 100},
                    "method": {"type": "string"},
                },
            },
        },
        "evidence_map": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["claim", "asset_id", "evidence"],
                "properties": {
                    "claim": {"type": "string"},
                    "asset_id": {"type": "string"},
                    "evidence": {"type": "string"},
                    "location": {"type": "string"},
                },
            },
        },
    },
}

JUDGE_CHECK = {
    "type": "object",
    "required": ["status", "evidence"],
    "properties": {
        "status": {"enum": ["pass", "fail", "uncertain"]},
        "evidence": {"type": "array", "items": {"type": "string"}},
    },
}

JUDGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "decision",
        "summary",
        "checks",
        "blocking_issues",
        "revision_suggestions",
        "residual_risks",
    ],
    "properties": {
        "decision": {"enum": ["pass", "revise", "reject"]},
        "summary": {"type": "string", "minLength": 1},
        "checks": {
            "type": "object",
            "required": [
                "paper_fidelity",
                "data_sufficiency",
                "toolbox_support",
                "answer_leakage",
                "scoring_quality",
                "resource_feasibility",
            ],
            "properties": {
                "paper_fidelity": JUDGE_CHECK,
                "data_sufficiency": JUDGE_CHECK,
                "toolbox_support": JUDGE_CHECK,
                "answer_leakage": JUDGE_CHECK,
                "scoring_quality": JUDGE_CHECK,
                "resource_feasibility": JUDGE_CHECK,
            },
        },
        "blocking_issues": {"type": "array", "items": {"type": "string"}},
        "revision_suggestions": {"type": "array", "items": {"type": "string"}},
        "residual_risks": {"type": "array", "items": {"type": "string"}},
    },
}

from __future__ import annotations

from typing import Any

TASK_TYPES = (
    "paper_reproduction",
    "conclusion_guided_reconstruction",
    "autonomous_research",
    "mechanistic_rule_discovery",
)

LEGACY_TASK_TYPE_MAP = {
    "mechanism_discovery": "autonomous_research",
}

QUERY_TIERS = ("broad", "medium", "narrow")


REQUIRED_SEED_FIELDS = {
    "seed_id",
    "title",
    "scientific_objective",
    "task_modes",
    "facets",
}


def validate_seed(seed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_SEED_FIELDS - seed.keys())
    if missing:
        errors.append(f"missing seed fields: {', '.join(missing)}")
    modes = seed.get("task_modes", [])
    invalid_modes = sorted(
        mode for mode in set(modes) if normalize_task_type(mode) not in TASK_TYPES
    )
    if invalid_modes:
        errors.append(f"invalid task modes: {', '.join(invalid_modes)}")
    facets = seed.get("facets", {})
    if not isinstance(facets, dict):
        errors.append("facets must be an object")
    elif not any(facets.get(name) for name in ("phenomena", "systems", "methods")):
        errors.append("facets must contain at least one phenomenon, system, or method")
    return errors


def validate_scientific_record(
    record: dict[str, Any], *, require_task_selection: bool = True
) -> list[str]:
    errors: list[str] = []
    required = (
        "paper_id",
        "central_problem",
        "inputs",
        "expected_outputs",
        "methods",
        "evidence",
    )
    for field in required:
        if field not in record:
            errors.append(f"missing scientific record field: {field}")
    selected = selected_task_type(record)
    if require_task_selection and not selected:
        errors.append("missing or invalid selected_task_type")
    rejected = record.get("rejected_task_types", [])
    invalid = sorted(mode for mode in set(rejected) if normalize_task_type(mode) not in TASK_TYPES)
    if invalid:
        errors.append(f"invalid rejected task types: {', '.join(invalid)}")
    if not isinstance(record.get("evidence", []), list):
        errors.append("evidence must be a list")
    return errors


def normalize_task_type(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = LEGACY_TASK_TYPE_MAP.get(value, value)
    return normalized if normalized in TASK_TYPES else None


def selected_task_type(record: dict[str, Any]) -> str | None:
    """Return exactly one task type, with a narrow legacy-record fallback."""

    selected = normalize_task_type(record.get("selected_task_type"))
    if selected:
        return selected
    legacy = [
        normalized
        for value in record.get("task_modes", [])
        if (normalized := normalize_task_type(value))
    ]
    return legacy[0] if len(set(legacy)) == 1 else None


def task_types_for_record(record: dict[str, Any]) -> list[str]:
    selected = selected_task_type(record)
    return [selected] if selected else []

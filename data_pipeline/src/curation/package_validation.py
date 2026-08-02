from pathlib import Path
from typing import Any

from src.core.models import TASK_TYPES


def package_readiness(record: dict[str, Any], task_type: str) -> dict[str, Any]:
    """Check whether a curated record can be materialized as one benchmark task."""

    package = record.get("benchmark_package") or {}
    public_inputs = package.get("public_inputs") or {}
    ground_truth = package.get("ground_truth") or {}
    errors: list[str] = []
    if task_type not in TASK_TYPES:
        errors.append(f"unsupported task mode: {task_type}")
    if not package:
        errors.append("missing benchmark_package curation")
    input_sections = ("reaction", "molecular_systems", "observations", "files", "training_systems")
    if not any(public_inputs.get(name) for name in input_sections):
        errors.append("no materializable public inputs")
    errors.extend(_public_file_errors(public_inputs.get("files")))
    if task_type == "paper_reproduction" and not (
        package.get("method_protocol") or record.get("public_method_protocol")
    ):
        errors.append("guided reproduction requires an explicit method protocol")
    if task_type == "conclusion_guided_reconstruction" and not (
        public_inputs.get("target_conclusion")
        or public_inputs.get("disclosed_conclusion")
        or package.get("public_conclusion")
    ):
        errors.append("conclusion-guided reconstruction must disclose the target conclusion")
    if task_type == "mechanistic_rule_discovery":
        training = (
            public_inputs.get("training_systems") or public_inputs.get("molecular_systems") or []
        )
        heldout = public_inputs.get("heldout_systems") or package.get("heldout_design")
        expected_result = ground_truth.get("expected_result") or {}
        hidden_prediction = ground_truth.get("heldout_predictions")
        if not hidden_prediction and isinstance(expected_result, dict):
            hidden_prediction = expected_result.get("heldout_predictions") or expected_result.get(
                "predictions"
            )
        if len(training) < 3:
            errors.append("rule discovery requires at least three comparable training systems")
        if not heldout:
            errors.append("rule discovery requires a solver-visible held-out prediction contract")
        if not hidden_prediction:
            errors.append("rule discovery requires hidden held-out reference outcomes")
    if not ground_truth.get("expected_result"):
        errors.append("missing hidden expected_result")
    if not ground_truth.get("expected_structured_output"):
        errors.append("missing expected_structured_output contract")
    rubric = ground_truth.get("scientific_conclusion_rubric") or []
    if not valid_scientific_rubric(rubric):
        errors.append("scientific_conclusion_rubric must contain complete criteria totaling 100")
    if not (ground_truth.get("evidence_gates") or ground_truth.get("evidence_gate_policy")):
        errors.append("missing task-specific evidence gates")
    if not package_value(package, "scientific_requirements", task_type):
        errors.append("missing scientific requirements")
    if not package_value(package, "leakage_markers", task_type):
        errors.append("missing mode-specific hidden-answer leakage markers")
    return {"passed": not errors, "errors": errors}


def package_value(package: dict[str, Any], key: str, task_type: str) -> Any:
    value = package.get(key)
    return value.get(task_type) if isinstance(value, dict) else value


def valid_scientific_rubric(rubric: list[dict[str, Any]]) -> bool:
    if not 3 <= len(rubric) <= 10:
        return False
    total = 0.0
    for criterion in rubric:
        required_fields = ("id", "statement", "acceptance_rule", "required_evidence")
        if not all(criterion.get(field) for field in required_fields):
            return False
        try:
            total += float(criterion.get("max_score", 0))
        except (TypeError, ValueError):
            return False
    return abs(total - 100.0) < 1e-9


def _public_file_errors(files: Any) -> list[str]:
    if not files:
        return []
    if not isinstance(files, dict):
        return ["public_inputs.files must map relative file names to actual inline content"]
    errors = []
    description_markers = (
        "file with columns",
        "directory containing",
        "not provided",
        "downloadable",
        "must be constructed",
    )
    for relative, value in files.items():
        path = Path(str(relative))
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"unsafe public input path: {relative}")
            continue
        if isinstance(value, dict):
            descriptive = {"description", "path", "file_id", "name", "availability", "status"}
            if not (set(value) - descriptive):
                errors.append(f"public input {relative} is described but has no inline content")
        elif isinstance(value, str):
            lower = value.casefold()
            if any(marker in lower for marker in description_markers) and "\n" not in value:
                errors.append(f"public input {relative} is a description rather than file content")
    return errors

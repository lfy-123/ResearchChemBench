"""MCP tool: validate structured computation output and declared artifacts."""

from __future__ import annotations

import json
import math

from ..adapters.runtime import safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path


TOOL_SPEC = ToolSpec(
    name="validate_computation",
    description="Validate a JSON computation result for required fields, finite numbers, success status, and existing artifacts.",
    category="validation",
    backend="ResearchChemBench deterministic validator",
    tags=("validation", "json", "artifacts"),
    side_effects=("reads computation result and artifact files",),
)


def _finite(value) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, list):
        return all(_finite(item) for item in value)
    if isinstance(value, dict):
        return all(_finite(item) for item in value.values())
    return False


def validate_computation_core(
    result_file: str,
    required_fields: list[str] | None = None,
    artifact_fields: list[str] | None = None,
) -> dict:
    path = safe_input_file(result_file)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Computation result must be a JSON object")
    required_fields = required_fields or []
    artifact_fields = artifact_fields or []
    missing = [field for field in required_fields if field not in value]
    artifacts = {}
    for field in artifact_fields:
        raw = value.get(field)
        if isinstance(raw, str):
            try:
                artifact = safe_input_file(raw)
                artifacts[field] = {"exists": True, "path": relative_workspace_path(artifact)}
            except (FileNotFoundError, ValueError) as exc:
                artifacts[field] = {"exists": False, "error": str(exc)}
        else:
            artifacts[field] = {"exists": False, "error": "field is not a path string"}
    finite = _finite(value)
    backend_success = value.get("status") not in {"error", "failed", "unavailable"}
    valid = not missing and finite and backend_success and all(item["exists"] for item in artifacts.values())
    return {
        "status": "success",
        "backend": "ResearchChemBench deterministic validator",
        "valid": valid,
        "result_file": relative_workspace_path(path),
        "missing_fields": missing,
        "finite_numbers": finite,
        "backend_success": backend_success,
        "artifacts": artifacts,
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def validate_computation(
        result_file: str,
        required_fields: list[str] | None = None,
        artifact_fields: list[str] | None = None,
    ) -> dict:
        arguments = {
            "result_file": result_file,
            "required_fields": required_fields,
            "artifact_fields": artifact_fields,
        }
        return execute_traced(TOOL_SPEC.name, arguments, lambda: validate_computation_core(**arguments))


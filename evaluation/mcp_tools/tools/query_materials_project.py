"""MCP tool: query Materials Project with an explicitly configured API key."""

from __future__ import annotations

import os

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="query_materials_project",
    description="Query Materials Project summary data by material ID or chemical formula using MP_API_KEY.",
    category="external_data",
    backend="Materials Project mp-api",
    dependencies=("mp-api",),
    tags=("materials_project", "materials", "structure", "properties"),
    requires_network=True,
    side_effects=("authenticated Materials Project request",),
)


def query_materials_project_core(
    material_id: str = "",
    formula: str = "",
    max_records: int = 10,
) -> dict:
    if bool(material_id.strip()) == bool(formula.strip()):
        raise ValueError("provide exactly one of material_id or formula")
    if max_records < 1 or max_records > 100:
        raise ValueError("max_records must be between 1 and 100")
    api_key = os.environ.get("MP_API_KEY", "").strip()
    if not api_key:
        return unavailable_result(
            "Materials Project mp-api",
            reason="MP_API_KEY is not configured",
            manual_action="Obtain a Materials Project API key and set MP_API_KEY for the MCP server.",
        )
    if not module_available("mp_api"):
        return unavailable_result(
            "Materials Project mp-api",
            reason="mp_api is not installed",
            manual_action="Install the services MCP profile environment (.tool_envs/services).",
        )
    from mp_api.client import MPRester

    fields = ["material_id", "formula_pretty", "symmetry", "band_gap", "energy_above_hull", "is_stable"]
    with MPRester(api_key) as rester:
        if material_id:
            documents = rester.materials.summary.search(material_ids=[material_id], fields=fields)
        else:
            documents = rester.materials.summary.search(formula=formula, fields=fields)
    records = []
    for document in documents[:max_records]:
        value = document.model_dump(mode="json") if hasattr(document, "model_dump") else dict(document)
        # emmet-core's MPID serializer can emit a malformed value with some
        # Pydantic combinations even though the document attribute is correct.
        # Normalize from the public attribute before returning data to an Agent.
        document_material_id = getattr(document, "material_id", None)
        if document_material_id is not None:
            value["material_id"] = str(document_material_id)
        records.append(value)
    return {"status": "success", "backend": "Materials Project mp-api", "count": len(records), "records": records}


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def query_materials_project(material_id: str = "", formula: str = "", max_records: int = 10) -> dict:
        arguments = {"material_id": material_id, "formula": formula, "max_records": max_records}
        return execute_traced(TOOL_SPEC.name, arguments, lambda: query_materials_project_core(**arguments))

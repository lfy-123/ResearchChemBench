"""MCP tool: list registered chemistry software and logical capabilities."""

from __future__ import annotations

from ..adapters.toolbox_registry import software_entries
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="list_toolbox_capabilities",
    description="List managed chemistry backends, capabilities, MCP tools, and configured status.",
    category="toolbox_management",
    backend="ResearchChemBench registry",
    dependencies=("pyyaml",),
    tags=("registry", "capabilities", "discovery"),
)


def list_toolbox_capabilities_core(
    category: str = "",
    status: str = "",
) -> dict:
    entries = software_entries()
    if category:
        entries = [entry for entry in entries if entry.get("category") == category]
    if status:
        entries = [entry for entry in entries if entry.get("status") == status]
    return {
        "status": "success",
        "count": len(entries),
        "software": [
            {
                "name": entry.get("name"),
                "category": entry.get("category"),
                "capabilities": entry.get("capabilities", []),
                "mcp_tools": entry.get("mcp_tools", []),
                "configured_status": entry.get("status"),
            }
            for entry in entries
        ],
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def list_toolbox_capabilities(category: str = "", status: str = "") -> dict:
        return execute_traced(
            TOOL_SPEC.name,
            {"category": category, "status": status},
            lambda: list_toolbox_capabilities_core(category, status),
        )


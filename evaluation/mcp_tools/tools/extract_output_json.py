"""MCP tool: read a JSON result produced by a chemistry calculation."""

from __future__ import annotations

from ..models import ToolSpec
from ..settings import ensure_chemgraph_on_path
from ..tracing import execute_traced
from ..workspace import resolve_workspace_path


TOOL_SPEC = ToolSpec(
    name="extract_output_json",
    description="Read a JSON result file produced by run_ase from the active workspace.",
    category="result_io",
    backend="ChemGraph",
    dependencies=(),
    tags=("json", "results"),
    side_effects=("reads result file",),
)


def register(mcp) -> None:
    ensure_chemgraph_on_path()
    from chemgraph.tools.ase_core import extract_output_json_core

    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def extract_output_json(json_file: str) -> dict:
        safe_path = resolve_workspace_path(json_file, must_exist=True)
        return execute_traced(
            TOOL_SPEC.name,
            {"json_file": json_file},
            lambda: extract_output_json_core(str(safe_path)),
        )

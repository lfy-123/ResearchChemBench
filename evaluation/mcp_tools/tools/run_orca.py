"""MCP tool: run a user-installed ORCA executable without bundling it."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_orca",
    description="Run a licensed user-provided ORCA executable on a workspace input file; ORCA is never downloaded by this project.",
    category="quantum_chemistry",
    backend="ORCA",
    executables=("orca",),
    tags=("orca", "licensed", "energy", "optimization"),
    side_effects=("runs configured ORCA installation", "writes ORCA output files"),
)


def run_orca_core(
    input_file: str,
    output_directory: str = "outputs/orca",
    timeout_seconds: int = 7200,
) -> dict:
    source = safe_input_file(input_file)
    return run_external(
        backend="ORCA",
        executable="orca",
        arguments=[str(source)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_ORCA_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_orca(input_file: str, output_directory: str = "outputs/orca", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_orca_core(**arguments))


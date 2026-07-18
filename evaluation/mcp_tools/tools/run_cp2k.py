"""MCP tool: run a configured CP2K executable."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_cp2k",
    description="Run CP2K on a workspace input deck using an installed or CHEMGRAPH_CP2K_COMMAND-configured executable.",
    category="periodic_dft",
    backend="CP2K",
    executables=("cp2k",),
    tags=("cp2k", "periodic", "dft", "molecular_dynamics"),
    side_effects=("runs CP2K", "writes CP2K output files"),
)


def run_cp2k_core(input_file: str, output_directory: str = "outputs/cp2k", timeout_seconds: int = 7200) -> dict:
    source = safe_input_file(input_file)
    return run_external(
        backend="CP2K",
        executable="cp2k",
        arguments=["-i", str(source)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_CP2K_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_cp2k(input_file: str, output_directory: str = "outputs/cp2k", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_cp2k_core(**arguments))


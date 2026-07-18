"""MCP tool: run LAMMPS from a workspace input script."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_lammps",
    description="Run LAMMPS from a workspace input script using a configured lmp executable.",
    category="molecular_dynamics",
    backend="LAMMPS",
    executables=("lmp",),
    tags=("lammps", "md", "materials"),
    side_effects=("runs LAMMPS", "writes trajectory and restart files"),
)


def run_lammps_core(input_file: str, output_directory: str = "outputs/lammps", timeout_seconds: int = 7200) -> dict:
    source = safe_input_file(input_file)
    return run_external(
        backend="LAMMPS",
        executable="lmp",
        arguments=["-in", str(source)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_LAMMPS_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_lammps(input_file: str, output_directory: str = "outputs/lammps", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_lammps_core(**arguments))


"""MCP tool: run PLUMED driver analysis."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_plumed",
    description="Run PLUMED driver on a workspace PLUMED input and optional XTC trajectory.",
    category="enhanced_sampling",
    backend="PLUMED",
    executables=("plumed",),
    tags=("plumed", "collective_variables", "trajectory"),
    side_effects=("runs PLUMED driver", "writes collective-variable output files"),
)


def run_plumed_core(
    plumed_file: str,
    trajectory_file: str = "",
    output_directory: str = "outputs/plumed",
    timeout_seconds: int = 3600,
) -> dict:
    source = safe_input_file(plumed_file)
    arguments = ["driver", "--plumed", str(source)]
    if trajectory_file:
        trajectory = safe_input_file(trajectory_file)
        arguments.extend(["--mf_xtc", str(trajectory)])
    return run_external(
        backend="PLUMED",
        executable="plumed",
        arguments=arguments,
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_PLUMED_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_plumed(plumed_file: str, trajectory_file: str = "", output_directory: str = "outputs/plumed", timeout_seconds: int = 3600) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_plumed_core(**arguments))


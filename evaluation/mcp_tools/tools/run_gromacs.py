"""MCP tool: run a GROMACS mdrun from a prepared TPR file."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_gromacs",
    description="Run GROMACS mdrun from a prepared workspace TPR file; system preparation remains a separate tool.",
    category="molecular_dynamics",
    backend="GROMACS",
    executables=("gmx",),
    tags=("gromacs", "md", "simulation"),
    side_effects=("runs GROMACS", "writes trajectory and checkpoint files"),
)


def run_gromacs_core(
    tpr_file: str,
    output_directory: str = "outputs/gromacs",
    deffnm: str = "run",
    timeout_seconds: int = 7200,
) -> dict:
    if not deffnm.replace("_", "").replace("-", "").isalnum():
        raise ValueError("deffnm must contain only letters, numbers, underscore, or hyphen")
    source = safe_input_file(tpr_file)
    return run_external(
        backend="GROMACS",
        executable="gmx",
        arguments=["mdrun", "-s", str(source), "-deffnm", deffnm],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_GROMACS_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_gromacs(tpr_file: str, output_directory: str = "outputs/gromacs", deffnm: str = "run", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_gromacs_core(**arguments))


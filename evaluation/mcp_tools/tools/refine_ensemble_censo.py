"""MCP tool: run CENSO ensemble refinement."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="refine_ensemble_censo",
    description="Run a configured CENSO executable on a workspace conformer ensemble.",
    category="conformer_search",
    backend="CENSO",
    executables=("censo",),
    tags=("censo", "ensemble", "thermochemistry"),
    side_effects=("runs CENSO", "writes refined ensemble files"),
)


def refine_ensemble_censo_core(
    ensemble_file: str,
    output_directory: str = "outputs/censo",
    max_cores: int = 1,
    timeout_seconds: int = 7200,
) -> dict:
    if max_cores < 1:
        raise ValueError("max_cores must be positive")
    source = safe_input_file(ensemble_file)
    return run_external(
        backend="CENSO",
        executable="censo",
        arguments=["-i", str(source), "--maxcores", str(max_cores)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_CENSO_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def refine_ensemble_censo(
        ensemble_file: str,
        output_directory: str = "outputs/censo",
        max_cores: int = 1,
        timeout_seconds: int = 7200,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: refine_ensemble_censo_core(**arguments))

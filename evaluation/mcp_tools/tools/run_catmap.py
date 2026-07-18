"""MCP tool: run a prepared CatMAP model."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_catmap",
    description="Run a prepared CatMAP model file with a configured CatMAP command-line entry point.",
    category="catalysis",
    backend="CatMAP",
    dependencies=("catmap",),
    executables=("catmap",),
    tags=("catmap", "microkinetics", "catalysis"),
    side_effects=("runs CatMAP", "writes microkinetic model outputs"),
)


def run_catmap_core(model_file: str, output_directory: str = "outputs/catmap", timeout_seconds: int = 3600) -> dict:
    source = safe_input_file(model_file)
    return run_external(
        backend="CatMAP",
        executable="catmap",
        arguments=[str(source)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_CATMAP_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_catmap(model_file: str, output_directory: str = "outputs/catmap", timeout_seconds: int = 3600) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_catmap_core(**arguments))


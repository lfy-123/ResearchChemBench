"""MCP tool: run a prepared intrinsic reaction-coordinate workflow."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_irc",
    description="Run a prepared pysisyphus intrinsic reaction-coordinate input from the active workspace.",
    category="reaction_path",
    backend="pysisyphus",
    dependencies=("pysisyphus",),
    executables=("pysis",),
    tags=("irc", "reaction_path", "pysisyphus"),
    side_effects=("runs IRC workflow", "writes reaction-path files"),
)


def run_irc_core(input_file: str, output_directory: str = "outputs/irc", timeout_seconds: int = 7200) -> dict:
    source = safe_input_file(input_file)
    return run_external(
        backend="pysisyphus IRC",
        executable="pysis",
        arguments=[str(source)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_PYSIS_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_irc(input_file: str, output_directory: str = "outputs/irc", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_irc_core(**arguments))


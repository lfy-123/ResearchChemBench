"""MCP tool: run a prepared transition-state workflow."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="find_transition_state",
    description="Run a prepared pysisyphus transition-state input; backend choice remains explicit and input construction is separate.",
    category="reaction_path",
    backend="pysisyphus",
    dependencies=("pysisyphus",),
    executables=("pysis",),
    tags=("transition_state", "pysisyphus", "saddle_point"),
    side_effects=("runs transition-state workflow", "writes optimization files"),
)


def find_transition_state_core(
    input_file: str,
    output_directory: str = "outputs/transition_state",
    backend: str = "pysisyphus",
    timeout_seconds: int = 7200,
) -> dict:
    if backend != "pysisyphus":
        return unavailable_result(
            backend,
            reason="Only prepared pysisyphus inputs are integrated in this initial version",
            manual_action="Provide a pysisyphus YAML input or add a reviewed backend adapter.",
        )
    source = safe_input_file(input_file)
    return run_external(
        backend="pysisyphus",
        executable="pysis",
        arguments=[str(source)],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_PYSIS_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def find_transition_state(input_file: str, output_directory: str = "outputs/transition_state", backend: str = "pysisyphus", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: find_transition_state_core(**arguments))


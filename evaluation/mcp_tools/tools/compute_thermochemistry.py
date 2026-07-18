"""MCP tool: run GoodVibes thermochemistry analysis."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="compute_thermochemistry",
    description="Compute GoodVibes thermochemistry from one parsed quantum-chemistry output file.",
    category="thermochemistry",
    backend="GoodVibes",
    dependencies=("goodvibes",),
    executables=("goodvibes",),
    tags=("thermochemistry", "goodvibes", "quasiharmonic"),
    side_effects=("runs GoodVibes", "writes thermochemistry logs"),
)


def compute_thermochemistry_core(
    output_file: str,
    output_directory: str = "outputs/goodvibes",
    temperature_kelvin: float = 298.15,
    frequency_scale: float = 1.0,
    timeout_seconds: int = 600,
) -> dict:
    if temperature_kelvin <= 0 or frequency_scale <= 0:
        raise ValueError("temperature_kelvin and frequency_scale must be positive")
    source = safe_input_file(output_file)
    arguments = ["-t", str(temperature_kelvin), "--fs", str(frequency_scale), str(source)]
    return run_external(
        backend="GoodVibes",
        executable="goodvibes",
        arguments=arguments,
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_GOODVIBES_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def compute_thermochemistry(
        output_file: str,
        output_directory: str = "outputs/goodvibes",
        temperature_kelvin: float = 298.15,
        frequency_scale: float = 1.0,
        timeout_seconds: int = 600,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: compute_thermochemistry_core(**arguments))


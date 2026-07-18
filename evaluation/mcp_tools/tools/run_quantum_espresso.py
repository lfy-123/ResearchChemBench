"""MCP tool: run Quantum ESPRESSO pw.x from a workspace input file."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_quantum_espresso",
    description="Run Quantum ESPRESSO pw.x with a workspace input deck and configured pseudopotentials.",
    category="periodic_dft",
    backend="Quantum ESPRESSO pw.x",
    executables=("pw.x",),
    tags=("quantum_espresso", "periodic", "dft"),
    side_effects=("runs pw.x", "writes periodic DFT output files"),
)


def run_quantum_espresso_core(
    input_file: str,
    output_directory: str = "outputs/quantum_espresso",
    timeout_seconds: int = 7200,
) -> dict:
    source = safe_input_file(input_file)
    return run_external(
        backend="Quantum ESPRESSO pw.x",
        executable="pw.x",
        arguments=[],
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_QE_COMMAND",
        timeout_seconds=timeout_seconds,
        stdin_text=source.read_text(encoding="utf-8"),
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_quantum_espresso(input_file: str, output_directory: str = "outputs/quantum_espresso", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_quantum_espresso_core(**arguments))


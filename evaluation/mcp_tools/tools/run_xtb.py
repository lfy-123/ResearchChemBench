"""MCP tool: run the standalone xTB executable."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_xtb",
    description="Run standalone xTB with an explicit GFN backend, charge, spin, and optional geometry optimization.",
    category="quantum_chemistry",
    backend="xTB",
    executables=("xtb",),
    tags=("xtb", "gfn1", "gfn2", "energy", "optimization"),
    side_effects=("runs xTB", "writes xTB output files"),
)


def run_xtb_core(
    input_structure_file: str,
    output_directory: str = "outputs/xtb",
    method: str = "gfn2",
    charge: int = 0,
    unpaired_electrons: int = 0,
    optimize: bool = False,
    timeout_seconds: int = 1800,
) -> dict:
    method_number = {"gfn1": "1", "gfn2": "2"}.get(method)
    if method_number is None:
        raise ValueError("method must be gfn1 or gfn2")
    source = safe_input_file(input_structure_file)
    arguments = [str(source), "--gfn", method_number, "--chrg", str(charge), "--uhf", str(unpaired_electrons)]
    if optimize:
        arguments.append("--opt")
    return run_external(
        backend=f"xTB/{method.upper()}",
        executable="xtb",
        arguments=arguments,
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_XTB_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_xtb(
        input_structure_file: str,
        output_directory: str = "outputs/xtb",
        method: str = "gfn2",
        charge: int = 0,
        unpaired_electrons: int = 0,
        optimize: bool = False,
        timeout_seconds: int = 1800,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_xtb_core(**arguments))


"""MCP tool: run CREST conformer search."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="generate_conformers_crest",
    description="Run a CREST conformer search from a workspace XYZ file with explicit charge and spin settings.",
    category="conformer_search",
    backend="CREST/xTB",
    executables=("crest",),
    tags=("crest", "conformers", "xtb"),
    side_effects=("runs CREST", "writes conformer ensemble files"),
)


def generate_conformers_crest_core(
    input_structure_file: str,
    output_directory: str = "outputs/crest",
    charge: int = 0,
    unpaired_electrons: int = 0,
    method: str = "gfn2",
    timeout_seconds: int = 3600,
) -> dict:
    if method not in {"gfn1", "gfn2", "gfnff"}:
        raise ValueError("method must be gfn1, gfn2, or gfnff")
    source = safe_input_file(input_structure_file)
    arguments = [str(source), f"--{method}", "--chrg", str(charge), "--uhf", str(unpaired_electrons)]
    return run_external(
        backend="CREST",
        executable="crest",
        arguments=arguments,
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_CREST_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def generate_conformers_crest(
        input_structure_file: str,
        output_directory: str = "outputs/crest",
        charge: int = 0,
        unpaired_electrons: int = 0,
        method: str = "gfn2",
        timeout_seconds: int = 3600,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: generate_conformers_crest_core(**arguments))


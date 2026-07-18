"""MCP tool: convert molecular or periodic structure files with ASE."""

from __future__ import annotations

from ..adapters.runtime import module_available, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="convert_structure",
    description="Convert a structure file between ASE-supported formats while preserving the active workspace boundary.",
    category="data_structure",
    backend="ASE",
    dependencies=("ase",),
    tags=("structure", "conversion", "io"),
    side_effects=("writes converted structure file",),
)


def convert_structure_core(
    input_file: str,
    output_file: str,
    input_format: str = "",
    output_format: str = "",
) -> dict:
    if not module_available("ase"):
        return unavailable_result("ASE", reason="ase is not installed", manual_action="Install ase in .toolbox_env.")
    from ase.io import read, write

    source = safe_input_file(input_file)
    destination = resolve_workspace_output_path(output_file)
    atoms = read(source, format=input_format or None)
    write(destination, atoms, format=output_format or None)
    return {
        "status": "success",
        "backend": "ASE",
        "input_file": relative_workspace_path(source),
        "output_file": relative_workspace_path(destination),
        "atom_count": len(atoms),
        "chemical_formula": atoms.get_chemical_formula(),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def convert_structure(
        input_file: str,
        output_file: str,
        input_format: str = "",
        output_format: str = "",
    ) -> dict:
        arguments = {
            "input_file": input_file,
            "output_file": output_file,
            "input_format": input_format,
            "output_format": output_format,
        }
        return execute_traced(TOOL_SPEC.name, arguments, lambda: convert_structure_core(**arguments))


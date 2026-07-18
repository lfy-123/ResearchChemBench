"""MCP tool: parse quantum-chemistry output with cclib."""

from __future__ import annotations

from ..adapters.runtime import module_available, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path


TOOL_SPEC = ToolSpec(
    name="analyze_wavefunction",
    description="Parse supported quantum-chemistry output with cclib and return energies, orbital indices, charges, and metadata.",
    category="wavefunction_analysis",
    backend="cclib",
    dependencies=("cclib",),
    tags=("cclib", "wavefunction", "output_parser", "orbitals"),
    side_effects=("reads quantum-chemistry output",),
)


def _list(value):
    return value.tolist() if hasattr(value, "tolist") else value


def analyze_wavefunction_core(output_file: str) -> dict:
    if not module_available("cclib"):
        return unavailable_result("cclib", reason="cclib is not installed", manual_action="Install cclib in .toolbox_env.")
    from cclib.io import ccopen

    source = safe_input_file(output_file)
    parser = ccopen(str(source))
    if parser is None:
        raise ValueError(f"cclib could not identify output format: {source.name}")
    data = parser.parse()
    homos = _list(getattr(data, "homos", []))
    orbital_energies = _list(getattr(data, "moenergies", []))
    return {
        "status": "success",
        "backend": "cclib",
        "output_file": relative_workspace_path(source),
        "metadata": getattr(data, "metadata", {}),
        "atom_numbers": _list(getattr(data, "atomnos", [])),
        "scf_energies_ev": _list(getattr(data, "scfenergies", [])),
        "homo_indices": homos,
        "orbital_energies_ev": orbital_energies,
        "mulliken_charges": _list(getattr(data, "atomcharges", {}).get("mulliken", [])),
        "attributes": sorted(data.getattributes().keys()),
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def analyze_wavefunction(output_file: str) -> dict:
        return execute_traced(TOOL_SPEC.name, {"output_file": output_file}, lambda: analyze_wavefunction_core(output_file))


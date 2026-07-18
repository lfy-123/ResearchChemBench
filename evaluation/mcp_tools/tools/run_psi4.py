"""MCP tool: run a bounded Psi4 single-point calculation."""

from __future__ import annotations

import json

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="run_psi4",
    description="Run a Psi4 molecular single-point energy using an explicit method, basis, memory, and thread count.",
    category="quantum_chemistry",
    backend="Psi4",
    dependencies=("psi4",),
    executables=("psi4",),
    tags=("psi4", "energy", "wavefunction"),
    side_effects=("runs Psi4", "writes Psi4 text and JSON outputs"),
)


def run_psi4_core(
    geometry: str,
    method: str = "hf",
    basis: str = "sto-3g",
    output_file: str = "outputs/psi4_result.json",
    memory_mb: int = 500,
    threads: int = 1,
) -> dict:
    if not geometry.strip() or memory_mb < 100 or threads < 1 or threads > 128:
        raise ValueError("geometry, memory_mb, or threads are invalid")
    if not module_available("psi4"):
        return unavailable_result(
            "Psi4",
            reason="psi4 is not installed",
            manual_action="Install the psi4 MCP profile environment (.tool_envs/psi4).",
        )
    import psi4

    destination = resolve_workspace_output_path(output_file)
    text_output = destination.with_suffix(".out")
    psi4.core.clean()
    psi4.set_memory(f"{memory_mb} MB")
    psi4.set_num_threads(threads)
    psi4.core.set_output_file(str(text_output), False)
    molecule = psi4.geometry(geometry)
    energy = float(psi4.energy(f"{method}/{basis}", molecule=molecule))
    result = {
        "status": "success",
        "backend": "Psi4",
        "method": method,
        "basis": basis,
        "energy_hartree": energy,
        "text_output": relative_workspace_path(text_output),
    }
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result["output_file"] = relative_workspace_path(destination)
    return result


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_psi4(
        geometry: str,
        method: str = "hf",
        basis: str = "sto-3g",
        output_file: str = "outputs/psi4_result.json",
        memory_mb: int = 500,
        threads: int = 1,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_psi4_core(**arguments))

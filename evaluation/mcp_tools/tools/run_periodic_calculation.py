"""MCP tool: dispatch an explicit periodic electronic-structure backend."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_periodic_calculation",
    description="Run an explicit QE, CP2K, DFTB+, SIESTA, or ABINIT backend from a prepared workspace input deck.",
    category="periodic_dft",
    backend="QE/CP2K/DFTB+/SIESTA/ABINIT",
    executables=("pw.x", "cp2k", "dftb+", "siesta", "abinit"),
    tags=("periodic", "dft", "backend_dispatch"),
    side_effects=("runs selected periodic backend", "writes calculation files"),
)


BACKENDS = {
    "quantum_espresso": ("Quantum ESPRESSO", "pw.x", "CHEMGRAPH_QE_COMMAND", "stdin"),
    "cp2k": ("CP2K", "cp2k", "CHEMGRAPH_CP2K_COMMAND", "cp2k"),
    "dftbplus": ("DFTB+", "dftb+", "CHEMGRAPH_DFTBPLUS_COMMAND", "none"),
    "siesta": ("SIESTA", "siesta", "CHEMGRAPH_SIESTA_COMMAND", "stdin"),
    "abinit": ("ABINIT", "abinit", "CHEMGRAPH_ABINIT_COMMAND", "stdin"),
}


def run_periodic_calculation_core(
    backend: str,
    input_file: str,
    output_directory: str = "outputs/periodic",
    timeout_seconds: int = 7200,
) -> dict:
    if backend not in BACKENDS:
        raise ValueError(f"backend must be one of {sorted(BACKENDS)}")
    label, executable, variable, mode = BACKENDS[backend]
    source = safe_input_file(input_file)
    arguments = ["-i", str(source)] if mode == "cp2k" else []
    stdin_text = source.read_text(encoding="utf-8") if mode == "stdin" else None
    return run_external(
        backend=label,
        executable=executable,
        arguments=arguments,
        output_directory=output_directory,
        environment_variable=variable,
        timeout_seconds=timeout_seconds,
        stdin_text=stdin_text,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_periodic_calculation(backend: str, input_file: str, output_directory: str = "outputs/periodic", timeout_seconds: int = 7200) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_periodic_calculation_core(**arguments))


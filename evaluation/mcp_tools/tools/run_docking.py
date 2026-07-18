"""MCP tool: run AutoDock Vina or GNINA docking."""

from __future__ import annotations

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_docking",
    description="Run an explicit AutoDock Vina or GNINA backend with workspace-confined receptor, ligand, and outputs.",
    category="docking",
    backend="AutoDock Vina/GNINA",
    executables=("vina", "gnina"),
    tags=("docking", "vina", "gnina"),
    side_effects=("runs docking software", "writes poses and score logs"),
)


def run_docking_core(
    receptor_file: str,
    ligand_file: str,
    center: list[float],
    size: list[float],
    output_directory: str = "outputs/docking",
    backend: str = "vina",
    exhaustiveness: int = 8,
    timeout_seconds: int = 3600,
) -> dict:
    if backend not in {"vina", "gnina"}:
        raise ValueError("backend must be vina or gnina")
    if len(center) != 3 or len(size) != 3 or exhaustiveness < 1:
        raise ValueError("center/size must contain three values and exhaustiveness must be positive")
    receptor = safe_input_file(receptor_file)
    ligand = safe_input_file(ligand_file)
    arguments = [
        "--receptor", str(receptor), "--ligand", str(ligand),
        "--center_x", str(center[0]), "--center_y", str(center[1]), "--center_z", str(center[2]),
        "--size_x", str(size[0]), "--size_y", str(size[1]), "--size_z", str(size[2]),
        "--exhaustiveness", str(exhaustiveness), "--out", "poses.pdbqt",
    ]
    return run_external(
        backend="AutoDock Vina" if backend == "vina" else "GNINA",
        executable=backend,
        arguments=arguments,
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_VINA_COMMAND" if backend == "vina" else "CHEMGRAPH_GNINA_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_docking(
        receptor_file: str,
        ligand_file: str,
        center: list[float],
        size: list[float],
        output_directory: str = "outputs/docking",
        backend: str = "vina",
        exhaustiveness: int = 8,
        timeout_seconds: int = 3600,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_docking_core(**arguments))


"""MCP tool: analyze a trajectory with MDAnalysis."""

from __future__ import annotations

from ..adapters.runtime import module_available, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path


TOOL_SPEC = ToolSpec(
    name="analyze_md_trajectory",
    description="Analyze topology/trajectory frames, selected atom counts, radius of gyration, and coordinate bounds with MDAnalysis.",
    category="molecular_dynamics",
    backend="MDAnalysis",
    dependencies=("MDAnalysis",),
    tags=("trajectory", "mdanalysis", "analysis"),
    side_effects=("reads topology and trajectory files",),
)


def analyze_md_trajectory_core(
    topology_file: str,
    trajectory_file: str = "",
    selection: str = "all",
    max_frames: int = 1000,
) -> dict:
    if max_frames < 1 or max_frames > 100_000:
        raise ValueError("max_frames must be between 1 and 100000")
    if not module_available("MDAnalysis"):
        return unavailable_result(
            "MDAnalysis",
            reason="MDAnalysis is not installed",
            manual_action="Install the md MCP profile environment (.tool_envs/md).",
        )
    import MDAnalysis as mda
    import numpy as np

    topology = safe_input_file(topology_file)
    trajectory = safe_input_file(trajectory_file) if trajectory_file else None
    universe = mda.Universe(str(topology), *([str(trajectory)] if trajectory else []))
    atoms = universe.select_atoms(selection)
    if len(atoms) == 0:
        raise ValueError("selection matched zero atoms")
    radii = []
    minima = []
    maxima = []
    for index, _frame in enumerate(universe.trajectory):
        if index >= max_frames:
            break
        coordinates = atoms.positions.copy()
        center = coordinates.mean(axis=0)
        radii.append(float(np.sqrt(np.mean(np.sum((coordinates - center) ** 2, axis=1)))))
        minima.append(coordinates.min(axis=0).tolist())
        maxima.append(coordinates.max(axis=0).tolist())
    return {
        "status": "success",
        "backend": "MDAnalysis",
        "topology_file": relative_workspace_path(topology),
        "trajectory_file": relative_workspace_path(trajectory) if trajectory else None,
        "selection": selection,
        "selected_atom_count": len(atoms),
        "frame_count": len(radii),
        "radius_of_gyration_like_angstrom": radii,
        "coordinate_minima": minima,
        "coordinate_maxima": maxima,
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def analyze_md_trajectory(topology_file: str, trajectory_file: str = "", selection: str = "all", max_frames: int = 1000) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: analyze_md_trajectory_core(**arguments))

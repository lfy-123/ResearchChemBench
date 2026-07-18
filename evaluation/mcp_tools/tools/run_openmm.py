"""MCP tool: minimize and optionally propagate a prepared PDB with OpenMM."""

from __future__ import annotations

import json

from ..adapters.runtime import module_available, safe_input_file, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced
from ..workspace import relative_workspace_path, resolve_workspace_output_path


TOOL_SPEC = ToolSpec(
    name="run_openmm",
    description="Run a small OpenMM minimization/MD job from a prepared PDB using whitelisted built-in force fields.",
    category="molecular_dynamics",
    backend="OpenMM",
    dependencies=("openmm",),
    tags=("openmm", "minimization", "md"),
    side_effects=("runs OpenMM", "writes final PDB and result JSON"),
)


ALLOWED_FORCE_FIELDS = {
    "amber14-all.xml",
    "amber14/tip3pfb.xml",
    "amber14/tip3p.xml",
    "tip3p.xml",
}


def run_openmm_core(
    input_pdb: str,
    output_pdb: str = "outputs/openmm_final.pdb",
    result_file: str = "outputs/openmm_result.json",
    force_fields: list[str] | None = None,
    temperature_kelvin: float = 300.0,
    steps: int = 0,
) -> dict:
    force_fields = force_fields or ["amber14-all.xml", "amber14/tip3pfb.xml"]
    if any(item not in ALLOWED_FORCE_FIELDS for item in force_fields):
        raise ValueError(f"force_fields must be selected from {sorted(ALLOWED_FORCE_FIELDS)}")
    if temperature_kelvin <= 0 or steps < 0 or steps > 10_000_000:
        raise ValueError("temperature_kelvin or steps is invalid")
    if not module_available("openmm"):
        return unavailable_result(
            "OpenMM",
            reason="openmm is not installed",
            manual_action="Install the md MCP profile environment (.tool_envs/md).",
        )
    import openmm
    from openmm import unit
    from openmm.app import ForceField, NoCutoff, PDBFile, Simulation

    source = safe_input_file(input_pdb)
    final_path = resolve_workspace_output_path(output_pdb)
    result_path = resolve_workspace_output_path(result_file)
    pdb = PDBFile(str(source))
    forcefield = ForceField(*force_fields)
    system = forcefield.createSystem(pdb.topology, nonbondedMethod=NoCutoff, constraints=None)
    integrator = openmm.LangevinMiddleIntegrator(temperature_kelvin * unit.kelvin, 1 / unit.picosecond, 0.001 * unit.picoseconds)
    simulation = Simulation(pdb.topology, system, integrator)
    simulation.context.setPositions(pdb.positions)
    simulation.minimizeEnergy()
    if steps:
        simulation.context.setVelocitiesToTemperature(temperature_kelvin * unit.kelvin, 2025)
        simulation.step(steps)
    state = simulation.context.getState(getEnergy=True, getPositions=True)
    energy = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    with final_path.open("w", encoding="utf-8") as handle:
        PDBFile.writeFile(pdb.topology, state.getPositions(), handle)
    result = {
        "status": "success",
        "backend": "OpenMM",
        "force_fields": force_fields,
        "steps": steps,
        "potential_energy_kj_mol": float(energy),
        "output_pdb": relative_workspace_path(final_path),
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result["result_file"] = relative_workspace_path(result_path)
    return result


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_openmm(
        input_pdb: str,
        output_pdb: str = "outputs/openmm_final.pdb",
        result_file: str = "outputs/openmm_result.json",
        force_fields: list[str] | None = None,
        temperature_kelvin: float = 300.0,
        steps: int = 0,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_openmm_core(**arguments))

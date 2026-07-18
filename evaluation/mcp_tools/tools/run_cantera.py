"""MCP tool: run a Cantera gas-phase equilibrium calculation."""

from __future__ import annotations

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_cantera",
    description="Run a Cantera gas-phase equilibrium calculation with a built-in mechanism and explicit thermodynamic mode.",
    category="reaction_kinetics",
    backend="Cantera",
    dependencies=("cantera",),
    tags=("cantera", "equilibrium", "kinetics", "thermochemistry"),
)


ALLOWED_MECHANISMS = {"gri30.yaml", "h2o2.yaml", "air.yaml", "nDodecane_Reitz.yaml"}
ALLOWED_EQUILIBRIUM_MODES = {"TP", "TV", "HP", "SP", "SV", "UV"}


def run_cantera_core(
    composition: str,
    temperature_kelvin: float = 1000.0,
    pressure_pa: float = 101325.0,
    mechanism: str = "gri30.yaml",
    equilibrate: str = "HP",
) -> dict:
    if mechanism not in ALLOWED_MECHANISMS or equilibrate not in ALLOWED_EQUILIBRIUM_MODES:
        raise ValueError("mechanism or equilibrate mode is not allowed")
    if temperature_kelvin <= 0 or pressure_pa <= 0 or not composition.strip():
        raise ValueError("composition, temperature, and pressure must be valid")
    if not module_available("cantera"):
        return unavailable_result(
            "Cantera",
            reason="cantera is not installed",
            manual_action="Install the reaction MCP profile environment (.tool_envs/reaction).",
        )
    import cantera as ct

    gas = ct.Solution(mechanism)
    gas.TPX = temperature_kelvin, pressure_pa, composition
    gas.equilibrate(equilibrate)
    species = sorted(
        (
            {"name": gas.species_names[index], "mole_fraction": float(value)}
            for index, value in enumerate(gas.X)
            if value > 1e-10
        ),
        key=lambda item: item["mole_fraction"],
        reverse=True,
    )
    return {
        "status": "success",
        "backend": "Cantera",
        "mechanism": mechanism,
        "equilibrium_mode": equilibrate,
        "temperature_kelvin": float(gas.T),
        "pressure_pa": float(gas.P),
        "enthalpy_mole_j_mol": float(gas.enthalpy_mole),
        "gibbs_mole_j_mol": float(gas.gibbs_mole),
        "major_species": species[:20],
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_cantera(
        composition: str,
        temperature_kelvin: float = 1000.0,
        pressure_pa: float = 101325.0,
        mechanism: str = "gri30.yaml",
        equilibrate: str = "HP",
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_cantera_core(**arguments))

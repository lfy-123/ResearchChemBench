"""MCP tool: solve a small mass-action microkinetic model."""

from __future__ import annotations

import math

from ..adapters.runtime import module_available, unavailable_result
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_reaction_kinetics",
    description="Integrate a user-specified irreversible mass-action reaction network with SciPy.",
    category="reaction_kinetics",
    backend="SciPy solve_ivp",
    dependencies=("scipy",),
    tags=("microkinetics", "ode", "mass_action"),
)


def run_reaction_kinetics_core(
    species: list[str],
    initial_concentrations: list[float],
    reactant_stoichiometry: list[list[float]],
    product_stoichiometry: list[list[float]],
    rate_constants: list[float],
    time_end: float = 1.0,
    points: int = 51,
) -> dict:
    if not module_available("scipy"):
        return unavailable_result(
            "SciPy",
            reason="scipy is not installed",
            manual_action="Install the reaction MCP profile environment (.tool_envs/reaction).",
        )
    import numpy as np
    from scipy.integrate import solve_ivp

    count = len(species)
    reactions = len(rate_constants)
    if count == 0 or len(initial_concentrations) != count:
        raise ValueError("species and initial_concentrations must have equal nonzero length")
    if len(reactant_stoichiometry) != reactions or len(product_stoichiometry) != reactions:
        raise ValueError("one reactant/product stoichiometry row is required per rate constant")
    if any(len(row) != count for row in [*reactant_stoichiometry, *product_stoichiometry]):
        raise ValueError("every stoichiometry row must match species length")
    if time_end <= 0 or points < 2 or any(value < 0 for value in initial_concentrations):
        raise ValueError("time_end/points/concentrations are invalid")
    reactants = np.asarray(reactant_stoichiometry, dtype=float)
    products = np.asarray(product_stoichiometry, dtype=float)
    net = products - reactants
    constants = np.asarray(rate_constants, dtype=float)

    def derivative(_time, concentrations):
        clipped = np.maximum(concentrations, 0.0)
        rates = constants * np.prod(np.power(clipped[None, :], reactants), axis=1)
        return net.T @ rates

    times = np.linspace(0.0, time_end, points)
    solution = solve_ivp(
        derivative,
        (0.0, time_end),
        np.asarray(initial_concentrations, dtype=float),
        t_eval=times,
        method="LSODA",
    )
    if not solution.success or any(not math.isfinite(float(value)) for value in solution.y.ravel()):
        raise RuntimeError(f"Kinetics integration failed: {solution.message}")
    return {
        "status": "success",
        "backend": "SciPy solve_ivp/LSODA",
        "species": species,
        "time": solution.t.tolist(),
        "concentrations": {name: solution.y[index].tolist() for index, name in enumerate(species)},
        "final_concentrations": {name: float(solution.y[index, -1]) for index, name in enumerate(species)},
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_reaction_kinetics(
        species: list[str],
        initial_concentrations: list[float],
        reactant_stoichiometry: list[list[float]],
        product_stoichiometry: list[list[float]],
        rate_constants: list[float],
        time_end: float = 1.0,
        points: int = 51,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_reaction_kinetics_core(**arguments))

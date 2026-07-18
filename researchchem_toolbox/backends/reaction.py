"""Reaction-path, equilibrium, and kinetics actions."""

from __future__ import annotations

import math
from typing import Any

import yaml

from .common import (
    command_artifacts,
    module_version,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    run_external,
    structure_dict,
    success,
    unavailable,
    unsupported,
    write_json,
    write_xyz,
)


ACTIONS = {
    "locate_transition_state", "trace_intrinsic_reaction_coordinate",
    "calculate_chemical_equilibrium", "integrate_reaction_network",
    "solve_microkinetic_model",
}


def _pysisyphus(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    directory = output_directory(action_id, "pysisyphus")
    structure_key = "initial_guess" if action_id == "locate_transition_state" else "transition_state"
    xyz = write_xyz(inputs[structure_key], directory / "input.xyz")
    calculator_backend = str(method["calculator_backend"]).lower()
    if calculator_backend not in {"xtb", "pyscf", "orca"}:
        raise ValueError("pysisyphus calculator_backend must be xtb, pyscf, or orca")
    calculator: dict[str, Any] = {
        "type": calculator_backend,
        "method": str(method["method"]),
        "charge": int(method.get("charge", structure_dict(inputs[structure_key]).get("charge", 0))),
        "mult": int(method.get("multiplicity", structure_dict(inputs[structure_key]).get("multiplicity", 1))),
    }
    if method.get("basis"):
        calculator["basis"] = str(method["basis"])
    configuration: dict[str, Any] = {
        "geom": {"type": "cart", "fn": str(xyz)},
        "calc": calculator,
    }
    if action_id == "locate_transition_state":
        configuration["tsopt"] = {
            "type": str(settings.get("optimizer", "rsirfo")),
            "thresh": str(settings.get("convergence", "gau")),
            "max_cycles": int(settings.get("max_cycles", 200)),
        }
    else:
        configuration["irc"] = {
            "type": str(settings.get("integrator", "eulerpc")),
            "step_length": float(settings.get("step_length", 0.1)),
            "max_cycles": int(settings.get("max_cycles", 150)),
            "forward": bool(settings.get("forward", True)),
            "backward": bool(settings.get("backward", True)),
        }
    input_path = directory / "pysis.yaml"
    input_path.write_text(yaml.safe_dump(configuration, sort_keys=False), encoding="utf-8")
    completed = run_external(
        executable="pysis",
        environment_variable="CHEMGRAPH_PYSIS_COMMAND",
        arguments=[str(input_path)],
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="pip install pysisyphus==1.0.0")
    if completed["returncode"] != 0:
        raise RuntimeError(f"pysisyphus failed: {completed['stderr'][-2000:]}")
    xyz_outputs = [path for path in directory.rglob("*.xyz") if path != xyz]
    if action_id == "locate_transition_state":
        candidate = xyz_outputs[-1] if xyz_outputs else None
        result = {
            "structure": structure_dict(relative_workspace_path(candidate)) if candidate else None,
            "converged": bool(candidate),
            "validation_required": "Call calculate_hessian and derive_vibrational_modes explicitly.",
        }
    else:
        result = {
            "path_files": [relative_workspace_path(path) for path in xyz_outputs],
            "forward": bool(settings.get("forward", True)),
            "backward": bool(settings.get("backward", True)),
        }
    artifacts = command_artifacts(directory)
    provenance = {"command": completed["command"], "generated_config": configuration}
    complete = (
        action_id == "locate_transition_state" and result.get("structure") is not None
    ) or (
        action_id == "trace_intrinsic_reaction_coordinate" and bool(result.get("path_files"))
    )
    if not complete:
        return partial_success(
            result,
            artifact_files=artifacts,
            backend_version=module_version("pysisyphus"),
            provenance=provenance,
            warnings=["pysisyphus completed without a parseable primary structure/path result."],
        )
    return success(
        result,
        artifact_files=artifacts,
        backend_version=module_version("pysisyphus"),
        provenance=provenance,
    )


def _cantera_equilibrium(request: dict[str, Any]) -> dict[str, Any]:
    import cantera as ct

    inputs, _method, settings = request_parts(request)
    mechanism = inputs.get("mechanism") or settings.get("mechanism")
    if not isinstance(mechanism, str) or not mechanism:
        raise ValueError("Cantera requires an explicit mechanism name/path")
    gas = ct.Solution(mechanism)
    composition = inputs["composition"]
    gas.TPX = (
        float(settings["temperature_kelvin"]),
        float(settings["pressure_pa"]),
        composition,
    )
    gas.equilibrate(str(settings["equilibrium_mode"]))
    species = sorted(
        (
            {"name": gas.species_names[index], "mole_fraction": float(value)}
            for index, value in enumerate(gas.X)
            if value > float(settings.get("report_threshold", 1e-12))
        ),
        key=lambda item: item["mole_fraction"],
        reverse=True,
    )
    return success(
        {
            "mechanism": mechanism,
            "equilibrium_mode": str(settings["equilibrium_mode"]),
            "temperature_kelvin": float(gas.T),
            "pressure_pa": float(gas.P),
            "enthalpy_mole_j_mol": float(gas.enthalpy_mole),
            "gibbs_mole_j_mol": float(gas.gibbs_mole),
            "species": species,
        },
        backend_version=getattr(ct, "__version__", None),
    )


def _network_parts(request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    inputs, method, settings = request_parts(request)
    network = inputs["network"]
    initial = inputs["initial_state"]
    if not isinstance(network, dict) or not isinstance(initial, dict):
        raise ValueError("network and initial_state must be mappings")
    return network, initial, settings


def _scipy_network(request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    from scipy.integrate import solve_ivp

    network, initial, settings = _network_parts(request)
    species = [str(value) for value in network["species"]]
    reactions = list(network["reactions"])
    if not species or not reactions:
        raise ValueError("ReactionNetwork requires non-empty species and reactions")
    initial_vector = np.asarray([float(initial.get(name, 0.0)) for name in species], dtype=float)
    if np.any(initial_vector < 0):
        raise ValueError("Initial concentrations cannot be negative")
    reactants = np.zeros((len(reactions), len(species)), dtype=float)
    products = np.zeros_like(reactants)
    constants = np.zeros(len(reactions), dtype=float)
    index = {name: position for position, name in enumerate(species)}
    for reaction_index, reaction in enumerate(reactions):
        for name, coefficient in dict(reaction["reactants"]).items():
            reactants[reaction_index, index[name]] = float(coefficient)
        for name, coefficient in dict(reaction["products"]).items():
            products[reaction_index, index[name]] = float(coefficient)
        constants[reaction_index] = float(reaction["forward_rate_constant"])
    net = products - reactants

    def derivative(_time, concentrations):
        clipped = np.maximum(concentrations, 0.0)
        rates = constants * np.prod(np.power(clipped[None, :], reactants), axis=1)
        return net.T @ rates

    end = float(settings["time_end_seconds"])
    points = int(settings["num_points"])
    times = np.linspace(0.0, end, points)
    solution = solve_ivp(
        derivative,
        (0.0, end),
        initial_vector,
        t_eval=times,
        method=str(settings.get("integrator", "LSODA")),
        rtol=float(settings.get("relative_tolerance", 1e-8)),
        atol=float(settings.get("absolute_tolerance", 1e-12)),
    )
    if not solution.success or not np.all(np.isfinite(solution.y)):
        raise RuntimeError(f"Kinetics integration failed: {solution.message}")
    return success(
        {
            "species": species,
            "time_seconds": solution.t.tolist(),
            "concentrations": {
                name: solution.y[position].tolist() for position, name in enumerate(species)
            },
            "final_state": {
                name: float(solution.y[position, -1]) for position, name in enumerate(species)
            },
            "integrator": str(settings.get("integrator", "LSODA")),
        },
        backend_version=module_version("scipy"),
    )


def _cantera_network(request: dict[str, Any]) -> dict[str, Any]:
    import cantera as ct
    import numpy as np

    network, initial, settings = _network_parts(request)
    mechanism = network.get("mechanism")
    composition = initial.get("composition")
    if not mechanism or not composition:
        return unsupported(
            "Cantera network integration requires network.mechanism and initial_state.composition"
        )
    gas = ct.Solution(str(mechanism))
    gas.TPX = (
        float(initial["temperature_kelvin"]),
        float(initial["pressure_pa"]),
        composition,
    )
    reactor = ct.IdealGasConstPressureReactor(gas)
    simulation = ct.ReactorNet([reactor])
    times = np.linspace(0.0, float(settings["time_end_seconds"]), int(settings["num_points"]))
    temperatures = []
    compositions = []
    for time_value in times:
        simulation.advance(float(time_value))
        temperatures.append(float(reactor.T))
        compositions.append(reactor.thermo.X.tolist())
    return success(
        {
            "time_seconds": times.tolist(),
            "temperature_kelvin": temperatures,
            "species": list(gas.species_names),
            "mole_fractions": compositions,
        },
        backend_version=getattr(ct, "__version__", None),
    )


def _catmap(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    model_value = inputs["model"]
    if not isinstance(model_value, dict):
        raise ValueError("CatMAP model must be a typed mapping")
    allowed = {
        "rxn_expressions", "species_definitions", "descriptor_names", "descriptor_ranges",
        "resolution", "surface_names", "data_file", "gas_thermo_mode", "adsorbate_thermo_mode",
        "scaler", "solver", "mapper", "output_variables",
    }
    unknown = sorted(set(model_value) - allowed)
    if unknown:
        raise ValueError(f"Unsupported CatMAP model fields: {unknown}")
    from catmap import ReactionModel

    model = ReactionModel()
    for name, value in model_value.items():
        setattr(model, name, value)
    model.temperature = float(settings["temperature_kelvin"])
    model.pressure = float(settings["pressure_bar"])
    model.run()
    result = {
        "temperature_kelvin": model.temperature,
        "pressure_bar": model.pressure,
        "output_variables": list(getattr(model, "output_variables", [])),
    }
    for name in result["output_variables"]:
        value = getattr(model, name, None)
        if value is not None:
            try:
                result[name] = value.tolist()
            except AttributeError:
                result[name] = value
    directory = output_directory("solve_microkinetic_model", "catmap")
    path = write_json(directory, "catmap_result.json", result)
    return success(
        result,
        artifact_files=[
            {"path": relative_workspace_path(path), "semantic_type": "MicrokineticResult", "media_type": "application/json"}
        ],
        backend_version=module_version("catmap"),
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "pysisyphus":
        return _pysisyphus(action_id, request)
    if action_id == "calculate_chemical_equilibrium" and backend_id == "cantera":
        return _cantera_equilibrium(request)
    if action_id == "integrate_reaction_network":
        return _scipy_network(request) if backend_id == "scipy" else _cantera_network(request)
    if action_id == "solve_microkinetic_model" and backend_id == "catmap":
        return _catmap(request)
    return unsupported(f"Unsupported reaction action/backend combination: {action_id}/{backend_id}")

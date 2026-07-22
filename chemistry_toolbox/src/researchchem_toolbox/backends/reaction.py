"""Reaction-path, equilibrium, and kinetics actions."""

from __future__ import annotations

import math
import pprint
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import yaml

from .composite import execute_sella
from .goodvibes import execute as execute_goodvibes
from .common import (
    command_artifacts,
    module_version,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
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
    "calculate_rate_constants", "calculate_tunneling_correction",
    "solve_microkinetic_model", "solve_master_equation",
    "analyze_thermochemical_selectivity", "analyze_reaction_free_energy_profile",
}


def _pysisyphus_xtb_gfn(method_name: str) -> int | str:
    """Map conventional xTB method spellings to pysisyphus' native GFN value."""

    normalized = re.sub(r"[^a-z0-9]+", "", method_name.casefold())
    values: dict[str, int | str] = {
        "gfn0": 0,
        "gfn0xtb": 0,
        "xtbgfn0": 0,
        "gfn1": 1,
        "gfn1xtb": 1,
        "xtbgfn1": 1,
        "gfn2": 2,
        "gfn2xtb": 2,
        "xtbgfn2": 2,
        "gfnff": "ff",
        "gfnffxtb": "ff",
        "xtbgfnff": "ff",
        "0": 0,
        "1": 1,
        "2": 2,
        "ff": "ff",
    }
    if normalized not in values:
        raise ValueError(
            "pysisyphus/XTB method must identify GFN0-xTB, GFN1-xTB, GFN2-xTB, "
            "or GFN-FF (compact forms gfn0, gfn1, gfn2, and gfnff are also accepted)"
        )
    return values[normalized]


def _pysisyphus_failure_detail(directory: Path, stderr: str) -> str:
    """Summarize native calculator failures without hiding scientific nonconvergence."""

    scc_markers = sorted(directory.rglob(".sccnotconverged"))
    if scc_markers:
        marker = scc_markers[0].relative_to(directory)
        return (
            "the Agent-selected xTB calculator did not converge its SCC for the supplied "
            f"geometry (native marker: {marker}). This is a numerical calculation failure, "
            "not an automatic backend-selection event; inspect the saved geometry/logs and "
            "explicitly decide the next scientific step."
        )
    crashed_outputs = sorted(directory.glob("crashed_calculator_*/xtb.out"))
    if crashed_outputs:
        diagnostic_phrases = (
            "error",
            "failed",
            "abnormal",
            "converg",
            "atoms in the start geometry",
            "very close",
            "too close",
            "short distance",
            "refuses",
        )
        lines = [
            line.strip()
            for line in crashed_outputs[-1].read_text(
                encoding="utf-8", errors="replace"
            ).splitlines()[-80:]
            if line.strip()
            and any(token in line.casefold() for token in diagnostic_phrases)
        ]
        if lines:
            return "xTB calculator failure: " + " | ".join(dict.fromkeys(lines))[-1600:]
    return stderr[-2000:] or "native pysisyphus process exited without a diagnostic message"


def _pysisyphus(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    directory = output_directory(action_id, "pysisyphus")
    structure_key = "initial_guess" if action_id == "locate_transition_state" else "transition_state"
    xyz = write_xyz(inputs[structure_key], directory / "input.xyz")
    calculator_backend = str(method["calculator_backend"]).lower()
    if calculator_backend not in {"xtb", "pyscf", "orca"}:
        raise ValueError("pysisyphus calculator_backend must be xtb, pyscf, or orca")
    method_name = str(method["method"]).strip()
    input_structure = structure_dict(inputs[structure_key])
    charge = int(method.get("charge", input_structure.get("charge", 0)))
    multiplicity = int(
        method.get("multiplicity", input_structure.get("multiplicity", 1))
    )
    calculator: dict[str, Any] = {
        "type": calculator_backend,
        "charge": charge,
        "mult": multiplicity,
    }
    if calculator_backend == "xtb":
        calculator["gfn"] = _pysisyphus_xtb_gfn(method_name)
    elif calculator_backend == "pyscf":
        if not method.get("basis"):
            raise ValueError("pysisyphus/PySCF requires method_spec.basis")
        normalized = method_name.lower().replace("-", "").replace("_", "")
        if normalized in {"scf", "hf", "rhf", "uhf"}:
            calculator["method"] = "scf"
        elif normalized in {"mp2", "ump2"}:
            calculator["method"] = "mp2"
        else:
            calculator["method"] = "dft"
            calculator["xc"] = str(method.get("functional") or method_name)
        calculator["basis"] = str(method["basis"])
        if normalized in {"uhf", "uks", "ump2"}:
            calculator["unrestricted"] = True
    else:
        keywords = [method_name]
        if method.get("basis"):
            keywords.append(str(method["basis"]))
        calculator["keywords"] = " ".join(keywords)
    configuration: dict[str, Any] = {
        "geom": {"type": "cart", "fn": str(xyz)},
        "calc": calculator,
    }
    if action_id == "locate_transition_state":
        configuration["tsopt"] = {
            "type": str(settings.get("optimizer", "rsirfo")),
            "thresh": str(settings.get("convergence", "gau")),
            "max_cycles": int(settings.get("max_cycles", 200)),
            "hessian_init": str(settings["hessian_init"]),
        }
    else:
        configuration["irc"] = {
            "type": str(settings.get("integrator", "eulerpc")),
            "step_length": float(settings.get("step_length", 0.1)),
            "max_cycles": int(settings.get("max_cycles", 150)),
            "forward": bool(settings.get("forward", True)),
            "backward": bool(settings.get("backward", True)),
            "hessian_init": str(settings["hessian_init"]),
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
        raise RuntimeError(
            f"pysisyphus failed: {_pysisyphus_failure_detail(directory, completed['stderr'])}"
        )
    xyz_outputs = [path for path in directory.rglob("*.xyz") if path != xyz]
    if action_id == "locate_transition_state":
        candidate = xyz_outputs[-1] if xyz_outputs else None
        result_structure = (
            structure_dict(relative_workspace_path(candidate)) if candidate else None
        )
        if result_structure is not None:
            # Native XYZ writers rarely retain molecular electronic-state metadata.
            # These values are the exact Agent-selected state used by the calculator.
            result_structure["charge"] = charge
            result_structure["multiplicity"] = multiplicity
        result = {
            "structure": result_structure,
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
        "resolution", "surface_names", "input_file", "gas_thermo_mode",
        "adsorbate_thermo_mode", "scaler", "solver", "mapper", "output_variables",
        "scaling_constraint_dict", "numerical_representation",
        "adsorbate_interaction_model", "decimal_precision", "tolerance",
        "max_rootfinding_iterations", "max_bisections", "max_damping_iterations",
        "use_numbers_solver", "prefactor_list", "descriptor_values",
    }
    unknown = sorted(set(model_value) - allowed)
    if unknown:
        raise ValueError(f"Unsupported CatMAP model fields: {unknown}")
    from catmap import ReactionModel

    directory = output_directory("solve_microkinetic_model", "catmap")
    configuration = dict(model_value)
    if "input_file" in configuration:
        configuration["input_file"] = str(resolve_input_file(configuration["input_file"]))
    configuration["temperature"] = float(settings["temperature_kelvin"])
    configuration["pressure"] = float(settings["pressure_bar"])
    # CatMAP's setup-file loader initializes the parser/scaler/solver/mapper
    # defaults.  Constructing ReactionModel() and setting attributes directly
    # leaves those objects uninitialized in CatMAP 0.3.x.  The generated file is
    # restricted to allow-listed literal assignments; arbitrary user code is
    # never accepted or executed.
    configuration["data_file"] = str(directory / "catmap_data.pkl")
    setup_path = directory / "model.mkm"
    setup_path.write_text(
        "\n".join(
            f"{name} = {pprint.pformat(value, sort_dicts=True, width=100)}"
            for name, value in configuration.items()
        )
        + "\n",
        encoding="utf-8",
    )
    model = ReactionModel(setup_file=str(setup_path))
    model.run()

    def json_value(value: Any) -> Any:
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {str(key): json_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [json_value(item) for item in value]
        if hasattr(value, "tolist"):
            return json_value(value.tolist())
        try:
            return float(value)
        except (TypeError, ValueError, OverflowError):
            return str(value)

    result = {
        "temperature_kelvin": model.temperature,
        "pressure_bar": model.pressure,
        "output_variables": list(getattr(model, "output_variables", [])),
        "output_labels": json_value(getattr(model, "output_labels", {})),
    }
    for name in result["output_variables"]:
        value = getattr(model, f"{name}_map", None)
        if value is None:
            value = getattr(model, name, None)
        if value is not None:
            result[name] = json_value(value)
    path = write_json(directory, "catmap_result.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "MicrokineticResult",
                "media_type": "application/json",
            },
            *[
                artifact
                for artifact in command_artifacts(directory)
                if artifact["path"] != relative_workspace_path(path)
            ],
        ],
        backend_version=module_version("catmap"),
        provenance={
            "generated_setup": relative_workspace_path(setup_path),
            "accepted_model_fields": sorted(model_value),
        },
    )


def _rmg_temperatures(value: Any) -> list[float]:
    if not isinstance(value, (list, tuple)) or not value:
        raise ValueError("temperatures_kelvin must be a non-empty list")
    temperatures = [float(item) for item in value]
    if any(not math.isfinite(item) or item <= 0 for item in temperatures):
        raise ValueError("temperatures_kelvin must contain positive finite values")
    return temperatures


def _rmg_arrhenius(specification: dict[str, Any]):
    from rmgpy.kinetics import Arrhenius

    required = {
        "pre_exponential_factor", "pre_exponential_unit", "temperature_exponent",
        "activation_energy_kj_mol", "reference_temperature_kelvin",
    }
    missing = sorted(required - set(specification))
    if missing:
        raise ValueError(f"Arrhenius term is missing fields: {missing}")
    keywords: dict[str, Any] = {
        "A": (
            float(specification["pre_exponential_factor"]),
            str(specification["pre_exponential_unit"]),
        ),
        "n": float(specification["temperature_exponent"]),
        "Ea": (float(specification["activation_energy_kj_mol"]), "kJ/mol"),
        "T0": (float(specification["reference_temperature_kelvin"]), "K"),
    }
    if specification.get("minimum_temperature_kelvin") is not None:
        keywords["Tmin"] = (float(specification["minimum_temperature_kelvin"]), "K")
    if specification.get("maximum_temperature_kelvin") is not None:
        keywords["Tmax"] = (float(specification["maximum_temperature_kelvin"]), "K")
    return Arrhenius(**keywords)


def _rmg_rate_constants(request: dict[str, Any]) -> dict[str, Any]:
    import rmgpy
    from rmgpy.kinetics import Chebyshev, MultiArrhenius, PDepArrhenius

    inputs, _method, settings = request_parts(request)
    model_spec = inputs["kinetics_model"]
    if not isinstance(model_spec, dict):
        raise ValueError("kinetics_model must be a typed object")
    model_type = str(model_spec.get("type") or "").strip().lower()
    temperatures = _rmg_temperatures(inputs["temperatures_kelvin"])
    if not isinstance(settings["allow_extrapolation"], bool):
        raise ValueError("allow_extrapolation must be an explicit boolean")
    allow_extrapolation = settings["allow_extrapolation"]
    reaction_order = int(model_spec.get("reaction_order", 0))
    rate_units = {
        1: "s^-1",
        2: "m^3/(mol*s)",
        3: "m^6/(mol^2*s)",
        4: "m^9/(mol^3*s)",
    }
    if reaction_order not in rate_units:
        raise ValueError("kinetics_model.reaction_order must be 1, 2, 3, or 4")

    minimum_temperature = model_spec.get("minimum_temperature_kelvin")
    maximum_temperature = model_spec.get("maximum_temperature_kelvin")
    if not allow_extrapolation:
        if minimum_temperature is not None and min(temperatures) < float(minimum_temperature):
            raise ValueError("Requested temperature is below the kinetics model validity range")
        if maximum_temperature is not None and max(temperatures) > float(maximum_temperature):
            raise ValueError("Requested temperature is above the kinetics model validity range")

    pressure_dependent = False
    if model_type == "arrhenius":
        model = _rmg_arrhenius(model_spec)
    elif model_type == "multi_arrhenius":
        terms = model_spec.get("terms")
        if not isinstance(terms, list) or not terms:
            raise ValueError("multi_arrhenius requires a non-empty terms list")
        model = MultiArrhenius(
            arrhenius=[_rmg_arrhenius(dict(term)) for term in terms],
            Tmin=(float(minimum_temperature), "K") if minimum_temperature is not None else None,
            Tmax=(float(maximum_temperature), "K") if maximum_temperature is not None else None,
        )
    elif model_type == "pressure_dependent_arrhenius":
        pressure_dependent = True
        tabulated_pressures = model_spec.get("pressures_bar")
        terms = model_spec.get("terms")
        if (
            not isinstance(tabulated_pressures, list)
            or not isinstance(terms, list)
            or not tabulated_pressures
            or len(tabulated_pressures) != len(terms)
        ):
            raise ValueError(
                "pressure_dependent_arrhenius requires aligned non-empty pressures_bar and terms"
            )
        tabulated_pressures = [float(value) for value in tabulated_pressures]
        if any(value <= 0 for value in tabulated_pressures):
            raise ValueError("pressures_bar must be positive")
        model = PDepArrhenius(
            pressures=(tabulated_pressures, "bar"),
            arrhenius=[_rmg_arrhenius(dict(term)) for term in terms],
            Tmin=(float(minimum_temperature), "K") if minimum_temperature is not None else None,
            Tmax=(float(maximum_temperature), "K") if maximum_temperature is not None else None,
            Pmin=(min(tabulated_pressures), "bar"),
            Pmax=(max(tabulated_pressures), "bar"),
        )
    elif model_type == "chebyshev":
        pressure_dependent = True
        coefficients = model_spec.get("coefficients")
        if not isinstance(coefficients, list) or not coefficients or not all(
            isinstance(row, list) and row for row in coefficients
        ):
            raise ValueError("chebyshev requires a non-empty rectangular coefficients matrix")
        width = len(coefficients[0])
        if any(len(row) != width for row in coefficients):
            raise ValueError("Chebyshev coefficients must form a rectangular matrix")
        required = {
            "rate_coefficient_unit", "minimum_temperature_kelvin",
            "maximum_temperature_kelvin", "minimum_pressure_bar", "maximum_pressure_bar",
        }
        missing = sorted(required - set(model_spec))
        if missing:
            raise ValueError(f"Chebyshev model is missing fields: {missing}")
        model = Chebyshev(
            coeffs=coefficients,
            kunits=str(model_spec["rate_coefficient_unit"]),
            Tmin=(float(model_spec["minimum_temperature_kelvin"]), "K"),
            Tmax=(float(model_spec["maximum_temperature_kelvin"]), "K"),
            Pmin=(float(model_spec["minimum_pressure_bar"]), "bar"),
            Pmax=(float(model_spec["maximum_pressure_bar"]), "bar"),
        )
    else:
        raise ValueError(
            "kinetics_model.type must be arrhenius, multi_arrhenius, "
            "pressure_dependent_arrhenius, or chebyshev"
        )

    if pressure_dependent:
        raw_pressures = inputs.get("pressures_pa")
        if not isinstance(raw_pressures, (list, tuple)) or not raw_pressures:
            raise ValueError("Pressure-dependent kinetics require a non-empty pressures_pa list")
        pressures = [float(value) for value in raw_pressures]
        if any(not math.isfinite(value) or value <= 0 for value in pressures):
            raise ValueError("pressures_pa must contain positive finite values")
        if not allow_extrapolation:
            minimum_pressure = float(model_spec.get("minimum_pressure_bar", min(model_spec.get("pressures_bar", [0.0])))) * 1e5
            maximum_pressure = float(model_spec.get("maximum_pressure_bar", max(model_spec.get("pressures_bar", [0.0])))) * 1e5
            if min(pressures) < minimum_pressure or max(pressures) > maximum_pressure:
                raise ValueError("Requested pressure is outside the kinetics model validity range")
        values = [
            [float(model.get_rate_coefficient(temperature, pressure)) for pressure in pressures]
            for temperature in temperatures
        ]
    else:
        pressures = None
        values = [float(model.get_rate_coefficient(temperature)) for temperature in temperatures]

    result = {
        "model_type": model_type,
        "reaction_order": reaction_order,
        "temperatures_kelvin": temperatures,
        "pressures_pa": pressures,
        "rate_coefficients": values,
        "rate_coefficient_unit": rate_units[reaction_order],
        "allow_extrapolation": allow_extrapolation,
    }
    directory = output_directory("calculate_rate_constants", "rmg")
    path = write_json(directory, "rate_constants.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "RateConstantResult",
                "media_type": "application/json",
            }
        ],
        backend_version=getattr(rmgpy, "__version__", None),
    )


def _rmg_tunneling(request: dict[str, Any]) -> dict[str, Any]:
    import rmgpy
    from rmgpy.kinetics.tunneling import Eckart, Wigner

    inputs, method, _settings = request_parts(request)
    temperatures = _rmg_temperatures(inputs["temperatures_kelvin"])
    frequency = float(inputs["imaginary_frequency_cm1"])
    if not math.isfinite(frequency) or frequency >= 0:
        raise ValueError("imaginary_frequency_cm1 must be a finite negative frequency")
    model_name = str(method["tunneling_model"]).strip().lower()
    if model_name == "wigner":
        model = Wigner(frequency=(frequency, "cm^-1"))
        energies = None
    elif model_name == "eckart":
        required = ("reactant_energy_kj_mol", "transition_state_energy_kj_mol")
        missing = [name for name in required if name not in inputs]
        if missing:
            raise ValueError(f"Eckart tunneling requires inputs: {missing}")
        reactant = float(inputs["reactant_energy_kj_mol"])
        transition = float(inputs["transition_state_energy_kj_mol"])
        product = inputs.get("product_energy_kj_mol")
        if transition <= reactant or (product is not None and transition <= float(product)):
            raise ValueError("Eckart transition-state energy must exceed reactant and product energies")
        model = Eckart(
            frequency=(frequency, "cm^-1"),
            E0_reac=(reactant, "kJ/mol"),
            E0_TS=(transition, "kJ/mol"),
            E0_prod=(float(product), "kJ/mol") if product is not None else None,
        )
        energies = {
            "reactant_energy_kj_mol": reactant,
            "transition_state_energy_kj_mol": transition,
            "product_energy_kj_mol": float(product) if product is not None else None,
        }
    else:
        raise ValueError("tunneling_model must be wigner or eckart")
    factors = [float(model.calculate_tunneling_factor(value)) for value in temperatures]
    result = {
        "tunneling_model": model_name,
        "imaginary_frequency_cm1": frequency,
        "temperatures_kelvin": temperatures,
        "tunneling_factors": factors,
        "energies": energies,
    }
    directory = output_directory("calculate_tunneling_correction", "rmg")
    path = write_json(directory, "tunneling_correction.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "TunnelingCorrectionResult",
                "media_type": "application/json",
            }
        ],
        backend_version=getattr(rmgpy, "__version__", None),
    )


def _safe_stage_relative_path(value: Any, *, field: str) -> Path:
    text = str(value).strip()
    path = Path(text)
    if not text or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{field} must be a normalized relative path inside the staged model")
    return path


def _stage_master_equation_model(
    action_id: str,
    backend_id: str,
    inputs: dict[str, Any],
) -> tuple[Path, Path, list[dict[str, str]]]:
    """Stage only the native model and explicitly supplied companion files.

    ``model_relative_path`` and companion ``relative_path`` values let an Agent
    preserve a backend's relative-file layout without granting arbitrary writes
    outside the isolated action directory.
    """

    directory = output_directory(action_id, backend_id)
    stage_root = directory / "staged_model"
    stage_root.mkdir()
    model_source = resolve_input_file(inputs["model_file"])
    if not model_source.is_file():
        raise ValueError("model_file must resolve to one regular file")
    default_relative = model_source.name
    model_relative = _safe_stage_relative_path(
        inputs.get("model_relative_path", default_relative),
        field="model_relative_path",
    )
    model_target = stage_root / model_relative
    model_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(model_source, model_target)
    staged = [
        {
            "source": relative_workspace_path(model_source),
            "relative_path": model_relative.as_posix(),
        }
    ]

    companions = inputs.get("companion_files", [])
    if not isinstance(companions, list):
        raise ValueError("companion_files must be a list")
    if len(companions) > 128:
        raise ValueError("At most 128 explicit companion files may be staged")
    occupied = {model_relative.as_posix()}
    for index, item in enumerate(companions):
        if isinstance(item, dict) and "source" in item:
            source_value = item["source"]
            source = resolve_input_file(source_value)
            relative = _safe_stage_relative_path(
                item.get("relative_path", source.name),
                field=f"companion_files[{index}].relative_path",
            )
        else:
            source = resolve_input_file(item)
            relative = _safe_stage_relative_path(
                source.name,
                field=f"companion_files[{index}]",
            )
        if not source.is_file():
            raise ValueError(f"companion_files[{index}] must resolve to one regular file")
        relative_text = relative.as_posix()
        if relative_text in occupied:
            raise ValueError(f"Duplicate staged path: {relative_text}")
        occupied.add(relative_text)
        target = stage_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        staged.append(
            {
                "source": relative_workspace_path(source),
                "relative_path": relative_text,
            }
        )
    return directory, model_target, staged


def _float_token(value: str) -> float | None:
    token = value.strip().replace("D", "E").replace("d", "e")
    if token in {"", "***", "-", "nan", "NaN"}:
        return None
    try:
        result = float(token)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def _bounded_warning_lines(*texts: str, limit: int = 40) -> list[str]:
    warnings: list[str] = []
    for text in texts:
        for line in text.splitlines():
            stripped = line.strip()
            lowered = stripped.lower()
            if stripped and (
                "warning" in lowered
                or "needs to be checked" in lowered
                or lowered.startswith("error")
            ):
                if stripped not in warnings:
                    warnings.append(stripped[:1000])
                if len(warnings) >= limit:
                    return warnings
    return warnings


def _mess_species_names(lines: list[str], heading: str) -> set[str]:
    names: set[str] = set()
    for index, line in enumerate(lines):
        if not line.strip().startswith(heading):
            continue
        cursor = index + 1
        while cursor < len(lines) and "Name" not in lines[cursor]:
            cursor += 1
        cursor += 1
        while cursor < len(lines) and lines[cursor].strip():
            token = lines[cursor].split()[0] if lines[cursor].split() else ""
            if token:
                names.add(token)
            cursor += 1
        break
    return names


def _parse_mess_rates(text: str, maximum_records: int) -> dict[str, Any]:
    lines = text.splitlines()
    wells = _mess_species_names(lines, "Wells (")
    bimolecular = _mess_species_names(lines, "Bimolecular Products (")
    start = next(
        (index for index, line in enumerate(lines) if line.strip() == "Species-Species Rate Tables:"),
        None,
    )
    if start is None:
        return {
            "rate_records": [],
            "total_rate_record_count": 0,
            "truncated": False,
            "wells": sorted(wells),
            "bimolecular_species": sorted(bimolecular),
        }
    stop = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].strip().startswith(
                "High Pressure Rate Coefficients (Temperature-Species Rate Tables)"
            )
        ),
        len(lines),
    )
    temperature: float | None = None
    pressure: float | None = None
    pressure_unit: str | None = None
    records: list[dict[str, Any]] = []
    total = 0
    cursor = start + 1
    condition_pattern = re.compile(
        r"^Temperature\s*=\s*([-+0-9.eEdD]+)\s*K"
        r"(?:\s+Pressure\s*=\s*([-+0-9.eEdD]+)\s*(\S+))?$"
    )
    while cursor < stop:
        stripped = lines[cursor].strip()
        condition = condition_pattern.match(stripped)
        if condition:
            temperature = _float_token(condition.group(1))
            pressure = _float_token(condition.group(2) or "")
            pressure_unit = condition.group(3) if condition.group(2) else None
            cursor += 1
            continue
        if stripped.startswith("From\\To") and temperature is not None:
            destinations = stripped.split()[1:]
            cursor += 1
            while cursor < stop and lines[cursor].strip():
                tokens = lines[cursor].split()
                if len(tokens) < 2:
                    break
                source = tokens[0]
                for destination, token in zip(destinations, tokens[1:]):
                    value = _float_token(token)
                    if value is None or source == destination:
                        continue
                    total += 1
                    if len(records) >= maximum_records:
                        continue
                    if source in wells:
                        unit = "s^-1"
                    elif source in bimolecular:
                        unit = "cm^3/s"
                    else:
                        unit = "backend_native"
                    records.append(
                        {
                            "from_species": source,
                            "to_species": destination,
                            "temperature_kelvin": temperature,
                            "pressure_value": pressure,
                            "pressure_unit": pressure_unit,
                            "pressure_limit": "finite" if pressure is not None else "high",
                            "rate_coefficient": value,
                            "rate_coefficient_unit": unit,
                        }
                    )
                cursor += 1
            continue
        cursor += 1
    return {
        "rate_records": records,
        "total_rate_record_count": total,
        "truncated": total > len(records),
        "wells": sorted(wells),
        "bimolecular_species": sorted(bimolecular),
    }


def _mess_master_equation(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    maximum_records = int(settings.get("maximum_rate_records", 10000))
    if not 1 <= maximum_records <= 100000:
        raise ValueError("maximum_rate_records must be between 1 and 100000")
    directory, model, staged = _stage_master_equation_model(
        "solve_master_equation", "mess", inputs
    )
    if model.suffix.lower() not in {".inp", ".in", ".mess"}:
        raise ValueError("MESS model_file must use .inp, .in, or .mess")
    completed = run_external(
        executable="mess",
        environment_variable="CHEMGRAPH_MESS_COMMAND",
        arguments=[model.name],
        directory=model.parent,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Configure MESS 2020.1.24")
    if completed["returncode"] != 0:
        raise RuntimeError(f"MESS failed: {completed['stderr'][-2000:]}")
    output = model.with_suffix(".out")
    log = model.with_suffix(".log")
    output_text = output.read_text(encoding="utf-8", errors="replace") if output.is_file() else ""
    log_text = log.read_text(encoding="utf-8", errors="replace") if log.is_file() else ""
    parsed = _parse_mess_rates(output_text, maximum_records)
    result = {
        "model_format": "mess_native",
        "model_file": relative_workspace_path(model),
        "staged_files": staged,
        **parsed,
        "completed": "rate calculation done" in log_text.lower(),
    }
    summary = write_json(directory, "master_equation_result.json", result)
    summary_path = relative_workspace_path(summary)
    artifacts = [
        item for item in command_artifacts(directory) if item["path"] != summary_path
    ]
    artifacts.append(
        {
            "path": summary_path,
            "semantic_type": "MasterEquationResult",
            "media_type": "application/json",
        }
    )
    warnings = _bounded_warning_lines(output_text, log_text, completed["stdout"], completed["stderr"])
    provenance = {
        "command": completed["command"],
        "native_model_preserved": True,
        "automatic_model_construction": False,
    }
    if not result["completed"] or not parsed["rate_records"]:
        return partial_success(
            result,
            artifact_files=artifacts,
            backend_version="2020.1.24",
            provenance=provenance,
            warnings=[*warnings, "MESS completed without a fully parseable rate table."],
        )
    return success(
        result,
        artifact_files=artifacts,
        backend_version="2020.1.24",
        provenance=provenance,
        warnings=warnings,
    )


def _xml_local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse_mesmer_rates(path: Path, maximum_records: int) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    conditions: list[dict[str, Any]] = []
    for element in root.iter():
        if _xml_local_name(element.tag) != "PTpair":
            continue
        conditions.append(
            {
                "temperature_kelvin": _float_token(element.attrib.get("T", "")),
                "pressure_value": _float_token(element.attrib.get("P", "")),
                "pressure_unit": element.attrib.get("units"),
            }
        )
    used_conditions: set[int] = set()
    records: list[dict[str, Any]] = []
    total = 0
    rate_lists = [
        element for element in root.iter() if _xml_local_name(element.tag) == "rateList"
    ]
    for rate_index, rate_list in enumerate(rate_lists):
        temperature = _float_token(rate_list.attrib.get("T", ""))
        condition_index = next(
            (
                index
                for index, condition in enumerate(conditions)
                if index not in used_conditions
                and condition["temperature_kelvin"] == temperature
            ),
            None,
        )
        if condition_index is None and rate_index < len(conditions):
            condition_index = rate_index
        condition = conditions[condition_index] if condition_index is not None else {}
        if condition_index is not None:
            used_conditions.add(condition_index)
        for element in rate_list.iter():
            rate_type = _xml_local_name(element.tag)
            if rate_type not in {"firstOrderRate", "secondOrderRate"}:
                continue
            value = _float_token(element.text or "")
            if value is None:
                continue
            total += 1
            if len(records) >= maximum_records:
                continue
            records.append(
                {
                    "from_species": element.attrib.get("fromRef"),
                    "to_species": element.attrib.get("toRef"),
                    "reaction_type": element.attrib.get("reactionType"),
                    "rate_type": rate_type,
                    "temperature_kelvin": temperature,
                    "pressure_value": condition.get("pressure_value"),
                    "pressure_unit": condition.get("pressure_unit"),
                    "bath_gas": rate_list.attrib.get("bathGas"),
                    "excess_reactant_concentration": _float_token(
                        rate_list.attrib.get("conc", "")
                    ),
                    "rate_coefficient": value,
                    "rate_coefficient_unit": (
                        "s^-1"
                        if rate_type == "firstOrderRate"
                        else "cm^3 molecule^-1 s^-1"
                    ),
                }
            )
    return {
        "conditions": conditions,
        "rate_records": records,
        "total_rate_record_count": total,
        "truncated": total > len(records),
    }


def _mesmer_master_equation(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    maximum_records = int(settings.get("maximum_rate_records", 10000))
    if not 1 <= maximum_records <= 100000:
        raise ValueError("maximum_rate_records must be between 1 and 100000")
    directory, model, staged = _stage_master_equation_model(
        "solve_master_equation", "mesmer", inputs
    )
    if model.suffix.lower() != ".xml":
        raise ValueError("MESMER model_file must use .xml")
    audit = model.parent / "mesmer.audit.xml"
    completed = run_external(
        executable="mesmer",
        environment_variable="CHEMGRAPH_MESMER_COMMAND",
        arguments=[model.name, f"-o{audit.name}"],
        directory=model.parent,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Configure MESMER 7.1")
    if completed["returncode"] != 0:
        raise RuntimeError(f"MESMER failed: {completed['stderr'][-2000:]}")
    parsed = _parse_mesmer_rates(audit, maximum_records) if audit.is_file() else {
        "conditions": [], "rate_records": [], "total_rate_record_count": 0, "truncated": False
    }
    log = model.parent / "mesmer.log"
    log_text = log.read_text(encoding="utf-8", errors="replace") if log.is_file() else ""
    result = {
        "model_format": "mesmer_xml",
        "model_file": relative_workspace_path(model),
        "staged_files": staged,
        **parsed,
        "completed": audit.is_file() and bool(parsed["rate_records"]),
    }
    summary = write_json(directory, "master_equation_result.json", result)
    summary_path = relative_workspace_path(summary)
    artifacts = [
        item for item in command_artifacts(directory) if item["path"] != summary_path
    ]
    artifacts.append(
        {
            "path": summary_path,
            "semantic_type": "MasterEquationResult",
            "media_type": "application/json",
        }
    )
    warnings = _bounded_warning_lines(
        completed["stdout"], completed["stderr"], log_text,
        audit.read_text(encoding="utf-8", errors="replace") if audit.is_file() else "",
    )
    provenance = {
        "command": completed["command"],
        "native_model_preserved": True,
        "automatic_model_construction": False,
    }
    if not result["completed"]:
        return partial_success(
            result,
            artifact_files=artifacts,
            backend_version="7.1",
            provenance=provenance,
            warnings=[*warnings, "MESMER completed without a parseable phenomenological rate list."],
        )
    return success(
        result,
        artifact_files=artifacts,
        backend_version="7.1",
        provenance=provenance,
        warnings=warnings,
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "goodvibes":
        return execute_goodvibes(action_id, request)
    if backend_id == "sella" and action_id == "locate_transition_state":
        return execute_sella(action_id, request)
    if backend_id == "pysisyphus":
        return _pysisyphus(action_id, request)
    if action_id == "calculate_chemical_equilibrium" and backend_id == "cantera":
        return _cantera_equilibrium(request)
    if action_id == "integrate_reaction_network":
        return _scipy_network(request) if backend_id == "scipy" else _cantera_network(request)
    if action_id == "solve_microkinetic_model" and backend_id == "catmap":
        return _catmap(request)
    if action_id == "calculate_rate_constants" and backend_id == "rmg":
        return _rmg_rate_constants(request)
    if action_id == "calculate_tunneling_correction" and backend_id == "rmg":
        return _rmg_tunneling(request)
    if action_id == "solve_master_equation":
        if backend_id == "mess":
            return _mess_master_equation(request)
        if backend_id == "mesmer":
            return _mesmer_master_equation(request)
    return unsupported(f"Unsupported reaction action/backend combination: {action_id}/{backend_id}")

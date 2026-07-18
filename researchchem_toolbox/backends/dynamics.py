"""Molecular-dynamics propagation and trajectory-analysis actions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import (
    command_artifacts,
    module_version,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    run_external,
    success,
    unavailable,
    unsupported,
    write_json,
)


ACTIONS = {
    "minimize_system_energy", "propagate_dynamics", "calculate_trajectory_rmsd",
    "calculate_radius_of_gyration", "calculate_radial_distribution",
    "calculate_mean_squared_displacement", "evaluate_collective_variables",
}


def _system_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and "result" in value and isinstance(value["result"], dict):
        value = value["result"]
    if not isinstance(value, dict):
        raise ValueError("system must be a ParameterizedSystem mapping or Artifact result")
    return dict(value)


def _openmm(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import openmm
    from openmm import XmlSerializer, unit
    from openmm.app import DCDReporter, PDBFile, StateDataReporter, Simulation

    inputs, method, settings = request_parts(request)
    system_value = _system_mapping(inputs["system"])
    topology_path = resolve_input_file(system_value["topology_path"])
    system_path = resolve_input_file(system_value["system_xml_path"])
    pdb = PDBFile(str(topology_path))
    system = XmlSerializer.deserialize(system_path.read_text(encoding="utf-8"))
    platform_name = method.get("platform")
    platform = openmm.Platform.getPlatformByName(str(platform_name)) if platform_name else None
    properties = {str(key): str(value) for key, value in dict(method.get("platform_properties") or {}).items()}
    directory = output_directory(action_id, "openmm")
    if action_id == "minimize_system_energy":
        integrator = openmm.VerletIntegrator(1.0 * unit.femtoseconds)
        simulation = Simulation(pdb.topology, system, integrator, platform, properties) if platform else Simulation(pdb.topology, system, integrator)
        simulation.context.setPositions(pdb.positions)
        initial = simulation.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        simulation.minimizeEnergy(
            tolerance=float(settings["force_tolerance_kj_mol_nm"]) * unit.kilojoule_per_mole / unit.nanometer,
            maxIterations=int(settings["max_iterations"]),
        )
        state = simulation.context.getState(getEnergy=True, getPositions=True)
        final = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        final_path = directory / "minimized.pdb"
        with final_path.open("w", encoding="utf-8") as handle:
            PDBFile.writeFile(pdb.topology, state.getPositions(), handle)
        result = {
            **system_value,
            "topology_path": relative_workspace_path(final_path),
            "initial_potential_energy_kj_mol": float(initial),
            "final_potential_energy_kj_mol": float(final),
            "minimized": True,
        }
    else:
        ensemble = str(settings["ensemble"]).upper()
        temperature = float(settings["temperature_kelvin"])
        timestep = float(settings["timestep_fs"])
        friction = float(settings.get("friction_per_ps", 1.0))
        if ensemble == "NVE":
            integrator = openmm.VerletIntegrator(timestep * unit.femtoseconds)
        elif ensemble in {"NVT", "NPT"}:
            integrator = openmm.LangevinMiddleIntegrator(
                temperature * unit.kelvin,
                friction / unit.picosecond,
                timestep * unit.femtoseconds,
            )
            if ensemble == "NPT":
                if "pressure_bar" not in settings:
                    raise ValueError("NPT propagation requires pressure_bar")
                system.addForce(
                    openmm.MonteCarloBarostat(
                        float(settings["pressure_bar"]) * unit.bar,
                        temperature * unit.kelvin,
                    )
                )
        else:
            raise ValueError("ensemble must be NVE, NVT, or NPT")
        simulation = Simulation(pdb.topology, system, integrator, platform, properties) if platform else Simulation(pdb.topology, system, integrator)
        simulation.context.setPositions(pdb.positions)
        if system_value.get("state_xml_path"):
            state_xml = resolve_input_file(system_value["state_xml_path"]).read_text(encoding="utf-8")
            simulation.context.setState(XmlSerializer.deserialize(state_xml))
        elif bool(settings.get("initialize_velocities", True)):
            simulation.context.setVelocitiesToTemperature(temperature * unit.kelvin, int(settings.get("random_seed", 0)))
        trajectory_path = directory / "trajectory.dcd"
        state_data_path = directory / "state.csv"
        interval = int(settings["report_interval"])
        steps = int(settings["steps"])
        if interval < 1 or interval > steps:
            raise ValueError("report_interval must be between 1 and steps")
        simulation.reporters.append(DCDReporter(str(trajectory_path), interval))
        simulation.reporters.append(
            StateDataReporter(
                str(state_data_path), interval, step=True, time=True, potentialEnergy=True,
                kineticEnergy=True, temperature=True, volume=True, density=True,
                separator=",",
            )
        )
        simulation.step(steps)
        final_state = simulation.context.getState(
            getPositions=True, getVelocities=True, getEnergy=True,
            enforcePeriodicBox=True,
        )
        final_pdb = directory / "final.pdb"
        state_xml_path = directory / "state.xml"
        with final_pdb.open("w", encoding="utf-8") as handle:
            PDBFile.writeFile(pdb.topology, final_state.getPositions(), handle)
        state_xml_path.write_text(XmlSerializer.serialize(final_state), encoding="utf-8")
        result = {
            "trajectory_path": relative_workspace_path(trajectory_path),
            "topology_path": relative_workspace_path(final_pdb),
            "state_xml_path": relative_workspace_path(state_xml_path),
            "state_data_path": relative_workspace_path(state_data_path),
            "ensemble": ensemble,
            "temperature_kelvin": temperature,
            "pressure_bar": settings.get("pressure_bar"),
            "timestep_fs": timestep,
            "steps": steps,
            "duration_ps": timestep * steps / 1000.0,
        }
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=getattr(openmm, "__version__", None),
    )


def _gromacs(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    system = _system_mapping(inputs["system"])
    coordinates = resolve_input_file(system.get("coordinate_path") or system.get("topology_path"))
    topology = resolve_input_file(system["gromacs_topology_path"])
    directory = output_directory(action_id, "gromacs")
    mdp_path = directory / "segment.mdp"
    if action_id == "minimize_system_energy":
        mdp = {
            "integrator": "steep",
            "emtol": float(settings["force_tolerance_kj_mol_nm"]),
            "nsteps": int(settings["max_iterations"]),
            "cutoff-scheme": str(method.get("cutoff_scheme", "Verlet")),
        }
    else:
        ensemble = str(settings["ensemble"]).upper()
        if ensemble not in {"NVE", "NVT", "NPT"}:
            raise ValueError("ensemble must be NVE, NVT, or NPT")
        if ensemble == "NPT" and "pressure_bar" not in settings:
            raise ValueError("NPT propagation requires pressure_bar")
        steps = int(settings["steps"])
        interval = int(settings["report_interval"])
        if interval < 1 or interval > steps:
            raise ValueError("report_interval must be between 1 and steps")
        mdp = {
            "integrator": "md",
            "dt": float(settings["timestep_fs"]) / 1000.0,
            "nsteps": steps,
            "nstxout-compressed": interval,
            "tcoupl": "V-rescale" if ensemble in {"NVT", "NPT"} else "no",
            "ref-t": float(settings["temperature_kelvin"]),
            "tau-t": float(settings.get("temperature_coupling_ps", 1.0)),
            "pcoupl": "C-rescale" if ensemble == "NPT" else "no",
            "ref-p": float(settings.get("pressure_bar", 1.0)),
            "tau-p": float(settings.get("pressure_coupling_ps", 5.0)),
            "compressibility": float(settings.get("compressibility_bar_inverse", 4.5e-5)),
            "cutoff-scheme": str(method.get("cutoff_scheme", "Verlet")),
        }
    mdp_path.write_text("\n".join(f"{key} = {value}" for key, value in mdp.items()) + "\n", encoding="utf-8")
    tpr = directory / "segment.tpr"
    grompp = run_external(
        executable="gmx", environment_variable="CHEMGRAPH_GROMACS_COMMAND",
        arguments=["grompp", "-f", str(mdp_path), "-c", str(coordinates), "-p", str(topology), "-o", str(tpr), "-maxwarn", "0"],
        directory=directory,
        timeout_seconds=min(600, int(request.get("resource_limits", {}).get("walltime_seconds", 1800))),
    )
    (directory / "grompp.stdout.log").write_text(grompp["stdout"], encoding="utf-8")
    (directory / "grompp.stderr.log").write_text(grompp["stderr"], encoding="utf-8")
    if not grompp["available"]:
        return unavailable(grompp["stderr"], install="conda install -c conda-forge gromacs")
    if grompp["returncode"] != 0:
        raise RuntimeError(f"gmx grompp failed: {grompp['stderr'][-2000:]}")
    mdrun = run_external(
        executable="gmx", environment_variable="CHEMGRAPH_GROMACS_COMMAND",
        arguments=["mdrun", "-deffnm", "segment"], directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "mdrun.stdout.log").write_text(mdrun["stdout"], encoding="utf-8")
    (directory / "mdrun.stderr.log").write_text(mdrun["stderr"], encoding="utf-8")
    if mdrun["returncode"] != 0:
        raise RuntimeError(f"gmx mdrun failed: {mdrun['stderr'][-2000:]}")
    final_path = directory / "segment.gro"
    trajectory_path = directory / "segment.xtc"
    checkpoint_path = directory / "segment.cpt"
    if action_id == "minimize_system_energy":
        result = {
            **system,
            "coordinate_path": relative_workspace_path(final_path) if final_path.is_file() else None,
            "minimized": final_path.is_file(),
            "settings": settings,
        }
        complete = final_path.is_file()
    else:
        result = {
            "final_structure_path": relative_workspace_path(final_path) if final_path.is_file() else None,
            "trajectory_path": relative_workspace_path(trajectory_path) if trajectory_path.is_file() else None,
            "checkpoint_path": relative_workspace_path(checkpoint_path) if checkpoint_path.is_file() else None,
            "settings": settings,
        }
        complete = final_path.is_file() and trajectory_path.is_file()
    artifacts = command_artifacts(directory)
    provenance = {"grompp": grompp["command"], "mdrun": mdrun["command"]}
    if not complete:
        return partial_success(
            result,
            artifact_files=artifacts,
            provenance=provenance,
            warnings=["GROMACS completed without all files required by the action's primary result."],
        )
    return success(result, artifact_files=artifacts, provenance=provenance)


def _lammps(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    system = _system_mapping(inputs["system"])
    data_path = resolve_input_file(system["lammps_data_path"])
    pair_style = str(system["pair_style"])
    pair_coefficients = list(system["pair_coefficients"])
    if any(";" in str(value) or "&" in str(value) for value in [pair_style, *pair_coefficients]):
        raise ValueError("LAMMPS force-field fields contain forbidden shell-like separators")
    directory = output_directory(action_id, "lammps")
    input_path = directory / "segment.in"
    lines = [
        f"units {method.get('units', 'real')}",
        f"atom_style {method.get('atom_style', 'full')}",
        f"read_data {data_path}",
        f"pair_style {pair_style}",
        *[f"pair_coeff {value}" for value in pair_coefficients],
        f"neighbor {float(method.get('neighbor_skin', 2.0))} bin",
    ]
    if action_id == "minimize_system_energy":
        lines.extend(
            [
                f"minimize {float(settings['energy_tolerance'])} {float(settings['force_tolerance'])} "
                f"{int(settings['max_iterations'])} {int(settings.get('max_evaluations', 10 * int(settings['max_iterations'])))}",
                "write_data minimized.data",
            ]
        )
    else:
        ensemble = str(settings["ensemble"]).upper()
        timestep = float(settings["timestep_fs"])
        steps = int(settings["steps"])
        interval = int(settings["report_interval"])
        if interval < 1 or interval > steps:
            raise ValueError("report_interval must be between 1 and steps")
        lines.extend([f"timestep {timestep}", f"thermo {interval}"])
        if ensemble == "NVE":
            lines.append("fix ensemble all nve")
        elif ensemble == "NVT":
            temperature = float(settings["temperature_kelvin"])
            lines.append(f"fix ensemble all nvt temp {temperature} {temperature} {float(settings.get('temperature_damping_fs', 100.0))}")
        elif ensemble == "NPT":
            temperature = float(settings["temperature_kelvin"])
            pressure = float(settings["pressure_bar"])
            lines.append(
                f"fix ensemble all npt temp {temperature} {temperature} {float(settings.get('temperature_damping_fs', 100.0))} "
                f"iso {pressure} {pressure} {float(settings.get('pressure_damping_fs', 1000.0))}"
            )
        else:
            raise ValueError("ensemble must be NVE, NVT, or NPT")
        lines.extend(
            [
                f"dump trajectory all custom {interval} trajectory.lammpstrj id type x y z",
                f"run {steps}",
                "write_data final.data",
            ]
        )
    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    completed = run_external(
        executable="lmp", environment_variable="CHEMGRAPH_LAMMPS_COMMAND",
        arguments=["-in", str(input_path)], directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge lammps")
    if completed["returncode"] != 0:
        raise RuntimeError(f"LAMMPS failed: {completed['stderr'][-2000:]}")
    final_path = directory / ("minimized.data" if action_id == "minimize_system_energy" else "final.data")
    trajectory_path = directory / "trajectory.lammpstrj"
    if action_id == "minimize_system_energy":
        result = {
            **system,
            "lammps_data_path": relative_workspace_path(final_path) if final_path.is_file() else None,
            "minimized": final_path.is_file(),
            "settings": settings,
        }
        complete = final_path.is_file()
    else:
        result = {
            "final_data_path": relative_workspace_path(final_path) if final_path.is_file() else None,
            "trajectory_path": relative_workspace_path(trajectory_path) if trajectory_path.is_file() else None,
            "settings": settings,
        }
        complete = final_path.is_file() and trajectory_path.is_file()
    artifacts = command_artifacts(directory)
    provenance = {"command": completed["command"]}
    if not complete:
        return partial_success(
            result,
            artifact_files=artifacts,
            provenance=provenance,
            warnings=["LAMMPS completed without all files required by the action's primary result."],
        )
    return success(result, artifact_files=artifacts, provenance=provenance)


def _trajectory_files(inputs: dict[str, Any]) -> tuple[Path, Path]:
    topology = resolve_input_file(inputs["topology"])
    trajectory = resolve_input_file(inputs["trajectory"])
    return topology, trajectory


def _mdanalysis(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import MDAnalysis as mda
    import numpy as np

    inputs, _method, settings = request_parts(request)
    topology, trajectory = _trajectory_files(inputs)
    universe = mda.Universe(str(topology), str(trajectory))
    if action_id == "calculate_trajectory_rmsd":
        from MDAnalysis.analysis import rms

        selection = str(settings["selection"])
        reference_value = inputs.get("reference")
        reference = mda.Universe(str(resolve_input_file(reference_value))) if reference_value else universe
        analysis = rms.RMSD(universe, reference, select=selection).run()
        array = np.asarray(analysis.results.rmsd)
        result = {"frame": array[:, 0].tolist(), "time_ps": array[:, 1].tolist(), "rmsd_angstrom": array[:, 2].tolist(), "selection": selection}
    elif action_id == "calculate_radius_of_gyration":
        atoms = universe.select_atoms(str(settings["selection"]))
        values, times = [], []
        for frame in universe.trajectory:
            values.append(float(atoms.radius_of_gyration()))
            times.append(float(frame.time))
        result = {"time_ps": times, "radius_of_gyration_angstrom": values, "selection": str(settings["selection"])}
    elif action_id == "calculate_radial_distribution":
        from MDAnalysis.analysis.rdf import InterRDF

        first = universe.select_atoms(str(settings["selection_a"]))
        second = universe.select_atoms(str(settings["selection_b"]))
        range_values = settings["range_angstrom"]
        analysis = InterRDF(first, second, nbins=int(settings["bins"]), range=(float(range_values[0]), float(range_values[1]))).run()
        result = {"distance_angstrom": analysis.results.bins.tolist(), "rdf": analysis.results.rdf.tolist(), "selection_a": str(settings["selection_a"]), "selection_b": str(settings["selection_b"])}
    elif action_id == "calculate_mean_squared_displacement":
        from MDAnalysis.analysis.msd import EinsteinMSD

        analysis = EinsteinMSD(
            universe,
            select=str(settings["selection"]),
            msd_type=str(settings["dimensions"]),
            fft=bool(settings.get("fft", True)),
        ).run()
        result = {"lag_index": list(range(len(analysis.results.timeseries))), "msd_angstrom2": np.asarray(analysis.results.timeseries).tolist(), "selection": str(settings["selection"]), "dimensions": str(settings["dimensions"])}
    else:
        return unsupported(f"MDAnalysis does not implement {action_id}")
    return success(result, backend_version=module_version("MDAnalysis"))


def _plumed(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    trajectory = resolve_input_file(inputs["trajectory"])
    topology = resolve_input_file(inputs["topology"])
    definitions = inputs["collective_variables"]
    if not isinstance(definitions, list) or not definitions:
        raise ValueError("collective_variables must be a non-empty list")
    allowed = {"DISTANCE", "ANGLE", "TORSION", "COORDINATION", "RMSD", "GYRATION"}
    lines = []
    labels = []
    for index, definition in enumerate(definitions):
        label = str(definition.get("label") or f"cv{index + 1}")
        kind = str(definition["type"]).upper()
        if kind not in allowed:
            raise ValueError(f"Unsupported PLUMED collective-variable type: {kind}")
        arguments = []
        for key, value in definition.items():
            if key in {"label", "type"}:
                continue
            if not key.replace("_", "").isalnum():
                raise ValueError(f"Invalid PLUMED argument name: {key}")
            if isinstance(value, list):
                value = ",".join(str(item) for item in value)
            arguments.append(f"{key.upper()}={value}")
        lines.append(f"{label}: {kind} {' '.join(arguments)}")
        labels.append(label)
    lines.append(f"PRINT ARG={','.join(labels)} FILE=collective_variables.dat STRIDE={int(settings.get('stride', 1))}")
    directory = output_directory("evaluate_collective_variables", "plumed")
    input_path = directory / "plumed.dat"
    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    suffix = trajectory.suffix.lower()
    flag = {".xtc": "--mf_xtc", ".trr": "--mf_trr", ".dcd": "--mf_dcd", ".xyz": "--ixyz"}.get(suffix)
    if flag is None:
        raise ValueError(f"Unsupported PLUMED trajectory format: {suffix}")
    completed = run_external(
        executable="plumed", environment_variable="CHEMGRAPH_PLUMED_COMMAND",
        arguments=["driver", "--plumed", str(input_path), flag, str(trajectory), "--pdb", str(topology)],
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge plumed")
    if completed["returncode"] != 0:
        raise RuntimeError(f"PLUMED failed: {completed['stderr'][-2000:]}")
    data_path = directory / "collective_variables.dat"
    result = {"data_path": relative_workspace_path(data_path), "collective_variables": labels}
    return success(result, artifact_files=command_artifacts(directory), provenance={"command": completed["command"]})


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "openmm":
        return _openmm(action_id, request)
    if backend_id == "gromacs":
        return _gromacs(action_id, request)
    if backend_id == "lammps":
        return _lammps(action_id, request)
    if backend_id == "mdanalysis":
        return _mdanalysis(action_id, request)
    if backend_id == "plumed":
        return _plumed(request)
    return unsupported(f"Unsupported dynamics action/backend combination: {action_id}/{backend_id}")

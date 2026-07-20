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
from .licensed_md import amber_pmemd as _amber_pmemd
from .licensed_md import charmm as _charmm
from .licensed_md import namd as _namd


ACTIONS = {
    "minimize_system_energy", "propagate_dynamics", "calculate_trajectory_rmsd",
    "calculate_force_field_energy", "calculate_force_field_forces",
    "decompose_force_field_energy",
    "calculate_radius_of_gyration", "calculate_radial_distribution",
    "calculate_mean_squared_displacement", "evaluate_collective_variables",
    "estimate_free_energy_difference", "calculate_potential_of_mean_force",
    "calculate_contacts", "calculate_solvent_accessible_surface",
    "calculate_dihedral_distribution", "calculate_hydrogen_bonds",
    "calculate_principal_components", "calculate_dynamic_cross_correlation",
    "assign_secondary_structure",
    "cluster_trajectory",
    "parse_alchemical_energy_data",
    "estimate_thermodynamic_expectations", "analyze_free_energy_convergence",
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
    if action_id in {
        "calculate_force_field_energy", "calculate_force_field_forces",
        "decompose_force_field_energy",
    }:
        if action_id == "decompose_force_field_energy":
            force_count = system.getNumForces()
            if force_count > 32:
                raise ValueError("OpenMM force-object decomposition supports at most 32 Force objects")
            for index in range(force_count):
                system.getForce(index).setForceGroup(index)
        integrator = openmm.VerletIntegrator(1.0 * unit.femtoseconds)
        simulation = (
            Simulation(pdb.topology, system, integrator, platform, properties)
            if platform else Simulation(pdb.topology, system, integrator)
        )
        simulation.context.setPositions(pdb.positions)
        use_saved_state = bool(settings["use_saved_state"])
        if use_saved_state:
            state_path = system_value.get("state_xml_path")
            if not state_path:
                raise ValueError("use_saved_state=true requires system.state_xml_path")
            saved = XmlSerializer.deserialize(
                resolve_input_file(state_path).read_text(encoding="utf-8")
            )
            simulation.context.setState(saved)
        enforce_periodic = bool(settings["enforce_periodic_box"])
        if action_id == "calculate_force_field_energy":
            state = simulation.context.getState(
                getEnergy=True,
                enforcePeriodicBox=enforce_periodic,
            )
            result = {
                "potential_energy_kj_mol": float(
                    state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
                ),
                "coordinate_source": "saved_state" if use_saved_state else "topology",
                "enforce_periodic_box": enforce_periodic,
                "particle_count": int(system.getNumParticles()),
            }
        elif action_id == "calculate_force_field_forces":
            state = simulation.context.getState(
                getForces=True,
                enforcePeriodicBox=enforce_periodic,
            )
            forces = state.getForces(asNumpy=True).value_in_unit(
                unit.kilojoule_per_mole / unit.nanometer
            )
            result = {
                "forces": forces.tolist(),
                "unit": "kJ/(mol*nm)",
                "coordinate_source": "saved_state" if use_saved_state else "topology",
                "enforce_periodic_box": enforce_periodic,
                "particle_count": int(system.getNumParticles()),
            }
        else:
            total_state = simulation.context.getState(
                getEnergy=True,
                enforcePeriodicBox=enforce_periodic,
            )
            total = float(
                total_state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
            )
            include_zero = bool(settings["include_zero_terms"])
            terms = []
            for index in range(system.getNumForces()):
                force = system.getForce(index)
                state = simulation.context.getState(
                    getEnergy=True,
                    enforcePeriodicBox=enforce_periodic,
                    groups={index},
                )
                energy = float(
                    state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
                )
                if include_zero or energy != 0.0:
                    terms.append(
                        {
                            "force_index": index,
                            "force_group": index,
                            "force_class": force.__class__.__name__,
                            "force_name": str(force.getName()),
                            "potential_energy_kj_mol": energy,
                        }
                    )
            result = {
                "total_potential_energy_kj_mol": total,
                "terms": terms,
                "force_object_count": int(system.getNumForces()),
                "reported_term_count": len(terms),
                "sum_reported_terms_kj_mol": float(
                    sum(term["potential_energy_kj_mol"] for term in terms)
                ),
                "coordinate_source": "saved_state" if use_saved_state else "topology",
                "enforce_periodic_box": enforce_periodic,
                "decomposition_scope": "one term per existing OpenMM Force object",
            }
        return success(result, backend_version=getattr(openmm, "__version__", None))
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


def _hoomd(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import hoomd
    import numpy as np

    inputs, method, settings = request_parts(request)
    system = _system_mapping(inputs["system"])
    if str(method["unit_system"]).lower() != "reduced_lj":
        raise ValueError("The validated HOOMD adapter currently requires unit_system=reduced_lj")
    device_name = str(method["device"]).strip().lower()
    if device_name == "cpu":
        device = hoomd.device.CPU()
    elif device_name == "gpu":
        device = hoomd.device.GPU()
    else:
        raise ValueError("HOOMD device must be cpu or gpu")
    simulation = hoomd.Simulation(device=device, seed=int(settings.get("random_seed", 0)))
    particles = dict(system["particles"])
    positions = np.asarray(particles["positions"], dtype=float)
    type_names = [str(value) for value in particles["type_names"]]
    type_ids = np.asarray(particles["type_ids"], dtype=int)
    masses = np.asarray(particles.get("masses", np.ones(len(positions))), dtype=float)
    if positions.ndim != 2 or positions.shape[1] != 3 or len(positions) == 0:
        raise ValueError("HOOMD particles.positions must be a non-empty Nx3 matrix")
    if len(type_ids) != len(positions) or len(masses) != len(positions):
        raise ValueError("HOOMD particle type_ids and masses must align with positions")
    if not type_names or type_ids.min() < 0 or type_ids.max() >= len(type_names):
        raise ValueError("HOOMD particle type_ids reference an unknown type")
    box = list(system["box"])
    if len(box) not in {3, 6}:
        raise ValueError("HOOMD box must contain [Lx,Ly,Lz] or [Lx,Ly,Lz,xy,xz,yz]")
    if len(box) == 3:
        box.extend([0.0, 0.0, 0.0])
    snapshot = hoomd.Snapshot()
    snapshot.configuration.box = [float(value) for value in box]
    snapshot.particles.N = len(positions)
    snapshot.particles.types = type_names
    snapshot.particles.position[:] = positions
    snapshot.particles.typeid[:] = type_ids
    snapshot.particles.mass[:] = masses
    bonds = system.get("bonds")
    if bonds:
        bond_groups = np.asarray(bonds["groups"], dtype=int)
        bond_type_ids = np.asarray(bonds["type_ids"], dtype=int)
        bond_types = [str(value) for value in bonds["type_names"]]
        if bond_groups.ndim != 2 or bond_groups.shape[1] != 2:
            raise ValueError("HOOMD bonds.groups must be an Nx2 integer matrix")
        if len(bond_type_ids) != len(bond_groups):
            raise ValueError("HOOMD bond type_ids must align with bond groups")
        snapshot.bonds.N = len(bond_groups)
        snapshot.bonds.types = bond_types
        snapshot.bonds.group[:] = bond_groups
        snapshot.bonds.typeid[:] = bond_type_ids
    simulation.create_state_from_snapshot(snapshot)

    if str(method["pair_potential"]).lower() != "lj":
        raise ValueError("The validated HOOMD pair_potential is lj")
    neighbor_list = hoomd.md.nlist.Cell(buffer=float(method["neighbor_buffer"]))
    pair = hoomd.md.pair.LJ(nlist=neighbor_list)
    for raw_pair, parameters in dict(method["pair_parameters"]).items():
        names = raw_pair.split("|") if isinstance(raw_pair, str) else list(raw_pair)
        if len(names) != 2 or any(name not in type_names for name in names):
            raise ValueError(f"Invalid HOOMD pair-parameter key: {raw_pair!r}")
        pair.params[tuple(names)] = {
            "epsilon": float(parameters["epsilon"]),
            "sigma": float(parameters["sigma"]),
        }
        pair.r_cut[tuple(names)] = float(parameters["r_cut"])
    forces = [pair]
    if bonds:
        if str(method.get("bond_potential", "harmonic")).lower() != "harmonic":
            raise ValueError("The validated HOOMD bond_potential is harmonic")
        harmonic = hoomd.md.bond.Harmonic()
        parameters = dict(method.get("bond_parameters") or {})
        for name in bonds["type_names"]:
            if name not in parameters:
                raise ValueError(f"Missing HOOMD harmonic parameters for bond type {name}")
            harmonic.params[str(name)] = {
                "k": float(parameters[name]["k"]),
                "r0": float(parameters[name]["r0"]),
            }
        forces.append(harmonic)

    directory = output_directory(action_id, "hoomd")
    all_filter = hoomd.filter.All()
    if action_id in {"calculate_force_field_energy", "calculate_force_field_forces"}:
        simulation.operations.integrator = hoomd.md.Integrator(
            dt=0.001,
            methods=[hoomd.md.methods.ConstantVolume(filter=all_filter)],
            forces=forces,
        )
        simulation.run(0)
        component_energies = [
            {
                "component_index": index,
                "force_class": force.__class__.__name__,
                "potential_energy": float(force.energy),
            }
            for index, force in enumerate(forces)
        ]
        if action_id == "calculate_force_field_energy":
            result = {
                "potential_energy": float(sum(item["potential_energy"] for item in component_energies)),
                "energy_unit": "reduced_energy",
                "components": component_energies,
                "particle_count": len(positions),
            }
        else:
            component_forces = [np.asarray(force.forces, dtype=float) for force in forces]
            total_forces = np.sum(component_forces, axis=0)
            result = {
                "forces": total_forces.tolist(),
                "unit": "reduced_energy/reduced_length",
                "components": [
                    {
                        **component_energies[index],
                        "forces": values.tolist(),
                    }
                    for index, values in enumerate(component_forces)
                ],
                "particle_count": len(positions),
            }
    elif action_id == "minimize_system_energy":
        fire = hoomd.md.minimize.FIRE(
            dt=float(settings["integration_timestep"]),
            force_tol=float(settings["force_tolerance"]),
            angmom_tol=float(settings.get("angular_momentum_tolerance", settings["force_tolerance"])),
            energy_tol=float(settings["energy_tolerance"]),
            methods=[hoomd.md.methods.ConstantVolume(filter=all_filter)],
            forces=forces,
        )
        simulation.operations.integrator = fire
        maximum = int(settings["max_iterations"])
        block = max(1, int(settings.get("steps_per_check", 10)))
        while simulation.timestep < maximum and not fire.converged:
            simulation.run(min(block, maximum - simulation.timestep))
        final_snapshot = simulation.state.get_snapshot()
        result = {
            **system,
            "particles": {
                **particles,
                "positions": np.asarray(final_snapshot.particles.position, dtype=float).tolist(),
            },
            "converged": bool(fire.converged),
            "steps": int(simulation.timestep),
            "potential_energy": float(sum(force.energy for force in forces)),
            "energy_unit": "reduced_energy",
        }
    else:
        ensemble = str(settings["ensemble"]).upper()
        temperature = float(settings["temperature_energy"])
        if ensemble == "NVE":
            integration_method = hoomd.md.methods.ConstantVolume(filter=all_filter)
        elif ensemble == "NVT":
            thermostat = hoomd.md.methods.thermostats.Bussi(
                kT=temperature,
                tau=float(settings.get("thermostat_tau", 1.0)),
            )
            integration_method = hoomd.md.methods.ConstantVolume(
                filter=all_filter, thermostat=thermostat
            )
        else:
            raise ValueError("The validated HOOMD adapter supports NVE or NVT")
        simulation.operations.integrator = hoomd.md.Integrator(
            dt=float(settings["timestep"]), methods=[integration_method], forces=forces
        )
        if bool(settings["initialize_velocities"]):
            simulation.state.thermalize_particle_momenta(filter=all_filter, kT=temperature)
        interval = int(settings["report_interval"])
        steps = int(settings["steps"])
        if interval < 1 or interval > steps:
            raise ValueError("report_interval must be between 1 and steps")
        trajectory_path = directory / "trajectory.gsd"
        simulation.operations.writers.append(
            hoomd.write.GSD(
                trigger=hoomd.trigger.Periodic(interval),
                filename=str(trajectory_path),
                filter=all_filter,
                mode="wb",
                dynamic=["property", "momentum"],
            )
        )
        simulation.run(steps)
        final_snapshot = simulation.state.get_snapshot()
        result = {
            "trajectory_path": relative_workspace_path(trajectory_path),
            "final_state": {
                "box": [float(value) for value in final_snapshot.configuration.box],
                "positions": np.asarray(final_snapshot.particles.position, dtype=float).tolist(),
                "velocities": np.asarray(final_snapshot.particles.velocity, dtype=float).tolist(),
                "type_names": list(final_snapshot.particles.types),
                "type_ids": np.asarray(final_snapshot.particles.typeid, dtype=int).tolist(),
            },
            "ensemble": ensemble,
            "temperature_energy": temperature,
            "timestep": float(settings["timestep"]),
            "steps": steps,
            "potential_energy": float(sum(force.energy for force in forces)),
            "energy_unit": "reduced_energy",
        }
    state_path = write_json(directory, "final_state.json", result)
    values = {
        "artifact_files": command_artifacts(directory),
        "backend_version": hoomd.version.version,
        "provenance": {"device": device_name, "unit_system": "reduced_lj"},
    }
    if action_id == "minimize_system_energy" and not result["converged"]:
        return partial_success(
            result,
            warnings=["HOOMD FIRE reached max_iterations before convergence."],
            **values,
        )
    return success(result, **values)


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

    def frame_slice() -> tuple[int, int | None, int]:
        start = int(settings.get("start_frame", 0))
        raw_stop = int(settings.get("stop_frame", -1))
        step = int(settings.get("frame_stride", 1))
        if start < 0 or step < 1:
            raise ValueError("start_frame must be nonnegative and frame_stride must be positive")
        stop = None if raw_stop == -1 else raw_stop
        if stop is not None and stop <= start:
            raise ValueError("stop_frame must be -1 or greater than start_frame")
        return start, stop, step

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
    elif action_id == "calculate_dihedral_distribution":
        from MDAnalysis.lib.distances import calc_dihedrals

        quartets = np.asarray(inputs["atom_quartets"], dtype=int)
        if quartets.ndim != 2 or quartets.shape[1] != 4 or len(quartets) == 0:
            raise ValueError("atom_quartets must be a non-empty Nx4 integer matrix")
        if quartets.min() < 0 or quartets.max() >= len(universe.atoms):
            raise ValueError("atom_quartets contains an atom index outside the topology")
        values, times = [], []
        for frame in universe.trajectory:
            positions = universe.atoms.positions
            box = frame.dimensions if bool(settings["periodic"]) else None
            values.append(
                calc_dihedrals(
                    positions[quartets[:, 0]], positions[quartets[:, 1]],
                    positions[quartets[:, 2]], positions[quartets[:, 3]], box=box,
                ).tolist()
            )
            times.append(float(frame.time))
        result = {
            "time_ps": times,
            "angles_radian": values,
            "angles_degree": np.degrees(np.asarray(values, dtype=float)).tolist(),
            "atom_quartets": quartets.tolist(),
        }
    elif action_id == "calculate_hydrogen_bonds":
        from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis

        start, stop, step = frame_slice()
        between = inputs.get("between_selections")
        if between is not None:
            if not isinstance(between, list) or not between:
                raise ValueError("between_selections must be a non-empty pair or list of selection pairs")
            if all(isinstance(item, str) for item in between):
                if len(between) != 2:
                    raise ValueError("between_selections pair must contain exactly two selections")
            elif not all(
                isinstance(item, (list, tuple))
                and len(item) == 2
                and all(isinstance(selection, str) for selection in item)
                for item in between
            ):
                raise ValueError("between_selections must contain two-string selection pairs")
        analysis = HydrogenBondAnalysis(
            universe,
            donors_sel=str(settings["donor_selection"]),
            hydrogens_sel=str(settings["hydrogen_selection"]),
            acceptors_sel=str(settings["acceptor_selection"]),
            between=between,
            d_h_cutoff=float(settings["donor_hydrogen_cutoff_angstrom"]),
            d_a_cutoff=float(settings["donor_acceptor_cutoff_angstrom"]),
            d_h_a_angle_cutoff=float(settings["angle_cutoff_degrees"]),
            update_selections=bool(settings["update_selections"]),
        ).run(start=start, stop=stop, step=step)
        raw_events = np.asarray(analysis.results.hbonds, dtype=float)
        if raw_events.size == 0:
            raw_events = np.empty((0, 6), dtype=float)
        maximum = int(settings["max_events"])
        if maximum < 1 or maximum > 1_000_000:
            raise ValueError("max_events must be between 1 and 1000000")
        events = [
            {
                "frame": int(row[0]),
                "donor_atom_index": int(row[1]),
                "hydrogen_atom_index": int(row[2]),
                "acceptor_atom_index": int(row[3]),
                "donor_acceptor_distance_angstrom": float(row[4]),
                "donor_hydrogen_acceptor_angle_degrees": float(row[5]),
            }
            for row in raw_events[:maximum]
        ]
        triples = raw_events[:, 1:4].astype(int) if len(raw_events) else np.empty((0, 3), dtype=int)
        unique, counts = (
            np.unique(triples, axis=0, return_counts=True)
            if len(triples) else (np.empty((0, 3), dtype=int), np.empty(0, dtype=int))
        )
        result = {
            "events": events,
            "event_count": int(len(raw_events)),
            "events_truncated": len(raw_events) > maximum,
            "time_ps": np.asarray(analysis.times, dtype=float).tolist(),
            "counts_by_frame": np.asarray(analysis.count_by_time(), dtype=int).tolist(),
            "bond_occupancies": [
                {
                    "donor_atom_index": int(pair[0]),
                    "hydrogen_atom_index": int(pair[1]),
                    "acceptor_atom_index": int(pair[2]),
                    "observed_frame_count": int(count),
                }
                for pair, count in zip(unique, counts)
            ],
            "selections": {
                "donor": str(settings["donor_selection"]),
                "hydrogen": str(settings["hydrogen_selection"]),
                "acceptor": str(settings["acceptor_selection"]),
                "between": between,
            },
            "cutoffs": {
                "donor_hydrogen_angstrom": float(settings["donor_hydrogen_cutoff_angstrom"]),
                "donor_acceptor_angstrom": float(settings["donor_acceptor_cutoff_angstrom"]),
                "angle_degrees": float(settings["angle_cutoff_degrees"]),
            },
        }
        if len(raw_events) > maximum:
            return partial_success(
                result,
                backend_version=module_version("MDAnalysis"),
                warnings=["Hydrogen-bond event records were truncated at max_events; aggregate counts are complete."],
            )
    elif action_id == "calculate_principal_components":
        from MDAnalysis.analysis.pca import PCA

        start, stop, step = frame_slice()
        selection = str(settings["selection"])
        atoms = universe.select_atoms(selection)
        maximum_atoms = int(settings["max_atoms"])
        if len(atoms) == 0:
            raise ValueError("selection matched no atoms")
        if maximum_atoms < 1 or len(atoms) > maximum_atoms:
            raise ValueError(f"selection contains {len(atoms)} atoms, exceeding max_atoms={maximum_atoms}")
        components = int(settings["n_components"])
        if components < 1 or components > 3 * len(atoms):
            raise ValueError("n_components must be between 1 and three times the selected atom count")
        analysis = PCA(
            universe,
            select=selection,
            align=bool(settings["align"]),
            n_components=components,
        ).run(start=start, stop=stop, step=step)
        projections = np.asarray(
            analysis.transform(
                atoms,
                n_components=components,
                start=start,
                stop=stop,
                step=step,
            ),
            dtype=float,
        )
        eigenvectors = np.asarray(analysis.results.p_components, dtype=float)[:, :components]
        result = {
            "atom_indices": atoms.indices.astype(int).tolist(),
            "selection": selection,
            "aligned": bool(settings["align"]),
            "component_count": components,
            "variance": np.asarray(analysis.results.variance, dtype=float)[:components].tolist(),
            "cumulative_variance": np.asarray(
                analysis.results.cumulated_variance, dtype=float
            )[:components].tolist(),
            "frame_projections": projections.tolist(),
            "mean_coordinates_angstrom": np.asarray(analysis.mean, dtype=float).reshape(-1, 3).tolist(),
            "eigenvectors": eigenvectors.tolist() if bool(settings["include_eigenvectors"]) else None,
        }
    elif action_id == "calculate_dynamic_cross_correlation":
        from MDAnalysis.analysis import align

        start, stop, step = frame_slice()
        selection = str(settings["selection"])
        atoms = universe.select_atoms(selection)
        maximum_atoms = int(settings["max_atoms"])
        if len(atoms) == 0:
            raise ValueError("selection matched no atoms")
        if maximum_atoms < 1 or len(atoms) > maximum_atoms:
            raise ValueError(f"selection contains {len(atoms)} atoms, exceeding max_atoms={maximum_atoms}")
        reference_frame = int(settings["reference_frame"])
        if reference_frame < 0 or reference_frame >= len(universe.trajectory):
            raise ValueError("reference_frame is outside the trajectory")
        if bool(settings["align"]):
            reference = mda.Universe(str(topology), str(trajectory))
            reference.trajectory[reference_frame]
            alignment_selection = str(settings["alignment_selection"]).strip()
            if not alignment_selection:
                raise ValueError("alignment_selection cannot be empty when align is true")
            align.AlignTraj(
                universe,
                reference,
                select=alignment_selection,
                in_memory=True,
            ).run(start=start, stop=stop, step=step)
        coordinates = []
        times = []
        for frame in universe.trajectory[start:stop:step]:
            coordinates.append(atoms.positions.copy())
            times.append(float(frame.time))
        positions = np.asarray(coordinates, dtype=float)
        if len(positions) < 2:
            raise ValueError("Dynamic cross-correlation requires at least two selected frames")
        fluctuations = positions - positions.mean(axis=0, keepdims=True)
        numerator = np.einsum("tix,tjx->ij", fluctuations, fluctuations)
        magnitudes = np.sqrt(np.einsum("tix,tix->i", fluctuations, fluctuations))
        denominator = np.outer(magnitudes, magnitudes)
        correlation = np.divide(
            numerator,
            denominator,
            out=np.zeros_like(numerator),
            where=denominator > 0,
        )
        result = {
            "matrix": correlation.tolist(),
            "atom_indices": atoms.indices.astype(int).tolist(),
            "selection": selection,
            "aligned": bool(settings["align"]),
            "alignment_selection": str(settings["alignment_selection"]),
            "reference_frame": reference_frame,
            "time_ps": times,
            "frame_count": len(times),
        }
    else:
        return unsupported(f"MDAnalysis does not implement {action_id}")
    return success(result, backend_version=module_version("MDAnalysis"))


def _mdtraj(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import mdtraj as md
    import numpy as np

    inputs, _method, settings = request_parts(request)
    topology, trajectory = _trajectory_files(inputs)
    value = md.load(str(trajectory), top=str(topology))
    time_ps = np.asarray(value.time, dtype=float).tolist()
    if action_id == "calculate_trajectory_rmsd":
        indices = np.asarray(settings["atom_indices"], dtype=int)
        if indices.ndim != 1 or len(indices) == 0:
            raise ValueError("atom_indices must be a non-empty integer list")
        reference_value = inputs.get("reference")
        reference = md.load(str(resolve_input_file(reference_value)), top=str(topology)) if reference_value else value
        frame = int(settings["reference_frame"])
        if frame < 0 or frame >= reference.n_frames:
            raise ValueError("reference_frame is outside the reference trajectory")
        rmsd_nm = md.rmsd(value, reference, frame=frame, atom_indices=indices)
        result = {
            "time_ps": time_ps,
            "rmsd_angstrom": (np.asarray(rmsd_nm) * 10.0).tolist(),
            "atom_indices": indices.tolist(),
            "reference_frame": frame,
        }
    elif action_id == "calculate_radius_of_gyration":
        indices = np.asarray(settings["atom_indices"], dtype=int)
        if indices.ndim != 1 or len(indices) == 0:
            raise ValueError("atom_indices must be a non-empty integer list")
        selected = value.atom_slice(indices)
        result = {
            "time_ps": time_ps,
            "radius_of_gyration_angstrom": (md.compute_rg(selected) * 10.0).tolist(),
            "atom_indices": indices.tolist(),
        }
    elif action_id == "calculate_contacts":
        pairs = np.asarray(inputs["residue_pairs"], dtype=int)
        if pairs.ndim != 2 or pairs.shape[1] != 2 or len(pairs) == 0:
            raise ValueError("residue_pairs must be a non-empty Nx2 integer matrix")
        distances, returned_pairs = md.compute_contacts(
            value,
            contacts=pairs,
            scheme=str(settings["scheme"]),
            periodic=bool(settings["periodic"]),
            soft_min=bool(settings["soft_min"]),
            soft_min_beta=float(settings.get("soft_min_beta", 20.0)),
        )
        result = {
            "time_ps": time_ps,
            "distance_angstrom": (np.asarray(distances) * 10.0).tolist(),
            "residue_pairs": np.asarray(returned_pairs, dtype=int).tolist(),
            "scheme": str(settings["scheme"]),
        }
    elif action_id == "calculate_solvent_accessible_surface":
        mode = str(settings["mode"]).lower()
        if mode not in {"atom", "residue"}:
            raise ValueError("mode must be atom or residue")
        areas = md.shrake_rupley(
            value,
            probe_radius=float(settings["probe_radius_nm"]),
            n_sphere_points=int(settings["sphere_points"]),
            mode=mode,
        )
        result = {
            "time_ps": time_ps,
            "surface_area_nm2": np.asarray(areas, dtype=float).tolist(),
            "mode": mode,
            "probe_radius_nm": float(settings["probe_radius_nm"]),
        }
    elif action_id == "calculate_dihedral_distribution":
        quartets = np.asarray(inputs["atom_quartets"], dtype=int)
        if quartets.ndim != 2 or quartets.shape[1] != 4 or len(quartets) == 0:
            raise ValueError("atom_quartets must be a non-empty Nx4 integer matrix")
        angles = md.compute_dihedrals(value, quartets, periodic=bool(settings["periodic"]))
        result = {
            "time_ps": time_ps,
            "angles_radian": np.asarray(angles, dtype=float).tolist(),
            "angles_degree": np.degrees(np.asarray(angles, dtype=float)).tolist(),
            "atom_quartets": quartets.tolist(),
        }
    elif action_id == "assign_secondary_structure":
        if not isinstance(settings["simplified"], bool):
            raise ValueError("simplified must be an explicit boolean")
        assignments = md.compute_dssp(value, simplified=settings["simplified"])
        residues = [
            {
                "residue_index": int(residue.index),
                "name": str(residue.name),
                "residue_sequence_number": int(residue.resSeq),
                "chain_index": int(residue.chain.index),
            }
            for residue in value.topology.residues
        ]
        result = {
            "time_ps": time_ps,
            "assignments": np.asarray(assignments, dtype=str).tolist(),
            "residues": residues,
            "simplified": settings["simplified"],
            "label_set": ["H", "E", "C", "NA"] if settings["simplified"] else None,
        }
    elif action_id == "cluster_trajectory":
        indices = np.asarray(settings["atom_indices"], dtype=int)
        if indices.ndim != 1 or len(indices) == 0:
            raise ValueError("atom_indices must be a non-empty integer list")
        if indices.min() < 0 or indices.max() >= value.n_atoms:
            raise ValueError("atom_indices contains an index outside the trajectory topology")
        stride = int(settings["frame_stride"])
        maximum = int(settings["max_clusters"])
        cutoff_angstrom = float(settings["rmsd_cutoff_angstrom"])
        if stride < 1:
            raise ValueError("frame_stride must be positive")
        if maximum < 1 or maximum > 10000:
            raise ValueError("max_clusters must be between 1 and 10000")
        if not np.isfinite(cutoff_angstrom) or cutoff_angstrom <= 0:
            raise ValueError("rmsd_cutoff_angstrom must be positive and finite")
        frame_indices = np.arange(0, value.n_frames, stride, dtype=int)
        sampled = value.slice(frame_indices, copy=True)
        cutoff_nm = cutoff_angstrom / 10.0
        unassigned = set(range(sampled.n_frames))
        leaders: list[int] = []
        while unassigned and len(leaders) < maximum:
            leader = min(unassigned)
            leaders.append(leader)
            distances = np.asarray(
                md.rmsd(sampled, sampled, frame=leader, atom_indices=indices), dtype=float
            )
            assigned_now = [index for index in unassigned if distances[index] <= cutoff_nm]
            unassigned.difference_update(assigned_now)
        distance_matrix = np.vstack(
            [
                np.asarray(md.rmsd(sampled, sampled, frame=leader, atom_indices=indices), dtype=float)
                for leader in leaders
            ]
        )
        assignments = np.argmin(distance_matrix, axis=0)
        assigned_distances = distance_matrix[assignments, np.arange(sampled.n_frames)]
        sizes = [int(np.sum(assignments == index)) for index in range(len(leaders))]
        result = {
            "sampled_frame_indices": frame_indices.tolist(),
            "cluster_assignments": assignments.astype(int).tolist(),
            "representative_frame_indices": [int(frame_indices[index]) for index in leaders],
            "cluster_sizes": sizes,
            "cluster_count": len(leaders),
            "atom_indices": indices.tolist(),
            "frame_stride": stride,
            "rmsd_cutoff_angstrom": cutoff_angstrom,
            "assigned_rmsd_angstrom": (assigned_distances * 10.0).tolist(),
            "assignments_exceeding_cutoff": int(np.sum(assigned_distances > cutoff_nm)),
            "max_clusters_reached": bool(unassigned),
        }
    else:
        return unsupported(f"MDTraj does not implement {action_id}")
    return success(result, backend_version=module_version("mdtraj"))


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


def _pymbar(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    import pymbar

    inputs, _method, settings = request_parts(request)
    reduced = np.asarray(inputs["reduced_potentials"], dtype=float)
    counts = np.asarray(inputs["samples_per_state"], dtype=int)
    if reduced.ndim != 2:
        raise ValueError("reduced_potentials must be a KxN matrix")
    if counts.ndim != 1 or len(counts) != reduced.shape[0]:
        raise ValueError("samples_per_state must contain one count for each thermodynamic state")
    if np.any(counts < 0) or int(counts.sum()) != reduced.shape[1]:
        raise ValueError("samples_per_state must be nonnegative and sum to the number of samples")
    if not np.all(np.isfinite(reduced)):
        raise ValueError("reduced_potentials must contain only finite values")
    maximum_iterations = int(settings["maximum_iterations"])
    relative_tolerance = float(settings["relative_tolerance"])
    if maximum_iterations < 1 or relative_tolerance <= 0:
        raise ValueError("maximum_iterations and relative_tolerance must be positive")

    def uncertainty_configuration() -> tuple[str, str | None, int]:
        uncertainty = str(settings["uncertainty_method"]).strip().lower()
        if uncertainty == "default":
            uncertainty_value = None
        elif uncertainty in {"svd", "svd-ew", "bootstrap"}:
            uncertainty_value = uncertainty
        else:
            raise ValueError("uncertainty_method must be default, svd, svd-ew, or bootstrap")
        bootstraps = int(settings.get("bootstrap_samples", 0))
        if uncertainty == "bootstrap" and bootstraps < 1:
            raise ValueError("bootstrap uncertainty requires bootstrap_samples >= 1")
        return uncertainty, uncertainty_value, bootstraps

    def estimator_for(matrix, sample_counts, *, bootstraps: int = 0):
        return pymbar.MBAR(
            matrix,
            sample_counts,
            maximum_iterations=maximum_iterations,
            relative_tolerance=relative_tolerance,
            initialize=str(settings.get("initialize", "zeros")),
            n_bootstraps=bootstraps,
            rseed=int(settings.get("random_seed", 0)),
            verbose=False,
        )

    if action_id == "estimate_thermodynamic_expectations":
        observables = np.asarray(inputs["observables"], dtype=float)
        if observables.ndim != 1 or len(observables) != reduced.shape[1]:
            raise ValueError("observables must be one finite value for each reduced-potential sample")
        if not np.all(np.isfinite(observables)):
            raise ValueError("observables must contain only finite values")
        output = str(settings["output"]).strip().lower()
        if output not in {"averages", "differences"}:
            raise ValueError("output must be averages or differences")
        estimates = estimator_for(reduced, counts).compute_expectations(observables, output=output)
        return success(
            {
                "expectation": np.asarray(estimates["mu"], dtype=float).tolist(),
                "uncertainty": np.asarray(estimates["sigma"], dtype=float).tolist(),
                "output": output,
                "observable_unit": str(settings["observable_unit"]),
                "state_count": int(reduced.shape[0]),
                "sample_count": int(reduced.shape[1]),
                "samples_per_state": counts.tolist(),
            },
            backend_version=module_version("pymbar"),
        )

    if action_id == "calculate_potential_of_mean_force":
        target = np.asarray(inputs["target_reduced_potential"], dtype=float)
        coordinate = np.asarray(inputs["collective_variable"], dtype=float)
        if target.ndim != 1 or len(target) != reduced.shape[1] or not np.all(np.isfinite(target)):
            raise ValueError("target_reduced_potential must contain one finite value per sample")
        if coordinate.ndim != 1 or len(coordinate) != reduced.shape[1] or not np.all(np.isfinite(coordinate)):
            raise ValueError("collective_variable must contain one finite scalar value per sample")
        edges = np.asarray(settings["bin_edges"], dtype=float)
        if edges.ndim != 1 or len(edges) < 3 or not np.all(np.isfinite(edges)):
            raise ValueError("bin_edges must contain at least three finite values")
        if not np.all(np.diff(edges) > 0):
            raise ValueError("bin_edges must be strictly increasing")
        indices = np.searchsorted(edges, coordinate, side="right") - 1
        indices[coordinate == edges[-1]] = len(edges) - 2
        if np.any(indices < 0) or np.any(indices >= len(edges) - 1):
            raise ValueError("Every collective-variable sample must lie inside the explicit bin range")
        occupied = sorted({int(value) for value in indices})
        centers = np.asarray([(edges[index] + edges[index + 1]) / 2 for index in occupied])
        uncertainty = str(settings["uncertainty_method"]).strip().lower()
        if uncertainty == "none":
            uncertainty_value = None
        elif uncertainty == "analytical":
            uncertainty_value = "analytical"
        else:
            raise ValueError("uncertainty_method must be none or analytical")
        reference = str(settings["reference"]).strip().lower()
        if reference == "lowest":
            reference_point = "from-lowest"
            reference_coordinate = None
        elif reference == "specified":
            if settings.get("reference_coordinate") is None:
                raise ValueError("reference='specified' requires reference_coordinate")
            reference_coordinate = float(settings["reference_coordinate"])
            if not np.isfinite(reference_coordinate):
                raise ValueError("reference_coordinate must be finite")
            reference_bin = int(np.searchsorted(edges, reference_coordinate, side="right") - 1)
            if reference_coordinate == edges[-1]:
                reference_bin = len(edges) - 2
            if reference_bin not in occupied:
                raise ValueError("reference_coordinate must lie in an occupied explicit bin")
            reference_point = "from-specified"
        else:
            raise ValueError("reference must be lowest or specified")
        estimator = pymbar.FES(
            reduced,
            counts,
            mbar_options={
                "maximum_iterations": maximum_iterations,
                "relative_tolerance": relative_tolerance,
                "initialize": str(settings.get("initialize", "zeros")),
            },
        )
        estimator.generate_fes(
            target,
            coordinate[:, None],
            fes_type="histogram",
            histogram_parameters={"bin_edges": [edges]},
        )
        estimates = estimator.get_fes(
            centers[:, None],
            reference_point=reference_point,
            fes_reference=reference_coordinate,
            uncertainty_method=uncertainty_value,
        )
        free_energy = np.asarray(estimates["f_i"], dtype=float)
        uncertainty_values = (
            np.asarray(estimates["df_i"], dtype=float)
            if "df_i" in estimates else None
        )
        bins = []
        for output_index, bin_index in enumerate(occupied):
            record = {
                "bin_index": bin_index,
                "lower_edge": float(edges[bin_index]),
                "upper_edge": float(edges[bin_index + 1]),
                "center": float(centers[output_index]),
                "sample_count": int(np.sum(indices == bin_index)),
                "free_energy_reduced": float(free_energy[output_index]),
            }
            if uncertainty_values is not None:
                record["uncertainty_reduced"] = float(uncertainty_values[output_index])
            if settings.get("temperature_kelvin") is not None:
                factor = 0.00831446261815324 * float(settings["temperature_kelvin"])
                record["free_energy_kj_mol"] = record["free_energy_reduced"] * factor
                if uncertainty_values is not None:
                    record["uncertainty_kj_mol"] = record["uncertainty_reduced"] * factor
            bins.append(record)
        return success(
            {
                "bins": bins,
                "bin_edges": edges.tolist(),
                "occupied_bin_count": len(occupied),
                "empty_bin_count": int(len(edges) - 1 - len(occupied)),
                "sample_count": int(len(coordinate)),
                "coordinate_unit": str(settings.get("coordinate_unit", "unspecified")),
                "reference": reference,
                "reference_coordinate": reference_coordinate,
                "uncertainty_method": uncertainty,
                "temperature_kelvin": settings.get("temperature_kelvin"),
                "method_note": "PyMBAR histogram FES; not thermodynamic integration of a mean force.",
            },
            backend_version=module_version("pymbar"),
        )

    if action_id == "analyze_free_energy_convergence":
        raw_fractions = settings["fractions"]
        if not isinstance(raw_fractions, (list, tuple)) or not raw_fractions:
            raise ValueError("fractions must be a non-empty list")
        fractions = [float(value) for value in raw_fractions]
        if any(not np.isfinite(value) or value <= 0 or value > 1 for value in fractions):
            raise ValueError("every convergence fraction must satisfy 0 < fraction <= 1")
        if fractions != sorted(set(fractions)):
            raise ValueError("fractions must be strictly increasing and unique")
        pair = np.asarray(settings["state_pair"], dtype=int)
        if pair.shape != (2,) or pair.min() < 0 or pair.max() >= reduced.shape[0] or pair[0] == pair[1]:
            raise ValueError("state_pair must contain two distinct valid zero-based state indices")
        uncertainty, uncertainty_value, bootstraps = uncertainty_configuration()
        offsets = np.concatenate(([0], np.cumsum(counts)))
        convergence = []
        for fraction in fractions:
            subcounts = np.asarray(
                [max(1, int(np.floor(value * fraction))) if value > 0 else 0 for value in counts],
                dtype=int,
            )
            columns = np.concatenate(
                [
                    np.arange(offsets[index], offsets[index] + subcounts[index], dtype=int)
                    for index in range(len(counts)) if subcounts[index] > 0
                ]
            )
            submatrix = reduced[:, columns]
            estimates = estimator_for(submatrix, subcounts, bootstraps=bootstraps).compute_free_energy_differences(
                compute_uncertainty=True,
                uncertainty_method=uncertainty_value,
            )
            delta = float(estimates["Delta_f"][pair[0], pair[1]])
            sigma = float(estimates["dDelta_f"][pair[0], pair[1]])
            record = {
                "fraction": fraction,
                "sample_count": int(subcounts.sum()),
                "samples_per_state": subcounts.tolist(),
                "delta_f": delta,
                "delta_f_uncertainty": sigma,
            }
            if settings.get("temperature_kelvin") is not None:
                factor = 0.00831446261815324 * float(settings["temperature_kelvin"])
                record["delta_g_kj_mol"] = delta * factor
                record["delta_g_uncertainty_kj_mol"] = sigma * factor
            convergence.append(record)
        return success(
            {
                "state_pair": pair.tolist(),
                "convergence": convergence,
                "uncertainty_method": uncertainty,
                "unit": "dimensionless_reduced_free_energy",
                "temperature_kelvin": settings.get("temperature_kelvin"),
            },
            backend_version=module_version("pymbar"),
        )

    uncertainty, uncertainty_value, bootstraps = uncertainty_configuration()
    estimator = estimator_for(reduced, counts, bootstraps=bootstraps)
    estimates = estimator.compute_free_energy_differences(
        compute_uncertainty=True,
        uncertainty_method=uncertainty_value,
        return_theta=bool(settings.get("include_theta", False)),
    )
    result = {
        "delta_f": np.asarray(estimates["Delta_f"], dtype=float).tolist(),
        "delta_f_uncertainty": np.asarray(estimates["dDelta_f"], dtype=float).tolist(),
        "unit": "dimensionless_reduced_free_energy",
        "state_count": int(reduced.shape[0]),
        "sample_count": int(reduced.shape[1]),
        "samples_per_state": counts.tolist(),
        "uncertainty_method": uncertainty,
    }
    if "Theta" in estimates:
        result["asymptotic_covariance"] = np.asarray(estimates["Theta"], dtype=float).tolist()
    temperature = settings.get("temperature_kelvin")
    if temperature is not None:
        gas_constant_kj_mol_k = 0.00831446261815324
        factor = gas_constant_kj_mol_k * float(temperature)
        result["delta_g_kj_mol"] = (np.asarray(estimates["Delta_f"]) * factor).tolist()
        result["delta_g_uncertainty_kj_mol"] = (
            np.asarray(estimates["dDelta_f"]) * factor
        ).tolist()
        result["temperature_kelvin"] = float(temperature)
    return success(result, backend_version=module_version("pymbar"))


def _alchemlyb(request: dict[str, Any]) -> dict[str, Any]:
    import pandas as pd
    from alchemlyb import concat

    inputs, _method, settings = request_parts(request)
    raw_files = inputs["files"]
    if not isinstance(raw_files, list):
        raw_files = [raw_files]
    if not raw_files:
        raise ValueError("files must contain at least one alchemical output Artifact")
    paths = [resolve_input_file(value) for value in raw_files]
    engine = str(settings["engine"]).strip().lower()
    observable = str(settings["observable"]).strip().lower()
    temperature = float(settings["temperature_kelvin"])
    filter_rows = bool(settings["filter_invalid_rows"])
    if observable not in {"u_nk", "dhdl"}:
        raise ValueError("observable must be u_nk or dhdl")
    frames = []
    for path in paths:
        if engine == "gromacs":
            from alchemlyb.parsing import gmx

            parser = gmx.extract_u_nk if observable == "u_nk" else gmx.extract_dHdl
            frame = parser(str(path), T=temperature, filter=filter_rows)
        elif engine == "amber":
            from alchemlyb.parsing import amber

            parser = amber.extract_u_nk if observable == "u_nk" else amber.extract_dHdl
            frame = parser(str(path), T=temperature)
        elif engine == "namd":
            if observable != "u_nk":
                raise ValueError("alchemlyb NAMD parsing exposes u_nk, not dhdl")
            from alchemlyb.parsing import namd

            frame = namd.extract_u_nk(str(path), T=temperature)
        else:
            raise ValueError("engine must be gromacs, amber, or namd")
        if frame is None:
            raise RuntimeError(f"alchemlyb returned no data for {path}")
        frames.append(frame)
    combined = concat(frames) if len(frames) > 1 else frames[0]
    if not isinstance(combined, pd.DataFrame) or combined.empty:
        raise RuntimeError("alchemlyb produced an empty normalized table")
    directory = output_directory("parse_alchemical_energy_data", "alchemlyb")
    output_path = directory / f"{observable}.csv"
    combined.to_csv(output_path)
    columns = [
        list(value) if isinstance(value, tuple) else value
        for value in combined.columns.tolist()
    ]
    result = {
        "data_path": relative_workspace_path(output_path),
        "engine": engine,
        "observable": observable,
        "temperature_kelvin": temperature,
        "energy_unit": combined.attrs.get("energy_unit", "kT"),
        "row_count": int(len(combined)),
        "column_count": int(len(combined.columns)),
        "index_names": [str(value) for value in combined.index.names],
        "columns": columns,
        "source_files": [relative_workspace_path(path) for path in paths],
    }
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=module_version("alchemlyb"),
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "openmm":
        return _openmm(action_id, request)
    if backend_id == "gromacs":
        return _gromacs(action_id, request)
    if backend_id == "lammps":
        return _lammps(action_id, request)
    if backend_id == "hoomd":
        return _hoomd(action_id, request)
    if backend_id == "namd":
        return _namd(action_id, request)
    if backend_id == "amber_pmemd":
        return _amber_pmemd(action_id, request)
    if backend_id == "charmm":
        return _charmm(action_id, request)
    if backend_id == "mdanalysis":
        return _mdanalysis(action_id, request)
    if backend_id == "mdtraj":
        return _mdtraj(action_id, request)
    if backend_id == "plumed":
        return _plumed(request)
    if backend_id == "pymbar" and action_id in {
        "estimate_free_energy_difference", "estimate_thermodynamic_expectations",
        "calculate_potential_of_mean_force", "analyze_free_energy_convergence",
    }:
        return _pymbar(action_id, request)
    if backend_id == "alchemlyb" and action_id == "parse_alchemical_energy_data":
        return _alchemlyb(request)
    return unsupported(f"Unsupported dynamics action/backend combination: {action_id}/{backend_id}")

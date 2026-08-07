"""Typed single-segment adapters for NAMD, Amber PMEMD, and CHARMM."""

from __future__ import annotations

import math
import os
import re
import shutil
from pathlib import Path
from typing import Any

from .common import (
    command_artifacts,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    run_external,
    success,
    unavailable,
    unsupported,
)


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[DdEe][-+]?\d+)?"


def _system_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and "result" in value and isinstance(value["result"], dict):
        value = value["result"]
    if not isinstance(value, dict):
        raise ValueError("system must be a ParameterizedSystem mapping or Artifact result")
    return dict(value)


def _system_path(system: dict[str, Any], *keys: str, required: bool = True) -> Path | None:
    for key in keys:
        if system.get(key) is not None:
            return resolve_input_file(system[key])
    if required:
        raise ValueError(f"system must contain one of: {', '.join(keys)}")
    return None


def _system_paths(system: dict[str, Any], *keys: str) -> list[Path]:
    value = None
    for key in keys:
        if system.get(key) is not None:
            value = system[key]
            break
    if not isinstance(value, list) or not value:
        raise ValueError(f"system must contain a non-empty list in one of: {', '.join(keys)}")
    return [resolve_input_file(item) for item in value]


def _positive(value: Any, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return result


def _interval(settings: dict[str, Any], steps: int) -> int:
    interval = int(settings["report_interval"])
    if interval < 1 or interval > max(1, steps):
        raise ValueError("report_interval must be between 1 and the number of steps")
    return interval


def _namd_bool(value: Any) -> str:
    return "yes" if bool(value) else "no"


def _namd_path(path: Path) -> str:
    text = str(path)
    if any(character in text for character in ("}", "\n", "\r")):
        raise ValueError("NAMD input paths cannot contain }, carriage returns, or line breaks")
    return "{" + text + "}"


def _render_namd(
    action_id: str,
    system: dict[str, Any],
    method: dict[str, Any],
    settings: dict[str, Any],
) -> str:
    family = str(method["force_field_family"]).strip().lower()
    if family != "charmm":
        raise ValueError("The configured NAMD adapter currently requires force_field_family='charmm'")
    psf = _system_path(system, "namd_psf_path", "psf_path")
    coordinates = _system_path(
        system,
        "namd_binary_coordinates_path",
        "coordinate_path",
        "namd_coordinate_path",
    )
    parameters = _system_paths(system, "namd_parameter_paths", "parameter_paths")
    coordinate_format = str(system.get("namd_coordinate_format") or "").lower()
    binary_coordinates = coordinate_format == "binary" or coordinates.suffix.lower() == ".coor"
    exclude = str(method["exclude"]).strip().lower()
    if exclude not in {"none", "1-2", "1-3", "1-4", "scaled1-4"}:
        raise ValueError("NAMD exclude must be none, 1-2, 1-3, 1-4, or scaled1-4")
    rigid_bonds = str(method["rigid_bonds"]).strip().lower()
    if rigid_bonds not in {"none", "water", "all"}:
        raise ValueError("NAMD rigid_bonds must be none, water, or all")
    lines = [
        f"structure {_namd_path(psf)}",
        f"{'bincoordinates' if binary_coordinates else 'coordinates'} {_namd_path(coordinates)}",
        *[f"parameters {_namd_path(path)}" for path in parameters],
        "paraTypeCharmm on",
        f"exclude {exclude}",
        f"oneFourScaling {_positive(method['one_four_scaling'], 'NAMD one_four_scaling'):.12g}",
        f"cutoff {_positive(method['cutoff_angstrom'], 'NAMD cutoff_angstrom'):.12g}",
        f"switching {_namd_bool(method['switching'])}",
        f"switchdist {_positive(method['switch_distance_angstrom'], 'NAMD switch_distance_angstrom'):.12g}",
        f"pairlistdist {_positive(method['pairlist_distance_angstrom'], 'NAMD pairlist_distance_angstrom'):.12g}",
        f"PME {_namd_bool(method['pme'])}",
        f"rigidBonds {rigid_bonds}",
        f"margin {_positive(method.get('margin_angstrom', 1.0), 'NAMD margin_angstrom'):.12g}",
        "outputName segment",
        "binaryoutput yes",
    ]
    extended = _system_path(system, "extended_system_path", "namd_extended_system_path", required=False)
    if extended is not None:
        lines.append(f"extendedSystem {_namd_path(extended)}")
    elif system.get("cell_basis_vectors_angstrom") is not None:
        vectors = system["cell_basis_vectors_angstrom"]
        if not isinstance(vectors, list) or len(vectors) != 3 or any(len(row) != 3 for row in vectors):
            raise ValueError("cell_basis_vectors_angstrom must contain three three-component vectors")
        for index, row in enumerate(vectors, start=1):
            lines.append(f"cellBasisVector{index} {float(row[0])} {float(row[1])} {float(row[2])}")
        origin = system.get("cell_origin_angstrom", [0.0, 0.0, 0.0])
        if len(origin) != 3:
            raise ValueError("cell_origin_angstrom must contain three values")
        lines.append(f"cellOrigin {float(origin[0])} {float(origin[1])} {float(origin[2])}")
    if bool(method["pme"]) and extended is None and system.get("cell_basis_vectors_angstrom") is None:
        raise ValueError("NAMD PME requires extended_system_path or explicit cell_basis_vectors_angstrom")
    velocity = _system_path(
        system,
        "namd_binary_velocities_path",
        "velocity_path",
        required=False,
    )
    if velocity is not None:
        lines.append(f"binvelocities {_namd_path(velocity)}")
    if action_id == "minimize_system_energy":
        iterations = int(settings["max_iterations"])
        if iterations < 1:
            raise ValueError("NAMD max_iterations must be positive")
        interval = _interval(settings, iterations)
        lines.extend(
            [
                "temperature 0",
                f"stepspercycle {math.gcd(20, iterations)}",
                f"outputEnergies {interval}",
                f"restartfreq {interval}",
                f"minimize {iterations}",
            ]
        )
    elif action_id == "propagate_dynamics":
        steps = int(settings["steps"])
        if steps < 1:
            raise ValueError("NAMD steps must be positive")
        interval = _interval(settings, steps)
        timestep = _positive(settings["timestep_fs"], "NAMD timestep_fs")
        temperature = _positive(settings["temperature_kelvin"], "NAMD temperature_kelvin")
        ensemble = str(settings["ensemble"]).upper()
        if ensemble not in {"NVE", "NVT", "NPT"}:
            raise ValueError("NAMD ensemble must be NVE, NVT, or NPT")
        if velocity is None:
            lines.extend([f"temperature {temperature:.12g}", f"seed {int(settings['random_seed'])}"])
        lines.extend(
            [
                f"timestep {timestep:.12g}",
                f"stepspercycle {math.gcd(20, steps)}",
                f"outputEnergies {interval}",
                f"restartfreq {interval}",
                f"DCDfile segment.dcd",
                f"dcdfreq {interval}",
            ]
        )
        if ensemble in {"NVT", "NPT"}:
            lines.extend(
                [
                    "langevin on",
                    f"langevinTemp {temperature:.12g}",
                    f"langevinDamping {_positive(settings.get('langevin_damping_per_ps', 1.0), 'NAMD Langevin damping'):.12g}",
                    f"langevinHydrogen {_namd_bool(settings.get('langevin_hydrogen', False))}",
                ]
            )
        if ensemble == "NPT":
            if not bool(method["pme"]):
                raise ValueError("NAMD NPT propagation requires PME=true")
            pressure = _positive(settings["pressure_bar"], "NAMD pressure_bar")
            lines.extend(
                [
                    "langevinPiston on",
                    f"langevinPistonTarget {pressure:.12g}",
                    f"langevinPistonPeriod {_positive(settings.get('piston_period_fs', 200.0), 'NAMD piston period'):.12g}",
                    f"langevinPistonDecay {_positive(settings.get('piston_decay_fs', 100.0), 'NAMD piston decay'):.12g}",
                    f"langevinPistonTemp {temperature:.12g}",
                    "useGroupPressure yes",
                    "useFlexibleCell no",
                    "useConstantArea no",
                ]
            )
        lines.append(f"run {steps}")
    else:
        raise ValueError(f"NAMD does not implement {action_id}")
    return "\n".join(lines) + "\n"


def _parse_namd_energy(text: str) -> dict[str, float] | None:
    titles = None
    values = None
    for line in text.splitlines():
        if line.startswith("ETITLE:"):
            titles = line.split(":", 1)[1].split()
        elif line.startswith("ENERGY:"):
            values = line.split(":", 1)[1].split()
    if not titles or not values or len(values) < len(titles):
        return None
    result: dict[str, float] = {}
    for name, value in zip(titles, values):
        try:
            result[name.lower()] = float(value)
        except ValueError:
            continue
    return result


def namd(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    system = _system_mapping(inputs["system"])
    directory = output_directory(action_id, "namd")
    input_path = directory / "segment.namd"
    input_path.write_text(_render_namd(action_id, system, method, settings), encoding="utf-8")
    cores = max(1, int(request.get("resource_limits", {}).get("cpu_cores") or 1))
    completed = run_external(
        executable="namd3",
        environment_variable="CHEMGRAPH_NAMD_COMMAND",
        arguments=[f"+p{cores}", str(input_path)],
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    log_path = directory / "segment.log"
    log_path.write_text(completed["stdout"], encoding="utf-8")
    (directory / "segment.err").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Stage NAMD under .software_cache/installations/namd and configure CHEMGRAPH_NAMD_COMMAND.")
    if completed["returncode"] != 0 or "End of program" not in completed["stdout"]:
        detail = (completed["stderr"] or completed["stdout"])[-4000:]
        raise RuntimeError(f"NAMD failed or did not reach End of program: {detail}")
    version_match = re.search(r"Info: NAMD\s+([^\s]+)", completed["stdout"])
    version = version_match.group(1) if version_match else None
    energy = _parse_namd_energy(completed["stdout"])
    coordinate_path = directory / "segment.coor"
    velocity_path = directory / "segment.vel"
    extended_path = directory / "segment.xsc"
    if not coordinate_path.is_file():
        raise RuntimeError("NAMD completed without segment.coor")
    final_system = {
        **system,
        "coordinate_path": relative_workspace_path(coordinate_path),
        "namd_binary_coordinates_path": relative_workspace_path(coordinate_path),
        "namd_coordinate_format": "binary",
        "namd_binary_velocities_path": relative_workspace_path(velocity_path) if velocity_path.is_file() else None,
        "extended_system_path": relative_workspace_path(extended_path) if extended_path.is_file() else None,
    }
    if action_id == "minimize_system_energy":
        result = {**final_system, "minimized": True, "final_energy_kcal_mol": energy}
    else:
        trajectory = directory / "segment.dcd"
        if not trajectory.is_file():
            raise RuntimeError("NAMD propagation completed without segment.dcd")
        result = {
            "trajectory_path": relative_workspace_path(trajectory),
            "final_system": final_system,
            "ensemble": str(settings["ensemble"]).upper(),
            "temperature_kelvin": float(settings["temperature_kelvin"]),
            "pressure_bar": settings.get("pressure_bar"),
            "timestep_fs": float(settings["timestep_fs"]),
            "steps": int(settings["steps"]),
            "duration_ps": float(settings["timestep_fs"]) * int(settings["steps"]) / 1000.0,
            "final_energy_kcal_mol": energy,
        }
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=version,
        provenance={"command": completed["command"], "parallel_processes": cores, "binary_variant": "multicore-avx512"},
    )


def _amber_constraints(value: Any) -> tuple[int, int]:
    normalized = str(value).strip().lower().replace("-", "_")
    mapping = {"none": (1, 1), "h_bonds": (2, 2), "all_bonds": (3, 3)}
    if normalized not in mapping:
        raise ValueError("Amber constraints must be none, h_bonds, or all_bonds")
    return mapping[normalized]


def _render_amber(
    action_id: str,
    method: dict[str, Any],
    settings: dict[str, Any],
) -> str:
    boundary = str(method["boundary"]).strip().lower()
    if boundary not in {"vacuum", "implicit", "periodic"}:
        raise ValueError("Amber boundary must be vacuum, implicit, or periodic")
    cutoff = _positive(method["cutoff_angstrom"], "Amber cutoff_angstrom")
    ntc, ntf = _amber_constraints(method["constraints"])
    values: list[tuple[str, Any]] = [("cut", cutoff), ("ntc", ntc), ("ntf", ntf)]
    if boundary == "implicit":
        if "igb" not in method:
            raise ValueError("Amber implicit solvent requires method_spec.igb")
        igb = int(method["igb"])
        if igb not in {1, 2, 5, 6, 7, 8, 10}:
            raise ValueError("Amber igb must be one of 1, 2, 5, 6, 7, 8, or 10")
        values.extend([("ntb", 0), ("igb", igb), ("saltcon", float(method.get("saltcon_molar", 0.0)))])
    elif boundary == "vacuum":
        values.extend([("ntb", 0), ("igb", 0)])
    if action_id == "minimize_system_energy":
        maxcyc = int(settings["max_iterations"])
        ncyc = int(settings["steepest_descent_steps"])
        if maxcyc < 1 or ncyc < 0 or ncyc > maxcyc:
            raise ValueError("Amber minimization requires 0 <= steepest_descent_steps <= max_iterations")
        interval = _interval(settings, maxcyc)
        if boundary == "periodic":
            values.append(("ntb", 1))
        values.extend(
            [
                ("imin", 1),
                ("maxcyc", maxcyc),
                ("ncyc", ncyc),
                ("drms", _positive(settings["gradient_tolerance_kcal_mol_angstrom"], "Amber gradient tolerance")),
                ("ntpr", interval),
            ]
        )
    elif action_id == "propagate_dynamics":
        steps = int(settings["steps"])
        if steps < 1:
            raise ValueError("Amber steps must be positive")
        interval = _interval(settings, steps)
        timestep_ps = _positive(settings["timestep_fs"], "Amber timestep_fs") / 1000.0
        temperature = _positive(settings["temperature_kelvin"], "Amber temperature_kelvin")
        ensemble = str(settings["ensemble"]).upper()
        if ensemble not in {"NVE", "NVT", "NPT"}:
            raise ValueError("Amber ensemble must be NVE, NVT, or NPT")
        if ensemble == "NPT" and boundary != "periodic":
            raise ValueError("Amber NPT propagation requires boundary='periodic'")
        restart = bool(settings["restart"])
        values.extend(
            [
                ("imin", 0),
                ("irest", 1 if restart else 0),
                ("ntx", 5 if restart else 1),
                ("nstlim", steps),
                ("dt", timestep_ps),
                ("ntpr", interval),
                ("ntwx", interval),
                ("ntwr", interval),
                ("ioutfm", 1),
                ("ig", int(settings["random_seed"])),
            ]
        )
        if not restart:
            values.append(("tempi", temperature))
        if boundary == "periodic":
            values.append(("ntb", 2 if ensemble == "NPT" else 1))
        if ensemble == "NVE":
            values.append(("ntt", 0))
        else:
            values.extend(
                [
                    ("ntt", 3),
                    ("gamma_ln", _positive(settings.get("langevin_collision_per_ps", 1.0), "Amber Langevin collision rate")),
                    ("temp0", temperature),
                ]
            )
        if ensemble == "NPT":
            values.extend(
                [
                    ("ntp", 1),
                    ("pres0", _positive(settings["pressure_bar"], "Amber pressure_bar")),
                    ("taup", _positive(settings.get("pressure_relaxation_ps", 2.0), "Amber pressure relaxation")),
                ]
            )
    else:
        raise ValueError(f"Amber PMEMD does not implement {action_id}")
    lines = ["ResearchChemBench typed atomic action", " &cntrl"]
    for name, value in values:
        rendered = f"{value:.12g}" if isinstance(value, float) else str(value)
        lines.append(f"  {name}={rendered},")
    lines.extend([" /", ""])
    return "\n".join(lines)


def _parse_amber_energy(text: str) -> float | None:
    final = text.rsplit("FINAL RESULTS", 1)[-1] if "FINAL RESULTS" in text else text
    match = re.search(rf"NSTEP\s+ENERGY[^\n]*\n\s*\d+\s+({_FLOAT})", final)
    if match:
        return float(match.group(1).replace("D", "E"))
    production = text.split("A V E R A G E S", 1)[0]
    matches = re.findall(rf"EPtot\s*=\s*({_FLOAT})", production)
    return float(matches[-1].replace("D", "E")) if matches else None


def amber_pmemd(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    system = _system_mapping(inputs["system"])
    topology = _system_path(system, "amber_topology_path", "prmtop_path", "topology_path")
    coordinates = _system_path(system, "amber_coordinate_path", "coordinate_path", "inpcrd_path")
    reference = _system_path(system, "reference_path", "amber_reference_path", required=False)
    directory = output_directory(action_id, "amber_pmemd")
    mdin = directory / "segment.mdin"
    mdout = directory / "segment.mdout"
    restart = directory / "segment.rst7"
    trajectory = directory / "segment.nc"
    mdinfo = directory / "segment.mdinfo"
    mdin.write_text(_render_amber(action_id, method, settings), encoding="utf-8")
    arguments = [
        "-O", "-i", str(mdin), "-o", str(mdout), "-p", str(topology), "-c", str(coordinates),
        "-r", str(restart), "-x", str(trajectory), "-inf", str(mdinfo),
    ]
    if reference is not None:
        arguments.extend(["-ref", str(reference)])
    cores = max(1, int(request.get("resource_limits", {}).get("cpu_cores") or 1))
    if cores == 1:
        completed = run_external(
            executable="pmemd",
            environment_variable="CHEMGRAPH_AMBER_COMMAND",
            arguments=arguments,
            directory=directory,
            timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
        )
    else:
        mpi_executable = os.environ.get("CHEMGRAPH_AMBER_MPI_EXECUTABLE", "").strip()
        if not mpi_executable or not Path(mpi_executable).is_file():
            return unavailable("Amber PMEMD MPI executable is not configured")
        completed = run_external(
            executable="mpirun",
            environment_variable="CHEMGRAPH_AMBER_MPIRUN_COMMAND",
            arguments=["--allow-run-as-root", "-np", str(cores), mpi_executable, *arguments],
            directory=directory,
            timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
        )
    (directory / "launcher.stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "launcher.stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Build Amber PMEMD under .software_cache/installations/amber/26.")
    text = mdout.read_text(encoding="utf-8", errors="replace") if mdout.is_file() else ""
    if completed["returncode"] != 0 or "Amber 26 PMEMD" not in text or "Total wall time:" not in text:
        detail = (completed["stderr"] or completed["stdout"] or text)[-4000:]
        raise RuntimeError(f"Amber PMEMD failed or produced incomplete output: {detail}")
    energy = _parse_amber_energy(text)
    if not restart.is_file():
        raise RuntimeError("Amber PMEMD completed without segment.rst7")
    final_system = {
        **system,
        "amber_topology_path": relative_workspace_path(topology),
        "amber_coordinate_path": relative_workspace_path(restart),
        "coordinate_path": relative_workspace_path(restart),
        "has_velocities": action_id == "propagate_dynamics",
    }
    if action_id == "minimize_system_energy":
        result = {
            **final_system,
            "minimized": True,
            "final_potential_energy_kcal_mol": energy,
        }
    else:
        if not trajectory.is_file():
            raise RuntimeError("Amber PMEMD propagation completed without segment.nc")
        result = {
            "trajectory_path": relative_workspace_path(trajectory),
            "final_system": final_system,
            "ensemble": str(settings["ensemble"]).upper(),
            "temperature_kelvin": float(settings["temperature_kelvin"]),
            "pressure_bar": settings.get("pressure_bar"),
            "timestep_fs": float(settings["timestep_fs"]),
            "steps": int(settings["steps"]),
            "duration_ps": float(settings["timestep_fs"]) * int(settings["steps"]) / 1000.0,
            "final_potential_energy_kcal_mol": energy,
        }
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version="26",
        provenance={"command": completed["command"], "parallel_processes": cores, "engine": "PMEMD"},
    )


def _charmm_choice(value: Any, name: str, choices: set[str]) -> str:
    normalized = str(value).strip().lower()
    if normalized not in choices:
        raise ValueError(f"{name} must be one of: {', '.join(sorted(choices))}")
    return normalized


def _render_charmm(
    action_id: str,
    system: dict[str, Any],
    method: dict[str, Any],
    settings: dict[str, Any],
    directory: Path,
) -> str:
    if str(method["force_field_family"]).strip().lower() != "charmm":
        raise ValueError("The CHARMM adapter requires force_field_family='charmm'")
    source_psf = _system_path(system, "charmm_psf_path", "psf_path")
    source_coordinates = _system_path(system, "charmm_coordinate_path", "coordinate_path")
    source_topologies = _system_paths(system, "charmm_topology_paths", "topology_definition_paths")
    source_parameters = _system_paths(system, "charmm_parameter_paths", "parameter_paths")
    psf = directory / "system.psf"
    coordinates = directory / ("coordinates.pdb" if str(method["coordinate_format"]).strip().lower() == "pdb" else "coordinates.crd")
    shutil.copy2(source_psf, psf)
    shutil.copy2(source_coordinates, coordinates)
    topologies = []
    for index, source in enumerate(source_topologies, start=1):
        target = directory / f"topology_{index}.rtf"
        shutil.copy2(source, target)
        topologies.append(target)
    parameters = []
    for index, source in enumerate(source_parameters, start=1):
        target = directory / f"parameter_{index}.prm"
        shutil.copy2(source, target)
        parameters.append(target)
    coordinate_format = _charmm_choice(method["coordinate_format"], "CHARMM coordinate_format", {"card", "pdb"})
    electrostatics = _charmm_choice(method["electrostatics"], "CHARMM electrostatics", {"cdie", "rdie"})
    electrostatic_switch = _charmm_choice(method["electrostatic_switch"], "CHARMM electrostatic_switch", {"fswitch", "fshift"})
    vdw_switch = _charmm_choice(method["vdw_switch"], "CHARMM vdw_switch", {"vswitch", "vshift"})
    constraints = _charmm_choice(method["constraints"], "CHARMM constraints", {"none", "h_bonds"})
    flexible = " flex" if bool(method["flexible_parameters"]) else ""
    lines = ["* ResearchChemBench typed atomic action", "*"]
    lines.append(f'read rtf card name "{topologies[0].name}"')
    lines.extend(f'read rtf card append name "{path.name}"' for path in topologies[1:])
    lines.append(f'read param card{flexible} name "{parameters[0].name}"')
    lines.extend(f'read param card{flexible} append name "{path.name}"' for path in parameters[1:])
    lines.extend(
        [
            f'read psf card name "{psf.name}"',
            f'read coor {coordinate_format} name "{coordinates.name}"',
            (
                f"nbonds atom {electrostatic_switch} {electrostatics} eps {_positive(method['dielectric'], 'CHARMM dielectric'):.12g} "
                f"vdw {vdw_switch} cutnb {_positive(method['pairlist_distance_angstrom'], 'CHARMM pairlist distance'):.12g} "
                f"ctofnb {_positive(method['cutoff_angstrom'], 'CHARMM cutoff'):.12g} "
                f"ctonnb {_positive(method['switch_on_angstrom'], 'CHARMM switch-on distance'):.12g}"
            ),
            "energy",
        ]
    )
    if constraints == "h_bonds":
        lines.append(f"shake bonh parameters tol {_positive(method.get('constraint_tolerance', 1e-8), 'CHARMM constraint tolerance'):.12g}")
    final_crd = "final.crd"
    final_psf = "final.psf"
    if action_id == "minimize_system_energy":
        algorithm = _charmm_choice(settings["algorithm"], "CHARMM minimization algorithm", {"sd", "conj", "abnr"})
        iterations = int(settings["max_iterations"])
        if iterations < 1:
            raise ValueError("CHARMM max_iterations must be positive")
        interval = _interval(settings, iterations)
        tolerance = _positive(settings["gradient_tolerance_kcal_mol_angstrom"], "CHARMM gradient tolerance")
        lines.extend(
            [
                f"mini {algorithm} nstep {iterations} nprint {interval} tolgrad {tolerance:.12g}",
                "energy",
            ]
        )
    elif action_id == "propagate_dynamics":
        steps = int(settings["steps"])
        if steps < 1:
            raise ValueError("CHARMM steps must be positive")
        interval = _interval(settings, steps)
        timestep_ps = _positive(settings["timestep_fs"], "CHARMM timestep_fs") / 1000.0
        temperature = _positive(settings["temperature_kelvin"], "CHARMM temperature_kelvin")
        ensemble = str(settings["ensemble"]).upper()
        if ensemble not in {"NVE", "NVT"}:
            raise ValueError("The configured CHARMM adapter supports NVE and NVT single segments")
        trajectory = "segment.dcd"
        restart_output = "segment.restart"
        lines.extend(
            [
                f'open unit 51 write file name "{trajectory}"',
                f'open unit 31 write card name "{restart_output}"',
            ]
        )
        restart = bool(settings["restart"])
        if restart:
            restart_input = _system_path(system, "charmm_restart_path", "restart_path")
            staged_restart = directory / "restart.in"
            shutil.copy2(restart_input, staged_restart)
            lines.append(f'open unit 30 read card name "{staged_restart.name}"')
        dynamics = [
            f"dynamics leap {'restart' if restart else 'start'} timestep {timestep_ps:.12g} nstep {steps}",
            f"nprint {interval} iprfrq {interval} inbfrq {int(method['nonbond_update_interval'])} ihbfrq 0",
            f"iunrea {30 if restart else -1} iunwri 31 iuncrd 51 iunvel -1 kunit -1",
            f"isvfrq {steps} nsavc {interval} nsavv 0",
        ]
        if not restart:
            dynamics.append(
                f"firstt {temperature:.12g} finalt {temperature:.12g} iasors 1 iasvel 1 iseed {int(settings['random_seed'])}"
            )
        if ensemble == "NVT":
            dynamics.append(
                f"tconst tcoupling {_positive(settings.get('temperature_coupling_ps', 5.0), 'CHARMM temperature coupling'):.12g} treference {temperature:.12g}"
            )
        lines.append(" -\n  ".join(dynamics))
    else:
        raise ValueError(f"CHARMM does not implement {action_id}")
    lines.extend(
        [
            f'write coor card name "{final_crd}"',
            "* ResearchChemBench final coordinates",
            "*",
            f'write psf card name "{final_psf}"',
            "* ResearchChemBench final PSF",
            "*",
            "stop",
            "",
        ]
    )
    return "\n".join(lines)


def _parse_charmm_minimization(text: str) -> tuple[float | None, float | None]:
    matches = re.findall(
        rf"^(?:MINI|ABNR|CONJ)>\s+\d+\s+({_FLOAT})\s+{_FLOAT}\s+({_FLOAT})",
        text,
        flags=re.MULTILINE,
    )
    if not matches:
        return None, None
    energy, gradient = matches[-1]
    return float(energy.replace("D", "E")), float(gradient.replace("D", "E"))


def _parse_charmm_dynamics_energy(text: str) -> float | None:
    matches = re.findall(
        rf"^DYNA>\s+\d+\s+{_FLOAT}\s+{_FLOAT}\s+{_FLOAT}\s+({_FLOAT})",
        text,
        flags=re.MULTILINE,
    )
    return float(matches[-1].replace("D", "E")) if matches else None


def charmm(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    system = _system_mapping(inputs["system"])
    directory = output_directory(action_id, "charmm")
    input_path = directory / "segment.inp"
    input_path.write_text(_render_charmm(action_id, system, method, settings, directory), encoding="utf-8")
    completed = run_external(
        executable="charmm",
        environment_variable="CHEMGRAPH_CHARMM_COMMAND",
        arguments=[],
        directory=directory,
        stdin_text=input_path.read_text(encoding="utf-8"),
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    output_path = directory / "segment.out"
    output_path.write_text(completed["stdout"], encoding="utf-8")
    (directory / "segment.err").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Build licensed CHARMM under .software_cache/installations/charmm/50b2.")
    if completed["returncode"] != 0 or "NORMAL TERMINATION BY NORMAL STOP" not in completed["stdout"]:
        detail = (completed["stderr"] or completed["stdout"])[-4000:]
        raise RuntimeError(f"CHARMM failed or did not terminate normally: {detail}")
    version_match = re.search(r"Stable Version\s+([^\s]+)", completed["stdout"])
    version = version_match.group(1) if version_match else None
    final_crd = directory / "final.crd"
    final_psf = directory / "final.psf"
    if not final_crd.is_file() or not final_psf.is_file():
        raise RuntimeError("CHARMM completed without final coordinate/PSF files")
    final_system = {
        **system,
        "charmm_coordinate_path": relative_workspace_path(final_crd),
        "coordinate_path": relative_workspace_path(final_crd),
        "charmm_psf_path": relative_workspace_path(final_psf),
        "psf_path": relative_workspace_path(final_psf),
    }
    if action_id == "minimize_system_energy":
        energy, gradient = _parse_charmm_minimization(completed["stdout"])
        tolerance = float(settings["gradient_tolerance_kcal_mol_angstrom"])
        converged = gradient is not None and gradient <= tolerance
        result = {
            **final_system,
            "minimized": converged,
            "final_energy_kcal_mol": energy,
            "final_gradient_kcal_mol_angstrom": gradient,
        }
        if not converged:
            return partial_success(
                result,
                artifact_files=command_artifacts(directory),
                backend_version=version,
                provenance={"command": completed["command"]},
                warnings=["CHARMM completed, but the requested minimization gradient tolerance was not reached."],
            )
    elif action_id == "propagate_dynamics":
        trajectory = directory / "segment.dcd"
        restart = directory / "segment.restart"
        if not trajectory.is_file() or not restart.is_file():
            raise RuntimeError("CHARMM propagation completed without trajectory/restart files")
        final_system["charmm_restart_path"] = relative_workspace_path(restart)
        result = {
            "trajectory_path": relative_workspace_path(trajectory),
            "final_system": final_system,
            "ensemble": str(settings["ensemble"]).upper(),
            "temperature_kelvin": float(settings["temperature_kelvin"]),
            "timestep_fs": float(settings["timestep_fs"]),
            "steps": int(settings["steps"]),
            "duration_ps": float(settings["timestep_fs"]) * int(settings["steps"]) / 1000.0,
            "final_energy_kcal_mol": _parse_charmm_dynamics_energy(completed["stdout"]),
        }
    else:
        return unsupported(f"CHARMM does not implement {action_id}")
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=version,
        provenance={"command": completed["command"]},
    )

"""Periodic electronic-structure and lattice-dynamics actions."""

from __future__ import annotations

import math
import os
import re
import shutil
from pathlib import Path
from typing import Any

from ..resources import is_resource_reference, resource_reference_metadata
from .common import (
    ase_atoms,
    atoms_and_coordinates,
    command_artifacts,
    module_version,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_command,
    resolve_input_file,
    run_external,
    structure_dict,
    structure_from_atoms,
    success,
    unavailable,
    unwrap_artifact,
    unsupported,
    write_json,
)
from .mlip import build_calculator as build_mlip_calculator
from .mlip import prepare_atoms as prepare_mlip_atoms


ACTIONS = {
    "calculate_quasiparticle_corrections", "calculate_bse_optical_spectrum",
    "generate_crystal_structure_candidates", "convert_crystal_structure_format",
    "generate_vasp_kpoint_mesh", "extract_vasp_band_gap",
    "calculate_adsorption_energy", "construct_pressure_enthalpy_phase_diagram",
    "assess_phonon_stability",
    "fit_effective_force_constants", "generate_thermal_displacement_configurations",
    "calculate_temperature_dependent_phonon_dispersion",
    "calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress",
    "relax_periodic_structure", "generate_displaced_supercells",
    "assemble_force_constants", "calculate_phonon_dispersion",
    "calculate_phonon_density_of_states",
    "calculate_harmonic_thermodynamics", "calculate_phonon_group_velocities",
    "calculate_lattice_thermal_conductivity",
    "calculate_electronic_band_structure", "calculate_density_of_states",
    "calculate_projected_density_of_states", "analyze_periodic_bonding",
    "calculate_charge_spilling",
}


def _run_yambo(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    directory = output_directory(action_id, "yambo")
    save_source = resolve_input_file(inputs["save_directory"])
    if not save_source.is_dir():
        raise ValueError("save_directory must be an existing Yambo SAVE directory")
    shutil.copytree(save_source, directory / "SAVE")
    input_source = resolve_input_file(inputs["input_file"])
    input_name = input_source.name
    shutil.copy2(input_source, directory / input_name)
    for value in unwrap_artifact(inputs.get("restart_directories", [])):
        source = resolve_input_file(value)
        if not source.is_dir():
            raise ValueError("each restart_directories item must be a directory")
        shutil.copytree(source, directory / source.name)

    job_name = str(settings["job_name"]).strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+(?:,[A-Za-z0-9_.-]+)*", job_name):
        raise ValueError("job_name must be a comma-separated list of safe Yambo job names")
    timeout = int(request.get("resource_limits", {}).get("walltime_seconds", 7200))
    completed = run_external(
        executable="yambo",
        environment_variable="CHEMGRAPH_YAMBO_COMMAND",
        arguments=["-F", input_name, "-J", job_name],
        directory=directory,
        timeout_seconds=timeout,
        environment_overrides={
            "OMP_NUM_THREADS": str(int(request.get("resource_limits", {}).get("cpu_cores", 1))),
            "OPENBLAS_NUM_THREADS": "1",
            "OMPI_MCA_pml": "ob1",
            "OMPI_MCA_btl": "self,vader,tcp",
        },
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Install Yambo 5.3 or later")
    if completed["returncode"] != 0:
        raise RuntimeError(f"Yambo failed: {completed['stderr'][-2000:]}")
    reports = list(directory.glob("r-*"))
    normal_exit = any("Game Over" in path.read_text(encoding="utf-8", errors="replace") for path in reports)
    if bool(settings["require_normal_exit"]) and not normal_exit:
        raise RuntimeError("Yambo completed without a Game Over marker")

    limit = int(settings["maximum_returned_records"])
    if not 1 <= limit <= 100000:
        raise ValueError("maximum_returned_records must be between 1 and 100000")
    if action_id == "calculate_quasiparticle_corrections":
        files = sorted(directory.glob("o-*.qp"))
        if not files:
            raise RuntimeError("Yambo produced no quasiparticle output (o-*.qp)")
        records = []
        for line in files[0].read_text(encoding="utf-8", errors="replace").splitlines():
            fields = line.split()
            if len(fields) < 5 or line.lstrip().startswith("#"):
                continue
            try:
                kpoint, band = int(fields[0]), int(fields[1])
                energy, correction, self_energy = map(float, fields[2:5])
            except ValueError:
                continue
            records.append({
                "kpoint_index": kpoint,
                "band_index": band,
                "reference_energy_ev": energy,
                "quasiparticle_correction_ev": correction,
                "quasiparticle_energy_ev": energy + correction,
                "self_energy_at_reference_ev": self_energy,
            })
        result = {"state_count": len(records), "states": records[:limit], "normal_exit": normal_exit}
    else:
        files = sorted(directory.glob("o-*.eps*"))
        if not files:
            raise RuntimeError("Yambo produced no BSE dielectric spectrum (o-*.eps*)")
        points = []
        for line in files[0].read_text(encoding="utf-8", errors="replace").splitlines():
            fields = line.split()
            if len(fields) < 3 or line.lstrip().startswith("#"):
                continue
            try:
                values = [float(value) for value in fields]
            except ValueError:
                continue
            points.append({"energy_ev": values[0], "epsilon_2": values[1], "epsilon_1": values[2]})
        result = {"point_count": len(points), "spectrum": points[:limit], "normal_exit": normal_exit}
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version="5.3.0",
        provenance={"command": completed["command"], "native_input_preserved": True},
    )


_ELEMENTS = (
    "X H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn "
    "Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr "
    "Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra "
    "Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og"
).split()
_ATOMIC_NUMBER = {symbol: index for index, symbol in enumerate(_ELEMENTS) if index}
_BOHR_TO_ANGSTROM = 0.529177210903
_AIRSS_FORMATS = {"cell", "res", "shx", "cif", "xtl", "xyz"}


def _finite_energy(value: Any, field: str) -> float:
    item = unwrap_artifact(value)
    if isinstance(item, dict):
        for key in ("energy", "energy_hartree", "energy_ev", "value"):
            if key in item:
                item = item[key]
                break
    try:
        result = float(item)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must contain one numeric energy") from exc
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _calculate_adsorption_energy(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    unit = str(settings["energy_unit"]).strip().lower()
    factors = {
        "hartree": 27.211386245988,
        "ev": 1.0,
        "kj/mol": 1.0 / 96.4853321233,
        "kcal/mol": 1.0 / 23.0605478306,
    }
    adsorbate_count = float(settings["adsorbate_count"])
    if not math.isfinite(adsorbate_count) or adsorbate_count <= 0:
        raise ValueError("adsorbate_count must be finite and positive")
    adsorbed = _finite_energy(inputs["adsorbed_system_energy"], "adsorbed_system_energy")
    clean = _finite_energy(inputs["clean_surface_energy"], "clean_surface_energy")
    references = unwrap_artifact(inputs["reference_species"])
    if not isinstance(references, list) or not references:
        raise ValueError("reference_species must be a non-empty list")
    normalized_references = []
    reference_total = 0.0
    for index, record in enumerate(references):
        if not isinstance(record, dict) or "energy" not in record or "stoichiometric_coefficient" not in record:
            raise ValueError("each reference_species record requires energy and stoichiometric_coefficient")
        coefficient = float(record["stoichiometric_coefficient"])
        energy = _finite_energy(record["energy"], f"reference_species[{index}].energy")
        if not math.isfinite(coefficient):
            raise ValueError("reference-species coefficients must be finite")
        reference_total += coefficient * energy
        normalized_references.append(
            {
                "label": str(record.get("label", index)),
                "energy": energy,
                "stoichiometric_coefficient": coefficient,
                "weighted_energy": coefficient * energy,
            }
        )
    adsorption_input = (adsorbed - clean - reference_total) / adsorbate_count
    return success(
        {
            "adsorption_energy": adsorption_input,
            "adsorption_energy_ev": adsorption_input * factors[unit],
            "energy_unit": unit,
            "sign_convention": "E(adsorbed system) - E(clean surface) - sum(nu_i E(reference_i)), divided by adsorbate_count",
            "adsorbate_count": adsorbate_count,
            "components": {
                "adsorbed_system_energy": adsorbed,
                "clean_surface_energy": clean,
                "reference_species": normalized_references,
            },
        }
    )


def _construct_pressure_enthalpy_phase_diagram(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    records = unwrap_artifact(inputs["phase_records"])
    if not isinstance(records, list) or not records:
        raise ValueError("phase_records must be a non-empty list")
    unit = str(settings["enthalpy_unit"]).strip().lower()
    factors = {
        "ev_per_formula_unit": 1.0,
        "hartree_per_formula_unit": 27.211386245988,
        "kj/mol": 1.0 / 96.4853321233,
    }
    tolerance = float(settings["energy_tolerance_ev_per_formula_unit"])
    maximum_transitions = int(settings["maximum_reported_transitions"])
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("energy_tolerance_ev_per_formula_unit must be finite and nonnegative")
    if not 1 <= maximum_transitions <= 10000:
        raise ValueError("maximum_reported_transitions must be between 1 and 10000")
    by_phase: dict[str, dict[float, float]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each phase record must be a mapping")
        phase = str(record.get("phase_id", "")).strip()
        pressure = float(record.get("pressure_gpa"))
        enthalpy = float(record.get("enthalpy")) * factors[unit]
        if not phase or not math.isfinite(pressure) or not math.isfinite(enthalpy):
            raise ValueError("phase_id, pressure_gpa, and enthalpy must be non-empty and finite")
        if pressure in by_phase.setdefault(phase, {}):
            raise ValueError(f"duplicate pressure point for phase {phase}")
        by_phase[phase][pressure] = enthalpy
    if len(by_phase) < 2:
        raise ValueError("at least two phases are required")
    pressure_grid = sorted(next(iter(by_phase.values())))
    if len(pressure_grid) < 2 or any(sorted(values) != pressure_grid for values in by_phase.values()):
        raise ValueError("every phase must use the same pressure grid with at least two points")
    stable_records = []
    for pressure in pressure_grid:
        energies = {phase: values[pressure] for phase, values in by_phase.items()}
        minimum = min(energies.values())
        stable = sorted(phase for phase, value in energies.items() if value - minimum <= tolerance)
        stable_records.append(
            {
                "pressure_gpa": pressure,
                "stable_phases": stable,
                "minimum_enthalpy_ev_per_formula_unit": minimum,
                "relative_enthalpies_ev_per_formula_unit": {
                    phase: value - minimum for phase, value in sorted(energies.items())
                },
            }
        )
    transitions = []
    primary = [record["stable_phases"][0] for record in stable_records]
    for index, (left_phase, right_phase) in enumerate(zip(primary, primary[1:])):
        if left_phase == right_phase:
            continue
        p0, p1 = pressure_grid[index : index + 2]
        d0 = by_phase[left_phase][p0] - by_phase[right_phase][p0]
        d1 = by_phase[left_phase][p1] - by_phase[right_phase][p1]
        crossing = p0 - d0 * (p1 - p0) / (d1 - d0) if d1 != d0 else (p0 + p1) / 2
        transitions.append(
            {
                "from_phase": left_phase,
                "to_phase": right_phase,
                "bracket_gpa": [p0, p1],
                "interpolated_transition_pressure_gpa": crossing,
                "interpolation": "linear_enthalpy_difference",
            }
        )
    return success(
        {
            "phase_count": len(by_phase),
            "pressure_grid_gpa": pressure_grid,
            "stable_phase_records": stable_records,
            "transitions": transitions[:maximum_transitions],
            "transition_count": len(transitions),
            "transitions_truncated": len(transitions) > maximum_transitions,
            "energy_tolerance_ev_per_formula_unit": tolerance,
        }
    )


def _assess_phonon_stability(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    records = unwrap_artifact(inputs["phonon_records"])
    if not isinstance(records, list) or not records:
        raise ValueError("phonon_records must be a non-empty list")
    unit = str(settings["frequency_unit"]).strip().lower()
    factors = {"thz": 1.0, "cm-1": 1.0 / 33.3564095198, "mev": 1.0 / 4.135667696}
    imaginary_tolerance = float(settings["imaginary_tolerance"]) * factors[unit]
    gamma_q_tolerance = float(settings["gamma_q_tolerance"])
    acoustic_tolerance = float(settings["acoustic_gamma_tolerance"]) * factors[unit]
    maximum_modes = int(settings["maximum_returned_imaginary_modes"])
    if min(imaginary_tolerance, gamma_q_tolerance, acoustic_tolerance) < 0:
        raise ValueError("phonon tolerances must be nonnegative")
    if not 1 <= maximum_modes <= 100000:
        raise ValueError("maximum_returned_imaginary_modes must be between 1 and 100000")
    imaginary = []
    all_frequencies = []
    gamma_frequencies = None
    for q_index, record in enumerate(records):
        if not isinstance(record, dict) or not isinstance(record.get("q_point"), (list, tuple)) or len(record["q_point"]) != 3:
            raise ValueError("each phonon record requires a three-component q_point")
        q_point = [float(value) for value in record["q_point"]]
        frequencies = [float(value) * factors[unit] for value in record.get("frequencies", [])]
        if not frequencies or not all(math.isfinite(value) for value in [*q_point, *frequencies]):
            raise ValueError("each phonon record requires finite non-empty frequencies")
        all_frequencies.extend(frequencies)
        if math.sqrt(sum(value * value for value in q_point)) <= gamma_q_tolerance:
            gamma_frequencies = frequencies
        for mode_index, frequency in enumerate(frequencies):
            if frequency < -imaginary_tolerance:
                imaginary.append(
                    {"q_index": q_index, "q_point": q_point, "mode_index": mode_index, "frequency_thz": frequency}
                )
    if gamma_frequencies is None:
        raise ValueError("phonon_records contains no Gamma point within gamma_q_tolerance")
    acoustic = sorted(gamma_frequencies, key=abs)[:3]
    acoustic_ok = len(acoustic) == 3 and all(abs(value) <= acoustic_tolerance for value in acoustic)
    return success(
        {
            "dynamically_stable": not imaginary,
            "imaginary_mode_count": len(imaginary),
            "imaginary_modes": imaginary[:maximum_modes],
            "imaginary_modes_truncated": len(imaginary) > maximum_modes,
            "minimum_frequency_thz": min(all_frequencies),
            "gamma_acoustic_frequencies_thz": acoustic,
            "gamma_acoustic_modes_within_tolerance": acoustic_ok,
            "frequency_count": len(all_frequencies),
            "tolerances": {
                "imaginary_frequency_thz": imaginary_tolerance,
                "gamma_q_norm": gamma_q_tolerance,
                "acoustic_gamma_thz": acoustic_tolerance,
            },
        }
    )


def _vaspkit_home(directory: Path, replacements: dict[str, str] | None = None) -> Path:
    configured = os.environ.get("CHEMGRAPH_VASPKIT_CONFIG", "").strip()
    if not configured or not Path(configured).is_file():
        raise RuntimeError("CHEMGRAPH_VASPKIT_CONFIG must point to the pinned VASPKIT configuration template")
    home = directory / "home"
    home.mkdir()
    text = Path(configured).read_text(encoding="utf-8", errors="strict")
    for name, value in (replacements or {}).items():
        pattern = rf"(?m)^({re.escape(name)}\s*=\s*)[^#\n]+"
        text, count = re.subn(pattern, rf"\g<1>{value} ", text, count=1)
        if count != 1:
            raise RuntimeError(f"VASPKIT configuration does not define {name}")
    (home / ".vaspkit").write_text(text, encoding="utf-8")
    return home


def _run_vaspkit_action(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    directory = output_directory(action_id, "vaspkit")
    timeout_seconds = int((request.get("resource_limits") or {}).get("walltime_seconds", 1800))

    if action_id == "generate_vasp_kpoint_mesh":
        resolution = float(settings["reciprocal_space_resolution_inverse_angstrom"])
        if not 0 < resolution <= 2:
            raise ValueError("reciprocal_space_resolution_inverse_angstrom must be in (0, 2]")
        scheme = str(settings["centering_scheme"]).strip().lower().replace("_", "-")
        flags = {"gamma": "G", "monkhorst-pack": "M"}
        if scheme not in flags:
            raise ValueError("centering_scheme must be gamma or monkhorst-pack")
        shutil.copy2(resolve_input_file(inputs["structure_file"]), directory / "POSCAR")
        home = _vaspkit_home(directory)
        completed = run_external(
            executable="vaspkit",
            environment_variable="CHEMGRAPH_VASPKIT_COMMAND",
            arguments=["-task", "102", "-file", "POSCAR", "-kpr", str(resolution), "-kps", flags[scheme]],
            directory=directory,
            timeout_seconds=max(1, timeout_seconds),
            environment_overrides={"HOME": str(home)},
        )
        (directory / "vaspkit.log").write_text(completed["stdout"] + completed["stderr"], encoding="utf-8")
        if not completed["available"]:
            return unavailable(completed["stderr"], install="Download VASPKIT 1.5.1 from the official SourceForge release.")
        output = directory / "KPOINTS"
        if completed["returncode"] != 0 or not output.is_file() or "Written KPOINTS File" not in completed["stdout"]:
            raise RuntimeError(f"VASPKIT did not generate KPOINTS: {(completed['stderr'] or completed['stdout'])[-2000:]}")
        lines = output.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) < 5:
            raise RuntimeError("VASPKIT generated an incomplete KPOINTS file")
        try:
            grid = [int(value) for value in lines[3].split()[:3]]
            shift = [float(value) for value in lines[4].split()[:3]]
        except ValueError as exc:
            raise RuntimeError("Could not parse VASPKIT KPOINTS grid") from exc
        return success(
            {
                "kpoint_file": relative_workspace_path(output),
                "grid": grid,
                "shift": shift,
                "centering_scheme": scheme,
                "reciprocal_space_resolution_inverse_angstrom": resolution,
                "potcar_generated": False,
            },
            artifact_files=command_artifacts(directory), backend_version="1.5.1",
            provenance={"command": completed["command"], "task": 102},
        )

    staged = {
        "structure_file": "POSCAR", "incar_file": "INCAR",
        "eigenvalue_file": "EIGENVAL", "dos_file": "DOSCAR",
        "outcar_file": "OUTCAR",
    }
    for key, name in staged.items():
        if inputs.get(key) is not None:
            shutil.copy2(resolve_input_file(inputs[key]), directory / name)
    zero = ".TRUE." if bool(settings["set_fermi_energy_zero"]) else ".FALSE."
    home = _vaspkit_home(directory, {"SET_FERMI_ENERGY_ZERO": zero})
    completed = run_external(
        executable="vaspkit", environment_variable="CHEMGRAPH_VASPKIT_COMMAND",
        arguments=["-task", "911", "-file", "POSCAR"], directory=directory,
        timeout_seconds=max(1, timeout_seconds), environment_overrides={"HOME": str(home)},
    )
    (directory / "vaspkit.log").write_text(completed["stdout"] + completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Download VASPKIT 1.5.1 from the official SourceForge release.")
    if completed["returncode"] != 0 or "Band Gap (eV)" not in completed["stdout"]:
        raise RuntimeError(f"VASPKIT band-gap extraction failed: {(completed['stderr'] or completed['stdout'])[-2000:]}")
    text = completed["stdout"]
    def match(pattern: str, label: str) -> re.Match[str]:
        found = re.search(pattern, text)
        if found is None:
            raise RuntimeError(f"Could not parse {label} from VASPKIT output")
        return found
    character = match(r"Band Character:\s+(\S+)", "band character").group(1)
    gap = float(match(r"Band Gap \(eV\):\s+([-+0-9.Ee]+)", "band gap").group(1))
    vbm = float(match(r"Eigenvalue of VBM \(eV\):\s+([-+0-9.Ee]+)", "VBM").group(1))
    cbm = float(match(r"Eigenvalue of CBM \(eV\):\s+([-+0-9.Ee]+)", "CBM").group(1))
    fermi = float(match(r"Fermi Energy \(eV\):\s+([-+0-9.Ee]+)", "Fermi energy").group(1))
    bands = [int(value) for value in match(r"Band Indexes of VBM & CBM:\s+(\d+)\s+(\d+)", "band indices").groups()]
    kpoints = [int(value) for value in match(r"Kpt Indexes of VBM & CBM:\s+(\d+)\s+(\d+)", "k-point indices").groups()]
    vbm_kpoint = [float(value) for value in match(r"Location of VBM \(frac\.\):\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)", "VBM k-point").groups()]
    cbm_kpoint = [float(value) for value in match(r"Location of CBM \(frac\.\):\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)", "CBM k-point").groups()]
    return success(
        {
            "band_character": character.lower(), "band_gap_ev": gap,
            "vbm_ev": vbm, "cbm_ev": cbm, "fermi_energy_ev": fermi,
            "vbm_band_index": bands[0], "cbm_band_index": bands[1],
            "vbm_kpoint_index": kpoints[0], "cbm_kpoint_index": kpoints[1],
            "vbm_fractional_kpoint": vbm_kpoint, "cbm_fractional_kpoint": cbm_kpoint,
            "fermi_energy_shifted_to_zero": bool(settings["set_fermi_energy_zero"]),
        },
        artifact_files=command_artifacts(directory), backend_version="1.5.1",
        provenance={"command": completed["command"], "task": 911},
    )


def _parse_airss_cell(text: str) -> dict[str, Any]:
    import io
    import warnings

    from ase.io import read

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        atoms = read(io.StringIO(text), format="castep-cell")
    return structure_from_atoms(atoms)


def _run_airss(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    directory = output_directory(action_id, "airss")
    timeout_seconds = int(
        request.get("resource_limits", {}).get("walltime_seconds", 7200)
    )

    if action_id == "generate_crystal_structure_candidates":
        seed_path = resolve_input_file(inputs["seed_file"])
        seed_text = seed_path.read_text(encoding="utf-8", errors="replace")
        candidate_count = int(settings["candidate_count"])
        if not 1 <= candidate_count <= 1000:
            raise ValueError("candidate_count must be between 1 and 1000")
        (directory / "seed.cell").write_text(seed_text, encoding="utf-8")
        candidates = []
        commands = []
        for index in range(1, candidate_count + 1):
            completed = run_external(
                executable="buildcell",
                environment_variable="CHEMGRAPH_AIRSS_BUILDCELL_COMMAND",
                arguments=[],
                directory=directory,
                stdin_text=seed_text,
                timeout_seconds=timeout_seconds,
            )
            if not completed["available"]:
                return unavailable(
                    completed["stderr"],
                    install="conda install -c conda-forge airss-with-default-names=0.9.3",
                )
            if completed["returncode"] != 0:
                raise RuntimeError(
                    f"AIRSS buildcell failed for candidate {index}: "
                    f"{completed['stderr'][-2000:]}"
                )
            cell_text = completed["stdout"].replace("\x00", "")
            candidate_path = directory / f"candidate_{index:04d}.cell"
            candidate_path.write_text(cell_text, encoding="utf-8")
            candidates.append(
                {
                    "candidate_id": f"airss-{index:04d}",
                    "structure": _parse_airss_cell(cell_text),
                    "structure_file": relative_workspace_path(candidate_path),
                }
            )
            commands.append(completed["command"])
        return success(
            {
                "candidate_count": len(candidates),
                "candidates": candidates,
                "relaxed": False,
                "ranked": False,
            },
            artifact_files=command_artifacts(directory),
            backend_version="0.9.3",
            provenance={
                "commands": commands,
                "seed_file": relative_workspace_path(directory / "seed.cell"),
                "automatic_relaxation": False,
                "automatic_ranking": False,
            },
        )

    input_format = str(settings["input_format"]).strip().lower()
    output_format = str(settings["output_format"]).strip().lower()
    if input_format not in _AIRSS_FORMATS or output_format not in _AIRSS_FORMATS:
        raise ValueError(
            "input_format and output_format must each be one of "
            f"{sorted(_AIRSS_FORMATS)}"
        )
    source = resolve_input_file(inputs["structure_file"])
    source_text = source.read_text(encoding="utf-8", errors="replace")
    staged_input = directory / f"input.{input_format}"
    staged_input.write_text(source_text, encoding="utf-8")
    completed = run_external(
        executable="cabal",
        environment_variable="CHEMGRAPH_AIRSS_CABAL_COMMAND",
        arguments=[input_format, output_format],
        directory=directory,
        stdin_text=source_text,
        timeout_seconds=timeout_seconds,
    )
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install="conda install -c conda-forge airss-with-default-names=0.9.3",
        )
    if completed["returncode"] != 0:
        raise RuntimeError(f"AIRSS cabal failed: {completed['stderr'][-2000:]}")
    output_text = completed["stdout"].replace("\x00", "")
    output_path = directory / f"converted.{output_format}"
    output_path.write_text(output_text, encoding="utf-8")
    return success(
        {
            "structure_file": relative_workspace_path(output_path),
            "input_format": input_format,
            "output_format": output_format,
        },
        artifact_files=command_artifacts(directory),
        backend_version="0.9.3",
        provenance={"command": completed["command"]},
    )


def _stage_tdep_file(value: Any, directory: Path, target_name: str) -> Path:
    source = resolve_input_file(value)
    target = directory / target_name
    shutil.copy2(source, target)
    return target


def _run_tdep(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, _method, settings = request_parts(request)
    directory = output_directory(action_id, "tdep")
    timeout_seconds = int(
        request.get("resource_limits", {}).get("walltime_seconds", 7200)
    )
    _stage_tdep_file(inputs["unit_cell_file"], directory, "infile.ucposcar")

    if action_id == "fit_effective_force_constants":
        _stage_tdep_file(inputs["supercell_file"], directory, "infile.ssposcar")
        _stage_tdep_file(inputs["simulation_file"], directory, "infile.sim.hdf5")
        arguments = ["-rc2", str(float(settings["second_order_cutoff_angstrom"]))]
        third_cutoff = settings["third_order_cutoff_angstrom"]
        fourth_cutoff = settings["fourth_order_cutoff_angstrom"]
        if third_cutoff is not None:
            arguments.extend(["-rc3", str(float(third_cutoff))])
        if fourth_cutoff is not None:
            arguments.extend(["-rc4", str(float(fourth_cutoff))])
        if bool(settings["polar"]):
            if "loto_splitting_file" not in inputs:
                raise ValueError("polar=true requires inputs.loto_splitting_file")
            _stage_tdep_file(
                inputs["loto_splitting_file"], directory, "infile.lotosplitting"
            )
            arguments.append("--polar")
        stride = int(settings["configuration_stride"])
        if stride < 1:
            raise ValueError("configuration_stride must be at least 1")
        arguments.extend(["--stride", str(stride)])
        if bool(settings["include_first_order"]):
            arguments.append("--firstorder")
        temperature = settings["self_consistent_temperature_kelvin"]
        if temperature is not None:
            arguments.extend(["--temperature", str(float(temperature))])
        if not bool(settings["enforce_rotational_invariance"]):
            arguments.append("--norotational")
        if not bool(settings["enforce_huang_invariance"]):
            arguments.append("--nohuang")
        if not bool(settings["enforce_hermitian_symmetry"]):
            arguments.append("--nohermitian")
        executable = "extract_forceconstants"
        variable = "CHEMGRAPH_TDEP_EXTRACT_FORCECONSTANTS_COMMAND"
    elif action_id == "generate_thermal_displacement_configurations":
        _stage_tdep_file(inputs["supercell_file"], directory, "infile.ssposcar")
        source = str(settings["initialization_source"])
        arguments = [
            "--nconf", str(int(settings["configuration_count"])),
            "--temperature", str(float(settings["temperature_kelvin"])),
        ]
        count = int(settings["configuration_count"])
        if not 1 <= count <= 10000:
            raise ValueError("configuration_count must be between 1 and 10000")
        if source == "force_constants":
            if "second_order_force_constants_file" not in inputs:
                raise ValueError(
                    "initialization_source=force_constants requires "
                    "inputs.second_order_force_constants_file"
                )
            _stage_tdep_file(
                inputs["second_order_force_constants_file"],
                directory,
                "infile.forceconstant",
            )
        elif source == "debye_temperature":
            value = settings["debye_temperature_kelvin"]
            if value is None or float(value) <= 0:
                raise ValueError("debye_temperature_kelvin must be positive")
            arguments.extend(["--debye_temperature", str(float(value))])
        elif source == "maximum_frequency":
            value = settings["maximum_frequency_thz"]
            if value is None or float(value) <= 0:
                raise ValueError("maximum_frequency_thz must be positive")
            arguments.extend(["--maximum_frequency", str(float(value))])
        else:
            raise ValueError(
                "initialization_source must be force_constants, debye_temperature, "
                "or maximum_frequency"
            )
        if str(settings["statistics"]) == "quantum":
            arguments.append("--quantum")
        output_formats = {"vasp": 1, "abinit": 2, "fhi_aims": 4, "siesta": 5}
        output_format = str(settings["output_format"])
        arguments.extend(["--output_format", str(output_formats[output_format])])
        minimum_distance = settings["minimum_distance_ratio"]
        if minimum_distance is not None:
            arguments.extend(["--mindist", str(float(minimum_distance))])
        executable = "canonical_configuration"
        variable = "CHEMGRAPH_TDEP_CANONICAL_CONFIGURATION_COMMAND"
    else:
        _stage_tdep_file(
            inputs["second_order_force_constants_file"],
            directory,
            "infile.forceconstant",
        )
        arguments = [
            "--unit", str(settings["frequency_unit"]),
            "--nq_on_path", str(int(settings["points_per_segment"])),
        ]
        if "q_path_file" in inputs:
            _stage_tdep_file(
                inputs["q_path_file"], directory, "infile.qpoints_dispersion"
            )
            arguments.append("--readpath")
        if bool(settings["calculate_gruneisen"]):
            if "third_order_force_constants_file" not in inputs:
                raise ValueError(
                    "calculate_gruneisen=true requires "
                    "inputs.third_order_force_constants_file"
                )
            _stage_tdep_file(
                inputs["third_order_force_constants_file"],
                directory,
                "infile.forceconstant_thirdorder",
            )
            arguments.append("--gruneisen")
        executable = "phonon_dispersion_relations"
        variable = "CHEMGRAPH_TDEP_PHONON_DISPERSION_COMMAND"

    completed = run_external(
        executable=executable,
        environment_variable=variable,
        arguments=arguments,
        directory=directory,
        timeout_seconds=timeout_seconds,
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install="Build TDEP 25.03 from https://github.com/tdep-developers/tdep",
        )
    if completed["returncode"] != 0:
        raise RuntimeError(f"TDEP {executable} failed: {completed['stderr'][-2000:]}")

    artifacts = command_artifacts(directory)
    common = {
        "artifact_files": artifacts,
        "backend_version": "25.03-d38f435",
        "provenance": {"command": completed["command"]},
    }
    if action_id == "fit_effective_force_constants":
        fc2 = directory / "outfile.forceconstant"
        fc3 = directory / "outfile.forceconstant_thirdorder"
        fc4 = directory / "outfile.forceconstant_fourthorder"
        if not fc2.is_file():
            raise RuntimeError("TDEP completed without outfile.forceconstant")
        r_squared = None
        match = re.search(
            r"second order:\s+([0-9.]+)\s+[0-9.]+", completed["stdout"]
        )
        if match:
            r_squared = float(match.group(1))
        return success(
            {
                "second_order_force_constants_file": relative_workspace_path(fc2),
                "third_order_force_constants_file": (
                    relative_workspace_path(fc3) if fc3.is_file() else None
                ),
                "fourth_order_force_constants_file": (
                    relative_workspace_path(fc4) if fc4.is_file() else None
                ),
                "cross_validation_r_squared": r_squared,
                "polar": bool(settings["polar"]),
            },
            **common,
        )
    if action_id == "generate_thermal_displacement_configurations":
        files = sorted(directory.glob("contcar_conf*"))
        if len(files) != int(settings["configuration_count"]):
            raise RuntimeError(
                "TDEP produced an unexpected number of thermal configurations"
            )
        configurations = []
        for index, path in enumerate(files, 1):
            item = {
                "configuration_id": f"tdep-{index:04d}",
                "structure_file": relative_workspace_path(path),
            }
            if str(settings["output_format"]) == "vasp":
                from ase.io import read

                item["structure"] = structure_from_atoms(read(str(path), format="vasp"))
            configurations.append(item)
        return success(
            {
                "configuration_count": len(configurations),
                "temperature_kelvin": float(settings["temperature_kelvin"]),
                "statistics": str(settings["statistics"]),
                "configurations": configurations,
            },
            **common,
        )
    dispersion_path = directory / "outfile.dispersion_relations"
    if not dispersion_path.is_file():
        raise RuntimeError("TDEP completed without outfile.dispersion_relations")
    values = np.loadtxt(dispersion_path, dtype=float)
    return success(
        {
            "path_coordinate": values[:, 0].tolist(),
            "frequencies": values[:, 1:].tolist(),
            "frequency_unit": str(settings["frequency_unit"]),
            "points_per_segment": int(settings["points_per_segment"]),
            "dispersion_file": relative_workspace_path(dispersion_path),
            "hdf5_file": relative_workspace_path(
                directory / "outfile.dispersion_relations.hdf5"
            ),
        },
        **common,
    )


def _periodic_structure(value: Any) -> tuple[dict[str, Any], list[str], list[list[float]], list[list[float]]]:
    structure = structure_dict(value)
    symbols, coordinates = atoms_and_coordinates(structure)
    cell = structure.get("cell_angstrom") or structure.get("cell")
    if cell is None or len(cell) != 3 or any(len(row) != 3 for row in cell):
        raise ValueError("Periodic structure requires a 3x3 cell_angstrom")
    if not all(bool(value) for value in structure.get("pbc", [True, True, True])):
        raise ValueError("Periodic actions require PBC in all three dimensions")
    return structure, symbols, coordinates, [[float(value) for value in row] for row in cell]


def _k_points(value: Any) -> tuple[int, int, int, int, int, int]:
    if isinstance(value, dict):
        grid = value.get("grid")
        shift = value.get("shift", [0, 0, 0])
    else:
        grid = value
        shift = [0, 0, 0]
    if not isinstance(grid, (list, tuple)) or len(grid) != 3:
        raise ValueError("k_points requires grid=[nx,ny,nz]")
    if not isinstance(shift, (list, tuple)) or len(shift) != 3:
        raise ValueError("k_points shift must contain three integers")
    return (*[int(item) for item in grid], *[int(item) for item in shift])


def _copy_pseudopotentials(mapping: dict[str, Any], directory: Path) -> tuple[dict[str, str], Path]:
    pseudo_dir = directory / "pseudopotentials"
    pseudo_dir.mkdir()
    names = {}
    for element, value in mapping.items():
        source = resolve_input_file(value)
        destination = pseudo_dir / source.name
        shutil.copy2(source, destination)
        names[str(element)] = destination.name
    return names, pseudo_dir


def _structure_payload(
    symbols: list[str],
    coordinates: list[list[float]],
    cell: list[list[float]],
    original: dict[str, Any],
) -> dict[str, Any]:
    return {
        "atoms": [
            {"element": symbol, "position_angstrom": [float(value) for value in row]}
            for symbol, row in zip(symbols, coordinates)
        ],
        "cell_angstrom": [[float(value) for value in row] for row in cell],
        "pbc": [True, True, True],
        "charge": int(original.get("charge", 0)),
        "multiplicity": int(original.get("multiplicity", 1)),
    }


def _numeric_tokens(text: str) -> list[float]:
    return [
        float(value.replace("D", "E").replace("d", "e"))
        for value in re.findall(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?", text)
    ]


def _convert_qe_vectors(
    rows: list[list[float]],
    unit: str,
    *,
    cell: list[list[float]],
    stdout: str,
) -> list[list[float]]:
    normalized = unit.lower().strip()
    if "crystal" in normalized:
        import numpy as np

        return (np.asarray(rows, dtype=float) @ np.asarray(cell, dtype=float)).tolist()
    if "bohr" in normalized:
        return [[value * _BOHR_TO_ANGSTROM for value in row] for row in rows]
    if "alat" in normalized:
        explicit = re.search(r"alat\s*=\s*([-+0-9.EeDd]+)", normalized)
        if explicit:
            scale_bohr = float(explicit.group(1).replace("D", "E").replace("d", "e"))
        else:
            matches = re.findall(
                r"lattice parameter \(alat\)\s*=\s*([-+0-9.EeDd]+)\s*a\.u\.",
                stdout,
                flags=re.I,
            )
            if not matches:
                raise ValueError("Could not resolve Quantum ESPRESSO alat unit")
            scale_bohr = float(matches[-1].replace("D", "E").replace("d", "e"))
        return [
            [value * scale_bohr * _BOHR_TO_ANGSTROM for value in row]
            for row in rows
        ]
    if not normalized or "angstrom" in normalized:
        return rows
    raise ValueError(f"Unsupported Quantum ESPRESSO coordinate unit: {unit}")


def _parse_qe_relaxed_structure(stdout: str, request: dict[str, Any]) -> dict[str, Any] | None:
    original, original_symbols, _coordinates, original_cell = _periodic_structure(
        request["inputs"]["structure"]
    )
    final_blocks = re.findall(
        r"Begin final coordinates(.*?)End final coordinates", stdout, flags=re.S | re.I
    )
    text = final_blocks[-1] if final_blocks else stdout
    lines = text.splitlines()
    position_indices = [
        index for index, line in enumerate(lines)
        if line.strip().upper().startswith("ATOMIC_POSITIONS")
    ]
    if not position_indices:
        return None
    position_index = position_indices[-1]
    position_header = lines[position_index]
    position_unit_match = re.search(r"[({]\s*([^)}]+)", position_header)
    position_unit = position_unit_match.group(1) if position_unit_match else "angstrom"
    symbols: list[str] = []
    raw_coordinates: list[list[float]] = []
    for line in lines[position_index + 1 : position_index + 1 + len(original_symbols)]:
        parts = line.split()
        if len(parts) < 4:
            return None
        symbols.append(parts[0])
        try:
            raw_coordinates.append([float(parts[1]), float(parts[2]), float(parts[3])])
        except ValueError:
            return None
    cell = original_cell
    cell_indices = [
        index for index, line in enumerate(lines[:position_index + 1])
        if line.strip().upper().startswith("CELL_PARAMETERS")
    ]
    if cell_indices:
        cell_index = cell_indices[-1]
        cell_header = lines[cell_index]
        cell_unit_match = re.search(r"[({]\s*([^)}]+)", cell_header)
        cell_unit = cell_unit_match.group(1) if cell_unit_match else "angstrom"
        try:
            raw_cell = [
                [float(value) for value in lines[cell_index + offset].split()[:3]]
                for offset in (1, 2, 3)
            ]
            cell = _convert_qe_vectors(raw_cell, cell_unit, cell=original_cell, stdout=stdout)
        except (ValueError, IndexError):
            return None
    try:
        coordinates = _convert_qe_vectors(
            raw_coordinates, position_unit, cell=cell, stdout=stdout
        )
    except ValueError:
        return None
    return _structure_payload(symbols, coordinates, cell, original)


def _qe_input(action_id: str, request: dict[str, Any], directory: Path) -> str:
    structure, symbols, coordinates, cell = _periodic_structure(request["inputs"]["structure"])
    method = request["method_spec"]
    settings = request["action_settings"]
    pseudos, pseudo_dir = _copy_pseudopotentials(dict(method["pseudopotentials"]), directory)
    missing = sorted(set(symbols) - set(pseudos))
    if missing:
        raise ValueError(f"Missing pseudopotentials for elements: {missing}")
    calculation = "scf"
    if action_id == "relax_periodic_structure":
        calculation = "vc-relax" if bool(settings.get("relax_cell", False)) else "relax"
    control = [
        "&CONTROL",
        f" calculation='{calculation}'",
        " prefix='researchchem'",
        f" pseudo_dir='{pseudo_dir}'",
        " outdir='./tmp'",
        " tprnfor=.true.",
        f" tstress={'.true.' if action_id in {'calculate_periodic_stress', 'relax_periodic_structure'} else '.false.'}",
        "/",
    ]
    system = [
        "&SYSTEM",
        " ibrav=0",
        f" nat={len(symbols)}",
        f" ntyp={len(set(symbols))}",
        f" ecutwfc={float(method['ecutwfc_ry'])}",
        f" input_dft='{method['input_dft']}'",
    ]
    if method.get("ecutrho_ry") is not None:
        system.append(f" ecutrho={float(method['ecutrho_ry'])}")
    if method.get("occupations"):
        system.append(f" occupations='{method['occupations']}'")
    if method.get("smearing"):
        system.extend([f" smearing='{method['smearing']}'", f" degauss={float(method.get('degauss_ry', 0.01))}"])
    system.append("/")
    electrons = ["&ELECTRONS", f" conv_thr={float(settings.get('scf_convergence_ry', 1e-8))}", "/"]
    if action_id == "relax_periodic_structure":
        control.insert(-1, f" forc_conv_thr={float(settings['force_threshold_ev_per_angstrom']) / 25.711043}")
        electrons.extend(
            [
                "&IONS",
                f" ion_dynamics='{settings.get('ion_dynamics', 'bfgs')}'",
                "/",
            ]
        )
        if bool(settings.get("relax_cell", False)):
            electrons.extend(["&CELL", f" press_conv_thr={float(settings.get('pressure_threshold_kbar', 0.5))}", "/"])
    species_lines = ["ATOMIC_SPECIES"]
    for symbol in sorted(set(symbols), key=symbols.index):
        species_lines.append(f"{symbol} {float(method.get('atomic_masses', {}).get(symbol, _ATOMIC_NUMBER[symbol]))} {pseudos[symbol]}")
    position_lines = ["ATOMIC_POSITIONS angstrom"] + [
        f"{symbol} {row[0]:.12f} {row[1]:.12f} {row[2]:.12f}"
        for symbol, row in zip(symbols, coordinates)
    ]
    cell_lines = ["CELL_PARAMETERS angstrom"] + [" ".join(f"{value:.12f}" for value in row) for row in cell]
    k = _k_points(method["k_points"])
    k_lines = ["K_POINTS automatic", " ".join(str(value) for value in k)]
    return "\n".join([*control, *system, *electrons, *species_lines, *position_lines, *cell_lines, *k_lines]) + "\n"


def _parse_qe(
    action_id: str,
    stdout: str,
    directory: Path,
    request: dict[str, Any],
) -> dict[str, Any]:
    energy_matches = re.findall(r"!\s+total energy\s+=\s+(-?\d+(?:\.\d+)?)\s+Ry", stdout)
    energy_ry = float(energy_matches[-1]) if energy_matches else None
    if action_id == "calculate_periodic_energy":
        if energy_ry is None:
            raise RuntimeError("Could not parse Quantum ESPRESSO total energy")
        return {"energy": energy_ry, "unit": "rydberg"}
    if action_id == "calculate_periodic_forces":
        number = r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?"
        forces = [
            [
                float(match.group(index).replace("D", "E").replace("d", "e"))
                for index in (1, 2, 3)
            ]
            for match in re.finditer(
                rf"^\s*atom\s+\d+\s+type\s+\d+\s+force\s*=\s*({number})\s+({number})\s+({number})",
                stdout,
                flags=re.M | re.I,
            )
        ]
        if not forces:
            raise RuntimeError("Could not parse Quantum ESPRESSO forces")
        return {"forces": forces, "unit": "rydberg/bohr", "energy_rydberg": energy_ry}
    if action_id == "calculate_periodic_stress":
        lines = stdout.splitlines()
        stress = None
        for index, line in enumerate(lines):
            if "total   stress" in line and index + 3 < len(lines):
                stress = [[float(value) for value in lines[index + offset].split()[:3]] for offset in (1, 2, 3)]
        if stress is None:
            raise RuntimeError("Could not parse Quantum ESPRESSO stress")
        return {"stress": stress, "unit": "rydberg/bohr^3", "energy_rydberg": energy_ry}
    relaxed = _parse_qe_relaxed_structure(stdout, request)
    return {
        "structure": relaxed,
        "converged": "convergence NOT achieved" not in stdout and "JOB DONE" in stdout,
        "energy_rydberg": energy_ry,
    }


def _run_qe(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    directory = output_directory(action_id, "quantum_espresso")
    text = _qe_input(action_id, request, directory)
    input_path = directory / "pw.in"
    input_path.write_text(text, encoding="utf-8")
    completed = run_external(
        executable="pw.x", environment_variable="CHEMGRAPH_QE_COMMAND",
        arguments=["-in", str(input_path)], directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 7200)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge qe")
    if completed["returncode"] != 0:
        raise RuntimeError(f"Quantum ESPRESSO failed: {completed['stderr'][-2000:]}")
    result = _parse_qe(action_id, completed["stdout"], directory, request)
    artifacts = command_artifacts(directory)
    provenance = {"command": completed["command"]}
    if action_id == "relax_periodic_structure" and (
        result.get("structure") is None or not result.get("converged")
    ):
        return partial_success(
            result,
            artifact_files=artifacts,
            provenance=provenance,
            warnings=[
                "Quantum ESPRESSO completed, but the relaxed structure was not both parsed and converged. Inspect the registered output artifacts."
            ],
        )
    return success(result, artifact_files=artifacts, provenance=provenance)


def _cp2k_input(action_id: str, request: dict[str, Any]) -> str:
    _structure, symbols, coordinates, cell = _periodic_structure(request["inputs"]["structure"])
    method = request["method_spec"]
    settings = request["action_settings"]
    run_type = "ENERGY_FORCE"
    if action_id == "calculate_periodic_energy":
        run_type = "ENERGY"
    elif action_id == "relax_periodic_structure":
        run_type = "CELL_OPT" if bool(settings.get("relax_cell", False)) else "GEO_OPT"
    scf_algorithm = str(method["scf_algorithm"]).lower()
    scf_lines = [
        "    &SCF",
        f"      EPS_SCF {float(settings.get('scf_convergence', 1e-6))}",
        f"      MAX_SCF {int(settings.get('max_scf_cycles', 100))}",
        "      SCF_GUESS ATOMIC",
    ]
    if scf_algorithm == "ot":
        scf_lines.extend(
            [
                "      &OT",
                f"        MINIMIZER {method.get('ot_minimizer', 'DIIS')}",
                f"        PRECONDITIONER {method.get('ot_preconditioner', 'FULL_SINGLE_INVERSE')}",
                "      &END OT",
                "      &OUTER_SCF",
                f"        EPS_SCF {float(settings.get('outer_scf_convergence', settings.get('scf_convergence', 1e-6)))}",
                f"        MAX_SCF {int(settings.get('max_outer_scf_cycles', 20))}",
                "      &END OUTER_SCF",
            ]
        )
    elif scf_algorithm == "diagonalization":
        scf_lines.extend(
            [
                "      &DIAGONALIZATION",
                "      &END DIAGONALIZATION",
                f"      ADDED_MOS {int(method.get('added_mos', 20))}",
                "      &SMEAR",
                "        METHOD FERMI_DIRAC",
                f"        ELECTRONIC_TEMPERATURE {float(method.get('electronic_temperature_kelvin', 300.0))}",
                "      &END SMEAR",
                "      &MIXING",
                f"        METHOD {method.get('mixing_method', 'BROYDEN_MIXING')}",
                f"        ALPHA {float(method.get('mixing_alpha', 0.2))}",
                "      &END MIXING",
            ]
        )
    else:
        raise ValueError("CP2K scf_algorithm must be ot or diagonalization")
    scf_lines.append("    &END SCF")
    k = _k_points(method["k_points"])
    kpoint_lines = []
    if k[:3] != (1, 1, 1):
        if scf_algorithm == "ot":
            raise ValueError("CP2K OT is restricted to Gamma-point calculations in this adapter")
        kpoint_lines = [
            "    &KPOINTS",
            f"      SCHEME MONKHORST-PACK {k[0]} {k[1]} {k[2]}",
            "    &END KPOINTS",
        ]
    lines = [
        "&GLOBAL", f"  RUN_TYPE {run_type}", "  PROJECT researchchem", "&END GLOBAL",
        "&FORCE_EVAL", "  METHOD Quickstep", "  &DFT",
        f"    BASIS_SET_FILE_NAME {method.get('basis_set_file', 'BASIS_MOLOPT')}",
        f"    POTENTIAL_FILE_NAME {method.get('potential_file', 'GTH_POTENTIALS')}",
        f"    &MGRID\n      CUTOFF {float(method['cutoff_ry'])}\n    &END MGRID",
        *scf_lines,
        *kpoint_lines,
        "    &XC", f"      &XC_FUNCTIONAL {method['method']}\n      &END XC_FUNCTIONAL", "    &END XC",
        "  &END DFT", "  &SUBSYS", "    &CELL",
        f"      A {' '.join(str(value) for value in cell[0])}",
        f"      B {' '.join(str(value) for value in cell[1])}",
        f"      C {' '.join(str(value) for value in cell[2])}",
        "    &END CELL", "    &COORD",
    ]
    if action_id == "calculate_periodic_stress":
        dft_start = lines.index("  &DFT")
        lines.insert(dft_start, "  STRESS_TENSOR ANALYTICAL")
    lines.extend(f"      {symbol} {row[0]} {row[1]} {row[2]}" for symbol, row in zip(symbols, coordinates))
    lines.extend(["    &END COORD"])
    for symbol in sorted(set(symbols), key=symbols.index):
        basis = method["basis_set"][symbol] if isinstance(method["basis_set"], dict) else method["basis_set"]
        potential = method["potential"][symbol] if isinstance(method["potential"], dict) else method["potential"]
        lines.extend(["    &KIND " + symbol, f"      ELEMENT {symbol}", f"      BASIS_SET {basis}", f"      POTENTIAL {potential}", "    &END KIND"])
    lines.extend(["  &END SUBSYS"])
    if action_id in {"calculate_periodic_forces", "calculate_periodic_stress"}:
        lines.extend(["  &PRINT"])
        if action_id == "calculate_periodic_forces":
            lines.extend(["    &FORCES ON", "    &END FORCES"])
        if action_id == "calculate_periodic_stress":
            lines.extend(["    &STRESS_TENSOR ON", "    &END STRESS_TENSOR"])
        lines.extend(["  &END PRINT"])
    lines.extend(["&END FORCE_EVAL"])
    if action_id == "relax_periodic_structure":
        section = "CELL_OPT" if bool(settings.get("relax_cell", False)) else "GEO_OPT"
        lines.extend(
            [
                "&MOTION", f"  &{section}",
                f"    MAX_ITER {int(settings.get('max_steps', 200))}",
                f"    MAX_FORCE {float(settings['force_threshold_ev_per_angstrom']) / 51.422067}",
                f"  &END {section}", "&END MOTION",
            ]
        )
    return "\n".join(lines) + "\n"


def _parse_cp2k(
    action_id: str,
    stdout: str,
    directory: Path,
    request: dict[str, Any],
) -> dict[str, Any]:
    energies = re.findall(r"ENERGY\| Total FORCE_EVAL.*?(-?\d+\.\d+(?:[Ee][+-]?\d+)?)", stdout)
    energy = float(energies[-1]) if energies else None
    if action_id == "calculate_periodic_energy":
        if energy is None:
            raise RuntimeError("Could not parse CP2K energy")
        return {"energy": energy, "unit": "hartree"}
    if action_id == "calculate_periodic_forces":
        current_matches = re.findall(
            r"^\s*FORCES\|\s+\d+\s+([+-]?\S+)\s+([+-]?\S+)\s+([+-]?\S+)(?:\s+\S+)?\s*$",
            stdout,
            re.M,
        )
        legacy_matches = re.findall(
            r"^\s*\d+\s+\d+\s+\S+\s+(-?\S+)\s+(-?\S+)\s+(-?\S+)\s*$",
            stdout,
            re.M,
        )
        matches = current_matches or legacy_matches
        forces = [[float(value) for value in row] for row in matches]
        if not forces:
            raise RuntimeError("Could not parse CP2K forces")
        return {"forces": forces, "unit": "hartree/bohr", "energy_hartree": energy}
    if action_id == "calculate_periodic_stress":
        current_header = re.search(
            r"^\s*STRESS\|\s+Analytical stress tensor \[([^\]]+)\]",
            stdout,
            re.M,
        )
        if current_header:
            rows = re.findall(
                r"^\s*STRESS\|\s+[xyzXYZ]\s+([+-]?\S+)\s+([+-]?\S+)\s+([+-]?\S+)\s*$",
                stdout[current_header.end() :],
                re.M,
            )[:3]
            source_unit = current_header.group(1).strip().lower()
            factors = {"bar": 1.0e-4, "kbar": 0.1, "gpa": 1.0, "pa": 1.0e-9}
            if source_unit not in factors:
                raise RuntimeError(f"Unsupported CP2K stress unit: {source_unit}")
            factor = factors[source_unit]
            stress = [[float(value) * factor for value in row] for row in rows]
            if len(stress) != 3:
                raise RuntimeError("Could not parse three CP2K analytical stress rows")
            return {
                "stress": stress,
                "unit": "GPa",
                "source_unit": source_unit,
                "energy_hartree": energy,
            }
        block = re.findall(r"STRESS TENSOR \[GPa\](.*?)(?:\n\s*\n)", stdout, re.S)
        rows = re.findall(r"^[XYZ]\s+(-?\S+)\s+(-?\S+)\s+(-?\S+)", block[-1], re.M) if block else []
        if len(rows) != 3:
            raise RuntimeError("Could not parse CP2K stress")
        return {"stress": [[float(value) for value in row] for row in rows], "unit": "GPa", "energy_hartree": energy}
    original, _symbols, _coordinates, original_cell = _periodic_structure(
        request["inputs"]["structure"]
    )
    xyz_outputs = sorted(
        directory.glob("researchchem-pos-*.xyz"), key=lambda path: path.stat().st_mtime_ns
    )
    relaxed = structure_dict(relative_workspace_path(xyz_outputs[-1])) if xyz_outputs else None
    cell = original_cell
    cell_outputs = sorted(
        directory.glob("researchchem*.cell"), key=lambda path: path.stat().st_mtime_ns
    )
    if cell_outputs:
        records = [
            line for line in cell_outputs[-1].read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        if records:
            values = _numeric_tokens(records[-1])
            if len(values) >= 11:
                cell = [values[2:5], values[5:8], values[8:11]]
    if relaxed is not None:
        parsed_symbols, parsed_coordinates = atoms_and_coordinates(relaxed)
        relaxed = _structure_payload(parsed_symbols, parsed_coordinates, cell, original)
    return {
        "structure": relaxed,
        "converged": "GEOMETRY OPTIMIZATION COMPLETED" in stdout or "CELL OPTIMIZATION COMPLETED" in stdout,
        "energy_hartree": energy,
    }


def _run_cp2k(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    directory = output_directory(action_id, "cp2k")
    input_path = directory / "cp2k.inp"
    input_path.write_text(_cp2k_input(action_id, request), encoding="utf-8")
    completed = run_external(
        executable="cp2k", environment_variable="CHEMGRAPH_CP2K_COMMAND",
        arguments=["-i", str(input_path)], directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 7200)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge cp2k")
    if completed["returncode"] != 0:
        raise RuntimeError(f"CP2K failed: {completed['stderr'][-2000:]}")
    result = _parse_cp2k(action_id, completed["stdout"], directory, request)
    artifacts = command_artifacts(directory)
    provenance = {"command": completed["command"]}
    if action_id == "relax_periodic_structure" and (
        result.get("structure") is None or not result.get("converged")
    ):
        return partial_success(
            result,
            artifact_files=artifacts,
            provenance=provenance,
            warnings=[
                "CP2K completed, but the relaxed structure was not both parsed and converged. Inspect the registered output artifacts."
            ],
        )
    return success(result, artifact_files=artifacts, provenance=provenance)


def _simple_periodic_input(backend_id: str, action_id: str, request: dict[str, Any], directory: Path) -> tuple[Path, list[str], str | None]:
    _structure, symbols, coordinates, cell = _periodic_structure(request["inputs"]["structure"])
    method = request["method_spec"]
    settings = request["action_settings"]
    if backend_id == "siesta":
        pseudos, _ = _copy_pseudopotentials(dict(method["pseudopotentials"]), directory)
        species = sorted(set(symbols), key=symbols.index)
        missing = sorted(set(species) - set(pseudos))
        if missing:
            raise ValueError(f"Missing SIESTA pseudopotentials for elements: {missing}")
        for symbol in species:
            suffix = Path(pseudos[symbol]).suffix or ".psf"
            shutil.copy2(
                directory / "pseudopotentials" / pseudos[symbol],
                directory / f"{symbol}{suffix}",
            )
        lines = [
            "SystemName ResearchChem", "SystemLabel researchchem",
            f"NumberOfAtoms {len(symbols)}", f"NumberOfSpecies {len(species)}",
            f"MeshCutoff {float(method['mesh_cutoff_ry'])} Ry",
            f"PAO.BasisSize {method['basis_size']}",
            f"XC.functional {method['xc_functional']}",
            f"XC.authors {method['xc_authors']}",
            "WriteForces true",
            "%block ChemicalSpeciesLabel",
        ]
        lines.extend(f"{index + 1} {_ATOMIC_NUMBER[symbol]} {symbol}" for index, symbol in enumerate(species))
        lines.extend(["%endblock ChemicalSpeciesLabel", "LatticeConstant 1.0 Ang", "%block LatticeVectors"])
        lines.extend(" ".join(str(value) for value in row) for row in cell)
        lines.extend(["%endblock LatticeVectors", "AtomicCoordinatesFormat Ang", "%block AtomicCoordinatesAndAtomicSpecies"])
        species_index = {symbol: index + 1 for index, symbol in enumerate(species)}
        lines.extend(f"{row[0]} {row[1]} {row[2]} {species_index[symbol]}" for symbol, row in zip(symbols, coordinates))
        lines.extend(["%endblock AtomicCoordinatesAndAtomicSpecies"])
        k = _k_points(method["k_points"])
        lines.extend(["%block kgrid_Monkhorst_Pack", f"{k[0]} 0 0 {k[3] / 2}", f"0 {k[1]} 0 {k[4] / 2}", f"0 0 {k[2]} {k[5] / 2}", "%endblock kgrid_Monkhorst_Pack"])
        if action_id == "relax_periodic_structure":
            lines.extend(
                [
                    "MD.TypeOfRun CG",
                    f"MD.NumCGsteps {int(settings['max_steps'])}",
                    f"MD.MaxForceTol {float(settings['force_threshold_ev_per_angstrom'])} eV/Ang",
                    f"MD.VariableCell {'true' if bool(settings['relax_cell']) else 'false'}",
                    f"MD.ConstantVolume {'false' if bool(settings['relax_cell']) else 'true'}",
                ]
            )
        path = directory / "siesta.fdf"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path, [], path.read_text(encoding="utf-8")
    if backend_id == "dftbplus":
        parameter_directory = resolve_input_file(method["parameter_set"])
        if not parameter_directory.is_dir():
            raise ValueError("DFTB+ parameter_set must resolve to a registered or workspace directory")
        species = sorted(set(symbols), key=symbols.index)
        missing_pairs = sorted(
            f"{first}-{second}.skf"
            for first in species
            for second in species
            if not (parameter_directory / f"{first}-{second}.skf").is_file()
        )
        if missing_pairs:
            raise ValueError(
                "DFTB+ parameter set lacks required directed Slater-Koster files: "
                + ", ".join(missing_pairs)
            )
        angular_momenta = dict(method["max_angular_momenta"])
        missing_angular = sorted(set(species) - set(angular_momenta))
        if missing_angular:
            raise ValueError(
                f"Missing DFTB+ max_angular_momenta for elements: {missing_angular}"
            )
        lines = ["Geometry = GenFormat {", f"  {len(symbols)} S", "  " + " ".join(species)]
        species_index = {symbol: index + 1 for index, symbol in enumerate(species)}
        lines.extend(f"  {index + 1} {species_index[symbol]} {row[0]} {row[1]} {row[2]}" for index, (symbol, row) in enumerate(zip(symbols, coordinates)))
        lines.extend(["  0.0 0.0 0.0", *["  " + " ".join(str(value) for value in row) for row in cell], "}"])
        if action_id == "relax_periodic_structure":
            lines.extend(
                [
                    "Driver = GeometryOptimization {",
                    "  Optimizer = Rational {}",
                    f"  MaxSteps = {int(settings['max_steps'])}",
                    "  Convergence = {",
                    f"    GradElem = {float(settings['force_threshold_ev_per_angstrom']) / 51.422067}",
                    "  }",
                    f"  LatticeOpt = {'Yes' if bool(settings['relax_cell']) else 'No'}",
                    "}",
                ]
            )
        scc = bool(method["scc"])
        lines.extend([
            "Hamiltonian = DFTB {", f"  SCC = {'Yes' if scc else 'No'}",
            "  SlaterKosterFiles = Type2FileNames {",
            f"    Prefix = \"{parameter_directory}/\"", "    Separator = \"-\"", "    Suffix = \".skf\"", "  }",
            "  MaxAngularMomentum = {",
        ])
        lines.extend(
            f"    {symbol} = \"{angular_momenta[symbol]}\"" for symbol in species
        )
        lines.append("  }")
        if scc:
            lines.extend(
                [
                    f"  SCCTolerance = {float(settings['scc_tolerance'])}",
                    f"  MaxSCCIterations = {int(settings['max_scc_iterations'])}",
                ]
            )
        if method.get("charge") is not None:
            lines.append(f"  Charge = {float(method['charge'])}")
        if method.get("shell_resolved_scc") is not None:
            lines.append(
                f"  ShellResolvedSCC = {'Yes' if bool(method['shell_resolved_scc']) else 'No'}"
            )
        if method.get("third_order_full") is not None:
            lines.append(
                f"  ThirdOrderFull = {'Yes' if bool(method['third_order_full']) else 'No'}"
            )
        if method.get("hubbard_derivatives"):
            lines.append("  HubbardDerivs = {")
            lines.extend(
                f"    {symbol} = {float(value)}"
                for symbol, value in dict(method["hubbard_derivatives"]).items()
            )
            lines.append("  }")
        if method.get("damp_xh_exponent") is not None:
            lines.extend(
                [
                    "  HCorrection = Damping {",
                    f"    Exponent = {float(method['damp_xh_exponent'])}",
                    "  }",
                ]
            )
        if method.get("fermi_temperature_kelvin") is not None:
            lines.extend(
                [
                    "  Filling = Fermi {",
                    f"    Temperature [Kelvin] = {float(method['fermi_temperature_kelvin'])}",
                    "  }",
                ]
            )
        k_points = _k_points(method["k_points"])
        lines.extend(
            [
                "  KPointsAndWeights = SupercellFolding {",
                f"    {k_points[0]} 0 0",
                f"    0 {k_points[1]} 0",
                f"    0 0 {k_points[2]}",
                f"    {k_points[3] / 2} {k_points[4] / 2} {k_points[5] / 2}",
                "  }",
                "}",
            ]
        )
        if action_id in {"calculate_periodic_forces", "relax_periodic_structure"}:
            lines.append("Analysis = { PrintForces = Yes }")
        lines.append("ParserOptions = { ParserVersion = 14 }")
        path = directory / "dftb_in.hsd"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path, [], None
    if backend_id == "abinit":
        pseudos, pseudo_dir = _copy_pseudopotentials(dict(method["pseudopotentials"]), directory)
        species = sorted(set(symbols), key=symbols.index)
        missing = sorted(set(species) - set(pseudos))
        if missing:
            raise ValueError(f"Missing ABINIT pseudopotentials for elements: {missing}")
        # Convert Cartesian Angstrom to reduced coordinates.
        import numpy as np

        reduced = np.linalg.solve(np.asarray(cell, dtype=float).T, np.asarray(coordinates, dtype=float).T).T
        lines = [
            f"natom {len(symbols)}", f"ntypat {len(species)}",
            "znucl " + " ".join(str(_ATOMIC_NUMBER[symbol]) for symbol in species),
            "typat " + " ".join(str(species.index(symbol) + 1) for symbol in symbols),
            "acell 1 1 1 angstrom", "rprim",
            *[" ".join(str(value) for value in row) for row in cell],
            "xred", *[" ".join(str(value) for value in row) for row in reduced],
            f"ecut {float(method['ecut_hartree'])}",
            f"ixc {method['ixc']}",
            "ngkpt " + " ".join(str(value) for value in _k_points(method["k_points"])[:3]),
            "nshiftk 1", "shiftk 0 0 0",
            "tolvrs " + str(float(settings.get("scf_convergence_hartree", 1e-10))),
            "prtwf 0",
            'pseudos "' + ", ".join(str(pseudo_dir / pseudos[symbol]) for symbol in species) + '"',
        ]
        if action_id == "relax_periodic_structure":
            lines.extend(
                [
                    "ionmov 2",
                    f"ntime {int(settings['max_steps'])}",
                    f"tolmxf {float(settings['force_threshold_ev_per_angstrom']) / 51.422067}",
                    f"optcell {2 if bool(settings['relax_cell']) else 0}",
                ]
            )
        path = directory / "abinit.abi"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path, [], None
    raise ValueError(f"Unsupported periodic backend: {backend_id}")


def _force_rows_after_marker(
    text: str,
    marker: str,
    atom_count: int,
) -> list[list[float]] | None:
    lines = text.splitlines()
    marker_indices = [
        index for index, line in enumerate(lines) if marker.lower() in line.lower()
    ]
    for marker_index in reversed(marker_indices):
        rows: list[list[float]] = []
        for line in lines[marker_index + 1 :]:
            values = _numeric_tokens(line)
            if len(values) >= 3:
                rows.append(values[-3:])
                if len(rows) == atom_count:
                    return rows
            elif rows:
                break
    return None


def _parse_siesta_forces(
    directory: Path,
    stdout: str,
    atom_count: int,
) -> list[list[float]] | None:
    force_files = sorted(directory.glob("*.FA"), key=lambda path: path.stat().st_mtime_ns)
    if force_files:
        rows = []
        for line in force_files[-1].read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
            values = _numeric_tokens(line)
            if len(values) >= 4:
                rows.append(values[-3:])
        if len(rows) == atom_count:
            return rows
    return _force_rows_after_marker(stdout, "Atomic forces", atom_count)


def _parse_dftb_forces(
    directory: Path,
    stdout: str,
    atom_count: int,
) -> list[list[float]] | None:
    detailed = directory / "detailed.out"
    text = detailed.read_text(encoding="utf-8", errors="replace") if detailed.is_file() else stdout
    return _force_rows_after_marker(text, "Total Forces", atom_count)


def _parse_abinit_forces(stdout: str, atom_count: int) -> list[list[float]] | None:
    result = _force_rows_after_marker(
        stdout, "cartesian forces (hartree/bohr) at end", atom_count
    )
    if result is not None:
        return result
    result = _force_rows_after_marker(stdout, "cartesian_forces:", atom_count)
    if result is not None:
        return result
    return _force_rows_after_marker(stdout, "forces (hartree/bohr)", atom_count)


def _parse_abinit_stress(stdout: str) -> list[list[float]] | None:
    headers = list(
        re.finditer(
            r"Cartesian components of stress tensor \(hartree/bohr\^3\)",
            stdout,
            flags=re.I,
        )
    )
    for header in reversed(headers):
        section = stdout[header.end() :]
        stop = re.search(
            r"Cartesian components of stress tensor \((?:GPa|hartree/bohr\^3)\)",
            section,
            flags=re.I,
        )
        if stop:
            section = section[: stop.start()]
        components: dict[tuple[int, int], float] = {}
        for match in re.finditer(
            r"sigma\(\s*([123])\s*([123])\s*\)\s*=\s*([-+0-9.EeDd]+)",
            section,
            flags=re.I,
        ):
            components[(int(match.group(1)) - 1, int(match.group(2)) - 1)] = float(
                match.group(3).replace("D", "E").replace("d", "e")
            )
        if all((index, index) in components for index in range(3)):
            matrix = [[0.0, 0.0, 0.0] for _ in range(3)]
            for (row, column), value in components.items():
                matrix[row][column] = value
                matrix[column][row] = value
            return matrix
    return None


def _parse_siesta_relaxed_structure(
    directory: Path,
    request: dict[str, Any],
) -> dict[str, Any] | None:
    original, symbols, _coordinates, _cell = _periodic_structure(request["inputs"]["structure"])
    files = sorted(directory.glob("*.XV"), key=lambda path: path.stat().st_mtime_ns)
    if not files:
        return None
    lines = files[-1].read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) < 4 + len(symbols):
        return None
    try:
        cell = [
            [value * _BOHR_TO_ANGSTROM for value in _numeric_tokens(lines[index])[:3]]
            for index in range(3)
        ]
        coordinates = [
            [value * _BOHR_TO_ANGSTROM for value in _numeric_tokens(line)[2:5]]
            for line in lines[4 : 4 + len(symbols)]
        ]
    except (ValueError, IndexError):
        return None
    if any(len(row) != 3 for row in [*cell, *coordinates]):
        return None
    return _structure_payload(symbols, coordinates, cell, original)


def _parse_dftb_gen(path: Path, request: dict[str, Any]) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    original, original_symbols, _coordinates, original_cell = _periodic_structure(
        request["inputs"]["structure"]
    )
    lines = [line.strip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    if len(lines) < 2:
        return None
    header = lines[0].split()
    try:
        atom_count = int(header[0])
    except (ValueError, IndexError):
        return None
    if atom_count != len(original_symbols):
        return None
    mode = header[1].upper() if len(header) > 1 else "C"
    species = lines[1].split()
    symbols: list[str] = []
    coordinates: list[list[float]] = []
    for line in lines[2 : 2 + atom_count]:
        parts = line.split()
        if len(parts) < 5:
            return None
        try:
            symbols.append(species[int(parts[1]) - 1])
            coordinates.append([float(parts[2]), float(parts[3]), float(parts[4])])
        except (ValueError, IndexError):
            return None
    cell = original_cell
    if mode in {"S", "F"} and len(lines) >= 2 + atom_count + 4:
        try:
            cell = [
                [float(value) for value in lines[2 + atom_count + offset].split()[:3]]
                for offset in (1, 2, 3)
            ]
        except (ValueError, IndexError):
            return None
    if mode == "F":
        import numpy as np

        coordinates = (np.asarray(coordinates, dtype=float) @ np.asarray(cell, dtype=float)).tolist()
    return _structure_payload(symbols, coordinates, cell, original)


def _values_after_keyword(lines: list[str], keyword: str, count: int) -> list[float] | None:
    indices = [
        index for index, line in enumerate(lines)
        if line.strip().lower().startswith(keyword.lower())
    ]
    for index in reversed(indices):
        values = _numeric_tokens(lines[index][len(lines[index]) - len(lines[index].lstrip()) + len(keyword):])
        cursor = index + 1
        while len(values) < count and cursor < len(lines):
            values.extend(_numeric_tokens(lines[cursor]))
            cursor += 1
        if len(values) >= count:
            return values[:count]
    return None


def _parse_abinit_relaxed_structure(
    stdout: str,
    request: dict[str, Any],
) -> dict[str, Any] | None:
    original, symbols, _coordinates, original_cell = _periodic_structure(request["inputs"]["structure"])
    lines = stdout.splitlines()
    reduced_values = _values_after_keyword(lines, "xred", 3 * len(symbols))
    if reduced_values is None:
        return None
    cell = original_cell
    rprimd = _values_after_keyword(lines, "rprimd", 9)
    if rprimd is not None:
        cell = [
            [value * _BOHR_TO_ANGSTROM for value in rprimd[index : index + 3]]
            for index in (0, 3, 6)
        ]
    import numpy as np

    reduced = np.asarray(reduced_values, dtype=float).reshape((-1, 3))
    coordinates = (reduced @ np.asarray(cell, dtype=float)).tolist()
    return _structure_payload(symbols, coordinates, cell, original)


def _run_simple_periodic(backend_id: str, action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    directory = output_directory(action_id, backend_id)
    input_path, pseudo_paths, stdin_text = _simple_periodic_input(backend_id, action_id, request, directory)
    executable = {"siesta": "siesta", "dftbplus": "dftb+", "abinit": "abinit"}[backend_id]
    variable = {"siesta": "CHEMGRAPH_SIESTA_COMMAND", "dftbplus": "CHEMGRAPH_DFTBPLUS_COMMAND", "abinit": "CHEMGRAPH_ABINIT_COMMAND"}[backend_id]
    arguments = [str(input_path), *pseudo_paths] if backend_id == "abinit" else []
    completed = run_external(
        executable=executable, environment_variable=variable, arguments=arguments,
        directory=directory, stdin_text=stdin_text,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 7200)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install=f"conda install -c conda-forge {executable}")
    if completed["returncode"] != 0:
        raise RuntimeError(f"{backend_id} failed: {completed['stderr'][-2000:]}")
    stdout = completed["stdout"]
    parsed_output = stdout
    if backend_id == "abinit":
        abinit_output = directory / "abinit.abo"
        if abinit_output.is_file():
            parsed_output += "\n" + abinit_output.read_text(
                encoding="utf-8", errors="replace"
            )
    energy = None
    _structure, symbols, _coordinates, _cell = _periodic_structure(request["inputs"]["structure"])
    if backend_id == "siesta":
        matches = re.findall(r"siesta:\s*E_KS\(eV\)\s*=\s*([-+0-9.EeDd]+)", stdout, flags=re.I)
        energy = float(matches[-1].replace("D", "E").replace("d", "e")) if matches else None
        energy_unit = "eV"
    elif backend_id == "dftbplus":
        detailed = directory / "detailed.out"
        text = detailed.read_text(encoding="utf-8") if detailed.is_file() else stdout
        matches = re.findall(r"Total energy:\s*([-+0-9.EeDd]+)\s+H", text, flags=re.I)
        energy = float(matches[-1].replace("D", "E").replace("d", "e")) if matches else None
        energy_unit = "hartree"
    else:
        matches = re.findall(r"\betotal\b\s*(?:=|:)?\s*([-+0-9.EeDd]+)", parsed_output, flags=re.I)
        energy = float(matches[-1].replace("D", "E").replace("d", "e")) if matches else None
        energy_unit = "hartree"
    if action_id == "calculate_periodic_energy":
        if energy is None:
            raise RuntimeError(f"Could not parse {backend_id} energy")
        result = {"energy": energy, "unit": energy_unit}
    elif action_id == "calculate_periodic_forces":
        if backend_id == "siesta":
            forces = _parse_siesta_forces(directory, stdout, len(symbols))
            force_unit = "eV/angstrom"
        elif backend_id == "dftbplus":
            forces = _parse_dftb_forces(directory, stdout, len(symbols))
            force_unit = "hartree/bohr"
        else:
            forces = _parse_abinit_forces(parsed_output, len(symbols))
            force_unit = "hartree/bohr"
        result = {
            "forces": forces,
            "unit": force_unit if forces is not None else None,
            "energy": energy,
            "energy_unit": energy_unit,
            "raw_output_path": relative_workspace_path(directory / "stdout.log"),
        }
    elif action_id == "calculate_periodic_stress":
        stress = _parse_abinit_stress(parsed_output) if backend_id == "abinit" else None
        result = {
            "stress": stress,
            "unit": "hartree/bohr^3" if stress is not None else None,
            "energy": energy,
            "energy_unit": energy_unit,
            "raw_output_path": relative_workspace_path(directory / "stdout.log"),
        }
    else:
        if backend_id == "siesta":
            relaxed = _parse_siesta_relaxed_structure(directory, request)
            converged = "outcoor: Relaxed atomic coordinates" in stdout or "siesta: Final energy" in stdout
        elif backend_id == "dftbplus":
            relaxed = _parse_dftb_gen(directory / "geo_end.gen", request)
            detailed_text = (directory / "detailed.out").read_text(encoding="utf-8", errors="replace") if (directory / "detailed.out").is_file() else stdout
            converged = "Geometry converged" in detailed_text
        else:
            relaxed = _parse_abinit_relaxed_structure(parsed_output, request)
            converged = "Calculation completed" in parsed_output or "completed successfully" in parsed_output.lower()
        result = {
            "structure": relaxed,
            "converged": converged,
            "energy": energy,
            "energy_unit": energy_unit,
            "raw_output_path": relative_workspace_path(directory / "stdout.log"),
        }
    artifacts = command_artifacts(directory)
    provenance = {"command": completed["command"]}
    primary_complete = (
        action_id == "calculate_periodic_energy"
        or (action_id == "calculate_periodic_forces" and result.get("forces") is not None)
        or (action_id == "calculate_periodic_stress" and result.get("stress") is not None)
        or (
            action_id == "relax_periodic_structure"
            and result.get("structure") is not None
            and bool(result.get("converged"))
        )
    )
    if not primary_complete:
        return partial_success(
            result,
            artifact_files=artifacts,
            provenance=provenance,
            warnings=[
                f"{backend_id} completed, but its primary result was not fully parsed or the relaxation did not converge. Inspect the registered output artifacts."
            ],
        )
    return success(result, artifact_files=artifacts, provenance=provenance)


def _phonopy_atoms(structure_value: Any):
    from phonopy.structure.atoms import PhonopyAtoms

    _structure, symbols, coordinates, cell = _periodic_structure(structure_value)
    return PhonopyAtoms(symbols=symbols, positions=coordinates, cell=cell)


def _phonon_object(backend_id: str, structure_value: Any, settings: dict[str, Any]):
    unitcell = _phonopy_atoms(structure_value)
    matrix = settings.get("supercell_matrix") or [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    primitive_matrix = settings.get("primitive_matrix", "auto")
    if backend_id == "phonopy":
        from phonopy import Phonopy

        return Phonopy(unitcell, matrix, primitive_matrix=primitive_matrix)
    from phono3py import Phono3py

    return Phono3py(
        unitcell,
        matrix,
        primitive_matrix=primitive_matrix,
        phonon_supercell_matrix=settings.get("phonon_supercell_matrix", matrix),
    )


def _jsonable(value: Any) -> Any:
    """Convert NumPy-rich phonon datasets into stable JSON-compatible objects."""

    import numpy as np

    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _phonons(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, _method, settings = request_parts(request)
    structure_value = inputs.get("structure")
    if action_id == "calculate_lattice_thermal_conductivity":
        fc2_value = inputs["second_order_force_constants"]
        fc3_value = inputs["third_order_force_constants"]
        if isinstance(fc2_value, dict) and "result" in fc2_value:
            fc2_value = fc2_value["result"]
        if isinstance(fc3_value, dict) and "result" in fc3_value:
            fc3_value = fc3_value["result"]
        fc2 = fc2_value.get("force_constants", fc2_value)
        fc3 = fc3_value.get("force_constants", fc3_value)
        supercell_matrix = fc3_value.get("supercell_matrix") or [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        phonon_supercell_matrix = fc2_value.get("supercell_matrix") or supercell_matrix
        phono3py = _phonon_object(
            "phono3py",
            structure_value,
            {
                "supercell_matrix": supercell_matrix,
                "phonon_supercell_matrix": phonon_supercell_matrix,
                "primitive_matrix": settings["primitive_matrix"],
            },
        )
        phono3py.fc2 = np.asarray(fc2, dtype=float)
        phono3py.fc3 = np.asarray(fc3, dtype=float)
        phono3py.mesh_numbers = settings["q_mesh"]
        phono3py.init_phph_interaction(
            symmetrize_fc3q=bool(settings.get("symmetrize_fc3q", False))
        )
        solution = str(settings["solution_method"]).strip().lower()
        if solution not in {"rta", "lbte"}:
            raise ValueError("solution_method must be rta or lbte")
        boundary = settings["boundary_mean_free_path_micrometer"]
        phono3py.run_thermal_conductivity(
            is_LBTE=solution == "lbte",
            temperatures=np.asarray(settings["temperatures_kelvin"], dtype=float),
            is_isotope=bool(settings["include_isotope_scattering"]),
            mass_variances=settings.get("mass_variances"),
            boundary_mfp=None if boundary is None else float(boundary),
            is_kappa_star=bool(settings.get("use_kappa_star", True)),
            is_full_pp=bool(settings.get("full_phonon_phonon_interaction", False)),
            log_level=0,
        )
        conductivity = phono3py.thermal_conductivity
        if conductivity is None or conductivity.kappa is None:
            raise RuntimeError("Phono3py completed without a thermal-conductivity tensor")
        kappa = np.asarray(conductivity.kappa, dtype=float)
        if kappa.ndim == 3 and kappa.shape[0] == 1:
            kappa = kappa[0]
        if not np.all(np.isfinite(kappa)):
            raise RuntimeError(
                "Phono3py produced non-finite conductivity; inspect force constants or set an explicit finite boundary mean free path"
            )
        result = {
            "temperatures_kelvin": np.asarray(conductivity.temperatures, dtype=float).tolist(),
            "kappa_w_mk": kappa.tolist(),
            "voigt_order": "xx,yy,zz,yz,xz,xy",
            "solution_method": solution,
            "q_mesh": settings["q_mesh"],
            "include_isotope_scattering": bool(settings["include_isotope_scattering"]),
            "boundary_mean_free_path_micrometer": boundary,
        }
        if bool(settings.get("include_mode_data", False)):
            for key, attribute in (
                ("linewidth_thz", "gamma"),
                ("group_velocity_thz_angstrom", "group_velocities"),
                ("mode_heat_capacity_ev_per_k", "heat_capacities"),
            ):
                value = getattr(conductivity, attribute, None)
                if value is not None:
                    result[key] = np.asarray(value, dtype=float).tolist()
        return success(result, backend_version=module_version("phono3py"))
    if action_id == "generate_displaced_supercells":
        phonon = _phonon_object(backend_id, structure_value, settings)
        distance = float(settings["displacement_distance_angstrom"])
        if backend_id == "phonopy":
            phonon.generate_displacements(distance=distance)
            supercells = phonon.supercells_with_displacements
            dataset = phonon.dataset
            order = 2
        else:
            order = int(settings["order"])
            if order == 2:
                phonon.generate_fc2_displacements(distance=distance)
                supercells = phonon.phonon_supercells_with_displacements
                dataset = phonon.phonon_dataset
            elif order == 3:
                phonon.generate_displacements(distance=distance)
                supercells = phonon.supercells_with_displacements
                dataset = phonon.dataset
            else:
                raise ValueError("phono3py displacement order must be 2 or 3")
        structures = []
        for index, supercell in enumerate(supercells):
            structures.append(
                {
                    "displacement_id": index,
                    "structure": {
                        "symbols": list(supercell.symbols),
                        "coordinates_angstrom": np.asarray(supercell.positions).tolist(),
                        "cell_angstrom": np.asarray(supercell.cell).tolist(),
                        "pbc": [True, True, True],
                    },
                }
            )
        return success(
            {
                "original_structure": structure_value,
                "supercell_matrix": settings["supercell_matrix"],
                "displacement_distance_angstrom": distance,
                "order": order,
                "displacements": structures,
                "dataset": _jsonable(dataset),
            },
            backend_version=module_version(backend_id),
        )
    displacement_set = inputs.get("displacement_set")
    if isinstance(displacement_set, dict) and "result" in displacement_set:
        displacement_set = displacement_set["result"]
    if action_id == "assemble_force_constants":
        force_set = inputs["force_set"]
        if isinstance(force_set, dict) and "result" in force_set:
            force_set = force_set["result"]
        structure_value = displacement_set["original_structure"]
        local_settings = {"supercell_matrix": displacement_set["supercell_matrix"]}
        phonon = _phonon_object(backend_id, structure_value, local_settings)
        force_values = force_set.get("forces", force_set) if isinstance(force_set, dict) else force_set
        if backend_id == "phonopy":
            phonon.dataset = displacement_set["dataset"]
            phonon.forces = np.asarray(force_values, dtype=float)
            phonon.produce_force_constants()
            constants = np.asarray(phonon.force_constants).tolist()
            order = 2
        else:
            order = int(displacement_set.get("order", 3))
            if order == 2:
                phonon.phonon_dataset = displacement_set["dataset"]
                phonon.phonon_forces = np.asarray(force_values, dtype=float)
                phonon.produce_fc2(is_compact_fc=False)
                constants = np.asarray(phonon.fc2).tolist()
            elif order == 3:
                phonon.dataset = displacement_set["dataset"]
                phonon.forces = np.asarray(force_values, dtype=float)
                phonon.produce_fc3(is_compact_fc=False)
                constants = np.asarray(phonon.fc3).tolist()
            else:
                raise ValueError("phono3py force-constant order must be 2 or 3")
        return success(
            {
                "force_constants": constants,
                "order": order,
                "supercell_matrix": displacement_set["supercell_matrix"],
                "original_structure": structure_value,
            },
            backend_version=module_version(backend_id),
        )
    force_constants = inputs["force_constants"]
    if isinstance(force_constants, dict) and "result" in force_constants:
        force_constants = force_constants["result"]
    structure_value = inputs["structure"]
    if int(force_constants.get("order", 2)) != 2:
        return unsupported("Phonon dispersion and DOS require second-order force constants")
    # Phono3py's harmonic analysis is implemented by its Phonopy dependency. This
    # remains the explicitly selected phono3py adapter; no backend dispatch occurs.
    phonon = _phonon_object("phonopy", structure_value, {"supercell_matrix": force_constants.get("supercell_matrix")})
    phonon.force_constants = np.asarray(force_constants["force_constants"], dtype=float)
    if action_id in {"calculate_phonon_dispersion", "calculate_phonon_group_velocities"}:
        q_path = settings["q_path"]
        paths = [np.asarray(segment, dtype=float) for segment in q_path]
        phonon.run_band_structure(
            paths,
            with_eigenvectors=bool(settings.get("with_eigenvectors", False)),
            with_group_velocities=action_id == "calculate_phonon_group_velocities",
            labels=settings.get("labels"),
        )
        result = phonon.get_band_structure_dict()
        if action_id == "calculate_phonon_group_velocities":
            return success(
                {
                    "qpoints": [np.asarray(value).tolist() for value in result["qpoints"]],
                    "distances": [np.asarray(value).tolist() for value in result["distances"]],
                    "frequencies_thz": [np.asarray(value).tolist() for value in result["frequencies"]],
                    "group_velocities_thz_angstrom": [
                        np.asarray(value).tolist() for value in result["group_velocities"]
                    ],
                    "labels": settings.get("labels"),
                },
                backend_version=module_version(backend_id),
            )
        return success(
            {
                "qpoints": [np.asarray(value).tolist() for value in result["qpoints"]],
                "distances": [np.asarray(value).tolist() for value in result["distances"]],
                "frequencies_thz": [np.asarray(value).tolist() for value in result["frequencies"]],
                "labels": settings.get("labels"),
            },
            backend_version=module_version(backend_id),
        )
    if action_id == "calculate_harmonic_thermodynamics":
        temperatures = np.asarray(settings["temperatures_kelvin"], dtype=float)
        if temperatures.ndim != 1 or len(temperatures) == 0 or np.any(temperatures < 0):
            raise ValueError("temperatures_kelvin must be a non-empty list of nonnegative values")
        phonon.run_mesh(settings["q_mesh"], with_eigenvectors=False, is_mesh_symmetry=True)
        phonon.run_thermal_properties(
            temperatures=temperatures,
            cutoff_frequency=settings.get("cutoff_frequency_thz"),
            pretend_real=bool(settings.get("pretend_real", False)),
            classical=bool(settings.get("classical", False)),
        )
        thermal = phonon.get_thermal_properties_dict()
        return success(
            {
                "temperatures_kelvin": np.asarray(thermal["temperatures"], dtype=float).tolist(),
                "free_energy_kj_mol": np.asarray(thermal["free_energy"], dtype=float).tolist(),
                "entropy_j_k_mol": np.asarray(thermal["entropy"], dtype=float).tolist(),
                "heat_capacity_cv_j_k_mol": np.asarray(thermal["heat_capacity"], dtype=float).tolist(),
                "q_mesh": settings["q_mesh"],
                "classical": bool(settings.get("classical", False)),
            },
            backend_version=module_version(backend_id),
        )
    phonon.run_mesh(settings["q_mesh"], with_eigenvectors=False, is_mesh_symmetry=True)
    phonon.run_total_dos()
    dos = phonon.get_total_dos_dict()
    return success(
        {"frequency_thz": np.asarray(dos["frequency_points"]).tolist(), "density_of_states": np.asarray(dos["total_dos"]).tolist(), "q_mesh": settings["q_mesh"]},
        backend_version=module_version(backend_id),
    )


def _run_mlip_periodic(
    backend_id: str,
    action_id: str,
    request: dict[str, Any],
) -> dict[str, Any]:
    import numpy as np
    from ase.stress import voigt_6_to_full_3x3_stress

    inputs, method, settings = request_parts(request)
    _periodic_structure(inputs["structure"])
    atoms = ase_atoms(inputs["structure"])
    prepare_mlip_atoms(backend_id, atoms, method)
    calculator, version, model_provenance = build_mlip_calculator(backend_id, method)
    atoms.calc = calculator

    if action_id == "calculate_periodic_energy":
        return success(
            {
                "energy": float(atoms.get_potential_energy()),
                "unit": "eV",
                "atom_count": len(atoms),
            },
            backend_version=version,
            provenance=model_provenance,
        )
    if action_id == "calculate_periodic_forces":
        forces = np.asarray(atoms.get_forces(), dtype=float)
        return success(
            {
                "forces": forces.tolist(),
                "unit": "eV/angstrom",
                "atom_count": len(atoms),
                "energy_ev": float(atoms.get_potential_energy()),
            },
            backend_version=version,
            provenance=model_provenance,
        )
    if action_id == "calculate_periodic_stress":
        stress_voigt = np.asarray(atoms.get_stress(voigt=True), dtype=float)
        stress = voigt_6_to_full_3x3_stress(stress_voigt)
        return success(
            {
                "stress": np.asarray(stress, dtype=float).tolist(),
                "unit": "eV/angstrom^3",
                "voigt_order": "xx,yy,zz,yz,xz,xy",
                "energy_ev": float(atoms.get_potential_energy()),
            },
            backend_version=version,
            provenance=model_provenance,
        )
    if action_id == "relax_periodic_structure":
        from ase.optimize import BFGS, FIRE, LBFGS

        directory = output_directory(action_id, backend_id)
        optimizer_name = str(settings["optimizer"]).lower()
        optimizer_class = {"bfgs": BFGS, "lbfgs": LBFGS, "fire": FIRE}.get(
            optimizer_name
        )
        if optimizer_class is None:
            raise ValueError("optimizer must be bfgs, lbfgs, or fire")
        target: Any = atoms
        if bool(settings["relax_cell"]):
            from ase.filters import FrechetCellFilter

            target = FrechetCellFilter(
                atoms,
                hydrostatic_strain=bool(settings.get("hydrostatic_strain", False)),
                scalar_pressure=float(
                    settings.get("scalar_pressure_ev_per_angstrom3", 0.0)
                ),
            )
        optimizer = optimizer_class(
            target,
            logfile=str(directory / "optimization.log"),
            trajectory=str(directory / "optimization.traj"),
        )
        converged = bool(
            optimizer.run(
                fmax=float(settings["force_threshold_ev_per_angstrom"]),
                steps=int(settings["max_steps"]),
            )
        )
        from ase.io import write

        write(str(directory / "optimized.extxyz"), atoms)
        result = {
            "structure": structure_from_atoms(atoms),
            "converged": converged,
            "energy": float(atoms.get_potential_energy()),
            "energy_unit": "eV",
            "optimizer": optimizer_name,
            "relax_cell": bool(settings["relax_cell"]),
        }
        values = {
            "artifact_files": command_artifacts(directory),
            "backend_version": version,
            "provenance": model_provenance,
        }
        if not converged:
            return partial_success(
                result,
                warnings=["MLIP relaxation reached its step limit before convergence."],
                **values,
            )
        return success(result, **values)
    return unsupported(f"MLIP backend does not implement {action_id}")


def _lobster_spin_values(values: dict[Any, Any], spin: str):
    import numpy as np
    from pymatgen.electronic_structure.core import Spin

    spin = spin.strip().lower()
    if spin == "up":
        if Spin.up not in values:
            raise ValueError("The LOBSTER output contains no spin-up channel")
        return np.asarray(values[Spin.up], dtype=float)
    if spin == "down":
        if Spin.down not in values:
            raise ValueError("The LOBSTER output contains no spin-down channel")
        return np.asarray(values[Spin.down], dtype=float)
    if spin in {"sum", "total"}:
        arrays = [np.asarray(value, dtype=float) for value in values.values()]
        if not arrays:
            raise ValueError("The LOBSTER output contains no spin channels")
        return np.sum(arrays, axis=0)
    raise ValueError("spin must be up, down, or sum")


def _lobster_bonding(request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    from pymatgen.io.lobster.outputs import Cohpcar, Icohplist

    inputs, _method, settings = request_parts(request)
    metric = str(settings["bonding_metric"]).strip().lower()
    if metric not in {"cohp", "coop", "cobi"}:
        raise ValueError("bonding_metric must be cohp, coop, or cobi")
    parser = Icohplist(
        filename=resolve_input_file(inputs["integrated_bond_list"]),
        are_coops=metric == "coop",
        are_cobis=metric == "cobi",
    )
    collection = parser.icohpcollection
    minimum = float(settings["minimum_absolute_integrated_value_ev"])
    maximum = int(settings["max_bonds"])
    if minimum < 0 or maximum < 1 or maximum > 100000:
        raise ValueError("minimum absolute value must be nonnegative and max_bonds must be 1..100000")
    records = []
    for label, first, second, length, translation, multiplicity, values in zip(
        collection._list_labels,
        collection._list_atom1,
        collection._list_atom2,
        collection._list_length,
        collection._list_translation,
        collection._list_num,
        collection._list_icohp,
    ):
        selected = float(_lobster_spin_values(values, str(settings["spin"])))
        if abs(selected) < minimum:
            continue
        records.append(
            {
                "bond_label": str(label),
                "atom_a": str(first),
                "atom_b": str(second),
                "distance_angstrom": float(length),
                "cell_translation": [int(value) for value in translation],
                "equivalent_bond_count": int(multiplicity),
                "integrated_value_ev": selected,
            }
        )
    records.sort(key=lambda item: (-abs(item["integrated_value_ev"]), item["bond_label"]))
    available_count = len(records)
    records = records[:maximum]
    if bool(settings["include_curve_data"]):
        if inputs.get("bond_curve_file") is None:
            raise ValueError("include_curve_data=true requires bond_curve_file")
        curves = Cohpcar(
            filename=resolve_input_file(inputs["bond_curve_file"]),
            are_coops=metric == "coop",
            are_cobis=metric == "cobi",
        )
        energies = np.asarray(curves.energies, dtype=float)
        minimum_energy = float(settings["minimum_energy_ev"])
        maximum_energy = float(settings["maximum_energy_ev"])
        if not minimum_energy < maximum_energy:
            raise ValueError("minimum_energy_ev must be less than maximum_energy_ev")
        stride = int(settings["curve_stride"])
        max_points = int(settings["max_curve_points"])
        if stride < 1 or max_points < 2:
            raise ValueError("curve_stride must be positive and max_curve_points must be at least two")
        selected_indices = np.where(
            (energies >= minimum_energy) & (energies <= maximum_energy)
        )[0][::stride]
        if len(selected_indices) > max_points:
            raise ValueError("Explicit energy window and curve_stride produce more than max_curve_points")
        for record in records:
            value = curves.cohp_data.get(record["bond_label"])
            if value is None:
                record["curve"] = None
                continue
            record["curve"] = {
                "energy_ev_relative_to_fermi": energies[selected_indices].tolist(),
                "bonding_curve_per_ev": _lobster_spin_values(
                    value["COHP"], str(settings["spin"])
                )[selected_indices].tolist(),
                "integrated_curve_ev": _lobster_spin_values(
                    value["ICOHP"], str(settings["spin"])
                )[selected_indices].tolist(),
            }
    directory = output_directory("analyze_periodic_bonding", "lobster")
    result = {
        "bonding_metric": metric,
        "spin": str(settings["spin"]).strip().lower(),
        "bonds": records,
        "bond_count": len(records),
        "available_filtered_bond_count": available_count,
        "truncated": available_count > len(records),
        "minimum_absolute_integrated_value_ev": minimum,
        "curve_data_included": bool(settings["include_curve_data"]),
        "sign_note": "Raw LOBSTER sign convention is preserved; no bonding/antibonding sign reinterpretation is applied.",
    }
    path = write_json(directory, "periodic_bonding.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "PeriodicBondingResult",
                "media_type": "application/json",
            }
        ],
        backend_version=module_version("pymatgen"),
    )


def _lobster_projected_dos(request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    from pymatgen.io.lobster.outputs import Doscar

    inputs, _method, settings = request_parts(request)
    parser = Doscar(
        doscar=resolve_input_file(inputs["dos_file"]),
        structure_file=resolve_input_file(inputs["structure_file"]),
    )
    energies = np.asarray(parser.energies, dtype=float)
    minimum = float(settings["minimum_energy_ev"])
    maximum = float(settings["maximum_energy_ev"])
    stride = int(settings["curve_stride"])
    if not minimum < maximum or stride < 1:
        raise ValueError("DOS energy bounds must be increasing and curve_stride must be positive")
    selected = np.where((energies >= minimum) & (energies <= maximum))[0][::stride]
    if not len(selected):
        raise ValueError("The explicit DOS energy window contains no points")
    raw_projections = inputs["projections"]
    if not isinstance(raw_projections, list) or not raw_projections:
        raise ValueError("projections must be a non-empty list")
    projections = []
    for index, projection in enumerate(raw_projections):
        if not isinstance(projection, dict):
            raise ValueError("Each projection must be an object")
        atom_index = int(projection["atom_index"])
        if atom_index < 0 or atom_index >= len(parser.pdos):
            raise ValueError(f"LOBSTER projection atom_index is out of range: {atom_index}")
        orbitals = projection.get("orbitals")
        if not isinstance(orbitals, list) or not orbitals:
            raise ValueError("Each LOBSTER projection requires a non-empty orbitals list")
        available = parser.pdos[atom_index]
        unknown = [str(orbital) for orbital in orbitals if str(orbital) not in available]
        if unknown:
            raise ValueError(
                f"Unknown LOBSTER orbitals for atom {atom_index}: {unknown}; available={sorted(available)}"
            )
        density = np.sum(
            [
                _lobster_spin_values(available[str(orbital)], str(settings["spin"]))
                for orbital in orbitals
            ],
            axis=0,
        )
        projections.append(
            {
                "label": str(projection.get("label") or f"projection_{index}"),
                "atom_index": atom_index,
                "element": str(parser.completedos.structure[atom_index].specie),
                "orbitals": [str(orbital) for orbital in orbitals],
                "density_of_states_per_ev": density[selected].tolist(),
            }
        )
    result = {
        "energy_ev_relative_to_fermi": energies[selected].tolist(),
        "total_density_of_states_per_ev": _lobster_spin_values(
            parser.tdensities, str(settings["spin"])
        )[selected].tolist(),
        "projections": projections,
        "spin": str(settings["spin"]).strip().lower(),
        "fermi_energy_ev_in_source_reference": float(parser.completedos.efermi),
        "energy_reference": "fermi_zero_from_lobster",
    }
    directory = output_directory("calculate_projected_density_of_states", "lobster")
    path = write_json(directory, "projected_density_of_states.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "ProjectedDensityOfStatesResult",
                "media_type": "application/json",
            }
        ],
        backend_version=module_version("pymatgen"),
    )


def _lobster_spilling(request: dict[str, Any]) -> dict[str, Any]:
    from pymatgen.io.lobster.outputs import Lobsterout

    inputs, _method, settings = request_parts(request)
    path = resolve_input_file(inputs["lobster_output"])
    parser = Lobsterout(path)
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    charge = [100.0 * float(value) for value in parser.charge_spilling]
    total = [100.0 * float(value) for value in parser.total_spilling]
    max_charge = float(settings["maximum_charge_spilling_percent"])
    max_total = float(settings["maximum_total_spilling_percent"])
    if max_charge < 0 or max_total < 0:
        raise ValueError("Spilling thresholds must be nonnegative percentages")
    finished = bool(re.search(r"\bfinished in\b", raw_text, flags=re.IGNORECASE))
    require_finished = bool(settings["require_finished"])
    quality_pass = (
        (finished or not require_finished)
        and (not charge or max(charge) <= max_charge)
        and (not total or max(total) <= max_total)
    )
    result = {
        "quality_pass": quality_pass,
        "finished": finished,
        "charge_spilling_percent": charge,
        "total_spilling_percent": total,
        "maximum_charge_spilling_percent": max(charge) if charge else None,
        "maximum_total_spilling_percent": max(total) if total else None,
        "thresholds": {
            "charge_spilling_percent": max_charge,
            "total_spilling_percent": max_total,
            "require_finished": require_finished,
        },
        "lobster_version": str(parser.lobster_version),
        "dft_program": str(parser.dft_program),
        "spin_channels": int(parser.number_of_spins),
        "warnings": [str(value) for value in parser.warning_lines],
        "available_outputs": {
            "cohp": bool(parser.has_cohpcar),
            "coop": bool(parser.has_coopcar),
            "cobi": bool(parser.has_cobicar),
            "dos": bool(parser.has_doscar),
            "charges": bool(parser.has_charge),
            "gross_populations": bool(parser.has_grosspopulation),
        },
    }
    directory = output_directory("calculate_charge_spilling", "lobster")
    result_path = write_json(directory, "projection_quality.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(result_path),
                "semantic_type": "ProjectionQualityResult",
                "media_type": "application/json",
            }
        ],
        backend_version=str(parser.lobster_version),
    )


def _vasp_grouped_structure(
    request: dict[str, Any],
) -> tuple[
    dict[str, Any],
    list[str],
    list[list[float]],
    list[list[float]],
    list[str],
    list[int],
]:
    structure, symbols, coordinates, cell = _periodic_structure(
        request["inputs"]["structure"]
    )
    species = list(dict.fromkeys(symbols))
    order = [
        index
        for species_name in species
        for index, symbol in enumerate(symbols)
        if symbol == species_name
    ]
    return (
        structure,
        symbols,
        coordinates,
        cell,
        species,
        order,
    )


def _vasp_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return ".TRUE." if value else ".FALSE."
    if isinstance(value, (list, tuple)):
        return " ".join(_vasp_scalar(item) for item in value)
    if isinstance(value, (str, int, float)):
        return str(value)
    raise ValueError(f"Unsupported INCAR value type: {type(value).__name__}")


def _write_vasp_inputs(
    action_id: str,
    request: dict[str, Any],
    directory: Path,
) -> tuple[list[str], list[int]]:
    (
        _structure,
        symbols,
        coordinates,
        cell,
        species,
        order,
    ) = _vasp_grouped_structure(request)
    method = request["method_spec"]
    settings = request["action_settings"]

    counts = [symbols.count(item) for item in species]
    poscar_lines = ["ResearchChemBench", "1.0"]
    poscar_lines.extend(" ".join(f"{value:.16g}" for value in row) for row in cell)
    poscar_lines.extend([" ".join(species), " ".join(str(item) for item in counts), "Cartesian"])
    poscar_lines.extend(
        " ".join(f"{value:.16g}" for value in coordinates[index]) for index in order
    )
    (directory / "POSCAR").write_text("\n".join(poscar_lines) + "\n", encoding="utf-8")

    mapping = dict(method["pseudopotentials"])
    missing = sorted(set(species) - set(mapping))
    if missing:
        raise ValueError(f"Missing VASP POTCAR resources for elements: {missing}")
    with (directory / "POTCAR").open("wb") as output:
        for element in species:
            selected = mapping[element]
            if is_resource_reference(selected):
                metadata = resource_reference_metadata(selected)
                if (
                    metadata.get("kind") == "variant_file_collection"
                    and metadata.get("element") != element
                ):
                    raise ValueError(
                        f"VASP POTCAR selection {metadata.get('selection')!r} belongs "
                        f"to element {metadata.get('element')!r}, not {element!r}"
                    )
            source = resolve_input_file(selected)
            dataset = source.read_bytes()
            output.write(dataset)
            if not dataset.endswith((b"\n", b"\r")):
                output.write(b"\n")

    k_points = _k_points(method["k_points"])
    scheme = str(method["kpoint_scheme"]).strip().lower()
    if scheme not in {"gamma", "monkhorst-pack"}:
        raise ValueError("kpoint_scheme must be gamma or monkhorst-pack")
    kpoint_lines = [
        "ResearchChemBench",
        "0",
        "Gamma" if scheme == "gamma" else "Monkhorst-Pack",
        " ".join(str(item) for item in k_points[:3]),
        " ".join(str(item) for item in k_points[3:]),
    ]
    (directory / "KPOINTS").write_text("\n".join(kpoint_lines) + "\n", encoding="utf-8")

    incar: dict[str, Any] = {
        "SYSTEM": "ResearchChemBench",
        "ENCUT": float(method["encut_ev"]),
        "PREC": str(method["precision"]),
        "ALGO": str(method["algorithm"]),
        "EDIFF": float(settings["scf_convergence_ev"]),
        "NELM": int(settings["max_scf_cycles"]),
        "ISMEAR": int(method["ismear"]),
        "SIGMA": float(method["sigma_ev"]),
        "ISPIN": 2 if bool(method["spin_polarized"]) else 1,
        "LREAL": method["real_space_projection"],
        "LWAVE": False,
        "LCHARG": False,
        "IBRION": -1,
        "NSW": 0,
    }
    xc_family = str(method["xc_family"]).strip().lower()
    if xc_family == "pbe":
        incar["GGA"] = "PE"
    elif xc_family == "pbesol":
        incar["GGA"] = "PS"
    elif xc_family == "lda":
        pass
    elif xc_family in {"scan", "r2scan"}:
        incar["METAGGA"] = xc_family.upper()
        incar["LASPH"] = True
    else:
        raise ValueError("xc_family must be lda, pbe, pbesol, scan, or r2scan")
    if method.get("initial_magnetic_moments") is not None:
        moments = list(method["initial_magnetic_moments"])
        if len(moments) != len(symbols):
            raise ValueError("initial_magnetic_moments must have one value per atom")
        incar["MAGMOM"] = [moments[index] for index in order]
    if method.get("electron_count") is not None:
        incar["NELECT"] = float(method["electron_count"])
    if action_id == "relax_periodic_structure":
        incar.update(
            {
                "IBRION": 2,
                "NSW": int(settings["max_steps"]),
                "EDIFFG": -abs(float(settings["force_threshold_ev_per_angstrom"])),
                "ISIF": 3 if bool(settings["relax_cell"]) else 2,
            }
        )
    protected = {"IBRION", "NSW", "EDIFFG", "ISIF"}
    for raw_key, value in dict(method.get("additional_incar") or {}).items():
        key = str(raw_key).strip().upper()
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
            raise ValueError(f"Invalid INCAR key: {raw_key!r}")
        if key in protected:
            raise ValueError(
                f"additional_incar cannot override action-semantic key {key}"
            )
        incar[key] = value
    (directory / "INCAR").write_text(
        "\n".join(f"{key} = {_vasp_scalar(value)}" for key, value in incar.items()) + "\n",
        encoding="utf-8",
    )
    return symbols, order


def _parse_vasp_result(
    action_id: str,
    directory: Path,
    request: dict[str, Any],
    symbols: list[str],
    order: list[int],
) -> dict[str, Any]:
    outcar_path = directory / "OUTCAR"
    if not outcar_path.is_file():
        raise RuntimeError("VASP completed without OUTCAR")
    outcar = outcar_path.read_text(encoding="utf-8", errors="replace")
    number = r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?"
    energy_matches = re.findall(
        rf"free\s+energy\s+TOTEN\s*=\s*({number})\s+eV", outcar, flags=re.I
    )
    energy = (
        float(energy_matches[-1].replace("D", "E").replace("d", "e"))
        if energy_matches
        else None
    )
    if action_id == "calculate_periodic_energy":
        if energy is None:
            raise RuntimeError("Could not parse VASP TOTEN")
        return {"energy": energy, "unit": "eV"}

    if action_id == "calculate_periodic_forces":
        matches = list(
            re.finditer(
                r"TOTAL-FORCE \(eV/Angst\)\s*-+\s*(.*?)(?:\n\s*--+|\n\s*total drift)",
                outcar,
                flags=re.S | re.I,
            )
        )
        if not matches:
            raise RuntimeError("Could not parse VASP force block")
        grouped = []
        for line in matches[-1].group(1).splitlines():
            values = _numeric_tokens(line)
            if len(values) >= 6:
                grouped.append(values[-3:])
        if len(grouped) != len(symbols):
            raise RuntimeError("VASP force count does not match input atom count")
        forces: list[list[float] | None] = [None] * len(symbols)
        for grouped_index, original_index in enumerate(order):
            forces[original_index] = grouped[grouped_index]
        return {
            "forces": forces,
            "unit": "eV/angstrom",
            "energy_ev": energy,
        }

    if action_id == "calculate_periodic_stress":
        stress_matches = re.findall(
            rf"in kB\s+({number})\s+({number})\s+({number})\s+({number})\s+({number})\s+({number})",
            outcar,
            flags=re.I,
        )
        if not stress_matches:
            raise RuntimeError("Could not parse VASP stress tensor")
        xx, yy, zz, xy, yz, zx = [
            float(value.replace("D", "E").replace("d", "e"))
            for value in stress_matches[-1]
        ]
        return {
            "stress": [[xx, xy, zx], [xy, yy, yz], [zx, yz, zz]],
            "unit": "kilobar",
            "sign_convention": "VASP OUTCAR in-kB convention",
            "energy_ev": energy,
        }

    contcar = directory / "CONTCAR"
    relaxed = None
    if contcar.is_file() and contcar.stat().st_size:
        from ase.io import read

        atoms = read(str(contcar), format="vasp")
        grouped_positions = atoms.get_positions().tolist()
        positions: list[list[float] | None] = [None] * len(symbols)
        for grouped_index, original_index in enumerate(order):
            positions[original_index] = grouped_positions[grouped_index]
        original = structure_dict(request["inputs"]["structure"])
        relaxed = {
            "atoms": [
                {"element": symbol, "position_angstrom": positions[index]}
                for index, symbol in enumerate(symbols)
            ],
            "cell_angstrom": atoms.cell.array.tolist(),
            "pbc": [True, True, True],
            "charge": int(original.get("charge", 0)),
            "multiplicity": int(original.get("multiplicity", 1)),
        }
    return {
        "structure": relaxed,
        "converged": "reached required accuracy" in outcar.lower(),
        "energy_ev": energy,
    }


def _run_vasp(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    directory = output_directory(action_id, "vasp")
    symbols, order = _write_vasp_inputs(action_id, request, directory)
    cores = max(1, int(request.get("resource_limits", {}).get("cpu_cores") or 1))
    if cores == 1:
        completed = run_external(
            executable="vasp_std",
            environment_variable="CHEMGRAPH_VASP_COMMAND",
            arguments=[],
            directory=directory,
            timeout_seconds=int(
                request.get("resource_limits", {}).get("walltime_seconds", 7200)
            ),
        )
    else:
        vasp_command = resolve_command("vasp_std", "CHEMGRAPH_VASP_COMMAND")
        if not vasp_command:
            completed = {
                "available": False,
                "returncode": None,
                "stdout": "",
                "stderr": "VASP executable was not found",
                "command": ["vasp_std"],
            }
        else:
            completed = run_external(
                executable="mpirun",
                environment_variable="CHEMGRAPH_VASP_MPI_COMMAND",
                arguments=["-np", str(cores), *vasp_command],
                directory=directory,
                timeout_seconds=int(
                    request.get("resource_limits", {}).get("walltime_seconds", 7200)
                ),
            )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    # POTCAR content is licensed input data and must not be returned as an output artifact.
    (directory / "POTCAR").unlink(missing_ok=True)
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Configure licensed VASP locally")
    if completed["returncode"] != 0:
        raise RuntimeError(
            "VASP failed: " + (completed["stderr"] or completed["stdout"])[-2000:]
        )
    result = _parse_vasp_result(action_id, directory, request, symbols, order)
    provenance = {
        "command": completed["command"],
        "mpi_processes": cores,
        "parallel_processes": cores,
    }
    artifacts = command_artifacts(directory)
    if action_id == "relax_periodic_structure" and (
        result.get("structure") is None or not result.get("converged")
    ):
        return partial_success(
            result,
            artifact_files=artifacts,
            provenance=provenance,
            backend_version="6.3.2",
            warnings=[
                "VASP completed, but the relaxed structure was not both parsed and converged."
            ],
        )
    return success(
        result,
        artifact_files=artifacts,
        provenance=provenance,
        backend_version="6.3.2",
    )


def _shengbte_thermal_conductivity(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    solution = str(settings["solution_method"]).strip().lower()
    if solution not in {"rta", "iterative"}:
        raise ValueError("solution_method must be rta or iterative")
    maximum_records = int(settings["maximum_temperature_records"])
    if not 1 <= maximum_records <= 10000:
        raise ValueError("maximum_temperature_records must be between 1 and 10000")
    require_normal_exit = settings["require_normal_exit"]
    if not isinstance(require_normal_exit, bool):
        raise ValueError("require_normal_exit must be an explicit boolean")

    directory = output_directory("calculate_lattice_thermal_conductivity", "shengbte")
    staged: list[dict[str, str]] = []
    names = {
        "control_file": "CONTROL",
        "second_order_force_constants_file": "FORCE_CONSTANTS_2ND",
        "third_order_force_constants_file": "FORCE_CONSTANTS_3RD",
    }
    if inputs.get("born_file") is not None:
        names["born_file"] = "BORN"
    occupied = set(names.values())
    for field, target_name in names.items():
        source = resolve_input_file(inputs[field])
        if not source.is_file():
            raise ValueError(f"{field} must resolve to one regular file")
        target = directory / target_name
        shutil.copy2(source, target)
        staged.append(
            {
                "field": field,
                "source": relative_workspace_path(source),
                "staged_name": target_name,
            }
        )
    companions = inputs.get("companion_files", [])
    if not isinstance(companions, list) or len(companions) > 64:
        raise ValueError("companion_files must be a list containing at most 64 files")
    for index, value in enumerate(companions):
        source = resolve_input_file(value)
        if not source.is_file():
            raise ValueError(f"companion_files[{index}] must resolve to one regular file")
        name = source.name
        if name in occupied:
            raise ValueError(f"Duplicate staged ShengBTE file name: {name}")
        occupied.add(name)
        shutil.copy2(source, directory / name)
        staged.append(
            {
                "field": f"companion_files[{index}]",
                "source": relative_workspace_path(source),
                "staged_name": name,
            }
        )

    completed = run_external(
        executable="ShengBTE",
        environment_variable="CHEMGRAPH_SHENGBTE_COMMAND",
        arguments=[],
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Configure the ShengBTE executable")
    if completed["returncode"] != 0:
        raise RuntimeError(f"ShengBTE failed: {completed['stderr'][-2000:]}")

    output_name = (
        "BTE.KappaTensorVsT_RTA"
        if solution == "rta"
        else "BTE.KappaTensorVsT_CONV"
    )
    conductivity_path = directory / output_name
    records: list[dict[str, Any]] = []
    total = 0
    if conductivity_path.is_file():
        for line in conductivity_path.read_text(encoding="utf-8", errors="replace").splitlines():
            tokens = line.split()
            if len(tokens) < 10:
                continue
            try:
                values = [
                    float(token.replace("D", "E").replace("d", "e"))
                    for token in tokens[:10]
                ]
            except ValueError:
                continue
            total += 1
            if len(records) >= maximum_records:
                continue
            records.append(
                {
                    "temperature_kelvin": values[0],
                    "kappa_w_mk": [values[1:4], values[4:7], values[7:10]],
                }
            )
    normal_exit = "normal exit" in (
        completed["stdout"] + "\n" + completed["stderr"]
    ).lower()
    result = {
        "solution_method": solution,
        "conductivity_records": records,
        "temperature_record_count": total,
        "truncated": total > len(records),
        "tensor_unit": "W m^-1 K^-1",
        "tensor_order": "row-major Cartesian 3x3",
        "normal_exit": normal_exit,
        "staged_inputs": staged,
        "native_control_preserved": True,
    }
    summary = write_json(directory, "lattice_thermal_conductivity.json", result)
    summary_path = relative_workspace_path(summary)
    artifacts = [
        item for item in command_artifacts(directory) if item["path"] != summary_path
    ]
    artifacts.append(
        {
            "path": summary_path,
            "semantic_type": "LatticeThermalConductivityResult",
            "media_type": "application/json",
        }
    )
    warnings = []
    for line in (completed["stdout"] + "\n" + completed["stderr"]).splitlines():
        if "warning" in line.lower() and line.strip() not in warnings:
            warnings.append(line.strip()[:1000])
        if len(warnings) >= 40:
            break
    common = {
        "artifact_files": artifacts,
        "backend_version": "source-b0d2090",
        "provenance": {
            "command": completed["command"],
            "automatic_model_construction": False,
            "native_control_preserved": True,
        },
    }
    if not records or (require_normal_exit and not normal_exit):
        return partial_success(
            result,
            **common,
            warnings=[
                *warnings,
                "ShengBTE completed without the requested validated conductivity output.",
            ],
        )
    return success(result, **common, warnings=warnings)


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "yambo" and action_id in {
        "calculate_quasiparticle_corrections", "calculate_bse_optical_spectrum"
    }:
        return _run_yambo(action_id, request)
    if backend_id == "internal_periodic_analysis":
        if action_id == "calculate_adsorption_energy":
            return _calculate_adsorption_energy(request)
        if action_id == "construct_pressure_enthalpy_phase_diagram":
            return _construct_pressure_enthalpy_phase_diagram(request)
        if action_id == "assess_phonon_stability":
            return _assess_phonon_stability(request)
    if backend_id == "vaspkit" and action_id in {"generate_vasp_kpoint_mesh", "extract_vasp_band_gap"}:
        return _run_vaspkit_action(action_id, request)
    if backend_id == "airss":
        return _run_airss(action_id, request)
    if backend_id == "tdep":
        return _run_tdep(action_id, request)
    if backend_id == "lobster":
        if action_id == "analyze_periodic_bonding":
            return _lobster_bonding(request)
        if action_id == "calculate_projected_density_of_states":
            return _lobster_projected_dos(request)
        if action_id == "calculate_charge_spilling":
            return _lobster_spilling(request)
    if backend_id == "gpaw":
        from .gpaw_adapter import execute as execute_gpaw

        return execute_gpaw(action_id, request)
    if backend_id == "quantum_espresso":
        return _run_qe(action_id, request)
    if backend_id == "cp2k":
        return _run_cp2k(action_id, request)
    if backend_id in {"siesta", "dftbplus", "abinit"}:
        return _run_simple_periodic(backend_id, action_id, request)
    if backend_id == "vasp":
        return _run_vasp(action_id, request)
    if backend_id in {"nequip", "allegro", "deepmd"}:
        return _run_mlip_periodic(backend_id, action_id, request)
    if backend_id in {"phonopy", "phono3py"}:
        return _phonons(action_id, backend_id, request)
    if backend_id == "shengbte" and action_id == "calculate_lattice_thermal_conductivity":
        return _shengbte_thermal_conductivity(request)
    return unsupported(f"Unsupported periodic action/backend combination: {action_id}/{backend_id}")

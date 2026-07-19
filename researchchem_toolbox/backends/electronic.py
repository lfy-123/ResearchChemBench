"""Molecular electronic-structure and derived-property actions."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .common import (
    ase_atoms,
    atom_spec,
    command_artifacts,
    module_version,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    run_external,
    structure_dict,
    structure_from_atoms,
    success,
    unavailable,
    unsupported,
    write_json,
    write_xyz,
)
from .mlip import build_calculator as build_mlip_calculator
from .mlip import prepare_atoms as prepare_mlip_atoms
from .quantum_legacy import gamess as _gamess
from .quantum_legacy import gaussian as _gaussian


ACTIONS = {
    "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
    "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals",
    "derive_vibrational_modes", "derive_ir_spectrum", "derive_thermochemistry",
}


def _ase_calculator(backend_id: str, method: dict[str, Any]):
    if backend_id == "ase_emt":
        from ase.calculators.emt import EMT

        return EMT(), module_version("ase")
    if backend_id == "tblite":
        from tblite.ase import TBLite

        name = str(method["method"]).lower().replace("_", "-")
        normalized = {"gfn1": "GFN1-xTB", "gfn1-xtb": "GFN1-xTB", "gfn2": "GFN2-xTB", "gfn2-xtb": "GFN2-xTB"}.get(name)
        if normalized is None:
            raise ValueError("TBLite method must be gfn1 or gfn2")
        return TBLite(method=normalized), module_version("tblite")
    if backend_id == "mace":
        from mace.calculators import mace_mp

        model = str(method["model"])
        allow_download = bool(method.get("allow_model_download", False))
        if not Path(model).expanduser().is_file() and not allow_download:
            raise RuntimeError(
                "MACE model is not a local file and allow_model_download was not explicitly true"
            )
        return (
            mace_mp(
                model=model,
                device=str(method["device"]),
                default_dtype=str(method.get("default_dtype", "float64")),
            ),
            module_version("mace-torch"),
        )
    if backend_id == "chgnet":
        from chgnet.model.dynamics import CHGNetCalculator

        if not bool(method.get("allow_model_download", False)):
            raise RuntimeError("CHGNet pretrained loading requires allow_model_download=true")
        return CHGNetCalculator(use_device=str(method["device"])), module_version("chgnet")
    if backend_id == "deepmd":
        calculator, version, _provenance = build_mlip_calculator(backend_id, method)
        return calculator, version
    raise ValueError(f"No ASE calculator implementation for {backend_id}")


def _ase_property(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, method, settings = request_parts(request)
    atoms = ase_atoms(inputs["structure"])
    prepare_mlip_atoms(backend_id, atoms, method)
    calculator, version = _ase_calculator(backend_id, method)
    atoms.calc = calculator
    if action_id == "calculate_energy":
        return success(
            {"energy": float(atoms.get_potential_energy()), "unit": "eV", "atom_count": len(atoms)},
            backend_version=version,
        )
    if action_id == "calculate_forces":
        forces = np.asarray(atoms.get_forces(), dtype=float)
        return success(
            {"forces": forces.tolist(), "unit": "eV/angstrom", "atom_count": len(atoms)},
            backend_version=version,
        )
    if action_id == "calculate_dipole_moment":
        dipole = np.asarray(atoms.get_dipole_moment(), dtype=float)
        return success({"dipole": dipole.tolist(), "unit": "e*angstrom"}, backend_version=version)
    if action_id == "optimize_geometry":
        from ase.optimize import BFGS, FIRE, LBFGS

        directory = output_directory(action_id, backend_id)
        optimizer_name = str(settings.get("optimizer", "bfgs")).lower()
        optimizer_class = {"bfgs": BFGS, "lbfgs": LBFGS, "fire": FIRE}.get(optimizer_name)
        if optimizer_class is None:
            raise ValueError("optimizer must be bfgs, lbfgs, or fire")
        log_path = directory / "optimization.log"
        trajectory_path = directory / "optimization.traj"
        optimizer = optimizer_class(atoms, logfile=str(log_path), trajectory=str(trajectory_path))
        converged = bool(
            optimizer.run(
                fmax=float(settings["fmax_ev_per_angstrom"]),
                steps=int(settings.get("max_steps", 500)),
            )
        )
        xyz_path = directory / "optimized.xyz"
        from ase.io import write

        write(str(xyz_path), atoms)
        result = {
            "structure": structure_from_atoms(atoms),
            "converged": converged,
            "energy": float(atoms.get_potential_energy()),
            "energy_unit": "eV",
            "optimizer": optimizer_name,
        }
        if not converged:
            return partial_success(
                result,
                artifact_files=command_artifacts(directory),
                backend_version=version,
                warnings=["Geometry optimization reached its step limit before convergence."],
            )
        return success(
            result,
            artifact_files=command_artifacts(directory),
            backend_version=version,
        )
    if action_id == "calculate_hessian":
        displacement = float(settings.get("displacement_angstrom", 0.01))
        if displacement <= 0:
            raise ValueError("displacement_angstrom must be positive")
        coordinates = atoms.get_positions().copy()
        dimensions = 3 * len(atoms)
        hessian = np.zeros((dimensions, dimensions), dtype=float)
        for column in range(dimensions):
            atom_index, axis = divmod(column, 3)
            plus = coordinates.copy()
            minus = coordinates.copy()
            plus[atom_index, axis] += displacement
            minus[atom_index, axis] -= displacement
            atoms.set_positions(plus)
            forces_plus = np.asarray(atoms.get_forces(), dtype=float).reshape(-1)
            atoms.set_positions(minus)
            forces_minus = np.asarray(atoms.get_forces(), dtype=float).reshape(-1)
            hessian[:, column] = -(forces_plus - forces_minus) / (2 * displacement)
        atoms.set_positions(coordinates)
        hessian = 0.5 * (hessian + hessian.T)
        return success(
            {"matrix": hessian.tolist(), "unit": "eV/angstrom^2", "displacement_angstrom": displacement},
            backend_version=version,
        )
    return unsupported(f"ASE calculator does not implement {action_id}")


def _xtb(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, method, settings = request_parts(request)
    directory = output_directory(action_id, "xtb")
    xyz = write_xyz(inputs["structure"], directory / "input.xyz")
    structure = structure_dict(inputs["structure"])
    method_name = str(method["method"]).lower().replace("-", "")
    method_number = {"gfn1": "1", "gfn1xtb": "1", "gfn2": "2", "gfn2xtb": "2"}.get(method_name)
    if method_number is None:
        raise ValueError("xTB method must be gfn1 or gfn2")
    charge = int(method.get("charge", structure.get("charge", 0)))
    unpaired = int(method.get("unpaired_electrons", max(0, int(structure.get("multiplicity", 1)) - 1)))
    arguments = [str(xyz), "--gfn", method_number, "--chrg", str(charge), "--uhf", str(unpaired)]
    if action_id == "optimize_geometry":
        arguments.extend(["--opt", str(settings["optimization_level"])])
    elif action_id == "calculate_hessian":
        arguments.append("--hess")
    completed = run_external(
        executable="xtb",
        environment_variable="CHEMGRAPH_XTB_COMMAND",
        arguments=arguments,
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge xtb")
    if completed["returncode"] != 0:
        raise RuntimeError(f"xTB failed: {completed['stderr'][-2000:]}")
    energy_matches = re.findall(r"TOTAL ENERGY\s+(-?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)", completed["stdout"])
    energy = float(energy_matches[-1]) if energy_matches else None
    if action_id == "calculate_energy":
        if energy is None:
            raise RuntimeError("Could not parse xTB TOTAL ENERGY")
        result = {"energy": energy, "unit": "hartree", "method": f"gfn{method_number}"}
    elif action_id == "optimize_geometry":
        optimized = directory / "xtbopt.xyz"
        if not optimized.is_file():
            raise RuntimeError("xTB optimization completed without xtbopt.xyz")
        result = {
            "structure": structure_dict(relative_workspace_path(optimized)),
            "converged": True,
            "energy": energy,
            "energy_unit": "hartree",
            "optimization_level": str(settings["optimization_level"]),
        }
    elif action_id == "calculate_hessian":
        hessian_path = directory / "hessian"
        if not hessian_path.is_file():
            raise RuntimeError("xTB Hessian calculation completed without hessian file")
        values = []
        for token in hessian_path.read_text(encoding="utf-8").replace("D", "E").split():
            try:
                values.append(float(token))
            except ValueError:
                continue
        dimensions = 3 * len(structure.get("atoms") or structure.get("symbols") or [])
        if dimensions and len(values) >= dimensions * dimensions:
            matrix = np.asarray(values[-dimensions * dimensions :]).reshape(dimensions, dimensions).tolist()
        else:
            matrix = None
        result = {
            "matrix": matrix,
            "unit": "hartree/bohr^2",
            "raw_hessian_path": relative_workspace_path(hessian_path),
        }
    else:
        return unsupported(f"xTB does not implement {action_id}")
    if action_id == "calculate_hessian" and result.get("matrix") is None:
        return partial_success(
            result,
            artifact_files=command_artifacts(directory),
            provenance={"command": completed["command"]},
            warnings=["xTB produced a Hessian file, but the dense Hessian matrix could not be parsed."],
        )
    return success(result, artifact_files=command_artifacts(directory), provenance={"command": completed["command"]})


def _pyscf(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    from pyscf import dft, gto, scf

    inputs, method, settings = request_parts(request)
    structure = structure_dict(inputs["structure"])
    method_name = str(method["method"]).lower()
    molecule = gto.M(
        atom=atom_spec(inputs["structure"]),
        basis=str(method["basis"]),
        charge=int(method.get("charge", structure.get("charge", 0))),
        spin=int(method.get("spin", max(0, int(structure.get("multiplicity", 1)) - 1))),
        unit="Angstrom",
        verbose=0,
    )
    classes = {"rhf": scf.RHF, "uhf": scf.UHF, "rks": dft.RKS, "uks": dft.UKS}
    if method_name not in classes:
        raise ValueError("PySCF method must be rhf, uhf, rks, or uks")
    calculation = classes[method_name](molecule)
    if method_name in {"rks", "uks"}:
        functional = method.get("functional") or method.get("xc")
        if not functional:
            raise ValueError("PySCF RKS/UKS requires an explicit functional in method_spec")
        calculation.xc = str(functional)
    calculation.conv_tol = float(settings.get("scf_convergence", 1e-9))
    energy = float(calculation.kernel())
    common = {
        "converged": bool(calculation.converged),
        "method": method_name,
        "basis": str(method["basis"]),
        "energy_hartree": energy,
    }
    if action_id == "calculate_energy":
        result = {**common, "energy": energy, "unit": "hartree"}
    elif action_id == "calculate_dipole_moment":
        dipole = calculation.dip_moment(mol=molecule, dm=calculation.make_rdm1(), unit="Debye", verbose=0)
        result = {**common, "dipole": np.asarray(dipole, dtype=float).tolist(), "unit": "debye"}
    elif action_id == "calculate_atomic_charges":
        population, charges = calculation.mulliken_pop(molecule, calculation.make_rdm1(), verbose=0)
        result = {
            **common,
            "analysis": str(method.get("population_analysis", "mulliken")),
            "charges": np.asarray(charges, dtype=float).tolist(),
            "unit": "elementary_charge",
            "orbital_populations": np.asarray(population, dtype=float).tolist(),
        }
    elif action_id == "calculate_orbitals":
        energies = calculation.mo_energy
        occupations = calculation.mo_occ
        if isinstance(energies, tuple):
            result = {
                **common,
                "alpha_energies_hartree": np.asarray(energies[0]).tolist(),
                "beta_energies_hartree": np.asarray(energies[1]).tolist(),
                "alpha_occupations": np.asarray(occupations[0]).tolist(),
                "beta_occupations": np.asarray(occupations[1]).tolist(),
            }
        else:
            result = {
                **common,
                "energies_hartree": np.asarray(energies).tolist(),
                "occupations": np.asarray(occupations).tolist(),
            }
        if bool(settings.get("include_coefficients", False)):
            result["coefficients"] = np.asarray(calculation.mo_coeff).tolist()
    else:
        return unsupported(f"PySCF does not implement {action_id}")
    return success(result, backend_version=module_version("pyscf"))


def _psi4_geometry(structure_value: Any) -> str:
    structure = structure_dict(structure_value)
    symbols = []
    coordinates = []
    if "atoms" in structure:
        for atom in structure["atoms"]:
            symbols.append(atom["element"])
            coordinates.append(atom["position_angstrom"])
    else:
        symbols = structure["symbols"]
        coordinates = structure.get("coordinates_angstrom") or structure["positions"]
    charge = int(structure.get("charge", 0))
    multiplicity = int(structure.get("multiplicity", 1))
    lines = [f"{charge} {multiplicity}"]
    lines.extend(f"{s} {r[0]} {r[1]} {r[2]}" for s, r in zip(symbols, coordinates))
    lines.append("units angstrom")
    lines.append("no_reorient")
    lines.append("no_com")
    return "\n".join(lines)


def _psi4(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    import psi4

    inputs, method, settings = request_parts(request)
    directory = output_directory(action_id, "psi4")
    output_path = directory / "psi4.out"
    psi4.core.clean()
    psi4.set_memory(f"{int(request.get('resource_limits', {}).get('memory_mb') or 1000)} MB")
    psi4.set_num_threads(int(request.get("resource_limits", {}).get("cpu_cores") or 1))
    psi4.core.set_output_file(str(output_path), False)
    molecule = psi4.geometry(_psi4_geometry(inputs["structure"]))
    model = f"{method['method']}/{method['basis']}"
    psi4.set_options(dict(method.get("options") or {}))
    if action_id == "calculate_hessian":
        matrix = np.asarray(psi4.hessian(model, molecule=molecule), dtype=float)
        result = {"matrix": matrix.tolist(), "unit": "hartree/bohr^2", "model": model}
    else:
        energy, wavefunction = psi4.energy(model, molecule=molecule, return_wfn=True)
        common = {"energy_hartree": float(energy), "model": model}
        if action_id == "calculate_energy":
            result = {**common, "energy": float(energy), "unit": "hartree"}
        elif action_id == "calculate_dipole_moment":
            psi4.oeprop(wavefunction, "DIPOLE")
            dipole = [float(psi4.core.variable(f"SCF DIPOLE {axis}")) for axis in ("X", "Y", "Z")]
            result = {**common, "dipole": dipole, "unit": "debye"}
        elif action_id == "calculate_atomic_charges":
            psi4.oeprop(wavefunction, "MULLIKEN_CHARGES")
            charges = np.asarray(wavefunction.atomic_point_charges(), dtype=float).tolist()
            result = {**common, "charges": charges, "analysis": "mulliken", "unit": "elementary_charge"}
        elif action_id == "calculate_orbitals":
            result = {
                **common,
                "alpha_energies_hartree": np.asarray(wavefunction.epsilon_a()).reshape(-1).tolist(),
                "alpha_occupations": [2.0 if i < wavefunction.nalpha() else 0.0 for i in range(wavefunction.nmo())],
            }
            if wavefunction.same_a_b_orbs() is False:
                result["beta_energies_hartree"] = np.asarray(wavefunction.epsilon_b()).reshape(-1).tolist()
                result["beta_occupations"] = [1.0 if i < wavefunction.nbeta() else 0.0 for i in range(wavefunction.nmo())]
        else:
            return unsupported(f"Psi4 does not implement {action_id}")
    result_path = write_json(directory, "result.json", result)
    return success(
        result,
        artifact_files=[
            {"path": relative_workspace_path(output_path), "semantic_type": "BackendOutput", "media_type": "text/plain"},
            {"path": relative_workspace_path(result_path), "semantic_type": "ElectronicResult", "media_type": "application/json"},
        ],
        backend_version=module_version("psi4"),
    )


def _render_orca(
    action_id: str,
    structure_value: Any,
    method: dict[str, Any],
    settings: dict[str, Any],
    resource_limits: dict[str, Any] | None = None,
) -> str:
    structure = structure_dict(structure_value)
    symbols = [atom["element"] for atom in structure["atoms"]]
    coordinates = [atom["position_angstrom"] for atom in structure["atoms"]]
    keyword = {
        "calculate_energy": "SP",
        "calculate_hessian": "Freq",
        "optimize_geometry": "Opt",
        "calculate_dipole_moment": "SP",
    }[action_id]
    header = f"! {method['method']} {method['basis']} {keyword}"
    if method.get("dispersion"):
        header += f" {method['dispersion']}"
    charge = int(method.get("charge", structure.get("charge", 0)))
    multiplicity = int(method.get("multiplicity", structure.get("multiplicity", 1)))
    lines = [header]
    parallel_processes = int((resource_limits or {}).get("cpu_cores") or 1)
    if parallel_processes > 1:
        lines.extend(["%pal", f"  nprocs {parallel_processes}", "end"])
    if action_id == "optimize_geometry":
        lines.extend(
            [
                "%geom",
                f"  Convergence {settings['optimization_convergence']}",
                f"  MaxIter {int(settings['max_steps'])}",
                "end",
            ]
        )
    lines.append(f"* xyz {charge} {multiplicity}")
    lines.extend(f"{s} {r[0]} {r[1]} {r[2]}" for s, r in zip(symbols, coordinates))
    lines.append("*")
    return "\n".join(lines) + "\n"


def _parse_orca_hessian(path: Path) -> list[list[float]] | None:
    """Parse ORCA's block-column $hessian section into a dense matrix."""

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    try:
        section = next(index for index, line in enumerate(lines) if line.strip().lower() == "$hessian")
        dimension = int(lines[section + 1].strip())
    except (StopIteration, ValueError, IndexError):
        return None
    matrix = [[0.0 for _ in range(dimension)] for _ in range(dimension)]
    populated: set[tuple[int, int]] = set()
    columns: list[int] = []
    for line in lines[section + 2 :]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("$"):
            break
        parts = stripped.split()
        if parts and all(part.isdigit() for part in parts):
            columns = [int(part) for part in parts]
            continue
        if not columns or not parts[0].isdigit():
            continue
        row = int(parts[0])
        if row >= dimension:
            continue
        values = parts[1:]
        for column, value in zip(columns, values):
            if column >= dimension:
                continue
            try:
                matrix[row][column] = float(value.replace("D", "E").replace("d", "e"))
            except ValueError:
                return None
            populated.add((row, column))
    return matrix if len(populated) == dimension * dimension else None


def _orca(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    directory = output_directory(action_id, "orca")
    input_path = directory / "job.inp"
    input_path.write_text(
        _render_orca(
            action_id,
            inputs["structure"],
            method,
            settings,
            dict(request.get("resource_limits") or {}),
        ),
        encoding="utf-8",
    )
    completed = run_external(
        executable="orca", environment_variable="CHEMGRAPH_ORCA_COMMAND",
        arguments=[str(input_path)], directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    output_path = directory / "job.out"
    output_path.write_text(completed["stdout"], encoding="utf-8")
    (directory / "job.err").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install=(
                "Place the licensed ORCA bundle in .software_cache/orca/6.1.1 "
                "and configure CHEMGRAPH_ORCA_COMMAND."
            ),
        )
    if completed["returncode"] != 0:
        detail = (completed["stderr"] or completed["stdout"])[-4000:]
        raise RuntimeError(f"ORCA failed: {detail}")
    version_match = re.search(r"Program Version\s+(\d+\.\d+\.\d+)", completed["stdout"])
    backend_version = version_match.group(1) if version_match else None
    energy_matches = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+(?:\.\d+)?)", completed["stdout"])
    energy = float(energy_matches[-1]) if energy_matches else None
    if action_id == "calculate_energy":
        if energy is None:
            raise RuntimeError("Could not parse ORCA final energy")
        result = {"energy": energy, "unit": "hartree"}
    elif action_id == "calculate_dipole_moment":
        match = re.search(
            r"Total Dipole Moment\s*:\s*(-?\S+)\s+(-?\S+)\s+(-?\S+)", completed["stdout"]
        )
        if not match:
            raise RuntimeError("Could not parse ORCA dipole moment")
        result = {"dipole": [float(match.group(i)) for i in (1, 2, 3)], "unit": "atomic_unit", "energy_hartree": energy}
    elif action_id == "optimize_geometry":
        final_xyz = directory / f"{input_path.stem}.xyz"
        if not final_xyz.is_file():
            candidates = sorted(
                path for path in directory.glob("*.xyz") if not path.name.endswith("_trj.xyz")
            )
            final_xyz = candidates[-1] if candidates else final_xyz
        if not final_xyz.is_file():
            raise RuntimeError("ORCA optimization produced no XYZ structure")
        result = {
            "structure": structure_dict(relative_workspace_path(final_xyz)),
            "converged": "THE OPTIMIZATION HAS CONVERGED" in completed["stdout"],
            "energy": energy,
            "energy_unit": "hartree",
            "optimization_convergence": str(settings["optimization_convergence"]),
        }
    elif action_id == "calculate_hessian":
        hess_files = list(directory.glob("*.hess"))
        if not hess_files:
            raise RuntimeError("ORCA frequency job produced no .hess file")
        matrix = _parse_orca_hessian(hess_files[-1])
        result = {
            "matrix": matrix,
            "unit": "hartree/bohr^2",
            "raw_hessian_path": relative_workspace_path(hess_files[-1]),
        }
    else:
        return unsupported(f"ORCA does not implement {action_id}")
    artifacts = command_artifacts(directory)
    provenance = {
        "command": completed["command"],
        "parallel_processes": int(
            (request.get("resource_limits") or {}).get("cpu_cores") or 1
        ),
    }
    incomplete = (
        (action_id == "calculate_hessian" and result.get("matrix") is None)
        or (action_id == "optimize_geometry" and not result.get("converged"))
    )
    if incomplete:
        return partial_success(
            result,
            artifact_files=artifacts,
            backend_version=backend_version,
            provenance=provenance,
            warnings=[
                "ORCA completed, but the primary result was not fully parsed or the optimization did not converge."
            ],
        )
    return success(
        result,
        artifact_files=artifacts,
        backend_version=backend_version,
        provenance=provenance,
    )


def _vibrations(request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    from ase.vibrations.data import VibrationsData

    inputs, _method, settings = request_parts(request)
    hessian_value = inputs["hessian"]
    if isinstance(hessian_value, dict) and "matrix" not in hessian_value and "result" in hessian_value:
        hessian_value = hessian_value["result"]
    matrix = np.asarray(hessian_value["matrix"] if isinstance(hessian_value, dict) else hessian_value, dtype=float)
    unit = str(hessian_value.get("unit", "eV/angstrom^2")) if isinstance(hessian_value, dict) else "eV/angstrom^2"
    if unit == "hartree/bohr^2":
        matrix = matrix * 27.211386245988 / (0.529177210903**2)
    elif unit != "eV/angstrom^2":
        raise ValueError(f"Unsupported Hessian unit: {unit}")
    atoms = ase_atoms(inputs["structure"])
    expected = 3 * len(atoms)
    if matrix.shape != (expected, expected):
        raise ValueError(f"Hessian shape must be {(expected, expected)}, received {matrix.shape}")
    vibrations = VibrationsData.from_2d(atoms, matrix)
    energies = vibrations.get_energies()
    frequencies = vibrations.get_frequencies()
    modes = vibrations.get_modes(all_atoms=True)
    return success(
        {
            "frequencies_cm1": [
                {"real": float(value.real), "imaginary": float(value.imag)} for value in frequencies
            ],
            "vibrational_energies_ev": [
                {"real": float(value.real), "imaginary": float(value.imag)} for value in energies
            ],
            "modes": np.asarray(modes).real.tolist(),
            "linearity": settings.get("linearity", "auto"),
        },
        backend_version=module_version("ase"),
    )


def _ir_spectrum(request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, _method, settings = request_parts(request)
    vibrations = inputs["vibrations"]
    if isinstance(vibrations, dict) and "result" in vibrations:
        vibrations = vibrations["result"]
    frequencies = vibrations.get("frequencies_cm1")
    intensities = vibrations.get("intensities") or vibrations.get("intensities_km_mol")
    if not frequencies or intensities is None:
        raise ValueError("vibrations must contain frequencies_cm1 and intensities")
    values = [float(item.get("real", item) if isinstance(item, dict) else item) for item in frequencies]
    intensities = [float(value) for value in intensities]
    if len(values) != len(intensities):
        raise ValueError("frequencies and intensities must be aligned")
    fwhm = float(settings["fwhm_cm1"])
    if fwhm <= 0:
        raise ValueError("fwhm_cm1 must be positive")
    start = float(settings.get("min_wavenumber_cm1", max(0.0, min(values) - 5 * fwhm)))
    end = float(settings.get("max_wavenumber_cm1", max(values) + 5 * fwhm))
    points = int(settings.get("points", 4000))
    grid = np.linspace(start, end, points)
    broadening = str(settings["broadening"]).lower()
    spectrum = np.zeros_like(grid)
    if broadening == "gaussian":
        sigma = fwhm / (2 * math.sqrt(2 * math.log(2)))
        for frequency, intensity in zip(values, intensities):
            spectrum += intensity * np.exp(-0.5 * ((grid - frequency) / sigma) ** 2)
    elif broadening == "lorentzian":
        gamma = fwhm / 2
        for frequency, intensity in zip(values, intensities):
            spectrum += intensity * gamma**2 / ((grid - frequency) ** 2 + gamma**2)
    else:
        raise ValueError("broadening must be gaussian or lorentzian")
    return success(
        {
            "wavenumber_cm1": grid.tolist(),
            "intensity": spectrum.tolist(),
            "line_frequencies_cm1": values,
            "line_intensities": intensities,
            "broadening": broadening,
            "fwhm_cm1": fwhm,
        },
        backend_version=module_version("numpy"),
    )


def _internal_thermochemistry(request: dict[str, Any]) -> dict[str, Any]:
    from ase.thermochemistry import IdealGasThermo

    inputs, _method, settings = request_parts(request)
    energy_value = inputs["energy"]
    frequencies = inputs["frequencies"]
    if isinstance(energy_value, dict) and "result" in energy_value:
        energy_value = energy_value["result"]
    if isinstance(frequencies, dict) and "result" in frequencies:
        frequencies = frequencies["result"]
    energy = float(energy_value.get("energy", energy_value.get("energy_hartree", energy_value)))
    unit = str(energy_value.get("unit", "hartree")) if isinstance(energy_value, dict) else "hartree"
    if unit == "hartree":
        energy *= 27.211386245988
    elif unit != "eV":
        raise ValueError(f"Unsupported energy unit: {unit}")
    vib_energies = frequencies.get("vibrational_energies_ev")
    if vib_energies is None:
        cm1 = frequencies["frequencies_cm1"]
        vib_energies = [float(item.get("real", item)) * 1.2398419843320026e-4 for item in cm1]
    else:
        vib_energies = [float(item.get("real", item)) for item in vib_energies]
    atoms_value = inputs.get("structure") or frequencies.get("structure")
    if atoms_value is None:
        return unsupported("internal_thermochemistry requires structure in inputs or FrequencyResult")
    atoms = ase_atoms(atoms_value)
    thermo = IdealGasThermo(
        vib_energies=vib_energies,
        potentialenergy=energy,
        atoms=atoms,
        geometry=str(settings.get("geometry", "nonlinear")),
        symmetrynumber=int(settings.get("symmetry_number", 1)),
        spin=float(settings.get("spin", 0.0)),
        ignore_imag_modes=bool(settings.get("ignore_imaginary_modes", False)),
    )
    temperature = float(settings["temperature_kelvin"])
    pressure = float(settings["pressure_pa"])
    enthalpy = float(thermo.get_enthalpy(temperature, verbose=False))
    entropy = float(thermo.get_entropy(temperature, pressure, verbose=False))
    gibbs = float(thermo.get_gibbs_energy(temperature, pressure, verbose=False))
    return success(
        {
            "temperature_kelvin": temperature,
            "pressure_pa": pressure,
            "enthalpy_ev": enthalpy,
            "entropy_ev_per_kelvin": entropy,
            "gibbs_free_energy_ev": gibbs,
        },
        backend_version=module_version("ase"),
    )


def _goodvibes(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    source_value = inputs.get("output_file")
    if source_value is None and isinstance(inputs.get("frequencies"), dict):
        source_value = inputs["frequencies"].get("output_file") or inputs["frequencies"].get("path")
    if source_value is None:
        return unsupported("GoodVibes requires a compatible quantum-chemistry output_file Artifact")
    source = resolve_input_file(source_value)
    directory = output_directory("derive_thermochemistry", "goodvibes")
    arguments = [
        "-t", str(settings["temperature_kelvin"]),
        "--fs", str(settings.get("frequency_scale", 1.0)),
        str(source),
    ]
    completed = run_external(
        executable="goodvibes", environment_variable="CHEMGRAPH_GOODVIBES_COMMAND",
        arguments=arguments, directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge goodvibes")
    if completed["returncode"] != 0:
        raise RuntimeError(f"GoodVibes failed: {completed['stderr'][-2000:]}")
    return success(
        {"temperature_kelvin": float(settings["temperature_kelvin"]), "raw_output": completed["stdout"][-10000:]},
        artifact_files=command_artifacts(directory),
        provenance={"command": completed["command"]},
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id in {"ase_emt", "tblite", "mace", "chgnet", "deepmd"}:
        return _ase_property(action_id, backend_id, request)
    if backend_id == "xtb":
        return _xtb(action_id, request)
    if backend_id == "pyscf":
        return _pyscf(action_id, request)
    if backend_id == "psi4":
        return _psi4(action_id, request)
    if backend_id == "orca":
        return _orca(action_id, request)
    if backend_id == "gaussian":
        return _gaussian(action_id, request)
    if backend_id == "gamess":
        return _gamess(action_id, request)
    if backend_id == "internal_vibrations" and action_id == "derive_vibrational_modes":
        return _vibrations(request)
    if backend_id == "internal_spectroscopy" and action_id == "derive_ir_spectrum":
        return _ir_spectrum(request)
    if backend_id == "internal_thermochemistry" and action_id == "derive_thermochemistry":
        return _internal_thermochemistry(request)
    if backend_id == "goodvibes" and action_id == "derive_thermochemistry":
        return _goodvibes(request)
    return unsupported(f"Unsupported electronic action/backend combination: {action_id}/{backend_id}")

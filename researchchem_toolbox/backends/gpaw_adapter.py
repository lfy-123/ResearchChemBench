"""Atomic GPAW adapter shared by molecular and periodic actions."""

from __future__ import annotations

from typing import Any

from .common import (
    ase_atoms,
    command_artifacts,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    structure_from_atoms,
    success,
    unwrap_artifact,
    write_json,
)


MOLECULAR_ACTIONS = {"calculate_energy", "calculate_forces", "optimize_geometry"}
PERIODIC_ACTIONS = {
    "calculate_periodic_energy", "calculate_periodic_forces",
    "calculate_periodic_stress", "relax_periodic_structure",
}
POSTPROCESS_ACTIONS = {
    "calculate_electronic_band_structure",
    "calculate_density_of_states",
    "calculate_projected_density_of_states",
}


def _ground_state_path(value: Any):
    item = unwrap_artifact(value)
    if isinstance(item, dict) and isinstance(item.get("result"), dict):
        item = item["result"]
    if isinstance(item, dict):
        for key in ("restart_path", "ground_state_path", "path"):
            if isinstance(item.get(key), str):
                return resolve_input_file(item[key])
    return resolve_input_file(item)


def _postprocess(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import gpaw
    import numpy as np
    from gpaw import GPAW

    inputs, _method, settings = request_parts(request)
    ground_state = _ground_state_path(inputs["ground_state"])
    directory = output_directory(action_id, "gpaw")
    calculator = GPAW(str(ground_state), txt=str(directory / "gpaw_analysis.txt"))
    atoms = calculator.get_atoms()
    energy_reference = str(settings["energy_reference"]).strip().lower()
    if energy_reference not in {"fermi", "absolute"}:
        raise ValueError("energy_reference must be fermi or absolute")

    if action_id == "calculate_electronic_band_structure":
        path = str(settings["band_path"]).strip().upper()
        if not path or any(not (character.isalpha() or character in "-,") for character in path):
            raise ValueError("band_path must be an explicit ASE high-symmetry label path")
        points = int(settings["number_of_points"])
        bands = int(settings["number_of_bands"])
        converged_bands = int(settings["converged_bands"])
        if points < 2 or points > 100000:
            raise ValueError("number_of_points must be between 2 and 100000")
        if bands < 1 or converged_bands < 1 or converged_bands > bands:
            raise ValueError("number_of_bands and converged_bands must satisfy 1 <= converged <= total")
        band_path = atoms.cell.bandpath(path=path, npoints=points)
        band_calculator = calculator.fixed_density(
            nbands=bands,
            symmetry="off",
            kpts=band_path,
            convergence={"bands": converged_bands},
            txt=str(directory / "gpaw_band_structure.txt"),
        )
        band_structure = band_calculator.band_structure()
        energies = np.asarray(band_structure.energies, dtype=float)
        reference = float(band_structure.reference)
        if energy_reference == "fermi":
            energies = energies - reference
        axis, special_points, labels = band_path.get_linear_kpoint_axis()
        result = {
            "band_path": path,
            "fractional_k_points": np.asarray(band_path.kpts, dtype=float).tolist(),
            "linear_k_axis": np.asarray(axis, dtype=float).tolist(),
            "special_point_axis": np.asarray(special_points, dtype=float).tolist(),
            "special_point_labels": [str(value) for value in labels],
            "energies_ev": energies.tolist(),
            "energy_reference": energy_reference,
            "reference_energy_ev": reference,
            "spin_channel_count": int(energies.shape[0]),
            "k_point_count": int(energies.shape[1]),
            "band_count": int(energies.shape[2]),
            "ground_state_path": relative_workspace_path(ground_state),
        }
        path_out = write_json(directory, "band_structure.json", result)
        provenance = {
            "ground_state_restart": relative_workspace_path(ground_state),
            "normalized_result": relative_workspace_path(path_out),
            "fixed_density": True,
        }
    else:
        minimum = float(settings["minimum_energy_ev"])
        maximum = float(settings["maximum_energy_ev"])
        points = int(settings["grid_points"])
        width = float(settings["broadening_ev"])
        if not np.isfinite(minimum) or not np.isfinite(maximum) or minimum >= maximum:
            raise ValueError("minimum_energy_ev must be below maximum_energy_ev")
        if points < 2 or points > 1000000:
            raise ValueError("grid_points must be between 2 and 1000000")
        if not np.isfinite(width) or width < 0:
            raise ValueError("broadening_ev must be finite and nonnegative")
        spin_name = str(settings["spin"]).strip().lower()
        spin = {"total": None, "up": 0, "down": 1}.get(spin_name)
        if spin_name not in {"total", "up", "down"}:
            raise ValueError("spin must be total, up, or down")
        energy = np.linspace(minimum, maximum, points)
        dos_calculator = calculator.dos(shift_fermi_level=energy_reference == "fermi")
        if action_id == "calculate_density_of_states":
            density = np.asarray(
                dos_calculator.raw_dos(energy, spin=spin, width=width), dtype=float
            )
            result = {
                "energy_ev": energy.tolist(),
                "density_of_states_per_ev": density.tolist(),
                "energy_reference": energy_reference,
                "reference_energy_ev": float(calculator.get_fermi_level()),
                "spin": spin_name,
                "broadening_ev": width,
                "ground_state_path": relative_workspace_path(ground_state),
            }
            path_out = write_json(directory, "density_of_states.json", result)
        else:
            raw_projections = inputs["projections"]
            if not isinstance(raw_projections, list) or not raw_projections:
                raise ValueError("projections must be a non-empty list of typed projection objects")
            angular_map = {"s": 0, "p": 1, "d": 2, "f": 3}
            projections = []
            for index, projection in enumerate(raw_projections):
                if not isinstance(projection, dict):
                    raise ValueError("Every projection must be an object")
                atom_index = int(projection["atom_index"])
                if atom_index < 0 or atom_index >= len(atoms):
                    raise ValueError("projection atom_index is outside the ground-state structure")
                angular_value = projection["angular_momentum"]
                if isinstance(angular_value, str):
                    angular = angular_map.get(angular_value.strip().lower())
                else:
                    angular = int(angular_value)
                if angular not in {0, 1, 2, 3}:
                    raise ValueError("angular_momentum must be s/p/d/f or 0/1/2/3")
                magnetic = projection.get("magnetic_component")
                if magnetic is not None:
                    magnetic = int(magnetic)
                    if magnetic < 0 or magnetic > 2 * angular:
                        raise ValueError("magnetic_component must be between 0 and 2*l")
                density = np.asarray(
                    dos_calculator.raw_pdos(
                        energy,
                        a=atom_index,
                        l=angular,
                        m=magnetic,
                        spin=spin,
                        width=width,
                    ),
                    dtype=float,
                )
                projections.append(
                    {
                        "label": str(
                            projection.get("label")
                            or f"atom_{atom_index}_{'spdf'[angular]}"
                        ),
                        "atom_index": atom_index,
                        "element": atoms[atom_index].symbol,
                        "angular_momentum": angular,
                        "magnetic_component": magnetic,
                        "density_of_states_per_ev": density.tolist(),
                    }
                )
            result = {
                "energy_ev": energy.tolist(),
                "projections": projections,
                "energy_reference": energy_reference,
                "reference_energy_ev": float(calculator.get_fermi_level()),
                "spin": spin_name,
                "broadening_ev": width,
                "ground_state_path": relative_workspace_path(ground_state),
            }
            path_out = write_json(directory, "projected_density_of_states.json", result)
        provenance = {
            "ground_state_restart": relative_workspace_path(ground_state),
            "normalized_result": relative_workspace_path(path_out),
        }
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=getattr(gpaw, "__version__", None),
        provenance=provenance,
    )


def _calculator(action_id: str, request: dict[str, Any], directory, atoms):
    from gpaw import FermiDirac, GPAW, PW

    _inputs, method, settings = request_parts(request)
    mode_name = str(method["mode"]).strip().lower()
    keyword: dict[str, Any] = {
        "xc": str(method["xc"]),
        "txt": str(directory / "gpaw.txt"),
        "convergence": {"energy": float(settings.get("scf_energy_convergence_ev", 1e-5))},
        "maxiter": int(settings.get("max_scf_cycles", 200)),
        "charge": float(method.get("charge", atoms.info.get("charge", 0))),
        "spinpol": bool(method["spin_polarized"]),
    }
    if mode_name == "pw":
        if action_id in MOLECULAR_ACTIONS:
            raise ValueError("GPAW molecular actions support explicit fd or lcao mode, not periodic PW mode")
        if "ecut_ev" not in method:
            raise ValueError("GPAW pw mode requires method_spec.ecut_ev")
        keyword["mode"] = PW(float(method["ecut_ev"]))
    elif mode_name == "fd":
        if "grid_spacing_angstrom" not in method:
            raise ValueError("GPAW fd mode requires method_spec.grid_spacing_angstrom")
        keyword["mode"] = "fd"
        keyword["h"] = float(method["grid_spacing_angstrom"])
    elif mode_name == "lcao":
        if "basis" not in method:
            raise ValueError("GPAW lcao mode requires method_spec.basis")
        keyword["mode"] = "lcao"
        keyword["basis"] = str(method["basis"])
    else:
        raise ValueError("GPAW mode must be pw, fd, or lcao")
    if action_id in PERIODIC_ACTIONS:
        raw_kpoints = method["k_points"]
        if isinstance(raw_kpoints, dict):
            grid = raw_kpoints.get("grid") or raw_kpoints.get("size")
            gamma = bool(raw_kpoints.get("gamma", True))
        else:
            grid = raw_kpoints
            gamma = True
        if not isinstance(grid, (list, tuple)) or len(grid) != 3:
            raise ValueError("GPAW periodic actions require k_points as a three-integer grid")
        keyword["kpts"] = {"size": tuple(int(value) for value in grid), "gamma": gamma}
    if method.get("occupations_width_ev") is not None:
        keyword["occupations"] = FermiDirac(float(method["occupations_width_ev"]))
    if method.get("setups") is not None:
        keyword["setups"] = method["setups"]
    if bool(method["spin_polarized"]):
        moments = method.get("initial_magnetic_moments")
        if not isinstance(moments, list) or len(moments) != len(atoms):
            raise ValueError("spin-polarized GPAW requires one initial_magnetic_moments value per atom")
        atoms.set_initial_magnetic_moments([float(value) for value in moments])
    return GPAW(**keyword), mode_name


def execute(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import gpaw
    import numpy as np

    if action_id in POSTPROCESS_ACTIONS:
        return _postprocess(action_id, request)
    inputs, _method, settings = request_parts(request)
    atoms = ase_atoms(inputs["structure"])
    molecular = action_id in MOLECULAR_ACTIONS
    if molecular:
        if any(bool(value) for value in atoms.pbc):
            raise ValueError("GPAW molecular actions require non-periodic input")
        vacuum = float(settings["vacuum_angstrom"])
        if vacuum <= 0:
            raise ValueError("vacuum_angstrom must be positive")
        atoms.center(vacuum=vacuum)
    else:
        if not all(bool(value) for value in atoms.pbc) or atoms.cell.volume <= 0:
            raise ValueError("GPAW periodic actions require a nonzero cell and PBC in all dimensions")
    directory = output_directory(action_id, "gpaw")
    calculator, mode_name = _calculator(action_id, request, directory, atoms)
    atoms.calc = calculator
    if action_id in {"calculate_energy", "calculate_periodic_energy"}:
        energy = float(atoms.get_potential_energy())
        result = {
            "energy": energy,
            "unit": "eV",
            "mode": mode_name,
            "atom_count": len(atoms),
        }
        if action_id == "calculate_periodic_energy":
            restart_path = directory / "ground_state.gpw"
            calculator.write(str(restart_path), mode="all")
            result["restart_path"] = relative_workspace_path(restart_path)
    elif action_id in {"calculate_forces", "calculate_periodic_forces"}:
        result = {
            "forces": np.asarray(atoms.get_forces(), dtype=float).tolist(),
            "unit": "eV/angstrom",
            "energy_ev": float(atoms.get_potential_energy()),
            "atom_count": len(atoms),
        }
    elif action_id == "calculate_periodic_stress":
        if mode_name != "pw":
            raise ValueError("GPAW stress calculations require explicit pw mode")
        result = {
            "stress": np.asarray(atoms.get_stress(voigt=False), dtype=float).tolist(),
            "unit": "eV/angstrom^3",
            "energy_ev": float(atoms.get_potential_energy()),
        }
    elif action_id in {"optimize_geometry", "relax_periodic_structure"}:
        from ase.filters import UnitCellFilter
        from ase.io import write
        from ase.optimize import BFGS, FIRE, LBFGS

        optimizer_name = str(settings["optimizer"]).strip().lower()
        optimizer_class = {"bfgs": BFGS, "lbfgs": LBFGS, "fire": FIRE}.get(optimizer_name)
        if optimizer_class is None:
            raise ValueError("optimizer must be bfgs, lbfgs, or fire")
        target = atoms
        relax_cell = action_id == "relax_periodic_structure" and bool(settings["relax_cell"])
        if relax_cell:
            target = UnitCellFilter(atoms)
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
        write(str(directory / "optimized.extxyz"), atoms)
        output_atoms = atoms.copy()
        if molecular:
            output_atoms.set_cell([0.0, 0.0, 0.0])
        result = {
            "structure": structure_from_atoms(output_atoms),
            "converged": converged,
            "energy": float(atoms.get_potential_energy()),
            "energy_unit": "eV",
            "optimizer": optimizer_name,
            "relax_cell": relax_cell,
        }
        if not converged:
            return partial_success(
                result,
                artifact_files=command_artifacts(directory),
                backend_version=getattr(gpaw, "__version__", None),
                warnings=["GPAW optimization reached its step limit before convergence."],
            )
    else:
        raise ValueError(f"GPAW does not implement {action_id}")
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=getattr(gpaw, "__version__", None),
    )

from __future__ import annotations

import pytest

from researchchem_toolbox.service import execute_action


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.75]},
    ],
    "pbc": [False, False, False],
    "charge": 0,
    "multiplicity": 1,
}


SILICON = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [1.3575, 1.3575, 1.3575]},
    ],
    "cell_angstrom": [[0.0, 2.715, 2.715], [2.715, 0.0, 2.715], [2.715, 2.715, 0.0]],
    "pbc": [True, True, True],
}


def test_gpaw_molecular_energy_and_forces(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    base = {
        "backend_id": "gpaw",
        "inputs": {"structure": H2},
        "method_spec": {"mode": "lcao", "basis": "dzp", "xc": "PBE", "spin_polarized": False},
        "action_settings": {
            "vacuum_angstrom": 3.0,
            "scf_energy_convergence_ev": 1e-4,
            "max_scf_cycles": 120,
        },
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
    }
    energy = execute_action("calculate_energy", base)
    forces = execute_action("calculate_forces", base)
    assert energy["status"] == "success"
    assert energy["result"]["unit"] == "eV"
    assert forces["status"] == "success"
    assert len(forces["result"]["forces"]) == 2

    optimization_request = {
        **base,
        "action_settings": {
            **base["action_settings"],
            "force_threshold_ev_per_angstrom": 2.0,
            "max_steps": 2,
            "optimizer": "bfgs",
        },
    }
    optimized = execute_action("optimize_geometry", optimization_request)
    assert optimized["status"] == "success"
    assert optimized["result"]["converged"] is True


def test_gpaw_periodic_energy(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "calculate_periodic_energy",
        {
            "backend_id": "gpaw",
            "inputs": {"structure": SILICON},
            "method_spec": {
                "mode": "lcao", "basis": "dzp", "xc": "PBE",
                "spin_polarized": False, "k_points": {"grid": [1, 1, 1], "gamma": True},
            },
            "action_settings": {"scf_energy_convergence_ev": 1e-4, "max_scf_cycles": 120},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["unit"] == "eV"
    assert result["result"]["restart_path"].endswith("ground_state.gpw")

    band_structure = execute_action(
        "calculate_electronic_band_structure",
        {
            "backend_id": "gpaw",
            "inputs": {"ground_state": result["output_artifacts"][0]},
            "method_spec": {},
            "action_settings": {
                "band_path": "GX",
                "number_of_points": 4,
                "number_of_bands": 6,
                "converged_bands": 4,
                "energy_reference": "fermi",
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert band_structure["status"] == "success"
    assert band_structure["result"]["k_point_count"] == 4
    assert band_structure["result"]["band_count"] == 6

    dos_settings = {
        "minimum_energy_ev": -10.0,
        "maximum_energy_ev": 10.0,
        "grid_points": 41,
        "broadening_ev": 0.2,
        "spin": "total",
        "energy_reference": "fermi",
    }
    dos = execute_action(
        "calculate_density_of_states",
        {
            "backend_id": "gpaw",
            "inputs": {"ground_state": result["output_artifacts"][0]},
            "method_spec": {},
            "action_settings": dos_settings,
        },
    )
    assert dos["status"] == "success"
    assert len(dos["result"]["density_of_states_per_ev"]) == 41

    projected = execute_action(
        "calculate_projected_density_of_states",
        {
            "backend_id": "gpaw",
            "inputs": {
                "ground_state": result["output_artifacts"][0],
                "projections": [
                    {"label": "Si0-s", "atom_index": 0, "angular_momentum": "s"}
                ],
            },
            "method_spec": {},
            "action_settings": dos_settings,
        },
    )
    assert projected["status"] == "success"
    assert projected["result"]["projections"][0]["label"] == "Si0-s"

    forces = execute_action(
        "calculate_periodic_forces",
        {
            "backend_id": "gpaw",
            "inputs": {"structure": SILICON},
            "method_spec": {
                "mode": "lcao", "basis": "dzp", "xc": "PBE",
                "spin_polarized": False, "k_points": {"grid": [1, 1, 1], "gamma": True},
            },
            "action_settings": {"scf_energy_convergence_ev": 1e-4, "max_scf_cycles": 120},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert forces["status"] == "success"
    assert len(forces["result"]["forces"]) == 2

    relaxation = execute_action(
        "relax_periodic_structure",
        {
            "backend_id": "gpaw",
            "inputs": {"structure": SILICON},
            "method_spec": {
                "mode": "lcao", "basis": "dzp", "xc": "PBE",
                "spin_polarized": False, "k_points": {"grid": [1, 1, 1], "gamma": True},
            },
            "action_settings": {
                "scf_energy_convergence_ev": 1e-4, "max_scf_cycles": 120,
                "force_threshold_ev_per_angstrom": 5.0, "max_steps": 2,
                "optimizer": "bfgs", "relax_cell": False,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert relaxation["status"] == "success"
    assert relaxation["result"]["converged"] is True

    stress = execute_action(
        "calculate_periodic_stress",
        {
            "backend_id": "gpaw",
            "inputs": {"structure": SILICON},
            "method_spec": {
                "mode": "pw", "ecut_ev": 100.0, "xc": "PBE",
                "spin_polarized": False, "k_points": {"grid": [1, 1, 1], "gamma": True},
            },
            "action_settings": {"scf_energy_convergence_ev": 1e-4, "max_scf_cycles": 120},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert stress["status"] == "success"
    assert len(stress["result"]["stress"]) == 3

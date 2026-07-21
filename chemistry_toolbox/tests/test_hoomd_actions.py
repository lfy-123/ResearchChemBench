from __future__ import annotations

from researchchem_toolbox.service import execute_action


SYSTEM = {
    "box": [10.0, 10.0, 10.0],
    "particles": {
        "positions": [[-0.6, 0.0, 0.0], [0.6, 0.0, 0.0]],
        "type_names": ["A"],
        "type_ids": [0, 0],
        "masses": [1.0, 1.0],
    },
}


METHOD = {
    "device": "cpu",
    "unit_system": "reduced_lj",
    "pair_potential": "lj",
    "pair_parameters": {"A|A": {"epsilon": 1.0, "sigma": 1.0, "r_cut": 2.5}},
    "neighbor_buffer": 0.4,
}


def test_hoomd_minimization_and_one_dynamics_segment(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    energy = execute_action(
        "calculate_force_field_energy",
        {
            "backend_id": "hoomd",
            "inputs": {"system": SYSTEM},
            "method_spec": METHOD,
            "action_settings": {},
        },
    )
    assert energy["status"] == "success"
    assert energy["result"]["particle_count"] == 2
    assert len(energy["result"]["components"]) == 1

    forces = execute_action(
        "calculate_force_field_forces",
        {
            "backend_id": "hoomd",
            "inputs": {"system": SYSTEM},
            "method_spec": METHOD,
            "action_settings": {},
        },
    )
    assert forces["status"] == "success"
    assert len(forces["result"]["forces"]) == 2
    assert forces["result"]["forces"][0][0] == -forces["result"]["forces"][1][0]

    minimized = execute_action(
        "minimize_system_energy",
        {
            "backend_id": "hoomd",
            "inputs": {"system": SYSTEM},
            "method_spec": METHOD,
            "action_settings": {
                "integration_timestep": 0.001,
                "force_tolerance": 1e-3,
                "energy_tolerance": 1e-8,
                "max_iterations": 1000,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert minimized["status"] == "success"
    assert minimized["result"]["converged"] is True

    trajectory = execute_action(
        "propagate_dynamics",
        {
            "backend_id": "hoomd",
            "inputs": {"system": minimized["result"]},
            "method_spec": METHOD,
            "action_settings": {
                "ensemble": "NVT",
                "temperature_energy": 1.0,
                "timestep": 0.001,
                "steps": 20,
                "report_interval": 5,
                "random_seed": 20260720,
                "initialize_velocities": True,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert trajectory["status"] == "success"
    assert trajectory["result"]["steps"] == 20
    assert trajectory["output_artifacts"]

from __future__ import annotations

import numpy as np

from chemistry_toolbox.src.service import execute_action


STRUCTURE = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [2.5, 2.5, 2.5]},
    ],
    "cell_angstrom": [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]],
    "pbc": [True, True, True],
}


def test_phono3py_rta_thermal_conductivity(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    fc2 = np.zeros((2, 2, 3, 3))
    spring = np.eye(3) * 0.1
    fc2[0, 0] = spring
    fc2[0, 1] = -spring
    fc2[1, 0] = -spring
    fc2[1, 1] = spring
    fc3 = np.random.default_rng(20260720).normal(scale=1e-3, size=(2, 2, 2, 3, 3, 3))
    matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    result = execute_action(
        "calculate_lattice_thermal_conductivity",
        {
            "backend_id": "phono3py",
            "inputs": {
                "structure": STRUCTURE,
                "second_order_force_constants": {
                    "force_constants": fc2.tolist(), "order": 2, "supercell_matrix": matrix,
                },
                "third_order_force_constants": {
                    "force_constants": fc3.tolist(), "order": 3, "supercell_matrix": matrix,
                },
            },
            "method_spec": {},
            "action_settings": {
                "q_mesh": [2, 2, 2],
                "temperatures_kelvin": [300.0],
                "solution_method": "rta",
                "include_isotope_scattering": False,
                "boundary_mean_free_path_micrometer": 1000.0,
                "primitive_matrix": "P",
            },
            "resource_limits": {"cpu_cores": 1,},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["temperatures_kelvin"] == [300.0]
    assert np.isfinite(np.asarray(result["result"]["kappa_w_mk"])).all()

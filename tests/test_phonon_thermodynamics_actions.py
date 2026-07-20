from __future__ import annotations

import numpy as np
import pytest

from researchchem_toolbox.service import execute_action


STRUCTURE = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [2.5, 2.5, 2.5]},
    ],
    "cell_angstrom": [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]],
    "pbc": [True, True, True],
}


def _force_constants():
    matrix = np.zeros((2, 2, 3, 3))
    spring = np.eye(3) * 0.1
    matrix[0, 0] = spring
    matrix[0, 1] = -spring
    matrix[1, 0] = -spring
    matrix[1, 1] = spring
    return {
        "force_constants": matrix.tolist(),
        "order": 2,
        "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "original_structure": STRUCTURE,
    }


@pytest.mark.parametrize("backend_id", ["phonopy", "phono3py"])
def test_harmonic_thermodynamics_and_group_velocities(tmp_path, monkeypatch, backend_id: str):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    common = {
        "backend_id": backend_id,
        "inputs": {"force_constants": _force_constants(), "structure": STRUCTURE},
        "method_spec": {},
    }
    thermal = execute_action(
        "calculate_harmonic_thermodynamics",
        {
            **common,
            "action_settings": {
                "q_mesh": [3, 3, 3],
                "temperatures_kelvin": [100.0, 300.0],
            },
        },
    )
    assert thermal["status"] == "success"
    assert thermal["result"]["temperatures_kelvin"] == [100.0, 300.0]

    velocities = execute_action(
        "calculate_phonon_group_velocities",
        {
            **common,
            "action_settings": {
                "q_path": [[[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.5, 0.0, 0.0]]],
            },
        },
    )
    assert velocities["status"] == "success"
    assert velocities["result"]["group_velocities_thz_angstrom"]

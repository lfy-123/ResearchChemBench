from __future__ import annotations

import pytest

from researchchem_toolbox.service import execute_action


WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.7578, 0.5859]},
        {"element": "H", "position_angstrom": [0.0, -0.7578, 0.5859]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


@pytest.mark.parametrize(
    ("action_id", "result_key"),
    [
        ("calculate_energy", "energy"),
        ("calculate_forces", "forces"),
        ("calculate_hessian", "matrix"),
        ("calculate_dipole_moment", "dipole"),
        ("calculate_atomic_charges", "charges"),
    ],
)
def test_nwchem_qcschema_atomic_actions(tmp_path, monkeypatch, action_id: str, result_key: str):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        action_id,
        {
            "backend_id": "nwchem",
            "inputs": {"structure": WATER},
            "method_spec": {"method": "hf", "basis": "sto-3g", "reference": "rhf"},
            "action_settings": {"scf_convergence": 1e-8, "max_scf_cycles": 100},
            "resource_limits": {"cpu_cores": 1, "memory_mb": 1024, "walltime_seconds": 300},
        },
    )
    assert result["status"] == "success"
    assert result_key in result["result"]
    assert result["output_artifacts"]
    if action_id == "calculate_atomic_charges":
        assert sum(result["result"]["charges"]) == pytest.approx(0.0, abs=0.05)

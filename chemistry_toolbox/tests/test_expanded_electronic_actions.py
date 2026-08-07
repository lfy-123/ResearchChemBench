from __future__ import annotations

import math

import pytest

from chemistry_toolbox.src.service import execute_action


WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.757, 0.586, 0.0]},
        {"element": "H", "position_angstrom": [-0.757, 0.586, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def _request(backend_id: str, method_spec: dict[str, object]) -> dict[str, object]:
    return {
        "backend_id": backend_id,
        "inputs": {"structure": WATER},
        "method_spec": method_spec,
        "action_settings": {"scf_convergence": 1e-9},
        "resource_limits": {"cpu_cores": 1,},
    }


@pytest.mark.parametrize(
    ("action_id", "expected_unit"),
    [
        ("calculate_forces", "eV/angstrom"),
        ("calculate_dipole_moment", "debye"),
        ("calculate_atomic_charges", "elementary_charge"),
    ],
)
def test_xtb_exposes_independent_derivative_and_property_actions(
    tmp_path, monkeypatch, action_id: str, expected_unit: str
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(action_id, _request("xtb", {"method": "gfn2"}))
    assert result["status"] == "success"
    assert result["result"]["unit"] == expected_unit
    if action_id == "calculate_forces":
        assert len(result["result"]["forces"]) == 3
    elif action_id == "calculate_dipole_moment":
        assert result["result"]["magnitude"] > 0
        assert math.sqrt(sum(value**2 for value in result["result"]["dipole"])) == pytest.approx(
            result["result"]["magnitude"], rel=0.01, abs=0.01
        )
        assert "dipole_atomic_units" in result["result"]
        assert "dipole_e_angstrom" in result["result"]
        assert "magnitude_e_angstrom" in result["result"]
    else:
        assert len(result["result"]["charges"]) == 3
        assert sum(result["result"]["charges"]) == pytest.approx(0.0, abs=1e-6)


@pytest.mark.parametrize("action_id", ["calculate_forces", "calculate_hessian"])
def test_pyscf_exposes_independent_analytic_derivative_actions(
    tmp_path, monkeypatch, action_id: str
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(action_id, _request("pyscf", {"method": "rhf", "basis": "sto-3g"}))
    assert result["status"] == "success"
    if action_id == "calculate_forces":
        assert result["result"]["unit"] == "eV/angstrom"
        assert len(result["result"]["forces"]) == 3
    else:
        assert result["result"]["unit"] == "hartree/bohr^2"
        assert len(result["result"]["matrix"]) == 9
        assert all(len(row) == 9 for row in result["result"]["matrix"])


def test_xtb_exposes_wiberg_bond_orders_as_an_atomic_action(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _request("xtb", {"method": "gfn2"})
    request["action_settings"] = {"minimum_bond_order": 0.05}
    result = execute_action("calculate_bond_orders", request)
    assert result["status"] == "success"
    assert len(result["result"]["bonds"]) == 2

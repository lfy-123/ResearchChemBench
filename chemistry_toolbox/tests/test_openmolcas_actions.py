from __future__ import annotations

import pytest

from chemistry_toolbox.src.service import execute_action


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.74]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}


def _request():
    return {
        "backend_id": "openmolcas",
        "inputs": {"structure": H2},
        "method_spec": {"method": "hf", "basis": "STO-3G"},
        "action_settings": {
            "use_symmetry": False,
            "use_uhf": False,
            "use_cholesky": False,
            "initial_guess": "default",
            "max_scf_iterations": 100,
            "scf_thresholds": [1.0e-9, 1.0e-4, 1.5e-4, 1.0e-3],
        },
        "resource_limits": { "cpu_cores": 1},
    }


def test_openmolcas_scf_energy_and_properties(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    energy = execute_action("calculate_energy", _request())
    assert energy["status"] == "success"
    assert energy["backend_version"] == "25.10"
    assert energy["result"]["energy_hartree"] == pytest.approx(-1.1167593075)
    assert energy["provenance"]["happy_landing"] is True

    dipole = execute_action("calculate_dipole_moment", _request())
    assert dipole["status"] == "success"
    assert dipole["result"]["magnitude"] == pytest.approx(0.0, abs=1.0e-10)
    assert dipole["result"]["unit"] == "debye"

    charges = execute_action("calculate_atomic_charges", _request())
    assert charges["status"] == "success"
    assert charges["result"]["charges"] == pytest.approx([0.0, 0.0], abs=1.0e-6)
    assert charges["result"]["analysis"] == "mulliken"

    orbitals = execute_action("calculate_orbitals", _request())
    assert orbitals["status"] == "success"
    assert orbitals["result"]["orbital_count"] == 2
    assert orbitals["result"]["occupations"] == [2.0, 0.0]
    assert orbitals["result"]["energies_hartree"] == pytest.approx([-0.5786, 0.6711])


def test_openmolcas_requires_explicit_uhf_for_open_shell(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _request()
    request["inputs"]["structure"] = {
        "atoms": [{"element": "H", "position_angstrom": [0.0, 0.0, 0.0]}],
        "charge": 0,
        "multiplicity": 2,
        "pbc": [False, False, False],
    }
    result = execute_action("calculate_energy", request)
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "backend_input_error"
    assert "use_uhf=true" in result["error"]["message"]

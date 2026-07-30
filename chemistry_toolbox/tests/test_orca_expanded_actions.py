from __future__ import annotations

import pytest

from researchchem_toolbox.service import execute_action


WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.757, 0.586, 0.0]},
        {"element": "H", "position_angstrom": [-0.757, 0.586, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def _orca_request(*, method=None, settings=None):
    return {
        "backend_id": "orca",
        "inputs": {"structure": WATER},
        "method_spec": {"method": "HF", "basis": "STO-3G", **(method or {})},
        "action_settings": settings or {},
        "resource_limits": {"cpu_cores": 1,},
    }


def test_orca_pal2_uses_matching_openmpi_without_ucx_noise(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _orca_request()
    request["resource_limits"] = {"cpu_cores": 2, "memory_mb": 2048}

    result = execute_action("calculate_energy", request)

    assert result["status"] == "success"
    output = next(tmp_path.glob("outputs/calculate_energy/orca/*/job.out"))
    stderr = next(tmp_path.glob("outputs/calculate_energy/orca/*/job.err"))
    assert "ORCA TERMINATED NORMALLY" in output.read_text(
        encoding="utf-8", errors="replace"
    )
    diagnostic = stderr.read_text(encoding="utf-8", errors="replace")
    assert "osc_ucx_component" not in diagnostic
    assert "cxiWaitEventWait" not in diagnostic


@pytest.mark.parametrize(
    ("action_id", "method", "settings", "result_key"),
    [
        ("calculate_forces", {}, {}, "forces"),
        ("calculate_atomic_charges", {"population_analysis": "mulliken"}, {}, "charges"),
        ("calculate_orbitals", {}, {}, "orbitals"),
        ("calculate_bond_orders", {}, {"minimum_bond_order": 0.05}, "bonds"),
    ],
)
def test_orca_independent_electronic_property_actions(
    tmp_path, monkeypatch, action_id, method, settings, result_key
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(action_id, _orca_request(method=method, settings=settings))
    assert result["status"] == "success"
    assert result["result"][result_key]


def test_orca_and_pyscf_excited_states_feed_internal_spectrum(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    orca = execute_action(
        "calculate_excited_states",
        _orca_request(
            method={"method": "B3LYP", "excited_state_method": "tddft"},
            settings={
                "number_of_states": 2,
                "spin_symmetry": "singlet",
                "excited_energy_tolerance_hartree": 1e-6,
                "residual_tolerance": 1e-6,
            },
        ),
    )
    assert orca["status"] == "success"
    assert len(orca["result"]["states"]) == 2

    spectrum = execute_action(
        "derive_uv_vis_spectrum",
        {
            "inputs": {"excited_states": orca["result"]},
            "method_spec": {},
            "action_settings": {
                "broadening": "gaussian",
                "fwhm_ev": 0.2,
                "minimum_energy_ev": 8.0,
                "maximum_energy_ev": 16.0,
                "grid_points": 200,
            },
        },
    )
    assert spectrum["status"] == "success"
    assert len(spectrum["result"]["energy_ev"]) == 200

    pyscf = execute_action(
        "calculate_excited_states",
        {
            "backend_id": "pyscf",
            "inputs": {"structure": WATER},
            "method_spec": {
                "method": "rhf",
                "basis": "sto-3g",
                "excited_state_method": "tda",
            },
            "action_settings": {
                "number_of_states": 2,
                "spin_symmetry": "singlet",
                "scf_convergence": 1e-9,
            },
            "resource_limits": {"cpu_cores": 1,},
        },
    )
    assert pyscf["status"] == "success"
    assert len(pyscf["result"]["states"]) == 2

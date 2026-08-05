from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from researchchem_toolbox.service import execute_action


SOURCE = Path(".software_cache/lobster/5.1.0/smoke/qe_diamond").resolve()


def _copy(tmp_path, name: str) -> Path:
    target = tmp_path / name
    shutil.copy2(SOURCE / name, target)
    return target


def test_lobster_bonding_curves_and_projection_quality(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    integrated = _copy(tmp_path, "ICOHPLIST.lobster")
    curves = _copy(tmp_path, "COHPCAR.lobster")
    lobsterout = _copy(tmp_path, "lobsterout")
    bonding = execute_action(
        "analyze_periodic_bonding",
        {
            "backend_id": "lobster",
            "inputs": {
                "integrated_bond_list": str(integrated),
                "bond_curve_file": str(curves),
            },
            "method_spec": {},
            "action_settings": {
                "bonding_metric": "cohp",
                "spin": "sum",
                "minimum_absolute_integrated_value_ev": 0.1,
                "max_bonds": 10,
                "include_curve_data": True,
                "minimum_energy_ev": -5.0,
                "maximum_energy_ev": 5.0,
                "curve_stride": 5,
                "max_curve_points": 100,
            },
        },
    )
    assert bonding["status"] == "success"
    assert bonding["result"]["bond_count"] == 1
    assert bonding["result"]["bonds"][0]["integrated_value_ev"] == pytest.approx(
        -9.604, abs=1.0e-3
    )
    assert bonding["result"]["bonds"][0]["curve"]["energy_ev_relative_to_fermi"]

    quality = execute_action(
        "calculate_charge_spilling",
        {
            "backend_id": "lobster",
            "inputs": {"lobster_output": str(lobsterout)},
            "method_spec": {},
            "action_settings": {
                "maximum_charge_spilling_percent": 2.0,
                "maximum_total_spilling_percent": 2.0,
                "require_finished": True,
            },
        },
    )
    assert quality["status"] == "success"
    assert quality["result"]["quality_pass"] is True
    assert quality["result"]["maximum_charge_spilling_percent"] == pytest.approx(1.12)


def test_lobster_projected_density_of_states(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    dos = _copy(tmp_path, "DOSCAR.lobster")
    structure = _copy(tmp_path, "POSCAR.lobster.vasp")
    result = execute_action(
        "calculate_projected_density_of_states",
        {
            "backend_id": "lobster",
            "inputs": {
                "dos_file": str(dos),
                "structure_file": str(structure),
                "projections": [
                    {
                        "label": "C0-sp",
                        "atom_index": 0,
                        "orbitals": ["2s", "2p_x", "2p_y", "2p_z"],
                    }
                ],
            },
            "method_spec": {},
            "action_settings": {
                "minimum_energy_ev": -5.0,
                "maximum_energy_ev": 5.0,
                "spin": "sum",
                "curve_stride": 4,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["projections"][0]["label"] == "C0-sp"
    assert len(result["result"]["energy_ev_relative_to_fermi"]) == len(
        result["result"]["projections"][0]["density_of_states_per_ev"]
    )

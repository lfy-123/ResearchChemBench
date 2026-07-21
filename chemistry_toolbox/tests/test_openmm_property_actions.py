from __future__ import annotations

import math

import pytest

from researchchem_toolbox.service import execute_action


WATER = """ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.957   0.000   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.927   0.000  1.00  0.00           H
CONECT    1    2    3
CONECT    2    1
CONECT    3    1
TER
END
"""


def test_openmm_energy_forces_and_force_object_decomposition(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    pdb_path = tmp_path / "water.pdb"
    pdb_path.write_text(WATER, encoding="utf-8")
    parameterized = execute_action(
        "assign_force_field_parameters",
        {
            "backend_id": "openmm_builder",
            "inputs": {"structure": str(pdb_path)},
            "method_spec": {"force_field": ["tip3p.xml"]},
            "action_settings": {},
        },
    )
    assert parameterized["status"] == "success"
    common = {
        "backend_id": "openmm",
        "inputs": {"system": parameterized["result"]},
        "method_spec": {"platform": "Reference", "platform_properties": {}},
    }
    energy = execute_action(
        "calculate_force_field_energy",
        {
            **common,
            "action_settings": {
                "use_saved_state": False,
                "enforce_periodic_box": False,
            },
        },
    )
    assert energy["status"] == "success"
    assert math.isfinite(energy["result"]["potential_energy_kj_mol"])

    forces = execute_action(
        "calculate_force_field_forces",
        {
            **common,
            "action_settings": {
                "use_saved_state": False,
                "enforce_periodic_box": False,
            },
        },
    )
    assert forces["status"] == "success"
    assert len(forces["result"]["forces"]) == 3
    assert forces["result"]["unit"] == "kJ/(mol*nm)"

    decomposition = execute_action(
        "decompose_force_field_energy",
        {
            **common,
            "action_settings": {
                "use_saved_state": False,
                "enforce_periodic_box": False,
                "include_zero_terms": True,
            },
        },
    )
    assert decomposition["status"] == "success"
    assert decomposition["result"]["force_object_count"] >= 1
    assert decomposition["result"]["reported_term_count"] == decomposition["result"]["force_object_count"]
    assert decomposition["result"]["sum_reported_terms_kj_mol"] == pytest.approx(
        decomposition["result"]["total_potential_energy_kj_mol"], abs=1e-8
    )

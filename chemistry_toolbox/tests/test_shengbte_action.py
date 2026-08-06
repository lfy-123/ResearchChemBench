from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from chemistry_toolbox.src.service import execute_action


SOURCE = Path(".software_cache/installations/shengbte/source/Test-RTA").resolve()


def _copy(tmp_path: Path, name: str) -> Path:
    target = tmp_path / name
    shutil.copy2(SOURCE / name, target)
    return target


def test_shengbte_rta_conductivity_from_explicit_native_model(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    control = _copy(tmp_path, "CONTROL")
    fc2 = _copy(tmp_path, "FORCE_CONSTANTS_2ND")
    fc3 = _copy(tmp_path, "FORCE_CONSTANTS_3RD")
    result = execute_action(
        "calculate_lattice_thermal_conductivity",
        {
            "backend_id": "shengbte",
            "inputs": {
                "control_file": str(control),
                "second_order_force_constants_file": str(fc2),
                "third_order_force_constants_file": str(fc3),
            },
            "method_spec": {},
            "action_settings": {
                "solution_method": "rta",
                "maximum_temperature_records": 100,
                "require_normal_exit": True,
            },
            "resource_limits": { "cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "source-b0d2090"
    assert result["result"]["native_control_preserved"] is True
    assert result["result"]["normal_exit"] is True
    record = result["result"]["conductivity_records"][0]
    assert record["temperature_kelvin"] == 300.0
    assert record["kappa_w_mk"][0][0] == pytest.approx(25.662, rel=1e-5)
    assert result["provenance"]["automatic_model_construction"] is False

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from researchchem_toolbox.service import execute_action


MESS_SOURCE = Path(".software_cache/mess/smoke/hco/hco.inp").resolve()
MESMER_SOURCE = Path(
    ".software_cache/mesmer/smoke/examples/H2Ominimal/H2Ominimal.xml"
).resolve()
MESMER_LIBRARY = Path(".software_cache/mesmer/smoke/librarymols.xml").resolve()
MESMER_DEFAULTS = Path(".software_cache/mesmer/smoke/defaults.xml").resolve()


def _copy(tmp_path: Path, source: Path) -> Path:
    target = tmp_path / source.name
    shutil.copy2(source, target)
    return target


def test_mess_solves_native_master_equation_model(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    model = _copy(tmp_path, MESS_SOURCE)
    result = execute_action(
        "solve_master_equation",
        {
            "backend_id": "mess",
            "inputs": {"model_file": str(model)},
            "method_spec": {},
            "action_settings": {"maximum_rate_records": 1000},
            "resource_limits": {"walltime_seconds": 120, "cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "2020.1.24"
    assert result["result"]["completed"] is True
    assert result["result"]["wells"] == ["W1"]
    assert result["result"]["bimolecular_species"] == ["P0"]
    records = result["result"]["rate_records"]
    assert any(
        record["from_species"] == "W1"
        and record["to_species"] == "P0"
        and record["temperature_kelvin"] == 500.0
        and record["pressure_value"] == 30.0
        and record["rate_coefficient"] == pytest.approx(24.0104)
        for record in records
    )
    assert result["provenance"]["automatic_model_construction"] is False


def test_mesmer_solves_xml_model_with_explicit_layout(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    model = _copy(tmp_path, MESMER_SOURCE)
    library = _copy(tmp_path, MESMER_LIBRARY)
    defaults = _copy(tmp_path, MESMER_DEFAULTS)
    result = execute_action(
        "solve_master_equation",
        {
            "backend_id": "mesmer",
            "inputs": {
                "model_file": str(model),
                "model_relative_path": "examples/H2Ominimal/H2Ominimal.xml",
                "companion_files": [
                    {"source": str(library), "relative_path": "librarymols.xml"},
                    {"source": str(defaults), "relative_path": "defaults.xml"},
                ],
            },
            "method_spec": {},
            "action_settings": {"maximum_rate_records": 100},
            "resource_limits": {"walltime_seconds": 120, "cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "7.1"
    assert result["result"]["completed"] is True
    records = result["result"]["rate_records"]
    first_order = next(record for record in records if record["rate_type"] == "firstOrderRate")
    second_order = next(record for record in records if record["rate_type"] == "secondOrderRate")
    assert first_order["temperature_kelvin"] == 560.0
    assert first_order["pressure_value"] == 7600.0
    assert first_order["rate_coefficient_unit"] == "s^-1"
    assert second_order["rate_coefficient"] == pytest.approx(7.36618e-12)
    assert second_order["rate_coefficient_unit"] == "cm^3 molecule^-1 s^-1"
    assert result["provenance"]["native_model_preserved"] is True

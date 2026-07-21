from __future__ import annotations

import json
from pathlib import Path

import pytest

from researchchem_toolbox.backends import goodvibes
from researchchem_toolbox.catalog import action_specs, backend_specs, validate_catalog


def _settings(**updates):
    values = {
        "temperature_kelvin": 298.15,
        "standard_state": "gas_1atm",
        "entropy_model": "grimme",
        "enthalpy_model": "head_gordon",
        "frequency_scale_factor": 0.99,
        "zpe_scale_factor": 0.98,
        "symmetry_correction": False,
        "imaginary_frequency_policy": "retain",
        "entropy_frequency_cutoff_cm1": 100.0,
        "enthalpy_frequency_cutoff_cm1": 75.0,
        "free_rotor_inertia_model": "global",
    }
    values.update(updates)
    return values


def _payload(file: Path, temperature: float = 298.15):
    return {
        "schema_version": "1.0",
        "goodvibes_version": "4.3.0",
        "options": {"temperature": temperature},
        "results": [
            {
                "file": str(file),
                "name": file.stem,
                "qcdata": {"file": str(file), "program": "Gaussian"},
                "thermo": {
                    "enthalpy": -10.0,
                    "qh_enthalpy": -9.9,
                    "entropy": 0.0001,
                    "qh_entropy": 0.00009,
                    "gibbs_free_energy": -10.029815,
                    "qh_gibbs_free_energy": -9.9268335,
                },
                "boltzmann_factor": 1.0,
            }
        ],
    }


def test_goodvibes_catalog_exposes_six_generic_actions():
    validate_catalog()
    backend = backend_specs()["goodvibes"]
    assert backend.runtime == "goodvibes"
    assert backend.pip_packages == ("goodvibes[full]==4.3.0",)
    assert set(backend.capabilities) == {
        "derive_thermochemistry",
        "scan_thermochemistry_temperature",
        "analyze_thermochemical_ensemble",
        "validate_thermochemistry_inputs",
        "analyze_thermochemical_selectivity",
        "analyze_reaction_free_energy_profile",
    }
    assert all(action_id in action_specs() for action_id in backend.capabilities)


def test_goodvibes_cli_mapping_distinguishes_scale_from_entropy_cutoff():
    arguments = goodvibes._common_arguments(
        _settings(), {}, temperature_kelvin=298.15
    )
    assert arguments[arguments.index("--vscal") + 1] == "0.99"
    assert arguments[arguments.index("--zpe-vscal") + 1] == "0.98"
    assert arguments[arguments.index("--fs") + 1] == "100"
    assert arguments[arguments.index("--fh") + 1] == "75"
    assert arguments[arguments.index("--bav") + 1] == "global"


def test_goodvibes_rejects_unrepresentable_independent_auto_zpe_scale():
    with pytest.raises(ValueError, match="cannot be represented faithfully"):
        goodvibes._common_arguments(
            _settings(frequency_scale_factor=0.99, zpe_scale_factor="auto"),
            {},
            temperature_kelvin=298.15,
        )


def test_goodvibes_derive_returns_structured_json_result(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    source = tmp_path / "water.log"
    source.write_text("test", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()
    calls = []

    monkeypatch.setattr(goodvibes, "output_directory", lambda *_args: output)
    monkeypatch.setattr(goodvibes, "resolve_input_file", lambda _value: source)
    monkeypatch.setattr(goodvibes, "module_version", lambda _name: "4.3.0")

    def fake_run_external(**kwargs):
        calls.append(kwargs)
        json_name = kwargs["arguments"][kwargs["arguments"].index("--json") + 1]
        (kwargs["directory"] / json_name).write_text(
            json.dumps(_payload(source)), encoding="utf-8"
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "completed",
            "stderr": "",
            "command": ["goodvibes", *kwargs["arguments"]],
        }

    monkeypatch.setattr(goodvibes, "run_external", fake_run_external)
    result = goodvibes.execute(
        "derive_thermochemistry",
        {
            "inputs": {"output_file": "water.log"},
            "method_spec": {},
            "action_settings": _settings(),
            "resource_limits": {"cpu_cores": 2, "walltime_seconds": 30},
        },
    )

    assert result["status"] == "success"
    assert result["backend_version"] == "4.3.0"
    assert result["result"]["goodvibes_schema_version"] == "1.0"
    selected = result["result"]["thermochemistry"]["selected_thermochemistry"]
    assert selected["enthalpy_field"] == "qh_enthalpy"
    assert selected["entropy_field"] == "qh_entropy"
    assert calls[0]["arguments"][calls[0]["arguments"].index("--jobs") + 1] == "2"


def test_goodvibes_label_groups_require_exact_disjoint_members(tmp_path, monkeypatch):
    first = (tmp_path / "first.log").resolve()
    second = (tmp_path / "second.log").resolve()
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")
    lookup = {"first": first, "second": second}
    monkeypatch.setattr(goodvibes, "resolve_input_file", lambda value: lookup[value])

    groups = goodvibes._label_groups(
        {"R": ["first"], "S": ["second"]}, [first, second]
    )
    assert groups == {"R": [str(first)], "S": [str(second)]}
    with pytest.raises(ValueError, match="exactly one label"):
        goodvibes._label_groups(
            {"R": ["first"], "S": ["first"]}, [first, second]
        )

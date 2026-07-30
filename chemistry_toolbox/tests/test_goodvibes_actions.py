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
        _settings(), {"media_solvent": "ethanol"}, temperature_kelvin=298.15
    )
    assert arguments[arguments.index("--vscal") + 1] == "0.99"
    assert arguments[arguments.index("--zpe-vscal") + 1] == "0.98"
    assert arguments[arguments.index("--fs") + 1] == "100"
    assert arguments[arguments.index("--fh") + 1] == "75"
    assert arguments[arguments.index("--bav") + 1] == "global"
    assert arguments[arguments.index("--media") + 1] == "ethanol"


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
            "resource_limits": {"cpu_cores": 2,},
        },
    )

    assert result["status"] == "success"
    assert result["backend_version"] == "4.3.0"
    assert result["result"]["goodvibes_schema_version"] == "1.0"
    selected = result["result"]["thermochemistry"]["selected_thermochemistry"]
    assert selected["enthalpy_field"] == "qh_enthalpy"
    assert selected["entropy_field"] == "qh_entropy"
    assert calls[0]["arguments"][calls[0]["arguments"].index("--jobs") + 1] == "2"
    assert calls[0]["arguments"][0] == str(output / "frequency.log")
    assert result["result"]["staged_inputs"][0]["source_path"] == "water.log"


def test_goodvibes_derive_stages_glob_sensitive_path_and_explicit_spc(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    frequency = tmp_path / "[Int-I]_frequency.log"
    single_point = tmp_path / "separate" / "[Int-I]_dlpno.out"
    single_point.parent.mkdir()
    frequency.write_text("frequency", encoding="utf-8")
    single_point.write_text("single point", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()
    lookup = {"frequency": frequency, "single_point": single_point}
    calls = []

    monkeypatch.setattr(goodvibes, "output_directory", lambda *_args: output)
    monkeypatch.setattr(goodvibes, "resolve_input_file", lambda value: lookup[value])
    monkeypatch.setattr(goodvibes, "module_version", lambda _name: "4.3.0")

    def fake_run_external(**kwargs):
        calls.append(kwargs)
        assert kwargs["arguments"][0] == str(output / "frequency.log")
        assert (output / "frequency_DLPNO.out").read_text(encoding="utf-8") == "single point"
        json_name = kwargs["arguments"][kwargs["arguments"].index("--json") + 1]
        payload = _payload(output / "frequency.log")
        payload["results"][0]["qcdata"].update(
            {"sp_energy": -10.5, "sp_suffix": "DLPNO"}
        )
        (kwargs["directory"] / json_name).write_text(
            json.dumps(payload), encoding="utf-8"
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
            "inputs": {
                "output_file": "frequency",
                "single_point_output_file": "single_point",
            },
            "method_spec": {"single_point_correction_suffix": "DLPNO"},
            "action_settings": _settings(),
            "resource_limits": {"cpu_cores": 1},
        },
    )

    assert result["status"] == "success"
    assert "--spc" in calls[0]["arguments"]
    roles = {item["role"] for item in result["result"]["staged_inputs"]}
    assert roles == {"frequency_output", "single_point_output"}
    manifest = json.loads((output / "staged_input_manifest.json").read_text())
    assert len(manifest) == 2


def test_goodvibes_run_once_escapes_glob_metacharacters(tmp_path, monkeypatch):
    source = tmp_path / "[complex].log"
    source.write_text("test", encoding="utf-8")

    def fake_run_external(**kwargs):
        assert kwargs["arguments"][0] != str(source)
        assert "[[]complex]" in kwargs["arguments"][0]
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
    payload, _completed = goodvibes._run_once(
        directory=tmp_path,
        output_files=[source],
        arguments=[],
        output_stem="escaped",
        timeout_seconds=30,
    )
    assert payload is not None


def test_goodvibes_rejects_unsafe_spc_suffix_before_staging(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    source = tmp_path / "frequency.log"
    source.write_text("test", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()
    monkeypatch.setattr(goodvibes, "output_directory", lambda *_args: output)
    monkeypatch.setattr(goodvibes, "resolve_input_file", lambda _value: source)
    with pytest.raises(ValueError, match="must contain only"):
        goodvibes.execute(
            "derive_thermochemistry",
            {
                "inputs": {"output_file": "frequency.log"},
                "method_spec": {"single_point_correction_suffix": "../../escape"},
                "action_settings": _settings(),
            },
        )
    assert not (tmp_path / "escape.out").exists()


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


def test_goodvibes_validation_avoids_native_check_spc_crash(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    first = (tmp_path / "first.log").resolve()
    second = (tmp_path / "second.log").resolve()
    for path in (first, second, tmp_path / "first_DLPNO.out", tmp_path / "second_DLPNO.out"):
        path.write_text("test", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()
    lookup = {"first": first, "second": second}
    calls = []

    monkeypatch.setattr(goodvibes, "output_directory", lambda *_args: output)
    monkeypatch.setattr(goodvibes, "resolve_input_file", lambda value: lookup[value])
    monkeypatch.setattr(goodvibes, "module_version", lambda _name: "4.3.0")

    def fake_run_external(**kwargs):
        calls.append(kwargs["arguments"])
        files = [Path(item) for item in kwargs["arguments"] if str(item).endswith(".log")]
        payload = _payload(files[0])
        payload["results"] = []
        for path in files:
            entry = _payload(path)["results"][0]
            entry["qcdata"].update(
                {
                    "charge": 0,
                    "multiplicity": 1,
                    "sp_energy": -11.0,
                    "sp_version_program": "ORCA 4.0.1.2",
                    "sp_solvation_model": "SMD,ETHANOL",
                    "sp_charge": 0,
                    "sp_multiplicity": 1,
                    "sp_suffix": "DLPNO",
                }
            )
            payload["results"].append(entry)
        json_name = kwargs["arguments"][kwargs["arguments"].index("--json") + 1]
        (kwargs["directory"] / json_name).write_text(
            json.dumps(payload), encoding="utf-8"
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "checks completed",
            "stderr": "",
            "command": ["goodvibes", *kwargs["arguments"]],
        }

    monkeypatch.setattr(goodvibes, "run_external", fake_run_external)
    settings = _settings(
        duplicate_energy_cutoff_kcal_mol=0.05,
        duplicate_rotational_cutoff_fraction=0.01,
        duplicate_rmsd_cutoff_angstrom=None,
    )
    result = goodvibes.execute(
        "validate_thermochemistry_inputs",
        {
            "inputs": {"output_files": ["first", "second"]},
            "method_spec": {"single_point_correction_suffix": "DLPNO"},
            "action_settings": settings,
            "resource_limits": {"cpu_cores": 1,},
        },
    )

    assert result["status"] == "success"
    assert result["result"]["consistent"] is True
    assert result["result"]["single_point_check_workaround"] is True
    assert len(calls) == 2
    assert "--spc" in calls[0] and "--check" not in calls[0]
    assert "--check" in calls[1] and "--spc" not in calls[1]


def test_validation_keeps_general_solvation_caution_out_of_consistency_issues():
    text = (
        "Caution! Implicit solvation (SMD/CPCM) detected. Enthalpic and entropic "
        "terms cannot be safely separated. Use them at your own risk!\n"
        "Caution! A calculation may not have terminated normally.\n"
    )
    assert goodvibes._validation_issue_lines(text) == [
        "Caution! A calculation may not have terminated normally."
    ]

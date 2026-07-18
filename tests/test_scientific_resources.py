from __future__ import annotations

import json

import pytest

from researchchem_toolbox import resources
from researchchem_toolbox.backends import docking, periodic
from researchchem_toolbox.backends.common import resolve_input_file
from researchchem_toolbox.catalog import catalog_snapshot


def _test_registry(tmp_path, monkeypatch):
    element_root = tmp_path / "elements"
    element_root.mkdir()
    (element_root / "Si.psp8").write_text("pseudo", encoding="utf-8")
    parameter_root = tmp_path / "parameters"
    parameter_root.mkdir()
    (parameter_root / "Si-Si.skf").write_text("sk", encoding="utf-8")
    config = tmp_path / "resources.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "selection_policy": "agent_explicit_no_default",
                "resources": [
                    {
                        "id": "test_pseudos",
                        "display_name": "Test pseudos",
                        "kind": "element_file_collection",
                        "selectable": True,
                        "compatible_backends": ["abinit"],
                        "format": "PSP8",
                        "version": "test",
                        "path": str(element_root),
                        "element_pattern": "{element}.psp8",
                        "expected_file_count": 1,
                    },
                    {
                        "id": "test_parameters",
                        "display_name": "Test SK",
                        "kind": "slater_koster_parameter_set",
                        "selectable": True,
                        "compatible_backends": ["dftbplus"],
                        "format": "SKF",
                        "version": "test",
                        "path": str(parameter_root),
                        "file_glob": "*.skf",
                        "expected_file_count": 1,
                    },
                    {
                        "id": "runtime_binary",
                        "display_name": "Runtime binary",
                        "kind": "backend_executable",
                        "selectable": False,
                        "compatible_backends": ["gnina"],
                        "path": str(tmp_path / "binary"),
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("RESEARCHCHEM_RESOURCE_CONFIG", str(config))
    resources._load_config_at.cache_clear()
    return element_root, parameter_root


def test_registered_resources_require_explicit_family_and_element(tmp_path, monkeypatch):
    element_root, parameter_root = _test_registry(tmp_path, monkeypatch)
    assert resources.resolve_resource_reference("resource://test_pseudos/Si") == element_root / "Si.psp8"
    assert resources.resolve_resource_reference(
        {"resource_id": "test_pseudos", "element": "Si"}
    ) == element_root / "Si.psp8"
    assert resources.resolve_resource_reference("resource://test_parameters") == parameter_root
    with pytest.raises(ValueError, match="requires an explicit chemical element"):
        resources.resolve_resource_reference("resource://test_pseudos")
    with pytest.raises((ValueError, FileNotFoundError), match="does not contain element|missing"):
        resources.resolve_resource_reference("resource://test_pseudos/C")
    with pytest.raises(ValueError, match="runtime-managed"):
        resources.resolve_resource_reference("resource://runtime_binary")
    with pytest.raises(ValueError):
        resources.resolve_resource_reference("resource://test_pseudos/../Si")


def test_common_file_resolver_accepts_only_registered_resource_refs(tmp_path, monkeypatch):
    element_root, _ = _test_registry(tmp_path, monkeypatch)
    assert resolve_input_file("resource://test_pseudos/Si") == element_root / "Si.psp8"
    with pytest.raises(ValueError, match="Unknown scientific resource"):
        resolve_input_file("resource://not_registered/Si")


def test_catalog_exposes_resource_policy_and_coverage(tmp_path, monkeypatch):
    _test_registry(tmp_path, monkeypatch)
    snapshot = catalog_snapshot(include_health=False)
    assert snapshot["scientific_resource_selection_policy"] == "agent_explicit_no_default"
    assert {item["id"] for item in snapshot["resources"]} == {
        "test_pseudos",
        "test_parameters",
        "runtime_binary",
    }
    pseudo = next(item for item in snapshot["resources"] if item["id"] == "test_pseudos")
    assert pseudo["selection_syntax"] == "resource://test_pseudos/<Element>"
    assert pseudo["elements"] == ["Si"]


def test_gnina_adapter_keeps_hardware_and_model_choice_explicit(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    receptor = tmp_path / "receptor.pdbqt"
    ligand = tmp_path / "ligand.pdbqt"
    receptor.write_text("ATOM\n", encoding="utf-8")
    ligand.write_text("ROOT\nENDROOT\nTORSDOF 0\n", encoding="utf-8")
    captured = {}

    def fake_run_external(**kwargs):
        captured.update(kwargs)
        output = kwargs["directory"] / "poses.pdbqt"
        output.write_text(
            "MODEL 1\n"
            "REMARK minimizedAffinity -7.25\n"
            "REMARK CNNscore 0.81\n"
            "REMARK CNNaffinity 6.40\n"
            "ENDMDL\n",
            encoding="utf-8",
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "",
            "stderr": "",
            "command": ["gnina"],
        }

    monkeypatch.setattr(docking, "run_external", fake_run_external)
    result = docking.execute(
        "dock_ligand",
        "gnina",
        {
            "inputs": {
                "receptor": "receptor.pdbqt",
                "ligand": "ligand.pdbqt",
                "search_space": {
                    "center_angstrom": [0, 0, 0],
                    "size_angstrom": [10, 10, 10],
                },
            },
            "method_spec": {"cnn_model": "builtin_default", "cnn_scoring": "rescore"},
            "action_settings": {
                "exhaustiveness": 1,
                "num_modes": 1,
                "use_gpu": False,
                "cpu": 1,
                "seed": 7,
            },
        },
    )
    assert result["status"] == "success"
    assert "--no_gpu" in captured["arguments"]
    assert "--energy_range" not in captured["arguments"]
    assert "--cnn" not in captured["arguments"]
    assert result["result"]["scores"][0]["cnn_pose_score"] == pytest.approx(0.81)


def test_dftb_input_uses_explicit_agent_method_fields(tmp_path, monkeypatch):
    parameter_root = tmp_path / "sk"
    parameter_root.mkdir()
    (parameter_root / "Si-Si.skf").write_text("sk", encoding="utf-8")
    monkeypatch.setattr(periodic, "resolve_input_file", lambda _value: parameter_root)
    structure = {
        "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
        "cell_angstrom": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
        "pbc": [True, True, True],
    }
    path, _arguments, _stdin = periodic._simple_periodic_input(
        "dftbplus",
        "calculate_periodic_energy",
        {
            "inputs": {"structure": structure},
            "method_spec": {
                "parameter_set": "resource://test_parameters",
                "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
                "scc": True,
                "max_angular_momenta": {"Si": "d"},
            },
            "action_settings": {"scc_tolerance": 1e-8, "max_scc_iterations": 100},
        },
        tmp_path,
    )
    text = path.read_text(encoding="utf-8")
    assert 'Si = "d"' in text
    assert "SCC = Yes" in text
    assert "SCCTolerance = 1e-08" in text
    assert "ParserVersion = 14" in text
    assert "Driver = {}" not in text


def test_periodic_parsers_distinguish_atomic_force_and_physical_stress_units(tmp_path):
    qe_stdout = """
     atom    1 type  1   force =     0.10000000    0.20000000    0.30000000
     Total force =     0.374166     Total SCF correction =     0.000000
    """
    request = {
        "inputs": {
            "structure": {
                "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
                "cell_angstrom": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                "pbc": [True, True, True],
            }
        }
    }
    qe = periodic._parse_qe(
        "calculate_periodic_forces", qe_stdout, tmp_path, request
    )
    assert qe["forces"] == [[0.1, 0.2, 0.3]]

    abinit_stdout = """
 Cartesian components of stress tensor (hartree/bohr^3)
  sigma(1 1)= -1.0E-05  sigma(3 2)=  4.0E-06
  sigma(2 2)= -2.0E-05  sigma(3 1)=  5.0E-06
  sigma(3 3)= -3.0E-05  sigma(2 1)=  6.0E-06
 Cartesian components of stress tensor (GPa)
  sigma(1 1)= -9.0E-01  sigma(3 2)=  4.0E-01
  sigma(2 2)= -8.0E-01  sigma(3 1)=  5.0E-01
  sigma(3 3)= -7.0E-01  sigma(2 1)=  6.0E-01
 cartesian forces (hartree/bohr) at end:
    1      0.10000000000000     0.20000000000000     0.30000000000000
 cartesian forces (eV/Angstrom) at end:
    1      5.10000000000000     5.20000000000000     5.30000000000000
    """
    assert periodic._parse_abinit_stress(abinit_stdout) == [
        [-1e-5, 6e-6, 5e-6],
        [6e-6, -2e-5, 4e-6],
        [5e-6, 4e-6, -3e-5],
    ]
    assert periodic._parse_abinit_forces(abinit_stdout, 1) == [[0.1, 0.2, 0.3]]


def test_dftb_relax_driver_uses_parser14_block_structure(tmp_path, monkeypatch):
    parameter_root = tmp_path / "sk"
    parameter_root.mkdir()
    (parameter_root / "Si-Si.skf").write_text("sk", encoding="utf-8")
    monkeypatch.setattr(periodic, "resolve_input_file", lambda _value: parameter_root)
    structure = {
        "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
        "cell_angstrom": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
        "pbc": [True, True, True],
    }
    path, _arguments, _stdin = periodic._simple_periodic_input(
        "dftbplus",
        "relax_periodic_structure",
        {
            "inputs": {"structure": structure},
            "method_spec": {
                "parameter_set": "resource://test_parameters",
                "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
                "scc": True,
                "max_angular_momenta": {"Si": "d"},
            },
            "action_settings": {
                "scc_tolerance": 1e-8,
                "max_scc_iterations": 100,
                "force_threshold_ev_per_angstrom": 0.1,
                "max_steps": 5,
                "relax_cell": False,
            },
        },
        tmp_path,
    )
    text = path.read_text(encoding="utf-8")
    assert "Driver = GeometryOptimization {\n" in text
    assert "  MaxSteps = 5\n" in text
    assert "  Convergence = {\n" in text
    assert "  LatticeOpt = No\n" in text

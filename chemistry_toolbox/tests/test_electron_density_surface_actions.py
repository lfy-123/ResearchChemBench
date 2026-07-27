from __future__ import annotations

import pytest

from researchchem_toolbox import service
from researchchem_toolbox.backends import electronic
from researchchem_toolbox.catalog import action_specs, backend_specs, validate_catalog
from researchchem_toolbox.discovery import inspect_action
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


def test_electron_density_actions_are_catalog_complete():
    validate_catalog()
    actions = action_specs()
    backends = backend_specs()
    assert actions["calculate_correlated_electron_density"].backend_ids == ("orca",)
    assert actions["export_electron_density_grid"].backend_ids == ("orca",)
    assert actions["calculate_electron_isodensity_surface"].backend_ids == ("multiwfn",)
    assert "calculate_correlated_electron_density" in backends["orca"].capabilities
    assert "calculate_electron_isodensity_surface" in backends["multiwfn"].capabilities


def test_multiwfn_surface_contract_uses_bohr_and_documents_legacy_alias():
    contract = inspect_action(
        "calculate_electron_isodensity_surface",
        backend_id="multiwfn",
        snapshot={"actions": [], "backends": [], "resources": [], "catalog_hash": "test"},
    )["selected_request_contract"]

    required = {
        item["name"]: item
        for item in contract["sections"]["action_settings"]["required"]
    }
    optional = {
        item["name"]: item
        for item in contract["sections"]["action_settings"]["optional_documented"]
    }
    assert set(required) == {"cutoffs_au", "grid_spacing_bohr"}
    assert required["grid_spacing_bohr"]["minimum"] == 0.02
    assert required["grid_spacing_bohr"]["maximum"] == 1.0
    assert "bohr" in required["grid_spacing_bohr"]["description"].casefold()
    assert contract["execute_action_request_template"]["action_settings"][
        "grid_spacing_bohr"
    ] == "<number>"

    legacy = optional["grid_spacing_angstrom"]
    assert legacy["deprecated"] is True
    assert legacy["replacement"] == "action_settings.grid_spacing_bohr"
    assert legacy["default"] is None
    assert "interpreted in bohr" in legacy["description"]
    fixed = {
        item["path"]: item for item in contract["backend_fixed_parameters"]
    }
    assert "backend_runtime.native_grid_spacing_unit" in fixed
    assert "backend_runtime.grid_spacing_unit_interpretation" not in fixed


def test_multiwfn_surface_backend_reports_physical_units_and_legacy_warning(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "density.wfn").write_text("wavefunction", encoding="utf-8")
    observed_stdin: list[str] = []

    def fake_run_external(**kwargs):
        observed_stdin.append(kwargs["stdin_text"])
        return {
            "available": True,
            "returncode": 0,
            "stdout": (
                "Loaded density.wfn successfully!\n"
                "Isosurface area: 100.0 Bohr^2 ( 28.0 Angstrom^2)\n"
                "Volume enclosed by the isosurface: 100.0 Bohr^3 "
                "( 14.0 Angstrom^3)\n"
            ),
            "stderr": "",
            "command": ["Multiwfn_noGUI", "density.wfn"],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    canonical = electronic._multiwfn_isodensity_surface(
        {
            "inputs": {"density_file": "density.wfn"},
            "method_spec": {},
            "action_settings": {
                "cutoffs_au": [0.0016],
                "grid_spacing_bohr": 0.1,
            },
            "resource_limits": {},
        }
    )
    assert canonical["status"] == "success"
    assert canonical["result"]["grid_spacing_bohr"] == 0.1
    assert canonical["result"]["grid_spacing_angstrom"] == pytest.approx(
        0.0529177210903
    )
    assert canonical["result"]["grid_spacing_input_field"] == "grid_spacing_bohr"
    assert canonical["warnings"] == []
    assert "\n3\n0.1\n6\n" in observed_stdin[-1]

    legacy = electronic._multiwfn_isodensity_surface(
        {
            "inputs": {"density_file": "density.wfn"},
            "method_spec": {},
            "action_settings": {
                "cutoffs_au": [0.0016],
                "grid_spacing_angstrom": 0.1,
            },
            "resource_limits": {},
        }
    )
    assert legacy["status"] == "success"
    assert legacy["result"]["grid_spacing_bohr"] == 0.1
    assert legacy["result"]["grid_spacing_input_field"] == "grid_spacing_angstrom"
    assert any("deprecated" in warning for warning in legacy["warnings"])


def test_multiwfn_surface_dispatch_accepts_only_one_spacing_field(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "density.wfn").write_text("wavefunction", encoding="utf-8")
    calls = []

    def available(backends):
        return {
            backend.id: {
                "available": True,
                "status": "available",
                "runtime": backend.runtime,
            }
            for backend in backends
        }

    monkeypatch.setattr(service, "probe_all_backends", available)
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **kwargs: calls.append(kwargs)
        or {
            "status": "success",
            "result": {"surfaces": []},
            "warnings": ["legacy alias accepted"],
        },
    )
    legacy = service.execute_action(
        "calculate_electron_isodensity_surface",
        {
            "backend_id": "multiwfn",
            "inputs": {"density_file": "density.wfn"},
            "method_spec": {},
            "action_settings": {
                "cutoffs_au": [0.0016],
                "grid_spacing_angstrom": 0.1,
            },
        },
    )
    assert legacy["status"] == "success"
    assert calls[-1]["payload"]["request"]["action_settings"][
        "grid_spacing_angstrom"
    ] == 0.1

    conflict = service.execute_action(
        "calculate_electron_isodensity_surface",
        {
            "backend_id": "multiwfn",
            "inputs": {"density_file": "density.wfn"},
            "method_spec": {},
            "action_settings": {
                "cutoffs_au": [0.0016],
                "grid_spacing_bohr": 0.1,
                "grid_spacing_angstrom": 0.1,
            },
        },
    )
    assert conflict["status"] == "invalid_request"
    assert conflict["error"]["code"] == "conflicting_setting_aliases"
    assert len(calls) == 1


def test_orca_density_renderer_requests_relaxed_double_hybrid_density():
    rendered = electronic._render_orca_density(
        WATER,
        {
            "method": "DSD-PBEP86",
            "basis": "def2-QZVPD",
            "auxiliary_basis": "def2-TZVPD/C",
            "dispersion": "D3BJ",
            "frozen_core": False,
            "pmodel": True,
            "density_type": "relaxed_mp2",
        },
        {
            "scf_convergence": "VeryTightSCF",
            "max_scf_cycles": 300,
            "stability_analysis": True,
        },
        {"cpu_cores": 16, "memory_mb": 24000},
    )
    assert "DSD-PBEP86 def2-QZVPD def2-TZVPD/C D3BJ NoFrozenCore PModel" in rendered
    assert "%maxcore 1500" in rendered
    assert "nprocs 16" in rendered
    assert "Density relaxed" in rendered
    assert "NatOrbs true" in rendered
    assert "STABPerform true" in rendered


def test_orca_density_renderer_accepts_literature_style_dispersion_alias():
    rendered = electronic._render_orca_density(
        WATER,
        {
            "method": "DSD-PBEP86-D3BJ",
            "basis": "def2-QZVPD",
            "auxiliary_basis": "def2-TZVPD/C",
            "density_type": "relaxed_mp2",
        },
        {
            "scf_convergence": "VeryTightSCF",
            "max_scf_cycles": 300,
            "stability_analysis": False,
        },
        {"cpu_cores": 1, "memory_mb": 2000},
    )

    assert "! DSD-PBEP86 def2-QZVPD def2-TZVPD/C D3BJ" in rendered
    assert "DSD-PBEP86-D3BJ" not in rendered


def test_orca_density_renderer_defaults_to_2000_mb_maxcore_per_process():
    rendered = electronic._render_orca_density(
        WATER,
        {
            "method": "CCSD",
            "basis": "def2-TZVPD",
            "density_type": "unrelaxed_ccsd",
        },
        {
            "scf_convergence": "VeryTightSCF",
            "max_scf_cycles": 300,
            "stability_analysis": False,
        },
        {"cpu_cores": 8},
    )
    assert "%maxcore 2000" in rendered
    assert "nprocs 8" in rendered


def test_orca_density_renderer_rejects_unavailable_ccsd_t_density():
    with pytest.raises(ValueError, match=r"does not provide an unrelaxed CCSD\(T\)"):
        electronic._render_orca_density(
            WATER,
            {
                "method": "CCSD(T)",
                "basis": "def2-TZVPD",
                "density_type": "unrelaxed_ccsd",
            },
            {
                "scf_convergence": "VeryTightSCF",
                "max_scf_cycles": 300,
                "stability_analysis": False,
            },
            {"cpu_cores": 1, "memory_mb": 1500},
        )


def test_orca_correlated_density_uses_short_relative_input_path(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    observed: dict[str, object] = {}

    def fake_run_external(**kwargs):
        observed.update(kwargs)
        directory = kwargs["directory"]
        (directory / "job.gbw").write_bytes(b"gbw")
        (directory / "job.densities").write_bytes(b"densities")
        (directory / "job.densitiesinfo").write_text("density metadata")
        return {
            "available": True,
            "returncode": 0,
            "stdout": (
                "Program Version 6.1.1\n"
                "FINAL SINGLE POINT ENERGY -75.000000000000\n"
                "MDCIP unrelaxed density\n"
                "ORCA TERMINATED NORMALLY\n"
            ),
            "stderr": "",
            "command": ["orca", *kwargs["arguments"]],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    result = electronic._orca_correlated_electron_density(
        {
            "inputs": {"structure": WATER},
            "method_spec": {
                "method": "CCSD",
                "basis": "STO-3G",
                "density_type": "unrelaxed_ccsd",
            },
            "action_settings": {
                "scf_convergence": "TightSCF",
                "max_scf_cycles": 100,
                "stability_analysis": False,
            },
            "resource_limits": {
                "cpu_cores": 1,
                "memory_mb": 1000,
            },
        }
    )

    assert result["status"] == "success"
    assert observed["arguments"] == ["./job.inp"]
    assert result["result"]["files"]["density_info"].endswith("job.densitiesinfo")
    assert result["provenance"]["requested_total_memory_mb"] == 1000
    assert result["provenance"]["orca_maxcore_mb_per_process"] == 1000
    assert result["provenance"]["memory_default_applied"] is False


def test_orca_density_contract_exposes_exact_types_limits_and_memory_mapping():
    contract = inspect_action(
        "calculate_correlated_electron_density",
        backend_id="orca",
        snapshot={"actions": [], "backends": [], "resources": [], "catalog_hash": "test"},
    )["selected_request_contract"]

    settings = {
        item["name"]: item
        for item in contract["sections"]["action_settings"]["required"]
    }
    assert settings["stability_analysis"]["type"] == "boolean"
    assert contract["execute_action_request_template"]["action_settings"][
        "stability_analysis"
    ] == "<boolean>"
    methods = {
        item["name"]: item
        for item in contract["sections"]["method_spec"]["optional_documented"]
    }
    assert methods["frozen_core"]["type"] == "boolean"
    assert methods["pmodel"]["type"] == "boolean"
    assert methods["charge"]["type"] == "integer"
    assert methods["multiplicity"]["type"] == "integer"

    resources = {
        item["name"]: item
        for item in contract["sections"]["resource_limits"][
            "optional_with_defaults"
        ]
    }
    assert "walltime_seconds" not in resources
    assert contract["execution_timeout_policy"] == {
        "execution_class": "compute",
        "timeout_seconds": 7200,
        "source": "evaluation_policy",
        "agent_controllable": False,
    }
    assert resources["cpu_cores"]["maximum"] == 48
    assert "floor(memory_mb / cpu_cores)" in resources["memory_mb"][
        "description"
    ]
    assert resources["memory_mb"]["derived_backend_parameter"]["name"] == (
        "orca_maxcore_mb_per_process"
    )
    assert "2000 MB per process" in resources["memory_mb"]["default_behavior"]


def test_orca_mdci_export_preserves_density_bundle_basename(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    source = tmp_path / "source"
    source.mkdir()
    (source / "job.gbw").write_bytes(b"gbw")
    (source / "job.densities").write_bytes(b"densities")
    (source / "job.densitiesinfo").write_text("density metadata")

    def fake_run_external(**kwargs):
        directory = kwargs["directory"]
        assert kwargs["arguments"] == ["job.gbw", "-i"]
        assert (directory / "job.gbw").is_file()
        assert (directory / "job.densities").is_file()
        assert (directory / "job.densitiesinfo").is_file()
        (directory / "job.eldens.cube").write_text("cube")
        return {
            "available": True,
            "returncode": 0,
            "stdout": "orca_plot completed",
            "stderr": "",
            "command": ["orca_plot", *kwargs["arguments"]],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    monkeypatch.setattr(electronic, "_cube_electron_integral", lambda _path: 10.0)
    result = electronic._orca_export_electron_density(
        {
            "inputs": {
                "electron_density": {
                    "method": "CCSD",
                    "basis": "STO-3G",
                    "density_type": "unrelaxed_ccsd",
                    "files": {
                        "gbw": "source/job.gbw",
                        "density_container": "source/job.densities",
                        "density_info": "source/job.densitiesinfo",
                    },
                }
            },
            "method_spec": {},
            "action_settings": {
                "density_source": "mdci",
                "output_format": "cube",
                "grid_points_per_axis": 60,
            },
            "resource_limits": {},
        }
    )

    assert result["status"] == "success"
    assert result["result"]["output_file"].endswith("job.eldens.cube")
    assert result["result"]["grid_points_per_axis"] == 60


def test_orca_mdci_export_defaults_to_300_grid_points_and_catalog_exposes_control(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    source = tmp_path / "source"
    source.mkdir()
    (source / "job.gbw").write_bytes(b"gbw")
    (source / "job.densities").write_bytes(b"densities")
    (source / "job.densitiesinfo").write_text("density metadata")
    observed: dict[str, str] = {}

    def fake_run_external(**kwargs):
        observed["stdin_text"] = kwargs["stdin_text"]
        directory = kwargs["directory"]
        (directory / "job.eldens.cube").write_text("cube")
        return {
            "available": True,
            "returncode": 0,
            "stdout": "orca_plot completed",
            "stderr": "",
            "command": ["orca_plot", *kwargs["arguments"]],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    monkeypatch.setattr(electronic, "_cube_electron_integral", lambda _path: 10.0)
    result = electronic._orca_export_electron_density(
        {
            "inputs": {
                "electron_density": {
                    "method": "CCSD",
                    "basis": "STO-3G",
                    "density_type": "unrelaxed_ccsd",
                    "files": {
                        "gbw": "source/job.gbw",
                        "density_container": "source/job.densities",
                        "density_info": "source/job.densitiesinfo",
                    },
                }
            },
            "method_spec": {},
            "action_settings": {"density_source": "mdci", "output_format": "cube"},
            "resource_limits": {},
        }
    )

    assert result["status"] == "success"
    assert "300 300 300" in observed["stdin_text"]

    contract = inspect_action(
        "export_electron_density_grid",
        backend_id="orca",
        snapshot={"actions": [], "backends": [], "resources": [], "catalog_hash": "test"},
    )["selected_request_contract"]
    optional = contract["sections"]["action_settings"]["optional_documented"]
    grid = next(item for item in optional if item["name"] == "grid_points_per_axis")
    assert grid["default"] == 300
    assert grid["minimum"] == 20
    assert grid["maximum"] == 400
    assert "cube" in grid["impact"]
    tolerance = next(
        item
        for item in optional
        if item["name"] == "electron_count_tolerance_percent"
    )
    strict = next(
        item
        for item in optional
        if item["name"] == "strict_electron_count_validation"
    )
    assert tolerance["default"] == 0.2
    assert strict["default"] is False


def test_orca_300_grid_rejects_walltime_too_short_for_single_process_export(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    source = tmp_path / "source"
    source.mkdir()
    (source / "job.gbw").write_bytes(b"gbw")
    (source / "job.densities").write_bytes(b"densities")
    (source / "job.densitiesinfo").write_text("density metadata")

    with pytest.raises(ValueError, match="walltime_seconds>=1800"):
        electronic._orca_export_electron_density(
            {
                "inputs": {
                    "electron_density": {
                        "method": "CCSD",
                        "basis": "STO-3G",
                        "density_type": "unrelaxed_ccsd",
                        "electron_count": 10,
                        "files": {
                            "gbw": "source/job.gbw",
                            "density_container": "source/job.densities",
                            "density_info": "source/job.densitiesinfo",
                        },
                    }
                },
                "method_spec": {},
                "action_settings": {
                    "density_source": "mdci",
                    "output_format": "cube",
                },
                "resource_limits": {"walltime_seconds": 600},
            }
        )


def test_real_orca_to_multiwfn_surface_action_chain(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    density = execute_action(
        "calculate_correlated_electron_density",
        {
            "backend_id": "orca",
            "inputs": {"structure": WATER},
            "method_spec": {
                "method": "HF",
                "basis": "STO-3G",
                "density_type": "scf",
            },
            "action_settings": {
                "scf_convergence": "TightSCF",
                "max_scf_cycles": 100,
                "stability_analysis": False,
            },
            "resource_limits": {
                "cpu_cores": 1,
                "memory_mb": 1000,
            },
        },
    )
    assert density["status"] == "success", density.get("error")
    density_artifact = next(
        item
        for item in density["output_artifacts"]
        if item["semantic_type"] == "ElectronDensityResult"
    )

    exported = execute_action(
        "export_electron_density_grid",
        {
            "backend_id": "orca",
            "inputs": {"electron_density": density_artifact},
            "method_spec": {},
            "action_settings": {"density_source": "scf", "output_format": "wfn"},
            "resource_limits": {
                "cpu_cores": 1,
                "memory_mb": 1000,
            },
        },
    )
    assert exported["status"] == "success", exported.get("error")
    wavefunction = next(
        item
        for item in exported["output_artifacts"]
        if item["semantic_type"] == "ElectronDensityWavefunction"
        and item["path"].endswith(".wfn")
    )

    surfaces = execute_action(
        "calculate_electron_isodensity_surface",
        {
            "backend_id": "multiwfn",
            "inputs": {"density_file": wavefunction},
            "method_spec": {},
            "action_settings": {
                "cutoffs_au": [0.001, 0.002],
                "grid_spacing_bohr": 0.2,
            },
            "resource_limits": {
                "cpu_cores": 2,
                "memory_mb": 1000,
            },
        },
    )
    assert surfaces["status"] == "success", surfaces.get("error")
    assert [item["cutoff_au"] for item in surfaces["result"]["surfaces"]] == [
        0.001,
        0.002,
    ]
    assert all(
        item["surface_area_angstrom2"] > 0
        and item["enclosed_volume_angstrom3"] > 0
        for item in surfaces["result"]["surfaces"]
    )
    assert surfaces["result"]["grid_spacing_bohr"] == 0.2
    assert surfaces["result"]["grid_spacing_angstrom"] == pytest.approx(
        0.1058354421806
    )

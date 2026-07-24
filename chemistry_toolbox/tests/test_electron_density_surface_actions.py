from __future__ import annotations

import pytest

from researchchem_toolbox.backends import electronic
from researchchem_toolbox.catalog import action_specs, backend_specs, validate_catalog
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
                "walltime_seconds": 120,
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
                "walltime_seconds": 120,
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
                "grid_spacing_angstrom": 0.2,
            },
            "resource_limits": {
                "cpu_cores": 2,
                "memory_mb": 1000,
                "walltime_seconds": 120,
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

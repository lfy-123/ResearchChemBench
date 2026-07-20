from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from researchchem_toolbox.catalog import action_specs, backend_specs, validate_catalog
from researchchem_toolbox.service import execute_action


ROOT = Path(__file__).resolve().parents[1]


def test_critic2_electron_density_topology_real_cube(tmp_path, monkeypatch):
    source = (
        ROOT
        / ".software_cache"
        / "gaussian"
        / "g16"
        / "install"
        / "g16"
        / "tests"
        / "test0677-ref.cube"
    )
    density = tmp_path / "density.cube"
    shutil.copy2(source, density)
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    result = execute_action(
        "analyze_electron_density_topology",
        {
            "backend_id": "critic2",
            "inputs": {"density_file": "density.cube"},
            "method_spec": {},
            "action_settings": {
                "system_type": "molecule",
                "density_format": "cube",
                "interpolation": "tricubic",
                "critical_point_types": ["nucleus", "bond", "ring", "cage"],
                "gradient_tolerance": 1e-10,
                "seed_strategy": "default",
                "report_detail": "short",
                "max_reported_critical_points": 12,
            },
            "resource_limits": {
                "cpu_cores": 1,
                "memory_mb": 1024,
                "walltime_seconds": 120,
            },
        },
    )

    assert result["status"] == "success"
    payload = result["result"]
    assert payload["nonequivalent_critical_point_count"] >= 4
    assert payload["reported_critical_point_count"] == 12
    assert payload["critical_points_truncated"] is True
    assert payload["counts_by_type"]["bond"] > 0
    assert payload["counts_by_type"]["ring"] > 0
    assert payload["critical_points"][0]["cartesian_coordinates_angstrom"]
    assert result["backend_version"] == "1.2.1081"
    assert result["output_artifacts"]


def test_critic2_is_an_atomic_catalog_backend():
    validate_catalog()
    action = action_specs()["analyze_electron_density_topology"]
    backend = backend_specs()["critic2"]
    assert action.backend_ids == ("critic2",)
    assert backend.capabilities == (
        "analyze_electron_density_topology",
        "calculate_atomic_basin_properties",
        "calculate_bader_charges",
    )
    assert "run_critic2" not in action_specs()


@pytest.mark.parametrize(
    ("action_id", "partition_method", "result_key"),
    [
        ("calculate_atomic_basin_properties", "yu_trinkle", "basins"),
        ("calculate_bader_charges", "henkelman_bader", "charges"),
    ],
)
def test_critic2_grid_basin_integrations(
    tmp_path, monkeypatch, action_id, partition_method, result_key
):
    source = (
        ROOT
        / ".software_cache"
        / "gaussian"
        / "g16"
        / "install"
        / "g16"
        / "tests"
        / "test0677-ref.cube"
    )
    shutil.copy2(source, tmp_path / "density.cube")
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        action_id,
        {
            "backend_id": "critic2",
            "inputs": {"density_file": "density.cube"},
            "method_spec": {},
            "action_settings": {
                "system_type": "molecule",
                "density_format": "cube",
                "interpolation": "tricubic",
                "partition_method": partition_method,
                "non_nuclear_maxima": False,
                "all_maxima_non_atomic": False,
                "write_weight_cubes": False,
                "max_reported_basins": 5,
                "laplacian_sum_tolerance": 1e-6,
            },
            "resource_limits": {
                "cpu_cores": 1,
                "memory_mb": 1024,
                "walltime_seconds": 120,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["basin_count"] > 0
    assert len(result["result"][result_key]) == 5
    assert result["result"]["basins_truncated"] is True
    assert abs(result["result"]["integrated_laplacian_sum"]) <= 1e-6

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from researchchem_toolbox.backends import periodic
from researchchem_toolbox.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
TDEP = ROOT / ".software_cache" / "tdep" / "25.03" / "source"
FIXTURES = TDEP / "tests" / "infiles"
RUNTIME = ROOT / ".envs" / "kinetics-legacy"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


def _configure(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("LD_LIBRARY_PATH", str(RUNTIME / "lib"))
    monkeypatch.setenv(
        "CHEMGRAPH_TDEP_EXTRACT_FORCECONSTANTS_COMMAND",
        str(TDEP / "bin" / "extract_forceconstants"),
    )
    monkeypatch.setenv(
        "CHEMGRAPH_TDEP_CANONICAL_CONFIGURATION_COMMAND",
        str(TDEP / "bin" / "canonical_configuration"),
    )
    monkeypatch.setenv(
        "CHEMGRAPH_TDEP_PHONON_DISPERSION_COMMAND",
        str(TDEP / "bin" / "phonon_dispersion_relations"),
    )


def _copy(tmp_path: Path, source_name: str, target_name: str | None = None) -> Path:
    return Path(shutil.copy2(FIXTURES / source_name, tmp_path / (target_name or source_name)))


def test_tdep_fits_effective_force_constants_from_official_fixture(tmp_path, monkeypatch):
    _configure(monkeypatch, tmp_path)
    result = _execute(
        "fit_effective_force_constants",
        "tdep",
        {
            "inputs": {
                "unit_cell_file": str(_copy(tmp_path, "infile.ucposcar", "unit.poscar")),
                "supercell_file": str(_copy(tmp_path, "infile.ssposcar", "super.poscar")),
                "simulation_file": str(_copy(tmp_path, "infile.sim.hdf5", "simulation.hdf5")),
                "loto_splitting_file": str(_copy(tmp_path, "infile.lotosplitting", "loto.dat")),
            },
            "method_spec": {},
            "action_settings": {
                "second_order_cutoff_angstrom": 0.0,
                "third_order_cutoff_angstrom": 0.0,
                "fourth_order_cutoff_angstrom": None,
                "polar": True,
                "configuration_stride": 1,
                "include_first_order": False,
                "self_consistent_temperature_kelvin": None,
                "enforce_rotational_invariance": True,
                "enforce_huang_invariance": True,
                "enforce_hermitian_symmetry": True,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 30},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["cross_validation_r_squared"] == pytest.approx(0.75292)
    assert result["result"]["third_order_force_constants_file"] is not None


def test_tdep_generates_canonical_thermal_configurations(tmp_path, monkeypatch):
    _configure(monkeypatch, tmp_path)
    unit = _copy(tmp_path, "infile.ucposcar", "unit.poscar")
    supercell = _copy(tmp_path, "infile.ucposcar", "super.poscar")
    result = _execute(
        "generate_thermal_displacement_configurations",
        "tdep",
        {
            "inputs": {"unit_cell_file": str(unit), "supercell_file": str(supercell)},
            "method_spec": {},
            "action_settings": {
                "temperature_kelvin": 300.0,
                "configuration_count": 2,
                "statistics": "classical",
                "output_format": "vasp",
                "initialization_source": "debye_temperature",
                "debye_temperature_kelvin": 400.0,
                "maximum_frequency_thz": None,
                "minimum_distance_ratio": None,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 30},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["configuration_count"] == 2
    assert all(item["structure"]["pbc"] == [True, True, True] for item in result["result"]["configurations"])


def test_tdep_calculates_effective_phonon_dispersion(tmp_path, monkeypatch):
    _configure(monkeypatch, tmp_path)
    result = _execute(
        "calculate_temperature_dependent_phonon_dispersion",
        "tdep",
        {
            "inputs": {
                "unit_cell_file": str(_copy(tmp_path, "infile.ucposcar", "unit.poscar")),
                "second_order_force_constants_file": str(_copy(tmp_path, "infile.forceconstant", "fc2.dat")),
            },
            "method_spec": {},
            "action_settings": {
                "frequency_unit": "thz",
                "points_per_segment": 20,
                "calculate_gruneisen": False,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 30},
        },
    )
    assert result["status"] == "success"
    assert len(result["result"]["path_coordinate"]) > 20
    assert len(result["result"]["frequencies"][0]) == 6

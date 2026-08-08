from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from chemistry_toolbox.src.backends import periodic, structure
from chemistry_toolbox.src.backends.common import structure_from_atoms
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".software_cache" / "installations" / "vaspkit" / "1.5.1"
STATE = ROOT / ".software_cache" / "state" / "vaspkit" / "1.5.1"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)
PACKAGE = CACHE / "vaspkit.1.5.1"
EXAMPLE = PACKAGE / "examples" / "ZnO_optimization"


pytestmark = pytest.mark.skipif(
    not (PACKAGE / "bin" / "vaspkit").is_file(),
    reason="VASPKIT cannot be redistributed; download 1.5.1 from the official SourceForge release",
)


def _configure(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_VASPKIT_COMMAND", str(PACKAGE / "bin" / "vaspkit"))
    monkeypatch.setenv("CHEMGRAPH_VASPKIT_CONFIG", str(STATE / "home" / ".vaspkit"))


def _stage(tmp_path: Path) -> dict[str, Path]:
    return {
        name: Path(shutil.copy2(EXAMPLE / name, tmp_path / name))
        for name in ("POSCAR", "INCAR", "EIGENVAL", "DOSCAR", "OUTCAR")
    }


def test_vaspkit_generates_explicit_kpoint_mesh(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    files = _stage(tmp_path)
    result = _execute(
        "generate_vasp_kpoint_mesh", "vaspkit",
        {
            "inputs": {"structure_file": str(files["POSCAR"])},
            "method_spec": {},
            "action_settings": {
                "reciprocal_space_resolution_inverse_angstrom": 0.04,
                "centering_scheme": "gamma",
            },
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["grid"] == [12, 12, 5]
    assert result["result"]["potcar_generated"] is False
    assert (tmp_path / result["result"]["kpoint_file"]).is_file()


def test_vaspkit_extracts_band_gap_through_service(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    files = _stage(tmp_path)
    result = execute_action(
        "extract_vasp_band_gap",
        {
            "backend_id": "vaspkit",
            "inputs": {
                "structure_file": str(files["POSCAR"]),
                "incar_file": str(files["INCAR"]),
                "eigenvalue_file": str(files["EIGENVAL"]),
                "dos_file": str(files["DOSCAR"]),
                "outcar_file": str(files["OUTCAR"]),
            },
            "method_spec": {},
            "action_settings": {"set_fermi_energy_zero": True},
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["band_character"] == "direct"
    assert result["result"]["band_gap_ev"] == pytest.approx(0.7667, abs=1e-4)
    assert result["result"]["vbm_band_index"] == 18
    assert result["result"]["cbm_band_index"] == 19


def test_vaspkit_reports_symmetry_and_equivalent_atoms(tmp_path, monkeypatch):
    from ase.io import read

    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    files = _stage(tmp_path)
    result = _execute(
        "analyze_crystal_symmetry", "vaspkit",
        {
            "inputs": {"structure": structure_from_atoms(read(files["POSCAR"]))},
            "method_spec": {},
            "action_settings": {
                "symmetry_tolerance_angstrom": 1e-5,
                "angle_tolerance_degrees": 0.2,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 30},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["space_group_number"] == 186
    assert result["result"]["international_symbol"] == "P6_3mc"
    assert result["result"]["equivalent_atom_groups"] == [[0, 1], [2, 3]]

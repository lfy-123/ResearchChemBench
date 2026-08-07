from __future__ import annotations

import os
from pathlib import Path

import pytest

from chemistry_toolbox.src.backends import reaction
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".software_cache" / "installations" / "pyfrag" / "2019"
SOURCE = ROOT / ".software_cache" / "sources" / "pyfrag" / "2019" / "source"
VALIDATION = ROOT / ".software_cache" / "validation" / "pyfrag" / "2019" / "smoke"
ORCA = ROOT / ".software_cache" / "installations" / "orca" / "6.1.1"
OPENMPI = ROOT / ".software_cache" / "shared" / "mpi" / "openmpi" / "4.1.8-fortran"
EXAMPLE_PATH = SOURCE / "host" / "standalone" / "orca" / "example" / "irc.amv"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


pytestmark = pytest.mark.skipif(
    not (CACHE / "bin" / "pyfrag-orca").is_file() or not (ORCA / "orca").is_file(),
    reason="PyFrag source and separately downloaded ORCA runtime are required",
)


def _configure(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_PYFRAG_COMMAND", str(CACHE / "bin" / "pyfrag-orca"))
    monkeypatch.setenv(
        "PATH",
        os.pathsep.join((str(ORCA), str(OPENMPI / "bin"), os.environ.get("PATH", ""))),
    )
    monkeypatch.setenv(
        "LD_LIBRARY_PATH",
        os.pathsep.join((str(OPENMPI / "lib"), os.environ.get("LD_LIBRARY_PATH", ""))),
    )
    monkeypatch.setenv("OPAL_PREFIX", str(OPENMPI))
    monkeypatch.setenv("OMPI_ALLOW_RUN_AS_ROOT", "1")
    monkeypatch.setenv("OMPI_ALLOW_RUN_AS_ROOT_CONFIRM", "1")
    monkeypatch.setenv("OMPI_MCA_pml", "ob1")
    monkeypatch.setenv("OMPI_MCA_btl", "self,vader,tcp")


def _analysis_request(path: Path) -> dict:
    return {
        "inputs": {"reaction_path_file": str(path)},
        "method_spec": {
            "orca_keywords": ["SP", "B3LYP", "6-31G(d)"],
            "charge": 0,
            "multiplicity": 1,
        },
        "action_settings": {
            "path_format": "amv",
            "path_type": "irc",
            "fragment_1_name": "pd",
            "fragment_2_name": "cc",
            "fragment_1_atom_indices": [1, 2],
            "fragment_2_atom_indices": [3, 4],
            "fragment_1_reference_energy_kcal_mol": 100.0,
            "fragment_2_reference_energy_kcal_mol": 200.0,
            "reaction_coordinate_atom_indices": [1, 3],
            "maximum_path_points": 2,
        },
        "resource_limits": {"cpu_cores": 1, "memory_mb": 4096, "walltime_seconds": 300},
    }


def test_pyfrag_runs_real_orca_activation_strain_profile(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    staged_path = tmp_path / "irc.amv"
    staged_path.write_bytes(EXAMPLE_PATH.read_bytes())

    result = _execute(
        "analyze_activation_strain_profile", "pyfrag", _analysis_request(staged_path)
    )

    assert result["status"] == "success"
    assert result["result"]["path_point_count"] == 2
    assert result["result"]["normal_orca_calculation_count"] == 6
    assert result["result"]["maximum_energy_closure_error_kcal_mol"] < 0.001
    assert result["result"]["fragment_definitions"][0]["atom_indices"] == [1, 2]


def test_pyfrag_summary_and_validation_parse_existing_native_table(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    profile = tmp_path / "fragment_energies.txt"
    profile.write_bytes(
        (VALIDATION / "orca-final" / "fragment_energies.txt").read_bytes()
    )

    summary = _execute(
        "summarize_activation_strain_profile",
        "pyfrag",
        {
            "inputs": {"profile_file": str(profile)},
            "action_settings": {"maximum_records": 10},
        },
    )
    validation = _execute(
        "validate_activation_strain_profile",
        "pyfrag",
        {
            "inputs": {"profile_file": str(profile)},
            "action_settings": {
                "energy_closure_tolerance_kcal_mol": 0.001,
                "expected_path_point_count": 2,
            },
        },
    )

    assert summary["status"] == "success"
    assert summary["result"]["total_record_count"] == 2
    assert validation["status"] == "success"
    assert validation["result"]["passed"] is True


def test_pyfrag_rejects_nonpartitioned_fragments_before_execution(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    staged_path = tmp_path / "irc.amv"
    staged_path.write_bytes(EXAMPLE_PATH.read_bytes())
    request = _analysis_request(staged_path)
    request["action_settings"]["fragment_2_atom_indices"] = [2, 3]

    with pytest.raises(ValueError, match="disjoint"):
        reaction.execute("analyze_activation_strain_profile", "pyfrag", request)

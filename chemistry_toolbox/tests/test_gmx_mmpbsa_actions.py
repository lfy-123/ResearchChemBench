from __future__ import annotations

import os
import shutil
from pathlib import Path

from researchchem_toolbox.backends import dynamics
from researchchem_toolbox.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".software_cache" / "gmx_mmpbsa" / "1.6.5"
RUNTIME = CACHE / "env"
EXAMPLES = CACHE / "smoke" / "gmx_MMPBSA_test" / "examples"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


def _configure_runtime(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_GMX_MMPBSA_COMMAND", str(RUNTIME / "bin" / "gmx_MMPBSA"))
    monkeypatch.setenv("AMBERHOME", str(RUNTIME))
    monkeypatch.setenv("OMPI_ALLOW_RUN_AS_ROOT", "1")
    monkeypatch.setenv("OMPI_ALLOW_RUN_AS_ROOT_CONFIRM", "1")
    monkeypatch.setenv("PATH", f"{RUNTIME / 'bin'}:{os.environ.get('PATH', '')}")
    monkeypatch.setenv("LD_LIBRARY_PATH", f"{RUNTIME / 'lib'}:{os.environ.get('LD_LIBRARY_PATH', '')}")


def _stage_fixture(tmp_path: Path, name: str) -> Path:
    return Path(shutil.copytree(EXAMPLES / name, tmp_path / "fixture"))


def _request(source: Path, *, decomposition: bool) -> dict:
    supporting = [
        {"source": str(path), "target": str(path.relative_to(source))}
        for path in sorted((source / "toppar").glob("*.itp"))
    ]
    settings = {"overwrite": True}
    if decomposition:
        settings["maximum_decomposition_records"] = 20
    return {
        "inputs": {
            "calculation_input": str(source / "mmpbsa.in"),
            "complex_structure": str(source / "com.tpr"),
            "complex_index": str(source / "index.ndx"),
            "complex_trajectory": str(source / "com_traj.xtc"),
            "complex_topology": str(source / "topol.top"),
            "supporting_files": supporting,
        },
        "method_spec": {"receptor_group_index": 3, "ligand_group_index": 4},
        "action_settings": settings,
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 600},
    }


def test_gmx_mmpbsa_calculates_official_protein_ligand_fixture(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    result = _execute(
        "calculate_end_state_binding_free_energy",
        "gmx_mmpbsa",
        _request(_stage_fixture(tmp_path, "Protein_ligand/ST"), decomposition=False),
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "1.6.5"
    total = result["result"]["models"]["generalized_born"]["total"]
    assert total["average_kcal_per_mol"] == -15.02
    assert total["sample_sd_kcal_per_mol"] == 1.69
    assert (tmp_path / result["result"]["results_file"]).is_file()
    assert (tmp_path / result["result"]["frame_energy_file"]).is_file()


def test_gmx_mmpbsa_calculates_and_aggregates_official_decomposition_fixture(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    result = _execute(
        "calculate_end_state_energy_decomposition",
        "gmx_mmpbsa",
        _request(_stage_fixture(tmp_path, "Decomposition_analysis"), decomposition=True),
    )
    assert result["status"] == "success"
    decomposition = result["result"]["decomposition"]
    assert decomposition["record_count"] == 153
    assert decomposition["returned_record_count"] == 20
    assert decomposition["truncated"] is True
    assert all(item["frame_count"] == 10 for item in decomposition["records_sorted_by_absolute_total"])
    assert decomposition["records_sorted_by_absolute_total"][0]["system"] == "ligand"
    assert decomposition["records_sorted_by_absolute_total"][0]["residue"] == "L:B:ARG:9"


def test_gmx_mmpbsa_summarizes_existing_results_and_dispatches(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    source = EXAMPLES / "Decomposition_analysis"
    results = Path(shutil.copy2(source / "FINAL_RESULTS_MMPBSA.dat", tmp_path / "results.dat"))
    decomposition = Path(shutil.copy2(source / "FINAL_DECOMP_MMPBSA.csv", tmp_path / "decomposition.csv"))
    response = execute_action(
        "summarize_end_state_free_energy_results",
        {
            "backend_id": "gmx_mmpbsa",
            "inputs": {"results_file": str(results), "decomposition_file": str(decomposition)},
            "method_spec": {},
            "action_settings": {"maximum_decomposition_records": 5},
            "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
        },
    )
    assert response["status"] == "success", response
    assert response["backend_version"] == "1.6.5"
    assert response["result"]["models"]["generalized_born"]["total"]["average_kcal_per_mol"] == -28.81
    assert response["result"]["decomposition"]["record_count"] == 153
    assert response["result"]["decomposition"]["returned_record_count"] == 5

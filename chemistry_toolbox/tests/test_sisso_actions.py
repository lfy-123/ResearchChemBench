from __future__ import annotations

import os
import shutil
from pathlib import Path

from chemistry_toolbox.src.backends import cheminformatics
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".software_cache" / "installations" / "sisso" / "3.5"
RUNTIME = ROOT / ".envs" / "kinetics-legacy"
MPI = CACHE / "toolchain" / "oneapi" / "mpi" / "2021.15"
DATASET = ROOT / "chemistry_toolbox" / "examples" / "integration" / "sisso" / "regression.csv"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


def _configure_runtime(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_SISSO_COMMAND", str(CACHE / "bin" / "SISSO_run"))
    monkeypatch.setenv("CHEMGRAPH_SISSO_PREDICT_COMMAND", str(CACHE / "bin" / "SISSO_predict"))
    monkeypatch.setenv("CHEMGRAPH_SISSO_MPIRUN_COMMAND", str(MPI / "bin" / "mpirun"))
    monkeypatch.setenv("I_MPI_ROOT", str(MPI))
    monkeypatch.setenv("PATH", f"{CACHE / 'bin'}:{MPI / 'bin'}:{RUNTIME / 'bin'}:{os.environ.get('PATH', '')}")
    monkeypatch.setenv("LD_LIBRARY_PATH", f"{MPI / 'lib'}:{RUNTIME / 'lib'}:{os.environ.get('LD_LIBRARY_PATH', '')}")


def _discovery_request(dataset: Path) -> dict:
    return {
        "inputs": {"dataset": str(dataset)},
        "method_spec": {
            "sample_id_column": "material",
            "target_column": "target",
            "feature_columns": ["f1", "f2", "f3"],
            "training_sample_ids": ["s1", "s2", "s3", "s4", "s5", "s6"],
            "validation_sample_ids": ["s7", "s8"],
            "feature_unit_groups": [[1, 2], [3, 3]],
            "operators": ["(*)"],
            "descriptor_dimension": 1,
            "feature_complexity": 1,
            "sis_subspace_size": 20,
            "sparsification_method": "L0",
            "fit_intercept": True,
            "selection_metric": "RMSE",
        },
        "action_settings": {
            "feature_storage_mode": 1,
            "feature_minimum_absolute_max": 1e-8,
            "feature_maximum_absolute_max": 1e8,
            "number_of_models": 5,
            "mpi_processes": 1,
            "maximum_prediction_records": 10,
        },
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 120},
    }


def _stage_dataset(tmp_path: Path) -> Path:
    return Path(shutil.copy2(DATASET, tmp_path / "regression.csv"))


def test_sisso_discovers_and_validates_exact_sparse_descriptor(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    result = _execute(
        "discover_sparse_symbolic_descriptor", "sisso", _discovery_request(_stage_dataset(tmp_path))
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "3.5"
    assert result["result"]["descriptors"][0]["expression"] == "(f1*f2)"
    assert abs(result["result"]["coefficients"][0] - 2.0) < 1e-10
    assert abs(result["result"]["intercept"] - 1.0) < 1e-10
    assert result["result"]["training_rmse"] < 1e-10
    assert result["result"]["validation"]["rmse"] < 1e-10
    assert [item["sample_id"] for item in result["result"]["validation"]["predictions"]] == ["s7", "s8"]


def test_sisso_evaluates_existing_model_with_official_predictor(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    dataset = _stage_dataset(tmp_path)
    fitted = _execute(
        "discover_sparse_symbolic_descriptor", "sisso", _discovery_request(dataset)
    )
    evaluated = _execute(
        "evaluate_sparse_symbolic_descriptor",
        "sisso",
        {
            "inputs": {"model_output": str(tmp_path / fitted["result"]["model_output"]), "dataset": str(dataset)},
            "method_spec": {
                "sample_id_column": "material",
                "target_column": "target",
                "feature_columns": ["f1", "f2", "f3"],
                "descriptor_dimension": 1,
            },
            "action_settings": {"maximum_prediction_records": 4},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 120},
        },
    )
    assert evaluated["status"] == "success"
    assert evaluated["result"]["evaluation"]["sample_count"] == 8
    assert evaluated["result"]["evaluation"]["returned_prediction_count"] == 4
    assert evaluated["result"]["evaluation"]["truncated"] is True
    assert evaluated["result"]["evaluation"]["rmse"] < 1e-10


def test_sisso_summarizes_existing_model_and_predictions_through_service(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    dataset = _stage_dataset(tmp_path)
    fitted = _execute(
        "discover_sparse_symbolic_descriptor", "sisso", _discovery_request(dataset)
    )
    request = {
        "backend_id": "sisso",
        "inputs": {
            "model_output": str(tmp_path / fitted["result"]["model_output"]),
            "prediction_output": str(tmp_path / fitted["result"]["prediction_output"]),
        },
        "method_spec": {},
        "action_settings": {"maximum_prediction_records": 1},
        "resource_limits": {"cpu_cores": 1, "memory_mb": 1024},
    }
    response = execute_action("summarize_sparse_symbolic_descriptor_results", request)
    assert response["status"] == "success", response
    assert response["result"]["model"]["descriptors"][0]["expression"] == "(f1*f2)"
    assert response["result"]["evaluation"]["sample_count"] == 2
    assert response["result"]["evaluation"]["returned_prediction_count"] == 1

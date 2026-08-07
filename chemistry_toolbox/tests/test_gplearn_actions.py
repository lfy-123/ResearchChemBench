from __future__ import annotations

import math
import shutil
from pathlib import Path

import pytest

from chemistry_toolbox.src.backends import cheminformatics
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "chemistry_toolbox" / "examples" / "integration" / "sisso" / "regression.csv"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


def _request(dataset: Path, *, seed: int = 7) -> dict:
    return {
        "inputs": {"dataset": str(dataset)},
        "method_spec": {
            "sample_id_column": "material",
            "target_column": "target",
            "feature_columns": ["f1", "f2", "f3"],
            "training_sample_ids": ["s1", "s2", "s3", "s4", "s5", "s6"],
            "validation_sample_ids": ["s7", "s8"],
            "function_set": ["add", "sub", "mul"],
            "metric": "rmse",
        },
        "action_settings": {
            "population_size": 500,
            "generations": 12,
            "tournament_size": 20,
            "stopping_criteria": 0.0,
            "const_range": [-3.0, 3.0],
            "init_depth": [2, 5],
            "init_method": "half and half",
            "parsimony_coefficient": 0.001,
            "p_crossover": 0.8,
            "p_subtree_mutation": 0.05,
            "p_hoist_mutation": 0.03,
            "p_point_mutation": 0.05,
            "p_point_replace": 0.05,
            "max_samples": 1.0,
            "low_memory": True,
            "n_jobs": 1,
            "random_seed": seed,
            "maximum_prediction_records": 1,
        },
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 120},
    }


def _stage(tmp_path: Path) -> Path:
    return Path(shutil.copy2(DATASET, tmp_path / "regression.csv"))


def test_gplearn_fits_reproducible_held_out_baseline(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _request(_stage(tmp_path))
    first = _execute("fit_symbolic_regression_baseline", "gplearn", request)
    second = _execute("fit_symbolic_regression_baseline", "gplearn", request)

    assert first["status"] == "success"
    assert first["backend_version"] == "0.4.3"
    assert first["result"]["expression"] == second["result"]["expression"]
    assert first["result"]["validation"]["rmse"] == second["result"]["validation"]["rmse"]
    assert math.isfinite(first["result"]["validation"]["rmse"])
    assert first["result"]["validation"]["returned_prediction_count"] == 1
    assert first["result"]["validation"]["truncated"] is True
    assert (tmp_path / first["result"]["results_file"]).is_file()


def test_gplearn_reports_cross_seed_stability(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _request(_stage(tmp_path))
    request["action_settings"].pop("random_seed")
    request["action_settings"].update(
        {"random_seeds": [2, 3, 7], "population_size": 300, "generations": 8}
    )
    result = _execute(
        "assess_symbolic_regression_seed_stability", "gplearn", request
    )

    assert result["status"] == "success"
    assert result["result"]["seed_count"] == 3
    assert len(result["result"]["runs"]) == 3
    assert 1 <= result["result"]["unique_expression_count"] <= 3
    assert math.isfinite(result["result"]["validation_rmse_sample_standard_deviation"])


def test_gplearn_summary_uses_json_and_rejects_split_leakage(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _request(_stage(tmp_path))
    fitted = _execute("fit_symbolic_regression_baseline", "gplearn", request)
    summarized = execute_action(
        "summarize_symbolic_regression_results",
        {
            "backend_id": "gplearn",
            "inputs": {"results_file": str(tmp_path / fitted["result"]["results_file"])},
            "method_spec": {},
            "action_settings": {"maximum_prediction_records": 1},
        },
    )
    assert summarized["status"] == "success"
    assert summarized["result"]["summary"]["expression"] == fitted["result"]["expression"]

    request["method_spec"]["validation_sample_ids"] = ["s6", "s7"]
    with pytest.raises(ValueError, match="overlap"):
        cheminformatics.execute("fit_symbolic_regression_baseline", "gplearn", request)

"""Atomic local cheminformatics actions."""

from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
from pathlib import Path
from typing import Any

from .common import (
    command_artifacts,
    module_version,
    output_directory,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    run_external,
    structure_dict,
    success,
    unavailable,
    unsupported,
)


ACTIONS = {
    "calculate_molecular_descriptors",
    "calculate_molecular_fingerprint",
    "calculate_molecular_similarity",
    "search_local_substructures",
    "enumerate_tautomers",
    "enumerate_stereoisomers",
    "discover_sparse_symbolic_descriptor",
    "evaluate_sparse_symbolic_descriptor",
    "summarize_sparse_symbolic_descriptor_results",
    "fit_symbolic_regression_baseline",
    "assess_symbolic_regression_seed_stability",
    "summarize_symbolic_regression_results",
}


_SISSO_OPERATORS = {
    "(+)", "(-)", "(*)", "(/)", "(exp)", "(exp-)", "(^-1)", "(^2)",
    "(^3)", "(sqrt)", "(cbrt)", "(log)", "(|-|)", "(scd)", "(^6)",
    "(sin)", "(cos)",
}
_SISSO_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,29}$")
_SISSO_SAMPLE_ID = re.compile(r"^[A-Za-z0-9_.:+-]+$")


def _sisso_table(
    path: Path,
    sample_id_column: str,
    target_column: str,
    feature_columns: list[str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if not feature_columns or len(feature_columns) > 10000 or len(set(feature_columns)) != len(feature_columns):
        raise ValueError("feature_columns must contain between 1 and 10000 unique names")
    for name in [sample_id_column, target_column, *feature_columns]:
        if not _SISSO_NAME.fullmatch(str(name)):
            raise ValueError(f"SISSO column name must match {_SISSO_NAME.pattern}: {name}")
    if len({sample_id_column, target_column, *feature_columns}) != len(feature_columns) + 2:
        raise ValueError("sample ID, target, and feature columns must be distinct")
    with path.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("dataset must be a CSV file with a header")
        missing = [name for name in [sample_id_column, target_column, *feature_columns] if name not in reader.fieldnames]
        if missing:
            raise ValueError(f"dataset is missing required columns: {missing}")
        rows = []
        indexed = {}
        for line_number, source in enumerate(reader, start=2):
            sample_id = str(source[sample_id_column]).strip()
            if not _SISSO_SAMPLE_ID.fullmatch(sample_id):
                raise ValueError(f"Invalid SISSO sample ID at CSV line {line_number}: {sample_id!r}")
            if sample_id in indexed:
                raise ValueError(f"Duplicate sample ID: {sample_id}")
            try:
                target = float(source[target_column])
                features = [float(source[name]) for name in feature_columns]
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Non-numeric target or feature at CSV line {line_number}") from exc
            if not all(math.isfinite(value) for value in [target, *features]):
                raise ValueError(f"Non-finite target or feature at CSV line {line_number}")
            row = {"sample_id": sample_id, "target": target, "features": features}
            rows.append(row)
            indexed[sample_id] = row
    if not rows:
        raise ValueError("dataset contains no rows")
    return rows, indexed


def _selected_rows(indexed: dict[str, dict[str, Any]], values: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(values, list) or not values or len(set(map(str, values))) != len(values):
        raise ValueError(f"{label} must be a non-empty list of unique sample IDs")
    missing = [str(value) for value in values if str(value) not in indexed]
    if missing:
        raise ValueError(f"Unknown {label}: {missing[:20]}")
    return [indexed[str(value)] for value in values]


def _write_sisso_data(path: Path, rows: list[dict[str, Any]], target_column: str, feature_columns: list[str]) -> None:
    lines = [" ".join(["sample_id", target_column, *feature_columns])]
    for row in rows:
        values = [row["sample_id"], format(row["target"], ".17g")]
        values.extend(format(value, ".17g") for value in row["features"])
        lines.append(" ".join(values))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _unit_groups(value: Any, feature_count: int) -> str:
    if not isinstance(value, list) or not value:
        raise ValueError("feature_unit_groups must be a non-empty list of [start, end] ranges")
    groups = []
    covered = []
    for item in value:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("every feature_unit_groups item must be [start, end]")
        start, end = map(int, item)
        if start < 1 or end < start or end > feature_count:
            raise ValueError("feature unit ranges use one-based indices within feature_columns")
        covered.extend(range(start, end + 1))
        groups.append(f"({start}:{end})")
    if sorted(covered) != list(range(1, feature_count + 1)) or len(set(covered)) != feature_count:
        raise ValueError("feature_unit_groups must partition every feature exactly once")
    return "".join(groups)


def _sisso_input(method: dict[str, Any], settings: dict[str, Any], sample_count: int, feature_count: int) -> str:
    dimension = int(method["descriptor_dimension"])
    complexity = int(method["feature_complexity"])
    subspace = int(method["sis_subspace_size"])
    model_count = int(settings["number_of_models"])
    storage = int(settings["feature_storage_mode"])
    if dimension < 1 or dimension > 10:
        raise ValueError("descriptor_dimension must be between 1 and 10")
    if complexity < 0 or complexity > 7:
        raise ValueError("feature_complexity must be between 0 and 7")
    if subspace < 1 or subspace > 100000000 or model_count < 1 or model_count > 1000000:
        raise ValueError("sis_subspace_size or number_of_models is outside the supported bound")
    if storage not in {1, 2}:
        raise ValueError("feature_storage_mode must be 1 (numeric) or 2 (S-expression)")
    operators = method["operators"]
    if not isinstance(operators, list) or not operators or any(str(item) not in _SISSO_OPERATORS for item in operators):
        raise ValueError(f"operators must be a non-empty list chosen from {sorted(_SISSO_OPERATORS)}")
    method_so = str(method["sparsification_method"]).upper()
    metric = str(method["selection_metric"]).upper()
    if method_so not in {"L0", "L1L0"}:
        raise ValueError("sparsification_method must be L0 or L1L0")
    if metric not in {"RMSE", "MAXAE"}:
        raise ValueError("selection_metric must be RMSE or MaxAE")
    lower = float(settings["feature_minimum_absolute_max"])
    upper = float(settings["feature_maximum_absolute_max"])
    if not 0 < lower < upper:
        raise ValueError("feature magnitude limits must satisfy 0 < minimum < maximum")
    units = _unit_groups(method["feature_unit_groups"], feature_count)
    fit_intercept = ".true." if bool(method["fit_intercept"]) else ".false."
    return "\n".join(
        [
            "ptype=1", "ntask=1", "scmt=.false.", f"desc_dim={dimension}",
            f"nsample={sample_count}", "restart=0", f"fstore={storage}",
            f"nsf={feature_count}", f"ops='{''.join(map(str, operators))}'",
            f"fcomplexity={complexity}", f"funit={units}", f"fmax_min={lower:.17g}",
            f"fmax_max={upper:.17g}", f"nf_sis={subspace}", f"method_so='{method_so}'",
            f"fit_intercept={fit_intercept}", f"metric='{metric}'", f"nmodel={model_count}", "",
        ]
    )


def _sisso_model(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = list(re.finditer(r"(?m)^\s*(\d+)D descriptor/model\(y=sum\(ci\*di\)\+c0\)\s*:", text))
    if not blocks:
        raise RuntimeError("Could not find a SISSO regression descriptor/model block")
    start = blocks[-1].start()
    block = text[start:]
    descriptors = [
        {"index": int(index), "expression": expression.strip(), "feature_id": int(feature_id)}
        for index, expression, feature_id in re.findall(
            r"(?m)^\s*d(\d+)\s*=\s*(.*?)\s+feature_ID:(\d+)\s*$", block
        )
    ]
    coefficient_match = re.search(r"coeff\.\(ci\):\s*([^\n]+)", block)
    intercept_match = re.search(r"\bc0:\s*([-+0-9.Ee]+)", block)
    metric_match = re.search(r"RMSE and MaxAE:\s*([-+0-9.Ee]+)\s+([-+0-9.Ee]+)", block)
    if not descriptors or coefficient_match is None or intercept_match is None or metric_match is None:
        raise RuntimeError("SISSO model block is incomplete")
    coefficients = [float(value) for value in coefficient_match.group(1).split()]
    if len(coefficients) != len(descriptors):
        raise RuntimeError("SISSO descriptor and coefficient counts differ")
    return {
        "descriptor_dimension": int(blocks[-1].group(1)),
        "descriptors": descriptors,
        "coefficients": coefficients,
        "intercept": float(intercept_match.group(1)),
        "training_rmse": float(metric_match.group(1)),
        "training_maximum_absolute_error": float(metric_match.group(2)),
        "energy_or_property_unit": "as_supplied",
    }


def _sisso_predictions(path: Path, maximum_records: int, sample_ids: list[str] | None = None) -> dict[str, Any]:
    if maximum_records < 1 or maximum_records > 1000000:
        raise ValueError("maximum_prediction_records must be between 1 and 1000000")
    records = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        fields = line.split()
        if len(fields) != 3:
            continue
        try:
            observed, predicted, residual = map(float, fields)
        except ValueError:
            continue
        index = len(records)
        records.append(
            {
                "sample_id": sample_ids[index] if sample_ids is not None and index < len(sample_ids) else None,
                "observed": observed,
                "predicted": predicted,
                "residual_observed_minus_predicted": residual,
            }
        )
    if not records:
        raise RuntimeError("Could not parse predictions from SISSO_predict output")
    residuals = [item["residual_observed_minus_predicted"] for item in records]
    return {
        "sample_count": len(records),
        "rmse": math.sqrt(sum(value * value for value in residuals) / len(residuals)),
        "maximum_absolute_error": max(map(abs, residuals)),
        "returned_prediction_count": min(len(records), maximum_records),
        "predictions": records[:maximum_records],
        "truncated": len(records) > maximum_records,
    }


def _run_sisso(directory: Path, request: dict[str, Any], processes: int) -> dict[str, Any]:
    cpu_cores = int((request.get("resource_limits") or {}).get("cpu_cores", 1))
    if processes < 1 or processes > cpu_cores:
        raise ValueError("mpi_processes must be positive and no larger than resource_limits.cpu_cores")
    timeout = int((request.get("resource_limits") or {}).get("walltime_seconds", 86400))
    if processes == 1:
        completed = run_external(
            executable="SISSO", arguments=[], directory=directory,
            environment_variable="CHEMGRAPH_SISSO_COMMAND", timeout_seconds=max(1, timeout),
        )
    else:
        command = os.environ.get("CHEMGRAPH_SISSO_COMMAND", "SISSO")
        completed = run_external(
            executable="mpirun", arguments=["-np", str(processes), command], directory=directory,
            environment_variable="CHEMGRAPH_SISSO_MPIRUN_COMMAND", timeout_seconds=max(1, timeout),
        )
    (directory / "log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return completed
    if completed["returncode"] != 0:
        detail = completed["stderr"].strip() or completed["stdout"].strip()
        raise RuntimeError(f"SISSO failed with exit code {completed['returncode']}: {detail[-3000:]}")
    if "SISSO done successfully!" not in completed["stdout"] or not (directory / "SISSO.out").is_file():
        raise RuntimeError("SISSO exited without its normal completion marker and model output")
    return completed


def _run_sisso_predict(
    directory: Path,
    rows: list[dict[str, Any]],
    target_column: str,
    feature_columns: list[str],
    dimension: int,
    maximum_records: int,
    request: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    _write_sisso_data(directory / "predict.dat", rows, target_column, feature_columns)
    (directory / "SISSO_predict_para").write_text(
        f"{len(rows)}\n{len(feature_columns)}\n{dimension}\n1\n", encoding="utf-8"
    )
    timeout = int((request.get("resource_limits") or {}).get("walltime_seconds", 86400))
    completed = run_external(
        executable="SISSO_predict", arguments=[], directory=directory,
        environment_variable="CHEMGRAPH_SISSO_PREDICT_COMMAND", timeout_seconds=max(1, timeout),
    )
    (directory / "predict.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "predict.stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return completed, {}
    if completed["returncode"] != 0:
        detail = completed["stderr"].strip() or completed["stdout"].strip()
        raise RuntimeError(f"SISSO_predict failed with exit code {completed['returncode']}: {detail[-3000:]}")
    output = directory / "predict_Y.out"
    if not output.is_file():
        raise RuntimeError("SISSO_predict completed without predict_Y.out")
    return completed, _sisso_predictions(output, maximum_records, [row["sample_id"] for row in rows])


def _discover_sisso(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    feature_columns = [str(value) for value in method["feature_columns"]]
    _rows, indexed = _sisso_table(
        resolve_input_file(inputs["dataset"]), str(method["sample_id_column"]),
        str(method["target_column"]), feature_columns,
    )
    training = _selected_rows(indexed, method["training_sample_ids"], "training_sample_ids")
    validation = _selected_rows(indexed, method["validation_sample_ids"], "validation_sample_ids")
    overlap = sorted({row["sample_id"] for row in training} & {row["sample_id"] for row in validation})
    if overlap:
        raise ValueError(f"training and validation sample IDs overlap: {overlap[:20]}")
    if len(training) < 3:
        raise ValueError("SISSO regression requires at least three training samples")
    directory = output_directory("discover_sparse_symbolic_descriptor", "sisso")
    _write_sisso_data(directory / "train.dat", training, str(method["target_column"]), feature_columns)
    (directory / "SISSO.in").write_text(
        _sisso_input(method, settings, len(training), len(feature_columns)), encoding="utf-8"
    )
    completed = _run_sisso(directory, request, int(settings["mpi_processes"]))
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Restore the cached SISSO 3.5 Intel MPI runtime.")
    model_path = directory / "SISSO.out"
    model = _sisso_model(model_path)
    predicted, evaluation = _run_sisso_predict(
        directory, validation, str(method["target_column"]), feature_columns,
        model["descriptor_dimension"], int(settings["maximum_prediction_records"]), request,
    )
    if not predicted["available"]:
        return unavailable(predicted["stderr"], install="Restore SISSO_predict and its bc dependency.")
    result = {
        **model,
        "training_sample_count": len(training),
        "validation_sample_count": len(validation),
        "validation": evaluation,
        "model_output": relative_workspace_path(model_path),
        "prediction_output": relative_workspace_path(directory / "predict_Y.out"),
        "feature_columns": feature_columns,
        "target_column": str(method["target_column"]),
    }
    return success(
        result, artifact_files=command_artifacts(directory), backend_version="3.5",
        provenance={"fit_command": completed["command"], "prediction_command": predicted["command"]},
    )


def _evaluate_sisso(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    feature_columns = [str(value) for value in method["feature_columns"]]
    rows, _indexed = _sisso_table(
        resolve_input_file(inputs["dataset"]), str(method["sample_id_column"]),
        str(method["target_column"]), feature_columns,
    )
    directory = output_directory("evaluate_sparse_symbolic_descriptor", "sisso")
    shutil.copy2(resolve_input_file(inputs["model_output"]), directory / "SISSO.out")
    model = _sisso_model(directory / "SISSO.out")
    dimension = int(method["descriptor_dimension"])
    if dimension != model["descriptor_dimension"]:
        raise ValueError("descriptor_dimension does not match the highest model in SISSO.out")
    completed, evaluation = _run_sisso_predict(
        directory, rows, str(method["target_column"]), feature_columns, dimension,
        int(settings["maximum_prediction_records"]), request,
    )
    if not completed["available"]:
        return unavailable(completed["stderr"], install="Restore SISSO_predict and its bc dependency.")
    return success(
        {
            "model": model,
            "evaluation": evaluation,
            "prediction_output": relative_workspace_path(directory / "predict_Y.out"),
            "descriptor_output": relative_workspace_path(directory / "predict_X.out"),
        },
        artifact_files=command_artifacts(directory), backend_version="3.5",
        provenance={"command": completed["command"]},
    )


def _summarize_sisso(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    model_path = resolve_input_file(inputs["model_output"])
    result = {"model": _sisso_model(model_path), "model_output": relative_workspace_path(model_path)}
    artifacts = [{"path": relative_workspace_path(model_path), "semantic_type": "SISSOModel", "media_type": "text/plain"}]
    if inputs.get("prediction_output") is not None:
        prediction = resolve_input_file(inputs["prediction_output"])
        result["evaluation"] = _sisso_predictions(prediction, int(settings["maximum_prediction_records"]))
        result["prediction_output"] = relative_workspace_path(prediction)
        artifacts.append({"path": relative_workspace_path(prediction), "semantic_type": "SISSOPredictions", "media_type": "text/plain"})
    return success(result, artifact_files=artifacts, backend_version="3.5")


_GPLEARN_FUNCTIONS = {
    "abs", "add", "cos", "div", "inv", "log", "max", "min", "mul",
    "neg", "sin", "sqrt", "sub", "tan",
}
_GPLEARN_METRICS = {"mean absolute error", "mse", "pearson", "rmse", "spearman"}


def _regression_split(
    inputs: dict[str, Any], method: dict[str, Any]
) -> tuple[list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    feature_columns = [str(value) for value in method["feature_columns"]]
    _rows, indexed = _sisso_table(
        resolve_input_file(inputs["dataset"]), str(method["sample_id_column"]),
        str(method["target_column"]), feature_columns,
    )
    training = _selected_rows(indexed, method["training_sample_ids"], "training_sample_ids")
    validation = _selected_rows(indexed, method["validation_sample_ids"], "validation_sample_ids")
    overlap = sorted({row["sample_id"] for row in training} & {row["sample_id"] for row in validation})
    if overlap:
        raise ValueError(f"training and validation sample IDs overlap: {overlap[:20]}")
    if len(training) < 3:
        raise ValueError("symbolic regression requires at least three training samples")
    return feature_columns, training, validation


def _finite_float(value: Any, label: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def _gplearn_parameters(
    method: dict[str, Any], settings: dict[str, Any], request: dict[str, Any], random_seed: int
) -> dict[str, Any]:
    functions = [str(value) for value in method["function_set"]]
    if not functions or len(functions) > len(_GPLEARN_FUNCTIONS) or len(set(functions)) != len(functions):
        raise ValueError("function_set must be a non-empty list of unique built-in functions")
    unknown = sorted(set(functions) - _GPLEARN_FUNCTIONS)
    if unknown:
        raise ValueError(f"unsupported gplearn functions: {unknown}")
    metric = str(method["metric"]).lower()
    if metric not in _GPLEARN_METRICS:
        raise ValueError(f"metric must be chosen from {sorted(_GPLEARN_METRICS)}")
    population = int(settings["population_size"])
    generations = int(settings["generations"])
    tournament = int(settings["tournament_size"])
    if not 10 <= population <= 100000:
        raise ValueError("population_size must be between 10 and 100000")
    if not 1 <= generations <= 10000:
        raise ValueError("generations must be between 1 and 10000")
    if not 2 <= tournament <= population:
        raise ValueError("tournament_size must be between 2 and population_size")
    init_depth = tuple(int(value) for value in settings["init_depth"])
    if len(init_depth) != 2 or not 1 <= init_depth[0] <= init_depth[1] <= 20:
        raise ValueError("init_depth must be [minimum, maximum] within 1..20")
    init_method = str(settings["init_method"]).lower()
    if init_method not in {"full", "grow", "half and half"}:
        raise ValueError("init_method must be full, grow, or half and half")
    raw_const = settings["const_range"]
    if raw_const is None:
        const_range = None
    else:
        const_range = tuple(_finite_float(value, "const_range") for value in raw_const)
        if len(const_range) != 2 or const_range[0] >= const_range[1]:
            raise ValueError("const_range must be null or [lower, upper] with lower < upper")
    probabilities = {
        name: _finite_float(settings[name], name)
        for name in ("p_crossover", "p_subtree_mutation", "p_hoist_mutation", "p_point_mutation")
    }
    if any(value < 0 or value > 1 for value in probabilities.values()) or sum(probabilities.values()) > 1:
        raise ValueError("genetic-operation probabilities must be in [0,1] and sum to at most 1")
    point_replace = _finite_float(settings["p_point_replace"], "p_point_replace")
    max_samples = _finite_float(settings["max_samples"], "max_samples")
    parsimony = _finite_float(settings["parsimony_coefficient"], "parsimony_coefficient")
    if not 0 <= point_replace <= 1 or not 0 < max_samples <= 1 or parsimony < 0:
        raise ValueError("p_point_replace/max_samples must be probabilities and parsimony_coefficient non-negative")
    n_jobs = int(settings["n_jobs"])
    cpu_cores = int((request.get("resource_limits") or {}).get("cpu_cores", 1))
    if n_jobs < 1 or n_jobs > cpu_cores:
        raise ValueError("n_jobs must be positive and no larger than resource_limits.cpu_cores")
    maximum_records = int(settings["maximum_prediction_records"])
    if not 1 <= maximum_records <= 1000000:
        raise ValueError("maximum_prediction_records must be between 1 and 1000000")
    return {
        "population_size": population,
        "generations": generations,
        "tournament_size": tournament,
        "stopping_criteria": _finite_float(settings["stopping_criteria"], "stopping_criteria"),
        "const_range": const_range,
        "init_depth": init_depth,
        "init_method": init_method,
        "function_set": functions,
        "metric": metric,
        "parsimony_coefficient": parsimony,
        **probabilities,
        "p_point_replace": point_replace,
        "max_samples": max_samples,
        "feature_names": [str(value) for value in method["feature_columns"]],
        "warm_start": False,
        "low_memory": bool(settings["low_memory"]),
        "n_jobs": n_jobs,
        "verbose": 0,
        "random_state": int(random_seed),
    }


def _regression_metrics(observed: list[float], predicted: list[float]) -> dict[str, Any]:
    residuals = [left - right for left, right in zip(observed, predicted)]
    mean = sum(observed) / len(observed)
    total = sum((value - mean) ** 2 for value in observed)
    squared = sum(value * value for value in residuals)
    return {
        "sample_count": len(observed),
        "rmse": math.sqrt(squared / len(residuals)),
        "mean_absolute_error": sum(map(abs, residuals)) / len(residuals),
        "maximum_absolute_error": max(map(abs, residuals)),
        "r_squared": None if total == 0 else 1.0 - squared / total,
    }


def _fit_gplearn_once(
    feature_columns: list[str], training: list[dict[str, Any]], validation: list[dict[str, Any]],
    method: dict[str, Any], settings: dict[str, Any], request: dict[str, Any], seed: int,
) -> dict[str, Any]:
    import numpy as np
    from gplearn.genetic import SymbolicRegressor

    parameters = _gplearn_parameters(method, settings, request, seed)
    train_x = np.asarray([row["features"] for row in training], dtype=float)
    train_y = np.asarray([row["target"] for row in training], dtype=float)
    validation_x = np.asarray([row["features"] for row in validation], dtype=float)
    validation_y = np.asarray([row["target"] for row in validation], dtype=float)
    estimator = SymbolicRegressor(**parameters)
    estimator.fit(train_x, train_y)
    train_prediction = estimator.predict(train_x).tolist()
    validation_prediction = estimator.predict(validation_x).tolist()
    if not all(math.isfinite(value) for value in [*train_prediction, *validation_prediction]):
        raise RuntimeError("gplearn produced non-finite predictions")
    maximum_records = int(settings["maximum_prediction_records"])
    records = [
        {
            "sample_id": row["sample_id"],
            "observed": row["target"],
            "predicted": predicted,
            "residual_observed_minus_predicted": row["target"] - predicted,
        }
        for row, predicted in zip(validation, validation_prediction)
    ]
    program = estimator._program
    return {
        "random_seed": seed,
        "expression": str(program),
        "program_length": int(program.length_),
        "program_depth": int(program.depth_),
        "raw_fitness": float(program.raw_fitness_),
        "penalized_fitness": float(program.fitness_),
        "training": _regression_metrics(train_y.tolist(), train_prediction),
        "validation": {
            **_regression_metrics(validation_y.tolist(), validation_prediction),
            "returned_prediction_count": min(len(records), maximum_records),
            "predictions": records[:maximum_records],
            "truncated": len(records) > maximum_records,
        },
        "feature_columns": feature_columns,
        "target_column": str(method["target_column"]),
        "training_sample_ids": [row["sample_id"] for row in training],
        "validation_sample_ids": [row["sample_id"] for row in validation],
        "completed_generations": len(estimator.run_details_["generation"]),
    }


def _write_gplearn_result(directory: Path, name: str, result: dict[str, Any]) -> Path:
    path = directory / name
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _fit_gplearn(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    features, training, validation = _regression_split(inputs, method)
    result = _fit_gplearn_once(
        features, training, validation, method, settings, request, int(settings["random_seed"])
    )
    directory = output_directory("fit_symbolic_regression_baseline", "gplearn")
    result_path = _write_gplearn_result(directory, "symbolic_regression_result.json", result)
    return success(
        {**result, "results_file": relative_workspace_path(result_path)},
        artifact_files=command_artifacts(directory), backend_version="0.4.3",
    )


def _gplearn_seed_stability(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    seeds = [int(value) for value in settings["random_seeds"]]
    if not 2 <= len(seeds) <= 100 or len(set(seeds)) != len(seeds):
        raise ValueError("random_seeds must contain between 2 and 100 unique integers")
    features, training, validation = _regression_split(inputs, method)
    runs = [
        _fit_gplearn_once(features, training, validation, method, settings, request, seed)
        for seed in seeds
    ]
    rmse_values = [run["validation"]["rmse"] for run in runs]
    equations = [run["expression"] for run in runs]
    result = {
        "seed_count": len(seeds),
        "runs": runs,
        "unique_expression_count": len(set(equations)),
        "identical_expression_fraction": max(equations.count(value) for value in set(equations)) / len(equations),
        "validation_rmse_mean": sum(rmse_values) / len(rmse_values),
        "validation_rmse_sample_standard_deviation": (
            math.sqrt(sum((value - sum(rmse_values) / len(rmse_values)) ** 2 for value in rmse_values) / (len(rmse_values) - 1))
        ),
    }
    directory = output_directory("assess_symbolic_regression_seed_stability", "gplearn")
    result_path = _write_gplearn_result(directory, "symbolic_regression_stability.json", result)
    return success(
        {**result, "results_file": relative_workspace_path(result_path)},
        artifact_files=command_artifacts(directory), backend_version="0.4.3",
    )


def _bounded_gplearn_json(value: Any, maximum_records: int) -> Any:
    if isinstance(value, dict):
        result = {key: _bounded_gplearn_json(item, maximum_records) for key, item in value.items()}
        predictions = result.get("predictions")
        if isinstance(predictions, list):
            original = len(predictions)
            result["predictions"] = predictions[:maximum_records]
            result["returned_prediction_count"] = min(original, maximum_records)
            result["truncated"] = bool(result.get("truncated")) or original > maximum_records
        return result
    if isinstance(value, list):
        return [_bounded_gplearn_json(item, maximum_records) for item in value]
    return value


def _summarize_gplearn(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    maximum_records = int(settings["maximum_prediction_records"])
    if not 1 <= maximum_records <= 1000000:
        raise ValueError("maximum_prediction_records must be between 1 and 1000000")
    path = resolve_input_file(inputs["results_file"])
    try:
        source = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("results_file must be valid UTF-8 JSON") from exc
    if not isinstance(source, dict) or not ({"expression", "validation"} <= set(source) or {"runs", "seed_count"} <= set(source)):
        raise ValueError("results_file is not a recognized gplearn Action result")
    return success(
        {"summary": _bounded_gplearn_json(source, maximum_records), "results_file": relative_workspace_path(path)},
        artifact_files=[{"path": relative_workspace_path(path), "semantic_type": "SymbolicRegressionResult", "media_type": "application/json"}],
        backend_version="0.4.3",
    )


def _molecule(value: Any):
    from rdkit import Chem

    item = structure_dict(value)
    smiles = item.get("smiles")
    molecule = Chem.MolFromSmiles(str(smiles)) if smiles else None
    if molecule is None and item.get("source_path"):
        path = str(item["source_path"])
        if path.lower().endswith((".sdf", ".mol")):
            molecule = Chem.MolFromMolFile(path, removeHs=False)
        elif path.lower().endswith(".pdb"):
            molecule = Chem.MolFromPDBFile(path, removeHs=False)
    if molecule is None:
        raise ValueError("RDKit cheminformatics actions require valid SMILES, SDF/MOL, or PDB input")
    return molecule


def _fingerprint(molecule, method: dict[str, Any], settings: dict[str, Any]):
    from rdkit import Chem
    from rdkit.Chem import AllChem, MACCSkeys

    fingerprint_type = str(method["fingerprint_type"]).lower().replace("-", "_")
    if fingerprint_type in {"morgan", "ecfp"}:
        radius = int(settings.get("radius", 2))
        n_bits = int(settings.get("n_bits", 2048))
        if radius < 0 or n_bits < 64 or n_bits > 65536:
            raise ValueError("Morgan fingerprint requires radius >= 0 and 64 <= n_bits <= 65536")
        return AllChem.GetMorganFingerprintAsBitVect(
            molecule,
            radius,
            nBits=n_bits,
            useChirality=bool(settings.get("use_chirality", True)),
        ), {"fingerprint_type": "morgan", "radius": radius, "n_bits": n_bits}
    if fingerprint_type in {"rdkit", "topological"}:
        n_bits = int(settings.get("n_bits", 2048))
        if n_bits < 64 or n_bits > 65536:
            raise ValueError("RDKit fingerprint requires 64 <= n_bits <= 65536")
        return Chem.RDKFingerprint(
            molecule,
            fpSize=n_bits,
            useHs=bool(settings.get("include_hydrogens", True)),
        ), {"fingerprint_type": "rdkit", "n_bits": n_bits}
    if fingerprint_type in {"maccs", "maccs_keys"}:
        value = MACCSkeys.GenMACCSKeys(molecule)
        return value, {"fingerprint_type": "maccs", "n_bits": int(value.GetNumBits())}
    raise ValueError("fingerprint_type must be morgan, rdkit, or maccs")


def _descriptors(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import Descriptors

    inputs, _method, settings = request_parts(request)
    molecule = _molecule(inputs["molecule"])
    available = {name: function for name, function in Descriptors._descList}
    default_names = [
        "MolWt",
        "ExactMolWt",
        "MolLogP",
        "TPSA",
        "NumHDonors",
        "NumHAcceptors",
        "NumRotatableBonds",
        "RingCount",
        "FractionCSP3",
        "HeavyAtomCount",
    ]
    names = list(settings.get("descriptor_names") or default_names)
    if not names or len(names) > 256:
        raise ValueError("descriptor_names must contain between 1 and 256 descriptor names")
    unknown = sorted(set(names) - set(available))
    if unknown:
        raise ValueError(f"Unknown RDKit descriptors: {unknown}")
    values = {name: float(available[name](molecule)) for name in names}
    return success(
        {"descriptors": values, "descriptor_count": len(values)},
        backend_version=module_version("rdkit"),
    )


def _fingerprint_action(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    fingerprint, metadata = _fingerprint(_molecule(inputs["molecule"]), method, settings)
    on_bits = [int(value) for value in fingerprint.GetOnBits()]
    return success(
        {
            **metadata,
            "on_bits": on_bits,
            "bit_count": len(on_bits),
        },
        backend_version=module_version("rdkit"),
    )


def _similarity(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit import DataStructs

    inputs, method, settings = request_parts(request)
    left, metadata_left = _fingerprint(_molecule(inputs["molecule_a"]), method, settings)
    right, metadata_right = _fingerprint(_molecule(inputs["molecule_b"]), method, settings)
    if metadata_left != metadata_right:
        raise RuntimeError("Fingerprint metadata mismatch")
    metric = str(method["similarity_metric"]).lower()
    functions = {
        "tanimoto": DataStructs.TanimotoSimilarity,
        "dice": DataStructs.DiceSimilarity,
        "cosine": DataStructs.CosineSimilarity,
    }
    if metric not in functions:
        raise ValueError("similarity_metric must be tanimoto, dice, or cosine")
    value = float(functions[metric](left, right))
    return success(
        {"similarity": value, "metric": metric, **metadata_left},
        backend_version=module_version("rdkit"),
    )


def _substructures(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit import Chem

    inputs, method, settings = request_parts(request)
    molecule = _molecule(inputs["molecule"])
    query_text = str(inputs["query"])
    query_format = str(method["query_format"]).lower()
    if query_format == "smarts":
        query = Chem.MolFromSmarts(query_text)
    elif query_format == "smiles":
        query = Chem.MolFromSmiles(query_text)
    else:
        raise ValueError("query_format must be smarts or smiles")
    if query is None:
        raise ValueError(f"Could not parse {query_format} query")
    max_matches = int(settings.get("max_matches", 1000))
    if max_matches < 1 or max_matches > 100000:
        raise ValueError("max_matches must be between 1 and 100000")
    matches = molecule.GetSubstructMatches(
        query,
        uniquify=bool(settings.get("unique", True)),
        useChirality=bool(settings.get("use_chirality", True)),
        maxMatches=max_matches,
    )
    return success(
        {
            "query": query_text,
            "query_format": query_format,
            "matches": [list(map(int, match)) for match in matches],
            "match_count": len(matches),
        },
        backend_version=module_version("rdkit"),
    )


def _tautomers(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit import Chem
    from rdkit.Chem.MolStandardize import rdMolStandardize

    inputs, _method, settings = request_parts(request)
    maximum = int(settings["max_tautomers"])
    if maximum < 1 or maximum > 10000:
        raise ValueError("max_tautomers must be between 1 and 10000")
    enumerator = rdMolStandardize.TautomerEnumerator()
    enumerator.SetMaxTautomers(maximum)
    values = enumerator.Enumerate(_molecule(inputs["molecule"]))
    smiles = sorted({Chem.MolToSmiles(value, canonical=True, isomericSmiles=True) for value in values})
    return success(
        {"molecules": [{"smiles": value} for value in smiles], "count": len(smiles), "max_tautomers": maximum},
        backend_version=module_version("rdkit"),
    )


def _stereoisomers(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit import Chem
    from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

    inputs, _method, settings = request_parts(request)
    maximum = int(settings["max_isomers"])
    if maximum < 1 or maximum > 10000:
        raise ValueError("max_isomers must be between 1 and 10000")
    options = StereoEnumerationOptions(
        onlyUnassigned=bool(settings["only_unassigned"]),
        unique=bool(settings["unique"]),
        maxIsomers=maximum,
        tryEmbedding=bool(settings.get("try_embedding", False)),
    )
    values = EnumerateStereoisomers(_molecule(inputs["molecule"]), options=options)
    smiles = sorted({Chem.MolToSmiles(value, canonical=True, isomericSmiles=True) for value in values})
    return success(
        {"molecules": [{"smiles": value} for value in smiles], "count": len(smiles), "settings": settings},
        backend_version=module_version("rdkit"),
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "sisso":
        if action_id == "discover_sparse_symbolic_descriptor":
            return _discover_sisso(request)
        if action_id == "evaluate_sparse_symbolic_descriptor":
            return _evaluate_sisso(request)
        if action_id == "summarize_sparse_symbolic_descriptor_results":
            return _summarize_sisso(request)
        return unsupported(f"Unsupported SISSO action: {action_id}")
    if backend_id == "gplearn":
        if action_id == "fit_symbolic_regression_baseline":
            return _fit_gplearn(request)
        if action_id == "assess_symbolic_regression_seed_stability":
            return _gplearn_seed_stability(request)
        if action_id == "summarize_symbolic_regression_results":
            return _summarize_gplearn(request)
        return unsupported(f"Unsupported gplearn action: {action_id}")
    if backend_id != "rdkit":
        return unsupported(f"Unsupported cheminformatics backend: {backend_id}")
    if action_id == "calculate_molecular_descriptors":
        return _descriptors(request)
    if action_id == "calculate_molecular_fingerprint":
        return _fingerprint_action(request)
    if action_id == "calculate_molecular_similarity":
        return _similarity(request)
    if action_id == "search_local_substructures":
        return _substructures(request)
    if action_id == "enumerate_tautomers":
        return _tautomers(request)
    if action_id == "enumerate_stereoisomers":
        return _stereoisomers(request)
    return unsupported(f"Unsupported cheminformatics action: {action_id}")

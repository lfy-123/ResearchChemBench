#!/usr/bin/env python3
"""Run fresh, machine-checkable validation for the complete public Action catalog.

The live catalog is the authority: every Action/Backend pair receives a record.
Existing smoke runners are used only as request factories or fresh execution
drivers.  Historical status/evidence files are never imported as proof.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import importlib
import json
import math
import os
import shutil
import sys
import tempfile
import threading
import time
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for _path in (SOURCE_ROOT, ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from dotenv import load_dotenv

from chemistry_toolbox.src.catalog import action_specs, backend_specs, validate_catalog
from chemistry_toolbox.src.service import execute_action as service_execute_action


SCHEMA_VERSION = 2
VALIDATOR_VERSION = "2.0.0"
PASS_STATUS = "passed"
TERMINAL_PASS_STATUSES = {"success"}
FACTORY_SOURCES = (
    "action_backend_matrix",
    "scientific_resources",
    "goodvibes",
    "data_sources",
)
MONOLITHIC_SOURCES = (
    "action_gap",
    "backend_gap",
)
PYTEST_DYNAMIC_SOURCE = "pytest_dynamic"
EXPLICIT_RECIPE_SOURCE = "explicit_catalog_gap_recipes"
EXPLICIT_RECIPE_PAIRS = (
    ("analyze_reaction_coordinate", "internal_reaction_analysis"),
    ("assign_force_field_parameters", "openff"),
    ("assign_partial_charges", "openff_am1bcc"),
    ("calculate_bse_optical_spectrum", "yambo"),
    ("calculate_correlated_electron_density", "orca"),
    ("calculate_electron_isodensity_surface", "multiwfn"),
    ("calculate_quasiparticle_corrections", "yambo"),
    ("enumerate_coordination_isomers", "internal_reaction_analysis"),
    ("explore_reaction_network", "kinbot"),
    ("export_electron_density_grid", "orca"),
    ("integrate_reaction_network", "scipy"),
    ("propagate_nonadiabatic_trajectory", "sharc"),
    ("scan_reaction_coordinates", "pysisyphus"),
    ("search_reaction_path", "pysisyphus"),
    ("solvate_molecular_system", "packmol"),
    ("validate_reaction_path", "internal_reaction_analysis"),
)
SCALAR_ENERGY_ACTIONS = {
    "calculate_adsorption_energy",
    "calculate_energy",
    "calculate_force_field_energy",
    "calculate_periodic_energy",
    "decompose_force_field_energy",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return _sha256_bytes(encoded.encode("utf-8"))


def _catalog() -> tuple[dict[str, Any], dict[str, Any], list[tuple[str, str]]]:
    validate_catalog()
    actions = action_specs()
    backends = backend_specs()
    pairs = sorted(
        (action.id, backend_id)
        for action in actions.values()
        for backend_id in action.backend_ids
    )
    return actions, backends, pairs


def _catalog_hash(actions: dict[str, Any], backends: dict[str, Any]) -> str:
    payload = {
        "actions": [actions[key].as_dict() for key in sorted(actions)],
        "backends": [backends[key].as_dict() for key in sorted(backends)],
    }
    return _json_hash(payload)


def _case_id(action_id: str, backend_id: str) -> str:
    return f"{action_id}__{backend_id}"


def _pair_from_case_id(value: str) -> tuple[str, str]:
    if "__" not in value:
        raise ValueError("case id must have the form <action>__<backend>")
    action_id, backend_id = value.rsplit("__", 1)
    if not action_id or not backend_id:
        raise ValueError("case id must have the form <action>__<backend>")
    return action_id, backend_id


def _shape(value: Any) -> list[int] | None:
    if not isinstance(value, (list, tuple)):
        return None
    result: list[int] = []
    cursor: Any = value
    while isinstance(cursor, (list, tuple)):
        result.append(len(cursor))
        if not cursor:
            break
        first_shape = _shape(cursor[0])
        if any(_shape(item) != first_shape for item in cursor[1:]):
            result.append(-1)
            break
        cursor = cursor[0]
    return result


def _numbers(value: Any) -> Iterator[float]:
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, (int, float)):
        yield float(value)
        return
    if isinstance(value, dict):
        for item in value.values():
            yield from _numbers(item)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _numbers(item)


def _all_finite(value: Any) -> tuple[bool, int]:
    values = list(_numbers(value))
    return all(math.isfinite(item) for item in values), len(values)


def _path_descriptor(value: str | Path, workspace: Path | None) -> dict[str, Any] | None:
    raw = str(value)
    candidate = Path(raw)
    if not candidate.is_absolute() and workspace is not None:
        candidate = workspace / candidate
    try:
        exists = candidate.exists()
    except OSError:
        return None
    if not exists:
        return None
    descriptor: dict[str, Any] = {
        "path": raw,
        "resolved_path": str(candidate.resolve()),
        "exists": True,
        "kind": "directory" if candidate.is_dir() else "file",
    }
    if candidate.is_file():
        descriptor["size_bytes"] = candidate.stat().st_size
        descriptor["sha256"] = _sha256_file(candidate)
    return descriptor


def _summarize(value: Any, workspace: Path | None, *, depth: int = 0) -> Any:
    """Preserve small values and summarize large scientific arrays without losing shape."""
    if depth > 12:
        return {"summary": "maximum nesting depth reached", "type": type(value).__name__}
    if isinstance(value, Path):
        return _path_descriptor(value, workspace) or str(value)
    if isinstance(value, str):
        descriptor = _path_descriptor(value, workspace)
        return descriptor if descriptor is not None else value
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, dict):
        return {
            str(key): _summarize(item, workspace, depth=depth + 1)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        shape = _shape(value)
        numeric = list(_numbers(value))
        if len(value) <= 32 and len(numeric) <= 256:
            return [_summarize(item, workspace, depth=depth + 1) for item in value]
        finite = [item for item in numeric if math.isfinite(item)]
        summary: dict[str, Any] = {
            "kind": "array_summary",
            "shape": shape,
            "item_count": len(value),
            "numeric_value_count": len(numeric),
            "all_finite": len(finite) == len(numeric),
            "sample": [
                _summarize(item, workspace, depth=depth + 1) for item in value[:3]
            ],
        }
        if finite:
            summary.update({"minimum": min(finite), "maximum": max(finite)})
        return summary
    if hasattr(value, "model_dump"):
        return _summarize(value.model_dump(mode="python"), workspace, depth=depth + 1)
    return repr(value)


def _normalize_request(request: Any) -> tuple[dict[str, Any], list[str]]:
    if hasattr(request, "model_dump"):
        normalized = request.model_dump(mode="python")
    elif isinstance(request, dict):
        normalized = copy.deepcopy(request)
    else:
        raise TypeError(f"Unsupported ActionRequest value: {type(request).__name__}")
    adaptations: list[str] = []
    limits = normalized.get("resource_limits")
    if isinstance(limits, dict) and "walltime_seconds" in limits:
        limits.pop("walltime_seconds", None)
        adaptations.append(
            "removed deprecated evaluator-owned resource_limits.walltime_seconds"
        )
    return normalized, adaptations


def _request_summary(
    action_id: str,
    backend_id: str,
    request: dict[str, Any],
    workspace: Path | None,
    actions: dict[str, Any],
    backends: dict[str, Any],
) -> dict[str, Any]:
    action = actions[action_id]
    backend = backends[backend_id]
    contract = {
        "action_required_inputs": list(action.required_inputs),
        "action_optional_inputs": list(action.optional_inputs),
        "backend_required_inputs": list(backend.required_input_fields.get(action_id, ())),
        "backend_required_methods": list(backend.required_method_fields.get(action_id, ())),
        "backend_required_settings": list(backend.required_setting_fields.get(action_id, ())),
        "required_component_roles": list(backend.required_component_roles.get(action_id, ())),
    }
    summarized = _summarize(request, workspace)
    return {
        "request_sha256": _json_hash(summarized),
        "contract": contract,
        "request": summarized,
    }


def _scientific_result_summary(response: dict[str, Any], workspace: Path | None) -> dict[str, Any]:
    result = response.get("result")
    finite, numeric_count = _all_finite(result)
    artifacts = []
    for artifact in response.get("output_artifacts") or []:
        value = artifact.model_dump(mode="python") if hasattr(artifact, "model_dump") else artifact
        artifacts.append(_summarize(value, workspace))
    return {
        "status": response.get("status"),
        "action": response.get("action"),
        "requested_backend": response.get("requested_backend"),
        "backend": response.get("backend"),
        "backend_version": response.get("backend_version"),
        "selection_source": response.get("selection_source"),
        "primary_result": _summarize(result, workspace),
        "numeric_value_count": numeric_count,
        "all_numeric_values_finite": finite,
        "output_artifacts": artifacts,
        "warnings": list(response.get("warnings") or []),
        "error": _summarize(response.get("error"), workspace),
        "provenance": _summarize(response.get("provenance") or {}, workspace),
    }


def _criterion(
    criterion_id: str,
    passed: bool | None,
    detail: str,
    *,
    required: bool = True,
) -> dict[str, Any]:
    return {
        "id": criterion_id,
        "required": required,
        "status": "not_applicable" if passed is None else ("passed" if passed else "failed"),
        "passed": passed,
        "detail": detail,
    }


def _find_key_values(value: Any, names: Iterable[str]) -> list[Any]:
    wanted = {name.casefold() for name in names}
    found: list[Any] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).casefold() in wanted:
                found.append(item)
            found.extend(_find_key_values(item, wanted))
    elif isinstance(value, (list, tuple)):
        for item in value:
            found.extend(_find_key_values(item, wanted))
    return found


def _first_sequence(value: Any, names: Iterable[str]) -> list[Any] | None:
    for item in _find_key_values(value, names):
        if isinstance(item, (list, tuple)):
            return list(item)
    return None


def _first_number(value: Any, names: Iterable[str]) -> float | None:
    for item in _find_key_values(value, names):
        if isinstance(item, bool):
            continue
        if isinstance(item, (int, float)):
            return float(item)
    return None


def _first_numeric_value(value: Any, names: Iterable[str]) -> float | None:
    for item in _find_key_values(value, names):
        for number in _numbers(item):
            if math.isfinite(number):
                return number
    return None


def _key_names(value: Any) -> Iterator[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _key_names(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _key_names(item)


def _structure_atom_count(value: Any) -> int | None:
    structures = _find_key_values(value, ("structure", "optimized_structure", "final_structure"))
    structures.append(value)
    for structure in structures:
        if not isinstance(structure, dict):
            continue
        atoms = structure.get("atoms")
        if isinstance(atoms, list):
            return len(atoms)
        symbols = structure.get("symbols") or structure.get("elements")
        if isinstance(symbols, list):
            return len(symbols)
        particles = structure.get("particles")
        if isinstance(particles, dict) and isinstance(particles.get("positions"), list):
            return len(particles["positions"])
    return None


def _max_matrix_asymmetry(matrix: Any) -> float | None:
    if not isinstance(matrix, (list, tuple)) or not matrix:
        return None
    size = len(matrix)
    if any(not isinstance(row, (list, tuple)) or len(row) != size for row in matrix):
        return None
    try:
        return max(
            abs(float(matrix[row][column]) - float(matrix[column][row]))
            for row in range(size)
            for column in range(size)
        )
    except (TypeError, ValueError):
        return None


def _artifact_criterion(response: dict[str, Any], workspace: Path | None) -> dict[str, Any]:
    artifacts = response.get("output_artifacts") or []
    if not artifacts:
        return _criterion(
            "output_artifact_integrity",
            None,
            "Action returned no output artifacts; result validation is in-memory.",
            required=False,
        )
    failures: list[str] = []
    for index, artifact in enumerate(artifacts):
        value = artifact.model_dump(mode="python") if hasattr(artifact, "model_dump") else artifact
        path_value = value.get("path") if isinstance(value, dict) else None
        if not path_value:
            failures.append(f"artifact[{index}] has no path")
            continue
        descriptor = _path_descriptor(str(path_value), workspace)
        if descriptor is None:
            failures.append(f"artifact[{index}] path does not exist: {path_value}")
        expected_sha = value.get("sha256") if isinstance(value, dict) else None
        if descriptor and expected_sha and descriptor.get("sha256") != expected_sha:
            failures.append(f"artifact[{index}] sha256 mismatch: {path_value}")
    return _criterion(
        "output_artifact_integrity",
        not failures,
        "; ".join(failures) if failures else f"Verified {len(artifacts)} output artifact(s).",
    )


def _scientific_criteria(
    action_id: str,
    expected_backend: str,
    request: dict[str, Any],
    response: dict[str, Any],
    workspace: Path | None,
) -> list[dict[str, Any]]:
    result = response.get("result")
    status = response.get("status")
    actual_backend = response.get("backend")
    finite, numeric_count = _all_finite(result)
    provenance = response.get("provenance") or {}
    fallback_count = provenance.get("automatic_fallback_count")
    criteria = [
        _criterion(
            "fresh_current_run_execution",
            True,
            "Captured directly around execute_action in this validation run.",
        ),
        _criterion(
            "canonical_action_envelope",
            response.get("action") == action_id,
            f"response.action={response.get('action')!r}; expected={action_id!r}",
        ),
        _criterion(
            "exact_backend_identity",
            actual_backend == expected_backend,
            f"response.backend={actual_backend!r}; expected={expected_backend!r}",
        ),
        _criterion(
            "successful_terminal_status",
            status in TERMINAL_PASS_STATUSES,
            f"status={status!r}; partial_success is not accepted as full scientific validation",
        ),
        _criterion(
            "nonempty_primary_result",
            result not in (None, {}, []),
            f"result_type={type(result).__name__}",
        ),
        _criterion(
            "finite_numeric_output",
            finite,
            f"checked {numeric_count} numeric value(s)",
        ),
        _artifact_criterion(response, workspace),
        _criterion(
            "no_automatic_backend_fallback",
            fallback_count in (None, 0),
            "automatic_fallback_count is absent or zero"
            if fallback_count in (None, 0)
            else f"automatic_fallback_count={fallback_count!r}",
        ),
    ]

    input_count = _structure_atom_count(request.get("inputs") or {})
    if action_id == "calculate_forces" or action_id.endswith("_forces"):
        forces = _first_sequence(result, ("forces", "force"))
        shape = _shape(forces) if forces is not None else None
        matrix_valid = bool(shape and len(shape) == 2 and shape[1] == 3 and shape[0] > 0)
        flat_valid = bool(shape and len(shape) == 1 and shape[0] > 0 and shape[0] % 3 == 0)
        valid = matrix_valid or flat_valid
        force_atom_count = (
            shape[0]
            if matrix_valid and shape is not None
            else shape[0] // 3
            if flat_valid and shape is not None
            else None
        )
        if input_count is not None:
            valid = valid and force_atom_count == input_count
        criteria.append(
            _criterion(
                "force_array_shape",
                valid,
                f"shape={shape}; force_atom_count={force_atom_count}; input_atom_count={input_count}",
            )
        )
    elif "hessian" in action_id:
        matrix = _first_sequence(result, ("hessian", "matrix"))
        shape = _shape(matrix) if matrix is not None else None
        valid = bool(shape and len(shape) == 2 and shape[0] == shape[1] and shape[0] > 0)
        if input_count is not None:
            valid = valid and shape is not None and shape[0] == 3 * input_count
        criteria.append(
            _criterion("hessian_square_shape", valid, f"shape={shape}; input_atom_count={input_count}")
        )
        asymmetry = _max_matrix_asymmetry(matrix)
        criteria.append(
            _criterion(
                "hessian_symmetry",
                asymmetry is not None and asymmetry <= 1.0e-6,
                f"maximum_absolute_asymmetry={asymmetry!r}; tolerance=1e-6",
            )
        )
    elif "dipole" in action_id:
        dipole = _first_sequence(result, ("dipole", "dipole_moment", "vector"))
        criteria.append(
            _criterion(
                "dipole_vector_shape",
                dipole is not None and len(dipole) == 3,
                f"shape={_shape(dipole) if dipole is not None else None}",
            )
        )
    elif action_id in {
        "assign_partial_charges",
        "calculate_atomic_charges",
        "calculate_bader_charges",
    }:
        charges = _first_sequence(
            result,
            ("charges", "partial_charges", "partial_charges_e", "atomic_charges"),
        )
        valid = charges is not None and len(charges) > 0
        if input_count is not None:
            valid = valid and len(charges or []) == input_count
        criteria.append(
            _criterion("atomic_charge_count", valid, f"count={len(charges or [])}; input_atom_count={input_count}")
        )
        target_charge = _first_number(request.get("inputs") or {}, ("charge", "net_charge"))
        numeric_charges = list(_numbers(charges)) if charges is not None else []
        if target_charge is not None and numeric_charges:
            charge_error = abs(sum(numeric_charges) - target_charge)
            criteria.append(
                _criterion(
                    "net_charge_conservation",
                    charge_error <= 0.2,
                    f"sum_atomic_charges={sum(numeric_charges):.8g}; "
                    f"target_charge={target_charge:.8g}; absolute_error={charge_error:.8g}",
                )
            )

    if any(token in action_id for token in ("optimize", "relax", "minimize")):
        output_count = _structure_atom_count(result)
        structure_valid = output_count is not None and output_count > 0 and (
            input_count is None or output_count == input_count
        )
        system_references = _find_key_values(
            result,
            (
                "coordinate_path",
                "topology_path",
                "amber_coordinate_path",
                "charmm_coordinate_path",
                "lammps_data_path",
                "namd_binary_coordinates_path",
            ),
        )
        criteria.append(
            _criterion(
                "optimized_structure_integrity",
                structure_valid
                or bool(system_references)
                or bool(response.get("output_artifacts")),
                f"input_atom_count={input_count}; output_atom_count={output_count}; "
                f"system_reference_count={len(system_references)}",
            )
        )
        convergence_values = _find_key_values(
            result,
            ("converged", "minimized", "optimization_converged", "geometry_converged"),
        )
        convergence = next(
            (item for item in convergence_values if isinstance(item, bool)), None
        )
        criteria.append(
            _criterion(
                "optimization_convergence",
                convergence is True,
                f"explicit_convergence_signal={convergence!r}",
            )
        )

    if action_id in {
        "search_compounds",
        "resolve_chemical_identity",
        "retrieve_compound_properties",
        "retrieve_compound_structure",
        "search_similar_compounds",
        "search_substructures",
        "search_protein_structures",
        "search_materials",
        "search_catalysis_records",
        "lookup_nist_webbook_species",
    }:
        count = _first_number(
            result, ("count", "record_count", "total_count", "match_count")
        )
        records = _first_sequence(
            result, ("records", "results", "items", "candidates")
        )
        identities = _find_key_values(result, ("identity",))
        valid = (count is not None and count > 0) or bool(records) or any(
            isinstance(item, dict) and bool(item) for item in identities
        )
        criteria.append(
            _criterion(
                "nonempty_data_records",
                valid,
                f"reported_count={count}; materialized_record_count={len(records or [])}",
            )
        )

    if action_id == "dock_ligand":
        scores = _first_sequence(result, ("scores", "affinities", "poses"))
        pose_path = _find_key_values(result, ("poses_path", "pose_path", "docked_poses"))
        criteria.append(
            _criterion(
                "docking_pose_and_score",
                bool(scores) and bool(pose_path or response.get("output_artifacts")),
                f"score_count={len(scores or [])}; pose_reference_count={len(pose_path)}",
            )
        )

    if action_id in SCALAR_ENERGY_ACTIONS:
        energy = _first_numeric_value(
            result,
            (
                "energy",
                "total_energy",
                "energy_ev",
                "energy_hartree",
                "free_energy",
                "adsorption_energy_ev",
                "potential_energy",
                "potential_energy_kj_mol",
                "total_potential_energy_kj_mol",
            ),
        )
        criteria.append(
            _criterion(
                "finite_energy_scalar",
                energy is not None and math.isfinite(energy),
                f"energy={energy!r}",
            )
        )
        units = _find_key_values(result, ("unit", "energy_unit", "units"))
        unit_keys = [
            key
            for key in _key_names(result)
            if key.casefold().endswith(
                ("_ev", "_hartree", "_kj_mol", "_kcal_mol", "_cm1")
            )
        ]
        criteria.append(
            _criterion(
                "energy_unit_declared",
                any(isinstance(item, str) and item.strip() for item in units)
                or bool(unit_keys),
                f"declared_units={units[:4]!r}; unit_encoded_keys={unit_keys[:4]!r}",
            )
        )

    if any(token in action_id for token in ("spectrum", "dispersion", "density_of_states")):
        sequences = [
            item
            for item in _find_key_values(
                result,
                (
                    "frequencies",
                    "frequencies_thz",
                    "frequency_thz",
                    "energies",
                    "energy_ev",
                    "energy_ev_relative_to_fermi",
                    "wavenumber_cm1",
                    "intensity",
                    "intensities",
                    "bands",
                    "dos",
                    "density_of_states",
                    "density_of_states_per_ev",
                    "total_density_of_states_per_ev",
                    "distances",
                    "qpoints",
                    "values",
                ),
            )
            if isinstance(item, (list, tuple))
        ]
        criteria.append(
            _criterion(
                "nonempty_spectral_series",
                any(len(item) > 0 for item in sequences)
                or bool(_first_sequence(result, ("spectrum", "states", "bands"))),
                f"candidate_series_shapes={[_shape(item) for item in sequences[:6]]}",
            )
        )

    explicit_checks: dict[str, tuple[bool, str]] = {}
    if action_id == "analyze_free_energy_convergence":
        convergence = _first_sequence(result, ("convergence",))
        fractions = [
            float(item["fraction"])
            for item in convergence or []
            if isinstance(item, dict) and isinstance(item.get("fraction"), (int, float))
        ]
        uncertainties = [
            float(item["delta_f_uncertainty"])
            for item in convergence or []
            if isinstance(item, dict)
            and isinstance(item.get("delta_f_uncertainty"), (int, float))
        ]
        explicit_checks["free_energy_convergence_series"] = (
            len(convergence or []) >= 2
            and len(fractions) == len(convergence or [])
            and len(uncertainties) == len(convergence or [])
            and fractions == sorted(fractions)
            and all(value >= 0 and math.isfinite(value) for value in uncertainties),
            f"point_count={len(convergence or [])}; fractions={fractions}; "
            f"uncertainties={uncertainties}",
        )
    elif action_id in {
        "calculate_end_state_binding_free_energy",
        "calculate_end_state_energy_decomposition",
        "summarize_end_state_free_energy_results",
    }:
        averages = list(
            _numbers(_find_key_values(result, ("average_kcal_per_mol",)))
        )
        units = _find_key_values(result, ("energy_unit", "unit"))
        explicit_checks["end_state_energy_statistics"] = (
            bool(averages)
            and all(math.isfinite(value) for value in averages)
            and any(isinstance(item, str) and item.strip() for item in units),
            f"average_count={len(averages)}; declared_units={units[:3]!r}",
        )
    elif action_id == "estimate_free_energy_difference":
        matrix = _first_sequence(result, ("delta_f",))
        shape = _shape(matrix) if matrix is not None else None
        explicit_checks["free_energy_difference_matrix"] = (
            bool(shape)
            and len(shape) == 2
            and shape[0] == shape[1]
            and shape[0] >= 2,
            f"delta_f_shape={shape}",
        )
    elif action_id == "parse_alchemical_energy_data":
        rows = _first_number(result, ("row_count",))
        columns = _first_number(result, ("column_count",))
        data_paths = _find_key_values(result, ("data_path",))
        explicit_checks["alchemical_energy_table_materialized"] = (
            rows is not None
            and rows > 0
            and columns is not None
            and columns >= 2
            and bool(data_paths or response.get("output_artifacts")),
            f"row_count={rows!r}; column_count={columns!r}; "
            f"data_reference_count={len(data_paths)}",
        )
    elif action_id == "assign_force_field_parameters":
        force_field = _find_key_values(result, ("force_field",))
        system_refs = _find_key_values(
            result,
            ("interchange_path", "system_xml_path", "topology_path"),
        )
        explicit_checks["parameterized_system_materialized"] = (
            bool(force_field) and bool(system_refs or response.get("output_artifacts")),
            f"force_field={force_field[:2]!r}; system_reference_count={len(system_refs)}",
        )
    elif action_id == "calculate_bse_optical_spectrum":
        spectrum = _first_sequence(result, ("spectrum",))
        point_count = _first_number(result, ("point_count",))
        explicit_checks["bse_spectrum_points"] = (
            bool(spectrum) and (point_count is None or point_count == len(spectrum)),
            f"point_count={point_count!r}; spectrum_records={len(spectrum or [])}",
        )
    elif action_id == "calculate_quasiparticle_corrections":
        states = _first_sequence(result, ("states",))
        state_count = _first_number(result, ("state_count",))
        explicit_checks["quasiparticle_state_records"] = (
            bool(states) and (state_count is None or state_count == len(states)),
            f"state_count={state_count!r}; state_records={len(states or [])}",
        )
    elif action_id == "calculate_correlated_electron_density":
        electron_count = _first_number(result, ("electron_count",))
        density_files = _find_key_values(
            result,
            ("files", "gbw", "density_container", "density_info"),
        )
        explicit_checks["electron_density_payload"] = (
            electron_count is not None
            and electron_count > 0
            and bool(density_files or response.get("output_artifacts")),
            f"electron_count={electron_count!r}; density_reference_count={len(density_files)}",
        )
    elif action_id == "export_electron_density_grid":
        output_files = _find_key_values(
            result,
            ("output_file", "density_file", "wavefunction_file", "grid_file"),
        )
        explicit_checks["density_export_materialized"] = (
            bool(output_files or response.get("output_artifacts")),
            f"result_reference_count={len(output_files)}; "
            f"artifact_count={len(response.get('output_artifacts') or [])}",
        )
    elif action_id == "calculate_electron_isodensity_surface":
        surfaces = _first_sequence(result, ("surfaces",))
        valid_surfaces = 0
        for surface in surfaces or []:
            if not isinstance(surface, dict):
                continue
            area = surface.get("surface_area_angstrom2")
            volume = surface.get("enclosed_volume_angstrom3")
            if (
                isinstance(area, (int, float))
                and isinstance(volume, (int, float))
                and float(area) > 0
                and float(volume) > 0
            ):
                valid_surfaces += 1
        explicit_checks["positive_isodensity_surfaces"] = (
            bool(surfaces) and valid_surfaces == len(surfaces),
            f"surface_count={len(surfaces or [])}; positive_area_volume_count={valid_surfaces}",
        )
    elif action_id == "enumerate_coordination_isomers":
        count = _first_number(result, ("isomer_count",))
        explicit_checks["coordination_isomers_enumerated"] = (
            count is not None and count > 0,
            f"isomer_count={count!r}",
        )
    elif action_id == "explore_reaction_network":
        complete_values = _find_key_values(result, ("pes_complete",))
        count = _first_number(result, ("reaction_record_count", "reaction_count"))
        explicit_checks["kinbot_pes_completed"] = (
            True in complete_values and count is not None and count > 0,
            f"pes_complete={complete_values[:2]!r}; reaction_count={count!r}",
        )
    elif action_id == "integrate_reaction_network":
        times = _first_sequence(result, ("times", "time_seconds", "time_points"))
        concentration_values = _find_key_values(
            result, ("concentrations", "mole_fractions", "states", "trajectory")
        )
        concentrations = next(
            (item for item in concentration_values if isinstance(item, (dict, list))),
            None,
        )
        concentration_lengths = (
            [len(item) for item in concentrations.values()]
            if isinstance(concentrations, dict)
            and all(isinstance(item, list) for item in concentrations.values())
            else [len(concentrations)]
            if isinstance(concentrations, list)
            else []
        )
        explicit_checks["kinetics_trajectory_nonempty"] = (
            bool(times)
            and bool(concentration_lengths)
            and all(length == len(times) for length in concentration_lengths),
            f"time_shape={_shape(times)}; concentration_lengths={concentration_lengths}",
        )
    elif action_id == "propagate_nonadiabatic_trajectory":
        record_count = _first_number(result, ("record_count",))
        final_time = _first_number(result, ("final_time_fs",))
        explicit_checks["nonadiabatic_trajectory_completed"] = (
            record_count is not None
            and record_count > 1
            and final_time is not None
            and final_time > 0,
            f"record_count={record_count!r}; final_time_fs={final_time!r}",
        )
    elif action_id == "scan_reaction_coordinates":
        completed = _first_number(result, ("completed_points",))
        requested = _first_number(result, ("requested_points",))
        energies = _first_sequence(result, ("energies_hartree", "energies"))
        explicit_checks["reaction_coordinate_scan_complete"] = (
            completed is not None
            and requested is not None
            and completed == requested
            and len(energies or []) == int(completed),
            f"completed_points={completed!r}; requested_points={requested!r}; "
            f"energy_count={len(energies or [])}",
        )
    elif action_id == "search_reaction_path":
        image_count = _first_number(result, ("image_count",))
        converged = _find_key_values(result, ("converged",))
        explicit_checks["reaction_path_converged"] = (
            image_count is not None and image_count >= 3 and True in converged,
            f"image_count={image_count!r}; converged={converged[:2]!r}",
        )
    elif action_id == "solvate_molecular_system":
        solvated = _find_key_values(result, ("solvated",))
        topology = _find_key_values(result, ("topology_path",))
        explicit_checks["solvated_system_materialized"] = (
            True in solvated and bool(topology or response.get("output_artifacts")),
            f"solvated={solvated[:2]!r}; topology_reference_count={len(topology)}",
        )
    elif action_id == "validate_reaction_path":
        valid_values = _find_key_values(result, ("valid",))
        explicit_checks["reaction_path_valid"] = (
            True in valid_values,
            f"valid={valid_values[:2]!r}",
        )
    elif action_id == "analyze_reaction_coordinate":
        image_count = _first_number(result, ("image_count",))
        coordinate = _first_sequence(result, ("reaction_coordinate",))
        energies = _first_sequence(result, ("energies",))
        explicit_checks["reaction_coordinate_alignment"] = (
            image_count is not None
            and image_count >= 3
            and len(coordinate or []) == int(image_count)
            and len(energies or []) == int(image_count),
            f"image_count={image_count!r}; coordinate_count={len(coordinate or [])}; "
            f"energy_count={len(energies or [])}",
        )
    for criterion_id, (passed, detail) in explicit_checks.items():
        criteria.append(_criterion(criterion_id, passed, detail))
    return criteria


def _attempt_passed(criteria: list[dict[str, Any]]) -> bool:
    return all(item["status"] == "passed" for item in criteria if item["required"])


def _attempt_outcome(response: dict[str, Any], criteria: list[dict[str, Any]]) -> str:
    if response.get("status") == "unavailable":
        return "blocked"
    if _attempt_passed(criteria):
        return "actual_execution"
    return "failure"


def _empty_record(action: Any, backend_id: str, selected: bool) -> dict[str, Any]:
    return {
        "case_id": _case_id(action.id, backend_id),
        "action": action.id,
        "backend": backend_id,
        "category": action.category,
        "primary_output": action.primary_output,
        "selected": selected,
        "execution_state": "not_executed" if selected else "not_selected",
        "status": "not_executed" if selected else "not_selected",
        "pass": False,
        "elapsed_seconds": None,
        "request_summary": None,
        "scientific_result_summary": None,
        "criteria": [
            _criterion(
                "fresh_current_run_execution",
                False if selected else None,
                "No fresh execution has been captured for this selected pair."
                if selected
                else "Pair is outside the requested selection.",
                required=selected,
            )
        ],
        "attempts": [],
        "planned_sources": [],
    }


def _refresh_pair_record(record: dict[str, Any]) -> None:
    attempts = record.get("attempts") or []
    if not attempts:
        return
    outcomes = [str(item.get("outcome") or "failure") for item in attempts]
    record["pass"] = "actual_execution" in outcomes
    if record["pass"]:
        record["execution_state"] = "actual_execution"
        record["status"] = PASS_STATUS
    elif "failure" in outcomes:
        record["execution_state"] = "failure"
        record["status"] = "failed"
    else:
        record["execution_state"] = "blocked"
        record["status"] = "blocked"
    record["elapsed_seconds"] = round(
        sum(float(item.get("elapsed_seconds") or 0.0) for item in attempts), 6
    )
    record["request_summary"] = [item.get("request_summary") for item in attempts]
    record["scientific_result_summary"] = [
        item.get("scientific_result_summary") for item in attempts
    ]
    record["criteria"] = [
        _criterion(
            "at_least_one_fresh_attempt_passed",
            record["pass"],
            f"{sum(item == 'actual_execution' for item in outcomes)}/{len(attempts)} "
            f"attempts passed; outcomes={outcomes}",
        )
    ]


def _summary(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    values = list(records.values())
    selected = [item for item in values if item.get("selected")]
    actual = [
        item for item in selected if item.get("execution_state") == "actual_execution"
    ]
    failures = [item for item in selected if item.get("execution_state") == "failure"]
    blocked = [item for item in selected if item.get("execution_state") == "blocked"]
    observed = [*actual, *failures, *blocked]
    passed = [item for item in selected if item.get("pass")]
    unexecuted = [item for item in selected if item.get("execution_state") == "not_executed"]
    return {
        "catalog_pair_count": len(values),
        "selected_pair_count": len(selected),
        "observed_pair_count": len(observed),
        "actual_execution_pair_count": len(actual),
        "passed_pair_count": len(passed),
        "failed_pair_count": len(failures),
        "blocked_pair_count": len(blocked),
        "not_executed_pair_count": len(unexecuted),
        "not_selected_pair_count": len(values) - len(selected),
        "fresh_attempt_count": sum(len(item.get("attempts") or []) for item in selected),
        "all_selected_observed": len(observed) == len(selected),
        "all_selected_executed": len(actual) == len(selected),
        "all_selected_passed": len(passed) == len(selected),
    }


def _write_report(path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = _utc_now()
    state["summary"] = _summary(state["records"])
    state["summary"]["runner_error_count"] = len(state.get("runner_errors") or [])
    payload = copy.deepcopy(state)
    payload["records"] = [payload["records"][key] for key in sorted(payload["records"])]
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _new_state(
    actions: dict[str, Any],
    pairs: list[tuple[str, str]],
    selected: set[tuple[str, str]],
    catalog_digest: str,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "validator_version": VALIDATOR_VERSION,
        "validation_run_id": str(uuid.uuid4()),
        "catalog_sha256": catalog_digest,
        "started_at": _utc_now(),
        "updated_at": _utc_now(),
        "evidence_policy": (
            "Only execute_action calls captured during this validation_run_id can pass. "
            "Tracked historical evidence/status JSON is never read as proof."
        ),
        "source_registry": {},
        "runner_errors": [],
        "summary": {},
        "records": {
            _case_id(action_id, backend_id): _empty_record(
                actions[action_id], backend_id, (action_id, backend_id) in selected
            )
            for action_id, backend_id in pairs
        },
    }


def _load_resume_state(
    path: Path,
    catalog_digest: str,
    selected: set[tuple[str, str]],
) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("resume output has an incompatible schema_version")
    if payload.get("validator_version") != VALIDATOR_VERSION:
        raise ValueError("resume output was created by a different validator version")
    if payload.get("catalog_sha256") != catalog_digest:
        raise ValueError("resume output does not match the current live catalog")
    records_value = payload.get("records")
    if not isinstance(records_value, list):
        raise ValueError("resume output records must be a list")
    payload["records"] = {str(item["case_id"]): item for item in records_value}
    requested = {_case_id(*pair) for pair in selected}
    for case_id, record in payload["records"].items():
        record["selected"] = case_id in requested
        if case_id in requested and record.get("execution_state") == "not_selected":
            record["execution_state"] = "not_executed"
            record["status"] = "not_executed"
            record["criteria"] = [
                _criterion(
                    "fresh_current_run_execution",
                    False,
                    "No fresh execution has been captured for this selected pair.",
                )
            ]
        elif case_id not in requested and record.get("execution_state") == "not_executed":
            record["execution_state"] = "not_selected"
            record["status"] = "not_selected"
    payload.setdefault("runner_errors", [])
    payload.setdefault("source_registry", {})
    payload["resumed_at"] = _utc_now()
    return payload


@contextlib.contextmanager
def _workspace_environment(workspace: Path) -> Iterator[None]:
    previous = os.environ.get("RESEARCHCHEMBENCH_WORKSPACE")
    os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("RESEARCHCHEMBENCH_WORKSPACE", None)
        else:
            os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = previous


class ValidationRun:
    def __init__(
        self,
        *,
        actions: dict[str, Any],
        backends: dict[str, Any],
        selected: set[tuple[str, str]],
        output: Path,
        state: dict[str, Any],
        resume: bool,
    ) -> None:
        self.actions = actions
        self.backends = backends
        self.selected = selected
        self.output = output
        self.state = state
        self.resume = resume
        self._record_lock = threading.RLock()

    def should_run(self, action_id: str, backend_id: str) -> bool:
        pair = (action_id, backend_id)
        if pair not in self.selected:
            return False
        record = self.state["records"][_case_id(*pair)]
        return not (self.resume and record.get("pass"))

    def add_planned_source(self, action_id: str, backend_id: str, source: str) -> None:
        record = self.state["records"].get(_case_id(action_id, backend_id))
        if record is not None and source not in record["planned_sources"]:
            record["planned_sources"].append(source)

    def has_source_pass(self, action_id: str, backend_id: str, source: str) -> bool:
        record = self.state["records"][_case_id(action_id, backend_id)]
        return any(
            item.get("source") == source and item.get("outcome") == "actual_execution"
            for item in record.get("attempts") or []
        )

    def capture_response(
        self,
        *,
        source: str,
        source_case_id: str,
        action_id: str,
        expected_backend: str,
        request: Any,
        response: dict[str, Any],
        workspace: Path | None,
        elapsed_seconds: float,
        execution_kind: str,
        execution_notes: str | None = None,
        additional_criteria: list[dict[str, Any]] | None = None,
        exception_value: dict[str, Any] | None = None,
    ) -> None:
        normalized, adaptations = _normalize_request(request)
        self.add_planned_source(action_id, expected_backend, source)
        criteria = _scientific_criteria(
            action_id, expected_backend, normalized, response, workspace
        )
        criteria.extend(additional_criteria or [])
        outcome = _attempt_outcome(response, criteria)
        attempt = {
            "attempt_id": f"{source}:{source_case_id}:{uuid.uuid4().hex[:12]}",
            "source": source,
            "source_case_id": source_case_id,
            "execution_kind": execution_kind,
            "execution_notes": execution_notes,
            "service_call_observed": True,
            "executed_at": _utc_now(),
            "elapsed_seconds": round(float(elapsed_seconds), 6),
            "request_adaptations": adaptations,
            "request_summary": _request_summary(
                action_id,
                expected_backend,
                normalized,
                workspace,
                self.actions,
                self.backends,
            ),
            "scientific_result_summary": _scientific_result_summary(response, workspace),
            "criteria": criteria,
            "outcome": outcome,
            "pass": outcome == "actual_execution",
            "exception": exception_value,
        }
        record = self.state["records"].get(_case_id(action_id, expected_backend))
        with self._record_lock:
            if record is None:
                self.state["runner_errors"].append(
                    {
                        "source": source,
                        "case_id": source_case_id,
                        "error": (
                            "Fresh runner called a pair absent from the live catalog: "
                            f"{action_id}/{expected_backend}"
                        ),
                    }
                )
            elif (action_id, expected_backend) in self.selected:
                record["attempts"].append(attempt)
                _refresh_pair_record(record)
                _write_report(self.output, self.state)

    def execute(
        self,
        *,
        source: str,
        source_case_id: str,
        action_id: str,
        expected_backend: str,
        request: Any,
        workspace: Path | None,
        force: bool = False,
    ) -> dict[str, Any]:
        normalized, _adaptations = _normalize_request(request)
        self.add_planned_source(action_id, expected_backend, source)
        if not force and not self.should_run(action_id, expected_backend):
            return service_execute_action(action_id, normalized)
        started = time.monotonic()
        response: dict[str, Any]
        exception_value: dict[str, Any] | None = None
        try:
            response = service_execute_action(action_id, normalized)
        except Exception as exc:
            response = {
                "status": "failed",
                "action": action_id,
                "requested_backend": expected_backend,
                "backend": expected_backend,
                "backend_version": None,
                "selection_source": None,
                "result": None,
                "output_artifacts": [],
                "warnings": [],
                "provenance": {},
                "error": {
                    "code": "validation_runner_exception",
                    "message": f"{type(exc).__name__}: {exc}",
                },
            }
            exception_value = {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
        elapsed = round(time.monotonic() - started, 6)
        self.capture_response(
            source=source,
            source_case_id=source_case_id,
            action_id=action_id,
            expected_backend=expected_backend,
            request=request,
            response=response,
            workspace=workspace,
            elapsed_seconds=elapsed,
            execution_kind="direct_recipe_service_call",
            exception_value=exception_value,
        )
        if exception_value is not None:
            raise RuntimeError(exception_value["message"])
        return response

    def record_factory_error(
        self,
        *,
        source: str,
        source_case_id: str,
        action_id: str,
        backend_id: str,
        exc: BaseException,
    ) -> None:
        record = self.state["records"][_case_id(action_id, backend_id)]
        criteria = [
            _criterion(
                "fresh_current_run_execution",
                False,
                f"Request factory failed before execute_action: {type(exc).__name__}: {exc}",
            )
        ]
        record["attempts"].append(
            {
                "attempt_id": f"{source}:{source_case_id}:{uuid.uuid4().hex[:12]}",
                "source": source,
                "source_case_id": source_case_id,
                "executed_at": _utc_now(),
                "elapsed_seconds": 0.0,
                "request_adaptations": [],
                "request_summary": None,
                "scientific_result_summary": None,
                "criteria": criteria,
                "execution_kind": "request_factory_failure",
                "service_call_observed": False,
                "outcome": "failure",
                "pass": False,
                "exception": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "traceback": traceback.format_exc(),
                },
            }
        )
        _refresh_pair_record(record)
        _write_report(self.output, self.state)

    def record_blocked(
        self,
        *,
        source: str,
        source_case_id: str,
        action_id: str,
        backend_id: str,
        request: Any,
        reason: str,
        workspace: Path | None,
    ) -> None:
        normalized, adaptations = _normalize_request(request)
        self.add_planned_source(action_id, backend_id, source)
        if (action_id, backend_id) not in self.selected:
            return
        record = self.state["records"][_case_id(action_id, backend_id)]
        criteria = [
            _criterion(
                "fresh_current_run_execution",
                False,
                f"Blocked before execute_action: {reason}",
            )
        ]
        record["attempts"].append(
            {
                "attempt_id": f"{source}:{source_case_id}:{uuid.uuid4().hex[:12]}",
                "source": source,
                "source_case_id": source_case_id,
                "execution_kind": "precondition_blocked",
                "service_call_observed": False,
                "executed_at": _utc_now(),
                "elapsed_seconds": 0.0,
                "request_adaptations": adaptations,
                "request_summary": _request_summary(
                    action_id,
                    backend_id,
                    normalized,
                    workspace,
                    self.actions,
                    self.backends,
                ),
                "scientific_result_summary": None,
                "criteria": criteria,
                "outcome": "blocked",
                "pass": False,
                "blocked_reason": reason,
                "exception": None,
            }
        )
        _refresh_pair_record(record)
        _write_report(self.output, self.state)


def _matrix_source(run: ValidationRun) -> int:
    module = importlib.import_module(
        "chemistry_toolbox.scripts.run_action_backend_matrix_smokes"
    )
    cases = module.all_cases()
    for case in cases:
        run.add_planned_source(case.action, case.backend, "action_backend_matrix")
    selected = [case for case in cases if run.should_run(case.action, case.backend)]
    if not selected:
        return 0
    count = 0
    with tempfile.TemporaryDirectory(prefix="researchchem-full-matrix-") as value:
        workspace = Path(value)
        context = module.Context(workspace)
        with _workspace_environment(workspace):
            for case in selected:
                try:
                    request = case.request_factory(context)
                    run.execute(
                        source="action_backend_matrix",
                        source_case_id=case.case_id,
                        action_id=case.action,
                        expected_backend=case.backend,
                        request=request,
                        workspace=workspace,
                    )
                except Exception as exc:
                    record = run.state["records"][_case_id(case.action, case.backend)]
                    if not record["attempts"] or record["attempts"][-1].get("source_case_id") != case.case_id:
                        run.record_factory_error(
                            source="action_backend_matrix",
                            source_case_id=case.case_id,
                            action_id=case.action,
                            backend_id=case.backend,
                            exc=exc,
                        )
                count += 1
    return count


def _resource_source(run: ValidationRun) -> int:
    module = importlib.import_module(
        "chemistry_toolbox.scripts.run_scientific_resource_smokes"
    )
    with tempfile.TemporaryDirectory(prefix="researchchem-full-resources-") as value:
        workspace = Path(value)
        module.prepare_docking_inputs(workspace)
        cases = [
            *module.request_cases(),
            module.gnina_case(),
            *module.orca_cases(),
            *module.model_and_vasp_cases(),
        ]
        for source_case_id, action_id, request in cases:
            run.add_planned_source(action_id, request["backend_id"], "scientific_resources")
        selected = [
            case for case in cases if run.should_run(case[1], case[2]["backend_id"])
        ]
        with _workspace_environment(workspace):
            for source_case_id, action_id, request in selected:
                try:
                    run.execute(
                        source="scientific_resources",
                        source_case_id=source_case_id,
                        action_id=action_id,
                        expected_backend=request["backend_id"],
                        request=request,
                        workspace=workspace,
                    )
                except Exception:
                    pass
        return len(selected)


def _goodvibes_source(run: ValidationRun) -> int:
    module = importlib.import_module(
        "chemistry_toolbox.scripts.run_goodvibes_action_smokes"
    )
    with tempfile.TemporaryDirectory(prefix="researchchem-full-goodvibes-") as value:
        workspace = Path(value)
        cases = module.cases(workspace)
        for _, action_id, _ in cases:
            run.add_planned_source(action_id, "goodvibes", "goodvibes")
        selected = [case for case in cases if run.should_run(case[1], "goodvibes")]
        with _workspace_environment(workspace):
            for source_case_id, action_id, request in selected:
                try:
                    run.execute(
                        source="goodvibes",
                        source_case_id=source_case_id,
                        action_id=action_id,
                        expected_backend="goodvibes",
                        request=request,
                        workspace=workspace,
                    )
                except Exception:
                    pass
        return len(selected)


def _data_cases(actions: dict[str, Any]) -> list[tuple[str, str, str, dict[str, Any]]]:
    requests = {
        "search_compounds": {
            "inputs": {"query": "water"},
            "action_settings": {"max_records": 1},
        },
        "search_protein_structures": {
            "inputs": {"query": "1CRN"},
            "action_settings": {"max_records": 1},
        },
        "search_materials": {
            "inputs": {"query": "mp-149"},
            "action_settings": {
                "max_records": 1,
                "fields": ["material_id", "formula_pretty"],
            },
        },
        "search_catalysis_records": {
            "inputs": {"query": {"reactants": "CO"}},
            "action_settings": {"max_records": 1},
        },
        "lookup_nist_webbook_species": {
            "inputs": {"query": {"identifier": "7732-18-5", "namespace": "cas"}},
            "action_settings": {"units": "SI", "max_records": 1},
        },
    }
    cases = []
    for action_id, partial in requests.items():
        request = {
            **partial,
            "method_spec": {},
            "resource_limits": {"cpu_cores": 1},
        }
        backend_id = actions[action_id].backend_ids[0]
        cases.append((action_id, action_id, backend_id, request))
    return cases


def _data_source(run: ValidationRun) -> int:
    cases = _data_cases(run.actions)
    for _, action_id, backend_id, _ in cases:
        run.add_planned_source(action_id, backend_id, "data_sources")
    selected = [case for case in cases if run.should_run(case[1], case[2])]
    load_dotenv(ROOT / "config.local.env", override=False)
    with tempfile.TemporaryDirectory(prefix="researchchem-full-data-") as value:
        workspace = Path(value)
        with _workspace_environment(workspace):
            for source_case_id, action_id, backend_id, request in selected:
                try:
                    run.execute(
                        source="data_sources",
                        source_case_id=source_case_id,
                        action_id=action_id,
                        expected_backend=backend_id,
                        request=request,
                        workspace=workspace,
                    )
                except Exception:
                    pass
    return len(selected)


def _monolithic_source(
    run: ValidationRun,
    *,
    source: str,
    module_name: str,
    output_attribute: str,
    argv: list[str],
    output_root: Path,
) -> int:
    """Capture fresh calls from a current runner whose cases are embedded in main()."""
    module = importlib.import_module(module_name)
    original_execute = module.execute_action
    original_output = getattr(module, output_attribute)
    original_argv = list(sys.argv)
    original_workspace = os.environ.get("RESEARCHCHEMBENCH_WORKSPACE")
    captured = 0

    def capture(action_id: str, request: Any) -> dict[str, Any]:
        nonlocal captured
        normalized, _ = _normalize_request(request)
        requested = normalized.get("backend_id")
        backend_id = requested or run.actions[action_id].backend_ids[0]
        run.add_planned_source(action_id, backend_id, source)
        captured += 1
        try:
            return run.execute(
                source=source,
                source_case_id=f"captured_call_{captured:03d}",
                action_id=action_id,
                expected_backend=backend_id,
                request=normalized,
                workspace=Path(os.environ["RESEARCHCHEMBENCH_WORKSPACE"])
                if os.environ.get("RESEARCHCHEMBENCH_WORKSPACE")
                else None,
            )
        except Exception as exc:
            return {
                "status": "failed",
                "action": action_id,
                "requested_backend": backend_id,
                "backend": backend_id,
                "backend_version": None,
                "selection_source": None,
                "result": None,
                "input_artifacts": [],
                "output_artifacts": [],
                "warnings": [],
                "provenance": {},
                "error": {"code": "validation_runner_exception", "message": str(exc)},
                "retryable": False,
            }

    module.execute_action = capture
    setattr(module, output_attribute, output_root / f"{source}.json")
    sys.argv = [module_name, *argv]
    try:
        try:
            module.main()
        except SystemExit as exc:
            if exc.code not in (None, 0, 1):
                raise
    finally:
        module.execute_action = original_execute
        setattr(module, output_attribute, original_output)
        sys.argv = original_argv
        if original_workspace is None:
            os.environ.pop("RESEARCHCHEMBENCH_WORKSPACE", None)
        else:
            os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = original_workspace
    return captured


def _pytest_dynamic_source(run: ValidationRun, temporary_root: Path) -> int:
    """Profile fresh calls to the real service while the current Action tests run."""
    import pytest

    test_paths = sorted((TOOLBOX_ROOT / "tests").glob("test_*.py"))
    if not test_paths:
        raise RuntimeError("No chemistry_toolbox/tests/test_*.py files were found")
    target_code = service_execute_action.__code__
    starts: dict[int, dict[str, Any]] = {}
    captured = 0
    capture_lock = threading.RLock()

    def profiler(frame, event, value):
        nonlocal captured
        if frame.f_code is not target_code:
            return profiler
        key = id(frame)
        if event == "call":
            starts[key] = {
                "started": time.monotonic(),
                "action_id": str(frame.f_locals.get("action_id") or ""),
                "request": frame.f_locals.get("request_value"),
                "workspace": os.environ.get("RESEARCHCHEMBENCH_WORKSPACE"),
                "pytest_case": os.environ.get("PYTEST_CURRENT_TEST", "pytest_dynamic"),
            }
        elif event == "return":
            call = starts.pop(key, None)
            if call is None:
                return profiler
            action_id = str(call["action_id"])
            if action_id not in run.actions:
                return profiler
            response = value if isinstance(value, dict) else {
                "status": "failed",
                "action": action_id,
                "requested_backend": None,
                "backend": None,
                "backend_version": None,
                "selection_source": None,
                "result": None,
                "input_artifacts": [],
                "output_artifacts": [],
                "warnings": [],
                "provenance": {},
                "error": {
                    "code": "pytest_dynamic_exception",
                    "message": "execute_action returned through an exception path",
                },
            }
            try:
                request, _adaptations = _normalize_request(call["request"])
                backend_id = (
                    response.get("backend")
                    or request.get("backend_id")
                    or request.get("source_id")
                )
                if backend_id is None and len(run.actions[action_id].backend_ids) == 1:
                    backend_id = run.actions[action_id].backend_ids[0]
                if backend_id is None:
                    # Negative dispatch tests deliberately reject auto/unsupported
                    # providers before a backend can be selected. They exercise the
                    # public service boundary but are not Action/backend executions.
                    return profiler
                backend_id = str(backend_id)
                run.add_planned_source(action_id, backend_id, PYTEST_DYNAMIC_SOURCE)
                if (action_id, backend_id) not in run.selected:
                    return profiler
                workspace_value = call.get("workspace")
                workspace = Path(workspace_value) if workspace_value else None
                with capture_lock:
                    captured += 1
                    run.capture_response(
                        source=PYTEST_DYNAMIC_SOURCE,
                        source_case_id=str(call["pytest_case"]).split(" ", 1)[0],
                        action_id=action_id,
                        expected_backend=backend_id,
                        request=request,
                        response=response,
                        workspace=workspace,
                        elapsed_seconds=time.monotonic() - float(call["started"]),
                        execution_kind="fresh_service_execution_under_pytest",
                        execution_notes=(
                            "The real service function was observed in this process; the named "
                            "test may monkeypatch its backend process boundary."
                        ),
                    )
            except Exception as exc:
                with capture_lock:
                    run.state["runner_errors"].append(
                        {
                            "source": PYTEST_DYNAMIC_SOURCE,
                            "action": action_id,
                            "pytest_case": call.get("pytest_case"),
                            "error": f"capture failed: {type(exc).__name__}: {exc}",
                            "traceback": traceback.format_exc(),
                        }
                    )
        return profiler

    previous_profile = sys.getprofile()
    get_thread_profile = getattr(threading, "getprofile", lambda: None)
    previous_thread_profile = get_thread_profile()
    pytest_workspace = temporary_root / "pytest-workspace"
    pytest_workspace.mkdir(parents=True, exist_ok=True)
    try:
        with _workspace_environment(pytest_workspace):
            sys.setprofile(profiler)
            threading.setprofile(profiler)
            exit_code = int(
                pytest.main(
                    [
                        "-q",
                        "-p",
                        "no:cacheprovider",
                        "--basetemp",
                        str(temporary_root / "pytest-tmp"),
                        *[str(path) for path in test_paths],
                    ]
                )
            )
    finally:
        sys.setprofile(previous_profile)
        threading.setprofile(previous_thread_profile)
    run.state["source_registry"]["pytest_dynamic"] = {
        "test_file_count": len(test_paths),
        "test_files": [str(path.relative_to(ROOT)) for path in test_paths],
        "pytest_exit_code": exit_code,
        "captured_service_call_count": captured,
        "fresh": True,
        "historical_evidence_imported": False,
    }
    if exit_code != 0:
        run.state["runner_errors"].append(
            {
                "source": PYTEST_DYNAMIC_SOURCE,
                "error": f"fresh pytest suite exited with code {exit_code}",
                "captured_service_call_count": captured,
            }
        )
    _write_report(run.output, run.state)
    if exit_code not in (0, 1, 5):
        raise RuntimeError(f"pytest dynamic runner exited with code {exit_code}")
    return captured


def _capture_report_request(action: Any, backend_id: str) -> dict[str, Any]:
    request: dict[str, Any] = {
        "inputs": {},
        "method_spec": {},
        "action_settings": {},
        "resource_limits": {"cpu_cores": 1},
    }
    if action.selection_policy == "agent_source_required":
        request["source_id"] = backend_id
    elif action.selection_policy not in {"fixed_source", "internal_deterministic"}:
        request["backend_id"] = backend_id
    return request


def _pytest_capture_report_source(run: ValidationRun, input_path: Path) -> int:
    """Import only fresh pytest profiler observations, never merged evidence."""
    resolved = input_path.resolve()
    if resolved == run.output.resolve():
        raise ValueError("--pytest-capture-report must differ from --output")
    payload_bytes = resolved.read_bytes()
    input_sha256 = _sha256_bytes(payload_bytes)
    payload = json.loads(payload_bytes.decode("utf-8"))
    generated_at = payload.get("generated_at")
    pytest_exit_code = payload.get("pytest_exit_code")
    if not isinstance(generated_at, str) or not generated_at.strip():
        raise ValueError("pytest capture report has no generated_at timestamp")
    try:
        datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("pytest capture report generated_at is not ISO-8601") from exc
    if not isinstance(pytest_exit_code, int):
        raise ValueError(
            "pytest capture report has no integer pytest_exit_code; it does not prove a fresh run"
        )
    action_entries = payload.get("actions")
    if not isinstance(action_entries, list):
        raise ValueError("pytest capture report actions must be a list")

    prior = run.state.get("source_registry", {}).get("pytest_dynamic_capture_report")
    if (
        run.resume
        and isinstance(prior, dict)
        and prior.get("input_sha256") == input_sha256
    ):
        return 0

    dynamic_observations: list[tuple[str, str, dict[str, Any]]] = []
    ignored_non_dynamic = 0
    rejected_dynamic = 0
    for action_entry in action_entries:
        if not isinstance(action_entry, dict):
            continue
        entry_action = str(action_entry.get("action") or "")
        for observation in action_entry.get("observations") or []:
            if not isinstance(observation, dict):
                continue
            if observation.get("source") != PYTEST_DYNAMIC_SOURCE:
                ignored_non_dynamic += 1
                continue
            action_id = str(observation.get("action") or entry_action)
            backend_id = str(observation.get("backend") or "")
            if (
                action_id != entry_action
                or action_id not in run.actions
                or backend_id not in run.actions[action_id].backend_ids
            ):
                rejected_dynamic += 1
                continue
            dynamic_observations.append((action_id, backend_id, observation))
    if not dynamic_observations:
        raise ValueError("pytest capture report contains no valid pytest_dynamic observations")

    imported_selected = 0
    for index, (action_id, backend_id, observation) in enumerate(
        dynamic_observations, start=1
    ):
        run.add_planned_source(action_id, backend_id, PYTEST_DYNAMIC_SOURCE)
        if (action_id, backend_id) not in run.selected:
            continue
        status = str(observation.get("status") or "unknown")
        detail = observation.get("detail")
        response = {
            "status": status,
            "action": action_id,
            "action_version": run.actions[action_id].version,
            "requested_backend": backend_id,
            "backend": backend_id,
            "backend_version": None,
            "selection_source": None,
            "result": None,
            "input_artifacts": [],
            "output_artifacts": [],
            "warnings": [
                "The fresh audit capture does not serialize the Action request/result payload."
            ],
            "provenance": {
                "pytest_capture_report_sha256": input_sha256,
                "pytest_capture_report_generated_at": generated_at,
            },
            "error": (
                None
                if status in TERMINAL_PASS_STATUSES
                else {
                    "code": "captured_pytest_observation",
                    "message": str(detail or f"captured status={status}"),
                }
            ),
        }
        elapsed = observation.get("elapsed_seconds")
        run.capture_response(
            source=PYTEST_DYNAMIC_SOURCE,
            source_case_id=f"capture_report_observation_{index:04d}",
            action_id=action_id,
            expected_backend=backend_id,
            request=_capture_report_request(run.actions[action_id], backend_id),
            response=response,
            workspace=None,
            elapsed_seconds=float(elapsed) if isinstance(elapsed, (int, float)) else 0.0,
            execution_kind="fresh_service_execution_under_pytest",
            execution_notes=(
                "Imported from the explicitly supplied fresh profiler report. Only the "
                "pytest_dynamic observation is used; merged external evidence is ignored."
            ),
            additional_criteria=[
                _criterion(
                    "complete_scientific_request_and_result_payload_available",
                    False,
                    "audit_action_test_coverage.py records status/backend but not the complete "
                    "request and scientific result; this observation cannot pass by itself.",
                )
            ],
        )
        imported_selected += 1

    run.state["source_registry"]["pytest_dynamic_capture_report"] = {
        "input_path": str(resolved),
        "input_sha256": input_sha256,
        "input_size_bytes": len(payload_bytes),
        "generated_at": generated_at,
        "pytest_exit_code": pytest_exit_code,
        "fresh_dynamic_observation_count": len(dynamic_observations),
        "imported_selected_dynamic_observation_count": imported_selected,
        "ignored_non_dynamic_observation_count": ignored_non_dynamic,
        "rejected_dynamic_observation_count": rejected_dynamic,
        "historical_or_external_observations_imported": False,
        "scientific_pass_authority": False,
    }
    if pytest_exit_code != 0:
        run.state["runner_errors"].append(
            {
                "source": PYTEST_DYNAMIC_SOURCE,
                "error": (
                    "supplied fresh pytest capture report has nonzero pytest_exit_code="
                    f"{pytest_exit_code}"
                ),
                "input_sha256": input_sha256,
            }
        )
    _write_report(run.output, run.state)
    return imported_selected


def _explicit_catalog_gap_recipes(run: ValidationRun) -> int:
    """Execute portable real recipes for pairs absent from the other fresh sources."""
    for action_id, backend_id in EXPLICIT_RECIPE_PAIRS:
        run.add_planned_source(action_id, backend_id, EXPLICIT_RECIPE_SOURCE)
    attempts = 0

    water = {
        "atoms": [
            {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [0.0, 0.757, 0.586]},
            {"element": "H", "position_angstrom": [0.0, -0.757, 0.586]},
        ],
        "charge": 0,
        "multiplicity": 1,
        "pbc": [False, False, False],
    }
    reactant = {
        "atoms": [
            {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [0.8, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    middle = {
        "atoms": [
            {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [1.0, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    product = {
        "atoms": [
            {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [1.2, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    path = {"structures": [reactant, middle, product]}

    with tempfile.TemporaryDirectory(prefix="researchchem-explicit-gap-recipes-") as value:
        workspace = Path(value)

        def wanted(action_id: str, backend_id: str) -> bool:
            if (action_id, backend_id) not in run.selected:
                return False
            return not (
                run.resume
                and run.has_source_pass(
                    action_id, backend_id, EXPLICIT_RECIPE_SOURCE
                )
            )

        def execute(
            source_case_id: str,
            action_id: str,
            backend_id: str,
            request: dict[str, Any],
            *,
            prerequisite: bool = False,
        ) -> dict[str, Any] | None:
            nonlocal attempts
            if not prerequisite and not wanted(action_id, backend_id):
                return None
            attempts += 1
            try:
                return run.execute(
                    source=EXPLICIT_RECIPE_SOURCE,
                    source_case_id=source_case_id,
                    action_id=action_id,
                    expected_backend=backend_id,
                    request=request,
                    workspace=workspace,
                    force=True,
                )
            except Exception:
                return None

        def blocked(
            source_case_id: str,
            action_id: str,
            backend_id: str,
            request: dict[str, Any],
            reason: str,
        ) -> None:
            nonlocal attempts
            if not wanted(action_id, backend_id):
                return
            attempts += 1
            run.record_blocked(
                source=EXPLICIT_RECIPE_SOURCE,
                source_case_id=source_case_id,
                action_id=action_id,
                backend_id=backend_id,
                request=request,
                reason=reason,
                workspace=workspace,
            )

        with _workspace_environment(workspace):
            internal_requests = (
                (
                    "enumerate_coordination_isomers_internal",
                    "enumerate_coordination_isomers",
                    {
                        "inputs": {
                            "structure": {
                                "atoms": [
                                    {"element": "P", "position_angstrom": [0, 0, 0]},
                                    *[
                                        {
                                            "element": "C",
                                            "position_angstrom": [index, 0, 0],
                                        }
                                        for index in range(1, 6)
                                    ],
                                ]
                            },
                            "coordination_center_index": 0,
                            "ligand_anchor_indices": [1, 2, 3, 4, 5],
                            "ligand_labels": ["A", "B", "B", "C", "C"],
                        },
                        "method_spec": {},
                        "action_settings": {
                            "coordination_geometry": "trigonal_bipyramidal",
                            "max_isomers": 20,
                        },
                        "resource_limits": {"cpu_cores": 1},
                    },
                ),
                (
                    "validate_reaction_path_internal",
                    "validate_reaction_path",
                    {
                        "inputs": {
                            "path": path,
                            "reactant": reactant,
                            "product": product,
                            "bond_changes": [
                                {"type": "break", "atom_indices": [0, 1]}
                            ],
                        },
                        "method_spec": {},
                        "action_settings": {
                            "endpoint_rmsd_tolerance_angstrom": 0.01,
                            "maximum_image_step_rmsd_angstrom": 0.3,
                            "bond_distance_tolerance_angstrom": 0.2,
                        },
                        "resource_limits": {"cpu_cores": 1},
                    },
                ),
                (
                    "analyze_reaction_coordinate_internal",
                    "analyze_reaction_coordinate",
                    {
                        "inputs": {
                            "path": path,
                            "energies": [-1.0, -0.9, -1.1],
                        },
                        "method_spec": {},
                        "action_settings": {"energy_unit": "hartree"},
                        "resource_limits": {"cpu_cores": 1},
                    },
                ),
            )
            for source_case_id, action_id, request in internal_requests:
                execute(
                    source_case_id,
                    action_id,
                    "internal_reaction_analysis",
                    request,
                )

            execute(
                "openff_ethanol_parameters",
                "assign_force_field_parameters",
                "openff",
                {
                    "backend_id": "openff",
                    "inputs": {"structure": {"smiles": "CCO"}},
                    "method_spec": {
                        "force_field": "openff_unconstrained-2.3.0.offxml"
                    },
                    "action_settings": {},
                    "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
                },
            )
            execute(
                "openff_am1bcc_ethanol",
                "assign_partial_charges",
                "openff_am1bcc",
                {
                    "backend_id": "openff_am1bcc",
                    "inputs": {"structure": {"smiles": "CCO"}},
                    "method_spec": {"charge_model": "am1bcc"},
                    "action_settings": {},
                    "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
                },
            )
            execute(
                "scipy_first_order_a_to_b",
                "integrate_reaction_network",
                "scipy",
                {
                    "backend_id": "scipy",
                    "inputs": {
                        "network": {
                            "species": ["A", "B"],
                            "reactions": [
                                {
                                    "reactants": {"A": 1},
                                    "products": {"B": 1},
                                    "forward_rate_constant": 1.0,
                                }
                            ],
                        },
                        "initial_state": {"A": 1.0, "B": 0.0},
                    },
                    "method_spec": {},
                    "action_settings": {
                        "time_end_seconds": 1.0,
                        "num_points": 5,
                    },
                    "resource_limits": {"cpu_cores": 1},
                },
            )

            solute_path = workspace / "packmol_solute.pdb"
            solute_path.write_text(
                "HETATM    1  C   MOL A   1       0.000   0.000   0.000  "
                "1.00  0.00           C\nEND\n",
                encoding="utf-8",
            )
            solvent_path = workspace / "packmol_water.pdb"
            solvent_path.write_text(
                "HETATM    1  O   HOH A   1       0.000   0.000   0.000  "
                "1.00  0.00           O\n"
                "HETATM    2  H1  HOH A   1       0.957   0.000   0.000  "
                "1.00  0.00           H\n"
                "HETATM    3  H2  HOH A   1      -0.240   0.927   0.000  "
                "1.00  0.00           H\nEND\n",
                encoding="utf-8",
            )
            execute(
                "packmol_three_waters",
                "solvate_molecular_system",
                "packmol",
                {
                    "backend_id": "packmol",
                    "inputs": {
                        "system": {
                            "solute_path": solute_path.name,
                            "force_field": "validation-only",
                            "solvated": False,
                        }
                    },
                    "method_spec": {},
                    "action_settings": {
                        "box_shape": "cubic",
                        "box_size_angstrom": [20.0, 20.0, 20.0],
                        "solvent_model": "explicit_water",
                        "solvent_path": solvent_path.name,
                        "molecule_counts": {"solvent": 3},
                        "tolerance_angstrom": 2.0,
                    },
                    "resource_limits": {"cpu_cores": 1},
                },
            )

            pysis_common = {
                "method_spec": {"calculator_backend": "xtb", "method": "gfn2"},
                "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
            }
            execute(
                "pysisyphus_h2_relaxed_scan",
                "scan_reaction_coordinates",
                "pysisyphus",
                {
                    "backend_id": "pysisyphus",
                    "inputs": {"structure": reactant},
                    **pysis_common,
                    "action_settings": {
                        "coordinate_type": "bond",
                        "atom_indices": [0, 1],
                        "start_value": 0.8,
                        "end_value": 0.9,
                        "value_unit": "angstrom",
                        "steps": 1,
                        "optimizer": "rfo",
                        "convergence": "gau_loose",
                        "max_cycles": 25,
                        "hessian_init": "fischer",
                    },
                },
            )
            execute(
                "pysisyphus_h2_neb",
                "search_reaction_path",
                "pysisyphus",
                {
                    "backend_id": "pysisyphus",
                    "inputs": {"reactant": reactant, "product": product},
                    **pysis_common,
                    "action_settings": {
                        "path_method": "neb",
                        "interpolation": "linear",
                        "images": 5,
                        "optimizer": "qm",
                        "convergence": "gau_loose",
                        "max_cycles": 25,
                        "climb": False,
                    },
                },
            )

            yambo_root = (
                ROOT
                / ".software_cache"
                / "validation"
                / "yambo"
                / "smoke"
                / "qe_si_gw_bse"
            )
            gw_request = {
                "backend_id": "yambo",
                "inputs": {"save_directory": "SAVE", "input_file": "gw.in"},
                "method_spec": {},
                "action_settings": {
                    "job_name": "gw",
                    "maximum_returned_records": 20,
                    "require_normal_exit": True,
                },
                "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
            }
            bse_request = {
                "backend_id": "yambo",
                "inputs": {
                    "save_directory": "SAVE",
                    "input_file": "bse.in",
                    "restart_directories": ["gw"],
                },
                "method_spec": {},
                "action_settings": {
                    "job_name": "bse,gw",
                    "maximum_returned_records": 100,
                    "require_normal_exit": True,
                },
                "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
            }
            yambo_ready = all(
                (yambo_root / name).exists()
                for name in ("SAVE", "gw", "gw.in", "bse.in")
            )
            if yambo_ready:
                shutil.copytree(yambo_root / "SAVE", workspace / "SAVE")
                shutil.copytree(yambo_root / "gw", workspace / "gw")
                shutil.copy2(yambo_root / "gw.in", workspace / "gw.in")
                shutil.copy2(yambo_root / "bse.in", workspace / "bse.in")
                execute(
                    "yambo_si_gw",
                    "calculate_quasiparticle_corrections",
                    "yambo",
                    gw_request,
                )
                execute(
                    "yambo_si_bse",
                    "calculate_bse_optical_spectrum",
                    "yambo",
                    bse_request,
                )
            else:
                reason = f"required Yambo SAVE/GW fixture is incomplete: {yambo_root}"
                blocked(
                    "yambo_si_gw",
                    "calculate_quasiparticle_corrections",
                    "yambo",
                    gw_request,
                    reason,
                )
                blocked(
                    "yambo_si_bse",
                    "calculate_bse_optical_spectrum",
                    "yambo",
                    bse_request,
                    reason,
                )

            sharc_root = (
                ROOT
                / ".software_cache"
                / "installations"
                / "sharc"
                / "source"
                / "tests"
                / "INPUT"
                / "LVC_overlap"
            )
            sharc_request = {
                "backend_id": "sharc",
                "inputs": {"trajectory_directory": "trajectory"},
                "method_spec": {"interface": "lvc"},
                "action_settings": {
                    "input_filename": "input",
                    "expected_final_time_fs": 30.0,
                    "final_time_tolerance_fs": 1.0e-6,
                    "maximum_returned_steps": 100,
                },
                "resource_limits": {"cpu_cores": 1, "memory_mb": 2048},
            }
            if sharc_root.is_dir():
                shutil.copytree(sharc_root, workspace / "trajectory")
                execute(
                    "sharc_lvc_overlap_30fs",
                    "propagate_nonadiabatic_trajectory",
                    "sharc",
                    sharc_request,
                )
            else:
                blocked(
                    "sharc_lvc_overlap_30fs",
                    "propagate_nonadiabatic_trajectory",
                    "sharc",
                    sharc_request,
                    f"required SHARC LVC fixture is missing: {sharc_root}",
                )

            kinbot_source = (
                ROOT
                / ".software_cache"
                / "validation"
                / "kinbot"
                / "smoke"
                / "action_nonempty_pes_validated3"
                / "input.json"
            )
            kinbot_request = {
                "backend_id": "kinbot",
                "inputs": {"input_file": "kinbot_input.json"},
                "method_spec": {},
                "action_settings": {
                    "maximum_returned_reactions": 100,
                    "require_pes_done": True,
                    "sella_force_threshold_ev_per_angstrom": 5.0e-4,
                    "sella_max_steps": 100,
                    "imaginary_frequency_threshold_cm1": 100.0,
                },
                "resource_limits": {"cpu_cores": 1, "memory_mb": 4096},
            }
            if kinbot_source.is_file():
                shutil.copy2(kinbot_source, workspace / "kinbot_input.json")
                execute(
                    "kinbot_formaldehyde_homolytic_scission",
                    "explore_reaction_network",
                    "kinbot",
                    kinbot_request,
                )
            else:
                blocked(
                    "kinbot_formaldehyde_homolytic_scission",
                    "explore_reaction_network",
                    "kinbot",
                    kinbot_request,
                    f"validated KinBot PES input is missing: {kinbot_source}",
                )

            density_request = {
                "backend_id": "orca",
                "inputs": {"structure": water},
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
                "resource_limits": {"cpu_cores": 1, "memory_mb": 1000},
            }
            density = execute(
                "orca_water_scf_density",
                "calculate_correlated_electron_density",
                "orca",
                density_request,
                prerequisite=(
                    ("export_electron_density_grid", "orca") in run.selected
                    or (
                        "calculate_electron_isodensity_surface",
                        "multiwfn",
                    )
                    in run.selected
                ),
            )
            density_artifact = None
            if density and density.get("status") == "success":
                density_artifact = next(
                    (
                        item
                        for item in density.get("output_artifacts") or []
                        if item.get("semantic_type") == "ElectronDensityResult"
                    ),
                    None,
                )
            export_template = {
                "backend_id": "orca",
                "inputs": {
                    "electron_density": density_artifact
                    or {"upstream_recipe": "orca_water_scf_density"}
                },
                "method_spec": {},
                "action_settings": {
                    "density_source": "scf",
                    "output_format": "wfn",
                },
                "resource_limits": {"cpu_cores": 1, "memory_mb": 1000},
            }
            exported = None
            if density_artifact is not None:
                exported = execute(
                    "orca_water_density_wfn_export",
                    "export_electron_density_grid",
                    "orca",
                    export_template,
                    prerequisite=(
                        (
                            "calculate_electron_isodensity_surface",
                            "multiwfn",
                        )
                        in run.selected
                    ),
                )
            else:
                blocked(
                    "orca_water_density_wfn_export",
                    "export_electron_density_grid",
                    "orca",
                    export_template,
                    "ORCA density prerequisite did not return a successful ElectronDensityResult artifact",
                )
            wavefunction = None
            if exported and exported.get("status") == "success":
                wavefunction = next(
                    (
                        item
                        for item in exported.get("output_artifacts") or []
                        if item.get("semantic_type")
                        == "ElectronDensityWavefunction"
                    ),
                    None,
                )
            surface_request = {
                "backend_id": "multiwfn",
                "inputs": {
                    "density_file": wavefunction
                    or {"upstream_recipe": "orca_water_density_wfn_export"}
                },
                "method_spec": {},
                "action_settings": {
                    "cutoffs_au": [0.001, 0.002],
                    "grid_spacing_bohr": 0.2,
                },
                "resource_limits": {"cpu_cores": 2, "memory_mb": 1000},
            }
            if wavefunction is not None:
                execute(
                    "multiwfn_water_isodensity_surfaces",
                    "calculate_electron_isodensity_surface",
                    "multiwfn",
                    surface_request,
                )
            else:
                blocked(
                    "multiwfn_water_isodensity_surfaces",
                    "calculate_electron_isodensity_surface",
                    "multiwfn",
                    surface_request,
                    "ORCA WFN export prerequisite did not return a successful wavefunction artifact",
                )
    return attempts


def _discover_factory_pairs(actions: dict[str, Any]) -> dict[tuple[str, str], list[str]]:
    discovered: dict[tuple[str, str], list[str]] = {}

    def add(action_id: str, backend_id: str, source: str) -> None:
        discovered.setdefault((action_id, backend_id), []).append(source)

    matrix = importlib.import_module(
        "chemistry_toolbox.scripts.run_action_backend_matrix_smokes"
    )
    for case in matrix.all_cases():
        add(case.action, case.backend, "action_backend_matrix")
    resources = importlib.import_module(
        "chemistry_toolbox.scripts.run_scientific_resource_smokes"
    )
    for _, action_id, request in [
        *resources.request_cases(),
        resources.gnina_case(),
        *resources.orca_cases(),
        *resources.model_and_vasp_cases(),
    ]:
        add(action_id, request["backend_id"], "scientific_resources")
    for action_id in (
        "derive_thermochemistry",
        "scan_thermochemistry_temperature",
        "analyze_thermochemical_ensemble",
        "validate_thermochemistry_inputs",
        "analyze_thermochemical_selectivity",
        "analyze_reaction_free_energy_profile",
    ):
        add(action_id, "goodvibes", "goodvibes")
    for _, action_id, backend_id, _ in _data_cases(actions):
        add(action_id, backend_id, "data_sources")
    for action_id, backend_id in EXPLICIT_RECIPE_PAIRS:
        add(action_id, backend_id, EXPLICIT_RECIPE_SOURCE)
    return discovered


def _select_pairs(
    actions: dict[str, Any],
    pairs: list[tuple[str, str]],
    groups: list[str],
    cases: list[str],
) -> set[tuple[str, str]]:
    known_groups = {action.category for action in actions.values()}
    unknown_groups = set(groups) - known_groups
    if unknown_groups:
        raise ValueError(f"unknown group(s): {sorted(unknown_groups)}")
    selected = {
        pair for pair in pairs if not groups or actions[pair[0]].category in set(groups)
    }
    if cases:
        requested = {_pair_from_case_id(value) for value in cases}
        unknown = requested - set(pairs)
        if unknown:
            raise ValueError(
                f"case id(s) absent from the live catalog: {sorted(_case_id(*pair) for pair in unknown)}"
            )
        selected &= requested
    return selected


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="Explicit JSON report path. Required unless --list is used.",
    )
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        help="Run one catalog category; repeatable.",
    )
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="Run one exact <action>__<backend> pair; repeatable.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Continue the same validation_run_id from --output and skip passed pairs.",
    )
    parser.add_argument(
        "--pytest-capture-report",
        type=Path,
        help=(
            "Import only source=pytest_dynamic observations from a freshly generated "
            "audit_action_test_coverage.py report instead of rerunning pytest."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all live catalog pairs and currently discoverable fresh case factories.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    actions, backends, pairs = _catalog()
    try:
        selected = _select_pairs(actions, pairs, args.group, args.case)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    discovered = _discover_factory_pairs(actions)
    if args.list:
        print("category\taction\tbackend\tcase_id\tfresh_case_factories")
        for action_id, backend_id in pairs:
            if (action_id, backend_id) not in selected:
                continue
            print(
                "\t".join(
                    (
                        actions[action_id].category,
                        action_id,
                        backend_id,
                        _case_id(action_id, backend_id),
                        ",".join(sorted(discovered.get((action_id, backend_id), []))) or "-",
                    )
                )
            )
        return 0
    if args.output is None:
        raise SystemExit("--output is required unless --list is used")
    if not selected:
        raise SystemExit("selection is empty")
    if args.pytest_capture_report is not None:
        if not args.pytest_capture_report.is_file():
            raise SystemExit(
                f"--pytest-capture-report does not exist: {args.pytest_capture_report}"
            )
        if args.pytest_capture_report.resolve() == args.output.resolve():
            raise SystemExit("--pytest-capture-report must differ from --output")

    catalog_digest = _catalog_hash(actions, backends)
    if args.resume:
        if not args.output.is_file():
            raise SystemExit(f"--resume output does not exist: {args.output}")
        try:
            state = _load_resume_state(args.output, catalog_digest, selected)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise SystemExit(f"cannot resume: {exc}") from exc
    else:
        state = _new_state(actions, pairs, selected, catalog_digest)
    run = ValidationRun(
        actions=actions,
        backends=backends,
        selected=selected,
        output=args.output,
        state=state,
        resume=args.resume,
    )
    for pair, sources in discovered.items():
        for source in sources:
            run.add_planned_source(*pair, source)
    state.setdefault("source_registry", {}).update({
        "factory_sources": list(FACTORY_SOURCES),
        "monolithic_fresh_capture_sources": list(MONOLITHIC_SOURCES),
        "pytest_dynamic_source": PYTEST_DYNAMIC_SOURCE,
        "explicit_recipe_source": EXPLICIT_RECIPE_SOURCE,
        "explicit_recipe_pair_count": len(EXPLICIT_RECIPE_PAIRS),
        "catalog_target_pair_count": len(pairs),
        "discovered_direct_recipe_pair_count": len(discovered),
        "fresh_pass_requires_current_validation_run_id": True,
        "pytest_capture_mode": (
            "import_explicit_fresh_report"
            if args.pytest_capture_report is not None
            else "run_fresh_pytest_in_process"
            if not args.group and not args.case
            else "not_run_for_filtered_selection"
        ),
        "policy": (
            "Factories are imported from current scripts. Monolithic runners and the real "
            "service.execute_action function under fresh pytest are instrumented in-process. "
            "All auxiliary output is temporary. No tracked evidence is read as pass evidence."
        ),
    })
    _write_report(args.output, state)

    source_functions: list[tuple[str, Callable[[ValidationRun], int]]] = [
        ("action_backend_matrix", _matrix_source),
        ("scientific_resources", _resource_source),
        ("goodvibes", _goodvibes_source),
        ("data_sources", _data_source),
    ]
    for source, function in source_functions:
        try:
            count = function(run)
            print(f"{source}: {count} fresh selected attempt(s)", flush=True)
        except Exception as exc:
            state["runner_errors"].append(
                {
                    "source": source,
                    "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            )
            _write_report(args.output, state)
            print(f"{source}: runner error: {type(exc).__name__}: {exc}", file=sys.stderr)

    # Embedded-case runners cannot honor pair-level filters without executing unrelated
    # chemistry. They are therefore used only for a complete, unfiltered catalog run.
    if not args.group and not args.case:
        with tempfile.TemporaryDirectory(prefix="researchchem-full-runner-output-") as value:
            output_root = Path(value)
            monolithic = (
                (
                    "action_gap",
                    "chemistry_toolbox.scripts.run_action_gap_smokes",
                    "STATUS_PATH",
                    ["--include-network"],
                ),
                (
                    "backend_gap",
                    "chemistry_toolbox.scripts.run_backend_gap_smokes",
                    "STATUS_PATH",
                    [],
                ),
            )
            for source, module_name, output_attribute, source_argv in monolithic:
                try:
                    count = _monolithic_source(
                        run,
                        source=source,
                        module_name=module_name,
                        output_attribute=output_attribute,
                        argv=source_argv,
                        output_root=output_root,
                    )
                    print(f"{source}: captured {count} fresh call(s)", flush=True)
                except Exception as exc:
                    state["runner_errors"].append(
                        {
                            "source": source,
                            "error": f"{type(exc).__name__}: {exc}",
                            "traceback": traceback.format_exc(),
                        }
                    )
                    _write_report(args.output, state)
                    print(f"{source}: runner error: {type(exc).__name__}: {exc}", file=sys.stderr)

            if args.pytest_capture_report is None:
                try:
                    count = _pytest_dynamic_source(run, output_root)
                    print(
                        f"{PYTEST_DYNAMIC_SOURCE}: captured {count} fresh service call(s)",
                        flush=True,
                    )
                except Exception as exc:
                    state["runner_errors"].append(
                        {
                            "source": PYTEST_DYNAMIC_SOURCE,
                            "error": f"{type(exc).__name__}: {exc}",
                            "traceback": traceback.format_exc(),
                        }
                    )
                    _write_report(args.output, state)
                    print(
                        f"{PYTEST_DYNAMIC_SOURCE}: runner error: {type(exc).__name__}: {exc}",
                        file=sys.stderr,
                    )

    if args.pytest_capture_report is not None:
        try:
            count = _pytest_capture_report_source(run, args.pytest_capture_report)
            print(
                f"{PYTEST_DYNAMIC_SOURCE}: imported {count} selected fresh observation(s) "
                f"from {args.pytest_capture_report}",
                flush=True,
            )
        except Exception as exc:
            state["runner_errors"].append(
                {
                    "source": PYTEST_DYNAMIC_SOURCE,
                    "capture_report": str(args.pytest_capture_report),
                    "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            )
            _write_report(args.output, state)
            print(
                f"{PYTEST_DYNAMIC_SOURCE}: capture report error: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )

    try:
        count = _explicit_catalog_gap_recipes(run)
        print(
            f"{EXPLICIT_RECIPE_SOURCE}: {count} fresh or blocked recipe attempt(s)",
            flush=True,
        )
    except Exception as exc:
        state["runner_errors"].append(
            {
                "source": EXPLICIT_RECIPE_SOURCE,
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            }
        )
        _write_report(args.output, state)
        print(
            f"{EXPLICIT_RECIPE_SOURCE}: runner error: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )

    _write_report(args.output, state)
    summary = state["summary"]
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    print(args.output.resolve())
    return 0 if summary["all_selected_passed"] and not state["runner_errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

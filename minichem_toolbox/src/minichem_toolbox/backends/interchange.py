"""Scientific schema normalization and existing-output parsing actions."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from .common import (
    atoms_and_coordinates,
    module_version,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    structure_dict,
    success,
    unwrap_artifact,
    unsupported,
    write_json,
)


ACTIONS = {
    "normalize_qcschema_molecule",
    "validate_qcschema_record",
    "parse_quantum_chemistry_output",
}


def _model_json(model: Any) -> dict[str, Any]:
    return json.loads(model.json())


def _record_value(value: Any) -> Any:
    item = unwrap_artifact(value)
    if isinstance(item, dict) and "result" in item and len(item) == 1:
        item = item["result"]
    if isinstance(item, dict) and isinstance(item.get("path"), str):
        item = item["path"]
    if isinstance(item, (str, Path)):
        path = resolve_input_file(item)
        return json.loads(path.read_text(encoding="utf-8"))
    return item


def _normalize_qcschema_molecule(request: dict[str, Any]) -> dict[str, Any]:
    import qcelemental as qcel

    inputs, _method, settings = request_parts(request)
    value = _record_value(inputs["structure"])
    if isinstance(value, dict) and value.get("schema_name") == "qcschema_molecule":
        molecule = qcel.models.Molecule(**value)
    else:
        structure = structure_dict(value)
        symbols, coordinates = atoms_and_coordinates(structure)
        bohr_per_angstrom = 1.0 / 0.529177210903
        geometry = [
            [float(component * bohr_per_angstrom) for component in position]
            for position in coordinates
        ]
        molecule = qcel.models.Molecule(
            symbols=symbols,
            geometry=geometry,
            molecular_charge=int(structure.get("charge", 0)),
            molecular_multiplicity=int(structure.get("multiplicity", 1)),
            fix_com=bool(settings["fix_center_of_mass"]),
            fix_orientation=bool(settings["fix_orientation"]),
        )
    normalized = _model_json(molecule)
    directory = output_directory("normalize_qcschema_molecule", "qcelemental")
    path = write_json(directory, "qcschema_molecule.json", normalized)
    return success(
        {
            "molecule": normalized,
            "schema_name": normalized.get("schema_name"),
            "schema_version": normalized.get("schema_version"),
            "geometry_unit": "bohr",
            "atom_count": len(normalized.get("symbols") or []),
        },
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "QCSchemaMolecule",
                "media_type": "application/json",
            }
        ],
        backend_version=module_version("qcelemental"),
    )


def _validate_qcschema_record(request: dict[str, Any]) -> dict[str, Any]:
    import qcelemental as qcel

    inputs, _method, settings = request_parts(request)
    record = _record_value(inputs["record"])
    if not isinstance(record, dict):
        raise ValueError("record must resolve to a JSON object")
    record_type = str(settings["record_type"]).strip().lower()
    models = {
        "molecule": qcel.models.Molecule,
        "atomic_input": qcel.models.AtomicInput,
        "atomic_result": qcel.models.AtomicResult,
        "optimization_input": qcel.models.OptimizationInput,
        "optimization_result": qcel.models.OptimizationResult,
    }
    if record_type not in models:
        raise ValueError(
            "record_type must be molecule, atomic_input, atomic_result, "
            "optimization_input, or optimization_result"
        )
    directory = output_directory("validate_qcschema_record", "qcelemental")
    try:
        normalized = _model_json(models[record_type](**record))
    except Exception as exc:
        errors = exc.errors() if hasattr(exc, "errors") else [{"message": str(exc)}]
        result = {
            "valid": False,
            "record_type": record_type,
            "errors": errors,
            "normalized_record": None,
        }
        path = write_json(directory, "validation_result.json", result)
        return success(
            result,
            artifact_files=[
                {
                    "path": relative_workspace_path(path),
                    "semantic_type": "QCSchemaValidationResult",
                    "media_type": "application/json",
                }
            ],
            backend_version=module_version("qcelemental"),
        )
    result = {
        "valid": True,
        "record_type": record_type,
        "errors": [],
        "normalized_record": normalized,
        "schema_name": normalized.get("schema_name"),
        "schema_version": normalized.get("schema_version"),
    }
    path = write_json(directory, "validated_record.json", result)
    return success(
        result,
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "QCSchemaValidationResult",
                "media_type": "application/json",
            }
        ],
        backend_version=module_version("qcelemental"),
    )


_CCLIB_GROUPS: dict[str, tuple[str, ...]] = {
    "metadata": (
        "metadata", "charge", "mult", "natom", "nbasis", "nmo", "coreelectrons",
    ),
    "atom_coordinates": ("atomcoords", "atomnos", "atommasses"),
    "energies": (
        "scfenergies", "mpenergies", "ccenergies", "dispersionenergies",
        "freeenergy", "enthalpy", "entropy", "temperature", "zpve",
    ),
    "gradients": ("grads",),
    "hessian": ("hessian",),
    "vibrational_frequencies": ("vibfreqs", "vibdisps"),
    "vibrational_intensities": ("vibirs", "vibramans", "vibfconsts", "vibrmasses"),
    "molecular_orbitals": ("moenergies", "homos", "mosyms", "mocoeffs"),
    "charges": ("atomcharges", "atomspins"),
    "multipoles": ("moments", "polarizabilities"),
    "excited_states": ("etenergies", "etoscs", "etsyms", "etsecs"),
}


_CCLIB_UNITS = {
    "atomcoords": "angstrom",
    "scfenergies": "eV",
    "mpenergies": "eV",
    "ccenergies": "eV",
    "dispersionenergies": "eV",
    "freeenergy": "hartree_per_particle",
    "enthalpy": "hartree_per_particle",
    "entropy": "hartree_per_particle_kelvin",
    "temperature": "kelvin",
    "zpve": "hartree_per_particle",
    "grads": "hartree_per_bohr",
    "hessian": "hartree_per_bohr_squared",
    "vibfreqs": "inverse_centimeter",
    "vibirs": "kilometer_per_mole",
    "vibramans": "angstrom_fourth_per_amu",
    "moenergies": "eV",
    "etenergies": "inverse_centimeter",
}


def _array_elements(value: Any) -> int:
    if isinstance(value, dict):
        return sum(_array_elements(item) for item in value.values())
    if isinstance(value, list):
        return sum(_array_elements(item) for item in value)
    return 1


def _append_orca_scf_targets_compat(parser: Any, inputfile: Any, line: str) -> bool:
    """Handle ORCA blocks whose first convergence report omits RMS-density."""

    while "Last Energy change" not in line:
        line = next(inputfile)
    delta_energy_value = float(line.split()[4])
    delta_energy_target = float(line.split()[7])
    line = next(inputfile)
    used_workaround = False
    if "Last MAX-Density change" in line:
        maximum_density_value = float(line.split()[4])
        maximum_density_target = float(line.split()[7])
        line = next(inputfile)
        if "Last RMS-Density change" in line:
            rms_density_value = float(line.split()[4])
            rms_density_target = float(line.split()[7])
        else:
            previous_values = parser.scfvalues[-1][-1]
            rms_density_value = (
                float(previous_values[2]) if len(previous_values) > 2 else math.nan
            )
            if parser.scftargets:
                rms_density_target = float(parser.scftargets[-1][2])
                if delta_energy_target != parser.scftargets[-1][0]:
                    raise ValueError("ORCA SCF energy target changed unexpectedly")
                if maximum_density_target != parser.scftargets[-1][1]:
                    raise ValueError("ORCA SCF maximum-density target changed unexpectedly")
            else:
                # ORCA 4 may omit the RMS target in the first convergence
                # summary. cclib 1.8.1 indexes a nonexistent previous target.
                # Preserve the missing value as NaN; it is parser metadata and
                # does not alter any electronic energy or requested property.
                rms_density_target = math.nan
                used_workaround = True
        parser.scfvalues[-1].append(
            [delta_energy_value, maximum_density_value, rms_density_value]
        )
        parser.scftargets.append(
            [delta_energy_target, maximum_density_target, rms_density_target]
        )
    return used_workaround


def _ccread_with_orca_compatibility(source: Path) -> tuple[Any, list[str]]:
    """Run cclib with a narrow ORCA 4/cclib 1.8.1 convergence-block fix."""

    from cclib.io import ccread
    from cclib.parser.orcaparser import ORCA

    original = ORCA._append_scfvalues_scftargets
    workaround_used = False

    def patched(parser: Any, inputfile: Any, line: str) -> None:
        nonlocal workaround_used
        workaround_used = (
            _append_orca_scf_targets_compat(parser, inputfile, line)
            or workaround_used
        )

    ORCA._append_scfvalues_scftargets = patched
    try:
        parsed = ccread(str(source), loglevel=40)
    except Exception as exc:
        raise RuntimeError(
            f"cclib could not parse {source.name}: {type(exc).__name__}: {exc}"
        ) from exc
    finally:
        ORCA._append_scfvalues_scftargets = original
    warnings = []
    if workaround_used:
        warnings.append(
            "Applied the cclib 1.8.1 compatibility fix for an ORCA convergence block "
            "whose first summary omitted the RMS-density target; electronic energies "
            "and requested scientific properties were not changed."
        )
    return parsed, warnings


def _parse_quantum_output(request: dict[str, Any]) -> dict[str, Any]:
    import cclib

    inputs, _method, settings = request_parts(request)
    source = resolve_input_file(inputs["output_file"])
    requested = settings["properties"]
    if not isinstance(requested, (list, tuple)) or not requested:
        raise ValueError("properties must be a non-empty list")
    groups = []
    for value in requested:
        group = str(value).strip().lower()
        if group not in _CCLIB_GROUPS:
            raise ValueError(
                f"Unknown cclib property group {group!r}; choose from {sorted(_CCLIB_GROUPS)}"
            )
        if group not in groups:
            groups.append(group)
    coordinate_frames = str(settings["coordinate_frames"]).strip().lower()
    if coordinate_frames not in {"last", "all"}:
        raise ValueError("coordinate_frames must be last or all")
    for name in ("include_orbital_coefficients", "include_excited_state_configurations"):
        if not isinstance(settings[name], bool):
            raise ValueError(f"{name} must be an explicit boolean")
    maximum = int(settings["max_array_elements"])
    if maximum < 1 or maximum > 100000000:
        raise ValueError("max_array_elements must be between 1 and 100000000")

    parsed, parser_warnings = _ccread_with_orca_compatibility(source)
    if parsed is None:
        raise RuntimeError("cclib could not recognize or parse the supplied output file")
    attributes = parsed.getattributes(tolists=True)
    selected: dict[str, Any] = {}
    missing_groups = []
    for group in groups:
        present = False
        for attribute in _CCLIB_GROUPS[group]:
            if attribute == "mocoeffs" and not settings["include_orbital_coefficients"]:
                continue
            if attribute == "etsecs" and not settings["include_excited_state_configurations"]:
                continue
            if attribute not in attributes:
                continue
            value = attributes[attribute]
            if attribute == "atomcoords" and coordinate_frames == "last" and value:
                value = value[-1]
            selected[attribute] = value
            present = True
        if not present:
            missing_groups.append(group)
    element_count = _array_elements(selected)
    if element_count > maximum:
        raise ValueError(
            f"Selected cclib data contains {element_count} scalar elements, exceeding "
            f"max_array_elements={maximum}; request fewer groups or raise the explicit limit"
        )
    metadata = dict(attributes.get("metadata") or {})
    result = {
        "parser": metadata.get("package") or parsed.__class__.__module__.split(".")[-1],
        "parser_class": parsed.__class__.__name__,
        "source_path": relative_workspace_path(source),
        "requested_property_groups": groups,
        "missing_property_groups": missing_groups,
        "coordinate_frames": coordinate_frames,
        "properties": selected,
        "attribute_units": {
            name: unit for name, unit in _CCLIB_UNITS.items() if name in selected
        },
        "scalar_element_count": element_count,
    }
    directory = output_directory("parse_quantum_chemistry_output", "cclib")
    path = write_json(directory, "parsed_quantum_output.json", result)
    version = getattr(cclib, "__version__", None) or module_version("cclib")
    kwargs = {
        "artifact_files": [
            {
                "path": relative_workspace_path(path),
                "semantic_type": "ParsedQuantumChemistryResult",
                "media_type": "application/json",
            }
        ],
        "backend_version": version,
        "warnings": [
            *parser_warnings,
            *(
                [f"Requested property groups not present in this output: {', '.join(missing_groups)}"]
                if missing_groups else []
            ),
        ],
    }
    return partial_success(result, **kwargs) if missing_groups else success(result, **kwargs)


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "qcelemental" and action_id == "normalize_qcschema_molecule":
        return _normalize_qcschema_molecule(request)
    if backend_id == "qcelemental" and action_id == "validate_qcschema_record":
        return _validate_qcschema_record(request)
    if backend_id == "cclib" and action_id == "parse_quantum_chemistry_output":
        return _parse_quantum_output(request)
    return unsupported(f"Unsupported interchange action/backend combination: {action_id}/{backend_id}")

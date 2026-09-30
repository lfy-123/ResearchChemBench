"""Scientific schema normalization and existing-output parsing actions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .quantum_reader import read_quantum_output as _read_quantum_output

from .common import (
    atoms_and_coordinates,
    failed,
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
        "metadata", "charge", "mult", "natom", "nbasis", "nmo", "coreelectrons", "optdone", "optstatus",
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

    version = getattr(cclib, "__version__", None) or module_version("cclib")
    parsed, parse_details = _read_quantum_output(source)
    if parsed is None:
        error = parse_details["error"]
        message = (
            f"cclib {version} could not parse {error['source_path']} "
            f"at line {error['line_number']} ({error['section']}): "
            f"{error['exception_type']}: {error['reason']}"
        )
        response = failed(message, code="output_parse_failed")
        response["error"].update(error, parser_version=version,
            evidence=[{"path": error["source_path"], "line_number": error["line_number"]}])
        response["backend_version"] = version
        return response
    parser_warnings = [
        f"{item['message']} (line {item['line_number']}; occurrences: {item['occurrences']})"
        for item in parse_details["diagnostics"]
    ]
    if parse_details["source_termination"] != "normal":
        parser_warnings.append(
            "Normal termination was not confirmed in the source output. Values can come from earlier completed steps; inspect property_sources before combining energies, geometries and frequencies."
        )
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
    incomplete = set(parse_details["incomplete_properties"])
    incomplete_groups = [group for group in groups
                         if "all" in incomplete or incomplete.intersection(_CCLIB_GROUPS[group])]
    metadata = dict(attributes.get("metadata") or {})
    result = {
        "parser": metadata.get("package") or parsed.__class__.__module__.split(".")[-1],
        "parser_class": parse_details["parser_class"],
        "source_path": relative_workspace_path(source),
        "requested_property_groups": groups,
        "missing_property_groups": missing_groups,
        "incomplete_property_groups": incomplete_groups,
        "source_termination": parse_details["source_termination"],
        "parse_diagnostics": parse_details["diagnostics"],
        "property_sources": {name: location for name, location in parse_details["property_sources"].items() if name in selected},
        "coordinate_frames": coordinate_frames,
        "properties": selected,
        "attribute_units": {
            name: unit for name, unit in _CCLIB_UNITS.items() if name in selected
        },
        "scalar_element_count": element_count,
    }
    directory = output_directory("parse_quantum_chemistry_output", "cclib")
    path = write_json(directory, "parsed_quantum_output.json", result)
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
    incomplete_output = missing_groups or incomplete_groups or parse_details["source_termination"] != "normal"
    return partial_success(result, **kwargs) if incomplete_output else success(result, **kwargs)


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if backend_id == "qcelemental" and action_id == "normalize_qcschema_molecule":
        return _normalize_qcschema_molecule(request)
    if backend_id == "qcelemental" and action_id == "validate_qcschema_record":
        return _validate_qcschema_record(request)
    if backend_id == "cclib" and action_id == "parse_quantum_chemistry_output":
        return _parse_quantum_output(request)
    return unsupported(f"Unsupported interchange action/backend combination: {action_id}/{backend_id}")

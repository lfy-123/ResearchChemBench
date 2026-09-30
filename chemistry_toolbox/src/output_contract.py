"""Read-only validation of the public submission contract and its outputs."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path, PurePosixPath

import jsonschema
from referencing.exceptions import Unresolvable


def _invalid_number(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def _finite_float(value):
    result = float(value)
    return result if math.isfinite(result) else _invalid_number(value)


def strict_json(payload):
    return json.loads(payload, parse_constant=_invalid_number, parse_float=_finite_float)


def public_path(workspace: Path, name: str) -> Path:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts:
        raise ValueError("Contract paths must be relative and remain inside the workspace")
    root = workspace.resolve()
    target = root
    for part in path.parts:
        target = target / part
        if target.is_symlink():
            raise ValueError("Contract paths must not traverse symlinks")
    target.resolve().relative_to(root)
    return target


def _external_refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"$ref", "$dynamicRef", "$recursiveRef"} and isinstance(child, str) and not child.startswith("#"):
                yield child
            yield from _external_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _external_refs(child)


def _pointer(parts):
    return "".join("/" + str(part).replace("~", "~0").replace("/", "~1") for part in parts)


def validate_output_contract(workspace: Path, contract_bytes: bytes | None, *, max_errors: int = 100) -> dict:
    """No hidden references, model calls, output mutation or scientific checks."""
    errors, checked_files = [], []
    error_count = 0
    def add(code, file, message, **details):
        nonlocal error_count
        error_count += 1
        if len(errors) < max_errors:
            errors.append({"code": code, "file": file, "message": str(message)[:2000], **details})
    result = {"applicable": contract_bytes is not None,
              "contract_sha256": hashlib.sha256(contract_bytes).hexdigest() if contract_bytes is not None else None,
              "checked_files": checked_files, "errors": errors,
              "validation_boundary": "Public output format only; scientific correctness is evaluated separately."}
    def finish():
        return {**result, "valid": error_count == 0, "status": "success" if error_count == 0 else "invalid_request",
                "error_count": error_count, "errors_truncated": error_count > len(errors)}
    if contract_bytes is None:
        return finish()
    try:
        contract = strict_json(contract_bytes)
        if not isinstance(contract, dict):
            raise ValueError("Public contract must be a JSON object")
        required = contract.get("required_files", [])
        if not isinstance(required, list):
            raise ValueError("required_files must be an array")
        report = contract.get("report_file")
        if report is not None and not isinstance(report, str):
            raise ValueError("report_file must be a relative path")
        required = list(required)
        if report and report not in [v if isinstance(v, str) else v.get("path") for v in required if isinstance(v, (str, dict))]:
            required.append(report)
        for specification in required:
            if isinstance(specification, str):
                name, allow_empty = specification, False
            elif isinstance(specification, dict) and isinstance(specification.get("path"), str):
                name, allow_empty = specification["path"], specification.get("allow_empty", False)
            else:
                raise ValueError("Each required file must be a path or an object with path")
            if not isinstance(allow_empty, bool):
                raise ValueError("allow_empty must be a boolean")
            try:
                target = public_path(workspace, name)
                exists = target.is_file() or target.is_dir()
                size = target.stat().st_size if target.is_file() else None
                nonempty = (size != 0) if target.is_file() else any(target.iterdir()) if target.is_dir() else False
                if name == report:
                    exists = target.is_file()
                    nonempty = exists and bool(target.read_text(errors="replace").strip())
                    allow_empty = False
                checked_files.append({"file": name, "path": name, "exists": exists, "size_bytes": size,
                                      "kind": "directory" if target.is_dir() else "file",
                                      "allow_empty": allow_empty, "satisfied": exists and (allow_empty or nonempty)})
                if not exists:
                    add("missing_required_file", name, "Required file does not exist")
                elif not allow_empty and not nonempty:
                    add("empty_required_file", name, "Required file is empty")
            except (OSError, ValueError) as exc:
                add("invalid_output_path", name, exc)
        primary = contract.get("primary_result_file")
        schema = contract.get("result_schema")
        if primary is not None:
            if not isinstance(primary, str):
                raise ValueError("primary_result_file must be a relative path")
            try:
                target = public_path(workspace, primary)
                document = strict_json(target.read_bytes())
            except json.JSONDecodeError as exc:
                add("invalid_json", primary, exc.msg, line=exc.lineno, column=exc.colno)
                return finish()
            except (OSError, ValueError) as exc:
                add("invalid_primary_result", primary, exc)
                return finish()
            if schema is not None:
                references = list(_external_refs(schema))
                if references:
                    add("unsupported_contract_reference", "submission_schema.json", "Only references within this public schema are allowed", references=references)
                    return finish()
                validator = jsonschema.validators.validator_for(schema)
                validator.check_schema(schema)
                def record(error):
                    add("schema_validation", primary, error.message,
                        instance_path=_pointer(error.absolute_path), json_path=error.json_path,
                        schema_path=_pointer(error.absolute_schema_path), keyword=error.validator)
                    for child in error.context:
                        record(child)
                for error in validator(schema).iter_errors(document):
                    record(error)
        elif schema is not None:
            add("invalid_contract", "submission_schema.json", "result_schema requires primary_result_file")
    except (ValueError, OSError, jsonschema.SchemaError) as exc:
        add("invalid_contract", "submission_schema.json", exc)
    except Unresolvable as exc:
        add("invalid_contract_reference", "submission_schema.json", exc)
    return finish()


def validate_workspace_output_contract(workspace: Path, *, max_errors: int = 100) -> dict:
    try:
        path = public_path(workspace, "submission_schema.json")
        payload = path.read_bytes() if path.exists() else None
    except (OSError, ValueError) as exc:
        return {"status": "invalid_request", "valid": False, "applicable": True,
                "contract_sha256": None, "errors": [{"code": "unreadable_contract", "file": "submission_schema.json", "message": str(exc)}],
                "error_count": 1, "errors_truncated": False}
    return validate_output_contract(workspace, payload, max_errors=max_errors)

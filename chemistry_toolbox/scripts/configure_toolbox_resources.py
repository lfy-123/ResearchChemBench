#!/usr/bin/env python3
"""Install and deeply verify operator-provided scientific data and binaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.resources import load_resource_config, resource_snapshot


STATUS_PATH = TOOLBOX_ROOT / "config" / "toolbox_resource_status.json"


def declared_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def install_target_path(value: str) -> Path:
    """Return a lexical absolute target without following an existing symlink."""

    path = Path(value).expanduser()
    return Path(os.path.abspath(path if path.is_absolute() else ROOT / path))


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def lexical_relative(path: Path) -> str:
    absolute = Path(os.path.abspath(path))
    try:
        return absolute.relative_to(ROOT).as_posix()
    except ValueError:
        return str(absolute)


def file_checksum(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_supporting_file(
    specification: dict[str, Any], key: str
) -> tuple[dict[str, Any] | None, list[str]]:
    record = specification.get(key)
    if not record:
        return None, []
    path = declared_path(str(record["path"]))
    result: dict[str, Any] = {
        "path": relative(path),
        "exists": path.is_file(),
        "algorithm": str(record["checksum_algorithm"]),
        "expected_checksum": str(record["checksum"]),
    }
    errors = []
    if not path.is_file():
        result["checksum_ok"] = False
        errors.append(f"Missing {key}: {path}")
        return result, errors
    actual = file_checksum(path, str(record["checksum_algorithm"]))
    result["actual_checksum"] = actual
    result["checksum_ok"] = actual.lower() == str(record["checksum"]).lower()
    if not result["checksum_ok"]:
        errors.append(f"{key} checksum mismatch: {path}")
    return result, errors


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with tarfile.open(archive, "r:*") as handle:
        members = handle.getmembers()
        for member in members:
            candidate = (root / member.name).resolve()
            try:
                candidate.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"Archive member escapes extraction root: {member.name}") from exc
            if member.issym() or member.islnk():
                raise ValueError(f"Archive links are not accepted: {member.name}")
        handle.extractall(root, members=members)


def install_executable(specification: dict[str, Any], *, verify_only: bool) -> dict[str, Any]:
    source = declared_path(str(specification["path"]))
    target = install_target_path(str(specification["install_target"]))
    result: dict[str, Any] = {
        "id": specification["id"],
        "kind": specification["kind"],
        "source": relative(source),
        "install_target": lexical_relative(target),
        "source_exists": source.is_file(),
    }
    if not source.is_file() and not verify_only:
        for value in specification.get("import_sources") or []:
            candidate = declared_path(str(value))
            if candidate.is_file():
                source.parent.mkdir(parents=True, exist_ok=True)
                candidate.replace(source)
                result["imported_from"] = relative(candidate)
                result["source_exists"] = True
                break
    if not source.is_file():
        result.update(status="fail", errors=[f"Missing executable: {source}"])
        return result
    errors = []
    supporting_files = {}
    for key in ("distribution_archive", "source_archive"):
        verification, verification_errors = verify_supporting_file(specification, key)
        if verification is not None:
            supporting_files[key] = verification
        errors.extend(verification_errors)
    if supporting_files:
        result["supporting_files"] = supporting_files
    actual = file_checksum(source, str(specification["checksum_algorithm"]))
    result["checksum"] = {
        "algorithm": specification["checksum_algorithm"],
        "expected": specification["checksum"],
        "actual": actual,
        "ok": actual.lower() == str(specification["checksum"]).lower(),
    }
    if not result["checksum"]["ok"]:
        errors.append("Executable checksum mismatch")
    if not verify_only and not errors:
        source.chmod(source.stat().st_mode | 0o111)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            link = target.readlink()
            lexical_link = Path(
                os.path.abspath(link if link.is_absolute() else target.parent / link)
            )
            if lexical_link != source:
                target.unlink()
        elif target.exists():
            if not target.is_file() or file_checksum(target, "sha256") != file_checksum(source, "sha256"):
                errors.append(f"Refusing to replace unrelated target: {target}")
        if not target.exists() and not target.is_symlink() and not errors:
            target.symlink_to(source)
    result["target_exists"] = target.is_file()
    result["target_is_symlink"] = target.is_symlink()
    if target.is_file() and not errors:
        probe_specification = dict(specification.get("version_probe") or {})
        arguments = [
            str(value)
            for value in probe_specification.get("arguments", ["--version"])
        ]
        accepted_returncodes = {
            int(value)
            for value in probe_specification.get("accepted_returncodes", [0])
        }
        try:
            completed = subprocess.run(
                [str(target), *arguments],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=60,
                check=False,
            )
            output = completed.stdout.strip().splitlines()
            output_pattern = str(probe_specification.get("output_regex") or "")
            match = re.search(output_pattern, completed.stdout) if output_pattern else None
            result["version_probe"] = {
                "arguments": arguments,
                "returncode": completed.returncode,
                "first_line": output[0][:500] if output else "",
                "output_regex": output_pattern or None,
                "matched_text": match.group(0) if match else None,
            }
            if completed.returncode not in accepted_returncodes:
                errors.append("Executable version probe failed")
            if output_pattern and match is None:
                errors.append("Executable version output did not match expected pattern")
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(f"Executable version probe failed: {exc}")
    elif not verify_only:
        errors.append("Configured executable target is missing")
    result["errors"] = errors
    result["status"] = "pass" if not errors else "fail"
    return result


def verify_archive(specification: dict[str, Any], *, verify_only: bool) -> tuple[dict[str, Any] | None, list[str]]:
    archive_spec = specification.get("archive")
    if not archive_spec:
        return None, []
    archive = declared_path(str(archive_spec["path"]))
    result: dict[str, Any] = {
        "path": relative(archive),
        "exists": archive.is_file(),
        "algorithm": archive_spec["checksum_algorithm"],
        "expected_checksum": archive_spec["checksum"],
    }
    errors = []
    if not archive.is_file():
        errors.append(f"Missing archive: {archive}")
        result["checksum_ok"] = False
        return result, errors
    actual = file_checksum(archive, str(archive_spec["checksum_algorithm"]))
    result["actual_checksum"] = actual
    result["checksum_ok"] = actual.lower() == str(archive_spec["checksum"]).lower()
    if not result["checksum_ok"]:
        errors.append(f"Archive checksum mismatch: {archive}")
        return result, errors
    root = declared_path(str(specification["path"]))
    if not root.exists() and not verify_only:
        extract_to = declared_path(str(archive_spec.get("extract_to") or root.parent))
        safe_extract(archive, extract_to)
        result["extracted_to"] = relative(extract_to)
    return result, errors


def manifest_records(specification: dict[str, Any]) -> dict[str, Any]:
    manifest_path = declared_path(str(specification["manifest"]))
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if specification["kind"] == "variant_file_collection":
        records = payload.get("variants") if isinstance(payload, dict) else None
        if not isinstance(records, dict):
            raise ValueError(f"Variant manifest requires a variants object: {manifest_path}")
        return records
    if not isinstance(payload, dict):
        raise ValueError(f"Resource manifest must be an object: {manifest_path}")
    return payload


def data_files(specification: dict[str, Any], root: Path) -> list[Path]:
    if specification["kind"] in {
        "element_file_collection",
        "variant_file_collection",
    }:
        manifest_path = specification.get("manifest")
        if manifest_path:
            manifest = manifest_records(specification)
            default_field = (
                "relative_path"
                if specification["kind"] == "variant_file_collection"
                else "filename"
            )
            field = str(
                specification.get("manifest_filename_field", default_field)
            )
            return [
                root / str(manifest[selection][field])
                for selection in sorted(manifest)
            ]
        if specification["kind"] == "variant_file_collection":
            raise ValueError("Variant file collections require a manifest")
        pattern = str(specification["element_pattern"])
        prefix, suffix = pattern.split("{element}", 1)
        return sorted(root.glob(f"{prefix}*{suffix}"))
    return sorted(root.glob(str(specification.get("file_glob", "*"))))


def verify_data_resource(specification: dict[str, Any], *, verify_only: bool, deep: bool) -> dict[str, Any]:
    root = declared_path(str(specification["path"]))
    archive_result, errors = verify_archive(specification, verify_only=verify_only)
    result: dict[str, Any] = {
        "id": specification["id"],
        "kind": specification["kind"],
        "path": relative(root),
        "archive": archive_result,
        "exists": root.is_dir(),
    }
    if not root.is_dir():
        errors.append(f"Missing resource directory after configuration: {root}")
        result.update(status="fail", errors=errors)
        return result
    try:
        files = data_files(specification, root)
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        errors.append(f"Could not enumerate resource files: {exc}")
        files = []
    result["file_count"] = len(files)
    result["expected_file_count"] = specification.get("expected_file_count")
    result["file_count_ok"] = len(files) == int(specification.get("expected_file_count", len(files)))
    if not result["file_count_ok"]:
        errors.append(
            f"Expected {specification.get('expected_file_count')} files, found {len(files)}"
        )
    missing = [relative(path) for path in files if not path.is_file()]
    result["missing_files"] = missing
    if missing:
        errors.append(f"Missing {len(missing)} declared files")
    if specification.get("manifest"):
        manifest_path = declared_path(str(specification["manifest"]))
        result["manifest"] = relative(manifest_path)
        result["manifest_exists"] = manifest_path.is_file()
        if not manifest_path.is_file():
            errors.append(f"Missing manifest: {manifest_path}")
        elif deep and not missing:
            manifest = manifest_records(specification)
            filename_field = str(
                specification.get(
                    "manifest_filename_field",
                    "relative_path"
                    if specification["kind"] == "variant_file_collection"
                    else "filename",
                )
            )
            checksum_field = str(
                specification.get(
                    "manifest_checksum_field",
                    "sha256"
                    if specification["kind"] == "variant_file_collection"
                    else "md5",
                )
            )
            mismatches = []
            for selection, record in manifest.items():
                path = root / str(record[filename_field])
                if file_checksum(path, checksum_field) != str(record[checksum_field]).lower():
                    mismatches.append(str(selection))
            is_variant = specification["kind"] == "variant_file_collection"
            deep_key = (
                "deep_variant_checksums" if is_variant else "deep_element_checksums"
            )
            mismatch_key = (
                "mismatched_selections" if is_variant else "mismatched_elements"
            )
            result[deep_key] = {
                "checked": len(manifest),
                "algorithm": checksum_field,
                mismatch_key: mismatches,
                "ok": not mismatches,
            }
            if mismatches:
                errors.append(f"Per-selection checksum mismatches: {mismatches}")
    snapshot = next(
        (item for item in resource_snapshot() if item["id"] == specification["id"]),
        {},
    )
    result["elements"] = snapshot.get("elements", [])
    result["element_count"] = snapshot.get("element_count")
    result["variants"] = snapshot.get("variants", [])
    result["variant_count"] = snapshot.get("variant_count")
    result["pair_count"] = snapshot.get("pair_count")
    result["errors"] = errors
    result["status"] = "pass" if not errors else "fail"
    return result


def verify_single_file_resource(specification: dict[str, Any]) -> dict[str, Any]:
    """Verify an Agent-selectable model or other exact scientific input file."""

    path = declared_path(str(specification["path"]))
    errors: list[str] = []
    result: dict[str, Any] = {
        "id": specification["id"],
        "kind": specification["kind"],
        "path": relative(path),
        "exists": path.is_file(),
        "size_bytes": path.stat().st_size if path.is_file() else None,
    }
    if not path.is_file():
        errors.append(f"Missing registered file: {path}")
    algorithm = str(specification.get("checksum_algorithm") or "").strip()
    expected = str(specification.get("checksum") or "").strip()
    if not algorithm or not expected:
        errors.append("Exact file resources require checksum_algorithm and checksum")
    elif path.is_file():
        actual = file_checksum(path, algorithm)
        result["checksum"] = {
            "algorithm": algorithm,
            "expected": expected,
            "actual": actual,
            "ok": actual.lower() == expected.lower(),
        }
        if not result["checksum"]["ok"]:
            errors.append("Registered file checksum mismatch")
    result["errors"] = errors
    result["status"] = "pass" if not errors else "fail"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Do not extract archives or create executable links.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip per-element SSSP content checksums.",
    )
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    config = load_resource_config()
    results = []
    for specification in config["resources"]:
        if specification["kind"] == "backend_executable":
            results.append(install_executable(specification, verify_only=args.verify_only))
        elif specification["kind"] in {"model_checkpoint", "single_file_resource"}:
            results.append(verify_single_file_resource(specification))
        else:
            results.append(
                verify_data_resource(
                    specification,
                    verify_only=args.verify_only,
                    deep=not args.quick,
                )
            )
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "selection_policy": config["selection_policy"],
        "configuration_mode": "verify_only" if args.verify_only else "install_and_verify",
        "deep_checks": not args.quick,
        "summary": {
            "resource_count": len(results),
            "passed": sum(item["status"] == "pass" for item in results),
            "failed": sum(item["status"] != "pass" for item in results),
            "all_ok": all(item["status"] == "pass" for item in results),
        },
        "resources": results,
    }
    if not args.no_write:
        STATUS_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(STATUS_PATH)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0 if payload["summary"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

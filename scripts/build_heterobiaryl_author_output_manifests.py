#!/usr/bin/env python3
"""Build file-level role and pairing manifests for Heterobiaryl/P(V) archives."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any
from zipfile import ZipFile, ZipInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = sorted(
    path
    for path in PROJECT_ROOT.glob(
        "tasks/*/data/benchmark_data/author_output_manifest.json"
    )
    if "Reproduction" in path.parts[-4]
)
_STAGE = re.compile(r"\[(Int-[IVX]+|TS-[IVX]+)")
_PATHWAY = re.compile(r"\](?:\d+\+|\+)?-(.+)$")


def _decoded_member_name(name: str) -> str:
    """Recover UTF-8 names stored in legacy ZIPs without the UTF-8 flag."""

    try:
        return name.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def _file_role(member_name: str) -> str | None:
    if member_name.startswith("__MACOSX/") or "/._" in member_name:
        return None
    if member_name.endswith("/.DS_Store") or member_name.endswith(".DS_Store"):
        return None
    if " freq/" in member_name:
        return "gaussian_frequency"
    if " Def2QZVPP/" in member_name:
        return "gaussian_def2_qzvpp_single_point"
    if " DLPNO/" in member_name:
        return "orca_dlpno_ccsdt_single_point"
    return "unclassified"


def _identity(member_name: str) -> str:
    stem = PurePosixPath(member_name).stem
    for suffix in ("_QZ", "_DLPNO"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem


def _member_record(
    archive: ZipFile,
    info: ZipInfo,
    *,
    state: str,
    archive_path: str,
) -> dict[str, Any] | None:
    member_name = _decoded_member_name(info.filename)
    role = _file_role(member_name)
    if info.is_dir() or role is None:
        return None
    identity = _identity(member_name)
    stage_match = _STAGE.search(identity)
    pathway_match = _PATHWAY.search(identity)
    content = archive.read(info)
    file_id = hashlib.sha256(
        f"{state}\0{identity}\0{role}".encode("utf-8")
    ).hexdigest()[:16]
    return {
        "file_id": file_id,
        "state": state,
        "archive_path": archive_path,
        "archive_member_path": member_name,
        "role": role,
        "structure_identity": identity,
        "stage": stage_match.group(1) if stage_match else None,
        "stationary_point_type": (
            "transition_state"
            if stage_match and stage_match.group(1).startswith("TS-")
            else "minimum"
        ),
        "pathway_label": pathway_match.group(1) if pathway_match else None,
        "size_bytes": info.file_size,
        "crc32": f"{info.CRC:08x}",
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def enrich_manifest(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    files: list[dict[str, Any]] = []
    for archive_record in value.get("archives", []):
        archive_path = str(archive_record["path"])
        archive_file = path.parent / archive_path
        with ZipFile(archive_file) as archive:
            for info in archive.infolist():
                record = _member_record(
                    archive,
                    info,
                    state=str(archive_record["state"]),
                    archive_path=archive_path,
                )
                if record is not None:
                    files.append(record)

    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in files:
        groups.setdefault(
            (record["state"], record["structure_identity"]), []
        ).append(record)
    pairings = []
    required_roles = {
        "gaussian_frequency",
        "gaussian_def2_qzvpp_single_point",
        "orca_dlpno_ccsdt_single_point",
    }
    for (state, identity), records in sorted(groups.items()):
        by_role = {record["role"]: record["file_id"] for record in records}
        pairing_id = hashlib.sha256(
            f"{state}\0{identity}".encode("utf-8")
        ).hexdigest()[:16]
        pairings.append(
            {
                "pairing_id": pairing_id,
                "state": state,
                "structure_identity": identity,
                "stage": records[0]["stage"],
                "stationary_point_type": records[0]["stationary_point_type"],
                "pathway_label": records[0]["pathway_label"],
                "files_by_role": by_role,
                "complete": set(by_role) == required_roles,
            }
        )

    value.update(
        {
            "schema_version": 2,
            "result_values_included": False,
            "file_role_policy": {
                "pairing_key": ["state", "structure_identity"],
                "required_roles": sorted(required_roles),
                "scientific_boundary": (
                    "The manifest identifies matching raw outputs only. It does not include "
                    "energies, barriers, pathway rankings, or paper conclusions."
                ),
            },
            "files": sorted(
                files,
                key=lambda item: (
                    item["state"],
                    item["structure_identity"],
                    item["role"],
                ),
            ),
            "pairings": pairings,
            "summary": {
                "archive_count": len(value.get("archives", [])),
                "file_count": len(files),
                "pairing_count": len(pairings),
                "complete_pairing_count": sum(item["complete"] for item in pairings),
                "unclassified_file_count": sum(
                    item["role"] == "unclassified" for item in files
                ),
            },
        }
    )
    return value


def main() -> int:
    updated = 0
    for path in MANIFESTS:
        value = enrich_manifest(path)
        output_path = path.with_name("author_output_file_roles.json")
        output_path.write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        input_manifest_path = path.with_name("input_manifest.json")
        if input_manifest_path.is_file():
            input_manifest = json.loads(input_manifest_path.read_text(encoding="utf-8"))
            for record in input_manifest.get("files", []):
                if record.get("path") == path.name:
                    record["size_bytes"] = path.stat().st_size
                    record["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            role_record = {
                "path": output_path.name,
                "size_bytes": output_path.stat().st_size,
                "sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
            }
            existing_role = next(
                (
                    record
                    for record in input_manifest.get("files", [])
                    if record.get("path") == output_path.name
                ),
                None,
            )
            if existing_role is None:
                input_manifest.setdefault("files", []).append(role_record)
            else:
                existing_role.update(role_record)
            input_manifest_path.write_text(
                json.dumps(input_manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            truth_path = path.parents[2] / "target_study" / "ground_truth.json"
            if truth_path.is_file():
                truth = json.loads(truth_path.read_text(encoding="utf-8"))
                truth.setdefault("reference_evidence", {})["input_manifest_sha256"] = (
                    hashlib.sha256(input_manifest_path.read_bytes()).hexdigest()
                )
                truth_path.write_text(
                    json.dumps(truth, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
        updated += 1
    print(f"Updated {updated} Heterobiaryl/P(V) author output manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

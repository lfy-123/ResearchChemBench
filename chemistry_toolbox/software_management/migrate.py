"""Non-destructive import of the legacy cache into the managed v2 layout."""

from __future__ import annotations

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .models import MigrationRule, SoftwareManifest
from .paths import within
from .receipts import write_json


def _copy_file(source: str, destination: str) -> str:
    try:
        os.link(source, destination)
        return destination
    except OSError:
        return shutil.copy2(source, destination)


def _copy_path(source: Path, destination: Path, strategy: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        destination.symlink_to(os.readlink(source))
    elif source.is_dir():
        copy_function = _copy_file if strategy == "hardlink" else shutil.copy2
        shutil.copytree(source, destination, symlinks=True, copy_function=copy_function)
    else:
        if strategy == "hardlink":
            _copy_file(str(source), str(destination))
        else:
            shutil.copy2(source, destination)


def _mapped_target(
    target: Path, legacy_root: Path, destination_root: Path, mappings: list[tuple[Path, Path]]
) -> Path | None:
    try:
        relative = target.relative_to(legacy_root)
    except ValueError:
        return None
    for source_prefix, destination_prefix in sorted(
        mappings, key=lambda item: len(item[0].parts), reverse=True
    ):
        try:
            suffix = relative.relative_to(source_prefix)
        except ValueError:
            continue
        return destination_root / destination_prefix / suffix
    return None


def rewrite_internal_absolute_symlinks(
    root: Path, legacy_root: Path, mappings: list[tuple[Path, Path]]
) -> dict[str, Any]:
    rewritten: list[str] = []
    unresolved: list[dict[str, str]] = []
    for link in root.rglob("*"):
        if not link.is_symlink():
            continue
        raw_target = Path(os.readlink(link))
        if not raw_target.is_absolute():
            continue
        mapped = _mapped_target(raw_target, legacy_root, root, mappings)
        if mapped is None:
            unresolved.append({"path": str(link.relative_to(root)), "target": str(raw_target)})
            continue
        relative_target = os.path.relpath(mapped, start=link.parent)
        link.unlink()
        link.symlink_to(relative_target)
        rewritten.append(str(link.relative_to(root)))
    return {"rewritten": rewritten, "unresolved": unresolved}


def migrate_legacy_cache(
    legacy_root: Path,
    destination_root: Path,
    manifests: Iterable[SoftwareManifest],
) -> dict[str, Any]:
    legacy_root = legacy_root.resolve()
    destination_root = destination_root.resolve()
    if legacy_root == destination_root:
        raise ValueError("Legacy and destination cache roots must differ")
    rules: list[tuple[str, MigrationRule]] = [
        (manifest.software_id, rule)
        for manifest in manifests
        for rule in manifest.migration
        if rule.role != "ignore"
    ]
    mappings = [(Path(rule.source), Path(rule.destination)) for _, rule in rules]
    records: list[dict[str, Any]] = []
    destinations: set[Path] = set()
    for software_id, rule in rules:
        source = within(legacy_root, rule.source, field="legacy migration source")
        destination = within(destination_root, rule.destination, field="migration destination")
        if destination in destinations:
            raise ValueError(f"Duplicate migration destination: {rule.destination}")
        destinations.add(destination)
        if not source.exists() and not source.is_symlink():
            if rule.optional:
                records.append(
                    {
                        "software_id": software_id,
                        "source": rule.source,
                        "destination": rule.destination,
                        "role": rule.role,
                        "status": "optional_missing",
                    }
                )
                continue
            raise FileNotFoundError(source)
        if destination.exists() or destination.is_symlink():
            if destination.is_dir() and not destination.is_symlink() and not any(destination.iterdir()):
                destination.rmdir()
            else:
                raise FileExistsError(destination)
        _copy_path(source, destination, rule.strategy)
        records.append(
            {
                "software_id": software_id,
                "source": rule.source,
                "destination": rule.destination,
                "role": rule.role,
                "strategy": rule.strategy,
                "status": "migrated",
            }
        )
    symlinks = rewrite_internal_absolute_symlinks(
        destination_root, legacy_root, mappings
    )
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "legacy_root": str(legacy_root),
        "destination_root": str(destination_root),
        "records": records,
        "symlinks": symlinks,
    }
    write_json(destination_root / "receipts" / "legacy-migration.json", report)
    return report

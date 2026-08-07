"""High-level API for initializing, installing, and verifying software."""

from __future__ import annotations

import fnmatch
import os
import platform
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .checksums import sha256
from .handlers import install_archive, install_commands, install_copy
from .manifests import load_catalog
from .models import SoftwareManifest
from .paths import LAYOUT_DIRECTORIES, cache_root, within
from .receipts import write_json
from .verify import verify_manifest


class SoftwareManager:
    def __init__(self, root: str | Path | None = None, *, catalog_path: str | Path | None = None):
        self.root = cache_root(root)
        self.catalog = load_catalog(catalog_path)

    def initialize(self) -> dict[str, Any]:
        self.root.mkdir(parents=True, exist_ok=True)
        for relative in LAYOUT_DIRECTORIES:
            (self.root / relative).mkdir(exist_ok=True)
        record = {
            "schema_version": 1,
            "layout": list(LAYOUT_DIRECTORIES),
            "platform": platform.platform(),
            "machine": platform.machine(),
        }
        write_json(self.root / ".layout.json", record)
        return record

    def manifest(self, software_id: str) -> SoftwareManifest:
        try:
            return self.catalog[software_id]
        except KeyError as exc:
            raise KeyError(f"Unknown software id: {software_id}") from exc

    def package_directory(self, manifest: SoftwareManifest) -> Path:
        return self.root / "packages" / manifest.software_id / manifest.version

    def packages(self, manifest: SoftwareManifest) -> list[Path]:
        directory = self.package_directory(manifest)
        if not directory.is_dir():
            return []
        return sorted(
            path
            for path in directory.iterdir()
            if not manifest.package_patterns
            or any(fnmatch.fnmatch(path.name, pattern) for pattern in manifest.package_patterns)
        )

    def stage(self, software_id: str, source: str | Path) -> dict[str, Any]:
        manifest = self.manifest(software_id)
        source_path = Path(source).expanduser().resolve()
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        directory = self.package_directory(manifest)
        directory.mkdir(parents=True, exist_ok=True)
        destination = directory / source_path.name
        if destination.exists():
            if source_path.is_file() and destination.is_file() and sha256(source_path) == sha256(destination):
                return {"status": "already_staged", "path": str(destination)}
            raise FileExistsError(destination)
        if source_path.is_dir():
            shutil.copytree(source_path, destination, symlinks=True)
            checksum = None
        else:
            shutil.copy2(source_path, destination)
            checksum = sha256(destination)
        return {"status": "staged", "path": str(destination), "sha256": checksum}

    def status(self, software_id: str | None = None) -> list[dict[str, Any]]:
        manifests = [self.manifest(software_id)] if software_id else self.catalog.values()
        result = []
        for manifest in manifests:
            installation = within(self.root, manifest.installation_path)
            result.append(
                {
                    "software_id": manifest.software_id,
                    "version": manifest.version,
                    "acquisition": manifest.acquisition,
                    "license": manifest.license,
                    "handler": manifest.handler,
                    "packages": [str(path.relative_to(self.root)) for path in self.packages(manifest)],
                    "installed": installation.is_dir(),
                    "installation": str(installation.relative_to(self.root)),
                }
            )
        return result

    def install(self, software_id: str, *, package: str | Path | None = None) -> dict[str, Any]:
        manifest = self.manifest(software_id)
        destination = within(self.root, manifest.installation_path)
        if destination.is_dir():
            verification = verify_manifest(self.root, manifest)
            return {"status": "already_installed", "verification": verification}
        if manifest.handler in {"manual", "external"}:
            raise RuntimeError(
                f"{software_id} uses handler={manifest.handler}; follow its manifest notes"
            )
        package_path = Path(package).expanduser().resolve() if package else None
        if package_path is None:
            candidates = self.packages(manifest)
            if len(candidates) != 1:
                raise RuntimeError(
                    f"Expected exactly one staged package for {software_id}, found {len(candidates)}"
                )
            package_path = candidates[0]
        if not package_path.exists():
            raise FileNotFoundError(package_path)
        if package_path.is_file():
            actual_sha256 = sha256(package_path)
            expected = manifest.package_sha256.get(package_path.name)
            if expected and actual_sha256.lower() != expected.lower():
                raise ValueError(f"Package checksum mismatch: {package_path}")
        else:
            actual_sha256 = None
        staging = self.root / "staging" / f"{software_id}-{uuid.uuid4().hex}"
        staging.mkdir(parents=True)
        staged_root = staging / "root"
        staged_installation = within(
            staged_root, manifest.installation_path, field="staged installation target"
        )
        install_options = dict(manifest.install_options)
        executable_paths = {
            str(path) for path in install_options.get("executable_paths", []) or []
        }
        executable_paths.update(manifest.entrypoints.values())
        install_options["executable_paths"] = sorted(executable_paths)
        try:
            if manifest.handler == "archive":
                install_archive(package_path, staged_installation, install_options)
            elif manifest.handler == "copy":
                install_copy(package_path, staged_installation, install_options)
            elif manifest.handler == "commands":
                staged_installation.mkdir()
                install_commands(package_path, staged_installation, install_options)
            else:
                raise RuntimeError(f"Unsupported handler: {manifest.handler}")
            verification = verify_manifest(staged_root, manifest)
            if verification["status"] != "pass":
                errors = "; ".join(verification["errors"])
                raise RuntimeError(f"Installation verification failed for {software_id}: {errors}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            staged_installation.replace(destination)
        finally:
            shutil.rmtree(staging, ignore_errors=True)
        receipt = {
            "schema_version": 1,
            "software_id": software_id,
            "version": manifest.version,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "package": str(package_path),
            "package_sha256": actual_sha256,
            "handler": manifest.handler,
            "installation": manifest.installation_path,
            "verification": verification,
        }
        write_json(self.root / "receipts" / software_id / f"{manifest.version}.json", receipt)
        return {"status": "installed", **receipt}

    def verify(self, software_id: str | None = None) -> list[dict[str, Any]]:
        manifests = [self.manifest(software_id)] if software_id else self.catalog.values()
        return [verify_manifest(self.root, manifest) for manifest in manifests]

"""Validated data models for software acquisition and installation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .paths import safe_relative_path


VALID_ACQUISITION = {"automatic", "manual", "bundled", "unavailable"}
VALID_HANDLERS = {"archive", "copy", "commands", "external", "manual"}
VALID_MIGRATION_ROLES = {
    "installation",
    "package",
    "source",
    "shared",
    "state",
    "validation",
    "build",
    "documentation",
    "ignore",
}


@dataclass(frozen=True)
class MigrationRule:
    source: str
    destination: str
    role: str
    optional: bool = False
    strategy: str = "hardlink"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "MigrationRule":
        source = str(value["source"])
        destination = str(value.get("destination") or "")
        role = str(value["role"])
        safe_relative_path(source, field="migration source")
        if role != "ignore":
            safe_relative_path(destination, field="migration destination")
        if role not in VALID_MIGRATION_ROLES:
            raise ValueError(f"Unsupported migration role: {role}")
        strategy = str(value.get("strategy") or "hardlink")
        if strategy not in {"hardlink", "copy"}:
            raise ValueError(f"Unsupported migration strategy: {strategy}")
        return cls(
            source=source,
            destination=destination,
            role=role,
            optional=bool(value.get("optional", False)),
            strategy=strategy,
        )


@dataclass(frozen=True)
class SoftwareManifest:
    software_id: str
    display_name: str
    version: str
    acquisition: str
    license: str
    handler: str
    installation_path: str
    installation_required: bool = True
    package_patterns: tuple[str, ...] = ()
    package_sha256: dict[str, str] = field(default_factory=dict)
    entrypoints: dict[str, str] = field(default_factory=dict)
    dependencies: tuple[str, ...] = ()
    install_options: dict[str, Any] = field(default_factory=dict)
    verification: tuple[dict[str, Any], ...] = ()
    migration: tuple[MigrationRule, ...] = ()
    notes: str = ""

    @classmethod
    def from_dict(cls, software_id: str, value: dict[str, Any]) -> "SoftwareManifest":
        if not software_id or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for character in software_id):
            raise ValueError(f"Invalid software id: {software_id!r}")
        acquisition = str(value.get("acquisition") or "manual")
        handler = str((value.get("installation") or {}).get("handler") or "manual")
        if acquisition not in VALID_ACQUISITION:
            raise ValueError(f"Unsupported acquisition policy for {software_id}: {acquisition}")
        if handler not in VALID_HANDLERS:
            raise ValueError(f"Unsupported installation handler for {software_id}: {handler}")
        version = str(value.get("version") or "unknown")
        installation = dict(value.get("installation") or {})
        installation_path = str(
            installation.get("target")
            or f"installations/{software_id}/{version}/linux-x86_64"
        )
        safe_relative_path(installation_path, field=f"{software_id} installation target")
        entrypoints = {
            str(name): str(path)
            for name, path in dict((value.get("runtime") or {}).get("entrypoints") or {}).items()
        }
        for path in entrypoints.values():
            safe_relative_path(path, field=f"{software_id} entrypoint")
        patterns = tuple(str(item) for item in value.get("accepted_packages") or ())
        if any(Path(pattern).is_absolute() or ".." in Path(pattern).parts for pattern in patterns):
            raise ValueError(f"Invalid package pattern for {software_id}")
        install_options = {
            key: item
            for key, item in installation.items()
            if key not in {"handler", "target"}
        }
        for path in install_options.get("executable_paths", []) or []:
            safe_relative_path(path, field=f"{software_id} executable path")
        for link, target in dict(install_options.get("aliases") or {}).items():
            safe_relative_path(link, field=f"{software_id} alias path")
            safe_relative_path(target, field=f"{software_id} alias target")
        return cls(
            software_id=software_id,
            display_name=str(value.get("display_name") or software_id),
            version=version,
            acquisition=acquisition,
            license=str(value.get("license") or "unknown"),
            handler=handler,
            installation_path=installation_path,
            installation_required=bool(installation.get("required", True)),
            package_patterns=patterns,
            package_sha256={str(key): str(item) for key, item in dict(value.get("package_sha256") or {}).items()},
            entrypoints=entrypoints,
            dependencies=tuple(str(item) for item in value.get("dependencies") or ()),
            install_options=install_options,
            verification=tuple(dict(item) for item in value.get("verification") or ()),
            migration=tuple(MigrationRule.from_dict(dict(item)) for item in value.get("migration") or ()),
            notes=str(value.get("notes") or ""),
        )

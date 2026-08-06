"""Deterministic classification of legacy cache paths into the v2 layout."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .paths import LAYOUT_DIRECTORIES, safe_relative_path


DEFAULT_LAYOUT_PATH = Path(__file__).with_name("legacy_layout.yaml")
ARCHIVE_SUFFIXES = (
    ".tar",
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
    ".tgz",
    ".tbz2",
    ".zip",
    ".deb",
    ".rpm",
    ".whl",
    ".pkg.tar.zst",
)


@lru_cache(maxsize=4)
def load_legacy_layout(path: str | Path = DEFAULT_LAYOUT_PATH) -> dict[str, Any]:
    value = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if value.get("schema_version") != 1:
        raise ValueError(f"Invalid legacy layout: {path}")
    return value


def _has_prefix(path: PurePosixPath, prefix: str) -> bool:
    parts = PurePosixPath(prefix).parts
    return path.parts[: len(parts)] == parts


def _matches_marker(component: str, marker: str) -> bool:
    """Match exact legacy role directories and their version/suffix variants."""

    return (
        component == marker
        or component.startswith(f"{marker}-")
        or (marker == "smoke" and component.startswith("smoke_"))
    )


def classify_legacy_path(
    value: str | Path, *, layout: dict[str, Any] | None = None
) -> Path | None:
    relative = safe_relative_path(value, field="legacy path")
    path = PurePosixPath(relative.as_posix())
    if not path.parts:
        raise ValueError("Legacy path must not be empty")
    config = layout or load_legacy_layout()
    root = path.parts[0]
    if root in set(config.get("ignored_roots") or ()):
        return None
    if any(_has_prefix(path, str(prefix)) for prefix in config.get("ignored_paths") or ()):
        return None

    root_destinations = dict(config.get("root_destinations") or {})
    if root in root_destinations:
        suffix = Path(*path.parts[1:])
        return Path(str(root_destinations[root])) / suffix

    for prefix, destination in dict(config.get("shared_overrides") or {}).items():
        if _has_prefix(path, str(prefix)):
            suffix = Path(*path.parts[len(PurePosixPath(prefix).parts) :])
            return Path(str(destination)) / suffix
    for prefix, destination in dict(config.get("state_overrides") or {}).items():
        if _has_prefix(path, str(prefix)):
            suffix = Path(*path.parts[len(PurePosixPath(prefix).parts) :])
            return Path(str(destination)) / suffix
    for prefix, destination in dict(config.get("validation_overrides") or {}).items():
        if _has_prefix(path, str(prefix)):
            suffix = Path(*path.parts[len(PurePosixPath(prefix).parts) :])
            return Path(str(destination)) / suffix
    if any(_has_prefix(path, str(prefix)) for prefix in config.get("runtime_source_overrides") or ()):
        return Path("installations") / path

    markers = {
        role: tuple(str(item) for item in values or ())
        for role, values in dict(config.get("role_markers") or {}).items()
    }
    # Legacy role directories occur directly below a software root or one
    # version directory. Deeper names such as pip/_internal/operations/build
    # are runtime content and must remain inside their installation.
    components = path.parts[1:3]
    destination_role = "installation"
    for role in ("package", "state", "validation", "build", "source"):
        if any(
            _matches_marker(component, marker)
            for component in components
            for marker in markers.get(role, ())
        ):
            destination_role = role
            break
    if path.name.lower().endswith(ARCHIVE_SUFFIXES):
        destination_role = "package"
    directory = {
        "installation": "installations",
        "package": "packages",
        "source": "sources",
        "build": "build",
        "state": "state",
        "validation": "validation",
    }[destination_role]
    return Path(directory) / path


def translate_project_cache_path(
    value: str, *, old_root: str = ".software_cache", new_root: str = ".software_cache"
) -> str:
    prefix = f"{old_root.rstrip('/')}/"
    if not value.startswith(prefix):
        return value
    relative = Path(value[len(prefix) :])
    if relative.parts and relative.parts[0] in set(LAYOUT_DIRECTORIES):
        classified = relative
    else:
        classified = classify_legacy_path(relative)
    if classified is None:
        raise ValueError(f"Path belongs to an ignored legacy cache root: {value}")
    translated = f"{new_root.rstrip('/')}/{classified.as_posix()}"
    return f"{translated}/" if value.endswith("/") else translated

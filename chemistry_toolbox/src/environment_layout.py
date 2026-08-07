"""Resolve chemistry-toolbox runtime prefixes under the project ``.envs`` root.

The public runtime identifiers (``quantum``, ``md``, ``cp2k`` and so on) stay
stable while every configured runtime points to one consolidated Conda
prefixes. There is no alternate environment layout or path fallback.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from .paths import PROJECT_ROOT, TOOLBOX_ROOT


ENV_ROOT_ENV = "RESEARCHCHEMBENCH_ENV_ROOT"
SOFTWARE_ROOT_ENV = "RESEARCHCHEMBENCH_SOFTWARE_ROOT"
ENVIRONMENT_CONFIG_PATH = TOOLBOX_ROOT / "environment" / "environments.yaml"
V2_SOFTWARE_DIRECTORIES = {
    "documentation",
    "installations",
    "packages",
    "sources",
    "shared",
    "state",
    "build",
    "staging",
    "validation",
    "receipts",
}


@lru_cache(maxsize=1)
def load_environment_config() -> dict[str, Any]:
    value = yaml.safe_load(ENVIRONMENT_CONFIG_PATH.read_text(encoding="utf-8")) or {}
    environments = value.get("environments")
    runtime_mapping = value.get("runtime_mapping")
    if not isinstance(environments, dict) or not isinstance(runtime_mapping, dict):
        raise ValueError(f"Invalid environment configuration: {ENVIRONMENT_CONFIG_PATH}")
    return value


@lru_cache(maxsize=1)
def _runtime_to_group() -> dict[str, str]:
    config = load_environment_config()
    result: dict[str, str] = {}
    for group, runtimes in config["runtime_mapping"].items():
        if group not in config["environments"]:
            raise ValueError(f"Unknown environment group {group!r}")
        for runtime in runtimes or []:
            runtime_name = str(runtime)
            if runtime_name in result:
                raise ValueError(f"Runtime {runtime_name!r} is assigned twice")
            result[runtime_name] = str(group)
    return result


def environment_path(runtime: str) -> Path | None:
    group = _runtime_to_group().get(runtime)
    if group is None:
        return None
    return _group_path(group)


def _environment_root_override() -> Path | None:
    value = os.environ.get(ENV_ROOT_ENV, "").strip()
    if not value:
        return None
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def software_root() -> Path:
    """Return the relocatable native-software cache root."""

    value = os.environ.get(SOFTWARE_ROOT_ENV, "").strip()
    path = Path(value).expanduser() if value else PROJECT_ROOT / ".software_cache"
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def _resolve_software_path(path: Path) -> Path:
    root = software_root()
    relative = Path(*path.parts[1:])
    if not relative.parts or relative.parts[0] in V2_SOFTWARE_DIRECTORIES:
        return (root / relative).resolve()
    if (root / ".layout.json").is_file():
        # Import lazily so the core environment module remains usable by itself.
        from chemistry_toolbox.software_management.legacy_layout import classify_legacy_path

        migrated = classify_legacy_path(relative)
        if migrated is None:
            raise ValueError(f"Configured path belongs to an excluded legacy cache entry: {path}")
        relative = migrated
    return (root / relative).resolve()


def _group_path(group: str) -> Path:
    configured = Path(str(load_environment_config()["environments"][group]["path"]))
    if override := _environment_root_override():
        return (override / configured.name).resolve()
    return configured.resolve() if configured.is_absolute() else (PROJECT_ROOT / configured).resolve()


def _project_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def resolve_runtime_path(runtime: str, configured_value: str | Path) -> Path:
    """Resolve a logical runtime to its consolidated physical prefix."""

    configured = environment_path(runtime)
    return configured if configured is not None else _project_path(configured_value)


def resolve_configured_path(value: str | Path) -> Path:
    """Resolve configured project paths under relocatable environment/cache roots."""

    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    if path.parts[:1] == (".envs",) and (override := _environment_root_override()):
        return override.joinpath(*path.parts[1:]).resolve()
    if path.parts[:1] == (".software_cache",):
        return _resolve_software_path(path)
    return (PROJECT_ROOT / path).resolve()

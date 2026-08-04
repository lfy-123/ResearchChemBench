"""Resolve MiniChem logical runtimes to its portable physical prefix."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from .paths import CONFIG_ROOT, PROJECT_ROOT


ENV_ROOT_ENV = "MINICHEM_ENV_ROOT"
ENVIRONMENT_CONFIG_PATH = CONFIG_ROOT / "merged_environments.yaml"


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
    """Resolve a configured path, including a relocated MiniChem runtime root."""

    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    if path.parts[:2] == (".mini_software_cache", "runtimes") and (
        override := _environment_root_override()
    ):
        return override.joinpath(*path.parts[2:]).resolve()
    return (PROJECT_ROOT / path).resolve()

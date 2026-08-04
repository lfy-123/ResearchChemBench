"""Resolve MiniChem paths relative to the toolbox root."""

from __future__ import annotations

import os
from pathlib import Path

from .paths import PROJECT_ROOT


ENV_ROOT_ENV = "MINICHEM_ENV_ROOT"


def environment_path(runtime: str) -> Path:
    del runtime
    root = _environment_root_override() or (PROJECT_ROOT / ".envs")
    return (root / "minichem").resolve()


def _environment_root_override() -> Path | None:
    value = os.environ.get(ENV_ROOT_ENV, "").strip()
    if not value:
        return None
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def resolve_runtime_path(runtime: str, configured_value: str | Path) -> Path:
    """Resolve a logical runtime to its consolidated physical prefix."""

    del configured_value
    return environment_path(runtime)


def resolve_configured_path(value: str | Path) -> Path:
    """Resolve a configured path, including a relocated MiniChem runtime root."""

    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (PROJECT_ROOT / path).resolve()

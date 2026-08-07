"""Path policy for the managed software cache."""

from __future__ import annotations

import os
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
CACHE_ROOT_ENV = "RESEARCHCHEMBENCH_SOFTWARE_ROOT"
LAYOUT_DIRECTORIES = (
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
)


def cache_root(value: str | Path | None = None) -> Path:
    configured = value if value is not None else os.environ.get(CACHE_ROOT_ENV)
    path = Path(configured).expanduser() if configured else PROJECT_ROOT / ".software_cache"
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def safe_relative_path(value: str | Path, *, field: str = "path") -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must be a cache-relative path: {value}")
    return path


def within(root: Path, value: str | Path, *, field: str = "path") -> Path:
    relative = safe_relative_path(value, field=field)
    result = (root / relative).resolve(strict=False)
    try:
        result.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{field} escapes cache root: {value}") from exc
    return result

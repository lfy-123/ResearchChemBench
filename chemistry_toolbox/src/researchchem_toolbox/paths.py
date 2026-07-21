"""Canonical project and chemistry-toolbox path discovery."""

from __future__ import annotations

import os
from pathlib import Path


CORE_PACKAGE_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = CORE_PACKAGE_ROOT.parent
TOOLBOX_ROOT = SOURCE_ROOT.parent


def _configured_path(variable: str) -> Path | None:
    value = os.environ.get(variable, "").strip()
    return Path(value).expanduser().resolve() if value else None


PROJECT_ROOT = _configured_path("RESEARCHCHEMBENCH_ROOT") or TOOLBOX_ROOT.parent
CONFIG_ROOT = (
    _configured_path("RESEARCHCHEM_TOOLBOX_CONFIG_ROOT") or TOOLBOX_ROOT / "config"
)
SCRIPTS_ROOT = TOOLBOX_ROOT / "scripts"
TESTS_ROOT = TOOLBOX_ROOT / "tests"
DOCS_ROOT = TOOLBOX_ROOT / "docs"


def project_path(*parts: str) -> Path:
    """Return a path relative to the benchmark repository root."""

    return PROJECT_ROOT.joinpath(*parts)


def toolbox_path(*parts: str) -> Path:
    """Return a path relative to the canonical chemistry-toolbox root."""

    return TOOLBOX_ROOT.joinpath(*parts)

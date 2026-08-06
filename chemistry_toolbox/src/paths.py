"""Canonical project and chemistry-toolbox path discovery."""

from __future__ import annotations

import os
import re
import socket
from pathlib import Path
from typing import Any


CORE_PACKAGE_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = CORE_PACKAGE_ROOT
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
EVIDENCE_STATUS_ROOT = TOOLBOX_ROOT / "evidence" / "status"


def project_path(*parts: str) -> Path:
    """Return a path relative to the benchmark repository root."""

    return PROJECT_ROOT.joinpath(*parts)


def toolbox_path(*parts: str) -> Path:
    """Return a path relative to the canonical chemistry-toolbox root."""

    return TOOLBOX_ROOT.joinpath(*parts)


def portable_report_value(value: Any) -> Any:
    """Replace repository-local absolute paths in persisted reports."""

    if isinstance(value, dict):
        return {key: portable_report_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [portable_report_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(portable_report_value(item) for item in value)
    if not isinstance(value, str):
        return value
    return portable_report_text(value)


def portable_report_text(value: str) -> str:
    """Remove host-specific project, storage, and hostname values from text."""

    root = str(PROJECT_ROOT.resolve())
    if value == root:
        return "."
    text = value.replace(root + os.sep, "")
    hostname = socket.gethostname().strip()
    if hostname:
        text = text.replace(hostname, "<host>")
    text = re.sub(r"/inspire/hdd/global_user/[^/\s\"']+", "<storage-root>", text)
    return "\n".join(line.rstrip() for line in text.split("\n"))

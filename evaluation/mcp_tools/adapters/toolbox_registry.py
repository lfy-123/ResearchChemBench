"""Read and summarize the machine-readable software registry."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def registry_path() -> Path:
    configured = os.environ.get("RESEARCHCHEM_TOOLBOX_REGISTRY", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    return PROJECT_ROOT / "config" / "toolbox_registry.yaml"


def load_registry() -> dict[str, Any]:
    path = registry_path()
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict) or not isinstance(value.get("software"), list):
        raise ValueError(f"Invalid toolbox registry: {path}")
    return value


def software_entries() -> list[dict[str, Any]]:
    entries = load_registry()["software"]
    return [dict(entry) for entry in entries]


def software_entry(name: str) -> dict[str, Any] | None:
    normalized = name.strip().lower()
    for entry in software_entries():
        if str(entry.get("name", "")).lower() == normalized:
            return entry
    return None

"""Compatibility view over the canonical BackendSpec catalog."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from researchchem_toolbox.catalog import backend_specs
from researchchem_toolbox.paths import CONFIG_ROOT


def registry_path() -> Path:
    configured = os.environ.get("RESEARCHCHEM_TOOLBOX_REGISTRY", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    return CONFIG_ROOT / "toolbox_registry.yaml"


def load_registry() -> dict[str, Any]:
    path = registry_path()
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"Invalid toolbox registry: {path}")
    if isinstance(value.get("software"), list):
        # Explicit override files may still provide a self-contained snapshot.
        return value
    if value.get("source_module") != "researchchem_toolbox.specs":
        raise ValueError(f"Invalid dynamic toolbox registry manifest: {path}")
    value["software"] = [
        {
            "name": specification.id,
            "display_name": specification.display_name,
            "runtime": specification.runtime,
            "capabilities": list(specification.capabilities),
            "description": specification.description,
            "python_modules": list(specification.python_modules),
            "executables": list(specification.executables),
            "environment_variables": list(specification.environment_variables),
            "conda_packages": list(specification.conda_packages),
            "pip_packages": list(specification.pip_packages),
            "required_data_resources": list(specification.required_data_resources),
            "license_class": specification.license_class,
            "install_notes": specification.install_notes,
        }
        for specification in backend_specs().values()
    ]
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

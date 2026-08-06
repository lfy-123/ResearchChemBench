"""Load and validate the version-controlled software catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import SoftwareManifest


DEFAULT_CATALOG_PATH = Path(__file__).resolve().parent / "manifests" / "catalog.yaml"


def load_catalog(path: str | Path | None = None) -> dict[str, SoftwareManifest]:
    catalog_path = Path(path) if path is not None else DEFAULT_CATALOG_PATH
    value: dict[str, Any] = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    if value.get("schema_version") != 1 or not isinstance(value.get("software"), dict):
        raise ValueError(f"Invalid software catalog: {catalog_path}")
    result = {
        str(software_id): SoftwareManifest.from_dict(str(software_id), dict(item or {}))
        for software_id, item in value["software"].items()
    }
    if len(result) != len(value["software"]):
        raise ValueError(f"Duplicate software ids in catalog: {catalog_path}")
    return result

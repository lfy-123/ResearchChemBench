"""Helpers for the current split evaluator representation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.stages.phase_gate import EVALUATION_FILES, is_blocking_finding


def read_mode_reference(root: str | Path, mode: str) -> dict[str, dict[str, Any]] | None:
    directory = Path(root) / "evaluator_reference" / mode
    if not directory.is_dir():
        return None
    values: dict[str, dict[str, Any]] = {}
    for name in EVALUATION_FILES:
        path = directory / name
        if not path.is_file():
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            return None
        values[name] = value
    return values


def read_split_reference(root: str | Path) -> dict[str, dict[str, dict[str, Any]]] | None:
    values = {
        mode: read_mode_reference(root, mode)
        for mode in ("autonomous_research", "paper_reproduction")
    }
    return values if all(values.values()) else None


__all__ = ["is_blocking_finding", "read_mode_reference", "read_split_reference"]

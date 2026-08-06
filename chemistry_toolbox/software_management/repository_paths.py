"""Audit and rewrite active repository references to the managed v2 cache layout."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from .legacy_layout import translate_project_cache_path
from .paths import PROJECT_ROOT


ACTIVE_ROOTS = ("config", "src", "mcp", "scripts", "tests")
TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
EXCLUDED_PARTS = {"docs", "evidence", "native_software_docs", "__pycache__"}
REFERENCE = re.compile(r"\.software_cache/[A-Za-z0-9_+@*?=./-]+")


def _rewrite_reference(match: re.Match[str]) -> str:
    value = match.group(0)
    punctuation = ""
    while value.endswith("."):
        value = value[:-1]
        punctuation = "." + punctuation
    return translate_project_cache_path(value) + punctuation


def rewrite_text(text: str) -> tuple[str, int]:
    rewritten, count = REFERENCE.subn(_rewrite_reference, text)
    return rewritten, count


def active_reference_files() -> list[Path]:
    toolbox = PROJECT_ROOT / "chemistry_toolbox"
    files = []
    for root_name in ACTIVE_ROOTS:
        root = toolbox / root_name
        for path in root.rglob("*"):
            if (
                path.is_file()
                and path.suffix in TEXT_SUFFIXES
                and not (set(path.relative_to(toolbox).parts) & EXCLUDED_PARTS)
            ):
                files.append(path)
    return sorted(files)


def rewrite_repository_paths(*, apply: bool = False) -> dict[str, Any]:
    records = []
    for path in active_reference_files():
        original = path.read_text(encoding="utf-8")
        rewritten, count = rewrite_text(original)
        if not count or rewritten == original:
            continue
        if apply:
            temporary = path.with_name(f".{path.name}.software-paths-{os.getpid()}")
            temporary.write_text(rewritten, encoding="utf-8")
            os.chmod(temporary, path.stat().st_mode)
            temporary.replace(path)
        records.append(
            {
                "path": path.relative_to(PROJECT_ROOT).as_posix(),
                "references": count,
            }
        )
    return {
        "schema_version": 1,
        "mode": "apply" if apply else "check",
        "changed_files": len(records),
        "changed_references": sum(item["references"] for item in records),
        "files": records,
    }

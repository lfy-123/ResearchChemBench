#!/usr/bin/env python3
"""Fail when active first-party toolbox text contains CJK characters."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".model_cache",
    ".pytest_cache",
    ".software_cache",
    ".venv",
    "__pycache__",
}
TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if relative.parts[:2] == ("environment", "locks"):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def find_violations(root: Path) -> list[str]:
    violations: list[str] = []
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            if CJK.search(line):
                violations.append(f"{path.relative_to(root)}:{line_number}: {line.strip()}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=TOOLBOX_ROOT)
    args = parser.parse_args()
    violations = find_violations(args.root.resolve())
    if violations:
        print("Non-English CJK text found in active toolbox files:")
        print("\n".join(violations))
        return 1
    print("English-only check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

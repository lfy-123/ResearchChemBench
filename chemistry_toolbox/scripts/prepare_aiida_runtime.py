#!/usr/bin/env python3
"""Materialize a temporary AiiDA config for a relocatable job invocation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def prepare(source: Path, destination: Path, repository_root: Path) -> None:
    document = json.loads(source.read_text(encoding="utf-8"))
    profiles = document.get("profiles")
    profile = profiles.get("researchchembench") if isinstance(profiles, dict) else None
    storage = profile.get("storage") if isinstance(profile, dict) else None
    config = storage.get("config") if isinstance(storage, dict) else None
    if not isinstance(config, dict):
        raise ValueError("AiiDA profile researchchembench has no storage configuration")

    configured = Path(str(config.get("filepath") or ""))
    candidates = []
    if configured.is_absolute() and (configured / "database.sqlite").is_file():
        try:
            configured.resolve().relative_to(repository_root.resolve())
        except ValueError:
            pass
        else:
            candidates.append(configured)
    if not candidates and configured.name:
        candidate = repository_root / configured.name
        if (candidate / "database.sqlite").is_file():
            candidates.append(candidate)
    if repository_root.is_dir():
        candidates.extend(
            item
            for item in sorted(repository_root.iterdir())
            if item.is_dir() and (item / "database.sqlite").is_file()
        )
    if not candidates:
        raise FileNotFoundError(f"No AiiDA SQLite repository found under {repository_root}")

    config["filepath"] = str(candidates[0].resolve())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args()
    prepare(args.source, args.destination, args.repository_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

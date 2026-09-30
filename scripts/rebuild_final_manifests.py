#!/usr/bin/env python3
"""Rebuild package manifests after final-task edits."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation.contracts import package_content_hash, package_payload_entries


def rebuild(package: Path) -> dict[str, object]:
    manifest_path = package / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = package_payload_entries(package)
    manifest["entries"] = [entry.model_dump(mode="json") for entry in entries]
    manifest["package_content_sha256"] = package_content_hash(entries)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"paper_id": manifest.get("paper_id"), "task_type": manifest.get("task_type"), "entries": len(entries), "package_content_sha256": manifest["package_content_sha256"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("tasks"))
    args = parser.parse_args()
    rows = []
    for mode in ("autonomous_research", "paper_reproduction"):
        for package in sorted((args.root / f"final_verified_{mode}").glob("paper_*")):
            rows.append(rebuild(package))
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

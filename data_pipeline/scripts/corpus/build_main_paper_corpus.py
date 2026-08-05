#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> None:
    from src.stages.stage01_inventory.corpus import inventory_corpus

    parser = argparse.ArgumentParser(
        description="Build a symlink-only corpus of unique main-paper PDFs."
    )
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    rows = inventory_corpus(source)
    selected = [
        row
        for row in rows
        if row.get("document_role") == "main_paper" and not row.get("duplicate_of")
    ]
    output.mkdir(parents=True, exist_ok=True)
    selected_paths = {output / row["relative_path"] for row in selected}
    for existing in sorted(output.rglob("*"), reverse=True):
        if existing.is_symlink() and existing not in selected_paths:
            existing.unlink()
        elif existing.is_file() and not existing.is_symlink():
            raise RuntimeError(f"Refusing to replace regular file in output corpus: {existing}")
        elif existing.is_dir() and not any(existing.iterdir()):
            existing.rmdir()
    for row in selected:
        destination = output / row["relative_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink() or destination.exists():
            destination.unlink()
        os.symlink(row["source_path"], destination)

    supplementary = [row for row in rows if row.get("document_role") == "supplementary"]
    duplicate_main = [
        row for row in rows if row.get("document_role") == "main_paper" and row.get("duplicate_of")
    ]
    manifest = {
        "source": str(source),
        "output": str(output),
        "source_pdf_files": len(rows),
        "selected_unique_main_papers": len(selected),
        "excluded_supplementary_files": len(supplementary),
        "excluded_duplicate_main_files": len(duplicate_main),
        "selected": [
            {
                "document_id": row["document_id"],
                "source_path": row["source_path"],
                "relative_path": row["relative_path"],
            }
            for row in selected
        ],
        "excluded_supplementary": [
            {
                "document_id": row["document_id"],
                "source_path": row["source_path"],
                "relative_path": row["relative_path"],
                "duplicate_of": row.get("duplicate_of"),
            }
            for row in supplementary
        ],
    }
    manifest_path = output.parent / "main_paper_corpus_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        f"source={len(rows)} main_unique={len(selected)} "
        f"excluded={len(rows) - len(selected)} output={output} manifest={manifest_path}"
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Iterable


LAYOUT_EXTRACTOR_VERSION = "pymupdf-blocks-v1"


def extract_layout_blocks(pdf_path: str | Path) -> list[dict[str, Any]]:
    """Extract ordered PDF text blocks without interpreting their scientific meaning."""

    import pymupdf

    rows: list[dict[str, Any]] = []
    with pymupdf.open(Path(pdf_path)) as document:
        for page_index, page in enumerate(document):
            blocks = page.get_text("blocks", sort=True)
            for block_index, block in enumerate(blocks):
                text = str(block[4]).strip()
                block_type = int(block[6]) if len(block) > 6 else 0
                if not text or block_type != 0:
                    continue
                rows.append(
                    {
                        "page": page_index + 1,
                        "block_index": block_index,
                        "bbox": [round(float(value), 3) for value in block[:4]],
                        "text": text,
                    }
                )
    return rows


def write_layout_blocks(pdf_path: str | Path, output_path: str | Path) -> int:
    rows = extract_layout_blocks(pdf_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def install_document_query_tool(tools_directory: str | Path) -> Path:
    destination = Path(tools_directory) / "document_query.py"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), destination)
    return destination


def query_layout(
    inputs_root: str | Path,
    *,
    document_id: str | None = None,
    pages: Iterable[int] = (),
    contains: str | None = None,
    context: int = 0,
) -> list[dict[str, Any]]:
    root = Path(inputs_root)
    page_set = set(pages)
    paths = (
        [root / "documents" / document_id / "layout_blocks.jsonl"]
        if document_id
        else sorted((root / "documents").glob("*/layout_blocks.jsonl"))
    )
    rows: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            continue
        document_rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        selected: set[int] = set()
        for index, row in enumerate(document_rows):
            page_match = not page_set or int(row.get("page") or 0) in page_set
            text_match = not contains or contains.casefold() in str(row.get("text") or "").casefold()
            if page_match and text_match:
                selected.update(
                    range(max(0, index - context), min(len(document_rows), index + context + 1))
                )
        for index in sorted(selected):
            rows.append({"document_id": path.parent.name, **document_rows[index]})
    return rows


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Read page-layout evidence without applying scientific interpretation."
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--list", action="store_true", help="List documents and layout availability")
    parser.add_argument("--document", help="Restrict a query to one document ID")
    parser.add_argument("--page", type=int, action="append", default=[])
    parser.add_argument("--contains", help="Case-insensitive text search")
    parser.add_argument("--context", type=int, default=0, help="Adjacent blocks to include")
    args = parser.parse_args()
    if args.context < 0:
        parser.error("--context must be non-negative")
    if args.list:
        for directory in sorted((args.root / "documents").iterdir()):
            if directory.is_dir():
                print(
                    json.dumps(
                        {
                            "document_id": directory.name,
                            "layout_blocks": (directory / "layout_blocks.jsonl").is_file(),
                            "source_pdf": (directory / "source.pdf").is_file(),
                        }
                    )
                )
        return 0
    for row in query_layout(
        args.root,
        document_id=args.document,
        pages=args.page,
        contains=args.contains,
        context=args.context,
    ):
        print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())


__all__ = [
    "LAYOUT_EXTRACTOR_VERSION",
    "extract_layout_blocks",
    "install_document_query_tool",
    "query_layout",
    "write_layout_blocks",
]

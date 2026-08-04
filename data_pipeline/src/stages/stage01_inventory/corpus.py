from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from src.core.io import sha256_file, stable_id
from src.core.logging import log_progress
from src.stages.stage01_inventory.document_role import classify_document_role


def inventory_corpus(root: str | Path) -> list[dict[str, Any]]:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Corpus directory does not exist: {root}")

    records: list[dict[str, Any]] = []
    hash_owner: dict[str, tuple[str, str]] = {}
    paths = sorted(root.rglob("*.pdf"))
    for index, path in enumerate(paths, start=1):
        digest = sha256_file(path)
        document_id = stable_id("doc", digest)
        owner = hash_owner.get(digest)
        duplicate_of = owner[0] if owner else None
        duplicate_of_source_path = owner[1] if owner else None
        if owner is None:
            hash_owner[digest] = (document_id, str(path.resolve()))
        info = pdf_info(path)
        document_role = classify_document_role(path, info.get("Title"))
        records.append(
            {
                "document_id": document_id,
                "paper_id": document_id,
                "source_path": str(path.resolve()),
                "relative_path": str(path.relative_to(root)),
                "file_name": path.name,
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "page_count": info.get("Pages"),
                "pdf_metadata": info,
                "document_role": document_role,
                "duplicate_of": duplicate_of,
                "duplicate_of_source_path": duplicate_of_source_path,
                "inventory_status": "duplicate" if duplicate_of else "canonical",
            }
        )
        log_progress("stage_01_inventory", index, len(paths), path.name)
    return records


def pdf_info(path: str | Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["pdfinfo", str(path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return {}
    output: dict[str, Any] = {}
    for line in result.stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if key == "Pages":
            try:
                output[key] = int(value)
                continue
            except ValueError:
                pass
        output[key] = value
    return output


def markdown_metadata(text: str) -> dict[str, Any]:
    title = ""
    headings: list[str] = []
    lines = text.splitlines()
    title_index = -1
    title_candidates: list[tuple[float, int, str]] = []
    for index, raw in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", raw.strip())
        if not match:
            continue
        heading = _clean_line(match.group(2))
        headings.append(heading)
        if len(match.group(1)) == 1:
            score = _markdown_title_score(heading, index)
            if score is not None:
                title_candidates.append((score, index, heading))
    if title_candidates:
        _, title_index, title = max(title_candidates)
    abstract = ""
    if title_index >= 0:
        paragraph: list[str] = []
        for raw in lines[title_index + 1 :]:
            line = raw.strip()
            if line.startswith("#"):
                if paragraph:
                    break
                continue
            if not line:
                if len(" ".join(paragraph)) >= 200:
                    break
                paragraph = []
                continue
            paragraph.append(line)
            joined = " ".join(paragraph)
            if len(joined) >= 200:
                abstract = re.sub(r"\s+", " ", joined).strip()[:5000]
                break
    return {
        "title": title,
        "abstract": abstract,
        "section_headings": list(dict.fromkeys(headings))[:80],
    }


def _markdown_title_score(value: str, line_index: int) -> float | None:
    normalized = value.casefold().strip()
    generic = {
        "article",
        "data descriptor",
        "open access",
        "research article",
        "scientific data",
        "supplementary information",
    }
    field_prefixes = (
        "source:",
        "class:",
        "label:",
        "number of",
        "atom types:",
        "dielectric constant",
        "band gap",
        "atomization energy",
        "volume of",
    )
    words = value.split()
    if normalized in generic or normalized.startswith(field_prefixes):
        return None
    if not 5 <= len(words) <= 35:
        return None
    return 100.0 - min(line_index, 80) + min(len(words), 20)


def _clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" \t\r\n|-_")

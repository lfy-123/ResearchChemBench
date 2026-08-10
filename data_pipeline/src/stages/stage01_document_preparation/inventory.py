from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from src.core.concurrency import ordered_parallel_map
from src.core.io import sha256_file, stable_id
from src.core.logging import log_progress
from src.stages.stage01_document_preparation.document_role import classify_document_role


def inventory_corpus(root: str | Path, *, workers: int = 1) -> list[dict[str, Any]]:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Corpus directory does not exist: {root}")

    paths = sorted(root.rglob("*.pdf"))

    def inspect(path: Path) -> tuple[str, dict[str, Any]]:
        return sha256_file(path), pdf_info(path)

    inspected = ordered_parallel_map(
        inspect,
        paths,
        max_workers=workers,
        on_complete=lambda completed, total, _index, path, _result: log_progress(
            "stage_01_inventory", completed, total, path.name
        ),
    )

    records: list[dict[str, Any]] = []
    hash_owner: dict[str, tuple[str, str]] = {}
    for path, (digest, info) in zip(paths, inspected, strict=True):
        document_id = stable_id("doc", digest)
        owner = hash_owner.get(digest)
        duplicate_of = owner[0] if owner else None
        duplicate_of_source_path = owner[1] if owner else None
        if owner is None:
            hash_owner[digest] = (document_id, str(path.resolve()))
        bundle_root, paper_metadata = _paper_bundle(path, root)
        manifest_document = _manifest_document(path, bundle_root, paper_metadata)
        document_role = str(
            manifest_document.get("document_role")
            or classify_document_role(path, info.get("Title"))
        )
        paper_id = str(paper_metadata.get("paper_id") or document_id)
        records.append(
            {
                "document_id": document_id,
                "paper_id": paper_id,
                "source_path": str(path.resolve()),
                "relative_path": str(path.relative_to(root)),
                "paper_relative_path": (
                    str(path.relative_to(bundle_root)) if bundle_root is not None else path.name
                ),
                "paper_bundle_path": str(bundle_root) if bundle_root is not None else None,
                "file_name": path.name,
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "page_count": info.get("Pages"),
                "pdf_metadata": info,
                "document_role": document_role,
                "doi": paper_metadata.get("doi"),
                "source_dataset": paper_metadata.get("dataset"),
                "source_record": paper_metadata.get("source_record") or {},
                "source_remote_uri": manifest_document.get("remote_uri"),
                "journal_name": paper_metadata.get("journal_name"),
                "issn": paper_metadata.get("issn"),
                "article_url": paper_metadata.get("article_url"),
                "duplicate_of": duplicate_of,
                "duplicate_of_source_path": duplicate_of_source_path,
                "inventory_status": "duplicate" if duplicate_of else "canonical",
            }
        )
    return records


def group_inventory_by_paper(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for record in records:
        paper_id = str(record["paper_id"])
        paper = grouped.setdefault(
            paper_id,
            {
                "paper_id": paper_id,
                "doi": record.get("doi"),
                "title": None,
                "journal_name": record.get("journal_name"),
                "issn": record.get("issn"),
                "article_url": record.get("article_url"),
                "source_dataset": record.get("source_dataset"),
                "paper_bundle_path": record.get("paper_bundle_path"),
                "main_documents": [],
                "supplementary_documents": [],
            },
        )
        key = (
            "supplementary_documents"
            if record.get("document_role") == "supplementary"
            else "main_documents"
        )
        paper[key].append(record["document_id"])
    return list(grouped.values())


def _paper_bundle(path: Path, corpus_root: Path) -> tuple[Path | None, dict[str, Any]]:
    for parent in (path.parent, *path.parents):
        if parent == corpus_root.parent:
            break
        manifest = parent / "paper.json"
        if manifest.is_file():
            try:
                value = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, TypeError):
                return parent, {}
            return parent, value if isinstance(value, dict) else {}
        if parent == corpus_root:
            break
    return None, {}


def _manifest_document(
    path: Path, bundle_root: Path | None, paper_metadata: dict[str, Any]
) -> dict[str, Any]:
    if bundle_root is None:
        return {}
    relative = str(path.relative_to(bundle_root))
    documents = [paper_metadata.get("main_document") or {}]
    documents.extend(paper_metadata.get("supplementary_documents") or [])
    for document in documents:
        if str(document.get("relative_path") or "") == relative:
            return document
    return {}


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

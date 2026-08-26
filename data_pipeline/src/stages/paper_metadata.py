from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from src.integrations.grobid import parse_grobid_tei


def canonical_paper_metadata(
    *,
    paper_id: str,
    paper_records: Iterable[dict[str, Any]] = (),
    documents: Iterable[dict[str, Any]] = (),
    tei_paths: Iterable[str | Path] = (),
) -> dict[str, Any]:
    """Collect directory metadata without asking a task-synthesis model to infer it."""

    records = list(paper_records)
    document_rows = list(documents)
    primary = next(
        (
            row
            for row in document_rows
            if str(row.get("document_role") or "")
            in {"main_paper", "main_article", "paper", "article"}
        ),
        document_rows[0] if document_rows else {},
    )
    sources = [*records, primary]
    source_records = [
        row.get("source_record")
        for row in [primary, *document_rows]
        if isinstance(row.get("source_record"), dict)
    ]
    pdf_metadata = primary.get("pdf_metadata")
    if not isinstance(pdf_metadata, dict):
        pdf_metadata = {}

    tei_metadata = _tei_metadata(tei_paths)
    title = (
        _first_text(sources, "title", "paper_title")
        or _text(pdf_metadata.get("Title") or pdf_metadata.get("title"))
        or _text(tei_metadata.get("title"))
    )
    doi = _first_text(sources, "doi")
    journal = _first_text(sources, "journal", "journal_name", "venue")
    publication_date = _first_text(
        source_records, "publication_date_normalized"
    ) or _normalized_date(
        _first_text(source_records, "publication_date")
        or _first_text(sources, "publication_date_normalized", "publication_date")
    )
    tei_authors = _clean_authors(tei_metadata.get("authors"))
    record_authors = _record_authors([primary, *records])
    pdf_authors = _pdf_authors(pdf_metadata.get("Author") or pdf_metadata.get("author"))
    authors = _reconciled_authors(tei_authors, record_authors, pdf_authors)

    return {
        "paper_id": paper_id,
        "title": title,
        "doi": doi,
        "journal": journal,
        "publication_date": publication_date,
        "publication_year": (
            int(publication_date[:4]) if publication_date[:4].isdigit() else None
        ),
        "authors": authors,
    }


def canonical_metadata_index(
    *,
    paper_ids: Iterable[str],
    paper_records: Iterable[dict[str, Any]],
    documents: Iterable[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    records = list(paper_records)
    document_rows = list(documents)
    return {
        paper_id: canonical_paper_metadata(
            paper_id=paper_id,
            paper_records=[
                row for row in records if str(row.get("paper_id") or "") == paper_id
            ],
            documents=[
                row
                for row in document_rows
                if str(row.get("paper_id") or "") == paper_id
            ],
            tei_paths=[
                row["grobid_tei_path"]
                for row in document_rows
                if str(row.get("paper_id") or "") == paper_id
                and row.get("grobid_tei_path")
            ],
        )
        for paper_id in paper_ids
    }


def locate_grobid_tei(
    source_root: str | Path, document_ids: Iterable[str]
) -> list[Path]:
    """Locate retained Stage01 TEI files by document ID in a historical run."""

    root = Path(source_root).expanduser().resolve()
    output: list[Path] = []
    for document_id in sorted({value for value in document_ids if value}):
        patterns = (
            f"batches/*/microbatches/*/resume_attempts/*/stage01/"
            f"stage_01_document_preparation/raw/grobid/tei/{document_id}.tei.xml",
            f"batches/*/microbatches/*/stage_01_document_preparation/"
            f"raw/grobid/tei/{document_id}.tei.xml",
            f"microbatches/*/stage_01_document_preparation/"
            f"raw/grobid/tei/{document_id}.tei.xml",
            f"stage_01_document_preparation/raw/grobid/tei/{document_id}.tei.xml",
        )
        matches = sorted({path for pattern in patterns for path in root.glob(pattern)})
        if matches:
            output.append(matches[-1])
    return output


def _first_text(rows: Iterable[dict[str, Any]], *keys: str) -> str:
    for row in rows:
        for key in keys:
            value = _text(row.get(key))
            if value:
                return value
    return ""


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _normalized_date(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value
    for pattern in ("%d %B %Y", "%d %b %Y", "%B %d, %Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, pattern).date().isoformat()
        except ValueError:
            continue
    return ""


def _tei_metadata(paths: Iterable[str | Path]) -> dict[str, Any]:
    for value in paths:
        path = Path(value).expanduser()
        if not path.is_file():
            continue
        try:
            metadata = parse_grobid_tei(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if _text(metadata.get("title")) or _clean_authors(metadata.get("authors")):
            return metadata
    return {}


def _record_authors(rows: Iterable[dict[str, Any]]) -> list[str]:
    for row in rows:
        authors = _clean_authors(row.get("authors"))
        if authors:
            return authors
    return []


def _clean_authors(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _pdf_authors(value: Any) -> list[str]:
    if isinstance(value, list):
        return _clean_authors(value)
    text = _text(value)
    if not text:
        return []
    # A single unseparated PDF Author value is frequently only the first author.
    # Accept only explicit multi-author delimiters as a complete fallback list.
    if ";" in text:
        parts = text.split(";")
    elif re.search(r",\s+and\s+", text, flags=re.IGNORECASE):
        parts = re.sub(
            r",\s+and\s+", ",", text, flags=re.IGNORECASE
        ).split(",")
    elif re.search(r"\s+and\s+", text, flags=re.IGNORECASE):
        parts = re.split(r"\s+and\s+", text, flags=re.IGNORECASE)
    else:
        return []
    return [part.strip() for part in parts if part.strip()]


def _reconciled_authors(*sources: list[str]) -> list[str]:
    available = [authors for authors in sources if authors]
    if not available:
        return []
    # A complete PDF list can safely trim GROBID affiliation fragments when the
    # parsed TEI begins with the same ordered authors and only appends extras.
    pdf_authors = sources[-1]
    tei_authors = sources[0]
    if pdf_authors and tei_authors and len(tei_authors) >= len(pdf_authors):
        prefix = tei_authors[: len(pdf_authors)]
        if [_name_key(value) for value in prefix] == [_name_key(value) for value in pdf_authors]:
            return pdf_authors
    return available[0]


def _name_key(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


__all__ = [
    "canonical_metadata_index",
    "canonical_paper_metadata",
    "locate_grobid_tei",
]

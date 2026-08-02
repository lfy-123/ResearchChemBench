from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from src.core.io import sha256_file, stable_id
from src.core.logging import log_progress


def inventory_corpus(root: str | Path) -> list[dict[str, Any]]:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Corpus directory does not exist: {root}")

    records: list[dict[str, Any]] = []
    hash_owner: dict[str, str] = {}
    paths = sorted(root.rglob("*.pdf"))
    for index, path in enumerate(paths, start=1):
        digest = sha256_file(path)
        document_id = stable_id("doc", digest)
        duplicate_of = hash_owner.get(digest)
        if duplicate_of is None:
            hash_owner[digest] = document_id
        info = pdf_info(path)
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
                "duplicate_of": duplicate_of,
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


def cheap_extract_documents(
    inventory: list[dict[str, Any]],
    text_dir: str | Path,
    max_chars: int = 2_000_000,
    reuse_existing: bool = True,
) -> list[dict[str, Any]]:
    text_dir = Path(text_dir).expanduser().resolve()
    text_dir.mkdir(parents=True, exist_ok=True)
    output: list[dict[str, Any]] = []
    canonical_text: dict[str, str] = {}

    total = len(inventory)
    for index, item in enumerate(inventory, start=1):
        record = dict(item)
        if item.get("duplicate_of"):
            record.update(
                {
                    "cheap_extract_status": "duplicate",
                    "cheap_text_path": canonical_text.get(item["duplicate_of"]),
                    "text_quality": {"score": 0.0, "needs_ocr": False},
                }
            )
            output.append(record)
            log_progress(
                "stage_02_cheap_extract",
                index,
                total,
                item.get("file_name", item["document_id"]),
                status="duplicate",
            )
            continue

        target = text_dir / f"{item['document_id']}.txt"
        try:
            if target.exists() and reuse_existing:
                text = target.read_text(encoding="utf-8", errors="replace")
                status = "reused"
            else:
                text = pdftotext(item["source_path"])
                if len(text) > max_chars:
                    text = text[:max_chars]
                target.write_text(text, encoding="utf-8")
                status = "success"
            canonical_text[item["document_id"]] = str(target)
            metadata_title = (item.get("pdf_metadata") or {}).get("Title")
            raw_first_page = ""
            if not metadata_title or metadata_title.casefold() in {"untitled", "none"}:
                raw_first_page = pdftotext_first_page_raw(item["source_path"])
            title = infer_title(text, metadata_title, item["file_name"], raw_first_page)
            abstract = extract_abstract(text)
            headings = extract_headings(text)
            quality = text_quality(text, item.get("page_count"))
            record.update(
                {
                    "title": title,
                    "abstract": abstract,
                    "section_headings": headings,
                    "cheap_text_path": str(target),
                    "cheap_extract_status": status,
                    "text_quality": quality,
                    "text_characters": len(text),
                    "retrieval_sources": ["local_corpus"],
                }
            )
        except Exception as exc:
            record.update(
                {
                    "title": item["file_name"],
                    "abstract": "",
                    "section_headings": [],
                    "cheap_text_path": None,
                    "cheap_extract_status": "failed",
                    "cheap_extract_error": str(exc),
                    "text_quality": {"score": 0.0, "needs_ocr": True},
                    "text_characters": 0,
                    "retrieval_sources": ["local_corpus"],
                }
            )
        output.append(record)
        log_progress(
            "stage_02_cheap_extract",
            index,
            total,
            item.get("file_name", item["document_id"]),
            status=record.get("cheap_extract_status"),
        )
    return output


def pdftotext(path: str | Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", "-nopgbrk", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return result.stdout


def pdftotext_first_page_raw(path: str | Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-raw", "-f", "1", "-l", "1", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout


def infer_title(
    text: str,
    metadata_title: str | None,
    file_name: str,
    raw_first_page: str = "",
) -> str:
    if metadata_title and metadata_title.casefold() not in {"untitled", "none"}:
        return _clean_line(metadata_title)
    raw_title = _title_from_raw_page(raw_first_page)
    if raw_title:
        return raw_title
    lines = [_clean_line(line) for line in text.splitlines()[:80]]
    candidates = [
        line
        for line in lines
        if 20 <= len(line) <= 240
        and not re.match(r"^(abstract|introduction|research article|open access)\b", line, re.I)
        and not re.search(r"\b(doi|copyright|www\.|https?://|volume|issue)\b", line, re.I)
    ]
    if candidates:
        return max(candidates[:12], key=lambda value: (len(value.split()), len(value)))
    return Path(file_name).stem


def _title_from_raw_page(text: str) -> str:
    lines = [_clean_line(line) for line in text.splitlines()[:30] if _clean_line(line)]
    while lines and re.match(
        r"^(article|open access|research article|data descriptor)$", lines[0], re.I
    ):
        lines.pop(0)
    candidates: list[tuple[float, str]] = []
    for start in range(min(8, len(lines))):
        for width in range(1, 4):
            window = lines[start : start + width]
            if len(window) != width:
                continue
            candidate = " ".join(window)
            words = candidate.split()
            if not 4 <= len(words) <= 28 or len(candidate) > 240:
                continue
            score = 30 - start * 4 + min(18, len(words))
            if re.search(r"[†§✉@]|\bORCID\b", candidate, re.I):
                score -= 30
            if sum(char.isdigit() for char in candidate) >= 2:
                score -= 20
            if any(re.search(r"\d+\s*$", line) for line in window):
                score -= 30
            if candidate.endswith((".", ";")):
                score -= 12
            if re.search(
                r"\b(abstract|received|accepted|published|doi|institute|university)\b",
                candidate,
                re.I,
            ):
                score -= 25
            candidates.append((score, candidate))
    return max(candidates, default=(0.0, ""))[1]


def extract_abstract(text: str) -> str:
    match = re.search(
        r"\babstract\b\s*[:\-]?\s*(.{80,5000}?)(?=\n\s*(?:1\.?\s+)?(?:introduction|background|keywords?|key words)\b)",
        text,
        flags=re.I | re.S,
    )
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()[:5000]


def extract_headings(text: str, limit: int = 80) -> list[str]:
    known = re.compile(
        r"^(?:\d+(?:\.\d+)*[.)]?\s+)?(?:abstract|introduction|background|results|discussion|"
        r"conclusion|conclusions|methods|materials and methods|computational methods|"
        r"computational details|theoretical methods|density functional theory calculations|"
        r"molecular dynamics simulations|data availability|code availability|references)\b",
        re.I,
    )
    headings: list[str] = []
    for raw in text.splitlines():
        line = _clean_line(raw)
        if not line or len(line) > 140:
            continue
        if known.match(line) or (
            3 <= len(line.split()) <= 12 and line.isupper() and any(char.isalpha() for char in line)
        ):
            headings.append(line)
        if len(headings) >= limit:
            break
    return list(dict.fromkeys(headings))


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


def text_quality(text: str, page_count: int | None) -> dict[str, Any]:
    non_space = sum(1 for char in text if not char.isspace())
    alpha_numeric = sum(1 for char in text if char.isalnum())
    readable_ratio = alpha_numeric / max(1, non_space)
    chars_per_page = len(text) / max(1, page_count or 1)
    length_score = min(1.0, chars_per_page / 1200)
    score = round(100 * (0.65 * readable_ratio + 0.35 * length_score), 1)
    return {
        "score": score,
        "readable_ratio": round(readable_ratio, 3),
        "characters_per_page": round(chars_per_page, 1),
        "needs_ocr": score < 45 or len(text) < 1000,
    }


def _clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" \t\r\n|-_")

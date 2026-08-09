from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.core.concurrency import ordered_parallel_map
from src.core.io import stable_id
from src.integrations.grobid import GrobidClient, extract_documents_with_grobid
from src.integrations.pdf_fallback import fallback_pdf_to_tei
from src.stages.stage05_asset_collection.parsers import parse_asset
from src.v2.contracts import evidence_id, record_header, write_json, write_jsonl

DOCUMENT_NORMALIZATION_IMPLEMENTATION_VERSION = (
    "v2-stage01-normalization-20260809-require-all-known-si"
)


def run_document_normalization(
    *,
    papers: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    workspace: Path,
    run_id: str,
    grobid_client: GrobidClient | None = None,
) -> dict[str, Any]:
    stage_root = workspace / "stage_01_document_preparation"
    raw_root = stage_root / "raw"
    selected_papers = {row["paper_id"]: row for row in papers if row.get("decision") == "pass"}
    canonical = [
        row
        for row in documents
        if row.get("paper_id") in selected_papers
        and not row.get("duplicate_of")
        and row.get("canonical_in_paper", True)
        and Path(str(row.get("source_path"))).suffix.casefold() == ".pdf"
    ]
    non_pdf = [
        row
        for row in documents
        if row.get("paper_id") in selected_papers
        and not row.get("duplicate_of")
        and Path(str(row.get("source_path"))).suffix.casefold() != ".pdf"
    ]
    attempts: list[dict[str, Any]] = []
    normalized: list[dict[str, Any]] = []
    if canonical:
        grobid_config = config.get("grobid") or {}
        grobid_rows = extract_documents_with_grobid(
            canonical,
            grobid_client
            or GrobidClient(
                base_url=str(grobid_config.get("base_url", "http://127.0.0.1:8070")),
                timeout_seconds=int(grobid_config.get("timeout_seconds", 900)),
                retries=int(grobid_config.get("retries", 2)),
            ),
            raw_root / "grobid" / "tei",
            raw_root / "grobid" / "text",
            max_chars=int(config.get("max_chars", 4_000_000)),
            reuse_existing=bool(grobid_config.get("reuse_existing", True)),
            exclude_supplementary=False,
            fallback_config={
                "enabled": True,
                "output_dir": raw_root / "pdftotext",
                "pdftotext_enabled": True,
                "pdftotext_timeout_seconds": int(
                    grobid_config.get("pdftotext_timeout_seconds", 300)
                ),
            },
            workers=int(grobid_config.get("workers", 1)),
        )
        for document, result in zip(canonical, grobid_rows, strict=True):
            text = _read_optional(result.get("text_path"))
            parser = (
                "pdftotext"
                if str(result.get("grobid_extract_status", "")).startswith("fallback_")
                else "grobid"
            )
            quality = assess_text_quality(
                text,
                document.get("page_count"),
                config,
                document.get("document_role"),
                result,
            )
            attempts.append(
                _attempt(
                    document, parser, result.get("grobid_extract_status", "failed"), quality, result
                )
            )
            if parser == "grobid" and not quality["passed"]:
                fallback_result = _pdftotext_fallback(document, raw_root, grobid_config)
                fallback_text = str(fallback_result.get("text") or "")
                fallback_quality = assess_text_quality(
                    fallback_text,
                    document.get("page_count"),
                    config,
                    document.get("document_role"),
                    fallback_result,
                )
                attempts.append(
                    _attempt(
                        document,
                        "pdftotext",
                        fallback_result.get("status", "failed"),
                        fallback_quality,
                        fallback_result,
                    )
                )
                if fallback_result.get("status") == "success" and fallback_quality["passed"]:
                    text = fallback_text
                    parser = "pdftotext"
                    result = {key: value for key, value in fallback_result.items() if key != "text"}
                    quality = fallback_quality
            if result.get("grobid_extract_status") != "failed" and quality["passed"]:
                normalized.append(
                    materialize_document(
                        document,
                        text,
                        parser,
                        result,
                        quality,
                        stage_root,
                        run_id,
                        stage_name="stage01",
                    )
                )
            else:
                normalized.append(
                    {
                        **document,
                        **record_header(
                            run_id=run_id,
                            stage="stage01",
                            paper_id=document["paper_id"],
                            document_id=document["document_id"],
                        ),
                        "processing_status": "failed",
                        "decision": "parse_failed",
                        "selected_parser": None,
                        "quality": quality,
                    }
                )

    if non_pdf:
        asset_rows = ordered_parallel_map(
            lambda document: _normalize_non_pdf(document, config, stage_root, raw_root, run_id),
            non_pdf,
            max_workers=int(config.get("asset_workers", 2)),
        )
        for record, attempt in asset_rows:
            normalized.append(record)
            attempts.append(attempt)

    normalized.sort(key=lambda row: (row["paper_id"], row["document_id"]))
    paper_rows = _paper_quality(papers, normalized, run_id)
    write_jsonl(stage_root / "documents.jsonl", normalized)
    write_jsonl(stage_root / "paper_bundles.jsonl", paper_rows)
    write_jsonl(stage_root / "parser_attempts.jsonl", attempts)
    write_jsonl(
        stage_root / "quality_reports.jsonl",
        [{"document_id": row["document_id"], "quality": row.get("quality")} for row in normalized],
    )
    write_jsonl(
        stage_root / "rejected.jsonl", [row for row in paper_rows if row["decision"] != "pass"]
    )
    summary = {
        **record_header(run_id=run_id, stage="stage01"),
        "papers": len(paper_rows),
        "documents": len(normalized),
        "passed_papers": sum(row["decision"] == "pass" for row in paper_rows),
        "failed_papers": sum(row["decision"] != "pass" for row in paper_rows),
        "partial_si_parse_papers": sum(bool(row.get("partial_si_parse")) for row in paper_rows),
        "failed_supplementary_documents": sum(
            len(row.get("failed_supplementary_document_ids") or []) for row in paper_rows
        ),
        "selected_parsers": _counts(normalized, "selected_parser"),
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"papers": paper_rows, "documents": normalized, "attempts": attempts, "summary": summary}


def _pdftotext_fallback(document, raw_root, grobid_config):
    output_dir = raw_root / "pdftotext_quality_fallback"
    try:
        result = fallback_pdf_to_tei(
            document,
            output_dir,
            {
                "pdftotext_enabled": True,
                "pdftotext_timeout_seconds": int(
                    grobid_config.get("pdftotext_timeout_seconds", 300)
                ),
            },
        )
        return {
            **result,
            "status": "success",
            "text_path": str(
                (output_dir.resolve() / document["document_id"] / "fallback_source.txt")
            ),
        }
    except Exception as exc:
        return {
            "status": "failed",
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
            "text_path": None,
        }


def assess_text_quality(
    text: str,
    pages: int | None,
    config: dict[str, Any],
    document_role: str | None = None,
    parser_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    characters = len(text)
    readable = sum(character.isprintable() or character in "\n\t" for character in text)
    replacement = text.count("\ufffd")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    repeated = len(lines) - len(set(lines))
    readable_ratio = readable / characters if characters else 0.0
    replacement_ratio = replacement / characters if characters else 1.0
    repeated_ratio = repeated / len(lines) if lines else 1.0
    chars_per_page = characters / pages if pages else None
    structured_pages = (parser_result or {}).get("structured_pages")
    page_coverage = (
        float(structured_pages) / float(pages) if structured_pages is not None and pages else None
    )
    minimum = int(
        config.get("min_supplementary_characters", 100)
        if document_role == "supplementary"
        else config.get("min_main_characters", 1000)
    )
    passed = (
        characters >= minimum
        and readable_ratio >= float(config.get("min_readable_character_ratio", 0.90))
        and replacement_ratio <= float(config.get("max_replacement_character_ratio", 0.01))
        and repeated_ratio <= float(config.get("max_repeated_line_ratio", 0.50))
        and (
            page_coverage is None
            or page_coverage >= float(config.get("min_page_coverage_ratio", 0.95))
        )
    )
    return {
        "passed": passed,
        "characters": characters,
        "characters_per_page": round(chars_per_page, 2) if chars_per_page is not None else None,
        "page_coverage_ratio": round(page_coverage, 5) if page_coverage is not None else None,
        "readable_character_ratio": round(readable_ratio, 5),
        "replacement_character_ratio": round(replacement_ratio, 5),
        "repeated_line_ratio": round(repeated_ratio, 5),
        "needs_ocr": bool(
            characters < minimum or (chars_per_page is not None and chars_per_page < 100)
        ),
        "table_caption_count": len(re.findall(r"\btable\s+s?\d+", text, re.I)),
        "figure_caption_count": len(re.findall(r"\bfig(?:ure)?\.?\s+s?\d+", text, re.I)),
        "equation_count": len(re.findall(r"\$\$|\\begin\{equation", text)),
        "truncated": False,
    }


def materialize_document(
    document,
    text,
    parser,
    parser_result,
    quality,
    stage_root,
    run_id,
    *,
    stage_name,
):
    target = stage_root / "normalized" / document["document_id"]
    target.mkdir(parents=True, exist_ok=True)
    markdown_path = target / "normalized_document.md"
    markdown_path.write_text(text, encoding="utf-8")
    blocks = _blocks(document["document_id"], text, parser, parser_result)
    write_jsonl(target / "content_blocks.jsonl", blocks)
    metadata = {
        "selected_parser": parser,
        "source_path": document["source_path"],
        "quality": quality,
        "parser_output": {
            key: value
            for key, value in parser_result.items()
            if key not in {"stdout_tail", "stderr_tail"}
        },
    }
    write_json(target / "metadata.json", metadata)
    return {
        **document,
        **record_header(
            run_id=run_id,
            stage=stage_name,
            paper_id=document["paper_id"],
            document_id=document["document_id"],
        ),
        "processing_status": "completed",
        "decision": "pass",
        "selected_parser": parser,
        "normalized_markdown_path": str(markdown_path),
        "content_blocks_path": str(target / "content_blocks.jsonl"),
        "quality": quality,
    }


def _normalize_non_pdf(document, config, stage_root, raw_root, run_id):
    asset = {
        "asset_id": document["document_id"],
        "paper_id": document["paper_id"],
        "file_name": document["file_name"],
        "original_path": document["source_path"],
        "size_bytes": document.get("size_bytes"),
        "sha256": document.get("sha256"),
        "media_type": document.get("content_type"),
    }
    mineru_config = {"execute": False, "enabled": False}
    updated, children, _clues = parse_asset(
        asset,
        parsed_root=raw_root / "structured_assets",
        mineru_config=mineru_config,
        next_round=0,
        max_text_chars=int(config.get("max_chars", 4_000_000)),
        max_archive_files=int(config.get("max_archive_files", 5000)),
        max_archive_bytes=int(config.get("max_archive_bytes", 50 * 1024**3)),
    )
    texts = _read_paths(updated.get("readable_paths") or [])
    child_records = []
    for child in children:
        child_id = stable_id("asset", document["document_id"], str(child), length=16)
        child_asset = {
            "asset_id": child_id,
            "paper_id": document["paper_id"],
            "file_name": child.name,
            "original_path": str(child),
            "size_bytes": child.stat().st_size,
            "sha256": None,
            "media_type": None,
        }
        child_updated, _grandchildren, _child_clues = parse_asset(
            child_asset,
            parsed_root=raw_root / "structured_assets",
            mineru_config=mineru_config,
            next_round=0,
            max_text_chars=int(config.get("max_chars", 4_000_000)),
            max_archive_files=int(config.get("max_archive_files", 5000)),
            max_archive_bytes=int(config.get("max_archive_bytes", 50 * 1024**3)),
        )
        child_records.append(child_updated)
        texts.extend(_read_paths(child_updated.get("readable_paths") or []))
    text = "\n\n".join(value for value in texts if value).strip()
    quality = assess_text_quality(text, None, config, "supplementary")
    details = {"asset": updated, "children": child_records}
    if updated.get("parse_status") in {"success", "partial"} and quality["passed"]:
        record = materialize_document(
            document,
            text,
            f"asset_{updated.get('parser') or 'unknown'}",
            details,
            quality,
            stage_root,
            run_id,
            stage_name="stage01",
        )
    else:
        record = {
            **document,
            **record_header(
                run_id=run_id,
                stage="stage01",
                paper_id=document["paper_id"],
                document_id=document["document_id"],
            ),
            "processing_status": "failed",
            "decision": "parse_failed",
            "selected_parser": None,
            "quality": quality,
            "parser_error": updated.get("error"),
        }
    attempt = _attempt(
        document,
        f"asset_{updated.get('parser') or 'unknown'}",
        str(updated.get("parse_status") or "failed"),
        quality,
        {"error": updated.get("error"), "text_path": (updated.get("readable_paths") or [None])[0]},
    )
    return record, attempt


def _read_paths(paths):
    output = []
    for value in paths:
        path = Path(str(value))
        if path.is_file():
            output.append(path.read_text(encoding="utf-8", errors="replace"))
    return output


def _blocks(
    document_id: str,
    text: str,
    parser: str,
    parser_result: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    structured_path = (parser_result or {}).get("content_list_v2_path")
    if structured_path and Path(str(structured_path)).is_file():
        try:
            payload = json.loads(Path(str(structured_path)).read_text(encoding="utf-8"))
            structured = _structured_blocks(document_id, payload, parser)
            if structured:
                return structured
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    blocks = []
    section: list[str] = []
    for index, raw in enumerate(re.split(r"\n\s*\n", text)):
        value = re.sub(r"\s+", " ", raw).strip()
        if not value:
            continue
        heading = re.match(r"^#{1,6}\s+(.+)$", raw.strip())
        if heading:
            section = [heading.group(1).strip()]
            block_type = "heading"
        else:
            block_type = "paragraph"
        blocks.append(
            {
                "block_id": evidence_id(document_id, index, value),
                "evidence_id": evidence_id(document_id, index, value),
                "document_id": document_id,
                "page": None,
                "section_path": section,
                "block_type": block_type,
                "text": value,
                "bbox": None,
                "source_parser": parser,
                "source_ref": f"normalized:{index}",
            }
        )
    return blocks


def _structured_blocks(document_id, payload, parser):
    blocks = []

    def walk(value, *, page=None, section=()):
        if isinstance(value, list):
            for item in value:
                walk(item, page=page, section=section)
            return
        if not isinstance(value, dict):
            return
        current_page = next(
            (
                value[key]
                for key in ("page_idx", "page_index", "page_number", "page")
                if value.get(key) is not None
            ),
            page,
        )
        raw_type = str(value.get("type") or value.get("block_type") or "paragraph")
        raw_text = value.get("text") or value.get("content")
        heading = raw_type.casefold() in {"title", "heading", "section_title"}
        current_section = (*section, str(raw_text).strip()) if heading and raw_text else section
        if isinstance(raw_text, str) and raw_text.strip():
            text_value = re.sub(r"\s+", " ", raw_text).strip()
            index = len(blocks)
            block_id = evidence_id(document_id, index, text_value)
            blocks.append(
                {
                    "block_id": block_id,
                    "evidence_id": block_id,
                    "document_id": document_id,
                    "page": current_page,
                    "section_path": list(current_section if heading else section),
                    "block_type": raw_type,
                    "text": text_value,
                    "bbox": value.get("bbox"),
                    "source_parser": parser,
                    "source_ref": f"content_list_v2:{index}",
                }
            )
            return
        for child in value.values():
            if isinstance(child, (dict, list)):
                walk(child, page=current_page, section=current_section)

    walk(payload)
    return blocks


def _paper_quality(papers, documents, run_id):
    by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        by_paper.setdefault(document["paper_id"], []).append(document)
    output = []
    for paper in papers:
        docs = by_paper.get(paper["paper_id"], [])
        excluded_type = _explicit_excluded_type(docs)
        main_ok = any(
            row.get("document_role") != "supplementary" and row.get("decision") == "pass"
            for row in docs
        )
        supplementary_docs = [row for row in docs if row.get("document_role") == "supplementary"]
        parsed_supplementary_docs = [
            row for row in supplementary_docs if row.get("decision") == "pass"
        ]
        failed_supplementary_docs = [
            row for row in supplementary_docs if row.get("decision") != "pass"
        ]
        requires_si = paper.get("package_status") == "complete_with_si"
        all_known_si_ok = bool(supplementary_docs) and not failed_supplementary_docs
        passed = not excluded_type and main_ok and (not requires_si or all_known_si_ok)
        output.append(
            {
                **record_header(run_id=run_id, stage="stage01", paper_id=paper["paper_id"]),
                "doi": paper.get("doi"),
                "title": paper.get("title"),
                "journal_name": paper.get("journal_name"),
                "article_url": paper.get("article_url"),
                "package_status": paper.get("package_status"),
                "document_ids": [row["document_id"] for row in docs],
                "main_parse_ok": main_ok,
                "supplementary_parse_ok": all_known_si_ok if requires_si else None,
                "known_supplementary_documents": len(supplementary_docs),
                "parsed_supplementary_documents": len(parsed_supplementary_docs),
                "failed_supplementary_document_ids": [
                    row["document_id"] for row in failed_supplementary_docs
                ],
                "partial_si_parse": bool(
                    requires_si and parsed_supplementary_docs and failed_supplementary_docs
                ),
                "processing_status": "completed",
                "excluded_document_type": excluded_type,
                "decision": (
                    "pass"
                    if passed
                    else "excluded_document_type"
                    if excluded_type
                    else "parse_failed"
                ),
            }
        )
    return output


def _explicit_excluded_type(documents):
    excluded = {"editorial", "correction", "retraction", "masthead", "review"}
    for document in documents:
        source = document.get("source_record") or {}
        for key in ("article_type", "publication_type", "document_type", "type"):
            value = str(source.get(key) or "").strip().casefold()
            if value in excluded:
                return value
    return None


def _attempt(document, parser, status, quality, details):
    return {
        "document_id": document["document_id"],
        "paper_id": document["paper_id"],
        "parser": parser,
        "status": status,
        "quality": quality,
        "error": details.get("error") or details.get("grobid_extract_error"),
        "output_path": details.get("markdown_path") or details.get("text_path"),
    }


def _read_optional(value: str | None) -> str:
    if not value:
        return ""
    path = Path(value)
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _counts(rows, key):
    output: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "none")
        output[value] = output.get(value, 0) + 1
    return dict(sorted(output.items()))

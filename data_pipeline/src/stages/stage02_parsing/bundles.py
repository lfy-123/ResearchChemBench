from __future__ import annotations

from typing import Any


def build_paper_text_bundles(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for document in documents:
        paper_id = str(document["paper_id"])
        bundle = grouped.setdefault(
            paper_id,
            {
                "paper_id": paper_id,
                "doi": document.get("doi"),
                "title": None,
                "journal_name": document.get("journal_name") or document.get("venue"),
                "issn": document.get("issn"),
                "article_url": document.get("article_url"),
                "source_dataset": document.get("source_dataset"),
                "source_record": document.get("source_record") or {},
                "paper_bundle_path": document.get("paper_bundle_path"),
                "main_documents": [],
                "supplementary_documents": [],
                "parse_errors": [],
            },
        )
        summary = {
            "paper_id": paper_id,
            "document_id": document.get("document_id"),
            "document_role": document.get("document_role"),
            "source_path": document.get("source_path"),
            "text_path": document.get("text_path"),
            "tei_path": document.get("grobid_tei_path"),
            "parse_status": document.get("grobid_extract_status"),
            "text_quality": document.get("text_quality"),
            "title": document.get("title"),
            "section_headings": document.get("section_headings") or [],
        }
        if document.get("grobid_extract_status") == "failed":
            bundle["parse_errors"].append(
                {
                    "document_id": document.get("document_id"),
                    "error": document.get("grobid_extract_error"),
                }
            )
        role = document.get("document_role")
        if role == "supplementary":
            bundle["supplementary_documents"].append(summary)
        else:
            bundle["main_documents"].append(summary)
            if document.get("title"):
                bundle["title"] = document["title"]
            if document.get("doi"):
                bundle["doi"] = document["doi"]
    for bundle in grouped.values():
        bundle["has_local_supplementary"] = bool(bundle["supplementary_documents"])
        bundle["usable_main_text"] = any(
            item.get("text_path") and item.get("parse_status") != "failed"
            for item in bundle["main_documents"]
        )
        bundle["usable_supplementary_text"] = any(
            item.get("text_path") and item.get("parse_status") != "failed"
            for item in bundle["supplementary_documents"]
        )
    return list(grouped.values())

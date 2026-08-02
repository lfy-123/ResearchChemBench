from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.core.io import sha256_file, stable_id
from src.ingestion.document_role import (
    GENERIC_SUPPLEMENTARY_TITLES,
    classify_document_role,
)


def build_study_bundles(
    documents: list[dict[str, Any]], assets: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    """Group shortlisted main text, SI, versions, and registered assets by study."""

    asset_map = {item["paper_id"]: item for item in assets or []}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for document in documents:
        if document.get("duplicate_of"):
            continue
        groups[_study_key(document)].append(document)

    bundles: list[dict[str, Any]] = []
    for group_key, members in groups.items():
        primary = max(members, key=_primary_rank)
        doi = _normalize_doi(primary.get("doi"))
        study_id = stable_id("study", doi or group_key, primary.get("title"))
        files: list[dict[str, Any]] = []
        seen_paths: set[str] = set()
        for member in members:
            role = _document_role(member)
            _append_file(files, seen_paths, role, member.get("source_path"), member.get("paper_id"))
            asset = asset_map.get(member["paper_id"], {})
            _append_file(
                files, seen_paths, "main_paper", asset.get("paper"), member.get("paper_id")
            )
            for value in asset.get("supplementary", []):
                _append_file(files, seen_paths, "supplementary", value, member.get("paper_id"))
            for value in asset.get("text", []):
                _append_file(files, seen_paths, "text", value, member.get("paper_id"))
            for value in asset.get("hidden_reference_files", []):
                _append_file(files, seen_paths, "hidden_reference", value, member.get("paper_id"))
        bundles.append(
            {
                "study_id": study_id,
                "paper_id": primary["paper_id"],
                "primary_paper_id": primary["paper_id"],
                "member_paper_ids": [item["paper_id"] for item in members],
                "doi": doi,
                "title": primary.get("title"),
                "files": files,
                "main_paper_path": _first_path(files, "main_paper"),
                "supplementary_paths": [
                    item["path"]
                    for item in files
                    if item["role"] == "supplementary" and item["exists"]
                ],
                "complete_main_paper": any(
                    item["role"] == "main_paper" and item["exists"] for item in files
                ),
                "has_supplementary_or_data": any(
                    item["role"] != "main_paper" and item["exists"] for item in files
                ),
                "status": "assembled_for_extraction",
                "grouping_method": "path_doi_title_hybrid",
            }
        )
    return sorted(bundles, key=lambda item: item["study_id"])


def member_bundle_map(bundles: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        paper_id: bundle for bundle in bundles for paper_id in bundle.get("member_paper_ids", [])
    }


def _study_key(document: dict[str, Any]) -> str:
    path_key = _structured_path_key(document.get("source_path"))
    if path_key:
        return f"path:{path_key}"
    doi = _normalize_doi(document.get("doi"))
    if doi:
        return f"doi:{doi}"
    title = _normalize_title(document.get("title"))
    return f"title:{title or document.get('paper_id')}"


def _structured_path_key(raw: Any) -> str | None:
    if not raw:
        return None
    path = Path(raw).resolve()
    parts = path.parts
    for index, part in enumerate(parts[:-1]):
        lower = part.casefold()
        if re.match(r"^\d+_hidden_reference_answers$", lower):
            return str(Path(*parts[:index]))
        if lower in {"paper", "supplementary"} or "supplementary" in lower:
            return str(Path(*parts[:index]))
    return None


def _document_role(document: dict[str, Any]) -> str:
    return str(
        document.get("document_role")
        or classify_document_role(document.get("source_path") or "", document.get("title"))
    )


def _primary_rank(document: dict[str, Any]) -> tuple[int, int, int]:
    role_score = 1 if _document_role(document) == "main_paper" else 0
    title = str(document.get("title") or "")
    title_score = (
        0 if any(value in title.casefold() for value in GENERIC_SUPPLEMENTARY_TITLES) else 1
    )
    return role_score, title_score, len(title)


def _append_file(
    files: list[dict[str, Any]], seen: set[str], role: str, raw: Any, paper_id: Any
) -> None:
    if not raw:
        return
    path = Path(raw).resolve()
    key = str(path)
    if key in seen:
        return
    seen.add(key)
    files.append(
        {
            "role": role,
            "path": key,
            "paper_id": paper_id,
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.is_file() else None,
            "size_bytes": path.stat().st_size if path.is_file() else None,
        }
    )


def _first_path(files: list[dict[str, Any]], role: str) -> str | None:
    return next((item["path"] for item in files if item["role"] == role and item["exists"]), None)


def _normalize_doi(value: Any) -> str | None:
    if not value:
        return None
    normalized = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", str(value).strip(), flags=re.I)
    return normalized.casefold() or None


def _normalize_title(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold()).strip()

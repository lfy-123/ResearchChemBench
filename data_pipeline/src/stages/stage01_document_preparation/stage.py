from __future__ import annotations

import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from src.contracts import (
    canonical_hash,
    decision_counts,
    record_header,
    write_json,
    write_jsonl,
)
from src.core.io import normalize_title, sha256_file, stable_id
from src.stages.stage01_document_preparation.inventory import (
    group_inventory_by_paper,
    inventory_corpus,
)
from src.stages.stage01_document_preparation.normalization import run_document_normalization
from src.stages.stage01_document_preparation.supplementary import (
    acquire_supplementary_materials,
)

PASS_STATUSES = {"complete_with_si", "complete_confirmed_no_si"}


def run_paper_package(
    *,
    corpus_root: str | Path,
    config: dict[str, Any],
    workspace: Path,
    run_id: str,
) -> dict[str, Any]:
    stage_root = workspace / "stage_01_document_preparation" / "package"
    stage_root.mkdir(parents=True, exist_ok=True)
    inventory = inventory_corpus(corpus_root, workers=int(config.get("workers", 1)))
    inventory.extend(_inventory_manifest_attachments(corpus_root, inventory))
    papers = group_inventory_by_paper(inventory)
    papers, inventory, duplicate_groups = _normalize_paper_identities(papers, inventory)
    by_document = {row["document_id"]: row for row in inventory}
    candidates: list[dict[str, Any]] = []
    for paper in papers:
        main = [by_document[value] for value in paper["main_documents"]]
        supplementary = [by_document[value] for value in paper["supplementary_documents"]]
        candidates.append(
            {
                **paper,
                "main_document_records": main,
                "supplementary_document_records": supplementary,
                "has_local_supplementary": bool(supplementary),
                "supplementary_discovery": _remote_discovery(main),
            }
        )

    acquisition = acquire_supplementary_materials(
        candidates,
        stage_root / "acquisition",
        {
            "enable_network": bool(config.get("enable_network", True)),
            "workers": int(config.get("network_workers", 4)),
            "publisher_adapters": config.get("publisher_adapters"),
            "paper_timeout_seconds": int(config.get("paper_timeout_seconds", 180)),
            "read_timeout_seconds": int(config.get("read_timeout_seconds", 30)),
            "connect_timeout_seconds": int(config.get("connect_timeout_seconds", 15)),
            "max_attachments_per_paper": int(config.get("max_attachments_per_paper", 20)),
            "max_file_bytes": int(config.get("max_file_bytes", 100 * 1024**2)),
            "max_total_bytes_per_paper": int(
                config.get("max_total_bytes_per_paper", 250 * 1024**2)
            ),
        },
    )
    documents = list(inventory)
    paper_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    for paper in acquisition:
        acquired_documents = [
            _attachment_document(paper["paper_id"], item)
            for item in ((paper.get("supplementary_acquisition") or {}).get("attachments") or [])
        ]
        documents.extend(acquired_documents)
        local_si = list(paper.get("supplementary_document_records") or [])
        acquisition_info = paper.get("supplementary_acquisition") or {}
        presence = acquisition_info.get("presence_status")
        if local_si or acquired_documents:
            status = "complete_with_si"
        elif presence == "absent_confirmed":
            status = "complete_confirmed_no_si"
        elif presence == "present_unavailable":
            status = "incomplete_si_unavailable"
        else:
            status = "retryable_acquisition_error"
        main_documents = list(paper.get("main_document_records") or [])
        if not main_documents or not any(
            _valid_pdf(Path(item["source_path"])) for item in main_documents
        ):
            status = "invalid_main_document"
        row = {
            **record_header(run_id=run_id, stage="stage01", paper_id=paper["paper_id"]),
            "doi": paper.get("doi"),
            "title": paper.get("title"),
            "journal_name": paper.get("journal_name"),
            "article_url": paper.get("article_url"),
            "paper_bundle_path": paper.get("paper_bundle_path"),
            "main_document_ids": [item["document_id"] for item in main_documents],
            "supplementary_document_ids": [
                item["document_id"] for item in [*local_si, *acquired_documents]
            ],
            "package_status": status,
            "processing_status": "completed",
            "decision": "pass" if status in PASS_STATUSES else "hold",
            "supplementary_acquisition": acquisition_info,
        }
        paper_rows.append(row)
        attempts.extend(
            {
                "paper_id": paper["paper_id"],
                **attempt,
            }
            for attempt in acquisition_info.get("attempts") or []
        )

    write_jsonl(stage_root / "papers.jsonl", paper_rows)
    write_jsonl(stage_root / "documents.jsonl", documents)
    write_jsonl(stage_root / "duplicate_groups.jsonl", duplicate_groups)
    write_jsonl(stage_root / "acquisition_attempts.jsonl", attempts)
    write_jsonl(stage_root / "held.jsonl", [row for row in paper_rows if row["decision"] != "pass"])
    summary = {
        **record_header(run_id=run_id, stage="stage01"),
        "papers": len(paper_rows),
        "documents": len(documents),
        "package_statuses": decision_counts(paper_rows, "package_status"),
        "passed": sum(row["decision"] == "pass" for row in paper_rows),
        "held": sum(row["decision"] != "pass" for row in paper_rows),
        "duplicate_groups": len(duplicate_groups),
        "corpus_root": str(Path(corpus_root).expanduser().resolve()),
        "config_hash": canonical_hash(config),
        "input_signature": canonical_hash(
            sorted(
                (row["document_id"], row.get("sha256"), row.get("source_path")) for row in documents
            )
        ),
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {
        "papers": paper_rows,
        "documents": documents,
        "duplicate_groups": duplicate_groups,
        "summary": summary,
    }


def run_stage01(
    *,
    corpus_root: str | Path,
    config: dict[str, Any],
    workspace: Path,
    run_id: str,
    grobid_client=None,
) -> dict[str, Any]:
    """Build paper/SI packages and perform low-cost document normalization."""

    package = run_paper_package(
        corpus_root=corpus_root,
        config=config.get("package") or config,
        workspace=workspace,
        run_id=run_id,
    )
    normalized = run_document_normalization(
        papers=package["papers"],
        documents=package["documents"],
        config=config.get("normalization") or config,
        workspace=workspace,
        run_id=run_id,
        grobid_client=grobid_client,
    )
    normalized["package"] = package
    normalized["summary"] = {
        **package["summary"],
        **normalized["summary"],
        "stage": "stage01",
        "duplicate_groups": package["summary"].get("duplicate_groups", 0),
    }
    return normalized


def _normalize_paper_identities(papers, inventory):
    by_document = {row["document_id"]: row for row in inventory}
    owners: list[dict[str, Any]] = []
    mapping: dict[str, str] = {}
    duplicate_groups: list[dict[str, Any]] = []
    for paper in papers:
        main = [by_document[value] for value in paper.get("main_documents") or []]
        title = str(
            paper.get("title")
            or next(
                (
                    (row.get("pdf_metadata") or {}).get("Title")
                    for row in main
                    if (row.get("pdf_metadata") or {}).get("Title")
                ),
                "",
            )
        ).strip()
        paper = {**paper, "title": title or None}
        owner = next((item for item in owners if _same_identity(item, paper, by_document)), None)
        if owner is None:
            owners.append(paper)
            mapping[paper["paper_id"]] = paper["paper_id"]
            continue
        original_id = paper["paper_id"]
        canonical_id = owner["paper_id"]
        mapping[original_id] = canonical_id
        owner["main_documents"].extend(paper.get("main_documents") or [])
        owner["supplementary_documents"].extend(paper.get("supplementary_documents") or [])
        for key in ("doi", "title", "journal_name", "issn", "article_url", "source_dataset"):
            owner[key] = owner.get(key) or paper.get(key)
        duplicate_groups.append(
            {
                "canonical_paper_id": canonical_id,
                "duplicate_paper_id": original_id,
                "reason": "doi_or_title_author_match",
                "main_document_ids": paper.get("main_documents") or [],
            }
        )

    remapped = []
    for document in inventory:
        source_paper_id = document["paper_id"]
        remapped.append(
            {
                **document,
                "paper_id": mapping.get(source_paper_id, source_paper_id),
                "source_paper_id": source_paper_id,
            }
        )
    remapped_by_id = {row["document_id"]: row for row in remapped}
    for paper in owners:
        main = [remapped_by_id[value] for value in paper.get("main_documents") or []]
        main.sort(
            key=lambda row: (int(row.get("page_count") or 0), int(row.get("size_bytes") or 0)),
            reverse=True,
        )
        canonical = main[0]["document_id"] if main else None
        paper["main_documents"] = list(dict.fromkeys(paper.get("main_documents") or []))
        paper["supplementary_documents"] = list(
            dict.fromkeys(paper.get("supplementary_documents") or [])
        )
        for row in main:
            row["canonical_in_paper"] = row["document_id"] == canonical
            row["paper_version_duplicate_of"] = (
                None if row["document_id"] == canonical else canonical
            )
    return owners, remapped, duplicate_groups


def _same_identity(left, right, by_document):
    left_doi = _normalize_doi(left.get("doi"))
    right_doi = _normalize_doi(right.get("doi"))
    if left_doi and right_doi:
        return left_doi == right_doi
    left_title = normalize_title(left.get("title") or "")
    right_title = normalize_title(right.get("title") or "")
    if not left_title or not right_title:
        return False
    left_author = _paper_author(left, by_document)
    right_author = _paper_author(right, by_document)
    if left_title == right_title:
        return bool(left_author and right_author and left_author == right_author)
    if SequenceMatcher(None, left_title, right_title).ratio() < 0.985:
        return False
    return bool(left_author and right_author and left_author == right_author)


def _paper_author(paper, by_document):
    for document_id in paper.get("main_documents") or []:
        value = (by_document[document_id].get("pdf_metadata") or {}).get("Author")
        if value:
            return "".join(character for character in str(value).casefold() if character.isalnum())
    return ""


def _normalize_doi(value):
    return str(value or "").strip().casefold().removeprefix("https://doi.org/").removeprefix("doi:")


def _inventory_manifest_attachments(corpus_root, existing):
    root = Path(corpus_root).expanduser().resolve()
    existing_paths = {Path(row["source_path"]).resolve() for row in existing}
    output = []
    for manifest_path in root.rglob("paper.json"):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        paper_id = str(manifest.get("paper_id") or "")
        if not paper_id:
            continue
        for attachment in manifest.get("supplementary_documents") or []:
            relative = attachment.get("relative_path")
            if not relative:
                continue
            path = (manifest_path.parent / str(relative)).resolve()
            if path in existing_paths or not path.is_file() or path.suffix.casefold() == ".pdf":
                continue
            digest = sha256_file(path)
            output.append(
                {
                    "document_id": stable_id("doc", digest),
                    "paper_id": paper_id,
                    "source_path": str(path),
                    "relative_path": str(path.relative_to(root)),
                    "paper_relative_path": str(path.relative_to(manifest_path.parent)),
                    "paper_bundle_path": str(manifest_path.parent),
                    "file_name": path.name,
                    "sha256": digest,
                    "size_bytes": path.stat().st_size,
                    "page_count": None,
                    "pdf_metadata": {},
                    "document_role": "supplementary",
                    "doi": manifest.get("doi"),
                    "source_dataset": manifest.get("dataset"),
                    "source_record": manifest.get("source_record") or {},
                    "source_remote_uri": attachment.get("remote_uri"),
                    "mapping_evidence": "stage00_paper_manifest",
                    "duplicate_of": None,
                    "duplicate_of_source_path": None,
                    "inventory_status": "canonical",
                }
            )
            existing_paths.add(path)
    return output


def _remote_discovery(main_documents: list[dict[str, Any]]) -> dict[str, Any]:
    uris: list[str] = []
    for document in main_documents:
        source = document.get("source_record") or {}
        for key in ("supplementary_uris", "matched_remote_uris"):
            values = source.get(key) or []
            if isinstance(values, str):
                values = [values]
            uris.extend(str(value) for value in values)
    return {"matched_remote_uris": list(dict.fromkeys(uris))}


def _attachment_document(paper_id: str, attachment: dict[str, Any]) -> dict[str, Any]:
    path = Path(attachment["path"]).resolve()
    digest = attachment.get("sha256") or sha256_file(path)
    return {
        "document_id": stable_id("doc", digest),
        "paper_id": paper_id,
        "source_path": str(path),
        "file_name": path.name,
        "sha256": digest,
        "size_bytes": path.stat().st_size,
        "page_count": None,
        "document_role": "supplementary",
        "source_remote_uri": attachment.get("source_url"),
        "mapping_evidence": attachment.get("source"),
        "duplicate_of": None,
        "inventory_status": "canonical",
    }


def _valid_pdf(path: Path) -> bool:
    try:
        if not path.is_file():
            return False
        with path.open("rb") as handle:
            return handle.read(5) == b"%PDF-"
    except OSError:
        return False

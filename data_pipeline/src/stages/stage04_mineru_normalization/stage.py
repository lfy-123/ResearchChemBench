"""Stage 04: normalize Stage 03 passes with high-quality MinerU parsing."""

from __future__ import annotations

import copy
import os
import shutil
from pathlib import Path
from typing import Any

from src.contracts import decision_counts, record_header, write_json, write_jsonl
from src.integrations.mineru import run_mineru_queue
from src.stages.stage01_document_preparation.normalization import (
    assess_text_quality,
    materialize_document,
)
from src.stages.stage03_toolbox_resource_gate.stage import STAGE03_FORWARD_DECISIONS


def run_stage04(
    *,
    stage03_records: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    workspace: Path,
    run_id: str,
    document_ids: set[str] | None = None,
    existing_deep_documents: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    stage_root = workspace / "stage_04_mineru_deep_normalization"
    records = copy.deepcopy(stage03_records)
    records, deep_documents, deep_attempts = _deep_normalize_passed_papers(
        records=records,
        documents=documents,
        config=config,
        stage_root=stage_root,
        run_id=run_id,
        document_ids=document_ids,
        existing_deep_documents=existing_deep_documents or [],
    )
    write_jsonl(stage_root / "decisions.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage04"),
        "papers": len(records),
        "input_passed": sum(
            row.get("gate_decision", row.get("decision")) in STAGE03_FORWARD_DECISIONS
            for row in records
        ),
        "passed": sum(bool(row.get("passed")) for row in records),
        "decisions": decision_counts(records),
        "deep_normalized_documents": sum(
            row.get("selected_parser") == "mineru" and row.get("decision") == "pass"
            for row in deep_documents
        ),
        "deep_parse_failed_papers": sum(
            row.get("decision") == "deep_parse_failed" for row in records
        ),
        "mineru_intermediate_bytes_removed": sum(
            int(
                ((row.get("deep_normalization") or {}).get("intermediate_cleanup") or {}).get(
                    "bytes_removed", 0
                )
            )
            for row in deep_documents
        ),
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {
        "records": records,
        "documents": deep_documents,
        "deep_parse_attempts": deep_attempts,
        "summary": summary,
    }


def _deep_normalize_passed_papers(
    *,
    records,
    documents,
    config,
    stage_root,
    run_id,
    document_ids=None,
    existing_deep_documents=None,
):
    mineru = config.get("mineru") or {}
    passed_ids = {row["paper_id"] for row in records if row.get("passed")}
    selected = [
        row
        for row in documents
        if row.get("paper_id") in passed_ids and row.get("decision") == "pass"
    ]
    selected_by_id = {str(row["document_id"]): row for row in selected}
    requested_ids = (
        set(selected_by_id)
        if document_ids is None
        else {str(value) for value in document_ids if str(value) in selected_by_id}
    )
    existing_by_id = {
        str(row["document_id"]): row
        for row in (existing_deep_documents or [])
        if str(row.get("document_id") or "") in selected_by_id
        and str(row.get("document_id") or "") not in requested_ids
    }
    unresolved_by_paper: dict[str, list[str]] = {}
    for document_id in sorted(set(selected_by_id) - requested_ids - set(existing_by_id)):
        document = selected_by_id[document_id]
        unresolved_by_paper.setdefault(str(document["paper_id"]), []).append(document_id)
    if not passed_ids:
        _write_deep_normalization(stage_root, [], [])
        return records, [], []
    if not bool(mineru.get("enabled", False)):
        retained = [
            {
                **row,
                "deep_normalization": {
                    "status": "disabled",
                    "selected_parser": row.get("selected_parser"),
                },
            }
            for row in selected
        ]
        for record in records:
            if record.get("passed"):
                record["deep_normalization"] = {"status": "disabled"}
        _write_deep_normalization(stage_root, retained, [])
        return records, retained, []

    process_documents = [row for row in selected if str(row["document_id"]) in requested_ids]
    pdf_documents = [
        row
        for row in process_documents
        if Path(str(row.get("source_path") or "")).suffix.casefold() == ".pdf"
    ]
    queue = [
        {
            "document_id": row["document_id"],
            "paper_id": row["paper_id"],
            "source_path": row["source_path"],
            "title": row.get("title"),
            "expected_pages": row.get("page_count"),
            "deep_parse_decision": "required_after_stage03_gate",
            "priority_score": 1.0,
            "reason": ["stage03_toolbox_and_resource_gate_passed"],
        }
        for row in pdf_documents
    ]
    results = run_mineru_queue(
        queue,
        stage_root / "deep_normalization" / "raw" / "mineru",
        execute=True,
        command=str(mineru.get("command", "mineru")),
        method=str(mineru.get("method", "auto")),
        backend=mineru.get("backend", "pipeline"),
        timeout_seconds=int(mineru.get("timeout_seconds", 3000)),
        working_directory=mineru.get("working_directory"),
        environment=mineru.get("environment"),
        extra_args=mineru.get("extra_args") or ["--formula", "true", "--table", "true"],
        reuse_existing=bool(mineru.get("reuse_existing", True)),
        min_markdown_chars=int(mineru.get("min_markdown_chars", 100)),
        stage_name="stage_04_mineru_deep_normalization",
        max_workers=int(mineru.get("api_concurrency", 1)),
        request_batch_size=int(mineru.get("request_batch_size", 1)),
    )
    by_id = {row["document_id"]: row for row in results}
    deep_root = stage_root / "deep_normalization"
    mineru_raw_root = deep_root / "raw" / "mineru"
    cleanup_intermediates = bool(mineru.get("cleanup_successful_intermediates", True))
    deep_documents: list[dict[str, Any]] = list(existing_by_id.values())
    attempts: list[dict[str, Any]] = []
    failed_by_paper: dict[str, list[str]] = {}
    timed_out_by_paper: dict[str, list[str]] = {}
    quality_config = {
        "min_main_characters": int(mineru.get("min_main_characters", 1000)),
        "min_supplementary_characters": int(mineru.get("min_supplementary_characters", 100)),
        "min_readable_character_ratio": float(mineru.get("min_readable_character_ratio", 0.90)),
        "max_replacement_character_ratio": float(
            mineru.get("max_replacement_character_ratio", 0.01)
        ),
        "max_repeated_line_ratio": float(mineru.get("max_repeated_line_ratio", 0.50)),
        "min_page_coverage_ratio": float(mineru.get("min_page_coverage_ratio", 0.95)),
    }
    pdf_ids = {row["document_id"] for row in pdf_documents}
    for document in process_documents:
        if document["document_id"] not in pdf_ids:
            deep_documents.append(
                {
                    **document,
                    "deep_normalization": {
                        "status": "reused_stage01_non_pdf",
                        "selected_parser": document.get("selected_parser"),
                    },
                }
            )
            continue
        result = by_id.get(document["document_id"], {})
        text = _read_optional(result.get("markdown_path"))
        quality = assess_text_quality(
            text,
            document.get("page_count"),
            quality_config,
            document.get("document_role"),
            result,
        )
        status = str(result.get("status") or "missing")
        timed_out = status == "timeout"
        attempt = {
            "paper_id": document["paper_id"],
            "document_id": document["document_id"],
            "parser": "mineru",
            "status": status,
            "quality": quality,
            "error": result.get("error"),
            "output_path": result.get("markdown_path"),
            "duration_seconds": result.get("duration_seconds"),
            "retry_suppressed_reason": result.get("retry_suppressed_reason"),
        }
        attempts.append(attempt)
        if status in {"success", "reused"} and quality["passed"]:
            stable_result = _materialize_mineru_parser_outputs(
                result,
                deep_root=deep_root,
                document_id=str(document["document_id"]),
            )
            deep = materialize_document(
                document,
                text,
                "mineru",
                stable_result,
                quality,
                deep_root,
                run_id,
                stage_name="stage04",
            )
            cleanup = (
                _remove_successful_mineru_raw(
                    mineru_raw_root,
                    document_id=str(document["document_id"]),
                )
                if cleanup_intermediates
                else {"status": "retained_by_config", "bytes_removed": 0, "files_removed": 0}
            )
            deep["stage01_selected_parser"] = document.get("selected_parser")
            deep["deep_normalization"] = {
                "status": "completed",
                "selected_parser": "mineru",
                "intermediate_cleanup": cleanup,
            }
            attempt["output_path"] = deep["normalized_markdown_path"]
            attempt["intermediate_cleanup"] = cleanup
            deep_documents.append(deep)
            continue
        failed_by_paper.setdefault(document["paper_id"], []).append(document["document_id"])
        if timed_out:
            timed_out_by_paper.setdefault(document["paper_id"], []).append(
                document["document_id"]
            )
        deep_documents.append(
            {
                **document,
                **record_header(
                    run_id=run_id,
                    stage="stage04",
                    paper_id=document["paper_id"],
                    document_id=document["document_id"],
                ),
                "processing_status": "failed",
                "decision": "deep_parse_failed",
                "passed": False,
                "failure_disposition": "terminal" if timed_out else "retryable",
                "failure_class": "mineru_timeout" if timed_out else "mineru_parse_failed",
                "error": result.get("error"),
                "selected_parser": None,
                "quality": quality,
                "deep_normalization": {
                    "status": "failed",
                    "attempted_parser": "mineru",
                    "error": result.get("error"),
                },
            }
        )

    successful_main = {
        row["paper_id"]
        for row in deep_documents
        if row.get("decision") == "pass"
        and row.get("selected_parser") == "mineru"
        and row.get("document_role") != "supplementary"
    }
    for paper_id in passed_ids - successful_main - set(unresolved_by_paper):
        failed_by_paper.setdefault(paper_id, []).append("missing_successful_main_document")
    for record in records:
        if record.get("paper_id") not in passed_ids:
            continue
        failed_documents = sorted(set(failed_by_paper.get(record["paper_id"], [])))
        timed_out_documents = sorted(
            set(timed_out_by_paper.get(record["paper_id"], []))
        )
        pending_documents = sorted(set(unresolved_by_paper.get(record["paper_id"], [])))
        record["gate_decision"] = record["decision"]
        record["deep_normalization"] = {
            "status": (
                "failed" if failed_documents else "pending" if pending_documents else "completed"
            ),
            "failed_document_ids": failed_documents,
            "timed_out_document_ids": timed_out_documents,
            "pending_document_ids": pending_documents,
            "document_count": sum(
                row.get("paper_id") == record["paper_id"] for row in deep_documents
            ),
        }
        if failed_documents:
            record["decision"] = "deep_parse_failed"
            record["passed"] = False
            record["processing_status"] = "failed"
            record["failure_disposition"] = (
                "terminal" if timed_out_documents else "retryable"
            )
            record["failure_class"] = (
                "mineru_timeout" if timed_out_documents else "mineru_parse_failed"
            )
            if timed_out_documents:
                record["error"] = {
                    "error_type": "MinerUTimeout",
                    "message": (
                        "MinerU exceeded the configured timeout for document(s): "
                        + ", ".join(timed_out_documents)
                    ),
                }
        elif pending_documents:
            record["decision"] = "processing_pending"
            record["passed"] = False
            record["processing_status"] = "pending"
            record["failure_disposition"] = "pending"

    _write_deep_normalization(stage_root, deep_documents, attempts)
    return records, deep_documents, attempts


def _write_deep_normalization(stage_root, documents, attempts):
    root = stage_root / "deep_normalization"
    write_jsonl(root / "documents.jsonl", documents)
    write_jsonl(root / "parser_attempts.jsonl", attempts)
    write_jsonl(
        root / "failed.jsonl",
        [row for row in documents if row.get("decision") == "deep_parse_failed"],
    )


def _read_optional(value):
    if not value:
        return ""
    path = Path(str(value))
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


_MINERU_STRUCTURED_PATH_KEYS = (
    "content_list_v2_path",
    "content_list_path",
    "middle_json_path",
    "model_json_path",
)


def _materialize_mineru_parser_outputs(result, *, deep_root: Path, document_id: str):
    """Promote reusable MinerU results before its raw directory is removed."""

    stable = dict(result)
    target = (deep_root / "normalized" / document_id).resolve()
    target.mkdir(parents=True, exist_ok=True)
    structured_root = target / "parser_structured"
    promoted = []
    for key in _MINERU_STRUCTURED_PATH_KEYS:
        source_value = result.get(key)
        if not source_value:
            continue
        source = Path(str(source_value)).expanduser().resolve()
        if not source.is_file():
            continue
        structured_root.mkdir(parents=True, exist_ok=True)
        destination = structured_root / source.name
        _link_or_copy(source, destination)
        stable[key] = str(destination.resolve())
        promoted.append(str(destination.resolve()))

    markdown_value = result.get("markdown_path")
    if markdown_value:
        markdown = Path(str(markdown_value)).expanduser().resolve()
        images = markdown.parent / "images"
        if images.is_dir():
            destination = target / "images"
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(images, destination, copy_function=_link_or_copy)
            stable["images_path"] = str(destination.resolve())
            promoted.append(str(destination.resolve()))

    stable["markdown_path"] = str((target / "normalized_document.md").resolve())
    stable["output_dir"] = str(target)
    stable["promoted_artifacts"] = promoted
    return stable


def _link_or_copy(source, destination):
    """Hard-link local parser artifacts when possible, with a copy fallback."""

    source_path = Path(source)
    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if destination_path.exists() or destination_path.is_symlink():
        destination_path.unlink()
    try:
        os.link(source_path, destination_path)
    except OSError:
        shutil.copy2(source_path, destination_path)
    return str(destination_path)


def _remove_successful_mineru_raw(raw_root: Path, *, document_id: str):
    """Delete only the validated per-document MinerU raw directory."""

    root = raw_root.expanduser().resolve()
    candidate = (root / document_id).resolve()
    if candidate.parent != root or candidate.name != document_id:
        raise ValueError("refusing to remove a MinerU path outside the raw document root")
    if not candidate.exists():
        return {"status": "already_absent", "bytes_removed": 0, "files_removed": 0}
    files = [path for path in candidate.rglob("*") if path.is_file() and not path.is_symlink()]
    bytes_removed = sum(path.stat().st_size for path in files)
    shutil.rmtree(candidate)
    return {
        "status": "removed",
        "bytes_removed": bytes_removed,
        "files_removed": len(files),
    }

#!/usr/bin/env python3
"""Promote successful MinerU results and remove their reproducible raw outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[2]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from src.contracts import read_json, read_jsonl, write_json, write_jsonl  # noqa: E402
from src.stages.stage04_mineru_normalization.stage import (  # noqa: E402
    _materialize_mineru_parser_outputs,
    _remove_successful_mineru_raw,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument(
        "--report-path",
        type=Path,
        help="Optional report path relative to the run root",
    )
    args = parser.parse_args()

    run_root = args.run_root.expanduser().resolve()
    if not run_root.is_dir() or run_root.parent.name != "runs":
        raise ValueError("--run-root must be one direct child of data_pipeline/runs")

    report = {
        "run_root": str(run_root),
        "dry_run": args.dry_run,
        "stage_roots_scanned": 0,
        "successful_raw_directories": 0,
        "raw_directories_removed": 0,
        "logical_bytes_removed": 0,
        "files_removed": 0,
        "skipped": {},
        "errors": [],
    }
    processed = 0
    normalized_by_document: dict[str, str] = {}
    for stage_root in _stage_roots(run_root):
        report["stage_roots_scanned"] += 1
        documents_path = stage_root / "deep_normalization" / "documents.jsonl"
        documents = read_jsonl(documents_path)
        changed = False
        cleanup_by_document = {}
        for document in documents:
            document_id = str(document.get("document_id") or "")
            normalized = Path(str(document.get("normalized_markdown_path") or ""))
            if (
                document_id
                and document.get("decision") == "pass"
                and document.get("selected_parser") == "mineru"
                and normalized.is_file()
            ):
                normalized_by_document[document_id] = str(normalized.resolve())
            raw_root = stage_root / "deep_normalization" / "raw" / "mineru"
            raw_document = raw_root / document_id
            if not raw_document.is_dir():
                continue
            if document.get("decision") != "pass" or document.get("selected_parser") != "mineru":
                _increment(report["skipped"], "not_successful")
                continue
            blocks = Path(str(document.get("content_blocks_path") or ""))
            metadata_path = normalized.parent / "metadata.json"
            if not (normalized.is_file() and blocks.is_file() and metadata_path.is_file()):
                _increment(report["skipped"], "stable_results_missing")
                continue
            report["successful_raw_directories"] += 1
            processed += 1
            if args.dry_run:
                cleanup = _raw_stats(raw_document)
            else:
                try:
                    metadata = read_json(metadata_path)
                    parser_output = metadata.get("parser_output") or {}
                    stable = _materialize_mineru_parser_outputs(
                        parser_output,
                        deep_root=stage_root / "deep_normalization",
                        document_id=document_id,
                    )
                    required = Path(str(stable.get("content_list_v2_path") or ""))
                    if not required.is_file():
                        raise FileNotFoundError(
                            f"promoted content_list_v2 is missing for {document_id}"
                        )
                    metadata["parser_output"] = stable
                    write_json(metadata_path, metadata)
                    cleanup = _remove_successful_mineru_raw(
                        raw_root,
                        document_id=document_id,
                    )
                except Exception as exc:
                    report["errors"].append(
                        {
                            "document_id": document_id,
                            "stage_root": str(stage_root),
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    continue
                cleanup_by_document[document_id] = cleanup
                document.setdefault("deep_normalization", {})[
                    "intermediate_cleanup"
                ] = cleanup
                changed = True
            report["raw_directories_removed"] += int(cleanup["status"] == "removed")
            report["logical_bytes_removed"] += int(cleanup.get("bytes_removed", 0))
            report["files_removed"] += int(cleanup.get("files_removed", 0))
            if args.progress_every > 0 and processed % args.progress_every == 0:
                print(
                    f"processed={processed} removed={report['raw_directories_removed']} "
                    f"logical_gib={report['logical_bytes_removed'] / 2**30:.3f}",
                    flush=True,
                )
        if changed:
            write_jsonl(documents_path, documents)
            _update_attempts(stage_root, cleanup_by_document)
            _update_summary(stage_root, cleanup_by_document)

    report["aggregate_attempt_paths_updated"] = (
        0
        if args.dry_run
        else _update_aggregate_attempts(run_root, normalized_by_document)
    )

    report_path = (
        (run_root / args.report_path).resolve()
        if args.report_path
        else run_root
        / "logs"
        / (
            "mineru_intermediate_cleanup.dry-run.json"
            if args.dry_run
            else "mineru_intermediate_cleanup.json"
        )
    )
    if run_root not in report_path.parents:
        raise ValueError("--report-path must remain inside --run-root")
    write_json(report_path, report)
    print(json.dumps({**report, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


def _stage_roots(run_root: Path):
    pattern = (
        "batches/*/microbatches/*/resume_attempts/generation-*/stage04/"
        "stage_04_mineru_deep_normalization"
    )
    return sorted(path for path in run_root.glob(pattern) if path.is_dir())


def _raw_stats(raw_document: Path):
    files = [
        path for path in raw_document.rglob("*") if path.is_file() and not path.is_symlink()
    ]
    return {
        "status": "dry_run",
        "bytes_removed": sum(path.stat().st_size for path in files),
        "files_removed": len(files),
    }


def _update_attempts(stage_root: Path, cleanup_by_document: dict[str, dict]) -> None:
    path = stage_root / "deep_normalization" / "parser_attempts.jsonl"
    rows = read_jsonl(path)
    changed = False
    for row in rows:
        cleanup = cleanup_by_document.get(str(row.get("document_id") or ""))
        if cleanup is None:
            continue
        normalized = (
            stage_root
            / "deep_normalization"
            / "normalized"
            / str(row["document_id"])
            / "normalized_document.md"
        )
        row["output_path"] = str(normalized.resolve())
        row["intermediate_cleanup"] = cleanup
        changed = True
    if changed:
        write_jsonl(path, rows)


def _update_aggregate_attempts(run_root: Path, normalized_by_document: dict[str, str]) -> int:
    updated = 0
    pattern = (
        "batches/**/stage_04_mineru_deep_normalization/"
        "deep_normalization/parser_attempts.jsonl"
    )
    for path in sorted(run_root.glob(pattern)):
        rows = read_jsonl(path)
        changed = False
        for row in rows:
            normalized = normalized_by_document.get(str(row.get("document_id") or ""))
            if not normalized or row.get("output_path") == normalized:
                continue
            row["output_path"] = normalized
            changed = True
            updated += 1
        if changed:
            write_jsonl(path, rows)
    return updated


def _update_summary(stage_root: Path, cleanup_by_document: dict[str, dict]) -> None:
    path = stage_root / "stage_summary.json"
    if not path.is_file():
        return
    summary = read_json(path)
    summary["mineru_intermediate_bytes_removed"] = sum(
        int(value.get("bytes_removed", 0)) for value in cleanup_by_document.values()
    )
    write_json(path, summary)


def _increment(counter: dict[str, int], key: str) -> None:
    counter[key] = counter.get(key, 0) + 1


if __name__ == "__main__":
    raise SystemExit(main())

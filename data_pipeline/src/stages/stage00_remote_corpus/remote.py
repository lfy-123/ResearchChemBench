from __future__ import annotations

import json
import os
import hashlib
import heapq
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Protocol

from src.core.io import read_json, sha256_file, stable_id, write_json, write_jsonl
from src.core.logging import log_progress
from src.integrations.xinghe import XingheObjectStore

STAGE00_SCHEMA_VERSION = 2


DATASETS: dict[str, dict[str, str]] = {
    "en-paper-hzzj": {
        "root": "s3://private-cooperate-data/en-paper-hzzj/",
        "pdf_prefix": "s3://private-cooperate-data/en-paper-hzzj/pdf/",
        "supplementary_prefix": "s3://private-cooperate-data/en-paper-hzzj/support/",
        "metadata_uri": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/"
            "物质科学类化学核心期刊_935168_0602.jsonl"
        ),
        "metadata_root": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/"
        ),
    },
    "kps-20260603-bu": {
        "root": "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/",
        "pdf_prefix": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/pdf/"
        ),
        "supplementary_prefix": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/support/"
        ),
        "metadata_uri": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/"
            "物质科学类化学核心期刊_935168_0602.jsonl"
        ),
        "metadata_root": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/"
        ),
    },
    "kps-2026-06-18": {
        "root": "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/",
        "pdf_prefix": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/pdf/"
        ),
        "supplementary_prefix": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/support/"
        ),
        "metadata_uri": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/"
            "物质化学期刊_99_0617.jsonl"
        ),
        "metadata_root": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/"
        ),
    },
    "kps-2026-05-07": {
        "root": "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/",
        "pdf_prefix": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/pdf/"
        ),
        "supplementary_prefix": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/support/"
        ),
        "metadata_uri": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/"
            "物质科学类化学核心期刊_935168_0507.jsonl"
        ),
        "metadata_root": (
            "s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/"
        ),
        "supplementary_discovery": "metadata_verified",
    },
}


class ObjectStore(Protocol):
    def iter_uris(self, prefix: str, *, start_after: str | None = None): ...

    def iter_jsonl(self, uri: str): ...

    def stat(self, uri: str) -> dict[str, Any]: ...

    def copy_to(self, uri: str, destination: str | Path) -> dict[str, Any]: ...


def prepare_remote_corpus(
    output_dir: str | Path,
    *,
    dataset: str,
    count: int,
    credentials: str | Path | None = None,
    outside: bool = False,
    resume: bool = True,
    copy_supplementary: bool = True,
    selection: str = "remote_order",
    seed: int = 0,
    exclude_selected_manifests: list[str | Path] | None = None,
    store: ObjectStore | None = None,
    resume_store=None,
    outer_batch_id: str | None = None,
    target_slot_start: int = 1,
    retry_only: bool = False,
) -> dict[str, Any]:
    if count < 1:
        raise ValueError("Stage 00 count must be at least 1")
    spec = _dataset_spec(dataset)
    root = Path(output_dir).expanduser().resolve()
    corpus = root / "corpus"
    corpus.mkdir(parents=True, exist_ok=True)
    cursor_path = root / "cursor.json"
    selected_path = root / "selected_papers.jsonl"
    existing = _read_rows(selected_path) if resume else []
    if existing and any(
        int(item.get("schema_version") or 0) != STAGE00_SCHEMA_VERSION
        for item in existing
    ):
        raise RuntimeError(
            f"{root} contains legacy Stage 00 records. Use a new output directory "
            "so supplementary-material mappings are rebuilt from the remote inventory."
        )
    if existing and any(item.get("dataset") != dataset for item in existing):
        raise RuntimeError(f"{root} already contains a different Stage 00 dataset")
    if selection not in {"remote_order", "seeded_sample"}:
        raise ValueError("Stage 00 selection must be remote_order or seeded_sample")
    if existing:
        existing = _reconcile_existing_records(
            existing[:count],
            corpus=corpus,
            dataset=dataset,
            store=store,
            credentials=credentials,
            outside=outside,
            resume_store=resume_store,
            spec=spec,
            copy_supplementary=copy_supplementary,
        )
        write_jsonl(selected_path, existing)
    if len(existing) >= count:
        return _stage_result(root, dataset, existing, reused=True)
    if store is None:
        if credentials is None:
            raise ValueError("Stage 00 credentials are required for remote access")
        store = XingheObjectStore(credentials, outside=outside)

    cursor = read_json(cursor_path) if resume and cursor_path.is_file() else {}
    start_after = cursor.get("last_main_uri")
    needed = count - len(existing)
    excluded_main_uris = _excluded_main_uris(exclude_selected_manifests or [])
    excluded_main_uris.update(
        str((row.get("main_document") or {}).get("remote_uri") or "")
        for row in existing
    )
    excluded_main_uris.discard("")
    if resume_store is not None:
        excluded_main_uris.update(resume_store.selected_main_uris(dataset))
    retry_rows = []
    if resume_store is not None:
        retry_rows = [
            row
            for row in resume_store.selections_for_batch(str(outer_batch_id or root.name))
            if int(row["target_slot_ordinal"]) >= int(target_slot_start) + len(existing)
            and int(row["target_slot_ordinal"]) < int(target_slot_start) + count
            and str(row.get("copy_state") or "")
            in {"reserved", "copy_retryable_failed"}
        ]
        retry_rows.sort(key=lambda row: int(row["target_slot_ordinal"]))
    retry_uris = [str(row["source_main_uri"]) for row in retry_rows[:needed]]
    new_needed = 0 if retry_only else needed - len(retry_uris)
    selected_uris = [
        *retry_uris,
        *_select_main_uris(
        store,
        spec["pdf_prefix"],
        count=new_needed,
        selection=selection,
        seed=seed,
        start_after=start_after,
        excluded_main_uris=excluded_main_uris | set(retry_uris),
        ),
    ]
    if not retry_only and len(selected_uris) < needed:
        raise RuntimeError(
            f"Stage 00 found only {len(selected_uris)} new PDFs; {needed} are required"
        )

    metadata = _metadata_for_selected(store, spec, selected_uris)
    supplementary_index, supplementary_inventory, supplementary_failures = _supplementary_for_selected(
        store,
        spec,
        selected_uris,
        metadata,
    )
    rows = list(existing)
    events = _read_rows(root / "copy_events.jsonl") if resume else []
    for index, main_uri in enumerate(selected_uris, start=len(existing) + 1):
        item = metadata.get(_basename(main_uri).casefold(), {})
        selection_row = None
        if resume_store is not None:
            slot = int(target_slot_start) + index - 1
            selection_row = resume_store.selection_for_slot(slot)
            if selection_row is not None:
                if str(selection_row["source_main_uri"]) != main_uri:
                    raise RuntimeError(
                        f"Stage00 target slot {slot} is reserved for "
                        f"{selection_row['source_main_uri']}, not {main_uri}"
                    )
            else:
                selection_row = resume_store.reserve_selection(
                    dataset=dataset,
                    source_main_uri=main_uri,
                    normalized_doi=_normalize_doi(
                        item.get("doi") or _doi_from_filename(_basename(main_uri))
                    ),
                    source_record_key=str(
                        item.get("relative_path")
                        or item.get("pdf_filename")
                        or _basename(main_uri)
                    ),
                    paper_id=None,
                    target_slot_ordinal=slot,
                    outer_batch_id=str(outer_batch_id or root.name),
                )
        try:
            record, paper_events = _materialize_paper(
                store,
                corpus,
                dataset=dataset,
                selection_index=index,
                main_uri=main_uri,
                metadata=item,
                supplementary_uris=supplementary_index.get(
                    _main_document_key(_basename(main_uri)), []
                ),
                supplementary_inventory=supplementary_inventory,
                supplementary_verification_failures=supplementary_failures.get(
                    _main_document_key(_basename(main_uri)), []
                ),
                copy_supplementary=copy_supplementary,
            )
        except Exception as exc:
            if resume_store is not None and selection_row is not None:
                resume_store.update_selection_copy(
                    str(selection_row["selection_id"]),
                    copy_state="copy_retryable_failed",
                    local_assets_state="missing_required",
                    error={"error_type": type(exc).__name__, "message": str(exc)},
                )
            raise
        if resume_store is not None and selection_row is not None:
            resume_store.update_selection_copy(
                str(selection_row["selection_id"]),
                copy_state=(
                    "materialized"
                    if record.get("copy_status") == "complete"
                    else "copy_retryable_failed"
                ),
                paper_id=record.get("paper_id"),
                source_sha256=(record.get("main_document") or {}).get("sha256"),
                local_assets_state="available",
                error={
                    "supplementary_copy_failures": record.get(
                        "supplementary_copy_failures"
                    )
                    or []
                },
            )
        rows.append(record)
        events.extend(paper_events)
        write_jsonl(selected_path, rows)
        write_jsonl(root / "copy_events.jsonl", events)
        write_json(
            cursor_path,
            {
                "schema_version": STAGE00_SCHEMA_VERSION,
                "dataset": dataset,
                "selection": selection,
                "seed": seed if selection == "seeded_sample" else None,
                "last_main_uri": main_uri,
                "selected_papers": len(rows),
                "excluded_main_uris": len(excluded_main_uris),
                "exclude_selected_manifests": [
                    str(Path(path).expanduser().resolve())
                    for path in (exclude_selected_manifests or [])
                ],
                "updated_at": _now(),
            },
        )
        log_progress("stage_00_remote_corpus", index, count, record["paper_id"], status=record["copy_status"])
    return _stage_result(root, dataset, rows, reused=False)


def _reconcile_existing_records(
    rows,
    *,
    corpus,
    dataset,
    store,
    credentials,
    outside,
    resume_store,
    spec,
    copy_supplementary,
):
    if not rows:
        return rows
    missing = []
    for row in rows:
        bundle = corpus / str(row["paper_id"])
        if _materialized_record_is_complete(row, bundle):
            continue
        selection = resume_store.selection_for_paper(str(row["paper_id"])) if resume_store else None
        if selection and selection.get("local_assets_state") == "pruned_terminal":
            continue
        missing.append(row)
    if not missing:
        return rows
    if store is None:
        if credentials is None:
            raise ValueError("Stage 00 credentials are required to restore missing assets")
        store = XingheObjectStore(credentials, outside=outside)
    selected_uris = [str((row.get("main_document") or {}).get("remote_uri") or "") for row in missing]
    metadata = _metadata_for_selected(store, spec, selected_uris)
    supplementary_index, supplementary_inventory, supplementary_failures = _supplementary_for_selected(
        store, spec, selected_uris, metadata
    )
    replacements = {str(row["paper_id"]): row for row in rows}
    for old in missing:
        main_uri = str((old.get("main_document") or {}).get("remote_uri") or "")
        item = metadata.get(_basename(main_uri).casefold(), old.get("source_record") or {})
        record, _events = _materialize_paper(
            store,
            corpus,
            dataset=dataset,
            selection_index=int(old.get("selection_index") or 0),
            main_uri=main_uri,
            metadata=item,
            supplementary_uris=supplementary_index.get(
                _main_document_key(_basename(main_uri)), []
            ),
            supplementary_inventory=supplementary_inventory,
            supplementary_verification_failures=supplementary_failures.get(
                _main_document_key(_basename(main_uri)), []
            ),
            copy_supplementary=copy_supplementary,
        )
        replacements[str(old["paper_id"])] = record
        if resume_store is not None:
            selection = resume_store.selection_for_paper(str(old["paper_id"]))
            if selection:
                resume_store.update_selection_copy(
                    str(selection["selection_id"]),
                    copy_state="materialized",
                    paper_id=record["paper_id"],
                    source_sha256=(record.get("main_document") or {}).get("sha256"),
                    local_assets_state="available",
                )
    return [replacements[str(row["paper_id"])] for row in rows]


def _dataset_spec(dataset: str) -> dict[str, str]:
    if dataset in DATASETS:
        return dict(DATASETS[dataset])
    if dataset.startswith("s3://"):
        prefix = dataset.rstrip("/") + "/"
        return {"root": prefix, "pdf_prefix": prefix}
    raise ValueError(f"unknown Stage 00 dataset: {dataset}")


def _select_main_uris(
    store: ObjectStore,
    prefix: str,
    *,
    count: int,
    selection: str,
    seed: int,
    start_after: str | None,
    excluded_main_uris: set[str] | None = None,
) -> list[str]:
    if count <= 0:
        return []
    excluded = excluded_main_uris or set()
    if selection == "remote_order":
        output: list[str] = []
        for uri in store.iter_uris(prefix, start_after=start_after):
            if uri.casefold().endswith(".pdf") and uri not in excluded:
                output.append(uri)
            if len(output) >= count:
                break
        return output
    # A hash priority is stable across incremental calls. Selecting the first N
    # unreserved objects therefore extends a seeded sample without reordering
    # any target slot already frozen in the selection ledger.
    heap: list[tuple[int, str]] = []
    for uri in store.iter_uris(prefix):
        if not uri.casefold().endswith(".pdf") or uri in excluded:
            continue
        priority = int.from_bytes(
            hashlib.sha256(f"{seed}\x00{uri}".encode("utf-8")).digest(), "big"
        )
        candidate = (-priority, uri)
        if len(heap) < count:
            heapq.heappush(heap, candidate)
        elif candidate > heap[0]:
            heapq.heapreplace(heap, candidate)
    return [uri for _priority, uri in sorted(heap, key=lambda item: (-item[0], item[1]))]


def _excluded_main_uris(manifests: list[str | Path]) -> set[str]:
    output: set[str] = set()
    for manifest in manifests:
        path = Path(manifest).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Stage 00 exclusion manifest does not exist: {path}")
        for row in _read_rows(path):
            uri = str(
                (row.get("main_document") or {}).get("remote_uri")
                or row.get("main_uri")
                or ""
            ).strip()
            if uri:
                output.add(uri)
    return output


def _metadata_for_selected(
    store: ObjectStore, spec: dict[str, str], selected_uris: list[str]
) -> dict[str, dict[str, Any]]:
    metadata_uri = spec.get("metadata_uri")
    if not metadata_uri:
        return {}
    wanted = {_basename(uri).casefold() for uri in selected_uris}
    output: dict[str, dict[str, Any]] = {}
    for row in store.iter_jsonl(metadata_uri):
        name = str(row.get("pdf_filename") or PurePosixPath(str(row.get("relative_path") or "")).name)
        key = name.casefold()
        if key in wanted:
            output[key] = row
            if len(output) == len(wanted):
                break
    return output


def _supplementary_for_selected(
    store: ObjectStore,
    spec: dict[str, str],
    selected_uris: list[str],
    metadata: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, list[str]], dict[str, Any], dict[str, list[dict[str, str]]]
]:
    prefix = spec.get("supplementary_prefix")
    wanted = {_main_document_key(_basename(uri)) for uri in selected_uris}
    output: dict[str, list[str]] = {key: [] for key in wanted}
    failures: dict[str, list[dict[str, str]]] = {key: [] for key in wanted}
    if not prefix:
        return output, {
            "method": "no_supplementary_prefix",
            "prefix": None,
            "objects_scanned": 0,
            "matched_objects": 0,
            "matched_papers": 0,
        }, failures
    if spec.get("supplementary_discovery") == "metadata_verified":
        checked = 0
        matched = 0
        metadata_root = spec.get("metadata_root") or spec["root"]
        for main_uri in selected_uris:
            basename = _basename(main_uri)
            owner = _main_document_key(basename)
            row = metadata.get(basename.casefold(), {})
            for raw in _support_paths(row.get("support_path")):
                checked += 1
                uri = _support_uri(metadata_root, raw)
                if not uri.startswith(prefix.rstrip("/") + "/"):
                    failures[owner].append(
                        {
                            "remote_uri": uri,
                            "error": "metadata support URI is outside the dataset supplementary prefix",
                        }
                    )
                    continue
                try:
                    store.stat(uri)
                except Exception as exc:
                    failures[owner].append(
                        {
                            "remote_uri": uri,
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    continue
                if _supplementary_owner_key(_basename(uri)) != owner:
                    failures[owner].append(
                        {
                            "remote_uri": uri,
                            "error": "metadata support filename does not match main document",
                        }
                    )
                    continue
                output[owner].append(uri)
                matched += 1
        for values in output.values():
            values.sort()
        return output, {
            "method": "metadata_candidates_verified_by_remote_stat",
            "prefix": prefix,
            "objects_scanned": checked,
            "matched_objects": matched,
            "matched_papers": sum(bool(values) for values in output.values()),
            "verification_failures": sum(len(values) for values in failures.values()),
        }, failures
    scanned = 0
    matched = 0
    for uri in store.iter_uris(prefix):
        scanned += 1
        owner = _supplementary_owner_key(_basename(uri))
        if owner not in wanted:
            continue
        output[owner].append(uri)
        matched += 1
    for values in output.values():
        values.sort()
    return output, {
        "method": "remote_inventory_doi_filename",
        "prefix": prefix,
        "objects_scanned": scanned,
        "matched_objects": matched,
        "matched_papers": sum(bool(values) for values in output.values()),
    }, failures


def _materialize_paper(
    store: ObjectStore,
    corpus: Path,
    *,
    dataset: str,
    selection_index: int,
    main_uri: str,
    metadata: dict[str, Any],
    supplementary_uris: list[str],
    supplementary_inventory: dict[str, Any],
    supplementary_verification_failures: list[dict[str, str]],
    copy_supplementary: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    doi = _normalize_doi(metadata.get("doi") or _doi_from_filename(_basename(main_uri)))
    paper_id = stable_id("paper", doi or main_uri, length=16)
    final_dir = corpus / paper_id
    if final_dir.is_dir() and (final_dir / "paper.json").is_file():
        record = read_json(final_dir / "paper.json")
        if int(record.get("schema_version") or 0) != STAGE00_SCHEMA_VERSION:
            raise RuntimeError(
                f"{final_dir} contains a legacy Stage 00 paper bundle; use a new "
                "output directory"
            )
        if record.get("main_document", {}).get("remote_uri") != main_uri:
            raise RuntimeError(f"Stage 00 paper directory collision: {final_dir}")
        if _materialized_record_is_complete(record, final_dir):
            return record, []
        shutil.rmtree(final_dir)
    partial = corpus / f".{paper_id}.partial"
    if partial.exists():
        shutil.rmtree(partial)
    (partial / "main").mkdir(parents=True)
    (partial / "supplementary").mkdir(parents=True)
    events: list[dict[str, Any]] = []
    main_name = _safe_name(_basename(main_uri))
    main_target = partial / "main" / main_name
    main_stat = store.copy_to(main_uri, main_target)
    main_doc = _document_record(main_uri, main_target, partial, main_stat, "main_paper")
    events.append(_copy_event(paper_id, main_doc, "copied"))

    supplementary: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    if copy_supplementary:
        for position, uri in enumerate(supplementary_uris, start=1):
            target = partial / "supplementary" / _safe_name(
                _basename(uri) or f"si-{position}.pdf"
            )
            try:
                stat = store.copy_to(uri, target)
                document = _document_record(uri, target, partial, stat, "supplementary")
                supplementary.append(document)
                events.append(_copy_event(paper_id, document, "copied"))
            except Exception as exc:
                failures.append({"remote_uri": uri, "error": f"{type(exc).__name__}: {exc}"})
                events.append({"paper_id": paper_id, "remote_uri": uri, "status": "failed", "error": failures[-1]["error"]})
    record = {
        "schema_version": STAGE00_SCHEMA_VERSION,
        "dataset": dataset,
        "paper_id": paper_id,
        "doi": doi or None,
        "title": metadata.get("title"),
        "journal_name": metadata.get("journal_name"),
        "issn": metadata.get("issn"),
        "article_url": metadata.get("article_url"),
        "source_record": {key: metadata.get(key) for key in ("relative_path", "pdf_filename", "support_path")},
        "supplementary_discovery": {
            "method": supplementary_inventory.get("method"),
            "inventory_prefix": supplementary_inventory.get("prefix"),
            "matched_remote_uris": supplementary_uris,
            "metadata_support_hints": _support_paths(metadata.get("support_path")),
            "verification_failures": supplementary_verification_failures,
            "status": "found" if supplementary_uris else "not_found",
        },
        "selection_index": selection_index,
        "main_document": main_doc,
        "supplementary_documents": supplementary,
        "supplementary_copy_failures": failures,
        "copy_status": "partial" if failures else "complete",
        "supplementary_copy_status": (
            "failed"
            if failures and not supplementary
            else "partial"
            if failures
            else "copied"
            if supplementary
            else "not_found"
        ),
        "copied_at": _now(),
    }
    write_json(partial / "paper.json", record)
    os.replace(partial, final_dir)
    record = _rebase_record_paths(record, final_dir)
    write_json(final_dir / "paper.json", record)
    return record, events


def _document_record(
    uri: str, path: Path, bundle_root: Path, stat: dict[str, Any], role: str
) -> dict[str, Any]:
    return {
        "remote_uri": uri,
        "relative_path": str(path.relative_to(bundle_root)),
        "file_name": path.name,
        "document_role": role,
        "size_bytes": path.stat().st_size,
        "etag": stat.get("etag"),
        "sha256": sha256_file(path),
    }


def _rebase_record_paths(record: dict[str, Any], _final_dir: Path) -> dict[str, Any]:
    return record


def _materialized_record_is_complete(record: dict[str, Any], root: Path) -> bool:
    if record.get("copy_status") != "complete":
        return False
    documents = [
        record.get("main_document") or {},
        *(record.get("supplementary_documents") or []),
    ]
    for document in documents:
        relative = str(document.get("relative_path") or "")
        path = root / relative
        if not relative or not path.is_file():
            return False
        expected = str(document.get("sha256") or "")
        if expected and sha256_file(path) != expected:
            return False
    return True


def _stage_result(root: Path, dataset: str, rows: list[dict[str, Any]], *, reused: bool) -> dict[str, Any]:
    summary = {
        "schema_version": STAGE00_SCHEMA_VERSION,
        "dataset": dataset,
        "papers": len(rows),
        "main_documents": len(rows),
        "supplementary_documents": sum(len(item.get("supplementary_documents") or []) for item in rows),
        "complete": sum(item.get("copy_status") == "complete" for item in rows),
        "partial": sum(item.get("copy_status") == "partial" for item in rows),
        "papers_with_supplementary": sum(
            bool(item.get("supplementary_documents")) for item in rows
        ),
        "papers_without_supplementary": sum(
            not item.get("supplementary_documents") for item in rows
        ),
        "supplementary_copy_failures": sum(
            len(item.get("supplementary_copy_failures") or []) for item in rows
        ),
        "reused": reused,
        "corpus_root": str(root / "corpus"),
    }
    write_json(root / "stage_summary.json", summary)
    write_jsonl(root / "source_manifest.jsonl", rows)
    return {"records": rows, "summary": summary, "corpus_root": str(root / "corpus")}


def _read_rows(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            output.append(json.loads(raw))
    return output


def _support_paths(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        return [text]
    return []


def _support_uri(root: str, path: str) -> str:
    if path.startswith("s3://"):
        return path
    return root.rstrip("/") + "/" + path.lstrip("/")


def _main_document_key(name: str) -> str:
    return Path(name).stem.casefold()


def _supplementary_owner_key(name: str) -> str:
    stem = Path(name).stem.casefold()
    match = re.fullmatch(r"(.+)_sup_[0-9]+(?:_.+)?", stem)
    return match.group(1) if match else ""


def _normalize_doi(value: Any) -> str:
    text = str(value or "").strip().casefold()
    return text.removeprefix("https://doi.org/").removeprefix("doi:")


def _doi_from_filename(name: str) -> str:
    stem = name[:-4] if name.casefold().endswith(".pdf") else name
    return stem.replace("_", "/", 1) if stem.startswith("10.") else ""


def _safe_name(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._()-]+", "_", value).strip("._")
    return (name or "document.pdf")[:220]


def _basename(uri: str) -> str:
    return PurePosixPath(uri).name


def _copy_event(paper_id: str, document: dict[str, Any], status: str) -> dict[str, Any]:
    return {"paper_id": paper_id, "remote_uri": document["remote_uri"], "role": document["document_role"], "status": status, "sha256": document["sha256"]}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

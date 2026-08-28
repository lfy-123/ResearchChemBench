from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from src.config import load_config
from src.contracts import canonical_hash
from src.core.io import read_jsonl, write_json
from src.core.resume import (
    FINAL_STATUSES,
    ResumeStateStore,
    document_input_fingerprint,
    input_fingerprint,
    paper_input_fingerprint,
    result_artifacts,
    scientific_stage_fingerprints,
    stable_input_value,
)

STAGE_FILES = {
    "stage01": (
        "stage_01_document_preparation/documents.jsonl",
        "stage_01_document_preparation/paper_bundles.jsonl",
    ),
    "stage02": ("stage_02_computational_content/decisions.jsonl",),
    "stage03": ("stage_03_toolbox_resource_gate/decisions.jsonl",),
    "stage04": (
        "stage_04_mineru_deep_normalization/deep_normalization/documents.jsonl",
        "stage_04_mineru_deep_normalization/decisions.jsonl",
    ),
    "stage05": ("stage_05_benchmark_suitability/decisions.jsonl",),
}
LEGACY_IMPORT_VERSION = 2


def import_legacy_run(
    run_root: str | Path,
    store: ResumeStateStore,
    *,
    generation: int = 0,
) -> dict[str, Any]:
    """Idempotently import old JSON/JSONL artifacts into the resume fact store."""

    root = Path(run_root).expanduser().resolve()
    batch_dirs = sorted((root / "batches").glob("batch-[0-9][0-9][0-9][0-9]"))
    reports = []
    slot_offset = 0
    for batch_dir in batch_dirs:
        config_path = root / "configs" / f"{batch_dir.name}.json"
        if not config_path.is_file():
            reports.append({"batch": batch_dir.name, "status": "missing_config"})
            continue
        config = _legacy_scientific_config(batch_dir, config_path)
        frozen_path = store.root / "config_snapshots" / f"{batch_dir.name}.json"
        if not frozen_path.is_file():
            write_json(frozen_path, _serializable_config(config))
        fingerprints = scientific_stage_fingerprints(config)
        configured_count = int((config.get("stage00") or {}).get("count", 0))
        import_key = f"legacy-v{LEGACY_IMPORT_VERSION}:{batch_dir.name}"
        source_signature = _legacy_source_signature(batch_dir, config_path)
        event = store.import_event(import_key)
        if event is not None and event.get("source_sha256") == source_signature:
            reports.append(
                {
                    "batch": batch_dir.name,
                    "status": "already_imported",
                    "configured_slots": configured_count,
                    "selections": 0,
                    "stage_rows": 0,
                }
            )
            slot_offset += configured_count
            continue
        selected_path = batch_dir / "stage_00_remote_corpus" / "selected_papers.jsonl"
        if not selected_path.is_file():
            selected_path = batch_dir / "stage_00_remote_corpus" / "source_manifest.jsonl"
        selected = read_jsonl(selected_path) if selected_path.is_file() else []
        imported_selections = 0
        imported_rows = 0
        for position, row in enumerate(selected, start=1):
            main = row.get("main_document") or {}
            uri = str(main.get("remote_uri") or "").strip()
            if not uri:
                continue
            selection = store.import_selection(
                dataset=str(row.get("dataset") or (config.get("stage00") or {}).get("dataset") or "unknown"),
                source_main_uri=uri,
                normalized_doi=row.get("doi"),
                source_record_key=(row.get("source_record") or {}).get("relative_path"),
                paper_id=row.get("paper_id"),
                target_slot_ordinal=slot_offset + position,
                outer_batch_id=batch_dir.name,
                replaces_selection_id=None,
            )
            local_dir = batch_dir / "stage_00_remote_corpus" / "corpus" / str(row["paper_id"])
            local_state = (
                "available"
                if local_dir.is_dir()
                else "pruned_terminal"
                if _registry_marks_deleted(config, str(row["paper_id"]))
                else "missing_required"
            )
            store.update_selection_copy(
                str(selection["selection_id"]),
                copy_state="materialized" if row.get("copy_status") == "complete" else "copy_retryable_failed",
                paper_id=str(row.get("paper_id") or "") or None,
                source_sha256=main.get("sha256"),
                local_assets_state=local_state,
                error={"supplementary_copy_failures": row.get("supplementary_copy_failures") or []},
            )
            if not store.has_work_history(
                outer_batch_id=batch_dir.name,
                stage="stage00",
                paper_id=str(row["paper_id"]),
            ):
                store.record_result(
                generation=generation,
                outer_batch_id=batch_dir.name,
                stage="stage00",
                paper_id=str(row["paper_id"]),
                document_id=None,
                config_fingerprint=fingerprints["stage00"],
                input_fingerprint=input_fingerprint({"remote_uri": uri}),
                row={
                    **row,
                    "processing_status": "completed" if row.get("copy_status") == "complete" else "failed",
                    "decision": "copied" if row.get("copy_status") == "complete" else "copy_incomplete",
                    "passed": row.get("copy_status") == "complete",
                },
                artifacts=(),
                imported=True,
            )
            imported_selections += 1

        package_path = batch_dir / "stage_01_document_preparation" / "package" / "papers.jsonl"
        if package_path.is_file():
            for row in read_jsonl(package_path):
                if store.has_work_history(
                    outer_batch_id=batch_dir.name,
                    stage="stage01_package",
                    paper_id=str(row["paper_id"]),
                ):
                    continue
                store.record_result(
                    generation=generation,
                    outer_batch_id=batch_dir.name,
                    stage="stage01_package",
                    paper_id=str(row["paper_id"]),
                    document_id=None,
                    config_fingerprint=fingerprints["stage01_package"],
                    input_fingerprint="",
                    row=row,
                    artifacts=(),
                    imported=True,
                )
                imported_rows += 1

        candidates: dict[tuple[str, str, str], tuple[str, float, dict[str, Any]]] = {}
        roots = [batch_dir, *sorted((batch_dir / "microbatches").glob("batch-*"))]
        for artifact_root in roots:
            for stage, relative_paths in STAGE_FILES.items():
                for relative in relative_paths:
                    path = artifact_root / relative
                    if not path.is_file():
                        continue
                    mtime = path.stat().st_mtime
                    for row in read_jsonl(path):
                        paper_id = str(row.get("paper_id") or "")
                        if not paper_id:
                            continue
                        document_id = str(row.get("document_id") or "")
                        key = (stage, paper_id, document_id)
                        created = str(row.get("created_at") or "")
                        score = (created, mtime)
                        previous = candidates.get(key)
                        if previous is None or score > (previous[0], previous[1]):
                            candidates[key] = (created, mtime, row)

        for (stage, paper_id, document_id), (_created, _mtime, row) in candidates.items():
            if store.has_work_history(
                outer_batch_id=batch_dir.name,
                stage=stage,
                paper_id=paper_id,
                document_id=document_id or None,
            ):
                continue
            store.record_result(
                generation=generation,
                outer_batch_id=batch_dir.name,
                stage=stage,
                paper_id=paper_id,
                document_id=document_id or None,
                config_fingerprint=fingerprints[stage],
                input_fingerprint="",
                row=row,
                artifacts=result_artifacts(row),
                imported=True,
            )
            imported_rows += 1

        # Old Stage05 output retains Router evidence only when the final record
        # contains it. Import it as an independent reusable checkpoint.
        stage05_rows = {
            paper_id: row
            for (stage, paper_id, document_id), (_created, _mtime, row) in candidates.items()
            if stage == "stage05" and not document_id
        }
        for paper_id, row in stage05_rows.items():
            if not row.get("router_response"):
                pass
            elif not store.has_work_history(
                outer_batch_id=batch_dir.name,
                stage="stage05_router",
                paper_id=paper_id,
            ):
                router_row = {
                    "paper_id": paper_id,
                    "processing_status": "completed",
                    "decision": "router_completed",
                    "passed": True,
                    "evidence_route": row.get("evidence_route"),
                    "router_response": row.get("router_response"),
                    "router_audit": row.get("router_audit"),
                    "route_validation_warnings": row.get("route_validation_warnings") or [],
                }
                store.record_result(
                    generation=generation,
                    outer_batch_id=batch_dir.name,
                    stage="stage05_router",
                    paper_id=paper_id,
                    document_id=None,
                    config_fingerprint=fingerprints["stage05_router"],
                    input_fingerprint="",
                    row=router_row,
                    imported=True,
                )
                imported_rows += 1
            if row.get("model_response") and not store.has_work_history(
                outer_batch_id=batch_dir.name,
                stage="stage05_auditor",
                paper_id=paper_id,
            ):
                attempts = row.get("model_response_attempts") or [
                    {
                        "response": row.get("model_response"),
                        "audit": row.get("model_audit") or {},
                    }
                ]
                store.record_result(
                    generation=generation,
                    outer_batch_id=batch_dir.name,
                    stage="stage05_auditor",
                    paper_id=paper_id,
                    document_id=None,
                    config_fingerprint=fingerprints["stage05_auditor"],
                    input_fingerprint="",
                    row={
                        "paper_id": paper_id,
                        "processing_status": "completed",
                        "decision": "auditor_completed",
                        "passed": True,
                        "model_response": row.get("model_response"),
                        "model_audit": row.get("model_audit") or {},
                        "model_response_attempts": attempts,
                        "contract_retry_performed": len(attempts) > 1,
                    },
                    imported=True,
                )
                imported_rows += 1

        reports.append(
            {
                "batch": batch_dir.name,
                "status": "imported",
                "configured_slots": configured_count,
                "selections": imported_selections,
                "stage_rows": imported_rows,
            }
        )
        store.record_import_event(
            import_key=import_key,
            source_path=batch_dir,
            source_sha256=source_signature,
        )
        slot_offset += configured_count or len(selected)

    report = {
        "run_root": str(root),
        "database": str(store.database),
        "batches": reports,
        "summary": store.export_audit_files(),
    }
    write_json(store.root / "migration_report.json", report)
    return report


def reconcile_dependencies(
    run_root: str | Path,
    store: ResumeStateStore,
    *,
    stop_stage: str = "stage05",
) -> dict[str, Any]:
    """Create pending/blocked work items that are absent from legacy artifacts."""

    root = Path(run_root).expanduser().resolve()
    stop_index = int(stop_stage.removeprefix("stage"))
    for batch_dir in sorted((root / "batches").glob("batch-[0-9][0-9][0-9][0-9]")):
        config_path = root / "configs" / f"{batch_dir.name}.json"
        if not config_path.is_file():
            continue
        frozen = store.root / "config_snapshots" / f"{batch_dir.name}.json"
        config = (
            json.loads(frozen.read_text(encoding="utf-8"))
            if frozen.is_file()
            else _legacy_scientific_config(batch_dir, config_path)
        )
        fingerprints = scientific_stage_fingerprints(config)
        stage00_path = batch_dir / "stage_00_remote_corpus" / "source_manifest.jsonl"
        source_rows = read_jsonl(stage00_path) if stage00_path.is_file() else []
        package_papers = _read_optional_jsonl(
            batch_dir / "stage_01_document_preparation" / "package" / "papers.jsonl"
        )
        package_documents = _read_optional_jsonl(
            batch_dir / "stage_01_document_preparation" / "package" / "documents.jsonl"
        )
        normalized_documents = _read_optional_jsonl(
            batch_dir / "stage_01_document_preparation" / "documents.jsonl"
        ) or package_documents
        package_by_id = {str(row["paper_id"]): row for row in package_papers}
        documents_by_paper: dict[str, list[dict[str, Any]]] = {}
        for document in package_documents:
            documents_by_paper.setdefault(str(document["paper_id"]), []).append(document)

        # ``plan_work`` is intentionally transactional, but opening a new
        # SQLite connection for every already-final item is prohibitively slow
        # on the shared filesystem.  Load each stage's current rows once and
        # only call plan_work for missing/non-final or changed items.
        current_cache: dict[str, dict[tuple[str, str], dict[str, Any]]] = {}

        def current_item(
            stage: str,
            paper_id: str,
            document_id: str | None = None,
            *,
            _cache=current_cache,
            _batch_name=batch_dir.name,
        ):
            if stage not in _cache:
                _cache[stage] = {
                    (str(item["paper_id"]), str(item.get("document_id") or "")): item
                    for item in store.current_work_items(
                        outer_batch_id=_batch_name, stage=stage
                    )
                }
            return _cache[stage].get((paper_id, document_id or ""))

        for source in source_rows:
            paper_id = str(source["paper_id"])
            stage00_item = current_item("stage00", paper_id)
            if not stage00_item or stage00_item["status"] not in {"succeeded", "forwarded"}:
                continue
            _ensure_pending(
                store,
                batch_dir.name,
                "stage01_package",
                paper_id,
                None,
                fingerprints["stage01_package"],
                input_fingerprint(stable_input_value(source)),
                existing=current_item("stage01_package", paper_id),
            )

        for paper_id, _paper in package_by_id.items():
            package_item = current_item("stage01_package", paper_id)
            if not package_item or package_item["status"] != "forwarded":
                continue
            for document in documents_by_paper.get(paper_id, []):
                _ensure_pending(
                    store,
                    batch_dir.name,
                    "stage01",
                    paper_id,
                    str(document["document_id"]),
                    fingerprints["stage01"],
                    document_input_fingerprint(document),
                    existing=current_item("stage01", paper_id, str(document["document_id"])),
                )

        if stop_index < 2:
            continue
        stage01_papers = _paper_work_results(store, batch_dir.name, "stage01")
        for paper_id, row in stage01_papers.items():
            if not row.get("passed"):
                continue
            docs = [
                item for item in normalized_documents if str(item.get("paper_id")) == paper_id
            ]
            _ensure_pending(
                store,
                batch_dir.name,
                "stage02",
                paper_id,
                None,
                fingerprints["stage02"],
                paper_input_fingerprint(row, docs),
                existing=current_item("stage02", paper_id),
            )

        if stop_index < 3:
            continue
        stage02 = _paper_work_results(store, batch_dir.name, "stage02")
        for paper_id, row in stage02.items():
            if row.get("passed"):
                _ensure_pending(
                    store,
                    batch_dir.name,
                    "stage03",
                    paper_id,
                    None,
                    fingerprints["stage03"],
                    paper_input_fingerprint(row, []),
                    existing=current_item("stage03", paper_id),
                )

        if stop_index < 4:
            continue
        stage03 = _paper_work_results(store, batch_dir.name, "stage03")
        normalized_by_paper: dict[str, list[dict[str, Any]]] = {}
        for document in normalized_documents:
            if document.get("decision") == "pass":
                normalized_by_paper.setdefault(str(document["paper_id"]), []).append(document)
        for paper_id, row in stage03.items():
            if not row.get("passed"):
                continue
            for document in normalized_by_paper.get(paper_id, []):
                _ensure_pending(
                    store,
                    batch_dir.name,
                    "stage04",
                    paper_id,
                    str(document["document_id"]),
                    fingerprints["stage04"],
                    document_input_fingerprint(document),
                    existing=current_item("stage04", paper_id, str(document["document_id"])),
                )

        if stop_index < 5:
            continue
        stage04 = _paper_work_results(store, batch_dir.name, "stage04")
        # Fetch the completed deep-normalization documents once.  The previous
        # implementation called ``current_results(stage04)`` inside the
        # per-paper loop below, rereading the entire Stage04 result set for
        # every paper during resume reconciliation.  On a large run this
        # turned startup into an O(papers * documents) shared-disk scan.
        deep_documents_by_paper: dict[str, list[dict[str, Any]]] = {}
        for document in store.current_results(outer_batch_id=batch_dir.name, stage="stage04"):
            if document.get("document_id"):
                deep_documents_by_paper.setdefault(str(document.get("paper_id")), []).append(
                    document
                )
        for paper_id, row in stage04.items():
            if not row.get("passed") or row.get("document_id"):
                continue
            deep_docs = deep_documents_by_paper.get(paper_id, [])
            fingerprint = paper_input_fingerprint(row, deep_docs)
            _ensure_pending(
                store,
                batch_dir.name,
                "stage05_router",
                paper_id,
                None,
                fingerprints["stage05_router"],
                fingerprint,
                existing=current_item("stage05_router", paper_id),
            )
            _ensure_pending(
                store,
                batch_dir.name,
                "stage05_auditor",
                paper_id,
                None,
                fingerprints["stage05_auditor"],
                fingerprint,
                existing=current_item("stage05_auditor", paper_id),
            )
            _ensure_pending(
                store,
                batch_dir.name,
                "stage05",
                paper_id,
                None,
                fingerprints["stage05"],
                fingerprint,
                existing=current_item("stage05", paper_id),
            )

    store.mark_blocked_by_missing_upstream(through_stage=stop_stage)
    summary = store.export_audit_files()
    write_json(store.root / "resume_plan.json", summary)
    return summary


def _ensure_pending(
    store,
    batch,
    stage,
    paper_id,
    document_id,
    config_hash,
    input_hash,
    *,
    existing: dict[str, Any] | None = None,
):
    if existing and str(existing.get("status")) in FINAL_STATUSES:
        recorded_config = str(existing.get("config_fingerprint") or "")
        recorded_input = str(existing.get("input_fingerprint") or "")
        # Imported legacy rows can lack an input fingerprint.  They are still
        # safe to reuse here; a changed non-empty fingerprint or configuration
        # is sent through plan_work and receives the normal stale/retry path.
        if recorded_config == config_hash and (
            not recorded_input or recorded_input == input_hash
        ):
            return
    store.plan_work(
        outer_batch_id=batch,
        stage=stage,
        paper_id=paper_id,
        document_id=document_id,
        config_fingerprint=config_hash,
        input_fingerprint=input_hash,
        allow_pending=False,
        upstream_ready=True,
    )


def _paper_work_results(store, batch, stage):
    output = {}
    for item in store.current_work_items(outer_batch_id=batch, stage=stage):
        if item.get("document_id"):
            continue
        row = json.loads(item["result_json"]) if item.get("result_json") else {}
        output[str(item["paper_id"])] = row
    return output


def _read_optional_jsonl(path: Path):
    return read_jsonl(path) if path.is_file() else []


def _legacy_source_signature(batch_dir: Path, config_path: Path) -> str:
    paths = [
        config_path,
        batch_dir / "config.snapshot.json",
        batch_dir / "stage_00_remote_corpus" / "selected_papers.jsonl",
        batch_dir / "stage_00_remote_corpus" / "source_manifest.jsonl",
        batch_dir / "stage_01_document_preparation" / "package" / "papers.jsonl",
        batch_dir / "stage_01_document_preparation" / "package" / "documents.jsonl",
    ]
    roots = [batch_dir, *sorted((batch_dir / "microbatches").glob("batch-*"))]
    paths.extend(
        root / relative
        for root in roots
        for relative_paths in STAGE_FILES.values()
        for relative in relative_paths
    )
    metadata = []
    for path in sorted({item.resolve() for item in paths}):
        if not path.is_file():
            continue
        stat = path.stat()
        metadata.append(
            {
                "path": str(path.relative_to(batch_dir.parent.parent)),
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        )
    return canonical_hash(
        {"version": LEGACY_IMPORT_VERSION, "files": metadata}
    )


def _registry_marks_deleted(config: dict[str, Any], paper_id: str) -> bool:
    database = Path(str((config.get("registry") or {}).get("database") or ""))
    if not database.is_file():
        return False
    try:
        with sqlite3.connect(database) as connection:
            row = connection.execute(
                """
                SELECT 1 FROM paper_sources
                WHERE run_id=? AND (source_paper_id=? OR canonical_paper_id=?)
                  AND asset_state='deleted' LIMIT 1
                """,
                (str(config.get("run_id") or ""), paper_id, paper_id),
            ).fetchone()
        return row is not None
    except (sqlite3.Error, OSError):
        return False


def _legacy_scientific_config(batch_dir: Path, config_path: Path) -> dict[str, Any]:
    snapshot = batch_dir / "config.snapshot.json"
    if snapshot.is_file():
        value = json.loads(snapshot.read_text(encoding="utf-8"))
        if isinstance(value, dict):
            return value
    return load_config(config_path)


def _serializable_config(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): (
                None if key == "_sandbox_runtime" else _serializable_config(item)
            )
            for key, item in value.items()
            if key not in {"execution_backend"}
        }
    if isinstance(value, list):
        return [_serializable_config(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)

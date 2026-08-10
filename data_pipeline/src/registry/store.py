from __future__ import annotations

import json
import shutil
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PRUNABLE_STAGES = {"stage00", "stage01", "stage02", "stage03"}


class ScreeningRegistry:
    """Persistent per-paper screening history and Stage00 asset lifecycle manager."""

    def __init__(
        self,
        database: str | Path,
        *,
        export_jsonl: str | Path | None = None,
        enabled: bool = True,
        prune_rejected_stage00_assets: bool = True,
    ) -> None:
        self.database = Path(database).expanduser()
        self.export_path = Path(export_jsonl).expanduser() if export_jsonl else None
        self.enabled = bool(enabled)
        self.prune_enabled = bool(prune_rejected_stage00_assets)
        self._lock = threading.RLock()
        if self.enabled:
            self.database.parent.mkdir(parents=True, exist_ok=True)
            self._initialize()

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> ScreeningRegistry:
        return cls(
            config["database"],
            export_jsonl=config.get("export_jsonl"),
            enabled=bool(config.get("enabled", True)),
            prune_rejected_stage00_assets=bool(config.get("prune_rejected_stage00_assets", True)),
        )

    def start_run(
        self,
        *,
        run_id: str,
        workspace: str | Path,
        config_path: str | Path,
        config_hash: str,
    ) -> None:
        if not self.enabled:
            return
        now = _now()
        with self._transaction() as connection:
            connection.execute(
                """
                INSERT INTO runs(run_id, workspace, config_path, config_hash, status, started_at, updated_at)
                VALUES (?, ?, ?, ?, 'running', ?, ?)
                ON CONFLICT(run_id) DO UPDATE SET
                    workspace=excluded.workspace,
                    config_path=excluded.config_path,
                    config_hash=excluded.config_hash,
                    status='running',
                    updated_at=excluded.updated_at
                """,
                (run_id, str(workspace), str(config_path), config_hash, now, now),
            )

    def register_stage00_manifest(
        self,
        *,
        run_id: str,
        manifest_path: str | Path,
        corpus_root: str | Path,
    ) -> int:
        if not self.enabled:
            return 0
        rows = _read_jsonl(manifest_path)
        root = Path(corpus_root).expanduser().resolve()
        now = _now()
        with self._transaction() as connection:
            for row in rows:
                paper_id = str(row["paper_id"])
                self._upsert_paper(connection, paper_id, row, now)
                local_dir = root / paper_id
                asset_state = "available" if local_dir.is_dir() else "deleted"
                connection.execute(
                    """
                    INSERT INTO paper_sources(
                        run_id, source_paper_id, canonical_paper_id, dataset, local_dir,
                        asset_state, main_remote_uri, supplementary_remote_uris_json,
                        source_record_json, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(run_id, source_paper_id) DO UPDATE SET
                        canonical_paper_id=excluded.canonical_paper_id,
                        dataset=excluded.dataset,
                        local_dir=excluded.local_dir,
                        asset_state=CASE
                            WHEN paper_sources.asset_state='deleted' AND excluded.asset_state='deleted'
                                THEN 'deleted'
                            ELSE excluded.asset_state
                        END,
                        main_remote_uri=excluded.main_remote_uri,
                        supplementary_remote_uris_json=excluded.supplementary_remote_uris_json,
                        source_record_json=excluded.source_record_json,
                        updated_at=excluded.updated_at
                    """,
                    (
                        run_id,
                        paper_id,
                        paper_id,
                        row.get("dataset"),
                        str(local_dir),
                        asset_state,
                        (row.get("main_document") or {}).get("remote_uri"),
                        _json(
                            [
                                item.get("remote_uri")
                                for item in row.get("supplementary_documents") or []
                                if item.get("remote_uri")
                            ]
                        ),
                        _json(row),
                        now,
                    ),
                )
                self._upsert_stage_result(
                    connection,
                    run_id=run_id,
                    stage="stage00",
                    row={
                        **row,
                        "decision": "copied"
                        if row.get("copy_status") == "complete"
                        else "copy_incomplete",
                        "passed": True,
                        "processing_status": "completed",
                    },
                    now=now,
                )
        return len(rows)

    def register_document_sources(
        self,
        *,
        run_id: str,
        documents: Iterable[dict[str, Any]],
    ) -> None:
        """Attach deduplicated canonical IDs to the Stage00 source directories."""

        if not self.enabled:
            return
        mappings = {
            (str(row.get("source_paper_id") or row.get("paper_id")), str(row["paper_id"]))
            for row in documents
            if row.get("paper_id")
        }
        if not mappings:
            return
        with self._transaction() as connection:
            for source_paper_id, canonical_paper_id in mappings:
                connection.execute(
                    """
                    UPDATE paper_sources
                    SET canonical_paper_id=?, updated_at=?
                    WHERE run_id=? AND source_paper_id=?
                    """,
                    (canonical_paper_id, _now(), run_id, source_paper_id),
                )

    def record_stage_results(
        self,
        *,
        run_id: str,
        stage: str,
        rows: Iterable[dict[str, Any]],
        prune: bool = True,
    ) -> dict[str, Any]:
        """Commit stage records before deleting rejected Stage00 paper bundles."""

        materialized = [row for row in rows if row.get("paper_id")]
        if not self.enabled:
            return {"recorded": 0, "deleted": 0, "bytes_freed": 0, "delete_failed": 0}
        now = _now()
        rejected_ids: set[str] = set()
        with self._transaction() as connection:
            for row in materialized:
                paper_id = str(row["paper_id"])
                self._upsert_paper(connection, paper_id, row, now)
                self._upsert_stage_result(connection, run_id=run_id, stage=stage, row=row, now=now)
                self._replace_software_mentions(
                    connection, run_id=run_id, stage=stage, row=row, now=now
                )
                if prune and self.prune_enabled and stage in PRUNABLE_STAGES and not _passed(row):
                    rejected_ids.add(paper_id)
            for paper_id in rejected_ids:
                connection.execute(
                    """
                    UPDATE paper_sources
                    SET asset_state='delete_pending', updated_at=?
                    WHERE run_id=? AND canonical_paper_id=? AND asset_state!='deleted'
                    """,
                    (now, run_id, paper_id),
                )

        deletion = {"deleted": 0, "bytes_freed": 0, "delete_failed": 0}
        for paper_id in sorted(rejected_ids):
            result = self._prune_paper(run_id=run_id, paper_id=paper_id, stage=stage)
            for key in deletion:
                deletion[key] += int(result.get(key, 0))
        return {"recorded": len(materialized), **deletion}

    def finish_run(self, *, run_id: str, status: str) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False}
        with self._transaction() as connection:
            connection.execute(
                "UPDATE runs SET status=?, updated_at=? WHERE run_id=?",
                (status, _now(), run_id),
            )
        if self.export_path:
            self.export_jsonl(self.export_path)
        return self.run_summary(run_id)

    def run_summary(self, run_id: str) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False}
        with self._connect() as connection:
            stages = {
                row["stage"]: {"papers": row["papers"], "passed": row["passed"]}
                for row in connection.execute(
                    """
                    SELECT stage, COUNT(DISTINCT paper_id) AS papers,
                           SUM(CASE WHEN passed=1 THEN 1 ELSE 0 END) AS passed
                    FROM stage_results WHERE run_id=? GROUP BY stage ORDER BY stage
                    """,
                    (run_id,),
                )
            }
            assets = dict(
                connection.execute(
                    """
                    SELECT COUNT(*) AS sources,
                           SUM(CASE WHEN asset_state='deleted' THEN 1 ELSE 0 END) AS deleted
                    FROM paper_sources WHERE run_id=?
                    """,
                    (run_id,),
                ).fetchone()
            )
            freed = connection.execute(
                """
                SELECT COALESCE(SUM(bytes_freed), 0) AS value FROM artifact_events
                WHERE run_id=? AND status='deleted'
                """,
                (run_id,),
            ).fetchone()["value"]
        return {
            "enabled": True,
            "database": str(self.database),
            "stages": stages,
            "source_assets": assets,
            "bytes_freed": int(freed or 0),
        }

    def export_jsonl(self, path: str | Path) -> int:
        target = Path(path).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            keys = connection.execute(
                "SELECT DISTINCT run_id, paper_id FROM stage_results ORDER BY run_id, paper_id"
            ).fetchall()
            rows = []
            for key in keys:
                run_id, paper_id = key["run_id"], key["paper_id"]
                paper = connection.execute(
                    "SELECT * FROM papers WHERE paper_id=?", (paper_id,)
                ).fetchone()
                sources = connection.execute(
                    """
                    SELECT * FROM paper_sources
                    WHERE run_id=? AND canonical_paper_id=? ORDER BY source_paper_id
                    """,
                    (run_id, paper_id),
                ).fetchall()
                stage_rows = connection.execute(
                    """
                    SELECT stage, record_id, decision, passed, processing_status, result_json,
                           recorded_at
                    FROM stage_results WHERE run_id=? AND paper_id=?
                    ORDER BY stage, record_id
                    """,
                    (run_id, paper_id),
                ).fetchall()
                stages: dict[str, list[dict[str, Any]]] = {}
                for stage_row in stage_rows:
                    stages.setdefault(stage_row["stage"], []).append(
                        {
                            "record_id": stage_row["record_id"],
                            "decision": stage_row["decision"],
                            "passed": bool(stage_row["passed"]),
                            "processing_status": stage_row["processing_status"],
                            "recorded_at": stage_row["recorded_at"],
                            "result": json.loads(stage_row["result_json"]),
                        }
                    )
                rows.append(
                    {
                        "run_id": run_id,
                        "paper_id": paper_id,
                        "paper": dict(paper) if paper else {},
                        "sources": [dict(source) for source in sources],
                        "stages": stages,
                    }
                )
        temporary = target.with_suffix(target.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as output:
            for row in rows:
                output.write(_json(row) + "\n")
        temporary.replace(target)
        return len(rows)

    def _prune_paper(self, *, run_id: str, paper_id: str, stage: str) -> dict[str, int]:
        with self._connect() as connection:
            sources = connection.execute(
                """
                SELECT source_paper_id, local_dir FROM paper_sources
                WHERE run_id=? AND canonical_paper_id=? AND asset_state='delete_pending'
                """,
                (run_id, paper_id),
            ).fetchall()
        result = {"deleted": 0, "bytes_freed": 0, "delete_failed": 0}
        for source in sources:
            source_paper_id = source["source_paper_id"]
            local_dir = Path(source["local_dir"])
            try:
                _validate_stage00_bundle(local_dir, source_paper_id)
                if not local_dir.exists():
                    status, bytes_freed, error = "deleted", 0, None
                else:
                    bytes_freed = _directory_size(local_dir)
                    shutil.rmtree(local_dir)
                    status, error = "deleted", None
                result["deleted"] += 1
                result["bytes_freed"] += bytes_freed
            except Exception as exc:
                status, bytes_freed, error = "delete_failed", 0, f"{type(exc).__name__}: {exc}"
                result["delete_failed"] += 1
            with self._transaction() as connection:
                connection.execute(
                    """
                    UPDATE paper_sources SET asset_state=?, updated_at=?
                    WHERE run_id=? AND source_paper_id=?
                    """,
                    (status, _now(), run_id, source_paper_id),
                )
                connection.execute(
                    """
                    INSERT INTO artifact_events(
                        run_id, paper_id, source_paper_id, stage, action, status,
                        local_dir, bytes_freed, error, created_at
                    ) VALUES (?, ?, ?, ?, 'delete_stage00_bundle', ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        paper_id,
                        source_paper_id,
                        stage,
                        status,
                        str(local_dir),
                        bytes_freed,
                        error,
                        _now(),
                    ),
                )
        return result

    def _initialize(self) -> None:
        with self._transaction() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS runs(
                    run_id TEXT PRIMARY KEY,
                    workspace TEXT NOT NULL,
                    config_path TEXT NOT NULL,
                    config_hash TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS papers(
                    paper_id TEXT PRIMARY KEY,
                    doi TEXT,
                    title TEXT,
                    journal_name TEXT,
                    article_url TEXT,
                    metadata_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS paper_sources(
                    run_id TEXT NOT NULL,
                    source_paper_id TEXT NOT NULL,
                    canonical_paper_id TEXT NOT NULL,
                    dataset TEXT,
                    local_dir TEXT NOT NULL,
                    asset_state TEXT NOT NULL,
                    main_remote_uri TEXT,
                    supplementary_remote_uris_json TEXT NOT NULL,
                    source_record_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY(run_id, source_paper_id)
                );
                CREATE INDEX IF NOT EXISTS paper_sources_canonical_idx
                    ON paper_sources(run_id, canonical_paper_id);
                CREATE TABLE IF NOT EXISTS stage_results(
                    run_id TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    passed INTEGER NOT NULL,
                    processing_status TEXT,
                    result_json TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    PRIMARY KEY(run_id, paper_id, stage, record_id)
                );
                CREATE INDEX IF NOT EXISTS stage_results_lookup_idx
                    ON stage_results(run_id, stage, decision, passed);
                CREATE TABLE IF NOT EXISTS software_mentions(
                    run_id TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    mention_index INTEGER NOT NULL,
                    raw_name TEXT,
                    normalized_identifier TEXT,
                    role TEXT,
                    actual_use INTEGER NOT NULL,
                    catalog_present INTEGER,
                    evidence_ids_json TEXT NOT NULL,
                    mention_json TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    PRIMARY KEY(run_id, paper_id, stage, mention_index)
                );
                CREATE TABLE IF NOT EXISTS artifact_events(
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    source_paper_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    local_dir TEXT NOT NULL,
                    bytes_freed INTEGER NOT NULL,
                    error TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )

    def _upsert_paper(self, connection, paper_id, row, now) -> None:
        connection.execute(
            """
            INSERT INTO papers(
                paper_id, doi, title, journal_name, article_url, metadata_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(paper_id) DO UPDATE SET
                doi=COALESCE(excluded.doi, papers.doi),
                title=COALESCE(excluded.title, papers.title),
                journal_name=COALESCE(excluded.journal_name, papers.journal_name),
                article_url=COALESCE(excluded.article_url, papers.article_url),
                metadata_json=excluded.metadata_json,
                updated_at=excluded.updated_at
            """,
            (
                paper_id,
                row.get("doi"),
                row.get("title"),
                row.get("journal_name"),
                row.get("article_url"),
                _json(_paper_metadata(row)),
                now,
            ),
        )

    def _upsert_stage_result(self, connection, *, run_id, stage, row, now) -> None:
        paper_id = str(row["paper_id"])
        record_id = str(
            row.get("task_pair_id") or row.get("candidate_id") or row.get("record_id") or paper_id
        )
        connection.execute(
            """
            INSERT INTO stage_results(
                run_id, paper_id, stage, record_id, decision, passed,
                processing_status, result_json, recorded_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id, paper_id, stage, record_id) DO UPDATE SET
                decision=excluded.decision,
                passed=excluded.passed,
                processing_status=excluded.processing_status,
                result_json=excluded.result_json,
                recorded_at=excluded.recorded_at
            """,
            (
                run_id,
                paper_id,
                stage,
                record_id,
                str(row.get("decision") or "missing"),
                int(_passed(row)),
                row.get("processing_status"),
                _json(row),
                now,
            ),
        )

    def _replace_software_mentions(self, connection, *, run_id, stage, row, now) -> None:
        paper_id = str(row["paper_id"])
        mentions = row.get("software_mentions") or []
        mappings = row.get("software_mappings") or []
        if not isinstance(mentions, list):
            return
        connection.execute(
            "DELETE FROM software_mentions WHERE run_id=? AND paper_id=? AND stage=?",
            (run_id, paper_id, stage),
        )
        for index, mention in enumerate(item for item in mentions if isinstance(item, dict)):
            mapping = (
                mappings[index]
                if index < len(mappings) and isinstance(mappings[index], dict)
                else {}
            )
            connection.execute(
                """
                INSERT INTO software_mentions(
                    run_id, paper_id, stage, mention_index, raw_name, normalized_identifier,
                    role, actual_use, catalog_present, evidence_ids_json, mention_json, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    paper_id,
                    stage,
                    index,
                    mention.get("raw_name"),
                    mapping.get("normalized_identifier"),
                    mention.get("role"),
                    int(bool(mention.get("actual_use"))),
                    int(bool(mapping.get("catalog_present"))) if mapping else None,
                    _json(mention.get("evidence_ids") or []),
                    _json({"mention": mention, "mapping": mapping}),
                    now,
                ),
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=60)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=60000")
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    def _transaction(self):
        return _Transaction(self)


class _Transaction:
    def __init__(self, registry: ScreeningRegistry) -> None:
        self.registry = registry
        self.connection: sqlite3.Connection | None = None

    def __enter__(self) -> sqlite3.Connection:
        self.registry._lock.acquire()
        self.connection = self.registry._connect()
        self.connection.execute("BEGIN IMMEDIATE")
        return self.connection

    def __exit__(self, exc_type, exc, traceback) -> None:
        assert self.connection is not None
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.connection.close()
            self.registry._lock.release()


def _passed(row: dict[str, Any]) -> bool:
    if "passed" in row:
        return bool(row.get("passed"))
    return str(row.get("decision") or "").casefold() in {"pass", "passed", "copied"}


def _validate_stage00_bundle(path: Path, source_paper_id: str) -> None:
    candidate = path.expanduser().absolute()
    if candidate.name != source_paper_id:
        raise ValueError("Stage00 bundle name does not match source_paper_id")
    if (
        candidate.parent.name != "corpus"
        or candidate.parent.parent.name != "stage_00_remote_corpus"
    ):
        raise ValueError("refusing to delete a path outside stage_00_remote_corpus/corpus")
    if candidate.is_symlink():
        raise ValueError("refusing to delete a symlinked Stage00 paper bundle")


def _directory_size(path: Path) -> int:
    return sum(
        item.stat().st_size for item in path.rglob("*") if item.is_file() and not item.is_symlink()
    )


def _paper_metadata(row: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "doi",
        "title",
        "journal_name",
        "article_url",
        "dataset",
        "source_record",
        "toolbox_profile_id",
        "toolbox_catalog_hash",
    )
    return {key: row.get(key) for key in keys if row.get(key) is not None}


def _read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    if not source.is_file():
        return []
    return [
        json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

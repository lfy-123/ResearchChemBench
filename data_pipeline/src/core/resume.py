from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from src.contracts import canonical_hash
from src.core.failure_classification import WorkDisposition, classify_stage_record
from src.core.io import sha256_file, write_json, write_jsonl


FINAL_STATUSES = {"succeeded", "terminal_reject", "forwarded", "not_applicable"}
RETRYABLE_STATUSES = {"pending", "retryable_failed"}
VALID_STATUSES = {
    "pending",
    "running",
    "succeeded",
    "terminal_reject",
    "forwarded",
    "retryable_failed",
    "blocked_by_upstream",
    "not_applicable",
    "stale",
}


class ResumeConfigurationMismatch(RuntimeError):
    pass


@dataclass(frozen=True)
class PlannedWork:
    action: str
    status: str
    result: dict[str, Any] | None = None
    reason: str | None = None


class ResumeStateStore:
    """Transactional fact store for Stage00-05 selection and work-item recovery."""

    def __init__(self, database: str | Path) -> None:
        self.database = Path(database).expanduser().resolve()
        self.root = self.database.parent
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._initialize()

    @classmethod
    def for_run_root(cls, run_root: str | Path) -> "ResumeStateStore":
        return cls(Path(run_root).expanduser().resolve() / "resume" / "resume_state.sqlite")

    def create_generation(
        self,
        *,
        command_hash: str,
        total_target: int,
        start_stage: str,
        stop_stage: str,
        invalidated_stages: Iterable[str] = (),
    ) -> int:
        now = _now()
        with self.transaction() as connection:
            current = connection.execute(
                "SELECT COALESCE(MAX(generation), 0) + 1 FROM resume_generations"
            ).fetchone()[0]
            connection.execute(
                """
                INSERT INTO resume_generations(
                    generation, command_hash, total_target, start_stage, stop_stage,
                    invalidated_stages_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'running', ?, ?)
                """,
                (
                    current,
                    command_hash,
                    int(total_target),
                    start_stage,
                    stop_stage,
                    _json(sorted(set(invalidated_stages))),
                    now,
                    now,
                ),
            )
        return int(current)

    def finish_generation(self, generation: int, *, status: str) -> None:
        with self.transaction() as connection:
            connection.execute(
                "UPDATE resume_generations SET status=?, updated_at=? WHERE generation=?",
                (status, _now(), int(generation)),
            )

    def reserve_selection(
        self,
        *,
        dataset: str,
        source_main_uri: str,
        normalized_doi: str | None,
        source_record_key: str | None,
        paper_id: str | None,
        target_slot_ordinal: int,
        outer_batch_id: str,
        replaces_selection_id: str | None = None,
    ) -> dict[str, Any]:
        now = _now()
        selection_id = f"selection_{uuid.uuid4().hex}"
        doi = _normalize_doi(normalized_doi)
        with self.transaction() as connection:
            by_slot = connection.execute(
                """
                SELECT * FROM corpus_selections
                WHERE target_slot_ordinal=? AND active=1
                """,
                (int(target_slot_ordinal),),
            ).fetchone()
            if by_slot:
                return dict(by_slot)
            conflict = connection.execute(
                "SELECT * FROM corpus_selections WHERE dataset=? AND source_main_uri=?",
                (dataset, source_main_uri),
            ).fetchone()
            if conflict:
                return dict(conflict)
            if doi:
                conflict = connection.execute(
                    """
                    SELECT * FROM corpus_selections
                    WHERE dataset=? AND normalized_doi=? AND active=1
                    """,
                    (dataset, doi),
                ).fetchone()
                if conflict:
                    raise ValueError(
                        f"selection DOI conflict for {doi}: {conflict['source_main_uri']}"
                    )
            event_ordinal = connection.execute(
                "SELECT COALESCE(MAX(selection_event_ordinal), 0) + 1 FROM corpus_selections"
            ).fetchone()[0]
            connection.execute(
                """
                INSERT INTO corpus_selections(
                    selection_id, dataset, source_main_uri, normalized_doi,
                    source_record_key, paper_id, target_slot_ordinal,
                    selection_event_ordinal, replaces_selection_id, outer_batch_id,
                    selected_at, copy_state, local_assets_state, active, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'reserved', 'missing_required', 1, ?)
                """,
                (
                    selection_id,
                    dataset,
                    source_main_uri,
                    doi or None,
                    source_record_key,
                    paper_id,
                    int(target_slot_ordinal),
                    int(event_ordinal),
                    replaces_selection_id,
                    outer_batch_id,
                    now,
                    now,
                ),
            )
            return dict(
                connection.execute(
                    "SELECT * FROM corpus_selections WHERE selection_id=?", (selection_id,)
                ).fetchone()
            )

    def import_selection(self, **values) -> dict[str, Any]:
        existing = self.selection_for_slot(int(values["target_slot_ordinal"]))
        if existing:
            if str(existing["source_main_uri"]) != str(values["source_main_uri"]):
                raise ValueError(
                    f"target slot {values['target_slot_ordinal']} is already bound to "
                    f"{existing['source_main_uri']}, not {values['source_main_uri']}"
                )
            return existing
        return self.reserve_selection(**values)

    def update_selection_copy(
        self,
        selection_id: str,
        *,
        copy_state: str,
        paper_id: str | None = None,
        source_sha256: str | None = None,
        local_assets_state: str | None = None,
        error: dict[str, Any] | None = None,
    ) -> None:
        with self.transaction() as connection:
            connection.execute(
                """
                UPDATE corpus_selections SET
                    copy_state=?, paper_id=COALESCE(?, paper_id),
                    source_sha256=COALESCE(?, source_sha256),
                    local_assets_state=COALESCE(?, local_assets_state),
                    last_error_json=?, updated_at=?
                WHERE selection_id=?
                """,
                (
                    copy_state,
                    paper_id,
                    source_sha256,
                    local_assets_state,
                    _json(error or {}),
                    _now(),
                    selection_id,
                ),
            )

    def selection_for_slot(self, target_slot_ordinal: int) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM corpus_selections
                WHERE target_slot_ordinal=? AND active=1
                ORDER BY selection_event_ordinal DESC LIMIT 1
                """,
                (int(target_slot_ordinal),),
            ).fetchone()
        return dict(row) if row else None

    def selections_for_batch(self, outer_batch_id: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM corpus_selections
                WHERE outer_batch_id=? AND active=1 ORDER BY target_slot_ordinal
                """,
                (outer_batch_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def selection_for_paper(self, paper_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM corpus_selections
                WHERE paper_id=? AND active=1
                ORDER BY selection_event_ordinal DESC LIMIT 1
                """,
                (paper_id,),
            ).fetchone()
        return dict(row) if row else None

    def set_local_assets_state(self, paper_id: str, state: str) -> int:
        with self.transaction() as connection:
            cursor = connection.execute(
                """
                UPDATE corpus_selections SET local_assets_state=?, updated_at=?
                WHERE paper_id=? AND active=1
                """,
                (state, _now(), paper_id),
            )
        return int(cursor.rowcount)

    def selected_main_uris(self, dataset: str) -> set[str]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT source_main_uri FROM corpus_selections WHERE dataset=?",
                (dataset,),
            ).fetchall()
        return {str(row[0]) for row in rows}

    def max_target_slot(self) -> int:
        with self.connect() as connection:
            value = connection.execute(
                "SELECT COALESCE(MAX(target_slot_ordinal), 0) FROM corpus_selections"
            ).fetchone()[0]
        return int(value)

    def plan_work(
        self,
        *,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None,
        config_fingerprint: str,
        input_fingerprint: str,
        allow_pending: bool = True,
        retry_only: bool = False,
        invalidated: bool = False,
        upstream_ready: bool = False,
    ) -> PlannedWork:
        document_key = document_id or ""
        with self.transaction() as connection:
            current = connection.execute(
                """
                SELECT * FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=?
                  AND is_current=1
                ORDER BY updated_at DESC LIMIT 1
                """,
                (outer_batch_id, stage, paper_id, document_key),
            ).fetchone()
            if current and str(current["config_fingerprint"]) != config_fingerprint:
                if not invalidated:
                    raise ResumeConfigurationMismatch(
                        f"{outer_batch_id}/{stage}/{paper_id}/{document_key or '-'} was produced "
                        "with a different scientific configuration; use --invalidate-stage"
                    )
                connection.execute(
                    "UPDATE stage_work_items SET is_current=0, status='stale', updated_at=? WHERE work_item_id=?",
                    (_now(), current["work_item_id"]),
                )
                current = None
            if current and str(current["input_fingerprint"] or "") not in {
                "",
                input_fingerprint,
            }:
                connection.execute(
                    "UPDATE stage_work_items SET is_current=0, status='stale', updated_at=? WHERE work_item_id=?",
                    (_now(), current["work_item_id"]),
                )
                current = None
            if current and not current["input_fingerprint"]:
                connection.execute(
                    "UPDATE stage_work_items SET input_fingerprint=?, updated_at=? WHERE work_item_id=?",
                    (input_fingerprint, _now(), current["work_item_id"]),
                )
            if current and current["status"] in FINAL_STATUSES:
                if self._paper_was_terminally_pruned(connection, paper_id) or self._artifacts_valid(
                    connection, current["work_item_id"]
                ):
                    return PlannedWork(
                        "reuse",
                        str(current["status"]),
                        _loads(current["result_json"]),
                    )
                connection.execute(
                    """
                    UPDATE stage_work_items SET status='retryable_failed',
                        failure_class='artifact_missing_or_changed', updated_at=?
                    WHERE work_item_id=?
                    """,
                    (_now(), current["work_item_id"]),
                )
                current = connection.execute(
                    "SELECT * FROM stage_work_items WHERE work_item_id=?",
                    (current["work_item_id"],),
                ).fetchone()
            if current:
                status = str(current["status"])
                if status == "blocked_by_upstream" and upstream_ready:
                    was_retryable = str(current["failure_class"] or "").endswith(
                        "after_retryable_failure"
                    )
                    status = "retryable_failed" if was_retryable else "pending"
                    connection.execute(
                        "UPDATE stage_work_items SET status=?, failure_class=?, updated_at=? "
                        "WHERE work_item_id=?",
                        (
                            status,
                            "upstream_recovered_retry" if was_retryable else None,
                            _now(),
                            current["work_item_id"],
                        ),
                    )
                if retry_only and status == "pending":
                    return PlannedWork(
                        "skip", status, _loads(current["result_json"]), reason="retry_only"
                    )
                if status == "blocked_by_upstream":
                    return PlannedWork(
                        "blocked", status, _loads(current["result_json"])
                    )
                if status in RETRYABLE_STATUSES and allow_pending:
                    connection.execute(
                        """
                        UPDATE stage_work_items SET status='running', failure_class=NULL,
                            updated_at=? WHERE work_item_id=?
                        """,
                        (_now(), current["work_item_id"]),
                    )
                    return PlannedWork("run", status)
                return PlannedWork("skip", status, _loads(current["result_json"]))
            # A prior generation may have explicitly invalidated this exact
            # scientific configuration, or an upstream input may have changed
            # and later returned to the same fingerprint. Attempts are kept in
            # the immutable attempt table, while the stable work item is
            # reactivated instead of violating its uniqueness constraint.
            reusable = connection.execute(
                """
                SELECT * FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=?
                  AND config_fingerprint=?
                ORDER BY updated_at DESC LIMIT 1
                """,
                (
                    outer_batch_id,
                    stage,
                    paper_id,
                    document_key,
                    config_fingerprint,
                ),
            ).fetchone()
            now = _now()
            if reusable is not None:
                work_item_id = str(reusable["work_item_id"])
                connection.execute(
                    """
                    UPDATE stage_work_items SET input_fingerprint=?, status='pending',
                        failure_class=NULL, result_json=NULL, current_attempt_id=NULL,
                        is_current=1, updated_at=? WHERE work_item_id=?
                    """,
                    (input_fingerprint, now, work_item_id),
                )
            else:
                work_item_id = uuid.uuid4().hex
                connection.execute(
                    """
                    INSERT INTO stage_work_items(
                        work_item_id, outer_batch_id, stage, paper_id, document_id,
                        config_fingerprint, input_fingerprint, status, is_current,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 1, ?, ?)
                    """,
                    (
                        work_item_id,
                        outer_batch_id,
                        stage,
                        paper_id,
                        document_key,
                        config_fingerprint,
                        input_fingerprint,
                        now,
                        now,
                    ),
                )
        if retry_only or not allow_pending:
            return PlannedWork("skip", "pending", reason="pending_not_enabled")
        with self.transaction() as connection:
            connection.execute(
                """
                UPDATE stage_work_items SET status='running', updated_at=?
                WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=?
                  AND config_fingerprint=? AND status='pending'
                """,
                (
                    _now(),
                    outer_batch_id,
                    stage,
                    paper_id,
                    document_key,
                    config_fingerprint,
                ),
            )
        return PlannedWork("run", "pending")

    def record_result(
        self,
        *,
        generation: int,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None,
        config_fingerprint: str,
        input_fingerprint: str,
        row: dict[str, Any],
        artifacts: Iterable[str | Path] = (),
        runtime_fingerprint: str = "",
        imported: bool = False,
    ) -> str:
        disposition = classify_stage_record(stage, row)
        return self._record_attempt(
            generation=generation,
            outer_batch_id=outer_batch_id,
            stage=stage,
            paper_id=paper_id,
            document_id=document_id,
            config_fingerprint=config_fingerprint,
            input_fingerprint=input_fingerprint,
            disposition=disposition,
            row=row,
            artifacts=artifacts,
            runtime_fingerprint=runtime_fingerprint,
            imported=imported,
        )

    def record_retryable_failure(
        self,
        *,
        generation: int,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None,
        config_fingerprint: str,
        input_fingerprint: str,
        failure_class: str,
        error: dict[str, Any],
    ) -> str:
        row = {
            "paper_id": paper_id,
            "document_id": document_id,
            "processing_status": "failed",
            "decision": "processing_failed",
            "passed": False,
            "error": error,
        }
        return self._record_attempt(
            generation=generation,
            outer_batch_id=outer_batch_id,
            stage=stage,
            paper_id=paper_id,
            document_id=document_id,
            config_fingerprint=config_fingerprint,
            input_fingerprint=input_fingerprint,
            disposition=WorkDisposition("retryable_failed", failure_class),
            row=row,
            artifacts=(),
            runtime_fingerprint="",
            imported=False,
        )

    def _record_attempt(
        self,
        *,
        generation: int,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None,
        config_fingerprint: str,
        input_fingerprint: str,
        disposition: WorkDisposition,
        row: dict[str, Any],
        artifacts: Iterable[str | Path],
        runtime_fingerprint: str,
        imported: bool,
    ) -> str:
        if disposition.status not in VALID_STATUSES:
            raise ValueError(f"invalid work status: {disposition.status}")
        document_key = document_id or ""
        artifact_rows = [_artifact(path) for path in artifacts if Path(path).is_file()]
        result_hash = canonical_hash(row)
        deterministic = canonical_hash(
            {
                "batch": outer_batch_id,
                "stage": stage,
                "paper": paper_id,
                "document": document_key,
                "config": config_fingerprint,
                "result": result_hash,
                "imported": bool(imported),
            }
        )
        attempt_id = f"attempt_{deterministic[:24]}" if imported else f"attempt_{uuid.uuid4().hex}"
        now = _now()
        with self.transaction() as connection:
            current = connection.execute(
                """
                SELECT * FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=?
                  AND config_fingerprint=?
                """,
                (outer_batch_id, stage, paper_id, document_key, config_fingerprint),
            ).fetchone()
            if current is None:
                connection.execute(
                    """
                    UPDATE stage_work_items SET is_current=0
                    WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=?
                    """,
                    (outer_batch_id, stage, paper_id, document_key),
                )
                work_item_id = uuid.uuid4().hex
                connection.execute(
                    """
                    INSERT INTO stage_work_items(
                        work_item_id, outer_batch_id, stage, paper_id, document_id,
                        config_fingerprint, input_fingerprint, status, failure_class,
                        result_json, current_attempt_id, is_current, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                    """,
                    (
                        work_item_id,
                        outer_batch_id,
                        stage,
                        paper_id,
                        document_key,
                        config_fingerprint,
                        input_fingerprint,
                        disposition.status,
                        disposition.failure_class,
                        _json(row),
                        attempt_id,
                        now,
                        now,
                    ),
                )
            else:
                work_item_id = str(current["work_item_id"])
                connection.execute(
                    """
                    UPDATE stage_work_items SET input_fingerprint=?, status=?, failure_class=?,
                        result_json=?, current_attempt_id=?, is_current=1, updated_at=?
                    WHERE work_item_id=?
                    """,
                    (
                        input_fingerprint,
                        disposition.status,
                        disposition.failure_class,
                        _json(row),
                        attempt_id,
                        now,
                        work_item_id,
                    ),
                )
            connection.execute(
                """
                INSERT OR IGNORE INTO stage_attempts(
                    attempt_id, work_item_id, resume_generation, stage, paper_id,
                    document_id, status, failure_class, started_at, finished_at,
                    runtime_fingerprint, result_json, error_json, imported
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt_id,
                    work_item_id,
                    int(generation),
                    stage,
                    paper_id,
                    document_key,
                    disposition.status,
                    disposition.failure_class,
                    str(row.get("created_at") or now),
                    now,
                    runtime_fingerprint,
                    _json(row),
                    _json(row.get("error") or {}),
                    int(imported),
                ),
            )
            for artifact in artifact_rows:
                connection.execute(
                    """
                    INSERT INTO artifact_manifests(
                        artifact_id, work_item_id, attempt_id, path, size_bytes,
                        sha256, required, recorded_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 1, ?)
                    """,
                    (
                        uuid.uuid4().hex,
                        work_item_id,
                        attempt_id,
                        artifact["path"],
                        artifact["size_bytes"],
                        artifact["sha256"],
                        now,
                    ),
                )
        return attempt_id

    def set_blocked(
        self,
        *,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None,
        config_fingerprint: str,
        input_fingerprint: str,
        reason: str,
    ) -> None:
        document_key = document_id or ""
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO stage_work_items(
                    work_item_id, outer_batch_id, stage, paper_id, document_id,
                    config_fingerprint, input_fingerprint, status, failure_class,
                    is_current, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'blocked_by_upstream', ?, 1, ?, ?)
                ON CONFLICT(outer_batch_id, stage, paper_id, document_id, config_fingerprint)
                DO UPDATE SET status='blocked_by_upstream', failure_class=excluded.failure_class,
                    input_fingerprint=excluded.input_fingerprint, is_current=1,
                    updated_at=excluded.updated_at
                """,
                (
                    uuid.uuid4().hex,
                    outer_batch_id,
                    stage,
                    paper_id,
                    document_key,
                    config_fingerprint,
                    input_fingerprint,
                    reason,
                    _now(),
                    _now(),
                ),
            )

    def invalidate_stage(self, stage: str, *, outer_batch_ids: Iterable[str] = ()) -> int:
        batches = tuple(dict.fromkeys(str(value) for value in outer_batch_ids))
        batch_clause = ""
        parameters: list[Any] = [_now(), stage]
        if batches:
            placeholders = ",".join("?" for _ in batches)
            batch_clause = f" AND outer_batch_id IN ({placeholders})"
            parameters.extend(batches)
        with self.transaction() as connection:
            cursor = connection.execute(
                f"""
                UPDATE stage_work_items SET is_current=0, status='stale', updated_at=?
                WHERE stage=? AND is_current=1{batch_clause}
                """,
                parameters,
            )
        return int(cursor.rowcount)

    def invalidate_stages(
        self, stages: Iterable[str], *, outer_batch_ids: Iterable[str] = ()
    ) -> dict[str, int]:
        return {
            stage: self.invalidate_stage(stage, outer_batch_ids=outer_batch_ids)
            for stage in dict.fromkeys(stages)
        }

    def mark_blocked_by_missing_upstream(self, *, through_stage: str) -> int:
        stop_index = int(through_stage.removeprefix("stage"))
        changed = 0
        dependencies = (
            ("stage02", "stage01"),
            ("stage03", "stage02"),
            ("stage04", "stage03"),
            ("stage05_router", "stage04"),
            ("stage05_auditor", "stage04"),
            ("stage05", "stage04"),
        )
        with self.transaction() as connection:
            for stage, upstream in dependencies:
                if int(_parent_stage(stage).removeprefix("stage")) > stop_index:
                    continue
                cursor = connection.execute(
                    """
                    UPDATE stage_work_items AS child
                    SET status='blocked_by_upstream', failure_class=(
                            CASE WHEN child.status='retryable_failed'
                            THEN 'upstream_not_forwarded_after_retryable_failure'
                            ELSE 'upstream_not_forwarded' END
                        ),
                        updated_at=?
                    WHERE child.stage=? AND child.is_current=1
                      AND child.status IN ('pending','retryable_failed')
                      AND NOT EXISTS (
                        SELECT 1 FROM stage_work_items AS parent
                        WHERE parent.outer_batch_id=child.outer_batch_id
                          AND parent.paper_id=child.paper_id
                          AND parent.document_id=''
                          AND parent.stage=? AND parent.is_current=1
                          AND parent.status IN ('forwarded','succeeded')
                      )
                    """,
                    (_now(), stage, upstream),
                )
                changed += int(cursor.rowcount)
        return changed

    def batches(self) -> list[str]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT outer_batch_id FROM corpus_selections
                UNION SELECT outer_batch_id FROM stage_work_items
                ORDER BY outer_batch_id
                """
            ).fetchall()
        return [str(row[0]) for row in rows]

    def work_counts(
        self,
        *,
        outer_batch_id: str | None = None,
        start_stage: str = "stage00",
        stop_stage: str = "stage05",
    ) -> dict[str, Any]:
        start_index = int(start_stage.removeprefix("stage"))
        stop_index = int(stop_stage.removeprefix("stage"))
        parameters: list[Any] = []
        where = ["is_current=1"]
        if outer_batch_id:
            where.append("outer_batch_id=?")
            parameters.append(outer_batch_id)
        with self.connect() as connection:
            rows = connection.execute(
                f"""
                SELECT outer_batch_id, stage, status, COUNT(*) AS count
                FROM stage_work_items WHERE {' AND '.join(where)}
                GROUP BY outer_batch_id, stage, status
                ORDER BY outer_batch_id, stage, status
                """,
                parameters,
            ).fetchall()
        batches: dict[str, dict[str, dict[str, int]]] = {}
        for row in rows:
            stage = str(row["stage"])
            parent = _parent_stage(stage)
            index = int(parent.removeprefix("stage"))
            if not start_index <= index <= stop_index:
                continue
            batches.setdefault(str(row["outer_batch_id"]), {}).setdefault(stage, {})[
                str(row["status"])
            ] = int(row["count"])
        totals: dict[str, dict[str, int]] = {}
        for stages in batches.values():
            for stage, statuses in stages.items():
                target = totals.setdefault(stage, {})
                for status, count in statuses.items():
                    target[status] = target.get(status, 0) + count
        return {"batches": batches, "totals": totals}

    def configuration_mismatches(
        self,
        *,
        outer_batch_id: str,
        fingerprints: dict[str, str],
        through_stage: str,
        invalidated_stages: Iterable[str] = (),
    ) -> list[dict[str, str]]:
        stop_index = int(through_stage.removeprefix("stage"))
        invalidated = set(invalidated_stages)
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT DISTINCT stage, config_fingerprint FROM stage_work_items
                WHERE outer_batch_id=? AND is_current=1
                """,
                (outer_batch_id,),
            ).fetchall()
        output = []
        for row in rows:
            stage = str(row["stage"])
            parent = _parent_stage(stage)
            if int(parent.removeprefix("stage")) > stop_index or stage in invalidated:
                continue
            expected = fingerprints.get(stage)
            actual = str(row["config_fingerprint"])
            if expected and expected != actual:
                output.append(
                    {"stage": stage, "recorded": actual, "requested": expected}
                )
        return output

    def current_results(self, *, outer_batch_id: str, stage: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT result_json FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND is_current=1
                  AND status IN ('succeeded','terminal_reject','forwarded','not_applicable')
                ORDER BY paper_id, document_id
                """,
                (outer_batch_id, stage),
            ).fetchall()
        return [_loads(row[0]) for row in rows if row[0]]

    def current_work_items(
        self, *, outer_batch_id: str, stage: str
    ) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND is_current=1
                ORDER BY paper_id, document_id
                """,
                (outer_batch_id, stage),
            ).fetchall()
        return [dict(row) for row in rows]

    def current_work_item(
        self,
        *,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None = None,
    ) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=?
                  AND is_current=1 ORDER BY updated_at DESC LIMIT 1
                """,
                (outer_batch_id, stage, paper_id, document_id or ""),
            ).fetchone()
        return dict(row) if row else None

    def has_work_history(
        self,
        *,
        outer_batch_id: str,
        stage: str,
        paper_id: str,
        document_id: str | None = None,
    ) -> bool:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT 1 FROM stage_work_items
                WHERE outer_batch_id=? AND stage=? AND paper_id=? AND document_id=? LIMIT 1
                """,
                (outer_batch_id, stage, paper_id, document_id or ""),
            ).fetchone()
        return row is not None

    def import_event(self, import_key: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM import_events WHERE import_key=?", (import_key,)
            ).fetchone()
        return dict(row) if row else None

    def record_import_event(
        self, *, import_key: str, source_path: str | Path, source_sha256: str
    ) -> None:
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO import_events(import_key, source_path, source_sha256, imported_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(import_key) DO UPDATE SET
                    source_path=excluded.source_path,
                    source_sha256=excluded.source_sha256,
                    imported_at=excluded.imported_at
                """,
                (import_key, str(Path(source_path).resolve()), source_sha256, _now()),
            )

    def plan_summary(self) -> dict[str, Any]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT stage, status, COUNT(*) AS count FROM stage_work_items
                WHERE is_current=1 GROUP BY stage, status ORDER BY stage, status
                """
            ).fetchall()
            selections = connection.execute(
                """
                SELECT copy_state, COUNT(*) AS count FROM corpus_selections
                WHERE active=1 GROUP BY copy_state ORDER BY copy_state
                """
            ).fetchall()
        stages: dict[str, dict[str, int]] = {}
        for row in rows:
            stages.setdefault(row["stage"], {})[row["status"]] = int(row["count"])
        return {
            "selections": {row["copy_state"]: int(row["count"]) for row in selections},
            "stages": stages,
        }

    def export_audit_files(self) -> dict[str, Any]:
        with self.connect() as connection:
            selection_rows = [dict(row) for row in connection.execute(
                "SELECT * FROM corpus_selections ORDER BY selection_event_ordinal"
            )]
            attempt_rows = [dict(row) for row in connection.execute(
                "SELECT * FROM stage_attempts ORDER BY started_at, attempt_id"
            )]
            unresolved = [dict(row) for row in connection.execute(
                """
                SELECT * FROM stage_work_items WHERE is_current=1
                  AND status IN ('pending','running','retryable_failed','blocked_by_upstream','stale')
                ORDER BY outer_batch_id, stage, paper_id, document_id
                """
            )]
        summary = self.plan_summary()
        write_json(self.root / "resume_summary.json", summary)
        write_jsonl(self.root / "selection_ledger.jsonl", selection_rows)
        write_jsonl(self.root / "attempts.jsonl", attempt_rows)
        write_jsonl(self.root / "unresolved.jsonl", unresolved)
        return summary

    def start_lease(self, *, owner_id: str, generation: int, command_hash: str, **identity) -> None:
        now = _now()
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO run_leases(
                    owner_id, owner_pid, hostname, boot_id, process_start_ticks,
                    heartbeat_at, command_hash, resume_generation, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'running', ?)
                """,
                (
                    owner_id,
                    identity["pid"],
                    identity["hostname"],
                    identity["boot_id"],
                    identity["process_start_ticks"],
                    now,
                    command_hash,
                    int(generation),
                    now,
                ),
            )

    def heartbeat_lease(self, owner_id: str) -> None:
        with self.transaction() as connection:
            connection.execute(
                "UPDATE run_leases SET heartbeat_at=? WHERE owner_id=? AND status='running'",
                (_now(), owner_id),
            )

    def finish_lease(self, owner_id: str, *, status: str) -> None:
        with self.transaction() as connection:
            connection.execute(
                "UPDATE run_leases SET status=?, heartbeat_at=? WHERE owner_id=?",
                (status, _now(), owner_id),
            )

    def reconcile_interrupted_work(self) -> int:
        with self.transaction() as connection:
            active = connection.execute(
                "SELECT owner_id FROM run_leases WHERE status='running'"
            ).fetchall()
            # The OS lock is authoritative. Any prior running DB lease observed
            # after acquiring that lock is from an interrupted process.
            for row in active:
                connection.execute(
                    "UPDATE run_leases SET status='interrupted_external', heartbeat_at=? WHERE owner_id=?",
                    (_now(), row["owner_id"]),
                )
            cursor = connection.execute(
                """
                UPDATE stage_work_items SET status='retryable_failed',
                    failure_class='interrupted_external', updated_at=?
                WHERE status='running'
                """,
                (_now(),),
            )
        return int(cursor.rowcount)

    def _artifacts_valid(self, connection, work_item_id: str) -> bool:
        work_item = connection.execute(
            "SELECT result_json FROM stage_work_items WHERE work_item_id=?",
            (work_item_id,),
        ).fetchone()
        result = _loads(work_item["result_json"]) if work_item else None
        for key in (
            "normalized_markdown_path",
            "content_blocks_path",
            "output_path",
            "markdown_path",
        ):
            value = (result or {}).get(key)
            if value and not Path(str(value)).is_file():
                return False
        rows = connection.execute(
            """
            SELECT artifact_manifests.* FROM artifact_manifests
            JOIN stage_work_items
              ON stage_work_items.work_item_id=artifact_manifests.work_item_id
             AND stage_work_items.current_attempt_id=artifact_manifests.attempt_id
            WHERE artifact_manifests.work_item_id=? AND artifact_manifests.required=1
            """,
            (work_item_id,),
        ).fetchall()
        for row in rows:
            path = Path(row["path"])
            if not path.is_file() or path.stat().st_size != int(row["size_bytes"]):
                return False
            if sha256_file(path) != row["sha256"]:
                return False
        return True

    @staticmethod
    def _paper_was_terminally_pruned(connection, paper_id: str) -> bool:
        row = connection.execute(
            """
            SELECT 1 FROM corpus_selections
            WHERE paper_id=? AND active=1 AND local_assets_state='pruned_terminal'
            LIMIT 1
            """,
            (paper_id,),
        ).fetchone()
        return row is not None

    def _initialize(self) -> None:
        with self.transaction() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS corpus_selections(
                    selection_id TEXT PRIMARY KEY,
                    dataset TEXT NOT NULL,
                    source_main_uri TEXT NOT NULL,
                    normalized_doi TEXT,
                    source_record_key TEXT,
                    paper_id TEXT,
                    source_sha256 TEXT,
                    target_slot_ordinal INTEGER NOT NULL,
                    selection_event_ordinal INTEGER NOT NULL UNIQUE,
                    replaces_selection_id TEXT,
                    outer_batch_id TEXT NOT NULL,
                    selected_at TEXT NOT NULL,
                    copy_state TEXT NOT NULL,
                    local_assets_state TEXT NOT NULL,
                    last_error_json TEXT NOT NULL DEFAULT '{}',
                    active INTEGER NOT NULL DEFAULT 1,
                    updated_at TEXT NOT NULL,
                    UNIQUE(dataset, source_main_uri)
                );
                CREATE UNIQUE INDEX IF NOT EXISTS corpus_selection_active_slot_idx
                    ON corpus_selections(target_slot_ordinal) WHERE active=1;
                CREATE UNIQUE INDEX IF NOT EXISTS corpus_selection_active_doi_idx
                    ON corpus_selections(dataset, normalized_doi)
                    WHERE active=1 AND normalized_doi IS NOT NULL AND normalized_doi!='';
                CREATE TABLE IF NOT EXISTS stage_work_items(
                    work_item_id TEXT PRIMARY KEY,
                    outer_batch_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    document_id TEXT NOT NULL DEFAULT '',
                    config_fingerprint TEXT NOT NULL,
                    input_fingerprint TEXT NOT NULL,
                    status TEXT NOT NULL,
                    failure_class TEXT,
                    result_json TEXT,
                    current_attempt_id TEXT,
                    is_current INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(outer_batch_id, stage, paper_id, document_id, config_fingerprint)
                );
                CREATE INDEX IF NOT EXISTS stage_work_current_idx
                    ON stage_work_items(outer_batch_id, stage, status, is_current);
                CREATE TABLE IF NOT EXISTS stage_attempts(
                    attempt_id TEXT PRIMARY KEY,
                    work_item_id TEXT NOT NULL,
                    resume_generation INTEGER NOT NULL,
                    stage TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    document_id TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL,
                    failure_class TEXT,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    runtime_fingerprint TEXT NOT NULL,
                    result_json TEXT,
                    error_json TEXT NOT NULL,
                    imported INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(work_item_id) REFERENCES stage_work_items(work_item_id)
                );
                CREATE TABLE IF NOT EXISTS artifact_manifests(
                    artifact_id TEXT PRIMARY KEY,
                    work_item_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    path TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    sha256 TEXT NOT NULL,
                    required INTEGER NOT NULL DEFAULT 1,
                    recorded_at TEXT NOT NULL,
                    FOREIGN KEY(work_item_id) REFERENCES stage_work_items(work_item_id),
                    FOREIGN KEY(attempt_id) REFERENCES stage_attempts(attempt_id)
                );
                CREATE TABLE IF NOT EXISTS run_leases(
                    owner_id TEXT PRIMARY KEY,
                    owner_pid INTEGER NOT NULL,
                    hostname TEXT NOT NULL,
                    boot_id TEXT NOT NULL,
                    process_start_ticks TEXT NOT NULL,
                    heartbeat_at TEXT NOT NULL,
                    command_hash TEXT NOT NULL,
                    resume_generation INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS resume_generations(
                    generation INTEGER PRIMARY KEY,
                    command_hash TEXT NOT NULL,
                    total_target INTEGER NOT NULL,
                    start_stage TEXT NOT NULL,
                    stop_stage TEXT NOT NULL,
                    invalidated_stages_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS import_events(
                    import_key TEXT PRIMARY KEY,
                    source_path TEXT NOT NULL,
                    source_sha256 TEXT NOT NULL,
                    imported_at TEXT NOT NULL
                );
                """
            )

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=60)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=60000")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    @contextmanager
    def transaction(self):
        with self._lock:
            connection = self.connect()
            try:
                connection.execute("BEGIN IMMEDIATE")
                yield connection
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                connection.close()


def scientific_stage_fingerprints(config: dict[str, Any]) -> dict[str, str]:
    """Hash scientific semantics while excluding endpoints, credentials and concurrency."""

    from src.prompts import (
        STAGE02_CLASSIFY_VERSION,
        STAGE02_PASS_VERIFY_VERSION,
        STAGE03_VERSION,
        STAGE05_ROUTER_VERSION,
        STAGE05_VERSION,
    )
    from src.stages.stage00_remote_corpus.remote import STAGE00_SCHEMA_VERSION
    from src.stages.stage01_document_preparation.normalization import (
        DOCUMENT_NORMALIZATION_IMPLEMENTATION_VERSION,
    )
    from src.stages.stage02_computational_content.stage import (
        COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION,
    )

    models = config.get("models") or {}
    stage_models = {
        "stage02": models.get((config.get("stage02") or {}).get("model_role", "screening")) or {},
        "stage03": models.get((config.get("stage03") or {}).get("model_role", "screening")) or {},
        "stage05_router": models.get("stage05_router") or {},
        "stage05_auditor": models.get("suitability") or {},
        "stage05": models.get("suitability") or {},
    }
    output = {}
    for stage in ("stage00", "stage01", "stage02", "stage03", "stage04", "stage05"):
        stage_config = config.get(stage) or {}
        if stage == "stage01":
            stage_config = config.get("stage01") or {}
        payload: dict[str, Any] = {"stage": stage, "config": _scientific_value(stage_config)}
        if stage in stage_models:
            payload["model"] = _scientific_model(stage_models[stage])
        if stage == "stage05":
            payload["router_model"] = _scientific_model(stage_models["stage05_router"])
        payload["implementation"] = {
            "stage00": STAGE00_SCHEMA_VERSION,
            "stage01": DOCUMENT_NORMALIZATION_IMPLEMENTATION_VERSION,
            "stage02": COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION,
            "stage03": STAGE03_VERSION,
            "stage04": "stage04-mineru-normalization-v2",
            "stage05": STAGE05_VERSION,
        }[stage]
        if stage == "stage02":
            payload["prompts"] = [STAGE02_CLASSIFY_VERSION, STAGE02_PASS_VERIFY_VERSION]
        if stage == "stage03":
            payload["capability_files"] = [
                _file_fingerprint(stage_config.get(key))
                for key in (
                    "toolbox_capabilities",
                    "software_aliases",
                    "external_software_aliases",
                )
                if stage_config.get(key)
            ]
        if stage == "stage04":
            environment = (stage_config.get("mineru") or {}).get("environment") or {}
            payload["external_files"] = [
                _file_fingerprint(value)
                for key, value in sorted(environment.items())
                if key.endswith("_CONFIG_JSON") and value
            ]
        if stage == "stage05":
            payload["prompts"] = [STAGE05_ROUTER_VERSION, STAGE05_VERSION]
        output[stage] = canonical_hash(payload)
    output["stage01_package"] = canonical_hash(
        {
            "stage": "stage01_package",
            "config": _scientific_value((config.get("stage01") or {}).get("package") or {}),
            "implementation": "stage01-paper-package-v2",
        }
    )
    output["stage05_router"] = canonical_hash(
        {
            "stage": "stage05_router",
            "config": _scientific_value(config.get("stage05") or {}),
            "model": _scientific_model(stage_models["stage05_router"]),
            "prompt": STAGE05_ROUTER_VERSION,
        }
    )
    output["stage05_auditor"] = canonical_hash(
        {
            "stage": "stage05_auditor",
            "config": _scientific_value(config.get("stage05") or {}),
            "model": _scientific_model(stage_models["stage05_auditor"]),
            "prompt": STAGE05_VERSION,
        }
    )
    return output


def input_fingerprint(*values: Any) -> str:
    return canonical_hash(values)


def stable_input_value(value: Any) -> Any:
    volatile = {
        "created_at",
        "run_id",
        "model_audit",
        "model_response_attempts",
        "parser_output",
        "updated_at",
    }
    if isinstance(value, dict):
        return {
            key: stable_input_value(item)
            for key, item in sorted(value.items())
            if key not in volatile
        }
    if isinstance(value, list):
        return [stable_input_value(item) for item in value]
    return value


def document_input_fingerprint(document: dict[str, Any]) -> str:
    return input_fingerprint(
        {
            "paper_id": document.get("paper_id"),
            "document_id": document.get("document_id"),
            "sha256": document.get("sha256"),
            "source_path": document.get("source_path"),
            "document_role": document.get("document_role"),
        }
    )


def paper_input_fingerprint(
    paper: dict[str, Any], documents: Iterable[dict[str, Any]]
) -> str:
    return input_fingerprint(
        stable_input_value(paper),
        [
            stable_input_value(document)
            for document in sorted(
                documents, key=lambda row: str(row.get("document_id") or "")
            )
        ],
    )


def result_artifacts(row: dict[str, Any]) -> list[str]:
    output = []
    for key in (
        "normalized_markdown_path",
        "content_blocks_path",
        "output_path",
        "markdown_path",
    ):
        value = row.get(key)
        if value and Path(str(value)).is_file():
            output.append(str(Path(str(value)).resolve()))
    return output


def _scientific_value(value: Any) -> Any:
    runtime_keys = {
        "api_concurrency",
        "base_url",
        "buffer_size",
        "cache",
        "cleanup",
        "connect_timeout_seconds",
        "credentials",
        "lifecycle_minutes",
        "manage_service",
        "network_workers",
        "outside",
        "proxy_url_env",
        "read_timeout_seconds",
        "retries",
        "service_log",
        "startup_timeout_seconds",
        "timeout_seconds",
        "use_proxy",
        "workers",
        "working_directory",
    }
    if isinstance(value, dict):
        return {
            key: _scientific_value(item)
            for key, item in sorted(value.items())
            if key not in runtime_keys and not key.startswith("_")
        }
    if isinstance(value, list):
        return [_scientific_value(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _scientific_model(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: _scientific_value(value.get(key))
        for key in ("model", "max_tokens", "thinking", "chat_template_kwargs")
        if value.get(key) is not None
    }


def _artifact(path: str | Path) -> dict[str, Any]:
    source = Path(path).expanduser().resolve()
    return {
        "path": str(source),
        "size_bytes": source.stat().st_size,
        "sha256": sha256_file(source),
    }


def _file_fingerprint(value: str | Path) -> dict[str, Any]:
    path = Path(str(value)).expanduser().resolve()
    result = {"path": str(path), "exists": path.is_file()}
    if path.is_file():
        result.update({"size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return result


def _normalize_doi(value: str | None) -> str:
    text = str(value or "").strip().casefold()
    return text.removeprefix("https://doi.org/").removeprefix("doi:").strip()


def _parent_stage(stage: str) -> str:
    if stage == "stage01_package":
        return "stage01"
    if stage in {"stage05_router", "stage05_auditor"}:
        return "stage05"
    return stage


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _loads(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

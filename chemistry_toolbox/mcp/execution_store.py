"""Durable run-scoped submission identities and replayable execution receipts.

The execution store deliberately records facts about a submission before the
toolbox starts a child process.  It does not attempt to make ``Popen`` and a
database transaction atomic; callers must reconcile a ``launching`` record
before starting a replacement process.
"""

from __future__ import annotations

from chemistry_toolbox.src.execution_states import TERMINAL_STATES, ALLOWED_TRANSITIONS, validate_state

import hashlib
import json
import os
import re
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .workspace import workspace_root
from chemistry_toolbox.src.recovery_io import control_directory


_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$")
_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$")
_LOCAL = threading.local()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    """Serialize a JSON-compatible value in a stable, hashable form."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def request_fingerprint(request: Any, input_manifest: Any | None = None) -> str:
    """Return a stable fingerprint for the requested side effect.

    Timestamps, process IDs and credentials are intentionally not accepted as
    implicit inputs.  Callers should pass only the normalized request and a
    content-addressed input manifest.
    """

    if hasattr(request, "model_dump"):
        request = request.model_dump(mode="json")
    payload = {"request": request, "input_manifest": input_manifest or []}
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


class SubmissionConflict(ValueError):
    """The same submission key was reused for a different request."""

    def __init__(self, *, run_id: str, submission_key: str, existing: dict[str, Any]):
        super().__init__(
            f"submission_key {submission_key!r} already belongs to a different request "
            f"in run {run_id!r}"
        )
        self.run_id = run_id
        self.submission_key = submission_key
        self.existing = existing


@dataclass(frozen=True)
class SubmissionReceipt:
    run_id: str
    submission_key: str
    entity_id: str
    entity_type: str
    receipt_id: str
    request_fingerprint: str
    accepted_at: str
    replayed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "submission_key": self.submission_key,
            "job_id": self.entity_id if self.entity_type == "job" else None,
            "batch_id": self.entity_id if self.entity_type == "batch" else None,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "receipt_id": self.receipt_id,
            "request_fingerprint": self.request_fingerprint,
            "accepted_at": self.accepted_at,
            "replayed": self.replayed,
        }


class ExecutionStore:
    """A small SQLite store scoped to one benchmark workspace and run."""

    schema_version = 2

    def __init__(self, root: Path, *, run_id: str, read_only: bool = False):
        self.root = Path(root).expanduser().resolve()
        self.run_id = self._validate_run_id(run_id)
        self.directory = control_directory(self.root, self.run_id)
        self.read_only = read_only
        self.path = self.directory / "execution.sqlite3"
        if not read_only:
            self.directory.mkdir(parents=True, exist_ok=True)
            self._initialize()

    @classmethod
    def for_workspace(cls, *, run_id: str | None = None) -> "ExecutionStore":
        value = run_id or os.environ.get("RESEARCHCHEMBENCH_RUN_ID") or "legacy"
        return cls(workspace_root(), run_id=value)

    @classmethod
    def open_existing(cls, root: Path, *, run_id: str | None = None) -> "ExecutionStore | None":
        """Open a live or portable control database without creating any files."""
        root = Path(root).expanduser().resolve()
        if run_id is None:
            meta = root / "_meta.json"
            try:
                run_id = json.loads(meta.read_text()).get("run_id") if meta.is_file() else None
            except (OSError, json.JSONDecodeError):
                return None
        if not run_id:
            return None
        store = cls(root, run_id=run_id, read_only=True)
        archive = root.parent / "control" / "execution.sqlite3"
        if archive.is_file():
            store.path, store.directory = archive, archive.parent
        return store if store.path.is_file() else None

    def execution_snapshot(self) -> list[dict[str, Any]]:
        """Read states and identity metadata in one consistent database snapshot."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT j.*, p.spec_json, s.request_json FROM jobs j "
                "LEFT JOIN job_specs p ON p.entity_id = j.entity_id "
                "LEFT JOIN submissions s ON s.entity_id = j.entity_id AND s.run_id = j.run_id "
                "WHERE j.run_id = ? ORDER BY j.entity_id", (self.run_id,),
            ).fetchall()
        result = []
        for row in rows:
            value = dict(row)
            value["spec"] = json.loads(value.pop("spec_json") or "{}")
            value["request"] = json.loads(value.pop("request_json") or "{}")
            result.append(value)
        return result

    @staticmethod
    def _validate_run_id(value: str) -> str:
        normalized = str(value).strip()
        if not _RUN_ID.fullmatch(normalized):
            raise ValueError("run_id must contain only letters, digits, '.', '_' ':' or '-'")
        return normalized

    @staticmethod
    def validate_submission_key(value: str) -> str:
        normalized = str(value).strip()
        if not _KEY.fullmatch(normalized):
            raise ValueError(
                "submission_key must start with an alphanumeric character and contain "
                "only letters, digits, '.', '_' ':' or '-'"
            )
        return normalized

    @contextmanager
    def _connect(self):
        connection = sqlite3.connect(self.path.as_uri() + "?mode=ro" if self.read_only else self.path,
                                     uri=self.read_only, timeout=30.0, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        # Rollback journal avoids WAL mmap on the shared HDD. This is a
        # single-host store and still requires working POSIX locks/fsync.
        if not self.read_only:
            connection.execute("PRAGMA synchronous = FULL")
        try:
            yield connection
            if connection.in_transaction:
                connection.commit()
        except BaseException:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS store_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            version = connection.execute("SELECT value FROM store_meta WHERE key = 'schema_version'").fetchone()
            if version and int(version[0]) > self.schema_version:
                raise ValueError("execution store schema is newer than this installation")
            if version and int(version[0]) == self.schema_version:
                return
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS store_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS submissions (
                    run_id TEXT NOT NULL,
                    submission_key TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    request_fingerprint TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    input_manifest_json TEXT NOT NULL,
                    receipt_id TEXT NOT NULL,
                    accepted_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    state TEXT NOT NULL,
                    PRIMARY KEY (run_id, submission_key),
                    UNIQUE (entity_id),
                    UNIQUE (receipt_id)
                );
                CREATE TABLE IF NOT EXISTS jobs (
                    entity_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    submission_key TEXT,
                    entity_type TEXT NOT NULL,
                    state TEXT NOT NULL,
                    host TEXT,
                    boot_id TEXT,
                    pid INTEGER,
                    start_ticks INTEGER,
                    launch_token TEXT,
                    state_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS execution_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    entity_id TEXT,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS records (namespace TEXT NOT NULL, key TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(namespace, key));
                CREATE TABLE IF NOT EXISTS job_specs (entity_id TEXT PRIMARY KEY, spec_json TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS jobs_run_state_idx
                    ON jobs(run_id, state);
                CREATE INDEX IF NOT EXISTS events_run_idx
                    ON execution_events(run_id, sequence);
                """
            )
            connection.execute(
                "INSERT OR REPLACE INTO store_meta(key, value) VALUES('schema_version', ?)",
                (str(self.schema_version),),
            )

    @staticmethod
    def _row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
        return dict(row) if row is not None else None

    def _submission_row(self, connection: sqlite3.Connection, key: str) -> dict[str, Any] | None:
        row = connection.execute(
            "SELECT * FROM submissions WHERE run_id = ? AND submission_key = ?",
            (self.run_id, key),
        ).fetchone()
        return self._row_dict(row)

    def accept_submission(
        self,
        *,
        submission_key: str,
        entity_type: str,
        request: Any,
        input_manifest: Any | None = None,
        entity_prefix: str = "job",
        spec: dict[str, Any] | None = None,
    ) -> SubmissionReceipt:
        """Record or replay a side-effect submission atomically."""

        key = self.validate_submission_key(submission_key)
        if entity_type not in {"job", "batch"}:
            raise ValueError("entity_type must be 'job' or 'batch'")
        request_value = request.model_dump(mode="json") if hasattr(request, "model_dump") else request
        manifest_value = input_manifest or []
        fingerprint = request_fingerprint(request_value, manifest_value)
        now = _now()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = self._submission_row(connection, key)
            if existing is not None:
                if existing["request_fingerprint"] != fingerprint:
                    raise SubmissionConflict(
                        run_id=self.run_id,
                        submission_key=key,
                        existing=existing,
                    )
                return SubmissionReceipt(
                    run_id=self.run_id,
                    submission_key=key,
                    entity_id=existing["entity_id"],
                    entity_type=existing["entity_type"],
                    receipt_id=existing["receipt_id"],
                    request_fingerprint=existing["request_fingerprint"],
                    accepted_at=existing["accepted_at"],
                    replayed=True,
                )

            prefix = "batch" if entity_type == "batch" else entity_prefix
            entity_id = f"{prefix}_{uuid.uuid4().hex}"
            receipt_id = f"receipt_{uuid.uuid4().hex}"
            request_json = canonical_json(request_value)
            manifest_json = canonical_json(manifest_value)
            connection.execute(
                """
                INSERT INTO submissions(
                    run_id, submission_key, entity_id, entity_type,
                    request_fingerprint, request_json, input_manifest_json,
                    receipt_id, accepted_at, updated_at, state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'accepted')
                """,
                (
                    self.run_id,
                    key,
                    entity_id,
                    entity_type,
                    fingerprint,
                    request_json,
                    manifest_json,
                    receipt_id,
                    now,
                    now,
                ),
            )
            connection.execute(
                """
                INSERT INTO jobs(
                    entity_id, run_id, submission_key, entity_type, state,
                    state_json, updated_at
                ) VALUES (?, ?, ?, ?, 'accepted', ?, ?)
                """,
                (
                    entity_id,
                    self.run_id,
                    key,
                    entity_type,
                    canonical_json({"state": "accepted", "accepted_at": now}),
                    now,
                ),
            )
            if spec is not None:
                connection.execute("INSERT INTO job_specs VALUES (?, ?)", (entity_id, canonical_json(spec)))
                connection.execute("UPDATE jobs SET state = 'queued', state_json = ? WHERE entity_id = ?",
                    (canonical_json({"state": "queued", "accepted_at": now, "queued_at": now}), entity_id))
            self._append_event(
                connection,
                entity_id=entity_id,
                event_type="submission_accepted",
                payload={
                    "run_id": self.run_id,
                    "submission_key": key,
                    "entity_type": entity_type,
                    "request_fingerprint": fingerprint,
                    "receipt_id": receipt_id,
                },
                created_at=now,
            )
            return SubmissionReceipt(
                run_id=self.run_id,
                submission_key=key,
                entity_id=entity_id,
                entity_type=entity_type,
                receipt_id=receipt_id,
                request_fingerprint=fingerprint,
                accepted_at=now,
                replayed=False,
            )

    @staticmethod
    def _append_event(
        connection: sqlite3.Connection,
        *,
        entity_id: str | None,
        event_type: str,
        payload: dict[str, Any],
        created_at: str,
    ) -> None:
        connection.execute(
            """
            INSERT INTO execution_events(run_id, entity_id, event_type, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload.get("run_id") or "",
                entity_id,
                event_type,
                canonical_json(payload),
                created_at,
            ),
        )

    def record_job_state(
        self,
        entity_id: str,
        state: str,
        *,
        state_payload: dict[str, Any] | None = None,
        event_type: str = "job_state_changed",
        expected_state: str | None = None,
        expected_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        validate_state(state)
        payload = {**(state_payload or {}), "state": state}
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM jobs WHERE entity_id = ? AND run_id = ?",
                (entity_id, self.run_id),
            ).fetchone()
            if row is None:
                raise KeyError(f"Unknown execution entity {entity_id!r}")
            old = row["state"]
            if expected_state is not None and old != expected_state:
                return dict(row)
            if expected_snapshot is not None and any(
                row[key] != expected_snapshot[key]
                for key in ("state", "state_json", "updated_at", "launch_token")
            ):
                return dict(row)
            terminal = TERMINAL_STATES
            if old in terminal and state != old:
                return dict(row)
            allowed = ALLOWED_TRANSITIONS
            if state != old and state not in allowed.get(old, set()):
                raise ValueError(f"illegal execution transition: {old} -> {state}")
            payload = {**json.loads(row["state_json"]), **payload}
            if row["state"] == state and row["state_json"] == canonical_json(payload):
                return dict(row)
            now = _now()
            connection.execute(
                "UPDATE jobs SET state = ?, state_json = ?, updated_at = ? "
                "WHERE entity_id = ? AND run_id = ?",
                (state, canonical_json(payload), now, entity_id, self.run_id),
            )
            identity = payload.get("supervisor_identity") or {}
            connection.execute("UPDATE jobs SET host=?, boot_id=?, pid=?, start_ticks=?, launch_token=? WHERE entity_id=?",
                (identity.get("host"), identity.get("boot_id"), identity.get("pid"), identity.get("start_ticks"), payload.get("launch_token"), entity_id))
            self._append_event(
                connection,
                entity_id=entity_id,
                event_type=event_type,
                payload={"run_id": self.run_id, **payload},
                created_at=now,
            )
        return {"entity_id": entity_id, "state": state, **payload, "updated_at": now}

    def get_submission(self, submission_key: str) -> dict[str, Any] | None:
        key = self.validate_submission_key(submission_key)
        with self._connect() as connection:
            row = self._submission_row(connection, key)
            if row is None:
                return None
            job = connection.execute(
                "SELECT * FROM jobs WHERE entity_id = ? AND run_id = ?",
                (row["entity_id"], self.run_id),
            ).fetchone()
            result = dict(row)
            if job is not None:
                result["job"] = dict(job)
            result["request"] = json.loads(result.pop("request_json"))
            result["input_manifest"] = json.loads(result.pop("input_manifest_json"))
            return result

    def list_submissions(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT submission_key, entity_id, entity_type, receipt_id, accepted_at "
                "FROM submissions WHERE run_id = ? ORDER BY accepted_at, entity_id",
                (self.run_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_jobs(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM jobs WHERE run_id = ? ORDER BY updated_at, entity_id",
                (self.run_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_job(self, entity_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM jobs WHERE run_id=? AND entity_id=?", (self.run_id, entity_id)).fetchone()
            return dict(row) if row else None

    def spec(self, entity_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute("SELECT spec_json FROM job_specs WHERE entity_id=?", (entity_id,)).fetchone()
            return json.loads(row[0]) if row else None

    def get_record(self, namespace: str, key: str, default=None):
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM records WHERE namespace=? AND key=?", (namespace, key)).fetchone()
            return json.loads(row[0]) if row else default

    def put_record(self, namespace: str, key: str, value, *, immutable=False):
        return self.put_records([(namespace, key, value)], immutable=immutable)[0]

    def put_records(self, records, *, immutable=False):
        """Commit related control records together (e.g. attempt and run identity)."""
        values = []
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            for namespace, key, value in records:
                old = connection.execute("SELECT payload FROM records WHERE namespace=? AND key=?", (namespace, key)).fetchone()
                if old and (immutable or old[0] == canonical_json(value)):
                    values.append(json.loads(old[0]))
                    continue
                connection.execute("INSERT OR REPLACE INTO records VALUES (?, ?, ?)", (namespace, key, canonical_json(value)))
                self._append_event(connection, entity_id=None, event_type=namespace, payload={"run_id": self.run_id, "key": key, "value": value}, created_at=_now())
                values.append(value)
        return values

    def records(self, namespace: str) -> dict:
        with self._connect() as connection:
            rows = connection.execute("SELECT key, payload FROM records WHERE namespace=? ORDER BY key", (namespace,)).fetchall()
            return {r[0]: json.loads(r[1]) for r in rows}

    def usage(self) -> dict[str, int]:
        details = self.usage_details()
        return details["budget_usage"]

    def usage_details(self) -> dict:
        sessions, epochs, reported = {}, {}, {}
        for event_id, value in self.records("usage").items():
            session = str(value.get("session_id") or event_id.split(":")[0])
            totals = sessions.setdefault(session, {"input_tokens": 0, "output_tokens": 0, "turns": 0})
            reported.setdefault(session, set()).update(value.get("reported_fields", value))
            for key in totals: totals[key] += int(value.get(key) or 0)
        streams = list(self.records("usage_stream").values())
        native_streams = [s for s in streams if s.get("kind") == "native" and not s.get("identity_error")]
        for stream in native_streams:
            session = stream["session_id"]
            for epoch, counts in stream.get("segments", {}).items():
                target = epochs.setdefault((session, epoch), {})
                for key, count in counts.items(): target[key] = max(target.get(key, 0), count)
        native = {}
        for (session, _), counts in epochs.items():
            target = native.setdefault(session, {})
            for key, count in counts.items(): target[key] = target.get(key, 0) + count
        for session, counts in native.items():
            target = sessions.setdefault(session, {"input_tokens": 0, "output_tokens": 0, "turns": 0})
            for key in ("input_tokens", "output_tokens"):
                # Native counters are authoritative for this session. Adding or
                # maxing ambiguous CLI summaries can count repeated totals twice.
                target[key] = counts.get(key, target[key])
            reported.setdefault(session, set()).update(counts)
        totals = {key: sum(s[key] for s in sessions.values()) for key in ("input_tokens", "output_tokens", "turns")}
        floor = self.get_record("usage_floor", "native_session", {})
        for key in ("input_tokens", "output_tokens"):
            totals[key] = max(totals[key], int(floor.get(key) or 0))
        details = {**totals, "input_total_tokens": totals["input_tokens"],
                   "budget_usage": dict(totals),
                   "total_tokens": totals["input_tokens"] + totals["output_tokens"], "by_session": sessions,
                   "budget_basis": "input_total_tokens + output_tokens (including cached input)",
                   "model_request_count": None, "agent_completed_turns": totals["turns"],
                   "last_event_at": max((s.get("last_event_at") or "" for s in native_streams), default="") or None,
                   "source": "provider_reported_events", "cost_available": False}
        for key in ("cached_input_tokens", "cache_write_input_tokens", "reasoning_output_tokens"):
            details[key] = sum(n[key] for n in native.values()) if native and all(key in n for n in native.values()) and len(native) == len(sessions) else None
        incomplete = any(s.get(k) for s in streams for k in ("discontinuity", "malformed_events", "identity_error", "invalid_counter", "read_error", "oversize_events", "backlog_bytes"))
        details["accounting_status"] = "partial" if incomplete else "reported" if sessions or floor else "unavailable"
        for field in ("input_tokens", "output_tokens"):
            if not (sessions and all(field in reported.get(s, ()) for s in sessions)) and field not in floor:
                details[field] = None
                if details["accounting_status"] == "reported": details["accounting_status"] = "partial"
        details["input_total_tokens"] = details["input_tokens"]
        details["total_tokens"] = details["input_tokens"] + details["output_tokens"] if details["input_tokens"] is not None and details["output_tokens"] is not None else None
        if details["accounting_status"] == "unavailable": details["agent_completed_turns"] = None
        details["counting_note"] = "Native cumulative and stdout incremental counters overlap and are not added. Cache/reasoning fields are subsets or provider-specific; unavailable values are null."
        request_ids = {(s["session_id"], identity) for s in native_streams for identity in s.get("request_ids", {})}
        details["model_request_count"] = len(request_ids) if native_streams and request_ids and not any(s.get("requests_without_identity") for s in native_streams) else None
        details["model_request_count_source"] = "provider_request_ids" if details["model_request_count"] is not None else "unavailable"
        # Multiple copies of a session must not double inferred steps/attribution.
        selected_streams = {}
        for stream in native_streams:
            session = stream["session_id"]
            if stream.get("observable_model_steps", 0) >= selected_streams.get(session, {}).get("observable_model_steps", -1):
                selected_streams[session] = stream
        details["observable_model_steps"] = sum(s.get("observable_model_steps", 0) for s in selected_streams.values()) if selected_streams else None
        details["observable_model_steps_source"] = "positive_provider_counter_updates; not an exact request count"
        details["usage_attribution"] = {group: {key: sum(s.get("attribution", {}).get(group, {}).get(key, 0) for s in selected_streams.values())
            for key in ("input_tokens", "output_tokens", "cached_input_tokens", "reasoning_output_tokens")} for group in ("inferred_wait", "unknown")}
        for field in ("input_tokens", "output_tokens", "cached_input_tokens", "reasoning_output_tokens"):
            total = details.get(field)
            if total is None or details["accounting_status"] == "unavailable":
                for group in details["usage_attribution"].values(): group[field] = None
            else:
                wait_value = min(total, details["usage_attribution"]["inferred_wait"][field])
                details["usage_attribution"]["inferred_wait"][field] = wait_value
                details["usage_attribution"]["unknown"][field] = total - wait_value
        calls = {(s["session_id"], k): v for s in native_streams for k, v in s.get("tool_calls", {}).items()}
        details["host_tool_call_count"] = len(calls) if native_streams else None
        details["tool_round_count"] = len({v["response_id"] for v in calls.values()}) if calls and all(v.get("response_id") for v in calls.values()) else None
        return details


def execution_store() -> ExecutionStore:
    """Return the store for the active MCP workspace and benchmark run."""

    return ExecutionStore.for_workspace()


__all__ = [
    "ExecutionStore",
    "SubmissionConflict",
    "SubmissionReceipt",
    "canonical_json",
    "execution_store",
    "request_fingerprint",
]

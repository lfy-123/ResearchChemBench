"""Incremental usage ingestion for live, final and recovery paths.

Only provider-reported counters are accounted. Cursor and counters live in one
atomic record; native cumulative counters and stdout turn increments are never
added together for the same session.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from chemistry_toolbox.src.recovery_io import file_lock

FIELDS = ("input_tokens", "output_tokens", "cached_input_tokens", "cache_write_input_tokens", "reasoning_output_tokens", "total_tokens")


def record_turn(store, session_id, event_id, event):
    usage = event.get("usage") or {}
    store.put_record("usage", str(session_id) + ":" + str(event_id), {
        "session_id": session_id, "input_tokens": int(usage.get("input_tokens") or 0),
        "output_tokens": int(usage.get("output_tokens") or 0), "turns": 1,
        "reported_fields": {k: int(usage[k]) for k in FIELDS if usage.get(k) is not None},
    }, immutable=True)


def ingest_file(store, path: Path, *, session_id: str, kind="native", attempt_id="", max_bytes=8 * 1024 * 1024):
    if max_bytes < 1:
        raise ValueError("max_bytes must be positive")
    key = hashlib.sha256((kind + str(path.resolve())).encode()).hexdigest()
    with file_lock(store.directory / "usage_locks" / (key + ".lock")):
        old = store.get_record("usage_stream", key, {})
        value = json.loads(json.dumps(old)) if old else {"session_id": session_id, "kind": kind, "offset": 0, "segments": {}, "turn_sequence": 0}
        try:
            stat = path.stat()
            with path.open("rb") as handle:
                prefix_length = value.get("prefix_length") or min(stat.st_size, 128)
                prefix = hashlib.sha256(handle.read(prefix_length)).hexdigest()
                identity = [stat.st_dev, stat.st_ino]
                if old and (old.get("identity") != identity or stat.st_size < old["offset"] or
                            (old.get("prefix_length") and old.get("prefix_hash") != prefix)):
                    value.update(offset=0, turn_sequence=0, discontinuity=True, skipping_oversize=False)
                    value.pop("identity_error", None)
                value.update(identity=identity, prefix_length=prefix_length, prefix_hash=prefix)
                handle.seek(value["offset"])
                start = handle.tell()
                line_limit = min(2 * 1024 * 1024, max_bytes)
                while handle.tell() - start < max_bytes and not value.get("identity_error"):
                    read_limit = min(line_limit, max_bytes - (handle.tell() - start))
                    line = handle.readline(read_limit)
                    if not line: break
                    if value.get("skipping_oversize"):
                        value["offset"] = handle.tell()
                        value["skipping_oversize"] = not line.endswith(b"\n")
                        continue
                    if not line.endswith(b"\n"):
                        # Ordinary partial lines are retried. An oversized line
                        # is skipped incrementally; persist that state so a large
                        # tool output cannot make one refresh read without bound.
                        if len(line) == line_limit:
                            value["skipping_oversize"] = True
                            value["offset"] = handle.tell()
                            value["oversize_events"] = value.get("oversize_events", 0) + 1
                            continue
                        break
                    value["offset"] = handle.tell()
                    try:
                        event = json.loads(line)
                        if not isinstance(event, dict): raise ValueError("not an event object")
                    except (ValueError, UnicodeError):
                        if kind == "stdout" and not line.lstrip().startswith((b"{", b"[")):
                            value["non_event_lines"] = value.get("non_event_lines", 0) + 1
                        else:
                            value["malformed_events"] = value.get("malformed_events", 0) + 1
                        continue
                    if kind == "stdout":
                        if event.get("type") == "turn.completed":
                            value["turn_sequence"] += 1
                            event_id = event.get("turn_id") or event.get("id") or attempt_id + ":" + str(value["turn_sequence"])
                            record_turn(store, session_id, event_id, event)
                        continue
                    payload = event.get("payload") or {}
                    if not isinstance(payload, dict):
                        value["malformed_events"] = value.get("malformed_events", 0) + 1
                        continue
                    if event.get("type") == "session_meta" and payload.get("id") != session_id:
                        value["identity_error"] = "session metadata does not match the expected session"
                        break
                    if event.get("type") == "response_item" and payload.get("type") in {"function_call", "custom_tool_call"}:
                        call_id = payload.get("call_id")
                        if call_id:
                            value.setdefault("tool_calls", {})[call_id] = {"name": payload.get("name"),
                                "response_id": payload.get("response_id") or event.get("response_id")}
                        value.setdefault("pending_call_names", []).append(str(payload.get("name") or ""))
                    if event.get("type") != "event_msg" or payload.get("type") != "token_count": continue
                    info = payload.get("info") or {}
                    if not isinstance(info, dict):
                        value["malformed_events"] = value.get("malformed_events", 0) + 1
                        continue
                    counters = info.get("total_token_usage")
                    if not isinstance(counters, dict): continue
                    # New segments require an explicit provider epoch; a falling
                    # counter alone must never be treated as extra consumption.
                    epoch = str(info.get("counter_epoch", "default"))
                    segment = value["segments"].setdefault(epoch, {})
                    previous = dict(segment)
                    for field in FIELDS:
                        counter = counters.get(field)
                        if counter is None: continue
                        if isinstance(counter, bool) or not isinstance(counter, int) or counter < 0:
                            value["invalid_counter"] = True
                            continue
                        if counter < segment.get(field, 0): value["discontinuity"] = True
                        segment[field] = max(segment.get(field, 0), counter)
                    if segment != previous:
                        value["observable_model_steps"] = value.get("observable_model_steps", 0) + 1
                        request_id = info.get("request_id") or payload.get("request_id") or event.get("request_id")
                        if request_id:
                            value.setdefault("request_ids", {})[str(request_id)] = True
                        else:
                            value["requests_without_identity"] = True
                        names = value.pop("pending_call_names", [])
                        waiting = bool(names) and all(name.split(".")[-1] in {"wait", "wait_execution_jobs", "wait_execution_events"}
                            or name.endswith(("__wait_execution_jobs", "__wait_execution_events")) for name in names)
                        group = "inferred_wait" if waiting else "unknown"
                        attributed = value.setdefault("attribution", {}).setdefault(group, {})
                        for field, count in segment.items():
                            attributed[field] = attributed.get(field, 0) + max(0, count - previous.get(field, 0))
                    value["last_event_at"] = event.get("timestamp")
                value["backlog_bytes"] = max(0, stat.st_size - value["offset"])
        except OSError as exc:
            value["read_error"] = str(exc)
        if value != old:
            store.put_record("usage_stream", key, value)
        return value


def refresh_usage(runner, *, force=False):
    from .codex_history import session_home
    from .recovery import runner_store
    now = time.monotonic()
    if not force and now - getattr(runner, "_last_usage_refresh", -100) < 1:
        return
    runner._last_usage_refresh = now
    store = runner_store(runner)
    sessions = {str(runner._resume_session_id)} if runner._resume_session_id else set()
    attempts = store.records("attempt")
    sessions.update(str(v["provider_session_id"]) for v in attempts.values() if v.get("provider_session_id"))
    for attempt_id, attempt in attempts.items():
        path = Path(attempt["log_path"])
        if path.is_file():
            ingest_file(store, path, session_id=str(attempt.get("provider_session_id") or runner._resume_session_id),
                        kind="stdout", attempt_id=attempt_id)
    for path in sorted((session_home(store) / "sessions").rglob("*.jsonl")):
        matches = [s for s in sessions if s in path.name]
        if len(matches) == 1:
            # Finite catch-up on exit; normal loops consume the next bounded chunk.
            for _ in range(8 if force else 1):
                value = ingest_file(store, path, session_id=matches[0])
                if value.get("backlog_bytes", 0) < 2 * 1024 * 1024: break
    details = store.usage_details()
    meta_path = runner.workspace / "_meta.json"
    if meta_path.is_file():
        try:
            metadata = json.loads(meta_path.read_text())
            if metadata.get("usage_details") != details:
                from chemistry_toolbox.src.recovery_io import atomic_json
                atomic_json(meta_path, {**metadata, "usage": store.usage(), "usage_details": details})
        except (OSError, ValueError):
            # The durable usage stream remains authoritative if the projection
            # is temporarily unwritable; finalization will write it again.
            pass
    return details

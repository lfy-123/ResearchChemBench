"""Export a redacted, event-sourced model input/output trajectory."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAT_VERSION = "researchchembench.model_io.v1"
SENSITIVE_KEY_PARTS = (
    "api_key",
    "apikey",
    "authorization",
    "access_token",
    "refresh_token",
    "password",
    "secret",
)
SENSITIVE_TEXT_PATTERNS = (
    re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(
        r"(?i)\b((?:OPENAI|JUDGE|ANTHROPIC|DEEPSEEK|BAILIAN)_API_KEY\s*=\s*)[^\s]+"
    ),
)


def _tool_catalog_delivery(workspace: Path) -> str:
    meta_path = workspace / "_meta.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            meta = {}
        if meta.get("tool_discovery_mode") == "progressive":
            return "progressive_mcp_discovery"
        if meta.get("tool_discovery_mode") == "full":
            return "eager_full_mcp_tools"
    return "legacy_or_unspecified"


def _redact_text(value: str) -> str:
    redacted = value
    for pattern in SENSITIVE_TEXT_PATTERNS:
        if pattern.groups:
            redacted = pattern.sub(r"\1<redacted>", redacted)
        else:
            redacted = pattern.sub("<redacted>", redacted)
    return redacted


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            normalized = str(key).lower().replace("-", "_")
            if any(part in normalized for part in SENSITIVE_KEY_PARTS):
                result[key] = "<redacted>"
            else:
                result[key] = _redact(item)
        return result
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_ref(workspace: Path, relative_path: str) -> dict[str, Any]:
    path = workspace / relative_path
    return {
        "path": relative_path,
        "exists": path.is_file(),
        "size_bytes": path.stat().st_size if path.is_file() else 0,
        "sha256": _sha256(path),
    }


def _load_json(value: str) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("OpenCode database JSON value is not an object")
    return parsed


def _opencode_records(
    workspace: Path,
) -> tuple[list[dict[str, Any]], dict[str, int], dict[str, list[str]]]:
    catalog_delivery = _tool_catalog_delivery(workspace)
    database = workspace / "_opencode" / "opencode.db"
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    try:
        sessions = connection.execute(
            "SELECT id, parent_id, title, directory, agent, model, "
            "time_created, time_updated FROM session ORDER BY time_created, id"
        ).fetchall()
        messages = connection.execute(
            "SELECT id, session_id, time_created, data "
            "FROM message ORDER BY time_created, id"
        ).fetchall()
        parts_by_message: dict[str, list[dict[str, Any]]] = {}
        for message_id, data in connection.execute(
            "SELECT message_id, data FROM part ORDER BY time_created, rowid"
        ):
            try:
                part = _load_json(data)
            except (json.JSONDecodeError, ValueError):
                continue
            parts_by_message.setdefault(str(message_id), []).append(_redact(part))
    finally:
        connection.close()

    records: list[dict[str, Any]] = [
        {
            "record_type": "session",
            "record_id": f"session:{session_id}",
            "session_id": session_id,
            "parent_session_id": parent_id,
            "title": _redact(title),
            "directory": _redact(directory),
            "agent": _redact(agent),
            "model": _redact(model),
            "time_created": time_created,
            "time_updated": time_updated,
        }
        for (
            session_id,
            parent_id,
            title,
            directory,
            agent,
            model,
            time_created,
            time_updated,
        ) in sessions
    ]
    session_metadata = {str(row[0]): row for row in sessions}
    context_refs: dict[str, list[str]] = {
        str(session_id): [] for session_id in session_metadata
    }
    previous_input_length: dict[str, int] = {}
    session_steps: dict[str, int] = {}
    step_index = 0
    input_count = 0
    for message_id, session_id, time_created, data in messages:
        try:
            message = _redact(_load_json(data))
        except (json.JSONDecodeError, ValueError):
            continue
        message_id = str(message_id)
        session_id = str(session_id)
        session_context = context_refs.setdefault(session_id, [])
        role = str(message.get("role") or "unknown")
        parts = parts_by_message.get(message_id, [])
        if role != "assistant":
            input_count += 1
            record_id = f"input_message:{message_id}"
            records.append(
                {
                    "record_type": "input_message",
                    "record_id": record_id,
                    "message_id": message_id,
                    "session_id": session_id,
                    "session_ref": f"session:{session_id}",
                    "role": role,
                    "time_created": time_created,
                    "message": message,
                    "parts": parts,
                }
            )
            session_context.append(record_id)
            continue

        step_index += 1
        session_steps[session_id] = session_steps.get(session_id, 0) + 1
        input_refs = list(session_context)
        previous_length = previous_input_length.get(session_id, 0)
        new_refs = input_refs[previous_length:]
        previous_input_length[session_id] = len(input_refs)
        output_ref = f"model_step:{step_index}:output"
        records.append(
            {
                "record_type": "model_step",
                "record_id": f"model_step:{step_index}",
                "step_index": step_index,
                "session_step_index": session_steps[session_id],
                "message_id": message_id,
                "session_id": session_id,
                "session_ref": f"session:{session_id}",
                "parent_session_id": (
                    session_metadata.get(session_id, (None, None))[1]
                ),
                "parent_message_id": message.get("parentID"),
                "time_created": time_created,
                "input": {
                    "representation": "event_sourced_refs",
                    "context_refs": input_refs,
                    "new_context_refs_since_previous_step": new_refs,
                    "initial_instruction_ref": "artifact:INSTRUCTIONS.md",
                    "tool_catalog_ref": "artifact:_toolbox_catalog.json",
                    "tool_catalog_delivery": catalog_delivery,
                    "provider_config_ref": "artifact:opencode.json",
                },
                "output": {
                    "record_ref": output_ref,
                    "message": message,
                    "parts": parts,
                },
            }
        )
        session_context.append(output_ref)
    return (
        records,
        {
            "model_step_count": step_index,
            "input_message_count": input_count,
            "context_record_count": sum(len(refs) for refs in context_refs.values()),
            "session_count": len(context_refs),
        },
        context_refs,
    )


def _fallback_records(
    workspace: Path,
) -> tuple[list[dict[str, Any]], dict[str, int], dict[str, list[str]]]:
    catalog_delivery = _tool_catalog_delivery(workspace)
    session_id = "primary"
    records: list[dict[str, Any]] = [
        {
            "record_type": "session",
            "record_id": f"session:{session_id}",
            "session_id": session_id,
            "parent_session_id": None,
        }
    ]
    instructions = workspace / "INSTRUCTIONS.md"
    input_ref = "input_message:initial_instructions"
    records.append(
        {
            "record_type": "input_message",
            "record_id": input_ref,
            "session_id": session_id,
            "session_ref": f"session:{session_id}",
            "role": "user",
            "message": {"role": "user"},
            "parts": [
                {
                    "type": "text",
                    "text": _redact_text(
                        instructions.read_text(encoding="utf-8", errors="replace")
                    ),
                }
            ]
            if instructions.is_file()
            else [],
        }
    )
    output = workspace / "_agent_output.jsonl"
    context_refs = [input_ref]
    previous_input_length = 0
    current: list[dict[str, Any]] | None = None
    step_index = 0
    if output.is_file():
        for line_number, line in enumerate(
            output.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            event = _redact(event)
            if event.get("type") == "step_start":
                current = [{"line_number": line_number, "event": event}]
                continue
            if current is not None:
                current.append({"line_number": line_number, "event": event})
            if event.get("type") == "step_finish" and current is not None:
                step_index += 1
                input_refs = list(context_refs)
                new_refs = input_refs[previous_input_length:]
                previous_input_length = len(input_refs)
                output_ref = f"model_step:{step_index}:output"
                records.append(
                    {
                        "record_type": "model_step",
                        "record_id": f"model_step:{step_index}",
                        "step_index": step_index,
                        "session_step_index": step_index,
                        "session_id": session_id,
                        "session_ref": f"session:{session_id}",
                        "input": {
                            "representation": "event_sourced_refs",
                            "context_refs": input_refs,
                            "new_context_refs_since_previous_step": new_refs,
                            "initial_instruction_ref": "artifact:INSTRUCTIONS.md",
                            "tool_catalog_ref": "artifact:_toolbox_catalog.json",
                            "tool_catalog_delivery": catalog_delivery,
                        },
                        "output": {"record_ref": output_ref, "events": current},
                    }
                )
                context_refs.append(output_ref)
                current = None
    return (
        records,
        {
            "model_step_count": step_index,
            "input_message_count": 1,
            "context_record_count": len(context_refs),
            "session_count": 1,
        },
        {session_id: context_refs},
    )


def _model_errors(
    workspace: Path, context_refs: dict[str, list[str]]
) -> list[dict[str, Any]]:
    output = workspace / "_agent_output.jsonl"
    errors = []
    if not output.is_file():
        return errors
    for line_number, line in enumerate(
        output.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("type") == "error":
            session_id = str(event.get("sessionID") or "primary")
            errors.append(
                {
                    "record_type": "model_error",
                    "record_id": f"model_error:{len(errors) + 1}",
                    "line_number": line_number,
                    "session_id": session_id,
                    "input": {
                        "representation": "event_sourced_refs",
                        "context_refs": list(context_refs.get(session_id, [])),
                    },
                    "error": _redact(event),
                }
            )
    return errors


def export_model_io_trace(workspace: str | Path) -> dict[str, Any]:
    """Write ``_model_io.jsonl`` and return its compact summary."""

    workspace = Path(workspace).resolve()
    database = workspace / "_opencode" / "opencode.db"
    if database.is_file():
        records, stats, context_refs = _opencode_records(workspace)
        capture_mode = "opencode_database_event_sourced"
    else:
        records, stats, context_refs = _fallback_records(workspace)
        capture_mode = "agent_event_stream_event_sourced"

    errors = _model_errors(workspace, context_refs)
    created_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "record_type": "trajectory_manifest",
        "record_id": "manifest",
        "format_version": FORMAT_VERSION,
        "created_at": created_at,
        "capture_mode": capture_mode,
        "representation": (
            "Event-sourced model trajectory. Each model_step input lists ordered "
            "references to the initial input and prior step outputs, avoiding full "
            "context duplication while preserving reconstructability."
        ),
        "raw_http_captured": False,
        "credentials_captured": False,
        "artifacts": {
            "artifact:INSTRUCTIONS.md": _artifact_ref(workspace, "INSTRUCTIONS.md"),
            "artifact:_toolbox_catalog.json": _artifact_ref(
                workspace, "_toolbox_catalog.json"
            ),
            "artifact:opencode.json": _artifact_ref(workspace, "opencode.json"),
            "artifact:_agent_output.jsonl": _artifact_ref(
                workspace, "_agent_output.jsonl"
            ),
            "artifact:_opencode/opencode.db": _artifact_ref(
                workspace, "_opencode/opencode.db"
            ),
        },
        "input_message_count": stats["input_message_count"],
        "model_step_count": stats["model_step_count"],
        "model_error_count": len(errors),
        "context_record_count": stats["context_record_count"],
        "session_count": stats["session_count"],
    }
    path = workspace / "_model_io.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for record in [manifest, *records, *errors]:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {
        "path": str(path),
        "format_version": FORMAT_VERSION,
        "capture_mode": capture_mode,
        "model_step_count": stats["model_step_count"],
        "model_error_count": len(errors),
        "session_count": stats["session_count"],
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }

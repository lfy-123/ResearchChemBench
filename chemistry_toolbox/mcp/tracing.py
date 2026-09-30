"""Agent-independent result, trace, and artifact capture for MCP tool calls."""

from __future__ import annotations

from contextvars import ContextVar

MCP_REQUEST_ID = ContextVar("mcp_request_id", default=None)

import asyncio
from contextlib import contextmanager

import hashlib
import json
import logging
import os
import shutil
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .workspace import relative_workspace_path, workspace_root
from chemistry_toolbox.src.execution_states import TERMINAL_STATES


_LOCK = threading.Lock()
DEFAULT_MAX_ARTIFACT_BYTES = 100 * 1024 * 1024
DEFAULT_MAX_ARTIFACT_FILES = 1000
LOGGER = logging.getLogger(__name__)
ACTION_RESULT_STATUSES = TERMINAL_STATES


def _positive_environment_integer(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer, received {raw!r}") from exc
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer, received {raw!r}")
    return value


def _artifact_limits() -> tuple[int, int]:
    """Validate trace settings before a chemistry operation is started."""

    return (
        _positive_environment_integer(
            "RESEARCHCHEM_MCP_MAX_ARTIFACT_FILES", DEFAULT_MAX_ARTIFACT_FILES
        ),
        _positive_environment_integer(
            "RESEARCHCHEM_MCP_MAX_ARTIFACT_BYTES", DEFAULT_MAX_ARTIFACT_BYTES
        ),
    )


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _next_sequence(root: Path) -> int:
    """Reserve a persistent sequence without overwriting after server restarts."""

    with _LOCK:
        result_dir = root / "_tool_results"
        result_dir.mkdir(parents=True, exist_ok=True)
        existing: list[int] = []
        for path in result_dir.iterdir():
            prefix = path.name.split("_", 1)[0].removeprefix(".sequence-")
            if prefix.isdigit():
                existing.append(int(prefix))
        sequence = max(existing, default=0) + 1
        while True:
            reservation = result_dir / f".sequence-{sequence:04d}"
            try:
                descriptor = os.open(
                    reservation,
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
            except FileExistsError:
                sequence += 1
                continue
            os.close(descriptor)
            return sequence


def _excluded(path: Path) -> bool:
    rel = path.relative_to(workspace_root())
    first = rel.parts[0] if rel.parts else ""
    execution_job_file = len(rel.parts) >= 2 and rel.parts[:2] == (
        "outputs",
        "execution_jobs",
    )
    return execution_job_file or first in {
        ".codex",
        ".claude",
        "_opencode",
        "_tool_results",
        "_tool_artifacts",
        "tool_logs",
    } or rel.name.startswith("_agent_output") or rel.name in {
        "_tool_trace.jsonl",
        "_tool_call_events.jsonl",
        "_meta.json",
        "_score.json",
        "_toolbox_catalog.json",
    }


def workspace_snapshot() -> dict[str, tuple[int, int]]:
    """Return size/mtime fingerprints for regular workspace files."""

    snapshot: dict[str, tuple[int, int]] = {}
    root = workspace_root()
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or _excluded(path):
            continue
        try:
            path.resolve().relative_to(root)
        except ValueError:
            continue
        stat = path.stat()
        snapshot[str(path.relative_to(root))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _capture_changed_artifacts(
    sequence: int,
    before: dict[str, tuple[int, int]],
    *,
    max_files: int,
    max_bytes: int,
) -> list[dict[str, Any]]:
    root = workspace_root()
    after = workspace_snapshot()
    changed = [rel for rel, fingerprint in after.items() if before.get(rel) != fingerprint]
    artifact_dir = root / "_tool_artifacts" / f"{sequence:04d}"
    records: list[dict[str, Any]] = []
    for rel in changed[:max_files]:
        source = root / rel
        if source.is_symlink() or not source.is_file():
            continue
        size = source.stat().st_size
        if size > max_bytes:
            records.append(
                {
                    "path": rel,
                    "snapshot_path": None,
                    "size_bytes": size,
                    "sha256": _sha256(source),
                    "snapshot_skipped": f"larger than {max_bytes} bytes",
                }
            )
            continue
        destination = artifact_dir / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        records.append(
            {
                "path": rel,
                "snapshot_path": relative_workspace_path(destination),
                "size_bytes": size,
                "sha256": _sha256(source),
            }
        )
    return records


@contextmanager
def _trace_operation(
    tool_name: str,
    arguments: dict[str, Any],
    *,
    capture_artifacts: bool = True,
) -> Any:
    """Execute one tool and persist a canonical result/trace/artifact record."""

    root = workspace_root()
    max_artifact_files, max_artifact_bytes = _artifact_limits()
    sequence = _next_sequence(root)
    result_dir = root / "_tool_results"
    result_dir.mkdir(parents=True, exist_ok=True)
    trace_path = root / "_tool_trace.jsonl"
    before = workspace_snapshot() if capture_artifacts else {}
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    status = "success"
    error = None
    operation_exception: BaseException | None = None
    outcome = {"result": None}
    _append_call_event(root, {"sequence": sequence, "tool": tool_name, "phase": "started", "at": started_wall,
                             "arguments": _jsonable(arguments), "mcp_request_id": MCP_REQUEST_ID.get(), "host_call_id": None})
    try:
        yield outcome
    except BaseException as exc:
        status = "cancelled" if isinstance(exc, asyncio.CancelledError) else "error"
        error = f"{type(exc).__name__}: {exc}"
        operation_exception = exc
        raise
    finally:
        try:
            duration = time.monotonic() - started
            result_payload = _jsonable(outcome["result"])
            transport_status = status
            recorded_status = status
            recorded_error: Any = error
            if (
                transport_status == "success"
                and isinstance(result_payload, dict)
                and result_payload.get("status") in ACTION_RESULT_STATUSES
            ):
                recorded_status = str(result_payload["status"])
                if recorded_status not in {"success", "partial_success"}:
                    recorded_error = result_payload.get("error") or (result_payload.get("execution_feedback") or {}).get("diagnostic")
            result_path = result_dir / f"{sequence:04d}_{tool_name}.json"
            result_path.write_text(
                json.dumps(
                    {
                        "status": recorded_status,
                        "transport_status": transport_status,
                        "result": result_payload,
                        "error": recorded_error,
                        "original_exception": outcome.get("original_exception"),
                        "display_projection": outcome.get("display_projection"),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            artifacts = (
                _capture_changed_artifacts(
                    sequence,
                    before,
                    max_files=max_artifact_files,
                    max_bytes=max_artifact_bytes,
                )
                if capture_artifacts
                else []
            )
            preview = json.dumps(result_payload, ensure_ascii=False, default=str)
            event = {
                "sequence": sequence,
                "run_id": os.environ.get(
                    "RESEARCHCHEM_MCP_RUN_ID",
                    os.environ.get("RESEARCHCHEMBENCH_RUN_ID", ""),
                ),
                "tool": tool_name,
                "mcp_request_id": MCP_REQUEST_ID.get(),
                "host_call_id": None,
                "arguments": _jsonable(arguments),
                "status": recorded_status,
                "transport_status": transport_status,
                "started_at": started_wall,
                "duration_seconds": round(duration, 6),
                "result_path": relative_workspace_path(result_path),
                "result_preview": preview[:2000],
                "error": recorded_error,
                "artifacts": artifacts,
            }
            with _LOCK:
                with trace_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(event, ensure_ascii=False) + "\n")
            _append_call_event(root, {"sequence": sequence, "tool": tool_name,
                "phase": "cancelled" if status == "cancelled" else "finished",
                "at": datetime.now(timezone.utc).isoformat(), "status": recorded_status,
                "result_path": relative_workspace_path(result_path)})
        except Exception:
            if operation_exception is None:
                raise
            LOGGER.exception(
                "Trace persistence also failed for tool %s; preserving the "
                "original tool exception",
                tool_name,
            )


def _append_call_event(root: Path, event: dict) -> None:
    with _LOCK:
        with (root / "_tool_call_events.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def execute_traced(tool_name, arguments, function, *, capture_artifacts=True):
    from chemistry_toolbox.src.execution_feedback import normalize_tool_feedback, exception_feedback, feedback_schema_version
    with _trace_operation(tool_name, arguments, capture_artifacts=capture_artifacts) as outcome:
        try:
            outcome["result"] = function()
        except Exception as exc:
            if feedback_schema_version() != 2:
                raise
            outcome["result"] = exception_feedback(exc, tool=tool_name)
            import traceback
            outcome["original_exception"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        return _project_traced(outcome, tool_name)


async def execute_traced_async(tool_name, arguments, function, *, capture_artifacts=False):
    from chemistry_toolbox.src.execution_feedback import normalize_tool_feedback, exception_feedback, feedback_schema_version
    with _trace_operation(tool_name, arguments, capture_artifacts=capture_artifacts) as outcome:
        try:
            outcome["result"] = await function()
        except Exception as exc:
            if feedback_schema_version() != 2:
                raise
            outcome["result"] = exception_feedback(exc, tool=tool_name)
            import traceback
            outcome["original_exception"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        return _project_traced(outcome, tool_name)


def _project_traced(outcome, tool_name):
    from chemistry_toolbox.src.execution_feedback import normalize_tool_feedback, feedback_schema_version
    view = normalize_tool_feedback(outcome["result"], tool=tool_name)
    outcome["display_projection"] = {"function": "normalize_tool_feedback", "schema_version": feedback_schema_version(),
        "tool": tool_name, "sha256": hashlib.sha256(json.dumps(_jsonable(view), sort_keys=True, ensure_ascii=False).encode()).hexdigest()}
    return view

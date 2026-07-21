"""Agent-independent result, trace, and artifact capture for MCP tool calls."""

from __future__ import annotations

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


_LOCK = threading.Lock()
DEFAULT_MAX_ARTIFACT_BYTES = 100 * 1024 * 1024
DEFAULT_MAX_ARTIFACT_FILES = 1000
LOGGER = logging.getLogger(__name__)
ACTION_RESULT_STATUSES = {
    "success",
    "partial_success",
    "invalid_request",
    "unsupported",
    "unavailable",
    "failed",
    "timeout",
    "cancelled",
}


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
    return first in {
        ".codex",
        ".claude",
        "_tool_results",
        "_tool_artifacts",
        "tool_logs",
    } or rel.name.startswith("_agent_output") or rel.name in {
        "_tool_trace.jsonl",
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


def execute_traced(
    tool_name: str,
    arguments: dict[str, Any],
    function: Callable[[], Any],
) -> Any:
    """Execute one tool and persist a canonical result/trace/artifact record."""

    root = workspace_root()
    max_artifact_files, max_artifact_bytes = _artifact_limits()
    sequence = _next_sequence(root)
    result_dir = root / "_tool_results"
    result_dir.mkdir(parents=True, exist_ok=True)
    trace_path = root / "_tool_trace.jsonl"
    before = workspace_snapshot()
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    status = "success"
    error = None
    operation_exception: Exception | None = None
    result: Any = None
    try:
        result = function()
        return result
    except Exception as exc:
        status = "error"
        error = f"{type(exc).__name__}: {exc}"
        operation_exception = exc
        raise
    finally:
        try:
            duration = time.monotonic() - started
            result_payload = _jsonable(result)
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
                    recorded_error = result_payload.get("error")
            result_path = result_dir / f"{sequence:04d}_{tool_name}.json"
            result_path.write_text(
                json.dumps(
                    {
                        "status": recorded_status,
                        "transport_status": transport_status,
                        "result": result_payload,
                        "error": recorded_error,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            artifacts = _capture_changed_artifacts(
                sequence,
                before,
                max_files=max_artifact_files,
                max_bytes=max_artifact_bytes,
            )
            preview = json.dumps(result_payload, ensure_ascii=False, default=str)
            event = {
                "sequence": sequence,
                "run_id": os.environ.get(
                    "RESEARCHCHEM_MCP_RUN_ID",
                    os.environ.get("RESEARCHCHEMBENCH_RUN_ID", ""),
                ),
                "tool": tool_name,
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
        except Exception:
            if operation_exception is None:
                raise
            LOGGER.exception(
                "Trace persistence also failed for tool %s; preserving the "
                "original tool exception",
                tool_name,
            )

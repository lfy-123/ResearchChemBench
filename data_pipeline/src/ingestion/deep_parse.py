from __future__ import annotations

import json
import os
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.core.logging import log_progress, pipeline_logger


def build_mineru_queue(
    documents: list[dict[str, Any]],
    include_optional: bool = False,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    allowed = {"required", "optional"} if include_optional else {"required"}
    queue: list[dict[str, Any]] = []
    for document in documents:
        if (document.get("pre_extraction_quality") or {}).get("decision") == "reject":
            continue
        classification = document.get("corpus_classification") or {}
        decision = classification.get("deep_parse_decision")
        if decision not in allowed or document.get("duplicate_of"):
            continue
        scores = classification.get("constructability_scores") or {}
        queue.append(
            {
                "document_id": document["document_id"],
                "paper_id": document["paper_id"],
                "source_path": document["source_path"],
                "title": document.get("title"),
                "expected_pages": document.get("page_count"),
                "deep_parse_decision": decision,
                "priority_score": max(scores.values(), default=0.0),
                "reason": _queue_reason(document),
            }
        )
    queue.sort(
        key=lambda item: (item["deep_parse_decision"] == "required", item["priority_score"]),
        reverse=True,
    )
    return queue[:limit] if limit is not None else queue


def run_mineru_queue(
    queue: list[dict[str, Any]],
    output_dir: str | Path,
    execute: bool = False,
    command: str = "mineru",
    method: str = "auto",
    backend: str | None = None,
    timeout_seconds: int = 3600,
    environment: dict[str, str] | None = None,
    extra_args: list[str] | None = None,
    reuse_existing: bool = True,
    min_markdown_chars: int = 1000,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    executable = _resolve_executable(command)
    results: list[dict[str, Any]] = []

    total = len(queue)
    for index, item in enumerate(queue, start=1):
        target = output_dir / item["document_id"]
        cli = [executable or command, "-p", item["source_path"], "-o", str(target), "-m", method]
        if backend:
            cli.extend(["-b", backend])
        cli.extend(extra_args or [])
        result = {
            **item,
            "command": cli,
            "output_dir": str(target),
            "started_at": _now(),
        }
        if not execute:
            result["status"] = "queued"
        elif not executable:
            result["status"] = "unavailable"
            result["error"] = f"MinerU command not found: {command}"
        else:
            target.mkdir(parents=True, exist_ok=True)
            existing = _inspect_output(
                target, min_markdown_chars, expected_pages=item.get("expected_pages")
            )
            if reuse_existing and existing["valid"]:
                result.update(existing)
                result["status"] = "reused"
                result["duration_seconds"] = 0.0
                result["finished_at"] = _now()
                results.append(result)
                log_progress(
                    "stage_07_mineru_parse",
                    index,
                    total,
                    Path(item["source_path"]).name,
                    status="reused",
                )
                continue
            started = time.monotonic()
            process_env = os.environ.copy()
            process_env.update({key: str(value) for key, value in (environment or {}).items()})
            heartbeat_stop = threading.Event()
            heartbeat = threading.Thread(
                target=_log_mineru_heartbeat,
                args=(heartbeat_stop, index, total, item, started),
                daemon=True,
            )
            heartbeat.start()
            try:
                completed = subprocess.run(
                    cli,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                    check=False,
                    env=process_env,
                )
                result["return_code"] = completed.returncode
                result["stdout_tail"] = completed.stdout[-4000:]
                result["stderr_tail"] = completed.stderr[-4000:]
                (target / "mineru.stdout.log").write_text(completed.stdout, encoding="utf-8")
                (target / "mineru.stderr.log").write_text(completed.stderr, encoding="utf-8")
                inspected = _inspect_output(
                    target, min_markdown_chars, expected_pages=item.get("expected_pages")
                )
                result.update(inspected)
                result["status"] = (
                    "success" if completed.returncode == 0 and inspected["valid"] else "failed"
                )
                if completed.returncode == 0 and not inspected["valid"]:
                    result["error"] = (
                        "MinerU exited successfully but required output validation failed"
                    )
            except subprocess.TimeoutExpired as exc:
                result["status"] = "timeout"
                result["error"] = str(exc)
                if exc.stdout:
                    (target / "mineru.stdout.log").write_text(
                        _as_text(exc.stdout), encoding="utf-8"
                    )
                if exc.stderr:
                    (target / "mineru.stderr.log").write_text(
                        _as_text(exc.stderr), encoding="utf-8"
                    )
            except Exception as exc:
                result["status"] = "failed"
                result["error"] = f"{type(exc).__name__}: {exc}"
            finally:
                heartbeat_stop.set()
                heartbeat.join(timeout=2)
            result["duration_seconds"] = round(time.monotonic() - started, 3)
        result["finished_at"] = _now()
        results.append(result)
        log_progress(
            "stage_07_mineru_parse",
            index,
            total,
            Path(item["source_path"]).name,
            status=result.get("status"),
        )
    return results


def _log_mineru_heartbeat(
    stop: threading.Event,
    index: int,
    total: int,
    item: dict[str, Any],
    started: float,
) -> None:
    file_name = Path(item["source_path"]).name
    pages = item.get("expected_pages") or "unknown"
    log_progress(
        "stage_07_mineru_parse",
        index - 1,
        total,
        f"running {index}/{total}: {file_name}, pages={pages}",
        status="running",
    )
    while not stop.wait(15):
        elapsed = round(time.monotonic() - started, 1)
        pipeline_logger().info(
            "HEARTBEAT | stage_07_mineru_parse | document=%d/%d | file=%s | pages=%s | elapsed_seconds=%.1f",
            index,
            total,
            file_name,
            pages,
            elapsed,
        )


def deep_text_map(results: list[dict[str, Any]]) -> dict[str, str]:
    return {
        item["paper_id"]: item["markdown_path"]
        for item in results
        if item.get("status") in {"success", "reused"}
        and item.get("markdown_path")
        and (item.get("deep_parse_quality") or {}).get("passed", True)
    }


def _queue_reason(document: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    classification = document.get("corpus_classification") or {}
    if (document.get("text_quality") or {}).get("needs_ocr"):
        reasons.append("low cheap-extraction text quality")
    modes = classification.get("eligible_modes", [])
    if modes:
        reasons.append(f"benchmark-constructable modes: {', '.join(modes)}")
    if classification.get("computational_role") == "primary":
        reasons.append("computation is a primary scientific method")
    return reasons or ["manual review candidate"]


def _find_largest(root: Path, pattern: str) -> Path | None:
    files = [path for path in root.rglob(pattern) if path.is_file()]
    return max(files, key=lambda path: path.stat().st_size) if files else None


def _resolve_executable(command: str) -> str | None:
    path = Path(command).expanduser()
    if path.parent != Path("."):
        return str(path.resolve()) if path.is_file() and os.access(path, os.X_OK) else None
    return shutil.which(command)


def _inspect_output(
    root: Path,
    min_markdown_chars: int,
    expected_pages: int | None = None,
) -> dict[str, Any]:
    markdown = _find_largest(root, "*.md")
    content_v2 = _find_largest(root, "*_content_list_v2.json")
    content_list = _find_largest(root, "*_content_list.json")
    middle = _find_largest(root, "*_middle.json")
    model = _find_largest(root, "*_model.json")
    images = sorted(path for path in root.rglob("images/*") if path.is_file())
    markdown_chars = markdown.stat().st_size if markdown else 0
    structured_pages = None
    structured_error = None
    if content_v2:
        try:
            payload = json.loads(content_v2.read_text(encoding="utf-8"))
            structured_pages = len(payload) if isinstance(payload, list) else None
        except (OSError, json.JSONDecodeError) as exc:
            structured_error = str(exc)
    valid = bool(
        markdown
        and markdown_chars >= min_markdown_chars
        and content_v2
        and structured_error is None
        and structured_pages
        and (expected_pages is None or structured_pages == expected_pages)
    )
    return {
        "valid": valid,
        "markdown_path": str(markdown.resolve()) if markdown else None,
        "markdown_bytes": markdown_chars,
        "content_list_v2_path": str(content_v2.resolve()) if content_v2 else None,
        "content_list_path": str(content_list.resolve()) if content_list else None,
        "middle_json_path": str(middle.resolve()) if middle else None,
        "model_json_path": str(model.resolve()) if model else None,
        "structured_pages": structured_pages,
        "expected_pages": expected_pages,
        "image_count": len(images),
        "structured_error": structured_error,
    }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_text(value: str | bytes) -> str:
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value

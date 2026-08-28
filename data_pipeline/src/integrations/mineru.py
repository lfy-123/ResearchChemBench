from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.core.logging import log_progress, pipeline_logger


def build_mineru_queue(
    documents: list[dict[str, Any]],
    limit: int | None = None,
) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for document in documents:
        if document.get("duplicate_of"):
            continue
        if not (document.get("resource_limits") or {}).get("passed", False):
            continue
        decision = "required"
        queue.append(
            {
                "document_id": document["document_id"],
                "paper_id": document["paper_id"],
                "source_path": document["source_path"],
                "title": document.get("title"),
                "expected_pages": document.get("page_count"),
                "deep_parse_decision": decision,
                "priority_score": 1.0,
                "reason": ["passed stages 03-04 and requires deep parsing for task construction"],
            }
        )
    queue.sort(key=lambda item: (item.get("title") or "", item["paper_id"]))
    return queue[:limit] if limit is not None else queue


def run_mineru_queue(
    queue: list[dict[str, Any]],
    output_dir: str | Path,
    execute: bool = False,
    command: str = "mineru",
    method: str = "auto",
    backend: str | None = None,
    timeout_seconds: int = 3000,
    working_directory: str | Path | None = None,
    environment: dict[str, str] | None = None,
    extra_args: list[str] | None = None,
    reuse_existing: bool = True,
    min_markdown_chars: int = 1000,
    stage_name: str = "mineru_queue",
    max_workers: int = 1,
    request_batch_size: int = 1,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    process_directory = (
        Path(working_directory).expanduser().resolve() if working_directory else None
    )
    sandbox_runtime = (environment or {}).get("_sandbox_runtime")
    process_environment = dict(environment or {})
    process_environment.pop("_sandbox_runtime", None)
    executable = None if sandbox_runtime is not None else _resolve_executable(command)
    total = len(queue)
    if not total:
        return []
    batch_size = max(1, int(request_batch_size))
    if batch_size > 1 and sandbox_runtime is None:
        return _run_mineru_batches(
            queue=queue,
            output_dir=output_dir,
            execute=execute,
            executable=executable,
            command=command,
            method=method,
            backend=backend,
            timeout_seconds=timeout_seconds,
            process_directory=process_directory,
            process_environment=process_environment,
            extra_args=extra_args,
            reuse_existing=reuse_existing,
            min_markdown_chars=min_markdown_chars,
            stage_name=stage_name,
            max_workers=max_workers,
            request_batch_size=batch_size,
        )
    worker_count = max(1, min(int(max_workers), total))
    results: list[dict[str, Any] | None] = [None] * total

    def process(index: int, item: dict[str, Any]) -> dict[str, Any]:
        return _run_mineru_item(
            item=item,
            index=index,
            total=total,
            output_dir=output_dir,
            execute=execute,
            executable=executable,
            command=command,
            method=method,
            backend=backend,
            timeout_seconds=timeout_seconds,
            process_directory=process_directory,
            process_environment=process_environment,
            extra_args=extra_args,
            reuse_existing=reuse_existing,
            min_markdown_chars=min_markdown_chars,
            stage_name=stage_name,
            sandbox_runtime=sandbox_runtime,
        )

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(process, index, item): index - 1
            for index, item in enumerate(queue, start=1)
        }
        completed_count = 0
        for future in as_completed(futures):
            position = futures[future]
            result = future.result()
            results[position] = result
            completed_count += 1
            log_progress(
                stage_name,
                completed_count,
                total,
                Path(result["source_path"]).name,
                status=result.get("status"),
            )
    return [result for result in results if result is not None]


def _run_mineru_batches(
    *,
    queue: list[dict[str, Any]],
    output_dir: Path,
    execute: bool,
    executable: str | None,
    command: str,
    method: str,
    backend: str | None,
    timeout_seconds: int,
    process_directory: Path | None,
    process_environment: dict[str, str],
    extra_args: list[str] | None,
    reuse_existing: bool,
    min_markdown_chars: int,
    stage_name: str,
    max_workers: int,
    request_batch_size: int,
) -> list[dict[str, Any]]:
    batches = [
        queue[offset : offset + request_batch_size]
        for offset in range(0, len(queue), request_batch_size)
    ]
    worker_count = max(1, min(int(max_workers), len(batches)))
    indexed_results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(
                _run_mineru_batch,
                batch=batch,
                batch_index=index,
                batch_total=len(batches),
                output_dir=output_dir,
                execute=execute,
                executable=executable,
                command=command,
                method=method,
                backend=backend,
                timeout_seconds=timeout_seconds,
                process_directory=process_directory,
                process_environment=process_environment,
                extra_args=extra_args,
                reuse_existing=reuse_existing,
                min_markdown_chars=min_markdown_chars,
                stage_name=stage_name,
            ): batch
            for index, batch in enumerate(batches, start=1)
        }
        completed_count = 0
        for future in as_completed(futures):
            batch_results = future.result()
            for result in batch_results:
                indexed_results[result["document_id"]] = result
                completed_count += 1
                log_progress(
                    stage_name,
                    completed_count,
                    len(queue),
                    Path(result["source_path"]).name,
                    status=result.get("status"),
                )
    return [indexed_results[item["document_id"]] for item in queue]


def _run_mineru_batch(
    *,
    batch: list[dict[str, Any]],
    batch_index: int,
    batch_total: int,
    output_dir: Path,
    execute: bool,
    executable: str | None,
    command: str,
    method: str,
    backend: str | None,
    timeout_seconds: int,
    process_directory: Path | None,
    process_environment: dict[str, str],
    extra_args: list[str] | None,
    reuse_existing: bool,
    min_markdown_chars: int,
    stage_name: str,
) -> list[dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    pending: list[dict[str, Any]] = []
    for item in batch:
        target = output_dir / item["document_id"]
        result = {
            **item,
            "output_dir": str(target),
            "started_at": _now(),
            "request_batch_index": batch_index,
            "request_batch_size": len(batch),
        }
        existing = _inspect_output(
            target, min_markdown_chars, expected_pages=item.get("expected_pages")
        )
        if reuse_existing and existing["valid"]:
            result.update(existing)
            result["status"] = "reused"
            result["duration_seconds"] = 0.0
            result["finished_at"] = _now()
            results[item["document_id"]] = result
        else:
            pending.append(item)
            results[item["document_id"]] = result

    if not pending:
        return [results[item["document_id"]] for item in batch]
    if not execute or not executable:
        for item in pending:
            result = results[item["document_id"]]
            result["status"] = "queued" if not execute else "unavailable"
            if execute:
                result["error"] = f"MinerU command not found: {command}"
            result["finished_at"] = _now()
        return [results[item["document_id"]] for item in batch]

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="mineru-input-", dir=output_dir) as input_temp:
        input_root = Path(input_temp)
        batch_output = output_dir / f".batch-{batch_index:06d}"
        shutil.rmtree(batch_output, ignore_errors=True)
        batch_output.mkdir(parents=True)
        for item in pending:
            source = Path(item["source_path"])
            staged = input_root / f"{item['document_id']}{source.suffix.casefold()}"
            try:
                os.link(source, staged)
            except OSError:
                staged.symlink_to(source.resolve())
        cli = [executable, "-p", str(input_root), "-o", str(batch_output), "-m", method]
        if backend:
            cli.extend(["-b", backend])
        cli.extend(extra_args or [])
        for item in pending:
            results[item["document_id"]]["command"] = cli

        process_env = os.environ.copy()
        process_env.update({key: str(value) for key, value in process_environment.items()})
        heartbeat_stop = threading.Event()
        heartbeat_item = {
            "source_path": f"request-batch-{batch_index}",
            "expected_pages": sum(int(item.get("expected_pages") or 0) for item in pending),
        }
        heartbeat = threading.Thread(
            target=_log_mineru_heartbeat,
            args=(
                heartbeat_stop,
                batch_index,
                batch_total,
                heartbeat_item,
                started,
                stage_name,
            ),
            daemon=True,
        )
        heartbeat.start()
        return_code: int | None = None
        stdout_text = ""
        stderr_text = ""
        batch_error: str | None = None
        try:
            completed = subprocess.run(
                cli,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                env=process_env,
                cwd=process_directory,
            )
            return_code = completed.returncode
            stdout_text = completed.stdout
            stderr_text = completed.stderr
        except subprocess.TimeoutExpired as exc:
            batch_error = str(exc)
            stdout_text = _as_text(exc.stdout) if exc.stdout else ""
            stderr_text = _as_text(exc.stderr) if exc.stderr else ""
        except Exception as exc:
            batch_error = f"{type(exc).__name__}: {exc}"
        finally:
            heartbeat_stop.set()
            heartbeat.join(timeout=2)

        duration = round(time.monotonic() - started, 3)
        for item in pending:
            document_id = item["document_id"]
            target = output_dir / document_id
            parsed_root = batch_output / document_id
            if parsed_root.is_dir():
                shutil.rmtree(target, ignore_errors=True)
                parsed_root.replace(target)
            target.mkdir(parents=True, exist_ok=True)
            (target / "mineru.stdout.log").write_text(stdout_text, encoding="utf-8")
            (target / "mineru.stderr.log").write_text(stderr_text, encoding="utf-8")
            inspected = _inspect_output(
                target, min_markdown_chars, expected_pages=item.get("expected_pages")
            )
            result = results[document_id]
            result.update(inspected)
            result["return_code"] = return_code
            result["stdout_tail"] = stdout_text[-4000:]
            result["stderr_tail"] = stderr_text[-4000:]
            result["duration_seconds"] = duration
            if inspected["valid"]:
                result["status"] = "success"
            elif batch_error is not None:
                result["status"] = "timeout" if return_code is None else "failed"
                result["error"] = batch_error
            else:
                result["status"] = "failed"
                result["error"] = (
                    "MinerU batch did not produce valid output for this document"
                )
            result["finished_at"] = _now()
        shutil.rmtree(batch_output, ignore_errors=True)
    return [results[item["document_id"]] for item in batch]


def _run_mineru_item(
    *,
    item: dict[str, Any],
    index: int,
    total: int,
    output_dir: Path,
    execute: bool,
    executable: str | None,
    command: str,
    method: str,
    backend: str | None,
    timeout_seconds: int,
    process_directory: Path | None,
    process_environment: dict[str, str],
    extra_args: list[str] | None,
    reuse_existing: bool,
    min_markdown_chars: int,
    stage_name: str,
    sandbox_runtime: Any,
) -> dict[str, Any]:
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
        result["finished_at"] = _now()
        return result
    if sandbox_runtime is None and not executable:
        result["status"] = "unavailable"
        result["error"] = f"MinerU command not found: {command}"
        result["finished_at"] = _now()
        return result

    target.mkdir(parents=True, exist_ok=True)
    existing = _inspect_output(
        target, min_markdown_chars, expected_pages=item.get("expected_pages")
    )
    if reuse_existing and existing["valid"]:
        result.update(existing)
        result["status"] = "reused"
        result["duration_seconds"] = 0.0
        result["finished_at"] = _now()
        return result

    started = time.monotonic()
    process_env = os.environ.copy()
    process_env.update({key: str(value) for key, value in process_environment.items()})
    heartbeat_stop = threading.Event()
    heartbeat = threading.Thread(
        target=_log_mineru_heartbeat,
        args=(heartbeat_stop, index, total, item, started, stage_name),
        daemon=True,
    )
    heartbeat.start()
    try:
        if sandbox_runtime is not None:
            remote = sandbox_runtime.run_mineru(
                item,
                target,
                command=command,
                method=method,
                backend=backend,
                timeout_seconds=timeout_seconds,
                environment=process_environment,
                extra_args=extra_args,
            )
            result.update(remote)
            return_code = remote.get("return_code")
            stdout_text = str(remote.get("stdout_tail") or "")
            stderr_text = str(remote.get("stderr_tail") or "")
        else:
            completed = subprocess.run(
                cli,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                env=process_env,
                cwd=process_directory,
            )
            return_code = completed.returncode
            stdout_text = completed.stdout
            stderr_text = completed.stderr
        result["return_code"] = return_code
        result["stdout_tail"] = stdout_text[-4000:]
        result["stderr_tail"] = stderr_text[-4000:]
        (target / "mineru.stdout.log").write_text(stdout_text, encoding="utf-8")
        (target / "mineru.stderr.log").write_text(stderr_text, encoding="utf-8")
        inspected = _inspect_output(
            target, min_markdown_chars, expected_pages=item.get("expected_pages")
        )
        result.update(inspected)
        result["status"] = "success" if return_code == 0 and inspected["valid"] else "failed"
        if return_code == 0 and not inspected["valid"]:
            result["error"] = "MinerU exited successfully but required output validation failed"
    except subprocess.TimeoutExpired as exc:
        result["status"] = "timeout"
        result["error"] = str(exc)
        if exc.stdout:
            (target / "mineru.stdout.log").write_text(_as_text(exc.stdout), encoding="utf-8")
        if exc.stderr:
            (target / "mineru.stderr.log").write_text(_as_text(exc.stderr), encoding="utf-8")
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        heartbeat_stop.set()
        heartbeat.join(timeout=2)
    result["duration_seconds"] = round(time.monotonic() - started, 3)
    result["finished_at"] = _now()
    return result


def _log_mineru_heartbeat(
    stop: threading.Event,
    index: int,
    total: int,
    item: dict[str, Any],
    started: float,
    stage_name: str = "mineru_queue",
) -> None:
    file_name = Path(item["source_path"]).name
    pages = item.get("expected_pages") or "unknown"
    log_progress(
        stage_name,
        index - 1,
        total,
        f"running {index}/{total}: {file_name}, pages={pages}",
        status="running",
    )
    while not stop.wait(15):
        elapsed = round(time.monotonic() - started, 1)
        pipeline_logger().info(
            "HEARTBEAT | %s | document=%d/%d | file=%s | pages=%s | elapsed_seconds=%.1f",
            stage_name,
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

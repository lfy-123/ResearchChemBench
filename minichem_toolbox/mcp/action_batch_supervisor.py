"""Persistent resource-aware supervisor for asynchronous predefined Actions."""

from __future__ import annotations

import ctypes
import json
import os
import signal
import sys
import time
import uuid
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from minichem_toolbox.distributed_pool import distributed_enabled, pool_snapshot
from minichem_toolbox.resource_budget import (
    active_resource_usage,
    evaluation_resource_budget,
    normalize_resource_limits,
)
from minichem_toolbox.service import execute_action

from .result_transport import compact_action_result
from .tracing import execute_traced


TERMINAL_STATUSES = {
    "success",
    "partial_success",
    "invalid_request",
    "unsupported",
    "unavailable",
    "failed",
    "timeout",
    "cancelled",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + f".{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def _request_parent_death_signal(expected_parent_pid: int) -> bool:
    """Terminate this detached supervisor when its owning MCP process exits."""

    if not sys.platform.startswith("linux"):
        return True
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return os.getppid() == expected_parent_pid


def _capacity_slots() -> list[dict[str, int]]:
    if distributed_enabled():
        return [dict(worker["available"]) for worker in pool_snapshot()["workers"]]
    budget = evaluation_resource_budget()
    reserved = active_resource_usage()
    return [
        {
            "cpu_cores": max(0, budget.cpu_cores - reserved["cpu_cores"]),
            "memory_mb": max(0, budget.memory_mb - reserved["memory_mb"]),
            "gpu_count": max(0, budget.gpu_count - reserved["gpu_count"]),
        }
    ]


def _select_launches(
    pending: list[dict[str, Any]], *, limit: int
) -> list[dict[str, Any]]:
    slots = _capacity_slots()
    selected: list[dict[str, Any]] = []
    for item in pending:
        if len(selected) >= limit:
            break
        resources = item["normalized_resources"]
        candidates = [
            (slot["cpu_cores"], slot["memory_mb"], index)
            for index, slot in enumerate(slots)
            if resources["cpu_cores"] <= slot["cpu_cores"]
            and resources["memory_mb"] <= slot["memory_mb"]
            and resources["gpu_count"] <= slot["gpu_count"]
        ]
        if not candidates:
            continue
        _cpu, _memory, slot_index = max(candidates)
        slot = slots[slot_index]
        for name in ("cpu_cores", "memory_mb", "gpu_count"):
            slot[name] -= resources[name]
        selected.append(item)
    return selected


def _execute_item(request: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    action_request = {
        "backend_id": request["backend_id"],
        "component_backends": request.get("component_backends") or {},
        "source_id": None,
        "inputs": item.get("inputs") or {},
        "method_spec": request.get("method_spec") or {},
        "action_settings": request.get("action_settings") or {},
        "resource_limits": item["resource_limits"],
    }
    started = time.monotonic()
    try:
        result = execute_traced(
            request["action_id"],
            {
                "entrypoint": "submit_action_batch_async",
                "batch_id": request["batch_id"],
                "batch_item_id": item["item_id"],
                "batch_index": item["batch_index"],
                "request": action_request,
            },
            lambda: compact_action_result(
                execute_action(request["action_id"], action_request)
            ),
            capture_artifacts=False,
        )
    except Exception as exc:
        result = {
            "status": "failed",
            "error": {
                "code": "async_batch_child_transport_error",
                "message": f"{type(exc).__name__}: {exc}",
            },
            "retryable": False,
        }
    return {
        "result": result,
        "duration_seconds": round(time.monotonic() - started, 6),
    }


def run_batch(request_path: Path) -> int:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    status_path = request_path.with_name("status.json")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["status"] = "running"
    status["supervisor_pid"] = os.getpid()
    status["started_at"] = _now()
    sequence = int(status.get("last_sequence") or 0)

    def event(event_type: str, **payload: Any) -> None:
        nonlocal sequence
        sequence += 1
        status.setdefault("events", []).append(
            {
                "sequence": sequence,
                "timestamp": _now(),
                "type": event_type,
                **payload,
            }
        )
        status["last_sequence"] = sequence
        status["updated_at"] = _now()
        _atomic_json(status_path, status)

    event("batch_started", supervisor_pid=os.getpid())
    pending = sorted(
        request["items"],
        key=lambda item: (
            -item["normalized_resources"]["cpu_cores"],
            -item["normalized_resources"]["memory_mb"],
            item["batch_index"],
        ),
    )
    item_status = {item["item_id"]: item for item in status["items"]}
    maximum_concurrency = min(
        len(pending), int(request.get("max_concurrency") or len(pending))
    )
    active: dict[Future, dict[str, Any]] = {}
    with ThreadPoolExecutor(
        max_workers=max(1, maximum_concurrency),
        thread_name_prefix="researchchem-async-action",
    ) as executor:
        while pending or active:
            launchable = _select_launches(
                pending, limit=maximum_concurrency - len(active)
            )
            for item in launchable:
                pending.remove(item)
                record = item_status[item["item_id"]]
                record["status"] = "running"
                record["started_at"] = _now()
                future = executor.submit(_execute_item, request, item)
                active[future] = item
                event(
                    "item_started",
                    item_id=item["item_id"],
                    batch_index=item["batch_index"],
                    resource_limits=item["resource_limits"],
                )
            if not active:
                time.sleep(0.5)
                continue
            completed, _unfinished = wait(
                tuple(active), timeout=0.5, return_when=FIRST_COMPLETED
            )
            for future in completed:
                item = active.pop(future)
                outcome = future.result()
                result = outcome["result"]
                error_code = str((result.get("error") or {}).get("code") or "")
                if (
                    result.get("status") == "unavailable"
                    and error_code == "distributed_resource_capacity_unavailable"
                ):
                    record = item_status[item["item_id"]]
                    record["status"] = "queued"
                    record.pop("started_at", None)
                    pending.append(item)
                    pending.sort(
                        key=lambda value: (
                            -value["normalized_resources"]["cpu_cores"],
                            -value["normalized_resources"]["memory_mb"],
                            value["batch_index"],
                        )
                    )
                    event("item_requeued", item_id=item["item_id"])
                    continue
                record = item_status[item["item_id"]]
                record.update(
                    {
                        "status": str(result.get("status") or "failed"),
                        "finished_at": _now(),
                        "duration_seconds": outcome["duration_seconds"],
                        "result": result,
                    }
                )
                event(
                    "item_finished",
                    item_id=item["item_id"],
                    batch_index=item["batch_index"],
                    status=record["status"],
                    resource_snapshot=(
                        pool_snapshot() if distributed_enabled() else None
                    ),
                )
    successful = sum(
        item["status"] in {"success", "partial_success"}
        for item in status["items"]
    )
    status["status"] = (
        "success"
        if successful == len(status["items"])
        else "partial_success" if successful else "failed"
    )
    status["finished_at"] = _now()
    status["successful_item_count"] = successful
    status["failed_item_count"] = len(status["items"]) - successful
    event(
        "batch_finished",
        status=status["status"],
        successful_item_count=successful,
        failed_item_count=status["failed_item_count"],
        resource_snapshot=pool_snapshot() if distributed_enabled() else None,
    )
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: action_batch_supervisor.py REQUEST.json", file=sys.stderr)
        return 64
    request_path = Path(sys.argv[1]).resolve()
    request = json.loads(request_path.read_text(encoding="utf-8"))
    expected_parent_pid = int(request.get("supervisor_parent_pid") or 0)
    if expected_parent_pid <= 0:
        print("missing supervisor_parent_pid", file=sys.stderr)
        return 64
    try:
        parent_is_alive = _request_parent_death_signal(expected_parent_pid)
    except OSError as exc:
        print(f"failed to configure parent-death signal: {exc}", file=sys.stderr)
        return 70
    if not parent_is_alive:
        print("owning MCP process exited before supervisor startup", file=sys.stderr)
        return 143
    return run_batch(request_path)


if __name__ == "__main__":
    raise SystemExit(main())

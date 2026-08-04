"""Persistent asynchronous Action batch submission and event feedback."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from minichem_toolbox.catalog import action_specs
from minichem_toolbox.distributed_pool import (
    DistributedResourceLimitExceeded,
    distributed_enabled,
    pool_snapshot,
    validate_distributed_resource_limits,
)
from minichem_toolbox.paths import PROJECT_ROOT
from minichem_toolbox.resource_budget import (
    ResourceBudgetExceeded,
    normalize_resource_limits,
    resource_budget_record,
    validate_resource_limits,
)

from .discovery_models import ActionBatchRequest, ExecutionEventWaitRequest
from .tracing import execute_traced
from .workspace import relative_workspace_path, resolve_workspace_output_path


ASYNC_ACTION_TOOL_NAMES = (
    "submit_action_batch_async",
    "wait_execution_events",
)
BATCH_ROOT = Path("outputs") / "action_batches"


TOOL_DESCRIPTIONS = {
    "submit_action_batch_async": (
        "Submit up to 32 already-independent requests sharing one batch-safe Action and backend. "
        "Returns immediately with a persistent batch_id. The toolbox sorts waiting children by "
        "requested CPU, then memory, automatically chooses anonymous compute workers, and queues "
        "legal requests until capacity is available. Do not use this for dependent calculations."
    ),
    "wait_execution_events": (
        "Wait up to 600 seconds for new events from one or more asynchronous Action batches. Use "
        "long waits for compute-heavy jobs and pass the returned per-batch next_sequence values on "
        "the next call. A timeout with no new events returns compact status counts instead of "
        "repeating every item. Completion/failure events include the latest anonymous worker CPU "
        "and memory availability so new work can be planned."
    ),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + f".{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def _batch_directory(batch_id: str, *, must_exist: bool = True) -> Path:
    directory = resolve_workspace_output_path(str(BATCH_ROOT / batch_id))
    if must_exist and not directory.is_dir():
        raise KeyError(f"Unknown asynchronous Action batch {batch_id!r}")
    return directory


def _validation_error(request: ActionBatchRequest) -> dict[str, Any] | None:
    specification = action_specs().get(request.action_id)
    if specification is None:
        return {"code": "unknown_action", "message": request.action_id}
    if not specification.batch_safe:
        return {
            "code": "action_not_batch_safe",
            "message": f"Action {request.action_id!r} does not declare batch_safe=true.",
        }
    if request.backend_id not in specification.backend_ids:
        return {
            "code": "backend_not_supported",
            "message": (
                f"Backend {request.backend_id!r} does not provide {request.action_id!r}."
            ),
        }
    if len({item.item_id for item in request.items}) != len(request.items):
        return {
            "code": "duplicate_batch_item_id",
            "message": "Every batch item_id must be unique.",
        }
    try:
        for item in request.items:
            resources = normalize_resource_limits(item.resource_limits)
            if distributed_enabled():
                validate_distributed_resource_limits(resources)
            else:
                validate_resource_limits(resources)
    except (DistributedResourceLimitExceeded, ResourceBudgetExceeded) as exc:
        return exc.as_error()
    return None


def _submit_action_batch_async(request: ActionBatchRequest) -> dict[str, Any]:
    error = _validation_error(request)
    if error is not None:
        return {"status": "invalid_request", "error": error}
    batch_id = f"batch_{uuid.uuid4().hex}"
    directory = _batch_directory(batch_id, must_exist=False)
    directory.mkdir(parents=True, exist_ok=False)
    submitted_at = _now()
    items = []
    status_items = []
    for index, item in enumerate(request.items):
        resource_limits = item.resource_limits.model_dump(mode="json")
        items.append(
            {
                "item_id": item.item_id,
                "batch_index": index,
                "inputs": item.inputs,
                "resource_limits": resource_limits,
                "normalized_resources": normalize_resource_limits(resource_limits),
            }
        )
        status_items.append(
            {
                "item_id": item.item_id,
                "batch_index": index,
                "status": "queued",
                "resource_limits": resource_limits,
            }
        )
    request_record = {
        "schema_version": 1,
        "batch_id": batch_id,
        "action_id": request.action_id,
        "backend_id": request.backend_id,
        "component_backends": request.component_backends,
        "method_spec": request.method_spec,
        "action_settings": request.action_settings,
        "items": items,
        "max_concurrency": request.max_concurrency,
        "submitted_at": submitted_at,
        "execution_mode": "distributed" if distributed_enabled() else "local",
        "supervisor_parent_pid": os.getpid(),
    }
    status_record = {
        "schema_version": 1,
        "batch_id": batch_id,
        "status": "queued",
        "action_id": request.action_id,
        "backend_id": request.backend_id,
        "submitted_at": submitted_at,
        "updated_at": submitted_at,
        "supervisor_pid": None,
        "last_sequence": 0,
        "events": [],
        "items": status_items,
    }
    request_path = directory / "request.json"
    status_path = directory / "status.json"
    _atomic_json(request_path, request_record)
    _atomic_json(status_path, status_record)
    try:
        with (directory / "supervisor.stdout.log").open("ab") as stdout_handle, (
            directory / "supervisor.stderr.log"
        ).open("ab") as stderr_handle:
            supervisor = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "minichem_mcp_tools.action_batch_supervisor",
                    str(request_path),
                ],
                cwd=PROJECT_ROOT,
                stdin=subprocess.DEVNULL,
                stdout=stdout_handle,
                stderr=stderr_handle,
                env=os.environ.copy(),
                shell=False,
                start_new_session=True,
                close_fds=True,
            )
    except Exception as exc:
        status_record.update(
            {
                "status": "failed",
                "updated_at": _now(),
                "error": {"code": "batch_supervisor_start_failed", "message": str(exc)},
            }
        )
        _atomic_json(status_path, status_record)
        return {"status": "failed", **status_record}
    return {
        "status": "success",
        "batch_id": batch_id,
        "batch_status": "queued",
        "action_id": request.action_id,
        "backend_id": request.backend_id,
        "item_count": len(items),
        "supervisor_pid": supervisor.pid,
        "status_path": relative_workspace_path(status_path),
        "execution_mode": request_record["execution_mode"],
        "scheduling": "largest_cpu_then_memory_first",
        "resource_snapshot": pool_snapshot() if distributed_enabled() else resource_budget_record(),
        "next_step": (
            "Call wait_execution_events with this batch_id and after_sequences set to "
            "the last returned next_sequence. For long scientific calculations, use "
            "timeout_seconds=600 instead of frequent short polling."
        ),
    }


def _read_events(request: ExecutionEventWaitRequest) -> dict[str, Any]:
    deadline = time.monotonic() + request.timeout_seconds
    while True:
        batches = []
        any_new = False
        for batch_id in request.batch_ids:
            status_path = _batch_directory(batch_id) / "status.json"
            status = json.loads(status_path.read_text(encoding="utf-8"))
            after = int(request.after_sequences.get(batch_id, 0))
            events = [
                event
                for event in status.get("events") or []
                if int(event.get("sequence") or 0) > after
            ]
            any_new = any_new or bool(events)
            terminal = status.get("status") in {
                "success",
                "partial_success",
                "failed",
                "cancelled",
            }
            status_items = status.get("items") or []
            status_counts: dict[str, int] = {}
            for item in status_items:
                item_status = str(item.get("status") or "unknown")
                status_counts[item_status] = status_counts.get(item_status, 0) + 1
            batch = {
                "batch_id": batch_id,
                "status": status.get("status"),
                "terminal": terminal,
                "events": events,
                "next_sequence": int(status.get("last_sequence") or 0),
                "item_status_counts": status_counts,
            }
            if events or terminal:
                batch["items"] = [
                    {
                        key: item.get(key)
                        for key in (
                            "item_id",
                            "batch_index",
                            "status",
                            "resource_limits",
                            "started_at",
                            "finished_at",
                        )
                        if key in item
                    }
                    for item in status_items
                ]
            batches.append(batch)
        if any_new or time.monotonic() >= deadline:
            return {
                "status": "success",
                "batches": batches,
                "event_count": sum(len(item["events"]) for item in batches),
                "timed_out": not any_new and request.timeout_seconds > 0,
                "resource_snapshot": pool_snapshot()
                if distributed_enabled()
                else resource_budget_record(),
            }
        time.sleep(min(0.25, max(0.0, deadline - time.monotonic())))


def submit_action_batch_async(request: ActionBatchRequest) -> dict[str, Any]:
    return execute_traced(
        "submit_action_batch_async",
        {"request": request.model_dump(mode="json")},
        lambda: _submit_action_batch_async(request),
        capture_artifacts=False,
    )


def wait_execution_events(request: ExecutionEventWaitRequest) -> dict[str, Any]:
    return execute_traced(
        "wait_execution_events",
        {"request": request.model_dump(mode="json")},
        lambda: _read_events(request),
        capture_artifacts=False,
    )


def register_async_action_tools(mcp) -> list[str]:
    functions = {name: globals()[name] for name in ASYNC_ACTION_TOOL_NAMES}
    for name, function in functions.items():
        mcp.tool(name=name, description=TOOL_DESCRIPTIONS[name])(function)
    return list(functions)


__all__ = [
    *ASYNC_ACTION_TOOL_NAMES,
    "ASYNC_ACTION_TOOL_NAMES",
    "register_async_action_tools",
]

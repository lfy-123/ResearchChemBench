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

from chemistry_toolbox.src.catalog import action_specs
from chemistry_toolbox.src.distributed_pool import (
    DistributedResourceLimitExceeded,
    distributed_enabled,
    pool_snapshot,
    validate_distributed_resource_limits,
)
from chemistry_toolbox.src.paths import PROJECT_ROOT
from chemistry_toolbox.src.resource_budget import (
    ResourceBudgetExceeded,
    normalize_resource_limits,
    resource_budget_record,
    validate_resource_limits,
)

from .discovery_models import ActionBatchRequest, ExecutionEventWaitRequest
from .supervision_policy import supervision_policy
from .tracing import execute_traced
from .workspace import relative_workspace_path, resolve_workspace_output_path


ASYNC_ACTION_TOOL_NAMES = (
    "submit_action_batch_async",
    "wait_execution_events",
)
BATCH_ROOT = Path("outputs") / "action_batches"
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


TOOL_DESCRIPTIONS = {
    "submit_action_batch_async": (
        "Submit up to 32 already-independent requests sharing one batch-safe Action and backend. "
        "Returns immediately with a persistent batch_id. The toolbox sorts waiting children by "
        "requested CPU, then memory, automatically chooses anonymous compute workers, and queues "
        "legal requests until capacity is available. Do not use this for dependent calculations."
    ),
    "wait_execution_events": (
        "Wait internally for a stable aggregate update from one or more Action batches. Terminal "
        "items start an evaluator-controlled settle window while running work and automatic queue "
        "fill continue. Returns new terminal results/artifacts, current running/queued items, "
        "resource availability, and per-batch next_sequence cursors. Do not poll status files."
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
    input_fingerprints: dict[str, list[str]] = {}
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
        fingerprint = json.dumps(item.inputs, sort_keys=True, separators=(",", ":"))
        input_fingerprints.setdefault(fingerprint, []).append(item.item_id)
    duplicate_input_groups = [
        item_ids for item_ids in input_fingerprints.values() if len(item_ids) > 1
    ]
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
        "duplicate_input_groups": duplicate_input_groups,
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
                    "chemistry_toolbox.mcp.action_batch_supervisor",
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
        "warnings": (
            [
                {
                    "code": "duplicate_batch_item_inputs",
                    "message": "Items with identical inputs may repeat the same computation.",
                    "item_id_groups": duplicate_input_groups,
                }
            ]
            if duplicate_input_groups
            else []
        ),
        "next_step": (
            "Call wait_execution_events with this batch_id. Reuse returned next_sequence "
            "cursors only for remaining batches; the toolbox waits through the stable window."
        ),
    }


def _resource_snapshot() -> dict[str, Any]:
    return pool_snapshot() if distributed_enabled() else resource_budget_record()


def _resource_signature(snapshot: dict[str, Any]) -> str:
    if snapshot.get("execution_mode") == "distributed":
        snapshot = {
            "available_cpu_cores": snapshot.get("available_cpu_cores"),
            "available_memory_mb": snapshot.get("available_memory_mb"),
            "active_reservation_count": snapshot.get("active_reservation_count"),
            "queued_request_count": snapshot.get("queued_request_count"),
            "workers": [
                {
                    "worker_id": worker.get("worker_id"),
                    "available": worker.get("available"),
                    "active_reservation_count": worker.get(
                        "active_reservation_count"
                    ),
                    "scheduling_state": worker.get("scheduling_state"),
                }
                for worker in snapshot.get("workers") or []
            ],
        }
    return json.dumps(snapshot, sort_keys=True, separators=(",", ":"))


def _item_worker_id(item: dict[str, Any]) -> str | None:
    return ((item.get("result") or {}).get("provenance") or {}).get(
        "compute_worker_id"
    )


def _compact_terminal_item(batch_id: str, item: dict[str, Any]) -> dict[str, Any]:
    return {
        "batch_id": batch_id,
        "item_id": item.get("item_id"),
        "batch_index": item.get("batch_index"),
        "status": item.get("status"),
        "worker_id": _item_worker_id(item),
        "resource_limits": item.get("resource_limits") or {},
        "duration_seconds": item.get("duration_seconds"),
        "finished_at": item.get("finished_at"),
        "result": item.get("result") or {},
    }


def _compact_active_item(batch_id: str, item: dict[str, Any]) -> dict[str, Any]:
    return {
        "batch_id": batch_id,
        "item_id": item.get("item_id"),
        "batch_index": item.get("batch_index"),
        "status": item.get("status"),
        "worker_id": _item_worker_id(item),
        "resource_limits": item.get("resource_limits") or {},
        "started_at": item.get("started_at"),
    }


def _read_events(
    request: ExecutionEventWaitRequest,
    *,
    policy: dict[str, int] | None = None,
    monotonic_fn=time.monotonic,
    sleep_fn=time.sleep,
) -> dict[str, Any]:
    settings = dict(policy or supervision_policy())
    started = monotonic_fn()
    aggregation_started: float | None = None
    last_material_change: float | None = None
    previous_state_signature: str | None = None
    previous_resource_signature: str | None = None
    stable_resource_snapshots = 0
    internal_checks = 0
    newly_terminal_keys: set[tuple[str, str]] = set()
    latest_batches: list[dict[str, Any]] = []
    latest_resource: dict[str, Any] = {}
    return_reason = "heartbeat"

    while True:
        now = monotonic_fn()
        try:
            batches: list[dict[str, Any]] = []
            state_rows: list[dict[str, Any]] = []
            for batch_id in request.batch_ids:
                status = json.loads(
                    (_batch_directory(batch_id) / "status.json").read_text(
                        encoding="utf-8"
                    )
                )
                after = int(request.after_sequences.get(batch_id, 0))
                events = [
                    event
                    for event in status.get("events") or []
                    if int(event.get("sequence") or 0) > after
                ]
                for event in events:
                    if event.get("type") == "item_finished" and event.get("item_id"):
                        newly_terminal_keys.add((batch_id, str(event["item_id"])))
                items = status.get("items") or []
                counts: dict[str, int] = {}
                for item in items:
                    item_status = str(item.get("status") or "unknown")
                    counts[item_status] = counts.get(item_status, 0) + 1
                    state_rows.append(
                        {
                            "batch_id": batch_id,
                            "item_id": item.get("item_id"),
                            "status": item_status,
                            "worker_id": _item_worker_id(item),
                        }
                    )
                batches.append(
                    {
                        "batch_id": batch_id,
                        "status": status.get("status"),
                        "terminal": str(status.get("status"))
                        in {"success", "partial_success", "failed", "cancelled"},
                        "events": events,
                        "next_sequence": int(status.get("last_sequence") or 0),
                        "item_status_counts": counts,
                        "items": items,
                    }
                )
            resource = _resource_snapshot()
        except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
            return {
                "status": "failed",
                "return_reason": "monitor_error",
                "error": {
                    "code": "action_batch_monitor_error",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "remaining_batch_ids": list(request.batch_ids),
                "wait_duration_seconds": round(max(0, now - started), 3),
                "internal_check_count": internal_checks,
            }

        internal_checks += 1
        state_signature = json.dumps(
            state_rows, sort_keys=True, separators=(",", ":")
        )
        resource_signature = _resource_signature(resource)
        material_change = (
            previous_state_signature is not None
            and state_signature != previous_state_signature
        ) or (
            previous_resource_signature is not None
            and resource_signature != previous_resource_signature
        )
        stable_resource_snapshots = (
            stable_resource_snapshots + 1
            if resource_signature == previous_resource_signature
            else 1
        )
        previous_state_signature = state_signature
        previous_resource_signature = resource_signature
        latest_batches = batches
        latest_resource = resource

        terminal_event_count = sum(
            event.get("type") in {"item_finished", "batch_finished"}
            for batch in batches
            for event in batch["events"]
        )
        all_terminal = all(batch["terminal"] for batch in batches)
        if (terminal_event_count or all_terminal) and aggregation_started is None:
            aggregation_started = now
            last_material_change = now
        elif aggregation_started is not None and material_change:
            last_material_change = now

        if aggregation_started is not None:
            aggregation_elapsed = now - aggregation_started
            settled_elapsed = now - (last_material_change or aggregation_started)
            if all_terminal and stable_resource_snapshots >= 2:
                return_reason = "all_terminal"
                break
            if aggregation_elapsed >= settings["max_batch_seconds"]:
                return_reason = "aggregation_time_cap"
                break
            if settled_elapsed >= settings["settle_seconds"]:
                return_reason = "settled_state_update"
                break
        elif now - started >= settings["heartbeat_seconds"]:
            return_reason = "heartbeat"
            break
        sleep_fn(settings["poll_interval_seconds"])

    terminal_items: list[dict[str, Any]] = []
    running_items: list[dict[str, Any]] = []
    queued_items: list[dict[str, Any]] = []
    transitions: list[dict[str, Any]] = []
    batch_summaries: list[dict[str, Any]] = []
    for batch in latest_batches:
        batch_id = batch["batch_id"]
        for item in batch.pop("items"):
            key = (batch_id, str(item.get("item_id")))
            if key in newly_terminal_keys:
                terminal_items.append(_compact_terminal_item(batch_id, item))
            elif item.get("status") == "queued":
                queued_items.append(_compact_active_item(batch_id, item))
            elif str(item.get("status")) not in TERMINAL_STATUSES:
                running_items.append(_compact_active_item(batch_id, item))
        transitions.extend(
            {
                key: event.get(key)
                for key in ("sequence", "timestamp", "type", "item_id", "status")
                if key in event
            }
            for event in batch.pop("events")
        )
        batch_summaries.append(batch)
    remaining = [
        batch["batch_id"] for batch in batch_summaries if not batch["terminal"]
    ]
    finished = monotonic_fn()
    aggregation_duration = (
        finished - aggregation_started if aggregation_started is not None else 0
    )
    settled_for = (
        finished - last_material_change if last_material_change is not None else 0
    )
    return {
        "status": "success",
        "return_reason": return_reason,
        "settled_for_seconds": round(max(0, settled_for), 3),
        "aggregation_duration_seconds": round(max(0, aggregation_duration), 3),
        "wait_duration_seconds": round(max(0, finished - started), 3),
        "resource_snapshot_stable": stable_resource_snapshots >= 2,
        "newly_terminal_items": terminal_items,
        "running_items": running_items,
        "queued_items": queued_items,
        "remaining_batch_ids": remaining,
        "next_sequences": {
            batch["batch_id"]: batch["next_sequence"] for batch in batch_summaries
        },
        "state_transitions": transitions,
        "batches": batch_summaries,
        "event_count": len(transitions),
        "summary": {
            "monitored_batches": len(batch_summaries),
            "newly_terminal": len(terminal_items),
            "running": len(running_items),
            "queued": len(queued_items),
            "remaining_batches": len(remaining),
        },
        "resource_snapshot": latest_resource,
        "internal_check_count": internal_checks,
        "deprecated_request_timeout_seconds_ignored": request.timeout_seconds,
        "recommended_action": (
            "process_terminal_results_then_wait_remaining"
            if terminal_items and remaining
            else "process_terminal_results"
            if terminal_items
            else "wait_again_with_remaining_batch_ids"
        ),
    }


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

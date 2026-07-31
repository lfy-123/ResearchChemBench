"""FastMCP bindings for progressive, task-independent catalog discovery."""

from __future__ import annotations

import threading
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

from pydantic import BaseModel

from researchchem_toolbox.discovery import (
    browse_action_category as _browse_action_category,
    inspect_action as _inspect_action,
    inspect_backend as _inspect_backend,
    inspect_resource as _inspect_resource,
    list_action_domains as _list_action_domains,
    search_actions as _search_actions,
    search_resources as _search_resources,
)
from researchchem_toolbox.catalog import action_specs
from researchchem_toolbox.distributed_pool import distributed_enabled, pool_snapshot
from researchchem_toolbox.resource_budget import (
    active_resource_jobs,
    active_resource_usage,
    evaluation_resource_budget,
    normalize_resource_limits,
)
from researchchem_toolbox.service import execute_action as _execute_action

from .discovery_models import (
    ActionCategoryBrowseRequest,
    ActionBatchRequest,
    ActionDomainListRequest,
    ActionInspectRequest,
    ActionSearchRequest,
    BackendInspectRequest,
    ProgressiveActionRequest,
    ResourceInspectRequest,
    ResourceSearchRequest,
)
from .result_transport import compact_action_result
from .tracing import execute_traced


RequestT = TypeVar("RequestT", bound=BaseModel)


PROGRESSIVE_DISCOVERY_TOOL_NAMES = (
    "list_action_domains",
    "browse_action_category",
    "search_actions",
    "inspect_action",
    "inspect_backend",
    "search_resources",
    "inspect_resource",
    "execute_action",
    "submit_action_batch",
)


TOOL_DESCRIPTIONS = {
    "list_action_domains": (
        "Return the compact complete domain index, counts, and by default every exact action_id "
        "grouped by domain. This does not select a domain or infer anything from the task."
    ),
    "browse_action_category": (
        "Return all compact Action summaries in one exact category selected from "
        "list_action_domains. Use this when the category is known and the Agent needs to compare "
        "the complete local choice set before inspecting one Action."
    ),
    "search_actions": (
        "Search the complete frozen Action catalog using English aliases and BM25 relevance. "
        "Hybrid mode adds offline all-MiniLM-L6-v2 semantic recall when its local cache is present; "
        "it never downloads a model or changes the catalog."
    ),
    "inspect_action": (
        "Inspect one exact Action before calling it. Pass backend_id and use the default contract "
        "level to receive a compact executable request template with every required field. Use "
        "full only for catalog, resource, runtime, or health audit."
    ),
    "inspect_backend": (
        "Inspect one exact Backend, its installed health and resources, and every Action capability. "
        "Optionally request the exact contract for one Action it provides."
    ),
    "search_resources": (
        "Search all registered scientific data/model/resource entries with explicit neutral filters. "
        "Returns compact exact ids and selection syntax without choosing a family or variant."
    ),
    "inspect_resource": (
        "Resolve one exact resource_id to its complete immutable metadata, coverage and explicit "
        "selection contract."
    ),
    "execute_action": (
        "Execute one exact predefined Scientific/Data Action selected by action_id. Start from the "
        "compact template returned by inspect_action for this exact backend and replace every "
        "placeholder. If validation returns repair_guidance, correct that same request and retry "
        "once before considering another backend. The dispatcher performs no scientific defaults, "
        "automatic retry, or fallback. Dense "
        "results are returned as concise scalars plus a typed primary ArtifactRef; the immutable "
        "artifact contains the complete coordinates, matrices, modes, or trajectories."
    ),
    "submit_action_batch": (
        "Run up to 32 independent requests concurrently when they share one Action and backend. "
        "Use this instead of repeated execute_action calls for two or more independent structures. "
        "Only batch_safe Actions are accepted; concurrency is derived from active CPU, memory, and "
        "GPU capacity, excess items queue automatically, and every child keeps an independent trace."
    ),
}


def _invoke_discovery(
    name: str,
    request: RequestT,
    function: Callable[[], dict[str, Any]],
) -> dict[str, Any]:
    arguments = {"request": request.model_dump(mode="json")}

    def run() -> dict[str, Any]:
        try:
            return function()
        except (KeyError, ValueError) as exc:
            return {
                "status": "invalid_request",
                "error": {
                    "code": "invalid_catalog_discovery_request",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "automatic_fallback": False,
            }
        except OSError as exc:
            return {
                "status": "failed",
                "error": {
                    "code": "catalog_discovery_os_error",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "automatic_fallback": False,
            }

    return execute_traced(name, arguments, run, capture_artifacts=False)


def list_action_domains(request: ActionDomainListRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "list_action_domains",
        request,
        lambda: _list_action_domains(**request.model_dump(mode="python")),
    )


def browse_action_category(request: ActionCategoryBrowseRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "browse_action_category",
        request,
        lambda: _browse_action_category(**request.model_dump(mode="python")),
    )


def search_actions(request: ActionSearchRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "search_actions",
        request,
        lambda: _search_actions(**request.model_dump(mode="python")),
    )


def inspect_action(request: ActionInspectRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "inspect_action",
        request,
        lambda: _inspect_action(**request.model_dump(mode="python")),
    )


def inspect_backend(request: BackendInspectRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "inspect_backend",
        request,
        lambda: _inspect_backend(**request.model_dump(mode="python")),
    )


def search_resources(request: ResourceSearchRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "search_resources",
        request,
        lambda: _search_resources(**request.model_dump(mode="python")),
    )


def inspect_resource(request: ResourceInspectRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "inspect_resource",
        request,
        lambda: _inspect_resource(**request.model_dump(mode="python")),
    )


def execute_action(request: ProgressiveActionRequest) -> dict[str, Any]:
    value = request.model_dump(mode="json")
    action_id = str(value.pop("action_id"))
    arguments = {
        "entrypoint": "progressive_execute_action",
        "request": value,
    }
    # Trace under the real scientific Action id so scoring and provenance stay
    # identical to the historical one-tool-per-Action surface.
    return execute_traced(
        action_id,
        arguments,
        lambda: compact_action_result(_execute_action(action_id, value)),
    )


def _select_distributed_batch_launches(
    pending: list[tuple[int, Any, dict[str, int]]], *, limit: int
) -> list[tuple[int, Any, dict[str, int]]]:
    """Place the next synchronous batch children against live worker slots."""

    slots = [dict(worker["available"]) for worker in pool_snapshot()["workers"]]
    selected: list[tuple[int, Any, dict[str, int]]] = []
    ordered = sorted(
        pending,
        key=lambda value: (
            -value[2]["cpu_cores"],
            -value[2]["memory_mb"],
            value[0],
        ),
    )
    for item in ordered:
        if len(selected) >= limit:
            break
        resources = item[2]
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


def submit_action_batch(request: ActionBatchRequest) -> dict[str, Any]:
    specification = action_specs().get(request.action_id)
    if specification is None:
        return {
            "status": "invalid_request",
            "error": {"code": "unknown_action", "message": request.action_id},
        }
    if not specification.batch_safe:
        return {
            "status": "invalid_request",
            "error": {
                "code": "action_not_batch_safe",
                "message": f"Action {request.action_id!r} does not declare batch_safe=true.",
            },
        }
    if request.backend_id not in specification.backend_ids:
        return {
            "status": "invalid_request",
            "error": {
                "code": "backend_not_supported",
                "message": (
                    f"Backend {request.backend_id!r} does not provide {request.action_id!r}."
                ),
            },
        }
    if len({item.item_id for item in request.items}) != len(request.items):
        return {
            "status": "invalid_request",
            "error": {
                "code": "duplicate_batch_item_id",
                "message": "Every batch item_id must be unique.",
            },
        }

    item_resources = [
        normalize_resource_limits(item.resource_limits) for item in request.items
    ]
    maximum_item = {
        name: max(resources[name] for resources in item_resources)
        for name in ("cpu_cores", "memory_mb", "gpu_count")
    }
    if distributed_enabled():
        snapshot = pool_snapshot()
        worker_capacities = [
            dict(worker.get("capacity") or worker["available"])
            for worker in snapshot["workers"]
        ]
        oversized = [
            resources
            for resources in item_resources
            if not any(
                all(
                    resources[name] <= capacity[name]
                    for name in ("cpu_cores", "memory_mb", "gpu_count")
                )
                for capacity in worker_capacities
            )
        ]
        if oversized:
            return {
                "status": "invalid_request",
                "error": {
                    "code": "distributed_resource_limit_exceeded",
                    "message": (
                        "At least one batch item cannot fit on one compute worker."
                    ),
                    "requested": oversized[0],
                    "single_job_cross_node_execution": False,
                    "retryable": False,
                },
            }
        available = {
            "cpu_cores": int(snapshot["available_cpu_cores"]),
            "memory_mb": int(snapshot["available_memory_mb"]),
            "gpu_count": int(snapshot["available_gpu_count"]),
        }
        parallelism = len(request.items)
        capacity = {
            "pool": snapshot,
            "available_at_submission": available,
            "maximum_item_resources": maximum_item,
            "scope": "distributed_compute_pool",
        }
    else:
        budget = evaluation_resource_budget()
        reserved = active_resource_usage()
        available = {
            name: max(0, int(getattr(budget, name)) - int(reserved[name]))
            for name in ("cpu_cores", "memory_mb", "gpu_count")
        }
        capacity_limits = [
            available["cpu_cores"] // maximum_item["cpu_cores"],
            available["memory_mb"] // maximum_item["memory_mb"],
        ]
        if maximum_item["gpu_count"] > 0:
            capacity_limits.append(
                available["gpu_count"] // maximum_item["gpu_count"]
            )
        parallelism = min(len(request.items), *capacity_limits)
        capacity = {
            "budget": budget.as_dict(),
            "reserved_at_submission": reserved,
            "available_at_submission": available,
            "maximum_item_resources": maximum_item,
            "active_jobs": active_resource_jobs(),
            "scope": "local_evaluation_budget",
        }
    if request.max_concurrency is not None:
        parallelism = min(parallelism, request.max_concurrency)
    if parallelism < 1:
        return {
            "status": "invalid_request",
            "error": {
                "code": "batch_resource_capacity_unavailable",
                "message": (
                    "No batch item currently fits the remaining evaluator resource budget."
                ),
                "retryable": True,
                "retry_when": "An active job releases enough CPU, memory, and GPU capacity.",
                "resource_capacity": capacity,
            },
        }

    results: list[dict[str, Any] | None] = [None] * len(request.items)
    concurrency_lock = threading.Lock()
    active_children = 0
    peak_concurrency = 0
    batch_started = time.monotonic()

    def execute_item(index: int, item) -> dict[str, Any]:
        nonlocal active_children, peak_concurrency
        action_request = {
            "backend_id": request.backend_id,
            "component_backends": request.component_backends,
            "source_id": None,
            "inputs": item.inputs,
            "method_spec": request.method_spec,
            "action_settings": request.action_settings,
            "resource_limits": item.resource_limits.model_dump(mode="json"),
        }
        started_at = datetime.now(timezone.utc).isoformat()
        started = time.monotonic()
        with concurrency_lock:
            active_children += 1
            peak_concurrency = max(peak_concurrency, active_children)
        try:
            try:
                traced = execute_traced(
                    request.action_id,
                    {
                        "entrypoint": "submit_action_batch",
                        "batch_item_id": item.item_id,
                        "batch_index": index,
                        "request": action_request,
                    },
                    lambda: compact_action_result(
                        _execute_action(request.action_id, action_request)
                    ),
                    capture_artifacts=False,
                )
            except Exception as exc:
                traced = {
                    "status": "failed",
                    "error": {
                        "code": "batch_child_transport_error",
                        "message": f"{type(exc).__name__}: {exc}",
                        "retryable": False,
                    },
                    "retryable": False,
                }
        finally:
            with concurrency_lock:
                active_children -= 1
        return {
            "item_id": item.item_id,
            "batch_index": index,
            "resource_limits": action_request["resource_limits"],
            "started_at": started_at,
            "duration_seconds": round(time.monotonic() - started, 6),
            "result": traced,
        }

    with ThreadPoolExecutor(
        max_workers=parallelism,
        thread_name_prefix="researchchem-action-batch",
    ) as executor:
        if distributed_enabled():
            pending = [
                (index, item, item_resources[index])
                for index, item in enumerate(request.items)
            ]
            active: dict[Future, tuple[int, Any, dict[str, int]]] = {}
            while pending or active:
                launchable = _select_distributed_batch_launches(
                    pending, limit=parallelism - len(active)
                )
                for entry in launchable:
                    pending.remove(entry)
                    index, item, _resources = entry
                    active[executor.submit(execute_item, index, item)] = entry
                if not active:
                    time.sleep(0.5)
                    continue
                completed, _unfinished = wait(
                    tuple(active), timeout=0.5, return_when=FIRST_COMPLETED
                )
                for future in completed:
                    entry = active.pop(future)
                    index = entry[0]
                    record = future.result()
                    child = record.get("result") or {}
                    error_code = str((child.get("error") or {}).get("code") or "")
                    if (
                        child.get("status") == "unavailable"
                        and error_code == "distributed_resource_capacity_unavailable"
                    ):
                        pending.append(entry)
                        continue
                    results[index] = record
        else:
            futures = {
                executor.submit(execute_item, index, item): index
                for index, item in enumerate(request.items)
            }
            for future, index in futures.items():
                results[index] = future.result()

    completed_results = [item for item in results if item is not None]
    successful = sum(
        item["result"].get("status") in {"success", "partial_success"}
        for item in completed_results
    )
    return {
        "status": (
            "success"
            if successful == len(results)
            else "partial_success" if successful else "failed"
        ),
        "action_id": request.action_id,
        "backend_id": request.backend_id,
        "batch_safe": True,
        "execution_mode": "resource_aware_parallel",
        "configured_max_concurrency": request.max_concurrency,
        "effective_max_concurrency": parallelism,
        "peak_concurrency": peak_concurrency,
        "wall_duration_seconds": round(time.monotonic() - batch_started, 6),
        "resource_capacity": capacity,
        "item_count": len(completed_results),
        "successful_item_count": successful,
        "failed_item_count": len(completed_results) - successful,
        "items": completed_results,
        "automatic_fallback": False,
    }


def register_progressive_discovery_tools(mcp) -> list[str]:
    functions = {
        name: globals()[name]
        for name in PROGRESSIVE_DISCOVERY_TOOL_NAMES
    }
    for name, function in functions.items():
        mcp.tool(name=name, description=TOOL_DESCRIPTIONS[name])(function)
    return list(functions)


__all__ = [
    *PROGRESSIVE_DISCOVERY_TOOL_NAMES,
    "PROGRESSIVE_DISCOVERY_TOOL_NAMES",
    "register_progressive_discovery_tools",
]

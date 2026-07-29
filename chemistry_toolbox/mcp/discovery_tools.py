"""FastMCP bindings for progressive, task-independent catalog discovery."""

from __future__ import annotations

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
        "Inspect one exact Action before calling it. Returns its input contract, provider-selection "
        "policy, provider health and required fields; pass backend_id for that provider's complete "
        "method/resource/runtime contract."
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
        "Execute one exact predefined Scientific/Data Action selected by action_id. Supply all "
        "provider, component, source, scientific, and resource choices required by inspect_action. "
        "The dispatcher validates the request and performs no defaults, retry, or fallback. Dense "
        "results are returned as concise scalars plus a typed primary ArtifactRef; the immutable "
        "artifact contains the complete coordinates, matrices, modes, or trajectories."
    ),
    "submit_action_batch": (
        "Execute up to 32 independent requests that share one Action and backend. Only Actions "
        "whose catalog contract declares batch_safe=true are accepted. Every child is traced and "
        "returned independently; no child may depend on another child in the same batch."
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

    results = []
    for index, item in enumerate(request.items):
        action_request = {
            "backend_id": request.backend_id,
            "component_backends": request.component_backends,
            "source_id": None,
            "inputs": item.inputs,
            "method_spec": request.method_spec,
            "action_settings": request.action_settings,
            "resource_limits": item.resource_limits.model_dump(mode="json"),
        }
        traced = execute_traced(
            request.action_id,
            {
                "entrypoint": "submit_action_batch",
                "batch_item_id": item.item_id,
                "batch_index": index,
                "request": action_request,
            },
            lambda action_request=action_request: compact_action_result(
                _execute_action(request.action_id, action_request)
            ),
        )
        results.append(
            {
                "item_id": item.item_id,
                "batch_index": index,
                "resource_limits": action_request["resource_limits"],
                "result": traced,
            }
        )
    successful = sum(
        item["result"].get("status") in {"success", "partial_success"}
        for item in results
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
        "item_count": len(results),
        "successful_item_count": successful,
        "failed_item_count": len(results) - successful,
        "items": results,
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

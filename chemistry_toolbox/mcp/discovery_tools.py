"""FastMCP bindings for progressive, task-independent catalog discovery."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from pydantic import BaseModel

from researchchem_toolbox.discovery import (
    inspect_action as _inspect_action,
    inspect_backend as _inspect_backend,
    inspect_resource as _inspect_resource,
    list_action_domains as _list_action_domains,
    search_actions as _search_actions,
    search_resources as _search_resources,
)
from researchchem_toolbox.service import execute_action as _execute_action

from .discovery_models import (
    ActionDomainListRequest,
    ActionInspectRequest,
    ActionSearchRequest,
    BackendInspectRequest,
    ProgressiveActionRequest,
    ResourceInspectRequest,
    ResourceSearchRequest,
)
from .tracing import execute_traced


RequestT = TypeVar("RequestT", bound=BaseModel)


PROGRESSIVE_DISCOVERY_TOOL_NAMES = (
    "list_action_domains",
    "search_actions",
    "inspect_action",
    "inspect_backend",
    "search_resources",
    "inspect_resource",
    "execute_action",
)


TOOL_DESCRIPTIONS = {
    "list_action_domains": (
        "Return the compact complete domain index, counts, and by default every exact action_id "
        "grouped by domain. This does not select a domain or infer anything from the task."
    ),
    "search_actions": (
        "Search the complete frozen Action catalog using only the supplied query and exact filters. "
        "Results are stable id-ordered facts, not recommendations or task-specific retrieval."
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
        "The dispatcher validates the request and performs no defaults, retry, or fallback."
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

    return execute_traced(name, arguments, run)


def list_action_domains(request: ActionDomainListRequest) -> dict[str, Any]:
    return _invoke_discovery(
        "list_action_domains",
        request,
        lambda: _list_action_domains(**request.model_dump(mode="python")),
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
        lambda: _execute_action(action_id, value),
    )


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

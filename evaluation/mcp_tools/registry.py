"""Register the complete task-independent atomic Action catalog with FastMCP."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from researchchem_toolbox.catalog import (
    active_catalog_snapshot,
    action_specs,
    catalog_snapshot,
    mcp_action_description,
    validate_catalog,
)
from researchchem_toolbox.models import ActionRequest, ActionSpec
from researchchem_toolbox.service import execute_action

from .tracing import execute_traced


PACKAGE_ROOT = Path(__file__).resolve().parent
TOOL_CONFIG_PATH = PACKAGE_ROOT / "tool_config.json"


class ToolRegistryError(RuntimeError):
    """Raised when the public atomic catalog cannot be registered safely."""


@dataclass(frozen=True)
class ToolRecord:
    """Compatibility view over an ActionSpec; there are no per-task enabled flags."""

    module_stem: str
    module_name: str
    path: Path
    enabled: bool
    spec: ActionSpec
    module: None = None
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "module_stem": self.module_stem,
            "module_name": self.module_name,
            "path": str(self.path),
            "enabled": True,
            "spec": self.spec.as_dict(),
            "error": self.error,
        }


def load_tool_config() -> dict[str, Any]:
    if not TOOL_CONFIG_PATH.is_file():
        return {}
    value = json.loads(TOOL_CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Tool configuration must be a JSON object: {TOOL_CONFIG_PATH}")
    return value


def discovered_module_stems() -> list[str]:
    """Return all 44 public action ids; task/profile filtering is intentionally absent."""

    return sorted(action_specs())


def tool_is_enabled(module_stem: str, config: dict[str, Any] | None = None) -> bool:
    return module_stem in action_specs()


def configuration_errors(config: dict[str, Any] | None = None) -> list[str]:
    value = config or load_tool_config()
    errors: list[str] = []
    if value.get("exposure_policy", "atomic_all") != "atomic_all":
        errors.append("tool_config.json exposure_policy must be atomic_all")
    if value.get("backend_selection_policy", "agent_required") != "agent_required":
        errors.append("tool_config.json backend_selection_policy must be agent_required")
    if value.get("automatic_fallback", False) is not False:
        errors.append("tool_config.json automatic_fallback must be false")
    if "enabled_tools" in value or "disabled_tools" in value:
        errors.append(
            "tool_config.json cannot contain enabled_tools/disabled_tools because the "
            "benchmark exposes the complete catalog for every task"
        )
    return errors


def discover_tools(*, include_disabled: bool = True, strict: bool = False) -> list[ToolRecord]:
    del include_disabled
    errors = configuration_errors()
    try:
        validate_catalog()
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
    if strict and errors:
        raise ToolRegistryError("; ".join(errors))
    return [
        ToolRecord(
            module_stem=specification.id,
            module_name=f"researchchem_toolbox.actions.{specification.id}",
            path=PACKAGE_ROOT / "<generated-from-action-catalog>",
            enabled=True,
            spec=specification,
            error="; ".join(errors) if errors else None,
        )
        for specification in action_specs().values()
    ]


def _make_action_callable(specification: ActionSpec):
    def invoke(request: ActionRequest) -> dict[str, Any]:
        arguments = {"request": request.model_dump(mode="json")}
        return execute_traced(
            specification.id,
            arguments,
            lambda: execute_action(specification.id, request),
        )

    invoke.__name__ = specification.id
    invoke.__qualname__ = specification.id
    invoke.__doc__ = mcp_action_description(specification)
    return invoke


def register_all_tools(mcp) -> list[str]:
    """Register all 40 Scientific Actions and all 5 Data Actions, without filtering."""

    discover_tools(strict=True)
    registered = []
    for specification in action_specs().values():
        function = _make_action_callable(specification)
        mcp.tool(
            name=specification.id,
            description=mcp_action_description(specification),
        )(function)
        registered.append(specification.id)
    return registered


def register_catalog_resources(mcp) -> None:
    """Expose the same complete, read-only catalog as an MCP Resource, not a tool."""

    @mcp.resource("researchchem://catalog")
    def complete_catalog() -> str:
        return json.dumps(active_catalog_snapshot(), ensure_ascii=False, indent=2)

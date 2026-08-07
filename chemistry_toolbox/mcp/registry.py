"""Register the complete task-independent atomic Action catalog with FastMCP."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.catalog import (
    active_catalog_snapshot,
    action_specs,
    mcp_action_description,
    resolve_tool_discovery_mode,
    validate_catalog,
)
from chemistry_toolbox.src.models import ActionRequest, ActionSpec
from chemistry_toolbox.src.service import execute_action

from .tracing import execute_traced
from .discovery_tools import register_progressive_discovery_tools
from .open_tools import register_open_execution_tools
from .async_action_tools import register_async_action_tools
from .software_catalog import open_execution_prompt, software_resource_snapshot


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
    """Return every public action id; task/profile filtering is intentionally absent."""

    return sorted(action_specs())


def tool_is_enabled(module_stem: str, config: dict[str, Any] | None = None) -> bool:
    return module_stem in action_specs()


def configuration_errors(config: dict[str, Any] | None = None) -> list[str]:
    value = config or load_tool_config()
    errors: list[str] = []
    if value.get("exposure_policy", "progressive_discovery") not in {
        "progressive_discovery",
        "atomic_all",
    }:
        errors.append(
            "tool_config.json exposure_policy must be progressive_discovery or atomic_all"
        )
    if value.get("backend_selection_policy", "per_action_explicit") != "per_action_explicit":
        errors.append("tool_config.json backend_selection_policy must be per_action_explicit")
    if value.get("automatic_fallback", False) is not False:
        errors.append("tool_config.json automatic_fallback must be false")
    if value.get("open_execution_policy") != "agent_explicit":
        errors.append("tool_config.json open_execution_policy must be agent_explicit")
    if value.get("execution_layers") != [
        "predefined_actions",
        "native_software",
        "programmable_analysis",
    ]:
        errors.append("tool_config.json must declare the three execution layers in order")
    if value.get("native_shell") is not False or value.get("programmable_shell") is not False:
        errors.append("tool_config.json native_shell and programmable_shell must be false")
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
            module_name=f"chemistry_toolbox.src.actions.{specification.id}",
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
    """Register the historical one-MCP-tool-per-Action compatibility surface."""

    discover_tools(strict=True)
    registered = []
    for specification in action_specs().values():
        function = _make_action_callable(specification)
        mcp.tool(
            name=specification.id,
            description=mcp_action_description(specification),
        )(function)
        registered.append(specification.id)
    registered.extend(register_open_execution_tools(mcp))
    registered.extend(register_async_action_tools(mcp))
    return registered


def register_progressive_tools(mcp) -> list[str]:
    """Register compact discovery/dispatch plus native/program primitives."""

    discover_tools(strict=True)
    registered = register_progressive_discovery_tools(mcp)
    registered.extend(register_open_execution_tools(mcp))
    registered.extend(register_async_action_tools(mcp))
    return registered


def register_public_tools(mcp, discovery_mode: str | None = None) -> list[str]:
    """Register the selected transport surface over the same complete catalog."""

    mode = resolve_tool_discovery_mode(discovery_mode)
    return register_all_tools(mcp) if mode == "full" else register_progressive_tools(mcp)


def register_catalog_resources(mcp, discovery_mode: str | None = None) -> None:
    """Expose complete read-only Action and open-execution catalogs."""

    mode = resolve_tool_discovery_mode(discovery_mode)

    @mcp.resource("researchchem://catalog")
    def complete_catalog() -> str:
        return json.dumps(active_catalog_snapshot(), ensure_ascii=False, indent=2)

    @mcp.resource("researchchem://software")
    def complete_software_inventory() -> str:
        return json.dumps(software_resource_snapshot(), ensure_ascii=False, indent=2)

    @mcp.resource("researchchem://execution-policy")
    def execution_policy() -> str:
        return open_execution_prompt(include_command_index=mode == "full")

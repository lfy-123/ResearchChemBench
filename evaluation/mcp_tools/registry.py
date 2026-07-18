"""Automatic discovery, validation, filtering, and registration of tool files."""

from __future__ import annotations

import importlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from .models import ToolSpec


PACKAGE_ROOT = Path(__file__).resolve().parent
TOOLS_DIR = PACKAGE_ROOT / "tools"
TOOL_CONFIG_PATH = PACKAGE_ROOT / "tool_config.json"
ENABLED_TOOLS_ENV = "RESEARCHCHEM_MCP_ENABLED_TOOLS"
DISABLED_TOOLS_ENV = "RESEARCHCHEM_MCP_DISABLED_TOOLS"


class ToolRegistryError(RuntimeError):
    """Raised when enabled tool modules cannot be safely registered."""


class _SingleToolRegistrationProxy:
    """Delegate to FastMCP while enforcing one matching registration per file."""

    def __init__(self, mcp: Any, expected_name: str) -> None:
        self._mcp = mcp
        self._expected_name = expected_name
        self._registered_names: list[str] = []

    def __getattr__(self, name: str) -> Any:
        return getattr(self._mcp, name)

    def _record(self, function: Any, explicit_name: str | None) -> None:
        registered_name = explicit_name or getattr(function, "__name__", "")
        if registered_name != self._expected_name:
            raise ToolRegistryError(
                f"Tool file {self._expected_name!r} tried to register "
                f"{registered_name!r}; the registered name must match TOOL_SPEC.name"
            )
        if self._registered_names:
            raise ToolRegistryError(
                f"Tool file {self._expected_name!r} tried to register more than "
                "one public MCP tool"
            )
        self._registered_names.append(registered_name)

    def tool(self, *args: Any, **kwargs: Any) -> Any:
        explicit_name = kwargs.get("name")
        if explicit_name is None and args and isinstance(args[0], str):
            explicit_name = args[0]

        # Support both @mcp.tool and @mcp.tool(...).
        if args and callable(args[0]):
            function = args[0]
            self._record(function, explicit_name)
            return self._mcp.tool(*args, **kwargs)

        decorator = self._mcp.tool(*args, **kwargs)

        def guarded_decorator(function: Any) -> Any:
            self._record(function, explicit_name)
            return decorator(function)

        return guarded_decorator

    def ensure_complete(self) -> None:
        if self._registered_names != [self._expected_name]:
            raise ToolRegistryError(
                f"Tool file {self._expected_name!r} must register exactly one "
                "public MCP tool"
            )


@dataclass
class ToolRecord:
    module_stem: str
    module_name: str
    path: Path
    enabled: bool
    spec: ToolSpec | None = None
    module: ModuleType | None = None
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "module_stem": self.module_stem,
            "module_name": self.module_name,
            "path": str(self.path),
            "enabled": self.enabled,
            "spec": self.spec.as_dict() if self.spec else None,
            "error": self.error,
        }


def load_tool_config() -> dict[str, Any]:
    value = json.loads(TOOL_CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Tool configuration must be a JSON object: {TOOL_CONFIG_PATH}")
    enabled = value.get("enabled_tools", ["*"])
    disabled = value.get("disabled_tools", [])
    if not isinstance(enabled, list) or not all(isinstance(item, str) for item in enabled):
        raise ValueError("tool_config.json enabled_tools must be a list of strings")
    if not isinstance(disabled, list) or not all(isinstance(item, str) for item in disabled):
        raise ValueError("tool_config.json disabled_tools must be a list of strings")
    return value


def _environment_names(name: str) -> set[str]:
    return {
        item.strip()
        for item in os.environ.get(name, "").split(",")
        if item.strip()
    }


def discovered_module_stems() -> list[str]:
    """Return tool filenames; adding/deleting a file changes this list automatically."""

    return sorted(
        path.stem
        for path in TOOLS_DIR.glob("*.py")
        if path.name != "__init__.py" and not path.name.startswith("_")
    )


def tool_is_enabled(module_stem: str, config: dict[str, Any] | None = None) -> bool:
    config = config or load_tool_config()
    enabled = _environment_names(ENABLED_TOOLS_ENV) or set(
        config.get("enabled_tools", ["*"])
    )
    disabled = set(config.get("disabled_tools", [])) | _environment_names(
        DISABLED_TOOLS_ENV
    )
    return (
        ("*" in enabled or module_stem in enabled)
        and "*" not in disabled
        and module_stem not in disabled
    )


def configuration_errors(config: dict[str, Any] | None = None) -> list[str]:
    config = config or load_tool_config()
    discovered = set(discovered_module_stems())
    errors: list[str] = []
    configured: set[str] = set()
    for field_name in ("enabled_tools", "disabled_tools"):
        names = config.get(field_name, [])
        if len(names) != len(set(names)):
            errors.append(f"tool_config.json {field_name} contains duplicate names")
        configured.update(names)

    for name in sorted(configured - discovered - {"*"}):
        errors.append(f"tool_config.json references missing tool file: {name}")

    environment_names = {
        ENABLED_TOOLS_ENV: _environment_names(ENABLED_TOOLS_ENV),
        DISABLED_TOOLS_ENV: _environment_names(DISABLED_TOOLS_ENV),
    }
    for variable, names in environment_names.items():
        for name in sorted(names - discovered - {"*"}):
            errors.append(f"{variable} references missing tool file: {name}")
    return errors


def discover_tools(
    *,
    include_disabled: bool = True,
    strict: bool = False,
) -> list[ToolRecord]:
    """Import tool files, validate ToolSpec/register, and report errors per file."""

    config = load_tool_config()
    records: list[ToolRecord] = []
    seen_names: dict[str, str] = {}
    for stem in discovered_module_stems():
        enabled = tool_is_enabled(stem, config)
        if not include_disabled and not enabled:
            continue
        module_name = f"{__package__}.tools.{stem}"
        record = ToolRecord(
            module_stem=stem,
            module_name=module_name,
            path=TOOLS_DIR / f"{stem}.py",
            enabled=enabled,
        )
        try:
            module = importlib.import_module(module_name)
            spec = getattr(module, "TOOL_SPEC", None)
            if not isinstance(spec, ToolSpec):
                raise TypeError("module must define TOOL_SPEC = ToolSpec(...)")
            spec.validate()
            if spec.name != stem:
                raise ValueError(
                    f"TOOL_SPEC.name {spec.name!r} must match filename {stem!r}"
                )
            register = getattr(module, "register", None)
            if not callable(register):
                raise TypeError("module must define callable register(mcp)")
            previous = seen_names.get(spec.name)
            if previous:
                raise ValueError(
                    f"duplicate tool name {spec.name!r} also defined by {previous}"
                )
            seen_names[spec.name] = module_name
            record.module = module
            record.spec = spec
        except Exception as exc:
            record.error = f"{type(exc).__name__}: {exc}"
        records.append(record)

    errors = [record for record in records if record.enabled and record.error]
    config_errors = configuration_errors(config)
    if strict and errors:
        details = "; ".join(
            f"{record.module_stem}: {record.error}" for record in errors
        )
        raise ToolRegistryError(f"Enabled MCP tool modules are invalid: {details}")
    if strict and config_errors:
        raise ToolRegistryError("; ".join(config_errors))
    return records


def register_all_tools(mcp) -> list[str]:
    """Register every enabled, automatically discovered one-file tool module."""

    records = discover_tools(include_disabled=False, strict=True)
    registered: list[str] = []
    for record in records:
        assert record.module is not None and record.spec is not None
        proxy = _SingleToolRegistrationProxy(mcp, record.spec.name)
        try:
            record.module.register(proxy)
            proxy.ensure_complete()
        except Exception as exc:
            if isinstance(exc, ToolRegistryError):
                raise
            raise ToolRegistryError(
                f"Failed to register MCP tool {record.spec.name!r}: "
                f"{type(exc).__name__}: {exc}"
            ) from exc
        registered.append(record.spec.name)
    return registered

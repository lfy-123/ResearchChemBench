"""Shared metadata contract for self-describing MCP tool modules."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass


_TOOL_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_SEQUENCE_FIELDS = (
    "dependencies",
    "tags",
    "executables",
    "side_effects",
    "aliases",
)


@dataclass(frozen=True)
class ToolSpec:
    """Metadata owned by one tool file rather than a central catalog."""

    name: str
    description: str
    category: str
    version: str = "1.0.0"
    backend: str = ""
    dependencies: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    requires_network: bool = False
    executables: tuple[str, ...] = ()
    side_effects: tuple[str, ...] = ()
    deprecated: bool = False
    aliases: tuple[str, ...] = ()

    def validate(self) -> None:
        if not isinstance(self.name, str) or not _TOOL_NAME_PATTERN.fullmatch(self.name):
            raise ValueError(
                f"Tool name must be lower snake_case and start with a letter: {self.name!r}"
            )
        for field_name in ("description", "category", "version", "backend"):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise ValueError(
                    f"Tool {self.name!r} field {field_name!r} must be a string"
                )
            if field_name != "backend" and not value.strip():
                raise ValueError(
                    f"Tool {self.name!r} has an empty {field_name}"
                )

        for field_name in _SEQUENCE_FIELDS:
            values = getattr(self, field_name)
            if not isinstance(values, tuple):
                raise ValueError(
                    f"Tool {self.name!r} field {field_name!r} must be a tuple"
                )
            if not all(isinstance(value, str) and value.strip() for value in values):
                raise ValueError(
                    f"Tool {self.name!r} field {field_name!r} must contain "
                    "non-empty strings"
                )
            if len(values) != len(set(values)):
                raise ValueError(
                    f"Tool {self.name!r} field {field_name!r} contains duplicates"
                )

        for alias in self.aliases:
            if not _TOOL_NAME_PATTERN.fullmatch(alias):
                raise ValueError(
                    f"Tool alias must use lower snake_case: {alias!r}"
                )
            if alias == self.name:
                raise ValueError(
                    f"Tool {self.name!r} must not repeat its own name as an alias"
                )

        for field_name in ("requires_network", "deprecated"):
            if not isinstance(getattr(self, field_name), bool):
                raise ValueError(
                    f"Tool {self.name!r} field {field_name!r} must be boolean"
                )

    def as_dict(self) -> dict:
        value = asdict(self)
        value["dependencies"] = list(self.dependencies)
        value["tags"] = list(self.tags)
        value["executables"] = list(self.executables)
        value["side_effects"] = list(self.side_effects)
        value["aliases"] = list(self.aliases)
        return value

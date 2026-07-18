"""Workspace confinement helpers shared by every portable chemistry tool."""

from __future__ import annotations

import os
from pathlib import Path


WORKSPACE_ENV_NAMES = (
    "RESEARCHCHEM_MCP_WORKSPACE",
    "RESEARCHCHEMBENCH_WORKSPACE",
)
OUTPUT_ROOTS = ("outputs", "code", "report", "tool_logs")
RESERVED_FILES = {
    "_agent_output.jsonl",
    "_meta.json",
    "_score.json",
    "_tool_trace.jsonl",
    "_tool_sequence",
    "INSTRUCTIONS.md",
    ".mcp.json",
    "opencode.json",
}


def workspace_root() -> Path:
    """Return an explicit workspace or use the MCP process working directory."""

    configured = next(
        (
            os.environ[name].strip()
            for name in WORKSPACE_ENV_NAMES
            if os.environ.get(name, "").strip()
        ),
        "",
    )
    root = Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()
    if not root.is_dir():
        raise RuntimeError(f"Chemistry MCP workspace does not exist: {root}")
    return root


def resolve_workspace_path(
    value: str,
    *,
    must_exist: bool = False,
    create_parent: bool = False,
) -> Path:
    """Resolve a tool path while rejecting traversal outside the workspace."""

    root = workspace_root()
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    unchecked = candidate.absolute()
    try:
        relative_unchecked = unchecked.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes chemistry MCP workspace: {value}") from exc
    cursor = root
    for part in relative_unchecked.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"Symlink paths are not allowed in chemistry workspace: {value}")
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes chemistry MCP workspace: {value}") from exc

    if must_exist and not resolved.exists():
        raise FileNotFoundError(f"Workspace file does not exist: {resolved}")
    if create_parent:
        resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def resolve_workspace_output_path(
    value: str,
    *,
    allowed_roots: tuple[str, ...] = OUTPUT_ROOTS,
) -> Path:
    """Resolve a writable path while protecting inputs and benchmark control files."""

    resolved = resolve_workspace_path(value, create_parent=False)
    root = workspace_root()
    relative = resolved.relative_to(root)
    if not relative.parts or relative.parts[0] not in allowed_roots:
        raise ValueError(
            f"Tool outputs must be under one of {allowed_roots}, received: {value}"
        )
    if relative.name in RESERVED_FILES or relative.parts[0].startswith("_tool_"):
        raise ValueError(f"Tool output path is reserved: {value}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def relative_workspace_path(path: str | Path) -> str:
    """Represent a path relative to the active chemistry workspace."""

    resolved = Path(path).resolve(strict=False)
    return str(resolved.relative_to(workspace_root()))

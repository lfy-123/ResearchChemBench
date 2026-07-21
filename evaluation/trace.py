"""Read and normalize benchmark Chemistry MCP trace events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SUCCESSFUL_TOOL_STATUSES = {"success", "partial_success"}


def load_tool_trace(workspace: Path) -> list[dict[str, Any]]:
    path = workspace / "_tool_trace.jsonl"
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def normalized_tool_calls(events: list[dict[str, Any]], *, successful_only: bool = True) -> list[dict]:
    calls: list[dict] = []
    for event in events:
        if successful_only and event.get("status") not in SUCCESSFUL_TOOL_STATUSES:
            continue
        name = event.get("tool")
        arguments = event.get("arguments", {})
        if name:
            calls.append({str(name): arguments if isinstance(arguments, dict) else {}})
    return calls


def process_metrics(events: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "tool_call_count": len(events),
        "successful_tool_calls": sum(
            event.get("status") in SUCCESSFUL_TOOL_STATUSES for event in events
        ),
        "failed_tool_calls": sum(
            event.get("status") not in SUCCESSFUL_TOOL_STATUSES for event in events
        ),
        "tool_runtime_seconds": round(
            sum(float(event.get("duration_seconds", 0) or 0) for event in events), 6
        ),
        "tools_used": [event.get("tool") for event in events],
    }

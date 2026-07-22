"""Read and normalize benchmark Chemistry MCP trace events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from researchchem_toolbox.catalog import action_specs


SUCCESSFUL_TOOL_STATUSES = {"success", "partial_success"}
CATALOG_DISCOVERY_TOOLS = {
    "list_action_domains",
    "search_actions",
    "inspect_action",
    "inspect_backend",
    "search_resources",
    "inspect_resource",
}


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


def load_native_agent_trace(workspace: Path) -> list[dict[str, Any]]:
    """Load native tool events from primary and child Agent sessions.

    ``_agent_output.jsonl`` contains the primary OpenCode stream. The
    event-sourced ``_model_io.jsonl`` additionally contains child/subagent
    sessions. Merge both sources and deduplicate their shared primary events by
    OpenCode call ID.
    """

    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    model_io_path = workspace / "_model_io.jsonl"
    if model_io_path.is_file():
        for line in model_io_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict) or record.get("record_type") != "model_step":
                continue
            output = record.get("output") if isinstance(record.get("output"), dict) else {}
            parts = output.get("parts") if isinstance(output.get("parts"), list) else []
            for part in parts:
                if isinstance(part, dict) and part.get("type") == "tool":
                    candidates.append(
                        (
                            part,
                            {
                                "source": "model_io",
                                "session_id": record.get("session_id"),
                                "session_step_index": record.get("session_step_index"),
                                "message_id": record.get("message_id"),
                            },
                        )
                    )

    output_path = workspace / "_agent_output.jsonl"
    if output_path.is_file():
        for line in output_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(value, dict) or value.get("type") != "tool_use":
                continue
            part = value.get("part")
            if isinstance(part, dict) and part.get("type") == "tool":
                candidates.append(
                    (
                        part,
                        {
                            "source": "agent_output",
                            "session_id": value.get("sessionID") or part.get("sessionID"),
                            "session_step_index": None,
                            "message_id": value.get("messageID") or part.get("messageID"),
                        },
                    )
                )

    events: list[dict[str, Any]] = []
    seen_call_ids: set[str] = set()
    for part, trace_context in candidates:
        tool = str(part.get("tool") or "")
        if not tool or tool.startswith("researchchem_toolbox_"):
            # Chemistry MCP has a separate authoritative trace with validated
            # scientific status and artifact provenance.
            continue
        call_id = str(part.get("callID") or "")
        if call_id and call_id in seen_call_ids:
            continue
        if call_id:
            seen_call_ids.add(call_id)
        state = part.get("state") if isinstance(part.get("state"), dict) else {}
        metadata = (
            state.get("metadata") if isinstance(state.get("metadata"), dict) else {}
        )
        exit_code = metadata.get("exit")
        status = str(state.get("status") or "unknown")
        if (
            tool == "invalid"
            or exit_code not in {None, 0}
            or status in {"error", "failed"}
        ):
            normalized_status = "failed"
        elif status == "completed":
            normalized_status = "success"
        else:
            normalized_status = status
        timing = state.get("time") if isinstance(state.get("time"), dict) else {}
        start = timing.get("start")
        end = timing.get("end")
        duration = 0.0
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            duration = max(0.0, (float(end) - float(start)) / 1000.0)
        output = state.get("output")
        if output is None:
            output = metadata.get("output")
        event: dict[str, Any] = {
            "sequence": len(events) + 1,
            "tool": tool,
            "status": normalized_status,
            "duration_seconds": round(duration, 6),
            "arguments": state.get("input") if isinstance(state.get("input"), dict) else {},
            "result_preview": output,
            "exit_code": exit_code,
            "call_id": call_id or None,
            **trace_context,
        }
        if normalized_status == "failed":
            event["error"] = {
                "exit_code": exit_code,
                "message": str(output or state.get("error") or "native tool failed"),
            }
        events.append(event)
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
    action_ids = set(action_specs())
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
        "catalog_discovery_call_count": sum(
            event.get("tool") in CATALOG_DISCOVERY_TOOLS for event in events
        ),
        "predefined_action_call_count": sum(
            event.get("tool") in action_ids for event in events
        ),
        "open_execution_call_count": sum(
            event.get("tool") not in CATALOG_DISCOVERY_TOOLS
            and event.get("tool") not in action_ids
            for event in events
        ),
    }

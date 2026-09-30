"""Provider event normalization shared by progress, audit and scoring readers."""
from __future__ import annotations

import json
from pathlib import Path

EVENT_VERSION = "agent-events-1"


def normalize_agent_event(event):
    """Keep the raw record at its source; normalize only observable fields."""
    if not isinstance(event, dict):
        return {"provider": "unknown", "kind": "unparsed", "raw": event}
    from ..agent_plugins.protocol import normalize_external_event
    external = normalize_external_event(event)
    if external is not None:
        return external
    typ = str(event.get("type") or "")
    part = event.get("part") if isinstance(event.get("part"), dict) else {}
    item = event.get("item") if isinstance(event.get("item"), dict) else {}
    value = {"provider": "unknown", "kind": "unparsed", "raw": event,
             "session_id": event.get("sessionID") or event.get("thread_id"),
             "phase": None, "call_id": None, "status": "unknown"}
    if typ.startswith(("thread.", "turn.", "item.")):
        value["provider"] = "codex"
        value["phase"] = typ.rsplit(".", 1)[-1]
        if typ == "thread.started":
            value["kind"] = "session"
        elif typ.startswith("turn."):
            value.update(kind="turn", usage=event.get("usage"), error=event.get("error"))
        elif isinstance(item, dict):
            kind = str(item.get("type") or "")
            value.update(call_id=item.get("id"), status=str(item.get("status") or "unknown"))
            if kind == "command_execution":
                value.update(kind="native_tool", tool="shell", arguments={"command": item.get("command")},
                             result_preview=item.get("aggregated_output"), exit_code=item.get("exit_code"))
            elif kind == "file_change":
                value.update(kind="native_tool", tool="file_change", arguments={"changes": item.get("changes")})
            elif kind == "mcp_tool_call":
                value.update(kind="mcp_tool", tool=item.get("tool"), server=item.get("server"),
                             arguments=item.get("arguments"), result_preview=item.get("result"), error=item.get("error"))
            elif kind in {"agent_message", "reasoning"}:
                value.update(kind="message" if kind == "agent_message" else "reasoning", text=item.get("text"))
    elif typ in {"tool_use", "step_start", "step_finish", "text", "reasoning"}:
        value["provider"] = "opencode"
        value["session_id"] = event.get("sessionID") or part.get("sessionID")
        value["message_id"] = event.get("messageID") or part.get("messageID")
        if typ == "tool_use":
            state = part.get("state") if isinstance(part.get("state"), dict) else {}
            metadata = state.get("metadata") if isinstance(state.get("metadata"), dict) else {}
            tool = str(part.get("tool", "unknown"))
            status = str(state.get("status") or "unknown")
            value.update(kind="mcp_tool" if tool.startswith("researchchem_toolbox_") else "native_tool",
                         tool=tool, call_id=part.get("callID"), status=status,
                         phase="completed" if status in {"completed", "error", "failed"} else "started",
                         arguments=state.get("input") or {}, result_preview=state.get("output", metadata.get("output")),
                         exit_code=metadata.get("exit"), error=state.get("error"))
            timing = state.get("time") if isinstance(state.get("time"), dict) else {}
            if all(isinstance(timing.get(k), (int, float)) for k in ("start", "end")):
                value["duration_seconds"] = max(0, (timing["end"] - timing["start"]) / 1000)
        elif typ in {"step_start", "step_finish"}:
            value.update(kind="turn", phase="started" if typ == "step_start" else "completed", usage=part.get("tokens"))
        else:
            value.update(kind="message" if typ == "text" else "reasoning", text=part.get("text"))
    elif typ == "assistant":
        message = event.get("message") if isinstance(event.get("message"), dict) else {}
        value.update(provider="claude", kind="message", text=event.get("content") or message.get("content"))
    elif typ == "result":
        value.update(kind="result", result_preview=event)
    elif typ in {"error", "session_error"}:
        value.update(kind="error", error=event.get("error") or event)
    if value.get("exit_code") not in (None, 0) or value.get("status") in {"failed", "error"} or value.get("tool") == "invalid":
        value["status"] = "failed"
    elif value.get("status") == "completed":
        value["status"] = "success"
    if not isinstance(value.get("call_id"), str):
        value["call_id"] = None
    if not isinstance(value.get("session_id"), str):
        value["session_id"] = None
    return value


def _records(path):
    if path.is_file():
        with path.open(encoding="utf-8", errors="replace") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    record = line.rstrip()
                yield line_number, record


def load_agent_events(workspace):
    workspace = Path(workspace)
    portable = workspace / "_agent_events.jsonl"
    if portable.is_file():
        return [record for _, record in _records(portable) if isinstance(record, dict)]
    meta = {}
    try:
        meta = json.loads((workspace / "_meta.json").read_text())
    except (OSError, ValueError):
        pass
    if isinstance(meta, dict) and meta.get("agent_kind") == "external":
        from ..agent_plugins.protocol import normalize_external_event
        values, seen = [], {}
        for number, raw in _records(workspace / "_agent_output.jsonl"):
            event = normalize_external_event(raw, run_id=meta.get("run_id"))
            if event is None:
                event = {"provider": "external", "kind": "unparsed", "raw": raw, "status": "unknown"}
            else:
                identity = (event["agent_id"], event.get("session_id"), event["event_id"])
                if identity in seen and seen[identity] == raw:
                    continue
                # Preserve conflicting repeats for the usage validator and audit.
                seen[identity] = raw
            values.append({**event, "source": "agent_output", "source_ref": "workspace/_agent_output.jsonl",
                           "line_number": number, "sequence": len(values) + 1,
                           "identity_confidence": "agent_reported"})
        return values
    candidates = []
    for number, record in _records(workspace / "_model_io.jsonl"):
        if not isinstance(record, dict) or record.get("record_type") != "model_step":
            continue
        output = record.get("output") if isinstance(record.get("output"), dict) else {}
        parts = output.get("parts") if isinstance(output.get("parts"), list) else []
        for part in parts:
            if isinstance(part, dict) and part.get("type") == "tool":
                value = normalize_agent_event({"type": "tool_use", "part": part, "sessionID": record.get("session_id")})
                candidates.append({**value, "source": "model_io", "source_ref": "workspace/_model_io.jsonl",
                                   "line_number": number, "session_step_index": record.get("session_step_index")})
    session, invocation, turn = None, 0, 0
    for number, record in _records(workspace / "_agent_output.jsonl"):
        value = normalize_agent_event(record)
        if value["kind"] == "session":
            session, invocation, turn = value.get("session_id"), invocation + 1, 0
        if value["kind"] == "turn" and value["phase"] == "started":
            turn += 1
        value.update(source="agent_output", source_ref="workspace/_agent_output.jsonl", line_number=number,
                     session_id=value.get("session_id") or session, observed_attempt=invocation or None,
                     session_step_index=turn or None)
        candidates.append(value)
    events, identities = [], {}
    for value in candidates:
        identity = None
        if (value.get("call_id") and value["kind"] in {"native_tool", "mcp_tool"}
                and (value.get("session_id") or value.get("observed_attempt"))):
            # Codex item_N is local to an invocation/turn, unlike OpenCode callID.
            scope = (value.get("observed_attempt"), value.get("session_step_index")) if value["provider"] == "codex" else ()
            identity = (value["provider"], value.get("session_id"), scope, value["call_id"])
        if identity in identities:
            position = identities[identity]
            if events[position].get("phase") != "completed" and value.get("phase") == "completed":
                events[position] = value
            continue
        if identity is not None:
            identities[identity] = len(events)
        value["identity_confidence"] = "provider_scoped" if identity else "observation_only"
        events.append(value)
    return [{**e, "sequence": n} for n, e in enumerate(events, 1)]


def event_capture_summary(events):
    unknown = sum(e["kind"] == "unparsed" for e in events)
    return {"parser_version": EVENT_VERSION, "observed_event_count": len(events),
            "unparsed_event_count": unknown, "capture_status": "partial" if unknown else "observed" if events else "unavailable",
            "model_api_request_count": None,
            "completed_turn_count": sum(e["kind"] == "turn" and e.get("phase") == "completed" for e in events),
            "completed_native_call_count": sum(e["kind"] == "native_tool" and e.get("phase") == "completed" for e in events)}

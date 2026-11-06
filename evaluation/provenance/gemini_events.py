"""Gemini stream-json events, explicitly selected to avoid OpenCode collisions."""


def normalize_gemini_event(event):
    typ = event.get("type")
    value = {"provider": "gemini", "kind": "unparsed", "raw": event,
             "session_id": event.get("session_id"), "phase": None, "call_id": None, "status": "unknown"}
    if typ == "init":
        value.update(kind="session", model=event.get("model"), phase="started")
    elif typ == "message":
        value.update(kind="message", text=event.get("content"), role=event.get("role"))
    elif typ in {"tool_use", "tool_result"}:
        name = event.get("tool_name") or "unknown"
        value.update(kind="mcp_tool" if event.get("_rcb_mcp") or name.startswith(("mcp_", "researchchem_toolbox_", "chemistry_wait_")) else "native_tool",
                     tool=name, call_id=event.get("tool_id"), arguments=event.get("parameters"),
                     phase="started" if typ == "tool_use" else "completed", result_preview=event.get("output"),
                     error=event.get("error"), status="failed" if event.get("status") == "error" else event.get("status", "running"))
    elif typ == "result":
        value.update(kind="turn", phase="completed" if event.get("status") == "success" else "failed",
                     status="success" if event.get("status") == "success" else "failed", error=event.get("error"), usage=event.get("stats"))
    elif typ == "error":
        value.update(kind="error", error=event, severity=event.get("severity"))
    return value

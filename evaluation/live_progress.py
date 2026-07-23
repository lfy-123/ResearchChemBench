"""Bounded, redacted live progress lines for Agent and Chemistry MCP runs."""

from __future__ import annotations

import json
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

from .model_io import redact_trace_value


MIN_PROGRESS_CHARS = 80
DEFAULT_PROGRESS_FILENAME = "_live_progress.log"


def _one_line(value: Any, *, max_chars: int) -> str:
    redacted = redact_trace_value(value)
    if isinstance(redacted, str):
        text = redacted
    else:
        text = json.dumps(redacted, ensure_ascii=False, sort_keys=True, default=str)
    text = " ".join(text.replace("\x00", "").split())
    if len(text) <= max_chars:
        return text
    omitted = len(text) - max_chars
    suffix = f"…<truncated {omitted} chars>"
    keep = max(1, max_chars - len(suffix))
    return text[:keep] + suffix


def progress_timestamp() -> str:
    """Return a sortable UTC timestamp for every human-readable log line."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


class LiveProgressReporter:
    """Write progress to a run-local file and optionally mirror it to stdout."""

    def __init__(
        self,
        workspace: Path,
        run_id: str,
        *,
        enabled: bool = True,
        console: bool = False,
        max_chars: int = 600,
        stream: TextIO | None = None,
    ):
        self.workspace = Path(workspace)
        self.run_id = run_id
        self.enabled = bool(enabled)
        self.console = bool(console)
        self.max_chars = max(MIN_PROGRESS_CHARS, int(max_chars))
        self.stream = stream if stream is not None else sys.stdout
        self.path = self.workspace / DEFAULT_PROGRESS_FILENAME
        self._handle: TextIO | None = None
        self._lock = threading.Lock()
        self._file_failed = False

    def _ensure_handle(self) -> TextIO:
        if self._handle is None:
            self.workspace.mkdir(parents=True, exist_ok=True)
            self._handle = self.path.open("a", encoding="utf-8")
        return self._handle

    def emit(self, kind: str, **fields: Any) -> None:
        if not self.enabled:
            return
        timestamp = progress_timestamp()
        redacted_fields = redact_trace_value(fields)
        parts = [
            f"{key}={_one_line(value, max_chars=self.max_chars)}"
            for key, value in redacted_fields.items()
            if value is not None and value != ""
        ]
        line = f"[RCB][{timestamp}][{self.run_id}][{kind}]"
        if parts:
            line += " " + " ".join(parts)
        with self._lock:
            if self.console:
                try:
                    print(line, file=self.stream, flush=True)
                except (OSError, ValueError):
                    self.console = False
            if not self._file_failed:
                try:
                    handle = self._ensure_handle()
                    handle.write(line + "\n")
                    handle.flush()
                except (OSError, ValueError):
                    self._file_failed = True
                    if self._handle is not None:
                        try:
                            self._handle.close()
                        except OSError:
                            pass
                        self._handle = None

    def handle_agent_line(self, line: str) -> None:
        """Summarize one OpenCode/Agent JSON stream event."""

        if not self.enabled:
            return
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            self.emit("AGENT_STREAM", text=line)
            return
        if not isinstance(event, dict):
            self.emit("AGENT_STREAM", value=event)
            return

        event_type = str(event.get("type") or "")
        part = event.get("part") if isinstance(event.get("part"), dict) else {}
        if event_type == "step_start":
            self.emit(
                "MODEL_STEP_START",
                session_id=event.get("sessionID") or part.get("sessionID"),
                message_id=part.get("messageID"),
            )
            return
        if event_type == "text":
            self.emit("MODEL_OUTPUT", text=part.get("text", ""))
            return
        if event_type == "assistant":
            message = event.get("message") if isinstance(event.get("message"), dict) else {}
            self.emit(
                "MODEL_OUTPUT",
                text=event.get("content") or message.get("content") or part.get("text") or "",
            )
            return
        if event_type == "reasoning":
            self.emit(
                "MODEL_REASONING",
                text=part.get("text") or part.get("reasoning") or "",
            )
            return
        if event_type == "tool_use":
            state = part.get("state") if isinstance(part.get("state"), dict) else {}
            tool = str(part.get("tool") or "unknown")
            kind = "MCP_AGENT_EVENT" if "researchchem" in tool else "NATIVE_TOOL"
            self.emit(
                kind,
                tool=tool,
                call_id=part.get("callID"),
                status=state.get("status"),
                input=state.get("input"),
                output=state.get("output"),
                error=state.get("error"),
            )
            return
        if event_type == "step_finish":
            self.emit(
                "MODEL_STEP",
                session_id=event.get("sessionID") or part.get("sessionID"),
                message_id=part.get("messageID"),
                reason=part.get("reason"),
                tokens=part.get("tokens"),
                cost=part.get("cost"),
            )
            return
        if event_type in {"error", "session_error"}:
            self.emit("AGENT_ERROR", error=event.get("error") or part or event)
            return
        if event_type == "result":
            self.emit("AGENT_RESULT", result=event)

    def handle_tool_trace_line(self, line: str) -> None:
        """Summarize one completed Chemistry MCP trace event."""

        if not self.enabled:
            return
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            self.emit("MCP_TRACE_PARSE_ERROR", text=line)
            return
        if not isinstance(event, dict):
            return
        arguments = event.get("arguments")
        request = (
            arguments.get("request")
            if isinstance(arguments, dict) and isinstance(arguments.get("request"), dict)
            else arguments
        )
        backend = None
        if isinstance(request, dict):
            backend = (
                request.get("backend_id")
                or request.get("runtime_id")
                or request.get("component_backends")
            )
        common = {
            "seq": event.get("sequence"),
            "tool": event.get("tool"),
        }
        self.emit(
            "MCP_CALL",
            **common,
            backend=backend,
            request=request,
        )
        self.emit(
            "MCP_RESULT",
            **common,
            status=event.get("status"),
            seconds=event.get("duration_seconds"),
            result=event.get("result_preview"),
            error=event.get("error"),
            artifacts=event.get("artifacts"),
        )

    def close(self) -> None:
        with self._lock:
            if self._handle is not None:
                try:
                    self._handle.close()
                except OSError:
                    pass
                self._handle = None


def append_progress_event(
    workspace: Path,
    run_id: str,
    kind: str,
    *,
    enabled: bool,
    console: bool = False,
    max_chars: int,
    **fields: Any,
) -> None:
    """Append one event outside the main Agent process, such as judge I/O."""

    reporter = LiveProgressReporter(
        workspace,
        run_id,
        enabled=enabled,
        console=console,
        max_chars=max_chars,
    )
    try:
        reporter.emit(kind, **fields)
    finally:
        reporter.close()

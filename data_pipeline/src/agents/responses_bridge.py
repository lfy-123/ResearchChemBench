"""A loopback Responses API facade for OpenAI-compatible chat endpoints.

Codex CLI speaks the Responses wire protocol. Several configured scientific
models expose only ``/chat/completions``. This module translates the small,
tool-capable subset used by the Stage06/07 construction Agents. The upstream
credential remains in this process and is never passed to the Agent child.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import tempfile
import threading
import time
import uuid
from contextlib import AbstractContextManager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable

import httpx
import jsonschema
from json_repair import repair_json

_TEXTUAL_TOOL_PROTOCOL_RE = re.compile(
    r"(?:<[^>]*(?:DSML|tool[_ -]?call|invoke)[^>]*>|"
    r"(?:recipient|to)\s*=\s*(?:functions\.|tools\.)|"
    r"<\|(?:assistant to=)?(?:functions\.|tools\.))",
    flags=re.IGNORECASE,
)
_FINAL_JSON_TOOL = "submit_final_json"
_FINAL_SCHEMA_PROMPT_PREFIX = "After completing all required workspace tool work"
_DSML_INVOKE_RE = re.compile(
    r"<(?!/)[^<>]*DSML[^<>]*invoke\b(?P<attributes>[^>]*)>"
    r"(?P<body>.*?)</[^<>]*DSML[^<>]*invoke\s*>",
    flags=re.IGNORECASE | re.DOTALL,
)
_DSML_PARAMETER_RE = re.compile(
    r"<(?!/)[^<>]*DSML[^<>]*parameter\b(?P<attributes>[^>]*)>"
    r"(?P<value>.*?)</[^<>]*DSML[^<>]*parameter\s*>",
    flags=re.IGNORECASE | re.DOTALL,
)
_TAG_ATTRIBUTE_RE = re.compile(
    r"(?P<name>[A-Za-z_][\w:.-]*)\s*=\s*(?P<quote>['\"])(?P<value>.*?)"
    r"(?P=quote)",
    flags=re.DOTALL,
)
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", flags=re.IGNORECASE | re.DOTALL)
_SHELL_TOOL_NAME_ALIASES = {"bash", "shell"}


def _text_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, list):
        return str(value or "")
    output: list[str] = []
    for item in value:
        if isinstance(item, str):
            output.append(item)
        elif isinstance(item, dict):
            if item.get("type") in {"input_text", "output_text", "text"}:
                output.append(str(item.get("text") or ""))
    return "\n".join(part for part in output if part)


def _normalized_tool_arguments(value: Any) -> str:
    """Return valid JSON arguments even when an upstream model truncates them."""

    if not isinstance(value, str):
        return json.dumps(value if value is not None else {}, ensure_ascii=False)
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = repair_json(value, return_objects=True)
    if not isinstance(parsed, dict):
        parsed = {"input": str(parsed or value)}
    return json.dumps(parsed, ensure_ascii=False)


def _contains_textual_tool_protocol(value: Any) -> bool:
    """Identify tool syntax emitted as prose instead of a native tool call."""

    return bool(_TEXTUAL_TOOL_PROTOCOL_RE.search(str(value or "")))


def _tag_attributes(value: str) -> dict[str, str]:
    return {
        match.group("name"): html.unescape(match.group("value"))
        for match in _TAG_ATTRIBUTE_RE.finditer(value)
    }


def _promote_dsml_tool_calls(
    result: dict[str, Any],
    *,
    allowed_names: set[str],
    custom_names: set[str],
) -> dict[str, Any]:
    """Promote complete DeepSeek DSML markup into native chat tool calls.

    Some DeepSeek deployments occasionally switch from the requested OpenAI
    tool-call envelope to their textual DSML envelope late in a long turn. Only
    complete invocations of tools advertised in the current request are
    promoted; malformed markup remains prose and is handled by protocol
    recovery without executing anything.
    """

    message = (result.get("choices") or [{}])[0].get("message") or {}
    if message.get("tool_calls"):
        return result
    content = str(message.get("content") or "")
    if not content or not allowed_names:
        return result

    calls: list[dict[str, Any]] = []
    for invoke in _DSML_INVOKE_RE.finditer(content):
        invoke_attributes = _tag_attributes(invoke.group("attributes"))
        name = _canonical_returned_tool_name(
            str(invoke_attributes.get("name") or ""), allowed_names=allowed_names
        )
        if name not in allowed_names:
            continue
        arguments: dict[str, str] = {}
        for parameter in _DSML_PARAMETER_RE.finditer(invoke.group("body")):
            attributes = _tag_attributes(parameter.group("attributes"))
            parameter_name = str(attributes.get("name") or "")
            if parameter_name:
                arguments[parameter_name] = html.unescape(parameter.group("value")).strip()
        if not arguments:
            continue
        if name in custom_names and "input" not in arguments:
            if len(arguments) != 1:
                continue
            arguments = {"input": next(iter(arguments.values()))}
        calls.append(
            {
                "id": f"call_dsml_{uuid.uuid4().hex}",
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": json.dumps(arguments, ensure_ascii=False),
                },
            }
        )

    if calls:
        message["content"] = ""
        message["tool_calls"] = calls
    return result


def _canonical_returned_tool_name(name: str, *, allowed_names: set[str]) -> str:
    """Map a narrow set of shell aliases to Codex's advertised terminal tool.

    Some OpenAI-compatible relays intermittently return ``Bash``/``shell`` even
    though the request advertised ``exec_command``.  The mapping is deliberately
    conditional on ``exec_command`` being present so it cannot affect harnesses
    or models that expose a real tool under one of those names.
    """

    if name in allowed_names:
        return name
    if "exec_command" in allowed_names and name.strip().casefold() in _SHELL_TOOL_NAME_ALIASES:
        return "exec_command"
    return name


def _normalize_returned_tool_aliases(
    result: dict[str, Any], *, allowed_names: set[str]
) -> dict[str, Any]:
    """Normalize relay-specific shell calls into the advertised Codex contract."""

    if "exec_command" not in allowed_names:
        return result
    message = (result.get("choices") or [{}])[0].get("message") or {}
    for call in message.get("tool_calls") or []:
        function = call.get("function") or {}
        raw_name = str(function.get("name") or "")
        canonical_name = _canonical_returned_tool_name(
            raw_name, allowed_names=allowed_names
        )
        if canonical_name == raw_name or canonical_name != "exec_command":
            continue
        try:
            arguments = json.loads(
                _normalized_tool_arguments(function.get("arguments") or "{}")
            )
        except json.JSONDecodeError:
            continue
        command = arguments.get("cmd")
        if not isinstance(command, str) or not command.strip():
            for alias in ("command", "script", "input"):
                candidate = arguments.get(alias)
                if isinstance(candidate, str) and candidate.strip():
                    command = candidate
                    break
        if not isinstance(command, str) or not command.strip():
            continue
        normalized_arguments: dict[str, Any] = {"cmd": command}
        for key in ("workdir", "yield_time_ms", "max_output_tokens", "tty"):
            if key in arguments:
                normalized_arguments[key] = arguments[key]
        function["name"] = "exec_command"
        function["arguments"] = json.dumps(normalized_arguments, ensure_ascii=False)
    return result


def _output_schema(payload: dict[str, Any]) -> dict[str, Any]:
    output_format = (payload.get("text") or {}).get("format") or {}
    schema = output_format.get("schema")
    if not isinstance(schema, dict):
        nested = output_format.get("json_schema") or {}
        schema = nested.get("schema") if isinstance(nested, dict) else None
    if not isinstance(schema, dict):
        return {"type": "object", "additionalProperties": True}
    output = json.loads(json.dumps(schema))
    output.pop("$schema", None)
    return output


def _json_object_candidates(value: Any) -> list[dict[str, Any]]:
    """Extract complete JSON objects without exposing surrounding reasoning text."""

    text = str(value or "").strip()
    if not text:
        return []
    candidates: list[dict[str, Any]] = []
    sources = [text, *[match.group(1).strip() for match in _JSON_FENCE_RE.finditer(text)]]
    decoder = json.JSONDecoder()
    for source in sources:
        try:
            parsed = json.loads(source)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            candidates.append(parsed)
        for match in re.finditer(r"\{", source):
            try:
                parsed, _ = decoder.raw_decode(source[match.start() :])
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                candidates.append(parsed)
    if not candidates:
        repaired = repair_json(text, return_objects=True)
        if isinstance(repaired, dict):
            candidates.append(repaired)
    return candidates


def _final_json_tool(
    payload: dict[str, Any], *, direct_schema: bool = False
) -> dict[str, Any]:
    if direct_schema:
        return {
            "type": "function",
            "function": {
                "name": _FINAL_JSON_TOOL,
                "description": (
                    "Submit the complete evidence-backed terminal contract. Populate every "
                    "required field with real values; never use schema examples or placeholders."
                ),
                "parameters": _output_schema(payload),
            },
        }
    return {
        "type": "function",
        "function": {
            "name": _FINAL_JSON_TOOL,
            "description": (
                "Submit the complete final JSON object as one serialized JSON document. "
                "This is the only valid final action; do not answer in plain text."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "document": {
                        "type": "string",
                        "description": (
                            "The complete serialized JSON object required by the response "
                            "contract, without Markdown fences or surrounding prose."
                        ),
                    }
                },
                "required": ["document"],
                "additionalProperties": False,
            },
        },
    }


def _submitted_final_json_object(result: dict[str, Any]) -> dict[str, Any] | None:
    message = (result.get("choices") or [{}])[0].get("message") or {}
    submission = next(
        (
            call
            for call in message.get("tool_calls") or []
            if str((call.get("function") or {}).get("name") or "")
            == _FINAL_JSON_TOOL
        ),
        None,
    )
    if submission is None:
        return None
    normalized = _normalized_tool_arguments(
        (submission.get("function") or {}).get("arguments") or "{}"
    )
    parsed = json.loads(normalized)
    if not isinstance(parsed, dict):
        return None
    document = parsed.get("document")
    if isinstance(document, dict):
        return document
    if isinstance(document, str):
        try:
            decoded = json.loads(document)
        except json.JSONDecodeError:
            decoded = repair_json(document, return_objects=True)
        return decoded if isinstance(decoded, dict) else None
    # Backward compatibility for cached or alternative endpoints that submit
    # the contract fields directly instead of wrapping a serialized document.
    return parsed


def _consume_final_json_tool(result: dict[str, Any]) -> dict[str, Any]:
    """Convert the bridge-only submission call into a normal assistant JSON message."""

    message = (result.get("choices") or [{}])[0].get("message") or {}
    calls = message.get("tool_calls") or []
    submission = next(
        (
            call
            for call in calls
            if str((call.get("function") or {}).get("name") or "") == _FINAL_JSON_TOOL
        ),
        None,
    )
    if submission is None:
        return result
    submitted = _submitted_final_json_object(result)
    message["content"] = json.dumps(submitted or {}, ensure_ascii=False)
    message["tool_calls"] = [call for call in calls if call is not submission]
    return result


def _persist_final_json_tool(result: dict[str, Any], destination: Path) -> bool:
    """Atomically persist a bridge-only final submission to a trusted path."""

    message = (result.get("choices") or [{}])[0].get("message") or {}
    submission = next(
        (
            call
            for call in message.get("tool_calls") or []
            if str((call.get("function") or {}).get("name") or "") == _FINAL_JSON_TOOL
        ),
        None,
    )
    if submission is None:
        return False
    parsed = _submitted_final_json_object(result)
    if parsed is None:
        return False
    _atomic_write_json(parsed, destination)
    return True


def _persist_final_json_content(
    result: dict[str, Any], destination: Path, *, schema: dict[str, Any] | None = None
) -> bool:
    """Persist a normal JSON-object response used by file-first finalization."""

    message = (result.get("choices") or [{}])[0].get("message") or {}
    for source in (message.get("content"), message.get("reasoning_content")):
        for parsed in reversed(_json_object_candidates(source)):
            if isinstance(schema, dict):
                try:
                    jsonschema.validate(parsed, schema)
                except jsonschema.ValidationError:
                    continue
            message["content"] = json.dumps(parsed, ensure_ascii=False)
            _atomic_write_json(parsed, destination)
            return True
    return False


def _atomic_write_json(parsed: dict[str, Any], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(parsed, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, destination)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _load_valid_json_artifact(
    source: Path, *, schema: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    """Load a complete file-first contract before asking the model to repeat it."""

    try:
        parsed = json.loads(source.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    if not isinstance(parsed, dict):
        return None
    if isinstance(schema, dict):
        try:
            jsonschema.validate(parsed, schema)
        except jsonschema.ValidationError:
            return None
    return parsed


def _artifact_fingerprint(source: Path | None) -> str | None:
    """Fingerprint an artifact so copied recovery inputs are not mistaken for new work."""

    if source is None:
        return None
    try:
        return hashlib.sha256(source.read_bytes()).hexdigest()
    except (FileNotFoundError, OSError):
        return None


def _artifact_contains_completion_placeholder(value: dict[str, Any]) -> bool:
    """Keep initialized scaffolds from being mistaken for completed Agent work."""

    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True).casefold()
    return "agent_required" in serialized or "replace_me" in serialized


def _artifact_completion_result(*, model: str, parsed: dict[str, Any]) -> dict[str, Any]:
    """Return a schema-valid terminal chat result from a trusted workspace artifact."""

    return {
        "id": f"chatcmpl_artifact_{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": json.dumps(parsed, ensure_ascii=False),
                },
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


def _limit_returned_tool_calls(result: dict[str, Any], *, maximum: int | None) -> dict[str, Any]:
    """Prevent one parallel model turn from overshooting the remaining tool budget."""

    if maximum is None:
        return result
    message = (result.get("choices") or [{}])[0].get("message") or {}
    calls = message.get("tool_calls") or []
    if len(calls) > max(0, maximum):
        message["tool_calls"] = calls[: max(0, maximum)]
    return result


def _retain_returned_tool_names(
    result: dict[str, Any], *, allowed_names: set[str] | None
) -> dict[str, Any]:
    if allowed_names is None:
        return result
    message = (result.get("choices") or [{}])[0].get("message") or {}
    message["tool_calls"] = [
        call
        for call in message.get("tool_calls") or []
        if str((call.get("function") or {}).get("name") or "") in allowed_names
    ]
    return result


def _retain_structured_artifact_write_calls(
    result: dict[str, Any], *, destination: Path
) -> dict[str, Any]:
    """Block read/search commands after a file-first phase enters finalization."""

    # A structured phase may have one terminal receipt plus sibling artifacts in
    # the same `outputs/` tree.  Keep the finalization boundary at that parent,
    # while still rejecting paths outside it and all non-write tools.
    if destination.parent.name.casefold() == "outputs":
        return _retain_file_first_artifact_write_calls(result, destination=destination.parent)

    message = (result.get("choices") or [{}])[0].get("message") or {}
    parent_name = destination.parent.name.lower()
    target_name = destination.name.lower()
    relative_target = f"{parent_name}/{target_name}"
    write_markers = (
        ">",
        "write_text",
        ".write(",
        "json.dump",
        "os.replace",
        "replace(",
        "rename(",
        "mv ",
        "tee ",
    )
    retained: list[dict[str, Any]] = []
    for call in message.get("tool_calls") or []:
        arguments = str((call.get("function") or {}).get("arguments") or "")
        lowered = arguments.lower()
        target_named = relative_target in lowered or (
            parent_name in lowered and target_name in lowered
        )
        if (
            target_named
            and (
                any(marker in lowered for marker in write_markers)
                or _native_write_call_targets(call, destination, exact_file=True)
            )
        ):
            retained.append(call)
    message["tool_calls"] = retained
    return result


def _retain_file_first_artifact_write_calls(
    result: dict[str, Any], *, destination: Path
) -> dict[str, Any]:
    """Keep only calls that can write the configured file-first artifact tree."""

    message = (result.get("choices") or [{}])[0].get("message") or {}
    directory_name = destination.name.lower()
    write_markers = (
        ">",
        "write_text",
        ".write(",
        "json.dump",
        "os.replace",
        "replace(",
        "rename(",
        "mv ",
        "tee ",
    )
    retained = []
    for call in message.get("tool_calls") or []:
        arguments = str((call.get("function") or {}).get("arguments") or "")
        lowered = arguments.lower()
        if (
            directory_name in lowered
            and (
                any(marker in lowered for marker in write_markers)
                or _native_write_call_targets(call, destination, exact_file=False)
            )
        ):
            retained.append(call)
    message["tool_calls"] = retained
    return result


_NATIVE_WRITE_TOOL_NAMES = frozenset(
    {"write", "write_file", "create_file", "write_text_file", "apply_patch"}
)
_NATIVE_WRITE_PATH_KEYS = frozenset(
    {"path", "file_path", "filepath", "filename", "target", "destination", "file"}
)
_NATIVE_WRITE_CONTENT_KEYS = frozenset({"content", "text", "data", "body", "patch"})


def _native_write_call_targets(
    call: dict[str, Any], destination: Path, *, exact_file: bool
) -> bool:
    """Recognize Codex/DeepSeek native file writes without allowing reads through.

    DeepSeek-compatible gateways may emit Codex's native ``write`` tool instead of an
    ``exec_command`` containing ``write_text`` or ``json.dump``.  During finalization
    the bridge deliberately filters all other tools, so this narrow structural check
    keeps legitimate writes while still requiring a target path and content payload.
    """

    function = call.get("function") or {}
    name = str(function.get("name") or "").casefold()
    if name not in _NATIVE_WRITE_TOOL_NAMES:
        return False
    raw_arguments = function.get("arguments")
    try:
        arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
    except (TypeError, json.JSONDecodeError):
        return False
    if not isinstance(arguments, dict):
        return False
    path_values = [
        str(value)
        for key, value in arguments.items()
        if str(key).casefold() in _NATIVE_WRITE_PATH_KEYS and isinstance(value, (str, Path))
    ]
    if not path_values or not any(
        str(key).casefold() in _NATIVE_WRITE_CONTENT_KEYS for key in arguments
    ):
        return False
    destination_resolved = destination.resolve()
    destination_name = destination_resolved.name.casefold()
    parent_name = destination_resolved.name.casefold()
    for value in path_values:
        normalized = value.replace("\\", "/").casefold().rstrip("/")
        if exact_file:
            if normalized == destination_name or normalized.endswith(f"/{destination_name}"):
                return True
            continue
        if normalized == parent_name or f"/{parent_name}/" in f"/{normalized}/":
            return True
    return False


def _close_tool_protocol(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Make every assistant tool call followed by exactly one tool result.

    Codex records a function call even when its local argument parser rejects the
    call. OpenAI-compatible chat endpoints reject that history unless a matching
    tool result is present. A synthetic failure result preserves the real failure
    while allowing the Agent to recover on its next model turn.
    """

    output: list[dict[str, Any]] = []
    pending: list[str] = []

    def close_pending() -> None:
        for call_id in pending:
            output.append(
                {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": (
                        "Tool call failed before execution because its arguments were "
                        "invalid, incomplete, or interrupted. Retry with a shorter call."
                    ),
                }
            )
        pending.clear()

    for message in messages:
        role = str(message.get("role") or "")
        if role == "assistant" and message.get("tool_calls"):
            if pending:
                close_pending()
            output.append(message)
            pending.extend(
                str(call.get("id") or "")
                for call in message.get("tool_calls") or []
                if call.get("id")
            )
            continue
        if role == "tool":
            call_id = str(message.get("tool_call_id") or "")
            if call_id in pending:
                output.append(message)
                pending.remove(call_id)
            # Orphaned tool outputs are invalid chat history and carry no usable
            # state once their assistant call has been closed.
            continue
        if pending:
            close_pending()
        output.append(message)
    if pending:
        close_pending()
    return output


def _content_filter_recovery_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Build a compact continuation payload after a relay content-filter error.

    A few OpenAI-compatible relays inspect the entire accumulated chat history,
    including raw output from shell/file tools.  Scientific source text can then
    be rejected even though the current turn is harmless.  The workspace is the
    source of truth for Codex, so it is safe to discard stale tool transcripts and
    ask the Agent to continue from the files it already inspected.  Keep the phase
    instructions and terminal/schema guidance, but remove assistant/tool protocol
    history that would otherwise make the relay reject the retry again.
    """

    recovered = json.loads(json.dumps(payload, ensure_ascii=False))
    messages = recovered.get("messages") or []
    kept: list[dict[str, Any]] = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        role = str(message.get("role") or "")
        if role != "system":
            continue
        content = _text_content(message.get("content"))
        if not content:
            continue
        # Keep the phase contract and the exact terminal schema.  Drop transient
        # Codex/tool-selection system prose, which is both redundant and the most
        # likely place for a relay to retain a flagged tool transcript.
        if (
            content.startswith(_FINAL_SCHEMA_PROMPT_PREFIX)
            or not kept
            or "finalization" in content.casefold()
            or "submit_final_json" in content
            or "fixed path" in content.casefold()
        ):
            kept.append({"role": "system", "content": content[:24000]})

    kept.append(
        {
            "role": "user",
            "content": (
                "The upstream relay rejected the accumulated tool transcript during "
                "content inspection. Continue from the current isolated workspace; "
                "the files already written are authoritative. Do not ask to repeat "
                "old observations. Inspect only the minimum needed, perform the next "
                "required edit or finalization, and return the requested structured "
                "receipt."
            ),
        }
    )
    recovered["messages"] = kept
    return recovered


def _is_content_filter_error(exc: httpx.HTTPStatusError) -> bool:
    """Return whether an upstream 4xx is the relay's conversation filter."""

    try:
        detail = exc.response.text
    except Exception:  # pragma: no cover - defensive for mocked responses
        detail = str(exc)
    lowered = str(detail).casefold()
    return any(
        marker in lowered
        for marker in (
            "data_inspection_failed",
            "inappropriate content",
            "content inspection",
            "content_filter",
        )
    )


def responses_to_chat(
    payload: dict[str, Any],
    *,
    configured_max_tokens: int | None = None,
    prefer_json_schema: bool = False,
) -> tuple[dict[str, Any], set[str]]:
    messages: list[dict[str, Any]] = []
    instructions = _text_content(payload.get("instructions"))
    if instructions:
        messages.append({"role": "system", "content": instructions})

    pending_calls: list[dict[str, Any]] = []
    for item in payload.get("input") or []:
        if isinstance(item, str):
            messages.append({"role": "user", "content": item})
            continue
        if not isinstance(item, dict):
            continue
        item_type = str(item.get("type") or "")
        role = str(item.get("role") or "")
        if role in {"system", "developer", "user", "assistant"}:
            if pending_calls:
                messages.append({"role": "assistant", "content": "", "tool_calls": pending_calls})
                pending_calls = []
            normalized_role = "system" if role == "developer" else role
            messages.append(
                {"role": normalized_role, "content": _text_content(item.get("content"))}
            )
            continue
        if item_type in {"function_call", "custom_tool_call", "local_shell_call"}:
            call_id = str(item.get("call_id") or item.get("id") or f"call_{uuid.uuid4().hex}")
            name = str(item.get("name") or "")
            arguments = item.get("arguments")
            if arguments is None:
                arguments = json.dumps({"input": item.get("input") or ""})
            else:
                arguments = _normalized_tool_arguments(arguments)
            pending_calls.append(
                {
                    "id": call_id,
                    "type": "function",
                    "function": {"name": name, "arguments": arguments},
                }
            )
            continue
        if item_type in {
            "function_call_output",
            "custom_tool_call_output",
            "local_shell_call_output",
        }:
            if pending_calls:
                messages.append({"role": "assistant", "content": "", "tool_calls": pending_calls})
                pending_calls = []
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": str(item.get("call_id") or ""),
                    "content": _text_content(item.get("output")),
                }
            )
    if pending_calls:
        messages.append({"role": "assistant", "content": "", "tool_calls": pending_calls})
    messages = _close_tool_protocol(messages)

    output_format = (payload.get("text") or {}).get("format") or {}
    if prefer_json_schema and output_format.get("type") == "json_schema":
        messages.append(
            {
                "role": "system",
                "content": (
                    f"{_FINAL_SCHEMA_PROMPT_PREFIX}, return one JSON "
                    "object that validates against this exact terminal response schema. "
                    "The schema does not replace required evidence inspection or file writes.\n"
                    + json.dumps(_output_schema(payload), ensure_ascii=False, separators=(",", ":"))
                ),
            }
        )

    tools: list[dict[str, Any]] = []
    custom_names: set[str] = set()
    for tool in payload.get("tools") or []:
        if not isinstance(tool, dict):
            continue
        tool_type = str(tool.get("type") or "function")
        name = str(tool.get("name") or "")
        if not name:
            continue
        if tool_type == "function":
            parameters = tool.get("parameters") or {
                "type": "object",
                "additionalProperties": True,
            }
        else:
            custom_names.add(name)
            parameters = {
                "type": "object",
                "properties": {"input": {"type": "string"}},
                "required": ["input"],
                "additionalProperties": False,
            }
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": str(tool.get("description") or ""),
                    "parameters": parameters,
                },
            }
        )

    output: dict[str, Any] = {
        "model": payload.get("model"),
        "messages": messages,
        "temperature": 0,
    }
    max_tokens = configured_max_tokens or payload.get("max_output_tokens")
    if max_tokens:
        output["max_tokens"] = int(max_tokens)
    if tools:
        output["tools"] = tools
        output["tool_choice"] = "auto"
    _configure_chat_response_format(
        output,
        responses_payload=payload,
        prefer_json_schema=prefer_json_schema,
    )
    return output, custom_names


def _configure_chat_response_format(
    chat_payload: dict[str, Any],
    *,
    responses_payload: dict[str, Any],
    prefer_json_schema: bool = False,
) -> None:
    """Enable JSON-only output only after the Agent has no tools available.

    Some DeepSeek-compatible gateways treat ``response_format=json_object`` as
    dominant over ``tools`` and return a JSON plan instead of a native tool call.
    Codex then mistakes that plan for the terminal response. Keep exploration
    tool-capable and restore JSON-object mode only for tool-free finalization.
    """

    output_format = (responses_payload.get("text") or {}).get("format") or {}
    wants_json = output_format.get("type") in {"json_schema", "json_object"}
    if wants_json and not chat_payload.get("tools"):
        if prefer_json_schema and output_format.get("type") == "json_schema":
            chat_payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": str(output_format.get("name") or "agent_response"),
                    "strict": bool(output_format.get("strict", True)),
                    "schema": _output_schema(responses_payload),
                },
            }
        else:
            chat_payload["response_format"] = {"type": "json_object"}
    else:
        chat_payload.pop("response_format", None)


def _flatten_structured_finalization_messages(
    messages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Retain task instructions and observations without stale tool protocol.

    DeepSeek thinking deployments may keep calling a tool from earlier assistant
    history even after the advertised tool set changes. A terminal submission is
    a fresh synthesis turn: preserve the user's phase contract, exact output
    schema, and every completed tool observation, but remove old call envelopes
    and the generic Codex tool-selection system prompt.
    """

    schema_messages: list[dict[str, Any]] = []
    task_messages: list[dict[str, Any]] = []
    observation_messages: list[dict[str, Any]] = []
    finalization_messages: list[dict[str, Any]] = []
    for message in messages:
        role = str(message.get("role") or "")
        content = _text_content(message.get("content"))
        if role == "system":
            if content.startswith(_FINAL_SCHEMA_PROMPT_PREFIX):
                schema_messages.append({"role": "system", "content": content})
            elif "submit_final_json" in content:
                finalization_messages.append({"role": "system", "content": content})
        elif role == "user" and content:
            task_messages.append({"role": "user", "content": content})
        elif role == "tool":
            observation_messages.append(
                {
                    "role": "user",
                    "content": (
                        "Previously executed workspace-tool observation"
                        f" ({message.get('tool_call_id') or 'unknown call'}):\n{content}"
                    ),
                }
            )
    return [
        *schema_messages,
        *task_messages,
        *observation_messages,
        *finalization_messages,
    ]


def chat_to_response_events(
    result: dict[str, Any], *, custom_names: set[str]
) -> list[dict[str, Any]]:
    response_id = f"resp_{uuid.uuid4().hex}"
    created_at = int(time.time())
    choice = (result.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    output_items: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []

    response_base = {
        "id": response_id,
        "object": "response",
        "created_at": created_at,
        "status": "in_progress",
        "model": result.get("model"),
        "output": [],
    }
    events.append({"type": "response.created", "response": response_base})

    output_index = 0
    for raw_call in message.get("tool_calls") or []:
        function = raw_call.get("function") or {}
        name = str(function.get("name") or "")
        arguments = _normalized_tool_arguments(function.get("arguments") or "{}")
        call_id = str(raw_call.get("id") or f"call_{uuid.uuid4().hex}")
        item_id = f"fc_{uuid.uuid4().hex}"
        if name in custom_names:
            try:
                parsed = json.loads(arguments)
                custom_input = str(parsed.get("input") or "")
            except (json.JSONDecodeError, AttributeError):
                custom_input = arguments
            item = {
                "id": item_id,
                "type": "custom_tool_call",
                "status": "completed",
                "call_id": call_id,
                "name": name,
                "input": custom_input,
            }
            events.append(
                {
                    "type": "response.output_item.added",
                    "output_index": output_index,
                    "item": {**item, "status": "in_progress", "input": ""},
                }
            )
            events.append(
                {
                    "type": "response.custom_tool_call_input.delta",
                    "output_index": output_index,
                    "item_id": item_id,
                    "delta": custom_input,
                }
            )
            events.append(
                {
                    "type": "response.custom_tool_call_input.done",
                    "output_index": output_index,
                    "item_id": item_id,
                    "input": custom_input,
                }
            )
        else:
            item = {
                "id": item_id,
                "type": "function_call",
                "status": "completed",
                "call_id": call_id,
                "name": name,
                "arguments": arguments,
            }
            events.append(
                {
                    "type": "response.output_item.added",
                    "output_index": output_index,
                    "item": {**item, "status": "in_progress", "arguments": ""},
                }
            )
            events.append(
                {
                    "type": "response.function_call_arguments.delta",
                    "output_index": output_index,
                    "item_id": item_id,
                    "delta": arguments,
                }
            )
            events.append(
                {
                    "type": "response.function_call_arguments.done",
                    "output_index": output_index,
                    "item_id": item_id,
                    "arguments": arguments,
                }
            )
        events.append(
            {
                "type": "response.output_item.done",
                "output_index": output_index,
                "item": item,
            }
        )
        output_items.append(item)
        output_index += 1

    content = str(message.get("content") or "")
    if content:
        item_id = f"msg_{uuid.uuid4().hex}"
        item = {
            "id": item_id,
            "type": "message",
            "status": "completed",
            "role": "assistant",
            "content": [{"type": "output_text", "text": content, "annotations": []}],
        }
        events.extend(
            [
                {
                    "type": "response.output_item.added",
                    "output_index": output_index,
                    "item": {
                        "id": item_id,
                        "type": "message",
                        "status": "in_progress",
                        "role": "assistant",
                        "content": [],
                    },
                },
                {
                    "type": "response.content_part.added",
                    "output_index": output_index,
                    "item_id": item_id,
                    "content_index": 0,
                    "part": {"type": "output_text", "text": "", "annotations": []},
                },
                {
                    "type": "response.output_text.delta",
                    "output_index": output_index,
                    "item_id": item_id,
                    "content_index": 0,
                    "delta": content,
                },
                {
                    "type": "response.output_text.done",
                    "output_index": output_index,
                    "item_id": item_id,
                    "content_index": 0,
                    "text": content,
                },
                {
                    "type": "response.content_part.done",
                    "output_index": output_index,
                    "item_id": item_id,
                    "content_index": 0,
                    "part": item["content"][0],
                },
                {
                    "type": "response.output_item.done",
                    "output_index": output_index,
                    "item": item,
                },
            ]
        )
        output_items.append(item)

    upstream_usage = result.get("usage") or {}
    cached_tokens = int(
        upstream_usage.get("prompt_cache_hit_tokens")
        or upstream_usage.get("cached_tokens")
        or (upstream_usage.get("prompt_tokens_details") or {}).get("cached_tokens")
        or 0
    )
    usage = {
        "input_tokens": int(upstream_usage.get("prompt_tokens") or 0),
        "output_tokens": int(upstream_usage.get("completion_tokens") or 0),
        "total_tokens": int(upstream_usage.get("total_tokens") or 0),
        "input_tokens_details": {"cached_tokens": cached_tokens},
        "output_tokens_details": {"reasoning_tokens": 0},
    }
    response = {
        **response_base,
        "status": "completed",
        "output": output_items,
        "usage": usage,
    }
    events.append({"type": "response.completed", "response": response})
    return events


class ResponsesBridge(AbstractContextManager["ResponsesBridge"]):
    def __init__(
        self,
        *,
        upstream_base_url: str,
        api_key: str,
        model: str,
        timeout_seconds: float,
        proxy_url: str | None = None,
        chat_template_kwargs: dict[str, Any] | None = None,
        thinking: str | None = None,
        max_tokens: int | None = None,
        structured_finalization_max_tokens: int | None = None,
        prefer_json_schema: bool = False,
        structured_finalization_via_submit_tool: bool = False,
        max_tool_calls: int = 24,
        finalization_reserve: int = 4,
        artifact_finalization_required: bool = True,
        structured_artifact_path: str | Path | None = None,
        file_first_artifact_path: str | Path | None = None,
        file_first_required_files: Iterable[str] | None = None,
        file_first_required_modified_files: Iterable[str] | None = None,
        retries: int = 2,
    ) -> None:
        self.upstream_base_url = upstream_base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.proxy_url = proxy_url
        self.chat_template_kwargs = dict(chat_template_kwargs or {})
        self.thinking = thinking
        self.max_tokens = max_tokens
        self.structured_finalization_max_tokens = structured_finalization_max_tokens
        self.prefer_json_schema = bool(prefer_json_schema)
        self.structured_finalization_via_submit_tool = bool(
            structured_finalization_via_submit_tool
        )
        self.max_tool_calls = max(0, int(max_tool_calls))
        self.finalization_reserve = max(0, int(finalization_reserve))
        self.artifact_finalization_required = bool(artifact_finalization_required)
        self.structured_artifact_path = (
            Path(structured_artifact_path).resolve()
            if structured_artifact_path is not None
            else None
        )
        self.structured_artifact_baseline_fingerprint = _artifact_fingerprint(
            self.structured_artifact_path
        )
        self.file_first_artifact_path = (
            Path(file_first_artifact_path).resolve()
            if file_first_artifact_path is not None
            else None
        )
        self.file_first_required_files = tuple(file_first_required_files or ())
        self.file_first_required_modified_files = tuple(
            file_first_required_modified_files or ()
        )
        self.file_first_modified_baseline_fingerprints = {
            relative: _artifact_fingerprint(self.file_first_artifact_path / relative)
            if self.file_first_artifact_path is not None
            else None
            for relative in self.file_first_required_modified_files
        }
        self.final_artifact_written = False
        self.retries = max(0, int(retries))
        self.usage_records: list[dict[str, Any]] = []
        self.seen_tool_call_ids: set[str] = set()
        self.tool_call_count = 0
        self.reasoning_by_tool_call_id: dict[str, str] = {}
        self.finalization_tool_call_baseline: int | None = None
        self.structured_finalization_attempts = 0
        self.trace_lock = threading.Lock()
        self.server: ThreadingHTTPServer | None = None
        self.thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        if self.server is None:
            raise RuntimeError("Responses bridge is not running")
        host, port = self.server.server_address[:2]
        return f"http://{host}:{port}/v1"

    def __enter__(self) -> "ResponsesBridge":
        bridge = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, _format: str, *_args: Any) -> None:
                return

            def do_GET(self) -> None:  # noqa: N802
                if self.path.rstrip("/") not in {"/v1/models", "/models"}:
                    self.send_error(404)
                    return
                body = json.dumps(
                    {
                        "object": "list",
                        "data": [{"id": bridge.model, "object": "model", "owned_by": "rcb"}],
                    }
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self) -> None:  # noqa: N802
                if self.path.rstrip("/") not in {"/v1/responses", "/responses"}:
                    self.send_error(404)
                    return
                try:
                    length = int(self.headers.get("Content-Length") or 0)
                    payload = json.loads(self.rfile.read(length))
                    result, custom_names = bridge._call_upstream(payload)
                    events = chat_to_response_events(result, custom_names=custom_names)
                except Exception as exc:
                    body = json.dumps(
                        {
                            "error": {
                                "type": type(exc).__name__,
                                "message": str(exc)[:2000],
                            }
                        }
                    ).encode("utf-8")
                    self.send_response(502)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return

                stream = bool(payload.get("stream", True))
                if not stream:
                    body = json.dumps(events[-1]["response"]).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                chunks = [
                    f"event: {event['type']}\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"
                    for event in events
                ]
                chunks.append("data: [DONE]\n\n")
                body = "".join(chunks).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
        if self.thread is not None:
            self.thread.join(timeout=5)
        self.server = None
        self.thread = None

    def _call_upstream(self, responses_payload: dict[str, Any]) -> tuple[dict[str, Any], set[str]]:
        for item in responses_payload.get("input") or []:
            if isinstance(item, dict) and item.get("type") in {
                "function_call",
                "custom_tool_call",
                "local_shell_call",
            }:
                call_id = str(item.get("call_id") or item.get("id") or "")
                if call_id:
                    self.seen_tool_call_ids.add(call_id)
        payload, custom_names = responses_to_chat(
            responses_payload,
            configured_max_tokens=self.max_tokens,
            prefer_json_schema=self.prefer_json_schema,
        )
        self._restore_reasoning_content(payload.get("messages") or [])
        payload["model"] = self.model
        structured_artifact_mode = self.structured_artifact_path is not None
        file_first_artifact_complete = bool(
            self.file_first_artifact_path is not None
            and self.file_first_required_files
            and all(
                (self.file_first_artifact_path / relative).is_file()
                for relative in self.file_first_required_files
            )
            and all(
                _artifact_fingerprint(self.file_first_artifact_path / relative) is not None
                and _artifact_fingerprint(self.file_first_artifact_path / relative)
                != self.file_first_modified_baseline_fingerprints.get(relative)
                for relative in self.file_first_required_modified_files
            )
        )
        structured_output_schema = (
            _output_schema(responses_payload) if structured_artifact_mode else None
        )
        completed_artifact = (
            _load_valid_json_artifact(
                self.structured_artifact_path,
                schema=structured_output_schema,
            )
            if self.structured_artifact_path is not None
            else None
        )
        artifact_changed = (
            completed_artifact is not None
            and not _artifact_contains_completion_placeholder(completed_artifact)
            and _artifact_fingerprint(self.structured_artifact_path)
            != self.structured_artifact_baseline_fingerprint
        )
        self.final_artifact_written = artifact_changed
        if artifact_changed:
            return (
                _artifact_completion_result(model=self.model, parsed=completed_artifact),
                custom_names,
            )
        seen_calls = self.tool_call_count
        remaining_calls = max(0, self.max_tool_calls - seen_calls)
        effective_finalization_reserve = (
            self.finalization_reserve
            if self.artifact_finalization_required
            else min(1, self.finalization_reserve)
        )
        finalization_call_consumed = (
            self.finalization_tool_call_baseline is not None
            and seen_calls > self.finalization_tool_call_baseline
        )
        returned_tool_limit: int | None = None
        force_final_json = False
        force_final_content = False
        structured_workspace_finalization = False
        file_first_workspace_finalization = False
        if file_first_artifact_complete and self.artifact_finalization_required:
            payload.pop("tools", None)
            payload.pop("tool_choice", None)
            returned_tool_limit = 0
            payload["messages"].append(
                {
                    "role": "system",
                    "content": (
                        "The required file-first artifact is complete. Do not request another "
                        "tool; return only the small final JSON receipt now."
                    ),
                }
            )
        elif (
            self.max_tool_calls and seen_calls >= self.max_tool_calls
        ) or finalization_call_consumed:
            if (
                structured_artifact_mode
                and not self.final_artifact_written
                and self.structured_finalization_attempts < 4
            ):
                self.structured_finalization_attempts += 1
                returned_tool_limit = 1
                if self.structured_finalization_via_submit_tool:
                    payload["tools"] = [
                        _final_json_tool(responses_payload, direct_schema=True)
                    ]
                    payload["tool_choice"] = "auto"
                    force_final_json = True
                else:
                    structured_workspace_finalization = True
            elif (
                self.file_first_artifact_path is not None
                and not file_first_artifact_complete
                and self.structured_finalization_attempts < 4
            ):
                self.structured_finalization_attempts += 1
                returned_tool_limit = 1
                file_first_workspace_finalization = True
            elif self.artifact_finalization_required:
                payload.pop("tools", None)
                payload.pop("tool_choice", None)
                returned_tool_limit = 0
            else:
                payload["tools"] = [_final_json_tool(responses_payload)]
                payload["tool_choice"] = "auto"
                returned_tool_limit = 1
                force_final_json = True
            payload["messages"].append(
                {
                    "role": "system",
                    "content": (
                        "The finalization tool call has been consumed or the hard tool-call "
                        f"budget of {self.max_tool_calls} has been reached. "
                        + (
                            "Call submit_final_json now with the complete evidence-backed "
                            "contract in the tool arguments. Do not use schema "
                            "examples or placeholders and do not request a shell tool."
                            if force_final_json
                            else
                            "Use exactly one workspace tool call now to atomically write the "
                            "complete contract to the fixed path stated in the phase instructions. "
                            "Write JSON data directly through a quoted heredoc and validate it; do "
                            "not embed JSON syntax as a Python dictionary. Do not read or search. "
                            "Keep internal reasoning minimal and devote the output budget to the "
                            "complete write-tool arguments."
                            if structured_workspace_finalization
                            else "Use exactly one workspace tool call now to write or repair "
                            f"the required files under `{self.file_first_artifact_path.name}/`. "
                            "Do not read or search; devote this call to the complete write."
                            if file_first_workspace_finalization
                            else "Do not request another tool. Return the final JSON response now, "
                            "using the evidence already collected; reject with precise missing "
                            "fields when the evidence is insufficient."
                            if self.artifact_finalization_required
                            else "Call submit_final_json now with the complete object required by "
                            "the response schema. Do not answer in plain text and do not request "
                            "a shell tool."
                        )
                    ),
                }
            )
        elif (
            self.max_tool_calls
            and effective_finalization_reserve
            and remaining_calls <= effective_finalization_reserve
        ):
            returned_tool_limit = 1
            if structured_artifact_mode and not self.final_artifact_written:
                if self.finalization_tool_call_baseline is None:
                    self.finalization_tool_call_baseline = seen_calls
                self.structured_finalization_attempts += 1
                if self.structured_finalization_via_submit_tool:
                    payload["tools"] = [
                        _final_json_tool(responses_payload, direct_schema=True)
                    ]
                    payload["tool_choice"] = "auto"
                    force_final_json = True
                    content = (
                        f"Only {remaining_calls} calls remain before the hard limit. The search "
                        "phase is over. Call submit_final_json now with the complete evidence-backed "
                        "contract in the tool arguments. Do not use generic schema "
                        "examples or placeholders and do not request a shell tool."
                    )
                else:
                    structured_workspace_finalization = True
                    content = (
                        f"Only {remaining_calls} calls remain before the hard limit. The search "
                        "phase is over. Exactly one workspace call is available: use it only to "
                        "atomically write the complete contract to the fixed path stated in the "
                        "phase instructions. Do not search, read, or inspect anything else. Write "
                        "the explicit terminal negative contract when evidence is insufficient."
                    )
            elif self.artifact_finalization_required:
                if self.file_first_artifact_path is not None and file_first_artifact_complete:
                    payload.pop("tools", None)
                    payload.pop("tool_choice", None)
                    returned_tool_limit = 0
                    content = (
                        "The required file-first artifact is complete. Do not request another "
                        "tool; return only the small final JSON receipt now."
                    )
                else:
                    if self.finalization_tool_call_baseline is None:
                        self.finalization_tool_call_baseline = seen_calls
                    file_first_workspace_finalization = (
                        self.file_first_artifact_path is not None
                    )
                    content = (
                        f"Only {remaining_calls} tool calls remain before the hard limit. "
                        "The search phase is over. Exactly one finalization tool call remains: "
                        "use it only to write or repair the required workspace artifact. "
                        "Do not reread, search, or inspect anything else; return the small "
                        "final JSON receipt only after the required files exist."
                    )
            else:
                payload["tools"] = [_final_json_tool(responses_payload)]
                payload["tool_choice"] = "auto"
                self.finalization_tool_call_baseline = seen_calls
                force_final_json = True
                content = (
                    f"Only {remaining_calls} calls remain before the hard limit. The search "
                    "phase is over and this phase uses an inline structured contract that "
                    "the orchestrator will persist. Call submit_final_json now with exactly "
                    "the complete object required by its schema. Do not answer in plain text "
                    "and do not request a shell tool; use the explicit terminal negative "
                    "decision when evidence is insufficient."
                )
            payload["messages"].append({"role": "system", "content": content})
        elif self.max_tool_calls:
            returned_tool_limit = max(
                0,
                remaining_calls - min(effective_finalization_reserve, remaining_calls),
            )
        if (
            force_final_json
            or structured_workspace_finalization
            or file_first_workspace_finalization
        ) and self.structured_finalization_max_tokens:
            payload["max_tokens"] = max(
                int(payload.get("max_tokens") or 0),
                int(self.structured_finalization_max_tokens),
            )
        if (
            force_final_json
            and structured_artifact_mode
            and self.structured_finalization_via_submit_tool
        ):
            payload["messages"] = _flatten_structured_finalization_messages(
                payload.get("messages") or []
            )
        _configure_chat_response_format(
            payload,
            responses_payload=responses_payload,
            prefer_json_schema=self.prefer_json_schema,
        )
        if self.chat_template_kwargs:
            payload["chat_template_kwargs"] = self.chat_template_kwargs
        elif self.thinking:
            payload["thinking"] = {"type": self.thinking}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        client_kwargs: dict[str, Any] = {"timeout": self.timeout_seconds}
        if self.proxy_url:
            client_kwargs["proxy"] = self.proxy_url
        last_error: Exception | None = None
        content_filter_recovered = False
        with httpx.Client(**client_kwargs) as client:
            for attempt in range(self.retries + 1):
                try:
                    response = client.post(
                        f"{self.upstream_base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    # Some OpenAI-compatible endpoints require strict JSON Schema
                    # objects (`additionalProperties: false`) while the benchmark
                    # contracts intentionally allow extension fields.  Fall back to
                    # JSON-object mode for the terminal response only; tool-capable
                    # exploration is unaffected and stricter gateways still receive
                    # the original schema first.
                    if (
                        getattr(response, "status_code", None) == 400
                        and payload.get("response_format", {}).get("type") == "json_schema"
                        and "additionalProperties" in getattr(response, "text", "")
                    ):
                        payload["response_format"] = {"type": "json_object"}
                        response = client.post(
                            f"{self.upstream_base_url}/chat/completions",
                            headers=headers,
                            json=payload,
                        )
                    if response.is_error:
                        detail = response.text[:4000]
                        raise httpx.HTTPStatusError(
                            f"upstream HTTP {response.status_code}: {detail}",
                            request=response.request,
                            response=response,
                        )
                    allowed_tool_names = {
                        str((tool.get("function") or {}).get("name") or "")
                        for tool in payload.get("tools") or []
                    }
                    raw_result = response.json()
                    self._trace_upstream_result(raw_result, phase="primary")
                    result = _promote_dsml_tool_calls(
                        raw_result,
                        allowed_names=allowed_tool_names,
                        custom_names=custom_names,
                    )
                    result = _normalize_returned_tool_aliases(
                        result, allowed_names=allowed_tool_names
                    )
                    if (
                        structured_workspace_finalization
                        and self.structured_artifact_path is not None
                    ):
                        result = _retain_structured_artifact_write_calls(
                            result,
                            destination=self.structured_artifact_path,
                        )
                    if (
                        file_first_workspace_finalization
                        and self.file_first_artifact_path is not None
                    ):
                        result = _retain_file_first_artifact_write_calls(
                            result,
                            destination=self.file_first_artifact_path,
                        )
                    result = _limit_returned_tool_calls(result, maximum=returned_tool_limit)
                    result = _retain_returned_tool_names(
                        result,
                        allowed_names=(
                            {_FINAL_JSON_TOOL}
                            if force_final_json
                            else allowed_tool_names
                            if structured_workspace_finalization
                            else None
                        ),
                    )
                    self._remember_reasoning_content(result)
                    if force_final_json and self.structured_artifact_path is not None:
                        self.final_artifact_written = (
                            _persist_final_json_tool(result, self.structured_artifact_path)
                            or _persist_final_json_content(
                                result,
                                self.structured_artifact_path,
                                schema=structured_output_schema,
                            )
                            or self.final_artifact_written
                        )
                    if force_final_content and self.structured_artifact_path is not None:
                        self.final_artifact_written = (
                            _persist_final_json_content(
                                result,
                                self.structured_artifact_path,
                                schema=structured_output_schema,
                            )
                            or self.final_artifact_written
                        )
                    if (
                        structured_workspace_finalization
                        and self.structured_artifact_path is not None
                    ):
                        self.final_artifact_written = (
                            _persist_final_json_content(
                                result,
                                self.structured_artifact_path,
                                schema=structured_output_schema,
                            )
                            or self.final_artifact_written
                        )
                    result = _consume_final_json_tool(result)
                    message = (result.get("choices") or [{}])[0].get("message") or {}
                    content = message.get("content") or ""
                    file_first_blank_response = (
                        self.artifact_finalization_required
                        and not structured_artifact_mode
                        and not file_first_artifact_complete
                        and not str(content).strip()
                    )
                    protocol_recovery_attempt = 0
                    protocol_recovery_limit = 3
                    recovery_payload = payload
                    early_structured_finalization = (
                        structured_artifact_mode
                        and self.structured_finalization_via_submit_tool
                        and not self.final_artifact_written
                    )
                    while (
                        not message.get("tool_calls")
                        and (
                            _contains_textual_tool_protocol(content)
                            or (force_final_json and not str(content).strip())
                            or (force_final_content and not self.final_artifact_written)
                            or file_first_blank_response
                            or (
                                structured_workspace_finalization
                                and not self.final_artifact_written
                            )
                            or file_first_workspace_finalization
                            or early_structured_finalization
                        )
                        and protocol_recovery_attempt < protocol_recovery_limit
                    ):
                        # Some chat-only models occasionally print their internal
                        # tool markup instead of returning native ``tool_calls``.
                        # Codex treats that prose as a terminal answer. Recover in
                        # this process so one malformed turn does not consume a
                        # full Agent retry or masquerade as an executed command.
                        recovery_payload = json.loads(json.dumps(recovery_payload))
                        structured_content_fallback = (
                            structured_workspace_finalization
                            and protocol_recovery_attempt >= 1
                        )
                        structured_submission_recovery = (
                            force_final_json or early_structured_finalization
                        )
                        if structured_submission_recovery:
                            recovery_payload["tools"] = [
                                _final_json_tool(
                                    responses_payload,
                                    direct_schema=(
                                        structured_artifact_mode
                                        and self.structured_finalization_via_submit_tool
                                    ),
                                )
                            ]
                        elif (
                            structured_workspace_finalization
                            and not structured_content_fallback
                        ) or file_first_workspace_finalization:
                            recovery_payload["tools"] = payload.get("tools") or []
                        elif file_first_blank_response:
                            recovery_payload["tools"] = payload.get("tools") or []
                        else:
                            recovery_payload.pop("tools", None)
                        recovery_payload.pop("tool_choice", None)
                        _configure_chat_response_format(
                            recovery_payload,
                            responses_payload=responses_payload,
                            prefer_json_schema=self.prefer_json_schema,
                        )
                        recovery_reason = (
                            "Your previous response did not call the required final JSON tool. "
                            if structured_submission_recovery
                            else "Your previous response was not one valid JSON object. "
                            if force_final_content
                            else "Your previous response did not write the required artifact. "
                            if structured_workspace_finalization
                            else "Your previous response did not write the required file-first artifact. "
                            if file_first_workspace_finalization
                            else "Your previous response was blank before the file-first phase completed. "
                            if file_first_blank_response
                            else "Your previous message printed tool-call protocol as plain text. "
                        )
                        recovery_payload["messages"].extend(
                            [
                                {
                                    "role": "assistant",
                                    "content": str(content)[:4000],
                                },
                                {
                                    "role": "system",
                                    "content": (
                                        recovery_reason
                                        + "No tool was executed. Do not emit an unavailable tool "
                                        "or claim that its command ran. "
                                        + (
                                            "Call submit_final_json now with the complete object "
                                            "required by its parameter schema. "
                                            if structured_submission_recovery
                                            else "Return the complete response-contract object "
                                            "as plain JSON without Markdown, prose, or tool syntax. "
                                            if force_final_content
                                            else (
                                                "Return the complete response-contract object as "
                                                "plain JSON without Markdown, prose, or tool syntax. "
                                                "The bridge will atomically persist it to the fixed "
                                                "workspace path. "
                                                if structured_content_fallback
                                                else "Use exactly one available workspace tool call "
                                                "to atomically write the complete contract to the fixed "
                                                "path in the phase instructions. Do not search or read. "
                                            )
                                            if structured_workspace_finalization
                                            else (
                                                "Use exactly one available workspace tool call to write "
                                                "the required files under the configured artifact "
                                                "directory. Do not search or read. "
                                            )
                                            if file_first_workspace_finalization
                                            else (
                                                "Continue the file-first phase with an available workspace "
                                                "tool call. Write the required artifact files before returning "
                                                "the small final receipt. Do not restart evidence collection. "
                                            )
                                            if file_first_blank_response
                                            else "Return exactly one valid JSON object and no "
                                            "surrounding prose, conforming to the required "
                                            "response schema. "
                                        )
                                        + "Use only evidence "
                                        "already collected. If a required artifact was not "
                                        "written or evidence is insufficient, return the "
                                        "explicit terminal negative/failure decision allowed "
                                        "by the output contract. This is protocol-recovery "
                                        f"attempt {protocol_recovery_attempt + 1} of 3."
                                    ),
                                },
                            ]
                        )
                        if structured_submission_recovery:
                            recovery_payload["messages"] = (
                                _flatten_structured_finalization_messages(
                                    recovery_payload.get("messages") or []
                                )
                            )
                        recovery = client.post(
                            f"{self.upstream_base_url}/chat/completions",
                            headers=headers,
                            json=recovery_payload,
                        )
                        if (
                            getattr(recovery, "status_code", None) == 400
                            and recovery_payload.get("response_format", {}).get("type")
                            == "json_schema"
                            and "additionalProperties" in getattr(recovery, "text", "")
                        ):
                            recovery_payload["response_format"] = {"type": "json_object"}
                            recovery = client.post(
                                f"{self.upstream_base_url}/chat/completions",
                                headers=headers,
                                json=recovery_payload,
                            )
                        if recovery.is_error:
                            detail = recovery.text[:4000]
                            raise httpx.HTTPStatusError(
                                f"upstream HTTP {recovery.status_code}: {detail}",
                                request=recovery.request,
                                response=recovery,
                            )
                        recovery_allowed_tool_names = {
                            str((tool.get("function") or {}).get("name") or "")
                            for tool in recovery_payload.get("tools") or []
                        }
                        raw_recovery = recovery.json()
                        self._trace_upstream_result(
                            raw_recovery,
                            phase=f"protocol_recovery_{protocol_recovery_attempt + 1}",
                        )
                        result = _promote_dsml_tool_calls(
                            raw_recovery,
                            allowed_names=recovery_allowed_tool_names,
                            custom_names=custom_names,
                        )
                        result = _normalize_returned_tool_aliases(
                            result, allowed_names=recovery_allowed_tool_names
                        )
                        if (
                            structured_workspace_finalization
                            and self.structured_artifact_path is not None
                        ):
                            result = _retain_structured_artifact_write_calls(
                                result,
                                destination=self.structured_artifact_path,
                            )
                        if (
                            file_first_workspace_finalization
                            and self.file_first_artifact_path is not None
                        ):
                            result = _retain_file_first_artifact_write_calls(
                                result,
                                destination=self.file_first_artifact_path,
                            )
                        result = _limit_returned_tool_calls(
                            result,
                            maximum=(
                                1
                                if (
                                    structured_submission_recovery
                                    or structured_workspace_finalization
                                    or file_first_workspace_finalization
                                    or file_first_blank_response
                                )
                                else 0
                            ),
                        )
                        result = _retain_returned_tool_names(
                            result,
                            allowed_names=(
                                {_FINAL_JSON_TOOL}
                                if structured_submission_recovery
                                else recovery_allowed_tool_names
                                if (
                                    structured_workspace_finalization
                                    or file_first_workspace_finalization
                                )
                                else None
                            ),
                        )
                        self._remember_reasoning_content(result)
                        if (
                            structured_submission_recovery
                            and self.structured_artifact_path is not None
                        ):
                            self.final_artifact_written = (
                                _persist_final_json_tool(result, self.structured_artifact_path)
                                or _persist_final_json_content(
                                    result,
                                    self.structured_artifact_path,
                                    schema=structured_output_schema,
                                )
                                or self.final_artifact_written
                            )
                        if force_final_content and self.structured_artifact_path is not None:
                            self.final_artifact_written = (
                                _persist_final_json_content(
                                    result,
                                    self.structured_artifact_path,
                                    schema=structured_output_schema,
                                )
                                or self.final_artifact_written
                            )
                        if (
                            structured_workspace_finalization
                            and self.structured_artifact_path is not None
                        ):
                            self.final_artifact_written = (
                                _persist_final_json_content(
                                    result,
                                    self.structured_artifact_path,
                                    schema=structured_output_schema,
                                )
                                or self.final_artifact_written
                            )
                        result = _consume_final_json_tool(result)
                        message = (result.get("choices") or [{}])[0].get("message") or {}
                        content = message.get("content") or ""
                        file_first_blank_response = (
                            self.artifact_finalization_required
                            and not structured_artifact_mode
                            and not file_first_artifact_complete
                            and not str(content).strip()
                        )
                        early_structured_finalization = (
                            structured_artifact_mode
                            and self.structured_finalization_via_submit_tool
                            and not self.final_artifact_written
                        )
                        protocol_recovery_attempt += 1
                    for call in message.get("tool_calls") or []:
                        call_id = str(call.get("id") or "")
                        if call_id:
                            self.seen_tool_call_ids.add(call_id)
                    self.tool_call_count += len(message.get("tool_calls") or [])
                    return result, custom_names
                except (httpx.TimeoutException, httpx.TransportError, httpx.HTTPStatusError) as exc:
                    last_error = exc
                    if (
                        isinstance(exc, httpx.HTTPStatusError)
                        and _is_content_filter_error(exc)
                        and not content_filter_recovered
                    ):
                        # Some relays reject a long accumulated tool transcript
                        # with a non-retryable 400.  Compact the conversation once
                        # and retry the same Agent turn from the live workspace.
                        payload = _content_filter_recovery_payload(payload)
                        content_filter_recovered = True
                        continue
                    retryable_status = not isinstance(exc, httpx.HTTPStatusError) or (
                        exc.response.status_code in {408, 409, 429, 500, 502, 503, 504}
                    )
                    if not retryable_status or attempt >= self.retries:
                        raise
                    time.sleep(min(8.0, 0.5 * (2**attempt)))
        assert last_error is not None
        raise last_error

    def _trace_upstream_result(self, result: dict[str, Any], *, phase: str) -> None:
        if self.structured_artifact_path is None:
            return
        choice = (result.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        calls = message.get("tool_calls") or []
        record = {
            "timestamp": time.time(),
            "phase": phase,
            "finish_reason": choice.get("finish_reason"),
            "content_characters": len(str(message.get("content") or "")),
            "reasoning_characters": len(str(message.get("reasoning_content") or "")),
            "tool_names": [
                str((call.get("function") or {}).get("name") or "") for call in calls
            ],
            "tool_argument_characters": [
                len(str((call.get("function") or {}).get("arguments") or ""))
                for call in calls
            ],
            "usage": result.get("usage") or {},
        }
        self.usage_records.append(dict(record["usage"]))
        trace_path = self.structured_artifact_path.parent.parent / "_bridge_trace.jsonl"
        try:
            with self.trace_lock:
                with trace_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            return

    def usage_summary(self) -> dict[str, Any]:
        """Return provider usage totals without relying on Codex's lossy aggregation."""

        prompt = sum(int(row.get("prompt_tokens") or 0) for row in self.usage_records)
        output = sum(int(row.get("completion_tokens") or 0) for row in self.usage_records)
        total = sum(int(row.get("total_tokens") or 0) for row in self.usage_records)
        cache_hit = sum(
            int(
                row.get("prompt_cache_hit_tokens")
                or row.get("cached_tokens")
                or (row.get("prompt_tokens_details") or {}).get("cached_tokens")
                or 0
            )
            for row in self.usage_records
        )
        return {
            "request_count": len(self.usage_records),
            "prompt_tokens": prompt,
            "prompt_cache_hit_tokens": cache_hit,
            "prompt_cache_miss_tokens": max(0, prompt - cache_hit),
            "completion_tokens": output,
            "total_tokens": total,
        }

    def _remember_reasoning_content(self, result: dict[str, Any]) -> None:
        message = (result.get("choices") or [{}])[0].get("message") or {}
        reasoning = message.get("reasoning_content")
        if reasoning in (None, ""):
            return
        value = str(reasoning)
        for call in message.get("tool_calls") or []:
            call_id = str(call.get("id") or "")
            if call_id:
                self.reasoning_by_tool_call_id[call_id] = value

    def _restore_reasoning_content(self, messages: list[dict[str, Any]]) -> None:
        for message in messages:
            if message.get("role") != "assistant" or not message.get("tool_calls"):
                continue
            reasoning = next(
                (
                    self.reasoning_by_tool_call_id.get(str(call.get("id") or ""))
                    for call in message.get("tool_calls") or []
                    if self.reasoning_by_tool_call_id.get(str(call.get("id") or ""))
                ),
                None,
            )
            if reasoning:
                message["reasoning_content"] = reasoning

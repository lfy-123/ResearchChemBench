"""Versioned UTF-8 windows and typed JSON Pointer selection; never runs a program."""
from __future__ import annotations

import codecs
import hashlib
import json
import re

from .response_policy import DEFAULT_TEXT_CHARS, MAX_RESPONSE_BYTES, compact_enabled, response_bytes
from .response_pages import pointer_part
from .workspace import resolve_workspace_path, relative_workspace_path

MAX_JSON_BYTES = 50 * 1024 * 1024


def _error(code, message, **fields):
    return {"status": "invalid_request", "error": {"code": code, "message": message}, **fields}


def _select(value, pointer):
    for encoded in pointer.split("/")[1:] if pointer else []:
        if re.search(r"~(?![01])", encoded):
            raise ValueError("invalid JSON Pointer escape")
        part = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value[part]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", part):
            value = value[int(part)]
        else:
            raise KeyError(part)
    return value


def _type(value):
    if value is None: return "null"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, dict): return "object"
    if isinstance(value, list): return "array"
    if isinstance(value, str): return "string"
    return "number"


def read_selected(request):
    path = resolve_workspace_path(request.path, must_exist=True)
    if not path.is_file():
        raise ValueError("Workspace text source is not a regular file")
    before = path.stat()
    if request.json_pointer is not None and before.st_size > MAX_JSON_BYTES:
        return _error("json_input_too_large", "Use text windows or a managed analysis program for this file.",
                      path=relative_workspace_path(path), size_bytes=before.st_size)
    limit = request.max_chars
    if compact_enabled():
        limit = min(limit if "max_chars" in request.model_fields_set else DEFAULT_TEXT_CHARS, MAX_RESPONSE_BYTES)
    hasher = hashlib.sha256()
    if request.json_pointer is not None:
        # One bounded buffer supplies both the digest and the selected values.
        with path.open("rb") as handle:
            raw = handle.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            return _error("json_input_too_large", "JSON grew beyond the parse limit.")
        hasher.update(raw)
        try:
            parsed = json.loads(raw)
        except (ValueError, UnicodeError):
            return _error("invalid_json", "The selected source is not valid JSON.", path=relative_workspace_path(path))
        selection = None
    else:
        decoder = codecs.getincrementaldecoder("utf-8")()
        chunks = []
        captured = 0
        total = 0
        line_number = 1
        selection_start = None
        selection_end = None
        lines = request.start_line is not None or request.end_line is not None
        with path.open("rb") as handle:
            while True:
                raw_chunk = handle.read(64 * 1024)
                hasher.update(raw_chunk)
                text = decoder.decode(raw_chunk, final=not raw_chunk)
                # LF defines a line; CRLF bytes/characters are retained exactly.
                parts = text.splitlines(keepends=True) if lines else [text]
                for part in parts:
                    start, end = total, total + len(part)
                    if lines:
                        eligible = line_number >= (request.start_line or 1) and (request.end_line is None or line_number <= request.end_line)
                        a, b = start, end
                    else:
                        a, b = max(start, request.offset), min(end, request.end_offset if request.end_offset is not None else end)
                        eligible = b > a
                    if eligible and b > a:
                        if selection_start is None: selection_start = a
                        selection_end = b
                        if captured < limit:
                            fragment = part[a - start:b - start][:limit - captured]
                            chunks.append(fragment); captured += len(fragment)
                    total = end
                    line_number += part.count("\n")
                if not raw_chunk: break
        selection = "".join(chunks)
        selection_start = selection_start if selection_start is not None else total
        selection_end = selection_end if selection_end is not None else selection_start
    after = path.stat()
    if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
        return _error("file_changed", "Source changed while reading; request a fresh version.", path=relative_workspace_path(path))
    digest = hasher.hexdigest()
    if request.expected_sha256 and digest != request.expected_sha256:
        return _error("file_version_mismatch", "Source differs from expected_sha256; do not concatenate versions.",
                      path=relative_workspace_path(path), sha256=digest)
    base = {"status": "success", "path": relative_workspace_path(path), "size_bytes": after.st_size,
            "sha256": digest, "encoding": "utf-8"}
    if request.json_pointer is not None:
        return _read_json(request, parsed, base)

    def output(content):
        end = selection_start + len(content)
        complete = end >= selection_end
        value = {**base, "content": content, "offset": selection_start, "end_offset": end,
                 "selection_end_offset": selection_end, "total_chars": total,
                 "complete": complete, "truncated": not complete, "next_offset": end if not complete else None}
        if not complete:
            value["next_tool_calls"] = [{"tool": "read_workspace_text", "arguments": {"request": {
                "path": base["path"], "offset": end, "end_offset": selection_end,
                "max_chars": limit, "expected_sha256": digest}}}]
        return value
    value = output(selection)
    if compact_enabled() and response_bytes(value) > MAX_RESPONSE_BYTES:
        lo, hi = 0, len(selection)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if response_bytes(output(selection[:mid])) <= MAX_RESPONSE_BYTES: lo = mid
            else: hi = mid - 1
        value = output(selection[:lo])
    if not value["complete"] and not value["content"]:
        return _error("read_metadata_too_large", "Use a shorter relative path or selector.")
    return value


def _read_json(request, parsed, base):
    try:
        value = _select(parsed, request.json_pointer)
    except (KeyError, IndexError):
        return _error("json_pointer_not_found", "No value exists at this JSON Pointer.", **{k:v for k,v in base.items() if k!='status'}, json_pointer=request.json_pointer)
    pointer = request.json_pointer
    common = {**base, "json_pointer": pointer, "value_type": _type(value)}
    if isinstance(value, list):
        if request.start_index > len(value):
            return _error("index_out_of_range", "start_index is past the selected array.")
        end = min(len(value), request.start_index + request.max_items)
        def result(n):
            response = {**common, "value": value[request.start_index:n], "start_index": request.start_index,
                        "end_index": n, "total_items": len(value), "complete": n == len(value),
                        "next_index": n if n < len(value) else None}
            if n < len(value):
                response["next_tool_calls"] = [{"tool":"read_workspace_text", "arguments":{"request":{
                    "path":base["path"], "json_pointer":pointer, "start_index":n,
                    "max_items":request.max_items, "expected_sha256":base["sha256"]}}}]
            return response
        while end > request.start_index and response_bytes(result(end)) > MAX_RESPONSE_BYTES:
            end -= 1
        if end == request.start_index and end < len(value):
            child = pointer + "/" + str(end)
            return {**_error("json_item_too_large", "Read this element using its child pointer."),
                    "path":base["path"], "sha256":base["sha256"], "json_pointer":child,
                    "next_tool_calls":[{"tool":"read_workspace_text","arguments":{"request":{
                        "path":base["path"],"json_pointer":child,"expected_sha256":base["sha256"]}}}]}
        return result(end)
    response = {**common, "value": value, "complete": True}
    if response_bytes(response) <= MAX_RESPONSE_BYTES:
        return response
    if isinstance(value, dict):
        from .response_pages import create_page
        fields = [{"name":k, "json_pointer":pointer + "/" + pointer_part(k), "value_type":_type(v)} for k,v in value.items()]
        return create_page({**common, "value":value, "complete":True}, tool="read_workspace_text",
                           base={**common, "complete":False, "selection_mode":"field_directory"},
                           collections={"fields":fields})
    return {**_error("json_value_too_large", "Use text windows or a managed analysis program for this scalar."),
            "path":base["path"],"sha256":base["sha256"],"json_pointer":pointer,"value_type":_type(value)}

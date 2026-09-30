"""Resource-bounded reads of registered evidence, without executing artifacts."""
from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

import ijson
from jsonpath_ng import parse

from evaluation.provenance.evidence_archive import resolve_reference

MAX_PARSE_BYTES = 128 * 1024 * 1024


def normalize_selection(request, *, allow_jsonpath=True):
    """Use one location syntax for reads and citations; never discard a location."""
    value = dict(request)
    for name in ("pointer", "selector"):
        if name in value and not isinstance(value[name], str):
            raise ValueError(f"{name} must be a string")
    if "pointer" in value and "selector" in value and value["pointer"] != value["selector"]:
        raise ValueError("pointer and selector conflict")
    location = value.get("pointer", value.get("selector"))
    if location is None:
        return value
    if "pointer" not in value and location.startswith("$") and allow_jsonpath:
        return value
    if (location and not location.startswith("/")) or re.search(r"~(?![01])", location):
        raise ValueError("location must be an RFC 6901 JSON Pointer; JSONPath is only supported for file selectors")
    value.pop("selector", None)
    value["pointer"] = location
    return value


class PointerLookupError(ValueError):
    def __init__(self, pointer, parent, *, keys=None, length=None):
        self.details = {"reason": "pointer_not_found", "pointer": pointer, "parent_pointer": parent}
        if keys is not None:
            self.details["available_keys"] = [str(k)[:80] for k in keys[:20]]
        if length is not None:
            self.details["array_length"] = length
        super().__init__("JSON Pointer does not exist: " + json.dumps(self.details, ensure_ascii=False))


def _open(path, mode):
    return gzip.open(path, mode) if path.suffix == ".gz" else open(path, mode)


class _LimitedReader:
    def __init__(self, stream):
        self.stream, self.remaining = stream, MAX_PARSE_BYTES

    def read(self, size=-1):
        data = self.stream.read(min(size if size >= 0 else self.remaining + 1, self.remaining + 1))
        self.remaining -= len(data)
        if self.remaining < 0:
            raise ValueError("structured evidence exceeds parser byte limit")
        return data


def json_projection(index, ref, *, pointer="", max_chars=12000, array_start=0, array_count=128, action=False):
    """Project an RFC 6901 subtree using a streaming parser, keeping omissions explicit."""
    normalize_selection({"pointer": pointer})
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (max_chars, array_start, array_count)) or not 1 <= max_chars <= 100000 or array_start < 0 or not 1 <= array_count <= 1000:
        raise ValueError("invalid JSON read limits")
    path = resolve_reference(index, ref)
    omitted, found, remaining = [], False, max_chars
    selection = None
    nearest = {"parent": "", "keys": None, "length": None}

    def note(at, reason, **facts):
        if len(omitted) < 64:
            omitted.append({"pointer": at, "reason": reason, **facts})

    def skip(first, tokens):
        depth = int(first[0] in {"start_map", "start_array"})
        while depth:
            event, _ = next(tokens)
            depth += (event in {"start_map", "start_array"}) - (event in {"end_map", "end_array"})

    def visit(first, tokens, at, retain, depth=0):
        nonlocal remaining, found, selection
        selected = at == pointer
        retain = retain or selected
        if selected:
            found = True
        kind, value = first
        if not retain and not pointer.startswith(at + "/"):
            skip(first, tokens)
            return None
        if depth > 32 and not retain:
            raise ValueError("JSON selector exceeds parser depth limit")
        if retain and (remaining < 128 or depth > 32):
            skip(first, tokens)
            note(at, "projection_limit")
            return {"$ref": ref, "pointer": at, "omitted": True}
        if kind == "start_map":
            value, count = {}, 0
            seeking = not retain and pointer.startswith(at + "/")
            if seeking:
                nearest.update(parent=at, keys=[], length=None)
            for event, key in tokens:
                if event == "end_map":
                    break
                if event != "map_key":
                    raise ValueError("invalid JSON object event")
                if seeking and nearest["parent"] == at and len(nearest["keys"]) < 20:
                    nearest["keys"].append(key)
                child = at + "/" + key.replace("~", "~0").replace("/", "~1")
                first_child = next(tokens)
                # Inventories remain indexed, and can be read explicitly.
                inventory = action and pointer == "" and key in {"output_artifacts", "artifacts", "artifact_inventory"}
                if inventory or (retain and count >= 96):
                    skip(first_child, tokens)
                    if not inventory:
                        note(child, "object_fields_omitted")
                    else:
                        value[key] = {"inventory_ref": ref, "pointer": child}
                    continue
                projected = visit(first_child, tokens, child, retain, depth + 1)
                if retain:
                    value[key] = projected
                    remaining -= len(key) + 4
                count += 1
        elif kind == "start_array":
            values, count = [], 0
            if not retain and pointer.startswith(at + "/"):
                nearest.update(parent=at, keys=None, length=0)
            start = array_start if selected else 0
            limit = array_count if selected else 128
            for event, item in tokens:
                if event == "end_array":
                    break
                child = at + "/" + str(count)
                if retain and (count < start or count >= start + limit or remaining < 128):
                    skip((event, item), tokens)
                else:
                    projected = visit((event, item), tokens, child, retain, depth + 1)
                    if retain:
                        values.append(projected)
                count += 1
            if nearest["parent"] == at and nearest["length"] is not None:
                nearest["length"] = count
            value = values
            if retain and (start or len(values) < count):
                note(at, "array_page", length=count, start=start, included=len(values))
                value = {"$ref": ref, "pointer": at, "length": count, "start": start, "items": values}
        elif retain:
            if isinstance(value, str) and len(value) > min(4096, remaining):
                note(at, "string_truncated")
                value = value[:min(4096, remaining)]
            remaining -= len(json.dumps(value, ensure_ascii=False)) + 1
        if selected:
            selection = value
        return value

    try:
        with _open(path, "rb") as stream:
            tokens = iter(ijson.basic_parse(_LimitedReader(stream), use_float=True))
            visit(next(tokens), tokens, "", False)
            if next(tokens, None) is not None:
                raise ValueError("extra JSON content")
    except (ijson.JSONError, StopIteration) as exc:
        raise ValueError(f"Invalid JSON evidence: {exc}") from exc
    if not found:
        raise PointerLookupError(pointer, **nearest)
    if action and isinstance(selection, dict) and isinstance(selection.get("action_result"), dict):
        selection = selection["action_result"]
    return {"ref": ref, "pointer": pointer, "value": selection, "omissions": omitted,
            "truncated": bool(omitted), "projection": "structured_json", "full_result_ref": ref}


def read_evidence_excerpt(index, ref, *, start=0, max_chars=12000, start_line=None, line_count=100):
    if start < 0 or not 1 <= max_chars <= 100000 or start > MAX_PARSE_BYTES:
        raise ValueError("invalid excerpt range")
    path = resolve_reference(index, ref)
    if start_line is not None and (start or not isinstance(start_line, int) or isinstance(start_line, bool)
            or not 1 <= start_line <= 1000000 or not isinstance(line_count, int) or not 1 <= line_count <= 1000):
        raise ValueError("invalid line range")
    with _open(path, "rb") as stream:
        if b"\0" in stream.read(1024):
            raise ValueError("binary evidence requires a format-specific reader")
    with _open(path, "rt") as stream:
        if start_line is not None:
            for _ in range(start_line - 1):
                skipped = stream.readline(MAX_PARSE_BYTES - start + 1)
                start += len(skipped)
                if start > MAX_PARSE_BYTES:
                    raise ValueError("text evidence exceeds parser byte limit")
                if not skipped:
                    break
        left = start
        while left and start_line is None:
            chunk = stream.read(min(left, 65536))
            if not chunk:
                break
            left -= len(chunk)
        if start_line is None:
            content = stream.read(max_chars)
        else:
            chunks, remaining = [], max_chars
            for _ in range(line_count):
                if remaining == 0:
                    break
                chunk = stream.readline(remaining)
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            content = "".join(chunks)
        more = bool(stream.read(1))
    result = {"ref": ref, "character_start": start, "content": content, "truncated": more or start > 0,
              "next_character_start": start + len(content) if more else None}
    if start_line is not None:
        result.update(line_start=start_line, line_end=start_line + max(0, len(content.splitlines()) - 1),
                      final_line_may_be_partial=more and not content.endswith("\n"))
    if Path(ref).suffix.lower() in {".csv", ".tsv"}:
        with _open(path, "rt") as stream:
            header = stream.readline(min(4096, max_chars))
        result["table_context"] = {"header_excerpt": header, "header_may_be_partial": not header.endswith("\n"),
                                   "representation": "raw text lines; quoted records may span multiple lines"}
    if Path(ref).suffix.lower() == ".xyz":
        result["structure_context"] = {"frame_identity": "not_parsed", "representation": "raw lines; no complete trajectory is asserted"}
    return result


def read_registered_evidence(index, request):
    """Only registered paths and bounded, declarative selectors are accepted."""
    request = normalize_selection(request)
    ref = request["ref"]
    path = resolve_reference(index, ref)
    selector = request.get("pointer", request.get("selector"))
    limit = request.get("max_chars", 12000)
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100000:
        raise ValueError("invalid read size")
    if selector is not None:
        if not isinstance(selector, str):
            raise ValueError("selector must be a string")
        if selector.startswith("$"):
            # JSONPath on arbitrary multi-match documents is bounded separately.
            with _open(path, "rb") as stream:
                raw = stream.read(2 * 1024 * 1024 + 1)
            if len(raw) > 2 * 1024 * 1024:
                raise ValueError("use a JSON Pointer for large JSON")
            matches = parse(selector).find(json.loads(raw))
            if not matches:
                raise ValueError("JSONPath does not exist")
            value = [{"path": str(m.full_path), "value": m.value} for m in matches]
            content = json.dumps(value, ensure_ascii=False)
            if len(content) > limit:
                raise ValueError("selection exceeds read limit; request a narrower selector")
            return {"ref": ref, "selector": selector, "content": content, "truncated": False}
        value = json_projection(index, ref, pointer=selector, max_chars=max(128, limit // 2),
                                array_start=request.get("array_start", 0), array_count=request.get("array_count", 128))
        content = json.dumps(value["value"], ensure_ascii=False)
        if len(content) > limit:
            raise ValueError("projection exceeds read limit; request a narrower selector")
        return {**value, "content": content}
    return read_evidence_excerpt(index, ref, start=request.get("start", 0), max_chars=limit,
                                 start_line=request.get("start_line"), line_count=request.get("line_count", 100))

"""Size-only projections; the complete review payload remains retrievable."""
from __future__ import annotations

import copy
import json
from .evidence_reading import normalize_selection, PointerLookupError


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def pack_prompt(payload, followups, *, fits):
    view = copy.deepcopy(payload)
    # These are presentation fields, never authored rules, checks or criteria.
    paths = [("evidence", "excerpts"), ("native_events",), ("tool_events",),
             ("evidence", "jobs"), ("evidence", "native_observations"),
             ("evidence", "rule_coverage"), ("evidence", "duplicate_content_references"),
             ("evidence", "coverage")]
    prompt = encoded({**view, "followups": followups})
    for path in paths:
        if fits(prompt):
            break
        parent = view
        for key in path[:-1]:
            parent = parent.get(key, {})
        value = parent.get(path[-1])
        if not isinstance(value, (list, dict)) or not value:
            continue
        pointer = "/" + "/".join(path)
        reference = {"ref": "review/payload", "pointer": pointer}
        projection = {"total_items": len(value), "read": reference,
                      "view_status": "partially_sent", "items": list(value) if isinstance(value, list) else []}
        parent[path[-1]] = projection
        while projection["items"]:
            # Reduce monotonically, preserving task-bound and report ordering.
            projection["items"] = projection["items"][:len(projection["items"]) // 2]
            prompt = encoded({**view, "followups": followups})
            if fits(prompt):
                return prompt
        projection["view_status"] = "not_sent_retrievable"
        prompt = encoded({**view, "followups": followups})
    return prompt


def record_page(value, request):
    """Bound host metadata, including one huge record, using JSON Pointers."""
    request = normalize_selection(request, allow_jsonpath=False)
    pointer = request.get("pointer", "")
    parent = ""
    for key in pointer.split("/")[1:] if pointer else []:
        key = key.replace("~1", "/").replace("~0", "~")
        try:
            if isinstance(value, list) and (not key.isascii() or not key.isdigit() or (key != "0" and key.startswith("0"))):
                raise IndexError("invalid JSON array index")
            selected = value[int(key)] if isinstance(value, list) else value[key]
        except (IndexError, KeyError, TypeError) as exc:
            raise PointerLookupError(pointer, parent, keys=list(value)[:20] if isinstance(value, dict) else None,
                                     length=len(value) if isinstance(value, list) else None) from exc
        value = selected
        parent += "/" + key.replace("~", "~0").replace("/", "~1")
    for alias, name in (("array_start", "start"), ("array_count", "count")):
        if alias in request:
            if not isinstance(value, list):
                raise ValueError("array paging requires an array target")
            if name in request and request[name] != request[alias]:
                raise ValueError(f"{alias} and {name} conflict")
            request[name] = request.pop(alias)
    limit = request.get("max_chars", 12000)
    start, count = request.get("start", 0), request.get("count", 30)
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (limit, start, count)) or limit < 256 or start < 0 or not 1 <= count <= 1000:
        raise ValueError("host pages require max_chars >= 256, start >= 0 and count 1..1000")
    page = {"ref": request["ref"], "pointer": pointer, "value": value, "truncated": False}
    if start == 0 and (not isinstance(value, (list, dict)) or len(value) <= count) and len(json.dumps(page, ensure_ascii=False)) <= limit:
        return page
    def child(key):
        return pointer + "/" + str(key).replace("~", "~0").replace("/", "~1")
    if isinstance(value, str):
        if start >= len(value):
            page.update(value="", start=start, truncated=start > 0, next=None)
            if len(json.dumps(page, ensure_ascii=False)) <= limit:
                return page
        length = min(count if "count" in request else limit, len(value) - start)
        while length > 0:
            page.update(value=value[start:start+length], start=start, truncated=True,
                        next={**request, "start": start+length} if start+length < len(value) else None)
            if len(json.dumps(page, ensure_ascii=False)) <= limit:
                return page
            length //= 2
    elif isinstance(value, (list, dict)):
        items = list(enumerate(value)) if isinstance(value, list) else list(value.items())
        page.update(value=[] if isinstance(value, list) else {}, start=start, total_items=len(items), truncated=True)
        if start >= len(items):
            page["next"] = None
            if len(json.dumps(page, ensure_ascii=False)) <= limit:
                return page
        for key, entry in items[start:start+count]:
            compact = {"read": {**request, "pointer": child(key), "start": 0}, "view_status": "not_sent_retrievable"}
            for candidate in (entry, compact):
                result = copy.deepcopy(page)
                result["value"].append(candidate) if isinstance(value, list) else result["value"].update({key: candidate})
                position = start + len(result["value"])
                result["next"] = {**request, "start": position} if position < len(items) else None
                if len(json.dumps(result, ensure_ascii=False)) <= limit:
                    page = result
                    break
            else:
                break
        if page["value"]:
            return page
    raise ValueError("page metadata exceeds limit; increase max_chars or request a narrower pointer")

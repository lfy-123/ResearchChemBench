"""Immutable, run-scoped pages of public tool results. Reading never acknowledges jobs."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
from pathlib import Path

from .response_policy import DEFAULT_PAGE_SIZE, MAX_RESPONSE_BYTES, TARGET_RESPONSE_BYTES, response_bytes
from .workspace import workspace_root

SNAPSHOT_DIRECTORY = Path("outputs/tool_responses")
_HEX = re.compile(r"^[0-9a-f]{64}$")


def run_scope() -> str:
    return os.environ.get("RESEARCHCHEMBENCH_RUN_ID", os.environ.get("RESEARCHCHEM_MCP_RUN_ID", "workspace"))


def _encoded(value) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=True, default=str).encode("utf-8")


def pointer_part(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _path(root: Path, digest: str) -> Path:
    if not _HEX.fullmatch(digest):
        raise ValueError("invalid response snapshot identity")
    path = root / SNAPSHOT_DIRECTORY / (digest + ".json")
    for p in (root / "outputs", root / SNAPSHOT_DIRECTORY, path):
        if p.is_symlink():
            raise ValueError("response snapshot cannot use symlinks")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("response snapshot escapes workspace")
    return path


def _save(record: dict, root: Path) -> tuple[str, dict]:
    data = _encoded(record) + b"\n"
    digest = hashlib.sha256(data).hexdigest()
    path = _path(root, digest)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Publish only a complete file. An identical concurrent writer has the same bytes.
    from chemistry_toolbox.src.recovery_io import file_lock
    with file_lock(path.with_suffix(".lock")):
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError("response snapshot was modified")
        else:
            from chemistry_toolbox.src.recovery_io import atomic_json
            atomic_json(path, json.loads(data))
    return digest, {"path": str(SNAPSHOT_DIRECTORY / path.name), "sha256": digest, "json_pointer": "/body"}


def _cursor(digest: str, offsets: dict[str, int]) -> str:
    return base64.urlsafe_b64encode(_encoded({"snapshot": digest, "offsets": offsets})).decode().rstrip("=")


def _decode(cursor: str) -> dict:
    if len(cursor) > 16000:
        raise ValueError("response cursor too long")
    try:
        value = json.loads(base64.b64decode(cursor + "=" * (-len(cursor) % 4), altchars=b"-_", validate=True))
    except (ValueError, TypeError, UnicodeError) as exc:
        raise ValueError("invalid response cursor") from exc
    if not isinstance(value, dict) or set(value) != {"snapshot", "offsets"}:
        raise ValueError("invalid response cursor")
    if not isinstance(value["snapshot"], str) or not _HEX.fullmatch(value["snapshot"]):
        raise ValueError("invalid response snapshot identity")
    return value


def create_page(body: dict, *, tool: str, base: dict, collections: dict[str, list],
                root: Path | None = None, scope: str | None = None,
                page_size: int = DEFAULT_PAGE_SIZE, final_fields: dict | None = None,
                pending_fields: dict | None = None) -> dict:
    root = (root or workspace_root()).resolve()
    if not 1 <= page_size <= 100:
        raise ValueError("page_size must be between 1 and 100")
    record = {"version": 1, "scope": scope if scope is not None else run_scope(),
              "tool": tool, "body": body, "base": base, "collections": collections,
              "page_size": page_size, "final_fields": final_fields or {},
              "pending_fields": pending_fields or {}}
    digest, _ = _save(record, root)
    return _render(record, digest, {k: 0 for k in collections})


def read_page(cursor: str, *, root: Path | None = None, scope: str | None = None,
              tool: str | None = None) -> dict:
    root = (root or workspace_root()).resolve()
    token = _decode(cursor)
    path = _path(root, token["snapshot"])
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != token["snapshot"]:
        raise ValueError("response snapshot was modified")
    record = json.loads(raw)
    if record["scope"] != (scope if scope is not None else run_scope()):
        raise ValueError("response cursor belongs to a different run or role")
    if tool is not None and record["tool"] != tool:
        raise ValueError("response cursor belongs to a different tool")
    return _render(record, token["snapshot"], token["offsets"])


def _render(record: dict, digest: str, offsets: dict) -> dict:
    collections = record["collections"]
    if not isinstance(offsets, dict) or set(offsets) != set(collections):
        raise ValueError("invalid response page offsets")
    for key, offset in offsets.items():
        if type(offset) is not int or not 0 <= offset <= len(collections[key]):
            raise ValueError("invalid response page offset")
    ref = {"path": str(SNAPSHOT_DIRECTORY / (digest + ".json")), "sha256": digest, "json_pointer": "/body"}
    next_offsets = dict(offsets)
    page = {**record["base"], **{k: [] for k in collections}}

    def envelope():
        pending = sum(len(v) - next_offsets[k] for k, v in collections.items())
        value = {**page, **(record["pending_fields"] if pending else record["final_fields"]),
                 "response_profile": "compact_v1", "response_tool": record["tool"], "response_snapshot": digest,
                 "full_response_ref": ref, "pending_result_count": pending,
                 "page_complete": pending == 0,
                 "pagination": {k: {"offset": offsets[k], "returned": next_offsets[k] - offsets[k],
                                      "total": len(v)} for k, v in collections.items()}}
        value["next_cursor"] = _cursor(digest, next_offsets) if pending else None
        if pending:
            value["recommended_action"] = "read_remaining_response_pages"
            value["next_tool_calls"] = [{"tool": "read_tool_response", "arguments": {"request": {"cursor": value["next_cursor"]}}}]
        return value

    count = 0
    for key, items in collections.items():
        while next_offsets[key] < len(items) and count < record["page_size"]:
            item = items[next_offsets[key]]
            page[key].append(item)
            next_offsets[key] += 1
            size = response_bytes(envelope())
            if size > TARGET_RESPONSE_BYTES and count:
                page[key].pop(); next_offsets[key] -= 1
                break
            if size > MAX_RESPONSE_BYTES:
                page[key].pop(); next_offsets[key] -= 1
                if not count:
                    # Large profiles/manifest entries are valid requests. Keep their
                    # identity and status, and give a verifiable full-item reference.
                    pointer = "/collections/" + pointer_part(key) + "/" + str(next_offsets[key])
                    item_ref = {**ref, "json_pointer": pointer}
                    essential = ("entity_id","job_id","batch_id","item_id","operation_id","submission_key",
                                 "request_digest","action_id","backend_id","name","path","source_path",
                                 "status","state","valid","format","semantic_type","sha256","result_state","result_receipt_id")
                    small = {k:item[k] for k in essential if isinstance(item,dict) and k in item}
                    if isinstance(item,dict) and item.get("execution_feedback"):
                        feedback=item["execution_feedback"]
                        small["execution_feedback"]={k:feedback[k] for k in ("job_status","action_status","process_status",
                            "software_status","convergence_status","scientific_validation_status","result_state","result_receipt_id") if k in feedback}
                        if feedback.get("diagnostic"):
                            from .response_projection import diagnostic_summary
                            small["execution_feedback"]["diagnostic"]=diagnostic_summary(feedback["diagnostic"])
                    if isinstance(item,dict) and item.get("error"):
                        from .response_projection import diagnostic_summary
                        small["error"]=diagnostic_summary(item["error"])
                    small.update(inline_complete=False,item_ref=item_ref)
                    page[key].append(small);next_offsets[key]+=1
                    if response_bytes(envelope())<=MAX_RESPONSE_BYTES:
                        count+=1
                        continue
                    page[key].pop();next_offsets[key]-=1
                    return {"status": "failed", "error": {"code": "response_identity_too_large", "category":"result_delivery",
                            "message": "Result identity exceeds the transport budget; read the full item reference."},
                            "full_response_ref":ref,"item_ref":item_ref}
                break
            count += 1
        if count >= record["page_size"] or next_offsets[key] < len(items):
            break
    value = envelope()
    if response_bytes(value) > MAX_RESPONSE_BYTES:
        return {"status": "failed", "error": {"code": "response_metadata_too_large", "category":"result_delivery",
                "message": "Read the full response through the referenced JSON fields."}, "full_response_ref": ref,
                "next_tool_calls": [{"tool": "read_workspace_text", "arguments": {"request": {
                    "path": ref["path"], "json_pointer": "/body", "expected_sha256": digest}}}]}
    return value

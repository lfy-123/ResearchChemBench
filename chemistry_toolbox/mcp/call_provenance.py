"""Out-of-band call attribution; never part of chemical inputs or results."""
from contextvars import ContextVar
import os
import re


CALL_PROVENANCE = ContextVar("tool_call_provenance", default=None)
META_KEY = "researchchembench/call_origin"
CALLER_ENV = "RESEARCHCHEMBENCH_TOOL_CALLER"
_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,160}$")


def request_provenance(meta, request_id):
    # Only an adapter-owned stdio server accepts adapter attribution. A direct
    # client cannot label its own failed calls as internal via MCP metadata.
    if os.environ.get(CALLER_ENV) != "adapter":
        return {"origin": "client" if request_id is not None else "unknown"}
    value = meta.get(META_KEY) if isinstance(meta, dict) else None
    if not isinstance(value, dict) or not isinstance(value.get("origin"), str) or value["origin"] not in {"client", "adapter_internal"}:
        return {"origin": "unknown"}
    if not isinstance(value.get("host_call_id"), str) or not _ID.fullmatch(value["host_call_id"]):
        return {"origin": "unknown"}
    result = {"origin": value["origin"], "host_call_id": value["host_call_id"]}
    for key in ("client_call_id", "client_tool", "role"):
        if isinstance(value.get(key), str) and _ID.fullmatch(value[key]):
            result[key] = value[key]
    if result["origin"] == "client" and "client_call_id" not in result:
        return {"origin": "unknown"}
    return result

"""Run-frozen presentation policy; independent of execution feedback semantics."""
from __future__ import annotations

import json
import os

PROFILE_ENV = "RESEARCHCHEMBENCH_TOOL_RESPONSE_PROFILE"
PROFILES = {"legacy", "compact_v1"}
TARGET_RESPONSE_BYTES = 16 * 1024
MAX_RESPONSE_BYTES = 32 * 1024
DEFAULT_TEXT_CHARS = 4000
DEFAULT_PAGE_SIZE = 25

COMPACT_READING_INSTRUCTIONS = """## Reading compact tool results
Keep complete computational data in benchmark files/Artifacts. Pass references directly
to downstream tools instead of reconstructing arrays from displayed pages. For numerical
comparisons, use managed analysis to read complete data and report the evidence you choose
with source references. Inspect summaries first, then the needed fields and contracts.

Tool responses can be paginated. An empty remaining_job_ids list means computations
ended; pending_result_count/next_cursor can still identify unread result pages.
For next_cursor, follow read_tool_response until page_complete. Text/JSON windows
use their returned next_tool_calls until complete. Inspect failures/partial results
before choosing the next computation. Continuation pages never resubmit or wait.
When selecting data to display, retain its identity, status/error, completeness,
returned range/total and continuation/source references. complete=false means partial
data, not a smaller dataset; never discard paging metadata while displaying only value.
page_complete covers directory pages, not all referenced values. Expand item_ref,
full_response_ref or field-directory pointers when needed. After truncated output,
retrieve missing evidence through these references without resubmitting computations.
Use read_workspace_text with JSON Pointer or line/character ranges and the returned
expected_sha256 for the same snapshot. Array paging requires a JSON Pointer and index;
text uses character or line ranges. Prefer display-size/depth defaults; any override
must follow the actual schema, including field dependencies. Do not guess larger limits.

Reuse already-read contracts while their catalog version is unchanged; reread whenever
needed for verification. Missing, null, non-converged and failed results are distinct.
Keep source identities, units, signs, methods, charge/spin, geometries and uncertainty.
Scientific evidence selection and changes of method remain the agent's decision;
presentation guidance never changes computation status or repairs failed calculations.
After disconnection or history compression, list_execution_jobs with
include_result_facts=true returns public result-receipt/scalar references. Restore
relevant method/state/evidence from those references; do not infer scientific success
from a terminal job or a successful tool call. Acknowledge only results you observed.
"""

MCP_DISPLAY_EXAMPLE = """function showMcp(result) {
  const {content = [], ...metadata} = result;
  if (Object.keys(metadata).length) text(metadata);
  for (const block of content) {
    if (block.type === "text") text(block.text);
    else if (block.type === "image") image(block);
    else if (block.type === "audio") audio(block);
    else text(block);
  }
}"""

CODE_MODE_READING_INSTRUCTIONS = """## Display in runtimes with code mode
The following applies only when the runtime exposes code mode and these display helpers.
Emit MCP text content directly instead of JSON-stringifying the outer CallToolResult
again. Preserve metadata, errors and every content block. Example:
""" + MCP_DISPLAY_EXAMPLE + """

Independent calls may run together, but printing several complete contracts or large
results in one exec can truncate their combined output. Keep a large complete display
separate from other large displays; keep computations parallel. Use existing references
and readers for the evidence you need. Do not increase display limits just to dump raw data.
"""


def context_reading_instructions() -> str:
    """One public text for all tasks; runtime-specific examples are conditional."""
    return COMPACT_READING_INSTRUCTIONS.rstrip() + "\n\n" + CODE_MODE_READING_INSTRUCTIONS.strip()


def response_profile() -> str:
    value = os.environ.get(PROFILE_ENV, "legacy")
    if value not in PROFILES:
        raise ValueError("unsupported tool_response_profile")
    return value


def compact_enabled() -> bool:
    return response_profile() == "compact_v1"


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=True, default=str)


def response_bytes(value) -> int:
    """Count the JSON text AND its MCP text-content escaping, with envelope room."""
    text = json_text(value)
    envelope = {"content": [{"type": "text", "text": text}]}
    return len(json_text(envelope).encode("utf-8")) + 256

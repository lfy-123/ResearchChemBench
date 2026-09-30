"""Read and normalize benchmark Chemistry MCP trace events."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.catalog import action_specs
from .execution_facts import execution_metrics

SUCCESSFUL_TOOL_STATUSES = {"success", "partial_success"}
CATALOG_DISCOVERY_TOOLS = {
    "list_action_domains",
    "search_actions",
    "inspect_action",
    "inspect_backend",
    "search_resources",
    "inspect_resource",
}
ACTION_BATCH_SUPERVISION_TOOLS = {"wait_execution_events"}
INTERPRETER_SHELL_PATTERN = re.compile(
    r"(?:^|[;&|()\n]\s*)(python(?:3(?:\.\d+)?)?|pypy3?|rscript|julia)\b",
    re.IGNORECASE,
)


def canonical_tool_trace_metadata(workspace: Path) -> dict[str, Any] | None:
    path = workspace / "_tool_trace.jsonl"
    if not path.is_file():
        return None
    payload = path.read_bytes()
    lines = payload.decode("utf-8", errors="replace").splitlines()
    event_count = 0
    invalid_line_count = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            invalid_line_count += 1
            continue
        if isinstance(value, dict):
            event_count += 1
        else:
            invalid_line_count += 1
    return {
        "path": "_tool_trace.jsonl",
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size_bytes": len(payload),
        "line_count": len(lines),
        "event_count": event_count,
        "invalid_line_count": invalid_line_count,
        "authoritative": True,
    }


def load_tool_trace(workspace: Path, *, strict: bool = False) -> list[dict[str, Any]]:
    path = workspace / "_tool_trace.jsonl"
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            if strict:
                raise ValueError(
                    f"Malformed canonical tool trace at {path}:{line_number}: {exc}"
                ) from exc
            continue
        if isinstance(value, dict):
            events.append(value)
        elif strict:
            raise ValueError(
                f"Canonical tool trace at {path}:{line_number} is not a JSON object"
            )
    return events


def load_native_agent_trace(workspace: Path) -> list[dict[str, Any]]:
    """Native operations are observations; managed MCP retains its own authority."""
    from .agent_events import load_agent_events
    return [event for event in load_agent_events(workspace)
            if event["kind"] == "native_tool" and event.get("phase") == "completed"]


def normalized_tool_calls(events: list[dict[str, Any]], *, successful_only: bool = True) -> list[dict]:
    calls: list[dict] = []
    for event in events:
        if successful_only and event.get("status") not in SUCCESSFUL_TOOL_STATUSES:
            continue
        name = event.get("tool")
        arguments = event.get("arguments", {})
        if name:
            calls.append({str(name): arguments if isinstance(arguments, dict) else {}})
    return calls


def _event_result(
    event: dict[str, Any], *, workspace: str | Path | None = None
) -> dict[str, Any]:
    if workspace is not None and isinstance(event.get("result_path"), str):
        result_path = Path(workspace).resolve() / str(event["result_path"])
        if result_path.is_file():
            try:
                saved = json.loads(result_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                saved = None
            if isinstance(saved, dict):
                inner = saved.get("result")
                return inner if isinstance(inner, dict) else saved
    value = event.get("result_preview")
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _job_context_metrics(
    events: list[dict[str, Any]], *, workspace: str | Path | None = None
) -> dict[str, int]:
    submissions = [
        _event_result(event, workspace=workspace)
        for event in events
        if event.get("tool") == "submit_analysis_program"
    ]
    compliance = [
        result.get("job_context_compliance")
        for result in submissions
        if isinstance(result.get("job_context_compliance"), dict)
    ]
    statuses = [str(item.get("status") or "unknown") for item in compliance]
    return {
        "analysis_program_submission_count": len(submissions),
        "job_context_audited_job_count": len(compliance),
        "job_context_import_count": sum(
            bool(item.get("job_context_imported")) for item in compliance
        ),
        "job_context_compliant_job_count": statuses.count("compliant"),
        "job_context_partial_job_count": statuses.count("partial"),
        "job_context_bypass_count": statuses.count("bypassed"),
        "job_context_not_adopted_count": statuses.count("not_adopted"),
    }


def _unmanaged_interpreter_shell_metrics(workspace: str | Path | None) -> dict[str, int]:
    if workspace is None:
        return {
            "unmanaged_interpreter_shell_call_count": 0,
            "unmanaged_python_shell_call_count": 0,
            "unmanaged_other_interpreter_shell_call_count": 0,
        }
    interpreter_calls = 0
    python_calls = 0
    for event in load_native_agent_trace(Path(workspace)):
        if str(event.get("tool") or "").casefold() not in {"bash", "shell"}:
            continue
        arguments = event.get("arguments") if isinstance(event.get("arguments"), dict) else {}
        command = arguments.get("command") or arguments.get("cmd")
        if not isinstance(command, str):
            continue
        match = INTERPRETER_SHELL_PATTERN.search(command.strip())
        if match is None:
            continue
        interpreter_calls += 1
        if match.group(1).casefold().startswith(("python", "pypy")):
            python_calls += 1
    return {
        "unmanaged_interpreter_shell_call_count": interpreter_calls,
        "unmanaged_python_shell_call_count": python_calls,
        "unmanaged_other_interpreter_shell_call_count": interpreter_calls - python_calls,
    }


def _discovery_metrics(
    events: list[dict[str, Any]], *, workspace: str | Path | None = None
) -> dict[str, int]:
    discovery_events = [
        event for event in events if event.get("tool") in CATALOG_DISCOVERY_TOOLS
    ]
    semantic_statuses: list[str] = []
    hybrid_searches = 0
    category_filter_advisories = 0
    result_bytes = 0
    inspect_result_bytes = 0
    for event in discovery_events:
        result = _event_result(event, workspace=workspace)
        retrieval = result.get("retrieval")
        if isinstance(retrieval, dict):
            if str(retrieval.get("mode") or "").casefold() == "hybrid":
                hybrid_searches += 1
            status = str(retrieval.get("semantic_status") or "").casefold()
            if status:
                semantic_statuses.append(status)
        if isinstance(result.get("category_filter_advisory"), dict):
            category_filter_advisories += 1
        encoded_size = len(
            json.dumps(result, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        result_bytes += encoded_size
        if event.get("tool") == "inspect_action":
            inspect_result_bytes += encoded_size
    return {
        "discovery_result_bytes": result_bytes,
        "inspect_action_result_bytes": inspect_result_bytes,
        "search_actions_call_count": sum(
            event.get("tool") == "search_actions" for event in discovery_events
        ),
        "hybrid_search_call_count": hybrid_searches,
        "category_filter_advisory_count": category_filter_advisories,
        "semantic_search_available_count": semantic_statuses.count("available"),
        "semantic_search_degraded_count": sum(
            status != "available" for status in semantic_statuses
        ),
    }


def process_metrics(
    events: list[dict[str, Any]], *, workspace: str | Path | None = None
) -> dict[str, Any]:
    action_ids = set(action_specs())
    scientific_action_ids = {
        action_id
        for action_id, specification in action_specs().items()
        if not specification.data_action
    }
    event_results = [_event_result(event, workspace=workspace) for event in events]
    error_codes = [
        str((result.get("error") or {}).get("code") or "")
        for result in event_results
    ]
    result_statuses = [str(result.get("status") or "").casefold() for result in event_results]
    job_context_metrics = _job_context_metrics(events, workspace=workspace)
    unmanaged_interpreter_metrics = _unmanaged_interpreter_shell_metrics(workspace)
    discovery_metrics = _discovery_metrics(events, workspace=workspace)
    wait_results = [
        result
        for event, result in zip(events, event_results)
        if event.get("tool") == "wait_execution_jobs"
    ]
    action_wait_results = [
        result
        for event, result in zip(events, event_results)
        if event.get("tool") in ACTION_BATCH_SUPERVISION_TOOLS
    ]
    supervision_results = wait_results + action_wait_results
    return {
        "tool_call_count": len(events),
        "successful_tool_calls": sum(
            event.get("status") in SUCCESSFUL_TOOL_STATUSES for event in events
        ),
        "failed_tool_calls": sum(
            event.get("status") not in SUCCESSFUL_TOOL_STATUSES for event in events
        ),
        "tool_runtime_seconds": round(
            sum(float(event.get("duration_seconds", 0) or 0) for event in events), 6
        ),
        "tools_used": [event.get("tool") for event in events],
        "catalog_discovery_call_count": sum(
            event.get("tool") in CATALOG_DISCOVERY_TOOLS for event in events
        ),
        "predefined_action_call_count": sum(
            event.get("tool") in action_ids for event in events
        ),
        "open_execution_call_count": sum(
            event.get("tool") not in CATALOG_DISCOVERY_TOOLS
            and event.get("tool") not in action_ids
            for event in events
        ),
        "execution_job_wait_call_count": len(wait_results),
        "execution_job_wait_seconds": round(
            sum(
                float(
                    result.get("wait_duration_seconds")
                    or result.get("aggregation_duration_seconds")
                    or 0
                )
                for result in wait_results
            ),
            6,
        ),
        "execution_job_wait_internal_check_count": sum(
            int(result.get("internal_check_count") or 0) for result in wait_results
        ),
        "execution_job_wait_transition_count": sum(
            len(result.get("state_transitions") or []) for result in wait_results
        ),
        "execution_job_wait_terminal_count": sum(
            len(result.get("newly_terminal_jobs") or []) for result in wait_results
        ),
        "action_batch_wait_call_count": len(action_wait_results),
        "action_batch_wait_seconds": round(
            sum(float(result.get("wait_duration_seconds") or 0) for result in action_wait_results),
            6,
        ),
        "action_batch_wait_internal_check_count": sum(
            int(result.get("internal_check_count") or 0)
            for result in action_wait_results
        ),
        "action_batch_wait_transition_count": sum(
            len(result.get("state_transitions") or [])
            for result in action_wait_results
        ),
        "action_batch_wait_terminal_count": sum(
            len(result.get("newly_terminal_items") or [])
            for result in action_wait_results
        ),
        "managed_supervision_call_count": len(supervision_results),
        "managed_supervision_internal_check_count": sum(
            int(result.get("internal_check_count") or 0)
            for result in supervision_results
        ),
        "resource_budget_rejection_count": sum(
            code in {
                "resource_budget_exceeded",
                "aggregate_resource_budget_exceeded",
            }
            for code in error_codes
        ),
        "invalid_request_count": sum(
            event.get("status") == "invalid_request" or status == "invalid_request"
            for event, status in zip(events, result_statuses)
        ),
        "request_rejection_count": sum(
            status in {"invalid_request", "unsupported", "unavailable"}
            or event.get("status") in {"invalid_request", "unsupported", "unavailable"}
            for event, status in zip(events, result_statuses)
        ),
        "preflight_rejection_count": sum(
            code.startswith(("python_", "runtime_", "staged_python_"))
            or code in {
                "external_execution_not_audited",
                "unstaged_workspace_relative_path",
            }
            or "calculation_intent_mismatch" in str(
                (result.get("error") or {}).get("message") or ""
            )
            for code, result in zip(error_codes, event_results)
        ),
        "policy_rejection_count": sum(
            code in {
                "external_execution_not_audited",
                "resource_budget_exceeded",
                "aggregate_resource_budget_exceeded",
            }
            for code in error_codes
        ),
        **execution_metrics(events, event_results, scientific_actions=scientific_action_ids,
                            action_ids=action_ids, workspace=workspace),
        **job_context_metrics,
        **unmanaged_interpreter_metrics,
        **discovery_metrics,
    }

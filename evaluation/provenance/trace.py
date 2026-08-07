"""Read and normalize benchmark Chemistry MCP trace events."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.catalog import action_specs

SUCCESSFUL_TOOL_STATUSES = {"success", "partial_success"}
CATALOG_DISCOVERY_TOOLS = {
    "list_action_domains",
    "search_actions",
    "inspect_action",
    "inspect_backend",
    "search_resources",
    "inspect_resource",
}
MANAGED_OPEN_EXECUTION_TOOLS = {
    "submit_native_job",
    "submit_analysis_program",
}
EXECUTION_JOB_OBSERVATION_TOOLS = {
    "get_execution_job",
    "wait_execution_jobs",
    "collect_execution_job",
}
ACTION_BATCH_SUPERVISION_TOOLS = {"wait_execution_events"}
SUCCESSFUL_JOB_STATES = {"success"}
FAILED_JOB_STATES = {"failed", "timeout", "cancelled"}
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
    """Load native tool events from primary and child Agent sessions.

    ``_agent_output.jsonl`` contains the primary OpenCode stream. The
    event-sourced ``_model_io.jsonl`` additionally contains child/subagent
    sessions. Merge both sources and deduplicate their shared primary events by
    OpenCode call ID.
    """

    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    model_io_path = workspace / "_model_io.jsonl"
    if model_io_path.is_file():
        for line in model_io_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict) or record.get("record_type") != "model_step":
                continue
            output = record.get("output") if isinstance(record.get("output"), dict) else {}
            parts = output.get("parts") if isinstance(output.get("parts"), list) else []
            for part in parts:
                if isinstance(part, dict) and part.get("type") == "tool":
                    candidates.append(
                        (
                            part,
                            {
                                "source": "model_io",
                                "session_id": record.get("session_id"),
                                "session_step_index": record.get("session_step_index"),
                                "message_id": record.get("message_id"),
                            },
                        )
                    )

    output_path = workspace / "_agent_output.jsonl"
    if output_path.is_file():
        for line in output_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(value, dict) or value.get("type") != "tool_use":
                continue
            part = value.get("part")
            if isinstance(part, dict) and part.get("type") == "tool":
                candidates.append(
                    (
                        part,
                        {
                            "source": "agent_output",
                            "session_id": value.get("sessionID") or part.get("sessionID"),
                            "session_step_index": None,
                            "message_id": value.get("messageID") or part.get("messageID"),
                        },
                    )
                )

    events: list[dict[str, Any]] = []
    seen_call_ids: set[str] = set()
    for part, trace_context in candidates:
        tool = str(part.get("tool") or "")
        if not tool or tool.startswith("researchchem_toolbox_"):
            # Chemistry MCP has a separate authoritative trace with validated
            # scientific status and artifact provenance.
            continue
        call_id = str(part.get("callID") or "")
        if call_id and call_id in seen_call_ids:
            continue
        if call_id:
            seen_call_ids.add(call_id)
        state = part.get("state") if isinstance(part.get("state"), dict) else {}
        metadata = (
            state.get("metadata") if isinstance(state.get("metadata"), dict) else {}
        )
        exit_code = metadata.get("exit")
        status = str(state.get("status") or "unknown")
        if (
            tool == "invalid"
            or exit_code not in {None, 0}
            or status in {"error", "failed"}
        ):
            normalized_status = "failed"
        elif status == "completed":
            normalized_status = "success"
        else:
            normalized_status = status
        timing = state.get("time") if isinstance(state.get("time"), dict) else {}
        start = timing.get("start")
        end = timing.get("end")
        duration = 0.0
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            duration = max(0.0, (float(end) - float(start)) / 1000.0)
        output = state.get("output")
        if output is None:
            output = metadata.get("output")
        event: dict[str, Any] = {
            "sequence": len(events) + 1,
            "tool": tool,
            "status": normalized_status,
            "duration_seconds": round(duration, 6),
            "arguments": state.get("input") if isinstance(state.get("input"), dict) else {},
            "result_preview": output,
            "exit_code": exit_code,
            "call_id": call_id or None,
            **trace_context,
        }
        if normalized_status == "failed":
            event["error"] = {
                "exit_code": exit_code,
                "message": str(output or state.get("error") or "native tool failed"),
            }
        events.append(event)
    return events


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


def _execution_job_states(
    events: list[dict[str, Any]], *, workspace: str | Path | None = None
) -> dict[str, str]:
    """Return the last Agent-observed state for every submitted execution job."""

    states: dict[str, str] = {}
    for event in events:
        tool = event.get("tool")
        if tool not in MANAGED_OPEN_EXECUTION_TOOLS | EXECUTION_JOB_OBSERVATION_TOOLS:
            continue
        result = _event_result(event, workspace=workspace)
        if tool == "wait_execution_jobs":
            for group in ("newly_terminal_jobs", "running_jobs", "queued_jobs"):
                for item in result.get(group) or []:
                    job_id = item.get("job_id")
                    state = item.get("status")
                    if isinstance(job_id, str) and isinstance(state, str):
                        states[job_id] = state.casefold()
            continue
        job = result.get("job") if isinstance(result.get("job"), dict) else {}
        arguments = (
            event.get("arguments") if isinstance(event.get("arguments"), dict) else {}
        )
        request = (
            arguments.get("request")
            if isinstance(arguments.get("request"), dict)
            else arguments
        )
        job_id = result.get("job_id") or job.get("job_id") or request.get("job_id")
        state = result.get("job_status") or job.get("status")
        if isinstance(job_id, str) and isinstance(state, str):
            states[job_id] = state.casefold()
    return states


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
    managed_scientific_events = [
        event
        for event in events
        if event.get("tool") in scientific_action_ids
        or event.get("tool") in MANAGED_OPEN_EXECUTION_TOOLS
    ]
    job_states = _execution_job_states(events, workspace=workspace)
    event_results = [_event_result(event, workspace=workspace) for event in events]
    error_codes = [
        str((result.get("error") or {}).get("code") or "")
        for result in event_results
    ]
    result_statuses = [str(result.get("status") or "").casefold() for result in event_results]
    managed_successes = 0
    managed_failures = 0
    managed_incomplete = 0
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
    for event in managed_scientific_events:
        if event.get("tool") not in MANAGED_OPEN_EXECUTION_TOOLS:
            if event.get("status") in SUCCESSFUL_TOOL_STATUSES:
                managed_successes += 1
            else:
                managed_failures += 1
            continue
        result = _event_result(event, workspace=workspace)
        job_id = result.get("job_id")
        state = job_states.get(str(job_id)) if job_id else None
        if (
            event.get("status") in SUCCESSFUL_TOOL_STATUSES
            and state in SUCCESSFUL_JOB_STATES
        ):
            managed_successes += 1
        else:
            managed_failures += 1
            if (
                event.get("status") in SUCCESSFUL_TOOL_STATUSES
                and state not in FAILED_JOB_STATES
            ):
                managed_incomplete += 1
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
        "managed_scientific_attempt_count": len(managed_scientific_events),
        "successful_managed_scientific_calls": managed_successes,
        "failed_managed_scientific_calls": managed_failures,
        "incomplete_managed_scientific_calls": managed_incomplete,
        "managed_scientific_tools_used": [
            event.get("tool") for event in managed_scientific_events
        ],
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
        "successful_execution_job_count": sum(
            state == "success" for state in job_states.values()
        ),
        "failed_execution_job_count": sum(
            state == "failed" for state in job_states.values()
        ),
        "timeout_execution_job_count": sum(
            state == "timeout" for state in job_states.values()
        ),
        "cancelled_execution_job_count": sum(
            state == "cancelled" for state in job_states.values()
        ),
        "backend_execution_failure_count": sum(
            event.get("status") == "failed"
            and code
            not in {
                "external_execution_not_audited",
                "resource_budget_exceeded",
                "aggregate_resource_budget_exceeded",
            }
            for event, code in zip(events, error_codes)
        )
        + sum(state in FAILED_JOB_STATES for state in job_states.values()),
        **job_context_metrics,
        **unmanaged_interpreter_metrics,
        **discovery_metrics,
    }

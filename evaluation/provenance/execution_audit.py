"""Join persisted submission facts to server request/response observations."""
from __future__ import annotations

import json
from pathlib import Path

from chemistry_toolbox.src.catalog import action_specs
from chemistry_toolbox.src.execution_states import ACTIVE_STATES, TERMINAL_STATES
from .trace import _event_result, load_tool_trace


def _client_requests(workspace):
    """Read structured provider tool requests only; never parse prose claims."""
    path = workspace / "_agent_output.jsonl"
    if not path.is_file():
        return
    seen = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        candidates = []
        item = event.get("item") or {}
        if isinstance(item, dict) and item.get("type") == "mcp_tool_call":
            candidates.append((item.get("id"), item.get("tool"), item.get("arguments")))
        part = event.get("part") or {}
        if isinstance(part, dict) and part.get("type") == "tool":
            candidates.append((part.get("callID"), part.get("tool"), (part.get("state") or {}).get("input")))
        message = event.get("message") or {}
        if isinstance(message, dict):
            for part in message.get("content") or []:
                if isinstance(part, dict) and part.get("type") == "tool_use":
                    candidates.append((part.get("id"), part.get("name"), part.get("input")))
        for call_id, tool, args in candidates:
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except ValueError:
                    continue
            if not isinstance(args, dict) or not isinstance(tool, str):
                continue
            name = tool.split("__")[-1].removeprefix("researchchem_toolbox_")
            request = args.get("request", args)
            if not isinstance(request, dict):
                continue
            key = request.get("submission_key")
            key = key if isinstance(key, str) else None
            identity = (str(call_id), name, key)
            if identity in seen:
                continue
            seen.add(identity)
            yield {"tool": name, "arguments": {**request, "submission_key": key}, "client_call_id": call_id,
                   "at": event.get("timestamp"), "evidence_source": "provider_request"}


def execution_submission_audit(workspace: Path, store) -> dict:
    """A stored response is not proof that the remote agent received it."""
    accepted = {item["submission_key"]: item for item in store.list_submissions()}
    jobs = {item["entity_id"]: item for item in store.list_jobs()}
    completed = {event.get("sequence"): event for event in load_tool_trace(workspace)}
    calls, malformed = {}, 0
    path = workspace / "_tool_call_events.jsonl"
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError("not an event object")
                if event.get("phase") == "started":
                    calls[event["sequence"]] = event
            except (ValueError, KeyError, TypeError):
                malformed += 1
    # Older runs have completed-call records but no start journal.
    for sequence, event in completed.items():
        calls.setdefault(sequence, {**event, "at": event.get("started_at")})
    tools = set(action_specs()) | {
        "submit_native_job", "submit_analysis_program", "submit_action_batch_async",
        "execute_action", "submit_action_batch",
    }
    server_keys = set()
    for event in calls.values():
        args = event.get("arguments") or {}
        if not isinstance(args, dict):
            continue
        request = args.get("request", args)
        if event.get("tool") in tools and isinstance(request, dict):
            key = request.get("submission_key")
            if isinstance(key, str):
                server_keys.add(key)
    for index, event in enumerate(_client_requests(workspace)):
        if event["tool"] in tools and event["arguments"].get("submission_key") not in server_keys:
            calls[f"client_{index}"] = event
    attempts = []
    for sequence, event in calls.items():
        if event.get("tool") not in tools:
            continue
        args = event.get("arguments") or {}
        if not isinstance(args, dict):
            continue
        request = args.get("request", args)
        if not isinstance(request, dict):
            continue
        key = request.get("submission_key")
        key = key if isinstance(key, str) else None
        receipt = accepted.get(key)
        finished = completed.get(sequence)
        result = _event_result(finished, workspace=workspace) if finished else {}
        response_receipt = result.get("receipt") or {}
        if not isinstance(response_receipt, dict):
            response_receipt = {}
        confirmed_response = bool(receipt and response_receipt.get("receipt_id") == receipt["receipt_id"])
        if receipt:
            outcome = "accepted_response_recorded" if confirmed_response else "accepted_response_unconfirmed"
        elif finished and finished.get("status") not in {"success", "partial_success", "cancelled"}:
            outcome = "rejected"
        else:
            outcome = "acceptance_unconfirmed"
        attempts.append({"sequence": sequence, "tool": event["tool"], "submission_key": key,
                         "evidence_source": event.get("evidence_source", "server_request"),
                         "request_started_at": event.get("at"), "outcome": outcome,
                         "entity_id": receipt["entity_id"] if receipt else result.get("job_id") or result.get("batch_id"),
                         "accepted_at": receipt["accepted_at"] if receipt else None,
                         "response_prepared_at": result.get("response_prepared_at"),
                         "server_response_recorded": confirmed_response})
    facts = []
    for receipt in accepted.values():
        job = jobs.get(receipt["entity_id"], {})
        facts.append({**receipt, "execution_state": job.get("state", "unknown")})
    return {"accepted_submission_count": len(facts), "request_attempt_count": len(attempts),
            "accepted_response_unconfirmed_count": sum(a["outcome"] == "accepted_response_unconfirmed" for a in attempts),
            "unconfirmed_request_count": sum(a["outcome"] == "acceptance_unconfirmed" for a in attempts),
            "active_submission_count": sum(f["execution_state"] in ACTIVE_STATES for f in facts),
            "terminal_submission_count": sum(f["execution_state"] in TERMINAL_STATES for f in facts),
            "malformed_call_event_count": malformed, "accepted_submissions": facts, "request_attempts": attempts,
            "evidence_boundary": "Database receipts establish acceptance. Server traces establish response persistence, not client receipt. Agent narrative is not execution evidence."}

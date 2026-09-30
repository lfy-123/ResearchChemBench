"""Identity-based execution accounting, separate from tool transport outcomes."""
from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.src.execution_states import ACTIVE_STATES, BLOCKED_STATES, KNOWN_STATES, TERMINAL_STATES

OPEN_SUBMISSIONS = {"submit_native_job", "submit_analysis_program"}
BATCH_SUBMISSIONS = {"submit_action_batch", "submit_action_batch_async"}
OBSERVATIONS = {"get_execution_job", "wait_execution_jobs", "collect_execution_job", "lookup_execution_submission", "wait_execution_events"}
REJECTIONS = {"invalid_request", "unsupported", "unavailable", "rejected", "declined", "recovery_blocked"}


def _dict(value):
    return value if isinstance(value, dict) else {}


def _records(value):
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _identifier(value):
    return value if isinstance(value, str) and value else None


def _action_id(value):
    return _identifier(value.get("action_id") if isinstance(value, dict) else value)


def _state(value):
    value = str(value or "unknown").casefold()
    value = {"complete": "success", "completed": "success", "error": "failed", "failure": "failed", "partial": "partial_success"}.get(value, value)
    return value if value in KNOWN_STATES else "unknown"


def _category(state):
    if state == "success":
        return "success"
    if state == "partial_success":
        return "partial"
    if state in TERMINAL_STATES:
        return "failed"
    if state in ACTIVE_STATES:
        return "active"
    return "unknown"  # Reconciliation blocks cannot establish that work is running.


def execution_metrics(events, results, *, scientific_actions, action_ids, workspace=None):
    """Count each job once; batch parents are receipts, not extra calculations.

    Older batch responses without job IDs use (batch_id, item_id). When either
    a response or the read-only ledger supplies the mapping, all observations
    share the real job identity. No state is inferred from successful polling.
    """
    rows, ledger_status, ledger_error = [], "unavailable", None
    if workspace is not None:
        try:
            store = ExecutionStore.open_existing(Path(workspace))
            if store is not None:
                rows, ledger_status = store.execution_snapshot(), "available"
        except (OSError, ValueError, sqlite3.Error) as exc:
            ledger_status, ledger_error = "unreadable", f"{type(exc).__name__}: {exc}"

    aliases, batch_actions, batch_requests = {}, {}, {}
    observations, synchronous = [], []
    accepted, rejected, unconfirmed = set(), 0, []
    confirmed_keys = {_identifier(row.get("submission_key")) for row in rows} - {None}
    scientific_tools = []

    def batch_key(batch_id, item_id):
        if _identifier(batch_id) and _identifier(item_id):
            return (batch_id, item_id)
        return None

    def register_batch(batch_id, request):
        if batch_id:
            batch_requests.setdefault(batch_id, {}).update(request)
            if _action_id(request.get("action_id")):
                batch_actions[batch_id] = _action_id(request["action_id"])

    # Map ledger children before processing trace observations (including old
    # traces whose compact batch views did not contain job_id).
    for row in rows:
        request, spec = row["request"], row["spec"]
        if row["entity_type"] == "batch":
            register_batch(row["entity_id"], request)
            accepted.add(row["entity_id"])
        else:
            key = batch_key(spec.get("parent_batch") or request.get("batch_id"), request.get("item_id"))
            if key:
                aliases[key] = row["entity_id"]
            else:
                accepted.add(row["entity_id"])

    def observe(value, *, batch_id=None, item_id=None, action=None, source, top=False, scientific=False, delivered=True):
        if not isinstance(value, dict) or value.get("entity_type") == "batch":
            return False
        feedback = _dict(value.get("execution_feedback"))
        nested = _dict(value.get("result"))
        job_id = _identifier(value.get("job_id") or value.get("entity_id") or feedback.get("job_id") or nested.get("job_id"))
        key = batch_key(value.get("batch_id") or batch_id, value.get("item_id") or item_id)
        if job_id and key:
            aliases[key] = job_id
        identity = job_id or key
        if identity is None:
            return False
        explicit = value.get("job_status") or feedback.get("job_status")
        # Top-level status is the tool response, while nested job/item records
        # contain execution state. Never count collect/get success as job success.
        if explicit is None and not top:
            explicit = value.get("state") or value.get("status") or nested.get("status")
        action = value.get("action_id") or value.get("action") or nested.get("action") or feedback.get("action") or action
        action = _action_id(action)
        scientific |= (value.get("job_type") or feedback.get("job_type")) in {"native_software", "programmable_analysis", "analysis_program"}
        observations.append({"identity": identity, "state": _state(explicit), "explicit": explicit is not None,
                             "action": action, "scientific": scientific, "source": source, "delivered": delivered})
        return True

    for position, (event, result) in enumerate(zip(events, results)):
        tool = event.get("tool")
        if tool not in action_ids | OPEN_SUBMISSIONS | BATCH_SUBMISSIONS | OBSERVATIONS | {"execute_action"}:
            continue
        args = _dict(event.get("arguments"))
        request = _dict(args.get("request")) or args
        action = tool if tool in action_ids else _action_id(args.get("action_id") or request.get("action_id") or result.get("action_id"))
        scientific = tool in OPEN_SUBMISSIONS or action in scientific_actions
        receipt = _dict(result.get("receipt"))
        submission = _dict(result.get("submission"))
        batch_id = _identifier(result.get("batch_id") or args.get("batch_id"))
        if receipt.get("entity_type") == "batch" or submission.get("entity_type") == "batch":
            batch_id = batch_id or _identifier(receipt.get("entity_id") or submission.get("entity_id"))
        job_id = _identifier(result.get("job_id"))
        submission_key = _identifier(result.get("submission_key") or submission.get("submission_key") or request.get("submission_key"))
        status = str(result.get("submission_status") or result.get("status") or event.get("status") or "unknown").casefold()
        is_submission = tool in OPEN_SUBMISSIONS | BATCH_SUBMISSIONS | action_ids | {"execute_action"}
        internal_child = args.get("entrypoint") in BATCH_SUBMISSIONS
        if is_submission and not internal_child:
            if job_id or batch_id:
                accepted.add(job_id or batch_id)
                if submission_key:
                    confirmed_keys.add(submission_key)
            elif status in REJECTIONS:
                rejected += 1
            elif tool in OPEN_SUBMISSIONS | BATCH_SUBMISSIONS:
                unconfirmed.append(submission_key)
        if batch_id:
            if tool in BATCH_SUBMISSIONS:
                register_batch(batch_id, request)
            elif submission:
                register_batch(batch_id, _dict(submission.get("request")))
        if tool == "lookup_execution_submission" and submission.get("entity_id"):
            accepted.add(submission["entity_id"])
            if submission_key:
                confirmed_keys.add(submission_key)
        if scientific and is_submission:
            scientific_tools.append(tool)
        source = f"{position}:{tool}"
        found = observe(result, batch_id=batch_id, item_id=args.get("batch_item_id"), action=action,
                        source=source, top=not internal_child, scientific=scientific,
                        delivered=not internal_child)
        observe(result.get("job"), action=action, scientific=scientific, source=source + ".job")
        if submission.get("entity_type") != "batch":
            original = _dict(submission.get("request"))
            observe(submission.get("job"), action=original.get("action_id"),
                    scientific=original.get("job_type") in {"native_software", "programmable_analysis", "analysis_program"}, source=source + ".submission.job")
        for group in ("newly_terminal_jobs", "running_jobs", "queued_jobs", "held_jobs",
                      "newly_terminal_items", "running_items", "queued_items", "held_items", "items"):
            for item in _records(result.get(group)):
                observe(item, batch_id=batch_id, action=action, source=source + "." + group)
        # Request IDs establish identity, but an error from a status query does
        # not establish a failed calculation. Explicit job_status still counts.
        if not found and _identifier(request.get("job_id")):
            observe({"job_id": request["job_id"], "job_status": result.get("job_status")}, source=source, top=True)
        if scientific and tool in action_ids | {"execute_action"} and not found and not batch_id and status not in REJECTIONS:
            synchronous.append(_state(result.get("status") or event.get("status")))

    facts = {}

    def fact_for(identity):
        identity = aliases.get(identity, identity)
        # JSON-encoded pair avoids collisions between equal item IDs in batches.
        identity = "batch_item:" + json.dumps(identity, separators=(",", ":")) if isinstance(identity, tuple) else identity
        return identity, facts.setdefault(identity, {"state": "unknown", "observed_state": None,
            "trace_state": "unknown", "ledger_state": None, "scientific": False, "sources": [], "conflict": False})

    # Accepted batch items are known attempts even before the scheduler expands
    # them into jobs. Their state remains accepted until actual evidence arrives.
    for batch_id, request in batch_requests.items():
        for item in _records(request.get("items")):
            key = batch_key(batch_id, item.get("item_id"))
            if key:
                _, fact = fact_for(key)
                fact["state"] = "accepted"
                fact["scientific"] = _action_id(request.get("action_id")) in scientific_actions
    for observation in observations:
        identity = observation["identity"]
        _, fact = fact_for(identity)
        action = observation["action"] or (batch_actions.get(identity[0]) if isinstance(identity, tuple) else None)
        fact["scientific"] |= observation["scientific"] or action in scientific_actions
        if not observation["explicit"]:
            continue
        state = observation["state"]
        fact["sources"].append(observation["source"])
        if observation["delivered"]:
            fact["observed_state"] = state
        if fact["trace_state"] in TERMINAL_STATES and state not in TERMINAL_STATES:
            fact["conflict"] = True
        else:
            if fact["trace_state"] in TERMINAL_STATES and state != fact["trace_state"]:
                fact["conflict"] = True
            fact["trace_state"] = fact["state"] = state
    for row in rows:
        if row["entity_type"] == "batch":
            continue
        _, fact = fact_for(row["entity_id"])
        spec = row["spec"]
        state = _state(row["state"])
        fact["ledger_state"] = state
        fact["scientific"] |= spec.get("job_type") in {"native_software", "programmable_analysis", "analysis_program"} or _action_id(spec.get("action_id")) in scientific_actions
        fact["sources"].append("execution_ledger")
        if fact["observed_state"] is not None and fact["observed_state"] != state:
            fact["conflict"] = True
        # A delayed nonterminal snapshot cannot undo an observed terminal state.
        if fact["state"] not in TERMINAL_STATES or state in TERMINAL_STATES:
            fact["state"] = state

    # A batch may also appear in get/collect job responses. Its receipt and
    # aggregate status must never count as another scientific calculation.
    facts = {identity: fact for identity, fact in facts.items() if identity not in batch_requests}
    counts = Counter(_category(f["state"]) for f in facts.values() if f["scientific"])
    counts.update(_category(state) for state in synchronous)
    states = Counter(f["state"] for f in facts.values())
    return {
        "metrics_schema_version": "trace-metrics-3",
        "execution_ledger_status": ledger_status,
        "execution_ledger_error": ledger_error,
        "submission_accepted_count": len(accepted - set(aliases.values())),
        "submission_rejected_count": rejected,
        "submission_unconfirmed_count": sum(key not in confirmed_keys for key in unconfirmed),
        "managed_scientific_attempt_count": sum(counts.values()),
        "successful_managed_scientific_calls": counts["success"],
        "partial_managed_scientific_calls": counts["partial"],
        "failed_managed_scientific_calls": counts["failed"],
        "active_managed_scientific_calls": counts["active"],
        "unknown_managed_scientific_calls": counts["unknown"],
        "managed_scientific_tools_used": scientific_tools,
        "execution_job_count": len(facts),
        "successful_execution_job_count": states["success"],
        "partial_execution_job_count": states["partial_success"],
        "failed_execution_job_count": states["failed"],
        "rejected_execution_job_count": sum(states[s] for s in {"invalid_request", "unsupported", "unavailable"}),
        "timeout_execution_job_count": states["timeout"],
        "cancelled_execution_job_count": states["cancelled"],
        "active_execution_job_count": sum(states[s] for s in ACTIVE_STATES),
        "unknown_execution_job_count": states["unknown"] + sum(states[s] for s in BLOCKED_STATES),
        "backend_execution_failure_count": sum(states[s] for s in {"failed", "timeout", "cancelled"}) + sum(_category(s) == "failed" for s in synchronous),
        "agent_observed_job_states": {job: f["observed_state"] for job, f in facts.items() if f["observed_state"] is not None},
        "ledger_final_job_states": {job: f["ledger_state"] for job, f in facts.items() if f["ledger_state"] is not None},
        "resolved_execution_job_states": {job: f["state"] for job, f in facts.items()},
        "execution_state_conflicts": [{"job_id": job, "observed_state": f["observed_state"],
            "ledger_state": f["ledger_state"], "resolved_state": f["state"], "sources": f["sources"]}
            for job, f in facts.items() if f["conflict"]],
    }

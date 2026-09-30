"""Public, bounded execution facts. This module never retries a calculation."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
from typing import Any

from .execution_states import TERMINAL_STATES, process_status


def feedback_schema_version() -> int:
    value = int(os.environ.get("RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION", "1"))
    if value not in {1, 2}:
        raise ValueError("unsupported feedback_schema_version")
    return value


def preserve_result(result: dict, root: Path) -> dict:
    """Content-addressed public copy; repeated observation does not create files."""
    from .recovery_io import atomic_json, file_hash, file_lock
    encoded = json.dumps(result, sort_keys=True, ensure_ascii=False, default=str).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    path = root / "outputs" / "execution_results" / (digest + ".json")
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Full-result path escapes the workspace or is a symlink")
    with file_lock(path.with_suffix(".lock")):
        if not path.exists():
            atomic_json(path, result)
        expected = hashlib.sha256(encoded + b"\n").hexdigest()
        if file_hash(path) != expected:
            raise ValueError("Previously preserved full result was modified")
    return {"path": str(path.relative_to(root)), "sha256": expected,
            "media_type": "application/json", "content": "complete_action_result"}


def bounded(value: Any, *, budget: int = 16000) -> Any:
    """Bound nested UTF-8 JSON, including unexpected dictionaries and strings."""
    if len(json.dumps(value, ensure_ascii=False, default=str).encode()) <= budget:
        return value
    if isinstance(value, str):
        raw = value.encode()
        size = max(0, (budget - 100) // 2)
        return raw[:size].decode(errors="ignore") + "\n[truncated; read full result]\n" + raw[-size:].decode(errors="ignore") if size else "[truncated]"
    if isinstance(value, (list, dict)):
        items = list(value.items()) if isinstance(value, dict) else list(enumerate(value))
        kept = items[:min(12, max(1, budget // 400))]
        per_item = max(100, (budget - 400) // max(1, len(kept)))
        if isinstance(value, dict):
            result = {str(k)[:100]: bounded(v, budget=max(60, per_item - 120)) for k, v in kept}
            result["_truncated"] = {"original_items": len(items), "read_full_result": True}
            return result
        return [bounded(v, budget=per_item) for _, v in kept] + [{"_truncated": True, "original_items": len(items)}]
    return str(value)[:max(1, budget // 4)]


def error_category(error: dict, status: str = "failed") -> str:
    explicit = error.get("category")
    if explicit:
        return str(explicit)
    code = str(error.get("code") or "")
    text = str(error.get("message") or "").lower()
    if status == "cancelled" or code == "cancelled":
        return "cancelled"
    if status == "timeout" or "deadline" in code or "timeout" in code:
        return "resource_limit"
    if any(s in code for s in ("memory_limit", "resource_limit", "resource_budget")):
        return "resource_limit"
    if status == "invalid_request" or code in {"backend_input_error", "electronic_state_invalid", "missing_electronic_state"}:
        return "invalid_input"
    if status == "unsupported":
        return "unsupported"
    if status == "unavailable":
        return "environment_unavailable"
    if code.startswith("result_") or code == "action_result_missing":
        return "result_delivery"
    if code == "output_parse_failed":
        return "output_parsing"
    # Explicit native failure markers, never inferred from a mere exit code.
    if any(s in text for s in (".sccnotconverged", "scc did not converge", "scc not converged", "scf not converged", "scf failed to converge")):
        return "numerical_nonconvergence"
    if "electron" in text and any(s in text for s in ("multiplicity", "spin multiplicity")):
        return "invalid_input"
    if any(s in code for s in ("transport", "launch", "runtime_missing", "worker_invalid_json")):
        return "infrastructure"
    return "unknown"


def repair_advice(category: str) -> dict:
    operation = {
        "invalid_input": "Inspect the reported fields and input contract; explicitly correct the input before a new calculation.",
        "numerical_nonconvergence": "Inspect the saved geometry and native diagnostic; decide whether a new scientific attempt is justified.",
        "resource_limit": "Inspect requested limits and the recorded resource termination before deciding on a new attempt.",
        "environment_unavailable": "Inspect backend availability and required dependencies.",
        "unsupported": "Inspect the supported Action/backend contract.",
        "result_delivery": "Collect the original job and inspect its existing files; do not repeat the calculation to repair an index.",
        "output_parsing": "Inspect the reported source file, line and parser diagnostic. Repair or replace the output reader and reparse the saved file; this error does not establish that the calculation failed.",
        "infrastructure": "Look up the original submission receipt and job before considering another execution.",
        "cancelled": "The execution was cancelled; inspect saved outputs and the cancellation reason.",
    }.get(category, "Inspect the original diagnostic and saved files; the cause and repairability are not yet established.")
    return {
        "message": operation,
        "repairability": "input_correction" if category == "invalid_input" else "unknown",
        "requires_agent_decision": True,
        "communication_replay": "Look up the original submission_key; an unchanged replay returns the original job.",
        "new_calculation": "Changed input or a new scientific attempt requires a new submission_key.",
        "automatic_retry": False,
    }


def diagnostic(error: Any, *, status: str, source: str, evidence=()) -> dict | None:
    if not error:
        return None
    raw = error if isinstance(error, dict) else {"message": str(error)}
    category = error_category(raw, status)
    value = {
        "category": category, "code": raw.get("code") or raw.get("classification") or "unknown_error",
        "message": bounded(raw.get("message") or str(error), budget=4500),
        "failure_stage": raw.get("failure_stage", raw.get("stage", "execution")), "source": source,
        "stage": raw.get("stage", raw.get("failure_stage", "execution")),
        "origin": raw.get("origin", source),
        "evidence": bounded(raw.get("evidence") or list(evidence), budget=3500),
        "input_issues": bounded(raw.get("input_issues") or raw.get("missing_fields") or [], budget=2000),
        "repair_advice": repair_advice(category),
    }
    for name in ("exception_type", "source_file", "source_line", "function", "failure_location", "diagnostic_ref", "log_paths"):
        value[name] = bounded(raw.get(name), budget=1800)
    return value


def execution_feedback(*, status: dict, action_result: dict | None = None,
                       record: dict | None = None, axes: dict | None = None,
                       program_diagnostic: dict | None = None) -> dict:
    record, axes = record or {}, axes or {}
    action = action_result or {}
    state = str(status.get("status") or action.get("status") or "failed")
    artifacts = action.get("output_artifacts") or []
    primary = [a for a in artifacts if a.get("semantic_type") not in {"BackendDiagnostic", "BackendFile"}]
    evidence = [a for a in artifacts if a.get("semantic_type") == "BackendDiagnostic"]
    raw_error = action.get("error") or program_diagnostic or status.get("error")
    source = "action_result.error" if action.get("error") else "analysis_diagnostic" if program_diagnostic else "process"
    # Operator/resource termination remains authoritative; retain Action error separately.
    if state in {"cancelled", "timeout"} or (status.get("error") or {}).get("code") == "memory_limit_exceeded":
        raw_error, source = status.get("error"), "process"
    if not raw_error and state in TERMINAL_STATES - {"success", "partial_success"}:
        raw_error = {"code": "diagnostic_unavailable", "message": "No structured cause was recorded; inspect the saved process logs."}
    error = diagnostic(raw_error, status=state, source=source, evidence=evidence)
    if error and source == "process":
        error["evidence"] = [status[k] for k in ("stdout_path", "stderr_path") if status.get(k)]
    try:
        process = process_status(state)
    except ValueError:
        process = "unknown"
    provenance = action.get("provenance") or {}
    result_state = record.get("result_state") or ("ready" if action else "pending" if state not in TERMINAL_STATES else "legacy_unavailable")
    value = {
        "schema_version": 1, "job_id": status.get("job_id"), "job_type": status.get("job_type", "predefined_action" if action else None),
        "action": action.get("action"), "backend": action.get("backend"),
        "job_status": state, "terminal": state in TERMINAL_STATES,
        "action_status": action.get("status"), "process_status": axes.get("process_status", process),
        "process_exit_code": status.get("return_code"),
        "software_status": axes.get("software_status", "not_checked"),
        "convergence_status": axes.get("convergence_status", "not_checked"),
        "scientific_validation_status": axes.get("scientific_validation_status", "not_checked"),
        "result_state": "ready" if result_state == "indexed" else result_state,
        "result_revision": record.get("terminal_revision"), "result_receipt_id": record.get("result_receipt_id"),
        "diagnostic": error,
        "process_error": bounded(status.get("error"), budget=1500),
        "action_error": bounded(action.get("error"), budget=5000),
        "result_diagnostic": record.get("result_diagnostic"),
        "warnings": bounded(action.get("warnings") or [], budget=2500),
        "primary_artifacts": bounded(primary, budget=3500),
        "diagnostic_artifacts": bounded(evidence, budget=2500),
        "artifact_count": len(artifacts) if action else len(record.get("artifact_manifest") or []),
        "effective_inputs": bounded(provenance.get("effective_inputs") or {}, budget=2000),
        "full_result_ref": record.get("full_result_ref"),
        "next_tool_calls": ([{"tool": "collect_execution_job", "arguments": {"job_id": status["job_id"]}}]
                            if status.get("job_id") and result_state in {"missing", "corrupt", "pending_index", "legacy_unavailable"} else []),
    }
    # No assumption that a normal process validated scientific conclusions.
    if action and error and error["category"] == "numerical_nonconvergence":
        value["convergence_status"] = "failed"
    payload = action.get("result")
    if isinstance(payload, dict) and isinstance(payload.get("converged"), bool):
        value["convergence_status"] = "converged" if payload["converged"] else "failed"
        value["convergence_source"] = "action_result.result.converged"
    value["truncation"] = {"full_result_preserved": bool(value["full_result_ref"]), "bounded_agent_view": True}
    if feedback_schema_version() == 2:
        value["schema_version"] = 2
        for key in ("action_error", "process_error"):
            value.pop(key, None)
        value["request"] = {"status": "accepted" if status.get("job_id") else "invalid" if state == "invalid_request" else "processed"}
        value["process"] = {"started": status.get("process_started", True if status.get("child_pid") or status.get("return_code") is not None else None),
                            "exit_code": status.get("return_code"), "status": value["process_status"]}
        value["observations"] = (axes or {}).get("observations")
        value["scientific_validation_status"] = "not_assessed"
    return value


def normalize_tool_feedback(value, *, tool: str):
    """A compact shared boundary contract; non-job tools do not invent job axes."""
    if feedback_schema_version() != 2 or not isinstance(value, dict):
        return value
    value = dict(value)
    for field in ("newly_terminal_jobs", "newly_terminal_items", "items"):
        if isinstance(value.get(field), list):
            value[field] = [normalize_tool_feedback(item, tool=tool) if isinstance(item, dict) and item.get("execution_feedback") else item
                            for item in value[field]]
    feedback = value.get("execution_feedback")
    if not feedback:
        state = value.get("status", "success")
        error = value.get("error")
        feedback = {"schema_version": 2, "tool": tool,
                    "request": {"status": "invalid" if state == "invalid_request" else "processed"},
                    "diagnostic": diagnostic(error, status=str(state), source="tool_boundary")}
        value["execution_feedback"] = feedback
    if feedback.get("diagnostic"):
        # One authoritative diagnostic body. Raw values remain in the trace.
        for key in ("error", "failure_diagnostic", "stdout_tail", "stderr_tail"):
            value.pop(key, None)
    for field in ("action_result", "result"):
        if isinstance(value.get(field), dict) and value[field].get("execution_feedback"):
            action = dict(value[field])
            action.pop("execution_feedback", None)
            action.pop("error", None)
            value[field] = action
    observation = feedback.get("observations")
    if observation:
        # Complete arrays remain in versioned interpretation/source records.
        feedback = dict(feedback)
        feedback["observations"] = {k: v for k, v in observation.items() if k != "frequency_blocks"}
        feedback["observations"]["frequency_blocks"] = [
            {k: v for k, v in block.items() if k != "frequencies_cm_1"}
            for block in observation.get("frequency_blocks", [])]
        value["execution_feedback"] = feedback
        value.pop("observations", None)
        for key in ("details", "execution_status_details"):
            value.pop(key, None)
    return value


def exception_feedback(exc: Exception, *, tool: str, stage: str = "tool_boundary"):
    invalid = isinstance(exc, (ValueError, KeyError, FileNotFoundError, FileExistsError, UnicodeError))
    state = "invalid_request" if invalid else "failed"
    return normalize_tool_feedback({"status": state, "error": {
        "code": "invalid_tool_request" if invalid else "tool_execution_error",
        "message": str(exc), "stage": stage, "origin": "tool_boundary",
        "exception_type": type(exc).__name__, "category": "invalid_input" if invalid else "infrastructure",
    }}, tool=tool)

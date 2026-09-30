"""Read the same durable facts for get, wait, collect and batch projections."""
from chemistry_toolbox.src.execution_feedback import execution_feedback, feedback_schema_version
from .execution_store import execution_store


def conditional_result(value, known_version=None):
    """A client must explicitly name the same interpretation to omit details."""
    import hashlib
    import json
    from chemistry_toolbox.src.native_observations import PARSER_VERSION
    feedback = value.get("execution_feedback") or {}
    identity = {k: feedback.get(k) for k in ("job_id", "job_status", "result_state", "result_revision",
                                           "result_receipt_id", "diagnostic", "artifact_count")}
    identity.update(parser_version=PARSER_VERSION, feedback_version=feedback_schema_version())
    version = hashlib.sha256(json.dumps(identity, sort_keys=True, default=str).encode()).hexdigest()
    value["result_version"] = version
    if known_version == version and feedback.get("terminal"):
        return {"status": value.get("status"), "job_id": feedback.get("job_id"),
                "job_status": feedback.get("job_status"), "result_state": feedback.get("result_state"),
                "result_receipt_id": feedback.get("result_receipt_id"), "result_version": version,
                "unchanged": True, "terminal": True, "full_result_ref": feedback.get("full_result_ref")}
    return value


def page_collection(value, request):
    value = dict(value)
    pages = {}
    for key in ("outputs", "artifact_manifest", "result_artifact_manifest"):
        files = value.get(key)
        if not isinstance(files, list):
            continue
        end = request.file_offset + request.max_files
        pages[key] = {"offset": request.file_offset, "count": len(files),
                      "next_offset": end if end < len(files) else None}
        value[key + "_count"] = len(files)
        value[key] = files[request.file_offset:end]
    value["pagination"] = pages
    value["truncated"] = any(p["offset"] > 0 or p["next_offset"] is not None for p in pages.values())
    return conditional_result(value, request.known_result_version)


def job_feedback(directory, status, *, axes=None, program_diagnostic=None, record=None):
    store = execution_store()
    job_id = status["job_id"]
    record = record if record is not None else store.get_record("result", job_id, {})
    record = dict(record or {})
    action = record.get("action_result")
    spec = store.spec(job_id) or {}
    if not action and spec.get("job_type") == "predefined_action":
        from .action_result_io import read_action_result
        action, problem = read_action_result(store, job_id)
        if problem and status.get("status") not in {"queued", "accepted", "launching", "running"}:
            record.update(result_state="missing" if problem["code"] == "result_missing" else "corrupt", result_diagnostic=problem)
        elif action and not record:
            record["result_state"] = "pending_index"
    if status.get("job_type") == "native_software" and (status.get("status") not in {"accepted", "queued", "launching", "running", "success"} or (axes or {}).get("software_status") == "failed"):
        from chemistry_toolbox.src.native_diagnostics import native_diagnostic
        program_diagnostic = native_diagnostic([directory / name for name in ("stdout.log", "stderr.log", "OUTCAR", "lobsterout")], root=store.root,
            software_id=(status.get("metadata") or {}).get("software_id", "unknown"), fallback=status.get("error"))
    view = execution_feedback(status=status, action_result=action, record=record,
                              axes=axes, program_diagnostic=program_diagnostic)
    import json
    import time
    try:
        activity = json.loads((directory / "activity.json").read_text())
        activity["age_seconds"] = max(0, time.time() - activity["observed_at"])
        view["activity"] = activity
    except (OSError, ValueError, KeyError, TypeError):
        view["activity"] = {"status": "unknown"}
    if feedback_schema_version() == 1 and not action and status.get("job_type") == "native_software" and view.get("diagnostic"):
        from .open_execution import _tail
        from chemistry_toolbox.src.execution_feedback import bounded
        view["diagnostic"]["evidence"] = bounded({"native_checks": (axes or {}).get("details", {}),
            "stdout_tail": _tail(directory / "stdout.log", 2000), "stderr_tail": _tail(directory / "stderr.log", 2000),
            "log_paths": [str((directory / name).relative_to(store.root)) for name in ("stdout.log", "stderr.log")]}, budget=6000)
    if spec.get("job_type") == "predefined_action":
        view.update(job_type="predefined_action", action=spec.get("action_id"))
    return view

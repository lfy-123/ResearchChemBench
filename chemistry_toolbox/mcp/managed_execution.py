"""Durable local submissions; no scientific processes are started by MCP."""
from __future__ import annotations

import json
import os
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from chemistry_toolbox.src.recovery_io import atomic_json, file_hash, file_lock
from chemistry_toolbox.src.resource_budget import normalize_resource_limits, resource_budget_record, validate_resource_limits
from chemistry_toolbox.src.timeout_policy import timeout_seconds_for
from .execution_store import ExecutionStore, SubmissionConflict, execution_store


def recovery_enabled() -> bool:
    return os.environ.get("RESEARCHCHEMBENCH_RECOVERY_ENABLED", "0").lower() in {"1", "true", "yes"}


def freeze_files(store: ExecutionStore, items: list) -> tuple[list, list]:
    """Hash the copied bytes, then recheck the source to reject concurrent edits."""
    from .workspace import resolve_workspace_path
    from .open_execution import _maximum_staged_bytes
    frozen, manifest, total, targets = [], [], 0, set()
    for item in items:
        source_value = item["source_path"] if isinstance(item, dict) else item.source_path
        target_value = item["target_path"] if isinstance(item, dict) else item.target_path
        target = PurePosixPath(target_value)
        if target.is_absolute() or ".." in target.parts or str(target) in targets:
            raise ValueError("invalid or duplicate snapshot target")
        targets.add(str(target))
        source = resolve_workspace_path(source_value, must_exist=True)
        if not source.is_file():
            raise ValueError("snapshot input must be a regular file")
        total += source.stat().st_size
        if total > _maximum_staged_bytes():
            raise ValueError("staged inputs exceed configured limit")
        snapshot_root = store.directory / "inputs"
        snapshot_root.mkdir(exist_ok=True)
        temporary = snapshot_root / (uuid.uuid4().hex + ".tmp")
        try:
            before = source.stat()
            with source.open("rb") as src, temporary.open("wb") as dst:
                shutil.copyfileobj(src, dst)
                dst.flush()
                os.fsync(dst.fileno())
            digest = file_hash(temporary)
            after = source.stat()
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino) or digest != file_hash(source):
                raise ValueError("input_changed_during_snapshot")
            destination = snapshot_root / digest
            os.replace(temporary, destination)
            record = {"source_path": str(source.relative_to(store.root)), "target_path": str(target), "sha256": digest, "size_bytes": destination.stat().st_size}
            manifest.append(record)
            frozen.append({**record, "snapshot_path": str(destination)})
        finally:
            temporary.unlink(missing_ok=True)
    return frozen, manifest


def submission_response(store: ExecutionStore, receipt) -> dict:
    job = store.get_job(receipt.entity_id)
    return {"status": "success", "recovery_capability": True, "replayed": receipt.replayed,
            "submission_status": "accepted", "response_prepared_at": datetime.now(timezone.utc).isoformat(),
            "job_id" if receipt.entity_type == "job" else "batch_id": receipt.entity_id,
            "job_status" if receipt.entity_type == "job" else "batch_status": job["state"],
            "submission_key": receipt.submission_key, "receipt": receipt.as_dict(),
            "next_step": "Keep this receipt. Accepted/queued is not running or completed. After a lost response, query lookup_execution_submission with the original submission_key before retrying."}


def accept(spec: dict, request: dict, key: str, frozen: list, manifest: list, *, batch=False) -> dict:
    from .job_manager import ensure_manager
    store = execution_store()
    if os.environ.get("RESEARCHCHEMBENCH_EXECUTION_MODE", "local") != "local":
        return {"status": "invalid_request", "error": {"code": "recovery_local_only"}}
    control = store.get_record("control", "current", {})
    run = store.get_record("run", "manifest", {})
    existing = store.get_submission(key)
    if not existing and (control.get("command") in {"cancel", "finalize", "pause"} or run.get("run_state") in {"recovering", "recovery_blocked", "completed", "failed", "cancelled", "budget_exhausted"}):
        return {"status": "recovery_blocked", "error": {"code": "run_not_accepting_submissions"}}
    spec = {**spec, "frozen_inputs": frozen, "budget": resource_budget_record(),
            "run_deadline": os.environ.get("RESEARCHCHEMBENCH_RUN_DEADLINE") or run.get("deadline_at")}
    try:
        receipt = store.accept_submission(submission_key=key, entity_type="batch" if batch else "job",
                                          entity_prefix="batch" if batch else "job", request=request,
                                          input_manifest=manifest, spec=spec)
    except SubmissionConflict as exc:
        return {"status": "invalid_request", "error": {"code": "submission_conflict", "message": str(exc)}}
    diagnostics = []
    if batch and not receipt.replayed:
        try:
            atomic_json(store.root / "outputs" / "action_batches" / receipt.entity_id / "status.json", {
                "batch_id": receipt.entity_id, "status": "queued", "items": [
                    {"item_id": child["item_id"], "batch_index": i, "status": "queued"}
                    for i, child in enumerate(spec["children"])], "events": [], "last_sequence": 0,
                "recovery_managed": True,
            })
        except Exception as exc:
            diagnostics.append({"code": "batch_projection_deferred", "message": f"{type(exc).__name__}: {exc}"})
    try:
        ensure_manager(store)
    except Exception as exc:
        # Acceptance is already committed. Never present wakeup failure as a
        # rejected submission, which could cause a duplicate scientific job.
        diagnostics.append({"code": "manager_wakeup_deferred", "message": f"{type(exc).__name__}: {exc}"})
    return {**submission_response(store, receipt),
            "scheduling": {"status": "deferred" if diagnostics else "notified", "diagnostics": diagnostics}}


def submit_job(*, job_type, runtime, command, stdin_target, staged_inputs, resource_limits, metadata, submission_key, submission_request=None):
    if not submission_key:
        return {"status": "invalid_request", "error": {"code": "submission_key_required"}}
    store = execution_store()
    validate_resource_limits(resource_limits)
    frozen, manifest = freeze_files(store, staged_inputs)
    if metadata.get("script_sha256"):
        script_hash = next((item["sha256"] for item in manifest if item["target_path"] == metadata.get("script_target")), None)
        if script_hash != metadata["script_sha256"]:
            raise ValueError("analysis_script_changed_after_validation")
    request = {"job_type": job_type, "runtime": runtime, "command": command, "stdin_target": stdin_target,
               "resource_limits": resource_limits, "request": submission_request}
    return accept({**request, "metadata": metadata}, request, submission_key, frozen, manifest)


def freeze_action_inputs(store: ExecutionStore, inputs: dict):
    from chemistry_toolbox.src.artifacts import canonicalize_artifact_refs, collect_artifact_refs
    # Expand compact references first, then snapshot all referenced files and
    # workspace file-valued inputs. The worker verifies these copies again.
    inputs = canonicalize_artifact_refs(inputs)
    paths = {ref.path for ref in collect_artifact_refs(inputs)}
    def visit(value):
        if isinstance(value, dict):
            for child in value.values(): visit(child)
        elif isinstance(value, list):
            for child in value: visit(child)
        elif isinstance(value, str) and len(value) < 4096:
            try:
                candidate = (store.root / value).resolve()
                if candidate.is_relative_to(store.root) and candidate.is_file(): paths.add(str(candidate.relative_to(store.root)))
            except (OSError, ValueError): pass
    visit(inputs)
    frozen, manifest = freeze_files(store, [{"source_path": p, "target_path": p} for p in sorted(paths)])
    digests = {item["target_path"]: item["sha256"] for item in manifest}
    for reference in collect_artifact_refs(inputs):
        if digests.get(reference.path) != reference.sha256:
            raise ValueError(f"Artifact hash mismatch: {reference.artifact_id}")
    return inputs, frozen, manifest


def action_spec(action_id: str, request: dict) -> tuple[dict, list, list]:
    from chemistry_toolbox.src.catalog import action_specs
    from chemistry_toolbox.src.artifacts import collect_artifact_refs
    inputs, frozen, manifest = freeze_action_inputs(execution_store(), request["inputs"])
    resources = normalize_resource_limits(request.get("resource_limits") or {})
    validate_resource_limits(resources)
    resources["walltime_seconds"] = timeout_seconds_for(action_specs()[action_id].execution_class)
    return {"job_type": "predefined_action", "runtime": "core", "action_id": action_id, "result_contract_version": 1,
            "electronic_state_policy": os.environ.get("RESEARCHCHEMBENCH_ELECTRONIC_STATE_POLICY", "legacy"),
            "action_request": {**request, "inputs": inputs}, "resource_limits": resources,
            "input_artifacts": [ref.model_dump(mode="json") for ref in collect_artifact_refs(inputs)],
            "metadata": {}, "command": [], "stdin_target": None}, frozen, manifest


def submit_action(action_id: str, request: dict):
    key = request.get("submission_key")
    if not key:
        return {"status": "invalid_request", "error": {"code": "submission_key_required"}}
    spec, frozen, manifest = action_spec(action_id, request)
    return accept(spec, {"action_id": action_id, **request}, key, frozen, manifest)


def submit_batch(request):
    key = request.submission_key
    if not key:
        return {"status": "invalid_request", "error": {"code": "submission_key_required"}}
    payload = request.model_dump(mode="json")
    children, manifest = [], []
    for item in request.items:
        child_request = {k: payload[k] for k in ("backend_id", "component_backends", "method_spec", "action_settings")}
        child_request.update(inputs=item.inputs, resource_limits=item.resource_limits.model_dump(mode="json"))
        spec, frozen, files = action_spec(request.action_id, child_request)
        children.append({"item_id": item.item_id, "spec": {**spec, "frozen_inputs": frozen}})
        manifest.append({"item_id": item.item_id, "files": files})
    return accept({"job_type": "batch", "children": children, "max_concurrency": request.max_concurrency}, payload, key, [], manifest, batch=True)

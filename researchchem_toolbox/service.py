"""Validate one exact agent selection, dispatch it, and build provenance."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .artifacts import ArtifactStore, collect_artifact_refs
from .catalog import action_specs, active_catalog_hash, backend_specs
from .models import ActionRequest, ActionResult
from .runtime import invoke_worker, probe_all_backends


def _invalid(
    action_id: str,
    request_backend: str | None,
    message: str,
    *,
    code: str = "invalid_request",
) -> dict[str, Any]:
    return ActionResult(
        status="invalid_request",
        action=action_id,
        action_version=action_specs().get(action_id).version if action_id in action_specs() else "unknown",
        requested_backend=request_backend,
        backend=None,
        selection_source="agent",
        error={"code": code, "message": message},
        retryable=False,
        provenance={
            "catalog_hash": active_catalog_hash(),
            "automatic_fallback_count": 0,
        },
    ).model_dump(mode="json")


def execute_action(action_id: str, request_value: ActionRequest | dict[str, Any]) -> dict[str, Any]:
    actions = action_specs()
    backends = backend_specs()
    if action_id not in actions:
        return _invalid(action_id, None, f"Unknown action: {action_id}", code="unknown_action")
    try:
        request = (
            request_value
            if isinstance(request_value, ActionRequest)
            else ActionRequest.model_validate(request_value)
        )
    except ValidationError as exc:
        return _invalid(action_id, None, str(exc))

    specification = actions[action_id]
    if specification.data_action:
        fixed_backend = specification.backend_ids[0]
        if request.backend_id is not None and request.backend_id != fixed_backend:
            return _invalid(
                action_id,
                request.backend_id,
                f"Data Action {action_id} uses fixed data source {fixed_backend}",
            )
        backend_id = fixed_backend
        selection_source = "fixed_data_source"
    else:
        if request.backend_id is None:
            return _invalid(action_id, None, "backend_id is required for every Scientific Action")
        backend_id = request.backend_id
        selection_source = "agent"
    if backend_id not in specification.backend_ids:
        return _invalid(
            action_id,
            backend_id,
            f"Backend {backend_id!r} does not declare support for action {action_id!r}",
            code="unsupported_backend",
        )

    missing_inputs = [name for name in specification.required_inputs if name not in request.inputs]
    if missing_inputs:
        return _invalid(
            action_id,
            backend_id,
            f"Missing required inputs: {missing_inputs}",
        )
    backend = backends[backend_id]
    missing_methods = [
        name
        for name in backend.required_method_fields.get(action_id, ())
        if name not in request.method_spec
    ]
    missing_settings = [
        name
        for name in backend.required_setting_fields.get(action_id, ())
        if name not in request.action_settings
    ]
    if missing_methods or missing_settings:
        parts = []
        if missing_methods:
            parts.append(f"method_spec fields {missing_methods}")
        if missing_settings:
            parts.append(f"action_settings fields {missing_settings}")
        return _invalid(
            action_id,
            backend_id,
            "Missing explicitly required scientific settings: " + "; ".join(parts),
        )

    health = probe_all_backends((backend,))[backend_id]
    if not health["available"]:
        return ActionResult(
            status="unavailable",
            action=action_id,
            action_version=specification.version,
            requested_backend=backend_id,
            backend=backend_id,
            selection_source=selection_source,
            error={
                "code": "backend_unavailable",
                "message": f"Requested backend {backend_id} is unavailable in runtime {backend.runtime}",
                "health": health,
            },
            retryable=False,
            provenance={
                "catalog_hash": active_catalog_hash(),
                "agent_selected_action": action_id,
                "agent_selected_backend": backend_id,
                "agent_selected_method_spec": request.method_spec,
                "agent_selected_action_settings": request.action_settings,
                "runtime_profile": backend.runtime,
                "automatic_fallback_count": 0,
            },
        ).model_dump(mode="json")

    input_artifacts = collect_artifact_refs(request.inputs)
    worker_payload = {
        "action_id": action_id,
        "backend_id": backend_id,
        "request": request.model_dump(mode="json"),
    }
    worker = invoke_worker(
        runtime=backend.runtime,
        payload=worker_payload,
        timeout_seconds=request.resource_limits.walltime_seconds,
    )
    status = worker.get("status", "failed")
    if status not in {
        "success", "partial_success", "invalid_request", "unsupported", "unavailable",
        "failed", "timeout", "cancelled",
    }:
        status = "failed"
        worker["error"] = {
            "code": "invalid_backend_status",
            "message": f"Backend returned invalid status {worker.get('status')!r}",
        }

    output_artifacts = []
    result_payload = worker.get("result")
    if status in {"success", "partial_success"}:
        store = ArtifactStore()
        parent_ids = [item.artifact_id for item in input_artifacts]
        output_artifacts.append(
            store.put_json(
                result_payload,
                semantic_type=specification.primary_output,
                producer_action=action_id,
                producer_backend=backend_id,
                parent_artifact_ids=parent_ids,
            )
        )
        for item in worker.get("artifact_files", []):
            try:
                output_artifacts.append(
                    store.register_file(
                        item["path"],
                        semantic_type=item.get("semantic_type", "BackendFile"),
                        media_type=item.get("media_type", "application/octet-stream"),
                        producer_action=action_id,
                        producer_backend=backend_id,
                        parent_artifact_ids=parent_ids,
                    )
                )
            except (KeyError, OSError, ValueError) as exc:
                worker.setdefault("warnings", []).append(f"Artifact registration failed: {exc}")

    provenance = {
        "catalog_hash": active_catalog_hash(),
        "agent_selected_action": action_id,
        "agent_selected_backend": backend_id,
        "agent_selected_method_spec": request.method_spec,
        "agent_selected_action_settings": request.action_settings,
        "runtime_profile": backend.runtime,
        "dispatcher_executed_backend": backend_id,
        "automatic_fallback_count": 0,
        **dict(worker.get("provenance") or {}),
    }
    return ActionResult(
        status=status,
        action=action_id,
        action_version=specification.version,
        requested_backend=backend_id,
        backend=backend_id,
        backend_version=worker.get("backend_version"),
        selection_source=selection_source,
        result=result_payload,
        input_artifacts=input_artifacts,
        output_artifacts=output_artifacts,
        warnings=list(worker.get("warnings") or []),
        provenance=provenance,
        error=worker.get("error"),
        retryable=bool(worker.get("retryable", False)),
    ).model_dump(mode="json")

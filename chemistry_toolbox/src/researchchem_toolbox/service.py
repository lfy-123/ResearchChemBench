"""Validate one exact agent selection, dispatch it, and build provenance."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any, Mapping

from pydantic import ValidationError

from .artifacts import ArtifactStore, canonicalize_artifact_refs, collect_artifact_refs
from .catalog import action_specs, active_catalog_hash, backend_specs
from .models import ActionRequest, ActionResult
from .resources import collect_resource_references
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


def _invalid_explicit_choice(
    action_id: str,
    backend_id: str,
    *,
    field_group: str,
    supplied: dict[str, Any],
    allowed: Mapping[str, tuple[str, ...]],
) -> dict[str, Any] | None:
    for field_name, choices in allowed.items():
        if field_name not in supplied:
            continue
        received = supplied[field_name]
        normalized = str(received).strip().casefold()
        if normalized not in {str(choice).casefold() for choice in choices}:
            return _invalid(
                action_id,
                backend_id,
                f"Invalid {field_group}.{field_name}={received!r} for {backend_id}/{action_id}; "
                f"choose exactly one of {list(choices)}",
            )
    return None


def _validate_composite_calculator_contract(
    action_id: str,
    backend_id: str,
    request: ActionRequest,
    backends: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Validate nested calculator requests before launching a composite worker.

    Sella and geomeTRIC evaluate both energy and forces through the exact
    ``component_backends.calculator`` selected by the Agent.  Their nested
    settings are part of the public request contract and must not fail later as
    an opaque optimizer exception.
    """

    if backend_id not in {"sella", "geometric"}:
        return None
    calculator_id = request.component_backends.get("calculator")
    if not calculator_id:
        return None  # The ordinary required-component check reports this first.
    calculator_method = request.method_spec.get("calculator_method")
    if not isinstance(calculator_method, Mapping):
        return _invalid(
            action_id,
            backend_id,
            "method_spec.calculator_method must be a mapping containing the exact method fields "
            f"for component_backends.calculator={calculator_id!r}",
        )
    nested_settings = request.action_settings.get("calculator_action_settings")
    if not isinstance(nested_settings, Mapping):
        return _invalid(
            action_id,
            backend_id,
            "action_settings.calculator_action_settings must be an action-keyed mapping with "
            "both 'calculate_energy' and 'calculate_forces' entries",
        )
    calculator = backends[calculator_id]
    for nested_action in ("calculate_energy", "calculate_forces"):
        supplied_settings = nested_settings.get(nested_action)
        if not isinstance(supplied_settings, Mapping):
            return _invalid(
                action_id,
                backend_id,
                "action_settings.calculator_action_settings must explicitly contain mapping "
                f"{nested_action!r}; for example {{'calculate_energy': {{}}, "
                "'calculate_forces': {}}}",
            )
        if nested_action not in calculator.capabilities:
            return _invalid(
                action_id,
                backend_id,
                f"Selected calculator {calculator_id!r} does not provide {nested_action!r}",
            )
        missing_methods = [
            field_name
            for field_name in calculator.required_method_fields.get(nested_action, ())
            if field_name not in calculator_method
        ]
        missing_settings = [
            field_name
            for field_name in calculator.required_setting_fields.get(nested_action, ())
            if field_name not in supplied_settings
        ]
        if missing_methods or missing_settings:
            parts = []
            if missing_methods:
                parts.append(
                    f"method_spec.calculator_method fields {missing_methods}"
                )
            if missing_settings:
                parts.append(
                    "action_settings.calculator_action_settings"
                    f".{nested_action} fields {missing_settings}"
                )
            return _invalid(
                action_id,
                backend_id,
                f"Nested calculator contract for {calculator_id}/{nested_action} is incomplete: "
                + "; ".join(parts),
            )
        for field_name, choices in calculator.allowed_method_values.get(
            nested_action, {}
        ).items():
            if field_name in calculator_method and str(
                calculator_method[field_name]
            ).strip().casefold() not in {
                str(choice).casefold() for choice in choices
            }:
                return _invalid(
                    action_id,
                    backend_id,
                    f"Invalid method_spec.calculator_method.{field_name}="
                    f"{calculator_method[field_name]!r} for {calculator_id}/{nested_action}; "
                    f"choose exactly one of {list(choices)}",
                )
        for field_name, choices in calculator.allowed_setting_values.get(
            nested_action, {}
        ).items():
            if field_name in supplied_settings and str(
                supplied_settings[field_name]
            ).strip().casefold() not in {
                str(choice).casefold() for choice in choices
            }:
                return _invalid(
                    action_id,
                    backend_id,
                    "Invalid action_settings.calculator_action_settings"
                    f".{nested_action}.{field_name}={supplied_settings[field_name]!r} "
                    f"for {calculator_id}/{nested_action}; choose exactly one of {list(choices)}",
                )
    return None


def _validate_artifact_input_semantics(
    action_id: str,
    backend_id: str,
    inputs: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Reject a typed ArtifactRef placed in a demonstrably incompatible slot."""

    if action_id != "derive_vibrational_modes":
        return None
    hessian = inputs.get("hessian")
    structure = inputs.get("structure")
    if (
        isinstance(hessian, Mapping)
        and isinstance(structure, Mapping)
        and hessian.get("artifact_id")
        and hessian.get("artifact_id") == structure.get("artifact_id")
    ):
        return _invalid(
            action_id,
            backend_id,
            "inputs.hessian and inputs.structure require two differently typed values: use the "
            "Hessian primary artifact from calculate_hessian for inputs.hessian and reuse the "
            "matching AtomicStructure input for inputs.structure",
            code="artifact_semantic_mismatch",
        )
    if isinstance(hessian, Mapping) and hessian.get("artifact_id"):
        if hessian.get("semantic_type") != "Hessian":
            return _invalid(
                action_id,
                backend_id,
                f"inputs.hessian received ArtifactRef semantic_type="
                f"{hessian.get('semantic_type')!r}; it requires the primary 'Hessian' JSON "
                "artifact returned by calculate_hessian",
                code="artifact_semantic_mismatch",
            )
    if isinstance(structure, Mapping) and structure.get("artifact_id"):
        semantic_type = str(structure.get("semantic_type") or "")
        media_type = str(structure.get("media_type") or "")
        suffix = PurePosixPath(str(structure.get("path") or "")).suffix.casefold()
        if not (
            semantic_type == "AtomicStructure"
            or media_type.startswith("chemical/")
            or suffix in {".xyz", ".pdb", ".sdf", ".mol"}
        ):
            return _invalid(
                action_id,
                backend_id,
                f"inputs.structure received ArtifactRef semantic_type={semantic_type!r}; use the "
                "matching AtomicStructure artifact or a registered structure file",
                code="artifact_semantic_mismatch",
            )
    return None


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
    policy = specification.selection_policy
    if policy == "fixed_source":
        fixed_backend = specification.backend_ids[0]
        if request.backend_id is not None and request.backend_id != fixed_backend:
            return _invalid(
                action_id,
                request.backend_id,
                f"Data Action {action_id} uses fixed data source {fixed_backend}",
            )
        if request.source_id is not None and request.source_id != fixed_backend:
            return _invalid(
                action_id,
                request.source_id,
                f"Data Action {action_id} uses fixed data source {fixed_backend}",
            )
        if request.component_backends:
            return _invalid(action_id, fixed_backend, f"Data Action {action_id} does not accept component_backends")
        backend_id = fixed_backend
        selection_source = "fixed_data_source"
    elif policy == "internal_deterministic":
        fixed_backend = specification.backend_ids[0]
        if request.backend_id is not None and request.backend_id != fixed_backend:
            return _invalid(
                action_id,
                request.backend_id,
                f"Action {action_id} uses fixed deterministic provider {fixed_backend}",
            )
        if request.source_id is not None or request.component_backends:
            return _invalid(
                action_id,
                request.backend_id,
                f"Action {action_id} does not accept source_id or component_backends",
            )
        backend_id = fixed_backend
        selection_source = "internal_deterministic"
    elif policy == "agent_source_required":
        if request.source_id is None:
            return _invalid(action_id, None, "source_id is required for this Data Action")
        if request.backend_id is not None or request.component_backends:
            return _invalid(action_id, request.backend_id, "This Data Action accepts source_id, not backend_id/component_backends")
        backend_id = request.source_id
        selection_source = "agent_data_source"
    elif policy in {"agent_backend_required", "agent_components_required"}:
        if request.backend_id is None:
            return _invalid(action_id, None, "backend_id is required for every Scientific Action")
        backend_id = request.backend_id
        selection_source = "agent_components" if policy == "agent_components_required" else "agent"
    else:  # defensive guard for stale serialized catalogs
        return _invalid(action_id, request.backend_id, f"Unknown selection policy: {policy}")
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
    missing_backend_inputs = [
        name
        for name in backend.required_input_fields.get(action_id, ())
        if name not in request.inputs
    ]
    if missing_backend_inputs:
        return _invalid(
            action_id,
            backend_id,
            f"Missing backend-specific required inputs: {missing_backend_inputs}",
        )
    required_component_roles = backend.required_component_roles.get(action_id, ())
    component_options = backend.component_backend_options.get(action_id, {})
    backend_uses_components = bool(required_component_roles or component_options)
    if request.component_backends and not backend_uses_components:
        return _invalid(
            action_id,
            backend_id,
            f"Backend {backend_id!r} for action {action_id!r} does not use component_backends",
        )
    if backend_uses_components:
        selection_source = "agent_components"
    missing_component_roles = [
        role for role in required_component_roles if role not in request.component_backends
    ]
    if missing_component_roles:
        return _invalid(
            action_id,
            backend_id,
            f"Missing explicitly required component_backends roles: {missing_component_roles}",
        )
    component_specs = []
    for role, component_backend_id in request.component_backends.items():
        if component_backend_id not in backends:
            return _invalid(
                action_id,
                backend_id,
                f"Unknown component backend {component_backend_id!r} for role {role!r}",
            )
        allowed = component_options.get(role)
        if allowed is None:
            return _invalid(
                action_id,
                backend_id,
                f"Unsupported component backend role {role!r} for {backend_id}/{action_id}",
            )
        if allowed is not None and component_backend_id not in allowed:
            return _invalid(
                action_id,
                backend_id,
                f"Component backend {component_backend_id!r} is not allowed for role {role!r}; "
                f"choose one of {list(allowed)}",
            )
        component_specs.append(backends[component_backend_id])
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

    invalid_choice = _invalid_explicit_choice(
        action_id,
        backend_id,
        field_group="method_spec",
        supplied=request.method_spec,
        allowed=backend.allowed_method_values.get(action_id, {}),
    ) or _invalid_explicit_choice(
        action_id,
        backend_id,
        field_group="action_settings",
        supplied=request.action_settings,
        allowed=backend.allowed_setting_values.get(action_id, {}),
    )
    if invalid_choice is not None:
        return invalid_choice

    invalid_composite = _validate_composite_calculator_contract(
        action_id, backend_id, request, backends
    )
    if invalid_composite is not None:
        return invalid_composite

    try:
        canonical_inputs = canonicalize_artifact_refs(request.inputs)
    except (KeyError, OSError, ValueError, ValidationError) as exc:
        return _invalid(
            action_id,
            backend_id,
            f"Invalid explicit ArtifactRef: {exc}",
            code="invalid_artifact_reference",
        )
    request = request.model_copy(update={"inputs": canonical_inputs})
    invalid_artifact_semantics = _validate_artifact_input_semantics(
        action_id, backend_id, request.inputs
    )
    if invalid_artifact_semantics is not None:
        return invalid_artifact_semantics
    resource_references = collect_resource_references(
        {"inputs": request.inputs, "method_spec": request.method_spec}
    )

    health_values = probe_all_backends((backend, *component_specs))
    health = health_values[backend_id]
    unavailable_components = {
        role: health_values[component_backend_id]
        for role, component_backend_id in request.component_backends.items()
        if not health_values[component_backend_id]["available"]
    }
    if unavailable_components:
        return ActionResult(
            status="unavailable",
            action=action_id,
            action_version=specification.version,
            requested_backend=backend_id,
            backend=backend_id,
            selection_source=selection_source,
            error={
                "code": "component_backend_unavailable",
                "message": "One or more Agent-selected component backends are unavailable",
                "components": unavailable_components,
            },
            retryable=False,
            provenance={
                "catalog_hash": active_catalog_hash(),
                "agent_selected_action": action_id,
                "agent_selected_backend": backend_id,
                "agent_selected_component_backends": request.component_backends,
                "agent_selected_source_id": request.source_id,
                "automatic_fallback_count": 0,
            },
        ).model_dump(mode="json")
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
                "agent_selected_resource_refs": resource_references,
                "agent_selected_component_backends": request.component_backends,
                "agent_selected_source_id": request.source_id,
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
    store = ArtifactStore()
    if status in {"success", "partial_success"}:
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
    elif worker.get("error"):
        parent_ids = [item.artifact_id for item in input_artifacts]
        try:
            output_artifacts.append(
                store.put_json(
                    {
                        "action": action_id,
                        "backend": backend_id,
                        "status": status,
                        "error": worker.get("error"),
                        "warnings": list(worker.get("warnings") or []),
                    },
                    semantic_type="BackendDiagnostic",
                    producer_action=action_id,
                    producer_backend=backend_id,
                    parent_artifact_ids=parent_ids,
                )
            )
        except (OSError, ValueError) as exc:
            worker.setdefault("warnings", []).append(
                f"Backend diagnostic artifact registration failed: {exc}"
            )

    provenance = {
        "catalog_hash": active_catalog_hash(),
        "agent_selected_action": action_id,
        "agent_selected_backend": backend_id,
        "agent_selected_method_spec": request.method_spec,
        "agent_selected_action_settings": request.action_settings,
        "agent_selected_resource_refs": resource_references,
        "agent_selected_component_backends": request.component_backends,
        "agent_selected_source_id": request.source_id,
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

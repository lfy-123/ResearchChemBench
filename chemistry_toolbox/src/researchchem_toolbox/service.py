"""Validate one exact agent selection, dispatch it, and build provenance."""

from __future__ import annotations

import math
from pathlib import PurePosixPath
from typing import Any, Mapping

from pydantic import ValidationError

from .artifacts import ArtifactStore, canonicalize_artifact_refs, collect_artifact_refs
from .catalog import action_specs, active_catalog_hash, backend_specs
from .models import ActionRequest, ActionResult
from .resource_budget import (
    ResourceBudgetExceeded,
    normalize_resource_limits,
    reserve_resources,
    resource_budget_record,
    validate_resource_limits,
)
from .resources import collect_resource_references
from .runtime import invoke_worker, probe_all_backends
from .timeout_policy import timeout_policy_record, timeout_seconds_for


def _invalid(
    action_id: str,
    request_backend: str | None,
    message: str,
    *,
    code: str = "invalid_request",
    error_details: Mapping[str, Any] | None = None,
    retryable: bool = False,
) -> dict[str, Any]:
    return ActionResult(
        status="invalid_request",
        action=action_id,
        action_version=action_specs().get(action_id).version if action_id in action_specs() else "unknown",
        requested_backend=request_backend,
        backend=None,
        selection_source="agent",
        error={"code": code, "message": message, **dict(error_details or {})},
        retryable=retryable,
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


def _validate_deprecated_setting_aliases(
    action_id: str,
    backend_id: str,
    settings: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Reject ambiguous requests while preserving explicit legacy aliases."""

    if (
        action_id == "calculate_electron_isodensity_surface"
        and backend_id == "multiwfn"
        and "grid_spacing_bohr" in settings
        and "grid_spacing_angstrom" in settings
    ):
        return _invalid(
            action_id,
            backend_id,
            "Supply exactly one of action_settings.grid_spacing_bohr (canonical) or "
            "action_settings.grid_spacing_angstrom (deprecated compatibility alias), not both.",
            code="conflicting_setting_aliases",
        )
    return None


def _required_setting_is_present(
    action_id: str,
    backend_id: str,
    field_name: str,
    settings: Mapping[str, Any],
) -> bool:
    if field_name in settings:
        return True
    return (
        action_id == "calculate_electron_isodensity_surface"
        and backend_id == "multiwfn"
        and field_name == "grid_spacing_bohr"
        and "grid_spacing_angstrom" in settings
    )


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


def _validate_backend_resource_constraints(
    action_id: str,
    backend_id: str,
    request: ActionRequest,
    selected_backends: tuple[Any, ...],
    timeout_seconds: int,
) -> dict[str, Any] | None:
    resources = normalize_resource_limits(request.resource_limits)
    cpu_cores = resources["cpu_cores"]
    for selected in selected_backends:
        maximum = selected.resource_constraints.get("maximum_cpu_cores")
        if maximum is not None and cpu_cores > int(maximum):
            reason = selected.resource_constraints.get("reason")
            detail = f" Reason: {reason}" if reason else ""
            return _invalid(
                action_id,
                backend_id,
                f"resource_limits.cpu_cores={cpu_cores} exceeds the validated maximum "
                f"{maximum} for selected backend {selected.id!r}.{detail} Select resources "
                "or a backend explicitly; no resource substitution or fallback is performed.",
                code="invalid_resource_limits",
            )
        maximum_walltime = selected.resource_constraints.get(
            "maximum_walltime_seconds"
        )
        if maximum_walltime is not None and timeout_seconds > int(maximum_walltime):
            reason = selected.resource_constraints.get("walltime_reason")
            detail = f" Reason: {reason}" if reason else ""
            return _invalid(
                action_id,
                backend_id,
                f"The evaluator-controlled timeout_seconds={timeout_seconds} exceeds the "
                f"validated Action maximum {maximum_walltime} for selected backend "
                f"{selected.id!r}.{detail} Adjust the evaluation timeout policy before "
                "running this benchmark; the Agent cannot change this value.",
                code="invalid_timeout_policy",
            )
    try:
        validate_resource_limits(resources)
    except ResourceBudgetExceeded as exc:
        error = exc.as_error()
        return _invalid(
            action_id,
            backend_id,
            error["message"],
            code=error["code"],
            error_details={
                key: value
                for key, value in error.items()
                if key not in {"code", "message", "retryable"}
            },
            retryable=bool(error.get("retryable")),
        )
    return None


def _validate_artifact_input_semantics(
    action_id: str,
    backend_id: str,
    inputs: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Reject a typed ArtifactRef placed in a demonstrably incompatible slot."""

    if action_id == "export_electron_density_grid":
        value = inputs.get("electron_density")
        if (
            isinstance(value, Mapping)
            and value.get("artifact_id")
            and value.get("semantic_type") != "ElectronDensityResult"
        ):
            return _invalid(
                action_id,
                backend_id,
                "inputs.electron_density requires the primary ElectronDensityResult artifact "
                "returned by calculate_correlated_electron_density. Pass the output_artifacts "
                "item whose semantic_type is 'ElectronDensityResult', "
                "{'artifact_id': 'art_...'}, or that exact artifact-id string; do not pass "
                "result.files.gbw or another backend file path.",
                code="artifact_semantic_mismatch",
            )
        return None
    if action_id == "calculate_electron_isodensity_surface":
        value = inputs.get("density_file")
        if isinstance(value, Mapping) and value.get("artifact_id"):
            semantic_type = str(value.get("semantic_type") or "")
            suffix = PurePosixPath(str(value.get("path") or "")).suffix.casefold()
            if semantic_type not in {
                "ElectronDensityWavefunction",
                "ElectronDensityGrid",
                "BackendFile",
            } and suffix not in {
                ".fch", ".fchk", ".wfn", ".wfx", ".mwfn", ".molden", ".47", ".cube",
            }:
                return _invalid(
                    action_id,
                    backend_id,
                    "inputs.density_file requires a wavefunction or electron-density grid "
                    "artifact returned by export_electron_density_grid",
                    code="artifact_semantic_mismatch",
                )
        return None

    if action_id == "derive_thermochemistry" and backend_id == "internal_thermochemistry":
        expected = {
            "energy": "EnergyResult",
            "frequencies": "FrequencyResult",
        }
        for field_name, semantic_type in expected.items():
            value = inputs.get(field_name)
            if (
                isinstance(value, Mapping)
                and value.get("artifact_id")
                and value.get("semantic_type") != semantic_type
            ):
                next_step = (
                    " Call derive_vibrational_modes explicitly before thermochemistry; the "
                    "framework will not insert that Action automatically."
                    if field_name == "frequencies"
                    and value.get("semantic_type") == "Hessian"
                    else ""
                )
                return _invalid(
                    action_id,
                    backend_id,
                    f"inputs.{field_name} received ArtifactRef semantic_type="
                    f"{value.get('semantic_type')!r}; it requires {semantic_type}.{next_step}",
                    code="artifact_semantic_mismatch",
                )
        return None
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


def _validate_inline_atomic_structures(
    action_id: str,
    backend_id: str,
    inputs: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Reject malformed inline AtomicStructure values before starting a worker."""

    def validate(value: Any, path: str) -> str | None:
        if isinstance(value, list):
            for index, item in enumerate(value):
                message = validate(item, f"{path}[{index}]")
                if message is not None:
                    return message
            return None
        if not isinstance(value, Mapping) or value.get("artifact_id"):
            return None
        if "structure" in value and isinstance(value["structure"], Mapping):
            message = validate(value["structure"], f"{path}.structure")
            if message is not None:
                return message
        if "atoms" not in value:
            return None
        atoms = value["atoms"]
        if not isinstance(atoms, list) or not atoms:
            return f"{path}.atoms must be a non-empty array of atom mappings"
        for index, atom in enumerate(atoms):
            atom_path = f"{path}.atoms[{index}]"
            if not isinstance(atom, Mapping):
                return f"{atom_path} must be a mapping"
            if not (atom.get("element") or atom.get("symbol")):
                return f"{atom_path} requires element (canonical) or symbol"
            position = atom.get("position_angstrom")
            if position is None:
                position = atom.get("position")
            if position is None:
                received = "; received unsupported key 'xyz'" if "xyz" in atom else ""
                return (
                    f"{atom_path} requires position_angstrom=[x, y, z]{received}. "
                    "Canonical example: {'atoms': [{'element': 'H', "
                    "'position_angstrom': [0.0, 0.0, 0.0]}], 'charge': 0, "
                    "'multiplicity': 1}"
                )
            if not isinstance(position, (list, tuple)) or len(position) != 3:
                return f"{atom_path}.position_angstrom must contain exactly three values"
            try:
                numeric = [float(item) for item in position]
            except (TypeError, ValueError):
                return f"{atom_path}.position_angstrom must contain three numeric values"
            if not all(math.isfinite(item) for item in numeric):
                return f"{atom_path}.position_angstrom must contain three finite values"
        return None

    for field_name, value in inputs.items():
        message = validate(value, f"inputs.{field_name}")
        if message is not None:
            return _invalid(
                action_id,
                backend_id,
                message,
                code="invalid_atomic_structure",
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
    if "timeout_seconds" in request.action_settings:
        return _invalid(
            action_id,
            request.backend_id or request.source_id,
            "action_settings.timeout_seconds is controlled by the evaluation policy and "
            "cannot be supplied by the Agent",
            code="evaluator_controlled_timeout",
        )
    execution_timeout = timeout_seconds_for(specification.execution_class)
    timeout_policy = timeout_policy_record(specification.execution_class)
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
    invalid_aliases = _validate_deprecated_setting_aliases(
        action_id, backend_id, request.action_settings
    )
    if invalid_aliases is not None:
        return invalid_aliases

    missing_methods = [
        name
        for name in backend.required_method_fields.get(action_id, ())
        if name not in request.method_spec
    ]
    missing_settings = [
        name
        for name in backend.required_setting_fields.get(action_id, ())
        if not _required_setting_is_present(
            action_id, backend_id, name, request.action_settings
        )
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

    invalid_resources = _validate_backend_resource_constraints(
        action_id,
        backend_id,
        request,
        (backend, *component_specs),
        execution_timeout,
    )
    if invalid_resources is not None:
        return invalid_resources

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
    invalid_inline_structure = _validate_inline_atomic_structures(
        action_id, backend_id, request.inputs
    )
    if invalid_inline_structure is not None:
        return invalid_inline_structure
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
                "execution_timeout_policy": timeout_policy,
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
                "execution_timeout_policy": timeout_policy,
            },
        ).model_dump(mode="json")

    input_artifacts = collect_artifact_refs(request.inputs)
    execution_request = request.model_dump(mode="json")
    execution_request["resource_limits"].update(
        normalize_resource_limits(request.resource_limits)
    )
    execution_request["resource_limits"]["walltime_seconds"] = execution_timeout
    execution_request["action_settings"]["timeout_seconds"] = execution_timeout
    worker_payload = {
        "action_id": action_id,
        "backend_id": backend_id,
        "request": execution_request,
    }
    try:
        reservation = reserve_resources(
            execution_request["resource_limits"],
            kind="predefined_action",
            label=f"{action_id}/{backend_id}",
        )
    except ResourceBudgetExceeded as exc:
        error = exc.as_error()
        return _invalid(
            action_id,
            backend_id,
            error["message"],
            code=error["code"],
            error_details={key: value for key, value in error.items() if key not in {"code", "message", "retryable"}},
            retryable=bool(error.get("retryable")),
        )
    try:
        worker = invoke_worker(
            runtime=backend.runtime,
            payload=worker_payload,
            timeout_seconds=execution_timeout,
        )
    finally:
        reservation.release()
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
        "execution_timeout_policy": timeout_policy,
        "evaluation_resource_budget": resource_budget_record(),
        "requested_resource_limits": normalize_resource_limits(
            request.resource_limits
        ),
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

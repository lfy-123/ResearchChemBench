"""Neutral, task-independent progressive discovery over the frozen catalog."""

from __future__ import annotations

import re
from typing import Any, Literal

from .catalog import (
    CATEGORY_LABELS,
    active_catalog_snapshot,
    action_specs,
    backend_specs,
)
from .models import ActionSpec, BackendSpec


ActionKind = Literal["all", "scientific", "data"]


def _snapshot(value: dict[str, Any] | None = None) -> dict[str, Any]:
    return value if value is not None else active_catalog_snapshot()


def _backend_health(snapshot: dict[str, Any], backend_id: str) -> dict[str, Any]:
    for backend in snapshot.get("backends", []):
        if backend.get("id") == backend_id:
            return dict(backend.get("health") or {})
    return {}


def _health_status(snapshot: dict[str, Any], backend_id: str) -> str:
    return str(_backend_health(snapshot, backend_id).get("status") or "not_probed")


def _resource_summary(resource: dict[str, Any]) -> dict[str, Any]:
    return {
        "resource_id": resource.get("id"),
        "display_name": resource.get("display_name", resource.get("id")),
        "kind": resource.get("kind"),
        "version": resource.get("version"),
        "format": resource.get("format"),
        "available": bool(resource.get("available")),
        "selectable": bool(resource.get("selectable", True)),
        "compatible_backends": list(resource.get("compatible_backends") or []),
        "selection_syntax": resource.get("selection_syntax"),
        "element_count": resource.get("element_count"),
        "variant_count": resource.get("variant_count"),
        "model_branches": list(resource.get("model_branches") or []),
    }


def _registered_resources(
    snapshot: dict[str, Any], backend_id: str
) -> list[dict[str, Any]]:
    return [
        _resource_summary(resource)
        for resource in snapshot.get("resources", [])
        if backend_id in (resource.get("compatible_backends") or [])
    ]


def _provider_contract(
    backend: BackendSpec,
    action_id: str,
    snapshot: dict[str, Any],
    *,
    detailed: bool,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "backend_id": backend.id,
        "display_name": backend.display_name,
        "description": backend.description,
        "runtime": backend.runtime,
        "health_status": _health_status(snapshot, backend.id),
        "required_input_fields": list(backend.required_input_fields.get(action_id, ())),
        "required_method_fields": list(backend.required_method_fields.get(action_id, ())),
        "required_setting_fields": list(backend.required_setting_fields.get(action_id, ())),
        "allowed_method_values": {
            field: list(choices)
            for field, choices in backend.allowed_method_values.get(action_id, {}).items()
        },
        "allowed_setting_values": {
            field: list(choices)
            for field, choices in backend.allowed_setting_values.get(action_id, {}).items()
        },
        "required_component_roles": list(
            backend.required_component_roles.get(action_id, ())
        ),
        "component_backend_options": {
            role: list(options)
            for role, options in backend.component_backend_options.get(action_id, {}).items()
        },
        "supported_system_types": list(
            backend.supported_system_types.get(action_id, ())
        ),
        "validation_level": backend.validation_levels.get(action_id),
    }
    if detailed:
        value.update(
            {
                "health": _backend_health(snapshot, backend.id),
                "method_parameter_reference": dict(backend.method_schema),
                "registered_resources": _registered_resources(snapshot, backend.id),
                "required_external_data": list(backend.required_data_resources),
                "python_modules": list(backend.python_modules),
                "executables": list(backend.executables),
                "environment_variables": list(backend.environment_variables),
                "license_class": backend.license_class,
                "install_notes": backend.install_notes,
            }
        )
    return value


def _selection_instruction(specification: ActionSpec) -> str:
    providers = ", ".join(specification.backend_ids)
    if specification.selection_policy == "fixed_source":
        return (
            f"This Data Action uses the fixed source {providers}; omit backend_id and "
            "component_backends. source_id may be omitted or equal the fixed source."
        )
    if specification.selection_policy == "internal_deterministic":
        return (
            f"This deterministic Action uses {providers}; omit backend_id, source_id, and "
            "component_backends."
        )
    if specification.selection_policy == "agent_source_required":
        return f"Select exactly one source_id from: {providers}."
    if specification.selection_policy == "agent_components_required":
        return (
            f"Select exactly one backend_id from: {providers}, then provide every component role "
            "required by that provider."
        )
    return f"Select exactly one backend_id from: {providers}."


def list_action_domains(*, snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    current = _snapshot(snapshot)
    actions = list(current.get("actions", []))
    domains = []
    for category, label in CATEGORY_LABELS.items():
        values = [action for action in actions if action.get("category") == category]
        domains.append(
            {
                "category": category,
                "description": label,
                "action_count": len(values),
                "scientific_action_count": sum(
                    not bool(action.get("data_action")) for action in values
                ),
                "data_action_count": sum(
                    bool(action.get("data_action")) for action in values
                ),
            }
        )
    return {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "catalog_visibility_policy": "complete_task_independent",
        "task_specific_filtering": False,
        "count": len(domains),
        "domains": domains,
    }


def search_actions(
    *,
    query: str | None = None,
    category: str | None = None,
    backend_id: str | None = None,
    action_kind: ActionKind = "all",
    available_only: bool = False,
    limit: int = 20,
    offset: int = 0,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = _snapshot(snapshot)
    actions = action_specs()
    backends = backend_specs()
    if category is not None and category not in CATEGORY_LABELS:
        raise ValueError(
            f"Unknown category {category!r}; choose one returned by list_action_domains"
        )
    if backend_id is not None and backend_id not in backends:
        raise ValueError(f"Unknown backend_id {backend_id!r}")
    terms = [term for term in re.split(r"\s+", (query or "").casefold().strip()) if term]
    matches: list[ActionSpec] = []
    for specification in sorted(actions.values(), key=lambda item: item.id):
        if category is not None and specification.category != category:
            continue
        if backend_id is not None and backend_id not in specification.backend_ids:
            continue
        if action_kind == "scientific" and specification.data_action:
            continue
        if action_kind == "data" and not specification.data_action:
            continue
        provider_values = [backends[item] for item in specification.backend_ids]
        if available_only and not any(
            _health_status(current, provider.id) == "available"
            for provider in provider_values
        ):
            continue
        haystack = " ".join(
            [
                specification.id,
                specification.category,
                CATEGORY_LABELS.get(specification.category, ""),
                specification.description,
                specification.primary_output,
                specification.input_description,
                *specification.required_inputs,
                *specification.optional_inputs,
                *(provider.id for provider in provider_values),
                *(provider.display_name for provider in provider_values),
                *(provider.description for provider in provider_values),
            ]
        ).casefold()
        if terms and not all(term in haystack for term in terms):
            continue
        matches.append(specification)

    page = matches[offset : offset + limit]
    results = []
    for specification in page:
        providers = [
            {
                "backend_id": backend,
                "display_name": backends[backend].display_name,
                "health_status": _health_status(current, backend),
            }
            for backend in specification.backend_ids
        ]
        results.append(
            {
                "action_id": specification.id,
                "category": specification.category,
                "description": specification.description,
                "primary_output": specification.primary_output,
                "data_action": specification.data_action,
                "selection_policy": specification.selection_policy,
                "providers": providers,
            }
        )
    next_offset = offset + len(page)
    return {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "query": query,
        "filters": {
            "category": category,
            "backend_id": backend_id,
            "action_kind": action_kind,
            "available_only": available_only,
        },
        "ordering": "stable_action_id_order_not_relevance_ranked",
        "total_matches": len(matches),
        "offset": offset,
        "count": len(results),
        "next_offset": next_offset if next_offset < len(matches) else None,
        "actions": results,
    }


def inspect_action(
    action_id: str,
    *,
    backend_id: str | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = _snapshot(snapshot)
    actions = action_specs()
    backends = backend_specs()
    if action_id not in actions:
        raise KeyError(f"Unknown action_id {action_id!r}")
    specification = actions[action_id]
    if backend_id is not None and backend_id not in specification.backend_ids:
        raise ValueError(
            f"Backend {backend_id!r} does not provide {action_id!r}; choose one of "
            f"{list(specification.backend_ids)}"
        )
    selected = (
        [backend_id] if backend_id is not None else list(specification.backend_ids)
    )
    provider_contracts = [
        _provider_contract(
            backends[item],
            action_id,
            current,
            detailed=backend_id is not None or len(selected) == 1,
        )
        for item in selected
    ]
    return {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "action": specification.as_dict(),
        "selection_instruction": _selection_instruction(specification),
        "execute_with": "execute_action",
        "action_request_fields": [
            "action_id",
            "backend_id",
            "component_backends",
            "source_id",
            "inputs",
            "method_spec",
            "action_settings",
            "resource_limits",
        ],
        "provider_contracts": provider_contracts,
        "detail_note": (
            "Exact details for the requested provider are included."
            if backend_id is not None or len(selected) == 1
            else "Provider summaries are included. Call inspect_action again with backend_id for "
            "that provider's full parameter, health, runtime, and resource reference."
        ),
        "automatic_fallback": False,
    }


def inspect_backend(
    backend_id: str,
    *,
    action_id: str | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = _snapshot(snapshot)
    actions = action_specs()
    backends = backend_specs()
    if backend_id not in backends:
        raise KeyError(f"Unknown backend_id {backend_id!r}")
    backend = backends[backend_id]
    if action_id is not None and action_id not in backend.capabilities:
        raise ValueError(
            f"Backend {backend_id!r} does not provide {action_id!r}; its capabilities are "
            f"{list(backend.capabilities)}"
        )
    capabilities = [
        {
            "action_id": item,
            "category": actions[item].category,
            "description": actions[item].description,
            "primary_output": actions[item].primary_output,
            "selection_policy": actions[item].selection_policy,
        }
        for item in backend.capabilities
    ]
    result: dict[str, Any] = {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "backend": {
            "backend_id": backend.id,
            "display_name": backend.display_name,
            "description": backend.description,
            "runtime": backend.runtime,
            "health": _backend_health(current, backend.id),
            "python_modules": list(backend.python_modules),
            "executables": list(backend.executables),
            "environment_variables": list(backend.environment_variables),
            "conda_packages": list(backend.conda_packages),
            "pip_packages": list(backend.pip_packages),
            "required_external_data": list(backend.required_data_resources),
            "license_class": backend.license_class,
            "install_notes": backend.install_notes,
            "method_parameter_reference": dict(backend.method_schema),
            "registered_resources": _registered_resources(current, backend.id),
        },
        "capability_count": len(capabilities),
        "capabilities": capabilities,
    }
    if action_id is not None:
        result["action_contract"] = _provider_contract(
            backend, action_id, current, detailed=True
        )
    return result


def search_resources(
    *,
    query: str | None = None,
    backend_id: str | None = None,
    available_only: bool = False,
    limit: int = 20,
    offset: int = 0,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = _snapshot(snapshot)
    if backend_id is not None and backend_id not in backend_specs():
        raise ValueError(f"Unknown backend_id {backend_id!r}")
    terms = [term for term in re.split(r"\s+", (query or "").casefold().strip()) if term]
    matches = []
    for resource in sorted(current.get("resources", []), key=lambda item: str(item.get("id"))):
        if backend_id is not None and backend_id not in (
            resource.get("compatible_backends") or []
        ):
            continue
        if available_only and not bool(resource.get("available")):
            continue
        haystack = " ".join(
            str(value)
            for value in (
                resource.get("id"),
                resource.get("display_name"),
                resource.get("kind"),
                resource.get("version"),
                resource.get("format"),
                " ".join(resource.get("compatible_backends") or []),
            )
            if value is not None
        ).casefold()
        if terms and not all(term in haystack for term in terms):
            continue
        matches.append(resource)
    page = matches[offset : offset + limit]
    next_offset = offset + len(page)
    return {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "ordering": "stable_resource_id_order_not_relevance_ranked",
        "total_matches": len(matches),
        "offset": offset,
        "count": len(page),
        "next_offset": next_offset if next_offset < len(matches) else None,
        "resources": [_resource_summary(resource) for resource in page],
    }


def inspect_resource(
    resource_id: str,
    *,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = _snapshot(snapshot)
    for resource in current.get("resources", []):
        if resource.get("id") == resource_id:
            return {
                "status": "success",
                "catalog_hash": current.get("catalog_hash"),
                "resource": resource,
                "selection_note": (
                    "Use the exact registered selection_syntax and explicitly choose every "
                    "required element, variant, model branch, device, or compatible method."
                ),
            }
    raise KeyError(f"Unknown resource_id {resource_id!r}")


__all__ = [
    "inspect_action",
    "inspect_backend",
    "inspect_resource",
    "list_action_domains",
    "search_actions",
    "search_resources",
]

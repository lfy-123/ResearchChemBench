"""Full, immutable-per-run Action/Data/Backend catalog for the benchmark."""

from __future__ import annotations

import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

from .models import ActionSpec, BackendSpec
from .runtime import probe_all_backends
from .resources import resource_snapshot, resources_for_backends
from .specs import ACTION_SPECS, BACKEND_SPECS


CATEGORY_LABELS = {
    "structure_and_system": "Structure, conformers, charges, and system construction",
    "molecular_electronic": "Molecular electronic structure and derived properties",
    "reaction_and_kinetics": "Reaction paths, equilibrium, and kinetics",
    "molecular_dynamics": "Molecular dynamics propagation and trajectory analysis",
    "periodic_and_phonons": "Periodic electronic structure and lattice dynamics",
    "docking": "Molecular docking",
    "data_sources": "External chemistry data sources",
}


def _resource_coverage(resource: dict[str, Any]) -> str:
    kind = resource.get("kind")
    if kind == "element_file_collection":
        return f"{resource.get('element_count', 0)} elements"
    if kind == "variant_file_collection":
        return (
            f"{resource.get('variant_count', 0)} exact variants/"
            f"{resource.get('element_count', 0)} elements"
        )
    if kind == "slater_koster_parameter_set":
        return (
            f"{resource.get('element_count', 0)} elements/"
            f"{resource.get('pair_count', 0)} directed pairs"
        )
    if kind == "model_checkpoint":
        branches = resource.get("model_branches") or []
        if branches:
            return f"one exact checkpoint/{len(branches)} explicit branches"
        if resource.get("single_task"):
            return "one exact single-task checkpoint"
        return "one exact checkpoint"
    if kind == "single_file_resource":
        return "one exact registered file"
    return "runtime-managed executable"


def action_specs() -> dict[str, ActionSpec]:
    return {spec.id: spec for spec in ACTION_SPECS}


def backend_specs() -> dict[str, BackendSpec]:
    return {spec.id: spec for spec in BACKEND_SPECS}


def validate_catalog() -> None:
    actions = action_specs()
    backends = backend_specs()
    if len(actions) != len(ACTION_SPECS):
        raise ValueError("Duplicate action ids in catalog")
    if len(backends) != len(BACKEND_SPECS):
        raise ValueError("Duplicate backend ids in catalog")
    for specification in ACTION_SPECS:
        specification.validate()
        unknown = sorted(set(specification.backend_ids) - set(backends))
        if unknown:
            raise ValueError(f"Action {specification.id} references unknown backends: {unknown}")
        for backend_id in specification.backend_ids:
            if specification.id not in backends[backend_id].capabilities:
                raise ValueError(
                    f"Action {specification.id} is missing from backend {backend_id} capabilities"
                )
    for specification in BACKEND_SPECS:
        specification.validate()
        unknown = sorted(set(specification.capabilities) - set(actions))
        if unknown:
            raise ValueError(f"Backend {specification.id} references unknown actions: {unknown}")
        for action_id in specification.capabilities:
            if specification.id not in actions[action_id].backend_ids:
                raise ValueError(
                    f"Backend {specification.id} is missing from action {action_id} choices"
                )
    scientific = [spec for spec in ACTION_SPECS if not spec.data_action]
    data = [spec for spec in ACTION_SPECS if spec.data_action]
    if len(scientific) != 40 or len(data) != 5:
        raise ValueError(
            f"Catalog must contain 40 Scientific Actions and 5 Data Actions; "
            f"received {len(scientific)} and {len(data)}"
        )


def catalog_snapshot(*, include_health: bool = True) -> dict[str, Any]:
    validate_catalog()
    health = probe_all_backends(BACKEND_SPECS) if include_health else {}
    payload: dict[str, Any] = {
        "schema_version": 3,
        "exposure_policy": "atomic_all",
        "backend_selection_policy": "agent_required",
        "scientific_resource_selection_policy": "agent_explicit_no_default",
        "automatic_fallback": False,
        "actions": [spec.as_dict() for spec in ACTION_SPECS],
        "backends": [
            {**spec.as_dict(), "health": health.get(spec.id)}
            for spec in BACKEND_SPECS
        ],
        "resources": resource_snapshot(),
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["catalog_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def catalog_hash(*, include_health: bool = False) -> str:
    return str(catalog_snapshot(include_health=include_health)["catalog_hash"])


def active_catalog_snapshot() -> dict[str, Any]:
    configured = (
        os.environ.get("RESEARCHCHEM_MCP_WORKSPACE", "").strip()
        or os.environ.get("RESEARCHCHEMBENCH_WORKSPACE", "").strip()
    )
    if configured:
        path = Path(configured).expanduser().resolve() / "_toolbox_catalog.json"
        if path.is_file():
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict) and value.get("catalog_hash"):
                return value
    return catalog_snapshot(include_health=True)


def active_catalog_hash() -> str:
    return str(active_catalog_snapshot()["catalog_hash"])


def mcp_action_description(specification: ActionSpec) -> str:
    backend_text = ", ".join(specification.backend_ids)
    backends = backend_specs()
    requirement_parts = []
    backend_notes = []
    for backend_id in specification.backend_ids:
        backend = backends[backend_id]
        method_fields = backend.required_method_fields.get(specification.id, ())
        setting_fields = backend.required_setting_fields.get(specification.id, ())
        details = []
        if method_fields:
            details.append("method_spec=" + ",".join(method_fields))
        if setting_fields:
            details.append("action_settings=" + ",".join(setting_fields))
        requirement_parts.append(
            backend_id + (" [" + "; ".join(details) + "]" if details else "")
        )
        note = f"{backend_id}: {backend.description}"
        if backend.required_data_resources:
            note += " External data: " + "; ".join(backend.required_data_resources)
        registered_resources = resources_for_backends((backend_id,))
        if registered_resources:
            resource_text = ", ".join(
                f"{item['id']} ({item.get('selection_syntax', 'runtime-managed')})"
                for item in registered_resources
            )
            note += " Registered resources: " + resource_text
        backend_notes.append(note)
    requirement = (
        f"backend_id is optional and, if supplied, must be {backend_text}."
        if specification.data_action
        else f"backend_id is required; choose exactly one of: {backend_text}."
    )
    required = ", ".join(specification.required_inputs) or "none"
    optional = ", ".join(specification.optional_inputs) or "none"
    input_contract = specification.input_description or "structured inputs described by the action"
    return (
        f"{specification.description} Primary output: {specification.primary_output}. "
        f"Input contract: {input_contract}. "
        f"Required inputs keys: {required}. Optional inputs keys: {optional}. "
        f"{requirement} Backend-specific required fields: {' | '.join(requirement_parts)}. "
        f"Backend notes: {' | '.join(backend_notes)}. "
        "The system validates and executes the exact choice; it never "
        "selects or falls back to another backend."
    )


def agent_toolbox_overview(
    *,
    include_health: bool = True,
    snapshot: dict[str, Any] | None = None,
) -> str:
    """Neutral system-prompt summary; it contains no workflow recipe or ranking."""

    if snapshot is not None:
        health = {
            backend["id"]: backend.get("health") or {}
            for backend in snapshot.get("backends", [])
        }
    else:
        health = probe_all_backends(BACKEND_SPECS) if include_health else {}
    grouped: dict[str, list[ActionSpec]] = defaultdict(list)
    for specification in ACTION_SPECS:
        grouped[specification.category].append(specification)
    lines = [
        "All tasks receive this same complete atomic tool catalog. You decide which tools "
        "to call, their order, and the backend/method for every computation. There is no "
        "hidden workflow, task-specific tool retrieval, automatic backend selection, or fallback.",
        "",
        "Every tool accepts one ActionRequest object with: backend_id, inputs, method_spec, "
        "action_settings, and optional resource_limits. backend_id is mandatory for Scientific "
        "Actions. Read each tool description before calling it; it lists the exact required keys "
        "for each backend.",
        "",
        "A minimal AtomicStructure is {'atoms': [{'element': 'H', "
        "'position_angstrom': [0, 0, 0]}], 'charge': 0, 'multiplicity': 1}. "
        "Periodic structures additionally contain a 3x3 cell_angstrom and pbc=[true,true,true]. "
        "Outputs can be passed onward as structured result objects or registered ArtifactRef objects.",
        "Scientific files use explicit registered ResourceRef values. Use either "
        "resource://<resource_id>/<Element> for element-file collections or "
        "resource://<resource_id>/<Variant> for exact variant collections such as VASP POTCARs, or "
        "resource://<resource_id> for a parameter set, model checkpoint, or other registered "
        "single file. You must choose the resource family/variant/checkpoint, element mapping, model "
        "branch, device, cutoffs, and compatible method; the dispatcher never chooses them.",
    ]
    for category in CATEGORY_LABELS:
        lines.extend(["", f"### {CATEGORY_LABELS[category]}"])
        for specification in grouped.get(category, []):
            backend_parts = []
            for backend_id in specification.backend_ids:
                state = health.get(backend_id, {}).get("status")
                backend_parts.append(f"{backend_id} ({state})" if state else backend_id)
            lines.append(
                f"- `{specification.id}` — {specification.description} "
                f"Backends/data source: {', '.join(backend_parts)}."
            )
    lines.extend(
        [
            "",
            "### Registered read-only scientific resources",
        ]
    )
    resource_values = snapshot.get("resources", []) if snapshot is not None else resource_snapshot()
    for resource in resource_values:
        backends_text = ", ".join(resource.get("compatible_backends") or [])
        state = "available" if resource.get("available") else "unavailable"
        if resource.get("selectable", True):
            coverage = _resource_coverage(resource)
            lines.append(
                f"- `{resource['id']}` — {resource.get('display_name', resource['id'])}; "
                f"backend: {backends_text}; format: {resource.get('format', '-')}; "
                f"coverage: {coverage}; status: {state}; syntax: `{resource.get('selection_syntax')}`."
            )
        else:
            lines.append(
                f"- `{resource['id']}` — runtime-managed resource for {backends_text}; status: {state}."
            )
    lines.extend(
        [
            "",
            "An unavailable backend remains visible so that the choice set is not hidden. "
            "If a call fails, inspect that exact result and independently decide whether to "
            "change parameters, call another tool, or submit a new call with another backend.",
        ]
    )
    return "\n".join(lines)


def markdown_catalog(*, include_health: bool = True) -> str:
    snapshot = catalog_snapshot(include_health=include_health)
    lines = [
        "# ResearchChem Atomic Tool Catalog",
        "",
        f"Catalog hash: `{snapshot['catalog_hash']}`",
        "",
        "The benchmark exposes every action below for every task. Backends are selected by the agent.",
        "",
        "| Action | Category | Primary output | Backends | Required inputs | Description |",
        "|---|---|---|---|---|---|",
    ]
    for action in snapshot["actions"]:
        lines.append(
            "| {id} | {category} | {primary_output} | {backends} | {required} | {description} |".format(
                id=action["id"],
                category=action["category"],
                primary_output=action["primary_output"],
                backends=", ".join(action["backend_ids"]),
                required=", ".join(action["required_inputs"]),
                description=action["description"].replace("|", "\\|"),
            )
        )
    lines.extend(
        [
            "",
            "## Registered scientific resources",
            "",
            "| Resource | Kind | Backends | Version | Format | Status | Explicit selection syntax | Coverage |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for resource in snapshot["resources"]:
        coverage = _resource_coverage(resource)
        lines.append(
            "| {id} | {kind} | {backends} | {version} | {format} | {status} | {syntax} | {coverage} |".format(
                id=resource["id"],
                kind=resource.get("kind", "-"),
                backends=", ".join(resource.get("compatible_backends") or []),
                version=resource.get("version", "-"),
                format=resource.get("format", "-"),
                status="available" if resource.get("available") else "unavailable",
                syntax=resource.get("selection_syntax", "runtime-managed"),
                coverage=coverage,
            )
        )
    lines.extend(
        [
            "",
            "## Backend installation and health",
            "",
            "| Backend | Runtime | Status | Conda packages | Pip packages | Executables | External scientific data | License |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for backend in snapshot["backends"]:
        health_item = backend.get("health") or {}
        lines.append(
            "| {id} | {runtime} | {status} | {conda} | {pip} | {executables} | {data} | {license} |".format(
                id=backend["id"],
                runtime=backend["runtime"],
                status=health_item.get("status", "not_probed"),
                conda=", ".join(backend["conda_packages"]),
                pip=", ".join(backend["pip_packages"]),
                executables=", ".join(backend["executables"]),
                data="; ".join(backend["required_data_resources"]).replace("|", "\\|"),
                license=backend["license_class"],
            )
        )
    return "\n".join(lines) + "\n"

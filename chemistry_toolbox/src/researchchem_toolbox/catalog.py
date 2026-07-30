"""Full, immutable-per-run Action/Data/Backend catalog for the benchmark."""

from __future__ import annotations

import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Literal

from .models import ActionSpec, BackendSpec
from .runtime import probe_all_backends
from .resources import resource_snapshot, resources_for_backends
from .specs import ACTION_SPECS, BACKEND_SPECS
from .parameter_specs import RESOURCE_LIMIT_PARAMETER_SPECS, common_fixed_parameter_specs
from .resource_budget import resource_budget_record
from .timeout_policy import timeout_policy_record


CATEGORY_LABELS = {
    "scientific_data_interchange": "Scientific records, schemas, and output parsing",
    "structure_and_system": "Structure, conformers, charges, and system construction",
    "cheminformatics": "Molecular descriptors, fingerprints, identifiers, and graph operations",
    "molecular_electronic": "Molecular electronic structure and derived properties",
    "reaction_and_kinetics": "Reaction paths, equilibrium, and kinetics",
    "molecular_dynamics": "Molecular dynamics propagation and trajectory analysis",
    "periodic_and_phonons": "Periodic electronic structure and lattice dynamics",
    "docking": "Molecular docking",
    "data_sources": "External chemistry data sources",
}


TOOL_DISCOVERY_MODE_ENV = "RESEARCHCHEM_TOOL_DISCOVERY_MODE"
ToolDiscoveryMode = Literal["progressive", "full"]


def resolve_tool_discovery_mode(value: str | None = None) -> ToolDiscoveryMode:
    """Resolve the public MCP surface without changing catalog membership.

    ``progressive`` exposes neutral catalog-discovery tools plus one explicit
    Action dispatcher. ``full`` retains the historical one-MCP-tool-per-Action
    surface for regression comparisons. Both modes make the same immutable
    task-independent catalog available and neither performs task retrieval.
    """

    raw = value
    if raw is None:
        raw = os.environ.get(TOOL_DISCOVERY_MODE_ENV, "progressive")
    normalized = str(raw).strip().lower().replace("-", "_")
    aliases = {
        "progressive": "progressive",
        "progressive_discovery": "progressive",
        "full": "full",
        "atomic_all": "full",
    }
    try:
        return aliases[normalized]  # type: ignore[return-value]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported tool discovery mode {raw!r}; choose progressive or full"
        ) from exc


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
        for action_id, roles in specification.component_backend_options.items():
            for role, options in roles.items():
                unknown_components = sorted(set(options) - set(backends))
                if unknown_components:
                    raise ValueError(
                        f"Backend {specification.id}/{action_id} role {role} references "
                        f"unknown component backends: {unknown_components}"
                    )
    scientific = [spec for spec in ACTION_SPECS if not spec.data_action]
    data = [spec for spec in ACTION_SPECS if spec.data_action]
    if not scientific or not data:
        raise ValueError("Catalog requires both Scientific Actions and Data Actions")


def catalog_snapshot(
    *,
    include_health: bool = True,
    discovery_mode: str | None = None,
    resource_budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_catalog()
    mode = resolve_tool_discovery_mode(discovery_mode)
    health = probe_all_backends(BACKEND_SPECS) if include_health else {}
    payload: dict[str, Any] = {
        "schema_version": 7,
        "execution_layers": [
            {
                "id": "predefined_actions",
                "role": "validated common scientific operations",
                "mandatory": False,
            },
            {
                "id": "native_software",
                "role": "Agent-authored native inputs and exact allowlisted commands",
                "mandatory": False,
            },
            {
                "id": "programmable_analysis",
                "role": "Agent-authored programs in explicitly selected chemistry runtimes",
                "mandatory": False,
            },
        ],
        "discovery_mode": mode,
        "exposure_policy": (
            "progressive_discovery" if mode == "progressive" else "atomic_all"
        ),
        "catalog_visibility_policy": "complete_task_independent",
        "task_specific_tool_filtering": False,
        "backend_selection_policy": "per_action_explicit",
        "provider_selection_policies": sorted(
            {spec.selection_policy for spec in ACTION_SPECS}
        ),
        "scientific_resource_selection_policy": "agent_explicit_no_default",
        "automatic_fallback": False,
        "evaluation_resource_budget": resource_budget or resource_budget_record(),
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
        input_fields = backend.required_input_fields.get(specification.id, ())
        method_fields = backend.required_method_fields.get(specification.id, ())
        setting_fields = backend.required_setting_fields.get(specification.id, ())
        method_choices = backend.allowed_method_values.get(specification.id, {})
        setting_choices = backend.allowed_setting_values.get(specification.id, {})
        component_roles = backend.required_component_roles.get(specification.id, ())
        component_options = backend.component_backend_options.get(specification.id, {})
        details = []
        if input_fields:
            details.append("inputs=" + ",".join(input_fields))
        if method_fields:
            details.append("method_spec=" + ",".join(method_fields))
        if setting_fields:
            details.append("action_settings=" + ",".join(setting_fields))
        for field_name, choices in method_choices.items():
            details.append(
                f"method_spec.{field_name}=[{'|'.join(str(choice) for choice in choices)}]"
            )
        for field_name, choices in setting_choices.items():
            details.append(
                f"action_settings.{field_name}=[{'|'.join(str(choice) for choice in choices)}]"
            )
        if component_roles:
            details.append(
                "component_backends="
                + ",".join(
                    f"{role}:[{'|'.join(component_options.get(role, ()))}]"
                    for role in component_roles
                )
            )
        requirement_parts.append(
            backend_id + (" [" + "; ".join(details) + "]" if details else "")
        )
        note = f"{backend_id}: {backend.description}"
        if backend.method_schema:
            note += " Explicit parameter schema: " + "; ".join(
                f"{name}={description}"
                for name, description in backend.method_schema.items()
            )
        if backend.required_data_resources:
            note += " External data: " + "; ".join(backend.required_data_resources)
        registered_resources = resources_for_backends((backend_id,))
        if registered_resources:
            resource_text = ", ".join(
                f"{item['id']} ({item.get('selection_syntax', 'runtime-managed')})"
                for item in registered_resources
            )
            note += " Registered resources: " + resource_text
        parameter_specs = backend.parameter_specs.get(specification.id, {})
        if parameter_specs:
            required_parameter_paths = {
                *(f"inputs.{name}" for name in (*specification.required_inputs, *input_fields)),
                *(f"method_spec.{name}" for name in method_fields),
                *(f"action_settings.{name}" for name in setting_fields),
            }
            note += " Agent-controllable parameter metadata: " + "; ".join(
                (
                    f"{field_path} "
                    + (
                        "required"
                        if field_path in required_parameter_paths
                        else f"optional default={metadata.get('default')!r}"
                    )
                    + ": "
                    f"{metadata.get('description')} Impact: {metadata.get('impact', 'documented by the backend contract')}"
                )
                for field_path, metadata in parameter_specs.items()
            )
        fixed_specs = common_fixed_parameter_specs(
            runtime=backend.runtime,
            executables=backend.executables,
            python_modules=backend.python_modules,
            resource_constraints=backend.resource_constraints,
            validation_level=backend.validation_levels.get(specification.id),
        )
        fixed_specs.update(backend.fixed_parameter_specs.get(specification.id, {}))
        if fixed_specs:
            note += " Backend-fixed parameters: " + "; ".join(
                f"{field_path}: {metadata.get('description')} Reason: {metadata.get('reason', 'backend implementation constraint')}"
                for field_path, metadata in fixed_specs.items()
            )
        backend_notes.append(note)
    policy = specification.selection_policy
    if policy == "fixed_source":
        requirement = f"The fixed data source is {backend_text}; backend_id/source_id are not required."
    elif policy == "internal_deterministic":
        requirement = f"The deterministic internal provider is {backend_text}; backend_id is not required."
    elif policy == "agent_source_required":
        requirement = f"source_id is required; choose exactly one of: {backend_text}."
    elif policy == "agent_components_required":
        requirement = (
            f"backend_id is required; choose exactly one primary backend from: {backend_text}. "
            "Also supply every component_backends role required by that backend."
        )
    else:
        requirement = f"backend_id is required; choose exactly one of: {backend_text}."
    required = ", ".join(specification.required_inputs) or "none"
    optional = ", ".join(specification.optional_inputs) or "none"
    input_contract = specification.input_description or "structured inputs described by the action"
    timeout_policy = timeout_policy_record(specification.execution_class)
    budget = resource_budget_record()
    batch_note = (
        "For two or more independent inputs using this same Action and Backend, use "
        "submit_action_batch; repeated execute_action calls are synchronous and serial. "
        if specification.batch_safe
        else ""
    )
    return (
        f"{specification.description} Primary output: {specification.primary_output}. "
        f"Input contract: {input_contract}. "
        f"Required inputs keys: {required}. Optional inputs keys: {optional}. "
        f"{requirement} Backend-specific required fields: {' | '.join(requirement_parts)}. "
        f"Backend notes: {' | '.join(backend_notes)}. "
        "Global optional resource_limits and defaults: "
        + "; ".join(
            f"{name}={metadata.get('default')!r} ({metadata.get('impact')})"
            for name, metadata in RESOURCE_LIMIT_PARAMETER_SPECS.items()
        )
        + ". "
        f"Execution class: {specification.execution_class}; timeout is evaluator-controlled "
        f"at {timeout_policy['timeout_seconds']} seconds and cannot be supplied by the Agent. "
        f"Per-task evaluator resource budget: cpu_cores={budget['cpu_cores']}, "
        f"memory_mb={budget['memory_mb']}, gpu_count={budget['gpu_count']}; individual and "
        "concurrent requests above it are rejected without automatic reduction. "
        f"{batch_note}"
        f"Provider selection policy: {policy}. The system validates and executes the exact "
        "declared provider choices; it never falls back to another backend or source."
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
    budget = (
        dict(snapshot.get("evaluation_resource_budget") or {})
        if snapshot is not None
        else resource_budget_record()
    )
    if not budget:
        budget = resource_budget_record()
    grouped: dict[str, list[ActionSpec]] = defaultdict(list)
    for specification in ACTION_SPECS:
        grouped[specification.category].append(specification)
    lines = [
        "Layer 1 exposes this same complete predefined Action catalog to every task. These "
        "Actions are validated conveniences for common operations, not a required workflow or "
        "the boundary of the toolbox. You decide which tools "
        "to call, their order, and every scientifically meaningful backend, component, source, "
        "and method choice. There is no "
        "hidden workflow, task-specific tool retrieval, automatic backend selection, or fallback.",
        "",
        (
            "Evaluator-controlled per-task resource budget: "
            f"cpu_cores={budget['cpu_cores']}, "
            f"memory_mb={budget['memory_mb']}, "
            f"gpu_count={budget['gpu_count']}. The Agent may choose requests "
            "within this envelope; single requests and concurrent reservations above it are "
            "rejected without automatic reduction."
        ),
        "",
        "Every predefined Action accepts one ActionRequest object with: backend_id, component_backends, "
        "source_id, inputs, method_spec, action_settings, and optional resource_limits. Read each "
        "tool description before calling it: numerical computations require an Agent-selected "
        "backend; composite computations also require every component role; fixed-source data and "
        "deterministic internal Actions do not require a fake backend choice.",
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
                f"Providers: {', '.join(backend_parts)}. Selection policy: "
                f"{specification.selection_policy}."
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
            "change parameters, call another Action, use the native-software layer, or write an "
            "analysis program. The system never makes that decision for you.",
        ]
    )
    return "\n".join(lines)


def progressive_toolbox_overview(
    *,
    snapshot: dict[str, Any] | None = None,
) -> str:
    """Compact first-layer index for on-demand, neutral catalog discovery."""

    actions = (
        list(snapshot.get("actions", []))
        if snapshot is not None
        else [specification.as_dict() for specification in ACTION_SPECS]
    )
    backends = (
        list(snapshot.get("backends", []))
        if snapshot is not None
        else [specification.as_dict() for specification in BACKEND_SPECS]
    )
    resources = (
        list(snapshot.get("resources", []))
        if snapshot is not None
        else resource_snapshot()
    )
    budget = (
        dict(snapshot.get("evaluation_resource_budget") or {})
        if snapshot is not None
        else resource_budget_record()
    )
    if not budget:
        budget = resource_budget_record()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for action in actions:
        grouped[str(action.get("category", ""))].append(action)

    scientific_count = sum(not bool(action.get("data_action")) for action in actions)
    data_count = len(actions) - scientific_count
    lines = [
        "The same complete, task-independent chemistry catalog is available to every task, but it "
        "is loaded progressively instead of placing every Action schema in the initial context. "
        f"The frozen catalog contains {len(actions)} predefined Actions "
        f"({scientific_count} Scientific Actions and {data_count} Data Actions), "
        f"{len(backends)} Backend entries, and {len(resources)} registered scientific resources. "
        "No task-specific retrieval, recommendation, ranking, automatic backend selection, retry, "
        "or fallback is performed.",
        "",
        (
            "Evaluator-controlled per-task resource budget: "
            f"cpu_cores={budget['cpu_cores']}, "
            f"memory_mb={budget['memory_mb']}, "
            f"gpu_count={budget['gpu_count']}. "
            "Single requests and the sum of concurrently active managed jobs cannot exceed it; "
            "the framework rejects excess requests rather than reducing them."
        ),
        "",
        "If you do not know the exact Action id, call `list_action_domains` once to receive every "
        "action_id grouped under the compact domain index; use `search_actions` when you need to "
        "filter those catalog entries with your own scientific terms or an exact category/backend "
        "filter. Call `inspect_action` before a new "
        "Action to obtain its exact inputs, provider policy, provider-specific field types, "
        "conditional rules, output contract, and fill-in `execute_action` request template; use "
        "`inspect_backend` to see one Backend's capabilities. Scientific files and model/data "
        "families are found with `search_resources` and resolved exactly with `inspect_resource`. "
        "These discovery operations only return catalog facts.",
        "",
        "Run a selected predefined Action through `execute_action`. Its request contains an explicit "
        "action_id plus backend_id, component_backends, source_id, inputs, method_spec, "
        "action_settings, and resource_limits. Numerical Actions require the provider choices "
        "declared by `inspect_action`; fixed-source and deterministic internal Actions do not accept "
        "invented provider choices. The dispatcher validates exactly what you provide and never "
        "substitutes another choice. `execute_action` is synchronous: obey any provider-specific "
        "maximum walltime returned by `inspect_action`.",
        "For two or more independent inputs that use the same batch_safe Action and Backend, use "
        "`submit_action_batch` instead of repeated `execute_action` calls. The batch tool runs "
        "children concurrently, derives safe concurrency from the active CPU, memory, and GPU "
        "budget, queues excess items, and preserves independent results and provenance.",
        "",
        "For capabilities outside the predefined Action layer, the software-native and programmable "
        "layers remain peers. Discover exact installed programs with `list_software`, retrieve one "
        "reviewed invocation guide with `inspect_software`, and search its cached manuals with "
        "`search_software_documentation`. You may instead author a complete Python analysis program "
        "and explicitly select a listed runtime. For a calculation longer than a synchronous Action "
        "permits, author the complete native input, call `submit_native_job`, and explicitly poll or "
        "collect that job; submission does not change the selected software or parameters. You "
        "decide whether and how to interleave all three layers.",
        "",
        "Available Action domains:",
    ]
    for category, label in CATEGORY_LABELS.items():
        values = grouped.get(category, [])
        scientific = sum(not bool(value.get("data_action")) for value in values)
        data = len(values) - scientific
        kind_text = f"{scientific} scientific"
        if data:
            kind_text += f", {data} data"
        lines.append(f"- `{category}` — {label} ({kind_text} Actions).")
    lines.extend(
        [
            "",
            "An unavailable Backend remains discoverable. If an exact call fails, inspect its result "
            "and independently decide the next scientific step; the framework does not add defaults "
            "or redirect the call.",
        ]
    )
    return "\n".join(lines)


def toolbox_overview(
    *,
    discovery_mode: str | None = None,
    include_health: bool = True,
    snapshot: dict[str, Any] | None = None,
) -> str:
    """Return the prompt index corresponding to the selected public surface."""

    mode = resolve_tool_discovery_mode(discovery_mode)
    if mode == "full":
        return agent_toolbox_overview(
            include_health=include_health,
            snapshot=snapshot,
        )
    return progressive_toolbox_overview(snapshot=snapshot)


def markdown_catalog(*, include_health: bool = True) -> str:
    snapshot = catalog_snapshot(include_health=include_health)
    backend_by_id = {backend["id"]: backend for backend in snapshot["backends"]}
    lines = [
        "# ResearchChem Atomic Tool Catalog",
        "",
        f"Catalog hash: `{snapshot['catalog_hash']}`",
        "",
        "These predefined Actions are the validated common-operation layer. They are exposed to every task but are not mandatory; the MCP server also exposes native-software and programmable-analysis layers. Provider selection follows each Action's policy.",
        "",
        "| Action | Category | Primary output | Selection policy | Providers | Required inputs | Description |",
        "|---|---|---|---|---|---|---|",
    ]
    for action in snapshot["actions"]:
        required = ", ".join(action["required_inputs"])
        if not required:
            contracts = []
            for backend_id in action["backend_ids"]:
                fields = backend_by_id[backend_id]["required_input_fields"].get(
                    action["id"], []
                )
                if fields:
                    contracts.append(f"{backend_id}({','.join(fields)})")
            required = "backend-specific: " + "; ".join(contracts) if contracts else "none"
        lines.append(
            "| {id} | {category} | {primary_output} | {policy} | {backends} | {required} | {description} |".format(
                id=action["id"],
                category=action["category"],
                primary_output=action["primary_output"],
                policy=action["selection_policy"],
                backends=", ".join(action["backend_ids"]),
                required=required,
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

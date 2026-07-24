"""Neutral, task-independent progressive discovery over the frozen catalog."""

from __future__ import annotations

import re
from typing import Any, Literal, Mapping

from .catalog import (
    CATEGORY_LABELS,
    active_catalog_snapshot,
    action_specs,
    backend_specs,
)
from .models import ActionSpec, BackendSpec
from .parameter_specs import (
    RESOURCE_LIMIT_PARAMETER_SPECS,
    common_fixed_parameter_specs,
    inferred_parameter_metadata,
)


ActionKind = Literal["all", "scientific", "data"]


_COMPOSITE_CALCULATOR_ACTIONS = {
    "geometric": ("calculate_energy", "calculate_forces"),
    "sella": ("calculate_energy", "calculate_forces"),
}

_ACTION_INPUT_HANDOFF_NOTES = {
    "derive_vibrational_modes": (
        "inputs.hessian expects the primary Hessian ArtifactRef returned by "
        "calculate_hessian. inputs.structure separately expects the exact matching "
        "AtomicStructure used to calculate that Hessian; never reuse one artifact_id "
        "for both fields."
    ),
    "derive_thermochemistry": (
        "For backend_id=internal_thermochemistry, inputs.energy expects an EnergyResult "
        "ArtifactRef and inputs.frequencies expects the FrequencyResult ArtifactRef returned "
        "by derive_vibrational_modes. A calculate_hessian primary artifact is a Hessian, not "
        "a FrequencyResult; explicitly run the separate vibrational-mode Action first."
    ),
}


def _lexical_stem(value: str) -> str:
    """Small deterministic morphology normalizer, not a relevance ranker."""

    for suffix in (
        "izations",
        "isations",
        "ization",
        "isation",
        "ations",
        "ation",
        "ments",
        "ment",
        "ing",
        "ed",
        "es",
        "s",
    ):
        if value.endswith(suffix) and len(value) - len(suffix) >= 5:
            return value[: -len(suffix)]
    return value


def _matches_all_terms(terms: list[str], haystack: str) -> bool:
    if not terms:
        return True
    words = re.findall(r"[a-z0-9]+", haystack.casefold())
    word_stems = [_lexical_stem(word) for word in words]
    for term in terms:
        if term in haystack:
            continue
        stem = _lexical_stem(term)
        if not any(
            word.startswith(stem)
            or stem.startswith(word_stem)
            and len(word_stem) >= 5
            for word, word_stem in zip(words, word_stems)
        ):
            return False
    return True


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
    fixed_parameters = common_fixed_parameter_specs(
        runtime=backend.runtime,
        executables=backend.executables,
        python_modules=backend.python_modules,
        resource_constraints=backend.resource_constraints,
        validation_level=backend.validation_levels.get(action_id),
    )
    fixed_parameters.update(backend.fixed_parameter_specs.get(action_id, {}))
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
        "resource_constraints": dict(backend.resource_constraints),
        "agent_controllable_parameters": {
            field_path: dict(metadata)
            for field_path, metadata in backend.parameter_specs.get(action_id, {}).items()
        },
        "backend_fixed_parameters": {
            field_path: dict(metadata)
            for field_path, metadata in fixed_parameters.items()
        },
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


def _field_type(field_name: str, *, section: str) -> dict[str, Any]:
    """Return a compact machine-readable shape hint for progressive discovery.

    The public Action dispatcher intentionally keeps three extensible mappings instead
    of eagerly registering one large Pydantic model per Action.  These hints make the
    selected Action/Backend contract explicit without loading every schema into the
    initial model context or choosing any scientific value for the Agent.
    """

    structure_fields = {
        "structure",
        "initial_guess",
        "reactant",
        "product",
        "ground_state",
        "geometry",
        "reference",
    }
    artifact_file_fields = {
        "control_file",
        "dos_file",
        "lobster_output",
        "output_file",
        "profile_definition_file",
        "second_order_force_constants_file",
        "structure_file",
        "third_order_force_constants_file",
    }
    mapping_fields = {
        "calculator_action_settings",
        "calculator_method",
        "chemical_species_mapping",
        "constraints",
        "flexible_parameters",
        "k_points",
        "label_groups",
        "molecule_counts",
        "pair_parameters",
        "pseudopotentials",
    }
    array_fields = {
        "atom_indices",
        "band_path",
        "bin_edges",
        "critical_point_types",
        "fractions",
        "integrated_bond_list",
        "models",
        "output_files",
        "properties",
        "q_mesh",
        "q_path",
        "scf_thresholds",
        "selection",
        "state_pair",
        "temperatures_kelvin",
    }
    explicit_boolean_fields = {
        "internal_coordinates",
        "symmetry_correction",
    }
    explicit_integer_fields = {
        "steps_per_diagonalization",
    }
    explicit_numeric_fields = {
        "finite_difference_step",
        "initial_trust_radius",
        "minimum_bond_order",
        "minimum_model_quality",
        "step_length",
        "threshold",
        "trust_radius_angstrom",
    }
    boolean_prefixes = (
        "add_",
        "align",
        "allow_",
        "canonical_",
        "center_",
        "deduplicate_",
        "enforce_",
        "filter_",
        "fix_",
        "generate_",
        "idealize",
        "ignore_",
        "include_",
        "initialize_",
        "keep_",
        "largest_",
        "match_",
        "neutralize",
        "only_",
        "periodic",
        "prealign_",
        "project_",
        "reflect",
        "relax_",
        "reorder_",
        "replace_",
        "require_",
        "restart",
        "simplified",
        "soft_min",
        "strict_",
        "symmetry_correction",
        "three_point_",
        "unique",
        "update_",
        "use_",
        "write_",
    )
    integer_tokens = (
        "_count",
        "_cycles",
        "_interval",
        "_iterations",
        "_points",
        "_steps",
        "_stride",
        "_bands",
        "max_",
        "num_",
        "number_of_",
        "random_seed",
        "starting_atom_serial",
        "starting_residue_number",
    )
    numeric_tokens = (
        "_angstrom",
        "_bar",
        "_cm1",
        "_degrees",
        "_ev",
        "_fraction",
        "_fs",
        "_hartree",
        "_kelvin",
        "_kj_mol_nm",
        "_kcal_mol",
        "_micrometer",
        "_mol_l",
        "_pa",
        "_percent",
        "_seconds",
        "_threshold",
        "_tolerance",
        "_ry",
    )

    if field_name in structure_fields:
        return {
            "type": "AtomicStructure | ArtifactRef | workspace-relative structure path",
            "canonical_inline_example": {
                "atoms": [
                    {
                        "element": "H",
                        "position_angstrom": [0.0, 0.0, 0.0],
                    }
                ],
                "charge": 0,
                "multiplicity": 1,
                "pbc": [False, False, False],
            },
            "accepted_forms": [
                "full AtomicStructure mapping",
                "full immutable ArtifactRef",
                "compact {'artifact_id': 'art_...'}",
                "exact artifact-id string",
                "workspace-relative .xyz, .pdb, .sdf, .mol, or ASE-readable structure path",
            ],
        }
    if field_name in artifact_file_fields or field_name.endswith("_file"):
        return {
            "type": "ArtifactRef | workspace-relative path",
            "accepted_forms": [
                "full immutable ArtifactRef",
                "compact {'artifact_id': 'art_...'}",
                "exact artifact-id string",
                "workspace-relative input path when the selected adapter accepts files",
            ],
        }
    if field_name == "energy":
        return {"type": "EnergyResult | ArtifactRef"}
    if field_name == "frequencies":
        return {"type": "FrequencyResult | ArtifactRef"}
    if field_name == "hessian":
        return {
            "type": "Hessian | ArtifactRef",
            "accepted_forms": [
                "dense Hessian result mapping with matrix and unit",
                "primary immutable ArtifactRef with semantic_type='Hessian'",
                "compact {'artifact_id': 'art_...'} for that Hessian artifact",
                "exact Hessian artifact-id string",
            ],
        }
    if field_name == "vibrations":
        return {"type": "FrequencyResult | ArtifactRef"}
    if field_name in mapping_fields:
        return {"type": "object"}
    if field_name in array_fields or field_name.endswith("_files"):
        return {"type": "array"}
    if field_name in explicit_boolean_fields or field_name.startswith(boolean_prefixes):
        return {"type": "boolean"}
    if field_name in explicit_integer_fields or field_name in {
        "charge",
        "multiplicity",
        "spin",
        "order",
        "dimensions",
    }:
        return {"type": "integer"}
    if any(token in field_name for token in integer_tokens):
        return {"type": "integer"}
    if field_name in {"frequency_scale_factor", "zpe_scale_factor"}:
        return {"type": "number | documented symbolic value"}
    if field_name in explicit_numeric_fields:
        return {"type": "number"}
    if any(field_name.endswith(token) for token in numeric_tokens):
        return {"type": "number"}
    if section == "inputs" and field_name.endswith("constants"):
        return {"type": "array | ArtifactRef"}
    return {"type": "string | documented structured value"}


def _placeholder(field_name: str, *, section: str, choices: tuple[str, ...] = ()) -> Any:
    if choices:
        return f"<choose exactly one: {' | '.join(str(choice) for choice in choices)}>"
    if field_name == "hessian":
        return "<dense Hessian result mapping or primary Hessian artifact_id>"
    shape = _field_type(field_name, section=section)["type"]
    if shape == "boolean":
        return "<boolean>"
    if shape == "integer":
        return "<integer>"
    if shape == "number":
        return "<number>"
    if shape == "object":
        return {"<field>": "<value>"}
    if shape == "array":
        return ["<value>"]
    if "AtomicStructure" in shape:
        return "<AtomicStructure, artifact_id, or workspace-relative structure path>"
    if "ArtifactRef" in shape:
        return "<artifact_id or accepted workspace-relative path>"
    return f"<{field_name}>"


def _field_contracts(
    fields: tuple[str, ...] | list[str],
    *,
    section: str,
    required: bool,
    choices: Mapping[str, tuple[str, ...]] | None = None,
    reference: Mapping[str, str] | None = None,
    metadata: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    allowed = choices or {}
    descriptions = reference or {}
    details = metadata or {}
    contracts: list[dict[str, Any]] = []
    for field_name in fields:
        contract = {
            "name": field_name,
            "required": required,
            **_field_type(field_name, section=section),
            **inferred_parameter_metadata(
                section, field_name, required=required
            ),
            **(
                {"allowed_values": list(allowed[field_name])}
                if field_name in allowed
                else {}
            ),
            **(
                {"description": descriptions[field_name]}
                if field_name in descriptions
                else {}
            ),
            **dict(details.get(field_name, {})),
        }
        if required:
            # Required fields have no operational default because the dispatcher
            # rejects omission.  Some backend adapters keep defensive direct-call
            # fallbacks; those must not be presented as public Action defaults.
            contract.pop("default", None)
        contracts.append(contract)
    return contracts


def _action_request_contract(
    specification: ActionSpec,
    backend: BackendSpec,
) -> dict[str, Any]:
    backend_inputs = backend.required_input_fields.get(specification.id, ())
    required_inputs = tuple(dict.fromkeys((*specification.required_inputs, *backend_inputs)))
    required_methods = backend.required_method_fields.get(specification.id, ())
    required_settings = backend.required_setting_fields.get(specification.id, ())
    method_choices = backend.allowed_method_values.get(specification.id, {})
    setting_choices = backend.allowed_setting_values.get(specification.id, {})
    registered_parameters = backend.parameter_specs.get(specification.id, {})
    registered_by_section: dict[str, dict[str, Mapping[str, Any]]] = {
        "inputs": {},
        "method_spec": {},
        "action_settings": {},
        "resource_limits": {},
    }
    for field_path, metadata in registered_parameters.items():
        section, field_name = field_path.split(".", 1)
        if section in registered_by_section:
            registered_by_section[section][field_name] = metadata
    optional_inputs = tuple(
        field_name
        for field_name in dict.fromkeys(
            (*specification.optional_inputs, *registered_by_section["inputs"])
        )
        if field_name not in required_inputs
    )
    optional_methods = tuple(
        field_name
        for field_name in dict.fromkeys(
            (
                *method_choices,
                *registered_by_section["method_spec"],
            )
        )
        if field_name not in required_methods
        and field_name not in required_settings
        and field_name not in setting_choices
        and "conditional" not in field_name
    )
    optional_settings = tuple(
        field_name for field_name in dict.fromkeys(
            (*setting_choices, *registered_by_section["action_settings"])
        )
        if field_name not in required_settings
    )
    conditional_rules = [
        {"name": field_name, "rule": description}
        for field_name, description in backend.method_schema.items()
        if "conditional" in field_name or " requires " in f" {description.casefold()} "
    ]
    fixed_parameters = common_fixed_parameter_specs(
        runtime=backend.runtime,
        executables=backend.executables,
        python_modules=backend.python_modules,
        resource_constraints=backend.resource_constraints,
        validation_level=backend.validation_levels.get(specification.id),
    )
    fixed_parameters.update(backend.fixed_parameter_specs.get(specification.id, {}))

    template: dict[str, Any] = {"action_id": specification.id}
    if specification.selection_policy in {
        "agent_backend_required",
        "agent_components_required",
    }:
        template["backend_id"] = backend.id
    elif specification.selection_policy == "agent_source_required":
        template["source_id"] = backend.id
    component_roles = backend.required_component_roles.get(specification.id, ())
    if component_roles:
        template["component_backends"] = {
            role: f"<choose exactly one: {' | '.join(backend.component_backend_options[specification.id][role])}>"
            for role in component_roles
        }
    template["inputs"] = {
        field_name: _placeholder(field_name, section="inputs")
        for field_name in required_inputs
    }
    template["method_spec"] = {
        field_name: _placeholder(
            field_name,
            section="method_spec",
            choices=method_choices.get(field_name, ()),
        )
        for field_name in required_methods
    }
    template["action_settings"] = {
        field_name: _placeholder(
            field_name,
            section="action_settings",
            choices=setting_choices.get(field_name, ()),
        )
        for field_name in required_settings
    }
    nested_component_actions = _COMPOSITE_CALCULATOR_ACTIONS.get(backend.id, ())
    if (
        nested_component_actions
        and "calculator_action_settings" in template["action_settings"]
    ):
        template["action_settings"]["calculator_action_settings"] = {
            action_id: {} for action_id in nested_component_actions
        }
    template["resource_limits"] = {
        "walltime_seconds": 1800,
        "memory_mb": None,
        "cpu_cores": None,
        "gpu_count": None,
    }

    return {
        "template_kind": "fill_every_angle_bracket_before_execute_action",
        "execute_action_request_template": template,
        "sections": {
            "inputs": {
                "required": _field_contracts(
                    required_inputs,
                    section="inputs",
                    required=True,
                    metadata=registered_by_section["inputs"],
                ),
                "optional": _field_contracts(
                    optional_inputs,
                    section="inputs",
                    required=False,
                    metadata=registered_by_section["inputs"],
                ),
            },
            "method_spec": {
                "required": _field_contracts(
                    required_methods,
                    section="method_spec",
                    required=True,
                    choices=method_choices,
                    reference=backend.method_schema,
                    metadata=registered_by_section["method_spec"],
                ),
                "optional_documented": _field_contracts(
                    optional_methods,
                    section="method_spec",
                    required=False,
                    choices=method_choices,
                    reference=backend.method_schema,
                    metadata=registered_by_section["method_spec"],
                ),
                # Compatibility alias retained for clients written against the
                # original discovery schema name.
                "optional_with_enumerated_values": _field_contracts(
                    optional_methods,
                    section="method_spec",
                    required=False,
                    choices=method_choices,
                    reference=backend.method_schema,
                    metadata=registered_by_section["method_spec"],
                ),
            },
            "action_settings": {
                "required": _field_contracts(
                    required_settings,
                    section="action_settings",
                    required=True,
                    choices=setting_choices,
                    reference=backend.method_schema,
                    metadata=registered_by_section["action_settings"],
                ),
                "optional_documented": _field_contracts(
                    optional_settings,
                    section="action_settings",
                    required=False,
                    choices=setting_choices,
                    reference=backend.method_schema,
                    metadata=registered_by_section["action_settings"],
                ),
                "optional_with_enumerated_values": _field_contracts(
                    optional_settings,
                    section="action_settings",
                    required=False,
                    choices=setting_choices,
                    reference=backend.method_schema,
                    metadata=registered_by_section["action_settings"],
                ),
            },
            "resource_limits": {
                "optional_with_defaults": [
                    {"name": field_name, "required": False, **dict(metadata)}
                    for field_name, metadata in RESOURCE_LIMIT_PARAMETER_SPECS.items()
                ],
            },
        },
        "backend_fixed_parameters": [
            {"path": field_path, **dict(metadata)}
            for field_path, metadata in fixed_parameters.items()
        ],
        "conditional_requirements": conditional_rules,
        "component_request_contracts": (
            {
                "calculator": {
                    "required_nested_actions": list(nested_component_actions),
                    "calculator_method_location": "method_spec.calculator_method",
                    "calculator_settings_location": (
                        "action_settings.calculator_action_settings.<nested_action>"
                    ),
                    "inspection_rule": (
                        "After choosing component_backends.calculator, inspect that exact "
                        "Backend for every required_nested_action and fill its required method "
                        "and setting fields. Empty nested mappings are valid only when the "
                        "selected calculator declares no settings for that nested Action."
                    ),
                }
            }
            if nested_component_actions
            else {}
        ),
        "output_contract": {
            "primary_output": specification.primary_output,
            "result_envelope": "ActionResult",
            "artifact_handoff": (
                "Use each returned output_artifacts ArtifactRef, compact artifact_id object, or "
                "exact artifact-id string as the typed input to a later Action."
            ),
            "input_handoff_note": _ACTION_INPUT_HANDOFF_NOTES.get(specification.id),
        },
        "execution_checklist": [
            "Replace every angle-bracket placeholder; placeholders are not defaults.",
            "Preserve the exact selected action_id and backend_id/source_id.",
            "Supply every required field in the section where it is listed.",
            "Apply every conditional requirement triggered by an Agent-selected option.",
            "Match ArtifactRef.semantic_type to each input field; differently typed required inputs normally require different artifact ids.",
            "The displayed resource limits are active defaults; override any of them when the selected calculation needs different resources.",
        ],
    }


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


def list_action_domains(
    *,
    include_action_ids: bool = True,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = _snapshot(snapshot)
    actions = list(current.get("actions", []))
    domains = []
    for category, label in CATEGORY_LABELS.items():
        values = [action for action in actions if action.get("category") == category]
        item = {
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
        if include_action_ids:
            item["action_ids"] = sorted(str(action.get("id")) for action in values)
        domains.append(item)
    return {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "catalog_visibility_policy": "complete_task_independent",
        "task_specific_filtering": False,
        "count": len(domains),
        "includes_action_ids": include_action_ids,
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
            ]
        ).casefold()
        if not _matches_all_terms(terms, haystack):
            continue
        matches.append(specification)

    page = matches[offset : offset + limit]
    results = []
    for specification in page:
        providers = [
            {
                "backend_id": backend,
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
    selected_request_contract = (
        _action_request_contract(specification, backends[backend_id])
        if backend_id is not None
        else None
    )
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
        "selected_request_contract": selected_request_contract,
        "detail_note": (
            "Exact details for the requested provider are included."
            if backend_id is not None or len(selected) == 1
            else "Provider summaries are included. Call inspect_action again with backend_id for "
            "that provider's full parameter, health, runtime, and resource reference."
        ),
        "request_contract_note": (
            "A complete fill-in request contract is included for the explicitly selected provider."
            if selected_request_contract is not None
            else "Select one provider and call inspect_action again with backend_id to obtain the "
            "fill-in execute_action request contract."
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
            "resource_constraints": dict(backend.resource_constraints),
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
        if not _matches_all_terms(terms, haystack):
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

"""Neutral, task-independent progressive discovery over the frozen catalog."""

from __future__ import annotations

import difflib
import re
from typing import Any, Literal, Mapping

from .action_aliases import aliases_for_action
from .catalog import (
    CATEGORY_LABELS,
    active_catalog_snapshot,
    action_specs,
    backend_specs,
    catalog_snapshot,
)
from .models import ActionSpec, BackendSpec
from .parameter_specs import (
    RESOURCE_LIMIT_PARAMETER_SPECS,
    common_fixed_parameter_specs,
    inferred_parameter_metadata,
)
from .resource_budget import resource_budget_record
from .distributed_pool import distributed_enabled
from .search_index import BM25Index, normalize_scores, tokenize, weighted_text
from .semantic_embeddings import MODEL_ID, semantic_scores
from .timeout_policy import timeout_policy_record


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


def _provider_summary(
    backend: BackendSpec, action_id: str, snapshot: dict[str, Any]
) -> dict[str, Any]:
    return {
        "backend_id": backend.id,
        "display_name": backend.display_name,
        "health_status": _health_status(snapshot, backend.id),
        "required_input_fields": list(backend.required_input_fields.get(action_id, ())),
        "required_method_fields": list(backend.required_method_fields.get(action_id, ())),
        "required_setting_fields": list(backend.required_setting_fields.get(action_id, ())),
        "required_component_roles": list(
            backend.required_component_roles.get(action_id, ())
        ),
        "supported_system_types": list(
            backend.supported_system_types.get(action_id, ())
        ),
        "validation_level": backend.validation_levels.get(action_id),
    }


def _action_summary(specification: ActionSpec) -> dict[str, Any]:
    return {
        "id": specification.id,
        "category": specification.category,
        "description": specification.description,
        "primary_output": specification.primary_output,
        "backend_ids": list(specification.backend_ids),
        "required_inputs": list(specification.required_inputs),
        "optional_inputs": list(specification.optional_inputs),
        "selection_policy": specification.selection_policy,
        "data_action": specification.data_action,
        "batch_safe": specification.batch_safe,
    }


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
        "initial_structure",
        "molecule",
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
        "cutoffs_au",
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
        "stability_analysis",
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
        "_bohr",
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
    if section == "inputs" and field_name == "ensemble":
        return {
            "type": "ConformerEnsemble | ArtifactRef | workspace-relative conformer file",
            "accepted_forms": [
                "typed ConformerEnsemble ArtifactRef, compact artifact_id object, or exact artifact-id string",
                "structured mapping containing a non-empty ensemble or conformers list",
                "workspace-relative .sdf, .mol, or multi-frame .xyz file",
            ],
            "rejected_forms": [
                "path to a JSON summary; pass the structured JSON value or typed artifact instead",
                "single AtomicStructure when the Action requires multiple conformers",
            ],
            "cardinality": "multiple conformers with identical atom count and atom ordering",
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
    if field_name == "electron_density":
        return {
            "type": "ElectronDensityResult ArtifactRef",
            "accepted_forms": [
                "primary immutable ArtifactRef with semantic_type='ElectronDensityResult' returned by calculate_correlated_electron_density",
                "compact {'artifact_id': 'art_...'} for that primary ElectronDensityResult artifact",
                "exact ElectronDensityResult artifact-id string",
            ],
            "rejected_forms": [
                "job.gbw or another path from result.files",
                "ElectronDensityWavefunction, BackendFile, or diagnostic artifact ids",
            ],
            "handoff_example": {
                "electron_density": "<copy output_artifacts item whose semantic_type is ElectronDensityResult, or its artifact_id>"
            },
        }
    if field_name == "density_file":
        return {
            "type": "ElectronDensityWavefunction | ElectronDensityGrid ArtifactRef | workspace-relative density file",
            "accepted_forms": [
                "output_artifacts item from export_electron_density_grid whose semantic_type is ElectronDensityWavefunction or ElectronDensityGrid",
                "compact {'artifact_id': 'art_...'} or exact artifact-id string for that typed artifact",
                "workspace-relative WFN, WFX, FCHK, MWFN, Molden, or cube path",
            ],
        }
    if field_name == "cutoffs_au":
        return {
            "type": "array",
            "items": {"type": "number"},
            "minimum_items": 1,
            "maximum_items": 100,
            "value_range": {"exclusive_minimum": 0.0, "exclusive_maximum": 0.1},
            "example": [0.001, 0.0015, 0.002],
            "compatibility_input": (
                "A comma-separated numeric string is normalized for compatibility, but new "
                "requests should always send a JSON array of numbers."
            ),
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
    if field_name == "electron_density":
        return "<primary ElectronDensityResult artifact_id from calculate_correlated_electron_density>"
    if field_name == "density_file":
        return "<ElectronDensityWavefunction or ElectronDensityGrid artifact_id from export_electron_density_grid>"
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
    policy_record = timeout_policy_record(specification.execution_class)
    fixed_parameters["execution_policy.timeout_seconds"] = {
        "description": (
            f"Evaluator-controlled {specification.execution_class} Action timeout: "
            f"{policy_record['timeout_seconds']} seconds."
        ),
        "reason": (
            "Timeout is a benchmark resource budget shared by all Agents and is not "
            "an Agent-selectable scientific parameter."
        ),
    }
    budget_record = resource_budget_record()
    for field_name in ("cpu_cores", "memory_mb", "gpu_count"):
        fixed_parameters[f"evaluation_resource_budget.{field_name}"] = {
            "description": (
                f"Distributed single-job maximum for {field_name}: "
                f"{budget_record[field_name]}."
                if distributed_enabled()
                else f"Per-task evaluator budget for {field_name}: "
                f"{budget_record[field_name]}."
            ),
            "reason": (
                "The benchmark operator fixes each worker's exposed capacity. The Agent may "
                "request resources within the per-job maximum while independent jobs share "
                "the aggregate distributed pool."
                if distributed_enabled()
                else "The benchmark operator fixes the resource envelope. The Agent may "
                "request resources within it but cannot enlarge it."
            ),
        }

    resource_parameter_specs = {
        field_name: dict(metadata)
        for field_name, metadata in RESOURCE_LIMIT_PARAMETER_SPECS.items()
    }
    for field_name, metadata in registered_by_section["resource_limits"].items():
        resource_parameter_specs.setdefault(field_name, {}).update(dict(metadata))
    for field_name in ("cpu_cores", "memory_mb", "gpu_count"):
        current_maximum = resource_parameter_specs[field_name].get("maximum")
        budget_maximum = int(budget_record[field_name])
        resource_parameter_specs[field_name]["maximum"] = (
            min(int(current_maximum), budget_maximum)
            if current_maximum is not None
            else budget_maximum
        )
        resource_parameter_specs[field_name]["evaluation_budget_reason"] = (
            "A single request cannot exceed the maximum capacity of one compute worker; "
            "concurrent requests use the distributed pool's aggregate available resources."
            if distributed_enabled()
            else "Single requests and the sum of concurrently active managed jobs cannot exceed "
            "the evaluator-controlled per-task resource budget."
        )
    resource_maximum_fields = {"cpu_cores": "maximum_cpu_cores"}
    for field_name, constraint_name in resource_maximum_fields.items():
        maximum = backend.resource_constraints.get(constraint_name)
        if maximum is None:
            continue
        current_maximum = resource_parameter_specs[field_name].get("maximum")
        resource_parameter_specs[field_name]["maximum"] = (
            min(int(current_maximum), int(maximum))
            if current_maximum is not None
            else int(maximum)
        )
        reason = backend.resource_constraints.get("reason")
        if reason:
            resource_parameter_specs[field_name]["backend_limit_reason"] = str(reason)

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
        field_name: metadata.get("default")
        for field_name, metadata in resource_parameter_specs.items()
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
                    for field_name, metadata in resource_parameter_specs.items()
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
        "execution_timeout_policy": policy_record,
        "evaluation_resource_budget": budget_record,
        "execution_checklist": [
            "Replace every angle-bracket placeholder; placeholders are not defaults.",
            "Preserve the exact selected action_id and backend_id/source_id.",
            "Supply every required field in the section where it is listed.",
            "Apply every conditional requirement triggered by an Agent-selected option.",
            "Match ArtifactRef.semantic_type to each input field; differently typed required inputs normally require different artifact ids.",
            "The displayed resource limits are active defaults; override any of them when the selected calculation needs different resources.",
        ],
    }


def _compact_action_request_contract(
    specification: ActionSpec,
    backend: BackendSpec,
) -> dict[str, Any]:
    """Return the bounded contract needed to execute one selected provider."""

    complete = _action_request_contract(specification, backend)
    sections = complete["sections"]

    def required(section: str) -> list[dict[str, Any]]:
        return [
            {
                key: value
                for key, value in item.items()
                if key
                in {
                    "name",
                    "required",
                    "type",
                    "allowed_values",
                    "accepted_forms",
                    "rejected_forms",
                    "cardinality",
                    "canonical_inline_example",
                    "description",
                }
            }
            for item in sections[section].get("required", [])
        ]

    optional_inputs = sections["inputs"].get("optional", [])
    important_optional_inputs = [
        {
            key: value
            for key, value in item.items()
            if key
            in {
                "name",
                "type",
                "accepted_forms",
                "rejected_forms",
                "cardinality",
                "description",
            }
        }
        for item in optional_inputs
        if item.get("name") in {"initial_structure"}
    ]
    enumerated_options: list[dict[str, Any]] = []
    for section_name in ("method_spec", "action_settings"):
        section_value = sections[section_name]
        candidates = [
            *section_value.get("required", []),
            *section_value.get("optional_documented", []),
        ]
        for item in candidates:
            if item.get("allowed_values"):
                enumerated_options.append(
                    {
                        "path": f"{section_name}.{item['name']}",
                        "required": bool(item.get("required")),
                        "allowed_values": item["allowed_values"],
                    }
                )

    usage_notes: list[str] = []
    if specification.id == "cluster_conformers" and backend.id == "rdkit":
        usage_notes.append(
            "Pass a typed conformer ensemble, a structured ensemble mapping, or a readable "
            "SDF/MOL/multi-frame XYZ file. A path to a JSON summary is not a conformer file."
        )
    if specification.id == "generate_conformer_ensemble" and backend.id == "crest":
        usage_notes.extend(
            [
                "CREST requires one complete starting geometry with coordinates; do not pass an ensemble or trajectory artifact.",
                "When inputs.initial_structure is supplied it overrides inputs.molecule. Select exactly one frame before submission.",
            ]
        )
    handoff_note = _ACTION_INPUT_HANDOFF_NOTES.get(specification.id)
    if handoff_note:
        usage_notes.append(handoff_note)

    return {
        "template_kind": "minimal_executable_request",
        "execute_action_request_template": complete[
            "execute_action_request_template"
        ],
        "required_contract": {
            "inputs": required("inputs"),
            "method_spec": required("method_spec"),
            "action_settings": required("action_settings"),
            "component_backends": list(
                backend.required_component_roles.get(specification.id, ())
            ),
        },
        "optional_field_names": {
            "inputs": [item["name"] for item in optional_inputs],
            "method_spec": [
                item["name"]
                for item in sections["method_spec"].get("optional_documented", [])
            ],
            "action_settings": [
                item["name"]
                for item in sections["action_settings"].get(
                    "optional_documented", []
                )
            ],
        },
        "important_optional_inputs": important_optional_inputs,
        "enumerated_options": enumerated_options,
        "conditional_requirements": complete["conditional_requirements"],
        "component_request_contracts": complete["component_request_contracts"],
        "output_contract": complete["output_contract"],
        "usage_notes": usage_notes,
        "retry_policy": (
            "On invalid_request, correct the reported fields and retry this same Action/Backend "
            "once. Do not switch providers before applying the diagnostic."
        ),
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


def browse_action_category(
    *,
    category: str,
    action_kind: ActionKind = "all",
    available_only: bool = False,
    detail_level: Literal["summary", "full"] = "full",
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the complete compact choice set inside one exact Action category."""

    result = search_actions(
        category=category,
        action_kind=action_kind,
        available_only=available_only,
        detail_level=detail_level,
        limit=100,
        snapshot=snapshot,
    )
    result["browse_mode"] = "complete_category"
    result["category_description"] = CATEGORY_LABELS[category]
    return result


def _action_search_fields(
    specifications: list[ActionSpec], backends: Mapping[str, BackendSpec]
) -> dict[str, dict[str, str]]:
    fields: dict[str, dict[str, str]] = {}
    for specification in specifications:
        providers = [backends[item] for item in specification.backend_ids]
        aliases = " ".join(
            dict.fromkeys((*aliases_for_action(specification.id), *specification.aliases))
        )
        fields[specification.id] = {
            "action_id": specification.id.replace("_", " "),
            "aliases": aliases,
            "primary_output": specification.primary_output,
            "category": CATEGORY_LABELS.get(specification.category, ""),
            "description": specification.description,
            "keywords": " ".join(specification.keywords),
            "capability_tags": " ".join(specification.capability_tags),
            "scientific_entities": " ".join(specification.scientific_entities),
            "task_verbs": " ".join(specification.task_verbs),
            "input_semantic_types": " ".join(
                specification.input_semantic_types or specification.required_inputs
            ),
            "output_semantic_types": " ".join(
                specification.output_semantic_types or (specification.primary_output,)
            ),
            "input_description": specification.input_description,
            "optional_inputs": " ".join(specification.optional_inputs),
            "backend_ids": " ".join(provider.id for provider in providers),
            "backend_names": " ".join(provider.display_name for provider in providers),
        }
    return fields


def _action_search_documents(fields: Mapping[str, Mapping[str, str]]) -> dict[str, str]:
    documents: dict[str, str] = {}
    for action_id, item in fields.items():
        documents[action_id] = weighted_text(
            (
                (item["action_id"], 5),
                (item["aliases"], 4),
                (item["primary_output"], 3),
                (item["category"], 2),
                (item["description"], 2),
                (item["keywords"], 2),
                (item["capability_tags"], 2),
                (item["scientific_entities"], 1),
                (item["task_verbs"], 1),
                (item["input_semantic_types"], 1),
                (item["output_semantic_types"], 1),
                (item["input_description"], 1),
                (item["optional_inputs"], 1),
                (item["backend_ids"], 1),
                (item["backend_names"], 1),
            )
        )
    return documents


def search_actions(
    *,
    query: str | None = None,
    category: str | None = None,
    backend_id: str | None = None,
    action_kind: ActionKind = "all",
    retrieval_mode: Literal["lexical", "hybrid"] = "hybrid",
    detail_level: Literal["summary", "full"] = "full",
    available_only: bool = False,
    limit: int = 20,
    offset: int = 0,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = (
        _snapshot(snapshot)
        if snapshot is not None or available_only
        else catalog_snapshot(include_health=False)
    )
    actions = action_specs()
    backends = backend_specs()
    if category is not None and category not in CATEGORY_LABELS:
        raise ValueError(
            f"Unknown category {category!r}; choose one returned by list_action_domains"
        )
    if backend_id is not None and backend_id not in backends:
        raise ValueError(f"Unknown backend_id {backend_id!r}")
    eligible: list[ActionSpec] = []
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
        eligible.append(specification)

    search_fields = _action_search_fields(eligible, backends)
    documents = _action_search_documents(search_fields)
    normalized_query = (query or "").casefold().strip()
    semantic_status = "not_requested"
    per_action_scores: dict[str, dict[str, float]] = {}
    per_action_explanations: dict[str, dict[str, Any]] = {}
    predicted_categories: list[dict[str, Any]] = []
    if normalized_query:
        document_vocabulary = sorted(
            {token for document in documents.values() for token in tokenize(document)}
        )
        query_tokens = tokenize(normalized_query)
        query_expansions: dict[str, str] = {}
        for token in query_tokens:
            if token in document_vocabulary or len(token) < 5:
                continue
            matches = difflib.get_close_matches(
                token, document_vocabulary, n=1, cutoff=0.86
            )
            if matches:
                query_expansions[token] = matches[0]
        lexical_query = " ".join(
            [normalized_query, *query_expansions.values()]
        ).strip()
        lexical_ranked = BM25Index(documents).search(lexical_query)
        lexical_raw = {item.document_id: item.score for item in lexical_ranked}
        lexical_terms = {
            item.document_id: list(item.matched_terms) for item in lexical_ranked
        }
        lexical = normalize_scores(lexical_raw)
        semantic_raw: dict[str, float] = {}
        if retrieval_mode == "hybrid":
            semantic_raw, semantic_status = semantic_scores(normalized_query, documents)
        semantic_positive = {
            key: max(0.0, value) for key, value in semantic_raw.items() if value >= 0.20
        }
        semantic = normalize_scores(semantic_positive)
        candidate_ids = set(lexical) | set(semantic)
        for action_id in candidate_ids:
            action_text = action_id.replace("_", " ")
            aliases = aliases_for_action(action_id)
            exact_bonus = 0.0
            if normalized_query in {action_id.casefold(), action_text.casefold()}:
                exact_bonus = 0.35
            elif any(normalized_query == alias.casefold() for alias in aliases):
                exact_bonus = 0.25
            elif normalized_query in documents[action_id].casefold():
                exact_bonus = 0.08
            lexical_score = lexical.get(action_id, 0.0)
            semantic_score = semantic.get(action_id, 0.0)
            combined = lexical_score + 0.12 * semantic_score + exact_bonus
            per_action_scores[action_id] = {
                "combined": combined,
                "bm25": lexical_score,
                "semantic": semantic_score,
                "exact_bonus": exact_bonus,
            }
            query_terms = set(tokenize(normalized_query))
            matched_fields = [
                field_name
                for field_name, field_text in search_fields[action_id].items()
                if query_terms & set(tokenize(field_text))
            ]
            exact_matches = []
            if normalized_query in {action_id.casefold(), action_text.casefold()}:
                exact_matches.append("action_id")
            if any(normalized_query == alias.casefold() for alias in aliases):
                exact_matches.append("alias")
            if exact_matches:
                ranking_reason = f"exact {' and '.join(exact_matches)} match"
            elif lexical_score and semantic_score:
                ranking_reason = "BM25 match with MiniLM semantic support"
            elif lexical_score:
                ranking_reason = "BM25 field match"
            else:
                ranking_reason = "MiniLM semantic recall"
            per_action_explanations[action_id] = {
                "matched_fields": matched_fields,
                "exact_matches": exact_matches,
                "expanded_terms": sorted(
                    set(lexical_terms.get(action_id, []))
                    | set(query_expansions.values())
                ),
                "ranking_reason": ranking_reason,
            }
        matches = sorted(
            (actions[action_id] for action_id in candidate_ids),
            key=lambda item: (-per_action_scores[item.id]["combined"], item.id),
        )
        ordering = "bm25_with_optional_minilm_semantic_recall"
        category_scores: dict[str, float] = {}
        for action_id, scores in per_action_scores.items():
            category_name = actions[action_id].category
            category_scores[category_name] = max(
                category_scores.get(category_name, 0.0), scores["combined"]
            )
        predicted_categories = [
            {
                "category": category_name,
                "label": CATEGORY_LABELS[category_name],
                "score": score,
            }
            for category_name, score in sorted(
                category_scores.items(), key=lambda item: (-item[1], item[0])
            )[:3]
        ]
    else:
        matches = eligible
        ordering = "stable_action_id_order"

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
        summary = {
                "action_id": specification.id,
                "category": specification.category,
                "description": specification.description,
                "primary_output": specification.primary_output,
                "data_action": specification.data_action,
                "batch_safe": specification.batch_safe,
                "selection_policy": specification.selection_policy,
                "provider_ids": [item["backend_id"] for item in providers],
                "relevance": per_action_scores.get(specification.id),
                **per_action_explanations.get(
                    specification.id,
                    {
                        "matched_fields": [],
                        "exact_matches": [],
                        "expanded_terms": [],
                        "ranking_reason": "stable catalog order",
                    },
                ),
            }
        if detail_level == "full":
            summary.update(
                {
                    "aliases": list(
                        dict.fromkeys(
                            (*aliases_for_action(specification.id), *specification.aliases)
                        )
                    ),
                    "keywords": list(specification.keywords),
                    "capability_tags": list(specification.capability_tags),
                    "scientific_entities": list(specification.scientific_entities),
                    "task_verbs": list(specification.task_verbs),
                    "input_semantic_types": list(
                        specification.input_semantic_types
                        or specification.required_inputs
                    ),
                    "output_semantic_types": list(
                        specification.output_semantic_types
                        or (specification.primary_output,)
                    ),
                    "execution_timeout_policy": timeout_policy_record(
                        specification.execution_class
                    ),
                    "evaluation_resource_budget": resource_budget_record(),
                    "providers": providers,
                }
            )
        results.append(summary)
    category_filter_advisory = None
    if normalized_query and category is not None:
        unrestricted = search_actions(
            query=query,
            category=None,
            backend_id=backend_id,
            action_kind=action_kind,
            retrieval_mode=retrieval_mode,
            detail_level="summary",
            available_only=available_only,
            limit=3,
            offset=0,
            snapshot=current,
        )
        unrestricted_actions = unrestricted.get("actions", [])
        unrestricted_top = unrestricted_actions[0] if unrestricted_actions else None
        filtered_top = results[0] if results else None
        if (
            isinstance(unrestricted_top, dict)
            and unrestricted_top.get("category") != category
            and unrestricted_top.get("exact_matches")
            and not (isinstance(filtered_top, dict) and filtered_top.get("exact_matches"))
        ):
            category_filter_advisory = {
                "code": "exact_match_outside_requested_category",
                "requested_category": category,
                "suggested_category": unrestricted_top.get("category"),
                "suggested_action_id": unrestricted_top.get("action_id"),
                "message": (
                    "The query has a stronger exact action or alias match outside the "
                    "requested category. Inspect the suggested action or retry without "
                    "a category filter."
                ),
            }
        predicted_categories = unrestricted.get(
            "predicted_categories", predicted_categories
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
        "ordering": ordering,
        "detail_level": detail_level,
        "predicted_categories": predicted_categories,
        "category_filter_advisory": category_filter_advisory,
        "retrieval": {
            "mode": retrieval_mode,
            "lexical_ranker": "bm25",
            "semantic_model": MODEL_ID if retrieval_mode == "hybrid" else None,
            "semantic_status": semantic_status,
            "semantic_threshold": 0.20 if retrieval_mode == "hybrid" else None,
            "query_expansions": query_expansions if normalized_query else {},
            "language": "English",
        },
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
    detail_level: Literal["summary", "contract", "full"] = "full",
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
    if detail_level == "full":
        provider_contracts = [
            _provider_contract(
                backends[item],
                action_id,
                current,
                detailed=backend_id is not None or len(selected) == 1,
            )
            for item in selected
        ]
    elif backend_id is not None and detail_level == "contract":
        provider_contracts = [
            _provider_summary(backends[backend_id], action_id, current)
        ]
    else:
        provider_contracts = [
            _provider_summary(backends[item], action_id, current) for item in selected
        ]
    selected_request_contract = None
    if backend_id is not None and detail_level == "contract":
        selected_request_contract = _compact_action_request_contract(
            specification, backends[backend_id]
        )
    elif backend_id is not None and detail_level == "full":
        selected_request_contract = _action_request_contract(
            specification, backends[backend_id]
        )
    result = {
        "status": "success",
        "catalog_hash": current.get("catalog_hash"),
        "detail_level": detail_level,
        "action": (
            specification.as_dict()
            if detail_level == "full"
            else _action_summary(specification)
        ),
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
            "The selected provider's compact execution requirements are included."
            if backend_id is not None and detail_level == "contract"
            else "Exact details for the requested provider are included."
            if backend_id is not None or len(selected) == 1
            else "Provider summaries are included. Call inspect_action again with backend_id for "
            "that provider's full parameter, health, runtime, and resource reference."
        ),
        "request_contract_note": (
            "A minimal executable request contract is included for the explicitly selected provider."
            if selected_request_contract is not None and detail_level == "contract"
            else "A complete audit request contract is included for the explicitly selected provider."
            if selected_request_contract is not None
            else "Select one provider and call inspect_action again with backend_id to obtain the "
            "fill-in execute_action request contract."
        ),
        "automatic_fallback": False,
    }
    if specification.batch_safe:
        parallel_execution: dict[str, Any] = {
            "eligible": True,
            "recommended_tool": "submit_action_batch",
            "use_when": (
                "Two or more independent inputs use this same Action and Backend."
            ),
            "warning": (
                "Repeated execute_action calls are synchronous and therefore serial. "
                "submit_action_batch runs independent children concurrently within the "
                "active CPU, memory, and GPU budget."
            ),
            "maximum_items": 32,
            "concurrency": "resource_aware_auto",
        }
        if backend_id is not None and selected_request_contract is not None:
            execute_template = selected_request_contract[
                "execute_action_request_template"
            ]
            parallel_execution["request_template"] = {
                "action_id": specification.id,
                "backend_id": backend_id,
                "component_backends": execute_template.get(
                    "component_backends", {}
                ),
                "method_spec": execute_template.get("method_spec", {}),
                "action_settings": execute_template.get("action_settings", {}),
                "items": [
                    {
                        "item_id": "<unique item id>",
                        "inputs": execute_template.get("inputs", {}),
                        "resource_limits": execute_template.get(
                            "resource_limits", {}
                        ),
                    }
                ],
            }
        result["parallel_execution"] = parallel_execution
    if detail_level in {"contract", "full"}:
        result["execution_timeout_policy"] = timeout_policy_record(
            specification.execution_class
        )
        result["evaluation_resource_budget"] = resource_budget_record()
    return result


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

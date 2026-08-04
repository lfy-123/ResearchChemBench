"""Focused Action/backend profile for ARCHE Case1-style mechanism tasks."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from .models import ActionSpec, BackendSpec


MINI_ACTION_IDS = frozenset(
    {
        "normalize_qcschema_molecule",
        "validate_qcschema_record",
        "parse_quantum_chemistry_output",
        "standardize_structure",
        "generate_3d_structure",
        "generate_conformer_ensemble",
        "cluster_conformers",
        "align_molecular_structures",
        "rank_conformers_from_results",
        "enumerate_coordination_isomers",
        "assign_protonation_states",
        "assign_partial_charges",
        "search_local_substructures",
        "enumerate_tautomers",
        "enumerate_stereoisomers",
        "calculate_energy",
        "calculate_forces",
        "calculate_hessian",
        "optimize_geometry",
        "calculate_dipole_moment",
        "calculate_atomic_charges",
        "calculate_electron_isodensity_surface",
        "calculate_bond_orders",
        "derive_vibrational_modes",
        "derive_ir_spectrum",
        "derive_thermochemistry",
        "scan_thermochemistry_temperature",
        "analyze_thermochemical_ensemble",
        "validate_thermochemistry_inputs",
        "locate_transition_state",
        "search_reaction_path",
        "scan_reaction_coordinates",
        "validate_reaction_path",
        "analyze_reaction_coordinate",
        "trace_intrinsic_reaction_coordinate",
        "analyze_thermochemical_selectivity",
        "analyze_reaction_free_energy_profile",
    }
)

MINI_BACKEND_IDS = frozenset(
    {
        "qcelemental",
        "cclib",
        "rdkit",
        "openbabel",
        "rdkit_etkdg",
        "crest",
        "internal_statistics",
        "internal_reaction_analysis",
        "rdkit_gasteiger",
        "xtb",
        "multiwfn",
        "gaussian",
        "internal_vibrations",
        "internal_spectroscopy",
        "internal_thermochemistry",
        "goodvibes",
        "sella",
        "pysisyphus",
    }
)

MINI_NATIVE_SOFTWARE_IDS = frozenset(
    {
        "gaussian",
        "crest",
        "xtb",
        "openbabel",
        "pysisyphus",
        "goodvibes",
        "multiwfn",
    }
)

MINI_RUNTIME_IDS = frozenset(
    {
        "core",
        "quantum",
        "reaction",
        "gaussian",
        "goodvibes",
        "multiwfn",
        "workflows",
        "sella",
    }
)


def _for_actions(mapping: Mapping[str, Any], action_ids: set[str]) -> dict[str, Any]:
    return {key: value for key, value in mapping.items() if key in action_ids}


def _component_options(
    mapping: Mapping[str, Mapping[str, tuple[str, ...]]],
    action_ids: set[str],
    backend_ids: set[str],
) -> dict[str, dict[str, tuple[str, ...]]]:
    result: dict[str, dict[str, tuple[str, ...]]] = {}
    for action_id, roles in mapping.items():
        if action_id not in action_ids:
            continue
        filtered = {
            role: tuple(option for option in options if option in backend_ids)
            for role, options in roles.items()
        }
        result[action_id] = {role: options for role, options in filtered.items() if options}
    return result


def _allowed_methods(
    mapping: Mapping[str, Mapping[str, tuple[str, ...]]],
    action_ids: set[str],
    backend_ids: set[str],
) -> dict[str, dict[str, tuple[str, ...]]]:
    result: dict[str, dict[str, tuple[str, ...]]] = {}
    for action_id, fields in mapping.items():
        if action_id not in action_ids:
            continue
        values = dict(fields)
        if "calculator_backend" in values:
            values["calculator_backend"] = tuple(
                item for item in values["calculator_backend"] if item in backend_ids
            )
        result[action_id] = values
    return result


def build_mini_specs(
    full_actions: tuple[ActionSpec, ...],
    full_backends: tuple[BackendSpec, ...],
) -> tuple[tuple[ActionSpec, ...], tuple[BackendSpec, ...]]:
    """Return an internally consistent subset of the comprehensive toolbox."""

    backend_ids = {item.id for item in full_backends if item.id in MINI_BACKEND_IDS}
    actions = tuple(
        replace(
            item,
            backend_ids=tuple(value for value in item.backend_ids if value in backend_ids),
        )
        for item in full_actions
        if item.id in MINI_ACTION_IDS
        and any(value in backend_ids for value in item.backend_ids)
    )
    action_ids = {item.id for item in actions}

    backends: list[BackendSpec] = []
    for item in full_backends:
        if item.id not in backend_ids:
            continue
        capabilities = tuple(value for value in item.capabilities if value in action_ids)
        if not capabilities:
            continue
        capability_ids = set(capabilities)
        backends.append(
            replace(
                item,
                capabilities=capabilities,
                required_input_fields=_for_actions(item.required_input_fields, capability_ids),
                required_method_fields=_for_actions(item.required_method_fields, capability_ids),
                required_setting_fields=_for_actions(item.required_setting_fields, capability_ids),
                allowed_method_values=_allowed_methods(
                    item.allowed_method_values, capability_ids, backend_ids
                ),
                allowed_setting_values=_for_actions(
                    item.allowed_setting_values, capability_ids
                ),
                required_component_roles=_for_actions(
                    item.required_component_roles, capability_ids
                ),
                component_backend_options=_component_options(
                    item.component_backend_options, capability_ids, backend_ids
                ),
                supported_system_types=_for_actions(
                    item.supported_system_types, capability_ids
                ),
                validation_levels=_for_actions(item.validation_levels, capability_ids),
                parameter_specs=_for_actions(item.parameter_specs, capability_ids),
                fixed_parameter_specs=_for_actions(
                    item.fixed_parameter_specs, capability_ids
                ),
            )
        )

    final_backend_ids = {item.id for item in backends}
    actions = tuple(
        replace(
            item,
            backend_ids=tuple(value for value in item.backend_ids if value in final_backend_ids),
        )
        for item in actions
    )
    return actions, tuple(backends)


__all__ = [
    "MINI_ACTION_IDS",
    "MINI_BACKEND_IDS",
    "MINI_NATIVE_SOFTWARE_IDS",
    "MINI_RUNTIME_IDS",
    "build_mini_specs",
]

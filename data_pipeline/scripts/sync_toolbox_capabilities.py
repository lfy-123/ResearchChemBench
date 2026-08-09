#!/usr/bin/env python3
"""Synchronize data-pipeline screening assets with the toolbox catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = PROJECT_ROOT / "data_pipeline"
ASSET_ROOT = PIPELINE_ROOT / "assets"
TOOLBOX_ROOT = PROJECT_ROOT / "chemistry_toolbox"

sys.path.insert(0, str(PROJECT_ROOT))

from chemistry_toolbox.src.actions import ACTION_SPECS  # noqa: E402
from chemistry_toolbox.src.backend_specs import BACKEND_SPECS  # noqa: E402
from chemistry_toolbox.src.catalog import catalog_hash, validate_catalog  # noqa: E402

EXPANDED_SOFTWARE = {
    "acpype",
    "airss",
    "bagel",
    "gmx_mmpbsa",
    "gplearn",
    "pmx",
    "pyfrag",
    "sisso",
    "tdep",
    "vaspkit",
}

# Software removed from the toolbox must not be exported into any screening
# capability asset, including aliases and explicit unavailable inventories.
EXCLUDED_SOFTWARE = {
    "adf",
    "ams",
    "calypso",
    "castep",
    "cccbdb",
    "cfour",
    "cosmotherm",
    "crystal",
    "easyspin",
    "fhi_aims",
    "matlab",
    "molpro",
    "multiwell",
    "nbo",
    "openeye",
    "progdyn",
    "qchem",
    "schrodinger",
    "terachem",
    "turbomole",
    "uspex",
    "wien2k",
}

EXPLICIT_ALIASES = {
    "acpype": {"ACPYPE"},
    "airss": {"AIRSS"},
    "bagel": {"BAGEL"},
    "gmx_mmpbsa": {"gmx_MMPBSA", "gmx-MMPBSA", "GMXMMPBSA"},
    "gplearn": {"gplearn"},
    "pmx": {"pmx"},
    "pyfrag": {"PyFrag", "PyFrag 2019"},
    "sisso": {"SISSO"},
    "tdep": {"TDEP"},
    "vaspkit": {"VASPKIT"},
    "amber_pmemd": {"AMBER", "AmberTools", "PMEMD", "pmemd.cuda"},
    "deepmd": {"DeePMD", "DeePMD-kit"},
    "hoomd": {"HOOMD", "HOOMD-blue"},
    "nist_webbook": {"NIST Chemistry WebBook", "NIST WebBook"},
    "rmg": {"RMG", "RMG-Py"},
}

PYTHON_PACKAGE_ALIASES = {
    "ase": {"ASE", "Atomic Simulation Environment"},
    "e3nn": {"e3nn"},
    "jax": {"JAX"},
    "matplotlib": {"Matplotlib"},
    "numpy": {"NumPy"},
    "pandas": {"pandas"},
    "scipy": {"SciPy"},
    "sklearn": {"scikit-learn", "sklearn"},
    "torch": {"PyTorch", "torch"},
}

GENERIC_NATIVE_EXECUTABLES = {"mpirun"}

REQUESTED_NAME_OVERRIDES = {
    "amber": "amber_pmemd",
    "deepmd_kit": "deepmd",
    "hoomd_blue": "hoomd",
    "nist_chemistry_webbook_interface": "nist_webbook",
    "rmg_py": "rmg",
}

FAMILY_ACTIONS = {
    "electronic_structure": {
        "analyze_electron_density_topology",
        "calculate_atomic_basin_properties",
        "calculate_atomic_charges",
        "calculate_bond_orders",
        "calculate_correlated_electron_density",
        "calculate_dipole_moment",
        "calculate_electron_isodensity_surface",
        "calculate_energy",
        "calculate_excited_states",
        "calculate_forces",
        "calculate_hessian",
        "calculate_multireference_nuclear_gradient",
        "calculate_multireference_state_energies",
        "calculate_nonadiabatic_coupling_vector",
        "calculate_orbitals",
        "export_electron_density_grid",
        "optimize_geometry",
    },
    "periodic_materials": {
        spec.id for spec in ACTION_SPECS if spec.category == "periodic_and_phonons"
    },
    "molecular_dynamics": {
        spec.id for spec in ACTION_SPECS if spec.category == "molecular_dynamics"
    }
    | {
        "assign_force_field_parameters",
        "convert_amber_topology_to_gromacs",
        "generate_small_molecule_topology",
        "solvate_molecular_system",
    },
    "reaction_kinetics": {
        spec.id for spec in ACTION_SPECS if spec.category == "reaction_and_kinetics"
    },
    "free_energy": {
        "analyze_free_energy_convergence",
        "calculate_end_state_binding_free_energy",
        "calculate_end_state_energy_decomposition",
        "estimate_free_energy_difference",
        "generate_alchemical_hybrid_topology",
        "map_alchemical_ligand_atoms",
        "mutate_biomolecular_residues_for_alchemy",
        "parse_alchemical_energy_data",
        "summarize_end_state_free_energy_results",
    },
    "docking_conformer": {
        "cluster_conformers",
        "dock_ligand",
        "generate_3d_structure",
        "generate_conformer_ensemble",
        "rank_conformers_from_results",
    },
    "multiscale": set(),
    "machine_learning_chemistry": {
        "assess_symbolic_regression_seed_stability",
        "discover_sparse_symbolic_descriptor",
        "evaluate_sparse_symbolic_descriptor",
        "fit_symbolic_regression_baseline",
        "summarize_sparse_symbolic_descriptor_results",
        "summarize_symbolic_regression_results",
    },
}

FAMILY_EXTRA_BACKENDS = {
    "electronic_structure": {"bagel"},
    "periodic_materials": {"airss", "tdep", "vaspkit"},
    "molecular_dynamics": {"acpype", "pmx"},
    "reaction_kinetics": {"kinbot", "pyfrag"},
    "free_energy": {"acpype", "gmx_mmpbsa", "pmx"},
    "docking_conformer": {"censo", "crest"},
    "multiscale": {"charmm", "cp2k", "gromacs", "openmm"},
    "machine_learning_chemistry": {
        "allegro",
        "chgnet",
        "deepmd",
        "gplearn",
        "mace",
        "nequip",
        "rdkit",
        "sisso",
    },
}

REQUIRED_ACTIONS = {
    "electronic_structure": ["calculate_energy"],
    "periodic_materials": ["calculate_periodic_energy"],
    "molecular_dynamics": ["propagate_dynamics"],
    "reaction_kinetics": ["locate_transition_state"],
    "free_energy": ["analyze_free_energy_convergence"],
    "docking_conformer": [],
    "multiscale": [],
    "machine_learning_chemistry": [],
}


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def _identifier(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def _source_version() -> str:
    return subprocess.run(
        ["git", "log", "-1", "--format=%h", "--", "chemistry_toolbox"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _successful_backends() -> set[str]:
    evidence = _read_json(
        TOOLBOX_ROOT / "evidence/status/action_test_coverage.json"
    )
    if evidence.get("failed_action_backend_pairs"):
        raise ValueError("Toolbox evidence contains failed Action/Backend pairs")
    if evidence.get("unobserved_action_backend_pairs"):
        raise ValueError("Toolbox evidence contains unobserved Action/Backend pairs")
    output = {
        str(item["backend"] if isinstance(item, dict) else item[1])
        for item in evidence.get("successful_action_backend_pairs") or []
    }
    registered = {spec.id for spec in BACKEND_SPECS}
    missing = registered - output
    if missing:
        raise ValueError(f"Backends without successful evidence: {sorted(missing)}")
    return output


def _native_validation_levels() -> dict[str, str]:
    manifest = _read_json(
        TOOLBOX_ROOT
        / "evidence/native_interface_smoke/20260728_all_software/manifest.json"
    )
    output: dict[str, str] = {}
    for item in manifest.get("software") or []:
        software_id = str(item["software_id"])
        if item.get("status") == "started_input_required":
            output[software_id] = "needs_complete_input"
        elif item.get("test_level") == "scientific_smoke":
            output[software_id] = "functional"
        elif item.get("status") == "passed":
            output[software_id] = "interface"
    return output


def _requested_identifiers() -> set[str]:
    inventory = yaml.safe_load(
        (TOOLBOX_ROOT / "config/requested_software.yaml").read_text(encoding="utf-8")
    )
    output = set()
    for item in inventory.get("requested_software") or []:
        identifier = _identifier(str(item["name"]))
        output.add(REQUESTED_NAME_OVERRIDES.get(identifier, identifier))
    return output


def _requested_software_inventory() -> list[dict[str, Any]]:
    status = _read_json(
        TOOLBOX_ROOT / "evidence/status/requested_software_status.json"
    )
    records = status.get("software") or []
    return [item for item in records if isinstance(item, dict)]


def _software_aliases() -> dict[str, list[str]]:
    existing = _read_json(ASSET_ROOT / "software_aliases.json")
    aliases: dict[str, set[str]] = {
        str(identifier): {str(value) for value in values}
        for identifier, values in existing.items()
    }
    for backend in BACKEND_SPECS:
        if backend.id.startswith("internal_"):
            continue
        aliases.setdefault(backend.id, set()).add(backend.display_name)
        aliases[backend.id].update(
            executable
            for executable in backend.executables
            if executable.casefold() not in GENERIC_NATIVE_EXECUTABLES
            and _identifier(executable) not in EXCLUDED_SOFTWARE
        )
    for identifier, values in EXPLICIT_ALIASES.items():
        aliases.setdefault(identifier, set()).update(values)
    for identifier, values in PYTHON_PACKAGE_ALIASES.items():
        aliases.setdefault(identifier, set()).update(values)
    for item in _requested_software_inventory():
        identifier = REQUESTED_NAME_OVERRIDES.get(
            _identifier(str(item.get("name") or "")),
            _identifier(str(item.get("name") or "")),
        )
        if not identifier or identifier in EXCLUDED_SOFTWARE:
            continue
        aliases.setdefault(identifier, set()).add(str(item["name"]))
        aliases[identifier].update(str(value) for value in item.get("commands") or [])
    for identifier in EXCLUDED_SOFTWARE:
        aliases.pop(identifier, None)
    return {
        identifier: sorted(values, key=lambda value: (value.casefold(), value))
        for identifier, values in sorted(aliases.items())
    }


def _python_packages() -> dict[str, dict[str, Any]]:
    source = TOOLBOX_ROOT / "config/mcp_profiles.yaml"
    profile_config = yaml.safe_load(source.read_text(encoding="utf-8"))
    package_profiles: dict[str, set[str]] = defaultdict(set)
    for profile_name, profile in (profile_config.get("profiles") or {}).items():
        checks = profile.get("health_checks") or {}
        for module in checks.get("modules") or []:
            identifier = str(module).split(".", 1)[0].strip()
            if identifier:
                package_profiles[identifier].add(str(profile_name))
    return {
        identifier: {
            "display_name": next(
                iter(sorted(PYTHON_PACKAGE_ALIASES.get(identifier, {identifier})))
            ),
            "aliases": sorted(
                {identifier, *PYTHON_PACKAGE_ALIASES.get(identifier, set())},
                key=lambda value: (value.casefold(), value),
            ),
            "availability": "configured_in_toolbox_runtime",
            "validation_level": "runtime_health_check_declared",
            "profiles": sorted(profiles),
            "execution_layer": "task_specific_python",
            "evidence_refs": ["chemistry_toolbox/config/mcp_profiles.yaml"],
        }
        for identifier, profiles in sorted(package_profiles.items())
    }


def _native_software(aliases: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    backend_ids = {backend.id for backend in BACKEND_SPECS}
    records: dict[str, dict[str, Any]] = {}
    for item in _requested_software_inventory():
        identifier = REQUESTED_NAME_OVERRIDES.get(
            _identifier(str(item.get("name") or "")),
            _identifier(str(item.get("name") or "")),
        )
        if (
            not identifier
            or identifier in EXCLUDED_SOFTWARE
            or identifier in backend_ids
            or item.get("status") != "configured"
        ):
            continue
        verification = item.get("verification") or {}
        smoke_success = any(
            isinstance(value, dict) and value.get("success") is True
            for value in (verification.get("runtime_smokes") or {}).values()
        )
        module_success = any(
            isinstance(value, dict) and value.get("available") is True
            for value in (verification.get("modules") or {}).values()
        )
        command_success = bool(verification.get("commands"))
        records[identifier] = {
            "display_name": str(item.get("name") or identifier),
            "aliases": aliases.get(identifier, []),
            "kind": str(item.get("kind") or "unknown"),
            "role": str(item.get("role") or ""),
            "availability": "configured_in_toolbox_runtime",
            "local_installation_status": "configured",
            "validation_level": (
                "functional" if smoke_success or module_success else "interface"
                if command_success else "configured"
            ),
            "execution_layer": "native_software_documentation",
            "actions": [],
            "method_families": [],
            "limitations": str(item.get("notes") or "") or None,
            "evidence_refs": [
                "chemistry_toolbox/config/requested_software.yaml",
                "chemistry_toolbox/evidence/status/requested_software_status.json",
            ],
        }
    return dict(sorted(records.items()))


def _runtime_profile_hash() -> str:
    content = (TOOLBOX_ROOT / "config/mcp_profiles.yaml").read_bytes()
    return hashlib.sha256(content).hexdigest()


def _method_families() -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for family, actions in FAMILY_ACTIONS.items():
        backends = {
            backend.id
            for backend in BACKEND_SPECS
            if set(backend.capabilities) & actions
        }
        backends.update(FAMILY_EXTRA_BACKENDS.get(family, set()))
        output[family] = {
            "backends": sorted(backends),
            "required_actions": REQUIRED_ACTIONS[family],
            "limitations": None,
        }
    return output


def _profile(
    *,
    aliases: dict[str, list[str]],
    source_hash: str,
    functional_backends: set[str],
    native_levels: dict[str, str],
    python_packages: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    actions_by_domain: dict[str, list[str]] = defaultdict(list)
    for action in ACTION_SPECS:
        actions_by_domain[action.category].append(action.id)
    actions = sorted(action.id for action in ACTION_SPECS)
    backends = sorted(backend.id for backend in BACKEND_SPECS)
    native_functional = {
        name for name, level in native_levels.items() if level == "functional"
    }
    scientific_smoke = functional_backends | native_functional
    interface_smoke = {
        name for name, level in native_levels.items() if level == "interface"
    } - scientific_smoke
    needs_complete_input = {
        name
        for name, level in native_levels.items()
        if level == "needs_complete_input"
    } - scientific_smoke
    available = {
        *actions,
        *backends,
        *aliases,
        *_requested_identifiers(),
        *native_levels,
        *(backend.runtime for backend in BACKEND_SPECS),
        *python_packages,
    } - EXCLUDED_SOFTWARE
    return {
        "catalog_hash": source_hash,
        "code_version": _source_version(),
        "capability_scope": "declared catalog plus committed functional evidence",
        "local_installation_status": "not_evaluated",
        "validation_sources": [
            "chemistry_toolbox/evidence/status/action_test_coverage.json",
            "chemistry_toolbox/evidence/native_interface_smoke/20260728_all_software/manifest.json",
            "docs/tools_v2/CHEMISTRY_TOOLBOX_V2_CHANGE_SUMMARY.md",
        ],
        "scientific_smoke": sorted(scientific_smoke),
        "interface_smoke": sorted(interface_smoke),
        "needs_complete_input": sorted(needs_complete_input),
        "analysis_runtimes": sorted({backend.runtime for backend in BACKEND_SPECS}),
        "python_packages": sorted(python_packages),
        "execution_layers": [
            "predefined_action",
            "native_software_documentation",
            "task_specific_python",
        ],
        "generic_python_analysis": True,
        "unavailable": [],
        "actions_by_domain": {
            domain: sorted(values) for domain, values in sorted(actions_by_domain.items())
        },
        "actions": actions,
        "backends": backends,
        "available_identifiers": sorted(available),
        "profile_id": "researchchembench-toolbox-20260807-v2",
        "generated_from": (
            "current chemistry_toolbox Action/Backend catalog and committed validation evidence"
        ),
    }


def _capabilities(
    *,
    profile: dict[str, Any],
    aliases: dict[str, list[str]],
    families: dict[str, dict[str, Any]],
    python_packages: dict[str, dict[str, Any]],
    native_software: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    action_by_id = {action.id: action for action in ACTION_SPECS}
    backend_families = {
        backend.id: sorted(
            family
            for family, value in families.items()
            if backend.id in value["backends"]
        )
        for backend in BACKEND_SPECS
    }
    backend_records = {}
    for backend in sorted(BACKEND_SPECS, key=lambda item: item.id):
        output_properties = sorted(
            {
                action_by_id[action].primary_output
                for action in backend.capabilities
                if action in action_by_id
            }
        )
        limitations = []
        if backend.install_notes:
            limitations.append(backend.install_notes)
        if backend.resource_constraints:
            limitations.append(
                "resource_constraints="
                + json.dumps(dict(backend.resource_constraints), sort_keys=True)
            )
        capabilities = set(backend.capabilities)
        backend_records[backend.id] = {
            "display_name": backend.display_name,
            "aliases": aliases.get(backend.id, []),
            "availability": "declared_supported",
            "local_installation_status": "not_evaluated",
            "validation_level": (
                "functional"
                if backend.id in profile["scientific_smoke"]
                else "catalogued"
            ),
            "actions": sorted(backend.capabilities),
            "method_families": backend_families[backend.id],
            "system_types": {
                action: list(values)
                for action, values in backend.supported_system_types.items()
            }
            or "unknown",
            "elements": "unknown",
            "basis_or_pseudopotential_constraints": "unknown",
            "periodic_support": (
                "supported"
                if "periodic_materials" in backend_families[backend.id]
                else "unknown"
            ),
            "excited_state_support": (
                "supported"
                if capabilities
                & {
                    "calculate_excited_states",
                    "calculate_multireference_state_energies",
                    "calculate_nonadiabatic_coupling_vector",
                    "propagate_nonadiabatic_trajectory",
                }
                else "unknown"
            ),
            "solvent_support": "unknown",
            "force_field_support": (
                "supported"
                if capabilities
                & {
                    "assign_force_field_parameters",
                    "calculate_force_field_energy",
                    "calculate_force_field_forces",
                    "generate_alchemical_hybrid_topology",
                    "generate_small_molecule_topology",
                }
                else "unknown"
            ),
            "input_formats": "unknown",
            "output_properties": output_properties,
            "method_constraints": dict(backend.method_schema) or "unknown",
            "allowed_method_values": {
                action: {field: list(values) for field, values in fields.items()}
                for action, fields in backend.allowed_method_values.items()
            }
            or "unknown",
            "limitations": limitations or None,
            "evidence_refs": [
                "chemistry_toolbox/evidence/status/action_test_coverage.json"
            ],
            "catalog_hash": profile["catalog_hash"],
        }
    return {
        "schema_version": 2,
        "profile_id": profile["profile_id"],
        "catalog_hash": profile["catalog_hash"],
        "runtime_profile_hash": _runtime_profile_hash(),
        "source_profile": "assets/toolbox.json",
        "source_toolbox": "chemistry_toolbox",
        "unknown_field_policy": "unknown",
        "local_installation_status": "not_evaluated",
        "method_families": families,
        "backends": backend_records,
        "native_software": native_software,
        "python_packages": python_packages,
        "execution_layers": profile["execution_layers"],
        "generic_python_analysis": profile["generic_python_analysis"],
    }


def _render(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def _write_or_check(path: Path, value: dict[str, Any], *, check: bool) -> bool:
    rendered = _render(value)
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    if current == rendered:
        return False
    if check:
        raise SystemExit(f"Stale generated toolbox asset: {path.relative_to(PROJECT_ROOT)}")
    path.write_text(rendered, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="fail if generated assets are stale"
    )
    args = parser.parse_args()

    validate_catalog()
    source_hash = catalog_hash(include_health=False)
    functional_backends = _successful_backends()
    native_levels = _native_validation_levels()
    aliases = _software_aliases()
    python_packages = _python_packages()
    native_software = _native_software(aliases)
    families = _method_families()
    profile = _profile(
        aliases=aliases,
        source_hash=source_hash,
        functional_backends=functional_backends,
        native_levels=native_levels,
        python_packages=python_packages,
    )
    capabilities = _capabilities(
        profile=profile,
        aliases=aliases,
        families=families,
        python_packages=python_packages,
        native_software=native_software,
    )

    changed = []
    for name, value in (
        ("software_aliases.json", aliases),
        ("toolbox.json", profile),
        ("toolbox_capabilities.json", capabilities),
    ):
        path = ASSET_ROOT / name
        if _write_or_check(path, value, check=args.check):
            changed.append(name)
    if not args.check:
        print(
            f"Synchronized {len(profile['actions'])} actions, "
            f"{len(profile['backends'])} backends; changed={changed or 'none'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

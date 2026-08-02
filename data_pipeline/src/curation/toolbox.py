from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.core.io import read_json

ALIASES = {
    "gaussian 16": "gaussian",
    "gaussian16": "gaussian",
    "gaussian 09": "gaussian",
    "open babel": "openbabel",
    "quantum espresso": "quantum_espresso",
    "qe": "quantum_espresso",
    "pwscf": "quantum_espresso",
    "dftb+": "dftbplus",
    "gfn1-xtb": "xtb",
    "gfn2-xtb": "xtb",
    "gfn1 xtb": "xtb",
    "gfn2 xtb": "xtb",
    "newton-x": "newton_x",
    "newtonx": "newton_x",
    "rmg-py": "rmg",
    "rmgpy": "rmg",
    "amber": "amber_pmemd",
    "ase": "ase_emt",
    "pdb-tools": "pdb_tools",
    "openff": "openff",
    "rdkit": "rdkit",
    "pymatgen": "pymatgen",
    "cclib": "cclib",
    "pyscf": "pyscf",
    "tblite": "tblite",
    "terachem": "terachem",
    "mace": "mace",
    "chgnet": "chgnet",
    "allegro": "allegro",
    "hoomd": "hoomd",
    "mdanalysis": "mdanalysis",
    "mdtraj": "mdtraj",
    "pymbar": "pymbar",
    "alchemlyb": "alchemlyb",
    "cantera": "cantera",
    "scipy": "scipy",
    "spglib": "spglib",
    "pdbfixer": "pdbfixer",
}


NON_SOFTWARE_TERMS = {
    "dft",
    "td-dft",
    "wavefunction",
    "molecular_dynamics",
    "metadynamics",
    "transition_state",
    "microkinetics",
    "machine_learning_potential",
    "docking",
    "monte_carlo",
    "frequency calculation",
    "neb",
    "irc",
}


METHOD_CAPABILITIES = {
    "dft": ("calculate_energy", "optimize_geometry", "calculate_forces"),
    "td-dft": ("calculate_excited_states",),
    "wavefunction": ("calculate_energy", "calculate_correlated_electron_density"),
    "molecular_dynamics": ("propagate_dynamics",),
    "metadynamics": ("propagate_dynamics", "evaluate_collective_variables"),
    "transition_state": ("locate_transition_state", "validate_reaction_path"),
    "neb": ("search_reaction_path", "validate_reaction_path"),
    "irc": ("trace_intrinsic_reaction_coordinate",),
    "microkinetics": ("solve_microkinetic_model", "integrate_reaction_network"),
    "machine_learning_potential": ("calculate_energy", "calculate_forces"),
    "docking": ("dock_ligand",),
    "frequency calculation": ("calculate_hessian", "derive_vibrational_modes"),
}

TEXT_SCANNABLE_SOFTWARE = {
    "automekin",
    "catmap",
    "censo",
    "charmm",
    "cp2k",
    "crest",
    "deepmd",
    "dftbplus",
    "gamess",
    "goodvibes",
    "gromacs",
    "kinbot",
    "lammps",
    "lobster",
    "mesmer",
    "mess",
    "multiwfn",
    "namd",
    "newton_x",
    "nwchem",
    "openmm",
    "openmolcas",
    "orca",
    "packmol",
    "phono3py",
    "phonopy",
    "plumed",
    "psi4",
    "pyscf",
    "quantum_espresso",
    "rmg",
    "sharc",
    "siesta",
    "terachem",
    "turbomole",
    "vasp",
    "xtb",
    "yambo",
}


def load_toolbox_profile(
    path: str | Path,
    selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profile = read_json(path)
    if not isinstance(profile, dict):
        raise ValueError("toolbox profile must be a JSON object")
    selection = selection or {}
    enabled_software = selection.get("enabled_software", ["*"])
    enabled_actions = selection.get("enabled_actions", ["*"])
    priority_values = selection.get("priority_software", [])

    all_software = set(profile.get("available_identifiers", []))
    if enabled_software != ["*"] and "*" not in enabled_software:
        all_software.intersection_update(_normalize(value) for value in enabled_software)
    all_actions = set(profile.get("actions", []))
    if enabled_actions != ["*"] and "*" not in enabled_actions:
        all_actions.intersection_update(enabled_actions)
    priority_software = (
        set(all_software)
        if "*" in priority_values
        else {_normalize(value) for value in priority_values}
    )

    selected = dict(profile)
    selected["available_identifiers"] = sorted(all_software | all_actions)
    selected["actions"] = sorted(all_actions)
    selected["priority_software"] = sorted(priority_software)
    selected["selection"] = {
        "enabled_software": enabled_software,
        "enabled_actions": enabled_actions,
        "priority_software": selection.get("priority_software", []),
        "preserve_priority_matches": selection.get("preserve_priority_matches", True),
    }
    return selected


def assess_toolbox_coverage(
    record: dict[str, Any],
    profile: dict[str, Any] | None,
) -> dict[str, Any]:
    if not profile:
        return {
            "status": "not_configured",
            "required_software": [],
            "directly_available": [],
            "unavailable": [],
            "unknown": [],
            "direct_coverage": 0.0,
            "capability_coverage": 0.0,
        }

    classification = record.get("source_classification") or {}
    candidates = list(classification.get("software", []))
    candidates.extend(record.get("tools", []))
    candidates.extend(_software_from_methods(record.get("methods", []), profile))
    candidates.extend(_software_from_asset_text(record, profile))
    required = []
    for value in candidates:
        normalized = _normalize(value)
        if normalized in NON_SOFTWARE_TERMS or normalized in required:
            continue
        if _looks_like_method(value):
            continue
        required.append(normalized)

    available = set(profile.get("available_identifiers", []))
    unavailable_set = set(profile.get("unavailable", []))
    direct = [value for value in required if value in available and value not in unavailable_set]
    blocked = [value for value in required if value in unavailable_set]
    unknown = [
        value for value in required if value not in available and value not in unavailable_set
    ]

    methods = list(classification.get("methods", [])) + list(record.get("methods", []))
    method_keys = {_normalize_method(value) for value in methods}
    requested_actions = sorted(
        {action for method in method_keys for action in METHOD_CAPABILITIES.get(method, ())}
    )
    action_set = set(profile.get("actions", []))
    covered_actions = [action for action in requested_actions if action in action_set]
    direct_ratio = len(direct) / len(required) if required else 1.0
    capability_ratio = (
        len(covered_actions) / len(requested_actions) if requested_actions else direct_ratio
    )
    evidence_levels = _software_evidence_levels(required, profile)
    input_dependent = sorted(
        value for value in required if evidence_levels.get(value) == "starts_requires_input"
    )
    functional_validation_pending = sorted(
        value
        for value in required
        if evidence_levels.get(value)
        in {"interface_smoke", "starts_requires_input", "healthy_backend"}
    )
    if blocked:
        coverage_state = "confirmed_unavailable"
    elif unknown:
        coverage_state = "partial_coverage"
    elif functional_validation_pending:
        coverage_state = "mapped_pending_functional_validation"
    else:
        coverage_state = "confirmed_covered"
    return {
        "status": "assessed",
        "coverage_state": coverage_state,
        "required_software": required,
        "directly_available": direct,
        "unavailable": blocked,
        "unknown": unknown,
        "direct_coverage": round(direct_ratio, 3),
        "requested_actions": requested_actions,
        "covered_actions": covered_actions,
        "capability_coverage": round(capability_ratio, 3),
        "software_evidence_levels": evidence_levels,
        "input_dependent_software": input_dependent,
        "functional_validation_pending": functional_validation_pending,
        "toolbox_profile_id": profile.get("profile_id"),
        "toolbox_catalog_hash": profile.get("catalog_hash"),
        "priority_matches": sorted(set(required) & set(profile.get("priority_software", []))),
        "preserve_priority_matches": (profile.get("selection") or {}).get(
            "preserve_priority_matches", True
        ),
    }


def _software_from_methods(methods: list[Any], profile: dict[str, Any]) -> list[str]:
    catalog = set(profile.get("backends", []))
    catalog.update(profile.get("scientific_smoke", []))
    catalog.update(profile.get("interface_smoke", []))
    catalog.update(profile.get("needs_complete_input", []))
    catalog.update(profile.get("unavailable", []))
    output = []
    for method in methods:
        if isinstance(method, dict):
            values = [
                method.get("software"),
                method.get("program"),
                method.get("tool"),
                method.get("name"),
                method.get("method_name"),
                method.get("description"),
            ]
        else:
            values = [method]
        for raw in values:
            for text in _text_values(raw):
                if not text:
                    continue
                normalized = _normalize(text)
                if normalized in catalog or normalized in ALIASES.values():
                    output.append(normalized)
                lowered = re.sub(r"[^a-z0-9+]+", " ", text.casefold()).strip()
                for identifier in catalog:
                    phrase = identifier.replace("_", " ")
                    if re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", lowered):
                        output.append(identifier)
                if "gfn1-xtb" in text.casefold() or "gfn2-xtb" in text.casefold():
                    output.append("xtb")
    return list(dict.fromkeys(output))


def _software_from_asset_text(record: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    assets = record.get("assets") or {}
    chunks = []
    for raw in assets.get("text", []):
        path = Path(str(raw))
        if path.is_file():
            chunks.append(path.read_text(encoding="utf-8", errors="replace")[:2_000_000])
    if not chunks:
        return []
    source = "\n".join(
        re.split(
            r"\n#{0,3}\s*(?:references|bibliography)\b",
            chunk.casefold(),
            maxsplit=1,
        )[0]
        for chunk in chunks
    )
    text = re.sub(r"[^a-z0-9+]+", " ", source)
    catalog = set(profile.get("backends", []))
    catalog.update(profile.get("scientific_smoke", []))
    catalog.update(profile.get("interface_smoke", []))
    catalog.update(profile.get("needs_complete_input", []))
    catalog.update(profile.get("unavailable", []))
    catalog.intersection_update(TEXT_SCANNABLE_SOFTWARE)
    catalog.add("terachem")
    found = []
    for identifier in catalog:
        phrase = identifier.replace("_", " ")
        if re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", text):
            found.append(identifier)
    return found


def _text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if item]
    return [str(value).strip()] if value else []


def _software_evidence_levels(required: list[str], profile: dict[str, Any]) -> dict[str, str]:
    scientific = set(profile.get("scientific_smoke", []))
    interface = set(profile.get("interface_smoke", []))
    needs_input = set(profile.get("needs_complete_input", []))
    backends = set(profile.get("backends", []))
    unavailable = set(profile.get("unavailable", []))
    output = {}
    for value in required:
        if value in unavailable:
            output[value] = "unavailable_or_unreliable"
        elif value in scientific:
            output[value] = "scientific_smoke"
        elif value in interface:
            output[value] = "interface_smoke"
        elif value in needs_input:
            output[value] = "starts_requires_input"
        elif value in backends:
            output[value] = "healthy_backend"
        else:
            output[value] = "unknown"
    return output


def _normalize(value: str) -> str:
    normalized = value.strip().casefold().replace("_", " ")
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s+(?:09|16|17|23)$", "", normalized)
    return ALIASES.get(normalized, normalized.replace(" ", "_"))


def _normalize_method(value: Any) -> str:
    normalized = _method_text(value).strip().casefold().replace("_", " ")
    if "td-dft" in normalized or "td dft" in normalized:
        return "td-dft"
    if "transition state" in normalized:
        return "transition_state"
    if "molecular dynamics" in normalized:
        return "molecular_dynamics"
    if "frequency" in normalized:
        return "frequency calculation"
    if "microkinetic" in normalized:
        return "microkinetics"
    if "machine learning potential" in normalized:
        return "machine_learning_potential"
    if "density functional" in normalized or normalized == "dft":
        return "dft"
    if "intrinsic reaction coordinate" in normalized or normalized == "irc":
        return "irc"
    if "nudged elastic band" in normalized or normalized == "neb":
        return "neb"
    return normalized.replace(" ", "_")


def _method_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        preferred = (
            value.get("name")
            or value.get("method_name")
            or value.get("method")
            or value.get("software")
            or value.get("action")
            or value.get("description")
        )
        return str(preferred or "")
    return str(value or "")


def _looks_like_method(value: str) -> bool:
    lower = value.casefold()
    signals = (
        "basis set",
        "functional",
        "geometry optimization",
        "frequency",
        "solvation",
        "transition-state",
        "transition state",
        "vertical excitation",
        "density functional",
        "molecular dynamics",
        "calculation",
        "analysis",
    )
    return any(signal in lower for signal in signals)

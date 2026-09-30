"""Resolve declared molecular state without inferring a scientific charge/spin."""
from __future__ import annotations

import os
import re

POLICY_ENV = "RESEARCHCHEMBENCH_ELECTRONIC_STATE_POLICY"
STRUCTURE_ROLES = frozenset({"structure", "molecule", "initial_structure", "initial_guess", "transition_state", "reactant", "product"})


class ElectronicStateError(ValueError):
    def __init__(self, code, message, issues):
        super().__init__(message)
        self.details = {"code": code, "message": message, "input_issues": issues,
                        "failure_stage": "input_preflight", "category": "invalid_input"}


def integer(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, str)) or not re.fullmatch(r"[+-]?\d+", str(value)):
        raise ElectronicStateError("electronic_state_invalid", f"{field} must be an integer", [{"field": field, "received": value}])
    return int(value)


def resolve_state(structure, method, *, field="inputs.structure", policy="legacy"):
    values, sources, warnings = {}, {}, []
    prior = structure.get("electronic_state_sources") or {}
    supplied = dict(method)
    spin_values = [(k, integer(method[k], "method_spec." + k) + 1) for k in ("spin", "unpaired_electrons") if k in method]
    if spin_values:
        if len({v for _, v in spin_values}) > 1 or ("multiplicity" in method and integer(method["multiplicity"], "method_spec.multiplicity") != spin_values[0][1]):
            raise ElectronicStateError("electronic_state_invalid", "Conflicting explicit spin and multiplicity", [{"field": "method_spec", "received": method}])
        supplied["multiplicity"] = spin_values[0][1]
    for name, default in (("charge", 0), ("multiplicity", 1)):
        if name in supplied:
            values[name] = integer(supplied[name], "method_spec." + name)
            sources[name] = "method_spec." + (spin_values[0][0] if name == "multiplicity" and spin_values else name)
            if name in structure and prior.get(name) != "legacy_default" and structure[name] != values[name]:
                warnings.append(f"Explicit {sources[name]}={values[name]} overrides {field}.{name}={structure[name]}")
        elif name in structure and prior.get(name) != "legacy_default":
            values[name] = integer(structure[name], field + "." + name)
            sources[name] = prior.get(name, "structured_input")
        elif policy == "strict":
            raise ElectronicStateError("missing_electronic_state", f"No declared {name} for {field}; supply method_spec.{name} or structured electronic state.",
                                       [{"field": "method_spec." + name, "input": field, "constraint": "explicit electronic state required"}])
        else:
            values[name], sources[name] = default, "legacy_default"
            warnings.append(f"{field}.{name} uses legacy default {default}; no explicit state was parsed")
    if values["multiplicity"] < 1:
        raise ElectronicStateError("electronic_state_invalid", "multiplicity must be positive", [{"field": "method_spec.multiplicity"}])
    coverage, reason = "not_checked", "legacy policy"
    pbc = structure.get("pbc", False)
    periodic = any(pbc) if isinstance(pbc, (list, tuple)) else bool(pbc)
    special = any(method.get(k) is not None for k in ("ecp", "pseudopotential", "pseudopotentials", "occupations", "fractional_occupations", "effective_electrons"))
    if periodic or special:
        reason = "Periodic, effective-electron or noninteger-occupation conventions require the backend-specific check"
    elif policy == "strict" and (structure.get("atoms") or structure.get("symbols")):
        from .backends.common import atoms_and_coordinates
        symbols, _ = atoms_and_coordinates(structure)
        # A fixed periodic table avoids requiring a particular quantum runtime.
        table = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split()
        numbers = {symbol: i + 1 for i, symbol in enumerate(table)}
        if all(s in numbers for s in symbols):
            n = sum(numbers[s] for s in symbols) - values["charge"]
            spin = values["multiplicity"] - 1
            if n < spin or (n - spin) % 2:
                raise ElectronicStateError("electronic_state_invalid", f"Electron count {n} and multiplicity {values['multiplicity']} are inconsistent for a finite integer-electron system.",
                                           [{"field": field, "electron_count": n, **values}])
            coverage, reason = "checked", "finite integer-electron consistency only; no scientific validation"
        else:
            reason = "Unknown/ghost element convention"
    resolved = {**structure, **values, "electronic_state_sources": sources}
    return resolved, {**values, "sources": sources, "warnings": warnings, "validation": coverage, "validation_reason": reason, "policy": policy}


def preflight_inputs(backend, specification, inputs, method, *, policy=None):
    policy = policy or os.environ.get(POLICY_ENV, "legacy")
    if policy not in {"legacy", "strict"}:
        raise ElectronicStateError("electronic_state_invalid", f"Unknown electronic state policy: {policy}", [])
    if backend.electronic_state_model != "finite_molecular":
        return inputs, {"electronic_state": {"validation": "not_applicable", "reason": "Backend does not declare the finite molecular state contract"}}
    from .backends.common import structure_dict
    effective, resolved = {}, dict(inputs)
    roles = STRUCTURE_ROLES & set((*specification.required_inputs, *specification.optional_inputs,
                                  *backend.required_input_fields.get(specification.id, ())))
    # CREST's declared initial_structure overrides molecule in its public contract.
    if "initial_structure" in inputs and "initial_structure" in roles:
        roles = roles - {"molecule"}
    for role in sorted(roles & inputs.keys()):
        structure = structure_dict(inputs[role])
        resolved[role], effective[role] = resolve_state(structure, method, field="inputs." + role, policy=policy)
    return resolved, {"electronic_state": effective or {"validation": "not_checked", "reason": "This Action uses a native file or no declared structural input"}}


def inherit_state(output_structure, input_structure, method):
    """For an adapter's state-preserving geometry output (XYZ has no state)."""
    resolved, _ = resolve_state(input_structure, method)
    return {**output_structure, **{k: resolved[k] for k in ("charge", "multiplicity", "electronic_state_sources")}}

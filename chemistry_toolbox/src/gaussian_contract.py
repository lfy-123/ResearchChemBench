"""Shared input contract for the typed Gaussian vertical-excitation Action."""

from __future__ import annotations

import re
from typing import Any


# Keep the first typed surface explicit. Other Gaussian methods remain available
# through native jobs; a method is never substituted to satisfy this contract.
GAUSSIAN_EXCITED_FUNCTIONALS = (
    "B3LYP", "CAM-B3LYP", "PBE1PBE", "PBEPBE", "BLYP", "M062X", "wB97XD", "APFD",
)


def validate_gaussian_dispersion(value: Any) -> str:
    text = str(value).strip()
    if not re.fullmatch(r"EmpiricalDispersion=(?:GD2|GD3|GD3BJ)", text, re.I):
        raise ValueError("Gaussian dispersion must be EmpiricalDispersion=GD2, EmpiricalDispersion=GD3 or EmpiricalDispersion=GD3BJ")
    return text


def validate_gaussian_excited_request(
    structure: dict[str, Any], method: dict[str, Any], settings: dict[str, Any],
) -> None:
    """Validate without starting Gaussian; also called by the input renderer."""
    functional = str(method["method"]).strip().casefold()
    if functional not in {name.casefold() for name in GAUSSIAN_EXCITED_FUNCTIONALS}:
        raise ValueError("Gaussian vertical excitations require a supported restricted DFT functional: "
                         + ", ".join(GAUSSIAN_EXCITED_FUNCTIONALS))
    if not re.fullmatch(r"[A-Za-z0-9+*(),._-]+", str(method["basis"])):
        raise ValueError("Gaussian basis must be a built-in basis keyword, not an input deck")
    if str(method["basis"]).casefold() in {"gen", "genecp", "chkbasis", "chkbas"}:
        raise ValueError("Gaussian excited-state Action requires a self-contained built-in basis")
    pbc = structure.get("pbc", False)
    periodic = any(pbc) if isinstance(pbc, (list, tuple)) else bool(pbc)
    if periodic:
        raise ValueError("Gaussian vertical excitations require a non-periodic structure")
    if method.get("multiplicity", structure.get("multiplicity", 1)) != 1:
        raise ValueError("Gaussian vertical excitations currently require a closed-shell singlet ground state; "
                         "choose the excited-state spin with action_settings.spin_symmetry")
    if str(settings["spin_symmetry"]).strip().lower() not in {"singlet", "triplet"}:
        raise ValueError("Gaussian spin_symmetry must be singlet or triplet")
    if str(method["excited_state_method"]).strip().lower() not in {"tddft", "tda"}:
        raise ValueError("Gaussian excited_state_method must be tddft or tda")
    count = settings["number_of_states"]
    if type(count) is not int or count < 1:
        raise ValueError("Gaussian number_of_states must be a positive integer")
    if str(settings["scf_convergence"]).strip().lower() not in {"loose", "tight", "verytight"}:
        raise ValueError("Gaussian scf_convergence must be Loose, Tight, or VeryTight")
    convergence = settings.get("td_convergence")
    if convergence is not None and (type(convergence) is not int or not 4 <= convergence <= 12):
        raise ValueError("Gaussian td_convergence must be an integer from 4 to 12 or null")
    foreign = {"excited_energy_tolerance_hartree", "residual_tolerance"} & settings.keys()
    if foreign:
        raise ValueError("Gaussian does not use ORCA convergence controls " + ", ".join(sorted(foreign))
                         + "; use td_convergence (Gaussian Conver=N)")
    dispersion = method.get("dispersion")
    if dispersion is not None:
        validate_gaussian_dispersion(dispersion)
    if method.get("solvent") is not None and method.get("solvation_model") is None:
        raise ValueError("Gaussian solvent requires an explicit solvation_model")
    if method.get("solvation_model") is not None:
        if str(method["solvation_model"]).strip().lower() not in {"pcm", "cpcm", "smd"} or not method.get("solvent"):
            raise ValueError("Gaussian solvation requires pcm/cpcm/smd and an explicit solvent")
        if not re.fullmatch(r"[A-Za-z0-9_.+-]+", str(method["solvent"])):
            raise ValueError("Gaussian solvent must be a solvent keyword")


def gaussian_excited_keyword(method: dict[str, Any], settings: dict[str, Any]) -> str:
    keyword = "TD" if str(method["excited_state_method"]).strip().lower() == "tddft" else "TDA"
    options = [f"NStates={settings['number_of_states']}", str(settings["spin_symmetry"]).strip().title() + "s"]
    if settings.get("td_convergence") is not None:
        options.append(f"Conver={settings['td_convergence']}")
    return keyword + "=(" + ",".join(options) + ")"

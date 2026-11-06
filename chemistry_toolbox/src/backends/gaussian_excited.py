"""Read Gaussian 16's final vertical TD/TDA block without loading logs into an LLM."""

from __future__ import annotations

import math
import re
from typing import Any


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[DdEe][-+]?\d+)?"
_STATE = re.compile(
    rf"^[ \t]*Excited State\s+(\d+):\s+(\S+)\s+({_FLOAT})\s+eV\s+({_FLOAT})\s+nm([^\n]*)",
    re.M,
)
_TRANSITION = re.compile(rf"^\s*(\d+)([ABab]?)\s*(->|<-)\s*(\d+)([ABab]?)\s+({_FLOAT})\s*$")


def _number(value: str) -> float:
    number = float(value.replace("D", "E").replace("d", "e"))
    if not math.isfinite(number):
        raise ValueError("Non-finite Gaussian excited-state value")
    return number


def parse_gaussian_excited_states(
    text: str, *, number_of_states: int, spin_symmetry: str, output_file: str,
) -> tuple[dict[str, Any], list[str]]:
    """Return observed states and explicit incompleteness, never guessed zeros.

    Only the final SCF calculation and its final excitation block are eligible.
    Printed orbital coefficients retain their native meaning and truncation;
    they are not converted into normalized probabilities.
    """
    scfs = list(re.finditer(r"SCF Done:", text))
    if not scfs:
        raise ValueError("No Gaussian SCF result precedes the excitation block")
    start = scfs[-1].start()
    calculation = text[start:]
    headers = list(re.finditer(r"Excitation energies and oscillator strengths[^\n]*", calculation))
    if not headers:
        raise ValueError("No final Gaussian excitation-energy block after the last SCF result")
    block_start = start + headers[-1].end()
    block = text[block_start:]
    matches = list(_STATE.finditer(block))
    if not matches:
        raise ValueError("No readable states in the final Gaussian excitation block")

    occupations = list(re.finditer(r"(\d+)\s+alpha electrons\s+(\d+)\s+beta electrons", text[:start]))
    homo = None
    if occupations:
        alpha, beta = map(int, occupations[-1].groups())
        if alpha != beta:
            raise ValueError("Gaussian output is not a closed-shell reference")
        homo = alpha
    issues: list[str] = []
    states: list[dict[str, Any]] = []
    seen: set[int] = set()
    for position, match in enumerate(matches):
        index = int(match.group(1))
        if index in seen:
            raise ValueError(f"Duplicate state index {index} in final Gaussian excitation block")
        seen.add(index)
        label = match.group(2)
        spin = label.split("-", 1)[0].casefold()
        if spin != spin_symmetry:
            raise ValueError(f"Gaussian returned {spin} state {index}, requested {spin_symmetry}")
        energy, wavelength = _number(match.group(3)), _number(match.group(4))
        if energy <= 0 or wavelength <= 0:
            raise ValueError(f"Non-positive excitation energy/wavelength for Gaussian state {index}")
        strength = re.search(rf"\bf\s*=\s*({_FLOAT})", match.group(5))
        oscillator = _number(strength.group(1)) if strength else None
        if oscillator is None:
            issues.append(f"State {index}: oscillator strength is missing, not zero.")
        elif oscillator < 0:
            raise ValueError(f"Negative oscillator strength for Gaussian state {index}")
        squared = re.search(rf"<S\*\*2>\s*=\s*({_FLOAT})", match.group(5))
        state: dict[str, Any] = {
            "state_index": index, "energy_ev": energy, "wavelength_nm": wavelength,
            "oscillator_strength": oscillator, "spin_symmetry": spin,
            "multiplicity": 1 if spin == "singlet" else 3, "symmetry_label": label,
            "source": {"path": output_file, "line_start": text.count("\n", 0, block_start + match.start()) + 1},
        }
        if squared:
            state["spin_squared"] = _number(squared.group(1))
        stop = matches[position + 1].start() if position + 1 < len(matches) else len(block)
        transitions = []
        for line in block[match.end():stop].splitlines():
            if not line.strip():
                continue
            transition = _TRANSITION.fullmatch(line)
            if not transition:
                break
            occupied, orbital_spin, direction, virtual, target_spin, coefficient = transition.groups()
            item: dict[str, Any] = {
                "from_orbital": int(occupied), "to_orbital": int(virtual),
                "direction": direction, "coefficient": _number(coefficient),
            }
            if orbital_spin or target_spin:
                item.update(from_spin=orbital_spin.upper(), to_spin=target_spin.upper())
            if homo is not None:
                def orbital_label(orbital):
                    if orbital <= homo:
                        return "HOMO" if orbital == homo else f"HOMO-{homo - orbital}"
                    return "LUMO" if orbital == homo + 1 else f"LUMO+{orbital - homo - 1}"
                item.update(from_label=orbital_label(int(occupied)), to_label=orbital_label(int(virtual)))
            transitions.append(item)
        state["printed_transitions"] = transitions
        states.append(state)

    # Dipole rows belong to this calculation, immediately before the final states.
    prefix = text[start:block_start]
    tables = list(re.finditer(r"Ground to excited state transition electric dipole moments[^\n]*", prefix))
    if tables:
        by_index = {state["state_index"]: state for state in states}
        rows_started = False
        for line in prefix[tables[-1].end():].splitlines():
            row = re.fullmatch(rf"\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*", line)
            if row:
                rows_started = True
                index = int(row.group(1))
                if index in by_index:
                    by_index[index]["transition_dipole_atomic_unit"] = [_number(row.group(i)) for i in (2, 3, 4)]
            elif rows_started:
                break

    expected = set(range(1, number_of_states + 1))
    if seen != expected:
        issues.append(f"Requested states 1..{number_of_states}; observed indices {sorted(seen)}.")
    converged = bool(re.search(r"Convergence (?:achieved )?on expansion vectors\.", prefix))
    if not converged:
        issues.append("Gaussian excited-state solver convergence was not confirmed in the final calculation.")
    if "Normal termination of Gaussian 16" not in block or "Error termination" in block:
        issues.append("Gaussian normal termination was not confirmed after the final states.")
    result = {
        "states": states, "spin_symmetry": spin_symmetry,
        "number_of_states_requested": number_of_states, "number_of_states_observed": len(states),
        "converged": converged, "complete": not issues, "output_file": output_file,
        "orbital_index_base": 1, "homo_orbital_index": homo,
        "lumo_orbital_index": homo + 1 if homo is not None else None,
        "transition_coefficient_definition": (
            "Native Gaussian printed excitation/de-excitation coefficients; only printed terms are present. "
            "These are not normalized probabilities or a complete excitation vector."
        ),
    }
    return result, issues

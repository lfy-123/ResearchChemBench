"""Typed atomic adapters for operator-provided Gaussian and GAMESS runtimes."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .common import (
    atoms_and_coordinates,
    command_artifacts,
    output_directory,
    partial_success,
    relative_workspace_path,
    request_parts,
    run_external,
    structure_dict,
    success,
    unavailable,
    unsupported,
)


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[DdEe][-+]?\d+)?"
_PERIODIC_SYMBOLS = (
    "",
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
)
_ATOMIC_NUMBERS = {symbol.lower(): number for number, symbol in enumerate(_PERIODIC_SYMBOLS) if symbol}


def _finite_float(value: Any, name: str, *, positive: bool = False) -> float:
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        qualifier = "positive and " if positive else ""
        raise ValueError(f"{name} must be {qualifier}finite")
    return result


def _safe_keyword(value: Any, name: str, pattern: str = r"[A-Za-z0-9+*(),./_=-]+") -> str:
    text = str(value).strip()
    if not text or not re.fullmatch(pattern, text):
        raise ValueError(f"{name} contains unsupported characters")
    return text


def _gaussian_scf_or_dft_method(value: Any) -> str:
    method = _safe_keyword(value, "Gaussian method")
    unsupported_fragments = (
        "MP2", "MP3", "MP4", "CCSD", "QCISD", "CASSCF", "CASPT",
        "CISD", "EOM", "B2PLYP", "DSD", "CBS-", "G4", "W1",
    )
    if any(fragment in method.upper() for fragment in unsupported_fragments):
        raise ValueError(
            "The Gaussian adapter currently reports SCF/DFT total energies only; "
            "correlated/composite methods are not accepted until their energies have a typed parser"
        )
    return method


def _molecular_structure(value: Any) -> tuple[dict[str, Any], list[str], list[list[float]]]:
    structure = structure_dict(value)
    if any(bool(flag) for flag in structure.get("pbc", [])):
        raise ValueError("Gaussian/GAMESS molecular adapters require a non-periodic structure")
    symbols, coordinates = atoms_and_coordinates(structure)
    return structure, symbols, coordinates


def _render_gaussian(
    action_id: str,
    structure_value: Any,
    method: dict[str, Any],
    settings: dict[str, Any],
    resource_limits: dict[str, Any] | None = None,
) -> str:
    """Render one bounded Gaussian job without accepting an arbitrary route deck."""

    structure, symbols, coordinates = _molecular_structure(structure_value)
    method_name = _gaussian_scf_or_dft_method(method["method"])
    basis = _safe_keyword(method["basis"], "Gaussian basis")
    if action_id == "optimize_geometry":
        max_steps = int(settings["max_steps"])
        if max_steps < 1:
            raise ValueError("Gaussian max_steps must be positive")
        task_keyword = (
            "Opt=("
            + _safe_keyword(
                settings["optimization_convergence"],
                "Gaussian optimization convergence",
                r"[A-Za-z0-9_-]+",
            )
            + f",MaxCycles={max_steps})"
        )
    else:
        task_keyword = {
            "calculate_energy": "SP",
            "calculate_hessian": "Freq",
            "calculate_dipole_moment": "SP",
        }[action_id]
    scf_keyword = _safe_keyword(
        settings["scf_convergence"],
        "Gaussian SCF convergence",
        r"[A-Za-z0-9_-]+",
    )
    route = [f"{method_name}/{basis}", task_keyword, f"SCF={scf_keyword}"]
    if method.get("dispersion"):
        route.append(_safe_keyword(method["dispersion"], "Gaussian dispersion"))
    limits = resource_limits or {}
    cores = max(1, int(limits.get("cpu_cores") or 1))
    memory_mb = max(128, int(limits.get("memory_mb") or 1000))
    charge = int(method.get("charge", structure.get("charge", 0)))
    multiplicity = int(method.get("multiplicity", structure.get("multiplicity", 1)))
    if multiplicity < 1:
        raise ValueError("Gaussian multiplicity must be at least one")
    lines = [
        "%Chk=job.chk",
        f"%NProcShared={cores}",
        f"%Mem={memory_mb}MB",
        "#P " + " ".join(route),
        "",
        "ResearchChemBench typed atomic action",
        "",
        f"{charge} {multiplicity}",
    ]
    lines.extend(
        f"{symbol} {row[0]:.12f} {row[1]:.12f} {row[2]:.12f}"
        for symbol, row in zip(symbols, coordinates)
    )
    lines.extend(["", ""])
    return "\n".join(lines)


def _parse_gaussian_energy(text: str) -> float | None:
    matches = re.findall(rf"SCF Done:\s+E\([^\n=]+\)\s*=\s*({_FLOAT})", text)
    return float(matches[-1].replace("D", "E")) if matches else None


def _parse_gaussian_dipole(text: str) -> list[float] | None:
    matches = re.findall(
        rf"Dipole moment \(field-independent basis, Debye\):\s*\n\s*"
        rf"X=\s*({_FLOAT})\s+Y=\s*({_FLOAT})\s+Z=\s*({_FLOAT})",
        text,
    )
    if not matches:
        return None
    return [float(value.replace("D", "E")) for value in matches[-1]]


def _parse_gaussian_geometry(text: str, symbols: list[str]) -> dict[str, Any] | None:
    lines = text.splitlines()
    blocks: list[list[list[float]]] = []
    for index, line in enumerate(lines):
        if "Standard orientation:" not in line and "Input orientation:" not in line:
            continue
        cursor = index + 1
        separators = 0
        while cursor < len(lines):
            if set(lines[cursor].strip()) == {"-"}:
                separators += 1
                cursor += 1
                if separators == 2:
                    break
            else:
                cursor += 1
        coordinates: list[list[float]] = []
        while cursor < len(lines):
            stripped = lines[cursor].strip()
            if set(stripped) == {"-"}:
                break
            parts = stripped.split()
            if len(parts) >= 6 and parts[0].isdigit():
                try:
                    coordinates.append([float(parts[3]), float(parts[4]), float(parts[5])])
                except ValueError:
                    coordinates = []
                    break
            cursor += 1
        if len(coordinates) == len(symbols):
            blocks.append(coordinates)
    if not blocks:
        return None
    return {
        "atoms": [
            {"element": symbol, "position_angstrom": row}
            for symbol, row in zip(symbols, blocks[-1])
        ],
        "pbc": [False, False, False],
    }


def _parse_gaussian_fchk_hessian(path: Path, expected_dimension: int) -> list[list[float]] | None:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    values: list[float] = []
    count = None
    for index, line in enumerate(lines):
        if not line.startswith("Cartesian Force Constants"):
            continue
        match = re.search(r"N=\s*(\d+)", line)
        if not match:
            return None
        count = int(match.group(1))
        for following in lines[index + 1 :]:
            for token in following.split():
                try:
                    values.append(float(token.replace("D", "E")))
                except ValueError:
                    break
                if len(values) == count:
                    break
            if len(values) == count:
                break
        break
    expected_count = expected_dimension * (expected_dimension + 1) // 2
    if count != expected_count or len(values) != expected_count:
        return None
    matrix = [[0.0 for _ in range(expected_dimension)] for _ in range(expected_dimension)]
    cursor = 0
    for row in range(expected_dimension):
        for column in range(row + 1):
            matrix[row][column] = values[cursor]
            matrix[column][row] = values[cursor]
            cursor += 1
    return matrix


def gaussian(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    structure, symbols, _coordinates = _molecular_structure(inputs["structure"])
    directory = output_directory(action_id, "gaussian")
    input_path = directory / "job.gjf"
    input_path.write_text(
        _render_gaussian(
            action_id,
            structure,
            method,
            settings,
            dict(request.get("resource_limits") or {}),
        ),
        encoding="utf-8",
    )
    completed = run_external(
        executable="g16",
        environment_variable="CHEMGRAPH_GAUSSIAN_COMMAND",
        arguments=[],
        directory=directory,
        stdin_text=input_path.read_text(encoding="utf-8"),
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    output_path = directory / "job.log"
    output_path.write_text(completed["stdout"], encoding="utf-8")
    (directory / "job.err").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install="Place the licensed Gaussian 16 distribution in .software_cache/gaussian/g16.",
        )
    if completed["returncode"] != 0 or "Normal termination of Gaussian 16" not in completed["stdout"]:
        detail = (completed["stderr"] or completed["stdout"])[-4000:]
        raise RuntimeError(f"Gaussian failed or did not terminate normally: {detail}")
    version_match = re.search(r"Gaussian 16, Revision\s+([^,\s]+)", completed["stdout"])
    backend_version = f"16 {version_match.group(1)}" if version_match else "16"
    energy = _parse_gaussian_energy(completed["stdout"])
    if energy is None:
        raise RuntimeError("Could not parse Gaussian SCF/DFT energy")
    output_file = relative_workspace_path(output_path)
    if action_id == "calculate_energy":
        result = {"energy": energy, "unit": "hartree", "output_file": output_file}
    elif action_id == "calculate_dipole_moment":
        dipole = _parse_gaussian_dipole(completed["stdout"])
        if dipole is None:
            raise RuntimeError("Could not parse Gaussian dipole moment")
        result = {
            "dipole": dipole,
            "unit": "debye",
            "energy_hartree": energy,
            "output_file": output_file,
        }
    elif action_id == "optimize_geometry":
        geometry = _parse_gaussian_geometry(completed["stdout"], symbols)
        if geometry is None:
            raise RuntimeError("Could not parse Gaussian optimized geometry")
        converged = "Optimization completed." in completed["stdout"]
        result = {
            "structure": geometry,
            "converged": converged,
            "energy": energy,
            "energy_unit": "hartree",
            "output_file": output_file,
        }
        if not converged:
            return partial_success(
                result,
                artifact_files=command_artifacts(directory),
                backend_version=backend_version,
                provenance={"command": completed["command"]},
                warnings=["Gaussian ended normally, but the geometry optimization did not converge."],
            )
    elif action_id == "calculate_hessian":
        checkpoint = directory / "job.chk"
        formatted = directory / "job.fchk"
        if not checkpoint.is_file():
            raise RuntimeError("Gaussian frequency calculation produced no checkpoint")
        formchk = run_external(
            executable="formchk",
            environment_variable="CHEMGRAPH_GAUSSIAN_FORMCHK_COMMAND",
            arguments=[str(checkpoint), str(formatted)],
            directory=directory,
            timeout_seconds=min(300, int(request.get("resource_limits", {}).get("walltime_seconds", 1800))),
        )
        (directory / "formchk.stdout.log").write_text(formchk["stdout"], encoding="utf-8")
        (directory / "formchk.stderr.log").write_text(formchk["stderr"], encoding="utf-8")
        matrix = (
            _parse_gaussian_fchk_hessian(formatted, 3 * len(symbols))
            if formchk["available"] and formchk["returncode"] == 0 and formatted.is_file()
            else None
        )
        result = {
            "matrix": matrix,
            "unit": "hartree/bohr^2",
            "energy_hartree": energy,
            "raw_hessian_path": relative_workspace_path(formatted) if formatted.is_file() else None,
            "output_file": output_file,
        }
        if matrix is None:
            return partial_success(
                result,
                artifact_files=command_artifacts(directory),
                backend_version=backend_version,
                provenance={"command": completed["command"], "formchk_command": formchk["command"]},
                warnings=["Gaussian completed, but the formatted checkpoint Hessian could not be parsed."],
            )
    else:
        return unsupported(f"Gaussian does not implement {action_id}")
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=backend_version,
        provenance={"command": completed["command"]},
    )


def _gamess_token(value: Any, name: str) -> str:
    return _safe_keyword(value, name, r"[A-Za-z0-9+-]+").upper()


def _gamess_convergence(value: Any) -> int:
    tolerance = _finite_float(value, "GAMESS scf_convergence", positive=True)
    exponent = int(round(-math.log10(tolerance)))
    if exponent < 4 or exponent > 14 or not math.isclose(tolerance, 10.0 ** (-exponent), rel_tol=1e-6):
        raise ValueError("GAMESS scf_convergence must be an exact power of ten from 1e-4 to 1e-14")
    return exponent


def _render_gamess(
    action_id: str,
    structure_value: Any,
    method: dict[str, Any],
    settings: dict[str, Any],
    resource_limits: dict[str, Any] | None = None,
) -> str:
    """Render a molecular GAMESS input from explicit scientific fields."""

    structure, symbols, coordinates = _molecular_structure(structure_value)
    scftyp = _gamess_token(method["scftyp"], "GAMESS SCFTYP")
    gbasis = _gamess_token(method["gbasis"], "GAMESS GBASIS")
    ngauss = int(method["ngauss"])
    if ngauss < 1 or ngauss > 9:
        raise ValueError("GAMESS NGAUSS must be between 1 and 9")
    runtyp = "OPTIMIZE" if action_id == "optimize_geometry" else "ENERGY"
    charge = int(method.get("charge", structure.get("charge", 0)))
    multiplicity = int(method.get("multiplicity", structure.get("multiplicity", 1)))
    if multiplicity < 1:
        raise ValueError("GAMESS multiplicity must be at least one")
    control = [
        f"SCFTYP={scftyp}",
        f"RUNTYP={runtyp}",
        "COORD=UNIQUE",
        "UNITS=ANGS",
        f"ICHARG={charge}",
        f"MULT={multiplicity}",
    ]
    if method.get("dfttyp"):
        control.append(f"DFTTYP={_gamess_token(method['dfttyp'], 'GAMESS DFTTYP')}")
    limits = resource_limits or {}
    memory_mb = max(128, int(limits.get("memory_mb") or 1000))
    mwords = max(1, memory_mb // 8)
    basis = [f"GBASIS={gbasis}", f"NGAUSS={ngauss}"]
    for key in ("ndfunc", "npfunc", "nffunc"):
        if key in method:
            value = int(method[key])
            if value < 0 or value > 9:
                raise ValueError(f"GAMESS {key.upper()} must be between 0 and 9")
            basis.append(f"{key.upper()}={value}")
    for key in ("diffsp", "diffs"):
        if key in method:
            basis.append(f"{key.upper()}={'.TRUE.' if bool(method[key]) else '.FALSE.'}")
    lines = [
        " $CONTRL " + " ".join(control) + " $END",
        f" $SYSTEM MWORDS={mwords} $END",
        f" $SCF DIRSCF=.TRUE. CONV={_gamess_convergence(settings['scf_convergence'])} $END",
        " $BASIS " + " ".join(basis) + " $END",
        f" $GUESS GUESS={_gamess_token(method.get('guess', 'HUCKEL'), 'GAMESS GUESS')} $END",
    ]
    if action_id == "optimize_geometry":
        tolerance = _finite_float(settings["gradient_tolerance_hartree_per_bohr"], "GAMESS gradient tolerance", positive=True)
        max_steps = int(settings["max_steps"])
        if max_steps < 1:
            raise ValueError("GAMESS max_steps must be positive")
        lines.append(f" $STATPT OPTTOL={tolerance:.12g} NSTEP={max_steps} $END")
    lines.extend([" $DATA", "ResearchChemBench typed atomic action", "C1"])
    for symbol, row in zip(symbols, coordinates):
        atomic_number = _ATOMIC_NUMBERS.get(symbol.lower())
        if atomic_number is None:
            raise ValueError(f"Unknown element for GAMESS: {symbol}")
        lines.append(
            f"{symbol} {float(atomic_number):.1f} {row[0]:.12f} {row[1]:.12f} {row[2]:.12f}"
        )
    lines.extend([" $END", ""])
    return "\n".join(lines)


def _parse_gamess_energy(text: str) -> float | None:
    matches = re.findall(rf"FINAL\s+[A-Z0-9()+-]+\s+ENERGY IS\s+({_FLOAT})", text)
    return float(matches[-1].replace("D", "E")) if matches else None


def _parse_gamess_dipole(text: str) -> list[float] | None:
    matches = re.findall(
        rf"DX\s+DY\s+DZ\s+/D/\s+\(DEBYE\)\s*\n\s*({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})",
        text,
    )
    if not matches:
        return None
    return [float(value.replace("D", "E")) for value in matches[-1]]


def _parse_gamess_geometry(text: str) -> dict[str, Any] | None:
    lines = text.splitlines()
    blocks: list[list[dict[str, Any]]] = []
    row_pattern = re.compile(
        rf"^\s*([A-Za-z][A-Za-z]?)\s+{_FLOAT}\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$"
    )
    for index, line in enumerate(lines):
        if "COORDINATES OF ALL ATOMS ARE (ANGS)" not in line:
            continue
        cursor = index + 1
        while cursor < len(lines) and set(lines[cursor].strip()) != {"-"}:
            cursor += 1
        cursor += 1
        atoms: list[dict[str, Any]] = []
        while cursor < len(lines):
            match = row_pattern.match(lines[cursor])
            if not match:
                break
            atoms.append(
                {
                    "element": match.group(1).title(),
                    "position_angstrom": [
                        float(match.group(2).replace("D", "E")),
                        float(match.group(3).replace("D", "E")),
                        float(match.group(4).replace("D", "E")),
                    ],
                }
            )
            cursor += 1
        if atoms:
            blocks.append(atoms)
    if not blocks:
        return None
    return {"atoms": blocks[-1], "pbc": [False, False, False]}


def gamess(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    directory = output_directory(action_id, "gamess")
    job_name = f"rchem_{directory.name}"
    input_path = directory / f"{job_name}.inp"
    input_path.write_text(
        _render_gamess(
            action_id,
            inputs["structure"],
            method,
            settings,
            dict(request.get("resource_limits") or {}),
        ),
        encoding="utf-8",
    )
    cores = max(1, int(request.get("resource_limits", {}).get("cpu_cores") or 1))
    completed = run_external(
        executable="rungms",
        environment_variable="CHEMGRAPH_GAMESS_COMMAND",
        arguments=[job_name, "00", str(cores), str(cores)],
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    output_path = directory / f"{job_name}.log"
    output_path.write_text(completed["stdout"], encoding="utf-8")
    (directory / f"{job_name}.err").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install="Build the registered GAMESS distribution under .software_cache/gamess.",
        )
    if completed["returncode"] != 0 or "EXECUTION OF GAMESS TERMINATED NORMALLY" not in completed["stdout"]:
        detail = (completed["stderr"] or completed["stdout"])[-4000:]
        raise RuntimeError(f"GAMESS failed or did not terminate normally: {detail}")
    version_match = re.search(r"GAMESS VERSION\s*=\s*([^*\n]+)", completed["stdout"])
    backend_version = version_match.group(1).strip() if version_match else None
    energy = _parse_gamess_energy(completed["stdout"])
    if energy is None:
        raise RuntimeError("Could not parse GAMESS final energy")
    output_file = relative_workspace_path(output_path)
    if action_id == "calculate_energy":
        result = {"energy": energy, "unit": "hartree", "output_file": output_file}
    elif action_id == "calculate_dipole_moment":
        dipole = _parse_gamess_dipole(completed["stdout"])
        if dipole is None:
            raise RuntimeError("Could not parse GAMESS dipole moment")
        result = {
            "dipole": dipole,
            "unit": "debye",
            "energy_hartree": energy,
            "output_file": output_file,
        }
    elif action_id == "optimize_geometry":
        geometry = _parse_gamess_geometry(completed["stdout"])
        if geometry is None:
            raise RuntimeError("Could not parse GAMESS final geometry")
        converged = "EQUILIBRIUM GEOMETRY LOCATED" in completed["stdout"]
        result = {
            "structure": geometry,
            "converged": converged,
            "energy": energy,
            "energy_unit": "hartree",
            "output_file": output_file,
        }
        if not converged:
            return partial_success(
                result,
                artifact_files=command_artifacts(directory),
                backend_version=backend_version,
                provenance={"command": completed["command"], "parallel_processes": cores},
                warnings=["GAMESS ended normally, but the geometry optimization did not converge."],
            )
    else:
        return unsupported(f"GAMESS does not implement {action_id}")
    return success(
        result,
        artifact_files=command_artifacts(directory),
        backend_version=backend_version,
        provenance={"command": completed["command"], "parallel_processes": cores},
    )

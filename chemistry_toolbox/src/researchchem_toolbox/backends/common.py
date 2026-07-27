"""Shared backend implementation helpers with workspace confinement."""

from __future__ import annotations

import importlib.metadata
import json
import math
import os
import re
import signal
import shlex
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any

from ..artifacts import ArtifactStore, relative_workspace_path, resolve_workspace_path, workspace_root
from ..resources import is_resource_reference, resolve_resource_reference


def success(
    result: Any,
    *,
    artifact_files: list[dict[str, str]] | None = None,
    backend_version: str | None = None,
    warnings: list[str] | None = None,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "status": "success",
        "result": result,
        "artifact_files": artifact_files or [],
        "backend_version": backend_version,
        "warnings": warnings or [],
        "provenance": provenance or {},
        "retryable": False,
    }


def partial_success(
    result: Any,
    *,
    artifact_files: list[dict[str, str]] | None = None,
    backend_version: str | None = None,
    warnings: list[str] | None = None,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return completed backend output whose primary scientific result is incomplete.

    This status is deliberately distinct from ``success``: raw logs or a partially
    parsed result must never masquerade as a complete Action result.
    """

    return {
        "status": "partial_success",
        "result": result,
        "artifact_files": artifact_files or [],
        "backend_version": backend_version,
        "warnings": warnings or [],
        "provenance": provenance or {},
        "retryable": False,
    }


def unavailable(message: str, *, install: str = "") -> dict[str, Any]:
    error = {"code": "backend_unavailable", "message": message}
    if install:
        error["install"] = install
    return {"status": "unavailable", "error": error, "retryable": False}


def unsupported(message: str) -> dict[str, Any]:
    return {
        "status": "unsupported",
        "error": {"code": "unsupported_request", "message": message},
        "retryable": False,
    }


def failed(message: str, *, code: str = "backend_failed", retryable: bool = False) -> dict[str, Any]:
    return {
        "status": "failed",
        "error": {"code": code, "message": message},
        "retryable": retryable,
    }


def module_version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def request_parts(request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        dict(request.get("inputs") or {}),
        dict(request.get("method_spec") or {}),
        dict(request.get("action_settings") or {}),
    )


def unwrap_artifact(value: Any) -> Any:
    if isinstance(value, dict) and "artifact_id" in value:
        return ArtifactStore().load(value)
    if isinstance(value, str) and value.startswith("art_"):
        return ArtifactStore().load(value)
    return value


def resolve_input_file(value: Any) -> Path:
    item = unwrap_artifact(value)
    if is_resource_reference(item):
        return resolve_resource_reference(item)
    if isinstance(item, dict) and isinstance(item.get("path"), str):
        return resolve_workspace_path(item["path"], must_exist=True)
    if isinstance(item, dict) and isinstance(item.get("file_path"), str):
        return resolve_workspace_path(item["file_path"], must_exist=True)
    if isinstance(item, str):
        return resolve_workspace_path(item, must_exist=True)
    raise ValueError(
        "Expected a workspace file path, file ArtifactRef, or explicit registered ResourceRef"
    )


def output_directory(action_id: str, backend_id: str) -> Path:
    directory = workspace_root() / "outputs" / action_id / backend_id / uuid.uuid4().hex[:12]
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def write_json(directory: Path, name: str, value: Any) -> Path:
    path = directory / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    return path


def _parse_xyz(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError(f"Empty XYZ file: {path}")
    try:
        count = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError(f"Invalid XYZ atom count: {path}") from exc
    atoms = []
    for line in lines[2 : 2 + count]:
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid XYZ atom line: {line!r}")
        atoms.append(
            {
                "element": parts[0],
                "position_angstrom": [float(parts[1]), float(parts[2]), float(parts[3])],
            }
        )
    if len(atoms) != count:
        raise ValueError(f"XYZ atom count mismatch: {path}")
    comment = lines[1] if len(lines) > 1 else ""
    charge_match = re.search(r"(?:^|\s)charge=(-?\d+)(?:\s|$)", comment)
    multiplicity_match = re.search(
        r"(?:^|\s)multiplicity=(\d+)(?:\s|$)", comment
    )
    return {
        "atoms": atoms,
        "charge": int(charge_match.group(1)) if charge_match else 0,
        "multiplicity": int(multiplicity_match.group(1)) if multiplicity_match else 1,
        "pbc": [False, False, False],
        "source_path": relative_workspace_path(path),
    }


def _parse_pdb(path: Path) -> dict[str, Any]:
    atoms = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        element = line[76:78].strip()
        if not element:
            element = "".join(character for character in line[12:16].strip() if character.isalpha())[:2].title()
        atoms.append(
            {
                "element": element,
                "position_angstrom": [
                    float(line[30:38]),
                    float(line[38:46]),
                    float(line[46:54]),
                ],
            }
        )
    if not atoms:
        raise ValueError(f"PDB contains no ATOM/HETATM coordinates: {path}")
    return {
        "atoms": atoms,
        "charge": 0,
        "multiplicity": 1,
        "pbc": [False, False, False],
        "source_path": relative_workspace_path(path),
    }


def _parse_sdf(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) < 4:
        raise ValueError(f"Invalid SDF/MOL file: {path}")
    try:
        atom_count = int(lines[3][:3])
    except ValueError as exc:
        raise ValueError(f"Unsupported non-V2000 SDF/MOL file: {path}") from exc
    atoms = []
    for line in lines[4 : 4 + atom_count]:
        atoms.append(
            {
                "element": line[31:34].strip(),
                "position_angstrom": [float(line[0:10]), float(line[10:20]), float(line[20:30])],
            }
        )
    return {
        "atoms": atoms,
        "charge": 0,
        "multiplicity": 1,
        "pbc": [False, False, False],
        "source_path": relative_workspace_path(path),
    }


def _parse_vasp_structure(path: Path) -> dict[str, Any]:
    from pymatgen.io.vasp.inputs import Poscar

    structure = Poscar.from_file(path, check_for_potcar=False).structure
    return {
        "atoms": [
            {
                "element": str(site.specie.symbol),
                "position_angstrom": [float(value) for value in site.coords],
            }
            for site in structure
        ],
        "cell_angstrom": [
            [float(value) for value in row] for row in structure.lattice.matrix
        ],
        "charge": 0,
        "multiplicity": 1,
        "pbc": [True, True, True],
        "source_path": relative_workspace_path(path),
    }


def structure_dict(value: Any) -> dict[str, Any]:
    item = unwrap_artifact(value)
    if isinstance(item, dict) and "result" in item and isinstance(item["result"], dict):
        item = item["result"]
    if isinstance(item, dict) and "structure" in item and isinstance(item["structure"], dict):
        item = item["structure"]
    if isinstance(item, dict):
        if "atoms" in item or "symbols" in item or "smiles" in item:
            return dict(item)
        if isinstance(item.get("path"), str):
            return structure_dict(item["path"])
    if isinstance(item, str):
        candidate = resolve_workspace_path(item, must_exist=False)
        if candidate.is_file():
            if candidate.suffix.lower() == ".xyz":
                return _parse_xyz(candidate)
            if candidate.suffix.lower() == ".pdb":
                return _parse_pdb(candidate)
            if candidate.suffix.lower() in {".sdf", ".mol"}:
                return _parse_sdf(candidate)
            if candidate.suffix.lower() in {".vasp", ".poscar"} or candidate.name.upper() in {
                "POSCAR",
                "CONTCAR",
            }:
                try:
                    return _parse_vasp_structure(candidate)
                except Exception as exc:
                    raise ValueError(
                        f"Could not parse VASP structure file {candidate}: {exc}"
                    ) from exc
            try:
                from ase.io import read

                return structure_from_atoms(read(str(candidate)))
            except Exception as exc:
                raise ValueError(f"Could not parse structure file {candidate}: {exc}") from exc
        return {"smiles": item}
    raise ValueError("Unsupported structure representation")


def atoms_and_coordinates(structure: dict[str, Any]) -> tuple[list[str], list[list[float]]]:
    if "atoms" in structure:
        atoms = structure["atoms"]
        if not isinstance(atoms, list) or not atoms:
            raise ValueError("AtomicStructure.atoms must be a non-empty array of atom mappings")
        symbols = []
        coordinates = []
        for index, atom in enumerate(atoms):
            if not isinstance(atom, dict):
                raise ValueError(f"AtomicStructure.atoms[{index}] must be a mapping")
            symbol = atom.get("element") or atom.get("symbol")
            if not symbol:
                raise ValueError(
                    f"AtomicStructure.atoms[{index}] requires an element field"
                )
            position = atom.get("position_angstrom")
            if position is None:
                position = atom.get("position")
            if position is None:
                suffix = "; the key 'xyz' is not part of AtomicStructure" if "xyz" in atom else ""
                raise ValueError(
                    f"AtomicStructure.atoms[{index}] requires position_angstrom=[x, y, z]"
                    f"{suffix}"
                )
            try:
                row = [float(value) for value in position]
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"AtomicStructure.atoms[{index}].position_angstrom must contain three numbers"
                ) from exc
            symbols.append(str(symbol))
            coordinates.append(row)
    else:
        symbols = [str(value) for value in structure.get("symbols", [])]
        coordinates = [
            [float(value) for value in row]
            for row in (
                structure.get("coordinates_angstrom")
                or structure.get("positions_angstrom")
                or structure.get("positions")
                or []
            )
        ]
    if not symbols or len(symbols) != len(coordinates):
        raise ValueError("Structure must contain aligned symbols and coordinates")
    if any(len(row) != 3 or not all(math.isfinite(value) for value in row) for row in coordinates):
        raise ValueError("All coordinates must contain three finite Angstrom values")
    return symbols, coordinates


def ase_atoms(value: Any):
    from ase import Atoms

    structure = structure_dict(value)
    if "smiles" in structure and len(structure) == 1:
        raise ValueError("A 3D AtomicStructure is required; SMILES alone is insufficient")
    symbols, coordinates = atoms_and_coordinates(structure)
    atoms = Atoms(symbols=symbols, positions=coordinates)
    cell = structure.get("cell_angstrom") or structure.get("cell")
    if cell is not None:
        atoms.set_cell(cell)
    pbc = structure.get("pbc", [False, False, False])
    atoms.set_pbc(pbc)
    atoms.info["charge"] = int(structure.get("charge", 0))
    atoms.info["multiplicity"] = int(structure.get("multiplicity", 1))
    return atoms


def structure_from_atoms(atoms) -> dict[str, Any]:
    return {
        "atoms": [
            {
                "element": symbol,
                "position_angstrom": [float(value) for value in position],
            }
            for symbol, position in zip(atoms.get_chemical_symbols(), atoms.get_positions())
        ],
        "cell_angstrom": [[float(value) for value in row] for row in atoms.cell.array],
        "pbc": [bool(value) for value in atoms.pbc],
        "charge": int(atoms.info.get("charge", 0)),
        "multiplicity": int(atoms.info.get("multiplicity", 1)),
    }


def write_xyz(structure_value: Any, path: Path) -> Path:
    structure = structure_dict(structure_value)
    symbols, coordinates = atoms_and_coordinates(structure)
    charge = int(structure.get("charge", 0))
    multiplicity = int(structure.get("multiplicity", 1))
    lines = [
        str(len(symbols)),
        (
            "generated by ResearchChemBench "
            f"charge={charge} multiplicity={multiplicity}"
        ),
    ]
    lines.extend(
        f"{symbol} {row[0]:.12f} {row[1]:.12f} {row[2]:.12f}"
        for symbol, row in zip(symbols, coordinates)
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def atom_spec(structure_value: Any) -> str:
    structure = structure_dict(structure_value)
    symbols, coordinates = atoms_and_coordinates(structure)
    return "; ".join(
        f"{symbol} {row[0]:.12f} {row[1]:.12f} {row[2]:.12f}"
        for symbol, row in zip(symbols, coordinates)
    )


def resolve_command(executable: str, environment_variable: str | None = None) -> list[str] | None:
    configured = os.environ.get(environment_variable or "", "").strip()
    if configured:
        command = shlex.split(configured)
        if command and (Path(command[0]).expanduser().is_file() or shutil.which(command[0])):
            return command
    path = shutil.which(executable)
    return [path] if path else None


def run_external(
    *,
    executable: str,
    arguments: list[str],
    directory: Path,
    environment_variable: str | None = None,
    stdin_text: str | None = None,
    timeout_seconds: int = 1800,
    environment_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    command = resolve_command(executable, environment_variable)
    if command is None:
        return {
            "available": False,
            "returncode": None,
            "stdout": "",
            "stderr": f"Executable {executable!r} was not found",
            "command": [executable, *arguments],
        }
    environment = os.environ.copy()
    environment.update(environment_overrides or {})
    process = subprocess.Popen(
        [*command, *arguments],
        cwd=directory,
        stdin=subprocess.PIPE if stdin_text is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
        # Scientific launchers frequently spawn worker processes.  Give every
        # call its own process group so a timeout cannot leave an unobserved
        # ORCA/orca_plot child consuming resources and writing late artifacts.
        start_new_session=os.name == "posix",
    )
    try:
        stdout, stderr = process.communicate(stdin_text, timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        else:
            process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            stdout, stderr = process.communicate()
        return {
            "available": True,
            "returncode": 124,
            "stdout": stdout or "",
            "stderr": stderr or "",
            "command": [Path(command[0]).name, *command[1:], *arguments],
            "timeout": True,
        }
    return {
        "available": True,
        "returncode": process.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "command": [Path(command[0]).name, *command[1:], *arguments],
    }


def command_artifacts(directory: Path) -> list[dict[str, str]]:
    artifacts = []
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            artifacts.append(
                {
                    "path": relative_workspace_path(path),
                    "semantic_type": "BackendFile",
                    "media_type": "text/plain" if path.suffix.lower() in {".txt", ".log", ".out", ".xyz", ".pdb", ".inp"} else "application/octet-stream",
                }
            )
    return artifacts

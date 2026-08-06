"""Structure, conformer, charge, and simulation-system actions."""

from __future__ import annotations

import itertools
import math
import os
import re
import shutil
from pathlib import Path
from typing import Any

from .common import (
    ase_atoms,
    command_artifacts,
    module_version,
    output_directory,
    relative_workspace_path,
    request_parts,
    resolve_input_file,
    run_external,
    structure_dict,
    success,
    unavailable,
    unwrap_artifact,
    unsupported,
    write_json,
    write_xyz,
)


ACTIONS = {
    "standardize_structure", "generate_3d_structure", "generate_conformer_ensemble",
    "cluster_conformers", "align_molecular_structures",
    "rank_conformers_from_results", "repair_biomolecular_structure",
    "assign_protonation_states", "assign_partial_charges",
    "assign_force_field_parameters", "solvate_molecular_system",
    "generate_small_molecule_topology", "convert_amber_topology_to_gromacs",
    "mutate_biomolecular_residues_for_alchemy", "generate_alchemical_hybrid_topology",
    "map_alchemical_ligand_atoms",
    "analyze_crystal_symmetry", "standardize_crystal_structure",
    "build_supercell", "enumerate_surface_slabs",
    "select_structure_subset", "renumber_biomolecular_structure",
    "normalize_pdb_records",
    "enumerate_coordination_isomers",
}


_ELEMENTS = (
    "X H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn "
    "Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr "
    "Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra "
    "Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og"
).split()
_ATOMIC_NUMBER = {symbol: index for index, symbol in enumerate(_ELEMENTS) if index}


def _crystal_arrays(value: Any):
    import numpy as np

    structure = structure_dict(value)
    atoms = structure.get("atoms") or []
    if not atoms:
        raise ValueError("Crystal actions require atoms with Cartesian coordinates")
    symbols = [str(atom["element"]) for atom in atoms]
    coordinates = np.asarray([atom["position_angstrom"] for atom in atoms], dtype=float)
    lattice = np.asarray(structure.get("cell_angstrom") or structure.get("cell"), dtype=float)
    if lattice.shape != (3, 3):
        raise ValueError("Crystal actions require a 3x3 cell_angstrom")
    if not all(bool(value) for value in structure.get("pbc", [True, True, True])):
        raise ValueError("Crystal actions require periodic boundary conditions in all dimensions")
    scaled = coordinates @ np.linalg.inv(lattice)
    try:
        numbers = [int(_ATOMIC_NUMBER[symbol]) for symbol in symbols]
    except KeyError as exc:
        raise ValueError(f"Unknown element symbol in crystal structure: {exc.args[0]}") from exc
    return structure, symbols, coordinates, lattice, scaled, numbers


def _crystal_payload(symbols, coordinates, lattice, original: dict[str, Any]) -> dict[str, Any]:
    return {
        "atoms": [
            {"element": str(symbol), "position_angstrom": [float(value) for value in row]}
            for symbol, row in zip(symbols, coordinates)
        ],
        "cell_angstrom": [[float(value) for value in row] for row in lattice],
        "pbc": [True, True, True],
        "charge": int(original.get("charge", 0)),
        "multiplicity": int(original.get("multiplicity", 1)),
    }


def _pymatgen_structure(value: Any):
    from pymatgen.core import Structure

    original, symbols, coordinates, lattice, _scaled, _numbers = _crystal_arrays(value)
    return original, Structure(lattice, symbols, coordinates, coords_are_cartesian=True)


def _pymatgen_payload(structure, original: dict[str, Any]) -> dict[str, Any]:
    symbols = [str(site.specie.symbol) for site in structure]
    return _crystal_payload(symbols, structure.cart_coords.tolist(), structure.lattice.matrix.tolist(), original)


def _analyze_crystal_symmetry(backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, _method, settings = request_parts(request)
    symprec = float(settings["symmetry_tolerance_angstrom"])
    angle = float(settings["angle_tolerance_degrees"])
    if symprec <= 0:
        raise ValueError("symmetry_tolerance_angstrom must be positive")
    if backend_id == "spglib":
        import spglib

        _original, _symbols, _coordinates, lattice, scaled, numbers = _crystal_arrays(inputs["structure"])
        dataset = spglib.get_symmetry_dataset(
            (lattice, scaled, numbers), symprec=symprec, angle_tolerance=angle
        )
        if dataset is None:
            raise RuntimeError("spglib could not determine a symmetry dataset")
        result = {
            "space_group_number": int(dataset.number),
            "international_symbol": str(dataset.international),
            "hall_symbol": str(dataset.hall),
            "hall_number": int(dataset.hall_number),
            "point_group": str(dataset.pointgroup),
            "choice": str(dataset.choice),
            "wyckoff_letters": [str(value) for value in dataset.wyckoffs],
            "equivalent_atom_indices": np.asarray(dataset.equivalent_atoms, dtype=int).tolist(),
            "transformation_matrix": np.asarray(dataset.transformation_matrix, dtype=float).tolist(),
            "origin_shift": np.asarray(dataset.origin_shift, dtype=float).tolist(),
            "symmetry_tolerance_angstrom": symprec,
            "angle_tolerance_degrees": angle,
        }
        return success(result, backend_version=module_version("spglib"))

    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

    _original, structure = _pymatgen_structure(inputs["structure"])
    analyzer = SpacegroupAnalyzer(structure, symprec=symprec, angle_tolerance=angle)
    symmetrized = analyzer.get_symmetrized_structure()
    result = {
        "space_group_number": int(analyzer.get_space_group_number()),
        "international_symbol": str(analyzer.get_space_group_symbol()),
        "hall_symbol": str(analyzer.get_hall()),
        "point_group": str(analyzer.get_point_group_symbol()),
        "crystal_system": str(analyzer.get_crystal_system()),
        "lattice_type": str(analyzer.get_lattice_type()),
        "equivalent_atom_groups": [list(map(int, indices)) for indices in symmetrized.equivalent_indices],
        "wyckoff_symbols": [str(value) for value in symmetrized.wyckoff_symbols],
        "symmetry_tolerance_angstrom": symprec,
        "angle_tolerance_degrees": angle,
    }
    return success(result, backend_version=module_version("pymatgen"))


def _analyze_vaspkit_symmetry(request: dict[str, Any]) -> dict[str, Any]:
    from ase.io import write

    inputs, _method, settings = request_parts(request)
    symprec = float(settings["symmetry_tolerance_angstrom"])
    angle = float(settings["angle_tolerance_degrees"])
    if symprec <= 0 or angle <= 0:
        raise ValueError("VASPKIT symmetry and angle tolerances must be positive")
    configured = os.environ.get("CHEMGRAPH_VASPKIT_CONFIG", "").strip()
    if not configured or not Path(configured).is_file():
        raise RuntimeError("CHEMGRAPH_VASPKIT_CONFIG must point to the pinned VASPKIT configuration template")
    directory = output_directory("analyze_crystal_symmetry", "vaspkit")
    write(directory / "POSCAR", ase_atoms(inputs["structure"]), format="vasp", direct=True, vasp5=True)
    home = directory / "home"
    home.mkdir()
    config = Path(configured).read_text(encoding="utf-8", errors="strict")
    replacements = {"SYMMETRY_TOLERANCE": format(symprec, ".17g"), "ANGLE_TOLERANCE": format(angle, ".17g")}
    for name, value in replacements.items():
        config, count = re.subn(
            rf"(?m)^({re.escape(name)}\s*=\s*)[^#\n]+", rf"\g<1>{value} ", config, count=1
        )
        if count != 1:
            raise RuntimeError(f"VASPKIT configuration does not define {name}")
    (home / ".vaspkit").write_text(config, encoding="utf-8")
    timeout = int((request.get("resource_limits") or {}).get("walltime_seconds", 1800))
    results = []
    for task in (601, 604):
        completed = run_external(
            executable="vaspkit", environment_variable="CHEMGRAPH_VASPKIT_COMMAND",
            arguments=["-task", str(task), "-file", "POSCAR", "-symprec", str(symprec)],
            directory=directory, timeout_seconds=max(1, timeout),
            environment_overrides={"HOME": str(home)},
        )
        (directory / f"vaspkit-{task}.log").write_text(
            completed["stdout"] + completed["stderr"], encoding="utf-8"
        )
        if not completed["available"]:
            return unavailable(completed["stderr"], install="Download VASPKIT 1.5.1 from the official SourceForge release.")
        if completed["returncode"] != 0 or "Space Group Number" not in completed["stdout"]:
            raise RuntimeError(f"VASPKIT symmetry task {task} failed: {(completed['stderr'] or completed['stdout'])[-2000:]}")
        results.append(completed)
    summary, equivalents = results[0]["stdout"], results[1]["stdout"]
    def value(pattern: str, label: str) -> str:
        matched = re.search(pattern, summary)
        if matched is None:
            raise RuntimeError(f"Could not parse {label} from VASPKIT symmetry output")
        return matched.group(1).strip()
    atom_rows = re.findall(r"\|\s+([A-Za-z]{1,3})\s+\|\s+(\d+)\s+\|\s+(\d+)\s+\|", equivalents)
    if not atom_rows:
        raise RuntimeError("Could not parse equivalent atoms from VASPKIT task 604")
    grouped: dict[int, list[int]] = {}
    for _symbol, atom_id, representative_id in atom_rows:
        grouped.setdefault(int(representative_id) - 1, []).append(int(atom_id) - 1)
    result = {
        "space_group_number": int(value(r"Space Group Number:\s+(\d+)", "space group number")),
        "international_symbol": value(r"International:\s+(\S+)", "international symbol"),
        "point_group": value(r"Point Group:\s+\d+\s+\[\s*([^\]]+)\]", "point group"),
        "crystal_system": value(r"Crystal System:\s+(\S+)", "crystal system").lower(),
        "bravais_lattice": value(r"Bravais Lattice:\s+(\S+)", "Bravais lattice"),
        "equivalent_atom_groups": list(grouped.values()),
        "representative_atom_indices": list(grouped),
        "symmetry_operation_count": int(value(r"Symmetry Operations:\s+(\d+)", "symmetry operations")),
        "symmetry_tolerance_angstrom": symprec,
        "angle_tolerance_degrees": angle,
    }
    return success(
        result, artifact_files=command_artifacts(directory), backend_version="1.5.1",
        provenance={"commands": [item["command"] for item in results], "tasks": [601, 604]},
    )


def _standardize_crystal(backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, _method, settings = request_parts(request)
    convention = str(settings["convention"]).strip().lower()
    if convention not in {"primitive", "conventional"}:
        raise ValueError("convention must be primitive or conventional")
    symprec = float(settings["symmetry_tolerance_angstrom"])
    angle = float(settings["angle_tolerance_degrees"])
    if backend_id == "spglib":
        import spglib

        original, _symbols, _coordinates, lattice, scaled, numbers = _crystal_arrays(inputs["structure"])
        standardized = spglib.standardize_cell(
            (lattice, scaled, numbers),
            to_primitive=convention == "primitive",
            no_idealize=not bool(settings["idealize"]),
            symprec=symprec,
            angle_tolerance=angle,
        )
        if standardized is None:
            raise RuntimeError("spglib could not standardize the supplied structure")
        new_lattice, new_scaled, new_numbers = standardized
        coordinates = np.asarray(new_scaled, dtype=float) @ np.asarray(new_lattice, dtype=float)
        symbols = [_ELEMENTS[int(number)] for number in new_numbers]
        result = {
            "structure": _crystal_payload(symbols, coordinates, new_lattice, original),
            "convention": convention,
            "idealized": bool(settings["idealize"]),
        }
        return success(result, backend_version=module_version("spglib"))

    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

    original, structure = _pymatgen_structure(inputs["structure"])
    analyzer = SpacegroupAnalyzer(structure, symprec=symprec, angle_tolerance=angle)
    standardized = (
        analyzer.get_primitive_standard_structure()
        if convention == "primitive"
        else analyzer.get_conventional_standard_structure()
    )
    result = {"structure": _pymatgen_payload(standardized, original), "convention": convention}
    return success(result, backend_version=module_version("pymatgen"))


def _build_supercell(request: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    inputs, _method, settings = request_parts(request)
    original, structure = _pymatgen_structure(inputs["structure"])
    matrix = np.asarray(settings["scaling_matrix"], dtype=int)
    if matrix.shape == (3,):
        matrix = np.diag(matrix)
    if matrix.shape != (3, 3) or round(float(np.linalg.det(matrix))) == 0:
        raise ValueError("scaling_matrix must be a nonsingular integer 3-vector or 3x3 matrix")
    result_structure = structure.copy()
    result_structure.make_supercell(matrix)
    return success(
        {
            "structure": _pymatgen_payload(result_structure, original),
            "scaling_matrix": matrix.tolist(),
            "atom_count": len(result_structure),
        },
        backend_version=module_version("pymatgen"),
    )


def _enumerate_surface_slabs(request: dict[str, Any]) -> dict[str, Any]:
    from pymatgen.core.surface import SlabGenerator

    inputs, _method, settings = request_parts(request)
    original, structure = _pymatgen_structure(inputs["structure"])
    miller = tuple(int(value) for value in settings["miller_index"])
    if len(miller) != 3 or miller == (0, 0, 0):
        raise ValueError("miller_index must contain three integers and cannot be [0,0,0]")
    maximum = int(settings["max_terminations"])
    if maximum < 1 or maximum > 128:
        raise ValueError("max_terminations must be between 1 and 128")
    generator = SlabGenerator(
        structure,
        miller,
        min_slab_size=float(settings["minimum_slab_thickness_angstrom"]),
        min_vacuum_size=float(settings["minimum_vacuum_thickness_angstrom"]),
        center_slab=bool(settings["center_slab"]),
        primitive=bool(settings["primitive"]),
    )
    all_slabs = generator.get_slabs(symmetrize=bool(settings.get("symmetrize", False)))
    selected = all_slabs[:maximum]
    result = {
        "structures": [
            {
                "termination_index": index,
                "shift": float(getattr(slab, "shift", 0.0)),
                "structure": _pymatgen_payload(slab, original),
            }
            for index, slab in enumerate(selected)
        ],
        "miller_index": list(miller),
        "termination_count": len(selected),
        "available_termination_count": len(all_slabs),
        "truncated": len(all_slabs) > len(selected),
    }
    return success(result, backend_version=module_version("pymatgen"))


def _rdkit_molecule(value: Any, *, add_hydrogens: bool = False):
    from rdkit import Chem

    item = structure_dict(value)
    molecule = None
    if item.get("smiles"):
        molecule = Chem.MolFromSmiles(str(item["smiles"]))
    elif item.get("source_path"):
        path = resolve_input_file(item["source_path"])
        suffix = path.suffix.lower()
        if suffix in {".sdf", ".mol"}:
            molecule = Chem.MolFromMolFile(str(path), removeHs=False)
        elif suffix == ".pdb":
            molecule = Chem.MolFromPDBFile(str(path), removeHs=False)
    elif item.get("path"):
        return _rdkit_molecule(item["path"], add_hydrogens=add_hydrogens)
    if molecule is None:
        raise ValueError("RDKit actions require SMILES, SDF/MOL, or PDB with bond information")
    return Chem.AddHs(molecule) if add_hydrogens else molecule


def _rdkit_structure(molecule, conformer_id: int = -1) -> dict[str, Any]:
    from rdkit import Chem

    conformer = molecule.GetConformer(conformer_id) if molecule.GetNumConformers() else None
    atoms = []
    for index, atom in enumerate(molecule.GetAtoms()):
        record: dict[str, Any] = {"element": atom.GetSymbol()}
        if conformer is not None:
            position = conformer.GetAtomPosition(index)
            record["position_angstrom"] = [float(position.x), float(position.y), float(position.z)]
        if atom.HasProp("_GasteigerCharge"):
            record["partial_charge_e"] = float(atom.GetProp("_GasteigerCharge"))
        atoms.append(record)
    return {
        "smiles": Chem.MolToSmiles(Chem.RemoveHs(molecule), canonical=True),
        "atoms": atoms,
        "charge": int(Chem.GetFormalCharge(molecule)),
        "multiplicity": 1,
        "pbc": [False, False, False],
    }


def _rdkit_coordinate_molecule(value: Any):
    """Build an RDKit molecule while preserving explicitly supplied atom coordinates."""

    from rdkit import Chem
    from rdkit.Geometry import Point3D

    item = structure_dict(value)
    atoms = item.get("atoms") or []
    if not atoms or any("position_angstrom" not in atom for atom in atoms):
        raise ValueError("RDKit alignment and clustering require 3D coordinates for every atom")
    molecule = _rdkit_molecule(item)
    if molecule.GetNumAtoms() != len(atoms):
        hydrogenated = Chem.AddHs(molecule)
        if hydrogenated.GetNumAtoms() == len(atoms):
            molecule = hydrogenated
        else:
            raise ValueError(
                "Coordinate atom count does not match the molecule graph, with or without explicit hydrogens"
            )
    expected = [atom.GetSymbol() for atom in molecule.GetAtoms()]
    supplied = [str(atom["element"]) for atom in atoms]
    if expected != supplied:
        raise ValueError(
            "Coordinate atom order/elements must match the molecule graph exactly; supply an SDF if atom order is ambiguous"
        )
    conformer = Chem.Conformer(len(atoms))
    for index, atom in enumerate(atoms):
        x, y, z = (float(coordinate) for coordinate in atom["position_angstrom"])
        if not all(math.isfinite(coordinate) for coordinate in (x, y, z)):
            raise ValueError("Molecular coordinates must be finite")
        conformer.SetAtomPosition(index, Point3D(x, y, z))
    molecule.RemoveAllConformers()
    molecule.AddConformer(conformer, assignId=True)
    return molecule


def _conformer_records(value: Any) -> list[dict[str, Any]]:
    item = unwrap_artifact(value)
    records = item.get("ensemble") or item.get("conformers") if isinstance(item, dict) else item
    if not isinstance(records, list) or not records:
        raise ValueError("ensemble must contain a non-empty conformer list")
    normalized = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError("Each conformer record must be an object")
        normalized.append(
            {
                "conformer_id": str(record.get("conformer_id", index)),
                "structure": record.get("structure", record),
            }
        )
    return normalized


def _conformer_file_molecules(path: Path) -> list[tuple[str, Any]]:
    """Load every conformer from a managed SDF/MOL or multi-XYZ artifact."""

    from rdkit import Chem

    suffix = path.suffix.casefold()
    if suffix in {".sdf", ".mol"}:
        supplier = Chem.SDMolSupplier(str(path), removeHs=False)
        molecules = [molecule for molecule in supplier if molecule is not None]
        if not molecules:
            raise ValueError(f"Conformer file contains no readable molecules: {path}")
        return [
            (
                molecule.GetProp("_Name") if molecule.HasProp("_Name") else str(index),
                molecule,
            )
            for index, molecule in enumerate(molecules)
        ]
    if suffix != ".xyz":
        raise ValueError("Conformer file must be SDF, MOL, or multi-XYZ")

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    molecules = []
    offset = 0
    while offset < len(lines):
        if not lines[offset].strip():
            offset += 1
            continue
        try:
            atom_count = int(lines[offset].strip())
        except ValueError as exc:
            raise ValueError(f"Invalid multi-XYZ atom count at line {offset + 1}: {path}") from exc
        end = offset + atom_count + 2
        if end > len(lines):
            raise ValueError(f"Truncated multi-XYZ conformer at line {offset + 1}: {path}")
        block = "\n".join(lines[offset:end]) + "\n"
        molecule = Chem.MolFromXYZBlock(block)
        if molecule is None:
            raise ValueError(f"RDKit could not parse multi-XYZ conformer {len(molecules)}: {path}")
        molecules.append((str(len(molecules)), molecule))
        offset = end
    if not molecules:
        raise ValueError(f"Conformer file contains no XYZ blocks: {path}")
    return molecules


def _conformer_molecules(value: Any) -> list[tuple[str, Any]]:
    item = unwrap_artifact(value)
    if isinstance(item, dict):
        file_value = item.get("ensemble_file") or item.get("path")
        if isinstance(file_value, str):
            return _conformer_file_molecules(resolve_input_file(file_value))
    if isinstance(item, str):
        candidate = resolve_input_file(item)
        return _conformer_file_molecules(candidate)
    records = _conformer_records(item)
    return [
        (record["conformer_id"], _rdkit_coordinate_molecule(record["structure"]))
        for record in records
    ]


def _cluster_conformers(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import AllChem
    from rdkit.ML.Cluster import Butina

    inputs, _method, settings = request_parts(request)
    loaded = _conformer_molecules(inputs["ensemble"])
    records = [{"conformer_id": conformer_id} for conformer_id, _molecule in loaded]
    molecules = [molecule for _conformer_id, molecule in loaded]
    molecule = molecules[0]
    first_symbols = [atom.GetSymbol() for atom in molecule.GetAtoms()]
    for candidate in molecules[1:]:
        if [atom.GetSymbol() for atom in candidate.GetAtoms()] != first_symbols:
            raise ValueError("All conformers must have identical atom ordering and elements")
        molecule.AddConformer(candidate.GetConformer(), assignId=True)
    cutoff = float(settings["rmsd_cutoff_angstrom"])
    if not math.isfinite(cutoff) or cutoff <= 0:
        raise ValueError("rmsd_cutoff_angstrom must be positive and finite")
    atom_selection = str(settings["atom_selection"]).strip().lower()
    if atom_selection == "all":
        atom_indices = list(range(molecule.GetNumAtoms()))
    elif atom_selection == "heavy":
        atom_indices = [atom.GetIdx() for atom in molecule.GetAtoms() if atom.GetAtomicNum() > 1]
    else:
        raise ValueError("atom_selection must be heavy or all")
    if not atom_indices:
        raise ValueError("The selected conformer atom set is empty")
    distances = list(
        AllChem.GetConformerRMSMatrix(
            molecule,
            atomIds=atom_indices,
            prealigned=bool(settings["prealign_conformers"]),
        )
    )
    cluster_indices = Butina.ClusterData(
        distances,
        len(records),
        cutoff,
        isDistData=True,
        reordering=bool(settings["reorder_cluster_centers"]),
    )
    clusters = []
    for cluster_index, members in enumerate(cluster_indices):
        member_indices = [int(value) for value in members]
        clusters.append(
            {
                "cluster_id": str(cluster_index),
                "representative_conformer_id": records[member_indices[0]]["conformer_id"],
                "member_conformer_ids": [records[index]["conformer_id"] for index in member_indices],
                "member_indices": member_indices,
                "size": len(member_indices),
            }
        )
    return success(
        {
            "clusters": clusters,
            "cluster_count": len(clusters),
            "conformer_count": len(records),
            "rmsd_cutoff_angstrom": cutoff,
            "atom_selection": atom_selection,
            "atom_indices": atom_indices,
            "prealigned": bool(settings["prealign_conformers"]),
        },
        backend_version=module_version("rdkit"),
    )


def _align_molecular_structures(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import rdMolAlign

    inputs, _method, settings = request_parts(request)
    reference = _rdkit_coordinate_molecule(inputs["reference"])
    probe = _rdkit_coordinate_molecule(inputs["probe"])
    raw_map = inputs["atom_map"]
    if not isinstance(raw_map, list) or len(raw_map) < 3:
        raise ValueError("atom_map must contain at least three [probe_index, reference_index] pairs")
    atom_map: list[tuple[int, int]] = []
    for pair in raw_map:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("Each atom_map entry must be [probe_index, reference_index]")
        probe_index, reference_index = int(pair[0]), int(pair[1])
        if not 0 <= probe_index < probe.GetNumAtoms():
            raise ValueError(f"Probe atom index out of range: {probe_index}")
        if not 0 <= reference_index < reference.GetNumAtoms():
            raise ValueError(f"Reference atom index out of range: {reference_index}")
        if probe.GetAtomWithIdx(probe_index).GetAtomicNum() != reference.GetAtomWithIdx(reference_index).GetAtomicNum():
            raise ValueError("Mapped probe/reference atoms must have the same element")
        atom_map.append((probe_index, reference_index))
    if len({pair[0] for pair in atom_map}) != len(atom_map) or len({pair[1] for pair in atom_map}) != len(atom_map):
        raise ValueError("atom_map indices must be one-to-one")
    maximum = int(settings["max_iterations"])
    if maximum < 1 or maximum > 100000:
        raise ValueError("max_iterations must be between 1 and 100000")
    rmsd = float(
        rdMolAlign.AlignMol(
            probe,
            reference,
            atomMap=atom_map,
            reflect=bool(settings["reflect"]),
            maxIters=maximum,
        )
    )
    return success(
        {
            "aligned_probe": _rdkit_structure(probe),
            "rmsd_angstrom": rmsd,
            "atom_map": [list(pair) for pair in atom_map],
            "reflect": bool(settings["reflect"]),
        },
        backend_version=module_version("rdkit"),
    )


def _write_rdkit_sdf(molecule, path: Path, conformer_ids: list[int] | None = None) -> None:
    from rdkit import Chem

    writer = Chem.SDWriter(str(path))
    try:
        for conformer_id in conformer_ids or [-1]:
            writer.write(molecule, confId=conformer_id)
    finally:
        writer.close()


def _standardize(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit import Chem
    from rdkit.Chem.MolStandardize import rdMolStandardize

    inputs, _method, settings = request_parts(request)
    molecule = _rdkit_molecule(inputs["structure"])
    molecule = rdMolStandardize.Cleanup(molecule)
    if bool(settings.get("largest_fragment", True)):
        molecule = rdMolStandardize.LargestFragmentChooser().choose(molecule)
    if bool(settings.get("neutralize", False)):
        molecule = rdMolStandardize.Uncharger().uncharge(molecule)
    if bool(settings.get("canonical_tautomer", False)):
        molecule = rdMolStandardize.TautomerEnumerator().Canonicalize(molecule)
    smiles = Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)
    return success(
        {
            "structure": {"smiles": smiles, "charge": int(Chem.GetFormalCharge(molecule))},
            "standardization_settings": settings,
        },
        backend_version=module_version("rdkit"),
    )


def _generate_3d_rdkit(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import AllChem

    inputs, _method, settings = request_parts(request)
    molecule = _rdkit_molecule(inputs["molecule"], add_hydrogens=True)
    seed = int(settings["random_seed"])
    parameters = AllChem.ETKDGv3()
    parameters.randomSeed = seed
    maximum_attempts = int(settings.get("max_attempts", 1000))
    # RDKit 2026 renamed this embedding control from maxAttempts to
    # maxIterations. Support both APIs without hiding the Agent parameter.
    if hasattr(parameters, "maxAttempts"):
        parameters.maxAttempts = maximum_attempts
    else:
        parameters.maxIterations = maximum_attempts
    status = AllChem.EmbedMolecule(molecule, parameters)
    if status != 0:
        raise RuntimeError(f"RDKit embedding failed with code {status}")
    directory = output_directory("generate_3d_structure", "rdkit")
    path = directory / "structure.sdf"
    _write_rdkit_sdf(molecule, path)
    return success(
        {"structure": _rdkit_structure(molecule), "random_seed": seed},
        artifact_files=[
            {"path": relative_workspace_path(path), "semantic_type": "AtomicStructure", "media_type": "chemical/x-mdl-sdfile"}
        ],
        backend_version=module_version("rdkit"),
    )


def _generate_3d_openbabel(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    molecule = structure_dict(inputs["molecule"])
    smiles = molecule.get("smiles")
    if not smiles:
        raise ValueError("Open Babel 3D generation currently requires SMILES")
    directory = output_directory("generate_3d_structure", "openbabel")
    path = directory / "structure.sdf"
    arguments = [f"-:{smiles}", "--gen3d", "-O", str(path)]
    force_field = method.get("force_field")
    if force_field:
        arguments.extend(["--ff", str(force_field)])
    completed = run_external(
        executable="obabel",
        arguments=arguments,
        directory=directory,
        timeout_seconds=int(settings.get("timeout_seconds", 600)),
    )
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge openbabel")
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if completed["returncode"] != 0 or not path.is_file():
        raise RuntimeError(f"Open Babel failed: {completed['stderr'][-2000:]}")
    return success(
        {"structure": structure_dict(relative_workspace_path(path))},
        artifact_files=[
            {"path": relative_workspace_path(path), "semantic_type": "AtomicStructure", "media_type": "chemical/x-mdl-sdfile"}
        ],
        provenance={"command": completed["command"]},
    )


def _conformers_rdkit(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import AllChem

    inputs, _method, settings = request_parts(request)
    molecule = _rdkit_molecule(inputs["molecule"], add_hydrogens=True)
    count = int(settings["num_conformers"])
    if count < 1 or count > 10000:
        raise ValueError("num_conformers must be between 1 and 10000")
    parameters = AllChem.ETKDGv3()
    parameters.randomSeed = int(settings["random_seed"])
    parameters.pruneRmsThresh = float(settings.get("prune_rms_threshold_angstrom", -1.0))
    conformer_ids = list(AllChem.EmbedMultipleConfs(molecule, numConfs=count, params=parameters))
    if not conformer_ids:
        raise RuntimeError("RDKit generated no conformers")
    directory = output_directory("generate_conformer_ensemble", "rdkit_etkdg")
    path = directory / "conformers.sdf"
    _write_rdkit_sdf(molecule, path, conformer_ids)
    ensemble = [
        {"conformer_id": str(identifier), "structure": _rdkit_structure(molecule, identifier)}
        for identifier in conformer_ids
    ]
    return success(
        {
            "ensemble": ensemble,
            "count": len(ensemble),
            "generation_settings": settings,
            "energies": None,
            "weights": None,
        },
        artifact_files=[
            {"path": relative_workspace_path(path), "semantic_type": "ConformerEnsemble", "media_type": "chemical/x-mdl-sdfile"}
        ],
        backend_version=module_version("rdkit"),
    )


def _conformers_crest(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    initial = inputs.get("initial_structure") or inputs.get("molecule")
    directory = output_directory("generate_conformer_ensemble", "crest")
    xyz = write_xyz(initial, directory / "input.xyz")
    method_name = "".join(character for character in str(method["method"]).casefold() if character.isalnum())
    method_argument = {
        "gfn1": "--gfn1",
        "gfn1xtb": "--gfn1",
        "xtbgfn1": "--gfn1",
        "gfn2": "--gfn2",
        "gfn2xtb": "--gfn2",
        "xtbgfn2": "--gfn2",
        "gfnff": "--gfnff",
        "gfnffxtb": "--gfnff",
        "xtbgfnff": "--gfnff",
    }.get(method_name)
    if method_argument is None:
        raise ValueError("CREST method must be GFN1-xTB, GFN2-xTB, or GFN-FF")
    structure = structure_dict(initial)
    charge = int(method.get("charge", structure.get("charge", 0)))
    multiplicity = int(method.get("multiplicity", structure.get("multiplicity", 1)))
    arguments = [str(xyz), method_argument, "--chrg", str(charge), "--uhf", str(max(0, multiplicity - 1))]
    solvation_model = str(method.get("solvation_model", "")).strip().casefold()
    if solvation_model:
        if solvation_model not in {"alpb", "gbsa"}:
            raise ValueError("CREST solvation_model must be alpb or gbsa")
        solvent = str(method.get("solvent", "")).strip()
        if not solvent:
            raise ValueError("CREST solvent is required when solvation_model is supplied")
        arguments.extend([f"--{solvation_model}", solvent])
    if "energy_window_kcal_mol" in settings:
        arguments.extend(["--ewin", str(settings["energy_window_kcal_mol"])])
    cpu_cores = int(request.get("resource_limits", {}).get("cpu_cores", 1))
    arguments.extend(["--T", str(cpu_cores)])
    completed = run_external(
        executable="crest",
        environment_variable="CHEMGRAPH_CREST_COMMAND",
        arguments=arguments,
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
        # CREST/xTB already parallelizes its sampling and electronic-structure
        # work through --T/OMP.  A second pthread OpenBLAS pool creates nested
        # parallelism, can exceed the Agent-selected CPU budget, and emits one
        # warning per linear-algebra call.  Keep BLAS serial inside the explicit
        # CREST worker pool while leaving the scientific --T choice untouched.
        environment_overrides={
            "OMP_NUM_THREADS": str(cpu_cores),
            "OPENBLAS_NUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1",
        },
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge crest xtb")
    if completed["returncode"] != 0:
        raise RuntimeError(f"CREST failed: {completed['stderr'][-2000:]}")
    ensemble_path = directory / "crest_conformers.xyz"
    if not ensemble_path.is_file():
        raise RuntimeError("CREST completed without crest_conformers.xyz")
    return success(
        {
            "ensemble_file": relative_workspace_path(ensemble_path),
            "generation_settings": {"method": method, **settings},
            "energies": None,
            "weights": None,
        },
        artifact_files=command_artifacts(directory),
        provenance={"command": completed["command"]},
    )


def _rank(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    ensemble = inputs["ensemble"]
    if isinstance(ensemble, dict) and "ensemble" in ensemble:
        ensemble = ensemble["ensemble"]
    scores = inputs["scores"]
    if not isinstance(ensemble, list) or not isinstance(scores, list) or len(ensemble) != len(scores):
        raise ValueError("ensemble and scores must be aligned lists of equal length")
    unit = str(settings["score_unit"]).lower()
    factors = {"hartree": 627.509474, "kcal_mol": 1.0, "kj_mol": 1 / 4.184, "ev": 23.060548}
    if unit not in factors:
        raise ValueError(f"Unsupported score_unit: {unit}")
    values = [float(item["value"] if isinstance(item, dict) else item) * factors[unit] for item in scores]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("All conformer scores must be finite")
    minimum = min(values)
    temperature = float(settings["temperature_kelvin"])
    if temperature <= 0:
        raise ValueError("temperature_kelvin must be positive")
    gas_constant = 0.00198720425864083  # kcal mol-1 K-1
    factors_boltzmann = [math.exp(-(value - minimum) / (gas_constant * temperature)) for value in values]
    total = sum(factors_boltzmann)
    records = []
    for index, (conformer, value, factor) in enumerate(zip(ensemble, values, factors_boltzmann)):
        records.append(
            {
                "conformer_id": str(conformer.get("conformer_id", index)) if isinstance(conformer, dict) else str(index),
                "structure": conformer.get("structure") if isinstance(conformer, dict) else conformer,
                "relative_score_kcal_mol": value - minimum,
                "weight": factor / total,
            }
        )
    records.sort(key=lambda item: item["relative_score_kcal_mol"])
    return success({"ensemble": records, "temperature_kelvin": temperature, "weighting": "boltzmann"})


def _enumerate_coordination_isomers(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    structure = structure_dict(inputs["structure"])
    atom_count = len(structure.get("atoms") or [])
    center = int(inputs["coordination_center_index"])
    anchors = [int(value) for value in inputs["ligand_anchor_indices"]]
    if center < 0 or center >= atom_count:
        raise ValueError("coordination_center_index is outside the supplied structure")
    if len(anchors) != len(set(anchors)) or center in anchors:
        raise ValueError("ligand_anchor_indices must be unique and exclude the coordination center")
    if any(index < 0 or index >= atom_count for index in anchors):
        raise ValueError("ligand_anchor_indices contains an index outside the supplied structure")

    geometry = str(settings["coordination_geometry"]).strip().lower()
    group_definition = {
        "trigonal_bipyramidal": (5, "axial", 2, "equatorial"),
        "square_pyramidal": (5, "apical", 1, "basal"),
        "octahedral": (6, "axial", 2, "equatorial"),
    }
    required_count, special_name, special_count, remaining_name = group_definition[geometry]
    if len(anchors) != required_count:
        raise ValueError(
            f"{geometry} requires exactly {required_count} ligand_anchor_indices"
        )
    max_isomers = int(settings["max_isomers"])
    if max_isomers < 1:
        raise ValueError("max_isomers must be positive")

    raw_labels = inputs.get("ligand_labels")
    if raw_labels is None:
        labels = {index: str(index) for index in anchors}
    elif isinstance(raw_labels, list) and len(raw_labels) == len(anchors):
        labels = {index: str(label) for index, label in zip(anchors, raw_labels)}
    elif isinstance(raw_labels, dict):
        labels = {index: str(raw_labels.get(str(index), raw_labels.get(index, index))) for index in anchors}
    else:
        raise ValueError(
            "ligand_labels must be omitted, an anchor-aligned list, or an index-to-label mapping"
        )

    records = []
    seen_label_partitions: set[tuple[tuple[str, ...], tuple[str, ...]]] = set()
    for selected in itertools.combinations(anchors, special_count):
        selected_set = set(selected)
        remaining = tuple(index for index in anchors if index not in selected_set)
        label_partition = (
            tuple(sorted(labels[index] for index in selected)),
            tuple(sorted(labels[index] for index in remaining)),
        )
        if label_partition in seen_label_partitions:
            continue
        seen_label_partitions.add(label_partition)
        records.append(
            {
                "isomer_id": f"{geometry}_{len(records) + 1:03d}",
                "site_groups": {
                    special_name: list(selected),
                    remaining_name: list(remaining),
                },
                "ligand_labels": {str(index): labels[index] for index in anchors},
                "symmetry_treatment": (
                    f"positions within {special_name} and within {remaining_name} are treated "
                    "as symmetry-equivalent; mirror/orientation permutations are not duplicated"
                ),
            }
        )
        if len(records) >= max_isomers:
            break
    return success(
        {
            "coordination_geometry": geometry,
            "coordination_center_index": center,
            "ligand_anchor_indices": anchors,
            "isomer_count": len(records),
            "isomers": records,
            "coordinates_generated": False,
            "energies_ranked": False,
        }
    )


def _pdbfixer(request: dict[str, Any], *, protonate: bool) -> dict[str, Any]:
    from openmm.app import PDBFile
    from pdbfixer import PDBFixer

    inputs, _method, settings = request_parts(request)
    source = resolve_input_file(inputs["structure"])
    action = "assign_protonation_states" if protonate else "repair_biomolecular_structure"
    directory = output_directory(action, "pdbfixer")
    destination = directory / ("protonated.pdb" if protonate else "repaired.pdb")
    fixer = PDBFixer(filename=str(source))
    if not protonate:
        fixer.findMissingResidues()
        if not bool(settings.get("add_missing_residues", False)):
            fixer.missingResidues = {}
        fixer.findNonstandardResidues()
        if bool(settings.get("replace_nonstandard_residues", True)):
            fixer.replaceNonstandardResidues()
        fixer.removeHeterogens(keepWater=bool(settings.get("keep_water", True)))
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
    else:
        fixer.addMissingHydrogens(float(settings["ph"]))
    with destination.open("w", encoding="utf-8") as handle:
        PDBFile.writeFile(fixer.topology, fixer.positions, handle, keepIds=True)
    return success(
        {
            "structure": structure_dict(relative_workspace_path(destination)),
            "atom_count": fixer.topology.getNumAtoms(),
            "residue_count": fixer.topology.getNumResidues(),
            "ph": float(settings["ph"]) if protonate else None,
        },
        artifact_files=[
            {"path": relative_workspace_path(destination), "semantic_type": "AtomicStructure", "media_type": "chemical/x-pdb"}
        ],
        backend_version=module_version("pdbfixer"),
    )


def _protonate_rdkit(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit import Chem

    inputs, _method, settings = request_parts(request)
    if settings["rule"] != "add_explicit_hydrogens":
        return unsupported("RDKit backend currently supports rule='add_explicit_hydrogens' only")
    molecule = Chem.AddHs(_rdkit_molecule(inputs["structure"]))
    return success(
        {"structure": _rdkit_structure(molecule), "ph": float(settings["ph"]), "rule": settings["rule"]},
        backend_version=module_version("rdkit"),
        warnings=["RDKit explicit-hydrogen addition is rule based and does not predict pKa."],
    )


def _gasteiger(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import AllChem

    inputs, method, _settings = request_parts(request)
    if str(method["charge_model"]).lower() not in {"gasteiger", "rdkit_gasteiger"}:
        raise ValueError("rdkit_gasteiger backend requires charge_model='gasteiger'")
    molecule = _rdkit_molecule(inputs["structure"], add_hydrogens=True)
    AllChem.ComputeGasteigerCharges(molecule)
    charges = [float(atom.GetProp("_GasteigerCharge")) for atom in molecule.GetAtoms()]
    if not all(math.isfinite(value) for value in charges):
        raise RuntimeError("RDKit produced non-finite Gasteiger charges")
    return success(
        {"structure": _rdkit_structure(molecule), "partial_charges_e": charges, "charge_model": "gasteiger"},
        backend_version=module_version("rdkit"),
    )


def _openff_charges(request: dict[str, Any]) -> dict[str, Any]:
    from openff.toolkit import Molecule

    inputs, method, _settings = request_parts(request)
    charge_model = str(method["charge_model"]).lower().replace("-", "")
    if charge_model != "am1bcc":
        raise ValueError(
            "openff_am1bcc requires charge_model='am1bcc'; AM1-BCC ELF10 requires a separately licensed OpenEye backend"
        )
    item = structure_dict(inputs["structure"])
    if not item.get("smiles"):
        raise ValueError("OpenFF charge assignment currently requires a structure with SMILES")
    molecule = Molecule.from_smiles(item["smiles"], allow_undefined_stereo=False)
    molecule.assign_partial_charges(charge_model)
    charges = [float(value.m_as("elementary_charge")) for value in molecule.partial_charges]
    return success(
        {"structure": item, "partial_charges_e": charges, "charge_model": charge_model},
        backend_version=module_version("openff-toolkit"),
    )


def _parameterize_openff(request: dict[str, Any]) -> dict[str, Any]:
    from openff.interchange import Interchange
    from openff.toolkit import ForceField, Molecule

    inputs, method, _settings = request_parts(request)
    item = structure_dict(inputs["structure"])
    if not item.get("smiles"):
        raise ValueError("OpenFF parameterization currently requires a structure with SMILES")
    molecule = Molecule.from_smiles(item["smiles"], allow_undefined_stereo=False)
    force_field_name = str(method["force_field"])
    force_field = ForceField(force_field_name)
    interchange = Interchange.from_smirnoff(force_field, molecule.to_topology())
    directory = output_directory("assign_force_field_parameters", "openff")
    path = directory / "interchange.json"
    path.write_text(interchange.model_dump_json(indent=2) + "\n", encoding="utf-8")
    result = {
        "structure": item,
        "force_field": force_field_name,
        "interchange_path": relative_workspace_path(path),
        "solvated": False,
    }
    return success(
        result,
        artifact_files=[
            {"path": relative_workspace_path(path), "semantic_type": "ParameterizedSystem", "media_type": "application/json"}
        ],
        backend_version=module_version("openff-interchange"),
    )


def _parameterize_openmm(request: dict[str, Any]) -> dict[str, Any]:
    import openmm
    from openmm import XmlSerializer
    from openmm.app import ForceField, PDBFile

    inputs, method, _settings = request_parts(request)
    source = resolve_input_file(inputs["structure"])
    force_fields = method["force_field"]
    if isinstance(force_fields, str):
        force_fields = [force_fields]
    pdb = PDBFile(str(source))
    force_field = ForceField(*[str(value) for value in force_fields])
    system = force_field.createSystem(pdb.topology)
    directory = output_directory("assign_force_field_parameters", "openmm_builder")
    system_path = directory / "system.xml"
    topology_path = directory / "topology.pdb"
    system_path.write_text(XmlSerializer.serialize(system), encoding="utf-8")
    with topology_path.open("w", encoding="utf-8") as handle:
        PDBFile.writeFile(pdb.topology, pdb.positions, handle)
    return success(
        {
            "topology_path": relative_workspace_path(topology_path),
            "system_xml_path": relative_workspace_path(system_path),
            "force_field": list(force_fields),
            "solvated": False,
        },
        artifact_files=[
            {"path": relative_workspace_path(topology_path), "semantic_type": "ParameterizedTopology", "media_type": "chemical/x-pdb"},
            {"path": relative_workspace_path(system_path), "semantic_type": "ParameterizedSystem", "media_type": "application/xml"},
        ],
        backend_version=getattr(openmm, "__version__", None),
    )


def _acpype_run(arguments: list[str], directory: Path, request: dict[str, Any]) -> dict[str, Any]:
    walltime = int((request.get("resource_limits") or {}).get("walltime_seconds", 1800))
    completed = run_external(
        executable="acpype",
        arguments=arguments,
        directory=directory,
        environment_variable="CHEMGRAPH_ACPYPE_COMMAND",
        timeout_seconds=max(1, walltime),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install="Install ACPYPE 2023.10.27, Open Babel 3.1.1, and AmberTools 26 in the configured ACPYPE runtime.",
        )
    if completed["returncode"] != 0:
        detail = completed["stderr"].strip() or completed["stdout"].strip()
        raise RuntimeError(f"ACPYPE failed with exit code {completed['returncode']}: {detail[-2000:]}")
    return completed


def _acpype_artifact(path: Path, semantic_type: str, media_type: str) -> dict[str, str]:
    return {
        "path": relative_workspace_path(path),
        "semantic_type": semantic_type,
        "media_type": media_type,
    }


def _generate_small_molecule_topology(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    source = resolve_input_file(inputs["structure_file"])
    if source.suffix.lower() not in {".pdb", ".mol2", ".mdl", ".mol", ".sdf"}:
        raise ValueError("structure_file must be PDB, MOL2, MDL, MOL, or SDF")
    atom_type = str(method["atom_type"]).lower()
    charge_method = str(method["charge_method"]).lower()
    charge_program = str(method["charge_program"]).lower()
    net_charge = int(method["net_charge"])
    multiplicity = int(method["multiplicity"])
    if multiplicity < 1:
        raise ValueError("multiplicity must be a positive integer")
    if charge_method == "user" and source.suffix.lower() != ".mol2":
        raise ValueError("charge_method='user' requires a MOL2 input carrying explicit charges")
    maximum_charge_time = int(settings["maximum_charge_time_seconds"])
    if maximum_charge_time < 1:
        raise ValueError("maximum_charge_time_seconds must be positive")
    directory = output_directory("generate_small_molecule_topology", "acpype")
    staged = shutil.copy2(source, directory / f"input{source.suffix.lower()}")
    arguments = [
        "-i", Path(staged).name, "-b", "molecule", "-n", str(net_charge),
        "-m", str(multiplicity), "-c", charge_method, "-a", atom_type,
        "-q", charge_program, "-o", str(settings["output_topologies"]).lower(),
        "-s", str(maximum_charge_time),
    ]
    if bool(settings["merge_atom_types"]):
        arguments.append("-g")
    if bool(settings["sort_atoms"]):
        arguments.append("-l")
    completed = _acpype_run(arguments, directory, request)
    if "status" in completed:
        return completed
    generated = directory / "molecule.acpype"
    if not generated.is_dir():
        raise RuntimeError("ACPYPE completed without creating molecule.acpype")
    expected = {
        "amber_topology_path": generated / "molecule_AC.prmtop",
        "amber_coordinate_path": generated / "molecule_AC.inpcrd",
    }
    gromacs_topology = generated / "molecule_GMX.top"
    gromacs_coordinates = generated / "molecule_GMX.gro"
    if gromacs_topology.is_file():
        expected["gromacs_topology_path"] = gromacs_topology
    if gromacs_coordinates.is_file():
        expected["gromacs_coordinate_path"] = gromacs_coordinates
    missing = [name for name, path in expected.items() if not path.is_file()]
    if missing:
        raise RuntimeError(f"ACPYPE completed without required outputs: {', '.join(missing)}")
    result = {
        name: relative_workspace_path(path) for name, path in expected.items()
    }
    result.update(
        {
            "force_field": atom_type,
            "charge_method": charge_method,
            "net_charge": net_charge,
            "multiplicity": multiplicity,
            "output_topologies": str(settings["output_topologies"]).lower(),
        }
    )
    artifacts = [
        _acpype_artifact(expected["amber_topology_path"], "AmberTopology", "application/octet-stream"),
        _acpype_artifact(expected["amber_coordinate_path"], "AmberCoordinates", "chemical/x-amber-inpcrd"),
    ]
    if gromacs_topology.is_file():
        artifacts.append(_acpype_artifact(gromacs_topology, "GromacsTopology", "text/plain"))
    if gromacs_coordinates.is_file():
        artifacts.append(_acpype_artifact(gromacs_coordinates, "GromacsCoordinates", "chemical/x-gromacs-gro"))
    return success(
        result,
        artifact_files=artifacts,
        backend_version="2023.10.27",
        provenance={"command": completed["command"]},
    )


def _convert_amber_topology_to_gromacs(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    topology = resolve_input_file(inputs["amber_topology"])
    coordinates = resolve_input_file(inputs["amber_coordinates"])
    directory = output_directory("convert_amber_topology_to_gromacs", "acpype")
    staged_topology = shutil.copy2(topology, directory / "input.prmtop")
    staged_coordinates = shutil.copy2(coordinates, directory / "input.inpcrd")
    arguments = [
        "-p", Path(staged_topology).name, "-x", Path(staged_coordinates).name,
        "-b", "converted",
    ]
    if bool(settings["direct_conversion"]):
        arguments.append("-u")
    if bool(settings["sort_atoms"]):
        arguments.append("-l")
    completed = _acpype_run(arguments, directory, request)
    if "status" in completed:
        return completed
    generated = directory / "converted.amb2gmx"
    gromacs_topology = generated / "converted_GMX.top"
    gromacs_coordinates = generated / "converted_GMX.gro"
    if not gromacs_topology.is_file() or not gromacs_coordinates.is_file():
        raise RuntimeError("ACPYPE completed without the converted GROMACS topology and coordinates")
    return success(
        {
            "gromacs_topology_path": relative_workspace_path(gromacs_topology),
            "gromacs_coordinate_path": relative_workspace_path(gromacs_coordinates),
            "direct_conversion": bool(settings["direct_conversion"]),
        },
        artifact_files=[
            _acpype_artifact(gromacs_topology, "GromacsTopology", "text/plain"),
            _acpype_artifact(gromacs_coordinates, "GromacsCoordinates", "chemical/x-gromacs-gro"),
        ],
        backend_version="2023.10.27",
        provenance={"command": completed["command"]},
    )


def _pmx_run(arguments: list[str], directory: Path, request: dict[str, Any]) -> dict[str, Any]:
    walltime = int((request.get("resource_limits") or {}).get("walltime_seconds", 1800))
    completed = run_external(
        executable="pmx",
        arguments=arguments,
        directory=directory,
        environment_variable="CHEMGRAPH_PMX_COMMAND",
        timeout_seconds=max(1, walltime),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(
            completed["stderr"],
            install="Build the fixed pmx commit and configure its GMXLIB mutation-force-field directory.",
        )
    if completed["returncode"] != 0:
        detail = completed["stderr"].strip() or completed["stdout"].strip()
        raise RuntimeError(f"pmx failed with exit code {completed['returncode']}: {detail[-2000:]}")
    return completed


def _pmx_mutate(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    source = resolve_input_file(inputs["structure"])
    if source.suffix.lower() not in {".pdb", ".gro"}:
        raise ValueError("pmx mutation requires a PDB or GRO structure")
    mutations = inputs["mutations"]
    if not isinstance(mutations, list) or not mutations:
        raise ValueError("mutations must be a non-empty list")
    keep_ids = bool(settings["keep_residue_ids"])
    has_reference = inputs.get("reference_structure") is not None
    preserve_ids = keep_ids or has_reference
    if keep_ids and has_reference:
        raise ValueError("keep_residue_ids and reference_structure are mutually exclusive pmx modes")
    lines = []
    normalized = []
    for index, item in enumerate(mutations):
        if not isinstance(item, dict):
            raise ValueError(f"mutations[{index}] must be a mapping")
        residue_id = int(item["residue_id"])
        target = str(item["target_residue_name"]).strip().upper()
        if residue_id < 1 or not target.isalnum():
            raise ValueError(f"mutations[{index}] has an invalid residue id or target name")
        chain = str(item.get("chain_id") or "").strip()
        if preserve_ids and (len(chain) != 1 or not chain.isalnum()):
            raise ValueError(f"mutations[{index}].chain_id is required when original residue ids are used")
        lines.append(f"{chain + ' ' if preserve_ids else ''}{residue_id} {target}")
        normalized.append({"chain_id": chain or None, "residue_id": residue_id, "target_residue_name": target})
    directory = output_directory("mutate_biomolecular_residues_for_alchemy", "pmx")
    staged = shutil.copy2(source, directory / f"input{source.suffix.lower()}")
    script = directory / "mutations.txt"
    script.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output = directory / f"hybrid{source.suffix.lower()}"
    arguments = [
        "mutate", "-f", Path(staged).name, "-o", output.name,
        "-ff", str(method["force_field"]), "--script", script.name,
    ]
    if keep_ids:
        arguments.append("--keep_resid")
    if has_reference:
        reference = resolve_input_file(inputs["reference_structure"])
        staged_reference = shutil.copy2(reference, directory / f"reference{reference.suffix.lower()}")
        arguments.extend(["--ref", Path(staged_reference).name])
    completed = _pmx_run(arguments, directory, request)
    if "status" in completed:
        return completed
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("pmx mutate completed without a hybrid structure")
    return success(
        {
            "structure_file": relative_workspace_path(output),
            "mutations": normalized,
            "force_field": str(method["force_field"]),
            "parameterized": False,
        },
        artifact_files=[_acpype_artifact(output, "AtomicStructure", "chemical/x-pdb" if output.suffix == ".pdb" else "chemical/x-gromacs-gro")],
        backend_version="0+untagged.1.g0dd5f0a",
        provenance={"command": completed["command"]},
    )


def _pmx_hybrid_topology(request: dict[str, Any]) -> dict[str, Any]:
    inputs, method, settings = request_parts(request)
    source = resolve_input_file(inputs["topology_file"])
    if source.suffix.lower() not in {".top", ".itp"}:
        raise ValueError("topology_file must be a GROMACS TOP or ITP file")
    directory = output_directory("generate_alchemical_hybrid_topology", "pmx")
    staged = shutil.copy2(source, directory / source.name)
    included = inputs.get("included_topology_files") or []
    if not isinstance(included, list):
        raise ValueError("included_topology_files must be a list")
    seen = {source.name}
    for value in included:
        include = resolve_input_file(value)
        if include.name in seen:
            raise ValueError(f"duplicate staged topology basename: {include.name}")
        seen.add(include.name)
        shutil.copy2(include, directory / include.name)
    output = directory / f"hybrid{source.suffix.lower()}"
    dummy_mass_scale = float(settings["dummy_mass_scale"])
    dummy_dihedral_scale = float(settings["dummy_dihedral_scale"])
    if dummy_mass_scale <= 0 or dummy_dihedral_scale < 0:
        raise ValueError("dummy_mass_scale must be positive and dummy_dihedral_scale non-negative")
    arguments = [
        "gentop", "-p", Path(staged).name, "-o", output.name,
        "-ff", str(method["force_field"]),
        "--scale_mass", str(dummy_mass_scale), "--scale_dih", str(dummy_dihedral_scale),
    ]
    if bool(settings["split_transformations"]):
        arguments.append("--split")
    if not bool(settings["recursive"]):
        arguments.append("--norecursive")
    completed = _pmx_run(arguments, directory, request)
    if "status" in completed:
        return completed
    if not output.is_file() or "typeB" not in output.read_text(encoding="utf-8", errors="replace"):
        raise RuntimeError("pmx gentop completed without a B-state hybrid topology")
    generated = [path for path in sorted(directory.iterdir()) if path.is_file() and path.suffix in {".top", ".itp"} and path != staged]
    return success(
        {
            "hybrid_topology_path": relative_workspace_path(output),
            "generated_topology_files": [relative_workspace_path(path) for path in generated],
            "force_field": str(method["force_field"]),
            "recursive": bool(settings["recursive"]),
            "split_transformations": bool(settings["split_transformations"]),
        },
        artifact_files=[_acpype_artifact(path, "AlchemicalTopology", "text/plain") for path in generated],
        backend_version="0+untagged.1.g0dd5f0a",
        provenance={"command": completed["command"]},
    )


def _pmx_atom_mapping(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    ligand_a = resolve_input_file(inputs["ligand_a"])
    ligand_b = resolve_input_file(inputs["ligand_b"])
    if ligand_a.suffix.lower() != ".pdb" or ligand_b.suffix.lower() != ".pdb":
        raise ValueError("pmx ligand atom mapping requires two PDB files")
    cutoff = float(settings["distance_cutoff_nm"])
    timeout = int(settings["mcs_timeout_seconds"])
    if cutoff <= 0 or timeout < 1:
        raise ValueError("distance_cutoff_nm and mcs_timeout_seconds must be positive")
    if not bool(settings["use_alignment"]) and not bool(settings["use_mcs"]):
        raise ValueError("At least one of use_alignment or use_mcs must be true")
    directory = output_directory("map_alchemical_ligand_atoms", "pmx")
    staged_a = shutil.copy2(ligand_a, directory / "ligand_a.pdb")
    staged_b = shutil.copy2(ligand_b, directory / "ligand_b.pdb")
    arguments = [
        "atomMapping", "-i1", Path(staged_a).name, "-i2", Path(staged_b).name,
        "-o1", "pairs_a.dat", "-o2", "pairs_b.dat", "-score", "score.dat",
        "-log", "mapping.log", "--d", str(cutoff), "--timeout", str(timeout),
    ]
    flags = {
        "use_alignment": "--no-alignment",
        "use_mcs": "--no-mcs",
        "map_nonpolar_hydrogens": "--no-H2H",
        "map_polar_hydrogens": "--H2Hpolar",
        "allow_hydrogen_to_heavy": "--H2Heavy",
        "rings_only": "--RingsOnly",
        "apply_distance_to_mcs": "--dMCS",
        "cross_check_swapped_order": "--swap",
        "check_chirality": "--no-chirality",
    }
    for key, flag in flags.items():
        value = bool(settings[key])
        inverted = key in {"use_alignment", "use_mcs", "map_nonpolar_hydrogens", "check_chirality"}
        if (inverted and not value) or (not inverted and value):
            arguments.append(flag)
    completed = _pmx_run(arguments, directory, request)
    if "status" in completed:
        return completed
    pairs_path = directory / "pairs_a.dat"
    score_path = directory / "score.dat"
    if not pairs_path.is_file() or not score_path.is_file():
        raise RuntimeError("pmx atomMapping completed without mapping and score files")
    pairs = []
    for line in pairs_path.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) >= 2:
            pairs.append([int(fields[0]), int(fields[1])])
    if not pairs:
        raise RuntimeError("pmx atomMapping produced an empty atom mapping")
    score_text = score_path.read_text(encoding="utf-8")
    try:
        score = float(score_text.split(":", 1)[1].strip())
    except (IndexError, ValueError) as exc:
        raise RuntimeError("Could not parse the pmx mapping dissimilarity score") from exc
    artifacts = [
        _acpype_artifact(pairs_path, "AlchemicalAtomMapping", "text/plain"),
        _acpype_artifact(directory / "pairs_b.dat", "AlchemicalAtomMapping", "text/plain"),
        _acpype_artifact(score_path, "MappingScore", "text/plain"),
        _acpype_artifact(directory / "mapping.log", "BackendLog", "text/plain"),
    ]
    return success(
        {
            "atom_pairs_one_based": pairs,
            "mapped_atom_count": len(pairs),
            "dissimilarity_score": score,
            "distance_cutoff_nm": cutoff,
        },
        artifact_files=artifacts,
        backend_version="0+untagged.1.g0dd5f0a",
        provenance={"command": completed["command"]},
    )


def _solvate_openmm(request: dict[str, Any]) -> dict[str, Any]:
    import openmm
    from openmm import XmlSerializer
    from openmm.app import ForceField, Modeller, PDBFile

    inputs, method, settings = request_parts(request)
    system_value = inputs["system"]
    if isinstance(system_value, dict) and "result" in system_value:
        system_value = system_value["result"]
    if not isinstance(system_value, dict):
        raise ValueError("OpenMM solvation requires a ParameterizedSystem object")
    topology_path = resolve_input_file(system_value["topology_path"])
    force_fields = method.get("force_field") or system_value.get("force_field")
    if isinstance(force_fields, str):
        force_fields = [force_fields]
    if not force_fields:
        raise ValueError("force_field must be supplied or present in ParameterizedSystem")
    pdb = PDBFile(str(topology_path))
    modeller = Modeller(pdb.topology, pdb.positions)
    force_field = ForceField(*force_fields)
    modeller.addSolvent(
        force_field,
        model=str(settings["solvent_model"]),
        padding=float(settings["padding_angstrom"]) * openmm.unit.angstrom,
        ionicStrength=float(settings.get("ionic_strength_molar", 0.0)) * openmm.unit.molar,
        positiveIon=str(settings.get("positive_ion", "Na+")),
        negativeIon=str(settings.get("negative_ion", "Cl-")),
    )
    created = force_field.createSystem(modeller.topology)
    directory = output_directory("solvate_molecular_system", "openmm_builder")
    solvated_path = directory / "solvated.pdb"
    system_path = directory / "system.xml"
    with solvated_path.open("w", encoding="utf-8") as handle:
        PDBFile.writeFile(modeller.topology, modeller.positions, handle)
    system_path.write_text(XmlSerializer.serialize(created), encoding="utf-8")
    return success(
        {
            "topology_path": relative_workspace_path(solvated_path),
            "system_xml_path": relative_workspace_path(system_path),
            "force_field": force_fields,
            "solvated": True,
            "environment_settings": settings,
        },
        artifact_files=[
            {"path": relative_workspace_path(solvated_path), "semantic_type": "ParameterizedTopology", "media_type": "chemical/x-pdb"},
            {"path": relative_workspace_path(system_path), "semantic_type": "ParameterizedSystem", "media_type": "application/xml"},
        ],
        backend_version=getattr(openmm, "__version__", None),
    )


def _solvate_packmol(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    system = inputs["system"]
    if not isinstance(system, dict):
        raise ValueError("Packmol requires a system mapping with solute_path")
    solute = resolve_input_file(system["solute_path"])
    solvent = resolve_input_file(settings["solvent_path"])
    counts = dict(settings["molecule_counts"])
    solvent_count = int(counts.get("solvent", 0))
    if solvent_count < 1:
        raise ValueError("molecule_counts.solvent must be positive")
    size = settings["box_size_angstrom"]
    if len(size) != 3:
        raise ValueError("box_size_angstrom must contain three values")
    box_shape = str(settings["box_shape"]).lower()
    if box_shape not in {"rectangular", "orthorhombic", "cubic"}:
        raise ValueError("Packmol box_shape must be rectangular, orthorhombic, or cubic")
    if box_shape == "cubic" and len({float(value) for value in size}) != 1:
        raise ValueError("A cubic Packmol box requires three equal box_size_angstrom values")
    directory = output_directory("solvate_molecular_system", "packmol")
    output = directory / "packed.pdb"
    text = (
        f"tolerance {float(settings.get('tolerance_angstrom', 2.0))}\n"
        f"filetype pdb\noutput {output.name}\n\n"
        f"structure {solute}\n  number 1\n  fixed 0. 0. 0. 0. 0. 0.\nend structure\n\n"
        f"structure {solvent}\n  number {solvent_count}\n"
        f"  inside box 0. 0. 0. {float(size[0])} {float(size[1])} {float(size[2])}\n"
        "end structure\n"
    )
    input_path = directory / "packmol.inp"
    input_path.write_text(text, encoding="utf-8")
    completed = run_external(
        executable="packmol", arguments=["-i", str(input_path)], directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
    )
    (directory / "stdout.log").write_text(completed["stdout"], encoding="utf-8")
    (directory / "stderr.log").write_text(completed["stderr"], encoding="utf-8")
    if not completed["available"]:
        return unavailable(completed["stderr"], install="conda install -c conda-forge packmol")
    if completed["returncode"] != 0 or not output.is_file():
        raise RuntimeError(f"Packmol failed: {completed['stderr'][-2000:]}")
    return success(
        {
            **system,
            "topology_path": relative_workspace_path(output),
            "solvated": True,
            "environment_settings": settings,
        },
        artifact_files=command_artifacts(directory),
        provenance={"command": completed["command"]},
    )


def _pdb_summary(lines: list[str]) -> dict[str, Any]:
    atom_lines = [line for line in lines if line.startswith(("ATOM  ", "HETATM"))]
    return {
        "atom_record_count": len(atom_lines),
        "heteroatom_record_count": sum(line.startswith("HETATM") for line in atom_lines),
        "chains": sorted({line[21] for line in atom_lines if len(line) > 21}),
        "model_count": sum(line.startswith("MODEL") for line in lines) or 1,
    }


def _resolve_pdb_input(value: Any) -> Path:
    item = unwrap_artifact(value)
    if isinstance(item, dict) and isinstance(item.get("result"), dict):
        item = item["result"]
    if isinstance(item, dict):
        for key in ("structure_path", "topology_path", "path"):
            if isinstance(item.get(key), str):
                return resolve_input_file(item[key])
    return resolve_input_file(item)


def _write_pdb_action(
    *,
    action_id: str,
    filename: str,
    lines: list[str],
    details: dict[str, Any],
) -> dict[str, Any]:
    directory = output_directory(action_id, "pdb_tools")
    path = directory / filename
    path.write_text("".join(lines), encoding="utf-8")
    return success(
        {
            "structure_path": relative_workspace_path(path),
            **_pdb_summary(lines),
            **details,
        },
        artifact_files=[
            {
                "path": relative_workspace_path(path),
                "semantic_type": "AtomicStructure",
                "media_type": "chemical/x-pdb",
            }
        ],
        backend_version=module_version("pdb-tools"),
    )


def _select_pdb_subset(request: dict[str, Any]) -> dict[str, Any]:
    from pdbtools import pdb_delhetatm, pdb_selchain, pdb_selmodel

    inputs, _method, settings = request_parts(request)
    source = _resolve_pdb_input(inputs["structure"])
    chains = settings["chains"]
    models = settings["models"]
    if not isinstance(chains, (list, tuple)) or any(
        not isinstance(value, str) or len(value) != 1 for value in chains
    ):
        raise ValueError("chains must be a list of one-character PDB chain identifiers")
    if not isinstance(models, (list, tuple)) or any(int(value) < 1 for value in models):
        raise ValueError("models must be a list of positive model identifiers")
    if not isinstance(settings["keep_heteroatoms"], bool):
        raise ValueError("keep_heteroatoms must be an explicit boolean")
    with source.open("r", encoding="utf-8", errors="replace") as handle:
        stream: Any = handle
        if models:
            stream = pdb_selmodel.run(stream, {int(value) for value in models})
        if chains:
            stream = pdb_selchain.run(stream, set(chains))
        if not settings["keep_heteroatoms"]:
            stream = pdb_delhetatm.run(stream)
        lines = list(stream)
    if not any(line.startswith(("ATOM  ", "HETATM")) for line in lines):
        raise ValueError("The requested PDB subset contains no ATOM/HETATM records")
    return _write_pdb_action(
        action_id="select_structure_subset",
        filename="selected.pdb",
        lines=lines,
        details={
            "selected_chains": list(chains),
            "selected_models": [int(value) for value in models],
            "keep_heteroatoms": settings["keep_heteroatoms"],
        },
    )


def _renumber_pdb(request: dict[str, Any]) -> dict[str, Any]:
    from pdbtools import pdb_reatom, pdb_reres

    inputs, _method, settings = request_parts(request)
    source = _resolve_pdb_input(inputs["structure"])
    atom_start = int(settings["starting_atom_serial"])
    residue_start = int(settings["starting_residue_number"])
    hybrid36 = settings["hybrid36"]
    if not isinstance(hybrid36, bool):
        raise ValueError("hybrid36 must be an explicit boolean")
    if atom_start < 1:
        raise ValueError("starting_atom_serial must be positive")
    if residue_start < -999 or residue_start > 9999:
        raise ValueError("starting_residue_number must be between -999 and 9999")
    with source.open("r", encoding="utf-8", errors="replace") as handle:
        residue_stream = pdb_reres.run(handle, residue_start)
        lines = list(pdb_reatom.run(residue_stream, atom_start, h36=hybrid36))
    return _write_pdb_action(
        action_id="renumber_biomolecular_structure",
        filename="renumbered.pdb",
        lines=lines,
        details={
            "starting_atom_serial": atom_start,
            "starting_residue_number": residue_start,
            "hybrid36": hybrid36,
        },
    )


def _normalize_pdb(request: dict[str, Any]) -> dict[str, Any]:
    from pdbtools import pdb_sort, pdb_tidy

    inputs, _method, settings = request_parts(request)
    source = _resolve_pdb_input(inputs["structure"])
    sort_by = str(settings["sort_by"]).strip().lower()
    sort_keys = {
        "none": None,
        "chain_and_residue": ["C", "R"],
        "chain": ["C"],
        "residue": ["R"],
    }.get(sort_by)
    if sort_by not in {"none", "chain_and_residue", "chain", "residue"}:
        raise ValueError("sort_by must be none, chain_and_residue, chain, or residue")
    strict = settings["strict_chain_breaks"]
    hybrid36 = settings["hybrid36"]
    if not isinstance(strict, bool) or not isinstance(hybrid36, bool):
        raise ValueError("strict_chain_breaks and hybrid36 must be explicit booleans")
    source_lines = source.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    model_count = sum(line.startswith("MODEL") for line in source_lines)
    if sort_keys is not None and model_count > 1:
        raise ValueError(
            "pdb-tools sorting does not support multi-model PDB files; select one model first "
            "or use sort_by=none"
        )
    if sort_keys is not None and model_count == 1:
        source_lines = [
            line for line in source_lines if not line.startswith(("MODEL", "ENDMDL"))
        ]
    stream: Any = source_lines
    if sort_keys is not None:
        stream = pdb_sort.run(stream, sort_keys)
    lines = list(pdb_tidy.run(stream, strict=strict, h36=hybrid36))
    return _write_pdb_action(
        action_id="normalize_pdb_records",
        filename="normalized.pdb",
        lines=lines,
        details={
            "sort_by": sort_by,
            "strict_chain_breaks": strict,
            "hybrid36": hybrid36,
        },
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if action_id == "enumerate_coordination_isomers" and backend_id == "internal_reaction_analysis":
        return _enumerate_coordination_isomers(request)
    if action_id == "analyze_crystal_symmetry" and backend_id == "vaspkit":
        return _analyze_vaspkit_symmetry(request)
    if action_id == "analyze_crystal_symmetry" and backend_id in {"spglib", "pymatgen"}:
        return _analyze_crystal_symmetry(backend_id, request)
    if action_id == "standardize_crystal_structure" and backend_id in {"spglib", "pymatgen"}:
        return _standardize_crystal(backend_id, request)
    if action_id == "build_supercell" and backend_id == "pymatgen":
        return _build_supercell(request)
    if action_id == "enumerate_surface_slabs" and backend_id == "pymatgen":
        return _enumerate_surface_slabs(request)
    if action_id == "standardize_structure" and backend_id == "rdkit":
        return _standardize(request)
    if action_id == "generate_3d_structure":
        return _generate_3d_rdkit(request) if backend_id == "rdkit" else _generate_3d_openbabel(request)
    if action_id == "generate_conformer_ensemble":
        return _conformers_rdkit(request) if backend_id == "rdkit_etkdg" else _conformers_crest(request)
    if action_id == "cluster_conformers" and backend_id == "rdkit":
        return _cluster_conformers(request)
    if action_id == "align_molecular_structures" and backend_id == "rdkit":
        return _align_molecular_structures(request)
    if action_id == "rank_conformers_from_results" and backend_id == "internal_statistics":
        return _rank(request)
    if action_id == "repair_biomolecular_structure" and backend_id == "pdbfixer":
        return _pdbfixer(request, protonate=False)
    if action_id == "assign_protonation_states":
        return _pdbfixer(request, protonate=True) if backend_id == "pdbfixer" else _protonate_rdkit(request)
    if action_id == "assign_partial_charges":
        return _gasteiger(request) if backend_id == "rdkit_gasteiger" else _openff_charges(request)
    if action_id == "assign_force_field_parameters":
        return _parameterize_openff(request) if backend_id == "openff" else _parameterize_openmm(request)
    if action_id == "generate_small_molecule_topology" and backend_id == "acpype":
        return _generate_small_molecule_topology(request)
    if action_id == "convert_amber_topology_to_gromacs" and backend_id == "acpype":
        return _convert_amber_topology_to_gromacs(request)
    if action_id == "mutate_biomolecular_residues_for_alchemy" and backend_id == "pmx":
        return _pmx_mutate(request)
    if action_id == "generate_alchemical_hybrid_topology" and backend_id == "pmx":
        return _pmx_hybrid_topology(request)
    if action_id == "map_alchemical_ligand_atoms" and backend_id == "pmx":
        return _pmx_atom_mapping(request)
    if action_id == "solvate_molecular_system":
        return _solvate_openmm(request) if backend_id == "openmm_builder" else _solvate_packmol(request)
    if action_id == "select_structure_subset" and backend_id == "pdb_tools":
        return _select_pdb_subset(request)
    if action_id == "renumber_biomolecular_structure" and backend_id == "pdb_tools":
        return _renumber_pdb(request)
    if action_id == "normalize_pdb_records" and backend_id == "pdb_tools":
        return _normalize_pdb(request)
    return unsupported(f"Unsupported structure action/backend combination: {action_id}/{backend_id}")

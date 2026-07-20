"""Structure, conformer, charge, and simulation-system actions."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from .common import (
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
    "analyze_crystal_symmetry", "standardize_crystal_structure",
    "build_supercell", "enumerate_surface_slabs",
    "select_structure_subset", "renumber_biomolecular_structure",
    "normalize_pdb_records",
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


def _cluster_conformers(request: dict[str, Any]) -> dict[str, Any]:
    from rdkit.Chem import AllChem
    from rdkit.ML.Cluster import Butina

    inputs, _method, settings = request_parts(request)
    records = _conformer_records(inputs["ensemble"])
    molecules = [_rdkit_coordinate_molecule(record["structure"]) for record in records]
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
    parameters.maxAttempts = int(settings.get("max_attempts", 1000))
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
    method_name = str(method["method"]).lower().replace("-", "")
    method_argument = {"gfn1": "--gfn1", "gfn2": "--gfn2", "gfnff": "--gfnff"}.get(method_name)
    if method_argument is None:
        raise ValueError("CREST method must be gfn1, gfn2, or gfnff")
    structure = structure_dict(initial)
    charge = int(method.get("charge", structure.get("charge", 0)))
    multiplicity = int(method.get("multiplicity", structure.get("multiplicity", 1)))
    arguments = [str(xyz), method_argument, "--chrg", str(charge), "--uhf", str(max(0, multiplicity - 1))]
    if "energy_window_kcal_mol" in settings:
        arguments.extend(["--ewin", str(settings["energy_window_kcal_mol"])])
    completed = run_external(
        executable="crest",
        environment_variable="CHEMGRAPH_CREST_COMMAND",
        arguments=arguments,
        directory=directory,
        timeout_seconds=int(request.get("resource_limits", {}).get("walltime_seconds", 1800)),
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
    if action_id == "solvate_molecular_system":
        return _solvate_openmm(request) if backend_id == "openmm_builder" else _solvate_packmol(request)
    if action_id == "select_structure_subset" and backend_id == "pdb_tools":
        return _select_pdb_subset(request)
    if action_id == "renumber_biomolecular_structure" and backend_id == "pdb_tools":
        return _renumber_pdb(request)
    if action_id == "normalize_pdb_records" and backend_id == "pdb_tools":
        return _normalize_pdb(request)
    return unsupported(f"Unsupported structure action/backend combination: {action_id}/{backend_id}")

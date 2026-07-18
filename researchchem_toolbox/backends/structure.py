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
    unsupported,
    write_json,
    write_xyz,
)


ACTIONS = {
    "standardize_structure", "generate_3d_structure", "generate_conformer_ensemble",
    "rank_conformers_from_results", "repair_biomolecular_structure",
    "assign_protonation_states", "assign_partial_charges",
    "assign_force_field_parameters", "solvate_molecular_system",
}


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


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if action_id == "standardize_structure" and backend_id == "rdkit":
        return _standardize(request)
    if action_id == "generate_3d_structure":
        return _generate_3d_rdkit(request) if backend_id == "rdkit" else _generate_3d_openbabel(request)
    if action_id == "generate_conformer_ensemble":
        return _conformers_rdkit(request) if backend_id == "rdkit_etkdg" else _conformers_crest(request)
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
    return unsupported(f"Unsupported structure action/backend combination: {action_id}/{backend_id}")

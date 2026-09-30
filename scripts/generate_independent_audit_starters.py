#!/usr/bin/env python3
"""Generate unoptimized XYZ starters from topology, not archived coordinates.

Reads an explicit-H atom-mapped SMILES plus coarse conformer identity windows.
Writes JSON to stdout only; package changes must be applied separately. No
quantum calculation, force-field minimization, energy ranking, source-coordinate
template, RMSD selection, or evaluator target is used.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from rdkit import Chem, rdBase
from rdkit.Chem import AllChem, rdMolDescriptors, rdMolTransforms


def graph_from_definition(definition: dict) -> Chem.Mol:
    parser = Chem.SmilesParserParams()
    parser.removeHs = False
    mol = Chem.MolFromSmiles(definition["mapped_smiles"], parser)
    if mol is None:
        raise ValueError("Invalid mapped SMILES")
    order = sorted(range(mol.GetNumAtoms()), key=lambda i: mol.GetAtomWithIdx(i).GetAtomMapNum())
    mol = Chem.RenumberAtoms(mol, order)
    assert [a.GetAtomMapNum() for a in mol.GetAtoms()] == list(range(1, mol.GetNumAtoms() + 1))
    assert mol.GetNumAtoms() == definition["atom_count"]
    assert rdMolDescriptors.CalcMolFormula(mol) == definition["formula"]
    assert sum(a.GetFormalCharge() for a in mol.GetAtoms()) == definition["charge"]
    assert mol.GetNumConformers() == 0
    return mol


def chirality(mol: Chem.Mol) -> list[tuple[int, str]]:
    return Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False)


def inspect_geometry(mol: Chem.Mol, expected_chirality: list) -> dict | None:
    xyz = mol.GetConformer().GetPositions()
    if not np.isfinite(xyz).all():
        return None
    pt = Chem.GetPeriodicTable()
    min_nonbonded_ratio = float("inf")
    max_bond_ratio = 0.0
    min_bond_ratio = float("inf")
    for i in range(mol.GetNumAtoms()):
        for j in range(i):
            radius = pt.GetRcovalent(mol.GetAtomWithIdx(i).GetAtomicNum()) + pt.GetRcovalent(mol.GetAtomWithIdx(j).GetAtomicNum())
            ratio = float(np.linalg.norm(xyz[i] - xyz[j]) / radius)
            if mol.GetBondBetweenAtoms(i, j):
                min_bond_ratio = min(min_bond_ratio, ratio)
                max_bond_ratio = max(max_bond_ratio, ratio)
                if not 0.72 < ratio < 1.32:
                    return None
            else:
                min_nonbonded_ratio = min(min_nonbonded_ratio, ratio)
                if ratio < 0.78:
                    return None
    measured = Chem.Mol(mol)
    Chem.AssignAtomChiralTagsFromStructure(measured, replaceExistingTags=True)
    Chem.AssignStereochemistry(measured, cleanIt=True, force=True)
    if chirality(measured) != expected_chirality:
        return None
    return {"atom_count": mol.GetNumAtoms(), "formula": rdMolDescriptors.CalcMolFormula(mol),
            "chiral_centers_zero_based": expected_chirality,
            "minimum_nonbonded_covalent_radius_ratio": min_nonbonded_ratio,
            "bond_covalent_radius_ratio_range": [min_bond_ratio, max_bond_ratio]}


def generate(definition: dict) -> dict:
    template = graph_from_definition(definition)
    stereo = chirality(template)
    pending = dict(definition["conformers"])
    accepted = {}
    for seed in range(914001, 914513):
        mol = Chem.Mol(template)
        params = AllChem.ETKDGv3()
        params.randomSeed = seed
        params.numThreads = 1
        params.useRandomCoords = True
        if AllChem.EmbedMolecule(mol, params) != 0:
            continue
        for filename, spec in list(pending.items()):
            candidate = Chem.Mol(mol)
            # Some conjugated-bond ETKDG priors are planar. A generic rotamer
            # rotation distinguishes task-defined initial classes without
            # importing any author's optimized angle or coordinate template.
            for window in spec["torsion_windows"]:
                if "initial_angle_deg" in window:
                    rdMolTransforms.SetDihedralDeg(candidate.GetConformer(), *[i-1 for i in window["atom_ids"]], window["initial_angle_deg"])
            validation = inspect_geometry(candidate, stereo)
            if validation is None:
                continue
            torsions = []
            matches = True
            for window in definition.get("shared_torsion_windows", []) + spec["torsion_windows"]:
                angle = rdMolTransforms.GetDihedralDeg(candidate.GetConformer(), *[i-1 for i in window["atom_ids"]])
                value = abs(angle) if window.get("absolute") else angle
                if not window["degrees"][0] <= value <= window["degrees"][1]:
                    matches = False
                    break
                torsions.append({"atom_ids": window["atom_ids"], "angle_deg": angle})
            if not matches:
                continue
            lines = [str(mol.GetNumAtoms()), f"Independent ETKDG topology-only starter {spec['id']}; unoptimized; charge 0 multiplicity 1; atom order retained"]
            for atom, pos in zip(candidate.GetAtoms(), candidate.GetConformer().GetPositions()):
                lines.append(f"{atom.GetSymbol()} {pos[0]:.8f} {pos[1]:.8f} {pos[2]:.8f}")
            accepted[filename] = {"xyz": "\n".join(lines)+"\n", "seed": seed,
                                  "validation": validation, "identity_torsions": torsions}
            del pending[filename]
        if not pending:
            break
    if pending:
        raise RuntimeError(f"No accepted topology-only starter for: {sorted(pending)}")
    return {"generator": "ETKDGv3 with optional generic rotamer rotations; first geometrically valid member of each coarse identity class",
            "rdkit_version": rdBase.rdkitVersion, "quantum_calculation": False,
            "force_field_minimization": False, "energy_ranking": False,
            "source_coordinate_template": False, "structures": accepted}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("definition", type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(json.loads(args.definition.read_text())), indent=2))


if __name__ == "__main__":
    main()

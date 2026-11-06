"""Accurate CIP labels and input identity checks, without changing stereochemistry.

RDKit is imported at the call boundary so non-molecular tool users need not load it.
Atom-map numbers are identifiers, never a substitute for stereochemical evidence.
"""
from __future__ import annotations


CIP_ALGORITHM = "rdkit.Chem.rdCIPLabeler.AssignCIPLabels"


def accurate_cip_labels(molecule):
    """Return labels by atom-map ID from a copy; preserve the caller's molecule."""
    from rdkit import Chem
    from rdkit.Chem import rdCIPLabeler

    mol = Chem.Mol(molecule)
    ids = [atom.GetAtomMapNum() for atom in mol.GetAtoms()]
    if not ids or any(atom_id <= 0 for atom_id in ids) or len(set(ids)) != len(ids):
        raise ValueError("CIP assignment requires unique positive atom-map IDs")
    for atom in mol.GetAtoms():
        if atom.HasProp("_CIPCode"):
            atom.ClearProp("_CIPCode")
    rdCIPLabeler.AssignCIPLabels(mol)
    return {atom.GetAtomMapNum(): atom.GetProp("_CIPCode") if atom.HasProp("_CIPCode") else None
            for atom in mol.GetAtoms()}


def _canonical(molecule):
    from rdkit import Chem

    mol = Chem.Mol(molecule)
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(0)
    return Chem.MolToSmiles(Chem.RemoveHs(mol), isomericSmiles=True)


def check_molecule_document(document):
    """Check explicit identities and declared CIP, including intentionally absent labels."""
    from rdkit import Chem

    errors = []
    for entry in document["molecules"]:
        name = entry["id"]
        params = Chem.SmilesParserParams()
        params.removeHs = False
        mapped = Chem.MolFromSmiles(entry["mapped_smiles"], params)
        plain = Chem.MolFromSmiles(entry["smiles"], params)
        if mapped is None or plain is None:
            errors.append(f"{name}:invalid_smiles")
            continue
        if _canonical(mapped) != _canonical(plain):
            errors.append(f"{name}:mapped_smiles_stereochemistry_mismatch")
        try:
            labels = accurate_cip_labels(mapped)
        except ValueError as error:
            errors.append(f"{name}:{error}")
            continue
        declared = {atom["atom_id"]: atom for atom in entry["atoms"]}
        if len(declared) != len(entry["atoms"]) or set(labels) != set(declared):
            errors.append(f"{name}:atom_map_table_mismatch")
            continue
        for atom in mapped.GetAtoms():
            atom_id = atom.GetAtomMapNum()
            if declared[atom_id]["element"] != atom.GetSymbol():
                errors.append(f"{name}:atom_{atom_id}:element_mismatch")
            if declared[atom_id].get("cip") != labels[atom_id]:
                errors.append(f"{name}:atom_{atom_id}:cip_expected_{labels[atom_id]}")
    return errors


def check_initial_geometry(document, xyz_text, mapping):
    """Validate an explicitly mapped starting geometry against its molecular identity."""
    from rdkit import Chem
    from rdkit.Chem import rdDetermineBonds

    entries = {item["id"]: item for item in document["molecules"]}
    molecule_id = mapping.get("molecule_id")
    if molecule_id is None:
        molecule_id = next(iter(entries)) if len(entries) == 1 else "S"
    if molecule_id not in entries:
        raise ValueError("initial XYZ requires an unambiguous molecule_id")
    entry = entries[molecule_id]
    mol = Chem.MolFromXYZBlock(xyz_text)
    if mol is None:
        raise ValueError("invalid initial XYZ")
    rows = mapping["atoms"]
    if sorted(row["xyz_row_1based"] for row in rows) != list(range(1, mol.GetNumAtoms() + 1)):
        raise ValueError("initial XYZ mapping is not one-to-one")
    # Coordinates determine adjacency and stereo, not a radical's bond orders.
    # Use the declared graph for bond orders only after checking adjacency.
    rdDetermineBonds.DetermineConnectivity(mol)
    reference_mol = Chem.MolFromSmiles(entry["mapped_smiles"])
    reference_atoms = {atom.GetAtomMapNum(): atom for atom in reference_mol.GetAtoms()}
    used = {row["heavy_atom_id"] for row in rows if row["heavy_atom_id"] is not None}
    expected = {atom["atom_id"] for atom in entry["atoms"] if atom["element"] != "H"}
    if used != expected:
        raise ValueError("initial XYZ heavy-atom mapping mismatch")
    next_id = max(used, default=0) + 1
    for row in rows:
        atom = mol.GetAtomWithIdx(row["xyz_row_1based"] - 1)
        if atom.GetSymbol() != row["element"]:
            raise ValueError("initial XYZ row element mismatch")
        atom_id = row["heavy_atom_id"]
        if atom_id is None:
            if atom.GetSymbol() != "H":
                raise ValueError("initial XYZ missing heavy-atom ID")
            atom_id, next_id = next_id, next_id + 1
        atom.SetAtomMapNum(atom_id)
    for row in rows:
        if row["heavy_atom_id"] is None:
            atom = mol.GetAtomWithIdx(row["xyz_row_1based"] - 1)
            parents = [other.GetAtomMapNum() for other in atom.GetNeighbors()]
            if parents != [row["hydrogen_attached_to_heavy_atom_id"]]:
                raise ValueError("initial XYZ hydrogen attachment mismatch")
    expected_bonds = {frozenset((bond.GetBeginAtom().GetAtomMapNum(), bond.GetEndAtom().GetAtomMapNum())): bond
                      for bond in reference_mol.GetBonds()}
    actual_bonds = {frozenset((bond.GetBeginAtom().GetAtomMapNum(), bond.GetEndAtom().GetAtomMapNum())): bond
                    for bond in mol.GetBonds() if bond.GetBeginAtom().GetSymbol() != "H" and bond.GetEndAtom().GetSymbol() != "H"}
    if set(actual_bonds) != set(expected_bonds):
        raise ValueError("initial XYZ fixed-atom connectivity mismatch")
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != "H":
            reference = reference_atoms[atom.GetAtomMapNum()]
            atom.SetFormalCharge(reference.GetFormalCharge())
            atom.SetNumRadicalElectrons(reference.GetNumRadicalElectrons())
        atom.SetNoImplicit(True)
    for key, bond in actual_bonds.items():
        bond.SetBondType(expected_bonds[key].GetBondType())
    Chem.SanitizeMol(mol)
    # Map IDs must not turn equivalent ligands (e.g. two F atoms) into stereo.
    atom_ids = [atom.GetAtomMapNum() for atom in mol.GetAtoms()]
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(0)
    Chem.AssignStereochemistryFrom3D(mol, replaceExistingTags=True)
    for atom, atom_id in zip(mol.GetAtoms(), atom_ids):
        atom.SetAtomMapNum(atom_id)
    if _canonical(mol) != _canonical(reference_mol):
        raise ValueError("initial XYZ molecular identity/stereochemistry mismatch")
    labels = accurate_cip_labels(mol)
    if Chem.MolToSmiles(Chem.RemoveHs(mol)) != Chem.MolToSmiles(reference_mol):
        raise ValueError("initial XYZ fixed-atom connectivity/stereochemistry mismatch")
    reference = accurate_cip_labels(reference_mol)
    if any(labels.get(atom_id) != label for atom_id, label in reference.items()):
        raise ValueError("initial XYZ fixed-atom stereochemistry mismatch")
    return True

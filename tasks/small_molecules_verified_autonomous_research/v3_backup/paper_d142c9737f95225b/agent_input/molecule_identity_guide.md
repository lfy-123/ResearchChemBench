# Molecule identity guide

- HL_Me: Neutral sulfur-containing ligand R=Me; SMILES `Cn1ccnc1CNCCSC`; molecular formula C8H15N3S; formal charge 0.
- HL_tBu: Neutral sulfur-containing ligand R=tBu; SMILES `Cn1ccnc1CNCCSC(C)(C)C`; molecular formula C11H21N3S; formal charge 0.
- HL_0: Neutral sulfur-free NN control ligand; SMILES `Cn1ccnc1CNCC`; molecular formula C7H13N3; formal charge 0.
- acetophenone: Acetophenone; SMILES `CC(=O)c1ccccc1`; molecular formula C8H8O; formal charge 0.
- iPrOH: Isopropanol; SMILES `CC(O)C`; molecular formula C3H8O; formal charge 0.
- acetone: Acetone; SMILES `CC(C)=O`; molecular formula C3H6O; formal charge 0.
- alcohol: 1-Phenylethanol; configuration is a reaction output; SMILES `CC(O)c1ccccc1`; molecular formula C8H10O; formal charge 0.
- KOtBu: Component representation of potassium tert-butoxide; SMILES `[K+].CC(C)(C)[O-]`; molecular formula C4H9KO; formal charge 0.
- CO: Carbon monoxide; SMILES `[C-]#[O+]`; molecular formula CO; formal charge 0.

See molecules.json for the complete stereochemical constraints, coordination descriptions and centers to be predicted. The neutral amine molecular graph may have a different charge from the oxidized state under investigation; use the electronic state explicitly specified in facts_and_conditions.json.

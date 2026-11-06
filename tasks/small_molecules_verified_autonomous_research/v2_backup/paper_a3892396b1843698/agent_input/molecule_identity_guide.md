# Molecule identity quick reference

- S: Specified neutral closed-shell starting molecule; SMILES `C=C/C=C/[C@@H]1C[C@@H]1/C=C/C=C`; molecular formula C11H14; formal charge 0.
- P1: Unranked candidate endpoint; SMILES `C1=C\C/C=C\C=C\CC/C=C/1`; molecular formula C11H14; formal charge 0.
- P2: Unranked candidate endpoint; SMILES `C=C[C@@H]1C=CCC=C[C@@H]1C=C`; molecular formula C11H14; formal charge 0.

See molecules.json for the full stereochemical constraints, coordination descriptions and centers to be predicted. A neutral amine molecular graph may differ in charge from the post-oxidation state under study; use the electronic state explicitly specified in facts_and_conditions.json.

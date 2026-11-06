# Molecule identity quick reference

- S: Specified neutral closed-shell starting molecule; SMILES `C=C/C=C/[C@@H]1C[C@@H]1/C=C/C=C`; molecular formula C11H14; formal charge 0.
- P1: Unranked candidate endpoint; SMILES `C1=C\C/C=C\C=C\CC/C=C/1`; molecular formula C11H14; formal charge 0.
- P2: Unranked candidate endpoint; SMILES `C=C[C@@H]1C=CCC=C[C@@H]1C=C`; molecular formula C11H14; formal charge 0.

See molecules.json for the full stereochemical constraints, coordination descriptions and centers to be predicted.

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. The independently generated `initial_geometry.xyz` is an unoptimized starting guess; `initial_geometry.mapping.json` maps its rows to the molecular atom IDs.

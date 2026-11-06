# Molecular identity quick reference

- A: Benzothiazole; SMILES `c1ccc2scnc2c1`; molecular formula C7H5NS; formal charge 0.
- B: Acylimidazole-substituted bicyclobutane; SMILES `Cn1ccnc1C(=O)C12CC1(c1ccccc1)C2`; molecular formula C15H14N2O; formal charge 0.
- L: (S,S)-tert-Butyl PyBOX; SMILES `CC(C)(C)[C@H]1COC(=N1)c1cccc(C2=N[C@H](CO2)C(C)(C)C)n1`; molecular formula C19H27N3O2; formal charge 0.
- P: Product connectivity; the saturated CH configuration is to be predicted; SMILES `Cn1ccnc1C(=O)C12CC(c3ccccc3)(C1)N1c3ccccc3SC12`; molecular formula C22H19N3OS; formal charge 0.
- OTf: Triflate; SMILES `O=S(=O)([O-])C(F)(F)F`; molecular formula CF3O3S-; formal charge -1.
- CHCl3: Chloroform; SMILES `ClC(Cl)Cl`; molecular formula CHCl3; formal charge 0.

See molecules.json for complete stereochemical constraints, coordination notes and prediction centers.

## Constraints that must also be satisfied

- P prediction_target: {"atom_id": 27, "quantity": "major product absolute R/S configuration", "configuration_supplied": false}

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. No initial XYZ is supplied; the molecular graphs and constraints define the starting identities.

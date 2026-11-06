# Molecule identity guide

- S: 3-Nitro-1H-pyrrole; SMILES `O=[N+]([O-])c1cc[nH]c1`; molecular formula C4H4N2O2; formal charge 0.
- RBr: Propargyl bromide; SMILES `C#CCBr`; molecular formula C3H3Br; formal charge 0.
- P: N-Propargyl-3-nitropyrrole; SMILES `C#CCn1cc([N+](=O)[O-])cc1`; molecular formula C7H6N2O2; formal charge 0.
- NaH: Ionic component representation of NaH; SMILES `[Na+].[H-]`; molecular formula HNa; formal charge 0.
- DMF: N,N-Dimethylformamide; SMILES `CN(C)C=O`; molecular formula C3H7NO; formal charge 0.

See molecules.json for the complete stereochemical constraints, coordination descriptions and centers to be predicted.

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. No initial XYZ is supplied; the molecular graphs and constraints define the starting identities.

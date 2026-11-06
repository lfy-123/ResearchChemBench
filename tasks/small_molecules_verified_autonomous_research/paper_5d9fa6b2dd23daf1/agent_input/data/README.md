# Molecular identity quick reference

- S_acid: (E)-Hex-3-enoic acid; SMILES `CC/C=C/CC(=O)O`; molecular formula C6H10O2; formal charge 0.
- AdOH: 1-Adamantanol; SMILES `OC12CC3CC(CC(C3)C1)C2`; molecular formula C10H16O; formal charge 0.
- TfOH: Triflic acid; SMILES `O=S(=O)(O)C(F)(F)F`; molecular formula CHF3O3S; formal charge 0.
- HFIP: Hexafluoroisopropanol; SMILES `OC(C(F)(F)F)C(F)(F)F`; molecular formula C3H2F6O; formal charge 0.
- S_amide: N-[(3E)-Hex-3-enyl]-p-toluenesulfonamide; SMILES `CC/C=C/CCNS(=O)(=O)c1ccc(C)cc1`; molecular formula C13H19NO2S; formal charge 0.
- P_acid: Lactone connectivity; ethyl/adamantyl groups are relatively trans; SMILES `O=C1CC(C23CC4CC(CC(C4)C2)C3)C(CC)O1`; molecular formula C16H24O2; formal charge 0.
- P_amide: Pyrrolidine connectivity; ethyl/adamantyl groups are relatively trans; SMILES `CCC1C(C23CC4CC(CC(C4)C2)C3)CCN1S(=O)(=O)c1ccc(C)cc1`; molecular formula C23H33NO2S; formal charge 0.

See molecules.json for complete stereochemical constraints, coordination notes and prediction centers.

## Constraints that must also be satisfied

- P_acid stereochemistry_constraint: "The ethyl and adamantan-1-yl groups on the ring are relatively trans. The SMILES fixes connectivity without fixing these two centers. Construct one enantiomeric representative satisfying this constraint; its overall mirror image is equally valid."
- P_acid stereo_constraints: [{"type": "relative_ring_face", "relationship": "trans", "center_atom_ids": [4, 15], "substituent_atom_ids": [5, 16], "ring_atom_ids": [2, 3, 4, 15, 18], "absolute_enantiomer_unspecified": true}]
- P_amide stereochemistry_constraint: "The ethyl and adamantan-1-yl groups on the ring are relatively trans. The SMILES fixes connectivity without fixing these two centers. Construct one enantiomeric representative satisfying this constraint; its overall mirror image is equally valid."
- P_amide stereo_constraints: [{"type": "relative_ring_face", "relationship": "trans", "center_atom_ids": [4, 3], "substituent_atom_ids": [5, 2], "ring_atom_ids": [3, 4, 15, 16, 17], "absolute_enantiomer_unspecified": true}]

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. No initial XYZ is supplied; the molecular graphs and constraints define the starting identities.

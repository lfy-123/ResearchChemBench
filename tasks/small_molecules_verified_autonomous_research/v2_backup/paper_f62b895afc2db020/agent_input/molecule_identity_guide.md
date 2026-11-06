# Molecule identity guide

- S: Cyclopentanone substituted with methoxycarbonyl and phenylallyl groups; SMILES `COC(=O)C1(CC(=C)c2ccccc2)CCCC1=O`; molecular formula C16H18O3; formal charge 0.
- P: Bicyclo[5.1.0]octane product connectivity; see the relative-configuration constraint; SMILES `COC(=O)C12CCCC(=O)CC1(c1ccccc1)C2`; molecular formula C16H18O3; formal charge 0.
- TXO: Thioxanthone; SMILES `O=C1c2ccccc2Sc2ccccc21`; molecular formula C13H8OS; formal charge 0.
- DMSO: Dimethyl sulfoxide; SMILES `CS(C)=O`; molecular formula C2H6OS; formal charge 0.

See molecules.json for the complete stereochemical constraints, coordination descriptions and centers to be predicted. The neutral amine molecular graph may have a different charge from the oxidized state under investigation; use the electronic state explicitly specified in facts_and_conditions.json.

## Constraints that must also be satisfied

- P stereochemistry_constraint: "Bicyclo[5.1.0]octane numbering: bridgehead C1 bears CO2Me and bridgehead C7 bears Ph; these two substituents lie on the same face of the three-membered ring (cis). The SMILES fixes connectivity only; cis must be imposed separately. The overall enantiomer is unspecified."
- P stereo_constraints: [{"type": "relative_ring_face", "relationship": "cis", "center_atom_ids": [12, 5], "substituent_atom_ids": [13, 3], "ring_atom_ids": [19, 12, 5], "absolute_enantiomer_unspecified": true}]

# Molecule identity guide

- S: Cyclopentanone substituted with methoxycarbonyl and phenylallyl groups; SMILES `COC(=O)C1(CC(=C)c2ccccc2)CCCC1=O`; molecular formula C16H18O3; formal charge 0.
- P_cis: Candidate cis bicyclo[5.1.0]octane product; apply the relative-configuration constraint; SMILES `COC(=O)C12CCCC(=O)CC1(c1ccccc1)C2`; molecular formula C16H18O3; formal charge 0.
- P_trans: Candidate trans bicyclo[5.1.0]octane product; apply the relative-configuration constraint; SMILES `COC(=O)C12CCCC(=O)CC1(c1ccccc1)C2`; molecular formula C16H18O3; formal charge 0.
- TXO: Thioxanthone; SMILES `O=C1c2ccccc2Sc2ccccc21`; molecular formula C13H8OS; formal charge 0.
- DMSO: Dimethyl sulfoxide; SMILES `CS(C)=O`; molecular formula C2H6OS; formal charge 0.

SMILES and atom/bond tables define connectivity. Atom IDs are local to each molecule; establish mappings when comparing states. Candidate labels identify structures, not experimental outcomes.

## Relative-configuration constraints

Both product candidates have the same connectivity. Their connectivity-only SMILES must be combined with the following constraints; neither absolute enantiomer is specified.

- P_cis: Bicyclo[5.1.0]octane numbering: bridgehead C1 bears CO2Me and bridgehead C7 bears Ph; these substituents lie on the same face of the three-membered ring (cis). The SMILES fixes connectivity only; impose the cis relative-configuration constraint for this candidate. The overall enantiomer is unspecified.
- P_cis stereo_constraints: [{"type": "relative_ring_face", "relationship": "cis", "center_atom_ids": [12, 5], "substituent_atom_ids": [13, 3], "ring_atom_ids": [19, 12, 5], "absolute_enantiomer_unspecified": true}]

- P_trans: Bicyclo[5.1.0]octane numbering: bridgehead C1 bears CO2Me and bridgehead C7 bears Ph; these substituents lie on opposite faces of the three-membered ring (trans). The SMILES fixes connectivity only; impose the trans relative-configuration constraint for this candidate. The overall enantiomer is unspecified.
- P_trans stereo_constraints: [{"type": "relative_ring_face", "relationship": "trans", "center_atom_ids": [12, 5], "substituent_atom_ids": [13, 3], "ring_atom_ids": [19, 12, 5], "absolute_enantiomer_unspecified": true}]

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. No initial XYZ is supplied; the molecular graphs and constraints define the starting identities.

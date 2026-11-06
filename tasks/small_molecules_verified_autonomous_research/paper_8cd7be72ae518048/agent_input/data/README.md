# Molecular identity quick reference

- S: 1,2-Dihydronaphthalene; SMILES `C1=CCCc2ccccc21`; molecular formula C10H10; formal charge 0.
- ArI: 4-tert-Butyliodobenzene; SMILES `CC(C)(C)c1ccc(I)cc1`; molecular formula C10H13I; formal charge 0.
- styrene: Styrene; SMILES `C=Cc1ccccc1`; molecular formula C8H8; formal charge 0.
- dippf: 1,1′-Bis(diisopropylphosphino)ferrocene; SMILES `[Fe+2].[c-]1(P(C(C)C)C(C)C)cccc1.[c-]1(P(C(C)C)C(C)C)cccc1`; molecular formula C22H36FeP2; formal charge 0.
- phenoxide: Phenoxide; SMILES `[O-]c1ccccc1`; molecular formula C6H5O-; formal charge -1.
- DABCO: 1,4-Diazabicyclo[2.2.2]octane; SMILES `C1CN2CCN1CC2`; molecular formula C6H12N2; formal charge 0.
- dba: Dibenzylideneacetone; SMILES `O=C(/C=C/c1ccccc1)/C=C/c1ccccc1`; molecular formula C17H14O; formal charge 0.
- Et2O: Diethyl ether; SMILES `CCOCC`; molecular formula C4H10O; formal charge 0.
- acetate: Acetate; SMILES `CC(=O)[O-]`; molecular formula C2H3O2-; formal charge -1.
- TBA: Tetra-n-butylammonium; SMILES `CCCC[N+](CCCC)(CCCC)CCCC`; molecular formula C16H36N+; formal charge 1.
- P_beta: Supplied β-product connectivity; SMILES `C1=C(c2ccc(C(C)(C)C)cc2)CCc2ccccc21`; molecular formula C20H22; formal charge 0.
- P_alpha: Supplied α-product connectivity; SMILES `CC(C)(C)c1ccc(C2CC=Cc3ccccc32)cc1`; molecular formula C20H22; formal charge 0.

See molecules.json for complete stereochemical constraints, coordination notes and prediction centers.

## Constraints that must also be satisfied

- dippf coordination_note: "Discrete Fe2+ and two Cp− units represent ferrocene's electron count/connectivity; each Cp coordinates to Fe through all five ring carbons, and each P is attached to one Cp carbon. Do not interpret the dot separator as free Cp in the experiment. Active Pd–phosphine coordination must be investigated separately."

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. No initial XYZ is supplied; the molecular graphs and constraints define the starting identities.

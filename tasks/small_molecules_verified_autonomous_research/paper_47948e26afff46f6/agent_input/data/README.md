# Molecule identity guide

- A: Quinoxalin-2(1H)-one; SMILES `O=c1cnc2ccccc2[nH]1`; molecular formula C8H6N2O; formal charge 0.
- B: Methyl 2-diazo-2-phenylacetate; SMILES `COC(=O)C(=[N+]=[N-])c1ccccc1`; molecular formula C9H8N2O2; formal charge 0.
- P_N: Candidate N-connected product; SMILES `COC(=O)C(c1ccccc1)n1c(=O)cnc2ccccc21`; molecular formula C17H14N2O3; formal charge 0.
- P_O: Candidate O-connected product; SMILES `COC(=O)C(c1ccccc1)Oc1cnc2ccccc2n1`; molecular formula C17H14N2O3; formal charge 0.
- DCM: Dichloromethane; SMILES `ClCCl`; molecular formula CH2Cl2; formal charge 0.

SMILES and atom/bond tables define connectivity. Atom IDs are local to each molecule; establish mappings when comparing states. Candidate labels identify structures, not experimental outcomes.

P_N and P_O differ in connectivity, not merely stereochemistry. The aryl-ester carbon is bonded to quinoxalinone N in P_N and to the oxygen attached to quinoxaline C2 in P_O. The stereochemistry at that carbon is unspecified. Electronic states and local reaction precursors are to be proposed for the computational models, rather than inferred from candidate product labels.

Construct three-dimensional conformers and reaction models from the supplied molecular graphs and constraints. No initial XYZ is supplied; the molecular graphs and constraints define the starting identities.

# Direct task inputs

Purpose: Mechanism discrimination; all states retained because the task requires calculation-backed protonation-state selection.

This directory contains 9 normal XYZ files generated independently from
the ordered generation SMILES and explicit atom-index table in `molecular_systems.json` with the chemistry-toolbox
`generate_conformer_ensemble` Action and the `rdkit_etkdg` backend. The structures
are ETKDG embeddings and have not been geometry-optimized. No author coordinate,
energy, Hessian, transition state, IRC, barrier, product endpoint, or reference
answer is present.

No experimental table is needed for this task and none is included.


The explicit P(V) ligand is methoxy (P-O-Me). Ethanol is the bulk solvent/protocol;
the coordinates do not contain an ethoxy ligand, explicit solvent, acid, or
counterion. P1/P2 are therefore bare +1/+2 molecular ions in the supplied model.


## Guided-reproduction additions

This copied raw-input set additionally contains a paper-reconstructed computational protocol, mapped pathway definitions, and workflow requirements. These files disclose methods and candidate routes but contain no published barrier, pathway ranking, author stationary-point coordinate, author IRC, or reference answer. Every numerical result must be regenerated.

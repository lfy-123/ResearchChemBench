# Direct task inputs

Purpose: P2 downstream coupling plus the supplied selectivity, non-detection, rate-series, and alcohol/ethoxide observations.

This directory contains 3 normal XYZ files generated independently from
the ordered generation SMILES and explicit atom-index table in `molecular_systems.json` with the chemistry-toolbox
`generate_conformer_ensemble` Action and the `rdkit_etkdg` backend. The structures
are ETKDG embeddings and have not been geometry-optimized. No author coordinate,
energy, Hessian, transition state, IRC, barrier, product endpoint, or reference
answer is present.

Filtered experimental observations: E01, E02, E04, E05, E06, E07, E08, E09, E10, E11, E12.


The explicit P(V) ligand is methoxy (P-O-Me). Ethanol is the bulk solvent/protocol;
the coordinates do not contain an ethoxy ligand, explicit solvent, acid, or
counterion. P1/P2 are therefore bare +1/+2 molecular ions in the supplied model.

A pre-addition phosphonium/ethanol model, the OMe/Me/H/Cl precursor series, counterions, and raw kinetic traces are not available and are not silently invented.

## Guided-reproduction additions

This copied raw-input set additionally contains a paper-reconstructed computational protocol, mapped pathway definitions, and workflow requirements. These files disclose methods and candidate routes but contain no published barrier, pathway ranking, author stationary-point coordinate, author IRC, or reference answer. Every numerical result must be regenerated.

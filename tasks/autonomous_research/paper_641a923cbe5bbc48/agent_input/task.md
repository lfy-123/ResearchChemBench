# Scientific objective

Determine the relative free energies of the three supplied conformers of isolated singly charged thiourea catalyst 7+ (Z,Z; E,Z; and Z,E) and identify the lowest conformer under a defensible, internally consistent computational model. The task is a direct computational investigation of conformer thermochemistry; do not assume that a named literature mechanism or prior ranking is correct.

# Public inputs and scientific boundaries

The directory `data/inputs` contains `zz.xyz`, `ez.xyz`, and `ze.xyz`. Each is a 45-atom Cartesian structure for isolated 7+, with element symbols in the XYZ body; use charge +1 and singlet multiplicity. The filenames and comments identify the three conformers. These are starting geometries, not result-bearing optimized structures. The scored system is the isolated cation only; nitromethane adducts, solvent populations, reaction barriers and experimental spectra are outside the scored endpoint. You may generate conformers or alter geometries during optimization, but must retain a mapping from every reported result to one of the three supplied identities.

# Required scientific validation/investigation

For each named conformer, perform a reproducible geometry optimization and a vibrational/minimum validation at a stated level of theory. Assemble a common free-energy convention and temperature for all three, state whether standard-state or other corrections were used, and report electronic, zero-point, thermal and entropic components when available. A conformer is computationally complete only when optimization converged, the frequency calculation completed, and the structure's minimum/saddle status is explicitly diagnosed. If any job fails or has imaginary frequencies, preserve that identity, report the failure and do not silently substitute another structure. Compare at least the three supplied identities; any extra conformers must be deduplicated by a stated structural criterion. Stop when all three identities have a converged thermochemical assessment or when a bounded failure prevents it; in the latter case provide the failed identities, attempted remedies and a limitation statement.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus any supporting calculation logs or coordinate files referenced by it. The JSON must include per-conformer status and thermochemical values, relative free energies with an explicit zero/reference convention, ordering if justified, validation evidence, method details, and a conclusion about the lowest conformer. Completion requires all three identities to be represented, or a truthful bounded-failure branch with the missing identities and reasons.

# Scientific objective

Determine the relative free energies of the three supplied conformers of the singly charged thiourea catalyst 7+ (Z,Z; E,Z; and Z,E) and test the authors' qualitative proposal that catalyst organization through a thiourea conformer is mechanistically important. Independently choose and justify a computational protocol; report which conformer is lowest in the chosen internally consistent comparison.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that organization of cationic thiourea catalyst 7+ through a preferred thiourea conformer is mechanistically important and use the isolated-cation conformer preference as a computational test related to their analogy with Takemoto's catalyst.

**Candidate route or mechanism.**
The authors' candidate explanation centers on comparing the Z,Z, E,Z, and Z,E thiourea configurations as distinct conformational arrangements of the isolated cation. Their broader study also considers whether substrate association can favor a different arrangement, but the present task should use that idea only to frame the isolated-conformer comparison.

**Discriminating evidence.**
The claim is tested by reproducible optimized geometries, vibrational checks for minima, and a common thermochemical comparison of electronic, zero-point, thermal, and entropic contributions. The authors also use substrate-association calculations and experimental structural evidence in the broader study, which are contextual comparisons rather than scored endpoints here.

# Public inputs and scientific boundaries

The directory `data/inputs` contains `zz.xyz`, `ez.xyz`, and `ze.xyz`. Each is a 45-atom Cartesian structure for isolated 7+, with element symbols in the XYZ body; use charge +1 and singlet multiplicity. The filenames and comments identify the three conformers. These are starting geometries, not result-bearing optimized structures. The scored system is the isolated cation only; nitromethane adducts, solvent populations, reaction barriers and experimental spectra are outside the scored endpoint. You may generate conformers or alter geometries during optimization, but must retain a mapping from every reported result to one of the three supplied identities.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

# Required scientific validation/investigation

For each named conformer, perform a reproducible geometry optimization and a vibrational/minimum validation at a stated level of theory. Assemble a common free-energy convention and temperature for all three, state whether standard-state or other corrections were used, and report electronic, zero-point, thermal and entropic components when available. A conformer is computationally complete only when optimization converged, the frequency calculation completed, and the structure's minimum/saddle status is explicitly diagnosed. If any job fails or has imaginary frequencies, preserve that identity, report the failure and do not silently substitute another structure. Compare at least the three supplied identities; any extra conformers must be deduplicated by a stated structural criterion.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus any supporting calculation logs or coordinate files referenced by it. The JSON must include per-conformer status and thermochemical values, relative free energies with an explicit zero/reference convention, ordering if justified, validation evidence, method details, and a conclusion about the qualitative author hypothesis. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

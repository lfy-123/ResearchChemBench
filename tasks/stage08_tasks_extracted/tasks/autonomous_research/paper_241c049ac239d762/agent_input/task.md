# Scientific objective

For the two fixed neutral nitroarenes in the public input, independently estimate and compare the singlet-to-triplet excitation energy. Report one gap for nitrobenzene and one for methyl 2-nitrobenzoate, the signed difference (methyl 2-nitrobenzoate minus nitrobenzene), and the ordering. Interpret what the comparison does and does not establish about differing photoinduced reactivity, without assuming a particular mechanism.

# Public inputs and scientific boundaries

`data/inputs/system.json` uniquely defines nitrobenzene and methyl 2-nitrobenzoate by canonical SMILES, names, neutral charge, and singlet/triplet multiplicities. You may generate 3-D geometries and conformers. The calculation is limited to isolated molecules or a declared continuum-solvent model. The public problem contains no author route or candidate mechanism; propose any interpretation from your own calculation and identify alternatives. Do not use the paper, SI or general web.

# Required scientific validation/investigation

For each named molecule, document connectivity and charge/multiplicity checks, geometry and conformer handling, method and basis, solvent and thermal corrections, and how singlet and triplet states are compared. Validate optimized stationary points with frequencies when optimization is performed, or provide an equivalent state/geometry quality check for a fixed-geometry calculation. Report conformer coverage and selection. Completion requires two reproducible gaps, their difference and ordering, populated validation fields, and a limitation-aware interpretation. Stop when the declared conformer/state search is exhausted; if a state fails, use the bounded-failure branch with diagnostics and do not invent a number.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-molecule gaps, signed difference, ordering, method/state/geometry disclosures, validation evidence, and an independent conclusion. Include a truthful `status` branch if one or both calculations fail.

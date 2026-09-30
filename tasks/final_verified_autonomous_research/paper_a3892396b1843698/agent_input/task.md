# Scientific objective

Independently investigate the two chemically allowed 10-electron sigmatropic rearrangements of the supplied 1,2-dibutadienecyclopropane (3a), determine validated 298.15 K Gibbs free-energy activation barriers for [3,3] and [5,5] shifts, and conclude how the channels compare. Do not assume a mechanism, transition-state geometry, conformer, or outcome before searching.

# Public inputs and scientific boundaries

`data/inputs/3a.xyz` is the complete neutral, closed-shell starting structure: 25 atoms, element labels and Cartesian coordinates in Å; atom order is fixed for reported structures. The system boundary is isolated-molecule electronic structure and Gibbs free energy at 298.15 K. Required observables are channel-specific ΔG‡ relative to 3a, validated TS character, and a comparison of the two channels. No solvent, experiment, paper, SI, or general-web lookup is allowed. You may generate conformers and models independently.

# Required scientific validation/investigation

Define a finite candidate-generation strategy for reactant conformers and both rearrangement channels, retain unique candidate identities and starting guesses, and state your deduplication rule. Optimize and validate candidates with a consistent disclosed protocol. A TS claim requires a stationary point, exactly one imaginary frequency, and a displacement/connectivity check supporting the named [3,3] or [5,5] rearrangement. Advance only candidates with documented convergence and chemical assignment; report unsuccessful or ambiguous branches. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the search plan, candidate identities, validation evidence, method and thermochemical settings, barriers in kcal/mol when available, and a final comparison. If either channel fails, use the failure branch with attempted calculations and their diagnostics rather than inventing a numeric result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

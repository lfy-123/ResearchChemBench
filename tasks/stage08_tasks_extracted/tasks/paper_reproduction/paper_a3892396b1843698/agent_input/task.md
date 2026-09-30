# Scientific objective

Independently investigate the two chemically allowed 10-electron sigmatropic rearrangements of the supplied 1,2-dibutadienecyclopropane (3a), determine validated 298.15 K Gibbs free-energy activation barriers for [3,3] and [5,5] shifts, and conclude how the channels compare. Do not assume a mechanism, transition-state geometry, conformer, or outcome before searching.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the strained 10-electron framework can undergo low-energy sigmatropic rearrangements through concerted, cyclopropyl-organized pathways, with transition-state electronic structure that may support both named channels.

**Candidate route or mechanism.**
Prioritize testing concerted [3,3] and [5,5] sigmatropic pathways using cyclopropyl-organized transition-state arrangements, while allowing the search to distinguish these from stepwise alternatives or competing electronic descriptions if the calculations indicate them. The authors considered both double-boat and double-chair conformational arrangements as candidate transition-state families.

**Discriminating evidence.**
Use optimized stationary points, vibrational analysis, displacement/connectivity checks, and consistent Gibbs free-energy comparisons to distinguish the channels and concerted versus stepwise interpretations. Electronic-structure analysis of the transition region may help assess whether the proposed pathway is supported.

# Public inputs and scientific boundaries

`data/inputs/3a.xyz` is the complete neutral, closed-shell starting structure: 25 atoms, element labels and Cartesian coordinates in Å; atom order is fixed for reported structures. The system boundary is isolated-molecule electronic structure and Gibbs free energy at 298.15 K. Required observables are channel-specific ΔG‡ relative to 3a, validated TS character, and a comparison of the two channels. No solvent, experiment, paper, SI, or general-web lookup is allowed. You may generate conformers and models independently.

# Required scientific validation/investigation

Define a finite candidate-generation strategy for reactant conformers and both rearrangement channels, retain unique candidate identities and starting guesses, and state your deduplication rule. Optimize and validate candidates with a consistent disclosed protocol. A TS claim requires a stationary point, exactly one imaginary frequency, and a displacement/connectivity check supporting the named [3,3] or [5,5] rearrangement. Advance only candidates with documented convergence and chemical assignment; report unsuccessful or ambiguous branches. Stop when your stated conformer/starting-guess coverage is exhausted or repeated additions yield no new validated stationary point, and report that coverage and any remaining uncertainty. Completion requires either validated barriers for both channels or a bounded-failure report that makes clear why a channel could not be established.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the search plan, candidate identities, validation evidence, method and thermochemical settings, barriers in kcal/mol when available, and a final comparison. If either channel fails, use the failure branch with attempts and limitations rather than inventing a numeric result.

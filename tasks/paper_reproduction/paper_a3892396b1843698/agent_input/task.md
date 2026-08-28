# Scientific objective

Using the supplied neutral 25-atom 1,2-dibutadienecyclopropane (3a) geometry, independently determine the 298.15 K Gibbs free-energy activation barriers for its [3,3] and [5,5] sigmatropic shifts. The authors qualitatively proposed that the strained 10-electron system can use concerted, cyclopropyl-organized pathways; test that proposal computationally without assuming a particular transition-state geometry or result.

# Public inputs and scientific boundaries

`data/inputs/3a.xyz` is the complete neutral, closed-shell starting structure: 25 atoms, element labels and Cartesian coordinates in Å. Treat atom order as fixed for any reported structures. The system boundary is the isolated molecule and its electronic plus thermal Gibbs free energy at 298.15 K; no solvent, experiment, or rate constant is required. The measured quantities are ΔG‡ for each named rearrangement relative to the same 3a reference, TS vibrational character, and the comparison between channels. You may generate conformers and computational models, but do not use the paper, SI, general web, or hidden reference values.

# Required scientific validation/investigation

Plan and execute a defensible independent electronic-structure workflow. Locate and optimize candidate reactant, [3,3]-shift TS, and [5,5]-shift TS structures, and compute thermochemistry on a consistent reference. Assign a TS only when it is a stationary point with exactly one imaginary frequency whose displacement is chemically consistent with the named rearrangement; report failed or ambiguous searches instead of fabricating a value. Deduplicate equivalent candidates by connectivity and geometry and explain which validated candidate is used for each channel. The investigation is complete when both named channels have either a validated barrier or a documented bounded failure after your disclosed search attempts; stop when additional starting guesses/conformer searches no longer produce a new validated candidate under your stated coverage rule. Report method, software, convergence, frequency and thermal settings, and any limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include provenance for every numerical value, candidate identity and validation evidence. A successful branch must give both barriers in kcal/mol and the TS checks; a bounded-failure branch must identify the failed channel, attempts and scientifically meaningful limitation. Also include a concise conclusion comparing the channels and whether the qualitative author hypothesis is supported.

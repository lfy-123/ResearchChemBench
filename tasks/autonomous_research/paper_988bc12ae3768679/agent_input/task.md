# Scientific objective

Determine, by independent computation, whether the two supplied protonation-state structures of dye 2a have distinguishable gas-phase low-lying singlet absorption profiles. Report S1–S4 excitation energies and oscillator strengths for each named structure, identify each brightest state, compare the profiles, and give a scoped scientific conclusion. Formulate and discriminate plausible electronic explanations from your calculations; no author mechanism, candidate ranking, or expected result is provided.

# Public inputs and scientific boundaries

Use `data/inputs/2a-acid.xyz` and `data/inputs/2a-base.xyz`. Each is a complete SI Cartesian geometry in angstroms: 62 atoms for acid and 58 atoms for base. Treat acid as formal charge +2, singlet multiplicity 1, and base as formal charge −2, singlet multiplicity 1. The systems are isolated gas-phase molecules and the scored endpoint is vertical S0-to-singlet excitation from the supplied geometries. Do not add solvent, counterions, vibronic structure, experimental band fitting, or NMR calculations to the scored endpoint. You may optimize or verify geometries, but disclose any change. Measure S1–S4 excitation energies in eV and dimensionless oscillator strengths for each named structure.

# Required scientific validation/investigation

Choose and disclose a defensible independent computational route. Validate input identity, atom count, charge, multiplicity, geometry provenance, convergence, and four-state coverage for each object. Select each brightest state by the largest oscillator strength among its own S1–S4 results and retain state identity and evidence. Explain which plausible electronic interpretation is supported by the computed comparisons, while separating calculation from inference and experiment. Completion requires both endpoint calculations and validation, or a bounded-failure record naming the failed object, diagnostic, attempted coverage, and limitation. Stop when both structures have been treated and the comparison is validated; do not expand into solvent or unrelated protonation states.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with method disclosure, per-structure validation, per-state results or truthful bounded-failure branches, brightest-state selectors, independent comparison/conclusion, and limitations. Supporting outputs may be placed under `report/`; do not include source-paper text or evaluator references.

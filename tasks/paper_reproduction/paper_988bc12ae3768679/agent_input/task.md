# Scientific objective

Independently test the authors' qualitative proposal that acid/base protonation of phenolic dye 2a changes its electronic absorption profile. Calculate vertical low-lying singlet excitations for the supplied 2a-acid and 2a-base S0 geometries, report excitation energies (eV) and oscillator strengths, identify the brightest state in each four-state set, and explain whether the profiles support a bathochromic acid/base switch. The author hypothesis is disclosed only as a qualitative route: protonation/deprotonation changes the electronic structure and hence the absorption; do not assume any numerical result or state ordering.

# Public inputs and scientific boundaries

Use `data/inputs/2a-acid.xyz` and `data/inputs/2a-base.xyz`. Each is an XYZ file in angstroms containing the complete SI S0 geometry: 62 atoms for 2a-acid and 58 atoms for 2a-base. Treat acid as formal charge +2, singlet multiplicity 1, and base as formal charge −2, singlet multiplicity 1. The systems are isolated molecules in the gas phase. The endpoint is vertical electronic excitation from these supplied geometries; do not add solvent, counterions, vibronic structure, experimental band fitting, or NMR calculations to the scored endpoint. You may optimize or verify geometries, but must disclose any change. The measured objects are S1–S4 singlet excitation energies and dimensionless oscillator strengths for each named structure.

# Required scientific validation/investigation

Plan and execute a defensible electronic-structure calculation, independently choosing software and model chemistry and disclosing them. Validate atom count, element order, charge, multiplicity, geometry provenance, convergence, and that at least four singlet states were computed for each named structure. Select the brightest state as the member of that structure's S1–S4 set having the largest oscillator strength; retain state labels and per-state evidence rather than reporting only an aggregate. Compare the two profiles and state whether the calculated evidence supports the qualitative switching hypothesis, distinguishing gas-phase vertical excitation from experiment. Completion requires both structures, all four states (or a clearly documented bounded failure), explicit validation evidence, and a conclusion. Stop after both endpoint calculations and validation are complete; if a calculation cannot be completed, stop after recording the failed object, diagnostic, attempted coverage, and scientifically justified limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus any referenced calculation outputs or scripts under `report/`. The JSON must include method disclosure, per-structure validation, four-state results when available, brightest-state selectors, comparison/conclusion, and limitations. Do not copy the paper or SI into the report.

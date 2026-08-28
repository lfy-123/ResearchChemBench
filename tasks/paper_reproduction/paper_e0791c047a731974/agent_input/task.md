# Scientific objective

Independently plan and execute calculations that test the authors' qualitative hypothesis that heavy-atom engineering of cyanine sensitizers can enhance triplet formation. For the named Cy2 cation, determine the vertical S1, T1 and T2 excitation energies and the relaxed T1 adiabatic energy in chloroform, then assess whether the computed state energetics support an energetically viable triplet-sensitizer interpretation. Do not assume the authors' numerical method or result values.

# Public inputs and scientific boundaries

The sole molecular input is `data/inputs/cy2_s0.xyz`, the 120-atom Cy2 cation S0 Cartesian geometry extracted from SI Section 5. The XYZ comment records the charge (+1), singlet starting multiplicity (1), and omission of iodide counterions. The research object is this same Cy2 connectivity and protonation state; do not add counterions or alter connectivity. Chloroform is the solvent boundary, represented by a defensible continuum or explicit-solvent model. The measured quantities are S1, T1 and T2 vertical excitation energies from S0, and the T1 adiabatic energy relative to S0, all in eV. You may choose software, functional, basis, solvation treatment and convergence settings, but report them.

# Required scientific validation/investigation

Establish the input identity and charge/multiplicity, optimize or otherwise validate the S0 geometry, and report whether the final S0 is stationary; if a frequency calculation is performed, report imaginary frequencies. Generate and identify S1, T1 and T2 without confusing vertical and relaxed states. Obtain a triplet T1 relaxed geometry and an energy difference relative to S0, preserving state multiplicity and documenting convergence. Check state ordering, the inequality 2×T1>S1, and the S1–T2 gap, and explain whether these checks support the proposed triplet-sensitizer hypothesis. A calculation is complete when all requested states have identifiable energies or a scientifically justified bounded failure is reported with logs and limitation. Stop after the fixed endpoint is validated and all requested observables are either obtained or explicitly unresolved; do not broaden to other cyanines.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus calculation inputs/logs sufficient to audit geometry, charge, multiplicity, state identity, convergence and energy references. Include a concise conclusion and limitations. If a requested state cannot be obtained, use the schema's bounded-failure branch and identify the missing observable rather than inventing a number.

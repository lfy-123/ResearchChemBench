# Scientific objective

For the specified periodic HoH3 crystal, independently determine its dynamical behavior at 0 K in the harmonic approximation and under a finite-temperature simulation or thermal effective-force-constant analysis. Establish whether the structure persists over the sampled finite-temperature interval and explain what the combined evidence does and does not imply about ambient-phase stability. The measured objects are harmonic phonon frequencies, finite-temperature dynamical observables, and a clearly defined structural-retention metric.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that cubic fcc HoH3 can show a harmonic dynamical instability at 0 K while remaining dynamically persistent at finite temperature, with anharmonic thermal motion stabilizing the retained structure. This is a qualitative dynamical claim and does not by itself establish thermodynamic stability.

**Candidate route or mechanism.**
A focused test is to compare the 0 K harmonic phonon spectrum with temperature-renormalized force-constant or phonon descriptions and to assess whether finite-temperature atomic motion retains the cubic structure. The relevant candidate explanation is stabilization of modes that are unstable in the harmonic limit through thermal anharmonicity; a competing explanation is finite-time persistence without full dynamical stabilization.

**Discriminating evidence.**
Discriminate these explanations using the sign and extent of harmonic phonon frequencies, finite-temperature renormalized phonons, trajectory-based structural-retention and phase-change metrics, and sensitivity across temperature, sampling duration, or numerical settings. Interpret the absence of an observed transition over a finite sample as persistence under those conditions rather than proof of absolute stability.

# Public inputs and scientific boundaries

Use `data/inputs/fcc_HoH3_POSCAR`, a unique 16-atom conventional cubic cell containing 4 Ho and 12 H (HoH3), lattice parameter 5.245 Å, with Ho at the fcc 4a positions, H at octahedral 4b and tetrahedral 8c positions. Treat it as a neutral periodic crystal at 0 GPa. You may generate supercells and computational models. The scored system is the isolated periodic HoH3 crystal; do not add a host or solvent. Do not score formation energies, convex-hull position, synthesis history, or electronic structure.

# Required scientific validation/investigation

Plan and execute an independent route that addresses both the harmonic and finite-temperature endpoints. Define candidate numerical settings, deduplicate equivalent analyses, and advance only analyses that report reproducible phonon/trajectory observables. Validate the harmonic result with a frequency-sign convention and convergence or supercell check. Validate finite-temperature persistence with an explicit structural-retention or phase-change criterion, sampled temperature and duration, and at least one sensitivity check. Completion requires a defensible answer for both endpoints or a bounded-failure report with the attempted scope, missing endpoint, and reason; stop when endpoint analyses, sensitivity evidence, coverage, and limitations are documented.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Report the independent method and search/analysis scope, exact object identity, observables, validation evidence, uncertainty/limitations, and conclusion. Any bounded failure must retain the attempted settings and explain how the missing endpoint prevents a stronger conclusion.

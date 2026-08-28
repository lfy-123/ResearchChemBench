# Scientific objective

Independently calculate and compare the neutral-singlet ground-state geometries, HOMO and LUMO energies, and internal hole reorganization energies of the three named fluorinated carbazole–diphenylamine HTMs JY1, JY2, and JY3. The authors' qualitative hypothesis is that fluorine substitution tunes frontier levels and reorganization energy; test that hypothesis without assuming any numerical outcome or winning structure.

# Public inputs and scientific boundaries

`data/inputs/molecules.json` is the complete system definition: each systematic name, formula, charge, multiplicity, identifier, and fluorine count is explicit. Build starting geometries yourself. The measured objects are isolated molecules only; do not score crystal packing, perovskite adsorption, optical spectra, hopping pathways, mobility, or device performance. Report energies in eV and retain atom identity/connectivity in every geometry artifact.

# Required scientific validation/investigation

For each named molecule, choose and justify a computational approach, generate at least one connectivity-preserving 3-D starting structure, optimize a neutral singlet ground state, and compute a vibrational Hessian or equivalent minimum test. A candidate is advanced only if connectivity and charge/multiplicity remain correct and the minimum test has no imaginary mode (or any exception is explicitly diagnosed). Extract HOMO/LUMO from the same validated state. Compute internal hole reorganization energy from clearly documented neutral/cation adiabatic or four-point energies, defining the convention and all states used. Completion requires all three molecules to have either validated values or a bounded, technically justified failure record; a failed molecule must report attempted approaches and its reason rather than fabricated values. Stop after the three named systems and all required validation attempts are covered; do not expand to unlisted analogues. Report convergence settings, software, model, conformer handling, failures, and limitations.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-molecule geometry identity, optimization/minimum evidence, HOMO/LUMO, λh (or an explicit bounded-failure branch), methods and a comparative conclusion.

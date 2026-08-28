# Scientific objective

Determine whether stoichiometric cubic fcc-HoH3 at 0 GPa is dynamically unstable in the 0-K harmonic limit yet dynamically persistent at finite temperature, and evaluate whether the evidence supports the authors' qualitative hypothesis that anharmonic thermal motion stabilizes the retained phase. The measured objects are the harmonic phonon spectrum, finite-temperature renormalized phonon spectrum, and finite-temperature trajectory stability.

# Public inputs and scientific boundaries

Use `data/inputs/fcc_HoH3_POSCAR`, a unique 16-atom conventional cubic cell containing 4 Ho and 12 H (HoH3), lattice parameter 5.245 Å, with Ho at the fcc 4a positions, H at octahedral 4b and tetrahedral 8c positions. Treat the structure as periodic, neutral, and at 0 GPa. You may generate supercells and displaced structures. The task does not score thermodynamic hull energies, synthesis conditions, electronic properties, or any particular software/model chemistry. You may choose a defensible computational implementation, but disclose method, convergence, supercell, temperature, trajectory length, and analysis definitions.

# Required scientific validation/investigation

Compute or otherwise obtain a harmonic phonon result and a finite-temperature dynamical result for this exact structure. Validate the harmonic result by reporting the frequency convention and whether imaginary modes occur, including their extent or representative minimum. Validate finite-temperature persistence with a trajectory or equivalent temperature-renormalized phonon analysis and an explicit structural-collapse/phase-change criterion. A successful investigation must identify the sampled temperature and time or other sampling domain, test numerical convergence or sensitivity at least once, and distinguish finite-time persistence from proof of absolute stability. Completion requires both limits to be analyzed or a bounded-failure report explaining which endpoint could not be computed and why; stop when the two endpoint analyses, one sensitivity check, and all required evidence are documented.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the chosen method, object identity, harmonic and finite-temperature observables, validation evidence, limitations, and a concise conclusion. Attach or reference machine-readable phonon/trajectory summaries when available; do not report unsupported precision.

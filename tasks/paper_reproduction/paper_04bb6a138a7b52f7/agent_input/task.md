# Scientific objective

Independently test the paper's qualitative proposal that oPmPCZ can access higher triplet states through hRISC. Compute the neutral molecule's optimized S0 geometry, vertical S1/T1/T6/T7 energies, ΔE(S1−T1), and SOC magnitudes |SOC(S1,T1)|, |SOC(S1,T6)| and |SOC(S1,T7)|. The author hypothesis is only a hypothesis: do not assume its result or state ordering.

# Public inputs and scientific boundaries

Use `data/inputs/molecule_identity.json`. It identifies one neutral, closed-shell oPmPCZ molecule (C44H28N4; charge 0; multiplicity 1) by its full name, and gives CCDC 2466817 as a controlled identity record for connectivity. Retrieve connectivity only; do not use a deposited crystal geometry as the calculated structure. Generate starting conformers yourself. The physical boundary is one isolated gas-phase molecule. Solvent, crystal packing, OLED layers, experimental spectra, and rate modelling are outside scope. At the same optimized S0 geometry, S1 means the lowest vertical singlet excited state and T1, T6, and T7 mean the first, sixth, and seventh vertical triplet roots in ascending energy within the reported calculation. The measured quantities are vertical energies in eV and SOC magnitudes in cm^-1, with the coupling convention stated.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure workflow independently. Optimize S0, report its Cartesian coordinates, and document charge, multiplicity, convergence, and whether a frequency/stationarity check was performed. Calculate enough singlet and triplet states to identify S1, T1, T6 and T7; retain excitation energies and state-indexing evidence, and explain any reordering or alternative assignment. Compute all three S1–Tn SOC magnitudes and state the SOC convention/software/settings. The investigation is complete when one internally consistent geometry/state assignment has converged and all eight electronic observables plus provenance are reported. If convergence or state identity cannot be established, submit a bounded limited report documenting the attempted workflow, failed validation, affected object, and missing observables without fabricating numbers or conclusions.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Complete reports include method provenance, optimized-geometry coordinates and validation, state-indexing evidence, the eight electronic observables with units, and a conclusion about whether the author's qualitative HLCT/hRISC hypothesis is supported. Limited reports include provenance and validation, omit unavailable geometry or observables, and state why the hypothesis cannot be assessed. Do not quote or search the paper for the numerical answer.

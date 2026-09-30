# Scientific objective

For the uniquely identified molecule oPmPCZ, determine computationally whether its low-lying singlet/triplet electronic structure and spin–orbit couplings are consistent with efficient access from S1 to higher triplet states. Compute the optimized S0 geometry, vertical S1/T1/T6/T7 energies, ΔE(S1−T1), and |SOC(S1,T1)|, |SOC(S1,T6)| and |SOC(S1,T7)|, then state the evidence-supported conclusion and limitations. Generate and test your own physical explanations, and formulate any mechanistic interpretation from the calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that hybridized local and charge-transfer (HLCT) character and higher-lying-triplet reverse intersystem crossing (hRISC) could enable triplet harvesting in oPmPCZ.

**Candidate route or mechanism.**
Consider hRISC from T6 or T7 to S1, compared with thermally activated reverse intersystem crossing from T1 to S1. Assess whether energetic proximity and differences in electronic character make these higher-triplet channels plausible.

**Discriminating evidence.**
The authors use excited-state energy calculations to compare singlet–triplet separations, natural transition orbital analysis to examine local/charge-transfer character and differences between states, and spin–orbit coupling calculations to compare S1 coupling to T1, T6, and T7.

# Public inputs and scientific boundaries

Use `data/inputs/molecule_identity.json`. It identifies one neutral, closed-shell oPmPCZ molecule (C44H28N4; charge 0; multiplicity 1) by its full name, and gives CCDC 2466817 as a controlled identity record for connectivity. Retrieve connectivity only; do not use a deposited crystal geometry as the calculated structure. Generate starting conformers yourself. The physical boundary is one isolated gas-phase molecule. Solvent, crystal packing, OLED layers, experimental spectra, and rate modelling are outside scope. At the same optimized S0 geometry, S1 means the lowest vertical singlet excited state and T1, T6, and T7 mean the first, sixth, and seventh vertical triplet roots in ascending energy within the reported calculation. The measured quantities are vertical energies in eV and SOC magnitudes in cm^-1, with the coupling convention stated.

# Required scientific validation/investigation

Plan and execute an independent electronic-structure investigation. Optimize S0, report its Cartesian coordinates, and document charge, multiplicity, convergence, and whether a frequency/stationarity check was performed. Calculate enough singlet and triplet states to identify S1, T1, T6 and T7; retain excitation energies and state-indexing evidence, and explain any reordering or alternative assignment. Compute all three S1–Tn SOC magnitudes and state the SOC convention/software/settings. The investigation is complete when one internally consistent geometry/state assignment has converged and all eight electronic observables plus provenance are reported. If convergence or state identity cannot be established, submit a bounded limited report documenting the attempted workflow, failed validation, affected object, and missing observables without fabricating numbers or conclusions.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Complete reports include method provenance, optimized-geometry coordinates and validation, state-indexing evidence, the eight electronic observables with units, and a conclusion about the physical interpretation. Limited reports include provenance and validation, omit unavailable geometry or observables, and state why interpretation cannot be resolved. If the hypothesis space is not uniquely resolved, report the competing interpretation and exact missing validation; do not invent a discovery story.

# Scientific objective

For the named Cy2 cation, determine the vertical S1, T1 and T2 excitation energies and the relaxed T1 adiabatic energy in chloroform, then interpret their ordering and separations in the context of triplet sensitization. Do not assume the authors' numerical method or result values.

# Author-provided scientific guidance

The authors propose that heavy-atom engineering of cyanine sensitizers can enhance triplet formation. Use this as context for interpreting the calculated Cy2 singlet/triplet energies; no direction or magnitude of the energy gaps is supplied.

This task tests the state-energetic component of that proposal, not the enhancement of SOC or ISC rates itself. Independently choose and validate an energy-calculation route; a separate SOC matrix-element or ISC-rate calculation is not required.

# Public inputs and scientific boundaries

Use electronic energies consistently: vertical EX = E(X; RS0) − E(S0; RS0) for S1, T1 and T2 at the same S0 geometry; adiabatic T1 = E(T1; RT1) − E(S0; RS0) at their respective relaxed geometries. Do not add ZPE or thermal/free-energy corrections to these electronic gaps. For the S1−T1 and T2−S1 gaps, use the vertical energies at the same S0 geometry. Identify triplet state/spin within the chosen method; a triplet-response method need not use a triplet reference determinant. The optional Cy2 diagnostic 2×T1−S1 may be reported, but it is not a criterion for sensitization.

The sole molecular input is `data/inputs/cy2_s0.xyz`, the 62-atom Cy2 cation S0 Cartesian geometry extracted from SI Section 5. The XYZ comment records the charge (+1), singlet starting multiplicity (1), and omission of iodide counterions. The research object is this same Cy2 connectivity and protonation state; do not add counterions or alter connectivity. Chloroform is the solvent boundary, represented by a defensible continuum or explicit-solvent model. The measured quantities are S1, T1 and T2 vertical excitation energies from S0, and the T1 adiabatic energy relative to S0, all in eV. You may choose software, functional, basis, solvation treatment and convergence settings, but report them.

# Required scientific validation/investigation

Establish the input identity and charge/multiplicity, optimize or otherwise validate the S0 geometry, and report whether the final S0 is stationary; if a frequency calculation is performed, report imaginary frequencies. Generate and identify S1, T1 and T2 without confusing vertical and relaxed states. Obtain a triplet T1 relaxed geometry and an energy difference relative to S0, preserving state multiplicity and documenting convergence. Report state ordering and the vertical S1−T1 and T2−S1 gaps in `validation.checks`, and explain the state-energetic findings relevant to the proposal. Completion requires the four requested energies and their validation, not an affirmative claim of enhanced SOC/ISC or a separate quantum-yield or annihilator calculation. Otherwise submit a failure/partial report with logs and the specific failure cause.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`, plus calculation inputs/logs sufficient to audit geometry, charge, multiplicity, state identity, convergence and energy references. Include a concise conclusion. If a requested state cannot be obtained, use the schema's bounded-failure branch and identify the missing observable rather than inventing a number.

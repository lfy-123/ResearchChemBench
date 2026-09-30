# Scientific objective

For the specified selenium-containing heptamethine cyanine cation Cy2, independently determine the low-lying excited-state energetics relevant to 830 nm triplet–triplet-annihilation sensitization. Compute or otherwise defensibly estimate vertical S1, T1 and T2 energies from S0 and the relaxed T1 adiabatic energy in chloroform, validate state identities and convergence, and conclude what the energetics do and do not establish about triplet sensitization.

# Public inputs and scientific boundaries

Use electronic energies consistently: vertical EX = E(X; RS0) − E(S0; RS0) for S1, T1 and T2 at the same S0 geometry; adiabatic T1 = E(T1; RT1) − E(S0; RS0) at their respective relaxed geometries. Do not add ZPE or thermal/free-energy corrections to these electronic gaps. For the S1−T1 and T2−S1 gaps, use the vertical energies at the same S0 geometry. Identify triplet state/spin within the chosen method; a triplet-response method need not use a triplet reference determinant. The optional Cy2 diagnostic 2×T1−S1 may be reported, but it is not a criterion for sensitization.

The sole molecular input is `data/inputs/cy2_s0.xyz`, the 62-atom Cy2 cation S0 Cartesian geometry extracted from SI Section 5. The XYZ comment specifies charge +1, singlet multiplicity 1 and omission of iodide counterions. Use this connectivity, protonation and charge exactly; do not add counterions or change the molecule. Chloroform is the solvent boundary, represented by a defensible continuum or explicit-solvent model. Requested observables are vertical S1, T1 and T2 energies from S0 and relaxed T1 adiabatic energy relative to S0, in eV. Method and software choices are open, but must be reported and justified.

# Required scientific validation/investigation

Validate the molecular identity and starting electronic state, then establish a stationary S0 geometry and report frequency evidence when available. Identify S1, T1 and T2 explicitly and distinguish vertical energies from relaxed-state energies. Relax the triplet T1 state with an appropriate state-specific treatment (an unrestricted triplet determinant or triplet-response optimization) and document convergence and the S0 reference used for the adiabatic gap. Report state ordering and the vertical S1−T1 and T2−S1 gaps in `validation.checks`, and formulate an energetic interpretation from these results. Completion requires the four requested energies and their validation, not a separate SOC, ISC-rate, quantum-yield or annihilator calculation. Incomplete work is submitted with evidence-backed diagnostics and logs.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`, with auditable inputs/logs and a concise conclusion. Include method choices, convergence/state evidence, energy references. If a requested state fails, use the bounded-failure branch and name the unresolved observable instead of fabricating a value.

# Scientific objective

Determine harmonic low-frequency lateral Y2 modes of Y2@Ih-C80(CH2Ph) and Y2@D5h-C80(CH2Ph), compare frequencies, and assess spin-lattice-relaxation implications. Lateral means substantial Y2 displacement parallel to the cage inner surface, not Y-Y-axis or framework motion. Atoms 81 and 82 (one-based XYZ atom records, excluding the two header lines) are Y; verify element labels rather than relying on an unverified index.

# Public inputs and scientific boundaries

Assign physical modes before comparing frequencies. With Cartesian displacement u and mass m, report Y participation sum_Y(m|u|²)/sum_all(m|u|²); for the Y–Y unit vector a, a useful transverse fraction is sum_Y[m(|u|²−(u·a)²)]/sum_Y(m|u|²). If the program prints mass-weighted eigenvectors, convert consistently. Use these measures and mode vectors to distinguish transverse Y motion from longitudinal/cage motion; disclose your criterion rather than selecting frequencies closest to an expected value. For each isomer put exactly four distinct, physically assigned primary lateral modes in `modes`; use their native `mode_id` values once each. Put any other examined or mixed candidates in optional `additional_modes`, with assignment evidence explaining why they are not in the primary set. There is no limit on exploration; this separates the four-mode comparison from additional candidates. Sort the identity-assigned primary set only for final pairing. If four primary modes cannot be assigned, report partial/failure rather than inventing or duplicating modes. A numerical spin-lattice T1 calculation is not required.

`data/inputs/y2_ih.xyz` and `data/inputs/y2_d5h.xyz` are explicit 96-atom XYZ geometries (87 C, 7 H, 2 Y), Angstrom. Use isolated neutral charge 0, multiplicity 2. No paper/SI/web/database access. Report cm-1 frequencies and assignment evidence. State software/model chemistry/settings.

# Required scientific validation/investigation

Analyze both fixed geometries with an independent frequency calculation or validated equivalent. Verify atoms, charge, spin, convergence and imaginary frequencies. For every selected mode report identity, frequency and Y2 lateral evidence; explain exclusion of longitudinal/framework modes. Report per-isomer lists, comparison statistic, direction. If failure occurs, report bounded failure with diagnostics and partial results. Completion requires both inputs analyzed and a reproducible assignment/comparison record.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`, with method, validation, per-isomer modes, comparison, interpretation and artifact paths.

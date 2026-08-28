# Scientific objective

Determine harmonic low-frequency lateral Y2 modes of Y2@Ih-C80(CH2Ph) and Y2@D5h-C80(CH2Ph), compare frequencies, and assess spin-lattice-relaxation implications. Lateral means substantial Y2 displacement parallel to the cage inner surface, not Y-Y-axis or framework motion. Atoms 88 and 89 are Y.

The authors qualitatively propose that cage isomerism changes the Y2-motion potential surface and lateral modes help explain T1 differences; independently test this.

# Public inputs and scientific boundaries

`data/inputs/y2_ih.xyz` and `data/inputs/y2_d5h.xyz` are explicit 96-atom XYZ geometries (87 C, 7 H, 2 Y), Angstrom. Use isolated neutral charge 0, multiplicity 2. No paper/SI/web/database access. Report cm-1 frequencies and assignment evidence. State software/model chemistry/settings.

# Required scientific validation/investigation

Analyze both fixed geometries with an independent frequency calculation or validated equivalent. Verify atoms, charge, spin, convergence and imaginary frequencies. For every selected mode report identity, frequency and Y2 lateral evidence; explain exclusion of longitudinal/framework modes. Report per-isomer lists, comparison statistic, direction and limitations. If failure occurs, report bounded failure with diagnostics and partial results. Completion requires both inputs analyzed and a reproducible assignment/comparison record; stop then.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with method, validation, per-isomer modes, comparison, interpretation, limitations and artifact paths.

# Scientific objective

Test whether cyano-induced molecular polarization explains excited-state charge separation across explicit H-capped phenylene–thiophene oligomers, and whether the relationship survives chain length, torsion and a fixed-cyano-count regiochemical counterexample.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. These finite neutral-singlet oligomers alternate para-phenylene and 2,5-thiophene with identical H end caps. They are not the dibrominated monomer reagents or a periodic polymer. Molecular dipoles and excitation descriptors cannot establish hydrogen-production rate or bulk carrier transport. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Nine explicit oligomers and independent excited observables.** Calculate all three substitution levels at n=1,2,3 with the same caps, method and state definition. Validate minima and conformer/torsion coverage. Compute dipole/ESP and independent electron-hole separation/overlap; do not infer charge separation from polarization alone.

2. **Same-count counterexample and common-torsion comparison.** Verify the two same-formula graphs differ in cyano position, then compare at relaxed and identical inter-ring torsions. Attribute any difference to the specified regio/twist intervention while acknowledging state-character changes. Supply all matched atom maps and NTO evidence.

3. **Frozen short-chain explanation challenged by n=3.** Freeze an explicit ordering or quantitative relationship using n<=2 before testing all n=3 members. State prediction residual/rank success and whether the regio control falsifies a dipole-only explanation. Do not claim polymer-length convergence from three short chains.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Bulk carrier separation and hydrogen-production rates are outside the finite-oligomer task.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.

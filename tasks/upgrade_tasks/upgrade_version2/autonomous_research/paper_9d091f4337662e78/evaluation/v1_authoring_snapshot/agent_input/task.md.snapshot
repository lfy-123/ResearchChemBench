# Scientific objective

Determine the supported absolute-configuration set at mapped stereocenter17 of compound1 from independently searched R/S conformer ensembles and experimental ECD, using a held-out spectral band and explicit sampling/broadening uncertainty.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. The known connectivity and E alkene are fixed; stereocenter17 is the only unresolved absolute label. The two enantiomers in achiral methanol are separate hypotheses, not one Boltzmann equilibrium. No author conformers, assignment or computed ECD are public. Digitized experimental observations have finite plot-reading precision. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Independent R/S coverage and normalized ensembles.** Search both configurations independently, show per-seed generation/deduplication, refine all retained conformers and document excluded populations. Supply geometries, G values, degeneracy and weights normalized within each configuration. Validate stereochemistry and minima. Conformer collapse is deduplicated, not artificially counted.

2. **Recomputable spectra and mirror control.** Provide per-conformer transition/rotatory strengths, weighted spectrum and analysis code under one convention. Verify a mirror pair has matching energy and opposite rotatory sign within numerical convergence. Never average R and S populations into one spectrum or choose the sign from the known label.

3. **Heldout band and uncertainty-supported candidate set.** Compare both frozen ensemble predictions against the heldout experimental band; compute residual/sign diagnostics across cutoff and broadening perturbations. Account separately for digitization and model errors. A two-member support set is valid only after the required searches and comparisons, not as a substitute for them.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Other natural products, synthetic routes and pharmacology are outside this version.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.

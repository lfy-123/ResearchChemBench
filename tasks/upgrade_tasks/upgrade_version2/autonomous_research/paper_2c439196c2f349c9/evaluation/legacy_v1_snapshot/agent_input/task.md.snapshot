# Scientific objective

Test instantaneous electronic, thermal-memory and mixed models against the same time/power observations for the INP solutions under the reported experimental conditions, and determine whether their contributions are identifiable.

# Public inputs and scientific boundaries

Use the source INP solution concentrations 0.25, 0.50 and 1.0 mM, CW 532 nm, 1 mm cell, with 50 mW temporal SSPM and power scans up to 150 mW. These are solution conditions; do not pool the separate 0.4 mm PMMA film. Source experimental solvent and beam/thermal quantities must be carried from a verified data table; no aqueous solvent is inferred from the dye name. The old isolated-molecule frontier gap is optional background only. fig10_measured_markers.csv supplies 27 visually digitized discrete temporal markers, with pixel coordinates and provenance in fig10_digitization_provenance.json. Its +/-4 pixel reading bounds are digitization uncertainty only; measurement uncertainty remains unknown. These rows are not fitted-curve samples and do not resolve the missing power/Z-scan/calibration input gate.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **All three physical models share the same measured observation rows, concentration/path-length/absorption/beam definitions and measurement uncertainty. Fit data and held-out conditions are disjoint; no synthetic or interpolated points count as measurements.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

**Development input gate: blocked.** Figure 10 now has 27 traceable discrete temporal marker rows with pixel-reading bounds. Independent power/intensity and Z-scan measurement rows from the remaining figures, with defensible experimental/digitization errors, remain missing. Fitted curves and fitted time constants are not independent observations. The available source text does not establish a complete calibrated SSPM beam-waist, instrument-response and thermal-parameter dataset. Obtain measurement/plot digitization with bounded parameter provenance before completing model discrimination. A current bounded-failure submission can document this gate, but cannot earn scientific completion. The full contract below remains the release requirement; it has not been weakened to make the blocked input pass.

# Required scientific validation/investigation

1. **Verified observation and physical-parameter table** Assemble and validate a measurement table with provenance and digitization/beam/thermal bounds. Resolve the current input gate before scientific fitting.

2. **Same-data constrained comparison of three physical models** Fit all three physically defined responses jointly under one calibration; preserve residuals and code, including any model rejection.

3. **Identifiability, history dependence and held-out prediction** Profile the mixed fraction and key correlated parameters, test rise-time/history dependence, and predict held-out conditions. Report bounded equivalence if justified.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Molecular DFT, PMMA-film modeling and optical limiter performance are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `observations`: Verified observation and physical-parameter table
- `model_comparison`: Same-data constrained comparison of three physical models
- `identifiability`: Identifiability, history dependence and held-out prediction

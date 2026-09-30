# Scientific objective

Determine whether lateral Y–Y motion has distinctive spin–phonon coupling relative to longitudinal and cage motion, and separate tensor derivatives from thermal mode weighting in the two cage isomers.

# Public inputs and scientific boundaries

Retain the complete 96-atom molecules, including the C87H7 adduct and two Y atoms (source XYZ rows 81 and 82, one-based). Both neutral molecules have a doublet electronic state. This is a molecular EPR-tensor task; a Gd substitution is not an equivalent electronic model.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **In a common molecule-fixed Cartesian frame, dT/dQ=[T(+h)-T(-h)]/(2h) for T=g or hyperfine A, with mass-weighted normal coordinate Q and units declared. Compare h/2. Report n=1/(exp(hc nu/kT)-1) and n(n+1) separately from the derivative-based coupling; use positive vibrational frequencies.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Mode eigenvectors and reproducible displacement classification** Optimize and validate both doublets, calculate modes and document projection-based assignment, including the four leading lateral candidates. Select three mode classes per cage by the declared rule.

2. **Six central tensor derivatives with step control** Calculate a consistent g or A tensor for each central and four displaced geometries, retaining full components, normal coordinate units and spin-density validation.

3. **Occupation versus coupling and rotational covariance** Perform the rigid-rotation check; compare bare derivative norms and thermal weights at both temperatures, and determine which mechanism explains differences between mode classes and cages.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Full relaxation-rate integration, all modes and Gd analogues are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `mode_assignment`: Mode eigenvectors and reproducible displacement classification
- `tensor_derivatives`: Six central tensor derivatives with step control
- `thermal_and_frame_controls`: Occupation versus coupling and rotational covariance

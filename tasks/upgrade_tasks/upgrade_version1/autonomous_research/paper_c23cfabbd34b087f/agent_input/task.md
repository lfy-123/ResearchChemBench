# Scientific objective

Determine how backbone topology and substituent changes affect open-shell character and low-energy optical states, separating relaxation and electronic effects with matched scaffolds and spin diagnostics.

# Public inputs and scientific boundaries

Use four supplied mapped graph models with source truncation: long alkoxy chains are OMe and the label TIPS denotes the source C#C-SiH3 computational substitute, not full Si(iPr)3. Generate independent coordinates. 1M and 2M differ by C2H2; compare spin/optical observables, never their bare total energies. Oxidized 2M-prime is a different compound and outside this matrix. Use common_scaffold_mapping.json for the exact 54/56 retained-heavy atom pair maps; shared-scaffold coordinates must be copied from the computed reference, not independently fitted.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Within each fixed composition report E(T)-E(CS) on shared CS geometry and separately at state-relaxed geometries. BS energies are determinant energies with S2/occupations, not a spin-pure singlet unless an explicitly justified projection is supplied. Across topologies compare like-defined gaps and state descriptors, not total E.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Four matched electronic-state and optical panels** Build all four structures and evaluate stable CS, BS and triplet alternatives with conformer/collapse evidence; calculate matched low optical states in a consistent medium.

2. **Within-topology frozen-scaffold substituent controls** Generate common-scaffold interventions for both substitution pairs using the public mapped graph correspondence and evaluate electronic-state differences without borrowing equilibrium thermal corrections.

3. **Independent spin calibration and topology/substitution discrimination** Select one ambiguous representative by a recorded rule, perform independent spin calibration, and quantify topology/substituent/relaxation effects with a method sensitivity.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Full alkyl groups, oxidation products, device performance and a large new molecular design series are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `relaxed_series`: Four matched electronic-state and optical panels
- `frozen_scaffold`: Within-topology frozen-scaffold substituent controls
- `calibrated_interpretation`: Independent spin calibration and topology/substitution discrimination

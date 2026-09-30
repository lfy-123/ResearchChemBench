# Scientific objective

Determine whether the full Ni complex supports a closed-shell description, a triplet or a distinct broken-symmetry state, and whether the conclusion survives geometry and electronic-method controls.

# Public inputs and scientific boundaries

Use all 165 atoms in complex_4.xyz without ligand truncation. Retain neutral charge and the original connectivity; singlet, unrestricted broken-symmetry Ms=0 and triplet alternatives must be distinguished. A BS input multiplicity of 1 is not proof of a pure singlet.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Adiabatic electronic spin gap E(T;R_T)-E(CS;R_CS), separately from vertical E(T;R_CS)-E(CS;R_CS), in kcal/mol (1 hartree=627.509474 kcal/mol). No ZPE or G is folded into these E gaps. A collapsed BS attempt has no independent minimum energy.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Two-method electronic-state and stability matrix** Optimize/test CS, triplet and distinct BS starts at each method; retain stability, natural-orbital and spin-population outputs. Document any repeated convergence to the same state.

2. **Vertical versus relaxed spin energetics** Evaluate the triplet on the CS geometry and independently relax the triplet, validating geometries and comparing their electronic gaps.

3. **Method robustness and metal–ligand electronic assignment** Compare method-dependent gaps and occupations; test localized-metal versus ligand-radical descriptions against the actual spin densities.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Full water oxidation, additional catalyst substitutions and excited-state spectra are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `state_matrix`: Two-method electronic-state and stability matrix
- `geometry_control`: Vertical versus relaxed spin energetics
- `interpretation`: Method robustness and metal–ligand electronic assignment

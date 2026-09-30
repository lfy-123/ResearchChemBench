# Scientific objective

Compare actual state character and SOC in the three sensitizers and determine whether a consistently defined rubrene energy-transfer cycle supports their proposed sensitization role.

# Public inputs and scientific boundaries

Use complete supplied mapped graphs, monocationic sensitizers with omitted iodide counterions, and separate neutral rubrene. The sensitizers differ in backbone and substituents as well as heavy atoms; they are not an isostructural I-to-Se substitution series. Use common chloroform continuum conditions and explicit heavy-element relativistic/basis definitions. Use Cy2_planar_control.json for exact bridge atom IDs and signed dihedrals.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Matched vertical gaps and SOC are evaluated at each S0 geometry. For energy transfer use consistent adiabatic excitation energies: delta_TTET=E_T1(rubrene)-E_T1(sensitizer); negative is energetically downhill. Rubrene annihilation balance=2E_T1(rubrene)-E_S1(rubrene); nonnegative is an energetic prerequisite. These are not rates or quantum yields.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Three sensitizer low-state windows and actual SOC** Generate independent conformers for all sensitizers, validate S0 and calculate state-resolved energy, oscillator/NTO and SOC windows with root tracking.

2. **Independent acceptor energies and closed transfer/annihilation comparison** Calculate independent rubrene S1/T1 and sensitizer T1 adiabatic energies and form the stated TTET and acceptor-annihilation balances.

3. **Geometry versus heavy-atom coupling and method robustness** Run the Cy2 planar/released intervention and a real SOC-method sensitivity; assess localized heavy-atom character and scope of any mechanistic inference.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Cy3, absolute ISC/TTET/TTA kinetics, diffusion, solution aggregation and device/quantum-yield predictions are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `sensitizer_states`: Three sensitizer low-state windows and actual SOC
- `rubrene_energy_cycle`: Independent acceptor energies and closed transfer/annihilation comparison
- `geometry_and_method_test`: Geometry versus heavy-atom coupling and method robustness

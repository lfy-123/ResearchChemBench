# Scientific objective

Determine whether proposed high-triplet singlet-transfer channels remain plausible after direct SOC, neighboring-state competition and geometric/method controls across the source emitter series.

# Author-provided scientific guidance

Main pp3–5/Figure3 and SI TablesS1/NTO figures use Gaussian09W B3LYP/6-31G(d,p), gas-phase energies and Multiwfn fragment analysis. The authors discuss T4 channels for Ph/Na and T3 for An/Py. These indices are source assignments, not fixed targets under a changed method. Direct SOC matrices, root-window enlargement and frozen-torsion tests are new; they cannot by themselves establish an absolute hot-exciton/RISC yield.

The matched controls and robustness checks below are benchmark-authored extensions. Reproducing an author assertion or old numerical endpoint alone does not complete this investigation.

# Public inputs and scientific boundaries

Use the four complete named source molecules. Ph-mP and An-mP are the fixed representative pair for the detailed intervention. Use a common gas-phase baseline and identical fragment and state-energy definitions. Use the full mapped graphs and terminal_bridge_control quadruples in molecular_identities.json; no predicted high-triplet channel index is specified for autonomous research.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **For a matched physical Tn, delta_STn=E(S1;R_S0)-E(Tn;R_S0). Report SOC norms in cm^-1 and neighboring Tn±1 spacings at the same geometry and Hamiltonian. Energy/SOC support necessary channel prerequisites; neither is an absolute RISC rate or quantum yield.**.

This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Four-member matched state windows with high-state SOC** Calibrate Ph-mP and An-mP first, then calculate the four-member window with states, oscillator strengths, transition densities and actual SOC pairs.

2. **Representative root-window and geometry interventions** For the two representatives enlarge the root set and repeat the fixed 45-degree terminal torsion, recording state overlap and changed gaps/couplings.

3. **Competing high-state channels and bounded inference** Compare each representative candidate against neighboring triplets and a CT-sensitive method contrast; state what necessary conditions are supported and which kinetics remain unknown.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Nonadiabatic dynamics, absolute RISC rates and quantum efficiencies are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `series_states`: Four-member matched state windows with high-state SOC
- `representative_controls`: Representative root-window and geometry interventions
- `channel_competition`: Competing high-state channels and bounded inference

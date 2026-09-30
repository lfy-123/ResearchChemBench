# Scientific objective

Test whether donor type and placement alter singlet–triplet proximity through charge-transfer localization, geometric relaxation or both, while retaining optically active states.

# Public inputs and scientific boundaries

Use the supplied complete mapped graphs. The common dibenzo[f,h]pyrazino[2,3-b]quinoxaline core has donor sites 3,6,11: TD_2T has triphenylamine at all three; CD_2T has phenylcarbazole at 11; TD_2C has phenylcarbazole at 3 and 6. All are neutral. Use a consistent gas-phase baseline, singlet ground states and singlet/triplet excited states. No author optimized geometries, CT assignments or predicted gaps are supplied. torsion_control_mapping.json provides all three signed atom quadruples and donor/core fragment partitions for each molecule.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Vertical gap=E(S1;R_S0)-E(T1;R_S0); adiabatic gap=E(S1;R_S1)-E(T1;R_T1). Do not mix these or use Kohn–Sham gaps as excitation gaps. SOC is the norm of three spin components in cm^-1 with operator and state basis stated.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Six matched vertical-state and SOC panels** Generate independently initialized conformers, build the common torsion intervention, and calculate energies, oscillator strengths, fragment-resolved transition densities and SOC for matched low states in all six cells.

2. **Conformer and excited-geometry discrimination** Follow S1 and T1 relaxation for each member and explicitly separate vertical and adiabatic gaps. Preserve conformer and root-switch diagnostics.

3. **Position versus geometry and method robustness** Compare changes at site 11 and sites 3/6, then quantify the shift from fixed to relaxed torsions and a decisive method sensitivity. Evaluate both CT-based and geometry-based explanations.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: OLED host/device modeling, absolute RISC rates and additional donor series are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `vertical_matrix`: Six matched vertical-state and SOC panels
- `relaxation_matrix`: Conformer and excited-geometry discrimination
- `causal_comparison`: Position versus geometry and method robustness

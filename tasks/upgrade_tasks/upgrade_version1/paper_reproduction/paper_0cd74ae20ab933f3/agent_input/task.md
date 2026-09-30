# Scientific objective

Determine whether axial-pyridine substitution changes exchange primarily through electronic effects or core geometry, and whether the H/Me/OMe ranking survives the uncertainty of the spin treatment.

# Author-provided scientific guidance

The authors propose that electron-rich 4-substituted pyridines strengthen exchange in Cu paddlewheels. Main pp6–7/Equation 2 connects the singlet-triplet gap to thermally populated triplets. SI pp5–6 uses ORCA 6.0.1 B3LYP-D3BJ/def2-SVP/RIJCOSX triplet geometries and multicollinear SF-TDDFT in PySCF-forge; SI pp35–36 compares functionals, Cu triple-zeta basis and CASSCF(2,2) geometries. SI reports both SF-TDA and non-TDA comparisons; reproduce their distinction rather than treating every gap as a BS energy difference. The benchmark common-core factorization and same-geometry higher-level comparison are new.

The matched controls and robustness checks below are benchmark-authored extensions. Reproducing an author assertion or old numerical endpoint alone does not complete this investigation.

# Public inputs and scientific boundaries

Retain all four anthracenecarboxylate bridges and two axial ligands. Use neutral isolated dimers, singlet/BS and triplet states. Label Cu_A/Cu_B, bridge_i/C_carboxyl/O_A/O_B (i=1..4), axial_A/N and axial_B/N. Bind each carboxylate O_A to Cu_A and O_B to Cu_B; each pyridine N binds its respective Cu. Preserve the same ligand atom mapping across H, para-CH3 and para-OCH3 replacements. Do not treat a closed-shell singlet as the open-shell reference by default.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **J=E_S-E_T in cm^-1, equivalent to H=-J S1.S2 for two S=1/2 sites; P_T(300 K)=100*3*exp[J/(0.69503476*300)]/(1+3*exp[J/(0.69503476*300)]). Project BS energies with documented <S^2>; no silent J versus 2J conversion.**.

This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Three-member relaxed/common-core exchange matrix** Construct the mapped series and evaluate relaxed triplet references plus common-core controls, retaining S2 and spin-density evidence for singlet/BS and triplet states. Report projected exchange, population and core distances.

2. **Representative spin-model calibration** Before expanding the series, calibrate the R_H spin gap at a common geometry using an available high-level/spin-adapted route and document the active orbitals and numerical stability.

3. **Quantified electronic/geometric effects and unresolved rankings** Compute the substituent differences at both geometrical regimes and the method-sensitive comparison of the closest pair. Decide what the intervention resolves about ligand electronics.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Specialized PySCF-forge algorithms, full magnetization curves and MOF photochemistry are not required.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `exchange_matrix`: Three-member relaxed/common-core exchange matrix
- `spin_calibration`: Representative spin-model calibration
- `effect_comparison`: Quantified electronic/geometric effects and unresolved rankings

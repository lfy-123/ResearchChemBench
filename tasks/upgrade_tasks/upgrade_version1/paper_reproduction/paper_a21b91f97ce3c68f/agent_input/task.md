# Scientific objective

Determine whether hyperconjugation explains axial/equatorial changes in signed one-bond 119Sn–13C couplings after controlling Sn–C distance and torsion, including a sulfur-containing challenge pair.

# Author-provided scientific guidance

Main analysis and SI TableS3 motivate axial/equatorial coupling differences and sulfur behavior. SI computational methods use CREST/GFN2 conformer searches, GD3B3LYP/def2-TZVPP structures and Gaussian NBO3.1; coupling calculations use GD3B3LYP/TZP-ZORA with a nonrelativistic Hamiltonian and Integral=NoXCTest. The basis name does not make this a relativistic calculation. The fixed-distance/torsion interventions and an independent protocol sensitivity are benchmark extensions.

The matched controls and robustness checks below are benchmark-authored extensions. Reproducing an author assertion or old numerical endpoint alone does not complete this investigation.

# Public inputs and scientific boundaries

Use full tri-n-butyltin substituents on the mapped thp pair 6, 1,3-dioxan-2-yl pair 7 and 1,3-dithian-5-yl pair 13. Generate both axial and equatorial SnBu3 chair arrangements for each ring; map the same Sn, ring carbon and all three butyl alpha-carbons using supplied IDs. Couplings concern the three Sn–C_butyl bonds, with isotope signs retained. Ring nomenclature alone does not establish the chair orientation.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Signed J_total(119Sn,13C)=J_FC+J_SD+J_PSO+J_DSO in Hz, for each mapped Sn–C_butyl bond; arithmetic mean over three bonds. Report raw unscaled J and the exact Hamiltonian/basis. An empirical scale or a relativistic change cannot share an uncalibrated narrow tolerance.**.

This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Three full axial/equatorial signed-coupling pairs** Build the six chair conformers, select reproducible low-energy representatives and calculate each signed Sn–C coupling with component and localized-orbital evidence.

2. **Orthogonal distance and torsion interventions** Run the matched torsion-at-fixed-distance and distance-at-fixed-torsion grids for one specified Sn–Bu bond in each compound; preserve constrained structures and actual J outputs.

3. **Hyperconjugation sufficiency and sulfur exception** Compare ordinary and sulfur responses and repeat the decisive coupling under a documented Hamiltonian/basis sensitivity, separating methodological changes from chemical effects.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: All original carbohydrate substrates, additional sulfur series and proprietary NBO upgrades are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `pair_matrix`: Three full axial/equatorial signed-coupling pairs
- `geometric_interventions`: Orthogonal distance and torsion interventions
- `mechanism_test`: Hyperconjugation sufficiency and sulfur exception

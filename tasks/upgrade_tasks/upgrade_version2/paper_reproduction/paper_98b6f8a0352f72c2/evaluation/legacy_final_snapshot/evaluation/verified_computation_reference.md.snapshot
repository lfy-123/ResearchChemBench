# Verified computation reference — paper_98b6f8a0352f72c2 (paper_reproduction)

Updated 2026-09-21. Evaluator-private evidence; never copy to agent_input.

Current scientific acceptance: **PASS_CURRENT_SCIENTIFIC_SUBGOAL**. Software-version differences alone are not a qualification. The task's scientific objective, key points, conclusions and tolerances have not changed.

## Valid calculation chain

The actual C24H19N3 neutral singlet was calculated with the author's ωB97X-D3/def2-TZVP, def2/J, RIJCOSX and CPCM(CHCl3) route, without symmetry constraints. Two ground-state Opt/Freq runs converged with 138 frequency rows and no imaginary vibrations. Both minima were followed by independent 40-singlet-root vertical TDDFT calculations. S1 is the lowest root in each complete table.

The native outputs use TDA. This is also the documented ORCA 4.2.1 default (manual PDF p.676, printed p.644); the paper's methods do not override it. These results are not described as full-RPA calculations.

| Conformer | S1 / eV | f | Derived lifetime / ns | Leading S1 NTO weight |
|---|---:|---:|---:|---:|
| primary | 3.673246 | 0.618266385 | 2.763885903 | 0.92094778 |
| conformer2, selected | 3.664926 | 0.638447321 | 2.688686276 | 0.92129144 |

Conformer2 is lower in calculated Gibbs energy by **3.703e-5 Eh**, correcting the earlier exponent typo. The lifetime is recomputed as 1.4999/(f × wavenumber²), in seconds when the wavenumber is in cm⁻¹. The three evaluator targets 3.65 eV, 0.64 and 2.70 ns pass unchanged; SI Table S1's 2.81 ns is also compatible.

## Repaired transition-character evidence

The old localization record mistakenly analyzed canonical molecular orbitals. Its claimed 24.8%/50.9% donor-localized hole fractions are withdrawn. Direct .nto-to-Molden conversion also failed the matched hole/electron occupation check and is not accepted evidence.

The repair reconstructs natural hole/electron densities from the original state-1 .cis transition vectors, canonical MO coefficients and native AO overlap. Recovered NTO weights agree with the actual ORCA state-1 table within 5e-9; MO overlap orthonormality errors are below 7e-12. Both Löwdin and Mulliken partitions give the same direction of partial charge redistribution.

In primary/conformer2, leading-hole phenazine weights are 75.99%/75.17%, and leading-electron weights are 96.18%/95.99%: increases of 20.19/20.82 percentage points. The complementary aromatic amine/linker contribution decreases. Both orbitals retain phenazine character; this supports partial amine-to-phenazine charge transfer and delocalization, not complete donor/acceptor separation. Per-atom populations are retained in the reconstruction evidence.

## Evidence and evaluator correspondence

- [Fresh raw-output replay and numeric checks](../../../../runs/hold_verification/group_6/paper_98b6f8a0352f72c2/20260921_acceptance/report/results.json): both Opt/Freq endpoints, actual input parameters, full root identity, lifetimes and every current numeric rule.
- [Actual transition-density reconstruction](../../../../runs/hold_verification/group_6/paper_98b6f8a0352f72c2/20260921_acceptance/report/transition_density_repair.json): original GBW/CIS/NTO/stdout/input hashes, printed-weight regression, overlap and atomic/group population evidence; no new SCF/TDDFT.
- [Supplementary verification](../../../../runs/hold_verification/group_6/paper_98b6f8a0352f72c2/20260921_acceptance/report/supplementary_verification.md): source comparison, corrections, process/result/conclusion mapping.
- [Previous reference preserved](../../../../runs/hold_verification/group_6/paper_98b6f8a0352f72c2/20260921_acceptance/private_reference_before/paper_reproduction.md): rejected historical analysis is retained for provenance, not reused for acceptance.

Current process points are supported by identity, two valid minima, explicit S1 selection and independent-conformer checks. The numerical conclusion and the separate transition-character conclusion are both supported. These claims cover the 12a/CHCl3 subproblem; no claim is made for every derivative or every spectrum in the paper.

Table 2's unscored 3.65 D transition-dipole entry differs from the internally consistent computed 6.66–6.78 D values. This discrepancy remains disclosed; no scored target was changed. ORCA 6.1.1 versus 4.2 is recorded as provenance and does not prevent acceptance of the reproduced conclusions.

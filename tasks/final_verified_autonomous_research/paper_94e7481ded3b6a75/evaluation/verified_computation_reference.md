# Verified computation reference — paper_94e7481ded3b6a75 (autonomous_research)

> Evaluator-private computation archive, not agent input or a scoring route. Reconciled 2026-09-18 from existing successful outputs; no new quantum calculation and no public-starter blind replay. The evaluator's scientific key points and conclusions remain the grading authority.

## Successful PBNA chain

The object is the isolated computational PBNA model C24H22B2N2, 50 atoms, 190 electrons, charge 0, singlet. Source: main p. 5 §3.2 / p. 6 Fig. 3; SI S19 computational method/Table S11 and S19–S20 Table S12. This is a specified molecular-property calculation, not independent discovery of the supplied object.

1. Establish atom order and full molecular connectivity against the source model. The existing validation preserves indexed connectivity, including core/substituent links 17–29, 18–25, 19–40 and 20–21 (one-based).
2. Gaussian 16 C.01 gas B3LYP/6-31G(d), `Opt=(Tight,CalcFC,MaxCycles=200) Freq Int=UltraFine SCF=(Tight,XQC,MaxCycle=512) NoSymm Temperature=298.15 Pop=Full`, 1 atm. [Actual input](../../../../docs/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/input.com) → [Completed optimization/frequency log](../../../../docs/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log).
3. Check normal termination, completed optimization and all 144 physical modes positive; lowest 18.4028 cm⁻¹. Read electronic energy, ZPE, harmonic G and total entropy from this branch at 298.15 K / 1 atm.
4. Use the final `pbna_b3lyp_optfreq.chk` and its [formatted checkpoint](../../../../docs/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/wavefunction.fchk). The 2026-09-16 existing Multiwfn analysis selects menu 8 → 1, then orbitals 95 and 96 (`8,1,95,96,0,-10,q`); it includes AO overlap. Sum atoms 1–20 as BN-anthracene core, 21–28 as N-methyl substituents, 29–50 as B-phenyl substituents.

| Observable | Existing computed value |
|---|---:|
| E | −1087.144521883793 Eh |
| ZPE | 0.410486 Eh |
| G | −1086.786926 Eh |
| S | 160.846 cal mol⁻¹ K⁻¹ |
| HOMO | −5.559820070242108 eV |
| LUMO | −1.640720212791934 eV |
| Core HOMO / LUMO Mulliken fraction | 86.27071% / 92.21407% |
| N-methyl HOMO / LUMO fraction | 2.96132% / 1.22335% |
| B-phenyl HOMO / LUMO fraction | 10.76797% / 6.56256% |

The previously archived 83.12%/83.85% squared-AO-coefficient fractions were nonorthogonal coefficient diagnostics, not genuine populations. They are replaced here by the already available overlap-aware output, not relabelled. The small difference in frontier-energy last digits is from final-checkpoint extraction versus rounded log eigenvalues, not a new calculation.

[Native Multiwfn output](../../../../docs/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out) · [Recorded invocation](../../../../docs/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.json) · [Raw extraction and atom-map verification](../../../../docs/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json).

These results support the specified minimum, frontier energies, thermochemical quantities and core localization. No new population threshold or altered numerical tolerance was introduced. Squared AO norms are not used as population evidence in the current reference.

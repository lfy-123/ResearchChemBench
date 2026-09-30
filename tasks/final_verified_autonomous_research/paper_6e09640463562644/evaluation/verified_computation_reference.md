# Verified computation reference — paper_6e09640463562644 (autonomous_research)

> Evaluator-private archive of real successful historical calculations. This is not an evaluator, answer input or claim of a blind agent replay. Scoring remains defined by the task/evaluator key points and conclusions.

## Current scope and source

Reviewed 2026-09-15 by reading existing outputs and performing arithmetic only. No new electronic-structure jobs were run. docs/verification is read-only: discrepancies in its historical status/prose are reconciled here, without changing those records. This replaces the old truncated automatic excerpt; its prior version remains in Git 40a6cb60.

Unmodified historical scientific record: [results.json](../../../../docs/verification/group_1/paper_6e09640463562644/report/results.json). Verification history: [verification_report.md](../../../../docs/verification/group_1/paper_6e09640463562644/verification_report.md).

Author coordinates/routes used in verification remain private. Their use does not invalidate author-route feasibility; no independent discovery from the current public starter is claimed. The two modes share numerical verification evidence, not the same public information.

Primary source: [SI](../../../../papers/paper_6e09640463562644/documents/supplementary_001.pdf) PDF p.2 specifies MP2(full), aug-cc-pVTZ(O,H)/def2-TZVPP(Ba), ZPE-inclusive relative energies and 0.951 IR scaling. [Main paper](../../../../papers/paper_6e09640463562644/documents/main.pdf) Figs.1–2 discuss the finite hydration series; Fig.3 uses 150 K Gibbs values, which are not the archived default-temperature Gibbs values below.

## Effective successful chain

1. Recover the nine SI candidate geometries privately; retain neutral charge, doublet multiplicity and the Ba/hydroxide/water atom mappings.
2. Perform the archived Gaussian UMP2(Full)/GenECP Opt/Freq calculations. All nine have completed optimization, normal application termination and zero imaginary frequencies; every 3N−6 frequency is in the linked log.
3. Extract electronic energy, the printed E+ZPE sum and the printed Gibbs sum at 298.15 K separately. The ZPE/G sums below retain Gaussian’s printed six-decimal-Hartree precision.
4. Determine O–H connectivity from the optimized geometry and project relative displacement vectors on each O–H bond; classify hydroxide versus water modes before comparing frequencies. Multiply harmonic frequencies by 0.951. Record all mode IDs, intensities and experimental band labels.
5. Compare the finite A/B sets and n-dependent structure/spectra. Do not substitute hydroxide-band red-shifts for the distinct water-network band evolution.

| Candidate | Modes / imaginary | E (Eh) | E+ZPE (Eh, printed) | G298.15 (Eh, printed) | Ba–O(OH) Å | Raw Opt/Freq |
|---|---:|---:|---:|---:|---:|---|
| 1A | 12 / 0 | -177.45301765797 | -177.417049 | -177.448275 | 2.331412 | [author_si_1a_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_1a_mp2full_avtz_def2tzvpp_optfreq_hpc_f02a319e/gaussian.log) |
| 2A | 21 / 0 | -253.82453119225 | -253.764130 | -253.799658 | 2.515447 | [author_si_2a_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_2a_mp2full_avtz_def2tzvpp_optfreq_hpc_78f2ae0c/gaussian.log) |
| 2B | 21 / 0 | -253.82278875833 | -253.761129 | -253.795696 | 2.352646 | [author_si_2b_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_2b_mp2full_avtz_def2tzvpp_optfreq_hpc_9478b7fc/gaussian.log) |
| 3A | 30 / 0 | -330.19470725495 | -330.110240 | -330.149183 | 3.311950 | [author_si_3a_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_3a_mp2full_avtz_def2tzvpp_optfreq_hpc_45c099c7/gaussian.log) |
| 3B | 30 / 0 | -330.19336392171 | -330.107131 | -330.145995 | 2.507845 | [author_si_3b_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_3b_mp2full_avtz_def2tzvpp_optfreq_hpc_7d134924/gaussian.log) |
| 4A | 39 / 0 | -406.55915081433 | -406.451757 | -406.498323 | 3.172057 | [author_si_4a_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_4a_mp2full_avtz_def2tzvpp_optfreq_hpc_4dad5378/gaussian.log) |
| 4B | 39 / 0 | -406.56027133254 | -406.448462 | -406.491665 | 2.501351 | [author_si_4b_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_4b_mp2full_avtz_def2tzvpp_optfreq_hpc_5f30308a/gaussian.log) |
| 5A | 48 / 0 | -482.92564504412 | -482.795502 | -482.846992 | 3.104144 | [author_si_5a_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_5a_mp2full_avtz_def2tzvpp_optfreq_hpc_3496cd8f/gaussian.log) |
| 5B | 48 / 0 | -482.92392611516 | -482.786486 | -482.833429 | 2.486480 | [author_si_5b_mp2full_avtz_def2tzvpp_optfreq](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/gaussian_batch/author_si_5b_mp2full_avtz_def2tzvpp_optfreq_hpc_f84722ce/gaussian.log) |

For all differences, Δ=B−A and 1 Eh=627.509474 kcal/mol. Positive values favor A.

| n | ΔE kcal/mol | Δ(E+ZPE) kcal/mol | ΔG298.15 kcal/mol |
|---:|---:|---:|---:|
| 2 | 1.093394 | 1.883156 | 2.486193 |
| 3 | 0.842954 | 1.950927 | 2.000500 |
| 4 | -0.703136 | 2.067644 | 4.177958 |
| 5 | 1.078644 | 5.657625 | 8.510911 |

Only the n=4 bare electronic comparison favors B; all ZPE/G comparisons favor A, and n=5 favors A on every listed basis. The old “4B/5B both lower” interpretation is superseded, not a reason to remove B candidates.

Complete mode/atom/vector data: [ir_mode_identity_audit_20260910.json](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/ir_mode_identity_audit_20260910.json). The 70/30% bond-projection classification is a stated analysis diagnostic, not an author threshold or potential-energy distribution. Band comparison records: [author_route_closure_20260911.json](../../../../docs/verification/group_1/paper_6e09640463562644/artifacts/author_route_closure_20260911.json); its old lower-energy-alternative limitation is superseded by the table above.

| n / A candidate | Hydroxide mode / scaled cm−1 | Water-network c modes / scaled cm−1 |
|---|---|---|
| 1A | 12: 3734.955 | 10: 2962.489 |
| 2A | 19: 3712.385 | 17: 2867.936 |
| 3A | 27: 3703.361 | 25: 2504.834 |
| 4A | 36: 3700.982 | 32: 2597.872; 31: 2576.340 |
| 5A | 45: 3701.208 | 38: 2623.493; 39: 2650.180 |

## Key-point support and limits

The complete minimum ledger supports stationary-point validation. Atom-mapped Ba–OH distances plus finite-set ZPE ordering support contact-like n=1–2 versus separated/solvent-shared n=3–5 in the A series. Assigned water-network bands show the pronounced n=3 red-shift and larger-n splitting; all compared experimental bands, calculated modes and errors are retained in the linked author_route_closure and mode-identity records. This supports the current finite-series harmonic task, not exhaustive global search, exact experimental-peak fitting, bulk-solvation dynamics, AIMD or the 150 K Gibbs curve.

## Maintenance boundary

This document records successful scientific dependencies rather than queue chronology. Failed/cancelled jobs are not steps in this chain; an actually successful retry-labeled output is valid. Full vectors, settings and arrays are retained in the linked evidence, not silently cut to eight entries. The archive is not a requirement that a future agent copy the author route.

## Evidence scope review (2026-09-19)

Current-reference coverage is **partial**. The nine retained MP2 endpoints are source-derived candidates; they support feasibility of those endpoints but do not certify the complete current AR hypothesis set. Compare energies only within each n; the following B-minus-A differences are electronic E + ZPE, not G(150 K) or the printed G(298.15 K).

| Candidate | B-A E+ZPE (kcal/mol) | Ba-OH (angstrom) | Vector-assigned hydroxide mode (scaled cm^-1) |
|---|---:|---:|---:|
| 1A | 0.0000 | 2.33141 | 3734.955 |
| 2A | 0.0000 | 2.51545 | 3712.385 |
| 2B | 1.8834 | 2.35265 | 3709.572 |
| 3A | 0.0000 | 3.31195 | 3703.361 |
| 3B | 1.9505 | 2.50785 | 3689.332 |
| 4A | 0.0000 | 3.17206 | 3700.982 |
| 4B | 2.0679 | 2.50135 | 3665.465 |
| 5A | 0.0000 | 3.10414 | 3701.208 |
| 5B | 5.6576 | 2.48648 | 3665.088 |

The hydroxide projection uses retained mode vectors and the documented historical 0.951 scaling. It does not cover every water stretch or band splitting. Complete mode-to-band comparison and current hypothesis coverage remain unresolved; successful frequency jobs do not close those requirements. Source anchors: main PDF p. 2 Table 1 and p. 3 spectral discussion; SI PDF pp. 15-17 Tables S1-S2. Native file paths, minimum checks, and thermochemical definitions are in `docs/verification/group_1/paper_6e09640463562644/provenance/retained_hydration_reaudit_20260916.json`; remaining gaps are explicitly reviewed in `retained_hydration_evaluator_review_20260916.json`. No new quantum or post-processing calculation was run.

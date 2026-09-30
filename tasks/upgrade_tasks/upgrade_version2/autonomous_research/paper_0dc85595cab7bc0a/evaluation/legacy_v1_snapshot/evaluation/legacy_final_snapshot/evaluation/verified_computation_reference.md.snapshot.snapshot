# Verified computation reference — paper_0dc85595cab7bc0a (autonomous_research)

> Evaluator-private archive of real successful historical calculations. This is not an evaluator, answer input or claim of a blind agent replay. Scoring remains defined by the task/evaluator key points and conclusions.

## Current scope and source

Reviewed 2026-09-15 by reading existing outputs and performing arithmetic only. No new electronic-structure jobs were run. docs/verification is read-only: discrepancies in its historical status/prose are reconciled here, without changing those records. This replaces the old truncated automatic excerpt; its prior version remains in Git 40a6cb60.

Unmodified historical scientific record: [results.json](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/report/results.json). Verification history: [verification_report.md](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/verification_report.md).

Author coordinates/routes used in verification remain private. Their use does not invalidate author-route feasibility; no independent discovery from the current public starter is claimed. The two modes share numerical verification evidence, not the same public information.

Primary source: [Main paper](../../../../papers/paper_0dc85595cab7bc0a/documents/main.pdf) PDF p.2, Fig.2; SI Fig.S5 and its endpoint tables. The paper compares within-stage regioisomers by Gibbs energy and uses LUMO distributions as a qualitative site rationale. The reported 9.9/11.3 kcal/mol differences are source references, not the local computed values.

## Effective successful chain

1. Recover 1-cis, IS1–IS7 and product-2 from private SI coordinate tables with retained labels and charge/multiplicity. These are author-route validation inputs, not agent inputs.
2. Optimize and frequency-test every endpoint at B3LYP-D3/6-31G(d,p), then obtain wB97XD/def2TZVP refined single points from the Link1 records. All nine are optimized minima with zero imaginary modes; gas-phase/isolated-molecule thermochemistry is the scoped model.
3. For within-stage comparisons use G_refined=E_refined+thermal Gibbs correction from the lower-level Opt/Freq log. Compare only same-stoichiometry IS2−IS1 and IS5−IS4; do not subtract different oxidation/stoichiometry endpoints as balanced reactions.
4. Use the existing LUMO cubes for mapped 1-cis C1/C2 and IS3 C3/C4. Integrate amplitude squared in a 1 Å sphere using cube voxel volume, and inspect the relative signed nearest-grid amplitudes. A global orbital sign is arbitrary.
5. Combine stage-specific thermochemistry and electronic rationale with the finite endpoint/coverage record; do not infer excited-state dynamics or a unique globally searched mechanism.

| Endpoint | Frequencies / imaginary | E refined Eh | Thermal G correction Eh | Raw successful output |
|---|---:|---:|---:|---|
| 1_cis | 150 / 0 | -1156.43337432 | 0.367428 | [1_cis](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_1_cis_optfreq_refined_sp_hpc20_p6/stdout.log) |
| is1 | 150 / 0 | -1156.38017151 | 0.371569 | [is1](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is1_optfreq_refined_sp_hpc20_p3/stdout.log) |
| is2 | 150 / 0 | -1156.36273118 | 0.369523 | [is2](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is2_optfreq_refined_sp_hpc20_p6/stdout.log) |
| is3 | 144 / 0 | -1155.25284904 | 0.351524 | [is3](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is3_optfreq_refined_sp_hpc20_p6/stdout.log) |
| is4 | 144 / 0 | -1155.19984106 | 0.355160 | [is4](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is4_optfreq_refined_sp_hpc20_p6/stdout.log) |
| is5 | 144 / 0 | -1155.18043450 | 0.353289 | [is5](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is5_optfreq_refined_sp_hpc20_p6/stdout.log) |
| is6 | 150 / 0 | -1156.29995041 | 0.373247 | [is6](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is6_optfreq_refined_sp_hpc20_p3/stdout.log) |
| is7 | 150 / 0 | -1156.32852063 | 0.375433 | [is7](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/hpc_runs/author_channel_is7_optfreq_refined_sp_hpc20_p3/stdout.log) |
| product-2 | 138 / 0 | -1154.07420285 | 0.334921 | [product-2](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/artifacts/gaussian_batch/author_channel_product_2_optfreq_refined_sp/stdout.log) |

ΔG(IS2−IS1)=9.660087921 kcal/mol; ΔG(IS5−IS4)=11.003730032 kcal/mol, from the same-definition differences with 627.509474 kcal/mol per Eh. [refined_profile_audit.json](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/provenance/refined_profile_audit.json) contains the detailed extraction; its earlier “missing product/LUMO” limitations are superseded by the product raw log above and later cube audit below.

Mapped local LUMO-density integrals: C1(atom21)=0.033433537 versus C2(atom25)=0.009993439; C3(atom3)=0.033354883 versus C4(atom11)=0.012406234. Ratios are 3.345549 and 2.688558. In IS3 the two nearest-grid signs are opposite; in 1-cis those two sampled signs are the same. Do not infer an absolute phase sign or every depicted nodal feature from those two samples. Complete mapping/grid/evidence: [lumo_reactive_site_mapping_audit_20260911.json](../../../../docs/verification/group_4/paper_0dc85595cab7bc0a/provenance/lumo_reactive_site_mapping_audit_20260911.json).

## Key-point support and limits

The nine minima, balanced stage differences and mapped qualitative orbital evidence support the current stationary-point/regioselectivity-rationale key points. The supported author continuation is IS1 → IS3 → IS4 → product-2, within the stated thermochemical scope. Spatial LUMO diagnostics are not Multiwfn atom-basin populations, kinetic barriers, excited-state dynamics or proof of exclusive experimental pathways. The old failure solely due to no displaced-public-starter replay is superseded. Public precursor and evaluator targets remain unchanged.

## Maintenance boundary

This document records successful scientific dependencies rather than queue chronology. Failed/cancelled jobs are not steps in this chain; an actually successful retry-labeled output is valid. Full vectors, settings and arrays are retained in the linked evidence, not silently cut to eight entries. The archive is not a requirement that a future agent copy the author route.

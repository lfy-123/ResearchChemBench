# 2026-11-04 来源、原生结果与评分口径复核

正文PDF2 Fig.2和SI PDF9 Fig.S5确为Gibbs能排序。重新读取4个历史Gaussian日志：两阶段ΔE为10.943972/12.177800 kcal/mol，热修正差为−1.283884/−1.174070，ΔG为9.660088/11.003730，排序保持。公开题面并未将ΔG设为唯一证据形式，因此本次修正两个评分项：允许有物理依据的同组成、同定义替代能量比较，须说明其支持所称热力学排序的理由及省略项影响；不因ΔE标签本身判失败，也不将裸ΔE冒充ΔG。候选身份/驻点有效性及事件顺序的要求保留。没有自动给旧运行补分。

本次逐份原始读取：[source_readback.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/GPT61_四项复核与运行修复_20261104/source_readback.json)；[修改方案](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/GPT61_四项复核与运行修复_20261104/修改方案.md)。以下历史验证记录保留原样，不恢复旧数值门槛。

# Round-one scope notice — 2026-11-03

Product 2 connectivity is supplied public input. Score only computed competing-site energetics, independent site explanations and the balanced sequence; never award product-identification points. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## 2026-10-27 V3 final-result migration

Six independent final results retain the original two-stage selectivity and product-prediction scope. No new quantum-chemistry or HPC jobs were run. Existing native results are reused only for the matching final claims listed in evidence_map.json; historical PASS labels are not transferred. Native endpoint/orbital evidence does not establish excited-state kinetics; initial local phase sampling does not reconstruct every source nodal feature, and no public-starter blind replay is certified. The dated record below is retained verbatim.

## 2026-10-20 专家第一轮评分规则同步

连续反应路线与最终产物身份合并为 30 分，须同时满足；前四项 70 分保留。

本节记录评分合同变更；下方原日期的计算结果、旧规则和验收范围按历史保留，不作为额外的现行评分要求。当前规则以 scoring_rules.json、reference_key_points.json 和 reference_conclusions.json 为准。本轮没有新增量子化学作业。

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

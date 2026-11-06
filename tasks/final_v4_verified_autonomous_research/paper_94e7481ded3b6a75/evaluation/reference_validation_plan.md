# Scoring applicability — 2026-10-29

This document retains source/verification context. Only current scoring_rules.json controls scoring: independent semantic pass/fail final conclusions, without numerical target windows or author-workflow requirements. Historical scientific findings below are unchanged and are not new validation.

# Current V3 evidence boundary — 2026-10-28

逐命题复用：吸收解释由真实80原子DCM TD S1/S2=3.4122/3.8949 eV及态特征支持；发射解释由234正模的S1、cLR垂直发射424.781160 nm与E00=409.2456 nm分别支持；两种模型适用性由50/80映射与吸收/发射不同敏感性支持。PR保留气相50原子HOMO/LUMO最终量原窗。未新计算或新V3验收。

The common final questions are absorption explanation, emission/relaxation explanation, absorption applicability and emission applicability. AR weights are 35/35/15/15. PR preserves its pre-existing extra final source-model HOMO/LUMO eigenvalues at 5/5 with unchanged targets -5.62/-1.71 eV and ±0.25 eV; common PR weights are 30/30/15/15. This explicit baseline exception is not imposed on AR. Frontier-localization nodes and duplicate all-in-one optical/transfer syntheses are retained only as unscored evidence. No optical tolerance is invented.

No new computation or blind evaluation was performed. Current rule-specific gaps are recorded in reference_qualification.json. The text below is historical and does not impose a current scoring or workflow requirement.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# V2 reference validation status

The source includes PBNA as the B-phenyl molecular reference within a functionalized BN-anthracene study. This task focuses on PBNA molecular solution optical response, not the substituent series or aggregation-induced behavior.

保留 group_1 有限模型参考，结论仅其分子/态范围；semantic judge 明确未校准。

Old source coordinates, calculations and V1 validation are retained as historical evidence; no inherited PASS or matrix completion obligation. This V2 package needs independent semantic evaluator calibration and isolated execution before scientific release. Existing logs must be parsed for the exact object, state, method, energy/measurement reference and claimed scope before reuse. Source results are conditional references, never a universal tolerance or mandatory winner.

Existing bounded PBNA native calculations and spectral analyses support finite-molecule feasibility. Their motion/solvation evidence may be used only for its actual state and conditions; it is not an AIE reference or semantic calibration.

Minimum later validation: verify genuine input/identity and applicable native output; recompute linked quantities/units from stored artifacts; assess whether the evidence sustains the particular scientific claim; test valid alternative/inconclusive cases and paper-specific misleading/invalid submissions. New numerical ranges require genuine method/model/extraction uncertainty, not legacy narrow tolerances. This round starts no science jobs and no paid/judge runs.


## 2026-09-30 source repair and bounded validation handoff

Experimental PBNA is the neutral singlet N-hexyl compound C34H42B2N2 (80 atoms), with two N-linked n-hexyl groups and the supplied B-phenyl BN-anthracene connectivity. Observations are for 10^-5 M dichloromethane solution at room temperature. The experimental identity is the reference for this question; physically admissible full-molecule models or explicitly mapped and justified approximations are allowed. State exactly which atoms or substituents change, why the approximation is adequate for each claimed optical property, and what cannot be transferred to the experiment. No additional full-molecule calculation matrix is prescribed. Other functionalized BN-anthracenes and condensed-phase aggregation are outside the required problem. Absorption bands, onset and emission features are distinct observables. Source identity distinction: main physical pp2–3 (section 2.2.3), SI physical p4 FigS3 and p6 TableS2 identify experimental N-hexyl PBNA, C34H42B2N2. The PBNA coordinate block in SI physical pp19–20 TableS12 instead contains the N-methyl computational approximation C24H22B2N2 (50 atoms). The experimental graph is in this package data/inputs/objects.json; the named author_model.json and author_model_mapping.json are PR-only assets in the companion paper_reproduction package. Reproduce the disclosed computational baseline or justify substitutions, then assess the transfer to the experimental molecule; the author approximation is not a second experimental identity and does not itself validate that transfer.

Reusable evidence: Existing 50-atom source-model S0/TD/orbital/NTO and limited excited-state outputs remain conditional evidence for N-methyl PBNA, after explicit graph/state remapping. They do not become 80-atom experimental calculations.

Still required for any enlarged claim: Assess the adequacy and optical consequence of truncation for the claims; retain missing solution excited-state/relaxation validation and software/method calibration. A chosen scientifically justified approximation is allowed; no fixed full-molecule matrix is newly required.

Rebind kp_identity, kp_quantitative_evidence, kp_validity_and_uncertainty, bounded_answer and dependent rules to this record. Preserve existing scoring weights and evidence requirements. No new scientific run, semantic judge or isolation test was performed.

Chronology: The 2026-09-28 dated design/case records retain their original bytes. The corrections in this 2026-09-30 section and integrity_repair_20260930 supersede their conflicting identity/protocol/rule descriptions; they are not retrospective preregistration.

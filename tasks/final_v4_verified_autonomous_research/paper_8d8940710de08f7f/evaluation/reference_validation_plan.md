# Scoring applicability — 2026-10-29

This document retains source/verification context. Only current scoring_rules.json controls scoring: independent semantic pass/fail final conclusions, without numerical target windows or author-workflow requirements. Historical scientific findings below are unchanged and are not new validation.

# Second expert review — 2026-10-28

Existing preference rules now require actual relative energies and matched vacuum/methanol gap comparison; flexibility requires quantitative mapped torsional/path evidence, not merely a nonzero penalty. No hard target, mesh or TS calculation is added. Source Table S8 Gibbs ambiguity and finite-path limits remain. No new scientific calculations were run.

# Current V3 validation scope — 2026-10-28

Four environment-specific preference rules reuse 12 R2SCAN/def2-TZVP/def2-J/RI minima. Existing qRRHO Z−lowest V gaps (SNaft/SAntr) are 3.487848/3.547305 kcal/mol in vacuum and 2.649947/2.679484 in methanol; electronic methanol gaps 3.039562/3.004860. Two contact explanations reuse separate ωB97M-V methanol QTAIM evidence (H/rho≈0.170, |V|/G≈0.789). Two flexibility results reuse the seven-point scans and released paths (sample maxima 6.283805/6.460401 kcal/mol). Redundant stability/flexibility synthesis and cross-medium restatements are no longer separately scored; their physical relations remain part of the relevant final answers.

SI Table S8 is printed in vacuo but its electronic energies match methanol better; source Gibbs temperature/environment are unresolved, so no exact Table S8 G reproduction is certified. Very small V+/V− differences do not establish unique populations. Finite scans and release paths do not certify continuous TS barriers or rates. Local Espinosa estimates do not decompose total conformer stabilization. Historical strict acceptance applies only to the bounded frozen scope, not a new V3 evaluation.

Package/rubric/runtime checks establish contract integrity only. No new scientific validation or agent blind run occurred. The historical plan follows unchanged.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# V2 reference validation plan

The source ORCA relaxed scans/optimization/frequency and existing neutral-molecule evidence demonstrate a feasible molecular route. ORCA/native and Python thermochemistry tools may support a chosen investigation after checking availability. First future review should reparse matching neutral raw outputs and verify source medium/functional labels before proposing new reference science.

## Existing evidence and limits

V1 evaluation/legacy_final_snapshot preserves older neutral/constrained source-method evidence. Source main Fig.8 and SI TableS8 give conditional source conformational/energy information, not an exhaustive independently validated ensemble. The source ωB97M-V density analysis belongs to a separate methanol calculation. No V1 mandatory dispersion/contact/environment matrix was completed by batch2; those operations are not active V2 criteria.

## Outstanding scientific calibration

No new full conformational reference or calibrated free-energy uncertainty has been obtained. Source labels and coordinates do not prove global sampling, and no experimental conformer fractions are supplied. Alternative-route scientific/semantic calibration and environment isolation remain pending.

This authoring run performed no new chemistry calculations, HPC submissions or remote judge calls. Offline package/contract/runtime checks do not establish chemical accuracy. A future reference review should verify source/structure/state correspondence, reproduce the claim-relevant quantities from raw existing artifacts, and assess the agent-chosen method limitations; additional science is separately authorized. No fixed V1 matrix, winner or uncalibrated tolerance is an acceptance rule. Actual alternative-route judging and private-file isolation must be checked independently.

## Source-label clarification at final closeout (2026-09-30)

Read main physical p5 and SI physical pp8–11, including the p8 Table S8 caption. The caption states in vacuo. Twelve already-existing paired single-point input/log files were re-read and hash-checked: six pairs share input coordinates and differ in the stated vacuum/methanol treatment. Their electronic energies raise a source-label inconsistency. This is diagnostic evidence, not a published correction, proof of the Gibbs-column environment, or a new free-energy tolerance. Exact paths and hashes are recorded in task_provenance/completion_source_label_review_20260930.json. No private diagnostic values or coordinates are exported to either task mode.

Reuse these native single-point artifacts only for their electronic-energy and provenance question after identity/method checks. They do not establish a minimum, complete sampling, a Gibbs-energy ordering, or the source flexibility/contact explanation. Existing validated endpoint/scan evidence may be reused only within its stated convergence, environment and coverage limits. The validation group should first reconcile those existing artifacts and source labels, then identify any necessary remaining flexibility/energy-profile and contact-evidence work. Keep constrained points distinct from minima; check environmental treatment in the actual density input before claiming methanol QTAIM. Do not rerun the paired single points merely because this wording changed. Any additional calculation remains outside this closeout.

The active kp_uncertainty/r_uncertainty/cf_7 supersede the absolute environmental wording in the dated original v2_design_audit.md, which is retained as historical provenance. Source originals, snapshots, scientific scope, weights, schema and public chemical graphs are unchanged. Source-label uncertainty is not a substitute for completing the scientific question.

The Table S8 provenance check is conditional on the submission using or diagnosing that source table. An independently justified route that does not use it has no obligation to retrieve or discuss S8 and cannot lose credit solely for omitting this source-specific diagnosis. General uncertainty and evidence requirements remain unchanged.

# Second expert review — 2026-10-28

Direct Gaussian log readback confirms G(C2h)-G(S4)=9.750242 kcal/mol at 298.15 K and 1 atm. The native_evidence top-level 8.769690 value is the electronic-energy difference, not Gibbs. Existing task and scoring already distinguish these quantities and retain the S4 minimum/C2h saddle and Hap/full-Egan boundaries; no scientific target or rule change is needed. No new scientific calculations were run.

# Current V3 validation scope — 2026-10-28

Three final quantitative rules retain S4/C2h Ir–Ir targets 2.599/2.724 Å (±0.01) and G(C2h)−G(S4)=9.7 kcal/mol (±0.2). Native distances are 2.598504/2.723610 Å; native Gaussian Gibbs sums −1655.046602/−1655.031064 Eh at 298.15 K and 1 atm give 9.750242 kcal/mol. The misleading C2h_minus_S4_kcal_mol field in native_evidence.json is 8.769690, actually the electronic-energy difference, and is not used as Gibbs evidence. The final ligand-mediated π-bonding explanation reuses occupied/empty directional orbital and occupancy evidence; the distinct orientation explanation reuses the S4/C2h structural-energy comparison. Model applicability uses actual curvature (S4 156 positive modes, C2h one −17.0855 cm−1 mode), molecular identity and explicit scalar-ECP/partition limits. Minima/saddle checks and individual orbital panels are supporting evidence, not independent scores.

Historical frozen-scope strict acceptance is preserved only as history. DeltaG differs from printed 9.7 by +0.050242 kcal/mol; no numerical window is changed. Correct Ir pairs are S4 1/2 and C2h 1/28. The failed composition module rc59 is partial output, not full success; later validated orbital blocks and native phase/occupancy evidence support bounded interpretation. Finite phase probes and simultaneous ligand distortions do not isolate a unique orientation energy decomposition. No SOC, full-Egan quantitative transfer, exact physical bond order 2.34 or equilibrium C2h population is certified.

Package/rubric/runtime checks establish contract integrity only. No new scientific validation or agent blind run occurred. The historical plan follows unchanged.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 6,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_6/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "733d1efabb39deac239f2318d48fc7385a9faa720b2a206bfeede892b4a158fa",
    "recorded_at_utc": "2026-09-28T15:08:44.745913+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "正确114原子截短二核先导已从平台停止后的最后有效SCF几何恢复，作业3fbad7fc在运行；完整210原子模型及自旋对照已准备，受先导质量门约束",
    "unfinished_scientific_or_input_work": "先导验证后做完整/截短、关联及自旋矩阵",
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md",
  "applicability": "114 原子截短模型在途先导不应冒充源 Hap 或完整 210 原子验证；V2 模型取舍先做来源/资源论证，避免无必要增加整套计算。",
  "new_scientific_calculations_performed": false,
  "source_model_correction": "Historical114-atom work remains a benchmark-added model only; source54-atom Hap model and210-atom experiment are distinguished."
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

The historical114-atom egan pilot is not source Hap evidence; its unfinished status cannot certify any stationary point. Later calibrate a chosen model against genuine raw electronic/structural evidence and source stationary-point definitions. No compulsory full210/114 pair or invented exact bond-order tolerance is retained.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Historical114-atom egan jobs are benchmark-added models, despite historical progress calling them source models. They are not the SI54-atom Hap model. Historical preparation/running states do not certify a minimum or a new V2 reference.

## 2026-09-30 current external correction and reuse (B5-V01)

The verification-group6 B5_V01_CORRECTION.json and corrected native evidence supersede the affected prior bounded acceptance. That acceptance was withdrawn. In the recorded native ordering, S4 Ir atoms are 1/2 and C2h Ir atoms are 1/28. The earlier C2h value 0.69909492 and its 129 original occupancy rows refer to Ir–O and must not support Ir–Ir nodes. Corrected C2h Mayer Ir–Ir is 0.61403928; the correct-pair native input explicitly selects 1,28 and its returned log contains 129 occupancy perturbation rows. Native composition evidence has 135 orbital blocks; HOMO129 Ir composition is 56.85882% (d contribution 56.84194%). These are private, condition-specific results, not mandatory answer values. Locators and freshly checked hashes are in task_provenance/integrity_repair_20260930.json. The correction status is native_correct_pair_repaired_science_partial; whole_paper_accepted=false.

Reuse the valid S4 electronic evidence and the five source54-atom Hap Gaussian outputs (three geometry/Hessian endpoints: two minima and one saddle; two stability records) only with their identity, state and stationary-point limits. Source main physical p.4 defines the method, pp.8–9 discusses bonding, and SI physical pp.22/29 establishes the C2h saddle rather than a second minimum. The historical114-atom egan pilot remains a benchmark model, not source Hap or the full210-atom Egan species. The raw electronic energy difference is not the source9.7 kcal/mol free-energy difference.

Remaining: the verification group must rebind the corrected pair/composition/perturbation evidence to kp_scope, kp_measure and kp_explain and assess model adequacy/uncertainty and the actual supported con_answer. Assess whether the available evidence discriminates the claimed bonding explanation; correct rows or rc=0 alone do not complete that inference or certify whole-question PASS. Any further scientific step must be justified by a remaining claim, not an inherited fixed grid or compulsory full-model run. Check element identity and mapping whenever files reorder atoms: valid remapping is accepted; 1/28 is specific to this native record and is not a universal public index requirement. Existing rules permit supported non-author conclusions. The original Ir–O rows remain preserved but excluded from Ir–Ir claims. No raw scientific file, evaluator weights or public input was changed; no new engine/job/judge was invoked by this repair.

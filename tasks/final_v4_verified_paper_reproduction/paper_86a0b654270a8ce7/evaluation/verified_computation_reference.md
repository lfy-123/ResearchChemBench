# V3 final-results scope and evidence reuse — 2026-10-28

Existing source-compatible B3LYP/def2-SVP/SMD(THF), 339 K minima give G1/G2 = -2795.462325/-2795.463430 Eh, ΔG = -2.901177 kJ/mol versus source -2.835540 kJ/mol (residual -0.0656375). Both have 384 positive modes (minima 11.3669/12.3800 cm−1). Absolute G offsets of approximately 8.9 kJ/mol remain unexplained. Fixed-geometry SuperFine curvature is not a reoptimization. Existing alternative-method plus borrowed-thermal sensitivity can reverse the small preference (+0.325/+0.332 kJ/mol with a 100 cm−1 entropy floor); it does not constitute alternative reoptimized Gibbs minima, and prevents a universal robustness claim. Geometry agreement supports contact compatibility, not a unique stacking energy. Historical strict acceptance is limited to the source model.

- `r_relative_gibbs`: 正文PDF2 §2.2、SI PDF11–18 → `docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/NATIVE_REUSE_READBACK.json`；原生G1/G2=-2795.462325/-2795.463430 Eh，差-2.901177 kJ/mol，在-2.84±0.50窗内。
- `r_relative_stability_synthesis`: 正文PDF2/3与SI构型 → `docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json`；几何与源重原子RMSD0.000076/0.000224 Å；同文件固定几何敏感性在100 cm−1熵处理下可到+0.325/+0.332 kJ/mol，故仅模型内偏好，不认证唯一堆积因果。
- `r_population_yield_limit`: 正文PDF2的Boltzmann表达式与PDF4分离产率 → 同一原生G/339 K定义，按exp[-(G2−G1)/(RT)]导出条件性[2]/[1]≈2.80；无互变/平衡证据，不能将19/53%产率当热平衡验证。

This update performs no new scientific calculation or validation. Historical PASS labels below are not a new V3 overall pass. The active rubric is `paper_science_v3` / `final_results_100`; all preceding versions and numerical conflicts remain archival evidence.

---

# V2 验证计算参考：Ir–salen–NHC 相对自由能

论文：`paper_86a0b654270a8ce7`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：完整两异构体在作者 THF/339 K 条件下的 B3LYP/def2SVP 实算有效最低点恢复源小幅 isomer2 偏好。源相对G -2.83554 对 -2.901177 kJ/mol，差0.06564，且真实网格敏感性同量级。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

What relative stability and molecular explanation are supported for the two supplied Ir–salen–NHC coordination isomers in THF at339K? Determine whether a preference can be established at the achievable evidence resolution and identify the limits of the explanation.

冻结题面中的科学目标：

What relative stability and molecular explanation are supported for the two supplied Ir–salen–NHC coordination isomers in THF at339K? Determine whether a preference can be established at the achievable evidence resolution and identify the limits of the explanation.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors use Gaussian16 B3LYP/def2-SVP with SMD(THF) at339K (SI p11) and favor isomer2 by about2.84kJ/mol, attributing stabilization to intramolecular phenyl/naphthyl stacking. They compare the result with an isolated yield ratio, which is not evidence of equilibrium without interconversion. Main p2 gives contradictory NHC trans-to-N/O labels in structural versus electrochemical paragraphs; follow verified graph/trans pair identity and disclose the inconsistency. The reported G values favor isomer2, but the printed exp(−ΔΔG/RT)=2.74 has an inconsistent sign or ratio definition when ΔΔG=G1−G2>0. Reconstruct the ratio from the defined G values; do not reuse the expression without correction. Reproduce the author baseline or justified substitutions, and separate later benchmark ensemble/contact/method controls from source work.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_86a0b654270a8ce7/documents/main.pdf](../../../../papers/paper_86a0b654270a8ce7/documents/main.pdf) | `b19110f192c994ade2406a46c6cc62346d465b27568db22c2b86df46f3af5879` |
| [papers/paper_86a0b654270a8ce7/documents/supplementary_001.pdf](../../../../papers/paper_86a0b654270a8ce7/documents/supplementary_001.pdf) | `59edd5baf1ea3027779a0ba8fef20348da233372dfdccdaf0ea2fa1f3f5886fb` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Native Gaussian B3LYP/def2SVP SMD(THF) Opt/Freq at 339 K; both full neutral-singlet C60H63IrN4O2 structures converge and have 384 positive modes. Independent fixed-geometry SuperFine frequencies provide a separate grid sensitivity, not new optimized minima.

1. 核对两个完整 C60H63IrN4O2、130 原子、中性单重态的配位异构体，以原子映射识别 trans donor；正文 N/O-trans 描述矛盾保留，不靠文字重新标号。

2. 按 Gaussian B3LYP/def2SVP、SMD(THF)、339 K 实际执行 UltraFine Opt/Freq，两端四项最终收敛标准均通过且各 384 正模。

3. 从同组成端点重建 G2−G1=−2.9011771 kJ/mol，对源 −2.8355396；分解共同绝对 G 偏移与约 −0.0656375 kJ/mol 的差分残差。绝对 G 零点原因未证实，不冒称绝对值相同。

4. 在固定几何上完成 SuperFine 频率控制，差变为 −2.964189 kJ/mol；它是网格/曲率敏感性，不是新的独立优化最低点。保留低频熵及固定几何方法控制，并从真实构型提取 NHC phenyl/salen naphthyl 非键接触。

5. 支持源模型中 isomer2 的小幅热力学偏好及接触解释相容性；19%/53% 分离产率不当平衡布居，不能唯一归因于 stacking、推出速率或器件/发光性质。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

#### required_calculations（冻结记录 E0015）

```json
[
  {
    "id": "two_UF_Opt_Freq_339K",
    "purpose": "Same-definition isomer relative Gibbs energy and structural comparison",
    "author_or_added": "author",
    "source_locator": "Main physicalp2; SI physicalp11.",
    "identity": "Two C60H63IrN4O2,130atom,q0/singlet six-donor isomers",
    "method": "G16 B3LYP/def2SVP/SMDTHF/339K/1atm UF",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log",
        "sha256": "8f406c07e68157faf3942ef7cc5359338cfd2ed584c4852ebb4a1bbf0ce1432c",
        "bytes": 3110668
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log",
        "sha256": "96ba7d4b682d213b37d6a94b3a759faa61d31210bb21adb9ba0b973e1e42cede",
        "bytes": 3110418
      }
    ],
    "native_validity": "Both original optimized structures have all4 Opt criteria YES,384 positive modes and full E/ZPE/H/G/S."
  },
  {
    "id": "complete_thermal_and_contact_controls",
    "purpose": "Bound numerical sensitivity and the contact/yield inference",
    "author_or_added": "added_validation",
    "source_locator": "Main physicalp2; SI physicalp11.",
    "identity": "Same two final UF geometries; graph-defined trans-pairs",
    "method": "Fixed-geometry SF complete Freq/339K; existing same-definition contact and thermal analyses",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.log",
        "sha256": "c7b1e175814fee900bd264484ec9510803f14d3a1db9509bc3cbd6780f81f97b",
        "bytes": 2509393
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.log",
        "sha256": "753f84db88755d151216d7cb8054f85f2be2190a7b8e8a5e0eda57f2b8317e2d",
        "bytes": 2509226
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_original6_20261007T040006Z/IR_FINAL_INDEPENDENT_READBACK.json",
        "sha256": "ad24bcc539ad5d58253a9791156caf9de6d702b9e8e13fdfe2681b9b8c12905f",
        "bytes": 33423
      }
    ],
    "native_validity": "SF has source-default force pass only. Displacement predictors fail default; it is local curvature, not a reoptimizedminimum. UF baseline remains independently valid."
  }
]
```


#### reused_results（冻结记录 E0015）

```json
[
  "docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/NATIVE_REUSE_READBACK.json"
]
```

### 最近一次原生有效性复核

本轮直接读两个原OptFreq，各384正频、正常优化；从原生G=-2795.462325/-2795.463430 Eh独立重算-2.90117710 kJ/mol。两个固定几何SuperFine Freq也实读，不把它们叫再次优化。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| G2−G1 (kJ/mol) | -2.835539610642796 | -2.9011771011656706 | Residual −0.0656375 kJ/mol (2.3%) for the source approximately 2.84 kJ/mol finding. Same composition, source-compatible minima and complete thermochemistry support agreement at this claim resolution. The actual SF change is −0.063012 kJ/mol; it is supporting measured sensitivity, not a fitted tolerance or confidence interval. |
| G1,G2 (Eh) | [-2795.45895,-2795.46003] | [-2795.462325,-2795.46343] | The absolute values do not match: common shifts about −8.86 and −8.93 kJ/mol. Their source zero/standard-state explanation is not proven; equal-stoichiometry relative stability is the target and cancellation leaves the explicitly small differential residual. |
| Lowest vibrational modes (cm−1) | Both source structures treated as molecular minima | [11.3669,12.38] | 384/384 positive modes and actual native optimized geometry convergence; frequency normal termination alone is not the acceptance reason. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Confirm full formulas and six-donor coordination identities, including explicitly supplied trans pairs. Match atom IDs through optimization; source textual N/O-trans descriptions conflict and cannot override the graph without evidence.

冻结要求：Confirm full formulas and six-donor coordination identities, including explicitly supplied trans pairs. Match atom IDs through optimization; source textual N/O-trans descriptions conflict and cannot override the graph without evidence. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：130原子及配位图

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "Two complete neutral singlet 130-atom C60H63IrN4O2 coordination isomers are supported by source coordinate/atom/trans-donor mapping and native outputs. Preserve the contradictory source N/O-trans prose; no prose-driven relabeling."
  }
]
```


证据记录：`E0079`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  }
]
```

### kp_quantitative_evidence — Recover a compatible quantitative isomer comparison from genuine molecular evidence with state, solvent, temperature and reference bookkeeping. Distinguish electronic energy from Gibbs free energy and assess whether any stated preference exceeds demonstrated uncertainty.

冻结要求：Recover a compatible quantitative isomer comparison from genuine molecular evidence with state, solvent, temperature and reference bookkeeping. Distinguish electronic energy from Gibbs free energy and assess whether any stated preference exceeds demonstrated uncertainty. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：相同组成、THF/339K相对G

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "The author B3LYP/def2SVP, SMD(THF),339K route has two fully converged UF Opt/Freq minima. Relative G2-G1 is -2.901177 kJ/mol against source -2.835540. This reproduces the approximately 3 kJ/mol model-level preference at the claim resolution; absolute G offset remains unverified. The full SF fixed-geometry sensitivity gives -2.964189, with separate electronic/thermal shifts; it is not a second fully optimized minimum or an error interval."
  }
]
```


证据记录：`E0079`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_grid_SiN_actual_native_seed_acceptance_20261002_a1/RESULT.json",
        "sha256": "22e2350203e7b1020ec8ba33212763b77b40340aad32a106e778b445311da522"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_grid_SiN_actual_native_seed_acceptance_20261002_a1/RESULT.json",
        "sha256": "22e2350203e7b1020ec8ba33212763b77b40340aad32a106e778b445311da522"
      }
    ]
  }
]
```

### kp_scientific_answer — Judge whether the proposed molecular account is supported by relevant evidence and not merely a contact visualization. Alternative stabilization accounts, reversed ordering and unresolved preference are eligible; no stacking mechanism or fixed intervention is obligatory.

冻结要求：Judge whether the proposed molecular account is supported by relevant evidence and not merely a contact visualization. Alternative stabilization accounts, reversed ordering and unresolved preference are eligible; no stacking mechanism or fixed intervention is obligatory. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：接触与小相对偏好相容

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "The source-method molecular baseline favors isomer2. Correctly mapped nonbonded NHC phenyl/salen naphthyl contacts are compatible with association; this evidence does not isolate stacking as the unique energetic cause. Source geometry agreement and genuine calculated thermochemistry provide positive reproduction, rather than reliance on the evaluator accepting an unresolved answer."
  }
]
```


证据记录：`E0079`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  }
]
```

### kp_validity_and_uncertainty — Use compatible molecular states and thermodynamic conventions for relative stability. Validate the structures/electronic states used, justify treatment of flexible modes and structural sampling where they affect the conclusion, and assess method/model uncertainty at the claimed resolution. Design checks relevant to your explanation rather than assume a contact proves causation.

冻结要求：Use compatible molecular states and thermodynamic conventions for relative stability. Validate the structures/electronic states used, justify treatment of flexible modes and structural sampling where they affect the conclusion, and assess method/model uncertainty at the claimed resolution. Design checks relevant to your explanation rather than assume a contact proves causation. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：正频/网格/低频/方法控制

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "UF baselines pass all four final native criteria and each has384 positive modes. Same-geometry SF gives384positive modes each, but predicted displacement criteria fail; retain only local curvature/grid sensitivity. Existing entropy-floor and fixed-geometry method probes expose sensitivity and cannot certify a complete conformer ensemble or new-method thermodynamic ranking. No global/model-independent preference is claimed."
  }
]
```


证据记录：`E0079`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_grid_SiN_actual_native_seed_acceptance_20261002_a1/RESULT.json",
        "sha256": "22e2350203e7b1020ec8ba33212763b77b40340aad32a106e778b445311da522"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_grid_SiN_actual_native_seed_acceptance_20261002_a1/RESULT.json",
        "sha256": "22e2350203e7b1020ec8ba33212763b77b40340aad32a106e778b445311da522"
      }
    ]
  }
]
```

### kp_bounded_conclusion — The result is a molecular thermodynamic/explanatory statement, not a synthetic yield prediction. Isolated yield ratios do not prove an equilibrium population or interconversion. A constrained contact change mixes energetic effects unless independently separated; finite stability does not prove emission efficiency or device performance.

冻结要求：The result is a molecular thermodynamic/explanatory statement, not a synthetic yield prediction. Isolated yield ratios do not prove an equilibrium population or interconversion. A constrained contact change mixes energetic effects unless independently separated; finite stability does not prove emission efficiency or device performance. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：不从分离产率推出平衡；bounded_answer在源模型范围闭合。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "The result is restricted to molecular thermodynamics and the limits of a contact explanation. Correct the source ratio sign algebraically; isolated19%/53% yields do not demonstrate equilibrium, rate or population. No excited-state, emission or device claim is accepted."
  }
]
```


证据记录：`E0079`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  }
]
```

### bounded_answer — A source-bounded evidence-supported answer to: What relative stability and molecular explanation are supported for the two supplied Ir–salen–NHC coordination isomers in THF at339K? Determine whether a preference can be established at the achievable evidence resolution and identify the limits of the explanation.

冻结要求：Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. The result is a molecular thermodynamic/explanatory statement, not a synthetic yield prediction. Isolated yield ratios do not prove an equilibrium population or interconversion. A constrained contact change mixes energetic effects unless independently separated; finite stability does not prove emission efficiency or device performance.

当前复审：kp_identity：130原子及配位图；kp_quantitative_evidence：相同组成、THF/339K相对G；kp_scientific_answer：接触与小相对偏好相容；kp_validity_and_uncertainty：正频/网格/低频/方法控制；kp_bounded_conclusion：不从分离产率推出平衡；bounded_answer在源模型范围闭合。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "The disclosed source model gives isomer2 a small lower Gibbs free energy, numerically reproduced to about0.07 kJ/mol by valid optimized source-route baselines. Its exact magnitude is sensitive to thermal/model choices; the evidence does not establish unique stacking causation or a synthetic yield prediction."
  }
]
```


证据记录：`E0079`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/Ir_source_geometry_G_precision_archive_strict_2_verification.json",
        "sha256": "05b9c09f8c214091833ce0606dc0240689dcec021d18aa2806a54eccc87b1c07",
        "bytes": 4642
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/RESULT.json",
        "sha256": "4110c80f07d81a9242afad262d0e10e677087e7fc0489f693d6acc57bb2f8ad2",
        "bytes": 33296
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_source_geometry_G_precision_archive_strict_2/run_status.json",
        "sha256": "9f8dedaca4ec323bc83f36a44a2071d55bfd38990ba923fb9e385018c5635402",
        "bytes": 6037
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/native_reuse_verification.json",
        "sha256": "601eda8df424eb234d0816a0ac39ea0b39980d43643dd39794add73dc8b3a0df",
        "bytes": 31311
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 137.05 小时；6 份计时日志/14 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,20 线程/进程；Gaussian %Mem=12000MB,70GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0004 · Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.log) | Gaussian:16352.2 | 正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.log) | Gaussian:16443.2 | 正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log) | Gaussian:190058；Gaussian:57004.2 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log) | Gaussian:151746；Gaussian:57597.1 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0040 · outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0056 · outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log) | Gaussian:613.5；Gaussian:511.7；Gaussian:97.9；Gaussian:667.4 | 正常；正常；正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0059 · outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log) | Gaussian:811.8；Gaussian:619.9；Gaussian:122.3；Gaussian:739.9 | 正常；正常；正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

绝对G共同偏移约8.9 kJ/mol未解释；源产率比不是平衡分布证明，固定几何不同方法会翻转小差。不认证唯一stacking因果或构象全集。

```json
[
  "No equilibrium yield prediction: the paper ratio expression has a sign/ratio inconsistency and isolated yields do not prove equilibrium.",
  "Fixed-geometry SF displacement criteria fail; only the original UF minima certify optimized basins. Optional historical checkpoint drift is not used for the required source baseline.",
  "Entropy-floor and other-method controls do not establish a global conformer ensemble or robust model-independent ordering."
]
```


原独立审查的 `material_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Absolute published G values remain shifted by8.86–8.93kJ/mol in UF. A1atm-to1M hypothesis explains most but not all; it is not an established correction. Equal-stoichiometry common offsets cancel in the relative question; residual relative mismatch is explicitly retained.",
  "SF is a fixed-geometry curvature diagnostic. Max/RMS predicted displacements are0.024683/0.004998 forisomer1 and0.044302/0.013918 forisomer2, failing0.0018/0.0012. Do not call these default-qualified SF minima. The original UF minima are independently valid; source does not mandate a separately SF-reoptimized route.",
  "SF electronic relative shift+0.112476 and thermal shift-0.175488kJ/mol sum to-0.063012, so the old electronic-only source-bracketing argument is rejected.",
  "Entropy-floor50/100cm-1 results -2.659825/-1.468915kJ/mol and fixed-geometry D3BJ/wB97XD plus borrowed thermal scenarios are sensitivity examples, not confidence intervals or complete alternative optimized thermodynamics. They do not establish global ensemble ranking.",
  "Unrecovered older bytes for two optional method-control checkpoints remain disclosed. No original checksum or raw output was rewritten. Mandatory core result provenance does not depend on those unrecovered binary versions.",
  "Source ratio sign and inconsistent N/O-trans prose are corrected/flagged from definedG and atom graphs. Source19%/53% yields are not equilibrium population validation.",
  "Scientific acceptance covers the current boundedAR/PR question. It does not certify every printed digit, exact private author settings, all results of the publication, a blindAR run, semantic judge calibration, runner isolation or an evaluator score."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_86a0b654270a8ce7.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_86a0b654270a8ce7/verified_computation_reference.md)；SHA-256 `692da61112ac06ae43912fa45ff4e190d9b33a6dfd198e49ac48a5f46d13b548`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_86a0b654270a8ce7.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_86a0b654270a8ce7.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_86a0b654270a8ce7.json) | `62cbc08237ebcd4de45fae6d4ccd1747b44c7e49bf1f945f90bdbc5056aa5bc0` | evidence_or_analysis |
| E0002 | [papers/paper_86a0b654270a8ce7/documents/main.pdf](../../../../papers/paper_86a0b654270a8ce7/documents/main.pdf) | `b19110f192c994ade2406a46c6cc62346d465b27568db22c2b86df46f3af5879` | source_document |
| E0003 | [papers/paper_86a0b654270a8ce7/documents/supplementary_001.pdf](../../../../papers/paper_86a0b654270a8ce7/documents/supplementary_001.pdf) | `59edd5baf1ea3027779a0ba8fef20348da233372dfdccdaf0ea2fa1f3f5886fb` | source_document |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `c7b1e175814fee900bd264484ec9510803f14d3a1db9509bc3cbd6780f81f97b` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `753f84db88755d151216d7cb8054f85f2be2190a7b8e8a5e0eda57f2b8317e2d` | native_output |
| E0006 | [docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `8f406c07e68157faf3942ef7cc5359338cfd2ed584c4852ebb4a1bbf0ce1432c` | native_output |
| E0007 | [docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `96ba7d4b682d213b37d6a94b3a759faa61d31210bb21adb9ba0b973e1e42cede` | native_output |
| E0008 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_original6_20261007T040006Z/IR_FINAL_INDEPENDENT_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_original6_20261007T040006Z/IR_FINAL_INDEPENDENT_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_IR_FINAL_INDEPENDENT_READBACK.json) | `ad24bcc539ad5d58253a9791156caf9de6d702b9e8e13fdfe2681b9b8c12905f` | evidence_or_analysis |
| E0009 | [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_task.md) | `02d2651b9e2a97ceee347d4e6a49e62e37746019c3b2b7345b96f82dc6663999` | historical_task_binding |
| E0010 | [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_reference_key_points.json) | `7705f0a3f68109c971b5341711ac6f78e7037644dc0dfb33d5cf95ff7251d3be` | historical_task_binding |
| E0011 | [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_reference_conclusions.json) | `8af0bd00667b11250dc0f3d4347b74b5a61d594a6775793ac46453e8243018e6` | historical_task_binding |
| E0012 | [tasks/v2_autonomous_research/paper_86a0b654270a8ce7/agent_input/task.md](../../../v2_autonomous_research/paper_86a0b654270a8ce7/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_task.md) | `e0cf18cb283ecb860b6fe9d4cf05279db00b6867d54586589200cc29b9e53903` | historical_task_binding |
| E0013 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/NATIVE_REUSE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/NATIVE_REUSE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_NATIVE_REUSE_READBACK.json) | `9658643ce9b0e522a26e1e6026420fb5e2a20908d985974e36921cfd967e3ced` | evidence_or_analysis |
| E0014 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/CURRENT_SCOPE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/CURRENT_SCOPE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_CURRENT_SCOPE_READBACK.json) | `e2ba3af4e1e0b0455887c011f7fade48f8218fd400b20d4e03ec8a3888a42916` | evidence_or_analysis |
| E0015 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/COMPUTATION_STAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_86a0b654270a8ce7/COMPUTATION_STAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_COMPUTATION_STAGE.json) | `7ea58c24fae67f89e5020a2cc63f8a6ff80bed764f714864df9166c63c30135c` | evidence_or_analysis |
| E0016 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_86a0b654270a8ce7.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_86a0b654270a8ce7.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_paper_86a0b654270a8ce7.md) | `9b7355afb38caac66b3d63981e52fd112489d33c86723039f4759dcbdd9d3ddb` | evidence_or_analysis |
| E0017 | [docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `edced55607106850bfed322359433241f325e6e86902b3d3c6f3a8c14ed85f1a` | historical_task_binding |
| E0018 | [docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `2f994e44afa2bc710d60131a292ed89876f26015bef04551e9eea87d34c0e926` | historical_task_binding |
| E0019 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_task.md) | `e0cf18cb283ecb860b6fe9d4cf05279db00b6867d54586589200cc29b9e53903` | historical_task_binding |
| E0020 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_reference_key_points.json) | `7705f0a3f68109c971b5341711ac6f78e7037644dc0dfb33d5cf95ff7251d3be` | historical_task_binding |
| E0021 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_reference_conclusions.json) | `8af0bd00667b11250dc0f3d4347b74b5a61d594a6775793ac46453e8243018e6` | historical_task_binding |
| E0022 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_task.md) | `02d2651b9e2a97ceee347d4e6a49e62e37746019c3b2b7345b96f82dc6663999` | historical_task_binding |
| E0023 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_reference_key_points.json) | `7705f0a3f68109c971b5341711ac6f78e7037644dc0dfb33d5cf95ff7251d3be` | historical_task_binding |
| E0024 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_reference_conclusions.json) | `8af0bd00667b11250dc0f3d4347b74b5a61d594a6775793ac46453e8243018e6` | historical_task_binding |
| E0025 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_package_manifest.json) | `1a2a1f541c81068f8400645328e3f459de32e6fa7f00a65ccf3cd3c4b83fac95` | historical_task_binding |
| E0026 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_package_manifest.json) | `d25dad4958b956e62fa45fab05df2bb048579419d123e904fa14dc92e0d534b1` | historical_task_binding |
| E0027 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group3/review_packets/paper_86a0b654270a8ce7_RETURNED_CONTROL_REVIEW_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group3/review_packets/paper_86a0b654270a8ce7_RETURNED_CONTROL_REVIEW_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_paper_86a0b654270a8ce7_RETURNED_CONTROL_REVIEW_20261006.json) | `c01e2896c44ed64d34a37d69d54826587a9637e5abc0da3819095a642842c481` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/Ir_before_final_20261007T041614Z/paper_86a0b654270a8ce7.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/Ir_before_final_20261007T041614Z/paper_86a0b654270a8ce7.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_paper_86a0b654270a8ce7.json) | `11f51a3c119de86635c07bfb0d3d4361e07854e8994cf649d55bfdccf3988c9f` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/calculation.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/calculation.chk) | `0f939699744aab1e4796bdc0cd553bc5b4c92ee86dcfa65eca0f623759098524` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/calculation.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/calculation.chk) | `0bc840205a3b3058efac1a0877b2589476e56b31ca39c31092ba5f17ba09033e` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/freq.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_freq.com) | `a011fed687c2911f5baa013d07aaf3793bbb3acc60ecb68feb6795332fe0ac1d` | input_or_analysis_code |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/freq.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_freq.com) | `5512d6a6b93f33eadc619c9ff9ee29157f0838a24482f3d61ea58814ba7e0241` | input_or_analysis_code |
| E0033 | [docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k.xyz](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_complex1_b3lyp_def2svp_smdthf_optfreq_339k.xyz) | `d85f3c80b09415de0fde892776a10808321a0c410d16cc2502153d34fb753775` | input_or_analysis_code |
| E0034 | [docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/input.com](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_input.com) | `b3f77f599b06db52a1d8753dbd8dd0332b2b59793bb6ea113ddffe9ad405a828` | input_or_analysis_code |
| E0035 | [docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k.xyz](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_complex2_b3lyp_def2svp_smdthf_optfreq_339k.xyz) | `69146d17a2cd563f15f058b32230d51359d6b345a598a03c1496c9a390cb3384` | input_or_analysis_code |
| E0036 | [docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/input.com](../../../../docs/v2_verification/history/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_input.com) | `7f98df2ae75d19130ee1d580d0c829f425fc33b5c33fdec953d146e41223f173` | input_or_analysis_code |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/sources/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/sources/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_main.txt) | `3acda1d9208a27e5d23e21a3a52d3bc6a285d7384b19d77c67a1e050cd0c0bfc` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/sources/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/sources/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_supplementary_001.txt) | `5f77242551992f1e3480b70f3f9f6ac4737cb8e467320b0024f1d4de1d5f8dc4` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_RESULT.json) | `aa743d75af8302163aa1264dbad1d02de7b7063f7470a25d098253c98c40abf1` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_native_excerpt.json) | `8693f6c07522a928273df9846a11eca5aebd44de33a8a9344cfb6ce2668aea8b` | native_output |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_complete_UF_SF_thermo_dye_S11_trajectory_audit_20261006_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_run_status.json) | `3af56541015e15f145aedb0ecadf9527b55594be26ec2312477bd8abd86a9d83` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_RESULT.json) | `c32375077c3dda87a550652edf37dd3800d8a2589ddd9684db5a5c81726b203e` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_run_status.json) | `d4320634234db2634ba879992c7bf072a782a251096f2defa743b9ce4e1b0a3f` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/verification_common.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/verification_common.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_verification_common.py) | `2add5f6c1dd1cc0bc4bec4be5a4328eb2e90387935ec93631b8cf5e65987a0a3` | input_or_analysis_code |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/frequency.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer1/frequency.fchk) | `9dfa4c3c61b85065577e3b9f7e45da6fd2e077042e41e22a325275a5164e56cc` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFineGrid_force_numerical_control_20261002_a1/isomer1.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFineGrid_force_numerical_control_20261002_a1/isomer1.fchk) | `4168193578d4105081f240c25cb3e4832b8492d38b007b0d52299707a41e1c31` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/frequency.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SF_fixed_geometry_curvature_339K_remaining24h_20261005_a2/isomer2/frequency.fchk) | `2f1b19c0f5300be4ef498c72404fee4e7730ace6411c317b073f95322ae8b991` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFineGrid_force_numerical_control_20261002_a1/isomer2.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFineGrid_force_numerical_control_20261002_a1/isomer2.fchk) | `8b275ea98a6b58e5b944b51cf635bd3597ad013d61fb2b2ef82a790b762e0be9` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/analysis/native_identity_339K_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/analysis/native_identity_339K_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_native_identity_339K_audit.json) | `63b798a411dfc86721374b49e0404115157d53ad7eb70251257754aa895d2e56` | evidence_or_analysis |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/analysis/nonbonded_ring_selection_repair.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/analysis/nonbonded_ring_selection_repair.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_nonbonded_ring_selection_repair.json) | `ddb8cfb04ea591e6ded6a6799676594ecef4c04e833b5dd0c9f4788c13dab8e9` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_86a0b654270a8ce7/paper_reproduction/agent_input/data/inputs/objects.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_86a0b654270a8ce7/paper_reproduction/agent_input/data/inputs/objects.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_objects.json) | `6d21e01401caebced2a4709f7c213fe4bb468c76313821d4c539ffde7c994a8e` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_native_excerpt.json) | `11b22f4c631950b1cdee10ddc66dbf2af3a5b493994a19dd64b93284df023402` | native_output |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_run_status.json) | `4a856e27bac4310f1466f583405ac562974d57a27db7491f3fa4d601a0e70cea` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/inputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/inputs/isomer1_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_input.com) | `ce3585bbef96a539a75be0ade65a5e34ad5d48d91b64c900da912942d502a63c` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_native_excerpt.json) | `9faba083e94c2e4230db4db332c3c1db9c70d9790e1ae2ece454138ad35baad2` | native_output |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/outputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_run_status.json) | `10dbe060addcc13c9f4ee83a5e39ffeccd4767b0d08664676c211be948cc5267` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/inputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_86a0b654270a8ce7/inputs/isomer2_matched_gas_SMD_D3_wB97XD_SVP_SP_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_input.com) | `53eb5f8756c48e4d39eddb8419fbe05831274f6b3d56b6f72db803824cd8d39c` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/verify_ir.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/verify_ir.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_verify_ir.py) | `26f5fc1033918146096a3ddac3646307cdb78bcf7c76b07cd52fe74af2525dbb` | input_or_analysis_code |
| E0063 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/task_info.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_task_info.json) | `99124a5efcf14f17c84dfd8b1f2eb279bde0b7ed67a99841ea8457d77b4064c2` | historical_task_binding |
| E0064 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_submission_schema.json) | `4087fbb9b13cc1d9c067c81a43b2264c1e1173440f25b8518e993536af7845da` | historical_task_binding |
| E0065 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_submission_guide.md) | `f678c374999c525867b38d95e0bdedda45729603de7e38687b2bebcadf40d87a` | historical_task_binding |
| E0066 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_scoring_rules.json) | `d99d5cd30c68adeb0e9ff1e3405b8d5f7a532648e1c3852fdd35c8e30e74e212` | historical_task_binding |
| E0067 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_evidence_map.json) | `4af1eedc644beca037291038280f9b7196fc93919dabd7475c150eb0d0520462` | historical_task_binding |
| E0068 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_critical_failures.json) | `ecd7e5ec9e9cd506db63ca4c35fc412ac642028770c50144f9722daaed2ea763` | historical_task_binding |
| E0069 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_reference_validation_plan.md) | `24c0dcc37e6281dc675b3519b5e51bdd47a9acbe3ed1b44838379c815d12ef30` | historical_task_binding |
| E0070 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/paper_route.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_86a0b654270a8ce7/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_paper_route.md) | `f689e4416ba5eaf7c264e2041edc3f327332336fed2e76d4d6429f469995fb90` | historical_task_binding |
| E0071 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/task_info.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_task_info.json) | `7edbc7baf709661ea3faf9c4c6eba015a2a11be91c3c9ab39d64d3ce633fef5d` | historical_task_binding |
| E0072 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_submission_schema.json) | `4087fbb9b13cc1d9c067c81a43b2264c1e1173440f25b8518e993536af7845da` | historical_task_binding |
| E0073 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_submission_guide.md) | `f678c374999c525867b38d95e0bdedda45729603de7e38687b2bebcadf40d87a` | historical_task_binding |
| E0074 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_scoring_rules.json) | `d99d5cd30c68adeb0e9ff1e3405b8d5f7a532648e1c3852fdd35c8e30e74e212` | historical_task_binding |
| E0075 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_evidence_map.json) | `4af1eedc644beca037291038280f9b7196fc93919dabd7475c150eb0d0520462` | historical_task_binding |
| E0076 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_critical_failures.json) | `ecd7e5ec9e9cd506db63ca4c35fc412ac642028770c50144f9722daaed2ea763` | historical_task_binding |
| E0077 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_reference_validation_plan.md) | `24c0dcc37e6281dc675b3519b5e51bdd47a9acbe3ed1b44838379c815d12ef30` | historical_task_binding |
| E0078 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/paper_route.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_86a0b654270a8ce7/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_paper_route.md) | `f689e4416ba5eaf7c264e2041edc3f327332336fed2e76d4d6429f469995fb90` | historical_task_binding |
| E0079 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group3/history/ready_withdrawal_20261005/paper_86a0b654270a8ce7_CURRENT_TASK_READY_20261003.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group3/history/ready_withdrawal_20261005/paper_86a0b654270a8ce7_CURRENT_TASK_READY_20261003.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_paper_86a0b654270a8ce7_CURRENT_TASK_READY_20261003.json) | `11a4b1843171b0a7f6fda1828bb0866ea407db664fa07b406e2da3383288b723` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/absolute_G_diagnosis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/analysis/absolute_G_diagnosis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_absolute_G_diagnosis.json) | `3c3f122b760c180664f0d8c1c4bac4f54ab8522b517670261f973a6a49997c90` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_86a0b654270a8ce7/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_86a0b654270a8ce7/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_main.json) | `ba82841b64edee0304545a13f57ead84da849a4e5e79ef93ebe7302a0f9f6846` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_86a0b654270a8ce7/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_86a0b654270a8ce7/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_supplementary_001.json) | `d6caa07815af79362ba5227fb1757bd27bc9a2bdf4ee001b4b54ef4393753078` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/IR_INDEPENDENT_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/IR_INDEPENDENT_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_IR_INDEPENDENT_READBACK.json) | `db08cd7f9f8d51069c396116f342f9317743b866fd4d5e3d5a6096b16a72b1c6` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/G3_IR_FREE_ENERGY_FOLLOWUP_RECEIPT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/G3_IR_FREE_ENERGY_FOLLOWUP_RECEIPT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_G3_IR_FREE_ENERGY_FOLLOWUP_RECEIPT.json) | `5876fa36b859e75d05760d37fb33067ec3df79be70394206c633f53738881482` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFine_complete_339K_Freq_24h_20261005_a1/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFine_complete_339K_Freq_24h_20261005_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_RESULT.json) | `72828dd0fb751c7ca105aeb99dfacb038ee5a71e45306ac954befbb5302e9054` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFine_complete_339K_Freq_24h_20261005_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_86a0b654270a8ce7/outputs/Ir_pair_SuperFine_complete_339K_Freq_24h_20261005_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_run_status.json) | `d0ae224a7675f54fab929318d05d27063b2838f01233be94674b2db1ac4605b8` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261005T080323Z/G3_RETURNED_STATIONARITY_CLARIFICATION_RECEIPT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261005T080323Z/G3_RETURNED_STATIONARITY_CLARIFICATION_RECEIPT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_86a0b654270a8ce7/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_G3_RETURNED_STATIONARITY_CLARIFICATION_RECEIPT.json) | `f76498d826622690587ee4548aafa6d2f3df36af7bc20005afd19cec927cfc29` | evidence_or_analysis |
| N0084 | [tasks/v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_key_points.json) | `7705f0a3f68109c971b5341711ac6f78e7037644dc0dfb33d5cf95ff7251d3be` | latest_review_evidence |
| N0085 | [tasks/v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json) | `8af0bd00667b11250dc0f3d4347b74b5a61d594a6775793ac46453e8243018e6` | latest_review_evidence |
| N0086 | [tasks/v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/scoring_rules.json) | `d99d5cd30c68adeb0e9ff1e3405b8d5f7a532648e1c3852fdd35c8e30e74e212` | latest_review_evidence |
| N0087 | [tasks/v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md) | `6f6951ff5a259ee1acde6532d16e777df35f419653a9aedc610158937bd75982` | latest_review_evidence |
| N0088 | [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/scoring_rules.json](scoring_rules.json) | `d99d5cd30c68adeb0e9ff1e3405b8d5f7a532648e1c3852fdd35c8e30e74e212` | latest_review_evidence |
| N0089 | [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `6f6951ff5a259ee1acde6532d16e777df35f419653a9aedc610158937bd75982` | latest_review_evidence |
| N0090 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0091 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/agent_input/task.md](../agent_input/task.md) | `02d2651b9e2a97ceee347d4e6a49e62e37746019c3b2b7345b96f82dc6663999` |
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_key_points.json](reference_key_points.json) | `7705f0a3f68109c971b5341711ac6f78e7037644dc0dfb33d5cf95ff7251d3be` |
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_conclusions.json](reference_conclusions.json) | `8af0bd00667b11250dc0f3d4347b74b5a61d594a6775793ac46453e8243018e6` |
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/scoring_rules.json](scoring_rules.json) | `d99d5cd30c68adeb0e9ff1e3405b8d5f7a532648e1c3852fdd35c8e30e74e212` |
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/critical_failures.json](critical_failures.json) | `ecd7e5ec9e9cd506db63ca4c35fc412ac642028770c50144f9722daaed2ea763` |
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/evidence_map.json](evidence_map.json) | `4af1eedc644beca037291038280f9b7196fc93919dabd7475c150eb0d0520462` |
| [tasks/v2_paper_reproduction/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `6f6951ff5a259ee1acde6532d16e777df35f419653a9aedc610158937bd75982` |


## Current scoring migration — 2026-10-19
Active policy: paper_science_v2; 100 binary scientific-result points across intermediate findings and final conclusions. Active rules supersede historical scoring weights and freezes. No process score or multiplier. This migration performs no new chemical calculation and preserves the existing frozen V2 acceptance with all scientific limitations. Main p2 contains contradictory trans-N/O labels and an inconsistent Boltzmann sign; public graph identity and definedG2-G1 govern. Both source-level minima are valid, but absoluteG values share an unexplained offset. SuperFine control is fixed-geometry curvature, not independently reoptimised minima. Low-frequency/conformer/model uncertainty limits fine thermodynamic claims. Stacking attribution is not an interaction-energy decomposition; isolated yield is not equilibrium.


## Authorized scoring-contract repair — 2026-10-19 (round3)
Self-audit confirmed19%/53% isolated yields are not supplied AR facts and are not needed for the population inference: retained the genuine computed Boltzmann relation while removing mandatory unpublished-value/source-expression criticism. Public scoring prose now describes100-point binary scientific results; reporting a contrary/unresolved answer does not automatically satisfy another target. This append changes the current evaluation contract only; original verification history remains verbatim, no new chemistry or acceptance upgrade is claimed.

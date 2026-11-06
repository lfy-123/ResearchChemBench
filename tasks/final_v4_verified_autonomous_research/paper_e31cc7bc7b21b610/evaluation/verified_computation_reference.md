# Second expert review — 2026-10-28

Direct Gaussian log readback confirms G(C2h)-G(S4)=9.750242 kcal/mol at 298.15 K and 1 atm. The native_evidence top-level 8.769690 value is the electronic-energy difference, not Gibbs. Existing task and scoring already distinguish these quantities and retain the S4 minimum/C2h saddle and Hap/full-Egan boundaries; no scientific target or rule change is needed. No new scientific calculations were run.

# V3 final-result evidence reuse — 2026-10-28

Preserve the short Ir–Ir bonding explanation and model limits. Explicitly bound the pre-existing numerical comparison to the neutral singlet 54-atom Hap model, S4 and C2h candidate orientations, gas phase and 298.15 K; the 210-atom experimental Egan dimer remains the observation to explain, not an interchangeable numerical target. The model/orientation candidates make the old hidden numeric scope public without disclosing their ordering or stationary character in AR.

Three final quantitative rules retain S4/C2h Ir–Ir targets 2.599/2.724 Å (±0.01) and G(C2h)−G(S4)=9.7 kcal/mol (±0.2). Native distances are 2.598504/2.723610 Å; native Gaussian Gibbs sums −1655.046602/−1655.031064 Eh at 298.15 K and 1 atm give 9.750242 kcal/mol. The misleading C2h_minus_S4_kcal_mol field in native_evidence.json is 8.769690, actually the electronic-energy difference, and is not used as Gibbs evidence. The final ligand-mediated π-bonding explanation reuses occupied/empty directional orbital and occupancy evidence; the distinct orientation explanation reuses the S4/C2h structural-energy comparison. Model applicability uses actual curvature (S4 156 positive modes, C2h one −17.0855 cm−1 mode), molecular identity and explicit scalar-ECP/partition limits. Minima/saddle checks and individual orbital panels are supporting evidence, not independent scores.

Limitations: Historical frozen-scope strict acceptance is preserved only as history. DeltaG differs from printed 9.7 by +0.050242 kcal/mol; no numerical window is changed. Correct Ir pairs are S4 1/2 and C2h 1/28. The failed composition module rc59 is partial output, not full success; later validated orbital blocks and native phase/occupancy evidence support bounded interpretation. Finite phase probes and simultaneous ligand distortions do not isolate a unique orientation energy decomposition. No SOC, full-Egan quantitative transfer, exact physical bond order 2.34 or equilibrium C2h population is certified.

The current policy is paper_science_v3 / final_results_100. The text below is an unchanged historical record; its old policies, scores and PASS labels are not current V3 certification. No new calculation was run.

---

# V2 验证计算参考：Hap Ir–Ir短键

论文：`paper_e31cc7bc7b21b610`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：键长与曲率复现，G差与源/原生联合打印区间相容；结构电子联合解释具实际依据。未将失败composition模块rc59当完整成功。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

短Ir–Ir键的结构与电子解释及截断分子模型的限度。

冻结题面中的科学目标：

What electronic and structural features can account for the short Ir–Ir bond in the supplied iminoxolene dimer, and how far can a molecular model support that explanation?

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_e31cc7bc7b21b610/documents/main.pdf](../../../../papers/paper_e31cc7bc7b21b610/documents/main.pdf) | `d10f786f46a66110c6c194aac86b204d3e34dc8be7d608d5c2557be4dd91f5d0` |
| [papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf](../../../../papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf) | `8160f45b57e772b48642e1e20d0ddddb8e64c97146b96bb942b33584b6cae2ec` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

54原子Hap、气相B3LYP/SDD(Ir)/6-31G*；S4最低点/C2h一阶鞍点及电子稳定性、Mayer/占据扰动、实际轨道方向分析。

1. 核对作者 54 原子 Hap 双 Ir 模型、ECP 电子数、Ir/配体原子映射，区分 Hap 计算模型与实验完整配体；Gaussian16 替代源软件的范围说明保留。

2. 按 B3LYP/SDD(Ir)/6-31G* 核收 S4 与 C2h 优化/频率：S4 的 156 个模全正，C2h 有唯一 −17.0855 cm⁻¹ 虚频，后者为鞍点而非稳定异构体。

3. 从真实坐标和能量提取 Ir–Ir=2.59850364/2.72360951 Å，对源 2.599/2.724；ΔG=9.750242 kcal/mol 对源 9.7。源坐标、网格与稳定性控制用于区分几何、热项和数值影响。

4. 按正确 Ir 原子对读取 Mayer 成键与各轨道流形贡献，检查占据、方向性和金属/配体 dπ 混合及未占 4e；由实际电子分析而非键长单独支持净 π 贡献。

5. 结论限于标量 ECP 的 Hap 局部模型和配体参与的 Ir–Ir 成键解释；SOC、完整实验配体迁移与唯一因果均不由该结果自动证明。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

从原生日志独立重算Ir–Ir=2.598504/2.723610 Å，对2.599/2.724；G差9.750242 kcal/mol，对9.7。S4 156正模、C2h唯一-17.0855 cm^-1，对源17.1i。正确Ir1/2与Ir1/28 Mayer为0.74459882/0.61403928。

Ir-Ir源2.599/2.724Å，实算2.59850364/2.72360951Å；ΔG源9.7，实算9.750242kcal/mol；S4全156正模，C2h唯一−17.0855cm−1。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_scope — Identity and scope

冻结要求：State the model composition, electron count, charge, electronic description and relation to the experimental dimer. A bonding explanation needs electronic evidence beyond a bond length. If comparing deformations or fragments, keep composition, state, reference and constraints consistent and distinguish minima from saddles.

当前复审：完整模型、有效驻点/映射、结构和能量、混合填充/空dπ轨道及方向证据共同支持成键解释。已回读真实Mayer/占据输出及10个cubegen原始数值文件，未只看summary。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "FullHapidentity and ECP/electron/atom mapping; experiment/model distinction."
  }
]
```


证据记录：`E0111`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json",
        "sha256": "cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json",
        "sha256": "cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      }
    ]
  }
]
```

### kp_measure — Quantitative scientific results

冻结要求：Establish a quantitative, physically sound molecular description of the observed metal–metal bonding using correct stoichiometry and a justified model. Full210-atom computation is not mandatory when a smaller representation demonstrably addresses the bounded claim.

当前复审：完整模型、有效驻点/映射、结构和能量、混合填充/空dπ轨道及方向证据共同支持成键解释。已回读真实Mayer/占据输出及10个cubegen原始数值文件，未只看summary。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Native bond lengths, curvature, energies,correctMayer pair and per-manifold values."
  }
]
```


证据记录：`E0111`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json",
        "sha256": "cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json",
        "sha256": "cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f"
      }
    ]
  }
]
```

### kp_explain — Evidence that distinguishes the claimed explanation

冻结要求：Support the proposed electronic/structural explanation with discriminating evidence. Orbital, density, energetic or other justified analyses can qualify; no prescribed orbital labels, deformation grid or fragment charge partition is required.

当前复审：完整模型、有效驻点/映射、结构和能量、混合填充/空dπ轨道及方向证据共同支持成键解释。已回读真实Mayer/占据输出及10个cubegen原始数值文件，未只看summary。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Electronic directional/occupation evidence beyond distance; ligand and metal mixing with vacant4e."
  }
]
```


证据记录：`E0111`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/directional_orbital_reanalysis.json",
        "sha256": "f622dcc5ea7f347d4e6dd76fe209d96893c7f6416fca5950102e6d01e758b649"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_evidence.csv",
        "sha256": "98604c40eab1e55e08c1217a0848189c7fcea06825da73aebe0ab1da67c21a9d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json",
        "sha256": "61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/directional_orbital_reanalysis.json",
        "sha256": "f622dcc5ea7f347d4e6dd76fe209d96893c7f6416fca5950102e6d01e758b649"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_evidence.csv",
        "sha256": "98604c40eab1e55e08c1217a0848189c7fcea06825da73aebe0ab1da67c21a9d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json",
        "sha256": "61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d"
      }
    ]
  }
]
```

### kp_robust — Uncertainty and limits

冻结要求：Assess whether model truncation, state stability and relevant numerical/relativistic assumptions limit the interpretation. Claimed minima/saddles and energetic comparisons require evidence appropriate to their structural status.

当前复审：完整模型、有效驻点/映射、结构和能量、混合填充/空dπ轨道及方向证据共同支持成键解释。已回读真实Mayer/占据输出及10个cubegen原始数值文件，未只看summary。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Actualstability/numerical/model checks; saddle,scalar-ECP,SOC/model-transfer and causality limits."
  }
]
```


证据记录：`E0111`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json",
        "sha256": "cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/directional_orbital_reanalysis.json",
        "sha256": "f622dcc5ea7f347d4e6dd76fe209d96893c7f6416fca5950102e6d01e758b649"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json",
        "sha256": "61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json",
        "sha256": "cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/directional_orbital_reanalysis.json",
        "sha256": "f622dcc5ea7f347d4e6dd76fe209d96893c7f6416fca5950102e6d01e758b649"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json",
        "sha256": "61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d"
      }
    ]
  }
]
```

### con_answer — What electronic and structural features can account for the short Ir–Ir bond in the supplied iminoxolene dimer, and how far can a molecular model support that explanation?

冻结要求：Provide or delimit an evidence-based explanation for the observed short bond and the validity of the chosen model. A reference bond length, nominal bond-order number or visually attractive orbital without supporting analysis is insufficient.

当前复审：完整模型、有效驻点/映射、结构和能量、混合填充/空dπ轨道及方向证据共同支持成键解释。已回读真实Mayer/占据输出及10个cubegen原始数值文件，未只看summary。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "The combined disclosedHap route supports a ligand-enabled net pi contribution andS4shortbond, with explicit model limits."
  }
]
```


证据记录：`E0111`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json",
        "sha256": "61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md",
        "sha256": "02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76",
        "prior_mutable_report_reference": {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md",
          "sha256": "0538ca7016481c02e18c5889cb9aaaa50720157b3adcb3061ab85aa5023661bd"
        },
        "kind": "derived_report_snapshot_not_native_output",
        "historical_digest_verified": false,
        "historical_digest_status": "unrecoverable_unverified_preserved; current derived summary is not substitute for old native evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json",
        "sha256": "61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 1.09 小时；7 份计时日志/11 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 20 线程/进程；Gaussian %Mem=80GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0027 · v2_Hap54_S4_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/gaussian.log) | Gaussian:152.8；Gaussian:413.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0030 · attempt_01/S4_mayer/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_mayer/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0031 · attempt_01/S4_occupancy/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_occupancy/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0032 · attempt_01/S4_composition/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_composition/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0033 · v2_Hap54_C2h_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/gaussian.log) | Gaussian:80；Gaussian:416.8 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0035 · attempt_01/C2h_mayer/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_mayer/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · attempt_01/C2h_occupancy/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_occupancy/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0037 · attempt_01/C2h_composition/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_composition/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0038 · attempt_01/C2h_occupancy/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_Ir1_Ir28_occupancy_B5V01/attempt_01/C2h_occupancy/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0039 · v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/gaussian.log) | Gaussian:209.4；Gaussian:1353；Gaussian:368 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0058 · v2_Hap54_S4_unrestricted_stability/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/gaussian.log) | Gaussian:497.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0059 · v2_Hap54_C2h_unrestricted_stability/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/gaussian.log) | Gaussian:330.6 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0060 · strict_S4_source_fixed_UltraFine_force/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/gaussian.log) | Gaussian:46 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0062 · strict_S4_source_fixed_SuperFineGrid_force/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/gaussian.log) | Gaussian:61.6 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

Mayer不是实验MOS=2.34；轨道扰动非可加能量分解；C2h不算稳定布居。角度和1e末位残差有源几何/网格/再松弛实测控制，原偏差不隐藏。

不认证完整210原子Egan、唯一因果分解、精确SOC或C2h稳定构象人口；这些不是当前必需对象。


原独立审查的 `material_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "The scalar-relativisticECP/modelroute reproduces the disclosed author baseline; no independentSOC/fullEgantransfer certification.",
  "CorrectMayer0.74459882/0.61403928 and occupancy-removalresponses are not the empiricalMOS-derived2.34 physicalbondorder. Per-orbitalresponses are nonadditive.",
  "Source4e and other manifolds contain substantialligandcharacter. Window-dependentnodalmetrics do not certify exactauthorwavefunctionphase.",
  "C2h is a constrained first-order saddle, not a second populatedequilibriumconformer; no Boltzmannmixture inferred.",
  "The donor-angle and orbital residuals remain explicit; no globally exact source-number reproduction is asserted.",
  "Neither a formal evaluator pass nor a blind autonomous-research execution is certified."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_e31cc7bc7b21b610.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_e31cc7bc7b21b610/verified_computation_reference.md)；SHA-256 `6c6f9729f7fc259ee4e67f95c61dc502b5c8bae563bf4d2dc2ad669f3a2dffd2`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_e31cc7bc7b21b610.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_e31cc7bc7b21b610.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_e31cc7bc7b21b610.json) | `4b16cea097ae2cd5efd4c1d8a8890a52a43995b156fc80ace9d2ce0eb6da6373` | evidence_or_analysis |
| E0002 | [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_task.md) | `5f28894903e884880b9390605d62687177072f4c639fb68b29cf8d3d8b5da922` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_e31cc7bc7b21b610/agent_input/task.md](../../../v2_paper_reproduction/paper_e31cc7bc7b21b610/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_task.md) | `8517213fe8e44fc7c2221c7dc73323ebcc0872b91bf305778cf79e538aa2b3ae` | historical_task_binding |
| E0004 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_ROOT_PRIMARY_SOURCE_READBACK.json) | `a131458d308b52199eb86e1c6e7fc3efefd0cc69c93f52a2a5001ed2c3df60d0` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_ROOT_NATIVE_READBACK.json) | `9f8ce2f290d610c66701f38fed799081fc653cd1cec06332a98de64ed1a3ea31` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e31cc7bc7b21b610/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e31cc7bc7b21b610/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_NATIVE_READBACK.json) | `702d949ba5bb17088c36671168d65516da7fcb5f1db294e5d463ab8276ab9829` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e31cc7bc7b21b610/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e31cc7bc7b21b610/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_COMPUTATION_COVERAGE.json) | `bb0ddb9b096ef860d65f9dd0adf645556e06178c2eefc63a6a0890b9550cd6c9` | evidence_or_analysis |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_e31cc7bc7b21b610.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_e31cc7bc7b21b610.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_paper_e31cc7bc7b21b610.md) | `ed42c60ab61d86d6ddb751e99b831d69cc395d6069623edcf10fa3113dc06b5e` | evidence_or_analysis |
| E0009 | [docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `1bc826e066d1546d69bdf19fbea2d091e0da49a59b9b9c1d01af6ac3daf72eac` | historical_task_binding |
| E0010 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_task.md) | `5f28894903e884880b9390605d62687177072f4c639fb68b29cf8d3d8b5da922` | historical_task_binding |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_package_manifest.json) | `d435d5fe4d917d6c46b934a50dd6c344961e0cf326154084052b6426dc8cb9a4` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_task.md) | `8517213fe8e44fc7c2221c7dc73323ebcc0872b91bf305778cf79e538aa2b3ae` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` | historical_task_binding |
| E0016 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` | historical_task_binding |
| E0017 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_package_manifest.json) | `cf2e5cd777d0748e97cde6f0d72d827f2299daa08f41871cdec5bb50c7976f8e` | historical_task_binding |
| E0018 | [papers/paper_e31cc7bc7b21b610/documents/main.pdf](../../../../papers/paper_e31cc7bc7b21b610/documents/main.pdf) | `d10f786f46a66110c6c194aac86b204d3e34dc8be7d608d5c2557be4dd91f5d0` | source_document |
| E0019 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_e31cc7bc7b21b610/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_e31cc7bc7b21b610/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_main.json) | `5c99e6a368d011c15a63c6043eec0bc222e2f39b582e72e25e92790c096fb2b2` | evidence_or_analysis |
| E0020 | [papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf](../../../../papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf) | `8160f45b57e772b48642e1e20d0ddddb8e64c97146b96bb942b33584b6cae2ec` | source_document |
| E0021 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_e31cc7bc7b21b610/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_e31cc7bc7b21b610/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_supplementary_001.json) | `c86e60aa18ac89e27494fdb09b0b6492cfdce209b5de044b44c5ab1fdb2acdda` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/source_fig6_p8.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/source_fig6_p8.png) | `852e312c5389f78174a5594c212b77ecd1487745e6f3f010753d7b6a803f9baa` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/native_evidence.json) | `cbc96a2bf0bad50714b3ca1d793afad81837c8883a185292f97173f2d1b67e3f` | evidence_or_analysis |
| E0024 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/directional_orbital_reanalysis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/directional_orbital_reanalysis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_directional_orbital_reanalysis.json) | `f622dcc5ea7f347d4e6dd76fe209d96893c7f6416fca5950102e6d01e758b649` | evidence_or_analysis |
| E0025 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_native_phase_evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_six_manifold_native_phase_evidence.json) | `61c822743c919744154f8e9de1ecca2eecfdd03e2e448dfa94414941975c9c4d` | evidence_or_analysis |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/completion_scope_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/completion_scope_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_completion_scope_review_20260930.json) | `8da837d6e7cdf83f78a0d095be40399759044a2434e1c9333f9f7e5fd23e84ef` | evidence_or_analysis |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_native_excerpt.json) | `a6934c62c78f0991b175f1c864ad535d42490dc98ddc43c5a511c32c0dbdf938` | native_output |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/Hap_core_identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/Hap_core_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_Hap_core_identity.json) | `aecf6cc56c9f5aebdee82130c8609243a4c0ffa162137da7f84f824de80511ed` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_mayer/bndmat.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_mayer/bndmat.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_bndmat.txt) | `68f2d36e42f739883d01748b9c28a9a11682826d8fa2f76170c8001ee9aa2bd7` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_mayer/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_mayer/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_native_excerpt.json) | `2687cef759f975dc1fa91f696f0dc51b84b324515475e13d5aeb79a5867250c4` | native_output |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_occupancy/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_occupancy/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_native_excerpt.json) | `ad99f8c28b13ac1a16dd1b55534a29ad010de6273b124e0f13f26f6c4a4472c7` | native_output |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_composition/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_source_S4_C2h_MO_Mayer_stack1/attempt_01/S4_composition/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_native_excerpt.json) | `d652eef62c0e96d90f70bb32f65c214f079bf13123aa71572f3d0cc72ca01adf` | native_output |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_native_excerpt.json) | `fd3df3c399a9c45fdceea3fdb6c13ec11f406b8f72c5bc9e12741e258a85f483` | native_output |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_mayer/bndmat.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_mayer/bndmat.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_bndmat.txt) | `85bb95c43dc6761f40c21445f1a52297403ccf37dbb378c3d003ce09d8d20117` | evidence_or_analysis |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_mayer/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_mayer/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_native_excerpt.json) | `5a0c79449233066516e38fd2f3572f6d27f257111330a95896c6221e26881461` | native_output |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_occupancy/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_occupancy/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `f7e7e677ccfb4543a07aec6c6e7d3dd2051ce5a244ba12a4f3c0c074e0ad7121` | native_output |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_composition/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_MO_Mayer_menu_corrected/attempt_01/C2h_composition/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_native_excerpt.json) | `e0f7d56f4e76c18b2199b70e12bba831f93afc597b69e8c9f27d26cffc1c28d4` | native_output |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_Ir1_Ir28_occupancy_B5V01/attempt_01/C2h_occupancy/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_Ir1_Ir28_occupancy_B5V01/attempt_01/C2h_occupancy/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_native_excerpt.json) | `d7beb648e93362a380eb0bf3045e4edbc65c90ed97f9594d3987ef6385250b93` | native_output |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_native_excerpt.json) | `fce5f75c3fc2dd8eeffd09be0d2f18820075a3a34acc709ac282f353fd8b9f92` | native_output |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/sources/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/sources/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_main.txt) | `662fc21f43b25c25a0cc70092e2d95662895f36486623eae181ab6b8d3ea1d18` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/../../B5_V01_CORRECTION.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/B5_V01_CORRECTION.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_B5_V01_CORRECTION.json) | `c8047327fca8b2c04ab746b817787ad4fa0a6b137028524696325f5b8c68be15` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_e31cc7bc7b21b610_STRICT_REVIEW_0720Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_e31cc7bc7b21b610_STRICT_REVIEW_0720Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_paper_e31cc7bc7b21b610_STRICT_REVIEW_0720Z.json) | `9dc09f6710fab43de0739b38b06b4cc16cfde3ab79807da71b8b62d5810b7ac6` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_e31cc7bc7b21b610_ready_rehash_0730Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_e31cc7bc7b21b610_ready_rehash_0730Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_paper_e31cc7bc7b21b610_ready_rehash_0730Z.json) | `17f337c41ec335e2e7129ed2106b888ed03e5934c394a27ca0daa5314af4c6d1` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/report.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_report.md) | `02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/paper_e31cc7bc7b21b610_abc425134ef3aef9491a3fc09df82a56ad5d0fba7724193ed1b8f768e8ddc52a.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/paper_e31cc7bc7b21b610_abc425134ef3aef9491a3fc09df82a56ad5d0fba7724193ed1b8f768e8ddc52a.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_paper_e31cc7bc7b21b610_abc425134ef3aef9491a3fc09df82a56ad5d0fba7724193ed1b8f768e8ddc52a.json) | `abc425134ef3aef9491a3fc09df82a56ad5d0fba7724193ed1b8f768e8ddc52a` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_20261002T0346Z/IR_READY_INDEPENDENT_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_20261002T0346Z/IR_READY_INDEPENDENT_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_IR_READY_INDEPENDENT_READBACK.json) | `d92b23b3cf0b3b333738ed7295e68c2aac457d06f4260652c21ab3e32f61c2bc` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_e31cc7bc7b21b610_COORDINATOR_CLOSURE_0810Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_e31cc7bc7b21b610_COORDINATOR_CLOSURE_0810Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_paper_e31cc7bc7b21b610_COORDINATOR_CLOSURE_0810Z.json) | `f8f016162ba5f5002681683718f7bd07faef0c171e47f9a1c45b80cc09cde69b` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_native_excerpt.json) | `eeef5679e7698b7262aca42aca8346c759b05bf105a5e46b995a1db485649670` | native_output |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_native_excerpt.json) | `88d5a63bb8a9bfef285b0603ab7309db9d29a3358edb6ba2abe155c71a844f30` | native_output |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_native_excerpt.json) | `a0ccc6b89798d287c513625a332e3d543653f17f60731b7b498031c90c1af7f2` | native_output |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/state.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/state.fchk) | `78ec8149c287aea70e18b64a9709991c105e48acd84476976dc8f9ffec916a2d` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_native_excerpt.json) | `d82fd5912b81fb5e40e8a412f8939afd76f79f89462e479da7cf88780cd90307` | native_output |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/state.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/state.fchk) | `e3a8e4a307ba75f6c1540b3e7ebd336c9c1f04e5c2e0764bb8621ddc710a6fb2` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/state.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/state.fchk) | `4fbe4ef0c0d62f35fd0c80b47cba565f094fb87198865dee05cb1f735515eb1e` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0065_input.com) | `ec2cbf306e6d8d70bd60cf446dddf3bf0d95a72ffbaecbcbd84bf3e2d8077e51` | input_or_analysis_code |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_input.com) | `9632ce1120e97587d97d1e0efa50d20006723b24153d81a86ea680352a92c4ec` | input_or_analysis_code |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/state.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/state.fchk) | `53eb2bf173d3bc371f95f0a78c24bcd97328dbc230391b9d2211def253b34fad` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/phase_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/phase_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0068_phase_results.json) | `4d012e85dd05b66c8c2dcf2319ef0b34c31435883d88ec0d83372908c14aca1f` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_returned_controls_and_source_geometry_parser_repair/attempt_01/returned_control_analysis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_returned_controls_and_source_geometry_parser_repair/attempt_01/returned_control_analysis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_returned_control_analysis.json) | `42c5ee418b644c4231792d6fbc0923a954cb0c4914937d38271449f55a261386` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_retained_precision_and_TD_targets/attempt_01/precision_controls.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_retained_precision_and_TD_targets/attempt_01/precision_controls.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_precision_controls.json) | `d24d2f94ae1db866ce71b2f12acc97796d49b902676316d83394ce8042774491` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0071_geometry.xyz) | `5373a07cf0532997feadfa37290494dfa1bfcd3a095dfc2f1b1505afd53e6c7a` | input_or_analysis_code |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_geometry.xyz) | `62a02cd4c7df1c0b65a36cacaa216791d917a91257eeda13766e2e4ed2844e65` | input_or_analysis_code |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0075_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_nosymm_optfreq_stable/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0076_input.com) | `9d7aa32a48fac863e61be538aac77b3bb2d02ace026aba024b45233f4d4d9dff` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_analysis.py) | `680849a340329ff214c814ca7b6aa1eb61d6e681bf9e13c11454345d82d92484` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_case.json) | `1e57304fae37d7235bf5dbc2142796adc6ad3126f738692b0f56d80848ce5005` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/paper_e31cc7bc7b21b610.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/paper_e31cc7bc7b21b610.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_paper_e31cc7bc7b21b610.json) | `9ed62f6bb682b4c4b2a1d62e4043c4463c80f325787b05635fcd84d6ac30cbff` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/source_comparisons.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/source_comparisons.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_source_comparisons.json) | `98ba966dc206b654be5fba066b54fd44f69ee6c198f91073499baf056df20e27` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/inputs/v2_Hap54_S4_source_optfreq/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/inputs/v2_Hap54_S4_source_optfreq/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_geometry.xyz) | `5373a07cf0532997feadfa37290494dfa1bfcd3a095dfc2f1b1505afd53e6c7a` | input_or_analysis_code |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/strict_group6_remaining_source_diagnostics/attempt_01/paper_e31cc7bc7b21b610.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/strict_group6_remaining_source_diagnostics/attempt_01/paper_e31cc7bc7b21b610.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_paper_e31cc7bc7b21b610.json) | `cad77ccf1ff89613c4143e149b753d69264b649ea821673774634040cb828917` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/inputs/v2_Hap54_C2h_source_optfreq/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/inputs/v2_Hap54_C2h_source_optfreq/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_geometry.xyz) | `62a02cd4c7df1c0b65a36cacaa216791d917a91257eeda13766e2e4ed2844e65` | input_or_analysis_code |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/paper_e31cc7bc7b21b610/current_report.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_current_report.md) | `02868a612ff16e29954c05efd195dc302ea71bf40bbd10e0d4f9c715c5bd0b76` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/CORRECTION.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/report_reference_repair_20260930/CORRECTION.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_CORRECTION.json) | `90cacb3435931d8e678deef0ded65356a0b396f3b94eac335ecfa3db5b94e82d` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_evidence.csv](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/six_manifold_evidence.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_six_manifold_evidence.csv) | `98604c40eab1e55e08c1217a0848189c7fcea06825da73aebe0ab1da67c21a9d` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0090_reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_FEEDBACK_0710Z.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_FEEDBACK_0710Z.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0091_COORDINATOR_FEEDBACK_0710Z.md) | `9f3add7c602135b22eaf31046d49ca5786e8cdc44e3f6ef7ecde75c2b5b9e26b` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0715Z.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0715Z.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0092_COORDINATOR_G6_REVIEW_0715Z.md) | `7abb1962749f444c42f0db1519673c1f70431684be34136ad8e6169ed5dbef3d` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_Ir1_Ir28_occupancy_B5V01/attempt_01/occupancy.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_Ir1_Ir28_occupancy_B5V01/attempt_01/occupancy.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0093_occupancy.txt) | `8193210a064b66368ab7364621c8f1b4d79c3294f8485d1e849a3ef7b3ed366e` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/B5_V01_readback_checks.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/B5_V01_readback_checks.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0094_B5_V01_readback_checks.json) | `6f23c356a276eb0704001d7f1006bfa209386ee51a1050cd3d4815f641f8d19b` | evidence_or_analysis |
| E0095 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/task_info.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0095_task_info.json) | `614204b621031fb056bd64b77a84083194fb528fc2f351dc903ca731fbf1a58c` | historical_task_binding |
| E0096 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0096_submission_schema.json) | `6cff83af3b27cb2357f664d45356b58e6872d5e62df18e6565a189574be30bdb` | historical_task_binding |
| E0097 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0097_submission_guide.md) | `685c1fb4c870f10aa539968ad910e6fbe6d80cc00f09384ef4ecf574ad6036eb` | historical_task_binding |
| E0098 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0098_scoring_rules.json) | `e28bcd939cb5604ae8147666668246ffff5978617f84aacafa7751a7867748ca` | historical_task_binding |
| E0099 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0099_evidence_map.json) | `b7a64c357cae8c46611b7d61f59a003cf9a448cc09ea5f21b9d6466ac186f7a7` | historical_task_binding |
| E0100 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0100_critical_failures.json) | `1a67f382033ae7eafa39598e69bc4f72556eda4f9b1212c5d0754e8ecc5290ff` | historical_task_binding |
| E0101 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0101_reference_validation_plan.md) | `acf743b2e35f14cb4cfc9e5dbb17ab44f79c8dbd8dbe28b083abf7189d8057c3` | historical_task_binding |
| E0102 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/paper_route.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0102_paper_route.md) | `92b14734600da8b1f7a4ec80f0304aaa1f7076664964fa4ac5353ffc090ad850` | historical_task_binding |
| E0103 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/task_info.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0103_task_info.json) | `a07b934ee66165a694440ebba586096ee48ce0acde44db8739e37cc1cba697b6` | historical_task_binding |
| E0104 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0104_submission_schema.json) | `6cff83af3b27cb2357f664d45356b58e6872d5e62df18e6565a189574be30bdb` | historical_task_binding |
| E0105 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0105_submission_guide.md) | `685c1fb4c870f10aa539968ad910e6fbe6d80cc00f09384ef4ecf574ad6036eb` | historical_task_binding |
| E0106 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0106_scoring_rules.json) | `e28bcd939cb5604ae8147666668246ffff5978617f84aacafa7751a7867748ca` | historical_task_binding |
| E0107 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0107_evidence_map.json) | `b7a64c357cae8c46611b7d61f59a003cf9a448cc09ea5f21b9d6466ac186f7a7` | historical_task_binding |
| E0108 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0108_critical_failures.json) | `1a67f382033ae7eafa39598e69bc4f72556eda4f9b1212c5d0754e8ecc5290ff` | historical_task_binding |
| E0109 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0109_reference_validation_plan.md) | `acf743b2e35f14cb4cfc9e5dbb17ab44f79c8dbd8dbe28b083abf7189d8057c3` | historical_task_binding |
| E0110 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/paper_route.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0110_paper_route.md) | `92b14734600da8b1f7a4ec80f0304aaa1f7076664964fa4ac5353ffc090ad850` | historical_task_binding |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/evidence_mapping.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_e31cc7bc7b21b610/evidence_mapping.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0111_evidence_mapping.json) | `07edad7e0d894da06e193e1bca8d29d7f1508f06b510afbcb0ff5257cbfb8fef` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0735Z.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0735Z.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0112_COORDINATOR_G6_REVIEW_0735Z.md) | `fc923cf78988366469c6f3f74fc09c40af587d01af1460f7066b137f1d4e4e0f` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0113_input.com) | `ba61788574e7dffc46a76eefee103661ca1aad55442c77753b229f7aa30df67c` | input_or_analysis_code |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0114_input.com) | `96d0034faab5b75612f629b3579097bdb23351b984b53555237c26b51bf9e20a` | input_or_analysis_code |
| E0115 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/Egan_identity.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/Egan_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0115_Egan_identity.json) | `098330de3a3d3ae48c4b8833956f7f19cb841962b9b1bb761b1b1f6a523e951f` | historical_task_binding |
| E0116 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/Hap_core_identity.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/Hap_core_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0116_Hap_core_identity.json) | `aecf6cc56c9f5aebdee82130c8609243a4c0ffa162137da7f84f824de80511ed` | historical_task_binding |
| E0117 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/dimer_identity.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/dimer_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0117_dimer_identity.json) | `8c2b95b26622f0022b662253d057e36f8c4528da0f3863e3bac26daa434177b1` | historical_task_binding |
| E0118 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/problem_context.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/agent_input/data/inputs/problem_context.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0118_problem_context.json) | `5dd1964f3a14fc788582cf6d1ecdff177b85257591ff6afdf3b47d347ca9bbb6` | historical_task_binding |
| E0119 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_alpha_egan_IrCl.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_alpha_egan_IrCl.xyz.snapshot) | `d5edd28894bdb2d0095e6d325d5ed70091b581f2280b541069685c722a129a31` | historical_task_binding |
| E0120 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_beta_egan_IrCl.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_beta_egan_IrCl.xyz.snapshot) | `99150501d1ebcb90aca4d4a0b364c36d6a717aafa4d3b4036f717d5a9f7c889b` | historical_task_binding |
| E0121 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot) | `d7f7e4f2999aad7a3d791e938463991849ab12148f1d50b24576be6c226d07f0` | historical_task_binding |
| E0122 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot) | `ebdc8bb22a7cdb27d6dcd6ef80b5c5b9aab3a3b532bdb08259d2f9c359c05565` | historical_task_binding |
| E0123 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot) | `ed3872a1adf5a7afac1a9ab7f1244942006cb182fee2c2dc451d1e1e85ebbefd` | historical_task_binding |
| E0124 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot) | `ca2b51375509b329b1029be8f439ca688f4d72a7cb01230443b6bb6ce6cbb7a5` | historical_task_binding |
| E0125 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot) | `8c5be11aafa4a8141c8488ee0a2878bfac1058f3504872da0bf6e56d10ecd2b8` | historical_task_binding |
| E0126 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot) | `7ba19d5fa3b4263b5801632b33db60c9c6147c83a81181fa77c4849870771cc5` | historical_task_binding |
| E0127 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot) | `f3928e9d1e8584701dd2c1a79d8a8853b110453252348680761157cbfa4f8be6` | historical_task_binding |
| E0128 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/historical_result_schema_mapping.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/historical_result_schema_mapping.json.snapshot) | `17cf6e140309431bb1a40a0dd31b831d42f0dca613691d10b72c5c6126a160b0` | historical_task_binding |
| E0129 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/maintenance_audit.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/maintenance_audit.md.snapshot) | `e5e2ed4ad535fc25f9363ba9f85b151b3b6db72cb749c0d800186571e4a1769e` | historical_task_binding |
| E0130 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/structure_provenance.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/structure_provenance.json.snapshot) | `945a62f17b2af658906d8ca2c2fdfd09c45f89e7b74e5c5648590aa390ea01f9` | historical_task_binding |
| E0131 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `de5e727984ea7424557c48b12ec38243dc0eeeef0027199d50272175094284bf` | historical_task_binding |
| E0132 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/package_manifest.json.snapshot) | `ba13b67f9f52e58e557a342791931c45a59afe31cfbb3bc8c398c574d4339a62` | historical_task_binding |
| E0133 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/paper_route.md.snapshot) | `cc55a0cce0419c7c10d584b159f03a6008eb59afc98f2ecec788b3abc25684c9` | historical_task_binding |
| E0134 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/task_info.json.snapshot) | `533ae32520237a992119cf31c7fb213349185860711f8604aecc399850bdf470` | historical_task_binding |
| E0135 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/Egan_identity.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/Egan_identity.json.snapshot) | `1f4d53905f1b8ea751ca2e63d892b7f07c83a75f283fae41ef60549ed73893cc` | historical_task_binding |
| E0136 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/dimer_definition.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/dimer_definition.json.snapshot) | `3bbf3f6d6602736b6aea5a84ca62f8b25b247a3cf4993a08841f3488c1f1e569` | historical_task_binding |
| E0137 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/egan_identity.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/egan_identity.json.snapshot) | `053ac8b7f89be0761b770365d7e79e78cc872bf4d896cff49094cdca22bc8d27` | historical_task_binding |
| E0138 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/retained_heavy_mapping.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/retained_heavy_mapping.json.snapshot) | `d538e5d05feaf32ddf9c46e8d57e4333c8e555296f1b234c71d7b5b0fd06aa0d` | historical_task_binding |
| E0139 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/study_scope.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/study_scope.json.snapshot) | `f6c191a3888afdcfe63fec66ab102b4b3578d719ea5ed860461133ae142b94b2` | historical_task_binding |
| E0140 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_guide.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_guide.md.snapshot) | `0f5e0b90e502305274e92ef5849a01a6f7c0bc0c2aefb33fec1fa9acde090365` | historical_task_binding |
| E0141 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_schema.json.snapshot) | `6c0680b353ab579e345a8d7aa1a17fbdc507852b4253dcaf0cd6ff224b673cce` | historical_task_binding |
| E0142 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/task.md.snapshot) | `29e41e81e5b1e7ec4813cd69f117e752977f741fa43eef755712849230d12e7b` | historical_task_binding |
| E0143 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/critical_failures.json.snapshot) | `975a9dc51c8314f9fba1bbccb1f67a5fb57cfefdcbc0785bf713b683e6f3dfdd` | historical_task_binding |
| E0144 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/evidence_map.json.snapshot) | `2fac6923a5993453d0d3205cfced2a83e7b4833090c94dd5a3aa0e1059170762` | historical_task_binding |
| E0145 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_conclusions.json.snapshot) | `87a79be48812fe35f44e919d6f0e399157c065b9254f7a2251f60d8e569b4b35` | historical_task_binding |
| E0146 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_key_points.json.snapshot) | `86dc7a6061ad1482df652a34f830c6cb394a456f1e54e8b47895e1566fc70c44` | historical_task_binding |
| E0147 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_validation_plan.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_validation_plan.md.snapshot) | `22fd69f9352ea54d8ceb1a4929c87473e951459aa503ac6ed1251e43fa7c9e37` | historical_task_binding |
| E0148 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/scoring_rules.json.snapshot) | `e49176e7bcc37ae580ef4dc305759cde72dd20d7100e8d31233b34a9d80de4cb` | historical_task_binding |
| E0149 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/package_manifest.json.snapshot) | `4e0c310a5aca14567a8e24e05a030c19138b4214d2bd8bf05bab1a3e9906a506` | historical_task_binding |
| E0150 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/paper_route.md.snapshot) | `bffa6f7b20fdcf1b7141135187bbca787a7187d0b6645675a7e8c2fc1f8569dd` | historical_task_binding |
| E0151 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/task_info.json.snapshot) | `38f44f94274629f5cbb8f9d1b27c1c84aa1e29338fd0c8ccd42d4409e02574d1` | historical_task_binding |
| E0152 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/evidence_reuse_inventory.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/evidence_reuse_inventory.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0152_evidence_reuse_inventory.json) | `0fe228dc8526898258ea1c54ad41b13a5a254977936d2967d8dda0d185895eb9` | historical_task_binding |
| E0153 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/integrity_repair_20260930.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/integrity_repair_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0153_integrity_repair_20260930.json) | `29b5b58664886214247204491a8dc37ee82657398e7aaa3be7c68438f07d2153` | historical_task_binding |
| E0154 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/public_visibility_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/public_visibility_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0154_public_visibility_audit.json) | `04e73e540e0d3385ea41e9ad072ef8336d1ddd45511620f68cfc79458ebc798b` | historical_task_binding |
| E0155 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0155_source_scope_audit.json) | `7105fd640cfe9ff05307b0bec555759f1e77bfb2d2db8e5a89e70577a2844107` | historical_task_binding |
| E0156 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0156_source_scope_audit.md) | `7105fd640cfe9ff05307b0bec555759f1e77bfb2d2db8e5a89e70577a2844107` | historical_task_binding |
| E0157 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/upgrade_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/upgrade_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0157_upgrade_audit.json) | `b255b63b0225399995c518c81ecdc737b8cc83620e61393c5f9352d555fa64e1` | historical_task_binding |
| E0158 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_design_audit.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_design_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0158_v2_design_audit.md) | `9c13fc161899897efe24194c13515e6f07a9de88a3e7df40c8ad3fdc0b57d52e` | historical_task_binding |
| E0159 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_upgrade_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_upgrade_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0159_v2_upgrade_audit.json) | `57ae489647fb6daf0647eb0316ef0c80a2e8cc4bffb51e292eae4438c28a8993` | historical_task_binding |
| E0160 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/Egan_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/Egan_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0160_Egan_identity.json) | `098330de3a3d3ae48c4b8833956f7f19cb841962b9b1bb761b1b1f6a523e951f` | historical_task_binding |
| E0161 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/Hap_core_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/Hap_core_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0161_Hap_core_identity.json) | `aecf6cc56c9f5aebdee82130c8609243a4c0ffa162137da7f84f824de80511ed` | historical_task_binding |
| E0162 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/dimer_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/dimer_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0162_dimer_identity.json) | `8c2b95b26622f0022b662253d057e36f8c4528da0f3863e3bac26daa434177b1` | historical_task_binding |
| E0163 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/problem_context.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/agent_input/data/inputs/problem_context.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0163_problem_context.json) | `5dd1964f3a14fc788582cf6d1ecdff177b85257591ff6afdf3b47d347ca9bbb6` | historical_task_binding |
| E0164 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_alpha_egan_IrCl.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_alpha_egan_IrCl.xyz.snapshot) | `d5edd28894bdb2d0095e6d325d5ed70091b581f2280b541069685c722a129a31` | historical_task_binding |
| E0165 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_beta_egan_IrCl.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/data/inputs/cis_beta_egan_IrCl.xyz.snapshot) | `99150501d1ebcb90aca4d4a0b364c36d6a717aafa4d3b4036f717d5a9f7c889b` | historical_task_binding |
| E0166 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot) | `8fb33c7b212efd42f7321b212d37a34e1eea3af6e147337dd704d7df21ca1879` | historical_task_binding |
| E0167 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot) | `30f47c32355d51f3be13400091e7a8fea38c9df4cb49173cb9a1647f9520d4c6` | historical_task_binding |
| E0168 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot) | `a44cef71c87ef37415b968b70528d356ed1b3316a9eac52455756b096faf3c03` | historical_task_binding |
| E0169 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot) | `981689912015b3104a5490427ac4de078e75c9bc1d18d664364ecef820c7a876` | historical_task_binding |
| E0170 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot) | `5f6f581e70b5f13b3b9c897efcaa323d384f47406eb879fbd790c4febc51b59c` | historical_task_binding |
| E0171 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot) | `1c1bd5118c9ef684af390c0603db4bb0fae7e4bc02236de36931cb7e56b004d9` | historical_task_binding |
| E0172 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot) | `1105d91ef5e6db73867b0291877dcc9ceb5abfca537a300435cb48a69bec44b7` | historical_task_binding |
| E0173 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/maintenance_audit.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/maintenance_audit.md.snapshot) | `34f44c1fd867dcc2b212a2e7a5af0e7b73eaa3b10a9040e3597732dee5253dc4` | historical_task_binding |
| E0174 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/structure_provenance.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/task_provenance/structure_provenance.json.snapshot) | `d36b6dc949ab63aaa448a164d0cd3b54cb546dfbfa57c37063249d1886bffd9e` | historical_task_binding |
| E0175 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `1bc826e066d1546d69bdf19fbea2d091e0da49a59b9b9c1d01af6ac3daf72eac` | historical_task_binding |
| E0176 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/package_manifest.json.snapshot) | `4d9bf588cc64858089f6bf7e01c4beabd14c78d9b949f35abf136b6743ab1921` | historical_task_binding |
| E0177 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/paper_route.md.snapshot) | `cc55a0cce0419c7c10d584b159f03a6008eb59afc98f2ecec788b3abc25684c9` | historical_task_binding |
| E0178 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_final_snapshot/task_info.json.snapshot) | `f74d0ccecf39381f13fd56ebbd4edee13ae4cb81907f854f429338755acd1cde` | historical_task_binding |
| E0179 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/Egan_identity.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/Egan_identity.json.snapshot) | `1f4d53905f1b8ea751ca2e63d892b7f07c83a75f283fae41ef60549ed73893cc` | historical_task_binding |
| E0180 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/dimer_definition.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/dimer_definition.json.snapshot) | `3bbf3f6d6602736b6aea5a84ca62f8b25b247a3cf4993a08841f3488c1f1e569` | historical_task_binding |
| E0181 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/egan_identity.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/egan_identity.json.snapshot) | `053ac8b7f89be0761b770365d7e79e78cc872bf4d896cff49094cdca22bc8d27` | historical_task_binding |
| E0182 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/retained_heavy_mapping.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/retained_heavy_mapping.json.snapshot) | `d538e5d05feaf32ddf9c46e8d57e4333c8e555296f1b234c71d7b5b0fd06aa0d` | historical_task_binding |
| E0183 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/study_scope.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/data/inputs/study_scope.json.snapshot) | `f6c191a3888afdcfe63fec66ab102b4b3578d719ea5ed860461133ae142b94b2` | historical_task_binding |
| E0184 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_guide.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_guide.md.snapshot) | `0f5e0b90e502305274e92ef5849a01a6f7c0bc0c2aefb33fec1fa9acde090365` | historical_task_binding |
| E0185 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/submission_schema.json.snapshot) | `6c0680b353ab579e345a8d7aa1a17fbdc507852b4253dcaf0cd6ff224b673cce` | historical_task_binding |
| E0186 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/agent_input/task.md.snapshot) | `f5bf7f9af49db0b560126e242ad0bd05dbc76eddda00e1f8374355434c91d7b7` | historical_task_binding |
| E0187 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/critical_failures.json.snapshot) | `975a9dc51c8314f9fba1bbccb1f67a5fb57cfefdcbc0785bf713b683e6f3dfdd` | historical_task_binding |
| E0188 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/evidence_map.json.snapshot) | `2fac6923a5993453d0d3205cfced2a83e7b4833090c94dd5a3aa0e1059170762` | historical_task_binding |
| E0189 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_conclusions.json.snapshot) | `87a79be48812fe35f44e919d6f0e399157c065b9254f7a2251f60d8e569b4b35` | historical_task_binding |
| E0190 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_key_points.json.snapshot) | `86dc7a6061ad1482df652a34f830c6cb394a456f1e54e8b47895e1566fc70c44` | historical_task_binding |
| E0191 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_validation_plan.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/reference_validation_plan.md.snapshot) | `22fd69f9352ea54d8ceb1a4929c87473e951459aa503ac6ed1251e43fa7c9e37` | historical_task_binding |
| E0192 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/evaluation/scoring_rules.json.snapshot) | `e49176e7bcc37ae580ef4dc305759cde72dd20d7100e8d31233b34a9d80de4cb` | historical_task_binding |
| E0193 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/package_manifest.json.snapshot) | `3b3e18b38a2420c6b95ab1315fb1bd4b0f6372427fd9662f3cb3bcf5993f1bb7` | historical_task_binding |
| E0194 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/paper_route.md.snapshot) | `bffa6f7b20fdcf1b7141135187bbca787a7187d0b6645675a7e8c2fc1f8569dd` | historical_task_binding |
| E0195 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/legacy_v1_snapshot/task_info.json.snapshot) | `10ef88733a6fd55d2c98eff04395a3398a096c9969786773fb7303998aa62fda` | historical_task_binding |
| E0196 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/evidence_reuse_inventory.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/evidence_reuse_inventory.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0196_evidence_reuse_inventory.json) | `0fe228dc8526898258ea1c54ad41b13a5a254977936d2967d8dda0d185895eb9` | historical_task_binding |
| E0197 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/integrity_repair_20260930.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/integrity_repair_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0197_integrity_repair_20260930.json) | `14fd855b10bfad778ae561673f2bf6ba2045c9fe32a2ed6667cfbbb8fbbd52ac` | historical_task_binding |
| E0198 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/public_visibility_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/public_visibility_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0198_public_visibility_audit.json) | `04e73e540e0d3385ea41e9ad072ef8336d1ddd45511620f68cfc79458ebc798b` | historical_task_binding |
| E0199 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0199_source_scope_audit.json) | `1d9da01d67cff80a1216060e42ec3edd60ae8123d6baafcc78c6ffd87fe5b956` | historical_task_binding |
| E0200 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/source_scope_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0200_source_scope_audit.md) | `1d9da01d67cff80a1216060e42ec3edd60ae8123d6baafcc78c6ffd87fe5b956` | historical_task_binding |
| E0201 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/upgrade_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/upgrade_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0201_upgrade_audit.json) | `963a0133dc4c5a078450a28e728f1fbd42da051dc7ce60aa70637b9504462c2a` | historical_task_binding |
| E0202 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_design_audit.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_design_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0202_v2_design_audit.md) | `9c13fc161899897efe24194c13515e6f07a9de88a3e7df40c8ad3fdc0b57d52e` | historical_task_binding |
| E0203 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_upgrade_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e31cc7bc7b21b610/evaluation/task_provenance/v2_upgrade_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0203_v2_upgrade_audit.json) | `396c65f0b75079192ed6da6c1b72d1031b5eed8bf096e7b256aa34b52dddce15` | historical_task_binding |
| E0204 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0204_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0205 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_unrestricted_stability/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0205_input.com) | `7982c717ebadfd5fd203e98590fe777bc8798a184d19c253b4c468e7b3d1f1a9` | input_or_analysis_code |
| E0206 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0206_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0207 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_C2h_unrestricted_stability/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0207_input.com) | `7982c717ebadfd5fd203e98590fe777bc8798a184d19c253b4c468e7b3d1f1a9` | input_or_analysis_code |
| E0208 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0208_geometry.xyz) | `5373a07cf0532997feadfa37290494dfa1bfcd3a095dfc2f1b1505afd53e6c7a` | input_or_analysis_code |
| E0209 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_UltraFine_force/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0209_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0210 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0210_geometry.xyz) | `5373a07cf0532997feadfa37290494dfa1bfcd3a095dfc2f1b1505afd53e6c7a` | input_or_analysis_code |
| E0211 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_S4_source_fixed_SuperFineGrid_force/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e31cc7bc7b21b610/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0211_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0212 | [.software_cache/installations/gaussian/g16/install/g16/cubegen](../../../../.software_cache/installations/gaussian/g16/install/g16/cubegen) | `e900c5d4d6d7d95bc6eb766e9004d8e76c8051335535e31e706fcbf296759f95` | evidence_or_analysis |
| E0213 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/wavefunction.fchk) | `4fbe4ef0c0d62f35fd0c80b47cba565f094fb87198865dee05cb1f735515eb1e` | evidence_or_analysis |
| E0214 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO118.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO118.values) | `671e6217182bcf1ba83b59d5c4ae1842a329ed82ff3f5dafa607ab2fe00fbc56` | evidence_or_analysis |
| E0215 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO119.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO119.values) | `f21326320925cbeb5cf5121b2c92e5ebb0224a6fb64b32a7c1b1101d5413b8d8` | evidence_or_analysis |
| E0216 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO122.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO122.values) | `d695e9bbda7972ec08f0a9dcb2fe7c0680e4a626618ae716766a3774a7701fd2` | evidence_or_analysis |
| E0217 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO123.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO123.values) | `f18307035af3a95a5bce23fa4c9e2b630e470d0e90702ea6eb29c6207381277b` | evidence_or_analysis |
| E0218 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO126.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO126.values) | `0e0edf32403ac80ed321ecce52d9ea689713119fab874e09d9b0e412ff293e9c` | evidence_or_analysis |
| E0219 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO127.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO127.values) | `fc57829f4f4f7535838113f6372fdf6f9699865ccccea5ab85ba629a8bc916f3` | evidence_or_analysis |
| E0220 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO128.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO128.values) | `edbfec64c920b058e6a4b035bb642bc233d5518af904ca7b044a148a38e8d9b1` | evidence_or_analysis |
| E0221 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO129.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO129.values) | `57ac576043edf576408a82c6c7a0f6896793e52419970e9b0b0be1308ae1c589` | evidence_or_analysis |
| E0222 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO130.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO130.values) | `1a45c50916e3f8fab28fccad9125e740d96f3518faeb11d5974d50803cf9f8b9` | evidence_or_analysis |
| E0223 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO131.values](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/v2_Hap54_S4_six_manifold_native_phase/attempt_01/MO131.values) | `8d2187522e07405c95586f6bc1ff124ee5fed05201e24cec24070fcffe5d49a6` | evidence_or_analysis |
| N0214 | [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` | latest_review_evidence |
| N0215 | [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` | latest_review_evidence |
| N0216 | [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json](scoring_rules.json) | `e28bcd939cb5604ae8147666668246ffff5978617f84aacafa7751a7867748ca` | latest_review_evidence |
| N0217 | [tasks/v2_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` | latest_review_evidence |
| N0218 | [tasks/v2_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` | latest_review_evidence |
| N0219 | [tasks/v2_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json) | `e28bcd939cb5604ae8147666668246ffff5978617f84aacafa7751a7867748ca` | latest_review_evidence |
| N0220 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0221 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/agent_input/task.md](../agent_input/task.md) | `5f28894903e884880b9390605d62687177072f4c639fb68b29cf8d3d8b5da922` |
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_key_points.json](reference_key_points.json) | `dbd015415b6e186752340717ad4f6d40f943b2ca7a284dc046e16ca776197f38` |
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_conclusions.json](reference_conclusions.json) | `e15cb7cef1a35d930cd043d418182f3d25d638c32be2f56d6d1caff7b2692656` |
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/scoring_rules.json](scoring_rules.json) | `e28bcd939cb5604ae8147666668246ffff5978617f84aacafa7751a7867748ca` |
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/critical_failures.json](critical_failures.json) | `1a67f382033ae7eafa39598e69bc4f72556eda4f9b1212c5d0754e8ecc5290ff` |
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/evidence_map.json](evidence_map.json) | `b7a64c357cae8c46611b7d61f59a003cf9a448cc09ea5f21b9d6466ac186f7a7` |
| [tasks/v2_autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `b1c9c6dafbf9d71f055647945f602473444d6ef0f4e5b99d5bf00c3fbf6acdb4` |

## Current scoring migration — 2026-10-19
Active paper_science_v2: 100 binary scientific-result points, intermediate findings plus final conclusions. Historical weights/freezes are superseded only as scoring policy. No process score or multiplier. No new chemical calculation or validation. Acceptance: PASS_STRICT_CURRENT_FROZEN_SCOPE. C2h has one imaginary mode, not a second metastable minimum. Native 9.750242 kcal/mol is +0.050242 relative to source 9.7; joint printed/native precision explains the boundary issue, not exact identity. Correct Ir pairs differ by ordering (S4 1/2, C2h 1/28). Failed composition module rc59 is not complete evidence; successful Mayer/occupancy and orbital-direction readbacks substantiate the retained claims. Scalar ECP Hap evidence does not establish SOC, full-Egan quantitative identity, or exact bond order 2.34.


## 2026-10-19 — Round 3 scoring-contract repair (not a chemical acceptance update)

The original verification history above remains verbatim. Current scoring uses the physical object/state/reference definitions in scoring_rules.json; author software and previous user acceptance are evaluator provenance, not facts a new agent must report. Numeric targets, tolerances, recorded residuals, reference acceptance status and scientific scope are unchanged. PR still addresses the disclosed baseline. Relevant final-claim evidence is assessed directly rather than requiring every intermediate numeric window or an unrelated branch to pass.
The 35-point final orbital/geometry/energy synthesis is retained: it adds the orientation-dependent filled/empty overlap explanation rather than repeating a distance. It remains a binary integrated proposition; calibration of partial evidence is an explicitly retained limitation, not an excuse to manufacture new weighted findings.

# 2026-10-28 V3 最终命题与证据复用

保留三成员分子交换科学范围，最终6条/100分：三个J、两个独立差分及一个电子解释；取消重叠电子态单独计分和原题未明确要求的人口评分。

r_j_h/r_j_me/r_j_ome：源几何 J=-334.370777/-341.412046/-344.582322 cm^-1，独立优化 J=-332.127051/-339.665675/-342.919948，均在原 ±10 窗内。r_me_h_effect/r_ome_me_effect：独立优化差为 -7.538624/-3.254273，条件半宽0.791650/0.790975。r_family_answer：H NTO 61.509881/38.290914% 与三成员 SF 态/几何比较支持耦合电子态解释；唯一因果分解未证明。旧 thermal_implication 为正文有依据但原公开题面未要求的隐藏输出，现仅保留非评分背景，不据此扩题。

限制：Me/OMe 没有对应几何的完整 Hessian；条件求根残差不代表总泛函/几何误差；材料拟合Me/OMe顺序不可替代分子顺序。历史严格通过限旧冻结范围，本轮不重验。

本轮未运行新计算；下列历史正文逐字保留，旧 PASS/V2 评分不构成本版全面通过。

---

# V2 验证计算参考：Cu2三成员磁交换

论文：`paper_0cd74ae20ab933f3`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：当前分子交换比较覆盖完整且符合源分子结果；材料实验Me/OMe名义排序不同，不外推。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

完整H/Me/OMe Cu2分子的取代相关交换差异及其可分辨性。

冻结题面中的科学目标：

Determine whether axial-pyridine substitution produces resolvable changes in the molecular magnetic exchange of the three supplied copper dimers, and what the evidence supports about that dependence.

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_0cd74ae20ab933f3/documents/main.pdf](../../../../papers/paper_0cd74ae20ab933f3/documents/main.pdf) | `e74146ea380e78e6bca3a1ca6eeb56ec4a16487ac58d2f169c0f92f64efea2aa` |
| [papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf](../../../../papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf) | `dd357023aa433eeb80376b2b8f11e44a332edd2d95cdc8809838e6f3a448c222` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

ORCA作者B3LYP-D3BJ/def2-SVP结构路线；PySCF-forge多共线SF；原SI几何与独立优化几何分别核验。

1. 由正文和 SI 建立 H/Me/OMe 三个完整中性 Cu2 模型，保留四个桥与两个轴向配体；分别核对 128/134/136 个原子、602/618/634 个电子。源 XYZ 与后续 ORCA 作者方法优化坐标分别登记，不混为同一个几何。

2. 按 B3LYP-D3BJ/def2-SVP 三重参考完成几何优化，在源几何和独立优化几何上实际执行 PySCF-forge 多共线 spin-flip 计算。按自旋与态性质辨认物理 singlet/triplet 根，保留 TDA/full-SF 对照和 Ritz 残差。Me/OMe 无对应几何的完整 Hessian，不将这些几何称为频率认证最低点。

3. 从 SF 两个物理态能量计算 J=E(S)−E(T)，按同一 Eh→cm⁻¹ 换算；禁止用 UKS 参考能量替代 SF triplet。源几何 J 为 −334.370777/−341.412046/−344.582322 cm⁻¹，独立优化后为 −332.127051/−339.665675/−342.919948 cm⁻¹。

4. 逐对计算 Me−H、OMe−H、OMe−Me 的差，并从实际残差建立有条件的数值界；新几何差为 −7.538624/−10.792897/−3.254273 cm⁻¹，对应半宽 0.791650/0.768307/0.790975。以源几何、full-SF 和新几何共同检验排序，不将绝对 J 的旧容差当作小取代效应的分辨率。

5. 结合 H-NTO 通道及几何敏感性，支持该分子系列反铁磁交换增强的有限结论；几何/电子因素尚耦合，不声称唯一取代因果、完整误差界或材料磁性预测。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| 源几何J(H/Me/OMe), cm^-1 | [-335,-342,-345] | [-334.3707768,-341.4120458,-344.5823217] | 实算−论文：[0.6292232,0.5879542,0.4176783]； SI整数结果与真实响应吻合到约0.2%；不是用±20容差掩盖小取代差。；源定位：SI S36 Table S4 |
| 独立优化J, cm^-1 | [-335,-342,-345] | [-332.1270511,-339.6656751,-342.9199484] | 实算−论文：[2.8729489,2.3343249,2.0800516]； 实测几何影响1.66–2.24cm^-1；三组差均有不跨零的独立残差区间，排序在源/优化及full-SF保持。；源定位：SI S5–6,S36 |
| H NTO主要权重,% | [62,38] | [61.509881,38.290914] | 实算−论文：[-0.490119,0.290914]； 两主通道一致，余0.199206%保留。；源定位：SI Fig.S44 |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| J, H/Me/OMe (cm−1) | [-335,-342,-345] | [-334.3707768,-341.4120458,-344.5823217] | Source Table S4 versus native SF on source coordinates; J=E(S)−E(T). Source-coordinate residuals are 0.42–0.63 cm−1. The historical ±20 cm−1 absolute-J criterion is only secondary context and is never applied to the small substitution differences. |
| J, H/Me/OMe (cm−1) | [-335,-342,-345] | [-332.1270511,-339.6656751,-342.9199484] | Same SF definition on separately optimized full models. Absolute shifts of about 2–3 cm−1 are consistent with the measured geometry/control sensitivity; the independent differential bounds support the scientific comparison. |
| Me−H / OMe−H / OMe−Me (cm−1) | [-7,-10,-3] | [-7.538624,-10.792897,-3.254273] | Pairwise differences of the same J definition. All corresponding conditional residual intervals exclude zero; source-coordinate differences −7.041269/−10.211545/−3.170276 and full-SF results retain the pattern. These are conditional numerical bounds, not calibrated total DFT uncertainty. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_scope — Identity and scope

冻结要求：Keep all four anionic bridges and both axial ligands unless explicitly studying a justified model with its limitations. Identify the electronic states represented by each energy, demonstrate relevant state validity, and make any spin projection and exchange convention auditable. Comparisons of substitution effects require comparable definitions and physical conditions.

当前复审：完整四桥/两轴向配体和S/T态、电子数及J符号已绑定。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Full source graphs, charges, triplet references, physical SF roots and J convention are explicit."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S5–S6；正文物理页6–7；当前V2物种定义",
    "actual_result": "128/134/136原子，602/618/634电子，q0、Sz=1三重态参考，完整4桥和2轴向配体；J=ES(SF)−ET(SF)，Hspin=−J S1·S2+常数，负J为AFM。",
    "reason": "物种、几何谱系及实际态身份均绑定；不用UKS参考替代SF triplet，不把分子量当材料拟合量。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_0cd74ae20ab933f3/source_graph_response_reanalysis.json",
        "sha256": "a740ffe2b3a0318784fdd3222f47c209b201a7ca37efb9bdec12614cb6296f64"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/Cu_author_geometry_closeout.json",
        "sha256": "fcd428a2f1a760469a1e3cde183951eda69974185a444a285ede74d27cd92d22"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_NATIVE_ACCEPTANCE.json",
        "sha256": "58de3420adca79f2cc3b34b61c4f27308d61f1c9361997604fbef1a0589fbd0f"
      }
    ]
  }
]
```

### kp_measure — Quantitative scientific results

冻结要求：Quantify the source-family exchange response with actual state-resolved raw evidence and explicit Hamiltonian/sign/unit conventions; report which members and conditions the evidence covers. A supported inability to resolve small differences is acceptable when its uncertainty is assessed.

当前复审：三个本轮读回result.json给出物理S/T根、独立残差<1e-6Eh和J；三成员均完成。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Source/native J and all three pairwise changes are reconstructed from recorded energies, not copied source labels."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S6 SF差定义；S35–S36 Table S4；协调2026-10-07优化→响应要求",
    "actual_result": {
      "sourceXYZ_J_cm1": [
        -334.370776795852,
        -341.4120458021902,
        -344.582321703863
      ],
      "new_geometry_J_cm1": [
        -332.12705114751003,
        -339.6656751112256,
        -342.9199483814662
      ],
      "new_geometry_three_pairs": [
        {
          "a": "H",
          "b": "CH3",
          "new_delta_cm1": -7.538623963715565,
          "new_conditional_halfwidth_cm1": 0.7916504731723359,
          "new_interval_cm1": [
            -8.330274436887901,
            -6.74697349054323
          ],
          "sign_resolved_under_Hermitian_state_association": true,
          "old_sourceXYZ_delta_cm1": -7.0412690063382115,
          "source_table_delta_cm1": -7.0,
          "geometry_effect_on_delta_cm1": -0.4973549573773539,
          "same_signed_order_as_sourceXYZ": true,
          "old_sourceXYZ_conditional_halfwidth_cm1": 0.4171766029837136,
          "old_sourceXYZ_fullSF_delta_cm1": -6.850448428681489
        },
        {
          "a": "H",
          "b": "OCH3",
          "new_delta_cm1": -10.792897233956182,
          "new_conditional_halfwidth_cm1": 0.7683067211488115,
          "new_interval_cm1": [
            -11.561203955104993,
            -10.024590512807372
          ],
          "sign_resolved_under_Hermitian_state_association": true,
          "old_sourceXYZ_delta_cm1": -10.211544908010978,
          "source_table_delta_cm1": -10.0,
          "geometry_effect_on_delta_cm1": -0.581352325945204,
          "same_signed_order_as_sourceXYZ": true,
          "old_sourceXYZ_conditional_halfwidth_cm1": 0.40980943187150987,
          "old_sourceXYZ_fullSF_delta_cm1": -10.008513111928778
        },
        {
          "a": "CH3",
          "b": "OCH3",
          "new_delta_cm1": -3.254273270240617,
          "new_conditional_halfwidth_cm1": 0.7909751011010814,
          "new_interval_cm1": [
            -4.045248371341699,
            -2.4632981691395357
          ],
          "sign_resolved_under_Hermitian_state_association": true,
          "old_sourceXYZ_delta_cm1": -3.170275901672767,
          "source_table_delta_cm1": -3.0,
          "geometry_effect_on_delta_cm1": -0.08399736856785012,
          "same_signed_order_as_sourceXYZ": true,
          "old_sourceXYZ_conditional_halfwidth_cm1": 0.8225778933510323,
          "old_sourceXYZ_fullSF_delta_cm1": -3.1580646832472894
        }
      ]
    },
    "reason": "三成员新旧同定义响应全部完成，SCF、物理S/T、态连续性和最终独立残差逐一满足；H补齐原缺项。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume3_Cu_final_physical_root_precision/attempt_01/Cu_final_physical_root_precision.json",
        "sha256": "1950265dfa75c118b4616d782b07283e5e5c48a4d789455d07ae21b070897f94"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/Cu_three_member_geometry_source_comparison.json",
        "sha256": "23905de662507185952b71d872bc5ad9c706d0f19e654c12e960060de46866bc"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_NATIVE_ACCEPTANCE.json",
        "sha256": "58de3420adca79f2cc3b34b61c4f27308d61f1c9361997604fbef1a0589fbd0f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/result.json",
        "sha256": "639bbec93377e5f8fe131d81d1b84432836a5a49acaeba86cd68ed8959718ab8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/CH3/result.json",
        "sha256": "1092f171e94d7bfe38953a740ccd8eed155f77768ee5ae5d8ba4f4ceff7dac65"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/OCH3/result.json",
        "sha256": "3ce380356833d4f8c833b570bad8c99a1bc0f661b37dc3d2c2061a3d02d89e97"
      }
    ]
  }
]
```

### kp_explain — Evidence that distinguishes the claimed explanation

冻结要求：Support the explanation of any observed difference with a research design that actually distinguishes its claimed cause from relevant confounding effects. No common-core operation, SF implementation or fixed calibration member is required. Merely comparing three unvalidated energies is insufficient.

当前复审：源/优化几何与TDA/full-SF对照支持有限分子系列关联；没有单一电子因果强结论。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Source-coordinate versus reoptimized and full-SF controls distinguish a reproducible family effect from root/convergence/geometry artifacts; they do not uniquely isolate an electronic substituent mechanism."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S35方法/几何敏感性、S36 Fig.S44及当前V2解释节点",
    "actual_result": "固定源几何TDA/fullSF对照保持三对符号；固定响应方法的源/优化几何对照也保持三对符号。H-NTO61.509881/38.290914%支持混合spin-flip通道，余0.199206%保留。",
    "reason": "实际对照排除了已测求根误差、TDA/fullSF选择和这次几何更新导致的排序反转；说明的是模型内稳健关联，不是未实验就宣称纯电子原因或普遍不可识别。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/Cu_three_member_geometry_source_comparison.json",
        "sha256": "23905de662507185952b71d872bc5ad9c706d0f19e654c12e960060de46866bc"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261004/CU_FINAL_TEN_NODE_REVIEW.json",
        "sha256": "0b31d95a89408e01ecb309827dc085cd725089de52682099a351a316c9904a89"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/Cu_H_source_NTO_readback.json",
        "sha256": "5d4da2f47dbf6141912866d43d70248a4deea3bcaa7602ca11d0517eba0a53e7"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_0cd74ae20ab933f3/source_graph_response_reanalysis.json",
        "sha256": "a740ffe2b3a0318784fdd3222f47c209b201a7ca37efb9bdec12614cb6296f64"
      }
    ]
  }
]
```

### kp_robust — Uncertainty and limits

冻结要求：Assess uncertainty relevant to the sign, ordering and size of the claimed differences. If methods or spin states disagree, investigate and delimit the inference; do not choose a winner by reproducing the source number.

当前复审：差分半宽0.79165/0.76831/0.79098cm^-1小于取代差7.54/10.79/3.25；总体模型误差单列。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Conditional root-residual halfwidths for Me−H, OMe−H, OMe−Me are 0.791650/0.768307/0.790975 cm−1, below their 7.538624/10.792897/3.254273 cm−1 magnitudes; model sensitivity and missing Hessians remain explicit."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S35–S36；当前V2不确定性要求",
    "actual_result": {
      "new_pair_intervals_cm1": [
        [
          -8.330274436887901,
          -6.74697349054323
        ],
        [
          -11.561203955104993,
          -10.024590512807372
        ],
        [
          -4.045248371341699,
          -2.4632981691395357
        ]
      ],
      "new_geometry_J_changes_cm1": [
        2.2437256483419787,
        1.7463706909646248,
        1.6623733223967747
      ],
      "pair_changes_cm1": [
        -0.4973549573773539,
        -0.581352325945204,
        -0.08399736856785012
      ]
    },
    "reason": "全部新独立残差<1e-6Eh；条件区间不跨零。数值界只约束固定Hermitian算符与正确态对应，投影Hermiticity不是全空间证明；fullSF非Hermitian不套用同一界。已量化几何影响，不用RMSD替代J误差。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/Cu_three_member_geometry_source_comparison.json",
        "sha256": "23905de662507185952b71d872bc5ad9c706d0f19e654c12e960060de46866bc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume3_Cu_final_physical_root_precision/attempt_01/Cu_final_physical_root_precision.json",
        "sha256": "1950265dfa75c118b4616d782b07283e5e5c48a4d789455d07ae21b070897f94"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_NATIVE_ACCEPTANCE.json",
        "sha256": "58de3420adca79f2cc3b34b61c4f27308d61f1c9361997604fbef1a0589fbd0f"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261004/CU_FINAL_TEN_NODE_REVIEW.json",
        "sha256": "0b31d95a89408e01ecb309827dc085cd725089de52682099a351a316c9904a89"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261006/CU_GEOMETRY_CLOSEOUT_ACCEPTANCE.json",
        "sha256": "611a444b9dcc3f5c261ee7d33dfb934c40aaa1b33ccb11f36cee6ce745879659"
      }
    ]
  }
]
```

### con_answer — Determine whether axial-pyridine substitution produces resolvable changes in the molecular magnetic exchange of the three supplied copper dimers, and what the evidence supports about that dependence.

冻结要求：Answer whether axial substitution has a resolvable molecular-exchange effect and what explanation is supported at the declared level. Reward supported trends, refutation or bounded non-resolution fairly; incomplete family coverage earns only its supported scope.

当前复审：当前分子交换比较覆盖完整且符合源分子结果；材料实验Me/OMe名义排序不同，不外推。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Resolvable model-family exchange differences with H<Me<OMe in antiferromagnetic magnitude; no bulk/material or unique-cause inference."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "当前AR/PR con_answer；源Table S4分子计算行",
    "actual_result": "在完整中性Cu2(AnCOO)4(4-RPy)2、B3LYP/def2SVP多共线SF的已验证分子范围，轴向取代对应可分辨的反铁磁交换增强：|J|(H)<|J|(Me)<|J|(OMe)。源XYZ的J=-334.370777/-341.412046/-344.582322cm^-1；独立作者方法优化后为-332.127051/-339.665675/-342.919948cm^-1。新几何Me−H、OMe−H、OMe−Me差分别-7.538624/-10.792897/-3.254273cm^-1，对应条件半宽0.791650/0.768307/0.790975cm^-1，三个区间都不跨零。旧三成员full-SF也保持同顺序；几何更新令三对差分别改变-0.497355/-0.581352/-0.083997cm^-1，未逆转差异。因此在实际检查的方法与几何变化范围内，差异并非求根误差、TDA选择或使用原源XYZ导致的排序假象。这支持分子系列取代与交换的关联；几何和电子变化仍共同存在，不能分离或宣称唯一纯轴向电子因果机制。Hermitian/态对应条件残差界不是泛函、几何或实验总误差界；不外推任意结构、基组/泛函、MOF磁性排序或光热响应。",
    "reason": "回答完整三成员分子问题，支持论文的分子交换趋势且绝对核心量在可继承同定义范围内；解释与不确定性明确限定。不靠允许负结论或rc0代替必需证据。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/Cu_three_member_geometry_source_comparison.json",
        "sha256": "23905de662507185952b71d872bc5ad9c706d0f19e654c12e960060de46866bc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume3_Cu_final_physical_root_precision/attempt_01/Cu_final_physical_root_precision.json",
        "sha256": "1950265dfa75c118b4616d782b07283e5e5c48a4d789455d07ae21b070897f94"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261004/CU_FINAL_TEN_NODE_REVIEW.json",
        "sha256": "0b31d95a89408e01ecb309827dc085cd725089de52682099a351a316c9904a89"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/Cu_author_geometry_closeout.json",
        "sha256": "fcd428a2f1a760469a1e3cde183951eda69974185a444a285ede74d27cd92d22"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/Cu_H_source_NTO_readback.json",
        "sha256": "5d4da2f47dbf6141912866d43d70248a4deea3bcaa7602ca11d0517eba0a53e7"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_NATIVE_ACCEPTANCE.json",
        "sha256": "58de3420adca79f2cc3b34b61c4f27308d61f1c9361997604fbef1a0589fbd0f"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**ORCA 33.53 分钟；另已完成 PySCF 记录 46.23 小时；失败/未完成计时 2.85 小时。均部分覆盖**。

已记录资源：ORCA 6.1.1/PySCF；原生设置 20 线程/进程；ORCA MaxCore=3500 MB/进程；另 PySCF-forge 2.13.1：已记录 20/40 线程；旧源几何 45000 MB，后续回执 20 CPU/100 GiB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)；[补充计时记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/SUPPLEMENTAL_RUNTIME.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0038 · attempt_01/H/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/orca_stdout.log) | ORCA:306.81 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[3500]} |
| [E0043 · attempt_01/CH3/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/orca_stdout.log) | ORCA:862.231 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[3500]} |
| [E0048 · attempt_01/OCH3/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/orca_stdout.log) | ORCA:842.827 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[3500]} |
| [E0052 · finish56_Cu_H_remaining_Ritz/attempt_01/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/pyscf.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0053 · finish56_Cu_H_remaining_Ritz/attempt_01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0064 · attempt_01/H/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/pyscf.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0067 · attempt_01/CH3/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/pyscf.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0070 · attempt_01/OCH3/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/pyscf.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

补充的已执行分析/响应计时如下；外层与内层重叠部分不重复相加。
```json
{
  "kind": "Additional PySCF timers; native ORCA timers separately counted",
  "records": [
    {
      "evidence_id": "E0002",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/result.json",
      "sha256": "639bbec93377e5f8fe131d81d1b84432836a5a49acaeba86cd68ed8959718ab8",
      "elapsed_seconds": 2457.7401982694864,
      "timed_operation_complete": true,
      "started_at": "2026-10-08T09:57:25.889160+00:00",
      "finished_at": "2026-10-08T10:38:23.629279+00:00",
      "failure_or_incomplete": null,
      "resources": {}
    },
    {
      "evidence_id": "E0003",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/CH3/result.json",
      "sha256": "1092f171e94d7bfe38953a740ccd8eed155f77768ee5ae5d8ba4f4ceff7dac65",
      "elapsed_seconds": 3283.108101638034,
      "timed_operation_complete": true,
      "started_at": "2026-10-08T06:39:19.777241+00:00",
      "finished_at": "2026-10-08T07:34:02.885315+00:00",
      "failure_or_incomplete": null,
      "resources": {}
    },
    {
      "evidence_id": "E0004",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/OCH3/result.json",
      "sha256": "3ce380356833d4f8c833b570bad8c99a1bc0f661b37dc3d2c2061a3d02d89e97",
      "elapsed_seconds": 4162.343586442992,
      "timed_operation_complete": true,
      "started_at": "2026-10-08T07:34:04.228579+00:00",
      "finished_at": "2026-10-08T08:43:26.572137+00:00",
      "failure_or_incomplete": null,
      "resources": {}
    },
    {
      "evidence_id": "E0063",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/result.json",
      "sha256": "82e8bb661443bd9faed37ee3d6e15c41b75396f8adcd1b4d8267b9c8ebf828b2",
      "elapsed_seconds": 5457.7660129684955,
      "timed_operation_complete": false,
      "started_at": "2026-10-07T07:24:53.151580+00:00",
      "finished_at": null,
      "failure_or_incomplete": "AssertionError('Different reference branch: preserve, do not assign by desired J')",
      "resources": {}
    },
    {
      "evidence_id": "E0066",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/result.json",
      "sha256": "258449438ad3fe8d01b45de2b30c6c7547a61a8d28c55c1e544309373a2f3ac7",
      "elapsed_seconds": 9797.840473249555,
      "timed_operation_complete": true,
      "started_at": "2026-10-07T14:50:53.888327+00:00",
      "finished_at": "2026-10-07T17:34:11.728734+00:00",
      "failure_or_incomplete": null,
      "resources": {}
    },
    {
      "evidence_id": "E0069",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/result.json",
      "sha256": "a29db3f880b078bd283e679a29c2c16b2df92c96a146b7820987677d8c9e9d4a",
      "elapsed_seconds": 10596.004155186936,
      "timed_operation_complete": true,
      "started_at": "2026-10-07T17:34:16.520057+00:00",
      "finished_at": "2026-10-07T20:30:52.524177+00:00",
      "failure_or_incomplete": null,
      "resources": {}
    },
    {
      "evidence_id": "E0072",
      "path": "runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_H/result.json",
      "sha256": "0ede3fc4be829827a20f8c7063ef0dc0fee6c66516ab13067477a7ccf3c7bf74",
      "elapsed_seconds": 24321.287124745548,
      "timed_operation_complete": true,
      "started_at": "2026-09-16T06:18:37.260448+00:00",
      "finished_at": "2026-09-16T13:03:58.548051+00:00",
      "failure_or_incomplete": null,
      "resources": {
        "threads": 40,
        "memory_mb": 45000
      }
    },
    {
      "evidence_id": "E0073",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_H_source_fullSF_tight_calibration/attempt_01/result.json",
      "sha256": "d0b5a46a34a4b292131ca447632e0f2e7ed62f03a8d845a9e7c4f11a45cd2db2",
      "elapsed_seconds": 15273.025670248084,
      "timed_operation_complete": true,
      "started_at": "2026-09-29T15:59:16.866745+00:00",
      "finished_at": "2026-09-29T20:13:49.892399+00:00",
      "failure_or_incomplete": null,
      "resources": {
        "runtime_pyscf": "2.13.1"
      }
    },
    {
      "evidence_id": "E0074",
      "path": "runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_CH3/result.json",
      "sha256": "88b8ec22c06a65f0f0aedb1312ce51410c2a908f2b251f079c14b1f153deb1da",
      "elapsed_seconds": 23106.578162059188,
      "timed_operation_complete": true,
      "started_at": "2026-09-16T06:23:19.739481+00:00",
      "finished_at": "2026-09-16T12:48:26.318074+00:00",
      "failure_or_incomplete": null,
      "resources": {
        "threads": 40,
        "memory_mb": 45000
      }
    },
    {
      "evidence_id": "E0075",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_CH3_source_fullSF_tight_calibration/attempt_01/result.json",
      "sha256": "0564d54f8625795ddf33cf2d57e8850f589cba3da9338403652fa1395c83b685",
      "elapsed_seconds": 19611.11987039633,
      "timed_operation_complete": true,
      "started_at": "2026-09-29T15:59:16.839186+00:00",
      "finished_at": "2026-09-29T21:26:07.960569+00:00",
      "failure_or_incomplete": null,
      "resources": {
        "runtime_pyscf": "2.13.1"
      }
    },
    {
      "evidence_id": "E0076",
      "path": "runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_OCH3/result.json",
      "sha256": "1e0f9fefe24f2203b4319b434e5227d5951d7a7f341737d6b18b1ecb65f972d5",
      "elapsed_seconds": 23095.17637388222,
      "timed_operation_complete": true,
      "started_at": "2026-09-16T06:41:35.477065+00:00",
      "finished_at": "2026-09-16T13:06:30.654933+00:00",
      "failure_or_incomplete": null,
      "resources": {
        "threads": 40,
        "memory_mb": 45000
      }
    },
    {
      "evidence_id": "E0077",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_OCH3_source_fullSF_tight_calibration/attempt_01/result.json",
      "sha256": "5a4d93096e304a4c8d0d05e86a9979e1f6e422318882813716b99c8644842129",
      "elapsed_seconds": 20520.61235260591,
      "timed_operation_complete": true,
      "started_at": "2026-09-29T16:00:52.150189+00:00",
      "finished_at": "2026-09-29T21:42:52.762528+00:00",
      "failure_or_incomplete": null,
      "resources": {
        "runtime_pyscf": "2.13.1"
      }
    },
    {
      "evidence_id": "E0078",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_OCH3_fullSF_checkpoint_residual_polish/attempt_01/result.json",
      "sha256": "753594149faa37325a29666bb8492c2c8a15b4697b922762f53a415083fff104",
      "elapsed_seconds": 10187.988980965689,
      "timed_operation_complete": true,
      "started_at": "2026-09-30T03:14:42.693677+00:00",
      "finished_at": "2026-09-30T06:04:30.682663+00:00",
      "failure_or_incomplete": null,
      "resources": {}
    },
    {
      "evidence_id": "E0113",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/result.json",
      "sha256": "41a6cd48910c33403bbe2717f2c05a6f78612beff956950e62c9646b633fad7a",
      "elapsed_seconds": 4788.015985669568,
      "timed_operation_complete": false,
      "started_at": "2026-10-08T05:09:30.026990+00:00",
      "finished_at": null,
      "failure_or_incomplete": "No completed end marker in this record",
      "resources": {}
    }
  ],
  "completed_seconds": 166412.82504968997,
  "failed_or_incomplete_seconds": 10245.781998638064,
  "note": "Selected distinct run records. E0061/E0062 are duplicates of E0003/E0004 and excluded; ORCA wrapper/cumulative timers excluded. These complete only the recorded operations, not a new whole-question scientific judgment."
}
```

## 6. 已知偏差、失败分支和不能外推的结论

Me/OMe未取得完整Hessian，不称严格频率最低点；任务实际结论不依赖该名称。；材料磁性/光热机理和纯电子取代因果未认证。；优化后OMe−H差−10.793与源整数−10不在固定算符数值区间内；此区间不是几何总误差。

```json
[
  "No unique decomposition of electronic versus geometric substitution effects.",
  "No material susceptibility, photothermal or magnetic-order prediction.",
  "No claim that exact last source digits or exact-geometry frequency minima for Me/OMe were recovered."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Conditional residual intervals assume the Hermitian operator and correct physical-state association; they are not functional, structural or experimental total error bars. Non-Hermitian full-SF is not assigned the same bound.",
  "Experimental material values −367/−383/−381 cm−1 are distinct and have a different nominal Me/OMe order; no bulk-material ordering or photothermal response is certified.",
  "Geometry and electronic substitution changes coexist. A unique pure-electronic causal decomposition is not established.",
  "ORCA version/B3LYP conventions and small final-gradient limitations remain declared. New full Hessians or an arbitrary functional grid are not inferred mandatory from this bounded result."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_0cd74ae20ab933f3.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0cd74ae20ab933f3/verified_computation_reference.md)；SHA-256 `be5b074d933e58443805d0a34898e1397530f86766be3edda058b36fa7e3081b`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_0cd74ae20ab933f3.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_0cd74ae20ab933f3.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_0cd74ae20ab933f3.json) | `49f337dce869b2a6bdc923a2e69a6efa7df8cab8b233e940bb6dc44302007c69` | evidence_or_analysis |
| E0002 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_result.json) | `639bbec93377e5f8fe131d81d1b84432836a5a49acaeba86cd68ed8959718ab8` | evidence_or_analysis |
| E0003 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/CH3/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/CH3/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_result.json) | `1092f171e94d7bfe38953a740ccd8eed155f77768ee5ae5d8ba4f4ceff7dac65` | evidence_or_analysis |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/OCH3/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/OCH3/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_result.json) | `3ce380356833d4f8c833b570bad8c99a1bc0f661b37dc3d2c2061a3d02d89e97` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume3_Cu_final_physical_root_precision/attempt_01/Cu_final_physical_root_precision.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume3_Cu_final_physical_root_precision/attempt_01/Cu_final_physical_root_precision.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_Cu_final_physical_root_precision.json) | `1950265dfa75c118b4616d782b07283e5e5c48a4d789455d07ae21b070897f94` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/Cu_author_geometry_closeout.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/Cu_author_geometry_closeout.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_Cu_author_geometry_closeout.json) | `fcd428a2f1a760469a1e3cde183951eda69974185a444a285ede74d27cd92d22` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/a03bc9ac6367ed29_paper_0cd74ae20ab933f3_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/a03bc9ac6367ed29_paper_0cd74ae20ab933f3_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_a03bc9ac6367ed29_paper_0cd74ae20ab933f3_primary_pages.json) | `a03bc9ac6367ed29a1b660a97619e8224f7811efe548dfe93018364cffa03c66` | evidence_or_analysis |
| E0008 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_task.md) | `39f0da3a1a6d4ce9e05bbabe049eb542dacb0b2887dec32b0df8765a7f1f3d9a` | historical_task_binding |
| E0009 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_reference_key_points.json) | `06d702dfccbd6d4f4076b8ebb24130e05bfbd8600e02ae84ee44da776b5647c1` | historical_task_binding |
| E0010 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_reference_conclusions.json) | `b3795a48af220c12aaf6fa4fc0d2640229cdb2870abbfdf2a63fe37e3191ba13` | historical_task_binding |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_task.md) | `b6f62b8122276d730351d9d122dbce0c222e298078c0bbcbae7a65e52ec6375a` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_reference_key_points.json) | `06d702dfccbd6d4f4076b8ebb24130e05bfbd8600e02ae84ee44da776b5647c1` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_reference_conclusions.json) | `b3795a48af220c12aaf6fa4fc0d2640229cdb2870abbfdf2a63fe37e3191ba13` | historical_task_binding |
| E0014 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0cd74ae20ab933f3/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0cd74ae20ab933f3/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_NATIVE_READBACK.json) | `3a6d9df1ce1927702724efc89eeca77934bcf9ae780cd77a7ab7678bc1c7973d` | evidence_or_analysis |
| E0015 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0cd74ae20ab933f3/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0cd74ae20ab933f3/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_COMPUTATION_COVERAGE.json) | `e8f3f3c2732116c721ccada574dd9d06fe601e3253d99ae29f42846e5a802b71` | evidence_or_analysis |
| E0016 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_0cd74ae20ab933f3.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_0cd74ae20ab933f3.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_paper_0cd74ae20ab933f3.md) | `7e26ebee70cecc02cbf05a2236267ae46611cddb412c02428851b11bdc3e2118` | evidence_or_analysis |
| E0017 | [docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `7bdfa7b9eb2733edb7b8b878112c9084617a74d0f0b087a000850a4bde820aa7` | historical_task_binding |
| E0018 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_0cd74ae20ab933f3/source_graph_response_reanalysis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_0cd74ae20ab933f3/source_graph_response_reanalysis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0018_source_graph_response_reanalysis.json) | `a740ffe2b3a0318784fdd3222f47c209b201a7ca37efb9bdec12614cb6296f64` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_NATIVE_ACCEPTANCE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_NATIVE_ACCEPTANCE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_RETURNED_NATIVE_ACCEPTANCE.json) | `58de3420adca79f2cc3b34b61c4f27308d61f1c9361997604fbef1a0589fbd0f` | evidence_or_analysis |
| E0020 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/Cu_three_member_geometry_source_comparison.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/Cu_three_member_geometry_source_comparison.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0020_Cu_three_member_geometry_source_comparison.json) | `23905de662507185952b71d872bc5ad9c706d0f19e654c12e960060de46866bc` | evidence_or_analysis |
| E0021 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261004/CU_FINAL_TEN_NODE_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261004/CU_FINAL_TEN_NODE_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_CU_FINAL_TEN_NODE_REVIEW.json) | `0b31d95a89408e01ecb309827dc085cd725089de52682099a351a316c9904a89` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/Cu_H_source_NTO_readback.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/Cu_H_source_NTO_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0022_Cu_H_source_NTO_readback.json) | `5d4da2f47dbf6141912866d43d70248a4deea3bcaa7602ca11d0517eba0a53e7` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261006/CU_GEOMETRY_CLOSEOUT_ACCEPTANCE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261006/CU_GEOMETRY_CLOSEOUT_ACCEPTANCE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0023_CU_GEOMETRY_CLOSEOUT_ACCEPTANCE.json) | `611a444b9dcc3f5c261ee7d33dfb934c40aaa1b33ccb11f36cee6ce745879659` | evidence_or_analysis |
| E0024 | [tasks/final_verified_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_scoring_rules.json) | `28de9e23fce1858c4d9c5158cb72f41ebe85b42f8d20f275c811f8c20c4ff627` | historical_task_binding |
| E0025 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_scoring_rules.json) | `a719af35068540bf624a588f61a10d62327af736f5ad71340d8cc1488ebdd529` | historical_task_binding |
| E0026 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_scoring_rules.json) | `a719af35068540bf624a588f61a10d62327af736f5ad71340d8cc1488ebdd529` | historical_task_binding |
| E0027 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/3f7e955e3dd91e54_G6.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/3f7e955e3dd91e54_G6.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_3f7e955e3dd91e54_G6.json) | `3f7e955e3dd91e548f0d7698dc4126ad796bcb5f33327c51d4e7503c61b9c912` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/G6.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/G6.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_G6.json) | `3f7e955e3dd91e548f0d7698dc4126ad796bcb5f33327c51d4e7503c61b9c912` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/15458f43a699a8b8_paper_0cd74ae20ab933f3_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/15458f43a699a8b8_paper_0cd74ae20ab933f3_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_15458f43a699a8b8_paper_0cd74ae20ab933f3_delivery_integrity.json) | `15458f43a699a8b84f0a74071c747cc9cc2ddf9bc0e694464378f7d1423abb34` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0cd74ae20ab933f3_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0cd74ae20ab933f3_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_paper_0cd74ae20ab933f3_delivery_integrity.json) | `15458f43a699a8b84f0a74071c747cc9cc2ddf9bc0e694464378f7d1423abb34` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0cd74ae20ab933f3_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0cd74ae20ab933f3_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_paper_0cd74ae20ab933f3_primary_pages.json) | `a03bc9ac6367ed29a1b660a97619e8224f7811efe548dfe93018364cffa03c66` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/8583d7c50b59e55a_paper_0cd74ae20ab933f3_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/8583d7c50b59e55a_paper_0cd74ae20ab933f3_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_8583d7c50b59e55a_paper_0cd74ae20ab933f3_native_readback.json) | `8583d7c50b59e55a9642ac42dc59654cfc938e36f2a4873aa1b361c6901a2157` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0cd74ae20ab933f3_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0cd74ae20ab933f3_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_paper_0cd74ae20ab933f3_native_readback.json) | `8583d7c50b59e55a9642ac42dc59654cfc938e36f2a4873aa1b361c6901a2157` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/prior_decisions/paper_0cd74ae20ab933f3.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/prior_decisions/paper_0cd74ae20ab933f3.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_paper_0cd74ae20ab933f3.json) | `7c74a2d40ccc2204f644ae91b60f8a08e37872cb1904090f43c868787e57a8ba` | evidence_or_analysis |
| E0035 | [runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_H/author.xyz](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_H/author.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_author.xyz) | `209361f93e20bd7a8f1f7cf72510393f453616622e90ea6c05335ec0e139d414` | input_or_analysis_code |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_H.xyz) | `00de7d5008a9857d192f4e7886a1e125268e5cbf0087a899e375caf68a300ecd` | input_or_analysis_code |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/H.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/H.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_H.inp) | `2369ec4a882c75c841137fa045faaab7560679a4403e768931945de1906426e6` | input_or_analysis_code |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_native_excerpt.json) | `09e8d406bdab6c90c98470edd141a61a02220797e631d79ab2cf473e8713dae9` | native_output |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/H.engrad](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/H/H.engrad) | `a0ffbe45e314cd72b69334a6e2d2244d8240e606cfac883f536506942da2900e` | evidence_or_analysis |
| E0040 | [runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_CH3/author.xyz](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_CH3/author.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_author.xyz) | `038c51c7e217f428a5504e2e99d7d3daa30cf18597e7a71b9aec42071af4b143` | input_or_analysis_code |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_CH3.xyz) | `9c78b5f136114735d9bfdac4224253e2ba8364de494ff2191d49c523e4b6ad92` | input_or_analysis_code |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_CH3.inp) | `6e2c9282855565f3992064c54f39e84d2f73f792de343d31260c217433602a27` | input_or_analysis_code |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_native_excerpt.json) | `522e421ad392f0afd4c797f3402f965192c130acc95e3b81b546afc56aab7ec3` | native_output |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3.engrad](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3.engrad) | `84019bb1b4e3283491519d0300ffcf90a462fba134115e31d2079ff07a8247c5` | evidence_or_analysis |
| E0045 | [runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_OCH3/author.xyz](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_OCH3/author.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_author.xyz) | `35d06497f04ab88d7b77508aa68eaf9bf7173a9c91642bcbc67b0d66b64d6e66` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_OCH3.xyz) | `c41d7fb8bf2b5f08671006bf8d4bec2c43a4cfe6efa98c415f11ea8301d6ebc5` | input_or_analysis_code |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_OCH3.inp) | `dae5db632b11c427fb6eff0e512d70001025e90fc8a29f09bbef3a42edc38e8b` | input_or_analysis_code |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_native_excerpt.json) | `2ce435a620afd4acde2ac8f16a524d1ab5c5b84151887d2f1d3af22d8a3bbc4f` | native_output |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3.engrad](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3.engrad) | `54211a4a547ceb0cdd178cc58003b5888b38ca7e4ec5053af1db76878d4b3e66` | evidence_or_analysis |
| E0050 | [papers/paper_0cd74ae20ab933f3/documents/main.pdf](../../../../papers/paper_0cd74ae20ab933f3/documents/main.pdf) | `e74146ea380e78e6bca3a1ca6eeb56ec4a16487ac58d2f169c0f92f64efea2aa` | source_document |
| E0051 | [papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf](../../../../papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf) | `dd357023aa433eeb80376b2b8f11e44a332edd2d95cdc8809838e6f3a448c222` | source_document |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/pyscf.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_native_excerpt.json) | `c76f825089223a02c4395793034c5d5e7c08df6a8a366654a2d4ba9cf83cbbf5` | native_output |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_native_excerpt.json) | `5df78ee49b6ed2832c9c20fff4ee704f359eba3c564e4b27a53e41abf95d5fab` | native_output |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_status.json) | `f3d97e8f46142d51ea2c5e8560285b3c47055106fd01fc2083bc56e93288c869` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/response-native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/response-native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_response-native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/remaining_H_response_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/remaining_H_response_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_remaining_H_response_receipt.json) | `52e53712045e7d987b1e7e14fbac314dd7e232a6e2348f40f3bca86e7fd9fe61` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_worker.py) | `c8c8a9f21d3c8ad4eefd0d04ad680350be88fab708300ad44508743cd6a90165` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/FROZEN_INPUT_OUTPUT_INTEGRITY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/FROZEN_INPUT_OUTPUT_INTEGRITY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_FROZEN_INPUT_OUTPUT_INTEGRITY.json) | `04b1c842b9a142f6531a0efb5d1f0fa89e9a61feafc44f33bc8c9fa9cf0829c6` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_PLATFORM_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0cd74ae20ab933f3/RETURNED_PLATFORM_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_RETURNED_PLATFORM_READBACK.json) | `80e69b199fa7badbce3c7f4d3c5e682295a3954d36410b47572e288a61350734` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/CH3_result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/CH3_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_CH3_result.json) | `1092f171e94d7bfe38953a740ccd8eed155f77768ee5ae5d8ba4f4ceff7dac65` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/OCH3_result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/OCH3_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_OCH3_result.json) | `3ce380356833d4f8c833b570bad8c99a1bc0f661b37dc3d2c2061a3d02d89e97` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0063_result.json) | `82e8bb661443bd9faed37ee3d6e15c41b75396f8adcd1b4d8267b9c8ebf828b2` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/pyscf.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0064_native_excerpt.json) | `990bcf45d10ddb050e32ae3f735d4cc47213b6faaeb40a54b6e66a45a4241d64` | native_output |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/new_uks.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/new_uks.chk) | `dddfd8abb45f4ffcf393f889cc20912d8db2d432ebcefdb9cd2b6fb8ece85b88` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_result.json) | `258449438ad3fe8d01b45de2b30c6c7547a61a8d28c55c1e544309373a2f3ac7` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/pyscf.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0067_native_excerpt.json) | `e3ac211c055e266cb0cc53e545ccfb7ea4f05921c9008bba7f8037606dd04587` | native_output |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/new_uks.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/new_uks.chk) | `beb9e0ec976ffde3f5839659a86eed4770abc28c40bdbae2cfacac388f6c0137` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_result.json) | `a29db3f880b078bd283e679a29c2c16b2df92c96a146b7820987677d8c9e9d4a` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/pyscf.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/pyscf.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_native_excerpt.json) | `25a7cffe125be9d7519716d272a5f73ba4a3ffd89f77b2a91edde39a7c4e7981` | native_output |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/new_uks.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/new_uks.chk) | `c77dcdbf06c7c3ac1a0dc93bf2d354ba225e19f1193d0756f1135a241bee82c3` | evidence_or_analysis |
| E0072 | [runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_H/result.json](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_H/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_result.json) | `0ede3fc4be829827a20f8c7063ef0dc0fee6c66516ab13067477a7ccf3c7bf74` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_H_source_fullSF_tight_calibration/attempt_01/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_H_source_fullSF_tight_calibration/attempt_01/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_result.json) | `d0b5a46a34a4b292131ca447632e0f2e7ed62f03a8d845a9e7c4f11a45cd2db2` | evidence_or_analysis |
| E0074 | [runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_CH3/result.json](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_CH3/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_result.json) | `88b8ec22c06a65f0f0aedb1312ce51410c2a908f2b251f079c14b1f153deb1da` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_CH3_source_fullSF_tight_calibration/attempt_01/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_CH3_source_fullSF_tight_calibration/attempt_01/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0075_result.json) | `0564d54f8625795ddf33cf2d57e8850f589cba3da9338403652fa1395c83b685` | evidence_or_analysis |
| E0076 | [runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_OCH3/result.json](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_OCH3/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0076_result.json) | `1e0f9fefe24f2203b4319b434e5227d5951d7a7f341737d6b18b1ecb65f972d5` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_OCH3_source_fullSF_tight_calibration/attempt_01/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_OCH3_source_fullSF_tight_calibration/attempt_01/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_result.json) | `5a4d93096e304a4c8d0d05e86a9979e1f6e422318882813716b99c8644842129` | evidence_or_analysis |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_OCH3_fullSF_checkpoint_residual_polish/attempt_01/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_R_OCH3_fullSF_checkpoint_residual_polish/attempt_01/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_result.json) | `753594149faa37325a29666bb8492c2c8a15b4697b922762f53a415083fff104` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_Cu_budget_terminal_vector_family_readback/attempt_01/Cu_terminal_vector_family_readback.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_Cu_budget_terminal_vector_family_readback/attempt_01/Cu_terminal_vector_family_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_Cu_terminal_vector_family_readback.json) | `10093126b33c80c132f7b0a7f67a00e31fcdeea7ee545ba2db446f4b739b1240` | evidence_or_analysis |
| E0080 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0cd74ae20ab933f3/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_package_manifest.json) | `8c96f5c26982a7cc63c0b90c0c3b72d50407946e0274c1cd646ec0329585d70a` | historical_task_binding |
| E0081 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0cd74ae20ab933f3/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_package_manifest.json) | `69ea2af73553725e3c4b00178d3fc82c2d27b01d10a22518fe64cfbc82b6c745` | historical_task_binding |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/valid_original_TDA_1e5_NTO.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/valid_original_TDA_1e5_NTO.npz) | `363ddb642b904ba750b51d609a2148706bdc660227948db678f2d5d164ef0643` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/failed_tight_Ritz_diagnostic_only_NTO.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/supervision_replay1_Cu_H_NTO_saved/attempt_01/failed_tight_Ritz_diagnostic_only_NTO.npz) | `dc282b4702e500f68fd18444a74334c6754d87d821c8e91f0d853cd24238c8f8` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_0cd74ae20ab933f3/H_source_graph_Hessian_acceptance_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_0cd74ae20ab933f3/H_source_graph_Hessian_acceptance_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_H_source_graph_Hessian_acceptance_20260930.json) | `664a60f8048c533b5d1bed54430d34ef35c3ddf978a1cb14578fc32e39249bad` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/Cu_remaining_author_geometry_result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/Cu_remaining_author_geometry_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_Cu_remaining_author_geometry_result.json) | `9c7a551b3725b17d5225b1fe84643aaabe85317c2d97689ed9d18c201ddec2ce` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_case.json) | `0f0c9bc69de7ccf072b8ed49ec85b98c0dfb199ddbbd6d6b6f2c707f89f26a8e` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_author_source_geometry_gradients/attempt_01/Cu_author_source_geometry_gradient_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_author_source_geometry_gradients/attempt_01/Cu_author_source_geometry_gradient_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_Cu_author_source_geometry_gradient_audit.json) | `98e7922d938224a340d37b4a906d8e458ea3ba1840e12d751f756fc68d1b334c` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_source_default_grid_gradients/attempt_01/Cu_source_default_grid_gradient_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_source_default_grid_gradients/attempt_01/Cu_source_default_grid_gradient_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_Cu_source_default_grid_gradient_audit.json) | `9586aa4fe8cf03f4e6800d3f6db38848ac0dea22decc25e98e975d20b10dc09e` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_status.json) | `3b16c47e8effc8013dc0ca7872a6bf049bcda3ebc6725545a9791462e1cab1b8` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume6_Cu_author_geometry_closeout/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0090_submission.json) | `6f9ea787edd860e532cd7b188586d187e6e900b3ab8a8d64a8632cc965fff3c1` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_0cd74ae20ab933f3/CURRENT_SI_METHOD_RESPONSE_READ.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_0cd74ae20ab933f3/CURRENT_SI_METHOD_RESPONSE_READ.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0091_CURRENT_SI_METHOD_RESPONSE_READ.json) | `1f9221ec89376f626ccf8b989942bc91ba4bdaff6f5cf6fe445b894e787fe9a1` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/CU_DIRECT_SOURCE_READ.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/CU_DIRECT_SOURCE_READ.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0092_CU_DIRECT_SOURCE_READ.json) | `a03bc9ac6367ed29a1b660a97619e8224f7811efe548dfe93018364cffa03c66` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/G6_CU_GEOMETRY_REVIEW_FOLLOWUP_REQUEST.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/G6_CU_GEOMETRY_REVIEW_FOLLOWUP_REQUEST.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0093_G6_CU_GEOMETRY_REVIEW_FOLLOWUP_REQUEST.json) | `2b03f0df48605e00b6ae304d7c7d02e330a8faadeffbbefa83dd5f5178d0631c` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261006/CU_AUTHOR_ROUTE_NODE_REVIEW_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/resume_20261006/CU_AUTHOR_ROUTE_NODE_REVIEW_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0094_CU_AUTHOR_ROUTE_NODE_REVIEW_20261006.json) | `1e80156cfcbb5f586754a457230eb32a014553b2b31bab23d1b94bdb77b3687e` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/CH3/CH3_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0095_CH3_trj.xyz) | `bf3101a456cd6e2b1f0b1e9f50797726e1a8f5ef39eeedeeaba8d6bcac740e8a` | input_or_analysis_code |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume5_Cu_remaining_author_geometry/attempt_01/OCH3/OCH3_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0096_OCH3_trj.xyz) | `5de5633605c7c3e84927fce3f6b648624b48cd80578e593efd007ee8cd22068c` | input_or_analysis_code |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0097_analysis.py) | `270287a7b8dae158c2aa6e83ebc457aa21c1fcc10fbd6df059871c95133d3ad9` | input_or_analysis_code |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/sf_helpers.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/sf_helpers.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0098_sf_helpers.py) | `804a9e964d730be91748e1476f4414186428bbde92cc47be3ed7f8ac970a6cbe` | input_or_analysis_code |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0099_run.sh) | `2cef7a27f3010c8fab1e58bff7a32fed1205ff6d3e0b19eb89b798967788066f` | input_or_analysis_code |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/mcfun_parallel.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/mcfun_parallel.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0100_mcfun_parallel.py) | `0201119090866fe27005301cb5bb5372d9ce62831a95864183028d6934d4dda6` | input_or_analysis_code |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0101_case.json) | `7bbdd1f8b4f1459b768a50d5e5a3507bb795c424a0c2c78d5245ac6887f636e6` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/uks.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/uks.chk) | `dddfd8abb45f4ffcf393f889cc20912d8db2d432ebcefdb9cd2b6fb8ece85b88` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/ritz.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/ritz.npz) | `213a82c68cb602a30df611f03f0dc892c6617fa1018ff166959fa66f930ab7ea` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/prior_H.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/prior_H.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0104_prior_H.json) | `41a6cd48910c33403bbe2717f2c05a6f78612beff956950e62c9646b633fad7a` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/stage.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/stage.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0105_stage.json) | `bad234b1ccf7ed0eba17c13450882db9532e83f25aabed41899f866026630edb` | evidence_or_analysis |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/CH3_native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/CH3_native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0106_CH3_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/OCH3_native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/OCH3_native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0107_OCH3_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/source_response_packet.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/source_response_packet.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0108_source_response_packet.json) | `0b31d95a89408e01ecb309827dc085cd725089de52682099a351a316c9904a89` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/geometry_closeout.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/geometry_closeout.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0109_geometry_closeout.json) | `fcd428a2f1a760469a1e3cde183951eda69974185a444a285ede74d27cd92d22` | evidence_or_analysis |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/inputs.sha256) | `41fa3414a07ffb5233666beb776d8270aef831894a1c98725846308c97fd51f4` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/uks.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/uks.chk) | `dddfd8abb45f4ffcf393f889cc20912d8db2d432ebcefdb9cd2b6fb8ece85b88` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/latest_native_ritz.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/latest_native_ritz.npz) | `213a82c68cb602a30df611f03f0dc892c6617fa1018ff166959fa66f930ab7ea` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0113_result.json) | `41a6cd48910c33403bbe2717f2c05a6f78612beff956950e62c9646b633fad7a` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/mcfun_parallel.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/mcfun_parallel.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0114_mcfun_parallel.py) | `0201119090866fe27005301cb5bb5372d9ce62831a95864183028d6934d4dda6` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/sf_helpers.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/H/sf_helpers.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0115_sf_helpers.py) | `804a9e964d730be91748e1476f4414186428bbde92cc47be3ed7f8ac970a6cbe` | input_or_analysis_code |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/inputs/finish56_Cu_H_remaining_Ritz/worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/inputs/finish56_Cu_H_remaining_Ritz/worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0116_worker.py) | `c8c8a9f21d3c8ad4eefd0d04ad680350be88fab708300ad44508743cd6a90165` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/inputs/finish56_Cu_H_remaining_Ritz/stage.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/inputs/finish56_Cu_H_remaining_Ritz/stage.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0117_stage.json) | `bad234b1ccf7ed0eba17c13450882db9532e83f25aabed41899f866026630edb` | evidence_or_analysis |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/CH3/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/CH3/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0118_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/OCH3/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume8_Cu_saved_Ritz_precision/attempt_01/OCH3/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0119_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0120 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/__init__.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/__init__.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0120___init__.py) | `8faa3f97d5bb3613ae71db475ed9065841781ed161b143a6a7fbd581e610c864` | input_or_analysis_code |
| E0121 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/numint2c_sftd.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/numint2c_sftd.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0121_numint2c_sftd.py) | `88b058333ce89fc65f42b60c8d24f53099f70c719b1fd204661ac7c0ef88cfce` | input_or_analysis_code |
| E0122 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/scf_genrep_sftd.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/scf_genrep_sftd.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0122_scf_genrep_sftd.py) | `9be7fcbbf6dd185ef54c856b02f3ed3cb7f5ac747a0ebcd82d342e90d1282bf7` | input_or_analysis_code |
| E0123 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftda.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftda.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0123_test_sftda.py) | `3230ea9a20c6a1e42f9ffa109c7274b19c8c05ff4059a7b7da1d38c688f966cc` | input_or_analysis_code |
| E0124 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftda_roks.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftda_roks.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0124_test_sftda_roks.py) | `76a1b91bdb91ddb6db8de0c764c5758f2cb190f0b09a39598ebb07cc09200caf` | input_or_analysis_code |
| E0125 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftddft.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftddft.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0125_test_sftddft.py) | `7c0c503793ca39d4bd8034b4cde23ff6ad43efcc9112171cdaa3904a4ae0b62b` | input_or_analysis_code |
| E0126 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftddft_roks.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/test/test_sftddft_roks.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0126_test_sftddft_roks.py) | `cec1888699f8bcc0bfbead191ce3bd8d8a338bd310fb2c31c66afb6e35f3ff3e` | input_or_analysis_code |
| E0127 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/uhf_sf.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/uhf_sf.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0127_uhf_sf.py) | `9c798d15a6b1ed8145edcb7eec04ce40fdc7d7539d1a1a025116249833e11e3a` | input_or_analysis_code |
| E0128 | [.software_cache/sources/pyscf-forge/repo/pyscf/sftda/uks_sf.py](../../../../.software_cache/sources/pyscf-forge/repo/pyscf/sftda/uks_sf.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0128_uks_sf.py) | `7d38f2dfd542372180b2ec271b8617dbf3054f873e0f36cc12723b5fd8398776` | input_or_analysis_code |
| E0129 | [.software_cache/installations/mcfun/0.2.6/mcfun/LebedevGrid.py](../../../../.software_cache/installations/mcfun/0.2.6/mcfun/LebedevGrid.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0129_LebedevGrid.py) | `209fe7e675cd3c97ea58e0cb3bfca7e83f90e89d1235db6770cc80ddb4f28e45` | input_or_analysis_code |
| E0130 | [.software_cache/installations/mcfun/0.2.6/mcfun/__init__.py](../../../../.software_cache/installations/mcfun/0.2.6/mcfun/__init__.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0130___init__.py) | `b60df48bf86ff83476d747a619e419c52e7be03cd124193ab77fb77910696348` | input_or_analysis_code |
| E0131 | [.software_cache/installations/mcfun/0.2.6/mcfun/eval_xc.py](../../../../.software_cache/installations/mcfun/0.2.6/mcfun/eval_xc.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0131_eval_xc.py) | `4fe9a25b4ed9e14b4c7b1c54abe27a652f60b49c7fc5f0c7c1edea89f0360a38` | input_or_analysis_code |
| E0132 | [.envs/researchchembench/lib/python3.10/site-packages/pyscf/tdscf/_lr_eig.py](../../../../.envs/researchchembench/lib/python3.10/site-packages/pyscf/tdscf/_lr_eig.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0132__lr_eig.py) | `99a210bafb8beb083a5f9995e72815f5fba60fcf95966d123ae01854856840e4` | input_or_analysis_code |
| E0133 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/final_independent_vectors.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/final_independent_vectors.npz) | `e1746dc3e527fb0dd6f8f7a663e79093029eaf599954525c2f3d0598d4256fdd` | evidence_or_analysis |
| E0134 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/polished_tda.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/finish56_Cu_H_remaining_Ritz/attempt_01/polished_tda.chk) | `ae02d9d3171ceeda0afcd0459e41fb67fab4e191816538432985513b8c32da6b` | evidence_or_analysis |
| E0135 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0135_worker.py) | `ffadaac87de76ea2af5d3091ba44822f4fa2c3f3a5d24803293886157da6e129` | input_or_analysis_code |
| E0136 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/sf_helpers.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/sf_helpers.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0136_sf_helpers.py) | `804a9e964d730be91748e1476f4414186428bbde92cc47be3ed7f8ac970a6cbe` | input_or_analysis_code |
| E0137 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/mcfun_parallel.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/mcfun_parallel.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0137_mcfun_parallel.py) | `0201119090866fe27005301cb5bb5372d9ce62831a95864183028d6934d4dda6` | input_or_analysis_code |
| E0138 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/new_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_optimized_geometry_response/attempt_01/H/new_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0138_new_geometry.xyz) | `00de7d5008a9857d192f4e7886a1e125268e5cbf0087a899e375caf68a300ecd` | input_or_analysis_code |
| E0139 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0139_worker.py) | `269c98f4e15e6317750cc183abca664954a2f9938015c22bb83b4836ce19452d` | input_or_analysis_code |
| E0140 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/sf_helpers.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/sf_helpers.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0140_sf_helpers.py) | `804a9e964d730be91748e1476f4414186428bbde92cc47be3ed7f8ac970a6cbe` | input_or_analysis_code |
| E0141 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/mcfun_parallel.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/mcfun_parallel.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0141_mcfun_parallel.py) | `0201119090866fe27005301cb5bb5372d9ce62831a95864183028d6934d4dda6` | input_or_analysis_code |
| E0142 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/new_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/CH3/new_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0142_new_geometry.xyz) | `9c78b5f136114735d9bfdac4224253e2ba8364de494ff2191d49c523e4b6ad92` | input_or_analysis_code |
| E0143 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0143_worker.py) | `269c98f4e15e6317750cc183abca664954a2f9938015c22bb83b4836ce19452d` | input_or_analysis_code |
| E0144 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/sf_helpers.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/sf_helpers.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0144_sf_helpers.py) | `804a9e964d730be91748e1476f4414186428bbde92cc47be3ed7f8ac970a6cbe` | input_or_analysis_code |
| E0145 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/mcfun_parallel.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/mcfun_parallel.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0145_mcfun_parallel.py) | `0201119090866fe27005301cb5bb5372d9ce62831a95864183028d6934d4dda6` | input_or_analysis_code |
| E0146 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/new_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/resume7_Cu_unrun_Me_OMe_response/attempt_01/OCH3/new_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_0cd74ae20ab933f3/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0146_new_geometry.xyz) | `c41d7fb8bf2b5f08671006bf8d4bec2c43a4cfe6efa98c415f11ea8301d6ebc5` | input_or_analysis_code |
| N0147 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/H_T_converged_geometry_optfreq_platform_resume2/attempt_01/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/H_T_converged_geometry_optfreq_platform_resume2/attempt_01/orca_stdout.log) | `9f3a7e21892f0aef136f0f6d978666c5e333cfd0734e94b0c8cd5064830c7e34` | 本轮直接读回原生日志；结果/route/频率详见native_readback.json |
| N0148 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_H_source_graph_gradient_geometry_freq_only/attempt_01/orca_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/outputs/v2_H_source_graph_gradient_geometry_freq_only/attempt_01/orca_stdout.log) | `a0f2c958126efb36d69353fd73e6da9f162a389b8b56c49c8ebe2c4e3fa941e2` | 本轮直接读回原生日志；结果/route/频率详见native_readback.json |
| N0149 | [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/agent_input/task.md](../agent_input/task.md) | `39f0da3a1a6d4ce9e05bbabe049eb542dacb0b2887dec32b0df8765a7f1f3d9a` | latest_review_evidence |
| N0150 | [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json](reference_key_points.json) | `06d702dfccbd6d4f4076b8ebb24130e05bfbd8600e02ae84ee44da776b5647c1` | latest_review_evidence |
| N0151 | [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json](reference_conclusions.json) | `b3795a48af220c12aaf6fa4fc0d2640229cdb2870abbfdf2a63fe37e3191ba13` | latest_review_evidence |
| N0152 | [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json](scoring_rules.json) | `a719af35068540bf624a588f61a10d62327af736f5ad71340d8cc1488ebdd529` | latest_review_evidence |
| N0153 | [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `20abf203384694e62a649da22da87ce62e6f038a0903260561b5cbc679c4d9fa` | latest_review_evidence |
| N0154 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0cd74ae20ab933f3/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0cd74ae20ab933f3/verified_computation_reference.md) | `be5b074d933e58443805d0a34898e1397530f86766be3edda058b36fa7e3081b` | latest_review_evidence |
| N0155 | [tasks/v2_paper_reproduction/paper_0cd74ae20ab933f3/agent_input/task.md](../../../v2_paper_reproduction/paper_0cd74ae20ab933f3/agent_input/task.md) | `b6f62b8122276d730351d9d122dbce0c222e298078c0bbcbae7a65e52ec6375a` | latest_review_evidence |
| N0156 | [tasks/v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json) | `06d702dfccbd6d4f4076b8ebb24130e05bfbd8600e02ae84ee44da776b5647c1` | latest_review_evidence |
| N0157 | [tasks/v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json) | `b3795a48af220c12aaf6fa4fc0d2640229cdb2870abbfdf2a63fe37e3191ba13` | latest_review_evidence |
| N0158 | [tasks/v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json) | `a719af35068540bf624a588f61a10d62327af736f5ad71340d8cc1488ebdd529` | latest_review_evidence |
| N0159 | [tasks/v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_validation_plan.md](../../../v2_paper_reproduction/paper_0cd74ae20ab933f3/evaluation/reference_validation_plan.md) | `20abf203384694e62a649da22da87ce62e6f038a0903260561b5cbc679c4d9fa` | latest_review_evidence |
| N0160 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0cd74ae20ab933f3/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0cd74ae20ab933f3/verified_computation_reference.md) | `8898849cafd461ee20e5f5218786e5dece66e96ed018974e63d5bba902fd436e` | latest_review_evidence |
| N0161 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0162 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/agent_input/task.md](../agent_input/task.md) | `39f0da3a1a6d4ce9e05bbabe049eb542dacb0b2887dec32b0df8765a7f1f3d9a` |
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_key_points.json](reference_key_points.json) | `06d702dfccbd6d4f4076b8ebb24130e05bfbd8600e02ae84ee44da776b5647c1` |
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_conclusions.json](reference_conclusions.json) | `b3795a48af220c12aaf6fa4fc0d2640229cdb2870abbfdf2a63fe37e3191ba13` |
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/scoring_rules.json](scoring_rules.json) | `a719af35068540bf624a588f61a10d62327af736f5ad71340d8cc1488ebdd529` |
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/critical_failures.json](critical_failures.json) | `32a1d1e238cc114ddc415e2bdd009c94b9faf1b876df7015cb68d98c57e0ea8b` |
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/evidence_map.json](evidence_map.json) | `b83d611d27bcdc1fa5ce30cf5b93cecba07b014d2393e53a1867aaf776c417c6` |
| [tasks/v2_autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `20abf203384694e62a649da22da87ce62e6f038a0903260561b5cbc679c4d9fa` |

## Current scoring policy — 2026-10-19

The active policy is paper_science_v2: independent intermediate scientific findings and final conclusions sum to 100; no process points, partial-credit discretion or multiplier applies. Active nodes, rules, PDF sources and fixed inclusive tolerances are in the synchronized JSON files. Historical evaluator IDs, weights, freezes and process language in the preceding archive are not current scoring instructions. The public task and PR author-route contract are unchanged. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE acceptance and its scientific limitations remain; this migration runs no new chemistry calculations and does not certify publication readiness.

## Round 3 scoring-contract repair — 2026-10-19

Removed transitive OMe−H difference leaf10; retained two independent adjacent effects14/14. Intermediate/final remains70/30. Source spin-flip representation no longer excludes physically valid correlated-state evidence. Final family inference must add electronic interpretation beyond rank recital. Existing chemical acceptance and all archived measurements/results above are unchanged. This is a contract/rubric repair with no new quantum calculations or online Judge certification. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_01/REPORT.md.

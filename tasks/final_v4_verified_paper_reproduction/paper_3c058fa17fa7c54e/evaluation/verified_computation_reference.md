## 2026-10-28 V3范围与逐命题证据复用

四个最终态能规则 r_ph_s1/r_ph_t1/r_da_s1/r_da_t1 复用原生TD日志：Ph 3.1413/1.7339、DA 2.9733/1.7293 eV，相对原目标残差 −0.0044/−0.0008/−0.0102/+0.0009 eV，原±0.050 eV硬窗不变。r_singlet_substitution_response/r_triplet_similarity：S1(DA−Ph)=−0.1680 eV、T1变化−0.0046 eV；r_ph_tta_compatible/r_da_tta_compatible：2T1−S1=0.3265/0.4853 eV；r_small_gap_tadf：S1−T1=1.4074/1.2440 eV。r_molecular_solution_interpretation 复用同一日志中Ph S1 f=0.2768、DA S1 f=0.0001及S2 f=0.3206，结合公开Table 1观察，支持态能与吸收峰不等同和解释边界；未把能量允许当作溶液速率证明。

证据缺口：没有溶液TTA速率/产率、弛豫发射态或完整机制的验证；只评有界联系，不能把能量兼容升格为唯一机制；正文p4 Ph S/T次序及HOMO/LUMO标注冲突保留；本轮直接查看p2 Fig2确定S/T身份；旧评分要求氧敏感性但公开输入未给；删除该隐含证据门槛，保留已给寿命与光谱解释。本轮未重新计算、未进行盲测或语义评分验证；以下历史正文逐字保留，不继承旧PASS为V3全部通过。活动标准以scoring_rules.json为准。

# V2 验证计算参考：An-σ低态与TTA能量

论文：`paper_3c058fa17fa7c54e`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：冻结V2核心低态与TTA能量问题得到复现；不需为非必需HF onset重算。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

完整An-σ-Ph/DA低态差及TTA能量允许性，不含速率/器件。

冻结题面中的科学目标：

Determine how An-σ-Ph and An-σ-DA differ in their molecular excited-state behavior and whether their singlet/triplet energetics support triplet–triplet annihilation as an energetically accessible channel under a clearly stated molecular model. Explain what the evidence can and cannot establish about the observed solution photophysics.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors attribute anthracene-like deep-blue behavior to interruption of intramolecular conjugation by the saturated σ unit and discuss TTA energetic accessibility. The main paper reports B3LYP/6-31G(d,p) optimized structures/orbitals, TD state energies at the same basis, but also describes an HF UV calculation; the printed HOMO/LUMO and S1/T1 ordering passages are internally ambiguous. SI PDF2 names Gaussian16 B3LYP/6-31G(d,p). Reproduce a defensible interpretation of these source definitions, documenting inconsistencies rather than treating a printed inequality as an unambiguous target. Source experimental solution absorption/PL/lifetimes are provided. The source device measurements are outside this task.

Reproduce the disclosed author baseline within this scope, or justify a substitute scientifically and assess its consequences. Clearly distinguish this reproduction from your additional investigation. Source conclusions are conditional evidence, not an answer that must be affirmed; scientifically justified corrections or unresolved results remain eligible. The V1 benchmark interventions were not part of the author protocol and are not required in this version.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_3c058fa17fa7c54e/documents/main.pdf](../../../../papers/paper_3c058fa17fa7c54e/documents/main.pdf) | `38002008855a03bf3bd90f3315f0008ae9fff275c1305e6fca20494ff3850e86` |
| [papers/paper_3c058fa17fa7c54e/documents/supplementary_001.pdf](../../../../papers/paper_3c058fa17fa7c54e/documents/supplementary_001.pdf) | `01140712f70bcc77d7c656fcc6c211bc78e72aaac4e90d1d37e3b22b7a7162cd` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

源plain-B3LYP/6-31G(d,p)优化/频率与同几何singlet/triplet TD；源含糊的HF onset另列。

1. 核对完整 An-σ-Ph/DA 的 95/100 原子与 C55H34F6/C57H35F6NO 身份，修复并保留真正完整图的优化支路；源 plain-B3LYP 路线不能换成任意加色散版本而不说明。

2. 核收真实基态 Opt/Freq 最低点，再在同一几何、方法与介质定义下独立计算 singlet/triplet TD10；不同结构支路以及源/优化几何对照分别保存。

3. 提取 S1/T1：Ph=3.1413/1.7339 eV，DA=2.9733/1.7293 eV；与源 3.1457/1.7347、2.9835/1.7284 同量对照，保留 0.0008–0.0102 eV 残差。

4. 实际计算 2T1−S1 为 0.3265/0.4853 eV，与源 0.3237/0.4733 比较，并结合已执行的同 Hamiltonian 几何控制确认正裕量和分子差别。态身份以波函数/轨道证据审查，不将高态根序号或光学 onset 替代低态量。

5. 源 DA S2 简并、Ph 某些局域化图及 HF 切线 onset 的差异仍保留为未认证项；它们不被冒称已复现。当前通过限于低态与 TTA 能量可达性，不证明 TTA 速率、产率或器件效率。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Ph S1/T1,eV | [3.1457,1.7347] | [3.1413,1.7339] | 实算−论文：[-0.0044,-0.0008]； 真实完整结构与279正模；同方法几何控制支持核心低态结果。；源定位：main theoretical calculations |
| DA S1/T1,eV | [2.9835,1.7284] | [2.9733,1.7293] | 实算−论文：[-0.0102,0.0009]； 294正模；差异较Ph/DA S1差约0.16–0.17eV小，态定义一致，不是仅看margin。；源定位：main theoretical calculations |
| 2T1−S1,eV | [0.3237,0.4733] | [0.3265,0.4853] | 实算−论文：[0.0028,0.012]； 作者路线与同Hamiltonian有效分支均保持正裕量；非TTA速率。；源定位：main theoretical calculations |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| S1 / T1, Ph (eV) | [3.1457,1.7347] | [3.1413,1.7339] | Same source plain-B3LYP vertical-state convention on the declared valid native minimum. Residual −0.0044/−0.0008 eV is retained; no claim of four-decimal reproduction. Same-method geometry controls corroborate the robust molecular energy comparison. |
| S1 / T1, DA (eV) | [2.9835,1.7284] | [2.9733,1.7293] | Same source plain-B3LYP vertical-state convention on the correct full identity. Residual −0.0102/+0.0009 eV is modest compared with the approximately 0.16–0.17 eV Ph/DA S1 distinction, and same-Hamiltonian branch controls preserve the result. This is not acceptance by margin alone. |
| 2T1−S1, Ph/DA (eV) | [0.3237,0.4733] | [0.3265,0.4853] | TTA vertical energy excess; no rate or yield interpretation. Source/native differences are 0.0028/0.0120 eV. Explored valid geometry branches independently retain positivity; source closeness, route validity and controls jointly support the bounded result. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Check both stated molecular identities and every model's relation to them. Do not substitute an ethynyl bridge or clipped chromophore and call it the supplied molecule. Charge, spin, state, geometry and medium must be explicit; claim-specific geometry validity is assessed from the actual evidence.

冻结要求：Check both stated molecular identities and every model's relation to them. Do not substitute an ethynyl bridge or clipped chromophore and call it the supplied molecule. Charge, spin, state, geometry and medium must be explicit; claim-specific geometry validity is assessed from the actual evidence.

当前复审：95/100原子完整分子，不以乙炔桥或剪裁替代。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Both full sigma-linked identities and neutral molecular state inventories are correct; no clipped/ethynyl model is accepted."
  }
]
```


证据记录：`E0123`。

```json
[
  {
    "source_locator": "main p2 Fig1/Scheme1; SI p4 formulas; current systems.json",
    "actual_result": "95/100原子完整Ph/DA、中性S0单重态；源方法最低点279/294正频已验；Ph为原生negligible-force停止，不误当Freq额外预测位移必须全YES。",
    "reason": "对象/参照明确，旧失败几何未替代当前有效最低点。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/stdout.log",
        "sha256": "7071223cf77debac3c77e73dd47b7e04b431d21748a1076ee29be5690e033e30",
        "role": "source-method Ph minimum"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/stdout.log",
        "sha256": "c9acbc70912de2871f11d6a13d267730fec06b74c718237653f71810889a89bf",
        "role": "source-method DA minimum"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_native_minimum_reclassification.json",
        "sha256": "563097b73ac7456d0524ba206d195756b4c388b8dbd2fe6d91bd124dc38ee3d1",
        "role": "minimum native alternate-stop audit"
      }
    ]
  }
]
```

### kp_results — Assess whether the submitted numerical state and photophysical quantities substantiate the molecular question for both supplied systems. Reconstruct energy references and units from raw outputs. Do not equate a KS gap with an excitation or compare inconsistent vertical/relaxed references. No particular excited-state optimization or prescribed angle is compulsory.

冻结要求：Assess whether the submitted numerical state and photophysical quantities substantiate the molecular question for both supplied systems. Reconstruct energy references and units from raw outputs. Do not equate a KS gap with an excitation or compare inconsistent vertical/relaxed references. No particular excited-state optimization or prescribed angle is compulsory.

当前复审：本轮直接读回279/294正频率及四个S/T TD原生日志。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Native S1/T1 values and 2T1−S1 margins use consistent vertical references. Ph bright S1 and DA dark S1/bright S2 distinguish absorption maxima from lowest excitation."
  }
]
```


证据记录：`E0123`。

```json
[
  {
    "source_locator": "main p2 Fig2 + p3 §2.2; SI p2",
    "actual_result": "同几何S/T逐根收敛；Fig2明确Ph S1=3.1457、T1=1.7347，解决p4相反叙述的参照选择；实际能量和残差见表。",
    "reason": "继承语义能量判据；源标签由直接图证选择，非按大小交换。激发能不等KS gap/E00。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log",
        "sha256": "c5ad39e16717976055f62768b87626e1db42a3217c760fa85a6b8f63bed806b0",
        "role": "Ph singlets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/input.com",
        "sha256": "77fa02ec80852852322eea9da08d96e10f9ae97aa76b1f0be5024555dc5bb53e",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log",
        "sha256": "27668d17c84516eb0f2200f6e8a673fa3726e1e9fc0fea9e09eff4fece169afb",
        "role": "Ph triplets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/input.com",
        "sha256": "71ed3f9e9a3ff5b4088fd99c9589969feee4f8039dc1e51a4424cab7e49d95b3",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log",
        "sha256": "f0c75aa72cbcf151a861088d5fc0c4ac13644d0fcbc3f59685bdf6a8d1231ab2",
        "role": "DA singlets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/input.com",
        "sha256": "9765477b8b3ddaa70c8c3b83335cc231d5c443b1be7e65f9d659086b03cb08ac",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log",
        "sha256": "4080440192da014601f4f3eff889f50a38d22c03d9d432c64f69030cd3faadb5",
        "role": "DA triplets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/input.com",
        "sha256": "f08f16b06db34648fcff5e4bd4b007bb6f563f6944d7380ec68150f73cce122c",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_3c058fa17fa7c54e/main_p2_Fig2.png",
        "sha256": "218c97f8cbe7bebae1185ada068b878e4639e05a2cff096778f6d412e6fe8aa2",
        "role": "direct source Fig2 inspection"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/paper_3c058fa17fa7c54e.json",
        "sha256": "184047f48c403cff4819a73ac0f7a87d0d6093e5b6da061a5de7537c568a7030",
        "role": "native spin/80root replay"
      }
    ]
  }
]
```

### kp_interpretation — Assess how the observed/computed evidence discriminates the agent's molecular interpretation and tests energetic accessibility. Credit evidence-grounded positive, negative or unresolved interpretations. Do not require a bridge intervention, orbital-localization narrative or the authors' TTA conclusion.

冻结要求：Assess how the observed/computed evidence discriminates the agent's molecular interpretation and tests energetic accessibility. Credit evidence-grounded positive, negative or unresolved interpretations. Do not require a bridge intervention, orbital-localization narrative or the authors' TTA conclusion.

当前复审：低态变化与正2T1−S1支持能量可达性，不强推TTA效率。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "The computed low-state distinction and positive TTA energy margin support the bounded energetic inference. Native orbital evidence does not support every source localization narrative, and no such unique narrative is required."
  }
]
```


证据记录：`E0123`。

```json
[
  {
    "source_locator": "main p3–5; Table1/Fig4",
    "actual_result": "Ph有亮S1，DA最低S1近暗而S2亮；两分子sigma中心前线权重很低。Ph当前HOMO/LUMO可同侧，不强迫作者单幅轨道图。能量可达不是机制/碰撞率。",
    "reason": "当前节点明确不要求独特桥干预或作者TTA机制；实际态/轨道/观测解释覆盖两对象。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_DA_solution_source_spatial_join.json",
        "sha256": "e3bdacb410dc98702415a5937f4e757d2734bc454826149def74b0a7c5e4954b",
        "role": "existing orbital/observational comparison"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/paper_3c058fa17fa7c54e.json",
        "sha256": "184047f48c403cff4819a73ac0f7a87d0d6093e5b6da061a5de7537c568a7030",
        "role": "native spin/80root replay"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log",
        "sha256": "c5ad39e16717976055f62768b87626e1db42a3217c760fa85a6b8f63bed806b0",
        "role": "Ph singlets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/input.com",
        "sha256": "77fa02ec80852852322eea9da08d96e10f9ae97aa76b1f0be5024555dc5bb53e",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log",
        "sha256": "27668d17c84516eb0f2200f6e8a673fa3726e1e9fc0fea9e09eff4fece169afb",
        "role": "Ph triplets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/input.com",
        "sha256": "71ed3f9e9a3ff5b4088fd99c9589969feee4f8039dc1e51a4424cab7e49d95b3",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log",
        "sha256": "f0c75aa72cbcf151a861088d5fc0c4ac13644d0fcbc3f59685bdf6a8d1231ab2",
        "role": "DA singlets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/input.com",
        "sha256": "9765477b8b3ddaa70c8c3b83335cc231d5c443b1be7e65f9d659086b03cb08ac",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log",
        "sha256": "4080440192da014601f4f3eff889f50a38d22c03d9d432c64f69030cd3faadb5",
        "role": "DA triplets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/input.com",
        "sha256": "f08f16b06db34648fcff5e4bd4b007bb6f563f6944d7380ec68150f73cce122c",
        "role": "TD input"
      }
    ]
  }
]
```

### kp_uncertainty — Judge whether method, geometry, state and observational limitations could reverse the agent's claimed difference or energetic inference. Require relevant numerical or evidential bounds appropriate to the claim, not a predetermined sensitivity grid. A small reported energy margin cannot be declared decisive without its uncertainty being addressed.

冻结要求：Judge whether method, geometry, state and observational limitations could reverse the agent's claimed difference or energetic inference. Require relevant numerical or evidential bounds appropriate to the claim, not a predetermined sensitivity grid. A small reported energy margin cannot be declared decisive without its uncertainty being addressed.

当前复审：同Hamiltonian几何分支控制、垂直/松弛定义保持；源高态简并并未假称通过。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Valid older same-Hamiltonian branches give positive margins 0.4239/0.6406 eV versus current 0.3265/0.4853; the Ph fixed/source geometry→minimum margin shift is −0.0025 eV. These are explored-model controls, not a calibrated total functional-error bar."
  }
]
```


证据记录：`E0123`。

```json
[
  {
    "source_locator": "main p2 Fig2,p4 Table1; old validated branch",
    "actual_result": "旧D3BJ几何支线TTA裕量Ph0.4239/DA0.6406eV；当前plain0.3265/0.4853；Ph源方法旧/新固定几何裕量差0.0025eV。所有已算同类支线保留正裕量。不能据此保证未测试泛函/溶液环境或速率。",
    "reason": "量化实测敏感性支持有限模型结论，未制造0.1eV统一容差或绝对稳健性。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/strict_first_wave_returns.json",
        "sha256": "27f8e4af59d2c283c874907817abc74f1d8a5da53063a1b803a5b92f6ca0479e",
        "role": "source-method geometry sensitivity"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/report/results.json",
        "sha256": "244e86b934978cd846bf38d19afc59f53e2f983e7a61ceccd0fd3e8bd0d2cf55",
        "role": "old valid results"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/stdout.log",
        "sha256": "d15c8e48c12a34eb3b77b6fdffdff6a76a1c588bb83c1465eb2c8113b9f56b7b",
        "role": "old D3BJ-geometry sensitivity"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/input.com",
        "sha256": "3e02a95b653f2b1a75170e8efd2bcb31c4aa63dbb92099be25ab1a90c70dadd4",
        "role": "old input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/stdout.log",
        "sha256": "bd8f73fb747992360d617076c122a49ee1ea84539d4387ca06adbd7a9a05b8c1",
        "role": "old D3BJ-geometry sensitivity"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/input.com",
        "sha256": "82872f1d6518c14be16095d045abb2b07a109741795ed18f25e2d812ecd3614a",
        "role": "old input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/stdout.log",
        "sha256": "5592423f10cb61ca2b786c8ef509fb30479fcb1454d65a8b463459b461a76876",
        "role": "old D3BJ-geometry sensitivity"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/input.com",
        "sha256": "89ea6cf83f18d923f39e835258b0de590cb12c7b79197ffbc823c6ccbcb3e2a7",
        "role": "old input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/stdout.log",
        "sha256": "ce328f666d0c989eac933ff1585c04e6509ac004323168dfcbc105505b15d510",
        "role": "old D3BJ-geometry sensitivity"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/input.com",
        "sha256": "ace2a744a1efd2c3693ea9e4c4d33cf9f3ad2be82d59a205eb0cc72c7198a74c",
        "role": "old input"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/paper_3c058fa17fa7c54e.json",
        "sha256": "9d3ea5ca7f4922b594292c4165b1cf0e9885e5265324d3bfb0dccf6488505c11",
        "role": "official default-width audit"
      }
    ]
  }
]
```

### kp_audit — Verify that evidence IDs resolve to actual hash-matched raw artifacts, models/methods are linked, and numerical transformations can be reproduced. Inspect research_log against real tool traces for process claims. Neither schema validity, normal termination, hypothesis count nor self-written chronology proves scientific validity.

冻结要求：Verify that evidence IDs resolve to actual hash-matched raw artifacts, models/methods are linked, and numerical transformations can be reproduced. Inspect research_log against real tool traces for process claims. Neither schema validity, normal termination, hypothesis count nor self-written chronology proves scientific validity.

当前复审：冻结V2核心低态与TTA能量问题得到复现；不需为非必需HF onset重算。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Six primary minimum/TD native logs, source Fig.2 and the existing evidence index are inspected; real raw outputs, not acceptance booleans, support the state quantities."
  }
]
```


证据记录：`E0123`。

```json
[
  {
    "source_locator": "current V2 AR/PR rules; source and native chain",
    "actual_result": "源PDF→Fig2读数、优化→same-geometryS/T、旧真实结果及HPC后处理均逐文件hash绑定；两个历史失败由成功后继替代但仍留档。",
    "reason": "没有虚构的新运行，也不从旧PASS字样直接导出当前通过。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log",
        "sha256": "c5ad39e16717976055f62768b87626e1db42a3217c760fa85a6b8f63bed806b0",
        "role": "Ph singlets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/input.com",
        "sha256": "77fa02ec80852852322eea9da08d96e10f9ae97aa76b1f0be5024555dc5bb53e",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log",
        "sha256": "27668d17c84516eb0f2200f6e8a673fa3726e1e9fc0fea9e09eff4fece169afb",
        "role": "Ph triplets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/input.com",
        "sha256": "71ed3f9e9a3ff5b4088fd99c9589969feee4f8039dc1e51a4424cab7e49d95b3",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log",
        "sha256": "f0c75aa72cbcf151a861088d5fc0c4ac13644d0fcbc3f59685bdf6a8d1231ab2",
        "role": "DA singlets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/input.com",
        "sha256": "9765477b8b3ddaa70c8c3b83335cc231d5c443b1be7e65f9d659086b03cb08ac",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log",
        "sha256": "4080440192da014601f4f3eff889f50a38d22c03d9d432c64f69030cd3faadb5",
        "role": "DA triplets"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/input.com",
        "sha256": "f08f16b06db34648fcff5e4bd4b007bb6f563f6944d7380ec68150f73cce122c",
        "role": "TD input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/stdout.log",
        "sha256": "7071223cf77debac3c77e73dd47b7e04b431d21748a1076ee29be5690e033e30",
        "role": "source-method Ph minimum"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/stdout.log",
        "sha256": "c9acbc70912de2871f11d6a13d267730fec06b74c718237653f71810889a89bf",
        "role": "source-method DA minimum"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/paper_3c058fa17fa7c54e.json",
        "sha256": "184047f48c403cff4819a73ac0f7a87d0d6093e5b6da061a5de7537c568a7030",
        "role": "native spin/80root replay"
      }
    ]
  }
]
```

### conclusion_answer — The final answer must state what is supported about the two molecules' excited behavior and TTA energy accessibility, identify unresolved scope and avoid inferring a rate, yield or OLED performance from molecular energy compatibility. Negative or adequately supported nonidentifiability can earn full credit.

冻结要求：The final answer must state what is supported about the two molecules' excited behavior and TTA energy accessibility, identify unresolved scope and avoid inferring a rate, yield or OLED performance from molecular energy compatibility. Negative or adequately supported nonidentifiability can earn full credit.

当前复审：冻结V2核心低态与TTA能量问题得到复现；不需为非必需HF onset重算。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Energetic TTA accessibility and model-level excited-state differences are supported; exact high-state degeneracy, rates, yields and OLED performance are not."
  }
]
```


证据记录：`E0123`。

```json
[
  {
    "source_locator": "main p2–5 and current question",
    "actual_result": "在明确的气相B3LYP/6-31G(d,p)垂直激发模型下，Ph/DA的S1分别3.1413/2.9733eV，T1分别1.7339/1.7293eV；2T1−S1=0.3265/0.4853eV，支持两者TTA能量可达。Ph最低单重态有可见强度，DA存在更低暗S1及约398nm亮S2；与395/396nm近同吸收及不同溶液寿命/PL相容。旧独立几何分支保持同样能量条件，但不提供普适理论误差界，因此不能把能量可达升级为溶液TTA速率、产率、唯一机制或OLED性能。",
    "reason": "当前问题在明确分子模型下回答能量可达与可辨差异，范围完整且与作者核心能量条件一致。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/paper_3c058fa17fa7c54e.json",
        "sha256": "184047f48c403cff4819a73ac0f7a87d0d6093e5b6da061a5de7537c568a7030",
        "role": "native spin/80root replay"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_DA_solution_source_spatial_join.json",
        "sha256": "e3bdacb410dc98702415a5937f4e757d2734bc454826149def74b0a7c5e4954b",
        "role": "existing orbital/observational comparison"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/strict_first_wave_returns.json",
        "sha256": "27f8e4af59d2c283c874907817abc74f1d8a5da53063a1b803a5b92f6ca0479e",
        "role": "source-method geometry sensitivity"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 15.34 小时；17 份计时日志/23 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 16,20 线程/进程；Gaussian %Mem=100GB,60GB,80GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0002 · strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log) | Gaussian:937.1 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0003 · strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log) | Gaussian:2072.1 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0004 · v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log) | Gaussian:569.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log) | Gaussian:950.9 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/stdout.log) | Gaussian:3862；Gaussian:2005.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · An_sigma_DA_source_identity_corrected_optfreq/attempt_002/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/stdout.log) | Gaussian:9872.7；Gaussian:2581 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0040 · author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/stdout.log) | Gaussian:2537 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0049 · reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/stdout.log) | Gaussian:2555.6 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0052 · hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/stdout.log) | Gaussian:8703.9；Gaussian:1612.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0055 · td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/stdout.log) | Gaussian:490.6 | 正常 | {"threads":[16],"Gaussian_mem":["60GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0058 · td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/stdout.log) | Gaussian:737.2 | 正常 | {"threads":[16],"Gaussian_mem":["60GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0061 · hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/stdout.log) | Gaussian:2741.2；Gaussian:1783.4 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0064 · td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/stdout.log) | Gaussian:485.5 | 正常 | {"threads":[16],"Gaussian_mem":["60GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0067 · td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/stdout.log) | Gaussian:446.7 | 正常 | {"threads":[16],"Gaussian_mem":["60GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0080 · An_sigma_Ph/Hirshfeld_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Hirshfeld_75_434/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0081 · An_sigma_Ph/Becke_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Becke_75_434/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0082 · An_sigma_Ph/Hirshfeld_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Hirshfeld_100_590/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0083 · An_sigma_Ph/Becke_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Becke_100_590/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0090 · An_sigma_DA/Hirshfeld_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Hirshfeld_75_434/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0091 · An_sigma_DA/Becke_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Becke_75_434/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0092 · An_sigma_DA/Hirshfeld_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Hirshfeld_100_590/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0093 · An_sigma_DA/Becke_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Becke_100_590/native.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0100 · cases/returned_comparison_repair_GV04_20261007/stdout.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0127 · hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log) | Gaussian:2903.5；Gaussian:1810.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0132 · hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log) | Gaussian:2775.8；Gaussian:1887.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0165 · v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/stdout.log) | Gaussian:912.7 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0216 · cases/retained_definition_replay/stdout.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0219 · cases/retained_definition_replay/stderr.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/stderr.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0224 · cases/returned_comparison_20261007/stdout.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/stdout.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0227 · cases/returned_comparison_20261007/stderr.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/stderr.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0231 · cases/returned_comparison_repair_GV04_20261007/stderr.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

DA S2简并、部分轨道局域图和HF切线onset未认证。；无法由此认证TTA量子产率/速率、OLED性能。

```json
[
  "DA source S2=2.9835 versus native 3.1151 eV is an explicit 0.1316 eV nonreproduction; exact S1/S2 degeneracy is not a required conclusion.",
  "Source Ph orbital localization across opposite anthracenes is not reproduced; the bounded interpretation is correspondingly revised.",
  "HF tangent onsets 3.1443/3.1308 versus source 3.04/3.01 eV are not certified matches and are not mixed with vertical S1/T1.",
  "The source figure reverses HOMO/LUMO labels; this source inconsistency remains.",
  "Explored-geometry stability of a TTA inequality does not prove solution TTA rates or total functional accuracy."
]
```


原独立审查的 `unresolved_issues`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  {
    "id": "U1",
    "blocking": false,
    "kind": "source_internal_spin_and_orbital_label_conflict",
    "source": "main PDF p2 Fig2 versus p3–4 prose",
    "finding": "Ph prose S1/T1 is reversed relative to the spin-labelled figure; HOMO/LUMO labels and energies are also reversed. Fig2 spin labels are used with direct visual evidence. No author-confirmed erratum is asserted.",
    "impact": "Does not alter the same-reference core TTA test; the conflicting passages remain traceable."
  },
  {
    "id": "U2",
    "blocking": false,
    "kind": "source_higher_state_mismatch",
    "source": "main PDF p2 Fig2",
    "finding": "DA source S1/S2=2.9835eV; native2.9733/3.1151eV, splitting0.1418eV and S2 residual+0.1316eV.",
    "impact": "Exact source high-root degeneracy is not reproduced. Current identity, lowest-state energy condition and observed-versus-bright-state discussion do not rely on that degeneracy; do not silently swap root identities to match it."
  },
  {
    "id": "U3",
    "blocking": false,
    "kind": "source_Ph_orbital_picture_mismatch",
    "source": "main PDF p2 Fig2 and p3 §2.2",
    "finding": "Current Ph canonical HOMO/LUMO mainly occupy the same anthracene; source depicts opposite units.",
    "impact": "No unique orbital-localization/causal bridge claim is accepted; current evaluator does not require that narrative. Native state differences and energetic inequality remain supported independently."
  },
  {
    "id": "U4",
    "blocking": false,
    "kind": "undisclosed_spectral_onset_definition",
    "source": "main PDF p3 simulated Eg and SI PDF p8 FigS7",
    "finding": "Fixed0.4eV 1/e-half-width HF curves reproduce the low-band shape approximately, but red-slope tangents3.14430665/3.13080238eV do not equal printed3.04/3.01eV. Raster green-line intersections3.11661347/3.07536319eV also differ.",
    "impact": "Exact tangent/plot rule remains unknown, not proved permanently unobtainable. The discrepancy is retained and is not excused by pixel precision. No tangent is used as vertical S1 or as an input to2T1-S1."
  },
  {
    "id": "U5",
    "blocking": false,
    "kind": "model_to_solution_and_historical_binary_limits",
    "source": "main PDF p4 Table1/p5; retained checkpoint manifests",
    "finding": "No source raw replicate uncertainty or solution triplet-energy measurement; finite geometry/integration checks do not calibrate solution or functional error. Old origin binaries absent after historical cleanup.",
    "impact": "Only declared-model inference is accepted; old text/manifest/geometry provenance supports reuse without falsely claiming current binary verification."
  }
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_3c058fa17fa7c54e.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_3c058fa17fa7c54e/verified_computation_reference.md)；SHA-256 `b1c583b81eddf89e4224a08c4879a5175315f8b433def3cb468d0e73d7474cde`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_3c058fa17fa7c54e_780d20f078e8e9.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_3c058fa17fa7c54e_780d20f078e8e9.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_3c058fa17fa7c54e_780d20f078e8e9.json) | `91b6bbd85d068f1e9a45fa9ac10db26829e8990da3697ba4fe6651668565eed7` | evidence_or_analysis |
| E0002 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_native_excerpt.json) | `c5ad39e16717976055f62768b87626e1db42a3217c760fa85a6b8f63bed806b0` | native_output |
| E0003 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_native_excerpt.json) | `27668d17c84516eb0f2200f6e8a673fa3726e1e9fc0fea9e09eff4fece169afb` | native_output |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `f0c75aa72cbcf151a861088d5fc0c4ac13644d0fcbc3f59685bdf6a8d1231ab2` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `4080440192da014601f4f3eff889f50a38d22c03d9d432c64f69030cd3faadb5` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `7071223cf77debac3c77e73dd47b7e04b431d21748a1076ee29be5690e033e30` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `c9acbc70912de2871f11d6a13d267730fec06b74c718237653f71810889a89bf` | native_output |
| E0008 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_3c058fa17fa7c54e/main_p2_Fig2.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_3c058fa17fa7c54e/main_p2_Fig2.png) | `218c97f8cbe7bebae1185ada068b878e4639e05a2cff096778f6d412e6fe8aa2` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3c058fa17fa7c54e/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3c058fa17fa7c54e/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_main.json) | `6b44014c6a1b80f1574a34e8e503fa61127a86db4d01cc05a6901ee0ed8c237a` | evidence_or_analysis |
| E0010 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3c058fa17fa7c54e/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3c058fa17fa7c54e/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_supplementary_001.json) | `09e35e8d8703e9984ad314f66753218fc8ea0cf99de3b2be0e72dd21beadac45` | evidence_or_analysis |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_task.md) | `26bdcd9ff68beb344561ba6d7bafffae4270b8b311dacf388ed7925215eb586f` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_reference_key_points.json) | `dbe2e15c6e49064454d0d38b1a14dddb2898a10163b40e5afb44282b37f6bbc8` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_reference_conclusions.json) | `523c1fb57e5a9f7a73cf829700f2fc932c6ed66e948bf57cd505ccc8c9c902ba` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_task.md) | `d878c8dcf58048734b76e82638f60470aa74c50ea3848298ed151d1d4129bb6c` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_reference_key_points.json) | `dbe2e15c6e49064454d0d38b1a14dddb2898a10163b40e5afb44282b37f6bbc8` | historical_task_binding |
| E0016 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_reference_conclusions.json) | `523c1fb57e5a9f7a73cf829700f2fc932c6ed66e948bf57cd505ccc8c9c902ba` | historical_task_binding |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_3c058fa17fa7c54e/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_3c058fa17fa7c54e/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_COMPUTATION_INVENTORY.json) | `8a11e92bee00f167e091e25b889a45f81d610660468af7a1dc3d17336bd528d0` | evidence_or_analysis |
| E0018 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/LATEST_RECORD.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/LATEST_RECORD.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_LATEST_RECORD.json) | `7b8804c2e9b9fa00a22b88cb9f673736a6e01177ccada9153ff0122d33ffa14c` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/NATIVE_EVIDENCE_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/NATIVE_EVIDENCE_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_NATIVE_EVIDENCE_INDEX.json) | `7eb982546a850f8ff6c2e9f288ba85fe6aa557665a798ba0194f753a49f68f7d` | evidence_or_analysis |
| E0020 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/SOURCE_COMPARISON.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/SOURCE_COMPARISON.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_SOURCE_COMPARISON.json) | `95d0f88b4e7956cde19175c83b3ba0d7f60ecf6f8a1ff4a223bf53a43d9465b5` | evidence_or_analysis |
| E0021 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/CALCULATION_LINKS.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/CALCULATION_LINKS.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_CALCULATION_LINKS.json) | `0cb04f00318270c12d13889c327e91523671c86273cd31f448668132831ea55b` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/SOURCE_QUANTITIES.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/SOURCE_QUANTITIES.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_SOURCE_QUANTITIES.json) | `023bd8a4ccdae46d56ec2fe0bd418361a2aa32a61cc9e4e2ad6c3da81d3f6056` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_3c058fa17fa7c54e.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_3c058fa17fa7c54e.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_paper_3c058fa17fa7c54e.md) | `f4544411520b75842efad6cc95c7c890c620bfa468c96b28f1203ccebb119528` | evidence_or_analysis |
| E0024 | [docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `84eca624d651a2228026817cf9d36edbe3205e4a096c1efed2cbce2493e9dded` | historical_task_binding |
| E0025 | [papers/paper_3c058fa17fa7c54e/documents/main.pdf](../../../../papers/paper_3c058fa17fa7c54e/documents/main.pdf) | `38002008855a03bf3bd90f3315f0008ae9fff275c1305e6fca20494ff3850e86` | source_document |
| E0026 | [papers/paper_3c058fa17fa7c54e/documents/supplementary_001.pdf](../../../../papers/paper_3c058fa17fa7c54e/documents/supplementary_001.pdf) | `01140712f70bcc77d7c656fcc6c211bc78e72aaac4e90d1d37e3b22b7a7162cd` | source_document |
| E0027 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/agent_input/data/inputs/systems.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/agent_input/data/inputs/systems.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_systems.json) | `9beb287f43f74ebb2e9f788c58b27db91978c10cde2dba3907a0c2d596bb290f` | historical_task_binding |
| E0028 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/agent_input/data/inputs/solution_observations.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/agent_input/data/inputs/solution_observations.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_solution_observations.json) | `c6d98802aeabdc1a29a540c90c73bf2072434bc64c79a675d85143034726fac3` | historical_task_binding |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/SOURCE_QUANTITIES.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/SOURCE_QUANTITIES.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_SOURCE_QUANTITIES.json) | `91cd5c73789a8bb85904e6439de96f07a822e42e08882592e56b9a147e3fb627` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/CALCULATION_LINKS.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/CALCULATION_LINKS.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_CALCULATION_LINKS.json) | `6e81f8d132cef3983bca81cf9afc6d28ac7d41f62396928a6fe5b32b0c0d9b2d` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/NATIVE_EVIDENCE_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/NATIVE_EVIDENCE_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_NATIVE_EVIDENCE_INDEX.json) | `743d57d88a01a9231f26b54f476dd2c0fba0b853133a9768cabdff3c75f46ebc` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/LINEAGE_AUDIT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/LINEAGE_AUDIT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_LINEAGE_AUDIT.json) | `5ca6a4101af585fd49c4e9175b0ce469b704c5f4862435dea21d00f1f1fe03c9` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/REVIEW_RESPONSE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/REVIEW_RESPONSE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_REVIEW_RESPONSE.json) | `05632a50ba3925323c19a1770e1651aca355b6ef0cf7a9849c70a7b0c2bec86f` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_input.com) | `0f16c4d7aa9dbc79e213dee1b722a4546259142dab8ff1e2eaf3b03c97c5cff3` | input_or_analysis_code |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_input.com) | `77fa02ec80852852322eea9da08d96e10f9ae97aa76b1f0be5024555dc5bb53e` | input_or_analysis_code |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_input.com) | `71ed3f9e9a3ff5b4088fd99c9589969feee4f8039dc1e51a4424cab7e49d95b3` | input_or_analysis_code |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_native_excerpt.json) | `e3fd576f518015ae1aa3ed5fa1c2ce654ef4d5832018b3279561427381f61616` | native_output |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_input.com) | `ca00bd8b3e9cc4e6bf8101d64226f2e1cda4bc3dd82a375e426ef65d240b3fed` | input_or_analysis_code |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_input.com) | `cc1717f9010791bb9b2fa66f3748427dc328de2b945540f3547b5b934c4201bb` | input_or_analysis_code |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_input.com) | `9765477b8b3ddaa70c8c3b83335cc231d5c443b1be7e65f9d659086b03cb08ac` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_input.com) | `f08f16b06db34648fcff5e4bd4b007bb6f563f6944d7380ec68150f73cce122c` | input_or_analysis_code |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_native_excerpt.json) | `f772b2980b5c08d84dbd236bd761a8e249a7da611f952e58754c97ebdf02ece3` | native_output |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_input.com) | `7f7249f3271dd567bcbc05212f088a1fea25472dc04c63aea1eb02b1099c6a49` | input_or_analysis_code |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_native_excerpt.json) | `5f341b69ae5c80d65ed4c4605fb2a17c04c6db848717e0a13492c2f9f5111ddb` | native_output |
| E0053 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_input.com) | `c8499b973f04086e0f8de3f8bc102769a614b8a8d27cc366d738aaff1c0f3e79` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_native_excerpt.json) | `d15c8e48c12a34eb3b77b6fdffdff6a76a1c588bb83c1465eb2c8113b9f56b7b` | native_output |
| E0056 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_input.com) | `3e02a95b653f2b1a75170e8efd2bcb31c4aa63dbb92099be25ab1a90c70dadd4` | input_or_analysis_code |
| E0057 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_native_excerpt.json) | `bd8f73fb747992360d617076c122a49ee1ea84539d4387ca06adbd7a9a05b8c1` | native_output |
| E0059 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_input.com) | `82872f1d6518c14be16095d045abb2b07a109741795ed18f25e2d812ecd3614a` | input_or_analysis_code |
| E0060 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_native_excerpt.json) | `49f7e23827c009f6d7b887c09c890e4b79a9ef357b2354e20830307edad4f995` | native_output |
| E0062 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_input.com) | `fbb6e1aa94a2c5fb16b5e2dc6f0ef7c8512c1aa67ef68de6f9105355c5a3c2cb` | input_or_analysis_code |
| E0063 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_native_excerpt.json) | `5592423f10cb61ca2b786c8ef509fb30479fcb1454d65a8b463459b461a76876` | native_output |
| E0065 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_input.com) | `89ea6cf83f18d923f39e835258b0de590cb12c7b79197ffbc823c6ccbcb3e2a7` | input_or_analysis_code |
| E0066 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_native_excerpt.json) | `ce328f666d0c989eac933ff1585c04e6509ac004323168dfcbc105505b15d510` | native_output |
| E0068 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_input.com) | `ace2a744a1efd2c3693ea9e4c4d33cf9f3ad2be82d59a205eb0cc72c7198a74c` | input_or_analysis_code |
| E0069 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_native_minimum_reclassification.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_native_minimum_reclassification.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_ph_native_minimum_reclassification.json) | `563097b73ac7456d0524ba206d195756b4c388b8dbd2fe6d91bd124dc38ee3d1` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/v2_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/v2_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_v2_returns.json) | `83f32ce6c2f5ff4af9f30ee90ca112cca4660726dd9bac5121413e3ccc77223e` | evidence_or_analysis |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_DA_solution_source_spatial_join.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_DA_solution_source_spatial_join.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_ph_DA_solution_source_spatial_join.json) | `e3bdacb410dc98702415a5937f4e757d2734bc454826149def74b0a7c5e4954b` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/strict_first_wave_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/strict_first_wave_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_strict_first_wave_returns.json) | `27f8e4af59d2c283c874907817abc74f1d8a5da53063a1b803a5b92f6ca0479e` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/orbital_partition_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/orbital_partition_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_orbital_partition_results.json) | `b67ee155982a7116a04102a054d2c45272f768c90091d4aafc06490ec2f896b8` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/orbital_runtime.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/orbital_runtime.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_orbital_runtime.py) | `2fc66a5bb9d5f9a73cd3117cfb0746a858eb57cfac5afc1bd3e92010ad6be066` | input_or_analysis_code |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/runtime.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/runtime.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_runtime.py) | `dacc41323d9a957296d3e811744379bbc76feb29695875d95fd2856509107af9` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_submission.json) | `7f752c41f1f283c79fb73812a96070a6d896fa0587ce9a520c78533b6f6e885b` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/input.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_input.json) | `f364f677c2064e998a7b27191349257d0ec952bfe1e1691f0bc81d5008aef14b` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Hirshfeld_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Hirshfeld_75_434/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_native_excerpt.json) | `ff0bd09c81585cba12617eb89fe9fe4e192f9dfc13f7a3f15b66f555f0313a63` | native_output |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Becke_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Becke_75_434/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_native_excerpt.json) | `0af93b49669586a164b4048173c2adaee4d4fcfcf79caa8bd23a296f5b57092c` | native_output |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Hirshfeld_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Hirshfeld_100_590/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_native_excerpt.json) | `e42fb99f069972e8fc1b6c82c5282497646857132d8b7065673905e8ec35b24f` | native_output |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Becke_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/Becke_100_590/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_native_excerpt.json) | `21d5a3e799a47eca6ac0e4e4b97ffafa4675ef8f3faea43af705277c50dcbf55` | native_output |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/orbital_partition_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/orbital_partition_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_orbital_partition_results.json) | `2bbd79e5ccd5c92ec576cd534c9ca33a5ac0c6773e2348f81d7a80867b3f69db` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/orbital_runtime.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/orbital_runtime.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_orbital_runtime.py) | `2fc66a5bb9d5f9a73cd3117cfb0746a858eb57cfac5afc1bd3e92010ad6be066` | input_or_analysis_code |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/runtime.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/runtime.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_runtime.py) | `dacc41323d9a957296d3e811744379bbc76feb29695875d95fd2856509107af9` | input_or_analysis_code |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_submission.json) | `548d3dc9f01b8bf05ecc219e0cc73282314ca4bf7bb2a5099dce5110e7176025` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/input.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_input.json) | `dafb9e9aa243dbe17284a1c31c454404a9aa0e58dabf55c0f2c14d7af0379fb4` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Hirshfeld_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Hirshfeld_75_434/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_native_excerpt.json) | `056060886f9d1268098a6822983935fae699599bc6c38c339f6f29b482278bb4` | native_output |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Becke_75_434/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Becke_75_434/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_native_excerpt.json) | `9a31cd46aa26f435cefedcb60a4f8488332ec8c2151d1ad954a0b8e7ee33a175` | native_output |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Hirshfeld_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Hirshfeld_100_590/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_native_excerpt.json) | `4d1364479cb82ef6062714a9cfa19365c1d62b77e1f19b033386abbbd6ef0631` | native_output |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Becke_100_590/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/Becke_100_590/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_native_excerpt.json) | `5e1b9a787f058653f3835fa2bc7f6ce8f059f0831474f0147c2c36222d6d2bea` | native_output |
| E0094 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/paper_3c058fa17fa7c54e.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/paper_3c058fa17fa7c54e.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_paper_3c058fa17fa7c54e.json) | `9d3ea5ca7f4922b594292c4165b1cf0e9885e5265324d3bfb0dccf6488505c11` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/compare_repair.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/compare_repair.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_compare_repair.py) | `76e4dc7ab1545b88253f7e809b23799d171bcc438a3690b76fd84ba41d30e72b` | input_or_analysis_code |
| E0096 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/submission.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_submission.json) | `4c8cb161e66cbd909763f99472efe2d023eb4a580ed2ac0a54bfba2ff38092b9` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/native_acceptance.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/native_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_native_acceptance.json) | `c8ef893236726614c50adb7314c2ad2d656a6b6955c9a511e7fe93aa2e7f379b` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/exit_code](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0099 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/manifest.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_manifest.json) | `61f284cfd1376f318b5d1cce7e8663542f6f9cc44aedbfbb9413af10427e9b9a` | evidence_or_analysis |
| E0100 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/stdout.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_native_excerpt.json) | `57448e620fa9a232b6125d2ef788af5cc81148d24aced547b3bffbfe77eda9f5` | native_output |
| E0101 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3c058fa17fa7c54e/source/SI8_embedded_0.jpeg](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3c058fa17fa7c54e/source/SI8_embedded_0.jpeg) | `a33e3834e841847a9ec1afe93c454b37a589e9b23f2972634b13f5d69a0cc6e7` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/AnSigma_default_width_source.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/AnSigma_default_width_source.png) | `d2a112d98555a6909f83f989626904cce7358ae2d65db6729a28bcffaa0a6504` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_3c058fa17fa7c54e_4a002143ef7247.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_3c058fa17fa7c54e_4a002143ef7247.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_paper_3c058fa17fa7c54e_4a002143ef7247.json) | `c23ea28a47daf43b056d1df2a0fdf3ab1132c737cf7ab078838a5284b1ff976d` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_entrypoint.sh) | `85a397e4315fe78df19749f2c4c0175a4d4e06f9cedf527d34259d98e3ece5e1` | input_or_analysis_code |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_entrypoint.sh) | `85a397e4315fe78df19749f2c4c0175a4d4e06f9cedf527d34259d98e3ece5e1` | input_or_analysis_code |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0106_entrypoint.sh) | `85a397e4315fe78df19749f2c4c0175a4d4e06f9cedf527d34259d98e3ece5e1` | input_or_analysis_code |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_entrypoint.sh) | `85a397e4315fe78df19749f2c4c0175a4d4e06f9cedf527d34259d98e3ece5e1` | input_or_analysis_code |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_entrypoint.sh) | `85a397e4315fe78df19749f2c4c0175a4d4e06f9cedf527d34259d98e3ece5e1` | input_or_analysis_code |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_entrypoint.sh) | `995843dcd4dac588242a28398b8c595a4f9913d7cef51936818cb74cd35e5fbd` | input_or_analysis_code |
| E0110 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_scoring_rules.json) | `5e6d7a17b69844c22767c30d419241b61c79f8cc70d3de91029d7d89a49a816e` | historical_task_binding |
| E0111 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3c058fa17fa7c54e/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0111_critical_failures.json) | `4def94b621d78eb31ebcaa3ad662933780199c1b6dfde7da8ac5e59f277e4564` | historical_task_binding |
| E0112 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_scoring_rules.json) | `5e6d7a17b69844c22767c30d419241b61c79f8cc70d3de91029d7d89a49a816e` | historical_task_binding |
| E0113 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3c058fa17fa7c54e/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_critical_failures.json) | `4def94b621d78eb31ebcaa3ad662933780199c1b6dfde7da8ac5e59f277e4564` | historical_task_binding |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0121 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/wrapper_exit_code](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0122 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/evidence.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0122_evidence.json) | `82287688a49aae3241f2d5f81602b13904576e33dd2ccca4b6569c7789fc8834` | evidence_or_analysis |
| E0123 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_3c058fa17fa7c54e/CURRENT_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_3c058fa17fa7c54e/CURRENT_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0123_CURRENT_REVIEW.json) | `f4d7cffda72ad146c69f5de58c8d0207e8cc71931c7e9343d82cf108df7da3bd` | evidence_or_analysis |
| E0124 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/report/results.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/report/results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0124_results.json) | `244e86b934978cd846bf38d19afc59f53e2f983e7a61ceccd0fd3e8bd0d2cf55` | evidence_or_analysis |
| E0125 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/paper_3c058fa17fa7c54e.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/paper_3c058fa17fa7c54e.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0125_paper_3c058fa17fa7c54e.json) | `184047f48c403cff4819a73ac0f7a87d0d6093e5b6da061a5de7537c568a7030` | evidence_or_analysis |
| E0126 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/SOURCE_COMPARISON.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/SOURCE_COMPARISON.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0126_SOURCE_COMPARISON.json) | `95d0f88b4e7956cde19175c83b3ba0d7f60ecf6f8a1ff4a223bf53a43d9465b5` | evidence_or_analysis |
| E0127 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0127_native_excerpt.json) | `c14084a692a88c3dcd55b1003c39f1861fcb32cbb84c65dd1ae2e40559ed6566` | native_output |
| E0128 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_Ph_singlet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_Ph_singlet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0128_input_manifest.json) | `77430f27a38cd941eae99e00ee1b8563744d33f73ed2c0089c09cc6dbc829c9d` | evidence_or_analysis |
| E0129 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0129_input_manifest.json) | `1d5bc1d9c6dab66e9599090c8b007ed4b3e6ee77cbb36dd77d7b8d37923b651e` | evidence_or_analysis |
| E0130 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_Ph_triplet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_Ph_triplet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0130_input_manifest.json) | `93d0c5033330f96f30fcf0b38d1a84cdf28051b7972009bb3877770f956d6587` | evidence_or_analysis |
| E0131 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0131_input_manifest.json) | `a20dd88d433b74b8255c12350850dca2a4a15bf1d2748318c5c4af6cdaf26881` | evidence_or_analysis |
| E0132 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0132_native_excerpt.json) | `c0bfe80cd3a3b7ef95653a312d9fbac08a011dbd67ecd35518ea0d69d96ff191` | native_output |
| E0133 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_DA_singlet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_DA_singlet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0133_input_manifest.json) | `d664316bbb3d73949e6049366c370df1b1d6c0e861501827d714c0fff35d4444` | evidence_or_analysis |
| E0134 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0134_input_manifest.json) | `cdfe08a93e5b5a2036880842ad90571ba76c0f2414b78c762069ccdf7cc39828` | evidence_or_analysis |
| E0135 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_DA_triplet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/provenance/local_stability_tests_20260910/td_exact_route/An_sigma_DA_triplet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0135_input_manifest.json) | `621229737c592880f0fef57d213ca94b9e469cfcca939aa784fbdb37e27168ab` | evidence_or_analysis |
| E0136 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/input_manifest.json](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/input_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0136_input_manifest.json) | `05601493f0b82d5c069dbf1a89a88e0fd5707762016ee32efb30e4b5c389ee89` | evidence_or_analysis |
| E0137 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0137_input.com) | `cbb2bff5443b70ce6cbf1171802138e05ff977d59d625d238df9df5e97d4cf21` | input_or_analysis_code |
| E0138 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0139 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0139_input.com) | `1849591c5ae9e34883b51472763816365e457e50e56f497efd9ab79e26a78a4d` | input_or_analysis_code |
| E0140 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/exit_code](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0141 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/SOURCE_COMPARISON.before_reviewfix.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_3c058fa17fa7c54e/reviewfix_55a92d176ddf56/SOURCE_COMPARISON.before_reviewfix.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0141_SOURCE_COMPARISON.before_reviewfix.json) | `6f0077a7c168562209486c15d1cf7f05e8f104737fd1874cb7bd50ff47d78854` | evidence_or_analysis |
| E0142 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0142_entrypoint.sh) | `06c6cf811e00d013dfe98dfc58ad7d03503a4fdbb752caed2f9dd30945bacadb` | input_or_analysis_code |
| E0143 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/postprocess.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/postprocess.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0143_postprocess.py) | `cbfc0f5fc767ac57cef82c0f1f844c1bd2524e32933515fa18d25c63c5406061` | input_or_analysis_code |
| E0144 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0144_entrypoint.sh) | `8da8e080e0af0e2dbe597ef0baf478d60eec2e78e4e181466b5144a94ef72f85` | input_or_analysis_code |
| E0145 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/postprocess.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/postprocess.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0145_postprocess.py) | `49737e1bc7493dbdeb28dbed58683cd33e1ca37b4d32b95b952de1612097cb8a` | input_or_analysis_code |
| E0146 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0146_entrypoint.sh) | `9e03a1db9fdf6964eb620e9d5769d9743279413ad97fa60ef436303197044ed2` | input_or_analysis_code |
| E0147 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/input_original.com](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_8d723004b65942b2b2f11811a0c7d433/input_original.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0147_input_original.com) | `1ba36bb408f16135aefd915446cd8f4bdcccc7acccad2b48ad27b1b51e0d6c81` | input_or_analysis_code |
| E0148 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0148_entrypoint.sh) | `9a66f4a4e064c19f09cce6c41c7a533965a52387ff1a83b9e90948a555584192` | input_or_analysis_code |
| E0149 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0149_entrypoint.sh) | `b3fa37a5d3adb47145095e8becd5b067f50534091de69ec121cc8e78112e959c` | input_or_analysis_code |
| E0150 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/local_migration_job_86d50091fb9e4a99bd4f59e6ca7a11fb__resubmit_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0150_entrypoint.sh) | `b8cb4cf282514c4ebce7e97eca64887a076f252b2c655c5f849d37248d5d6fbf` | input_or_analysis_code |
| E0151 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0151_entrypoint.sh) | `d6e90412da55f110ba3f1dd7ed54092e2e080c5327958c2116034c5bd1727360` | input_or_analysis_code |
| E0152 | [docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0152_entrypoint.sh) | `f9e24545642220d4ea142bb7fbd07f7bc5791ab231d55529247c9b83e173a2a5` | input_or_analysis_code |
| E0153 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/provenance/source_text/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/provenance/source_text/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0153_main.txt) | `2f1d8a34aa4ffe034823606f2567a7d6a48cdd1e6ebbcec6b1cfd543cbdeb1f6` | evidence_or_analysis |
| E0154 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/provenance/source_text/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/provenance/source_text/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0154_supplementary_001.txt) | `b7408448fda78ee454b611ef11527904d6a905c1030c39769bd87f1550d35f72` | evidence_or_analysis |
| E0155 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_minimum_orbital_coverage_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/ph_minimum_orbital_coverage_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0155_ph_minimum_orbital_coverage_returns.json) | `48e61c4249bf6f920883fd42ed8629779af4bd5caa731bd1d8251c6f33bcbf7b` | evidence_or_analysis |
| E0156 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/bounded_conclusions/paper_3c058fa17fa7c54e.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/bounded_conclusions/paper_3c058fa17fa7c54e.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0156_paper_3c058fa17fa7c54e.json) | `eb503f537b1f33a307fa0d9f66303ef63bd1533890b20385b1662fb2cb1913a2` | evidence_or_analysis |
| E0157 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/checkpoint.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/checkpoint.fchk) | `47bce961ce4acc2df69d46e1480900e74b918327eb4953e136c8afb1887924c0` | evidence_or_analysis |
| E0158 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/checkpoint.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/checkpoint.fchk) | `7188d4ea4d8005137ede0d209ab1dfa00adcf0d84a54a7b144bca90a80980c58` | evidence_or_analysis |
| E0159 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0159_entrypoint.sh) | `7a7ac8ae2008ee3b27b4ee6e7aeae03f18cd5a1c99fe95d772e89e49fe69b308` | input_or_analysis_code |
| E0160 | [.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI) | `d7d2539dae7b8d2faf03ca473d856cf1936a7b8ca4fdcfbb3e1cfa5f45184030` | evidence_or_analysis |
| E0161 | [.software_cache/installations/gaussian/g16/install/g16/formchk](../../../../.software_cache/installations/gaussian/g16/install/g16/formchk) | `78dc9981fd170cc99d8052aa26471244e04fd2c8aea7d73aaf641c193e7b6bd5` | evidence_or_analysis |
| E0162 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/checkpoint.chk) | `20ac2f13232fa5b204230a4ab89d914f7398951da07f5e8dbf61627e5be8f9e9` | evidence_or_analysis |
| E0163 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0163_entrypoint.sh) | `7a7ac8ae2008ee3b27b4ee6e7aeae03f18cd5a1c99fe95d772e89e49fe69b308` | input_or_analysis_code |
| E0164 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/checkpoint.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/checkpoint.fchk) | `d6fef388ae10113ee618e3a79b496702618b37b60a949204a4698a3c62fc1fa7` | evidence_or_analysis |
| E0165 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0165_native_excerpt.json) | `0757d0223e82a11f871167bb8f91704168a58b3057808c35433408d4d5c688a8` | native_output |
| E0166 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/checkpoint.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/checkpoint.fchk) | `7311e6f875bfe82a23fb37f06949378a5c90382da244536549f8c326c54963d6` | evidence_or_analysis |
| E0183 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/public_recheck_20261007/uvvis_eq5.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/public_recheck_20261007/uvvis_eq5.png) | `eae0bb85a899acb278a4f7a968adcf87a1b9df9aaffed1c831a8cc9ae34aca66` | evidence_or_analysis |
| E0184 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/public_recheck_20261007/gaussian_uvvis.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/public_recheck_20261007/gaussian_uvvis.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0184_gaussian_uvvis.txt) | `b1f5a4669b79e5f1638cc9b0cfc1ce35dace4d19ed8566d7690f75a45bb2cf8d` | evidence_or_analysis |
| E0185 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/entrypoint.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0185_entrypoint.sh) | `e9ef3d943bb729ce62e6ec54c180c1fa7a2736974239e8cb91348c3e68399cd3` | input_or_analysis_code |
| E0186 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_3c058fa17fa7c54e_4a002143ef7247_input.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_3c058fa17fa7c54e_4a002143ef7247_input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0186_paper_3c058fa17fa7c54e_4a002143ef7247_input.json) | `4b633c364466c938018ded9544b11936bce83bdeac7df12db54a0c805064e1ff` | evidence_or_analysis |
| E0187 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sigma_orbital_coverage_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sigma_orbital_coverage_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0187_sigma_orbital_coverage_returns.json) | `75833d1498034aaa55da83e176bac9b35a371563e275e633889ff689ece68ba9` | evidence_or_analysis |
| E0188 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/input.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_Ph_accepted_minimum_four_orbital_partitions/attempt_001/An_sigma_Ph/input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0188_input.json) | `6498b6209e8adefaee8f89b33bba0334c607aaa797a4e8bab693c9d46cb9d6ce` | evidence_or_analysis |
| E0189 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/input.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_sigma_Ph_DA_existing_frontier_four_orbital_partitions/attempt_001/An_sigma_DA/input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0189_input.json) | `466a0ffb9b137d0623ae21e861d4600b5bb32c6eba2b27a2792f1eb6e9a687fd` | evidence_or_analysis |
| E0190 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_plainB3LYP_optfreq_recovery/attempt_003/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0190_submission.json) | `9b9a1c09a386ffcabf89ad55c19c8776c409bfe7e4b4e78f713e406d3d923b1e` | evidence_or_analysis |
| E0191 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_singlets_TD10/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0191_submission.json) | `9a35718e55b3ed455a51f5dfccaaf3308a6386bde1ea52caf65327539c311134` | evidence_or_analysis |
| E0192 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/strict_An_sigma_Ph_native_minimum_triplets_TD10/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0192_submission.json) | `b2856aefabb5d87ef4287b27e90b4dabeef9dea9b3aef8012e43b50e0ebf17ab` | evidence_or_analysis |
| E0193 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/author_route_An_sigma_Ph_HF_sourceUV_window_TD80_read/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0193_submission.json) | `e5233569a2cbb027a15df6a4548de95a1ea1d65cedd1976057e06a1967fa794e` | evidence_or_analysis |
| E0194 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/An_sigma_DA_source_identity_corrected_optfreq/attempt_002/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0194_submission.json) | `32559a40813ea67dc538a89336799dbefc02b2b1bf2631a7d7d61a6863cc9fe1` | evidence_or_analysis |
| E0195 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_singlets_TD10/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0195_submission.json) | `fc950f834d007f964ae70d218b43404f4a46983db3cd8d8090de5f36990f9c91` | evidence_or_analysis |
| E0196 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_DA_plainB3LYP_triplets_TD10/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0196_submission.json) | `1cc850819fdda7c9d6a6e1e7c2cf3ba9d319fbe4ef9df9d733d4239ab7dd47a6` | evidence_or_analysis |
| E0197 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/reopen_DA_HF84_checkpoint_guard4_same_Conver6/attempt_001/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0197_submission.json) | `be0a8bec0c909881392361cad4d1c4ee0ccaf9517d8e71cecf390d5a801fa73d` | evidence_or_analysis |
| E0198 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/DA_partial_window_results.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/DA_partial_window_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0198_DA_partial_window_results.json) | `a8fdbcf18d818d90f2da77449df3fd8d5f53dd1bd0b415913ee2f0cec71b5bc5` | evidence_or_analysis |
| E0199 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/spectrum_FWHM_0.15.csv](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/spectrum_FWHM_0.15.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0199_spectrum_FWHM_0.15.csv) | `a9089125e505136ff6743c676058af7d74cd620e43f31fd912657372c2fb52fa` | evidence_or_analysis |
| E0200 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/spectrum_FWHM_0.3.csv](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/spectrum_FWHM_0.3.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0200_spectrum_FWHM_0.3.csv) | `21ab37d4ed9a7dce4527b5077311ebadd00f6e3b624ea81fa03b61ff9e85503e` | evidence_or_analysis |
| E0201 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/spectrum_FWHM_0.45.csv](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/HF_final_window/attempt_001/spectrum_FWHM_0.45.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0201_spectrum_FWHM_0.45.csv) | `6eae2ca844ccdfd1c0abe03b0065036c16d29bf5e3be2827b06183c2c7579c44` | evidence_or_analysis |
| E0203 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/DBC_SOURCE_ROUTE_RECOVERY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/DBC_SOURCE_ROUTE_RECOVERY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0203_DBC_SOURCE_ROUTE_RECOVERY.json) | `e173048a0cd460c117630e4fffc25f20db2967e1679fbd355746471ddab738c6` | evidence_or_analysis |
| E0216 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/stdout.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0216_native_excerpt.json) | `df439d21070fcd172e97ed0725525b5545b24d885b080f3e8b4560e7fd754ee5` | native_output |
| E0217 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/exit_code](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0218 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/wrapper_exit_code](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0219 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/stderr.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0219_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0220 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/native_acceptance.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/native_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0220_native_acceptance.json) | `e582dd406cc933b454c91005a883bff90d5bd1b1a8a4e472880b3e9b48cf45fc` | evidence_or_analysis |
| E0221 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/submission_intent.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/submission_intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0221_submission_intent.json) | `b68e95d01ea86fe7ce2a75243ca3057a675c845348d8ecec178d638ba720f290` | evidence_or_analysis |
| E0222 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/submission.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0222_submission.json) | `42f96a943efb48ba4ad00b44f2c356006fb79e591313aff33b547ee5bc88f7b5` | evidence_or_analysis |
| E0223 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_and_reaudit_20261008T0318Z/deliveries/W03.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_and_reaudit_20261008T0318Z/deliveries/W03.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0223_W03.json) | `8ac94f449e5b0a7515aa09e9fc36dc4146be84de3bf335ead975639aec370686` | evidence_or_analysis |
| E0224 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/stdout.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0224_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0225 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/exit_code](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/exit_code) | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | evidence_or_analysis |
| E0226 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/wrapper_exit_code](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/wrapper_exit_code) | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | evidence_or_analysis |
| E0227 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/stderr.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0227_native_excerpt.json) | `9af2c3b16f93bcaac14c77291162db157818f87ee5065a37cf20999ad85d6700` | native_output |
| E0228 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/submission_intent.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/submission_intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0228_submission_intent.json) | `6e6ac74a25368d0f15781b4d1fd10e5beb71d470a308c2206289f825d03faf78` | evidence_or_analysis |
| E0229 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/submission.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0229_submission.json) | `257032e9e355c31b167b241c88109e122184ff3b70014777eddcf5740a1ef76a` | evidence_or_analysis |
| E0230 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/wrapper_exit_code](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/wrapper_exit_code) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0231 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/stderr.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0231_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0232 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/submission_intent.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_repair_GV04_20261007/submission_intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0232_submission_intent.json) | `43ee40b114258d06279fb59ee0cce757e9b026443fde98e8f800f0bbfcd55b39` | evidence_or_analysis |
| E0233 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0233_entrypoint.sh) | `85a397e4315fe78df19749f2c4c0175a4d4e06f9cedf527d34259d98e3ece5e1` | input_or_analysis_code |
| E0234 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_3c058fa17fa7c54e/outputs/v2_An_sigma_Ph_fixed_failedprecision_geometry_singlets_TD10/attempt_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0234_input.com) | `64a4d787b043dedf4ea4d5ff187f5d90905b76d4d792938c855deaf2c9601964` | input_or_analysis_code |
| E0260 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/entrypoint.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/retained_definition_replay/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0260_entrypoint.sh) | `2000ecb9127cb099f1e30daa19bfcefa3f41a308f0d8e05b04da93001ca392a8` | input_or_analysis_code |
| E0261 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/entrypoint.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0261_entrypoint.sh) | `38b121beb50de4b02e54006e423ad9fa495faa04cc2e923d4901657dd5ce5228` | input_or_analysis_code |
| E0262 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/returned_compare.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/cases/returned_comparison_20261007/returned_compare.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3c058fa17fa7c54e/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0262_returned_compare.py) | `deba59db961f10d0da56b82bd3e810588a05c2979073b2976f57b2d147d4fed7` | input_or_analysis_code |
| N0209 | [tasks/v2_autonomous_research/paper_3c058fa17fa7c54e/agent_input/task.md](../../../v2_autonomous_research/paper_3c058fa17fa7c54e/agent_input/task.md) | `26bdcd9ff68beb344561ba6d7bafffae4270b8b311dacf388ed7925215eb586f` | latest_review_evidence |
| N0210 | [tasks/v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json) | `dbe2e15c6e49064454d0d38b1a14dddb2898a10163b40e5afb44282b37f6bbc8` | latest_review_evidence |
| N0211 | [tasks/v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json) | `523c1fb57e5a9f7a73cf829700f2fc932c6ed66e948bf57cd505ccc8c9c902ba` | latest_review_evidence |
| N0212 | [tasks/v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json) | `5e6d7a17b69844c22767c30d419241b61c79f8cc70d3de91029d7d89a49a816e` | latest_review_evidence |
| N0213 | [tasks/v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_3c058fa17fa7c54e/evaluation/reference_validation_plan.md) | `9b77d299a576918ec1a481d4f40f559277f24c013e8edd3c9e473a066dbe5517` | latest_review_evidence |
| N0214 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_3c058fa17fa7c54e/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_3c058fa17fa7c54e/verified_computation_reference.md) | `9a3185ba2d9dbb52d9be8616925a6a567819ad11fe8b62c7c786a0682d53e4f1` | latest_review_evidence |
| N0215 | [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/agent_input/task.md](../agent_input/task.md) | `d878c8dcf58048734b76e82638f60470aa74c50ea3848298ed151d1d4129bb6c` | latest_review_evidence |
| N0216 | [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json](reference_key_points.json) | `dbe2e15c6e49064454d0d38b1a14dddb2898a10163b40e5afb44282b37f6bbc8` | latest_review_evidence |
| N0217 | [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json](reference_conclusions.json) | `523c1fb57e5a9f7a73cf829700f2fc932c6ed66e948bf57cd505ccc8c9c902ba` | latest_review_evidence |
| N0218 | [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json](scoring_rules.json) | `5e6d7a17b69844c22767c30d419241b61c79f8cc70d3de91029d7d89a49a816e` | latest_review_evidence |
| N0219 | [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `9b77d299a576918ec1a481d4f40f559277f24c013e8edd3c9e473a066dbe5517` | latest_review_evidence |
| N0220 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_3c058fa17fa7c54e/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_3c058fa17fa7c54e/verified_computation_reference.md) | `b1c583b81eddf89e4224a08c4879a5175315f8b433def3cb468d0e73d7474cde` | latest_review_evidence |
| N0221 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0222 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/agent_input/task.md](../agent_input/task.md) | `d878c8dcf58048734b76e82638f60470aa74c50ea3848298ed151d1d4129bb6c` |
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_key_points.json](reference_key_points.json) | `dbe2e15c6e49064454d0d38b1a14dddb2898a10163b40e5afb44282b37f6bbc8` |
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_conclusions.json](reference_conclusions.json) | `523c1fb57e5a9f7a73cf829700f2fc932c6ed66e948bf57cd505ccc8c9c902ba` |
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/scoring_rules.json](scoring_rules.json) | `5e6d7a17b69844c22767c30d419241b61c79f8cc70d3de91029d7d89a49a816e` |
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/critical_failures.json](critical_failures.json) | `4def94b621d78eb31ebcaa3ad662933780199c1b6dfde7da8ac5e59f277e4564` |
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/evidence_map.json](evidence_map.json) | `d8eb4afee8d713b506b081e6c508482a5bdccbc30dbcd8966a7b21803ad05866` |
| [tasks/v2_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `9b77d299a576918ec1a481d4f40f559277f24c013e8edd3c9e473a066dbe5517` |

## Current scientific scoring policy — 2026-10-19

Active scoring is paper_science_v2: independent binary intermediate findings and final conclusions total 100. The synchronized JSON files replace historical process weights, partial-credit discretion and obsolete scoring freezes. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE and all recorded residuals/limitations remain; migration performs no new chemical validation. Public input, task_info.json and paper_route.md remain byte-identical. Source-versus-verification quantities are kept distinct; the new tolerances are fixed benchmark criteria, not fitted offsets. Historical reference-stage text above is provenance rather than the current runtime gate.


## Authorized public-contract and scientific-rule repair — 2026-10-19 round3

This repair preserves every preceding historical computation/acceptance statement verbatim. Current scoring remains paper_science_v2,100 independent scientific points. Mode-specific public objects now control AR eligibility; PR retains its disclosed source-baseline targets. Necessary experimental lifetime facts and obsolete process-score prose are repaired in public files where applicable. No source task, original paper, native computation, engine or historical acceptance is changed. Source/verification residuals and uncalibrated method-transfer limits remain; this is not a new chemical validation or online Judge result. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_02/paper_3c058fa17fa7c54e.md.

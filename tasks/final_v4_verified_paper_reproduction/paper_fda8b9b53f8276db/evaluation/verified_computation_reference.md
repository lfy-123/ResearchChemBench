# V3 scope and evidence reuse — 2026-10-28

Same free neutral singlet ligand and local molecular-versus-crystal structure question; no Re, biological, global conformer or lattice scope. Six final cis-basin bond properties retain their original targets and ±0.01 A windows. Public same-side candidate identity makes the pre-existing reference basin explicit without disclosing its stability or crystal orientation. No separate optimization-completion points.

Six final bond rules reuse native cis_gas lengths 1.4893836346/1.4256919932/1.3393508724/1.3161615032/1.3099111402/1.3989213292 A, all within original source windows. The orientation outcome reuses the 36.652415-degree molecular torsion versus -155.187862-degree experimental torsion, intact mapped graph, four converged Tight criteria and 87 positive modes (minimum41.5141 cm^-1); local-minimum validity is evidence, not a separate score. Local correspondence reuses signed residuals and RMSE0.0041514785 A; the 0.001 A marginal ESD is not the 0.0005 A rounding bound and covariance is absent. Phase interpretation is bounded by gas/crystal model differences and the existing trans control, lower by22.8426608 kJ/mol electronic energy and22.6606874 kJ/mol raw298.15K/1atm G: cis is not a proven global winner. Gaussian16 substitutes03; author grid unknown. Source/native reflection-equivalent heavy-atom RMSD0.0022304239 A supersedes an unreflected0.6209 A mapping; fixed-source-coordinate force/curvature diagnostics are not reoptimizations. Two angle differences beyond printed rounding remain context, not new numerical targets. Historical bounded acceptance does not establish a new V3 PASS.

Final rules: r_bond_c1_c2, r_bond_c2_c3, r_bond_n1_c1, r_bond_n2_c2, r_bond_n3_c3, r_bond_c1_c10, r_orientation_contrast, r_local_core_correspondence, r_phase_model_interpretation.

The following text is unchanged historical verification, including its old policy/status wording. It is not a declaration of a new V3 PASS. No new calculations were performed.

---

# V2 验证计算参考：自由喹喔啉配体

论文：`paper_fda8b9b53f8276db`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：本轮读源页和两原生OptFreq；小角差有实际源坐标/网格控制，结构核心结果一致。不把V3成功或失败反推到本篇自由配体V2。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

自由配体的分子结构与晶体结构如何对应及解释差异的限度。

冻结题面中的科学目标：

What molecular description of the free quinoxaline ligand is supported by the supplied crystal structure and an independent molecular investigation, and how should agreement or disagreement with the crystal geometry be interpreted? Establish which structural conclusions are reliable and which remain model dependent.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors use crystal-derived initial coordinates and B3LYP/6-311+G(2d,p) for free ligand1, with vibrational validation; their source Gaussian03 molecular calculation gives a cis pyridyl orientation while the experimental crystal is trans (main p4, SI TablesS2–S3/FigsS10–S11). They attribute the difference to gas versus packed solid conditions and report small selected bond residuals. Those are a local computed structure and an interpretation, not proof of exhaustive conformational or lattice thermodynamics. Reproduce that disclosed molecular baseline or explain substitutions. The previous mandatory MeCN and torsional controls were builder additions and are no longer required.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_fda8b9b53f8276db/documents/main.pdf](../../../../papers/paper_fda8b9b53f8276db/documents/main.pdf) | `0afa69242ab928c082802d029d66eaa4c3c58cea7f791438d64de1c7f88de8d1` |
| [papers/paper_fda8b9b53f8276db/documents/supplementary_001.pdf](../../../../papers/paper_fda8b9b53f8276db/documents/supplementary_001.pdf) | `13ace6b2daec90e737a69c21f21a4af2d7cab7a54b967859e270ca1147c496de` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

C15H13N3、B3LYP/6-311+G(2d,p)气相cis/trans OptFreq，Gaussian16替03；源几何/网格和曲率检查。

1. 由精修 CIF 与源 SI 核对完整 C15H13N3、31 原子配体及原子标号，排除旧 oxdiff 错误分子式；原始 CIF 不修改。

2. 按气相 B3LYP/6-311+G(2d,p) 执行 cis/trans Opt/Freq，两端四项 Tight 条件及各 87 正模通过。源 Gaussian03 与实际 Gaussian16 差别明示。

3. 从相同图/反射等价 cis 几何提取六键四角，对照 SI 理论表与晶体中央坐标/ESD。六条理论键长恢复源三位小数；理论-晶体 RMSE=0.00415148 Å 对源 0.004 Å，两个角残差 +0.01274095/−0.02292966° 保留。

4. 实际完成源坐标 Fine/UltraFine 梯度与曲率控制及 atom-map 检查，cis 重原子 RMS=0.0022304 Å；trans 是独立低能气相最低点，不能用其较低 G 解释固体布居。

5. 以有限局部结构与两个有效气相盆地解释分子/晶体对照；未知晶体协方差、相态及软件/网格限制保留，不将 ESD/打印位数变成统一 DFT 容差，也不外推 Re 配合物或生物活性。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

#### required_calculations（冻结记录 E0008）

```json
[
  {
    "id": "free_ligand_cis_Opt_Freq",
    "purpose": "Recover source finite free-ligand model and test minimum",
    "author_or_added": "author",
    "source_locator": "Main physicalp4§2.4; SI physicalpp10–13,TablesS2/S3,FigsS10/S11; original CCDC2433822CIF.",
    "identity": "C15H13N3,31atoms,neutral singlet; original CIF labels retained",
    "method": "B3LYP/6-311+G(2d,p), gas; Gaussian16 substitution for Gaussian03 explicitly disclosed",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log",
        "sha256": "0d6e46df42cfefbe413525ee3f465ae300b69cde02256e84e89d60be668da778",
        "bytes": 389935
      }
    ],
    "native_validity": "NativeOpt completed and87positive modes; full atom mapping separate from stale CIF acquisition metadata."
  },
  {
    "id": "trans_and_source_structure_analysis",
    "purpose": "Quantify local bonds/angles versus source and separate conformation from phase",
    "author_or_added": "added_validation_and_required_analysis",
    "source_locator": "Main physicalp4§2.4; SI physicalpp10–13,TablesS2/S3,FigsS10/S11; original CCDC2433822CIF.",
    "identity": "Same free ligand and full source coordinates/CIF",
    "method": "Independent transgas minimum plus existing HPC metric, derivative/grid and source-coordinate analyses",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log",
        "sha256": "3a0a9c1703dd535e0ed0ab50842c5b05419ced062e21de0b34e446916dfa67ed",
        "bytes": 489630
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      }
    ],
    "native_validity": "Transalso87positive modes; sixbonds/fourangles/full source map are computed, residual and uncertainty definitions retained."
  }
]
```


#### reused_results（冻结记录 E0008）

```json
[
  "docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/NATIVE_REUSE_READBACK.json"
]
```

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| 记录量 (A) | 1.489 | 未给出／不适用 |  |
| 记录量 (A) | 1.426 | 未给出／不适用 |  |
| 记录量 (A) | 1.339 | 未给出／不适用 |  |
| 记录量 (A) | 1.316 | 未给出／不适用 |  |
| 记录量 (A) | 1.31 | 未给出／不适用 |  |
| 记录量 (A) | 1.399 | 未给出／不适用 |  |
| 记录量 (orientation) | computedcis/crystaltrans | 未给出／不适用 | No lattice selection inference |
| 记录量 (degree) | 117.3 | 未给出／不适用 | Same mapped free-ligand cis gas structure; crystal angle separately recorded |
| 记录量 (degree) | 116.68 | 未给出／不适用 | Same mapped free-ligand cis gas structure; crystal angle separately recorded |
| 记录量 (degree) | 118.14 | 未给出／不适用 | Same mapped free-ligand cis gas structure; crystal angle separately recorded |
| 记录量 (degree) | 118.58 | 未给出／不适用 | Same mapped free-ligand cis gas structure; crystal angle separately recorded |
| 记录量 (A) | 0.004 | 未给出／不适用 | SixTableS2bondresiduals againstprintedexperimentalcentralvalues; ESDcovariance/modelerrornotabsorbedintoauniformtolerance |

两构型各87正模；六源理论键长与0.001 Å打印相容，理论/晶体RMSE0.00415148 Å对0.004；两角残差+0.01274095/-0.02292966°。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Map the full ligand graph and CIF labels consistently; distinguish free ligand1 from the Re complex and do not confuse molecular orientations with connectivity changes. Recognize the stale _chemical_oxdiff_formula C12H12N2O; the refined atom table and formula_sum/moiety establish C15H13N3. Correctly disclosed atom relabeling or metadata-conflict resolution is valid and must not be failed for disagreeing with the stale field.

冻结要求：Map the full ligand graph and CIF labels consistently; distinguish free ligand1 from the Re complex and do not confuse molecular orientations with connectivity changes. Recognize the stale _chemical_oxdiff_formula C12H12N2O; the refined atom table and formula_sum/moiety establish C15H13N3. Correctly disclosed atom relabeling or metadata-conflict resolution is valid and must not be failed for disagreeing with the stale field. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：全图/CIF对应、六键四角与完整几何、局部最低点、晶体trans/源分子cis差异和模型边界均覆盖。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Fullgraph,CIFrefinedformula C15H13N3 andlabelmapverified; staleoxdiffformulaexcluded, originalCIFunchanged.",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```


证据记录：`E0030`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```

### kp_quantitative_evidence — Check structural quantities extracted from genuine models against correctly mapped measured coordinates/bonds, including metric definitions, original precision and crystallographic uncertainty. The reported ESD is not a universal electronic-structure tolerance.

冻结要求：Check structural quantities extracted from genuine models against correctly mapped measured coordinates/bonds, including metric definitions, original precision and crystallographic uncertainty. The reported ESD is not a universal electronic-structure tolerance. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：全图/CIF对应、六键四角与完整几何、局部最低点、晶体trans/源分子cis差异和模型边界均覆盖。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Sixsourcebonds/fourangles pluscrystalESDs andCIFcentralcoordinates; signedresiduals retained, noESDorprintingconvertedtoDFTtolerance. RMSEcis.00415148A,trans.00310558A.",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```


证据记录：`E0030`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```

### kp_scientific_answer — Judge the evidence supporting the proposed molecular structure and interpretation of crystal/model differences. No prescribed cis winner, solvent contrast or torsional scan is mandatory; alternative structures and evidence-supported unresolved phase attribution are eligible.

冻结要求：Judge the evidence supporting the proposed molecular structure and interpretation of crystal/model differences. No prescribed cis winner, solvent contrast or torsional scan is mandatory; alternative structures and evidence-supported unresolved phase attribution are eligible. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：全图/CIF对应、六键四角与完整几何、局部最低点、晶体trans/源分子cis差异和模型边界均覆盖。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Correctfree31atomligand and localbondgeometry are supported. Sourcecislocalbasin and independenttransminimum are both real on the disclosedgassurface; translowerG doesnotexplainsolidpopulation. Crystal/modeldifference is an evidencedfinite structuralcomparison; packingasuniquecause remainsunproven.",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```


证据记录：`E0030`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```

### kp_validity_and_uncertainty — Verify any claimed optimized state or structural minimum and define the molecular/experimental environments compared. If reporting residuals, state the included atoms/bonds and statistic; separate marginal crystallographic ESDs, absent covariance, rounding and model error. A local minimum is not a certified global minimum, and bond agreement alone cannot explain a phase-dependent conformation.

冻结要求：Verify any claimed optimized state or structural minimum and define the molecular/experimental environments compared. If reporting residuals, state the included atoms/bonds and statistic; separate marginal crystallographic ESDs, absent covariance, rounding and model error. A local minimum is not a certified global minimum, and bond agreement alone cannot explain a phase-dependent conformation. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：全图/CIF对应、六键四角与完整几何、局部最低点、晶体trans/源分子cis差异和模型边界均覆盖。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "TwogasOpt/FreqminimaallTightcriteria and87positivefrequencies; sourceS3fixedcurvature/gradient/gridcontrolseparate. G03/G16,numericalgrid,finitebasins,unknowncrystalcovarianceandphaseinterpretationdisclosed.",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```


证据记录：`E0030`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```

### kp_bounded_conclusion — Do not equate agreement of several local bonds with a globally correct conformation or phase equilibrium. Finite molecular energies do not establish crystal lattice free energy, solid-state conformer populations, Re-complex behavior or biological activity.

冻结要求：Do not equate agreement of several local bonds with a globally correct conformation or phase equilibrium. Finite molecular energies do not establish crystal lattice free energy, solid-state conformer populations, Re-complex behavior or biological activity. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：全图/CIF对应、六键四角与完整几何、局部最低点、晶体trans/源分子cis差异和模型边界均覆盖。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Wholepublicquestionaddressed by actualmodelidentity/structure/relativebasins and evidence-limitedphaseinterpretation; noRe/biology/latticeclaims.",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```


证据记录：`E0030`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```

### bounded_answer — A source-bounded evidence-supported answer to: What molecular description of the free quinoxaline ligand is supported by the supplied crystal structure and an independent molecular investigation, and how should agreement or disagreement with the crystal geometry be interpreted? Establish which structural conclusions are reliable and which remain model dependent.

冻结要求：Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question. Do not equate agreement of several local bonds with a globally correct conformation or phase equilibrium. Finite molecular energies do not establish crystal lattice free energy, solid-state conformer populations, Re-complex behavior or biological activity.

当前复审：全图/CIF对应、六键四角与完整几何、局部最低点、晶体trans/源分子cis差异和模型边界均覆盖。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "basis": "Correctfree31atomligand and localbondgeometry are supported. Sourcecislocalbasin and independenttransminimum are both real on the disclosedgassurface; translowerG doesnotexplainsolidpopulation. Crystal/modeldifference is an evidencedfinite structuralcomparison; packingasuniquecause remainsunproven.",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```


证据记录：`E0030`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json",
        "sha256": "73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d",
        "bytes": 1407
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json",
        "sha256": "1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505",
        "bytes": 26928
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json",
        "sha256": "8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a",
        "bytes": 5955
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json",
        "sha256": "463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859",
        "bytes": 1395
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json",
        "sha256": "7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd",
        "bytes": 10067
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json",
        "sha256": "f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6",
        "bytes": 3455
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json",
        "sha256": "33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767",
        "bytes": 3447
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json",
        "sha256": "ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2",
        "bytes": 5688
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json",
        "sha256": "52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa",
        "bytes": 3464
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json",
        "sha256": "ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea",
        "bytes": 18537
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 2.35 小时；7 份计时日志/12 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,20 线程/进程；Gaussian %Mem=12GB,70GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0025 · outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log) | Gaussian:797.3；Gaussian:730.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0027 · outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log) | Gaussian:911.1；Gaussian:722.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0049 · outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log) | Gaussian:816.4；Gaussian:684.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0052 · outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log) | Gaussian:1574.1；Gaussian:790.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0087 · outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/stdout.log) | Gaussian:566.8；Gaussian:44.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0093 · outputs/cis_gas_SuperFineGrid_sensitivity_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/stdout.log) | Gaussian:414.4 | 正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0095 · outputs/trans_gas_SuperFineGrid_sensitivity_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/stdout.log) | Gaussian:394.2 | 正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0100 · outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0101 · outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stderr.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0103 · outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0105 · outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0108 · outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0109 · outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0111 · outputs/ligand_source_derivative_readback_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0112 · outputs/ligand_source_derivative_readback_strict_a1/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

不是gas全局cis最稳定或只因晶格导致构象的证明；V3完整Re配合物需独立验证。

不宣称gas全局一定偏好cis或仅晶格导致构象；MeCN/Re扩展和旧可选MeCN二进制hash漂移不用于本次范围。


原独立审查的 `acceptance_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Two sourceTableS2 angles differ+.01274095/-.02292966degree; explicitly notexactprintednumberreproduction",
  "SourceS3 vsS2 internalangle difference .00535648degree; do notforce printagreement",
  "Mirror-equivalentcis twist disclosed; properrotation-onlyheavyRMS.620918A not silentlyreplaced",
  "FineGridnotclaimedactualG03grid; fixedsourcefreq/force notnewoptimizedminimum",
  "AllatomNewton cosine is notinterpretable duehydrogenmapping; onlydisclosedheavyatommetricsused",
  "Nocondensedphasepopulation/latticefreeenergy/globalminimumclaim",
  "OptionalMeCN historicalbinarycause andoldbytes notclosed; neitherrequirednorusedtoearncoregate",
  "The grid/Hessian Newton response is a local diagnostic, not an uncertainty distribution or an exact numerical tolerance. It is not used to convert two failed print intervals into exactmatches.",
  "Source statement that phase alone causes conformation is not independently established; the current task explicitly asks to assess that interpretation and its limits."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_fda8b9b53f8276db.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_fda8b9b53f8276db/verified_computation_reference.md)；SHA-256 `d319add46ddf1d646d64a79e718be9011ee3220fd9ac44efaef267bfdbe4c693`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_fda8b9b53f8276db.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_fda8b9b53f8276db.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_fda8b9b53f8276db.json) | `b81e293e39ea4f0e674bf01a3cf8a54d29fd017c516602ba22d569d66eea2af9` | evidence_or_analysis |
| E0002 | [tasks/v2_autonomous_research/paper_fda8b9b53f8276db/agent_input/task.md](../../../v2_autonomous_research/paper_fda8b9b53f8276db/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_task.md) | `6aa196db02387bbbfb1e96c024f480e2ae6d2d466c7edd0d53b991a4d2f8f724` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_task.md) | `09326d01471e4a0f133f7d1cffa8639bfb93f1ac4e47e309690369e3b04f3fc8` | historical_task_binding |
| E0004 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_ROOT_PRIMARY_SOURCE_READBACK.json) | `a131458d308b52199eb86e1c6e7fc3efefd0cc69c93f52a2a5001ed2c3df60d0` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_ROOT_NATIVE_READBACK.json) | `9f8ce2f290d610c66701f38fed799081fc653cd1cec06332a98de64ed1a3ea31` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/NATIVE_REUSE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/NATIVE_REUSE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_NATIVE_REUSE_READBACK.json) | `2562af751eed8932bcf76180f4a5640c28008988c8ba0f46d3dbb0a4ffee1d2d` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/CURRENT_SCOPE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/CURRENT_SCOPE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_CURRENT_SCOPE_READBACK.json) | `1c97e0e6fab5ded7298f39fdc48330d8f8b9e35a9c8b8e04326835ffa2897bbc` | evidence_or_analysis |
| E0008 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/COMPUTATION_STAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_fda8b9b53f8276db/COMPUTATION_STAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_COMPUTATION_STAGE.json) | `e7fa8bcd0584c186fd6a40d1a845b50880de54ae8de57b945e102a9788d84d81` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_fda8b9b53f8276db.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_fda8b9b53f8276db.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_paper_fda8b9b53f8276db.md) | `d813bcdc064d83c818e9445aba5b0f283b13ca3b51e7be7f9d5170948bd846d5` | evidence_or_analysis |
| E0010 | [docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `1bb893c2c762f7da9f2fe025e9f08eb0ed52eb4474fd748087c4a6e2e7d826fa` | historical_task_binding |
| E0011 | [docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `f216006f29eb90fbf9312082dbb0d97e050359c38202d3b52fa384349ae3042c` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_task.md) | `6aa196db02387bbbfb1e96c024f480e2ae6d2d466c7edd0d53b991a4d2f8f724` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_reference_key_points.json) | `d50f33632cacecb4050725e5f608366ecdbcb38d53acb526e8dfb2a75c63caf3` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_reference_conclusions.json) | `4df04a63dc8404466c40b0e7119f1a61dfc47608d2029e85d6df0639b4297faf` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_package_manifest.json) | `68acdb0e05e69e9e5540f0bc900fadbaaf312e21b483e0633f8e742e103c5796` | historical_task_binding |
| E0016 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_task.md) | `09326d01471e4a0f133f7d1cffa8639bfb93f1ac4e47e309690369e3b04f3fc8` | historical_task_binding |
| E0017 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_reference_key_points.json) | `d50f33632cacecb4050725e5f608366ecdbcb38d53acb526e8dfb2a75c63caf3` | historical_task_binding |
| E0018 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_reference_conclusions.json) | `4df04a63dc8404466c40b0e7119f1a61dfc47608d2029e85d6df0639b4297faf` | historical_task_binding |
| E0019 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_package_manifest.json) | `4528d91e2fa01d995e4cc4064a23a2eb0b74a956aab7d551746246a074517ad0` | historical_task_binding |
| E0020 | [papers/paper_fda8b9b53f8276db/documents/main.pdf](../../../../papers/paper_fda8b9b53f8276db/documents/main.pdf) | `0afa69242ab928c082802d029d66eaa4c3c58cea7f791438d64de1c7f88de8d1` | source_document |
| E0021 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_fda8b9b53f8276db/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_fda8b9b53f8276db/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_main.json) | `f495974b735bf0186e11279a57e92ae243495fbfb307e190f5798b53c4071279` | evidence_or_analysis |
| E0022 | [papers/paper_fda8b9b53f8276db/documents/supplementary_001.pdf](../../../../papers/paper_fda8b9b53f8276db/documents/supplementary_001.pdf) | `13ace6b2daec90e737a69c21f21a4af2d7cab7a54b967859e270ca1147c496de` | source_document |
| E0023 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_fda8b9b53f8276db/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_fda8b9b53f8276db/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_supplementary_001.json) | `4443b00fd5ca52f394957bd5a8ab1f572e6cd1f3ae777ba53d8b157eaee251f6` | evidence_or_analysis |
| E0024 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/native_reuse_verification.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_native_reuse_verification.json) | `ad0de39bb0551c04c87280d02fac21890b36d28fcc293f555350217bc6285fea` | evidence_or_analysis |
| E0025 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_native_excerpt.json) | `0d6e46df42cfefbe413525ee3f465ae300b69cde02256e84e89d60be668da778` | native_output |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_input.com) | `81e15d05bbb94753b652d7875864a77d72c762b5c1e37f9c2aba7cc3aeb61908` | input_or_analysis_code |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_native_excerpt.json) | `3a0a9c1703dd535e0ed0ab50842c5b05419ced062e21de0b34e446916dfa67ed` | native_output |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_input.com) | `591bf9bf9283469dad3ff9fb35602bc33bad31ce72b4f29d3b9fc073da50545c` | input_or_analysis_code |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/20261003T0339Z_paper_fda8b9b53f8276db/paper_fda8b9b53f8276db.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/20261003T0339Z_paper_fda8b9b53f8276db/paper_fda8b9b53f8276db.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_paper_fda8b9b53f8276db.json) | `3e9b9603cb59d6287adee6bdd475b2b1260f6e3684273f637333e4fc46252660` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group3/review_packets/paper_fda8b9b53f8276db.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group3/review_packets/paper_fda8b9b53f8276db.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_paper_fda8b9b53f8276db.json) | `a3dd01db77c87847e11f8771d0050fb6fac244efc909e320151a24549083379f` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_20261003T0326Z/LIGAND_REVIEW_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_20261003T0326Z/LIGAND_REVIEW_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_LIGAND_REVIEW_READBACK.json) | `dcf5e9531c6c63e3511769448200c57b1e308d2a523ca53dd893b89a35b4b4fd` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_RESULT.json) | `ec2ff342afab0a246ef91bad0aba4801a126f97777e624943f44b94563a79bc2` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_ligand_S2_angles_S3_mapping_archive_strict_a1_verification.json) | `73c2409dc41eb0a0aac54174584bad155a0e71578dc1c041857c724790343e3d` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_RESULT.json) | `1ecd5aaa45ba8f9c1f8755e42d970cd023bfa53d97c02e9b4a83a0ca12a78505` | evidence_or_analysis |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_run_status.json) | `8fe8c5557cdda17e13c0f4336b65bc672ac48a4d00ad28a74bb88e3129dd3a7a` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_S3_parity_grid_diagnosis_strict_a1_verification.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_ligand_S3_parity_grid_diagnosis_strict_a1_verification.json) | `463da3ce8932f06a21d5d84f60e5dd15356a9683c5c4cfba04c2980502eda859` | evidence_or_analysis |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_RESULT.json) | `7d0998ec9ba1b3c175d40b46c8a67638c436525967b08ff40f71f8921bc33ebd` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_run_status.json) | `f4060ed105773454d456baffffff8f5c63cb07b12eea213b44519604724deea6` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_source_derivative_readback_strict_a1_verification.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_ligand_source_derivative_readback_strict_a1_verification.json) | `33ae01f308ac06df8ba58aee0b2e44e1b7835a137d533b6def42ea6547a38767` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_run_status.json) | `52fdb2d349adb5f9fa75afba3f252be6a15baef1ce70fd1cdf99c8e0ecd502fa` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/final_ligand_scalar_readback_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/final_ligand_scalar_readback_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_final_ligand_scalar_readback_20260930.json) | `a421848bdc9769c7d65d09aa3c7d30dad72fdfe4150a99fa390c53b178e52648` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/CIF_field_conflict_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/CIF_field_conflict_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_CIF_field_conflict_20260930.json) | `b0014c4cf7298a375548e9bb609c487c5d39af5d9600de98214616856fe1a447` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_run_status.json) | `87feae3b8ffd10cb47dcd41eb6b3aae6a5486eab65191daf81585dc101adaf02` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.chk) | `d02111122963958f895b795e7773bf94008ffa6c511878c6cdf6e85fb090821c` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.fchk) | `7a264fa1dc706b12bf7a0bdb6e0e79e02fca787179c94d01f53f4cb9f83eac44` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_run_status.json) | `71128fbbcfaeec7802e485f8ed8f23ca0affe38d660a7e7bc91b3fdd60ddea8c` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.chk) | `25ea6e283f7eebb3653f9601fd947ea0a23b7c085c244590e936716d2f232ebc` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/calculation.fchk) | `4b0a52f8426108136237aebbdce97b12bcbc841c16c0a500e07370856f1e5f60` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_native_excerpt.json) | `ccb5ec05c94094cd61c687d35adf078e2bfb1f72299ba2197ef7dd33786e59f1` | native_output |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_input.com) | `1518241cea1d0596d378fa529c6ff356bb619fdfe18316d46ce681c53a0f5de5` | input_or_analysis_code |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_run_status.json) | `d41aac131f1a6ca422224d9571132819dc3a27e5c910fa44a31841912d154ee1` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_native_excerpt.json) | `84140a0c00a38cfd8961d189a08274c8c87e99e47e30761713873469e35a046b` | native_output |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_input.com) | `d0826fdf341bd0bfa6cf4f0a699bd57a83b0e3635484ddefa896213ab6311ca1` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_run_status.json) | `e254700be706bf265339ae61b966ac6aae04bf6150a6b175408396ecaef4ea20` | evidence_or_analysis |
| E0055 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/data/inputs/ccdc_2433822.cif](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/data/inputs/ccdc_2433822.cif)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_ccdc_2433822.cif) | `a293d9f910e0831b14dbf92baf50f1f8601c36eabcef7b5fd9c5beb541c51fa3` | input_or_analysis_code |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_fda8b9b53f8276db/paper_reproduction/agent_input/data/inputs/objects.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_fda8b9b53f8276db/paper_reproduction/agent_input/data/inputs/objects.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_objects.json) | `70956be6f015040e4ae6aa60c2b32a8b2f28ed4844b77764953d8e22da2ac54c` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_fda8b9b53f8276db/paper_reproduction/agent_input/data/inputs/experimental_bonds.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_fda8b9b53f8276db/paper_reproduction/agent_input/data/inputs/experimental_bonds.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_experimental_bonds.json) | `d03603b4966ac915003db75b747afe579c842c2e81f3c2ae0cbd251e1009559c` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_fda8b9b53f8276db/paper_reproduction/agent_input/data/inputs/crystal_provenance.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_fda8b9b53f8276db/paper_reproduction/agent_input/data/inputs/crystal_provenance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_crystal_provenance.json) | `01b740b64bcccdf9f1f8598126ee04796318991c9e96d7ee8e59f531d121b4d7` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/verify_ligand.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/verify_ligand.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_verify_ligand.py) | `d58f0a556d25a38d3c8ba22cf99282ebf051236f773b4fb32a66836722a16f5d` | input_or_analysis_code |
| E0060 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/task_info.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_task_info.json) | `cb421c89467b862adcce6c80b1db65f1f302dcaad59632c62129c153888fcdde` | historical_task_binding |
| E0061 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_submission_schema.json) | `9be4a855489a4c5ae60d901e254d3b047d084ad6ad589b456ce4b6dcd757c5d3` | historical_task_binding |
| E0062 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_submission_guide.md) | `b453a51b7ad6511579e7282b36eb5cc1bb46eaec00c285a6c5134d44b91a29ef` | historical_task_binding |
| E0063 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_scoring_rules.json) | `6d9b4444c27908061749bdbb7bc887160eb22e2d80a99a27bedb2b28102c674c` | historical_task_binding |
| E0064 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_evidence_map.json) | `2d7fc463c1f8f3f1b662dcecf6f13b91719b4133bb250a08e75fd36897684895` | historical_task_binding |
| E0065 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_critical_failures.json) | `f57e2a2b354bc31ae2e60a41b3b89b138fc1128378797f404963aa433fc85d18` | historical_task_binding |
| E0066 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_reference_validation_plan.md) | `a065223a653f7ae463ffb69a3ed6b63728d0645bdf66070a0b6e852ce435bb8e` | historical_task_binding |
| E0067 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/paper_route.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_fda8b9b53f8276db/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_paper_route.md) | `4e594c087a1d6952b8049d80631ec3d98da4590a5db24c193344a88056c171f3` | historical_task_binding |
| E0068 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/task_info.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_task_info.json) | `ef642fb0bc48e3f1d14f1fded24e8e00bf7d3b6e476efc5acd3ac2aed7cc7c72` | historical_task_binding |
| E0069 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_submission_schema.json) | `9be4a855489a4c5ae60d901e254d3b047d084ad6ad589b456ce4b6dcd757c5d3` | historical_task_binding |
| E0070 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_submission_guide.md) | `b453a51b7ad6511579e7282b36eb5cc1bb46eaec00c285a6c5134d44b91a29ef` | historical_task_binding |
| E0071 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_scoring_rules.json) | `6d9b4444c27908061749bdbb7bc887160eb22e2d80a99a27bedb2b28102c674c` | historical_task_binding |
| E0072 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_evidence_map.json) | `2d7fc463c1f8f3f1b662dcecf6f13b91719b4133bb250a08e75fd36897684895` | historical_task_binding |
| E0073 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_critical_failures.json) | `f57e2a2b354bc31ae2e60a41b3b89b138fc1128378797f404963aa433fc85d18` | historical_task_binding |
| E0074 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_reference_validation_plan.md) | `a065223a653f7ae463ffb69a3ed6b63728d0645bdf66070a0b6e852ce435bb8e` | historical_task_binding |
| E0075 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/paper_route.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_fda8b9b53f8276db/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_paper_route.md) | `4e594c087a1d6952b8049d80631ec3d98da4590a5db24c193344a88056c171f3` | historical_task_binding |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1_design.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1_design.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_ligand_exact_S3_FineFreq_UltraFineForce_strict_a1_design.json) | `6f2294ad422d44e4c40746a7f7b3e206321ed4c4a3f6a4ad1bc2842637cfcd9d` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_native_excerpt.json) | `df7e0c44d0f5563945767009e85db480c3ca0da8d19bc74cc4975decbc169de7` | native_output |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_run_status.json) | `01090cf0c363304386ab38b59a1a8608f90905a7bc8e3a062426ffde10de37c9` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/sourceFine.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/sourceFine.fchk) | `9eac9d5a0e3de6cf98b34c6d7d92365037a259ddb4230f5609e36346850822da` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_exact_S3_FineFreq_UltraFineForce_strict_a1/calculation.fchk) | `dee87d9d1ac31f10d424b3802637d0a1df3a33b5983a221af8e1ff5434925156` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/calculation.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/calculation.chk) | `59b9d9c2c9967fc8a53dbef81d26d93a4145d0afa03b1864c5d5e630a233bfed` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/calculation.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/calculation.chk) | `d436d7892945b1d77435d0f0ab7aa6bc3ad5e57e906394ca6c9dd62012512251` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_native_excerpt.json) | `47f5fa39edee39be95f5692f1e1570d3d93a3967ba448c25ee37811c95c78904` | native_output |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_run_status.json) | `c7516cc7a6a0d74f5ebb4e2bd0646804362bf7b6d96581e3483b59e763b9792c` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_native_excerpt.json) | `e51c3dfc2d5993803d8820edf122640daff1dd1903966eda6191e3392a1b0269` | native_output |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/run_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/run_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_run_status.json) | `edcdfdc5a412d84c831cebe1a9a807f4cf2b84d5471e89c4f7b508d48302061e` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/atom_map.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/analysis/atom_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_atom_map.json) | `6e57cefbfdb14ed6d5367c2f055d49a2a0a117d80ea88bbc11fd414788c1fbc4` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/inputs/ligand_S2_angles_S3_mapping_archive_strict_a1/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/inputs/ligand_S2_angles_S3_mapping_archive_strict_a1/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0098_analysis.py) | `9e44c01e749bd8f9dd2db1f5495420efef917cca0a346e61964f31317341516d` | input_or_analysis_code |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1.fchk) | `5e19038d2efb70faa50e89e8fad3ef3275e80d9abf7ec31fa3d7f077d3ce7d6e` | evidence_or_analysis |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_native_excerpt.json) | `ab486ec245d4280e5568b5f19e77d1e86ba934f12bc379e3c138b4764a930115` | native_output |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1.chk) | `59b9d9c2c9967fc8a53dbef81d26d93a4145d0afa03b1864c5d5e630a233bfed` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_native_excerpt.json) | `97ca41510c2702243661e37472191d335c2820972bd6ff62f47d244d1a75fe60` | native_output |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1.chk) | `d436d7892945b1d77435d0f0ab7aa6bc3ad5e57e906394ca6c9dd62012512251` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/cis_MeCN_B3LYP_6311p2dp_optfreq_a1_formchk.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_native_excerpt.json) | `e00082b272a8cbeb192413b4f0150260a2a72ea1f79822fdf166fa3e736b97ba` | native_output |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S2_angles_S3_mapping_archive_strict_a1/trans_MeCN_B3LYP_6311p2dp_optfreq_a1.fchk) | `bc39166de28a3bab92e476426dc453cd9dd701fb13c64f7203eb8d08b924633f` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/inputs/ligand_S3_parity_grid_diagnosis_strict_a1/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/inputs/ligand_S3_parity_grid_diagnosis_strict_a1/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_analysis.py) | `13cef4890066cbd07fa6e66933640c03f74c8c74b3117067b5f4f3d23698b4d3` | input_or_analysis_code |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_native_excerpt.json) | `b541d4148d2bf0c8aaeebd2dd570f38246a4b4e62f2b41d7b603b87098b9b0f5` | native_output |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_S3_parity_grid_diagnosis_strict_a1/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/inputs/ligand_source_derivative_readback_strict_a1/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/inputs/ligand_source_derivative_readback_strict_a1/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_analysis.py) | `dbfa55bc13ba784066d699d867e5abd8dd4119e2fec70e48c4f0208622cfe154` | input_or_analysis_code |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0111_native_excerpt.json) | `4455bfbb26fcfdc46c2c04d740791ab7e252e485133d0779aaaf9c49b9bf4f36` | native_output |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_fda8b9b53f8276db/outputs/ligand_source_derivative_readback_strict_a1/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/recheck_ligand_scalars_final_20260930.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/recheck_ligand_scalars_final_20260930.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_recheck_ligand_scalars_final_20260930.py) | `ee31d61dcfba4a8bb14a4dc16d955d275e26cf0217c96427367208e7d4e711ec` | input_or_analysis_code |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/cis_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_input.com) | `81e15d05bbb94753b652d7875864a77d72c762b5c1e37f9c2aba7cc3aeb61908` | input_or_analysis_code |
| E0115 | [.software_cache/installations/gaussian/g16/install/g16/g16](../../../../.software_cache/installations/gaussian/g16/install/g16/g16) | `384f3baca38297d3f11ed2168bb9be836778fa4c5f5d07cb38751e3ed1a66db5` | evidence_or_analysis |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/trans_gas_B3LYP_6311p2dp_strict_optfreq_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0116_input.com) | `591bf9bf9283469dad3ff9fb35602bc33bad31ce72b4f29d3b9fc073da50545c` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/cis_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0117_input.com) | `1518241cea1d0596d378fa529c6ff356bb619fdfe18316d46ce681c53a0f5de5` | input_or_analysis_code |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/inputs/trans_MeCN_B3LYP_6311p2dp_optfreq_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0118_input.com) | `d0826fdf341bd0bfa6cf4f0a699bd57a83b0e3635484ddefa896213ab6311ca1` | input_or_analysis_code |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/cis_gas_SuperFineGrid_sensitivity_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0119_input.com) | `3d5cbbc60ab6f7ccbc729ef50cadbc310a802dc1fe874f7cea4d6ba6ae612f96` | input_or_analysis_code |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_fda8b9b53f8276db/outputs/trans_gas_SuperFineGrid_sensitivity_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_fda8b9b53f8276db/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0120_input.com) | `4bdb32173639918d1956739fae144195642649f1e02bba521d199e974b54d986` | input_or_analysis_code |
| N0111 | [tasks/v2_autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_key_points.json) | `d50f33632cacecb4050725e5f608366ecdbcb38d53acb526e8dfb2a75c63caf3` | latest_review_evidence |
| N0112 | [tasks/v2_autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json) | `4df04a63dc8404466c40b0e7119f1a61dfc47608d2029e85d6df0639b4297faf` | latest_review_evidence |
| N0113 | [tasks/v2_autonomous_research/paper_fda8b9b53f8276db/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_fda8b9b53f8276db/evaluation/scoring_rules.json) | `6d9b4444c27908061749bdbb7bc887160eb22e2d80a99a27bedb2b28102c674c` | latest_review_evidence |
| N0114 | [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_key_points.json](reference_key_points.json) | `d50f33632cacecb4050725e5f608366ecdbcb38d53acb526e8dfb2a75c63caf3` | latest_review_evidence |
| N0115 | [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json](reference_conclusions.json) | `4df04a63dc8404466c40b0e7119f1a61dfc47608d2029e85d6df0639b4297faf` | latest_review_evidence |
| N0116 | [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/scoring_rules.json](scoring_rules.json) | `6d9b4444c27908061749bdbb7bc887160eb22e2d80a99a27bedb2b28102c674c` | latest_review_evidence |
| N0117 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0118 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/agent_input/task.md](../agent_input/task.md) | `09326d01471e4a0f133f7d1cffa8639bfb93f1ac4e47e309690369e3b04f3fc8` |
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_key_points.json](reference_key_points.json) | `d50f33632cacecb4050725e5f608366ecdbcb38d53acb526e8dfb2a75c63caf3` |
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_conclusions.json](reference_conclusions.json) | `4df04a63dc8404466c40b0e7119f1a61dfc47608d2029e85d6df0639b4297faf` |
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/scoring_rules.json](scoring_rules.json) | `6d9b4444c27908061749bdbb7bc887160eb22e2d80a99a27bedb2b28102c674c` |
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/critical_failures.json](critical_failures.json) | `f57e2a2b354bc31ae2e60a41b3b89b138fc1128378797f404963aa433fc85d18` |
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/evidence_map.json](evidence_map.json) | `2d7fc463c1f8f3f1b662dcecf6f13b91719b4133bb250a08e75fd36897684895` |
| [tasks/v2_paper_reproduction/paper_fda8b9b53f8276db/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `e1053b9df8aedb844447645b29de63ed38c93baa82e454fc2c0ca505c9f868f9` |

## Current scoring migration — 2026-10-19
Active paper_science_v2: 100 binary scientific-result points, intermediate findings plus final conclusions. Historical weights/freezes are superseded only as scoring policy. No process score or multiplier. No new chemical calculation or validation. Acceptance: PASS_STRICT_CURRENT_FROZEN_SCOPE. CIF legacy formula and source angle/label conflicts remain disclosed. Crystal ESD is not a universal DFT tolerance. Both computed cis and trans are local gas-phase basins; verification trans lies lower, so no global cis winner is claimed. No lattice free energy, crystal population, exclusive lattice causality, Re-complex or biological conclusion follows.


## 2026-10-19 — Round 3 scoring-contract repair (not a chemical acceptance update)

The original verification history above remains verbatim. Current scoring uses the physical object/state/reference definitions in scoring_rules.json; author software and previous user acceptance are evaluator provenance, not facts a new agent must report. Numeric targets, tolerances, recorded residuals, reference acceptance status and scientific scope are unchanged. PR still addresses the disclosed baseline. Relevant final-claim evidence is assessed directly rather than requiring every intermediate numeric window or an unrelated branch to pass.

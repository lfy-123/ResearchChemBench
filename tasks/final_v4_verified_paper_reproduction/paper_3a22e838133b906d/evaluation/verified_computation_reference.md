# 2026-10-28 V3 final-results scope and evidence reuse

Retain the local structural explanation of neutral Cy/OEt 2a and its deethylated anion/salt. AR has three structural-response conclusions plus electronic-origin and crystal-applicability conclusions (5 rules). PR preserves five existing methyl-model length windows plus the same two explanations (7 rules). This documented pre-existing numeric-baseline difference is not silently imposed on AR. No dealkylation kinetics or mandatory dimer study is added.

r_bo_contraction/r_bound_po_elongation/r_dealkylated_po_localization and the five PR length rules reuse native-linked E0035 values: neutral B–O/P–O 1.695595912/1.516778733 Å; anion B–O/bound P–O/dealkylated P–O 1.579131666/1.558034117/1.485185525 Å. r_intrinsic_local_reorganization reuses E0037 mapped Mulliken values (newly dealkylated O -0.388194 to -0.667027 e; B 0.459462 to 0.421207 e; P 1.098982 to 1.266521 e), paired geometries and E0001 reviewed full/Li controls. r_crystal_environment_distinction uses model differences -0.116464246/+0.041255384 Å versus measured -0.042/+0.012 Å; its finite-model attribution remains bounded. Every PR ±0.010 Å hard window is unchanged.

Evidence gaps / limits: No native crystal dimer or solution aggregation validation; outside this task scope; Relaxed anion P charge 1.266521 e differs from printed 1.266 e by 0.000521 e; source-geometry control gives 1.265960 e. These charges are explanatory evidence, not numeric score targets; AR and PR retain their pre-existing applicability difference: PR has five source-methyl hard windows; unifying these would change scope and requires parent review

This edit performs no new calculation or scientific revalidation. Only scoring_rules.json defines current scoring. All historical text below is preserved verbatim; its PASS labels and earlier scoring policies are historical, not a new full V3 pass.

---

# V2 验证计算参考：磷酸酯–硼烷去烷基化

论文：`paper_3a22e838133b906d`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：局部去烷基化B–O缩短/P–O重组及其解释得到作者路线复现。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

作者模型及完整/Li控制下的B/O/P结构重组和晶体解释边界。

冻结题面中的科学目标：

What molecular account of the local B/O/P structural differences between phosphonate–borane2a and its dealkylated lithium salt is supported by the crystallographic observations and a defensible model investigation? Determine what can be attributed within the studied models and where experimental environment or model representation limits the conclusion.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

Main Scheme1/Fig1 reports LiI dealkylation of2a under reflux, isolation of[Li(MeCN)2][3], and a crystal dimer with a Li2O2 core. The authors observe a shorter B···O contact and slightly longer associated P–O bond in the salt. Scheme2 and SI p78 use small models with R/R′=Me, Gaussian16 C.01 B3LYP-D3(BJ)/6-311++G(2d,p), optimization and no imaginary frequencies. They explicitly note that the anion calculation omits Li coordination and fits experimental P–O distances less well. Reproduce the disclosed model baseline with transparent truncation and justified substitutions; additional full-molecule, environment or association studies are new investigations. The previous benchmark’s full coordination ladder, balanced reaction cycle and mandatory dimerization panel were not performed as that complete protocol in the paper. No source CIF or effective dimer minimum has been manufactured for this package.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_3a22e838133b906d/documents/main.pdf](../../../../papers/paper_3a22e838133b906d/documents/main.pdf) | `0b3a6429a4f8d324616b78c736daedf397971e63fdeff848f1b28058a39a1238` |
| [papers/paper_3a22e838133b906d/documents/supplementary_001.pdf](../../../../papers/paper_3a22e838133b906d/documents/supplementary_001.pdf) | `0179f85740483c73a9996ca3c5ef36fd4f0044eca862b18eadc90e03463a7235` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Gaussian16 C.01 B3LYP-D3BJ/6-311++G(2d,p)甲基中性/阴离子作者模型，真实完整取代和Li控制。

1. 从 SI 确认作者甲基截断的中性/去烷基化阴离子及 B/O/P 映射；将其与实验晶体、完整取代基和含 Li 环境区别，保持电荷及去烷基化计量。

2. 按 Gaussian16 C.01 B3LYP-D3BJ/6-311++G(2d,p) 核收五个甲基中性/阴离子、完整及 Li 对照模型的 Opt/Freq，正模数为 75/87/162/183/165。不得把离子对和自由阴离子混作同一参照。

3. 从真实端点提取 B–O、结合 O 的 P–O 与另一 P–O：中性 1.695596/1.516779 Å，阴离子 1.579132/1.558034/1.485186 Å；按相同原子映射与源几何比较。

4. 在源阴离子坐标及松弛结构上实际计算同人口定义的 P 电荷，分别 1.265960/1.266521 e，对源 1.266 e；源坐标/松弛的差异单列，结合完整取代基和 Li 作用检查截断模型解释范围。

5. 将局部 B/O/P 重组与电子变化作为支持；气相有限模型不等于晶体环境，晶体 ESD 也不被当作 DFT 误差阈值。完整模型与 Li 对照用于限定而非消除该边界。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| 中性B–O/P–O,Å | [1.696,1.517] | [1.695595912,1.516778733] | 实算−论文：[-0.000404088,-0.000221267]； 均在正文三位小数打印区间，保持同原子映射。；源定位：main Scheme2 |
| 阴离子B–O/P–O/另一P–O,Å | [1.579,1.558,1.485] | [1.579131666,1.558034117,1.485185525] | 实算−论文：[0.000131666,3.4117e-05,0.000185525]； 同作者模型五项结构重现。；源定位：main Scheme2 |
| 阴离子Mulliken P,e | 1.266 | {"source_geom":1.26596,"relaxed":1.266521} | 实算−论文：{"source_geom":-4e-05,"relaxed":0.000521}； 源几何值吻合，松弛差由真实几何控制检验；不把Mulliken说成NPA/Hirshfeld。；源定位：SI S81 |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Neutral B–O / P–O (Å) | [1.696106,1.51678] | [1.695596,1.516779] | Source SI methyl geometry versus native same-method methyl neutral minimum. Residuals ≤0.000510 Å are small relative to the 0.117 Å source B–O and 0.041 Å P–O dealkylation responses; source-coordinate versus relaxed comparisons identify the same model and basin. |
| Anion B–O / bound P–O / other P–O (Å) | [1.579096,1.557922,1.485132] | [1.579132,1.558034,1.485186] | Atom-mapped source and native methyl anion. Local coordinates reproduce the source geometry to approximately 0.0001 Å for this endpoint; no crystal ESD is used as an acceptance threshold. |
| Anion phosphorus charge (e) | 1.266 | {"source_geometry":1.26596,"reoptimized":1.266521} | Same population convention on source-coordinate and relaxed methyl anion. Source-coordinate value rounds to the source number; the explicit geometry control accounts for the 0.000561 e change of the relaxed value. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Check full Cy/OEt identities and deethylation bookkeeping, distinguish the B-interacting O atom from other phosphonate oxygens through explicit mapping, and preserve Li/MeCN charge/stoichiometry in whatever models are used. Coordinate and atom labels from different crystal/model files are not automatically equivalent.

冻结要求：Check full Cy/OEt identities and deethylation bookkeeping, distinguish the B-interacting O atom from other phosphonate oxygens through explicit mapping, and preserve Li/MeCN charge/stoichiometry in whatever models are used. Coordinate and atom labels from different crystal/model files are not automatically equivalent. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：甲基截断、完整模型、阴离子/Li离子对正确区分。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Methyl source truncation, full Cy/OEt identity, deethylation bookkeeping, oxygen correspondence and Li charge/stoichiometry are distinguished."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "assessment": "Full Cy/OEt, methyl source model, deethylation, B-interacting O, Li and MeCN identities remain distinct."
  }
]
```

### kp_quantitative_evidence — Check numerical local geometry and any additional electronic/energetic evidence against actual structures, chemically correct atom correspondence and full-versus-truncated identities. Experimental ESDs are measurement uncertainties, not a universal allowed deviation for gas-phase models.

冻结要求：Check numerical local geometry and any additional electronic/energetic evidence against actual structures, chemically correct atom correspondence and full-versus-truncated identities. Experimental ESDs are measurement uncertainties, not a universal allowed deviation for gas-phase models. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：五个模型75/87/162/183/165正频率；本轮读回原生日志，五个源键长与P电荷吻合。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Native B–O/P–O lengths and charge reproduce the source model; measured crystal distances and full-model outputs are separate comparisons."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "assessment": "Source five distances, ten source charges, full-model and Li contrasts are auditable; experimental crystal distances are not a gas-phase numerical tolerance."
  }
]
```

### kp_scientific_answer — Judge whether the submitted study explains or appropriately bounds the observed local changes without requiring a specific decomposition or model ladder. A model can disagree with the source and receive credit when genuine evidence explains its applicability and limits.

冻结要求：Judge whether the submitted study explains or appropriately bounds the observed local changes without requiring a specific decomposition or model ladder. A model can disagree with the source and receive credit when genuine evidence explains its applicability and limits. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：完整取代和Li模型量化气相简化与晶体间差异；与作者Li配位限制一致。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Dealkylation-driven local rearrangement is supported across the model ladder. Mixed Li-pair distance shifts bound a unique environmental explanation."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "assessment": "Model dealkylation reproduces the direction of B–O shortening/P–O lengthening; restoring substituents does not remove crystal-versus-model mismatch."
  }
]
```

### kp_validity_and_uncertainty — Any attribution must be supported by evidence capable of separating the claimed effects, with explicitly defined model/environment and uncertainty. Verify structures to the extent claimed; thermodynamic/association claims require balanced reference states and conventions. An observed crystal dimer does not itself validate a finite optimized dimer or mandate its calculation for a narrower conclusion.

冻结要求：Any attribution must be supported by evidence capable of separating the claimed effects, with explicitly defined model/environment and uncertainty. Verify structures to the extent claimed; thermodynamic/association claims require balanced reference states and conventions. An observed crystal dimer does not itself validate a finite optimized dimer or mandate its calculation for a narrower conclusion. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：晶体ESD没有当作DFT容差；松弛0.000521e差保留。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Actual minima and explicit representation/environment changes are evaluated; crystal ESDs are not applied as universal model tolerances."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "assessment": "Five local minima verified; bounded Li contrast does not establish complete environmental causation or an aggregation equilibrium."
  }
]
```

### kp_bounded_conclusion — Conclusions concern the full experimental identities or explicitly labeled approximations. A methyl-truncated model does not automatically establish the geometry of the full Cy/OEt lithium salt. Finite structures do not prove solution aggregation, reaction kinetics, solubility, electrolyte performance or thermal robustness. A gas-phase model and a crystal are different physical environments.

冻结要求：Conclusions concern the full experimental identities or explicitly labeled approximations. A methyl-truncated model does not automatically establish the geometry of the full Cy/OEt lithium salt. Finite structures do not prove solution aggregation, reaction kinetics, solubility, electrolyte performance or thermal robustness. A gas-phase model and a crystal are different physical environments. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：局部去烷基化B–O缩短/P–O重组及其解释得到作者路线复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "No full Li2O2 crystal-dimer or solution aggregation claim follows from the finite models, and those calculations are not required for this local conclusion."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "assessment": "Finite structures support a local structural account while preserving crystal/environment, conformer and population-analysis limitations."
  }
]
```

### bounded_answer — A source-bounded evidence-supported answer to: What molecular account of the local B/O/P structural differences between phosphonate–borane2a and its dealkylated lithium salt is supported by the crystallographic observations and a defensible model investigation? Determine what can be attributed within the studied models and where experimental environment or model representation limits the conclusion.

冻结要求：Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. Conclusions concern the full experimental identities or explicitly labeled approximations. A methyl-truncated model does not automatically establish the geometry of the full Cy/OEt lithium salt. Finite structures do not prove solution aggregation, reaction kinetics, solubility, electrolyte performance or thermal robustness. A gas-phase model and a crystal are different physical environments.

当前复审：局部去烷基化B–O缩短/P–O重组及其解释得到作者路线复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "The local B/O/P comparison and limits of truncation/environment interpretation are reproduced and evidenced."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "assessment": "The task is fully answered within the current source-bounded scientific question, without a mandatory dimer or association ladder."
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 20.35 小时；5 份计时日志/10 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 8,20 线程/进程；Gaussian %Mem=20GB,80GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0004 · execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log) | Gaussian:1093.7；Gaussian:971.2 | 正常；正常 | {"threads":[8],"Gaussian_mem":["20GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log) | Gaussian:2152.2；Gaussian:1364.6 | 正常；正常 | {"threads":[8],"Gaussian_mem":["20GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · full_anion_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/gaussian.log) | Gaussian:15381.7；Gaussian:4635.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/gaussian.log) | Gaussian:8928.3；Gaussian:10081.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · Li_anion_O6_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/gaussian.log) | Gaussian:23196.7；Gaussian:5469.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

没有把气相甲基模型当完整晶体；源和松弛电荷不逐位一致。

```json
[
  "Crystal B–O 1.666→1.624 Å and P–O 1.513→1.525 Å are not the same environment as the gas-phase methyl values.",
  "Full models give B–O 1.704729→1.581643 Å, P–O 1.508244→1.550408 Å. Li-pair B–O 1.634010 is closer to crystal but P–O 1.564749 is worse; no exclusive Li explanation.",
  "No aggregation, solubility, kinetics, electrolyte or bulk-stability inference."
]
```


原独立审查的 `acceptance_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Applies only to the current hashed AR/PR scientific question and the cited reproduced author baseline.",
  "Does not certify every claim in the paper, an evaluator score, or a blind agent run.",
  "Source inconsistencies and stated model limitations remain disclosed; no task/evaluator/source edits or fitted tolerance were used."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_3a22e838133b906d.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_3a22e838133b906d/verified_computation_reference.md)；SHA-256 `27058b995fd8d63eb5babedf0babf37a0cc9bac91f21c11f065fb4565e312fca`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_3a22e838133b906d.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_3a22e838133b906d.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_3a22e838133b906d.json) | `ba39c0cf0bf44ac0a6146007f73bd6232ae294a3262775c4c2cc1a2a227a817c` | evidence_or_analysis |
| E0002 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_3a22e838133b906d_STRICT_REVIEW_0720Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_3a22e838133b906d_STRICT_REVIEW_0720Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_paper_3a22e838133b906d_STRICT_REVIEW_0720Z.json) | `bac2ed452b1d338d94aba7baed175ff4a70baca5053b3084fa1644f86261c9c7` | evidence_or_analysis |
| E0003 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_3a22e838133b906d_closure_readback_075059Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_3a22e838133b906d_closure_readback_075059Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_paper_3a22e838133b906d_closure_readback_075059Z.json) | `1f3c6ff687c6dbe62dbb809a7769058b269ac33fe1a9ad14a5dcafa17238f0a5` | evidence_or_analysis |
| E0004 | [docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `6eef17edbe3a9c5c180a9fb7bb5d4895391e2b2551a2ff8e1892ea87ab506f41` | native_output |
| E0005 | [docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `97dc91d677012d30d4465ac8701bc60578c001b2f52748db35e2830b0b822c09` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `4414375a96aa958bd90337fce88bd47c7efd0da6a3d96013a656d1f71b0f43ec` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `6aae0dc55714536ad74ec79b58cec53872d1b3285f0aac08a6241d4bbfc22be1` | native_output |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `40ba80da31c6c7569e6efe8b47a1c9bf3ccdda2c5ec042a6691d4f87d9390000` | native_output |
| E0009 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3a22e838133b906d/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3a22e838133b906d/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_main.json) | `4b5a4d4a8ba3503da7993082812e033d261c878be113d62ec88ca431acab4725` | evidence_or_analysis |
| E0010 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3a22e838133b906d/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_3a22e838133b906d/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_supplementary_001.json) | `02ddb654b06a3ee7ce000259bed00d314565ff2fa7ec0f833e1117a42c9cefdf` | evidence_or_analysis |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_task.md) | `16eb55197586668378ece81a7f29e7909622e7b118503b05c1001efdacb7b2a8` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_task.md) | `d372d8fc4f830d636729b06bf24784edc00f41155e73070ef9bcf92552ebd2af` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` | historical_task_binding |
| E0016 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` | historical_task_binding |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_3a22e838133b906d/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_3a22e838133b906d/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_NATIVE_READBACK.json) | `3fc102c9cdce0f24fa93dc404e057c4562c37504c66416304aca39d2dca6349b` | evidence_or_analysis |
| E0018 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_3a22e838133b906d/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_3a22e838133b906d/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_COMPUTATION_COVERAGE.json) | `098752e1a8ad684ca0a3fcb4bd11f53a01408ae7a980d7974f8fd98a201cd50a` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_3a22e838133b906d.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_3a22e838133b906d.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_paper_3a22e838133b906d.md) | `2e18c602d2c2fd40db8d42d52300eb49bb9dfed3026f5a1abefb79c68dd3930c` | evidence_or_analysis |
| E0020 | [docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `0d66d3184d057c5b8854518d01f1b83fb0c6be090aac638a6d3b5c3aaf9c419f` | historical_task_binding |
| E0021 | [docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `2f994e44afa2bc710d60131a292ed89876f26015bef04551e9eea87d34c0e926` | historical_task_binding |
| E0022 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_package_manifest.json) | `f4f41f6eaec161eec58ebeacd4cea467a1394c7f61991d5b3e698d724074b1a3` | historical_task_binding |
| E0023 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_package_manifest.json) | `41878929f96330adee08f7fabed002f728bfdc6bf853bb13e318f4f93ae5182b` | historical_task_binding |
| E0024 | [papers/paper_3a22e838133b906d/documents/main.pdf](../../../../papers/paper_3a22e838133b906d/documents/main.pdf) | `0b3a6429a4f8d324616b78c736daedf397971e63fdeff848f1b28058a39a1238` | source_document |
| E0025 | [papers/paper_3a22e838133b906d/documents/supplementary_001.pdf](../../../../papers/paper_3a22e838133b906d/documents/supplementary_001.pdf) | `0179f85740483c73a9996ca3c5ef36fd4f0044eca862b18eadc90e03463a7235` | source_document |
| E0026 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_sources/paper_3a22e838133b906d/SI_physical81_embedded0_Im60.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_sources/paper_3a22e838133b906d/SI_physical81_embedded0_Im60.png) | `5bdb5fe2c1587756890964647d2b1d3bfafb4109d18b38dbe6a89b21ae1287d8` | evidence_or_analysis |
| E0027 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_sources/paper_3a22e838133b906d/SI_physical81_embedded1_Im61.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_sources/paper_3a22e838133b906d/SI_physical81_embedded1_Im61.png) | `17419c630de77428479d586ceb89b4021a7a87ac7d3c4a8247ed0285315e70b5` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_3a22e838133b906d/native_evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_3a22e838133b906d/native_evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_native_evidence.json) | `1e1edac1a09e738dcfd4ce2291b93f2bf603ae474117b39a07b18c10bb22dbd0` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_3a22e838133b906d_ready_rehash_0730Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_3a22e838133b906d_ready_rehash_0730Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_paper_3a22e838133b906d_ready_rehash_0730Z.json) | `55e80b19b7b52d7375cf5849a5b711057d80a82f1fae35272fcb0471ed3b08ca` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0735Z.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0735Z.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_COORDINATOR_G6_REVIEW_0735Z.md) | `fc923cf78988366469c6f3f74fc09c40af587d01af1460f7066b137f1d4e4e0f` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/paper_3a22e838133b906d_60168713821cdfb210239c8549ab58daf0aec097eaaedd5d1508d5b408f7709b.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/paper_3a22e838133b906d_60168713821cdfb210239c8549ab58daf0aec097eaaedd5d1508d5b408f7709b.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_paper_3a22e838133b906d_60168713821cdfb210239c8549ab58daf0aec097eaaedd5d1508d5b408f7709b.json) | `60168713821cdfb210239c8549ab58daf0aec097eaaedd5d1508d5b408f7709b` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_3a22e838133b906d/completion_scope_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_3a22e838133b906d/completion_scope_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_completion_scope_review_20260930.json) | `32dd09e57f57bec225b86066fd846881b52d59b2f3f699f93e1b0e40506e304d` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_analysis.py) | `680849a340329ff214c814ca7b6aa1eb61d6e681bf9e13c11454345d82d92484` | input_or_analysis_code |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_case.json) | `1e57304fae37d7235bf5dbc2142796adc6ad3126f738692b0f56d80848ce5005` | evidence_or_analysis |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/paper_3a22e838133b906d.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/paper_3a22e838133b906d.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_paper_3a22e838133b906d.json) | `544fae90fb33cea86c3b70a262b34486495969d8e5abf8f363cab29f82ac5304` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/source_comparisons.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_e31cc7bc7b21b610/outputs/strict_group6_retained_source_comparison/attempt_01/source_comparisons.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_source_comparisons.json) | `98ba966dc206b654be5fba066b54fd44f69ee6c198f91073499baf056df20e27` | evidence_or_analysis |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/strict_group6_remaining_source_diagnostics/attempt_01/paper_3a22e838133b906d.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/strict_group6_remaining_source_diagnostics/attempt_01/paper_3a22e838133b906d.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_paper_3a22e838133b906d.json) | `a3f88c8f1fa327b4378135ac61c162d87ec29f0384ba3c8625e8de0c9d1460f8` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_3a22e838133b906d/evaluation/reference_key_points.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_3a22e838133b906d/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_3a22e838133b906d/evaluation/reference_conclusions.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/autonomous_research/paper_3a22e838133b906d/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_key_points.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_conclusions.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/contracts/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_FEEDBACK_0710Z.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_FEEDBACK_0710Z.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_COORDINATOR_FEEDBACK_0710Z.md) | `9f3add7c602135b22eaf31046d49ca5786e8cdc44e3f6ef7ecde75c2b5b9e26b` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0715Z.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/COORDINATOR_G6_REVIEW_0715Z.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_COORDINATOR_G6_REVIEW_0715Z.md) | `7abb1962749f444c42f0db1519673c1f70431684be34136ad8e6169ed5dbef3d` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_3a22e838133b906d_COORDINATOR_CLOSURE_0740Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group6/papers/paper_3a22e838133b906d_COORDINATOR_CLOSURE_0740Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_paper_3a22e838133b906d_COORDINATOR_CLOSURE_0740Z.json) | `3400a2183ab3e2cf425fab021ba43751dd07669cf3c94ffd9f9f8760e67d8ff8` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/input.com](../../../../docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_input.com) | `e1281cbfb7429fd467a035345e393f3d5bab437b6b412adc644f75b3886f4ce5` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/input.com](../../../../docs/v2_verification/history/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_input.com) | `6fea0b2418e36c3bde92813eefe14c9b803c3e9568533c13d2473160f82d4b33` | input_or_analysis_code |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_geometry.xyz) | `bea191bbc3afbb2b0a00aa478814ea1629614cae0e8428f3b2e7beaa261872fb` | input_or_analysis_code |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_final_geometry.xyz) | `a82b37529c7ddbc6081a8e3748b4c63524220196c7ba2cf543d503ba092edb2b` | input_or_analysis_code |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_anion_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_input.com) | `617ca1cc3ac094d5ac72885f58b27aa43921aaee58acf7c2093ff99a1bb503b0` | input_or_analysis_code |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_geometry.xyz) | `94f4736d5efc269ee79e4fcc8babadd6c072d37a0251071251c873dae0415afc` | input_or_analysis_code |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_final_geometry.xyz) | `4e97be09021ff16a19ea7d105f0486b2ca909b3cc000fa89bbadb2ca14968f1c` | input_or_analysis_code |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/full_neutral_source_optfreq_platform_resume2_readfc/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_input.com) | `64b397336fa9e366db815eeb00d42138bc587731a08b96f830f97791ab1c873a` | input_or_analysis_code |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_geometry.xyz) | `17f162e83d5d426e78f2cc7d8677d7a322aa98734c87e14bbb9b3a1b254012d1` | input_or_analysis_code |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_3a22e838133b906d/outputs/Li_anion_O6_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_input.com) | `4d080a910e9c44c89083baebe4dc914f35b7f4900177cb012028f559cb2afcfd` | input_or_analysis_code |
| E0059 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/task_info.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_task_info.json) | `b9e56b0170c66d24896058f2b091d8428e11f5f6dee21fb39aa5bb715453924e` | historical_task_binding |
| E0060 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_submission_schema.json) | `2ca76a810824be596ea3e8b12c4a71fed134061945113ffcdf30d77134fd86de` | historical_task_binding |
| E0061 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_submission_guide.md) | `f678c374999c525867b38d95e0bdedda45729603de7e38687b2bebcadf40d87a` | historical_task_binding |
| E0062 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_scoring_rules.json) | `cba67f2242ea13b6401902c86c1f482d13056776c4d3217cac41d780e049b33f` | historical_task_binding |
| E0063 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_evidence_map.json) | `06da4f024d2675bc2afeb3065c09d880f3e12ecfaa94645208855b537bedc684` | historical_task_binding |
| E0064 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_critical_failures.json) | `e91e05629fe1ddb3ce3b54431f46387a685fe9b1f11ba0056cea9a88ebe578db` | historical_task_binding |
| E0065 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_reference_validation_plan.md) | `285c76406f2ecf2b9a4f5e24ca0b5da12bdc4aed5b49f2d20e106caf41a6e881` | historical_task_binding |
| E0066 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/paper_route.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_3a22e838133b906d/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_paper_route.md) | `c00a71f3a9beac3b609a5c95a659dc01226ecd7a6df67cef20f4e986e030a8db` | historical_task_binding |
| E0067 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/task_info.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_task_info.json) | `a8c4a4ca825a8b30c667f5561e556d38a86bab7311a91314fd8652111a617b57` | historical_task_binding |
| E0068 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_submission_schema.json) | `2ca76a810824be596ea3e8b12c4a71fed134061945113ffcdf30d77134fd86de` | historical_task_binding |
| E0069 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_submission_guide.md) | `f678c374999c525867b38d95e0bdedda45729603de7e38687b2bebcadf40d87a` | historical_task_binding |
| E0070 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_scoring_rules.json) | `cba67f2242ea13b6401902c86c1f482d13056776c4d3217cac41d780e049b33f` | historical_task_binding |
| E0071 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_evidence_map.json) | `06da4f024d2675bc2afeb3065c09d880f3e12ecfaa94645208855b537bedc684` | historical_task_binding |
| E0072 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_critical_failures.json) | `e91e05629fe1ddb3ce3b54431f46387a685fe9b1f11ba0056cea9a88ebe578db` | historical_task_binding |
| E0073 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_reference_validation_plan.md) | `285c76406f2ecf2b9a4f5e24ca0b5da12bdc4aed5b49f2d20e106caf41a6e881` | historical_task_binding |
| E0074 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/paper_route.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_3a22e838133b906d/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_3a22e838133b906d/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_paper_route.md) | `c00a71f3a9beac3b609a5c95a659dc01226ecd7a6df67cef20f4e986e030a8db` | historical_task_binding |
| N0074 | [tasks/v2_autonomous_research/paper_3a22e838133b906d/agent_input/task.md](../../../v2_autonomous_research/paper_3a22e838133b906d/agent_input/task.md) | `16eb55197586668378ece81a7f29e7909622e7b118503b05c1001efdacb7b2a8` | latest_review_evidence |
| N0075 | [tasks/v2_autonomous_research/paper_3a22e838133b906d/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_3a22e838133b906d/evaluation/reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` | latest_review_evidence |
| N0076 | [tasks/v2_autonomous_research/paper_3a22e838133b906d/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_3a22e838133b906d/evaluation/reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` | latest_review_evidence |
| N0077 | [tasks/v2_autonomous_research/paper_3a22e838133b906d/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_3a22e838133b906d/evaluation/scoring_rules.json) | `cba67f2242ea13b6401902c86c1f482d13056776c4d3217cac41d780e049b33f` | latest_review_evidence |
| N0078 | [tasks/v2_autonomous_research/paper_3a22e838133b906d/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_3a22e838133b906d/evaluation/reference_validation_plan.md) | `2caf87f96faad0580274475dcc24a9f710681e6157421045f2b0561393ebda75` | latest_review_evidence |
| N0079 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_3a22e838133b906d/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_3a22e838133b906d/verified_computation_reference.md) | `dfbeb84392d73c75359d36bf834268890589f6336eb05628b6402950ad44fe1e` | latest_review_evidence |
| N0080 | [tasks/v2_paper_reproduction/paper_3a22e838133b906d/agent_input/task.md](../agent_input/task.md) | `d372d8fc4f830d636729b06bf24784edc00f41155e73070ef9bcf92552ebd2af` | latest_review_evidence |
| N0081 | [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/reference_key_points.json](reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` | latest_review_evidence |
| N0082 | [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/reference_conclusions.json](reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` | latest_review_evidence |
| N0083 | [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/scoring_rules.json](scoring_rules.json) | `cba67f2242ea13b6401902c86c1f482d13056776c4d3217cac41d780e049b33f` | latest_review_evidence |
| N0084 | [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `2caf87f96faad0580274475dcc24a9f710681e6157421045f2b0561393ebda75` | latest_review_evidence |
| N0085 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_3a22e838133b906d/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_3a22e838133b906d/verified_computation_reference.md) | `27058b995fd8d63eb5babedf0babf37a0cc9bac91f21c11f065fb4565e312fca` | latest_review_evidence |
| N0086 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0087 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/agent_input/task.md](../agent_input/task.md) | `d372d8fc4f830d636729b06bf24784edc00f41155e73070ef9bcf92552ebd2af` |
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/reference_key_points.json](reference_key_points.json) | `3bdbaf6ea9e82a8310ba31dcc962670c6f443cf47860ca842c9d38584f208aab` |
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/reference_conclusions.json](reference_conclusions.json) | `aec783cbfac170a1d93e9b43176ad8cca477895684dfd8decce186d10df1004a` |
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/scoring_rules.json](scoring_rules.json) | `cba67f2242ea13b6401902c86c1f482d13056776c4d3217cac41d780e049b33f` |
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/critical_failures.json](critical_failures.json) | `e91e05629fe1ddb3ce3b54431f46387a685fe9b1f11ba0056cea9a88ebe578db` |
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/evidence_map.json](evidence_map.json) | `06da4f024d2675bc2afeb3065c09d880f3e12ecfaa94645208855b537bedc684` |
| [tasks/v2_paper_reproduction/paper_3a22e838133b906d/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `2caf87f96faad0580274475dcc24a9f710681e6157421045f2b0561393ebda75` |

## Current scientific scoring policy — 2026-10-19

Active scoring is paper_science_v2: independent binary intermediate findings and final conclusions total 100. The synchronized JSON files replace historical process weights, partial-credit discretion and obsolete scoring freezes. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE and all recorded residuals/limitations remain; migration performs no new chemical validation. Public input, task_info.json and paper_route.md remain byte-identical. Source-versus-verification quantities are kept distinct; the new tolerances are fixed benchmark criteria, not fitted offsets. Historical reference-stage text above is provenance rather than the current runtime gate.


## Authorized public-contract and scientific-rule repair — 2026-10-19 round3

This repair preserves every preceding historical computation/acceptance statement verbatim. Current scoring remains paper_science_v2,100 independent scientific points. Mode-specific public objects now control AR eligibility; PR retains its disclosed source-baseline targets. Necessary experimental lifetime facts and obsolete process-score prose are repaired in public files where applicable. No source task, original paper, native computation, engine or historical acceptance is changed. Source/verification residuals and uncalibrated method-transfer limits remain; this is not a new chemical validation or online Judge result. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_02/paper_3a22e838133b906d.md.

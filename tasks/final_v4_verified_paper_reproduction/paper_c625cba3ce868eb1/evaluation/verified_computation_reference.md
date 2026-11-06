# 2026-10-28 V3范围与证据复用（group_07）

逐命题复用：R4位点电子比较及PR电荷差/幅比由原生B3LYP/CBSB7 CPCM-water输出和固定密度MK控制支撑；默认Δq(R4/7)=−0.484265/−0.055066 e、比8.794265，加密−0.427513/−0.049492 e、比8.638022。环化解释复用R/E身份与闭环连接关系，适用性结论明确水相单体/真实DCM混合物和多因素比较的界限。不新做计算，不将未收敛67原子扩展算作机理验证。

AR retains (R)-4 as the required object and compound 7 as optional. PR retains its original evaluator/disclosed author baseline comparing R4 and 7, including signed MK contrasts -0.441/-0.049 electron (±0.05 each) and magnitude ratio 9.0 (±1.0); the old public optional-7 sentence is corrected for PR only. Common final dimensions are electronic comparison (30), regioselectivity explanation (45) and experimental/causal applicability (25). AR has one electronic comparison; PR has three numeric outcomes at 12/8/10. Hbond/local-field and six-/seven-ring node scores and duplicate sign/qualitative-comparator scores are removed. All numerical windows are unchanged.

- Source MK fitting grid and exact individual charge digits are not recovered; default and denser fixed-density results are both preserved, not cherry-picked.
- Existing calculations are water monomers, not a converged DCM/NBS/Et3N competing-TS network. The 67-atom extension was not converged and is not evidence of kinetics.
- Original PR public optional-7 wording conflicted with its required comparator/charge/ratio scoring; the disclosed author-baseline requirement is now explicit. AR remains optional-7.
- The source NBS amount/volume and printed concentration disagree (47.3 versus 473 mM), and compound 7 changes both hydroperoxide and scaffold/branching.

以下历史正文原样保留；历史PASS不代表本次V3全面通过。

---

# V2 验证计算参考：氢过氧化物卤环化

论文：`paper_c625cba3ce868eb1`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：源关键极化效应与真实同定义结果相符；拟合敏感性已实际测量，未用任意电荷指标替代或把极化当动力学证明。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

R-4的局部电子极化能解释怎样的卤环化选择性，非酶NBS模型有哪些限度。

冻结题面中的科学目标：

What molecular evidence can explain the observed halocyclization selectivity of hydroperoxide (R)-4, and what remains uncertain when the source nonenzymatic NBS reaction is used as the chemical model?

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors propose that the allylic hydroperoxide polarizes the alkene and affects bromiranium-ion ring closure. They compare4 and hydroperoxide-free7 using MEP maps/MEP-fitted charges and note different enzyme product distributions; these substrates also differ structurally, so the comparison does not isolate every possible cause. Their NBS experiment argues that enzyme participation is unnecessary for the observed profile (main pp3,5–7). Source computations are B3LYP/CBSB7 with C-PCM water in Gaussian16 A.03; minima were checked by frequencies, and MEP/charges used the same level. SI pp30–32 give source optimized minima and charge visualization. Reproduce/audit this molecular baseline or justify substitutions, explicitly separating aqueous monomer calculations from the DCM/NBS chemical model. The source does not supply a validated NBS reaction-path/free-energy network; the old mandatory face/closure/proton-relay matrix was a benchmark extension. Do not turn the source polarization hypothesis into a presumed answer. The NBS procedure on main PDF p7 prints 51 mg, 0.284 mmol and 473 mM in 6 mL CH2Cl2. The stated amount and volume imply about 47.3 mM, a tenfold discrepancy with the printed concentration. Retain both source entries and state which is used in any concentration-dependent model; do not treat the typo as experimentally resolved.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_c625cba3ce868eb1/documents/main.pdf](../../../../papers/paper_c625cba3ce868eb1/documents/main.pdf) | `44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8` |
| [papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf](../../../../papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf) | `19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

作者B3LYP/CBSB7、C-PCM水的R4/7完整模型优化频率和MEP拟合电荷；真实固定密度MK拟合敏感性控制。

1. 按完整 33 原子 (R)-4 和 25 原子 7，核对中性 singlet、R/E 构型、OH/OOH 原子及烯烃位点；用图确认攻击两个位点闭合的六元/七元环，NBS 不被换作裸 Br−。

2. 执行作者 Gaussian B3LYP/CBSB7、CPCM 水相 Opt/Freq，核收 93/69 正模及匹配电子密度的 MK 电荷、带符号 MEP 表面。源精确坐标 SP 与松弛结果分开。

3. 由默认 MK 算 q(C2)−q(C4)=−0.484265、q(C8)−q(C10)=−0.055066 e，对源 −0.441/−0.049；幅度比 8.794265 对源约 9。四个单原子残差完整保留。

4. 在完全相同保存密度上执行预定加密拟合，得到 −0.427513/−0.049492 e、比 8.638022；检验相对极化不是该有限采样选择造成的翻转，不通过挑选最近数字恢复未披露的作者采样。

5. 结论限于作者水相单体的极化解释及其与非酶 NBS 现象的相容性。R4/7 同时改变骨架与支化，水相不等于 DCM/NBS/Et3N 混合物；未收敛的 67 原子 DCM 扩展不算成功路径，局部方向曲率也不等于完整 Hessian 或活化势垒。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Alkene signed MK contrasts R4,7 (e) | [-0.441,-0.049] | [-0.484265,-0.055066] | Default discrepancies −0.043265/−0.006066 e are explicitly retained. Independently preset denser fitting at exactly unchanged density gives −0.427513/−0.049492 e; the strongly asymmetric versus nearly symmetric distinction is quantitative and robust, not simply a charge-sign match. |
| R4/7 contrast-magnitude ratio (dimensionless) | 9.0 | {"default":8.7942650637,"denser_fixed_density":8.6380223066} | Ratio errors 2.3% and 4.0% at two independently defined samplings; consistent with the source approximately ninefold polarization contrast. No universal per-atom tolerance is created. |
| Four source alkene charges R4 C2,C4;7 C8,C10 (e) | [-0.507,-0.066,-0.311,-0.262] | {"default":[-0.533926,-0.049661,-0.313449,-0.258383],"denser_fixed_density":[-0.499762,-0.072249,-0.309513,-0.260021]} | Source sampling is unreported. Native fixed-density variation accounts for most of the observed residual scale; denser-fit residuals are 0.00724,−0.00625,0.00149,0.00198 e. This supports reasonable representation sensitivity for the molecular polarization claim, not printed-digit identity. |
| Valid vibrational minima (cm−1 / count) | Source no imaginary frequencies | {"R4_modes":93,"R4_min_cm1":20.4609,"7_modes":69,"7_min_cm1":36.5594} | Native source-level geometries and unchanged-density controls are the evidence basis; uncomputed reaction paths are not substituted for minima. |

R4/7分别93/69正模；源图碳电荷约-0.507/-0.066与-0.311/-0.262，极化差比约9；原生MK给8.64–8.79。原始正曲率与MK输出已回读。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Correct stereochemistry and reactive inventory

冻结要求：Preserve (R)-4 connectivity, E alkene, alcohol and hydroperoxide identity. Map any proposed bond changes explicitly; ring size follows the actual graph. Use a chemically identified brominating source and balanced proton/electron inventory rather than treating bromide as electrophilic bromine. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists. Atom identifiers are local to the declared object and map_namespace. Evaluate identity, closure topology and reacting atoms after applying an explicit chemically valid bijective remapping; a changed numeric label alone is not a chemical error.

当前复审：身份、两个有效最低点、同定义电荷/MEP、结构混杂与因果边界覆盖；比较支持更强烯烃极化，不声称已建立完整反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical3–4/7; SI30–32",
    "actual_result": "R4:33atom/C10H20O3/q0singlet/map9R/E-C2=C4；OH为O21-H22，OOH为O23-O24-H25。7:25atom/C8H16O/q0singlet/E-C8=C10。优化对应93/69正频率，MK波函数/坐标匹配。O21到C4经18/15/9/6成六元环，到C2成七元环；NBS为中性具名溴源，非裸Br−。",
    "reason": "原子映射、反应物态及官能团以实际图与原生日志核验，环大小是图拓扑陈述而不是已经求得反应路径。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/stdout.log",
        "sha256": "d71119e27d3a76a605068fa318851671bf77b1e2285064ce0970712cf50b33ac"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/stdout.log",
        "sha256": "a70b088f87d09417be7cfac1b04166d1a7d3c4253c08756ff6a4231576931872"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/stdout.log",
        "sha256": "3a8bcc2254938b32e4eb58922164f27af6d46af6bc56165ea7ca9e9455bdb6f6"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/stdout.log",
        "sha256": "13e64fd4d478dec68dfc3227843bc0b6a6d9257f73b94d60721e475e40ca333e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_identity_pair_audit.json",
        "sha256": "89772963a703168fda600c976567a053c988e10961d169192043216a65fe38aa"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_identity_pair_audit.json",
        "sha256": "0f9ff7cf1abed87a549ae1df5be18a57ba5a6f8f741913ee69b8510e7b72cb3b"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/SOURCE_PAGES.json",
        "sha256": "bc5d368e680535a6f0df9dc4449649a1584e1f092ba3de599577c12687e56183"
      }
    ]
  }
]
```


证据记录：`E0021`。

```json
[
  {
    "actual_result": "R4:33atom/C10H20O3/q0singlet/map9R/E-C2=C4；OH为O21-H22，OOH为O23-O24-H25。7:25atom/C8H16O/q0singlet/E-C8=C10。优化对应93/69正频率，MK波函数/坐标匹配。O21到C4经18/15/9/6成六元环，到C2成七元环；NBS为中性具名溴源，非裸Br−。"
  }
]
```

### kp_selectivity — Quantitative explanation of local selectivity

冻结要求：New quantitative evidence must bear on the observed selectivity and distinguish what is established from what is assumed. Do not require a particular intermediate, two alkene faces or named ring-closure matrix if another valid route addresses the question. An MEP asymmetry alone is not a kinetic selectivity proof. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：身份、两个有效最低点、同定义电荷/MEP、结构混杂与因果边界覆盖；比较支持更强烯烃极化，不声称已建立完整反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical3–4/Figure4 physical5; SI30FigureS50",
    "actual_result": "默认R4/7的有符号烯烃电荷差−0.484265/−0.055066e；源−0.441/−0.049；固定密度6为−0.427513/−0.049492。三组均给R4明显更强极化，幅度比约8.64–9。有符号MEP从对应收敛波函数真实生成；MEP表面统计不替代MK原子电荷。",
    "reason": "量化了源提出的反应物电子偏置，可作为NBS选择性的有限解释；不把MEP数值当活化能或断言路径选择。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_single_point.log",
        "sha256": "a70b088f87d09417be7cfac1b04166d1a7d3c4253c08756ff6a4231576931872"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_single_point.log",
        "sha256": "13e64fd4d478dec68dfc3227843bc0b6a6d9257f73b94d60721e475e40ca333e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/analysis_summary.json",
        "sha256": "7c6a3530c395fbec4e20d09880eb93581d87748a38abbeeec322ee0bedd4faac"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/results/Br_author_MK_four_column_and_contrast.json",
        "sha256": "9dd69619864a73e33a7fabc40a81b3e6448a3aa8776acf4d46130c9a4b6d2bce"
      }
    ]
  }
]
```


证据记录：`E0021`。

```json
[
  {
    "actual_result": "默认R4/7的有符号烯烃电荷差−0.484265/−0.055066e；源−0.441/−0.049；固定密度6为−0.427513/−0.049492。三组均给R4明显更强极化，幅度比约8.64–9。有符号MEP从对应收敛波函数真实生成；MEP表面统计不替代MK原子电荷。"
  }
]
```

### kp_causality — Adequacy of the explanatory comparison

冻结要求：Evaluate the claimed causal factor against important model/structural confounding. Comparing4 and7 cannot automatically isolate only hydroperoxide effects; alternative justified tests are eligible. Claimed saddles/pathways require appropriate physical evidence. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：身份、两个有效最低点、同定义电荷/MEP、结构混杂与因果边界覆盖；比较支持更强烯烃极化，不声称已建立完整反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical4 qualifier and physical5 future-work paragraph",
    "actual_result": "R4/7既改变OOH也改变碳骨架支化/立体环境；源提到偕二甲基Thorpe–Ingold仍待研究。两种MK采样使用同一收敛电子密度且差0，极化方向与相对大小保留；只能排除该有限拟合控制造成排序翻转。",
    "reason": "区分已测电子相关与未隔离因果。无需为当前有限解释创造未被作者或当前任务要求的完整竞争TS矩阵。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_identity_pair_audit.json",
        "sha256": "89772963a703168fda600c976567a053c988e10961d169192043216a65fe38aa"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_identity_pair_audit.json",
        "sha256": "0f9ff7cf1abed87a549ae1df5be18a57ba5a6f8f741913ee69b8510e7b72cb3b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/results/MK_fixed_density_fit_controls.json",
        "sha256": "a8b16a400b2eda3a05c5d6a3e278509a7f918242b0a6be885b7a298e5c191b35"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/SOURCE_PAGES.json",
        "sha256": "bc5d368e680535a6f0df9dc4449649a1584e1f092ba3de599577c12687e56183"
      }
    ]
  }
]
```


证据记录：`E0021`。

```json
[
  {
    "actual_result": "R4/7既改变OOH也改变碳骨架支化/立体环境；源提到偕二甲基Thorpe–Ingold仍待研究。两种MK采样使用同一收敛电子密度且差0，极化方向与相对大小保留；只能排除该有限拟合控制造成排序翻转。"
  }
]
```

### kp_uncertainty — States, references and uncertainty

冻结要求：Use consistent stoichiometry, solvent/temperature/standard-state assumptions and evidence-based uncertainty for the claimed effect. Source room-temperature/unspecified aspects must be stated rather than given invented precision. Do not confuse aqueous MEP with a DCM free-energy path. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists. For concentration-dependent claims, address the source inconsistency between 0.284 mmol NBS in 6 mL (about 47.3 mM by amount/volume) and the printed 473 mM. Preserve the source ambiguity rather than inventing a confirmed concentration.

当前复审：身份、两个有效最低点、同定义电荷/MEP、结构混杂与因果边界覆盖；比较支持更强烯烃极化，不声称已建立完整反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical7/9; SI30–32",
    "actual_result": "同定义列出源、精确SI旧SP、优化后默认和固定加密MK，所有单原子差异保留。当前C.01替代源A.03（文献又写A.02）不声称二进制相同。水相单体/一构象不等于DCM/NBS/Et3N混合物；473mM与0.284mmol/6mL=47.3mM冲突明确；没有浓度依赖速率结论。",
    "reason": "既有MK验收是同一方法下方向/相对差别，未构造新的电荷容差。实际采样变化用于稳健性检查，非渐近误差界。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/AUTHOR_MK_SOURCE_REVIEW_20261007.json",
        "sha256": "907a73b4806332aa3b0da76eee896399b2c1cae82c9228f9858f0e9d0ca312f8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/analysis_summary.json",
        "sha256": "7c6a3530c395fbec4e20d09880eb93581d87748a38abbeeec322ee0bedd4faac"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/SOURCE_PAGES.json",
        "sha256": "bc5d368e680535a6f0df9dc4449649a1584e1f092ba3de599577c12687e56183"
      }
    ]
  }
]
```


证据记录：`E0021`。

```json
[
  {
    "actual_result": "同定义列出源、精确SI旧SP、优化后默认和固定加密MK，所有单原子差异保留。当前C.01替代源A.03（文献又写A.02）不声称二进制相同。水相单体/一构象不等于DCM/NBS/Et3N混合物；473mM与0.284mmol/6mL=47.3mM冲突明确；没有浓度依赖速率结论。"
  }
]
```

### kp_scope — Evidence-proportional experimental interpretation

冻结要求：Accept supported, revised or well-investigated unresolved explanations. Distinguish the selected (R)-4 model from the mixed-substrate NBS experiment and the enzyme context; no claim of enzyme control or full cascade yield from a local model. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：身份、两个有效最低点、同定义电荷/MEP、结构混杂与因果边界覆盖；比较支持更强烯烃极化，不声称已建立完整反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical3–5/7; currentV2AR/PRtask",
    "actual_result": "NBS对照产生相似谱形表明该观察无需酶也可出现；选定R4不代表3/4混合物整体或生物级联。额外67atomDCM点5保持未收敛；新4Force方向曲率为正且两步长一致，但不是完整Hessian或通路证明，未据此授路径通过。",
    "reason": "额外路径失败如实保留；当前核心结论不依赖该自选路径，因此不把它再列为所有作者基线的必需后继。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/SOURCE_PAGES.json",
        "sha256": "bc5d368e680535a6f0df9dc4449649a1584e1f092ba3de599577c12687e56183"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/RETURNED_CURVATURE_NATIVE_INTAKE.json",
        "sha256": "b6b34f2915977f264b8d279a22c8fc1bee6deb70b9c97e586d921abd08483a6a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/results/recovery_result.json",
        "sha256": "e42c35dc68b30e06735de7219928cde7b6214f5705a7da68d1856c447f66042b"
      }
    ]
  }
]
```


证据记录：`E0021`。

```json
[
  {
    "actual_result": "NBS对照产生相似谱形表明该观察无需酶也可出现；选定R4不代表3/4混合物整体或生物级联。额外67atomDCM点5保持未收敛；新4Force方向曲率为正且两步长一致，但不是完整Hessian或通路证明，未据此授路径通过。"
  }
]
```

### conclusion_investigation — What molecular evidence can explain the observed halocyclization selectivity of hydroperoxide (R)-4, and what remains uncertain when the source nonenzymatic NBS reaction is used as the chemical model?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list. Assess completion against the original public scientific question, not a self-narrowed addressed_scope. Missing necessary investigation, a failed calculation, copied public source values or a statement of source ambiguity earns no credit for the missing work and cannot yield whole-task full credit. Preserve credit for independently valid completed parts and accept sufficiently supported non-author conclusions without a fixed route or extra method matrix.

当前复审：身份、两个有效最低点、同定义电荷/MEP、结构混杂与因果边界覆盖；比较支持更强烯烃极化，不声称已建立完整反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main3–5/7; SI30–32",
    "actual_result": "作者水相B3LYP/CBSB7/CPCM的真实最低点及同波函数MK/MEP支持(R)-4烯烃位点显著不等价：默认q(C2)−q(C4)=−0.484265e，7的q(C8)−q(C10)=−0.055066e，幅度比8.794265；源图对应−0.441/−0.049e、比9.0。预定固定密度加密后仍为−0.427513/−0.049492e、比8.638022。因此源核心的“邻近OOH一端更负、4相较7更强极化”在既有定性验收口径和采样控制下重现。这个反应物电子偏置为非酶NBS条件下的选择性提供有限分子解释，与实验六元环偏好相容，不等同于已确定哪一溴鎓离子出口、活化自由能或定量产率。实际图中O21–C18–C15–C9–C6–C4闭合为六元环，而连至C2增加一个环原子；NBS为具名亲电溴源，不能以裸Br−代替。4与7同时改变碳数、支化及立体环境，未隔离OOH唯一因果；正文也将偕二甲基Thorpe–Ingold作用列为待研究。NBS对照说明特定产物谱形无需酶参与即可出现，并不证明酶在其他条件无作用。水相单体不是DCM反应溶液，所选R4不是整个3/4混合物，源473mM与量/体积47.3mM冲突保留且不用于速率推算。",
    "reason": "源的限定电子极化结论与当前题的解释/不确定性均有新增与旧计算支持；完整动力学、固定点6–10不是本候选所主张或当前必需的结论。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_identity_pair_audit.json",
        "sha256": "89772963a703168fda600c976567a053c988e10961d169192043216a65fe38aa"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_identity_pair_audit.json",
        "sha256": "0f9ff7cf1abed87a549ae1df5be18a57ba5a6f8f741913ee69b8510e7b72cb3b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/analysis_summary.json",
        "sha256": "7c6a3530c395fbec4e20d09880eb93581d87748a38abbeeec322ee0bedd4faac"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/results/Br_author_MK_four_column_and_contrast.json",
        "sha256": "9dd69619864a73e33a7fabc40a81b3e6448a3aa8776acf4d46130c9a4b6d2bce"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json",
        "sha256": "aedd38f1d2e1ff06de2b53396a8dbee422ff0b7a3b5960366865f30b6fcffe71"
      }
    ]
  }
]
```


证据记录：`E0021`。

```json
[
  {
    "actual_result": "作者水相B3LYP/CBSB7/CPCM的真实最低点及同波函数MK/MEP支持(R)-4烯烃位点显著不等价：默认q(C2)−q(C4)=−0.484265e，7的q(C8)−q(C10)=−0.055066e，幅度比8.794265；源图对应−0.441/−0.049e、比9.0。预定固定密度加密后仍为−0.427513/−0.049492e、比8.638022。因此源核心的“邻近OOH一端更负、4相较7更强极化”在既有定性验收口径和采样控制下重现。这个反应物电子偏置为非酶NBS条件下的选择性提供有限分子解释，与实验六元环偏好相容，不等同于已确定哪一溴鎓离子出口、活化自由能或定量产率。实际图中O21–C18–C15–C9–C6–C4闭合为六元环，而连至C2增加一个环原子；NBS为具名亲电溴源，不能以裸Br−代替。4与7同时改变碳数、支化及立体环境，未隔离OOH唯一因果；正文也将偕二甲基Thorpe–Ingold作用列为待研究。NBS对照说明特定产物谱形无需酶参与即可出现，并不证明酶在其他条件无作用。水相单体不是DCM反应溶液，所选R4不是整个3/4混合物，源473mM与量/体积47.3mM冲突保留且不用于速率推算。"
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 3.97 小时；14 份计时日志/16 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,6,8,20 线程/进程；Gaussian %Mem=16000MB,16GB,20000MB,24000MB,48000MB,8GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0004 · v2_execution_20260929/data/7_single_point.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_single_point.log) | Gaussian:267.5 | 正常 | {"threads":[6],"Gaussian_mem":["20000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · v2_execution_20260929/data/R4_single_point.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_single_point.log) | Gaussian:958.5 | 正常 | {"threads":[6],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · native_population/7_default_density1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_default_density1/gaussian.log) | Gaussian:1.6 | 正常 | {"threads":[4],"Gaussian_mem":["8GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · native_population/7_density6_fixed4layers/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_density6_fixed4layers/gaussian.log) | Gaussian:1.7 | 正常 | {"threads":[4],"Gaussian_mem":["8GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · native_population/R4_default_density1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_default_density1/gaussian.log) | Gaussian:4.1 | 正常 | {"threads":[4],"Gaussian_mem":["8GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · native_population/R4_density6_fixed4layers/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_density6_fixed4layers/gaussian.log) | Gaussian:1.8 | 正常 | {"threads":[4],"Gaussian_mem":["8GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0010 · execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/stdout.log) | Gaussian:267.5 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[6],"Gaussian_mem":["20000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0011 · execution_jobs/job_473a36ad38d341958b02aed35c740048/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/stdout.log) | Gaussian:4081.1；Gaussian:4940.3 | 正常；正常 | {"threads":[8],"Gaussian_mem":["48000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0012 · execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/stdout.log) | Gaussian:958.5 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[6],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0013 · execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/stdout.log) | Gaussian:1296.5；Gaussian:1573.7 | 正常；正常 | {"threads":[8],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0064 · results/R4/multiwfn.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/multiwfn.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0067 · results/7/multiwfn.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/multiwfn.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0094 · gaussian_batch/R4_esp_mk/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/stdout.log) | Gaussian:469.3 | 正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0096 · gaussian_batch/alkenol7_esp_mk/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/stdout.log) | Gaussian:122.7 | 正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0098 · native_cases/probe01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe01/gaussian.log) | Gaussian:138.5 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0099 · native_cases/probe02/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe02/gaussian.log) | Gaussian:137.3 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0100 · native_cases/probe03/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe03/gaussian.log) | Gaussian:147.3 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0101 · native_cases/probe04/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe04/gaussian.log) | Gaussian:147.4 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

水相分子计算与DCM/NBS实验不同；两分子结构并非只差单一因素；源473 mM与量/体积推得47.3 mM的冲突保留。

```json
[
  "No source atomic-charge last-digit match is claimed; charge partitions and unspecified fitting sampling remain representation-sensitive.",
  "Water monomers do not reproduce DCM reaction free energies. The optional failed 67-atom path contributes no accepted evidence and is not a source-mandated step.",
  "4 versus7 changes more than OOH; enzyme independence applies only to the observed profile. NBS amount/volume implies47.3 mM versus printed473 mM; no rate inference is made."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Individual source atomic charges are not all matched; robustness concerns the stated signed contrast and relative polarization.",
  "Water-continuum monomers do not reproduce the DCM/NBS reaction free-energy network or enzyme chemistry.",
  "The NBS source concentration is internally inconsistent (473 mM versus 47.3 mM from amount/volume); no concentration-dependent rate is certified.",
  "The additional 67-atom path remains unconverged and has no role in the accepted conclusion."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_c625cba3ce868eb1.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_c625cba3ce868eb1/verified_computation_reference.md)；SHA-256 `942b36790dcf92bda9fa563321f8d1b622921b39fd91fbd412eada2664ff81ce`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_c625cba3ce868eb1.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_c625cba3ce868eb1.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_c625cba3ce868eb1.json) | `2389d597e42e313e5dd71ab4c473de4d72e5b99219526acd97e383c4488494b9` | evidence_or_analysis |
| E0002 | [papers/paper_c625cba3ce868eb1/documents/main.pdf](../../../../papers/paper_c625cba3ce868eb1/documents/main.pdf) | `44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8` | source_document |
| E0003 | [papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf](../../../../papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf) | `19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db` | source_document |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_single_point.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_single_point.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `13e64fd4d478dec68dfc3227843bc0b6a6d9257f73b94d60721e475e40ca333e` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_single_point.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_single_point.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `a70b088f87d09417be7cfac1b04166d1a7d3c4253c08756ff6a4231576931872` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_default_density1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_default_density1/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `b84648198f5a9e1569f0dbbdd5a1698dc3c30f34ed656e842703a4753398181e` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_density6_fixed4layers/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_density6_fixed4layers/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `3ad95b612cb23042cb6ad1cef70f09f70235d0a0677b1a190e17876156a7589e` | native_output |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_default_density1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_default_density1/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `424a376c366a35593af6077548ed19985831c638ce71122b57e352e5cf2337e7` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_density6_fixed4layers/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_density6_fixed4layers/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `eaad20be43b6f07ade5ab8ec5dad5d417595bc326e52d51e133e39a3988cdba4` | native_output |
| E0010 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `13e64fd4d478dec68dfc3227843bc0b6a6d9257f73b94d60721e475e40ca333e` | native_output |
| E0011 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `d71119e27d3a76a605068fa318851671bf77b1e2285064ce0970712cf50b33ac` | native_output |
| E0012 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_native_excerpt.json) | `a70b088f87d09417be7cfac1b04166d1a7d3c4253c08756ff6a4231576931872` | native_output |
| E0013 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_native_excerpt.json) | `3a8bcc2254938b32e4eb58922164f27af6d46af6bc56165ea7ca9e9455bdb6f6` | native_output |
| E0014 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/results/MK_fixed_density_fit_controls.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/results/MK_fixed_density_fit_controls.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_MK_fixed_density_fit_controls.json) | `a8b16a400b2eda3a05c5d6a3e278509a7f918242b0a6be885b7a298e5c191b35` | evidence_or_analysis |
| E0015 | [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_task.md) | `ba542a061e6d1c7eb2289f25e2ef375ba6d7ad8c1cba712b9e429915e3ab8568` | historical_task_binding |
| E0016 | [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_reference_key_points.json) | `7190ab1a303a14d25eed1cfb61c2e093b0d562c03c6feb246a3a1a48ecb00294` | historical_task_binding |
| E0017 | [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_reference_conclusions.json) | `306729d60335d769f34bc5039fd908edb04788677574b9a4f0be52fdffc97bd7` | historical_task_binding |
| E0018 | [tasks/v2_autonomous_research/paper_c625cba3ce868eb1/agent_input/task.md](../../../v2_autonomous_research/paper_c625cba3ce868eb1/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_task.md) | `5ec3fcba37151f4277a8f5a814ecac8c25dbabd9bb2a5b4e1f52e6a3eda96928` | historical_task_binding |
| E0019 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/SOURCE_ROUTE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/SOURCE_ROUTE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_SOURCE_ROUTE_READBACK.json) | `0f04f4b570bd4a823a03f1840ddd8b349c64c94ccf9ce94eb63ae31d4c2bc738` | evidence_or_analysis |
| E0020 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/NATIVE_REUSE_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/NATIVE_REUSE_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_NATIVE_REUSE_INTAKE.json) | `44daf5e8144df39c1edc7b9514f9eb22f3bade3c210550573ed02f4f4860d195` | evidence_or_analysis |
| E0021 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_COMPUTATION_COVERAGE.json) | `c6d202337eacae3377255fcfa3db7149722fbda9978c1f7b1a598f122c8cae1d` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/INTENT_RECEIPT_RECONCILIATION.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_c625cba3ce868eb1/INTENT_RECEIPT_RECONCILIATION.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_INTENT_RECEIPT_RECONCILIATION.json) | `2aa33cf9b48b49fdaeabe16d56893e54c9772dd3f2d40452dfa1156b5d6d75be` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_c625cba3ce868eb1.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_c625cba3ce868eb1.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_paper_c625cba3ce868eb1.md) | `81ea574a5b1ad7b07b66710ec7a15baff931bde94a7097d5018d52e3dd8e6da7` | evidence_or_analysis |
| E0024 | [docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `7fdaba36a9e0f724d4c8b48f5e0a7d29ed5559916059fdf46d178fc28a6a960e` | historical_task_binding |
| E0025 | [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `7fdaba36a9e0f724d4c8b48f5e0a7d29ed5559916059fdf46d178fc28a6a960e` | historical_task_binding |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_identity_pair_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/R4_identity_pair_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_R4_identity_pair_audit.json) | `89772963a703168fda600c976567a053c988e10961d169192043216a65fe38aa` | evidence_or_analysis |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_identity_pair_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/data/7_identity_pair_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_7_identity_pair_audit.json) | `0f9ff7cf1abed87a549ae1df5be18a57ba5a6f8f741913ee69b8510e7b72cb3b` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/SOURCE_PAGES.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/SOURCE_PAGES.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_SOURCE_PAGES.json) | `bc5d368e680535a6f0df9dc4449649a1584e1f092ba3de599577c12687e56183` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/analysis_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_analysis_summary.json) | `7c6a3530c395fbec4e20d09880eb93581d87748a38abbeeec322ee0bedd4faac` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/results/Br_author_MK_four_column_and_contrast.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/results/Br_author_MK_four_column_and_contrast.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_Br_author_MK_four_column_and_contrast.json) | `9dd69619864a73e33a7fabc40a81b3e6448a3aa8776acf4d46130c9a4b6d2bce` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/AUTHOR_MK_SOURCE_REVIEW_20261007.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/AUTHOR_MK_SOURCE_REVIEW_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_AUTHOR_MK_SOURCE_REVIEW_20261007.json) | `907a73b4806332aa3b0da76eee896399b2c1cae82c9228f9858f0e9d0ca312f8` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/RETURNED_CURVATURE_NATIVE_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/RETURNED_CURVATURE_NATIVE_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_RETURNED_CURVATURE_NATIVE_INTAKE.json) | `b6b34f2915977f264b8d279a22c8fc1bee6deb70b9c97e586d921abd08483a6a` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/results/recovery_result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/results/recovery_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_recovery_result.json) | `e42c35dc68b30e06735de7219928cde7b6214f5705a7da68d1856c447f66042b` | evidence_or_analysis |
| E0034 | [tasks/final_verified_paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_scoring_rules.json) | `aedd38f1d2e1ff06de2b53396a8dbee422ff0b7a3b5960366865f30b6fcffe71` | historical_task_binding |
| E0035 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_task.md) | `5ec3fcba37151f4277a8f5a814ecac8c25dbabd9bb2a5b4e1f52e6a3eda96928` | historical_task_binding |
| E0036 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_reference_key_points.json) | `7190ab1a303a14d25eed1cfb61c2e093b0d562c03c6feb246a3a1a48ecb00294` | historical_task_binding |
| E0037 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_reference_conclusions.json) | `306729d60335d769f34bc5039fd908edb04788677574b9a4f0be52fdffc97bd7` | historical_task_binding |
| E0038 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_scoring_rules.json) | `489e75bf8c10e0d1ead1aa752bb302054c169d2ed83c5dc391f2f8c435fff0c0` | historical_task_binding |
| E0039 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_task.md) | `ba542a061e6d1c7eb2289f25e2ef375ba6d7ad8c1cba712b9e429915e3ab8568` | historical_task_binding |
| E0040 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_reference_key_points.json) | `7190ab1a303a14d25eed1cfb61c2e093b0d562c03c6feb246a3a1a48ecb00294` | historical_task_binding |
| E0041 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_reference_conclusions.json) | `306729d60335d769f34bc5039fd908edb04788677574b9a4f0be52fdffc97bd7` | historical_task_binding |
| E0042 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_scoring_rules.json) | `489e75bf8c10e0d1ead1aa752bb302054c169d2ed83c5dc391f2f8c435fff0c0` | historical_task_binding |
| E0043 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7c388c58ce38b47e_G4.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7c388c58ce38b47e_G4.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_7c388c58ce38b47e_G4.json) | `7c388c58ce38b47e86e25cf2dffaf501baa1826a280e6620cd674fffadde9508` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G4.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G4.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_G4.json) | `7c388c58ce38b47e86e25cf2dffaf501baa1826a280e6620cd674fffadde9508` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7c4aa0f67992a768_paper_c625cba3ce868eb1_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7c4aa0f67992a768_paper_c625cba3ce868eb1_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_7c4aa0f67992a768_paper_c625cba3ce868eb1_delivery_integrity.json) | `7c4aa0f67992a768335e4a3cba97a5ce7283a28fe60e2aedaf42b4bf4b2c7da9` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_c625cba3ce868eb1_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_c625cba3ce868eb1_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_paper_c625cba3ce868eb1_delivery_integrity.json) | `7c4aa0f67992a768335e4a3cba97a5ce7283a28fe60e2aedaf42b4bf4b2c7da9` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/9f470654dc4cb726_paper_c625cba3ce868eb1_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/9f470654dc4cb726_paper_c625cba3ce868eb1_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_9f470654dc4cb726_paper_c625cba3ce868eb1_primary_pages.json) | `9f470654dc4cb726f3f38da96ffe0622dcaa6d7c9e841d6d48db3b6fd1c78b87` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_c625cba3ce868eb1_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_c625cba3ce868eb1_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_paper_c625cba3ce868eb1_primary_pages.json) | `9f470654dc4cb726f3f38da96ffe0622dcaa6d7c9e841d6d48db3b6fd1c78b87` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e0e31b241c1751f6_G4_PA_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e0e31b241c1751f6_G4_PA_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_e0e31b241c1751f6_G4_PA_native_readback.json) | `e0e31b241c1751f622de318b4d83c8e8ec43abe8f39b5b8aaeb6013bb664450b` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/G4_PA_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/G4_PA_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_G4_PA_native_readback.json) | `e0e31b241c1751f622de318b4d83c8e8ec43abe8f39b5b8aaeb6013bb664450b` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_default_density1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_default_density1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_input.com) | `cad181259e0466c0be7902b7c01c8c945185a10206dac688d4c22663ce0b2e1a` | input_or_analysis_code |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_density6_fixed4layers/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_density6_fixed4layers/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_input.com) | `3a421ab3dc717de72fa0bb7e44333a0829d6fdb2f0e92a2d0fa13ce9dec847f0` | input_or_analysis_code |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_default_density1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_default_density1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_input.com) | `cad181259e0466c0be7902b7c01c8c945185a10206dac688d4c22663ce0b2e1a` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_density6_fixed4layers/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_density6_fixed4layers/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_input.com) | `3a421ab3dc717de72fa0bb7e44333a0829d6fdb2f0e92a2d0fa13ce9dec847f0` | input_or_analysis_code |
| E0055 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_input.com) | `5ff2cc2ed0573074385f29bd4efac874dea67a227444d2b26cfaa57ebf36ee83` | input_or_analysis_code |
| E0056 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_input.com) | `69b2d70979a3d010c0a32fc0957840609b564358212050d807910460af80b7aa` | input_or_analysis_code |
| E0057 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_input.com) | `3d48b391aa4bb82aec9b81bae912ad4c4ac51eea83a080eef3e522915e5d79e0` | input_or_analysis_code |
| E0058 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_input.com) | `9eaf09bac2596ff6a465d6f77928ecd4f2b372a7823a4190ac961794ae3f2590` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_submission.json) | `c6ea51bda2ad8e1740df6e0438422404403c07ca512ab3b2338727763acbf26a` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_status.json) | `b2b4491f17e356769f1376d0558dcaf5a67af72439fbc048ee769430013246ff` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_analysis.py) | `7207b8623cb73e33b25a870ae5262610c37632f17abf6f51768d79451cb8927b` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/inputs.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_inputs.json) | `ad129ad6a850ef56dd4e174194de15f8266eeb31a4028e82de1f5be0ad2d6897` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/result_manifest.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/result_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_result_manifest.json) | `5a689a04ce54c5ffc7e107942b54e3ed8c3f6081698589ef814ab086923535a7` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/multiwfn.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/multiwfn.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_native_excerpt.json) | `0041839bf53bf163923a21830878b4d8b718247b3dd7bac2349ecc89043bd3de` | native_output |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/source.mep.pdb](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/source.mep.pdb) | `7bada25671fba62354583471be914ece0ed6e23442a621f4b6ab0d17ded7fa29` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/surface_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/R4/surface_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_surface_summary.json) | `cb6dbe7346dc2904928961c5c8a0796638403edf25aa106418c92b8794ed011c` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/multiwfn.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/multiwfn.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_native_excerpt.json) | `9e305913b417645da8c5d9ae7e4e328c698e65623547c446e55484efb818aa7a` | native_output |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/source.mep.pdb](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/source.mep.pdb) | `e15c708ee710df8248eb5fb59472e16769a2309ab5c2630d385c10aa202ece7e` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/surface_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/source_signed_MEP/a01/results/7/surface_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_surface_summary.json) | `f6ebaf3345d9ece353521cdf3cacb69bc636d47486fae897de7ad75122a67e74` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_submission.json) | `f81313a54836b3e7740ddfbd5b80e47526c97c6af1123663432ae7e422cc6ac0` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_status.json) | `4efe663477255ab861951905121e06958049d51dcadba2fb00d61ad719650796` | evidence_or_analysis |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/results/run_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/results/run_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_run_summary.json) | `2136ce3675250701c8f7872bef8d7be1f5f3391670a9d3e4090b2ba15216542f` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_submission.json) | `012fbc1dfbf21e4b06dcf8c0e5e476a996a3e064de1c25b9f1f0180866f9e4b6` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_status.json) | `443329bd7cfe54fa249b3f62d84d67eb12f7e3304a49aeefc62dd902239f2c24` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/results/run_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_history60_return_and_source_MK_assessment_20261007/a01/results/run_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_run_summary.json) | `b42972152139cc75b61ec4003533f537b41364ba8119e99593eb9729a3310606` | evidence_or_analysis |
| E0076 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/PASS_CANDIDATE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_c625cba3ce868eb1/PASS_CANDIDATE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_PASS_CANDIDATE.json) | `d16e358ac84b4aeb9ff8d42f54fb1678f296a80f1146163f99a504e4404546cc` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_C2Br_OptRestart_HIGH6_20261004/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_C2Br_OptRestart_HIGH6_20261004/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_submission.json) | `dea94ac2e8c5dd4e32357dc63e35fa9a60635b5073515f9a74f0743f41a1a61d` | evidence_or_analysis |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_C2Br_OptRestart_HIGH6_20261004_explicit_method/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_C2Br_OptRestart_HIGH6_20261004_explicit_method/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_submission.json) | `8f34ecbd8703b929b5ea5f3f621c86c04b9bb83b59334b47ab56f74ec55de065` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_C4Br_single_failedpoint_projectedCartesian_20261002/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_C4Br_single_failedpoint_projectedCartesian_20261002/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_submission.json) | `b4f6fb40f3090111e0d69e05b245592c2b75d086bebfdefef258897068676b4d` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_OptRestart_state_guard_fix_20261004/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_OptRestart_state_guard_fix_20261004/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_submission.json) | `6f99b85fc6439b898fbb65571c010da47269afc7f93cb0a40f1f46a62477cdc9` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_Cartesian_constrained_BFGS_once32F_20261005/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_Cartesian_constrained_BFGS_once32F_20261005/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_submission.json) | `33dc7946ad9f775fb789ac42109d22db33a25629881ce2f49c68b1530586a112` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_PDens10_one_repair20F_gate5_20261006/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_PDens10_one_repair20F_gate5_20261006/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_submission.json) | `18933deff0909ae5d066e47b53eac17c416c5c51ce437e5a2cf02cd850899516` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_submission.json) | `0942c8310ba3d58f81fd96aea989bb33b03118964599a2167a785139e21d4eac` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_fixed_derivative_surface_7F_20261006/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_fixed_derivative_surface_7F_20261006/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_submission.json) | `8222cc26098e3aea842b12067cf7f1d86ec4233860a1f50c2348e968b0fdebcc` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_submission.json) | `a7e5c76ad209dd29f210717adac6b24d4d471a19125c0acd97a3bcdfdf881e1e` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/C4Br_point5_freshHessian_scan5_step025/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/C4Br_point5_freshHessian_scan5_step025/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_submission.json) | `319238c656ff671dfc66460c9a97ec49919e847e1d436e747871807b2d3a9b80` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/G4_Br_PDens10_return_Harziane_full_evidence_20261007/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/G4_Br_PDens10_return_Harziane_full_evidence_20261007/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_submission.json) | `415f04793bd05faa3a17da0ae1f7962a614058d03e4d0e26ccd869f20e97d2d3` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/R4_NBS_Et3N_face_a_DCM_pilot/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/R4_NBS_Et3N_face_a_DCM_pilot/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_submission.json) | `c3ad1ee8be0cce2c26ca00d192ed539fa2fda6a0bc75ef06d6a46c7d2ae3d959` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/R4_NBS_Et3N_native_C4Br_relaxed_scan10_DCM/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/R4_NBS_Et3N_native_C4Br_relaxed_scan10_DCM/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_submission.json) | `fe02d62eff8e7f1866fa98e20cc76ebe0671ee6096c53514b66c9c2ee4e2524d` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/R4_source_six_ring_C2Br_finite_control_20261003/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/R4_source_six_ring_C2Br_finite_control_20261003/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_submission.json) | `fede29c4301256125f83fd51119ebbb2db7780b0ffde541ad1e63eafa54bbe97` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_binding.json) | `164f222ceb6ee0faf5f29d73814a8f2ffd64ddfdd77334c0849d04b2d42549eb` | evidence_or_analysis |
| E0092 | [.software_cache/installations/gaussian/g16/install/g16/formchk](../../../../.software_cache/installations/gaussian/g16/install/g16/formchk) | `78dc9981fd170cc99d8052aa26471244e04fd2c8aea7d73aaf641c193e7b6bd5` | evidence_or_analysis |
| E0093 | [.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI) | `d7d2539dae7b8d2faf03ca473d856cf1936a7b8ca4fdcfbb3e1cfa5f45184030` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_native_excerpt.json) | `0bb004fd7b10ab6354d62d5a1cb4e087682edb207346d74d77a045e7c3db1bc4` | native_output |
| E0095 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_input.com) | `1a14db78f3ab71b774685d1171eaae0564c4581e4156bc9dbcd9a9523e44b65d` | input_or_analysis_code |
| E0096 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_native_excerpt.json) | `fe902d2eedf870f2ff10eca31b35be6388e85275a2f2bfbdb41f11e2fc69d106` | native_output |
| E0097 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_input.com) | `c85a66cbeb0b7938729750f448670368dac669f1174d1728d699a51ed41a8d81` | input_or_analysis_code |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0098_native_excerpt.json) | `56298f579fed50dd03200d2a729db201da90b0197ebafc842802b4054ab1001f` | native_output |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe02/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe02/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_native_excerpt.json) | `51e9536a40570937ea46921607d41c9cd3119f3ef56949ba7e010311341ab982` | native_output |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe03/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe03/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_native_excerpt.json) | `55c117266b8eea7cc3edd564653bd3eb5b6c0ef678b408454da13d2c6e0ef71c` | native_output |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe04/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe04/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_native_excerpt.json) | `6506a6186c2c57dba9eb6d4c2828a50cd47de35136929f8f1e6ee27523e24c0a` | native_output |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/native_cases/force40/job.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_restored_BFGS_add40F_gate5_20261007/a01/native_cases/force40/job.chk) | `093a0b282be56d774191ad64509f90226b29552d05d91c42dcdc5351cf32c486` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group4/BR_HISTORY40_BUDGET_RELEASE_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group4/BR_HISTORY40_BUDGET_RELEASE_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_BR_HISTORY40_BUDGET_RELEASE_20261007.json) | `ebb976895a3dab10b0fce33f4d9c99bd1dda30fa03645bafab54e16035380982` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/verification_report.md](../../../../docs/v2_verification/history/verification/group_4/paper_c625cba3ce868eb1/verification_report.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_verification_report.md) | `c5a907e7f1ed39cec29f8021391cf99a0662d5665d454627a5db749b8818b3a1` | evidence_or_analysis |
| E0105 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_critical_failures.json) | `95ea3db4a6fa510f59f15f1714ae657b1b31407f39f01cea983d270ed321c333` | historical_task_binding |
| E0106 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_c625cba3ce868eb1/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0106_package_manifest.json) | `89c8fa1427bfa78667c31c657871b903bd079cf1f03951cc6d8772e9982e868b` | historical_task_binding |
| E0107 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_critical_failures.json) | `95ea3db4a6fa510f59f15f1714ae657b1b31407f39f01cea983d270ed321c333` | historical_task_binding |
| E0108 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_package_manifest.json) | `eb594145d958df14326321550011e89b9e4a06d63c134fc3258353619d863050` | historical_task_binding |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/reuse_audit/R4_native.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/reuse_audit/R4_native.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_R4_native.json) | `89772963a703168fda600c976567a053c988e10961d169192043216a65fe38aa` | evidence_or_analysis |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/reuse_audit/7_native.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/reuse_audit/7_native.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_7_native.json) | `0f9ff7cf1abed87a549ae1df5be18a57ba5a6f8f741913ee69b8510e7b72cb3b` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/settings.ini](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/settings.ini) | `1299b5485e5197fa86497b8fc0632583e5fee0a2d0cb1f95c9aef5b8092a4d25` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/contract_snapshot/20260930_final_repair/binding.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/contract_snapshot/20260930_final_repair/binding.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_binding.json) | `7b01e4850b7d8db1ca0435c93c45f32264265153090339ff213e0176a59254b5` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REVIEWED_FOLLOWUP_WINDOW_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REVIEWED_FOLLOWUP_WINDOW_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_REVIEWED_FOLLOWUP_WINDOW_20260930.json) | `3de07be5e6428385a87219a1411227baa8b83129b99009261d7313261d0f6605` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_input.com) | `167a46ea9be4f9c1ede8b68ed46da492b8c7d824dfab32705e1262ba8c32108e` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe02/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe02/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0115_input.com) | `0a96ab5c4fdb843a6ceb6f47797da989cd7361fbc67696341432950911be9a39` | input_or_analysis_code |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe03/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe03/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0116_input.com) | `64895e4a7b3566f5b42cdb7f365776c3db7f99bebc1d73e28a2555de0a674b14` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe04/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_point5_directional_curvature4F_20261008/a01/native_cases/probe04/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_c625cba3ce868eb1/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0117_input.com) | `b39121e53300d22c44c0d8479793c239458d1f9ee833f4cf22b15a781cafb877` | input_or_analysis_code |
| N0118 | [tasks/v2_autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_key_points.json) | `7190ab1a303a14d25eed1cfb61c2e093b0d562c03c6feb246a3a1a48ecb00294` | latest_review_evidence |
| N0119 | [tasks/v2_autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json) | `306729d60335d769f34bc5039fd908edb04788677574b9a4f0be52fdffc97bd7` | latest_review_evidence |
| N0120 | [tasks/v2_autonomous_research/paper_c625cba3ce868eb1/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_c625cba3ce868eb1/evaluation/scoring_rules.json) | `489e75bf8c10e0d1ead1aa752bb302054c169d2ed83c5dc391f2f8c435fff0c0` | latest_review_evidence |
| N0121 | [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json](scoring_rules.json) | `489e75bf8c10e0d1ead1aa752bb302054c169d2ed83c5dc391f2f8c435fff0c0` | latest_review_evidence |
| N0122 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0123 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/agent_input/task.md](../agent_input/task.md) | `ba542a061e6d1c7eb2289f25e2ef375ba6d7ad8c1cba712b9e429915e3ab8568` |
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_key_points.json](reference_key_points.json) | `7190ab1a303a14d25eed1cfb61c2e093b0d562c03c6feb246a3a1a48ecb00294` |
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_conclusions.json](reference_conclusions.json) | `306729d60335d769f34bc5039fd908edb04788677574b9a4f0be52fdffc97bd7` |
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/scoring_rules.json](scoring_rules.json) | `489e75bf8c10e0d1ead1aa752bb302054c169d2ed83c5dc391f2f8c435fff0c0` |
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/critical_failures.json](critical_failures.json) | `95ea3db4a6fa510f59f15f1714ae657b1b31407f39f01cea983d270ed321c333` |
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/evidence_map.json](evidence_map.json) | `57af4cc7efa0697e679be5beebbb0a05db34498cd241d659a8eb1c03a1e9e129` |
| [tasks/v2_paper_reproduction/paper_c625cba3ce868eb1/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `6f8d4fe38d9b2784b1707f8fbbd29e408485ae57a27cb2c1bf1f5921fa4d4961` |

## 2026-10-19 active paper_science_v2 scoring migration

The active private rubric assigns 100 points only to independent intermediate findings and final scientific conclusions, using binary leaves and no process score or multiplier. Historical criteria/weights above are archival, not active scoring. Public inputs and author-route contract remain byte-identical. Existing acceptance remains PASS_STRICT_CURRENT_FROZEN_SCOPE; this migration is not new chemical validation. Fixed windows and retained boundaries are in scoring_rules.json and reference_qualification.json.


## 2026-10-19 Round3 scoring-contract repair

Historical verification statements above are preserved verbatim. Current mode-specific scientific rules supersede earlier scoring-policy wording; this append does not change the chemistry acceptance class.

- Audited every existing leaf for scientific role, source/verification support and physical definitions; retained unproven narrow-window risks as explicit provisional calibration limits rather than inventing wider tolerances.

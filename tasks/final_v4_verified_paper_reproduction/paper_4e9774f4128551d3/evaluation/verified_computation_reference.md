# 本次V3范围与逐命题证据复用（2026-10-28）

解释题范围不变：端点稳定性、平衡解释、有限时选择性可辨识性及局部立体转换。两模式各4条同权重最终命题。保留既有模式差异：PR稳定性项为原2.3171919±1.0 kcal/mol纯MeOH复合G目标，AR为自选可比条件的稳定性判断，未向AR暗加纯MeOH门槛。

- `endpoint_stability`：四个原生日志的单点与热项；2.641369354 kcal/mol；PR原2.3171919±1.0窗口保留，AR原无强制纯MeOH数字门槛。
- `equilibrium_implication`：已有动力学analysis_summary记录native298.15 K平衡T/C=86.325116；是模型平衡，不是实测K。
- `finite_time_nonuniqueness`：source_endpoint_kinetic_witness/a01/results/analysis_summary.json；12组条件反例，同G与详细平衡下30min T/C可0.1/1.1/10。
- `local_stereochemical_reset`：公开map6/47/52/Si101图与SI20–21；已有inventory审查保持其余11/13/30立体中心。无真实质子化TS，规则不要求。

未提交新计算；以下历史正文逐字保留。历史PASS不代表新V3全部命题重新验证通过。

---

# V2 验证计算参考：Harziane端点稳定性与选择性限制

论文：`paper_4e9774f4128551d3`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：当前稳定性与有限时选择性不可唯一推断问题已闭合，未声称作者未计算的质子化TS或实测速率。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

50/trans与S20/cis端点相对稳定性及其对非平衡质子解选择性的解释限度。

冻结题面中的科学目标：

What molecular explanation of the stereochemical outcome of the reported 50 → silyl enol ether → ketoester sequence is supported by reproducible evidence, and how securely can that explanation be related to the experimental conditions?

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors sought cis material despite calculations favouring trans-50 by 2.32 kcal/mol. They report that reversible epimerization gave trans, whereas isolated silyl-enol-ether protonolysis with (±)-CSA gave 1.1:1 trans:cis. Their DFT comparison is a product thermodynamic rationale, not a calculated protonation mechanism. SI p71 specifies Gaussian09, B3LYP-D3/6-31G(d,p) optimization, B3LYP-D3/6-311++G(d,p) single points and IEF-PCM methanol (epsilon32.63), with thermal corrections; tables S35–S38 provide structures/frequencies. Reproduce/audit that disclosed baseline and assess its explanatory limits. A solvent inconsistency remains between main Scheme5 and SI pp20–21; document which interpretation is used. Acid-face pathways, single-MeOH clusters and mandatory weighted kinetic matrices were added by the benchmark, not established by the source.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_4e9774f4128551d3/documents/main.pdf](../../../../papers/paper_4e9774f4128551d3/documents/main.pdf) | `37a7fad866bff774d010cc6b61af21da2150a78c5bce69c1ff41574648c5b8b4` |
| [papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf](../../../../papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf) | `64fda6d0c684c5c53ad4434788b2fe57bfa21ff63ec78215d47885b4103de76a` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

B3LYP-D3/6-31G(d,p) Opt/Freq→6-311++G(d,p)/IEFPCM(MeOH ε32.63)SP，一次气相RRHO校正；G09Defaults/FineGrid实算控制。

1. 核对 50/trans 与 S20/cis 两个完整 C20H30O3、53 原子、中性单重态端点，检查立体化学与原子库存；准备过的烯醇/CSA 图不冒称已认证酸解最低点或过渡态。

2. 执行 B3LYP-D3/6-31G(d,p) 优化/频率，两个端点各 153 正模；随后按作者 6-311++G(d,p)/IEFPCM MeOH(ε=32.63) 单点。复合 G 只加一次低层气相 RRHO 校正。

3. 从原生记录计算 G(S20)−G(50)=2.641369354 kcal/mol；源为 2.3171919，差 0.324177，沿用已存在的同量 ±1 kcal/mol 标准。G09Defaults/FineGrid 控制保留 2.633079954/2.632408519；SI 热项 0.416764/0.417259 Eh 得到恢复，绝对高层 SP 残差不隐藏。

4. 利用已有十二组保持相同端点 G 与详细平衡的条件动力学反例，计算固定 30 min 下可出现约 0.1、1.1、10 的 T/C，证明端点稳定性不能唯一指定单次质子解比率。这是可辨识性计算，不是分子 TS 或实验速率拟合。

5. 将可逆 trans 偏好、一次 1.1:1、BINOL 条件及三轮回收 70% 区分。正文/SI 的 THF/MeOH 1:1/10:1 矛盾公开保留，纯 MeOH 模型不替代实验混合物；不声称质子化面或完整反应路径已验证。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| G(S20)−G(50),kcal/mol | 2.3171919 | 2.641369354 | 实算−论文：0.324177454； 既有针对同一端点量±1标准内，正稳定性结论保持；本轮直接打印Gcorr重算2.641225，~0.000144差来自打印口径，非科学差。；源定位：SI S71 |
| RRHO Gcorr,Eh | [0.416764,0.417259] | [0.416764,0.417259] | 实算−论文：[0,0]； 两个153正模最低点热项重现。；源定位：SI S71 |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| G(S20)-G(50), kcal/mol | 2.3171919 | 2.641369354 | Same endpoint observable lies0.324177 kcal/mol from source, within the pre-existing same-quantity±1 kcal/mol rule; not extended to absolute SP energies or rates. G09Defaults control2.633080 preserves this result. |
| Thermal corrections, Eh | [0.416764,0.417259] | [0.416764,0.417259] | Direct native thermochemistry equals SI printed corrections. |
| Finite-time selectivity versus equilibrium | Single-pass1.1:1 trans/cis;70% after recycling | Same endpointG admits hypothetical detailed-balanced finite-time ratios0.1–10 while retaining the same stationary ratio. | A mathematical counterexample to endpoint-only kinetic inference, not claimed molecular rates or fit to1.1:1. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Correct stereochemical and chemical identities

冻结要求：Preserve source polycycle stereocentres outside the epimerizing region; verify 50/enol connectivity, proton/silicon/acid inventory and CSA chirality from actual structures. Do not treat an arbitrary constrained enol conformer as a confirmed minimum. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：两完整C20H30O3、53原子、中性单重态端点立体身份正确。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Full endpoints preserve stereochemical identities and atom inventory; no arbitrary acid complex is treated as a proven minimum."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical6; SI physical20–21 and TablesS35/S36",
    "actual_result": "50/S20均C20H30O3、53atom、q0/singlet；C6由R变S，远端11S/13R/30S保持。两端各153正频率，Opt与SP几何成对。O-TMS图编辑仅去C6-H7并将6–47/47–52改为双/单键，保留O52-Si101及三甲基；CSA两对映体CIP相反。烯醇+MeOH+CSA与ketoester+MeOTMS+CSA净库存同为C34H58O8SSi、102atom、q0。准备的烯醇/CSA图不称最低点。",
    "reason": "本题身份由实际图、源53atom端点和原生曲率支持；没有以假设反应储库替代量化最低点。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/stdout.log",
        "sha256": "03a5b18fc6fbad7d57a1d9e78c48c321cc40e9b84530f68c278e72fbcd12e1f4"
      },
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/stdout.log",
        "sha256": "f38246161d1544c512adbc5eed2aae6ab124969a1d12fb15ad50ac48989a4375"
      },
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/stdout.log",
        "sha256": "f41aed18706ecf8de85d2dd26f0c7c11c502ce5d280ec3bb275f4d0cb363ea90"
      },
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/stdout.log",
        "sha256": "a000e90f1744228420e1085c6fd8d58413ed430c094e4368b3506f80c8d260dd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/integrated_inventory_and_kinetic_test_preparation_20260930.json",
        "sha256": "3a243e3f7157943d88764e96ee0a9bb5a8dcc7ea11e872d11bd2c557345baf24"
      }
    ]
  }
]
```

### kp_question — Evidence explains the epimerization outcome

冻结要求：Reproducible quantities must materially assess why this sequence can yield the observed cis/trans distribution. Endpoint thermodynamics alone does not establish protonolysis selectivity. A valid limited conclusion exposing that insufficiency can earn credit if supported by substantive analysis, not a copied2.32 scalar. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：本轮四个原生日志重读复合G，确认trans更稳定。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Thermodynamic trans preference reproduced; quantitative detailed-balance examples establish why it cannot alone select a finite-time ratio."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical6; SI physical71 energy table",
    "actual_result": "ΔG(S20−50)=2.641369354(primary)及2.633079954(G09Defaults)，源2.3171919kcal/mol；均trans更低。旧±1.0对同一量适用。固定端点G的条件动力学模型仍允许不同30min支路，端点稳定性不足以指定1.1:1。",
    "reason": "实际热化学支持可逆条件trans偏好，现成守恒/详细平衡反例检验了从端点G推单次比率这一推论，而非仅重复2.32。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/stdout.log",
        "sha256": "03a5b18fc6fbad7d57a1d9e78c48c321cc40e9b84530f68c278e72fbcd12e1f4"
      },
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/stdout.log",
        "sha256": "f38246161d1544c512adbc5eed2aae6ab124969a1d12fb15ad50ac48989a4375"
      },
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/stdout.log",
        "sha256": "f41aed18706ecf8de85d2dd26f0c7c11c502ce5d280ec3bb275f4d0cb363ea90"
      },
      {
        "path": "docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/stdout.log",
        "sha256": "a000e90f1744228420e1085c6fd8d58413ed430c094e4368b3506f80c8d260dd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "8499f525a464335db0e096dc78cd1117627ce7942f962e5749c855a088a3f80e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/results/analysis_summary.json",
        "sha256": "f7c6f8ccc7a06c152c664eede3eca458b0f7d732baf5e33e385032f3e4dfc57b"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json",
        "sha256": "9b1be0e06b3d0e67ef93bef3ff7b560dfb73f0bae61a1918cecf445d19c7b840"
      }
    ]
  }
]
```

### kp_discrimination — Claims tested against the actual experimental contrast

冻结要求：Evaluate whether chosen evidence discriminates the submitted stereochemical account. Distinguish reversible-tautomerization observations, single-pass protonolysis and repeated isolated yield. Accept alternative molecular or kinetic reasoning with valid evidence; no face/acid matrix or single-solvent-cluster protocol is compulsory. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：固定端点G的12组详细平衡反例能产生不同有限时T/C，证明不能仅由端点算1.1:1。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Reversible trans preference, one-pass protonolysis ratio and recycled isolated yield are not conflated."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical6; Scheme5 physical5; SI20–21",
    "actual_result": "原生主路线固定ΔG在298.15K的两最低点条件平衡T/C=86.3251；源表为49.9474。已算30min反例在各自相同平衡比下分别约0.1、1.1、10，概率守恒与详细平衡通过。可逆只得trans、单次CSA1.1:1、BINOL3:1偏cis与三轮70%分开处理。",
    "reason": "反例仅否定端点能唯一决定有限时间选择性的逻辑，不冒充分子势垒、动力学拟合或实际实验达到平衡的证据。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/analysis.py",
        "sha256": "ff0aa507b1eb62b10eba1ba71ea16ac15618f6c83cf85693e9e7216a9eee49df"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/model.json",
        "sha256": "d48685804341af2634951c9992ba74fc8eca159d306c5747705e8fbd49bd8e51"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/results/analysis_summary.json",
        "sha256": "f7c6f8ccc7a06c152c664eede3eca458b0f7d732baf5e33e385032f3e4dfc57b"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_4e9774f4128551d3/SOURCE_PAGES.json",
        "sha256": "c2991118fb5de379103eff53aa114c7848f19e847e760be0f86021c93ecb5ceb"
      }
    ]
  }
]
```

### kp_uncertainty — Solvent and representation uncertainty addressed

冻结要求：Show how decisive conformational, acid/racemate, thermal or medium assumptions affect the claimed inference when applicable. Treat the1:1 versus10:1 solvent discrepancy explicitly and do not invent experimental uncertainty. The degree of robustness required follows the claim, not a fixed pair of functionals. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：纯MeOH源模型与实验THF/MeOH混合物分开；源1:1/10:1冲突保留；数值控制不冒充全面模型误差。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "THF/MeOH main1:1 versus SI10:1 remains explicit; pureMeOH PCM is only the author baseline."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI71 method; mainScheme5; SI21 solvent volumes",
    "actual_result": "同几何FineGrid控制ΔG2.632408519，联合G09Defaults2.633079954，原UltraFine2.641369354，绝对高SP源差仍在0.01358/0.01408Eh量级。低层气相RRHO298.15K/1atm+MeOHSP，同组成参照修正抵消；直接Gcorr与G−E精度口径分开。实验23°C与计算298.15K不混称。主文1:1/SI10:1与源未明确的烯醇E/Z、酸/构象范围均限制动力学外推。",
    "reason": "±1.0是既有针对相对G的验收窗口，非实验误差或所有方法的误差条。源绝对SP未复制，但不改变该精度下相对稳定性。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/50/gaussian.log",
        "sha256": "506b87b7f3b6addab51c579110c961f00ab30990c73f4faaf143713b8bb13777"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/S20/gaussian.log",
        "sha256": "67796080a4e44b6a067a29ee2001785823824cd978ecf77374a361c6b0207e8f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_grid_completed_same_definition_comparison_20261005/a01/results/Harziane_FineGrid_same_definition.json",
        "sha256": "6e3dd271a52eb58b851b58ef47affae950159d0de4bfdb25166389b1b833ad16"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/RAW_THERMAL_PRECISION_APPENDIX_20261007.json",
        "sha256": "5e51bdb41f0f7aad7321d45908908ec89f125b8ce36170827ec318ff8cdf70c1"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/integrated_inventory_and_kinetic_test_preparation_20260930.json",
        "sha256": "3a243e3f7157943d88764e96ee0a9bb5a8dcc7ea11e872d11bd2c557345baf24"
      }
    ]
  }
]
```

### kp_conclusion — Stereochemical conclusion proportional to evidence

冻结要求：Accept supported, contradicted or well-demonstrated unresolved local explanations. Do not infer a rate ratio from arbitrary endpoint G, equate70% recycling yield with single-pass selectivity, or claim an optimized acid protocol outside the source sequence. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：当前稳定性与有限时选择性不可唯一推断问题已闭合，未声称作者未计算的质子化TS或实测速率。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "No physical protonolysis barrier/rate or acid-face mechanism is inferred."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main physical6; SI21/71",
    "actual_result": "可靠结论是trans端点热力学更稳定且端点G不决定第二罐质子解单次比率；cis可通过该序列获得并靠再循环积累。不预测实际质子化面、酸优化、速率常数、产率或全构象总体。",
    "reason": "回答当前整个有界问题的稳定性与可推断范围两部分；不是以“未做”本身证明不可识别。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "8499f525a464335db0e096dc78cd1117627ce7942f962e5749c855a088a3f80e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/results/analysis_summary.json",
        "sha256": "f7c6f8ccc7a06c152c664eede3eca458b0f7d732baf5e33e385032f3e4dfc57b"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_4e9774f4128551d3/SOURCE_PAGES.json",
        "sha256": "c2991118fb5de379103eff53aa114c7848f19e847e760be0f86021c93ecb5ceb"
      }
    ]
  }
]
```

### conclusion_investigation — What molecular explanation of the stereochemical outcome of the reported 50 → silyl enol ether → ketoester sequence is supported by reproducible evidence, and how securely can that explanation be related to the experimental conditions?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list.

当前复审：当前稳定性与有限时选择性不可唯一推断问题已闭合，未声称作者未计算的质子化TS或实测速率。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Current endpoint rationale and its explanatory limits are substantively answered."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Main5–6; SI20–21/71–75",
    "actual_result": "同一53原子中性单重态50/trans与S20/cis的作者两层热化学路线给出正的G(S20)−G(50)：既有主路线2.641369354、联合G09Defaults控制2.633079954 kcal/mol；源2.3171919。这支持作者“trans产物更稳定”的约2.3 kcal/mol解释，与可逆酮烯醇条件只得trans的观察相容。该量沿用同对象、同定义已验收±1.0 kcal/mol范围；不将其用于绝对SCF能量或动力学误差。先转为O-TMS烯醇醚再于第二罐用外消旋CSA处理，可在非平衡反应过程中得到cis，但产物G不能决定单次1.1:1。已有12组满足详细平衡的条件动力学反例，在固定端点G时可给出30分钟T/C约0.1、1.1、10，证明端点稳定性对该比例的推断不唯一；这些是假设势垒模型，非实际酸解TS或对实验比例的拟合。单次1.1:1、Lewis酸/BINOL的3:1偏cis与三轮分离再循环70%是不同观察。纯MeOH连续介质不能冒充主文THF/MeOH1:1或SI10:1混合介质；酶/酸面机理、最优条件和精确产率均未声称。",
    "reason": "当前AR/PR科学问题由有效作者端点路线、相同定义容差与新增条件推论检验共同覆盖；允许有限解释不等于实际机理已求得。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/COORDINATOR_REVIEW_PACKAGE_20261007.json",
        "sha256": "5353d06967256ec92292a5cf7fbd5cb493071b76641619f71ee1a4b8843c82f3"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/results/analysis_summary.json",
        "sha256": "f7c6f8ccc7a06c152c664eede3eca458b0f7d732baf5e33e385032f3e4dfc57b"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/verified_computation_reference.md",
        "sha256": "cb0018b889805e1804bb208b2c8445d44cdb42102f21e3fe79a19561d6d14e3f"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 8.33 小时；9 份计时日志/12 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 2,20 线程/进程；Gaussian %Mem=100GB,12000MB,16GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0008 · v2_execution_20260929/data/50_original_optfreq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_original_optfreq.log) | Gaussian:16102.8；Gaussian:10427.5 | 正常；正常 | {"threads":[2],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · v2_execution_20260929/data/S20_original_optfreq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_original_optfreq.log) | Gaussian:721.7；Gaussian:770.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0010 · v2_execution_20260929/data/50_original_sp.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_original_sp.log) | Gaussian:260.1 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0011 · v2_execution_20260929/data/S20_original_sp.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_original_sp.log) | Gaussian:262.5 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0023 · execution_jobs/job_804c8dd7298340348cacc04e51187501/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/stdout.log) | Gaussian:16102.8；Gaussian:10427.5 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[2],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0024 · gaussian_batch/author_structure_50_si_eps3263_pcm_sp/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/stdout.log) | Gaussian:260.1 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0025 · gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/stdout.log) | Gaussian:721.7；Gaussian:770.6 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0026 · gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/stdout.log) | Gaussian:262.5 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0030 · native_cases/50/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/50/gaussian.log) | Gaussian:228.9 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0031 · native_cases/S20/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/S20/gaussian.log) | Gaussian:222.9 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0053 · native_cases/50/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/50/gaussian.log) | Gaussian:278 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0054 · native_cases/S20/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/S20/gaussian.log) | Gaussian:274.4 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0055 · source_endpoint_kinetic_witness/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0056 · source_endpoint_thermochemistry/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0057 · two_endpoints_GD3BJ_damping_control_SP/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/gaussian.log) | Gaussian:222.8；Gaussian:220.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

绝对高SP能与源相差约0.014Eh，未当作一致；相对G在原有同量标准内。；假设详细平衡模型不是实际分子酸解路径，不能声称1.1:1选择性被量化预测。

```json
[
  "Absolute SP energies differ from source by~0.014Eh but are not separate current observables; the relevant relativeG is tested at its inherited resolution. Acid-pathway matrix is retired/outside the required baseline."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Absolute high-level SCF energies are not source-matched; the inherited ±1 kcal/mol is only for the same relative thermochemical quantity.",
  "No actual protonolysis transition-state, kinetic ratio or isolated-yield prediction is certified. The 12 kinetic examples are conditional counterexamples, not physical rate calculations.",
  "Main THF/MeOH 1:1 versus SI 10:1 remains unresolved; pure methanol PCM is not asserted equivalent to the mixed reaction medium."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_4e9774f4128551d3.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_4e9774f4128551d3/verified_computation_reference.md)；SHA-256 `18e84f42f43a15fb34382f05ed3bdcf501cee735ad4a49dbac43ec878fc58eec`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_4e9774f4128551d3.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_4e9774f4128551d3.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_4e9774f4128551d3.json) | `7284bce110e6be814115e101135f293c4cdf994e89dc04b09acad7573524d6b7` | evidence_or_analysis |
| E0002 | [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_task.md) | `399a3257815ce71ca0a157a2a54b93107d578f9df5f5d1f1ac8f348f839c4fcc` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_reference_key_points.json) | `07a31a8d4026e2e4fc049b1a5630496ca3df0033c1b9934e2fd4c17fad76a16b` | historical_task_binding |
| E0004 | [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_reference_conclusions.json) | `bcef587d7ae42957a9c409741fffaf1836a8ec812fad61f1f694bfa5b4fb1416` | historical_task_binding |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_audit_2_native_readback.json) | `ef1f45e93e2e7a9a0b0956e810ff714a67de5072fbba619fa5fb56e2340249c1` | evidence_or_analysis |
| E0006 | [papers/paper_4e9774f4128551d3/documents/main.pdf](../../../../papers/paper_4e9774f4128551d3/documents/main.pdf) | `37a7fad866bff774d010cc6b61af21da2150a78c5bce69c1ff41574648c5b8b4` | source_document |
| E0007 | [papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf](../../../../papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf) | `64fda6d0c684c5c53ad4434788b2fe57bfa21ff63ec78215d47885b4103de76a` | source_document |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_original_optfreq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_original_optfreq.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `03a5b18fc6fbad7d57a1d9e78c48c321cc40e9b84530f68c278e72fbcd12e1f4` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_original_optfreq.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_original_optfreq.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `f41aed18706ecf8de85d2dd26f0c7c11c502ce5d280ec3bb275f4d0cb363ea90` | native_output |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_original_sp.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_original_sp.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `f38246161d1544c512adbc5eed2aae6ab124969a1d12fb15ad50ac48989a4375` | native_output |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_original_sp.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_original_sp.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `a000e90f1744228420e1085c6fd8d58413ed430c094e4368b3506f80c8d260dd` | native_output |
| E0012 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/results/analysis_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_analysis_summary.json) | `8499f525a464335db0e096dc78cd1117627ce7942f962e5749c855a088a3f80e` | evidence_or_analysis |
| E0013 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_analysis.py) | `ff0aa507b1eb62b10eba1ba71ea16ac15618f6c83cf85693e9e7216a9eee49df` | input_or_analysis_code |
| E0014 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/results/analysis_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_analysis_summary.json) | `f7c6f8ccc7a06c152c664eede3eca458b0f7d732baf5e33e385032f3e4dfc57b` | evidence_or_analysis |
| E0015 | [tasks/final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_scoring_rules.json) | `9b1be0e06b3d0e67ef93bef3ff7b560dfb73f0bae61a1918cecf445d19c7b840` | historical_task_binding |
| E0016 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/SOURCE_ROUTE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/SOURCE_ROUTE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_SOURCE_ROUTE_READBACK.json) | `5499229ee6c29b4fe41f68aa9b636acd5ecd9f0200527fe2702c13d59111aa0f` | evidence_or_analysis |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/NATIVE_REUSE_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/NATIVE_REUSE_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_NATIVE_REUSE_INTAKE.json) | `9ff8cc5a9deb08ab3b285b079de4c53655a938a58ea59f12e97813fbf4d2a42b` | evidence_or_analysis |
| E0018 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_COMPUTATION_COVERAGE.json) | `e37f9bf3a03edb3fadbda9420fd5dc3e9d885554c0611bad523db7ced3bad76e` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/INTENT_RECEIPT_RECONCILIATION.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_4e9774f4128551d3/INTENT_RECEIPT_RECONCILIATION.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_INTENT_RECEIPT_RECONCILIATION.json) | `9fb2efa386de2a0e1b8f99d63bb4e24a07f3d5905d17b5301bed6035cb66da3e` | evidence_or_analysis |
| E0020 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_4e9774f4128551d3.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_4e9774f4128551d3.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_paper_4e9774f4128551d3.md) | `497fb411879bfcc0e77e074f1903c139e1f5d59a06c2e3e1382350684520034b` | evidence_or_analysis |
| E0021 | [docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `cb0018b889805e1804bb208b2c8445d44cdb42102f21e3fe79a19561d6d14e3f` | historical_task_binding |
| E0022 | [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `cb0018b889805e1804bb208b2c8445d44cdb42102f21e3fe79a19561d6d14e3f` | historical_task_binding |
| E0023 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_native_excerpt.json) | `03a5b18fc6fbad7d57a1d9e78c48c321cc40e9b84530f68c278e72fbcd12e1f4` | native_output |
| E0024 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_native_excerpt.json) | `f38246161d1544c512adbc5eed2aae6ab124969a1d12fb15ad50ac48989a4375` | native_output |
| E0025 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_native_excerpt.json) | `f41aed18706ecf8de85d2dd26f0c7c11c502ce5d280ec3bb275f4d0cb363ea90` | native_output |
| E0026 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_native_excerpt.json) | `a000e90f1744228420e1085c6fd8d58413ed430c094e4368b3506f80c8d260dd` | native_output |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/integrated_inventory_and_kinetic_test_preparation_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/integrated_inventory_and_kinetic_test_preparation_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_integrated_inventory_and_kinetic_test_preparation_20260930.json) | `3a243e3f7157943d88764e96ee0a9bb5a8dcc7ea11e872d11bd2c557345baf24` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/model.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/model.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_model.json) | `d48685804341af2634951c9992ba74fc8eca159d306c5747705e8fbd49bd8e51` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_4e9774f4128551d3/SOURCE_PAGES.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_4e9774f4128551d3/SOURCE_PAGES.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_SOURCE_PAGES.json) | `c2991118fb5de379103eff53aa114c7848f19e847e760be0f86021c93ecb5ceb` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/50/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/50/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_native_excerpt.json) | `506b87b7f3b6addab51c579110c961f00ab30990c73f4faaf143713b8bb13777` | native_output |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/S20/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/S20/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_native_excerpt.json) | `67796080a4e44b6a067a29ee2001785823824cd978ecf77374a361c6b0207e8f` | native_output |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_grid_completed_same_definition_comparison_20261005/a01/results/Harziane_FineGrid_same_definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_grid_completed_same_definition_comparison_20261005/a01/results/Harziane_FineGrid_same_definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_Harziane_FineGrid_same_definition.json) | `6e3dd271a52eb58b851b58ef47affae950159d0de4bfdb25166389b1b833ad16` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/RAW_THERMAL_PRECISION_APPENDIX_20261007.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/RAW_THERMAL_PRECISION_APPENDIX_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_RAW_THERMAL_PRECISION_APPENDIX_20261007.json) | `5e51bdb41f0f7aad7321d45908908ec89f125b8ce36170827ec318ff8cdf70c1` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/COORDINATOR_REVIEW_PACKAGE_20261007.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/COORDINATOR_REVIEW_PACKAGE_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_COORDINATOR_REVIEW_PACKAGE_20261007.json) | `5353d06967256ec92292a5cf7fbd5cb493071b76641619f71ee1a4b8843c82f3` | evidence_or_analysis |
| E0035 | [tasks/final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_verified_computation_reference.md) | `cb0018b889805e1804bb208b2c8445d44cdb42102f21e3fe79a19561d6d14e3f` | historical_task_binding |
| E0036 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_task.md) | `4117c3b7f89924946131860689420ff583f89c6613139cdc45105738f8f8a495` | historical_task_binding |
| E0037 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_reference_key_points.json) | `07a31a8d4026e2e4fc049b1a5630496ca3df0033c1b9934e2fd4c17fad76a16b` | historical_task_binding |
| E0038 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_reference_conclusions.json) | `bcef587d7ae42957a9c409741fffaf1836a8ec812fad61f1f694bfa5b4fb1416` | historical_task_binding |
| E0039 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_scoring_rules.json) | `c087ee88ee671238bb2c05fab41e0a2a558bbbb6cabf81ace5bb261b72136073` | historical_task_binding |
| E0040 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_task.md) | `399a3257815ce71ca0a157a2a54b93107d578f9df5f5d1f1ac8f348f839c4fcc` | historical_task_binding |
| E0041 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_reference_key_points.json) | `07a31a8d4026e2e4fc049b1a5630496ca3df0033c1b9934e2fd4c17fad76a16b` | historical_task_binding |
| E0042 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_reference_conclusions.json) | `bcef587d7ae42957a9c409741fffaf1836a8ec812fad61f1f694bfa5b4fb1416` | historical_task_binding |
| E0043 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_scoring_rules.json) | `c087ee88ee671238bb2c05fab41e0a2a558bbbb6cabf81ace5bb261b72136073` | historical_task_binding |
| E0044 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7c388c58ce38b47e_G4.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7c388c58ce38b47e_G4.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_7c388c58ce38b47e_G4.json) | `7c388c58ce38b47e86e25cf2dffaf501baa1826a280e6620cd674fffadde9508` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G4.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G4.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_G4.json) | `7c388c58ce38b47e86e25cf2dffaf501baa1826a280e6620cd674fffadde9508` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e86110644d709d9a_paper_4e9774f4128551d3_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e86110644d709d9a_paper_4e9774f4128551d3_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_e86110644d709d9a_paper_4e9774f4128551d3_delivery_integrity.json) | `e86110644d709d9af131014650688e56860442edac4b8d214170ac701f6c161b` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_4e9774f4128551d3_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_4e9774f4128551d3_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_paper_4e9774f4128551d3_delivery_integrity.json) | `e86110644d709d9af131014650688e56860442edac4b8d214170ac701f6c161b` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/b656189a5be5badf_paper_4e9774f4128551d3_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/b656189a5be5badf_paper_4e9774f4128551d3_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_b656189a5be5badf_paper_4e9774f4128551d3_primary_pages.json) | `b656189a5be5badf824dc25c2f2dd90e0bc3601ca4f7566e1ebade822d0a7c5f` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_4e9774f4128551d3_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_4e9774f4128551d3_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_paper_4e9774f4128551d3_primary_pages.json) | `b656189a5be5badf824dc25c2f2dd90e0bc3601ca4f7566e1ebade822d0a7c5f` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e0e31b241c1751f6_G4_PA_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e0e31b241c1751f6_G4_PA_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_e0e31b241c1751f6_G4_PA_native_readback.json) | `e0e31b241c1751f622de318b4d83c8e8ec43abe8f39b5b8aaeb6013bb664450b` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/G4_PA_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/G4_PA_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_G4_PA_native_readback.json) | `e0e31b241c1751f622de318b4d83c8e8ec43abe8f39b5b8aaeb6013bb664450b` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/prior_decisions/paper_4e9774f4128551d3.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/prior_decisions/paper_4e9774f4128551d3.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_paper_4e9774f4128551d3.json) | `c3a23f7fc746caa181bf12bcfba25fb4a08693b51ea787756adcbe759fdeef29` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/50/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/50/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_native_excerpt.json) | `663e245954c51bb6da1a8619da8c8b5fa44575c314b37277d3befdb4a0dc2734` | native_output |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/S20/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/S20/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_native_excerpt.json) | `411720dca51827bedbdb3f6efcc18b9761c28258bf0fc81335fd38091f3fd4e2` | native_output |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_native_excerpt.json) | `b0c84c635fadf6a27169b45f88e8da561eabe6dcd9f16b71bae1e9f3a2adc510` | native_output |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_native_excerpt.json) | `8499f525a464335db0e096dc78cd1117627ce7942f962e5749c855a088a3f80e` | native_output |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_native_excerpt.json) | `9be07977ddfc52d618d42e22740a9d845c94e5fb661e35eb63b5f26bce266f5b` | native_output |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/reuse_audit/50_native.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/reuse_audit/50_native.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_50_native.json) | `ee440c566f0d31a00e325b92593fbdffcb7d067d99c9d109210f1be471fad13d` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/reuse_audit/S20_native.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/reuse_audit/S20_native.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_S20_native.json) | `ad0cbab20de0ead15b116645d7343cd12ca3b7bc6d559cb3231c24279c12a6c9` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/v2_source_evaluator_audit_20260929/batch4/work/papers/paper_4e9774f4128551d3/supplementary_001_selected.txt](../../../../docs/v2_verification/history/v2_source_evaluator_audit_20260929/batch4/work/papers/paper_4e9774f4128551d3/supplementary_001_selected.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_supplementary_001_selected.txt) | `e9616424f5d6adf45727831aeb4bbb2ec20878d7609137a9bd81a5c6cb61dbd4` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_submission.json) | `494a1e0b2132f13485a4b7ae26d7d9d1dc63dcefe398792043c5952b085f247c` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_status.json) | `a49f78b117443b1acf922215be675d415cd3bc6886e652e034a2dfede820dd08` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_analysis.py) | `1a8c1538f17d641a1dff3aef76848dd13b49db3a5b1f07d3fd57c3d55052276f` | input_or_analysis_code |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/inputs.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_inputs.json) | `3d89ec096e7ca84d5ede4e81a66c6ae84352ee57fa1940e48d93fb0de87b835d` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_submission.json) | `2a4f1cdf5d882aa87b35e08c1ee43928e626ee645ebca9c7be60fe166fb58f62` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_status.json) | `b9d1eb058e72491257bc7cfb052d1480db95995aad817a014d2bd03798b3cbaa` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_submission.json) | `dc3558e75f7cce36a0dc0361fef5e703306a57dbdc645595af1e84129cf2d0b6` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_status.json) | `22cee60c0b6d303b0fa6dfd0aabb3504f8031b183733668da16dc377d74c3efa` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/results/G09Defaults_source_comparison.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/results/G09Defaults_source_comparison.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_G09Defaults_source_comparison.json) | `e015b5c0dbe3a4b3e7d6b40395cb07ed96c84d39edaa6363791bfa93e9120efd` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/results/grid_control.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/results/grid_control.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_grid_control.json) | `9e792b07d85e2b86da0ef592e601efe31ba13699555195a8e6ab1da840b70142` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_identity_pair_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/50_identity_pair_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_50_identity_pair_audit.json) | `ee440c566f0d31a00e325b92593fbdffcb7d067d99c9d109210f1be471fad13d` | evidence_or_analysis |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_identity_pair_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/S20_identity_pair_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_S20_identity_pair_audit.json) | `ad0cbab20de0ead15b116645d7343cd12ca3b7bc6d559cb3231c24279c12a6c9` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_4e9774f4128551d3/PASS_CANDIDATE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_4e9774f4128551d3/PASS_CANDIDATE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_PASS_CANDIDATE.json) | `3ba97ffe0cc7d22c18f5ead1f670cc4fc709ecfc6e562db51e8f1635fbd684f6` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_AsymmetricIEFPCM_fixed_geometry_SP_20261006/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_AsymmetricIEFPCM_fixed_geometry_SP_20261006/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_submission.json) | `f17e521f8f5e8f71e5349bd76340fd5b532edab97a3db6db9c4e33ee0e0254d1` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_submission.json) | `3ed6ed5245eaf7e46523336c781725b6c73b3776355f7bf855fc68276a44ff89` | evidence_or_analysis |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_grid_completed_same_definition_comparison_20261005/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_grid_completed_same_definition_comparison_20261005/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_submission.json) | `d483f5f974d1a05e75309290da0da25d41eae1f702dc4bb11274b07cbbf175de` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/group4_strict_source_readback/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/group4_strict_source_readback/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_submission.json) | `0984463ce07e3ec8c0b8d9a9211bf9413a77d1b08fd6df63e14f849be9ec514c` | evidence_or_analysis |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_submission.json) | `0ec8e60935d951266c91cb2a8eda07711ad034abd555bbc79b00ceeb6948520d` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/native_workspace_batch/outputs/execution_jobs/job_804c8dd7298340348cacc04e51187501/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_input.com) | `ce19756e39703a537dc38047daf4d7e4c3363a60e1b0ac6baa8f4a1f1035b6c5` | input_or_analysis_code |
| E0080 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_50_si_eps3263_pcm_sp/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_input.com) | `1a8467353cdcfa79999f201229c1e6dfa8f8fe826a5f4c924bab8ceac8f97034` | input_or_analysis_code |
| E0081 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_s36_recovered_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_input.com) | `d5dd3c7d22a80cba18e5f6975a2f7a6e3eaadfcd38c12a81ec92902fa49b1600` | input_or_analysis_code |
| E0082 | [docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_4e9774f4128551d3/artifacts/gaussian_batch/author_structure_S20_si_eps3263_pcm_sp/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_input.com) | `6f155b7b2bb81e8c2c113ce9adce826936823a374e8b5e92bb6ad42c0d4b00b1` | input_or_analysis_code |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_binding.json) | `b57ab549cf0bc68d3818d2984e88cee121d623f4ae220e0282f16d0649bd315b` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/current_public_systems.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/data/current_public_systems.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_current_public_systems.json) | `2a9bff1903df4ace6adc7cb2152736e88b393cf516cc295e7b2cd046dcd77784` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/provenance/component_preparation.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/provenance/component_preparation.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_component_preparation.json) | `f449f925ea558a8551337362a06faabdd9753facaeda35876003791c10896114` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/author_inference_boundary_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/author_inference_boundary_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_author_inference_boundary_review_20260930.json) | `d5af030b12ee768f985ab2d45089a618b9a53378b0ef894bee4de2e8a62f3157` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/enol_TMS_E_THF_component_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/enol_TMS_E_THF_component_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_enol_TMS_E_THF_component_optfreq_sp.com) | `ae9c753d716dd761e4bfa126145f0751472c04820f06818591a48dc274ac5c96` | input_or_analysis_code |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/enol_TMS_Z_THF_component_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/enol_TMS_Z_THF_component_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_enol_TMS_Z_THF_component_optfreq_sp.com) | `06bba6c1abbb6e5637a5e70f192fc463cba2fb46c698b1e3ed66f7ab6dcf4996` | input_or_analysis_code |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/CSA_A_THF_component_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/CSA_A_THF_component_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_CSA_A_THF_component_optfreq_sp.com) | `ca38aaaa758ed0a6275c905f9aa9b88dc4e71654de939754f915dd91f90fac51` | input_or_analysis_code |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/CSA_B_THF_component_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/CSA_B_THF_component_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_CSA_B_THF_component_optfreq_sp.com) | `c988b2733a7537440d606bb9476e7ccd45da8058a80d85bad0a4f6bf471d6acc` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/methanol_THF_component_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/inputs/methanol_THF_component_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_methanol_THF_component_optfreq_sp.com) | `8560ce6ad08bf0e3aec42614d97da705969f6735e449f920b76f22d930c6c7ca` | input_or_analysis_code |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/50/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/50/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_input.com) | `a8c90cace0c874d8fab9695d515379f3969ce29a97a6fb8f440764168f66da7b` | input_or_analysis_code |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/S20/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09Defaults_toproute_nativefix_twoSP_20261006/a01/native_cases/S20/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_input.com) | `06ac08d7f07343f8e63f199203d3e5af1b4781ec4cecc99ed759cbb4d46e28c1` | input_or_analysis_code |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/G4_Br_PDens10_return_Harziane_full_evidence_20261007/a01/results/Harziane_full_source_native_review_bundle.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/G4_Br_PDens10_return_Harziane_full_evidence_20261007/a01/results/Harziane_full_source_native_review_bundle.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_Harziane_full_source_native_review_bundle.json) | `039c1e1ac5dc6afaea4221322c990f7240e3b866068e3c1096a00d85a34d55b0` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group4/HARZIANE_SOURCE_DECISION_ENTRY_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group4/HARZIANE_SOURCE_DECISION_ENTRY_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_HARZIANE_SOURCE_DECISION_ENTRY_20261007.json) | `09cad08846deb38aab2ba1a537b60f2a0fe027fc5da1f2b331849fb377ec8772` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group4/source_reread_20261003/paper_4e9774f4128551d3_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group4/source_reread_20261003/paper_4e9774f4128551d3_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_paper_4e9774f4128551d3_primary_pages.json) | `4e3cdbdbb3b3bc9ee4219fc0e4ff614ed37ae4ae2d7c4f5d5bbbb8c91f2c3ebd` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/conditional_kinetic_witness_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/conditional_kinetic_witness_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_conditional_kinetic_witness_review_20260930.json) | `8e5d2e5682e49d59b6d31c7ef97496fca6200e0542761f4ea9b3ebedadc6ec94` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/AUTHOR_COMPATIBILITY_RETURN_REVIEW_20261006.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/AUTHOR_COMPATIBILITY_RETURN_REVIEW_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0098_AUTHOR_COMPATIBILITY_RETURN_REVIEW_20261006.json) | `29b44fb95f91014b5a1a6327b90b5659fdc3e02dcc3cd8c9db9cae9e37d3ea06` | evidence_or_analysis |
| E0099 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_critical_failures.json) | `f9600e2547658652bb140d75d48f6b6c71724d21280561d7b3826a7765cb413b` | historical_task_binding |
| E0100 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_4e9774f4128551d3/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_package_manifest.json) | `22749666fd8acd3e8f62d11c832070a8ac05f4d2fed3a4a9b2c1fd5745278551` | historical_task_binding |
| E0101 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_critical_failures.json) | `f9600e2547658652bb140d75d48f6b6c71724d21280561d7b3826a7765cb413b` | historical_task_binding |
| E0102 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_4e9774f4128551d3/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0102_package_manifest.json) | `2ab1f26c51e6be3e6c01b8462469b097c43ae437f48aea96af272449922b41e5` | historical_task_binding |
| E0103 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_4e9774f4128551d3/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_4e9774f4128551d3/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_main.json) | `5c40cf54574024ae18e23505ef2639cbdc2869c138667949f0488149be4e081f` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_4e9774f4128551d3/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_4e9774f4128551d3/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_supplementary_001.json) | `939d3ab1a3a35b445ae55017b02939f095fd752d4e368320d99a5e33e6b4cd10` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/report/results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/report/results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_results.json) | `2116236a9481f7c5c058e725bb4c8360c97bbd2bdafd8c5346da55eea1a7faf8` | evidence_or_analysis |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/strict_controls_mirror_PTMA_readback/a01/results/4e_damping_control.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/strict_controls_mirror_PTMA_readback/a01/results/4e_damping_control.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0106_4e_damping_control.json) | `8eb2202a2e2a6378106806c0aab9e4d7c4fa44c66a649e4e27ff33a826c27fa9` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_4e9774f4128551d3_native_readback_0740Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_4e9774f4128551d3_native_readback_0740Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_paper_4e9774f4128551d3_native_readback_0740Z.json) | `0ccc324b28cbd5c164300c246739a24c157390bdab9a104a0dd75905010af56b` | evidence_or_analysis |
| E0108 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/paper_4e9774f4128551d3_76f302f8191ba7d52a000dc7bc36f17e8edb37e1fe8ed1d49937a9eeb07d25ca.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/paper_4e9774f4128551d3_76f302f8191ba7d52a000dc7bc36f17e8edb37e1fe8ed1d49937a9eeb07d25ca.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_paper_4e9774f4128551d3_76f302f8191ba7d52a000dc7bc36f17e8edb37e1fe8ed1d49937a9eeb07d25ca.json) | `76f302f8191ba7d52a000dc7bc36f17e8edb37e1fe8ed1d49937a9eeb07d25ca` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_20261002T0346Z/EPIMERIZATION_SOURCE_DISAGREEMENT_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_20261002T0346Z/EPIMERIZATION_SOURCE_DISAGREEMENT_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_EPIMERIZATION_SOURCE_DISAGREEMENT_READBACK.json) | `33737c87beb5925a112970175a3b0f47e162fde1c9a337fd2a35590dc94e5142` | evidence_or_analysis |
| E0110 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_original6_20261007T040006Z/HARZIANE_NATIVE_SOURCE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_original6_20261007T040006Z/HARZIANE_NATIVE_SOURCE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_HARZIANE_NATIVE_SOURCE_READBACK.json) | `66102ee0237126d8f388763146a03f47f175773d2a153c0f869b3c8976eb9e10` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/50/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/50/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0111_input.com) | `af8e49b5e7814f7588de43d8a0f449526158f27155861c5f84a81d1bec5704ab` | input_or_analysis_code |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/S20/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/G09_default_FineGrid_two_source_SP_20261005/a01/native_cases/S20/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_input.com) | `0e37541aeeab10f6f01b3d811fd0793a2e26c07a94d38fb37fa67e1d9fc0705b` | input_or_analysis_code |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_kinetic_witness/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/source_endpoint_thermochemistry/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0115_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_4e9774f4128551d3/v2_execution_20260929/outputs/two_endpoints_GD3BJ_damping_control_SP/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0116_input.com) | `7228393799905bcd4da00a4e4d2728b097685e5bd82063a31da3d174b4f32565` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REVIEWED_FOLLOWUP_WINDOW_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REVIEWED_FOLLOWUP_WINDOW_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_4e9774f4128551d3/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0117_REVIEWED_FOLLOWUP_WINDOW_20260930.json) | `3de07be5e6428385a87219a1411227baa8b83129b99009261d7313261d0f6605` | evidence_or_analysis |
| N0118 | [tasks/v2_autonomous_research/paper_4e9774f4128551d3/agent_input/task.md](../../../v2_autonomous_research/paper_4e9774f4128551d3/agent_input/task.md) | `4117c3b7f89924946131860689420ff583f89c6613139cdc45105738f8f8a495` | latest_review_evidence |
| N0119 | [tasks/v2_autonomous_research/paper_4e9774f4128551d3/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_4e9774f4128551d3/evaluation/reference_key_points.json) | `07a31a8d4026e2e4fc049b1a5630496ca3df0033c1b9934e2fd4c17fad76a16b` | latest_review_evidence |
| N0120 | [tasks/v2_autonomous_research/paper_4e9774f4128551d3/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_4e9774f4128551d3/evaluation/reference_conclusions.json) | `bcef587d7ae42957a9c409741fffaf1836a8ec812fad61f1f694bfa5b4fb1416` | latest_review_evidence |
| N0121 | [tasks/v2_autonomous_research/paper_4e9774f4128551d3/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_4e9774f4128551d3/evaluation/scoring_rules.json) | `c087ee88ee671238bb2c05fab41e0a2a558bbbb6cabf81ace5bb261b72136073` | latest_review_evidence |
| N0122 | [tasks/v2_autonomous_research/paper_4e9774f4128551d3/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_4e9774f4128551d3/evaluation/reference_validation_plan.md) | `08ab79c79c38bc0cbcc81f4377a3895839a5ac8561662c17f10b5f83e3312aeb` | latest_review_evidence |
| N0123 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_4e9774f4128551d3/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_4e9774f4128551d3/verified_computation_reference.md) | `ff5b561ef1f0950a13a4e5846d8103ddc43b544be9a22fbd883c4c9d6517b2cc` | latest_review_evidence |
| N0124 | [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json](scoring_rules.json) | `c087ee88ee671238bb2c05fab41e0a2a558bbbb6cabf81ace5bb261b72136073` | latest_review_evidence |
| N0125 | [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `08ab79c79c38bc0cbcc81f4377a3895839a5ac8561662c17f10b5f83e3312aeb` | latest_review_evidence |
| N0126 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_4e9774f4128551d3/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_4e9774f4128551d3/verified_computation_reference.md) | `18e84f42f43a15fb34382f05ed3bdcf501cee735ad4a49dbac43ec878fc58eec` | latest_review_evidence |
| N0127 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0128 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/agent_input/task.md](../agent_input/task.md) | `399a3257815ce71ca0a157a2a54b93107d578f9df5f5d1f1ac8f348f839c4fcc` |
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_key_points.json](reference_key_points.json) | `07a31a8d4026e2e4fc049b1a5630496ca3df0033c1b9934e2fd4c17fad76a16b` |
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_conclusions.json](reference_conclusions.json) | `bcef587d7ae42957a9c409741fffaf1836a8ec812fad61f1f694bfa5b4fb1416` |
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/scoring_rules.json](scoring_rules.json) | `c087ee88ee671238bb2c05fab41e0a2a558bbbb6cabf81ace5bb261b72136073` |
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/critical_failures.json](critical_failures.json) | `f9600e2547658652bb140d75d48f6b6c71724d21280561d7b3826a7765cb413b` |
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/evidence_map.json](evidence_map.json) | `e792b1b11eff99ce6392bc5db1a7387bfb7abfb8ce8073387c1f9c3850e43a3d` |
| [tasks/v2_paper_reproduction/paper_4e9774f4128551d3/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `08ab79c79c38bc0cbcc81f4377a3895839a5ac8561662c17f10b5f83e3312aeb` |

## Current scientific scoring policy — 2026-10-19

Active scoring is paper_science_v2: independent binary intermediate findings and final conclusions total 100. The synchronized JSON files replace historical process weights, partial-credit discretion and obsolete scoring freezes. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE and all recorded residuals/limitations remain; migration performs no new chemical validation. Public input, task_info.json and paper_route.md remain byte-identical. Source-versus-verification quantities are kept distinct; the new tolerances are fixed benchmark criteria, not fitted offsets. Historical reference-stage text above is provenance rather than the current runtime gate.


## Authorized public-contract and scientific-rule repair — 2026-10-19 round3

This repair preserves every preceding historical computation/acceptance statement verbatim. Current scoring remains paper_science_v2,100 independent scientific points. Mode-specific public objects now control AR eligibility; PR retains its disclosed source-baseline targets. Necessary experimental lifetime facts and obsolete process-score prose are repaired in public files where applicable. No source task, original paper, native computation, engine or historical acceptance is changed. Source/verification residuals and uncalibrated method-transfer limits remain; this is not a new chemical validation or online Judge result. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_02/paper_4e9774f4128551d3.md.

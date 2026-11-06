# Second expert review — 2026-10-28

Original PR numerical definitions and targets remain unchanged. Evidence covers reported twist basins, not every justified AR conformational family. Complete submissions may have empty decisions arrays; actual results, validations, successful operations and generated native artifacts remain required. No new scientific calculations were run.

# V3 final-result evidence reuse — 2026-10-28

Final de-duplication: the contraction comparison supports the 30-point framework explanation and has no separate score; the 20-point structural block and 25+25-point bonding explanations remain.

Same two complete isolated molecules, neutral singlets and first-oxidation doublets; molecular structural/electronic response only. Shared electronic and comparative final propositions carry identical weights; the inherited 20-point structure block is qualitative contraction in AR and four source-basin endpoint windows in PR.

r_contraction_nor/r_contraction_dtco (AR) and r_ss_nor_n/r_ss_nor_r/r_ss_dtco_n/r_ss_dtco_r (PR) reuse four BP86/TZVP minima: 4.056140073, 3.983239316, 3.688938805, 3.529845446 Å. The contraction comparison (0.072900758 versus 0.159093359 Å) supports r_framework_explanation without a separate ordering score. r_first_oxidation_bonding_nor/r_first_oxidation_bonding_dtco reuse mapped NPA/spin and same-geometry density/orbital analyses in native_reuse_verification.json; r_framework_explanation compares these responses within the tested local basins. All final propositions have existing relevant evidence, but have not been newly judged under V3.

Limitations: AR has no source-basin absolute distance window; PR retains four original ±0.02 Å windows for the disclosed twist basins. This pre-existing mode difference is retained explicitly rather than silently extending AR. Other radical conformations within 1–5 kcal/mol were not exhaustively ranked. BP86 is a GGA despite the main-text hybrid mislabel. Source absolute IP operator is unresolved and not scored. Paper_info publication date (2026-01-13) differs from PDF publication line (2026-01-14); DOI/title match.

The current policy is paper_science_v3 / final_results_100. The text below is an unchanged historical record; its old policies, scores and PASS labels are not current V3 certification. No new calculation was run.

---

# V2 验证计算参考：norDTCO/DTCO首氧化

论文：`paper_0de37d01e35c27df`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：现V2两框架首氧化比较已复现；V3 naph失败不属于本V2范围。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

两个给定框架中性→自由基阳离子的局部结构/电子响应，不含naph、二次氧化和绝对IP题目。

冻结题面中的科学目标：

How do norDTCO and DTCO respond at the molecular level to removal of one electron, and what account of their structural and electronic changes is supported? Determine how confidently the available molecular evidence distinguishes the behavior of the constrained and unconstrained frameworks.

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_0de37d01e35c27df/documents/main.pdf](../../../../papers/paper_0de37d01e35c27df/documents/main.pdf) | `0e7674491acb0b2565ea4dbec1dc37cad1a408c963344f839db245d3b7f85177` |
| [papers/paper_0de37d01e35c27df/documents/supplementary_001.pdf](../../../../papers/paper_0de37d01e35c27df/documents/supplementary_001.pdf) | `5db011e6236dc4acc437de3264214f79e39ea967de00ab8459a83934f55623a1` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

作者BP86/TZVP真实Opt/Freq与稳定性/NBO；四个最低点和同几何密度控制。

1. 核对 norDTCO/DTCO 两个完整骨架，分别建立中性 restricted singlet 与失一个电子的 unrestricted doublet；保证电荷、自旋、硫原子与其余原子映射一致。

2. 按 Gaussian BP86/TZVP 实际优化四个端点并计算频率，四者均有正频率；自由基另核电子稳定性、电子数和 S²。BP86 为 GGA，保留论文将其称为 hybrid 的术语错误而不改变计算方法。

3. 从原生优化几何直接计算 S···S：nor 中性/自由基 4.056140/3.983239 Å，DTCO 为 3.688939/3.529845 Å；收缩约 0.073/0.159 Å，与源 0.073/0.157 Å 同量比较。

4. 用实际保存密度重新读取电荷、自旋、成键指标及电子重排，区分固定核几何氧化和完全松弛氧化，检验结构收缩的电子解释；不得用单一距离或电荷建立全部因果。

5. 将受限/非受限骨架的不同响应作为最终分子结论。绝对电离能不属于当前必要量，不将其未认证支路或旧任务矩阵写成已完成的必要验证。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| 四端点S–S, Å | [4.056,3.983,3.687,3.53] | [4.056140073,3.983239316,3.688938805,3.529845446] | 实算−论文：[0.000140073,0.000239316,0.001938805,-0.000154554]； 本轮直接从四份原生日志最后坐标重算；最大误差0.00194Å远小于两框架收缩差0.086Å。；源定位：main Table1 p4 |
| 收缩nor/DTCO,Å | [0.073,0.157] | [0.072900758,0.159093359] | 实算−论文：[-9.9242e-05,0.002093359]； 符号与受限框架收缩较小均复现。；源定位：main p4 |
| S NPA响应,e | nor 0.17/0.15→0.50/0.49；DTCO0.13→0.48 | nor0.15408/0.17081→0.5078/0.5019；DTCO0.13275→0.48886 | 实算−论文：最大约0.012e； 同人口定义，与~0.34–0.36e变化相比很小；联合自旋/密度证据。；源定位：main Fig3邻文 |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| S···S neutral/radical, norDTCO (Å) | [4.056,3.983] | [4.05614,3.983239] | Same BP86/TZVP neutral versus radical local minima. Source distances agree at 0.001 Å reporting precision; native contraction is 0.072901 Å versus source 0.073 Å. |
| S···S neutral/radical, DTCO (Å) | [3.687,3.53] | [3.688939,3.529845] | Same molecular charge comparison with the native validated geometry. Neutral discrepancy 0.001939 Å is retained. The 0.159093 Å contraction versus source 0.157 Å is close relative to the distinct 0.073 Å nor response; positive-mode/tightened geometry evidence supports the same physical branch. No universal 0.002 Å threshold is asserted. |
| Sulfur NPA charges, neutral then radical (e) | {"nor":[0.17,0.15,0.5,0.49],"DTCO":[0.13,0.48]} | {"nor":[0.15408,0.17081,0.5078,0.5019],"DTCO":[0.13275,0.48886]} | Atom-mapped sulfur populations; nor neutral sulfur order is exchanged in source labels. Population magnitudes and oxidation redistribution agree; relaxed structure and partition dependence preclude last-digit scalar certification. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Verify norDTCO/DTCO graphs and stereochemical framework, neutral versus+1 electron counts and spin treatment. Do not insert a conventional sulfur–sulfur covalent edge merely to encode the expected radical answer.

冻结要求：Verify norDTCO/DTCO graphs and stereochemical framework, neutral versus+1 electron counts and spin treatment. Do not insert a conventional sulfur–sulfur covalent edge merely to encode the expected radical answer. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：26/20原子、q0 singlet/q+1 doublet守恒，未预置S–S普通共价键。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Correct norDTCO/DTCO graphs and neutral/+1 charge-spin/electron counts; no conventional S–S covalent edge inserted into identity."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S3/S4/S7/S8;mainmethodp9",
    "actual_result": {
      "nor": "C10H14S2,26atoms,106/105electrons,q0m1/q+1m2",
      "DTCO": "C6H12S2,20atoms,80/79electrons,q0m1/q+1m2",
      "sulfur_maps": "nor16/17;DTCOpublic1/5;fullgraphnoinsertedSSedge"
    },
    "reason": "CompleteelementgraphandmappedSidentitywith correctodd-electronradicals; sourceframework retained.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json",
        "sha256": "ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da",
        "bytes": 97295,
        "role": "Fourminima+tenfixedpoint electronicstates"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log",
        "sha256": "1d7e740146cb4474ae66a826c734ba1771a865e1cd0a9aa4a04dbc87e519a073",
        "bytes": 325079,
        "role": "RawGaussiannor_neutral"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log",
        "sha256": "ce1e282e4368fbcac1f12bbf19686f2851cdd3129b1796a61baa7679e5aaa42f",
        "bytes": 837638,
        "role": "RawGaussiannor_cation"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log",
        "sha256": "2d0a3ae85bf96ce699c9875a86fa3efd23ceeb79b67adef28c9033ece70e4fb7",
        "bytes": 267964,
        "role": "RawGaussianDTCO_neutral"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log",
        "sha256": "6545d7848c0be3c9f4aa008e11bcdfbf980426a0d00f49f283d5baf98784a8ce",
        "bytes": 5759413,
        "role": "RawGaussianDTCO_cation"
      }
    ]
  }
]
```

### kp_quantitative_evidence — Check genuine quantitative evidence of the neutral/radical response with correct electron count, atom mapping and energetic/electronic definitions. A sulfur separation alone cannot establish an electronic bonding account.

冻结要求：Check genuine quantitative evidence of the neutral/radical response with correct electron count, atom mapping and energetic/electronic definitions. A sulfur separation alone cannot establish an electronic bonding account. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：四份原始结构读回及72/72/54/54正频率闭合。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Distances, sulfur charges/spins, frontier occupation change and independent Mayer/Lowdin/NAO checks go beyond geometric contraction."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainp4Table1/Fig3;SIcoordtables",
    "actual_result": {
      "distance_rows": {
        "nor_neutral": 4.056140073290493,
        "nor_cation": 3.9832393155985497,
        "DTCO_neutral": 3.6889388047419547,
        "DTCO_cation": 3.5298454461313176
      },
      "Mayer_neutral_radical": {
        "nor": [
          0.0019298724165925957,
          0.289272111553902
        ],
        "DTCO": [
          -0.008096715181000493,
          0.28847395982104584
        ]
      },
      "NAOWiberg_neutral_radical": {
        "nor": [
          0.0049,
          0.1569
        ],
        "DTCO": [
          0.0026,
          0.1549
        ]
      },
      "cationS2_before": [
        0.7515,
        0.7516
      ]
    },
    "reason": "Distancealone notusedasbondproof; actualnativeNPA/spin andindependentlycheckedmatrix/orbitalanalysis supportelectronicaccount. Negative/smallMayerneutralvalueisnot forcedpositive.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json",
        "sha256": "ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da",
        "bytes": 97295,
        "role": "Fourminima+tenfixedpoint electronicstates"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/sulfur_source_HOMO_LP_character_existingWF_20261003_a1/RESULT.json",
        "sha256": "ba5d29445a5981cf8587a0fb514077eb270051c4dc53f71e175951fd04d2ddc3",
        "bytes": 13036,
        "role": "HPC orbitalcharacter evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk",
        "sha256": "13c06340bd0ee702d9f7f0db09e11093be535406880874fc6a566c2c4b97dceb",
        "bytes": 11611697,
        "role": "Same-objectFCHK"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log",
        "sha256": "4ba9df937d559293fcd366e5562ef666985e551b31c6845e505e35c66f03f500",
        "bytes": 636760,
        "role": "NativeNBO/stability"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk",
        "sha256": "9850310ccb62435e1b9e92e9120fadedf3ec20dbca3feed47158e234de517153",
        "bytes": 6125708,
        "role": "Same-objectFCHK"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log",
        "sha256": "0a7b33f1d4b0f3df1d527b469eb47f6e1719376bbb9b91c896570f097cdf51b8",
        "bytes": 446272,
        "role": "NativeNBO/stability"
      }
    ]
  }
]
```

### kp_scientific_answer — Judge whether the chosen evidence supports an explanatory comparison of norDTCO and DTCO. No specific2c–3e assignment, population analysis or frozen-geometry operation is mandatory; justified alternative or unresolved descriptions receive appropriate credit.

冻结要求：Judge whether the chosen evidence supports an explanatory comparison of norDTCO and DTCO. No specific2c–3e assignment, population analysis or frozen-geometry operation is mandatory; justified alternative or unresolved descriptions receive appropriate credit. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：硫自由基自旋、NPA、前线轨道与同几何密度支持弱离域2c–3e相容描述。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "The native contractions reproduce the source constrained/unconstrained distinction; same-nuclei oxidation controls demonstrate an electronic response independent of subsequent geometry relaxation."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainp4firstoxidation paragraphs/Fig3;sourceconformerlimitation",
    "actual_result": "In these two verified first-oxidation molecularbasins, removing one electron produces sulfur-centered radical character and a modest transannular contraction in both frameworks. norDTCO contracts4.056140→3.983239Å (0.072901Å); DTCO contracts3.688939→3.529845Å (0.159093Å), reproducing the source distinction that the constrained frameworkrelaxesless. Both have sulfur NPAcharges rising fromabout0.15–0.17/0.13 toabout0.50/0.49 and sulfur spin concentrated overthepair (nor0.44156/0.41792,DTCO0.44492/0.44492). Source-directedfrontierorbitalinspection finds sulfur-dominant HOMO/HOMO−1 with opposingS–Soverlaps, and same-geometry density controls show removalofaboutoneelectron fromthecation-UNOprojection:1.995→1.000. Mayer/NAOWiberg indices increasein both. This supports a weak,delocalized two-center/three-electron-compatible response ratherthan a uniqueordinarycovalentS–Sbond. The stronger DTCOstructuralrelaxation is robustwithin these basins; similarverticalelectronicresponse warnsagainst treatingdifferentcontraction alone asaqualitativelydifferentbond. Otherconformers werenotexhaustivelyranked;source notes1–5kcal/mol alternatives. AbsoluteIP,secondoxidation,electrodepotentials andproteinratesare notinferred.",
    "reason": "Bothframeworks actuallycomputed; directionandrelativecontractiontracksource; densitycontrolsseparategeometryrelaxation fromelectronremoval.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json",
        "sha256": "ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da",
        "bytes": 97295,
        "role": "Fourminima+tenfixedpoint electronicstates"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/sulfur_source_HOMO_LP_character_existingWF_20261003_a1/RESULT.json",
        "sha256": "ba5d29445a5981cf8587a0fb514077eb270051c4dc53f71e175951fd04d2ddc3",
        "bytes": 13036,
        "role": "HPC orbitalcharacter evidence"
      }
    ]
  }
]
```

### kp_validity_and_uncertainty — Use appropriate electronic and structural evidence for the level of bonding or oxidation claim. Distinguish vertical and adiabatic ionization and orbital-energy proxies, define spin and population conventions, and assess relevant uncertainty. If a state or conformer is said to be preferred, justify that claim within the explored space.

冻结要求：Use appropriate electronic and structural evidence for the level of bonding or oxidation claim. Distinguish vertical and adiabatic ionization and orbital-energy proxies, define spin and population conventions, and assess relevant uncertainty. If a state or conformer is said to be preferred, justify that claim within the explored space. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：仅认可所检验构象盆地；IP、轨道能代理、S–S距离不是同一个量。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Four minima and stable doublets are established. Populations and weak bonding interpretations remain definition-dependent; no global conformer preference or source-table IP operation is invented."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainp4Table1,p9method;sourceconformersp4",
    "actual_result": {
      "actualminima": "nor72/72positive modes;DTCO54/54positive modes",
      "minimum_cm1": [
        60.6081,
        47.8821,
        104.3185,
        108.8787
      ],
      "energydefinitions": "VerticalatRneutral/adiabaticateachminimum/ZPEcorrection/orbitalproxy distinct",
      "parentstable": "all10FCHKstatesstabilitychecked",
      "scope": "No globalconformerpreferenceclaim; unknownsourceIPoperation explicitlyexcluded fromcalibration"
    },
    "reason": "TrueOptsteps andfrequencycurvaturebothverified. Populationdefinition-dependentbondindices donotassignintegerbonds. IPdefectdoesnotinvalidateindependentobservables used.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json",
        "sha256": "ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da",
        "bytes": 97295,
        "role": "Fourminima+tenfixedpoint electronicstates"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log",
        "sha256": "1d7e740146cb4474ae66a826c734ba1771a865e1cd0a9aa4a04dbc87e519a073",
        "bytes": 325079,
        "role": "RawGaussiannor_neutral"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log",
        "sha256": "ce1e282e4368fbcac1f12bbf19686f2851cdd3129b1796a61baa7679e5aaa42f",
        "bytes": 837638,
        "role": "RawGaussiannor_cation"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log",
        "sha256": "2d0a3ae85bf96ce699c9875a86fa3efd23ceeb79b67adef28c9033ece70e4fb7",
        "bytes": 267964,
        "role": "RawGaussianDTCO_neutral"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log",
        "sha256": "6545d7848c0be3c9f4aa008e11bcdfbf980426a0d00f49f283d5baf98784a8ce",
        "bytes": 5759413,
        "role": "RawGaussianDTCO_cation"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W06/papers/paper_0de37d01e35c27df/outputs/W06_native_definition_diagnostic_20261006_a1/RESULT.json",
        "sha256": "ea1bcd062afe2891723707ce6caed6115cae778bfb238f2d04596c1b6b4a57b5",
        "bytes": 27106,
        "role": "raw or derived native evidence"
      }
    ]
  }
]
```

### kp_bounded_conclusion — Limit the account to these two finite molecular first-oxidation systems. Do not infer dication bonding, potential inversion, condensed-phase electrode potentials or protein electron-transfer rates solely from these results.

冻结要求：Limit the account to these two finite molecular first-oxidation systems. Do not infer dication bonding, potential inversion, condensed-phase electrode potentials or protein electron-transfer rates solely from these results. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：现V2两框架首氧化比较已复现；V3 naph失败不属于本V2范围。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Limited to first oxidation of these two finite molecules; no dication, inversion, solution electrode or protein electron-transfer claim."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "V2finitefirstoxidationboundary",
    "actual_result": "In these two verified first-oxidation molecularbasins, removing one electron produces sulfur-centered radical character and a modest transannular contraction in both frameworks. norDTCO contracts4.056140→3.983239Å (0.072901Å); DTCO contracts3.688939→3.529845Å (0.159093Å), reproducing the source distinction that the constrained frameworkrelaxesless. Both have sulfur NPAcharges rising fromabout0.15–0.17/0.13 toabout0.50/0.49 and sulfur spin concentrated overthepair (nor0.44156/0.41792,DTCO0.44492/0.44492). Source-directedfrontierorbitalinspection finds sulfur-dominant HOMO/HOMO−1 with opposingS–Soverlaps, and same-geometry density controls show removalofaboutoneelectron fromthecation-UNOprojection:1.995→1.000. Mayer/NAOWiberg indices increasein both. This supports a weak,delocalized two-center/three-electron-compatible response ratherthan a uniqueordinarycovalentS–Sbond. The stronger DTCOstructuralrelaxation is robustwithin these basins; similarverticalelectronicresponse warnsagainst treatingdifferentcontraction alone asaqualitativelydifferentbond. Otherconformers werenotexhaustivelyranked;source notes1–5kcal/mol alternatives. AbsoluteIP,secondoxidation,electrodepotentials andproteinratesare notinferred.",
    "reason": "No dication/inversion/electrode/kinetic/proteinextrapolation; noordinarybondlabel encoded.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json",
        "sha256": "ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da",
        "bytes": 97295,
        "role": "Fourminima+tenfixedpoint electronicstates"
      }
    ]
  }
]
```

### bounded_answer — A source-bounded evidence-supported answer to: How do norDTCO and DTCO respond at the molecular level to removal of one electron, and what account of their structural and electronic changes is supported? Determine how confidently the available molecular evidence distinguishes the behavior of the constrained and unconstrained frameworks.

冻结要求：Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. Limit the account to these two finite molecular first-oxidation systems. Do not infer dication bonding, potential inversion, condensed-phase electrode potentials or protein electron-transfer rates solely from these results.

当前复审：现V2两框架首氧化比较已复现；V3 naph失败不属于本V2范围。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "The source structural response and sulfur-centered electronic change are reproduced within the stated molecular comparison."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainTable1/Fig3;currentV2twoframeworkquestion",
    "actual_result": "In these two verified first-oxidation molecularbasins, removing one electron produces sulfur-centered radical character and a modest transannular contraction in both frameworks. norDTCO contracts4.056140→3.983239Å (0.072901Å); DTCO contracts3.688939→3.529845Å (0.159093Å), reproducing the source distinction that the constrained frameworkrelaxesless. Both have sulfur NPAcharges rising fromabout0.15–0.17/0.13 toabout0.50/0.49 and sulfur spin concentrated overthepair (nor0.44156/0.41792,DTCO0.44492/0.44492). Source-directedfrontierorbitalinspection finds sulfur-dominant HOMO/HOMO−1 with opposingS–Soverlaps, and same-geometry density controls show removalofaboutoneelectron fromthecation-UNOprojection:1.995→1.000. Mayer/NAOWiberg indices increasein both. This supports a weak,delocalized two-center/three-electron-compatible response ratherthan a uniqueordinarycovalentS–Sbond. The stronger DTCOstructuralrelaxation is robustwithin these basins; similarverticalelectronicresponse warnsagainst treatingdifferentcontraction alone asaqualitativelydifferentbond. Otherconformers werenotexhaustivelyranked;source notes1–5kcal/mol alternatives. AbsoluteIP,secondoxidation,electrodepotentials andproteinratesare notinferred.",
    "reason": "Entirepresentproblem supportedusingoldnor andcompletednewDTCO/electronicproof. UndefinedexternalIPisexplicitlynotusedtoexplainfirstoxidationresponse.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json",
        "sha256": "ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da",
        "bytes": 97295,
        "role": "Fourminima+tenfixedpoint electronicstates"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/sulfur_source_HOMO_LP_character_existingWF_20261003_a1/RESULT.json",
        "sha256": "ba5d29445a5981cf8587a0fb514077eb270051c4dc53f71e175951fd04d2ddc3",
        "bytes": 13036,
        "role": "HPC orbitalcharacter evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log",
        "sha256": "1d7e740146cb4474ae66a826c734ba1771a865e1cd0a9aa4a04dbc87e519a073",
        "bytes": 325079,
        "role": "RawGaussiannor_neutral"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log",
        "sha256": "ce1e282e4368fbcac1f12bbf19686f2851cdd3129b1796a61baa7679e5aaa42f",
        "bytes": 837638,
        "role": "RawGaussiannor_cation"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log",
        "sha256": "2d0a3ae85bf96ce699c9875a86fa3efd23ceeb79b67adef28c9033ece70e4fb7",
        "bytes": 267964,
        "role": "RawGaussianDTCO_neutral"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log",
        "sha256": "6545d7848c0be3c9f4aa008e11bcdfbf980426a0d00f49f283d5baf98784a8ce",
        "bytes": 5759413,
        "role": "RawGaussianDTCO_cation"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 2.03 小时；15 份计时日志/30 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,20 线程/进程；Gaussian %Mem=12000MB,12GB,70GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0002 · outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log) | Gaussian:86.1；Gaussian:525 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0003 · outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log) | Gaussian:1338.5；Gaussian:797.3 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0004 · outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log) | Gaussian:414.2；Gaussian:290.2 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log) | Gaussian:50；Gaussian:306.8 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:398.2；Gaussian:19.6 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:249.8；Gaussian:15.4 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0055 · outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:639.8；Gaussian:23.4 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0056 · outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:487.6；Gaussian:38.4 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0057 · outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:335.4；Gaussian:19.1 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0058 · outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:179；Gaussian:8.5 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0059 · outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:243.4；Gaussian:14.7 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0060 · outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log) | Gaussian:227.6；Gaussian:12.8 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0061 · outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log) | Gaussian:285.4；Gaussian:8.6 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0062 · outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log) | Gaussian:223.6；Gaussian:16.3 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0063 · outputs/DTCO_literal_SI4_neutral_verticalcation_BP86TZVP_reference_20261002_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/DTCO_literal_SI4_neutral_verticalcation_BP86TZVP_reference_20261002_a1/stdout.log) | Gaussian:31.4；Gaussian:37.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["70GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

源绝对DFT IP和某孤对分裂未复现，不可称全部论文数值一致。；未全球排序其他构象，不含二价离子、反转电势或蛋白速率。

```json
[
  "Source DFT IP 8.968/8.964 eV does not reproduce native vertical ΔSCF 7.5325/7.6471 eV; the source operation is unresolved and exact IP matching is outside the required structural/electronic comparison.",
  "Only explored local conformers are certified.",
  "Two-center/three-electron-compatible is a bounded description, not a unique localized-bond proof."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Source absolute DFT ionization potentials and the exact DTCO lone-pair splitting are not reproduced; vertical, adiabatic, ZPE and orbital proxies remain distinct.",
  "Local basins are validated; all radical conformers are not globally ranked, and the source's 1–5 kcal/mol alternatives remain relevant.",
  "Population-dependent bond indices do not establish a unique ordinary covalent S–S bond or an integer bond order.",
  "Dication chemistry, potential inversion, solution electrode potentials and protein electron-transfer rates are not certified."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_0de37d01e35c27df.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0de37d01e35c27df/verified_computation_reference.md)；SHA-256 `de368b09cb39e639bd39e973300cb8897cd255aad0eeeb8315e66f2c8812d7f5`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_0de37d01e35c27df.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_0de37d01e35c27df.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_0de37d01e35c27df.json) | `a356b0e0baf00adc6835bd027cf050a58adbbb7007708e4af1e6b818cbce4c9c` | evidence_or_analysis |
| E0002 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_native_excerpt.json) | `1d7e740146cb4474ae66a826c734ba1771a865e1cd0a9aa4a04dbc87e519a073` | native_output |
| E0003 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_native_excerpt.json) | `ce1e282e4368fbcac1f12bbf19686f2851cdd3129b1796a61baa7679e5aaa42f` | native_output |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `2d0a3ae85bf96ce699c9875a86fa3efd23ceeb79b67adef28c9033ece70e4fb7` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `6545d7848c0be3c9f4aa008e11bcdfbf980426a0d00f49f283d5baf98784a8ce` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `4ba9df937d559293fcd366e5562ef666985e551b31c6845e505e35c66f03f500` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `0a7b33f1d4b0f3df1d527b469eb47f6e1719376bbb9b91c896570f097cdf51b8` | native_output |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/analysis/native_reuse_verification.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_native_reuse_verification.json) | `ed57869dfde483a0220dd11a5974adaff89a4f2daee8f004d75ae28537b7f8da` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/a1b4b9e9f3e13b39_paper_0de37d01e35c27df_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/a1b4b9e9f3e13b39_paper_0de37d01e35c27df_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_a1b4b9e9f3e13b39_paper_0de37d01e35c27df_primary_pages.json) | `a1b4b9e9f3e13b394d3fa7cafd92c6e81eb5de8559e4dba8b11828c9402163ed` | evidence_or_analysis |
| E0010 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_task.md) | `9806a909a40ef75f643357eb4fb915e5064fed45115cbceb170fd98d69e68ac6` | historical_task_binding |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_reference_key_points.json) | `55a51955f70aa7458af807b2a43c5e9917901752a2d5d2dd51fc8b3508fe62e0` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_reference_conclusions.json) | `36993afde3258dd81122ba84f822eb540f8a41e61a3bc013cd6c9aaa70fbbba4` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_task.md) | `81dc1c81187facaf7718f9be75b5e0f054191070b7f1e30bc95b662c3c1ad927` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_reference_key_points.json) | `55a51955f70aa7458af807b2a43c5e9917901752a2d5d2dd51fc8b3508fe62e0` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_reference_conclusions.json) | `36993afde3258dd81122ba84f822eb540f8a41e61a3bc013cd6c9aaa70fbbba4` | historical_task_binding |
| E0016 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_NATIVE_READBACK.json) | `b2fef5f52a0da5d8f0bf864c5b8de2f7d4afd45f8c27414f041ec56902fea626` | evidence_or_analysis |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_COMPUTATION_INVENTORY.json) | `c8ce4ea798980885afdcf6d0ea1661265b6259c747e2f6bb85cc2079e0e11374` | evidence_or_analysis |
| E0018 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_0de37d01e35c27df.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_0de37d01e35c27df.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0018_paper_0de37d01e35c27df.md) | `ce80904dbedd1a51b7d2067d849fe2f6dc65e234a7ac42c9d7d0b319d700b612` | evidence_or_analysis |
| E0019 | [docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `f5dcbea5df05b0a9134105460e7a4afd1c1b3bdf0a9d494caa76d02df0a5388d` | historical_task_binding |
| E0020 | [docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `5373963fe0fa0d04f715860384e6eefa6752929a14c16774ebd76618e69b86ce` | historical_task_binding |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/sulfur_source_HOMO_LP_character_existingWF_20261003_a1/RESULT.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/sulfur_source_HOMO_LP_character_existingWF_20261003_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_RESULT.json) | `ba5d29445a5981cf8587a0fb514077eb270051c4dc53f71e175951fd04d2ddc3` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `13c06340bd0ee702d9f7f0db09e11093be535406880874fc6a566c2c4b97dceb` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `9850310ccb62435e1b9e92e9120fadedf3ec20dbca3feed47158e234de517153` | evidence_or_analysis |
| E0024 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W06/papers/paper_0de37d01e35c27df/outputs/W06_native_definition_diagnostic_20261006_a1/RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W06/papers/paper_0de37d01e35c27df/outputs/W06_native_definition_diagnostic_20261006_a1/RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_RESULT.json) | `ea1bcd062afe2891723707ce6caed6115cae778bfb238f2d04596c1b6b4a57b5` | evidence_or_analysis |
| E0025 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_scoring_rules.json) | `e0cad21a2854ecb7fa52fdb50507c23de6464574c1a27be7911c48ce314776c1` | historical_task_binding |
| E0026 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_scoring_rules.json) | `e0cad21a2854ecb7fa52fdb50507c23de6464574c1a27be7911c48ce314776c1` | historical_task_binding |
| E0027 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/fdb7c12c0438d47b_W06.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/fdb7c12c0438d47b_W06.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_fdb7c12c0438d47b_W06.json) | `fdb7c12c0438d47b5d9f465f829e66d337e9711b089d44108138c033d67c2a91` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W06.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W06.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_W06.json) | `fdb7c12c0438d47b5d9f465f829e66d337e9711b089d44108138c033d67c2a91` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/45070b991c5f0745_paper_0de37d01e35c27df_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/45070b991c5f0745_paper_0de37d01e35c27df_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_45070b991c5f0745_paper_0de37d01e35c27df_delivery_integrity.json) | `45070b991c5f0745d55eb897af4bcfe32b9daff371d031b93445740a441db8b1` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0de37d01e35c27df_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0de37d01e35c27df_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_paper_0de37d01e35c27df_delivery_integrity.json) | `45070b991c5f0745d55eb897af4bcfe32b9daff371d031b93445740a441db8b1` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0de37d01e35c27df_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0de37d01e35c27df_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_paper_0de37d01e35c27df_primary_pages.json) | `a1b4b9e9f3e13b394d3fa7cafd92c6e81eb5de8559e4dba8b11828c9402163ed` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/6e77c7ad14eedde0_paper_0de37d01e35c27df_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/6e77c7ad14eedde0_paper_0de37d01e35c27df_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_6e77c7ad14eedde0_paper_0de37d01e35c27df_native_readback.json) | `6e77c7ad14eedde0d8def2be04c48f01eeebd57554102ba0a5ad1738d5f3598b` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0de37d01e35c27df_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_0de37d01e35c27df_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_paper_0de37d01e35c27df_native_readback.json) | `6e77c7ad14eedde0d8def2be04c48f01eeebd57554102ba0a5ad1738d5f3598b` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_neutral_BP86_TZVP_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_input.com) | `7e290f2cacd0387eadf46730e9010c8e5bdce5a87f166f0db8ac3be095f3edee` | input_or_analysis_code |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/legacy_nor_cation_BP86_TZVP_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_input.com) | `276c75560b840f02d039da1c84c9743afdad6c987eb9b68586f39584259b7750` | input_or_analysis_code |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_BP86_TZVP_strict_optfreq_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_input.com) | `d1c205b93656c41a8ec4b05de7146b5c2595795c3419a5fae603a673240a881c` | input_or_analysis_code |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_author_BP86_TZVP_optfreq_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_input.com) | `d8212c57c32fc8ad91f6d4160e0c136314aac735dce2ea86a3f83a81b5a63919` | input_or_analysis_code |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_cation_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_input.com) | `43e50439166c0c08170625fe1600ffdff70389a7e7cdc1134bf314c2147a3711` | input_or_analysis_code |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_cation_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_input.com) | `79faceaef59cdb58b736919d68b76e8bc4337ed309a91df0fc0672d1b711cb7f` | input_or_analysis_code |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `2e9e3f4bdc5093069ac577d119ede4a4884b8913bdb83931aa91171ae99d9a79` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `e289140207c89ad630ae1f8cef7676ca5ff0e4e71012dd577e5fcf9f6a5f8654` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `5202412344b5debc4af88290d67946886b54553457988766d1d1c800b626397a` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `e9de5cd63825299b0b3d93249dbeb400f3ad0af80a05087406fa3f2b7579316d` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `adacd8b7cffce46aef46dccf7292ae406c194bea9935d503919e768dc140faa1` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/calculation.fchk) | `f5a0b8fe36bb196884474a16f8a195f49886f5766f08935c37c05162b4daf1e0` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/calculation.fchk) | `6741b9d13773942b0c319998f7885996a3518ae21652611f533d61138ebcdd40` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/calculation.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/calculation.fchk) | `534fe9f5e2daa732f910834aebced20688dc2bf6f660c3eaa0e33b68d3f2a66c` | evidence_or_analysis |
| E0048 | [papers/paper_0de37d01e35c27df/documents/main.pdf](../../../../papers/paper_0de37d01e35c27df/documents/main.pdf) | `0e7674491acb0b2565ea4dbec1dc37cad1a408c963344f839db245d3b7f85177` | source_document |
| E0049 | [papers/paper_0de37d01e35c27df/documents/supplementary_001.pdf](../../../../papers/paper_0de37d01e35c27df/documents/supplementary_001.pdf) | `5db011e6236dc4acc437de3264214f79e39ea967de00ab8459a83934f55623a1` | source_document |
| E0050 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/sources/supplementary_001_method_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/sources/supplementary_001_method_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_supplementary_001_method_pages.json) | `0732f3ee3a86bfbd864b8e56464f0f6198a8a56a6a858e6480da3cdb1436b63d` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/sources/main_method_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0de37d01e35c27df/sources/main_method_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_main_method_pages.json) | `707f7e4312c9bb0fa91036813d0da11de3d2188b633f4dce09c06371c6c3a377` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0de37d01e35c27df/SCIENTIFIC_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0de37d01e35c27df/SCIENTIFIC_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_SCIENTIFIC_REVIEW.json) | `e0c2901d8b04a250b1cc9ef2b4726c8a74a886973f8603134b7e436c372f92ff` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/analysis/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1_orbital_arrays.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/analysis/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1_orbital_arrays.npz) | `ce446e298450383bb549b53748f21b81953c39b06a434e3439e0f13d5aa577d2` | evidence_or_analysis |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/analysis/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2_orbital_arrays.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/analysis/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2_orbital_arrays.npz) | `92a38721aaafb99789e48f380396888d43a38e46b31a585fa7f2526db3b5f79c` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_native_excerpt.json) | `935a7b2634ed156ceb6b1dabd03f21f19b2c576597b0dc7add7cc59efecc2dd8` | native_output |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_native_excerpt.json) | `aa1ee614195417c516ee56587ef72348db025739163420b8f3b2d08fb0843666` | native_output |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_native_excerpt.json) | `fa25a3898b0c33b1c544fdfcce144532502a18868cef3659e8234d692b514a3d` | native_output |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_native_excerpt.json) | `0b37e899b06e87a059f95ba77d28110837e73840b37c17a6661313c6db976314` | native_output |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_native_excerpt.json) | `578f70310e9b6506de1f2a301cd7bf6b2897a7c17e75a725ff54eb38b0a660fe` | native_output |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_native_excerpt.json) | `c7226c577507e48b32f6905fcfaa2cbf0194129a60e26e5211a720128b73f52f` | native_output |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_native_excerpt.json) | `b97ce3c8192316afc6449e7eb1ba1143cc6f0c61ef72335d2162ae916ed36fa7` | native_output |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_native_excerpt.json) | `6c94c75e5a4d6302176c5044759a416e8f471ecd3f8523de67a0c24ddca1b9b6` | native_output |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/DTCO_literal_SI4_neutral_verticalcation_BP86TZVP_reference_20261002_a1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_0de37d01e35c27df/outputs/DTCO_literal_SI4_neutral_verticalcation_BP86TZVP_reference_20261002_a1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0063_native_excerpt.json) | `201fe7cc5031c1d64ed9ef372b277f6ebe41d1e650f6873faad663da46f4e822` | native_output |
| E0064 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0de37d01e35c27df/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0064_critical_failures.json) | `84347bde4535d2e42f3e5de7595645ccb16f6e1102b8b4e80c869a07b3dc3c11` | historical_task_binding |
| E0065 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0de37d01e35c27df/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0065_critical_failures.json) | `84347bde4535d2e42f3e5de7595645ccb16f6e1102b8b4e80c869a07b3dc3c11` | historical_task_binding |
| E0066 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0de37d01e35c27df/SCIENTIFIC_REVIEW.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_0de37d01e35c27df/SCIENTIFIC_REVIEW.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_SCIENTIFIC_REVIEW.md) | `e91465188ad3ac570c85aab4a2037cc44c306b504093bc9acc0e531d1557fc19` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0067_input.com) | `4cd86094ea508ec37857d7d45ce1f28727d07421394837f7346ec6ef5517150e` | input_or_analysis_code |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_cation_on_neutral_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0068_input.com) | `c5e9ada02d7ee965f775a785f9627b7907ffe35bc3dc766155d1dfc165d5f822` | input_or_analysis_code |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/nor_neutral_on_cation_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_input.com) | `89f24e587768375d71f703f4d398ebe19b288b70fc9631cb1bf6966052791ec9` | input_or_analysis_code |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_neutral_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_input.com) | `e62a18d18449270b0f9adfbd1d795034ac8582bd583ed70b38714c1fdbbb55ed` | input_or_analysis_code |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_neutral_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0071_input.com) | `c510d95bd1eee5f457a74617cb8dcdbd43615251aaa93e785c78a2b74647d497` | input_or_analysis_code |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_cation_BP86_TZVP_stable_NBO_a1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_input.com) | `6a6c7302ad0f97e03ee5cf2436bedd6c0a5192a4b5b999430ab1347c7cf4c931` | input_or_analysis_code |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_neutral_on_refined_neutral_BP86_TZVP_stable_NBO_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_input.com) | `66c3c936ddeefb0211190dbdbb804698be986745397914bbf844e887b0b7835a` | input_or_analysis_code |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_3/papers/paper_0de37d01e35c27df/outputs/DTCO_cation_on_refined_neutral_BP86_TZVP_stable_NBO_a2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0de37d01e35c27df/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_input.com) | `8ec9ef07baa2e6fe2c7d2a04bdc6bd537936386f71280cadbe5c8c79e9832d1b` | input_or_analysis_code |
| N0075 | [tasks/v2_autonomous_research/paper_0de37d01e35c27df/agent_input/task.md](../agent_input/task.md) | `9806a909a40ef75f643357eb4fb915e5064fed45115cbceb170fd98d69e68ac6` | latest_review_evidence |
| N0076 | [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/reference_key_points.json](reference_key_points.json) | `55a51955f70aa7458af807b2a43c5e9917901752a2d5d2dd51fc8b3508fe62e0` | latest_review_evidence |
| N0077 | [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/reference_conclusions.json](reference_conclusions.json) | `36993afde3258dd81122ba84f822eb540f8a41e61a3bc013cd6c9aaa70fbbba4` | latest_review_evidence |
| N0078 | [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/scoring_rules.json](scoring_rules.json) | `e0cad21a2854ecb7fa52fdb50507c23de6464574c1a27be7911c48ce314776c1` | latest_review_evidence |
| N0079 | [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `b4d47583f6f82950af731cdb7f9c8e000cc3fece72aa1b2cc034c76bffcffbbc` | latest_review_evidence |
| N0080 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0de37d01e35c27df/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0de37d01e35c27df/verified_computation_reference.md) | `de368b09cb39e639bd39e973300cb8897cd255aad0eeeb8315e66f2c8812d7f5` | latest_review_evidence |
| N0081 | [tasks/v2_paper_reproduction/paper_0de37d01e35c27df/agent_input/task.md](../../../v2_paper_reproduction/paper_0de37d01e35c27df/agent_input/task.md) | `81dc1c81187facaf7718f9be75b5e0f054191070b7f1e30bc95b662c3c1ad927` | latest_review_evidence |
| N0082 | [tasks/v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_key_points.json) | `55a51955f70aa7458af807b2a43c5e9917901752a2d5d2dd51fc8b3508fe62e0` | latest_review_evidence |
| N0083 | [tasks/v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_conclusions.json) | `36993afde3258dd81122ba84f822eb540f8a41e61a3bc013cd6c9aaa70fbbba4` | latest_review_evidence |
| N0084 | [tasks/v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/scoring_rules.json) | `e0cad21a2854ecb7fa52fdb50507c23de6464574c1a27be7911c48ce314776c1` | latest_review_evidence |
| N0085 | [tasks/v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_validation_plan.md](../../../v2_paper_reproduction/paper_0de37d01e35c27df/evaluation/reference_validation_plan.md) | `b4d47583f6f82950af731cdb7f9c8e000cc3fece72aa1b2cc034c76bffcffbbc` | latest_review_evidence |
| N0086 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0de37d01e35c27df/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0de37d01e35c27df/verified_computation_reference.md) | `3c360c3c2efe7e946baa814afeac60e0e3c9a2615d8b4417223088134d043f98` | latest_review_evidence |
| N0087 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0088 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/agent_input/task.md](../agent_input/task.md) | `9806a909a40ef75f643357eb4fb915e5064fed45115cbceb170fd98d69e68ac6` |
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/reference_key_points.json](reference_key_points.json) | `55a51955f70aa7458af807b2a43c5e9917901752a2d5d2dd51fc8b3508fe62e0` |
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/reference_conclusions.json](reference_conclusions.json) | `36993afde3258dd81122ba84f822eb540f8a41e61a3bc013cd6c9aaa70fbbba4` |
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/scoring_rules.json](scoring_rules.json) | `e0cad21a2854ecb7fa52fdb50507c23de6464574c1a27be7911c48ce314776c1` |
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/critical_failures.json](critical_failures.json) | `84347bde4535d2e42f3e5de7595645ccb16f6e1102b8b4e80c869a07b3dc3c11` |
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/evidence_map.json](evidence_map.json) | `6c45ddf661cab3f705c614ed98a988ccca5a1c20d443d7f8d26e2ebd181eee26` |
| [tasks/v2_autonomous_research/paper_0de37d01e35c27df/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `b4d47583f6f82950af731cdb7f9c8e000cc3fece72aa1b2cc034c76bffcffbbc` |

## Current scoring policy — 2026-10-19

The active policy is paper_science_v2: independent intermediate scientific findings and final conclusions sum to 100; no process points, partial-credit discretion or multiplier applies. Active nodes, rules, PDF sources and fixed inclusive tolerances are in the synchronized JSON files. Historical evaluator IDs, weights, freezes and process language in the preceding archive are not current scoring instructions. The public task and PR author-route contract are unchanged. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE acceptance and its scientific limitations remain; this migration runs no new chemistry calculations and does not certify publication readiness.

## Round 3 scoring-contract repair — 2026-10-19

AR four source-twist endpoint leaves20 replaced by two molecular contraction leaves10+10. Original70/30 split retained; other conformer family qualifies only if actual contraction and electronic propositions are established. Existing chemical acceptance and all archived measurements/results above are unchanged. This is a contract/rubric repair with no new quantum calculations or online Judge certification. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_01/REPORT.md.

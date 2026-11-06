# 2026-10-28 二次审查（group_10）

局部热力学排序与结构关联有支持；PR只有298.15K条件重建数值窗内，273.15/313.15K三个值均超窗，源温度和动力学唯一性未认证。本轮只直接读源文、原生证据和必要算术核对；未新增计算，不继承历史PASS。逐命题覆盖及专家问题见本轮审查材料。

---

# 2026-10-28 V3范围与逐命题证据复用（group_10）

局限于6b/PhSO2Cl/Cu(acac)2/4CzIPN在MeCN、313.15 K下的局部氯化区域与Z立体选择性解释。AR独立选择物理模型；PR保留作者四个65原子中间体与源表自由能复现。四个结构及三个排序/几何项不再独立得分。保留原模式差异：AR三个最终命题40/40/20；PR对应28/28/20并保留三个源表数值各8分；两模式均100分。

- `r_regioselective_capture_account`：docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json：313.15 K相对C1ss为C3ss10.826133、C1sa2.348304、C3sa6.500419 kcal/mol；C1在两个立体家族均较低。released_outlet_identity_curvature_composite.json提供C–Cl1.903636 Å及C1–Cu断开，支持局部连接，不是势垒。
- `r_stereochemical_product_account`：docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json：同角色C2–C3–Cpropyl角121.317488/129.711905°；出口S/酯羰基高优先级取代基同侧、二面角−10.620089°。C1ss较C1sa低2.348304 kcal/mol（313.15 K）。已支持局部热力学/构型关联，不能唯一归因应变或推出产物比。
- `r_local_inference_limits`：docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json及outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json：三温排序一致、189正模出口；正文Scheme3的光/铜/自由基控制有参与性而非局部势垒辨识力。支持条件性解释及边界。

证据缺口：SI的G273.15标签及作者真实热化学温度未澄清；298.15 K数值重建不是作者笔误证明；局部出口有正曲率和成键身份，但没有支持唯一成键机制/精确选择比的竞争势垒；四个有限最低点不能认证全构象/自旋/配位系综；几何差异不是独立的应变能分解；V3语义判分及独立AR盲测未执行；历史严格局部验收不自动继承。本轮无新增量化计算、无重验证、无ARCHE盲测；历史PASS不自动继承。以下历史正文原样保留，历史评分描述不再是当前评分合同。

---

# V2 验证计算参考：Cu/联烯局部选择性

论文：`paper_db6c4e0558113873`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：全部源分量与两套温度结果共同支持条件重建；没有为单一目标调温。有限局部选择性结果实际恢复。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

四个allyl–CuIII中间体如何支持局部C–Cl形成的选择性解释及其限度。

冻结题面中的科学目标：

What molecular account of local C–Cl bond formation can explain the observed chlorosulfonylation selectivity of allenoate6b under the source photo/copper conditions, and what evidence limits that account?

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_db6c4e0558113873/documents/main.pdf](../../../../papers/paper_db6c4e0558113873/documents/main.pdf) | `9b9d8841f0eb5ec7561cb770ad3bd43d0820639e443412d5da1bc74842318c8c` |
| [papers/paper_db6c4e0558113873/documents/supplementary_001.pdf](../../../../papers/paper_db6c4e0558113873/documents/supplementary_001.pdf) | `a6585fbc4d364923517f436132456b23b012d972eeecb7a818a8a4259c1a6608` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

四个完整65原子对象，B3LYP-D3BJ低层OptFreq→M06/SMD MeCN高层单点；273.15/298.15/313.15 K热项实际控制。

1. 从作者 SI 核对四个完整 65 原子 Cu 模型，保留 E/Z 几何、配体、同一计量与电子态。源正文/表格温度标签冲突先登记，不能为配合数值悄改标签。

2. 实际完成作者 B3LYP-D3BJ 低层 Opt/Freq 与 M06/SMD MeCN 高层单点；低/高层电子及热项与 SI 在约 10⁻⁶ Eh 量级吻合，四个端点的最低点有效性由原生日志支持。

3. 对 273.15、298.15、313.15 K 分别重算热化学并只合并一次热校正。298.15 K 相对 G=[0,10.713284,2.293929,6.437268] kcal/mol 恢复 SI [0,10.712842,2.292292,6.435737]；313.15 K 的 [0,10.82613,2.34830,6.50042] 恢复正文 [0,10.8,2.3,6.5]。

4. 保留 273.15 K 按字面不能复原该表的事实；以实际三温计算区分数值重现与标签纠正，不声称原文所有温度标注自洽。核收已有 Z 局部出口的真实有效性证据。

5. 最终认证所述模型的局部反应/选择性证据及温度依赖的源解释；不将局部出口与几个端点当作完整催化循环、精确总体速率或无误差实验选择性。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| C1 synanti−synsyn ΔG (kcal/mol) | 2.3 | {"273.15":2.203666540117588,"298.15":2.2939293511099166,"313.15":2.3483035717846406} | 同65原子,q0/singlet; E_M06,SMD+Gcorr_B3LYP-D3BJ;分别273.15/298.15/313.15K。 Three explicitly chosen temperatures independently give 2.203667/2.293929/2.348304. SourceTableS1 thermal/electronic components agree with the298.15K native column while the main figure is consistent with313.15K. The finite conditional ordering and source local explanation survive all three. Neither this agreement nor the old ±1 benchmark band certifies the SI273.15 label; no tolerance is adopted from that old band. |
| C3 competing intermediates ΔG relative C1synsyn (kcal/mol) | {"main":{"C3_synsyn":10.8,"C3_synanti":6.5},"SI_table":{"C3_synsyn":10.712841741266955,"C3_synanti":6.435737166007901}} | [{"T_K":273.15,"relative":{"C1_synsyn":0.0,"C3_synsyn":10.525321858793125,"C1_synanti":2.203666540117588,"C3_synanti":6.331719446295429}},{"T_K":298.15,"relative":{"C1_synsyn":0.0,"C3_synsyn":10.713284434103516,"C1_synanti":2.2939293511099166,"C3_synanti":6.437267971023323}},{"T_K":313.15,"relative":{"C1_synsyn":0.0,"C3_synsyn":10.826133492355323,"C1_synanti":2.3483035717846406,"C3_synanti":6.500418990567126}}] | 作者四模型同共同零点；C3新增实算。 All four source geometries and high-level electronic/thermal components were separately reproduced. At298.15K the two C3 source-table relative-energy residuals are +0.000443/+0.001531kcal/mol; at313.15K the main10.8/6.5 values are reproduced as10.826133/6.500419. These are separate comparisons, not an inferred common temperature. |
| Source panel angles/dihedrals (degree) | {"angles":[123.7,129.7],"dihedrals":[-6.1,13.1]} | {"panel_angles":[123.73190079047063,129.71190518794643],"panel_dihedrals":[-6.19814756149057,13.061533097681872],"fixed_propyl_angles":[121.31748829129602,129.71190518794643]} | 两个panel的C4分别ester-carbonyl/propyl；固定chemical-role另外列。 Panel-specific atom mapping precedes comparison: angular residuals are +0.031901/+0.011905deg and dihedral residuals -0.098148/-0.038467deg. Source panelC4 has different chemical roles. These small source-coordinate reproduction differences support geometric association only; no assigned strain energy or inherited ±3deg gate. |
| CCl outlet geometry / curvature | 未给出／不适用 | {"CCl_A":1.9036360599140265,"CS_A":1.8062792238593677,"alkene_CC_A":1.3461710200487158,"positive_modes":189,"Opt_fourYES":true,"postFreq_max_displacement_NO":true} | 当前题的附加局部成键验证；不是源reported barrier。 原Opt完成+正曲率+同库存graph核收；postFreq预测位移NO保留，未被用于宣布新的数值阈值或动力学完成。；这是保留的非必要源差异，不作为已复现量。 |

SI源相对G=[0,10.712842,2.292292,6.435737]，298.15 K实算[0,10.713284,2.293929,6.437268] kcal/mol；313.15 K实算[0,10.82613,2.34830,6.50042]恢复正文[0,10.8,2.3,6.5]；各189正模。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Metal/ligand and atom accounting

冻结要求：Validate6b and full relevant ligand/substrate identity, Cu coordination/charge/spin, chlorine and reagent reservoirs. Formal CuIII labels alone do not validate electronic states. Different ligand inventories cannot be compared by bare total energies. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：四有效最低点、完整能量分量、温度冲突控制、真实C–Cl扫描/释放局部连结、选择性限度覆盖；构象差不冒充反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0009`。

```json
[
  {
    "source_locator": "main Fig1 pp8–9; SI65 method/TableS1,SI66–74 coordinates",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log",
        "sha256": "478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log",
        "sha256": "4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      }
    ]
  }
]
```


证据记录：`E0015`。

```json
[
  {
    "source_locator": "main Fig1 pp8–9; SI65 method/TableS1,SI66–74 coordinates",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log",
        "sha256": "478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log",
        "sha256": "4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      }
    ]
  }
]
```

### kp_reaction — Quantitative evidence for local C–Cl selectivity

冻结要求：Generate auditable quantities bearing on local C–Cl formation/selectivity. Repeating the source2.3kcal/mol minima difference alone does not establish the reaction route. Non-author models and bounded conclusions are eligible when grounded in relevant raw evidence. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：四有效最低点、完整能量分量、温度冲突控制、真实C–Cl扫描/释放局部连结、选择性限度覆盖；构象差不冒充反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0009`。

```json
[
  {
    "source_locator": "main Fig1 p8 andobserved6b connectivity;SI65",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log",
        "sha256": "478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log",
        "sha256": "4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/gaussian.log",
        "sha256": "c8153e242933065dc3ad5a76a914132ee54930862e7673584fd6124c768d0e29"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json",
        "sha256": "b3482ca59fbdf46460ec28dd8a00372adb9598b5632e08056bfc0f8aabf3b7b1"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      }
    ]
  }
]
```


证据记录：`E0015`。

```json
[
  {
    "source_locator": "main Fig1 p8 andobserved6b connectivity;SI65",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log",
        "sha256": "478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log",
        "sha256": "4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/gaussian.log",
        "sha256": "c8153e242933065dc3ad5a76a914132ee54930862e7673584fd6124c768d0e29"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json",
        "sha256": "b3482ca59fbdf46460ec28dd8a00372adb9598b5632e08056bfc0f8aabf3b7b1"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      }
    ]
  }
]
```

### kp_test — Mechanistic inference distinguished from endpoint ranking

冻结要求：Judge the discriminating power of the selected tests in light of observed product and catalyst/trapping controls. A claimed activation route needs connectivity and appropriate stationary/path evidence; neither author CuIII capture nor direct transfer is mandatory. Properly demonstrated collapse or indistinguishability is acceptable. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：四有效最低点、完整能量分量、温度冲突控制、真实C–Cl扫描/释放局部连结、选择性限度覆盖；构象差不冒充反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0009`。

```json
[
  {
    "source_locator": "main Scheme3 pp6–8,Scheme4 pp8–9",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json",
        "sha256": "19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f"
      }
    ]
  }
]
```


证据记录：`E0015`。

```json
[
  {
    "source_locator": "main Scheme3 pp6–8,Scheme4 pp8–9",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json",
        "sha256": "19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f"
      }
    ]
  }
]
```

### kp_limits — State and condition sensitivity

冻结要求：Bound model/spin, preparation/binding and thermal/solvation effects relevant to the inference. Explain source40°C versus any calculation temperature; do not equate the SI G273.15 label with verified313.15K thermochemistry or add arbitrary tolerance. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：四有效最低点、完整能量分量、温度冲突控制、真实C–Cl扫描/释放局部连结、选择性限度覆盖；构象差不冒充反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0009`。

```json
[
  {
    "source_locator": "SI64 40C;SI65 G273.15 label; currentkp_limits",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/batches/source_definition_audit_20261006/a01/results/paper_db6c4e0558113873.json",
        "sha256": "862b56ca6b0b3e7fd361c595b4b9e54858080cb9f0bac7466de7a5278cab1120"
      }
    ]
  }
]
```


证据记录：`E0015`。

```json
[
  {
    "source_locator": "SI64 40C;SI65 G273.15 label; currentkp_limits",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/batches/source_definition_audit_20261006/a01/results/paper_db6c4e0558113873.json",
        "sha256": "862b56ca6b0b3e7fd361c595b4b9e54858080cb9f0bac7466de7a5278cab1120"
      }
    ]
  }
]
```

### kp_conclusion — Local explanation with appropriate causal scope

冻结要求：Support or challenge the source rationale in proportion to evidence. Local energetics cannot prove the entire photocycle, quantitative yield or an exclusive global pathway. No source conformer or Cu oxidation-state winner is compulsory. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：四有效最低点、完整能量分量、温度冲突控制、真实C–Cl扫描/释放局部连结、选择性限度覆盖；构象差不冒充反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0009`。

```json
[
  {
    "source_locator": "main p9 and current local6b question",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json",
        "sha256": "b3482ca59fbdf46460ec28dd8a00372adb9598b5632e08056bfc0f8aabf3b7b1"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json",
        "sha256": "19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f"
      }
    ]
  }
]
```


证据记录：`E0015`。

```json
[
  {
    "source_locator": "main p9 and current local6b question",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json",
        "sha256": "b3482ca59fbdf46460ec28dd8a00372adb9598b5632e08056bfc0f8aabf3b7b1"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json",
        "sha256": "19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f"
      }
    ]
  }
]
```

### conclusion_investigation — What molecular account of local C–Cl bond formation can explain the observed chlorosulfonylation selectivity of allenoate6b under the source photo/copper conditions, and what evidence limits that account?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list.

当前复审：四有效最低点、完整能量分量、温度冲突控制、真实C–Cl扫描/释放局部连结、选择性限度覆盖；构象差不冒充反应势垒。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0009`。

```json
[
  {
    "source_locator": "current AR/PR objective;mainpp6–9/SI65",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log",
        "sha256": "478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log",
        "sha256": "4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json",
        "sha256": "19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f"
      }
    ]
  }
]
```


证据记录：`E0015`。

```json
[
  {
    "source_locator": "current AR/PR objective;mainpp6–9/SI65",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log",
        "sha256": "7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log",
        "sha256": "2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log",
        "sha256": "478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log",
        "sha256": "4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log",
        "sha256": "5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json",
        "sha256": "37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json",
        "sha256": "19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 51.85 小时；失败/状态未确认阶段 45.08 分钟；11 份计时日志/17 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 8,20 线程/进程；Gaussian %Mem=16GB,96000MB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0013 · gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log) | Gaussian:47687.1；Gaussian:19250.4 | 正常；正常 | {"threads":[8],"Gaussian_mem":["96000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0014 · gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log) | Gaussian:49835.3；Gaussian:18727.5 | 正常；正常 | {"threads":[8],"Gaussian_mem":["96000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0024 · Cu_CCl_point9_to_bondregion_scan7_20261002/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/gaussian.log) | Gaussian:7210.4 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0027 · Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log) | Gaussian:1341.4；Gaussian:1053.1；Gaussian:471.7 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0041 · source_four_minima_thermochemistry/a01/C1_synsyn_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log) | Gaussian:47687.1；Gaussian:19250.4 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[8],"Gaussian_mem":["96000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0042 · source_four_minima_thermochemistry/a01/C1_synsyn_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_high.log) | Gaussian:17636 | 正常 | {"threads":[8],"Gaussian_mem":["96000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0043 · source_four_minima_thermochemistry/a01/C1_synanti_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log) | Gaussian:49835.3；Gaussian:18727.5 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[8],"Gaussian_mem":["96000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0044 · source_four_minima_thermochemistry/a01/C1_synanti_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_high.log) | Gaussian:18200.9 | 正常 | {"threads":[8],"Gaussian_mem":["96000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0045 · source_four_minima_thermochemistry/a01/C3_synsyn_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log) | Gaussian:890.6；Gaussian:1173.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0046 · source_four_minima_thermochemistry/a01/C3_synsyn_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_high.log) | Gaussian:507.4 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0047 · source_four_minima_thermochemistry/a01/C3_synanti_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log) | Gaussian:992.2；Gaussian:1150.5 | 正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0048 · source_four_minima_thermochemistry/a01/C3_synanti_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_high.log) | Gaussian:527.3 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0086 · synsyn_Cu_CCl_closure_scan/a03/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/gaussian.log) | Gaussian:2704.9 | 其他/未确认 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

SI的G273.15标签不与数值一致；这是有证据的热项重建，不声称作者已确认笔误。未复现全光催化循环或速率。

通过的是有证据等价重建与当前局部问题；不宣称SI的273.15K标签本身已正确复现或作者已勘误，不认证全光氧化还原循环/反应速率。


原独立审查的 `unresolved_issues`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  {
    "issue": "SI G273.15标签与数值列、正文Fig1不完全同定义",
    "blocking_for_current_contract": false,
    "evidence_ids": [
      "SI",
      "main",
      "source_definition_audit",
      "thermo"
    ],
    "disposition": "字面273.15K复现不成立；298.15K数值一致强烈提示热学标签问题，但不声称已恢复作者私有输入。313.15K靠近正文不是作者温度证明。现行PR明确要求调查/保留，三温分析及当前局部结论均已完成。"
  },
  {
    "issue": "Fig1两panel C4不是同化学角色；形变与能量的因果分解未建立",
    "blocking_for_current_contract": false,
    "evidence_ids": [
      "main",
      "geometry_review"
    ],
    "disposition": "保留图示及固定化学角色两种比较，接受结构关联、拒绝一条角度等于独立2.3 kcal/mol张力能的过度结论。"
  },
  {
    "issue": "有限模型不能证明反应速率、真实唯一自旋/配位态或完整催化机制",
    "blocking_for_current_contract": false,
    "evidence_ids": [
      "AR_task",
      "PR_task",
      "AR_key_points",
      "outlet_analysis"
    ],
    "disposition": "有实算局部成键与基线证据，结论已限定；无同定义已解锁必要计算欠账。若未来另行主张动力学，则需对应势垒/连接/竞争态证据，非本轮要求。"
  }
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_db6c4e0558113873.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_db6c4e0558113873/verified_computation_reference.md)；SHA-256 `90d9831f0ea005355bb3a14580244188d01d027bf1cc2e2388621b20ff1836c8`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_db6c4e0558113873_ef263bc05409b5.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_db6c4e0558113873_ef263bc05409b5.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_db6c4e0558113873_ef263bc05409b5.json) | `da6392979a6e04dbc986bf3dc5b2065cde5ad68eaccac9bf2855bc774bd9f5c1` | evidence_or_analysis |
| E0002 | [tasks/v2_autonomous_research/paper_db6c4e0558113873/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_task.md) | `2316b7c5bb8d9c230a3dfdad68d10abac9aa6d7892ff8d5b805702c93d2f9f2a` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_db6c4e0558113873/agent_input/task.md](../../../v2_paper_reproduction/paper_db6c4e0558113873/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_task.md) | `3530922fb335f6910a6f61b0b9289a506d8a8cd334581ef4a22641a4c972a503` | historical_task_binding |
| E0004 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_ROOT_PRIMARY_SOURCE_READBACK.json) | `a131458d308b52199eb86e1c6e7fc3efefd0cc69c93f52a2a5001ed2c3df60d0` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_ROOT_NATIVE_READBACK.json) | `9f8ce2f290d610c66701f38fed799081fc653cd1cec06332a98de64ed1a3ea31` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_db6c4e0558113873/NATIVE_COMPUTATION_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_db6c4e0558113873/NATIVE_COMPUTATION_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_NATIVE_COMPUTATION_INDEX.json) | `31f5d9d577172a17f7acffedd45958d05366bbcee5ec9c243148cbfa2a855b13` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_db6c4e0558113873/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_db6c4e0558113873/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_COMPUTATION_INVENTORY.json) | `ec760ec1b0b8d38a5b22f10359a2e33940fac61c3199f664768ab647ef733697` | evidence_or_analysis |
| E0008 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_db6c4e0558113873/PUBLIC_DATA_LINK_AUDIT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_db6c4e0558113873/PUBLIC_DATA_LINK_AUDIT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_PUBLIC_DATA_LINK_AUDIT.json) | `109ed9016a31516db1056510f2857b25fc066f33da933edd08cc3c1ac507c307` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_db6c4e0558113873/SOURCE_COMPARISON.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_db6c4e0558113873/SOURCE_COMPARISON.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_SOURCE_COMPARISON.json) | `9d29146116d4d468c19b1087f452eb9f91ffabc81a95384be4c17e2b6345736e` | evidence_or_analysis |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_db6c4e0558113873.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_db6c4e0558113873.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_paper_db6c4e0558113873.md) | `fce376740fc953b22dcde9d4824d9240852aa1783aec3b66fbd24f5bf5733f85` | evidence_or_analysis |
| E0011 | [docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `994c5f3460cdcc5b86f8dc4b54682be8af9841631e2563081bb056e7bde71a87` | historical_task_binding |
| E0012 | [tasks/v2_paper_reproduction/paper_db6c4e0558113873/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `994c5f3460cdcc5b86f8dc4b54682be8af9841631e2563081bb056e7bde71a87` | historical_task_binding |
| E0013 | [docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_native_excerpt.json) | `7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e` | native_output |
| E0014 | [docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_native_excerpt.json) | `2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50` | native_output |
| E0015 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_db6c4e0558113873_ef263bc05409b5_input.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/reviews/paper_db6c4e0558113873_ef263bc05409b5_input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_paper_db6c4e0558113873_ef263bc05409b5_input.json) | `4a96c652429a1bb5a45f40d22f42e4c67b0fedeb49ebaea1a110abbc9c513618` | evidence_or_analysis |
| E0016 | [papers/paper_db6c4e0558113873/documents/main.pdf](../../../../papers/paper_db6c4e0558113873/documents/main.pdf) | `9b9d8841f0eb5ec7561cb770ad3bd43d0820639e443412d5da1bc74842318c8c` | source_document |
| E0017 | [papers/paper_db6c4e0558113873/documents/supplementary_001.pdf](../../../../papers/paper_db6c4e0558113873/documents/supplementary_001.pdf) | `a6585fbc4d364923517f436132456b23b012d972eeecb7a818a8a4259c1a6608` | source_document |
| E0018 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/results/analysis_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0018_analysis_summary.json) | `37b3ebc52041de8334bc30f53635c74871d2dcaedd381b35c236dc05fe4d5f1a` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_analysis.py) | `f0985dfac4f4d2e4d9c1f1c1e7821888e851dcb5ff51524890b084322335a99e` | input_or_analysis_code |
| E0020 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/inputs.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0020_inputs.json) | `acf4bff0d7ab181347e877a978c6fc223c6e49c5b1f77f2e5c0d7595f522f84f` | evidence_or_analysis |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/native_gaussian.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/native_gaussian.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_native_gaussian.py) | `b6adb055f8133e4e7baf6cb93e581b94a75409ef1698ff167b1bb9363c8ad5d9` | input_or_analysis_code |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/source_geometry_and_reference_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0022_source_geometry_and_reference_review_20260930.json) | `19e0060642637f30ab22d74d331a212a983231612ab91262bced1eb0fce6d56f` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/batches/source_definition_audit_20261006/a01/results/paper_db6c4e0558113873.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/batches/source_definition_audit_20261006/a01/results/paper_db6c4e0558113873.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0023_paper_db6c4e0558113873.json) | `862b56ca6b0b3e7fd361c595b4b9e54858080cb9f0bac7466de7a5278cab1120` | evidence_or_analysis |
| E0024 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_native_excerpt.json) | `c8153e242933065dc3ad5a76a914132ee54930862e7673584fd6124c768d0e29` | native_output |
| E0025 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_input.com) | `ede709c0b718b12768e2db002ddc241ba2afecd687506d999658dd08dc0d4ef7` | input_or_analysis_code |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_seven_point_outlet_graph_readback_20261002/a01/results/seven_point_outlet_review.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_seven_point_outlet_graph_readback_20261002/a01/results/seven_point_outlet_review.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_seven_point_outlet_review.json) | `ff82f72b4cd0af96d46c8e61394ca8783badb858c2538a5cee97691854fae658` | evidence_or_analysis |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_native_excerpt.json) | `5f37dda79a8b04a1bdeb75fd82287ba6b54acab4a4207ce834ee9ddedf4cc5d7` | native_output |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_input.com) | `d69741f10849ef209f24d0e82c5de002908c465cdd4f6fb527f46a7f0f222ae2` | input_or_analysis_code |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/results/released_outlet_identity_curvature_composite.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_released_outlet_identity_curvature_composite.json) | `b3482ca59fbdf46460ec28dd8a00372adb9598b5632e08056bfc0f8aabf3b7b1` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_analysis.py) | `0e6c0b0a5c3b1743b0af2e7a61258f637975ecefd0028a2a4e99a219dc9bdfb4` | input_or_analysis_code |
| E0031 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_task.md) | `2316b7c5bb8d9c230a3dfdad68d10abac9aa6d7892ff8d5b805702c93d2f9f2a` | historical_task_binding |
| E0032 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_reference_key_points.json) | `d3f44516d429a53801b3f7a79caa0eb9a6823672a54bcd1d2557d0042d54e6f8` | historical_task_binding |
| E0033 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_reference_conclusions.json) | `958721ad986ea25a62d73b812d9e4622013ec86b2cda74897589aa94aed79c53` | historical_task_binding |
| E0034 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_scoring_rules.json) | `1dab2c7dec41b68473c7259c9baef8ad7827a365bc963ee103051e367f8f8c40` | historical_task_binding |
| E0035 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_critical_failures.json) | `6d9140c7fc4d7ee6747b152d4bb27f1b688e8f9e81071f1874ce14e9a1912fbd` | historical_task_binding |
| E0036 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_task.md) | `3530922fb335f6910a6f61b0b9289a506d8a8cd334581ef4a22641a4c972a503` | historical_task_binding |
| E0037 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_reference_key_points.json) | `d3f44516d429a53801b3f7a79caa0eb9a6823672a54bcd1d2557d0042d54e6f8` | historical_task_binding |
| E0038 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_reference_conclusions.json) | `958721ad986ea25a62d73b812d9e4622013ec86b2cda74897589aa94aed79c53` | historical_task_binding |
| E0039 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_scoring_rules.json) | `1dab2c7dec41b68473c7259c9baef8ad7827a365bc963ee103051e367f8f8c40` | historical_task_binding |
| E0040 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_critical_failures.json) | `6d9140c7fc4d7ee6747b152d4bb27f1b688e8f9e81071f1874ce14e9a1912fbd` | historical_task_binding |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_low.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_native_excerpt.json) | `7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e` | native_output |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synsyn_high.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_native_excerpt.json) | `eb935229fce76ed80b61adf443c078c0e99f3a8f37fc494f83aece515a149158` | native_output |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_low.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_native_excerpt.json) | `2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50` | native_output |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C1_synanti_high.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_native_excerpt.json) | `f4ce8acf91ae31dfddc30890b2cf39e7f9a41cf53f6d1beeade3538f8d8a5243` | native_output |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_low.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_native_excerpt.json) | `478f7b05871782d3cf5c2332a130212143c7580008beafabd94887c726bca0b7` | native_output |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synsyn_high.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_native_excerpt.json) | `60a3e43d9a465a2c0b3cbf83b577deb3125d85e8cc6da505876ba91c625e40c3` | native_output |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_low.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_native_excerpt.json) | `4e147da9e16bb63479f0fae992cde94a9af5382bcdb8f96365e2ce582ca9f98e` | native_output |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/C3_synanti_high.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_native_excerpt.json) | `e07b329ac1fa173c1a94c94e68fa7103f30cb5244b7c75be6f3cb4bb4ac93162` | native_output |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synsyn_source_optfreq_SP/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synsyn_source_optfreq_SP/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0049_submission.json) | `eaff76406bf7ad602eee13ce9cea86d350209979a7f2f88f72a7ab785ed92f72` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synsyn_source_optfreq_SP/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synsyn_source_optfreq_SP/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synanti_source_optfreq_SP/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synanti_source_optfreq_SP/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_submission.json) | `2ca73b71862617d5a12130398ff70fa9b1538ea783386cb37b2807c52256cb4e` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synanti_source_optfreq_SP/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/C3_synanti_source_optfreq_SP/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_submission.json) | `b959dddf943cbbb8248c69c26675d5c5f3670ccf9cbbc8208081d7aee44f14da` | evidence_or_analysis |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_submission.json) | `bf66c54c59cfbd5627a7bb9320c24fe90d14cb3de74be83e9c29a728c77a0f1f` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_seven_point_outlet_graph_readback_20261002/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_seven_point_outlet_graph_readback_20261002/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_submission.json) | `509f4d7f25383bdc14549a1aa015d1b60bfcbf87006f0159d617eb17aa83854b` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_seven_point_outlet_graph_readback_20261002/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_seven_point_outlet_graph_readback_20261002/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_submission.json) | `2e402d43184b7e1083f20c1c02ccf191766ecfbe00172c7ffa1b384df4148e83` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_submission.json) | `61aec47c70e6c8c437e1e562477d2a817bd453c005f62b5331f45dc04be06eda` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_released_outlet_identity_curvature_composite_20261002/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_db6c4e0558113873/CURRENT_QUESTION_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_db6c4e0558113873/CURRENT_QUESTION_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_CURRENT_QUESTION_REVIEW.json) | `500664a2d5186858e7d219e1f733f8e31c658f4ba9a795dd2cec77cacdcdf1e0` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W08_PUBLIC_SOURCE_RECHECK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W08_PUBLIC_SOURCE_RECHECK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_W08_PUBLIC_SOURCE_RECHECK.json) | `28aaa1c990f8f58745938dafa72aede78e48e97af2b5d1071b1a9a3bc469d217` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_db6c4e0558113873/SOURCE_EXCERPTS.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_db6c4e0558113873/SOURCE_EXCERPTS.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0075_SOURCE_EXCERPTS.txt) | `51647c81747ff2426e69b5c697da42635aa25e341db3f7b40c2b01fab27f3262` | evidence_or_analysis |
| E0076 | [docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/input.com](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0076_input.com) | `495f5e91edb6d0b78e4c1911a168a08f924868fea3ce93d2622277058abe9106` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/synsyn_author_b3d3_genecp_opt_freq_v2_optimized.xyz](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/synsyn_author_b3d3_genecp_opt_freq_v2_optimized.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_synsyn_author_b3d3_genecp_opt_freq_v2_optimized.xyz) | `2a214fe2d38680ca3b810caaa31f9527fcd4eec594580b1c7a0f0bc6d143a79f` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/input.com](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_input.com) | `86e3b338fbf09489715bc90705f6121a811e29d4fa446e78a0e99138048734ed` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/synanti_author_b3d3_genecp_opt_freq_v2_optimized.xyz](../../../../docs/v2_verification/history/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/synanti_author_b3d3_genecp_opt_freq_v2_optimized.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_synanti_author_b3d3_genecp_opt_freq_v2_optimized.xyz) | `3c0df4049a4964228a890776ab224c68961175c69ae537572669265a48617b42` | input_or_analysis_code |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/baseline_audits/20260930T054922Z/audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/baseline_audits/20260930T054922Z/audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_audit.json) | `6c3e79ebed57b4d1717de726e0c0fbd5188ee4c4332ae22bf6f15db63c036016` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_binding.json) | `78d2df2f20376fd474fae49ebc02edc3836f57a96d019bc865aa97de9d917d40` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/inputs/source_extracts/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/inputs/source_extracts/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_main.txt) | `0b7f68b75acc18870f5e0d20188f43583e940e9dabd330793a571e3b000bd7fe` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/inputs/source_extracts/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/inputs/source_extracts/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_supplementary_001.txt) | `c9eef02c675c8031fb3c0bb0bfa2c1e51ce5a9ab7264562ee262d4b448aa451c` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/data/view_1.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/data/view_1.png) | `9572a41e78506c0eb419f5a8871fda437c437e8834777c1b16d9c14e518957a1` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_input.com) | `0f35b50f58e20aa4ce875dc968bbc443ad61965dc3b75a9b0e361670e53d2ca9` | input_or_analysis_code |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_native_excerpt.json) | `2add2f2583b8b0b88c1efd94f921a35c56f991bce5c66a80ea09982b40bd708b` | native_output |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_status.json) | `f13f706b4930a4b70cb6d1d2cedf43d6fa81a28a58102df8b5fb65ed55d6e412` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_native-return-code.txt) | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_submission.json) | `31e9c3212637191fd65b165de5bb94a08195b945ecd565d9c63e4d5507ed9d85` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_CCl_point9_to_bondregion_scan7_20261002/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0090_run.sh) | `525e07dbf35cf22369fabafd99794c69ea0796de3ca38eca6d8462854baad3c3` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/Cu_qualified_outlet_release_optfreq_SP_20261002/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0091_run.sh) | `525e07dbf35cf22369fabafd99794c69ea0796de3ca38eca6d8462854baad3c3` | input_or_analysis_code |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/v2_execution_20260929/outputs/source_four_minima_thermochemistry/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0092_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REPAIR_NOTICE_INTAKE_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REPAIR_NOTICE_INTAKE_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0093_REPAIR_NOTICE_INTAKE_20260930.json) | `12ac91fe44e16b379e42f1555748e1e0f4baeb1cd3cb4cac7c3a4ec304c3fe77` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REVIEWED_FOLLOWUP_WINDOW_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/v2_execution_20260929/REVIEWED_FOLLOWUP_WINDOW_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0094_REVIEWED_FOLLOWUP_WINDOW_20260930.json) | `3de07be5e6428385a87219a1411227baa8b83129b99009261d7313261d0f6605` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_db6c4e0558113873/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_db6c4e0558113873/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0095_NATIVE_READBACK.json) | `4d4aba2aed95b0a72a768b3faa70807ff62d4f2a6ff8983f3f9d6773a2310b12` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W08_RETURN_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W08_RETURN_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0096_W08_RETURN_INTAKE.json) | `ffcd8d44104220283be1f0de54d1fe9782f69ac6f5a70d93251052e05204f265` | evidence_or_analysis |
| E0097 | [tasks/final_verified_paper_reproduction/paper_db6c4e0558113873/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_db6c4e0558113873/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0097_scoring_rules.json) | `72c81663b5567135a079c53ffc1560315a284d6f0a11759751ac99e7d5b45a86` | historical_task_binding |
| E0098 | [tasks/final_verified_paper_reproduction/paper_db6c4e0558113873/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_db6c4e0558113873/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0098_verified_computation_reference.md) | `994c5f3460cdcc5b86f8dc4b54682be8af9841631e2563081bb056e7bde71a87` | historical_task_binding |
| E0099 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_db6c4e0558113873/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0099_package_manifest.json) | `9da24785fbad859b3ee704df058cbd71fe8a339161a668b9861fae7a1ea42197` | historical_task_binding |
| E0100 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_db6c4e0558113873/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0100_package_manifest.json) | `83bef24e77683301895c643e3c9c9d0f066dc450c0a392d4ab4bf9dfdca58587` | historical_task_binding |
| E0101 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/events_20261007/PUBLIC_SOURCE_RECHECK_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/events_20261007/PUBLIC_SOURCE_RECHECK_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0101_PUBLIC_SOURCE_RECHECK_20261007.json) | `b6791f0ceb0562a7fce789546e252f2937021b57b8a7bca3c15d35a716c2e01b` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/outputs/synsyn_Cu_CCl_closure_scan/a03/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_db6c4e0558113873/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0102_run.sh) | `63f9b04bc6ab9ad9fad832b306a7255ad0fc8f0cd24ffc8f291e7b482ccfd190` | input_or_analysis_code |
| N0093 | [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/reference_key_points.json](reference_key_points.json) | `d3f44516d429a53801b3f7a79caa0eb9a6823672a54bcd1d2557d0042d54e6f8` | latest_review_evidence |
| N0094 | [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/reference_conclusions.json](reference_conclusions.json) | `958721ad986ea25a62d73b812d9e4622013ec86b2cda74897589aa94aed79c53` | latest_review_evidence |
| N0095 | [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/scoring_rules.json](scoring_rules.json) | `1dab2c7dec41b68473c7259c9baef8ad7827a365bc963ee103051e367f8f8c40` | latest_review_evidence |
| N0096 | [tasks/v2_paper_reproduction/paper_db6c4e0558113873/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_db6c4e0558113873/evaluation/reference_key_points.json) | `d3f44516d429a53801b3f7a79caa0eb9a6823672a54bcd1d2557d0042d54e6f8` | latest_review_evidence |
| N0097 | [tasks/v2_paper_reproduction/paper_db6c4e0558113873/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_db6c4e0558113873/evaluation/reference_conclusions.json) | `958721ad986ea25a62d73b812d9e4622013ec86b2cda74897589aa94aed79c53` | latest_review_evidence |
| N0098 | [tasks/v2_paper_reproduction/paper_db6c4e0558113873/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_db6c4e0558113873/evaluation/scoring_rules.json) | `1dab2c7dec41b68473c7259c9baef8ad7827a365bc963ee103051e367f8f8c40` | latest_review_evidence |
| N0099 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0100 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/agent_input/task.md](../agent_input/task.md) | `2316b7c5bb8d9c230a3dfdad68d10abac9aa6d7892ff8d5b805702c93d2f9f2a` |
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/reference_key_points.json](reference_key_points.json) | `d3f44516d429a53801b3f7a79caa0eb9a6823672a54bcd1d2557d0042d54e6f8` |
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/reference_conclusions.json](reference_conclusions.json) | `958721ad986ea25a62d73b812d9e4622013ec86b2cda74897589aa94aed79c53` |
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/scoring_rules.json](scoring_rules.json) | `1dab2c7dec41b68473c7259c9baef8ad7827a365bc963ee103051e367f8f8c40` |
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/critical_failures.json](critical_failures.json) | `6d9140c7fc4d7ee6747b152d4bb27f1b688e8f9e81071f1874ce14e9a1912fbd` |
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/evidence_map.json](evidence_map.json) | `688fa19c904a57b2bbed705c58e18996887cfb601e57e0c4de5e1ab498a09f54` |
| [tasks/v2_autonomous_research/paper_db6c4e0558113873/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `bd09c6d1f8a21b5a8230aa6e498f50b9f881a58d99a7780efbc41229a3f89f96` |

## 2026-10-19 active paper_science_v2 scoring migration

The active private rubric assigns 100 points only to independent intermediate findings and final scientific conclusions, using binary leaves and no process score or multiplier. Historical criteria/weights above are archival, not active scoring. Public inputs and author-route contract remain byte-identical. Existing acceptance remains PASS_STRICT_CURRENT_FROZEN_SCOPE; this migration is not new chemical validation. Fixed windows and retained boundaries are in scoring_rules.json and reference_qualification.json.


## 2026-10-19 Round3 scoring-contract repair

Historical verification statements above are preserved verbatim. Current mode-specific scientific rules supersede earlier scoring-policy wording; this append does not change the chemistry acceptance class.

- Removed the three AR exact-G numeric gates (24 points): no unambiguous author numerical temperature matches the public reaction condition. No verification values replace source targets.
- Redistributed those 24 points across the eight existing distinct intermediate structural/ordering/geometry propositions; no new chemical computation or new claim is introduced.
- Removed mandatory private SI-label history from AR final14 and figure-panel C4 criticism from AR geometry8.
- Audited every existing leaf for scientific role, source/verification support and physical definitions; retained unproven narrow-window risks as explicit provisional calibration limits rather than inventing wider tolerances.
- Source-temperature correction: the main figure does not prove author 313.15 K thermochemistry. Numerical consistency with a verifier temperature column is not recovered author provenance. AR omits condition-unmatched exact targets; PR compares the printed source column with its unresolved temperature explicitly retained.

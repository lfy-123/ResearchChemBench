# 2026-10-28 二次审查（group_10）

现存S1、f、Zn4p及PR两自由能均在原硬窗；有限电子与热竞争解释有支持；Zn4p必答设计及精确相态布居仍未解决。本轮只直接读源文、原生证据和必要算术核对；未新增计算，不继承历史PASS。逐命题覆盖及专家问题见本轮审查材料。

---

# 2026-10-28 V3范围与逐命题证据复用（group_10）

保持完整Z-cAACCy的构型—低能吸收解释问题，保留两模式六个原有光谱/轨道最终硬数值。取消两个几何交付独立分和重复红移/混合综合分；按最终分子解释、热可达性、凝聚相适用性评分。原PR另有300 K D3BJ/无D3BJ自由能复现，本轮保留其两个硬窗；AR不新增该消融，范围差异显式登记。

- `r_perpendicular_s1_energy`：SI p21 TableS8/S9或正文p4 Fig2；已读NAO crosscheck与原生TD：3.1097，源target 3.1097±0.05 eV，原窗获支持。
- `r_perpendicular_s1_strength`：SI p21 TableS8/S9或正文p4 Fig2；已读NAO crosscheck与原生TD：0.0883，源target 0.0883±0.01 dimensionless，原窗获支持。
- `r_perpendicular_zn4p`：SI p21 TableS8/S9或正文p4 Fig2；已读NAO crosscheck与原生TD：2.0949854839，源target 2.1±0.5 percent，原窗获支持。
- `r_coplanar_s1_energy`：SI p21 TableS8/S9或正文p4 Fig2；已读NAO crosscheck与原生TD：2.4524，源target 2.4526±0.05 eV，原窗获支持。
- `r_coplanar_s1_strength`：SI p21 TableS8/S9或正文p4 Fig2；已读NAO crosscheck与原生TD：0.0132，源target 0.0132±0.01 dimensionless，原窗获支持。
- `r_coplanar_zn4p`：SI p21 TableS8/S9或正文p4 Fig2；已读NAO crosscheck与原生TD：8.5476790314，源target 8.5±0.5 percent，原窗获支持。
- `r_molecular_absorption_explanation`：正文pp3–4 Figs1/2；2.4524 vs3.1097 eV及2.094985→8.547679% Zn4p，S1到对应LUMO；原生两构型及234正模支持局部稳定构型。无需按两个结构分别给分。
- `r_thermal_accessibility`：正文pp4–5/SI p21 TableS7；300 K RRHO ΔG(D3) −0.047259 kJ/mol支持近简并；无D3精修+4.681266；软模精修变化−0.042008，不能强定近零排序。
- `r_d3_free_energy`：SI TableS7；原生RRHO ΔG -0.0472589928 kJ/mol，保持源-0.1/+4.8±0.5硬窗；敏感性不冒充源程序相同。
- `r_nod3_free_energy`：SI TableS7；原生RRHO ΔG +4.681265855 kJ/mol，保持源-0.1/+4.8±0.5硬窗；敏感性不冒充源程序相同。
- `r_solution_crystal_applicability`：正文p4两晶体同黄色溶液；已有气相构型/ΔG支持可达性，但未计算晶体堆积和真实溶液布居/转动率，保持适用边界。

证据缺口：原AR/PR热力学任务不同：PR有D3BJ/no-D3的两个硬数值，AR只有近室温热竞争；未静默统一；NAO实现已做闭合/全角动量子空间核对，但并非取得作者私有NBO程序，C2p残差保留；分子近零自由能不能确定精确溶液布居、转动速率或晶体堆积。本轮无新增量化计算、无重验证、无ARCHE盲测；历史PASS不自动继承。以下历史正文原样保留，历史评分描述不再是当前评分合同。

---

# V2 验证计算参考：Zn 构型与低能吸收

论文：`paper_9ec32e81e2826041`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：同作者PBE0构型/TD路线以及有闭合检验的NAO分区恢复构型吸收差、Zn4p增量和近简并热力学；核心结果确有原生TD及完整最低点支持。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

Investigate the relationship between accessible molecular configurations and low-energy electronic absorption of the supplied Z-cAACCy complex. Determine what molecular evidence can explain the optical contrast between its reported crystal samples, what role the Zn center has in the relevant electronic response if any, and what cannot be inferred from an isolated-molecule study. Select and test your own account of the structure–property relationship without assuming a preferred geometry or metal contribution.

冻结题面中的科学目标：

Investigate the relationship between accessible molecular configurations and low-energy electronic absorption of the supplied Z-cAACCy complex. Determine what molecular evidence can explain the optical contrast between its reported crystal samples, what role the Zn center has in the relevant electronic response if any, and what cannot be inferred from an isolated-molecule study. Select and test your own account of the structure–property relationship without assuming a preferred geometry or metal contribution.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The source reports colorless/perpendicular and yellow/more-coplanar crystal forms, with angles between carbene/zincafluorene ring planes83.1 and23.9degrees (main p3 Figure1). Its interpretation is that coplanarity stabilizes a C–Zn pi-type LUMO and enables lower-energy absorption; source Zn4p LUMO contributions are2.1% versus8.5% (main p4 Figure2). Reconstruct the full molecular conformations and reproduce/assess this baseline. SI p3 uses PBE0/6-311+G** with D3BJ for ground-state optimizations and frequencies, also separately omits D3BJ to examine dispersion; G is at300K. TableS7 gives Gcoplanar−Gperpendicular−0.1kJ/mol withD3BJ and+4.8without forZ-cAACCy. TD-PBE0/6-311+G** on the optimized ground states gives five lowest singlets; TablesS8/S9 report S1=3.1097eV,f0.0883 versus2.4526eV,f0.0132. Source NAO/Multiwfn orbital analysis is one metal-character definition, not a unique physical population observable. Thermal low-frequency treatment and population implications require scrutiny; identical yellow solutions do not measure a gas free-energy difference. Fixed cross-geometry decompositions, alternative root-matching diagnostics and broader sensitivities are benchmark additions. Z-IP SOC/phosphorescence calculations are not part of this molecule reproduction.

Reproduce the disclosed source baseline and assess what it supports about the same scientific question. Explain source ambiguities and any deviations. Additional tests you choose are your extensions; they are not publication results. A defensible disagreement earns scientific credit; protocol fidelity is assessed separately on the process axis.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf](../../../../papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf) | `dbb8ec5153da3d86acde2fd320f01cc1bae86bf16cebf2fd2cf835280933d7cb` |
| [papers/paper_9ec32e81e2826041/documents/main.pdf](../../../../papers/paper_9ec32e81e2826041/documents/main.pdf) | `c494b9ed5388f0c6d968d8e80ce851426473aa9779a3c3930927445340195dec` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Full neutral C35H43NZn PBE0/6-311+G(d,p) D3BJ/no-D3 source geometries, frequencies at 300 K, and native TD outputs were read. Four baselines plus polished no-D3 endpoint each have 234 positive modes. A saved-density independent NAO implementation has checked norm/electron closure and full-angular-subspace mapping; native diagnostic output was read.

1. 核对完整 80 原子、中性单重态 C35H43NZn 与两个几何家族，保留 Dipp/cyclic 基团；晶体平面角只是观测，不能强制为气相/分子平衡角。

2. 按作者 PBE0/6-311+G(d,p) 执行 D3BJ/no-D3 两几何族四套 Opt/Freq、300 K 热化学和真实 TD；补做 no-D3 perpendicular 收敛/软模控制，四端点各 234 正模，精修分支另列。

3. 读取两族各 S1–S5 的能量/f，与源十条响应逐项比较；perpendicular/coplanar S1=3.1097/2.4524 eV、f=0.0883/0.0132，激发能最大差约 0.0002 eV、十个 f 一致。

4. 由保存密度的独立 NAO 实现、完整角动量子空间、电子数/范数闭合及 MO146 身份重建 LUMO 参与；Zn4p=2.094985/8.547679%，carbene C2p=55.230944/53.539807%。替代实现的等价性有实际检查，不能自称作者私有程序完全相同。

5. 比较 300 K RRHO 的 Gcoplanar−Gperpendicular，D3BJ/no-D3 为 −0.047259/+4.681266 kJ/mol，qRRHO 仅作独立敏感性。支持低能吸收与 Zn 混合变化，近零 G 不支持稳健布居顺序或晶体/器件性能。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

### 最近一次原生有效性复核

本轮读coplanar/perpendicular原生TD10及4+1 OptFreq：S1=2.4524/3.1097 eV，正常Freq各234正模；读取NAO诊断原始输出并保留源C2p百分数的小残差。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| S1 perpendicular,coplanar (eV) | [3.1097,2.4526] | [3.1097,2.4524] | All five perpendicular source TD energies match; coplanar residuals only 0.0001–0.0002 eV. All ten oscillator strengths match. This directly reproduces the approximately 0.657 eV contrast. |
| LUMO Zn4p perpendicular,coplanar (%) | [2.1,8.5] | [2.0949854839,8.5476790314] | Residuals −0.0050/+0.0477 percentage points. Equivalent NAO partition is supported by stored transformation/norm/electron closure and matched transitions, not private author-binary identity. |
| LUMO carbene C2p perpendicular,coplanar (%) | [55.2,53.4] | [55.2309442224,53.5398073248] | Residuals +0.0309/+0.1398 percentage points; source C2p dominance and Zn4p change survive. Coplanar difference is retained rather than dismissed as rounding. |
| Gcoplanar−Gperpendicular, D3BJ/no-D3, 300 K (kJ/mol) | [-0.1,4.8] | [-0.0472589928,4.681265855] | Residuals +0.05274/−0.11873 kJ/mol. Source finding is near-degeneracy versus a few-kJ no-D3 preference, not robust tiny ranking. Native Hessian polish changes the no-D3 gap −0.04201 kJ/mol; qRRHO controls identify thermal sensitivity without claiming a universal interval. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_zinc_system_identity — Correct full complex, graph/state identity and configuration mapping.

冻结要求：Check all80atoms and the supplied connectivity, including N-Dipp and cyclic groups, in actual inputs/outputs; ensure Zn/carbene/biphenyl identities survive transformations. Inspect charge, electronic state and declared model. Different atomic orderings require explicit mapping, not assumed indices. Deleting bulky groups changes the physical problem unless its approximation is validated.

当前复审：完整80原子中性单重态

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "Full neutral singlet 80-atom graph, bulky Dipp/cyclic groups and four native minima are retained. Explicit atom maps distinguish the two orientations. Crystal 83.1/23.9-degree planes are observations, not imposed molecular equilibrium angles."
  }
]
```


证据记录：`E0054`。

```json
[
  {
    "assessment": "bounded_evidence_and_explicit_limit",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "assessment": "bounded_evidence_and_explicit_limit",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  }
]
```

### kp_configuration_optical_evidence — Real molecular configuration and low-energy absorption findings.

冻结要求：Inspect native structures and actual electronic excitation/response evidence relevant to the proposed interpretation. Recompute energies/units and any reported thermochemistry. For optical claims check transition energy, strength and state character or an appropriate alternative optical observable; a ground-state orbital gap alone is not a vertical transition. The number of states must cover the claimed absorption range, not an arbitrary five-root quota. Source values alone earn no new evidence credit.

当前复审：真实TD/频率/构型

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "Both geometry families have real Opt/Freq and vertical TD results. All ten source S1-S5 energies and strengths are compared, with S1/S2 composition kept separate. Coplanar S1 2.4524 eV/f0.0132 versus perpendicular 3.1097 eV/f0.0883 reproduces the published low-energy absorption contrast. No orbital gap is substituted for a vertical excitation."
  }
]
```


证据记录：`E0054`。

```json
[
  {
    "assessment": "bounded_evidence_and_explicit_limit",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "assessment": "bounded_evidence_and_explicit_limit",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  }
]
```

### kp_structure_property_explanation — Evidence for the relation of configurations, optical behavior and any Zn contribution.

冻结要求：Assess whether the chosen study discriminates the claimed relation instead of reading planarity labels or assuming metal participation. A Zn-role claim needs an explicit, meaningful population/transition analysis and actual mapped evidence; different justified partitions are acceptable and not expected to reproduce8.5%. Corresponding states across geometries must be justified rather than assumed by root index. If dispersion causation is claimed, require separation adequate to that claim, not the V1 decomposition matrix for every submission. Reject unique causation if residual changes remain unaccounted.

当前复审：跃迁相关Zn4p与C2p分区

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "The acceptor is explicitly MO146; coplanar S1 is dominated by 144->146, perpendicular S1 by 145->146 and 144->146. Complete NAO subspaces support ligand-dominated acceptor character and increased Zn4p mixing in the coplanar case (8.547679 vs 2.094985%). Both C2p and perpendicular Zn3d provide additional definition checks. This supports the molecular account, not unique causation or a claim that LUMO percentage equals total excited-state metal charge."
  }
]
```


证据记录：`E0054`。

```json
[
  {
    "assessment": "superseded_with_source_scope_correction_20261002",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "assessment": "bounded_evidence_and_explicit_limit",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  }
]
```

### kp_state_thermo_reliability — Uncertainty and validity appropriate to the state and stability claims.

冻结要求：Validate minima when called stable, distinguish constrained diagnostics and failed searches, and check thermodynamic conventions if using G/populations. Small energy differences need uncertainty sufficient for the claim; low-frequency ambiguity cannot be hidden in many digits. Distinguish molecular absorption and crystal edges, and thermal population from a single structure. Accept other justified reliability strategies without fixed method/D3/temperature/family requirements.

当前复审：D3/noD3和热力学控制；最终结构-吸收关系与源一致。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "Four minima have 234 positive modes. The formerly unresolved noD3 perpendicular displacement/Hessian question has a completed independent finite control; all final tightened criteria pass and soft-mode identities remain aligned. Native 300K/1atm RRHO is compared to source; qRRHO remains a separately labeled sensitivity. Near-zero D3 free energy does not establish a robust sign, conformer population, barrier or crystal thermodynamics."
  }
]
```


证据记录：`E0054`。

```json
[
  {
    "assessment": "superseded_with_source_scope_correction_20261002",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "assessment": "bounded_evidence_and_explicit_limit",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  }
]
```

### conclusion_investigation — Investigate the relationship between accessible molecular configurations and low-energy electronic absorption of the supplied Z-cAACCy complex. Determine what molecular evidence can explain the optical contrast between its reported crystal samples, what role the Zn center has in the relevant electronic response if any, and what cannot be inferred from an isolated-molecule study. Select and test your own account of the structure–property relationship without assuming a preferred geometry or metal contribution.

冻结要求：Conclude what molecular configurations and optical evidence explain about the observed contrast, including the supported role or lack of identifiable role of Zn. Permit alternatives, contradiction or an evidence-backed limit; do not require coplanarity, D3 stabilization or a source percentage as a winner. Distinguish valid partial evidence from uncomputed cases called non-identifiable. No isolated-molecule result alone establishes crystal population, identical-solution conformer ratio, lifetime, SOC or photocatalytic behavior.

当前复审：kp_zinc_system_identity：完整80原子中性单重态；kp_configuration_optical_evidence：真实TD/频率/构型；kp_structure_property_explanation：跃迁相关Zn4p与C2p分区；kp_state_thermo_reliability：D3/noD3和热力学控制；最终结构-吸收关系与源一致。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "rationale": "Two accessible molecular configurations, a lower-energy coplanar absorption and stronger Zn4p contribution to its actual acceptor reproduce the source-supported molecular explanation. The current conclusion explicitly separates vertical molecular spectra from crystal reflectance and solution population. No lifetime, SOC, phosphorescence, Z-SIP/Z-IP or triplet photocatalysis claim is certified."
  }
]
```


证据记录：`E0054`。

```json
[
  {
    "assessment": "bounded_answer_ready_for_independent_review",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json",
        "sha256": "0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json",
        "sha256": "9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json",
        "sha256": "dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json",
        "sha256": "7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json",
        "sha256": "7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json",
        "sha256": "7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json",
        "sha256": "e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408"
      }
    ]
  },
  {
    "assessment": "bounded_answer_ready_for_independent_review",
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json",
        "sha256": "91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json",
        "sha256": "3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json",
        "sha256": "4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json",
        "sha256": "4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 45.30 小时；9 份计时日志/14 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 20 线程/进程；Gaussian %Mem=12GB,90GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0004 · outputs/coplanar_PBE0_D3geometry_canonical_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/gaussian.log) | Gaussian:4070.4 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · outputs/coplanar_nod3_optfreq_recovery1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_nod3_optfreq_recovery1/gaussian.log) | Gaussian:12146.5；Gaussian:18679 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · outputs/perpendicular_PBE0_D3geometry_canonical_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/gaussian.log) | Gaussian:3829.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · outputs/perpendicular_nod3_optfreq_recovery2/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_nod3_optfreq_recovery2/gaussian.log) | Gaussian:21114.5；Gaussian:16875.8 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/audit_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/audit_stdout.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/gaussian.log) | Gaussian:639.9；Gaussian:17403.3 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0010 · ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/gaussian.log) | Gaussian:16909；Gaussian:17240.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0011 · ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/gaussian.log) | Gaussian:16713.4；Gaussian:17335.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0070 · outputs/v2_coplanar_D3geom_NAOMO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_coplanar_D3geom_NAOMO_a01/gaussian.log) | Gaussian:53.5 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0071 · outputs/v2_perpendicular_D3geom_NAOMO_diagnostic_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_perpendicular_D3geom_NAOMO_diagnostic_a01/gaussian.log) | Gaussian:55 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

不能把单分子vertical跃迁直接称晶体边/溶液布居，也不能从-0.047 kJ/mol的D3差得稳健唯一构型；NAO等价有证据但不宣称私人作者二进制逐字一致。

```json
[
  "No exact author Gaussian revision/NAO binary is certified; source private implementation details are not a scientific requirement.",
  "No robust tiny D3 Gibbs ordering, crystal population, solution conformer ratio, luminescence, SOC or photocatalytic response is inferred."
]
```


原独立审查的 `material_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Every printed digit is not reproduced. Residuals remain in the comparison table, including coplanar C2p +0.139807 percentage points and noD3 G -0.118734 kJ/mol. No probability distribution or universal error bar is inferred from these residuals.",
  "Exact Gaussian16 C.02 and author NAO binary/coefficient identity are not verified. The valence-shell choice was taken from retained native NBO Cor/Val labels before reading the repaired percentages; those labels are our retained native output, not unpublished author files.",
  "Numerical completeness of the independent NAO construction and multi-component agreement support compatible analysis; they do not prove algorithm identity. Old deleted-PNAO/GSVD/electron-deficit output remains invalid and is not reused as accepted quantitative evidence.",
  "RRHO near-degeneracy is method-dependent: recorded qRRHO controls change the magnitude. No robust tiny D3 preference, crystal population, solution conformer ratio or rotational rate is accepted.",
  "Transition configuration percentages retain both 2X^2 and signed 2(X^2-Y^2); the source weighting formula is not stated. This does not affect identification of the dominant acceptor.",
  "This is scientific reference validation informed by the paper. It is not a blind autonomous-agent run, an evaluator score, runner-isolation certification, or verification of the entire publication.",
  "The formal reference_validation_plan.md contains historical pending text and separate future evaluator-calibration work. This review records scientific completion externally; it does not certify those unperformed deployment checks or alter the formal evaluation package."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_9ec32e81e2826041.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_9ec32e81e2826041/verified_computation_reference.md)；SHA-256 `439ef7d0d1351b166c409bc664c79e8d524f9c1a2a7f7d89106fb5382691812e`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_9ec32e81e2826041.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_9ec32e81e2826041.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_9ec32e81e2826041.json) | `619a6a57b090efc6e019e6ab34ac8dada2712d8b0c44624e791e45f9ff2a22ff` | evidence_or_analysis |
| E0002 | [papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf](../../../../papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf) | `dbb8ec5153da3d86acde2fd320f01cc1bae86bf16cebf2fd2cf835280933d7cb` | source_document |
| E0003 | [papers/paper_9ec32e81e2826041/documents/main.pdf](../../../../papers/paper_9ec32e81e2826041/documents/main.pdf) | `c494b9ed5388f0c6d968d8e80ce851426473aa9779a3c3930927445340195dec` | source_document |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `3867ad09d6eb5b9a74f02166cd203d48af0da6b63f06cb6ea380b9d1fbb248b2` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_nod3_optfreq_recovery1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_nod3_optfreq_recovery1/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `8dcad86652f55fbbc483eae2020aaceb91f20a5f47339c8b1ede2aa1ecef3e20` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `83e9958b0b2410fb481f9156b4e1d449e61f6acc790de5a0d83c58e21076304f` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_nod3_optfreq_recovery2/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_nod3_optfreq_recovery2/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `b2a933f0deca7293bc2f6cc5d3d8c195949e6c3fbcad7017de14b498a63a0da4` | native_output |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/audit_stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/audit_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `4b85831c933137a503a37593ff7114fd607d891ad6a236b9972fe7aa279461dd` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `1e361d0660f49a69ee535cfc5da5ec96cfbd821a3b49615f5a1ac2004e3e7c53` | native_output |
| E0010 | [docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `b8eb48e3c1acfe26873c67d4c0ce7397d124fcfab3dae31c521a0f26040f94ec` | native_output |
| E0011 | [docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `8c26b5d46ba1e846e010db7baf99f5883b41ead5b53d14726788a7e6f64404f1` | native_output |
| E0012 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_Fig2_saved_NAO_crosscheck_20261005.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_Fig2_saved_NAO_crosscheck_20261005.json) | `bba421dd0511386d64b99960fbb65a9b7e077922344719fae3e17d932fce0f97` | evidence_or_analysis |
| E0013 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_THERMO_MODE_COMPARISON_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_THERMO_MODE_COMPARISON_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_ZN_THERMO_MODE_COMPARISON_20261006.json) | `66f4379251eaea80d035fd706fab6065e65c88aef26d174a409b2f5fa29dab36` | evidence_or_analysis |
| E0014 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_task.md) | `6cb7dd6284e88143887c55dda248b51c552df1aa651041e0441507aef94c0111` | historical_task_binding |
| E0015 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_reference_key_points.json) | `f11616779cce919d23152d6969beec1adf23b203aa0d87563a1c67f77f0bf690` | historical_task_binding |
| E0016 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_reference_conclusions.json) | `71e146bf39482aefdc689f5dae10299242dba7ab6f8e72455f62666fdb7aa0b8` | historical_task_binding |
| E0017 | [tasks/v2_autonomous_research/paper_9ec32e81e2826041/agent_input/task.md](../../../v2_autonomous_research/paper_9ec32e81e2826041/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_task.md) | `f4ec0f9b16bdc427c0b7d272b5349778c8cd58c7cc18900fe6aac19eea7bf9de` | historical_task_binding |
| E0018 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9ec32e81e2826041/NATIVE_EVIDENCE_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9ec32e81e2826041/NATIVE_EVIDENCE_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_NATIVE_EVIDENCE_INDEX.json) | `22c28607af8d913d19c1f91dbb254ba5217d9a4ec2e326b2ba0b2d2b1bed405a` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9ec32e81e2826041/SOURCE_PAGES_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9ec32e81e2826041/SOURCE_PAGES_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_SOURCE_PAGES_READBACK.json) | `d2c12f5d29e208bb47ee6862c00abc66109e4c362ca12efbfa3ce162275fffc6` | evidence_or_analysis |
| E0020 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9ec32e81e2826041/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9ec32e81e2826041/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_COMPUTATION_INVENTORY.json) | `06419d1e74970f02a24735bed1199cffb6d0175074ad44f967029d1c32ddd78d` | evidence_or_analysis |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_9ec32e81e2826041.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_9ec32e81e2826041.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_paper_9ec32e81e2826041.md) | `dc945de8861e277eff8d92b024f3fd7670a60a62d71e9d28c8b1d8073f32a8be` | evidence_or_analysis |
| E0022 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/legacy_v1_archive/verified_computation_reference.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/legacy_v1_archive/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_verified_computation_reference.md) | `fe75a19b95f51cd57b32507dc81116ff4a80f66f6fda4f7eaf49b436ded0e025` | historical_task_binding |
| E0023 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/legacy_v1_archive/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/legacy_v1_archive/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `ab67413dade13ce49e11148530ef63c04d6280fb1acead82211e1a05fff888cb` | historical_task_binding |
| E0024 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_task.md) | `f4ec0f9b16bdc427c0b7d272b5349778c8cd58c7cc18900fe6aac19eea7bf9de` | historical_task_binding |
| E0025 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_reference_key_points.json) | `f11616779cce919d23152d6969beec1adf23b203aa0d87563a1c67f77f0bf690` | historical_task_binding |
| E0026 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_reference_conclusions.json) | `71e146bf39482aefdc689f5dae10299242dba7ab6f8e72455f62666fdb7aa0b8` | historical_task_binding |
| E0027 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9ec32e81e2826041/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_package_manifest.json) | `6af5b69fcdb10286899bfa906669f4eeb2900950395451af8c876125211091da` | historical_task_binding |
| E0028 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_task.md) | `6cb7dd6284e88143887c55dda248b51c552df1aa651041e0441507aef94c0111` | historical_task_binding |
| E0029 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_reference_key_points.json) | `f11616779cce919d23152d6969beec1adf23b203aa0d87563a1c67f77f0bf690` | historical_task_binding |
| E0030 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_reference_conclusions.json) | `71e146bf39482aefdc689f5dae10299242dba7ab6f8e72455f62666fdb7aa0b8` | historical_task_binding |
| E0031 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9ec32e81e2826041/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_package_manifest.json) | `e450bac9822c7621f22afac67ef5e40e81e74bf0da57332c882aebae9fe4824c` | historical_task_binding |
| E0032 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/Zn_before_final_20261006T142144Z/paper_9ec32e81e2826041.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/history/Zn_before_final_20261006T142144Z/paper_9ec32e81e2826041.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_paper_9ec32e81e2826041.json) | `26ce39dbee01829a45f5d40ec9a69e2e8f92f248f37aad645a14b92e552eed9b` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/strict_author_route_validation_20261001/pause12_focus6_20261006T141129Z/ZN_FINAL_INDEPENDENT_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/pause12_focus6_20261006T141129Z/ZN_FINAL_INDEPENDENT_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_ZN_FINAL_INDEPENDENT_READBACK.json) | `f585e641120c4dd39e57a4585739efa3746d009f060ac2c92eae454d64a41efd` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/ZN_INDEPENDENT_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/ZN_INDEPENDENT_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_ZN_INDEPENDENT_READBACK.json) | `c553f8273585c8e12128bfb943cd480b83e13ecc6d7761b904dfdf17611f0b06` | evidence_or_analysis |
| E0035 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_FIG2_COMPLETE_REVIEW_ADDENDUM_20261005.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_FIG2_COMPLETE_REVIEW_ADDENDUM_20261005.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_ZN_FIG2_COMPLETE_REVIEW_ADDENDUM_20261005.json) | `848cb6b1fb40e3e2f34c52d23854146ae65cb2b8ab4aae39180cd3a91f682ceb` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_FINAL_HESSIAN_NATIVE_ACCEPTANCE_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_FINAL_HESSIAN_NATIVE_ACCEPTANCE_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_ZN_FINAL_HESSIAN_NATIVE_ACCEPTANCE_20261006.json) | `f52a36d619087daa33ff8d0e3796d0448a5e734275958f8925cef57f26aee2a6` | evidence_or_analysis |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/author_zinc_valence_NAO_diagnostic_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_author_zinc_valence_NAO_diagnostic_20261002.json) | `7b541d0c6e42363f30eef7871b15f1a153edc5334bbe3f66a08178e5e90194e8` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_TD_source_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_zinc_TD_source_acceptance.json) | `7ee2a773ca331cdeb3f56ca115df3f62ca1f4319bddc394c11e5febb52a7a6b9` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_thermochemistry_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_zinc_thermochemistry_audit.json) | `dd00bdfeb5345bb94bbe08f7111403283200747dce71f473669724930f254640` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/coplanar/NAO_transform.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/coplanar/NAO_transform.npz) | `c512ed1f41b2080d449b42e4d7ba4a584eb1cbde7f7fe431fcb758cf61353f08` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/zinc_D3geometry_transition_v3/coplanar_PBE0_D3geometry_canonical_TD10/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/zinc_D3geometry_transition_v3/coplanar_PBE0_D3geometry_canonical_TD10/wavefunction.fchk) | `0513a0ff0ee56158503715870ec70f2fcd4cdf04e68a6e61944a08de66fb47c7` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/perpendicular/NAO_transform.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_author_zinc_valence_NAO_diagnostic_20261002_a02/perpendicular/NAO_transform.npz) | `34873a367ee211962d850537cd6c78b3f97391a2065c4720b715e3c29e49a944` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/wavefunction.fchk) | `a3e6329796d850837745584121947d2f2198e2465442f81547c62f42610a98f7` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_input.com) | `506b12b2a70595c239bbac25274419fb05bc8d47cfa0988b5aca2201997831d8` | input_or_analysis_code |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_nod3_optfreq_recovery1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_nod3_optfreq_recovery1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_input.com) | `9b6277544100d4e21e61d277bb50dea75eaf93b0cc15e1c4ced367e683224f49` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_input.com) | `1c9728d110b2af33088ade7e7c4ddd9adcc55e3911f647c23459bc52e4ea5c73` | input_or_analysis_code |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_nod3_optfreq_recovery2/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_nod3_optfreq_recovery2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_input.com) | `aba86bf56f27c6a87adb1fd10781f71917c96069c5af03e59dbf67c05f1c2399` | input_or_analysis_code |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_input.com) | `383e21ae689609cc1380c7ac6e649c604a8249bb12ab89ffa5c0fbe0fcd5a124` | input_or_analysis_code |
| E0049 | [docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/input.com](../../../../docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_input.com) | `76ea1cf06afde18eaff6efad630dbd6d92ecba59c2350cbcf5fe8720b0b1bfc9` | input_or_analysis_code |
| E0050 | [docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/input.com](../../../../docs/v2_verification/history/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_input.com) | `874c4216c6c5c885d49628ff73c3829e8b847570106b8b40f5a66d116943cf2d` | input_or_analysis_code |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_Zn_noD3_control_accept_20261005_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_Zn_noD3_control_accept_20261005_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_execution.json) | `d1dd89098be49c77c42919f99bf47d1e73599e0881a086311eda5fd47023207f` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/Zn_noD3_Tight_control_acceptance_20261005.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/Zn_noD3_Tight_control_acceptance_20261005.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_Zn_noD3_Tight_control_acceptance_20261005.json) | `ac77aa548e2cfed334a23da0b334da13a591c147a216586894e52a5c7764a6b8` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_9ec32e81e2826041/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_9ec32e81e2826041/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_main.json) | `f819f4ced2e2227b9cf920901301134d5bdf02ec170656daa4367ec20a0c6be7` | evidence_or_analysis |
| E0054 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/papers/paper_9ec32e81e2826041.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/papers/paper_9ec32e81e2826041.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_paper_9ec32e81e2826041.json) | `03cfd3f79cf3537e427add15b3eded84c46cfae1309962752708a69d9db30c11` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/reviews/paper_9ec32e81e2826041.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/reviews/paper_9ec32e81e2826041.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_paper_9ec32e81e2826041.json) | `d1e6fe37516f16601ddaac16ca0cca4542eca5261ad6183f58849aca4b5102ec` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_zinc_source_transition_review_20260930.json) | `91c1bc69948bab44e74ba4085b636e7167e14fcea23501e8a4d6199fc917b847` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_source_transition_spdf_20260930_a02.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_zinc_source_transition_spdf_20260930_a02.json) | `3d3f3efd5c244dbda21d08e067f129efeb376af70e4d6c9a206a6d9219d4df5b` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_naomo_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_zinc_naomo_audit.json) | `4f99ea8bb106eee893122a59f7186e5024927a9fe5fe2a20b5bc87c8178e12e0` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_perpendicular_naomo_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_zinc_perpendicular_naomo_audit.json) | `4b4a9820671ac409ffe2b9746642f06f0325e7a94ab6d9ba176cabad33a471ea` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/ZN_REVIEW_FOLLOWUP_RECEIPT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/ZN_REVIEW_FOLLOWUP_RECEIPT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_ZN_REVIEW_FOLLOWUP_RECEIPT.json) | `8edf5321e81ce18bfc52e3a2f8aa7c39fdd305c95b0c6f463b509b8cf565ba55` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/ZN_STATIONARITY_FOLLOWUP_RECEIPT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continue_all_20261005T0407Z/ZN_STATIONARITY_FOLLOWUP_RECEIPT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_ZN_STATIONARITY_FOLLOWUP_RECEIPT.json) | `2733c7b86e941ad405d793f3e4b3fabf2635ed497e5c8f27b2dfe925ed7e6f47` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_Fig2_saved_NAO_crosscheck_20261005_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_Fig2_saved_NAO_crosscheck_20261005_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_execution.json) | `5f8dd373f2451c48f7d7e530c3ecf5f7c39e5158689642e4e034f65215e36506` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_perp_noD3_ReadFC_Tight_control_20261005_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_execution.json) | `c8ad03179eb00db686f2f92ff251a07b03c21105a99b1aa20665a157f5af1e19` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_zinc_NAO_subspace_review_20260930.json) | `0a398a713b5fbed0a984e4f9dc0288001b89fdb8b72806fd84d3c0d841396df4` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/v2_execution_20260929/zinc_NAO_subspace_diagnostic_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_zinc_NAO_subspace_diagnostic_20260930.json) | `9dd30201c28903299576354e43e14910ef0e8242452e9ddb45daa220dbccdcd5` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_paper_9ec32e81e2826041_PROVENANCE_CLOSURE_20261002.json) | `e2135b09c97bcf707ca4514bcd6cf1304ce4fb5dd82f44e5876b8482c928f408` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_ZN_NAO_VALENCE_ROOT_CAUSE_20261002.json) | `7d99ab41fc43179cc7ac9fa057533a827c515c882b821d63079102183865ddb3` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_9ec32e81e2826041/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_9ec32e81e2826041/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_supplementary_001.json) | `aeca76a13313f90dfa3a744e8381475fa325a07810aef1f768cc05127d1aa5ce` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_NAO_subspace_diagnostic_20260930_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_NAO_subspace_diagnostic_20260930_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_execution.json) | `7a522e0cd050e78a562bdeb633b432a5718deb4609e29460217eed7358907566` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_coplanar_D3geom_NAOMO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_coplanar_D3geom_NAOMO_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_native_excerpt.json) | `1fd6245eae07bbddd8175bbc57cd9da2b36eae7ff0716f1fdbea3b69d82b5afd` | native_output |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_perpendicular_D3geom_NAOMO_diagnostic_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_perpendicular_D3geom_NAOMO_diagnostic_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_native_excerpt.json) | `8fbbc154b8f743b2ea39951caa53498e37563437146c41a3f7b6803eaac89e2b` | native_output |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/perpendicular_PBE0_D3geometry_canonical_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/perpendicular_PBE0_D3geometry_canonical_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_input.com) | `1c9728d110b2af33088ade7e7c4ddd9adcc55e3911f647c23459bc52e4ea5c73` | input_or_analysis_code |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/coplanar_PBE0_D3geometry_canonical_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/coplanar_PBE0_D3geometry_canonical_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_input.com) | `506b12b2a70595c239bbac25274419fb05bc8d47cfa0988b5aca2201997831d8` | input_or_analysis_code |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_execution.json) | `84050b50869f7e8fe601340fec2ec6e23375d69954be83df7e84578333eb0b90` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/provenance/v2_zinc_source_transition_spdf_20260930_a02_hpc_submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/provenance/v2_zinc_source_transition_spdf_20260930_a02_hpc_submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_v2_zinc_source_transition_spdf_20260930_a02_hpc_submission.json) | `9816cd598979360c1909e304b0123b8a7a1320abcd6ed7231f7139d7551e0817` | evidence_or_analysis |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/coplanar_PBE0_D3geometry_canonical_TD10/checkpoint.chk) | `66a32a32db257054a8d5285c45370f6d7ba876e9f7b0ed0fca4ba718e9ca3c79` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/fchk_overlap_spdf_20260930.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/fchk_overlap_spdf_20260930.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_fchk_overlap_spdf_20260930.py) | `5058572a4cdbc46a0ce90339d99f03722d2e47a3efc2c4a15e0defcae328a92e` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/wavefunction_calibration.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/wavefunction_calibration.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_wavefunction_calibration.json) | `2557e5fd006a44ecd97e2f32bc828ddd80ee0774ff442e9c40950496277e4b37` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/transition_character.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/transition_character.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_transition_character.json) | `46332697083e9d3e871984b5d4823ca931a47f20b92fff216bd90813da798e7a` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/transition_density.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/transition_density.npz) | `9144b3d77d724beb2df9aef6a4011a4576fffbde3a54552b2f7e1a0ee7987b8c` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/self_overlap.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/coplanar_PBE0_D3geometry_canonical_TD10/self_overlap.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_self_overlap.json) | `dc2bd729eade6a6868ad7d1646dcd5eb44acfa95b07161057178a0919a4a2201` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/perpendicular_PBE0_D3geometry_canonical_TD10/checkpoint.chk) | `7e83dbd2fbfa386f7bec75ca588c52d8136d6869a08e4eabf1f83287fd08cb16` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/wavefunction_calibration.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/wavefunction_calibration.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_wavefunction_calibration.json) | `73bdbb7eb212bd5d52c42397f49facd7c0a095a116a90f08b0069e823836429b` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/transition_character.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/transition_character.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_transition_character.json) | `ba4f8214f15aeb04a1bb8fc512ee91bd1814bac87a1d22902ba23b212709bdab` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/transition_density.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/transition_density.npz) | `4af6b1aaa1b02d2db3fd8d12a43a571a6abf36238e4a4fcff2a2d69b6be8193c` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/self_overlap.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_zinc_source_transition_spdf_20260930_a02/perpendicular_PBE0_D3geometry_canonical_TD10/self_overlap.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_self_overlap.json) | `89943f375607295c340e40b9b81e256b426dde27ccfff6bae15ee7d4a3b298cf` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/audit_zinc_valence_NAO_20261002.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/audit_zinc_valence_NAO_20261002.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_audit_zinc_valence_NAO_20261002.py) | `71bd0cae472a5a48b900ebe242c8c78cb961dd471c4a43ddde6c22e541ff96d3` | input_or_analysis_code |
| E0088 | [.software_cache/installations/gaussian/g16/install/g16/g16](../../../../.software_cache/installations/gaussian/g16/install/g16/g16) | `384f3baca38297d3f11ed2168bb9be836778fa4c5f5d07cb38751e3ed1a66db5` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/perpendicular_PBE0_D3geometry_canonical_TD10/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/perpendicular_PBE0_D3geometry_canonical_TD10/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/coplanar_PBE0_D3geometry_canonical_TD10/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/inputs/coplanar_PBE0_D3geometry_canonical_TD10/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_coplanar_D3geom_NAOMO_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_coplanar_D3geom_NAOMO_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_input.com) | `7df934b454ea7f8e9de45291ef8552752146793410aba3f0f692e884b02617f6` | input_or_analysis_code |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_perpendicular_D3geom_NAOMO_diagnostic_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/outputs/v2_perpendicular_D3geom_NAOMO_diagnostic_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9ec32e81e2826041/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_input.com) | `7df934b454ea7f8e9de45291ef8552752146793410aba3f0f692e884b02617f6` | input_or_analysis_code |
| N0093 | [tasks/v2_autonomous_research/paper_9ec32e81e2826041/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_9ec32e81e2826041/evaluation/reference_key_points.json) | `f11616779cce919d23152d6969beec1adf23b203aa0d87563a1c67f77f0bf690` | latest_review_evidence |
| N0094 | [tasks/v2_autonomous_research/paper_9ec32e81e2826041/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_9ec32e81e2826041/evaluation/reference_conclusions.json) | `71e146bf39482aefdc689f5dae10299242dba7ab6f8e72455f62666fdb7aa0b8` | latest_review_evidence |
| N0095 | [tasks/v2_autonomous_research/paper_9ec32e81e2826041/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_9ec32e81e2826041/evaluation/scoring_rules.json) | `ecaa584587ebb0388c5597e11fbe9996dcb09204e23a330acc847f669e020752` | latest_review_evidence |
| N0096 | [tasks/v2_autonomous_research/paper_9ec32e81e2826041/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_9ec32e81e2826041/evaluation/reference_validation_plan.md) | `075afad523e277fafc4c59929500967fed592c5976c402d64634cf62401ce118` | latest_review_evidence |
| N0097 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/scoring_rules.json](scoring_rules.json) | `ecaa584587ebb0388c5597e11fbe9996dcb09204e23a330acc847f669e020752` | latest_review_evidence |
| N0098 | [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `075afad523e277fafc4c59929500967fed592c5976c402d64634cf62401ce118` | latest_review_evidence |
| N0099 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0100 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/agent_input/task.md](../agent_input/task.md) | `6cb7dd6284e88143887c55dda248b51c552df1aa651041e0441507aef94c0111` |
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_key_points.json](reference_key_points.json) | `f11616779cce919d23152d6969beec1adf23b203aa0d87563a1c67f77f0bf690` |
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_conclusions.json](reference_conclusions.json) | `71e146bf39482aefdc689f5dae10299242dba7ab6f8e72455f62666fdb7aa0b8` |
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/scoring_rules.json](scoring_rules.json) | `ecaa584587ebb0388c5597e11fbe9996dcb09204e23a330acc847f669e020752` |
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/critical_failures.json](critical_failures.json) | `e586aa2985efae07c40f8f0066f153978a6cc6a4bed2f7a586c5b2b4d6f58e66` |
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/evidence_map.json](evidence_map.json) | `c389779d81d914d1dfb62f8f42eaca463d059b6a93c6aa3982fca19edad42b81` |
| [tasks/v2_paper_reproduction/paper_9ec32e81e2826041/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `075afad523e277fafc4c59929500967fed592c5976c402d64634cf62401ce118` |

## Current scoring migration — 2026-10-19
Active policy: paper_science_v2, 100 binary scientific-result points with intermediate and final conclusions. Active rule/reference files supersede historical scoring weights or freezes. No process score or multiplier remains. This migration is not new computation or new chemical acceptance; independently strict frozen-scope status remains unchanged. Preserved limitations: Verified S1=3.1097/2.4524eV versus source3.1097/2.4526; f0.0883/0.0132. Zn4p2.094985/8.547679% versus2.1/8.5%; equivalent NAO implementation is checked, not claimed identical to private author binary. Carbene C2p53.539807 versus53.4% residual retained. D3/noD3 G differences-0.047259/+4.681266kJ/mol versus-0.1/+4.8; near-zero ordering and exact populations not robust.

## Scoring-contract repair — 2026-10-19, round 3

- PR retains the explicitly disclosed D3BJ/no-D3 300 K comparison; AR independently scores the physical thermal-competition result without that prescribed source ablation.

The source and native calculations above remain unchanged historical evidence. Active mode-specific rules govern current scoring; this edit does not certify a new chemistry run or alter strict acceptance.

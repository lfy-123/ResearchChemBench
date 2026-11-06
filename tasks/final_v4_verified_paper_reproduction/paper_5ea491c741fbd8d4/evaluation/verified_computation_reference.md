# 2026-10-28 V3 scope and evidence reuse

Retain the authenticated isoxazole crystal-packing question. Eight final outcomes comprise five surface fractions, the directional contact network, quantitatively defined aromatic packing and a distinct interpretation of surface prevalence; no new energetic task or chemical identity is introduced.

- `r_hh_fraction`: H···H Hirshfeld contact area; evidence: source_main, source_cif, native_surface.
- `r_ho_fraction`: H···O/O···H Hirshfeld contact area; evidence: source_main, source_cif, native_surface.
- `r_cc_fraction`: C···C Hirshfeld contact area; evidence: source_main, source_cif, native_surface.
- `r_hn_fraction`: H···N/N···H Hirshfeld contact area; evidence: source_main, source_cif, native_surface.
- `r_ch_fraction`: C···H/H···C Hirshfeld contact area; evidence: source_main, source_cif, native_surface.
- `r_contact_network`: Intermolecular contact network and its distinction from intramolecular contacts; evidence: source_main, source_cif, verification_records.
- `r_aromatic_packing`: Quantitative physical description of the aromatic packing contact; evidence: source_main, source_cif, verification_records.
- `r_surface_contribution_interpretation`: What the calculated surface distribution establishes about packing; evidence: source_main, source_cif, native_surface.

Known limits: CE25.8/OCC is an evidenced substitute for CE17.5, not exact software/session identity; Deposited Z geometry conflicts with the source E name; centroid norm and source 3.3883 angstrom label conflict; Exact source hydrogen policy and crystallographic covariance are unavailable; no energy ranking or lattice thermodynamics follows; No new V3 semantic calibration or blind run. No new calculation or V3 scientific PASS is asserted. All text below is preserved historical evidence, including obsolete scoring statements; the active V3 JSON files govern scoring.

---

# V2 验证计算参考：Isoxazole / CCDC2445596 晶体相互作用

论文：`paper_5ea491c741fbd8d4`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：完整实测晶体上的真实 Hirshfeld 网格积分恢复了五类接触百分数至论文一位小数；同一 CIF 的实际相邻分子/环几何支持滑移堆积与接触解释。题目明确排除把表面积直接当能量，故不要求另算未披露的晶格热力学。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

What intermolecular interactions account for the observed packing of the specified isoxazole crystal, and how strongly can the available evidence distinguish their roles? Establish which interpretations are supported, contradicted or unresolved within the authenticated crystal and the limits of the chosen evidence.

冻结题面中的科学目标：

What intermolecular interactions account for the observed packing of the specified isoxazole crystal, and how strongly can the available evidence distinguish their roles? Establish which interpretations are supported, contradicted or unresolved within the authenticated crystal and the limits of the chosen evidence.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The source attributes packing of the measured P21/c crystal to C–H···O motifs and aromatic contacts (§3.2–3.3, Figs.2–5). It uses CrystalExplorer 17.5 Hirshfeld surfaces and fingerprints, with hydrogen distances normalized to neutron values. It reports H···H 38.7%, O···H/H···O 29.1%, C···C 13.4%, N···H/H···N 9.7% and C···H/H···C 6.2%; these are author-derived surface fractions, not stabilization energies or required answers. Section 3.2 (physical PDF p4) labels 3.3883(6) angstrom as a centroid-centroid distance for Cg(1) = C9/C10/N1/O2/C11 and Cg(2) = C2/C3/C4/C5/C6/C7, with symmetry 1-X,-1/2+Y,1/2-Z. This is the author-reported value and label, not an independently certified target. Verify the full mapping and physical quantity definition against the supplied CIF, distinguishing the centroid norm from centroid-to-plane projections; document any evidenced source discrepancy. The separate isolated-molecule route is Gaussian 09/B3LYP/6-311+G(d,p), while another method sentence says 6-31+G(d,p); document that ambiguity. Neither the isolated orbital gap nor fingerprint percentages prove an interaction-energy ranking. Reproduce and critically assess the disclosed contact interpretation where the actual source data permit it. Pair-energy calculations, any cutoff comparison and additional robustness analyses would be your investigations, not author-reported protocols. No force-field, surface package or quantum code is asserted available merely because the authors used it.

Source interpretation and ambiguities: the methods continuation on physical PDF p3 gives a d_norm display range of -0.18 to 1.4 and labels it a.u.; p4 gives -0.676 to 1.415 and labels it angstrom. d_norm is a normalized distance quantity; the two ranges and the dimensional labels are inconsistent as reported. Record the definition and display settings actually used, and do not treat either printed interval as a certified numerical target or tolerance. In section 3.2, the S(7) C6-H6...O3 motif is intramolecular, whereas the C8-H8...O3 and C12-H12B...O2 contacts form the intermolecular R2^2(9) motif. Verify source labels and symmetry operations against authenticated coordinates before using them. The red/blue triangles on the shape-index surface and flat curvedness regions (pp4-6, Figs2-5) are the authors' evidence for a pi-packing interpretation; they do not measure stabilization energies or establish an energetic ordering. These are disclosed source claims to assess, not required outcomes.

Source attachments provided for PR: data/author_sources/2445596_original.cif preserves the full user-supplied deposition, and data/author_sources/isoxazole_mmc1.zip preserves the independently supplied 1a.cif. data/author_sources/checkcif_observations.md discloses the four-page checkCIF text with source hash (the official public-package contract excludes PDFs); data/author_sources/isoxazole_mmc3.docx contains Figs S1-S5 (NMR, chromatography/mass and UV-vis material) and Tables S1-S3 (source XRD/DFT intramolecular geometry comparisons). These are author disclosures, not newly generated evidence. Their broader spectroscopy and molecular-property content does not add tasks to the crystal-packing question. Use the common minimal CIF for an auditable structure baseline; the original retains source attribution and ancillary refinement data.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_5ea491c741fbd8d4/documents/main.pdf](../../../../papers/paper_5ea491c741fbd8d4/documents/main.pdf) | `7621bdebf4659fb6c1e67f15c6ceda8dccbb4442eec850819fd613db4bc8ba6a` |
| [papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf](../../../../papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf) | `4d381cbbbbade30dc691faf5ca339844b62b609a221568ee0f9a7983b29299a5` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Source crystallographic contacts and Hirshfeld area analysis actually reproduced on complete measured CIF. CrystalExplorer25.8 bundled OCC stockholder engine is a declared substitute for17.5; raw-H and neutron-like C-H1.083A models, three grids and8/12A environments provide measured comparability evidence.

1. 使用已补齐的 CCDC 2445596 原始 CIF 与完整 SI，核对 C12H11NO3、27 原子、300 K、P21/c、Z=4、原子标号与对称操作；保持沉积结构的 Z 构型，不按文章 E 名称擅改坐标。

2. 在真实晶胞/邻居下重算分子内 S7、分子间 R2²9 接触和芳环几何。直接区分质心范数 3.7482107 Å 与质心到平面投影 3.3883652 Å；后者而非前者恢复源 3.3883，环夹角约 3.24986° 对源 3.25°。

3. 用 CrystalExplorer 25.8 所带 OCC stockholder 引擎计算 Hirshfeld 面，以面积积分得到各接触比例；该程序为源 17.5 的公开替代，等价性由真实源量与控制支撑，不假称二进制相同。

4. 完成 raw-H 与 C–H=1.083 Å 归一化、三网格、8/12 Å 环境及密度表控制，核对原生网格拓扑/精度。细网格 H-H/H-O/C-C/H-N/C-H=38.7026668/29.1110503/13.3759770/9.6595142/6.1714965%，全部四舍五入为源 38.7/29.1/13.4/9.7/6.2。

5. 保留 CIF 边际 ESD 的条件传播、网格与氢位置敏感性；以接触和表面证据解释实际晶体堆积，不用接触面积排名冒充结合能或晶格能。旧“待下载 CIF/表面待计算”状态由本记录明确替代。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

### 最近一次原生有效性复核

本轮读取 OCC 原生日志的 191×104×146 网格、72797 顶点/72792 面、254.376 Å² 表面积，以及 surface_pilot_results.json 和拓扑精度报告；源 CIF 在场。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| H-H,H-O,C-C,H-N,C-H area% | [38.7,29.1,13.4,9.7,6.2] | [38.7026668,29.1110503,13.375977,9.6595142,6.1714965] | All five round to the source1-decimal values at fine grid. Finer quadrature gives similarly38.7016/29.1130/13.3755/9.6566/6.1724. Grid/environment/density-table controls are retained; no invented broad tolerance. |
| Source-labelled centroid distance,A | 3.3883 | {"centroid_norm":3.74821071165,"centroid_to_plane":3.388365195,"plane_angle_deg":3.2498635} | Current task specifically requires verifying this quantity-definition conflict. Same source rings/symmetry reproduce source projection and3.25deg ring angle. Do not relabel norm as matched; a source-label correction is supported by actual CIF geometry. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Authentic source crystal and correctly related representations

冻结要求：Authenticate CCDC2445596 source bytes, measured cell/space group, composition, occupancy/disorder and graph-to-CIF mapping. Check each investigated representation and its relationship to the source. Do not accept arbitrary placed dimers or checkCIF images as crystal coordinates. Geometry relaxation may be a deliberate study but cannot be silently substituted for measured packing. Read actual submitted files and tool provenance, resolve identifiers and recompute the quantities supporting the claim. No old scalar target or universal uncalibrated tolerance applies. Missing evidence cannot be scored as an indistinguishable result. Judge alternative valid routes by the same scientific standard, not by agreement with the author or completion of a private reference matrix. Award full criterion credit only when the full substantive requirement of that criterion in the public scientific question is supported. Narrowing addressed_scope does not erase missing coverage. Independently valid partial evidence earns only the corresponding credit; a fully met independent criterion is not automatically capped because another criterion is incomplete. Award no credit to the affected claim when essential identity, validity or evidence is absent; fluent explanation does not repair it. These are judgment anchors, not a calibrated numerical equivalence threshold. The supplied minimal CIF and its graph map are valid source-input candidates, with exact original/derived hashes in source_recovery_20260930.json. Do not require an investigator to reacquire unavailable external bytes when the authorized source input is present. Input authentication alone cannot satisfy quantitative support or interpretation criteria. Treat the provided source geometry as the physical identity: its 7=8 double bond is Z by CIP although the article uses E. Do not penalize faithful deposited geometry for disagreeing with that name, or require rotating/rebuilding the crystal to fit the old E-labelled graph. Historical E-labelled monomer evidence requires actual geometry/mapping review before any reuse.

当前复审：真实源晶体、映射与Z构型

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "27-atomC12H11NO3,300K,P21/c,Z4,source atom map and original coordinates retained; depositedZ configuration not changed to article E name."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "rationale": "Deposited CCDC2445596 geometry authenticated; Z CIP preserved despite E label, source H constraints explicit."
  },
  {
    "rationale": "Deposited CCDC2445596 geometry authenticated; Z CIP preserved despite E label, source H constraints explicit."
  }
]
```

### kp_quantitative_support — Reproducible, relevant quantitative evidence

冻结要求：Check numerical definitions, object coverage and raw evidence appropriate to the submitted analysis. Area claims need a valid area measure rather than atom-pair counts; energy claims need consistent composition, geometry, states and energy reference with demonstrated numerical/basis adequacy. These are conditional standards, not a requirement to compute both surface areas and energies. No fixed cutoff, CP sequence, pair count or surface method is mandatory. Read actual submitted files and tool provenance, resolve identifiers and recompute the quantities supporting the claim. No old scalar target or universal uncalibrated tolerance applies. Missing evidence cannot be scored as an indistinguishable result. Judge alternative valid routes by the same scientific standard, not by agreement with the author or completion of a private reference matrix. Award full criterion credit only when the full substantive requirement of that criterion in the public scientific question is supported. Narrowing addressed_scope does not erase missing coverage. Independently valid partial evidence earns only the corresponding credit; a fully met independent criterion is not automatically capped because another criterion is incomplete. Award no credit to the affected claim when essential identity, validity or evidence is absent; fluent explanation does not repair it. These are judgment anchors, not a calibrated numerical equivalence threshold. For a submitted source-surface comparison, the source d_norm display ranges/labels conflict (p3 versus p4); neither is a certified acceptance interval. Judge the defined normalized quantity, reproducibility and disclosed comparability, not matching a color scale. For any claimed ring-distance comparison, distinguish centroid-centroid distance from each centroid-to-the-other-ring-plane projection, with explicit atom labels, cell, symmetry operation and lattice translation. The author labels 3.3883(6) angstrom as a centroid distance, but the existing source-coordinate audit records 3.74821071165 angstrom for that centroid distance and 3.38836519500 angstrom for the original isoxazole centroid to the transformed phenyl plane. Preserve this source quantity-definition conflict; do not impose the printed value as a correct centroid target. Accept independently evidenced correction of a physical-quantity label without requiring agreement with the source. Numerical proximity does not establish an author erratum. See crystal_distance_definition evidence for the exact mapping and raw records; this is conditional on the submitted claim, not a hidden required AR ring analysis.

当前复审：真实面元积分

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Native surface area integration, not pair counts; physical neighboring molecules and geometry are represented."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "rationale": "Six raw surfaces and actual area quadrature plus density controls retained. New source-CIF uncertainty propagation distinguishes centroid and plane quantities."
  },
  {
    "rationale": "Six raw surfaces and actual area quadrature plus density controls retained. New source-CIF uncertainty propagation distinguishes centroid and plane quantities."
  }
]
```

### kp_scientific_interpretation — Evidence discriminates the proposed packing explanation

冻结要求：Assess whether the submitted evidence can support, falsify or limit its intermolecular interpretation. Inspect selection and relevant neglected interactions or modeling confounds in relation to the claim, not a preselected contact list. An alternative physical analysis may earn full credit. Geometric overlap or high contact frequency alone is not an interaction-energy decomposition or causal stabilization proof. Read actual submitted files and tool provenance, resolve identifiers and recompute the quantities supporting the claim. No old scalar target or universal uncalibrated tolerance applies. Missing evidence cannot be scored as an indistinguishable result. Judge alternative valid routes by the same scientific standard, not by agreement with the author or completion of a private reference matrix. Award full criterion credit only when the full substantive requirement of that criterion in the public scientific question is supported. Narrowing addressed_scope does not erase missing coverage. Independently valid partial evidence earns only the corresponding credit; a fully met independent criterion is not automatically capped because another criterion is incomplete. Award no credit to the affected claim when essential identity, validity or evidence is absent; fluent explanation does not repair it. These are judgment anchors, not a calibrated numerical equivalence threshold. When source motifs are invoked, distinguish intramolecular S(7) from intermolecular R2^2(9). Source shape-index/curvedness patterns support a packing interpretation but do not supply an energy ranking. Other valid physical explanations remain eligible; the source motifs are not a hidden required AR contact list.

当前复审：晶体接触与滑移堆积

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "IntramolecularS7 separated from intermolecularR2²9 and slipped aromatic contacts; source major packing interpretation supported without energy ordering."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "rationale": "C-H...O ring motifs and offset aromatic contacts are geometrically supported; surface areas do not rank stabilization energies."
  },
  {
    "rationale": "C-H...O ring motifs and offset aromatic contacts are geometrically supported; surface areas do not rank stabilization energies."
  }
]
```

### kp_uncertainty_limits — Claim-appropriate uncertainty and scientific scope

冻结要求：Evaluate uncertainty from actual data quality and the chosen representation, numerical analysis and coverage. Require a quantitative or justified bounded resolution where differences support a claim; do not invent a universal tolerance. A finite molecular interaction analysis cannot alone establish bulk free energy or biological activity. Unavailable coordinates are a prerequisite failure, not evidence that mechanisms are indistinguishable. Read actual submitted files and tool provenance, resolve identifiers and recompute the quantities supporting the claim. No old scalar target or universal uncalibrated tolerance applies. Missing evidence cannot be scored as an indistinguishable result. Judge alternative valid routes by the same scientific standard, not by agreement with the author or completion of a private reference matrix. Award full criterion credit only when the full substantive requirement of that criterion in the public scientific question is supported. Narrowing addressed_scope does not erase missing coverage. Independently valid partial evidence earns only the corresponding credit; a fully met independent criterion is not automatically capped because another criterion is incomplete. Award no credit to the affected claim when essential identity, validity or evidence is absent; fluent explanation does not repair it. These are judgment anchors, not a calibrated numerical equivalence threshold. For the recorded ring-distance conflict, printed source uncertainty and long decimal output must not be transferred to a different physical quantity. The archived audit did not propagate cell/coordinate uncertainties; it supplies no calibrated acceptance interval. A justified alternative definition or symmetry-equivalent representation must be checked on its own evidence.

当前复审：网格/H长度/环境控制；最终结论仅为几何和表面支持的相互作用解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Real grid,H-normalization,radius,density-table and mesh-precision controls; CIF marginal-esd propagation labelled conditional."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "rationale": "Marginal-esd bound is diagnostic, not calibrated covariance. Native ASCII surface seams and disclosure of CE version/H treatment retained."
  },
  {
    "rationale": "Marginal-esd bound is diagnostic, not calibrated covariance. Native ASCII surface seams and disclosure of CE version/H treatment retained."
  }
]
```

### conclusion_investigation — What intermolecular interactions account for the observed packing of the specified isoxazole crystal, and how strongly can the available evidence distinguish their roles? Establish which interpretations are supported, contradicted or unresolved within the authenticated crystal and the limits of the chosen evidence.

冻结要求：Answer the specified question within the explicitly investigated domain. Supported, refuted and evidence-sufficient unresolved conclusions are eligible for equal credit. Scope reductions must be explicit; untested parts cannot be generalized. Distinguish complete scientific non-identifiability from missing input or failed calculations. Do not require any author-specific hypothesis count, control matrix, method, winner or numerical answer. Historical package PASS is not V2 evidence. Completion and coverage: the full question concerns interactions in the authenticated observed crystal. An isolated monomer, a cell-only model or a source-input validation report covers only a prerequisite or limited molecular property, not the packing question. Reducing addressed_scope does not convert that partial evidence into whole-task completion or full credit for unaddressed criteria. Credit independently valid parts according to what they establish. An adequately investigated, evidence-supported inability to distinguish interactions can be a scientific conclusion; unavailable coordinates or failed calculations cannot establish it. The source crystal and atom map are now supplied and have passed input-identity checks. That check does not answer the interaction question: claim-appropriate scientific evidence, uncertainty and scope remain required. Scientific reference expansion and semantic calibration remain pending; no package text claims an enforced host scheduling gate. An evidenced correction of the source distance label is eligible scientific reasoning, including an evidence-supported unresolved source-label conflict. Resolving that local geometry alone does not complete the packing investigation or prove energetic stabilization. Source disagreement is not itself a failure and no private ring value is a mandatory outcome.

当前复审：kp_identity：真实源晶体、映射与Z构型；kp_quantitative_support：真实面元积分；kp_scientific_interpretation：晶体接触与滑移堆积；kp_uncertainty_limits：网格/H长度/环境控制；最终结论仅为几何和表面支持的相互作用解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Full observed-crystal packing question answered within geometric/surface evidence. Final conclusion identifier is read from current contract if differently named."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "rationale": "Measured packing supports hydrogen-contact network and slipped aromatic contacts. Relative energetic roles remain unresolved; source E/centroid labels cannot be forced onto the coordinates."
  },
  {
    "rationale": "Measured packing supports hydrogen-contact network and slipped aromatic contacts. Relative energetic roles remain unresolved; source E/centroid labels cannot be forced onto the coordinates."
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**六次 OCC 内核累计 6.19 秒；所在整批 16.76 秒（相互包含，不相加）；其他分析时长缺失**。

已记录资源：CrystalExplorer/OCC；CE 25.8/OCC；整批记录 4 CPU/16 GiB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)；[补充计时记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/SUPPLEMENTAL_RUNTIME.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0008 · attempt_01/CH1083_010_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/native.log) | OCC:2.55336 | 正常 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0034 · attempt_01/CH1083_015_R12/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/native.log) | OCC:1.38867 | 正常 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0035 · attempt_01/CH1083_015_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/native.log) | OCC:0.8617 | 正常 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · attempt_01/CH1083_025_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/native.log) | OCC:0.300689 | 正常 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0037 · attempt_01/raw015_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/native.log) | OCC:0.824747 | 正常 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0038 · attempt_01/raw025_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/native.log) | OCC:0.256278 | 正常 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

补充的已执行分析/响应计时如下；外层与内层重叠部分不重复相加。
```json
{
  "kind": "Hirshfeld six-export batch timer; overlaps native OCC timers",
  "records": [
    {
      "evidence_id": "E0010",
      "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/surface_pilot_results.json",
      "sha256": "58e86de48cfdfbbd8048cb9cb6bc7483edf028081abd49190f01ad66fdee7761",
      "elapsed_seconds": 16.756749,
      "started_at": "2026-09-30T09:36:17.806887+00:00",
      "finished_at": "2026-09-30T09:36:34.563636+00:00",
      "resources": {
        "cores": 4,
        "memory_gib": 16
      }
    }
  ],
  "note": "Batch timer includes the six OCC engine timings. Do not sum the two."
}
```

## 6. 已知偏差、失败分支和不能外推的结论

文章 E 名称与沉积 Z 几何冲突；3.3883 Å 是近似重现的质心到环平面投影，不是 3.74821 Å 的质心距。不能宣传“这个印刷质心距离已重现”。

```json
[
  "No pair-energy/lattice-free-energy ranking is certified or required. Author session,full covariance and exact17.5 density table are not required private artifacts. Source dnorm display interval conflict is not a numerical target."
]
```


原独立审查的 `material_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Acceptance covers currentV2 measured-crystalpacking and evidence-supported limits only; it does not certify interaction-energy ranking, latticefreeenergy, docking or biochemical claims.",
  "CE25.8-bundledOCC is a documented stockholder-surface substitute for CE17.5. Exact source session/density-table/Hatom-type policy is not recovered; actual6grid/H/radius and densitytable controls support the area/contact conclusions.",
  "Source E naming is inconsistent with authenticated depositedZconfiguration; original CIF coordinates are retained. This is a source-label discrepancy, not permission to rebuild a differentcrystal.",
  "Source3.3883(6)A centroid label conflicts with the exact statedrings/symmetry: centroid3.748210712A, projection3.388365195A. Numerical closeness to the projection does not prove the authors intended correction; both source label and verified physical quantities are recorded.",
  "CIF marginal-esd propagation supplies a conditional first-order diagnostic/envelope, not the absent fullcovariance or a calibrated statisticalconfidenceinterval. Source0.0006A is not transferred to a differentquantity.",
  "dnorm is normalized, not length. Conflicting source display ranges/units are not fitted as numericaltargets. Shapeindex/curvedness and contact area do not measure stabilizationenergy.",
  "ASCII surface seams were diagnosed using retainedoriginalmeshes and explicitprecision controls; welding was a numericalaudit, not silent alteration of originalscientificoutputs.",
  "Strict scientificreference validation is not a blind AR performance evaluation. Sourceinformation is used by validator, not leaked into agentinputs."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_5ea491c741fbd8d4.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_5ea491c741fbd8d4/verified_computation_reference.md)；SHA-256 `bb45d316138957987caad94da22fc1996ed4ef673c405ff87e354c386c41ad89`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_5ea491c741fbd8d4.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_5ea491c741fbd8d4.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_5ea491c741fbd8d4.json) | `9fc1b1a5ee3d2def051f54ce027b78459f6d75b502de5b425533cca2a15094c8` | evidence_or_analysis |
| E0002 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_task.md) | `836e812c3ce5368cc89d0f9cf26998bc860741b3fe4889c64d5753c58b47b24d` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_reference_key_points.json) | `29278488c80d4654ffb263adc044b35ff1103fcbe423651e5fb5683698a634d0` | historical_task_binding |
| E0004 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_reference_conclusions.json) | `25f37ca515231f3d8177437fca911f169cbd17d14cf5379008ce6f3b268681e6` | historical_task_binding |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_audit_2_native_readback.json) | `ef1f45e93e2e7a9a0b0956e810ff714a67de5072fbba619fa5fb56e2340249c1` | evidence_or_analysis |
| E0006 | [papers/paper_5ea491c741fbd8d4/documents/main.pdf](../../../../papers/paper_5ea491c741fbd8d4/documents/main.pdf) | `7621bdebf4659fb6c1e67f15c6ceda8dccbb4442eec850819fd613db4bc8ba6a` | source_document |
| E0007 | [papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf](../../../../papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf) | `4d381cbbbbade30dc691faf5ca339844b62b609a221568ee0f9a7983b29299a5` | source_document |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `891a19d3292aa1f5e19b2b4d2413c34c2bb8d03d31512321aabef6f8d404e269` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/surface.ply](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/surface.ply) | `23cfa154f53e9b3ec7c56ee507fa008b44f316267a239d755898922e699ed97b` | evidence_or_analysis |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/surface_pilot_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/surface_pilot_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_surface_pilot_results.json) | `58e86de48cfdfbbd8048cb9cb6bc7483edf028081abd49190f01ad66fdee7761` | evidence_or_analysis |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_ASCII_precision_topology_audit/attempt_01/precision_audit_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_ASCII_precision_topology_audit/attempt_01/precision_audit_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_precision_audit_results.json) | `1a9d4bedff030f297e2ecde5e1405498907852b310f85564d712483e1b81ae1b` | evidence_or_analysis |
| E0012 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/inputs/source_crystal.cif](../agent_input/data/inputs/source_crystal.cif)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_source_crystal.cif) | `b22ef7a983d3365a8f5b4bc6abd1654352f86972829b34488b619339cb810ae3` | input_or_analysis_code |
| E0013 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_5ea491c741fbd8d4/FILE_INTEGRITY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_5ea491c741fbd8d4/FILE_INTEGRITY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_FILE_INTEGRITY.json) | `b95ca3ace077f6cbd6b29c26f04a35e6deef1484003e74825cbf9bab841d2b25` | evidence_or_analysis |
| E0014 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_5ea491c741fbd8d4/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_5ea491c741fbd8d4/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_COMPUTATION_COVERAGE.json) | `9919b68f809723fdf5a4133889836035856acf0f022ca5086666790024d810bb` | evidence_or_analysis |
| E0015 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_5ea491c741fbd8d4.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_5ea491c741fbd8d4.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_paper_5ea491c741fbd8d4.md) | `be8b9e258f374e4e68ca43cc17759f3a639e0ad527afc720f28b1591c4737f26` | evidence_or_analysis |
| E0016 | [docs/v2_verification/history/v2_strict_release_20261011/original_files/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/verified_computation_reference.md](../../../../docs/v2_verification/history/v2_strict_release_20261011/original_files/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_verified_computation_reference.md) | `c9f83d64796b3339865c0eab04606e062e389c7dac711f0c637ca715e71ef9b5` | historical_task_binding |
| E0017 | [docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `36ca02c7c8969d1d64690690661d02a92ed46f6f1a45dac6c6b3156bcba82e29` | historical_task_binding |
| E0018 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/legacy_v1_snapshot/evaluation/verified_computation_reference.md.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/verified_computation_reference.md.snapshot) | `cfea0c8dc3d5ff587908124569a81f5e5e3e658dc50f06138677a50b49c34b2d` | historical_task_binding |
| E0019 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_task.md) | `9809103dd85b27e9a99f5c3158734ec219aea478b35c37c9aa47724f50d137bb` | historical_task_binding |
| E0020 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_reference_key_points.json) | `29278488c80d4654ffb263adc044b35ff1103fcbe423651e5fb5683698a634d0` | historical_task_binding |
| E0021 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_reference_conclusions.json) | `25f37ca515231f3d8177437fca911f169cbd17d14cf5379008ce6f3b268681e6` | historical_task_binding |
| E0022 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/agent_input/data/inputs/system.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/agent_input/data/inputs/system.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_system.json) | `d70bbcc0eee6783bd497ee06e68f0156ee4cce62087126f2270791a51f54da21` | historical_task_binding |
| E0023 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_task.md) | `836e812c3ce5368cc89d0f9cf26998bc860741b3fe4889c64d5753c58b47b24d` | historical_task_binding |
| E0024 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_reference_key_points.json) | `29278488c80d4654ffb263adc044b35ff1103fcbe423651e5fb5683698a634d0` | historical_task_binding |
| E0025 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_reference_conclusions.json) | `25f37ca515231f3d8177437fca911f169cbd17d14cf5379008ce6f3b268681e6` | historical_task_binding |
| E0026 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/inputs/system.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/inputs/system.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_system.json) | `d70bbcc0eee6783bd497ee06e68f0156ee4cce62087126f2270791a51f54da21` | historical_task_binding |
| E0027 | [papers/paper_5ea491c741fbd8d4/documents/user_supplied_20260930/isoxazole_mmc1.zip](../../../../papers/paper_5ea491c741fbd8d4/documents/user_supplied_20260930/isoxazole_mmc1.zip) | `59048684e58e1a69bf82c86ab3f440cf7ebfd0550377792f46c97cde65bc9be8` | evidence_or_analysis |
| E0028 | [papers/paper_5ea491c741fbd8d4/documents/user_supplied_20260930/isoxazole_mmc3.docx](../../../../papers/paper_5ea491c741fbd8d4/documents/user_supplied_20260930/isoxazole_mmc3.docx) | `07d9b3d4306e71346983760f7107a71203ee6d27b9d3cdf347e77602fde7b7d3` | evidence_or_analysis |
| E0029 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/author_sources/2445596_original.cif](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/author_sources/2445596_original.cif)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_2445596_original.cif) | `3d0d3db9b4232bd19d56e55705a5a4240af868d5a80151046de71951ec1d8d89` | input_or_analysis_code |
| E0030 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/inputs/source_crystal.cif](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/agent_input/data/inputs/source_crystal.cif)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_source_crystal.cif) | `b22ef7a983d3365a8f5b4bc6abd1654352f86972829b34488b619339cb810ae3` | input_or_analysis_code |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/sequential_closeout_20261007T163751Z/CRYSTAL_INDEPENDENT_NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/sequential_closeout_20261007T163751Z/CRYSTAL_INDEPENDENT_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_CRYSTAL_INDEPENDENT_NATIVE_READBACK.json) | `f65381b01b247aa721687b364901aac06cd550e85eaa130a79e7e4523029069d` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_c28b0a1c549f4575/cases/w12_existing_energy_convention_discrimination/CRYSTAL_distance_uncertainty_results.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_c28b0a1c549f4575/cases/w12_existing_energy_convention_discrimination/CRYSTAL_distance_uncertainty_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_CRYSTAL_distance_uncertainty_results.json) | `02872df37a7a5c43bc1105547e5e2b4354ee052d5ac4209a6bfb1c1d85bf0b81` | evidence_or_analysis |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_native_mesh_topology_area_audit/attempt_01/mesh_audit_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_native_mesh_topology_area_audit/attempt_01/mesh_audit_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_mesh_audit_results.json) | `feed61b1e5048d884f1a724c9fe6f0e91856d7cbb5f7fb1daaf2c1e9d75ab70f` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_native_excerpt.json) | `9036c2a13d31458b055a73f5e2d068d164a05859824056e0e749ff3732632c63` | native_output |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_native_excerpt.json) | `f9269138d84857bada1f54998213108723b7775c6c2b62ca64c9736d25b612c6` | native_output |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `e009d5f7cd141134eac02aba08b2ad158afa9201628d9d61cde1226b4a089be3` | native_output |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_native_excerpt.json) | `e856929076411fd031b31e1fd99282558b31caea502acc2ce266f965d36e9220` | native_output |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_native_excerpt.json) | `ed6108b15d2f66b82d36bf5d829989a1593ca2e38163f0ed04575faf00cd5203` | native_output |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/inside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/inside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_inside.xyz) | `f6b054f18341f85a3a15d4f44851c8bed7d9b90f075536810942dad92200eb57` | input_or_analysis_code |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/outside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/outside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_outside.xyz) | `752726c8cb83dacd781dc3178af4d5a090a0b472e1ca85850de4427853363448` | input_or_analysis_code |
| E0041 | [.software_cache/installations/crystalexplorer/v25.8/squashfs-root/usr/bin/occ](../../../../.software_cache/installations/crystalexplorer/v25.8/squashfs-root/usr/bin/occ) | `35561547019e36104b25d12ddbbaaa75cb16c2df55f20b8d3f917ca61bba322f` | evidence_or_analysis |
| E0042 | [.software_cache/installations/crystalexplorer/v25.8/squashfs-root/usr/share/crystalexplorer/share/occ/basis/thakkar.json](../../../../.software_cache/installations/crystalexplorer/v25.8/squashfs-root/usr/share/crystalexplorer/share/occ/basis/thakkar.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_thakkar.json) | `89395cc8a1fa7091f74d021391e4fd5b713ca147fe3e247868e21f69bea83887` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/surface.ply](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/surface.ply) | `d3eed2abcbfa770c9d30b04f6b4dbf75aa6edeb26f17ed0042eb006e8464131a` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/surface.ply](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/surface.ply) | `91153dd7963aa04bcf8f19fae441ec5ba7f8199223a09d2cd25aed8788a16ca3` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/surface.ply](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/surface.ply) | `3ee12866fa76a720697108abc5698d2a8b83cfa73c4ea458647d4d144dd62e56` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/surface.ply](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/surface.ply) | `a21b90dea9707518927d02c5f7206c05197b1369283f460c27f534c9b15b2cbd` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/surface.ply](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/surface.ply) | `2673867abb7358456c33d7d9dca92b8e2fe66ede8958e1e848c214e43a9f6d34` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_native_mesh_topology_area_audit/attempt_01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_native_mesh_topology_area_audit/attempt_01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_analysis.py) | `5d43986cdcaddcb57374dfc5a6f6699e76ff716a578c98f9baf023fe76ee1427` | input_or_analysis_code |
| E0049 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_scoring_rules.json) | `044c129a1e159dc7193b9932f944ac9dfb6383a57abf87588d3b8c5eb9b4b9a5` | historical_task_binding |
| E0050 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_scoring_rules.json) | `044c129a1e159dc7193b9932f944ac9dfb6383a57abf87588d3b8c5eb9b4b9a5` | historical_task_binding |
| E0051 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_5ea491c741fbd8d4/SOURCE_MANIFEST.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_5ea491c741fbd8d4/SOURCE_MANIFEST.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_SOURCE_MANIFEST.json) | `f89a4d32ec49d9de7a4d222ffa38c3987ca0f6ea929ee56706de0f31b59bc0b9` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/packing.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/packing.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_packing.json) | `8b81e5ec0129a7b5d79d52f14fe990729a7b2037dfd80e752280a28d36863b3f` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/packing.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/packing.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_packing.json) | `6e01b2225aed56a837d8297d5452d317f27d94fe3f8d8491cc0822d557c8af4e` | evidence_or_analysis |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/packing.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/packing.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_packing.json) | `2f0c257718a5d75a2d5ca957eb1a660b3ac0b7ed06b637bdc72cdbdbc7d9c8ea` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/packing.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/packing.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_packing.json) | `e917d07ce8548384a9f78160260ff3b9fb3408e486acfdf4ff2e800e690cebac` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/packing.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_010_R8/packing.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_packing.json) | `9bc05344b7d689478aaf84682b4f8ebc5d7eeb0ad5eee1a2113d92acaed68d6c` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/packing.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/packing.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_packing.json) | `d6a47ed592176f515df4720038902a6bfb85754bd6a1a34602edea2223f6dbc6` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/source.cif](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/source.cif)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_source.cif) | `3d0d3db9b4232bd19d56e55705a5a4240af868d5a80151046de71951ec1d8d89` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/inside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/inside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_inside.xyz) | `958b61d077bee252b02262394b5e4a623d3e7f8b523b884457c94c09aaa5fb5d` | input_or_analysis_code |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/outside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw025_R8/outside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_outside.xyz) | `b5c3838c5a3834de7d382b8fd6cf4785aa8a35841b6a007bf691ecd73d710e0a` | input_or_analysis_code |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/inside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/inside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_inside.xyz) | `958b61d077bee252b02262394b5e4a623d3e7f8b523b884457c94c09aaa5fb5d` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/outside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/raw015_R8/outside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_outside.xyz) | `b5c3838c5a3834de7d382b8fd6cf4785aa8a35841b6a007bf691ecd73d710e0a` | input_or_analysis_code |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/inside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/inside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_inside.xyz) | `f6b054f18341f85a3a15d4f44851c8bed7d9b90f075536810942dad92200eb57` | input_or_analysis_code |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/outside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_025_R8/outside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_outside.xyz) | `752726c8cb83dacd781dc3178af4d5a090a0b472e1ca85850de4427853363448` | input_or_analysis_code |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/inside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/inside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_inside.xyz) | `f6b054f18341f85a3a15d4f44851c8bed7d9b90f075536810942dad92200eb57` | input_or_analysis_code |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/outside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R8/outside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_outside.xyz) | `752726c8cb83dacd781dc3178af4d5a090a0b472e1ca85850de4427853363448` | input_or_analysis_code |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/inside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/inside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_inside.xyz) | `f6b054f18341f85a3a15d4f44851c8bed7d9b90f075536810942dad92200eb57` | input_or_analysis_code |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/outside.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/outputs/v2_CIF_Z_CE258_Hirshfeld_grid_H_baseline_datafix/attempt_01/CH1083_015_R12/outside.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_5ea491c741fbd8d4/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_outside.xyz) | `abf56b20642121ef8a4ba919d8b64d41ca4ce4432cc3b62bb60a2051886b19cc` | input_or_analysis_code |
| N0069 | [tasks/v2_autonomous_research/paper_5ea491c741fbd8d4/agent_input/task.md](../../../v2_autonomous_research/paper_5ea491c741fbd8d4/agent_input/task.md) | `9809103dd85b27e9a99f5c3158734ec219aea478b35c37c9aa47724f50d137bb` | latest_review_evidence |
| N0070 | [tasks/v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json) | `29278488c80d4654ffb263adc044b35ff1103fcbe423651e5fb5683698a634d0` | latest_review_evidence |
| N0071 | [tasks/v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json) | `25f37ca515231f3d8177437fca911f169cbd17d14cf5379008ce6f3b268681e6` | latest_review_evidence |
| N0072 | [tasks/v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json) | `044c129a1e159dc7193b9932f944ac9dfb6383a57abf87588d3b8c5eb9b4b9a5` | latest_review_evidence |
| N0073 | [tasks/v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_5ea491c741fbd8d4/evaluation/reference_validation_plan.md) | `cded5c23e905165ddcd4fadd1eb58f6727a16221fe67038a51bfdb74d7f0a69c` | latest_review_evidence |
| N0074 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json](scoring_rules.json) | `044c129a1e159dc7193b9932f944ac9dfb6383a57abf87588d3b8c5eb9b4b9a5` | latest_review_evidence |
| N0075 | [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `cded5c23e905165ddcd4fadd1eb58f6727a16221fe67038a51bfdb74d7f0a69c` | latest_review_evidence |
| N0076 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0077 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/agent_input/task.md](../agent_input/task.md) | `836e812c3ce5368cc89d0f9cf26998bc860741b3fe4889c64d5753c58b47b24d` |
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_key_points.json](reference_key_points.json) | `29278488c80d4654ffb263adc044b35ff1103fcbe423651e5fb5683698a634d0` |
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_conclusions.json](reference_conclusions.json) | `25f37ca515231f3d8177437fca911f169cbd17d14cf5379008ce6f3b268681e6` |
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/scoring_rules.json](scoring_rules.json) | `044c129a1e159dc7193b9932f944ac9dfb6383a57abf87588d3b8c5eb9b4b9a5` |
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/critical_failures.json](critical_failures.json) | `4ec385ed8c34c778741152e26c49b2db569559cda00fdc91d57f0cbd9f0112be` |
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/evidence_map.json](evidence_map.json) | `d7dd7187468256a3c585cd6af55a4890621112f752b52d1e92c14d0565ef261e` |
| [tasks/v2_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `cded5c23e905165ddcd4fadd1eb58f6727a16221fe67038a51bfdb74d7f0a69c` |

## Current scientific scoring policy — 2026-10-19

Active scoring is paper_science_v2: independent binary intermediate findings and final conclusions total 100. The synchronized JSON files replace historical process weights, partial-credit discretion and obsolete scoring freezes. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE and all recorded residuals/limitations remain; migration performs no new chemical validation. Public input, task_info.json and paper_route.md remain byte-identical. Source-versus-verification quantities are kept distinct; the new tolerances are fixed benchmark criteria, not fitted offsets. Historical reference-stage text above is provenance rather than the current runtime gate.


## Authorized public-contract and scientific-rule repair — 2026-10-19 round3

This repair preserves every preceding historical computation/acceptance statement verbatim. Current scoring remains paper_science_v2,100 independent scientific points. Mode-specific public objects now control AR eligibility; PR retains its disclosed source-baseline targets. Necessary experimental lifetime facts and obsolete process-score prose are repaired in public files where applicable. No source task, original paper, native computation, engine or historical acceptance is changed. Source/verification residuals and uncalibrated method-transfer limits remain; this is not a new chemical validation or online Judge result. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_02/paper_5ea491c741fbd8d4.md.

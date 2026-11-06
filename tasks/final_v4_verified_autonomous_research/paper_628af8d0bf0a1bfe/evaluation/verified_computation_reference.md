# 2026-10-28 second review: response-definition clarification

Two-ring means are explicit local verification aggregates, not an authenticated author scalar aggregation. E0050 current evidence is for 4a only; 4c is supported by mapped shielding. Scores, numeric policy and scientific scope are unchanged.

---

# 2026-10-28 V3 final-results scope and evidence reuse

The full isolated neutral-singlet 4a/4c central-pentalene magnetic comparison is unchanged. Five independent final propositions cover individual magnetic assignments, paired contrast, localization and the bounded substituent explanation; the former integrated synthesis duplicates these results and has no separate score. AR selects the response route; PR retains the disclosed source baseline and its method/plane ambiguities.

r_response_4a/r_response_4c and r_pair_contrast reuse the atom-mapped native tensor records E0047/E0048/E0049: source-frame ring means 23.19515/19.20415 ppm, contrast +3.991 ppm; matched relaxed SI/main-basis contrasts +4.00737/+3.96152 ppm and face/plane variants about 3.9405–4.0981 ppm. r_central_attribution reuses E0050 final physical current export (48 directional queries; all 8 central bonds paratropic) with its declared mixed 18-MO limitation, together with localized shielding. r_substituent_interpretation reuses actual paired structural/response comparisons including the constrained common-core contrast +5.87040 ppm; that extension is not a free minimum or a unique causal decomposition. Existing active V2 rules have no numeric gates; historical ±2 ppm is retained only in historical prose, not newly reinstated or changed.

Evidence gaps / limits: Main caption and SI disagree on NICS basis; exact author plane fitting atoms/subversion are not fully specified; Current export uses a transparent mixed nominal 18-MO approximation; it is not proof of the unpublished author pi-only selection or a full current-topology equivalence; The common-core comparison does not uniquely separate substituent electronics from all peripheral/relaxation contributions; explanation is bounded association

This edit performs no new calculation or scientific revalidation. Only scoring_rules.json defines current scoring. All historical text below is preserved verbatim; its PASS labels and earlier scoring policies are historical, not a new full V3 pass.

---

# V2 验证计算参考：4a/4c pentalene 磁响应

论文：`paper_628af8d0bf0a1bfe`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：完整两分子的源 M06-2X 结构/磁屏蔽路线及主文/SI 基组差异控制存在。实际 NICS 为 23.19515/19.20415 ppm，对源23.6/19.2；差值约4 ppm以及两者顺磁响应符号均保留。没有依靠“正常退出”判断磁性。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

Determine whether the two supplied benzothiophene-fused pentalenes differ in molecular magnetic response associated with their central pentalene unit. Develop and test an interpretation of any difference, or establish a defensible limit on what can be distinguished, and assess what your evidence supports about antiaromatic character within this pair. Neither a response ordering nor a substituent mechanism is given.

冻结题面中的科学目标：

Determine whether the two supplied benzothiophene-fused pentalenes differ in molecular magnetic response associated with their central pentalene unit. Develop and test an interpretation of any difference, or establish a defensible limit on what can be distinguished, and assess what your evidence supports about antiaromatic character within this pair. Neither a response ordering nor a substituent mechanism is given.

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_628af8d0bf0a1bfe/documents/main.pdf](../../../../papers/paper_628af8d0bf0a1bfe/documents/main.pdf) | `327d99aeb6698b39bc1833dec1bb95f244445ee173fb51d060aa17ef6dcf52a1` |
| [papers/paper_628af8d0bf0a1bfe/documents/supplementary_001.pdf](../../../../papers/paper_628af8d0bf0a1bfe/documents/supplementary_001.pdf) | `7d4e1b91fc4c4501b692d2b1804669e276daaf77502ac8755e5735dac565aec1` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

M06-2X/6-31++G(d) opt/freq followed by SI M06-2X/6-311+G(2d,p) NICS. NICS=-n^T sigma n at1.7A above each five-carbon centroid. Main/SI basis and plane wording ambiguity is explicitly investigated with reproducible atom sets/transforms; publicpyAroma replay is a justified implementation check.

1. 核对 4a/4c 完整含 CF3/OMe 结构与 64/60 原子、q=0 单重态。M06-2X/6-31++G(d) Opt/Freq 给出 186/174 正模，源图、环原子集合及坐标框架冻结。

2. 按 SI M06-2X/6-311+G(2d,p) 计算实际屏蔽张量，在每个五碳环质心外 1.7 Å 定位探针；用 NICS=−nᵀσn 及两个环的算术平均，明确法向、符号和投影。

3. 两环均值为 23.19515/19.20415 ppm，对源 23.6/19.2；源方法差约 3.991 ppm。保留同一量的历史 ±2 ppm 规则，但小差的可靠性由实算控制独立支持。

4. 核收正文/SI 基组、两面/平面定义、pyAroma 4.1 公开实现重放及实际几何/电子控制；已算受约束共同核心差 5.8704 ppm 明确标为约束支路，不称自由最低点。匹配定义下约 3.94–4.10 ppm 的差保持。

5. 以两分子均呈正的中央磁响应、4a 更强作为有限结论，结合电子/几何证据谈反芳香性关联；单一标量不等于唯一因果分解或所有芳香性定义。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

### 最近一次原生有效性复核

本轮原生两条 Gaussian NICS 日志均正常结束，真实 Bq 完整屏蔽张量与探针坐标在日志中；方法来源独立读自 SI：NICS M06-2X/6-311+G(2d,p)，主文写6-31++G(2d,p)，明确分列。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Two-ring mean NICS(1.7)zz,ppm | [23.6,19.2] | [23.19515,19.20415] | Residuals-0.40485/+0.00415 within unchanged same-object historical±2ppm; actual matched controls independently preserve the contrast and are not inferred merely by overlap of±2bands. |
| 4a-minus4c contrast,ppm | 4.4 | 3.991SI;3.9615main-basis;3.9405–4.0981face/plane variants;5.8704constrained-common-core extension | Relevant numerical/definition sensitivity much smaller than the positive~4ppm conclusion. Common-core result is labelled constrained, not an equilibriumminimum. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_full_system_identity — Correct full molecules, core mapping and physical states.

冻结要求：Check full4a/4c stoichiometry and source connectivity in actual structures, including all CF3/OMe groups and sulfur-containing fused rings. Distinguish the central carbon pentalene from thiophene/benzene. Check charge, state and declared geometry assumptions. Correct output on a truncated substitute cannot answer the full-pair question without an explicit validated approximation.

当前复审：64/60原子完整身份

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "FullCF3/OMe-containing constitutional identities and source state preserved."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SIp14 methods;TablesS11/S13",
    "actual_result": {
      "objects": "full4a64atoms/4c60atoms,q0singlet",
      "positive_modes": [
        186,
        174
      ],
      "lowest_modes_cm1": [
        11.2785,
        14.4537
      ]
    },
    "reason": "Fullgraphs/mappingandactualminimaarebound;4eprimeor4fnot substitutedforthepair.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log",
        "sha256": "89019fddab437c30f5d2b9d20d3bd4010f34ed3f1c27db6560b7cdd7178c1edd"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log",
        "sha256": "189fde92e47dbfad0f5c0a54c797cbfaa26b88399e30372e09f210057107d5d4"
      }
    ]
  }
]
```

### kp_magnetic_response_evidence — Inspectable magnetic response with reproducible definition and arithmetic.

冻结要求：Verify actual response output, geometry and analysis for both systems at comparable stated conditions. Recompute relevant contrasts. For a tensor route, inspect full tensor/probe/frame/sign mapping; for current-density routes inspect field convention, density/current evidence and integration or interpretation used. No particular NICS height, ring averaging, ACID software or source scalar is mandatory. A source number or diagram alone is not newly generated scientific evidence.

当前复审：实张量与法向投影

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Actual paired response tensors,probes and negative-shielding convention retained."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainp5Fig5a;SIp14",
    "actual_result": {
      "definition": "NICS=-n^T sigma n;+1.7Aaboveeach5carbonringcentroid;arithmetic2ringmean",
      "ring_atoms_1based": [
        [
          1,
          2,
          3,
          4,
          13
        ],
        [
          4,
          7,
          6,
          5,
          13
        ]
      ],
      "core_atoms_1based": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        13
      ],
      "current_means_ppm": {
        "4a": 23.195149999999998,
        "4c": 19.20415
      },
      "same_SI_pair_difference_ppm": 3.9909999999999997
    },
    "reason": "Sameobjectsandobservablesmatchinheritedunchanged+/-2ppmcriterion;actualcomparativeresponseremainsnewlycomputedhistoricalscientificevidence.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/gaussian.log",
        "sha256": "5c09e70a0e3e21c93891d4f1358a75dc21acaa466e4bb425f95a8a3307429111"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/gaussian.log",
        "sha256": "016fec31bfab6580ffe466d361e9a9db3b6219561935a8e940acf9edb2109693"
      }
    ]
  }
]
```

### kp_attribution — Evidence supporting the scope of the substituent/antiaromatic interpretation.

冻结要求：Assess whether selected comparisons can distinguish the submitted explanation from material geometry, nonlocal-response or measurement-definition effects for the claims actually made. Direct causation needs more than two unequal scalars; a clearly limited association can be valid but must not claim unique cause. No fixed-core swap, BLA or exact diagnostic matrix is mandatory. Reward actual contrary or indistinguishable results when they are supported, without requiring4a>4c.

当前复审：有限取代/几何解释

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Existing geometry/electronic comparison preserves ordering but does not isolate one cause; no bare scalar is used as universalaromaticityproof."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainp5Fig5b/c;currentrule_attribution",
    "actual_result": {
      "control_differences_ppm": [
        {
          "case": "SI_basis_relaxed",
          "difference_ppm": 4.0073701140464095
        },
        {
          "case": "main_basis_relaxed",
          "difference_ppm": 3.9615182235069923
        },
        {
          "case": "already_computed_constrained_common_core",
          "difference_ppm": 5.870397706672577,
          "not_a_free_minimum": true,
          "not_required_new_matrix": true
        }
      ],
      "48current_queries": "8bonds,twofaces,twofielddefinitions;16/32neighborsasdeclared;allparatropicdirectionretained",
      "association": "sourceelectron-withdrawing4astrongerthandonating4c"
    },
    "reason": "Alreadyperformedcommoncoretestpreservesorderingbutperiphery/relaxationareconfounded;claimassociationandboundedmagneticcharacter,notuniquecause. Mixednominal18subspaceisdisclosed;privateauthorMOlistnotmandatory.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_grid/gaussian.log",
        "sha256": "ecf47b821c5b9b79f75854d788d60ae0dc1dcd3de67aa17bc93ae6448babf5a5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_grid/gaussian.log",
        "sha256": "cf87ad3a7eefc3204f6168e900737ca19eca1575a99deee3e772f875f30bc4a5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_basis_sensitivity/gaussian.log",
        "sha256": "d57e87f0efc887df5888477f682b34b7ed1a73c7cd07edddbd24ae9600cdda0f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_basis_sensitivity/gaussian.log",
        "sha256": "8a1571de0f4ffbf457f5d16d65c9d3aa05704e2d3677c662be325dbad33fadf2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_rotated_grid/gaussian.log",
        "sha256": "9cbf646cf2bc70da4793770232e6a03a5d2d90ccea36673d206ecc78e4b718e8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_commoncore_grid/gaussian.log",
        "sha256": "4f2bbebf6ce964c411d793631bc4e11002cfdc88480e6d2dea0f206f4cb069c7"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_commoncore_grid/gaussian.log",
        "sha256": "7e58df562dcbc54b7700c831c6dcad5bef8c87b432481b7c18a3cef3d90cfa5c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_full_export_field_repair_acceptance_20261007.json",
        "sha256": "e1ccba010f4b56d1e1f5b8ef4a063a22f96cbec2053c97e3ba0c06571a98309b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/execution.json",
        "sha256": "d720975f9fc2e4be65dda33db2cf57413b7c63d0c5fd5e8e1d29625617ddc362"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log",
        "sha256": "ab6d3464f8fed7c326125b6daa00c56069f67df42c7be5b5916ddb4f40f12167"
      }
    ]
  }
]
```

### kp_response_reliability — Scientific/numerical reliability appropriate to the chosen magnetic method.

冻结要求：Validate stationary points when asserted, constraints when used, response conventions and dominant numerical/structural uncertainty. Projection must be invariant to mere coordinate labeling; an unaligned global zz is not a molecular normal response. A current or tensor method needs relevant convergence/uncertainty, but not the reference grid. Source basis discrepancy is not a tolerance to force agreement. Uncertainty must support the precision and directional conclusion claimed. Source plane-scope wording differs: main physical p5 Figure 5 says benzothiophene-fused pentalene frameworks, whereas SI physical p14 says pentalene frameworks. This does not prove different planes, and the inspected passages do not fully specify author fitting atoms or coordinate transforms. For a plane-based projection or current interpretation, require the submitted plane/fitting definition, explicit mapped atom set and reproducible coordinate/field/view transformation with direction and sign. Judge the validity of that declared convention and its effect on the actual claim; do not penalize failure to guess unpublished author atoms. For PR, distinguish disclosed-condition fidelity, a justified substitution for missing details and an extension. AR remains free to choose a suitable response method; no source-specific plane or additional comparison matrix is mandatory. Supported ambiguity earns applicable credit, but uncertainty alone does not replace response evidence.

当前复审：基组、面向、探针和旋转控制；最终比较为4a更强的正NICS响应。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Plane atoms,field sign,frame transform,face and basis controls explicit and actual."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "SIp14 andcurrentrule_response_reliability",
    "actual_result": {
      "matched_plane_face_contrasts": [
        {
          "definition": "pyAroma4.1_calCoor_local_ring",
          "face": -1,
          "4a_ringmean_ppm": 23.208118820357125,
          "4c_ringmean_ppm": 19.15769107089481,
          "4a_minus_4c_ppm": 4.050427749462315
        },
        {
          "definition": "pyAroma4.1_calCoor_local_ring",
          "face": 1,
          "4a_ringmean_ppm": 23.19798152079955,
          "4c_ringmean_ppm": 19.204923839691006,
          "4a_minus_4c_ppm": 3.993057681108546
        },
        {
          "definition": "SI_pentalene_xy_fixed_z",
          "face": -1,
          "4a_ringmean_ppm": 23.21035,
          "4c_ringmean_ppm": 19.157850000000003,
          "4a_minus_4c_ppm": 4.052499999999995
        },
        {
          "definition": "SI_pentalene_xy_fixed_z",
          "face": 1,
          "4a_ringmean_ppm": 23.195149999999998,
          "4c_ringmean_ppm": 19.20415,
          "4a_minus_4c_ppm": 3.9909999999999997
        },
        {
          "definition": "main_fused_xy_fixed_z",
          "face": -1,
          "4a_ringmean_ppm": 23.244750024002286,
          "4c_ringmean_ppm": 19.146641401119922,
          "4a_minus_4c_ppm": 4.098108622882364
        },
        {
          "definition": "main_fused_xy_fixed_z",
          "face": 1,
          "4a_ringmean_ppm": 23.18107056723744,
          "4c_ringmean_ppm": 19.240535744990197,
          "4a_minus_4c_ppm": 3.940534822247244
        }
      ],
      "nuclear_integral_max_error_ppm": 0.04008121151197663,
      "nuclear_gate_ppm": 0.05,
      "global_moment_max_error_cgsppm": 4.259669254835785e-05,
      "global_gate": 0.01,
      "source4a_tighter_grid_ring_values_ppm": [
        23.0505,
        23.4422
      ],
      "export_fields": "6505batches/1232325points;onlysmallzeroedfieldsrestored"
    },
    "reason": "Plane/frame/field identities explicit;basisandprojectionrotationeffectschecked. Responsecomparisonwellabovemeasurednumericalchanges. KernelintegrationerrorisnotmisusedasGIAOmethodaccuracy.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_full_export_field_repair_acceptance_20261007.json",
        "sha256": "e1ccba010f4b56d1e1f5b8ef4a063a22f96cbec2053c97e3ba0c06571a98309b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/execution.json",
        "sha256": "d720975f9fc2e4be65dda33db2cf57413b7c63d0c5fd5e8e1d29625617ddc362"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log",
        "sha256": "ab6d3464f8fed7c326125b6daa00c56069f67df42c7be5b5916ddb4f40f12167"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/gaussian.log",
        "sha256": "df10d35d1f7c100f48a606121595bbef49c85625eb4c330b4394560745789e69"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/reopen_pyaroma_public_replay_20261004.json",
        "sha256": "c94976b050b990e28d3e07d97eb4db8ade91585f4fafa44957c7747ee833a9fb"
      }
    ]
  }
]
```

### conclusion_investigation — Determine whether the two supplied benzothiophene-fused pentalenes differ in molecular magnetic response associated with their central pentalene unit. Develop and test an interpretation of any difference, or establish a defensible limit on what can be distinguished, and assess what your evidence supports about antiaromatic character within this pair. Neither a response ordering nor a substituent mechanism is given.

冻结要求：Answer whether a response difference is established within this pair, its supported interpretation, and the limits of antiaromatic attribution. Accept supported alternative measures, reverse/no-resolvable contrasts and evidence-based restricted conclusions. Do not require a numerical source target or topological-charge explanation. A missing response calculation is not evidence of non-identifiability; a positive scalar alone does not prove a universal aromaticity, stability or reactivity statement.

当前复审：kp_full_system_identity：64/60原子完整身份；kp_magnetic_response_evidence：实张量与法向投影；kp_attribution：有限取代/几何解释；kp_response_reliability：基组、面向、探针和旋转控制；最终比较为4a更强的正NICS响应。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Positive paratropic central response for both,4a stronger,with limited substituent association reproduces the required source comparison."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainp5Fig5;currentconclusion_investigation",
    "actual_result": {
      "answer": "4a stronger positive centralnormalresponse than4c;finiteparatropiccharacterforboth,qualifiedsubstituentassociation",
      "scope": "isolatedmolecularpair/authorHamiltonian"
    },
    "reason": "Everycurrentnodehasactualevidence;exactprivateplot/MOprocedureanduniquechemicalcausearenotclaimed.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/gaussian.log",
        "sha256": "5c09e70a0e3e21c93891d4f1358a75dc21acaa466e4bb425f95a8a3307429111"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/gaussian.log",
        "sha256": "016fec31bfab6580ffe466d361e9a9db3b6219561935a8e940acf9edb2109693"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_full_export_field_repair_acceptance_20261007.json",
        "sha256": "e1ccba010f4b56d1e1f5b8ef4a063a22f96cbec2053c97e3ba0c06571a98309b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/execution.json",
        "sha256": "d720975f9fc2e4be65dda33db2cf57413b7c63d0c5fd5e8e1d29625617ddc362"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log",
        "sha256": "ab6d3464f8fed7c326125b6daa00c56069f67df42c7be5b5916ddb4f40f12167"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 14.48 小时；14 份计时日志/16 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 20 线程/进程；Gaussian %Mem=12GB,24GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0008 · outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/gaussian.log) | Gaussian:2367.7 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/gaussian.log) | Gaussian:1426.9 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0019 · local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log) | Gaussian:1122.7；Gaussian:14901.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0020 · local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log) | Gaussian:1520.2；Gaussian:9299.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0021 · outputs/4a_relaxed_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_grid/gaussian.log) | Gaussian:2895.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0022 · outputs/4c_relaxed_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_grid/gaussian.log) | Gaussian:1436.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0023 · outputs/4a_relaxed_basis_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_basis_sensitivity/gaussian.log) | Gaussian:2074.3 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0024 · outputs/4c_relaxed_basis_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_basis_sensitivity/gaussian.log) | Gaussian:1225.3 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0025 · outputs/4c_rotated_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_rotated_grid/gaussian.log) | Gaussian:1720.9 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0026 · outputs/4a_commoncore_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_commoncore_grid/gaussian.log) | Gaussian:2990.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0027 · outputs/4c_commoncore_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_commoncore_grid/gaussian.log) | Gaussian:1881.7 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0030 · outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log) | Gaussian:393.8 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0031 · outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/gaussian.log) | Gaussian:2444.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0044 · local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/stdout.log) | Gaussian:4431 | 正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

不能将有限 NICS 比较称为独立复现作者纯π ACID路径；相关 MO 子空间选择尚不是唯一π分解。此内容不是当前四个必要节点的硬门槛。

```json
[
  "Nominal18MO current subspace is mixed and not certified as author pure-pi selection. ACID is complementary; exact privateMO indices/picture are not needed to validate the independently sufficient NICSroute."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Full nominal18MO subspace is mixed; authentic author pure-pi orbital selection not certified.",
  "Source main/SI shielding-basis wording differs and both declared comparisons are retained.",
  "No universal aromaticity scale, experimental packing or unique causal attribution is claimed."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_628af8d0bf0a1bfe.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_628af8d0bf0a1bfe/verified_computation_reference.md)；SHA-256 `395f621e64699b48bcc7dd3a7048b55bffdc67888825b1a5635a0ce0bd042e1e`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_628af8d0bf0a1bfe.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_628af8d0bf0a1bfe.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_628af8d0bf0a1bfe.json) | `15c242cda049a7e74d93c66d378884b6758819e2d792fd1574255b1454133a30` | evidence_or_analysis |
| E0002 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/agent_input/task.md](../../../v2_paper_reproduction/paper_628af8d0bf0a1bfe/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_task.md) | `a62fad6e7cdd5133c7dbcbeebaf267d4b3e30602a7975e3b6733197fc36b04a2` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_reference_key_points.json) | `c88dbf642e475f5d4da43eb67c2866c4fd03f3ebb3f41645a213a7bd91dc0b6d` | historical_task_binding |
| E0004 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_reference_conclusions.json) | `0032ce3dfa10dafaa4cb2ffff4febcb2320e2432dbe6e61b0657b66ff34be379` | historical_task_binding |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_audit_2_native_readback.json) | `ef1f45e93e2e7a9a0b0956e810ff714a67de5072fbba619fa5fb56e2340249c1` | evidence_or_analysis |
| E0006 | [papers/paper_628af8d0bf0a1bfe/documents/main.pdf](../../../../papers/paper_628af8d0bf0a1bfe/documents/main.pdf) | `327d99aeb6698b39bc1833dec1bb95f244445ee173fb51d060aa17ef6dcf52a1` | source_document |
| E0007 | [papers/paper_628af8d0bf0a1bfe/documents/supplementary_001.pdf](../../../../papers/paper_628af8d0bf0a1bfe/documents/supplementary_001.pdf) | `7d4e1b91fc4c4501b692d2b1804669e276daaf77502ac8755e5735dac565aec1` | source_document |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `5c09e70a0e3e21c93891d4f1358a75dc21acaa466e4bb425f95a8a3307429111` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `016fec31bfab6580ffe466d361e9a9db3b6219561935a8e940acf9edb2109693` | native_output |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/reopen_pyaroma_public_replay_20261004.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/reopen_pyaroma_public_replay_20261004.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_reopen_pyaroma_public_replay_20261004.json) | `c94976b050b990e28d3e07d97eb4db8ade91585f4fafa44957c7747ee833a9fb` | evidence_or_analysis |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4a_relaxed_grid/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4a_relaxed_grid/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_definition.json) | `4d4882acc262263c427c78ee661072818b85ecdb3da321094334579f17b6507c` | evidence_or_analysis |
| E0012 | [tasks/final_verified_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_scoring_rules.json) | `2d969ccca594c5ce09ddf43c10afd8c4ce1ee276041c4e2727c0b2bf0bb2ac96` | historical_task_binding |
| E0013 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_628af8d0bf0a1bfe/NATIVE_EVIDENCE_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_628af8d0bf0a1bfe/NATIVE_EVIDENCE_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_NATIVE_EVIDENCE_INDEX.json) | `6fe7658b68457528c9af85f9947b6147c98bac7dd1185671c87fe7dd3f661186` | evidence_or_analysis |
| E0014 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_628af8d0bf0a1bfe/SOURCE_PAGES_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_628af8d0bf0a1bfe/SOURCE_PAGES_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_SOURCE_PAGES_READBACK.json) | `5ebee7cdedd58fb53a4f6f379476e44eaddd353f55baeede0df32196d42995c1` | evidence_or_analysis |
| E0015 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_628af8d0bf0a1bfe/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_628af8d0bf0a1bfe/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_COMPUTATION_INVENTORY.json) | `a750898d3d460ce4abb348a39cd300830eee3de4e756d1447f3ac62a2e0bc8b1` | evidence_or_analysis |
| E0016 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_628af8d0bf0a1bfe.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_628af8d0bf0a1bfe.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_paper_628af8d0bf0a1bfe.md) | `224abf0eeb390a1738e72eaa0bd86b35cb8f98bc89cde7ca95a70b0a1e5f4a2d` | evidence_or_analysis |
| E0017 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/legacy_v1_archive/verified_computation_reference.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/paper_reproduction/evaluation/legacy_v1_archive/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_verified_computation_reference.md) | `4cc76ef56e9681d6ddace878b71b4ead1b544b57fe59e8a584c8ea40c06a491f` | historical_task_binding |
| E0018 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/legacy_v1_archive/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/paper_reproduction/evaluation/legacy_v1_archive/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `cc9e87acfcda59a6280956f9157bbf7c15a3131bddb062475daef2786fb5adbe` | historical_task_binding |
| E0019 | [docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_native_excerpt.json) | `89019fddab437c30f5d2b9d20d3bd4010f34ed3f1c27db6560b7cdd7178c1edd` | native_output |
| E0020 | [docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0020_native_excerpt.json) | `189fde92e47dbfad0f5c0a54c797cbfaa26b88399e30372e09f210057107d5d4` | native_output |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_grid/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_native_excerpt.json) | `ecf47b821c5b9b79f75854d788d60ae0dc1dcd3de67aa17bc93ae6448babf5a5` | native_output |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_grid/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0022_native_excerpt.json) | `cf87ad3a7eefc3204f6168e900737ca19eca1575a99deee3e772f875f30bc4a5` | native_output |
| E0023 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_basis_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_basis_sensitivity/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0023_native_excerpt.json) | `d57e87f0efc887df5888477f682b34b7ed1a73c7cd07edddbd24ae9600cdda0f` | native_output |
| E0024 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_basis_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_basis_sensitivity/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_native_excerpt.json) | `8a1571de0f4ffbf457f5d16d65c9d3aa05704e2d3677c662be325dbad33fadf2` | native_output |
| E0025 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_rotated_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_rotated_grid/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_native_excerpt.json) | `9cbf646cf2bc70da4793770232e6a03a5d2d90ccea36673d206ecc78e4b718e8` | native_output |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_commoncore_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_commoncore_grid/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_native_excerpt.json) | `4f2bbebf6ce964c411d793631bc4e11002cfdc88480e6d2dea0f206f4cb069c7` | native_output |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_commoncore_grid/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_commoncore_grid/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_native_excerpt.json) | `7e58df562dcbc54b7700c831c6dcad5bef8c87b432481b7c18a3cef3d90cfa5c` | native_output |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_full_export_field_repair_acceptance_20261007.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_full_export_field_repair_acceptance_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_author_4a_full_export_field_repair_acceptance_20261007.json) | `e1ccba010f4b56d1e1f5b8ef4a063a22f96cbec2053c97e3ba0c06571a98309b` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_execution.json) | `d720975f9fc2e4be65dda33db2cf57413b7c63d0c5fd5e8e1d29625617ddc362` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_native_excerpt.json) | `ab6d3464f8fed7c326125b6daa00c56069f67df42c7be5b5916ddb4f40f12167` | native_output |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_native_excerpt.json) | `df10d35d1f7c100f48a606121595bbef49c85625eb4c330b4394560745789e69` | native_output |
| E0032 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_task.md) | `a77bbcea36a7b0f058eb83bdf0582108f2f217a2e372d01b2381eff352e01ee7` | historical_task_binding |
| E0033 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_reference_key_points.json) | `c88dbf642e475f5d4da43eb67c2866c4fd03f3ebb3f41645a213a7bd91dc0b6d` | historical_task_binding |
| E0034 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_reference_conclusions.json) | `0032ce3dfa10dafaa4cb2ffff4febcb2320e2432dbe6e61b0657b66ff34be379` | historical_task_binding |
| E0035 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_scoring_rules.json) | `309b3764fa2b57bb153982f87719a4b3bd7532a11faa39bc8728e1e2d967b30d` | historical_task_binding |
| E0036 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_task.md) | `a62fad6e7cdd5133c7dbcbeebaf267d4b3e30602a7975e3b6733197fc36b04a2` | historical_task_binding |
| E0037 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_reference_key_points.json) | `c88dbf642e475f5d4da43eb67c2866c4fd03f3ebb3f41645a213a7bd91dc0b6d` | historical_task_binding |
| E0038 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_reference_conclusions.json) | `0032ce3dfa10dafaa4cb2ffff4febcb2320e2432dbe6e61b0657b66ff34be379` | historical_task_binding |
| E0039 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_scoring_rules.json) | `309b3764fa2b57bb153982f87719a4b3bd7532a11faa39bc8728e1e2d967b30d` | historical_task_binding |
| E0040 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G1.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G1.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_G1.json) | `ccad79bf939c39a02d6d81ef6b33306a032329039eb7887cda053cf14d145f6b` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_628af8d0bf0a1bfe_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_628af8d0bf0a1bfe_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_paper_628af8d0bf0a1bfe_delivery_integrity.json) | `a3836d104197bf3cefaf8f32f89038d2627bb1b09cf226bebee0cfacf21957e4` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/LEGACY_NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/LEGACY_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_LEGACY_NATIVE_READBACK.json) | `889c1e7fec348a2c08b8e188367172731bc870d94d1e5b38b9a47550dce5c30d` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/SOURCE_PAGE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/SOURCE_PAGE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_SOURCE_PAGE_READBACK.json) | `bd4590ede5bef400cd4a197a607c5d6ff21bd6fa704e3fc99d61188aea8f51d3` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_native_excerpt.json) | `d6e27ac0a4ab36cbc94dba8b404e2d58dcdb79ac2568abd96da68501dab3aff4` | native_output |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_input.com) | `0fb929d42cf1f51a28657340d2abd5f51795c2633df95282ba7a14a686adf9d0` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_input.com) | `e4d4119ddd396a020acd04130142442ef458620398f733fae7ff2f1949821e12` | input_or_analysis_code |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/nics_native_source_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/nics_native_source_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_nics_native_source_audit.json) | `c4c66d7af51e122324a5321e3b0b3155e7ef25096533f8b5dc1367ea82fc0fcd` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_pyaroma_source_NICS_acceptance_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_pyaroma_source_NICS_acceptance_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_author_4a_pyaroma_source_NICS_acceptance_20261002.json) | `9b73b9ea898807d8b66947ba0cdbcb44de298cbd9467ca8a730630c9c11bcdae` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4c_pyaroma_source_NICS_acceptance_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4c_pyaroma_source_NICS_acceptance_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0049_author_4c_pyaroma_source_NICS_acceptance_20261002.json) | `91654bf2742d7a7155b26fd7d78744b63d0c38aba6edfc3c64aa6d6099c96a4f` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/NICS_FINAL_EXPORT_PHYSICAL_ACCEPTANCE_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/NICS_FINAL_EXPORT_PHYSICAL_ACCEPTANCE_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_NICS_FINAL_EXPORT_PHYSICAL_ACCEPTANCE_20261007.json) | `37b1d163c331a3cbcb4344b9c5a846967bf2fd8ce2648763d7da3c1886abf5f2` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/nics_author_route_scope_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/nics_author_route_scope_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_nics_author_route_scope_20260930.json) | `0311608e24c47de1484f7c2d08c9a1b9c9d69bcc7085fed10ddf48458576374b` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_NICS_grid_convergence_acceptance_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/v2_execution_20260929/author_4a_NICS_grid_convergence_acceptance_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_author_4a_NICS_grid_convergence_acceptance_20261002.json) | `f1443e47d2e35a1b88ce56cd9613dcc10b37631b63e5e85e57f039157658e04f` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_input.com) | `b13ef084f08db8bc4f5f9782419f968079627b38a2b6e87693fd1ad71652b9bf` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_input.com) | `57e272b50b89b0f28f47a80545ec15d90ce2c0753309a80af27d3873faa63c2e` | input_or_analysis_code |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_grid/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_grid/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_input.com) | `e717a3d9dbb10dd4bfdef6e6d3038a0f1bbdd6a08db341226d6490cc9b6119d1` | input_or_analysis_code |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_grid/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_grid/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_input.com) | `aa5f41d91f4173add2edb482b4db381590d97fa25249e1f8e1f84847ba9b8a1e` | input_or_analysis_code |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_basis_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_relaxed_basis_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_input.com) | `d8372ae736fe60f556e0490d41d72fd0e63fce435e88bf035c800fc928b04d1b` | input_or_analysis_code |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_basis_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_relaxed_basis_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_input.com) | `7d18cdb933395e644d2bfb4c3b211d2d040b369aea877352e1e4b16951e64942` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_rotated_grid/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_rotated_grid/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_input.com) | `7eae2ba5cb89a7745ce860904c2fcefcec21b52cb24c75fb53d94162fc2c50eb` | input_or_analysis_code |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_commoncore_grid/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4a_commoncore_grid/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_input.com) | `9815813548a34a72e0be085ec4b3413560f83a43120493566726d0f6e91fdcfe` | input_or_analysis_code |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_commoncore_grid/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/4c_commoncore_grid/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_input.com) | `9d85b1e81866c868b282a98de3a59583b567b434e63262addcc0b29c6b4ab655` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_CSGT_full_export_repair_20261007_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_input.com) | `942e5a41e6eb69884528349d32c3749be432c86bd0867edaead7882eb4987052` | input_or_analysis_code |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0063_input.com) | `2b5a431f7bc419fb3a32a62729c49784bdaf25b06502bfb06af86c75aaec79c3` | input_or_analysis_code |
| E0064 | [tasks/final_verified_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0064_verified_computation_reference.md) | `cc9e87acfcda59a6280956f9157bbf7c15a3131bddb062475daef2786fb5adbe` | historical_task_binding |
| E0065 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0065_critical_failures.json) | `3b2f0f200e37e9a4f549a914cc6ae671a7314d427484fa7d7f0ae7ef600d29b1` | historical_task_binding |
| E0066 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_628af8d0bf0a1bfe/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_package_manifest.json) | `be9b142be392b148afbbcd6a2125891d6d4d6101393200d9c96b65dc6e5093a6` | historical_task_binding |
| E0067 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0067_critical_failures.json) | `3b2f0f200e37e9a4f549a914cc6ae671a7314d427484fa7d7f0ae7ef600d29b1` | historical_task_binding |
| E0068 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_628af8d0bf0a1bfe/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0068_package_manifest.json) | `d08bf272775c7b45ea61d18cd5b6732e99106bc26c63928fae50bd221a394d13` | historical_task_binding |
| E0069 | [docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_input.com) | `0627508a55d02c78a665c87e1cbde012d74e5b87fcbe63d4d59793c08e48f26a` | input_or_analysis_code |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_relaxed_grid/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_relaxed_grid/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_definition.json) | `f0676d4cd0a52565b41ae46d19889d3519ad2ed1ad32fb4b0f002d10e63b03e6` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4a_relaxed_basis_sensitivity/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4a_relaxed_basis_sensitivity/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0071_definition.json) | `27d4a704fdb699ffa8eccdaaf6a8d28d6ea9949e6fc83a854cf66c15c8b1f1c5` | evidence_or_analysis |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_relaxed_basis_sensitivity/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_relaxed_basis_sensitivity/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_definition.json) | `7577c0ae82e32a00f2d15a871ebb5f614e48e8379db71bf0f150bddeec5a41b8` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_rotated_grid/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_rotated_grid/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_definition.json) | `a73b404193021999a3815191edd463cf4f5e4c802184318c844c7e609615350f` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4a_commoncore_grid/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4a_commoncore_grid/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_definition.json) | `08cf28afa6d7e45db29a838fe42b945eef63764d634a2c6f256af1dee9a6bafa` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_commoncore_grid/definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/4c_commoncore_grid/definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0075_definition.json) | `1969283a8653eed4b967b9263b724219ef8dcb086568b71370cdca924c701509` | evidence_or_analysis |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0076_execution.json) | `40dba6c69e47f83584666e2a8898e7ebbc98b1ffdceee00e984d9643464c56d2` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_input.com) | `0fb929d42cf1f51a28657340d2abd5f51795c2633df95282ba7a14a686adf9d0` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_pyaroma_source_NICS_20261002_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_identity.json) | `7d90c59f0cfccf2086a9ac250e6cf5d89942c12ce8ed303075caeabee1f81a58` | evidence_or_analysis |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_execution.json) | `1405bcce5603e38cfd37d44f3008c125808ce8de852d26f97ea4164d21eb0927` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_input.com) | `e4d4119ddd396a020acd04130142442ef458620398f733fae7ff2f1949821e12` | input_or_analysis_code |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4c_pyaroma_source_NICS_20261002_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_identity.json) | `0e375c79b7764976ad22d3779339aa3d45fba7f269f2ebc264675413b986d25d` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/analysis_result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_export_field_repair_20261007_a01/analysis_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_analysis_result.json) | `18cd3704984b63607851c2f83ecef2be34a5ed5f6d623045c2afb8fdf6e8142d` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/accept_4a_full_export_fields_20261007.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/accept_4a_full_export_fields_20261007.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_accept_4a_full_export_fields_20261007.py) | `1c9089b463b1dc50c12f1619c765e91274a138ed139912250ec3776655c37935` | input_or_analysis_code |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_export_field_repair_20261007_a01/analysis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_export_field_repair_20261007_a01/analysis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_analysis.json) | `93f4a7616b8930a5e722dae0c60caf2020877f41981c4c7c02469ba7a17162df` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/outputs/v2_author_4a_NICS_grid_convergence_20261002_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_execution.json) | `eaab166a041592b9ecba3cf133775a623bad60d3a925d65942e108d879fa1119` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_NICS_grid_convergence_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_NICS_grid_convergence_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_input.com) | `2b5a431f7bc419fb3a32a62729c49784bdaf25b06502bfb06af86c75aaec79c3` | input_or_analysis_code |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_NICS_grid_convergence_20261002_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/inputs/v2_author_4a_NICS_grid_convergence_20261002_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_628af8d0bf0a1bfe/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_identity.json) | `55bfd5249a567c340d9378f398f63752728dc0411f887026ddf59b0ae91d49b7` | evidence_or_analysis |
| N0088 | [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/agent_input/task.md](../agent_input/task.md) | `a77bbcea36a7b0f058eb83bdf0582108f2f217a2e372d01b2381eff352e01ee7` | latest_review_evidence |
| N0089 | [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json](reference_key_points.json) | `c88dbf642e475f5d4da43eb67c2866c4fd03f3ebb3f41645a213a7bd91dc0b6d` | latest_review_evidence |
| N0090 | [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json](reference_conclusions.json) | `0032ce3dfa10dafaa4cb2ffff4febcb2320e2432dbe6e61b0657b66ff34be379` | latest_review_evidence |
| N0091 | [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json](scoring_rules.json) | `309b3764fa2b57bb153982f87719a4b3bd7532a11faa39bc8728e1e2d967b30d` | latest_review_evidence |
| N0092 | [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `0f1bdedfacb09eb03ad1943e011125af8c5031b81aa11c8fbd5b1e1ae9ee75ef` | latest_review_evidence |
| N0093 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json) | `309b3764fa2b57bb153982f87719a4b3bd7532a11faa39bc8728e1e2d967b30d` | latest_review_evidence |
| N0094 | [tasks/v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_validation_plan.md](../../../v2_paper_reproduction/paper_628af8d0bf0a1bfe/evaluation/reference_validation_plan.md) | `0f1bdedfacb09eb03ad1943e011125af8c5031b81aa11c8fbd5b1e1ae9ee75ef` | latest_review_evidence |
| N0095 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0096 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/agent_input/task.md](../agent_input/task.md) | `a77bbcea36a7b0f058eb83bdf0582108f2f217a2e372d01b2381eff352e01ee7` |
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_key_points.json](reference_key_points.json) | `c88dbf642e475f5d4da43eb67c2866c4fd03f3ebb3f41645a213a7bd91dc0b6d` |
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_conclusions.json](reference_conclusions.json) | `0032ce3dfa10dafaa4cb2ffff4febcb2320e2432dbe6e61b0657b66ff34be379` |
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/scoring_rules.json](scoring_rules.json) | `309b3764fa2b57bb153982f87719a4b3bd7532a11faa39bc8728e1e2d967b30d` |
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/critical_failures.json](critical_failures.json) | `3b2f0f200e37e9a4f549a914cc6ae671a7314d427484fa7d7f0ae7ef600d29b1` |
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/evidence_map.json](evidence_map.json) | `f98b4b0fb5ff400e76eaa2bb716691e4a2152e23faa6737b7d5da727500483fa` |
| [tasks/v2_autonomous_research/paper_628af8d0bf0a1bfe/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `0f1bdedfacb09eb03ad1943e011125af8c5031b81aa11c8fbd5b1e1ae9ee75ef` |


## Current scoring migration — 2026-10-19
Active policy: paper_science_v2; 100 binary scientific-result points across intermediate findings and final conclusions. Active rules supersede historical scoring weights and freezes. No process score or multiplier. This migration performs no new chemical calculation and preserves the existing frozen V2 acceptance with all scientific limitations. Main p5 gives NICS basis 6-31++G(2d,p), SI p14 gives 6-311+G(2d,p). Plane wording differs and exact author fit atoms are undisclosed. A ±2 ppm historical same-observable gate does not by itself establish the difference. Fixed 18-MO current reconstruction is an approximation, not the author unpublished pi selection. No unique substituent causal decomposition is certified.


## Authorized scoring-contract repair — 2026-10-19 (round3)
Retained source-supported sign/contrast and bounded magnetic interpretation; corrected public unconditional opposite/unresolved credit and process-axis wording without revealing the AR response ordering. Public scoring prose now describes100-point binary scientific results; reporting a contrary/unresolved answer does not automatically satisfy another target. This append changes the current evaluation contract only; original verification history remains verbatim, no new chemistry or acceptance upgrade is claimed.

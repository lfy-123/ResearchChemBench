# 2026-10-28 V3 scope and evidence reuse

Four neutral BF2 chelates: retain the original solution-absorption explanation, with four lower-band assignments, aromatic-extension interpretation and the distinct weak-low/strong-high 1c features. Seven nonduplicated final outcomes replace thirteen V2 leaves; no numeric target or scientific object is changed.

- `r_low_state_1a`: Physical assignment of the 1a lower-energy absorption band; evidence: main_assignment, si_structures, native_state_synthesis.
- `r_low_state_1b`: Physical assignment of the 1b lower-energy absorption band; evidence: main_assignment, si_structures, native_state_synthesis.
- `r_low_state_1c`: Physical assignment of the 1c lower-energy absorption band; evidence: main_assignment, si_structures, native_state_synthesis.
- `r_low_state_1d`: Physical assignment of the 1d lower-energy absorption band; evidence: main_assignment, si_structures, native_state_synthesis.
- `r_conjugation_explanation`: Electronic explanation of the shifts across 1a–1d; evidence: main_absorption, main_assignment, native_state_synthesis.
- `r_weak_low_band`: Physical explanation of the weak lower-energy 1c band; evidence: main_assignment, native_state_synthesis.
- `r_upper_band_1c`: Physical assignment of the stronger higher-energy 1c band; evidence: main_absorption, main_assignment, native_state_synthesis.

Known limits: Source solvent implementation is incompletely specified; PCM toluene and CAM are explicit extensions; 1c source S3 maps only approximately to CAM S4 (transition overlap 0.5297355); root equality is not physical identity; No exact experimental line shape, robust 1c/1d fine ordering, emission or solid-state conclusion is established; V3 semantic review and blind AR calibration were not rerun. No new calculation or V3 scientific PASS is asserted. All text below is preserved historical evidence, including obsolete scoring statements; the active V3 JSON files govern scoring.

---

# V2 验证计算参考：BF2四分子吸收

论文：`paper_2f2aa11ea61a32bb`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：四分子强弱差异/带角色的作者计算结论已恢复；不宣称完整实验线形或发光效率。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

1a–1d的分子吸收比较及1c弱低态/较高亮态区分。

冻结题面中的科学目标：

What molecular explanation of the absorption differences among complexes1a–1d in toluene is supported by the supplied observations and an independent investigation? Establish defensible state/band assignments and the limits of any proposed structure–spectrum relationship.

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_2f2aa11ea61a32bb/documents/main.pdf](../../../../papers/paper_2f2aa11ea61a32bb/documents/main.pdf) | `bfdb4129439627d7d651b864d72f7c08c512af56365e473b538a8460c1e6a694` |
| [papers/paper_2f2aa11ea61a32bb/documents/supplementary_001.pdf](../../../../papers/paper_2f2aa11ea61a32bb/documents/supplementary_001.pdf) | `6187b34d441b880b245cbbbd3350b5a9ca926ba472f56bd2026bad2a0e174983` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

作者B3LYP/6-31+G(d,p)；气相源基线重放，加明确标注PCM甲苯的扩展及CAM态对应控制。

1. 由论文图及 SI 核对 1a–1d 的完整 N,O-BF2 化学图和四种连接方式；1c 的弱低态与较高亮态分开建立对照。

2. 按 Gaussian B3LYP/6-31+G(d,p) 计算气相及明确声明的 PCM 甲苯分支，核收八个优化/频率最低点，每个具有 66 或 84 个正模。源未完整披露溶剂实现，源理论重放与额外溶剂控制不混称。

3. 从实际 TD 输出提取 1aS1、1bS1、1cS1/S2/S3、1dS1 六组 λ/f：361.55/0.1015、396.34/0.1425、420.49/0.0080、350.76/0.2334、341.19/0.0719、405.62/0.1348，与 Fig.3 的打印分辨率逐项对照。

4. 用已完成的跃迁密度/态特征及 CAM 对照检查同态对应；1c 的源 S3 对应控制方法 S4，保留实际重叠而不照搬根序号。以弱低态和高能亮态解释峰与根的差别。

5. 最终结论限定于四种分子在所声明环境下的吸收差异及态性质；不把源未声明的溶剂选项称作精确复刻，也不从离散根直接推断全部实验带形或发光效率。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| 六锚点λ,nm | [362,396,420,351,341,406] | [361.55,396.34,420.49,350.76,341.19,405.62] | 实算−论文：[-0.45,0.34,0.49,-0.24,0.19,-0.38]； 全部处于源整nm打印区间；应选作者TD20日志的1b f=0.1425，不能把另一次TD10 f=0.1424称完全同打印。；源定位：main Fig3 |
| 六锚点f | [0.102,0.143,0.008,0.233,0.072,0.135] | [0.1015,0.1425,0.008,0.2334,0.0719,0.1348] | 实算−论文：[-0.0005,-0.0005,0,0.0004,-0.0001,-0.0002]； 源三小数与原生打印区间相容；1c S1明显弱、S2/S3亮态角色恢复。；源定位：main Fig3 |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| λ / f: 1aS1,1bS1,1cS1,1cS2,1cS3,1dS1 (nm / dimensionless) | [[362,0.102],[396,0.143],[420,0.008],[351,0.233],[341,0.072],[406,0.135]] | [[361.55,0.1015],[396.34,0.1425],[420.49,0.008],[350.76,0.2334],[341.19,0.0719],[405.62,0.1348]] | Source Fig.3 B3LYP vertical transitions matched by molecular identity and state role. Source whole-nm/three-decimal-f intervals and native values overlap within their printed resolutions; this is direct precision consistency rather than an arbitrary chemical tolerance. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Verify the complete N,O-BF2 graphs and distinct pyridyl/isoquinolyl/quinolyl attachment positions; isomeric1b–1d cannot be identified by formula alone. State labels must correspond to physical transitions rather than being transferred blindly by root index.

冻结要求：Verify the complete N,O-BF2 graphs and distinct pyridyl/isoquinolyl/quinolyl attachment positions; isomeric1b–1d cannot be identified by formula alone. State labels must correspond to physical transitions rather than being transferred blindly by root index. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：四个连接异构图独立核对，不能用化学式替代身份。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Distinct complete 1a–1d connectivity and BF2 coordination are retained; isomer identity is not inferred from formula."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_source_object_geometry_20261001.json",
        "sha256": "fc9eb2fac5ec939fcf7ac42180be2c16bae4af2584967df8d7493bb66977034e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      }
    ],
    "limits": "1c CAM S3/S4 correspondence is mixed, not exact equality by root index."
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_source_object_geometry_20261001.json",
        "sha256": "fc9eb2fac5ec939fcf7ac42180be2c16bae4af2584967df8d7493bb66977034e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      }
    ],
    "limits": "1c CAM S3/S4 correspondence is mixed, not exact equality by root index."
  }
]
```

### kp_quantitative_evidence — Verify calculated or analyzed spectral evidence against real outputs, actual molecular connectivity, states, medium and correctly associated experimental band roles. Independently check unit conversion and any spectral processing.

冻结要求：Verify calculated or analyzed spectral evidence against real outputs, actual molecular connectivity, states, medium and correctly associated experimental band roles. Independently check unit conversion and any spectral processing. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：源6个λ/f锚点和各分子10/20态真实输出读回。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Native TD energies, wavelengths and oscillator strengths reproduce all six Fig.3 reference transitions at the reported precision level."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json",
        "sha256": "00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      }
    ],
    "limits": "Common energy-axis widths0.05/0.10/0.15eV are model choices; printing intervals are not scientific error bars."
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json",
        "sha256": "00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      }
    ],
    "limits": "Common energy-axis widths0.05/0.10/0.15eV are model choices; printing intervals are not scientific error bars."
  }
]
```

### kp_scientific_answer — Assess whether the evidence supports the stated explanation across1a–1d and the two distinct1c features. No fixed S1/brightest-root rule, common geometry decomposition, author orbital assignment or specific functional is a required answer.

冻结要求：Assess whether the evidence supports the stated explanation across1a–1d and the two distinct1c features. No fixed S1/brightest-root rule, common geometry decomposition, author orbital assignment or specific functional is a required answer. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：1c弱S1与高亮态区别支持作者解释；态对应控制不盲用根号。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "1c weak S1 versus bright S2/S3 is directly supported by intensity/transition evidence; the four-molecule absorption comparison is investigated."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json",
        "sha256": "00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json",
        "sha256": "be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7"
      }
    ],
    "limits": "Cannot uniquely assign structural causality or choose the true functional by experimental proximity;1c high-energy band need not equal one vertical root."
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json",
        "sha256": "00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json",
        "sha256": "be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7"
      }
    ],
    "limits": "Cannot uniquely assign structural causality or choose the true functional by experimental proximity;1c high-energy band need not equal one vertical root."
  }
]
```

### kp_validity_and_uncertainty — A spectral assignment must compare the same kind of observable and show relevant state character/intensity or other sufficient evidence. Explain model-dependent shifts and uncertainty rather than selecting whichever computed root is closest after the fact. Validate the adequacy of structures, methods and analysis for the claims using a defensible route of your choice.

冻结要求：A spectral assignment must compare the same kind of observable and show relevant state character/intensity or other sufficient evidence. Explain model-dependent shifts and uncertainty rather than selecting whichever computed root is closest after the fact. Validate the adequacy of structures, methods and analysis for the claims using a defensible route of your choice. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：八个气/溶最低点各66或84正模；源未完整声明溶剂实现，额外PCM不冒充源参数。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Eight minima and solvent/functional/state controls support bounded assignments. A 0.0001 eV 1c/1d PCM S1 difference is smaller than 0.0006–0.0007 eV orientation sensitivity and is not ranked."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      }
    ],
    "limits": "Source undisclosed solvent convention remains disclosed; primary absolute solution RMSE0.13074699187697578eV is not a pass tolerance."
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      }
    ],
    "limits": "Source undisclosed solvent convention remains disclosed; primary absolute solution RMSE0.13074699187697578eV is not a pass tolerance."
  }
]
```

### kp_bounded_conclusion — Conclusions cover solution absorption of these four molecules. A frontier gap, vertical transition or inferred geometric effect does not establish emission efficiency, crystal polymorphism, white-light generation or OLED performance. Distinguish observed band maxima from computed vertical energies and from a chosen broadening model.

冻结要求：Conclusions cover solution absorption of these four molecules. A frontier gap, vertical transition or inferred geometric effect does not establish emission efficiency, crystal polymorphism, white-light generation or OLED performance. Distinguish observed band maxima from computed vertical energies and from a chosen broadening model. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability.

当前复审：四分子强弱差异/带角色的作者计算结论已恢复；不宣称完整实验线形或发光效率。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Vertical transitions, broadened bands and measured maxima remain different observables; no emission/OLED/crystal claim."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json",
        "sha256": "be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7"
      }
    ],
    "limits": "No source-external device/emission claim; no robust fine1c/1d ordering."
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json",
        "sha256": "be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7"
      }
    ],
    "limits": "No source-external device/emission claim; no robust fine1c/1d ordering."
  }
]
```

### bounded_answer — A source-bounded evidence-supported answer to: What molecular explanation of the absorption differences among complexes1a–1d in toluene is supported by the supplied observations and an independent investigation? Establish defensible state/band assignments and the limits of any proposed structure–spectrum relationship.

冻结要求：Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. Conclusions cover solution absorption of these four molecules. A frontier gap, vertical transition or inferred geometric effect does not establish emission efficiency, crystal polymorphism, white-light generation or OLED performance. Distinguish observed band maxima from computed vertical energies and from a chosen broadening model.

当前复审：四分子强弱差异/带角色的作者计算结论已恢复；不宣称完整实验线形或发光效率。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Reproduced source anchors and independently tested solution assignments support the required molecular interpretation with explicit fine-ranking limits."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json",
        "sha256": "00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_source_object_geometry_20261001.json",
        "sha256": "fc9eb2fac5ec939fcf7ac42180be2c16bae4af2584967df8d7493bb66977034e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json",
        "sha256": "be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7"
      }
    ],
    "limits": [
      "Readiness is for independent scientific review, not a semantic judge score or an isolated blind AR run.",
      "Source calculated vertical transitions and experimental solution band maxima are different observables. Primary solution energy residuals and method shifts remain explicit; no assertion of exact experimental reproduction.",
      "Source gas method reproduced; IEFPCM toluene and CAM are disclosed extensions, not recovered undocumented author solvent settings.",
      "1c/1d primary S1 difference 0.0001 eV is not resolved against observed numerical rotation response 0.0006–0.0007 eV.",
      "No emission efficiency, white light, polymorph or OLED inference; no unique causal decomposition of conjugation versus geometry.",
      "TD20 and TD10 leading amplitudes agree; small TD20 amplitudes were not all printed, so no new full-vector overlap claim."
    ]
  },
  {
    "evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json",
        "sha256": "ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json",
        "sha256": "00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json",
        "sha256": "1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_source_object_geometry_20261001.json",
        "sha256": "fc9eb2fac5ec939fcf7ac42180be2c16bae4af2584967df8d7493bb66977034e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json",
        "sha256": "034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json",
        "sha256": "673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json",
        "sha256": "be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7"
      }
    ],
    "limits": [
      "Readiness is for independent scientific review, not a semantic judge score or an isolated blind AR run.",
      "Source calculated vertical transitions and experimental solution band maxima are different observables. Primary solution energy residuals and method shifts remain explicit; no assertion of exact experimental reproduction.",
      "Source gas method reproduced; IEFPCM toluene and CAM are disclosed extensions, not recovered undocumented author solvent settings.",
      "1c/1d primary S1 difference 0.0001 eV is not resolved against observed numerical rotation response 0.0006–0.0007 eV.",
      "No emission efficiency, white light, polymorph or OLED inference; no unique causal decomposition of conjugation versus geometry.",
      "TD20 and TD10 leading amplitudes agree; small TD20 amplitudes were not all printed, so no new full-vector overlap claim."
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 40.04 小时；27 份计时日志/36 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,8,20 线程/进程；Gaussian %Mem=12GB,16000MB,24000MB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0005 · outputs/1a_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_gas_TD10_sensitivity/gaussian.log) | Gaussian:102.8 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · outputs/1c_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_gas_TD10_sensitivity/gaussian.log) | Gaussian:163.7 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · outputs/1d_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_gas_TD10_sensitivity/gaussian.log) | Gaussian:209.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stdout.log) | Gaussian:7742.6 | 正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0033 · gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stdout.log) | Gaussian:2571.8；Gaussian:11279.5 | 正常；正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0034 · outputs/1a_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_optfreq/gaussian.log) | Gaussian:255.7；Gaussian:162.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0035 · gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stdout.log) | Gaussian:7059.6；Gaussian:36131.3 | 正常；正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · outputs/1b_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_optfreq/gaussian.log) | Gaussian:500；Gaussian:357.5 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0037 · gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stdout.log) | Gaussian:8089.7；Gaussian:39109.3 | 正常；正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0038 · outputs/1c_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_optfreq/gaussian.log) | Gaussian:491.8；Gaussian:359.8 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0039 · gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stdout.log) | Gaussian:3401.6；Gaussian:17441 | 正常；正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0040 · outputs/1d_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_optfreq/gaussian.log) | Gaussian:457.6；Gaussian:332.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0041 · execution_jobs/job_48526662c922436996fc8ee3141898fb/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/stdout.log) | Gaussian:762.5；Gaussian:564 | 正常；正常 | {"threads":[8],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0042 · outputs/1a_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_TD10/gaussian.log) | Gaussian:120.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0043 · outputs/1a_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_CAM_toluene_TD10/gaussian.log) | Gaussian:160.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0044 · outputs/1b_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_gas_TD10_sensitivity/gaussian.log) | Gaussian:187.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0045 · outputs/1b_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_TD10/gaussian.log) | Gaussian:211.8 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0046 · outputs/1b_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_CAM_toluene_TD10/gaussian.log) | Gaussian:293 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0047 · outputs/1c_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_TD10/gaussian.log) | Gaussian:221.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0048 · outputs/1c_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_CAM_toluene_TD10/gaussian.log) | Gaussian:267.8 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0049 · outputs/1d_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_TD10/gaussian.log) | Gaussian:166.3 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0050 · outputs/1d_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_CAM_toluene_TD10/gaussian.log) | Gaussian:326.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0051 · gaussian_batch/author_1b_b3lyp_631pdp_td/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stdout.log) | Gaussian:7742.6 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0052 · execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stdout.log) | Gaussian:3249.2 | 正常 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0053 · gaussian_batch/author_1b_b3lyp_631pdp_td20/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stdout.log) | Gaussian:3249.2 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0079 · execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/stdout.log) | Gaussian:7059.6；Gaussian:36131.3 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[4],"Gaussian_mem":["16000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0090 · outputs/1b_aligned_baseline_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_aligned_baseline_TD10/gaussian.log) | Gaussian:215.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0091 · execution_jobs/job_533be45a59fe4d7a97300260934cacf2/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/stdout.log) | Gaussian:505.8 | 正常 | {"threads":[8],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0094 · gaussian_batch/1b_b3lyp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stdout.log) | Gaussian:762.5；Gaussian:564 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[8],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0095 · gaussian_batch/1b_b3lyp_td20/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stdout.log) | Gaussian:505.8 | 正常；此日志为同内容副本，已从累计排除 | {"threads":[8],"Gaussian_mem":["24000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0097 · outputs/1b_commonchelate_opt/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_opt/gaussian.log) | Gaussian:463.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0099 · outputs/1b_commonchelate_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_TD10/gaussian.log) | Gaussian:197.9 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0114 · execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stderr.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stderr.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0118 · execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stderr.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

作者气相基线和溶液PCM比较分开，不能以TD根直接等同所有实验峰。

```json
[
  "PCM implementation is declared because the source solvent treatment is incomplete.",
  "No resolved 1c/1d S1 ordering at the 0.0001 eV scale.",
  "CAM root numbers differ; the overlap correspondence is reported rather than treating S3 as invariant."
]
```


原独立审查的 `material_limits`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "No exact experimental band or absolute spectrum reproduction claim: the chosen PCM model retains its reported0.13074699eV lower-band RMSE; this is not a pass tolerance.",
  "Printed intervals check consistency, not a newly fitted scientific error allowance. The source calculation and measured solution bands are distinct quantities.",
  "1c/1d PCM S1 separation0.0001eV is unresolved relative to measured rotation response0.0006–0.0007eV; no robust fine ordering.",
  "B3LYP 1cS3 best matches CAM S4 with mixed overlap0.5297; root number alone is not state identity.",
  "Expanded connectivity and transition-density character support a bounded explanation, not a unique decomposition of structural causality.",
  "AR evidence validation here is author-informed; it does not certify a blind agent execution or a formal evaluator pass."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_2f2aa11ea61a32bb.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_2f2aa11ea61a32bb/verified_computation_reference.md)；SHA-256 `77cb5f5aa810af6eeda8b8518f73792eb07c491c3f5507a12964a3b47e578baf`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_2f2aa11ea61a32bb.json) | `fcb623812dc78f41ce86bde36d46864666f84c1a259b27f350009da2b21d1393` | evidence_or_analysis |
| E0002 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_2f2aa11ea61a32bb/main.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_2f2aa11ea61a32bb/main.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_main.json) | `3283f4bf64fdad635aa3de447b77dc6e152d2bfaf0183b7c9a9d9745161b0173` | evidence_or_analysis |
| E0003 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_2f2aa11ea61a32bb/supplementary_001.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/sources/paper_2f2aa11ea61a32bb/supplementary_001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_supplementary_001.json) | `4bd9ac718fdd63ddc8ac095fc8b115a85835ecc67975f4acbe856476c23eb369` | evidence_or_analysis |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/source_main_p3_review.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/source_main_p3_review.png) | `dd0c19355b29daf26a5585fbf217c0d9b42437e35bcc8985f3ed97f058634b4a` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_gas_TD10_sensitivity/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `7bdb8b922482c899ce9b0cb4d743eb6da48970821c09e99a6570bd0fc3b7207f` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_gas_TD10_sensitivity/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `e0a456d041fd8aecf3db6b74f9aebefb70905b7f8f30d970593279429039ca5b` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_gas_TD10_sensitivity/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `9163a10742303c7b04e097c81b0a72795373e688e330cd7932731929a0cbd4b2` | native_output |
| E0008 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `f5725e0043b684a54f93b88544e3eecdf59599915cc682aefdbea3d96523dc07` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/1c_toluene_TD10__1c_CAM_toluene_TD10_overlap.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/1c_toluene_TD10__1c_CAM_toluene_TD10_overlap.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_1c_toluene_TD10__1c_CAM_toluene_TD10_overlap.json) | `8b369c59da5d399ab704408d413c009c0eb99cf3217abb80042f18b062423f3d` | evidence_or_analysis |
| E0010 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_task.md) | `dd43729c371b972edac10ffd287fbe2c175efac8434180a92f629e86400bdb27` | historical_task_binding |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_reference_key_points.json) | `6f9007fb0608b31c0c75b6402c3fb5bbe9ccab7c5f081b2dd040b40f63066744` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_reference_conclusions.json) | `ecf9ce5dbf2a81b6462a3ce79a10718f6595b39e8a687fb5a50c8a6221eb33c9` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_task.md) | `bc1baa1103e3742f6c85e1a2aae4474fb44fe5a76616e9c08c0476a4ea45ac3e` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_reference_key_points.json) | `6f9007fb0608b31c0c75b6402c3fb5bbe9ccab7c5f081b2dd040b40f63066744` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_reference_conclusions.json) | `ecf9ce5dbf2a81b6462a3ce79a10718f6595b39e8a687fb5a50c8a6221eb33c9` | historical_task_binding |
| E0016 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_2f2aa11ea61a32bb/NATIVE_EVIDENCE_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_2f2aa11ea61a32bb/NATIVE_EVIDENCE_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_NATIVE_EVIDENCE_INDEX.json) | `1304f0e6b2cae7414649b251163c538d33dc34a06997195c90be9f376570ecfe` | evidence_or_analysis |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_2f2aa11ea61a32bb/SOURCE_PAGES_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_2f2aa11ea61a32bb/SOURCE_PAGES_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_SOURCE_PAGES_READBACK.json) | `8e6d22565caaa4ac8c90274fd5bd88d7a3ae08f255a335fb4ccfa8c0a83a19ed` | evidence_or_analysis |
| E0018 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_2f2aa11ea61a32bb/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_2f2aa11ea61a32bb/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0018_COMPUTATION_INVENTORY.json) | `0d8903e78e7e0f9da1462cbdbb1480838738b076798509ab130921f24be75017` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_2f2aa11ea61a32bb.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_2f2aa11ea61a32bb.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_paper_2f2aa11ea61a32bb.md) | `5094c28d58e60880e1efa67a10b44a4eeb8f8c049ee5671edaf5b6891b1d125c` | evidence_or_analysis |
| E0020 | [docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `a27d6e5d6860a8f4acecd25f2323581875611d527110ab06f782fe6dd4b74249` | historical_task_binding |
| E0021 | [docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `08adbb6d9bca955b59fb0bf1c0aec12a880e17cef5e0046d3b794c7d09444ce3` | historical_task_binding |
| E0022 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0022_package_manifest.json) | `754cf9c31e90403f0a191989cfe27c2d494c2e9bd7810eed1cdeb1a3563638d0` | historical_task_binding |
| E0023 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0023_package_manifest.json) | `260a33e9963a42ff1de20fd8c12c633347e49558057d53f890329ec285684ead` | historical_task_binding |
| E0024 | [papers/paper_2f2aa11ea61a32bb/documents/main.pdf](../../../../papers/paper_2f2aa11ea61a32bb/documents/main.pdf) | `bfdb4129439627d7d651b864d72f7c08c512af56365e473b538a8460c1e6a694` | source_document |
| E0025 | [papers/paper_2f2aa11ea61a32bb/documents/supplementary_001.pdf](../../../../papers/paper_2f2aa11ea61a32bb/documents/supplementary_001.pdf) | `6187b34d441b880b245cbbbd3350b5a9ca926ba472f56bd2026bad2a0e174983` | source_document |
| E0026 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_2f2aa11ea61a32bb_native_readback_0821Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_2f2aa11ea61a32bb_native_readback_0821Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_paper_2f2aa11ea61a32bb_native_readback_0821Z.json) | `6b1f452914a29c42bc4e00e40df4b57b906b3937f8bf3473e43a73a7bf910289` | evidence_or_analysis |
| E0027 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_READY_FOR_REVIEW_20261001.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_READY_FOR_REVIEW_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_BF2_READY_FOR_REVIEW_20261001.json) | `81858ac9f8e8c35bd76716147e672196495f7e46edf7b9bb347bbd81a930e1e9` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/reviews/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/reviews/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_paper_2f2aa11ea61a32bb.json) | `8f5c05821a01fae636577776d2fd17e35b8e78a6861693e430ac939910f4044d` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_gas_TD10_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_gas_TD10_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_input.com) | `ef2f556df355d97cd4fa4d9f5a5954d848efb2a35bbd23c8aafdab5196bc979b` | input_or_analysis_code |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_gas_TD10_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_gas_TD10_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_input.com) | `df403461e001e02a75abae4b31d99b82a3dee485d60b7d561f5612ee7b4532ef` | input_or_analysis_code |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_gas_TD10_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_gas_TD10_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_input.com) | `f867b728df5bedd2b329e36d683e85765e424cb5fe05171ed2280c576e53c6b4` | input_or_analysis_code |
| E0032 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_input.com) | `c0eb84acd5bc8d04dbec9ffd8aa03e59d16236ad33ff737084942ca5bd7723d1` | input_or_analysis_code |
| E0033 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_native_excerpt.json) | `94c395a9a61209e74fcdbe02e618bcb56ea204d2ca3897db0cf4fe9641a1647a` | native_output |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_native_excerpt.json) | `e787825fbed45ba7bca052876a946fc9406a69df0ada9f1ce839facec7889776` | native_output |
| E0035 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_native_excerpt.json) | `deca7ac1e7a19bad9425d465681ae0d293557172bb2c3d8a6b853eeaa965470c` | native_output |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `e062582b9c1d0bae404e1c4a57272a12e727cc4a690555cc701eca595692035a` | native_output |
| E0037 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_native_excerpt.json) | `b3156268b074b4eba874c6104c6337e564f10554ff5c0627c7a5bbc9e3013f51` | native_output |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_native_excerpt.json) | `aca3b9410abba8da4c8ae3a0cc1add6b98321900ce1e911ec91c772cebf8c800` | native_output |
| E0039 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_native_excerpt.json) | `3efa564059672b19cd18ad1c85a1c40b4c7db4897dcafad872d6c72fef00faf7` | native_output |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_native_excerpt.json) | `5f35a31aec65ee804bba69ca803a80a958daab8399e7b6c9b3c6aedfc2dd0e35` | native_output |
| E0041 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_native_excerpt.json) | `cb3571ee2c2ba4d6602705919106b5d6a7a4b16cb39d4a6a84355b61387bc7e4` | native_output |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_native_excerpt.json) | `dcafe2f1000574ed307241fd2e3d49fd813358c47fa48f7846b49f20cec6e0d5` | native_output |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_CAM_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_native_excerpt.json) | `0f02d5218b81be20d4572f7e4387768fa359ae4e0a70da636e61a5c9316a8fa8` | native_output |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_gas_TD10_sensitivity/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_gas_TD10_sensitivity/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_native_excerpt.json) | `2184b0c4d2ab98caae7ebb94c305f6e581a3e7297bd219818ab4745a03587dd5` | native_output |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_native_excerpt.json) | `6a42730b0abfedab8854750ce96035a23be673430811123d51000d134101d229` | native_output |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_CAM_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_native_excerpt.json) | `d78c7d729b5d44eb31c59bf49cdd3249a4cdb773ae82b655acbe170418350c50` | native_output |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_native_excerpt.json) | `f0d565236935aa2a0d4d75df37a3224af678a42350f8ee2de24b879a666fe59a` | native_output |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_CAM_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_native_excerpt.json) | `428d50456767dac811e926da3b561cc6903430c36a91d54940c561609dbf3966` | native_output |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0049_native_excerpt.json) | `5fa691c34f22a8bb83263aa566fce4dae4b636ebb46fea4b186bd791b85f2b6e` | native_output |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_CAM_toluene_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_CAM_toluene_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_native_excerpt.json) | `5e4683487f8725f9d193ed1f3b3522d3b73895885459ae0c4f1ca809f997da36` | native_output |
| E0051 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_native_excerpt.json) | `f5725e0043b684a54f93b88544e3eecdf59599915cc682aefdbea3d96523dc07` | native_output |
| E0052 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_native_excerpt.json) | `7a51003e727643bef8fb341f12b8715fe0c611c193ed42abeb095c0b5ecfe905` | native_output |
| E0053 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_native_excerpt.json) | `7a51003e727643bef8fb341f12b8715fe0c611c193ed42abeb095c0b5ecfe905` | native_output |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_six_state_role_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_bf2_six_state_role_audit.json) | `00008e5e522ba4568632da17cf2ee8a419c29ca80cc3d709488558428d2c5cdc` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_author_route_state_synthesis_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_bf2_author_route_state_synthesis_20260930.json) | `ce365d48a19bddbcb336c4d6bbadc1144c87ff7d618d8f47c56ba1e80195f17d` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/validation/bf2_quality.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_bf2_quality.json) | `1e15fbeca2ef53f69eaf1f336ffc700b895f63f12637d2538088d11a675b4528` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/1c_toluene_TD10__1c_gas_TD10_sensitivity_overlap.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/1c_toluene_TD10__1c_gas_TD10_sensitivity_overlap.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_1c_toluene_TD10__1c_gas_TD10_sensitivity_overlap.json) | `dc2cf0210e59bd0442d048b18ff1cc93fe7f5053ad30aa36da28d4604212be39` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/1c_CAM_toluene_TD10/transition_character.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/1c_CAM_toluene_TD10/transition_character.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_transition_character.json) | `234ff724021f9d1aa6778a788c8801cd276ee4ca1400c8a1bbf48914d7e97e03` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/BF2_transition_controls_v2/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_execution.json) | `e16959a8770f71c4a58fc7f48f2dfe629c84cb43207aff59db78efc4b5fbbccb` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/bf2_redshift_subject_correction_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_bf2_redshift_subject_correction_20261001.json) | `be9b92212270a2fcaab02549881858228089711edddcd0b0d28512676f1daee7` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/provenance/source_text/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/provenance/source_text/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_main.txt) | `626b6f85960c90bdc7de803db5114738d9763ae0bca8d1a04d5c867309ba0466` | evidence_or_analysis |
| E0062 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/data/inputs/observations.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/data/inputs/observations.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_observations.json) | `51e79ce57118289fa95cfe447de673e345c7577d7aebe82212426a76ac369582` | historical_task_binding |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/history/20261001T024702Z_bf2_direction_correction/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/history/20261001T024702Z_bf2_direction_correction/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0063_paper_2f2aa11ea61a32bb.json) | `d879cb3e681bd7f3bdedace68efa9eb4d6e0701ce1a973fbb27cca3436da1e95` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_source_object_geometry_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_source_object_geometry_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0064_strict_source_object_geometry_20261001.json) | `fc9eb2fac5ec939fcf7ac42180be2c16bae4af2584967df8d7493bb66977034e` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/SOURCE_OBJECT_AUDIT_SPEC_20261001.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/SOURCE_OBJECT_AUDIT_SPEC_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0065_SOURCE_OBJECT_AUDIT_SPEC_20261001.json) | `3f5d6b0071af911bd5a3746a1eefa8a6f96abe08c6b9e632544b1300ab35452c` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/evidence/1b_legacy_gas_minimum_input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/evidence/1b_legacy_gas_minimum_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_1b_legacy_gas_minimum_input.com) | `cc78772b540d9c34aa74784146c6a7ef3153af88e07b6ae998ed2e1d0c74cfb9` | input_or_analysis_code |
| E0067 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0067_input.com) | `bd813c4b800b319aeefcfed59426bd3fa9d69864e2ca1c3d81c6ed41ac933d85` | input_or_analysis_code |
| E0068 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0068_input.com) | `cc78772b540d9c34aa74784146c6a7ef3153af88e07b6ae998ed2e1d0c74cfb9` | input_or_analysis_code |
| E0069 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/1b_b3lyp_optfreq.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/1b_b3lyp_optfreq.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_1b_b3lyp_optfreq.com) | `bd813c4b800b319aeefcfed59426bd3fa9d69864e2ca1c3d81c6ed41ac933d85` | input_or_analysis_code |
| E0070 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/author_1b_b3lyp_631pdp_optfreq.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/author_1b_b3lyp_631pdp_optfreq.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_author_1b_b3lyp_631pdp_optfreq.com) | `cc78772b540d9c34aa74784146c6a7ef3153af88e07b6ae998ed2e1d0c74cfb9` | input_or_analysis_code |
| E0071 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0071_input.com) | `cc78772b540d9c34aa74784146c6a7ef3153af88e07b6ae998ed2e1d0c74cfb9` | input_or_analysis_code |
| E0072 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_input.com) | `bd813c4b800b319aeefcfed59426bd3fa9d69864e2ca1c3d81c6ed41ac933d85` | input_or_analysis_code |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_gas_TD10_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_gas_TD10_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_input.com) | `75deba37de1693474150747c8bcf0924b8ced4877f8d3af19634a47f8db688b7` | input_or_analysis_code |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_input.com) | `e972a538d51a5a6491810766962430c315a15330196930ecb1865159775fdc81` | input_or_analysis_code |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_gas_TD10_sensitivity/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_gas_TD10_sensitivity/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0075_input.com) | `8ec770aa7b07f3c43d54ce9181d0b213516a038dcca738340f86a04327bb7f0d` | input_or_analysis_code |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_toluene_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_toluene_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0076_input.com) | `de7e66484b236e01cf37bd243ffe72064b39338acc248d72aa097a15fa08e436` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/provenance/qzcli_hpc/author_1b_b3lyp_631pdp_td20_hpc20_20260906T142750Z/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/provenance/qzcli_hpc/author_1b_b3lyp_631pdp_td20_hpc20_20260906T142750Z/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_input.com) | `225d5f27689d9b08215b27942fa11ee9fd29e1c07fa2c6437d840e4ef4ce969e` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_input.com) | `85df7a00135ac1e9fe4f823d0050df0dde251242b39feeae81e04fe5272d56d0` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_native_excerpt.json) | `deca7ac1e7a19bad9425d465681ae0d293557172bb2c3d8a6b853eeaa965470c` | native_output |
| E0080 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/author_1b_b3lyp_631pdp_td20.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/author_1b_b3lyp_631pdp_td20.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_author_1b_b3lyp_631pdp_td20.com) | `85df7a00135ac1e9fe4f823d0050df0dde251242b39feeae81e04fe5272d56d0` | input_or_analysis_code |
| E0081 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/author_1b_b3lyp_631pdp_td.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/author_1b_b3lyp_631pdp_td.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_author_1b_b3lyp_631pdp_td.com) | `c0eb84acd5bc8d04dbec9ffd8aa03e59d16236ad33ff737084942ca5bd7723d1` | input_or_analysis_code |
| E0082 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_input.com) | `c0eb84acd5bc8d04dbec9ffd8aa03e59d16236ad33ff737084942ca5bd7723d1` | input_or_analysis_code |
| E0083 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_input.com) | `85df7a00135ac1e9fe4f823d0050df0dde251242b39feeae81e04fe5272d56d0` | input_or_analysis_code |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_aligned_baseline_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_aligned_baseline_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_input.com) | `32669b7eb30d1a8744a8b21386a7dca3e8e222a6d982e9641f14aed62abc743c` | input_or_analysis_code |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_aligned_baseline_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_aligned_baseline_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_input.com) | `32669b7eb30d1a8744a8b21386a7dca3e8e222a6d982e9641f14aed62abc743c` | input_or_analysis_code |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_input.com) | `de9f28ba8666d69ba79d965002b56d9ad4de5453c4a294c62f3f5939136d56e0` | input_or_analysis_code |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_CAM_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_CAM_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_input.com) | `55074f6f5729b45f7f78152e260d7200debb7d546bc35b7f23737a61707d31ab` | input_or_analysis_code |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_input.com) | `eec1e0c96039797e2b4baf7db893c931d68fe8dcddf6aeb79d1273cece5f2888` | input_or_analysis_code |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_CAM_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_CAM_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_input.com) | `55074f6f5729b45f7f78152e260d7200debb7d546bc35b7f23737a61707d31ab` | input_or_analysis_code |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_aligned_baseline_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_aligned_baseline_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0090_native_excerpt.json) | `0ff38d18eb62da4bd6bf556d4bdea599b280c323ce8a9ecf5a9ac618aeb0f09b` | native_output |
| E0091 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0091_native_excerpt.json) | `a00a5c423c966df058ea51d2afd2f910c6c9a834fbff01f604088c4f316f1a1a` | native_output |
| E0092 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0092_input.com) | `8cde0871c89808fbe3ea42cbdc7500bf47fbd286edad481ba17cc748d2ffb1f3` | input_or_analysis_code |
| E0093 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/1b_b3lyp_td20.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/code/1b_b3lyp_td20.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0093_1b_b3lyp_td20.com) | `8cde0871c89808fbe3ea42cbdc7500bf47fbd286edad481ba17cc748d2ffb1f3` | input_or_analysis_code |
| E0094 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0094_native_excerpt.json) | `cb3571ee2c2ba4d6602705919106b5d6a7a4b16cb39d4a6a84355b61387bc7e4` | native_output |
| E0095 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stdout.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0095_native_excerpt.json) | `a00a5c423c966df058ea51d2afd2f910c6c9a834fbff01f604088c4f316f1a1a` | native_output |
| E0096 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0096_input.com) | `8cde0871c89808fbe3ea42cbdc7500bf47fbd286edad481ba17cc748d2ffb1f3` | input_or_analysis_code |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_opt/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_opt/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0097_native_excerpt.json) | `9fe2190513deca6dd05b702fd18d4c9d0b116495f7f52f8bec0e5b72b06adf97` | native_output |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0098_input.com) | `76fe32a5091d30d68fcab765ab36bdea3660fc25119bc1767b1c1e7dbe2907da` | input_or_analysis_code |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_TD10/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_TD10/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0099_native_excerpt.json) | `80fc6a0b5ce0bd977e1230f56c73abdafea57e7462bd005c43c19d8f142eece1` | native_output |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_commonchelate_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/inputs/1b_commonchelate_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0100_input.com) | `aa5ca8eee2d65e942224a4338e6070f920b8b0b286e721f85687000de6e50592` | input_or_analysis_code |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/v2_execution_20260929/strict_BF2_exact_geometry_TD_reuse_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0101_strict_BF2_exact_geometry_TD_reuse_20261001.json) | `034d9d06b5077e3ada8c92f1d2ac6a2145cfc2576ebcbc30160b77b527df7600` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/artifact_audits/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/artifact_audits/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0102_paper_2f2aa11ea61a32bb.json) | `c7f733ddb14bc3b11f13a2848df0ff0c1c9a6168b6a9fbfc0544f1f8a8246fe8` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/native_scalars/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/native_scalars/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0103_paper_2f2aa11ea61a32bb.json) | `e8d7731cfee5974e9a27eb835df772a9302aead89304c33e1e96db4f5e9434c7` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/validation_independent_review_20261001T0316Z/supplemental_scalars/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/validation_independent_review_20261001T0316Z/supplemental_scalars/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0104_paper_2f2aa11ea61a32bb.json) | `d9b7dd2204675e1dc386c123a6c6916efbb91a6c96d5b2080fb2a603f6ab17e3` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0105_input.com) | `5976586310cb64061ad743614c56b2182f7cce2b091102a4964be892554d4b36` | input_or_analysis_code |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0106_input.com) | `6bbde86c580e426b867ae38e3722e7b38509b78cefd47a77fc955d1d0ad7b8cd` | input_or_analysis_code |
| E0107 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0107_input.com) | `9991cade4734493e4bd00135afaaa2e21206720bc20b68abfcd3b5a1980bedf0` | input_or_analysis_code |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0108_input.com) | `d2410ab6bdd5cf8442a888ac566d3913e3f5226e9c86458402420f19298ea54d` | input_or_analysis_code |
| E0109 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0109_input.com) | `726fe987323a0c15ee7263ffd53eed875576c15a57ae91df353254a67423b365` | input_or_analysis_code |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0110_input.com) | `9ee632176ca9492751dc095d9c7420e1bfd2156dcd1348ba3c0b8279d3623ac3` | input_or_analysis_code |
| E0111 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/status.json](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0111_status.json) | `0e965bafa39305cc660b487bbccdc22f0febdd8d78ef34eba8a5512f377cb61e` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/collection.json](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/collection.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0112_collection.json) | `1861a76146e210770858cc1d35054930110508bfa1a3e4c427404bb0b3b8f557` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/fort.7](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/fort.7) | `a6914b68f394d6efa8df5ad3fc3fa8b42221f1c585e07eb932a61789b5ebbdfe` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stderr.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0114_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0115 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/status.json](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0115_status.json) | `a0c6cbea370825ec50b768f37d5baeeee099401e1d99a6fe63e7821024c06db1` | evidence_or_analysis |
| E0116 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/collection.json](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/collection.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0116_collection.json) | `a15e5dc90fcbfc1d1cf59a751c560f1b43a76da095b78344b99d17b712b15dcd` | evidence_or_analysis |
| E0117 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/fort.7](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/fort.7) | `885639739f32e6cca1f39968a65e8077538a04ba4ac04f9b7b7810b5fb215ea3` | evidence_or_analysis |
| E0118 | [docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stderr.log](../../../../docs/v2_verification/history/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0118_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0119 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/data/inputs/objects.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/data/inputs/objects.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0119_objects.json) | `514621e36bd81d70a41d0404c1a81bdbf5c11775ae2a111e8c105e1324a6913b` | historical_task_binding |
| E0120 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/data/inputs/observations.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/data/inputs/observations.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0120_observations.json) | `51e79ce57118289fa95cfe447de673e345c7577d7aebe82212426a76ac369582` | historical_task_binding |
| E0121 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/resources.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/resources.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0121_resources.md) | `97aa937cbbbb8509a22fd18b59a05a30aed4509ecc6d2cd7c8cd55e7da27e4e7` | historical_task_binding |
| E0122 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0122_submission_guide.md) | `f678c374999c525867b38d95e0bdedda45729603de7e38687b2bebcadf40d87a` | historical_task_binding |
| E0123 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0123_submission_schema.json) | `7a77afcbcdac3d4b236971429bd7c49a85a80132ba03a86755c8b42767a9ab18` | historical_task_binding |
| E0124 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0124_critical_failures.json) | `2de4384ce555c2d706f9d50c07b52d8037877f2b4240d8f8f6ffc06948636df5` | historical_task_binding |
| E0125 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0125_evidence_map.json) | `f6e41000c784406a5d7d6e5921c961d9bb57db48e0c78ac2fd0429d4b66f9e2f` | historical_task_binding |
| E0126 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1a.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1a.xyz.snapshot) | `4435a0b932a4a1235df2ce77a42c83cd384a1f10e672c5f433b4e3b99645a7ff` | historical_task_binding |
| E0127 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1b.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1b.xyz.snapshot) | `81b54b65f613a4c6c69a6f996798e6ae7b55f2b3b4fa5f4321d6353b04aecba3` | historical_task_binding |
| E0128 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1c.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1c.xyz.snapshot) | `44c46e705af9dc905f903c78c9bb9682629f089c0cd4ae0e45faf3496d73f219` | historical_task_binding |
| E0129 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1d.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1d.xyz.snapshot) | `26e6c2d56f77f6b000882f719d5e554a859351d2de0be895225fce96c8f109d8` | historical_task_binding |
| E0130 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot) | `6929cbcc54ea18b8c632009d33c78661bd6b1aef0747233a19b02a29565d76ab` | historical_task_binding |
| E0131 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot) | `b3e370eae95d1370e9bb483e46f9dfb41888e17be5969227be2602cf9ec47640` | historical_task_binding |
| E0132 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot) | `5f041f09e173530358ecbf5148fed4782adea36290997a6440c64f9ec2d95ef1` | historical_task_binding |
| E0133 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot) | `ed46ef5839ba75cee2ea0caa4ba10310d9a7260539fcedc11c465db174ba198d` | historical_task_binding |
| E0134 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot) | `fd21ef0a95f5b6316de2404bad89caf01a9eb13441e449f6d2a0e2985f610d23` | historical_task_binding |
| E0135 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot) | `cbf75528b86a292b84ff72a66c7199f11533c8db1355778fda5f7d52480f8f4d` | historical_task_binding |
| E0136 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot) | `6960406ced75b00f72a8bcbb6cf3b6ddef56e987e5d81d3fb6778b6d09363a53` | historical_task_binding |
| E0137 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot) | `278d62181f011148a2f6692460eaa07b67a57188b1d845a906be2a69d232e040` | historical_task_binding |
| E0138 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/task_provenance/quality_repair_provenance.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/task_provenance/quality_repair_provenance.json.snapshot) | `2990909fcb07229a47453f06c4c13b32556c1be7fe4fff6fb87662a733dc8959` | historical_task_binding |
| E0139 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `d9c9809b8174ee362071b0be2091ebff1be8be95b313a0282083e4165697853c` | historical_task_binding |
| E0140 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/package_manifest.json.snapshot) | `94615cb613213eced6406316e8d7656f6c9117a60f9c1bc944f741272bbf6111` | historical_task_binding |
| E0141 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/paper_route.md.snapshot) | `63ef8760bbf28b4cfc233fe1e5bab9ea2360e164501b84870b9842a63868fcb4` | historical_task_binding |
| E0142 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/task_info.json.snapshot) | `69a0724563f36b15a7e26fdd1923a80e7b226f096e202b6a41184ce3344bb9f2` | historical_task_binding |
| E0143 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0143_reference_validation_plan.md) | `dd8dcec35bdea4da946302814702ebc3bcb90b2a741bd73837820db3bd5dcaf0` | historical_task_binding |
| E0144 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0144_scoring_rules.json) | `ac54b028e9878dc7afe2fea00777140af5e7094f7007584de8b94e81d5055283` | historical_task_binding |
| E0145 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/existing_evidence_reuse.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/existing_evidence_reuse.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0145_existing_evidence_reuse.json) | `2af1bcb233b131616a7cae1b65cd4647d75d04c67767dc606f97d2c311ae5f70` | historical_task_binding |
| E0146 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/offline_native_evidence_review.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/offline_native_evidence_review.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0146_offline_native_evidence_review.json) | `f47b7f018faaae84ac9dfe5fbce7000225f1dd252b3467d1a9b88a43a82e45e8` | historical_task_binding |
| E0147 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/scientific_acceptance_cases.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/scientific_acceptance_cases.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0147_scientific_acceptance_cases.json) | `d12752dbb2fe6fc3a1bd12bf95d0b881f4deb0d8d696d5c0bf5ee670bfb933b5` | historical_task_binding |
| E0148 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0148_source_scope_audit.json) | `8c84ab009f705b04d6a38be2c2d526af726a7ab11d730d8dfaabb4b401abe2a4` | historical_task_binding |
| E0149 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0149_source_scope_audit.md) | `9e6202c4fd743be2e13ed255cfbda9e1a7e36717f307ee6ee8f278532f5dad1f` | historical_task_binding |
| E0150 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/upgrade_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/upgrade_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0150_upgrade_audit.json) | `db367fa497a5c55dbf02746bc5615486ac295ca8654dadfa39bda7c0b6bc73bf` | historical_task_binding |
| E0151 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/v2_design_audit.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/v2_design_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0151_v2_design_audit.md) | `2b9033ce3c0a27db8e1ae9dba2320ff9539e1869fd26767cc52003c266c3ae93` | historical_task_binding |
| E0152 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/visibility_audit.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/task_provenance/visibility_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0152_visibility_audit.json) | `436e3b7154a5283ff6f99b91ccb50ae0ec1b54580624e538908f2385f658e387` | historical_task_binding |
| E0153 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/controls.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/controls.json.snapshot) | `aba89b600ba108f3c426a2ba43d2c33f46e1a74c6c8e110a65932f8fec405107` | historical_task_binding |
| E0154 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/data_provenance.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/data_provenance.json.snapshot) | `36b974ecc7b51acb107c37c0d54db96f53f905657d758ca43f68d8954d0c3e55` | historical_task_binding |
| E0155 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot) | `6929cbcc54ea18b8c632009d33c78661bd6b1aef0747233a19b02a29565d76ab` | historical_task_binding |
| E0156 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/objects.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/objects.json.snapshot) | `689b6368557612bd5a2c19f26d4727bdb9d8b702d58b85d5c47211637f6646ca` | historical_task_binding |
| E0157 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_guide.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_guide.md.snapshot) | `c1c28110295303e3fc7eece2e01a432bec7ddb8b9991f5f687b9b8b1b2986ee9` | historical_task_binding |
| E0158 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_schema.json.snapshot) | `0d401d000b657b204e2a6a99112e8e8cc9ee543636234ff78791b80a66dc19ea` | historical_task_binding |
| E0159 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/task.md.snapshot) | `116dc57084fa1b73981bf45544fa48da5b1d16a56b1fd660eb4f1947614ac2b8` | historical_task_binding |
| E0160 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/critical_failures.json.snapshot) | `4c5fe5af21ae969f3df669ca686fe5db35b243d065484ba941cba20c6054b03f` | historical_task_binding |
| E0161 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/evidence_map.json.snapshot) | `d72db790d1f596c07b187620ed55ce15d5aeffd52d195f2ec2adc9f6b091b883` | historical_task_binding |
| E0162 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/phase1_reference_binding.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/phase1_reference_binding.json.snapshot) | `1390578db1e876e8cd985c5e8855209e3cd03bafeedcc2d0eb4c9f5611c3446d` | historical_task_binding |
| E0163 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_conclusions.json.snapshot) | `0fee84cb0a2bcf8fc16c39008dcea2ac480f64c3476f31409e99170d2575d73e` | historical_task_binding |
| E0164 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_key_points.json.snapshot) | `b7adea4f7281277d9000e027d9d3e7992df4ceef5f6f7e521b3bcdcafeea4307` | historical_task_binding |
| E0165 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_validation_plan.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_validation_plan.md.snapshot) | `eed33a6e673f84d5da80f2f39ddfd4797d503ad958018afa7e4d558034f85eb4` | historical_task_binding |
| E0166 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/scoring_rules.json.snapshot) | `94a55c5a83a1ef7706eff3b78c552f1f07619a82730fbc91a7429f2dfd253568` | historical_task_binding |
| E0167 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/task_provenance/upgrade_audit.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/task_provenance/upgrade_audit.json.snapshot) | `dc7b454e9063352ff3e7c26eb62f646084296023dee5ab5e12ac220dda4eebc7` | historical_task_binding |
| E0168 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `fd1be66c9c2577e13e641a01b27021f36fbca82cbb18268060a61aa6de8f4e47` | historical_task_binding |
| E0169 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/package_manifest.json.snapshot) | `5465ddfb183a2547f942c05d96800b3634dccdf3f7f570365f64e3ea3e3de432` | historical_task_binding |
| E0170 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/paper_route.md.snapshot) | `2a9233faf0da53ed9e61efb2b849a6740ab045feee0caf8b85f2aa22e3e82a25` | historical_task_binding |
| E0171 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/task_info.json.snapshot) | `45580e9b418a1a75d94432df338e5852b5201b79ac816aaba20ff452061199b3` | historical_task_binding |
| E0172 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/paper_route.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0172_paper_route.md) | `7337920a23728f7651e20cbd6ea923652741720ae4ec02981be5776fa1520f81` | historical_task_binding |
| E0173 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/task_info.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_2f2aa11ea61a32bb/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0173_task_info.json) | `975d86cb3b23565edfc91a5d058e5ce3deeb52017d4171c87a90faa04f23cbc4` | historical_task_binding |
| E0174 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/data/inputs/objects.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/data/inputs/objects.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0174_objects.json) | `514621e36bd81d70a41d0404c1a81bdbf5c11775ae2a111e8c105e1324a6913b` | historical_task_binding |
| E0175 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/resources.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/resources.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0175_resources.md) | `97aa937cbbbb8509a22fd18b59a05a30aed4509ecc6d2cd7c8cd55e7da27e4e7` | historical_task_binding |
| E0176 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/submission_guide.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/submission_guide.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0176_submission_guide.md) | `f678c374999c525867b38d95e0bdedda45729603de7e38687b2bebcadf40d87a` | historical_task_binding |
| E0177 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/submission_schema.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/submission_schema.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0177_submission_schema.json) | `7a77afcbcdac3d4b236971429bd7c49a85a80132ba03a86755c8b42767a9ab18` | historical_task_binding |
| E0178 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0178_critical_failures.json) | `2de4384ce555c2d706f9d50c07b52d8037877f2b4240d8f8f6ffc06948636df5` | historical_task_binding |
| E0179 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/evidence_map.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0179_evidence_map.json) | `f6e41000c784406a5d7d6e5921c961d9bb57db48e0c78ac2fd0429d4b66f9e2f` | historical_task_binding |
| E0180 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1a.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1a.xyz.snapshot) | `4435a0b932a4a1235df2ce77a42c83cd384a1f10e672c5f433b4e3b99645a7ff` | historical_task_binding |
| E0181 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1b.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1b.xyz.snapshot) | `81b54b65f613a4c6c69a6f996798e6ae7b55f2b3b4fa5f4321d6353b04aecba3` | historical_task_binding |
| E0182 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1c.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1c.xyz.snapshot) | `44c46e705af9dc905f903c78c9bb9682629f089c0cd4ae0e45faf3496d73f219` | historical_task_binding |
| E0183 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1d.xyz.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/1d.xyz.snapshot) | `26e6c2d56f77f6b000882f719d5e554a859351d2de0be895225fce96c8f109d8` | historical_task_binding |
| E0184 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot) | `6929cbcc54ea18b8c632009d33c78661bd6b1aef0747233a19b02a29565d76ab` | historical_task_binding |
| E0185 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/submission_schema.json.snapshot) | `b3e370eae95d1370e9bb483e46f9dfb41888e17be5969227be2602cf9ec47640` | historical_task_binding |
| E0186 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/agent_input/task.md.snapshot) | `d922c38b4677e6f66bbfe16da406006fd36f4a7360b14797e9f7294c18be816d` | historical_task_binding |
| E0187 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/critical_failures.json.snapshot) | `ed46ef5839ba75cee2ea0caa4ba10310d9a7260539fcedc11c465db174ba198d` | historical_task_binding |
| E0188 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/evidence_map.json.snapshot) | `fd21ef0a95f5b6316de2404bad89caf01a9eb13441e449f6d2a0e2985f610d23` | historical_task_binding |
| E0189 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_conclusions.json.snapshot) | `cbf75528b86a292b84ff72a66c7199f11533c8db1355778fda5f7d52480f8f4d` | historical_task_binding |
| E0190 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/reference_key_points.json.snapshot) | `6960406ced75b00f72a8bcbb6cf3b6ddef56e987e5d81d3fb6778b6d09363a53` | historical_task_binding |
| E0191 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/scoring_rules.json.snapshot) | `278d62181f011148a2f6692460eaa07b67a57188b1d845a906be2a69d232e040` | historical_task_binding |
| E0192 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/task_provenance/quality_repair_provenance.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/task_provenance/quality_repair_provenance.json.snapshot) | `c952a56cf3990d412a7db5ce7a540637dd266ac19c8e272bfcee11cc346f8623` | historical_task_binding |
| E0193 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `a27d6e5d6860a8f4acecd25f2323581875611d527110ab06f782fe6dd4b74249` | historical_task_binding |
| E0194 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/package_manifest.json.snapshot) | `d7ed548b5198c346950cd5c09c11daae964b5f8c599e67db20a3577e1e451b0f` | historical_task_binding |
| E0195 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/paper_route.md.snapshot) | `63ef8760bbf28b4cfc233fe1e5bab9ea2360e164501b84870b9842a63868fcb4` | historical_task_binding |
| E0196 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/legacy_final_snapshot/task_info.json.snapshot) | `aa0fff42cbf89baf26e2f1e63d6dbdaf7bb1393a687cb2d4f25046dd3a36cde8` | historical_task_binding |
| E0197 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0197_reference_validation_plan.md) | `dd8dcec35bdea4da946302814702ebc3bcb90b2a741bd73837820db3bd5dcaf0` | historical_task_binding |
| E0198 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0198_scoring_rules.json) | `ac54b028e9878dc7afe2fea00777140af5e7094f7007584de8b94e81d5055283` | historical_task_binding |
| E0199 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/existing_evidence_reuse.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/existing_evidence_reuse.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0199_existing_evidence_reuse.json) | `2af1bcb233b131616a7cae1b65cd4647d75d04c67767dc606f97d2c311ae5f70` | historical_task_binding |
| E0200 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/offline_native_evidence_review.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/offline_native_evidence_review.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0200_offline_native_evidence_review.json) | `f47b7f018faaae84ac9dfe5fbce7000225f1dd252b3467d1a9b88a43a82e45e8` | historical_task_binding |
| E0201 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/scientific_acceptance_cases.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/scientific_acceptance_cases.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0201_scientific_acceptance_cases.json) | `d12752dbb2fe6fc3a1bd12bf95d0b881f4deb0d8d696d5c0bf5ee670bfb933b5` | historical_task_binding |
| E0202 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0202_source_scope_audit.json) | `8c84ab009f705b04d6a38be2c2d526af726a7ab11d730d8dfaabb4b401abe2a4` | historical_task_binding |
| E0203 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/source_scope_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0203_source_scope_audit.md) | `9e6202c4fd743be2e13ed255cfbda9e1a7e36717f307ee6ee8f278532f5dad1f` | historical_task_binding |
| E0204 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/upgrade_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/upgrade_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0204_upgrade_audit.json) | `2032b485bb4d35024b1dfd9921280f90aab0a5f5339e87e20f1d21b15805f643` | historical_task_binding |
| E0205 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/v2_design_audit.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/v2_design_audit.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0205_v2_design_audit.md) | `2b9033ce3c0a27db8e1ae9dba2320ff9539e1869fd26767cc52003c266c3ae93` | historical_task_binding |
| E0206 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/visibility_audit.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/task_provenance/visibility_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0206_visibility_audit.json) | `436e3b7154a5283ff6f99b91ccb50ae0ec1b54580624e538908f2385f658e387` | historical_task_binding |
| E0207 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/controls.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/controls.json.snapshot) | `aba89b600ba108f3c426a2ba43d2c33f46e1a74c6c8e110a65932f8fec405107` | historical_task_binding |
| E0208 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/data_provenance.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/data_provenance.json.snapshot) | `36b974ecc7b51acb107c37c0d54db96f53f905657d758ca43f68d8954d0c3e55` | historical_task_binding |
| E0209 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/experimental_absorption.json.snapshot) | `6929cbcc54ea18b8c632009d33c78661bd6b1aef0747233a19b02a29565d76ab` | historical_task_binding |
| E0210 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/objects.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/data/inputs/objects.json.snapshot) | `689b6368557612bd5a2c19f26d4727bdb9d8b702d58b85d5c47211637f6646ca` | historical_task_binding |
| E0211 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_guide.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_guide.md.snapshot) | `c1c28110295303e3fc7eece2e01a432bec7ddb8b9991f5f687b9b8b1b2986ee9` | historical_task_binding |
| E0212 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_schema.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/submission_schema.json.snapshot) | `0d401d000b657b204e2a6a99112e8e8cc9ee543636234ff78791b80a66dc19ea` | historical_task_binding |
| E0213 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/task.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/agent_input/task.md.snapshot) | `ad65bccfcc5f5ed479e66b3cb8ede13d1caa720244684e77f59a4ec23869bb99` | historical_task_binding |
| E0214 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/critical_failures.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/critical_failures.json.snapshot) | `4c5fe5af21ae969f3df669ca686fe5db35b243d065484ba941cba20c6054b03f` | historical_task_binding |
| E0215 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/evidence_map.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/evidence_map.json.snapshot) | `d72db790d1f596c07b187620ed55ce15d5aeffd52d195f2ec2adc9f6b091b883` | historical_task_binding |
| E0216 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/phase1_reference_binding.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/phase1_reference_binding.json.snapshot) | `4d65777c3ccc7d0524c586f90243f025249a0d9efc8c688df94b7340a6929e40` | historical_task_binding |
| E0217 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_conclusions.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_conclusions.json.snapshot) | `0fee84cb0a2bcf8fc16c39008dcea2ac480f64c3476f31409e99170d2575d73e` | historical_task_binding |
| E0218 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_key_points.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_key_points.json.snapshot) | `b7adea4f7281277d9000e027d9d3e7992df4ceef5f6f7e521b3bcdcafeea4307` | historical_task_binding |
| E0219 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_validation_plan.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/reference_validation_plan.md.snapshot) | `adf38b14346e26df9d069f207dd0b63bc5cf0032d6c4c63efad3b8029e3e36e3` | historical_task_binding |
| E0220 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/scoring_rules.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/scoring_rules.json.snapshot) | `94a55c5a83a1ef7706eff3b78c552f1f07619a82730fbc91a7429f2dfd253568` | historical_task_binding |
| E0221 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/task_provenance/upgrade_audit.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/task_provenance/upgrade_audit.json.snapshot) | `cefe5b33a6666ad2a0da5b1339759f3c57e3373acfe739643b5356f79a9b2bfd` | historical_task_binding |
| E0222 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `08adbb6d9bca955b59fb0bf1c0aec12a880e17cef5e0046d3b794c7d09444ce3` | historical_task_binding |
| E0223 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/package_manifest.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/package_manifest.json.snapshot) | `119adb1cb6b0622134bd4d6044b5b0e3672ad629262daca3866f8b913a4405a6` | historical_task_binding |
| E0224 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/paper_route.md.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/paper_route.md.snapshot) | `2a9233faf0da53ed9e61efb2b849a6740ab045feee0caf8b85f2aa22e3e82a25` | historical_task_binding |
| E0225 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/task_info.json.snapshot](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/v1_development_snapshot/task_info.json.snapshot) | `1e5075fc11e2142a9fcdadd723179fe1ef5a7299795349c4e5a5f254363a8bce` | historical_task_binding |
| E0226 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/paper_route.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/paper_route.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0226_paper_route.md) | `7337920a23728f7651e20cbd6ea923652741720ae4ec02981be5776fa1520f81` | historical_task_binding |
| E0227 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/task_info.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_2f2aa11ea61a32bb/task_info.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0227_task_info.json) | `e4d5f09c2f3f5708e83b416fd44568cf1c1e590f8e1a76a6f652ba5f9a40f64d` | historical_task_binding |
| E0228 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/BF2_PROVENANCE_CLOSURE_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0228_BF2_PROVENANCE_CLOSURE_20261001.json) | `673d05cdfd91ecd8a8168f266669ab16dec3a1eb91c072c1e5eb7e2e8bfa0de5` | evidence_or_analysis |
| E0229 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/release_20260930T134348/paper_2f2aa11ea61a32bb.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/v2_execution_20260929/release_20260930T134348/paper_2f2aa11ea61a32bb.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0229_paper_2f2aa11ea61a32bb.json) | `67ffd2ca7e1aac801f4cfc585213c065cbae818f36a1b906aa7e5a149fbb0e8d` | evidence_or_analysis |
| E0230 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0230_input.com) | `2e6a757f9d67c4584003db5a22e9f189eb2b58ec20e655cac43b3a0a80fbf68e` | input_or_analysis_code |
| E0231 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_CAM_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1a_CAM_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0231_input.com) | `695add26c1d2220fc020c2de059cbd93871db2c1a2f05cef46d3ab952d626de6` | input_or_analysis_code |
| E0232 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0232_input.com) | `87bbd56fa25c32f60701b2660f7bc960092bdb911a3cc99c44baed158f8065cd` | input_or_analysis_code |
| E0233 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_CAM_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1c_CAM_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0233_input.com) | `017debdc9188556ebc3c45eb33db9ea7f4155d5cb889a495060da023fb14e995` | input_or_analysis_code |
| E0234 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0234_input.com) | `2505359a3cbc234d6a2de8cf3b42cc9df81985a03876712531800e1d008ed0cc` | input_or_analysis_code |
| E0235 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_CAM_toluene_TD10/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1d_CAM_toluene_TD10/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0235_input.com) | `c4c95fab681ad542296b11a8e2341b720857031aa39b007486a06fe61c23e536` | input_or_analysis_code |
| E0236 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_opt/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/outputs/1b_commonchelate_opt/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_2f2aa11ea61a32bb/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0236_input.com) | `11acc4e53ce5e670ad16570fc2c363294011257893ef761f1287201c90d8555b` | input_or_analysis_code |
| N0237 | [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/agent_input/task.md](../agent_input/task.md) | `dd43729c371b972edac10ffd287fbe2c175efac8434180a92f629e86400bdb27` | latest_review_evidence |
| N0238 | [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json](reference_key_points.json) | `6f9007fb0608b31c0c75b6402c3fb5bbe9ccab7c5f081b2dd040b40f63066744` | latest_review_evidence |
| N0239 | [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json](reference_conclusions.json) | `ecf9ce5dbf2a81b6462a3ce79a10718f6595b39e8a687fb5a50c8a6221eb33c9` | latest_review_evidence |
| N0240 | [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json](scoring_rules.json) | `ac54b028e9878dc7afe2fea00777140af5e7094f7007584de8b94e81d5055283` | latest_review_evidence |
| N0241 | [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `98762212fbc7e8d3e04f75474accd25efadaab95cfda62524172d9c7ec63f9ee` | latest_review_evidence |
| N0242 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_2f2aa11ea61a32bb/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_2f2aa11ea61a32bb/verified_computation_reference.md) | `77cb5f5aa810af6eeda8b8518f73792eb07c491c3f5507a12964a3b47e578baf` | latest_review_evidence |
| N0243 | [tasks/v2_paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/task.md](../../../v2_paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/task.md) | `bc1baa1103e3742f6c85e1a2aae4474fb44fe5a76616e9c08c0476a4ea45ac3e` | latest_review_evidence |
| N0244 | [tasks/v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json) | `6f9007fb0608b31c0c75b6402c3fb5bbe9ccab7c5f081b2dd040b40f63066744` | latest_review_evidence |
| N0245 | [tasks/v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json) | `ecf9ce5dbf2a81b6462a3ce79a10718f6595b39e8a687fb5a50c8a6221eb33c9` | latest_review_evidence |
| N0246 | [tasks/v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json) | `ac54b028e9878dc7afe2fea00777140af5e7094f7007584de8b94e81d5055283` | latest_review_evidence |
| N0247 | [tasks/v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md](../../../v2_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md) | `98762212fbc7e8d3e04f75474accd25efadaab95cfda62524172d9c7ec63f9ee` | latest_review_evidence |
| N0248 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_2f2aa11ea61a32bb/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_2f2aa11ea61a32bb/verified_computation_reference.md) | `6b52e3c543b1c7f96d0d7a56b50452d3475b1fe046a559f41ed2d564f9f5b628` | latest_review_evidence |
| N0249 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0250 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/agent_input/task.md](../agent_input/task.md) | `dd43729c371b972edac10ffd287fbe2c175efac8434180a92f629e86400bdb27` |
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_key_points.json](reference_key_points.json) | `6f9007fb0608b31c0c75b6402c3fb5bbe9ccab7c5f081b2dd040b40f63066744` |
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_conclusions.json](reference_conclusions.json) | `ecf9ce5dbf2a81b6462a3ce79a10718f6595b39e8a687fb5a50c8a6221eb33c9` |
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/scoring_rules.json](scoring_rules.json) | `ac54b028e9878dc7afe2fea00777140af5e7094f7007584de8b94e81d5055283` |
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/critical_failures.json](critical_failures.json) | `2de4384ce555c2d706f9d50c07b52d8037877f2b4240d8f8f6ffc06948636df5` |
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/evidence_map.json](evidence_map.json) | `f6e41000c784406a5d7d6e5921c961d9bb57db48e0c78ac2fd0429d4b66f9e2f` |
| [tasks/v2_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `98762212fbc7e8d3e04f75474accd25efadaab95cfda62524172d9c7ec63f9ee` |

## Current scoring policy — 2026-10-19

The active policy is paper_science_v2: independent intermediate scientific findings and final conclusions sum to 100; no process points, partial-credit discretion or multiplier applies. Active nodes, rules, PDF sources and fixed inclusive tolerances are in the synchronized JSON files. Historical evaluator IDs, weights, freezes and process language in the preceding archive are not current scoring instructions. The public task and PR author-route contract are unchanged. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE acceptance and its scientific limitations remain; this migration runs no new chemistry calculations and does not certify publication readiness.

## Round 3 scoring-contract repair — 2026-10-19

All13 original leaves76/24 retained after source/native review. Clarified gas baseline versus toluene interpretation; no numerical windows added and no root-count gate. Existing chemical acceptance and all archived measurements/results above are unchanged. This is a contract/rubric repair with no new quantum calculations or online Judge certification. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_01/REPORT.md.

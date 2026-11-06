# 2026-10-28 V3范围与证据复用（group_07）

逐命题复用：generation_loss_account使用已执行RBF/测量模型及冷暖响应分析；conditional_kinetic_information复用同直径−20°C的0.4132620919、0.1520539119 s^-1条件log-yield量；microscopic_nonuniqueness复用qI模型的相同信号见证；continuous_optimum_limit复用坐标/类别约定敏感性。原7项改为4个最终结论，没有新增计算或量子化学要求。

AR/PR share four final outcomes and weights 30/30/25/15. PR retains source linear-RBF smoothing=0.2 and source interpretation as disclosed reproduction baseline; AR independently selects its analysis. No fixed rate targets/tolerances existed or are introduced. Observed cold/warm yield bands and post-quench definitions are evidence for the physical account, not independent points for repeating public facts. Conditional rate information and demonstrated nonuniqueness are genuine final answers to the question despite their former intermediate labels.

- No calibrated GC uncertainty or numerical detection limits are supplied; no elementary rate constants or statistical confidence intervals are certified.
- The product-only symmetry is conditional on its stated observation model; it does not prove global nonidentifiability of every model using all channels.
- The source omits RBF library, coordinate and polynomial conventions, and Table S2 and plot labels disagree at entries 3/7/17; no unique exact continuous optimum or author surface is certified.

以下历史正文原样保留；历史PASS不代表本次V3全面通过。

---

# V2 验证计算参考：1a 微流数据的动力学信息

论文：`paper_60f4c45810428116`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：此题的作者计算路线是实测网格的数据分析。作者的 linear-RBF/smoothing=0.2 已真实执行，23 个非堵塞点、类别缺失、采样极大值和冷长/暖短的有效区域保留；额外实际不可辨识性检验支持有限动力学解释。没有把读表误说成量子化学重现。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

What kinetic information about the transformation of benzyl chloromethyl sulfide 1a can be established from the measured residence-time/temperature grid, and which mechanistic or rate claims are not identifiable from those observations?

冻结题面中的科学目标：

What kinetic information about the transformation of benzyl chloromethyl sulfide 1a can be established from the measured residence-time/temperature grid, and which mechanistic or rate claims are not identifiable from those observations?

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_60f4c45810428116/documents/main.pdf](../../../../papers/paper_60f4c45810428116/documents/main.pdf) | `7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f` |
| [papers/paper_60f4c45810428116/documents/supplementary_001.pdf](../../../../papers/paper_60f4c45810428116/documents/supplementary_001.pdf) | `5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Author two-dimensional linear RBF with smoothing0.2 was actually executed. Unknown library/polynomial/coordinate convention is handled by declared and executed sensitivity alternatives. Native scientific work is data analysis, not a mandatory quantum calculation. Source redox and a five-pool model are auxiliary/outside required baseline.

1. 从作者 1a 流动实验数据核对 23 条非堵塞观测，保留温度、停留时间、流量稀释、淬灭定义、trace/nd 类别及另两条堵塞点；不把其他底物 1h/SPh 的叙事当作 1a 数据。

2. 按作者二维 linear-RBF、smoothing=0.2 路线实际分析，同时保留库/多项式/坐标约定未披露处的已执行敏感性分支；插值不被当作新的实验观测。

3. 直接重建 −78/−60/−40/−20°C 下所采网格的最高 2a 产率 95/93/89/88%，并计算 −20°C、同直径条件 87→47→23% 在 0.11→1.6→6.3 s 下的条件 log-yield 差 0.413262/0.152054 s⁻¹。

4. 执行 product-only 辨识检验：A→I→D、y=qI 下 (kf,kd,q)=(2,5,0.6) 与 (5,2,0.24) 产生相同信号，保存数值差为零的见证。该模型证明有条件的非唯一性，不将假设速率当成作者微观动力学常数。

5. 保留共同凸包内可达约 24.3 个百分点的插值坐标约定差、未知测量误差和淬灭限制；支持冷/长与暖/短有效区及生成/损耗解释，不声称连续最优点或唯一反应网络。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

### 最近一次原生有效性复核

本轮读 source_table.csv、analysis.py、两个原始 analysis_summary.json；RBF 中的实际矩阵残差约 10^-13、坐标规范敏感性与留一误差已保存。独立正文/SI 文本确认 linear RBF 和 smoothing 0.2。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Measured maximum2a yield% at-78,-60,-40,-20C | [95,93,89,88] | [95,93,89,88] | Exact audit of observed rows; maxima are sampled-grid findings, not continuousoptima. |
| Same-diameter conditional decline at-20C | 87→47→23% at0.11→1.6→6.3s | conditional log-yield contrasts0.413262 and0.152054 s^-1 | Arithmetic from source rows, with explicit first-order/invariant-capture/no-generation conditions; not elementary constants. |
| Product-only identifiability witness | Author describes generation versus decomposition; no calibrated microscopicrates | A→I→D, y=qI: (kf,kd,q)=(2,5,.6) and(5,2,.24) produce identical product signals | Saved actual analysis reports maximumdifference0; rates and capture fractions physically permitted. This is a conditional counterexample, not assertion of a true unique1a network. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_data — Faithful data and measurement model

冻结要求：Use source23 observations plus two clogged missing positions; preserve trace/n.d./dash without invented thresholds. State how post-quench yields, recovery, dilution and time/temperature definitions enter the analysis. Recompute data transformations from source rows and code. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：25行中2堵塞、23观测及trace/nd保留

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "All observed rows,categories,flow dilution,residence-time and quench definitions retained."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  }
]
```

### kp_inference — Quantitative kinetic information from the grid

冻结要求：Produce a reproducible analysis that establishes or bounds kinetic information rather than only redrawing a contour or copying an old redox scalar. Any model and parameter count are acceptable if physically/statistically appropriate. Effective rates and identifiable combinations may be valid outcomes; independent elementary rates are not required merely because V1 demanded them. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：实际趋势及条件log产率差

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Quantitative observed-time trends and conditional interval rates go beyond plotting."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  }
]
```

### kp_identifiability — Inference strength and alternative explanations tested

冻结要求：Substantiate the distinction between data-supported and assumption-dependent claims using suitable diagnostics. A good fit alone does not establish mechanism or unique rate constants; a failed fit alone does not prove non-identifiability. No mandatory A→Q or back-quench branch, optimizer count or holdout count. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：实际对称参数反例

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Actual product-only symmetry and interpolation alternatives establish the stated limited identifiability."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  }
]
```

### kp_uncertainty — Missingness, uncertainty and numerical validity

冻结要求：Account for missing/categorical data, unknown measurement errors and relevant numerical/model sensitivity. Declare assumptions instead of fabricating error bars. Check numerical reliability for the adopted method; no specific ODE or matrix-exponential solver is mandatory. All data are public so retrospective splits are not blind predictions. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：插值定义/缺失性；kp_conclusion与最终结论：只覆盖1a数据的可辨识信息。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Two clogged points,trace/nd,unknown assayerror and up to24.3percentage-point common-hull coordinate-convention spread are explicit."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  }
]
```

### kp_conclusion — Conclusions confined to1a dataset

冻结要求：Accept evidence-backed identifiability limitations or supported rate information. The1h/SPh back-quench interpretation cannot be asserted as source-established1a chemistry. Do not claim unseen-condition validation, precise microscopic barriers, or source-certified networks from an empirical fit. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：kp_data：25行中2堵塞、23观测及trace/nd保留；kp_inference：实际趋势及条件log产率差；kp_identifiability：实际对称参数反例；kp_uncertainty：插值定义/缺失性；kp_conclusion与最终结论：只覆盖1a数据的可辨识信息。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "No1h/SPh back-quench story imported as1a fact; no unseen-condition or microscopic-rate claim."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  }
]
```

### conclusion_investigation — What kinetic information about the transformation of benzyl chloromethyl sulfide 1a can be established from the measured residence-time/temperature grid, and which mechanistic or rate claims are not identifiable from those observations?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list.

当前复审：kp_data：25行中2堵塞、23观测及trace/nd保留；kp_inference：实际趋势及条件log产率差；kp_identifiability：实际对称参数反例；kp_uncertainty：插值定义/缺失性；kp_conclusion与最终结论：只覆盖1a数据的可辨识信息。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "finding": "Source empirical cold/long versus warm/short productive band reproduced with defensible limits on kinetic interpretation."
  }
]
```


证据记录：`E0027`。

```json
[
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  },
  {
    "evidence": [
      {
        "path": "papers/paper_60f4c45810428116/documents/main.pdf",
        "sha256": "7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f",
        "role": "primary_source",
        "physical_pages": [
          3,
          4,
          5,
          6
        ]
      },
      {
        "path": "papers/paper_60f4c45810428116/documents/supplementary_001.pdf",
        "sha256": "5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62",
        "role": "primary_source",
        "physical_pages": [
          4,
          5,
          6,
          19
        ]
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md",
        "sha256": "e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json",
        "sha256": "0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json",
        "sha256": "a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json",
        "sha256": "686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json",
        "sha256": "6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json",
        "sha256": "6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c",
        "role": "evidence"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json",
        "sha256": "41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4",
        "role": "evidence"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**5 个已保存分析阶段合计 2.57 分钟（执行时戳，秒级精度）；全流程不全；其中内层计时 41.98 秒，不重复加总**。

已记录资源：Python/SciPy RBF 与图像分析；回执请求 4 CPU/16 GiB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)；[补充计时记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/SUPPLEMENTAL_RUNTIME.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0028 · RBF_polynomial_default_control_20261007/a01/analysis.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0029 · source_pixel_mask_audit_v1/a01/analysis.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0030 · source_pixel_mask_audit_v1/a01/runner.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runner.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0031 · source_rbf_complement/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0032 · source_rbf_complement/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runner.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0033 · source_rbf_sensitivity/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0034 · source_rbf_sensitivity/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runner.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0035 · source_saved_surface_figure_comparison/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/analysis.log) | Python-analysis:41.9769 | 其他/未确认 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · source_saved_surface_figure_comparison/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/runner.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

补充的已执行分析/响应计时如下；外层与内层重叠部分不重复相加。
```json
{
  "kind": "Execution wrapper timestamps, one-second precision; not queue time",
  "records": [
    {
      "directory": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01",
      "elapsed_seconds": 12.0,
      "started_at": "2026-10-07T15:26:14Z",
      "finished_at": "2026-10-07T15:26:26Z",
      "return_code": 0,
      "sources": [
        {
          "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/runtime-started.txt",
          "sha256": "da71592d2cb1e9c2f3af77543f1be51dd957268389d70861b1994b144f026b78"
        },
        {
          "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/status.json",
          "sha256": "0cc375f785fd88445b2548fc003d1b8927ddfcfb6ae9a290bf185424fbba6037"
        }
      ]
    },
    {
      "directory": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01",
      "elapsed_seconds": 27.0,
      "started_at": "2026-10-06T10:47:56Z",
      "finished_at": "2026-10-06T10:48:23Z",
      "return_code": 0,
      "sources": [
        {
          "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runtime-started.txt",
          "sha256": "c82f3fb05d2b6d4a26f3ea090a0e17aeb30731fa262b6f826f8efdbb3844c339"
        },
        {
          "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/status.json",
          "sha256": "0b6336a2ac924ffed4ead016826dfc3bd165e150bf3a832b87c530c3b1ebad01"
        }
      ]
    },
    {
      "directory": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01",
      "elapsed_seconds": 29.0,
      "started_at": "2026-09-29T15:30:04Z",
      "finished_at": "2026-09-29T15:30:33Z",
      "return_code": 0,
      "sources": [
        {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runtime-started.txt",
          "sha256": "1dec9c8462133d38831c4c3ebc2c5bc8032f04c328b6c650a5043cfa56d84849"
        },
        {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/status.json",
          "sha256": "a92345f2b717d77aca146bb365f06534a1a919449195e758f09327e99546314b"
        }
      ]
    },
    {
      "directory": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01",
      "elapsed_seconds": 26.0,
      "started_at": "2026-09-29T15:04:35Z",
      "finished_at": "2026-09-29T15:05:01Z",
      "return_code": 0,
      "sources": [
        {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runtime-started.txt",
          "sha256": "f678bef8eb7c4b2472f404ef6ce525a7dc9cf59cb59d4c4257d505c3edfa3a03"
        },
        {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/status.json",
          "sha256": "e1522061ad822044994665430269b922088704b570d907fc7861387577612cbf"
        }
      ]
    },
    {
      "directory": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01",
      "elapsed_seconds": 60.0,
      "started_at": "2026-10-01T07:15:12Z",
      "finished_at": "2026-10-01T07:16:12Z",
      "return_code": 0,
      "sources": [
        {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/runtime-started.txt",
          "sha256": "1dc1e136304c2f7e6b278ae52d93687ee4754205c1a4b05f4986034c77e06a95"
        },
        {
          "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/status.json",
          "sha256": "b690afc8b1a31f59a4321657471c8525fef5c8ce2903b202c9373c26338222fc"
        }
      ]
    }
  ],
  "completed_seconds": 154.0,
  "note": "Partial saved analysis stages only; wrappers include their contained analysis timers, so do not add both. rc0 is not a scientific verdict."
}
```

提交请求的记录（与原生软件设置分开）：
```json
[
  {
    "evidence_id": "E0148",
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/submission_receipt.json",
    "requested": {
      "cpu": 4,
      "cpus_per_task": 4,
      "mem_gi": 16,
      "memory_per_cpu": "4G",
      "instances": 1,
      "priority": 6
    }
  },
  {
    "evidence_id": "E0161",
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/submission_receipt.json",
    "requested": {
      "cpu": 4,
      "cpus_per_task": 4,
      "mem_gi": 16,
      "memory_per_cpu": "4G",
      "instances": 1,
      "priority": 6
    }
  }
]
```

## 6. 已知偏差、失败分支和不能外推的结论

95/93/89/88% 是原实验采样最高值，经计算分析恢复，不是从分子动力学预测的产率；连续最优点、微观速率和图中每个像素未验证。

```json
[
  "Source table/figure rows3,7,17 conflict; table retained and variants analysed. Exact contour pixels or author plotting library are not required current scientific endpoints."
]
```


原独立审查的 `source_exceptions_and_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Three source table/figure label conflicts: source entries3,7,17. TableS2 is retained; figure variants are explicit sensitivity cases.",
  "Exact authorRBF library, polynomial and coordinate convention not identified; accepted only disclosed linear/smooth.2 route and scope-relevant empirical conclusions, not all contour pixels.",
  "No independently calibrated elementary rate constants or unique full network are claimed or required by the task."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_60f4c45810428116.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_60f4c45810428116/verified_computation_reference.md)；SHA-256 `0b619d2c8d1b50522eeee932fd0e5f67886f55c97b74d7fbbb1c043c271e384d`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_60f4c45810428116.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_60f4c45810428116.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_60f4c45810428116.json) | `694b5f49c45cd74c556970073b30eddb612c82f11f25e881518907154dad98ae` | evidence_or_analysis |
| E0002 | [tasks/v2_paper_reproduction/paper_60f4c45810428116/agent_input/task.md](../../../v2_paper_reproduction/paper_60f4c45810428116/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_task.md) | `fba76810466ed91262ca59549312770f5d8b0de655a3af27739bf365230297b7` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_60f4c45810428116/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_60f4c45810428116/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_reference_key_points.json) | `176b0b0dba4c0d17507cf7c4263329188168f9f235ee1a4d8b3db42975601dd4` | historical_task_binding |
| E0004 | [tasks/v2_paper_reproduction/paper_60f4c45810428116/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_60f4c45810428116/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_reference_conclusions.json) | `6c3bd86f4135dcfe3b57c592552beeab105ee062e7d470fb0a5c22b30eb6e42e` | historical_task_binding |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_audit_2_native_readback.json) | `ef1f45e93e2e7a9a0b0956e810ff714a67de5072fbba619fa5fb56e2340249c1` | evidence_or_analysis |
| E0006 | [papers/paper_60f4c45810428116/documents/main.pdf](../../../../papers/paper_60f4c45810428116/documents/main.pdf) | `7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f` | source_document |
| E0007 | [papers/paper_60f4c45810428116/documents/supplementary_001.pdf](../../../../papers/paper_60f4c45810428116/documents/supplementary_001.pdf) | `5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62` | source_document |
| E0008 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_sources/microflow_SI_p5.png](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/audit_2_sources/microflow_SI_p5.png) | `b19836125729e6446d5c30c44222792c30aaa17b06a9d25e3e4a9d475bcfba51` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/source_table.csv](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/source_table.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_source_table.csv) | `81f32cb51e8f3039ef6c2b2c1a2eb122525adaed196a34d83d78dc63b65e5f65` | evidence_or_analysis |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_analysis.py) | `126066a958ba18e279a9409810ba9764c61d1014b69d0823f4420eceb90979e8` | input_or_analysis_code |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/analysis_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_analysis_summary.json) | `e5fc157a376efef00060125d10fe0955472180ecf2c32cad4b72edaf4bc3f0f2` | evidence_or_analysis |
| E0012 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/analysis_summary.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_analysis_summary.json) | `c9171d5559004f8990899d97cb331751bb2a7e439d623d4b470194d5b4764031` | evidence_or_analysis |
| E0013 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_60f4c45810428116/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_60f4c45810428116/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_COMPUTATION_COVERAGE.json) | `0508f89ed03ff4bcbdca1e96b1790cbd2bb8883ceb9b2a43aee616cd2d983c96` | evidence_or_analysis |
| E0014 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_60f4c45810428116.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_60f4c45810428116.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_paper_60f4c45810428116.md) | `b81e6698f0ecc58c2ac4aca8d81d7f2d7a27af097f22351038f1f721d33d8fb5` | evidence_or_analysis |
| E0015 | [docs/v2_verification/papers/paper_60f4c45810428116/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `72cf48a01e43a973e77ca21790d00b15b20b72a8abedee62391624bade48178e` | historical_task_binding |
| E0016 | [tasks/v2_paper_reproduction/paper_60f4c45810428116/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_60f4c45810428116/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `72cf48a01e43a973e77ca21790d00b15b20b72a8abedee62391624bade48178e` | historical_task_binding |
| E0017 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_task.md) | `7f451384462692c4a7c0219fe0546c18c0efae65aeb82d1d88b6eee6bcbc605d` | historical_task_binding |
| E0018 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0018_reference_key_points.json) | `176b0b0dba4c0d17507cf7c4263329188168f9f235ee1a4d8b3db42975601dd4` | historical_task_binding |
| E0019 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_reference_conclusions.json) | `6c3bd86f4135dcfe3b57c592552beeab105ee062e7d470fb0a5c22b30eb6e42e` | historical_task_binding |
| E0020 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0020_scoring_rules.json) | `d3dd88c7be101c15b567648324a23753831ec6f0a92028b880ab60478016b07f` | historical_task_binding |
| E0021 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_task.md) | `fba76810466ed91262ca59549312770f5d8b0de655a3af27739bf365230297b7` | historical_task_binding |
| E0022 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0022_reference_key_points.json) | `176b0b0dba4c0d17507cf7c4263329188168f9f235ee1a4d8b3db42975601dd4` | historical_task_binding |
| E0023 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0023_reference_conclusions.json) | `6c3bd86f4135dcfe3b57c592552beeab105ee062e7d470fb0a5c22b30eb6e42e` | historical_task_binding |
| E0024 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_scoring_rules.json) | `d3dd88c7be101c15b567648324a23753831ec6f0a92028b880ab60478016b07f` | historical_task_binding |
| E0025 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_60f4c45810428116_source_and_hash_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_60f4c45810428116_source_and_hash_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_paper_60f4c45810428116_source_and_hash_readback.json) | `0d60fcdc12c1b16ce2aa861f996dd6a95edbd2390c2e333360e39af41f9df049` | evidence_or_analysis |
| E0026 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/EVIDENCE_MANIFEST.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/EVIDENCE_MANIFEST.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_EVIDENCE_MANIFEST.json) | `9346d3bea1158fe33d27a46e0822fe4906683c33437afb6f1acc8483df56d976` | evidence_or_analysis |
| E0027 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/evidence_map.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/evidence_map.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0027_evidence_map.json) | `b7c8a00e0bd4e1fce61aef115954ee1a39f3351f86454d50ce2ef1158da6eadc` | evidence_or_analysis |
| E0028 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/analysis.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0028_native_excerpt.json) | `78bd609de63e80026b9254fdf40083fd4c6836ca13a2200d7acd192b099ce8a3` | native_output |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/analysis.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_native_excerpt.json) | `eb73237ef34bc8b9792ba027c3549ac90d9db7eb5f41ee95f941138eb6424245` | native_output |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runner.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runner.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_native_excerpt.json) | `d916b53765c0d5903c8ae0ac56150b5f9a43006bfb8caa69d0073e5aa5db0b82` | native_output |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_native_excerpt.json) | `c9171d5559004f8990899d97cb331751bb2a7e439d623d4b470194d5b4764031` | native_output |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runner.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_native_excerpt.json) | `24718f9c8307dac631a47d0ce584096efa13f7aefbe9bc79bc7c67f1ef539f65` | native_output |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_native_excerpt.json) | `e5fc157a376efef00060125d10fe0955472180ecf2c32cad4b72edaf4bc3f0f2` | native_output |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runner.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_native_excerpt.json) | `2b09b6a149627dbc1ee455333feeaff2ed7b3ec767ad85998c3bd08468350027` | native_output |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_native_excerpt.json) | `574641e5e3dd385311723a694fc8729bc80fd73210245afd0c83ebf24241113d` | native_output |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/runner.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `0c99aabc00f16bcb2ccdcdc44d7a398b46b242dd899caadc8786a654d142b17a` | native_output |
| E0037 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/AUTHOR_ROUTE_RECONSTRUCTION.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/AUTHOR_ROUTE_RECONSTRUCTION.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_AUTHOR_ROUTE_RECONSTRUCTION.md) | `a283392d58ac22eabcda87bae3ab170a5a141edcd167f7fbe3517aa15bd24cce` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/results/rbf_default_control.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/results/rbf_default_control.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_rbf_default_control.json) | `aa1529cf11deff4a6a60a7b2796d029c84edaeb5cea2259140012e55696201c0` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/results/micro_per_observation_residuals.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/results/micro_per_observation_residuals.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_micro_per_observation_residuals.json) | `742b5fe5d28a4e541a2019c55652f152213a288546d5dadcecc3c766b97c13f3` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/mask_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_mask_audit.json) | `41fcb81f8a6cf1eb84be4aae620f10c40309677b07c77f4de8448150e235b3b4` | evidence_or_analysis |
| E0041 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_critical_failures.json) | `c6782ce3a21f346eb214d7ca2ca78a04ace33dc5e439378e4d0570066ded339f` | historical_task_binding |
| E0042 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_critical_failures.json) | `c6782ce3a21f346eb214d7ca2ca78a04ace33dc5e439378e4d0570066ded339f` | historical_task_binding |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/report.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_report.md) | `e078d84b912989cd58e0e55b55217ab821ab652ffcfb71cf776976ca03ec249e` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/report/results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_results.json) | `0ef9dc0897e56f63ffc282e17ffa9db7ae21112d4609b2e266f500d9a32a40a5` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/strict_final_claim_scope_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_strict_final_claim_scope_20261001.json) | `a7dcc95b9df0def6153881059a6c931ddd16af4c8685259365062b6d12a107be` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/observations.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_observations.json) | `686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_inputs.json) | `6c1bb6cab2ac2a9038349b14910ca4c46be8140450b20a8e2785ff509be6dd2f` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/results/figure_comparison.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_figure_comparison.json) | `6e01fccb4058b7d618bb8dbf15adf893b833778d8371cb2536321855ed504d3c` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis_plan.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/analysis_plan.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0049_analysis_plan.json) | `098f182d82a82f4a32c598d1cac94fa334f82c9dfe25f2c68aee332a68a809d7` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/preparation.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/preparation.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_preparation.json) | `aa1a391046f8b7078077bd62467f6140c39b16f2c4ad0fdebe881ca0b3878c3a` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/result_manifest.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/result_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_result_manifest.json) | `277e321390cfdde3bed16f53a00523e9f8c9839d7a973f4093f0868e20ee7e99` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runtime-host.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runtime-host.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_runtime-host.txt) | `c3402d0649d82a1afdb28e3dcb6ba8ee390185627305622ae922a7a88b53de85` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runtime-started.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/runtime-started.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_runtime-started.txt) | `f678bef8eb7c4b2472f404ef6ce525a7dc9cf59cb59d4c4257d505c3edfa3a03` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_status.json) | `e1522061ad822044994665430269b922088704b570d907fc7861387577612cbf` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/submit-command.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/submit-command.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_submit-command.json) | `d32ef6093c4f79a5022f4aa67cb2c73af6cc48f2e3149887072e70ed9ff5039a` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_submit-intent.json) | `a42083730c0caacbeeb48a9e3f63e583f355f463293f59a54da875a73c17b668` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/conditional_symmetry.csv](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/conditional_symmetry.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_conditional_symmetry.csv) | `c83ae443e76fb9a688a9fa37ceadc35e4562788fc01a1ce6852e94d678bad102` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_log10seconds.npz) | `eddc5b68e45708307b5aefc179d2b4a412a555c45ed5392401d0852eb4df94a8` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_log10seconds.pdf) | `1b5a15c4c8d8cccdbcd901131a579bf6e6af4adbf0d5b7d5967c081dffe575d1` | source_document |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_seconds.npz) | `c8c97de522f9be28748302e2fac88410599893430e1537aa3ddaf7a6a623f5e7` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__raw_C_seconds.pdf) | `2c4886344b261c4cfd0da6e8744c85ac4b641550c14b3aaf76a13cb4c0b6fadc` | source_document |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__scaled_C_log10seconds.npz) | `5f4cc985ac17759f60afc0d169b79daf781550d8a60c3f6c5859fdb3a8f368ed` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__scaled_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/plot_labels_trace_zero_display__scaled_C_log10seconds.pdf) | `c8f024fe4183da80cb0884e0d66bba24f741ad0def8a842dd0323f34c8366162` | source_document |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_log10seconds.npz) | `0fcaab3de59750812b5fbf308e10c5635955776715435c93ff25d7d170fb98cd` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_log10seconds.pdf) | `5ec1dae3eb5450d7e906f24f3015ce42abe0ccc9256c7175232a3f8c8ddea2b3` | source_document |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_seconds.npz) | `272d7437aa72623a3656e404a8fb1b7f3df8855c857e7ab2f8cc1685d9484411` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__raw_C_seconds.pdf) | `0b6350f68a1e72b91f453045e877f2b79a68eb6e1b8a722d785f7053c7ff8048` | source_document |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__scaled_C_log10seconds.npz) | `9480b670044b52466913f0ebe0c3aae7b503fbcfb9e50635e4076194c383ae50` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__scaled_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_numeric_only__scaled_C_log10seconds.pdf) | `724646766c461c44b2400829393930ceb26305ddf2a2d5f43ac2bd7ee7ffa57a` | source_document |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_log10seconds.npz) | `857e2f7202799a3100ae3eaf92e3b05dd3735dd05558a707cc0ba2c27cc9b228` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_log10seconds.pdf) | `93ddf8cddd549cae7ed0a4d2880a6f47f38902fa3023f09a289deba726403afa` | source_document |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_seconds.npz) | `5df1542e029bcba78215984f0e2789a96e19fd1c54613fd6b770abc2bc994752` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__raw_C_seconds.pdf) | `91c8c86586996423501126339daeaad71eed535f4bed453c00c8659ee7ca67dd` | source_document |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__scaled_C_log10seconds.npz) | `d749584280e789fc2e68f258ec77e6311d92c1e56ef6d9fdfa10e019df1b21ce` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__scaled_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_sensitivity/a01/results/table_trace_zero_display__scaled_C_log10seconds.pdf) | `6d283729ef068af0d93c28a44c0bb109e649fbb623bbca45c383c237ba2bac76` | source_document |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_analysis.py) | `f113e8df339e4f6f33d5364dc6adfe8d42d419ed41640dbc4ba691bba011b08a` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis_plan.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/analysis_plan.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_analysis_plan.json) | `a6849bf1196e8b69605af0eac4a32e62009340eaffaaee601ed04a89dae02a8d` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/observations.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/observations.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_observations.json) | `686c8c56e54779b6a9fe20c1e3ab0bb01ef0d15601c53eb2890dbfc0e3b741b7` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/preparation.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/preparation.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_preparation.json) | `dce716d4597b63ce58a893e8df6362f17db6bd5f5358c6d498bb5d268167de70` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/result_manifest.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/result_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_result_manifest.json) | `71bcf7d5d2e334aa867525c50d4f023fb23c5b8029a5607f58894017e44fd749` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runtime-host.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runtime-host.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_runtime-host.txt) | `4e839c7cb401ae9ba1c550c6cca0fa3ca277b9220d97400d0add7d4ae23e6180` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runtime-started.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/runtime-started.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_runtime-started.txt) | `1dec9c8462133d38831c4c3ebc2c5bc8032f04c328b6c650a5043cfa56d84849` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_status.json) | `a92345f2b717d77aca146bb365f06534a1a919449195e758f09327e99546314b` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/submit-command.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/submit-command.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_submit-command.json) | `b7e9fc7e3fbeb931b1da2e5509c46aee1368558b30c3bfd937252c6fe4da27d0` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_submit-intent.json) | `580642f45537beb2f6e5c5b6e2ec4f947a40d1536fd3747412a97b83918a0caa` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/table_trace_zero_display__raw_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/table_trace_zero_display__raw_C_log10seconds.npz) | `857e2f7202799a3100ae3eaf92e3b05dd3735dd05558a707cc0ba2c27cc9b228` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/table_trace_zero_display__raw_C_seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/table_trace_zero_display__raw_C_seconds.npz) | `5df1542e029bcba78215984f0e2789a96e19fd1c54613fd6b770abc2bc994752` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/table_trace_zero_display__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/table_trace_zero_display__scaled_C_log10seconds.npz) | `d749584280e789fc2e68f258ec77e6311d92c1e56ef6d9fdfa10e019df1b21ce` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_log10seconds.npz) | `96be206ed699331399d31f38f8d6923f6e2d3254c4c582f5125292359e56779f` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_log10seconds.pdf) | `3fcdceb389e94963deb376f3823efe34e3266a1fb0a30870398d823f8434a90f` | source_document |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_seconds.npz) | `571de0ea0dd49420803d1877d2949a61ff69bb096cbd0aa3902dbff63a11b873` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__raw_C_seconds.pdf) | `556f97a47d124134b6c985e37ba8d20b63a23990a7075de4ea137ca7f5823e39` | source_document |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__scaled_C_log10seconds.npz) | `13e290f63018612ca793479393170582c19d7ab78fe63cbebd0cf1d3549d1aae` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__scaled_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/numeric_only__scaled_C_log10seconds.pdf) | `d0cd6bcd6ef8e2db00341d2e212656a8b6ca7cb0e2a84d2c7e1102ba55a32861` | source_document |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_log10seconds.npz) | `619602e032937b8f383b1c58b6b574caff8c37e77a5570aa80b6d44da7b5c44c` | evidence_or_analysis |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_log10seconds.pdf) | `23ef92b5f0c50a4c8a2dfa469a9ad3253086009c504724770ee24a6fb4115459` | source_document |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_seconds.npz) | `d573cc5e47e7149b68963e334d2bce4ed3cfc8ffed4f697a5da6b0b091329451` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__raw_C_seconds.pdf) | `baf9e3050a173afd87e306cd4cd82aa7e9107382888e7500fd6f1e754972e6a6` | source_document |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__scaled_C_log10seconds.npz) | `00f740b5ff56dd7315a2258ee7f0f1bb108431dc98ac867819f12fbf9cf51b80` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__scaled_C_log10seconds.pdf](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_rbf_complement/a01/results/source_display_zero_nd_trace__scaled_C_log10seconds.pdf) | `807ed19c75a54d07c2a0db03b5d8beaa0cc590dac06572da4b5027366b06e8f0` | source_document |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/data/verification_context.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/data/verification_context.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0105_verification_context.json) | `4846e1ffee2dd8326e053be4b9c05308aef4ec4a31a71ab46d58bb7e74a759ff` | evidence_or_analysis |
| E0106 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/submission_receipt.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0106_submission_receipt.json) | `d9237a5098dfb0e3460f916d2b5193e820225e19c89dcf8f786d58de50017b09` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/submit-intent.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0107_submit-intent.json) | `ee678a30b2ca3500fd6554ba6425ae9e19cd73833a6cd30014f52e940ca08fbe` | evidence_or_analysis |
| E0108 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/inputs.sha256](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/inputs.sha256) | `f070ff5c9532c912c5949d619f6012822d051a8119dfb6f5d6d428df2ed12b1e` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/analysis.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0109_analysis.py) | `dc7ad32b6085192db7985a098f34e7d4c9641bb3bcceef3c53e0eed29037b706` | input_or_analysis_code |
| E0110 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runtime-host.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runtime-host.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0110_runtime-host.txt) | `8688f06fecaafd4ad69fb5f361dda76ccbdbac2eb39467b80a1205bfb60bf486` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/case.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0111_case.json) | `0f4d43fb148b4e6cb5e5ca9fcae5f31846f2564ba42bbb2c2414d3d299f8a2a8` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runtime-started.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/runtime-started.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0112_runtime-started.txt) | `c82f3fb05d2b6d4a26f3ea090a0e17aeb30731fa262b6f826f8efdbb3844c339` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/inputs.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0113_inputs.json) | `4a83bf47b5e4e85413121517f0d67bac2fd34a7a4ffb26dfa49d376d206bca94` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/run.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0114_run.sh) | `4443493dcc35228d2a0632aaf92710875949f3393edd9cd47c36e1a3c4e42599` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/native-return-code.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0115_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0116 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0116_status.json) | `0b6336a2ac924ffed4ead016826dfc3bd165e150bf3a832b87c530c3b1ebad01` | evidence_or_analysis |
| E0117 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_mask_audit.pdf](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_mask_audit.pdf) | `861b920dd9b90dead8fb6fd627c13f3abf44a1b992d97383b6d08c2d73a23f2c` | source_document |
| E0118 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_mask_audit.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_mask_audit.png) | `b91ccbd579510974f38a67f7ab5a9141348f51c770d263fcebea487d8540a6d2` | evidence_or_analysis |
| E0119 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_extreme_pixel_crops.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_extreme_pixel_crops.png) | `e640b4e3b228c343f0d5534c816afc3fffccb2d980ff08bce5a52689acc9d252` | evidence_or_analysis |
| E0120 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_mask_diagnostic.npz](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_mask_diagnostic.npz) | `61dd80756e1b1288eacb502af33c45e37d50161bc2b7e3d30e426f249c2d1e54` | evidence_or_analysis |
| E0121 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_mask_diagnostic.npz](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_mask_diagnostic.npz) | `cb2b89afc0a2316147daf6e69ede5ca7c3d2796c82744f42e453a58f0e988cd2` | evidence_or_analysis |
| E0122 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_mask_audit.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_mask_audit.png) | `76eea2f403cc3f42ecb6cab8b89ea1398d9da7e51d2165a75d6c0e5d20357c56` | evidence_or_analysis |
| E0123 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_mask_audit.pdf](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/3a_mask_audit.pdf) | `de83e0fdda16004aa460b28b6069867310bc27ccf17a2a0f4aa4f6c50701dada` | source_document |
| E0124 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_extreme_pixel_crops.png](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/source_pixel_mask_audit_v1/a01/results/2a_extreme_pixel_crops.png) | `5d734cce120e791867073b71f495012955df8fa6740f67a0669e7c00d7b38aa6` | evidence_or_analysis |
| E0125 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/RETURNED_JOB_INTAKE_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/RETURNED_JOB_INTAKE_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0125_RETURNED_JOB_INTAKE_20261006.json) | `81ad90dab8b6b28335b8f0d1ef495502db8ec7c9c7a2563d0f2702bcf4318d08` | evidence_or_analysis |
| E0126 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/INHERITED_ARTIFACT_HASH_READBACK_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/INHERITED_ARTIFACT_HASH_READBACK_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0126_INHERITED_ARTIFACT_HASH_READBACK_20261006.json) | `1d9b2b551d31fe21aebd515fb99d19370a190df54693427a70c0e515a661bd98` | evidence_or_analysis |
| E0127 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/FINAL_PLATFORM_READBACK_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/FINAL_PLATFORM_READBACK_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0127_FINAL_PLATFORM_READBACK_20261006.json) | `6609e7eb6da16aefaead2ffa26168a9e778687fd5fd1c839ac3cc7e7b8f2afa7` | evidence_or_analysis |
| E0128 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_60f4c45810428116/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0128_package_manifest.json) | `1454ed0530ec673be10ca789bafa05e07e8886d09cf4b8f8ff08116aa9d84cd7` | historical_task_binding |
| E0129 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_60f4c45810428116/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0129_package_manifest.json) | `0e78c779e4882404de9d6b69be72865d4061df893830dd92782ab09e2895de2d` | historical_task_binding |
| E0130 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/VERIFICATION_REPORT.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/VERIFICATION_REPORT.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0130_VERIFICATION_REPORT.md) | `090b8bb8803154375f32a36932b06193e20e0bcbdc1cd4cc2c77de54f035a849` | evidence_or_analysis |
| E0131 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/SOURCE_COMPARISON.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/SOURCE_COMPARISON.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0131_SOURCE_COMPARISON.json) | `e768cd6ef45985d6c83266338f44f4eea5ab5ab820081e81c97335a0f2703301` | evidence_or_analysis |
| E0132 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/RECOVERY_PLAN.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/RECOVERY_PLAN.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0132_RECOVERY_PLAN.json) | `982d799d8e8e0eea5730eca15b731910c705af2ecd399b07bd8079dbbabcfbd5` | evidence_or_analysis |
| E0133 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/TASK_SCOPE_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/TASK_SCOPE_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0133_TASK_SCOPE_REVIEW.json) | `3681c9bb829cc44003ba6e6f65de14ca48d9c0da78ad562444abaf743cfba448` | evidence_or_analysis |
| E0134 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/NEW_NATIVE_ACCEPTANCE_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/NEW_NATIVE_ACCEPTANCE_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0134_NEW_NATIVE_ACCEPTANCE_20261006.json) | `bd10e6716992e6956fe2b5e990dc8cb7975987a9e78b9868a1acd55e68331d0c` | evidence_or_analysis |
| E0135 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/SUBMISSION_PARSER_INCIDENTS_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/SUBMISSION_PARSER_INCIDENTS_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0135_SUBMISSION_PARSER_INCIDENTS_20261006.json) | `b27101ccf48981335f65914ececcbf4f00728256a929931a5a03b55d67ba886a` | evidence_or_analysis |
| E0136 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/SUPERVISION_EVENT_INTAKE_20261006T133201Z.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/SUPERVISION_EVENT_INTAKE_20261006T133201Z.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0136_SUPERVISION_EVENT_INTAKE_20261006T133201Z.json) | `00c8728964f154666f769ec52fe3d7ca3cc5d91498593aae50c12170b0fc4d45` | evidence_or_analysis |
| E0137 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/SUPERVISION_PLATFORM_RECHECK_20261006.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/SUPERVISION_PLATFORM_RECHECK_20261006.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0137_SUPERVISION_PLATFORM_RECHECK_20261006.json) | `7ca77b31e2ca0a4149b53ea12b8bebcd00b90706d95ba742213113baf3469450` | evidence_or_analysis |
| E0138 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/SOURCE_REVIEW_ADDENDUM_20261007.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/SOURCE_REVIEW_ADDENDUM_20261007.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0138_SOURCE_REVIEW_ADDENDUM_20261007.md) | `26efeb2c088211f27ff64f6ca8cb3b63f17bd897381d98fbcb6d402ddb881037` | evidence_or_analysis |
| E0139 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/PUBLIC_SOURCE_REVIEW_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/PUBLIC_SOURCE_REVIEW_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0139_PUBLIC_SOURCE_REVIEW_20261007.json) | `26d4e56faa579e2b65e46c3e0509a1bbbe3477ce12febee1c10eadcb8c9175e8` | evidence_or_analysis |
| E0140 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/RETURNED_JOB_INTAKE_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/RETURNED_JOB_INTAKE_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0140_RETURNED_JOB_INTAKE_20261007.json) | `3107560f56c5ff3fa4843e01984942521b3d062f6aecb31cc44c5088b8a9e92f` | evidence_or_analysis |
| E0141 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/analysis.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0141_analysis.py) | `4a65c09845475ee63ad20f6cc38fb75f473d09e7b32f1ce2439dd88684a34f72` | input_or_analysis_code |
| E0142 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/inputs.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0142_inputs.json) | `0083a7ddbaae0633edb1451d0f7115962b54b8d7c434df7071bfda94a636c7e0` | evidence_or_analysis |
| E0143 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/inputs.sha256](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/inputs.sha256) | `eca92c769ee9c546a3344b80a0fecf2b61bb942f1d8699a4e76f724877d68a2e` | evidence_or_analysis |
| E0144 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/run.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0144_run.sh) | `0a0a01f45788cd6c5fba5991b30e71e82096fabc58ee5ffbfffae3025a67e0a7` | input_or_analysis_code |
| E0145 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/case.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0145_case.json) | `56723baf63f791d31cc013489b05d6cd5a49b9f868bce74733e1eb6da1667e82` | evidence_or_analysis |
| E0146 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/LOCAL_PREFLIGHT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/LOCAL_PREFLIGHT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0146_LOCAL_PREFLIGHT.json) | `c282eb641f0ceaff08a2f210ce9eda3641691b19dbfaeb7485bf9a39b13e7edf` | evidence_or_analysis |
| E0147 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/submit-intent.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0147_submit-intent.json) | `db3b638673eaa1825bed9be13f8533bc9a1a798a34e6d6f5e832147c09846a8a` | evidence_or_analysis |
| E0148 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/submission_receipt.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0148_submission_receipt.json) | `543bc7dd3df0a85831a090fc01ec98d647a60baf6dd96750f9bb996bbec0bd95` | evidence_or_analysis |
| E0149 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/IMMEDIATE_ACCEPTANCE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/IMMEDIATE_ACCEPTANCE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0149_IMMEDIATE_ACCEPTANCE.json) | `3411698b4b0ccf19ecdd7e196e1e2c9e467acf055bc69e87a39dc1a5ca0405a0` | evidence_or_analysis |
| E0150 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/CLOSEOUT_DISPOSITION_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/CLOSEOUT_DISPOSITION_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0150_CLOSEOUT_DISPOSITION_20261007.json) | `2c6a41afb667894d3fd473d881c9202a2517d135323c45c3e51a098e97249440` | evidence_or_analysis |
| E0151 | [docs/v2_verification/history/strict_author_route_validation_20261001/sequential_closeout_20261007T163751Z/deliveries/W09.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/sequential_closeout_20261007T163751Z/deliveries/W09.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0151_W09.json) | `09f2be7b734ae79ad55f089239131cd9772114e875c5ba69cac1dd43303a943a` | evidence_or_analysis |
| E0152 | [docs/v2_verification/history/strict_author_route_validation_20261001/sequential_closeout_20261007T163751Z/deliveries/W09.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/sequential_closeout_20261007T163751Z/deliveries/W09.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0152_W09.md) | `21b54b750fca362a87954405974ad668dbb759f4d3505427b4fd76565979bf85` | evidence_or_analysis |
| E0153 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/RETURNED_JOB_INTAKE_CLOSEOUT_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/RETURNED_JOB_INTAKE_CLOSEOUT_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0153_RETURNED_JOB_INTAKE_CLOSEOUT_20261007.json) | `d725d54794d8e0e7bd25d80b1e36fb58c1b160f67ef7148e1dd96d9c79de86d0` | evidence_or_analysis |
| E0154 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/native-return-code.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0154_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0155 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_polynomial_default_control_20261007/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0155_status.json) | `0cc375f785fd88445b2548fc003d1b8927ddfcfb6ae9a290bf185424fbba6037` | evidence_or_analysis |
| E0156 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/analysis.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0156_analysis.py) | `33337f984482a1ee77bcab2c592f64d3a2c06cf7f85a2168f90ba150f8fae9d2` | input_or_analysis_code |
| E0157 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/inputs.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0157_inputs.json) | `d025142ca32187da05310b39e233b9124531e6c245ef5bce1f0b505aa29a3526` | evidence_or_analysis |
| E0158 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/run.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0158_run.sh) | `634bd9610bf1b9af269da333235f8510530bdd9b485d9c032b062c828f7314c2` | input_or_analysis_code |
| E0159 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/inputs.sha256](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/inputs.sha256) | `ea513efc41adede2af98d161ee58ddbb6b135d56484fa74fc9e6aa12ae1128af` | evidence_or_analysis |
| E0160 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/RECOVERY_PLAN.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/RECOVERY_PLAN.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0160_RECOVERY_PLAN.json) | `ba7dbd3b825f33a37d9d84bb4a89594df92b841eafd7b76363fe1c8c396da1e8` | evidence_or_analysis |
| E0161 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/submission_receipt.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0161_submission_receipt.json) | `fbed05f6a30209f769d3e6c0a8443c7cfd79dce379a6ca5e0e21943196540e2d` | evidence_or_analysis |
| E0162 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/IMMEDIATE_ACCEPTANCE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W09/papers/paper_60f4c45810428116/outputs/RBF_INP_per_observation_join_20261007/a01/IMMEDIATE_ACCEPTANCE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0162_IMMEDIATE_ACCEPTANCE.json) | `18cab0ade22511e834a8019c9b48594e55645d02292c865f7803ccc0712b5ef5` | evidence_or_analysis |
| E0163 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0163_analysis.py) | `cc48c9a68498891ff4fbe4a3dd10cd738b488e7be3b8574926b74d5e69c370e9` | input_or_analysis_code |
| E0164 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_60f4c45810428116/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0164_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| E0165 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/2a__plot_labels_trace_zero_display__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/2a__plot_labels_trace_zero_display__scaled_C_log10seconds.npz) | `5f4cc985ac17759f60afc0d169b79daf781550d8a60c3f6c5859fdb3a8f368ed` | evidence_or_analysis |
| E0166 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/3a__source_display_zero_nd_trace__scaled_C_log10seconds.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_60f4c45810428116/v2_execution_20260929/outputs/source_saved_surface_figure_comparison/a01/3a__source_display_zero_nd_trace__scaled_C_log10seconds.npz) | `00f740b5ff56dd7315a2258ee7f0f1bb108431dc98ac867819f12fbf9cf51b80` | evidence_or_analysis |
| N0167 | [tasks/v2_autonomous_research/paper_60f4c45810428116/agent_input/task.md](../agent_input/task.md) | `7f451384462692c4a7c0219fe0546c18c0efae65aeb82d1d88b6eee6bcbc605d` | latest_review_evidence |
| N0168 | [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/reference_key_points.json](reference_key_points.json) | `176b0b0dba4c0d17507cf7c4263329188168f9f235ee1a4d8b3db42975601dd4` | latest_review_evidence |
| N0169 | [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/reference_conclusions.json](reference_conclusions.json) | `6c3bd86f4135dcfe3b57c592552beeab105ee062e7d470fb0a5c22b30eb6e42e` | latest_review_evidence |
| N0170 | [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/scoring_rules.json](scoring_rules.json) | `d3dd88c7be101c15b567648324a23753831ec6f0a92028b880ab60478016b07f` | latest_review_evidence |
| N0171 | [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `f09741ee420221177b654a7e9fa08388f638380bf9491f532c585ee0d1ba5338` | latest_review_evidence |
| N0172 | [tasks/v2_paper_reproduction/paper_60f4c45810428116/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_60f4c45810428116/evaluation/scoring_rules.json) | `d3dd88c7be101c15b567648324a23753831ec6f0a92028b880ab60478016b07f` | latest_review_evidence |
| N0173 | [tasks/v2_paper_reproduction/paper_60f4c45810428116/evaluation/reference_validation_plan.md](../../../v2_paper_reproduction/paper_60f4c45810428116/evaluation/reference_validation_plan.md) | `f09741ee420221177b654a7e9fa08388f638380bf9491f532c585ee0d1ba5338` | latest_review_evidence |
| N0174 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0175 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_60f4c45810428116/agent_input/task.md](../agent_input/task.md) | `7f451384462692c4a7c0219fe0546c18c0efae65aeb82d1d88b6eee6bcbc605d` |
| [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/reference_key_points.json](reference_key_points.json) | `176b0b0dba4c0d17507cf7c4263329188168f9f235ee1a4d8b3db42975601dd4` |
| [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/reference_conclusions.json](reference_conclusions.json) | `6c3bd86f4135dcfe3b57c592552beeab105ee062e7d470fb0a5c22b30eb6e42e` |
| [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/scoring_rules.json](scoring_rules.json) | `d3dd88c7be101c15b567648324a23753831ec6f0a92028b880ab60478016b07f` |
| [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/critical_failures.json](critical_failures.json) | `c6782ce3a21f346eb214d7ca2ca78a04ace33dc5e439378e4d0570066ded339f` |
| [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/evidence_map.json](evidence_map.json) | `b37a8d465e02cc96fa55ce843dcf26c33ece0a5ae503f9bd736f9438efc36f12` |
| [tasks/v2_autonomous_research/paper_60f4c45810428116/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `f09741ee420221177b654a7e9fa08388f638380bf9491f532c585ee0d1ba5338` |


## Current scoring migration — 2026-10-19
Active policy: paper_science_v2; 100 binary scientific-result points, intermediate findings and final conclusions, no process awards or multipliers. The current scoring_rules/reference_key_points/reference_conclusions supersede historical scoring descriptions and weights in this retained verification history. This migration performs no new chemistry calculation and does not upgrade verification acceptance. Physical and scientific limitations remain: Source table/figure entries3,7,17 conflict; TableS2 remains the reference with declared variants. Author RBF library, polynomial and coordinate convention are underspecified. Verification found up to24.3 percentage-point coordinate sensitivity and a zero-difference product-only identifiability witness, but establishes neither unique microscopic constants nor continuous optimum. No full reactor CFD or other substrate required.


## Authorized scoring-contract repair — 2026-10-19 (round3)
Removed duplicate inferential_scope8; redistributed4+4 to conditional kinetic information and demonstrated microscopic nonuniqueness. The genuinely integrative generation_loss_synthesis remains12. New split88/12. Public scoring prose now describes100-point binary scientific results; reporting a contrary/unresolved answer does not automatically satisfy another target. This append changes the current evaluation contract only; original verification history remains verbatim, no new chemistry or acceptance upgrade is claimed.

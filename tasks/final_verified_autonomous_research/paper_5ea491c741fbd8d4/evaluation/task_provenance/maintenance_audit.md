# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_5ea491c741fbd8d4`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

修复候选级未求 Hessian 的 null/诊断表示；成功选中候选仍要求真实验证。PR 主协议选正文直接计算描述的 B3LYP/6-311+G(d,p)；另一处 6-31+G(d,p) 属原文冲突，未因本地数值选择方法。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：isoxazole 1a 五候选轨道

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_5ea491c741fbd8d4`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的身份、无泄露输入及成功计算成立；需修失败候选 schema，并确认方法自由与轨道数值的比较口径。

复审摘要：五起点/三极小值成立；未计算 Hessian 的失败候选不能如实填 schema；自由方法数值比较需说明。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_5ea491c741fbd8d4)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_5ea491c741fbd8d4`；group：`group_1`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p3–5 的对象/计算方法、p7 Table 2 的 isoxazole 1a 前线轨道参考。

- [正文](../../../../../papers/paper_5ea491c741fbd8d4/documents/main.pdf)
- [SI](../../../../../papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

公开名称、SMILES、E 构型和中性单重态，3D 需自行生成；没有作者优化坐标、轨道能或最优候选答案。PR 格式拆分后补回 objective 的 isoxazole 1a 主语，不改变指导内容。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

五条独立起始候选 Opt/Freq 均 75 实频，几何去重为 3 个不同极小值；selected seed 303 的 HOMO −6.56393059 eV、LUMO −2.88386271 eV、gap 3.68006788 eV，与 −6.3362/−2.7171/3.6191 的 AR、PR 既定容差均相容，gap 为实际差值。

有限五候选/三终态支持任务既定结构和轨道比较，不证明穷尽全局构象，也不把轨道能当实验氧化还原势。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/report/results.json) 保持只读。

专门核查记录：

- [provenance/orbital_closure_audit_20260915.json](../../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/provenance/orbital_closure_audit_20260915.json)
- [artifacts/author_orbitals_20260915.json](../../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/author_orbitals_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `ar_rule_search` → `ar_process_search` | semantic；真实证据/适用边界见第 3 节 | `$.method.justification` / `$.conformer_search` / `$.candidates` |
| `ar_rule_validation` → `ar_process_validation` | semantic；真实证据/适用边界见第 3 节 | `$.candidates` / `$.selected_candidate_id` / `$.sensitivity_assessment` |
| `ar_rule_gap` → `ar_result_gap` | 3.680067876；参考 3.6191 ± 0.35 eV；算术通过 | `$.gap_eV` |
| `ar_rule_homo` → `ar_result_orbitals` | -6.56393059；参考 -6.3362 ± 0.45 eV；算术通过 | `$.homo_eV` |
| `ar_rule_lumo` → `ar_result_orbitals` | -2.883862714；参考 -2.7171 ± 0.45 eV；算术通过 | `$.lumo_eV` |
| `ar_rule_final` → `ar_final_conclusion` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` / `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final；不更改目标或容差。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_5ea491c741fbd8d4`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

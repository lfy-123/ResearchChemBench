# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_5d94285cfbd51973`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

定向复核 AZ9 正确 53 原子图、conventional IP/EA/η/μ/χ/ω 算术和有限构象/基组敏感性；保留 9 minima/611 候选证据，不将有限搜索宣称全局证明，不推断生物活性。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：AZ9 九构象电子描述符

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_5d94285cfbd51973`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的 AZ9 身份、无泄露输入、构象/灵敏度链和描述符定义相容；未发现新的实质性缺口。

复审摘要：SMILES自包含；9极小值与9敏感性单点支持；按公开conventional公式评分。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_5d94285cfbd51973)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_5d94285cfbd51973`；group：`group_4`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI PDF p7 方法、p41 Table S12 的 AZ9 轨道/描述符。任务已有 conventional μ/ω 定义，不套用 SI 的非标准/有符号问题派生行。

- [正文](../../../../../papers/paper_5d94285cfbd51973/documents/main.pdf)
- [SI](../../../../../papers/paper_5d94285cfbd51973/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

公开AZ9 SMILES与身份、电荷自旋，53原子neutral singlet；无作者坐标/能量。PR补回objective主语，保持原有合法指令范围。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

九条B3LYP/6-31G(d)构象极小值均153实频；12轮611候选池的TFD去重覆盖9盆地，最低basin04 E=−1719.93864109 Eh。HOMO−5.59139565、LUMO−1.16981749、gap4.42157815 eV、dipole6.0404 D均满足目标；九条更大基组单点形成敏感性链。

代表分支基组敏感性 ΔHOMO−0.3496663、ΔLUMO−0.4106198、Δgap−0.0609535 eV、Δdipole+0.3157 D如实保留，不拿敏感性支替换主路线。有限池不等于全局极小值证明；IP/EA是轨道派生，不是ΔSCF/实验量。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_4/paper_5d94285cfbd51973/report/results.json) 保持只读。

专门核查记录：

- [provenance/author_descriptor_closure_20260914.json](../../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/author_descriptor_closure_20260914.json)
- [provenance/evaluation_task_qualification.json](../../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/evaluation_task_qualification.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `ar_r_process` → `ar_process` | semantic；真实证据/适用边界见第 3 节 | `$.conformer_search.candidates` / `$.stationarity.evidence` |
| `ar_r_method` → `ar_method` | semantic；真实证据/适用边界见第 3 节 | `$.method.software` / `$.method.electronic_structure_method` / `$.method.basis_or_representation` / `$.method.phase` / `$.method.justification` |
| `ar_r_search` → `ar_search` | semantic；真实证据/适用边界见第 3 节 | `$.conformer_search.generated_count` / `$.conformer_search.deduplicated_count` / `$.conformer_search.advanced_count` / `$.conformer_search.frequency_validated_count` / `$.conformer_search.energy_span_kcal_mol` / `$.conformer_search.stopping_evidence` / `$.conformer_search.coverage_rationale` |
| `ar_r_structure` → `ar_structure` | semantic；真实证据/适用边界见第 3 节 | `$.selected_structure.xyz` / `$.selected_structure.selection_basis` / `$.stationarity.imaginary_frequency_count` / `$.stationarity.evidence` |
| `ar_r_sensitivity` → `ar_sensitivity` | semantic；真实证据/适用边界见第 3 节 | `$.sensitivity.test` / `$.sensitivity.delta_homo_ev` / `$.sensitivity.delta_lumo_ev` / `$.sensitivity.delta_gap_ev` / `$.sensitivity.delta_dipole_debye` / `$.sensitivity.interpretation` |
| `ar_r_homo` → `ar_homo` | -5.591395646；参考 -5.5758 ± 0.35 eV；算术通过 | `$.properties.homo_ev` |
| `ar_r_lumo` → `ar_lumo` | -1.169817495；参考 -1.1556 ± 0.35 eV；算术通过 | `$.properties.lumo_ev` |
| `ar_r_gap` → `ar_gap` | 4.421578151；参考 4.4202 ± 0.35 eV；算术通过 | `$.properties.gap_ev` |
| `ar_r_dipole` → `ar_dipole` | 6.0404；参考 5.847 ± 1 D；算术通过 | `$.properties.dipole_debye` |
| `ar_r_derived` → `ar_derived` | semantic；真实证据/适用边界见第 3 节 | `$.properties.ip_ev` / `$.properties.ea_ev` / `$.properties.hardness_ev` / `$.properties.softness_ev_inverse` / `$.properties.chemical_potential_ev` / `$.properties.electronegativity_ev` / `$.properties.electrophilicity_ev` |
| `ar_r_final` → `ar_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` / `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final。保留已公开且已验证的conventional descriptor公式；不变更gold/容差。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_5d94285cfbd51973`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

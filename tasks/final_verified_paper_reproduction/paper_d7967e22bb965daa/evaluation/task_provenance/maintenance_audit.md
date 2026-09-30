# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_d7967e22bb965daa`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

四份 TS 终态已从公开侧移入 author_results，可恢复；新增无目标几何/能量的四路线及原子角色。保留两 INT2 反应物、quartet、局部零点和原势垒；PR 提供无答案热化学路线，失败未知频率不填零。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：四个 quartet 插入 TS 的局部自由能势垒

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_d7967e22bb965daa`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

仅 PR；四个作者 TS 答案直接公开，必须先确认候选定义与去除坐标的修法。

复审摘要：四个68原子SI TS公开；四局部势垒真实有据，不能用给定TS替代TS搜索。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_d7967e22bb965daa)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_d7967e22bb965daa`；group：`group_2`；模式：`paper_reproduction`。

结论：**HOLD，暂不用于正式评估**。四个公开候选 TS 坐标是作者求得的终态；是否改为无答案候选构建任务须先决定。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p10；SI PDF p92–97 的 M06L 路线/熵处理，INT2A p141–144、INT2B p149–151，四 TS p156–180。

- [正文](../../../../../papers/paper_d7967e22bb965daa/documents/main.pdf)
- [SI](../../../../../papers/paper_d7967e22bb965daa/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

四个68原子 quartet TS 与 SI 全坐标匹配；另给INT2A/B作local references。目标虽然已有“四个给定候选比较”的文字，但候选就是作者求得TS终态，按本benchmark禁止向agent给待求TS的边界不能直接发布；不得靠加 starting 注释洗掉。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

20条已归档成功阶段覆盖六物种优化/频率和单点、八条IRC。M06L气相Opt/Freq→THF单点，2/3熵修正；A/B以INT2A、C/D以INT2B为零点，10.258029/12.425524/13.190985/12.022525 kcal/mol均符合10.2/12.4/13.2/12.0±1。

每支IRC40步正常到MaxPoints，化学成键方向有专门证据，但不是所有端点已优化成极小值或完整多维机制证明。AR源模式不存在，不补造。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_2/paper_d7967e22bb965daa/report/results.json) 保持只读。

专门核查记录：

- [provenance/final_closure_20260916/FINAL_AUDIT.md](../../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/FINAL_AUDIT.md)
- [provenance/final_closure_20260916/independent_report.json](../../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/independent_report.json)
- [provenance/final_closure_20260916/author_route_evaluation_audit.json](../../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/author_route_evaluation_audit.json)
- [provenance/chemical_mode_projection_20260914.json](../../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/chemical_mode_projection_20260914.json)
- [provenance/IRC_chemical_assignment_20260915/independent_IRC_assignment.json](../../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/IRC_chemical_assignment_20260915/independent_IRC_assignment.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `r_process_ts` → `kp_process_ts_validation` | semantic；真实证据/适用边界见第 3 节 | `$.candidates[].frequency_validation` |
| `r_process_ref` → `kp_process_reference` | semantic；真实证据/适用边界见第 3 节 | `$.reference_convention.reference_state` / `$.reference_convention.energy_expression` |
| `r_barrier_a` → `kp_result_fourway` | 10.25802915；参考 10.2 ± 1 kcal/mol；算术通过 | `$.comparison.barrier_values.TS3A-quartet` |
| `r_barrier_b` → `kp_result_fourway` | 12.42552426；参考 12.4 ± 1 kcal/mol；算术通过 | `$.comparison.barrier_values.TS3B-quartet` |
| `r_barrier_c` → `kp_result_fourway` | 13.19098542；参考 13.2 ± 1 kcal/mol；算术通过 | `$.comparison.barrier_values.TS3C-quartet` |
| `r_barrier_d` → `kp_result_fourway` | 12.02252513；参考 12 ± 1 kcal/mol；算术通过 | `$.comparison.barrier_values.TS3D-quartet` |
| `r_order` → `kp_result_order` | semantic；真实证据/适用边界见第 3 节 | `$.comparison.ordering` |
| `r_final` → `c_final_selectivity` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |
| `r_limits` → `c_limitations` | semantic；真实证据/适用边界见第 3 节 | `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

仅PR hold。建议负责人明确是否改为保留四候选机理标签/原子映射而去掉TS答案，让agent自建TS，INT2参考保留与否按目标另定；科学目标/交付边界变化需确认。若另开给定TS能量基准应独立命名，不并入本发现评估。

前轮建议去向（迁移已撤回）：`tasks/hold_verified_paper_reproduction/paper_d7967e22bb965daa`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

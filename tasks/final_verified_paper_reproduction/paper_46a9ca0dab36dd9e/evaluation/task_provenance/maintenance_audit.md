# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_46a9ca0dab36dd9e`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

明确隐式 MeCN、最高 f 选态和三片段 Mulliken-like IFCT。SI S34–S35 最高 f 原则在现有 TD30 输出选择 state20；既有 state20 IFCT 63.541/3.820% 可供核查，不把 state22 历史输出改名。布居口径为负责人批准的 benchmark 约定，不冒称原文唯一规定。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：Cat1 六重态 TD / IFCT

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_46a9ca0dab36dd9e`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的目标激发态、溶剂和 IFCT 定义没有与单值评分充分对齐。

复审摘要：正确离子对已算LMCT；任择激发态/分区却要求62.4/4.3%，MeCN边界也不清。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_46a9ca0dab36dd9e)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_46a9ca0dab36dd9e`；group：`group_4`；模式：`paper_reproduction`。

结论：**HOLD，暂不用于正式评估**。溶剂边界与真实 SMD(MeCN) 路线存在歧义，代表激发态/IFCT 比较协议未唯一界定。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI PDF p34–35 的态/IFCT资料，p37计算条件；正文的62.4% LMCT /4.3% MLCT来自特定所选态与分析口径。

- [正文](../../../../../papers/paper_46a9ca0dab36dd9e/documents/main.pdf)
- [SI](../../../../../papers/paper_46a9ca0dab36dd9e/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

TEA+·FeCl4−共34原子，总charge0/sextet，身份自包含、无作者XYZ。AR说 excluding solvent，PR只说没有溶剂分子；实际验证SMD(MeCN)，不能把这处歧义仅凭措辞断定允许相同溶剂。允许任意合理低激发态/fragment partition但打单一百分比目标。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

ground-state96实频、TD30；历史选择state22（非最大f，最亮为state20）。state22 Hirshfeld LMCT62.060/MLCT4.103%；Mulliken-like62.492/4.351%；state20/21对照也有真实输出。支持作者所选态的LMCT结论，不能证明任选态都应满足同一gold。

片段必须区分Cl、Fe、TEA+；把整个FeCl4作为一个片段会改变LMCT意义。公开task允许自定义分区和状态，但evaluator强比62.4/4.3。state22是方法相关序号，不能直接公开并要求所有方法都取22。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/report/results.json) 保持只读。

专门核查记录：

- [provenance/ifct_closure_20260915.json](../../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/ifct_closure_20260915.json)
- [provenance/evaluation_task_qualification.json](../../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/evaluation_task_qualification.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `pr_r_system` → `pr_process_system` | semantic；真实证据/适用边界见第 3 节 | `$.system.charge` / `$.system.multiplicity` / `$.system.geometry_source` |
| `pr_r_states` → `pr_process_states` | semantic；真实证据/适用边界见第 3 节 | `$.state_selection.states_examined` / `$.state_selection.state_id` / `$.state_selection.rationale` / `$.state_selection.states[].state_id` |
| `pr_r_ifct` → `pr_process_ifct` | semantic；真实证据/适用边界见第 3 节 | `$.validation.fragment_definition` / `$.validation.sensitivity_check` / `$.ifct_records[].state_id` / `$.ifct_records[].fragment_definition` |
| `pr_r_lmct` → `pr_result_lmct` | 62.06；参考 62.4 ± 10 percent；算术通过 | `$.ifct.lmct_percent` |
| `pr_r_mlct` → `pr_result_mlct` | 4.103；参考 4.3 ± 5 percent；算术通过 | `$.ifct.mlct_percent` |
| `pr_r_final` → `pr_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` / `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式hold。建议确认MeCN连续介质为公共边界并保留无显式溶剂；按论文定义待比较的谱带/态性质、Cl→Fe与Fe→Cl及归一化/分区，PR可给主协议；AR保留选择自由时需批准方法/态匹配的评分分支。先明确协议，不自动重算。

前轮建议去向（迁移已撤回）：`tasks/hold_verified_paper_reproduction/paper_46a9ca0dab36dd9e`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_746e066c163800d8`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

compound5.xyz 已替换为完整拓扑独立嵌入、未优化起点；原坐标留 evaluation/author_results/compound5.xyz。公开身份文件保存原子映射/配位，生成未使用作者终态坐标约束或目标参数，未新增量化验证。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：compound 5 螺烯内缘扭转

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_746e066c163800d8`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 均有待求几何答案泄露，另有二面角正负约定与失败分支问题。

复审摘要：72 原子作者优化终态公开；signed/absolute 与正值 gold 不一致；失败 schema 强制虚频数。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_746e066c163800d8)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_746e066c163800d8`；group：`group_1`；模式：`paper_reproduction`。

结论：**HOLD，暂不用于正式评估**。公开作者优化坐标直接包含所评分的内缘扭转答案；有符号/绝对均值口径还需决定。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF/印刷 p4 给出实验约 27.0° 和优化结构讨论；SI PDF p45–46 为 compound 5 优化坐标。

- [正文](../../../../../papers/paper_746e066c163800d8/documents/main.pdf)
- [SI](../../../../../papers/paper_746e066c163800d8/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

72 原子 compound5.xyz 全部坐标匹配 SI。待求量恰是优化螺烯的五个内缘扭转，直接测量作者输入几何即可接近 27.1°；这是两模式共同的答案结构泄露，不是合法给定结构性质例外。实验参照 27.0° 本身可公开；已纠正其来源页码 6→4。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

作者路线优化/频率 210 实频，实际平均扭转 27.09676855°；紧收敛复核 27.09673780°。这些确实支持论文结果，但不能授权公开其终态。

任务允许 signed 或 absolute dihedral 平均，数值规则却直接与正 27.1 比较；相反手性/原子顺序下的负号不能被误判为结构错误。修这一口径涉及允许答案集合，待确认。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_746e066c163800d8/report/results.json) 保持只读。

专门核查记录：

- [provenance/inner_rim_closure_audit_20260915.json](../../../../../docs/verification/group_1/paper_746e066c163800d8/provenance/inner_rim_closure_audit_20260915.json)
- [artifacts/inner_rim_complete_20260915.json](../../../../../docs/verification/group_1/paper_746e066c163800d8/artifacts/inner_rim_complete_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `pr_r1` → `pr_process_minimum` | semantic；真实证据/适用边界见第 3 节 | `$.validation.minimum_test` / `$.validation.imaginary_modes` |
| `pr_r2` → `pr_process_torsion_trace` | semantic；真实证据/适用边界见第 3 节 | `$.torsions` |
| `pr_r3` → `pr_result_mean` | 27.09676855；参考 27.1 ± 2 degree；算术通过 | `$.mean_torsion_deg` |
| `pr_r4` → `pr_final` | semantic；真实证据/适用边界见第 3 节 | `$.interpretation` / `$.limitations` |
| `pr_r5` → `pr_result_calibration` | semantic；真实证据/适用边界见第 3 节 | `$.interpretation` / `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/data/inputs/experimental_torsion_boundary.json`：核对正文 PDF p4，实验校准来源页码6→4；不改27.0实测值。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式 hold。建议批准后由独立分子图/连接性生成同身份初始几何，作者终态移 evaluation/author_results；保留映射且不使用作者坐标作模板。另确认评分采用五个扭转绝对值的平均，或签名/手性等价规则。无需因更换 starter 自动重算历史作者路线。

前轮建议去向（迁移已撤回）：`tasks/hold_verified_paper_reproduction/paper_746e066c163800d8`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 已同步五角平均绝对值、完整图/原子映射、实验比较移交 evaluator；失败允许未知频率 null，成功必须有真实频率或等效最小值证据。实验边界文件从公开侧移入 author_results，可恢复；原数值/容差不变。

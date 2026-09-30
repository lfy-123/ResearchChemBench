# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_b33676a2051f5e91`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

保留既有 PR 作者待检验 β-scission 路线和原势垒；核对同支原子/能量零点，不扩充通道或重算。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：Int-3 β-scission TS / IRC

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_b33676a2051f5e91`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

PR 指定断裂通道有真实支持；AR 的9.07数值适用条件需要明确绑定到正确通道。

复审摘要：反应物输入合法；TS/IRC支持指定通道；AR 条件仅写validated_result，未显式限制数值的通道。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_b33676a2051f5e91)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_b33676a2051f5e91`；group：`group_4`；模式：`paper_reproduction`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p8 Int-3 β-scission势垒9.07及比较13.39；SI PDF p23作者方法、p33反应物坐标。

- [正文](../../../../../papers/paper_b33676a2051f5e91/documents/main.pdf)
- [SI](../../../../../papers/paper_b33676a2051f5e91/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

24原子中性doublet Int-3 只公开反应物；TS、产品坐标与势垒均不公开。AR保持自行提出/辨别通道，PR仅给待检验的acetophenone+ethyl路线假设；格式整理后补全“that channel”指代，没有把TS答案写入输入。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

BHandHLYP/aug-cc-pVDZ/SMD(MeCN)真实reactant 66实频，TS一虚频−474.9764 cm⁻¹，ΔG‡8.89745683 kcal/mol符合9.07±2。正向IRC64点回到Int-3；反向80点到MaxPoints，C12–C13=3.658492 Å、C12=O24=1.213425 Å，片段图acetophenone/ethyl，ethyl自旋和0.998047。证据足以支持指定断裂通道，不冒称无限远解离收敛。

三候选是同一通道的两个拉伸guess及QST2，不是三条独立机理；没有完整竞争通道排序或产物minimum频率验证。当前完成条件是至少一个验证通道，历史作者路线支持该科学结论；不能宣传AR盲测/全局最优选择已验证。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_4/paper_b33676a2051f5e91/report/results.json) 保持只读。

专门核查记录：

- [provenance/author_channel_closure_20260915.json](../../../../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/author_channel_closure_20260915.json)
- [provenance/evaluation_task_qualification.json](../../../../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/evaluation_task_qualification.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `pr_r1` → `pr_process_freq` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion.frequency_validation` |
| `pr_r2` → `pr_process_connection` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion.connection_validation` |
| `pr_r3` → `pr_result_barrier` | 8.897456833；参考 9.07 ± 2 kcal/mol；算术通过 | `$.conclusion.barrier_kcal_mol` |
| `pr_r4` → `pr_result_identity` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion.channel` |
| `pr_r5` → `pr_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` / `$.failure` |

历史正式 results.json 直接通过当前 result_schema 检查。

成功分支没有填充 `$.failure`；这些只用于失败/局限分支，不当作缺少科学结果。其余绑定均能在真实结果/私有等价映射中定位。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：澄清既有给定结构角色/公开来源，或补全格式拆分后的主语；不改变目标、方法或评分。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final。AR私有结果映射仅把现有conclusion包装为一条channels，明确作者定向选择；无新增科学数值、无补算。

前轮建议去向（迁移已撤回）：`tasks/final_verified_paper_reproduction/paper_b33676a2051f5e91`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

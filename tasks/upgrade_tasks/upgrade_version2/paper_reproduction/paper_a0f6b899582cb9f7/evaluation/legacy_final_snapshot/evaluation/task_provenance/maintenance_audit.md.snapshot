# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_a0f6b899582cb9f7`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

定向复核 raw 核+电子电荷二阶矩、完整张量、原点、DÅ 及拟合面法向；不替换为 traceless。既有 66 实频和 -111.07681064 DÅ 证据限于孤立 M3，不升级器件结论。现有定义无需改变。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：M3 身份、几何与多极矩

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_a0f6b899582cb9f7`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 未发现新的直接泄露或必需数据缺失；前轮张量定义修复需由你验收。

复审摘要：独立 M3 starter；原始二阶矩/轴/单位已有明确约定；现有三极小值支持目标。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_a0f6b899582cb9f7)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_a0f6b899582cb9f7`；group：`group_1`；模式：`paper_reproduction`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 M3 定义及 N···S/平面性讨论；SI PDF p7 Table S1，M3 三个对角元 −83.67/−103.14/−108.35。表头 Debye 对二阶矩量纲不完整，且非零迹说明不能套 traceless 张量。

- [正文](../../../../../papers/paper_a0f6b899582cb9f7/documents/main.pdf)
- [SI](../../../../../papers/paper_a0f6b899582cb9f7/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

24 原子 C12H8N2S2，2,5-di(thiophen-2-yl)pyrazine；公开几何是按正确图 ETKDG/MMFF、固定种子构建，不匹配 SI 坐标。无目标多极矩或最优几何答案。已明确 Qij=ΣZARAiRAj−∫ρrirj、核+电子、声明原点、Debye Å 及分子面法向，不把任意输入实验室 z 当 stacking 方向。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

三个真实优化极小值，66 实频；选定结构 dipole=0 D、平面 RMS 0.00025046 Å、N···S=2.99065 Å，旋转后的原始张量 Qzz=−111.07681064 DÅ，处于 −108.35±5 既有范围。不是 traceless 或乘三的另一 convention。

此处修的是原已采用物理量的定义/单位说明，与 private paper_route 已有说明一致，不缩放数值、不换参考、不放宽容差。孤立分子二阶矩不能证明器件性能或固体结合能。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/report/results.json) 保持只读。

专门核查记录：

- [provenance/correct_m3_closure_20260915.json](../../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/correct_m3_closure_20260915.json)
- [artifacts/correct_identity_multipoles_20260915.json](../../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/artifacts/correct_identity_multipoles_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `pr_rule_process_opt` → `pr_process_optimization` | semantic；真实证据/适用边界见第 3 节 | `$.validation` |
| `pr_rule_process_struct` → `pr_process_structure` | semantic；真实证据/适用边界见第 3 节 | `$.method.axis_convention` / `$.observables.planarity_rms_angstrom` / `$.observables.ns_distance_angstrom` |
| `pr_rule_qzz` → `pr_result_tensor` | -111.0768106；参考 -108.35 ± 5 Debye angstrom；算术通过 | `$.observables.qzz_stacking_debye_angstrom` |
| `pr_rule_dipole` → `pr_result_dipole` | semantic；真实证据/适用边界见第 3 节 | `$.observables.dipole_debye` / `$.conclusion` |
| `pr_rule_final` → `pr_final_conclusion` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：SI Table S1三对角元非零迹，真实计算raw张量；澄清既有raw二阶矩及DÅ单位，不改数值目标、容差或方法自由度。
- `evaluation/reference_key_points.json`：统一原单位标注和raw张量口径；保留gold及容差。
- `agent_input/submission_schema.json`：为原张量字段补充单位/定义描述，不增必填项。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final；保留方法/原点/全张量变换证据，未要求新计算。

前轮建议去向（迁移已撤回）：`tasks/final_verified_paper_reproduction/paper_a0f6b899582cb9f7`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

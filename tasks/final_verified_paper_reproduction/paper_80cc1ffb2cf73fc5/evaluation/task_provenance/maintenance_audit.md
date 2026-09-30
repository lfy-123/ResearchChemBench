# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

保留获准的 Z1 anion；从 SI Fig S1 的独立黑色实验向量路径提取 825 个窗口顶点，排除蓝色拟合、红色背景和理论曲线，不用理论结果制造实验峰。按坐标刻度还原，保留重复x及噪声，非原始探测数据。公开相对零点与比较规则，无作者计算移位；未新增量化计算。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：Z1 Franck–Condon 谱与模式归属

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_80cc1ffb2cf73fc5`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的 FC 和模式计算成立；实验比较的输入/职责未闭合，PR 还有允许质疑与强制支持的评分冲突。

复审摘要：只有实验窗口，没有峰表/trace；PR mode 条款允许质疑，final 条款却强制肯定解释。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_80cc1ffb2cf73fc5)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_80cc1ffb2cf73fc5`；group：`group_1`；模式：`paper_reproduction`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI PDF p6 的 Z1 anion 坐标与正文 FC 解释；实验窗口/电子脱附背景与任务 problem_definition 一致。

- [正文](../../../../../papers/paper_80cc1ffb2cf73fc5/documents/main.pdf)
- [SI](../../../../../papers/paper_80cc1ffb2cf73fc5/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

27 原子 singlet anion 是已给定初态，全部匹配 SI；并非同时把待求 neutral radical、FC 模式、HR 因子或谱强度给出。charge −1/singlet→0/doublet，同核连接性明确。窗口公开，但无实验逐点 trace；task/schema 明确无观测时不编造 MAE。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

anion/neutral 各 75 实频，FC 四个实际成功段及模式后处理完整；scale 0.9566、T=6 K、HWHM=2 cm⁻¹、grid=1 cm⁻¹ 的历史谱，主导面内 mode 3：85.9573 cm⁻¹、HR 1.20932，约占选定强度 99.63%。上述设置只在 private reference 记录，不强迫 AR 路线。

无逐点实测 trace 就不能声称数值拟合误差已验证；当前 evaluator/scoring 接受带该限制的 FC 机理/模式解释，未补造实验数据。只纳入明确成功的 FC 日志段，不纳入失败尾段。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/report/results.json) 保持只读。

专门核查记录：

- [provenance/fc_closure_audit_20260914.json](../../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/fc_closure_audit_20260914.json)
- [artifacts/fc_closure_20260914/fc_analysis.json](../../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/fc_analysis.json)
- [artifacts/fc_closure_20260914/modes_full.json](../../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/modes_full.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `pr_r_min` → `pr_kp_process_minimum` | semantic；真实证据/适用边界见第 3 节 | `$.structures` / `$.validation` |
| `pr_r_fc` → `pr_kp_process_fc` | semantic；真实证据/适用边界见第 3 节 | `$.calculation` / `$.peaks` / `$.comparison.origin_alignment` |
| `pr_r_mode` → `pr_kp_result_mode` | semantic；真实证据/适用边界见第 3 节 | `$.modes` / `$.conclusion` |
| `pr_r_limit` → `pr_kp_result_limit` | semantic；真实证据/适用边界见第 3 节 | `$.limitations` / `$.conclusion` |
| `pr_r_final` → `pr_c_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：澄清既有给定结构角色/公开来源，或补全格式拆分后的主语；不改变目标、方法或评分。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final，维持给定初态→未知中性态/振动响应范围；不称从无结构输入独立发现全部端点。

前轮建议去向（迁移已撤回）：`tasks/final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 按已批准边界保留 source-optimized 给定对象/初态；统一 XYZ 注释和 task_info，不称其为独立生成或待发现几何。待求性质/中间关键点仍由 agent 计算，未公开结果或排名。

- 完成存量 FC 与新增纯实验曲线的相对对齐后处理；全部窗口内已存跃迁均列出，未匹配强峰/强度差异保留。支持获准的突出特征/物理进动有限结论，不把 Z1-only 写成全谱或绝对脱附能验证。

# 当前状态：经负责人授权移入 hold

2026-09-16 再复核：67份篇内历史几何和2份队列起点均不匹配正确7a，独立重原子图检查也失败。已完成的输入修复保留，但不能仅靠改标签、改映射或重算误差表补齐正确对象的验证证据。未新增计算。下方 verified_tasks 状态为移入 hold 前的历史。

---

# 当前实施状态

## 已批准修复记录（2026-09-16）

已按正文 p4/SI S1–S3 修正 pyrazole 取代图、重建标签到图原子的映射；Cl1/Cl2 为 C14 上同一氯的来源别名。补纯实验47行及原文括号不确定度，删除公开侧要求对隐藏值算误差的矛盾；PR 明确方法对。旧错对象链暂不能认证修正后任务，整体优劣仍不造跨单位权重。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：compound 7a 两种泛函几何

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_a3968806251093cd`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 当前分子图与论文对象不一致；现有验证不能认证正确 7a。另有缺实验数据/映射及方法比较问题。

复审摘要：7a 位置异构体算错；隐藏实验列却要求 MAE；标签映射、方法胜负与失败 schema 未对齐。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_a3968806251093cd)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_a3968806251093cd`；group：`group_2`；模式：`paper_reproduction`。

结论：**HOLD，暂不用于正式评估**。分子连接关系与论文不一致，且公开实验比较数据/映射缺失；历史运行成功不能证明当前论文对象已验证。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p4 / Fig. 3：pyrazole N1–N2–C9–C8–C7，N1 连 phenyl，C7 连 O1-chlorophenyl ether，C8 接 imine，C9 接 methyl；SI 几何比较表与此标签体系对应。

- [正文](../../../../../papers/paper_a3968806251093cd/documents/main.pdf)
- [SI](../../../../../papers/paper_a3968806251093cd/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

当前 SMILES 名称写 5-phenoxy/4-methylene，但图把这两处取代位置交换。RDKit graph：N1=4 邻接 C11（历史映射 C8），O1=22 接 C21（历史映射 C7），N1 不邻接该 O-bearing 碳。分子式 C20H17ClN6OS 和 46 原子正确不能排除位置异构体错误。atom_map 只列测量标签组合，无真实标签到图映射。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

两条 B3LYP/CAM-B3LYP Opt/Freq 确实成功，各 132 实频，但同为上述错误图。B3LYP 末态 N1–C7=2.196492 Å，N1–C8=1.376571 Å，O1–C7=1.368864 Å。CAM 和现存生成 SDF/7a_repaired.xyz 同样错误。原几何 MAE 包含不应作键角的非键合三元组，无法证明正确论文 7a 的结论。

此外：①task 要求 agent 对 withheld SCXRD 计算 MAE/RMSE，却未给实验列；②PR 允许任意 conventional/range-separated pair，却强制 CAM-B3LYP 胜 B3LYP；③历史48条/方法含重复角，公开去重表47条/方法。schema 能通过不代表科学身份/实验比较有效。reference 已撤回旧“身份及完整比較通过”，保留真实历史日志与数值并标明不适用。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_2/paper_a3968806251093cd/report/results.json) 保持只读。

专门核查记录：

- [provenance/author_route_evaluation_audit.json](../../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/author_route_evaluation_audit.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `pr_r1` → `pr_process_identity` | semantic；真实证据/适用边界见第 3 节 | `$.mapping.label_to_atom` / `$.mapping.mapping_basis` |
| `pr_r2` → `pr_process_stationary` | semantic；真实证据/适用边界见第 3 节 | `$.models[]` |
| `pr_r3` → `pr_result_geometry` | semantic；真实证据/适用边界见第 3 节 | `$.observables[]` / `$.metrics[]` |
| `pr_r4` → `pr_result_model` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` / `$.metrics[]` |
| `pr_r5` → `pr_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |
| `pr_r6` → `pr_limit` | semantic；真实证据/适用边界见第 3 节 | `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。 已明确撤回错误对象的科学通过表述。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式 hold。先请负责人确认依据正文/SI 修正连接图和完整标签映射；再决定公开仅实验观测列让 agent 比较，还是将比较完全交 evaluator，并同步评分。PR 若按原文比较 B3LYP/CAM，应明确方法范围；AR 不预埋作者胜负。先查是否有正确图的已有结果；当前检查的作者级链及生成结构未找到。不能把旧 PASS 复用为新正确分子验证，不擅自重算。

前轮建议去向（迁移已撤回）：`tasks/hold_verified_paper_reproduction/paper_a3968806251093cd`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 已扩大检索至包含被 Git 忽略的历史日志/输入：67 份有几何记录，正确对象匹配 0 份。当前正确对象验证缺口不能靠修改 reference/名称消除；未更改 group 或发起重算。

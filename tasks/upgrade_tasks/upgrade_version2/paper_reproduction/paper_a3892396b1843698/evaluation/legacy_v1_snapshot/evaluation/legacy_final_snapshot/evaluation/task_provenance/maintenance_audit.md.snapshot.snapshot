# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_a3892396b1843698`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

定向复核公开 3a 为反应物、两指定 [3,3]/[5,5] TS/IRC 支路与局部热化学基准。历史 GoodVibes entropy-only Grimme qRRHO（无 Head-Gordon 焓修正）及两势垒保留；未加入未知通道/端点要求。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：3a [3,3] / [5,5] 重排势垒

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_a3892396b1843698`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 当前 TS 子问题的身份、公开输入和作者路线证据一致；未发现新的实质性缺口。

复审摘要：只公开反应物 3a，不公开 TS/产品；两通道 TS/IRC/端点链完整。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_a3892396b1843698)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_a3892396b1843698`；group：`group_2`；模式：`paper_reproduction`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p4 的 [3,3]/[5,5] 势垒；SI PDF p6 热化学、p11 反应物 3a 坐标。

- [正文](../../../../../papers/paper_a3892396b1843698/documents/main.pdf)
- [SI](../../../../../papers/paper_a3892396b1843698/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

唯一公开几何是中性 singlet 25 原子反应物 3a；没有 TS 或产品终态。公开反应物是反应问题的必要对象，不能与直接提供待求 TS 混为一谈。两个待比较 shift 通道是当前任务范围。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

ωB97XD/def2SVP Opt/Freq→def2TZVPP 单点及一致的 entropy-only Grimme qRRHO；两个 TS 各一虚频，双向 IRC 和四个后续端点极小值闭合。ΔG‡为 23.50589160、26.22790785 kcal/mol，分别符合 23.5/26.2±3。构型/通道映射支持势垒顺序。

验证者使用作者路线/TS 可以证明此子问题能算出 evaluator 结论；不等价于某模型已从公开反应物独立找到 TS。没有因此要求新 public-start replay。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_2/paper_a3892396b1843698/report/results.json) 保持只读。

专门核查记录：

- [AUTHOR_ROUTE_FINAL_AUDIT_20260914.md](../../../../../docs/verification/group_2/paper_a3892396b1843698/AUTHOR_ROUTE_FINAL_AUDIT_20260914.md)
- [provenance/author_route_evaluation_audit.json](../../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/author_route_evaluation_audit.json)
- [provenance/independent_author_route_numeric_20260914.json](../../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/independent_author_route_numeric_20260914.json)
- [provenance/endpoint_minima_audit_20260914.json](../../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/endpoint_minima_audit_20260914.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `r_pr_kp_ts` → `kp_pr_process_ts` | semantic；真实证据/适用边界见第 3 节 | `$.channels.shift_33.validation` / `$.channels.shift_55.validation` |
| `r_pr_kp_ref` → `kp_pr_process_reference` | semantic；真实证据/适用边界见第 3 节 | `$.method.reference_state` / `$.method.thermochemistry` |
| `r_pr_barrier_33` → `kp_pr_result_barriers` | 23.5058916；参考 23.5 ± 3 kcal/mol；算术通过 | `$.channels.shift_33.barrier_kcal_mol` |
| `r_pr_barrier_55` → `kp_pr_result_barriers` | 26.22790785；参考 26.2 ± 3 kcal/mol；算术通过 | `$.channels.shift_55.barrier_kcal_mol` |
| `r_pr_order` → `kp_pr_result_comparison` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |
| `r_pr_final` → `c_pr_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final；当前可用于 TS 搜索测试的本批候选之一，但实际执行需只暴露 agent_input。

前轮建议去向（迁移已撤回）：`tasks/final_verified_paper_reproduction/paper_a3892396b1843698`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

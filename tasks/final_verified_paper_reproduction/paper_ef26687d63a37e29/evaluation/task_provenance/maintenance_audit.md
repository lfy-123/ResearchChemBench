# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_ef26687d63a37e29`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

接触选择定义澄清（负责人本轮批准）：AR/PR 的主 O 均固定为输入 atom-map 49（PO 链端 O；PA 图中 C48=O49），P=46；从各自已优化几何的完整 N-ethyl alpha/beta H 集合分别取最近 H，同一 O 用于三个主接触，精确并列时用最小输入 map ID。其他 O/H 只作辅助，不按 gold 选 O/H；接触 H 电荷取相同被选 H，全部 H 电荷保留。同步 task/schema、关键点、评分比较和 task_info，无新增强制 AR scalar summary，无答案数字/几何加入公开输入；主数值、容差、权重不变。旧几何后处理复核六接触与历史结果一致，未新增量化计算。

Et2N3P.xyz 已替换为完整拓扑独立嵌入、未优化起点；原坐标留 evaluation/author_results/Et2N3P.xyz。公开身份文件保存原子映射/配位，生成未使用作者终态坐标约束或目标参数，未新增量化验证。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：free / PO / PA 接触、电荷与 ESP

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_ef26687d63a37e29`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 仍使用作者优化几何；前轮补齐身份并没有消除答案信息。

复审摘要：46/56/61 原子模型验证有效，但作者终态及 PA 的部分终态仍在公开输入。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_ef26687d63a37e29)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_ef26687d63a37e29`；group：`group_1`；模式：`paper_reproduction`。

结论：**HOLD，暂不用于正式评估**。已纠正截断坐标，但公开作者终态仍直接包含所评分接触距离；独立 starter 修法待批准。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 Fig. 6（PDF p8，相关解释 p10）；SI PDF p35–40 的 free/PO/PA 优化坐标及接触量。

- [正文](../../../../../papers/paper_ef26687d63a37e29/documents/main.pdf)
- [SI](../../../../../papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

确认 AR 的 free 原为 22 原子 C6H13N3，PO 原为 29 原子 C8H18N3，均缺 P，后者还缺 O；与已声明物种不符。本轮从 PR/SI 唯一完整转录补齐至 46 原子 C12H30N3P、56 原子 C15H36N3OP；PA 保持 61 原子 C20H34N3O3P。身份缺损已修，但 free/PO 全部作者坐标、PA 的 51/61 作者坐标仍含接触几何答案；补芳环不使整体独立。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

完整正确 46/56/61 原子模型已有真实极小值验证；P 的 ADCH 电荷 −0.018993/0.447060/0.455684 e，PO/PA 六个 O···P/H 接触均通过现有 ±0.25 Å，MEP 链可追溯。旧截断模型不是本次采纳的科学证据。

原公共 provenance/任务文字的“不含作者优化结果”不真实；已改任务说明，并将维护 JSON 移入 evaluation/task_provenance。历史 JSON 中的旧判断只作维护历史，不能作为无泄露证明。坐标泄露仍未解除，不能因为所有数值吻合就发布。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_ef26687d63a37e29/report/results.json) 保持只读。

专门核查记录：

- [provenance/complete_pa_closure_20260915.json](../../../../../docs/verification/group_1/paper_ef26687d63a37e29/provenance/complete_pa_closure_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `r_pr_minima` → `kp_pr_process_minima` | semantic；真实证据/适用边界见第 3 节 | `$.species[*].imaginary_frequency_count` / `$.species[*].structure_file` / `$.species[*].status` |
| `r_pr_mapping` → `kp_pr_process_mapping` | semantic；真实证据/适用边界见第 3 节 | `$.species[*].distances[*].atom_indices` / `$.method.mapping_notes` |
| `r_pr_mep` → `kp_pr_mep` | semantic；真实证据/适用边界见第 3 节 | `$.species[*].mep_observation` |
| `r_pr_final` → `con_pr_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion.mechanistic_claim` / `$.conclusion.supporting_observations` |
| `r_pr_limits` → `con_pr_limits` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion.alternative_or_scope` / `$.limitations` |
| `r_pr_po_OP` → `kp_pr_distances` | 1.829262；参考 1.828 ± 0.25 angstrom；算术通过 | `$.contact_summary.PO.O_P_A` |
| `r_pr_po_OalphaH` → `kp_pr_distances` | 2.125092709；参考 2.124 ± 0.25 angstrom；算术通过 | `$.contact_summary.PO.O_alphaH_A` |
| `r_pr_po_ObetaH` → `kp_pr_distances` | 2.440469877；参考 2.437 ± 0.25 angstrom；算术通过 | `$.contact_summary.PO.O_betaH_A` |
| `r_pr_pa_OP` → `kp_pr_distances` | 2.65221031；参考 2.651 ± 0.25 angstrom；算术通过 | `$.contact_summary.PA.O_P_A` |
| `r_pr_pa_OalphaH` → `kp_pr_distances` | 2.311797025；参考 2.312 ± 0.25 angstrom；算术通过 | `$.contact_summary.PA.O_alphaH_A` |
| `r_pr_pa_ObetaH` → `kp_pr_distances` | 2.363290557；参考 2.363 ± 0.25 angstrom；算术通过 | `$.contact_summary.PA.O_betaH_A` |
| `r_pr_P_charge_free` → `kp_pr_charge` | -0.018993；参考 -0.018 ± 0.03 e；算术通过 | `$.charge_summary.free.P_e` |
| `r_pr_P_charge_PO` → `kp_pr_charge` | 0.44706；参考 0.447 ± 0.03 e；算术通过 | `$.charge_summary.PO.P_e` |
| `r_pr_P_charge_PA` → `kp_pr_charge` | 0.455684；参考 0.455 ± 0.03 e；算术通过 | `$.charge_summary.PA.P_e` |
| `r_pr_H_charge` → `kp_pr_charge` | semantic；真实证据/适用边界见第 3 节 | `$.species[*].charges` / `$.charge_summary` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：纠正“不是作者优化结果”的不实来源说明；保留输入边界待决定。
- `agent_input/data/inputs/structure_provenance.json` → `evaluation/task_provenance/structure_provenance.json`：维护记录私有化；保留原文件，不作为评分输入。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式 hold。建议负责人批准由正确完整分子图独立构建三模型、保留电子态/身份/必要片段定义，作者坐标私有化；不采用小扰动冒充独立构建，不新增评分或私自改科学目标。

前轮建议去向（迁移已撤回）：`tasks/hold_verified_paper_reproduction/paper_ef26687d63a37e29`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- Et2N3P_PO.xyz 已替换为完整拓扑独立嵌入、未优化起点；原坐标留 evaluation/author_results/Et2N3P_PO.xyz。公开身份文件保存原子映射/配位，生成未使用作者终态坐标约束或目标参数，未新增量化验证。

- Et2N3P_PA.xyz 已替换为完整拓扑独立嵌入、未优化起点；原坐标留 evaluation/author_results/Et2N3P_PA.xyz。公开身份文件保存原子映射/配位，生成未使用作者终态坐标约束或目标参数，未新增量化验证。

- 三个完整图/式/电荷和原子映射已核对，公开说明不再声称保留 SI 片段；保留现有接触、ADCH 与 ESP 指标。旧 structure_provenance 已明确标记历史，不再代表当前公开起点。

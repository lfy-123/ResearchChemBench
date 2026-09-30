# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_paper_reproduction/paper_44f9727c4e9a4b6f`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

1H_start.xyz 已替换为完整拓扑独立嵌入、未优化起点；原坐标留 evaluation/author_results/1H_start.xyz。公开身份文件保存原子映射/配位，生成未使用作者终态坐标约束或目标参数，未新增量化验证。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：1H Fe 几何、自旋与 Mössbauer

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`paper_reproduction`。工作目录：`tasks/verified_tasks/paper_reproduction/paper_44f9727c4e9a4b6f`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

仅PR；公开作者1H终态直接暴露Fe–Fe距离，其他计算及必要Mössbauer校准均有支持。

复审摘要：87原子作者终态泄露几何答案；校准常数是必要输入应保留；BS/HS/位移真实成立。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_44f9727c4e9a4b6f)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_44f9727c4e9a4b6f`；group：`group_6`；模式：`paper_reproduction`。

结论：**HOLD，暂不用于正式评估**。公开作者优化结构可直接量得被评分的 Fe–Fe 距离；独立 starter 修法待批准。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI S5–S6的TPSSh/ZORA/校准说明，S32–S33 Table S10的1H优化坐标；Fe–Fe几何和Mössbauer是当前必评。

- [正文](../../../../../papers/paper_44f9727c4e9a4b6f/documents/main.pdf)
- [SI](../../../../../papers/paper_44f9727c4e9a4b6f/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

87原子1H_start.xyz全部匹配SI优化结果，待求Fe···Fe≈3.086 Å可直接测得，构成答案泄露。mossbauer_protocol的A/B/C、grid、basis等是计算密度到位移所需校准定义，不是目标密度/位移，可合法公开于本PR任务。

模式核对：PR 可以给作者定性假设/待比较路线，但不能把已求得的结构/TS、排序或参考值当作指导输入；存在该问题的包已明确 hold，不以数值通过替代隔离修复。

## 3. 历史真实计算支持与限制

正确broken-symmetry极小值零虚频；Fe–Fe3.086431831 Å，E(BS)−E(HS)=−0.026282803515 Eh；SARC/J/DefGrid3的Fe密度经δ=A(ρ0−C)+B得到0.517809/0.523604 mm/s，符合0.52±0.07。

ORCA打印261个笛卡尔频率槽不等于261个物理振动；保留零虚频和真实结构验证口径。AR源不存在，不补造。全数值符合仍不能解除几何答案泄露。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/report/results.json) 保持只读。

专门核查记录：

- [provenance/FE_ROUTE_AND_CLOSURE_20260915.md](../../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/FE_ROUTE_AND_CLOSURE_20260915.md)
- [provenance/corrected_mossbauer_evidence_20260915.json](../../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/corrected_mossbauer_evidence_20260915.json)
- [provenance/evaluator_crosscheck_20260915.json](../../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/evaluator_crosscheck_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `rule_minimum` → `kp_process_minimum` | 0；参考 0 ± 0 imaginary modes；算术通过 | `$.validation.imaginary_frequency_count` |
| `rule_minimum_evidence` → `kp_process_minimum` | semantic；真实证据/适用边界见第 3 节 | `$.status` / `$.failure_report` / `$.artifacts` |
| `rule_distance` → `kp_result_distance` | 3.086431831；参考 3.086 ± 0.08 Å；算术通过 | `$.validation.fe_fe_distance_angstrom` |
| `rule_delta_fe1` → `kp_result_mossbauer` | 0.5178094024；参考 0.52 ± 0.07 mm s−1；算术通过 | `$.mossbauer.Fe1.isomer_shift_mm_per_s` |
| `rule_delta_fe2` → `kp_result_mossbauer` | 0.5236036402；参考 0.52 ± 0.07 mm s−1；算术通过 | `$.mossbauer.Fe2.isomer_shift_mm_per_s` |
| `rule_mossbauer_evidence` → `kp_result_mossbauer` | semantic；真实证据/适用边界见第 3 节 | `$.status` / `$.failure_report` / `$.artifacts` |
| `rule_spin` → `kp_process_spin` | semantic；真实证据/适用边界见第 3 节 | `$.status` / `$.failure_report` / `$.artifacts` |
| `rule_final` → `conclusion_final_assignment` | semantic；真实证据/适用边界见第 3 节 | `$.final_conclusion` / `$.status` / `$.coverage.limitations` / `$.failure_report` |
| `rule_final_spin` → `conclusion_final_spin` | semantic；真实证据/适用边界见第 3 节 | `$.final_conclusion` / `$.status` / `$.failure_report` |

历史正式 results.json 直接通过当前 result_schema 检查。

成功分支没有填充 `$.failure_report`；这些只用于失败/局限分支，不当作缺少科学结果。其余绑定均能在真实结果/私有等价映射中定位。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：澄清既有给定结构角色/公开来源，或补全格式拆分后的主语；不改变目标、方法或评分。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

仅PR hold。建议批准后用正确化学图、氧化态/配体与自旋边界独立构建初始几何，保留公开校准协议，作者终态移author_results；不得简单扰动原坐标。

前轮建议去向（迁移已撤回）：`tasks/hold_verified_paper_reproduction/paper_44f9727c4e9a4b6f`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 补完整 susan/过氧/μ-oxo 配位图及明确原子身份；独立嵌入使用通用配位和排斥边界，不用作者 Fe···Fe 距离。保留 +2 BS singlet、MeCN、HS 和 Mössbauer 协议，不把模型变成闭壳层。

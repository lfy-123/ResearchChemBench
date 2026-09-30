# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_46f6118697c6397c`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

定向复核 SI Table S3 的 3.8436 eV/322.58 nm/f=0.4243 自洽；evidence_map 已记录正文 4.33 eV 冲突，无需换金标。完整 CIF/四 triflate 保留；轨道按物理身份而非程序固定编号，未增加其他化合物的因果对照。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：compound 2 三分支 TD50

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_46f6118697c6397c`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的 compound-2 TD 子问题已获支持；保留 SI 数值与局部解释界限，不扩张为全取代基因果验证。

复审摘要：CIF 自包含，三分支 Opt/Freq+TD50 成立；正文/SI 数值冲突和因果范围需明示。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_46f6118697c6397c)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_46f6118697c6397c`；group：`group_2`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI PDF p18 Table S3 给出 3.8436 eV/322.58 nm/f=0.4243；正文 p4 的 4.33 eV 与其 323 nm 不自洽。当前源 evaluator 本来采用 SI 数值，本轮不择值或改目标。

- [正文](../../../../../papers/paper_46f6118697c6397c/documents/main.pdf)
- [SI](../../../../../papers/paper_46f6118697c6397c/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

自包含实验 CIF CCDC 2512981，不需要 agent 临时访问数据库；完整 68 原子、四个 triflate 是必要分子身份。CIF 无序/对称需正确展开，非作者计算吸收答案。现有物种、溶剂 CH2Cl2 边界充分。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

三条 CIF 派生分支 B1_op2/B2_A_op5/B2_B_op5 均 198 实频，分别 TD50；三条最大 f 均为当次第 5 态。E/f=3.8445/0.4733、3.8138/0.4255、3.8208/0.4292，全部在现行 ±0.15 eV/±0.05 内。代表支 217→222 映射 HOMO−4→LUMO，有轨道性质依据。

reference 原称“按任务约定选择最低激发能分支”过强，已改为历史报告的代表选择；未新增面向 agent 的筛选规则或固定 state 5。数字编号随程序改变，不应当成物理身份。不能声称晶体堆积或全构象空间被验证。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_2/paper_46f6118697c6397c/report/results.json) 保持只读。

专门核查记录：

- [provenance/author_route_evaluation_audit.json](../../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/author_route_evaluation_audit.json)
- [provenance/compound2_cif_preprocessing.json](../../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/compound2_cif_preprocessing.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `ar_r_identity` → `ar_kp_process_identity` | semantic；真实证据/适用边界见第 3 节 | `$.identity` |
| `ar_r_validation` → `ar_kp_process_validation` | semantic；真实证据/适用边界见第 3 节 | `$.validation` |
| `ar_r_energy` → `ar_kp_result_energy` | 3.8138；参考 3.8436 ± 0.15 eV；算术通过 | `$.result.excitation_energy_eV` |
| `ar_r_osc` → `ar_kp_result_osc` | 0.4255；参考 0.4243 ± 0.05 dimensionless；算术通过 | `$.result.oscillator_strength` |
| `ar_r_character` → `ar_kp_result_character` | semantic；真实证据/适用边界见第 3 节 | `$.result.conclusion` |
| `ar_r_final` → `ar_c_final` | semantic；真实证据/适用边界见第 3 节 | `$.result.conclusion` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。 已将历史代表分支选择与当前公开要求分开。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final；保留 SI 作为当前既有评分来源并注明正文印刷冲突，未按本地值修改标准。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_46f6118697c6397c`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

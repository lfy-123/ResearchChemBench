# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_e31cc7bc7b21b610`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

已确认两给定 cis 异构体；私有规则联合核对数值、符号、两绝对电子能和能序，不将答案能序加入公开输入，未改原容差。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：egan-IrCl cis-α / cis-β 相对能

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_e31cc7bc7b21b610`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的电子能比较可计算；有数值容差与排序的一致性风险，给定终态边界待验收。

复审摘要：各 168 实频，ΔE=1.43848；1.44±1.5 允许负值，需显式与能序联合判定。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_e31cc7bc7b21b610)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_e31cc7bc7b21b610`；group：`group_1`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI PDF p24–27 的 cis-α/cis-β egan-IrCl 完整优化坐标；原文电子能比较（1.44 kcal/mol）。

- [正文](../../../../../papers/paper_e31cc7bc7b21b610/documents/main.pdf)
- [SI](../../../../../papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

两结构各 58 原子、charge 0/singlet；元素/补氢问题在既有成功验证前已纠正，并核对 SI。当前原始目标就是给定两异构体的电子能比较，不是结构/异构体发现。明示 source-optimized 给定对象，未公开能序或差值；将补氢/元素维修历史 JSON 移到 task_provenance。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

Gaussian B3LYP、Ir SDD/其余 6-31G(d)，气相两条 Opt/Freq 均 168 实频；Eα=−2204.52499151、Eβ=−2204.52269915 Eh，(Eβ−Eα)×627.5094740631=1.43847762 kcal/mol，满足现行 1.44±1.5。

支持气相电子稳定性，不是自由能、互变势垒、速率或溶液平衡。历史作者结构公开是既有给定性质任务范围，不将其重新宣称自主几何生成。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/report/results.json) 保持只读。

专门核查记录：

- [provenance/correct_identity_closure_20260915.json](../../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/correct_identity_closure_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `r_ar_alpha_process` → `kp_ar_process_alpha` | semantic；真实证据/适用边界见第 3 节 | `$.isomers.cis_alpha` |
| `r_ar_beta_process` → `kp_ar_process_beta` | semantic；真实证据/适用边界见第 3 节 | `$.isomers.cis_beta` |
| `r_ar_energy` → `kp_ar_result_energy` | 1.438477618；参考 1.44 ± 1.5 kcal/mol；算术通过 | `$.relative_energy.value` |
| `r_ar_conclusion` → `con_ar_final` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` / `$.limitations` |

历史正式 results.json 不能直接符合当前 AR schema；已在私有 [historical_result_schema_mapping.json](historical_result_schema_mapping.json) 中作无损字段适配，映射后的 schema 检查通过。新增文字仅说明既有覆盖/选择限制，未伪造新搜索或结果。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：移出维护历史引用，明确既有固定异构体相对电子能任务范围；不改对象或评分。
- `agent_input/data/inputs/structure_provenance.json` → `evaluation/task_provenance/structure_provenance.json`：维护记录私有化；保留原文件，不作为评分输入。
- task_info.json 同步移除已私有化维护 JSON 的公开 data 声明；完整科学输入不变。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final。AR 的零虚频 count→空数组、limitations 列表→字符串仅在私有映射中无损转换，不修改 group 结果或现行评分。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_e31cc7bc7b21b610`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 按已批准边界保留 source-optimized 给定对象/初态；统一 XYZ 注释和 task_info，不称其为独立生成或待发现几何。待求性质/中间关键点仍由 agent 计算，未公开结果或排名。

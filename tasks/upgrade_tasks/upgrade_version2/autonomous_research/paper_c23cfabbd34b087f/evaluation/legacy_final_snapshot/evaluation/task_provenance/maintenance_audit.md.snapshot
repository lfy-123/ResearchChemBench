# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_c23cfabbd34b087f`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

按已批准边界保留 source-optimized 给定对象/初态；统一 XYZ 注释和 task_info，不称其为独立生成或待发现几何。待求性质/中间关键点仍由 agent 计算，未公开结果或排名。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：1M-TIPS D3 / PCM TD20

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_c23cfabbd34b087f`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的固定模型吸收成立；作者优化几何作为已给定模型的角色待验收。

复审摘要：102原子截短模型，300实频+TD20有据；不得外推实验长链/聚集体系。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_c23cfabbd34b087f)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_c23cfabbd34b087f`；group：`group_2`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p4 的模型近红外吸收与跃迁指认；SI PDF p42 计算方法、p44–46 的 1M-TIPS 模型坐标。

- [正文](../../../../../papers/paper_c23cfabbd34b087f/documents/main.pdf)
- [SI](../../../../../papers/paper_c23cfabbd34b087f/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

102 原子 C58H42Si2，charge 0/singlet、CHCl3；不得补成实验 dodecyl 体系。XYZ 全匹配 SI，原 task 已明确是 supplied model geometry 的吸收性质计算，不是几何发现；本轮明示这个既有范围，未临时重定义目标。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

真实显式 D3/PCM(CHCl3) 模型 Opt/Freq 有 300 实频，TD20 得到 735.93 nm/f=1.2539；209→210 为 HOMO→LUMO，系数0.69912，支持 π–π* 指认。与735±25 nm、1.24±0.25相容。

只支持现有截短分子模型吸收，不是全实验取代体系/聚集光谱；未执行 NTO 不能补写 NTO 图。state index 不是强制物理身份。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_2/paper_c23cfabbd34b087f/report/results.json) 保持只读。

专门核查记录：

- [provenance/author_route_evaluation_audit.json](../../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/author_route_evaluation_audit.json)
- [provenance/1m_tips_td_state_parse.json](../../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/1m_tips_td_state_parse.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `ar_r_geom` → `ar_process_geometry` | semantic；真实证据/适用边界见第 3 节 | `$.validation.stationary_point_test` / `$.validation.imaginary_frequency_count` |
| `ar_r_state` → `ar_process_state` | semantic；真实证据/适用边界见第 3 节 | `$.validation.state_selection_evidence` / `$.investigation.selection_rule` |
| `ar_r_wave` → `ar_wavelength` | 735.93；参考 735 ± 25 nm；算术通过 | `$.result.wavelength_nm` |
| `ar_r_osc` → `ar_oscillator` | 1.2539；参考 1.24 ± 0.25 dimensionless；算术通过 | `$.result.oscillator_strength` |
| `ar_r_char` → `ar_character` | semantic；真实证据/适用边界见第 3 节 | `$.result.dominant_transition` / `$.result.transition_character` |
| `ar_r_final` → `ar_final` | semantic；真实证据/适用边界见第 3 节 | `$.result.conclusion` / `$.limitations` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：澄清既有给定结构角色/公开来源，或补全格式拆分后的主语；不改变目标、方法或评分。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final；保留实际轨道展开作为指认，不新增隐藏指标。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_c23cfabbd34b087f`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 定向复核给定 C58H42Si2/102 原子及 CHCl3，300 实频、TD20/735.93 nm/f1.2539 支持模型吸收；不硬编码轨道 209→210，不要求新增 NTO 或实验长链/聚集模型。

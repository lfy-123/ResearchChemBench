# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_d8e5490cd9942f4f`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

按已批准边界保留 source-optimized 给定对象/初态；统一 XYZ 注释和 task_info，不称其为独立生成或待发现几何。待求性质/中间关键点仍由 agent 计算，未公开结果或排名。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：syn / anti La-KHQ 热化学

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_d8e5490cd9942f4f`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

AR/PR 的指定 syn/anti 自由能比较成立；给定作者端点的范围仍应由你验收。

复审摘要：两端点各 237 实频，ΔG=4.393821；不是完整构象搜索，作者端点保留边界待确认。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_d8e5490cd9942f4f)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_d8e5490cd9942f4f`；group：`group_2`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

正文 PDF p5；SI PDF p21–22 Eq. S2 / Table S2 的 ΔG 定义与 4.2 kcal/mol，p85–91 syn/anti 优化结构。

- [正文](../../../../../papers/paper_d8e5490cd9942f4f/documents/main.pdf)
- [SI](../../../../../papers/paper_d8e5490cd9942f4f/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

两端点各 81 原子，La+C32H38N4O6，charge +1/singlet；水连续介质、298 K、1 M 与 ΔG=G(anti)−G(syn) 公开明确。坐标全匹配 SI，但任务本来就是给定两构象端点自由能比较，未把端点生成当待发现目标；未公开谁更稳定。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

ωB97XD、La LCRECP46MWB、SMD(水) 两 Opt/Freq 均 237 实频；ΔG=4.393821 kcal/mol，在4.2±1内。相同分子数的1 M标准态校正相消，不把1 atm单个绝对 G直接冒称不经校正的1 M绝对值。

仅比较两个指定端点，有限 alternatives/retries；不是全局构象、质子转移、络合形成或完整溶液平衡。数值规则绑定还含 unit 字段，这是语义配对不是第二个要减目标的数字；验收已分别检查值和单位。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/report/results.json) 保持只读。

专门核查记录：

- [provenance/author_route_evaluation_audit.json](../../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/author_route_evaluation_audit.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `r_kp_process_minima` → `kp_process_minima` | semantic；真实证据/适用边界见第 3 节 | `$.endpoints[].id` / `$.endpoints[].identity` / `$.endpoints[].validation_status` / `$.endpoints[].imaginary_mode_count` / `$.investigation` |
| `r_kp_process_consistency` → `kp_process_consistency` | semantic；真实证据/适用边界见第 3 节 | `$.endpoints[].id` / `$.endpoints[].free_energy` / `$.endpoints[].free_energy_unit` / `$.route` / `$.investigation` / `$.investigation` |
| `r_kp_result_delta_g` → `kp_result_delta_g` | 4.393821；参考 4.2 ± 1 kcal/mol；算术通过 | `$.conclusion.delta_g_conf` / `$.conclusion.delta_g_unit` |
| `r_c_final_preference` → `c_final_preference` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |
| `r_c_limitation` → `c_limitation` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |

历史正式 results.json 直接通过当前 result_schema 检查。

当前绑定均能在真实结果中定位；值、单位、符号和候选/态身份仍以上述逐篇科学判断为准。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- `agent_input/task.md`：澄清既有给定结构角色/公开来源，或补全格式拆分后的主语；不改变目标、方法或评分。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

两模式移 final；已明确几何来源/角色，不改电子态或自由能零点。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_d8e5490cd9942f4f`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

- 定向复核给定 81 原子 La +1/singlet、水/298 K/1 M 及 Ganti−Gsyn；历史两端点各 237 实频、4.393821 kcal/mol 仍对应当前固定对象。未扩大全局构象范围。

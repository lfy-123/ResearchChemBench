# 当前目录与审批状态（2026-09-17）

本包已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权，迁入 `tasks/final_verified_autonomous_research/paper_6f9a36fff6964313`。

当前任务范围、有效计算依据和限制见[已验证计算参考](../verified_computation_reference.md)。本次迁移及元数据收尾未改变任务科学内容，也未新增量化计算或模型盲测。

下方“仍在 verified_tasks”“未批准迁移”“已退回 verified_tasks”等文字属于此前维护阶段的历史状态，不代表当前目录或审批状态；当前状态以本节为准。历史科学事实和修复记录保留不变。

---

# 历史实施状态（2026-09-16）

## 已批准修复记录（2026-09-16）

PR 补无答案两层级 Mulliken 主协议；AR 单构象不再被要求证明全构象不变性，未做敏感性仍不能取得稳健性证据分。原量和容差未改。

本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。

---

# 本批维护审查：三体系 Mulliken 电荷

> 当前状态：已按负责人指令退回 verified_tasks 复审；本文件下方为前轮审查记录，不是负责人验收/迁移批准。当前仅记录问题和建议，等待确认后才改任务；再次迁入 final 或 hold 还需独立的明确确认。

## 本次复审结论（2026-09-16，待负责人确认）

本模式：`autonomous_research`。工作目录：`tasks/verified_tasks/autonomous_research/paper_6f9a36fff6964313`。本批全部34包均已退回暂存；本包未获得 final/hold 迁移确认。

PR 的方法—电荷评分协议未对齐；AR 的单构象覆盖/稳健性措辞需要澄清，而不是重新判为未验证。

复审摘要：PR 自选方法与固定 Mulliken 数值不匹配；AR 不应把有限覆盖说成构象不敏感。

具体文件/规则、论文及真实输出依据、模式差异和建议修法见[集中报告中的本篇分析](../../../../verified_tasks/MAINTENANCE_REPORT.md#paper_6f9a36fff6964313)。本轮只分析；没有再修改 task.md、科学输入、schema 或 evaluator，也没有新增量化计算。即使建议无需科学修复，也须负责人验收并另行批准去向后才可迁移。

**下方为前轮维护历史。其“移 final/hold”“通过”字样仅记录前轮审查者判断，迁移已撤回，不代表当前验收或授权；以本次复审和集中报告为准。**

日期：2026-09-16。论文：`paper_6f9a36fff6964313`；group：`group_1`；模式：`autonomous_research`。

结论：**当前既有科学范围通过，移入 final**。当前既有科学范围内可移入 final；作者路线证据不等于自主盲测通过。

修复前版本：`e67441a9`；格式检查点：`42970e03`。本记录不是 evaluator 规则，也不证明运行时隔离或自主 agent 盲测通过。

## 1. 原文依据与对象

SI S16 的两层级路线与 Fig. S7 的 Mulliken 电荷；原文图示阳离子片段，而当前任务明确的完整离子对必须保留 OTf。

- [正文](../../../../../papers/paper_6f9a36fff6964313/documents/main.pdf)
- [SI](../../../../../papers/paper_6f9a36fff6964313/documents/supplementary_001.pdf)
- [当前任务](../../agent_input/task.md)、[提交 schema](../../agent_input/submission_schema.json)

## 2. 输入、答案边界与必要信息

systems.json 以 SMILES、分子式、电荷、自旋、MeCN 和原子环境定义 TFAP、PTMA·OTf、TMTFABA·OTf。无作者 3D、电荷答案或候选排名；17/32/37 原子体系均可独立构建。

模式核对：AR 只以当前公开科学问题、对象与测量边界作为输入；本维护没有把历史作者方法、参考数值、胜出构象/机理或本档案加入 agent_input。历史科学链可以共用，但其作者定向选择不冒充自主探索证据。

## 3. 历史真实计算支持与限制

B3LYP-D3BJ/6-31G(d,p)/IEFPCM(MeCN) 三次 Opt/Freq 分别 45/90/105 实频；同几何 M062X-D3/def2TZVP/SMD(MeCN) 单点给出 qC(TFAP)=0.203728、qC(TMT)=0.198533、qN(PTMA)=0.040059、qN(TMT)=0.058695 e；四值落在 PR 现行 ±0.02 e 内。SP/优化几何依赖已核对。实际只有每体系一个验证构象。

AR 以可审计四电荷、差值、覆盖和不确定性为目标，不把作者四个固定数值作为硬评分；可以在诚实的有限覆盖范围内通过。PR 却允许自选电子结构方法/基组和离子对构象，同时硬比上述作者电荷；最后一项已离容差边界仅约 0.001305 e。Mulliken 电荷不是与模型无关的唯一实验量，这属于比较协议未对齐，不能以一次算中数字宣称公平性已闭合。

完整有效步骤及输入/输出索引见 [verified_computation_reference.md](../verified_computation_reference.md)，不依赖本文件作为评分标准。原始 [group 结果](../../../../../docs/verification/group_1/paper_6f9a36fff6964313/report/results.json) 保持只读。

专门核查记录：

- [provenance/charge_closure_audit_20260915.json](../../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/charge_closure_audit_20260915.json)
- [artifacts/complete_author_charges_20260915.json](../../../../../docs/verification/group_1/paper_6f9a36fff6964313/artifacts/complete_author_charges_20260915.json)

## 4. 当前评分契约核对

原有五个 evaluator JSON 已核对。下表是与实际结果的字段绑定/算术复核；semantic 行的科学解释见上节，**没有重新运行 LLM judge**。格式成立不消除上节的科学问题；尤其错误分子的数值不能认证论文目标。

| 规则 → 关键点/结论 | 类型与真实结果核对 | 绑定 |
|---|---|---|
| `ar_s1` → `ar_p1` | semantic；真实证据/适用边界见第 3 节 | `$.coverage` / `$.systems` |
| `ar_s2` → `ar_p2` | semantic；真实证据/适用边界见第 3 节 | `$.systems` |
| `ar_s3` → `ar_r1` | semantic；真实证据/适用边界见第 3 节 | `$.status` / `$.systems` / `$.comparison` / `$.failure` |
| `ar_s4` → `ar_c1` | semantic；真实证据/适用边界见第 3 节 | `$.conclusion` |
| `ar_s5` → `ar_c2` | semantic；真实证据/适用边界见第 3 节 | `$.limitations` |

历史正式 results.json 不能直接符合当前 AR schema；已在私有 [historical_result_schema_mapping.json](historical_result_schema_mapping.json) 中作无损字段适配，映射后的 schema 检查通过。新增文字仅说明既有覆盖/选择限制，未伪造新搜索或结果。

成功分支没有填充 `$.failure`；这些只用于失败/局限分支，不当作缺少科学结果。其余绑定均能在真实结果/私有等价映射中定位。

## 5. 本轮实际修改

- 先按统一章节整理 task.md；PR 单列既有作者定性 guidance。格式步骤没有改变非标题文字。
- 本包科学输入和评分未改；只作格式、reference 适用性说明和维护归档。
- 更新 reference 的任务版本说明，避免把维护后的副本仍称为“原样仅复制”。
- 包迁移只调整目录与相对链接；manifest 随文件变化重建。源任务、正文/SI 和 group 原始记录不修改。

## 6. 后续行动与发布边界

AR 移 final，私有无损字段映射保留只做一构象的事实。PR 移 hold：建议确认后公开 SI 两层级主比较协议（无四个答案），明确离子对/构象选择与敏感性报告；或保留方法自由而另行批准方法敏感的评分分支。不自行锁定方法、扩大容差或降为 optional。

前轮建议去向（迁移已撤回）：`tasks/final_verified_autonomous_research/paper_6f9a36fff6964313`。集中报告：[MAINTENANCE_REPORT.md](../../../../verified_tasks/MAINTENANCE_REPORT.md)。相对链接已按退回 verified_tasks 后的实际位置重算。

没有新增量化计算、HPC 操作或 benchmark 发布。包校验/软件回归不能替代科学审计；只交付 agent_input 的物化路径已核查，真实运行环境的挂载、共享目录、网络和检索隔离尚未作端到端测试。任务的五个 evaluator JSON 与 reference 继续位于私有侧；task_provenance 是可移除的维护资料，不是 agent 必需输入。

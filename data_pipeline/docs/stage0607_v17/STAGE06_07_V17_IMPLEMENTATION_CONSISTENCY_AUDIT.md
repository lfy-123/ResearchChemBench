# Stage06/07 v17 实施一致性审计

## 1. 审计结论

本轮代码与 `STAGE06_07_V17_BOUNDED_STAGE07_AUDIT_AND_REPAIR_MODIFICATION_PLAN.md` 一致，可以进入同十篇论文实测。核心阶段边界、失败语义和 evaluator Gate 已落实；没有加入论文特例或 tolerance 科学值硬编码。

## 2. 逐项对照

### Stage06 是唯一 Builder

- Stage06 仍负责目标选择、输入闭合、两种公开模式和 evaluator 文件生成。
- Stage07 prompt 明确禁止 replacement workflow、new objective、system-set change 和从论文重建。
- Stage07 新决策集合不存在 `approved_after_workflow_redesign`。

### Stage07 只审计可审计候选

- Runner 与 Stage07 的 eligible set 均只包含 `provisional_constructed` 和 `constructed`。
- `provisional_not_constructible` 的 handoff 设为 false，不进入 Stage07。
- `execution_artifact_incomplete` 变成 `artifact_delivery_failure_retryable`，不再伪装成科学拒绝，也不进入 Stage07。

### Stage07 单次审计与有限修复

- 主执行路径只创建一个 attempt workspace，只调用一次 harness。
- request 显式设置 `codex_native_resume=false`。
- Agent/API/receipt 失败直接形成本次执行失败 checkpoint，不再次调用新 Agent。
- 已完成 checkpoint 的读取仍保留，用于进程中断后的任务级断点复用；它不延续失败对话。
- 外部 Gate 对最终快照只读运行一次，不触发第二次 Agent 调用。

### evaluator crosswalk

共享 helper 检查：

- 纯 numeric scalar/list/map 是否使用 numeric rule，或具有明确 projection；
- numeric target 是否为非空纯数值结构；
- 无 projection 时 target/reference 的形状和值是否一致；
- 多个 binding fields 配 scalar target 时是否有 projection；
- reference/rule ID、submission artifact、field 和 comparison 的基础闭合。

Stage06/Stage07 Agent self-check 和 external Gate 均通过安装同一个 `evaluator_reference.py` 使用该 helper。

不检查：

- tolerance 是否取科学最优值；
- tolerance 是整数、小数、字符串说明还是嵌套格式；
- unit 使用统一字符串还是非空字段映射；
- 特定论文、分子、软件或 comparison 命名。

### Stage06 完成顺序

Prompt 要求 workflow review 保持紧凑且闭合，随后立即 bootstrap 和生成 task/evaluator；只有完整树通过自查后才补充非必要 metadata。finalization reserve 只能用于补文件、Gate 修复和最终复读，不能重复 `pwd`、宽泛 `ls/find` 或重新选择 scope。

## 3. 已知非阻断遗留

`stage07_task_judge/stage.py` 中仍存在未接入生产调用图的旧 `_run_audit_agent()` 参考 helper，现行 `run_stage07()` 不调用它。生产路径已经是单次 `_run_audit_repair_agent()`。该旧 helper 不影响本轮行为，但后续可在单独清理提交中连同专属旧测试删除，避免把代码清理和本轮行为修改混在一起。

部分旧测试仍以 `task_pair_id` 构造 fixture；当前生产合同已统一为 `paper_id`。本轮没有为了让这些旧 fixture 通过而恢复双 ID 兼容逻辑。

## 4. 实测验收条件

- Stage07 不处理科学拒绝或 artifact-incomplete 产物；
- 不出现 `approved_after_workflow_redesign`；
- Stage07 每篇最多一次 Agent 调用；
- `paper_9ec...` 若 Stage06 再次未交付完整产物，不得由 Stage07 重建发布；
- `paper_a556...` 的自然语言 Figure connectivity 不得被当作机器可执行输入；
- 发布 evaluator 不得出现 numeric-map/semantic 无 projection；
- 发布 evaluator 不得出现 multi-field/scalar target 无 projection；
- 每个发布任务必须逐篇审查 task、inputs、reference、rules 和 reproduction/autonomous 转换。

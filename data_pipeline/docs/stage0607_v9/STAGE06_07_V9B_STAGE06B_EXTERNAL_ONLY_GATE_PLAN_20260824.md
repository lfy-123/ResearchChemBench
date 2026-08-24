# Stage06/07 v9B：Stage06B 取消 Agent 自查、保留外部只读 Gate

日期：2026-08-24

状态：实施中

关联方案：`STAGE06_07_V9_AGENT_SELF_CHECK_AND_EXTERNAL_GATE_PLAN_20260824.md`

## 1. 本轮目标

本轮只调整 Gate 的运行职责，不改变科学任务选择、hidden reference、评分语义、模式边界或 Stage07 的科学审计职责。

目标流程：

```text
Stage06A：Agent 生成 → Agent 自查 phase_gate → 同一 workspace 修复 → 编排器外部只读 Gate
Stage06B：Agent 生成转换结果 → 编排器外部只读 Gate（一次）→ Stage07
```

Stage06B 不再收到强制运行 `phase_gate.py` 的 prompt，也不因外部 Gate finding 触发 Codex resume。普通 API/超时/无效 receipt 重试仍然保留。

## 2. 为什么只取消 Stage06B Agent 自查

Stage06A 负责构建科学任务对和 handoff 文件，存在较多相互依赖的文件，因此 Agent 在同一上下文内自查有直接价值。

Stage06B 是窄范围的 autonomous public-surface converter，主要执行脱敏、目录清理和交付面保持。它不负责重新判断科学范围，Agent-facing Gate 会增加工具调用并与转换工作竞争预算；当前失败轨迹中的主要失败类型也是转换语义/预算问题，而不是 Gate finding。

Stage06B 仍保留一次外部只读 Gate，因为 Agent 仍会修改公开文件，路线文件泄漏、内部协议泄漏、输入路径缺失和交付合同不闭合仍需在进入 Stage07 前被观测。外部 Gate 的 finding 作为 warning 传递给 Stage07，不在 Stage06B 内启动恢复循环。

## 3. 关键实现约束

### 3.1 不可直接把布尔值改为 false

当前 `_run_phase()` 将 `phase_gate_agent_self_check=True` 同时解释为“Agent 自查 + 外部检查”；将其改为 `False` 会落入旧的 Gate finding recovery 路径，反而可能触发 retry/resume。

因此新增显式的内部 Gate 模式（不暴露给论文任务）：

- `agent_and_external`：注入 Agent 自查 prompt，并执行一次外部只读 Gate；Stage06A 使用。
- `external_only`：不注入自查 prompt，只执行一次外部只读 Gate；Stage06B 使用。
- `bounded_recovery`：保留旧 fixture/兼容调用的 Gate finding recovery 行为。
- `none`：不启用 Gate。

当未提供新模式时，旧的 `phase_gate_agent_self_check` 参数继续映射到兼容行为，避免破坏已有测试和历史调用。

### 3.2 Stage06B 外部 Gate 行为

- `phase_gate_max_checks=1`；外部检查不产生第二次模型调用。
- Gate finding 写入 `phase_gate_report.json`、converter receipt 和 handoff warning。
- `agent_self_check_required=false`，报告 authority 为 `orchestrator_external_read_only`。
- 不修改科学输入、claims、答案、物理边界或 deliverables。
- Stage07A/Stage07B 和最终发布 Gate 仍可根据完整 pair 决定修复或阻断。

### 3.3 Prompt 边界

Stage06A 的自查指令保持不变。

Stage06B 删除 `MANDATORY AGENT SELF-CHECK` 段落，仅保留转换职责、答案盲、公共表面和 receipt 要求。不得因为取消自查而增加论文特例关键词、固定文件名单以外的科学规则或新的恢复协议。

## 4. 代码修改范围

1. `src/stages/stage06_task_builder/stage.py`
   - 为 `_run_phase()` 增加显式 Gate 模式解析；拆分“是否向 Agent 注入自查”和“是否执行外部只读 Gate”。
   - Stage06A 调用设为 `agent_and_external`。
   - Stage06B 调用设为 `external_only`。
   - 修正 Gate 报告中的 `agent_self_check_required`，不再硬编码为 true。
   - 保留旧 bounded recovery 作为兼容路径，但新 Stage06B 不进入该路径。
2. `src/stages/stage06_task_builder/prompts.py`
   - 将 Stage06B prompt 版本标记为 external-only；删除强制调用 Gate 的段落。
3. `tests/test_stage0607_v9_self_check.py` 与必要的早期 Gate 测试
   - 增加 external-only 单调用、无 prompt 注入、finding 不触发 recovery 的回归。
   - 保证旧 bounded recovery fixture 仍通过。
4. 本目录实施日志
   - 记录代码 diff、测试命令、Git commit、测试样本清单和运行分析。

不修改 Stage00–05、benchmark 评分器、论文科学规则和 Stage07B 的科学边界。

## 5. 回归与验收标准

代码回归必须证明：

1. Stage06A 的 prompt 包含自查命令，Gate finding 能在同一 workspace 进入 Agent 修复上下文。
2. Stage06B 的 prompt 不包含强制自查命令。
3. Stage06B external-only 只调用 Agent 一次；外部 Gate finding 只记录并返回，不触发 `RECOVERY_CONTEXT.md`、Codex resume 或第二次 Agent 调用。
4. Stage06B external-only 报告标记 `agent_self_check_required=false`。
5. 旧调用未显式指定模式时，已有 bounded recovery 测试保持原行为。
6. Gate 仍然只做 transport/public-contract 检查，不增加论文、分子、数值或科学中心性特例。

## 6. 10 篇历史科学通过样本测试

代码回归通过后，从已有 Stage06/07 运行结果中选择 10 篇曾经 `scientific_audit_passed=1` 且有 Stage07 科学批准记录的论文。样本固定写入测试 manifest，优先覆盖：

- 已发布/机械通过；
- 科学批准但机械阻断；
- 启用过 Stage07B 修复；
- reproduction/autonomous 两种模式都有文件的任务。

使用 `gpt-5.6-sol`、Codex harness，并发 10。测试不是要求所有论文重新科学批准，而是验证 Gate 与阶段职责。

逐篇记录：

- Stage06A Agent 自查是否执行、最终 findings、外部 Gate 是否通过；
- Stage06A handoff 是否在进入 Stage06B 前满足 Gate 要求；
- Stage06B 是否只执行一次外部 Gate，是否出现 converter retry；
- Stage07A/Stage07B 的决策、最终 Gate 状态和发布状态；
- 每个未通过 Gate 的 finding、缺少文件/字段、责任阶段和必要性；
- 将代码缺陷、prompt 执行失败、论文输入闭合问题和模型能力问题分开统计。

Gate finding 的“缺少”不自动等于“必须补齐”：分析时按以下三类归档：

- 发布合同必需：缺失时应由对应阶段生成或由 Stage07B 修复；
- 科学内容必需：由 Stage06A/Stage07A 判断，代码不代替科学裁决；
- 可选/模式不适用：不应阻断，若阻断则视为 Gate 误报或合同绑定错误。

## 7. 风险与回退

若测试显示 Stage06B 外部 warning 无法可靠传递到 Stage07，先修复 handoff 传递，不恢复 Agent 自查循环。只有在发现通用、可重复的 Stage06B transport 问题且外部 Gate 无法被后续阶段处理时，才重新评估是否需要在 prompt 中加入一段简短的人工检查清单；不为单篇论文添加规则。

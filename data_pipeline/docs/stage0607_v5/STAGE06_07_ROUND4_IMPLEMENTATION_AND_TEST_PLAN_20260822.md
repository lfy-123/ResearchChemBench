# Stage06/07 v5.1 第四轮实施与测试记录

日期：2026-08-22
基线：`e4e820d`（hidden reference 的编排器 `task_pair_id` 规范化已经提交）

## 1. 本轮目标

本轮以 v5.1 总目标为约束，先处理上一批 DeepSeek 10 篇中能够确定归因于通用合同/运输层的两个问题：

1. private `critical_failures` 允许使用带 `id` 和 `message` 的结构化记录，但 evaluator schema 只接受 `list[str]`；这会让科学已批准的任务被机械阻断。
2. Agent 生成的 `observed_fields` 反复出现 `$..field`。Stage07 已定义的绑定子集使用 `$.field`、`$.group.field` 和 bracket-quoted selector，不支持 recursive descent；该输出可以做受限的确定性运输归一化，但不能由代码推断科学字段。

本轮不新增论文、分子、固定答案、固定软件或数值特例，也不把科学代表性、输入闭合、参考态和软件可用性改写成机械规则。

批量运行中又确认一个通用编排问题：`src.cli run-stage06-07` 的进程码 0 不代表 Stage06/07 内部一定完成。批处理脚本现读取 `late_stage_run_summary.json`，将 Stage06 retryable/artifact-delivery failure、Stage07 未运行、Stage07 retryable failure、summary 缺失/损坏标为批次失败；科学拒绝和机械阻断仍作为已完成的科学结果记录。

同一批次还出现 Stage06B 明确返回 `needs_conversion_retry`、但 `_converter_phase_findings()` 原先把该状态当作“无需检查”，随后直接结束 Stage06 的情况。现已把这个显式可恢复状态接入 `_run_phase` 已有的有限重试/恢复循环，不改变 Stage06B 的科学权限。

## 2. 实施内容

### 2.1 Stage07 evaluator projection

- 在 `_project_hidden_for_mode()` 中把 private `critical_failures` 的字符串/结构化记录投影为 evaluator 所需的字符串列表。
- 保留 `id: message` 文本，科学内容不变；该投影只解决 schema 类型边界。
- 增加回归测试，验证含结构化 critical failure 的双模式 pair 可以通过 schema dry-run。

### 2.2 绑定路径运输归一化

- 在 mechanical gate 的 evaluator dry-run 之前扫描所有 acceptance profile 的 `observed_fields`，包括 mode-specific binding。
- 只把满足“以 `$..` 开头、去掉一个点后仍是当前受支持 JSONPath 子集，且对应显式路径在至少一个适用 mode 的结果 schema 中为 `present/open`”的选择器改为 `$.` 形式。
- 不解析、不改写其他 JSONPath，不寻找候选字段，也不改变 target、tolerance、proposition 或 mode scope。
- 将修改文件的前后 SHA-256 和 profile ID 写入 `orchestrator_normalizations.json`/机械报告的 `normalization_records`，保证 Agent 原始产物与最终发布树可追溯。
- Stage07 prompt 增加 `$..` 反例和最终逐条复核要求。

### 2.3 总目标同步

v5.1 总目标已经明确：完整论文核心计算路线优先；只有成本、关键数据、路线闭合等独立科学理由成立时才退回最重要核心子过程；完整路线和核心子过程都无法构建时科学拒绝；工具箱缺少软件只能登记缺口，不能作为科学拒绝理由。该原则由 Stage06A/Stage07 审计，不由本轮代码硬编码。

## 3. 回归验证

通过：

```text
PYTHONPATH=. pytest -q tests/test_stage0607_agents.py tests/test_stage0607_v5_contracts.py
156 passed（加入批次内部失败和 Stage06B retry 状态回归测试后）

PYTHONPATH=. pytest -q tests/test_batch_workflow.py tests/test_stage_layout.py tests/test_pipeline.py
259 passed
```

新增测试覆盖：

- 结构化 `critical_failures` 的 evaluator projection；
- `$..foo` 到 `$.foo` 的受限归一化；
- normalization provenance 记录；
- 既有 hidden identity、mode-specific binding、open schema 和 route evidence 测试仍保持通过。

## 4. 上一批 10 篇结果的归因结论

结果目录：`runs/stage06-07-v5-round3-deepseek10-concurrency10-20260821-retry`。

- 10/10 进程完成，全部 `exit_code=0`；Stage07 科学结果均为 `approved_with_repairs`。
- 7 篇已发布，2 篇被旧代码的 `$..` binding 误阻断，1 篇被结构化 `critical_failures` schema 冲突阻断；这三类阻断不是科学拒绝。
- `task_pair_id` 阻断已在 `e4e820d` 修复；本轮补齐另外两类通用合同问题。
- 论文代表性需逐篇由 Agent/人工对正文和 SI 复核，不能由机械 gate 判定。已核对的任务中，完整路线或最重要核心子过程的选择总体符合 v5.1 原则；软件缺口任务保持科学任务并标记 `conditional`，没有被错误拒绝。
- `Stage07B` 本轮仍不启用：旧批次的机械阻断主要是两个确定性合同 bug，修复后需要重新抽样验证，尚无证据表明需要第二个 Agent 承担稳定、窄且重复的修复族。

## 5. 下一步测试

提交本轮代码后，使用 `deepseek-v4-pro-0813`、`codex` harness、`high` reasoning、并发 10，从 Stage05 通过集合用固定随机种子重新抽取 10 篇。提交后按要求等待约 30 分钟，再逐篇检查：

- Stage06A 是否先考虑完整论文核心路线；
- 降级子流程是否为最重要且有证据的核心子流程；
- 两者均不可构建时是否明确科学拒绝，而不是选择外围流程；
- 软件缺口是否登记但不导致科学拒绝；
- Stage06B 是否保持答案盲和公共边界完整；
- Stage07 是否完成科学审计、代表性审计和合同修复；
- mechanical gate 是否只报告真实 transport 问题，且不再产生上述两类误阻断。

若新批次仍出现同一类通用合同问题，下一轮只继续改通用 prompt/合同边界；若只出现论文输入不足、源材料缺失或模型科学判断差异，则记录为任务/模型问题，不添加论文特例。

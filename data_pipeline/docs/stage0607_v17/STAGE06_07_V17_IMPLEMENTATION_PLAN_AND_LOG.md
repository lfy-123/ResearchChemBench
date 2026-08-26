# Stage06/07 v17 代码修改计划与实施记录

## 1. 实施原则

- 以 `STAGE06_07_V17_BOUNDED_STAGE07_AUDIT_AND_REPAIR_MODIFICATION_PLAN.md` 为唯一设计基线。
- 只做通用阶段边界、状态语义和 evaluator 一致性修改，不增加论文特例。
- 保留 v16 已完成的输入闭合、最终合成和统一 Gate 设计。
- 优先删除 Stage07 redesign 分支和重复职责，不建立新的复杂编排层。
- Gate 只阻断明确不可执行的合同矛盾，不判断 tolerance 的科学最优值。
- 修改后先做定向回归，再跑同十篇论文。

## 2. 代码修改计划

### P1. 固化 Stage07 准入边界

- 修改 `src/late_stage_runner.py`，只把 `provisional_constructed`/`constructed` 送入 Stage07。
- 修改 `STAGE07_ELIGIBLE_STAGE06_DECISIONS` 使用相同集合。
- 添加路由回归测试，锁定 `provisional_not_constructible` 不进入 Stage07。

状态：已完成。Runner 和 Stage07 使用相同的准入集合；科学拒绝不再进入审计阶段。

### P2. 分离 Stage06 科学拒绝和执行未完成

- 在 Stage06 receipt 归一化/发布边界识别 `execution_artifact_incomplete`。
- 将其发布为 `artifact_delivery_failure_retryable`，设置 `handoff_ready=false`。
- 保留真正 source-backed `scientific_not_constructible` 的现有路径。
- 添加与 `paper_9ec...` 同构的 fixture。

状态：已完成。`execution_artifact_incomplete` 被归为 `artifact_delivery_failure_retryable`，并设置 `handoff_ready=false`。

### P3. 缩减 Stage07 prompt 和决策合同

- 将角色改为 existing-candidate scientific auditor and bounded repairer。
- 删除切换 workflow、重新选择 scope、重建任务和 redesign closure 段落。
- 明确科学目标、系统集合、计算问题和结论含义为不可变边界。
- 保留 source materials，仅用于核实/修复当前候选。
- 强化输入机器可执行闭合和 evaluator crosswalk。
- 删除 `approved_after_workflow_redesign` schema、approved set、summary 和测试期望。

状态：已完成。Stage07 prompt、schema、approved set 和汇总均删除 redesign 成功路径；主执行函数只调用 Agent 一次，不执行失败后 retry、conversation resume 或 Gate 驱动的第二次 Agent 调用。已完成 checkpoint 复用仍保留为任务级断点恢复。

### P4. 增强通用 evaluator 一致性检查

- 在共享 helper 中识别纯 numeric scalar/list/map。
- 检查 rule type 与 reference value shape。
- 检查多字段/scalar target 是否具有明确 aggregate/projection。
- 对 direct identity numeric 规则检查 target/reference 对应。
- tolerance 科学选择继续保持非阻断。
- 保证 Stage06/Stage07 self-check 和 external Gate 复用同一 helper。

状态：已完成。共享 checker 现在检查 numeric scalar/list/map、rule/reference 类型、target/reference 形状和值、多字段 scalar target 与 projection。unit 只要求非空；tolerance 格式/科学选择仍为 diagnostic。

### P5. 优化 Stage06 交付顺序提示

- 强化先生成完整 task/evaluator，再补充非必要详细 metadata。
- 禁止在 finalization reserve 重复目录检查和重新展开 source。
- 不通过简单增加工具上限掩盖完成顺序问题。

状态：已完成。Prompt 要求先写紧凑闭合 review，随后立即 bootstrap 并交付 task/evaluator；finalization reserve 禁止重复目录枚举和重新展开 scope。

### P6. 定向测试和全量相关回归

- 新增 v17 定向测试文件。
- 更新受决策集合变化影响的既有 Stage07 测试。
- 运行 v10-v16 evaluator/Gate、Stage06/07 agent 和 pipeline 定向集合。
- 记录测试命令和结果。

状态：已完成 v17 定向与相邻 Gate 回归；旧版全量测试中的历史 ID/redesign/recovery fixture 另行记录，不作为新合同预期。

### P7. 方案一致性审计

- 对照设计文档逐条检查代码和测试。
- 检查是否残留新的 Stage07 workflow redesign 生成路径。
- 检查 Stage06 failure semantics 和 runner 路由一致。
- 检查未引入论文特例和 tolerance 过度阻断。
- 记录偏差和最终结论。

状态：已完成代码级审计，结论记录于独立一致性报告。

### P8. 同十篇论文测试与产物审计

- 使用 `gpt-5.6-sol`、high reasoning 和与前轮相同论文集合。
- 监督批次至终态。
- 汇总 Stage06/07 决策、Gate、发布状态和失败原因。
- 对所有发布任务逐篇审计 task、inputs、reference、rules 和 mode conversion。
- 形成最终测试分析报告。

状态：待实施。

## 3. 实施日志

### 2026-08-26：设计基线

- 完成 v16.2 十篇结果复核。
- 确认 Stage07 当前允许 `provisional_not_constructible` 和 workflow redesign。
- 确认 `paper_9ec8c4761c4f171b` 是 artifact completion failure，而不是科学不可构建。
- 确认 published evaluator 存在 numeric map/semantic 和 multi-field/scalar target 漏检。
- 建立 v17 修改方案和本实施计划。

### 2026-08-26：代码实施

- Stage07 准入仅保留 `provisional_constructed` 和 `constructed`。
- Stage07 主执行路径改为一次 Agent 调用；删除失败后的语义 retry、Codex conversation resume、恢复工作区和 Gate recovery loop。
- Stage07 prompt 改为 existing-candidate audit，明确禁止替代 workflow、新目标、系统集合变更和从论文重建。
- approved receipt 不再要求 `candidate_workflows_checked`，避免重新搜索替代 workflow。
- Stage06 将 `execution_artifact_incomplete` 从科学拒绝分离为执行/交付失败。
- Stage06 prompt 优先完整 task/evaluator 交付，限制大体积 review 占用 finalization 预算。
- 共享 evaluator checker 新增通用 reference/rule/target/binding crosswalk 检查。

### 2026-08-26：回归和真实旧产物验证

通过命令：

```bash
PYTHONPATH=.:.. python -m pytest -q \
  tests/test_stage0607_v10_unified_gate.py \
  tests/test_stage0607_v13_split_reference.py \
  tests/test_stage0607_v15_minimal_evaluator.py \
  tests/test_stage0607_v16_contracts.py \
  tests/test_stage0607_v17_bounded_audit.py \
  tests/test_stage0607_v5_contracts.py
```

结果：`72 passed`。

Stage07 新边界相关补充测试结果：`14 passed`，包括单次 Agent 调用、禁止 redesign、完整 public-surface 审计和 evaluator crosswalk。

对 v16.2 真实旧产物运行新 checker：

- `paper_9ec8c4761c4f171b`：捕获 `scoring_rule_numeric_reference_type_mismatch:r1:semantic`；
- `paper_a5564360a31f760b`：捕获两条 `multifield_scalar_target_without_projection` 和两条 `target_reference_shape_mismatch`。

上述 findings 由值形状和绑定关系推导，没有论文、分子、软件、固定数值或 comparison 名称特例。

相关旧测试集合曾得到 `183 passed, 22 failed`。失败主要来自此前尚未更新的 `task_pair_id` fixture，以及已被本方案删除的 Stage07 redesign/two-attempt recovery 断言；其中本轮直接相关的 Stage07 prompt 和 single-attempt Gate 测试已经更新并单独通过。其余 ID fixture 属于更早的 paper_id 全局迁移遗留，不通过在生产代码恢复旧字段来消除。

后续实施、测试和一致性审计结果将在本文件继续记录。

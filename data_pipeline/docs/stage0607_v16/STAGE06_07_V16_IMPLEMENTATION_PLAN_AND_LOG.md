# Stage06/07 v16 代码实施计划与执行记录

本文件用于记录对 `STAGE06_07_V16_FINAL_SYNTHESIS_INPUT_CLOSURE_AND_GATE_MODIFICATION_PLAN.md` 的逐项实现、测试和一致性核对。

## 1. 实施原则

- 先修改 prompt 和数据边界，再修改验证器；
- 不让代码生成或猜测论文特定科学输入；
- 不新增 Agent、retry/replay 或第二套 Gate 语义；
- 保留用户已有的 Stage00–05、chemistry toolbox 和无关工作区修改；
- 每个阶段完成后运行定向测试，并用 Git 提交可回滚版本；
- 最终对照方案文档逐项审计，再提交同十篇论文测试。

## 2. 代码修改计划

### P1：合成 Prompt 重构

文件：`src/stages/stage06_task_builder/prompts.py`

任务：

1. 将模型身份改为 final scientific benchmark task synthesizer；
2. 删除模型可见的 `Stage06A`、`Stage06B`、`Stage07`、later repair、handoff 和 provisional 描述；
3. 将工作顺序固定为：科学目标选择 → 最小输入集合 → input closure → 完整任务/evaluator → self-check；
4. 明确模型不得把必需工作留给后续 Agent；
5. 保留 source-specific 输入恢复要求，但明确只检查 selected workflow 资产；
6. 明确 evaluator 五文件、四种 rule type、binding 和 tolerance 要求；
7. 要求 `process_rubric.json` 任务相关，不得使用空泛模板；
8. 保留一次 grouped validation 和 repair 的工具预算。

验收：prompt 文本不出现内部阶段职责转移，且包含 input closure、public/private isolation、evaluator completeness 和 final self-check。

### P2：Bootstrap public/private 边界

文件：`src/stages/stage06_task_builder/bootstrap_task_pair.py`

任务：

1. 删除完整 `workflow_scope` 写入 public `task_info`/`task_spec`；
2. 删除 `Replace this scaffold...` 默认值；
3. public metadata 使用明确白名单；
4. private `ground_truth_items`、`canonical_answer`、`evidence_ids`、private scope 只留在 evaluator/review；
5. 保留统一 `paper_id`，不增加 paper-level identity；
6. 不改变 evaluator-local `key_point_id`、`conclusion_id`、`rule_id`；
7. 让 public `task.md` 保持科学内容的唯一权威说明。

验收：fixture 中 private scope 和目标答案不会出现在 public task metadata；无 placeholder。

### P3：Input closure 合同

文件：`src/stages/stage06_task_builder/validation.py`、`src/stages/stage06_task_builder/stage.py`

任务：

1. 接受 `workflow_completeness_check.input_closure` 或等价 review 字段；
2. 对成功任务要求 `status=closed`、非空 assets、空 unresolved_fields；
3. 只验证 selected workflow 声明的最小资产集合；
4. 不实现论文特定的科学输入生成；
5. 将输入闭合状态写入 handoff/receipt 供后续审计；
6. 将 source extraction failure 与 scientific blocker 保持区分。

验收：成功 fixture 缺少必要输入时得到明确 finding；真正科学拒绝 fixture 不要求生成任务树。

### P4：通用资产和 public surface Gate

文件：`src/stages/phase_gate.py`、`src/stages/evaluator_reference.py`

任务：

1. 继续使用 shared evaluator helper；
2. 增加声明资产的非空、路径和适用格式基本读取检查；
3. 不根据文件内容猜测化学角色；
4. 检查 public 文件中的 private evaluator marker 和 placeholder；
5. 检查 key point/conclusion 与 scoring rule coverage；
6. 检查 binding 指向任务声明的提交字段；
7. tolerance 相关科学选择仅生成 diagnostics；
8. 不新增 `human_review_required`。

验收：损坏 XYZ、private scope 泄露、缺少 rule 的 fixture 阻断；非整数 tolerance fixture 不阻断。

### P5：回归测试

新增或扩展 tests：

- final synthesis prompt contract；
- input closure contract；
- bootstrap public/private isolation；
- placeholder rejection；
- generic structured asset validation；
- evaluator key point/conclusion/rule coverage；
- public answer leakage；
- tolerance diagnostic/non-blocking behavior；
- Stage06A/external Gate finding parity。

### P6：方案一致性审计和 Git

1. 运行 v15 既有定向测试；
2. 运行 v16 新增测试；
3. 对照方案文档逐项检查 prompt、代码和 Gate 行为；
4. 记录未实现或需要后续人工判断的边界；
5. 只提交本轮相关代码、测试和文档；
6. 保留用户其他工作区修改。

### P7：十篇论文测试

在代码和方案审计通过后，使用同一十篇论文、`gpt-5.6-sol`、`high` 推理强度和既定 API 配置运行测试。记录：

- 每篇 input closure 状态；
- Stage06 初始任务是否完整；
- self-check findings；
- public leakage/placeholder；
- evaluator coverage；
- Stage07 scientific decision；
- Stage07 transport repairs；
- final Gate 状态；
- 运行错误和实际原因。

## 3. 执行记录

| 时间 | 阶段 | 修改/测试 | 结果 | Git |
|---|---|---|---|---|
| 2026-08-26 | P1 | Prompt 重构 | 已完成；合成和转换 prompt 不再出现内部阶段身份，输入闭合先于任务生成 | 本轮提交 |
| 2026-08-26 | P2 | Bootstrap 边界 | 已完成；删除 public scope/complexity 投影、scaffold prose 和通用 rubric 模板 | 本轮提交 |
| 2026-08-26 | P3 | Input closure | 已完成；显式 closure 与既有等价字段共用一套 selected-input 合同 | 本轮提交 |
| 2026-08-26 | P4 | Gate/evaluator | 已完成；加入格式读取、private-field/placeholder、binding field/comparison 检查；tolerance 质量为 diagnostic | 本轮提交 |
| 2026-08-26 | P5 | 定向回归 | v9/v10/v13/v14/v15/v16 共 57 项通过；更大历史集合 219 项通过、19 项为既有 paper-id/resume/legacy fixture 不兼容 | 本轮提交 |
| 2026-08-26 | P6 | 一致性审计 | 已完成代码级审计；未新增 Agent、retry、论文特例或 human-review 标签 | 本轮提交 |
| 2026-08-26 | P7 | 十篇论文测试 | 前两轮用于发现终局审计和 Gate 反馈闭环缺陷；v16.1 修复后启动干净重跑 | 进行中 |

## 6. P7 前置回归：Stage07 终局写入缺陷

### 6.1 发现

`paper_308bbee002d4560c` 的 Stage07 Agent 调用成功（11 次调用、无 stderr、`agent_run.status=succeeded`），但只把
“pre-edit scientific audit freeze”写入 `outputs/stage07_audit.json`，随后直接结束。该对象将所有可修复检查列为
`repairable`，并明确写着 coordinate parsing、binding reconciliation、public scan 和 Gate 尚未执行；编排器因此把
模型返回的 `objective_failure_retryable` 当作终局失败。这里没有 API、harness 或文件系统故障，根因是 prompt 把一个中间审计检查点设计成了和终局回执相同的文件/结构。

### 6.2 修复

提交 `7756998 fix(stage07): require terminal audit after repairs`：

- Stage07 prompt 改为“先检查但不写终局文件 → 完成 source-backed 修复 → 运行 self-check/Gate → 只写一次完整
  `stage07_audit.json`”；明确禁止把 pre-edit/repairable findings 对象作为终局响应；
- 保留科学拒绝和真实运行故障的语义边界，不用代码标签掩盖未完成修复；
- 修复 Stage06 prompt 的 `private private reference` 笔误；
- 增加 prompt 回归断言，确保该中间态描述不会回归。

### 6.3 另一项科学质量回归

`paper_3590deded767345e` 在 v16 Stage06A 因“坐标解析损坏”科学拒绝，但 v15 rerun3 的 Stage07 曾依据 SI layout
恢复 5 个氮原子字段并成功发布。v16 Agent 已查看 `pypdf_layout.txt`，但未继续执行 source-backed 恢复，过早把 parser
异常等同于 source absence。该现象不是 Gate 误阻断，而是 input-closure 工作流执行不足；后续十篇重跑需单独统计并对比
`derived_coordinates/index.json`、layout fallback 和 Stage07 修复证据。代码不应猜测原子或化学结构，改进重点应是 prompt 中的
恢复顺序/预算和 Agent 是否真正完成恢复后的闭合检查。

### 6.4 Stage06 合成自查未闭环

第二轮 `paper_308bbee002d4560c` 的 self-check 与 external Gate 都返回同一组 18 个 blocking findings，说明两套
Gate 语义已经一致。主要问题是 scoring rule 使用了非合同形状（一个 rule 同时列出多个 key point/conclusion、field 不是
JSONPath、缺少 comparison），并把 package 内的 `paper_route.md`/`workflow_spec.json` 当成 evaluated-Agent 必交的
route-fidelity evidence。Agent 只使用 31/120 次工具调用，收到 exit code 1 和完整 JSON findings 后没有执行修复，而直接写了
`constructed` receipt。因此根因不是额度不足、external Gate 覆盖 self-check 或 validator 死规则，而是 prompt 没有把
“Gate 的非零校验返回是可修复反馈，最后一次失败不得成功退出”说成明确的终局工作流。

v16.1 对此只修改 Agent 工作说明，不新增 orchestrator retry/replay 或强制修复：

- 给出 minimal rule 的 `reference_id`、JSONPath field、comparison 和 required submission artifact 约束；
- 明确 Gate exit code 1 是正常验证反馈，必须在下一次 workspace call 修复并重跑；
- 明确最后一次 self-check 为 failed 或仍有 blocking finding 时不得返回 `constructed`；
- Stage07 同样把完整、具体、可执行的 scoring rules 作为批准前条件，但 tolerance 的科学取值和格式质量仍只做诊断。

新增 prompt 回归后，v9/v14/v15/v16 定向集合共 31 项通过，另有 5 项 Stage06/Stage07 工作流 prompt 回归通过。

### 6.5 Reproduction helper 与 Gate 的 public/private 冲突

v16.1 第三轮的 `paper_308bbee002d4560c` 证明 self-check/external Gate finding 已一致，但又暴露出更早的 helper
validator 冲突：`validate_reproduction.py` 要求 public `task_info.json`/`task_spec.json` 含有 private
`workflow_scope` 和 `complexity_profile`，而 shared Gate 正确地以 `public_private_field_present` 阻断它们。Agent 先删掉
private 字段，helper 报错后又将其加回，最终不可能同时满足两个合同。该冲突也解释了为什么仅强化 self-check prompt 仍不能
稳定闭环。

修复保持单一 public/private 语义：

- reproduction helper 不再要求 private review 字段，并在发现这三个 private key 时直接给出与 Gate 同类的泄露错误；
- public complexity/scope 仍保留在 private `workflow_review.json` 和 receipt，不回填 public metadata；
- 合成 prompt 明确 `process_rubric.json` 是顶层数组，并给出通用 `route_fidelity` row，证据只能引用 required submission
  artifact；这解决 transport shape，不引入论文科学关键词或固定评分值；
- 新增 helper 行为测试：干净 public projection 通过，加入 private field 后失败。

修复后 v9/v14/v15/v16 定向集合共 32 项通过，5 项工作流 prompt 回归继续通过。第三轮已停止以避免继续产生受矛盾
validator 污染的输出；下一轮必须使用新 workspace 重新运行同十篇。

## 4. 最终一致性标准

只有同时满足以下条件才进入十篇论文测试：

- prompt 不再向模型暴露内部阶段职责；
- 输入闭合位于任务生成之前；
- public metadata 不含 private workflow/evaluator 内容；
- 无 scaffold placeholder；
- evaluator 五文件结构和 rule coverage 完整；
- Gate 的阻断/diagnostic 边界与方案一致；
- 没有新增 Agent、retry/replay、论文特例或 human-review 标签；
- 定向回归测试通过。

## 5. 代码级一致性审计

- Prompt：科学目标选择 → selected-workflow 最小输入 → input closure → 完整 public/private 文件 → shared self-check，顺序与方案一致。
- Public/private：`workflow_scope`、`complexity_profile`、Ground Truth 和 scoring metadata 不再由 bootstrap/canonicalization 投影到 public JSON；Gate 会阻断再次泄露。
- Input closure：代码只读取 Agent 声明的 closure 和资产，不生成结构、不补化学状态、不扫描论文分支。
- Evaluator：五文件仍是权威来源，四种 rule type 不变；规则必须覆盖 reference、具有 target/expected、JSONPath/document binding 和 comparison。
- Tolerance：缺失仍阻断；非标准但非空的 authored 表达生成 `scoring_rule_quality_tolerance_format` diagnostic，不改变 Gate 通过状态。
- Gate 一致性：Agent workspace 安装的 self-check 与外部 Gate 都使用 `phase_gate.py` 及同一 `evaluator_reference.py`。
- 未引入：新 Agent、retry/replay、论文关键词、论文 ID 特例、`human_review_required`。

历史大集合中的失败主要来自此前已经取消兼容的 `task_pair_id` fixture、已废弃的第一层 recovery/resume 行为和旧 receipt/schema 断言；它们不属于 v16 新合同，也没有通过恢复旧字段或旧 resume 来规避。P7 以真实十篇论文输出验证当前合同。

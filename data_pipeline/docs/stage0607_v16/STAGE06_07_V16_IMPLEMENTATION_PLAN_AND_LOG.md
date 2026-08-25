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
| 待执行 | P7 | 十篇论文测试 | 等待代码提交后启动并持续监控 | 待提交 |

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

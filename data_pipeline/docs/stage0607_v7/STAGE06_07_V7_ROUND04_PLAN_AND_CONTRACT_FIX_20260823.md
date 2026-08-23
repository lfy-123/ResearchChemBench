# Stage06/07 v7 Round04：Hidden evaluator contract 闭合与回归计划

日期：2026-08-23
基线 commit：`675ee7b docs(stage06-07): plan v7 round3 prompt regression`
迭代范围：仅 Stage06/07 的通用 transport、schema、机械可观察性；不修改 Stage00–05 结果。

## 1. 本轮目标

Round03 的三组同样本运行暴露了一个可复现的合同缺陷：Stage06/07 允许 Agent 使用
`kind`、`numeric_tolerances` 向量和旧 binding 别名，但 Stage07 evaluator dry-run 只做
Pydantic/路径形状检查，因而可能把没有可执行 `canonical_projection`/`comparison` 的
hidden profile 判为通过。Round04 只解决这条通用运输链，不把科学语义猜测塞进代码。

本轮要保证：

1. typed acceptance profile 的必要字段可被确定性检查；向量容差保持逐字段表达；
2. `applies_to_modes` 先于 profile/binding 检查生效，单 mode profile 不污染另一 mode；
3. 旧 transport 别名可安全投影到 canonical 字段，但缺失的科学映射仍报告为 finding；
4. Stage06A 的 task-pair handoff 只做窄合同检查，不要求 Stage06B 尚未生成的 autonomous 树；
5. Stage07 最终 artifact 出口和 pre-publish gate 使用同一 syntax-only normalizer，并记录哈希
   provenance；
6. Agent 的科学结论、target、unit、comparison 和 canonical projection 不由代码生成。

## 2. 问题归类和处理边界

### 代码缺陷（本轮修复）

- evaluator dry-run 未检查非空 Ground Truth 下的 typed profile 完整性；
- profile applicability 未在检查前过滤；
- hidden contract 的 legacy type/binding 别名没有统一的最终运输投影；
- Stage07 finalizer 的 hidden normalization 没有统一 provenance 出口；
- Stage06A active builder 复用了过宽的 pair validator，存在把 Stage06B 责任提前变成重试的风险；
- `document_target` 旧别名未显式标记 document binding，可能被误当作结构化 JSON 字段；
- Stage06A 缺 reproduction submission contract 时，不能用空 required-path 集合制造
  `artifact_not_required` 的误导 finding。

### Prompt/Agent 责任（本轮不以代码替代）

Stage06 hidden-reference prompt 和 Stage07 audit prompt 已要求每个适用 mode 的
`mode_submission_bindings`、`canonical_projection`、`comparison`。缺少这些科学映射时，
代码只阻断并给出可修复 finding；由 Stage07 Agent 根据源证据补齐，不能自动猜测单位、
比较运算、字段语义或答案。

### 模型/源材料问题（本轮不归因于代码）

论文代表性、输入坐标/参考态缺失、软件不可用、模型不能从正文恢复映射，以及模型选题偏离
论文主线，仍由 Stage06/07 的科学判断和源材料决定。它们不是本轮 mechanical gate 的
硬编码规则。

## 3. 代码修改计划

### 3.1 Stage06 typed contract helper

在 `validation.py` 中复用 `acceptance_profile_type_findings`：

- 检查标准 profile type 和必要 target/tolerance/proposition/artifact 形状；
- 接受显式 `numeric_tolerances` map，验证每个值为有限非负数；标量 tolerance 同样检查有限性和非负性；
- 不推断 unit、target 或科学比较。

### 3.2 Stage06 syntax-only normalizer

在 `stage.py` 中：

- 将 `kind`/legacy type 投影为 canonical `type`；
- 将 `artifact`、`field`、`projection`、`comparison_type` 等纯运输别名投影为
  `artifact_paths`、`observed_fields`、`canonical_projection`、`comparison`；
- 从显式 `*_atol`/`*_rtol` 收集向量容差而不压成一个数；
- 从 owner truth 继承明确的 mode scope；
- `binding_type=document` 或 `document_target` 只标记文档绑定，不生成结论。

### 3.3 Stage06 hidden-reference prompt 对齐

原 prompt 同时要求“每个 profile 必须有 shared `submission_binding`”和 mode matrix，
容易让模型在模式特定场景下产生含义冲突的双字段。仅做一处通用措辞澄清：同表示使用
shared binding，表示随 mode 变化时使用 `mode_submission_bindings`，每个适用 mode 行
都必须闭合；不增加任何论文或评分特例。`STAGE06_HIDDEN_VERSION` 更新为
`v5-stage06-hidden-reference-round4-20260823`。

### 3.4 Stage06A 窄 handoff validator

active `task_pair_builder` 只验证 hidden 文件可读、profile typed shape 和已有 binding
合同；不要求 autonomous 目录、Stage07 审计字段或 Stage06B 转换结果。缺少 reproduction
submission contract 时不将空路径集合当作 required-file 白名单。

### 3.5 Stage07 gate/finalizer

- pre-publish gate 在 evaluator dry-run 前执行同一 syntax-only normalizer；
- 仅检查当前 mode 适用的 profile；
- 非空 Ground Truth 下，缺 profile/binding/projection/comparison 均为机械 finding；
- finalizer 和 gate 合并 `orchestrator_normalizations.json`，记录 before/after SHA-256；
- Agent 自报字段继续存为 `agent_observed_*`，不冒充 orchestrator 状态。

## 4. 回归测试矩阵

新增 `tests/test_stage0607_v7_round04_contracts.py`，覆盖：

- type alias 和 vector tolerance 保留；
- `document_target` 文档绑定投影；
- reproduction-only/autonomous-only profile 过滤；
- shared profile 两个 mode 都检查；
- malformed typed profile 不再被 gate 判为 passed；
- Stage06 hidden validator 接受合法单 mode scope；
- Stage06A handoff 不要求 autonomous tree；
- finalizer provenance 合并且不覆盖既有记录。

## 5. 验收标准

- 既有 Stage06/07 测试全部通过；
- Round03 malformed artifact 明确 `failed`，且 finding 指向缺失映射；
- canonical valid artifact 仍 `passed`；
- 缺语义 profile/projection 的 artifact 仍 `failed`，不能被 normalizer 掩盖；
- 不出现论文、分子、固定数字、固定软件或固定文件名特例。

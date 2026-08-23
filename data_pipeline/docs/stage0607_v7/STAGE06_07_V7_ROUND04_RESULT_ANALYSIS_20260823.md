# Stage06/07 v7 Round04：结果、回放与剩余问题

日期：2026-08-23
对应计划：[Round04 plan](STAGE06_07_V7_ROUND04_PLAN_AND_CONTRACT_FIX_20260823.md)

## 1. 实施内容

本轮完成了计划中的通用修复：

- `src/stages/stage06_task_builder/validation.py`
  - 新增 typed acceptance profile 形状检查；
  - numeric vector/标量 tolerance 逐字段检查有限性和非负性；
  - 原 profile 检查复用该 helper。
- `src/stages/stage06_task_builder/stage.py`
  - 增强 hidden contract syntax normalizer（type、scope、binding aliases）；
  - `document_target` 识别为文档绑定；
  - task-pair builder 接入窄 transport validator；
  - 缺失 reproduction submission contract 时不伪造 required-path mismatch；
  - 删除本轮中未使用的 `_MODE_BINDING_NAMES` 死代码。
- `src/stages/stage06_task_builder/prompts.py`
  - 澄清 shared binding 与 mode matrix 的互斥选择，避免 prompt 自相矛盾；
  - `STAGE06_HIDDEN_VERSION` 更新为 `v5-stage06-hidden-reference-round4-20260823`。
- `src/stages/stage07_task_judge/validation.py`
  - pre-publish evaluator dry-run 先按 `applies_to_modes` 过滤；
  - 对非空 Ground Truth 检查 profile type、binding、projection、comparison；
  - final transport normalization 和已有 provenance 合并。
- `src/stages/stage07_task_judge/stage.py`
  - finalizer 在 approved artifact 出口运行同一 normalizer，并记录哈希 provenance；
  - implementation version 更新为 `v13-hidden-contract-transport-round4-20260823`。

没有修改 Stage06/07 的科学目标选择、软件能力判断、答案泄漏规则或任何论文特例；本轮
唯一的 prompt 改动是 transport 合同术语对齐。

## 2. 自动化测试

命令：

```text
PYTHONPATH=. pytest -q tests/test_stage0607_agents.py \
  tests/test_stage0607_v5_contracts.py \
  tests/test_stage0607_v7_round04_contracts.py
```

结果：`189 passed`。

新增的 9 个回归用例证明：

1. alias/vector profile 可规范化且不丢失多字段容差；
2. reproduction-only 和 autonomous-only profile 不会互相触发 gate；
3. shared profile 在两个 mode 都经过检查；
4. 缺 `canonical_projection`/`comparison` 的 profile 会阻断发布；
5. Stage06A handoff 不会因为尚未存在 autonomous tree 而失败；
6. Stage06 hidden validator 接受显式单 mode scope；
7. finalizer 保留已有 provenance，并追加本轮 normalization 记录；
8. hidden-reference prompt 明确 shared binding 与 mode matrix 的选择边界；
9. 非有限/负的标量 tolerance 会被拒绝。

另行执行 `python -m compileall -q` 和 `git diff --check`，均通过。
全仓库回归 `PYTHONPATH=. pytest -q` 结果为 `576 passed`。

## 3. Round03 artifact 回放

为避免修改原始 runs，先复制三个审计 artifact 到临时目录，再使用当前代码执行
`stage07_mechanical_pre_publish_check`：

| 回放样本 | 原始来源 | 当前 gate | 主要观察 |
|---|---|---|---|
| malformed | DeepSeek→DeepSeek，`paper_d2cba483b776cfb7` | `failed` | 19 个 profile 的 legacy type/binding 被规范化，但仍明确报告缺 `canonical_projection`/`comparison`；不再误报 passed |
| canonical | DeepSeek→GPT，`paper_d2cba483b776cfb7` | `passed` | 适用 mode 的 typed profile 和 binding 完整，无 mechanical finding |
| incomplete semantic | GPT→GPT，`paper_1d3ae60b0873aff0` | `failed` | 缺语义 propositions 和 projection 仍被阻断，normalizer 没有替模型补答案 |

回放还确认 mode-specific profile 的“不适用”只进入 diagnostics，不进入 findings；
这修复了 Round03 中 reproduction 被检查 autonomous profile、反之亦然的风险。

## 4. 问题归因

### 已解决的代码问题

Round03 的关键代码 bug 是 gate 只看结构/路径而不看 typed evaluator contract，导致
malformed hidden profile 可能发布。本轮已用回归测试和真实 artifact 回放复现并修复。

### 仍需由 Stage07 Agent 处理的问题

回放中剩余的 `canonical_projection`、`comparison`、semantic proposition 缺失是科学
映射缺失，不应由代码猜测。Stage07 prompt 已明确要求逐 mode binding matrix 和显式
projection/comparison；下一次真实模型运行若再次产生这些 finding，应让 Agent 修复或
返回明确机械阻断，而不是放宽 gate。

### 不属于本轮代码问题的问题

论文计算主线代表性、输入闭合、软件缺口、模型选择能力和 source evidence 不足仍需按
Stage06/07 科学角色审计。合理拒绝不等于管线 bug，本轮没有提高科学批准率作为目标。

## 5. 结论与下一步

Round04 达到本轮合同目标：机械 gate 不再把 malformed evaluator contract 当成可发布，
同时不误阻断 canonical valid contract，也不要求 Stage06A 提前完成 Stage06B。下一轮如
需继续，应优先用一次新的同模型/跨模型小样本运行观察 Agent 是否能根据这些 finding 自行
补齐 binding；若仍失败，应归类为 prompt 执行或模型能力问题，不能继续增加论文特例规则。

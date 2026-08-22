# Stage06/07 v6 Round 2：科学闭合、映射审计与三种模型配置

日期：2026-08-22

## 1. 基线与上一轮证据

本轮基于 v6 Round 1 的双模型结果：

- DeepSeek/DeepSeek：5 篇全部完成，4 篇 `approved_with_repairs` 发布，1 篇科学拒绝；机械阻断 0，schema load failure 0。
- GPT-5.6 Sol（Pro reasoning mode）/GPT：5 篇全部完成，1 篇发布，4 篇科学拒绝；机械阻断 0，schema load failure 0。

样本不重叠，因此发布率不用于比较模型优劣。逐篇轨迹只支持以下通用问题：

1. Stage06A 有时在 `workflow_review` 中保留未解决的源控制字段，却仍输出可交接的候选状态；这是 Prompt 状态语义不够单一的问题。
2. Stage07 有时把“形状有效的 binding”当成“语义映射闭合”，尤其是在公共匿名 key 与私有 canonical key 不同的任务中；这是 Stage07 Prompt 审计不够明确的问题，不能用机械 gate 推断科学语义。
3. Stage06 handoff 记录读取 `workflow_scope.kind`，而模型可合法输出合同中的 `workflow_scope.scope_kind`，导致 `workflow_scope_kind: null`；这是低风险通用运输元数据 bug。
4. GPT 轨迹中的 `jq: command not found` 是工具遵循/模型能力问题，不加入论文特例或代码规则。

## 2. Round 2 修改范围

### 2.1 Stage06A Prompt

- 明确：只有必要科学输入、源控制状态、路线和目标链条均已闭合时才能使用 `candidate_ready`。
- 仅格式、binding、披露和辅助校验问题可以交给 Stage07 修复；不能把未解决科学事实作为“临时草稿”交给 Stage07 猜测。
- 保留整篇主线优先和中心性审查，不新增论文、分子、软件、数字或固定关键词规则。

### 2.2 Stage07 Prompt

- 在最终审计表中明确“选定流程必须直接支撑论文最终计算主张”，不能因“在已闭合候选中最容易构建”而发布外围支撑流程。
- 明确 `source_constrained_construction` 不自动等于闭合；存在未修复的源控制字段时不得批准。
- 在 mode-specific binding 审计中要求比较公共 alias/key domain 与 hidden canonical domain；两者不同必须在 `canonical_projection` 或 mode binding 中逐项列出映射。
- 这些要求仍由 Agent 根据正文/SI 判断，代码不执行科学中心性、物质平衡、TS 或溶剂裁决。

### 2.3 代码与批量测试运输层

- Stage06 handoff 的 scope 投影兼容读取 `kind` 和 `scope_kind`，只修复记录可追踪性，不改变科学决策。
- 批量脚本增加独立的 Stage06/Stage07 模型、endpoint、API key 环境变量和 reasoning 参数；默认行为保持单模型不变。
- 不修改 mechanical gate 的科学责任边界。

## 3. 三种可比测试配置

从同一 Stage05 通过集合随机抽取 5 篇，记录随机种子并将相同 5 篇同时提交到三个独立输出目录：

1. DeepSeek → DeepSeek：Stage06A/06B 与 Stage07 均使用 `deepseek-v4-pro-0813`。
2. GPT → GPT：Stage06A/06B 与 Stage07 均使用 `gpt-5.6-sol`，`reasoning.mode=pro`。
3. DeepSeek → GPT：Stage06A/06B 使用 `deepseek-v4-pro-0813`，Stage07 使用 `gpt-5.6-sol`，`reasoning.mode=pro`。

三组使用 Codex harness、high effort、相同 Prompt/代码版本和相同并发设置，并在同一批次启动。这样可以区分 Stage06 选题/构建能力与 Stage07 审计/修复能力；不能把单篇科学拒绝当作 Prompt 缺陷。

## 4. 验收与归因

- 代码：全量测试、批处理参数测试、`workflow_scope_kind` 投影测试、无 schema load failure、无静默状态丢失。
- Prompt：跨至少两个模型或两个阶段配置重复出现的同类错误，才驱动下一轮修改；单模型/单论文错误记录为模型能力或源材料问题。
- 科学任务：逐篇对照正文/SI 判断整篇主线优先、核心子流程中心性、输入闭合、软件缺口登记和公共/私有映射。
- 不以发布率为唯一目标；科学拒绝和 `conditional` 软件状态在证据充分时是正确结果。

若三组结果仅出现模型特有差异，保留 Prompt 不变并在模型比较中记录；若出现跨配置共性问题，再进入 Round 3，避免为单篇论文增加规则。

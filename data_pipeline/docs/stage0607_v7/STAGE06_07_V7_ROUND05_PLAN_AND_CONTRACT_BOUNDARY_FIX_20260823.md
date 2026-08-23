# Stage06/07 v7 Round05：阶段边界与 hidden contract 无损检查

日期：2026-08-23  
基线 commit：`22ea9df fix(stage06-07): close hidden evaluator transport contract`  
迭代范围：仅 Stage06/07 的通用 transport、阶段边界和发布可观察性；不修改 Stage00–05，不加入论文、分子、软件或固定答案特例。

## 1. 本轮目标

Round04 的专项测试和边界回放已经证明 malformed evaluator contract 会被阻断，但进一步用中性 fixture 复核发现四个可复现的通用缺口：

1. Stage06A 的窄 handoff validator 仍可能要求 Stage06B 尚未生成的 autonomous mode binding；
2. hidden syntax normalizer 会静默删除 orphan profile，或把一个被多个 Ground Truth 共用的 profile 复制成多个 profile；
3. shared `submission_binding` 与 `mode_submission_bindings` 同时存在时没有显式歧义状态；
4. truth/profile mode scope 不闭合，以及 ready hidden contract 没有任何 Ground Truth 时，Stage07 gate 仍可能放行。

本轮只修复这些可确定的合同问题。代码不判断科学重要性、答案、单位、比较运算或论文代表性。

## 2. 处理边界

### 代码负责

- 在 Stage06A handoff 只检查当前阶段需要的 binding 行；保留已存在的其他 mode 行的形状检查，但不把待转换行缺失变成 Stage06A 重试；
- 在任何 syntax normalization 之前检查 profile ownership、scope 和 binding 来源是否有歧义；发现结构问题时保留原始合同并报告 finding；
- 在 Stage07 pre-publish 阶段确认每个适用 Ground Truth 都有适用的 profile/binding，且 ready 合同至少有一个 Ground Truth；
- 将这些 findings 写入既有 mechanical report/provenance，不新增复杂评分规则。

### Agent/Prompt 负责

- 选择完整论文路线或有证据的核心子流程；
- 判断 Ground Truth 的科学语义、代表性、输入闭合和 mode 适用范围；
- 补齐 `canonical_projection`、`comparison`、单位、目标和命题；
- Stage06B 的答案盲脱敏。

## 3. 最小修改计划

1. 给 acceptance binding 检查增加可选的 `required_binding_modes`，Stage06A 只要求 reproduction 行；Stage07 最终 gate 保持全 mode 严格检查。
2. 增加 paper-neutral hidden contract preflight：检测 orphan、重复 owner、shared/matrix 并存、truth/profile scope 不一致和 ready 空 Ground Truth；不自动猜测或删除科学字段。
3. Stage06A、legacy hidden phase、Stage07 finalizer/gate 在 normalization 前先运行 preflight；有结构 finding 时保留原始文件，避免 normalizer 掩盖问题。
4. 增加 Round05 回归矩阵，覆盖合法 shared/matrix、Stage06A partial matrix、orphan、duplicate owner、binding ambiguity、scope mismatch 和空 Ground Truth。

## 4. 验收标准

- Round04 的 189 个 Stage06/07 专项测试和全仓库测试继续通过；
- 既有合法 alias/vector、single-mode、document binding 和 canonical artifact 不改变结果；
- Stage06A partial matrix 不再因 autonomous 缺失行失败；
- orphan/duplicate/ambiguous/scope-invalid/empty-ready hidden contract 明确失败且原始 profile 不被静默删除；
- Stage07 对所有适用 mode 的完整矩阵仍严格阻断；
- 没有新增论文、分子、软件、固定数值或科学裁决规则。

## 5. 测试安排

代码回归通过后，使用相同 Prompt、Codex、high reasoning，提交一组小规模三组合测试：DeepSeek→DeepSeek、GPT→GPT、DeepSeek→GPT。模型结果只用于判断 Agent 是否能处理新的结构 finding；合理科学拒绝仍是有效终态，不以发布率为唯一指标。


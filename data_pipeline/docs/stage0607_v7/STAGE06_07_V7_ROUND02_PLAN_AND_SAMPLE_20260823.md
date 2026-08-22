# v7 Round 02：阶段组合对照计划

日期：2026-08-23  
依据：Round 01 结果分析与 v7 十五轮目标  
本轮不修改 Prompt 或代码；先用对照实验判断差异来自 Stage06 选题、Stage07 审计，还是模型能力。

## 1. 对照设计

同一批 5 篇 Stage05 通过论文分别运行三种组合：

1. DeepSeek→DeepSeek：Stage06A/06B/Stage07 均 `deepseek-v4-pro-0813`；
2. GPT→GPT：Stage06A/06B/Stage07 均 `gpt-5.6-sol`；
3. DeepSeek→GPT：Stage06A/06B 使用 `deepseek-v4-pro-0813`，Stage07 使用 `gpt-5.6-sol`。

三组使用同一 Prompt、Codex harness、`reasoning_effort=high`、并发 5 和同一来源快照。这样可以区分：

- Stage06 选题/输入闭合差异；
- Stage07 科学审计与修复差异；
- 两阶段组合带来的协同或冲突。

## 2. 随机样本

来源 Stage05 通过集合共 582 篇；随机种子 `20260825`；从排除 Round 01 十篇样本后的集合中抽取，本轮三组共用以下 5 篇：

`paper_1c0c90e7aa74498c`、`paper_7365b45a306d8947`、`paper_4ca4735bcf490d5a`、`paper_8f891f94d53054e4`、`paper_b79009dc92a2bc4e`

## 3. 结果目录

- `runs/stage06-07-v7-round2-same5-deepseek-deepseek-20260823`
- `runs/stage06-07-v7-round2-same5-gpt-gpt-20260823`
- `runs/stage06-07-v7-round2-same5-deepseek-gpt-20260823`

## 4. 分析规则

完成后逐篇比较 Stage06 handoff 是否一致、Stage07 是否识别同一科学缺陷、修复是否保持原问题语义、两个模式是否隔离、机械状态是否与发布状态一致。只有同一论文/同一阶段在多个组合中重复出现的通用错误，才进入 Round 03 的 Prompt 或代码修改；单个模型的漏判记录为模型能力差异。

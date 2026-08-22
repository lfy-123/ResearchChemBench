# v7 Round 01：阶段协议 Prompt 调整与双模型回归计划

日期：2026-08-23  
Prompt 基线 commit：`9ee69f5`  
完整回归：567 passed

## 修改范围

本轮只调整角色 Prompt 的执行顺序和完成判定：

- Stage06A：`DECISION PROTOCOL`，先作 scope 决策，再写 provisional handoff，最后按 unresolved fields 决定状态；
- Stage06B：`CONVERSION PROTOCOL`，先分类 remove/preserve/uncertain，再做答案盲转换，最后复核公共面；
- Stage07：`AUDIT PROTOCOL`，先冻结科学审计，再做证据支持的修复，最后重新核对树、binding 和 receipt；
- 删除重复的 Stage06A 顺序说明；没有加入案例、固定化学规则、示例答案或模型专用分支。

## 随机样本

Stage05 最新通过集合：582 篇。随机种子：`20260823`。两组样本互不重叠：

DeepSeek 组：

`paper_0b4e294e099f72da`、`paper_584ac85fd9f0b344`、`paper_5ab87c809ec4a7d0`、
`paper_94b0a8ae694590ea`、`paper_a55b812fd43d286d`

GPT 组：

`paper_4b4e0bec6df820fc`、`paper_6ff878fdedc4533d`、`paper_761a1e321d9bc798`、
`paper_b5c446c7067dd511`、`paper_d1135c5a2aaf5d4b`

## 当前提交状态

尚未提交。当前 GPT API `/v1/models` 没有 `gpt-5.6-pro`，因此没有使用 `gpt-5.6-sol` 冒充该模型。获得可用的 `gpt-5.6-pro` endpoint 或明确替代模型后，使用相同 Prompt、Codex harness、high reasoning、并发 5，同时提交两组。

2026-08-23 的直接 API 探测也返回 HTTP 404：`model_not_available`，并明确说明该模型不在当前 API key 的可用范围内。该证据将本轮状态分类为外部配置阻断，不归因于代码或 Prompt。

截至后续连续复核，`/v1/models` 和直接调用仍给出同一结果。由于 v7 的每轮比较明确要求目标 GPT 模型，不能用 `gpt-5.6-sol` 无标记替代；Round 1 在提交前保持 blocked，待外部模型配置变化后恢复。

## 预定结果分析

逐篇记录 Stage06A scope、Stage06B disclosure、Stage07 audit/repair/decision、机械状态和源材料依据；将差异归因为代码、Prompt、模型能力或源材料，不能以发布率直接评价 Prompt。

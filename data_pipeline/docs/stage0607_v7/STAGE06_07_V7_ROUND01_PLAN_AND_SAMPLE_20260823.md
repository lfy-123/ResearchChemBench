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

## 提交配置

本轮实际模型为 `deepseek-v4-pro-0813` 与 `gpt-5.6-sol`。两组均使用 Codex harness、high reasoning effort、并发 5，且使用相同 Prompt 和同一 Stage05 来源集合；两组样本互不重叠。GPT `/v1/models` 已确认包含 `gpt-5.6-sol`；DeepSeek `/v1/models` 探测在提交前超时，但端点已有同模型任务运行，故按运行结果继续观察，不把超时误判为代码或 Prompt 失败。

结果目录：

- `runs/stage06-07-v7-round1-same5-deepseek-20260823`
- `runs/stage06-07-v7-round1-same5-gpt-20260823`

旧的 `v6-round4` 运行目录仍单独保留，不能混入本轮统计。

## 实际提交记录

2026-08-23 00:46（Asia/Hong_Kong）已同时提交：

- DeepSeek 进程批次：`runs/stage06-07-v7-round1-same5-deepseek-20260823`，Stage06A/06B/07 均为 `deepseek-v4-pro-0813`；
- GPT 进程批次：`runs/stage06-07-v7-round1-same5-gpt-20260823`，Stage06A/06B/07 均为 `gpt-5.6-sol`。

两批均设置 `--harness codex`、`--max-parallel 5`、Stage06/07 `reasoning_effort=high`。提交后两个批处理进程均保持运行并已创建 `batch_status.json`；本节不把尚未完成的中间状态解释为模型或 Prompt 结论。

## 预定结果分析

逐篇记录 Stage06A scope、Stage06B disclosure、Stage07 audit/repair/decision、机械状态和源材料依据；将差异归因为代码、Prompt、模型能力或源材料，不能以发布率直接评价 Prompt。

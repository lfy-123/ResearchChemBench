# Stage06/07 v6 Round 2：三种阶段模型配置提交记录

日期：2026-08-22

## 1. 固定样本

Stage05 通过集合：582 篇；随机种子：`20260872`。为隔离“论文内容”变量，三组使用完全相同的 5 篇：

- `paper_5be4368e659d4b40`
- `paper_9774cf028b321785`
- `paper_75221561972a5c9c`
- `paper_f171fa1f83158f7c`
- `paper_525ba02ec147f066`

## 2. 同时提交的三组

所有组均使用 Codex harness、reasoning effort `high`、并发 5、Round 2 Prompt 和代码提交 `54296c9`。

| 配置 | 结果目录 | Stage06A/06B | Stage07 |
|---|---|---|---|
| 同模型 DeepSeek | `runs/stage06-07-v6-round2-same5-deepseek-deepseek-20260822` | `deepseek-v4-pro-0813` | `deepseek-v4-pro-0813` |
| 同模型 GPT | `runs/stage06-07-v6-round2-same5-gpt-gpt-20260822` | `gpt-5.6-sol`, `reasoning.mode=pro` | `gpt-5.6-sol`, `reasoning.mode=pro` |
| 混合 | `runs/stage06-07-v6-round2-same5-deepseek-gpt-20260822` | `deepseek-v4-pro-0813` | `gpt-5.6-sol`, `reasoning.mode=pro` |

首批三个批次在同一 shell 调用中启动，但在产生终态前发现 Stage06A 新增句中的拒绝枚举笔误（`scientific_reject` 应为正式合同枚举 `scientific_not_constructible`），因此已显式标记为 `CANCELLED`，不纳入分析。

修正后的三批次在同一 shell 调用中重新并行启动，当前使用以下结果目录：

- `runs/stage06-07-v6-round2-retry-same5-deepseek-deepseek-20260822`
- `runs/stage06-07-v6-round2-retry-same5-gpt-gpt-20260822`
- `runs/stage06-07-v6-round2-retry-same5-deepseek-gpt-20260822`

重提交流程进程号为：DeepSeek→DeepSeek `1926314`，GPT→GPT `1926315`，DeepSeek→GPT `1926316`。

## 3. 比较方法

逐篇对比三组的 Stage06 选题/闭合、Stage06B 公共面、Stage07 科学审计/修复/决定、binding 映射和机械发布状态。只有在不同模型配置中重复出现的同类错误，才作为下一轮通用 Prompt 修改依据；单篇或单模型差异归因于模型能力或源材料。

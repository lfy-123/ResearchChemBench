# Stage06/07 v6 Round 1：模型探测与测试提交记录

日期：2026-08-22

## 1. 本轮代码与 Prompt

- Prompt/代码提交：`87ae64d prompt(stage06-07): add model-neutral execution ordering`
- Round 1 调整：Stage06A、Stage06B、Stage07 增加通用执行顺序说明；没有加入论文、分子、软件或固定数值特例。
- 定向回归：173 passed。
- 全量回归：560 passed。

## 2. Stage05 样本

从 Stage05 通过集合中使用随机种子 `20260871` 抽取 10 篇，并固定为两组不重叠样本：

DeepSeek 组：

- `paper_1e565b6f67f458a5`
- `paper_56da7f9591ef00f2`
- `paper_f7ec54ea468f3071`
- `paper_8f891f94d53054e4`
- `paper_d7d81f71aa46298b`

GPT 组：

- `paper_30cec9ecf4782412`
- `paper_8e9141f166ee0a28`
- `paper_4ee9947f568c29ba`
- `paper_ae6c1c97de168e40`
- `paper_3c3d73b8715d5fcd`

Stage05 通过集合当前发现数量为 582 篇。

## 3. 模型/协议探测

本轮目标要求 GPT 组使用 `gpt-5.6-pro`。对当前配置的 GPT endpoint 做了只读 `/models` 探测，并用最小请求验证了模型名：

- `gpt-5.6-pro`：endpoint 返回 `model_not_available`；
- `gpt-5.6`：endpoint 返回 `model_not_available`；
- `gpt-5.6-sol`：请求成功，返回 `gpt-5.6-sol`。

当前本地 endpoint 实际提供 `gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna` 等模型，没有独立的 `gpt-5.6-pro` slug。DeepSeek endpoint 的模型探测在本次 15 秒只读请求中超时，尚未据此判定模型不可用。

因此本轮不把 `gpt-5.6-sol` 静默标记为 `gpt-5.6-pro`。DeepSeek 组先按目标模型提交；GPT 组等待可用的 `gpt-5.6-pro` endpoint 或用户确认后再提交。若后续确认 `gpt-5.6-sol` 是目标 `gpt-5.6` 的实际提供名，必须在结果文档中明确记录为配置映射，而不能伪造模型名。

## 4. DeepSeek 提交配置

- 模型：`deepseek-v4-pro-0813`
- Harness：Codex
- 推理强度：high
- 并发：5
- 两个阶段使用同一模型和同一 Prompt 版本
- 结果目录：`runs/stage06-07-v6-round1-deepseek5-20260822`

## 5. 归因边界

模型 endpoint 不可用属于外部配置/服务状态，不归因于 Prompt 或 Stage06/07 科学代码。两组样本必须使用同一 Prompt 和 harness；在 GPT 组未获得目标模型前，不使用 `gpt-5.6-sol` 结果冒充本轮的 `gpt-5.6-pro` 对照。

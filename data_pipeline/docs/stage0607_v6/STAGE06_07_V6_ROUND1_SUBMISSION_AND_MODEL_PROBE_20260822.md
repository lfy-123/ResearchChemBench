# Stage06/07 v6 Round 1：模型探测与测试提交记录

日期：2026-08-22

## 1. 本轮代码与 Prompt

- Prompt 基线提交：`87ae64d prompt(stage06-07): add model-neutral execution ordering`
- 测试所用通用 harness 修复提交：`d4deb09 fix(harness): support configurable reasoning mode`
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

官方 OpenAI 文档说明 GPT-5.6 的 Pro 是 reasoning mode，而不是独立模型 slug；`gpt-5.6` alias 路由到 GPT-5.6 Sol。因此本轮以 `gpt-5.6-sol` 加 `reasoning.mode=pro` 实现用户要求的 Pro 对照，并在所有运行记录中保留这两个字段，不把模型名写成不存在的 `gpt-5.6-pro`。管线新增了模型无关的可选 `reasoning_mode` 传递，普通模型不设置该字段时行为不变。

## 4. DeepSeek 提交配置

- 模型：`deepseek-v4-pro-0813`
- Harness：Codex
- 推理强度：high
- 并发：5
- 两个阶段使用同一模型和同一 Prompt 版本
- 结果目录：`runs/stage06-07-v6-round1-deepseek5-20260822`

GPT 组：

- 模型：`gpt-5.6-sol`
- Pro 模式：`reasoning.mode=pro`
- 推理强度：high
- Harness：Codex
- 并发：5
- 结果目录：`runs/stage06-07-v6-round1-gpt56sol-pro5-20260822`

## 5. 归因边界

模型 slug 探测结果属于外部协议配置；reasoning mode 传递是通用 harness 兼容修复，不是论文特例。两组样本使用同一 Prompt、代码逻辑、Codex harness、high effort 和可比并发；模型名与 Pro mode 分开记录，后续分析不得把两者混为一个模型变量。

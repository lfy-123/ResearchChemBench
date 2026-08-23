# v7 Round 03：集合/比较充分性澄清后的三组合复测

日期：2026-08-23  
Prompt commit：`507d254`  

## 1. 本轮变更

Round 02 之后只增加一条通用语义澄清：当最终结论依赖系列、成对比较、构象/状态集合或加权聚合时，单个成员只能是中间/支持性计算，除非论文明确把它定义为独立决定性问题；Stage07 必须检查该子流程是否足以回答自己的最终结论。没有增加论文、分子、固定数字、软件、答案或格式特例；代码未改动。

## 2. 三组合和样本

同一批 5 篇 Stage05 通过论文分别运行：

- DeepSeek→DeepSeek；
- GPT→GPT；
- DeepSeek Stage06→GPT Stage07。

随机种子：`20260826`；排除 Round 01/02 已用样本。样本：

`paper_d2cba483b776cfb7`、`paper_efb2d9ec4fdb3b0f`、`paper_108e6a1fb1e8f309`、`paper_1d3ae60b0873aff0`、`paper_849802730178edb8`

## 3. 运行目录

- `runs/stage06-07-v7-round3-same5-deepseek-deepseek-20260823`
- `runs/stage06-07-v7-round3-same5-gpt-gpt-20260823`
- `runs/stage06-07-v7-round3-same5-deepseek-gpt-20260823`

均使用 Codex、high reasoning、并发 5、Round 2 后的同一 Prompt。完成后重点核对：集合/比较结论是否覆盖必要成员、源闭合不足时是否拒绝或合理缩小、Stage07 是否修复代表性问题，以及机械状态是否可解释。


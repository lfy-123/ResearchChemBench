# Stage06/07 v5 Round 18 实施与定向回归记录

日期：2026-08-22

## 1. 本轮范围

本轮先验证 `f6e7f3b` 对 Stage06B recovery budget 的修复，再检查两个此前受影响的论文。测试使用 GPT-5.6-sol、Codex harness、high、并发 2；结果目录为：

`runs/stage06-07-v5-round18-targeted-gpt56sol2-concurrency2-20260822`

## 2. 定向结果

| paper | Stage06 | Stage07 | 判断 |
|---|---|---|---|
| `paper_adde784df62951c6` | `provisional_not_constructible` | `rejected_scientific_unrepairable` | 正确。论文/SI虽给出 Gaussian16 路线和坐标块，但无法可靠把多个坐标 frame 映射到 int-A/int-B/TS/path-b/product，几何敏感的势垒任务不能靠猜测补齐。 |
| `paper_51a03695e1ccb105` | `provisional_constructed`；Stage06B recovery 成功 | `approved_with_repairs`，但 mechanical gate 阻断 | Stage06B 已成功生成完整自主任务树，回执路径和 recovery budget 均正常；Stage07 科学审计和代表性判断完成。阻断原因是 hidden reference 中 `evidence_gate_policy` 和 `managed_computation_policy` 仍为字符串，而 evaluator 合同要求对象。 |

两个 worker 均正常完成，批次为 `COMPLETED`，无 API/进程/transport failure。第一篇的科学拒绝不计为代码缺陷；第二篇的 mechanical block 也不是 gate 误报，而是 Stage07 最终修复/类型复核没有落实 Prompt 要求。

## 3. 本轮 Prompt 修复

提交：`863e76b`。

- Stage06A 明确要求两个 policy 字段始终写 JSON object，不能把说明句直接写成字符串。
- Stage07 最终批准清单要求重新读取 Ground Truth，检查解析后的类型；若 handoff 给出句子，必须放进对象的 `description` 等字段，并在字符串类型出现时先修复再批准。
- 这是通用合同提示，不包含论文、分子、软件或数值特例；代码仍不判断 policy 的科学内容。

## 4. 验证

- Stage06/07 定向测试：`169 passed`。
- 全量测试（显式 `PYTHONPATH=.`）：`556 passed`。
- 修复前一次无 `PYTHONPATH` 的全量命令产生了环境导入错误，重跑后确认不是代码回归。

## 5. 下一步

在该 Prompt 修复后，用 DeepSeek-v4-pro-0813、Codex harness、high、并发 10、随机 10 篇 Stage05 通过论文做下一批回归。逐篇检查完整路线优先级、核心子流程代表性、输入/参考态闭合、软件缺口登记、Stage06B 答案盲转换以及 Stage07 科学/机械状态是否一致。除非出现新的稳定共性问题，不增加 Stage07B；当前 Round 18 只有 1 篇同类简单合同阻断，尚未达到既定启用阈值。

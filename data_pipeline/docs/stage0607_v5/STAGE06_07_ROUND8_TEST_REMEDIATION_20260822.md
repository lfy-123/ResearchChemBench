# Stage06/07 v5 Round 8：限流污染复核与单批次回归

日期：2026-08-22  
代码基线：`f80d5f3`（Round 7 代表性证据字段修复）  
模型/Harness：DeepSeek-v4-pro-0813 / Codex；reasoning `high`

## 1. Round 7 测试结论

Round 7 目录为：

`runs/stage06-07-v5-round7-deepseek10-concurrency10-20260822`

按约定等待超过 30 分钟后，10 个 worker 仍未形成 Stage06A/Stage06B/Stage07 终态。轨迹中多次出现：

`HTTP 429 Too many concurrent requests`（Codex Responses 本地转发端口返回）。

同时，Round 6 目录仍有 10 个 worker 在运行；两个批次共用同一 DeepSeek endpoint，实际并发约为 20，而不是各自声明的 10。该结果是测试编排条件污染，不是论文科学拒绝，也不是 Stage06/07 合同结论。两个批次已停止，原始轨迹保留；`batch_status.json` 标为 `ABORTED_TEST_OVERLAP`。

## 2. 本轮处理

- 不修改 Stage06/07 科学规则或论文特例；Round 7 的代码改动保持在 `f80d5f3`。
- 结束重叠的 Round 6/7 worker，避免继续占用 endpoint 并污染后续测试。
- 在无其他 Stage06/07 批次运行时重新提交单一 10 篇、并发 10 的 DeepSeek 批次。

## 3. 干净回归批次

结果目录：

`runs/stage06-07-v5-round8-deepseek10-concurrency10-20260822`

随机种子：`20260826`；Stage05 source set 不变。提交后按用户要求至少等待 30 分钟，再统一审查终态和逐篇科学代表性。若该批次仍无终态，将把限流/模型服务可用性单独记录为测试基础设施问题，不据此修改 Stage06/07。

## 4. 代码与 Prompt 回归

Round 7 修改后的 Stage06/07 相关测试：`159 passed`（`tests/test_stage0607_agents.py` 与
`tests/test_stage0607_v5_contracts.py`）。截至本记录更新时，全量回归为 `546 passed`
（`PYTHONPATH=. pytest -q`）。本轮尚未发现新的、与论文无关且可复现的 Stage06/07 代码缺陷；
是否需要下一轮修改，等待干净批次的真实 Stage07 产物。

截至 08:14 HKT，Round 8 已产生 8 份 Stage06A `workflow_review.json`，其中已看到的候选均
记录了完整路线优先、候选比较、主张覆盖、资源观察和软件状态；已有 4 份 Stage06A
`construction_receipt.json`，尚未有 Stage07 终态。当前 worker 仍在运行，不能把“尚未形成
终态”解释为科学拒绝或 Stage06/07 合同失败。

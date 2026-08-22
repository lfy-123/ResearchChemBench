# Stage06/07 v5 Round 14 实施与测试记录

日期：2026-08-22

代码基线：`2079eaf`

总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 实施内容

本轮只修改 Stage06A/Stage07 Prompt 与对应合同测试：

- Stage06A：要求按标准单 frame 或 concatenated multi-frame XYZ 保存源坐标；禁止用 aggregate atom count 包装多个结构；IRC/映射路径核对元素组成、原子数、charge 和 mapping。
- Stage06A：被选中 workflow 未计算的 comparison side 只能作为 unscored context，不能成为 computed final Key Point。
- Stage07：修复后重新逐 frame 解析公开资产；IRC 路径必须同 atom set；不同组成只能使用显式平衡的 thermochemical formula。
- Stage07：每个差值执行 symbolic formula、canonical value/order、sign、prose 和 per-mode binding 的代入核对。
- Stage07：资源审计要求展开 branch count、system size 与有依据的 per-branch walltime/memory 观察；禁止仅凭 “high but bounded” 断言可行。
- Stage07：最终批准清单要求 hidden policy 为 JSON objects、route-fidelity criterion 有源证据、toolbox status 与 inventory/gap list 一致。

没有增加论文、分子、软件、固定数值或固定 workflow 特例；代码侧仍不裁决科学化学计量、能量符号或成本。

## 2. 回归结果

- Stage06/07 定向测试：`165 passed`；
- 全量测试：`552 passed`；
- `git diff --check`：通过。

## 3. Stage07B 判断

不启用。Round 13 仅 1/10 因简单合同问题机械阻断，未达到 10 篇至少 2 篇或连续两批重复的触发条件。优先验证 Stage07 的窄最终清单能否消除该问题。

## 4. Round 14 批次

待运行：新的随机 10 篇，`gpt-5.6-sol` high、Codex harness、并发 10。完成后补充逐篇结果和是否停止迭代的依据。

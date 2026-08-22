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

结果目录：

`runs/stage06-07-v5-round14-gpt56sol10-concurrency10-20260822`

配置：随机种子 `20260859`，10 篇，`gpt-5.6-sol` high，Codex harness，并发 10。

终态：10/10 worker 收束；8 篇正常完成，2 篇 Stage06 技术失败。正常完成的 8 篇中，5 篇被科学拒绝，3 篇经修复后批准并发布；没有机械发布阻断。

| 论文 | Stage06/07 结果 | 对照论文后的判断 |
|---|---|---|
| `paper_cdfaaeab9a9494c3` | 科学拒绝 | 正确。五个聚合物的周期 HSE06 主线缺精确周期原子模型、构象/有限到周期映射；有限模型也是 supporting-only 且不闭合。 |
| `paper_fcc3c7f2c46a0fbe` | 科学拒绝 | 正确。核心六分子 descriptor/MEP 与 TDDFT 路线缺可复现计算态；单个 4b 结构验证和 Hirshfeld 分支不能代表主结论。 |
| `paper_552bf59e74da289e` | 科学拒绝 | 正确。828 原子 tetramer 缺坐标和确定性组装/构象选择；拟合替代路线又缺原始曲线与完整模型。 |
| `paper_6818d4d7426cf7a5` | 科学拒绝 | 正确。核心 Ni 过渡态比较虽有坐标，但电荷和多重度/电子态未公开，不能猜测；Stage07 没有被精确数值诱导误批。 |
| `paper_b5c446c7067dd511` | 科学拒绝 | 正确。四个发光体的几何敏感构象态及确定性筛选缺失；孤立芳香基团计算只是 supporting control。 |
| `paper_c23cfabbd34b087f` | 修复后批准并发布 | 科学范围合理：两侧 102/106 原子精确 SI 结构的 TDDFT/前线轨道比较直接支撑光学调控主张；Stage07 修复了错误的 gap binding、脱敏和交付合同。但资源状态仍为 `uncertain`。 |
| `paper_584ac85fd9f0b344` | 修复后批准并发布 | 输入、两对比较、Q-state 数值、差值方向和自主表面基本闭合，完整覆盖论文的四体系计算路线。但四个 122–130 原子体系的优化、Hessian、TDDFT（最高需覆盖约 25 roots）没有可辩护的预算结论，资源状态仍为 `uncertain`。 |
| `paper_8087b0d38cdf6fdf` | 修复后批准并发布 | 20 个精确源结构及能量/光谱两条主线在科学上有代表性；Stage07 正确修复 label/basis 不一致和模式 binding。但 20 次优化加 8 次 TDDFT 未证明能在政策内完成，资源状态仍为 `uncertain`。 |
| `paper_adde784df62951c6` | Stage06 artifact delivery failure | 代码运输缺陷。Stage06B 已完整写出 8 个资产和全部公共文件，只因回执路径少了 `outputs/` 被误判缺失。Round 16 修复。 |
| `paper_51a03695e1ccb105` | Stage06 retryable failure | 代码 Unicode 输入缺陷。pypdf 返回 surrogate code units，UTF-8 layout 写入失败。Round 15 已修复。 |

## 5. 共性判断

### 5.1 已达到预期的部分

- 5 篇科学拒绝均针对中央 workflow 的真实输入态/路线闭合问题；没有为了通过率改选外围任务。
- 软件安装状态没有被当作科学拒绝理由。
- 两个已完成的 Stage06B 转换保持答案盲和中性资产表面；Stage07 能修复 disclosure/binding 后直接发布。
- 机械 gate 没有产生误阻断，Stage07B 触发数为 0。

### 5.2 仍未闭环的共性问题

三篇获批任务全部出现同一矛盾：Stage07 明确写 `resource_status=uncertain`，并承认没有可信的 branch runtime/memory 依据，却留下 `remaining_issues=[]` 并批准发布。这里不是要求代码估算化学成本，而是 Stage07 的最终决策没有服从自己的资源审计结果。

下一轮应只调整 Agent 决策闭环：批准必须有可辩护的资源可行性；若完整路线无法证明可行，应缩到仍然中央、闭合且可辩护的核心子流程；若做不到则科学拒绝。不能添加 atom-count、软件或论文特例 gate，也不能因为论文没有报告 walltime 就机械拒绝所有任务。允许 Agent 根据展开后的分支数、体系规模、方法复杂度、并行依赖和资源政策作保守科学估计并清楚陈述依据。

## 6. Stage07B 判断

不启用。本批没有“科学批准但简单机械合同阻断”的任务，问题是 Stage07 自己的科学资源决策闭环，不属于 Stage07B 的窄 transport 修复职责。

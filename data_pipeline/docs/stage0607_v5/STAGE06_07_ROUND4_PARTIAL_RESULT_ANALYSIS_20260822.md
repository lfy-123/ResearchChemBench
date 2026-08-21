# Stage06/07 v5.1 第四轮 30 分钟结果分析（部分）

批次目录：`runs/stage06-07-v5-round4-deepseek10-concurrency10-20260822`
模型：`deepseek-v4-pro-0813`；Codex harness；high；并发 10；随机种子 `20260822`。

## 1. 30 分钟时的状态

批次仍在运行：10 篇已提交，1 篇完成，9 篇仍在 Agent 计算/审计阶段。按用户要求，本记录不把未完成论文当作失败，也不提前汇总为最终通过率。

已完成论文：`paper_3c89b494a1645491`。

## 2. 已完成论文逐篇审查

### `paper_3c89b494a1645491`

Stage06：`provisional_not_constructible`。Stage07：`rejected_scientific_unrepairable`。该结果符合 v5.1 总目标，而不是代码失败：

- 论文的中心计算路线是 Au-Au 结构的 DFT 优化、AIM/DI 和 NBO 分析；Stage06 先检查完整路线，再检查 AIM-only/NBO-only 两个核心子流程。
- 可见正文/SI/不可变快照均没有起始 Au1·X Cartesian 坐标。AIM/DI/NBO 都依赖几何或波函数，不能用猜测坐标构造“容易包装”的外围任务。
- Stage07 明确记录了输入、参考态、动作/产物和 binding 均无法在不猜测科学事实的前提下闭合，`selected_scope_kind=none_selected`，没有因为缺少软件拒绝；`toolbox_status=available`。
- 没有生成 public task pair，因此没有触发 mechanical gate；这属于可见的科学拒绝，不是“批准后静默丢失”。

判定：该篇体现了完整路线优先、核心子流程兜底、无核心闭合则拒绝三条目标。当前没有发现代码或 prompt 的共性缺陷。

## 3. 本轮代码变更的验证状态

本轮代码提交：

- `4b157b5`：结构化 `critical_failures` evaluator projection、`$..` 受限路径归一化、prompt 反例和回归测试；
- `7bdd5d6`：路径归一化进一步要求显式候选路径在至少一个适用 mode 的结果 schema 中为 `present/open`，降低误改合法递归语义的风险。

批量运行轨迹还暴露出批处理脚本的状态语义问题：CLI 进程即使返回 0，Stage06 仍可能记录 `artifact_delivery_failure_retryable` 并跳过 Stage07。已在未重启当前批次的代码中增加 `late_stage_run_summary.json` 读取，将此类内部失败标为批次 `FAILED`；科学拒绝仍保持 `COMPLETED`。

完整批次中 `paper_35349e84bdec7e59` 具体触发了该问题：Stage06A 构建成功，Stage06B 返回 `needs_conversion_retry`，但由于 converter 状态未接入 `_run_phase` 的恢复循环，最终以 `autonomous_conversion_failed` 结束，Stage07 未运行。这个结果不是科学拒绝，也不是“论文不可用”；代码已修复为在该显式状态下进入有限重试。当前批次使用的是修复前进程，故其 `batch_status.json` 仍记录 `exit_code=0/completed`，应按 `late_stage_run_summary` 后验解释。

回归测试：Stage06/07 154 passed；管线相关 259 passed。

## 4. 尚不能下结论的项目

剩余 9 篇需要完成后再逐篇检查：

- 完整计算路线是否优先于容易构建的外围子流程；
- 降级是否有成本/关键输入/闭合证据，且是否选择了最重要子流程；
- 软件缺口是否登记但没有造成科学拒绝；
- Stage06B 是否保持答案盲和物理边界；
- Stage07 是否独立复核代表性、输入闭合、mode-specific binding 和公共答案边界；
- 是否还出现非 `$..`、非结构化 critical failure、非 hidden identity 的重复合同问题。

在剩余任务完成前，不启用 Stage07B，也不追加论文特例规则。

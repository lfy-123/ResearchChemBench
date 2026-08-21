# Stage06/07 v5 第0轮基线与第1轮计划

## 基线

- Git HEAD：`1851c4e`（`docs(stage06-07): record round9 role audit and final projection fix`）。
- 相关源码：`src/stages/stage06_task_builder/`、`src/stages/stage07_task_judge/`。
- 已知回归：上一批 20 篇中 17 篇科学批准、3 篇科学拒绝、16 篇发布、1 篇因适用 mode 未过滤而机械阻断；科学拒绝主要对应源材料不可执行，不计为代码失败。
- 工作树含大量其他模块用户改动；本轮不恢复、不覆盖、不提交这些文件。

## 第1轮代码计划

1. 在 `_evaluator_dry_run` 中先读取并规范 `applies_to_modes`，不适用 profile 跳过；适用但缺 binding 才报告 finding。
2. 完善 `_binding_for_mode` 对顶层和嵌套 mode map 的读取优先级；新写出只使用规范 mode map，旧字段仅兼容读取。
3. 修改 Stage06 hidden scope 校验/normalizer，允许 shared、reproduction-only、autonomous-only，并检查 profile 与 truth scope 一致；不新增论文特例。
4. 删除 `_evaluation_ground_truth_findings` 对 `dual_axis_100`/总分的强制注入和硬依赖；保留基本结构与 Key Point/结论引用检查。若外部 evaluator schema明确需要字段，记录为下游合同诊断，不在科学合成阶段猜测评分策略。
5. 将 route evidence map 的渲染收窄到 evidence ID/route category/step index 等索引字段，并在 Stage07 prompt 中明确禁止目标值、结论、DOI和源路径。
6. 统一 autonomous public key-point alias 的 prompt和转换投影，禁止公开 `gt_*`/内部 profile ID。
7. 对 gate 的 deterministic normalization 写出 provenance 文件/字段，保持 gate 可追溯；不把科学 finding写入代码规则。

## 验证顺序

- 先运行定向 Stage06/07 单测，再运行完整 `pytest`；
- 对历史机械阻断 fixture 做 mode-specific 回放；
- 提交 DeepSeek-v4-pro-0813、Codex harness、并发10、随机10篇 Stage05通过论文；
- 完成后逐篇分析并决定是否进入第2轮；Stage07B仅记录设计，不在第1轮预先启用。


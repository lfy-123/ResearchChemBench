# Stage06/07 第4轮实现与回归记录

日期：2026-08-21  
基线：`25dbd33`  
测试：`runs/stage06-07-v4-round4-deepseek10-concurrency10-20260821`

## 结果

- 10/10 CLI完成，`failed_count=0`。
- 9篇进入Stage07，8篇科学批准并机械发布，1篇 mechanical阻断。
- 阻断原因全部集中为 JSONPath 过滤表达式 `$.channels[?(@.channel=='R1')].appearance_energy_eV` 等 parser 不支持。
- 另一篇 `objective_failure_retryable` 在四轮均为同一抽样论文，属于 Stage06 模型/源材料执行失败，未出现合同 gate finding。

## 修改

Stage07 gate 对包含 `[?` 的 evaluator-side JSONPath filter 不再产生 `evaluator_binding_path_invalid`；改写为 `evaluator_binding_filter_unchecked` diagnostic。代码不尝试解释筛选条件，也不改变 Ground Truth 或科学结果。过滤表达式的实际评分仍由 evaluator 负责。

## 归因

- 前四轮出现的 mode binding、语义 document、开放 schema、dotted mapping、wildcard 等阻断均已消失，说明它们是代码兼容性问题。
- 本轮剩余过滤表达式同样是通用 parser 边界，不是论文特例。
- `objective_failure_retryable` 为单一模型/材料运行问题，目前不应通过代码特判。

## 决策

过滤表达式修复后再次回归；若无机械误报，即进入20篇扩大测试。Stage07B仍无必要：机械 gate 已能区分真实合同缺失和语法观察限制，且没有稳定的“可由二次 Agent 修复”的剩余样本。

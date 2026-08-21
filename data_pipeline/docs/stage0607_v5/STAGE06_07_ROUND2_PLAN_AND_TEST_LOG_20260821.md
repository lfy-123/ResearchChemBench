# Stage06/07 v5 第2轮计划与回归记录

日期：2026-08-21  
约束：继续遵守 [v5 优化总目标](STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md)，只修改 Stage06/07 及相关测试/文档。

## 本轮动机

第 1 轮发现并处理了两类通用问题：

1. 显式 `document_binding` 被机械 gate 当作结构化 JSONPath；代码修复已提交 `9243218`。
2. 非标识符结果键被 Agent 写成非法点式 JSONPath；Stage06A/Stage07 已补充 bracket-quoted selector 的通用 Prompt 约束，提交 `e3223bf`。
3. `route_evidence_map` 的个别类别键带有 `target` 语义；已补充安全中性类别约束，提交 `f58159f`。

第 1 轮还包含科学拒绝和模型初稿 task-pair ID 漂移，但最终状态均可解释，不把它们升级为代码特例或 Stage07B。

## 固定测试配置

- 模型：`deepseek-v4-pro-0813`
- Harness：`codex`
- 推理强度：`high`
- 并发：10
- 来源：Stage05 通过集合（579 篇）
- 随机种子：`20260823`
- 为避免重复诊断，本轮从第 1 轮样本之外随机抽取；这仍是从 Stage05 通过集合的随机样本。

## 本轮样本

`paper_db240bad20dd713b`、`paper_3a22e838133b906d`、`paper_7e0876a1157628a1`、
`paper_12d39852f89f878d`、`paper_819294338622a34b`、`paper_e89f843779fe543e`、
`paper_738aae0a244ebfd1`、`paper_401424fff23076fb`、`paper_a120e3316cb174f2`、
`paper_081abed2be5bc909`。

结果目录：`runs/stage06-07-v5-round2-deepseek10-concurrency10-20260821/`。

## 验收重点

逐篇记录 Stage06A scope/completeness、Stage06B 隔离、Stage07 scientific decision/repairs、机械 gate、发布树和模型异常。特别检查：

- document binding 是否只产生可解释 diagnostic，不再误阻断；
- bracket-quoted selector 是否通过；
- route evidence map 是否只含中性类别和 evidence ID；
- mode-specific profile 是否正确过滤；
- 科学拒绝是否能见且不被代码改写；
- 是否出现至少 2 篇同类、低风险、科学批准后的合同阻断，以决定是否启用 Stage07B。

本文件在任务完成后追加逐篇结果、问题归因和下一轮决定。

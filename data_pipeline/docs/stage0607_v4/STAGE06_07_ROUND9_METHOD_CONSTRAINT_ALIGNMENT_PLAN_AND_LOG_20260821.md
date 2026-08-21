# Stage06/07 第9轮方法约束元数据对齐方案与实施记录

## 问题

当自主任务的`task.md`/`task_spec.method_constraints`公开声明某个方法是科学问题定义
的一部分时，任务元数据必须同时声明`public_scientific_method_constraints`并显式保留
`workflow_scope.autonomy_scope=fixed_input_method_constrained_workflow`。第8轮样本
`585288a`出现了`method_constraints`非空但`method_disclosure=no_paper_method`的矛盾。

这是通用合同投影问题，不是针对Ph-BODIPY、CAM-B3LYP或任何固定论文的规则。

## 修改计划

1. 归一化时同时读取`workflow_scope.autonomy_scope`和公开`method_constraints`；只要后者
   非空，就投影为方法约束披露。
2. Stage06内部的task-info/task-spec投影使用同一推导规则，避免不同阶段漂移。
3. Stage07 Prompt要求最终自主`task_spec.json`显式保存scope，并禁止非空方法约束与
   `no_paper_method`并存。
4. 添加最小回归测试，覆盖“无workflow_scope但有公开方法约束”的任务。
5. 运行Stage06/07专项和全量测试；下一步以DeepSeek并发10重新跑10篇回归。

## 实施内容

| 文件 | 修改 |
|---|---|
| `src/stages/stage06_task_builder/validation.py` | `canonicalize_mode_task_contract`将非空公开方法约束视为约束模式信号。 |
| `src/stages/stage06_task_builder/stage.py` | 统一Stage06任务投影的method disclosure推导；补充函数文档。 |
| `src/stages/stage07_task_judge/prompts.py` | 要求自主最终scope显式存在，并校验方法约束与披露字段一致。 |
| `tests/test_stage0607_agents.py` | 增加无scope但有方法约束的归一化回归测试。 |

## Git版本

- 代码修复：`6d7404c fix(stage06-07): preserve autonomous method constraints in metadata`
- Prompt修复：`1191846 prompt(stage07): require explicit autonomous scope metadata`

## 验证

- Stage06/07专项测试：137 passed
- 全量测试：524 passed
- 临时复制第8轮`585288a`自主任务并执行归一化：`method_disclosure`正确投影为
  `public_scientific_method_constraints`（未修改原始测试产物）。

## 归因与下一步

本轮修复的是代码侧合同投影和Prompt清晰度，不改变科学目标、Ground Truth数值或
Agent裁决权。待10篇回归完成后，若不再出现此类模式/方法披露漂移，再扩大到20篇；
若出现新的重复缺陷，继续按目标文档区分代码、Prompt和模型能力，迭代总数不超过10轮。
Stage07B仍不必要，除非出现“科学批准+可由确定性合同操作修复”的稳定阻断。

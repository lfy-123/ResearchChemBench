# Stage06/07 v15 方案一致性复核

复核日期：2026-08-25

对照文件：

- `STAGE06_07_V15_MINIMAL_EVALUATOR_AND_GATE_MODIFICATION_PLAN.md`
- `STAGE06_07_V15_IMPLEMENTATION_PLAN.md`

## 1. 已落实项

| 方案要求 | 代码位置 | 结果 |
| --- | --- | --- |
| 五个 split evaluator 文件是权威来源 | `src/stages/evaluator_reference.py`、`stage07_task_judge/package.py` | 通过；compatibility reference 仍为 projection |
| key point/conclusion 必须有具体 statement、expected、evidence | `minimal_evaluator_findings()` | 通过；空值、占位文本、引用不闭合会阻断 |
| 每个 key point/conclusion 必须有 rule | `minimal_evaluator_findings()` | 通过；缺 coverage 会阻断 |
| 只保留 numeric/ordering/condition/semantic | `MINIMAL_RULE_TYPES`、`_V15_RULE_TYPES` | 通过；旧字段只作读取归一化，不是新 prompt 入口 |
| numeric 必须有 target/unit/tolerance | shared helper 和独立 Gate fallback | 通过；容差只做可执行性检查，不评价科学最佳值 |
| numeric reference 不得降级为 semantic；semantic expected 不能是泛化占位 | `minimal_evaluator_findings()` | 通过；数值 reference 强制 numeric，泛化 expected 阻断 |
| 其他三类必须有 expected | shared helper 和独立 Gate fallback | 通过 |
| binding 必须可执行并指向公开 required_files | shared helper、phase Gate | 通过 |
| keywords 不再是必需字段 | shared helper、prompt、测试 | 通过 |
| self-check 与 external Gate 共享语义 | `phase_gate.py` 调用 shared helper；Stage07 validation 调用同一 helper | 通过 |
| Stage06A prompt 强调自查和修复 blocking findings | `stage06_task_builder/prompts.py` | 通过 |
| 不新增 resume/retry/replay | 本轮未改相关编排逻辑 | 通过 |
| 不自动生成科学答案或容差 | helper 只读检查；package 不补造科学内容 | 通过 |

## 2. 有意保留的兼容部分

`phase_gate.py` 仍保留旧 hidden-reference acceptance profile 的读取函数，供未迁移的历史包读取；这些分支不属于 v15 split evaluator 生产格式。新 Stage06A prompt 不再要求旧类型，v15 split 文件的 Gate 不再依赖 `keywords`、旧 `acceptance_type` 或旧 profile policy。

独立 `inputs/tools/phase_gate.py` 在没有仓库 import path 的 Agent 沙箱中使用同文件内 fallback；正常管线运行时会优先调用 `src.stages.evaluator_reference.minimal_evaluator_findings()`。fallback 与 shared helper 的必需字段和阻断边界已由同一 fixture 回归覆盖。

## 3. 测试结果

通过：

```text
24 passed
```

覆盖：

- 完整四类 rule；
- numeric 缺 target/unit/tolerance；
- 非整数 tolerance；
- condition/semantic expected；
- 缺 binding、非法路径；
- 占位 statement；
- 缺 rule coverage；
- keywords 缺失不阻断；
- self-check / external Gate 同一快照一致；
- split reference package assembly 和 compatibility projection。

工作区完整 `tests/test_stage0607*` 还存在若干与本轮无关的既有 paper_id/resume/mock 合同失败；这些失败来自此前未提交的 v14 工作区修改，未由本轮 evaluator 修改引入，未将其混入本次 scoped 改动。

## 4. 发布前结论

代码与 v15 目标一致，可以进入十篇论文的 GPT-5.6-sol 合成测试。测试时重点记录：

1. 每篇五个 evaluator 文件是否生成且无 placeholder；
2. 每个 key point/conclusion 是否有 rule coverage；
3. Stage06A self-check 和 Stage07 external Gate 的 blocking findings 是否一致；
4. Stage07 科学批准与最终发布状态；
5. 任何失败是科学不可构建、文件合同缺失，还是 Agent 没有按 prompt 完成 evaluator。

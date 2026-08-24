# Stage06/07 v9B：10 篇历史科学批准样本 Gate 轨迹分析

日期：2026-08-24  
代码版本：`15262cb`（`feat(stage06): make autonomous converter gate external-only`）  
测试结果：[runs/stage06-07-v9b-gpt10-codex-20260824](/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline/runs/stage06-07-v9b-gpt10-codex-20260824)  
模型：`gpt-5.6-sol`；Harness：Codex；reasoning：`high`；并发：10

## 1. 结论先行

本批次证明了两件事：

1. Stage06A 的 Agent 自查是有用的。模型在同一 workspace 内根据 Gate 输出补齐了 receipt、handoff 文件、输入坐标路径、最终 claim 和部分合同字段；6 个进入构建的任务中，5 个最终自查通过，1 个仍未通过。
2. 当前自查 Gate 与编排器外部 Gate 的检查范围不一致。自查通过的 5 个构建任务中，4 个仍被外部 Stage06A Gate 判定失败；因此当前不能把“Agent 自查通过”解释为“已经满足外部 Gate”。这首先是代码/合同实现不一致，其次才是 Agent 没有补齐合同的问题。

本批次不能证明自查提高了最终发布率：没有同一批论文、同一模型、关闭自查的对照组，而且外部 Gate 还检查了自查没有检查的 evaluator acceptance 合同。观测到的最终发布率只能作为现状记录，不能作为因果结论。

## 2. 测试范围和判定口径

测试 manifest 来自 Stage05 已通过候选中的历史科学批准记录，刻意包含曾经机械通过、机械阻断以及经过 Stage07B 的样本。10 篇全部完成，worker 失败数为 0，批次状态为 `COMPLETED`。

这里区分四类状态：

- **科学构建/科学审计**：模型对论文是否有可闭合、值得构建的计算化学问题作出的判断；代码不代替这个判断。
- **Agent 自查**：Agent 在自己的 workspace 中运行 `inputs/tools/phase_gate.py`，可在同一上下文内修改文件后再次运行。
- **外部 Gate**：编排器在 Agent 结束后对最终 workspace 做的一次独立检查；它不触发 Gate finding recovery。
- **发布 Gate**：Stage07A/Stage07B 和最终 package validator 对 evaluator 合同及公开包的检查。

Agent 自查的最终状态是从各任务的 `_agent_stdout.jsonl` 中重建的；workspace 中的 `phase_gate_report.json` 由编排器最后写入，因此不能单独用该文件区分 Agent 自查和外部 Gate。

## 3. 汇总结果

| 环节 | 结果 |
|---|---:|
| 批次完成 | 10/10 |
| Stage06A `provisional_constructed` | 6/10 |
| Stage06A `provisional_not_constructible` | 4/10 |
| 构建任务 Agent 自查最终通过 | 5/6 |
| 构建任务 Agent 自查最终失败 | 1/6 |
| 构建任务外部 Stage06A Gate 通过 | 1/6 |
| 构建任务外部 Stage06A Gate 失败 | 5/6 |
| Stage06B Agent-facing Gate 调用 | 0 |
| 构建任务 Stage06B 外部 Gate 通过 | 5/6 |
| 构建任务 Stage06B 外部 Gate 失败 | 1/6 |
| 构建任务 Stage07 科学批准（含修复） | 6/6 |
| Stage07A 外部 Gate 通过 | 0/6 |
| Stage07B repaired | 1/6 |
| Stage07B technical_blocked | 3/6 |
| Stage07B not_eligible | 2/6 |
| 最终 publish-ready | 1/6 |

4 篇 `provisional_not_constructible` 任务没有进入 Stage06B。这不是机械 Gate 把任务误杀，而是 Stage06A/Stage07 对源材料闭合性作出的科学不可构建判断；它们的 Stage06A Gate 若运行，均未发现成功任务树的强制缺陷。

## 4. 逐篇轨迹

| 论文 | Stage06A 科学结果 | Agent 自查最终 | 外部 Stage06A | Stage06B 外部 | Stage07 科学结果 | Stage07B / 最终 | 主要问题归类 |
|---|---|---|---|---|---|---|---|
| `paper_2aca1dd116799b28` | constructed | 通过（先失败后修复） | 失败：`semantic_acceptance_contract_missing` ap-1~3 | 通过 | approved_with_repairs | technical_blocked，未发布 | acceptance profile 类型/命题合同不完整；不是输入科学闭合问题 |
| `paper_308bbee002d4560c` | constructed | 通过（先失败后修复） | 通过 | 通过 | approved_with_repairs | not_eligible，未发布 | Stage07A 生成重复 binding 来源及缺 comparison/projection |
| `paper_30cec9ecf4782412` | not_constructible | 通过（负向路径） | 未进入成功树 | 未运行 | rejected_scientific_unrepairable | not_run | 源材料/路线闭合不足，科学拒绝合理 |
| `paper_3590deded767345e` | constructed | 通过（先失败后修复） | 失败：`semantic_acceptance_contract_missing` ap-1~5 | 通过 | approved_with_repairs | repaired，最终发布 | Stage06A 语义 profile 缺命题；Stage07B 能补合同 comparison |
| `paper_611000e1de080f6f` | constructed | 通过（多次修复） | 失败：ap-1 语义、ap-2 numeric target/unit/projection | 通过 | approved_with_repairs | technical_blocked，未发布 | Agent 把可评分字段写成不完整 profile；科学输入本身不是阻断原因 |
| `paper_76ae2dc25f0a5aeb` | not_constructible | 通过（负向路径） | 未进入成功树 | 未运行 | rejected_scientific_unrepairable | not_run | 关键坐标/路线闭合不足，科学拒绝合理 |
| `paper_8b7bf002cc6a4ba9` | constructed | 通过（先失败后修复） | 失败：comparison/projection、rubric 容器、workflow schema | 失败：autonomous rubric 非数组、results schema 缺失 | approved_with_repairs | not_eligible，未发布 | Stage06A/06B 合同输出错误；Stage07B 正确拒绝接管不支持的科学/结构性错误 |
| `paper_9455a82229de2427` | constructed | 失败（多次仍失败） | 失败：缺 final claim、4 个输入资产及语义 profile | 通过 | approved_with_repairs | technical_blocked，未发布 | Stage06A 未补齐构建必需资产和 conclusion rubric；Stage07 后续无法凭空恢复源坐标 |
| `paper_9ec8c4761c4f171b` | not_constructible | 未运行成功树 | 未进入成功树 | 未运行 | rejected_scientific_unrepairable | not_run | 科学不可构建 |
| `paper_a5564360a31f760b` | not_constructible | 通过（负向路径） | 未进入成功树 | 未运行 | rejected_scientific_unrepairable | not_run | 科学不可构建 |

## 5. Stage06A 自查是否真正发挥作用

### 5.1 有帮助的部分

从 Agent 的实际命令轨迹可以看到，自查不是只写在 prompt 中：

- `paper_2aca...`：第一次发现 receipt、handoff 和输入资产缺失，Agent 补齐后再次运行并通过。
- `paper_308...`：第一次发现 receipt/handoff 缺失，后续修复后通过。
- `paper_359...`：第一次发现 receipt、final claim 和输入资产缺失，后续修复后通过。
- `paper_611...`：经历多次合同字段修复后通过。
- `paper_8b7...`：先发现 rubric/schema 问题，后续自查最终通过；但转换 Agent 的 autonomous 合同仍被 Stage06B 外部 Gate 发现。
- `paper_945...`：多次自查仍报告 conclusion、acceptance profile 和四个坐标资产缺失，最终未通过。

因此，自查对“文件存在、路径闭合、receipt/handoff 完整、基本交付结构”有直接的早期反馈价值；它也没有触发额外 Codex resume，修复发生在同一次 Agent 上下文内。

### 5.2 不能据此宣称提高最终 Gate 通过率

构建任务中，自查最终通过 5/6，但外部 Stage06A 只有 1/6 通过，Stage07 最终只有 1/6 发布。这个差距不能简单归咎于模型不听反馈，因为外部检查还包含自查工具没有实现的 acceptance/evaluator 检查。

要证明“自查提高通过率”，必须做固定样本 A/B：同一论文、同一模型、同一 prompt 版本，一组 `agent_and_external`，一组关闭 Agent 自查但保留外部 Gate；至少比较外部 Gate 通过率、缺失项数量和 Agent 修复命令数。本批次没有这个对照，结论只能是“自查对早期闭合有效，最终收益待验证”。

## 6. 最重要的代码问题：两套 Gate 语义不一致

Stage06A Agent 实际调用的是工作区内的独立脚本 `inputs/tools/phase_gate.py`。它检查文件、路径、交付物、模式和基本 hidden reference 结构，但不完整检查 acceptance profile 的 typed contract 和 submission binding。

编排器的 `_stage06a_phase_gate_findings()` 还调用 `_acceptance_profile_findings()`，因此会检查：

- `semantic_propositions` 是否有 `required_propositions`；
- numeric profile 是否有 target、unit/tolerance；
- submission binding 是否有 projection/comparison；
- profile 与 binding 是否闭合。

典型结果是：

```text
Agent 自查：passed
外部 Stage06A：failed
semantic_acceptance_contract_missing:ap-1
numeric_acceptance_target_or_unit_missing:ap-2
acceptance_submission_projection_missing:ap-2
```

这属于代码/合同设计问题，而不是单篇论文的模型能力问题。当前 workspace 的 `phase_gate_report.json` 还会被外部报告覆盖，导致不读取 stdout 就无法追踪两次检查的独立结果；这是可观测性缺陷。

### 最小修复方向

1. 让 standalone self-check 与外部 Stage06A Gate 共享同一套通用 typed-contract 检查，或明确把外部 Stage06A Gate 收窄到 standalone 已承诺的范围；推荐前者，但只加入通用合同检查，不加入论文、分子、数值中心性规则。
2. 分开保存 `agent_self_check_report.json` 和 `external_phase_gate_report.json`，各自记录 authority、attempt、findings；不再用同一个文件覆盖。
3. 保持 Gate finding fail-open 传递给下一阶段，不把 Gate 变成科学拒绝器；自查工具的作用是让 Agent 尽早修复，外部 Gate 的作用是观测和最终合同判定。

## 7. 缺失项的责任和必要性

| 缺失项 | 应由谁生成 | 是否发布合同必需 | 本批次判断 |
|---|---|---|---|
| `construction_receipt.json` | Stage06A | 是（constructed 路径） | 自查能促成补齐；不应由 Stage07 猜测 |
| `workflow_completeness_check.json`、`public_to_private_asset_map.json` | Stage06A | 是（handoff） | 属于构建交接，不是科学答案 |
| `data/inputs` 中被 `task_spec` 引用的坐标 | Stage06A，且必须来自源材料 | 是（若任务宣称使用该 workflow） | `paper_945...` 缺失是真缺陷；Stage07 不应伪造坐标 |
| `claim_role=final`、结论 rubric | Stage06A/Stage07A 的科学合同 | 是（有可评分任务时） | 内容由 Agent 科学判断，代码只检查结构 |
| semantic profile 的 propositions | 生成该 profile 的 Stage06A/Stage07A | 是（profile type 为 semantic 时） | 空列表不是“可选”；应改正确类型或补源证据支持的命题 |
| numeric profile 的 target、unit、tolerance | Stage06A/Stage07A | 是（profile type 为 numeric 时） | 代码不能发明目标值；缺失应由 Agent 修复或改为合理的非数值 claim |
| binding 的 projection/comparison | Stage07A；纯 transport 修复可由 Stage07B | 是（evaluator 需要解释结果） | `paper_359...` 证明 Stage07B 可做窄修复 |
| autonomous rubric/results schema | Stage06B | 是（自主公开表面） | `paper_8b...` 的外部失败属于 Stage06B 输出错误 |
| reproduction route evidence | Stage06A/Stage07A，取决于模式合同 | reproduction 若声明路线复现则是；autonomous 不应泄漏 | 不应通过关键词硬编码；应由模式合同声明 |

“缺失”不等于“论文不可用”：如果缺的是可选字段或不适用模式字段，Gate 应跳过；如果缺的是源坐标、答案所需的必要命题或 evaluator binding，则是任务合同不完整。科学不可构建与合同不完整必须继续分开统计。

## 8. Stage06B external-only 验证

本批次 6 个转换任务的 Agent stdout 中没有 `phase_gate.py --phase stage06b` 调用；每个转换阶段最多有一次编排器外部检查，`agent_self_check_required=false`。5/6 通过，唯一失败的 `paper_8b...` 明确报告 autonomous rubric 容器和 results schema 缺失。

这说明 v9B 的核心改动生效：取消 Stage06B Agent-facing Gate 没有引入 resume/recovery 黑洞，外部 Gate 仍能把问题传递给 Stage07。当前没有证据表明应恢复 Stage06B 自查循环。

## 9. Stage07/Stage07B 结果的含义

6 个科学构建任务全部被 Stage07 科学批准，说明科学审计没有把合同问题误判为科学不可修复。最终发布率低，主要来自 evaluator 合同，而不是 Stage06A 的科学选题：

- `paper_359...` 的 comparison 缺失是窄 transport 问题，Stage07B 修复后发布。
- `paper_2aca...`、`paper_611...`、`paper_945...` 的 profile 语义/数值合同缺失，Stage07B 虽尝试修复，但最终仍 technical_blocked；这里不能让 Stage07B 猜科学答案。
- `paper_308...` 同时出现 shared binding 与 mode matrix，属于不允许的重复来源，且另有 projection/comparison 缺失；Stage07B 将其标记 `not_eligible`，要求 Stage07A 重新作合同判断是合理的。
- `paper_8b...` 的 evaluator load/rubric 容器错误和 route evidence 缺失超出 Stage07B 的窄 transport 权限，因此 `not_eligible` 合理。

Stage07B 当前的“not_eligible”不是把论文科学拒绝，而是拒绝在无法确认科学语义的情况下自动改答案合同；这一边界应保留。

## 10. 下一轮只做通用、低复杂度修复

下一轮不增加论文特例规则，也不把 Gate 变成科学中心性审计器。建议只做：

1. 统一 standalone self-check 与 Stage06A 外部 Gate 的通用 acceptance-contract 检查；
2. 分离 Agent/外部 Gate 报告，补充可观测性；
3. 在 Stage07 输出端做确定性的单一 binding 来源归一化：有 mode matrix 时删除重复 shared binding，不能安全归一化时明确报告给 Stage07A；
4. 保持 Stage06B external-only；
5. 用固定 fixture 回归上述三类合同错误，再做一次同样本 A/B 测试，才评价自查对最终通过率的贡献。

在这几项完成前，不建议扩大批量合成，也不建议通过放宽 Gate 来提高发布数量；那会把真实的 evaluator 缺陷掩盖成“通过”。


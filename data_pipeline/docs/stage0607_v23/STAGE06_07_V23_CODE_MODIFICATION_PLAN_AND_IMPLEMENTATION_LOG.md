# Stage06/07 v23 代码修改计划与实施记录

## 1. 依据与目标

本计划严格依据：

`docs/stage0607_v23/STAGE06_07_V23_TOKEN_EFFICIENCY_SEMANTIC_EVALUATOR_AND_FINALIZATION_MODIFICATION_PLAN.md`

本轮只解决以下问题：

1. Stage06 在 reproduction 自查通过后出现重复目录/Gate 检查，浪费大量 token，甚至未生成 autonomous；
2. `construction_receipt.json` 被 Bridge 过早视为完整任务，finalization reserve 又过大；
3. reproduction 可能把作者科学路线写成结果排序或最终答案，Stage07 未能识别；
4. evaluator 被误解为必须依赖数值规则，文本关键点和科学结论没有被正常视为评估依据；
5. numeric rule 的 binding 需要定位到实际数值字段，不能只绑定整个对象或数组。

保持不变的边界：

- 不恢复 Stage06B、Stage07B、conversion retry、旧 session resume 或兼容投影；
- 不增加论文、化合物、关键词或固定数值特例；
- 不让代码生成候选、统一预处理论文科学输入或判断科学结论；
- Stage06 self-check 只由 Prompt 要求，不新增编排器对 self-check 报告的强制控制；
- evaluator 不声明由代码、大模型或人工评分；
- 权重、总分、通过阈值和评分执行器选择属于 benchmark runtime，不进入 Stage06/07 evaluator 文件。

## 2. 修改前审计

### 2.1 已经符合 v23、无需重复实现

- `src/stages/phase_gate.py` 已使用同一实现供 Agent self-check 和 external Gate 调用；
- Gate 已允许 `numeric`、`ordering`、`condition`、`semantic` 四类规则；
- Gate 没有要求至少存在一个 numeric rule；
- numeric rule 已要求 `target`、`unit`、`tolerance` 和 binding；
- non-numeric rule 已要求具体 `expected` 和 binding；
- tolerance 只产生 diagnostic，不因科学选择本身阻断；
- evaluator 已拆分为五个独立文件；
- Stage07B 和 Stage06B 已不在活动流程中。

### 2.2 必须修改

- Stage06 Prompt 仍是 13 个连续步骤，终态和 Gate 说明重复，缺少明确的非进展约束；
- Stage06 默认 `synthesis_finalization_reserve=28`；
- Stage06 将 receipt 配置为 Bridge 的 `structured_artifact_path`，receipt 可以提前终止整个工作流；
- Stage07 Prompt 没有从隐藏 reference 反向检查公开表面是否直接泄露答案；
- Stage07 evaluator 审计没有明确接受文本关键点和科学结论；
- Gate 能验证 selector 存在于 schema，但没有区分 numeric scalar leaf 与整个对象/数组；
- 版本号仍为 v22。

### 2.3 修改前测试基线

从仓库根目录运行：

```bash
PYTHONPATH=.:data_pipeline .envs/researchchembench/bin/pytest -q \
  data_pipeline/tests/test_stage0607_v19_contracts.py
```

结果：`10 passed`。

## 3. 逐文件修改计划

### P1. Stage06 Prompt：四个里程碑和非进展约束

文件：`src/stages/stage06_task_builder/prompts.py`

- 升级 Prompt version；
- 将工作流整理为四个不可倒退的里程碑：
  1. input closure + scientific core + private paper route；
  2. 完整 reproduction + reproduction Gate；
  3. 完整 autonomous + full-pair Gate；
  4. terminal receipt；
- 加入无文件变化时不重复 `find/ls/pwd/Gate/report read` 的约束；
- reproduction Gate passed 后立即推进 autonomous，不再重复审查已通过模式；
- 要求同一模式文件尽可能分组写入；
- 增加短抽象示例，区分 author scientific route 与结果排序/答案；
- 明确过程关键点、数值、排序、条件、结构身份和文本科学结论都可成为 evaluator；
- evaluator 不出现评分执行器、权重、总分或 pass threshold 字段；
- 开放搜索任务由 Agent 按论文目标定义有限范围和停止依据，代码不规定候选数。

### P2. Stage06 终态：receipt 不再驱动 Bridge 提前完成

文件：

- `src/stages/stage06_task_builder/stage.py`
- `src/config.py`
- `config.example.json`

修改：

- Stage06 request 继续使用受信任的 `outputs/construction_receipt.json` structured artifact，
  但同时声明完整双模式 task tree 的 required paths；Bridge 只有在 receipt 和 required paths
  全部完成时才接受 artifact completion；
- receipt 仍由 Agent 在 full-pair Gate passed 后最后写入，并继续作为 Stage06 response schema；
- Stage06 代码显式要求 receipt 文件存在并校验其 schema；
- external Gate 仍在 Agent 单次退出后对实际 task tree 做权威只读检查；
- 默认 finalization reserve 从 28 缩小到 6，只保留小型终态响应空间；
- 升级 implementation version；
- 不修改通用 Bridge，不新增 conditional completion、retry 或恢复分支。

这样保持实现简单：Bridge 仍只接收一个固定 receipt，但不会把 receipt 单文件当成完整 task
tree；如果 Agent 仍未完成，Bridge 会继续允许有限的写入，external Gate 最终如实阻断，编排器
不会主动制造一个“constructed 半成品”。

### P3. Stage07：答案反推和 evaluator 科学可用性审计

文件：

- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_task_judge/stage.py`

修改：

- 升级 Prompt/implementation version；
- 要求从隐藏 evaluator 提取 reference values、ordering、最终候选/结构身份、最终结论和 tolerance；
- 对 `task.md`、`task_info.json`、`submission_schema.json`、public filenames 和 public input
  注释执行答案反推测试；
- 若不计算即可从公开内容填写待评分 ordering、最终候选或主要结论，则视为泄露；
- reproduction 允许作者假设、候选方向和定性机理，但禁止候选胜出方向、结果排序、结果结构和完整结论；
- evaluator 审计以关键点、结论、证据链和任务/schema 对齐为核心，不强制 numeric；
- semantic rule 不因不能由简单数值比较器执行而拒绝；
- Stage07 仍只做有界修复，不重建 Stage06 失败任务。

### P4. Common Gate：最小 numeric leaf 检查

文件：`src/stages/phase_gate.py`

- 保持四种 rule type 和五个 evaluator 文件不变；
- 保持 semantic-only evaluator 可通过；
- 将 schema selector 查询改为同时返回“是否可定位”和“明确目标 schema”；
- numeric rule 的 fields 若只明确指向 `object` 或 `array`，且没有任何 scalar numeric leaf，阻断；
- 对开放 schema 中无法静态确定类型的 selector 不做过度阻断；
- semantic/ordering/condition binding 可以指向结论、证据对象或集合；
- 不检查 tolerance 是否科学最优，不增加自然语言关键词黑名单。

### P5. 定向测试

文件：

- 更新 `tests/test_stage0607_v19_contracts.py`；
- 新增 `tests/test_stage0607_v23_evaluator_and_finalization.py`。

覆盖：

1. Stage06 四里程碑顺序和非进展约束；
2. author route/答案方向 micro-example；
3. Stage06 request 不再配置 receipt structured artifact，reserve 为 6；
4. receipt 缺失时 Stage06 明确失败；
5. semantic/condition-only evaluator 通过；
6. mixed numeric/semantic evaluator 通过；
7. numeric rule 缺 target/unit/tolerance 阻断；
8. numeric binding 只指向数组/对象阻断；
9. numeric binding 指向明确 number leaf 通过；
10. semantic binding 指向结论或证据对象允许；
11. self-check 与 external Gate 对同一 fixture findings 一致；
12. Stage07 Prompt 包含答案反推测试且不要求 numeric rule。

## 4. 实施顺序和 Git 边界

1. 提交 v23 设计与本代码计划文档；
2. 完成 P1/P2，并运行 Prompt/Stage06 定向测试；
3. 完成 P3，并运行 Stage07 定向测试；
4. 完成 P4/P5，并运行 Stage06/07 定向测试集；
5. 运行格式、静态检查和相关回归测试；
6. 回读 v23 方案，逐项填写第 6 节一致性表；
7. 仅暂存本轮文件并提交代码；
8. API 连通性预检通过后，以并发 5 提交固定五篇真实回归；
9. 监督 Stage06/07 状态、工具轨迹、self/external Gate、release 和任务科学质量；
10. 写最终测试与质量分析报告，单独提交文档。

工作区其他 Stage00–05、chemistry toolbox、配置和用户文件均不纳入本轮提交。

## 5. 固定五篇真实回归配置

论文：

- `paper_2aca1dd116799b28`
- `paper_611000e1de080f6f`
- `paper_76ae2dc25f0a5aeb`
- `paper_9455a82229de2427`
- `paper_a5564360a31f760b`

运行配置：

- Stage06/Stage07 model：`gpt-5.6-sol`；
- reasoning effort：`high`；
- endpoint：沿用本地 `http://127.0.0.1:50917/v1`；
- API key：使用用户本轮提供的新 key，仅通过环境变量传入，不写入文档、日志或运行 manifest；
- batch concurrency：5；
- source run：脚本现有固定 Stage00–05 source run；
- 新建独立 v23 run，不覆盖 v22 结果。

科学拒绝不算技术失败，不以强行提高发布篇数为目标。

## 6. 方案一致性审查（代码完成后填写）

| 检查项 | 状态 | 证据 |
|---|---|---|
| 双模式 v22 科学定义保持不变 | completed | Stage06/07 Prompt 保留 objective/author-route/autonomous 边界 |
| Stage06 四里程碑和非进展约束落地 | completed | v23 Prompt 的 A–D milestones 与 progress discipline |
| reproduction 不公开结果排序/完整答案 | completed | Prompt 明确禁止结果方向、结构和完整结论；Stage07 增加答案反推 |
| autonomous 不公开 author route | completed | Prompt 要求从每个 Agent-visible surface 移除 |
| evaluator 正常支持数值与文本关键点/结论 | completed | semantic/ordering/condition 不要求 numeric 或特定评分执行器 |
| Gate 不强制 numeric rule | completed | semantic/condition-only fixture passed |
| numeric rule 完整且 binding 定位数值 leaf | completed | object/array binding 阻断，明确 numeric leaf 通过 |
| tolerance 科学选择不阻断 | completed | 仅保留 tolerance diagnostic |
| receipt 只有与完整 task tree 一起才触发 Bridge 完成 | completed | structured artifact required files；receipt 单独出现不会完成 |
| finalization reserve 已缩小 | completed | Stage06 默认从 28 改为 6 |
| Stage07 答案反推测试落地 | completed | v23 Prompt 与审计 fixture 已覆盖 |
| 未新增 retry/resume/Stage06B/Stage07B/兼容投影 | completed | 本轮未改入这些流程 |
| 无论文或化学类型特例 | completed | 仅通用 schema、Prompt 和 Gate 逻辑 |
| 定向回归通过 | completed | 31 Stage06/07 tests + 247 pipeline/batch tests passed |

## 7. 实施记录

| 时间 | 步骤 | 状态 | 说明 |
|---|---|---|---|
| 2026-08-27 | 现状审计 | completed | Gate 已支持 semantic-only；定位 Prompt、receipt、reserve、Stage07 和 numeric leaf 缺口 |
| 2026-08-27 | 修改前基线 | completed | `tests/test_stage0607_v19_contracts.py`: 10 passed |
| 2026-08-27 | 代码修改计划 | completed | 本文档 |
| 2026-08-27 | P1 Stage06 Prompt | completed | 四个里程碑、非进展规则、semantic evaluator 说明和抽象示例 |
| 2026-08-27 | P2 Stage06 终态 | completed | receipt + required task tree gating；reserve=6 |
| 2026-08-27 | P3 Stage07 审计 | completed | answer-inversion、route/answer 边界和 evaluator 可判断性 |
| 2026-08-27 | P4/P5 Gate 与测试 | completed | numeric leaf 检查；定向测试与 pipeline/batch 回归通过 |
| 2026-08-27 | 一致性审查 | completed | 已逐项核对 v23 方案；真实回归尚待执行 |
| 2026-08-27 | 五篇真实回归 | completed | 固定五篇均完成并机械发布；Stage06 总 token 约 8.35M |
| 2026-08-27 | 结果分析 | completed | 详见 `STAGE06_07_V23_FIVE_PAPER_REGRESSION_AND_QUALITY_ANALYSIS.md`；机械发布 5/5，但严格直接可用 0/5 |

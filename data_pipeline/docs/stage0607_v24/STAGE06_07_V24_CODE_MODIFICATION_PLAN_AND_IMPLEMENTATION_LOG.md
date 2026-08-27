# Stage06/07 v24 代码修改计划与实施记录

## 1. 目标与约束

本文档把
`STAGE06_07_V24_FEASIBILITY_FIRST_TASK_CONSTRUCTION_AND_AUDIT_MODIFICATION_PLAN.md`
转换为可执行的代码修改计划，并在实施、测试、方案对照和五篇真实回归期间持续记录事实。

核心约束：

- 先判断科学可行性，再生成任务；
- `paper_reproduction` 与 `autonomous_research` 分别判断，可发布一个或两个模式；
- 只有两个模式都不可行时才整篇科学拒绝；
- 论文/SI 已有明确且不泄露答案的结构时优先生成自包含输入；
- CCDC/PubChem 仅在任务实际依赖数据库记录或检索时启用；
- evaluator reference 只来自当前论文/SI；
- Stage07 审计和修复已有模式，但不改变科学目标，也不从零创建缺失模式；
- self-check 与 external Gate 共用同一机械实现；
- 不增加论文特例、化学类型硬编码、retry/resume、Stage06B/Stage07B 或旧格式兼容投影。

工作区已有大量与本任务无关的 Stage00–05、resume、sandbox 和 chemistry toolbox 修改。本轮只修改
Stage06/07 v24 直接涉及的文件和本记录，不覆盖或清理用户既有修改。

## 2. 基线差距

| 领域 | 当前 v23 行为 | v24 要求 |
|---|---|---|
| Stage06 可行性 | 单一 `input_closure`，直接要求完整任务对 | 四项闭合，按模式分别判断 |
| 输出模式 | 两个模式都必须存在 | 一个或两个模式均可发布 |
| 数据库 | Prompt 没有明确按需层级 | 论文结构优先；特定记录和检索任务按需启用 |
| Agent 完成合同 | bridge 固定要求两个模式的 16 个文件 | receipt 声明 `release_modes`，文件由同一 Gate 验证 |
| Common Gate | 默认遍历两个模式；仍读取旧 `input_closure` | 只验证 `release_modes`；验证 v24 workflow review |
| Gate 最小合同 | 缺 numeric target 类型、required chain 和 XYZ 内容检查 | 补齐三项通用机械检查 |
| Stage07 | 把 substantial evaluator rewrite 当作拒绝理由 | 目标不变且来源闭合时允许大幅重写 |
| Stage07 单模式处置 | 只能批准或拒绝完整任务对 | 可剔除不可修模式并批准剩余模式 |
| Release | `assemble_release_pair()` 固定装配两个模式 | 按最终 `release_modes` 动态装配和写 manifest |
| 统计 | 主要统计 paper-level pair | 同时记录 paper、mode 和 paired release 数量 |

## 3. 代码修改步骤

### 步骤 A：Stage06 v24 Prompt 与 receipt

修改：

- `src/stages/stage06_task_builder/prompts.py`
- `src/agents/schemas.py`
- `src/stages/stage06_task_builder/stage.py`

实现：

1. 工作流改为冻结 scientific core、完成四项 feasibility、分别决定两个模式、只构建可行模式、统一自查、
   最后写 receipt。
2. `workflow_review.json` 使用 `feasibility.objective/public_inputs/evaluation/
   reproducible_investigation/modes/release_modes`。
3. 写清输入三层选择：论文/SI 自包含优先、特定记录用 stable record ID、记录选择为科研步骤时才名称检索。
4. `construction_receipt.json` 对 constructed 结果必须给出非空 `release_modes`。
5. 移除 bridge 对完整双模式 16 文件的固定要求，避免单模式结果被基础设施错误阻断；最终完整性由同一 Gate
   根据 `release_modes` 验证。
6. Stage06 handoff 和 summary 明确实际生成模式，不保留 `task_pair_path` 兼容字段。

### 步骤 B：Common Gate v24

修改：

- `src/stages/phase_gate.py`

实现：

1. 从 workflow review 读取并验证 `release_modes`，默认只检查这些模式。
2. 单模式 self-check 只能检查已声明可行模式；整篇科学拒绝不能残留公开任务树。
3. 检查 numeric `target` 为 JSON number，但不判断 tolerance 的科学选择。
4. scoring binding 必须指向 schema 中显式声明且位于 `required` 链的字段；numeric binding 必须到达
   number/integer leaf。
5. 对公开 `.xyz` 做最小标准解析：atom count、comment 行、坐标行数和前三个坐标数值。
6. evaluator 继续只做通用完整性和引用闭合检查，不判断机理、分子身份、中心性或 tolerance 最优性。

### 步骤 C：Stage07 v24 审计与修复

修改：

- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_task_judge/validation.py`
- `src/stages/stage07_task_judge/stage.py`

实现：

1. Stage07 不信任 Stage06 自报的四项 feasibility，读取实际公开文件和 source evidence 独立复核。
2. 对已有且目标正确的模式允许大幅重写 task、input 表达、schema 和 evaluator；修复必须由既有来源唯一决定。
3. 不可修复模式从最终 `release_modes` 剔除并删除其公开/evaluator 目录；剩余模式仍可批准。
4. 不改变目标、不用弱代理目标替换、不从零创建缺失模式；没有模式可保留时科学拒绝。
5. audit receipt 明确最终 `release_modes`，external Gate 按该集合复核。

### 步骤 D：动态 release

修改：

- `src/stages/stage07_task_judge/package.py`

实现：

1. 用 `assemble_release()` 取代固定 pair 装配，根据最终 workflow review 的 `release_modes` 发布。
2. 只复制并验证实际批准模式；论文 PDF/SI 仍只进入 `release/papers/<paper_id>`，不进入 Agent input。
3. release manifest 只列出实际存在的 task package。
4. Stage07 记录 mode-level publish 数和 complete-pair 数。

### 步骤 E：定向测试与回归

新增：

- `tests/test_stage0607_v24_feasibility_and_release.py`

调整现有 Stage06/07 定向测试到 v24 当前合同，不增加旧合同兼容分支。覆盖：

- reproduction-only、autonomous-only 和完整 pair Gate/release；
- 两模式都不可行的 receipt-only 结果；
- undeclared mode、错误 `release_modes` 和缺失模式；
- self-check/external Gate 合同一致；
- numeric target 类型、schema 显式字段、required chain、numeric leaf；
- 合法/非法 XYZ；
- Stage06/Stage07 Prompt 的 feasibility-first、输入层级、单模式与大幅修复边界；
- 非数据库任务不要求 record ID 或 snapshot。

测试顺序：

1. v24 新测试；
2. Stage06/07 现有定向测试；
3. 与修改文件相关的 late-stage runner/package tests；
4. `git diff --check` 和编译检查。

## 4. 方案一致性审计

代码完成后逐条对照 v24 文档第 3–14 节，至少核对：

- 四项 feasibility 和 per-mode decision 是否真实进入 Prompt、review 和 Gate；
- 单模式是否能走完 Stage06、Stage07、release 和 manifest；
- 数据库是否确实是按需路径而非默认依赖；
- Stage07 是否能大幅修复已有模式、拒绝目标漂移和从零重建；
- evaluator reference、mode disclosure、answer inversion 和 measurement contract 边界是否保留；
- Gate 是否只阻断必要机械合同，没有引入论文或化学特例；
- 是否仍有 v23 pair-only 或 `input_closure` 兼容逻辑残留。

审计结论和偏差修复记录写回本文件。

## 5. 五篇真实回归计划

固定论文：

- `paper_2aca1dd116799b28`
- `paper_611000e1de080f6f`
- `paper_76ae2dc25f0a5aeb`
- `paper_9455a82229de2427`
- `paper_a5564360a31f760b`

运行配置：

- Stage06/Stage07：`gpt-5.6-sol`；
- reasoning effort：`high`；
- Codex harness；
- 并发数：5；
- 使用与 v23 相同历史 Stage00–05 输入和当前已确认 API 配置；
- 新 run 目录独立，不覆盖 v23 基线。

监督内容：

1. Agent 是否先完成 feasibility 再写任务；
2. 是否按模式停止不可行构建，而不是强行凑完整 pair；
3. self-check、external Gate、Stage07 repair 和 release 是否一致；
4. 是否出现工具循环、提前 receipt、遗漏模式目录或非法输入文件；
5. token、工具调用和时间是否存在明显浪费。

## 6. 最终质量分析框架

每篇逐文件检查：

- 科学目标中心性、完整性和可计算性；
- `agent_input` 是否闭合、身份唯一、没有论文/SI或答案泄露；
- reproduction 是否只给作者定性路线；
- autonomous 是否真正隐藏作者路线并要求自主提出/验证解释；
- validation/search scope 是否足以复现 Agent 的实际调查；
- submission schema 与 deliverables 是否合理；
- 五个 evaluator 文件是否具体、来源绑定、规则覆盖且 claim-rule-binding 对齐；
- numeric/non-numeric reference 的选择和 measurement definition 是否公平；
- Stage07 是否发现并正确修复或拒绝 Stage06 问题；
- release 包和论文元数据是否完整。

最终报告同时与 v23 五篇结果对比，但不以发布篇数作为质量指标。

## 7. 实施日志

- 2026-08-27：完成 v24 方案与当前 v23 代码基线差距审查；确认需要跨 Prompt、schema、Gate、Stage06、
  Stage07、release 和测试修改，不能仅调整 Prompt。
- 2026-08-27：完成 Stage06 v24 Prompt、receipt schema 和动态 mode handoff 修改；去除双模式固定 artifact
  allowlist，改由 review 的 `release_modes` 决定最终验证范围。
- 2026-08-27：完成 Common Gate v24 修改：按 `release_modes` 检查、拒绝 scientific rejection 残留模式、
  numeric target 类型、required schema chain 和最小 XYZ 语法。
- 2026-08-27：完成 Stage07 v24 Prompt、receipt validation、动态 release 装配；Stage07 可保留单模式，
  不再把完整 pair 作为审批前提，并明确已有模式可大幅重写、缺失模式不可从零创建。
- 2026-08-27：新增 `tests/test_stage0607_v24_feasibility_and_release.py`，4 个 v24 定向测试全部通过。

以下旧测试中的 v19/v23 fixture 仍使用已废弃的 pair-only `workflow_review` 和 receipt 合同；它们作为历史
合同回归记录保留，不作为 v24 验收依据，不能通过添加兼容分支来迁就。

## 8. 最终一致性结论

代码层面已覆盖 Prompt/schema/Gate/Stage07/release 的 v24 主路径。真实回归前仍需完成：

- stage06/07 全量实际调用；
- 运行轨迹和输出逐文件审查；
- 与 v24 第 3–14 节逐条对照并记录任何偏差。

## 9. 五篇回归与质量结论

待真实运行和逐文件审查后填写。

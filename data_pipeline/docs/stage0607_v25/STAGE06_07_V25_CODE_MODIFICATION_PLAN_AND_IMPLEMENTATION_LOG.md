# Stage06/07 v25 代码修改计划与实施记录

## 1. 目标

根据
`STAGE06_07_V25_TASK_COMPLETENESS_AND_AUDIT_MODIFICATION_PLAN.md`，将 Stage06 从“生成结构合法的任务包”
升级为“先证明任务指令、输入、过程关键点和最终结论完整，再构建任务”；将 Stage07 升级为对上述内容逐项
审计、修补并重新验证的科学审计 workflow。

本次修改不引入论文特例、统一候选数量、强制 numeric 规则或 tolerance 科学判断，也不修改
`experiment_validation` 模式。只修改当前 autonomous_research / paper_reproduction 管线的 Stage06、Stage07、
Common Gate、结构化 receipt 和定向测试。

## 2. 实施步骤

### 步骤 1：更新 Stage06 Prompt 和 receipt 合同

修改：

- `src/stages/stage06_task_builder/prompts.py`
- `src/agents/schemas.py`

内容：

1. Prompt 明确 Stage06 workflow：冻结 scientific core → 输入闭合 → 指令完整性 → 模式构建 → 关键点/结论
   完整性 → 自查 → Gate → receipt。
2. Stage06 另写私有 `outputs/paper_route.md`，记录论文实际计算路线供 Stage07/人工参考；该文件与模式目录
   并列，绝不进入 Agent-visible `agent_input` 或发布包。
3. 要求每个可构建模式的 evaluator 至少有一个过程关键点和一个最终结论；关键点增加
   `key_point_type: process|result`，结论保持 `claim_role: final`。
4. 要求 task.md 明确研究对象、输入、观测量、验证要求、完成条件、停止条件和限制；开放搜索只要求停止
   条件，不规定候选数量。
5. workflow review 增加 `task_quality`，记录 instruction/input/process-keypoint/final-conclusion/mode
   separation 的状态、证据、问题和修复建议。
6. 明确禁止 undefined label、未定义物理量、无界搜索和破坏性 `rm -rf` 操作。
7. Stage06 receipt 继续只声明实际 `release_modes`，不增加旧 ID 或 pair 兼容字段。

### 步骤 2：扩展 Common Gate 的通用完整性检查

修改：

- `src/stages/phase_gate.py`

内容：

1. 检查 task.md 四个逻辑 section 是否存在；允许合理的标题变体，不绑定论文或化学术语。
2. 检查任务文本至少包含完成/停止逻辑，防止“有限搜索”没有结束条件。
3. 检查 workflow review 的 `task_quality` 各项目是否存在并通过。
4. 检查 `reference_key_points.json` 至少包含一个 `key_point_type=process` 的关键点。
5. 继续检查最终 conclusion、evidence 和 scoring binding 的机械闭合。
6. 不检查 tolerance 的科学优劣，不检查具体方法、机理或论文中心性。

### 步骤 3：重写 Stage07 审计 workflow

修改：

- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_task_judge/validation.py`
- `src/stages/stage07_task_judge/stage.py`

内容：

1. Stage07 按 objective、inputs、instruction_completeness、process_keypoints、final_conclusions、
   mode_separation、answer_inversion、evaluator_quality 的顺序审计。
2. 每项审计必须返回结构化 status、finding、evidence 和 repairs，不能只写自由格式的笼统通过结论。
3. Stage07 可以补充必要的任务说明、输入映射、完成/停止条件、schema 字段、过程关键点和最终结论，
   但不得改变 Stage06 scientific objective。
4. 缺少一个模式时只能保留已有且可修复的模式，不能从零创建缺失模式。
5. Prompt 明确使用安全复制/增量修改，不执行被运行环境拒绝的破坏性删除命令。
6. 审计完成后使用同一 phase Gate，Gate 失败不得发布。

### 步骤 4：更新测试

修改/新增：

- `tests/test_stage0607_v24_feasibility_and_release.py`（迁移为 v25 合同）
- `tests/test_stage0607_v25_task_completeness.py`

覆盖：

1. 缺少过程关键点时 Gate/Stage06 不通过；
2. 缺少最终结论时不通过；
3. 开放搜索有停止条件但没有候选数量限制时通过；
4. 开放搜索无停止条件时不通过；
5. 四个任务指令 section 缺失时不通过；
6. Stage07 审计 receipt 缺少结构化审计项目时拒绝；
7. Stage07 可以补充关键点但不能改变 objective；
8. semantic/ordering/condition 关键点不要求 numeric；
9. 单模式发布、论文 PDF 隔离和两种模式路线隔离继续通过。

### 步骤 5：一致性审计和真实回归

1. `pytest` 运行 v25 和相关 package/Gate 测试；
2. `git diff --check` 和编译检查；
3. 逐条对照 v25 方案第 2–10 节；
4. 使用 `gpt-5.6-sol`、`high`、并发 5 提交相同五篇论文；
5. 监督每篇 Stage06/07 的 receipt、tool trace、Gate、release_modes 和最终文件；
6. 逐篇检查任务指令、agent_input、过程关键点、最终结论和论文路线隐藏；
7. 记录 Stage07 发现的问题、修补内容和仍存在的歧义。

## 3. 方案一致性验收标准

代码完成后必须确认：

- Stage06 可构建模式都有非空 process key points 和 final conclusions；
- 开放搜索有停止条件但没有统一候选数硬编码；
- task.md、输入数据和 schema 形成可执行闭环；
- reproduction/autonomous 的唯一差异是作者路线披露；
- Stage07 的八个审计维度都有结构化报告；
- Stage07 只在原 scientific objective 上修复；
- 单模式发布和科学拒绝逻辑保持；
- Gate 仍只负责通用文件合同和最小完整性检查；
- evaluator 可以使用文本、结构、排序和条件关键点，不被强制 numeric 化；
- 论文/SI 不进入 Agent-visible 输入；
- 没有重新引入旧 ID、pair-only 合同或兼容投影。

## 4. 实施记录

### 4.1 Stage06、Gate 和 Stage07 合同实现（2026-08-27）

- `src/stages/stage06_task_builder/prompts.py` 已切换为
  `v25-task-completeness-first-20260827`，把 scientific core、输入闭合、四段任务指令、过程/最终关键点和
  self-check 明确为一个 workflow；不再规定统一候选数量。
- `src/stages/phase_gate.py` 增加通用任务完整性检查：四个逻辑 section、完成条件、停止/边界条件、至少一个
  `key_point_type=process` 关键点、`claim_role=final` 结论，以及 `workflow_review.task_quality` 收据；不判定
  tolerance 的科学优劣，也不加入论文特例。
- `src/stages/stage07_task_judge/prompts.py` 切换为 v25 审计提示，要求八个审计维度逐项给出
  `status/finding/evidence/repairs`，并明确只能在既定 scientific objective 上修补。
- `src/stages/stage07_task_judge/validation.py` 对批准收据实际校验八个维度；批准时不得残留 `failed`，避免
  “schema 合法但没有做完整审计”的假通过。
- Stage06/Stage07 implementation version 已分别更新为
  `v25-task-completeness-first`、`v25-task-completeness-scientific-audit`。

### 4.2 定向测试结果

新增 `tests/test_stage0607_v25_task_completeness.py`，覆盖完整任务通过、缺过程关键点、缺停止条件和批准审计
维度缺失四个边界；运行结果：`4 passed`。编译检查和 `git diff --check` 通过。

历史 v19/v23 测试 fixture 使用的是已废弃的 v24/旧 workflow review 合同，未作为 v25 兼容目标；后续真实回归
前将只以 v25 fixture 和当前包合同测试作为验收依据。

### 4.3 私有论文路线补充（2026-08-27）

按补充需求，Stage06 Prompt 现在要求写出非空 `outputs/paper_route.md`。Gate 对 candidate-ready 根目录检查其
存在且非空；Stage07 可读取并用于审计，`assemble_release_pair()` 不复制它，因此发布包和两种
Agent-visible `agent_input` 均不含该路线文件。

### 4.4 五篇真实回归（2026-08-27）

运行目录：
`runs/stage0607-v25-gpt-5.6-sol-20260827-five`；模型和两个阶段均为 `gpt-5.6-sol`，reasoning effort
`high`，并发 5。五篇均一次完成，`technical_blocked=0`：

| paper | Stage06 | Stage07 / 发布 |
|---|---|---|
| `paper_2aca1dd116799b28` | scientific rejection：精确计算结构/映射无法闭合 | 未运行 |
| `paper_611000e1de080f6f` | constructed | `approved_with_repairs`，双模式发布 |
| `paper_76ae2dc25f0a5aeb` | scientific rejection：R-EDY 17 几何无法可靠恢复 | 未运行 |
| `paper_9455a82229de2427` | constructed | `approved_with_repairs`，双模式发布 |
| `paper_a5564360a31f760b` | scientific rejection：三套关键结构/坐标输入不闭合 | 未运行 |

两个发布任务都具备四个逻辑指令段、非空过程关键点和最终结论，Agent-visible 输入无 PDF/SI 或
`paper_route.md`。Stage07 对 `paper_611...` 修复 5 项、对 `paper_945...` 修复 4 项，八个审计维度均有结构化
收据且最终 self-check/external Gate 均通过。两篇自主科研任务去除了作者路线，论文复现任务只保留定性作者路线。

发现的剩余质量问题：`paper_611...` 的 `task_info.json` 数据描述仍写“30-atom”，而实际 XYZ 为 31 原子；Stage07
只修复了 task.md，未同步该自由文本描述。这不构成技术 Gate 失败，但会造成输入说明歧义，后续应让 Stage07
审计同步修正 task_info 描述，或由生成 Prompt 要求所有输入数量描述与文件一致。

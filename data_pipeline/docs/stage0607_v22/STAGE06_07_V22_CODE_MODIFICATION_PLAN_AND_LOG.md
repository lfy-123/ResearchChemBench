# Stage06/07 v22 代码修改计划与实施记录

## 1. 依据与目标

本计划依据：

`docs/stage0607_v22/STAGE06_07_V22_DUAL_MODE_SCIENTIFIC_TASK_CONTENT_MODIFICATION_PLAN.md`

核心语义必须变为：

```text
paper_reproduction
= 科学目标 + 作者科学路线提示 + Agent 自主规划计算与验证

autonomous_research
= 相同科学目标 + 无作者科学路线提示 + Agent 自主提出路线并计算验证
```

两种模式都不向被评测 Agent 公开论文详细 computational protocol、结果性结构、数值、排序、
完整结论、tolerance、PDF 或 SI。

## 2. 现状审计

### 2.1 必须修改的问题

1. Stage06 Prompt 当前写着 `paper_reproduction` 完整披露 paper route，并要求 autonomous
   复制 reproduction 后删除方法和路线。
2. 当前 `task.md` 模板说明把“Required work / computational route”写成了可公开的论文路线。
3. 当前 autonomous 定义只强调自主选择方法，未强制在存在假设空间时自主提出科学路线。
4. Stage07 Prompt 当前要求 reproduction 公开 source-supported computational route，且 Pair
   审计以 route disclosure 作为差异依据。
5. Stage06/07 implementation/prompt version 和结果标签仍使用旧的
   `reproduction_first_same_agent` 语义，容易误导后续审计。
6. 现有 v19 Prompt 回归测试断言旧的“copy reproduction”语义，必须替换为新契约测试。

### 2.2 不修改的边界

- 不恢复 Stage06B、conversion retry 或旧 resume；
- 不让代码生成或判断化学候选；
- 不增加论文、化合物或关键词特例；
- 不强制所有任务使用固定 candidates/calculations/conclusion JSON；
- 不让 Gate 承担科学语义判断；
- 不因纯计算任务两个模式接近而拒绝。

## 3. 逐文件修改计划

### 3.1 `src/stages/stage06_task_builder/prompts.py`

- 升级 Prompt version。
- 重写 Agent 职业为双模式科学任务设计者。
- 增加“四层信息模型”：scientific objective、author scientific route、computational
  route、hidden reference results。
- 明确 reproduction 只公开作者科学路线，不公开论文 computational protocol。
- 明确 autonomous 隐藏作者科学路线；存在假设空间时要求 Agent 自主提出并比较路线；纯计算
  任务不虚构 discovery。
- 禁止结果性 TS/intermediate/conformer/数值等进入任何 public input。
- 保留结果导向 scientific validation requirements，但不规定软件、functional、basis 或
  执行顺序。
- 删除“copy stable reproduction task”以及“reproduction 完整披露 paper route”的矛盾说明。
- 要求两种 evaluator 与各自任务职责一致，可共享真实共同结果规则。

### 3.2 `src/stages/stage06_task_builder/stage.py`

- 升级 implementation version。
- 将 `mode_generation_strategy` 改成描述“shared objective / author-route disclosure”，
  不暗示目录复制或 protocol 转换。
- 保留单 Agent 连续工作流和 intermediate reproduction self-check，但把它解释为科学理解
  顺序，不改变 autonomous 的独立构建要求。
- 不增加代码层面的科学输入检查或候选生成。

### 3.3 `src/stages/stage07_task_judge/prompts.py`

- 升级 Prompt version。
- reproduction 审计改为：作者科学路线是否 source-supported；论文 protocol 是否隐藏；结果性
  结构是否隐藏；Agent 是否自主规划计算。
- autonomous 审计改为：作者科学路线、候选和结果是否隐藏；有假设空间时是否要求自主提出；纯
  计算任务是否被错误添加 discovery 要求。
- Pair 审计以 scientific objective 相同、author-route 只在 reproduction 公开为准。
- 不再要求 reproduction 公开论文计算路线。

### 3.4 `src/stages/phase_gate.py`

- 只检查是否存在与当前 workflow review 对应的必要机械合同。
- 不增加 route、候选或机理关键词规则。
- 运行现有 Gate fixtures；若发现“两种模式必须完全相同输入”的旧假设，只做最小删除。

### 3.5 `tests/test_stage0607_v19_contracts.py`

- 将旧 Prompt 顺序测试改为新语义测试：reproduction scientific route disclosure、共同
  autonomous computational planning、autonomous hypothesis formation、无 protocol disclosure。
- 保留 Gate、receipt、release isolation 等与本版仍相关的测试。

### 3.6 新增定向测试

在 `tests/test_stage0607_v22_dual_mode.py` 增加字符串契约测试和最小 fixture：

1. reproduction 公开 author scientific route，但隐藏 paper protocol；
2. autonomous 隐藏 author route；
3. 两种模式都要求自主计算路线；
4. 有假设空间时 autonomous 要求提出路线；
5. 纯计算任务允许任务结构接近；
6. result-bearing artifact 不进入 public input 的 Prompt 要求存在。

## 4. 实施顺序

1. 先修改 Stage06 Prompt；
2. 修改 Stage07 Prompt；
3. 修改 Stage06/07 版本和 strategy 元数据；
4. 更新旧断言并新增 v22 定向测试；
5. 运行定向测试、阶段相关全量测试；
6. 回读本计划和 v22 方案逐项比对；
7. 提交代码和文档；
8. 使用上一轮相同五篇论文、`gpt-5.6-sol`、high reasoning 提交真实回归；
9. 监督每篇 Stage06、Stage07、Gate、release 和 Agent-visible task 内容；
10. 形成逐篇质量分析报告。

## 5. 实施记录

| 步骤 | 状态 | 说明 |
|---|---|---|
| 现状审计 | completed | 已确认 Prompt 仍是旧 route-disclosure/copy 语义 |
| Stage06 Prompt | completed | 改为只公开作者科学路线；两种模式均自主规划计算；隐藏 protocol 和结果性 artifact |
| Stage07 Prompt | completed | 审计 author-route disclosure、protocol/result 泄露、验证要求和纯计算任务边界 |
| 编排元数据 | completed | Stage06/07 implementation 与 strategy 版本升级 |
| 定向测试 | completed | v19/v20 相关测试与新增 v22 测试共 32 passed |
| 方案一致性审查 | completed | 已搜索旧版本语义，确认 stage06/07 源码无旧策略残留 |
| 五篇真实回归 | completed_with_findings | 3 published、1 scientific_rejection、1 technical_blocked；详见五篇回归报告 |
| 运行结果报告 | completed_with_findings | 已逐篇核对双模式边界、PDF/SI 隔离、evaluator、Gate 与运行轨迹 |

## 6. 五篇回归后的方案一致性复核

回归目录：

`runs/stage0607-v22-gpt-5.6-sol-20260827-dual-mode-five`

已确认的实现一致项：

- release 目录和 `tasks/{task_type}/{paper_id}` 布局符合 v22 设计；论文 PDF/SI 只在
  `release/papers/{paper_id}/documents/`，没有进入 `agent_input`。
- 两种模式均自主规划计算路线；autonomous 在 611/945 中隐藏作者科学路线并要求自主假设或
  搜索；reproduction 暴露作者定性科学路线。
- Stage06 self-check、Stage07 audit self-check 和 external Gate 对已发布的三篇均通过；
  tolerance 仅产生人工复核 diagnostics，不构成机械阻断。
- a556 因输入图结构不可唯一恢复而科学拒绝，符合“不猜测任务定义输入”的边界。

尚未完全一致项：

- `paper_2aca1dd116799b28` 的 reproduction `task.md` 把 `17 > 15 > 16` 及其对应机理方向
  写入公开 objective，属于结果方向泄露。Stage07 当前审计未识别该语义问题；需要按回归报告
  第 4 节加强 author-route/参考答案边界。
- `paper_76ae2dc25f0a5aeb` 的 Agent 在 reproduction self-check 后反复搜索目录，未在预算内
  创建 autonomous 文件。编排器正确地以 `technical_blocked` 拒绝不完整任务，但 Prompt 的
  阶段切换仍需更明确的终止式里程碑。

因此，代码结构和文件合同已基本落地，但在扩大运行前仍应完成上述两个 Prompt/流程层面的
最小修正；不应通过 Gate 黑名单、论文特例或旧版兼容代码绕过问题。

## 7. 当前验证记录

- 旧 v19/v20 相关测试与 v22 新增测试：`32 passed`。
- `src/stages/stage06_task_builder`、`src/stages/stage07_task_judge` 中未发现旧的
  `reproduction_first_same_agent`、v20 Prompt version 或“reproduction 公开 paper
  computational route”的残留定义。
- 当前工作区还有大量与本任务无关的既有修改，提交时只暂存本计划涉及的文件。

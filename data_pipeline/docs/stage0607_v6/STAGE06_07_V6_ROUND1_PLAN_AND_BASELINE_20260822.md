# Stage06/07 v6 Round 1：最小执行顺序 Prompt 调整计划

日期：2026-08-22
目标文档：[STAGE06_07_V6_PROMPT_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260822.md](./STAGE06_07_V6_PROMPT_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260822.md)

## 1. 基线

- 代码基线：`586d4c5 fix(stage06-07): close asset and ranking audit gaps`。
- Stage06A、Stage06B、Stage07 的 Prompt 当前已经包含大量科学边界和合同要求，但职责、修复和最终复核步骤分散在长文本中。
- v5 Round 20 的主要剩余问题是：模型完成修复后漏做局部一致性复核；Stage07 的科学审计、文件修复和最终决定容易相互污染；不同角色对“先判断、再写入、最后复核”的执行顺序不够显式。
- 本轮不把 Round 20 的具体电荷、多重度、组成或数值案例写成规则；这些仍由 Agent 根据源材料判断。

## 2. 本轮问题假设

如果同一个通用的阶段顺序在三个角色 Prompt 中都被明确表达，且不增加科学判断条款，模型更可能：

1. 在写入任务文件前完成一次范围/转换审计；
2. 将 source-backed repair 与科学决定分开；
3. 在最终 receipt 前重新检查受影响文件和状态一致性。

该假设需要用 DeepSeek 与 GPT-5.6-pro 的同轮样本对比验证，不能只根据 Prompt 文本判断成立。

## 3. 计划修改

### 3.1 Stage06A

在现有职责说明之后加入一个紧凑的 `EXECUTION ORDER`：先盘点与选择范围，再写入复现草稿，最后重新读取关键产物并报告未闭合项。保持现有科学规则不变。

### 3.2 Stage06B

在现有转换职责之后加入一个紧凑的 `CONVERSION ORDER`：先检查预置公共树，再执行答案盲转换，最后扫描公共文件并报告语义不确定性。保持 Stage06B 不得改动科学 workflow 和 hidden truth 的边界不变。

### 3.3 Stage07

在现有科学工作流指令之前加入一个紧凑的 `AUDIT ORDER`，明确三个阶段：scientific audit、source-backed repair、final consistency pass。该段只规定时序，不增加化学判决规则。

### 3.4 版本与测试

- 更新三个 Prompt 的版本标识，使缓存和运行轨迹能区分 Round 1。
- 增加最小 Prompt 合同测试，检查三角色都包含时序段，且 Stage07 的 audit 顺序出现在 repair 前。
- 不修改 mechanical gate、Stage00–05、hidden truth 或 evaluator 科学判定逻辑。

## 4. 回归与双模型测试

代码修改后先运行 Stage06/07 定向测试和全量测试。随后从 Stage05 通过集合随机抽取 10 篇：5 篇使用 `deepseek-v4-pro-0813`，5 篇使用 `gpt-5.6-pro`，两组使用完全相同的 Prompt、代码、harness、推理强度和可比并发配置。每篇结果均对照正文/SI，分别归因到代码、Prompt、模型能力和源材料。

## 5. 继续条件

- 如果两个模型都显示相同的 Prompt 时序误解，Round 2 只做一次更小的术语/输出顺序调整；
- 如果问题只出现在一个模型或单篇论文，不添加特例，记录为模型能力或源材料问题；
- 如果出现代码/运输回归，先隔离为通用合同问题，不把科学问题写入代码规则。

## 6. 已完成的代码与测试准备

已实施的修改仅涉及 Prompt 版本和执行顺序：

- Stage06A 增加 `EXECUTION ORDER`；
- Stage06B 增加 `CONVERSION ORDER`；
- Stage07 增加 `AUDIT ORDER`，明确 scientific audit → source-backed repair → final consistency pass；
- 三个 Prompt 版本更新为 Round 1 标识；
- 新增一条模型无关的 Prompt 合同测试，检查时序存在和顺序，不检查具体论文或化学答案。

验证结果：

- Stage06/07 定向回归：`173 passed`；
- 全量回归：`560 passed in 12.79s`；
- `git diff --check`：通过；
- 尚未提交双模型运行任务，等待本轮 Git 版本提交后开始。

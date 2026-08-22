# Stage06/07 v6 Round 3：公共答案扫描 Prompt 修补与三组合回归

日期：2026-08-22

## 1. 触发原因

Round 2 的同批三组合测试显示，最终科学终态一致，但 `paper_525ba02ec147f066` 的已发布 reproduction 表面在不同轨迹中留下了答案性内容：直接的候选排序、100% 目标概率或选择结论。该问题跨模型组合出现，属于 Stage07 最终公共表面审计 Prompt 的执行性缺口；不通过 mechanical gate 添加论文特例规则解决。

## 2. 本轮唯一修改

在 Stage07 Prompt 增加 `MANDATORY FINAL PUBLIC-ANSWER SCAN`：

- 在批准前逐文件检查 `paper_reproduction/` 与 `autonomous_research/` 全部 Markdown、JSON、manifest、workflow metadata、route map、rubric、文件名和输入头；
- 从 hidden reference 和审计证据动态派生 target values、tolerances、rankings/trends、preference propositions 和 conclusion statements；
- 明确禁止把答案伪装进 `supported_primary_claims`、`target_definition`、`why_this_subworkflow_is_core`、`workflow_spec`、rubric title 或 route-navigation prose；
- 要求 `scientific_audit_table` 增加 `public_answer_leakage` 行，只有两个 public roots 都闭合才可 `disclosure_status=passed`。

不修改 mechanical gate 的科学判断，不增加论文名、分子名、固定数字或关键词规则；不修改 Stage06 的科学选择逻辑。

## 3. 回归测试

使用 Round 2 的同批 5 篇作为受控回归样本，三种配置在同一 shell 同时提交，便于直接比较 Prompt 修补前后和 Stage06/Stage07 模型组合：

1. DeepSeek→DeepSeek：`stage06-07-v6-round3-pubscan-same5-deepseek-deepseek-20260822`
2. GPT→GPT：`stage06-07-v6-round3-pubscan-same5-gpt-gpt-20260822`
3. DeepSeek→GPT：`stage06-07-v6-round3-pubscan-same5-deepseek-gpt-20260822`

使用 Codex harness、high reasoning、并发 5；GPT 使用 `gpt-5.6-sol` 的 `reasoning.mode=pro`。论文集合和 Round 2 相同：

`paper_5be4368e659d4b40`、`paper_9774cf028b321785`、`paper_75221561972a5c9c`、`paper_f171fa1f83158f7c`、`paper_525ba02ec147f066`。

## 4. 验收

- 代码回归测试保持通过；
- 三组终态、机械状态和 schema 状态完整；
- 重点检查 `paper_525ba02ec147f066` 两个 public roots 是否不再出现答案性排序/数值/结论；
- 其余论文逐篇确认整篇主线优先、核心子流程降级、输入闭合和软件缺口登记；
- 只有公共答案泄漏在不同论文/组合中仍重复，才继续调整 Prompt；单篇源材料或模型输出差异归入观察项。


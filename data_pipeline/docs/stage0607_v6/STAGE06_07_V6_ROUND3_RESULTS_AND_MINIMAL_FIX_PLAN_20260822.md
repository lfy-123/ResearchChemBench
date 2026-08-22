# Stage06/07 v6 Round 3：三模型组合结果、责任判断与最小修复方案

日期：2026-08-22

## 1. 测试范围

本轮同时运行同一批 5 篇论文，使用 Codex harness、high reasoning、并发 5：

| 组合 | 结果目录 |
|---|---|
| DeepSeek → DeepSeek | `runs/stage06-07-v6-round3-pubscan-same5-deepseek-deepseek-20260822` |
| GPT → GPT | `runs/stage06-07-v6-round3-pubscan-same5-gpt-gpt-20260822` |
| DeepSeek → GPT | `runs/stage06-07-v6-round3-pubscan-same5-deepseek-gpt-20260822` |

三组均正常退出，15/15 论文流程完成；没有出现 API、批处理状态或 evaluator schema import 的普遍故障。

## 2. 结果概览

| 论文 | DeepSeek→DeepSeek | GPT→GPT | DeepSeek→GPT | 科学判断 |
|---|---|---|---|---|
| `paper_525ba02ec147f066` | approved，但机械阻断 | published | published | DP4+ compound-5 核心子流程可闭合 |
| `paper_f171fa1f83158f7c` | published | scientific reject | published | TD-DFT/ECD 子流程依赖模型对资产闭合的判断 |
| `paper_75221561972a5c9c` | published | scientific reject | scientific reject | 周期吸附/DOS 路线缺失必要输入时拒绝合理 |
| `paper_5be4368e659d4b40` | scientific reject | scientific reject | scientific reject | 周期界面/Ru/缺陷/磁态参考态不足，拒绝合理 |
| `paper_9774cf028b321785` | scientific reject | scientific reject | scientific reject | TS 电荷/多重度和成对结构不足，拒绝合理 |

GPT→GPT 与 DeepSeek→GPT 都通过了 `paper_525...` 的机械检查；DeepSeek→DeepSeek 的同一任务只因下述无效私有 profile 被阻断。这说明 gate 对适用 mode 的过滤逻辑本身已经存在，不能把该事件继续归因成“gate 没有过滤 applies_to_modes”。

## 3. `ap_gt_private_alias` 的责任判断

DeepSeek→DeepSeek 的 hidden reference 中有 5 个 Ground Truth/profile，其中前 4 个适用于 `paper_reproduction` 和 `autonomous_research`，额外的 `ap_gt_private_alias` 和 `gt_private_alias` 只声明 `hidden_reference_only`，绑定的是 `$.private_source_mapping`。

当前 gate 的行为是：

1. 对每个 public mode 调用 `_profile_applies_to_mode()`；
2. 未声明 scope 视为 shared，声明 public mode 子集则只检查适用 mode；
3. `hidden_reference_only` 不是公开 mode，当前 `_mode_scope()` 将它报告为非法 scope；
4. 因而产生 `evaluator_acceptance_profile_mode_scope_invalid` 并阻止发布。

这个阻断不是误报：该 profile 不能被任一公开 evaluator 评分，也不应出现在公开 mode 的投影中。它是 Stage06 hidden-reference builder/Stage07 audit 没有清除“私有证据项被误建成 acceptance profile”的合同问题。把 gate 改成无条件接受会使无效 profile 静默留在 private Ground Truth，反而掩盖问题。

同时，Round 3 证明 `_profile_applies_to_mode()` 对合法的 reproduction-only、autonomous-only、shared profile 已按适用 mode 过滤；下一轮只增加回归测试，不重写这段逻辑。

## 4. 本轮未发现的代码缺陷

- 三组 batch 均正常完成，`failed_count=0`；
- evaluator registry 在已发布任务中可加载，未出现普遍 schema failure；
- approved-but-mechanical-blocked 状态已写入 `audit_results.jsonl`，没有静默发布；
- 本轮公共答案扫描已执行，DeepSeek→GPT 两个发布任务显示 `public_answer_leakage=closed`；GPT→GPT 和 DeepSeek→DeepSeek 的 `paper_525...` 审计记录仍可能将该行记为 `repairable`，但最终发布表面中没有发现 Round 2 的直接排序/目标数值残留；这属于 Agent 对“修复后状态”措辞不一致，暂不增加代码规则。

## 5. 最小修复方案

### 5.1 Stage06 hidden-reference Prompt

明确 acceptance profile 的公共作用域只能是：

- `paper_reproduction`；
- `autonomous_research`；
- 两者的并集。

不得创建 `hidden_reference_only`、`private_only` 或其他非公开 mode 的 Ground Truth/profile。私有候选映射、作者标签和答案性 source mapping 必须写入 `private_evidence_map.json`，不能写成可评分 Ground Truth。每个 profile 必须恰好对应一个选定的、至少适用于一个公开 mode 的 Ground Truth item。

### 5.2 Stage07 audit Prompt

在 mode-specific binding 检查和最终 evaluator dry-run 前增加同一条通用检查：

- 枚举 hidden reference 的 truth/profile；
- 删除或修复没有任何公开 mode 适用范围的 orphan profile/truth；
- 不改变冻结的科学目标，只把私有映射移回 `private_evidence_map.json`；
- 重新确认每个公开 profile 对每个适用 mode 有真实 binding；
- 若不能在不猜测科学内容的情况下修复，返回 findings/reject，不报告 contract passed。

这不是论文特例，也不把科学中心性下沉到代码；它是 Ground Truth 与 evaluator 公共 mode 的通用合同审计。

### 5.3 公共答案扫描状态的一致性

GPT→GPT 的 `paper_525...` 审计把 `public_answer_leakage` 行保留为 `repairable`，同时又报告
`disclosure_status=passed` 并发布。最终文件已经没有 Round 2 中的直接答案残留，因此这不是发布内容的
新泄漏，但它是 Stage07 receipt Prompt 的状态语义执行不一致。已在 Prompt 中补充：修复后必须重新扫描并
将该行改为 `closed`；`repairable` 与 `disclosure_status=passed` 不能同时出现。暂不把这项下沉为
机械 gate 的论文内容规则。

### 5.4 代码回归覆盖

增加轻量测试覆盖：

1. reproduction-only profile 不被 autonomous gate 检查；
2. autonomous-only profile 不被 reproduction gate 检查；
3. shared profile 两个 mode 都被检查；
4. 非公开 scope（如 `hidden_reference_only`）被明确报告为 invalid，而不是被静默忽略。

不修改 `_profile_applies_to_mode()` 的现有语义，不为 `paper_525...` 添加固定 ID、分子名或数字规则。

## 6. 下一轮验收

先运行完整 Stage06/07 单元回归；随后仍使用同一批 5 篇同时提交三组组合，确认：

- DeepSeek→DeepSeek 不再因 orphan private profile 机械阻断，或在 Stage07 明确拒绝/修复并留下可见原因；
- 三组合法发布任务的 evaluator dry-run 均通过；
- 公共答案扫描持续有效；
- 科学拒绝仍由论文输入闭合性决定，而不是被机械规则替代。

只有该受控回归通过后，才扩大到随机论文比较模型组合差异。

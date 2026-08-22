# Stage06/07 v5 Round 13 实施与测试记录

日期：2026-08-22

代码基线：`5dbccc6`

总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 本轮问题来源

Round 12 的 10 篇测试中，Stage06A 的科学方向约 9/10，但有 3 篇在 Stage06B 因同一种工作区运输问题失败：

- 普通 shell 已成功，Agent 却被 optional code-mode host 的错误事件干扰并误判 shell 不可用；
- Agent 或恢复过程把整个 `paper_reproduction/` wrapper 嵌套复制到 autonomous 输出根目录；
- 顶层任务文件缺失，Stage06B semantic validator 正确拒绝了不完整输出。

另有一个 Prompt 边界问题：闭合候选中相对最中心的流程，如果仍然只是论文最终主张的辅助证据，不能替代不闭合的直接核心流程。

## 2. 实施内容

### 2.1 Stage06B 运输职责前置

- `_setup_converter_inputs()` 将 reproduction 公开树的**内容**直接预置到可写的
  `outputs/autonomous_research/`；Stage06B 只编辑正确根目录中的现成任务。
- 新增 `_ensure_converter_output_scaffold()`，在恢复合并后：
  - 提升并移除确定错误的嵌套 `paper_reproduction/` wrapper；
  - 保留已经存在的顶层语义编辑；
  - 只补齐缺失的必需公开文件和缺失的输入树。
- converter validator 显式拒绝 `paper_reproduction/` 和 `conversion_packet/` wrapper 残留。

这部分只处理目录运输和必需文件存在性，不执行科学脱敏、任务选择或答案判断。

### 2.2 Codex 工具面降噪

- Codex harness 新增可配置的 `codex_disable_code_mode`。
- Stage06/07 默认显式传入 `--disable code_mode --disable code_mode_host`。
- 普通 shell 和文件系统工具不受影响。

### 2.3 Prompt 对齐

- Stage06B 明确输出树已经预置，禁止再次复制整个输入树或创建嵌套 wrapper。
- Stage06A/Stage07 使用一致的通用中心性边界：仅仅是“所有闭合候选中最中心”仍不够；若所选流程对最高中心性论文主张只是 supporting-only evidence，而直接流程不闭合，应拒绝该论文而不是包装外围片段。

## 3. 代码审查与回归

- 新增/更新测试覆盖：预置输出根、嵌套 wrapper 恢复、wrapper validator、Codex feature 参数及 Prompt 合同。
- Stage06/07 定向回归：`165 passed`。
- 全量回归：`552 passed`。
- `git diff --check`：通过。
- 通用性检查：代码和 Prompt 没有论文 ID、特定分子、特定软件或固定科学答案规则。

## 4. 职责边界复核

- Stage06A：仍负责科学范围选择、闭合论证和任务构建；
- Stage06B：仍只负责从 reproduction 公开面转换 autonomous 公开面；
- Stage07：仍负责独立科学审计、必要修复和批准/拒绝；
- 代码：只负责确定性的工作区运输、恢复、结构验证和工具配置。

本轮不启用 Stage07B，因为 Round 12 的稳定失败簇发生在 Stage06B 交付之前，并非 Stage07 审计后仍需简单合同修复的任务。

## 5. Round 13 批次

待运行：`gpt-5.6-sol`、high、Codex harness、随机新 10 篇、并发 10。批次结束后在本文补充逐篇正文/SI 对照、各角色行为、严格端到端结果和下一轮决定。

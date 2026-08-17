# Stage06/07 Agent Authority — Round 2

## Round 1 真实测试

- 代码：`960a2d4`
- 论文：`paper_6904a9c8c09855cc`
- 模型：`deepseek-v4-pro-0813`
- 输出：`runs/stage06-07-agent-authority-round1-20260818-paper6904-pro0813`
- Stage06：`provisional_constructed`，选择 `core_scientific_subworkflow`，复杂度 `high`。
- Stage07 Agent：`approved_with_repairs`，保留原 workflow，完成机械字段、公开面泄漏、复现路线和 Ground Truth 对齐修复。
- 最终管线：错误地变成 `objective_failure_retryable`。

### 已确认的代码缺陷

1. Agent 已批准后，`_publish_mode_bundles()` 再调用 `validate_mode_task()`，以 `reproduction_route_fidelity_evidence_missing` 覆盖 Agent 决策。这不是模型能力问题。
2. Stage06 写入 20 条 hard mechanical findings，Stage07 Prompt 又要求读取它。Agent 因而搜索系统目录寻找 validator 并修复重复合同字段，使用 71 次工具调用和约 418.6 万 tokens，偏离科学审计。
3. Stage07 完成 Agent 审计后仍运行合同报告、工具箱重对齐、verified snapshot 内容读取等代码侧语义操作，增加复杂度和新的失败面。
4. 发布器使用固定文件 allowlist，而不是原样复制 Agent 决定的 mode task；这会静默丢弃 Agent 认为必要的文件。

## Round 2 修改

1. 删除 Stage06 `stage06_contract_findings.json` 的生成和 record 中对应统计，不再把机械合同当作 Stage07 工作清单。
2. Stage07 不再读取或生成 `task_pair_contract_report`，不修改 Agent 返回的 contract/disclosure 状态。
3. `_publish_mode_bundles()` 只做 mode 目录隔离复制，不运行 `validate_mode_task()`，不使用固定任务文件 allowlist。
4. 发布目录排除内部 `public_manifest.json`，不额外写入面向被评估 Agent 的内部审计文件；隐藏答案仍只进入独立 evaluator registry。
5. evaluator registry 缺少可选映射文件时采取 best-effort 跳过，不覆盖 Agent 科学决策。
6. 删除 verified snapshot 的内容读取和代码推断；恢复仍使用 Agent 已写的 workspace artifact。
7. 保留最小 transport 安全：workspace-relative artifact 路径、非空目录、禁止嵌套 `stage06_candidate`。

## 验收

- Agent 返回 approved 且交付安全非空目录后，发布器不得用内容 validator 改判。
- Stage07 Prompt/输入不再出现 Stage06 hard contract findings。
- 公开 mode bundle 来源于 Agent mode 目录，不含 sibling mode、hidden reference 或内部 handoff。
- 全量 pytest 通过。
- 使用同一论文和 `deepseek-v4-pro-0813` 重新测试；记录工具调用、token、Agent decision 和管线 decision。

## 执行记录

| 版本 | Git commit | 测试状态 | 结果 |
|---|---|---|---|
| Round 2 | 待提交 | 待运行 | 待运行 |


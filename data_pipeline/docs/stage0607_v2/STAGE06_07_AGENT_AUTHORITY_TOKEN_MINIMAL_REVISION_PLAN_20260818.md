# Stage06/07 Agent Authority and Minimal Recovery — Round 1

## 目标

本轮只修复通用架构缺陷，不针对任何单篇论文添加规则。Stage06/07 的科学判断仍由 Agent 完成；编排器只负责隔离工作区、复制文件、保存运行记录和发布 Agent 已选择的结果。

## 本轮修改

1. Stage07 不再使用 `task_pair_contract_report`、changed-files 对比或其它内容检查作为 Agent 决策的硬门禁。诊断报告可以保留为非权威观察，但不得把 Agent 的批准改成重试或拒绝。
2. Stage07 接收批准结果时只验证安全的 artifact 定位和非空文件树；不要求自然语言最终消息包含完整科学 JSON。Agent 运行器的结构化响应或内部 `outputs/stage07_audit.json` 作为 receipt 来源。
3. Stage07 recovery 不重复复制完整 source snapshot。初始输入使用精简 source packet；恢复尝试优先复用上一轮 task tree、精确失败上下文和相关证据，必要时才带回完整材料。
4. Stage06B 只读取论文复现 public task、共享输入和转换说明，不读取 hidden reference、ground truth 或完整 Stage06 内部合同；conversion report 只作为内部运行记录，不进入公开任务。
5. Prompt 明确：优先修复 Stage06 选定的核心科学 workflow；只有该 workflow 有证据支持的不可修复阻塞时，才由 Agent 自主选择另一条完整且重要的 workflow。

## 不做的事

- 不新增针对测试论文的 molecule、文件名、数值或 workflow 规则。
- 不用代码判断科学问题是否重要、任务是否可复现或是否通过。
- 不改变 Stage06/07 的 Agent 模型协议或工具箱内容。
- 不把内部 receipt、合同、来源记录复制到公开任务目录。

## 验收

- 相关 Stage06/07 单元测试和完整 pytest 通过。
- 发生机械诊断 findings 时，Stage07 不再自动触发 `invalid_phase_contract` 重试。
- Agent 明确批准且交付非空 task tree 时可以发布，即使非权威诊断仍有 findings。
- recovery 输入不包含重复的完整 source snapshot，且仍保留 Agent 解决问题所需的证据入口。
- Stage06B 不可见 hidden reference/ground truth。

## 执行记录

| 轮次 | Git commit | 测试论文 | 模型/结果 | 发现 | 后续 |
|---|---|---|---|---|---|
| Round 1 | 待提交 | `paper_6904a9c8c09855cc` | 待运行 | 待运行 | 根据通用问题决定是否进入 Round 2 |


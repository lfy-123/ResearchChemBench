# Stage06/07 通用代码缺陷修复方案（2026-08-17）

## 目标

本轮只修复编排器、发布门禁、数据完整性校验、工具箱事实匹配和可观测性问题，不针对六篇测试论文写特例，也不替 Agent 做科学路线选择。

工具箱只向 Stage06/07 提供已安装软件清单。软件匹配按 `software_id`、显示名和 alias 判断；软件版本号不参与缺失判断，也不比较版本号。预设 Action 不进入两个阶段的判断。

## 修改项

### 1. Stage07 发布前重新执行确定性任务树审计（P0）

在 Agent 完成修复和 autonomous public-surface guard 之后，对最终 `outputs/task_pair` 执行 `validate_task_pair`。把结果写入最终 receipt，并将确定性 findings 与 Agent outcomes 合并。

若批准结果仍有任务树结构、公共输入、Ground Truth、双模式一致性、路线隔离或 evidence 完整性问题，则禁止发布为 approved；输出可追溯的 Stage07 rejection 记录。单纯的软件缺口不阻断发布，而标记为 `needs_software`。

### 2. Guard 修改后重新计算审计语义（P0）

Guard 只能做机械的文件规范化；规范化完成后必须重新生成最终审计摘要、findings、outcomes、toolbox 状态和 repair 记录，避免 receipt 描述修改前的任务树。

### 3. 新 repair 路径增加 Agent receipt 语义校验（P1）

`stage07_audit_repair` 使用和旧 objective audit 相同的 `validate_agent_audit` 合同检查，但不把模型科学判断硬编码为代码规则。

### 4. 增加通用输入 artifact 完整性检查（P1）

对 `task_spec.input_assets` 对应的公共输入文件执行通用检查：文件非空、JSON/文本不为明显占位内容、结构化 JSON 不得完全由 null/空值组成。该检查不解析具体化学含义。

### 5. 增强 Ground Truth 占位检查（P1）

识别“待从 SI 提取”“后续补充”“TBD”等说明性字符串，防止它们被当成 canonical answer。真实数值、类别、结构或文字命题继续允许作为 Ground Truth。

### 6. 增加最终 evidence ID 全量扫描（P1）

递归扫描最终任务树中 `evidence_id(s)`、`source_evidence_ids`、`evidence_refs` 字段，并与最终 `evidence_index.json` 对比。未知 ID 作为发布前完整性问题。

### 7. 工具箱按 canonical ID/alias 匹配，忽略软件版本（P1）

根据 Stage07 输入的只读 `installed_software` 清单，建立规范化软件名匹配：忽略大小写、空格、标点和版本后缀，并使用清单中的 aliases。Gaussian09、Gaussian16、G09、G16、Gaussian 统一视为 Gaussian 软件条目；不得因为版本字符串不同而标记缺失。

工具箱缺口只生成 `needs_software` 和建议清单，不改变科学通过/拒绝结论。

### 8. 明确 Stage06 provisional 状态语义（P1）

保留 Stage06 将草稿交给 Stage07 修复的设计，但将 `provisional_constructed` 与科学通过状态分开记录，避免 `passed=true` 被误解为最终可发布。Stage07 仍可接收 provisional handoff。

### 9. 减少 Stage07 工作区的重复材料（P2）

保留 Stage06 candidate 和 source materials 的职责边界；避免将同一份源材料重复嵌套到 task pair 中。该项只做通用路径/复制整理，不按论文名称删除文件。

### 10. 增加阶段级状态心跳（P2）

在 Stage06/07 的论文 workspace 写入稳定的阶段、phase、attempt、最后更新时间和错误类别，便于监测运行，不再依赖只有启动/结束时间的顶层状态。

## 验收标准

1. Agent 返回批准后，最终任务树仍必须通过确定性审计才可进入 `audited_tasks`。
2. Agent receipt 与最终文件事实一致；Guard 后重新生成审计摘要。
3. Gaussian09/G16 等版本别名在已安装 Gaussian 条目存在时不再产生软件缺口。
4. 软件缺失只产生 `needs_software`，不会单独导致科学 rejection。
5. 空数据、全 null 数据、明显占位 Ground Truth、未知 evidence ID 不得被发布为 approved。
6. 不添加论文、分子、软件或路线特例；不向 Agent 暴露预设 Action。
7. 六篇测试的每一轮结果、代码版本、发现的问题和后续修复记录到单独的迭代日志。


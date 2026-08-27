# Stage06/07 v27 终态协议、Gate 边界与并发调度修改方案

## 1. 目标

v27 针对 v26 回归中暴露的两个技术阻断进行修复，并明确各层职责：

1. 科学不可构建的论文必须正常结束为 `scientific_rejection`，不能因缺少终态文件被误记为 `technical_blocked`；
2. Stage07 的科学审计、修复结果、`workflow_review` 和机械 Gate 必须状态闭合；
3. 不通过开放 `rm` 权限解决 Agent 文件操作问题；
4. Common Gate 只验证发布包的机械完整性，不承担科学可行性决策；
5. 保持每篇论文内部 Stage06 → Stage07 的顺序，同时让批量任务采用并发槽位滚动调度。

本方案不增加 Stage08，不恢复 Stage07B，不引入旧 ID 或兼容投影。

## 2. 失败根因归纳

### 2.1 `paper_3590deded767345e`

Agent 已完成 `workflow_review.json`，并正确判断两种模式均不可构建，但没有写
`construction_receipt.json`。Stage06 编排器把“科学拒绝分支没有终态回执”当成 Agent artifact 缺失，导致进程等待并最终成为技术失败。

根因是拒绝分支终态协议不明确，而不是工具调用上限或 API 失败。

### 2.2 `paper_9ec8c4761c4f171b`

Stage07 的科学修复内容基本正确，但文件操作和状态写回没有闭合：

- Agent 执行 `rm -rf` 被安全策略拒绝；
- 文本 patch 依赖脆弱上下文，多次定位失败；
- Agent 将 `workflow_review.decision` 写成未定义的 `audited_with_repairs`；
- `audit_receipt.json` 声称已批准，但 audited artifact 的 workflow review 仍包含失败状态；
- external Gate 因此阻断。

根因不是单一的 `rm` 失败，而是“修复工具不稳定 + 状态枚举没有分层 + 修复后没有保证单一状态来源”。

## 3. 终态协议

### 3.1 Stage06 成功分支

当至少一个模式可行时，Agent 必须最后写入并返回完全一致的：

```text
outputs/construction_receipt.json
```

回执中的 `decision` 必须为：

```text
constructed
```

并包含实际 `release_modes`、feasibility、self-check 和 common Gate 已完成的信息。

### 3.2 Stage06 科学拒绝分支

当两个模式均不可行时，Agent 仍然必须最后写入并返回完全一致的：

```text
outputs/construction_receipt.json
```

回执格式固定为：

```json
{
  "decision": "scientific_not_constructible",
  "paper_id": "...",
  "artifact_path": "outputs/workflow_review.json",
  "release_modes": [],
  "milestones": {"feasibility": "failed"},
  "failure_code": "...",
  "failure_reasons": [],
  "summary": "..."
}
```

该分支不得创建任务目录、evaluator 目录或 `paper_route.md`。编排器读到合法的科学拒绝回执后，直接将论文标记为 `scientific_rejection`，不再要求普通任务文件通过发布 Gate。

### 3.3 Stage07 终态

Stage07 只接受以下四种 `audit_decision`：

```text
approved
approved_with_repairs
rejected_scientific_unrepairable
technical_blocked
```

`audit_decision` 只写入 `audit_receipt.json`，不能写入 `workflow_review.decision`。

Stage07 修复后，`workflow_review.decision` 必须保持 Stage06 的合法值：

```text
candidate_ready
```

不能使用 `audited_with_repairs`、`repaired` 等新的 workflow decision。是否修复由 `audit_receipt.audit_decision` 和 `repairs` 表达。

## 4. 科学拒绝由谁承担

科学决策不由 Common Gate 承担：

### Stage06

Stage06 负责第一次 feasibility 判断：

- objective 是否可计算；
- public inputs 是否闭合；
- evaluator 是否有来源依据；
- investigation 是否能复现；
- 每个模式是否可行。

两种模式都不可行时，Stage06 输出 `scientific_not_constructible`。

### Stage07

Stage07 负责最终科学审计：

- 检查任务指令、输入、schema、evaluator 的科学合同；
- 修复不改变 scientific objective 的问题；
- 对无法修复的科学缺陷输出 `rejected_scientific_unrepairable`；
- 对已修复且机械完整的任务输出 `approved_with_repairs`。

### 编排器

编排器只做状态映射和文件装配：

- Stage06 `scientific_not_constructible` → `scientific_rejection`；
- Stage07 `rejected_scientific_unrepairable` → `scientific_rejection`；
- Stage07 `approved/approved_with_repairs` + Mechanical Gate 通过 → `published`；
- 缺文件、JSON 损坏、修复 artifact 不存在或进程异常 → `technical_blocked`。

编排器不得根据自己的科学判断重建任务。

## 5. Gate 边界（已确认）

本版本明确采用以下职责边界：`feasibility` 和 `task_quality` 的科学判断交给 Stage06/Stage07 Agent；Common Gate 不根据它们决定科学拒绝。Common Gate 只负责机械包完整性、安全隔离和 runtime 可读取性。科学拒绝必须通过 Stage06/Stage07 的合法 receipt 产生，而不是由 Gate 推断。

### 5.1 Common Mechanical Gate 负责

Common Gate 只检查发布包能否被 runtime 安全读取：

- 必须文件和目录存在；
- JSON 可解析；
- 路径安全、无越界和 symlink；
- submission schema 可读取；
- required files、primary result file 和基本 binding 路径存在；
- evaluator 文件存在且结构可解析；
- agent_input 不包含 PDF、SI、evaluator、paper route 或源论文文件；
- package manifest 和 release 装配可完成。

Gate 可以做最小的结构闭合检查，但不判定科学真值、科学中心性、输入合理性、机制正确性、tolerance 质量或模式公平性。

### 5.2 Common Gate 不负责

以下决策由 Stage06/Stage07 Agent 负责，不能再次由 Common Gate 作为科学阻断条件执行：

- feasibility closure 是否科学上通过；
- scientific objective 是否合理；
- 输入是否足以完成科学研究；
- 过程关键点和最终结论是否科学充分；
- reproduction/autonomous 是否泄露路线；
- evaluator 的科学参考答案是否正确。

`workflow_review` 仍然保存为审计证据，但其科学状态不再由 Common Gate重复裁决。

## 6. workflow_review 单一来源和一致性

### Stage06 输出

Stage06 的 `workflow_review.decision` 只能是：

```text
candidate_ready
scientific_not_constructible
```

### Stage07 输出

Stage07 不改变 `workflow_review.decision` 的枚举和值：

- `candidate_ready` 继续表示存在已选定的可审计模式；
- Stage07 是否修复由 `audit_receipt.audit_decision` 表达；
- task_quality 修复状态写在 `workflow_review.task_quality`，但不能新增 decision 枚举。

### 编排器一致性校验

在装配 release 前，编排器必须检查：

1. `audit_receipt.paper_id` 与 workflow review 一致；
2. `audit_receipt.release_modes` 与 workflow review 的 `feasibility.release_modes` 一致；
3. approved/approved_with_repairs 时 workflow review.decision 为 `candidate_ready`；
4. `rejected_scientific_unrepairable` 时不得装配任务；
5. `technical_blocked` 不得装配任务；
6. 实际 audited artifact 重新读取后的状态与 receipt 一致。

## 7. Stage07 文件修复方式

不开放 Agent 的 `rm -rf` 权限。原因是开放删除权限会扩大工作区破坏范围，不能解决状态和 patch 不一致问题。

采用以下方式：

1. 编排器在 Agent 启动前创建隔离的空 audited 输出目录；
2. 将 Stage06 candidate 复制为只读输入；
3. Agent 只能在 audited 输出目录中增量写入或完整重写文件；
4. 对 JSON 提供安全的读取/重写工具，避免依赖长文本 patch；
5. 如果需要重建目录，由编排器执行受控的目录替换，而不是 Agent 执行 `rm -rf`；
6. 修复完成后，Agent 必须重新读取实际文件、运行 Gate 并写出 receipt；
7. 编排器再次读取 audited artifact，不能只相信 Agent 的 repair summary。

## 8. 并发调度语义

当前批处理使用 `ThreadPoolExecutor(max_workers=max_parallel)`：

- 所有选中的论文 future 会一次性提交；
- 同时运行的论文数最多为 `max_parallel`；
- 每篇论文内部仍严格执行 Stage06 完成后再执行 Stage07；
- 某篇论文完成后，其并发槽位立即释放，等待队列中的下一篇论文马上开始；
- 不需要等待当前全部论文完成后才开始下一篇；
- 只有最终 batch 汇总和 release consolidation 会等待所有 future 终态。

因此：

- 10 篇论文、并发 10：十篇同时启动；
- 20 篇论文、并发 10：先运行 10 篇，任意一篇结束后立即补充下一篇；
- 并发 10 不是“十篇完成后再启动下一批”，而是滚动窗口。

并发提高可能增加 API 排队、429、5xx、连接超时、本地 bridge/内存和临时文件压力。v27 不加入盲目 retry；批量前应通过 4→8→10 的容量探测选择稳定值。

## 9. 代码修改范围

### Stage06

- 明确成功和科学拒绝都必须写 `construction_receipt.json`；
- 编排器增加合法科学拒绝回执的终态映射；
- 保留 Stage06 的 scientific feasibility 责任；
- 更新 implementation version，避免输出继续标记为 v25。

### Stage07

- 将 workflow review decision 限制为 Stage06 合法枚举；
- 禁止写入 `audited_with_repairs`；
- 将修复状态只放在 `audit_receipt.audit_decision` 和 `repairs`；
- 改进 audited workspace 初始化和 JSON 安全写入；
- 修复后重新读取真实 artifact 并校验 receipt 一致性。

### Common Gate

- 从科学 Gate 转为 Mechanical Gate；
- 保留文件、JSON、schema、路径、安全隔离和最小引用结构检查；
- 不再依据 workflow_review 的 scientific feasibility/task quality 直接做科学拒绝；
- 将科学检查结果保留为 diagnostics 或 Stage06/07 receipt 内容。

### 测试

新增定向 fixture：

1. scientific rejection 有 construction receipt，批次结果为 scientific_rejection；
2. scientific rejection 缺少任务目录不触发普通任务 Gate；
3. Stage07 approved_with_repairs 保持 workflow_review.decision 为 candidate_ready；
4. 非法 `audited_with_repairs` 被 receipt/schema 校验拒绝；
5. receipt、workflow review、release modes 不一致时技术阻断；
6. Agent 修复不需要 `rm -rf`；
7. Mechanical Gate 不因 scientific feasibility 或 task quality 标签失败而阻断已通过 Stage07 的包；
8. max_parallel 小于论文数时，完成一个任务后立即启动队列下一任务。

## 10. 验收标准

v27 通过验收需要满足：

- `paper_359...` 类型的科学拒绝不会因缺少回执而挂起；
- `paper_9ec...` 类型的 Stage07 修复不会依赖开放 rm 权限；
- workflow_review 不再出现未定义 decision；
- 科学拒绝由 Stage06/Stage07 承担，Common Gate 不做科学裁决；
- 机械 Gate 仍能阻断真正缺文件、格式错误和信息泄露；
- 单篇内部 Stage06→Stage07 顺序不变；
- 批量并发采用滚动槽位，不必等待整个 batch 才启动下一篇；
- 发布任务的结构和 agent_input 隔离保持不变。

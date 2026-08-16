# Stage06/Stage07 候选构建、修复审计与工作流重设计修改方案

> 日期：2026-08-16
> 版本：stage06-provisional-builder-stage07-repair-first-v1
> 状态：用户已确认，正在按本方案实施
> 适用范围：`src/stages/stage06_task_builder/`、`src/stages/stage07_task_judge/`、
> `src/late_stage_runner.py`、Agent schema、配置、测试和运行文档

## 1. 修改目标

本方案将两个阶段重新划分为：

- Stage06 是候选评估任务构建器，不是最终有效性裁判；
- Stage07 是最终科学审计、任务修复和必要时工作流重设计 Agent；
- 代码只负责工作空间、文件传递、状态、恢复和客观故障，不判断评估任务的科学有效性；
- Stage07 必须优先修复 Stage06 已选择的工作流，不能一开始就寻找另一个更容易的工作流；
- 只有确认 Stage06 工作流存在不可修复的科学阻断后，Stage07 才能选择论文中的其他完整工作流；
- 如果替代工作流构建成功，使用独立状态 `approved_after_workflow_redesign`；
- 工具箱暂缺软件不导致论文或任务被拒绝，只记录 `needs_software`。

## 2. 总体结构

~~~text
论文 PDF / 全部 SI / 解析正文 / 表格 / 坐标 / 工具箱快照
                              |
                              v
                    Stage06 Builder Agent
                              |
                +-------------+-------------+
                |                           |
                v                           v
     provisional_constructed    provisional_not_constructible
                |                           |
                +-------------+-------------+
                              |
                   复制到独立 Stage07 workspace
                              |
                              v
                 Stage07 Audit-Repair Agent
                              |
              优先审计并修复 Stage06 原工作流
                              |
                 +------------+------------+
                 |                         |
                 v                         v
           原工作流可修复             原工作流不可修复
                 |                         |
                 v                         v
      approved / approved_with_repairs   搜索其他完整工作流
                                           |
                              +------------+------------+
                              |                         |
                              v                         v
                    找到完整替代工作流          没有完整替代工作流
                              |                         |
                              v                         v
          approved_after_workflow_redesign  rejected_scientific_unrepairable
~~~

Stage06 的原始产物和轨迹永久保留。Stage07 只修改复制到自己工作空间的副本，最终任务从
Stage07 的输出目录发布。

## 3. 代码侧职责边界

### 3.1 代码不再判断的内容

Stage06 和 Stage07 的运行代码不再根据机械规则判断：

- 计算工作流是否科学完整；
- workflow scope 是否选择正确；
- 任务是否足够复杂；
- Ground Truth 是否充分；
- Acceptance Profile 或 rubric 是否科学合理；
- 自主科研模式是否泄漏论文路线；
- evidence ID 是否足以支持某个科学结论；
- 两种模式的科学内容是否一致；
- 论文是否可复现或应被拒绝。

当前 `_task_pair_builder_phase_findings()`、`validate_workflow_review()`、
`validate_task_pair_draft()`、`validate_task_pair()`、`deterministic_stage07_audit()` 等科学或内容
有效性检查不再参与运行时的通过/拒绝决策。为便于离线诊断，可以暂时保留这些函数，但不得
阻断 Stage06 进入 Stage07，也不得覆盖 Stage07 Agent 的最终科学结论。

### 3.2 代码仍保留的技术检查

代码只检查管线是否正常工作：

- Agent 进程是否正常退出；
- receipt 是否为可解析的结构化 JSON；
- Agent 声明的输出路径是否位于当前独立 workspace；
- 输入只读目录和输出可写目录是否正确隔离；
- 是否至少存在可交给下一阶段的候选目录或失败报告；
- Stage06 到 Stage07 是否通过复制目录传递信息；
- Hidden Reference 是否被操作系统级目录复制逻辑直接放进公开任务目录；
- API、harness、PDF、文件系统、磁盘空间和解析服务是否发生客观故障；
- checkpoint、resume 和原子目录发布是否成功。

这些检查失败时只能产生客观或交付失败，不能产生论文科学拒绝。代码可以计算文件 hash 和
manifest 用于追溯，但不能因为科学内容 hash、字段或语义不符合机械规则而拒绝任务。

## 4. Stage06 修改方案

### 4.1 Stage06 的职责

Stage06 继续由一个 Builder Agent 完成：

1. 以论文 PDF、全部 SI 和解析内容为主要依据；
2. Stage02–05 结果只作为检索提示；
3. 抽取论文作者实际执行的计算化学过程；
4. 优先选择整篇论文的完整计算流程；
5. 若整篇流程确有缺口，再选择最大、完整、非平凡的子流程；
6. 先生成论文复现模式；
7. 复制论文复现模式目录，再修改为自主科研模式；
8. 为两种模式生成相同的输入、Ground Truth、Acceptance Profile 和结论评分；
9. 记录工具箱需求和缺失软件建议；
10. 如果它认为没有可构建流程，提交证据和原因，但该结论仍需 Stage07 复核。

### 4.2 Stage06 不再因为内容 finding 重试

Stage06 不再因为 route leakage、task mode、scope、rubric、Ground Truth、evidence 或目录合同等
内容问题启动多次 recovery Agent。这些问题连同候选产物直接交给 Stage07。

Stage06 只在下列客观情况重试：

- API 或模型短暂掉线；
- Codex、Claude 或 OpenCode harness 异常退出；
- PDF/解析文件暂时无法读取；
- Agent 被中断且留下可恢复的 partial workspace；
- receipt 被网关截断；
- 文件写入或磁盘发生临时故障。

### 4.3 Stage06 输出状态

| 状态 | 含义 | 是否进入 Stage07 |
|---|---|---|
| `provisional_constructed` | Agent 已生成完整或部分候选任务 | 是 |
| `provisional_not_constructible` | Stage06 认为当前论文或工作流不可构建 | 是 |
| `artifact_delivery_failure_retryable` | Agent 有响应，但没有可传递文件或报告 | 客观恢复后进入 |
| `objective_failure_retryable` | API、Agent、解析或文件系统故障 | 重试后进入 |

运行时不再输出 `construction_invalid`。Stage06 的 `passed` 字段不再代表最终任务有效性，建议改为
`handoff_ready`，只表示 Stage07 是否获得了可读取的交接包。

### 4.4 Stage06 目录

~~~text
stage_06_task_construction/
  provisional_tasks/<paper_id>/
    paper_info.json
    workflow_review.json
    construction_receipt.json
    paper_reproduction/
    autonomous_research/
    hidden_reference/
    toolbox_requirements.json
  provisional_rejections/<paper_id>/
    paper_info.json
    workflow_review.json
    construction_receipt.json
  checkpoints/
  workspaces/
  build_results.jsonl
  stage_summary.json
~~~

候选任务即使不完整也可以交给 Stage07，只要 Stage06 留下了可理解的任务或失败报告。Stage07
负责判断缺失内容能否从论文或 SI 中恢复。

## 5. Stage07 修改方案

### 5.1 角色变化

当前 Stage07 是只读 objective auditor，并且 prompt 明确禁止读取论文、修改或重建任务。需要将其
改为单个 `Audit-Repair Agent`：

- 可以读取论文、SI、完整解析材料、Stage06 轨迹和工具箱快照；
- 可以修改 Stage07 输出目录中的任务副本；
- 可以补齐 Stage06 漏掉但原始材料真实存在的数据；
- 可以清理自主模式路线泄漏；
- 可以补全 Ground Truth、中间结论、最终结论、Acceptance Profile 和 rubric；
- 可以在必要时放弃 Stage06 工作流并重新设计任务；
- 不能修改 Stage06 原始目录和化学工具箱；
- 不能猜测、近似重建或补造来源中不存在的科学数据。

### 5.2 独立 workspace

每篇论文使用新的 Stage07 workspace：

~~~text
stage_07_task_audit/
  workspaces/<paper_id>/audit_repair/attempt-XX/
    inputs/
      stage06_candidate/       # Stage06 原始产物的只读复制
      main_paper.pdf
      supplementary/
      documents/
      evidence_index.json
      source_manifest.json
      toolbox_snapshot.json
      resource_policy.json
    outputs/
      task_pair/               # Stage07 修复或重建后的任务
      stage07_audit.json
~~~

Stage07 开始时由代码把 Stage06 候选复制到 `inputs/stage06_candidate/`。Agent 再将需要编辑的内容
复制到 `outputs/task_pair/`。不同 Agent 之间不共享会话，只通过文件夹复制传递信息。

## 6. Stage07 repair-first 决策顺序

这是本版方案相对于上一版最重要的更正。

### 6.1 Prompt 中增加的简短强制规则

Stage07 prompt 开头加入以下简短规则，不再增加复杂的多层提示：

> **REPAIR-FIRST RULE:** First audit and attempt to repair the workflow selected by Stage06. Do not
> search for or switch to another workflow while the selected workflow can be repaired from the paper,
> SI, parsed assets, or task artifacts. Only after recording an evidence-backed, scientifically
> unrepairable blocker may you select another complete workflow and redesign the task pair.

对应中文语义是：优先审计和修复 Stage06 原工作流；只要能够从论文、SI、解析资产或已有任务
中恢复，就不得切换工作流；只有写明有证据支持且科学上不可修复的阻断后，才允许寻找其他
工作流。

### 6.2 固定处理顺序

Stage07 必须按以下顺序执行：

1. 读取 Stage06 的任务、workflow review、失败理由和轨迹摘要；
2. 检查 Stage06 所选工作流的输入、路线、参数、结果和结论闭环；
3. 对所有疑似缺失内容，先到主文、全部 SI、layout、表格和坐标材料中定向搜索；
4. 如果来源中存在相关内容，修复原工作流，不得切换；
5. 修复任务指令、两种模式、Ground Truth、rubric、证据和工具箱说明；
6. 只有确认原工作流需要来源中不存在的数据、无法恢复的核心参数或不存在的 Ground Truth
   时，才将原工作流标记为不可修复；
7. 原工作流不可修复后，才建立论文的其他计算工作流清单；
8. 找到其他完整且非平凡的流程时，重新设计任务；
9. 所有合理工作流均不可构建时，最终拒绝。

伪代码为：

~~~text
if objective_failure:
    objective_failure_retryable
else:
    audit(stage06_workflow)
    search_source_for_missing_material(stage06_workflow)

    if stage06_workflow_is_repairable:
        repair(stage06_workflow)
        approved or approved_with_repairs
    else:
        record_evidence_backed_unrepairable_blocker()
        search_alternative_workflows()

        if complete_alternative_exists:
            redesign_task_pair()
            approved_after_workflow_redesign
        else:
            rejected_scientific_unrepairable
~~~

## 7. Stage07 的修复与拒绝边界

### 7.1 可直接修复的问题

- 论文或 SI 中存在，但 Stage06 没有复制的坐标、结构、表格或输入文件；
- 自主科研任务中泄漏作者的软件、方法、参数或路线；
- 任务指令、边界条件和提交要求不清楚；
- 中间关键结论或最终结论抽取不完整，但原文存在；
- Ground Truth 类型、Acceptance Profile、容差或 rubric 关联不完整；
- 两种模式的输入、科学问题、Ground Truth 或提交合同不一致；
- 论文复现模式对作者路线描述不完整；
- evidence 引用、文件名、元数据或工具箱需求记录不完整；
- Stage06 认为数据缺失，但 Stage07 在其他 SI、layout、表格或解析 fallback 中找到了数据。

修复这些问题后返回 `approved_with_repairs`。如果没有发生实际修改，则返回 `approved`。

### 7.2 允许重设计的条件

Stage07 只有在原工作流满足至少一个不可修复条件时才能切换：

- 必需输入在主文、所有 SI 和全部可用解析材料中均不存在；
- 核心结构、状态、构象、质子化、电荷或多重度无法确定；
- 核心方法、参数、模型或边界条件不可恢复；
- 原工作流没有可信、可评分的中间或最终 Ground Truth；
- 原工作流本身断裂，无法形成输入—计算—结果—结论闭环；
- 原工作流无法在资源预算内形成有意义的任务，且不能通过保留同一科学目标合理缩减；
- Stage06 选择的是无意义的 trivial 工作流，且无法在同一工作流中扩展为有效任务。

若原工作流可以通过增加同一工作流中的步骤、分支或来源资产完成，则优先扩充修复，不应立即
切换到另一个主题。只有科学问题、workflow identity、主要分支或任务 scope 发生实质变化时，
才算 workflow redesign。

### 7.3 最终拒绝条件

Stage07 在确认原工作流不可修复，并检查合理替代工作流后，只有以下情况才拒绝：

- 论文所有候选工作流都缺少必要输入；
- 所有流程都缺少关键参数或状态定义；
- 没有任何完整的计算流程；
- 没有可评分的中间或最终结论；
- 所有候选只能依赖猜测、近似重建或补造数据；
- 所有候选均明显超过资源限制且无法合理缩减；
- 论文中的计算只属于背景引用、简单处理或没有 benchmark 价值的单次调用。

API、Agent、PDF 或解析故障不能产生科学拒绝。工具箱缺软件也不能产生科学拒绝。

## 8. Stage07 最终状态

### 8.1 主状态

| `audit_decision` | 含义 |
|---|---|
| `approved` | 原工作流有效，未发生实际修改 |
| `approved_with_repairs` | 保留 Stage06 原工作流并完成修复 |
| `approved_after_workflow_redesign` | 原工作流有不可修复阻断，已改用其他完整工作流并重建任务 |
| `rejected_scientific_unrepairable` | 原工作流和所有合理替代工作流均不可构建 |
| `objective_failure_retryable` | API、Agent、PDF、解析或文件系统故障 |

`approved_after_workflow_redesign` 也适用于：

- Stage06 返回 `provisional_not_constructible`，Stage07 找到另一个完整工作流；
- Stage06 选择的 partial workflow 不可用，Stage07 改为完整 major/full workflow；
- Stage07 必须更换科学问题、主要流程或核心 Ground Truth 才能构建任务。

如果 Stage06 暂停构建，但 Stage07 从来源中恢复的是同一个工作流，则使用
`approved_with_repairs`，并记录 `repair_origin=stage06_abstention_reversed`，不视为工作流重设计。

### 8.2 工具箱和资源状态

工具箱状态与主状态正交：

~~~json
{
  "toolbox_status": "available | needs_software | unknown",
  "required_additions": [],
  "resource_status": "feasible | high_cost | infeasible | uncertain"
}
~~~

例如：

~~~json
{
  "audit_decision": "approved_after_workflow_redesign",
  "toolbox_status": "needs_software"
}
~~~

工具箱缺失不改变 `approved*` 状态。资源真正不可行时，Stage07 应先尝试保留同一科学目标并合理
缩减；只有无法缩减且没有替代工作流时才拒绝。

## 9. Stage07 receipt

Stage07 的结构化结果建议为：

~~~json
{
  "audit_decision": "approved_with_repairs",
  "source_stage06_decision": "provisional_constructed",
  "original_task_pair_id": "...",
  "final_task_pair_id": "...",
  "selected_workflow_preserved": true,
  "repairs": [
    {
      "category": "mode_isolation",
      "details": "...",
      "source_evidence_ids": [],
      "changed_files": []
    }
  ],
  "workflow_redesign": {
    "performed": false,
    "trigger": "",
    "original_scope": {},
    "original_blockers": [],
    "replacement_scope": {},
    "replacement_reason": "",
    "evidence_ids": [],
    "changed_files": []
  },
  "remaining_issues": [],
  "toolbox_status": "available",
  "required_additions": [],
  "resource_status": "feasible",
  "summary": ""
}
~~~

当 `audit_decision=approved_after_workflow_redesign` 时必须满足：

- `selected_workflow_preserved=false`；
- `workflow_redesign.performed=true`；
- 记录原工作流不可修复的具体原因；
- 记录已检查的来源和 evidence ID；
- 记录替代 workflow scope、选择理由和修改文件；
- Stage07 输出完整的新任务对和共享 hidden reference。

代码只验证 receipt 能否解析、路径是否安全以及 Agent 声明的输出目录是否存在，不判断这些科学
理由是否正确。

## 10. Stage07 输出和发布

~~~text
stage_07_task_audit/
  audited_tasks/<paper_id>/
    paper_info.json
    paper_reproduction/
    autonomous_research/
    hidden_reference/
    toolbox_requirements.json
    stage07_audit.json
  rejected_tasks/<paper_id>/
    paper_info.json
    stage06_handoff.json
    stage07_audit.json
  checkpoints/
  workspaces/
  audit_results.jsonl
  stage_summary.json
~~~

发布规则：

- `approved`、`approved_with_repairs`、`approved_after_workflow_redesign`：发布 Stage07 输出任务；
- `rejected_scientific_unrepairable`：不发布任务，只保留拒绝证据和轨迹；
- `objective_failure_retryable`：保留 checkpoint，等待 resume；
- Stage06 候选目录不删除，便于追溯 Stage07 修改前后的差异；
- 不生成 `failed_count.txt`、`finished_at.txt` 等大量零散状态文件。

## 11. 当前代码的具体修改点

### 11.1 Stage06

`src/stages/stage06_task_builder/stage.py`：

- 取消 task-pair semantic validator 对运行结果的阻断；
- 取消内容 finding 触发的多轮 recovery；
- 将 `constructed` 改为 `provisional_constructed`；
- 将 Stage06 科学拒绝改为 `provisional_not_constructible`；
- 移除运行时 `construction_invalid` 路径；
- 把候选任务或失败交接包原子写入 provisional 目录；
- 只保留客观故障和 artifact delivery recovery。

`src/stages/stage06_task_builder/prompts.py`：

- 将最终产物表述为 Stage07 待审计的候选任务；
- 保持 full-paper-first、复现模式先生成、再复制成自主模式；
- 明确无需为了机械 schema 漂移反复重建科学任务；
- 保持不得补造科学输入或 Ground Truth 的要求。

`src/stages/stage06_task_builder/validation.py`：

- 不再从运行路径调用；
- 可保留为人工/离线诊断模块，或后续单独移至 diagnostics。

### 11.2 Stage07

`src/stages/stage07_task_judge/stage.py`：

- eligible records 同时包含 Stage06 构建和暂定不可构建记录；
- 创建包含论文、SI、解析材料和 Stage06 候选的独立 workspace；
- 从只读审计改为可写输出副本；
- 不再合并代码生成的 deterministic scientific outcomes；
- 接收 Agent 修复后或重设计后的完整任务目录；
- 根据 Agent 主状态写入 audited/rejected 目录；
- 只对客观故障执行 recovery。

`src/stages/stage07_task_judge/prompts.py`：

- 删除“禁止读取论文、禁止修改、禁止决定是否保留”的旧约束；
- 加入简短 `REPAIR-FIRST RULE`；
- 定义修复、重设计和拒绝边界；
- 明确工具箱只读且缺软件不拒绝；
- 明确复现模式先完成，再复制并脱敏为自主模式；
- 要求记录修复清单或 workflow redesign 证据。

`src/stages/stage07_task_judge/validation.py`：

- 移除运行时 `validate_task_pair()` 和 deterministic outcome 合并；
- 仅保留 receipt 解析、路径安全、输出目录存在等技术检查；
- 原科学检查可以保留为离线诊断，不影响 Agent 决策。

### 11.3 公共模块

`src/agents/schemas.py`：

- 增加新的 Stage07 receipt schema；
- 增加 `approved_after_workflow_redesign`；
- 将 workflow redesign、repair、toolbox 和 resource 字段结构化。

`src/late_stage_runner.py`：

- 不再只把 `decision=constructed` 的论文传给 Stage07；
- 传递 `provisional_constructed` 和 `provisional_not_constructible`；
- Stage07 使用完整历史文档和 Stage06 交接包；
- summary 分别统计 repaired、redesigned、rejected 和 objective failure。

`src/config.py`、`config.example.json`：

- Stage07 增加 audit-repair 工具调用预算；
- 模型和 harness 继续完全配置化；
- Codex、OpenCode 和 Claude 均使用同一职责合同；
- recovery 只面向客观中断或产物交付，不面向科学 finding。

## 12. 测试计划

### 12.1 Stage06

- Agent 生成有路线泄漏或 rubric 不完整的任务，Stage06 仍输出
  `provisional_constructed`；
- Stage06 认为当前工作流不可构建时仍生成可供 Stage07 复核的 handoff；
- API、harness 和解析失败仍为 `objective_failure_retryable`；
- Stage06 不再因为内容 finding 连续调用 recovery Agent。

### 12.2 Stage07 修复优先级

- Stage06 漏复制 SI 坐标，但来源中存在：Stage07 修复原工作流，返回
  `approved_with_repairs`；
- 自主模式泄漏 Gaussian/PBE0 路线：Stage07 清理同一工作流，不得切换；
- Ground Truth 不完整但论文存在结论：Stage07 补齐并保留原工作流；
- 同一工作流可通过补充数据完成，同时论文还有其他工作流：Stage07 必须选择修复原工作流。

### 12.3 Workflow redesign

- 原工作流缺少来源中不存在的核心输入，论文另有完整流程：返回
  `approved_after_workflow_redesign`；
- 原工作流不可修复，但 Agent 未记录证据就切换：Stage07 Agent 应在自己的审计流程中继续修正
  receipt，不得把无依据切换写成成功；
- Stage06 暂定不可构建，Stage07 找到同一工作流遗漏数据：`approved_with_repairs`；
- Stage06 暂定不可构建，Stage07 找到不同工作流：`approved_after_workflow_redesign`；
- 所有工作流均不可构建：`rejected_scientific_unrepairable`。

### 12.4 其他边界

- 缺软件只产生 `needs_software`，不改变 approved 状态；
- 数据为 Agent 近似重建且无来源支持时不得修复为通过；
- API 或 PDF 故障不得归为科学拒绝；
- Stage07 只修改自己的输出副本；
- 两种模式的输入和结论保持一致，自主模式不包含论文路线；
- Stage07 发布目录不包含论文 PDF 和私有 hidden answer 的公开副本。

## 13. 实施顺序

1. 修改状态合同和 Agent schema；
2. 简化 Stage06 运行时判断，建立 provisional handoff；
3. 重写 Stage07 workspace 和 repair-first prompt；
4. 实现 Stage07 修复/重设计后的目录接收与状态汇总；
5. 修改 late-stage runner 和 resume；
6. 更新单元测试；
7. 使用现有 gallaphosphene 轨迹做离线交接测试；
8. 使用当前 API 重新运行 gallaphosphene；
9. 检查 Stage07 是否优先修复原工作流；
10. 单篇符合预期后重新提交固定六篇；
11. 逐篇检查 repaired、redesigned、rejected 和 objective failure 是否符合论文证据；
12. 更新实现日志、分析报告并按版本提交 Git。

## 14. 验收标准

- 代码不再以科学内容 finding 阻断 Stage06 或替代 Stage07 判断；
- Stage06 的候选和暂定拒绝都能进入 Stage07；
- Stage07 能读取论文和 SI，并在独立 workspace 修改任务副本；
- Stage07 在原工作流可修复时不会搜索或切换到其他工作流；
- 原工作流不可修复但存在替代流程时，能完整重建并返回
  `approved_after_workflow_redesign`；
- 没有可用工作流时能给出证据充分的最终拒绝；
- 小问题被实际修复，而不是只输出问题列表；
- 缺软件不会导致科学拒绝；
- 客观故障保持可恢复；
- 最终公开任务来自 Stage07 输出，Stage06 原始产物保持可追溯；
- 运行目录保持简洁，不重新引入大量零散日志文件。

## 15. 当前状态

本文档只是待确认的代码修改方案。创建本文档时尚未按本方案修改 Stage06、Stage07、runner、
schema、配置或测试。用户确认后再制定实施计划并开始修改代码。

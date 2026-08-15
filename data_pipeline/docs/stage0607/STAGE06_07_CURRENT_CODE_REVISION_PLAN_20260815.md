# Stage06/Stage07 单 Agent 简化修改方案

> 日期：2026-08-15
> 版本：single-agent-full-workflow-first-v2
> 状态：已按本方案完成首轮实现与回归；真实 API 回归记录见 `STAGE06_07_IMPLEMENTATION_LOG_20260815.md`。
> 适用代码：src/stages/stage06_task_builder/、src/stages/stage07_task_judge/、src/agents/

## 1. 最终设计结论

Stage06 默认只使用一个 Agent 调用完成一篇论文的全部任务构建。

这个 Agent 在同一个受控 workflow 中依次完成：

1. 阅读论文 PDF、全部 SI 和解析材料；
2. 抽取论文作者实际执行的全部计算化学工作；
3. 优先判断整篇论文的计算化学流程能否完整复现；
4. 如果整篇流程缺少必要数据，再选择范围最大的完整计算子流程；
5. 先生成论文复现模式任务；
6. 调用代码提供的复制脚本，把论文复现任务完整复制为自主科研任务；
7. 在副本上删除论文路线、软件、方法和参数披露，改写为自主科研模式；
8. 生成两个模式共同使用的私有 Ground Truth、Acceptance Profile 和结论 rubric；
9. 写出工具箱缺口、资源风险、scope、复杂度和证据记录。

如果在步骤 3 或步骤 4 发现必要数据缺失、流程不完整、没有可评分结论或无法复现，Agent 立即停止，不再创建两个任务目录，只写科学失败记录。

默认流程为：

~~~text
论文 PDF / SI / 解析正文 / 表格 / 坐标
                    |
                    v
          单个 Stage06 Builder Agent
                    |
       +------------+-------------+
       |                          |
       | 不可构建                  | 可构建
       v                          v
scientific_not_constructible   生成 paper_reproduction/
                                  |
                                  v
                    调用确定性复制/校验脚本
                                  |
                                  v
                        生成 autonomous_research/
                                  |
                                  v
                   生成共同 hidden_reference/
                                  |
                                  v
                         代码执行最终校验
                                  |
                                  v
                              Stage07
~~~

不再默认使用“主构建器 + Autonomous Converter”两个 Agent。独立 converter 只作为可配置备用模式，用于单 Agent 多次发生自主模式路线泄漏、或未来需要更强上下文隔离时启用。

## 2. 为什么一个 Agent 可以完成

两个 Agent 的拆分不是科学上的必要条件。其唯一明显优势是第二个 Agent 从未看过论文路线和答案，因此自主模式的上下文隔离更强。

但对当前任务而言，一个 Agent 有四个更直接的优势：

- 论文只需要完整阅读一次；
- 流程选择、输入、路线、Ground Truth 和两个任务模式共享同一科学理解；
- 不需要把大量 workflow context 再传给第二个 Agent；
- 复现任务与自主任务可以在同一工作流中保持一致，明显减少 token、延迟和调用失败点。

因此，本方案默认采用一个 Agent。隔离主要由代码负责：

- reproduction、autonomous、hidden reference 使用不同目录；
- Agent 必须先生成 reproduction，再调用固定复制脚本；
- 复制脚本冻结输入、科学目标和 submission contract；
- autonomous 只能修改 allowlist 字段；
- 代码扫描自主任务中的路线 token 和隐藏答案；
- Stage07 再进行独立审计。

需要明确接受的取舍是：单 Agent 已经看过论文路线和答案，所以只能做到输出目录级和代码级硬隔离，不能做到模型上下文级隔离。这个风险通过确定性泄漏校验和 Stage07 控制。

## 3. 已确认且保持不变的要求

- Stage06 Agent 在独立工作空间中运行。
- Stage07 Agent 使用另一个独立工作空间和新会话。
- Agent 只在自己的 workspace 写文件。
- 论文、SI、上游结果和工具箱快照只读。
- Stage02/03/05 只作为提示和历史记录，不是不可推翻的科学事实。
- 论文 PDF、SI 和由其生成的解析材料是主要科学来源。
- 工具箱缺少软件不能导致 Stage06 直接淘汰任务。
- 工具箱只读；Agent 只能提出缺失软件和能力建议。
- 两个模式共享相同输入、科学目标、submission contract、Ground Truth 和结论评分。
- 两个模式可以使用不同的过程 rubric。
- 论文信息文件与两个评估任务目录同级保存。
- API、harness、解析或磁盘故障不能伪装为论文科学失败。
- Stage07 只做客观审计，不自动修复，不决定发布。
- Codex、Claude、OpenCode 继续由配置选择，业务代码不绑定特定 harness。

## 4. 任务选择总原则

选择算法采用“完整性硬门槛，范围优先，复杂度次优先，科学价值和资源可行性共同约束”。

优先级按以下顺序执行：

1. 首先寻找整篇论文完整的计算化学工作流；
2. 整篇流程完整且资源可接受时，必须优先选择整篇流程；
3. 整篇流程有 essential data/process 缺失时，寻找论文中最大的完整主工作流；
4. 主工作流仍不完整时，寻找最大的完整计算子流程；
5. 多个同范围候选都完整时，优先选择更复杂、核心计算更多、工具调用更多、科学推理更丰富的候选；
6. 只有一次简单计算调用并直接读出答案的任务不进入 benchmark；
7. 如果论文只存在低复杂度的一步任务，即使它技术上完整，也标记为不适合当前 benchmark。

这是一种分层选择，不是单纯追求最高复杂度。完整性和可复现性永远是硬门槛，不能为了增加难度使用缺数据的流程。

## 5. 工作流范围标记

每个成功任务必须明确标记 workflow_scope。

### 5.1 full_paper_computational_workflow

表示任务覆盖论文中支持主要科学结论的完整计算化学工作，包括主要输入、核心计算分支、必要验证、中间结论和最终结论。

它不要求纳入与主要科学问题无关的调试计算、重复收敛测试或纯绘图，但不能主动删除论文核心计算分支。

### 5.2 major_paper_workflow

表示整篇论文包含多个相对独立的计算工作流，任务完整覆盖其中一个主要工作流。该工作流必须支持论文的一个重要 claim，而不是边缘补充计算。

### 5.3 partial_computational_subworkflow

表示更大的论文流程存在缺失或不可执行部分，但任务选择了其中一个输入、过程、输出和 Ground Truth 全部闭合的子流程。

partial 不代表可以降低完整性要求，只表示覆盖范围小于论文主要计算任务。

### 5.4 scope 元数据

workflow_review.json 和 paper_info.json 都必须记录：

~~~json
{
  "workflow_scope": {
    "kind": "full_paper_computational_workflow",
    "included_workflow_ids": [],
    "excluded_workflow_ids": [],
    "included_claim_ids": [],
    "excluded_claim_ids": [],
    "selection_rationale": "...",
    "larger_scope_failure_reasons": [],
    "scope_evidence_ids": []
  }
}
~~~

如果选择 major 或 partial，larger_scope_failure_reasons 必须说明为什么不能采用整篇或更大范围，并引用证据或明确的缺失记录。

这个 scope 标记同时写入：

- 同级 paper_info.json；
- 两个模式的 task_info.json；
- 两个模式的 task_spec.json；
- Stage07 audit packet。

公开 scope 只说明任务覆盖范围，不泄漏目标答案。

## 6. 复杂度与挑战性要求

### 6.1 什么是有效复杂度

只计算能产生新科学产物或需要科学判断的操作，例如：

- 多个结构、构象、电子态或反应路径的优化；
- 频率、热化学、激发态、单点能或高层级校正；
- 分子动力学采样、自由能、NEB、QM/MM 或微观动力学；
- 多个条件、催化剂、吸附位点或候选结构的比较；
- 前一步结果决定后一步输入或路线；
- 收敛、稳定性、状态身份或方法一致性验证；
- 需要组合多个计算结果形成中间和最终结论。

以下不计为核心复杂度：

- 文件复制和格式转换；
- 读取已经存在的答案；
- 绘图；
- 简单算术；
- 写报告；
- 单纯调用一次计算然后直接返回一个值；
- 为满足步数而人为拆分同一个命令。

### 6.2 最低挑战性门槛

默认拒绝 low_complexity_trivial 候选。以下任务属于低复杂度：

- 一次 single-point、optimization、frequency 或 property 调用即可直接得到全部评分答案；
- 没有多体系、多状态、多条件、多步骤或验证要求；
- 不需要根据中间产物作任何科学分析；
- 过程分只能评价“是否调用了工具”和“是否读出了数值”。

可接受候选至少满足以下条件之一，并且具有一个有意义的分析/验证阶段：

- 两个或更多不同的核心计算阶段；
- 多个结构/状态/条件需要独立计算并比较；
- 存在真实的 artifact dependency；
- 存在迭代决策、验证或失败恢复；
- 需要两个或更多工具/软件能力协同完成；
- 需要整合多个计算产物才能形成结论。

这里不使用机械的固定 tool-call 数作为唯一门槛，因为一个 toolbox Action 可能封装多个底层作业。代码和 Agent同时记录预计的最小工具调用数和实际科学操作数。

### 6.3 complexity_profile

每个候选必须输出：

~~~json
{
  "complexity_profile": {
    "level": "high",
    "scientific_core_operation_count": 8,
    "estimated_min_tool_calls": 12,
    "estimated_typical_tool_calls": 20,
    "dependency_edge_count": 5,
    "parallel_branch_count": 3,
    "system_or_state_count": 6,
    "software_capability_count": 3,
    "iterative_decisions": [],
    "validation_operations": [],
    "reasoning_requirements": [],
    "non_core_operations_excluded": []
  }
}
~~~

complexity level 允许：

- high；
- medium；
- low_complexity_trivial。

正式构建只接受 high 或 medium。low_complexity_trivial 即使数据完整，也返回 benchmark_not_challenging。

estimated_min_tool_calls 只是基于当前工具箱接口粒度的估计，不能通过人为拆分调用提高复杂度。

## 7. 完整性与可复现性要求

### 7.1 必须完整的核心内容

- 作者确实执行了计算化学工作；
- 任务科学问题和目标明确；
- 关键输入结构、组成、状态和边界条件存在；
- 会影响科学结论的核心方法、模型和参数充分；
- 工作流步骤、分支、依赖和中间产物清楚；
- 至少有多个可评分过程点或结论点；
- 中间关键结论和最终结论有论文证据；
- 资源规模可接受，或能够在不改变目标的情况下合理约束。

### 7.2 可以使用默认值的内容

以下目标无关执行控制可以使用 benchmark_fixed 或 software_default：

- SCF 数值阈值；
- 积分网格；
- 并行数、内存和任务调度参数；
- 最大迭代数；
- 目标无关的收敛加严策略；
- 文件格式和单位的确定性转换。

每个默认值必须记录来源和理由，不能伪装成 paper_reported。

### 7.3 不得推测的核心内容

无法唯一确认以下内容时，对应范围不可构建：

- 分子、表面、晶体或反应结构；
- 构象、吸附位点、质子化、charge、multiplicity 或电子态；
- 核心泛函、基组、赝势、色散、力场或溶剂模型；
- 反应、参考物种、化学计量、目标状态或路径身份；
- 必要原始数据；
- 用于评分的中间或最终 Ground Truth。

如果整篇流程缺这些内容，Agent 必须继续检查能否选择一个更小但完整且非平凡的子流程。只有没有任何完整且达到复杂度门槛的候选时，才论文级失败。

### 7.4 工具箱和资源

工具箱缺软件、版本、许可证或 Action 时：

- 不淘汰科学任务；
- 继续生成两个模式；
- 写入 toolbox_requirements.json；
- Stage07 输出 needs_software 或 toolbox_capability_unknown。

只有任务成本明显超过资源政策，并且无法在保持科学目标的前提下约束范围时，才返回 resource_infeasible。

## 8. 单 Agent Stage06 workflow

### 8.1 Agent 角色

角色名建议：stage06_task_pair_builder。

同一个 Agent、同一次 harness 会话完成整个任务。Agent 不负责正式目录提交，只在 staging workspace 中工作。

### 8.2 输入目录

~~~text
inputs/
  source_manifest.json
  coverage_manifest.json
  main_paper.pdf
  supplementary/*.pdf
  normalized/*.md
  layout/*.txt
  tables/*
  coordinates/*
  stage02_hint.json
  stage03_hint.json
  stage05_hint.json
  toolbox_snapshot.json
  resource_policy.json
  task_contract.json
  scripts/
    validate_workflow_review.py
    validate_reproduction.py
    copy_reproduction_to_autonomous.py
    validate_task_pair_draft.py
~~~

输入优先级：

1. 原始 PDF、SI 和作者提供的数据；
2. normalized full text、layout、table、coordinate fallback；
3. Stage02/03/05 hints；
4. 工具箱和资源政策。

Stage02/03/05 的历史结论可以被主 Agent 推翻，但必须记录 disposition 和证据。

### 8.3 Agent 内部执行顺序

主 prompt 要求严格按以下顺序：

1. 建立论文计算工作流 inventory；
2. 尝试选择 full-paper workflow；
3. 若不完整，记录 larger-scope blocker 并依次选择 major/partial workflow；
4. 检查选定范围是否达到 medium/high complexity；
5. 原子写 workflow_review.json；
6. 如果不可构建，写 construction_receipt.json 后立即结束；
7. 如果可构建，生成 paper_reproduction/；
8. 运行 validate_reproduction.py；
9. 运行 copy_reproduction_to_autonomous.py；
10. 只修改 autonomous_research/ 的 allowlist 文件；
11. 生成 hidden_reference/；
12. 运行 validate_task_pair_draft.py；
13. 写 construction_receipt.json，并返回固定路径 receipt。

Agent 不需要反复把大段论文内容写进 JSON。所有事实使用 evidence ID 和源文件路径引用。

### 8.4 成功输出目录

~~~text
outputs/
  workflow_review.json
  paper_reproduction/
    task.md
    task_info.json
    task_spec.json
    submission_contract.json
    process_rubric.json
    data/inputs/*
    paper_route.md
    workflow_spec.json
    route_evidence_map.json
  autonomous_research/
    task.md
    task_info.json
    task_spec.json
    submission_contract.json
    process_rubric.json
    data/inputs/*
  hidden_reference/
    ground_truth_common.json
    acceptance_profiles.json
    conclusion_rubric.json
    private_evidence_map.json
  toolbox_requirements.json
  construction_receipt.json
~~~

paper_info.json、evidence_index.json、source_manifest.json 和 construction_record.json 由代码在正式 task-pair 根目录生成，不交给 Agent 自由编写。

### 8.5 scientific failure 输出

scientific failure 不生成任何正式 task 目录，只写：

~~~json
{
  "decision": "scientific_not_constructible",
  "paper_workflow_inventory_complete": true,
  "full_paper_workflow_checked": true,
  "alternative_scope_search_complete": true,
  "failure_code": "no_complete_nontrivial_workflow",
  "failure_reasons": [
    {
      "scope_attempted": "full_paper_computational_workflow",
      "code": "missing_core_input",
      "details": "...",
      "evidence_ids": [],
      "checked_sources": []
    }
  ]
}
~~~

允许的 scientific failure code 至少包括：

- no_author_performed_computation；
- missing_core_input；
- incomplete_computational_process；
- missing_ground_truth；
- source_evidence_insufficient；
- resource_infeasible；
- no_complete_nontrivial_workflow；
- benchmark_not_challenging。

API、harness、文件损坏、解析文件不可访问和磁盘错误不得使用这些 code。

## 9. 两种任务模式的生成规则

### 9.1 先生成论文复现模式

paper_reproduction 需要公开：

- 选定范围和 scope label；
- 科学问题和全部公共输入；
- 论文采用的软件、方法、参数和步骤；
- 工作流依赖、分支和关键中间产物；
- 必要验证和提交物；
- 资源、单位和格式约束。

不能公开：

- 目标数值；
- 中间结论的标准答案；
- 最终结论；
- 结果排序、趋势和机理答案；
- scoring tolerance；
- private evidence 内容。

### 9.2 代码复制

Agent 必须调用固定脚本 copy_reproduction_to_autonomous.py。脚本执行：

1. 验证 reproduction 必填文件；
2. 计算 reproduction_base_hash；
3. 完整复制目录；
4. 冻结 data/inputs/、submission_contract.json、科学问题和 deliverables；
5. 删除 reproduction-only route 文件；
6. 写 conversion_contract.json 和 derived_from.json；
7. 只开放 allowlist 文件给 Agent 修改。

Agent 不能自行用任意复制命令绕过该脚本。

### 9.3 再生成自主科研模式

autonomous_research 需要：

- 保持同一 scope、科学问题、输入和提交物；
- 删除作者软件、方法层级、参数、路线顺序和候选路径；
- 要求被评估 Agent 自行选择工具、方法和研究路线；
- 保留问题边界、物理条件、原始观测和必要实验输入；
- 使用 autonomous 专用过程 rubric；
- 不增加任何论文未提供的科学事实。

### 9.4 两模式允许差异

允许差异：

- task.md；
- task_info.json 的 mode、task instruction 和 disclosure 字段；
- task_spec.json 的 mode、task instruction 和 disclosure 字段；
- process_rubric.json；
- reproduction-only 的 paper_route.md、workflow_spec.json、route_evidence_map.json；
- public_manifest.json 和 derived_from.json。

必须一致：

- data/inputs/；
- submission_contract.json；
- workflow_scope；
- scientific question identity；
- target quantities；
- required deliverables；
- Ground Truth IDs；
- conclusion rubric；
- Acceptance Profiles。

## 10. Ground Truth 和评分

### 10.1 Ground Truth 类型

共同 Hidden Reference 支持：

- 数值和单位；
- 结构和几何；
- 类别、排序和趋势；
- 中间关键结论；
- 最终计算结论；
- 与计算目标直接相关的论文或实验结论。

### 10.2 过程分

论文复现过程 rubric 评价：

- 是否按论文路线执行多个核心计算阶段；
- 是否正确传递中间产物；
- 是否完成必要的分支、对照和验证；
- 是否处理收敛和失败恢复；
- 是否形成可追溯证据链。

自主科研过程 rubric 评价：

- 是否设计合理的多步骤研究路线；
- 是否选择适当工具和方法；
- 是否根据中间结果调整路线；
- 是否进行必要对照、验证和误差分析；
- 是否在资源约束下完成复杂任务。

不能把文件转换、绘图、读数或简单算术作为高分过程项。

### 10.3 结论分

两个模式使用完全相同的：

- Ground Truth items；
- Acceptance Profiles；
- conclusion rubric；
- 权重、单位、容差和 required propositions。

每个中间/最终结论都必须绑定实际提交 artifact，不能只让评估模型自由阅读报告后主观打分。

## 11. 单 Agent 的信息隔离

### 11.1 可以实现的隔离

代码保证：

- reproduction、autonomous 和 hidden reference 在不同目录；
- public 目录不含 hidden 文件；
- autonomous 目录不含 route 文件；
- 两模式 public inputs 内容 hash 一致；
- hidden target 数值和 proposition 不出现在 public 文本；
- autonomous 不出现论文路线 token、软件和方法披露；
- 正式结果只有全部校验通过后才原子提交。

### 11.2 无法实现的隔离

由于同一个 Agent 已读过全文并生成两种模式，模型上下文本身无法遗忘论文路线和答案。

本方案接受这一点，以减少调用和重复阅读。安全性依赖：

- 强结构化输出；
- 固定复制脚本；
- allowlist；
- 数值和文本泄漏扫描；
- mode-pair hash；
- Stage07 独立审计。

### 11.3 可配置的备用 converter

保留配置：

~~~yaml
stage06:
  mode_generation_strategy: single_agent
~~~

允许值：

- single_agent：默认，一个 Agent 生成全部内容；
- isolated_converter：主 Agent 只生成 reproduction 和 hidden，代码复制后使用第二个隔离 Agent 生成 autonomous。

只有以下情况建议切换 isolated_converter：

- 单 Agent autonomous 路线泄漏率持续超标；
- 模型无法稳定遵守 allowlist；
- 需要做严格的模式隔离实验；
- 单 Agent context 太长导致后半段任务质量明显下降。

业务 schema 和最终目录在两种策略下保持一致。

## 12. Stage06 状态与 resume

### 12.1 论文级状态

- constructed；
- scientific_not_constructible；
- objective_failure_retryable；
- construction_invalid。

非互斥标记：

- workflow_scope_kind；
- complexity_level；
- toolbox_gap_present；
- resource_risk_present；
- benchmark_defaults_used；
- stage05_candidate_replaced。

### 12.2 单 Agent 内部 checkpoint

默认只有一个 Stage06 Agent phase，但通过文件 milestone 支持恢复：

- workflow_review_validated；
- reproduction_validated；
- autonomous_copy_created；
- autonomous_validated；
- hidden_reference_validated；
- pair_draft_validated。

这些 milestone 是 checkpoint JSON 中的字段，不创建大量 finished_at.txt、failed_count.txt 等散落文件。

客观失败重试时，新 attempt 可以读取受控 recovery artifact，从最后一个通过的 milestone 继续；科学失败不自动重试，除非输入、prompt、schema 或规则版本改变。

### 12.3 fingerprint

至少包含：

- 原始 PDF/SI 和解析材料 hash；
- Stage02/03/05 hints hash；
- toolbox 内容 hash；
- resource policy hash；
- prompt/schema/helper-script version；
- harness、模型和权限 profile。

## 13. Stage07 审计

Stage07 使用独立 Agent 和只读 workspace，审计：

1. workflow_scope 是否如实，full/major/partial 标记是否有证据；
2. 是否优先选择了最大完整范围；
3. complexity 是否达到 medium/high，是否存在人为拆分步骤；
4. reproduction 是否完整披露论文路线且未泄漏答案；
5. autonomous 是否移除路线并保持相同科学目标；
6. 两模式输入、submission contract、Ground Truth 和结论评分是否一致；
7. 中间结论和最终结论是否完整、可评分且有证据；
8. 工具箱是否缺软件或功能；
9. 成本是否明显不可实现；
10. provenance 和 mode isolation 是否完整。

Stage07 默认读取紧凑 audit packet，必要时定向读取 source evidence bundle，不从头重新构建任务。

允许的 outcome：

- passed_audit；
- needs_software；
- task_missing_data；
- task_missing_ground_truth；
- workflow_incomplete；
- task_cost_too_high；
- acceptance_rule_invalid；
- mode_isolation_violation；
- mode_pair_inconsistent；
- provenance_incomplete；
- toolbox_capability_unknown；
- audit_failed_retryable。

新增两个客观 finding code，但可映射到现有 outcome：

- scope_underselected -> workflow_incomplete；
- task_not_challenging -> workflow_incomplete。

Stage07 不修改 Stage06 任务，也不因 needs_software 删除任务。

## 14. 必须修复的当前代码问题

### P0.1 evidence ID

修复 validation.py::_evidence_map_ids：递归读取 evidence_id 和 evidence_ids，以 snapshot 实际集合校验，不依赖 ID 前缀。

### P0.2 boundary

重写 _route_boundary_coverage_findings，按结构化 key/value/unit/applicability 比较，不序列化整个 JSON 后做 alias 子串判断。周期体系不能机械要求 molecular multiplicity。

### P0.3 坐标标签

修复 _layout_coordinate_blocks 的跨页标签状态，防止页码、S40、图号或页眉覆盖真实结构标签。输出页范围、atom count、formula 和 confidence。

### P0.4 表格 coverage

支持 HTML、Markdown、parser structured 和 layout fallback，并记录 complete、partial、failed 或 image_only。解析器未提取不能直接等于论文缺失。

### P0.5 Ground Truth 一致性

检查数值差、排序、趋势和文字 proposition 的一致性；出现符号冲突时必须回查 source evidence。

### P0.6 物化逻辑

不再由 _materialize_reproduction 从另一个模式重新拼装字段。Agent staging 输出通过校验后直接复制/原子提交，规范化代码只能修改固定 metadata，不能丢弃 task_spec 合法内容。

### P0.7 scientific failure

失败结果也必须验证：

- paper workflow inventory 是否完成；
- full-paper workflow 是否检查；
- alternative scope search 是否完成；
- evidence/source refs 是否存在；
- 为什么不能选择更大范围；
- 是否仅剩 trivial workflow；
- 工具箱缺失是否被错误当作 scientific failure。

## 15. 文件级修改计划

### 15.1 src/agents/schemas.py

- 定义单 Agent task-pair builder schema；
- 支持 success 和 scientific failure 的 discriminator；
- 增加 workflow_scope 和 complexity_profile；
- 增加 full/major/partial 范围枚举；
- 增加 benchmark_not_challenging 和 no_complete_nontrivial_workflow；
- 保留 typed Ground Truth、Acceptance Profile 和 Stage07 outcome；
- 为 optional isolated_converter 保留兼容 receipt schema。

### 15.2 src/stages/stage06_task_builder/prompts.py

- 合并现有 review、autonomous、reproduction、hidden 四套主 prompt；
- 新建单 Agent 顺序式 workflow prompt；
- 明确 full-paper-first 的选择规则；
- 明确复杂度门槛和非核心假步骤；
- 明确 scientific failure 的早停规则；
- 明确 reproduction-first、固定脚本复制、autonomous redaction；
- 保留 optional converter prompt，但默认不调用；
- Stage02/03/05 只称为 hints。

### 15.3 src/stages/stage06_task_builder/stage.py

- 将默认四 phase 改为一个 task_pair_builder phase；
- snapshot 加入 PDF/SI、coverage、完整解析材料和 helper scripts；
- 提供 validate/copy helper；
- 接收 Agent 同时生成的 reproduction、autonomous 和 hidden artifacts；
- 成功后执行独立 deterministic validation 和 atomic commit；
- scientific failure 时不运行后续 phase；
- optional isolated_converter 使用配置分支；
- 写 scope、complexity、toolbox gap 和 milestone；
- 保留 checkpoint/recovery，但不创建散落日志文件。

### 15.4 src/stages/stage06_task_builder/validation.py

- 删除“至少两步/必须一条 dependency edge/最多三个 GT”等旧机械规则；
- 新增 nontrivial complexity validator；
- 新增 scope selection 和 larger-scope failure validator；
- 检查 estimated tool calls 不是人为拆分；
- 检查两个模式输入、目标、submission contract 和 Ground Truth 一致；
- 检查 autonomous route leakage；
- 实现 P0.1、P0.2、P0.5、P0.7。

### 15.5 PDF、表格和坐标辅助代码

首版继续在 stage.py 中小范围修复，避免引入新的大模块：

- 修复跨页坐标标签；
- 增加 coordinate confidence；
- 扩展 table fallback；
- 生成 coverage manifest；
- 将解析失败与论文科学缺失区分。

稳定后再考虑抽出 source_materials.py。

### 15.6 src/stages/stage07_task_judge/

- audit packet 增加 workflow_scope、complexity_profile 和 larger-scope reason；
- 审计范围是否被不必要缩小；
- 审计 trivial single-call task；
- 继续检查工具箱、成本、GT、隔离和 provenance；
- finding-to-outcome 使用显式 code map；
- source evidence hash 纳入 fingerprint。

### 15.7 src/late_stage_runner.py 与配置

新增：

~~~yaml
stage06:
  mode_generation_strategy: single_agent
  preferred_scope: full_paper_computational_workflow
  minimum_complexity: medium
  reject_trivial_single_call: true
  task_pair_builder_max_tool_calls: 48
  task_pair_builder_timeout_seconds: 7200
~~~

具体 tool-call budget 经试跑标定，不写死在业务逻辑。

harness 继续支持 codex、claude、opencode；默认同一个 builder Agent key 完成所有 Stage06 工作。

## 16. 测试计划

### 16.1 P0 回归

1. 单数 evidence_id 正确识别；
2. boundary 结构化比较无字符串误命中；
3. 周期体系不被 multiplicity 误杀；
4. 跨页坐标标签不被 S40/页码覆盖；
5. HTML/Markdown/parser/layout 表格 coverage；
6. 数值与文字 GT 冲突被捕获；
7. Agent task_spec 不被 materializer 丢失；
8. scientific failure 缺 inventory/coverage/evidence 时无效。

### 16.2 范围选择测试

1. full-paper 完整时不得降级选择 partial；
2. full-paper 缺 essential input 时可以选择完整 major；
3. major 不完整时可以选择完整 partial；
4. partial 必须记录 larger-scope failure；
5. 只有 trivial subworkflow 时返回 benchmark_not_challenging；
6. 多个完整候选时选择复杂度更高且论文更核心的候选；
7. 工具箱缺失不改变 scope selection。

### 16.3 复杂度测试

1. 一次 single-point 直接得答案被拒绝；
2. 多结构独立优化和比较可达到 medium；
3. 优化 -> 频率 -> 高层单点 -> 热化学分析可达到 high；
4. 文件转换、绘图和读数不能增加 scientific_core_operation_count；
5. 一个高级 Action 封装多个作业时，不按单一 API call 错判 trivial；
6. estimated tool calls 与 workflow steps、systems 和 toolbox actions 能互相解释。

### 16.4 单 Agent task-pair 测试

1. Agent 必须先写有效 workflow_review；
2. reproduction 校验失败时复制脚本拒绝执行；
3. autonomous 必须来源于 reproduction base hash；
4. Agent 只能修改 allowlist 文件；
5. 两模式 data/inputs 和 submission contract hash 相同；
6. autonomous 不含 route token；
7. public task 不含 hidden result；
8. private reference 同时适用于两模式；
9. 中途 objective failure 可以从 milestone 恢复。

### 16.5 Stage07 测试

1. full/major/partial scope 审计；
2. scope_underselected 被识别；
3. task_not_challenging 被识别；
4. toolbox missing 与 capability unknown 分开；
5. 合法 benchmark default 不被当作 missing data；
6. 多 outcome 同时保留；
7. audit failure 正确标为 retryable。

### 16.6 真实论文回归

顺序：

1. 一篇人工确认的整篇计算流程完整正样本；
2. 一篇整篇不完整但存在复杂完整子流程的样本；
3. 一篇只有简单单次计算的低复杂度样本；
4. 一篇工具箱缺软件但科学流程完整的样本；
5. 之前六篇历史样本。

重点检查：

- 是否真的优先选择整篇计算任务；
- 是否在必要时选择最大的完整子流程；
- scope 标记是否准确；
- 任务复杂度是否足以评估多工具调用和科研规划；
- 失败是否来自真实科学缺失而不是 validator/parser bug；
- reproduction/autonomous 是否只有信息披露差异。

## 17. 实施顺序

### P0：修确定性 bug

先修 evidence、boundary、coordinate、table coverage、GT consistency、materializer 和 failure validator，并补单元测试。

### P1：单 Agent schema 与 prompt

定义 full-paper-first、scope、complexity、success/failure 合同，合并四个旧 phase prompt。

### P2：单 Agent orchestration

实现 staging helper scripts、单 phase Agent 调用、内部 milestone、复制和原子提交。

### P3：任务对验证

实现 scope、nontrivial complexity、copy integrity、route leakage 和 shared GT 校验。

### P4：Stage07

加入 scope/complexity 审计、显式 outcome mapping 和 source fallback。

### P5：真实样本迭代

按正样本、复杂子流程、trivial、toolbox gap、六篇历史样本的顺序运行。只调整通用规则，不为单篇论文写特殊逻辑。

## 18. 验收标准

实现完成必须满足：

- 每篇论文默认只调用一个 Stage06 Agent；
- Agent 只完整阅读论文一次；
- 优先选择整篇论文完整计算流程；
- 整篇不可构建时选择范围最大的完整复杂子流程；
- 每个成功任务标记 full_paper、major 或 partial；
- major/partial 记录未选更大范围的原因；
- trivial single-call 任务不进入 benchmark；
- medium/high 任务具有多个真实计算、分支、状态、依赖或验证；
- 论文复现任务先生成；
- 自主任务由固定脚本复制后改写；
- 两模式输入、目标、submission contract、GT 和结论 rubric 一致；
- 两模式只有路线披露和过程 rubric 不同；
- 工具箱缺失不造成 scientific reject；
- public/hidden 和 autonomous/route 泄漏检查通过；
- Stage07 能审计 scope、复杂度、完整性、软件、成本和评分；
- API 波动可以 resume；
- Codex、Claude、OpenCode 使用同一合同；
- 不生成大量散落日志文件；
- 六篇历史样本和独立正负样本得到可解释结果。

确认本版后，代码修改按 P0 -> P1 -> P2 -> P3 -> P4 -> P5 执行。在单元测试和 mock 单 Agent workflow 通过前，不提交真实长时间任务。

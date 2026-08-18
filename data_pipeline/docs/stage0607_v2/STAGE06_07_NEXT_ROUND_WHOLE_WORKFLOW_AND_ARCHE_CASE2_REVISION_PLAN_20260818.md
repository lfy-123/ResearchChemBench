# Stage06/07 下一轮修改方案：整篇路线优先、核心子过程降级与 ARCHE Case2 式自主任务

日期：2026-08-18  
状态：方案草案，待确认；本轮只记录方案，不修改代码。

## 1. 目标与本轮边界

本轮目标是让 Stage06/07 稳定地产生“围绕明确科学目标的计算化学评估任务”，并让两个模式的差异只来自公开给被评估 Agent 的信息：

- 论文复现模式：公开论文给出的计算路线、方法、参数和必要输入，评估 Agent 是否能忠实执行并解释论文路线。
- 自主科研模式：公开科学问题、实验事实、输入结构和物理边界；隐藏作者的具体计算路线与结论性答案，评估 Agent 是否能提出并验证合理的机制/计算方案。

本轮不引入论文特例关键词，不让代码替 Stage06/07 Agent 作科学裁决，也不把所有任务强行改造成 ARCHE 的三种 Case。ARCHE Case2 只作为自主模式的信息边界和任务形态参考。

本轮要解决的核心问题分为三类：

1. 任务选择策略没有把“整篇路线优先、核心子过程降级”表达成可执行决策。
2. 自主模式的公开边界仍容易误删必要的物理事实，或泄漏作者方法/答案。
3. Stage06/07 产物合同仍有机械缺口（`source_id`、`route_fidelity`、`results_schema`、模式差异比较、发布状态语义），导致科学审计通过后仍无法发布。

## 2. 来自最近测试的证据与问题归类

最近两个测试目录为：

- `runs/stage06-07-fifth-round-paper6904-deepseek-v4-pro-0813-20260818T095630Z`
- `runs/stage06-07-fifth-round-paper6904-gpt-5.6-sol-20260818T095630Z`

两者均完成了 Stage06A、Stage06B、Stage07 的 Agent 运行，科学审计分别为 `approved_with_repairs`，但没有发布，主要因为机械合同失败。

### 2.1 代码/合同问题（应由代码修复）

- autonomous `task_info.json` 删除了 `source_id`，而 evaluator schema 将其设为必填，导致真实加载失败。
- `route_fidelity` 只在已有 rubric 条目时才会被归一化；Agent 没生成该条目时，代码只能报告缺失，不能进行低风险合同补齐。
- mode pair gate 仍将自主模式中性化后的结果字段名和文件名当成科学资产不一致，产生必然误报。
- DeepSeek 产物缺少 `results_schema`，代码未在 Stage06 handoff 或早期合同检查中明确指出缺失。
- `passed=true`、Agent 的科学决定、机械门禁和发布状态并列出现，语义混淆。
- 并发运行的 `history run_id` 可能相同，影响追踪。
- `stage_summary.json` 中 `paper_id/document_id` 为空，不能可靠关联上下游。

这些问题不能通过增加科学死规则解决，应通过统一合同、归一化和状态字段解决。

### 2.2 Prompt/角色边界问题（应由 Prompt 与输入裁剪修复）

- “整篇路线优先”没有要求 Agent 先证明整篇路线不可取，再降级到子过程。
- 自主模式没有用“观察事实 / 必需物理边界 / 作者实现方法 / 作者结论”四类边界说明可保留与必须隐藏的信息。
- Stage07 没有明确要求检查候选反应/机制的质量守恒、参考态闭合、TS 类型与计算动作是否匹配等通用科学一致性。
- Stage06A、Stage06B 的职责虽然已基本拆开，但转换器仍可能因看不到全文而无法判断某段信息是否属于作者路线；转换器应只处理带有来源分类的 handoff，而不是自行猜测。
- Agent 输出过多重复 trace、receipt 和内部合同，增加 token 消耗且污染最终任务目录。

### 2.3 模型/环境能力问题（不作为代码裁决）

- DeepSeek Pro 选择了整条复杂路线，GPT 选择了核心子过程；两种选择都可能合理，不能以“更短”或“更长”直接判错。
- DeepSeek 的模型元数据 fallback、GPT Code Mode spawn warning 属于 harness/环境问题；本轮只记录，不将其伪装成科学失败。
- Agent 未公开电荷/多重度、错误命名某些结构、遗漏某个实验事实等，首先归因于模型能力或 Prompt 清晰度；只有当合同要求未定义或代码错误覆盖 Agent 输出时，才归因于代码。

## 3. ARCHE Case2 提炼出的自主模式原则

### 3.1 Case2 的科学任务形态

ARCHE Case2 的输入是一个未预先指定机制的蓝光驱动 α-iodoboronate C–I cleavage 反应。公开内容包括：

- 底物、产物和反应组分（HPPh2、Cs2CO3）；
- 溶剂体系、450 nm 光照、反应温度/产率等实验条件；
- 可用于提出问题的实验观察（如光、碱、膦和自由基抑制剂对反应的影响）；
- 研究目标：提出并比较 concerted、ionic、radical、photo-induced 等可能解释。

没有在初始问题中直接给出作者最终提出的 CsPPh2 复合物、S2 激发、64.0 kcal/mol 等答案性信息。Agent 先生成多个假设，计算排除不相容路径，再根据矛盾反思并提出新的复合物假设。

### 3.2 自主模式应公开的信息

自主模式必须公开足以定义科学问题、执行计算和解释结果的事实，但不应公开作者的实现路线或答案。信息分类如下：

| 信息类别 | 自主模式策略 | 例子 |
|---|---|---|
| 科学目标 | 保留 | 判断哪些机制可解释实验反应及光化学约束 |
| 原始实验事实 | 保留 | 底物/产物、试剂、当量、溶剂、温度、波长、产率、对照结果 |
| 计算输入观测 | 保留 | 公开的结构坐标、实验测得或任务规定的边界条件 |
| 物理边界 | 保留 | 光子能量来源、相态/溶剂环境、温度、压力、总电荷/自旋约束（若输入体系需要） |
| 工具箱可用软件 | 保留为软件家族清单 | 例如 Gaussian、RDKit；不提供作者实际 route |
| 方法家族 | 可作为问题空间提示 | 如“可考虑基态、激发态、自由基或离子模型”；不公开论文采用的具体 functional/basis/route |
| 作者实现方法 | 隐藏 | functional、basis、dispersion、SCRF 细节、特定 TS/IRC 路线、作者计算顺序 |
| 作者命名的机制/中间体 | 默认隐藏或中性化 | CsPPh2、Mechanism G、NH3-assisted 等作者标签 |
| 作者解释 | 隐藏 | “该复合物通过协同 push–pull 降低激发能”等解释 |
| 论文最终结论与数值 GT | 隐藏 | 64.0、63.6、-3.0、favored mechanism 等答案性内容 |

“可保留哪些物理边界”不是固定关键词规则，而是一个通用判定：删除某项后，任务是否仍能定义实验条件、守恒约束和可解释的目标。不能删除溶剂、温度、光波长、电荷/自旋等使目标不可定义的事实；可以删除作者如何在软件中实现这些事实的 route 字符串。

### 3.3 自主模式的诚实命名

如果任务给出固定候选结构或固定候选机制，它应标记为 `bounded_autonomous_comparison`（或 evaluator 认可的等价枚举），而不是宣传成完全开放的“从零发现”。只有不给候选路线/候选结构、让 Agent 自行提出和筛选假设时，才可标记为更开放的 discovery 类任务。

## 4. 计算路线选择策略

### 4.1 默认策略：整篇计算路线优先

Stage06A 首先根据正文、补充材料和 Stage05 candidate 参考，重建论文围绕主要科学问题的完整计算路线。整篇路线包括能够支撑主要结论的连续步骤、必要中间产物、关键比较和最终解释，不等同于把论文中所有附带分析全部塞入任务。

Stage05 输出只能作为候选提示；Stage06A 可以修正其范围，但必须以论文正文和补充材料证据为主。

### 4.2 只有四类证据允许降级为核心子过程

当整篇路线不适合 benchmark 时，Agent 必须在 handoff 中给出证据化的 `downgrade_reasons`，只能来自：

1. 计算成本过高或不可接受的墙钟时间（例如关键作业预计十多个小时且会使评测无法重复）；
2. 关键输入数据或中间结构在论文/补充材料中缺失或无法可靠重建；
3. 论文路线依赖工具箱未覆盖的软件家族，且当前任务无法在不改变科学问题的情况下替代；
4. 整篇路线包含无法闭合、不可复现的步骤，继续纳入会使评估目标失真。

Agent 的偏好、任务较长、想节省 token、某个子过程更容易写，不构成降级理由。代码不根据固定步数或文件数量自动判定复杂度，只保存 Agent 的证据和估计。

### 4.3 核心子过程的选择标准

降级时选择的不是任意“第一步”或最短步骤，而是整篇路线中同时满足以下条件的最小连续子过程：

- 直接支撑论文主要科学结论或决定性机制判断；
- 有清楚的输入、计算动作、输出和验证标准；
- 包含足够的中间关键结论与至少一个最终结论；
- 能独立构成可执行、可评分的科学目标；
- 在可接受的成本与工具覆盖范围内可复现。

Stage06A 必须记录 `claim_coverage`、`omitted_workflow_parts`、`why_this_subworkflow_is_core` 和 `selection_confidence`。这些是审计证据，不是代码裁决字段。

### 4.4 选择输出结构

建议在 private handoff 中增加以下语义字段（字段名可按现有 schema 归一化）：

```json
{
  "workflow_scope": "whole_paper_route | core_scientific_subworkflow",
  "selection_reason": "evidence-based narrative",
  "downgrade_reasons": [],
  "claim_coverage": ["claim_id"],
  "omitted_workflow_parts": [],
  "estimated_cost": {"relative": "low|medium|high", "basis": "agent estimate"},
  "software_coverage": {"available": [], "missing": [], "alternatives": []}
}
```

该字段不包含 canonical answer，不进入 autonomous public surface。

## 5. Stage06 设计

### 5.1 Stage06A：主构建器

输入只保留对科学判断必要的材料：论文正文解析、补充材料解析、PDF/原文路径、Stage05 candidate 摘要、只读工具箱软件家族清单和现有评估 schema 说明。去除重复全文、副本 receipt、旧阶段冗余日志和无关中间 trace。

职责顺序：

1. 抽取围绕科学目标的完整计算路线和证据链；
2. 判断整篇路线是否可复现；
3. 默认构建整篇路线，只有出现 4.2 的证据化 blocker 才选择核心子过程；
4. 先完成论文复现模式 draft、private hidden reference、key points 和 acceptance profile；
5. 生成供 Stage06B 使用的 conversion handoff，其中明确标注每个信息片段属于“可公开实验事实”“可公开物理边界”“论文实现方法”“答案性内容”；
6. 报告工具箱已安装软件家族、缺失软件和建议，但不修改工具箱。

Stage06A 不生成最终 autonomous public task，不复制完整论文路线到 autonomous 目录，不写无用途的 conversion receipt。

### 5.2 Stage06B：窄职责自主模式转换器

Stage06B 不需要重新阅读整篇论文，也不应凭文件名猜测哪些信息是路线。它只读取 Stage06A 生成的 handoff、reproduction draft、公开边界分类和必要输入资产，然后：

- 复制论文复现任务为独立 autonomous 工作区；
- 删除/中性化被分类为作者实现方法、作者标签、答案性内容的公开表面；
- 保留实验事实、物理边界、结构和任务目标所必需的信息；
- 生成 autonomous 的中性任务说明、输入资产名、rubric 和 submission schema；
- 不改变 hidden ground truth 的真实答案、容差和结论；
- 不新增科学结论，不重选 workflow；发现 handoff 分类不确定时，原样报告 `conversion_uncertainty` 供 Stage07 审计。

转换输出只包含评估任务必需文件。来源分类、删除清单、转换合同等内部材料留在外层 staging/audit 目录，禁止进入最终任务目录。

### 5.3 两个 Agent 的工作区和信息传递

Stage06A、Stage06B、Stage07 使用独立 workspace。阶段之间只通过显式复制的 handoff/reproduction bundle 传递，不共享可写目录。最终目录结构保持：

```text
pair_root/
  paper_info.json                 # 与两个任务同级，含来源追溯信息
  paper_reproduction/             # 仅复现任务文件
  autonomous_research/            # 仅自主任务文件
  stage07_audit/                  # 外层审计证据，不发布
```

## 6. Stage07 设计

Stage07 是科学审计 Agent，拥有对任务科学可用性的最终意见，但不由代码替它决定“科学上通过/拒绝”。它先审计并优先修复 Stage06 的工作流；只有 Stage06 工作流不可用且论文中存在另一个完整、重要、可复现的工作流时，才重新设计并输出明确的 `workflow_redesign_required` 状态。

审计顺序：

1. 检查科学目标是否明确、是否有中间关键结论和最终结论；
2. 检查输入—计算—输出—评价链是否闭合，包括参考态、原子/电荷/自旋守恒、溶剂/温度/光照等边界；
3. 检查整篇路线或核心子过程的选择理由是否与 4.2/4.3 一致；
4. 检查 reproduction 是否公开足够的论文路线，autonomous 是否只隐藏作者实现方法而保留任务定义所需事实；
5. 修复小问题：缺少字段、边界条件表述、结论/中间 key point、错误标签、路线泄漏和 rubric 绑定；
6. 遇到重大问题（关键数据缺失、无法复现、工作流在科学上不可闭合、成本不可接受且无合适子过程）才拒绝；
7. 如果原工作流不可用但发现替代核心工作流，优先记录替代方案并输出 `workflow_redesign_required`，不把它伪装成普通修复。

Stage07 的审计输出建议拆分为：

```json
{
  "scientific_audit_decision": "approved|approved_with_repairs|rejected|workflow_redesign_required",
  "repair_summary": [],
  "major_blockers": [],
  "workflow_scope_review": {},
  "toolbox_observation": {},
  "publish_recommendation": "ready|needs_software|missing_data|too_expensive|redesign_required"
}
```

`publish_recommendation` 是客观发布分类，不应被机械 gate 改写为科学决定。

## 7. 自主模式公开边界合同

### 7.1 reproduction 与 autonomous 的差异

| 内容 | reproduction | autonomous |
|---|---|---|
| 科学目标 | 共享 | 共享 |
| 实验事实/计算输入观测 | 共享 | 共享 |
| 物理边界条件 | 共享 | 共享 |
| 作者 route、functional、basis、SCRF、步骤顺序 | 公开 | 隐藏/中性化 |
| 作者命名机制与最终数值 | 仅可放 hidden reference，不进 public | 隐藏 |
| 工具箱软件家族 | 可公开 | 可公开 |
| 评估结论 acceptance profile | 同一 profile | 同一 profile |
| 过程 rubric | 可不同 | 可不同，但结论语义必须一致 |

### 7.2 不能误删的边界

转换器不得删除以下定义问题所需事实：反应物/产物结构、溶剂或相态、温度、压力、光照波长/能量、实验当量、总电荷与多重度约束、必要的实验对照和已公开观测。对于未知但必需的量，应标为“需要 Agent 自行确定/提出假设”，不能悄悄删除。

### 7.3 可以隐藏的方法信息

隐藏论文作者使用的具体 functional、basis、dispersion、solvation implementation、Gaussian route、收敛设置、TS/IRC 处理顺序、特定中间体命名和作者给出的最终机制。可以保留“可考虑哪些方法家族”的问题提示，但不能让提示直接等价于论文答案。

## 8. 机械合同与 evaluator 对齐

### 8.1 代码只做机械工作

代码可以做：目录复制、文件白名单、JSON schema、ID/mode 归一化、路径安全、hash、manifest、evaluator load、结果字段存在性、staging 清理和审计事实记录。代码不能做：判断机制是否正确、选择整篇还是子过程、根据固定阈值拒绝科学任务、覆盖 Agent 的 scientific decision。

### 8.2 下一轮必须修复的合同项

1. **匿名来源标识**：为 autonomous 提供不泄漏 DOI/标题的稳定匿名 `source_id`，或让 evaluator 明确把 provenance 从 public TaskInfo 移出；不能回填真实 DOI。
2. **route fidelity**：统一结构化 `criterion_type=route_fidelity`。若 Agent 未生成，Stage07 可要求修复；代码只做低风险 schema 归一化，不覆写已有 rubric 的科学含义。
3. **results_schema**：把 `submission_contract.results_schema` 设为通用必要合同，Stage06 handoff、Stage07 审计和 evaluator 使用同一份定义。
4. **模式差异比较**：submission contract 比较 required files、submission path 和语义结构，不比较自主中性化后的字段名/文件名；输入资产按 asset_id 对应的内容 hash 比较。
5. **发布状态拆分**：在 `audit_results.jsonl` 与 `stage_summary.json` 同时记录 `scientific_audit_passed`、`mechanical_contract_passed`、`publish_ready`，Agent 自报字段命名为 `agent_observed_*`。
6. **run_id/追踪**：使用微秒时间或 UUID，并把 `paper_id`、`document_id`、model/harness 写入 summary。
7. **发布树清理**：最终 bundle 只保留任务文件；转换分类、删除清单、内部 receipt、workspace 和 staging 目录必须留在外层审计目录。

### 8.3 机械 gate 的最小检查

机械 gate 应检查合同完整性，但不能因合法的自主脱敏而误报：

- mode/task_mode/task_id 合法且可归一化；
- `results_schema` 与 acceptance profile 的字段绑定存在；
- route fidelity criterion 在 reproduction 中存在；
- asset content hash 一致，允许 comment/文件名中性化；
- manifest/hash 与实际内容一致；
- published tree 无 workspace/staging/来源合同；
- evaluator 可真实加载 public TaskInfo、GroundTruth 和 submission contract。

对于无法机械判断的科学问题，gate 只记录 finding，交给 Stage07 Agent；不触发“代码裁决科学拒绝”。

## 9. Prompt 与输入裁剪调整

### 9.1 Stage06A Prompt 增补

- 明确“整篇路线优先”；降级必须填写 blocker、核心性证据、覆盖的主要 claim 和被省略部分。
- 明确目标是围绕一个科学问题的完整计算流程，不是机械收集论文所有计算。
- 要求为每个关键结论建立 `key_point -> evidence -> computation -> acceptance` 链。
- 要求将公开事实、物理边界、作者方法、答案性内容分类，供 Stage06B 使用。
- 明确软件版本不构成缺失；只判断软件家族是否可用。
- 删除要求生成重复自主任务、内部 receipt、长篇过程 trace 的指令。

### 9.2 Stage06B Prompt 增补

- 只按 Stage06A handoff 分类进行中和；不重新阅读全文、不重新选择 workflow。
- 保留定义科学问题和执行任务必需的物理边界；隐藏作者实现方法和答案。
- 对不确定分类输出 `conversion_uncertainty`，不要擅自删除关键事实。
- 只写最终任务所需文件，不写来源合同、删除清单、转换回执。

### 9.3 Stage07 Prompt 增补

- 先修复 Stage06 现有 workflow；只有不可用且存在替代核心路线时才 redesign。
- 用通用一致性表检查参考态、守恒、输入类型与计算动作、实验边界、证据定位和结论链。
- 区分重大 blocker 与可修复小问题；工具箱暂缺只标记 `needs_software`，不自动丢弃。
- 允许两个模式的过程 rubric 不同，但结论 acceptance profile 一致。
- 不把模型无法判断的科学细节交给代码硬编码；通过说明和证据请求 Agent 作判断。

### 9.4 输入去重与 token 控制

每个 Agent 只接收其职责所需的最小材料：

- Stage06A：正文/补充材料的去重解析、必要 PDF 索引、Stage05 摘要、工具箱软件清单和 schema 摘要；
- Stage06B：reproduction draft、handoff 分类、输入资产和 disclosure policy；
- Stage07：两个 public bundle、private hidden reference、handoff 摘要、工具箱软件清单和审计 schema。

禁止重复注入同一篇全文、已生成的重复 route 文件、旧阶段完整日志和多份同义合同。轨迹只保留外层 audit 目录中的摘要和错误信息。

## 10. 测试与验收计划

本轮代码确认后，先用 `deepseek-v4-pro-0813` 和 `gpt-5.6-sol` 对同一篇论文做回归；不得为该论文添加特殊规则。验收分三层：

### 10.1 科学任务验收（Agent 负责）

- 整篇路线优先；若降级，存在证据化 blocker；
- 任务围绕单一明确科学目标；
- 有中间 key points 与最终结论；
- 输入—计算—输出—评价链可执行；
- autonomous 保留必要事实、不泄漏作者路线/答案；
- Stage07 优先修复而非随意 redesign。

### 10.2 机械合同验收（代码负责）

- 两个 public bundle 可被 evaluator 真实加载；
- 匿名 `source_id`、`results_schema`、route fidelity、manifest、路径和 ID 合同闭合；
- 合法的 autonomous 文件中性化不触发 pair mismatch；
- 最终目录无内部来源合同和 staging 残留；
- 科学审计、机械合同和发布状态可分别读取。

### 10.3 回归与通用性

至少保留一份 round3/round5 产物作为 regression fixture，覆盖：匿名 source、route rubric、results schema、模式中性化和 evaluator load。通过单篇论文后，再用不同计算方向/不同软件组合的论文验证“整篇优先/核心子过程降级”没有论文特例。

## 11. 实施顺序与回滚边界

确认方案后按以下顺序实现：

1. 先提交当前代码和本方案文档到 git，建立版本基线。
2. 更新统一 mode/ID/source/schema 合同和 mechanical status 记录。
3. 修复 pair gate、results schema、route criterion、manifest/staging 检查。
4. 更新 Stage06A、Stage06B、Stage07 Prompt 和输入裁剪。
5. 接入真实 evaluator dry run，运行现有单测和 regression fixture。
6. 用两个模型跑一篇论文，检查科学轨迹与机械产物。
7. 若失败，先判断是代码合同、Prompt、模型或 harness，再做最小范围修复；不新增论文特例规则。

任何涉及 hidden GT 数值、论文科学结论或 autonomous 公开边界的改动，都必须在 Stage07 Agent 的审计证据中说明，代码不得静默覆盖。

## 12. 预期结果

本轮完成后，Stage06/07 应形成如下稳定闭环：

```text
论文正文/补充材料
        ↓
Stage06A：整篇路线优先，必要时选择最核心子过程
        ↓
论文复现 draft + hidden reference + disclosure handoff
        ↓
Stage06B：按分类复制并生成自主 public surface
        ↓
Stage07：优先修复原 workflow；必要时明确 redesign
        ↓
代码机械合同闭合 + evaluator 真实加载
        ↓
reproduction/ 与 autonomous/ 两个干净、可发布的评估任务目录
```

成功标准不是让代码替 Agent 选出“正确机制”，而是让 Agent 有足够空间完成科学构建和审计，同时让文件合同、模式隔离、追踪和评估加载可靠闭合。

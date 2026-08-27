# Stage06/07 v23 Token 效率、语义评估与终态控制修改方案

## 1. 文档状态

本文档是 v23 设计方案，当前只定义修改目标和实现边界，不修改代码，也不提交新一轮测试。

依据包括：

- v22 双模式科学任务定义；
- v22 五篇真实回归结果；
- v20/v22 已发布任务的逐文件对比；
- 用户关于数值与文本结论均可作为评估依据的最新反馈。

## 2. v23 总目标

v23 不改变已经确认的双模式定义：

```text
paper_reproduction
= 科学目标
+ 作者提出的科学路线（假设、候选方向或定性机理）
+ 被评测 Agent 自主规划计算
+ 计算、验证并判断作者主张是否成立

autonomous_research
= 相同科学目标
+ 研究前公开输入和物理边界
+ 不公开作者科学路线
+ 被评测 Agent 自主提出假设、候选或机理（若存在真实假设空间）
+ 自主规划计算、验证并形成结论
```

v23 重点解决四类问题：

1. Stage06 工具调用非进展循环和 token 浪费；
2. Bridge 在任务文件未完成时提前强制 terminal receipt；
3. reproduction 中作者科学路线与参考答案方向混淆；
4. evaluator 被错误理解成必须依赖 numeric rule，文本关键点和科学结论没有被正常视为评估依据。

## 3. 已确认的根因

### 3.1 Token 增长不是主要由科学阅读造成

五篇 Stage06 总 token 从 v20 的约 8.62M 增长到 v22 的约 27.97M，约为 3.24 倍。

`paper_76ae...` 的 150 个已完成 shell 调用中：

- 91 次 `find outputs`；
- 20 次重复读取 reproduction self-check；
- 7 次 `pwd`；
- 4 次 `ls outputs`；
- 至少 122/150 次属于没有文件变化支撑的重复检查。

`paper_945...` 的 106 个调用中，也有至少 56 次重复目录、Gate 或报告检查。

每次工具调用都会携带不断增长的历史上下文，因此一个很小的 `find` 也会重复计入原始 Prompt、
论文证据、已生成文件和之前全部工具记录。大量输入 token 命中 cache，但仍浪费请求次数、延迟、
上下文处理和执行稳定性。

### 3.2 `paper_76ae...` 在 152 次左右结束不是偶然

当前配置：

```text
synthesis_max_tool_calls = 180
synthesis_finalization_reserve = 28
```

因此 finalization 区间从第 `180 - 28 = 152` 次调用开始。

Stage06 又将：

```text
structured_artifact_path = outputs/construction_receipt.json
```

作为结构化终态。Bridge 在第 152 次附近开始强制 finalization，但当时 autonomous tree 尚未
生成。Agent 因此返回 `constructed` receipt，外部 Gate 随后发现 autonomous 的公开文件和五个
evaluator 文件全部缺失。

根因是：

```text
非进展循环
→ 到达 finalization reserve
→ receipt 被错误当成完整 task package
→ Bridge 强制结束
→ external Gate 正确阻断半成品
```

它不是 API 故障、resume 问题或科学不可构建。

## 4. Evaluator 的正式定位

### 4.1 不要求所有任务都依赖数值评分

计算化学任务可以由多类结果构成：

- 数值：能垒、能量、频率、几何参数、光谱量、速率等；
- 排序：候选、通道、产物、构象或机理的相对顺序；
- 条件：是否为 minimum、是否为一阶 saddle、路径是否连通、状态是否正确；
- 语义结论：机理是否被支持、哪个解释最符合证据、限制条件是否合理、结论是否由计算支撑。

因此 v23 不设置“至少一个 numeric rule”或“评估必须能够完全由确定性代码完成”的要求。
一个以机理、结构身份或科学解释为核心的任务可以没有 numeric rule，只要参考关键点、参考结论、
证据和 semantic/condition/ordering rules 足够具体。

### 4.2 Evaluator 不绑定具体评分执行器

Stage06/07 只负责生成科学上完整、具体、可判断的 evaluator reference，不在评估文件中指定后续
必须由确定性代码、大模型或人工中的哪一种方式执行评分。

评估文件应正常表达：

- 计算过程中必须完成和验证的关键点；
- 应获得的数值、排序、状态、结构身份或文本结论；
- 结论成立所依赖的计算证据；
- 会使任务结果无效的关键失败条件。

数值结果和文本结果都可以成为正式评估依据。benchmark runtime 后续可以根据规则内容选择合适的
评分执行方式，但该选择不写入合成任务的 evaluator 文件，也不成为 Stage06/07 的额外职责。

### 4.3 数值存在时仍正常生成数值规则

“允许语义评分”不等于“尽量不写数值规则”。当任务明确要求核心数值，且论文存在可信 reference
value 时，合成 Agent 仍应正常生成：

```json
{
  "rule_id": "...",
  "reference_id": "...",
  "type": "numeric",
  "target": 0.0,
  "unit": "...",
  "tolerance": 0.0,
  "binding": {
    "artifact_paths": ["report/results.json"],
    "fields": ["..."],
    "comparison": "..."
  }
}
```

target 和 tolerance 必须由 Agent 按科学证据正常制定，不能因为后续评分方式不同就省略。
Gate 只检查规则是否完整、字段是否可定位，不判断 tolerance 是否唯一正确。

### 4.4 结论本身可以成为主要评分规则

语义规则可以直接引用 reference conclusion：

```json
{
  "rule_id": "rule_final_mechanism",
  "reference_id": "conclusion_final_mechanism",
  "type": "semantic",
  "expected": "提交必须根据实际计算证据判断哪一种机理最受支持，并正确说明仍不能排除的替代解释。",
  "binding": {
    "artifact_paths": ["report/results.json"],
    "fields": ["$.conclusion", "$.mechanistic_evidence", "$.uncertainty"],
    "comparison": "比较提交结论与隐藏参考结论，并检查结论是否由提交中的计算证据支持。"
  }
}
```

semantic rule 不要求绑定到单个 scalar，可以绑定结论、支持证据、验证记录和不确定性字段。它不能
只写“答案合理”或“与论文一致”，必须给出具体 expected scientific content。评估文件不需要特别
声明该规则将由大模型判断。

### 4.5 保持 evaluator 文件精简

继续使用现有五个文件：

```text
reference_key_points.json
reference_conclusions.json
scoring_rules.json
evidence_map.json
critical_failures.json
```

继续使用四种 rule type：

```text
numeric
ordering
condition
semantic
```

本版不增加新的 rule type、评分执行器标签、人工复核标签、总分字段、权重字段或兼容字段。每个
task 根据科学内容选择必要规则，不追求规则数量。规则权重、总分聚合和通过阈值属于 benchmark
侧评分 runtime 的职责，不属于 Stage06/07 合成文件设计。

## 5. Stage06 Prompt 修改方案

### 5.1 将长工作流压缩成四个清晰里程碑

Prompt 只保留一次完整工作流说明：

```text
A. 完成 input closure、scientific core 和 private paper route
B. 完成 reproduction 全部文件，运行 reproduction Gate，只修复实际 findings
C. Gate passed 后立即完成 autonomous 全部文件，运行 full-pair Gate，只修复实际 findings
D. full-pair Gate passed 后写 construction_receipt.json，一次结束
```

删除散落在 Prompt 多个位置的重复 terminal receipt 警告，避免 Agent 因担心“最后一次写入”而
反复审计、不敢结束。

### 5.2 增加非进展约束

加入以下短规则：

- 文件没有变化时，不重复运行相同的 `find`、`ls`、`pwd` 或读取相同 Gate report；
- Gate passed 后，除非相关文件随后被修改，不重新读取或重跑该 Gate；
- reproduction self-check passed 后，下一次写文件必须推进 autonomous tree；
- 将同一模式的相关 JSON 和 task 文件分组写入，避免每个文件单独一次工具调用；
- 工具写入失败时立即修正该写入，不通过反复目录检查代替修复；
- 不输出无动作的“我会继续/我正在恢复”消息，直接执行下一里程碑。

这些约束只改善单次 Agent 行为，不增加 orchestrator retry、resume 或第二次对话。

### 5.3 加入一个短的双模式边界示例

不加入完整论文示例，只加入抽象 micro-example：

```text
允许 reproduction 公开：
“作者提出选择性来自催化剂组织下的分子内硫进攻，需要独立计算验证。”

禁止 reproduction 公开：
“S 通道比 R 通道低 1.9 kcal/mol，因此主要得到 S 产品。”

autonomous：
只给相同科学问题和研究前输入，要求 Agent 自主提出并比较选择性来源。
```

该示例说明概念边界，不提供特定论文模板、固定 schema 或化学硬编码。

### 5.4 加入一个短的 evaluator 示例

```text
numeric rule 用于明确数值目标；
semantic rule 可用于文本形式的最终机理、结构身份和证据链结论；
一个任务不必强行同时拥有四种 rule。
```

同时说明：numeric binding 应定位实际数值字段；semantic binding 可以定位结论和支持证据对象。

### 5.5 要求任务范围有限但不由代码规定化学搜索

对于结构、构象、TS、机理或 excited-state landscape 搜索，合成 Agent 应在 task instruction 中
给出任务特定的最低充分范围和停止依据，例如：

- 搜索哪些物理/化学空间；
- 候选如何生成、去重和晋级；
- 何时可以形成有限范围内的结论；
- 哪些未覆盖空间必须写入 limitations。

代码不统一生成候选，不预处理论文输入，也不规定固定候选数。

## 6. Bridge 与 Stage06 终态控制修改方案

### 6.1 Receipt 不再作为 task tree 完成的充分条件

Stage06 不应继续让 Bridge 根据单个：

`outputs/construction_receipt.json`

判断完整任务已生成。

建议：

- Stage06 final response 仍使用现有 receipt schema；
- Agent 仍在 full-pair Gate passed 后写 receipt；
- 取消 receipt 对 Bridge 的提前 artifact-complete 语义；
- Bridge 不在 task tree 未完成时强制 Agent 写 `constructed` receipt；
- 外部 Stage06 Gate 继续对 Agent 退出后的实际目录进行权威、只读机械检查。

这不增加“编排器强制检查 Agent self-check 结果”。Agent self-check 仍由 Prompt 要求执行；外部 Gate
仍是现有最终机械审查。

### 6.2 缩小 finalization reserve

将 Stage06 的 finalization reserve 从 28 调整到较小值，例如 4–8。它只为返回最终结构化 response
保留，不提前占用 28 个本可用于生成 autonomous 文件的调用。

### 6.3 不增加 retry/resume

v23 不增加：

- Stage06 conversion retry；
- Stage06B；
- 旧 session resume；
- 因 incomplete artifact 自动开始第二次 Agent 对话；
- 通过标签掩盖 incomplete output。

一次 Agent 如果仍未生成完整 task tree，external Gate 应正常给出 technical blocked，但 Bridge
不能主动制造这个 incomplete terminal state。

## 7. Stage07 科学审计修改方案

### 7.1 使用“答案反推测试”检查公开泄露

Stage07 先从私有 evaluator 提取：

- reference values；
- ordering；
- 最终候选或结果结构身份；
- final conclusions；
- tolerance。

然后检查所有公开表面：

- `task.md`；
- `task_info.json`；
- `submission_schema.json`；
- 文件名；
- public input 内容和注释。

通用判断：

> 如果被评测 Agent 不运行任何计算，仅阅读公开任务就能填写待评估 ordering、最终候选或主要
> 结论，则发生了答案泄露。

Stage07 通过语义比较完成该检查，不增加论文关键词、化合物特例或结果黑名单。

### 7.2 正确理解 reproduction scientific route

允许：

- 作者假设；
- 候选方向；
- 定性机理；
- 需要验证的解释。

禁止：

- 哪个候选最终胜出；
- 数值和方向性排序；
- 结果性 TS/intermediate/conformer；
- 完整 reference conclusion；
- tolerance。

例如 2aca 可以公开“作者用 charge transfer/delocalization 与 distortion 解释取代基效应”，
不能公开“16 最低、15 居中、17 最高”。

### 7.3 审计 evaluator 的科学可用性，而不是强制 numeric

Stage07 检查：

- key points 和 conclusions 是否具体、source-supported；
- semantic expected 是否包含真正的参考科学内容；
- submission 与隐藏 evaluator 是否提供了足以判断文本结论的内容；
- numeric rule 若存在，是否有 target/unit/tolerance；
- 数值、结论、验证和 critical failures 是否与任务及 schema 一致；
- 不因任务没有 numeric rule 而拒绝；
- 不因 semantic rule 无法由简单数值比较器直接判断而拒绝。

## 8. Common Gate 修改方案

Agent self-check 和 external Gate 继续使用同一份通用合同检查实现。

### 8.1 必须阻断

- 必要 evaluator 文件缺失或 JSON 无效；
- key points、conclusions、rules、evidence 或 critical failures 为空；
- evaluator-local ID 引用断裂；
- 一个关键点或结论完全没有对应 rule；
- numeric rule 缺少 target、unit、tolerance 或 binding；
- ordering/condition/semantic rule 缺少具体 expected 或 binding；
- binding 指向 submission schema 中不存在的字段；
- numeric binding 只停留在整个对象/数组，无法定位实际数值属性；
- task deliverable 与 submission schema 不一致。

### 8.2 不阻断

- 没有 numeric rule，但任务的核心本来是结构、机理或语义结论；
- semantic rule 的判断需要语义理解，而不是简单数值比较；
- tolerance 的具体科学选择；
- reference conclusion 的措辞不是固定模板；
- 不同论文使用不同 schema 结构；
- 规则数量少但已覆盖真正关键内容。

### 8.3 只产生 diagnostic

- numeric tolerance 需要人工科学复核；
- semantic conclusion 边界较宽但仍具体可判断；
- 开放搜索覆盖范围需要后续人工评估。

Gate 不尝试判断论文中心性、机理正确性或 tolerance 是否最优。

## 9. Runtime toolbox 文件处理

不再鼓励合成 Agent 将完整 `toolbox_capabilities.json` 复制到最终 task 的
`data/inputs`。该文件属于 runtime 能力描述，不是论文科学输入。

建议：

- 被评测 Agent 通过 benchmark runtime 正常看到实际工具；
- task package 只包含科学问题需要的输入；
- 若必须说明能力，只保留简短、通用、与实际 runtime 一致的描述，不按论文关键词裁剪；
- 不改变不同论文科学输入由模型判断和组织的原则。

## 10. 代码修改范围预案

待方案确认后，预计涉及：

- `src/stages/stage06_task_builder/prompts.py`
  - 精简工作流；
  - 增加非进展规则；
  - 增加两个 micro-examples；
  - 更新 evaluator 和双模式边界说明。
- `src/stages/stage06_task_builder/stage.py`
  - 修正 receipt/Bridge metadata；
  - 缩小 finalization reserve；
  - 升级 implementation version。
- `src/stages/stage07_task_judge/prompts.py`
  - 增加答案反推测试；
  - 区分 author route 和 result direction；
  - 接受文本关键点和科学结论作为 semantic 规则。
- `src/stages/stage07_task_judge/stage.py`
  - 升级 implementation version，不恢复 Stage07B。
- `src/stages/phase_gate.py`
  - 区分 numeric leaf binding 和 semantic evidence binding；
  - 不要求 numeric rule 必须存在；
  - 保持 self-check/external 共用实现。
- `src/agents/responses_bridge.py` 或 Stage06 harness metadata
  - 取消 receipt 在任务未完成时触发强制 finalization 的行为；
  - 优先通过 Stage06 局部配置解决，避免扩大通用 Bridge 复杂度。
- 定向测试文件
  - Prompt 契约；
  - semantic-only evaluator fixture；
  - mixed numeric/semantic evaluator fixture；
  - numeric binding leaf 检查；
  - finalization reserve/receipt 生命周期测试。

## 11. 测试计划

### 11.1 固定 fixture

必须覆盖：

1. 只有 semantic/condition rules 的机理任务可以通过 Gate；
2. 同时有 numeric 和 semantic rules 的任务可以通过；
3. numeric rule 缺 target/unit/tolerance 时阻断；
4. semantic rule expected 为空或只写模板话术时阻断；
5. numeric binding 只指向整个数组时阻断；
6. semantic binding 指向结论和支持证据对象时允许；
7. receipt 出现但 autonomous tree 缺失时，Bridge 不应提前判定完整；
8. self-check 与 external Gate 对同一 fixture 给出相同机械 findings。

### 11.2 真实论文回归

优先重跑三篇：

- `paper_2aca1dd116799b28`
  - reproduction 不再泄露 16/15/17 方向排序；
  - Stage07 能发现并修复语义等价的排序泄露。
- `paper_76ae2dc25f0a5aeb`
  - reproduction passed 后立即生成完整 autonomous tree；
  - 不在第 152 次附近被强制 constructed receipt。
- `paper_9455a82229de2427`
  - 保留 autonomous product discovery；
  - 消除重复 Gate、目录检查和 receipt 终止循环。

### 11.3 运行指标

不把 token 或工具调用数作为 Gate 条件，但回归报告必须统计：

- 每篇 Stage06/07 tool calls；
- 重复 `find/ls/pwd/report read/Gate` 次数；
- input/cache-hit/output tokens；
- reproduction Gate 次数；
- full-pair Gate 次数；
- 是否一次完成；
- 最终 scientific/technical/release 状态。

预期三篇 Stage06 大部分任务应控制在约 30–60 次有效工具调用范围，不再出现 100–150 次非进展
循环。该范围用于分析，不写成论文任务的机械拒绝规则。

## 12. 方案一致性验收标准

代码完成后必须逐项确认：

- 双模式定义未退回“reproduction 固定 protocol / autonomous 只删方法”；
- Prompt 中只有短抽象示例，没有论文特例或可复制模板；
- reproduction 不公开 reference ordering、结果结构和完整结论；
- autonomous 不公开作者科学路线；
- evaluator 正常支持数值与文本关键点、科学结论作为评估依据；
- 有明确数值时仍正常生成 numeric target/unit/tolerance；
- Gate 不要求每个任务必须有 numeric rule；
- semantic rule 具体、source-supported，并具有足够信息支持后续判断；
- receipt 不会在 task tree 不完整时触发 Bridge 提前 finalization；
- 没有新增 retry、resume、Stage06B、Stage07B 或兼容投影；
- 代码保持精简，没有论文或任务类型硬编码。

## 13. 已确认的职责边界

1. Stage06/07 负责生成过程关键点、参考结论、评分规则、证据映射和关键失败条件；
2. 评估依据既可以是数值，也可以是排序、状态、结构身份、机理或其他文本科学结论；
3. 评估文件不声明评分必须由大模型、确定性代码或人工执行，只保证规则科学具体且可以判断；
4. rule weight、总分聚合、pass threshold 和评分执行器选择由 benchmark 侧代码负责，本版不在
   evaluator 文件中设计这些字段；
5. 一个任务可以没有 numeric rule，但如果核心目标包含可信明确数值，合成 Agent 仍应正常生成
   numeric rule，不应把它替换为模糊文本；
6. semantic rule 可以成为主要评分规则，并可以同时检查结论和支持证据；
7. 人工后续仍可修改 tolerance 或 evaluator，但 Prompt 不以此为理由降低初始合成质量。

# Stage06/07 第六轮优化方案：最小边界、模式对齐与 Agent 科学审计

## 1. 文档目的

本方案综合以下材料：

- 第五轮方案及其代码归因；
- DeepSeek-v4-pro-0813 与 GPT-5.6-sol 的同论文 Codex 测试；
- `STAGE06_07_NEXT_ROUND_ANALYSIS_20260818.md`；
- 另一 Agent 对 Stage06/07 框架的复核意见；
- 用户对科学裁决、信息隔离、代码复杂度和向后兼容的约束。

本轮只定义修改方案，不修改代码。目标是让 Stage06/07 形成通用的合成数据阶段：

1. Stage06A 选择围绕明确科学目标的整篇计算路线，必要时选择最重要的核心子过程；
2. Stage06B 只做公共表面转换，保持答案盲；
3. Stage07 负责科学闭合、Ground Truth/binding 审计、修复、重构或拒绝；
4. 编排器只负责工作空间、文件传递、机械记录和发布，不代替 Agent 做科学裁决；
5. 保留历史任务可加载能力，不为了清理字段制造不必要的 breaking change。

## 2. 对上一版方案的修订结论

### 2.1 采纳：Stage06B 不接触正文/SI 中的答案材料

上一版建议把完整正文和补充材料直接提供给 Stage06B。该建议不采纳。

原因是 Stage06B 的输出是 autonomous 公共表面。如果它可以直接读取完整论文路线、答案和证据映射，就可能把作者路线或答案以文件名、描述、结构标签或任务指令的形式泄漏到 autonomous 任务中，破坏信息隔离。

采用以下替代方案：

- Stage06A 在构建时增加一次 `workflow_completeness_check`；
- Stage06A 输出私有的 `public_to_private_asset_map.json`，只保存匿名 public asset ID 与源文件/证据 ID 的映射，不放在任何公开任务目录；
- Stage07 同时读取完整正文/SI、Stage06 handoff 和该私有映射，在审计时恢复遗漏资产或重写公共表面；
- Stage06B 仍然只能读取 reproduction 任务和脱敏转换包，不读取 hidden reference、完整源材料或私有 Ground Truth。

### 2.2 采纳：pair ID 由编排器确定性生成

上一版仅建议给 `canonicalize_mode_task_contract()` 传入 pair ID，不足以解决问题。实测 GPT 在 Stage06 handoff 阶段已经生成了包含 `reproduction_pair` 的非规范 ID，说明根因是 Agent 被允许自由命名任务身份。

本轮改为：

```text
canonical_task_pair_id = <anonymous_paper_id>_task_pair
```

具体匿名 ID 规则由编排器统一生成。Agent 不再决定 `task_pair_id`，只能在科学内容中引用编排器提供的 ID。两个模式的任务 ID 由代码派生：

```text
<canonical_task_pair_id>_autonomous
<canonical_task_pair_id>_reproduction
```

旧任务仍可读取；新任务不再接受 Agent 自拟的 pair ID。迁移期间，代码应把旧 ID 记录为 `original_task_pair_id`，但不把旧 ID 继续作为新发布路径的主 ID。

### 2.3 采纳：机械阻断必须显式结束并报告

当前 active path 已经不会因为机械 finding 自动触发完整 Stage07 重试，但仍存在决策黑洞：Agent 返回 approved，机械检查失败后既不发布、也不重试，summary 又可能继续显示 approved。

本轮要求：

- 科学决定保留为 Agent 的决定；
- 机械发布失败单独生成 `mechanical_publish_blocked`；
- `stage_summary.json` 写入：
  - `mechanical_publish_blocked`；
  - `mechanical_approved_but_unpublished`；
  - `blocking_reasons`；
  - `publish_ready`；
- 不把机械阻断改写为 `rejected_scientific_unrepairable`；
- 不静默跳过发布；
- 是否再次运行 Agent 由显式技术恢复策略决定，默认不重复运行完整科学审计。

## 3. Autonomous 模式的定位必须诚实

当前 autonomous 同时出现以下互相牵制的要求：

- 不公开作者具体方法；
- 允许 Agent 自选方法和路线；
- 结论评分却严格对齐论文特定方法得到的绝对数值。

这不是 paper-specific bug，而是模式定义问题。下一轮需要从以下两种明确设计中选择一种，不能继续使用含混措辞：

### 方案 A：方法约束的自主工作流比较（推荐，改动较小）

- public task 明确提供定义目标所必需的物理边界，例如溶剂、温度、压力、电荷和自旋；
- 隐藏作者的 functional、basis、具体 route 和步骤顺序；
- autonomous 允许选择工作流和实现细节，但不是完全开放的方法发现；
- `autonomy_scope` 统一写为 `fixed_input_method_constrained_workflow`；
- 结论可以保留论文数值评分，但必须在 public task 中公开所有定义目标所需的物理条件。

### 方案 B：真正的方法探索

- 不固定作者路线；
- autonomous 结论主要评分排序、差值符号、趋势、关键中间结论和过程证据；
- 放宽方法相关绝对数值的容差，或不把论文特定绝对值作为硬门槛；
- `autonomy_scope` 写为 `fixed_input_method_discovery`。

本轮默认采用方案 A，以降低对现有 Evaluator 和 Ground Truth 的改动。若后续决定采用方案 B，需要单独修订 acceptance profile，不能只改一个 Prompt 词语。

## 4. 统一模式字段，但保留 Evaluator 兼容层

当前字段存在三套体系：目录名、`scientific_mode`、`task_mode`、`method_disclosure`、`pathway_disclosure` 的取值彼此交叉，导致代码依赖 canonicalize 做字符串修复。

### 4.1 新任务的规范来源字段

新任务在内部合同中只使用一个科学模式字段：

```json
{"mode": "autonomous_research"}
```

或：

```json
{"mode": "paper_reproduction"}
```

以下字段由代码从 `mode` 派生，不由 Agent 自由填写：

- Evaluator 兼容的 `task_mode`：
  - autonomous → `open_discovery`；
  - reproduction → `guided_reproduction`；
- `method_disclosure`；
- `pathway_disclosure`；
- 任务 ID 后缀。

这样既保持内部只有一个模式来源，又不破坏当前 Evaluator 的 Literal 枚举。后续 Evaluator schema 升级后，可移除兼容投影。

### 4.2 删除或停止写入的字段

- 不再由 Agent 独立写入 `scientific_mode`；
- 不再把 `pathway_disclosure` 当作独立决策字段；
- 不再通过多处 canonicalize 修复模式含义；
- 旧任务仍可读取，但发布新任务时由 `mode` 统一派生。

## 5. Stage06A 修改方案：自检而非代码裁决

### 5.1 Prompt 增加最小闭合记录

Stage06A 在选择工作流后，必须输出一份私有 `workflow_completeness_check`，至少覆盖：

| 字段 | 含义 |
|---|---|
| `full_workflow_considered` | 是否先检查了整篇论文的目标中心路线 |
| `selected_scope` | 选择整篇路线还是核心子过程 |
| `covered_claims` | 任务实际评估的中间/最终结论 |
| `excluded_claims` | 明确不覆盖的结论 |
| `required_assets` | 每个计算操作需要的结构、参考态和观测输入 |
| `workflow_steps` | 输入 → 动作 → 产物 → 验证标准 → evidence |
| `unresolved_questions` | 仍无法从正文/SI确认的问题 |
| `public_to_private_asset_map` | 匿名资产与源材料的私有映射 |

如果选择子过程，必须说明：

- 为什么整篇路线成本过高、数据不闭合、软件不可用或难以复现；
- 为什么该子过程是论文科学目标中最重要的部分；
- 它保留了哪些依赖、关键点和计算挑战。

### 5.2 代码只做非阻断观察

代码可以对以下内容做结构化观察，并把 finding 反馈给 Stage06A 的有限自修复回合：

- workflow step 引用的文件是否实际存在；
- asset ID 是否能映射到 materialized path；
- 是否存在明显悬空的 step/output 引用；
- handoff 是否包含 `public_to_private_asset_map.json`。

这些观察不判断化学正确性、不判断参考态是否科学充分、不自动拒绝任务。最多允许一次定向回合，避免重复读取论文和无界 token 消耗。

### 5.3 Stage06A 不能做的事

- 不能把任意易算的一步包装成核心科学目标；
- 不能把无法确认的答案写入 public scope；
- 不能让 Agent 自拟 pair ID；
- 不能把 hidden reference 或答案映射传给 Stage06B。

## 6. Stage06B 修改方案：保持答案盲的窄转换器

Stage06B 输入保持最小化：

```text
inputs/task_pair/paper_reproduction/
inputs/task_pair/conversion_packet/
```

其中 conversion packet 只包含：

- 公共科学目标；
- 匿名 Key Point ID；
- 物理边界分类；
- 脱敏规则；
- public asset ID 和已 materialized 文件路径；
- 共享 submission contract 的字段形状。

不得提供：

- 完整正文/SI；
- hidden reference；
- canonical answer；
- `public_to_private_asset_map`；
- route evidence map 中能恢复答案的内容。

Stage06B 可以：

- 删除作者方法和路线泄漏；
- 中性化文件名、XYZ comment 和 JSON 描述；
- 保留问题定义必需的物理边界；
- 对 conversion packet 中标为 `uncertain` 的字段采取 preserve + report；
- 发现公共资产疑似缺失时在 `conversion_report.json` 中报告，不猜测和补造结构。

Stage06B 不负责工作流科学闭合，也不负责重新选择论文工作流。遗漏资产由 Stage06A 自检或 Stage07 使用私有映射和源材料恢复。

## 7. Stage07 修改方案：增强 Agent 审计，不增强代码科学裁决

### 7.1 Stage07 输入

Stage07 继续获得：

- Stage06 public task pair；
- 完整正文/SI 和解析证据；
- `public_to_private_asset_map.json`；
- Stage06 completeness check；
- hidden reference 草稿；
- toolbox 软件清单。

这些材料只给 Stage07，不进入 autonomous public task。

### 7.2 Stage07 必须执行的顺序

1. 优先审计并修复 Stage06 选定的目标中心 workflow；
2. 核对每个 scored quantity 的输入、参考态、动作、产物、验证标准和 evidence；
3. 核对每个 Ground Truth 与 acceptance binding 的一一对应关系；
4. 修复可从正文/SI或私有映射确认的小问题；
5. 如果原 workflow 无法修复，检查论文中另一个完整且重要的 workflow；
6. 只有没有可复现工作流时才拒绝。

Stage07 输出中必须保留一张六行科学审计表，每行包含：

- `status`: `closed | repairable | unrepairable`；
- evidence IDs；
- 检查结论；
- 实际修改文件；
- 若未修复，说明拒绝或重构理由。

六行分别覆盖：目标范围、输入/边界、参考态和计量、动作与产物、Ground Truth/binding、自主模式信息边界。

这张表是 Agent 的科学证据，不由编排器填写或推导。

### 7.3 Stage07 对 evaluator binding 的职责

Stage07 必须逐条确认：

```text
GT item
→ acceptance profile
→ observed field / selector
→ submission_contract result schema
→ task.md 要求的输出
→ 可评分的中间/最终结论
```

代码只做：JSON 可解析、路径安全、schema load 诊断和报告；不根据 JSONPath 的科学含义自动批准或拒绝。

## 8. Hidden Reference 简化方案

### 8.1 唯一权威文件

Stage06 hidden builder 只写：

```text
hidden_reference/ground_truth_common.json
```

该文件包含两种模式共同的：

- ground truth items；
- intermediate/final conclusion；
- acceptance profiles；
- evidence grades 和 evidence IDs；
- shared conclusion rubric；
- critical failure 和 evidence policy。

### 8.2 模式差异

模式差异只保留在：

- reproduction process rubric；
- autonomous process rubric；
- mode-specific managed computation/process policy。

如果当前 Evaluator 仍要求 `ground_truth_reproduction.json` 和 `ground_truth_autonomous.json`，它们只能由代码从 `ground_truth_common.json` 机械投影生成，禁止 Agent 分别编辑。投影文件不属于新的权威来源。

## 9. task.md 与 task_info.task 的兼容处理

直接删除 `task_info.task` 会破坏当前 Evaluator，因为 `TaskInfo.task` 目前是必填字段。因此本轮不做直接 breaking change。

采用两阶段迁移：

### 第六轮

- `task.md` 成为唯一人工编辑的任务指令；
- Agent 不再独立生成或修改 `task_info.task`；
- 发布前代码从 `task.md` 读取内容，写入 `task_info.task` 作为兼容派生字段；
- 若两者不一致，以 `task.md` 为准并重新生成 `task_info.task`；
- 所有 validator 停止把 `task_info.task` 当作独立来源。

### 后续 Evaluator 迁移

- 将 `TaskInfo.task` 改为可选或默认空字符串；
- Evaluator 优先读取同目录 `task.md`，旧包 fallback 到 `task_info.task`；
- 历史任务迁移完成后再删除兼容字段。

## 10. Complexity profile 重构

当前 complexity 混合了任务复杂度、workflow 结构和过程 rubric 元数据，导致字段 alias 和重复计数不断增加。

新结构只保留任务复杂度：

```json
{
  "level": "medium | high",
  "rationale": "为什么该科学目标包含多步计算、分支、验证或迭代",
  "estimated_tool_calls": {
    "min": 10,
    "typical": 25
  }
}
```

移出 complexity：

- workflow 依赖、分支、体系/状态数量 → `workflow_spec`；
- validation 和 iterative criterion 数量 → 从 `process_rubric` 派生，不再重复存储。

删除或停止写入：

- `core_operation_count`、`core_computation_count`、`tool_call_count` 等 legacy alias；
- `dependency_edge_count`、`parallel_branch_count` 等 workflow 字段；
- `iterative_decision_count`、`validation_operation_count` 等 rubric 字段；
- `complexity_level` 与 `level` 双写。

复杂度只做资源和任务难度说明，不作为编排器科学裁决条件。

## 11. 代码侧确定性缺陷与处理

| 编号 | 当前问题 | 修改方案 | 是否涉及科学裁决 |
|---|---|---|---|
| C1 | 缺少 route criterion 时代码覆写 rubric[0] | 删除覆写；只记录机械 finding，交 Stage07 修复 | 否 |
| C2 | route fidelity 同时依赖关键词和 `criterion_type` | 统一使用 `criterion_type=route_fidelity` | 否 |
| C3 | evaluator dry-run 名称容易被理解为已完成真实评分 | 改名为 `schema_load_diagnostic`；真实 scoring 未运行就明确写 `not_run` | 否 |
| C4 | Agent 可自由命名 pair ID | 编排器生成 canonical pair ID，Agent 只消费 | 否 |
| C5 | approved + mechanical blocked 后静默不发布 | 写显式 blocked 状态、计数和阻断原因 | 否 |
| C6 | deterministic_stage07_audit、重复 gate、重复 finalize 逻辑已失去 active 作用 | 删除未使用代码和重复调用，保留单一机械记录路径 | 否 |
| C7 | common hidden policy 被无差别复制到 autonomous | shared conclusion policy 与 mode-specific process policy 分离 | 否 |
| C8 | boundary 条目格式不一致时转换包静默丢弃 | 无损保留并标记 `unclassified`，交 Stage06B/Stage07 判断 | 否 |
| C9 | complexity alias 和多套计数字段 | 按第10节收敛为最小 schema | 否 |
| C10 | `task_info.task` 与 task.md 可能漂移 | 发布时从 task.md 派生兼容字段 | 否 |

以下内容明确不写入代码规则：

- 特定分子、特定溶剂、Gaussian route 的关键词判断；
- “输入文件数量不足就拒绝”；
- 由代码推断 charge/multiplicity、TS 类型或参考态；
- 由代码判断某个 Ground Truth 是否科学正确；
- 为 GPT 或 paper 6904 增加特殊分支。

## 12. Prompt 精简原则

下一轮同步清理 Prompt：

- 删除重复的“再次读取全部文件”“生成完整过程日志”“生成 conversion receipt”等无效指令；
- Stage06A 只保留科学目标选择、workflow completeness、证据链和 reproduction 构建；
- Stage06B 只保留脱敏、公共边界保留、uncertain 报告；
- Stage07 只保留优先修复原 workflow、逐项 binding 审计、必要时重构/拒绝；
- 机械合同、路径安全、manifest 由编排器完成，不在 Agent Prompt 中反复解释；
- 每个 Agent 的最终 receipt 只返回状态、artifact path、关键 finding 和修改文件。

## 13. 修改后的验收标准

### 代码验收

- 编排器不产生科学 approve/reject；
- `approved + mechanical blocked` 可见且有明确终态；
- 新任务 pair ID 始终确定性；
- hidden common 是唯一人工维护的 Ground Truth 来源；
- task.md 是任务指令唯一编辑源，task_info.task 仅为兼容派生；
- complexity 没有 legacy alias 和 workflow/rubric 重复字段；
- 没有未调用的 Stage07 科学审计函数和重复 gate 路径。

### Agent 验收

- Stage06A 输出 workflow completeness 和私有 asset map；
- Stage06B 不可读取正文/SI、hidden reference 或私有映射；
- Stage07 能用正文/SI和私有映射恢复遗漏资产；
- Stage07 的六行审计表真实反映闭合、修复和拒绝理由；
- 每个 GT item 都有一条可解释的 binding 链；
- autonomous 的方法自由度和 acceptance profile 语义一致；
- 整篇路线过复杂时，选取的子过程仍然是论文核心科学目标的一部分。

### 回归测试

1. 使用现有 DeepSeek 完整产物作为正向 fixture；
2. 使用现有 GPT 缺失资产产物作为负向 fixture，验证 Stage07 能发现并修复/拒绝，而不是由代码直接裁决；
3. 使用一篇不同类型论文验证没有 paper-6904 特例规则；
4. 对比 Codex harness 下 DeepSeek 和 GPT 的 workflow completeness、asset map、binding audit 和最终任务质量，不以工具调用次数单独判断优劣。

## 14. 不在第六轮处理的内容

- 不重新设计整个 Evaluator 评分服务；
- 不把真实 Agent submission scoring 塞进 Stage07 编排器；
- 不给 Stage06B 正文/SI答案访问权；
- 不增加针对单篇论文的科学关键词规则；
- 不用代码替 Agent 判断某个工作流是否科学重要；
- 不为了清理字段立即破坏历史任务兼容性。

## 15. 用户最终确认的边界修订

本节覆盖第 9 节关于 `task_info.task` 的兼容建议：用户明确要求任务指令只保留在
`task.md`，不保留 `task_info.task` 兼容派生字段。因此本轮实现删除该字段，并同步让
Evaluator/repository/runtime 从同目录 `task.md` 读取任务指令。历史 JSON 中若残留该额外
字段，Pydantic 兼容加载时忽略它，但新发布任务不会再写入；历史任务若没有 `task.md`，
不列入可运行任务清单。

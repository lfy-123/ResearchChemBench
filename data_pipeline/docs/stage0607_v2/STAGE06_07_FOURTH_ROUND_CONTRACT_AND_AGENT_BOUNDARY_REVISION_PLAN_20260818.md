# Stage06/07 第四轮修改方案

## 1. 文档目的

本文是 Stage06/Stage07 第四轮修改方案，综合以下材料形成：

- Round 3 真实运行结果：`stage06-07-agent-authority-round3-20260818-paper6904-pro0813`；
- 对 Round 3 任务和轨迹的独立审查；
- 另一 Agent 对当前代码、Evaluator 合同和运行结果的分析；
- 当前项目中 Stage06/07 的 active path、Evaluator schema 和发布逻辑。

本轮的目标是修复通用协议和权限边界，不为论文 `paper_6904a9c8c09855cc` 增加关键词、路线或分子特例。

本轮仍然遵守以下原则：

1. 科学工作流的选择、完整性判断和 Stage07 最终科学裁决由 Agent 完成。
2. 编排器只负责隔离工作空间、文件传递、机械合同、Evaluator 可加载性和发布。
3. 机械 gate 失败只能阻止不完整或不可加载的文件发布，不能把 Agent 的科学 `approved` 改成科学 `rejected`。
4. Stage06B 保持窄职责，不负责重新选择科学工作流，也不负责重建 Ground Truth。
5. 不再把更多化学死规则写入 Python；需要增加的约束优先使用通用字段和明确 Prompt 表达。

## 2. Round 3 的已确认问题

### 2.1 Mode、task_mode 和 task ID 没有形成闭合合同

Round 3 最终自主任务的 [task_info.json](../../runs/stage06-07-agent-authority-round3-20260818-paper6904-pro0813/stage_07_task_audit/published_tasks/paper_6904a9c8c09855cc_autonomous_research/task_info.json) 中为：

```json
{
  "mode": "autonomous_research",
  "task_mode": "autonomous_research",
  "scientific_mode": "autonomous_research",
  "task_id": "..._autonomous_research"
}
```

但 Evaluator 的 `TaskInfo.task_mode` 合同只接受 `open_discovery` 或 `guided_reproduction`，当前 Stage06 内部 validator 也将自主模式映射为 `open_discovery`，并要求 task ID 以 `_autonomous` 结尾。

这不是模型科学判断问题，而是生成协议、validator 和最终 Agent 修改结果没有统一。

### 2.2 Reproduction 公共 scope 泄漏了被评分的科学结论

Round 3 的 reproduction `workflow_scope.supported_primary_claims` 中包含：

- NH3-assisted bimolecular route 是优选路线；
- barrier difference 为 5.1 kcal/mol。

论文复现模式可以公开作者执行路线和方法，但不应在公共任务的 scope、任务说明、workflow summary 或 rubric 中直接给出最终答案、答案排序或目标数值。最终结论应只存在于 hidden reference 和 evaluator registry。

### 2.3 Stage06B 的输入包职责不闭合

当前 `_setup_converter_inputs` 会把以下材料复制给 Stage06B：

- 完整 reproduction public task；
- `objective_card.json`；
- `key_points.json`；
- `conversion_brief.json`。

本轮这些辅助文件仍然包含 PBE0、intramolecular、NH3-assisted、19.2、24.3、5.1 和路线结论等信息。它们不一定被发布给最终 benchmark Agent，但会让 Stage06B 获得答案相关信息，并且让“删除哪些信息、保留哪些信息”的职责变得含糊。

同时，Stage06A Prompt 仍要求生成 autonomous copy，而 active code 又调用 Stage06B 覆盖 autonomous surface，形成职责重叠。

### 2.4 Route fidelity rubric 没有形成可识别的合同

Round 3 reproduction 的 `process_rubric.json` 虽然有 `input_route_setup` 等路线相关条目，但没有稳定、结构化的 `paper_route_fidelity` criterion。当前 validator 主要依赖自由文本中是否包含 `route fidelity`、`route_fidelity` 或 `paper route`，而 active Stage07 path 又没有执行完整的 `validate_task_pair`。

结果是：任务可以声称 `contract_status=passed`，但没有可靠证明 reproduction 过程分真正评价了作者路线的忠实执行。

### 2.5 complexity profile 存在重复命名

运行结果中同时出现：

- `scientific_core_operation_count` 与 `core_computation_count`；
- `estimated_typical_tool_calls` 与 `tool_call_count`；
- `dependency_edge_count` 与 `dependency_count`。

代码中存在 alias normalizer，但最终输出仍可能同时保留两套字段，导致维护和统计漂移。

### 2.6 evaluator dry run 仍是 Agent 自报

Stage07 Agent 返回 `evaluator_dry_run_status=passed` 后，active path 主要检查 Agent 指向的 `outputs/task_pair` 是否存在、是否非空以及路径是否安全；没有实际加载最终发布任务的 `task_info.json`、`task_spec.json`、submission contract 和 evaluator ground truth 来验证可执行性。

这会把“Evaluator 能否真正加载”与“Agent 认为可以加载”混为一谈。

### 2.7 发布临时目录没有清理

`_publish_mode_bundles` 先创建 `.paper_...` staging 目录，再调用 `atomic_commit_tree` 复制到正式目录，但没有删除 staging 源目录。因此 `published_tasks/` 下会同时出现正式目录和隐藏的重复临时目录。

这是纯工程清理问题，不涉及科学裁决，但会污染发布树并增加存储和扫描成本。

### 2.8 Round 3 的科学审计仍漏掉通用的 workflow 一致性问题

复现任务对 TS 初始结构使用普通 `opt`，同时要求优化后具有一个虚频。Stage07 没有识别这一潜在冲突。

这不应通过加入 Gaussian、TS-1a 或具体关键词的死规则解决，而应增加通用的交叉检查要求：

```text
输入结构类型 → 计算动作 → 输出产物 → 验证标准 → Ground Truth 绑定
```

Stage07 必须逐步骤确认这条链是否科学一致。

## 3. 第四轮的目标架构

```text
Stage06A Scientific Builder
  选择科学目标、确认完整工作流、生成 reproduction draft、hidden draft、转换包
                         |
                         v
Stage06B Autonomous Surface Converter
  只根据转换包中和 reproduction public task 生成 autonomous public surface
                         |
                         v
Stage07 Audit-Repair Agent
  审计科学完整性、可复现性、边界条件、泄漏和 Evaluator 语义
  修复小问题；必要时重建工作流；由 Agent 决定 approved/rejected
                         |
                         v
Orchestrator mechanical prepublish gate
  只检查文件合同、mode/ID、manifest、Evaluator load 和发布目录
```

Stage06A 不再负责生成最终 autonomous 目录；Stage06B 是唯一负责 autonomous 公共表面转换的 Agent；Stage07 是最终科学审计者。

## 4. Canonical mode 合同

代码、Prompt、task 文件和 Evaluator 必须使用下面的唯一映射：

| 内容 | 论文复现模式 | 自主科研模式 |
|---|---|---|
| 发布目录 | `paper_reproduction/` | `autonomous_research/` |
| `mode` | `paper_reproduction` | `autonomous_research` |
| `scientific_mode` | `paper_reproduction` | `autonomous_research` |
| `task_mode` | `guided_reproduction` | `open_discovery` |
| task ID 后缀 | `_reproduction` | `_autonomous` |
| 方法公开 | `paper_route_disclosed` | `no_paper_method` |
| 路线公开 | `paper_route_disclosed` | `public_problem_only` |

`autonomous_research/` 是目录和科学模式名称；`open_discovery` 是 Evaluator 对自主任务执行模式的标准枚举。两者不能再互换。

由于当前 Round 3 任务直接提供 reference、candidate A、candidate B，它更准确地属于：

```json
{
  "autonomy_scope": "fixed_input_candidate_comparison"
}
```

这表示评估方法选择、工具调用、计算验证和结果分析能力，而不声称评估候选结构搜索或完全开放的问题拆解能力。该字段应作为公开任务元数据，但不改变 Evaluator 所需的 `task_mode=open_discovery`。

## 5. Stage06A 修改方案

### 5.1 Builder 的职责

Stage06A 只负责：

1. 从正文、SI 和解析证据中选择一个明确科学目标；
2. 选择整篇论文核心流程或最重要的完整核心子流程；
3. 判断输入、参数、计算步骤、Key Points、Ground Truth 和资源可行性；
4. 生成论文复现任务；
5. 生成 hidden reference draft；
6. 生成自主转换所需的结构化转换包；
7. 返回 provisional construction receipt。

Stage06A 不再生成或维护最终 autonomous public task。可以生成最小的 autonomous scaffold 作为文件布局占位，但不能把它视为 authoritative autonomous output。

### 5.2 Shared Objective、Public Scope、Private Claims 分层

Stage06A 输出应明确分成三层：

#### Shared Objective

两种模式都公开：

- 科学问题的中性描述；
- 公共输入文件；
- 必需实验观测和计算边界条件；
- 交付文件和结果字段；
- Key Point ID，不含答案。

#### Mode-specific Public Scope

论文复现模式可以公开：

- 作者软件；
- functional、basis、solvent model；
- 计算路线和依赖顺序；
- 路线执行所需的验证方法。

自主模式只公开：

- 公共科学目标；
- 输入结构和必要边界条件；
- 交付文件和输出字段；
- `autonomy_scope`。

两种模式的 public scope 都不得包含最终答案、答案排序、目标数值或“哪条路线更优”的表述。

#### Private Scientific Claims

只放在 hidden reference/evaluator registry：

- 数值 Ground Truth；
- 中间结论和最终结论；
- 目标排序和机制偏好；
- forbidden contradictions；
- 证据等级和私有 evidence map。

`workflow_scope.supported_primary_claims` 在 public task 中只能是 claim ID 或中性任务目标，不得写成包含答案的句子。

## 6. Stage06B 转换包设计

Stage06B 不需要接收完整论文全文，但必须收到一个比当前更清晰的最小转换包：

```text
inputs/conversion_packet/
├── public_objective.json
├── public_input_assets.json
├── route_redaction_map.json
├── preserve_boundary_conditions.json
├── asset_neutralization_map.json
├── key_point_ids.json
└── deliverable_contract.json
```

### 6.1 `public_objective.json`

只包含中性的 scientific question、scope、输入描述和 `autonomy_scope`。不得包含：

- PBE0、Gaussian、basis、solvent model 等作者方法；
- intramolecular/NH3-assisted 等作者路线标签，除非它们是明确的公共问题事实；
- canonical answers、ranking、5.1 kcal/mol 等答案信息。

### 6.2 `route_redaction_map.json`

由 Stage06A 生成，供 Stage06B 执行：

```json
{
  "files_to_remove": ["paper_route.md", "workflow_spec.json"],
  "fields_to_rewrite": ["scientific_mode_description", "input_assets[].description"],
  "tokens_to_remove": ["PBE0-D3BJ", "def2-SVP", "TS-1a"],
  "answer_bearing_phrases_to_remove": ["favored route", "5.1 kcal/mol"]
}
```

它是 Stage06B 的内部输入，不得复制到最终任务目录。

### 6.3 `preserve_boundary_conditions.json`

明确区分必须保留的公共事实和可删除的作者方法。例如：

```json
[
  {
    "name": "temperature",
    "value": "298.15 K",
    "classification": "public_boundary_condition",
    "reason": "needed to define thermochemistry"
  },
  {
    "name": "solvent",
    "value": "THF",
    "classification": "public_boundary_condition",
    "reason": "needed to define solution-phase energy"
  }
]
```

Stage06B 不得删除 `public_boundary_condition`；如果某字段分类不确定，应保留并标记 `needs_stage07_review`，不能自行猜测。

### 6.4 `key_point_ids.json`

只允许包含：

- Key Point ID；
- `claim_role`；
- `acceptance_type`；
- 输出 artifact/path 绑定。

不得包含：

- `canonical_answer`；
- `required_propositions`；
- `forbidden_contradictions`；
- 目标排序和数值。

这样 Stage06B 能保持输出结构一致，但不会接触 hidden answer。

### 6.5 Stage06B Prompt 修改

Prompt 必须明确三种动作：

- `remove`：按 redaction map 删除或改写作者路线和答案泄漏；
- `preserve`：保留 conversion packet 标记的公共输入和边界条件；
- `uncertain`：不做科学猜测，输出待 Stage07 审计的问题。

Stage06B 的输出状态增加“”：

- `converted`；
- `conversion_uncertain`：文件已生成，但存在明确的待审计项；
- `needs_conversion_retry`：API、workspace 或文件交付失败。

`conversion_uncertain` 不应被代码当作科学拒绝，而应进入 Stage07。

## 7. Stage07 修改方案

### 7.1 Agent 科学职责

Stage07 仍然拥有最终科学裁决权，优先级固定为：

1. 科学目标和工作流是否可执行；
2. 输入结构、计算动作、输出产物和验证标准是否一致；
3. 必要的公共边界条件是否保留；
4. 自主模式是否泄漏方法、路线、答案或候选语义；
5. Evaluator binding、Ground Truth 和 rubric 是否能实际评分；
6. 软件和资源是否可用。

Stage07 不要求覆盖整篇论文，但必须判断选择的目标是否支持论文主要科学 claim；如果 Stage06 选择的是完整但外围的子流程，应在同一审计中改为更重要的闭合子流程。

### 7.2 通用 workflow consistency 检查

Prompt 中增加统一表格化自检，但不写论文特例：

| 检查项 | 要回答的问题 |
|---|---|
| 输入类型 | 这是 minimum、transition state、reactant、product 还是普通候选结构？ |
| 计算动作 | 当前 optimization/frequency/single-point/MD 等动作是否适用于该输入？ |
| 输出产物 | 是否产生新的、可验证的科学产物？ |
| 验证标准 | 虚频、收敛、守恒、趋势或数值绑定是否与输入类型一致？ |
| Ground Truth | 中间结论和最终结论是否绑定到实际输出字段？ |

这可以发现 TS 普通优化之类的通用问题，但不添加 Gaussian 或特定论文关键词规则。

### 7.3 Stage07 结果合同

Agent 的科学决策字段保持不变：

- `approved`；
- `approved_with_repairs`；
- `approved_after_workflow_redesign`；
- `rejected_scientific_unrepairable`；
- `objective_failure_retryable`。

新增或规范：

- `mechanical_pre_publish_status`：由代码生成；
- `evaluator_dry_run_status`：由代码真实生成；
- `scientific_decision`：Agent 原样保留。

代码不得把 mechanical failure 改写成 `rejected_scientific_unrepairable`。

## 8. Stage07 Mechanical Prepublish Gate

不重新启用已经禁用的 `deterministic_stage07_audit()`，也不调用会产生广泛科学否决的旧 `validate_task_pair()` 作为 Stage07 科学裁决器。

新增一个窄范围的 `stage07_mechanical_pre_publish_check()`，只检查：

1. 两个 mode 目录存在且互相隔离；
2. mode、scientific_mode、task_mode、task ID 后缀符合 canonical contract；
3. JSON/Markdown/XYZ 文件可读；
4. required deliverables、submission contract 和相对路径安全；
5. reproduction 具有结构化 `paper_route_fidelity` rubric；
6. 两种模式共享 task pair ID、输入资产和 submission contract；
7. hidden reference 不在 public task 目录；
8. manifest hash 与文件内容一致；
9. evaluator registry 中的 task_info 和 ground truth 可以被真实加载；
10. published_tasks 下没有 staging、workspace、source 或 handoff 目录。

发现机械问题时：

- 可以将具体 findings 送入 Stage07 Agent 的 recovery/repair workspace；
- 或将任务标记为 `objective_failure_retryable`，等待重新交付；
- 不得把它解释为科学不可构建；
- 不得修改 Agent 已经给出的科学结论。

## 9. Evaluator Dry Run 接入

Stage07 发布前由代码执行最小真实加载测试：

1. 读取 reproduction/autonomous `task_info.json`，通过 `evaluation.schemas.task.TaskInfo`；
2. 读取 `task_spec.json`、submission contract 和 required deliverables；
3. 读取 evaluator registry 中对应 mode 的 private ground truth；
4. 校验 acceptance profile 的 artifact paths 和 JSONPath binding 指向存在的提交字段；
5. 确认两个 mode 都能建立 evaluator task record；
6. 将真实结果写入 `mechanical_pre_publish_report.json` 和 Stage07 记录中的 `evaluator_dry_run_status`。

Agent 返回的 `evaluator_dry_run_status` 只能作为建议字段，不能作为最终事实来源。

## 10. Complexity profile 统一

统一发布字段为：

```json
{
  "scientific_core_operation_count": 0,
  "estimated_min_tool_calls": 0,
  "estimated_typical_tool_calls": 0,
  "dependency_edge_count": 0,
  "parallel_branch_count": 0,
  "system_or_state_count": 0,
  "software_capability_count": 0,
  "iterative_decision_count": 0,
  "validation_operation_count": 0
}
```

兼容旧输入时只在读取阶段执行一次 alias normalization；最终 public task、audit record 和 evaluator registry 不再同时写入：

- `core_computation_count`；
- `tool_call_count`；
- `dependency_count`。

复杂度数字仍是 Agent 估计和审计元数据，不能被代码当作科学裁决的唯一依据。

## 11. Route fidelity rubric 统一

不再依赖自由文本关键词判断。reproduction `process_rubric.json` 至少包含一个结构化 criterion：

```json
{
  "id": "paper_route_fidelity",
  "criterion_type": "route_fidelity",
  "max_score": 15,
  "description": "Execute the disclosed paper route and preserve its method/dependency order.",
  "ground_truth_ids": [],
  "evidence_artifacts": ["report/process_trace.jsonl"]
}
```

该 criterion 评价过程执行，不泄漏最终答案。代码只检查它是否存在、分值是否纳入 100 分 rubric、证据 artifact 是否是 required deliverable；具体科学评分仍由 Evaluator/Agent 完成。

## 12. 发布清理

修复 `_publish_mode_bundles`：

1. 创建临时 staging 目录；
2. 原子提交到正式目录；
3. 成功后立即删除 staging 目录；
4. 失败时保留有限的内部失败证据，但不得留在 `published_tasks/`；
5. 发布后机械 gate 重新扫描，确保只存在正式 mode 目录。

该改动只影响文件清理，不影响 Agent 内容。

## 13. Prompt 精简和边界修正

### Stage06A

- 删除“生成最终 autonomous copy”的要求；
- 改为生成 `conversion_packet`；
- 明确 public scope 与 private claims 分层；
- 明确 reproduction 不得公开答案性 `supported_primary_claims`；
- 增加 workflow consistency 自检表。

### Stage06B

- 不再接收含 canonical answers 的原始 `key_points.json`；
- 不再接收含 PBE0/路线结论的完整 `objective_card.json`；
- 使用 conversion packet 的 remove/preserve/uncertain 三分法；
- 不重新选择 workflow；
- 不修改 hidden reference；
- 不把 `conversion_report.json` 放到最终任务目录；
- 输出简短转换报告和未解决披露清单。

### Stage07

- 增加结构化 workflow consistency 检查；
- 明确先修复 Stage06 选中的 workflow；
- 只有确认不可修复时才 redesign；
- 先科学可执行性，再泄漏，再合同和格式；
- 机械 gate 的结果由代码提供给 Agent，但不替代科学裁决。

## 14. 实施顺序

### 第一步：合同和字段统一

- 修改 mode/task_mode/task ID 生成和 normalizer；
- 修改 schema、bootstrap、Stage06/07 Prompt 和测试 fixture；
- 清理重复 complexity alias；
- 将 `autonomy_scope` 加入公开 task metadata。

### 第二步：Stage06A/Stage06B 边界重构

- 让 Builder 只生成 reproduction、hidden draft 和 conversion packet；
- 重写 `_setup_converter_inputs`，去除答案性 key points 和 scope claim；
- 增加 boundary condition、asset neutralization 和 route redaction 文件；
- 修改 Stage06B 输出合同。

### 第三步：Stage07 机械 prepublish gate

- 新增窄范围机械检查；
- 接入真实 Evaluator load dry run；
- 将结果写入代码生成的机械报告；
- 不恢复旧 deterministic scientific judge。

### 第四步：发布清理和 rubric

- 修复 staging 目录清理；
- 增加结构化 `paper_route_fidelity` criterion；
- 检查 public 任务目录只包含任务文件。

### 第五步：Prompt 和科学一致性验证

- 加入通用输入类型—计算动作—验证目标一致性检查；
- 不增加论文或软件特例；
- 通过 6904 回归测试后，再用至少一篇不同任务方向论文验证通用性。

## 15. 验收标准

### 协议

- autonomous `task_mode=open_discovery`；
- autonomous task ID 以 `_autonomous` 结尾；
- reproduction `task_mode=guided_reproduction`；
- reproduction task ID 以 `_reproduction` 结尾；
- 两种模式的 `mode`、`scientific_mode`、`task_mode` 不再混用。

### 信息隔离

- Stage06B 输入不含 canonical answers、forbidden contradictions 和最终结论；
- autonomous public task 不含作者方法、路线标签、source evidence ID 或答案数值；
- reproduction public scope 不含答案性 supported claims；
- 必要 solvent、temperature、pressure、charge、multiplicity 等边界条件不被误删。

### Evaluator

- `evaluator_dry_run_status` 由代码真实加载结果生成；
- 两种模式都能被 Evaluator schema 加载；
- acceptance profile 的 JSONPath 绑定指向实际提交字段；
- route fidelity criterion 存在且被纳入过程 rubric。

### 发布

- `published_tasks/` 只包含正式任务目录；
- 不存在 `.paper_...` staging 目录；
- 不包含 hidden reference、source materials、workspace、handoff 或 conversion report。

### 科学质量

- Stage07 能记录 workflow consistency 检查结果；
- 不用代码决定 scientific approved/rejected；
- 不要求覆盖整篇论文，但保留最重要、完整、可评分且具有计算挑战的目标。

## 16. 测试计划

1. 单元测试：mode/task ID、complexity canonical fields、route fidelity criterion、converter packet 脱敏、staging cleanup。
2. Evaluator load test：对两个 mode 分别加载 task info、task spec、submission contract 和 ground truth。
3. Stage06B artifact test：确认 packet 中不存在 `canonical_answer`、目标排序和答案性 claims。
4. Round 3 回归：使用同一论文确认 Stage07 仍能修复自主表面，且不再依赖 Stage07 补救 mode/ID 合同。
5. 通用性测试：至少增加一篇不同软件或不同任务方向的论文，防止 6904 特例化。
6. 轨迹指标：记录 Builder、Converter、Stage07 的工具调用和 token，确认 packet 缩小后没有重复扫描整个任务树。

## 17. 明确不做的事情

- 不加入 `PBE0`、`TS-1a`、`NH3` 等论文特定关键词规则；
- 不恢复代码侧科学裁决器；
- 不用固定“至少 N 步”判断任务是否有意义；
- 不让 Stage06B 重新设计科学 workflow；
- 不把 hidden Ground Truth 复制给 Stage06B；
- 不因为工具箱暂缺软件而自动科学拒绝；
- 不把 autonomous fixed-candidate comparison 宣传成完全开放的结构搜索 benchmark。

## 18. 预期结果

完成第四轮后，Stage06/07 应达到以下状态：

- Stage06A 负责科学工作流和 private reference，Stage06B 负责公共表面转换，职责不重叠；
- Stage06B 不需要完整论文全文，但拥有足够明确的 redaction/preserve 边界；
- Stage07 能修复科学和公开边界问题，而不是依赖代码静默覆盖；
- 编排器能真实证明任务可被 Evaluator 加载，但不代替 Agent 判断科学价值；
- 两种模式的文件合同、ID、评分绑定和发布目录形成闭合协议；
- 任务仍然围绕重要科学目标和完整计算子过程构建，不因机械规则退化为简单单步任务。

## 19. Round 4 实际实现记录

### Git commits

- `166897c fix(stage06-07): close round4 contracts and evaluator gate`
- `0b7415f fix(stage07): write gate failure record in active workspace`
- `60bbb70 fix(stage06-07): accept neutralized shared inputs and route rubric`
- `b547ccb fix(stage06): keep submission contract mode-neutral`

这些提交只包含本轮 Stage06/07、机械 gate 和专项测试文件；没有清理或覆盖工作区内其他用户改动。

### 已实现内容

1. 清理 Stage06A Prompt 的职责冲突：Builder 只生成 reproduction、hidden reference draft 和转换包，不再声称生成 authoritative autonomous task。
2. Stage06B 继续只接收最小 conversion packet，不接收 canonical answers、private evidence 或完整 Stage06A review。
3. Stage06 active path 在进入 Stage07 前统一 mode/task_mode/task ID、共享 submission contract，并将等价的 `route_fidelity` rubric 归一化为 `paper_route_fidelity`、`criterion_type=route_fidelity` 和 `evidence_artifacts`。
4. 新增 `stage07_mechanical_pre_publish_check()`：只检查文件合同、mode/ID、输入资产、route fidelity、隐藏目录隔离和 Evaluator 可加载性，不判断科学 approved/rejected。
5. Evaluator dry-run 通过项目真实 `TaskInfo`/`GroundTruth` Pydantic schema 加载两个 mode，并将结果写入 `mechanical_pre_publish_report.json`。
6. 输入一致性 gate 比较内容指纹；对 XYZ 仅忽略可脱敏的第二行 comment 和路径名，允许 autonomous 公共表面做中性重命名。
7. 修复 public bundle staging 源目录清理；Stage07 Prompt 加入通用“输入状态→计算动作→输出产物→验证→Ground Truth”一致性检查。
8. submission contract 保持 mode-neutral，仅保留共享 `task_pair_id` 和 required paths，不再把 reproduction 的 mode-specific `task_id`复制给 autonomous。

### 测试结果

```text
PYTHONPATH=. pytest -q tests/test_stage0607_agents.py tests/test_pipeline.py tests/test_batch_workflow.py
369 passed
```

新增/覆盖的专项测试包括 evaluator load gate、neutralized XYZ input matching、route rubric canonicalization 和 Stage06/07 mode 合同。

### 6904 Pro-0813 回归

运行目录：`runs/stage06-07-round4-20260818-paper6904-pro0813`。

- 论文：`paper_6904a9c8c09855cc`，DOI `10.1002/anie.202525581`。
- 模型：`deepseek-v4-pro-0813`；harness：Codex；API 参数来自 `config.local.env`。
- Stage06：`provisional_constructed`，选中第一 N–H tautomerization 的核心科学子流程；Builder 46 calls、约 2.40M tokens，Converter 25 calls、约 0.57M tokens。
- Stage07：最终 `approved_with_repairs`，`selected_workflow_preserved=true`，`toolbox_status=available`，`resource_status=feasible`，最终 mechanical gate 和 evaluator dry-run 均为 `passed`；最终成功尝试 37 calls、约 2.08M tokens（此前失败恢复尝试另有额外消耗）。
- 最终发布目录：
  - `stage_07_task_audit/published_tasks/paper_6904a9c8c09855cc_g70_first_nh3_tautomerization_paper_reproduction`
  - `stage_07_task_audit/published_tasks/paper_6904a9c8c09855cc_g70_first_nh3_tautomerization_autonomous_research`
- 发布目录没有 hidden reference、source materials、workspace、handoff、conversion report 或 staging 临时目录；私有 ground truth 只位于 `evaluator_registry/`。

### 运行轨迹中发现并修复的问题

1. 首次回归因 Stage07 gate 异常分支引用未定义变量 `workspace` 失败。修复为当前 Agent 工作区 `root`，提交 `0b7415f`。
2. 首次 gate 将 autonomous 中性 XYZ 文件名/comment 的差异误判为输入科学资产差异；改为内容指纹比较，提交 `60bbb70`。
3. Agent 输出了语义等价但字段名不同的 `route_fidelity` criterion。Stage06 active path 增加通用 rubric canonicalization，并由 gate 检查结构化字段。
4. Stage07 恢复尝试中曾把 mode-specific `task_id`带入共享 submission contract；改为删除该字段，提交 `b547ccb`。

上述失败均为文件合同/编排代码问题，不是模型科学判断；最终 Agent 仍保留了同一个重要科学子流程，并完成自主表面脱敏、rubric 调整和 hidden contract 同步。

### 后续建议

- 继续保留 mechanical gate，但只扩展通用文件和 Evaluator 合同，不加入论文/软件关键词规则。
- 将最终运行的 `mechanical_pre_publish_report.json`、两个 Agent 的 `agent_run.json`、`_bridge_trace.jsonl` 和发布 manifest 作为回归审计样本。
- 对不同任务方向增加 holdout 回归，重点观察 Agent 是否能主动选择重要核心子流程，以及 Stage07 是否能修复小问题而不是频繁触发机械恢复。

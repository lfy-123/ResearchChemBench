# Stage06/07 v16 最终任务合成、输入闭合与 Gate 修改方案

## 1. 目标

将合成 Agent 的工作定义为最终科学 benchmark task synthesizer。模型在一次工作流中完成科学目标选择、最小输入闭合、任务文件、评估文件和最终自查，不在 prompt 中暴露内部阶段编号、后续 Agent 或后续修复安排。

本轮不新增科学 Agent，不让代码统一理解或生成不同论文的化学输入，也不通过增加论文特例解决问题。代码只负责通用文件合同、适用格式的基本完整性验证、public/private 边界和 evaluator binding 检查。

最终任务必须满足：

- 科学目标明确、中心性有证据支持；
- 选定目标所需输入已经闭合；
- 任务输入文件存在且可读取；
- `task.md` 是完整、独立的任务说明；
- evaluator 五文件包含具体关键点、结论和可执行规则；
- public surface 不包含答案、隐藏评分或 private workflow metadata；
- Gate 只阻断必要文件、格式、引用和绑定问题；
- tolerance 的科学选择只产生诊断，不因格式细节过度阻断。

## 2. 模型职责和工作顺序

### 2.1 模型身份

模型身份使用“final scientific benchmark task synthesizer”。模型可见 prompt 不出现 `Stage06A`、`Stage06B`、`Stage07`、`later reviewer`、`final repairer`、`handoff` 或 `provisional` 等内部编排描述。

模型必须把当前输出视为最终任务包，不得把必需的科学、输入、evaluator、metadata 或文件合同工作留给其他 Agent。

### 2.2 选择科学目标

模型先选择一个最重要、闭合、资源可行的计算化学目标，并记录：

- scientific question；
- 目标覆盖的论文中心结论；
- 选定 workflow 和省略分支；
- 选择理由；
- 复杂度和资源评估。

在目标尚未确定前不生成最终 public task。

### 2.3 最小输入集合和输入闭合

目标确定后，模型只列出该 workflow 真正需要的最小输入集合，不扫描无关论文分支。每个输入需要记录：

- public path；
- 科学角色；
- 声明格式；
- source evidence IDs；
- 验证状态。

在生成任务前写入 `workflow_completeness_check.input_closure`（或等价的 `workflow_review.input_closure`），至少包含：

```json
{
  "status": "closed",
  "assets": [],
  "closed_fields": [],
  "unresolved_fields": []
}
```

模型必须根据论文证据完成以下任务级闭合：

- 结构、物种或周期模型身份；
- 原子数、组成和结构边界；
- 电荷和 multiplicity；
- 构象、过渡态、吸附位点或激发态身份；
- 溶剂、温度、压力、周期性等必要边界；
- 反应能的平衡参考和符号约定；
- 成对比较或集合比较所需的全部成员；
- 结果绑定所需的输入和计算步骤。

坐标、表格或结构抽取异常时，模型检查已有的 normalized、layout、table、derived-coordinate 和 coverage evidence，并进行当前论文特定的 source-backed 恢复。不得猜测缺失化学内容。

只有 `input_closure.status=closed` 且 `unresolved_fields=[]` 时才能生成成功任务。真正缺失且无法从证据恢复的 source-controlling science 才能科学拒绝；软件缺口记录为非阻断 readiness 信息。

### 2.4 生成最终任务

输入闭合后，模型一次生成：

```text
paper_reproduction/
autonomous_research/
evaluator_reference/
workflow_review.json
workflow_completeness_check.json
construction_receipt.json
```

`task.md` 是 evaluated Agent 的唯一任务说明，不能要求 evaluated Agent 读取 package-internal JSON 才能知道科学义务。

## 3. 任务文件结构

### 3.1 Public reproduction

```text
paper_reproduction/
  task.md
  task_info.json
  task_spec.json
  submission_contract.json
  process_rubric.json
  paper_route.md
  workflow_spec.json
  route_evidence_map.json
  data/inputs/*
```

### 3.2 Public autonomous

```text
autonomous_research/
  task.md
  task_info.json
  task_spec.json
  submission_contract.json
  process_rubric.json
  data/inputs/*
```

Autonomous surface 只保留问题定义所需的物理边界、公开方法约束、匿名输入和提交要求，不保留作者路线、内部标签、答案、参考值或 tolerance。

### 3.3 Private evaluator

```text
evaluator_reference/
  reference_key_points.json
  reference_conclusions.json
  scoring_rules.json
  evidence_map.json
  critical_failures.json
```

split evaluator 文件是权威来源。兼容性 `evaluation/reference.json` 只能是 projection，不得产生第二套 scoring 语义。

## 4. Evaluator 设计

### 4.1 Key points

`reference_key_points.json` 记录计算过程中的必要关键节点和中间结果，例如结构验证、频率验证、单体系能量、gap、barrier、中间排序和必要条件。

### 4.2 Conclusions

`reference_conclusions.json` 记录最终科学结论，例如路径偏好、结构稳定性、趋势、ordering 或机制结论，并关联 supporting key point IDs 和 evidence IDs。

### 4.3 Scoring rules

规则类型只使用：

```text
numeric
ordering
condition
semantic
```

每个 key point 和 conclusion 必须至少有一条规则。规则必须有 target/expected、binding、comparison；numeric 规则还必须有 unit 和 tolerance。规则必须能够从 `report/results.json` 或 `report/report.md` 中执行。

Agent 必须正常制定 tolerance。Gate 只检查规则是否完整、可引用、可绑定，不因为 tolerance 的科学取值、小数位、整数格式或文字风格阻断。

### 4.4 Process rubric

`process_rubric.json` 必须描述当前任务的具体过程检查点，不能只生成通用的 `workflow_execution`、`validation_and_analysis`、`paper_route_fidelity` 模板。它不替代 split evaluator，也不定义额外 score scale。

## 5. Public/private 边界

bootstrap 只能把以下白名单字段写入 public metadata：

```text
paper_id
task_id
category
benchmark_family
scientific_question
boundary_conditions
input_assets
required_deliverables
public method constraints
public task description
```

以下字段只能保留在 private review/evaluator：

```text
workflow_scope
supported_primary_claims
ground_truth_items
canonical_answer
acceptance_parameters
evidence_ids
private route metadata
```

删除所有默认 scaffold，例如 `Replace this scaffold with an evidence-backed task description.`。不添加第二种 paper identity；paper-level identity 统一使用 `paper_id`，只有 evaluator 内部保留 `key_point_id`、`conclusion_id` 和 `rule_id`。

## 6. 输入验证的职责边界

代码不负责统一理解或生成不同论文的科学输入。代码只对 Agent 已声明的最终资产做通用验证：

- 文件存在、非空、路径安全；
- JSON 可解析；
- 声明为 XYZ、CSV、TSV、CIF、POSCAR 等格式时进行基本语法读取；
- 输入绑定和提交绑定指向真实路径；
- 不自动推断缺失原子、构象、TS、吸附位点、周期模型或反应路径。

模型负责当前论文特定的输入角色识别、source-backed 恢复和科学闭合。Gate 负责发现不可读取的必要文件，但不猜测文件科学含义。

## 7. Gate 阻断边界

### 7.1 必须阻断

- 必要文件缺失或为空；
- JSON 无法解析；
- 声明格式无法读取；
- evaluator 文件为空或为纯模板；
- key point/conclusion 没有规则；
- rule 缺少 target/expected/binding；
- evidence ID 不存在；
- binding 指向不存在的结果字段；
- public 文件含有明显 private evaluator 字段；
- task instructions、submission contract 和 input assets 不一致；
- paper_id 不一致。

### 7.2 只生成 diagnostics

- tolerance 可能需要人工微调；
- tolerance 的整数/小数形式；
- prose 风格；
- 非关键 metadata 描述风格；
- compatibility projection 与 split evaluator 的非关键差异。

不添加 `human_review_required` 标签。Gate 通过后直接输出正常通过状态。

## 8. Internal conversion 和外部审查

内部 autonomous conversion 只做 answer-blind public transformation：删除作者路线、隐藏答案和内部标签，匿名化资产，保留问题定义所需物理边界和结果字段结构。它不重新选择科学目标、不猜测缺失输入、不重新生成 Ground Truth，也不触发语义 retry。

外部科学审查可以保留，但不出现在模型 prompt 中。它只独立检查科学代表性、真实 scientific blocker 和最终 public/private 边界，是安全兜底，不是合成 Agent 的默认修复流程。

## 9. 修改范围

预计修改：

1. `src/stages/stage06_task_builder/prompts.py`：改为最终合成 prompt，加入“先输入闭合、后任务生成”的工作流，删除内部阶段和后续修复描述。
2. `src/stages/stage06_task_builder/bootstrap_task_pair.py`：删除 private `workflow_scope` public 投影，删除 scaffold，使用 public 字段白名单。
3. `src/stages/phase_gate.py`：增加声明资产的通用格式检查、placeholder 检查、public/private 边界检查和 evaluator binding 检查；保持 tolerance 诊断策略。
4. `src/stages/stage06_task_builder/stage.py`：将输入闭合结果纳入合成合同，确保 selected workflow 的最小资产集合被记录和检查，不做论文特定科学推断。
5. `src/stages/evaluator_reference.py`：维持四种 rule type，统一 key point/conclusion/rule/binding coverage。
6. `tests/`：加入输入闭合、placeholder、private scope 泄露、损坏结构文件、evaluator coverage 和 tolerance 非阻断 fixture。

不修改 Stage00–05、chemistry toolbox、第一层 resume 或新增 retry/replay 机制。

## 10. 验收指标

定向回归和十篇论文测试中检查：

```text
input_closure false-positive rejection      0
placeholder                                 0
public answer leakage                       0
malformed required asset                    0
evaluator rule coverage missing             0
Stage06 self-check blocking findings        0
external mechanical Gate block              0
Stage07 transport repair                    尽量为 0
```

真正缺少 source-controlling science 的论文仍可科学拒绝，但必须与格式错误和可恢复 source extraction failure 区分。测试需同时比较 Stage06 原始输出、self-check 后输出和最终审查输出。

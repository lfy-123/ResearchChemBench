# Stage06-Stage07 Agent 化改造详细方案

> 版本：2026-08-13 修订版
> 状态：设计确认稿，尚未实施代码修改
> 适用范围：ResearchChemBench 数据管线 Stage06 任务构建与 Stage07 任务审计

## 1. 目标与已确认原则

Stage06 的目标不是把论文摘要改写成一道题，而是从论文正文和补充材料中恢复一个证据完整、可执行、可评分的计算化学工作流，并围绕同一个科学目标生成两种评估模式：

1. 自主科研模式：提供完成研究所需的输入、背景和边界条件，但不公开作者采用的计算路线。
2. 论文复现模式：在自主科研模式任务的基础上，增加论文采用的方法、步骤和路线，并修改任务指令为复现导向。

Stage07 使用 Agent 对 Stage06 产物做客观审计，不负责决定最终是否发布，也不自动修补任务。

本方案固定以下原则：

- Stage06 和 Stage07 的每次 Agent 调用都在独立工作区中运行。
- Agent 之间只通过经过校验的文件夹副本和结构化清单传递信息，不共享会话历史或可变工作目录。
- Stage06 使用同一套可配置 Agent 角色完成两种模式，但采用分阶段的新会话：先生成自主科研模式，再复制其文件夹并生成论文复现模式。
- 两种模式共享相同的科学目标、输入资产、Ground Truth 和结论验收规则。
- 两种模式唯一的实验变量是公开给被评估智能体的信息不同；过程 rubric 可以不同。
- Public Spec 与 Hidden Reference 必须由目录、权限和代码校验硬隔离，不能只依赖 prompt。
- 化学工具箱对 Stage06/07 Agent 只读。Agent 可以报告缺失能力和安装建议，不能修改工具箱。
- 工具箱暂缺不会导致 Stage06 淘汰论文，任务仍然生成并进入 Stage07 审计。
- Stage05 candidate 只是定位线索，不是 Stage06 必须遵从的约束。
- 论文来源、证据和许可信息单独保存，与两个任务目录同级，不放入任务目录。
- Stage07 只输出客观审计结果和证据，不引入额外发布语义。

## 2. 总体架构

```text
Stage05 approved paper/candidates
                |
                v
Stage06A Input Snapshot
  冻结论文、SI、Stage05、工具箱与资源约束
                |
                v
Stage06B Scientific Workflow Review
  全文审查、候选重选、完整性判断、公共/隐藏信息分类
       |                         |
       | 论文自身不可构建          | 基础设施故障
       v                         v
  scientific_reject       objective_failure_retryable
                |
                v
Stage06C Autonomous Task Builder
  独立工作区，只接收公共输入，不接收论文路线和隐藏答案
                |
                v
代码校验 + 冻结 autonomous_research/
                |
                v
复制 autonomous_research/ -> paper_reproduction/
                |
                v
Stage06D Reproduction Enricher
  新会话、独立工作区，在副本上增加论文方法路线并修改指令
                |
                v
Stage06E Hidden Reference Builder
  新会话、独立私有工作区，生成共同 Ground Truth 和 rubrics
                |
                v
Stage06F Pair Validation and Commit
  校验两模式同源、公开边界和文件完整性，原子提交
                |
                v
Stage07 Agent Audit
  独立只读工作区，审计任务对、隐藏参考、工具箱和成本
                |
                v
代码汇总客观 audit outcomes
```

“同一个 Agent”在这里指相同的 `agent_key`、harness、模型和系统能力配置，不是持续共享上下文的一个会话。每个科学阶段都启动新会话，避免自主模式在上下文中接触论文路线或 Ground Truth。

## 3. 工作区与文件传递

### 3.1 独立工作区

每个任务和阶段创建唯一工作区：

```text
workspaces/
  <paper_id>/
    stage06_review_<attempt_id>/
    stage06_autonomous_<attempt_id>/
    stage06_reproduction_<attempt_id>/
    stage06_hidden_reference_<attempt_id>/
    stage07_audit_<attempt_id>/
```

约束如下：

- 工作区之间不能使用指向其他工作区的软链接。
- Agent 只能写当前工作区中的指定输出目录。
- 论文原文、工具箱快照和已冻结产物以只读方式挂载或复制。
- 工作区中不能出现长期有效的 API 密钥、许可证文件或共享缓存凭据。
- 一次调用结束后生成 `output_manifest.json`，记录文件路径、大小和 SHA-256。
- 下游只接收清单中声明且通过 schema 校验的文件。

### 3.2 文件夹复制协议

Stage06C 完成后，编排器执行以下动作：

1. 校验自主科研模式目录。
2. 计算目录 manifest 和内容哈希。
3. 将整个自主科研模式目录复制到论文复现模式工作区。
4. 验证复制前后基础文件哈希相同。
5. 仅向 Stage06D 开放允许修改和新增的文件。

Stage06D 允许：

- 修改公开任务指令，使其明确要求按论文路线复现。
- 新增论文方法、计算路线、步骤依赖和参数说明。
- 新增复现模式专用过程 rubric。
- 更新模式标识和公开文件 manifest。

Stage06D 不允许：

- 修改输入结构、原始数据或公共背景事实。
- 修改科学目标、最终目标量或 Ground Truth 身份。
- 删除自主模式中完成任务所必需的输入。
- 把隐藏数值、结论或评分答案复制到公开目录。

编排器用 allowlist 和文件级差异检查执行这些约束，不能只让模型自报遵守。

### 3.3 原子提交

Agent 不能直接写正式结果目录。成功流程为：

1. 在临时工作区生成产物。
2. 执行 schema、manifest、路径、泄漏和跨模式一致性检查。
3. 全部通过后原子移动到正式 `stage_06_task_construction` 目录。
4. 任一步失败则保留诊断记录，不留下半成品正式任务。

## 4. Stage06 详细设计

### 4.1 Stage06A：Input Snapshot

代码先生成不可变输入快照，包含：

- 论文正文和全部已知 SI 的解析结果。
- MinerU、pypdf layout、表格、图片说明和坐标文件。
- Stage02/03/04 的分类、软件、方法、资源和证据。
- Stage05 的候选、审核维度和 evidence IDs。
- 化学工具箱能力快照。
- CPU、GPU、内存、墙钟时间、许可证等资源边界。
- 论文 DOI、题目、作者、期刊、年份和源文件哈希。

快照需要记录：

```json
{
  "snapshot_id": "...",
  "paper_id": "...",
  "created_at": "...",
  "source_manifest_hash": "...",
  "toolbox_snapshot_hash": "...",
  "resource_policy_hash": "...",
  "stage05_record_hash": "..."
}
```

后续重试必须引用同一个快照；输入发生变化时创建新快照和新 attempt，不能静默覆盖。

### 4.2 Stage06B：Scientific Workflow Review

该阶段允许 Agent 阅读论文正文、全部 SI、解析备用文本和 Stage05 记录。其职责是：

- 判断论文是否真的包含作者执行的完整计算化学过程。
- 检查必要输入、方法、参数、依赖关系、中间产物和结果证据。
- 判断该过程能否被转化为可执行且可评分的任务。
- 选择最适合构建 benchmark 的工作流。
- 将证据分类为公共输入、复现路线、隐藏答案或论文元数据。
- 报告工具箱能力差距，但不因暂缺工具直接淘汰。

#### Stage05 candidate 的处理

Stage05 candidate 只作为搜索入口。Stage06 Agent 可以：

- 修正 Stage05 对工作流边界的判断。
- 拆分或合并 candidate。
- 放弃 Stage05 candidate，选择论文中另一个更完整的工作流。
- 在证据支持时重新定义更适合评分的科学目标。

但每次偏离都必须输出：

- `stage05_candidate_disposition`；
- 被采用或放弃的原因；
- 新工作流的 evidence IDs；
- 完整性和可评分性对比。

#### 论文自身不可构建的淘汰条件

以下情况属于 `scientific_reject`，直接结束该论文的 Stage06 构建：

- 缺少完成目标所需的关键输入数据，且无法从正文或 SI 确定恢复。
- 计算过程不完整，关键步骤、依赖或参数无法确定。
- 工作流难以复现，不能形成可信的任务合同。
- 关键证据定位不完整，无法为输入、过程或 Ground Truth 建立可追溯依据。
- 论文只有计算结果描述，没有足够的作者执行过程。
- 无法形成可客观评分的中间目标或最终目标。
- 必要资源规模明显超出允许范围，且没有不改变科学问题的可行裁剪方式。

淘汰记录必须区分具体原因，不能只输出 `reject`。

#### 客观失败条件

以下情况不属于论文淘汰，标记为 `objective_failure_retryable`：

- Agent harness 启动失败或超时。
- 模型 API 掉线、限流或返回不可解析内容。
- 论文或 SI 的解析文件损坏、缺失或临时不可访问。
- 工作区复制、磁盘或 manifest 校验发生基础设施错误。

这类记录保留 `failure_class`、错误信息和重试条件，并进入统一重试队列。

#### 工具箱暂缺

工具箱缺少软件、版本、模块或 Action 时：

- 不淘汰论文。
- 不停止 Stage06 任务生成。
- 将缺失能力写入 `toolbox_requirements.json`。
- 标注当前能力为 `available`、`missing`、`unknown` 或 `incompatible`。
- 给出安装或扩展建议，但不执行修改。
- 在 Stage07 中继续独立审计。

### 4.3 公共信息与隐藏信息边界

Stage06B 输出两份互相隔离的清单。

#### 可以进入公共任务的信息

- 原始实验数据。
- 边界条件和作为计算输入的观测值。
- 完成计算必需的结构、坐标、组成、状态和环境信息。
- 不属于评分目标、但完成计算所必需的实验事实。
- 不泄露目标答案的背景知识、单位和数据格式说明。
- 资源约束和允许使用的工具范围。

#### 必须留在 Hidden Reference 的信息

- 被设为评分目标的作者计算结果。
- 被设为评分点的中间科学结论。
- 被设为评分点的最终实验或论文结论。
- 会直接泄露目标类别、排序、趋势或机理的解释。
- Ground Truth 的标准化答案、容差和判分逻辑。

作者对实验的解释和论文中的实验结论不是一律隐藏，而是按角色处理：

- 若它们是评估目标，则进入 Hidden Reference。
- 若它们不是评估目标且是完成任务必需背景，可以公开。
- 若公开后会使目标退化为抄写答案，则必须隐藏或更换评估目标。

任何事实不能同时以答案形式出现在公开任务和 Hidden Reference 中。代码需进行 evidence ID 交集、数值、规范化文本和语义泄漏检查。

### 4.4 Stage06C：自主科研模式生成

Stage06C 使用新会话和独立工作区。它只接收：

- Stage06B 生成的公共输入清单。
- 已复制的公共输入资产。
- 科学问题边界。
- 工具箱只读能力快照。
- 资源预算和任务格式规范。

它不能接收：

- 作者的实现路线。
- 论文中的目标结果和目标结论。
- Hidden Reference。
- Stage06B 的私有推理或包含答案的摘要。

自主科研任务应说明：

- 研究目标和需要回答的科学问题。
- 可使用的输入文件和每个文件的角色。
- 必须提交的计算产物、分析产物和结论。
- 资源、单位、精度和输出格式约束。
- 哪些方法选择由被评估智能体自主决定。

它不应说明：

- 论文采用的软件和固定路线，除非软件本身是任务不可避免的环境约束。
- 作者的步骤顺序、关键中间体选择或收敛策略。
- 作为评分答案的中间结论和最终结论。

建议公开目录至少包含：

```text
autonomous_research/
  task.md
  task_spec.json
  inputs/
  submission_contract.json
  public_manifest.json
```

### 4.5 Stage06D：论文复现模式生成

编排器先复制已冻结的 `autonomous_research/`，形成 `paper_reproduction/`。随后，同一个 `agent_key` 以新会话进入独立工作区，对副本做受限修改。

Stage06D 额外获得：

- 论文实际采用的方法、软件、参数和步骤依赖。
- 论文路线相关 evidence IDs。
- 允许修改的文件和字段清单。

论文复现任务在保留自主任务的科学目标、输入和提交合同基础上：

- 把任务指令改为按论文路线实施和复现。
- 增加作者采用的计算方法与关键参数。
- 增加工作流步骤、依赖关系和预期中间产物类型。
- 公开足以执行路线的信息，但仍不公开目标结果和目标结论。

建议新增：

```text
paper_reproduction/
  paper_route.md
  workflow_spec.json
  route_evidence_map.json
```

复制关系写入：

```json
{
  "derived_from_mode": "autonomous_research",
  "base_manifest_hash": "...",
  "allowed_differences": [
    "task_instructions",
    "paper_route",
    "workflow_spec",
    "process_rubric_reference"
  ]
}
```

### 4.6 Stage06E：共同 Hidden Reference

两种模式只生成一份共同的 Hidden Reference。它位于私有目录，不复制到任何公开任务目录。

Ground Truth 不限于数值，至少支持：

- 数值结果和单位。
- 结构或几何目标。
- 排序、类别和趋势。
- 中间关键结论。
- 最终计算结论。
- 与计算任务直接相关的实验结论或论文结论。
- 机理、选择性、稳定性或因果解释中的必要命题。

每个 Ground Truth item 都必须包含：

```json
{
  "ground_truth_id": "gt-001",
  "kind": "textual_intermediate_conclusion",
  "canonical_answer": "...",
  "required_propositions": [],
  "forbidden_contradictions": [],
  "acceptance_profile_id": "ap-001",
  "evidence_grade": "A",
  "evidence_ids": [],
  "applies_to_modes": [
    "autonomous_research",
    "paper_reproduction"
  ]
}
```

#### 证据等级

证据等级同时适用于数值和文字 Ground Truth：

- `A`：正文或 SI 中有直接、明确、可定位的结果或结论。
- `B`：可由论文给出的明确数据经过确定性转换得到。
- `C`：需要有限科学解释或跨证据组合，但证据链完整。
- `D`：依赖较强推断、图像估读或证据存在冲突。

默认规则：

- A/B 可以作为主要评分项。
- C 可以作为评分项，但必须记录推导规则并在 Stage07 重点审计。
- D 不应作为高权重确定性答案；通常需要降权、人工补证或淘汰该评分项。

### 4.7 Acceptance Profile 类型化

Acceptance Profile 是“什么样的被评估输出算正确”的机器可执行合同，而不是一句模糊的“与论文一致”。

支持的类型至少包括：

- `numeric_tolerance`：目标值、单位、绝对或相对容差、有效位数规则。
- `categorical`：标准类别、允许同义标签和拒绝标签。
- `ranking`：完整排序、允许并列和必须满足的成对关系。
- `trend`：变化方向、适用区间和允许例外。
- `structure_identity`：分子、构象、位点、键连或立体化学匹配规则。
- `geometry_metric`：键长、键角、二面角、RMSD 等结构阈值。
- `mechanism_claim`：必要物种、步骤、速控环节或因果关系。
- `semantic_propositions`：文字结论必须覆盖的命题和不得出现的矛盾命题。
- `artifact_validation`：输出文件、可解析性和必要字段要求。

示例：

```json
{
  "acceptance_profile_id": "ap-001",
  "type": "semantic_propositions",
  "required_propositions": [
    {
      "id": "p1",
      "statement": "...",
      "weight": 0.6
    },
    {
      "id": "p2",
      "statement": "...",
      "weight": 0.4
    }
  ],
  "forbidden_contradictions": [],
  "minimum_score": 0.8
}
```

同一个结论评分项在两种模式中引用同一个 Acceptance Profile。Stage06D 不得创建不同的结论容差或改写正确答案。

### 4.8 过程分与结论分

总评分分为两大部分：

- `process_score`：是否实施了具有科学意义的计算、检查和分析过程。
- `conclusion_score`：中间关键结论和最终结论是否正确。

两种模式的结论 rubric 必须相同；过程 rubric 可以不同。

自主科研模式的过程 rubric 可以评价：

- 是否选择了合理的方法和软件。
- 是否设计了必要的对照、构象、状态或收敛检查。
- 是否根据中间结果调整路线。
- 是否生成足以支持结论的证据链。

论文复现模式的过程 rubric 可以评价：

- 是否按公开的论文路线执行。
- 是否使用指定参数和步骤依赖。
- 是否生成路线规定的中间产物。
- 是否完成论文中必要的验证步骤。

过程项不能仅奖励启动软件、转换格式、读取数值、绘图或简单算术。每个高权重过程项必须对应真实科学产物或判断。

### 4.9 工具箱只读接入与建议

Agent 获得的是版本化的能力快照，而不是工具箱源码的写权限。快照至少描述：

- 软件名称、别名、版本和许可证状态。
- 是否已安装、是否可调用。
- 可用原生命令和已配置 Action。
- 已验证支持的关键功能。
- 通用前后处理能力。
- 已知限制和探针结果。

Stage06/07 Agent 可以：

- 检查任务需要的软件和功能。
- 判断现有能力是否足够。
- 提出缺失软件、版本、插件、参数文件、许可证或 Action 建议。

Agent 不可以：

- 安装、升级或删除软件。
- 修改工具箱配置、Action 或环境变量。
- 写入工具箱目录。
- 用未经授权的联网安装绕过限制。

建议输出：

```json
{
  "requirements": [
    {
      "requirement_id": "tool-001",
      "software": "...",
      "capability": "...",
      "status": "missing",
      "required_by_steps": ["s2"],
      "blocking_now": true,
      "suggested_action": "...",
      "evidence_ids": []
    }
  ]
}
```

`blocking_now=true` 表示当前工具箱不能立即执行，不表示论文或任务应被 Stage06 淘汰。

### 4.10 Stage06 论文级状态

建议使用以下互斥主状态：

- `constructed`：任务对和 Hidden Reference 已生成并通过代码校验。
- `scientific_reject`：论文自身证据或流程不满足构建要求。
- `objective_failure_retryable`：基础设施、Agent、模型或解析故障。
- `construction_invalid`：Agent 已生成，但产物未通过 schema、隔离或一致性检查，可重试或进入诊断。

同时记录非互斥标记：

- `toolbox_gap_present`；
- `high_cost_risk`；
- `evidence_grade_c_present`；
- `stage05_candidate_replaced`。

## 5. Stage07 详细设计

### 5.1 定位

Stage07 是只读审计阶段。它检查 Stage06 任务是否如实、完整、可执行和可评分，但不负责：

- 自动修改任务。
- 自动安装软件。
- 决定最终发布。
- 引入新的 benchmark 治理阶段。

### 5.2 输入

Stage07 工作区获得只读副本：

- `autonomous_research/`；
- `paper_reproduction/`；
- `hidden_reference/`；
- 同级的 `paper_info.json` 与证据索引；
- Stage06 manifests、日志和决策记录；
- Stage05 记录；
- 工具箱能力快照；
- 资源预算。

Stage07 Agent 需要具备查看私有参考的权限，但其输出中不得复述会泄漏答案的具体内容。公开版审计摘要和私有详细审计报告应分开保存。

### 5.3 审计内容

Stage07 至少检查：

1. 任务所需关键输入是否存在、可读且语义明确。
2. 计算工作流是否完整，步骤依赖是否成立。
3. 自主模式是否意外泄露论文路线或答案。
4. 论文复现模式是否确实来源于自主模式副本，且只增加允许的信息。
5. 两种模式的输入资产、科学目标和结论 Ground Truth 是否一致。
6. 过程 rubric 的差异是否合理。
7. 中间结论和最终结论是否都有证据和可执行 Acceptance Profile。
8. 论文信息、证据和来源是否可追溯。
9. 当前工具箱是否缺少必要软件或功能。
10. 资源成本是否明显过高或难以实际运行。
11. 是否存在关键数据、关键结论或证据定位缺失。

### 5.4 客观审计结果

Stage07 不用单个互斥标签压扁所有问题。推荐使用一个主结论加多项客观 outcome：

```json
{
  "audit_summary": "issues_found",
  "outcomes": [
    {
      "type": "needs_software",
      "severity": "blocking",
      "scope": "both_modes",
      "details": "...",
      "evidence_refs": []
    },
    {
      "type": "task_missing_data",
      "severity": "blocking",
      "scope": "autonomous_research",
      "details": "...",
      "evidence_refs": []
    }
  ]
}
```

`audit_summary` 只允许：

- `passed_audit`：没有发现影响完整性、执行或评分的问题。
- `issues_found`：发现一个或多个客观问题。
- `audit_failed_retryable`：Stage07 自身因 Agent、模型、文件或基础设施问题未完成。

首版 outcome 类型至少包括：

- `needs_software`：当前工具箱缺少软件、功能、版本、许可证或依赖。
- `task_missing_data`：缺少关键输入、结构、参数、边界条件或数据文件。
- `task_missing_ground_truth`：缺少关键中间结论、最终结论、标准答案或证据。
- `workflow_incomplete`：计算步骤、依赖或必要分析不完整。
- `task_cost_too_high`：成本或资源需求明显过高，难以实现。
- `acceptance_rule_invalid`：判分规则不明确、不可执行或与 Ground Truth 不一致。
- `mode_isolation_violation`：自主模式泄漏路线/答案，或两种模式出现不允许的串联。
- `mode_pair_inconsistent`：两种模式的科学目标、输入或结论基准不一致。
- `provenance_incomplete`：论文、证据、版本或来源信息无法追溯。
- `toolbox_capability_unknown`：现有快照不足以确认功能支持，需要后续检查。

一个任务可以同时具有多个 outcome，例如同时 `needs_software` 和 `task_cost_too_high`。后续筛选阶段可以根据这些客观结果自行制定策略，Stage07 不替它做决定。

### 5.5 Stage07 不自动修复

Stage07 可以给出 `recommended_actions`，例如补充哪个文件、安装什么软件或重新生成哪个字段，但不能直接修改 Stage06 产物。修复应由后续显式流程发起，并产生新的 Stage06 revision 和新的 Stage07 audit。

## 6. 正式产物目录

建议每个任务对使用如下结构：

```text
stage_06_task_construction/
  tasks/
    <paper_id>/
      paper_info.json
      evidence_index.json
      source_manifest.json
      construction_record.json
      toolbox_requirements.json
      autonomous_research/
        task.md
        task_spec.json
        inputs/
        submission_contract.json
        public_manifest.json
      paper_reproduction/
        task.md
        task_spec.json
        inputs/
        submission_contract.json
        public_manifest.json
        paper_route.md
        workflow_spec.json
        route_evidence_map.json
      hidden_reference/
        ground_truth.json
        acceptance_profiles.json
        process_rubric_autonomous.json
        process_rubric_reproduction.json
        conclusion_rubric.json
        private_evidence_map.json
        hidden_manifest.json
```

这里 `paper_info.json`、`evidence_index.json` 和 `source_manifest.json` 与两个任务目录同级，明确不放进任一模式目录。

Stage07 建议输出：

```text
stage_07_task_audit/
  audits/
    <paper_id>/
      audit_summary.json
      public_audit_report.md
      private_audit_details.json
      toolbox_gap_report.json
      cost_risk_report.json
      audit_manifest.json
```

## 7. 论文信息与追溯

`paper_info.json` 至少记录：

- 内部 paper ID。
- DOI、题目、作者、期刊和年份。
- 正文及每份 SI 的来源 URI。
- 原始文件哈希与解析版本。
- 各 Stage 输入记录和版本。
- 任务所采用的工作流及证据索引。
- Stage05 candidate 被采用、修改或替换的记录。
- 许可证、访问条件和允许发布范围。
- Stage06/07 使用的 harness、模型、prompt、配置和运行时间。

论文信息留在内部同级文件中。未来生成公开数据集时，由独立发布流程决定哪些字段可以公开。

## 8. Agent Harness 可替换设计

### 8.1 统一接口

Stage06/07 业务代码不直接绑定 Codex、Claude Code 或 OpenCode。定义统一适配器：

```python
class AgentHarness:
    def run(
        self,
        *,
        workspace: Path,
        instruction_file: Path,
        input_manifest: Path,
        output_contract: Path,
        timeout_seconds: int,
        environment_policy: dict,
    ) -> AgentRunResult:
        ...
```

`AgentRunResult` 至少包含：

- `status`；
- `exit_code`；
- `session_id`；
- `stdout_path`；
- `stderr_path`；
- `usage`；
- `output_manifest_path`；
- `failure_class`；
- `retryable`。

### 8.2 配置示例

```yaml
stage06:
  agent_key: codex_stage06
  harness: codex
  model: configurable
  workspace_root: workspaces/stage06
  toolbox_access: read_only
  network_access: disabled
  max_attempts: 3

stage07:
  agent_key: claude_stage07
  harness: claude
  model: configurable
  workspace_root: workspaces/stage07
  toolbox_access: read_only
  network_access: disabled
  max_attempts: 3
```

适配器首版建议支持：

- `codex`；
- `claude`；
- `opencode`；
- 一个用于测试的 `mock` harness。

型号、命令、超时和环境变量全部放在配置层，不写死在业务代码中。

### 8.3 权限策略

每个 harness 都必须遵守相同策略：

- 当前工作区可写。
- 输入快照、工具箱和已冻结上游产物只读。
- 正式输出目录不可直接写。
- 默认禁止联网；确需联网时使用显式白名单和审计日志。
- 不允许跨任务读取其他论文的工作区。
- 不允许访问 Hidden Reference 的阶段不能通过路径猜测读取它。

## 9. 状态机、重试与 Resume

每个 paper/phase 使用显式状态：

- `pending`；
- `running`；
- `succeeded`；
- `scientific_reject`；
- `failed_retryable`；
- `failed_terminal`；
- `invalid_output`。

Resume 依据不是“目录存在”，而是同时满足：

- 成功 marker 存在。
- 输出 schema 有效。
- manifest 哈希匹配。
- 输入快照、Agent 配置和 prompt 版本未变化。
- 下游需要的文件完整。

模型掉线和 Agent 超时采用指数退避重试。解析输入缺失应等待上游恢复后重试。科学淘汰不自动重试，除非论文/SI、工具箱策略或构建规则发生版本变化。

建议保存：

```text
state/
  stage06_<paper_id>.json
  stage07_<paper_id>.json
attempts/
  <paper_id>/<phase>/<attempt_id>/run_record.json
```

## 10. 代码校验器

模型输出之后至少运行以下确定性校验：

### 10.1 Schema 校验

- 所有必填字段存在。
- enum、ID、单位和路径类型合法。
- 引用的 evidence ID、Ground Truth ID 和 Acceptance Profile ID 存在。

### 10.2 文件与 manifest 校验

- 文件不存在越界路径或软链接逃逸。
- manifest 中的大小和哈希一致。
- 两种模式的输入资产内容一致。
- 论文复现目录确实派生自自主目录。

### 10.3 隐藏答案泄漏校验

- 公共目录不能引用 hidden 文件路径或 hidden IDs。
- 公共文本不能出现目标数值的精确或单位变体。
- 公共文本不能直接出现被隐藏的标准结论。
- 自主模式不能出现论文路线专有步骤和参数。

语义检查可由独立审计模型辅助，但数值、ID、路径和规范化文本检查必须由代码执行。

### 10.4 跨模式一致性校验

- 科学问题 ID 相同。
- 输入资产哈希相同。
- 结论 rubric 和 Acceptance Profile 引用相同。
- Ground Truth 集合相同。
- 仅过程 rubric、公开路线和任务说明允许不同。

### 10.5 科学可评分性校验

- 至少一个真实计算步骤产生新的科学产物。
- 至少一个中间或最终 Ground Truth 可评分。
- 每个评分项有证据、类型化 Acceptance Profile 和权重。
- 结论总权重和过程总权重满足配置规范。
- 评分项没有要求被评估智能体读取论文隐藏答案。

## 11. 成本处理

Stage06 可以基于论文规模、体系大小、方法层级和历史数据给出成本风险。模型估计需要标记来源：

- `model_estimated`；
- `historically_calibrated`；
- `probe_confirmed`。

Stage06 只在成本明显不可实现且无法合理裁剪时作 `scientific_reject`。工具箱缺少某软件不等同于成本过高。

Stage07 客观报告：

- 预计 CPU/GPU、内存、磁盘和墙钟时间。
- 估计依据和不确定性。
- 是否明显超过当前资源政策。
- 是否存在不改变科学目标的缩减方案。

Stage07 不需要执行完整 gold run，也不需要决定最终发布。

## 12. 失败分类

统一错误分类建议：

| 类别 | 示例 | Stage06 行为 | Stage07 表达 |
| --- | --- | --- | --- |
| `scientific_missing_input` | 缺关键结构或实验输入 | 淘汰 | `task_missing_data` |
| `scientific_incomplete_workflow` | 关键计算步骤或参数缺失 | 淘汰 | `workflow_incomplete` |
| `scientific_missing_ground_truth` | 无关键结果或结论证据 | 淘汰 | `task_missing_ground_truth` |
| `scientific_unreproducible` | 证据不足以恢复流程 | 淘汰 | 对应事实问题 |
| `toolbox_missing` | 软件或功能未安装 | 继续构建并记录 | `needs_software` |
| `toolbox_unknown` | 能力快照不能确认支持 | 继续构建并记录 | `toolbox_capability_unknown` |
| `resource_infeasible` | 明显超出资源且不可裁剪 | 淘汰 | `task_cost_too_high` |
| `agent_or_model_failure` | API 掉线、超时 | 可重试失败 | `audit_failed_retryable` |
| `source_parse_failure` | 正文/SI 无法读取 | 可重试失败 | `audit_failed_retryable` |
| `invalid_generated_artifact` | schema 或隔离校验失败 | 重试/诊断 | 对应 outcome |

## 13. 实施顺序

### 第一阶段：合同与目录

1. 定义 Stage06/07 JSON Schema。
2. 定义正式任务对目录和私有目录。
3. 实现 evidence、manifest、hash 和 snapshot 工具。
4. 实现公共/隐藏路径权限策略。

### 第二阶段：Harness 与工作区

1. 定义 `AgentHarness` 接口。
2. 实现 Codex 适配器和 mock 适配器。
3. 再实现 Claude/OpenCode 适配器。
4. 实现独立工作区、只读挂载、超时、日志和重试。

### 第三阶段：Stage06

1. 实现 Input Snapshot。
2. 实现 Scientific Workflow Review。
3. 实现公共/隐藏证据分流。
4. 实现自主任务生成。
5. 实现冻结、复制和论文复现增补。
6. 实现共同 Hidden Reference 和 rubrics。
7. 实现 pair validator 与原子提交。

### 第四阶段：Stage07

1. 实现只读审计工作区。
2. 实现客观 outcome schema。
3. 实现公开摘要和私有详情分离。
4. 实现论文级汇总和 resume。

### 第五阶段：回归验证

建议先选少量覆盖不同软件、任务方向和失败类型的论文，验证：

- 自主模式没有路线或答案泄漏。
- 复现模式确实由自主目录复制产生。
- 两种模式输入和结论评分一致。
- 文字 Ground Truth 可被类型化评分。
- 工具箱缺失不会误淘汰。
- 模型掉线可以 resume/retry。
- Stage07 能同时报告多个客观问题。
- 不同 harness 的结果都满足同一输出合同。

## 14. 验收标准

实现完成需要满足：

- 每次 Agent 调用有独立工作区、输入清单和输出 manifest。
- 自主模式先生成并冻结，复现模式由其完整副本派生。
- 两种模式由同一个配置化 Agent 角色完成，但不共享会话上下文。
- Public Spec 与 Hidden Reference 在物理目录和访问权限上隔离。
- 论文信息文件位于两个模式目录的同级位置。
- 两种模式共享 Ground Truth、结论 rubric 和 Acceptance Profiles。
- 中间文字结论和最终文字结论都能作为 Ground Truth。
- 过程 rubric 允许按模式不同。
- 工具箱全程只读，缺失能力被记录但不导致任务淘汰。
- Stage05 candidate 可以被 Stage06 有证据地替换。
- 论文自身不完整与 Agent/模型/解析故障使用不同状态。
- Stage07 只输出客观审计结论和问题，不自动修复或决定发布。
- resume 能识别每个 paper/phase 的真实完成状态。

## 15. 当前无待确认边界

基于截至 2026-08-13 的讨论，本方案实施所需的产品边界已经明确。实现时可以把下列内容作为配置默认值，而无需改变上述语义：

- 每阶段最大 Agent 调用次数和超时时间。
- 首个默认 harness 和模型。
- 过程分与结论分的具体权重。
- Acceptance Profile 的默认容差模板。
- Stage07 各 outcome 的 severity 默认映射。
- 工作区保留天数和日志压缩策略。

这些属于运行参数和标定问题，可以在小规模回归实验中调整，不构成架构层面的待确认事项。

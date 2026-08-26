# Stage06/07 v19 release、双模式任务语义与代码修改方案

## 1. 目标

本方案统一处理 Stage06/07 的双模式科学语义、任务指令、evaluator 边界、输出文件
组织、可见性、发布、安装和对应代码修改计划。

目标是：

1. 将运行证据、人工审计母版和可发布任务包分开；
2. 在 `runs/<run_id>/release/` 生成统一、易检查的发布候选；
3. 使用唯一 `paper_id` 关联论文、论文复现任务和自主科研任务；
4. 从目录层面隔离 Agent 输入和 evaluator 私有文件；
5. 人工确认后，将 release 安装到 benchmark 的 `papers/` 和 `tasks/`；
6. 不把 workspace、checkpoint、Agent 脚本或构建记录复制进正式 benchmark。

Stage06 的双模式合成采用一次连续 Agent 调用，但不是同时铺开两套模板。Agent 必须先
完成完整的 `paper_reproduction` 任务、输入、submission schema 和 evaluator，运行单模式
self-check 并修复到通过；之后才以该稳定基线为副本，语义派生完整
`autonomous_research`，最后运行双模式 self-check。派生必须审查整个公开合同和 evaluator，
不能只改 `task.md`。原 Stage06B 的转换职责合并到这一次调用中，不恢复独立 converter、
conversion retry、receipt 或 uncertain 状态。

`construction_receipt.json` 是该调用的终止合同，只能最后写入：构建成功时必须晚于两次
self-check；科学不可构建时必须晚于完整的 evidence-backed `workflow_review.json`。Prompt
必须明确 receipt 的必填字段 `decision`、`paper_id`、`artifact_path`、`summary`，避免模型
写出无效 receipt 后被 `required_until_artifact` 执行协议持续要求无意义工具调用。

## 2. 三层数据边界

### 2.1 运行与审计层

原始执行信息继续保存在：

```text
runs/<run_id>/
├── run_summary.json
├── papers/
│   └── <paper_id>/
│       ├── stage_06_task_construction/
│       └── stage_07_task_audit/
└── release/
```

`papers/<paper_id>/stage_06_task_construction/` 和
`stage_07_task_audit/` 保留 Agent workspace、checkpoints、phase artifacts、Gate
报告、构建记录和完整审计母版。这些文件只用于追踪、调试和科学审计，
不是 benchmark 任务文件。

### 2.2 Release candidate 层

批次完成后统一生成：

```text
runs/<run_id>/release/
├── release_manifest.json
├── papers/
│   └── <paper_id>/
└── tasks/
    ├── autonomous_research/
    │   └── <paper_id>/
    └── paper_reproduction/
        └── <paper_id>/
```

release 只包含科学批准、机械检查通过且完整组装的任务。科学拒绝、技术阻断和机械
阻断只保留在运行摘要和阶段记录中，不进入 release。

### 2.3 正式 benchmark 层

人工确认后安装到：

```text
ResearchChemBench/
├── papers/
│   └── <paper_id>/
└── tasks/
    ├── autonomous_research/
    │   └── <paper_id>/
    ├── paper_reproduction/
    │   └── <paper_id>/
    └── experiment_validation/
        └── <paper_id>/
```

release 应保留在原 run 中作为来源记录。正式安装采用校验后的原子复制，不移动或
删除原 release。

## 3. 论文库结构

每篇论文在一个共享目录中只保存一次：

```text
papers/<paper_id>/
├── paper_info.json
└── documents/
    ├── main.pdf
    ├── supplementary_001.pdf
    ├── supplementary_002.pdf
    └── ...
```

正文统一命名为 `main.pdf`，补充材料按稳定顺序命名为
`supplementary_NNN.pdf`。原始文件名、文档类型、来源和 SHA-256 写入
`paper_info.json`，不依赖复杂的出版社文件名表达身份。

`paper_info.json` 的最小结构为：

```json
{
  "paper_id": "paper_2aca1dd116799b28",
  "title": "...",
  "doi": "...",
  "journal": "...",
  "publication_date": "YYYY-MM-DD",
  "publication_year": 2025,
  "authors": ["..."],
  "documents": [
    {
      "document_type": "main_article",
      "path": "documents/main.pdf",
      "original_filename": "...",
      "sha256": "..."
    },
    {
      "document_type": "supplementary_information",
      "path": "documents/supplementary_001.pdf",
      "original_filename": "...",
      "sha256": "..."
    }
  ]
}
```

论文正文和 SI 只属于合成、审计和人工策展资源，**不得属于任何模式的被评测
Agent 输入**。该规则同时适用于 `autonomous_research` 和 `paper_reproduction`。
论文文件不能因为与任务位于同一 release 中而被 runner 自动暴露；论文复现模式
所需的计算路线必须由合成阶段提取并完整写入 `task.md`，不能要求被评测 Agent
自行阅读论文。

## 4. 单个最终任务包结构

每个模式的最终包使用相同外壳：

```text
tasks/<task_type>/<paper_id>/
├── agent_input/
│   ├── task.md
│   ├── submission_schema.json
│   └── data/
│       └── inputs/
├── task_info.json
├── evaluation/
│   ├── reference_key_points.json
│   ├── reference_conclusions.json
│   ├── scoring_rules.json
│   ├── evidence_map.json
│   └── critical_failures.json
└── package_manifest.json
```

### 4.1 `agent_input/`

该目录是被评测 Agent 的完整可见面。runner 只将其**内容**物化到 Agent workspace
根目录：

```text
agent_input/task.md                 -> workspace/task.md
agent_input/submission_schema.json  -> workspace/submission_schema.json
agent_input/data/                   -> workspace/data/
```

runner 不得挂载整个任务包，也不得依靠 prompt 告诉 Agent 不要查看 evaluator。

### 4.2 `task_info.json`

该文件供 benchmark repository、调度和展示使用，不物化给被评测 Agent。删除
`task_id`、`task_family_id`、`source_id` 等重复身份，使用 `paper_id + task_type`
定位任务。

建议结构：

```json
{
  "paper_id": "paper_2aca1dd116799b28",
  "task_type": "autonomous_research",
  "title": "...",
  "category": "...",
  "paper": {
    "title": "...",
    "doi": "...",
    "journal": "...",
    "publication_date": "YYYY-MM-DD"
  },
  "data": [
    {"path": "data/inputs", "description": "..."}
  ],
  "required_deliverables": [
    {"path": "report/results.json", "description": "..."}
  ]
}
```

删除字段：

- `schema_version`；
- `task_id`；
- `task_family_id`；
- `source_id`；
- 空 `tags`；
- `runtime_readiness`；
- `related_task_ids`；
- `reference_schema`。

任务中的简要论文信息由 release assembler 从共享 `paper_info.json` 投影，禁止两种
模式分别人工填写而产生漂移。完整作者和文档清单只保存在共享论文目录。

### 4.3 `evaluation/`

该目录仅供 evaluator 和人工审计使用，永不进入 Agent workspace。五个文件保持
拆分设计：

- `reference_key_points.json`：参考关键计算节点；
- `reference_conclusions.json`：参考最终科学结论；
- `scoring_rules.json`：规则类型、目标、单位、容差、比较和提交绑定；
- `evidence_map.json`：参考内容与论文证据的关系；
- `critical_failures.json`：整体任务严重失败条件。

两种模式各自保留完整 evaluation，使任务包可独立安装、验证和评分。文件较小，
不为了去重引入跨包运行时依赖。

### 4.4 `package_manifest.json`

manifest 位于包根目录，不暴露给 Agent。它记录 `paper_id`、`task_type`、包格式、
内容哈希、`agent_input_root` 和所有文件的路径/大小/SHA-256/可见性。

最小示意：

```json
{
  "paper_id": "paper_2aca1dd116799b28",
  "task_type": "autonomous_research",
  "package_format": 1,
  "agent_input_root": "agent_input",
  "package_content_sha256": "...",
  "entries": [
    {
      "path": "agent_input/task.md",
      "sha256": "...",
      "visibility": "agent"
    },
    {
      "path": "evaluation/scoring_rules.json",
      "sha256": "...",
      "visibility": "evaluator"
    }
  ]
}
```

可见范围采用固定目录边界：只有 `agent_input/` 能进入 Agent workspace。manifest
负责验证而不能动态扩大 Agent 权限。

## 5. 唯一身份与 repository 索引

一篇论文只保留一个持久化身份：`paper_id`。三种正式任务类型通过目录和 `task_type`
区分，
repository 使用 `(task_type, paper_id)` 作为索引键：

```python
load_task(paper_id="paper_2aca1dd116799b28", task_type="autonomous_research")
```

不得为了适配索引重新创建 mode-specific task ID。日志需要单字符串时可以临时显示
`paper_id [task_type]`，但不写入新的持久化身份字段。

## 6. Release assembler

批次结束后由单一 release assembler：

1. 读取各 paper 的终态记录，只选择 publish-ready 任务；
2. 确认两个模式均存在且来自同一 `paper_id`；
3. 从可信 source snapshot 复制正文和全部 SI，每篇只复制一次；
4. 生成共享 `paper_info.json`；
5. 将最终任务指令、提交 schema 和输入组织到 `agent_input/`；
6. 将五个 evaluator 文件组织到 `evaluation/`；
7. 生成精简 `task_info.json`；
8. 生成 `package_manifest.json` 和内容哈希；
9. 检查两种模式的公开输入是否符合共同科学核心和各自 task kind；默认使用相同
   问题定义输入，任何差异必须经过 Stage07 科学审计，不能由 assembler 猜测或修正；
10. 确认论文 PDF、evaluation、内部证据和构建记录不在 `agent_input/`；
11. 分别验证两个任务包，并确认 pair 完整；
12. 生成 `release_manifest.json`；
13. 在私有 staging 目录完成全部检查后，原子提交到
    `runs/<run_id>/release/`。

任何一个模式失败都不得留下半个 release pair。assembler 不从 Agent prose 推断路径，
只读取 Stage07 声明的已批准 artifact。

## 7. `release_manifest.json`

release manifest 只记录 release 来源、论文和任务包：

```json
{
  "release_id": "stage0607-v19-202608xx",
  "source_run_id": "stage0607-v19-202608xx",
  "papers": [
    {
      "paper_id": "paper_2aca1dd116799b28",
      "path": "papers/paper_2aca1dd116799b28"
    }
  ],
  "tasks": [
    {
      "paper_id": "paper_2aca1dd116799b28",
      "task_type": "autonomous_research",
      "path": "tasks/autonomous_research/paper_2aca1dd116799b28",
      "package_sha256": "..."
    },
    {
      "paper_id": "paper_2aca1dd116799b28",
      "task_type": "paper_reproduction",
      "path": "tasks/paper_reproduction/paper_2aca1dd116799b28",
      "package_sha256": "..."
    }
  ]
}
```

不增加 `human_review_required` 等逐任务标签；release 与正式 benchmark 的目录边界
已经表达其策展状态。

## 8. 人工确认后的安装

人工确认后，将 release 原子复制到正式仓库：

```text
release/papers/<paper_id>/
  -> ResearchChemBench/papers/<paper_id>/

release/tasks/<task_type>/<paper_id>/
  -> ResearchChemBench/tasks/<task_type>/<paper_id>/
```

安装规则：

1. 目标不存在时复制；
2. 目标存在且哈希完全一致时跳过；
3. 目标存在但哈希不一致时停止，禁止静默覆盖；
4. 安装后验证所有 paper/task 关联、包哈希和 `(task_type, paper_id)` 唯一性；
5. 保留原 release，不通过移动或删除破坏运行来源。

## 9. 不进入 release 的内容

以下内容只保留在 runs 内部审计层：

- `workspaces/`、`checkpoints/`、`phase_artifacts/`；
- Agent stdout/stderr、session 和工具轨迹；
- `build_stage06a.py`、`finalize_stage06a.py`、`repair_evaluator.py`；
- construction/handoff/audit 的详细内部记录；
- 大型 `evidence_index.json`；
- Gate 中间报告和缓存文件；
- 科学拒绝、技术阻断和机械阻断的半成品树。

release 只提供论文库、两个完整任务包和 release manifest。

## 10. 已确认的双模式基本原则

本版本同时确认任务指令和科学语义边界：

1. 两种模式的被评测 Agent 都不能看到论文正文、补充材料、evaluation、证据索引或
   Stage06/07 工作记录；
2. 两种模式从同一个科学目标出发，使用相同的问题本体和物理边界；
3. `autonomous_research` 由被评测 Agent 自行选择并论证计算路线；
4. `paper_reproduction` 由 `task.md` 完整披露论文采用的计算路线，但不披露论文结果；
5. 任务必须自包含，不能出现“按论文方法”“与论文报告值比较”等需要读取不可见
   论文才能执行的义务；
6. 路线信息可以公开给 reproduction，参考数值、参考排序、机制结论和 evaluator
   tolerance 不能公开给任一模式；
7. 两种模式在同一次 Agent 调用中顺序生成：先完整生成并自查 reproduction，再复制其
   共同科学问题和公开输入作为 autonomous 的起点；转换必须重写任务路线并同步审查
   schema、输入表面和 evaluator，不能只做关键词删除；
8. 任务是 discovery 还是 validation 由实际公开输入决定，不能由标题或 prompt
   随意声称。

## 11. 科学核心与双模式生成模型

### 11.1 模式无关的科学核心

Stage06 在写任何公开任务前，先在私有审计区形成一个紧凑的科学核心：

```text
scientific_objective
task_kind
public_inputs
physical_boundaries
requested_scientific_results
required_deliverables
```

各字段含义如下：

- `scientific_objective`：需要解决的科学问题，不包含论文答案；
- `task_kind`：`discovery`、`validation`、`comparison` 或其他准确描述任务性质的类型；
- `public_inputs`：被评测 Agent 实际能够读取的输入及其科学角色；
- `physical_boundaries`：电荷、自旋、相态、溶剂、温度、周期边界等定义问题所必需的
  条件；
- `requested_scientific_results`：要得到哪些结构、能量、性质、路径验证或科学结论；
- `required_deliverables`：需要提交的文件和结构化字段。

这些是问题定义，不是论文路线。共同科学核心不能包含作者软件、route string、作者
搜索步骤、参考结果、参考排序、机制答案、tolerance 或私有 evidence ID。

### 11.2 论文路线

Stage06 另在私有审计区形成 `paper_route`，记录：

- 软件和计算方法；
- 泛函、基组、赝势、力场或溶剂模型；
- 初始状态、计算顺序和步骤依赖；
- 结构优化、过渡态搜索、采样或模拟路线；
- frequency、IRC、收敛性和其他验证方法；
- 后处理和电子结构分析；
- 允许的来源支持范围和无法确定的路线细节。

`paper_route` 只用于生成 reproduction 指令和私有审计，不作为独立公开文件交给
被评测 Agent，也不能包含最终参考答案。

### 11.3 两种模式的生成关系

```text
autonomous_research
    = 共同科学核心
    + 方法和科研路线由 Agent 自主选择并说明理由

paper_reproduction
    = 共同科学核心
    + 从论文提取并在 task.md 中完整展开的 paper_route
    + 偏离路线必须报告
```

两种模式默认使用同一组问题定义输入。若公开输入包含作者最终目标结构，例如明确的
过渡态结构，则两个模式都只能定义成候选结构验证任务。若目标是自主发现过渡态，
则两个模式的 Agent 输入都不得包含作者最终过渡态；作者过渡态只保留在 evaluator
私有参考中。

不允许为了强行产生一个 discovery 任务而删除科学执行所必需的输入。如果论文路线
在不公开答案结构的前提下无法执行，应选择诚实的 validation 目标，或者判定该
discovery scope 不可构建。

## 12. 两种模式的 `task.md` 完整结构

两种模式统一使用四段外壳：

```text
Scientific objective
Public inputs and scientific boundaries
Required work / computational route
Deliverables
```

共同部分必须写清楚科学目标、输入、条件、结果类型和交付物。差异只放在第三部分：

- autonomous 写必须获得的科学证据，但不规定实现方法；
- reproduction 写完整的论文计算路线，但不写参考结果。

### 12.1 已通过任务样例

样例来自已科学批准的 `paper_2aca1dd116799b28`，科学目标是比较六个 Bergman 环化
体系的过渡态、反应能垒以及影响过渡态稳定性的几何和电子因素。现有任务公开了作者
过渡态，因此按 v19 的 discovery 定义，需要把六个作者过渡态从 `agent_input/`
移到 evaluator 私有侧，两种模式只公开六组反应物和产物。

### 12.2 Autonomous 指令样例

```markdown
# Comparative transition-state study of six Bergman cyclizations

## Scientific objective

For each of the six supplied reactant-product pairs, locate and validate a
transition state connecting the reactant and product.

Use the resulting stationary points and reaction paths to determine the
electronic activation barrier of each system and identify which geometric and
electronic factors account for differences in transition-state stabilization
across the series.

## Public inputs and scientific boundaries

The directory `data/inputs/` contains the reactant and product structures for
systems `a` through `f`:

- `system_a_reactant.xyz` and `system_a_product.xyz`
- `system_b_reactant.xyz` and `system_b_product.xyz`
- `system_c_reactant.xyz` and `system_c_product.xyz`
- `system_d_reactant.xyz` and `system_d_product.xyz`
- `system_e_reactant.xyz` and `system_e_product.xyz`
- `system_f_reactant.xyz` and `system_f_product.xyz`

All systems are neutral singlets and should be studied in the gas phase. Atom
indices are one-based and follow the XYZ row order after the two-line header.

## Required scientific results

For every system:

1. Locate a candidate transition state connecting the supplied reactant and
   product.
2. Demonstrate that the reactant and product are minima and that the candidate
   transition state is a first-order saddle point.
3. Verify that the transition state connects the intended reactant and product
   basins using an appropriate reaction-path analysis.
4. Report the reactant and transition-state electronic energies and the
   electronic activation barrier in kcal/mol.
5. Report the relevant forming-bond distance in the reactant and transition
   state.
6. Perform an appropriate electronic-structure analysis and use it, together
   with the geometric and energetic results, to explain differences across the
   six systems.

Select and justify the computational method, transition-state search strategy,
reaction-path validation procedure and electronic analysis. Do not assume that
one geometric descriptor alone determines the result.

## Deliverables

Submit:

- `report/results.json`, following `submission_schema.json`;
- `report/methods.md`, describing all methods, software, settings and
  convergence controls;
- `report/validation.md`, documenting frequency analysis, reaction-path
  connectivity, optimization status and important limitations;
- optimized transition-state structures under `report/structures/`.
```

该模式不能在 `task.md`、`submission_schema.json`、公开文件名、XYZ comment 或其他
Agent 可见元数据中出现 B3LYP、Gaussian、QST3、NBO、作者最终数值、作者机制结论
或作者过渡态结构，除非某个方法本身就是经明确审计的问题定义，而不是论文路线。

### 12.3 Paper reproduction 指令样例

```markdown
# Reproduction of a six-system Bergman-cyclization transition-state study

## Scientific objective

For each of the six supplied reactant-product pairs, locate and validate a
transition state connecting the reactant and product.

Reproduce the computational route specified below, calculate the electronic
activation barriers, and determine which geometric and electronic factors
account for differences in transition-state stabilization across the series.

## Public inputs and scientific boundaries

The directory `data/inputs/` contains the reactant and product structures for
systems `a` through `f`:

- `system_a_reactant.xyz` and `system_a_product.xyz`
- `system_b_reactant.xyz` and `system_b_product.xyz`
- `system_c_reactant.xyz` and `system_c_product.xyz`
- `system_d_reactant.xyz` and `system_d_product.xyz`
- `system_e_reactant.xyz` and `system_e_product.xyz`
- `system_f_reactant.xyz` and `system_f_product.xyz`

All systems are neutral singlets and should be studied in the gas phase. Atom
indices are one-based and follow the XYZ row order after the two-line header.

## Computational route to reproduce

Use the following computational route:

1. Optimize the reactant and product structures with RB3LYP/6-31G(d,p).
2. Construct a chemically plausible transition-state guess for each pair and
   locate the transition state using an unrestricted UB3LYP/6-31G(d,p)
   transition-state search compatible with a QST3 workflow.
3. Perform harmonic frequency calculations. Reactants and products must have
   zero imaginary frequencies, and each transition state must have exactly one
   reaction-coordinate imaginary frequency.
4. Run forward and reverse IRC calculations at UB3LYP/6-31G(d,p). Extend the
   reaction path sufficiently to reach both endpoint basins, and verify the
   endpoint identities by optimization and connectivity comparison.
5. Calculate the electronic activation energy as
   `E(transition state) - E(reactant)` and report it in kcal/mol.
6. Measure the C17-C32 distance in each reactant and transition state.
7. Perform NBO charge and second-order perturbation analyses at
   B3LYP/6-31G(d,p). Report charges at C15, C16, C17 and C32, together with the
   transition-state interaction corresponding to
   `BD*(1) C15-C16 / BD*(1) C17-C32`.
8. Compare all six systems and determine which geometric and electronic
   descriptors explain differences in transition-state stabilization.

If a specified step cannot be reproduced exactly, document the failure and any
scientifically justified substitution. Do not replace the specified route
silently.

## Deliverables

Submit:

- `report/results.json`, following `submission_schema.json`;
- `report/methods.md`, documenting the executed route, software, keywords,
  settings and deviations;
- `report/validation.md`, documenting frequency analysis, IRC connectivity,
  convergence and limitations;
- optimized transition-state structures under `report/structures/`.
```

reproduction 可以公开方法和路线，但仍不能公开六个体系的参考能垒、参考几何参数、
NBO 参考数值、相对排序、机制答案或 evaluator tolerance。

## 13. Submission schema 与 evaluator 的模式差异

两种模式共享核心科学结果，但不强制使用完全相同的结构化字段。强制相同会把论文
路线通过 schema 泄漏给 autonomous。

例如本样例中：

- 两种模式都可要求驻点类型、路径连通性、能垒、结构和科学结论；
- reproduction 可要求固定的 NBO charge 和 E(2) 字段；
- autonomous 应允许报告其选择的电子分析方法、描述符和支持证据，不应在 schema
  中隐式强制 NBO；
- autonomous 的评分重点是驻点真实性、路径连通性、结果内部一致性、合理的定量
  结果和科学论证；
- reproduction 可以对论文方法下的数值和论文路线执行程度采用更具体的比较。

因此 Stage06 私有审计树中的 evaluator 建议直接按模式拆分：

```text
evaluator_reference/
├── autonomous_research/
│   ├── reference_key_points.json
│   ├── reference_conclusions.json
│   ├── scoring_rules.json
│   ├── evidence_map.json
│   └── critical_failures.json
└── paper_reproduction/
    ├── reference_key_points.json
    ├── reference_conclusions.json
    ├── scoring_rules.json
    ├── evidence_map.json
    └── critical_failures.json
```

最终 release 中每个任务包仍只包含自身的五个 evaluation 文件，不引入跨包依赖。

Agent 必须生成完整、具体、可执行的 evaluator：关键点、结论、规则、提交字段和证据
关系不能是空模板。Gate 负责检查文件完整性、引用闭合、规则类型所需字段和提交绑定
是否可用，但不判断某个 tolerance 的具体科学选择是否最优，也不因为 tolerance 是
整数、小数或某种等价表示而阻断。

## 14. Stage06/07 职责调整

### 14.1 Stage06：一次完成最终任务合成

Stage06 的 Agent 被描述为最终科学评估任务合成者，不在 prompt 中说明自己位于
“Stage06”或后续还有哪个 Agent。它在同一次调用、同一上下文和同一 workspace 中按
以下顺序完成任务：

1. 阅读论文和 SI，选择一个核心且封闭的科学目标；
2. 判断任务是 discovery、validation、comparison 还是其他准确类型；
3. 检查完成该目标所需的公开输入是否闭合；
4. 形成共同科学核心和独立 paper route；
5. 先集中完成 paper reproduction：任务指令、submission schema、公开输入和完整
   evaluator；
6. 对 reproduction 单模式运行共享自查，修复全部阻断问题，形成稳定基线；
7. 在同一次调用中复制该基线作为 autonomous 起点，保留共同科学目标、问题边界和
   合理公开输入，重写计算路线为由被评测 Agent 自主选择；
8. 同步调整 autonomous 的 task、task_info、submission schema、文件名/内容和
   evaluator。论文方法专属字段或评分规则只有在仍是问题定义时才能保留；
9. 检查 autonomous 所有 Agent 可见面，包括 task、schema、输入文件名、输入内容和
   comment，清除论文路线和答案泄漏；
10. 对完整双模式候选运行与外部 Gate 使用同一实现的最终自查，修复阻断问题后再结束。

这里的“复制”是同一 Agent 为保持科学目标和输入一致而使用的工作步骤，不是恢复旧的
独立 converter。Agent 不能只修改 `task.md` 或按关键词删除文本；它必须根据模式语义
审查整个公开面，并允许两种模式采用合理不同的 submission schema 和 evaluator。

prompt 只强调自查是完成任务的必要工作，不增加“编排器强制检查是否执行自查”的
额外协议。外部 Gate 始终重新检查实际最终文件，不依赖 Agent 声称自己通过自查。
Agent 自查报告与外部 Gate 报告使用不同文件名，互不覆盖。

### 14.2 Stage07：审计和有限修复

Stage07 只接收 Stage06 已构建的完整候选。它可以看到论文、SI、Stage06 私有科学
核心、paper route、两个任务模式和 evaluator，因为 Stage07 Agent 是数据管线内部
审计者，不是被 benchmark 评测的 Agent。

Stage07 负责：

- 判断科学目标是否核心、合理、闭合且可评估；
- 检查 task kind 与公开输入是否相符；
- 检查两种模式是否保持同一个科学问题；
- 检查 autonomous 整个公开面是否泄漏论文路线或答案；
- 检查 reproduction 是否完整、自包含地披露论文路线；
- 检查任务是否引用被评测 Agent 看不到的论文或数值；
- 检查 task、schema、输入、evaluator 和交付物是否一致；
- 对来源明确的小范围文件问题做证据支持的有限修复。

Stage07 不从 Stage06 科学失败或缺失任务中重建新任务。科学目标错误、输入不闭合、
任务类型根本错误或候选无法在有限修复内恢复时，直接拒绝。Stage07 通过后才调用
确定性 release assembler。

## 15. Gate 阻断边界

### 15.1 必须阻断

- 必需任务文件或 evaluation 文件缺失；
- JSON 无法解析、路径越界、manifest/hash 不一致；
- 本管线生成的 `autonomous_research` 或 `paper_reproduction` 的 `agent_input/` 中出现
  论文 PDF、evaluation、私有证据或构建记录；
- task 引用了没有公开提供的论文、SI、实验值或内部文件；
- task、公开输入、submission schema 和交付物合同不一致；
- evaluator 为空模板、缺少关键点或结论、规则未覆盖参考项、提交绑定不存在；
- 两种模式使用错误的 `paper_id` 或目录身份；
- Stage07 科学审计未批准，或者 release pair 只完成一个模式。

### 15.2 只记录诊断、不机械阻断

- tolerance 的具体科学宽严是否最优；
- tolerance 使用整数还是小数；
- 等价的单位或规则文字风格；
- Agent 选择的科学表述是否符合某种固定关键词；
- 需要人工进一步调整的评分权重或细节。

Gate 不通过全局方法关键词黑名单来判断 autonomous 泄漏。Stage06 应记录该论文真实的
paper route，Stage07 对所有公开表面做语义审计；机械 Gate 只验证明确的可见性、文件
和合同事实，避免继续堆积论文特例和方法名死规则。

## 16. 代码修改计划

本节是已经确认并用于实施的代码边界；实际完成项、测试结果和逐条一致性复核记录在
`STAGE06_07_V19_IMPLEMENTATION_PLAN_AND_LOG.md`。

### 16.1 第一步：建立修改基线

1. 记录当前 Stage06/07 定向测试结果和五篇已通过任务的文件快照；
2. 只纳入 v19 相关文件，保留工作区中 Stage00-05 和 chemistry toolbox 的既有修改；
3. 建立按“合同与运行时、Stage06、Gate、Stage07/release、测试”拆分的 Git 提交；
4. 不保留旧字段或旧模式别名的兼容投影，新实现直接以 v19 合同为准。

### 16.2 第二步：修改 Task Package 公共合同和 benchmark runtime

修改：

- 将 `researchchembench_contracts/task_package.py` 迁移为
  `evaluation/contracts/task_package.py`，随后删除原顶层合同包；
- 新建 `evaluation/contracts/__init__.py`；
- `evaluation/repository.py`；
- `evaluation/execution/workspace.py`；
- `evaluation/execution/runner.py`；
- 必要的 CLI、scoring、web 和对应测试。

目标：

1. 将 Task Package 顶层合同改成 v19 的 `agent_input/ + task_info.json +
   evaluation/ + package_manifest.json`；
2. `task_info.json` 只保留 `paper_id`、`task_type`、title/category、论文简要信息、数据
   描述和交付物，不再要求 `schema_version/task_id/task_family_id/source_id/tags/
   runtime_readiness/related_task_ids/reference_schema`；
3. `submission_schema.json` 位于 `agent_input/`，身份字段如确有必要只使用
   `paper_id`，不得重新引入 task ID；
4. `package_manifest.json` 使用 `paper_id`、`task_type`、`package_format`、
   `agent_input_root`、内容哈希和固定 visibility；
5. repository 使用 `(task_type, paper_id)` 建立索引，并正式支持
   `autonomous_research`、`paper_reproduction` 和 `experiment_validation`；API 和
   runner 显式接收这两个参数，不依赖全局唯一 mode-specific task ID；
6. runner 只把 `agent_input/` 的内容复制到 workspace 根目录，绝不根据宽泛 allowlist
   挂载包根目录；
7. evaluator 只能通过 evaluator context 读取 `evaluation/`；
8. 删除 v19 路径上的 legacy adapter、mode aliases 和旧 ID 投影，不生成兼容字段。

### 16.3 第三步：重写 Stage06 双模式合成流程

修改：

- `src/stages/stage06_task_builder/prompts.py`；
- `src/stages/stage06_task_builder/stage.py`；
- `src/stages/stage06_task_builder/validation.py`；
- `src/stages/stage06_task_builder/bootstrap_task_pair.py`；
- `src/config.py` 及 Stage06 配置测试。

具体修改：

1. 将 builder prompt 改成第 14.1 节的最终合成职责和工作顺序；
2. 在 prompt 中写入第 12 节的统一任务结构和 disclosure 边界；
3. 要求 Agent 先完成 input closure 和 task-kind 判断，再生成任务；
4. 同一个 synthesis Agent 先完整生成并自查 reproduction，再在同一调用中从其稳定
   基线派生 autonomous；派生过程必须基于共同科学核心做全公开面语义改写，不是独立
   Agent 的关键词 redaction；
5. 删除 `autonomous_converter_instructions`、converter harness、converter receipt、
   conversion retry/uncertain 状态、conversion audit 和相关配置；
6. 删除 `_setup_converter_inputs`、`_converter_*`、`_write_conversion_audit` 等只服务于
   Stage06B 转换链的代码；
7. `bootstrap_task_pair.py` 不再生成带占位符的科学内容或 evaluator 骨架。若直接写出
   最终文件后该脚本不再有机械价值，则删除脚本和调用；
8. Stage06 私有候选中保存共同科学核心、paper route、输入闭合记录、reproduction
   单模式自查结果和两个模式各自的
   evaluator；
9. 取消“两模式输入哈希必须完全相等”和“submission schema 形状必须相同”等不合理
   约束，改由 Stage07 审计问题一致性和输入科学角色；
10. Stage06 返回值只记录一次合成结果和一次最终合同状态，不再出现 Stage06A/06B
    conversion 状态组合。

### 16.4 第四步：统一 Agent 自查和外部 Gate

修改：

- `src/stages/phase_gate.py`；
- `src/stages/evaluator_reference.py`；
- `src/stages/stage06_task_builder/validation.py`；
- `src/stages/stage07_task_judge/validation.py`；
- Stage06/07 workspace 中复制的 Gate helper。

具体修改：

1. 只保留一个 v19 evaluator/任务合同检查实现；
2. Agent 自查脚本和外部 Gate 直接调用同一个函数，不再维护两套相似规则；
3. 删除 v13/v15/v16 兼容分支、acceptance profile 旧投影、mode alias 和旧目录探测；
4. evaluator 检查循环覆盖两个模式各自的五个文件；
5. 阻断项严格限制为第 15.1 节，tolerance 科学选择进入 diagnostics；
6. 检查 `agent_input/` 与私有目录的物理隔离，以及 task/schema/deliverable/binding 闭合；
7. 自查报告写 `agent_self_check_report.json`，外部报告写
   `external_phase_gate_report.json`，禁止相互覆盖；
8. prompt 要求 Agent 修复自查发现，但 orchestrator 不把“是否留下自查报告”设计成
   一层新的成功标签；外部 Gate 始终以实际文件为准。

### 16.5 第五步：收敛 Stage07 为审计与有限修复

修改：

- `src/stages/stage07_task_judge/prompts.py`；
- `src/stages/stage07_task_judge/stage.py`；
- `src/stages/stage07_task_judge/validation.py`。

具体修改：

1. prompt 使用第 14.2 节职责，不提后续阶段，不暗示可以重新构建任务；
2. Stage07 只接收 Stage06 完整候选，不为缺失/科学失败候选准备 fallback source；
3. 删除 `_prepare_stage07_fallback_source` 以及任何重建任务的残留分支；
4. 增加明确的语义审计清单：task kind、输入角色、两模式目标一致、autonomous
   路线/答案泄漏、reproduction 路线完整、自包含、schema/evaluator 对齐；
5. 允许来源明确的局部修复；改变科学目标、重新选择工作流或从零生成 evaluator 时
   必须拒绝；
6. Stage07 输出只使用 approved、approved_with_repairs、
   rejected_scientific_unrepairable 和 technical_blocked 等当前必要状态，不增加
   `human_review_required`；
7. 审计通过后对最终 audited snapshot 运行统一 Gate，再进入 release assembly。

### 16.6 第六步：实现 v19 release assembler

修改：

- `src/stages/stage07_task_judge/package.py`；
- `src/stages/stage07_task_judge/stage.py`；
- `src/late_stage_runner.py` 和正常 pipeline 的 Stage07 批次收尾逻辑；
- 共享 manifest/hash 校验代码。

具体修改：

1. 将现有 `final_tasks/` 发布改成 `runs/<run_id>/release/`；
2. 每篇批准论文原子生成：
   `release/papers/<paper_id>/`、
   `release/tasks/autonomous_research/<paper_id>/` 和
   `release/tasks/paper_reproduction/<paper_id>/`；
3. 论文正文和 SI 每篇只复制一次到 `release/papers/`，不得复制到任何
   `agent_input/`；
4. 从 Stage07 审计树复制真实 `task.md`、schema、公开输入和对应模式 evaluation，
   不在 assembler 中推断或改写科学内容；
5. assembler 只生成精简 `task_info.json`、package manifest、paper metadata 和 hash；
6. 两个模式或论文目录任一失败时不提交半个 release pair；
7. Stage07 全批次完成后统一生成 `release_manifest.json`，避免并发任务竞争写同一
   manifest；
8. 删除 `_normalize_required_deliverables` 等旧兼容投影和基于 task ID 的组装逻辑；
9. release 保持不可变，人工确认后的 installer 只执行第 8 节的校验复制。

### 16.7 第七步：测试与回归验证

更新或新增：

- `tests/test_stage0607_v19_task_semantics.py`；
- `tests/test_stage0607_v19_unified_gate.py`；
- `tests/test_stage0607_v19_release.py`；
- repository、runner、scoring 和 Task Package 合同测试。

固定 fixture 至少包括：

1. discovery：只公开反应物/产物，作者目标结构仅在 evaluation；
2. validation：公开候选结构，task 明确要求验证而不是发现；
3. reproduction：公开论文路线但不公开参考结果；
4. autonomous：不公开路线，schema 也不泄漏方法特定字段；
5. 任务错误引用不可见论文或 PDF 时被阻断；
6. evaluation 空模板、缺规则或 binding 不存在时被阻断；
7. tolerance 取值或等价格式不会触发机械阻断；
8. runner workspace 中只有 task、submission schema 和 data；
9. repository 可同时索引同一 `paper_id` 的两个模式；
10. release 不包含 workspace、checkpoint、Gate 中间报告和构建脚本。

定向单元测试通过后，对此前成功合成的论文做同样本回归，至少重点复核：

- `paper_2aca1dd116799b28`：过渡态 discovery/validation 是否与公开输入一致；
- `paper_9455a82229de2427`：不再要求读取不可见论文中的实验值，autonomous 不再泄漏
  Gaussian/CBS-QB3；
- 其余已通过任务：两种模式文件完整、科学目标合理、evaluator 具体可执行、release
  隔离正确。

## 17. 实施完成后的方案一致性复核

代码完成后逐条对照本文件，至少确认：

1. Stage06 不再有独立的 reproduction-to-autonomous converter Agent；派生在同一个
   synthesis Agent 调用中完成；
2. 两种模式都不能看到论文 PDF、SI 或 evaluation；
3. reproduction 先从共同科学核心完整生成并自查；autonomous 从同一稳定科学基线
   派生且经过全公开面审查；
4. task kind 与实际公开输入一致；
5. evaluator 按模式完整生成，规则不是空模板；
6. 自查和外部 Gate 使用同一合同实现，报告不覆盖；
7. Stage07 只审计和有限修复，不重建；
8. release 采用 `papers/ + tasks/<task_type>/<paper_id>/`；
9. 唯一论文身份是 `paper_id`，评估内部 ID 仅限 key point、rule 和 conclusion；
10. runtime 只物化 `agent_input/`；
11. 没有遗留 mode alias、旧 ID 投影或旧 package 兼容分支；
12. 定向测试、同样本回归和最终输出人工抽查均通过。

## 18. Benchmark 侧完整适配方案

当前顶层 `researchchembench_contracts/` 实际只有 `task_package.py` 和导出用的
`__init__.py`，其内容只服务于 benchmark Task Package 和运行时验证。它不应作为一个
看似独立、实际只有单一用途的顶层包继续存在。v19 推荐由 benchmark 的 `evaluation`
模块直接拥有该合同。

### 18.1 合同代码归位

推荐迁移为：

```text
evaluation/
└── contracts/
    ├── __init__.py
    └── task_package.py
```

实施内容：

1. 将 `researchchembench_contracts/task_package.py` 的 v19 有效合同迁入
   `evaluation/contracts/task_package.py`；
2. 只保留 v19 的 `paper_id + task_type + agent_input` 合同，删除旧 Task Package v1
   模型和兼容校验；
3. benchmark 内部统一从 `evaluation.contracts` 导入；
4. data pipeline 的 release assembler 也从 `evaluation.contracts` 导入，不复制第二套
   package schema；
5. 删除顶层 `researchchembench_contracts/` 源码目录及 `pyproject.toml` 中对应 package
   include；
6. 不把合同放进 data pipeline，因为最终任务格式由 benchmark runtime 消费和拥有，
   data pipeline 是该格式的生产者。

### 18.2 Repository 身份和目录发现

修改 `evaluation/repository.py`：

1. `TaskPackage` 只保存 `paper_id`、`task_type`、目录、category 和 package hash；
2. repository 只从以下标准目录发现任务：

   ```text
   tasks/autonomous_research/<paper_id>/
   tasks/paper_reproduction/<paper_id>/
   tasks/experiment_validation/<paper_id>/
   ```

3. 内部索引直接使用 Python tuple `(task_type, paper_id)`；
4. 对外 API 显式接收两个参数，例如：

   ```python
   load_task(paper_id="paper_2aca1dd116799b28", task_type="autonomous_research")
   ```

5. 删除 `DuplicateTaskIdError` 和全局 `task_id` 唯一逻辑，替换为同一
   `(task_type, paper_id)` 目录重复检查；
6. 不创建 `TaskKey ID`、mode suffix 或拼接后持久化的复合 ID；tuple 只是代码索引，
   不是新身份字段；
7. `list_tasks()` 返回包含 `paper_id` 和 `task_type` 的记录，不再返回一组含义不完整
   的 ID 字符串。

`paper_id + task_type` 的职责是：

- `paper_id` 标识唯一来源论文，并关联共享论文库、该论文所属 mode set、审计记录和结果；
- `task_type` 标识要运行哪一种 benchmark 任务语义；
- 两者合起来唯一定位 `tasks/<task_type>/<paper_id>/`；
- 计算论文同时拥有自主科研和论文复现任务；另一组实验论文只拥有实验验证任务；
- 这两个值是两个独立字段，不拼成新的持久化 task ID。

最终数据集采用更严格的 mode-set 不变量：

```text
计算论文：
    {autonomous_research, paper_reproduction}

实验论文：
    {experiment_validation}
```

每篇论文在每种 `task_type` 下最多发布一个核心任务。计算论文同时生成两个计算模式；
experiment-validation 使用另一组实验论文，不与计算论文的两个模式交叉。repository
仍按单个任务索引，release validator/installer 负责检查每篇论文的 mode set 是否完整且
没有混合；同一个 `paper_id` 不得同时出现在计算论文集合和实验论文集合中。

### 18.3 Runner 和 workspace

修改 `evaluation/execution/runner.py`、`workspace.py`、`lifecycle.py`：

1. `TaskRunner` 构造参数改为 `paper_id` 和 `task_type`；
2. runner 读取 `<package>/agent_input/task.md` 和
   `<package>/agent_input/submission_schema.json`；
3. workspace 创建时只复制 `agent_input/` 的内容：

   ```text
   agent_input/task.md                 -> workspace/task.md
   agent_input/submission_schema.json  -> workspace/submission_schema.json
   agent_input/data/                   -> workspace/data/
   ```

4. 不再读取 manifest allowlist 来动态扩大公开面；`agent_input/` 是唯一公开根；
5. `task_info.json`、`package_manifest.json`、`evaluation/` 和 `papers/` 永远不进入
   workspace；
6. 运行记录和 `_meta.json` 分别记录 `paper_id`、`task_type`、agent、repeat 和 run ID，
   不再写 `task_id`；
7. run ID 是一次执行的技术身份，可以由 `task_type-paper_id-agent-time-nonce` 组成，
   但该字符串不回写任务包，也不成为新的任务 ID。

### 18.4 Scoring 和 evaluator 加载

修改 `evaluation/scoring/adapters.py`、`service.py` 和相关 schema：

1. scorer 通过 `(task_type, paper_id)` 找到任务包；
2. evaluator context 直接读取五个拆分文件，不再要求聚合的
   `evaluation/reference.json`；
3. 在内存中建立评分运行对象，不生成新的持久化 evaluator 格式；
4. autonomous 和 reproduction 分别读取自己的 evaluation，不假设两套规则完全相同；
5. 结构化结果只按该模式的 `submission_schema.json` 和 `scoring_rules.json` 绑定；
6. score、provenance 和 token usage 记录分别写 `paper_id` 与 `task_type`；
7. evaluator 文件仍不可被 Agent-facing API、静态文件接口或 workspace materializer
   读取。

### 18.5 CLI、评测配置和 Web API

推荐修改为显式双字段接口：

```bash
researchchembench-eval \
  --paper-id paper_2aca1dd116799b28 \
  --task-type autonomous_research \
  --agent <agent>
```

批量评测配置推荐写为：

```yaml
tasks:
  - paper_id: paper_2aca1dd116799b28
    task_type: autonomous_research
  - paper_id: paper_2aca1dd116799b28
    task_type: paper_reproduction
```

Web API 推荐改为：

```text
GET  /api/tasks
GET  /api/tasks/<task_type>/<paper_id>/info
GET  /api/tasks/<task_type>/<paper_id>/files
POST /api/runs  {"paper_id": "...", "task_type": "...", "agent": "..."}
```

`/files` 只能浏览 `agent_input/data/`，不得以相对路径访问 package 根、论文库或
evaluation。前端任务选择器显示 `paper_id`、任务模式、title 和论文简要信息，不构造
隐藏的 task ID。

### 18.6 论文库在 benchmark 中的职责

benchmark 使用：

```text
papers/<paper_id>/paper_info.json
papers/<paper_id>/documents/main.pdf
papers/<paper_id>/documents/supplementary_*.pdf
```

其中：

- repository 可以读取 `paper_info.json` 用于后台展示和人工策展；
- 被评测 Agent 的 runner 不读取也不直接挂载共享 `papers/`；
- Agent-facing Web 文件接口不提供论文下载路径；
- scorer 使用任务包中的 evaluation 即可评分，不要求运行时重新解析 PDF；
- 论文 PDF 只服务于数据集审计、人工复核和未来重新合成。

用户已确认 `experiment_validation` 需要把论文正文和 SI 显式放入自己的
`agent_input/`。在该模式中，论文实验事实和作者结论属于公开问题材料；作者结论应
表示为待独立计算检验的 hypothesis，不能作为主要隐藏答案。主要评分对象应是 Agent
实际产生的计算过程、关键计算结果、计算产物、计算 observable 与实验 observation 的
映射、竞争假设区分能力和由这些证据支持的校准结论。仅复述论文结论而没有有效计算
证据必须按严重失败处理。PDF/SI 由 experiment-validation 生产管线显式复制到该任务
自己的 `agent_input/` 并由其 Gate 审计；共享 `papers/` 仍不能被 runner 整体挂载。
本计算任务管线不会为 experiment-validation 生产或修改这些输入。

### 18.7 Benchmark 测试迁移

需要重写或新增：

- `tests/test_task_package_v1.py` 对应的 v19 package 测试；
- repository 的 `(task_type, paper_id)` 发现、重复和查询测试；
- runner 只复制 `agent_input/` 的隔离测试；
- scorer 读取五个 evaluator 文件的测试；
- CLI 双字段参数和 YAML task selector 测试；
- Web API 双字段路由和目录越界测试；
- run metadata、results、token provenance 不再依赖 task ID 的测试；
- data pipeline release 与 benchmark repository 的端到端加载测试。

端到端验收必须证明：

1. 同一 `paper_id` 的多个正式模式可以同时被索引、运行和评分；
2. 全链路没有 `task_id` 或 `task_family_id`；
3. 被评测 Agent workspace 中不存在 evaluation、paper metadata 或 manifest；
   autonomous/reproduction 中不存在 PDF，experiment-validation 仅能看到其生产管线
   显式放入 `agent_input/` 的 PDF/SI；
4. release 任务无需转换即可被 benchmark 直接加载；
5. scorer 可以用相应模式的五个 evaluation 文件完成评分；
6. CLI、批量配置、Web、结果记录使用同一组 `paper_id + task_type` 参数。

## 19. 用户已确认的实施决定与剩余边界

已确认：

1. 将合同迁移到 `evaluation/contracts/task_package.py`，并彻底删除顶层
   `researchchembench_contracts/`；
2. 现有 `ResearchChemBench/tasks/` 下的旧格式任务不迁移、不兼容，在代码实施阶段
   删除；删除前只做目标清单和路径核对，不把旧任务内容投影进 v19；
3. benchmark runtime 继续正式支持 `experiment_validation`，标准目录为
   `tasks/experiment_validation/<paper_id>/`；`data_pipeline_experiment_validation` 的
   内部改造不属于本实施任务；
4. CLI、YAML、Web API、repository、runner、scoring 和运行记录统一使用两个显式字段
   `paper_id + task_type`，不接受单字符串复合任务选择器；
5. 旧 run/result 文件保持不动，新 runtime 不读取其中的 `task_id`，也不提供兼容
   adapter；新运行全部写 `paper_id + task_type`。

6. `experiment_validation` 的 `agent_input/` 允许包含由其生产管线显式选择的论文
   PDF/SI；共享 `papers/` 不直接挂载。其作者结论是公开待验证假设，主要评分绑定独立
   计算过程和结果；本管线的 `autonomous_research` 和 `paper_reproduction` 仍禁止
   PDF/SI。
7. 每篇论文在每种 `task_type` 下最多发布一个核心任务，因此
   `(task_type, paper_id)` 足以唯一定位任务，不增加 subtask ID；
8. 计算论文固定生成 `{autonomous_research, paper_reproduction}` 任务对；
   experiment-validation 使用不同的实验论文，每篇只生成 `{experiment_validation}`，
   两类 mode set 不交叉。

当前 data pipeline 和共享 benchmark runtime 的实现边界已经闭合，没有其他阻塞代码
实施的未确认事项。

`experiment_validation` 的论文通常没有作者参考计算结果，因此它自己的数据管线仍需
决定如何形成可审计的 computational reference：运行策展参考计算、采用方法鲁棒的
区间/趋势规则，或二者结合。该问题只影响 experiment-validation evaluator 的科学
强度，不影响当前 autonomous/reproduction 管线和共享 runtime 改造，也不授权本任务
修改其代码。

代码实施开始后按第 16-18 节执行，并在删除现有 tasks 前核对精确目标目录。当前文档
更新步骤不修改代码，也不删除 tasks。

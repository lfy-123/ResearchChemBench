# Stage06/07 v24 科学可行性优先、任务构建与审计修改方案

## 1. 文档状态

本文档是 v24 讨论版设计方案。它根据 v23 五篇真实回归、逐文件质量审查以及用户对外部数据、
结构输入和计算成本边界的确认编写。

当前只确定设计和后续代码修改范围，不修改代码，不提交新测试。

已确认边界：

1. 被评测 Agent 不能访问一般互联网，也不能看到论文或 SI；
2. benchmark runtime 可以提供 CCDC、PubChem 等受控数据库连接；
3. 必要输入尽可能放入 `agent_input` 自包含；
4. 可以只提供唯一分子连接关系，由被评测 Agent 自行生成 3D conformer；
5. Stage06 不判断实际计算成本，重点保证科学问题定义完整、计算路线可以被复现；
6. Stage06 必须在合成任务前先判断科学可行性；缺少必要输入或评分参考的模式不继续合成；
7. 两种模式分别判断可行性：只有一个模式可行时只发布该模式，不因另一模式不可行而放弃整篇论文；
8. Stage07 可以修复 Stage06 的构建产物，但不能更换、削弱或重新定义科学目标；
9. CCDC、PubChem 等受控数据库是按需输入来源，不是所有任务的必经步骤；只有任务实际依赖数据库记录
   或数据库检索时，才要求被评测 Agent 主动调用连接器，并由数据管线保存 Agent 不可见的固定快照。

## 2. v23 问题与 v24 总目标

v23 的五篇任务全部机械发布，但严格逐文件审查后没有一篇可以不经修正直接进入 benchmark。
该结果不是五篇论文突然全部科学可行，而是以下两类变化叠加：

- 合理变化：新模式不再要求复现论文软件、泛函、基组和 ordered protocol，因此旧版部分拒绝标准
  已不适用；
- 错误放行：Stage06 把论文中存在的信息、外部数据库理论可得的信息和最终 `agent_input` 中实际可得
  的信息混为一谈，Stage07 又没有独立推翻错误的 `input_closure=passed`。

v24 的总目标是：

```text
先证明任务可构建
再生成 paper_reproduction
再从 route-neutral scientific core 生成 autonomous_research
最后验证 evaluator 与实际提交合同
```

一个“可以写出合理 task.md”的论文不等于任务可构建。只有科学目标、公开输入、隐藏参考和可复现
调查合同对某一模式同时闭合时，Stage06 才构建该模式。两种模式可以同时通过，也可以只通过一个；
只有两个模式都不可行时，整篇论文才以 `scientific_not_constructible` 结束。

## 3. 科学输入与受控外部数据库边界

### 3.1 三类可接受公开输入与不可接受边界

#### A. 论文已有、自包含且不泄露答案的输入，默认优先

包括：

- SMILES；
- SDF、MOL、CIF；
- 合法 XYZ；
- 完整分子连接表和必要的原子映射；
- 明确的电荷、多重度、绝对构型；
- 任务所需实验条件和物理边界。

如果论文正文或 SI 已经提供这些信息，且它们属于研究前的科学对象定义而不是待评分结果，Stage06 应优先
直接利用并写入 `agent_input/data/inputs/`，不再为了形式上的“自主检索”强制转换为 PubChem/CCDC 查询。
Stage06 可以从来源明确且结构唯一的论文结构式整理出机器可读的 SMILES、SDF 或连接表，但必须核对
连接关系、立体化学、电荷和必要的原子映射；来源图示仍有歧义时不能自行猜测。

直接给出确定的分子身份不妨碍被评测 Agent 自主开展科研。被评测 Agent 仍负责生成 3D conformer、选择
合理构象、组装复合物、提出候选机理和准备计算输入。自包含输入不需要数据库快照。

#### B. 特定数据库记录是必要科学输入时，使用稳定记录标识

当任务必须使用某个特定实验晶体、盐型、多晶型或数据库实体，而论文没有提供足够的可直接使用结构时，
可以依赖受控数据库。此时必须同时满足：

1. 明确数据库名称；
2. 明确、稳定、唯一的 CID、CCDC deposition number、CSD refcode 或等价记录标识；
3. benchmark runtime 已声明提供对应连接器；
4. 数据库记录唯一对应任务实体；
5. 如需结构变换，变换位置、操作和保留的构型必须明确且无歧义；
6. 数据库记录和变换不能直接携带待评分的结果结构或答案。

例如以下形式可以成为闭合输入：

```text
database: CCDC
record_id: 1941938
purpose: starting connectivity for p-2BN
transformation: replace the explicitly identified octyl side chains with methyl while preserving
the deposited core connectivity and stereochemical relationships
```

被评测 Agent 必须主动调用 runtime 数据库连接器获取该记录、验证身份并准备计算结构。连接器不访问随时间变化
的实时结果，而是返回任务合成时保存的 pinned record snapshot。只有使用名称检索候选时才额外固定 search
result set。数据管线按实际路径保存 query（如有）、候选结果集合（如有）、最终记录、retrieval timestamp、
数据库版本信息（若有）和 checksum；这些快照位于 Agent 不可见的 provenance 区域，但通过正常数据库工具
调用返回给 Agent。这样既保留数据库检索和身份判断能力，也保证不同模型、不同时间获得相同的数据库视图。

#### C. 数据库记录选择本身是科研步骤时，允许名称检索候选

只有任务确实要评价实体检索、晶型选择或结构选择能力时，才可以不直接给出唯一记录 ID，而只给化学名称
和足以判断的科学约束。连接器必须返回任务合成时固定的候选结果集合，Agent 负责选择记录并说明理由。
Stage06 必须确认候选空间有限、选择条件可表述，并且不同合理选择不会使隐藏 reference 失去公平可比性。

普通分子身份不应为了增加工具调用而采用这种路径。一个无歧义的普通分子若已由论文给出 SMILES、结构式
或结构文件，直接使用自包含输入即可。

#### D. 不可接受输入

包括：

- 只有论文内部编号，例如 `(S)-A2`；
- 只有作者专用名称，例如 `p-2BN`，却没有结构文件、完整连接关系，且也没有受控数据库中的可判定候选；
- “根据论文图构建”；
- “自行从文献寻找催化剂结构”；
- 只有数据库名称或模糊名称，却没有唯一记录标识，也没有把有限候选选择明确设为科研步骤；
- 需要猜测取代位置、质子化、互变异构、绝对构型或反应原子映射；
- 依赖论文/SI 或一般互联网才能解释的输入。

### 3.2 输入来源的选择顺序

Stage06 按以下顺序选择最简单且科学闭合的输入方式：

```text
论文/SI 已有可用且不泄露答案的结构身份
-> 直接生成自包含输入

任务依赖某条特定实验或数据库记录
-> 给稳定记录标识，由 Agent 调用固定快照连接器

选择哪条记录本身是研究问题
-> 给名称和科学约束，由 Agent 在固定候选集合中选择
```

不得为了统一格式而把第一类任务强制改造成数据库检索任务，也不得因为数据库理论上可以搜索，就省略
Stage06 对实体身份、歧义和答案泄露的判断。

### 3.3 数据库可用不等于自动闭合

CCDC/PubChem 连接只是按需使用的输入来源，不是放宽科学身份的理由。任务实际依赖数据库时，Stage06
仍必须判断：

- record ID 是否对应任务中真正计算的实体；
- 是否还需要论文未公开的结构变换；
- 数据库实体是否具有正确质子化、构型和取代形式；
- 变换后是否仍有多个不等价结构解释；
- 数据库条目是否为研究前输入，而不是待复现结果。

无论输入来自论文还是数据库，都要做同一项答案边界判断：反应物、已知产物、起始催化剂或研究前实验
条件可以作为问题定义；如果某个 TS、最低能中间体、优势构象、产物排序或机理身份正是待评分结论，就不能
因为它出现在论文、SI 或数据库记录中而放入公开输入。

## 4. Stage06 科学可行性的四个必要条件

四项条件先在共享科学核心上判断，再分别判断 reproduction 和 autonomous。某个模式任意一项失败，
Stage06 不生成该模式；另一个模式仍可独立构建。只有两种模式都失败时，才输出整篇论文级
`scientific_not_constructible`。

### 4.1 Scientific objective closure

必须满足：

- 目标是论文中心或足够重要的计算科学问题；
- 可以通过计算得到明确的过程关键点和结论；
- reproduction 和 autonomous 能围绕同一个目标构建；
- 不为了适配已有输入而缩成与论文核心关系很弱的代理任务；
- 若缩小范围，必须说明缩小后的问题为何仍能检验中心科学主张。

缺少作者完整软件或 protocol 不导致该项失败。

### 4.2 Public input closure

执行以下反事实测试：

> 删除论文、SI、隐藏 evaluator 和一般互联网，只给最终 `agent_input` 以及明确允许的数据库连接器，
> 被评测 Agent 能否唯一建立任务要求的计算体系？

必须能确定：

- 研究对象和分子连接关系；
- 必要的立体化学、质子化和原子映射；
- 电荷、多重度和环境；
- 比较对象和物理边界；
- 哪些内容由 Agent 自行生成，哪些是已给定输入。

Stage06 还必须记录每项关键输入来自论文/SI、自包含文件还是受控数据库，以及它是研究前输入还是待评分
结果。论文已经给出的结构身份可以直接使用，但“论文中存在”本身不能替代对最终公开文件的核验。

允许 Agent 自行生成 conformer 和 3D 初始几何，不允许 Agent 猜分子身份或连接关系。

### 4.3 Evaluation closure

必须确认论文/SI 具有足够的隐藏参考来生成：

- source-supported reference key points；
- source-supported reference conclusions；
- 数值、排序、结构身份、状态或具体文本结论；
- 初步评分规则；
- evidence map 和 critical failures。

v24 采用“开放任务、封闭参考”：被评测 Agent 可以自主提出论文之外的候选、假设和计算路线，但正式
evaluator 的 reference key points、reference conclusions、数值、排序、结构身份和机理结论只能来自当前
论文正文或 SI，并必须绑定具体 source evidence。Stage06/Stage07 自行推导的新机理、自行计算的新数值、
其他论文结果或先前模型输出不得成为隐藏参考答案。若当前论文/SI 的参考不足以形成具体可判断的 evaluator，
对应模式的 evaluation closure 失败。

同时，公开任务必须给出公平比较所需的 measurement contract，例如：

- 被评分物理量定义；
- 能量参考和比较方向；
- 单位；
- 必要的温度、标准态和电子态边界；
- RMSD 的 atom set/alignment convention；
- reorganization energy 使用的定义；
- submission 字段和结果结构。

这些属于问题定义，不是参考答案，也不是作者计算 protocol。

如果源数值存在但 measurement definition 无法恢复：

1. 能公开一个与 source reference 确实可比较的定义时，正常生成 numeric rule；
2. 数值无法公平比较但可靠排序/机理结论仍可判断时，以 ordering/semantic/condition 为主要规则；
3. 连关键结论都无法公平判断时，判定该科学目标不可构建。

若正文、SI、图表之间存在无法解释的 reference 冲突，不自行选择最方便的结果。可以在定义明确时分别保存
不同量；可以降级为论文中仍一致的 ordering/semantic/condition reference；若核心参考整体不确定，则
对应模式不可构建。

### 4.4 Reproducible investigation closure

Stage06 不判断实际运行成本、体系大小和真实完成时间，但任务必须满足：

- 科学搜索空间有限且可以描述；
- 候选生成、去重、晋级和停止依据明确；
- 验证条件明确；
- 未覆盖空间需要进入 limitations；
- 被评测 Agent 自主选择方法并完整记录方法、参数、输入构造、搜索范围和 provenance；
- 另一个研究者可以根据提交记录复现被评测 Agent 实际执行的计算路线。

这里要求复现的是被评测 Agent 的实际路线，不是作者论文的逐步 protocol。

## 5. Stage06 新工作流

### A. 选择并冻结科学目标

先确定：

- objective；
- requested results；
- physical boundaries；
- route-neutral validation requirements。

此时不生成任何 public task 或 evaluator。

### B. 完成四项可行性审查

写 `outputs/workflow_review.json`，分别记录：

```text
objective closure
public input closure
evaluation closure
reproducible investigation closure
```

每项说明：

- `passed` 或 `failed`；
- 证据；
- 必要 public input 的文件路径或数据库 record ID/query；
- 未解决问题；
- 未解决问题是否会改变科学对象或评分公平性。

共享审查完成后，分别记录：

```text
paper_reproduction: feasible | infeasible
autonomous_research: feasible | infeasible
release_modes: [实际可构建和发布的模式]
```

模式不可行必须给出该模式特有的理由。例如作者路线使 reproduction 具有有限候选空间，但移除该路线
后 autonomous 成为无法合理限定的开放搜索时，可以只构建 reproduction。

### C. 对不可行模式立即终止

某一模式任一必要条件失败：

```text
mode decision = infeasible
```

停止该模式的合成，不为其生成 public task 或 evaluator；如果另一模式可行，则继续构建并发布另一模式。
只有两个模式都不可行时，才只写 `workflow_review.json` 和 rejection receipt，并使用论文级：

```text
decision = scientific_not_constructible
```

不得通过以下方式绕过：

- 引用被评测 Agent 看不到的论文图；
- 假设可以访问一般互联网；
- 把内部编号当结构；
- 让被评测 Agent 自行猜连接关系；
- 选择过弱、非中心的替代目标；
- 用模糊 semantic rule 掩盖 reference 不足；
- 把非关键 warning 写成理由后继续把 essential input 标为 passed。

### D. 构建可行的 paper reproduction

只有 reproduction 的可行性四项全部通过才进入该步骤：

```text
paper_reproduction
= route-neutral scientific core
+ author qualitative scientific route
```

允许公开：

- 作者假设；
- 候选机理类别；
- 定性科学解释；
- 需要独立验证的路线。

禁止公开：

- 候选胜出方向；
- reference ordering；
- 结果性 TS、intermediate 或 selected conformer；
- 数值答案；
- 完整结论；
- 论文软件、model chemistry 和 ordered protocol。

完成完整 public task 和五个 evaluator 文件，运行 reproduction self-check，只修实际 findings。

### E. 从 route-neutral core 构建可行的 autonomous research

```text
autonomous_research
= route-neutral scientific core
```

只有 autonomous 的可行性四项全部通过才构建。不得复制 reproduction 后只删除几个句子。objective、
validation、search scope 和 deliverables 都必须从不含 `author_route` 的 scientific core 生成。

autonomous 可以规定：

- 科学目标；
- 研究前输入；
- 物理和 measurement boundary；
- 结果必须具备的有效性；
- 有限搜索和停止依据。

autonomous 不应规定作者专有的反应坐标、解释 observable、候选机理或等价暗示。若有真实假设空间，
要求被评测 Agent 自行提出至少两个可区分解释，并自行选择判别计算和 observable。

若两种模式都构建，完成 full-pair semantic audit 和 self-check；若只构建一个模式，运行对应 single-mode
semantic audit 和同一 common Gate。所有 `release_modes` 都通过后才写 constructed receipt。

## 6. workflow review 最小结构

建议保持精简：

```json
{
  "decision": "candidate_ready | scientific_not_constructible",
  "paper_id": "...",
  "scientific_core": {},
  "feasibility": {
    "objective": {},
    "public_inputs": {},
    "evaluation": {},
    "reproducible_investigation": {},
    "modes": {
      "paper_reproduction": {"status": "feasible | infeasible", "reasons": []},
      "autonomous_research": {"status": "feasible | infeasible", "reasons": []}
    },
    "release_modes": []
  },
  "paper_route": {},
  "reference_results": {},
  "reasons": [],
  "warnings": []
}
```

`public_inputs` 至少表达：

```json
{
  "status": "passed",
  "agent_input_assets": [
    {
      "path": "data/inputs/reactants.sdf",
      "purpose": "problem-defining reactants",
      "source": "paper_or_si"
    }
  ],
  "database_inputs": [
    {
      "database": "CCDC",
      "record_id": "1941938",
      "purpose": "starting connectivity",
      "transformation": "explicit deterministic transformation or none"
    }
  ],
  "unresolved_essential_inputs": []
}
```

`database_inputs` 可以为空；自包含任务不应为了填充该字段而制造数据库依赖。只有走数据库路径时才要求记录
稳定标识，或者在“记录选择本身是科研步骤”时记录固定 query 和候选集合。

若 `unresolved_essential_inputs` 非空，`status` 不能为 `passed`。非关键 conformer coverage、方法敏感性等
进入 warnings 或任务 limitations，不与 essential input 混用。

## 7. evaluator 合同修改

继续保留五个文件：

```text
reference_key_points.json
reference_conclusions.json
scoring_rules.json
evidence_map.json
critical_failures.json
```

继续保留四种 rule type：

```text
numeric
ordering
condition
semantic
```

不增加权重、总分、pass threshold、scoring-executor 或人工复核标签。

Stage06 和 Stage07 必须逐条核对：

```text
reference scientific claim
-> rule type 与 target/expected
-> binding 指向的 submission field
```

要求：

- numeric target 是 JSON number；
- 一个独立 scalar target 对应一条 numeric rule；
- 多个数值拆开；
- numeric field 在 schema 中明确为 number/integer；
- 用于评分的必要字段进入对应 `required` 链；
- semantic expected 包含具体科学内容；
- 有可信核心数值时不能以 semantic rule 合法为理由省略；
- 无公平可比较定义的 source number 不强行作为 numeric rule。

参考结果只来自当前论文/SI，但评分规则不能强制 autonomous 重走作者 ordered protocol。可以评价提交是否
获得与论文相容的科学结果、是否提供充分验证和证据链；不能因为 Agent 使用不同而有效的计算路线就自动
判错。通用 stationary-point、state、convergence 和 provenance 有效性要求属于任务/评分合同，不是新增的
隐藏科学答案。

Prompt 只加入一个短 numeric 和一个短 semantic 示例，不加入完整论文模板。

## 8. Stage07 新审计顺序

Stage07 不信任 Stage06 自报的 `feasibility.*.status=passed`，必须检查实际文件。

### 8.1 Scientific objective drift

确认 Stage06 没有为适配输入而将中心问题换成较弱或无代表性的代理任务。

### 8.2 Actual public input closure

从最终 `agent_input` 和允许的数据库连接规则重新判断：

- 文件是否真实存在；
- 自包含结构是否与 source evidence 一致且不泄露待评分结果；
- 若任务依赖特定数据库记录，稳定记录标识是否明确；
- 若数据库记录选择本身是科研步骤，query、固定候选集合和选择条件是否明确；
- 若任务依赖数据库，runtime 连接器是否属于允许能力且记录对应目标实体；
- 数据库或自包含结构所需的变换是否确定；
- 是否仍依赖论文/SI、一般互联网或猜测。

Stage07 可以修复 Stage06 构建产物中的错误，包括：补写源证据已经唯一确定但 Stage06 遗漏的输入、
修复结构文件转录或格式、补全实际需要的 database record ID/provenance、纠正 schema/evaluator binding，
以及重写不准确或发生泄露的任务表达。所有修复都必须由既有源证据唯一决定，并在修改后重新验证实际文件。

只要某个模式已经存在完整的任务目录、科学目标合理且保持不变，Stage07 可以对该模式进行大幅重写，
包括重写 task instruction、public input 表达、submission schema 和 evaluator 文件。允许大幅修改的是构建
质量，不是科学问题本身。若整个模式目录缺失，Stage07 不从零新建该模式；该模式保持未构建，另一可行
模式仍可独立批准和发布。

Stage07 不得：

- 更换科学目标；
- 将较弱、非中心的代理问题替代原目标；
- 为使任务通过而重新定义待评分科学量；
- 在源证据不足时发明分子身份、连接、构型或 reference；
- 把不可行的 autonomous 通过重新加入作者路线变成可行。

如果问题来自科学目标选择、目标本身不可闭合或修复必然改变目标，Stage07 必须拒绝相应模式。若另一模式
保持可行，则可以只批准另一模式，不必拒绝整篇论文。

### 8.3 Evaluation closure

检查 measurement definition、reference、rule、binding 和 schema 是否公平一致。

### 8.4 Mode boundary and answer inversion

检查 reproduction 只包含作者定性路线，autonomous 不包含作者路线，两者均不泄露结果。

### 8.5 Repair verification

每次修复后：

- 重读完整 `task.md`；
- JSON 重新 parse；
- XYZ 或其他标准格式用相应最小 parser 验证；
- evaluator 重新核对 claim-rule-binding；
- 最后运行 common Gate；
- receipt 只能描述从最终文件实际验证的结果。

## 9. Common Gate 最小修改

只增加通用机械合同：

1. numeric target 必须是 JSON number；
2. 被评分字段必须在 schema 中显式声明；
3. numeric binding 必须解析到 number/integer leaf；
4. 用于评分的必要字段进入对应 required 链；
5. `.xyz` 检查 atom count、comment、坐标行数和数值列。

Gate 不判断：

- 分子身份是否科学正确；
- CCDC/PubChem record ID 是否对应正确科学对象；
- tolerance 是否科学最优；
- 论文机理是否正确；
- 任务是否论文中心；
- autonomous 是否语义泄露路线。

这些仍由 Stage06/07 Agent 科学判断。self-check 和 external Gate 继续共用同一机械实现。

## 10. 当前五篇的预期处置

这些是人工预期，不写入代码或 Prompt：

| paper_id | v24 预期 |
|---|---|
| `paper_2aca...` | objective/input/reference 可闭合；应构建，修 autonomous 路线和 evaluator |
| `paper_611...` | 正确 S0 XYZ 可获得时应构建；非法 XYZ 必须被 Gate 阻断 |
| `paper_76ae...` | 必须补完整 catalyst/substrate 连接和构型或稳定数据库 ID；否则科学拒绝 |
| `paper_945...` | objective/input/reference 基本闭合；应构建并修 numeric rule |
| `paper_a556...` | CCDC 可用、变换明确、measurement definition 可比较时构建；否则拒绝或改用可靠 non-numeric 核心 |

发布篇数不是验收指标，也不在 Prompt 中暗示应通过或拒绝几篇。

## 11. 五项实施硬边界

### 11.1 科学可行性按模式独立判断，任务对不是强制发布单位

一篇论文可以发布一个或两个模式：

```text
paper_reproduction 可行 -> 可以发布 reproduction
autonomous_research 可行 -> 可以发布 autonomous
二者都可行 -> 发布完整任务对
只有一个可行 -> 只发布该模式
二者都不可行 -> 整篇论文 scientific_not_constructible
```

不能只证明 reproduction 可行，就默认 autonomous 也可行。典型反例是：作者路线将一个巨大机理空间
缩小为一个明确候选，因此 reproduction 可以验证；移除该路线后，autonomous 变成没有合理边界的全反应
空间搜索。此时保留 reproduction、拒绝 autonomous，而不是放弃整篇论文或把作者路线泄露给 autonomous。

Stage06 的 feasibility review 应分别记录两个模式的可行性和 `release_modes`。后续统计必须区分
paper-level constructibility、mode-level release 和真正成对任务数量，不能把单模式发布误报为完整任务对。

### 11.2 Public measurement contract 不得成为作者路线泄露

为了公平比较，任务可以公开：

- 被评分物理量的定义；
- 能量参考、温度、标准态和单位；
- RMSD atom set/alignment convention；
- reorganization-energy definition；
- submission schema 和结果字段；
- 结果成立所需的通用验证条件。

但 measurement contract 不能公开：

- 作者特有的反应坐标；
- 作者用来证明其解释的专有 observable；
- 应优先搜索的作者候选；
- 与 reference conclusion 等价的结构特征或结果方向。

原则是：

```text
公开“如何定义和报告结果”
不公开“应该沿哪条作者路线找到结果”
```

Stage07 应分别审计 measurement definition 和 route leakage，不能因为某段文字属于“validation”就默认其
可以进入 autonomous。

### 11.3 仅在实际依赖时启用 CCDC/PubChem，且依赖必须可复现

数据库不是通用必需工具。论文/SI 已提供明确、机器可用且不泄露答案的分子身份时，直接生成自包含输入；
被评测 Agent 自行完成构象、三维结构和计算模型准备。只有任务确实依赖特定记录或记录选择时，才引入
CCDC/PubChem 连接器。

任务依赖某条特定受控数据库记录时，必须记录：

- database 名称；
- stable record ID；
- 检索用途；
- 预期实体身份；
- 必要的确定性结构变换；
- 检索或解析 provenance；
- 若 runtime 能提供，记录数据库记录版本、retrieval timestamp 或内容 checksum。

在这些数据库依赖型任务中，被评测 Agent 应通过数据库工具主动获取记录，而不是在 `agent_input` 中同时
获得数据管线预取的同一结构文件。runtime 连接器返回任务合成时固定的 pinned record snapshot；如果记录
选择本身属于科研步骤，还要返回固定的 pinned search result set。快照同时保存在 Agent 不可见的 provenance
区，用于科学审计、回归重放和数据库漂移追踪。

若许可不允许保存完整数据库内容，则保存合法的记录摘要、query、retrieval timestamp、版本信息（若有）
和内容 checksum。数据库临时不可用属于技术运行问题，不改变任务的科学可行性结论。

数据库临时连接故障属于技术运行问题，不应被改写成科学不可构建；但任务所依赖的数据库实体不唯一、
record ID 与目标不符、候选选择没有科学边界或结构变换存在科学歧义，属于 input closure 失败。

若任务不依赖数据库，则不要求数据库调用、记录 ID、候选快照或数据库 provenance，也不能因没有这些内容
而拒绝任务。

### 11.4 独立方法与论文 reference 必须先判断可比性

“被评测 Agent 自主选择计算方法”不表示任何论文数值都能直接作为严格 numeric target。Stage06 必须
判断 reference 对合理方法变化和 measurement definition 的敏感性：

```text
定义明确，且合理独立方法下可公平比较
-> 正常 numeric rule

绝对数值方法敏感，但数值、排序和科学结论仍具有可解释关系
-> 保留合理 tolerance，并同时生成必要的 ordering/condition/semantic rules

source number 的定义无法恢复，但可靠排序或科学结论仍可判断
-> 不把该 number 强行作为 numeric target，只使用可靠 non-numeric reference

连核心排序、状态或结论都不能公平判断
-> evaluation closure failed
```

不设置统一 tolerance，不强制 numeric rule，也不因为 numeric rule 缺失就放宽 key point 和 conclusion 的
具体性。所有被采用的 reference 都必须与公开 measurement contract 一致。

### 11.5 实际 Prompt 必须显著短于设计文档

本文档用于完整定义边界，不应原样复制到 Stage06/07 Prompt。实际 Stage06 Prompt 只保留：

```text
A. 冻结 route-neutral scientific core
B. 审查 objective/input/evaluation/reproducibility 和 per-mode feasibility
C. 停止不可行模式；两个模式都失败时才整篇科学拒绝
D. 构建并自查可行的 reproduction
E. 从 clean core 构建并自查可行的 autonomous
F. evaluator semantic alignment 和 terminal receipt
```

只加入三个短示例：

1. 受控数据库输入示例；
2. author route、answer 和 autonomous 边界示例；
3. 一个 numeric rule 和一个 semantic rule 的最小结构示例。

Prompt 不重复解释所有例外，不加入完整论文模板，不为每类化学问题增加 checklist。token 优化应删除重复
文字和重复工具行为，不能删除任务关键的科学对照、验证、uncertainty 或 alternative hypotheses。

## 12. 后续代码修改范围预案

方案确认后预计涉及：

- `src/stages/stage06_task_builder/prompts.py`
  - feasibility-first 工作流；
  - 受控数据库边界；
  - objective/input/evaluation/reproducibility 四项闭合；
  - route-neutral autonomous 生成；
  - evaluator micro-examples。
- `src/stages/stage07_task_judge/prompts.py`
  - 独立复核 feasibility；
  - database input 审计；
  - objective drift；
  - repair 后解析验证。
- `src/stages/phase_gate.py`
  - numeric target 类型；
  - explicit schema field/required chain；
  - numeric leaf；
  - XYZ parser。
- Stage06/07 定向测试
  - 论文/SI 已有 SMILES、结构式或结构文件时优先生成自包含输入，不制造数据库依赖；
  - 自包含 source structure 的身份核验和答案泄露边界；
  - 特定 CCDC/PubChem 记录依赖的 stable record ID；
  - 数据库记录选择属于科研步骤时的固定 query、候选集合和选择条件；
  - 明确 database transformation；
  - database provenance 和可恢复性；
  - 非数据库任务不因缺少 record ID、snapshot 或数据库调用而失败；
  - 论文内部 label 拒绝；
  - 缺作者 protocol 不误拒绝；
  - 缺 measurement definition 时不错误生成 numeric rule；
  - evaluator reference 仅来自当前论文/SI；
  - Agent/Stage06/Stage07 自行推导结果不能成为 reference；
  - 正文/SI reference 冲突时不任意选择；
  - reproduction 可行但 autonomous 不闭合时，只发布 reproduction；
  - autonomous 可行但 reproduction 不闭合时，只发布 autonomous；
  - 两种模式都不可行时才整篇 scientific rejection；
  - measurement contract 不包含 author-route discriminator；
  - method-sensitive source number 不被错误强制为 numeric target；
  - 整篇 scientific rejection 不生成任务树，单模式不可行不生成对应模式树；
  - Stage07 能推翻单个模式的错误 feasibility，并保留另一可行模式；
  - Stage07 可以修复构建文件，但不能改变 scientific objective；
  - 已存在完整模式且目标正确时，Stage07 可以大幅重写构建产物；
  - 整个模式缺失时 Stage07 不从零补建该模式；
  - numeric/schema/XYZ Gate fixtures。

本版不增加新 Agent、Stage06B、Stage07B、retry、resume、兼容投影或代码生成 evaluator 科学骨架。

## 13. 验收标准

- Stage06 先判断四项可行性，不继续合成不可行模式；
- reproduction 和 autonomous 分别判断，只构建并发布实际可行模式；
- 单模式发布与完整任务对在 workflow review、receipt、release 和统计中明确区分；
- 不因缺少作者软件、泛函或 ordered protocol 误拒绝；
- 不因论文中存在结构图或数据库理论可查而误判任务输入闭合；
- 论文/SI 已提供明确且不泄露答案的结构身份时，优先生成自包含输入，不强制数据库调用；
- 数据库不是必填输入；非数据库任务不要求 record ID、snapshot 或数据库 provenance；
- 特定数据库记录输入具有明确 database、stable record ID、用途和确定性变换；
- 记录选择本身是科研步骤时，任务具有有限候选空间和明确选择条件；
- 仅数据库依赖型任务要求被评测 Agent 主动调用连接器，并返回对应 pinned record/search snapshot；
- 数据管线仅为实际数据库依赖保存足够的候选集合、记录快照、query 和 provenance；
- 可以由被评测 Agent 自主生成 3D conformer；
- 科学对象、连接关系和必要构型不需要猜测；
- source number 只有在 measurement definition 可公平比较时才成为 numeric target；
- evaluator 的科学 reference 只来自当前论文/SI，且具有 source evidence；
- autonomous 不因采用不同于论文的有效计算路线而被过程规则错误拒绝；
- public measurement contract 不携带作者路线、专有 discriminator 或结果方向；
- reproduction 公开作者定性路线但不公开答案；
- autonomous 从 route-neutral core 生成，不残留作者路线；
- evaluator claim、rule 和 binding 对齐；
- Stage07 能拒绝 Stage06 的错误可行性判断；
- Stage07 可修复构建错误和遗漏，但不能修改、削弱或替换科学目标；
- 完整模式可以大幅重写，缺失模式不能由 Stage07 从零重建；
- 修复后实际文件被重新读取或解析；
- self-check 与 external Gate 使用相同机械合同；
- 没有论文、化学类型、关键词或固定数值特例；
- 实际 Stage06/07 Prompt 保持精简，不照搬完整设计文档；
- 不以发布率作为成功标准。

## 14. 最终输入边界确认

本版不再存在需要阻塞代码设计的数据库输入边界问题，按以下规则执行：

1. **论文已有结构优先。** 论文/SI 给出明确 SMILES、结构文件或唯一结构式时，Stage06 直接整理成
   自包含输入；标准化学名称可以先由 Stage06 解析为机器可读结构，但解析不唯一时不能猜测。
2. **连接关系必须闭合，3D 不必预先给定。** 分子身份、连接关系、必要立体化学、电荷和多重度必须明确；
   conformer、复合物组装和 TS 初猜原则上由被评测 Agent 自主完成。
3. **输入结构不能变成答案泄露。** 已知反应物、已知产物和起始催化剂可以作为问题定义；若某个 TS、
   中间体、优势构象、产物排序或机理身份正是评分目标，则不得放入公开输入。
4. **特定实验记录才要求 record ID。** 只有科学问题依赖特定 CCDC 晶体、PubChem 实体、盐型或晶型时，
   才给出 stable record ID 并固定 record snapshot。
5. **名称检索不是默认步骤。** 只有数据库记录选择本身属于科研能力时，才让 Agent 根据名称和科学约束
   搜索固定候选集合；普通任务不为增加工具调用而这样设计。
6. **数据库可以作为可选辅助工具。** 非数据库依赖型任务中，Agent 可以自行调用允许的连接器补充名称、
   性质或结构信息，但该调用不参与任务可行性证明，不能成为隐藏 reference 的来源；runtime 记录该次调用
   的实际 query 和结果用于运行 provenance 即可。
7. **来源图示可以人工智能整理但不能凭空补全。** Stage06 可以将唯一、清楚的二维结构式转成 SMILES/SDF；
   取代位置、立体构型、质子化或原子映射仍有多个合理解释时，该输入不闭合，应补充来源证据或拒绝模式。
8. **数据库许可影响快照保存形式，不改变科学合同。** 允许保存完整记录时保存结构快照；不允许时保存合法
   摘要、record ID、query、时间、版本和 checksum，并确保 runtime 能稳定重放任务所依赖的数据库视图。

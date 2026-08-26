# Stage06/07 v21 发现导向自主科研任务修改方案

## 1. 文档状态

本文件是基于 v20 五篇真实回归形成的待确认设计方案。本轮只定义下一版任务语义、Agent
职责、evaluator 和审计边界，不修改代码，不提交新的论文测试。

v21 的核心目标是解决当前双模式差异不足的问题：

- `paper_reproduction` 不只是“指定方法计算同一个输入”，而是公开论文作者选择的候选、
  机理假设和计算路线，评估是否能够忠实执行和复现；
- `autonomous_research` 不再继承论文已经选定的产物、过渡态或机制候选，只提供研究开始前
  可获得的科学目标、初始体系和物理边界，要求被评测 Agent 自主提出候选并验证机制；
- 两种模式围绕同一科学问题，但公开信息量、public inputs 和 evaluator 重点可以不同。

## 2. 对用户设想的判断

该方向可行，而且比当前 v20 更能区分两类能力：

```text
paper_reproduction
  评估：能否理解并执行作者的候选、机理和计算路线

autonomous_research
  评估：能否从初始科学问题出发提出候选、搜索路径、验证并形成结论
```

但 reproduction 不应公开所有“正确答案”。建议区分三类信息：

### 2.1 reproduction 可以公开

- 作者研究的科学目标；
- 作者提出或选择的候选产物、构象、反应通道和过渡态身份；
- 论文披露的软件、方法、basis、solvation、thermochemistry 和计算顺序；
- 论文要求验证的 mechanism hypothesis；
- 完成计算所需且不会直接替代计算的 source-supported structures；
- 定性的待验证假设，例如“作者提出 pathway A 可能解释选择性”。

### 2.2 reproduction 不应公开

- 需要被重新计算的最终数值；
- 正确的能量排序，如果排序本身就是评分目标；
- 最终定量误差和 tolerance；
- 可以从 schema 直接读取的 reference conclusion；
- evaluator 的 hidden key points 和 scoring rules。

如果把数值答案、正确排序和 tolerance 全部给出，reproduction 将退化为结果抄写或格式
填充，无法验证计算能力。

### 2.3 autonomous 必须隐藏

- 作者最终选择的候选集合；
- 作者确认的机制、关键中间体、TS 和产物排序；
- 作者的计算软件、方法和有序计算过程；
- 论文 route 特有的文件名、结构标签和步骤编号；
- 论文结果、reference values、结论和 tolerance；
- 排除错误候选的负向提示，例如“不要使用某个暗态结构”。

## 3. 两种模式的新定义

### 3.1 `paper_reproduction`

目标：重放作者已经提出的科学路线，并判断计算是否得到论文支持的结果。

被评测 Agent 应获得：

1. 科学问题；
2. 作者选择的候选或 mechanism hypothesis；
3. 作者披露的计算过程；
4. 对应候选结构或执行该路线所需的 public inputs；
5. 明确的验证和交付要求。

它主要评分：

- route fidelity；
- calculation completion；
- stationary-point/state/convergence validation；
- numeric reproduction；
- 是否能够从重新计算的结果支持或否定作者假设。

### 3.2 `autonomous_research`

目标：在不知道作者候选、机制和计算路线的情况下，从初始体系和研究目标自主形成并验证
科学假设。

被评测 Agent 应获得：

1. 科学目标；
2. pre-discovery initial inputs；
3. charge、multiplicity、environment、temperature、composition 等必要物理边界；
4. 可选的实验约束，但只有当任务明确属于 experiment-constrained discovery 时才公开；
5. 计算预算和交付要求。

它应自主完成：

- 提出候选产物、构象、反应通道或机制；
- 设计候选搜索和筛选方法；
- 选择计算模型和验证策略；
- 对候选进行排序或淘汰；
- 找到最有支持的机制或结论；
- 说明未搜索空间和不确定性。

它主要评分：

- candidate coverage；
- hypothesis quality；
- search strategy；
- physical and chemical validity；
- validation evidence；
- 是否发现 paper-supported key candidate/mechanism；
- 是否给出同等合理或更合理的替代解释；
- final conclusion 和 uncertainty。

## 4. 两种模式不再强制共享完全相同的 public inputs

v20 默认两个模式共享相同 public inputs。这会使 reproduction 中作者提供的 TS、product、
rotamer 或 selected candidate 自动泄露到 autonomous。

v21 应改为：

```text
共享的是 scientific core 和 physical problem，
不是强制共享每一个 public artifact。
```

### 4.1 shared inputs

两种模式可以共同拥有：

- 初始反应物、催化剂、底物或基础分子结构；
- 初始 charge、multiplicity 和 environment；
- 研究目标所必需的非答案边界；
- 相同的计算资源上限。

### 4.2 reproduction-only inputs

只允许出现在 reproduction：

- paper-selected TS/product/intermediate coordinates；
- source-labeled rotamers 或 conformers；
- 作者 mechanism graph；
- paper route input decks 或 route-specific starting guesses；
- 会暴露作者候选选择的文件名和注释。

### 4.3 autonomous-only public input construction

autonomous 应从 pre-discovery source facts 重新准备输入，例如：

- 反应物和催化剂的独立结构，而不是最终 TS complex；
- 未标记为正确答案的初始 conformer 或 reactant ensemble；
- 物理组成和边界，而不是作者优化后的 product；
- 必要时提供中性的 `candidate_A/B`，但仅适用于“候选选择”任务，不应冒充完整 discovery。

代码不能自动决定或构造这些科学输入。Stage06 Agent 根据论文证据判断是否存在唯一、完整、
可公开的 pre-discovery inputs。

## 5. 构建可行性边界

并非每篇可以做 reproduction 的论文都能生成真正的 autonomous discovery task。

autonomous 只有同时满足以下条件才可构建：

1. 研究开始前的初始体系能够从 source 唯一获得；
2. 删除作者候选后，任务仍具有明确边界；
3. 候选空间在 benchmark 预算内可以合理探索；
4. 不需要 Agent 猜测缺失分子、反应物、连接关系或实验条件；
5. evaluator 能识别 paper-supported solution 以及科学等价替代方案；
6. 任务不会因为开放空间过大而变成不可验证的研究项目。

如果不满足：

- 不允许把 paper-selected candidates 改名后继续称为 discovery；
- 不允许代码生成 decoy candidates 或自动构造 mechanism；
- 不允许 Stage07 重建另一项任务；
- 整个双模式 pair 应科学拒绝，或者未来产品层面允许只发布 reproduction。

在当前“两种模式必须成对发布”的前提下，建议采用严格策略：只要 autonomous discovery
不闭合，该论文不发布任务对。这会降低发布率，但能保证模式含义真实。

## 6. Stage06 新工作流

仍保持一个 Stage06 Agent 连续完成任务，暂不恢复独立 converter 或 conversion retry。

### 6.1 第一步：建立共同科学问题

Agent 先确定：

- scientific objective；
- initial physical system；
- observable or conclusion to determine；
- pre-discovery information boundary；
- 哪些 source facts 属于作者后验发现。

### 6.2 第二步：建立简约 disclosure inventory

在 private `workflow_review.json` 中维护三个列表即可，不增加复杂 schema：

```json
{
  "disclosure_inventory": {
    "shared_public": [],
    "reproduction_only": [],
    "evaluator_only": []
  }
}
```

含义：

- `shared_public`：研究开始前即可获得的信息；
- `reproduction_only`：作者候选、机理和路线；
- `evaluator_only`：数值答案、正确排序、最终结论和 tolerance。

这个 inventory 由 Agent 科学判断，不由代码按关键词生成。

### 6.3 第三步：完整构建 reproduction

按照作者候选和 paper route 完成：

- `task.md`；
- public inputs；
- `submission_schema.json`；
- evaluator；
- self-check。

reproduction self-check 除机械合同外，Agent 还需确认没有把 evaluator-only 数值写进任何
public file。

### 6.4 第四步：从空目录构建 autonomous

不再复制整个 reproduction directory。Agent 应：

1. 创建空的 autonomous task package；
2. 只从 `shared_public` 重建 task 和 data；
3. 删除 paper-selected candidates、route、mechanism、conclusion 和 negative hints；
4. 将任务从“执行候选”改为“提出并验证候选”；
5. 独立设计 submission schema 和 evaluator；
6. 检查任务在公开输入下是否仍可执行。

同一个 Agent 可以参考自己已完成的 reproduction 来理解科学问题，但不能把 reproduction
当作文件模板直接复制。先用这一简单设计测试；只有多轮仍出现严重泄露时，再考虑增加一个
只看到 sanitized brief 的独立 autonomous task designer。

### 6.5 第五步：双模式自查

Agent 最后逐文件检查：

```text
task.md
submission_schema.json
public data filenames
public data comments and contents
```

检查：

- reproduction 是否意外公开 numeric answer/order/tolerance；
- autonomous 是否出现 paper candidate、mechanism、route 或 conclusion；
- autonomous evaluator 是否真的评分 candidate discovery，而不是复制 reproduction rules；
- 两个任务是否仍在回答同一上层科学问题。

Gate 仍只做机械检查，不接管上述语义判断。

## 7. 两种模式任务指令结构

两种 `task.md` 都保持四段，避免继续增加文件和关键词。

### 7.1 Reproduction

```text
1. Scientific objective
2. Author-proposed candidates/mechanism and public inputs
3. Paper-supported computational route and required validation
4. Deliverables
```

第二段允许公开作者选择的候选，但使用“需要复现验证的 paper-supported hypothesis”措辞，
不能把待计算数值写成已知答案。

### 7.2 Autonomous

```text
1. Scientific objective
2. Initial system and physical boundaries
3. Required autonomous investigation
4. Deliverables
```

第三段要求提出候选、设计搜索、验证和形成结论，但不规定具体软件和方法。

## 8. Autonomous submission schema 的最小设计

不同论文结果形式不同，不应设计化学专用固定字段。保持三个通用顶层概念：

```json
{
  "candidates": [],
  "calculations": [],
  "conclusion": {}
}
```

### `candidates`

记录 Agent 实际提出的候选，每项只需：

- local candidate ID；
- human-readable description；
- optional artifact path；
- why it was considered。

### `calculations`

记录候选对应的计算和验证证据：

- candidate ID；
- method summary；
- key numerical results；
- validation status；
- uncertainty or failure notes。

### `conclusion`

记录：

- selected candidate or mechanism；
- supporting evidence；
- rejected alternatives；
- uncertainty and unexplored space。

具体子字段仍由 Stage06 Agent根据任务定义，不在代码中强制所有化学任务使用同一 schema。

大型结构不要作为数百个 JSON object 嵌入主结果。submission schema 可以要求独立 XYZ、
CIF 或其他 artifact，并在 JSON 中记录路径。

## 9. Autonomous evaluator 设计

autonomous evaluator 不能由 reproduction evaluator 简单复制后放宽 tolerance。

仍使用现有五个文件，不增加新 evaluator 文件：

```text
reference_key_points.json
reference_conclusions.json
scoring_rules.json
critical_failures.json
evidence_map.json
```

### 9.1 应覆盖

- 是否提出至少一个 source-supported key candidate/mechanism；
- 是否覆盖关键竞争候选；
- 是否执行必要的物理/化学验证；
- 是否使用内部一致的比较尺度；
- 是否得到正确 ordering、condition 或结论；
- 是否给出合理替代机制；
- 是否诚实报告未收敛、未搜索或不确定部分。

### 9.2 不应要求

- 软件和路线必须与论文相同；
- 不同方法下无必要复现的绝对 total energies；
- 与论文虚频或绝对能量过度接近；
- 候选描述必须逐字匹配论文命名；
- 只有 paper answer 才能得分，而不允许科学等价结果。

### 9.3 规则类型

不新增大量 rule type。现有类型足够：

- `numeric`：关键可比较量；
- `ordering`：候选或路径相对顺序；
- `condition`：候选覆盖、validation、收敛和必要产物；
- `semantic`：机制等价性、结论和科学解释。

Gate 只检查规则可执行，不判断 tolerance 或机制是否科学最优。

## 10. Stage07 新审计职责

Stage07 仍只审计和有限修复，不重建 Stage06 失败任务。

### 10.1 Reproduction 审计

- 作者候选和 paper route 是否 source-supported；
- 是否公开了不应公开的 numeric answer、ordering 或 tolerance；
- schema 是否通过 `const`、`enum`、example/default 泄露答案；
- evaluator 是否覆盖 route fidelity、关键计算节点和最终结果。

### 10.2 Autonomous 审计

- public inputs 是否真的是 pre-discovery inputs；
- 是否仍含 paper-selected TS/product/rotamer/mechanism；
- 文件名和注释是否泄露 source labels；
- 是否要求 Agent 实际提出候选和 search strategy；
- 是否在现有输入和预算内可完成；
- evaluator 是否评分 discovery，而不是复制 reproduction numeric targets；
- 是否允许科学等价替代发现。

### 10.3 Pair 审计

两种模式不再要求相同 public files，只要求：

- 同一上层 scientific objective；
- 同一初始物理体系；
- reproduction 多公开作者后验信息；
- autonomous 不改变问题，只撤去作者后验信息并增加自主发现职责。

### 10.4 有限修复边界

Stage07 可以：

- 删除遗漏的 route/answer hint；
- 修复少量 schema answer leakage；
- 调整个别 evaluator rule；
- 修正少量 public filename/comment。

Stage07 必须拒绝：

- autonomous public inputs 本质上仍是 paper-selected answer；
- 缺少 pre-discovery initial system；
- 需要重新选择科学目标；
- 需要重新生成候选集合或完整 evaluator；
- discovery scope 超出预算且无法小范围修复。

## 11. Gate 边界

Gate 继续保持最小机械职责，不增加机理、候选或论文路线关键词规则。

可以阻断：

- 必需文件缺失；
- JSON/schema/binding 不可解析；
- evaluator 空模板；
- PDF/SI 或大段 source material 出现在 agent input；
- public data artifact 与 manifest 不一致。

不阻断：

- 某个候选是否属于 paper answer；
- 某句话是否泄露机理；
- autonomous search 是否科学充分；
- tolerance 是否适合某种方法。

这些由 Stage06/07 语义审计和人工复核负责。

## 12. v20 其他问题的处理方案

### 12.1 Public schema 答案泄露

Stage06/07 Prompt 明确检查 `const`、`enum`、example 和 default 是否编码 reference answer。
不在 Gate 中禁止所有 `const/enum`，因为合法类别约束仍需要它们。

### 12.2 Autonomous evaluator 过度复制

autonomous 必须从 scientific discovery criteria 独立编写 evaluator。Prompt 禁止只修改
reproduction tolerance 后直接使用。

### 12.3 Stage07 receipt 与真实 diff 不一致

代码机械计算 candidate 与 audited task 的 `changed_files`。Agent 仍写 scientific reason；
发布前检查 receipt 路径是否覆盖真实 diff。这不介入科学判断。

### 12.4 Stage07 `rm -rf` 被 sandbox 拒绝

编排器在 Agent 启动前把 candidate 安全复制到 `outputs/audited_task/`。Stage07 只修改现有
副本，不再自行删除和复制目录。

### 12.5 不可用 PDF 工具和无效安装

- Prompt 明确现成 `document_query.py` 是首选；
- 明确不要安装 PDF 包；
- query 增加通用 page-range；
- 不加入化学专用解析。

### 12.6 Metadata 文本问题

canonical metadata 层增加 HTML unescape、Unicode NFC 和明确排版空格清理，不猜测作者
姓名，不写论文特例。

### 12.7 大型 JSON 交付

允许 submission schema 将结构、轨迹和大矩阵作为独立 artifact；主 JSON 只保存路径、
摘要、关键数值和 validation 状态。

## 13. 当前四篇任务按新定义的预期

### `paper_2aca...`

- reproduction：可以公开 Bergman candidate pathway 和 QST3/IRC route，但不能公开正确
  barrier ordering；
- autonomous：只给 reactant structures 和目标，要求提出并验证可能的 cyclization path；
- 是否可构建取决于候选路径搜索能否在预算内闭合。

### `paper_611...`

- reproduction：可以公开 ISO-1/ISO-2 rotamers 和 TD-DFT route；
- autonomous：如果目标是自主发现 bright conformers，应给完整、唯一的 molecular model
  和合理 conformer-search starting point，不能只给论文挑出的两个 bright rotamers；
- 当前 source 的 31 原子模型代表性和初始构象边界不足，按严格定义很可能应拒绝。

### `paper_76ae...`

- reproduction：继续给两个 TS2 candidates 和论文双层路线；
- autonomous：应给 reactant/catalyst/substrate starting structures，要求提出 competing
  ring-opening mechanisms 和 TS candidates；
- 当前只有 paper-selected TS geometries，若原始 reactant complex 无法唯一恢复，应拒绝
  autonomous，而不是给 TS 改名。

### `paper_9455...`

- reproduction：给 P1/P2 和 CBS-QB3 route；
- autonomous：只给 SiN、isoprene、H-loss boundary 和预算，要求提出 product candidates；
- 论文实际探索 38 个 isomers，完整 search 可能过于昂贵。Stage06 应评估能否设计一个仍然
  有意义且预算闭合的 candidate-generation task，否则拒绝。

这意味着新标准下发布率可能低于 v20，但模式差异和 benchmark 解释力会明显提高。

## 14. 预期代码修改范围

用户确认后，代码计划应覆盖：

- `src/stages/stage06_task_builder/prompts.py`
  - 新双模式定义；
  - disclosure inventory；
  - reproduction-first 但 autonomous 从空目录构建；
  - pre-discovery input closure；
  - 独立 autonomous evaluator。

- `src/stages/stage07_task_judge/prompts.py`
  - reproduction answer leakage audit；
  - autonomous candidate/mechanism/route leakage audit；
  - 不同 public inputs 下的 pair consistency；
  - discovery evaluator coherence。

- `src/stages/stage07_task_judge/stage.py`
  - Stage07 启动前安全预复制 candidate；
  - 机械记录真实 changed files；
  - 不新增科学判断。

- `src/stages/pdf_layout.py`
  - 通用 page-range query。

- `src/stages/paper_metadata.py`
  - 通用 HTML/Unicode normalization。

- `src/stages/phase_gate.py`
  - 原则上不增加科学规则；
  - 仅在两种模式 public inputs 不同导致现有机械假设冲突时做最小调整。

- tests
  - 双模式不同 public inputs 合法；
  - reproduction schema 不公开答案；
  - autonomous 不含 paper-selected candidates/route；
  - Stage07 changed-files receipt 一致；
  - benchmark runner 仍只物化 `agent_input/`。

## 15. 测试方案

先用通用 fixtures：

1. reproduction 有 paper TS，autonomous 只有 reactants：合法 pair；
2. autonomous 复制 paper TS：Stage07 scientific rejection；
3. reproduction schema 用 `const` 写正确 ordering：Stage07 发现并修复；
4. autonomous evaluator 只复制 reproduction target/tolerance：Stage07 发现；
5. autonomous initial inputs 不足以生成候选：Stage06 scientific rejection；
6. autonomous candidate space 超预算：Stage06 scientific rejection；
7. 两种 public input 不同但 scientific core 一致：Gate 正常通过；
8. receipt repairs 与真实 diff 不一致：机械 provenance 检查发现；
9. source material 进入任一 agent input：Gate 阻断；
10. 大型结构使用独立 artifact：submission binding 正常。

固定 fixture 通过后再选择少量真实论文测试，不以“必须发布五篇”为目标，而以模式语义是否
真实为目标。

## 16. 验收标准

1. reproduction 明确公开作者候选、机制假设和 paper route；
2. reproduction 不公开待评分数值、正确排序、最终答案和 tolerance；
3. autonomous 不包含作者候选、机理、route、结论和 negative hints；
4. autonomous public inputs 是 pre-discovery inputs；
5. autonomous 明确要求提出候选、search、validation 和 conclusion；
6. 两种模式可以使用不同 public inputs，但回答同一上层问题；
7. autonomous evaluator 不由 reproduction evaluator 简单复制；
8. evaluator 允许科学等价候选或机制；
9. Stage07 只能有限修复，不能重建不可构建 discovery task；
10. Gate 不增加论文、化学或 tolerance 规则；
11. 生产代码无 paper/compound/task-direction 特例；
12. Stage07 receipt 与真实文件 diff 一致；
13. runner 仍只向被评测 Agent 物化 `agent_input/`；
14. 单元、定向和真实任务审查均有报告。

## 17. 最终建议

建议采用该方向，但将其表述为：

```text
reproduction = author-guided hypothesis and route reproduction
autonomous = pre-discovery input driven candidate/mechanism discovery
```

不要继续把 reproduction task package 整体复制成 autonomous，也不要通过简单删除方法名来
声称已经完成自主科研转换。

该修改会减少可发布论文数量，并提高 Stage06 对 pre-discovery inputs 和搜索预算的判断
要求；这是获得真实模式差异必须付出的成本。优先保证任务语义真实，而不是维持表面上的
一篇论文两个任务通过率。

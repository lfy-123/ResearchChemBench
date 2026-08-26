# Stage06/07 v22 双模式科学评估任务内容修改方案

## 1. 文档状态与本轮范围

本文件是待用户确认的设计方案。本轮不修改生产代码，不提交新测试任务。

本版优先解决评估任务本身的科学含义和内容组织：

- `paper_reproduction` 应评估能否用计算证据复现论文作者提出的假设、候选或机理；
- `autonomous_research` 应评估能否从研究前输入出发，自主提出候选、搜索并验证机理；
- 两个模式不能只通过“是否指定计算方法”来区分；
- `task.md`、public inputs、submission contract 和 evaluator 必须一起随模式变化。

上一轮发现的 schema 答案泄露、evaluator 复制、未定义布尔判断、大型 JSON、Stage07
审计记录和工具效率问题也在本方案中给出处理位置，但这些是配套改进，不改变本版的主线。

## 2. 当前设计与目标设计的根本差异

### 2.1 当前实际设计

当前 Stage06 的主要流程是：

1. 先构建完整的论文复现任务；
2. 对论文复现任务执行自查；
3. 把稳定的复现任务复制为 autonomous 的起点；
4. 删除论文软件、方法和路线；
5. 让 autonomous Agent 自主选择方法。

因此，当前实际能力边界更接近：

```text
paper_reproduction = 给定论文候选 + 给定论文路线 + 计算验证
autonomous_research = 给定论文候选 + 自主选择路线 + 计算验证
```

上一轮发布任务中：

- `paper_76ae...` 的 autonomous 已获得两个论文选定的 TS2；
- `paper_9455...` 的 autonomous 已获得论文选定的 P1/P2；
- `paper_611...` 的 autonomous 已获得论文筛选出的两个 bright rotamers；
- `paper_2aca...` 的 autonomous 已获得明确反应中心和目标环化过程。

这些任务能够评估方法选择和计算验证，但不能充分评估候选提出或机制发现。

### 2.2 目标设计

新版能力边界应为：

```text
paper_reproduction
  = 科学问题
  + 作者提出的假设/候选/机理
  + 作者计算路线
  + 重新计算并判断证据是否复现论文结论

autonomous_research
  = 同一上层科学问题
  + 研究开始前可获得的初始体系和物理边界
  + 自主提出候选/机理
  + 自主选择搜索和验证路线
  + 独立形成结论
```

两个模式评估的是两个不同层次的能力：

- reproduction：作者引导下的科学证据复现；
- autonomous：不知道作者答案时的候选和机制发现。

## 3. 两种模式共享什么、差异是什么

两种模式共享的不是完全相同的文件，而是同一个上层科学问题。

### 3.1 必须共享

- 同一研究体系；
- 同一需要回答的科学问题；
- 同一类可观察量或最终科学判断；
- 不冲突的电荷、自旋、环境、温度和组成边界；
- 相同或可比较的资源预算。

### 3.2 允许不同

- public input 文件；
- 是否提供作者选择的候选和后验结构；
- 是否指定计算路线；
- submission schema 中的过程字段；
- evaluator 的评分重点和数值容差。

### 3.3 不允许的伪差异

以下变化不足以构成自主科研模式：

- 只删除 Gaussian、B3LYP、CBS-QB3 等方法名；
- 把论文候选从 `TS2-R-S` 政名为 `candidate_A`；
- 保留论文 TS/product/rotamer，只让 Agent 自己选方法；
- 复制 reproduction evaluator 后只放宽 tolerance；
- 在任务说明中加入“independent”或“autonomous”，但不改变候选发现职责。

## 4. 科学信息边界

Stage06 Agent 需要在构建任务前完成一次简约的信息分类。该分类放在 private
`workflow_review.json` 中，不进入被评测 Agent 的输入。

```json
{
  "disclosure_inventory": {
    "shared_public": [],
    "reproduction_only": [],
    "evaluator_only": []
  }
}
```

### 4.1 `shared_public`

研究开始前可以获得，并可用于两个模式的信息：

- 反应物、催化剂、底物或基础分子结构；
- 已知实验组成、反应环境和状态边界；
- 任务需要解释的实验现象；
- 如果实验在计算研究之前已确认，可包括实验产物或选择性；
- 不包含作者计算后才确定的候选或机制。

实验结果能否公开取决于任务定义：如果目标是用计算解释已知实验现象，可以公开；如果目标
是盲预测该实验结果，则必须隐藏。不能因为某条信息出现在论文中就自动判定其公开性。

### 4.2 `reproduction_only`

只在论文复现模式中公开：

- 作者提出的机理假设；
- 作者选择的候选产物、构象、反应通道或 TS；
- 执行论文路线所需的候选结构和 route-specific starting guess；
- 作者的软件、方法、basis、solvation、thermochemistry 和有序计算过程；
- 作者要求执行的 frequency、IRC、state tracking 等验证步骤。

### 4.3 `evaluator_only`

两个模式均不公开：

- 待重新计算的关键数值；
- 正确能量、性质或候选排序；
- hidden reference conclusion（除 reproduction 中作为待验证假设公开的定性作者主张外）；
- evaluator key points、scoring rules 和 tolerance；
- 可以直接代替计算的最终结构或结果文件。

### 4.4 论文复现模式中“公开论文结论”的边界

论文提出的候选或机理可以作为待验证的作者假设公开，例如：

```text
论文提出路径 A 控制该选择性。请重新计算关键候选，判断你的计算证据是否复现并支持该解释。
```

但不能同时公开：

```text
路径 A 比路径 B 低 1.9 kcal/mol，允许误差 0.6 kcal/mol，因此 A 必须胜出。
```

前者公开了被复现的科学主张；后者公开了待评分答案和评分尺度。论文复现模式的结论评分
不能只看 Agent 是否重复一句“支持路径 A”，而要绑定其实际计算、验证和数值证据。

## 5. `paper_reproduction` 任务的完整设计

### 5.1 模式目标

给定论文作者的科学假设、候选或机理以及论文计算路线，要求被评测 Agent 重新执行关键计算，
验证候选身份，复现关键数值或趋势，并判断自己的计算证据是否支持论文结论。

它不是纯软件操作题，也不是把论文步骤逐行转换成命令。每一个计算步骤都应服务于一个明确
的科学判断。

### 5.2 `task.md` 固定为四个逻辑部分

#### 1. Scientific question

说明：

- 研究体系和现象；
- 论文试图回答的科学问题；
- 需要被重新验证的最终科学判断。

不在这一部分提前给出待评分数值。

#### 2. Author-proposed hypothesis and candidates

说明：

- 作者提出了什么机理或解释；
- 作者选择了哪些候选进行验证；
- 候选之间的科学关系；
- 哪些输入结构对应这些候选。

候选应被表述为“需要重新计算验证的作者假设”，而不是不可质疑的正确答案。

#### 3. Paper-supported computational investigation

说明：

- 论文使用的软件和模型化学；
- 有序计算过程；
- 每个计算节点需要验证什么；
- 能量、自由能、光谱或动力学量如何组装和比较；
- 论文没有明确说明的设置应如实标记，不得由合成 Agent 编造成论文事实。

路线描述应把操作与科学目的关联，例如：

```text
对两个 TS candidate 进行频率分析，以验证它们是否都是同一反应事件的一阶鞍点；随后在同一
热化学和溶剂模型下比较自由能，判断作者提出的选择性来源能否被复现。
```

#### 4. Required evidence and deliverables

要求提交：

- 方法和实际运行设置；
- 收敛和状态验证；
- 关键中间数值；
- 最终比较结果；
- 计算证据是否支持论文假设；
- 偏离论文结果时的证据化说明。

### 5.3 Public inputs

reproduction 可以包含：

- 两种模式共享的初始结构；
- 作者选择的 candidate、TS、intermediate、rotamer 或 product；
- 论文路线执行所需且不会直接给出结果的输入 deck/starting guess；
- 必要且经过最小提取的结构、组成和边界信息。

不复制 PDF、SI、整篇 Markdown 或包含大段论文解释的 source artifact。

### 5.4 Submission contract

submission schema 根据任务定义具体字段，但至少覆盖三个语义部分：

- `calculations`：关键计算和验证证据；
- `results`：关键数值、比较和排序；
- `conclusion`：是否复现并支持作者假设及其依据。

这三个是内容概念，不要求所有论文强制使用完全相同的 JSON 字段名。

不允许 schema 用 `const`、单元素 `enum`、带答案的 `default/example` 写入正确数值、排序或
结论。合法的单位、状态类别和文件类型约束仍可使用 `enum`。

### 5.5 Reproduction evaluator

应覆盖：

- 作者路线中的关键执行节点；
- candidate identity 和必要 stationary-state/state validation；
- 可复现的关键数值；
- 路径或候选排序；
- 最终结论是否由提交的计算证据支持。

不能把“结论字符串与论文一致”单独作为主要得分。结论规则必须绑定计算结果和验证证据。

## 6. `autonomous_research` 任务的完整设计

### 6.1 模式目标

在不知道论文候选、机理和计算路线的条件下，从研究前输入和科学问题出发，自主提出候选，
设计搜索和验证策略，比较候选并形成结论。

自主性至少同时包含：

- hypothesis/candidate autonomy；
- search-strategy autonomy；
- method autonomy；
- evidence interpretation autonomy。

如果任务只满足 method autonomy，应诚实归类为 validation/comparison，不得发布为本版定义
下的 `autonomous_research`。

### 6.2 `task.md` 固定为四个逻辑部分

#### 1. Scientific question

与 reproduction 保持同一上层问题，但不提“论文”“作者”“复现”“与论文不同的方法”等
来源痕迹。

#### 2. Initial system and physical boundaries

仅说明：

- pre-discovery starting structures；
- 组成、电荷、自旋、环境、温度等必要边界；
- 已知实验约束；
- 搜索空间边界和计算预算。

如果已知产物来自研究前实验事实，可以提供产物并要求发现路径/TS；如果产物本身是论文计算
发现，则不能公开。

#### 3. Required autonomous investigation

明确要求被评测 Agent：

1. 提出一个以上科学合理的候选、机理、构象或通道；
2. 说明候选生成和搜索策略；
3. 选择并论证计算模型；
4. 对关键候选执行结构、状态、频率、路径或其他适用验证；
5. 在内部一致的尺度上比较候选；
6. 形成结论并说明淘汰候选的依据；
7. 报告没有覆盖的空间、失败计算和不确定性。

具体任务可以只要求其中适用的步骤，但不能只要求“选择方法后计算两个已给定候选”。

#### 4. Required evidence and deliverables

要求交付：

- Agent 实际提出的候选及本地 ID；
- 候选结构 artifact 或可复现描述；
- 搜索和筛选过程；
- 每个关键候选的计算和验证证据；
- 比较结果、最终结论和不确定性。

### 6.3 Public inputs

autonomous 只能包含 `shared_public` 内容，例如：

- 分离的反应物、催化剂和底物；
- 未被论文后验筛选的基础结构或初始构象；
- 必要物理边界；
- 与任务定义一致的实验条件。

不能包含：

- 论文选定的 TS、product、intermediate 或 bright rotamer；
- 暴露作者结论的文件名、结构注释或编号；
- paper route input deck；
- “不要考虑暗态结构”一类负向答案提示。

### 6.4 Submission contract

保持简单且可适配不同计算化学任务，使用三个顶层内容概念：

```json
{
  "candidates": [],
  "calculations": [],
  "conclusion": {}
}
```

- `candidates`：候选 ID、描述、提出理由和可选 artifact path；
- `calculations`：候选关联、方法摘要、关键结果、validation 和失败信息；
- `conclusion`：选定候选/机理、支持证据、淘汰候选和不确定性。

具体子字段仍由 Stage06 Agent根据任务确定，代码不写统一化学 schema。

大型坐标、轨迹和矩阵应作为独立 XYZ/CIF/文本 artifact；主 JSON 只记录路径、摘要、关键数值
和验证状态。

### 6.5 Autonomous evaluator

必须独立围绕 discovery 能力设计，不能复制 reproduction evaluator 后只改 tolerance。

应覆盖：

- 是否提出论文支持的关键候选或科学等价候选；
- 是否覆盖主要竞争假设；
- candidate generation/search 是否有科学依据；
- 必要的物理和化学验证是否完成；
- 比较是否使用内部一致的尺度；
- ordering、condition 或关键趋势是否正确；
- 结论是否由计算证据支持；
- 是否诚实报告失败和未搜索空间。

不应机械要求：

- 软件和路线与论文一致；
- 合理替代方法下不稳定的绝对 total energy；
- 虚频与论文逐数值接近；
- 候选名称逐字匹配论文；
- 只有论文命名的唯一机理才能得分。

如果允许方法自由，应主要评分稳定的相对量、趋势、物理有效性和内部一致性。numeric target
仍应正常生成 target、unit 和初始 tolerance，但 Stage06 Agent 必须解释为什么这个量在允许的
方法空间内仍可比较。

## 7. Stage06 Agent 的新职业与 Prompt 结构

### 7.1 职业定义

建议把开头改为：

```text
You are a computational-chemistry benchmark research director and paired-task architect.
From one paper, identify a central, computationally testable scientific question and design two
complete evaluation tasks around it: an author-guided evidence-reproduction task and a
pre-discovery candidate/mechanism-discovery task. You are responsible for the scientific scope,
public inputs, submission contracts, hidden evaluators, and the internal consistency of both tasks.
```

Prompt 不写“Stage06”“后续 Stage07 会修复”或“后续人工会补 evaluator”。Agent 应把当前工作
理解成任务正式完成前的最后构建职责。

### 7.2 工作顺序

#### A. 识别科学问题

从论文中选择一个中心、非平凡、可计算且有明确证据的科学问题。先判断它更接近：

- 机制/候选发现；
- 选择性或排序解释；
- 结构/状态识别；
- 性质或现象解释；
- 其他可验证计算问题。

这里是语义分类，不增加代码枚举或特殊分支。

#### B. 建立 private scientific brief

记录：

- scientific question；
- pre-discovery initial system；
- paper hypothesis/candidates/mechanism；
- paper route；
- paper-supported results and conclusion；
- disclosure inventory；
- autonomous constructibility and budget assessment。

#### C. 完整构建 reproduction

按第五节完成 task、inputs、submission schema 和 evaluator。完成后运行 reproduction self-check，
读取报告并修复机械问题。

#### D. 独立构建 autonomous

逻辑上以同一 scientific brief 为来源，但从空的 autonomous 目录构建：

- 只使用 `shared_public`；
- 不复制 reproduction 的 task、schema、data 或 evaluator；
- 重新写 candidate/search-oriented task；
- 重新判断 public input closure；
- 独立写 submission schema 和 evaluator。

同一个 Agent 可以先完成 reproduction 以保证科学理解，但“转换”是从共同科学问题重新设计，
不是目录级复制和删词。

#### E. 双模式语义自查

Agent 必须逐一检查：

```text
task.md
submission_schema.json
public data filenames
public data comments and file contents
task_info descriptions
evaluator key points/conclusions/rules
```

并明确回答：

1. reproduction 是否公开作者假设和路线，但隐藏待评分数值、排序和 tolerance？
2. autonomous 是否完全移除了作者候选、机制、路线和后验结构？
3. autonomous 是否真的要求提出候选和搜索，而不只是自主选方法？
4. 两个任务是否仍回答同一上层科学问题？
5. 两个 evaluator 是否分别适配 evidence reproduction 和 discovery？

#### F. 机械自查

最后运行现有统一 Gate，修复必需文件、JSON、binding、manifest 和 evaluator 完整性问题。
机械 Gate 通过后才写 terminal receipt。

## 8. Stage06 Prompt 中需要删除或替换的现有表述

删除当前含义：

```text
copy the stable reproduction task as the starting point for autonomous research
```

替换为：

```text
Construct autonomous_research independently from the shared scientific question and
pre-discovery inputs. Start from an empty task directory. Do not copy the reproduction task,
submission schema, public candidate files, or evaluator. The autonomous task must require the
evaluated Agent to propose and validate candidates or mechanisms, not merely select a method for
paper-selected candidates.
```

把当前 autonomous 定义：

```text
let the evaluated Agent choose and justify methods, search strategy and analyses
```

扩展为：

```text
require the evaluated Agent to formulate candidate hypotheses, design a bounded search,
select methods, validate the candidates, compare alternatives and form an evidence-backed
conclusion without access to the paper-selected candidates or route.
```

把 reproduction 从“完全披露 route”扩展为：

```text
state the scientific question and the author-proposed hypothesis/candidates first, then disclose
the paper-supported computational route as the means to reproduce and test that claim. Every
required calculation must support a stated scientific validation or comparison.
```

## 9. Stage07 的配套审计职责

Stage07 仍是审计和有限修复 Agent，不重建 Stage06 失败任务。

### 9.1 Reproduction 审计

- 科学问题是否中心且明确；
- 作者候选/机理是否有 source evidence；
- task 是否把路线与科学验证关联，而不是只列软件步骤；
- public task/schema/data 是否泄露 numeric result、正确排序或 tolerance；
- evaluator 是否同时覆盖过程证据和最终结果。

### 9.2 Autonomous 审计

- public inputs 是否真的是 pre-discovery inputs；
- 是否仍含论文选定 TS/product/rotamer/mechanism；
- 文件名、注释、schema 是否泄露作者候选；
- 是否要求 Agent 提出候选、设计搜索和验证；
- 搜索空间是否在给定预算内闭合；
- evaluator 是否独立评分 discovery；
- 是否允许科学等价的候选或机制。

### 9.3 Pair 审计

- 两个模式是否回答同一科学问题；
- reproduction 是否比 autonomous 多公开作者后验信息；
- autonomous 是否没有通过删词改变成另一个更简单的问题；
- 两种 public inputs 不同是否有合理的 disclosure 原因；
- 两个任务是否各自可以在无论文/SI的条件下独立执行。

### 9.4 修复边界

Stage07 可以修复：

- 少量措辞或边界不清；
- 个别 schema answer leakage；
- 少量文件名或注释泄露；
- 个别 evaluator binding、rule 或 tolerance 表述问题。

Stage07 必须拒绝：

- autonomous 的核心输入仍是论文后验候选；
- 缺少构建自主任务所需的初始体系；
- 任务没有 candidate discovery 职责；
- evaluator 需要大规模重写；
- 搜索空间明显超出预算；
- 需要重新选择科学目标或重建任务。

## 10. Gate 的职责保持最小

Gate 只阻断：

- 必需文件缺失；
- JSON 或 schema 无法解析；
- submission binding 指向不存在的字段或 artifact；
- evaluator 是空模板或没有可执行规则；
- PDF/SI 或大段 source material 进入 Agent 输入；
- manifest 与实际 public artifact 不一致。

Gate 不判断：

- 某个结构是不是作者后验候选；
- 某句话是否泄露机制；
- autonomous 候选空间是否科学合理；
- 某个 tolerance 是否是唯一最佳值；
- 某个方法是否适合特定论文。

这些由 Stage06 self-review、Stage07 科学审计和最终人工审查处理。不添加论文、化合物或任务
类型特例，也不通过关键词黑名单替代科学审计。

## 11. 上一轮小问题的配套处理

### 11.1 Schema 直接泄露答案

问题：`paper_2aca...` 的 reproduction schema 用 `const` 固定正确 barrier ordering。

处理：

- Stage06 语义自查覆盖 schema、example、default 和 public data；
- Stage07 对照 hidden reference 检查整个 public surface；
- 不在 Gate 中全局禁止 `const/enum`，避免破坏合法 schema 约束。

### 11.2 Autonomous evaluator 复制 reproduction

问题：多篇 autonomous 仅复制 numeric target 并放宽 tolerance。

处理：

- Prompt 要求 autonomous evaluator 从 discovery criteria 独立编写；
- 每条 numeric rule 说明该量为何在自由方法下仍可比较；
- Stage07 单独回答 evaluator 是否与允许的自主性一致；
- 不用代码按任务类型自动改 tolerance。

### 11.3 未定义的主观布尔字段

问题：`both_bright`、`closely_similar` 等字段没有公开操作定义。

处理：

- 若任务要求布尔判断，task 必须给出可执行定义；或者
- submission 只要求原始 numeric result 和解释，由 evaluator 根据 hidden rule 评分；
- 不允许 schema 强制一个无法从 public contract 推导的结论字段。

### 11.4 大型 JSON 坐标输出

问题：126 原子结构被要求嵌入大量 JSON object，但 evaluator 不评分这些字段。

处理：

- 坐标、轨迹和大矩阵使用独立 artifact；
- JSON 保存 artifact path、摘要和关键验证；
- 只要求真正用于审计或评分的交付内容。

### 11.5 Source material 暴露

问题：Stage06 初稿曾把整份 SI-derived Markdown 放入 public data。

处理：

- Prompt 要求只提取完成任务所需的最小数据；
- self-check 和 external Gate 继续阻断 PDF/SI 或大段 source material；
- 不影响合法的、经过最小提取的结构或数值输入。

### 11.6 Stage07 receipt 与真实修改不一致

处理：代码机械计算 candidate 与 audited output 的 changed-file list；Agent 只解释修改原因。
这是 provenance 修复，不介入科学判断。

### 11.7 Stage07 目录复制命令冲突

处理：编排器在启动 Stage07 前准备好 audited candidate 副本；Agent 只修改该副本，不执行
`rm -rf` 或重建目录。

### 11.8 文档工具探测和 metadata

这些属于低优先级配套项：

- Prompt 明确使用现有 `document_query.py`，不安装 PDF 包；
- document query 后续补通用 page-range；
- metadata 后续统一做 HTML unescape 和 Unicode NFC。

它们不与双模式内容修改绑定，可在主任务完成后单独提交和验证。

## 12. 四篇现有任务在新版定义下应如何变化

### 12.1 `paper_2aca...`

Reproduction：

- 公开 Bergman cyclization hypothesis、作者候选和 QST3/frequency/IRC route；
- 要求复现 barrier、ordering 和 transition-state stabilization 解释；
- 不在 schema 中写入正确 ordering。

Autonomous：

- 从 reactant 和可公开的实验/结构边界出发；
- 要求提出可能的 cyclization path、product/TS candidate 并验证；
- 只有当 C17-C32 和 1,4-diradical 是研究前已知目标时才公开，否则也应隐藏；
- 如果搜索空间无法在预算内闭合，应拒绝 autonomous。

### 12.2 `paper_611...`

Reproduction：

- 公开作者的 ISO-1/ISO-2 候选、bright-state hypothesis 和 TD-DFT route；
- 要求重新优化、state tracking 和复现 emission 结论；
- 不把 brightness 作为无需验证的事实。

Autonomous：

- 应提供未被论文后验筛选的、完整且唯一的 molecular model/starting ensemble；
- 要求自主进行 conformer/state search，发现 emissive structures；
- 不能只提供两个论文 bright rotamers；
- 若现有 31 原子输入不能定义真实搜索起点，应科学拒绝。

### 12.3 `paper_76ae...`

Reproduction：

- 公开作者提出的 TS2-R-S/TS2-S-R candidates 和双层自由能路线；
- 要求重新验证 TS、复现 ΔΔG 并判断选择性解释。

Autonomous：

- 只提供可唯一确定的 catalyst/substrate/reactant starting system；
- 要求提出竞争的 sulfur-attack/ring-opening mechanisms 和 TS candidates；
- 不提供论文 TS2 coordinates 和 source labels；
- 若反应前体系无法从 source 唯一恢复，应拒绝。

### 12.4 `paper_9455...`

Reproduction：

- 公开论文 P1/P2 hypothesis 和 CBS-QB3 route；
- 要求复现 0 K thermochemistry 并判断是否支持 H-loss 解释。

Autonomous：

- 提供 SiN、isoprene 和可公开的 H-loss/实验边界；
- 要求提出 product candidates、筛选并比较；
- 不提供论文 P1/P2 structures；
- 论文探索 38 个 isomers，若无法形成预算闭合的搜索任务，应拒绝。

## 13. 一组完整的双模式任务示例

以下以 `paper_76ae...` 的选择性问题说明同一 scientific question 如何生成两个真正不同的
任务。示例只展示任务内容设计，不固定实际论文中的数值和文件名。

### 13.1 Reproduction task

```text
# 1. Scientific question

研究该手性磷酸催化体系中，竞争的硫进攻/oxetane 开环过渡态能否解释实验立体选择性。
重新计算作者提出的两个关键候选，并判断所得自由能证据是否复现论文的选择性解释。

# 2. Author-proposed hypothesis and candidates

作者提出两个具有不同立体排列的 TS candidate，它们代表通向相反 product sense 的竞争通道，
并假设二者的 solution-phase Gibbs free-energy difference 决定主要产物。输入目录提供两个作者
候选的起始几何和固定的结构身份。将其视为需要重新验证的假设，不要预设两者一定都是正确
的一阶鞍点。

# 3. Paper-supported computational investigation

使用论文披露的几何优化、频率、溶剂单点和热化学组装路线。分别验证两个候选是否对应同一
开环事件的一阶鞍点；在相同温度、标准态和溶剂模型下计算可比自由能；报告 signed ΔΔG，
并判断计算结果是否支持作者提出的 product-sense explanation。论文未明确的数值设置应记录
为运行选择，不能表述为论文事实。

# 4. Required evidence and deliverables

提交实际 route、收敛状态、虚频和 normal-mode assignment、component energies、assembled
free energies、signed comparison、product-sense conclusion，以及结论与计算证据的对应关系。
```

Reproduction public data 可以是：

```text
data/inputs/author_candidate_1.xyz
data/inputs/author_candidate_2.xyz
```

Hidden evaluator 评分：

- 两个作者候选是否被正确优化和验证；
- normal mode 是否对应目标反应事件；
- route 和自由能组装是否符合论文；
- ΔΔG、ordering 和 product sense 是否复现；
- 结论是否由提交证据支持。

公开任务中不写正确 ΔΔG、lower candidate、product sense 和 tolerance。

### 13.2 Autonomous task

只有在论文证据能唯一提供反应前体系时，才可以构建如下任务：

```text
# 1. Scientific question

确定该手性磷酸催化反应中硫进攻和 oxetane 开环的可行机理，识别决定立体选择性的竞争通道，
并预测主要 product sense。

# 2. Initial system and physical boundaries

输入目录提供分离的催化剂、底物和反应物结构，以及体系组成、电荷、自旋、溶剂、温度和计算
预算。没有预先提供过渡态、反应复合物、作者候选或产物排序。

# 3. Required autonomous investigation

提出合理的进攻方向、催化剂/底物相对构型和反应通道；设计有边界的构象与 TS candidate 搜索；
自主选择并论证计算方法；验证关键候选确实连接合理端点；在一致的自由能尺度上比较竞争通道；
据此预测 product sense，并报告被淘汰候选、未覆盖空间和不确定性。

# 4. Required evidence and deliverables

提交提出的候选清单和结构 artifact、候选生成与筛选说明、关键计算和 validation、可比自由能、
最终机制和 product-sense conclusion，以及限制和不确定性。
```

Autonomous public data 应是：

```text
data/inputs/catalyst.xyz
data/inputs/substrate.xyz
data/inputs/reagent.xyz
```

而不是 reproduction 的两个 TS 文件。

Hidden evaluator 评分：

- 是否提出 paper-supported 或科学等价的关键通道；
- 是否覆盖主要竞争立体排列；
- candidate search 和 validation 是否可信；
- free-energy comparison 是否内部一致；
- 是否发现正确趋势和 product sense；
- 是否合理处理替代机制和不确定性。

这组示例体现了真正的模式差异：reproduction 的研究对象是作者候选的证据复现；autonomous
的研究对象是从反应前体系发现候选和机理。二者回答同一选择性问题，但 public data、工作
内容、submission contract 和 evaluator 都不同。

## 14. 构建可行性与发布政策

不是每篇论文都同时适合两个模式。Autonomous 只有满足以下条件才可构建：

1. pre-discovery initial system 唯一且完整；
2. 去掉作者候选后科学问题仍然闭合；
3. 候选空间可在 benchmark 预算内合理探索；
4. 不要求 Agent 猜测缺失分子、连接关系或状态；
5. evaluator 能评价 paper-supported 和科学等价答案；
6. 任务不会退化成无限开放的真实研究项目。

当前按成对发布政策处理：任何一个模式科学上不可构建，整对任务拒绝。不能用降低 autonomous
定义或复制论文候选来维持发布率。

## 15. 预期代码修改范围

用户确认后制定单独的代码实施计划。预计涉及：

### 15.1 主体修改

- `src/stages/stage06_task_builder/prompts.py`
  - 重写职业定义和双模式语义；
  - reproduction 先构建；
  - autonomous 从空目录独立构建；
  - disclosure inventory；
  - 两种 evaluator 独立设计；
  - 全 public-surface 语义自查。

- `src/stages/stage07_task_judge/prompts.py`
  - author-guided reproduction 审计；
  - pre-discovery autonomous 审计；
  - evaluator independence；
  - pair scientific consistency；
  - 有限修复和拒绝边界。

- `src/stages/phase_gate.py`
  - 不增加科学规则；
  - 只移除“两种模式必须共享相同 public inputs”等与新设计冲突的机械假设，如当前仍存在。

### 15.2 配套修改

- `src/stages/stage07_task_judge/stage.py`
  - 预准备 audited copy；
  - 机械记录 changed files。

- document query 和 metadata
  - 在主体改动验证完成后作为独立小提交处理。

### 15.3 不做的修改

- 不恢复 Stage06B converter；
- 不恢复 conversion retry 或旧 resume；
- 不为特定论文/化合物写代码分支；
- 不让代码生成科学候选或统一预处理化学输入；
- 不设计大量新的 evaluator rule type；
- 不让 Stage07 重建 Stage06 失败任务。

## 16. 测试计划

### 16.1 Prompt/fixture 测试

1. reproduction 公开 paper TS 和 route，但不公开 numeric result/order/tolerance；
2. autonomous 只有 reactants，要求 candidate generation/search/validation；
3. 两种 public inputs 不同但 scientific question 相同；
4. autonomous 复制 paper TS 时由 Stage07 科学拒绝；
5. reproduction schema 用 `const/default/example` 写答案时能在语义审计中发现；
6. autonomous evaluator 复制 reproduction target/tolerance 时能被审计发现；
7. autonomous initial inputs 不闭合时 Stage06 科学拒绝；
8. autonomous 搜索空间超预算时 Stage06 科学拒绝；
9. 大型结构作为独立 artifact 时 binding 正常；
10. Gate 仍只阻断机械合同和 source-material exposure。

### 16.2 真实论文回归

优先使用上一轮已发布的四篇加一篇既有候选，以同样模型和并发设置重跑。不能只统计 Gate
通过率，应逐篇审查：

- reproduction 是否是科学假设复现而非操作步骤列表；
- autonomous 是否不含论文候选、机制、route 和后验结构；
- autonomous 是否要求候选生成和搜索；
- 两种任务是否回答同一科学问题；
- public inputs 是否分别闭合；
- evaluator 是否完整、具体、可执行并适配模式；
- Stage07 是否发现并处理语义问题；
- 科学拒绝是否有证据且符合新版边界。

### 16.3 不以发布率作为唯一成功指标

新版可能把部分旧发布任务判定为 autonomous 不可构建。验收重点是模式真实性和任务质量，
而不是维持“四篇发布”或“五篇发布”的表面结果。

## 17. 验收标准

1. reproduction 先写科学问题和作者假设，再写用于验证的论文路线；
2. reproduction 的每个主要计算步骤都对应科学验证目的；
3. reproduction 不公开待评分数值、正确排序和 tolerance；
4. autonomous 不公开作者候选、机制、方法、route 和后验结构；
5. autonomous 明确要求候选提出、搜索、验证、比较和结论；
6. 两个模式回答同一上层科学问题，但可以使用不同 public inputs；
7. autonomous public inputs 是研究前输入且足以执行；
8. 两种 submission contract 与各自任务职责一致；
9. reproduction evaluator 评分证据复现，autonomous evaluator 评分 discovery；
10. evaluator 完整、具体、可执行，不是空模板；
11. evaluator 不因方法自主而机械复制论文绝对量和 tolerance；
12. Stage06 自查覆盖 task、schema、data 和 evaluator；
13. Stage07 能审计双模式语义并只做有限修复；
14. Gate 保持最小机械职责；
15. 生产代码没有论文、化合物或机理关键词特例；
16. 被评测 Agent 在两个模式中都看不到 PDF/SI 和 hidden evaluator。

## 18. 建议实施顺序

用户确认本方案后：

1. 先写详细代码修改计划；
2. 只重写 Stage06/07 Prompt 和必要的 pair/Gate 假设；
3. 增加双模式内容 fixtures；
4. 完成主体测试；
5. 再处理 receipt、目录预复制和大型 artifact 等配套项；
6. 工具便利性和 metadata 作为最后的小提交；
7. 对照本方案逐项验收；
8. 再提交真实论文测试并形成逐篇质量报告。

本版最重要的设计原则是：

```text
论文复现模式公开作者假设和路线，评估能否用计算证据复现论文发现；
自主科研模式只公开研究前问题和输入，评估能否自主提出并验证候选或机理。
```

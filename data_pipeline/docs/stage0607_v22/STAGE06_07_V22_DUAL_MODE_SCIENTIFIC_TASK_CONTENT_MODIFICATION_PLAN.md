# Stage06/07 v22 双模式科学评估任务内容修改方案（更正版）

## 1. 文档状态与范围

本文件是根据双模式边界讨论重新整理的待确认方案。本轮只更正设计，不修改生产代码，不提交
测试任务。

本版优先解决评估任务本身的内容：

- 两种模式怎样围绕同一科学问题构建；
- 论文复现模式可以获得什么作者提示；
- 自主科研模式需要多承担哪一层科研职责；
- 哪些结构、结果、方法和评价信息必须隐藏；
- task、public inputs、submission contract 和 evaluator 如何保持一致。

上一轮测试发现的 schema 答案泄露、evaluator 不匹配、主观布尔字段、大型 JSON、Stage07
记录和工具效率问题作为配套项处理，不改变本版主体。

## 2. 最终模式定义

### 2.1 `paper_reproduction`

```text
科学目标
+ 作者给出的科学路线
+ 必要的研究前输入和科学边界
+ Agent 自主规划计算路线
+ 计算、验证并判断能否复现论文发现
```

这里的“作者科学路线”可以是：

- 作者提出的假设；
- 作者考虑的候选方案；
- 作者发现或主张的定性机理；
- 作者认为需要比较的科学解释；
- 作者给出的定性因果关系或研究方向。

它不是论文的软件、模型化学和有序计算步骤。

### 2.2 `autonomous_research`

```text
相同科学目标
+ 必要的研究前输入和科学边界
+ Agent 自主提出科学路线（如果问题存在假设空间）
+ Agent 自主规划计算路线
+ 计算、验证并形成结论
```

### 2.3 两种模式原则上的核心差异

```text
paper_reproduction：公开作者科学路线
autonomous_research：不公开作者科学路线
```

两种模式都不公开论文详细计算 protocol，两种模式都要求被评测 Agent 自主选择和论证计算
方法。

如果一篇论文没有真实的假设、候选或机理空间，两种模式可以非常接近。不得为了制造差异而
虚构候选、机理或额外科研问题，也不得仅因缺少假设空间而拒绝纯计算任务。

## 3. 四层信息模型

所有任务先按四层信息理解，避免继续混淆“科学路线”和“计算路线”。

| 层次 | 内容 | Reproduction | Autonomous |
|---|---|---|---|
| 科学目标 | 要回答什么科学问题 | 公开 | 公开 |
| 作者科学路线 | 假设、候选、机理或定性解释 | 公开 | 隐藏 |
| 计算路线 | 软件、方法、搜索、验证和分析流程 | Agent 自主设计 | Agent 自主设计 |
| 参考结果 | 数值、排序、结果结构、结论和 tolerance | 隐藏 | 隐藏 |

### 3.1 科学目标

科学目标定义问题本身，例如：

- 确定反应选择性的来源；
- 找到反应物到实验产物之间的可行路径；
- 判断不同构象的发光性质；
- 计算一个固定体系的热化学量；
- 比较多个体系的稳定性或势垒。

它必须对两个模式保持一致。

### 3.2 作者科学路线

作者科学路线告诉 reproduction Agent“作者认为应该沿什么科学方向研究”，例如：

- 选择性可能来自两种竞争的进攻构型；
- 某类环化机制可能控制反应；
- 两种构象可能对应不同发光行为；
- 某个产物族可能解释实验热化学；
- 某个电子态或结构因素可能产生观察到的趋势。

它不告诉 Agent“应该用什么软件和模型化学计算”。

### 3.3 计算路线

计算路线包括：

- 软件和电子结构方法；
- functional、basis、solvation 和 thermochemistry；
- 候选生成、构象搜索、TS search 和 state search；
- frequency、IRC、state tracking 或其他验证；
- 后处理和不确定性分析。

这些由两个模式的被评测 Agent 自主制定。论文实际使用的 protocol 只作为 private source
evidence 保留，不进入任何公开任务，也不作为 route fidelity 的机械评分标准。

### 3.4 参考结果

以下内容对两个模式都隐藏：

- 待重新计算的数值；
- 正确排序和最终条件判断；
- 最终优化得到的结果性结构；
- 论文结论的完整 reference answer；
- scoring rules 和 tolerance。

这里的“完整 reference answer”与 reproduction 主动公开的定性科学路线不冲突。Reproduction
可以告诉 Agent 作者主张的机理是什么，但支持该机理的结果结构、数值、排序和完整证据仍然
隐藏，评分重点是 Agent 能否通过独立计算重新建立这条证据链。

## 4. 公开信息与隐藏信息边界

Stage06 Agent 在构建任务前应在 private `workflow_review.json` 中记录简约分类：

```json
{
  "disclosure_inventory": {
    "shared_public": [],
    "reproduction_scientific_route": [],
    "hidden_reference": []
  }
}
```

这些列表由 Agent 根据科学语义判断，代码不按关键词或论文类型自动生成。

### 4.1 `shared_public`

两个模式都可以获得：

- 科学目标；
- 反应物、催化剂、底物或基础分子结构；
- 体系组成、电荷、自旋、溶剂、温度等必要边界；
- 研究开始前已经存在的事实；
- 完成任务所需的计算预算和交付要求；
- 与任务定义相符的实验现象。

### 4.2 实验结果是否公开

按任务目标判断：

- 解释型任务可以公开待解释的实验产物、选择性或光谱现象；
- 预测型任务必须隐藏待预测的实验结论。

例如：

```text
已知实验主要生成 R 产物，请解释选择性来源。
```

可以公开 R；而：

```text
预测该反应的主要对映体。
```

不能公开 R。

这由 Stage06 Agent 判断，代码不做实验字段黑白名单。

### 4.3 `reproduction_scientific_route`

只在 reproduction 公开：

- 作者假设；
- 作者考虑的候选类别或科学方案；
- 作者发现的定性机理；
- 作者认为关键的竞争关系；
- 为说明该科学路线所必需的非结果性文字描述。

### 4.4 候选描述与结果性结构的边界

“公开作者候选”不等于公开作者最终计算结果。

| 信息 | Reproduction 是否公开 |
|---|---|
| 作者提出存在路径 A/B | 公开 |
| 作者提出某类成键或断键机理 | 公开 |
| 候选的化学身份或定性关系 | 可以公开 |
| 研究前已有的反应物/产物结构 | 按任务目标公开 |
| 论文最终优化得到的 TS geometry | 隐藏 |
| 论文最终找到的中间体 geometry | 若属于待复现结论则隐藏 |
| 论文筛选后的最优构象 geometry | 若属于待复现结论则隐藏 |
| 最终频率、能量、排序和数值 | 隐藏 |

判断原则：

```text
problem-defining input 可以公开；
result-bearing artifact 必须隐藏。
```

例如 reproduction 可以写：

> 作者提出两个竞争的立体进攻方向可能控制选择性，请分别寻找和验证相应过渡态。

但不能直接提供论文最终优化得到的两个 TS 坐标。

### 4.5 `hidden_reference`

包括：

- 论文详细计算 protocol；
- 最终结果结构；
- reference values、ordering 和 conclusions；
- evaluator key points、rules 和 tolerance；
- PDF、SI 和大段 source-derived material。

论文 protocol 可以用于合成 Agent 理解论文证据和设计合理 reference evaluator，但不能出现在
被评测 Agent 的 task、schema、文件名、注释或 public data 中。

## 5. `paper_reproduction` 任务设计

### 5.1 模式目标

给出科学问题和作者科学路线，要求被评测 Agent 自主把该路线转化为计算研究，寻找必要结构，
完成验证，复现关键数值或趋势，并判断计算证据是否支持作者的主张。

它评估的是：

- 能否理解作者的科学假设；
- 能否把假设转化为合理计算问题；
- 能否独立规划和执行计算；
- 能否用结果支持或否定论文发现。

### 5.2 `task.md` 的四个逻辑部分

#### 1. Scientific objective

写清楚研究体系、科学问题和需要回答的最终判断，不公开待评分数值。

#### 2. Author-provided scientific route

写清楚作者提出的：

- 假设；
- 候选类型；
- 机理；
- 定性关系或解释。

使用“需要独立计算验证的作者主张”措辞，不把它描述成无需验证的正确答案。

#### 3. Required scientific validation

给出结果导向的最低证据要求，但不规定论文计算步骤。例如：

- TS 必须有可信的一阶鞍点和反应路径证据；
- excited-state 任务必须说明 state/root tracking；
- 构象或候选比较必须使用内部一致的能量尺度；
- 计算必须报告收敛、失败和不确定性；
- 最终结论必须能追溯到实际计算证据。

不写：

- 必须使用某个软件；
- 必须使用论文 functional/basis；
- 必须采用论文 TS search 工具；
- 必须严格按照论文计算顺序执行。

#### 4. Deliverables

要求交付：

- 自主选择的计算方案及理由；
- 搜索或构建的关键结构 artifact；
- 关键计算和验证结果；
- 数值、比较、排序或其他目标结果；
- 是否复现并支持作者科学路线；
- 限制、失败和不确定性。

### 5.3 Public inputs

默认只包含：

- shared problem-defining inputs；
- 研究前已有结构；
- 必要物理边界；
- 不会直接替代计算的最小科学数据。

如果作者科学路线只能通过文字说明，就只写在 `task.md`，不额外复制论文结果文件。

只有当某个 candidate artifact 本身是研究前输入而不是论文计算结论时，才可进入 reproduction
public data。最终优化 TS、最终中间体、筛选后的最优构象等结果性 artifact 默认隐藏。

### 5.4 Submission contract

schema 由具体科学任务决定，不强制所有任务拥有 candidate 数组。至少表达三个内容概念：

- computational approach and rationale；
- results and validation evidence；
- conclusion and uncertainty。

具体任务可以增加 candidates、structures、energies、states 或其他字段，但代码不生成固定化学
骨架。

schema 不能通过 `const`、单元素 `enum`、`default` 或 `example` 写入正确数值、排序、结构
身份或最终结论。

### 5.5 Reproduction evaluator

应评价：

- Agent 的计算方案是否科学合理；
- 作者科学路线要求的关键对象是否被实际搜索和验证；
- 提交的结构、状态或路径证据是否有效；
- 关键数值、趋势或比较是否复现论文结果；
- 结论是否由提交证据支持；
- 偏离论文时是否给出合理证据和不确定性。

不评价 paper protocol fidelity，不要求软件、functional、basis 或步骤与论文一致。

## 6. `autonomous_research` 任务设计

### 6.1 模式目标

只给出科学目标、研究前输入和科学验证要求，不给出作者科学路线。被评测 Agent 自己决定应当
提出什么假设、考虑什么候选或采用什么计算策略，并形成结论。

### 6.2 `task.md` 的四个逻辑部分

#### 1. Scientific objective

与 reproduction 保持同一上层问题，但不出现“论文”“作者”“复现”“与论文不同的方法”等
来源痕迹。

#### 2. Initial inputs and scientific boundaries

写清楚研究前输入、体系边界、可公开实验事实和计算预算。不加入作者后验发现。

#### 3. Required independent investigation

如果问题存在假设空间，要求 Agent：

- 提出合理假设、候选、构象、状态或机理；
- 设计有边界的搜索和筛选；
- 自主选择并论证计算方法；
- 验证关键候选；
- 比较替代解释并形成结论；
- 报告没有覆盖的空间和不确定性。

如果任务是纯计算、没有真实假设空间，则要求 Agent：

- 自主选择适合的计算方法；
- 完成必要的数值和物理验证；
- 得到目标结果并解释不确定性。

不能为了让 autonomous 看起来更开放而虚构候选或机理。

#### 4. Deliverables

按任务实际内容要求方法理由、结果、验证证据、结论和不确定性。只有任务确实存在候选空间时，
才要求候选列表和搜索记录。

### 6.3 Public inputs

autonomous 只使用 `shared_public`：

- 研究前初始体系；
- problem-defining structures；
- 必要物理边界；
- 与目标一致的实验事实。

不公开作者科学路线、论文结果结构、论文 protocol、reference values 和 evaluator。

### 6.4 Submission contract

与 reproduction 一样根据任务科学内容设计，不强制：

```json
{"candidates": [], "calculations": [], "conclusion": {}}
```

成为所有任务的固定骨架。

对于机制/候选任务可以要求 candidates；对于纯数值任务只需 approach、results、validation 和
conclusion。大型结构、轨迹和矩阵使用独立 XYZ/CIF/文本 artifact，主 JSON 只保留路径、摘要
和关键数值。

### 6.5 Autonomous evaluator

共有科学结果可以复用 reproduction evaluator 的 reference evidence 和部分结果规则，但不能
无审查地整份复制。

如果存在假设空间，autonomous evaluator 额外评价：

- 假设或候选是否科学合理；
- 是否覆盖关键竞争解释；
- 搜索和筛选是否有依据；
- 是否发现 paper-supported 或科学等价路线。

如果是纯计算任务，autonomous evaluator 可以与 reproduction evaluator 高度相似，甚至共享
大部分规则。不得为了制造差异而添加虚假 discovery 规则。

两种 evaluator 都应正常生成完整、具体、可执行的 numeric、ordering、condition 或 semantic
规则。numeric rule 需要 target、unit、初始 tolerance 和 binding，但 Gate 不判断 tolerance
是不是唯一最佳选择。

## 7. 两种模式的配对关系

### 7.1 必须一致

- scientific objective；
- 基础研究体系；
- 不冲突的物理边界；
- 需要回答的最终科学问题；
- 必要的科学验证标准。

### 7.2 可以不同

- reproduction 多一段 author-provided scientific route；
- 当科学路线需要非结果性补充材料时，public inputs 可以不同；
- submission contract 可以因候选职责不同而变化；
- evaluator 可以增加或删除 hypothesis-generation 相关规则。

### 7.3 也可以相同或接近

如果论文是纯计算问题、没有真实假设空间：

- 两个 task 可以非常接近；
- public inputs 可以完全相同；
- submission schema 可以相同；
- evaluator 可以共享大部分或全部科学结果规则。

这不是构建失败。真实性优先于人为制造模式差异。

### 7.4 仍然需要科学拒绝的情况

没有假设空间不是拒绝理由，但以下情况仍应拒绝：

- 连科学目标所需的初始体系都无法唯一确定；
- 必要组成、电荷、自旋或其他定义性边界缺失且必须猜测；
- 任务在现有预算内不可执行；
- 没有可评价的计算结果或验证证据；
- task、inputs 和 evaluator 无法指向同一个科学对象。

## 8. Stage06 Agent 的职业和工作流

### 8.1 职业定义

建议 Prompt 开头改为：

```text
You are a computational-chemistry benchmark research director and paired-task architect.
Design two complete evaluation tasks around one source-supported scientific objective.
The reproduction task discloses the authors' scientific hypothesis, candidate direction or
mechanistic explanation, but both evaluated Agents must independently design their computational
approach. The autonomous task receives no author scientific route and must formulate one when the
problem genuinely has hypothesis space. You are responsible for inputs, validation requirements,
submission contracts, hidden evaluators and pair consistency.
```

Prompt 不写“Stage06”“Stage07 将修复”或“后续人工会补 evaluator”。Agent 应把自己理解成完整
评估任务的最终设计者。

### 8.2 Private scientific brief

构建前记录：

- `scientific_objective`；
- `shared_initial_facts`；
- `author_scientific_route`；
- `paper_computational_protocol_private`；
- `reference_results`；
- `artifact_disclosure`；
- `validation_requirements`；
- `constructibility_notes`。

不要求新增复杂公共 schema；这些内容放在 private `workflow_review.json`。

### 8.3 工作顺序

#### A. 确定科学目标

选择中心、非平凡、可计算且有 reference evidence 的科学问题。

#### B. 区分科学路线与计算 protocol

明确作者的科学假设/候选/机理是什么，以及论文实际如何计算。前者只给 reproduction，后者
两个模式都隐藏。

#### C. 判断 artifact 身份

逐一判断输入文件是 problem-defining input 还是 result-bearing artifact。结果性 TS、中间体、
构象和数值不能进入 public inputs。

#### D. 完整构建 reproduction

完成 task、public inputs、submission schema 和 evaluator，并运行 reproduction self-check。

#### E. 构建 autonomous

从相同 scientific objective 和 `shared_public` 构建，不复制 reproduction 的科学路线、结果性
artifact 或 evaluator-specific 内容。

允许复用真正共享的初始输入。纯计算任务不强行创造 candidate discovery。

#### F. 双模式语义自查

逐项检查：

```text
task.md
submission_schema.json
public data filenames
public data comments and contents
task_info descriptions
evaluator key points/conclusions/rules
```

明确回答：

1. reproduction 是否只公开作者科学路线，而没有公开论文计算 protocol？
2. reproduction 是否误放入论文结果性结构或数值？
3. autonomous 是否隐藏作者科学路线？
4. 两个模式是否都要求 Agent 自主规划计算？
5. 科学验证要求是否明确但不规定具体方法？
6. 如果没有假设空间，是否避免虚构 discovery 要求？
7. 两个 evaluator 是否与各自公开任务一致？

#### G. 机械自查

运行统一 Gate，修复必需文件、JSON、binding、manifest 和 evaluator 完整性问题，通过后才写
terminal receipt。

## 9. Stage06 Prompt 的具体更改

### 9.1 删除现有转换定义

删除：

```text
copy the stable reproduction task as the starting point for autonomous research
```

避免把 autonomous 理解成“复制任务后删除方法名”。

### 9.2 新 reproduction 指令

```text
State the scientific objective and the authors' scientific route: their hypothesis, candidate
direction or mechanistic explanation. Do not disclose the paper's software, model chemistry,
ordered computational protocol, reference structures, numerical results, ordering or tolerance.
Require the evaluated Agent to design and justify its own computational approach, locate or build
any result structures needed to test the authors' route, satisfy the scientific validation
requirements and decide whether its evidence reproduces the paper-supported conclusion.
```

### 9.3 新 autonomous 指令

```text
State the same scientific objective, initial system and scientific boundaries without the
authors' hypothesis, candidate direction or mechanistic explanation. When the problem has genuine
hypothesis space, require the evaluated Agent to formulate and compare scientifically reasonable
routes. For a direct computation with no genuine hypothesis space, do not invent candidates;
require an independently justified computation, validation and conclusion.
```

### 9.4 新结果性 artifact 指令

```text
Do not expose an optimized transition state, intermediate, selected conformer or other artifact
when that artifact is itself a result the evaluated Agent is expected to reproduce. Public inputs
must define the problem, not supply the solution.
```

### 9.5 新科学验证指令

```text
Write outcome-based scientific validation requirements without prescribing the paper's
computational protocol. Require sufficient evidence for the claimed structure, state, pathway,
comparison or property, while leaving software, model chemistry and execution order to the
evaluated Agent.
```

## 10. Stage07 的配套审计职责

Stage07 继续只做审计和有限修复，不重建任务。

### 10.1 Reproduction 审计

- 作者科学路线是否有 source evidence；
- 是否把假设表达为待验证主张；
- 是否意外公开 paper computational protocol；
- 是否意外提供结果性 TS/intermediate/conformer；
- 是否泄露 reference number、ordering、conclusion 或 tolerance；
- 是否要求 Agent 自主规划计算；
- 科学验证要求是否充分且不绑定具体方法；
- evaluator 是否评分计算证据，而不是只匹配作者结论文本。

### 10.2 Autonomous 审计

- 是否隐藏作者科学路线；
- 是否仍在 task、schema、filename、comment 或 data 中泄露作者候选/机理；
- 有假设空间时是否要求 Agent 自主提出和比较；
- 无假设空间时是否没有虚构候选；
- 是否要求自主计算、验证和结论；
- evaluator 是否与真实任务职责一致。

### 10.3 Pair 审计

- 是否回答同一 scientific objective；
- 唯一预期差异是否主要来自 author scientific route disclosure；
- 两个模式是否都隐藏 paper protocol 和 reference answer；
- public inputs 相同或不同时是否都有科学理由；
- 是否为了追求表面差异改变了 scientific question。

### 10.4 有限修复边界

可以修复：

- 少量措辞和边界；
- 个别 protocol/answer 泄露；
- 少量 schema、filename 或 comment 问题；
- 个别 evaluator binding 或 rule。

必须拒绝：

- 需要重新选择科学目标；
- 结果性结构已经构成任务核心且无法通过少量删除恢复；
- essential input 缺失；
- evaluator 需要整体重建；
- 任务在预算内不可执行。

不能仅因两个纯计算模式很相似而拒绝。

## 11. Gate 边界

Gate 继续只阻断：

- 必需文件缺失；
- JSON/schema/binding 不可解析；
- evaluator 是空模板或没有可执行规则；
- PDF/SI 或大段 source material 进入 Agent 输入；
- manifest 与 public artifact 不一致。

Gate 不判断：

- 一段文字是否属于作者科学路线；
- 一个结构是否是论文结论；
- 是否存在真实假设空间；
- 某种方法是否科学最优；
- tolerance 是否唯一正确。

这些由 Stage06 self-review、Stage07 科学审计和人工检查完成。不要增加论文、化合物、机理或
关键词特例。

## 12. 上一轮问题的配套处理

### 12.1 Schema 答案泄露

上一轮 `paper_2aca...` 的 schema 用 `const` 固定正确 ordering。

处理：Stage06/07 对照 hidden reference 检查 task、schema、default/example、filename、comment
和 public data。Gate 不全局禁止合法 `const/enum`。

### 12.2 Evaluator 与模式不匹配

上一轮 autonomous evaluator 常复制 reproduction numeric target 后只放宽 tolerance。

处理：

- 允许共享真正共同的结果规则；
- 有假设空间时，autonomous 增加 hypothesis/candidate/search 相关评价；
- 纯计算任务允许 evaluator 高度相似；
- 每条 numeric rule 由 Agent 正常给出 target、unit、tolerance 和 binding；
- 不用代码自动修改 tolerance。

### 12.3 未定义布尔判断

`both_bright`、`closely_similar` 等判断如果进入 public contract，必须有可执行定义；否则只要求
原始数值和科学解释，由 hidden evaluator 评分。

### 12.4 大型 JSON

大型坐标、轨迹和矩阵改用独立 artifact。主 JSON 只保存路径、摘要、关键数值和 validation。

### 12.5 Source material 暴露

Prompt 要求只提取完成任务所需的最小输入；self-check 和 external Gate 继续阻断 PDF/SI 或
大段 source-derived material。

### 12.6 Stage07 receipt

代码机械计算 candidate 与 audited output 的 changed-file list，Agent 解释修复原因。

### 12.7 Stage07 目录复制

编排器在 Agent 启动前准备 audited copy，Agent 不执行 `rm -rf` 或重新复制目录。

### 12.8 工具和 metadata

作为低优先级独立改进：

- Prompt 使用现有 `document_query.py`，不安装 PDF 包；
- document query 增加通用 page range；
- metadata 做 HTML unescape 和 Unicode NFC。

## 13. 具体任务示例

### 13.1 有科学路线空间的选择性任务

#### Reproduction

```text
# 1. Scientific objective

确定该手性催化反应的选择性来源，并判断计算结果是否能够复现观察到的 product sense。

# 2. Author-provided scientific route

作者提出，两个不同立体进攻方向可能形成竞争反应通道，它们的相对稳定性决定主要产物。
请把这一主张视为需要独立计算验证的科学路线。

# 3. Required scientific validation

自主提出适合的计算研究方案，寻找两个方向对应的关键结构，验证它们是否代表目标反应事件，
在一致的热化学尺度下比较，并说明结果是否支持该选择性解释。报告收敛、失败和不确定性。

# 4. Deliverables

提交计算方案及理由、搜索得到的结构 artifact、关键验证、相对自由能、product-sense conclusion
和证据链。
```

Public inputs 只包含研究前 catalyst/substrate/reagent 和必要边界，不包含论文最终 TS 坐标。

#### Autonomous

```text
# 1. Scientific objective

确定该手性催化反应的选择性来源，并预测或解释主要 product sense。

# 2. Initial inputs and scientific boundaries

输入提供研究前 catalyst/substrate/reagent、组成、电荷、自旋、溶剂和温度。

# 3. Required independent investigation

自主提出可能的选择性来源、竞争机理或关键构型，设计搜索和计算验证，比较替代解释并形成
结论。报告没有覆盖的空间、失败和不确定性。

# 4. Deliverables

提交提出的科学路线、候选和结构 artifact、计算与验证、最终结论和证据链。
```

两个任务使用相同初始结构，也都自主选择计算方法。区别只是 reproduction 已知作者提出的
“两个立体进攻方向”科学路线。

### 13.2 没有假设空间的纯计算任务

假设目标是计算一个固定分子的垂直激发能。

#### Reproduction

```text
计算给定分子的目标垂直激发能，使用科学合理的方法完成状态识别、收敛和结果验证，并判断
结果是否复现该体系的参考性质。
```

#### Autonomous

```text
计算给定分子的目标垂直激发能，使用科学合理的方法完成状态识别、收敛和结果验证，并给出
结论和不确定性。
```

如果论文没有额外科学路线可以公开，这两个任务可以接近。二者仍是有效计算任务，不添加虚假
构象、机理或候选。

## 14. 上一轮四篇任务在新边界下的变化

### `paper_2aca...`

- reproduction 可公开作者认为 Bergman cyclization 解释目标现象；
- 不公开 QST3/B3LYP route、最终 TS/product geometry、barrier 和 ordering；
- Agent 自主搜索、验证反应路径并复现趋势；
- autonomous 不获得 Bergman scientific-route 提示，只获得按目标允许公开的初始体系和现象。

### `paper_611...`

- reproduction 可公开作者认为特定 rotamer/state relationship 解释发光行为；
- 不公开论文 TD-DFT route，也不直接提供论文筛选后的 bright-state result geometry；
- Agent 自主进行 conformer/state investigation；
- autonomous 不获得作者的 rotamer/bright-state 路线提示；
- 如果该任务最终只是固定结构的性质计算，两种模式可以接近，不强行创造 conformer discovery。

### `paper_76ae...`

- reproduction 可公开作者提出两个竞争立体进攻方向控制选择性；
- 不提供论文最终 TS2 coordinates、双层计算 route、ΔΔG 和 ordering；
- Agent 自主寻找和验证对应通道；
- autonomous 连“两种进攻方向”提示也不获得，需要自主提出选择性解释。

### `paper_9455...`

- reproduction 可公开作者提出某类 H-loss cyclic product route 解释实验热化学；
- 不公开 CBS-QB3 protocol、最终优化 P1/P2 geometry 和 reaction energies；
- autonomous 只获得按任务目标允许公开的 SiN/isoprene/实验边界；
- 如果目标只是固定产物的热化学计算，不强行要求发现 38 个 isomer。

## 15. 预期代码修改范围

用户确认后再制定详细实施计划。预计涉及：

### 主体

- `src/stages/stage06_task_builder/prompts.py`
  - 四层信息模型；
  - author scientific route 与 paper computational protocol 分离；
  - result-bearing artifact 边界；
  - 两种模式都方法自主；
  - 纯计算任务允许模式接近；
  - 全 public-surface self-review。

- `src/stages/stage07_task_judge/prompts.py`
  - science-route disclosure 审计；
  - result artifact 和 paper protocol 泄露审计；
  - 纯计算任务相似性合法；
  - evaluator 与任务职责一致性。

- `src/stages/phase_gate.py`
  - 不新增科学规则；
  - 只处理与“两个模式必须有不同/相同 public inputs”等新设计冲突的机械假设，如代码仍存在。

### 配套

- `src/stages/stage07_task_judge/stage.py`
  - audited copy；
  - changed-file provenance。

- document query 和 metadata
  - 主体验证后独立修改。

### 明确不做

- 不恢复 Stage06B converter；
- 不恢复 conversion retry 或旧 resume；
- 不写论文/化合物特例；
- 不让代码判断或生成科学候选；
- 不固定所有任务必须有 candidates schema；
- 不增加大量 evaluator rule type；
- 不让 Stage07 重建失败任务。

## 16. 测试计划

### 16.1 Fixtures

1. reproduction 公开文字科学路线，但两个模式都不公开 paper protocol；
2. 最终 TS geometry 属于 reference result，不能进入 reproduction public data；
3. 两种模式都要求自主方法和科学验证；
4. autonomous 不含 author scientific route；
5. 解释型任务可以公开实验现象，预测型任务隐藏实验结论；
6. 纯计算任务的两个 task/schema/evaluator 高度相似仍合法；
7. schema 用 `const/default/example` 写答案时被语义审计发现；
8. evaluator 空模板或 binding 失效时 Gate 阻断；
9. 大型结构用独立 artifact 时正常 binding；
10. PDF/SI/source material 暴露时 Gate 阻断。

### 16.2 真实任务回归

逐篇检查：

- scientific objective 是否一致；
- reproduction 是否只多公开作者科学路线；
- 两种模式是否都隐藏 paper protocol；
- reproduction 是否误放结果性结构；
- autonomous 是否隐藏作者假设/候选/机理；
- 科学验证要求是否充分但不规定方法；
- 纯计算任务是否没有虚构 discovery；
- submission contract 是否只要求必要交付；
- evaluator 是否完整、可执行并与模式一致；
- Stage07 是否正确审计和有限修复。

不以两个模式的文字差异大小或发布数量作为唯一指标。

## 17. 验收标准

1. 两种模式共享同一 scientific objective；
2. reproduction 公开作者科学路线，但不公开论文详细计算 protocol；
3. autonomous 不公开作者科学路线；
4. 两种模式都要求 Agent 自主选择计算方法和流程；
5. 两种模式都包含结果导向的科学验证要求；
6. 最终 TS/intermediate/conformer 等结果性 artifact 不进入 public inputs；
7. 实验事实是否公开与解释/预测任务目标一致；
8. 纯计算论文不会因缺少假设空间被拒绝；
9. 纯计算任务允许两个模式和 evaluator 高度相似；
10. schema 不泄露 reference answer；
11. evaluator 完整、具体、可执行；
12. evaluator 不要求 paper protocol fidelity；
13. 有假设空间时 autonomous 评价科学路线提出和替代解释；
14. 无假设空间时不虚构候选或 discovery rules；
15. Stage06 self-review 覆盖 task、schema、data 和 evaluator；
16. Stage07 只审计和有限修复；
17. Gate 保持最小机械职责；
18. 生产代码无论文、化合物或关键词特例；
19. 两种模式均不向被评测 Agent 暴露 PDF/SI 和 hidden evaluator。

## 18. 相对原 v22 的更正摘要

1. 将模式分界从“是否公开论文计算路线”改成“是否公开作者科学路线”；
2. 明确两种模式都自主规划计算方法和验证流程；
3. 将 author hypothesis/mechanism 与 paper computational protocol 分成两个概念；
4. 明确论文最终 TS 等结果性结构在 reproduction 中也隐藏；
5. 保留任务所需的结果导向科学验证要求；
6. 实验事实按解释型/预测型任务决定是否公开；
7. 取消 autonomous 必须总有候选/机理发现空间的要求；
8. 允许纯计算论文正常构建，两个模式可以高度相似；
9. 取消 autonomous schema 必须固定为 candidates/calculations/conclusion；
10. 允许两个 evaluator 共享真实共同规则，不再强求形式上的完全独立；
11. 保留 Gate 的最小机械职责，不增加科学关键词规则；
12. 将上一轮小问题安排为配套修复，不改变双模式主体。

最终定义：

```text
paper_reproduction
= 科学目标 + 作者科学路线提示 + Agent 自主计算与验证

autonomous_research
= 相同科学目标 + 无作者科学路线提示 + Agent 自主提出路线并计算验证
```

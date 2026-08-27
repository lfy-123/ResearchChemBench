# Stage06/07 v25 任务完整性前置与科学审计修改方案

## 1. 版本目标

v25 在 v24 的 feasibility-first 和 per-mode release 基础上，进一步把“任务指令完整性、公开输入闭合性、
过程验证关键点和最终结论关键点”设为合成阶段的核心验收内容。Stage06 负责尽可能生成可直接使用的完整
任务，Stage07 负责对已有任务执行独立、分阶段的科学审计和必要修补。

本版本不以增加大量固定规则为目标，也不把 scoring tolerance 的科学选择提前硬编码到 Gate。重点是保证
被评测 Agent 在看不到论文、SI 和 evaluator 的情况下，能够唯一理解任务、建立计算体系、知道必须验证什么、
知道何时可以结束，并提交能够支持最终结论的结果。

## 2. 已确认的边界

以下边界由用户确认，v25 视为硬约束：

1. Stage06 每个可构建模式必须包含至少一个过程验证关键点和至少一个最终结论关键点；缺少任一类时，
   该模式不得进入构建和发布。
2. 开放搜索任务必须有明确的停止条件、完成判据或搜索边界，但不得强行规定统一的候选假设数量。候选
   数量由被评测 Agent 根据任务科学问题自主决定，并在提交中记录实际覆盖范围。
3. Stage07 可以补充缺失的必要输入说明、任务要求、schema 字段、过程关键点、最终结论、evaluator 引用
   和其他必要内容；修复必须建立在 Stage06 已选定的 scientific objective 上，不得改变目标、换成弱代理
   问题或凭空创建新的科学任务。
4. 如果两个模式中只有一个可行，只发布该模式；不为了凑 pair 强行创建另一个模式。
5. 输入可以使用论文/SI 中已经明确且不泄露答案的结构，也可以允许被评测 Agent 自己生成 3D conformer、
   复合物或 TS 初猜；但不能要求 Agent 猜测连接关系、质子化、电荷、多重度、原子映射或结果结构。
6. CCDC、PubChem 等数据库按需使用，不是所有任务的强制步骤。依赖数据库时使用稳定记录或固定候选快照。
7. 论文正文和 SI 可以供 Stage06/07 内部读取，但不得进入 `paper_reproduction` 或 `autonomous_research`
   的 Agent-visible `agent_input`。
8. evaluator 可以包含 numeric、ordering、condition 和 semantic 规则。Gate 只检查规则完整、可解析、引用
   闭合和 binding 可用，不对 tolerance 的具体科学选择作过度阻断；规则由人工后审。
9. 不新增 task_id、task_family_id、task_pair_id 等论文级 ID；保留 `paper_id`，评估文件内部继续使用
   `key_point_id`、`conclusion_id`、`rule_id` 和 `evidence_id`。

当前没有待确认的边界问题。以下方案中的“硬性检查”仅限于任务闭合、关键点存在和文件合同；科学方法优劣、
tolerance 是否最优及机理解释强弱仍由 Stage07 科学审计和后续人工审查负责。

## 3. v24 遗留问题

v24 已经解决了文件缺失、论文 PDF 泄露、单模式发布和技术 Gate 不一致等问题，但真实回归暴露出：

- 某些任务使用论文原子标签，公开输入没有对应映射；
- “finite candidate set”“relevant stationary point”等表述没有可执行定义；
- 激发能等物理量可能没有说明 vertical/adiabatic 定义；
- 任务要求过程验证，但 evaluator 关键点主要只有最终数值；
- 产品身份、候选身份和输出槽位之间可能没有明确映射；
- Stage07 的 `scientific_audit` 结构过于宽松，无法确认其确实审计了任务指令和关键点；
- Common Gate 只能判断结构合同，无法识别任务语义上的歧义。

v25 的重点是让 Stage06 在生成时尽早消除这些问题，让 Stage07 以结构化 workflow 再次检查，而不是仅在最后
检查文件是否存在。

## 4. Stage06 v25 工作流

### 4.1 冻结 scientific objective

Stage06 先确定并写入共享 scientific core：

- scientific objective；
- scientific question；
- physical boundary；
- measurement boundary；
- requested results；
- required process observations；
- required final conclusion；
- validation requirements；
- search and stopping logic。

scientific objective 一旦确定，后续模式只能改变 route disclosure，不得改变目标、比较对象或被评价的科学
问题。

### 4.2 输入闭合审查

Stage06 必须建立内部输入清单，逐项确认：

- 研究对象和分子连接关系是否唯一；
- 结构文件或 SMILES 是否存在且不泄露待评分结果；
- 电荷、多重度、质子化、立体化学是否明确；
- 原子映射是否公开可用；
- 溶剂、气相、温度、标准态等边界是否足够；
- 比较对象是否明确；
- 数据库记录或检索候选是否真的需要；
- 哪些结构由 Agent 自主生成，哪些属于公开输入；
- 结果结构、TS、最低能中间体或优势构象是否错误地放进公开输入。

如果任务使用了原子标签、候选名称或内部编号，必须随 Agent input 提供不含答案的明确映射；否则改成结构性
描述，或判定输入不闭合。

### 4.3 任务指令完整性审查

每个模式的 `task.md` 必须明确回答：

1. 研究什么科学问题；
2. 使用哪些输入，输入分别代表什么；
3. Agent 可以自主生成什么；
4. 必须计算哪些物理量或结构性质；
5. 必须检查哪些过程验证条件；
6. 如何判断任务完成；
7. 结果需要提交哪些字段；
8. 搜索范围、停止条件和限制是什么。

禁止无定义地使用以下表述：`relevant`、`appropriate`、`finite set`、`as needed`、`corresponding product`、
`candidate structure`。若确实需要使用，必须在同一任务中给出对象定义、选择条件或完成判据。

对于开放搜索：

- 必须有完成判据或停止条件；
- 不规定统一的候选数量；
- 不要求 Agent 为了满足形式而虚构候选；
- Agent 自行决定候选数量，并在结果中报告实际覆盖范围和未覆盖空间。

对于直接计算：

- 必须定义目标状态和物理量；
- 必须定义 endpoint、参考态或比较方向；
- 必须定义验证条件和停止条件；
- 不要求人为添加 discovery 任务。

### 4.4 两种模式的指令边界

#### `paper_reproduction`

公开：科学目标、作者的定性假设、候选方向或机理路线。

隐藏：论文软件、模型化学、详细执行步骤、结果结构、数值答案、结果排序、tolerance 和完整结论。

任务要求 Agent 自主设计计算路线，验证作者的假设或发现。

#### `autonomous_research`

公开：科学目标、研究对象、输入和科学验证边界。

隐藏：作者假设、候选路线、机理、结果方向、答案结构和数值。

如果存在真实假设空间，要求 Agent 提出并比较合理解释；如果只是直接计算，不强行要求虚构新的机制发现。

### 4.5 过程关键点和最终结论关键点

每个可构建模式必须生成两类关键点：

#### 过程验证关键点

至少覆盖任务实际需要的部分：

- 输入体系和结构身份；
- 电荷、多重度和状态确认；
- 关键几何、频率、收敛或状态验证；
- TS/中间体/产物连接验证；
- 独立计算、敏感性检查或交叉验证；
- 搜索覆盖和限制。

关键点必须来自论文/SI 或任务科学定义，不能只写“完成计算”或“结果合理”。

#### 最终结论关键点

至少包括：

- 论文支持的最终科学发现或比较关系；
- 适用范围；
- 必要的限制条件；
- 不能从计算推出的过强结论。

最终结论可以是数值、排序、结构身份、条件判断或文本语义，不要求全部转换成 numeric。

Stage06 必须在写 `construction_receipt.json` 前确认：

```text
process_key_points 非空
final_conclusions 非空
每个关键点有 source evidence
每个最终结论有 supporting key points
```

若缺少任一类，模式标记为不可构建，不得只靠后续 Stage07 补救。

### 4.6 Stage06 输出

保留 v24 的目录结构，不增加不必要的顶层文件：

```text
outputs/
  workflow_review.json
  MODE/
    task.md
    task_info.json
    submission_schema.json
    data/inputs/...
  evaluator_reference/MODE/
    reference_key_points.json
    reference_conclusions.json
    scoring_rules.json
    evidence_map.json
    critical_failures.json
  construction_receipt.json
```

在 `workflow_review.json` 的 `feasibility` 或内部质量字段中记录：

- `instruction_completeness`；
- `input_completeness`；
- `process_key_points`；
- `final_conclusions`；
- `mode_separation`。

这些字段用于 Stage07 审计，不进入被评测 Agent 的公开输入。

## 5. Stage07 v25 完整审计工作流

Stage07 读取 Stage06 候选、source snapshot 和所有模式文件，按以下顺序工作。

### 阶段 A：候选接收

确认候选目录、source snapshot、workflow review 和 declared modes 均存在。缺少文件或执行环境异常才使用
`technical_blocked`。

### 阶段 B：scientific objective 审计

检查目标是否：

- 是论文中心或有意义的计算科学问题；
- 在两个模式间保持一致；
- 没有被缩成无关代理；
- 与 requested results 和最终结论一致。

Stage07 可以补充目标的必要定义，但不得更换目标。

### 阶段 C：输入完整性审计

执行反事实测试：删除论文、SI 和 evaluator 后，只保留 Agent input 和允许的数据库连接器，Agent 是否能唯一
建立体系？

重点检查结构身份、原子映射、状态、环境、比较对象和结果泄露。格式合法但科学身份不唯一时，不能通过。

### 阶段 D：任务指令审计

为每个模式建立以下内部映射：

```text
任务要求
→ 所需输入
→ Agent 可执行操作
→ 过程验证
→ 完成/停止条件
→ 提交字段
```

发现 undefined label、未定义物理量、缺少停止条件、vertical/adiabatic 歧义或任务要求与 schema 不一致时，
优先修复 task.md 和 schema。

### 阶段 E：关键点和结论审计

Stage07 必须分别判断：

- 是否存在过程验证关键点；
- 是否存在最终结论关键点；
- 过程关键点是否覆盖任务要求的关键计算节点；
- 最终结论是否覆盖论文的最终发现；
- 关键点和结论是否有 source evidence；
- 是否存在只有数值、没有过程或文本结论的情况；
- 是否存在空泛模板或与任务无关的关键点。

如果缺少必要关键点或结论，Stage07 可以从当前论文/SI 补充，但不得发明论文没有支持的科学结论。

### 阶段 F：模式和答案泄露审计

确认 reproduction 只公开作者定性路线，autonomous 不公开作者路线。检查 task.md、task_info、schema、文件名、
XYZ 注释和所有 Agent-visible 数据。

### 阶段 G：必要修补

允许修补：

- 任务指令中的科学定义、输入说明和停止条件；
- 公开结构或原子映射说明；
- submission schema 必要字段；
- 过程关键点和最终结论关键点；
- evaluator key point/conclusion/evidence 的缺失或引用闭合问题；
- 模式选择和目录清理。

不允许：

- 改变 scientific objective；
- 把论文复现目标替换成弱代理；
- 发明论文未支持的参考结果；
- 从零创建 Stage06 没有生成的模式；
- 为了通过 Gate 而删除必要的科学要求。

### 阶段 H：自查、Gate 和发布决定

修补完成后：

1. 运行同一 `phase_gate.py`；
2. 读取 self-check report；
3. 修复阻断性文件合同问题；
4. 更新 workflow review 的最终 `release_modes`；
5. 写 audit receipt；
6. 动态装配实际批准模式。

批准模式必须同时满足：

- instruction completeness 通过；
- input completeness 通过；
- process key points 非空且充分；
- final conclusions 非空且充分；
- mode separation 通过；
- Gate 通过。

## 6. Gate 与代码修改范围

### 6.1 Gate 保持的职责

Gate 继续负责通用机械合同：

- 文件和目录存在；
- JSON 可解析；
- task_info 与 paper_id/task_type 一致；
- required deliverables 与 submission schema 一致；
- evaluator 文件非空且引用闭合；
- binding 指向声明字段；
- XYZ 基本格式合法；
- 论文 PDF 不进入 Agent input；
- declared modes 与目录一致。

### 6.2 Gate 新增的最小通用检查

不引入论文或化学类型特例，只增加：

- task.md 四个逻辑部分必须存在；
- workflow review 中过程关键点和最终结论关键点必须非空；
- 开放搜索任务必须出现明确完成/停止条件；
- 任务中声明的 public input 路径必须实际存在；
- 必要 validation 输出字段不能是空模板；
- 使用显式 atom label 时必须存在公开映射说明。

Gate 不检查：

- tolerance 是否科学最优；
- 计算方法是否最优；
- 论文机理是否唯一正确；
- 自主 Agent 是否提出了某个预设的新机制。

### 6.3 Stage07 schema

将 `scientific_audit` 从任意 object 收紧为少量通用项目，每个项目至少包含：

```json
{
  "status": "passed|failed|repaired",
  "finding": "...",
  "evidence": ["..."],
  "repairs": ["..."]
}
```

必须包含：

- `objective`；
- `inputs`；
- `instruction_completeness`；
- `process_keypoints`；
- `final_conclusions`；
- `mode_separation`；
- `answer_inversion`；
- `evaluator_quality`。

这不是把科学判断硬编码进 Python，而是确保 Stage07 真实报告每个审计维度。

## 7. 不同任务的处理原则

### 7.1 结构完整但答案结构应隐藏

可以给出反应物、起始构象和研究前结构；不能给出待评分 TS、最低能中间体、优势产物或答案构象。

### 7.2 论文只有定性结论

仍然可以生成任务。关键点使用文本、ordering、condition 或 semantic 形式，不强行制造 numeric reference。

### 7.3 论文有数值但方法敏感

任务可以保留数值参考，但应在 measurement boundary 中明确物理量定义和方法限制；scoring tolerance 留给
人工后审，不以窄 tolerance 作为 Stage06/07 的主要阻断条件。

### 7.4 输入无法唯一闭合

如果 reproduction 可闭合而 autonomous 不可闭合，只发布 reproduction；如果两者都无法闭合，才科学拒绝。

## 8. 测试计划

新增和调整定向测试，保持测试简洁，覆盖：

1. 缺过程关键点时 Stage06 不构建；
2. 缺最终结论关键点时 Stage06 不构建；
3. 开放搜索有停止条件但没有固定候选数量时通过；
4. 没有停止条件时被识别；
5. 原子标签缺少公开映射时被识别；
6. vertical/adiabatic 定义缺失的任务进入 Stage07 修补；
7. Stage07 可以补充必要关键点但不能改变 objective；
8. reproduction/autonomous 路线泄露检查；
9. 单模式发布；
10. 过程关键点和最终结论均为文本时仍可通过结构 Gate；
11. evaluator 只包含 semantic/ordering/condition 时不被误判为缺少 numeric；
12. 论文 PDF 不进入 Agent-visible 输入。

测试顺序：

1. v25 新增定向测试；
2. v24 Gate/release 测试；
3. Stage06/07 package 和 runner 测试；
4. `git diff --check`、编译检查和五篇真实回归。

## 9. 真实回归验收标准

每篇论文逐模式检查：

- 任务指令四部分是否完整；
- 输入是否自包含且无歧义；
- reproduction 是否只公开作者定性路线；
- autonomous 是否隐藏作者路线；
- 是否存在明确验证和停止条件；
- 是否有过程关键点；
- 是否有最终结论关键点；
- 关键点和结论是否来自论文/SI 证据；
- Stage07 是否发现并修复 Stage06 问题；
- release_modes 是否与最终目录一致；
- 是否出现 technical_blocked、工具循环或无效重试。

发布篇数不是唯一指标。科学拒绝一个输入不闭合的任务，优于机械发布一个无法公平评估的任务。

## 10. 预期改进

相较 v24，v25 应达到：

- Stage06 生成的任务指令更少出现未定义术语和隐含前提；
- Agent input 的结构身份、状态和比较对象更明确；
- 每个任务都同时具备过程验证关键点和最终结论关键点；
- evaluator 不再只有数值结果，也覆盖文本、结构、条件和机制结论；
- Stage07 的审计从“文件/事实修复”扩展为“目标—输入—指令—关键点—结论”的完整闭环；
- Stage07 修复工作量下降，修复主要集中在少量 source-supported wording 或字段补充；
- 单模式和科学拒绝逻辑继续保持；
- 不通过添加论文特例、固定候选数量或过严 tolerance 来制造表面通过率。

## 11. 尚不需要修改的部分

以下内容不属于本版本重点：

- scoring tolerance 的最终科学选择；
- benchmark 侧权重和总分策略；
- experiment_validation 模式；
- 实际计算成本估计；
- 论文外的新科学结论生成；
- 统一所有任务的候选数量或软件路线。


# Stage06/07 v20 双模式任务、路线泄露与运行轨迹深度审查

## 1. 审查范围

本报告针对以下 run 的四篇发布任务和一篇科学拒绝任务：

```text
runs/stage0607-v20-gpt-5.6-sol-20260827-model-driven-input-closure-5
```

对每个发布任务逐项比较：

- `paper_reproduction/agent_input/task.md`；
- `autonomous_research/agent_input/task.md`；
- 两种模式的 `submission_schema.json`；
- public data 文件名、注释和内容；
- 两种模式的 reference key points、conclusions 和 scoring rules；
- Stage06 candidate、Stage07 audited task 和 audit receipt 的真实 diff；
- Stage06/07 Agent stdout、stderr、Gate 调用和工具失败。

被评测 Agent 的实际可见面只有任务包中的 `agent_input/`。根目录的 `task_info.json` 和
`evaluation/` 不会被 benchmark runner 物化到 Agent workspace。benchmark 侧已有测试明确
验证 workspace 中不存在 `task_info.json` 和 `evaluation/`。因此，release 根目录
`task_info.json` 中的论文题名、DOI 和期刊不是本轮的 Agent 泄露面。

## 2. 总体结论

### 2.1 两种模式的基本设计成立

四篇任务都实现了以下基本区别：

- reproduction 披露论文支持的具体软件、方法、basis、solvation、thermochemistry 或
  reaction-path route；
- autonomous 不披露上述具体路线，要求被评测 Agent 自行选择和论证计算策略；
- 两种模式使用相同的科学对象和 public inputs；
- autonomous 没有看到论文 PDF/SI、reference key points、reference conclusions 或
  scoring rules；
- public data 中没有隐藏 numeric target 或 tolerance。

因此，没有发现 autonomous `agent_input` 直接泄露 Gaussian 版本、B3LYP/CBS-QB3、QST3、
SMD 双层路线或论文数值答案。

### 2.2 当前 autonomous 是“方法自主验证”，不是开放发现

四篇 autonomous 都继承了论文已经选定的研究对象：

- `2aca`：给定 EDY15/16/17 和明确 Bergman reaction center；
- `611`：给定两个 source-selected rotamers；
- `76ae`：给定两个 source-selected TS2 candidate geometries 和 stereochemical labels；
- `9455`：给定 source-selected P1/P2，而不是让 Agent 在 P1–P38 中发现候选。

Agent 自主决定的是“如何算、如何验证和如何解释”，不是“研究哪个对象、搜索哪些候选”。
这与当前 reproduction-first 派生设计一致，但任务类型应被理解为：

```text
method-autonomous validation / comparison
```

而不是 open-ended autonomous discovery。若 benchmark 的目标就是评估不依赖论文路线的
计算能力，该设计合理；若目标是评估完整的自主科研选题、候选生成和机制发现能力，则当前
难度明显不足。

### 2.3 仍有一个直接答案泄露和数个间接提示

最明确的问题不在 autonomous，而在 `paper_2aca...` 的 reproduction public schema：

```json
"prefixItems": [
  {"const": "EDY16"},
  {"const": "EDY15"},
  {"const": "EDY17"}
]
```

它直接公开了正确 barrier ordering。Stage07 只删除了 `task.md` 中的答案，没有检查到
schema。

autonomous 没有同等级直接答案泄露，但存在以下较弱问题：

- `611` 写着 “A method different from the paper's may be used”，无意义地告诉 Agent 这是
  从论文任务转换而来；
- `611` 的 schema 要求输出 `both_bright` 和 `closely_similar`，但 task 没有定义 brightness
  或 similarity threshold；
- `9455` 公开实验区间和已经筛选出的 P1/P2，使任务成为确认式验证，而不是产品发现；
- `76ae` 的 `TS2-R-S`、`TS2-S-R` 文件名保留论文步骤和立体标签。标签对保持输入身份有用，
  但也说明候选和反应步骤已经由论文选择；
- `2aca` 的 “Do not infer a conclusion from DSC temperatures alone” 暗示论文还有 DSC 证据，
  对没有拿到 DSC 数据的 Agent 没有实际帮助，也不是完成计算所需边界。

## 3. 逐篇双模式审查

### 3.1 `paper_2aca1dd116799b28`

#### Reproduction

设计合理部分：

- 目标是重现 EDY15/16/17 Bergman cyclization barriers；
- public input 为三个完整 reactant XYZ；
- charge、multiplicity、gas-phase、reaction center 清楚；
- route 给出 Gaussian 09、restricted/unrestricted B3LYP/6-31G(d,p)、QST3、frequency、IRC；
- 要求 reactant/product minima、单虚频 TS 和 IRC endpoint，不是只比最终数字；
- evaluator 覆盖三个 barrier、reaction-path validation、ordering 和 conclusion。

问题：

1. reproduction schema 硬编码正确 ordering，属于直接答案泄露；
2. task 要求 construction product 和 TS guess，但 public input 只有 reactant。论文没有给出
   QST3 guess construction，任务仍可执行，但不同 Agent 的初猜负担差异较大；
3. 论文没有说明表格 barrier 的具体 thermochemical definition，3 kcal/mol tolerance 是合理
   初始处理，但三个 barrier 间隔小于 tolerance，最终主要依赖独立 ordering rule。

#### Autonomous

没有发现 Gaussian、B3LYP、QST3、IRC keyword、MAXPOINTS 或论文 barrier 数值泄露。它正确
要求 Agent 自行选择 TS search 和 reaction-path validation 方法。

reaction center C17–C32 和 C15/C16 diradical center 是定义目标所需的科学边界，不应当被
当成论文路线泄露。否则被评测 Agent无法知道要计算哪个反应。

问题主要有两个：

- “Do not infer a conclusion from DSC temperatures alone” 是不必要的 source-context 提示；
- autonomous evaluator 仍以论文三个 barrier 为 target，只把 tolerance 从 3 增加到
  4 kcal/mol。若 Agent 选择不同但合理的模型化学，绝对 barrier 可能系统偏移，而 ordering
  和 reaction-path validity 仍正确。当前评分可能低估方法自主任务。

结论：autonomous route hiding 基本合格；reproduction schema 必须修复后才能入库。

### 3.2 `paper_611000e1de080f6f`

#### Reproduction

当前任务不再把 31 原子坐标错误声明为完整实验化合物，而是定义成 coordinate-defined 4a
computational model。这是必要且诚实的边界修正。

route 披露 Gaussian 16、TD-B3LYP/6-31G(d,p)、CPCM acetonitrile、S1 optimization、root
tracking 和 vertical emission extraction，足以执行。

但仍有三项科学风险：

1. 正文 general calculation paragraph 强调 M06，而 SI coordinate header 标成 RB3LYP；
   Stage06 选择 B3LYP 有 source basis，但不能说论文路线完全无歧义；
2. public task 将输入称为 “two supplied bright rotamers”，提前给出 brightness conclusion；
3. “do not replace with the orthogonal dark-state structure” 提供论文中的负向候选线索。它能
   防止算错对象，但也泄露了论文存在另一暗态结构。

#### Autonomous

Stage07 已删除 autonomous 中的 orthogonal dark-state 提示。最终任务没有具体 functional、
basis、software 或 paper route。

仍有两个问题：

- “A method different from the paper's may be used” 暴露了转换痕迹，且 Agent 根本看不到
  论文，应该改成单纯要求选择并论证方法；
- `both_bright`、`closely_similar` 是强制 boolean 字段，但 public contract 不定义判定尺度。
  evaluator 虽有 numeric targets，却没有解释 boolean 如何由 numeric result 导出。

更重要的是，autonomous evaluator 使用论文精确结果：

- emission energy tolerance：0.08 eV；
- oscillator strength tolerance：0.08。

对于明确允许换方法的任务，这个尺度可能仍过度绑定 B3LYP result。应重点评估：S1 是否
正确、计算是否收敛、state tracking 是否可信、两构象相对趋势是否一致，再由人工校准绝对
数值 tolerance。

结论：没有直接 paper-route 泄露，但任务代表性、bright/dark 提示和评分尺度都需要重点
人工复核。

### 3.3 `paper_76ae2dc25f0a5aeb`

#### Reproduction

这是双模式结构最清楚的一篇。reproduction 完整披露：

- Gaussian 16；
- B3LYP-D3(BJ)/6-31G(d) gas-phase TS optimization/frequency；
- B3LYP-D3(BJ)/6-311+G(d,p) SMD(toluene) single point；
- `G_solution = E_SMD + G_thermal_correction`；
- 298.15 K 和 signed ΔΔG 定义；
- 虚频 mode 必须对应 sulfur attack / oxetane C–O cleavage。

任务、schema 和 evaluator 对同一科学对象，未发现公开 reference answer。

#### Autonomous

没有具体软件、functional、basis 或论文数值泄露。Agent 可以自行选择 electronic structure、
solvation、thermochemistry 和 TS validation 方法。

`TS2-R-S`、`TS2-S-R` 标签以及文件注释 “TS starting geometry” 会告诉 Agent 这两个结构是
论文选定的 competing TS candidates。对于 validation/comparison，这是必要输入身份；对于
discovery，则属于候选选择已完成。因此问题是任务定位，不是答案泄露。

两个改进点：

1. autonomous evaluator 基本复制 reproduction reference，仍要求论文虚频附近
   `±35 cm-1` 和 `ΔΔG = 1.9 ± 0.6 kcal/mol`。这与自由方法选择不完全匹配；
2. schema 要把两个 126 原子 optimized geometries 作为 252 个 JSON object 嵌入
   `results.json`，体积大、对 Agent 输出不友好，而且当前 scoring rules 没有绑定这些
   coordinates。独立 XYZ artifact 会更简单、可验证。

结论：route hiding 合格、科学目标清楚；自主评分和交付格式仍可精简。

### 3.4 `paper_9455a82229de2427`

#### Reproduction

任务给出 CBS-QB3 的完整 route，并要求 0 K E0、molecular minima、atomic-H reaction balance
和 P1/P2 experimental interval comparison。Stage07 又补上 P1/P2 reaction-energy key points
和 scoring rules，最终 evaluator 覆盖完整。

严格 absolute total energy tolerance `1e-5 Hartree` 对 exact-route reproduction 可以理解，
但容易受 Gaussian revision/defaults 影响。任务核心是 reaction energy，不应让绝对总能量
占据不成比例的评分权重。

#### Autonomous

没有 CBS-QB3、Gaussian、B3LYP/CBSB7、CCSD(T)、MP4 或 MP2 route 泄露。任务正确要求
Agent 自选适合 open-shell/closed-shell species 的方法，说明 0 K energy convention 和
uncertainty。

公开 `-162 ± 27 kJ/mol` experimental interval 本身不是论文计算路线，也不是 P1/P2 隐藏
计算答案。是否公开它取决于任务定义：

- 如果目标是“给定实验边界，验证 P1/P2”，公开合理；
- 如果目标是“盲预测实验 exoergicity 或发现产品”，则属于 target leakage。

当前任务明确写成 validation，因此在现有合同下合理。但只给 P1/P2 而不给其他 36 个候选，
意味着 Agent 不能发现产品，只能验证论文已经筛选出的候选。

结论：四篇中 autonomous evaluator 与方法自由度匹配最好；自主性仍限于方法而非候选发现。

## 4. Evaluator 完整性和可执行性

四篇两种模式的 evaluator 文件均存在、非空，numeric rules 都有 target、unit、tolerance 和
binding。不存在早期版本那种空模板或只有笼统语义句的问题。

但“文件完整”和“评分科学公平”是两件事。本轮主要发现：

1. reproduction-first 让 Agent 倾向于复制 evaluator，再只修改 method rule 和 tolerance；
2. `76ae` autonomous 几乎完整复制 reproduction numeric references；
3. `611` autonomous 只把 tolerance 从 0.05 调到 0.08；
4. `2aca` autonomous 只把 tolerance 从 3 调到 4 kcal/mol；
5. `9455` autonomous 删除了 absolute-energy rules，只保留 reaction energies、interval 和
   conclusion，反而更符合方法自主任务。

所以当前最好的 autonomous evaluator 派生方式不是“统一放宽 tolerance”，而是重新判断：

- 哪些过程性证据与方法无关；
- 哪些最终趋势必须稳定；
- 哪些绝对数字会随合理方法改变；
- 是否应分别评分 physical validity、internal consistency、ordering 和 numeric proximity。

这仍应由 Stage06/07 Agent 科学判断，不适合写成代码固定规则。

## 5. Stage06/07 运行轨迹中的积极信号

### 5.1 layout 证据工具实际解决问题

五篇 Stage06 和四篇 Stage07 都使用了 `document_query.py`。`2aca` 因此从原始 PDF layout
恢复了被 Markdown 粘连的坐标，`611` 也跨页验证了两个 S0/S1 coordinate headers。

### 5.2 Stage06 self-check 确实修复过真实问题

`paper_9455...` 的 Stage06 初稿曾把整份 SI-derived `document.md` 复制到两个 public
`data/inputs/si_coordinate_source.md`。第一次 full-pair Gate 明确失败：

```text
autonomous_research:paper_source_material_exposed:data/inputs/si_coordinate_source.md
```

Agent 随后删除 source material，只保留完成任务所需的 coordinates，并再次运行 Gate 至
passed。这个轨迹说明：

- public paper-material content check 有实际价值；
- self-check 不是形式动作；
- 最终 release 没有 PDF/SI 或整篇衍生正文泄露。

### 5.3 Stage07 有效修复了科学质量

- `2aca`：删除两个 task.md 中的预期 ordering；
- `611`：删除 autonomous 中 orthogonal dark-state 提示；
- `9455`：限制过度结论，并补齐两个核心 reaction-energy rules；
- `76ae`：无修复，candidate 与 audited task 一致。

其中 `9455` 的修复最能证明 Stage07 不只是复述 Gate，而是在审计科学 scope 和 evaluator。

## 6. 运行轨迹暴露的其他问题

### 6.1 Stage07 repair receipt 不总是真实

`611` 的 autonomous task 实际发生修改，但 receipt 写成：

```json
"audit_decision": "approved",
"repairs": []
```

内容结果变好，但 provenance 错误。当前代码相信 Agent 自报 repairs，没有用真实文件 diff
进行机械核对。

### 6.2 Stage07 的复制指令与 sandbox 冲突

四篇 Stage07 都尝试：

```text
rm -rf outputs/audited_task && cp -a inputs/candidate outputs/audited_task
```

命令均被 destructive-command policy 拒绝，之后才改用安全复制。问题完全可避免，而且与
科学审计无关。

### 6.3 Agent 会探测不可用工具

运行中出现：

- `pdftotext: command not found`；
- `jq: command not found`；
- `rdkit` 不存在；
- sandbox 无网络时尝试 `pip install pymupdf`；
- 少量 shell quoting/awk command 错误。

这些失败没有触发 pipeline retry，也没有导致 technical block，但消耗 tool budget。
`paper_9455...` 的 Stage06 实际发起 67 次 command，比其他 Stage06 的 26–37 次明显更高，
与反复提取、复制 source、Gate 失败后修复有关。

### 6.4 document query 还不够方便

Agent 多次尝试 `pdftotext -f ... -l ...`，说明它需要连续页范围，而现有 query CLI 主要是
单页或关键词上下文。增加通用 page-range 读取可以减少工具探测，不需要引入任何化学规则。

### 6.5 机械 Gate 通过不等于语义审计完成

`2aca` 的 schema answer leak 在 Stage06 self-check、external Gate 和 Stage07 Gate 中全部
通过。这是符合当前 Gate 边界的：Gate 能检查 schema 可解析，不能用通用机械规则判断某个
`const` 是否恰好等于论文答案。

真正的问题是 Stage06/07 虽被 Prompt 要求检查完整 public surface，模型仍把主要注意力
放在 task.md 上。不能通过向 Gate 添加数值黑名单解决，应强化语义审计步骤。

### 6.6 Metadata 完整但文本规范化不足

release metadata 已不再为空，但 `paper_9455...` 标题仍含 HTML entity，个别作者名存在分离
重音符号或大小写异常。这不影响被评测 Agent，因为 metadata 不进入 workspace，但影响数据
展示、检索和人工管理。

## 7. 问题优先级

### P0：正式入库前必须处理

1. 删除 `2aca` reproduction schema 中固定正确 ordering；
2. 全面复核 `611` reproduction 的 bright/dark 提示和 coordinate-defined model 代表性；
3. 确保任何实际 Stage07 修改都在 receipt 中记录。

### P1：影响 autonomous 评分公平性

1. 重新审查 `2aca/611/76ae` autonomous tolerance 与方法自由度；
2. 明确定义或取消 `611` 的 `both_bright/closely_similar` 主观 boolean；
3. 将 `76ae` 大型 coordinate JSON deliverable 改为独立 artifact，避免无评分绑定的大输出。

### P2：运行效率和可维护性

1. Stage07 进入 Agent 前机械预复制 candidate，避免 `rm -rf`；
2. Prompt 明确优先使用现成 query，不安装 PDF 包；
3. query CLI 支持 page range；
4. canonical metadata 做 HTML unescape 和 Unicode normalization。

## 8. 建议的最小改进方向

不扩大 Gate，不添加论文关键词或固定数值规则。只做以下通用调整：

1. Stage06 在派生 autonomous 后，分别列出两种模式所有 `agent_input` 文件，并与 hidden
   reference/conclusion 做语义对照；
2. Stage07 对 reproduction 和 autonomous 都检查 task、schema、data filename/comment，
   不把 public-surface audit 只理解为 task.md；
3. Stage07 单独回答：“autonomous evaluator 是否与它允许的方法自由度相容”；
4. 代码只负责计算 candidate/audited task 的 changed-file list，Agent 负责解释修复原因；
5. benchmark 文档明确 autonomous 的当前定义是“固定科学对象下的方法自主验证”，避免将其
   误称为完整 open discovery。

## 9. 最终评价

两种模式不是简单复制：task route 和 method schema 已发生真实转换，autonomous 的具体论文
路线隐藏总体合格。当前主要问题已经从“缺文件、Gate 阻断”转移为更高层次的质量问题：

- 个别公开 schema 泄露答案；
- autonomous 任务的候选对象仍由论文预选；
- evaluator 对方法自由度适配不足；
- Stage07 有效修复但记录不完全可信；
- 工具接口仍产生可避免的失败和调用浪费。

这说明 v20 的基础结构已经可用，但正式批量生成前还需要一轮针对 public-surface 语义审计
和 autonomous evaluator coherence 的小范围优化。

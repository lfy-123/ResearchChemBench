# Stage06/07 v22 已发布任务与 v20 对比质量分析

## 1. 分析范围

本报告逐文件比较以下两轮相同论文输出：

- 旧逻辑：`runs/stage0607-v20-gpt-5.6-sol-20260827-model-driven-input-closure-5`
- 新逻辑：`runs/stage0607-v22-gpt-5.6-sol-20260827-dual-mode-five`

重点检查 v22 最终发布的三篇：

- `paper_2aca1dd116799b28`
- `paper_611000e1de080f6f`
- `paper_9455a82229de2427`

比较对象包括两种模式的 `task.md`、公开输入、`submission_schema.json`、参考关键点、参考结论、
评分规则、evidence map、critical failures、Stage07 修复记录和运行轨迹。

## 2. 总体判断

v22 在任务的科研性、输入隔离和双模式区分上明显优于 v20，但没有完全达到修改方案预期。

| 维度 | v20 | v22 | 判断 |
|---|---|---|---|
| reproduction 定义 | 公开论文软件和详细计算步骤 | 公开作者科学路线，由 Agent 自主规划计算 | 明显改善 |
| autonomous 定义 | 多数只是删除指定方法 | 隐藏作者路线，要求自主提出假设/候选/机理 | 明显改善 |
| 公开输入 | 经常提供论文选定或优化的结构 | 主要提供 identity-level 输入和物理边界 | 明显改善 |
| 科学目标 | 经常缩成局部数值复算 | 更接近论文核心发现或机理问题 | 明显改善 |
| evaluator 覆盖 | 数值和简单结论为主 | 加入搜索、验证、机理、假设、局限性 | 改善 |
| evaluator 可执行绑定 | 多数直接绑定精确数值字段 | 多处只绑定数组或数组下不存在的直接字段 | 出现退步 |
| 答案泄露 | v20 Stage07 能修复 2aca 排序泄露 | v22 Stage07 错误放过同类泄露 | 明显问题 |
| 发布稳定性 | 4/5 发布 | 3/5 发布，1 technical_blocked | 退步 |
| Stage06 成本 | 约 8.62M tokens（五篇） | 约 27.97M tokens（五篇） | 约 3.24 倍，明显退步 |

所以本轮可以评价为：**模式设计方向正确，三篇中的两篇质量明显提升，但尚不能判定 v22 已完全
实现方案。**

## 3. 逐篇任务指令对比

### 3.1 `paper_611...`：本轮提升最明显

#### v20

v20 将任务缩成两个已选 bright rotamer 的 S1 几何优化和发射能/振子强度复算：

- reproduction 直接指定 Gaussian 16、TD-B3LYP/6-31G(d,p)、CPCM、Root=1；
- autonomous 仍使用论文选定的 `rotamer_A.xyz` 和 `rotamer_B.xyz`；
- 两种模式都只判断两个 bright rotamer 是否相似；
- 没有覆盖论文更核心的 dark TICT minimum 及 4a/4b 对照机理。

这更像一个局部计算 recipe，而不是完整的科学评估任务。公开的两个 rotamer 还是论文筛选后的
结构性结果，显著缩小了搜索空间。

#### v22

v22 将科学目标改成：

- reproduction：验证作者提出的 4a dark TICT basin、扭转/电荷转移路线以及 4b control；
- autonomous：不知道 TICT 路线，自主比较多种 excited-state relaxation 假设，搜索 4a/4b
  的 bright/dark basins；
- 输入从两个结果性 XYZ 改成 4a/4b 的 SMILES、分子身份、溶剂和 singlet manifold；
- 两种模式均自主选择 excited-state method、solvation、state tracking 和搜索方法；
- 要求 minimum validation、same-surface connectivity、state identity、charge-transfer
  diagnostics、method sensitivity 和 uncertainty。

#### evaluator 对比

v20 evaluator 只有两组 bright emission energy、oscillator strength 和“两个 rotamer 相似”。
v22 evaluator 覆盖：

- dark minimum twist angle；
- dark basin 相对 bright basin 的能量；
- dark-state emission energy 和 oscillator strength；
- bright-state property；
- charge-transfer character；
- 4b 对照结论；
- minimum/state/path validation；
- autonomous hypothesis search；
- 最终 differential TICT conclusion。

Stage07 还发现相对能量缺少 reference，修复了 task、schema，并补入 0.51 eV 的私有评分点。
这说明新版 Stage07 在这一篇确实发挥了科学审计和有界修复作用。

#### 结论

这一篇基本达到 v22 方案预期，也是最能证明新模式有价值的样本。唯一重要风险是任务范围和计算
成本显著增加：从两个给定 rotamer 的局部复算升级为两个分子的 excited-state landscape 搜索，
但没有给出计算预算和足够明确的搜索停止标准，可能导致被评测 Agent 的完成率降低。

### 3.2 `paper_945...`：自主科研模式从“验证候选”变成真正的候选发现

#### v20

v20 直接向两种模式提供 P1/P2 产品坐标：

- reproduction 指定 Gaussian 16 CBS-QB3 的完整执行流程；
- autonomous 虽可自行选方法，但仍只需验证已经给出的 P1/P2；
- autonomous 不需要提出候选产品，实际只是 method-independent validation；
- 论文的关键产物身份已经通过坐标公开，存在明显答案捷径。

#### v22

v22 只公开 SiN、isoprene、H-loss stoichiometry、charge/spin、单碰撞条件和实验反应能：

- reproduction 获得作者提出的两个 cyclic product 候选和定性反应路线，但不获得产品坐标、
  CBS-QB3 protocol、参考能量或排序；
- autonomous 不获得 P1/P2 名称、结构或反应路线，必须提出 SiNC5H7 connectivity hypothesis
  space，生成、去重、筛选和排序不同连接类型；
- 两种模式都需要验证 minima、电子态、E0 一致性、sensitivity 和 uncertainty；
- 明确限制：热化学一致不能单独证明 branching 或完整动力学机理。

这与用户期望的定义高度一致：reproduction 得到作者候选路线，自主科研模式只得到科学问题和
研究前实验边界。

#### evaluator 对比

v20 autonomous evaluator 只有 P1/P2 两个反应能、实验区间和结论。v22 autonomous evaluator
增加：

- 是否自主发现两个领先 cyclic assignments；
- 是否搜索不同 connectivity classes；
- generation/deduplication/screening/promotion 的搜索证据；
- minimum/state/convergence/sensitivity validation；
- 产物排序和实验区间；
- 对 branching/完整机理的合理限制。

#### 结论

这篇基本达到 v22 预期，且相比 v20 是实质性升级。不过 autonomous 要求至少三个 ranked
products、至少两类 connectivity，并发现论文两个领先候选，却没有计算预算或覆盖率停止条件。
“没有发现更低候选”本身难以严格证明，可能使任务对不同 Agent 的资源使用不公平。

### 3.3 `paper_2aca...`：科研性提高，但 reproduction 泄露排序答案

#### v20

v20 向 Agent 提供论文 reactant XYZ 和固定原子标签，并在 reproduction 中指定：

- Gaussian 09；
- RB3LYP/6-31G(d,p) minima；
- UB3LYP/6-31G(d,p) QST3；
- frequency、IRC 和 MAXPOINTS；
- 固定 C17-C32 bond formation。

这是一套论文 protocol 复跑任务。v20 Stage07 曾经明确发现并移除 public objective 中泄露的
`EDY16 < EDY15 < EDY17` 排序。

#### v22 的改善

- 输入改为三个化合物的系统命名和 substitution identity，不再提供论文选定的 reactant
  geometry；
- 两种模式都自主选择软件、方法、open-shell treatment、conformer strategy 和 energy
  convention；
- reproduction 只应获得作者 charge-transfer/delocalization scientific route；
- autonomous 必须提出至少两个可区分解释，并用 observables 比较；
- validation 加入 conformer sensitivity、open-shell/multireference diagnostics、method
  sensitivity 和 uncertainty。

#### 未达到预期之处

v22 reproduction 的公开 objective 直接写出：

- donor-acceptor 16 preferentially stabilized；
- donor-donor 15 intermediate；
- acceptor-acceptor 17 least reactive。

这等价于公开了 barrier/reactivity 的方向排序。v22 方案允许公开作者的假设、候选或定性机理，
但明确要求隐藏 reference ordering 和完整结论。Stage07 的审计报告却声称 reproduction
“withholding ordering”，与实际 `task.md` 不一致。

更值得注意的是，v20 Stage07 已经能发现并修复同一论文的排序泄露，而 v22 反而没有发现，说明
新版 author-route disclosure 规则产生了过宽解释：审计 Agent 把结果方向也误归为科学路线。

#### 结论

这篇的任务范围和自主科研要求比 v20 更好，但 reproduction 不符合 v22 的隐藏答案边界，不能
视为完全合格发布任务。应将公开 route 改成“作者提出通过电荷转移/畸变解释取代基效应”，而不
说明哪个化合物最低、居中或最高。

## 4. evaluator 文件的总体变化

### 4.1 改善

新版 evaluator 不再只是数值答案表，整体上更接近真正的计算化学评估：

- key points 包含过程关键节点、结构/电子性质和验证证据；
- conclusion 有明确、实际的论文参考结论；
- scoring rules 同时覆盖 numeric、ordering、condition 和 semantic；
- critical failures 从 2–3 条增加到 4–6 条，且多为任务特定的严重科学失败；
- evidence map 更完整，2aca 从 3 条增加到 6–9 条，945 增加到 8 条；
- tolerance 随 method freedom 合理放宽，并只产生人工科学复核 diagnostic，不机械阻断。

从“是否把关键点、结论和初步评估方法写出来”这一要求看，三篇都明显好于 v20，文件也不是空
模板。

### 4.2 新问题：评分绑定丰富了，但机器可执行性下降

多条 v22 规则的 `binding.fields` 只指向集合，而不是实际数值字段：

- 2aca numeric barriers 绑定 `$.systems`，没有绑定具体 label 对应的
  `activation_barrier`；
- 945 numeric energies 绑定 `$.products` 或 `$.ranked_products`，没有指定哪一产品及
  `reaction_energy_0K_kJ_mol`；
- 611 的 numeric path 写成 `$.molecules.4a.regions.twist_angle_deg`，但 `regions` 是数组，
  该路径缺少数组选择或 dark-region 判定条件。

相较之下，v20 经常直接绑定如 `$.compounds.EDY15.barrier_kcal_mol`，虽然 evaluator 较简单，
但字段定位更明确。

此外，2aca autonomous 将三个数值 barrier 合并进一个 `semantic` rule，并在 expected 文本中
写“within 2.5 kcal/mol”，而不是为三个值建立明确 numeric rule。它对人工语义评分仍可用，
但不符合“具体、可执行的数值评分”最佳实践。

因此，当前 Gate 证明的是“规则和 binding 字段存在”，没有充分证明 evaluator 能稳定地自动
找到数组中正确对象并执行比较。这个问题不会造成当前 Gate 阻断，却会在真正运行 benchmark
grader 时暴露。

## 5. 当前运行结果中的问题

### 5.1 发布率下降

- v20：4/5 published，1 scientific rejection；
- v22：3/5 published，1 scientific rejection，1 technical blocked。

`a556` 两轮都因缺少唯一分子输入而科学拒绝，结论稳定且合理。下降来自 `paper_76ae...`。

### 5.2 `paper_76ae...` 不是科学失败

该 Agent 已完成 reproduction 及其 self-check，但之后重复执行 `find outputs`、读取同一报告并
反复声明“继续构建 autonomous”，最终在第 152 次工具调用后返回 `constructed`。配置上限是
180，因此它不是严格意义上的 hard-limit exhaustion，而是**在预算仍有剩余时提前返回了错误
终态**。此时 autonomous 的三个公开文件和五个 evaluator 文件全部不存在，外部 Gate 正确将其
判为 `technical_blocked`。

根因更接近单次 Agent 内的非进展循环和阶段切换失败，而不是 API、resume 或 Gate 误阻断。

### 5.3 Stage06 成本显著上升

五篇 Stage06 合计 token：

- v20：约 8.62M；
- v22：约 27.97M；
- v22 约为 v20 的 3.24 倍。

主要异常样本：

- `paper_76ae...`：约 12.45M tokens、150 个已完成 shell 调用，最终仍不完整；
- `paper_945...`：约 8.13M tokens、106 个 shell 调用，虽然最终发布，但 terminal audit/
  receipt 写入前出现大量重复检查；
- `paper_a556...`：科学拒绝也使用约 3.11M tokens 和 60 个 shell 调用。

2aca 和 611 的开销只比 v20 温和上升，说明成本问题并非“新版科学任务必然更贵”，而是特定
轨迹发生重复检查和终止困难。

### 5.4 任务科学闭合与运行可行性尚未统一

v22 更严格地移除了论文结果结构，但也把结构构建和搜索成本转移给被评测 Agent：

- 2aca 要从系统命名构建三个较大分子、做 conformer search、open-shell TS 和路径验证；
- 611 要搜索两个分子的 excited-state landscapes 和 same-surface paths；
- 945 autonomous 要做开放的 SiNC5H7 constitutional-isomer search。

这些任务科学上更真实，但尚无明确计算预算、搜索停止条件或“最低充分证据”边界。没有这类边界，
任务可能完整但不适合在统一 benchmark runtime 中公平执行。

### 5.5 通用 toolbox 输入噪声

2aca 两种模式都携带约 187 KB 的 `toolbox_capabilities.json`。它没有泄露论文结果，也不是固定
protocol，但大部分内容与该任务无关，会增加 Agent 阅读和搜索成本。应考虑按实际 runtime
能力生成通用但相关的能力视图，而不是复制整个 catalog；不应采用论文关键词特例裁剪。

## 6. 对 v22 修改方案的逐项验收

| 方案要求 | 验收结果 |
|---|---|
| reproduction 公开作者科学路线，不公开论文计算 protocol | 三篇均不公开 protocol；611/945 合格，2aca 路线夹带结果方向 |
| autonomous 隐藏作者路线并自主提出路线 | 三篇已发布任务基本合格 |
| 两种模式均自主规划计算 | 合格 |
| 不提供结果性 TS/intermediate/conformer | 合格 |
| 纯计算任务不强制虚假 discovery | 未在三篇中发现明显违反，但这三篇都有真实比较/假设空间 |
| evaluator 完整、具体、非空模板 | 合格 |
| evaluator 可执行且与 schema 对齐 | 语义上对齐，但数组绑定不够精确，部分不完全合格 |
| Stage07 专注审计和有界修复 | 611 表现良好，945 无需修复，2aca 漏检关键泄露 |
| Gate 只做机械合同检查 | 合格；当前问题也说明科学泄露不能依赖机械 Gate |
| 运行稳定、一次完成 | 未达到；76ae technical blocked，945 有明显重复终止轨迹 |

## 7. 最终结论与优先级

本轮不是“质量下降导致只有三篇发布”，而是两种因素叠加：

1. **科学任务质量总体提升**：尤其是 611 和 945，已经从论文 recipe/给定候选验证升级为用户
   期望的科学目标、作者路线提示和自主研究差异；
2. **流程和审计仍有缺口**：76ae 的失败是 Stage06 非进展循环，2aca 是 Stage07 对答案泄露
   漏检，评分 binding 还存在自动执行歧义。

建议后续按以下优先级处理：

1. 先修复 Stage06/Stage07 对“作者科学路线”与“结果方向/排序”的通用语义边界；
2. 修复 Stage06 reproduction self-check 后的阶段切换和 terminal receipt 非进展循环；
3. 让 evaluator binding 精确定位数组元素及数值字段，同时保持 Gate 不判断 tolerance 科学选择；
4. 为开放搜索型任务在 prompt 中要求 Agent 给出任务特定、科学合理的计算预算与停止标准，仍由
   Agent 设计，不由代码预处理化学输入；
5. 完成上述修正后重跑 2aca、76ae、945 三篇即可验证关键问题，无需立即重跑全部五篇。

# Stage06/07 v20 五篇回归与合成任务质量分析

## 1. 审查结论

v20 已经解决本轮方案针对的两个主要工程问题：

1. Stage06/07 可以通过通用 PDF layout 证据层区分“派生 Markdown 损坏”和“原始科学
   证据缺失”；
2. 标题、DOI、期刊、发布日期和作者可以沿 canonical paper metadata 链路进入 release。

固定五篇回归最终为：

- 4 篇发布；
- 1 篇科学拒绝；
- 0 篇 technical block；
- 0 篇机械 Gate 阻断；
- Stage06 Agent self-check 与 external Gate 对已构建任务均为 passed。

相较 v19.1 的 2 篇发布，v20 恢复了 `paper_2aca...` 这篇此前因坐标列解析粘连而被
误拒绝的任务；`paper_a556...` 仍因真实的计算定义缺失而被科学拒绝。说明通过率提升主要
来自证据访问能力改善，而不是放宽 Gate 或降低科学闭合标准。

但是，四篇发布任务不能全部不经人工复核直接进入正式 benchmark：

- `paper_2aca...` 的 reproduction `submission_schema.json` 将正确 barrier ordering 写成
  固定 `const`，公开面仍存在答案泄露；
- `paper_611...` 是从“完整实验化合物”改成“SI 坐标定义的 31 原子 computational
  model”后才成立，科学边界自洽，但其论文中心性和模型代表性需要人工重点复核；
- `paper_611...` 的 Stage07 实际修改了 autonomous task，却在 audit receipt 中声明无修复；
- 部分 autonomous evaluator 允许自由选方法，却继续使用接近论文路线结果的较窄数值
  tolerance，公共任务自由度与评分尺度尚未完全匹配；
- canonical metadata 已完整，但个别 HTML entity 和作者字符仍未做足够的通用文本归一化。

因此，本轮总体判断是：**v20 的工程方向成立，任务质量和有效召回率均提高，但语义泄露
审计、autonomous evaluator 一致性和审计回执真实性仍需一轮小而通用的改进。**

## 2. 测试配置和产物位置

测试 run：

```text
runs/stage0607-v20-gpt-5.6-sol-20260827-model-driven-input-closure-5
```

最终 release：

```text
runs/stage0607-v20-gpt-5.6-sol-20260827-model-driven-input-closure-5/release
```

配置：

- Stage06 model：`gpt-5.6-sol`；
- Stage07 model：`gpt-5.6-sol`；
- reasoning effort：`high`；
- 并发数：5；
- 五篇从同一时点开始，全部正常完成；
- 最长单篇约 15 分 37 秒；
- batch `failed_count = 0`。

代码实现提交：

```text
b0bbf81 feat(stage0607): add model-driven evidence closure
```

代码验证：

- v19/v20/late-stage 定向测试：22 passed；
- 全量测试：409 passed；
- `git diff --check`：通过；
- 真实 `paper_2aca...` SI：84 页、2370 个 layout blocks；原 PDF layout 成功保留第 26 页
  坐标 `-2.783404  -1.943641  0.767615` 的列边界。

## 3. 最终结果

| paper_id | Stage06 | Stage07 | 最终结果 | 主要判断 |
|---|---|---|---|---|
| `paper_2aca1dd116799b28` | candidate ready | approved with repairs | published | 旧解析误拒绝已解决；Stage07 删除 task 中答案泄露，但漏查 schema 泄露 |
| `paper_611000e1de080f6f` | candidate ready | approved | published | 改为 coordinate-defined model 后内部闭合；需人工判断模型代表性 |
| `paper_76ae2dc25f0a5aeb` | candidate ready | approved | published | 输入、路线、双模式差异和 evaluator 最完整稳定 |
| `paper_9455a82229de2427` | candidate ready | approved with repairs | published | Stage07 补齐核心 reaction-energy 评分并限制结论范围 |
| `paper_a5564360a31f760b` | scientific not constructible | 未进入 Stage07 | scientific rejection | 关键计算定义和边界确实无法从原始证据唯一恢复 |

v19.1 基线只有 `paper_76ae...` 和 `paper_9455...` 发布。本轮新增发布的两篇需要分别看待：

- `paper_2aca...` 是明确修复了解析表示造成的假阴性；
- `paper_611...` 不是恢复原来那个“完整实验化合物”的任务，而是重新限定为 SI 坐标
  唯一定义的 computational model validation，属于科学目标边界的收缩和澄清。

## 4. 运行轨迹审查

### 4.1 正常行为

五篇 Stage06 都实际调用了 `document_query.py`。Stage07 对四篇候选也使用了 layout 查询。
这证明新增工具不是只存在于代码或 Prompt 中，而是进入了实际模型工作流。

最关键的成功案例是 `paper_2aca...`：

1. normalized Markdown 中坐标列粘连；
2. Stage06 查询原 PDF layout；
3. 恢复完整、连续的 EDY15/16/17 坐标；
4. 检查标签、原子索引、反应中心和 barrier 映射；
5. 完成 reproduction-first 双模式任务；
6. reproduction self-check、full-pair self-check 和 external Gate 全部通过；
7. Stage07 再进行独立科学审计和有限修复。

该轨迹符合 v20 设定的“模型判断科学输入，代码只提供证据访问”边界。

`paper_a556...` 也体现了拒绝逻辑没有被放宽。Stage06 明确区分了：

- 数值 target 清楚；
- 化学身份和 methyl truncation 基本清楚；
- 但 S1 state-following、reorganization energy 定义、RMSD protocol、Huang–Rhys/mode
  mapping、environment 和 conformer boundary 不闭合。

Agent 还回查了原始/layout 证据，并说明拒绝不是由 Markdown/OCR 损坏造成。这是合理的
科学拒绝。

### 4.2 不必要的工具探测

虽然没有 retry、任务中断或 technical block，Agent 仍尝试过环境中不可用或不必要的工具：

- `pdftotext`；
- `jq`；
- `awk`；
- `rdkit`；
- `pip install pymupdf`。

失败后 Agent 均回到现成的 `document_query.py`，所以没有影响最终结果。但这增加了工具
调用和上下文开销。根因不是 API 或 retry，而是 Prompt 只介绍了可用查询工具，没有明确
说明无需安装/探测其他 PDF 工具；当前查询 CLI 也只有单页读取，长区间核查不够方便。

### 4.3 Stage07 初始复制动作与 sandbox 冲突

四篇 Stage07 都首先尝试使用 `rm -rf outputs/audited_task && cp -a ...`。该命令被 Agent
sandbox 的 destructive-command policy 拒绝，之后 Agent 改用安全方式继续。该问题没有
造成失败，但每篇都产生一次无意义的工具错误。

这是工程接口不匹配：Prompt 要求 Agent 自己复制 candidate，却没有告诉它目标目录初始
为空、无需删除。更简洁的后续做法是由编排器在进入 Agent 前完成纯机械复制，让 Stage07
只编辑既有 `outputs/audited_task/`；这不介入任何科学判断。

## 5. 发布包完整性

四篇发布任务均同时具有 `paper_reproduction` 和 `autonomous_research`。每个模式包含：

```text
<task_type>/<paper_id>/
├── task_info.json
├── package_manifest.json
├── agent_input/
│   ├── task.md
│   ├── submission_schema.json
│   └── data/...
└── evaluation/
    ├── reference_key_points.json
    ├── reference_conclusions.json
    ├── scoring_rules.json
    ├── critical_failures.json
    └── evidence_map.json
```

检查结果：

- 8 个任务包必需文件均存在；
- 所有 JSON 可解析并通过共享 phase Gate；
- 两种模式的 public data 一致；
- evaluator key point、conclusion 和 scoring rule 均非空；
- numeric rule 均具有 target、unit、tolerance 和 binding；
- binding 指向 submission schema 中的可提交结果；
- 论文 PDF/SI 只在 `release/papers/<paper_id>/documents/`，没有进入任何 `agent_input/`；
- paper metadata 只在包根目录和 paper release 层，被评测 Agent workspace 不会物化这些
  字段。

规模如下：

| paper_id | 每模式 public data | reproduction evaluator | autonomous evaluator |
|---|---:|---|---|
| `2aca` | 3 XYZ | 4 key points / 1 conclusion / 5 rules | 4 / 1 / 5 |
| `611` | 2 XYZ | 5 / 1 / 6 | 5 / 1 / 6 |
| `76ae` | 2 XYZ | 5 / 1 / 8 | 5 / 1 / 8 |
| `9455` | 1 coordinates file | 7 / 1 / 8 | 3 / 1 / 4 |

文件完整性已经不是当前主要问题；剩余问题集中在公开语义、科学范围和评分尺度。

## 6. 逐篇任务质量分析

### 6.1 `paper_2aca1dd116799b28`

#### 已解决的问题

Stage06 从原始 SI layout 恢复了三份完整 reactant XYZ，不再因 Markdown 将相邻负数粘连
而误拒绝。任务科学核心清楚：

- 三种 enediyne 的 Bergman cyclization；
- neutral singlet、gas-phase 边界；
- C17–C32 成键，C15/C16 为 diradical centers；
- reproduction 给出 Gaussian 09、B3LYP/6-31G(d,p)、QST3、frequency 和 IRC 路线；
- autonomous 保留目标和输入，但把方法选择交给被评测 Agent；
- evaluator 同时覆盖三个 barrier、stationary-point/reaction-path 验证、ordering 和结论。

Stage07 发现 Stage06 在两个 `task.md` 中直接写出了预期 ordering，并完成两处有限修复。
这说明 Stage07 的新职责确实发挥了作用。

#### 仍存在的问题

最终 reproduction `agent_input/submission_schema.json` 仍包含：

```json
"prefixItems": [
  {"const": "EDY16"},
  {"const": "EDY15"},
  {"const": "EDY17"}
]
```

被评测 Agent 可以不计算 ordering，直接从 schema 读取正确答案。Stage07 虽然修复了
`task.md`，却没有把“所有公开文件”完整审计到底。机械 Gate 不应该也无法可靠判断这类
语义泄露，因此这是 Stage06/07 模型审计遗漏，不是 Gate 缺陷。

结论：科学任务主体质量高，旧根因已解决，但该 reproduction 包在删除 schema 固定排序
前不应直接入正式 benchmark。

### 6.2 `paper_611000e1de080f6f`

#### 旧冲突和本轮处理

旧任务把两个 31 原子 `C15H11NO4` 坐标误写成完整实验 4a；实验命名化合物具有不同的
完整组成，Stage07 因身份冲突拒绝是合理的。

v20 没有继续掩盖该冲突，而是将任务定义为：

```text
coordinate-defined 4a computational model
```

Stage06 review 明确记录：

- public identity 只由 SI 中 `4a-ISO-1-S0-ACN` 和 `4a-ISO-2-S0-ACN` 的坐标块定义；
- 不声称它们是完整实验 tert-butyl/N-methyl compound；
- public 输入为两份 S0 几何；
- hidden evaluator target 为对应 S1 emission energy 和 oscillator strength；
- 目标是 source-defined computational model validation。

这种改写在内部是科学闭合的，而且比旧版错误身份声明明显更好。它不是“放宽身份检查”，
而是诚实缩小了被验证对象。

#### 风险和遗漏

这篇是否适合作为最终 benchmark，取决于 benchmark 是否接受“论文 SI 中唯一坐标定义的
缩减 computational model”作为独立任务对象。需要人工重点确认：

1. 该缩减模型是否足够代表论文核心 photophysical claim；
2. SI 是否充分解释了该 31 原子模型与实验 4a 的关系；
3. 选择 B3LYP 而非正文 general calculation paragraph 中的 M06，是否有充分 source basis。

同时存在两类公开提示：

- reproduction 直接称它们为 “two supplied bright rotamers”；
- reproduction 要求不要替换成 orthogonal dark-state structure。

这些文字向被评测 Agent 提供了 brightness 结论和负向路线线索。Stage07 已从 autonomous
task 删除第二条提示，但 reproduction 中仍有类似信息。虽然 reproduction 可以披露论文
路线，却仍不应直接披露参考结论。

autonomous task 允许使用与论文不同的方法，但 evaluator 对两组 emission energy 和
oscillator strength 分别使用 `0.08 eV` 和 `0.08` 的 tolerance。是否足以容纳真正不同但
合理的模型化学，需要人工校准；否则任务表面自主，评分仍过度绑定论文路线。

#### Stage07 回执错误

Stage07 实际删除了 autonomous task 中的 dark-state 提示，但 `audit_receipt.json` 写成：

```json
{"audit_decision": "approved", "repairs": []}
```

最终任务内容因此变好，但审计记录与文件 diff 不一致。正确记录应为
`approved_with_repairs`，并列出该文件和修复原因。

结论：任务可以作为人工重点复核候选，不应被描述成对旧完整化合物任务的简单恢复。

### 6.3 `paper_76ae2dc25f0a5aeb`

这是本轮最稳定的一篇：

- 两份 126 原子、同组成的 TS starting geometries 完整；
- charge、multiplicity、toluene、temperature 和 signed ΔΔG 定义清楚；
- reproduction 给出两层 B3LYP-D3(BJ) + SMD 路线；
- autonomous 保留同一 TS comparison，但允许自行选择方法；
- evaluator 覆盖 method、TS convergence、单一虚频及 mode assignment、ΔΔG、ordering 和
  product-sense conclusion；
- Stage07 没有实际修改，`approved / repairs=[]` 与文件 diff 一致。

需要人工注意的仅是 autonomous 的 evaluator 仍使用论文路线的虚频参考和
`ΔΔG = 1.9 ± 0.6 kcal/mol`。当 autonomous 允许改变 functional、basis、solvation 和
thermochemistry protocol 时，这个 tolerance 是否与方法自由度匹配，仍属于科学评分设计
问题，而不是 Gate 问题。

结论：科学目标、输入和 evaluator 完整，可作为本轮高质量基准样本；autonomous tolerance
需按正式 benchmark 评分策略复核。

### 6.4 `paper_9455a82229de2427`

任务要求比较 SiN + isoprene 到 P1/P2 + H 的 0 K reaction energy：

- 输入包含 SiN、isoprene、P1 和 P2 坐标及 state/multiplicity 边界；
- reproduction 给出 Gaussian 16 CBS-QB3 route；
- autonomous 自行选择量化方法，并要求明确 0 K energy convention 和 uncertainty；
- 两种模式都正确把 atomic H 纳入 reaction balance；
- public task 提供实验区间 `-162 ± 27 kJ mol-1`，但不提供隐藏计算答案。

Stage07 完成三项真实而有价值的有限修复：

1. 将 conclusion 限制为 “among the supplied candidates”，避免两种候选证明全体系实验
   selectivity 的过度结论；
2. 在 reproduction key points 中补入 P1/P2 reaction energies；
3. 为这两个核心输出补入 numeric scoring rules。

audit receipt 的三项修复与实际 diff 一致。说明 Stage07 对 scientific scope 和 evaluator
覆盖度的审计有效。

剩余问题是 reproduction evaluator 还对四个绝对 CBS-QB3 total energies 使用
`1e-5 Hartree` tolerance。对严格路线复现这不是无效规则，但相较任务核心 reaction
energies，它可能对 Gaussian revision/defaults 过度敏感。人工可考虑降低绝对总能量权重，
把 reaction balance、reaction energy、state correctness 和结论作为核心评分。

结论：最终任务质量较 Stage06 candidate 有明确提升，且修复没有改变科学目标。

### 6.5 `paper_a5564360a31f760b`

Stage06 的拒绝依据来自真实科学不闭合，而非格式问题：

- source 报告了 λ、RMSD 和 Huang–Rhys 数值；
- 但没有唯一的 S1 optimization/state-following protocol；
- 没有唯一 reorganization-energy expression；
- 没有 RMSD atom selection/alignment/symmetry mapping；
- 没有 Hessian、Duschinsky 和 mode-matching 定义；
- environment、conformer 和 search boundary 不清楚。

任意补上一套惯例都会改变被复现量的定义。Stage06 也确认缺陷存在于原始证据，而非某个
派生 parser。根据 v20 边界，继续科学拒绝是正确结果，Stage07 不应从零重建。

## 7. 两种模式质量判断

### 7.1 paper reproduction

优点：

- 四篇都比 autonomous 更完整地披露 paper-supported route；
- 输入、物理边界、结果字段和 evaluator 基本对齐；
- 都要求关键过程验证，而不只要求最终数字；
- `9455` 经 Stage07 后已把核心 reaction-energy 输出纳入评分。

问题：

- `2aca` schema 硬编码正确 ordering；
- `611` 公开称 rotamers 为 bright，并提供 orthogonal dark-state 排除线索；
- 部分规则过度依赖绝对总能量或论文精确数值。

### 7.2 autonomous research

优点：

- 四篇均未披露具体 Gaussian route、functional/basis 的完整论文组合；
- task.md 普遍要求模型自行选择并论证方法；
- public inputs 与 reproduction 保持一致；
- PDF/SI、evaluator 和 reference values 都未进入 Agent workspace。

问题：

- 方法自由度与 evaluator tolerance 未总是同步放宽或重构；
- `611` 的问题命名和 brightness/similarity 叙述仍给出一定先验；
- autonomous 的核心不应只是删除 paper route，还应确保评分允许多个科学合理路线产生的
  可接受差异。

总体上，双模式转换是正确的，不是把 reproduction task.md 简单删几行；但 evaluator
独立性仍弱于 task instruction 独立性。

## 8. Gate 和 Stage07 的边界判断

本轮所有 self-check 和 external Gate 均通过，且没有再次出现“Agent 自查通过、external
Gate 阻断”的旧问题。这证明共享 `phase_gate.py` 的机械语义已经一致。

本轮发现的答案泄露、模型代表性和 tolerance coherence 不应被塞进机械 Gate：

- 用关键词或固定数值扫描无法稳健识别语义泄露；
- 不同论文的合理 tolerance 不同；
- coordinate-defined model 是否代表论文核心属于科学判断。

正确分工仍是：

- Gate：文件、JSON、ID、binding、最小 evaluator 可执行性和 PDF 隔离；
- Stage06：完整合成和模型驱动输入闭合；
- Stage07：跨全部 public surface 的语义泄露、科学一致性和 evaluator coherence 审计；
- 人工：最终确认目标中心性和 tolerance 的具体科学尺度。

## 9. 方案一致性复核

| v20 验收项 | 代码实现 | 真实回归结论 |
|---|---|---|
| 无论文/化学特例 | 通过 | 未发现测试 paper ID、化合物或数值进入生产代码 |
| 科学输入由 Stage06 判断 | 通过 | 五篇均由 Agent 按目标生成 input closure |
| 区分解析损坏与原始缺失 | 通过 | `2aca` 恢复，`a556` 真实拒绝 |
| 允许无损恢复、禁止猜测 | 通过 | 两种行为均出现且归因合理 |
| 格式可解析不等于科学身份 | 通过 | `611` 没再错误声称完整实验化合物 |
| Stage07 独立审计、不重建 | 通过 | 四篇候选均只做零或有限修复；拒绝样本未重建 |
| Gate 最小机械职责 | 通过 | 0 mechanical block，未增加化学规则 |
| evaluator 完整可执行 | 文件合同通过 | 内容完整，但部分 autonomous tolerance 需人工校准 |
| canonical metadata 进入 release | 通过 | 四篇 title/date/year/authors 非空 |
| authors 来自 header metadata | 基本通过 | 无 bibliography 污染；个别字符归一化仍有瑕疵 |
| metadata 不进入 Agent workspace | 通过 | release 注入，agent_input 无 paper metadata/PDF |
| self/external Gate 语义一致 | 通过 | 已构建任务全部同时 passed |
| 单元和真实回归有报告 | 通过 | 22 + 409 tests，本文记录五篇回归 |
| 完成后回看方案 | 通过 | 本表完成逐项核对 |

需要强调：方案的代码边界已实现；真实 Agent 行为仍暴露了语义审计不完全。这不是恢复旧
兼容代码或增加 Gate 规则的理由，而是下一轮 Prompt 与审计记录接口应更精确。

## 10. 后续最小优化建议

### 10.1 优先级一：完整 public-surface 泄露审计

不增加关键词黑名单或论文特例。调整 Stage06/07 Prompt，要求对两种模式分别建立公开面
清单并逐项审计：

```text
task.md
submission_schema.json
task_info.json 中被评测侧可见的部分
public data filenames
public data comments/content
```

对 reproduction 也明确要求：可以披露 source-supported route，但不得把 numeric answer、
ordering、reference conclusion 写进 task 或 schema。Stage07 在写 receipt 前，将 hidden
reference/conclusion 与全部 public files 做一次语义对照。

### 10.2 优先级二：autonomous contract 与 evaluator 同步审计

在 Prompt 中增加一条通用要求，不写任何固定 tolerance：

> 当 autonomous 允许改变方法、模型或分析路线时，检查其 numeric tolerance、condition
> 和 conclusion rule 是否仍与该自由度科学相容；不能沿用 reproduction evaluator 而不做
> 重新判断。

同时要求 key points 聚焦任务真正需要评估的计算节点和结论，不因 source 中存在 total
energy 就默认所有绝对能量都应成为高权重评分项。

### 10.3 优先级三：让修复记录可验证

Stage07 Agent 继续负责写修复原因，但由代码对 candidate 和 audited task 计算相对路径级
`changed_files`。若 `repairs[].file` 与实际 diff 不一致，应在发布前报告 provenance
不一致；这只是文件事实检查，不判断修复是否科学合理。

### 10.4 优先级四：消除无意义工具失败

- 编排器预先把 candidate 复制为 `outputs/audited_task/`；
- Prompt 明确不要删除该目录；
- 告知 Agent 优先使用现成 `document_query.py`，无需安装 PDF 包；
- 为 query CLI 增加通用 page range 读取，仍不加入化学语义。

### 10.5 优先级五：通用 metadata 文本归一化

在 canonical metadata 层统一进行：

- HTML entity unescape；
- Unicode NFC normalization；
- 合并组合附加符号前的异常空格；
- 只清理明确的排版字符问题，不猜测作者姓名拼写。

该处理可修复 title 中的 `&#x...;` 和部分分离重音符号，同时保持无 paper 特例原则。

## 11. 最终判断

v20 已达到本轮最重要的目标：

- `2aca` 不再因派生文件损坏被误拒绝；
- `a556` 仍因真实科学不闭合被拒绝；
- self-check 和 external Gate 不再语义分叉；
- Stage07 能实际修复答案泄露、结论范围和 evaluator 漏项；
- release 结构、论文隔离和 metadata 链路正常；
- 没有通过论文特例、化学硬编码或放宽 Gate 获得通过率。

任务质量总体高于 v19.1，但当前正式入库建议为：

- `paper_76ae...`：可进入常规人工复核；
- `paper_9455...`：可进入常规人工复核，关注绝对能量 tolerance；
- `paper_2aca...`：先删除 reproduction schema 的固定 ordering，再复核；
- `paper_611...`：作为 coordinate-defined model 候选进行重点科学复核，并修正公开 brightness
  提示和审计回执；
- `paper_a556...`：维持科学拒绝。

下一步应优先修复跨全部 public surface 的语义审计和 evaluator 自主性一致性，而不是扩大
机械 Gate。

# Stage06/07 v23 五篇回归与评估任务质量分析

## 1. 结论摘要

本轮运行目录：

`runs/stage0607-v23-gpt-5.6-sol-20260827-five`

五篇论文在代码状态上均为 `published`，但逐文件审查后，不能将这个结果解释为“五篇任务均可直接进入 benchmark”。更准确的结论是：

- 终态控制和 token 效率改进有效；
- 双模式的总体定义已基本落地；
- 文件数量和发布目录结构完整；
- Gate 仍只能证明机械合同通过，不能证明 public input、evaluator binding 和 Stage07 科学审计结论正确；
- 严格按“无需人工修正即可执行和评分”的标准，本轮为 `0/5`；
- `paper_2aca...`、`paper_611...`、`paper_945...` 的科学目标可保留，但需要有界修复；
- `paper_76ae...`、`paper_a556...` 的核心分子输入没有在离线 Agent 输入中唯一闭合，应补齐明确结构输入，否则应拒绝发布。

因此，本轮的 `5/5 published` 是机械发布率，不是最终科学可用率。

## 2. 运行结果与效率

### 2.1 发布状态

| paper_id | 代码结果 | 人工逐文件复核结论 |
|---|---:|---|
| `paper_2aca1dd116799b28` | published | 目标可用；autonomous 路线残留且 evaluator 语义绑定错位 |
| `paper_611000e1de080f6f` | published | 公开 XYZ 无效；多个 evaluator binding/schema 不可执行 |
| `paper_76ae2dc25f0a5aeb` | published | 催化剂和底物身份未唯一闭合；已知 1.9 kcal/mol 核心数值未进入 numeric rule |
| `paper_9455a82229de2427` | published | 任务主体较好；numeric target 不是数值，评分规则需修复 |
| `paper_a5564360a31f760b` | published | 依赖 CCDC/论文专用名称恢复分子结构，离线任务不自包含 |

### 2.2 调用与 token

| paper_id | Stage06 requests | Stage06 total tokens | Stage07 requests | Stage07 total tokens |
|---|---:|---:|---:|---:|
| `paper_2aca...` | 25 | 1,709,450 | 14 | 313,707 |
| `paper_611...` | 36 | 2,411,987 | 27 | 1,049,672 |
| `paper_76ae...` | 32 | 1,559,067 | 17 | 483,636 |
| `paper_945...` | 33 | 1,810,464 | 19 | 647,750 |
| `paper_a556...` | 21 | 861,422 | 15 | 339,246 |
| 合计 | 147 | 8,352,390 | 92 | 2,834,011 |

Stage06 总 token 约 8.35M，相比 v22 约 27.97M 下降约 70%，并接近 v20 的约 8.62M。`paper_76ae...` 不再因反复 `find/Gate/report read` 在 autonomous 生成前耗尽调用预算，说明四里程碑、非进展约束、完整树终态和 reserve 缩减是有效的。

但低 token 不等于低错误率。Stage06 仍出现多次 JSON、patch 和 Gate 修复失败；`paper_611...` 的 Stage07 又因重复应用局部补丁引入了新的公开文件错误。

## 3. 最终发布文件完整性

每篇论文、每种模式都存在：

- `agent_input/task.md`
- `agent_input/submission_schema.json`
- `agent_input/data/inputs/...`
- `task_info.json`
- `package_manifest.json`
- `evaluation/reference_key_points.json`
- `evaluation/reference_conclusions.json`
- `evaluation/scoring_rules.json`
- `evaluation/evidence_map.json`
- `evaluation/critical_failures.json`

论文正文和 SI 只位于 `release/papers/<paper_id>/documents/`，没有复制到两种模式的 `agent_input`。发布目录结构符合 v19/v23 文件管理设计。

文件“存在”不代表内容可用。当前最明显的反例是 `paper_611...`：四个 XYZ 文件都存在且被 manifest 收录，但不是合法 XYZ。

## 4. 逐篇质量审查

### 4.1 `paper_2aca1dd116799b28`

#### 科学任务

论文复现模式总体合理：公开三个反应物起始几何，给出作者关于电荷转移、平面性和位阻的定性路线，不公开模型化学、能垒、排序和 tolerance，并要求 Agent 独立寻找和验证 Bergman 环化 TS。

自主科研模式的 objective 已删除显式作者路线，但第三部分仍要求：

- arm planarity/dihedrals；
- donor-to-acceptor delocalization；
- support or challenge the proposed explanation。

这些不是纯粹的结果验证要求，而是与论文作者解释高度重合的判别路线。Stage07 的 receipt 声称已移除 autonomous 的作者路线，但实际只修复了局部措辞，未检查完整 `task.md`，所以修复不完整。

#### Evaluator

参考关键点和结论包含实际能垒、排序、TS/path 验证和机理结论，科学内容本身充分；问题在 scoring rule 的对应关系：

- `r2` 引用 `kp2`，但 `kp2` 是 TS 验证；`r2` 实际评估能垒排序；
- `r2` 的 binding 却指向 `$.validation`，不包含能垒排序；
- `r3` 引用 `kp3`，但 `kp3` 是数值/排序；`r3` 实际评估 TS/path 验证；
- `r3` 的 binding 却指向 activation energy 数值，不包含 TS/path 证据；
- `r1` 的 `target` 是 JSONPath 字符串，实际参考值放在 `expected` 字典中，不符合 v23 所定义的 numeric target；
- reproduction 和 autonomous evaluator 完全复制，autonomous 没有覆盖独立假设比较。

Gate 只确认 reference_id 存在、selector 可定位和字段非空，没有检查“reference claim、expected 和 binding 是否表达同一件科学事情”，因此错误通过。

#### 结论

科学目标和公开结构可保留；修复 autonomous 路线残留，并重写少量 scoring rules 后可用。当前版本不能直接发布。

### 4.2 `paper_611000e1de080f6f`

#### 公开输入格式错误

Stage06 生成的 XYZ 缺少原子数首行。Stage07 识别了问题，但多次执行了低上下文的“把空行替换为 30”补丁。最终四个公开文件都以三行连续的 `30` 开头：

```text
30
30
30
4a ISO-1 S0 starting geometry ...
O ...
```

文件共有 35 行，而一个 30 原子 XYZ 应为 32 行。任何标准 XYZ parser 都会把第二行当 comment、第三行当第一条坐标并失败。Stage07 receipt 中“making each public Cartesian file valid XYZ”的陈述与实际产物相反。

#### 模式区分

reproduction 保留 TICT 作者假设但隐藏数值和最终暗态结构，方向基本正确。autonomous 已删除 TICT 名称和“dark candidate”答案措辞，但仍把 coumarin-pyrrole torsion 和 0–180° 扫描直接定义为核心搜索坐标。由于作者路线本身正是该扭转坐标，这仍然会明显缩小 autonomous 的假设空间，至少属于边界偏紧，应重新判断该坐标是问题定义还是作者路线。

#### Evaluator/schema

- reproduction 的四个 numeric binding 字段位于 schema 顶层，但这些字段不是 `required`；合法提交可以完全不含被评分数值；
- reproduction 的 `rotamers` 是 required，但 numeric rules 不绑定其中的记录；
- condition/ordering rules 多数只绑定 `$.conclusion`，没有绑定 landscape/search/rotamer evidence；
- autonomous 的 numeric rule `ar_r2` 绑定 `$.mechanism`，但 autonomous schema 根本没有声明 `mechanism`；
- 因顶层 JSON Schema 默认允许 additional properties，Gate 把未声明字段误认为可接受；
- `ar_r2` 的 binding 指向对象而不是明确 numeric leaf，仍通过了 numeric leaf Gate；
- 多值 numeric target 使用字典而不是一个明确标量，后续评分语义不统一。

#### 结论

科学目标和源坐标可保留，但必须重新生成合法 XYZ，并系统对齐 schema 与 evaluator。当前版本不可执行、不可直接评分。

### 4.3 `paper_76ae2dc25f0a5aeb`

#### 输入闭合失败

任务只公开文本 `molecular_specification.txt`。其中 `(S)-A2` 是论文内部催化剂编号，不是可唯一恢复结构的公共分子定义；没有 SMILES、SDF/MOL/CIF、明确取代基清单或原子映射。底物描述也同时出现 `N-benzyloxetan-3-amine` 和“benzyl substituent at C3”等容易产生不同连接方式的表达。

被评估 Agent 不接触论文/SI，且任务应按离线 `agent_input` 自包含。仅凭 `(S)-A2`、SPINOL-derived 和绝对构型不能构建唯一的完整大分子催化剂。Stage06 workflow review 一方面声称“unambiguous identities/connectivity”，另一方面又要求 Agent 检查 exact catalyst depiction，内部已经存在矛盾。Stage07 只把 BINOL 更正为 SPINOL，没有解决分子图缺失。

#### Evaluator

源 SI 明确给出：

- TS2-R-S：0.0 kcal/mol；
- TS2-S-R：1.9 kcal/mol。

任务本身也要求 `relative_free_energy_kcal_mol`，但 evaluator 只保留 `R-S lower than S-R` 的 ordering/condition，没有生成 1.9 kcal/mol numeric rule 和初始 tolerance。这并不是“文本任务无需 numeric rule”的合理应用，而是遗漏了该任务真实存在且属于核心结论的数值参考。

#### 结论

当前任务不应发布。需要从源证据生成不泄露结果、但唯一确定分子身份的公共结构输入；若做不到，应科学拒绝。结构闭合后还需补上数值参考规则。

### 4.4 `paper_9455a82229de2427`

#### 科学任务

这是本轮主体质量最好的一篇：

- reproduction 给出作者提出的 N 端加成、环化/异构化、H 脱除定性路线；
- 不公开最终产品结构、P1/P2 标签、参考能量、排序和 tolerance；
- autonomous 只给反应物、计量、气相边界和实验放热区间，并要求自主提出有限结构/路径搜索；
- 两种模式都区分热力学相容性与动力学/分支证明。

#### Evaluator

参考关键点已给出约 -156 和 -150 kJ/mol，但 numeric rule 的 `target` 是：

```text
"reaction_energies_kj_mol values for leading two cyclic products"
```

这是描述字符串，不是数值目标。Gate 的 `_has_value()` 只判断 target 非空，所以把它当成有效 numeric target。`product_1`、`product_2` 也没有与两个具体结构身份建立稳定映射，且不是 schema 中的 required 子字段。

#### 结论

任务主体可以保留。将两个数值拆成明确的 scalar numeric rules，并通过产品/候选 ID 建立结构身份与能量的对应关系后可用。

### 4.5 `paper_a5564360a31f760b`

#### 输入闭合失败

公开输入只描述：

- p-2BN 是 pyrazine-derived、para-oriented；
- m-2BN 是 pyrimidine-derived、meta-oriented；
- octyl 替换为 methyl；
- 可选使用 CCDC 1941938/2480480。

这不足以唯一确定完整分子图、取代位置和原子映射。CCDC 是外部数据库标识；任务包没有 CIF/SDF/SMILES，运行环境又不能假定有网络或 CCDC 访问权限。论文内部名称 `p-2BN/m-2BN` 也不能替代自包含结构。

Stage06 workflow review 明确承认“article does not publish Cartesian coordinates for methylated variants”，却仍将 input closure 标为 passed。Stage07 进一步把“可以使用 CCDC”误判为输入已闭合。这个判断不符合 benchmark 的离线自包含边界。

#### 任务与 evaluator

任务目标、reproduction 的 ICT/rigidity 定性路线以及隐藏 numeric evaluator 本身较完整；numeric target、单位和 tolerance 也比其他几篇规范。但 autonomous 指令给出的“electronic-state relaxation versus conformational/vibrational flexibility”示例会轻度提示作者 rigidity 路线，建议删除示例，只要求提出至少两个可区分假设。

#### 结论

在没有完整公共分子图之前不应发布。最简单的正确做法是提供源证据支持、仅定义起始体系而不携带 S0/S1 结果的结构文件；若无法唯一构造，则科学拒绝。

## 5. 为什么 self-check、external Gate 和 Stage07 都没有阻断

### 5.1 self-check 与 external Gate 已统一，但统一的是同一套有限机械语义

五篇的 reproduction self-check、full-pair self-check、Stage06 external Gate 和 Stage07 audit Gate 均 passed。这个结果说明两套 Gate 已对齐，不再出现“Agent Gate passed、外部同合同 Gate failed”的旧问题。

但它们共同漏掉了：

- 标准 XYZ 的 header/comment/atom-count 语法；
- 论文专用名称或外部数据库标识是否足以离线唯一构造分子；
- numeric target 是否真的是 JSON number；
- binding 是否绑定到 schema 明确声明的字段，而不是由 `additionalProperties=true` 放行；
- scoring rule 的 reference claim、expected 和 binding 是否语义一致；
- Stage07 声称完成的 repair 是否真的产生了预期文件内容。

统一 Gate 是必要条件，但不是充分条件。

### 5.2 当前 Gate 的具体代码缺口

`src/stages/phase_gate.py` 对 numeric target 只调用 `_has_value()`，因此字符串和字典都可通过。对 schema selector，遇到默认开放的 `additionalProperties=true` 时返回“无法静态确定但允许”，导致完全未声明的 `$.mechanism` 也可通过。

numeric leaf 检查只会阻断“明确声明为 object/array”的 binding；当 selector 落到开放 schema 时会返回未知并放行。因此 v23 的实现只解决了显式 object/array 绑定，没有实现“numeric rule 一定绑定到真实 numeric leaf”的完整设计目标。

Gate 对 reference_id 的检查是集合覆盖，不理解 `kp2` 的科学含义，所以无法发现 `paper_2aca...` 中排序和 TS 验证被交叉绑定。

### 5.3 Stage07 的执行问题

Stage07 Prompt 已要求 answer inversion、input sufficiency 和 evaluator alignment，但实际执行出现三类问题：

1. 只修复命中的局部句子，没有重新阅读整个 autonomous public surface；
2. 以“有化学名称/外部 ID”为充分输入，没有从 evaluated Agent 的离线视角测试唯一可构建性；
3. patch 部分成功后继续用低上下文补丁重试，没有验证最终文件，`paper_611...` 因而由缺 header 变成三重 header。

Stage07 receipt 和 Gate passed 被当成完成证据，但 receipt 中的自然语言断言没有得到独立验证。

## 6. 与 v22 的差异

### 6.1 明确改善

- Stage06 token 从约 27.97M 降到约 8.35M；
- 五篇都生成完整双模式目录，不再出现 receipt 提前结束造成 autonomous 缺失；
- reproduction/ autonomous 的总定义比早期版本清楚；
- Stage07 确实发现并修复了一部分答案泄露，如 `paper_a556...` 的结果方向、`paper_611...` 的 bright/dark 结果措辞；
- metadata 最终从 release metadata 正常注入，不再为空。

### 6.2 没有证明改善的部分

- v22 发布 3/5，v23 发布 5/5；新增的两篇 `76ae/a556` 恰好都存在输入不闭合，所以发布率上升不能解释为科学质量上升；
- v23 的部分任务比 v22 更短、更封闭，但也删掉了方法敏感性、open-shell 诊断或明确的多假设比较；
- Stage07 修复数量增加，但出现了修复引入新错误；
- evaluator 的“文件完整”提高了，rule 的科学可执行性仍不稳定。

综合判断：v23 明确提升了流程效率和终态可靠性，但科学任务/evaluator 的最终可用性没有同步达到发布标准。

## 7. 下一版建议

### 7.1 Stage06 Prompt：增加一个简短的最终语义对齐动作

不增加新文件、不增加第二个 Agent、不让代码生成 evaluator 骨架。要求 Stage06 在 final Gate 前逐条核对：

```text
reference_id 的科学主张
→ rule 的 type 与 target/expected
→ binding 指向的提交字段
```

三者必须是同一个科学判断。多篇论文有多个数值时，一条 numeric rule 只对应一个标量 target；不要用路径字符串、描述文本或数值字典代替 target。

同时明确：若任务核心要求一个论文已给出、证据可信的数值，不能以“semantic-only 允许”为理由省略该 numeric reference；semantic-only 只适用于核心答案本来就是非数值的任务。

### 7.2 Stage07 Prompt：从离线 Agent 视角检查 input closure

加入一个明确但不化学硬编码的问题：

> 只给 evaluated Agent 最终 `agent_input/`，不允许读取论文/SI、互联网或外部数据库，它能否唯一构造所有任务定义所必需的体系？若只能依赖论文编号、作者内部化合物标签、CCDC/数据库 ID 或猜测取代基，则 input closure 失败。

这仍由 Stage07 Agent 做科学判断，不由代码统一预处理分子输入。

### 7.3 Stage07 修复后必须验证最终内容

对每个修改文件：

- 读取或解析修改后的最终版本；
- 对标准格式使用相应 parser/最小语法检查；
- 不根据 patch 的部分成功输出推断修复完成；
- 若同一补丁失败，先查看当前文件，再构造带充分上下文的新补丁，禁止重复无上下文 hunk。

### 7.4 Gate 只增加三条通用机械约束

避免加入论文关键词或科学硬规则，只补足当前合同本身：

1. numeric `target` 必须是 JSON number；多值结果拆成多条 scalar rule；
2. binding 的顶层字段必须在 `result_schema.properties` 中显式声明，不能仅靠默认 `additionalProperties=true` 放行；numeric binding 必须解析到明确 number/integer leaf；
3. 对 `.xyz` 执行标准 atom-count/header/coordinate-line 语法检查。

不让 Gate 判断 tolerance 科学最优、不判断分子是否科学正确、不做论文类型关键词匹配。

### 7.5 当前五篇的处置

- `2aca`：修复 autonomous 路线和 evaluator 映射后重新审计；
- `611`：从源坐标重新生成四个合法 XYZ，重写 schema/binding 后重新审计；
- `76ae`：补充唯一分子结构，补 1.9 kcal/mol numeric rule；否则拒绝；
- `945`：拆分两个 numeric scalar rules，并绑定结构身份；
- `a556`：补充自包含结构文件；做不到则拒绝。

在上述修复前，不建议把本轮 `release/tasks` 直接同步到正式 benchmark `tasks/`。

## 8. 复核位置

供其他 Agent 独立检查的最终结果根目录：

`/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline/runs/stage0607-v23-gpt-5.6-sol-20260827-five/release`

重点目录：

- public tasks：`release/tasks/{autonomous_research,paper_reproduction}/<paper_id>/agent_input/`
- hidden evaluator：`release/tasks/{autonomous_research,paper_reproduction}/<paper_id>/evaluation/`
- Stage07 轨迹：`papers/<paper_id>/stage_07_task_audit/workspaces/<paper_id>/attempt-*/_agent_stdout.jsonl`
- Stage07 receipt：同一 attempt 下的 `outputs/audit_receipt.json`
- Stage06 轨迹：`papers/<paper_id>/stage_06_task_construction/workspaces/<paper_id>/final_task_synthesis/attempt-*/_agent_stdout.jsonl`


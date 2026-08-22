# Stage06/07 v5 Round 20 最终结果与迭代总结

日期：2026-08-22
最终代码基线：`586d4c5 fix(stage06-07): close asset and ranking audit gaps`
Round 20 计划提交：`1e786e0 docs(stage06-07): plan final round twenty regression`
总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 最终判断

Round 20 的 10 篇任务全部正常结束，没有 harness/API/进程失败，也没有机械误阻断：

- 10/10 运行完成，`failed_count=0`；
- 6/10 科学拒绝，逐篇复核均有源材料不闭合依据；
- 4/10 经 Stage07 修复后发布；
- 0/10 `mechanical_publish_blocked`；
- 0/10 `mechanical_approved_but_unpublished`；
- 代码回归在 Round 19 已达到 559 tests passed，Round 20 收尾再次执行全量回归。

本轮证明代码运输层已经基本稳定：mode scope、路径、manifest、发布状态、evaluator 投影和机械诊断没有再造成错误拒绝或静默黑洞。没有发现需要继续修改的确定性代码 bug。

但是，4 个发布任务中只有科学范围选择本身总体合理；其中仍有 3 类发布前科学审计瑕疵：

1. 一个任务的输入定义存在明显电荷/多重度和分子组成冲突，Stage07 错误批准；
2. 两个任务在方法自由的 autonomous 模式中仍绑定论文方法下的绝对数值或具体波长；
3. 一个任务没有确定公开电荷/多重度，并错误地把频率分析当作电子态验证手段。

这些问题都属于 Stage07 未执行或未完全执行现有 Prompt 中已经写明的科学检查，而不是机械 gate 应补的代码规则。继续把化学判断写成代码死规则会降低通用性；继续往已经很长的 Prompt 追加零散句子也很可能增加认知负担。因此 Round 20 按预算结束，不再追加论文、分子、格式或固定数值特例。

## 2. 测试配置与结果目录

- 结果目录：`runs/stage06-07-v5-round20-final-deepseek10-concurrency10-20260822`
- 来源：`runs/stage00-05-qualityfix-published-since-20260101-20260814T201641`
- 模型：DeepSeek-v4-pro-0813
- Harness：Codex
- 推理强度：high
- 并发：10
- 随机种子：`20260861`
- 总状态：`COMPLETED`
- 完成数：10
- 失败数：0

运行从 2026-08-22 08:08:14Z 开始，最后一篇于 08:58:33Z 完成。单篇耗时约 15–50 分钟，长任务没有超时或丢失终态。

## 3. 十篇逐篇审查

| paper | 管线结果 | 独立审查 | 范围代表性 | 主要判断 |
|---|---|---|---|---|
| `paper_22572412ba3a8028` | 科学拒绝 | 正确 | 不可构建 | W/NiFe-LDH 周期模型缺晶格、原子位置、W/氧空位位置、固定层和吸附位点。VASP/VASPKIT 已安装，未因软件拒绝。 |
| `paper_f39d98d29b4bf709` | 科学拒绝 | 正确 | 不可构建 | Co3Cu(111)/CuCo2S4(004) 缺原子坐标、终止面、反应位点、TS 映射和磁性态。VASP 已安装，拒绝依据是科学输入不足。 |
| `paper_23922de7d9683340` | 科学拒绝 | 正确 | 不可构建 | MgO hydration 的 PS-MD/DFTB/DFT/NEB 主线缺轨迹快照、ReaxFF 参数和 NEB 端点；唯一闭合内容是外围方法验证，Stage06/07 没有用外围任务替代核心问题。 |
| `paper_78014d64fd768de0` | 科学拒绝 | 正确 | 不可构建 | Cu-doped Bi2O2Se 缺周期坐标和 dopant supercell 定义。VASP/VASPKIT 可用，拒绝与软件无关。 |
| `paper_f57b0e05340978fd` | 科学拒绝 | 正确 | 不可构建 | [7]-OTf 的 CIF 只在文献中被引用而未进入源快照；PM6 扫描依赖精确的 D(3,44,45,7) 原子编号，不能用猜测结构支撑 46.5 kcal/mol 紧目标。 |
| `paper_0e4d3d3cea9cb896` | Stage06 构建，Stage07 拒绝 | 正确终态 | Stage06 误构建 | Stage06 仅用 C98 graphene seed 猜测 CuNxN'yO 活性位；Stage07 正确指出论文结果依赖多个 metastable configurations 中选出的具体位点，而公共输入没有坐标或确定性搜索协议。VASPsol 缺口被登记但不是拒绝理由。 |
| `paper_2f2aa11ea61a32bb` | 发布 | 基本可用，需修 hidden autonomous 口径 | A：完整计算主线 | 12 个 SI 坐标全部闭合，覆盖论文全部 DFT/TD-DFT 计算路线；近简并量使用分组/趋势。缺陷是 autonomous hidden proposition 仍要求论文方法下的 341/351 nm，并继续使用 reproduction 的 A 编号。 |
| `paper_13639735b154735a` | 发布 | 基本可用，需修 mode-specific acceptance | A：完整计算主线 | 11 个 XYZ 均为合法单帧；三个 adsorption 模型、两组同组成 minimum/TS 和完整机理计算主线闭合。缺陷是 autonomous 允许自选方法，却仍按论文 B3LYP 路线的 12.0、1.37、角度和距离严格数值评分。 |
| `paper_4b27492a0c5bab9c` | 发布 | 科学范围合理，电子态合同不闭合 | B：最高中心性闭合子流程 | 完整成对电解机理缺 CBr4/下游参考态，选择 1a/1ab/1ac 的直接阳极 N2 脱除势垒合理；六个 XYZ 三对组成匹配。任务未明确各物种 charge/multiplicity，并错误地声称频率可验证电子态。 |
| `paper_47b659434cda4eab` | 发布 | 错误发布 | 任务本身不可用 | 输入 JSON 同时写 `charge=1`、`multiplicity=1`、`electronic_state=doublet`；doublet 应对应 multiplicity 2。`alpha_C10` 的 SMILES 实际碳数与对应 beta 路径不一致，多个 alpha 标签存在同类 off-by-one，不能支持同组成路径比较。Stage07 明称已核对电子态和元素守恒却漏掉冲突。 |

### 3.1 `paper_136...` 的 evaluator diagnostics 不是漏阻断

机械报告包含多条 `evaluator_binding_fields_missing`，原因是公共 `submission_contract.json` 使用开放 schema：

```json
{
  "results_schema": {
    "type": "object",
    "additionalProperties": true
  }
}
```

因此 gate 无法从公开 schema 静态证明 hidden JSONPath 存在，只能给 diagnostic。实际 `task.md` 已完整声明 `co2_oc_o_angles`、`co2_adsorption_distances`、两个 barrier object 和 validation 字段；`ground_truth_common.json` 的 mode bindings 与这些字段一致。该诊断不应升级成机械阻断，否则会重新制造 open-schema 误报。

### 3.2 `paper_2f2...` 的科学范围是合格的

论文的 headline 是晶体多晶型和白光发射，但这些主要由实验光谱、SCXRD/PXRD 支撑。数据管线的目标是覆盖论文的完整**计算化学过程**，不是把非计算实验强行变成计算任务。该任务覆盖全部 12 个 DFT/TD-DFT 体系、优化、频率、S1–S3、轨道/振子强度、planarity 和 halogen-position 比较，属于 A 级完整计算主线。

问题只在 autonomous hidden projection：方法自由时不应把 341/351 nm 当作必须命中的具体论文数值；A01/A02 等私有/reproduction ID 也应在 autonomous evaluator 投影为 `candidate_1/candidate_2` 或使用不依赖文件名的中性描述。

### 3.3 `paper_4b...` 的子流程选择是合格的

完整论文机理包含 diazo 阳极氧化、CBr4 阴极还原、Br− coupling 和 HAT。源材料没有足够的独立下游参考态，也没有完整的 1aa/1ad minimum/TS 对。Stage06 选择有完整 1a/1ab/1ac 坐标和自由能数据的 N2 extrusion branch，直接支撑“首次直接阳极氧化”和底物反应性趋势，属于 B 级最高中心性闭合子过程，并非随意外围计算。

任务的缺陷不是范围，而是电子态合同：

- 公开任务只说 reactant 是 neutral diazo、TS 与 reactant 同 charge；
- 没有明确 singlet/doublet 等 multiplicity；
- “用 harmonic frequency 验证 charge/multiplicity”在科学上不成立，频率只能支持 stationary-point character；
- 电子态应由源计算、电子数奇偶性、预期态和必要的自旋诊断共同确定。

## 4. 代码问题、Prompt 设计与模型能力的归因

### 4.1 确定性代码问题：本轮未发现新问题

Round 19 修复的 `TaskInfo.data[*].name` 运输问题在本轮没有复现。Round 20 还验证了：

- `applies_to_modes` 正确过滤；reproduction-only profiles 在 autonomous 中只产生 `not_applicable` diagnostic，不会误阻断；
- mode-specific Ground Truth 可以只投影到适用模式；
- bracket-quoted JSONPath 能通过运输检查；
- 开放 schema 只产生观察性 diagnostic；
- mode pair 的资产/shape 差异只作观察，不做科学裁决；
- Stage07 科学批准后发布状态可见；本轮无 approved-but-unpublished 黑洞；
- 所有发布任务都生成 evaluator registry 和 published manifest；
- 科学拒绝不会被机械 gate 伪装成代码失败。

不能因为 `paper_47b...` 的 charge/multiplicity 错误给 gate 增加“doublet 必须 multiplicity=2”之类的化学规则。类似电子态表达可能来自不同 schema、自由文本或软件 convention，代码无法通用地判定完整科学语义；这仍是 Stage07 的职责。

### 4.2 Prompt/角色设计问题

Stage07 的职责仍然偏宽。一个 turn 内同时要求它完成：

- 论文中心性和范围审计；
- 输入/参考态/电子态/计量审计；
- 成本和软件审计；
- autonomous 脱敏；
- Ground Truth/profile/binding 修复；
- task metadata、route map 和发布合同修复。

当前 Prompt 已明确写出：

- method-discovery autonomous 不得只按隐藏论文方法的紧绝对值评分；
- 近简并量应使用 tie group、partial order 或 mode-specific acceptance；
- 每个 scored difference 必须核对组成、charge、sign 和 binding；
- 输入与物理边界必须独立审查。

所以本轮缺陷不能归因于“Prompt 完全没说”。更准确的归因是：Prompt 过长、职责跨度过大，导致模型完成了大量修复后，在最终局部一致性检查中漏项。下一次若继续优化，方向应是压缩和结构化现有要求，而不是继续追加长篇原则：

1. Stage07 先输出 immutable scientific audit matrix，再进入 repair；
2. audit matrix 为每个输入显式列 `formula / charge / multiplicity / electronic_state / provenance / consistency`；
3. 为每个 acceptance profile 显式列两个 mode 的 `method freedom / target type / binding / alias / applicable`；
4. 未填完矩阵不能声明 row closed；
5. 删除重复段落和重复 disclosure 原则，减少上下文噪声。

这仍是 Agent 自审，不是代码代做科学裁决。

### 4.3 模型能力/单次执行问题

以下问题已有明确 Prompt，却仍被 DeepSeek 漏掉，应归为模型执行失败：

- `paper_47b...` 中 JSON 内的 multiplicity=1 与 doublet 明文冲突；
- `paper_47b...` 中要求 composition-balanced path，却没有核对 SMILES 碳数；
- `paper_2f2...` 的 autonomous hidden proposition 保留具体 341/351 nm；
- `paper_136...` 在 method discovery 下仍共享论文方法的严格绝对数值；
- `paper_4b...` 把频率分析错误用于“验证”电子态。

同一模型也展示了有效能力：它正确拒绝 5 个资产不闭合任务，Stage07 又独立推翻 Stage06 对 `paper_0e4...` 的错误构建，并正确识别两篇完整计算主线和一篇中心性足够的子流程。因此不能简单判断模型“不具备科学审计能力”；更准确的结论是它在长、多职责 Stage07 turn 中局部一致性可靠性不足。

## 5. 角色是否发挥预期作用

### Stage06A

总体发挥作用：

- 5 篇在构建阶段正确拒绝；
- 没有因软件未安装缩小或拒绝科学目标；
- 对 MgO hydration 没有用外围验证任务凑通过；
- 对两篇论文选择完整计算主线；
- 对 `paper_4b...` 给出了从完整路线降级到核心子过程的证据。

不足：

- `paper_0e4...` 仍用通用 graphene seed 猜具体活性位；
- `paper_47b...` 构造了内部矛盾的模型定义；
- 对 `paper_4b...` 没有闭合电子态。

### Stage06B

总体发挥作用：

- 保持答案盲，仅处理 autonomous 公共表面；
- 中性化文件名、XYZ comments 和路线文件；
- 没有重新选择 workflow 或修改科学 truth；
- 没有暴露 source route 到 method-discovery autonomous task。

本轮没有证据支持扩大 Stage06B 权限。科学输入和 hidden acceptance 的问题应由 Stage06A/Stage07 处理。

### Stage07

有明显正向价值：

- 独立推翻 `paper_0e4...` 的错误 Stage06 批准；
- 对三个可发布任务修复 route evidence 泄漏、路径、mode metadata、JSONPath 和 private mapping；
- 没有把软件缺口当成拒绝条件；
- 能审查完整路线与核心子流程的代表性。

但没有完全达到理想目标：

- 错误发布 `paper_47b...`；
- 对三个发布任务的电子态或 autonomous acceptance 留下瑕疵；
- 审计 receipt 中“closed/passed”的自报与实际局部内容不完全相符。

因此 Stage07 是当前主要剩余瓶颈，但瓶颈是科学审计执行可靠性，不是代码 gate。

### Orchestrator / mechanical gate

本轮发挥符合边界：

- 只做运输、schema、路径、mode scope、manifest 和发布可观察性；
- 没有用弱机械启发式否决科学任务；
- diagnostics 与 findings 分离；
- 0 个机械误阻断。

## 6. Stage07B 是否启用

结论：不启用。

总目标要求在 10 篇中至少 2 篇出现同类“Stage07 已科学批准、只差简单合同修复而机械阻断”的情况，才考虑 Stage07B。本轮：

- `mechanical_publish_blocked=0`；
- `mechanical_approved_but_unpublished=0`；
- 没有同类简单 transport 阻断；
- 剩余问题是电子态、输入真实性和 mode-specific scientific acceptance。

这些问题明确超出 Stage07B 的窄职责。启用 Stage07B 不会修复它们，反而可能让一个没有科学批准权的角色越权修改科学内容。

## 7. 对总目标的验收

### 已达到

- 代码侧没有稳定、可复现的共性 bug；
- 10/10 正常运行，无并发/harness/发布状态故障；
- 完整计算主线优先、核心子流程次之、外围流程不凑数的原则已明显生效；
- 软件缺口只登记、不作为科学拒绝理由；
- Stage06A、Stage06B、Stage07 和 orchestrator 的权限边界总体清楚；
- 科学拒绝是合法结果，未追求所有论文发布；
- 无论文/分子/固定答案代码特例；
- 无机械误阻断，Stage07B 不越权启用。

从最终科学决定看，6 个正确拒绝、3 个科学范围合理的发布、1 个错误发布，decision-level 正确处理为 9/10（90%），高于总目标的 80% 门槛。

### 未完全达到

- 4 个发布 bundle 并非全部无需人工复核；
- Stage07 的局部科学一致性检查仍会漏项；
- autonomous method freedom 与 hidden acceptance 的一致性不是每次都能正确执行；
- Stage07 的 `closed/passed` 自报不能等同于绝对科学正确。

因此可以结束本轮代码迭代，但不能把当前发布树解释为“无需后续质量抽检”。合理的生产策略是保留抽样科学 QA，并把发布任务中的 mode-specific acceptance 和电子态作为人工抽检重点。

## 8. 后续继续优化时的边界

如果未来开启新一轮，不建议：

- 给机械 gate 增加化学计量、电子态、溶剂、TS 或固定单位的判决规则；
- 针对本轮四篇论文、具体分子名或具体数值增加特例；
- 给 Stage06B 完整 source/hidden answer 权限；
- 启用 Stage07B 处理科学问题；
- 继续无上限扩张 Stage07 Prompt。

建议优先评估：

1. 对 Stage07 Prompt 去重和压缩；
2. 把“输入电子态矩阵”和“mode acceptance 矩阵”变成必填的结构化审计输出；
3. 同一 Stage07 turn 内先冻结 scientific audit，再允许 repair；
4. 用另一个强模型对同一批次做 blind audit，对比是模型特性还是任务结构导致；
5. 保持代码只验证矩阵结构完整，不判定矩阵中的化学结论。

这些是下一阶段的 Prompt/模型评估方向，不是 Round 20 继续追加的代码修复项。

## 9. 最终结论

Stage06/07 的工程管线已从“机械误阻断和运输不稳定”推进到“代码稳定、科学 Agent 决定成为主要误差源”。这是符合总目标边界的进展：论文能否构建取决于源材料和模型能力，而不是要求全通过；代码没有再把科学不确定性伪装成机械真理。

Round 20 后应停止继续打补丁。当前最重要的剩余工作不是增加代码规则，而是提高 Stage07 在长任务中的局部一致性可靠性，并对已发布任务保留科学抽检。Stage07B 在本轮没有触发依据。

# Stage06/07 v7 Round05：三路模型对照分析

日期：2026-08-23  
基线提交：`9f3dc87 fix(stage06-07): preserve hidden contract ownership boundaries`  
对应目标：[v7 总目标](STAGE06_07_V7_PROMPT_ITERATION_OBJECTIVE_20260823.md)

## 1. 测试范围与终态

三路使用同一组五篇论文、同一 Codex harness、high reasoning 和同一版本的
Stage06/07 代码；仅改变 Stage06/Stage07 模型组合：

| 组合 | 运行目录 | 终态 |
|---|---|---|
| DeepSeek→DeepSeek | `runs/stage06-07-v7-round5-same5-deepseek-deepseek-20260823` | 5/5 完成；1 发布、4 科学拒绝 |
| GPT→GPT | `runs/stage06-07-v7-round5-same5-gpt-gpt-20260823` | 5/5 任务进程结束；4 篇完成、1 篇 Stage06 retryable failure；完成的 4 篇中 1 发布、3 科学拒绝 |
| DeepSeek→GPT | `runs/stage06-07-v7-round5-same5-deepseek-gpt-20260823` | 5/5 完成；2 发布、3 科学拒绝 |

三路已发布的任务均满足：

- `mechanical_publish_blocked = 0`；
- pre-publish mechanical contract 通过；
- published-bundle 基础检查通过；
- 未观察到 hidden 目录、非法路径、JSON 读取失败或跨 mode profile 误检。

这里的“发布数量”不是质量目标。四篇科学拒绝分别有源材料闭合性依据；它们不能被
简单归为管线失败。

## 2. 逐篇对照

### `paper_108e6a1fb1e8f309`

三路均拒绝。Stage06/07 都指出主线 DFT 稳定性比较缺少控制性坐标，扩大或收缩到
核心子流程仍依赖同一缺失几何。拒绝与总目标“完整路线和重要子流程均无法闭合则拒绝”
一致，属于合理源材料拒绝，不是代码问题。

### `paper_849802730178edb8`

三路均拒绝。中心的周期 DFT+U/吸附位点比较需要未提供的 CDW 超胞和 Fe 位点坐标；
单个位点也不能脱离该缺失结构形成独立、代表性的任务。拒绝合理。

### `paper_efb2d9ec4fdb3b0f`

三路均拒绝。FM/AFM 比较和 J 拟合是论文的核心计算支撑，但几何、AFM 位点映射和
拟合闭合条件不足。仅复述表格数值不是独立的非平凡计算流程，因此拒绝合理。

### `paper_d2cba483b776cfb7`

论文的中心是 Pd 催化 difluoromethylation 的 DFT 机理。DeepSeek→DeepSeek 保守地
拒绝，理由是源没有显式 charge/multiplicity；DeepSeek→GPT 根据源中明确的反应平衡、
氧化态和自由基标签补出了量子态并发布；GPT→GPT 没有形成完整的 hidden profile
`comparison`/`semantic_acceptance_contract`，被 validator 正确归类为 retryable。

这里没有足够证据判定某个模型一定“科学正确”。需要把“源明确给出”“由源给出的守恒和
明确电子态标签唯一推导”“仅凭常见化学假设猜测”分成三档：只有前两档可作为闭合依据，
且第二档必须在审计记录推导；氧化态标签本身不能自动等价于唯一 multiplicity。这是
通用 Prompt 合同边界，不应加入 Pd 特例。

### `paper_1d3ae60b0873aff0`

论文是 Fe@PCN-224 的 paramagnetic pNMR 研究，正文/SI 以 Fe(III)–Cl、Fe(III)–OH
和 Fe(II) 三个模型的共同比较支撑配位环境判断。

- DeepSeek→DeepSeek 选择三模型比较，代表性符合目标；
- GPT→GPT 只保留 Fe(III)–Cl 单模型，并把另两个分支列为 omitted；
- DeepSeek→GPT 保留三模型比较。

这不是代码 bug。它是 Stage06A/Stage07 对“系列/候选集合/比较结论不能只取一个成员”
这一已有规则执行不稳定，属于 Prompt 可执行性和模型能力差异。下一轮可以把一条很短的
selection gate 前置到两个 prompt：若最终结论依赖 X-vs-Y、候选系列、构象集合或聚合量，
单个成员只能是中间证据；必须纳入最小完整比较，或给出源证据支持的不可构建原因。

软件判断也出现差异：GPT 登记了源明确命名但 toolbox 未列出的 pNMR 独立工具，DeepSeek
认为通用脚本后处理足够。应统一“独立程序/插件且路线实际依赖”与“公式或简单后处理”的
区分；有歧义时登记 observation/uncertain，不因软件缺口拒绝任务。

## 3. 问题归因

### 代码层

Round05 修复后的 ownership、profile scope、`applies_to_modes` 和 legacy contract
边界在这组三路结果中工作正常。没有发现新的 mechanical gate 误阻断或 validator 误报。
一个候选的通用缺口是：published bundle 检查还没有验证 autonomous
`task_spec.workflow_scope.autonomy_scope` 的存在、位置和枚举。

### Prompt/角色层

1. 比较/系列完整性规则虽已存在，但位置靠后、表述较长，不能稳定约束 GPT 的单分支选择。
2. 量子态“可推导”与“猜测”的边界不够明确。
3. 独立软件 gap 与可脚本化后处理的边界不够明确。
4. autonomous scope 的最终公共投影位置没有被写成单一、不可替代的交付合同。

### 模型能力层

GPT→GPT 的 Pd hidden contract 缺字段是模型没有完成结构化交付，不是代码错误；代码的
retryable 分类是期望行为。三路在同一论文上的选题差异也说明模型遵循长 prompt 的稳定性
不同，不能据此增加论文专用规则。

### 源材料层

三篇共同拒绝的论文确实缺少控制性几何/磁性/量子态信息。科学拒绝是有效终态，不应为
提高通过率而放宽闭合标准。

## 4. Round06 候选改进（尚未实施）

按风险从低到高：

1. **先做 Prompt 精简和前置**：在 Stage06A、Stage07 的选择/最终决定前加入同一段
   3 句 selection gate，要求最小完整比较并要求证据引用；不新增论文或化学特例。
2. **明确量子态证据三档**：源明确、源约束唯一推导、需要常见假设；第三档不得宣称
   closed，第二档必须记录推导链。
3. **明确软件 gap 三档**：独立工具缺失登记；简单脚本后处理不自动登记；不确定则记录
   observation，且软件缺口不触发科学拒绝。
4. **轻量公共合同检查**：只检查 autonomous `task_spec.json.workflow_scope.autonomy_scope`
   的 canonical 位置和合法枚举，并在 Stage07 报告中显式指出缺失；不判断科学内容，先配
   legacy fixture 再决定是否阻断发布。

不建议本轮引入 CanonicalTask 大型重构、自动中心性评分、论文关键词规则或 Stage07B。
只有同类“简单合同修复”在多轮、多论文中稳定重复，才重新评估是否需要窄 Stage07B。

## 5. 结论

Round05 的代码目标基本达成：机械层可解释、mode-specific hidden contract 不再互相
误检，合理科学拒绝能够保留。当前主要瓶颈是 Prompt 长度和模型执行一致性，以及一个可
通用化的 autonomous metadata 投影合同。下一轮应优先做小幅 Prompt 调整和轻量合同观察，
并用新的同样本/新样本对照验证；不能把单篇论文的科学判断差异误写成代码规则。

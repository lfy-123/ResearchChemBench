# v7 Round 02：三种模型组合结果分析

日期：2026-08-23  
测试计划：[Round 02 计划](STAGE06_07_V7_ROUND02_PLAN_AND_SAMPLE_20260823.md)  
三组结果目录：

- `runs/stage06-07-v7-round2-same5-deepseek-deepseek-20260823`
- `runs/stage06-07-v7-round2-same5-gpt-gpt-20260823`
- `runs/stage06-07-v7-round2-same5-deepseek-gpt-20260823`

## 1. 运行完整性

三批共 15 个子任务全部 `COMPLETED`，批次失败数均为 0。三组均使用 Codex、high reasoning、并发 5；三组使用同一批论文和同一 Prompt。

| 组合 | Stage06 | Stage07 | 发布 | 科学拒绝 | 机械阻断 |
|---|---|---|---:|---:|---:|
| DS→DS | DeepSeek | DeepSeek | 5 | 0 | 0 |
| GPT→GPT | GPT | GPT | 1 | 4 | 0 |
| DS→GPT | DeepSeek | GPT | 4 | 0 | 1 |

## 2. 同一论文的组合对照

### `paper_1c0c90e7aa74498c`（Molecular Structure 2026.145689）

- DS→DS：Stage06 选择 30 原子配体的 B3LYP 几何优化、频率和 XRD 内坐标比较，发布。
- DS→GPT：Stage06 选择几何、频率和热力学扩展，GPT Stage07 修复后发布，但最终 `execution_readiness=conditional`；机械通过。
- GPT→GPT：GPT 无法确认完整源坐标/CIF 或确定性构建，科学拒绝。

判断：这是 Stage06 模型对“SMILES/结构描述 + XRD 参数是否足以支持 source-constrained construction”的保守程度差异。DS 任务明确记录了确定性构建、指标鲁棒性和输入闭合证据；GPT 选择拒绝也有源证据依据。不能仅用发布率判定一方错误。`execution_readiness=conditional` 但仍发布值得作为观测项保留；本轮没有产生机械或静默发布错误。

### `paper_4ca4735bcf490d5a`（JOC 5c02269）

- DS→DS：选择两条对映 TS 的自由能比较，发布。
- DS→GPT：Stage06 选择同一催化体系的两 TS IGMH/频率核心子流程。GPT 识别出独立溶液相能量分支的 SMD 溶剂缺失，但保留闭合 IGMH 分支；科学审计通过。随后机械 gate 发现 `TaskInfo.archive_extractions` 缺少 schema 要求的 `source`/`destination`，状态为 `mechanical_blocked`，未发布。
- GPT→GPT：因溶剂、电子态和坐标抽取均不闭合而科学拒绝。

判断：DS→GPT 的机械阻断是有效保护，不是 gate 误报；它暴露的是 Agent 产出的 metadata contract 不完整，代码正确阻止发布并写入 `mechanical_approved_but_unpublished=1`。科学上，GPT Stage07 没有把缺失溶剂误用于 IGMH 分支，保留子流程是可解释的。

### `paper_7365b45a306d8947`（Org. Lett. 5c04997）

- DS→DS：选择 compound 1 两个相对构型的 conformer-search → DFT → GIAO 13C → Boltzmann → DP4+ 全链条，发布。该分支直接对应文中 R²/DP4+ 的相对构型结论。
- DS→GPT：同一个 DeepSeek Stage06 在另一轮中选择了单一 conformer 的 ECD/TDDFT 分支，GPT Stage07 审计为“一个直接但不完整的 ECD 组件”，仍发布。
- GPT→GPT：因缺少可恢复的六个 source conformer 几何而科学拒绝。

判断：三种结果显示模型在“源坐标不完整时是否允许 source-constrained construction、以及哪一个子流程最核心”上存在明显随机/能力差异。单一 conformer ECD 任务本身是非平凡、输入闭合的计算子流程，但不能代表论文完整的多化合物加权 ECD 结论；Stage07 receipt 已明确标注其为 partial component。当前 Prompt 已要求“不得用 supporting-only fragment 替代未闭合 direct claim”，但 Agent 仍可能将 direct component 解释为足够子问题。这是需要在更多样本中确认的 Prompt/模型边界风险，不足以认定代码 bug。

### `paper_8f891f94d53054e4`（JACS Au 5c01555）

- DS→DS 与 DS→GPT：均能从源材料恢复四个 P4 宏环种子，构建 ECD/构象比较任务并发布。
- GPT→GPT：判断源坐标附录截断，无法安全构建，科学拒绝。

判断：GPT 的拒绝是合法的源材料闭合判断；DS 的公开资产逐帧解析通过，任务包含四个种子和最低能构象后的 ECD，不是外围单点计算。差异主要来自解析/恢复能力，不是代码状态错误。

### `paper_b79009dc92a2bc4e`（Advanced Synthesis & Catalysis 70193）

三种组合均选择 EDA 复合物 singlet/triplet 优化、频率、自由能差和电荷转移分析，均发布，Stage07 修复数分别为 6、2、3。说明该论文的结构和核心物理边界较清晰，三种角色职责都能稳定工作。

## 3. 代码问题审查

本轮没有确认新的代码 bug：

- `applies_to_modes` 过滤和 mode-specific hidden projection 在所有发布任务中未产生跨模式误阻断；
- 三种组合均正确完成 Stage06→Stage07，科学拒绝不会被误报为机械失败；
- `paper_4ca...` 的 malformed `archive_extractions` 被机械 gate 捕获，发布状态明确为 `mechanical_blocked`，没有“Agent approved 但目录静默为空”的决策黑洞；
- 批处理脚本正确记录了实际 Stage06/07 模型、harness、推理强度和失败分类。

仍需持续观察但暂不修代码：

- Agent 自报 `contract_status=passed` 与编排器 evaluator load failure 仍可能不同；这次差异被 `orchestrator_mechanical_status` 正确记录并阻止发布，属于 Agent 合同自检能力问题，不是 gate 逻辑错误。
- `execution_readiness=conditional` 的科学批准是否应发布，取决于 `conditional` 是否只是非阻断软件/资源观察；本轮没有证据显示它导致不可执行任务，因此暂不改变发布规则。

## 4. Prompt/模型判断

Round 02 没有出现三种组合都重复的同一错误。主要差异是：

1. GPT Stage06 对 source-constrained construction 更保守，导致 4 篇科学拒绝；其中多数有明确缺失坐标/构象证据，拒绝不能视为失败。
2. DeepSeek Stage06 在同一论文的不同运行中可能选择不同中心子流程，说明存在采样/模型能力不稳定；其中 NMR/DP4+ 与单 conformer ECD 的差异需要后续复核，但目前没有足够证据把它归因于代码。
3. GPT Stage07 能识别并保留一个闭合的 IGMH 核心分支，但对“单个 ensemble member 是否足以支撑最终 ensemble 结论”的边界判断偏宽；这可能是 Prompt 语义仍不够明确，也可能是模型判断能力限制。

## 5. Round 02 结论与下一步

代码侧继续保持不变。下一轮先增加一个通用、极短的 Stage06/Stage07 语义澄清：当最终结论依赖成对比较、系列、构象/状态集合或加权 ensemble 时，单个成员只能作为中间/支持性计算，除非论文明确将其作为独立决定性子问题；Stage07 不应因“直接组件”措辞而自动把它升级为足够的最终任务。该澄清不包含论文、分子、软件、固定数字或答案。

随后用新随机样本复测三种组合。若仍只有单个模型的零散遗漏，则记录为模型能力限制，不继续堆叠规则。


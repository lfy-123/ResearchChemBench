# Stage06/07 v6 Round 2：三模型组合测试结果与归因

日期：2026-08-22

## 1. 测试设计

本轮在同一份代码、同一版 Prompt、同一批 5 篇 Stage05 通过论文上，同时运行三种组合：

| 组合 | Stage06A/06B | Stage07 | 论文数 |
|---|---|---|---:|
| DeepSeek→DeepSeek | `deepseek-v4-pro-0813` | `deepseek-v4-pro-0813` | 5 |
| GPT→GPT | `gpt-5.6-sol`（Pro reasoning） | `gpt-5.6-sol`（Pro reasoning） | 5 |
| DeepSeek→GPT | `deepseek-v4-pro-0813` | `gpt-5.6-sol`（Pro reasoning） | 5 |

三组论文完全相同：

`paper_5be4368e659d4b40`、`paper_9774cf028b321785`、`paper_75221561972a5c9c`、`paper_f171fa1f83158f7c`、`paper_525ba02ec147f066`。

结果目录：

- `runs/stage06-07-v6-round2-retry-same5-deepseek-deepseek-20260822`
- `runs/stage06-07-v6-round2-retry-same5-gpt-gpt-20260822`
- `runs/stage06-07-v6-round2-retry-same5-deepseek-gpt-20260822`

三组均 `COMPLETED`，15/15 论文正常退出。

## 2. 终态矩阵

| 论文 | DeepSeek→DeepSeek | GPT→GPT | DeepSeek→GPT | 科学判断 |
|---|---|---|---|---|
| `paper_525ba02ec147f066` | 发布 | 发布 | 发布 | DP4+ 两候选构型比较，输入闭合，适合作为核心子流程 |
| `paper_f171fa1f83158f7c` | 发布 | 发布 | 发布 | TD-DFT/ECD 计算主线，坐标和物理边界闭合 |
| `paper_5be4368e659d4b40` | 科学拒绝 | 科学拒绝 | 科学拒绝 | 周期界面、Ru/缺陷位点、磁态和 vacancy 参考态不闭合 |
| `paper_75221561972a5c9c` | 科学拒绝 | 科学拒绝 | 科学拒绝 | 掺杂周期模型、Na 位点、晶格和 CI-NEB endpoints 缺失 |
| `paper_9774cf028b321785` | 科学拒绝 | 科学拒绝 | 科学拒绝 | 中心 TS workflow 缺 charge/multiplicity，坐标资产不能提供两侧 TS |

所有已发布样本均为 `approved_with_repairs`，没有 `mechanical_publish_blocked`、`schema_load_failed` 或静默发布。三组 `stage_summary.json` 与 `late_stage_run_summary.json` 的发布状态一致。

## 3. 逐篇科学审查与 Stage06/07 角色表现

### 3.1 `paper_525ba02ec147f066`（bistaxascendin E）

Stage06 两个模型都选择 compound 5 的 NMR/DP4+ 两候选比较，而不是把 ECD、实验生物学或其他化合物拼成不可执行的“大任务”。这是对论文计算主线的合理核心子流程降级：该分支直接解决论文中 ROESY 未解决的 C-5′ 相对构型，并保留两侧候选、构象权重、shielding/shift 数据和 DP4+ 过程。

Stage07 在三种组合中都批准并修复了输入/元数据/绑定问题，证明 Stage07 的科学中心性和合同修复职责发挥稳定。修复包括 OCR 元素、零人口构象记录、mode-specific bindings 和 provenance。

但公开表面仍出现答案泄漏，详见第 4 节。这是当前唯一需要继续修补的共性 Prompt 问题。

### 3.2 `paper_f171fa1f83158f7c`（clathriamine A）

三组均保留完整的计算化学主线：源坐标 → 构象/热化学 → 两种 TD-DFT ECD → Boltzmann 加权 → 与实验 ECD 比较。该流程直接支撑绝对构型判定，非计算的 NMR、分离和生物实验被正确排除。三组均通过机械检查并发布；GPT 与 DeepSeek 的 Stage07 修复均有明确 source evidence，未发现阶段职责或代码状态错误。

### 3.3 `paper_5be4368e659d4b40`（Ru/SFM 周期 DFT）

GPT Stage06 和 DeepSeek→GPT 的 Stage06 均正确标为不可构建；DeepSeek→DeepSeek 的 Stage06 曾把 vacancy 分支标为 `candidate_ready`，声称可通过 source-constrained construction 枚举 Ru/缺陷位点。该判断没有满足“周期模型的原子位置/终止/占位、磁初始化、参考态和缺陷选择必须可复现”的通用闭合要求。

DeepSeek Stage07 最终独立拒绝了该候选，指出 Fe/Mo ordering、磁态、O2 reference、Ru/缺陷氧选择等 source-controlling degrees of freedom 缺失；GPT Stage07 对另外两次轨迹也作出同样拒绝。因此最终发布层安全，但 DeepSeek Stage06 的中间判断存在模型方差/能力问题，尚不足以证明需要论文特例规则。

### 3.4 `paper_75221561972a5c9c`（N/P 共掺杂石墨烯）

GPT Stage06 与 DeepSeek→DeepSeek 的 Stage06 拒绝；DeepSeek→GPT 的 Stage06 一次将 Na adsorption 子流程标为 `candidate_ready`，并自行引入 site enumeration/lowest-energy selection 方案。该方案不能恢复缺失的掺杂拓扑、晶格/真空、Na 位点和 CI-NEB endpoints，GPT Stage07 正确将其拒绝。三组最终结论一致，说明 Stage07 的独立审计能拦截 Stage06 的过度构造。

### 3.5 `paper_9774cf028b321785`（Cu(III) TS 选择性）

三组 Stage06/07 均拒绝。该论文的唯一中心计算流程是成对 Cu(III) reductive-elimination TS 比较，但缺少每个 scored stationary point 的 charge/multiplicity，坐标资产也不能提供两侧可映射 TS。把论文报告能量做算术不能替代新的非平凡计算。三种模型都识别到同一源材料阻断，属于正确科学拒绝。

## 4. 发现的真实问题与归因

### 4.1 共性 Prompt 设计问题：公共表面答案泄漏

在 `paper_525ba02ec147f066` 的已发布 reproduction 表面中，三种组合留下了不同程度的答案性内容：

- GPT→GPT：`supported_primary_claims` 直接写出 “5A is preferred over 5B”；
- DeepSeek→GPT：`why_this_subworkflow_is_core` 写出 “all-data 100% DP4+ probability”；
- DeepSeek→DeepSeek：`workflow_spec` 留下“selected epimer is unchanged ...”的答案性鲁棒性结论。

这些内容不是路线常数、物理边界或原始输入，而是 hidden target 的排序、数值或结论投影，违反 reproduction 与 autonomous 都只能保留中性任务目标/claim ID 的边界。Stage07 的 Prompt 虽已有动态泄漏审计条款，但最终检查在不同模型/轨迹中没有稳定覆盖所有 reproduction JSON 和 workflow metadata。

归因：这是 Prompt 的最终审计清单不够可执行、模型遵循不稳定的问题；不是论文特例，也不是 mechanical gate 的科学裁决问题。现有 gate 只验证结构/绑定形状，无法证明语义脱敏已经完成。

### 4.2 Stage06 的 source-constrained 过度构造

DeepSeek 在两篇周期 DFT 论文的不同轨迹中出现过一次 `candidate_ready` 过度判断，但同一模型的另一条轨迹能正确拒绝，且三组 Stage07 都最终拒绝。现有 Stage06 Prompt 已有通用的周期模型、TS 和 source-controlling field 约束；因此当前证据更符合模型方差/能力问题，而非需要加入论文特例规则的代码 bug。

保留观察项：下一轮在 Stage06A 的输出要求中增加更短、更硬的“未闭合 source-controlling degree 不得 `candidate_ready`”终检字段；如果跨新论文仍重复，才考虑进一步 Prompt 重构。

### 4.3 代码侧检查

本轮 15 个任务中：

- `mechanical_contract_passed` 与科学批准状态一致；
- 无 `mechanical_publish_blocked`、无 `mechanical_approved_but_unpublished`；
- 无 evaluator schema load failure；
- 三种模型组合的 batch 状态均正确从 `RUNNING` 进入 `COMPLETED`；
- Round 2 代码回归：`179 passed`。

因此本轮没有发现新的代码 bug。`workflow_scope_kind` 兼容读取修复已生效；中间 `workflow_scope_kind` 在 summary 中缺失不再影响实际 handoff/审计，后续只需考虑可观测性，不应归因成科学失败。

## 5. 模型组合比较

- 最终科学终态完全一致：2 篇发布、3 篇科学拒绝。
- GPT Stage07 与 DeepSeek Stage07 在同一论文上的最终科学判断一致；差异主要在 Stage06 是否把源控制不完整的周期模型暂时标成 `candidate_ready`。
- DeepSeek→GPT 的组合没有在最终质量上超过同模型组合，但 GPT Stage07 对 DeepSeek Stage06 的过度构造能稳定纠正；这是“窄审计 Agent”设计有效的证据。
- GPT 与 DeepSeek 的单篇中间轨迹差异不能用发布率比较。当前样本支持：Stage07 使用哪一种模型不是决定最终科学质量的主因，Prompt/独立审计比单纯换模型更重要。

## 6. Round 3 决定

进入 Round 3，但只做一项通用 Prompt 修补：要求 Stage07 在批准前生成并逐文件核对 `public_answer_scan`，分别覆盖 reproduction 与 autonomous 的 Markdown、JSON、文件名、route evidence 和 rubric；扫描对象由 hidden reference 动态派生，不使用论文名、分子名、数字或固定关键词。任何 target value、tolerance、ranking/trend、preferred label 或 conclusion proposition 出现在 public metadata 时，必须中性化并在最终审计表中标记为已修复。

不修改 mechanical gate 来执行科学语义，不新增论文特例；周期 DFT 的 `candidate_ready` 方差仅作为 Stage06 Prompt 的短终检提示和观测项。


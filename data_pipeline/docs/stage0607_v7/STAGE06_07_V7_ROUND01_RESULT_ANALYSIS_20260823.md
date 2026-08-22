# v7 Round 01：双模型结果分析

日期：2026-08-23  
Prompt commit：`9ee69f5`（阶段协议优化），测试记录提交：`b922a04`  
模型：DeepSeek `deepseek-v4-pro-0813`；GPT `gpt-5.6-sol`  
运行目录：

- `runs/stage06-07-v7-round1-same5-deepseek-20260823`
- `runs/stage06-07-v7-round1-same5-gpt-20260823`

## 1. 运行完整性

两批各 5 篇全部完成，批处理状态均为 `COMPLETED`，每篇 CLI 退出码为 0。两批均使用 Codex harness、Stage06/07 `reasoning_effort=high`、并发 5。未发现因批处理脚本、凭据传递、阶段状态汇总或 Stage07 未运行导致的代码级失败。

统计如下：

| 模型 | 科学批准/发布 | 科学拒绝 | 机械阻断 | Stage06 retryable |
|---|---:|---:|---:|---:|
| DeepSeek | 4 | 1 | 0 | 0 |
| GPT | 1 | 4 | 0 | 0 |

发布率差异不能单独解释为 Prompt 优劣；本样本中两组论文不同，且 GPT 组恰好包含四篇输入闭合性较差的论文。

## 2. 逐篇核对

### DeepSeek 组

1. `paper_0b4e294e099f72da`（JACS 5c17740）：Stage06 选取 Ni 催化 C-糖基化的 beta/alpha TS 比较，属于论文核心机理子流程。Stage07 发现 L-beta/L-alpha 坐标在源抽取中重复、与不同能量/频率证据冲突，拒绝直接沿用，改选有独立坐标和证据的 J radical-capture beta/alpha 比较，并记录了证据和修改文件。该 workflow redesign 符合“核心子流程优先于错误的完整候选”原则；需持续观察 Stage07 重设计是否始终保留原科学问题语义，但本例没有发现越权或机械错误。
2. `paper_584ac85fd9f0b344`（ICA 2025.123000）：选取四个源坐标体系的完整计算核心（优化、频率、TDDFT、Q/B/CT 分类及成对比较），代表性充分。Stage07 5 项修复后发布，机械检查通过。
3. `paper_5ab87c809ec4a7d0`（Biomaterials 2025.123872）：Stage06/07 识别 VP 单层、吸附构型和表面参考几何缺失，无法在不猜测的情况下重建吸附能、Bader 电荷和键活化，科学拒绝正确；这不是代码失败。
4. `paper_94b0a8ae694590ea`（ACS AMI 5c23007）：Stage06 标为完整计算核心，任务围绕三种 TTA 衍生物的 B3LYP HOMO/LUMO 与 SWCNT 对齐，输入、边界和交付链条闭合，Stage07 修复后发布。该任务代表论文的计算电子结构主线；本次未发现外围选题证据。
5. `paper_a55b812fd43d286d`（D5OB01996）：选取 Cu 催化 B–H insertion 的完整 DFT 自由能剖面，明确两个步骤的平衡参考态、TS 频率和速率决定步骤，符合完整路线优先原则，Stage07 修复后发布。

### GPT 组

1. `paper_4b4e0bec6df820fc`（D5CP04404A）：目标是轴向卤素配位对 FeN4/C 磁矩与 OH 吸附的影响；源中缺失石墨烯注册、N4/金属/配体及吸附位点坐标，也无确定性构建协议，拒绝正确。
2. `paper_6ff878fdedc4533d`（JACS 5c17804）：目标是 [20]collarene⊃C60/C70 结合/形变能比较，但坐标抽取只有一个 730 原子宿主记录，无法区分客体、复合物和孤立参考态；拒绝正确。
3. `paper_761a1e321d9bc798`（D5CC06226H）：目标是 DTF[11]CPP 的跃迁及自由基阳离子轨道/自旋密度，但缺少中性和自由基阳离子源几何，拒绝正确。
4. `paper_b5c446c7067dd511`（Molecular Structure 2025.144503）：四个受体的激发态/HLCT 计算没有坐标、构象协议或机器可读电荷/多重度，拒绝正确。
5. `paper_d1135c5a2aaf5d4b`（Bioorganic Chemistry 2026.109529）：选取 compound 5B 两条催化剂自由路径的 DFT 机理比较，坐标附录可用，覆盖核心计算结论，Stage07 修复 3 处后发布。

## 3. 代码与 Prompt 判断

### 已验证没有出现的代码问题

- 两批所有完成任务均正确进入 Stage07；没有“Stage06 成功但 Stage07 未运行”的汇总错误。
- 科学拒绝不会被误记为机械失败；`mechanical_publish_blocked=0` 与 `publication_state=not_applicable` 一致。
- 已有 `applies_to_modes` 过滤和 mode-aware hidden projection；本轮发布任务的两个模式机械检查均通过，没有观察到跨模式 acceptance profile 误阻断。
- Stage07 的修复/重设计、变更文件、审计结论和最终发布状态均写入 audit receipt；没有发现静默发布或批准后无状态记录。

### 本轮尚未证明的风险

- `published_bundle_mechanical_check()` 仍偏结构级，不能替代 Stage07 的科学泄漏审计；本轮不能据此声称所有公共 route evidence 都没有答案性内容。
- Stage06 的 workflow 代表性主要仍由 Agent 的 source-backed rationale 证明，没有代码自动判断标题/摘要/主图/结论覆盖度。本轮 10 篇中没有足够证据证明它会稳定发现“可执行但外围”的候选。
- DeepSeek 的 `paper_0b4e...` 由 Stage07 重设计 workflow，说明审计能力有效，但也提示需要在后续样本中检查“重设计是否保持科学问题”这一通用边界。

## 4. Round 01 结论

本轮没有发现可重复、模型无关的 Prompt 缺陷，也没有确认新的代码 bug。DeepSeek 与 GPT 的批准率差异主要由样本源材料可执行性和模型能力共同造成，不能据此调整 Prompt。下一轮应采用同一批 5 篇论文分别运行三种组合：DeepSeek→DeepSeek、GPT→GPT、DeepSeek Stage06→GPT Stage07，以隔离 Stage06 选题能力与 Stage07 审计能力；只有出现同一输入在多个组合中重复的角色越权、代表性误判、脱敏泄漏或状态错误，才修改通用 Prompt/代码。


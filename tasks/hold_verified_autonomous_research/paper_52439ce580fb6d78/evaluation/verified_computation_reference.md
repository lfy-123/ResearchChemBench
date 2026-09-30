# Verified computation reference — paper_52439ce580fb6d78 / autonomous_research

## 当前状态（2026-09-23 更正）

按用户要求迁入 HOLD，等待后续独立复核。此前本文件声称“当前公开输入仍为 1T-like”，该判断有误：2026-09-21 input_closure 已修正上下 Se 面内对齐和六角晶格精度，当前任务副本含此修复。acceptance JSON 的 prior_as_published_input_valid=false 指修复前版本；同一 JSON 的 current_public_input_facts_valid=true 才描述当前版本。旧 limitation 字符串未更新，不能据此否定现有输入。详见 [HOLD 问题与交接说明](task_provenance/hold_review_20260923.md)。

## 已有成功计算流程

1. 从正文 H 相原型建立 VSe2 单层，PBE+U、500 eV 平面波截断做结构松弛；不把优化终态作为公开初始坐标。
2. 在一致计算口径下比较 FM、NM、周期 2 与周期 4 AFM。已算候选中 FM 最低，周期 4 AFM 高 21.07552 meV/化学式。
3. 明确磁矩方向和 K/K′ 坐标，计算含 SOC 的谷能级并由独立 V-d 投影确认态身份。
4. 比较 7×7×1 和 9×9×1 网格：劈裂分别为 153.878 与 152.058 meV，均满足现行 137±25 meV 规则。
5. 后续 input_closure 修复公开原型的 H/T 身份错误：上下 Se 的 xy 均为 (1/3,2/3)，原始 a=3.31 Å、初始 z=0.58/0.42 保留。记录对称性 P-6m2 (187)，与已验证 H 相对象一致。

## 验证范围与证据

这条作者路线支持当前 FM/SOC 科学子目标；不声称已复现所有晶格、磁矩或整篇论文。优化 a=3.383116 Å、V 投影磁矩 1.5335 μB 与论文约 3.31 Å、1.29 μB 的未评分差异保留。HOLD 状态不等同于缺计算；本轮未新增量化计算，也没有变更科学目标或容差。

证据（仓库根相对路径）：
- runs/hold_verification/group_6/paper_52439ce580fb6d78/20260921_input_closure/report/supplementary_verification.md 与 results.json。
- runs/hold_verification/group_6/paper_52439ce580fb6d78/20260921_acceptance/report/supplementary_verification.md 与 results.json。原始输入、输出及各项规则的明细沿其中路径追溯。

本文件是 evaluator 私有计算记录，不是 agent 输入或替代评分规则。

# paper_52439ce580fb6d78：HOLD 交接与旧判断更正

日期：2026-09-23；验证分组：group_6。按用户要求，两个模式从 verified_tasks 移到 hold_verified_autonomous_research / hold_verified_paper_reproduction。本轮不重算，不改公开输入或 evaluator，不改 docs/verification 原记录。

## 已确认的事实

上一轮“当前公开输入仍是 1T-like”判断不正确，源自把旧状态字段当作现状。2026-09-21_input_closure 已修复两模式的 vse2_2h_primitive.json，当前副本也包含修复：上下 Se 的面内分数坐标均为 (1/3,2/3)，z 分别为 0.58、0.42，V 为 (0,0,0.5)；六角 b 向量为 (-1.655,2.866544086526492,0) Å。旧 1T-like 输入的下层 Se 是 (2/3,1/3,0.42)。当前没有把优化后终态坐标作为初始结构，a=3.31 Å 和初始高度保持原型值。

正文 Fig.1 和 SI Table S1 支持研究 H 相 VSe2 与 137 meV 谷劈裂。已有正确 H 相计算给出 7×7/9×9 SOC 劈裂 153.878/152.058 meV，满足现有 137±25 meV；FM 低于已算 NM、周期 2/4 AFM，周期 4 AFM 高 21.07552 meV/化学式。

## 当前真正需要处理的问题

20260921_acceptance/report/results.json 同时包含 prior_as_published_input_valid=false、current_public_input_facts_valid=true，以及未清理的“literal public supplied structure is still centrosymmetric1T-like”旧描述。前一布尔值针对修复前输入，不能覆盖后一布尔值和当前坐标事实。上一轮生成的 reference 错误沿用了旧描述；本轮已更正两份 reference。任务留在 HOLD 是本次用户指定的审查安排，不应表述成“当前模型已经证实错误”。

尚未发现仅凭现有证据就必须新增量化计算的缺口。未评分的差异仍存在：优化 a=3.383116 Å、V 投影磁矩=1.5335 μB，对应原文约 3.31 Å、1.29 μB；不得将当前通过扩展为全文逐数复现。当前 evaluator 核心是有限磁序候选中的 FM 和 SOC 谷劈裂。

## 后续 agent 的处理建议

先以本 HOLD 的 task.md、公开 primitive 和五个 evaluator 文件为当前任务标准，核对修复前后坐标与真实 H 相生产输入的来源关系，独立确认当前原型的 H 相对称/配位身份，再核对两套 SOC 根及 K/K′、磁矩方向、能量单位和磁序比较。将验收 JSON 的旧状态与新状态区别写清，不因 prior_as_published_input_valid=false 重新宣布当前输入错误，不把优化结果回填为 agent 初始坐标。若所有对应关系成立，只需记录当前包审核结论，交用户决定解除 HOLD；只有找到实际未覆盖的必评项再说明是否需要额外计算，不重复已有成功计算。不要移动到 final，等待用户决定。

## 证据入口（均相对仓库根目录）

- runs/hold_verification/group_6/paper_52439ce580fb6d78/20260921_input_closure/report/supplementary_verification.md：明确记录输入已改、对称性 P-6m2 (187) 和未注入终态。
- runs/hold_verification/group_6/paper_52439ce580fb6d78/20260921_input_closure/report/results.json：输入修正与已有计算关系。
- runs/hold_verification/group_6/paper_52439ce580fb6d78/20260921_acceptance/report/results.json：包含新旧混合状态字段、原始证据路径和逐规则判断。
- runs/hold_verification/group_6/paper_52439ce580fb6d78/20260921_acceptance/report/supplementary_verification.md：FM、SOC 当前验收。
- papers/paper_52439ce580fb6d78/documents/main.pdf 与 supplementary_001.pdf：论文依据。

## 2026-10-28 V3范围与逐命题证据复用

r_bn_s1_energy/r_cc_s1_energy：原生日志2.1401/2.7731 eV对源2.1406/2.7731；r_bn_bright_energy/r_bn_bright_strength：BN S5 3.6111 eV、f=1.8535，对源3.6113/1.8524；r_cc_bright_energy/r_cc_bright_strength：CC S2 3.0152 eV、f=.4081。六个保留硬窗均有对应原生日志，E±.05 eV和f±.02不变。r_bn_strength_pattern/r_cc_strength_pattern：逐根六态E/f表支持弱最低态和不同亮态位置；r_bn_s1_explanation：INDEPENDENT_COMPARISON的HOMO/LUMO实值BN−4.997677/−2.224685、CC−5.750137/−2.354689 eV，跃迁85→86主导及签名对应支持解释。四个绝对轨道数值及两S1组态移为非评分证据；不是删除最终激发能目标。

证据缺口：SI S11 Sr/H尤其S2–S4不匹配，不能声称定量CT面板已复现或由缩隙推出CT增强；旧中间TD checkpoint原像缺失，现存同哈希fchk和原生日志仍支持结果核验，但精确重启不保证；没有验证全局自旋/全部泛函、发射态或器件推广；这些不属于当前问题。本轮未重新计算、未进行盲测或语义评分验证；以下历史正文逐字保留，不继承旧PASS为V3全部通过。活动标准以scoring_rules.json为准。

# V2 验证计算参考：BN-AkFlu versus CC-AkFlu molecular excitations

论文：`paper_9a58a1fa6ed7d780`；模式：`autonomous_research`；发布整理：2026-10-17。

**验收：当前冻结 V2 完整任务范围内独立严格通过。** 不依赖用户接受数值偏差；不代表论文全文或补充材料全部数值均已复现。

本文件仅供私有 evaluator / 维护者使用，不得放入被测 agent 的公开输入。

## 发布与验收绑定

- 科学题面、公开输入、关键点、结论、评分及容差逐文件从已复审的 `upgrade_version2` 复制，评分策略保持 `dual_axis_100.scientific_results.v1`。
- 历史开发快照和计算缓存未复制进发布包，原件仍在源目录与 docs 中。
- [独立验收裁定](../../../../docs/v2_verification/maintenance/job_followup_20261017/COORDINATOR_REVIEW/paper_9a58a1fa6ed7d780/DECISION.json)；[原始复审全文](../../../../docs/v2_verification/maintenance/job_followup_20261017/COORDINATOR_REVIEW/paper_9a58a1fa6ed7d780/REVIEW.md)；[原生证据解析](../../../../docs/v2_verification/maintenance/job_followup_20261017/COORDINATOR_REVIEW/paper_9a58a1fa6ed7d780/NATIVE_READBACK.json)。
- [本包证据和资源索引](verification_evidence_index.json)记录原生文件路径、哈希、处理器、内存和程序打印时长。

## 计算过程及结果对照

以下为独立复审报告原文。报告中“未导出”指独立裁定当时的历史状态；本次已根据用户授权复制至 V2 发布目录。没有重新计算或修改原裁定。

# BN-AkFlu / CC-AkFlu：当前 V2 任务独立复审

日期：2026-10-17 UTC。论文 paper_9a58a1fa6ed7d780。裁定：PASS_STRICT_CURRENT_FROZEN_V2_TASK，适用 upgrade_version2 的 AR、PR 两模式。不是全文或所有补充材料数值复现，也不是已运行盲测 agent 或校准语义评分器。

## 判定边界

逐字回读两个 agent_input/task.md、五个关键点及最终结论后，当前科学问题是：这两个指定完整气相分子的内部 BN 替换如何影响低能电子激发，以及哪些分子解释和比较有证据。关键点明确不强制某一个 Sr/D 指标、亮根序号或跨几何分解。PR 披露 B3LYP/6-311G(d,p)、Gaussian、Multiwfn 及 S11/S14/S15 来源，要求保留描述符分歧；没有把 S11 的每一数值规定为独立必须匹配的目标。

本裁定依靠正面复现的轨道变化、12 个能量/振子强度、物理态对应和真实最低点证据，而不是依据“允许未解答答案”授通过。已有 Multiwfn 密度分析也已实际执行，S11 不一致并未删除或被宣布合理。不得把本裁定改述成源定量 CT 解释、全 SI 面板已复现。

2026-10-12 状态曾将完整 S11 面板设为整任务的必过门；本次对当前冻结合同逐项独立裁定，纠正该额外门的适用范围，不改变题面、节点、目标、容差或来源数字。80 项候选证据均仍可读；仅两份 scoring_rules 的策略字符串与旧哈希不同，反向替换 scientific_results.v1 为 open_research.v1 后逐字哈希相同。这是用户授权的 10 月16日评分策略修改，未改变科学范围。

## 原文、原生证据与实际结果

亲自读取正文物理第3页（期刊1056）、SI S3/S39/S41/S42/S43及结构表 S21/S22。作者采用 Gaussian16、B3LYP/6-311G(d,p)，单分子气相。原生 Opt/Freq/TD 输入和日志一致：40原子、170电子、q0/m1、5D/7F。BN 与 CC 优化均原生四项 YES，各有114个正频率，最低36.8935/41.7933 cm⁻¹。实际 Opt 位移与 Freq 后另打印的预测位移已区分。两个 full TD 原生均 expansion-vector convergence；逐条重读 39,673 个 X/Y 系数，12根的 2Σ(X²−Y²) 与1最大差小于0.000015。未声称单独完成全局自旋/Stable门。

|比较量|论文|真实计算|判断|
|---|---:|---:|---|
|BN HOMO / LUMO，eV|−5.00 / −2.22|−4.997677 / −2.224685|与源所印组成量精度相容|
|CC HOMO / LUMO，eV|−5.75 / −2.35|−5.750137 / −2.354689|与源所印组成量精度相容|
|BN / CC KS gap，eV|2.78 / 3.40|2.772992 / 3.395448|缩隙结论及大小一致；源gap由已舍入组成量相减，不声称逐末位相等|
|BN S1，eV|2.1406|2.1401|差−0.0005eV|
|CC S1，eV|2.7731|2.7731|打印精度内相同|
|BN−CC S1差，eV|−0.6325|−0.6330|差−0.0005eV，约源效应0.079%|
|BN亮S5 f|1.8524|1.8535|差0.0011，约0.059%|
|CC亮S2 f|0.4081|0.4081|打印精度内相同|

BN六根能量差−0.0005至−0.0002eV；CC六根E/f与所印源值一致。BN S1 f0.0081对0.0080属于弱跃迁的小绝对残差；原TD首算为0.0080，续算full-coefficient为0.0081，两个输出均保留并统一使用与密度分析配对的后者，不择优。以上微小残差不能仅由打印舍入解释，也没有已证明版本因果；合理性基于同物理对象/方法/收敛、12根的系统一致性、主组态和效应量级，非新增通用经验容差。

原生S1均85→86主导，签名跃迁核对比支持S1↔S1，0.9362942665对下一候选0.0001071472。不同指标NTO密度相似度0.9389092929；不能混写成旧预审误记的0.957363。保存fchk的HOMO/LUMO已独立解析，支持BN使HOMO上升约0.75246eV、LUMO上升约0.13000eV。KS gap不等同激发能；它与匹配TD结果共同支持论文的分子解释。已经完成的固定几何两对照保留S1效应符号（−0.5081/−0.5991eV），是额外控制，不是最低点或泛函不变性证明。

## 六个必要节点

|节点|独立判定依据|
|---|---|
|kp_identity|原生原子/电子/自旋、完整图与映射、源结构和优化后对应可追溯。|
|kp_quantitative_evidence|真实12根E/f及BN/CC同定义比较、物理根对应；不混淆BN-Flu S4与BN-AkFlu S5。|
|kp_scientific_answer|HOMO上移更多、缩隙、匹配S1降低及振子强度分布变化，实际正面复现论文相关分子结果。|
|kp_validity_and_uncertainty|最低点、完整响应归一化、态对应及已有几何控制支持必要结论；密度定义差、模型限制及不明确亮根对应如实保留。|
|kp_bounded_conclusion|仅两分子的低能电子结构，不推导发光率、非辐射速率、晶体堆积或器件性能。|
|bounded_answer|以上证据共同回答冻结科学问题；未借由无结果或不收敛来声称不可辨识。|

## 未通过的扩展主张及限制

- S11 Sr/H数值依然不匹配，尤其S2–S4。源Sr=[0.797,0.795,0.919,0.913]，独立积分约[0.78437,0.91367,0.74134,0.74959]。不能称这些差异为小误差；也不能把来源态/后处理缺项已解决。
- 不接受“定量CT面板全部复现”、更强CT由缩隙推出、完整展宽吸收谱或全部源MO文字标签已复现。源S14/S15部分HOMO+1标签冲突已保留。
- 旧中间TD checkpoint原像已缺失；历史收集清单/依赖哈希、现存同哈希fchk与两份原生日志可支持结果核验，不保证精确重启缺失的中间文件。
- 未证明全部泛函/全局自旋最低态、PLQY、发射峰、动力学、固态/器件结论；这些不在冻结任务内。

不需为当前完整冻结问题重跑已经成功的量化计算。若未来把定量CT/S11或器件结论加入目标，必须重新开验收门，不继承本PASS。本轮不修改发布目录或ZIP，不启动新科学计算。

## 可复查记录

本目录 NATIVE_READBACK.json、SOURCE_AND_EVIDENCE_AUDIT.json、INDEPENDENT_COMPARISON.json 保存独立原生提取、源页、80项证据哈希与任务合同绑定；W06_CLOSEOUT.md/json为受审工人交付，不是裁定本身。


## 原生计算时长与资源

每条时长均照录原日志中的阶段记录；CPU time 与 wall/Elapsed time 不混用。缺失字段标为未记录，不推测总耗时，也不把多作业 CPU 时长当日历时长。完整索引另见 verification_evidence_index.json。

| 原生文件 | 日志处理器/内存设置 | 原生日志时长 |
|---|---|---|
| [docs/upgrade_tasks_verification/group_3/papers/paper_9a58a1fa6ed7d780/outputs/legacy_BN_optfreq/stdout.log](../../../../docs/upgrade_tasks_verification/group_3/papers/paper_9a58a1fa6ed7d780/outputs/legacy_BN_optfreq/stdout.log) | CPU=4; mem=12000MB | Job cpu time:       0 days  0 hours 24 minutes 31.3 seconds.<br>Elapsed time:       0 days  1 hours  0 minutes 42.6 seconds.<br>Job cpu time:       0 days  2 hours 12 minutes  0.3 seconds.<br>Elapsed time:       0 days  6 hours 21 minutes 57.9 seconds. |
| [docs/upgrade_tasks_verification/group_3/papers/paper_9a58a1fa6ed7d780/outputs/legacy_BN_TD6_fullcoeff/stdout.log](../../../../docs/upgrade_tasks_verification/group_3/papers/paper_9a58a1fa6ed7d780/outputs/legacy_BN_TD6_fullcoeff/stdout.log) | CPU=20; mem=8GB | Job cpu time:       0 days  0 hours 29 minutes 50.6 seconds.<br>Elapsed time:       0 days  0 hours  1 minutes 29.8 seconds. |
| [docs/verification/group_1/paper_9a58a1fa6ed7d780/artifacts/gaussian_batch/supp_bn_akflu_td_b3lyp_optgeom/stdout.log](../../../../docs/verification/group_1/paper_9a58a1fa6ed7d780/artifacts/gaussian_batch/supp_bn_akflu_td_b3lyp_optgeom/stdout.log) | CPU=4; mem=12000MB | Job cpu time:       0 days  0 hours 28 minutes 28.0 seconds.<br>Elapsed time:       0 days  2 hours  1 minutes 21.9 seconds. |
| [docs/upgrade_tasks_verification/group_3/papers/paper_9a58a1fa6ed7d780/outputs/CC_AkFlu_author_B3LYP_6311Gdp_optfreq_TD6_a1/stdout.log](../../../../docs/upgrade_tasks_verification/group_3/papers/paper_9a58a1fa6ed7d780/outputs/CC_AkFlu_author_B3LYP_6311Gdp_optfreq_TD6_a1/stdout.log) | CPU=20; mem=70GB | Job cpu time:       0 days  0 hours 13 minutes 12.9 seconds.<br>Elapsed time:       0 days  0 hours  0 minutes 40.7 seconds.<br>Job cpu time:       0 days  2 hours 17 minutes 56.1 seconds.<br>Elapsed time:       0 days  0 hours  6 minutes 57.9 seconds.<br>Job cpu time:       0 days  0 hours 56 minutes  1.8 seconds.<br>Elapsed time:       0 days  0 hours  2 minutes 49.9 seconds. |

## Current scoring migration — 2026-10-19
Active policy: paper_science_v2, 100 binary scientific-result points with intermediate and final conclusions. Active rule/reference files supersede historical scoring weights or freezes. No process score or multiplier remains. This migration is not new computation or new chemical acceptance; independently strict frozen-scope status remains unchanged. Preserved limitations: BN/CC source six-state energies and oscillator strengths were actually computed; BN small energy residuals -0.0005 to -0.0002eV and S5f+0.0011 remain distinct from printed source values. S11 Sr/H especially S2-S4 remains materially unmatched; no exact CT panel or broader all-SI reproduction is certified. Source HOMO+1 wording conflicts are not treated as physical occupied acceptor targets. No global method/spin proof or optical/device kinetics.

## Scoring-contract repair — 2026-10-19, round 3

- Confirmed independent molecular results were bundled: split S1 HOMO-to-LUMO character into BN and CC leaves (5+5); independent missing/wrong outcomes do not erase the other molecule. Same total 70 intermediate/30 conclusion.

The source and native calculations above remain unchanged historical evidence. Active mode-specific rules govern current scoring; this edit does not certify a new chemistry run or alter strict acceptance.

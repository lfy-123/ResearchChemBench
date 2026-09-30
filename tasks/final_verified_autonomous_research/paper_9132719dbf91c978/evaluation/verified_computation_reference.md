# 已验证成功计算过程：paper_9132719dbf91c978 / autonomous_research

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 4；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_4.md)
- [正文](../../../../papers/paper_9132719dbf91c978/documents/main.pdf)；[补充材料](../../../../papers/paper_9132719dbf91c978/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/terminal_h2_closure_20260923/result.json)；[历史结构化结果](../../../../docs/verification/group_4/paper_9132719dbf91c978/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_autonomous_research/paper_9132719dbf91c978/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_autonomous_research/paper_9132719dbf91c978/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

目标为指定中性 singlet、77 原子 INT-G 的终端 H2 还原消除，不是整条 Pd 催化循环。SI S10/S12 支持 PBE0-D3BJ/def2-SVP 气相 Opt/Freq，然后在相同几何做 MN15/def2-TZVP、SMD(N,N-dimethylacetamide) 单点；Gaussian16 C.01 对应作者 A.03。复合 G=`EMN15,solv+GcorrPBE0,gas`，298.15 K/1 atm。

## 3. 成功计算链与结果

作者 INT-G 与 TS6 身份 → 两者 Opt/Freq → 同几何高层 SP → TS 的 H–H 模投影 → 正/反 IRC 54/8 点 → 两端直接自由 Opt/Freq → 正向 η²-H2 结合产物的 17 点释放扫描及后续 2 个已收敛扩展点 → 分离的 75 原子 Pd(0) 与 H2 各自 Opt/Freq → 片段高层 SP → 比较完整终端步骤。

INT-G 225 正频；TS6 225 模中唯一 −478.5853 cm⁻¹，H76–H77 为反应模；两 IRC 后端点各 225 正频。正向 IRC 最初得到的是结合 H2，不是自由 H2；释放后 Pd–H 为约 5.184/4.667 Å，才用独立片段计算确认 75/2 原子端点（219/1 正频）。

| 对象 | 复合 G，Eh |
|---|---:|
| INT-G | −2390.18969245 |
| TS6 | −2390.18847425 |
| 分离 Pd(0) | −2389.02277737 |
| H2 | −1.16972074406 |

`(GTS6−GINTG)×627.509474 = 0.764432041 kcal/mol`，满足 0.9±2.0。分离产物反应 ΔG 为 −1.760580779 kcal/mol（1 atm）；若将所有溶质改为 1 M 则为 +0.133747667，不可混用两种零点。这一产物比较是连接性解释，不是本轮新增评分靶。

13 个完整有效计算的 elapsed 合计 56.0244 h、原生日志 CPU 合计 1095.6769 h，非并行日历时长。释放扩展后第 3 点失败，只有前两个确已收敛点作为后继结构来源；失败尾部不计成功步骤。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| intg | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/int_g_full_si_pbe1pbe_optfreq_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log) | -2389.17238657 / -2388.626963 | 225 模；负模 无；最低正频 21.7744 cm⁻¹；日志正常结束 |
| ts6 | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_full77_si_pbe1pbe_optfreq_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log) | -2389.17206797 / -2388.628271 | 225 模；负模 [-478.5853]；最低正频 22.2074 cm⁻¹；日志正常结束 |
| intg_sp | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log) | -2390.73511645 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| ts6_sp | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log) | -2390.73227125 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| forward | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log) | -2389.17882019 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| reverse | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log) | -2389.17229198 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| forward_min | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_forward_irc_endpoint_optfreq_20260916/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log) | -2389.17900611 / -2388.634391 | 225 模；负模 无；最低正频 21.7055 cm⁻¹；日志正常结束 |
| reverse_min | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_reverse_irc_endpoint_optfreq_20260916/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log) | -2389.17236547 / -2388.627221 | 225 模；负模 无；最低正频 20.8626 cm⁻¹；日志正常结束 |
| scan | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_h2_bound_product_source_level_release_scan_20260918/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_h2_bound_product_source_level_release_scan_20260918_hpc20_p6/stdout.log) | -2389.15991111 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| pd0 | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_released_pd0_source_optfreq_20260922/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log) | -2387.99325689 / -2387.463345 | 219 模；负模 无；最低正频 20.9212 cm⁻¹；日志正常结束 |
| h2 | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_released_h2_source_optfreq_20260922/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log) | -1.16382779781 / -1.165372 | 1 模；负模 无；最低正频 4384.1493 cm⁻¹；日志正常结束 |
| pd0_sp | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_released_pd0_source_mn15_dmac_sp_20260922/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log) | -2389.55268937 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| h2_sp | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/recovery27_20260915/ts6_released_h2_source_mn15_dmac_sp_20260922/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log) | -1.16817574406 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| release accepted extension | [输入](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_h2_release_final_segment_source_scan_20260921_hpc20_p6/input.com) / [输出](../../../../docs/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_h2_release_final_segment_source_scan_20260921_hpc20_p6/stdout.log) | 前缀范围见说明；不取失败尾部数值 | 仅作已接受路径/扫描几何证据；不采用失败尾部的频率/热化学；整日志非正常终止，仅采用已接受前缀；仅第 1、2 个收敛释放点；第 3 点失败未纳入有效链。 |

### 输入参数与步骤关联

下列 Gaussian route 按对应成功原生日志的回显记录；上表“输入”链接保留历史输入文件，不能在参数有差异时把它当成此次执行版本。完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束应连同原始日志回显核对。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

已核实的版本差异：`intg`、`ts6`、`reverse_min`、`pd0`、`h2` 的历史输入设置 MaxCycles=300 或 400，实际有效日志设置 MaxCycles=8；这些步骤都有 Optimization completed 和正常结束，并完成后续频率分析，不能把迭代上限写成实际迭代次数，也不能因上限为 8 就误判为未收敛。逐项比较 route 后，差异仅为这一迭代上限，理论方法、收敛阈值、溶剂及温度等关键词相同。

- `intg`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(Cartesian,CalcFC,Tight,MaxCycles=8) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `ts6`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(TS,CalcFC,NoEigenTest,Cartesian,Tight,MaxCycles=8) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `intg_sp`：`#p MN15/def2TZVP SCRF=(SMD,Solvent=N,N-DimethylAcetamide) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `ts6_sp`：`#p MN15/def2TZVP SCRF=(SMD,Solvent=N,N-DimethylAcetamide) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `forward`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ IRC=(LQA,CalcFC,Forward,MaxPoints=160,StepSize=5,VeryTight) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `reverse`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ IRC=(LQA,CalcFC,Reverse,MaxPoints=160,StepSize=5,VeryTight) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `forward_min`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=300,MaxStep=5) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `reverse_min`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=5) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `scan`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(ModRedundant,CalcFC,Tight,MaxCycles=300,MaxStep=5) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `pd0`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=3) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `h2`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=3) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `pd0_sp`：`#p MN15/def2TZVP SP SCRF=(SMD,Solvent=N,N-DimethylAcetamide) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `h2_sp`：`#p MN15/def2TZVP SP SCRF=(SMD,Solvent=N,N-DimethylAcetamide) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `release accepted extension`：`#p PBE1PBE/def2SVP EmpiricalDispersion=GD3BJ Opt=(ModRedundant,CalcFC,Tight,MaxCycles=300,MaxStep=5) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_process_minimum` | The submission validates the supplied neutral singlet INT-G as a stationary-point minimum and reports its imaginary-frequency count. | 77原子INT-G、0/1、225正频。 |
| 关键点 `kp_process_ts` | The submission validates a transition state for H2 reductive elimination and demonstrates endpoint connectivity. | TS唯一H–H虚频；双向IRC和真实端点；释放扫描、独立75/2原子片段证据。 |
| 关键点 `kp_result_barrier` | The submission reports the computed free-energy barrier for H2 reductive elimination from INT-G. | 0.764432041 kcal/mol，满足0.9±2.0；同几何复合G、共同INT-G零点。 |
| 结论 `c_final_barrier` | The computed terminal H2-elimination step has a very small free-energy barrier consistent with the authors' catalytic-cycle interpretation, within the stated model limitations. | 真实低势垒支持该终端H2消除步骤；不是整个催化周期验证。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_kp_minimum` | `$.stationary_point.minimum_n_imaginary, $.system.charge, $.system.multiplicity`；minimum_n_imaginary is 0 and system charge/multiplicity identify the supplied INT-G | `kp_process_minimum`：77原子INT-G、0/1、225正频。 |
| `r_kp_ts` | `$.stationary_point.ts_n_imaginary, $.connection_evidence.supports_both_endpoints`；ts_n_imaginary is 1 and connection_evidence supports both endpoints | `kp_process_ts`：TS唯一H–H虚频；双向IRC和真实端点；释放扫描、独立75/2原子片段证据。 |
| `r_barrier` | `$.barrier.value_kcal_mol`；0.9 ± 2.0 kcal/mol | `kp_result_barrier`：0.764432041 kcal/mol，满足0.9±2.0；同几何复合G、共同INT-G零点。 |
| `r_final` | `$.conclusion, $.limitations`；conclusion interprets the terminal barrier and states limitations | `c_final_barrier`：真实低势垒支持该终端H2消除步骤；不是整个催化周期验证。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

两模式的最低点、相关 TS、两侧连接证据和低势垒均有真实计算支持。结论严格为所给终端子步骤，不能冒充完整催化循环、脱氢总速率或实验产率。

本轮未改变当前较宽的数值容差或加入新产物热力学评分，也不修改公开结构。后续发布整理仍应检查任务指令、公开初始结构边界和泛化的 limitation 文句。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [TERMINAL_H2_STRICT_CLOSURE_20260923.md](../../../../docs/verification/group_4/paper_9132719dbf91c978/TERMINAL_H2_STRICT_CLOSURE_20260923.md)
- [evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_9132719dbf91c978/provenance/evaluation_task_qualification.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

SI p10方法、p12终端H2释放路线和坐标。

实际修复：保留完整INT-G已知反应物，要求自建TS；明确DMAc、298.15K/1atm以及INT-G共同零点；绑定success与真实势垒/驻点/连接，取消泛泛停止/局限要求。

验证适用性：结合H2中间体不等于分离H2，原档案已保存额外释放证据；不需要重算。方法路径是作者知情验证，不是AR搜索轨迹。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_process_minimum` | A defensible minimum validation is reported with charge 0, multiplicity 1 and no imaginary frequencies (or a clearly justified reoptimization result). | 14个有效步骤：INT-G/TS优化频率与MN15单点、双向IRC、端点和后续H2释放/分离片段。TS−478.5853，G势垒0.764432041 kcal/mol，符合0.9±2.0。 |
| `kp_process_ts` | One imaginary mode is reported for the TS and an IRC, mode-following, scan, or equivalent evidence supports both INT-G-side and H2/Pd(0)-side endpoints. | 14个有效步骤：INT-G/TS优化频率与MN15单点、双向IRC、端点和后续H2释放/分离片段。TS−478.5853，G势垒0.764432041 kcal/mol，符合0.9±2.0。 |
| `kp_result_barrier` | The reported barrier is approximately 0.9 kcal/mol within the stated comparison tolerance, with units and reference state explicit. | 14个有效步骤：INT-G/TS优化频率与MN15单点、双向IRC、端点和后续H2释放/分离片段。TS−478.5853，G势垒0.764432041 kcal/mol，符合0.9±2.0。 |
| `c_final_barrier` | Real minimum, H2-elimination saddle and connection evidence support a very small terminal barrier and corresponding regeneration-step interpretation. | 14个有效步骤：INT-G/TS优化频率与MN15单点、双向IRC、端点和后续H2释放/分离片段。TS−478.5853，G势垒0.764432041 kcal/mol，符合0.9±2.0。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_kp_minimum` → `kp_process_minimum`；读取 `$.stationary_point.minimum_n_imaginary, $.system.charge, $.system.multiplicity`。
- `r_kp_ts` → `kp_process_ts`；读取 `$.stationary_point, $.connection_evidence, $.investigation`。
- `r_barrier` → `kp_result_barrier`；读取 `$.barrier.value_kcal_mol`。
- `r_final` → `c_final_barrier`；读取 `$.conclusion, $.barrier, $.method, $.connection_evidence`。

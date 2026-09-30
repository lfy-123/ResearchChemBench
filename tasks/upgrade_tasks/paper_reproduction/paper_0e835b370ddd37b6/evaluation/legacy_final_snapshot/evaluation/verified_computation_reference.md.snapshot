# 已验证成功计算过程：paper_0e835b370ddd37b6 / paper_reproduction

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 4；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_4.md)
- [正文](../../../../papers/paper_0e835b370ddd37b6/documents/main.pdf)；[补充材料](../../../../papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/author_h2_closure_20260925/result.json)；[历史结构化结果](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_paper_reproduction/paper_0e835b370ddd37b6/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_paper_reproduction/paper_0e835b370ddd37b6/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

只比较 silylene 1 与 V′ 的 H2 活化。当前公共1已按来源修复为55原子，V′36原子；均中性 singlet，另有 H2。TS/产物加上 H2 后分别57/38原子。正文 pp3–5、Table2 以及 SI 坐标和 TableS12 为依据；不计算其余 silylene、乙炔或氨硼烷子题。

真实 Gaussian16 C.01，PBE0/PBE1PBE-D3BJ/def2-TZVP，SMD(benzene)，298 K、1 atm，UltraFine、NoSymm。源文为 Gaussian09；当前任务容許明确披露的模型选择。本次以真实输入中的温度298 K记录，不自动写成298.15 K。

## 3. 成功计算链与结果

两反应物和H2独立 Opt/Freq → 两条作者标签 H–H 活化 TS 独立 Opt/Freq → H–H 虚频投影 → 各 TS 双向 IRC → 四个实际 IRC 端点分别 Opt/Freq → 两反应物终态波函数 Stable → 同一分离反应物零点计算势垒。另分别优化源产品结构用于反应能；不能把该结构代替真实 IRC 端点来声称连接性。

1/V′最低点分别159/102正频，H2一个正频；TS分别165/108模中唯一 −1243.4664/−1328.1352 cm⁻¹；四个直接端点全实频。两反向 IRC 达到160点上限，再由自由优化得到具有完整 H2 的前体端点；未声称仅靠 IRC 的终止文字证明最低点。

| 量，kcal/mol | 1 实算 | V′ 实算 | 正文 1 / V′ |
|---|---:|---:|---|
| 分离 silylene+H2→TS 的 ΔG‡ | 33.065984223 | 47.132236592 | 32.9 / 47.4 |
| 源产品相对分离反应物 ΔG | −29.098869328 | −20.574780634 | −29.4 / −21.3 |

公式：`[GTS−Gsilylene−GH2]×627.509474`，不是相遇复合物作零点。势垒相差14.066252369 kcal/mol，支持1更易活化H2。当前 evaluator 是同尺度的 expert comparison，没有凭空添加 numeric 容差。

17 个完整步骤 elapsed 合计108.1703 h，原生日志 CPU 合计2107.0105 h，不是并行日历工期。早期错误61原子对象、PBE0DH及无效优化分支不属于有效主链。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| 1 Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/completed_followups_20260915/silylene_1_source_recalcfc_optfreq_exacthessian_20260922/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log) | -1628.19648795 / -1627.784758 | 159 模；负模 无；最低正频 9.8946 cm⁻¹；日志正常结束 |
| Vprime Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | -1055.7523748 / -1055.510565 | 102 模；负模 无；最低正频 21.0877 cm⁻¹；日志正常结束 |
| H2 Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/h2_full_si_pbe1pbe_optfreq_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log) | -1.16787757403 / -1.169328 | 1 模；负模 无；最低正频 4406.4137 cm⁻¹；日志正常结束 |
| TS1 Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | -1629.32660215 / -1628.901392 | 165 模；负模 [-1243.4664]；最低正频 28.2981 cm⁻¹；日志正常结束 |
| TSVprime Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | -1056.85995349 / -1056.604783 | 108 模；负模 [-1328.1352]；最低正频 21.2836 cm⁻¹；日志正常结束 |
| P1 Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | -1629.43008686 / -1629.000458 | 165 模；负模 无；最低正频 31.7962 cm⁻¹；日志正常结束 |
| PVprime Opt/Freq | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log) | -1056.9714741 / -1056.712681 | 108 模；负模 无；最低正频 20.2353 cm⁻¹；日志正常结束 |
| 1 forward irc | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_irc_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log) | -1629.42972524 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| 1 forward endpoint | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_endpoint_optfreq_20260921/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_endpoint_optfreq_20260921/stdout.log) | -1629.42982802 / -1628.999358 | 165 模；负模 无；最低正频 29.7732 cm⁻¹；日志正常结束 |
| 1 reverse irc | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_irc_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log) | -1629.36494847 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| 1 reverse endpoint | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_endpoint_optfreq_20260921/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_endpoint_optfreq_20260921_hpc20_p6/stdout.log) | -1629.36630024 / -1628.946935 | 165 模；负模 无；最低正频 23.772 cm⁻¹；日志正常结束 |
| Vprime forward irc | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_irc_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log) | -1056.97130802 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| Vprime forward endpoint | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_endpoint_optfreq_20260921/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_forward_endpoint_optfreq_20260921_hpc20_p6/stdout.log) | -1056.9714709 / -1056.71276 | 108 模；负模 无；最低正频 19.8858 cm⁻¹；日志正常结束 |
| Vprime reverse irc | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_irc_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log) | -1056.91626204 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| Vprime reverse endpoint | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_endpoint_optfreq_20260921/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_reverse_endpoint_optfreq_20260921_hpc20_p6/stdout.log) | -1056.92260484 / -1056.673014 | 108 模；负模 无；最低正频 18.2946 cm⁻¹；日志正常结束 |
| 1 Stable | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/completed_followups_20260915/silylene_1_exacthessian_parent_wf_stability_20260925/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_exacthessian_parent_wf_stability_20260925_hpc20_p6/stdout.log) | -1628.19648795 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| Vprime Stable | [输入](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/recovery27_20260915/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_wf_stability_20260915/input.com) / [输出](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918_computed_parent_wf_stability_20260915/stdout.log) | -1055.7523748 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |

### 输入参数与步骤关联

下列 Gaussian route 按对应成功原生日志的回显记录；上表“输入”链接保留历史输入文件，不能在参数有差异时把它当成此次执行版本。完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束应连同原始日志回显核对。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

已核实的版本差异：`Vprime Opt/Freq`、`H2 Opt/Freq`、`TS1 Opt/Freq`、`TSVprime Opt/Freq`、`P1 Opt/Freq`、`1 forward endpoint` 的历史输入设置 MaxCycles=300 或 400，实际有效日志设置 MaxCycles=8；这些步骤都有 Optimization completed 和正常结束，并完成后续频率分析，不能把迭代上限写成实际迭代次数，也不能因上限为 8 就误判为未收敛。逐项比较 route 后，差异仅为这一迭代上限，理论方法、收敛阈值、溶剂及温度等关键词相同。

- `1 Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(CalcAll,Tight,MaxCycles=400,MaxStep=1) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `Vprime Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=5) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `H2 Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(Cartesian,CalcFC,Tight,MaxCycles=8) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `TS1 Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(TS,CalcFC,NoEigenTest,Tight,MaxCycles=8,MaxStep=5) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `TSVprime Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(TS,CalcFC,NoEigenTest,Tight,MaxCycles=8,MaxStep=5) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `P1 Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=5) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `PVprime Opt/Freq`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=400,MaxStep=5) Freq SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512) Temperature=298`。
- `1 forward irc`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 IRC=(LQA,CalcFC,Forward,MaxPoints=160,StepSize=5,VeryTight) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `1 forward endpoint`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=3) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `1 reverse irc`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 IRC=(LQA,CalcFC,Reverse,MaxPoints=160,StepSize=5,VeryTight) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `1 reverse endpoint`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 Opt=(CalcFC,Tight,MaxCycles=400,MaxStep=3) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `Vprime forward irc`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 IRC=(LQA,CalcFC,Forward,MaxPoints=160,StepSize=5,VeryTight) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `Vprime forward endpoint`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 Opt=(CalcFC,Tight,MaxCycles=400,MaxStep=3) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `Vprime reverse irc`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 IRC=(LQA,CalcFC,Reverse,MaxPoints=160,StepSize=5,VeryTight) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `Vprime reverse endpoint`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ SCRF=(SMD,Solvent=Benzene) Temperature=298 Opt=(CalcFC,Tight,MaxCycles=400,MaxStep=3) Freq NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `1 Stable`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Stable SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。
- `Vprime Stable`：`#p PBE1PBE/def2TZVP EmpiricalDispersion=GD3BJ Stable SCRF=(SMD,Solvent=Benzene) NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512)`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_minima` | Both named reactants are optimized minima with zero imaginary frequencies. | 1/V′的55/36原子0/1最低点分别159/102正频。 |
| 关键点 `kp_ts` | Each named system has a reported H2 activation TS with exactly one H-H-cleavage imaginary mode and endpoint connectivity evidence. | 两个唯一H–H虚频、四条实际IRC及四个直接端点全实频。 |
| 关键点 `kp_barriers` | Comparable H-H activation barriers are reported for both systems in kcal/mol. | 同分离反应物零点33.065984223/47.132236592 kcal/mol。 |
| 结论 `c_final` | Validated calculations support a model-bounded relative H2 activation conclusion, or explicitly report unresolved bounded failure. | 1比V′低14.066252369 kcal/mol，两个反应G负；支持当前相对活化结论。 |
| 结论 `c_limit` | Interpretation is limited by TS search coverage and computational model choice. | 现有结果说明一个来源通道/系统、方法与软件版本边界，不伪造全局搜索。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_minima` | `$.systems[*].minimum`；for every system, when outcome_status is validated_success, optimized=true and imaginary_frequencies=0 with evidence; a bounded_failure system must still identify the minimum-search outcome truthfully in its minimum object | `kp_minima`：1/V′的55/36原子0/1最低点分别159/102正频。 |
| `r_ts` | `$.systems[*].ts_search`；for every system, candidates_attempted, candidates_validated, coverage and evidence document the H2-activation search; validated_success requires a one-imaginary-frequency H-H-cleavage TS and endpoint evidence, while bounded_failure requires the attempted coverage and explicit failure reason | `kp_ts`：两个唯一H–H虚频、四条实际IRC及四个直接端点全实频。 |
| `r_barriers` | `$.systems[*].barrier`；validated_success systems report a kcal/mol barrier computed from separated silylene + H2 reactants to the validated H-H-activation TS; bounded_failure systems report null and an explicit failure reason. When both systems succeed, compare the two barriers on the same stated model and preserve each named system identity | `kp_barriers`：同分离反应物零点33.065984223/47.132236592 kcal/mol。 |
| `r_final` | `$.conclusion`；supported relative conclusion or honest unresolved outcome | `c_final`：1比V′低14.066252369 kcal/mol，两个反应G负；支持当前相对活化结论。 |
| `r_limit` | `$.limitations`；limitations state search coverage and model dependence | `c_limit`：现有结果说明一个来源通道/系统、方法与软件版本边界，不伪造全局搜索。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

两模式科学关键点和相对活化结论得到支持；来源辅助 TS 种子不否定可计算性，也不代表已经做过公开输入盲搜索。反应物、TS、路径、真正端点各有独立证据。

本轮不扩展候选数、不放宽评分、不新增实验或计算；源包仍有 limitation 独立计分与一般停止条款，留待后续规范化，不能把本次入库等同于发布验收。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [AUTHOR_H2_STRICT_CLOSURE_20260925.md](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/AUTHOR_H2_STRICT_CLOSURE_20260925.md)
- [evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/evaluation_task_qualification.json)
- [result.json](../../../../docs/verification/group_4/paper_0e835b370ddd37b6/provenance/public_input_repair_20260925/result.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

正文pp3–5方法/Table2与SI相应H2活化通道。

实际修复：保留两个完整已知silylene+H2反应物，无作者TS；明确苯/298K/1atm、分离反应物零点；绑定1/V-prime唯一对象，完成须两套真实TS/路径/势垒。私有结论明确1势垒低于V′，不公开排序，不增加数值硬靶；删c_limit/两轮停止规则。

验证适用性：未完成分支仅提交实际已算部分，不得作为完整排序成果；合法额外尝试不影响主结果。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_minima` | minimum validation for 1 and V-prime | 17个有效步骤覆盖两个最低点、H2、两TS、IRC/四端点、稳定性；势垒33.065984223/47.132236592 kcal/mol，方向符合正文32.9/47.4。 |
| `kp_ts` | one validated TS per system | 17个有效步骤覆盖两个最低点、H2、两TS、IRC/四端点、稳定性；势垒33.065984223/47.132236592 kcal/mol，方向符合正文32.9/47.4。 |
| `kp_barriers` | two comparable barriers | 17个有效步骤覆盖两个最低点、H2、两TS、IRC/四端点、稳定性；势垒33.065984223/47.132236592 kcal/mol，方向符合正文32.9/47.4。 |
| `c_final` | Validated H–H activation barriers from separated reactants are lower for silylene 1 than for V-prime. The comparison must be supported by the two corresponding TSs and a common method/Gibbs convention. | 17个有效步骤覆盖两个最低点、H2、两TS、IRC/四端点、稳定性；势垒33.065984223/47.132236592 kcal/mol，方向符合正文32.9/47.4。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_minima` → `kp_minima`；读取 `$.systems[*].minimum`。
- `r_ts` → `kp_ts`；读取 `$.systems[*].ts_search`。
- `r_barriers` → `kp_barriers`；读取 `$.systems, $.method`。
- `r_final` → `c_final`；读取 `$.systems, $.comparison, $.conclusion, $.method`。

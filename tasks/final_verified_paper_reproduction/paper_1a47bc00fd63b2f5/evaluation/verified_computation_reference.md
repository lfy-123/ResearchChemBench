# 已验证成功计算过程：paper_1a47bc00fd63b2f5 / paper_reproduction

归档日期：2026-09-26。原有效计算链保留；2026-09-27主定量协议明确后的适用性见第8节，较早对应快照见第7节。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 3；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_3.md)
- [正文](../../../../papers/paper_1a47bc00fd63b2f5/documents/main.pdf)；[补充材料](../../../../papers/paper_1a47bc00fd63b2f5/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/closeout_20260925/final_channel_audit.json)；[历史结构化结果](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_paper_reproduction/paper_1a47bc00fd63b2f5/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_paper_reproduction/paper_1a47bc00fd63b2f5/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

本论文当前只有 PR 包。目标为中性 singlet、54 原子、底物1a与一当量 bis(4-nitrophenyl) phosphate 的第一步 C–C 环化，两通道对应 ortho/4-hydroxybenzofuran 与 para/6-hydroxybenzofuran。公开任务以 SMILES 定义身份，验证允许利用作者 SI 的构象/TS 作为起点；两者不要求搜索轨迹相同。

SI PDF p59 方法：Gaussian16，B3LYP-D3/6-31+G(d)、UltraFine、SMD(toluene)、298.15 K 优化/频率；同几何 B3LYP-D3/6-311+G(d,p) 单点。D3 用 GD3 零阻尼，不使用旧 GD3BJ 分支。G 由 `Ehigh + Gcorr_low` 构成。p60 Fig.S3、p61 TableS5 和相应坐标提供路线/能量依据。

## 3. 成功计算链与结果

SI 身份与构型核对 → INT1、TS1、TS1′ 同层级 Opt/Freq → 同几何高层 SP → 两 TS 的实际双向 IRC 已接受前缀 → 从其真实终点继续无约束优化 → 必要的真实软模位移后再优化/频率 → 四个对应最低点及通道原子映射 → 共同 INT1 能量账本。另有一个 ortho 前体正向软模扰动最低点用作敏感性，不冒充新通道。

两 TS 各有 156 模和唯一相关虚频 −267.4872/−285.8447 cm⁻¹；共同 INT1 及四个主端点均 156 正频。形成键在各自源原子序中为 C5–C10；由 OH 与成键位点的环图距离 1/3 区分 ortho/para，不仅凭文件名。

| 项目 | 实算 kcal/mol | 来源/评分参考 |
|---|---:|---|
| INT1→TS1 | 19.355178322 | Fig.S3：13.9−(−5.4)=19.3 |
| INT1→TS1′ | 26.883378107 | Fig.S3：21.5−(−5.4)=26.9 |
| para−ortho | +7.528199785 | evaluator +7.6±1.5；SI 表按反向减法为 −7.53 |

有效路径前缀为 ortho 100/12、para 100/100 个非零点。12 点反向 IRC 在后续 corrector 失败；只使用已接受点，再从对应坐标做完整自由优化。这里采用任务明确允许的“IRC 或科学等价路径”证据，不宣称所有 IRC 已达到终端最低点。Berny 松弛有最高约 4.280 kcal/mol 的试探上坡；已记录求值点都在相应 TS 以下，不能进一步宣称连续严格单调下降。

ortho 端点曾有软负模，最终通过真实的 0.05 Å 模位移及新 Opt/Freq 得到全实频；不是人工删除负频。必要父结构/位移/自由优化传承见后面的专门链接。共同能量零点 INT1 不代表两反向 IRC 必须到同一个构象：SI 区分 INT1 与 INT1′；未计算其互变势垒，不编造相同盆地。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| INT1 Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260914/INT1_author_GD3_optfreq_20260914/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/INT1_author_GD3_optfreq_20260914/20260914T121646553885Z_hpc-job-1931178-cluster-slurmd-0/gaussian.log) | -2090.05305151 / -2089.730484 | 156 模；负模 无；最低正频 11.9401 cm⁻¹；日志正常结束 |
| TS1 Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260914/TS1_author_GD3_optfreq_20260914/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_author_GD3_optfreq_20260914/20260914T121646550333Z_hpc-job-1931184-cluster-slurmd-0/gaussian.log) | -2090.02644451 / -2089.700787 | 156 模；负模 [-267.4872]；最低正频 8.574 cm⁻¹；日志正常结束 |
| TS1_prime Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260914/TS1_prime_author_GD3_optfreq_20260914/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_prime_author_GD3_optfreq_20260914/20260914T121646549249Z_hpc-job-1931190-cluster-slurmd-0/gaussian.log) | -2090.01194017 / -2089.689031 | 156 模；负模 [-285.8447]；最低正频 6.9131 cm⁻¹；日志正常结束 |
| INT1 high-level SP | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/INT1_author_GD3_6311pgdp_sp_20260915/local_gradient_probe/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/INT1_author_GD3_6311pgdp_sp_20260915/local_gradient_probe/gaussian.log) | -2090.5158802 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| TS1 high-level SP | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_author_GD3_6311pgdp_sp_20260915/local_gradient_probe/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_author_GD3_6311pgdp_sp_20260915/local_gradient_probe/gaussian.log) | -2090.48812676 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| TS1_prime high-level SP | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_prime_author_GD3_6311pgdp_sp_20260915/local_gradient_probe/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_prime_author_GD3_6311pgdp_sp_20260915/local_gradient_probe/gaussian.log) | -2090.47338081 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| ortho_forward accepted IRC prefix | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_author_GD3_RCFC_v2_irc_20260915/20260915T071350845813Z_hpc-job-2000133-cluster-slurmd-0/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_author_GD3_RCFC_v2_irc_20260915/20260915T071350845813Z_hpc-job-2000133-cluster-slurmd-0/gaussian.log) | 前缀范围见说明；不取失败尾部数值 | 仅作已接受路径/扫描几何证据；不采用失败尾部的频率/热化学；日志正常结束；只使用 100 个已接受非零路径点；完整收敛性按原日志披露，后续连接自由优化最低点。 |
| ortho_reverse accepted IRC prefix | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_author_GD3_REVERSE_Tight_defaultStep10_IRC_20260916/20260918T035127781180Z_hpc-job-2074449-cluster-slurmd-0/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_author_GD3_REVERSE_Tight_defaultStep10_IRC_20260916/20260918T035127781180Z_hpc-job-2074449-cluster-slurmd-0/gaussian.log) | 前缀范围见说明；不取失败尾部数值 | 仅作已接受路径/扫描几何证据；不采用失败尾部的频率/热化学；整日志非正常终止，仅采用已接受前缀；只使用 12 个已接受非零路径点；完整收敛性按原日志披露，后续连接自由优化最低点。 |
| para_forward accepted IRC prefix | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_prime_author_GD3_RCFC_v2_irc_20260915/20260915T071333486920Z_hpc-job-2000136-cluster-slurmd-0/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_prime_author_GD3_RCFC_v2_irc_20260915/20260915T071333486920Z_hpc-job-2000136-cluster-slurmd-0/gaussian.log) | 前缀范围见说明；不取失败尾部数值 | 仅作已接受路径/扫描几何证据；不采用失败尾部的频率/热化学；日志正常结束；只使用 100 个已接受非零路径点；完整收敛性按原日志披露，后续连接自由优化最低点。 |
| para_reverse accepted IRC prefix | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_prime_author_GD3_RCFC_v2_irc_20260915/20260915T071333486920Z_hpc-job-2000136-cluster-slurmd-0/input.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_prime_author_GD3_RCFC_v2_irc_20260915/20260915T071333486920Z_hpc-job-2000136-cluster-slurmd-0/gaussian.log) | 前缀范围见说明；不取失败尾部数值 | 仅作已接受路径/扫描几何证据；不采用失败尾部的频率/热化学；日志正常结束；只使用 100 个已接受非零路径点；完整收敛性按原日志披露，后续连接自由优化最低点。 |
| ortho_precursor_minus endpoint Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_reverse_softmode_minus_005A_authorPES_20260925/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_reverse_softmode_minus_005A_authorPES_20260925/20260925T025938618869Z_hpc-job-2216127-cluster-slurmd-0/gaussian.log) | -2090.05303374 / -2089.732814 | 156 模；负模 无；最低正频 5.9782 cm⁻¹；日志正常结束 |
| ortho_precursor_plus endpoint Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_reverse_softmode_plus_005A_authorPES_20260925/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_reverse_softmode_plus_005A_authorPES_20260925/20260925T025939183006Z_hpc-job-2216130-cluster-slurmd-0/gaussian.log) | -2090.05303213 / -2089.733051 | 156 模；负模 无；最低正频 5.2911 cm⁻¹；日志正常结束 |
| ortho_product endpoint Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1_FORWARD_actual_softmode_minus_005A_samePES_optfreq_20260918/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_FORWARD_actual_softmode_minus_005A_samePES_optfreq_20260918/20260918T082632064188Z_hpc-job-2083473-cluster-slurmd-0/gaussian.log) | -2090.03716809 / -2089.710921 | 156 模；负模 无；最低正频 6.5086 cm⁻¹；日志正常结束 |
| para_precursor endpoint Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1prime_FORWARD_actual_IRC_endpoint_optfreq_20260916/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1prime_FORWARD_actual_IRC_endpoint_optfreq_20260916/20260916T061703074407Z_hpc-job-2030397-cluster-slurmd-0/gaussian.log) | -2090.04487245 / -2089.725057 | 156 模；负模 无；最低正频 9.1457 cm⁻¹；日志正常结束 |
| para_product endpoint Opt/Freq | [输入](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/repair_20260915/TS1prime_REVERSE_actual_IRC_endpoint_optfreq_20260916/production.com) / [输出](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1prime_REVERSE_actual_IRC_endpoint_optfreq_20260916/20260916T061701998489Z_hpc-job-2030727-cluster-slurmd-0/gaussian.log) | -2090.02753884 / -2089.701028 | 156 模；负模 无；最低正频 7.0348 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `INT1 Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 Opt=(CalcFC,MaxStep=5,MaxCycles=256) Freq Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `TS1 Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 Opt=(TS,CalcFC,NoEigenTest,MaxStep=5,MaxCycles=256) Freq Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `TS1_prime Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 Opt=(TS,CalcFC,NoEigenTest,MaxStep=5,MaxCycles=256) Freq Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `INT1 high-level SP`：`#p B3LYP/6-311+G(d,p) EmpiricalDispersion=GD3 SP Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `TS1 high-level SP`：`#p B3LYP/6-311+G(d,p) EmpiricalDispersion=GD3 SP Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `TS1_prime high-level SP`：`#p B3LYP/6-311+G(d,p) EmpiricalDispersion=GD3 SP Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `ortho_forward accepted IRC prefix`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 IRC=(RCFC,MaxPoints=100,StepSize=2,MaxCycles=300) Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `ortho_reverse accepted IRC prefix`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 IRC=(RCFC,Reverse,Tight,MaxPoints=100,StepSize=10,MaxCycles=300) Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `para_forward accepted IRC prefix`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 IRC=(RCFC,MaxPoints=100,StepSize=2,MaxCycles=300) Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `para_reverse accepted IRC prefix`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 IRC=(RCFC,MaxPoints=100,StepSize=2,MaxCycles=300) Geom=AllCheck Guess=Read Int=UltraFine SCRF=(SMD,Solvent=Toluene) NoSymm SCF=(XQC,MaxCycle=512)`。
- `ortho_precursor_minus endpoint Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 Opt=(Redundant,Tight,RCFC,MaxStep=3,MaxCycles=256) Freq Guess=Read Int=UltraFine NoSymm SCRF=(SMD,Solvent=Toluene) SCF=(XQC,Conver=10)`。
- `ortho_precursor_plus endpoint Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 Opt=(Redundant,Tight,RCFC,MaxStep=3,MaxCycles=256) Freq Guess=Read Int=UltraFine NoSymm SCRF=(SMD,Solvent=Toluene) SCF=(XQC,Conver=10)`。
- `ortho_product endpoint Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 SCRF=(SMD,Solvent=Toluene) Opt=(Tight,CalcFC,MaxStep=5,MaxCycles=256) Freq Int=UltraFine NoSymm SCF=(XQC,MaxCycle=512) Guess=Read`。
- `para_precursor endpoint Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 SCRF=(SMD,Solvent=Toluene) Opt=(CalcFC,MaxStep=5,MaxCycles=256) Freq Int=UltraFine NoSymm SCF=(XQC,MaxCycle=512)`。
- `para_product endpoint Opt/Freq`：`#p B3LYP/6-31+G(d) EmpiricalDispersion=GD3 SCRF=(SMD,Solvent=Toluene) Opt=(CalcFC,MaxStep=5,MaxCycles=256) Freq Int=UltraFine NoSymm SCF=(XQC,MaxCycle=512)`。

### IRC 到端点的必要有效传承

只列最终采用的几何传承；含软负模的中间结构仅作已计算的路径/位移父结构，不能当最低点。它们不是额外“通过”的端点。无关失败/重试不展开。

| 通道/方向 | 实际后继结构链 |
|---|---|
| ortho_forward | [TS1_FORWARD_actual_IRC_endpoint_optfreq_20260915](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_FORWARD_actual_IRC_endpoint_optfreq_20260915/20260916T044308372733Z_hpc-job-2023101-cluster-slurmd-0/gaussian.log)（软模父结构，不计最低点） → [TS1_FORWARD_samePES_Tight_endpoint_softmode_repair_20260916](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_FORWARD_samePES_Tight_endpoint_softmode_repair_20260916/20260916T162919767163Z_hpc-job-2051703-cluster-slurmd-0/gaussian.log)（软模父结构，不计最低点） → [TS1_FORWARD_actual_softmode_minus_005A_samePES_optfreq_20260918](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_FORWARD_actual_softmode_minus_005A_samePES_optfreq_20260918/20260918T082632064188Z_hpc-job-2083473-cluster-slurmd-0/gaussian.log)（全实频最低点） |
| ortho_reverse | [TS1_GD3_reverse_actual_IRC_accepted12_endpoint_20260923](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_GD3_reverse_actual_IRC_accepted12_endpoint_20260923/20260923T123354661493Z_hpc-job-2202081-cluster-slurmd-0/gaussian.log)（软模父结构，不计最低点） → [TS1_reverse_softmode_minus_005A_authorPES_20260925](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1_reverse_softmode_minus_005A_authorPES_20260925/20260925T025938618869Z_hpc-job-2216127-cluster-slurmd-0/gaussian.log)（全实频最低点） |
| para_forward | [TS1prime_FORWARD_actual_IRC_endpoint_optfreq_20260916](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1prime_FORWARD_actual_IRC_endpoint_optfreq_20260916/20260916T061703074407Z_hpc-job-2030397-cluster-slurmd-0/gaussian.log)（全实频最低点） |
| para_reverse | [TS1prime_REVERSE_actual_IRC_endpoint_optfreq_20260916](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/qzcli_hpc/TS1prime_REVERSE_actual_IRC_endpoint_optfreq_20260916/20260916T061701998489Z_hpc-job-2030727-cluster-slurmd-0/gaussian.log)（全实频最低点） |

### 同几何复合能账本

| 状态 | Ehigh，Eh | Gcorr_low，Eh | 复合G，Eh |
|---|---:|---:|---:|
| INT1 | -2090.5158802 | 0.322567 | -2090.1933132 |
| TS1 | -2090.48812676 | 0.325658 | -2090.1624687599997 |
| TS1_prime | -2090.47338081 | 0.322909 | -2090.15047181 |

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_process_stationary` | Reported stationary points are classified using harmonic frequencies, with minima having no imaginary modes and transition structures having one relevant imaginary mode. | 两TS各唯一相关虚频，INT1和四主端点全实频；软模问题经实际优化修复。 |
| 关键点 `kp_process_irc` | Each reported cyclization transition structure is connected by IRC or equivalent path-following evidence to the intended precursor and post-cyclization minimum. | 各通道实际IRC前缀、后继自由优化及原子/氢映射构成任务允许的等价路径；不声称IRC全部终端收敛。 |
| 关键点 `kp_result_order` | The productive ortho/4-hydroxybenzofuran cyclization transition state is lower than the competing para/6-hydroxybenzofuran transition state on the authors' model. | 同一INT1零点，ortho19.355178 < para26.883378 kcal/mol。 |
| 关键点 `kp_result_delta` | The authors report a signed barrier difference of +7.6 kcal/mol for the para transition state relative to the ortho transition state. | para−ortho=7.528199785，满足7.6±1.5。 |
| 结论 `c_final_kinetic` | The validated barrier ordering supports kinetic control favoring the ortho/4-hydroxybenzofuran channel and is consistent with the observed strong regioselectivity within the defined model boundary. | 验证第一环化两通道的动力学ortho偏好；不涉及后续脱水或所有机理。 |
| 结论 `c_limitation` | The conclusion is bounded by the implicit-solvent DFT model, conformer coverage and transition-state validation actually performed. | 原结果披露路径/构象及实现范围；档案不增加新的limitation评分。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_process_stationary` | `$.candidates`；frequency classifications and candidate-specific validation evidence are reported | `kp_process_stationary`：两TS各唯一相关虚频，INT1和四主端点全实频；软模问题经实际优化修复。 |
| `r_process_irc` | `$.candidates`；IRC or equivalent connectivity evidence is supplied separately for the reported candidates/channels | `kp_process_irc`：各通道实际IRC前缀、后继自由优化及原子/氢映射构成任务允许的等价路径；不声称IRC全部终端收敛。 |
| `r_order` | `$.barrier_comparison`；ortho_4_hydroxybenzofuran lower than para_6_hydroxybenzofuran when status is completed | `kp_result_order`：同一INT1零点，ortho19.355178 < para26.883378 kcal/mol。 |
| `r_delta` | `$.barrier_comparison.signed_delta_delta_g_kcal_mol`；7.6 ± 1.5 kcal/mol | `kp_result_delta`：para−ortho=7.528199785，满足7.6±1.5。 |
| `r_final` | `$.conclusion.claim`；barrier ordering supports kinetic ortho selectivity within the defined scope when status is completed; bounded failure instead states the conclusion is limited | `c_final_kinetic`：验证第一环化两通道的动力学ortho偏好；不涉及后续脱水或所有机理。 |
| `r_limitation` | `$.conclusion.limitations`；specific method, conformer coverage and validation limitations are disclosed | `c_limitation`：原结果披露路径/构象及实现范围；档案不增加新的limitation评分。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

作者第一环化子路线可算，得到当前关键数值与结论；不扩张到后续脱水、完整催化循环或产率。保持当前 PR，不补造不存在的 AR 包。

公开文字“common catalyst-bound precursor”容易被误读为两个 IRC 的同一几何终点；有效证据实际是共同 INT1 能量参照，前体构象可不同。建议后续整理清晰区分这两层含义，不改现有比较目标。历史真计算支持任务允许的等价路径条款；本轮只归档，未做任何新计算或删改历史失败记录。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [verification_report.md](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/verification_report.md)
- [acceptance_mapping.json](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/closeout_20260925/acceptance_mapping.json)
- [path_inheritance_audit.json](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/closeout_20260925/path_inheritance_audit.json)
- [formal_result_sync.json](../../../../docs/verification/group_3/paper_1a47bc00fd63b2f5/provenance/closeout_20260925/formal_result_sync.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

正文pp1,4；SI p59方法、p60 Fig.S3、p61 TableS5。

实际修复：更正ortho/para相对于游离酚OH，而不是醚氧；两攻击碳相对醚连接位都是邻位。保留解释已知实验选择性的任务角色。明确同一G零点不要求两条反向IRC到完全相同前驱构象；完成分支覆盖两通道，早期失败允许没有未算出的频率/IRC。删除c_limitation。

验证适用性：不把IRC步数上限前缀当已收敛端点；后继真实OptFreq补全。只处理存在的PR，不补造AR；公开实验方向用于解释，不是未知选择性盲测。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_process_stationary` | The submission provides frequency evidence and assigns stationary-point character consistently for each reported candidate. | 15份原生日志及有效IRC前缀→真实自由优化端点；TS虚频−267.4872/−285.8447，势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，符合7.6±1.5。 |
| `kp_process_irc` | Both regiochannel TS candidates have channel-specific IRC or equivalent path-following evidence. Credit only connections actually established; a failure record is not evidence of the missing connection. | 15份原生日志及有效IRC前缀→真实自由优化端点；TS虚频−267.4872/−285.8447，势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，符合7.6±1.5。 |
| `kp_result_order` | A traceable common-reference Gibbs comparison of the two validated channels places ortho below para. Failure disclosure cannot substitute for an uncomputed ordering. | 15份原生日志及有效IRC前缀→真实自由优化端点；TS虚频−267.4872/−285.8447，势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，符合7.6±1.5。 |
| `kp_result_delta` | 7.6 | 15份原生日志及有效IRC前缀→真实自由优化端点；TS虚频−267.4872/−285.8447，势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，符合7.6±1.5。 |
| `c_final_kinetic` | Two validated first-cyclization channels give lower ortho than para barrier on the same reference and support the observed regioselectivity. The experimental input alone is not computational evidence. | 15份原生日志及有效IRC前缀→真实自由优化端点；TS虚频−267.4872/−285.8447，势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，符合7.6±1.5。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_process_stationary` → `kp_process_stationary`；读取 `$.candidates`。
- `r_process_irc` → `kp_process_irc`；读取 `$.candidates`。
- `r_order` → `kp_result_order`；读取 `$.barrier_comparison, $.system.method, $.candidates`（2026-09-27统一主协议，见第8节）。
- `r_delta` → `kp_result_delta`；读取 `$.barrier_comparison.signed_delta_delta_g_kcal_mol, $.system.method, $.candidates`。
- `r_final` → `c_final_kinetic`；读取 `$.conclusion.claim, $.candidates, $.barrier_comparison, $.system`。

## 8. 2026-09-27 主定量协议与评分适用范围统一

正文机理比较、SI PDF p59 Section 9和p61 Table S5再次核对：作者主方法为B3LYP-D3/6-31+G(d) Opt/Freq、B3LYP-D3/6-311+G(d,p)同几何SP、UltraFine、SMD(toluene)。Table S5还有不同方法控制；换成任务para−ortho符号后B3LYP、BLYP、HF为5.95、5.19、5.62 kcal/mol，不能统一套用主方法7.6±1.5。

现已按获准修法在PR题面明确主协议，并写清与实际验证一致的任务实现口径：GD3零阻尼、298.15K/1atm、未缩放harmonic修正，`G = Ehigh + (Glow - Elow)`，不重复加ZPE。部分默认细节是为基准明确约定，未声称SI逐字披露了全部默认值。额外方法允许控制但与主candidates/barrier_comparison分开；不提供TS结构或答案。

已重读第3节三个主Opt/Freq及三个SP的真实输入/日志，确认GD3、UltraFine、两层基组、SMD(toluene)、正常终止及能量账本；原19.355178322/26.883378107与差7.528199785 kcal/mol未变。历史 `system.method` 已具备修后成功分支所需的 optimization/single_point/solvent/temperature_K/pressure_atm/energy_convention，结果无需补造即可通过提交契约；因此这次明确协议不引入新的验证计算缺口。

`r_delta`保留7.6±1.5和原ID，绑定主差值、`$.system.method`及`$.candidates`；r_order/r_final同步主协议及控制计算的评判职责。评分须检查真实输入/输出和能量账本，不能凭方法标签或相近数值放行，也不对额外控制套用主参考。4个关键点、1个科学结论及权重不变；原始15步骤、IRC有效前缀/后继端点和历史验证文件未修改。

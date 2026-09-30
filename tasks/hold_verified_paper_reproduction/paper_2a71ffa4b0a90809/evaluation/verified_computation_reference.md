# 历史验证计算过程（SMD18 对齐待核实）：paper_2a71ffa4b0a90809 / paper_reproduction

归档日期：2026-09-26；复核日期：2026-09-27。**当前 HOLD，最新判断以第8节为准。**发现 SI 要求 SMD18，而历史计算使用普通 SMD，尚不能把约30 kcal/mol称为同一作者协议下对31 kcal/mol的验证。第4、5、7节保留历史验收判断，不是当前发布批准；历史真实计算及数值仍然保留。

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 4；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_4.md)
- [正文](../../../../papers/paper_2a71ffa4b0a90809/documents/main.pdf)；[补充材料](../../../../papers/paper_2a71ffa4b0a90809/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/continuous_profile_closure_20260925/result.json)；[历史结构化结果](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/hold_verified_paper_reproduction/paper_2a71ffa4b0a90809/agent_input/task.md)；[submission_schema](../../../../tasks/hold_verified_paper_reproduction/paper_2a71ffa4b0a90809/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

本档案仅涉及 PR。对象1a-syn：32原子C18F12I2、中性singlet，F27–C10–C13–I28 为来源一致的有符号取代基二面角；F在中央linker、I在外环，不能要求F/I各直接键连轴碳。SI S60 的作者协议为 M06-2X-D3/6-311+G(d,p)（C/F）、SDD（I）、**SMD18(THF)**、193.15K；S68–S69 描述向0°的 ModRedundant 扫描及约31 kcal/mol。历史计算实际使用普通 SMD(THF)，与作者协议不完全相同；此前将两者合并的写法已在本次更正。

实际 Gaussian16 C.01，GD3 零阻尼，193.15K/1atm。自由起点优化后开始连续受限扫描，保持同分支；初始G最低点与五个连续分支频率样本组成六个完整G状态。

## 3. 成功计算链与结果

正确1a-syn → 自由Opt/Freq最低点 → 连续15个已接受受约束电子几何 → 选其中5个几何单独完成Freq → 逐点确认与扫描父几何一致 → 去除整体运动/受限方向后计算89维切向曲率 → 相对于自由起点的G剖面 → 独立起点和低频处理敏感性。

| 实际角度，° | G，Eh | ΔG，kcal/mol | 完整Hessian负模，cm⁻¹ |
|---:|---:|---:|---|
| 69.563620 | −1906.474795 | 0 | 无 |
| 59.626152 | −1906.473137 | 1.040410708 | 无 |
| 39.750848 | −1906.462122 | 7.952427565 | 无 |
| 19.875591 | −1906.443159 | 19.851889722 | −13.5818 |
| 4.968998 | −1906.430518 | 27.784236983 | −46.5389 |
| 0.000243 | −1906.426981 | 30.003737993 | −30.6624 |

受限点的负扭转曲率不等于自由方向未收敛；五点切向曲率均正。G沿用原生Gaussian对负模的自动排除约定，不手动改正负号；该约定不是严格受限配分函数。`max(Gi−Gstart)×627.509474` 给30.003737993，处于31±1的下沿，仅高0.003737993；必须保留原值，不能四舍五入制造更大裕量。

独立0°起点给29.946634631，相差0.057103362（小于任务1.0的细化变化阈值），但它自身已在硬评分下界以外。50/100 cm⁻¹正频下限诊断给29.731694702/29.327035556；不是替换主结果的“新答案”。因此当前原生约定下通过，并不代表任意低频处理均稳定通过。

六个完整主步骤elapsed共2.9882h、实际CPU59.4741h；15点扫描有效前缀与后续磁盘失败所属整作业成本单列4.5582h，不能把尾部失败称作完整成功。独立起点仅属敏感性，不混入同分支六点主剖面。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| 1a_s129_gd3_193K_start_constrained_optfreq_20260914 | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/author_scan_repair_20260914/1a_s129_gd3_193K_start_constrained_optfreq_20260914/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_start_constrained_optfreq_20260914_hpc20_p6/stdout.log) | -1906.58615522 / -1906.474795 | 90 模；负模 无；最低正频 13.6371 cm⁻¹；日志正常结束 |
| 1a_s129_sequential_p02_freq_20260925 | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/completed_followups_20260915/1a_s129_sequential_p02_freq_20260925/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_p02_freq_20260925_hpc20_p6/stdout.log) | -1906.58517932 / -1906.473137 | 90 模；负模 无；最低正频 15.3764 cm⁻¹；日志正常结束 |
| 1a_s129_sequential_p06_freq_20260925 | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/completed_followups_20260915/1a_s129_sequential_p06_freq_20260925/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_p06_freq_20260925_hpc20_p6/stdout.log) | -1906.57371902 / -1906.462122 | 90 模；负模 无；最低正频 10.0613 cm⁻¹；日志正常结束 |
| 1a_s129_sequential_p10_freq_20260925 | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/completed_followups_20260915/1a_s129_sequential_p10_freq_20260925/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_p10_freq_20260925_hpc20_p6/stdout.log) | -1906.55524555 / -1906.443159 | 90 模；负模 [-13.5818]；最低正频 11.6514 cm⁻¹；日志正常结束 |
| 1a_s129_sequential_p13_freq_20260925 | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/completed_followups_20260915/1a_s129_sequential_p13_freq_20260925/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_p13_freq_20260925_hpc20_p6/stdout.log) | -1906.5426165 / -1906.430518 | 90 模；负模 [-46.5389]；最低正频 14.3465 cm⁻¹；日志正常结束 |
| 1a_s129_sequential_endpoint_freq_diskrepair_20260925 | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/completed_followups_20260915/1a_s129_sequential_endpoint_freq_diskrepair_20260925/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_endpoint_freq_diskrepair_20260925_hpc20_p6/stdout.log) | -1906.53922471 / -1906.426981 | 90 模；负模 [-30.6624]；最低正频 17.1324 cm⁻¹；日志正常结束 |
| sequential scan accepted prefix | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_gd3_193K_scan_optfreq_20260923_hpc20_p6/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_sequential_gd3_193K_scan_optfreq_20260923_hpc20_p6/stdout.log) | 前缀范围见说明；不取失败尾部数值 | 仅作已接受路径/扫描几何证据；不采用失败尾部的频率/热化学；整日志非正常终止，仅采用已接受前缀；只纳入 15 个已收敛电子扫描点；尾部磁盘失败不计为完整成功。六个 Gibbs 状态另有正常结束的频率日志。 |
| independent near-zero sensitivity | [输入](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_00deg_constrained_optfreq_20260914_hpc20_p6/input.com) / [输出](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_00deg_constrained_optfreq_20260914_hpc20_p6/stdout.log) | -1906.53946543 / -1906.427072 | 90 模；负模 [-27.0805]；最低正频 18.0628 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `1a_s129_gd3_193K_start_constrained_optfreq_20260914`：`#p M062X/GenECP EmpiricalDispersion=GD3 Opt=(Tight,MaxCycles=300) Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `1a_s129_sequential_p02_freq_20260925`：`#p M062X/GenECP EmpiricalDispersion=GD3 Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `1a_s129_sequential_p06_freq_20260925`：`#p M062X/GenECP EmpiricalDispersion=GD3 Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `1a_s129_sequential_p10_freq_20260925`：`#p M062X/GenECP EmpiricalDispersion=GD3 Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `1a_s129_sequential_p13_freq_20260925`：`#p M062X/GenECP EmpiricalDispersion=GD3 Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `1a_s129_sequential_endpoint_freq_diskrepair_20260925`：`#p M062X/GenECP EmpiricalDispersion=GD3 Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `sequential scan accepted prefix`：`#p M062X/GenECP EmpiricalDispersion=GD3 Opt=(ModRedundant,CalcFC,Tight,MaxCycles=300) Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。
- `independent near-zero sensitivity`：`#p M062X/GenECP EmpiricalDispersion=GD3 Opt=(Tight,MaxCycles=300,ModRedundant) Freq SCRF=(SMD,Solvent=THF) Temperature=193.15 NoSymm SCF=(XQC,MaxCycle=512)`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_input` | Uses supplied 1a-syn C18F12I2 neutral singlet and an explicit connectivity-valid F-C-C-I dihedral. | C18F12I2、32原子0/1；F27–C10–C13–I28对应当前PR和SI。 |
| 关键点 `kp_profile` | Builds a validated constrained profile from the syn starting angle toward zero degrees. | 15个连续已收敛电子几何，6个同分支G状态；自由最低点全正、受限点89维切向曲率正。 |
| 关键点 `kp_barrier` | Extracts the rotational barrier as the maximum relative Gibbs free energy on the profile. | 30.003737993 kcal/mol，在31±1下沿内；0.000243°采样最大。 |
| 关键点 `kp_limits` | Bounds the rigidity interpretation by sensitivity and the constrained-scan nature of the observable. | 独立近零起点差0.057103362；低频口径可越过硬评分边界，明确披露。 |
| 结论 `c_final` | The investigation supports a scoped rotational-barrier and rigidity conclusion for 1a. | 有限受限剖面支持较高扭转阻力；不是无约束TS或实验活化势垒。 |
| 结论 `c_limitation` | The scan has model and profile interpretation limits. | 热化学负模处理/采样范围/硬阈值敏感性均保留，不冒称稳健逐值复现。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_input` | `$.system`；Identity and atom mapping match the supplied XYZ. | `kp_input`：C18F12I2、32原子0/1；F27–C10–C13–I28对应当前PR和SI。 |
| `r_profile` | `$.scan_states, $.validation`；Profile coverage and state validation satisfy the task contract. | `kp_profile`：15个连续已收敛电子几何，6个同分支G状态；自由最低点全正、受限点89维切向曲率正。 |
| `r_barrier` | `$.barrier_result.barrier_kcal_mol`；31.0 ± 1.0 kcal/mol | `kp_barrier`：30.003737993 kcal/mol，在31±1下沿内；0.000243°采样最大。 |
| `r_limits` | `$.sensitivity, $.limitations`；Sensitivity and scoped limitations are specific. | `kp_limits`：独立近零起点差0.057103362；低频口径可越过硬评分边界，明确披露。 |
| `r_final` | `$.conclusion`；Final conclusion reports barrier and scoped rigidity interpretation. | `c_final`：有限受限剖面支持较高扭转阻力；不是无约束TS或实验活化势垒。 |
| `r_limitation` | `$.limitations`；Limitations are explicit and task-specific. | `c_limitation`：热化学负模处理/采样范围/硬阈值敏感性均保留，不冒称稳健逐值复现。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

PR 原任务允许明确受约束状态与自由最低点的区别，故实算支持其有限剖面目标及原容差，仍必须披露临界值和热化学敏感性。不能声称已找到无约束TS、完整syn→anti最小能量路径或实验速率势垒。

当前 AR 没有同步修正：F–C–C–I 文字定义不同，且要求所有做频率的推进态无虚频，与这条成功证据不一致。因此 AR 本轮不复制，也不擅自修改。后续应依据正文/SI明确同一坐标定义及受限验证规则，再复核现有链的适用性；不能仅因包校验通过就把它算作科学通过。发布前还应判断31±1硬阈值在合理热化学口径下是否足够稳定，不自动扩大容差。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [CONTINUOUS_PROFILE_STRICT_CLOSURE_20260925.md](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/CONTINUOUS_PROFILE_STRICT_CLOSURE_20260925.md)
- [result.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/continuous_G_profile_20260925/result.json)
- [result.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/constrained_curvature_20260925/result.json)
- [evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/evaluation_task_qualification.json)
- [current_target_disposition_20260926.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/current_target_disposition_20260926.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

SI p60方法、pp68–69的受限F–C–C–I扫描和约31 kcal/mol。

实际修复：保留PR受限剖面目标，成功至少五个不同有效状态、起点与近零端、真实势垒和实质敏感性。取消c_limitation；kp_limits保留为实际数值敏感性检查，不只是声明。原31±1靶和容差未改。

验证适用性：待负责人决定评分口径/参考容差，暂不建议发布。主结果离30下界仅0.003737993，极小实现差异就翻转判分；既有实算并非缺失，不以扩大容差或替换gold自动解决，不重算、不迁移。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_input` | Reports formula, charge, multiplicity, coordinate provenance and four atom indices consistent with the 32-atom XYZ. | 15电子扫描状态/6 Gibbs点，主势垒30.003737993；独立近零29.946634631，低频50/100处理29.731694702/29.327035556；自由起点90正模，受限切向89维曲率检查支持受限驻点。 |
| `kp_profile` | At least five distinct converged states span the interval with actual angles, relative Gibbs energies, state validation and maximum identified. | 15电子扫描状态/6 Gibbs点，主势垒30.003737993；独立近零29.946634631，低频50/100处理29.731694702/29.327035556；自由起点90正模，受限切向89维曲率检查支持受限驻点。 |
| `kp_barrier` | Numeric barrier in kcal mol-1 with reference state, maximum state, extraction method and coverage. | 15电子扫描状态/6 Gibbs点，主势垒30.003737993；独立近零29.946634631，低频50/100处理29.731694702/29.327035556；自由起点90正模，受限切向89维曲率检查支持受限驻点。 |
| `kp_limits` | A concrete numerical sensitivity/robustness test reports its effect on the constrained-scan barrier and identifies the quantity actually computed. | 15电子扫描状态/6 Gibbs点，主势垒30.003737993；独立近零29.946634631，低频50/100处理29.731694702/29.327035556；自由起点90正模，受限切向89维曲率检查支持受限驻点。 |
| `c_final` | States extracted barrier, maximum location and whether the evidence supports rigid/atropisomeric behavior within the computational boundary. | 15电子扫描状态/6 Gibbs点，主势垒30.003737993；独立近零29.946634631，低频50/100处理29.731694702/29.327035556；自由起点90正模，受限切向89维曲率检查支持受限驻点。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_input` → `kp_input`；读取 `$.system`。
- `r_profile` → `kp_profile`；读取 `$.scan_states, $.validation`。
- `r_barrier` → `kp_barrier`；读取 `$.barrier_result.barrier_kcal_mol`。
- `r_limits` → `kp_limits`；读取 `$.sensitivity, $.barrier_result`。
- `r_final` → `c_final`；读取 `$.conclusion`。

## 8. 2026-09-27 原文/实际输入再次核对：SMD18 缺项，暂停发布

### 已确认事实

1. 正文 PDF 第5页明确给 **31.0 kcal/mol**；SI S-68 描述约69°到0°的受限扫描及 **31 kcal/mol**；S-69 的实际图题为 Figure S52–S54，其中 S54 是 Gibbs 剖面。正文与 SI 不支持把论文原值写为30。SI 段落内图号比实际图题错后一个，不影响数值读取。
2. SI S-60、S-66、S-69 明写 **SMD18**；S-85 的 S24 为 Engelage 等的 *Refined SMD Parameters for Bromine and Iodine Accurately Model Halogen-Bonding Interactions in Solution*，DOI `10.1002/chem.201803652`。本次核对该 DOI 的出版者摘要记录，SMD18是修改 Br/I Coulomb 半径后的模型，其他参数沿用SMD；不是把“18”误读为引用号。
3. 第3节原始 input.com 全部为 `SCRF=(SMD,Solvent=THF)`，没有 SMD18 半径读入。`constrained_curvature_20260925` 的五份 `.fchk` 均在 `PCM-NOrd` 中保持原子顺序，`PCM-SphereRadii` 的第23、28项（I）均为 **3.74165773 bohr = 1.9800000017 Å**。这直接确认了实际腔体参数，而不仅是根据 route 名称猜测。
4. 作者 SI Table S21 的 syn 起点电子能/G为 **−1906.5806471 / −1906.469033 Eh**；历史实际起点为 **−1906.58615522 / −1906.474795 Eh**。实际减作者分别为 **−3.456397484 / −3.615709589 kcal/mol**。差异在电子能层面已存在，不能只归因于负模或热熵处理；两套起点不同，不能把作者起点与本地终点混合相减。
5. 本地连续近零端 E/G 为 **−1906.53922471 / −1906.426981 Eh**；对应电子势垒 **29.449339645**，G−E 修正差 **0.554398345**，总 Gibbs 势垒 **30.003737993 kcal/mol**。独立端点 **29.946634631**；50/100 cm⁻¹低频控制 **29.731694702 / 29.327035556**。这些是原有实算值，不是本次新计算。

### 判断与不能据此作出的推断

**已确认的路线不一致是 SMD18 → 普通 SMD。**它是需要优先核查的物理模型差异，而非简单四舍五入；尚未有同几何、同其他参数的 SMD18 对照，不能声称它已经定量解释了全部约1 kcal/mol偏差，也不能保证补入SMD18就一定得到31。M06-2X、GD3、基组/ECP、THF、193.15K、0/1及SI定义的扫描对象总体对齐；Gaussian版本、网格、基组近线性相关、精确扫描网格和热化学约定仍需在作者材料可确定的范围内记录，不能将其中任一未知项认定为已证实原因。

之前“不是缺计算、只是评分边缘敏感性”及“采用本地30替换原靶”的建议不再作为处理依据。原 `31.0 ± 1.0` 保留；主值刚好在容差内并不证明作者协议已被复现。现有链支持普通SMD下同一扭转对象的高势垒趋势，不足以完成SMD18数值对齐验收。

### 后续处理（本次没有执行任何新计算）

- 先从 S24 正文/SI或作者输入核实准确 SMD18 Br/I 参数及 Gaussian 实现；本次未取得该参数表，**不猜填半径**。若既有文件存在真正SMD18计算，应先检索并利用，不默认重算全部链。
- 如无匹配计算，建议先获准做同一 syn/近零几何、其余参数相同的普通SMD/SMD18成对单点诊断，分离溶剂模型的电子能贡献。该诊断不能替代完整 Gibbs 验证。
- 若需要正式恢复作者协议，应统一 SMD18 下的起点、连续受限扫描及必要频率/热化学计算，保留受限点的正确曲率定义；不能把0°受限点冒充无约束TS。分别核对 Table S21 起点、剖面和31的参照。
- 匹配协议、实际结果与任务/evaluator一致后再申请迁出 hold；若仍有偏差，报告原因和适用范围，再由负责人决定，不自动改为30或扩大容差。

本次仅把本PR包移入 `tasks/hold_verified_paper_reproduction/paper_2a71ffa4b0a90809`，修正维护说明和迁移链接。AR没有入本批，未移动或修改；公开输入、task、schema及五个evaluator文件未改，历史docs/verification未改。

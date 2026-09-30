# 已验证成功计算过程：paper_2877efc02814175d / paper_reproduction

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 2；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_2.md)
- [正文](../../../../docs/verification/group_2/paper_2877efc02814175d/source_data/user_supplied_20260925/1-s2.0-S0022286025023567-main.pdf)；[补充材料](../../../../papers/paper_2877efc02814175d/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/recovered_source_closure_20260925/INDEPENDENT_RESULTS.json)；[历史结构化结果](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/recovered_source_closure_20260925/paper_reproduction/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_paper_reproduction/paper_2877efc02814175d/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_paper_reproduction/paper_2877efc02814175d/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

固定 DQCS–Cd、DQCS–Co、DQCS–Ni 三个 65 原子配合物，不把单分子连续介质模型的前线轨道描述符扩展为溶液结合自由能或显式离子竞争。SI Tables S1–S3 支持各对象 +2 电荷；Cd/Ni singlet，Co doublet。2026-09-25 用户补充的可读正文 §2.3、§3.8、Table 1 支持 B3LYP/LANL2DZ、DMSO 及比较趋势；原 `papers/.../documents/main.pdf` 仍不可正常提取，下面引用实际可读原件而非把旧损坏文件称为恢复。

实际 Gaussian16 C.01；B3LYP/LANL2DZ，PCM(DMSO)，UltraFine、Tight/XQC。正文说明 DMSO，但未公布精确连续介质关键字及开壳层前线轨道选取口径，因此 PCM 与同自旋 gap 是明确披露的实现，不能冒称找回作者未公开输入。历史源软件为 Gaussian09W。

## 3. 成功计算链与结果

三个 SI 对象身份/电荷自旋核对 → Cd/Ni 独立 Opt/Freq；Co 先完成 Stable=Opt 得稳定波函数，再由该 checkpoint 做 Opt/Freq，最后对同一几何再次 Stable=Opt → 分别读取占据/空轨道 → 同一公式计算 gap、硬度和亲电性 → 比较趋势。三个终态均 189 个正频率，最低分别 15.4929、10.5196、16.0487 cm⁻¹。

统一取最小非负**同自旋** HOMO–LUMO gap；`eta=gap/2`，`mu=(HOMO+LUMO)/2`，`omega=mu²/(2eta)`，全部以 eV 为基础计算。Co 的 alpha/beta 两通道均保留；不是混用 alpha HOMO 和 beta LUMO 来人为缩小 gap。

| 对象 | 实算 gap/eta/omega，eV | 正文 Table 1 gap/eta/omega，eV |
|---|---|---|
| Cd | 1.980716805 / 0.990358402 / 10.096990298 | 1.997 / 0.998 / 9.957 |
| Co，alpha | 1.515946328 / 0.757973164 / 15.022868871 | 1.511 / 0.755 / 15.112 |
| Ni | 1.238934416 / 0.619467208 / 19.837103098 | 1.243 / 0.621 / 19.744 |

Co beta：gap 1.521660719、eta 0.760830359、omega 14.946830819 eV；两口径均支持 gap/硬度 Cd>Co>Ni、亲电性 Ni>Co>Cd。Co 的 `<S²>` 为湮灭前 0.9911、后 0.7509；Stable 不等于严格自旋纯态。当前 evaluator 评上述定性三对象趋势，不硬评作者小数逐位一致。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| Cd Opt/Freq | [输入](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_cd_b3lyp_lanl2dz_dmsO_optfreq_local_migration_20260904T161554Z/input.com) / [输出](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_cd_b3lyp_lanl2dz_dmsO_optfreq_local_migration_20260904T161554Z/stdout.log) | -1635.12731689 / -1634.676108 | 189 模；负模 无；最低正频 15.4929 cm⁻¹；日志正常结束 |
| Co preparatory Stable=Opt determinant | [输入](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_Co_doublet_PCM_DMSO_wavefunction_stability_20260915_20260916T043623Z/input.com) / [输出](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_Co_doublet_PCM_DMSO_wavefunction_stability_20260915_20260916T043623Z/stdout.log) | -1732.07687439 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束；后续 Co Opt/Freq 的实际 %OldChk 波函数来源；不以本步骤代替终态频率验证。 |
| Co Opt/Freq | [输入](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_Co_stable_doublet_checkpoint_optfreq_20260916_20260916T211754Z/input.com) / [输出](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_Co_stable_doublet_checkpoint_optfreq_20260916_20260916T211754Z/stdout.log) | -1732.08606314 / -1731.631885 | 189 模；负模 无；最低正频 10.5196 cm⁻¹；日志正常结束 |
| Co final Stable/frontiers | [输入](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_Co_final_minimum_checkpoint_stability_20260918_20260918T033658Z/input.com) / [输出](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_Co_final_minimum_checkpoint_stability_20260918_20260918T033658Z/stdout.log) | -1732.08606314 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| Ni Opt/Freq | [输入](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_ni_b3lyp_lanl2dz_dmsO_optfreq_local_migration_20260904T150248Z/input.com) / [输出](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/qzcli_hpc/author_ni_b3lyp_lanl2dz_dmsO_optfreq_local_migration_20260904T150248Z/stdout.log) | -1756.29455962 / -1755.838623 | 189 模；负模 无；最低正频 16.0487 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `Cd Opt/Freq`：`#p B3LYP/LANL2DZ Opt=(CalcFC,MaxCycles=300) Freq SCRF=(PCM,Solvent=DMSO) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。
- `Co preparatory Stable=Opt determinant`：`#p UB3LYP/LANL2DZ Stable=Opt SCRF=(PCM,Solvent=DMSO) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。
- `Co Opt/Freq`：`#p UB3LYP/LANL2DZ Guess=Read Opt=(CalcFC,MaxCyc=300,MaxStep=10) Freq SCRF=(PCM,Solvent=DMSO) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。
- `Co final Stable/frontiers`：`#p UB3LYP/LANL2DZ Guess=Read Stable=Opt SCRF=(PCM,Solvent=DMSO) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。
- `Ni Opt/Freq`：`#p B3LYP/LANL2DZ Opt=(CalcFC,MaxCycles=300) Freq SCRF=(PCM,Solvent=DMSO) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `p_state` | The submitted calculation checks each supplied 65-center complex identity and uses the source-supported object-specific states: total charge +2 with singlet multiplicity 1 for Cd and Ni, and doublet multiplicity 2 for Co. | 三个65原子对象；Cd(+2,1)、Co(+2,2)、Ni(+2,1)，不套用统一singlet。 |
| 关键点 `p_converge` | The submitted electronic-structure calculations establish convergence or explicitly document a bounded failure for every named complex. | 三者189正频；Co稳定波函数→Opt/Freq→终点Stable，同几何关联。 |
| 关键点 `p_gap` | The computed HOMO-LUMO gaps are reported for the three named complexes using one defined orbital convention. | Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV。 |
| 关键点 `p_desc` | Hardness and electrophilicity are computed and defined consistently across the three complexes. | 同一eta=gap/2、omega=mu²/(2eta)定义；完整数值见§3。 |
| 结论 `c_trend` | Within the supplied three-complex comparison, the electronic descriptors support a monotonic metal-dependent trend with Ni the smallest-gap/softest/most electrophilic member in the reported reference analysis. | gap/eta为Cd>Co>Ni，omega相反，两个Co自旋通道均保持趋势。 |
| 结论 `c_limits` | The result is limited to the supplied geometries, state assignment, solvent treatment and chosen electronic-structure model. | 当前评分所需披露：PCM/同自旋实现、非直接结合自由能；历史结果已有对应解释，不新增限制。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_state` | `$.state_checks.details`；identity and source-supported object-specific state checks | `p_state`：三个65原子对象；Cd(+2,1)、Co(+2,2)、Ni(+2,1)，不套用统一singlet。 |
| `r_conv` | `$.complexes[].validation`；per-object convergence or failure | `p_converge`：三者189正频；Co稳定波函数→Opt/Freq→终点Stable，同几何关联。 |
| `r_gap` | `$.complexes[].observables`；per-object gaps | `p_gap`：Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV。 |
| `r_desc` | `$.method.descriptor_definitions, $.complexes[].observables`；hardness and electrophilicity | `p_desc`：同一eta=gap/2、omega=mu²/(2eta)定义；完整数值见§3。 |
| `r_trend` | `$.comparison`；qualified trend | `c_trend`：gap/eta为Cd>Co>Ni，omega相反，两个Co自旋通道均保持趋势。 |
| `r_lim` | `$.limitations`；limitations | `c_limits`：当前评分所需披露：PCM/同自旋实现、非直接结合自由能；历史结果已有对应解释，不新增限制。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

作者知情计算支持两模式的四关键点、描述符趋势及原评分结论。没有验证自由配体结合能、金属交换平衡、显式溶剂物种分布或盲自主计算。软件版本/连续介质实现差异已披露，不因此自动要求重算。

待整理：恢复正文尚保存在 group2 的 source_data，而原论文库 main.pdf 仍损坏，后续应维护论文索引；不能把“已找到可读原件”误写成原库文件已修复。源包的旧元数据/私有说明和 limitation 评分需另轮按流程核对，本轮不改变科学内容。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [FINAL_AUDIT.md](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/recovered_source_closure_20260925/FINAL_AUDIT.md)
- [EVALUATOR_AUDIT.json](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/recovered_source_closure_20260925/EVALUATOR_AUDIT.json)
- [independent_descriptors.json](../../../../docs/verification/group_2/paper_2877efc02814175d/provenance/completed_stability_analysis_20260918/independent_descriptors.json)
- [SOURCE_RECEIPT.json](../../../../docs/verification/group_2/paper_2877efc02814175d/source_data/user_supplied_20260925/SOURCE_RECEIPT.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

可读正文位于group_2/source_data/user_supplied_20260925，正文§2.3/p2、§3.8/Table1/p8；SI Tables S1–S3/pp11–13。

实际修复：保留给定三配合物性质比较；绑定Cd/Co/Ni唯一对象及正确自旋，规范gap/eta/omega定义；删除legacy metadata追问及c_limits，将有效状态/收敛证据接回c_trend。

验证适用性：仅以当前定性序关系评分，不新增逐数值靶；给定结构不是待发现答案。不将电子描述符等同结合自由能。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `p_state` | All three named objects are individually identified and their 65-center/+2/state checks are recorded as Cd(+2,1), Co(+2,2), and Ni(+2,1). | 三对象189个正模；Co稳定性→优化频率→终态稳定性链存在。gap Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV；eta同序、omega反序。 |
| `p_converge` | Per-object convergence/stationarity evidence supports the valid observables. Credit only actually validated objects; diagnostics for a failed object do not establish its convergence. | 三对象189个正模；Co稳定性→优化频率→终态稳定性链存在。gap Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV；eta同序、omega反序。 |
| `p_gap` | Calculated gap values in eV are supplied for Cd, Co, and Ni under one consistent orbital convention. Credit only gaps supported by real converged calculations; a missing value remains unachieved. | 三对象189个正模；Co稳定性→优化频率→终态稳定性链存在。gap Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV；eta同序、omega反序。 |
| `p_desc` | Per-object hardness and electrophilicity with units and formulas are reported for the valid calculations. | 三对象189个正模；Co稳定性→优化频率→终态稳定性链存在。gap Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV；eta同序、omega反序。 |
| `c_trend` | Real like-defined results support gap and hardness Cd > Co > Ni, electrophilicity Ni > Co > Cd. These are electronic descriptors, not measured binding free energies. | 三对象189个正模；Co稳定性→优化频率→终态稳定性链存在。gap Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV；eta同序、omega反序。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_state` → `p_state`；读取 `$.state_checks, $.complexes`。
- `r_conv` → `p_converge`；读取 `$.complexes[*].validation`。
- `r_gap` → `p_gap`；读取 `$.complexes[*].observables`。
- `r_desc` → `p_desc`；读取 `$.method.descriptor_definitions, $.complexes[*].observables`。
- `r_trend` → `c_trend`；读取 `$.comparison, $.complexes, $.method`。

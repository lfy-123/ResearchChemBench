# 已验证成功计算过程：paper_8fefc96b015c4577 / paper_reproduction

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 2；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_2.md)
- [正文](../../../../papers/paper_8fefc96b015c4577/documents/main.pdf)；[补充材料](../../../../papers/paper_8fefc96b015c4577/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/INDEPENDENT_RESULTS.json)；[历史结构化结果](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/paper_reproduction/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_paper_reproduction/paper_8fefc96b015c4577/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_paper_reproduction/paper_8fefc96b015c4577/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

三个固定 53 原子对象 C21H24F2NO4S：共同中间体 B、两个候选 TS2/TS2′，全部为中性 doublet。入库时 AR 公共文件曾使用 `state_reference / state_candidate_1 / state_candidate_2`，依次对应 B/TS2/TS2′；不是中性闭壳层。SI p34 方法及 pp36–41 坐标，正文 p4 的同一能量零点为依据。

Gaussian16，B3LYP-D3 **zero damping/GD3**、def2-TZVPP、SMD(DMSO)、UltraFine；每个对象重新 Opt/Freq（两 TS 使用 TS 优化）。原始日志确认 153 个振动模式，B 无虚频；TS2/TS2′ 各一个 −470.6863/−476.5989 cm⁻¹ 虚频。

## 3. 成功计算链与结果

作者 SI 坐标及正确 doublet 状态 → B 最低点优化/频率、两个候选 TS 优化/频率 → 核对唯一虚频位移 → 读取同口径 Gibbs 总能 → 以 B 作共同零点计算两势垒与差值。位移检查分别沿 C22–C45、C5–C22 成键方向；±0.05 模位移使距离分别 2.0500→2.1657 Å、2.0636→2.1788 Å。此为振动模式证据，不是假称已完成 IRC；历史题面把进一步 IRC/位移列为可行时的增强验证；修订版要求相关负模检查，IRC仍非强制。

| 状态 | 实算 G，Eh | 作者 SI G，Eh |
|---|---:|---:|
| B | −1768.467198 | −1768.468122 |
| TS2 | −1768.446078 | −1768.447278 |
| TS2′ | −1768.436510 | −1768.437447 |

`ΔG‡=(GTS−GB)×627.509474`：TS2 为 13.253000092、TS2′ 为 19.257010740，差为 +6.004010648 kcal/mol，分别满足 13.08±1.5、19.25±1.5；PR 差值还满足 6.17±1.5。正文 −13.13、−0.05、6.12 是**相对于分离反应物的高度**，不能把 −0.05 误当相对于 B 的势垒；减去 B 后才是本任务参考 13.08/19.25。两个候选均有正势垒且 TS2 更低。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| intermediate_B Opt/Freq | [输入](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/qzcli_hpc/author_intermediate_B_doublet_b3lypd3_def2tzvpp_smd_optfreq_hpc20_20260911T063150Z/input.com) / [输出](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/qzcli_hpc/author_intermediate_B_doublet_b3lypd3_def2tzvpp_smd_optfreq_hpc20_20260911T063150Z/stdout.log) | -1768.82471489 / -1768.467198 | 153 模；负模 无；最低正频 14.6939 cm⁻¹；日志正常结束 |
| ts2 Opt/Freq | [输入](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/qzcli_hpc/author_ts2_doublet_b3lypd3_def2tzvpp_smd_optfreq_hpc20_20260911T063154Z/input.com) / [输出](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/qzcli_hpc/author_ts2_doublet_b3lypd3_def2tzvpp_smd_optfreq_hpc20_20260911T063154Z/stdout.log) | -1768.80202896 / -1768.446078 | 153 模；负模 [-470.6863]；最低正频 12.7413 cm⁻¹；日志正常结束 |
| ts2_prime Opt/Freq | [输入](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/qzcli_hpc/author_ts2_prime_doublet_b3lypd3_def2tzvpp_smd_optfreq_hpc20_20260911T063201Z/input.com) / [输出](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/qzcli_hpc/author_ts2_prime_doublet_b3lypd3_def2tzvpp_smd_optfreq_hpc20_20260911T063201Z/stdout.log) | -1768.79326476 / -1768.43651 | 153 模；负模 [-476.5989]；最低正频 11.7263 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `intermediate_B Opt/Freq`：`#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 SCRF=(SMD,Solvent=DimethylSulfoxide) Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。
- `ts2 Opt/Freq`：`#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 SCRF=(SMD,Solvent=DimethylSulfoxide) Opt=(TS,CalcFC,NoEigenTest,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。
- `ts2_prime Opt/Freq`：`#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 SCRF=(SMD,Solvent=DimethylSulfoxide) Opt=(TS,CalcFC,NoEigenTest,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_proc_freq` | The submitted workflow classifies intermediate B as a minimum and TS2 and TS2′ as first-order saddle points using harmonic frequencies. | B 0个虚频、两TS各1个反应相关虚频；各153模。 |
| 关键点 `kp_proc_trace` | The barrier comparison uses a common B reference and traceable, consistently defined Gibbs free energies. | 同一53原子中性doublet、B3LYP-D3/def2-TZVPP/SMD-DMSO，B共同零点。 |
| 关键点 `kp_res_barriers` | The calculated barriers reproduce the source comparison for TS2 and TS2′ relative to B. | 13.253000092/19.257010740 kcal/mol，符合13.08/19.25各±1.5。 |
| 关键点 `kp_res_difference` | The two cyclization barriers are separated substantially, with TS2 lower than TS2′ in the source model. | PR TS2′−TS2=+6.004010648，符合+6.17±1.5。 |
| 结论 `c_final` | Within the supplied molecular model and the submitted computational protocol, the validated barrier comparison supports the authors' qualitative proposal that the TS2 cyclization is more feasible than TS2′ and therefore rationalizes preferential progression toward the hydroisoquinoline pathway. | 较低TS2通道得到有限模型支持；没有把未完成IRC或完整反应网络写成已验证。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_freq` | `$.states.intermediate_B.validation_status, $.states.ts2.validation_status, $.states.ts2_prime.validation_status, $.states.intermediate_B.imaginary_frequency_count, $.states.ts2.imaginary_frequency_count, $.states.ts2_prime.imaginary_frequency_count`；Frequency counts and validation statuses distinguish the minimum from first-order saddles for each named structure. | `kp_proc_freq`：B 0个虚频、两TS各1个反应相关虚频；各153模。 |
| `r_trace` | `$.method.software, $.method.model_chemistry, $.method.solvent, $.states.intermediate_B.identity, $.comparison.reference_state`；The calculation is reproducible from explicit method, state identity, units, and common-reference provenance. | `kp_proc_trace`：同一53原子中性doublet、B3LYP-D3/def2-TZVPP/SMD-DMSO，B共同零点。 |
| `r_b1` | `$.comparison.barrier_ts2`；13.08 ± 1.5 kcal/mol | `kp_res_barriers`：13.253000092/19.257010740 kcal/mol，符合13.08/19.25各±1.5。 |
| `r_b2` | `$.comparison.barrier_ts2_prime`；19.25 ± 1.5 kcal/mol | `kp_res_barriers`：13.253000092/19.257010740 kcal/mol，符合13.08/19.25各±1.5。 |
| `r_diff` | `$.comparison.barrier_difference`；6.17 ± 1.5 kcal/mol | `kp_res_difference`：PR TS2′−TS2=+6.004010648，符合+6.17±1.5。 |
| `r_conc` | `$.conclusion, $.limitations`；TS2 is lower than TS2′ and the conclusion is explicitly limited to the validated computational model. | `c_final`：较低TS2通道得到有限模型支持；没有把未完成IRC或完整反应网络写成已验证。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

入库时任务是给定三个对象的驻点/热化学比较（2026-09-26 已按负责人要求移除公开作者TS）；验证支持 AR 的候选排序以及 PR 的作者通道解释，不证明从公开反应物自主发现 TS 或完整反应网络。必须按当前科学目标另做公开输入边界审查，不能因为改名就声称作者 TS 坐标不含答案。

待后续修复：私有 `paper_route.md` 仍称 neutral closed-shell，与真实 doublet 及当前公开任务不符；应同步但本轮不改。reference 中不包含新计算，不把论文 G 当作实算 G，不把模式检查冒称 IRC。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [FINAL_AUDIT.md](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/FINAL_AUDIT.md)
- [EVALUATOR_AUDIT.json](../../../../docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/EVALUATOR_AUDIT.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

正文p4/Scheme3；SI p34方法、pp36–41 B/TS2/TS2′坐标。

实际修复：按负责人要求把三份作者坐标移至evaluation/author_results；公开SMILES/连接图和ETKDGv3(seed20260926)+UFF独立生成的自由基初态，0/2，53原子。两TS须自行构建。AR候选编号不含作者通道，私有规则按真实连接/成键模式映射，不按能量挑身份；PR提供两通道指导但不提供胜者。主比较DMSO/298.15K/1atm。

验证适用性：历史作者知情验证支持相同驻点和能垒可计算，不是新公开初态的盲测成功。未新增强制IRC；现有负模位移证据有效。author_results仅作私有结构参考，未新增RMSD评分。公开初态只做化学身份/连通性/数值几何检查，未运行QM。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_proc_freq` | Frequency evidence establishes zero imaginary modes for B and one relevant imaginary mode for each of TS2 and TS2′. Credit only states actually validated; reporting failure does not validate a missing state. | 原始B/两TS均重新OptFreq；153模分别0/1/1个虚频，TS模式−470.6863/−476.5989 cm⁻¹，成键模式对应C22–C45和C5–C22（历史原子顺序）。势垒13.253000092/19.257010740，差6.004010648 kcal/mol，目标13.08/19.25/6.17各±1.5未改。 |
| `kp_proc_trace` | Map each saddle by molecular connectivity and forming-bond/negative-mode evidence: benzyl-tethered aryl closure corresponds to private TS2, arenesulfonyl aryl closure to private TS2-prime. Never map by closest energy or by arbitrary candidate number. Common-reference energies and all optimized identities are traceable. | 原始B/两TS均重新OptFreq；153模分别0/1/1个虚频，TS模式−470.6863/−476.5989 cm⁻¹，成键模式对应C22–C45和C5–C22（历史原子顺序）。势垒13.253000092/19.257010740，差6.004010648 kcal/mol，目标13.08/19.25/6.17各±1.5未改。 |
| `kp_res_barriers` | Both chemically identified saddle barriers are calculated from consistent Gibbs energies relative to B, with units and traceable calculation evidence, and agree with the private targets within the stated tolerances. | 原始B/两TS均重新OptFreq；153模分别0/1/1个虚频，TS模式−470.6863/−476.5989 cm⁻¹，成键模式对应C22–C45和C5–C22（历史原子顺序）。势垒13.253000092/19.257010740，差6.004010648 kcal/mol，目标13.08/19.25/6.17各±1.5未改。 |
| `kp_res_difference` | Correctly mapped benzyl-tethered aryl closure has the lower common-reference barrier than arenesulfonyl aryl closure; both values and their subtraction are supported by validated saddles. | 原始B/两TS均重新OptFreq；153模分别0/1/1个虚频，TS模式−470.6863/−476.5989 cm⁻¹，成键模式对应C22–C45和C5–C22（历史原子顺序）。势垒13.253000092/19.257010740，差6.004010648 kcal/mol，目标13.08/19.25/6.17各±1.5未改。 |
| `c_final` | Correctly mapped benzyl-tethered aryl closure has the lower common-reference barrier than arenesulfonyl aryl closure; both values and their subtraction are supported by validated saddles. | 原始B/两TS均重新OptFreq；153模分别0/1/1个虚频，TS模式−470.6863/−476.5989 cm⁻¹，成键模式对应C22–C45和C5–C22（历史原子顺序）。势垒13.253000092/19.257010740，差6.004010648 kcal/mol，目标13.08/19.25/6.17各±1.5未改。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_freq` → `kp_proc_freq`；读取 `$.states.intermediate_B.validation_status, $.states.ts2.validation_status, $.states.ts2_prime.validation_status, $.states.intermediate_B.imaginary_frequency_count, $.states.ts2.imaginary_frequency_count, $.states.ts2_prime.imaginary_frequency_count`。
- `r_trace` → `kp_proc_trace`；读取 `$.states, $.method, $.comparison`。
- `r_b1` → `kp_res_barriers`；读取 `$.states, $.comparison`。
- `r_b2` → `kp_res_barriers`；读取 `$.states, $.comparison`。
- `r_diff` → `kp_res_difference`；读取 `$.comparison.barrier_difference`。
- `r_conc` → `c_final`；读取 `$.states, $.comparison, $.conclusion`。

格式适配只将旧结果 optimized_geometry 映射为 geometry_file、mode_check.forming_C_C_pair_1based 映射为 forming_bond_1based，并通过元素标记反应物连接图建立旧/新原子编号对应；不改变计算值、不把验证者所知的TS作为公开输入。AR候选编号可交换，评分按化学通道映射。

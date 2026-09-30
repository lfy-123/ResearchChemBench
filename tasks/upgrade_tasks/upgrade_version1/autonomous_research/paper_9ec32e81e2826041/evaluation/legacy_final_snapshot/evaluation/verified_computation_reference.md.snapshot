# 已验证成功计算过程：paper_9ec32e81e2826041 / autonomous_research

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 3；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_3.md)
- [正文](../../../../papers/paper_9ec32e81e2826041/documents/main.pdf)；[补充材料](../../../../papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_3/paper_9ec32e81e2826041/provenance/closeout_20260923/acceptance_evidence.json)；[历史结构化结果](../../../../docs/verification/group_3/paper_9ec32e81e2826041/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_autonomous_research/paper_9ec32e81e2826041/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_autonomous_research/paper_9ec32e81e2826041/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

两个指定 Z-cAAC^Cy 构象，均为 C35H43NZn、80 原子、中性 singlet。SI Tables S1/S2 的源坐标已由逐行解析核对；旧损坏坐标不是本次依据。SI PDF p3 明确 PBE0/6-311+G**、D3BJ、300 K；Table S7（p21）比较 `Gcoplanar−Gperpendicular`。

实际 Gaussian16 C.01 的 PBE1PBE/6-311+G(d,p)、GD3BJ、气相、300 K/1 atm、UltraFine、NoSymm，SCF/XQC 与 checkpoint 数值重启见真实输入。源文为 C.02；差异披露，不把软件修订号写成相同。任务未要求计算无 D3BJ 分支、其他配体、晶体或溶液布居。

## 3. 成功计算链与结果

正确 SI 两套 80 原子坐标 → 各自独立 Opt/Freq → 检查元素序、连接关系及构象保留 → 统一 300 K RRHO Gibbs 能 → 有符号差值。两者均 234 个正频率，最低 11.1432/13.8852 cm⁻¹。

| 构象 | E，Eh | 热 G 修正，Eh | G，Eh |
|---|---:|---:|---:|
| perpendicular | −3192.15207682 | 0.626271 | −3191.525806 |
| coplanar | −3192.15336107 | 0.627537 | −3191.525824 |

`ΔG=(−3191.525824+3191.525806)×2625.499638 = −0.047258993 kJ/mol`。SI 为 −0.1 kJ/mol；数值不同但支持当前近等能结论，非严格简并。打印精度对应差值舍入界约 0.00263 kJ/mol，不应声称无限精度。最终结构相对源坐标 RMSD 约 0.000000488/0.000506041 Å；两构象分别保留约 72.733°/17.006° 的平面夹角，不能把 coplanar 标签误当理想 0° 约束。

两有效作业 elapsed 合计 68246.812 s（18.9574 h），实际并行日历跨度约 9.56 h；CPU 请求乘 elapsed 与日志实际 CPU 用时不是同一个量。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| perpendicular Opt/Freq | [输入](../../../../docs/verification/group_3/paper_9ec32e81e2826041/provenance/repair_20260915/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/production.com) / [输出](../../../../docs/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/gaussian.log) | -3192.15207682 / -3191.525806 | 234 模；负模 无；最低正频 11.1432 cm⁻¹；日志正常结束 |
| coplanar Opt/Freq | [输入](../../../../docs/verification/group_3/paper_9ec32e81e2826041/provenance/repair_20260915/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/production.com) / [输出](../../../../docs/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/gaussian.log) | -3192.15336107 / -3191.525824 | 234 模；负模 无；最低正频 13.8852 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `perpendicular Opt/Freq`：`#p PBE1PBE/6-311+G(d,p) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxStep=5,MaxCycles=256) Freq Temperature=300 Int=UltraFine NoSymm SCF=(XQC,MaxCycle=2048) Guess=Restart`。
- `coplanar Opt/Freq`：`#p PBE1PBE/6-311+G(d,p) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxStep=5,MaxCycles=256) Freq Temperature=300 Int=UltraFine NoSymm SCF=(XQC,MaxCycle=2048) Guess=Restart`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `ar_process_inputs` | The submission validates the named structure and reports its thermochemistry. | 两份80原子源映射、0/1态和连接性对应；非旧损坏坐标。 |
| 关键点 `ar_process_validation` | The submission validates the named structure and reports its thermochemistry. | 两独立最低点234正频，各自同300 K RRHO。 |
| 关键点 `ar_result_delta` | The signed Gibbs free-energy difference is computed with the stated convention. | Gcoplanar−Gperpendicular=−0.047258993 kJ/mol，非绝对值或相反号。 |
| 结论 `ar_final_conclusion` | The two-state comparison is interpreted within the stated computational boundary. | 两指定构象近等能；不是全局简并或溶液布居结论。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_ar_process_inputs` | `$.structures[*].stationary_point`；The required validation is reported. | `ar_process_inputs`：两份80原子源映射、0/1态和连接性对应；非旧损坏坐标。 |
| `r_ar_process_validation` | `$.structures[*].stationary_point`；The required validation is reported. | `ar_process_validation`：两独立最低点234正频，各自同300 K RRHO。 |
| `r_ar_result_delta` | `$.comparison`；The submission reports the signed G_coplanar − G_perpendicular comparison in kJ mol−1 when both calculations are complete, or gives a truthful bounded-failure explanation without a fabricated number. | `ar_result_delta`：Gcoplanar−Gperpendicular=−0.047258993 kJ/mol，非绝对值或相反号。 |
| `r_ar_final_conclusion` | `$.conclusion, $.limitations`；The conclusion is bounded and limitation-aware. | `ar_final_conclusion`：两指定构象近等能；不是全局简并或溶液布居结论。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

同一两构象比较支持两模式当前 evaluator。不给“任意构象全局最低”或溶液真实布居认证，也不要求验证者从随机几何独立发现已给定对象。

待整理：两个 process 评分项目前绑定相似的驻点证据，后续可检查是否重复计分；当前是已有作者结构的给定构象性质任务，是否更换公开优化起点需按科学目标及维护流程单独处理，不由本次复制擅自改变。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [verification_report.md](../../../../docs/verification/group_3/paper_9ec32e81e2826041/verification_report.md)
- [source_row_audit.json](../../../../docs/verification/group_3/paper_9ec32e81e2826041/provenance/closeout_20260918/source_coordinate_repair/source_row_audit.json)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

SI p3 PBE0-D3BJ/6-311+G**方法、Tables S1/S2 pp13–15、Table S7 p21。

实际修复：明确主量为含D3BJ的源协议、气相300K/1atm harmonic Gibbs；其他方法仅作另报控制。区分身份与驻点两个过程项，绑定两个不同构象。AR仅去掉两份重复文件名，coplanar.xyz和perpendicular.xyz完整保留。

验证适用性：SI不含色散为+4.8，不能把任意方法结果强行按近等能评分；现已明示源主协议，不新增−0.1硬容差。构象名称定义给定比较对象，不要求独立发现其几何。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `ar_process_inputs` | Two uniquely labeled 80-atom C35H43NZn conformers have consistent chemical identity, charge 0, multiplicity 1 and input-to-result mapping. | 两构象各234正模，G为−3191.525824/−3191.525806 Eh，差−0.047258993 kJ/mol；对应SI含色散−0.1。 |
| `ar_process_validation` | Both distinct conformers are optimized minima with frequency evidence and consistently computed primary-protocol Gibbs energies at 300 K. | 两构象各234正模，G为−3191.525824/−3191.525806 Eh，差−0.047258993 kJ/mol；对应SI含色散−0.1。 |
| `ar_result_delta` | The signed difference G_coplanar − G_perpendicular in kJ mol−1 is computed from two traceable, like-defined Gibbs energies. Missing calculations do not earn this result by supplying a failure explanation. | 两构象各234正模，G为−3191.525824/−3191.525806 Eh，差−0.047258993 kJ/mol；对应SI含色散−0.1。 |
| `ar_final_conclusion` | The primary PBE0-D3BJ/6-311+G(d,p), 300 K gas-phase harmonic Gibbs comparison supports near-isoenergetic conformers. Check the signed subtraction and distinct optimized identities; do not apply this claim blindly to dispersion-free control calculations. | 两构象各234正模，G为−3191.525824/−3191.525806 Eh，差−0.047258993 kJ/mol；对应SI含色散−0.1。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_ar_process_inputs` → `ar_process_inputs`；读取 `$.structures[*].label, $.structures[*].input_file, $.structures[*].input_validation`。
- `r_ar_process_validation` → `ar_process_validation`；读取 `$.structures[*].stationary_point, $.structures[*].method, $.structures[*].free_energy`。
- `r_ar_result_delta` → `ar_result_delta`；读取 `$.comparison`。
- `r_ar_final_conclusion` → `ar_final_conclusion`；读取 `$.conclusion, $.comparison, $.structures`。

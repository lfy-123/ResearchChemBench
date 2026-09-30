# 已验证成功计算过程：paper_72822e4ddb5d9b11 / autonomous_research

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 5；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_5.md)
- [正文](../../../../papers/paper_72822e4ddb5d9b11/documents/main.pdf)；[补充材料](../../../../papers/paper_72822e4ddb5d9b11/documents/supplementary_001.pdf)
- [实算核查记录](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/report/closure_audit.json)；[历史结构化结果](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_autonomous_research/paper_72822e4ddb5d9b11/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_autonomous_research/paper_72822e4ddb5d9b11/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

固定 complex4、165原子、中性，比较singlet/triplet两个自旋态。SI pp10–11规定几何优化和电子结构用ORCA、B3LYP/BP86、Ni及第一配位层Cl1/Cl2/N1/N2/C1/C2用def2-TZVP，其余def2-SVP；本链采用允许的B3LYP分支，不冒充BP86。源坐标见SI pp99–100。

真实 ORCA6.1.1、B3LYP、DEFGRID3、VeryTightSCF；TZVP原子索引为1、3、5、7、9、49、59（1-based，按实际输入）。主比较为电子能差，不是G或TDDFT/SMD甲苯子题；不把论文其他方法直接混入这一子任务。

## 3. 成功计算链与结果

正确SI原子身份（早期无效元素0已按O修复） → singlet甲基扭转后独立优化得到真实最低点 → 同一几何Hessian → triplet用相同网格/基组Opt+Hessian → 同原子图、配位第一层及状态核对 → 同方法电子能差。

singlet优化日志与其后独立Hessian是两个文件，不能因为Hessian日志没有Opt步骤而误判“未优化”。两个最终Hessian各495模，含6个整体零模，其余全正，最低有效振动为8.698285/9.178230 cm⁻¹。triplet `<S²>=2.063319`，如实保留；singlet为闭壳层。

| 状态 | 用于比较的 E，Eh |
|---|---:|
| singlet（最终Hessian点） | −5967.657038894920 |
| triplet | −5967.605693210459 |

`(Etriplet−Esinglet)×627.5094740631 = +32.219903 kcal/mol`，singlet明显更低。SI TableS1 的B3LYP由表内能量差得31.4，BP86为25.1；本次不是精确复现31.4，更不能称为复现25.1。正文支持triplet高于20，当前evaluator要求正gap及singlet最低，实算满足。

成功singlet优化34335.324s、独立Hessian46070.673s、tripletOpt/Hessian113182.348s，共约53.7745h elapsed之和，不代表并行日历时长。早期带负频的结构未作为最低点，也不是简单删掉负频；后续有效几何和Hessian替代该分支，历史日志仍保存。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| singlet_state optimization | [输入](../../../../runs/hold_verification/group_5/torsion_restart_20260918/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_methyl_torsion20_minus_orbital_resume_20260918/20260918T095757_594190_343/input.inp) / [输出](../../../../runs/hold_verification/group_5/torsion_restart_20260918/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_methyl_torsion20_minus_orbital_resume_20260918/20260918T095757_594190_343/orca_stdout.log) | -5967.657035602952 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| singlet_state Hessian | [输入](../../../../runs/hold_verification/group_5/complex4_endpoint_20260919/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_singlet_torsion_minimum_hessian_20260919/20260919T080601_476816_187/input.inp) / [输出](../../../../runs/hold_verification/group_5/complex4_endpoint_20260919/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_singlet_torsion_minimum_hessian_20260919/20260919T080601_476816_187/orca_stdout.log) | -5967.65703889492 / -5966.42074644 | 495 模；负模 无；最低正频 8.7 cm⁻¹；日志正常结束 |
| triplet_state optimization | [输入](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_triplet_matched_grid_stationarity_20260921/20260921T065101_137993_188/input.inp) / [输出](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_triplet_matched_grid_stationarity_20260921/20260921T065101_137993_188/orca_stdout.log) | -5967.605693210459 / -5966.37414445 | 495 模；负模 无；最低正频 9.18 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `singlet_state optimization`：`! B3LYP def2-SVP VeryTightSCF DEFGRID3 VeryTightOpt MOREAD`。
- `singlet_state Hessian`：`! B3LYP def2-SVP VeryTightSCF DEFGRID3 Freq MOREAD`。
- `triplet_state optimization`：`! B3LYP def2-SVP VeryTightSCF DEFGRID3 TightOpt Freq MOREAD`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_process_states` | Neutral complex 4 is compared in multiplicities 1 and 3 with consistent energies and state-specific convergence and stationarity evidence. | 165原子中性1/3两态，同网格及混合基组，优化与Hessian关联；495模无负频。 |
| 关键点 `kp_result_gap` | The triplet is substantially higher in energy than the closed-shell singlet. | Etriplet−Esinglet=+32.219903 kcal/mol，满足正gap与singlet更低，不新增数字硬靶。 |
| 结论 `c_final_ground_state` | Validated state ordering supports a closed-shell singlet ground-state interpretation for complex 4. | 指定两态比较支持闭壳层singlet解释，且量级与正文>20/B3LYP31.4一致。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_process` | `$.states.singlet_state, $.states.triplet_state`；Named singlet/triplet calculations, consistent comparison, convergence and state-specific stationarity evidence are present. | `kp_process_states`：165原子中性1/3两态，同网格及混合基组，优化与Hessian关联；495模无负频。 |
| `r_gap` | `$.status, $.conclusion.claim, $.conclusion.limitations`；Completed output has singlet lower and positive gap; bounded failure has no fabricated gap and a specific limitation. | `kp_result_gap`：Etriplet−Esinglet=+32.219903 kcal/mol，满足正gap与singlet更低，不新增数字硬靶。 |
| `r_final` | `$.conclusion.claim, $.conclusion.validation_summary, $.conclusion.limitations`；Final conclusion connects validated ordering to the singlet interpretation and states limitations. | `c_final_ground_state`：指定两态比较支持闭壳层singlet解释，且量级与正文>20/B3LYP31.4一致。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

两模式的指定自旋态比较和最终结论可计算。没有把该子问题扩展为其他化合物、所有自旋态的全局搜索、NICS/ACID或TDDFT。当前正gap标准不应被误写成新增的32.219903硬目标。

发布整理仍需单独检查作者优化结构作为固定物性对象输入的边界；本轮是保存既有源任务和证据，不宣称完成无泄漏发布审计，也不改动公开几何或评分。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [supplementary_verification.md](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/report/supplementary_verification.md)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

SI pp10–11两态分别优化/频率及分层基组、正文p4，SI复合物4坐标pp99–100。

实际修复：保留给定复合物的两态性质比较；明确分别弛豫后的电子Et−Es而非垂直或G能差；完成必须有两电子能/gap/lower_state，评分绑定实际数值与证据，不按免责声明给分。

验证适用性：不将B3LYP32.22声称为BP8625.1逐值复现；现行只评分方向，不新增数值容差或额外电子态搜索。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_process_states` | Both named states have explicit multiplicities, methods, relaxed electronic energies, convergence and stationarity evidence. Credit only states actually established; a failure explanation cannot replace missing state evidence. | ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。 |
| `kp_result_gap` | Completed output identifies singlet as lower with a positive gap; bounded failure does not fabricate a gap. | ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。 |
| `c_final_ground_state` | Traceable relaxed-state electronic energies give a positive Et−Es gap and lower closed-shell singlet in this two-state comparison. | ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_process` → `kp_process_states`；读取 `$.states.singlet_state, $.states.triplet_state`。
- `r_gap` → `kp_result_gap`；读取 `$.status, $.states, $.gap_kcal_mol, $.lower_state, $.conclusion.claim`。
- `r_final` → `c_final_ground_state`；读取 `$.conclusion.claim, $.states, $.gap_kcal_mol, $.lower_state`。

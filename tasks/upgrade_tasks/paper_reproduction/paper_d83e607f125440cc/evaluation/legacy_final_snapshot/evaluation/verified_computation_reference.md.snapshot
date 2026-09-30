# 已验证成功计算过程：paper_d83e607f125440cc / paper_reproduction

归档日期：2026-09-26。原有效计算链保留；2026-09-27的提交契约修复及当前验证适用性见第8节，较早对应快照见第7节。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 1；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_1.md)
- [正文](../../../../papers/paper_d83e607f125440cc/documents/main.pdf)；[补充材料](../../../../papers/paper_d83e607f125440cc/documents/supplementary_001.pdf)
- [实算核查记录](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/b3lyp_bde_closure_20260922/raw_results.json)；[历史结构化结果](../../../../docs/verification/group_1/paper_d83e607f125440cc/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_paper_reproduction/paper_d83e607f125440cc/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_paper_reproduction/paper_d83e607f125440cc/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

目标仅为气相 2g 自由基阳离子的最低点、硫 Hirshfeld 自旋，以及与 2a 的苄位 C–H 断键能比较。2g 为 C8H10OS、20 原子、+1/doublet；2a 为 C8H10O2、20 原子、+1/doublet。2g 原子序中 S9，选择苄位 C12–H13（1-based；原 JSON 为 0-based 11–12），不是 S–CH3 上的 C–H。删除该苄位 H 得 19 原子的 +1/singlet 片段；另计算中性 doublet H 原子。

SI §S6、Tables S8/S10/S13/S16 及 §S7 坐标是来源。实际路线为 Gaussian16 的 B3LYP/6-311+G(d)，气相；两个母体与两个片段各自 Opt/Freq，H 原子单点，2g 最低点另外做 `Pop=Hirshfeld`。SI 电子能表头的“HF”不能解释为本任务使用 Hartree–Fock；方法段明确是 B3LYP。实际采用电子断键能，不加 ZPE/热焓/自由能修正。

## 3. 成功计算链与结果

2g 使用 SI 知情母体结构；2a 按任务给出的化学身份用 RDKit ETKDGv3（seed=20260830）及 MMFF 构建，不冒称是作者同一精确构象。两母体各自优化/频率 → 按同一苄位定义生成并优化脱 H 片段 → 同层级 H 单点 → 2g 最低点 Hirshfeld 分析 → 电子能差及同口径比较。所有分子端点分别为 54/54/51/51 个正频率；H 原子没有分子振动频率，不应误记为缺少频率。

| 量 | 实际计算 | 当前 evaluator | 判断 |
|---|---:|---:|---|
| 硫 Hirshfeld 自旋 | 0.400976 | 0.401 ± 0.05 | 满足 |
| 2g BDE，kJ/mol | 198.527743115 | 198.5 ± 8 | 满足 |
| 2a BDE，kJ/mol | 172.594617223 | 173.7 ± 8 | 满足 |
| 2g−2a，kJ/mol | +25.933125892 | 2g 更高 | 支持相同方向 |

公式：`BDE=[E(fragment,+1,singlet)+E(H,0,doublet)−E(parent,+1,doublet)]×2625.499638`，能量输入为 Hartree。下表保留实际原始总能；G 虽可由频率输出读出，但不用于这一 BDE。所需唯一有效 Gaussian 步骤 elapsed 合计 2685.8 s，非日历工期，旧错误 HF 分支不纳入。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| 2g_parent | [输入](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/gaussian_batch/2g_b3lyp_6311plus_optfreq_hpc_c5f90a1f/input.com) / [输出](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/gaussian_batch/2g_b3lyp_6311plus_optfreq_hpc_c5f90a1f/gaussian.log) | -784.11750352 / -783.993744 | 54 模；负模 无；最低正频 59.9295 cm⁻¹；日志正常结束 |
| 2a_parent | [输入](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/gaussian_batch/2a_b3lyp_6311plus_optfreq_hpc_d2c8d191/input.com) / [输出](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/gaussian_batch/2a_b3lyp_6311plus_optfreq_hpc_d2c8d191/gaussian.log) | -461.12812483 / -460.99961 | 54 模；负模 无；最低正频 59.2978 cm⁻¹；日志正常结束 |
| 2g_fragment | [输入](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_bde_repair_20260921/2g_B3LYP_6311plus_BDE_repair_20260921/input.com) / [输出](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_bde_repair_20260921/2g_B3LYP_6311plus_BDE_repair_20260921/gaussian.log) | -783.539732366 / -783.423321 | 51 模；负模 无；最低正频 71.9931 cm⁻¹；日志正常结束 |
| 2a_fragment | [输入](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_bde_repair_20260921/2a_B3LYP_6311plus_BDE_repair_20260921/input.com) / [输出](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_bde_repair_20260921/2a_B3LYP_6311plus_BDE_repair_20260921/gaussian.log) | -460.560231082 / -460.438608 | 51 模；负模 无；最低正频 70.4795 cm⁻¹；日志正常结束 |
| H | [输入](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_bde_repair_20260921/H_B3LYP_6311plus_BDE_repair_20260921/input.com) / [输出](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_bde_repair_20260921/H_B3LYP_6311plus_BDE_repair_20260921/gaussian.log) | -0.50215593009 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| spin | [输入](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/gaussian_batch/2g_hirshfeld_b3lyp_sp_hpc_604143ae/input.com) / [输出](../../../../docs/verification/group_1/paper_d83e607f125440cc/artifacts/gaussian_batch/2g_hirshfeld_b3lyp_sp_hpc_604143ae/gaussian.log) | -784.11750352 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `2g_parent`：`#p B3LYP/6-311+G(d) Opt=(CalcFC,MaxCycles=180) Freq NoSymm SCF=(XQC,Tight,MaxCycle=512)`。
- `2a_parent`：`#p B3LYP/6-311+G(d) Opt=(CalcFC,MaxCycles=180) Freq NoSymm SCF=(XQC,Tight,MaxCycle=512)`。
- `2g_fragment`：`#p B3LYP/6-311+G(d) Opt=(CalcFC,Tight,MaxCycles=180) Freq NoSymm SCF=(XQC,Tight,MaxCycle=512)`。
- `2a_fragment`：`#p B3LYP/6-311+G(d) Opt=(CalcFC,Tight,MaxCycles=180) Freq NoSymm SCF=(XQC,Tight,MaxCycle=512)`。
- `H`：`#p B3LYP/6-311+G(d) SP NoSymm SCF=(XQC,Tight,MaxCycle=512)`。
- `spin`：`#p B3LYP/6-311+G(d) SP Pop=Hirshfeld NoSymm SCF=(XQC,Tight,MaxCycle=512)`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_minimum` | The optimized 4-(methylsulfanyl)benzyl alcohol radical cation is validated as a stationary minimum by vibrational analysis. | 2g母体54正频，最低59.9295 cm⁻¹；四个分子端点均无虚频。 |
| 关键点 `kp_spin` | The unique sulfur atom carries substantial Hirshfeld spin density in 2g•+. | Hirshfeld硫0.400976；0.401±0.05范围内。 |
| 关键点 `kp_bde` | The benzylic C–H BDE of 2g is higher than that of the methoxy analogue under the defined comparison. | 2g/2a电子BDE198.527743/172.594617 kJ/mol；两项均在原±8内，2g高25.933126。 |
| 结论 `conclusion_mechanism` | Within the computed gas-phase descriptor boundary, the result supports the authors' qualitative explanation of the methylsulfanyl substrate's anomalous oxidation behavior. | 硫自旋局域及更高2g苄位BDE提供与氧化行为相关的描述符支持，不据此证明完整机理。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_minimum` | `$.minimum_validation.validation_statement`；Report zero imaginary frequencies (or explicitly diagnose a failure and do not claim a minimum). | `kp_minimum`：2g母体54正频，最低59.9295 cm⁻¹；四个分子端点均无虚频。 |
| `r_spin` | `$.spin_density.sulfur_hirshfeld`；0.401 ± 0.05 dimensionless Hirshfeld spin population | `kp_spin`：Hirshfeld硫0.400976；0.401±0.05范围内。 |
| `r_bde2g` | `$.bde_2g.value`；198.5 ± 8.0 kJ/mol | `kp_bde`：2g/2a电子BDE198.527743/172.594617 kJ/mol；两项均在原±8内，2g高25.933126。 |
| `r_bde2a` | `$.bde_2a_comparator.value`；173.7 ± 8.0 kJ/mol | `kp_bde`：2g/2a电子BDE198.527743/172.594617 kJ/mol；两项均在原±8内，2g高25.933126。 |
| `r_conclusion` | `$.conclusion`；A bounded conclusion states that sulfur localization and higher 2g BDE support, but do not alone prove, the qualitative explanation. | `conclusion_mechanism`：硫自旋局域及更高2g苄位BDE提供与氧化行为相关的描述符支持，不据此证明完整机理。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

科学结果支持两个当前模式的三个必评关键点和各自最终结论。历史 group1 资格记录只登记 PR，本次对 AR 重新做了同对象、同数值、同结论范围的适用性检查；没有把 PR 的“独立计划”伪写为真实 AR 盲测轨迹。支持的是任务科学子问题可完成，不是全氧化机理或 agent 自主发现成功率。

待后续整理：私有 `paper_route.md` 仍有 HF-based BDE 旧表述，须与真实 B3LYP 路线同步。历史 `report/results.json` 符合 PR 的提交 schema，但不符合 AR 成功分支的提交 schema：缺少 `investigation`，其必需字段为 `plan / models_or_conformers / coverage / stopping_rule`。现有数值结果满足 AR 三条 numeric 规则，只能作为相同科学子问题的验证证据，不能把独立规划字段补造后宣称完成了 AR 盲测。本档案不是 AR 结果提交；本轮保留源任务、评分和公开数据。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [b3lyp_descriptor_closure_audit_20260922.json](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/b3lyp_descriptor_closure_audit_20260922.json)
- [bde_input_staging.json](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/bde_input_staging.json)
- [prepare_comparator_and_bde_inputs.py](../../../../docs/verification/group_1/paper_d83e607f125440cc/provenance/prepare_comparator_and_bde_inputs.py)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

SI S6、Tables S8/S10/S13/S16，PDF pp34–36；正文的氧化机理解释。

实际修复：保留2g已知母体输入和2a自行构建；明确气相绝热电子断键能，+1 doublet母体/+1 singlet去氢片段/中性doublet H，排除主结果中的ZPE/热修正；修复HF方法误写、最低点字段绑定和普通停止/免责声明门槛。

验证适用性：PR历史结果可直接匹配新schema；AR旧结果缺investigation，只作为同一科学量的验证证据，不补造自主规划。格式测试里的AR investigation是明确标注的synthetic外壳，不是新验证。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_minimum` | Frequency evidence with zero imaginary modes, or justified equivalent stationarity/full-internal-curvature evidence, establishes the vacuum 2g•+ minimum. | 历史实际使用频率分支：2g母体54个正频、无虚频；没有将等效分支格式样例当成计算验证。 |
| `kp_spin` | Hirshfeld spin density on sulfur is 0.401 (dimensionless atomic spin population). | 母体/片段四份OptFreq、H单点和Hirshfeld单点共6步骤；S=0.400976，2g/2a电子BDE=198.527743115/172.594617223 kJ/mol。 |
| `kp_bde` | 2g BDE is 198.5 kJ mol−1 and 2a BDE is 173.7 kJ mol−1, so 2g is higher by 24.8 kJ mol−1. | 母体/片段四份OptFreq、H单点和Hirshfeld单点共6步骤；S=0.400976，2g/2a电子BDE=198.527743115/172.594617223 kJ/mol。 |
| `conclusion_mechanism` | Substantial sulfur Hirshfeld spin population and a higher electronic 2g benzylic C–H dissociation energy than 2a are correctly calculated and interpreted as descriptor-level oxidation evidence. | 母体/片段四份OptFreq、H单点和Hirshfeld单点共6步骤；S=0.400976，2g/2a电子BDE=198.527743115/172.594617223 kJ/mol。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_minimum` → `kp_minimum`；读取 `$.minimum_validation, $.system`（2026-09-27统一两类证据分支，见第8节）。
- `r_spin` → `kp_spin`；读取 `$.spin_density.sulfur_hirshfeld`。
- `r_bde2g` → `kp_bde`；读取 `$.bde_2g.value`。
- `r_bde2a` → `kp_bde`；读取 `$.bde_2a_comparator.value`。
- `r_conclusion` → `conclusion_mechanism`；读取 `$.conclusion, $.comparison, $.method, $.spin_density, $.bde_2g, $.bde_2a_comparator`。

## 8. 2026-09-27 极小点证据契约修复后的适用性

再次核对SI S34（Section S6，频率验证极小点）及Table S10，历史2g母体Opt/Freq确实得到54个正频、无虚频。原始输入、日志和6步计算结果均未改；自旋0.400976及两BDE 198.527743115/172.594617223 kJ/mol继续支持现有数值目标。

原题面与r_minimum已允许等效极小点证据，但schema强制整数虚频数、kp_minimum只写频率，现已统一。旧的 `imaginary_frequencies` + `validation_statement` 频率格式继续兼容；等效分支使用 `validation_method=equivalent`、非空 `equivalent_evidence` 路径及论证，可以省略未计算的频率数。评分读取完整 `$.minimum_validation` 和 `$.system`，检查实际驻定性及全部内部自由度正曲率证据，不把优化收敛、声明文字或有限方向采样当成充分证明。PR题面误带的AR investigation句子已删除。

等效分支是原题面已有的benchmark接受方式，不声称论文或本地历史验证实际使用过该替代路线。历史验证继续是频率分支，原结构化结果无需改变即可提交；新增分支的合成格式样例只检验软件，不是新增科学验证。3个关键点、1个结论、数值靶/容差及输入数据均不变。

# 已验证计算参考：paper_1255ed42fa7e12ff / autonomous_research

核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/autonomous_research/paper_1255ed42fa7e12ff`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 4。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16 ωB97XD/6-311G(d,p)，TD 六个单重激发态、Root=1，CPCM acetonitrile，37 原子中性体系。三个 TS 各一个相关质子迁移虚频，六端点各 105 个正频率。以最低六根中的 S1 接受点审查路径。Se 反向仅采用旧路径 0–17 点，再接 EqSolv/IOp(9/49=5) 修复尾段；排除旧 18–62 点。方法见正文物理第 2–3 页，Table 1 在第 5 页；本次重新解析全部采用路径点的六根能量及 Root1 选择。

论文来源：[正文](../../../../papers/paper_1255ed42fa7e12ff/documents/main.pdf)；[SI](../../../../papers/paper_1255ed42fa7e12ff/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

三个 37 atom S1 enol 是明确给定的起始反应物，没有 keto/TS/IRC 答案。注释如实标明 SI 来源。需确认自由溶剂/方法选择与固定 CPCM 数值靶的有效答案范围；不因坐标来源于 SI 自动删除合法起点。

## 2. 有效计算链、结果与推导

ΔG‡=(G_TS−G_enol)×627.5094740631；k=(kBT/h)exp(−ΔG‡·4184/(RT))，T=298.15 K、kB=1.380649e−23 J/K、h=6.62607015e−34 J s、R=8.31446261815324 J mol⁻¹ K⁻¹。O/S/Se 势垒 13.426192707/7.703933813/6.661640577 kcal/mol；速率 894.941234/1.400359025e7/8.132903866e7 s⁻¹，均在原势垒 ±1、log10(k) ±0.25 容差内。采用前/反向点数为 O 73/101、S 68/121、Se 96/178；Se 18 点前缀+161 点尾段减一个共享连接点，连接 TD 能差约 2e−8 Eh。六根最低间隙依次 0.2334/0.3674/0.4484/0.0225/0.4653/0.0174 eV。只核验有限六根排序；没有波函数重叠连续性或非绝热动力学证明。

| 体系 | G_TS / Eh | G_enol / Eh | G_keto / Eh | ΔG‡ / kcal mol⁻¹ | k / s⁻¹ |
| --- | --- | --- | --- | --- | --- |
| O | -1156.9141480000 | -1156.9355440000 | -1156.9404270000 | 13.426192707 | 894.941234 |
| S | -1479.8982090000 | -1479.9104860000 | -1479.9203390000 | 7.703933813 | 14003590.3 |
| Se | -3483.2767700000 | -3483.2873860000 | -3483.3034960000 | 6.661640577 | 81329038.7 |

## 3. 当前必评关键点与结论覆盖

| 当前ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| p1 / process | Frequency validation establishes minima and one-imaginary-mode TS. | 3个相关单虚频TS+6个105正频最低点，S1态及模式证据。 | r1 |
| p2 / process | IRC connects enol and keto endpoints. | 六方向路径/终态，Se仅用有效前缀和修复尾段，所有采用点的六根排序复核。 | r2 |
| p3 / result | Barriers are reported for all three compounds. | 原G独立复算三势垒13.426193/7.703934/6.661641，均满足原±1。 | r3_O, r3_S, r3_Se |
| p4 / result | TST rates are reported at 298.15 K. | 298.15K普通TST公式复算三个k，原log10容差±.25；非动力学轨迹。 | r4_O, r4_S, r4_Se |

| 结论 ID / 当前角色 | 当前科学主张 | 证据和接受边界 |
| --- | --- | --- |
| c1 / final | Barrier ordering is O>S>Se and rate ordering is O<S<Se. | 第2节原始量推导及本表支持关键点：p1, p2, p3, p4。作者路线范围，不代表独立盲搜索。 |

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。Se 旧反向日志只采用 0–17 点，后段已排除。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | /O/TS; adopted_chain/8QBDY_O_ESIPT_TS_S1__retry_001 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_ESIPT_TS_S1__retry_001_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_ESIPT_TS_S1__retry_001_hpc20_p6/stdout.log) | [0, 1] | -1157.1345681100 | -1156.9141480000 | 105 / 1 / -1610.3462 | native normal |
| 2 | /O/paths/forward; adopted_chain/8QBDY_O_source_ts_lqa_forward_irc_20260915 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_source_ts_lqa_forward_irc_20260915_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_source_ts_lqa_forward_irc_20260915_hpc20_p6/stdout.log) | [0, 1] | -1157.1589078400 | — | — | native normal |
| 3 | /O/paths/reverse; adopted_chain/8QBDY_O_source_ts_lqa_reverse_irc_20260915 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_source_ts_lqa_reverse_irc_20260915_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_source_ts_lqa_reverse_irc_20260915_hpc20_p6/stdout.log) | [0, 1] | -1157.1626999600 | — | — | native normal |
| 4 | /O/endpoints/enol; adopted_chain/8QBDY_O_accepted_forward_irc_endpoint_s1_optfreq_20260922 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_accepted_forward_irc_endpoint_s1_optfreq_20260922_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_accepted_forward_irc_endpoint_s1_optfreq_20260922_hpc20_p6/stdout.log) | [0, 1] | -1157.1593027800 | -1156.9355440000 | 105 / 0 / 12.3788 | native normal |
| 5 | /O/endpoints/keto; adopted_chain/8QBDY_O_accepted_reverse_irc_endpoint_s1_optfreq_20260922 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_accepted_reverse_irc_endpoint_s1_optfreq_20260922_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_O_accepted_reverse_irc_endpoint_s1_optfreq_20260922_hpc20_p6/stdout.log) | [0, 1] | -1157.1643422000 | -1156.9404270000 | 105 / 0 / 20.3992 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 6 | /S/TS; adopted_chain/8QBDY_S_computed_scan_peak_ts_optfreq_20260918 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_hpc20_p6/stdout.log) | [0, 1] | -1480.1139902500 | -1479.8982090000 | 105 / 1 / -1304.8512 | native normal |
| 7 | /S/paths/forward; adopted_chain/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_forward_irc | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_forward_irc_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_forward_irc_hpc20_p6/stdout.log) | [0, 1] | -1480.1270868000 | — | — | native normal |
| 8 | /S/paths/reverse; adopted_chain/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_reverse_irc | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_reverse_irc_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_computed_scan_peak_ts_optfreq_20260918_reverse_irc_hpc20_p6/stdout.log) | [0, 1] | -1480.1417778800 | — | — | native normal |
| 9 | /S/endpoints/enol; adopted_chain/8QBDY_S_accepted_forward_irc_endpoint_s1_optfreq_20260922 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_accepted_forward_irc_endpoint_s1_optfreq_20260922_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_accepted_forward_irc_endpoint_s1_optfreq_20260922_hpc20_p6/stdout.log) | [0, 1] | -1480.1273847300 | -1479.9104860000 | 105 / 0 / 18.7768 | native normal |
| 10 | /S/endpoints/keto; adopted_chain/8QBDY_S_accepted_reverse_irc_endpoint_s1_optfreq_20260922 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_accepted_reverse_irc_endpoint_s1_optfreq_20260922_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_S_accepted_reverse_irc_endpoint_s1_optfreq_20260922_hpc20_p6/stdout.log) | [0, 1] | -1480.1421676300 | -1479.9203390000 | 105 / 0 / 18.985 | native normal |
| 11 | /Se/TS; adopted_chain/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_hpc20_p6/stdout.log) | [0, 1] | -3483.4903605300 | -3483.2767700000 | 105 / 1 / -1218.5164 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 12 | /Se/paths/forward; adopted_chain/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_forward_irc | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_forward_irc_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_forward_irc_hpc20_p6/stdout.log) | [0, 1] | -3483.5009827600 | — | — | native normal |
| 13 | /Se/paths/reverse; adopted_chain/8QBDY_Se_reverse_p017_lowest_root_tail_20260925 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_reverse_p017_lowest_root_tail_20260925_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_reverse_p017_lowest_root_tail_20260925_hpc20_p6/stdout.log) | [0, 1] | -3483.5233390800 | — | — | native normal |
| 14 | /Se/endpoints/enol; adopted_chain/8QBDY_Se_accepted_forward_irc_endpoint_s1_optfreq_20260922 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_accepted_forward_irc_endpoint_s1_optfreq_20260922_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_accepted_forward_irc_endpoint_s1_optfreq_20260922_hpc20_p6/stdout.log) | [0, 1] | -3483.5012949400 | -3483.2873860000 | 105 / 0 / 16.6061 | native normal |
| 15 | /Se/endpoints/keto; adopted_chain/8QBDY_Se_corrected_lowest_tail_endpoint_s1_optfreq_20260926 | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_corrected_lowest_tail_endpoint_s1_optfreq_20260926_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_corrected_lowest_tail_endpoint_s1_optfreq_20260926_hpc20_p6/stdout.log) | [0, 1] | -3483.5234950600 | -3483.3034960000 | 105 / 0 / 11.332 | native normal |
| 16 | adopted_chain/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_reverse_irc | [输入](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_reverse_irc_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/hpc_runs/8QBDY_Se_computed_prefix_peak_ts_optfreq_20260919_reverse_irc_hpc20_p6/stdout.log) | [0, 1] | -3483.5043914800（采用点17；非日志末段） | — | — | native normal；仅0–17点有效 |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) Opt=(TS,CalcFC,NoEigenTest,MaxCycles=300) Freq SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 2 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) IRC=(LQA,CalcFC,Forward,MaxPoints=100,StepSize=5) SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 3 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) IRC=(LQA,CalcFC,Reverse,MaxPoints=100,StepSize=5) SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 4, 5, 9, 10, 14 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) Opt=(CalcFC,Tight,MaxCycles=300,MaxStep=3) Freq SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 6, 11 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) Opt=(TS,CalcFC,NoEigenTest,Tight,MaxStep=5,MaxCycles=300) Freq SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 7, 12 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) IRC=(LQA,CalcFC,Forward,MaxPoints=120,StepSize=5,VeryTight) SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 8, 16 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1) IRC=(LQA,CalcFC,Reverse,MaxPoints=120,StepSize=5,VeryTight) SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 13 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1,EqSolv) IRC=(Downhill,LQA,CalcFC,NoGradStop,StepSize=2,MaxPoints=160,VeryTight) IOp(9/49=5) SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |
| 15 | `#p wB97XD/6-311G(d,p) TD=(NStates=6,Root=1,EqSolv) Opt=(CalcFC,Tight,MaxCycles=300,MaxStep=3) Freq IOp(9/49=5) SCRF=(CPCM,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512)` |

## 5. 模型、连接与后处理原始出处

- [provenance/repaired_path_closeout_20260928/result.json](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/provenance/repaired_path_closeout_20260928/result.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/report/results.json)
- [明确截取的 Se 原反向有效前缀 0–17](../../../../docs/verification/group_4/paper_1255ed42fa7e12ff/provenance/repaired_path_closeout_20260928/Se_reverse_accepted_prefix_0_to_17.log)

## 6. 本次核查与未认证事项

本包新增参考前 package validator 为 passed，实际策略 `dual_axis_100.v1`；真实历史 report 的实际 output runner 格式检查为 False。这些是软件状态，不能替代本文件的科学判断。

当前格式诊断：schema_validation: 'hypotheses' is a required property。

本轮未新算电子结构、未提交/停止 HPC；qRRHO 重读及原始数值/几何/根序/拓扑重提取为已有结果后处理。源图/构型/CIP 审计沿用已定位原证据并核对适用性，不冒称全部重新执行。完整采用链记录在本文件，删除辅助 task_provenance 不应使来源失联。公开包只允许 agent_input；部署侧父目录、容器挂载及网络隔离本轮未实测。维护问题不通过改写 reference 变成 gold。

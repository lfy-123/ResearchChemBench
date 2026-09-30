# 已验证计算参考：paper_3c89b494a1645491 / autonomous_research

核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/autonomous_research/paper_3c89b494a1645491`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 4。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**资格边界：真实计算及有限模型定性分类已核实；两项 DI 超出原始字面区间。登记为语义 QUALIFIED 不等于所有定量必评项已严格完成；接受精度须按维护报告确认。此参考如实记录已证实部分，不出具无条件 PASS。**

## 1. 论文、模型与采用协议

Gaussian 16 C.01 BP86-D3BJ/def2-TZVPP，Au 60 核 ECP；184 原子 C76H88Au4N16、+4 单重态、546 正频率。由 CCDC 2500223 晶体删除阴离子/溶剂，保留完整四配体及环状 Au 标号。fchk 导出后 Multiwfn 2026.7.15 计算四个 BCP、八条连接路径、0.20/0.10 Bohr 两档 DI 网格；源用 G16 C.02/Multiwfn 3.8。SI 物理第 27 页方法、第 28 页拓扑图、第 29 页 Table S2，正文第 4 页近似 DI 区间及分类。软件/网格差异已知，但不能无证据认定其解释所有 DI 差异。

论文来源：[正文](../../../../papers/paper_3c89b494a1645491/documents/main.pdf)；[SI](../../../../papers/paper_3c89b494a1645491/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

真实 CIF 为 CCDC 2500223，保留完整出处/占据/晶胞及原子标签；system_definition 指定仅移除阴离子和溶剂、+4 单重态及四边。实验晶体是任务给定结构证据，不是计算 BCP/DI 答案，DOI/CCDC 号不单独构成答案泄露；未向 agent 提供 fchk 或拓扑计算结果。

## 2. 有效计算链、结果与推导

四 BCP 的 ∇²ρ>0、H<0、|V|/G=1.165961–1.167434；平均 ρ=0.036440290765，在现行 0.036475±0.001 内。由原始 CPprop 与两份 LIDI 矩阵重新提取，0.10-Bohr DI=0.37506794/0.37627436/0.37365572/0.37591119；对应 0.20-Bohr=0.37548906/0.37717135/0.37501872/0.37676476。细网格 Au 原子 1/2/3/4→basin 91/123/114/57，不能按 basin 顺序误认原子。BCP 5/6/7/8 各有两条 94 点路径，末点与对应 Au 距离 <7e−7 Å。定性上支持以闭壳层为主且有少量共享的 metallophilic 接触。两项原始 DI 不在字面 [0.374,0.376]；按正文三位小数显示为 .375/.376/.374/.376，但这不是新容差。SI 八位值及细微接触排序未精确复现，两档网格差也不是严格误差界。登记的有限模型语义 PASS 与当前 PR 关键点窄区间措辞存在需确认的接受精度边界；本次不把它写成全部定量点严格通过。

| 接触 | BCP | rho | laplacian | ELF | H | V | G | abs(V)/G | DI 0.10 | DI字面区间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Au1-Au2 | 5 | 0.0363852360 | 0.0858782724 | 0.1656989989 | -0.0042852040 | -0.0300079064 | 0.0257227024 | 1.1665922956 | 0.37506794 | True |
| Au2-Au3 | 6 | 0.0365799424 | 0.0864129484 | 0.1661669426 | -0.0043379921 | -0.0302466950 | 0.0259087030 | 1.1674337799 | 0.37627436 | False |
| Au3-Au4 | 7 | 0.0362731183 | 0.0856104924 | 0.1653478189 | -0.0042524702 | -0.0298757508 | 0.0256232805 | 1.1659611944 | 0.37365572 | False |
| Au4-Au1 | 8 | 0.0365228663 | 0.0862866978 | 0.1659748235 | -0.0043200070 | -0.0301792970 | 0.0258592900 | 1.1670582199 | 0.37591119 | True |

## 3. 当前必评关键点与结论覆盖

| 当前ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| ar_process_hypothesis / process | The submission proposes at least one plausible electronic explanation and tests it with a reproducible calculation on the pinned +4 singlet cluster. | 作者路线做了结构/拓扑/双网格检验；历史report没有事前自主hypotheses，未认证AR探索。 | ar_r1 |
| ar_process_validation / process | The submitted investigation validates identity/state, geometry or stationary-state justification, four named edge contacts and four BCPs before drawing a bonding conclusion. | 184atom +4/1最低点、546正频，四BCP八条真实路径。 | ar_r2 |
| ar_result_aim / result | The independent quantitative analysis supports the source-observed Au···Au contact topology and its characteristic AIM/DI pattern. | rho及定性AIM模式支持；两项DI字面区间越界，当前精度接受边界待确认。 | ar_r3 |
| ar_result_class / result | The final interpretation classifies the four contacts as metallophilic and predominantly closed-shell with minor shared-shell contribution, while stating model limitations. | 四个1<\|V\|/G<2、正laplacian、负H及非零DI，支持有限模型成键分类。 | ar_r4 |

| 结论 ID / 当前角色 | 当前科学主张 | 证据和接受边界 |
| --- | --- | --- |
| ar_final / final | Independent calculations support predominantly closed-shell metallophilic Au···Au interactions with measurable electron sharing in the four-edge Au4 core, subject to finite-cluster and method limitations. | 定性分类由四BCP/DI支持；DI精确窄区间未全部命中，见第2节。AR事前hypotheses未验证。 |

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Au1_optimization_frequency | [输入](../../../../docs/verification/group_4/paper_3c89b494a1645491/provenance/local_full_route_gates_20260913/au1_cation_bp86_def2tzvpp_optfreq_scratch_repair/input.com) / [原始输出](../../../../docs/verification/group_4/paper_3c89b494a1645491/provenance/local_full_route_gates_20260913/au1_cation_bp86_def2tzvpp_optfreq_scratch_repair/stdout.log) | [4, 1] | -4369.6195943200 | -4368.2827060000 | 546 / 0 / 7.4089 | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1 | `#p BP86/def2TZVPP EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512)` |

## 5. 模型、连接与后处理原始出处

- [provenance/au1_closeout_20260928/result.json](../../../../docs/verification/group_4/paper_3c89b494a1645491/provenance/au1_closeout_20260928/result.json)
- [provenance/au1_closeout_20260928/geometry_review.json](../../../../docs/verification/group_4/paper_3c89b494a1645491/provenance/au1_closeout_20260928/geometry_review.json)
- [provenance/au1_closeout_20260928/topology_review.json](../../../../docs/verification/group_4/paper_3c89b494a1645491/provenance/au1_closeout_20260928/topology_review.json)
- [provenance/au1_closeout_20260928/DI_discrepancy_review.json](../../../../docs/verification/group_4/paper_3c89b494a1645491/provenance/au1_closeout_20260928/DI_discrepancy_review.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../docs/verification/group_4/paper_3c89b494a1645491/report/results.json)
- [au1_20260928/export.json](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/export.json)
- [au1_20260928/topology_complete/CPprop.txt](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/topology_complete/CPprop.txt)
- [au1_20260928/topology_complete/CPs.txt](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/topology_complete/CPs.txt)
- [au1_20260928/topology_complete/paths.txt](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/topology_complete/paths.txt)
- [au1_20260928/topology_complete/stdout](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/topology_complete/stdout)
- [au1_20260928/di_020_hpc20/stdin](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_020_hpc20/stdin)
- [au1_20260928/di_020_hpc20/stdout](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_020_hpc20/stdout)
- [au1_20260928/di_020_hpc20/settings.ini](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_020_hpc20/settings.ini)
- [au1_20260928/di_020_hpc20/LIDI.txt](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_020_hpc20/LIDI.txt)
- [au1_20260928/di_020_hpc20/exit_code](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_020_hpc20/exit_code)
- [au1_20260928/di_010_hpc20/stdin](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_010_hpc20/stdin)
- [au1_20260928/di_010_hpc20/stdout](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_010_hpc20/stdout)
- [au1_20260928/di_010_hpc20/settings.ini](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_010_hpc20/settings.ini)
- [au1_20260928/di_010_hpc20/LIDI.txt](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_010_hpc20/LIDI.txt)
- [au1_20260928/di_010_hpc20/exit_code](../../../../docs/verification/group_4/paper_3c89b494a1645491/au1_20260928/di_010_hpc20/exit_code)

## 6. 本次核查与未认证事项

本包新增参考前 package validator 为 passed，实际策略 `dual_axis_100.v1`；真实历史 report 的实际 output runner 格式检查为 False。这些是软件状态，不能替代本文件的科学判断。

当前格式诊断：schema_validation: 'hypotheses' is a required property。

本轮未新算电子结构、未提交/停止 HPC；qRRHO 重读及原始数值/几何/根序/拓扑重提取为已有结果后处理。源图/构型/CIP 审计沿用已定位原证据并核对适用性，不冒称全部重新执行。完整采用链记录在本文件，删除辅助 task_provenance 不应使来源失联。公开包只允许 agent_input；部署侧父目录、容器挂载及网络隔离本轮未实测。维护问题不通过改写 reference 变成 gold。

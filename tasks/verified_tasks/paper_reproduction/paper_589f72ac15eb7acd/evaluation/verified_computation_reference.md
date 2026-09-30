# 已验证计算参考：paper_589f72ac15eb7acd / paper_reproduction

> 2026-09-29 修后同步：任务修复和当前评分映射见第 3、6 节；全部仍在 verified_tasks，未获迁移确认。
核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/paper_reproduction/paper_589f72ac15eb7acd`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 2。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16 C.01，CAM-B3LYP/CEP-31G，D3；孤立气相、总电荷 0，HS 多重度 5、LS 多重度 1。正文 Table 2（main PDF 物理第 8 页）报告 −34/−28/−21 kJ mol⁻¹。验证采用作者 cis 起始框架，逐态重新优化/频率；不是把作者能量当输出。与作者 G16 A.03 存在版本差异。

论文来源：[正文](../../../../../papers/paper_589f72ac15eb7acd/documents/main.pdf)；[SI](../../../../../papers/paper_589f72ac15eb7acd/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

公开输入只有中立系统定义，C21H19N5S、三种辅助配体、cis 与 0/(5,1) 齐全，未含作者末态坐标或参考能量。来源旧 C21/C22 疑点已按当前真实身份更正，不照抄旧待修列表。

## 2. 有效计算链、结果与推导

六态 E(HS)−E(LS)×2625.499638 分别为 −33.764571、−28.500043、−21.415006 kJ/mol。三者均 HS 电子能较低；C3>C2>C1 是 LS 相对稳定化趋势，不是 C3 的 LS 已成为基态。LPh-TDA 为 C21H19N5S，两个辅助配体经 N 配位，cis 六 Fe–N 位点保持。既有六态身份/图/自旋检查及 97 次尝试审计见来源记录，失败不混入六个采用态。本次独立重读能量、频率、态与输入路线；图同构检查沿用并审阅原档，未冒称重新做全局构象搜索。

| 对象 | 态 | q | 2S+1 | N | E / Eh | 完整模数 | 最低频 / cm⁻¹ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | HS | 0 | 5 | 53 | -363.6176374010 | 153 | 8.3977 |
| C1 | LS | 0 | 1 | 53 | -363.6047771550 | 153 | 13.2501 |
| C2 | HS | 0 | 5 | 53 | -362.0562847360 | 153 | 7.7279 |
| C2 | LS | 0 | 1 | 53 | -362.0454296430 | 153 | 11.9508 |
| C3 | HS | 0 | 5 | 59 | -352.5130764200 | 171 | 8.4798 |
| C3 | LS | 0 | 1 | 59 | -352.5049198750 | 171 | 14.0169 |

## 3. 修后当前必评关键点与结论覆盖（2026-09-29）

本表对齐本包当前五个 evaluator JSON。历史真实计算链及数值仍见第 2、4、5 节；reference 不新增评分门槛。

| 当前 ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| pr_process_states / process | The submission constructs the three named neutral Fe(II) complexes with both intended HS and LS states and preserves donor/atom identity. | C1/C2 53 atom，C3 59 atom，0/5 和 0/1 六态，cis N-donor 图及来源核对。 | pr_r1 |
| pr_process_validation / process | The submitted state energies are supported by optimization and state-validation diagnostics plus explicit coverage/stopping information. | 六个采用态优化、完整频率及源身份/自旋档；失败不充当成功。 | pr_r2 |
| pr_result_values / result | The calculation provides supported isolated electronic HS-minus-LS gaps for each fixed complex. | 三个 HS−LS 计算值由日志产生；正文值仅用于独立对照。 | pr_r3a, pr_r3b, pr_r3c |
| pr_result_order / result | The series follows the reported relative ligand-field trend. | −21.415>−28.500>−33.765，C3>C2>C1 相对 LS 稳定化，非 LS 基态。 | pr_r4 |

| 结论 ID / 角色 | 当前科学主张 | 支持关键点及边界 |
| --- | --- | --- |
| pr_final / final | The independent calculation supports the author's qualitative hypothesis for the isolated series within method uncertainty. | pr_process_states, pr_process_validation, pr_result_values, pr_result_order。现有六态支持限定孤立电子能比较；未认证自主事前计划或全局构象穷尽。合理替代方法按实际电子态和能量证据判断，不强制复现作者每个数值。 |

修前→修后：关键点 4→4；结论记录 1→1。现有结论为科学成果，不另给普通免责声明计分。真实计算支持范围不因本次改关联而扩大。

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C1_HS | [输入](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C1_HS_source_cis_frame_isolated_optfreq_20260923_20260923T154050Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C1_HS_source_cis_frame_isolated_optfreq_20260923_20260923T154050Z/stdout.log) | [0, 5] | -363.6176374010 | -363.2914180000 | 153 / 0 / 8.3977 | native normal |
| 2 | C1_LS | [输入](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C1_LS_source_cis_frame_isolated_optfreq_20260923_20260923T155216Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C1_LS_source_cis_frame_isolated_optfreq_20260923_20260923T155216Z/stdout.log) | [0, 1] | -363.6047771550 | -363.2699260000 | 153 / 0 / 13.2501 | native normal |
| 3 | C2_HS | [输入](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C2_HS_source_cis_frame_isolated_optfreq_20260923_20260923T155147Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C2_HS_source_cis_frame_isolated_optfreq_20260923_20260923T155147Z/stdout.log) | [0, 5] | -362.0562847360 | -361.7339700000 | 153 / 0 / 7.7279 | native normal |
| 4 | C2_LS | [输入](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C2_LS_source_cis_frame_isolated_optfreq_20260923_20260923T155231Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C2_LS_source_cis_frame_isolated_optfreq_20260923_20260923T155231Z/stdout.log) | [0, 1] | -362.0454296430 | -361.7138670000 | 153 / 0 / 11.9508 | native normal |
| 5 | C3_HS | [输入](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C3_HS_exact_final_geometry_Hessian_refresh_optfreq_20260925_20260925T175227Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C3_HS_exact_final_geometry_Hessian_refresh_optfreq_20260925_20260925T175227Z/stdout.log) | [0, 5] | -352.5130764200 | -352.1305920000 | 171 / 0 / 8.4798 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 6 | C3_LS | [输入](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C3_LS_source_cis_frame_isolated_optfreq_20260923_20260923T155246Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/qzcli_hpc/author_C3_LS_source_cis_frame_isolated_optfreq_20260923_20260923T155246Z/stdout.log) | [0, 1] | -352.5049198750 | -352.1134740000 | 171 / 0 / 14.0169 | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 2, 3, 4, 6 | `#p CAM-B3LYP/CEP-31G EmpiricalDispersion=GD3 Opt=(CalcFC,MaxCyc=300,MaxStep=10) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 5 | `#p CAM-B3LYP/CEP-31G EmpiricalDispersion=GD3 Opt=(Cartesian,CalcFC,RecalcFC=10,MaxCyc=300,MaxStep=3) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |

## 5. 模型、连接与后处理原始出处

- [provenance/six_state_closure_20260926/INDEPENDENT_RESULTS.json](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/six_state_closure_20260926/INDEPENDENT_RESULTS.json)
- [provenance/six_state_closure_20260926/EVALUATOR_AUDIT.json](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/provenance/six_state_closure_20260926/EVALUATOR_AUDIT.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../../docs/verification/group_2/paper_589f72ac15eb7acd/report/results.json)

## 6. 修后包检查与未认证事项（2026-09-29）

当前策略为 `dual_axis_100.scientific_results.v1`；真实历史 report 对本包的实际输出检查：**通过**。本包已执行 20 个提交样例，每个分别经过 JSON Schema 和真实 validate_output_contract；合成正反例只测试格式，未加入本计算档案的科学证据。

现有六态支持限定孤立电子能比较；未认证自主事前计划或全局构象穷尽。合理替代方法按实际电子态和能量证据判断，不强制复现作者每个数值。

[逐包维护记录](task_provenance/maintenance_audit.md)及[集中报告第30节](../../../MAINTENANCE_REPORT.md)记录实际修改、检查与未闭合项。普通免责声明已取消必填及独立计分，身份/态/收敛/频率/路径/参考态和真实失败证据保留。

本次没有新电子结构计算、HPC 操作、完整 LLM 评分或 AR 盲测；没有迁移 final/hold。文件导出检查只覆盖 agent_input 物化，不能替代部署侧父目录、容器挂载和网络隔离。完整原始证据直接链接在第 4、5 节，不依赖 task_provenance 的长期存在。

# 已验证计算参考：paper_9e7293af88532cd4 / autonomous_research

> 2026-09-29 修后同步：任务修复和当前评分映射见第 3、6 节；全部仍在 verified_tasks，未获迁移确认。
核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/autonomous_research/paper_9e7293af88532cd4`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 4。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16 PBE1PBE/def2-TZVP，Mo 28 核 ECP，IEFPCM water，四个中性单重态 Opt/Freq。反应为 Im5 + H₂O → product 3；原 complex 1 与 product 3 相差 NH，不得裸减冒充反应能。四个最低点依次为 25/27/24/3 原子、69/75/66/3 个正频率。SI 物理第 5–7 页的 1 atm/1 M 标签不一致；本次采用当前已修订任务明确区分的四种量，不替作者消除冲突。

论文来源：[正文](../../../../../papers/paper_9e7293af88532cd4/documents/main.pdf)；[SI](../../../../../papers/paper_9e7293af88532cd4/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

四套 XYZ 是已修订任务明确给定的验证/性质对象，不将 product_3 文件名一律视为答案泄露。四输入完整、单位/态明示，water 必须独立优化；不评独立发现整个 1→3 反应。源题已公开配平和四种标准态算式，不回退旧未配平版本。

## 2. 有效计算链、结果与推导

raw=(G3−GIm5−Gwater)×627.5094740631=3.974017499 kcal/mol；source_recipe=raw−RT ln55.34=1.596081539；all1M=raw−RT ln(Rgas·T·1 M/1 atm)=2.079689054；bulk=all1M−RT ln55.34=−0.298246907。R=0.00198720425864083 kcal mol⁻¹ K⁻¹，Rgas=0.08205736608096 L atm mol⁻¹ K⁻¹，T=298.15 K，Δn=−1。当前 source_recipe 与 1.6±8.0 比较，其余三值不能替换该靶。直接从最终几何得到 Mo–N–O=178.213119°、N–O=1.197462 Å，频率第 64 模 1698.7976 cm⁻¹；NO 主伸缩指认的位移投影由既有诊断提供。这支持末步热化学及键合诊断，不证明完整机理或唯一氧化态。

| 组分 | 原始 1 atm G / Eh |
| --- | --- |
| reactant_1 | -859.2627110000 |
| product_3 | -914.5192590000 |
| im5 | -838.1439130000 |
| water | -76.3816790000 |

## 3. 修后当前必评关键点与结论覆盖（2026-09-29）

本表对齐本包当前五个 evaluator JSON。历史真实计算链及数值仍见第 2、4、5 节；reference 不新增评分门槛。

| 当前 ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| ar_process_endpoints / process | All four source-defined structures are validated while retaining original complex1 and complex3 records. | 全部四个中性单重最低点的69/75/66/3正频；未丢原complex1。 | ar_r1 |
| ar_process_thermo / process | Final water binding is atom balanced; the source arithmetic and consistent standard states are separated. | 配平Im5+water→3；从原G复算四个标准态约定。 | ar_r2 |
| ar_result_delta / result | The SI S7 +1.6 kcal/mol value belongs to Im5 + H2O -> product3 using its stated raw-G minus RTln55.34 recipe. | source_recipe 1.596081539，对现行1.6±8.0。 | ar_r3 |
| ar_result_interpretation / result | The submission distinguishes computed electronic/mechanistic evidence from unsupported certainty about a pathway or oxidation-state assignment. | MoNO角、NO距离和1698.7976 cm⁻¹模；只支持键合诊断。 | ar_r4 |

| 结论 ID / 角色 | 当前科学主张 | 支持关键点及边界 |
| --- | --- | --- |
| ar_final / final | A source-aware conclusion about the final Im5-water association step, retaining original endpoint validation and a diagnostic; explicitly distinguish the SI arithmetic from consistent standard states and do not claim a complete1-to-3 mechanism. | ar_process_endpoints, ar_process_thermo, ar_result_delta, ar_result_interpretation。末步配平水结合及诊断有真实证据；不是整个反应机理验证。原 ±8.0 kcal/mol 宽容差保留，本轮不重新制定数值标准。 |

修前→修后：关键点 4→4；结论记录 1→1。现有结论为科学成果，不另给普通免责声明计分。真实计算支持范围不因本次改关联而扩大。

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | reactant_1 | [输入](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/reactant_1_si_pbe1pbe_pcm_optfreq_20260915/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/reactant_1_si_pbe1pbe_pcm_optfreq_20260915/stdout.log) | [0, 1] | -859.4041250870 | -859.2627110000 | 69 / 0 / 66.7395 | native normal |
| 2 | product_3 | [输入](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/product_3_si_pbe1pbe_pcm_optfreq_20260915/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/product_3_si_pbe1pbe_pcm_optfreq_20260915/stdout.log) | [0, 1] | -914.6757203260 | -914.5192590000 | 75 / 0 / 54.6857 | native normal |
| 3 | im5 | [输入](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/im5_full_si_water_binding_optfreq_20260921/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/im5_full_si_water_binding_optfreq_20260921/stdout.log) | [0, 1] | -838.2784927220 | -838.1439130000 | 66 / 0 / 69.5884 | native normal |
| 4 | water | [输入](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/water_full_si_binding_reference_optfreq_20260921/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/local_stage_tests_20260914/water_full_si_binding_reference_optfreq_20260921/stdout.log) | [0, 1] | -76.3847839949 | -76.3816790000 | 3 / 0 / 1621.3727 | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 2 | `#p PBE1PBE/GenECP Opt=(Cartesian,CalcFC,Tight,MaxCycles=8) Freq SCRF=(IEFPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512)` |
| 3 | `#p PBE1PBE/GenECP Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=5) Freq SCRF=(IEFPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512)` |
| 4 | `#p PBE1PBE/def2TZVP Opt=(CalcFC,Tight,MaxCycles=8,MaxStep=5) Freq SCRF=(IEFPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512)` |

## 5. 模型、连接与后处理原始出处

- [provenance/balanced_reference_closure_20260926/result.json](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/provenance/balanced_reference_closure_20260926/result.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../../docs/verification/group_4/paper_9e7293af88532cd4/report/results.json)

## 6. 修后包检查与未认证事项（2026-09-29）

当前策略为 `dual_axis_100.scientific_results.v1`；真实历史 report 对本包的实际输出检查：**通过**。本包已执行 10 个提交样例，每个分别经过 JSON Schema 和真实 validate_output_contract；合成正反例只测试格式，未加入本计算档案的科学证据。

末步配平水结合及诊断有真实证据；不是整个反应机理验证。原 ±8.0 kcal/mol 宽容差保留，本轮不重新制定数值标准。

[逐包维护记录](task_provenance/maintenance_audit.md)及[集中报告第30节](../../../MAINTENANCE_REPORT.md)记录实际修改、检查与未闭合项。普通免责声明已取消必填及独立计分，身份/态/收敛/频率/路径/参考态和真实失败证据保留。

本次没有新电子结构计算、HPC 操作、完整 LLM 评分或 AR 盲测；没有迁移 final/hold。文件导出检查只覆盖 agent_input 物化，不能替代部署侧父目录、容器挂载和网络隔离。完整原始证据直接链接在第 4、5 节，不依赖 task_provenance 的长期存在。

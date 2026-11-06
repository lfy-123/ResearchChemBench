# paper_7516a3cbacb70032：现行科学分V2与完整验证参考

更新：2026-10-25。当前状态 **RESULTS_COMPLETE_NUMERIC_REVIEW**，限定现行科学问题的全部必要结果与结论。必要结果齐全；12项相对比较最大绝对差0.073764 kcal/mol。323.15 K由热表指纹与实验温度推断；不能写成作者明确给出该温度命令。

父级登记依据：[验收决定](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_acceptance_decision.json)；独立原生证据：[审计JSON](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/audit.json)、[详细审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/audit.md)。这里使用已经完成的验证计算，没有新增量化作业，也不是盲测Agent成绩。

## 现行评分与范围

每题科学分100分，过程分0；二元项分别计分。6个中间科学项各10分，覆盖连续成键、立体竞争、配体对照和能量顺序；最终形成与螺旋解释各15分、二者与动力学区别10分。无独立流程分；相对能量作为可证伪方向的依据，未设置追随当前误差的新硬数值窗。

确认323.15 K的来源指纹推断和GoodVibes准谐焓约定；评估结合态VI到中性游离产品的范围区别，以及局部势垒排序能支持的限速措辞。原有题面60/20/20及条件作者指导措辞按迁移指南保留，私有现行规则不再奖励研究质量。

|现行科学项|类型|权重|论文依据|验证覆盖|
|---|---|---:|---|---|
|ch_activation：底物C–H活化的反应连接|中间|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|alkyne_insertion：炔烃并入与C–C成键|中间|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|ring_closure：后续C–N成环与指定骨架|中间|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|helicity_competition：M/P竞争方向|中间|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|ligand_comparison：配体降低局部活化困难|中间|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|step_difficulty：成产物步骤的局部困难排序|中间|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|formation_answer：最终：连接的螺烯形成解释|最终|15|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|helicity_answer：最终：配体与螺旋选择的关系|最终|15|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|
|kinetic_answer：最终：立体选择与较困难步骤的区分|最终|10|V2_MAIN, V2_SI|本节独立审计的相关结构、能量、连接或性质比较；按规则的范围使用|

|证据ID|原始文件|PDF页序（1起算）|SHA256|
|---|---|---|---|
|V2_MAIN|[main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_7516a3cbacb70032/documents/main.pdf)|7, 8|73aea65b0e8a722b9cc59a4f848d438554de3f9d70ebbea6b86cef4b6d88f80a|
|V2_SI|[supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_7516a3cbacb70032/documents/supplementary_001.pdf)|65, 66, 67, 101, 102, 103, 104|dc33c26abe33a7160cdfe4bee2b662263f0a0526b46be3347b1ceefc6179c6b9|

## 现行验收采用的计算过程、结果、差值和方法边界

**以下为已获父级验收的独立审计证据原文。原文中的“建议”“待父级确认”描述审计当时的登记步骤；当前状态以上方及父级决定为准。旧KP过程项仅是覆盖审计历史，不是第4节现行评分。**

独立审查：paper_7516a3cbacb70032
时间：2026-10-24T16:08:05.949011+00:00

建议以本审查修正后的作者方法证据列为 `RESULTS_COMPLETE_NUMERIC_REVIEW`。当前科学问题所需的 M/P、配体促进作用、插入／消除及产物骨架终点均有有效原生证据，未发现核心定性反向。该建议不等于严格数值通过，也不直接修改父级通过数量。

审查直接读取了当前任务、2026-10-23 验收标准、原论文/SI及24份Gaussian原生日志；只在本目录写文件，未提交或重跑QC，未改owner文件或任务。原生计算全部有效，但发现owner后处理遗漏作者准谐焓并假定298.15 K。此问题已用原生日志离线纠正，不能把原先方法不一致直接包装成一般数值误差。

方法与来源

[SI](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_7516a3cbacb70032/documents/supplementary_001.pdf) S65明示Gaussian16、PBE0-D3(BJ)/6-31G(d,p)-SDD(Ir,Ag)几何/频率、PBE0-D3(BJ)/6-311++G(d,p)-SDD溶剂单点、SMD二氯甲烷、GoodVibes3.2、100 cm⁻¹准RRHO及1M。实际输入/原生程序与该电子结构方法一致；采用作者结构的固定几何Freq，不要求重复优化。M/P已完成自身OptFreq和匹配SP。电荷/自旋由原生输入核为配体模型及下游+1单重态，无配体模型0单重态；作者原始输入未提供，不能冒称其电荷输入逐字引用。

SI S67 Table S10的qh-H与H确实不同：VI为−2066.841与−2066.833 Eh，V为−2066.866与−2066.858 Eh，M TS为−4229.932与−4229.918 Eh。表中qh-G由qh-H−T·qh-S组成。owner原GoodVibes命令未启用QH，只用H−T·qh-S，因此作者热化学定义未完全执行。

本审查直接调用同版本GoodVibes3.2的calc_bbe，对12份自身频率日志读取振动、转动、平动信息，启用Grimme熵与准谐焓（均100 cm⁻¹）、1M、scale1，再以各自匹配的自身SMD单点SCF替换气相电子能。既未输入作者能量作计算分量，也未添加拟合偏移。298.15 K修正焓的结果和323.15 K的结果均保存在audit.json。

计算温度需区分明示和推断：SI S65未明写计算温度；实验明示50°C。本审查只检查原默认298.15 K和该报告温度323.15 K，没有扫温追值。323.15 K加QH后，12项qh-G全部与S67打印的0.001 Eh一致，24个T·S/T·qh-S项最大偏差7.6131×10⁻⁷ Eh（表打印到10⁻⁶ Eh，M/P重优化及舍入可解释末位）。例如M TS的T·S/T·qh-S为0.203611444/0.185135501，对0.203612/0.185136；VI为0.137033333/0.127140523，对0.137034/0.127141。这是多个独立源热项共同支持的作者设置识别，不是将温度当作已报告的原始命令。

| 比较（kcal/mol） | 独立修正值 | 作者值 | 修正−作者 |
|---|---:|---:|---:|
| M CMD | 16.428767 | 16.4 | +0.028767 |
| P CMD | 18.141479 | 18.1 | +0.041479 |
| P-M | 1.712713 | 1.7 | +0.012713 |
| Ligand-free CMD | 22.455003 | 22.5 | -0.044997 |
| Ligand M minus ligand-free CMD | -6.026236 | -6.1 | +0.073764 |
| Insertion TSIV-IV | 11.879554 | 11.9 | -0.020446 |
| Elimination TSV-V | 25.596144 | 25.6 | -0.003856 |
| V-IV | -14.962811 | -14.9 | -0.062811 |
| VI-V | 17.264808 | 17.2 | +0.064808 |
| VI-IV | 2.301997 | 2.3 | +0.001997 |
| III(M)-II | 3.472709 | 3.4 | +0.072709 |
| III-1a minus INT-1a | 20.378657 | 20.4 | -0.021343 |

作者值来源：M/P为正文PDF第8页/图7b；无配体和反应中间态、下游局部差为SI S66图S2。图中插入14.1是III(M)+参照；同库存IV→TSIV是−19.1−(−31.0)=11.9。当前比较不将14.1误作局部IV势垒。

原生有效性与连接

12组Freq/SP的SHA256逐一与owner记录一致、没有Error termination，均有Normal termination；所有频率计算的原生MAX/RMS力均通过。频率/SP采用相同几何，RMSD均为机器精度量级。12个配对的完整路径、输入、SHA、频率数、SCF及模型见audit.json，以下是实际检查的原生文件。

| 结构 | 频率日志 | 单点日志 | 虚频（cm⁻¹） | 修正G（Eh，323.15 K） |
|---|---|---|---:|---:|
| TSII-_M_-L1 | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_M_-L1/optfreq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_M_-L1/solvent_sp.log) | -865.5983 | -4230.117554054 |
| TSII-_P_-L1 | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_P_-L1/optfreq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_P_-L1/solvent_sp.log) | -1335.8686 | -4230.114824672 |
| II-1a-L1 | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/II-1a-L1/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/II-1a-L1/solvent_sp.log) | 0 | -4230.143734959 |
| INT-1a | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/INT-1a/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/INT-1a/solvent_sp.log) | 0 | -3450.798315412 |
| TS-1a | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/TS-1a/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/TS-1a/solvent_sp.log) | -1193.8757 | -3450.762531087 |
| III-1a | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/III-1a/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/III-1a/solvent_sp.log) | 0 | -3450.765839955 |
| III-_M_ | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/III-_M_/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/III-_M_/solvent_sp.log) | 0 | -4230.138200846 |
| IV-_M_ | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/IV-_M_/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/IV-_M_/solvent_sp.log) | 0 | -2066.971659443 |
| TSIV-_M_ | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/TSIV-_M_/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/TSIV-_M_/solvent_sp.log) | -286.1936 | -2066.952728167 |
| V-_M_ | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/V-_M_/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/V-_M_/solvent_sp.log) | 0 | -2066.995504200 |
| TSV-_M_ | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/TSV-_M_/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/TSV-_M_/solvent_sp.log) | -432.9291 | -2066.954714149 |
| VI-_M_ | [Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/VI-_M_/author_freq.log) | [SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/VI-_M_/solvent_sp.log) | 0 | -2066.967990977 |

VI有95原子、279个正频率，最低11.1232 cm⁻¹，MAX/RMS力0.000014/0.000003 a.u.；气相SCF=−2067.19487516 Eh，溶剂SP=−2067.68046507 Eh。原PDF S101–S103的95原子逐元素和坐标与输入XYZ完全相同；其原生几何与来源RMSD=6.24×10⁻¹⁵ Å。

直接解析负频率振型，M/P CMD均是C26–H39断裂与H39–O130形成（配体P=O辅助），无配体为H39–O75（OTf）；TSIV−286.1936 cm⁻¹的C26–C73距离导数−0.91665，TSV−432.9291 cm⁻¹的N55–C72导数−1.13769，吻合插入和消除成键。C26–C73距离IV/TSIV/V/VI=2.771835/1.978270/1.500926/1.466605 Å；N55–C72距离V/TSV/VI=2.613640/1.884686/1.474344 Å。振型整体符号任意。

独立构建VI的C/N距离图并与公开PRODUCT图做带元素同构，37个重原子完全匹配。N56–H50距离1.017589 Å，故有机部分为C35H23N2；完整模型仍含Ir和C13的取代Cp，不能写成中性游离C35H22N2产品。SI S104晶体式明确为C35H22N2，题面在PI6来源说明中已明确这一区别。VI结合Ir/NH不是事后缩小范围；当前题面排除完整再生/活化释放动力学，所需两个新骨架键已验证。未证明释放或去质子势垒，也不作其已验证的宣称。

直接以公共配体图匹配四个有配体原生结构，并复算轴向有向体积，M/P/II/III分别+2.048540/+1.998563/+2.100334/+2.052309 Å³，全部满足题目正号对映体。M/P反应分支标签仍来自作者结构及来源映射，不宣称独立全构象螺旋搜索。

III→IV连接方面，作者模型III(M)+AgOTf+C14H10→IV(M)+L1AgOTf·HOTf左右均为IrC83H67N3PO7S2F6Ag，总电荷均+1，底物骨架在作者路线中保留。交换和配位自由能/势垒未独立计算，不把它解释成新证明的全局低势垒步骤。任务允许声明分子边界；完整交换网络、所有催化剂再生和全IRC不是当前最小验收门。

验收边界

M低于P、配体使局部CMD降低约6 kcal/mol、插入<CMD<消除，以及连接到指定螺烯重原子骨架，均有本次独立有效证据。作者“消除很可能限速”仅支持为当前所比较基元步骤中的较高局部势垒，不升级为实验全局周转律；91% ee及82%收率不是本次计算预测。精确温度命令仍为来源表指纹推断，数值偏差需父级/专家判断。

供父级同步两模式来源参考的中文更正附录：[source_reference_correction.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/source_reference_correction.md)。证据与复算数值：[audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/audit.json)。


---

## 历史验证记录（不覆盖上方最新验收和V2权重）

历史pending、旧热定义、旧过程权重与旧发表限制描述其记录时状态。主比较以本页最新审计为准，历史数据不删除、不改造成新的计算结果。

# Independent computation verification

当前科学问题已完成验证：RESULTS_COMPLETE_NUMERIC_REVIEW。两模式共用证据。以下早期状态和数值为历史记录；当前验收以文末父级独立验收及323.15 K准谐焓/熵更正为准。

## Follow-up 2026-10-23T0033Z — new returned evidence

Current whole-question status remains **INCOMPLETE**. M通道138原子TS正常完成，原生Opt/Freq29469.17秒（8.19h），唯一虚频−865.5983cm−1。最终源距离图不变；C26–H39与O130–H39沿该模式反向变化，符合来源Figure7的氧辅助C–H裂解/CMD过程。SMD大基组单点和P通道仍未完成；GoodVibes热校正及必要参考态尚不能组成完整自由能比较。不得将当前气相RRHO G当作者16.4kcal/mol势垒，也不据单TS声称螺旋偏好。

| Case | Stage | Electronic E / Eh | Native RRHO G / Eh | Imaginary count | Wall seconds |
|---|---|---:|---:|---:|---:|
| TSII-_M_-L1 | optfreq | -4230.18558369 | -4229.200874 | 1 | 29469.17 |

All new stages have native return code0 and normal termination; optimization, frequencies and formula/connectivity checks were separately inspected.

- `hpc-job-4d795a7a-f314-4ddc-9773-a1e2387e14e9`, TSII-_M_-L1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_M_-L1/optfreq.log`, SHA256 `9d474604dd18955326c4a3ed48fa3c1cfa9c93db86da35c9112e8233f2765cef`.

New evidence and comparison: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/new44_group_01/new_results.json`, `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/job_followup_20261023T0033Z/author_comparison.json`. Current per-paper required coverage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/new44_group_01/coverage.json`. Objective-blocker accounting: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/new44_group_01/blocker_inventory.json`. Existing failure/successor lineage is preserved. No source physics, evaluator or numerical tolerance changed.

## Follow-up 2026-10-23T0647Z — new evidence and bounded successors

Current whole-question status: **INCOMPLETE; no new acceptance candidate**.

新核收M通道SMD大基组SP（5362.67秒）。实际运行GoodVibes3.2，Grimme熵校正、100cm−1阈值、1M、298.15K，得到组合qh-G=−4230.090383Eh。频率缩放明确1.0，温度沿用既有披露假设。P通道仍计算，当前值不是16.4kcal/mol绝对势垒。

原P通道Opt/Freq及溶剂SP待返回并做同一GoodVibes校正；匹配参考态、必要配位/成键路线与配体竞争证据仍未覆盖。M单TS完整不是整题完整。

| Case | Stage | E / Eh | Native RRHO G / Eh | Seconds |
|---|---|---:|---:|---:|
| TSII-_M_-L1 | solvent_sp | -4231.09414289 | — | 5362.67 |

Native result provenance:

- `TSII-_M_-L1/solvent_sp`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_M_-L1/solvent_sp.log`; SHA256 `49b10c6f05359ed2e22cb63fed54db30fa39be765165c34168236f1af1f41cff`.

Author comparison: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/job_followup_20261023T0647Z/author_comparison.json`. Remaining coverage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/job_followup_20261023T0647Z/coverage.json`. Failure lineage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0647Z/new44_group_01/repair_lineage.json`. New objective source blockers:0. Physical model, task statement, evaluator, tolerances and weights unchanged. Existing source/software-version/temperature assumptions remain disclosed; no completed component is a whole-question pass.

GoodVibes3.2 execution: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/job_followup_20261023T0647Z/quasi_RRHO_receipt.json`; [official project documentation](https://github.com/patonlab/GoodVibes).

## Verification target correction 2026-10-23 — required results and author geometries

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No new acceptance candidate. Standard SHA256: `85c52de6f6299b911939cd0636229a1249e4fdf387748f1fa0c6ad75617fbf02`.

Current task requirements, author sources and methods, actual inputs/logs, signed differences, missing evidence and minimal next steps: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/verification_matrix.json`; readable table: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/verification_matrix.md`.

- New required author-route checks: `hpc-job-8598269f-ee76-4fbd-a811-0cdcc81a9d11`; spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/job_spec.json`. Stage-specific purpose and local-relaxation justification are frozen in the spec. First native check `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/job_audits/hpc-job-8598269f-ee76-4fbd-a811-0cdcc81a9d11/native_audit.json`.

Remaining required evidence:

- IR_helicity: 复用M、保留P；直接作者II几何Freq/SP并做相同热校正。
- IR_ligand_role: 直接作者对应4结构含II几何；来源无配体活化22.5为对比不是强制容差。
- IR_product_progression: 直接作者III/IV/TSIV/V/TSV/VI，核局部比较和模式；显式保留配体捕获/炔结合未量化的连接边界。

Physical models, task statement, evaluator, tolerances and weights unchanged. No new objective source blocker. Prior healthy jobs retained. Component completion is not whole-question completion.

## Native job follow-up 2026-10-23 10:44 UTC

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No new acceptance candidate. Standard SHA256: `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`.

Updated claim-by-claim verification matrix and signed comparisons: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/job_followup_20261023T1044Z/verification_matrix.json`; readable table `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/job_followup_20261023T1044Z/verification_matrix.md`. Native receipt: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1044Z/new44_group_01/native_return_review.json`.

- `TSII-_P_-L1/optfreq` completed normally, rc0, 29829.26s; native log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_P_-L1/optfreq.log` (SHA256 `717e4bb64ec2e21d0365454156ddc206d3087e671b2fb605cf6e33635e7cdc83`). This certifies only this stage.

P CMD Opt/Freq is normal with exactly one -1335.8686cm-1 mode involving C26-H39 cleavage/O130-H39 formation; source distance graph retained. GoodVibes3.2 Grimme entropy(100cm-1,298.15K,1M,scale1.0) executed: qh thermal correction=1.003956Eh at printed precision. P solvent SP and II reference remain active, so no completed M/P solution-energy comparison is claimed.

Remaining required evidence:

- IR_helicity: 复用M；P溶剂SP返回后组合已执行的同一GoodVibes热校正，保留II参考及必要后续作者结构批次。
- IR_ligand_role: 直接作者对应4结构含II几何；来源无配体活化22.5为对比不是强制容差。
- IR_product_progression: 直接作者III/IV/TSIV/V/TSV/VI，核局部比较和模式；显式保留配体捕获/炔结合未量化的连接边界。

Healthy jobs and successful stages retained. No new objective source blocker; no task, evaluator, weights, tolerances or expert materials modified.

## Native job follow-up 2026-10-23 12:21 UTC

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No acceptance candidate. Standard SHA256: `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`.

P solventSP completed normally, E=-4231.09211157Eh. Actual GoodVibes3.2 execution at298.15K/1M, Grimme entropy100cm-1 and scale1.0 gives qh-G(P)=-4230.088155Eh; matched priorM=-4230.090383Eh. DeltaG(P-M)=+1.398091kcal/mol versus author+1.7, signed difference-0.301909; M favored. CLI energies rounded1e-6Eh. P unique-1335.8686 C-H/O-H transfer mode and source graph reused. II reference authorFreq newly complete, zeroimaginary and forces passed; solutionSP and ligand/product sequence still pending. Absolute16.4/18.1 CMD barriers and complete mechanism are not yet certified.

Claim matrix: [paper_7516a3cbacb70032](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1221Z/new44_group_01/papers/paper_7516a3cbacb70032/verification_matrix.md); numerical/native comparison: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1221Z/new44_group_01/papers/paper_7516a3cbacb70032/author_comparison.json`; native return receipt: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1221Z/new44_group_01/native_return_review.json`.

New native stages:

- `TSII-_P_-L1/solvent_sp`: rc0, normal termination, 5156.05s; `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/new44_20261022/calculation/TSII-_P_-L1/solvent_sp.log` SHA256 `bb9e5b8d340f8d4129606fdaf2c00862cbf48cbce9b3a67f4a6d9e0fba5d88b8`. Stage scope only.
- `II-1a-L1/author_freq`: rc0, normal termination, 12996.46s; `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_7516a3cbacb70032/verification_target_correction_20261023/ligand_and_product_author_geometry/calculation/II-1a-L1/author_freq.log` SHA256 `52a89a7c901823ca78de084b3ff1a00cffa8d00425d91bcdf2d0c3bb56e2eafe`. Stage scope only.

Remaining necessary results:

- IR_helicity: 复用已核M/P局部差值；保留II参考与配体/后续批次，II返回后重组绝对CMD势垒。
- IR_ligand_role: 直接作者对应4结构含II几何；来源无配体活化22.5为对比不是强制容差。
- IR_product_progression: 直接作者III/IV/TSIV/V/TSV/VI，核局部比较和模式；显式保留配体捕获/炔结合未量化的连接边界。

Healthy batches retained; no new source blocker. Physical methods, task/scoring/weights/tolerances and expert materials unchanged.

## Native job follow-up 2026-10-23 15:50 UTC

Matched GoodVibes3.2 Grimme QS (100 cm-1 cutoff, 298.15 K, 1 M, scale 1.0) with returned II-1a-L1 solvent SP gives Gq(II)=-4230.115712 Eh; M=-4230.090383 and P=-4230.088155 Eh. Absolute CMD barriers are 15.894187 and 17.292279 kcal/mol versus author 16.4/18.1 (signed -0.505813/-0.807721); P-M=1.398091 versus 1.7 (signed -0.301909). These are valid local barrier comparisons; ligand-role and product-progression evidence remains incomplete, so no whole-question candidate.

Source SHA256 policy `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`; this is a current native evidence note. It does not change task text, evaluator, tolerances, expert materials, or acceptance status.

## Verification follow-up 2026-10-24 01:40 UTC — native evidence amendment

Ligand-free INT-1a/TS-1a/III-1a native frequency/force/SP now complete. Actual GoodVibes3.2 Grimme100cm-1/298.15K/1M/scale1 gives localCMD22.034995vs author22.5kcal/mol (delta-0.465005); uniqueTS-1193.8757 has C26-H39/O75-H39 transfer. Relative to existing L1-M15.894187vs16.4, ligand lowers this controlled local barrier6.140808vs6.1; no cross-formula totalG subtraction or experimental rate claim. Existing M/P difference1.398091vs1.7 reused. III(M)Gqh=-4230.110829Eh received; IV/TSIV/V/TSV/VI product-side evidence not complete and III-to-IV association/inventory boundary remains. No whole-question candidate.

Current evidence: [paper_7516a3cbacb70032 author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_7516a3cbacb70032/author_comparison.json); [itemized verification matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_7516a3cbacb70032/verification_matrix.json); [native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_7516a3cbacb70032/native_receipts.json); [reaction mode and source bond mapping](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/transition_mode_review.json). Current standard SHA2562743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379. No new whole-task candidate; no task/scoring/tolerance change. Prior raw records retained; latest native receipts supersede stale parser/completion interpretations.

## Verification follow-up 2026-10-24 03:38 UTC — native evidence amendment

New IV(M) source-frequency zeroimag/maxRMSforce0.000023/0.000004 and solventSP-2067.68118603Eh are normal; actual GoodVibes3.2 Grimme100cm-1/298.15K/1M/scale1 yields Gqh=-2066.954395Eh. Newly returned TSIV(M) frequency has sole-286.1936vs source-286.19cm-1, max/RMSforce0.000009/0.000002. Its dominant C26-C73 bond-forming mode matches source IV-to-V alkyne insertion: source distances2.771835/1.978270/1.500926Angstrom for IV/TS/V. Original TSIVsolventSP runs; V/TSV/VI still incomplete. Do not form solution insertion barrier before ownSP or subtract III-to-IV totals across different inventories. Existing matched ligand-free22.034995 andL1-M/P15.894187/17.292279 barriers reused. No whole-question kinetics/rate-determining conclusion yet.

Current evidence: [author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_7516a3cbacb70032/author_comparison.json); [itemized verification matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_7516a3cbacb70032/verification_matrix.json); [native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_7516a3cbacb70032/native_receipts.json); [source mapping and reaction modes](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/transition_mode_review.json). Standard SHA2562743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379. No whole-question acceptance candidate; no task/scoring/tolerance change. Prior raw records retained; this amendment supersedes stale completion interpretations only.

## Verification follow-up 2026-10-24 07:52 UTC — native evidence amendment

NewTSIVSP,Vfrequency/SP,TSVfrequency/SP allnormal/force/indexvalid. ActualGoodVibes3.2Grimme100cm-1/298.15K/1M/scale1 yields TSIV/V/TSV Gqh=-2066.935763/-2066.978095/-2066.937824Eh, reuseownIV=-2066.954395. LocalinsertionIV-to-TSIV11.691757vsFigureS2sameleveldifference11.9(delta-0.208243);localeliminationV-to-TSV25.270434vs25.6(delta-0.329566);V-IV=-14.871975vs-14.9. Printedsourceinsertion14.1usesIII(M)+reference,notIV; no mixingassociationlevels orcross-inventorytotals. TSIVC26-C73andTSVN55-C72formingmodesverified;TSVsole-432.9291andforce0.000004/0.000001pass. Relative localdifficulty supportsinsertionbelowCMDand eliminationabove,butVIownFreq/SPandproductgraphstillpendingoriginal859826batch. Wholequestionincomplete.

Current evidence: [author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/papers/paper_7516a3cbacb70032/author_comparison.json); [itemized verification matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/papers/paper_7516a3cbacb70032/verification_matrix.json); [native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/papers/paper_7516a3cbacb70032/native_receipts.json); [source mapping and reaction modes](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/transition_mode_review.json). Standard SHA2562743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379. Sulf has a RESULTS_COMPLETE_NUMERIC_REVIEW candidate, requiring parent independent review; Cu/Ir remain incomplete. No task/scoring/tolerance change. Prior raw records retained; this amendment supersedes stale completion interpretations only.

## Verification follow-up 2026-10-24 15:33 UTC — Cu repair and Ir completion candidate

859826全部正常完成，VI自身Freq/SP新收，零虚频、MAX/RMSforce0.000014/0.000003，二者同几何。真实GoodVibes3.2/Grimme100cm⁻¹/298.15K/1M/scale1得到Gqh(VI)=−2066.950950Eh。VI−V17.033745对17.2（差−0.166255）、VI−IV2.161770对2.3（差−0.138230）kcal/mol。所需12个Freq/SP配对均核同几何/物种/电荷自旋；公共轴配体II/M/P/III均为指定正号。VI有机重原子图与题目螺烯同构，插入形成C26–C73、消除形成N55–C72，与实际TS模式和源前后图对应。III+AgOTf+炔→IV+L1AgOTf·HOTf元素/电荷配平且底物子图保持；不跨库存减总G。

复用M/P CMD15.894187/17.292279对16.4/18.1（M偏好差1.398091对1.7），无配体CMD22.034995对22.5，L1-M降低6.140808对6.1；局部插入11.691757对11.9，局部消除25.270434对25.6。当前任务必要的分子结果和限定结论齐全，提出RESULTS_COMPLETE_NUMERIC_REVIEW候选，待父级独立审查；不自行更新总表或称严格数值通过。VI仍含Ir和N56–H50（有机C35H23N2），不是孤立中性产物；未声称完整释放/再生/全局微观动力学或实验91%ee复现。作者插入14.1以III(M)+为零点，不能混为IV局部11.9；配体交换/炔结合的连接已核模型库存，但未声称其自由能或势垒独立计算。原文未列Gaussian电荷输入/温度，现行模型推定和298.15K假设明确保留专家判断；不把重要未解物种偷偷叫数值误差。GoodVibes导入超时已在同代码/参数有界诊断中rc0完成，无QC重算，新增客观来源阻碍0。

当前逐项证据：[matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/new44_group_01/papers/paper_7516a3cbacb70032/verification_matrix.json)；[readable comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/new44_group_01/papers/paper_7516a3cbacb70032/author_comparison.md)；[native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/new44_group_01/papers/paper_7516a3cbacb70032/native_receipts.json)；[handoff](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/new44_group_01/handoff.md)。仅此验证参考和manifest更新；题面、评分、容差及专家材料不变。旧原生日志与历史报告保留。

## 父级独立验收与热力学校正更正（2026-10-24）

父级已核收独立审查：当前任务必要计算及相关结论完整，登记为 **RESULTS_COMPLETE_NUMERIC_REVIEW**。这是完整科学问题的结果验证，不是缺项时的定性暂定通过；温度识别依据和模型边界仍明确披露。

作者热化学参考更正与独立核验（2026-10-24）

`paper_7516a3cbacb70032` 的本段参考适用于自主科研与论文复现模式共同的当前科学问题。独立核验支持 `RESULTS_COMPLETE_NUMERIC_REVIEW`，最终验收由父级裁定；本段不是自动满分、发布或严格数值容差裁决。

更正此前298.15 K且仅准谐熵的参考：该口径下的VI−V=17.033745、VI−IV=2.161770及M/P=15.894187/17.292279 kcal/mol保留为历史后处理结果，但不再作为作者方法一致的最终数值参考。遗漏准谐焓是可纠正的后处理不一致，已由现有原生日志离线修复，不需要重新计算电子结构。

作者方法依据为[SI PDF](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_7516a3cbacb70032/documents/supplementary_001.pdf) S65、S67：Gaussian16；气相PBE0-D3(BJ)/6-31G(d,p)-SDD(Ir,Ag)几何/频率；PBE0-D3(BJ)/6-311++G(d,p)-SDD的SMD二氯甲烷单点；GoodVibes3.2、100 cm⁻¹准RRHO、1M。S67明确给出不同的H与qh-H，且qh-G=qh-H−T·qh-S；例如VI的H/qh-H为−2066.833/−2066.841 Eh。故本次启用准谐焓及Grimme准谐熵，频率缩放1.0。

计算温度323.15 K属于证据支持的识别，不是直接引用作者输入：正文实验明示50°C，SI S65未明示热化学温度。用323.15 K和上述修正，12个独立计算的qh-G全部符合S67的0.001 Eh打印精度，24个T·S/T·qh-S项最大偏差7.6131×10⁻⁷ Eh，符合10⁻⁶ Eh打印分辨率附近。M TS的T·S/T·qh-S=0.203611444/0.185135501 Eh，对源0.203612/0.185136；VI=0.137033333/0.127140523，对源0.137034/0.127141。只比较了旧298.15 K与实验报告的323.15 K，无扫温、换泛函或拟合能量。

所有新参考值来自真实原生输出的独立后处理：读取每个结构自身Gaussian频率日志，运行GoodVibes3.2 `calc_bbe(..., QS="grimme", QH=True, s_freq_cutoff=100, H_FREQ_CUTOFF=100, temperature=323.15, conc=1, freq_scale_factor=1, spc=False)`，再加入该结构自身匹配SMD单点电子能与气相电子能之差。作者表中电子能/热项只用于最后核对，未回填为计算输入；保留原生Freq/SP文件、哈希、实际设置及每项热化学分量于独立audit.json。

| 比较（kcal/mol） | 独立修正值 | 作者值 | 修正−作者 |
|---|---:|---:|---:|
| M CMD | 16.428767 | 16.4 | +0.028767 |
| P CMD | 18.141479 | 18.1 | +0.041479 |
| P-M | 1.712713 | 1.7 | +0.012713 |
| Ligand-free CMD | 22.455003 | 22.5 | -0.044997 |
| Ligand M minus ligand-free CMD | -6.026236 | -6.1 | +0.073764 |
| Insertion TSIV-IV | 11.879554 | 11.9 | -0.020446 |
| Elimination TSV-V | 25.596144 | 25.6 | -0.003856 |
| V-IV | -14.962811 | -14.9 | -0.062811 |
| VI-V | 17.264808 | 17.2 | +0.064808 |
| VI-IV | 2.301997 | 2.3 | +0.001997 |
| III(M)-II | 3.472709 | 3.4 | +0.072709 |
| III-1a minus INT-1a | 20.378657 | 20.4 | -0.021343 |

M/P参考来自正文PDF第8页及图7b；其余参考由SI S66图S2同参照能级或局部势垒读得。III(M)−II=−26.1−(−29.5)=3.4；无配体产物−反应物=0.4−(−20.0)=20.4。插入14.1使用III(M)+参照；本表局部插入IV→TSIV采用11.9。不得将不同库存的III、IV总G直接相减。

修正后的所有结论保持：M路径较低、配体降低CMD局部势垒、所比较步骤中插入<CMD<消除。24份原生Freq/SP日志均正常终止；12对几何相符，频率指数和原生力检查有效。M/P和无配体CMD振型对应正确的质子转移；TSIV、TSV振型分别对应C26–C73及N55–C72成键。VI原生279个正频率、最低11.1232 cm⁻¹，MAX/RMS力0.000014/0.000003；323.15 K修正G(VI)=−2066.967990977 Eh。

终点范围与连接：VI的37重原子有机图与题目指定产物一致，源PDF S101–S103坐标与实际输入完全一致。它仍含Ir及N56–H50，有机部分C35H23N2；题目观察的中性晶体产品C35H22N2来自SI S104。此处验证了C–C及C–N关环达到作者结合态终点，不冒称已经优化/验证游离中性产品的释放或去质子动力学。当前题面允许声明分子边界并明确排除完整催化剂再生，故无需因该已知边界补全循环。

III(M)+AgOTf+炔→IV(M)+L1AgOTf·HOTf的元素、电荷库存守恒，来源结构连接保持底物骨架；交换/配位本身的自由能和势垒未独立复现。表中局部难度不构成实验周转律，不独立预测91% ee或82%收率。全IRC、全构象和题外再生未增加为统一门槛。

独立审查：[audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/audit.md)；机器可读的全部原生文件哈希、12组热项和修正比较：[audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/audit.json)。本段更正仅增加真实核验证据，不修改科学问题、评分、权重或容差。

父级决定：[parent_acceptance_decision.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_acceptance_decision.json)。

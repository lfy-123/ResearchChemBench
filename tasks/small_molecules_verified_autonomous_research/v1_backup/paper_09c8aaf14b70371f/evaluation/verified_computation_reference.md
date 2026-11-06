## 2026-10-20 专家第一轮评分规则同步

删除中性受电子轨道区域和还原阴离子自旋分布两项；最终解释加入基于化学知识与计算的峰电位差异假说。五项分值为 25/20/15/10/30。

本节记录评分合同变更；下方原日期的计算结果、旧规则和验收范围按历史保留，不作为额外的现行评分要求。当前规则以 scoring_rules.json、reference_key_points.json 和 reference_conclusions.json 为准。本轮没有新增量子化学作业。

> 2026-10-17 评分覆盖同步：依据正文第12–14页及2026-10-15既有验收，将2号已被支持的有限关系、空间及溶剂比较纳入原三项规则；50/25/25不变，无新容差或新计算。仅精确作者构象/标量归属仍受限。下方“2号不在活动评分中”的旧资格描述只属于修订前版本，不能覆盖本条；正式总分/发布仍未放行。

> 2026-10-17 当前状态同步：已有2026-10-15的现行限定科学问题验收证据，本轮复核并同步记录，没有新增量化计算。[当前状态及限制](current_verification_status.json)区分科学覆盖与评分/发布资格。下方旧pending、失败和目录位置按原日期/范围保留，不覆盖后续现行验收；本次整理不自动放行正式评分或发布。

# paper_09c8aaf14b70371f 验证计算参考（autonomous_research）

专家材料同步整理标记：expert8_20261015；整理时间：2026-10-15T13:34:03.626007+00:00。

## 最新结论与历史状态的关系

## 2026-10-15 当前五化合物科学问题验收

父级验收时间：2026-10-15T05:12:56.012193+00:00。**当前公开科学问题的计算验证通过，`current_scope_verified=true`；正式来源/评分资格仍冻结，`release_ready=false`，官方总分不赋值。** 本条更新此前仅覆盖1/3/4/5、随后撤回完整通过登记的状态；不更改历史原始结果。

当前题面要求提出并检验五个查尔酮跨结构和溶剂的分子解释，并识别其适用范围。正文第2页方法、第14页关系讨论与SI坐标经过核对；沿作者B3LYP/6-311+G(2df,2p)、IEF-PCM及中性/还原态路线得到真实结果。父级独立重读新增化合物2的8份log/fchk；独立复核进程重核全部25组log/fchk、24份cube及72个已有哈希，分子图、E构型、原子/电子数、完整正频率和几何一致。

|当前科学问题部分|已完成证据及判定|
|---|---|
|3–5关系与1的偏离|两溶剂均得到3→4→5的LUMO升高；1与3仅差0.005490/0.005212 eV，而Epc相差0.163/0.170 V，支持有限关系及其失效范围。|
|化合物2的实际覆盖|SI起点A与结构明确的B各完成两溶剂中性/阴离子优化、96正频率和同根Stable。中性B−A自由能为0.783132/0.759914 kcal/mol；两个构象均有比3高的LUMO、但实验Epc更正，均支持与1类似的关系偏离。未声称穷尽构象或唯一对应作者E1/E2。|
|五分子的电子接受区域|12个中性轨道和12个还原态自旋cube均有原生波函数来源；共轭烯酮区域重要且分布延伸至芳环。独立网格积分0.999576–0.999871；片段积分仅为描述，不新设百分比阈值。|
|溶剂行为和边界|3从DCM到ACN/DMSO的LUMO降低0.029032/0.031293 eV，作者为0.030/0.032，主要趋势一致。ACN/DMSO轨道变化均小；实验1/2/3/4/5变化为+15/−21/+8/−15/−37 mV，不认证2/4/5微小变化方向预测。|

**保留的数值和方法边界：** 1/3/4/5绝对LUMO仍低于作者0.126783–0.136391 eV；化合物2的A/B候选与未唯一归属的作者标量差约0.074449–0.141718 eV。这些不是已经精确复现的标量，未使用拟合偏移、新容差或论文值替代计算。当前任务及活动规则要求检验关系、空间分布及解释边界，未要求匹配绝对电位或上述未校准标量，因此这些差异不推翻已得到的有限关系和反例。

所有12个阴离子及4个化合物2中性模型有显式Stable且保持原根；其他9个中性模型为收敛的限制性单重态Opt/Freq，不能写成全部25态都显式通过Stable或全局基态已证明。部分优化按Gaussian negligible-force条件结束，位移NO如实保留。唯一因果机制、精确电化学电位、完整构象群体和全部微小溶剂变化方向均未认证。

正式`qualification.json`的source-definition/calibration hold及原评分规则原样保留，未赋官方总分，未发布。科学覆盖验收记录与正式资格限制分列，不因隐藏规则排除化合物2便直接通过五分子题面；本次新增通过依赖化合物2的实际补算和独立检验。

[父级原生核查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/parent_09c8_native_crosscheck.json) · [独立科学意见](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_by_lane06.md) · [25组原生与24份空间数据核查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_native_checks.json)。

本汇总于2026-10-15整理。新增2号8组真实计算及空间证据补齐此前五化合物题面缺口；取代仅凭1/3/4/5证据的早期状态。当前科学覆盖通过，并不更改qualification.json中保留的来源/校准冻结和release_ready=false。其旧NOT_VERIFIED_FOR_NEW_SCOPE不再描述缺算情况；仍须与正式资格限制区分。

## 作者路线、复用与新增计算

1. 依据正文第2页方法、Table 4（第7页）、Tables 5–7（第9–11页）、Figs. 11–14（第12–14页）和SI第24–27页结构核对五种E查尔酮。采用Gaussian 16、B3LYP/6-311+G(2df,2p)、IEF-PCM；中性0/1，还原阴离子−1/2，后者UB3LYP。实际优化使用Tight、UltraFine、SCF Tight/XQC等设置，具体MaxCycles与续算以原生日志route为准。热化学298.15 K，实验未报告条件不冒称已知。
2. 复用1/3/4/5的两溶剂×中性/阴离子16组及3的DCM中性1组。对化合物2，A取SI可追溯结构起点，B从明确ringB转动180°生成；A/B分别在ACN/DMSO计算中性和阴离子，共8组新增，不是事后选择最接近作者值的构象。
3. 对25组log/fchk检查分子图、E构型、原子/电子数、优化结束、完整正频率和波函数/几何一致。2号34原子、142/143电子、96正模；其8组有5组四项收敛YES、3组按negligible-force结束，保留原始位移NO。12阴离子及4个2号中性显式Stable并保持原根，其余9个受限中性仅Opt/Freq，不夸大为全局基态证明。
4. 从fchk提取中性LUMO并保留Eh→eV换算；从可追溯波函数生成12个中性LUMO与12个阴离子自旋cube，核查几何与网格归一并按同一公开原子分区作描述性积分。3的额外DCM中性不在这24份空间cube之内。
5. 对比3–5趋势、1/2反例和溶剂差。2号A/B的中性B−A自由能为0.783132/0.759914 kcal/mol（ACN/DMSO），阴离子为约1.6378/1.6660；两候选均支持同方向偏离，不认证完整构象群或唯一作者E1/E2归属。
6. 父级独立核对新增8组log/fchk，另一验证组核对总25组和24 cube以及既有72个哈希；根据完整题面验收有限关系、空间证据及解释边界。

以上为6个工作阶段；25组最终模型、其中8组补算，不等于25次HPC提交或总优化步数。复用和失败诊断不重复计为新增模型；本次整理未新跑QC，没有可统一核实的全历史wall/CPU合计，故不填写推测工时。

## 中性LUMO逐量对照

所有差值为本地−论文，eV。作者2号标量的构象归属仍未唯一确定，下表A/B只是对同一已发表标量作透明诊断，不能作为两个已验证作者构象。绝对残差未用拟合偏移消除，也没有新增统一容差。

| 模型/环境 | 作者值 | 本地值 | 差值 | 性质 |
| --- | --- | --- | --- | --- |
| 1/acetonitrile/LUMO | -2.537000 | -2.664244 | -0.127244 | 绝对值残差保留；关系另评 |
| 1/dmso/LUMO | -2.540000 | -2.666783 | -0.126783 | 绝对值残差保留；关系另评 |
| 3/acetonitrile/LUMO | -2.538000 | -2.669734 | -0.131734 | 绝对值残差保留；关系另评 |
| 3/dichloromethane/LUMO | -2.508000 | -2.640702 | -0.132702 | 绝对值残差保留；关系另评 |
| 3/dmso/LUMO | -2.540000 | -2.671995 | -0.131995 | 绝对值残差保留；关系另评 |
| 4/acetonitrile/LUMO | -2.470000 | -2.606143 | -0.136143 | 绝对值残差保留；关系另评 |
| 4/dmso/LUMO | -2.473000 | -2.609391 | -0.136391 | 绝对值残差保留；关系另评 |
| 5/acetonitrile/LUMO | -2.293000 | -2.424953 | -0.131953 | 绝对值残差保留；关系另评 |
| 5/dmso/LUMO | -2.298000 | -2.429232 | -0.131232 | 绝对值残差保留；关系另评 |
| 2/candidateA/acetonitrile/LUMO | -2.493000 | -2.634554 | -0.141554 | 绝对值残差保留；关系另评 |
| 2/candidateA/dmso/LUMO | -2.496000 | -2.637718 | -0.141718 | 绝对值残差保留；关系另评 |
| 2/candidateB/acetonitrile/LUMO | -2.493000 | -2.567449 | -0.074449 | 绝对值残差保留；关系另评 |
| 2/candidateB/dmso/LUMO | -2.496000 | -2.570760 | -0.074760 | 绝对值残差保留；关系另评 |

## 相对关系、空间结果与最终解释

| 比较 | 作者/实验依据 | 实际计算结果 | 科学解释与边界 |
| --- | --- | --- | --- |
| 3→4→5 | 两溶剂作者LUMO升高、Epc更负 | ACN −2.669734→−2.606143→−2.424953；DMSO −2.671995→−2.609391→−2.429232 eV | 局部系列关系恢复，不能外推为通用因果机制 |
| 1与3 | Epc差+0.163/+0.170 V | LUMO差+0.005490/+0.005212 eV | 轨道近等能却Epc差大，统一描述有反例 |
| 2与3 | Epc差+0.117/+0.088 V | A/B中性LUMO均比3高 | 两明确构象均支持反例；作者E1/E2归属仍hold |
| 3 DCM→ACN/DMSO LUMO降低 | 0.030/0.032 eV | 0.029032/0.031293 eV；差−0.000968/−0.000707 | 主要溶剂方向一致，不是绝对电位验证 |
| 五分子DMSO−ACN实验变化 | +15/−21/+8/−15/−37 mV | LUMO全部微降约0.002261–0.004279 eV | 仅小幅度比较成立；2/4/5微小方向不能认证 |
| 电子接受区域 | 中性轨道及还原态自旋的共轭离域 | 12+12 cube；积分0.999576–0.999871 | 烯酮重要并延伸芳环；分区不设阈值、不限制到单原子 |

## 25组原生证据与状态检验

| 模型 | 原子数 | 电荷/多重度 | 正频数/应有 | 最低频率 cm⁻¹ | 态检验范围 | 原生证据 |
| --- | --- | --- | --- | --- | --- | --- |
| chalcone1_neutral_acetonitrile | 33 | 0/1 | 93/93 | 21.1522 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_neutral_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_neutral_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone1_validated_wavefunctions_spatial/outputs/chalcone1_neutral_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_neutral_acetonitrile/input.com>) |
| chalcone1_anion_acetonitrile | 33 | -1/2 | 93/93 | 18.4925 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_anion_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_anion_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone1_validated_wavefunctions_spatial/outputs/chalcone1_anion_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_anion_acetonitrile/input.com>) |
| chalcone1_neutral_dmso | 33 | 0/1 | 93/93 | 21.0747 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_neutral_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_neutral_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone1_validated_wavefunctions_spatial/outputs/chalcone1_neutral_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_neutral_dmso/input.com>) |
| chalcone1_anion_dmso | 33 | -1/2 | 93/93 | 19.2492 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_anion_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_anion_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone1_validated_wavefunctions_spatial/outputs/chalcone1_anion_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone1_anion_dmso/input.com>) |
| chalcone3_neutral_acetonitrile_reused | 28 | 0/1 | 78/78 | 23.6526 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/provenance/qzcli_hpc/chalcone_E_author_IEFPCM_acetonitrile_optfreq_20260915/20260915T095707480436Z_hpc-job-2004465-cluster-slurmd-0/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_acetonitrile_existing_wavefunction_export/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_acetonitrile_existing_LUMO_cube/outputs/LUMO.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/provenance/qzcli_hpc/chalcone_E_author_IEFPCM_acetonitrile_optfreq_20260915/20260915T095707480436Z_hpc-job-2004465-cluster-slurmd-0/input.com>) |
| chalcone3_anion_acetonitrile | 28 | -1/2 | 78/78 | 27.4265 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_anion_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_anion_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone3_validated_wavefunctions_spatial/outputs/chalcone3_anion_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_anion_acetonitrile/input.com>) |
| chalcone3_neutral_dmso | 28 | 0/1 | 78/78 | 22.6392 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone3_validated_wavefunctions_spatial/outputs/chalcone3_neutral_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_dmso/input.com>) |
| chalcone3_anion_dmso | 28 | -1/2 | 78/78 | 26.1504 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_anion_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_anion_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone3_validated_wavefunctions_spatial/outputs/chalcone3_anion_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_anion_dmso/input.com>) |
| chalcone4_neutral_acetonitrile | 33 | 0/1 | 93/93 | 8.5972 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_neutral_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_neutral_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone4_validated_wavefunctions_spatial/outputs/chalcone4_neutral_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_neutral_acetonitrile/input.com>) |
| chalcone4_anion_acetonitrile | 33 | -1/2 | 93/93 | 19.7987 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_anion_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_anion_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone4_validated_wavefunctions_spatial/outputs/chalcone4_anion_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_anion_acetonitrile/input.com>) |
| chalcone4_neutral_dmso | 33 | 0/1 | 93/93 | 6.3441 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_neutral_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_neutral_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone4_validated_wavefunctions_spatial/outputs/chalcone4_neutral_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_neutral_dmso/input.com>) |
| chalcone4_anion_dmso | 33 | -1/2 | 93/93 | 19.5812 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_anion_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_anion_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone4_validated_wavefunctions_spatial/outputs/chalcone4_anion_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone4_anion_dmso/input.com>) |
| chalcone5_neutral_acetonitrile | 40 | 0/1 | 114/114 | 12.6798 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_neutral_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_neutral_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone5_validated_wavefunctions_spatial/outputs/chalcone5_neutral_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_neutral_acetonitrile/input.com>) |
| chalcone5_anion_acetonitrile | 40 | -1/2 | 114/114 | 17.0565 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_anion_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_anion_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone5_validated_wavefunctions_spatial/outputs/chalcone5_anion_acetonitrile.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_anion_acetonitrile/input.com>) |
| chalcone5_neutral_dmso | 40 | 0/1 | 114/114 | 12.5796 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_neutral_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_neutral_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone5_validated_wavefunctions_spatial/outputs/chalcone5_neutral_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_neutral_dmso/input.com>) |
| chalcone5_anion_dmso | 40 | -1/2 | 114/114 | 17.3051 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_anion_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_anion_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/cases/chalcone5_validated_wavefunctions_spatial/outputs/chalcone5_anion_dmso.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone5_anion_dmso/input.com>) |
| chalcone2_SI_A_anion_acetonitrile | 34 | -1/2 | 96/96 | 19.3210 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_acetonitrile/outputs/spin.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_acetonitrile/input.com>) |
| chalcone2_SI_A_anion_dmso | 34 | -1/2 | 96/96 | 19.4816 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_dmso/outputs/spin.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_anion_dmso/input.com>) |
| chalcone2_SI_A_neutral_acetonitrile | 34 | 0/1 | 96/96 | 10.5126 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_acetonitrile/outputs/lumo.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_acetonitrile/input.com>) |
| chalcone2_SI_A_neutral_dmso | 34 | 0/1 | 96/96 | 10.9461 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_dmso/outputs/lumo.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_SI_A_neutral_dmso/input.com>) |
| chalcone2_ringB_B_anion_acetonitrile | 34 | -1/2 | 96/96 | 23.1673 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_acetonitrile/outputs/spin.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_acetonitrile/input.com>) |
| chalcone2_ringB_B_anion_dmso | 34 | -1/2 | 96/96 | 23.6192 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_dmso/outputs/spin.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_anion_dmso/input.com>) |
| chalcone2_ringB_B_neutral_acetonitrile | 34 | 0/1 | 96/96 | 17.1206 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_acetonitrile/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_acetonitrile/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_acetonitrile/outputs/lumo.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_acetonitrile/input.com>) |
| chalcone2_ringB_B_neutral_dmso | 34 | 0/1 | 96/96 | 17.0178 | 显式同根Stable | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_dmso/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_dmso/outputs/calculation.fchk>) · [cube](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_dmso/outputs/lumo.cube>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/cases/chalcone2_ringB_B_neutral_dmso/input.com>) |
| chalcone3_neutral_dichloromethane | 28 | 0/1 | 78/78 | 22.8087 | 受限单重态Opt/Freq | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_dichloromethane/outputs/gaussian.log>) · [fchk](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_dichloromethane/outputs/calculation.fchk>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/cases/chalcone3_neutral_dichloromethane/input.com>) |

原生表的频率及Stable结论来自既有独立原生复核记录；本次整理读取该记录与对应路径，不把文档打包称为新做了25套QC。每份输入和route可沿模型目录和log追溯。

## 验收、来源和额外诊断入口

- [五分子逐规则定量复核](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/five_compound_rule_review.json>)
- [新增2号空间分区](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/compound2_native_cube_fragment_audit.json>)
- [父级8组原生核查](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/parent_09c8_native_crosscheck.json>)
- [全25组/24cube核查](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_native_checks.json>)
- [独立科学意见](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_by_lane06.md>)

## 当前自主科研五条规则的证据解释

### rule_series_relationship

作者Table 4及正文末段讨论的有限关系是3→4→5的LUMO依次升高，而实验Epc更负；1/3的轨道能几乎相等却有明显不同Epc。本地两溶剂均恢复排序；1−3的LUMO仅+0.005490/+0.005212 eV，实验Epc却+0.163/+0.170 V。新增化合物2两明确定义构象A/B均有比3高的LUMO，但实验Epc更正+0.117/+0.088 V，补齐五分子题面并成为另一反例。绝对LUMO残差和2号原作者构象归属仍保留；50分原人工规则没有eV、相关系数或拟合窗口。2号不借新增结果自动加入活动标量评分，更不能靠在隐藏规则排除2号来宣称五分子已算。

### rule_electron_addition_region

作者Figs. 11–14的中性受电子轨道和还原态自旋分布共同支持共轭烯酮区域重要并向芳环离域。实际12份中性LUMO cube和12份阴离子spin cube均可追溯到相应log/fchk；积分0.999576–0.999871，几何/原子序匹配。新增2号两构象各两溶剂同样支持该拓扑，烯酮区域轨道norm约0.564–0.566、自旋约0.635–0.637仅为指定分区的描述。25分人工规则比较空间物理分布，不比较相位配色，不设原子百分比阈值，不把单一中性轨道图当成实际还原态验证。作者2号原构象归属仍hold。

### rule_solvent_relationship

要求检验溶剂变化并界定解释范围。3从DCM到ACN/DMSO的LUMO降低0.029032/0.031293 eV，对作者0.030/0.032，差−0.000968/−0.000707；对应公开Epc由−2.019到−1.859/−1.851 V。两种极性溶剂间本地轨道变化约−0.002261至−0.004279 eV，量级小；但是1/2/3/4/5实测DMSO−ACN为+15/−21/+8/−15/−37 mV，而计算LUMO均微降，不能声称预测了2/4/5变化方向。25分原人工规则支持3的主要方向及小变化量级的有限比较，不认证绝对电位或所有微小溶剂趋势；源表5号0.005 eV不能被正文“<0.004”误设为硬上限。

### rule_evidence_validity

证据有效性逐结果约束，不独立赋科学分。父级直接重读2号8组，独立复核重读总25组log/fchk并检查24 cube：分子图、E构型、电子数、几何和完整正频率相符。12阴离子与4个2号中性有显式Stable且同根；其他9个中性只有收敛的受限单重态Opt/Freq，不能写全部25态显式Stable或全局最低。2号34原子、142/143电子、96正模；其他物种分别按3N−6核验。部分Gaussian按negligible-force结束，位移NO保留。程序正常结束只是一项条件，不能替代分子身份/态/物理量和波函数来源检查。

### rule_answer

综合结论是3–5有有限结构–还原性质关系，1和新增真实计算的2显示统一LUMO描述不足，轨道/自旋共同支持离域受电子区域，3的较大溶剂变化有方向支持而ACN/DMSO微小变化存在解释边界。该结论来自实算与实验的对比，不是照抄Epc排名，也没有证明唯一取代效应或直接计算绝对电位。本条不重复分配科学分。当前科学覆盖父审通过与旧qualification中的NOT_VERIFIED_FOR_NEW_SCOPE/来源校准冻结并列；本次只更新计算档案，不给官方总分、不宣称已发布。

---

# 历史验证记录（原文保留；当前状态以上方最新汇总为准）

<!-- PARENT_09C8_PUBLIC_SCOPE_ACCEPTED_20261015 -->

## 2026-10-15 当前五化合物科学问题验收

父级验收时间：2026-10-15T05:12:56.012193+00:00。**当前公开科学问题的计算验证通过，`current_scope_verified=true`；正式来源/评分资格仍冻结，`release_ready=false`，官方总分不赋值。** 本条更新此前仅覆盖1/3/4/5、随后撤回完整通过登记的状态；不更改历史原始结果。

当前题面要求提出并检验五个查尔酮跨结构和溶剂的分子解释，并识别其适用范围。正文第2页方法、第14页关系讨论与SI坐标经过核对；沿作者B3LYP/6-311+G(2df,2p)、IEF-PCM及中性/还原态路线得到真实结果。父级独立重读新增化合物2的8份log/fchk；独立复核进程重核全部25组log/fchk、24份cube及72个已有哈希，分子图、E构型、原子/电子数、完整正频率和几何一致。

|当前科学问题部分|已完成证据及判定|
|---|---|
|3–5关系与1的偏离|两溶剂均得到3→4→5的LUMO升高；1与3仅差0.005490/0.005212 eV，而Epc相差0.163/0.170 V，支持有限关系及其失效范围。|
|化合物2的实际覆盖|SI起点A与结构明确的B各完成两溶剂中性/阴离子优化、96正频率和同根Stable。中性B−A自由能为0.783132/0.759914 kcal/mol；两个构象均有比3高的LUMO、但实验Epc更正，均支持与1类似的关系偏离。未声称穷尽构象或唯一对应作者E1/E2。|
|五分子的电子接受区域|12个中性轨道和12个还原态自旋cube均有原生波函数来源；共轭烯酮区域重要且分布延伸至芳环。独立网格积分0.999576–0.999871；片段积分仅为描述，不新设百分比阈值。|
|溶剂行为和边界|3从DCM到ACN/DMSO的LUMO降低0.029032/0.031293 eV，作者为0.030/0.032，主要趋势一致。ACN/DMSO轨道变化均小；实验1/2/3/4/5变化为+15/−21/+8/−15/−37 mV，不认证2/4/5微小变化方向预测。|

**保留的数值和方法边界：** 1/3/4/5绝对LUMO仍低于作者0.126783–0.136391 eV；化合物2的A/B候选与未唯一归属的作者标量差约0.074449–0.141718 eV。这些不是已经精确复现的标量，未使用拟合偏移、新容差或论文值替代计算。当前任务及活动规则要求检验关系、空间分布及解释边界，未要求匹配绝对电位或上述未校准标量，因此这些差异不推翻已得到的有限关系和反例。

所有12个阴离子及4个化合物2中性模型有显式Stable且保持原根；其他9个中性模型为收敛的限制性单重态Opt/Freq，不能写成全部25态都显式通过Stable或全局基态已证明。部分优化按Gaussian negligible-force条件结束，位移NO如实保留。唯一因果机制、精确电化学电位、完整构象群体和全部微小溶剂变化方向均未认证。

正式`qualification.json`的source-definition/calibration hold及原评分规则原样保留，未赋官方总分，未发布。科学覆盖验收记录与正式资格限制分列，不因隐藏规则排除化合物2便直接通过五分子题面；本次新增通过依赖化合物2的实际补算和独立检验。

[父级原生核查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/parent_09c8_native_crosscheck.json) · [独立科学意见](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_by_lane06.md) · [25组原生与24份空间数据核查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_native_checks.json)。


以下为按各自日期保留的核收历史。

<!-- LANE_A_04_20261015T014600Z_FINITE_RETURN -->

溶剂比较边界更正：ACN→DMSO实验Epc依次变化1:+15、2:−21、3:+8、4:−15、5:−37mV，而所有计算中性LUMO均微降。只认证ACN/DMSO轨道变化幅度小，以及3从DCM到ACN/DMSO的较大方向趋势；这些微小轨道变化不能预测2/4/5的Epc方向，不是绝对电位计算。

有限返回核收，2026-10-15

五分子已有原生neutral/anion与溶剂比较。新2号A/B八例图/电荷自旋/E几何保持，96正频、Stable能量不变；5例四YES，3例Gaussian negligible-force合法结束（位移NO披露）。2号A ACN/DMSO LUMO−2.634554/−2.637718，B−2.567449/−2.570760eV，两候选均比3高而Epc更正，支持1/2对3–5关系的偏离。2号中性enone区|ψ|²56.4–56.6%、anion|spin|48.3–48.7%，余量延伸芳环。三active rules复现，公开五分子问题已有有边界解释；提报父级独立核收，未自行计PASS。

三项活动定性科学结论已复现，公开五分子问题的有边界解释提报父级独立核收。此条不自行更新严格PASS统计。精确作者标量/构象源定义与calibration hold保持，release_ready=false；无新容差、绝对偏移或拟合Epc。

必要科学边界：

- 精确作者Table4溶液轨道数值与2号E1/E2物性归属仍未证明；这些源标量不转为新的题面要求。
- release_ready=false；源定义/标量calibration hold原样保留。

后继与预算：

- 父级独立核收五分子有边界科学解释；不为拟合作者标量重算或移动绝对轨道能。

新增作业：无。本次末查活动作业：无。

证据与比较：

- [five_compound_rule_review.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/five_compound_rule_review.json)，sha256 175df1677a4b17d3fa3fa21088ed19f03f2ce421328d2c1cef814fe6884d97a9
- [compound2_native_cube_fragment_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/compound2_native_cube_fragment_audit.json)，sha256 0a463225604dd5377b5479e465e49623b92f900df0e6fe72b40a3ab4d051d72f

[逐项数值、作者参照与保留原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/current_round_numerical_comparison.json)；[完整当前报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/current_round_verification_report.md)；[返回作业/累计成本来源](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/attempt_20261015T014600Z/returned_jobs.json)。

以下历史段落完整保留，只适用其记录时点。
<!-- END_LANE_A_04_20261015T014600Z_FINITE_RETURN -->

<!-- LANE_A_04_20261014T143300Z_VERIFIED_INTAKE -->
paper_09c8aaf14b70371f — 当前公开问题核收记录，2026-10-14

**current_scope_verified=false；本轮没有整题PASS。** 以下内容为当前状态；后附旧段落仅保留其当时含义。

公开问题包含五种化合物；1/3/4/5有效结果复用，compound2两种E候选×两溶剂×中性/阴离子共8项Opt/Freq/Stable仍排队。三个compound3固定几何诊断已正常完成，ε差异和SI几何均不能解释约0.13 eV的LUMO残差。气相Hamiltonian作用于ACN优化几何得到−2.534245 eV、接近作者ACN−2.538，仅为来源定义线索。

三个单点均1次正常终止、28原子0/1、同输入几何及fchk一致：ACN几何/气相−2.5342447965、SI几何/ACN PCM−2.6405926737、ACN几何/ε27.5 PCM−2.6670461085 eV。原ACN PCM−2.6697343785对作者−2.538残差保留。ε改动仅+0.00268827 eV，SI几何改动+0.02914170 eV。气相Hamiltonian数值接近是定义线索，不证明作者计算约定。

S²摘要已独立更正：旧宽正则误抓SCF迭代次数15/14/14；明确Gaussian S**2行的正确结果均为空（闭壳层未打印该记录）。原回执/原生日志/fchk保留；已归档旧runner，后续解析器只改此显示字段，不改成功、稳定性同根或频率门控，不重算QC。

当前缺口：

- compound2尚无原生计算输出；不能将隐藏评分排除项视作完整公开问题已覆盖。
- compound2源E1/E2与Table4/Fig11/12物性唯一归属仍不明。
- 作者溶液轨道能定义尚未证实；不能因气相单点接近而更换作者Hamiltonian或拟合偏移。

下一步：

- 收取既有8项的Opt/Freq/Stable与LUMO/自旋cube，按原子图、E构型、态、驻点、完整正频及稳定性根逐项核收。
- 使用本轮三SP诊断定位来源差异；若获得作者轨道输出/输入，仅做定义核对，保留全部直接PCM值。

已提交且首查的新增ID：hpc-job-04175526-5a3c-4cd2-976a-09b56342fe34, hpc-job-7923e98f-fa01-4300-acd6-1b27b6d4c49f, hpc-job-f25e9feb-9cdf-46cf-967a-f45e7191ebaf, hpc-job-a2e14064-861f-4ba6-a24b-8a61c54c81f7, hpc-job-ef4620b1-3729-41c0-ae87-01bacdcb8db7, hpc-job-3ed5762b-df3c-4b16-b943-fcc5895324ed, hpc-job-7d472501-b048-4877-9f20-25048eb612a4, hpc-job-a606be19-4f82-4d84-bf11-f9ce786de8ad, hpc-job-e9e637e7-f866-4e5b-9c26-4a8627021f22。

活动ID（2026-10-14T16:49:30.550217+00:00）：hpc-job-3ed5762b-df3c-4b16-b943-fcc5895324ed, hpc-job-7923e98f-fa01-4300-acd6-1b27b6d4c49f, hpc-job-7d472501-b048-4877-9f20-25048eb612a4, hpc-job-a2e14064-861f-4ba6-a24b-8a61c54c81f7, hpc-job-a606be19-4f82-4d84-bf11-f9ce786de8ad, hpc-job-e9e637e7-f866-4e5b-9c26-4a8627021f22, hpc-job-ef4620b1-3729-41c0-ae87-01bacdcb8db7, hpc-job-f25e9feb-9cdf-46cf-967a-f45e7191ebaf。

[本轮完整报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/current_round_verification_report.md)；[逐项数值/原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/current_round_numerical_comparison.json)；[原生/执行器回执](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/current_round_native_observation.json)。

- [compound3_minimal_diagnostic_returned_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/compound3_minimal_diagnostic_returned_audit.json)；SHA256 `0ad2c29461ff0d6de411a940b9058472af42e128bb83255438de7fe20e110caf`。
- [S2_parser_correction_audit_20261014.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/S2_parser_correction_audit_20261014.json)；SHA256 `6dd31e4826cf3ef7ffb20d9c9d635fb82802abc836b9578cadcbea9027231e0d`。

公开任务、输入、评分与容差保持原字节；历史失败成本保留，不以平台SUCCEEDED或诊断频率宣布驻点。
<!-- END_LANE_A_04_20261014T143300Z_VERIFIED_INTAKE -->

<!-- FULL_PUBLIC_QUESTION_COVERAGE_RECHECK_20261014 -->
# 2026-10-14 完整公开科学问题覆盖复核

更新时间：2026-10-14T14:41:54.393671+00:00。**current_scope_verified=false；完整五化合物问题尚未验证完成。**

公开题面明确包含 five supplied chalcones。此前 PASS 只核过 1/3/4/5 的受限范围，不能据评分排除项认定完整题面已经完成。既有 17 个有效波函数、9 个 LUMO 值、16 份空间分布证据继续保留，化合物 2 目前缺少经科学核验的中性/还原态溶剂证据。

化合物 2 的来源歧义已具体定位：主文物理第 10 页 Table 6 有低能 E1/E2，而 SI 第 24–25 页仅给一套未标构象/溶剂的坐标。现以原 SI 和保持完整分子图及 E 烯酮构型的 ring-B 180° 候选分别计算乙腈/DMSO 的中性态与阴离子；这是来源支持的候选诊断，不能按接近数值反推作者唯一构象。

既有绝对溶剂 LUMO 残差 0.1268–0.1364 eV 保留。化合物 3 旧气相 fchk 第一虚轨道为 −2.5069840679 eV，作者为 −2.507 eV；这提示检查溶剂/几何处理，但尚未证明偏差成因。另提交三个固定几何单点诊断，分别隔离气相反应场、作者 SI 几何及正文乙腈 ε=27.5 的差异，不拟合偏移或介电常数。

本轮已真实提交 9 个 HPC 作业（8 个 Opt/Freq/Stable、1 个含 3 单点的诊断作业，总计 164 CPU）。首次检查 2026-10-14T14:39:55.030871+00:00 全部 QUEUEING / NOT_STARTED；平台受理不代表原生完成或科学通过。单构型原生计算上限 12 小时、诊断单点各 1 小时，不承诺排队或完成时间。

[本轮独立记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/verification_report.md)、[完整作业收据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/submitted_jobs.jsonl)、[首次原生检查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/coverage_recheck_20261014T135000Z/first_native_check.json)。本条为最新判断，以下历史 PASS/当前范围表述原样保留作过程记录，不能覆盖上述完整题面结论。

---

# 最新验证范围与状态：2026-10-13 07:30 UTC有限续接

更新时间：2026-10-13T08:23:11.050136+00:00。**PASS_CURRENT_SCOPE_MANUAL**；current_scope_verified=true。

父审通过的当前1/3/4/5定性范围继续有效，实际科学任务哈希未变。复用17个中性/阴离子波函数、9个LUMO值和16份空间分布证据；3→4→5排序、1/3的适用边界及溶剂趋势保持。没有新量化计算。

未完成/阻碍：当前活动范围无计算阻碍；绝对LUMO源/本地差0.1268–0.1364 eV仍在，不是逐数值复现。2号E1/E2归属SOURCE_BLOCKED但已被实际合同排除活动评分。Fig11轨道振幅与密度单位歧义保留。

本轮新作业：无。排队中的作业尚无原生应用结果。

逐目标覆盖、作者/本地差异、原容差、累计预算和精确后继：[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T073000Z/verification_report.md)；[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T073000Z/coverage.json)；[successor](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T073000Z/successor.json)。

历史PASS与“当前”措辞仅在各自时间/范围成立，不自动覆盖本次活动范围。以下完整保留此前记录。

---

<!-- GROUP_A_CONTINUATION_20261013T030303Z -->
# 最新验证状态（2026-10-13）

2026-10-13T03:49:16.117291+00:00；任务SHA256 `d555f1ab4860a5353b05543c0e1f15f48aa18ed369a247bf0c3e6f56c69b230f`；**PASS_CURRENT_SCOPE_MANUAL**；current_scope_verified=true。

当前活动范围1/3/4/5全部完成。本轮收取的上轮16个Opt/Freq结果和旧3/ACN最低点合格；八个阴离子稳定性检查均already stable且能量不变。17个波函数支撑9个中性LUMO能量及8+8中性/阴离子空间分布；15个新cube与旧3/ACN cube逐一核过原子、轨道号、单位和网格积分并亲读图。3→4→5在ACN/DMSO中LUMO逐渐升高；1/3仅差0.00549/0.00521eV但实测Epc差0.163/0.170V，共同关系不能普遍外推。DMSO−ACN只−0.00226至−0.00428eV，3从DCM到ACN/DMSO降低0.02903/0.03129eV。中性受电子轨道与还原态自旋都支持共轭烯酮并延伸至芳环。

限定/阻碍：当前活动目标无计算阻碍。源绝对LUMO比计算高0.1268–0.1364eV，原差保留，未拟合/平移；Fig11把轨道等值面标为密度单位，故并列振幅/带符号密度解释，不声称完全重现源等值面。2号E1/E2来源归属仍SOURCE_BLOCKED但已由实际合同排除活动评分。此处PASS仅指当前定性比较范围，非绝对电位或逐位源数值复现。

逐目标[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/coverage.json)、[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/verification_report.md)及[精确后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/successor.json)。

活动作业：无。

以下旧版本原文完整保留为历史；其中旧PASS/“当前”或撤销范围不能覆盖上面的当前判断。未修改任何科学任务/评分/容差。

---

<!-- CORE7_CONTINUATION_GROUP_A_20261012 -->
# 最新验证范围与状态

2026-10-12T20:29:07.460936+00:00；当前任务SHA256 `d555f1ab4860a5353b05543c0e1f15f48aa18ed369a247bf0c3e6f56c69b230f`。**当前整题未严格通过**；科学状态 `PARTIAL`。

当前任务已转为系列还原构效关系。复用3/ACN的合格E最低点及其波函数，取消旧E/Z热互变验收。原生最终LUMO为−2.669709 eV，论文−2.538；差−0.131709保留。1/3/4/5的中性及还原态ACN/DMSO、3中性DCM作业已提交，尚不足判断完整系列/空间分布。 旧checkpoint导出已成功；原子/电子数、能量和坐标已与原生日志核对，几何RMSD5.27e−7Å。fchk完整精度LUMO为−2.669734379eV（日志舍入−2.669709），与源差−0.131734379eV；首次轨道56的cube后处理已提交。

阻碍：系列计算及可追溯LUMO/自旋密度图待完成。2号E1/E2属性归属仍缺来源，但已明确在当前活动评分之外，不据此制造整题失败。没有新数值窗口。

本轮报告：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/verification_report.md；逐目标覆盖：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/coverage.json；作业及后继：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/core7_upgrade_20261012T190159Z/successor.json。

当前活动作业：hpc-job-9eff1e9d-f79a-4332-94e5-8caa7263b0bc, hpc-job-d16fa6cd-a79b-4e18-a95c-b2245a2c87e3, hpc-job-a1dede8a-2bfa-406c-be33-87924c3c574b, hpc-job-92f6e425-6c6a-429d-a4be-059fa5e091b3, hpc-job-f563774b-ba8d-41df-90de-4340c13551ae, hpc-job-0b678115-24cf-4865-86b8-bc38062ed1a6, hpc-job-00b522a3-307e-43f2-8ac0-8cbe36a8cab1, hpc-job-7c3b748c-355e-4b90-bb4e-18e4a5b600d1, hpc-job-4763bdfe-4c04-47c0-89be-46c703d02c1c, hpc-job-d4055d6b-757a-4630-8290-dc956c347936, hpc-job-9521c45c-6f6a-4d49-b800-e362355762d7, hpc-job-45fd2532-6d25-4776-bddb-5b31e14742ee, hpc-job-c4e4e32d-fa69-40e8-8f6d-b2d18080d245, hpc-job-e958ec5e-ec9e-4e4d-8c0e-fc61993ac417, hpc-job-92338414-668a-43f2-9705-8276be40e74f, hpc-job-be2dbd73-1121-40a1-85f7-bbf4d6ac950b, hpc-job-18ce1c66-a6a0-4601-8891-f8831ebeb035。

下列旧版本完整保留为历史；其中PASS、“当前”或旧范围结论不自动覆盖本轮实际合同。

---



<!-- phase2-verification-20261010T231612Z-group01 -->

## 2026-10-11 phase2 / group01 独立计算验证

状态：**COMPUTING**；科学结果状态：`INCOMPLETE`。审查绑定冻结输入包SHA256 `b1455ce39a10636963da16610eef71c000125b5440cb438c8264ccf8e7dd6509`；该科学合同未变更。追加证据后的当前包hash见本轮group_01/manifest_changes.json及completion.json，避免在自哈希文件内循环引用。

完整逐篇报告：[paper_09c8aaf14b70371f verification_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/verification_report.md)；逐目标记录：[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/coverage.json)；原生重组：[reassembled_results.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/reassembled_results.json)；本篇日志与哈希：[native_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/native_audit.json)。

这是可查看作者路线的参考验证，不是自主盲测。原有历史保留；本条针对当前集合与冻结范围的最新判定。全部必需科学目标实际验证：False。

| 当前目标 | 本轮状态 | 实际证据/缺口 |
|---|---|---|
| ar_kp1 | PARTIAL | 存在直接TS、约束扭转扫描、端点引导QST3等有记录的候选策略。 尚未选出最低已连接路线，搜索覆盖有限。 |
| ar_kp2 | COMPUTING | 三个最低点已验；气相QST3正在运行。 两个介质均未有唯一扭转虚频并连接E/Z。 |
| ar_kp3 | COMPUTING | 源目标1.43eV/92.5°；没有符合连接门槛的实际值。 气相TS/IRC缺。 |
| ar_kp4 | PARTIAL | 源目标1.42eV/92.5°；乙腈扫描只支持初猜。 乙腈TS/IRC缺。 |
| ar_kp5 | PARTIAL | 气相Z−E0.286009eV，差+0.056009；乙腈E最低点已验。 乙腈Z最低点在算，乙腈0.27eV未验。 |
| ar_c1 | PARTIAL | 已验证气相E更稳，未恢复两介质连通的~92.5°高势垒路径。 最终势垒与介质比较未闭合。 |
| ar_c2 | PARTIAL | 未把热路径当光化学或实验速率。 无真实TS势垒不能确认热动力学阻滞尺度。 |

| 数值规则 | 源值 | 实际值 | 实际−源 | 原容差 | 单个数值命中 |
|---|---:|---:|---:|---:|---|
| ar_r3 / eV | 1.43 | None | None | 0.15 | False |
| ar_r4 / eV | 1.42 | None | None | 0.15 | False |
| ar_r8 / degrees | 92.5 | None | None | 2.0 | False |
| ar_r9 / degrees | 92.5 | None | None | 2.0 | False |
| ar_r10 / eV | 0.23 | 0.28600892146612517 | 0.056008921466125156 | 0.15 | True |
| ar_r11 / eV | 0.27 | None | None | 0.15 | False |

数值命中独立于身份/连接门；Rh、BN的节点差不能据此获得全任务PASS。None表示必需值尚未取得，未用约束峰、错误构象或别的能量参照替代。

未完成/阻塞：

- 气相和乙腈均无验收的唯一扭转虚频TS及E/Z双向连接。

- 乙腈Z尚未完成自由Opt/Freq；当前两介质的最终势垒/溶剂效应不能PASS。

新作业与资源/时间：[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/jobs.json)；复用计算步数和可恢复原生CPU/elapsed：[resource_accounting.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/resource_accounting.json)；可恢复后继：[resume_state.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/resume_state.json)。没有周期resume或新Codex/子代理。

acn_Z_released_minimum=hpc-job-49a46b3b-2be8-4efb-adb8-94e5937e3d4f (RUNNING), gas_EZ_QST3=hpc-job-b1279d26-38c8-4d9d-b67f-fb6c780ad5d7 (RUNNING).


<!-- group01-native-return-and-storage-update -->

### 2026-10-11 本轮收取与后继更新

乙腈Z新作业hpc-job-49a46b3b-2be8-4efb-adb8-94e5937e3d4f已正常完成。28原子0/1、78正模、与E全元素图同构，中央扭转Z1.640198°、E179.106081°。Z−E=0.298462212eV，对源0.27差+0.028462212eV，在不变±0.15内。因此ar_kp5所需四最低点和气相/乙腈差值均已通过；气相QST3及两介质真实鞍点/双向连接仍缺，整篇保持COMPUTING。原生elapsed3468.9s、CPU69100.4s，平台实例Deleted。

本条更新前文相应作业/目标状态；最新细节见[paper_09c8aaf14b70371f verification_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/verification_report.md)、[new_results.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/new_results.json)和[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/small_molecules_20261010T231612Z_g01/jobs.json)。所有其他未通过项保留。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`fb11cf2dbf8ec33e43c7516c7cc13d505c54623e5dc75570dde7863487d2b1f1`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_09c8aaf14b70371f/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_09c8aaf14b70371f/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_09c8aaf14b70371f/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。

## 2026-10-12 approved series-scope upgrade (chalcone-series-redox-20261012)

**Current new-scope status: NOT_VERIFIED_FOR_NEW_SCOPE; release_ready=false.** This appendix supersedes historical task requirements above, not their recorded scientific outcomes. No quantum calculations, HPC submissions or live job polls were performed for this upgrade.

The current task asks about five-chalcone reduction structure-property relationships (Table 4/Figs.11-14). Gas/ACN E/Z paths, Z-E gaps and thermal hindrance are no longer scored. Historical source numbers and tolerances remain unchanged in qualification.json; their retirement is not a PASS.

The latest inspected legacy audit is dated 2026-10-12T15:20:40.004320+00:00: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/remaining24_20261012T134810Z_group_A/verification_report.md. Overall MISMATCH: the returned QST3 candidate has a -7.748784-degree central dihedral, one -56.4847 cm^-1 mode and a diagnostic 0.605513 eV gap, so it is not the source near-orthogonal E/Z saddle. No current job status was inferred from older RUNNING entries. Four validated E/Z minima remain valid within their original scope; Z-E values 0.286008921/0.298462212 eV are historical support only.

Reusable native evidence (accepted geometry/frequency scope only):

| Model | Native output | SHA256 |
|---|---|---|
| 3/E gas | /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/artifacts/gaussian/chalcone_E_b3lyp_opt_freq_retry2/stdout.log | 37a41dbd616f7cdcc8b7a0a16f8879a2c9a4b14dd2dba02eac14f344ac2e974b |
| 3/E ACN | /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_3/paper_09c8aaf14b70371f/provenance/qzcli_hpc/chalcone_E_author_IEFPCM_acetonitrile_optfreq_20260915/20260915T095707480436Z_hpc-job-2004465-cluster-slurmd-0/gaussian.log | 366f18241fc3a113045b314d4130186cdcdced0dd7ba87ac6de52a6411d36724 |

Both are neutral C15H12O singlet minima with 78 positive modes in the recorded audit. Reuse those optimized geometries/frequency checks and inspect native orbitals/checkpoints before rerunning anything. This appendix does not newly certify orbital energies or spatial distributions.

New evidence still needed: author-comparable solution neutral orbitals, paired neutral/anion distributions, and linked series/solvent comparisons. Compound 2 is on a source-definition hold because Table 6 E1/G and E2/E minima cannot silently be interchanged in the Table 4 property reference. Its dependent targets are outside active acceptance requirements until attribution is resolved; removing them does not certify the five-member scope. All new numerical references lack calibrated windows and are handled by manual scientific comparison. No new tolerance has been created.

See qualification.json, target_map.json and validation_plan.json for current applicability, native-success requirements and the author-only verification delta. DCM verification is restricted to compound 3 neutral orbital results, not a new anion reference. The approved implementation is not scientific verification or release approval.

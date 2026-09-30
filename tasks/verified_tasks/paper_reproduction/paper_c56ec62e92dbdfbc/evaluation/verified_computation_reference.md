# 已验证计算参考：paper_c56ec62e92dbdfbc / paper_reproduction

> 2026-09-29 修后同步：任务修复和当前评分映射见第 3、6 节；全部仍在 verified_tasks，未获迁移确认。
核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/paper_reproduction/paper_c56ec62e92dbdfbc`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 2。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16，气相 B3LYP-D3BJ/6-31G(d) Opt/Freq，ωB97XD/6-311++G(d,p) PCM Xylene-mixture 高层单点；各模型中性单重态。GoodVibes 4.3，298.15 K、1 M、Grimme 100 cm⁻¹ 熵修正、无准谐焓修正、频率比例 1。四个来源 TS 各 116 原子、342 模，分别只有一个负频率；八个 QRC 优化端点全为 342 个正频率。另有 catalyst 4i、1a、2a、MeOH 四个已验证参照组分及单点。正文物理第 5 页 Figure 2、SI 74–75、85 页；SI 普通方法 6-31G(d) 与构象段 6-31+G(d) 不同，未静默合并。作者 Perl 热修正实现未取得，GoodVibes 是明确替代实现。

论文来源：[正文](../../../../../papers/paper_c56ec62e92dbdfbc/documents/main.pdf)；[SI](../../../../../papers/paper_c56ec62e92dbdfbc/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

公开 4i、1a、2a 的 82/20/26 atom XYZ 及 system.json 为分离反应物输入，均可解析；没有给最终 TS、R/S 能差或优胜路径。催化剂构型/键表由系统文件定义。既有作者 TS 只出现在私有验证档；本次没有新增到 agent_input。

## 2. 有效计算链、结果与推导

G_i=E_high,i+(G_qRRHO,low,i−E_low,i)。所有 TS 的配平参照为 G(TS)+2G(MeOH)−G(4i)−G(1a)−G(2a)，不能遗漏 2 MeOH。四个共同参照高度：CC_R 11.760297125、CC_S 13.738713650、dep_R 7.430898304、dep_S 9.564634049 kcal/mol；ΔΔG‡=S−R=1.978416525（源 2.0±1.0），支持 R 与 C–C 形成决定选择性。四个 TS 的虚频依次 −345.8570、−410.3163、−1030.3150、−973.0562 cm⁻¹。有机片段的连接与产物 CIP 溯源见独立立体化学档；不能用中间体局部 CIP 字母直接替代最终 R/S。两个步骤各 TS→端点有证据，但完整催化剂复合物盆地同一性及宏观动力学网络没有认证。有限四个作者最低代表 TS 及来源构象筛选，不认证重新执行 CREST 或独立搜索收敛。

| 组分/TS | G高层+qRRHO / Eh | 共同参照G / kcal mol⁻¹ |
| --- | --- | --- |
| TSCC_R | -14570.6235956325 | 11.7602971252 |
| TSCC_S | -14570.6204428251 | 13.7387136498 |
| TSdep_R | -14570.6304949687 | 7.4308983040 |
| TSdep_S | -14570.6270946444 | 9.5646340491 |
| catalyst_4i | -13801.1633312937 | — |
| reactant_1a | -461.1611264320 | — |
| reactant_2a | -539.7065500027 | — |
| MeOH | -115.6943354347 | — |

## 3. 修后当前必评关键点与结论覆盖（2026-09-29）

本表对齐本包当前五个 evaluator JSON。历史真实计算链及数值仍见第 2、4、5 节；reference 不新增评分门槛。

| 当前 ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| kp_process_ts / process | Every retained R- and S-forming transition-state candidate is explicitly identified and validated as a first-order saddle with the intended bond-forming mode and path connectivity. | 四个一虚频鞍点+八个QRC优化正频端点；R/S取最终产物片段CIP映射，不按文件名猜。 | r_ts |
| kp_process_coverage / process | The investigation covers distinct stereochemical/pathway and conformational families and declares a scientifically justified stopping basis. | 四个作者最低TS代表覆盖两配置和两步；有高层/热化学敏感性，未认证自主CREST或采样收敛。 | r_coverage |
| kp_result_ordering / result | The lowest validated R- and S-forming C–C pathways are compared on one separated-reactants free-energy reference. | 共同分离反应物并补2MeOH的CC_R/S=11.760297/13.738714，差1.978417；原2±1。 | r_delta |
| kp_result_mechanism / result | The selectivity conclusion identifies C–C bond formation as the enantiodetermining event and discusses the subsequent rearomatization barrier comparison. | 共同参照dep_R/S=7.430898/9.564634低于各CC分支，支持有限路线C–C决定选择性；非完整动力学网络。 | r_mechanism |

| 结论 ID / 角色 | 当前科学主张 | 支持关键点及边界 |
| --- | --- | --- |
| c_final_selectivity / final | The submitted validated pathway comparison supports a specific favored configuration and identifies the event controlling enantioselectivity within the stated monomeric model. | kp_process_ts, kp_process_coverage, kp_result_ordering, kp_result_mechanism。现有四个作者代表 TS 支持有限路线的 R/S 能差与步骤比较；不能据此认证所有竞争家族的自主采样已收敛，也未认证完整催化剂复合物盆地连接或全局动力学网络。现行 coverage 要求未降级。 |

修前→修后：关键点 4→4；结论记录 1→1。现有结论为科学成果，不另给普通免责声明计分。真实计算支持范围不因本次改关联而扩大。

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | author_reactant_1a_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/artifacts/gaussian_batch/author_reactant_1a_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/artifacts/gaussian_batch/author_reactant_1a_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq/stdout.log) | [0, 1] | -461.3336637300 | -461.2028950000 | 54 / 0 / 35.4802 | native normal |
| 2 | author_reactant_2a_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/artifacts/gaussian_batch/author_reactant_2a_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/artifacts/gaussian_batch/author_reactant_2a_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq/stdout.log) | [0, 1] | -539.9694357190 | -539.7842860000 | 72 / 0 / 49.3071 | native normal |
| 3 | author_TSCC_R_SI_main_method_optfreq_20260923_20260923T133200Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_SI_main_method_optfreq_20260923_20260923T133200Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_SI_main_method_optfreq_20260923_20260923T133200Z/stdout.log) | [0, 1] | -14561.8932854000 | -14561.1935550000 | 342 / 1 / -345.857 | native normal |
| 4 | author_TSCC_R_computed_mode_QRC_minus_optfreq_20260925_20260925T163549Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_computed_mode_QRC_minus_optfreq_20260925_20260925T163549Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_computed_mode_QRC_minus_optfreq_20260925_20260925T163549Z/stdout.log) | [0, 1] | -14561.8984296000 | -14561.1996300000 | 342 / 0 / 8.0215 | native normal |
| 5 | author_TSCC_R_computed_mode_QRC_plus_optfreq_20260925_20260925T162411Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_computed_mode_QRC_plus_optfreq_20260925_20260925T162411Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_computed_mode_QRC_plus_optfreq_20260925_20260925T162411Z/stdout.log) | [0, 1] | -14561.9129114000 | -14561.2109770000 | 342 / 0 / 9.5203 | native normal |
| 6 | author_TSCC_R_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T114258Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T114258Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_R_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T114258Z/stdout.log) | [0, 1] | -14571.3466462000 | — | — | native normal |
| 7 | author_TSCC_S_SI_main_method_optfreq_20260923_20260923T133216Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_SI_main_method_optfreq_20260923_20260923T133216Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_SI_main_method_optfreq_20260923_20260923T133216Z/stdout.log) | [0, 1] | -14561.8948010000 | -14561.1943290000 | 342 / 1 / -410.3163 | native normal |
| 8 | author_TSCC_S_computed_mode_QRC_minus_optfreq_20260925_20260925T162456Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_computed_mode_QRC_minus_optfreq_20260925_20260925T162456Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_computed_mode_QRC_minus_optfreq_20260925_20260925T162456Z/stdout.log) | [0, 1] | -14561.9111953000 | -14561.2088550000 | 342 / 0 / 12.6573 | native normal |
| 9 | author_TSCC_S_computed_mode_QRC_plus_optfreq_20260925_20260925T162440Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_computed_mode_QRC_plus_optfreq_20260925_20260925T162440Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_computed_mode_QRC_plus_optfreq_20260925_20260925T162440Z/stdout.log) | [0, 1] | -14561.9078888000 | -14561.2078170000 | 342 / 0 / 9.8283 | native normal |
| 10 | author_TSCC_S_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T120436Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T120436Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSCC_S_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T120436Z/stdout.log) | [0, 1] | -14571.3447279000 | — | — | native normal |
| 11 | author_TSdep_R_SI_main_method_optfreq_20260923_20260923T133232Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_SI_main_method_optfreq_20260923_20260923T133232Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_SI_main_method_optfreq_20260923_20260923T133232Z/stdout.log) | [0, 1] | -14561.8852221000 | -14561.1882130000 | 342 / 1 / -1030.315 | native normal |
| 12 | author_TSdep_R_computed_mode_QRC_minus_optfreq_20260925_20260925T164630Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_computed_mode_QRC_minus_optfreq_20260925_20260925T164630Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_computed_mode_QRC_minus_optfreq_20260925_20260925T164630Z/stdout.log) | [0, 1] | -14561.9076650000 | -14561.2069390000 | 342 / 0 / 9.4041 | native normal |
| 13 | author_TSdep_R_computed_mode_QRC_plus_optfreq_20260925_20260925T162512Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_computed_mode_QRC_plus_optfreq_20260925_20260925T162512Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_computed_mode_QRC_plus_optfreq_20260925_20260925T162512Z/stdout.log) | [0, 1] | -14561.9064798000 | -14561.2062600000 | 342 / 0 / 10.71 | native normal |
| 14 | author_TSdep_R_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T115346Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T115346Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_R_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T115346Z/stdout.log) | [0, 1] | -14571.3503387000 | — | — | native normal |
| 15 | author_TSdep_S_SI_main_method_optfreq_20260923_20260923T133247Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_SI_main_method_optfreq_20260923_20260923T133247Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_SI_main_method_optfreq_20260923_20260923T133247Z/stdout.log) | [0, 1] | -14561.8823118000 | -14561.1860850000 | 342 / 1 / -973.0562 | native normal |
| 16 | author_TSdep_S_computed_mode_QRC_minus_optfreq_20260925_20260925T164704Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_computed_mode_QRC_minus_optfreq_20260925_20260925T164704Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_computed_mode_QRC_minus_optfreq_20260925_20260925T164704Z/stdout.log) | [0, 1] | -14561.9048478000 | -14561.2068570000 | 342 / 0 / 5.129 | native normal |
| 17 | author_TSdep_S_computed_mode_QRC_plus_optfreq_20260925_20260925T164647Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_computed_mode_QRC_plus_optfreq_20260925_20260925T164647Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_computed_mode_QRC_plus_optfreq_20260925_20260925T164647Z/stdout.log) | [0, 1] | -14561.9103249000 | -14561.2099400000 | 342 / 0 / 10.1487 | native normal |
| 18 | author_TSdep_S_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T115402Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T115402Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_TSdep_S_validated_main_TS_high_basis_xylene_mixture_SP_20260925_20260925T115402Z/stdout.log) | [0, 1] | -14571.3466503000 | — | — | native normal |
| 19 | author_balancing_MeOH_gas_optfreq_20260926_20260926T090046Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_balancing_MeOH_gas_optfreq_20260926_20260926T090046Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_balancing_MeOH_gas_optfreq_20260926_20260926T090046Z/stdout.log) | [0, 1] | -115.7175093250 | -115.6887530000 | 12 / 0 / 345.5008 | native normal |
| 20 | author_balancing_MeOH_validated_minimum_xylene_high_SP_20260926_20260926T093318Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_balancing_MeOH_validated_minimum_xylene_high_SP_20260926_20260926T093318Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_balancing_MeOH_validated_minimum_xylene_high_SP_20260926_20260926T093318Z/stdout.log) | [0, 1] | -115.7261092890 | — | — | native normal |
| 21 | author_catalyst_4i_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq_hpc20_20260906T032916Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_catalyst_4i_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq_hpc20_20260906T032916Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_catalyst_4i_b3lyp_631gd_v5_b3lypd3bj_631gd_optfreq_hpc20_20260906T032916Z/stdout.log) | [0, 1] | -13792.0208560000 | -13791.5901120000 | 240 / 0 / 3.919 | native normal |
| 22 | author_catalyst_4i_balanced_reference_xylene_high_SP_20260926_20260926T093243Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_catalyst_4i_balanced_reference_xylene_high_SP_20260926_20260926T093243Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_catalyst_4i_balanced_reference_xylene_high_SP_20260926_20260926T093243Z/stdout.log) | [0, 1] | -13801.6149410000 | — | — | native normal |
| 23 | author_reactant_1a_balanced_reference_xylene_high_SP_20260926_20260926T085946Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_reactant_1a_balanced_reference_xylene_high_SP_20260926_20260926T085946Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_reactant_1a_balanced_reference_xylene_high_SP_20260926_20260926T085946Z/stdout.log) | [0, 1] | -461.2959510640 | — | — | native normal |
| 24 | author_reactant_2a_balanced_reference_xylene_high_SP_20260926_20260926T090025Z | [输入](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_reactant_2a_balanced_reference_xylene_high_SP_20260926_20260926T090025Z/input.com) / [原始输出](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/qzcli_hpc/author_reactant_2a_balanced_reference_xylene_high_SP_20260926_20260926T090025Z/stdout.log) | [0, 1] | -539.8956540750 | — | — | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 2, 21 | `#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 3, 7, 11, 15 | `#p B3LYP/6-31G(d) Opt=(TS,CalcFC,NoEigenTest,MaxCyc=300,MaxStep=10) Freq EmpiricalDispersion=GD3BJ NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 4, 5, 8, 9, 12, 13, 16, 17 | `#p B3LYP/6-31G(d) Opt=(CalcFC,MaxCyc=300,MaxStep=10) Freq EmpiricalDispersion=GD3BJ NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 6, 10, 14, 18, 20, 22, 23, 24 | `#p wB97XD/6-311++G(d,p) SP SCRF=(PCM,Solvent=Xylene-mixture) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 19 | `#p B3LYP/6-31G(d) Opt=(CalcFC,MaxCyc=300) Freq EmpiricalDispersion=GD3BJ NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |

## 5. 模型、连接与后处理原始出处

- [provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json)
- [provenance/author_answer_validation_20260926/QRRHO_REFERENCE_AUDIT.json](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/author_answer_validation_20260926/QRRHO_REFERENCE_AUDIT.json)
- [provenance/author_answer_validation_20260926/BALANCED_REFERENCE_AUDIT.json](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/author_answer_validation_20260926/BALANCED_REFERENCE_AUDIT.json)
- [provenance/resumption_20260926/STEREOCHEMISTRY/INDEPENDENT_RESULTS.json](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/provenance/resumption_20260926/STEREOCHEMISTRY/INDEPENDENT_RESULTS.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../../docs/verification/group_2/paper_c56ec62e92dbdfbc/report/results.json)
- [compute_c56_qrrho_author_20260926.py](../../../../../docs/verification/group_2/compute_c56_qrrho_author_20260926.py)
- [compute_c56_balanced_reference_20260926.py](../../../../../docs/verification/group_2/compute_c56_balanced_reference_20260926.py)

## 6. 修后包检查与未认证事项（2026-09-29）

当前策略为 `dual_axis_100.scientific_results.v1`；真实历史 report 对本包的实际输出检查：**通过**。本包已执行 14 个提交样例，每个分别经过 JSON Schema 和真实 validate_output_contract；合成正反例只测试格式，未加入本计算档案的科学证据。

现有四个作者代表 TS 支持有限路线的 R/S 能差与步骤比较；不能据此认证所有竞争家族的自主采样已收敛，也未认证完整催化剂复合物盆地连接或全局动力学网络。现行 coverage 要求未降级。

[逐包维护记录](task_provenance/maintenance_audit.md)及[集中报告第30节](../../../MAINTENANCE_REPORT.md)记录实际修改、检查与未闭合项。普通免责声明已取消必填及独立计分，身份/态/收敛/频率/路径/参考态和真实失败证据保留。

本次没有新电子结构计算、HPC 操作、完整 LLM 评分或 AR 盲测；没有迁移 final/hold。文件导出检查只覆盖 agent_input 物化，不能替代部署侧父目录、容器挂载和网络隔离。完整原始证据直接链接在第 4、5 节，不依赖 task_provenance 的长期存在。

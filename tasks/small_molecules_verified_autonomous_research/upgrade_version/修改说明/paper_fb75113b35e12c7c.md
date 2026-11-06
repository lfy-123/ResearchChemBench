# 第一轮专家反馈调整 — 2026-11-03

补PI1/PI2带映射2Z,4E结构与SDF、未排序候选位点及MeS-/MeSH；删PI3及15分，鲁棒性仅比较PI1/PI2；六项20/20/10/15/20/15。

原system.json含名称和文字连接式，但没有可解析结构。补PI1/PI2的映射SMILES/SDF并验证2Z,4E，提供alpha/delta/beta-prime未排序初始位点及独立的后续闭环位点。PI3属独立砜底物，按专家要求移出当前任务；旧证据保留为历史。保留PI1二次加成和PI1/PI2稳健性，避免把近简并端点排序写成唯一实验分布。

当前评分：PI1 单加成具有弱且依赖模型的位点选择性 20分；PI1 在所考察成环结局的竞争中偏向可达的简单加成 20分；PI1 的第二次 MeSH 加成具有弱热力学竞争力 10分；PI2 成环端点比简单加成物明显更稳定 15分；PI2 可达成环选择 γ 衍生的呋喃连接方式 20分；两个环烯酮底物的选择性可靠度比较 15分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_fb75113b35e12c7c：2026-10-29 最终结论分项统一

现行分项：PI1 单加成具有弱且依赖模型的位点选择性15分；PI1 在所考察成环结局的竞争中偏向可达的简单加成15分；PI1 的第二次 MeSH 加成具有弱热力学竞争力10分；PI2 成环端点比简单加成物明显更稳定15分；PI2 可达成环选择 γ 衍生的呋喃连接方式20分；PI3 偏向 α 连接的质子化加成产物15分；三个底物的选择性可靠度不同10分。合计100分，全部semantic/conclusion，逐项pass/fail；无数值匹配门槛或need_review。

旧→新：7项→7项。原数值规则：无；原数值仅留历史证据。

科学范围未变：task.md、全部agent_input/data、guide和submission_schema均保持原字节。原要求的能量、位点、产物、比较与解释仍完整保留；量化结果作为结论证据，取消作者目标值和容差评分。构象、描述符、作者节点、计算次数及完成流程没有独立奖励。已存在不同终答框架保留，未为统一条数人为拆分。

## 科学要求—规则—独立性—来源—已有验证

|公开科学要求|规则|独立性|正文/SI|已存验证支持与缺口|
|---|---|---|---|---|
|必需结果1：PI1单加成位点及中性产物偏好|r_r5_site_answer|同一方法内PI1产品/位点比较不等于跨模型稳健性。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|PI1 G1/G7小能差且优先位点改序，不稳健强制唯一赢家。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|
|必需结果2：PI1简单加成与环化可达性|r_r5_product_class|PI1环化受阻不同于其简单加成的位点微排序。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|PI1 α局部G7‡35.401941；γ种子释放开环1.469834→2.762128 Å仅局部证据。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|
|必需结果3：PI1第二MeSH加成增量及竞争性|r_r5_second_competition|第二次加成使用另一配平库存，和第一次位点偏好可独立成立。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|mono+MeSH→double增量−2.141554 kcal/mol，来源约−2；弱效应需限定。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|
|必需结果4：PI2简单/环产物及两环连接稳定性|r_r6_thermodynamic_fate|PI2终态类别稳定性不同于形成路径可达性。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|PI2环−17.048283/−17.230832，对简单−3.969174/−2.184290/−3.461029。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|
|必需结果5：PI2可达成环连接及PI1对比|r_r6_accessible_fate|PI2竞争路线能到达何种环连接不由最终环能量相近决定。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|PI2 α局部G7‡27.297280；γ有限电子能路径最高9.564782，对同方法α29.132496。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|
|必需结果6：PI3质子化产物位点偏好|r_sulf_site_answer|PI3为不同分子，位点偏好可独立于PI1/PI2成立。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|PI3中性α/竞争−10.657089/−9.504704/−5.245893 kcal/mol。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|
|必需结果7：各类预测的定量敏感性与稳健性|r_comparative_robustness|跨模型结论敏感性是对预测可靠性的额外科学回答，不再次奖励某一单模型赢家。|正文PDF8–11 Schemes12–15；SI PDF30–34 Eq.S1/TableS4/Fig.S8，39/47/51坐标|实算G1/G7保留PI3和PI2类别，改变PI1简单端点排序；近环端点不能称同等稳健。 主要边界：PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。|

## 文件与理由

scoring_rules更新逐项判据/二态政策；reference_conclusions与supporting key points同步；原key points完整置于明确非评分历史记录；evidence_map及覆盖/资格文档更新现行映射，保留来源证据及历史接受分类；paper_route区分现行评分和历史路线；package_manifest重建。验证参考文件逐字不改。同步审查页完整中文规则与原始JSON，以及审查任务副本。

## 保留专家事项

- PI3 α中性SP存在MAX/RMS density 0.22963/0.0072282、orbital gradient0.00042272残差；不因软件收敛标签忽略。
- 中性PI2母体small-step最大梯度0.0005810986超过原打印0.0003000000；此诊断是证据有效性而非作者匹配门槛。
- PI1位点小能差、PI2初始阴离子正文/图排序冲突、有限γ电子扫描及MeSH/EtSH模型差异均保留。

没有新QM/HPC或盲测，合同和运行时通过不等于科学满分；已知参考缺陷另记objective_issue_flags，不恢复人工待定得分。

## 2026-10-27及以前历史修改说明（评分政策已由上文替代）

下列记录保留原数值、方法、偏差及旧设计历史；旧窗口和need_review不是当前评分要求。

# paper_fb75113b35e12c7c 修改说明

## 科学问题与范围
原题已明确三个 dendralene 的位点、质子化产物、两种环烯酮成环、PI1二次加成和稳健性；问题本身保留。本轮将冗长的过程要求改成七项可单独回答的最终问题，是“预测＋计算解释”混合题。没有加入PI2/PI3二次加成、PI3成环、EtSH实验产率或全网络复现。

## 文件级修改及原因
|文件/位置|修改前|修改后及理由|
|---|---|---|
|agent_input/task.md|含作者指导条件段、研究质量分及过程性叙述|五段英文任务，七项最终输出；删除对不可用作者材料的依赖和旧过程分承诺|
|agent_input/submission_guide.md|研究质量/问题解决两类得分、双模式措辞|只对支持充分的最终结果计分；schema及其文件/ID合同保持|
|evaluation/scoring_rules.json、reference_conclusions.json|13项V2，其中10个中间节点|7个V3独立最终命题，共100分；不以完成作者节点清单给分|
|reference_key_points.json|旧中间结果可单独计分|保留有效来源证据，逐条scored=false；方法/结构仍可支撑最终答案|
|reference_qualification.json、task_definition.json、critical_failures.json|旧V2与历史验收状态|同步V3、逐结果证据覆盖和英文有效性规则；历史状态单独保留，不继承PASS|
|paper_route.md、verified_computation_reference.md|活动60/40及历史记录混杂|更新活动评分说明；验证参考仅顶部加入本版说明，历史日志不删改|
|package_manifest.json|旧哈希|重建内容哈希并实际加载校验|
|system.json、submission_schema.json|身份明确、格式合理|保留；不为外观重造结构或合同|

## 公开信息、身份与泄漏
公开PI1/PI2为SI S4的2Z,4E双甲酯；PI3为S6的双苯基乙烯砜，保留规定appendage E关系。直接读SI S39/S47/S51坐标段及S31–S32映射，未换分子图或删必要异构信息。PI4 MeS−/MeSH、298.15 K及1 M参照保留。公开没有胜出位点、作者中间体/TS、数值或论文依赖；来源与数字只在评价侧。本轮未添加新结构。

## 最终规则及原过程项处置
|rule_id|最终命题|分|状态|
|---|---|---:|---|
|r_r5_site_answer|PI1 monoaddition has weak, model-dependent site selectivity|15|三态：实际有效计算仍存在实质位点/机理冲突时复核|
|r_r5_product_class|PI1 favors accessible simple addition over the considered cyclized outcomes|15|三态：实际有效计算仍存在实质位点/机理冲突时复核|
|r_r5_second_competition|A second MeSH addition to PI1 is weakly thermodynamically competitive|10|二态|
|r_r6_thermodynamic_fate|PI2 cyclized endpoints are substantially more stable than simple adducts|15|二态|
|r_r6_accessible_fate|PI2 accessible cyclization selects the gamma-derived furan connectivity|20|三态：实际有效计算仍存在实质位点/机理冲突时复核|
|r_sulf_site_answer|PI3 favors alpha-connected protonated addition products|15|三态：实际有效计算仍存在实质位点/机理冲突时复核|
|r_comparative_robustness|Selectivity reliability differs across the three substrates|10|二态|

三态具体触发条件已写入每条review_triggers；缺计算、错身份、参照不一致、低质量数值本身不走review。R5两种成环节点不再各自计分，而作为“为何简单加成可达”的参考证据；R6α/γ路径不按两段完成计分，而证明可达产物连接。阴离子排序只支持中性产物解释，不另收分。所有旧来源数字原本均无硬窗，本次没有新增/放宽窗口。R6“环端点稳定”与“哪一连接可达”是两个不同最终问题，不重复计同一事实。

## 题面—来源—规则—本地证据
本轮直接阅读正文PDF 7–11页（尤其Scheme 12–15）、SI S4/S6/S30–S34及母体坐标页，查看Figure S8原图；非仅依据旧总结。

所有下表数值为实际本地原生量（单位kcal/mol，除另注），来源值另列。证据文件 `docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json` 的 comparisons / robustness_actual_two_method_comparison 逐项关联实际Opt/Freq和SP日志；抽读R5_SMe1的optfreq.log和method7.log确认实际能量与正常终止，另核gamma更正收据。

|题面输出|正文/SI|规则|已有原生量/文件|覆盖或缺口|
|---|---|---|---|---|
|PI1 monoaddition has weak, model-dependent site selectivity|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_r5_site_answer|PI1 G1/G7 monoaddition rankings in robustness_actual_two_method_comparison; no unique rank is forced.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|
|PI1 favors accessible simple addition over the considered cyclized outcomes|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_r5_product_class|R5 alpha local G7 35.401941 vs source 35.6; reconstructed gamma seed opens 1.469834 to 2.762128 Å.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|
|A second MeSH addition to PI1 is weakly thermodynamically competitive|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_r5_second_competition|Second-addition deltaG=-2.141554 vs source approx -2.0 kcal/mol.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|
|PI2 cyclized endpoints are substantially more stable than simple adducts|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_r6_thermodynamic_fate|R6 cyclic -17.048283/-17.230832 versus simple -3.969174/-2.184290/-3.461029 kcal/mol.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|
|PI2 accessible cyclization selects the gamma-derived furan connectivity|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_r6_accessible_fate|R6 alpha local G7 27.297280 vs 27.6; gamma finite electronic path maximum 9.564782 vs matched alpha electronic barrier 29.132496.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|
|PI3 favors alpha-connected protonated addition products|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_sulf_site_answer|PI3 neutral alpha/SMe6/SMe1 G7=-10.657089/-9.504704/-5.245893 kcal/mol.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|
|Selectivity reliability differs across the three substrates|Main pp. 8–11, Schemes 12–15; SI S30–S34, Eq. S1/Table S4/Fig. S8|r_comparative_robustness|Native G1/G7 comparison preserves PI3 preference and PI2 cyclic class, changes PI1 simple-product winner.；author_comparison.json相应字段及其native_evidence|有限模型下覆盖；不声称全局网络/实验分布|

## 方法差异与未决事项
原生使用ORCA 6.1.1，来源6.0.1；B3LYP-D3BJ/def2-TZVP CPCM氯仿Opt/Freq及ωB97M-V/def2-TZVPD SMD单点，G7=SP7+(G1−E1)。源和实算均区分MeS−阴离子形成与MeSH中性形成。精确1 M常数比RTln24.46使双分子缔合差−0.000130877 kcal/mol，不改变排序。R5/R6α局部G势垒与来源差−0.198059/−0.302720；R6γ9.564782是有限12点约束电子路径，绝非精确G势垒或全局无势垒。R5γ由中性结构删H38重构后开环，只证明局部不稳。

R6初始阴离子正文δ最低而图/SI为β′最低，故不强判唯一初始排序。Sulf中性α产物SP虽原生收敛，其MAX/RMS density 0.22963/0.0072282及orbital gradient 0.00042272等需专家判断；中性R6_0_1的small-step替代收敛MAXgradient=0.0005810986超过0.0003000000，不能误写成环阴离子未收敛。R5简单产品G1/G7改序、二加成略有利与EtSH实验不完全一致均保留。

## 验证复用与自检
本轮没有提交新QM/HPC或ARCHE盲测。上述同身份同物理量可复用；原生结果覆盖有界问题，但严格数值质量、全构象/全路径并未被本轮认证。额外计算并非本轮动作；专家若认为SCF残差影响排序，应针对受影响结果评估，而非自动满分。JSON解析、manifest、validate_task_package、validate_rubric及逐题TaskRepository.from_v3实际通过。仍需父级审核：七条最终输出的拆分是否避免重复；Sulf残差对小能差可信度的影响。结构合同通过不等于科学验收通过。

## 组末复审与实际文件补充

|文件|本次收尾修改|理由|
|---|---|---|
|evaluation/reference_qualification.json|当前verification_status明确V3_NOT_REASSESSED；旧验收状态保留historical_reference_status|杜绝从旧PASS/NUMERIC_REVIEW自动继承本版科学验收|
|evaluation/research_contract.json / reproduction_protocol.json|明确私有历史来源记录角色、当前唯一V3评分入口；合同评分字段同步V3|来源方案/旧合同决定不能隐含增加过程或作者节点要求|
|evaluation/evidence_map.json / scoring_rules.json / reference_conclusions.json|补V3_EXISTING_NATIVE_EVIDENCE及七项引用|每个最终命题同时可定位来源和已有原生证据|
|package_manifest.json|根据最终内容再次重建|保证组末修订后的哈希和包内容一致|

收尾重复执行JSON解析、rubric/package校验和隔离V3加载，均通过；未启动量子化学、HPC或盲测。

逐文件与只读`v1_backup/paper_fb75113b35e12c7c`比较，实际变化清单：`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/critical_failures.json`、`evaluation/evidence_map.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/reproduction_protocol.json`、`evaluation/research_contract.json`、`evaluation/scoring_rules.json`、`evaluation/task_definition.json`、`evaluation/verified_computation_reference.md`、`package_manifest.json`、`paper_route.md`。以上文件均已在文件变化表及本节说明原因。保持原样：`agent_input/data/inputs/system.json`、`agent_input/submission_schema.json`、`task_info.json`。历史`verified_computation_reference.md`原文逐字仍为本版文件后缀；实际运行的是临时`v3_autonomous_research`布局下的`TaskRepository.from_v3`。

## 2026-10-27 复核后确认的最小修复

本轮先逐字复核旧公开task、当前task、公开system/guide/schema及当前评价，再直接重读正文PDF9–11与SI30–31（计算方法和1M热化学定义）。确认正文9–10的PI2低能环产物及不同成环可达性是计算结论，正文11同时强调PI1选择性不稳健；公开输入没有MeSH产物分布。因此当前题面“PI2's accessible cyclic-product connectivity”确实预设了本应预测的产物类别，需修。范围仍为三个既定分子、PI1/PI2简单/成环、PI1二次加成及稳健性。

|实际改文件|本轮旧→新|理由及影响|
|---|---|---|
|`agent_input/task.md`第5项|“Identify and explain PI2's accessible cyclic-product connectivity”→“Determine which PI2 simple-addition or cyclic-product connectivities are supported as accessible”|开放比较两类结果，不预告PI2会形成可达环产物；原热力学与可达性问题均保留|
|`agent_input/task.md`第7项|“using informative sensitivity calculations”→量化敏感性证据来自有信息量的比较，可使用自己已生成结果，不指定追加方法/重算|保留实证稳健性要求，消除为满足条款而另开新方法/作业的误读；泛泛不确定性仍不算回答|
|`evaluation/scoring_rules.json`、`reference_conclusions.json`|稳健性expected补充允许对已有真实结果做量化敏感性分析，不要求固定跨方法矩阵或额外重算|公开/私有同义；不改7项终答、权重、PI2参考答案或源数值|
|`paper_route.md`|追加本轮边界说明|区分开放预测题与私有参考计算结论，旧来源记录保留|
|`package_manifest.json`|重建entries/content hash|反映本轮实际载荷|

本轮实际复核的验证结果位置：`docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json`，其中`robustness_actual_two_method_comparison`保存G1/G7实际比较；`gamma_results`保存PI2有限gamma电子路径9.564781807与同方法alpha电子势垒29.132496089 kcal/mol。此证据支持有限模型下的结论，不能作为把答案预置到公开题面的理由；也不意味着每个参试者必须照抄G1/G7方法组合。PI1改序、PI3部分SCF密度/轨道残差、PI2有限扫描不能成为精确G势垒等原限制继续保留。

全量公开文件检查后，仅task存在本轮相关问题；system分子/条件、guide和schema未改。`reference_key_points.json`及`verified_computation_reference.md`对本轮before快照逐字节一致，未篡改旧数值和计算过程。实际完成JSON解析、V3 rubric、package及隔离TaskRepository/runtime验证：`paper_science_v3` / `final_results_100`，7项共100分、0过程项。没有新增QM/HPC、没有重验科学PASS；验证记录在`/tmp/rcb_upgrade19_20261027/confirmed_repairs/01/validation.json`。

</details>

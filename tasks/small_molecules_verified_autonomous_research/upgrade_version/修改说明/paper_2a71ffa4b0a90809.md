# 第二轮专家反馈调整 — 2026-11-03

删除“识别并定量检验相关结合或离子对相互作用”的题面提示，保留初始活化与定量分子比较要求。

正文Scheme 3支持氯离子结合的参考解释，但公开题面不必预先指定调查结合或离子对相互作用。私有评分仍接受有真实计算支持的参考或等效解释；四项权重30/25/25/20不变。

[修改前后记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/第二轮专家反馈调整记录_20261103.md)

---

# 第一轮专家反馈调整 — 2026-11-03

聚焦催化剂如何促进初始活化及相关结合/离子对相互作用；C/E时间交叉仅作为静态解释的边界。

Scheme 3把氯离子结合纳入关键活化解释。采用初始活化设问，使任务与所评分的结合/结构证据匹配，同时不在公开题面写死唯一机理。C/E时间交叉保留为解释范围，不能仅由静态结合能精确预测小时级曲线。

当前评分：A/B活性差别的分子起源 30分；C/D活性差别的分子解释 25分；C/E行为的分子解释及证据的解释范围 25分；相对于无催化剂反应的催化剂依赖增强 20分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_2a71ffa4b0a90809 最终结论分项评分统一（2026-10-29）

逐条核对现有独立最终命题，保留其科学范围与权重，删除人工待定分及旧数值门槛政策。

A/B活性差别的分子起源 30分；C/D活性差别的分子解释 25分；C/E行为的分子解释及证据的解释范围 25分；相对于无催化剂反应的催化剂依赖增强 20分。

旧→新规则数：4→4；仅保留独立终答，全部semantic/pass-fail，100分。科学范围不变；公开题面/输入/提交结构字节不变。

See evidence_map.json and original source PDFs.

逐项问题、独立性、来源与验证映射见[协调进度](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/最终结论分项评分统一_20261029/进度/organic19_a_paper_2a71ffa4b0a90809.json)及[完整审查报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_2a71ffa4b0a90809.md)。

修改文件及原因：

- `paper_route.md`：同步最终结论二态合同、引用或非评分历史证据边界。
- `package_manifest.json`：重建实际内容哈希。
- `evaluation/scoring_rules.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/final_result_coverage.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/conclusion_coverage_20261029.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_key_points.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/critical_failures.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/evidence_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_qualification.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/target_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。

未运行新量化计算。验证参考SHA256保持`ccfbd2c02ec9f30bfc57b5499252bb3d65da0aaf3fe87d1fb2e6b005a6b571f8`，原始接受分类、数值差异和方法限制未升级。rubric/package/runtime加载及源/副本逐文件哈希校验通过。

当前专家事项：

|事项类别／已知事实|影响|专家需判断|建议处理|
|---|---|---|---|
|证据范围：C初始布居未知，C/E时间交叉没有独立动力学模型。|C/D与C/E解释的因果强度。|现有结合、连接及方向性电子证据是否足以支持提交者的具体有界归因。|按实际主张判断；允许静态比较无法解释时间交叉的有据结论，不要求新增时序计算。|
|数值／有效性：C/D势垒残差−0.2871/−0.6105，D端点差0.2334而源<0.1；有限模连接和ESP网格。|可达性和电子证据的精度，非硬数值门槛。|这些有限证据的解释范围与所声称控制机制是否匹配。|保留偏差和有限连接／网格定义，不认证完整IRC或连续极值。|
|历史失配：A约束扫描29.99558036965低于旧31±1下界。|历史来源对照，不是活动规则。|历史证据是否被错误借用为当前通过理由。|原值原窗继续保留，不舍入、不恢复隐藏门槛。|
|已修设计问题：公开机制维度和时间要求歧义已澄清。|四终答的公平解释与拆分。|评价时是否遵守等价解释直接pass、缺证fail的边界。|使用当前规则，不把旧节点清单或时间交叉必解要求带回。|

跨任务汇总见 [需专家重点审查的问题](<../需专家重点审查的问题.md>)。以上事项分别涉及证据充分性、数值或来源差异与推断范围；不因存在局部边界就要求补齐完整机理，也不由本页给出新的整题通过／失败结论。

---

## 2026-10-29之前的修改历史（非当前评分判据）

# paper_2a71ffa4b0a90809 改编说明

原题与新版都问五种催化剂及无催化剂背景的结构–活性解释，属于解释题。保留实验时间–产率数据，不奖励复述其排序；不扩为Mannich全循环、C–C过渡态、精确产率或新催化剂预测。当前版把必须回答的A/B、C/D、C/E及背景对照写清，仍由agent选择物理解释、模型和方法；下文来源构象/电子解释是参考证据，最新修复见末节。

|文件|修改前|修改后及理由|
|---|---|---|
|agent_input/task.md|“principal differences”较泛，未区分具体对照|五段英文；明确四个相互区分的比较问题及统一物理参照，未公开胜出分子机制或数值|
|evaluation/scoring_rules.json / reference_conclusions.json|18项局部节点、7个逐构象数值和综合解释并存|4个独立最终解释，100分；局部计算是证据，不按作者节点清单计分|
|reference_key_points.json|局部拓扑、预组织、转动及亲和能独立给分|原expected和数值原样保留，统一scored=false；没有删除有效证据|
|evidence_map.json|原文/SI定位|定位仍适用，保留；final_result_coverage.json补新规则到本地证据的映射|
|qualification / current status / target_map / validation plans / paper_route|混合历史V2、旧pending和过程分计划|同步当前V3，原文件留在受保护v1_backup，未另建重复备份；不继承旧PASS|
|submission guide/schema / manifest|通用结果合同|仅说明终答与证据绑定，不新增提交字段；重建hash|
|verified_computation_reference.md|完整历史日志|只加本版范围说明，原文不动；另存本次15日志重读结果|

输入system.json/observations.json/README原内容无科学问题，全部保留。以正文p3 Fig2、SI p27结构及pp128–129坐标核对：A/B同C18F12I2但相对轴向身份相反；C为对苯撑、D为乙炔、E为直接联苯，均有两个I。RDKit解析/分子式核对见自检。中性产品C17H18Cl3NO4不混作[M+H]+。正文p4文字把D的86%写为8h，而p5 Fig5表为12h；继续采用原输入的图表时间值。公开已知仅实验产率与化学身份/条件，没有作者优化结构、机制/计算值。七个亲和能不是原题指定的独立终答，不能借V3把旧中间清单改名为最终结论。

|最终规则|命题|权重|状态与复核触发|
|---|---|---:|---|
|r_axial_activity_contrast|A/B相对轴向排列为何导致主要活性差异|30|三态；只有真实、收敛、同身份替代模型导致无法消除的因果归属冲突才复核|
|r_linker_accessibility_contrast|C/D活性对照的分子解释，构象可达性为参考解释|25|三态；同上；若声称动力学可达性，缺连接/仅端点能差不成立|
|r_framework_electronic_explanation|C/E行为的分子解释及证据对时间交叉的解释范围|25|三态；同上；若声称σ-hole，净电荷不能替代方向性证据；不强制新时间动力学|
|r_background_contrast|催化剂相对非零背景的增强差异|20|三态；有实际冲突的物理解释才复核，复述产率/缺计算fail|

所有条目required_for_success=true；已确认等价的模型直接pass，不强制作者序列。数字硬窗不允许复核绕过。本篇不再有独立硬窗，因为原题未要求七个构象逐值作为最终答案；这是评分对象修正，非避免失配。旧A/B/Csyn/Canti/Dsyn/Danti/E目标分别−8.2/−2.6/−5.9/−1.5/−7.1/−2.5/−3.3，各±1.0 kcal/mol，一一完整留在非评分key points，均可由现有本地值落入旧窗。旧五个结合拓扑、预组织、C/D转动和ESP条目也转成对应解释的支持证据。A约束扫描31±1早已不属于本版原题核心，不恢复计分。

|题面最终要求|正文/SI依据|新规则|已有本地量/原生文件|覆盖与缺口|
|---|---|---|---|---|
|A/B活性差异|正文p3–5；SI63、66|r_axial_activity_contrast|A/B结合G −8.209078940/−2.558356126；group_4/.../outputs/1a_syn_chloride及1a_anti_chloride/gaussian.log；minimum_parent_evidence_table.json列全部组成|两个实际复合物支持双点/单点；15份输出hash、热化学重读一致|
|C/D可达性|正文p7 Fig6；SI60、66|r_linker_accessibility_contrast|C_paired_connection.json → C_rotation_redundant_recovery/stationary.log及mode±/minimum.log；halogen_new_results.json中的D连接；17.612935918/1.589481498 kcal/mol|有限解析虚模双端松弛，非长IRC；C初始群体不知，不能推出精确速率|
|电子与C/E交叉|正文p7 Fig7、p8–9/12；SI61–62|r_framework_electronic_explanation|halogen_new_results.json → 5个*_ESP_surface/surface_result.json及波函数/cube；A/B/C/D/E 129.309510/116.007992/109.738371/126.603178/118.753132 kJ/mol|有限网格支持方向/排序，未认证连续面极值；时间交叉为公开观察不是新算结果|
|背景增强|正文p4–5 Fig5、p8–9/12|r_background_contrast|同7组原生结合G与完整复合物、五供体ESP；对照同时间observations|支持有界结构–活性归因；无未催化基元势垒/全反应动力学，题目未要求，不能声称已验证全循环|

完整本地账本：`docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/minimum_parent_evidence_table.json`。本轮直接读取正文和SI相关页，并从15份Gaussian原日志重提G、负频与正常终止并核hash，另阅读C/D连接和ESP原生分析索引。并非只引用旧验收。

本地与来源方法均为M06-2X-D3/6-311+G(d,p)/SDD(I)、SMD18(THF)、193.15K；使用I半径2.74Å。源表压力未明示，但Cl热项支持1atm；结合1M转换另减1.0605682035。七项本地G依次为−8.209078940、−2.558356126、−5.911139246、−1.455194470、−7.131017663、−2.494350159、−3.284384587 kcal/mol，对源图最大差0.044805530。C/D势垒对17.9/2.2差−0.287064082/−0.610518502；D端点差0.233433524不等于来源<0.1，不能换旧端点来追值。ESP比来源128/114/108/125/117高1.31–2.01 kJ/mol；保留有限网格定义。A旧扫描29.99558036965仍超31±1下界，不舍入宣布通过。

本轮没有新QM/HPC、没有盲测。相同身份/物理量可复用，但精确C群体、连续ESP极值、宏观速率/产率和完整循环不在现有证据中。需要父级确认四个最终对照的拆分和非评分七值处理；科学未解事项不包装为通过。JSON、V3总分/一规则一结论、包manifest、英文公开输入及分子式已实际检查；合同通过仅表示设计可加载。

终检补充：公开文件已清除author/paper/article/SI依赖措辞；active expected不要求参试者报告未公开金标偏差或源文冲突。源私有数值与历史差异仅供评测者比较。6包批量RDKit核对共54个SMILES（6d19为文字构造模型，没有SMILES），54/54可解析；显式原子/键表一致。CIP先移除原子映射号的人工优先级；4e为6R/11S/13R/30S、c625为9R及E。没有更改原输入分子。旧附属qualification/plan/status内的已验证标签已明确降为历史上下文，本版以final_result_coverage逐项判定。


## 2026-10-27 交叉审查确认后的修复

本轮修正的是提示过强和时间要求歧义：先前题面把C/D构象可达性、骨架电子效应直接列成解题维度，并可能使“changing time-dependent ordering”被理解为强制求C/E交叉动力学。现在保留A/B、C/D、C/E及无催化背景四个具体比较，由参与者选择物理解释与定量检验；C/E必须评估分子证据解释到哪一步，但其交叉成因可有据地未决，不要求另建时间动力学模型。只写局限或复述产率仍不构成答案。

|实际修改文件|具体修改与理由|
|---|---|
|agent_input/task.md|四个比较改为并列清单，去预定构象/电子原因；明确交叉的证据能力判断与未决范围|
|agent_input/submission_guide.md|同步四个比较和交叉判断，既有接口不变|
|evaluation/scoring_rules.json、reference_conclusions.json|C/D与C/E规则/描述同步；构象和σ-hole保留为参考解释，有证据的物理等价说明可通过；只有实际声称可达性或σ-hole时才要求相应连接或方向性证据|
|evaluation/reference_key_points.json|添加非评分来源证据适用范围，防止其旧“必须”语气重新变成隐藏方法清单；原条目及数值未改|
|evaluation/reference_qualification.json、final_result_coverage.json、paper_route.md|明确方法选择自由与C/E时间边界，既有有限参考计算不升级为交叉动力学验证|
|package_manifest.json|按实际载荷重建hash|

依据：正文PDF7 Fig6–8、SI60–66支持参考构象/结合/电子解释，正文8–9/12说明单描述符不能解释整套活性。既有原生索引`docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/minimum_parent_evidence_table.json`的C/D连接、电子/结合比较及physical_unknowns支持有限说明；未知C群体、未验证时间动力学不能靠题干措辞升级为已证。

沿用四个rule_id保证溯源；其中linker_accessibility/framework_electronic的历史命名不再意味着唯一路线，活动description/expected明确按C/D、C/E最终比较判断。A/B与背景规则不变，30/25/25/20、复核触发、成功要求不变。本轮不调整先前已转为非评分背景的七个结合G窗，也不宣称这些窗仍是活动硬门槛；现有分子输入、来源数值、原生记录均未改。JSON、V3、package及独立运行时加载通过；无新QM/HPC、无盲测、无自动科学PASS。

本轮快照：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/before`。相对该快照的实际包文件差异（9个）：`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/final_result_coverage.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/scoring_rules.json`、`package_manifest.json`、`paper_route.md`。验证记录：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/03/validation_results.json`。本说明文件的追加不属于agent公开输入。

</details>

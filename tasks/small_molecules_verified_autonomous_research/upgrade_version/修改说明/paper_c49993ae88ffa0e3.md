# 第一轮专家反馈调整 — 2026-11-03

明确两分子额外水用于净热力学及离子态差异稳定化；不要求水介导质子接力或水催化路径；保留生成水额外计数。

正文Fig. 2及SI S40–S41研究水合对离子态的差异稳定化，没有证明两水催化路径。两分子额外水分配给两个参照片段，脱氧生成水另计；局部ET更有利可与净反应略不那么放热并存，不能由此直接推算加速或最优体相水含量。

当前评分：无加水净脱氧的热力学驱动力 20分；双加水净脱氧的热力学驱动力 20分；预成H2PQ光驱动还原的分子基础 30分；有限水合为何改变反应热力学及其解释能力 30分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_c49993ae88ffa0e3：2026-10-29 最终结论分项统一

现行分项：无加水净脱氧的热力学驱动力20分；双加水净脱氧的热力学驱动力20分；预成H2PQ光驱动还原的分子基础30分；有限水合为何改变反应热力学及其解释能力30分。合计100分，全部semantic/conclusion，逐项pass/fail；无数值匹配门槛或need_review。

旧→新：4项→4项。原数值规则：r_cumulative_f_dry、r_cumulative_f_water；原数值仅留历史证据。

科学范围未变：task.md、全部agent_input/data、guide和submission_schema均保持原字节。原要求的能量、位点、产物、比较与解释仍完整保留；量化结果作为结论证据，取消作者目标值和容差评分。构象、描述符、作者节点、计算次数及完成流程没有独立奖励。已存在不同终答框架保留，未为统一条数人为拆分。

## 科学要求—规则—独立性—来源—已有验证

|公开科学要求|规则|独立性|正文/SI|已存验证支持与缺口|
|---|---|---|---|---|
|必需结果1中的无加水规范净G及其驱动力|r_cumulative_f_dry|无加水净热力学命题可独立于双水计算成功。|正文PDF4 Fig.2；SI PDF38–41方法、GoodVibes表和电子态说明|规范干净G−115.102153417，来源−115.1；S1反应物与Py/生成水缔合物参照配平。 主要边界：原始GoodVibes YAML及作者频率输出未取得，重建全标签协议不冒充作者原件。|
|必需结果1中的双加水规范净G及其驱动力|r_cumulative_f_water|双水净热力学命题可独立于无水计算成功，不对两情景差值重复加分。|正文PDF4 Fig.2；SI PDF38–41方法、GoodVibes表和电子态说明|双水净G−112.238810567，来源−112.1；两侧各两个附加水，生成水另计。 主要边界：原始GoodVibes YAML及作者频率输出未取得，重建全标签协议不冒充作者原件。|
|必需结果2：光还原剂角色与配平电子/质子变化|r_reductant_molecular_role|解释光激发还原剂提供氢/电子当量，不以净G负号取代分子作用机制。|正文PDF4 Fig.2；SI PDF38–41方法、GoodVibes表和电子态说明|既有132原生日志及热项组装支持PT/ET状态与两个氢当量转移；不确立唯一先后。 主要边界：原始GoodVibes YAML及作者频率输出未取得，重建全标签协议不冒充作者原件。|
|必需结果3：干/水合定量对比、局部水合作用及实验解释范围|r_local_hydration_effect|判断离子型局部转移的差异水合稳定，与两种净终态驱动是不同命题。|正文PDF4 Fig.2；SI PDF38–41方法、GoodVibes表和电子态说明|首次ET干/水合−1.433879/−8.220575，第二次+7.328581/−9.583636；局部端点不是动力学势垒。 主要边界：原始GoodVibes YAML及作者频率输出未取得，重建全标签协议不冒充作者原件。|

## 文件与理由

scoring_rules更新逐项判据/二态政策；reference_conclusions与supporting key points同步；原key points完整置于明确非评分历史记录；evidence_map及覆盖/资格文档更新现行映射，保留来源证据及历史接受分类；paper_route区分现行评分和历史路线；package_manifest重建。验证参考文件逐字不改。同步审查页完整中文规则与原始JSON，以及审查任务副本。

## 保留专家事项

- 原始GoodVibes YAML及作者频率输出未取得，重建全标签协议不冒充作者原件。
- 双水末端conf3热项残差−0.321883 kcal/mol保留；不为贴值选去重/其他后处理。
- 两水母体模型不能证明取代实验体系的最佳水比例、唯一动力学顺序、速率或完整再生。

没有新QM/HPC或盲测，合同和运行时通过不等于科学满分；已知参考缺陷另记objective_issue_flags，不恢复人工待定得分。

## 2026-10-27及以前历史修改说明（评分政策已由上文替代）

下列记录保留原数值、方法、偏差及旧设计历史；旧窗口和need_review不是当前评分要求。

# paper_c49993ae88ffa0e3 改编说明

原问题为预成H2PQ对母体PyO光脱氧直到产物的热力学解释，以及零/双水比较。新版仍为该解释题，保留净反应数值、分子作用与水合影响；不扩催化再生、真实衍生物全系列或速率预测，也不删终点定量要求。

|文件|改前|改后与原因|
|---|---|---|
|task.md|泛称“quantitative evidence through products”|明确两个净G、分子作用、水合比较；补共同初末态和水库存以避免隐藏参照；不写作者PT/ET序列|
|scoring_rules/reference_conclusions|12个逐节点数字+3局部定性+2综合结论|4个终答：干净G20、湿净G20、光驱动还原分子解释30、水合效应30；每项一规则|
|reference_key_points|逐节点独立计分|旧原文和全部窗原样保留为scored=false，不强制中间体链|
|qualification/status/target_map/已有plans、paper_route|V2与历史状态混杂|同步V3和逐命题复用，未继承旧PASS；原文件在受保护v1_backup|
|guide/schema/manifest|通用提交合同|保留字段，仅同步终答说明/hash|
|verified_computation_reference|历史全过程|仅顶部加V3范围与复用声明，原始日志不变|
|final_result_coverage|无新版映射|新增私有逐规则本地证据索引供复审|

公开system.json的4个母体图和实验文件中具名衍生物全部保留；实际检查SMILES、图原子/键与分子式。实验含预成试剂的衍生物反应、0–1%水产率，本来就是解释背景，不将已给产率再评分。删改旧文件中“cited paragraph”的外部来源措辞为中立的“supplied experimental conditions”。新版只明确净能量比较所需的S1-H2PQ+S0-PyO及PQ+Py/生成水关联体，未公开任何计算能量、胜出PT/ET路线或作者中间体序列。两个额外水在两片段各留一个来自SI40–41的量定义；否则无法公平执行原净G硬窗。未知活性过程由agent提出。

|规则|最终命题|分数|状态|
|---|---|---:|---|
|r_cumulative_f_dry|零加水最终净G，−115.1±2.0 kcal/mol|20|二态，超窗/错初末态fail|
|r_cumulative_f_water|双加水最终净G，−112.1±2.0 kcal/mol|20|二态，超窗/水库存错fail|
|r_reductant_molecular_role|H2PQ光酸/光还原剂提供质子电子当量的分子解释|30|三态；实际收敛且态/组成可比的替代机理引起未解决实质冲突才复核|
|r_local_hydration_effect|局部水合差异稳定离子态，解释适用范围|30|三态；同库存替代水合模型有真实冲突才复核|

所有必要项required_for_success=true；已成立等价PCET/HAT描述可直接pass，不以作者节点标签判分。缺计算/复述源数值fail。两个净G不与“净反应放热”另重复计分，分子解释评反应物怎样提供氢/电子及电子态转换，水合解释评相对稳定作用。

旧数字逐项处理（kcal/mol）：

|旧rule_id|原目标/窗|去向|
|---|---:|---|
|r_dry_first_pt|-0.9 ± 1.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_dry_first_et|-1.6 ± 1.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_hydrated_first_pt|-2.2 ± 1.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_hydrated_first_et|-8.2 ± 1.5|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_second_dry_pt|2.3 ± 1.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_second_dry_et|7.4 ± 1.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_second_water_pt|-1.3 ± 1.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_second_water_et|-9.6 ± 1.5|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_cumulative_i_dry|-43.9 ± 2.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_cumulative_i_water|-41.7 ± 2.0|scored=false；仅支持分子解释/水合解释，不要求复刻该节点|
|r_cumulative_f_dry|-115.1 ± 2.0|保留最终硬窗，20分|
|r_cumulative_f_water|-112.1 ± 2.0|保留最终硬窗，20分|

十个中间窗转非评分不是为躲误差：全部12量最大本地误差0.166121，小于各旧窗。转移依据是原题没有要求逐个作者中间态的数值清单；最终净G仍保留原批准窗且未改物理定义。

|题面输出|正文/SI|规则|本地量与原生文件|覆盖/缺口|
|---|---|---|---|---|
|零水净G|正文p4 Fig2A；SI40|r_cumulative_f_dry|−115.102153417；parent_pq_native_readback.json→66对中S1-H2PQ/PyO/S0-PQ/PyOH2的low/high日志；关联Py/生成水产品|差−0.002153417，支持原±2窗；不是基态反应物净G|
|双水净G|正文p4；SI40–41|r_cumulative_f_water|−112.238810567；同索引含S1-H2PQ-H2O/PyO-H2O/PQ-H2O/PyOH2-H2O构象|差−0.138810567；终点一构象qhG残差仍在，未择近去重结果|
|光驱动还原分子作用|正文p4竞争路线/PCET-HAT保留；SI38–41|r_reductant_molecular_role|首PT/ET −0.922739/−1.433879；干第二PT/ET +2.266745/+7.328581；两中性自由基累计−43.868608|支持平衡的两氢当量/光酸光还原解释；未确定唯一顺序/动力学|
|水合效应|正文p4末段；SI40–41|r_local_hydration_effect|首次双水PT/ET−2.197755/−8.220575；第二次−1.344649/−9.583636；累计I−41.738197|ET相对稳定强；有限两水不能证明0.1%最佳或预测衍生物速度|

原生总索引：`docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/parent_pq_native_readback.json`。本轮逐个读取132份低/高层日志并重核hash、SCF/TD能与频率块，132个hash均一致、均有正常终止且打印频率无负值；化学有效性仍结合原几何/态/热项账本，不以正常终止代替。正文p1/3/4和SI38–41已直接读；同时读输入和旧完整规则。没有把正文−0.9等值伪作实算。

方法为M06-2X/def2-TZVPP//6-31+G(d,p)、SMD(MeCN)、298.15K/1M，S1使用TD总能。GoodVibes3.0.2统一全标签、Grimme100cm−1、scale1、外部对称、Gconf，原命令无--dup；不是追值选协议。源0_PES.yaml与原频率文件未取得；本地重建不称原件。双水PyOH2-H2O conf3电子能贴近但qhG差−0.321883 kcal/mol；最终全标签−112.238811未采用更接近源的去重−112.117152。第二湿PT全标签−1.344649与去重−0.950069均保留，前者协议一致而非择近。干第二ET源绝对表7.329311与图差值7.4有四舍五入差，目标7.4未动。

本轮未提交QM/HPC、未盲测；相同初末态终点证据可复用。完整动力学、真实混合体系、最佳水百分比未覆盖且题内排除；原作者YAML与热项残差仍需专家追溯，不把静态合同通过说成科学问题全解。包/V3/JSON和原子分子式已检查；请父级复核新增公开参照是否足够清晰及四终答拆分。

终检补充：公开文件已清除author/paper/article/SI依赖措辞；active expected不要求参试者报告未公开金标偏差或源文冲突。源私有数值与历史差异仅供评测者比较。6包批量RDKit核对共54个SMILES（6d19为文字构造模型，没有SMILES），54/54可解析；显式原子/键表一致。CIP先移除原子映射号的人工优先级；4e为6R/11S/13R/30S、c625为9R及E。没有更改原输入分子。旧附属qualification/plan/status内的已验证标签已明确降为历史上下文，本版以final_result_coverage逐项判定。


## 2026-10-27 交叉审查确认后的修复

确认的问题是公开合同矛盾：修复前task同时允许选择电子态/缔合，又固定S1、产物缔合及每片段一水；system.water_model_note却仍说缔合未指定。本轮将固定约定明确限定为**两项必需净G的标准化报告参照**。对实际机理的态、缔合和转移假说仍由参与者提出并验证；标准参照不证明唯一活性态、真实溶液缔合或转移次序。替代模型可支持解释，但其结果不能替代两项指定参照的净G。

|实际修改文件|具体修改与理由|
|---|---|
|agent_input/task.md|区分自主机理探索与两项报告参照；零/两水定义分条，澄清水合H2PQ片段为最低激发单重态，其余参照片段为基态；不公开PT/ET顺序或计算值|
|agent_input/data/inputs/system.json|只改water_model_note：每片段一附加水仅适用于标准净G；水的位置/取向/构象仍未指定；分子图、组成、电荷和其他字段逐项不变|
|agent_input/submission_guide.md|用既有量值/参照字段区分标准结果与替代机理模型，不新增schema字段|
|evaluation/scoring_rules.json、reference_conclusions.json|两数值规则明确完整初末片段与适用范围；两解释规则不把报告参照当唯一机理；保持一规则一结论|
|evaluation/reference_key_points.json|仅同步两项最终净G对应的支持性expected，其他历史中间证据不变|
|evaluation/reference_qualification.json、final_result_coverage.json、paper_route.md|同步标准参照的适用边界，不升级原生证据状态|
|package_manifest.json|按实际载荷重建hash|

依据重核：正文PDF4 Fig2及SI38–41确实使用S1、逐片段水合和1M热化学；原生独立索引`docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/parent_pq_native_readback.json`中final_dry/final_two_water的products/references明示S0-PQ+PyOH2和各一水版本，净值−115.102153417/−112.238810567。此次复核使用来源及已有原生readback，不是新增计算，也不把参照定义推成唯一反应态证据。

四规则及20/20/30/30不变；两净G仍为−115.1/−112.1±2.0 kcal/mol，numeric/binary且不得need_review。原YAML缺失、末端构象热项残差、实际水活度/唯一动力学未证等边界继续保留。JSON、V3、package和独立临时TaskRepository运行时均通过，加载为paper_science_v3/final_results_100；这不是新科学PASS。

本轮快照：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/before`。相对该快照的实际包文件差异（10个）：`agent_input/data/inputs/system.json`、`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/final_result_coverage.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/scoring_rules.json`、`package_manifest.json`、`paper_route.md`。验证记录：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/03/validation_results.json`。本说明文件的追加不属于agent公开输入。

</details>

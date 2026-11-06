# 第一轮专家反馈调整 — 2026-11-03

专家认为无问题；保留完整配体、起始S=5/2和初始氧化范围；电子能/自由能与最终产物释放边界保持。

专家认为输入无问题，卡中已经给完整12-TMC及DMA、+1电荷、起始S=5/2和初始氧化范围。保留这些边界以及电子能与热自由能的区别；不把论文未完成的最终N-脱甲基释放加入题目。

当前评分：通过有根据的竞争分析确定能量受支持的初始氧化机制 40分；氧化剂引发 DMA 氧化能力的分子和电子解释 25分；初始氧化产生羟基化 DMA 部分而未确立最终 N-脱甲基 35分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_7cfd59d5c7061c6b 最终结论分项评分统一（2026-10-29）

逐条核对现有独立最终命题，保留其科学范围与权重，删除人工待定分及旧数值门槛政策。

通过有根据的竞争分析确定能量受支持的初始氧化机制 40分；氧化剂引发 DMA 氧化能力的分子和电子解释 25分；初始氧化产生羟基化 DMA 部分而未确立最终 N-脱甲基 35分。

旧→新规则数：3→3；仅保留独立终答，全部semantic/pass-fail，100分。科学范围不变；公开题面/输入/提交结构字节不变。

来源定位：正文 PDF 第 7–9 页、Figures 7/8 与实验条件；SI S33、S35、S37–S38（电子能与热项分列）、S44/S49 结构及 S56 起的完整坐标。

逐项问题、独立性、来源与验证映射见[协调进度](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/最终结论分项评分统一_20261029/进度/organic19_a_paper_7cfd59d5c7061c6b.json)及[完整审查报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_7cfd59d5c7061c6b.md)。

修改文件及原因：

- `paper_route.md`：同步最终结论二态合同、引用或非评分历史证据边界。
- `package_manifest.json`：重建实际内容哈希。
- `evaluation/scoring_rules.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/conclusion_coverage_20261029.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_key_points.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/critical_failures.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/evidence_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_conclusions.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_qualification.json`：同步最终结论二态合同、引用或非评分历史证据边界。

未运行新量化计算。验证参考SHA256保持`c8900ca67faf60ae6bdc4ba9b2d5f6e711d2cdc4507d84d8d43760bd7c2d0f17`，原始接受分类、数值差异和方法限制未升级。rubric/package/runtime加载及源/副本逐文件哈希校验通过。

当前专家事项：

1. **HAT 与反弹构象的连接范围。** 已连接 HAT 的 IM2 为 −3.260376，来源构象另算为 −10.086223 kcal/mol；两者互变未算，新 IM3 为 −45.752726。影响 `r_initial_oxidation_outcome` 和机制解释的连续性。建议分清各自端点与相对参照，认可有支持的局部羟基化，不描述成已经证明的全局最低连续轨迹；这是证据连接问题，不能用放宽旧数值窗解决。
2. **电子态/溶剂自主模型与参考覆盖。** 实验只约束初始 S=5/2，来源电子能与 G 排序不同，原生只计算六重态/CPCM TFE 参照；影响前两项物理解释。建议审查提交者自己的态、溶剂及同量参照是否合理。解除模型锁定已完成，不等于所有其他状态已验证，也不要求为重现历史 baseline 强制追加状态/溶剂计算。
3. **有限扫描与最终脱甲基边界。** 反弹 +2.862579 是低层有限扫描，不是已认证 TS 或精确零势垒；C–O 形成、N–C 保留和自旋变化支持初始羟基化，但未算产物释放。影响第三项。建议按有限化学结局判断，不将完整 N-脱甲基追加为隐藏任务，也不从电子高度推精确 213 K 速率。

---

## 2026-10-29之前的修改历史（非当前评分判据）

# paper_7cfd59d5c7061c6b 修改说明

## 原问题与修改后的科学问题
原公开题只问完整12-TMC Fe-peroxo如何引发DMA初始氧化、哪种机制能量有利，并明确不等于最终脱甲基。改后保留这一解释/机制判别题，用三个独立最终答案展开：竞争机制、活性氧电子结构为何可氧化C–H、初始氧化产物的化学结局。分子/条件/范围不扩不缩。

## 文件级修改
|文件|修改前|修改后与原因|
|---|---|---|
|task.md|短题面未显式分清最终答案；没有要求两作者TS数值|五段英文，三项机制/物理解释/化学结局；未新增作者节点定量任务|
|submission_guide.md|过程质量和结果独立计分；source-comparable措辞|最终结果唯一计分，能量定义中立化；outputs/code合同保留|
|scoring_rules/reference_conclusions|6中间节点含2硬窗＋2最终项|3最终命题40/25/35；过程/中间节点独立分取消|
|reference_key_points|节点/13.1和9.2各±2计分|scored=false；两原窗以historical_numeric_context原样存储，不改数值或容差|
|evidence_map/qualification|旧V2和定性PASS|逐命题映射最新原生审计，取消本版自动继承验收|
|paper_route/verified_computation_reference|活动旧数值/路径缺项描述|活动规则V3、旧节点窗非评分；验证顶部说明并原文保留日志|
|manifest|旧哈希|重建和运行时校验|
|XYZ/inventory/schema|完整准确的独立起始分子与合同|原样保留；不借作者相对摆放或中间体|

## 两数值窗的判别（父级复审要求）
13.1和9.2分别是O–O TS与后续HAT TS对共同RC的作者途径节点；原task.md没有把它们列作独立最终量值交付。因此不把旧intermediate改名conclusion，也不为保住分而新增题面“必须报两个节点”。两项±2.0原窗完整保留非评分历史参考与本地比较，本版无active numeric规则。这不同于公开明确要求overall barriers的9f24。机制优劣仍需实际能量证据，取消节点计分不降低科学成立条件。

## 公开信息、来源与身份
直接读正文PDF7–9（Figure7/8、计算方法），SI S33、35、37–38的电子能/热项分列、S44/S49结构和S56起的完整坐标。公开原子数实数：iron_peroxo 47=C12H28FeN4O2，dma 20=C8H11N，合计67/+1。保留12-TMC，未换13/14-TMC或para-MeO-DMA。两XYZ仍独立无相对布置；起始六重态有实验支持，但SI S2的电子能双重态低1.16，而全G偏六重态，不能升格为电子态全球排序。不给作者活化顺序、TS、目标数值或胜出答案。

## 最终规则
|规则|最终命题|权重|状态及原因|
|---|---|---:|---|
|r_preferred_initial_mechanism|活化后氧化优于完整peroxo直接HAT|40|三态；有效竞争态/路线出现实质冲突才review|
|r_oxidizing_activity_explanation|Fe/O电子重组如何产生氧化能力|25|三态；有效自旋耦合/电子分析有未决物理冲突；等价标签直接pass|
|r_initial_oxidation_outcome|保N–C的初始羟基化结局和驱动|35|二态|

第一项比较路线，第二项解释反应性物理起因，第三项判定氧化后的底物性质；均不是完成O–O/HAT/IM2/rebound节点清单。缺计算、无支持推测和错态直接fail；不按Mulliken精确数分数，也不强迫全IRC。

## 逐项证据覆盖
最新原生入口：`docs/verification/small_molecules_autonomous_research/qualitative_acceptance_check_20261022T0725Z/7cfd_independent_review/review.json`，读取独立审查及25日志索引，抽读RC、TS1b、TS2b实际高层日志（−2473.91362832/−2473.89280026/−2473.89901079 Eh），确认真实SCF和正常结束。新反弹端点以自身高层值，不借旧构象。

|题面要求|正文/SI|新rule|本地原生量/文件字段|覆盖/缺口|
|---|---|---|---|---|
|哪种机制有利|正文7 Figure7；SI S35/S37|r_preferred_initial_mechanism|direct28.085485、activation13.069805、HAT高9.172639；review.json comparisons/IRC|局部竞争覆盖；不证明环境无关唯一限速|
|活性Fe/O解释|正文7–8 Figure8；SI S38|r_oxidizing_activity_explanation|O–O模与Fe/O自旋重分配、C–H/O–H反向距离导数；independent_native_audit|等价价态/耦合描述允许；非全局自旋搜索|
|初始氧化结局|正文7；SI S37/S38|r_initial_oxidation_outcome|新IM3 E−2473.98653993Eh，RC相对−45.752726；C–O1.402251Å/N–C1.453281Å，底物自旋0.003852；相对源IM2下降35.666503|羟基化局部连接覆盖；跨构象互变和最终释放未算|

非评分原窗：13.069805对13.1差−0.030195，9.172639对9.2差−0.027361，均在原±2内；这仅说明历史数值关系，不直接产生本版分。局部HAT为11.366876，不能误叫9.2。

## 方法差异、数值偏差及剩余验证
实际TPSSh/def2-SVP几何/频率、def2-TZVPP高层、CPCM纯TFE电子能，不加D3/ZPE/RRHO；G16 B.01→C.01，实验TFE/MeOH及213 K与电子能模型有别。旧HAT连通IM2=−3.260376，比源−10.1高6.839624；源构象独立量−10.086223不能替代旧构象或声称已算互变。新连接IM3=−45.752726对源−46.2差+0.447274；反弹扫描低层最高+2.862579不是认证TS、不是严格无势垒。直接HAT产物仅低层+23.269432，不当成源高层+22.5复现。

本轮无新QM/HPC/盲测。旧局部路径、恢复端点和反弹可复用；不同HAT/反弹起始构象不冒称单一全局最低连续路线。未解最终脱甲基是原题之外，不新增补算；所需定性结论需独立评判，不继承旧暂定PASS。全部JSON、manifest、V3和隔离加载通过。父级重点复核：取消两个节点窗的合理性已按原公开题执行，三个最终物理命题是否独立、不落回作者清单。

## 组末复审与实际文件补充

|文件|本次收尾修改|理由|
|---|---|---|
|evaluation/reference_qualification.json|当前verification_status明确V3_NOT_REASSESSED；旧验收状态保留historical_reference_status|杜绝从旧PASS/NUMERIC_REVIEW自动继承本版科学验收|
|evaluation/critical_failures.json|伪造与私有答案泄漏规则翻译为英文；普通错误仅影响相关结果|活动评分语言统一，未扩大invalid_submission触发|
|agent_input/task.md / submission_guide.md|XYZ补全data/inputs路径；删除author/article/SI措辞，改为独立选模型和方法|公开任务不依赖私有来源且实际文件可定位|
|package_manifest.json|根据最终内容再次重建|保证组末修订后的哈希和包内容一致|

收尾重复执行JSON解析、rubric/package校验和隔离V3加载，均通过；未启动量子化学、HPC或盲测。

逐文件与只读`v1_backup/paper_7cfd59d5c7061c6b`比较，实际变化清单：`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/critical_failures.json`、`evaluation/evidence_map.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/scoring_rules.json`、`evaluation/verified_computation_reference.md`、`package_manifest.json`、`paper_route.md`。以上文件均已在文件变化表及本节说明原因。保持原样：`agent_input/data/inputs/dma.xyz`、`agent_input/data/inputs/iron_peroxo.xyz`、`agent_input/data/inputs/molecular_inventory.json`、`agent_input/submission_schema.json`、`task_info.json`。历史`verified_computation_reference.md`原文逐字仍为本版文件后缀；实际运行的是临时`v3_autonomous_research`布局下的`TaskRepository.from_v3`。

## 2026-10-27 复核后确认的最小修复

本轮直接重读正文PDF7、9及SI33、35、37–38，并核对旧公开task/guide、当前全部公开文件和原生验证索引。确认两类问题：当前task将“oxidize a DMA C-H bond”作为已定反应类型；当前task/guide又把全程高自旋/TFE电子能基准写成必用模型。前者是当前题面新增提示；后者可追溯到旧guide第11行，**不是本轮新发现的实验事实，也不能误称全部由上一轮改编引入**。二者与自主决定初始氧化机制/相关态的目标存在张力，本轮据用户授权统一修复。

正文7的初始高自旋与正文9的TFE/MeOH(1:1)、213K实验条件保留。源计算采取TPSSh、CPCM纯TFE和指定电子能口径；SI33 TableS2中n=12双重态电子能相对六重态为−1.16 kcal/mol，而包含所列贡献的G为+3.14 kcal/mol。这恰说明实验初始S=5/2、全程电子态排序及选用的能量量并非同一命题；不能由初始实验自旋直接锁死后续所有态。

|实际改文件|本轮旧→新|理由及影响|
|---|---|---|
|`agent_input/task.md`|“oxidize a DMA C-H bond”→“initiate DMA oxidation”|不预给C–H/HAT反应类型；仍要求真实分子/电子证据解释活性|
|`agent_input/task.md`|必用high-spin体系/TFE continuum→保留实验起始S=5/2，明确它不固定后续态；自主论证混合溶剂表征和相关态|公开区分实验事实和模型假设，不新增完整自旋筛查或溶剂扫描义务|
|`agent_input/submission_guide.md`|固定电子能、TFE及不加热/色散项的baseline条款→声明实际电子能/焓/G、所含项及配平共同参照；自主选相关态/溶剂表征|避免正文开放但指南暗中仍强制历史模型；要求每个比较内部同量同参照，不能混加热项追数值|
|`evaluation/scoring_rules.json`、`reference_conclusions.json`|第一、二最终命题先按自主机制/活性解释评，再将O–O/HAT与六重态TFE说明为私有参考；各规则同步模型自主性|基准不是唯一通过路线。科学等价的、有证据的最终解释可直接pass；单纯模型不同不自动fail或review，仅已有列明的实质科学冲突才review|
|`evaluation/reference_qualification.json`|`physical_definition`明确改为`reference_physical_definition`；新增model admissibility与参考覆盖边界|旧原生证据只验证其原模型，不能因为放开自主模型就冒称已验证所有其他态/溶剂|
|`paper_route.md`|纠正仍提“source-scoped quantitative targets”的过时句，追加本轮自主模型说明|保留来源路线/数值，明确目前无该类active硬窗；不把来源约定转成路线义务|
|`package_manifest.json`|重建entries/content hash|对应当前载荷|

本轮复核原生验证结果位置：`docs/verification/small_molecules_autonomous_research/qualitative_acceptance_check_20261022T0725Z/7cfd_independent_review/review.json`的`comparisons`、`independent_native_audit`及`limitations`。共同RC电子高度仍为直接HAT28.085485453、活化13.069804975、后续HAT9.172638562 kcal/mol；各对应日志路径/sha/能量仍在原索引（例如`TS1a_high`、`TS1b_high`、`TS2b_high`），没有改动。来源13.1/9.2的旧±2窗仍原样保存在非评分key points。旧HAT相连IM2为−3.260376、来源构象IM2为−10.086223 kcal/mol；两构象互变动力学未算，不能说成一条全局最低连续轨迹。新羟化端点−45.752726及有限扫描也不证明最终胺/甲醛释放或精确实验速率。

这是解除不恰当模型锁定及答案提示，**不是补算、不是换金标、不是将所有替代机理自动判对**。三终答及40/25/35分不变；wrong identity、无竞争证据、不相容能量参照等仍失败。全量公开检查确认XYZ、inventory仅提供起始身份/初始自旋，没有优化遇合几何或后续路线；它们和schema完全未改。`reference_key_points.json`及`verified_computation_reference.md`对本轮before快照逐字节一致。JSON、V3 rubric、package及隔离TaskRepository/runtime实际通过：`paper_science_v3` / `final_results_100`，3项100分、0过程项。无新QM/HPC、无新盲测或科学PASS；原模型之外的科学结论必须由参试者实际证据支持。验证记录见`/tmp/rcb_upgrade19_20261027/confirmed_repairs/01/validation.json`。

父审口径确认：第三最终结果仍要求有计算支持的保留N–C键的初始羟化底物，而非最终脱甲基释放；本轮没有以模型自主性为由删除或放宽该化学结果。实验初始化学起点S=5/2保留，全程六重态和纯TFE是历史计算模型的选择，解除其唯一性不等于已验证新自旋途径。

</details>

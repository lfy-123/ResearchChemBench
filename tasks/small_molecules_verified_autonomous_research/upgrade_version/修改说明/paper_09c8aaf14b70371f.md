# 第一轮专家反馈调整 — 2026-11-03

明确五分子计算排序与实验比较；去掉题面预设的羟基分组提示；强调分子结构差异，允许描述符失效或排序未分辨。

Table 4中1和3的ACN LUMO几乎相同，而Epc明显不同。应让agent量化计算顺序及适用域；删除“含羟基”只是减少题面归因提示，不改变实际分子中的羟基，也不强制所有有效描述符复现同一个反例。

当前评分：化合物 3–5 中取代基依赖的还原关系 25分；所计算还原关系对化合物 1 和 2 的适用性 20分；全部五种化合物的 ACN/DMSO 溶剂效应尺度 15分；化合物 3 的 DCM／极性溶剂比较方向 10分；峰电位差异的分子假说及其证据边界 30分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_09c8aaf14b70371f 最终结论分项评分统一（2026-10-29）

逐条核对现有独立最终命题，保留其科学范围与权重，删除人工待定分及旧数值门槛政策。

化合物 3–5 中取代基依赖的还原关系 25分；所计算还原关系对含羟基化合物 1 和 2 的适用性 20分；全部五种化合物的 ACN/DMSO 溶剂效应尺度 15分；化合物 3 的 DCM／极性溶剂比较方向 10分；峰电位差异的分子假说及其证据边界 30分。

旧→新规则数：5→5；仅保留独立终答，全部semantic/pass-fail，100分。科学范围不变；公开题面/输入/提交结构字节不变。

相关论文位置：正文 PDF 第 2 页方法、第 7 页 Table 4、第 10 页 Table 6、第 12–15 页电子解释与 Fig. 13/14；SI 第 1–3 页化学身份、第 24–27 页坐标。逐项定位与证据身份见 [evidence_map.json](<../tasks/autonomous_research/paper_09c8aaf14b70371f/evaluation/evidence_map.json>) 及第 4 节的 `evidence_ids`。

逐项问题、独立性、来源与验证映射见[协调进度](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/最终结论分项评分统一_20261029/进度/organic19_a_paper_09c8aaf14b70371f.json)及[完整审查报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_09c8aaf14b70371f.md)。

修改文件及原因：

- `paper_route.md`：同步最终结论二态合同、引用或非评分历史证据边界。
- `package_manifest.json`：重建实际内容哈希。
- `evaluation/scoring_rules.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/qualification.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/conclusion_coverage_20261029.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/validation_plan.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_key_points.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/critical_failures.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/evidence_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/target_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。

未运行新量化计算。验证参考SHA256保持`72ac598799ad529fe569f0f528f6cc05b0798c94dfb407acc82dc1fa7748a4f9`，原始接受分类、数值差异和方法限制未升级。rubric/package/runtime加载及源/副本逐文件哈希校验通过。

当前专家事项：

|已知事实／数值|影响的规则或推断|专家需判断及建议处理|
|---|---|---|
|2 的 A/B 模型均有实际计算，但来源 E1/E2 标量归属尚未确定。|`r_hydroxy_departure` 的来源构象解释。|核对原文构象归属；当前以明确 A/B 模型和同定义关系判断，不要求猜中标签。|
|绝对 LUMO 有约 −0.13 eV 系统偏移，而 3–5 顺序和溶剂方向保留。|四类电子关系的可比性与第五项物理解释。|审查计算设置／构象差异是否影响有限推断；保留残差，不平移或追加隐含阈值。|
|5 的供电子和扩展共轭同时变化；羟基偏离原因未被独立分离。|`r_bounded_relationship` 的因果强度。|接受有计算锚点且清楚限定的假说；不据相关性认证唯一原因。替代模型的普适解释若有独立证据，按现行规则直接判断。|

上述是当前证据与解释的审查事项；描述符必须制造反例、化合物 5 骨架误写等设计问题已修复，不再作为待修任务。

汇总入口：[需专家重点审查的问题](<../需专家重点审查的问题.md>)。

---

## 2026-10-29之前的修改历史（非当前评分判据）

# paper_09c8aaf14b70371f 修改说明

## 问题与范围
原题要求解释五种查尔酮的还原峰电位和溶剂依赖，但“molecular-level explanation”过宽。新版仍为解释题，保留五分子、ACN/DMSO和3号DCM对照，明确四类比较及一个独立物理假说。未改为预测题、未增加绝对电位/全电化学机制，也未删除2号。

## 文件级变更
|文件|改前→改后|原因|
|---|---|---|
|agent_input/task.md|泛化解释→五节英文题干及明确比较、数量定义、边界|使题面与可判断最终答案对应，同时保留方法自主性|
|evaluation/scoring_rules.json|V2四个intermediate+一个汇总项→V3五个独立结论，25/20/15/10/30|前四项本来就是最终构效/溶剂比较，非流程节点；第五项改为新增分子解释，避免重奖比较事实|
|reference_conclusions/key_points、evidence_map、critical_failures|同步五项结论、原生证据与二态/复核策略；旧关键点标scored=false|过程证据继续可追溯，不独立得分|
|qualification/current_verification_status/target_map/validation_plan|清除过时active空间分布规则及已验证总标记，保留历史字段|旧通过不能自动转V3通过|
|paper_route、verified_computation_reference|路线重写当前范围；验证参考只加顶部说明，以下原文保留|纠正旧“新系列未验证/2号排除”的活动误导|
|submission_guide/schema、manifest|保留原提交字段，只同步结论说明和文件哈希|无需新合同|

五种mapped SMILES、E构型、分子式、CV测量和未知条件均保留；已直接核SI pp.1–3化学名及pp.24–27坐标。公开输入只有实验值，没有作者LUMO/胜出模型。原文相关定位留私有侧。旧source_record_id是中立实验记录标识。

## 最终规则
|rule_id|最终命题|分|判定|
|---|---|---:|---|
|r_series_3_5|3–5电子结构—还原关系|25|二态|
|r_hydroxy_departure|1/2偏离同一描述关系|20|二态|
|r_acn_dmso|五种ACN/DMSO变化尺度小|15|二态|
|r_dcm_comparison|3号极性溶剂相对DCM轨道稳定化方向|10|二态|
|r_bounded_relationship|以计算支持的结构/介质效应解释峰电位差异及证据边界|30|只有同身份/参照的两套有证据物理解读仍冲突才复核；缺算/猜测失败|

总100。原批准活动规则无硬数值窗口；本轮没有新增或放宽窗口。原先已退出范围的E/Z势垒及角度窗口保留于qualification历史记录，不恢复计分。轨道/自旋图仅作可选证据，不作为额外任务。

## 题面—来源—规则—原生证据
原生总索引：`docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_native_checks.json`；2号补充核对`parent_09c8_native_crosscheck.json`。索引逐行给出log/fchk/cube绝对路径。

|最终要求|正文/SI|新规则|本地值/文件|覆盖或缺口|
|---|---|---|---|---|
|3–5关系与数值|正文p.7 Table4，p.14 Fig13；SI pp.2–3身份|r_series_3_5|ACN LUMO −2.669734/−2.606143/−2.424953 eV；对应neutral fchk|趋势覆盖；不是作者−2.538/−2.470/−2.293精确复现|
|1/2反例|p.7、p.10 Table6、p.14；SI pp.1–2、24–25|r_hydroxy_departure|1−3差0.005490/0.005212 eV，Epc差0.163/0.170 V；2/A −2.634554/−2.637718，B −2.567449/−2.570760 eV|两构象均反例；作者E1/E2标量归属未决|
|ACN/DMSO尺度|p.7 Table4、p.12|r_acn_dmso|DMSO−ACN约−0.002261至−0.004279 eV，13中性fchk|小尺度覆盖，2/4/5实验微小方向未认证|
|3号DCM方向|p.14 Fig14|r_dcm_comparison|降低0.029032/0.031293 eV，3/DCM、ACN、DMSO fchk|覆盖；作者0.030/0.032为来源值|
|分子解释与边界|pp.12–15，Fig13/14|r_bounded_relationship|上述关系/反例及25态原生记录支持有限轨道解释|可支持有限电子结构解释，不证明羟基唯一因果、绝对电位或全机制|

## 方法差异与自检
源方法B3LYP/6-311+G(2df,2p)、IEF-PCM、298 K；本地相同层级，并显式Tight/UltraFine等设置；A/B只代表明确构象而非穷尽。1/3/4/5绝对LUMO比源低0.126783–0.136391 eV，2号A/B差0.074449–0.141718 eV，未平移修正。本轮直接重读原生1/ACN fchk，提取−2.6642441956 eV；完整索引支持其余逐量定位。旧25态验证中只有12阴离子和4个2号中性有显式Stable，不能全称全局基态已证。

没有新QM/HPC；同量同身份证据可复用。`validate_task_package`及V3 rubric已通过（仅合同）。仍需专家核实的是2号原文构象归属与第五项解释的科学充分性；未进行ARCHE盲测、不宣称V3科学全通过。

父级复审修正：题面删除外部论文/SI措辞；四项比较均允许同物理命题的已验证电子接受性/溶剂稳定化等价量直接通过，LUMO仅为来源参考路径，避免题面自主选择descriptor与私有强制LUMO冲突。第五项补明正文p.14中5号para-NH2/para-OMe供电子效应的参考解释，仍不捏造OH唯一因果。已再次重建manifest并验证。

末次组内核对：相对v1_backup实际修改15个文件，与上表覆盖一致；未新增/删除文件，agent_input/data原始数据逐字未改，验证参考历史原文完整保留。独立临时仓库加载本篇为paper_science_v3 / final_results_100，权重合计100，包与V3合同通过；公开文本无外部作者/论文/SI依赖及旧过程计分。五个mapped SMILES均可解析且分子式一致，五个烯键均明确为E；保留原子映射未改。 这些检查只确认合同、身份和证据读取，不代表本篇科学结果已全部通过。

## 2026-10-27 已确认问题定向修复（独立交叉复核后）

**确认依据。** 交叉复核直接对照正文 PDF 第 2、7、14、15 页与 SI `supplementary_001.pdf` 第 1–4 页，而非沿用前轮自评。第 14 页的 1/3 近等 LUMO 与 2/3 趋势反例针对中性 LUMO 关系；第 15 页另讨论羰基 13C 化学位移关系，不能据此推导所有可选描述符都必须失败。SI 第 3 页明确化合物 5 为 `(2E)-1-(4-aminophenyl)-3-(6-methoxynaphthalen-2-yl)prop-2-en-1-one`，并非两个 para 取代苯基。原生审计 `docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_native_checks.json` 与同目录 `parent_09c8_native_crosscheck.json` 对应 25 组 log/fchk；ACN 的 1/3 LUMO 为 −2.664244/−2.669734 eV，差约 0.00549 eV，而 Epc 差 0.163 V；2 的两个已识别模型亦支持该 LUMO 关系的偏离。这些记录不能排除未实际检验的其他描述符。

**具体修复与理由。** `r_hydroxy_departure` 保留 ID 和 20 分，改为判断所提交计算关系对 1/2 的实际适用范围。来源 LUMO 的反例仍是充分参照；若其他独立实算、同物理定义且与测得 Epc 关系成立的模型支持五个化合物的共同关系，也可直接通过，不强造羟基偏离或额外机制。仅拟合给定 Epc、将观测重命名为计算量或无证据声称普适关系均失败。该项 `allow_need_review` 从 false 改为 true，仅容纳有效计算支持、经身份/构象/溶剂/物理量核查后仍无法解决的实质科学冲突；已充分成立的替代解释直接通过，科学未决不当作通过，缺证据不进入复核。第五项修正 5 的 4-aminophenyl / 6-methoxynaphthalen-2-yl 实际骨架，保留供电子与扩展共轭的有限假说，不将二者贡献或羟基原因认作唯一因果。前文“para-NH2/para-OMe”表述由本节纠正。

**同步与边界。** 规则、reference conclusions、对应原有及生成的 supporting key points、四份活动范围 metadata、证据覆盖与私有 route 已同步。五项仍为 25/20/15/10/30；公开题面原本已中立地询问适用性，因此未更改。未增加绝对电位、轨道图、自旋或构象搜索义务；2 的来源构象精确归属及 LUMO 绝对偏差仍保留。历史验证参考逐字未动。

**实际修改文件（相对本任务包）。**

- `evaluation/current_verification_status.json`
- `evaluation/evidence_map.json`
- `evaluation/qualification.json`
- `evaluation/reference_conclusions.json`
- `evaluation/reference_key_points.json`
- `evaluation/scoring_rules.json`
- `evaluation/target_map.json`
- `evaluation/validation_plan.json`
- `package_manifest.json`
- `paper_route.md`

另追加本篇 `修改说明/paper_09c8aaf14b70371f.md`。本轮只修改四篇获准升级副本及对应说明；原版、其他任务、README、总体报告与 benchmark 代码均未编辑。

**检查结果与保留边界。** 已重建 manifest；所有包内 JSON 可解析，`validate_rubric` 与 `validate_task_package` 均通过，并将本篇复制到隔离目录后实际执行 `TaskRepository.from_v3` 加载成功。相对修复前快照，5 条 rule_id、reference_id、条数、100 分权重、已有数值 target/tolerance/unit、binding 与证据 ID 保持不变；规则/结论/generated supporting item 的预期和标题一致。`agent_input/data`、提交 schema、来源 evidence 数组及 historical 字段逐字或结构等值核对通过。未新增或删除包内文件。校验记录：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/02/validation.json`；修复前快照：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/before/`。以上确认合同、同步和加载，不代表所有最终科学结论已获验收；没有新 QM/HPC、ARCHE 盲测或发布。

</details>

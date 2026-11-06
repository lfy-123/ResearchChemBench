# 第一轮专家反馈调整 — 2026-11-03

删除双胺化观察PI5及时间趋势要求，保留首次两对位电子响应、构象/对称性和底物证据不能独立确定净ee的结论。

SI Table S2提供特定构象两对位的NPA比较，不能单独计算后续双胺化动力学拆分或净ee。删除PI5和时间趋势要求，同时保留首次位点响应、机械穿套、构象/对称性及推断范围。不强制NPA为唯一方法，不把一次构象计算当作溶液系综。

当前评分：计算溶液结构及对位环境的等价或不等价 35分；计算对位响应及其对亲电胺化的含义 35分；首次胺化位点响应及底物证据对净ee推断的范围 30分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_8769f3cc6d18e26c：2026-10-29 最终结论分项统一

现行分项：计算溶液结构及对位环境的等价或不等价35分；计算对位响应及其对亲电胺化的含义35分；计算底物结构及位点响应对净对映选择性能够确立的内容30分。合计100分，全部semantic/conclusion，逐项pass/fail；无数值匹配门槛或need_review。

旧→新：3项→3项。原数值规则：无；原数值仅留历史证据。

科学范围未变：task.md、全部agent_input/data、guide和submission_schema均保持原字节。原要求的能量、位点、产物、比较与解释仍完整保留；量化结果作为结论证据，取消作者目标值和容差评分。构象、描述符、作者节点、计算次数及完成流程没有独立奖励。已存在不同终答框架保留，未为统一条数人为拆分。

## 科学要求—规则—独立性—来源—已有验证

|公开科学要求|规则|独立性|正文/SI|已存验证支持与缺口|
|---|---|---|---|---|
|必需结果1：S的结构组织、相互作用及两个para环境|r_structural_account|空间预组织是否造成环境等价，不以电荷差或催化选择性成立为前提。|正文PDF8–10，Fig.5–6；SI002 PDF70–71、79–80，Table S2|123原子、363正频、单次穿线；质心距3.8314515/4.9406438 Å支持甲苯单构象组织。 主要边界：只有SMD甲苯局部最低点；实验CHCl3的系综及动力学未被验证。|
|必需结果2：两个para数值响应与相对胺化易感性|r_relative_susceptibility|电子响应及其化学意义与具体组织解释不同；同一几何可有不同描述符响应。|正文PDF8–10，Fig.5–6；SI002 PDF70–71、79–80，Table S2|同几何NPA −0.27809/−0.26568 e，差−0.01241；来源差−0.018，幅度小31.06%。 主要边界：只有SMD甲苯局部最低点；实验CHCl3的系综及动力学未被验证。|
|必需结果3：结构/位点/对称对净ee及单/双胺化时间趋势的解释能力|r_enantioselectivity_reach|判断底物信息对催化选择和时间趋势的推断范围，可在不同局部结构/响应解释下独立成立。|正文PDF8–10，Fig.5–6；SI002 PDF70–71、79–80，Table S2|实际构象与镜像操作支持对称关系；未计算催化选择、布居、交换或后续动力学。 主要边界：只有SMD甲苯局部最低点；实验CHCl3的系综及动力学未被验证。|

## 文件与理由

scoring_rules更新逐项判据/二态政策；reference_conclusions与supporting key points同步；原key points完整置于明确非评分历史记录；evidence_map及覆盖/资格文档更新现行映射，保留来源证据及历史接受分类；paper_route区分现行评分和历史路线；package_manifest重建。验证参考文件逐字不改。同步审查页完整中文规则与原始JSON，以及审查任务副本。

## 保留专家事项

- 只有SMD甲苯局部最低点；实验CHCl3的系综及动力学未被验证。
- para NPA差幅度较来源小约31.06%，保留方法/网格差异；这不是数值扣分门槛。
- 来源允许位阻较小芳环参与的替代解释，底物描述符不能证明唯一催化机制。

没有新QM/HPC或盲测，合同和运行时通过不等于科学满分；已知参考缺陷另记objective_issue_flags，不恢复人工待定得分。

## 2026-10-27及以前历史修改说明（评分政策已由上文替代）

下列记录保留原数值、方法、偏差及旧设计历史；旧窗口和need_review不是当前评分要求。

# paper_8769f3cc6d18e26c 修改说明

## 原题与改题
保留轮烷底物溶液结构、两para响应及对实验机械平面手性选择性解释的解释题。未改分子、穿线拓扑、CHCl3/25°C实验、试剂及mono/di观察；并未扩大成催化循环或为了省算删除真实反应关联。原7项包含三个接触节点、NPA节点和重复汇总；新版按三个独立终答拆分：结构35、响应35、选择性解释范围30。

## 修改文件
|文件|前后变化|理由|
|---|---|---|
|task.md|长通用研究模板→五节英文、三个明确最终输出|删除公开author guidance及过程质量分措辞；明确单构象/系综、描述符/动力学|
|scoring_rules、reference_conclusions/key_points|7项→3项；旧氢键/芳环/CHπ/NPA保留非计分证据|不把作者接触清单包装成大机制，不重复奖励同一结构事实|
|evidence_map/critical_failures、reference_qualification|精确原文与native映射，V3二态/科学复核|旧数值review不自动PASS，亦不能凭幅度无硬窗暗扣|
|research_contract/task_definition/reproduction_protocol、paper_route|当前范围及规则同步；旧未取到TableS2等记录明确历史|SI已实际读取，不能保留活动缺源误报；作者协议仅私有背景|
|submission_guide/schema、verified_reference、manifest|原字段保留、去过程质量分；验证仅加顶部范围说明；哈希更新|不加提交合同、保留计算历史|

公开system.json全英文身份与观察保留；不新增作者姿态/电荷/胜出机理。穿线25环和完整两组分身份依据SI坐标核对，不把两个未穿线SMILES当完整体系。

## 规则
|rule|终答|分|状态|
|---|---|---:|---|
|r_structural_account|条件性溶液预组织解释两位点空间不等价|35|确定支持/缺证为二态；相同拓扑有效替代结构显示不同组织或等价位点且科学冲突未决才复核|
|r_relative_susceptibility|同构象电子响应数值及相对胺化假说|35|缺算/错映射失败；有效替代响应/构象的实质反向解释才复核|
|r_enantioselectivity_reach|由真实位点和镜像证据推导底物不能独自决定净ee|30|二态；通用局限段落不算结果|

总100，全required。−0.277/−0.259 e始终无硬窗口；本轮未新增容差。等价已成立直接pass，不自动送review。各接触/频率/结构不是独立计分项。

## 逐项证据对应
|题面结果|原文/SI|规则|实际本地量/文件|覆盖缺口|
|---|---|---|---|---|
|条件性结构组织|正文PDF8–10、SI002 PDF70–79|r_structural_account|native_recomputed.json记录123原子、363正频、一次穿线；A/B质心3.8314515/4.9406438Å、角13.50247/43.14617°，两H···O1.8676344/2.2073412Å|支持甲苯单最低点，不是CHCl3系综；晶体4.14Å不能当本地值|
|两para数值及胺化响应|正文PDF10，SI002 TableS2 PDF79–80|r_relative_susceptibility|最终原子120/74 NPA−0.27809/−0.26568 e，差−0.01241 e|源−0.277/−0.259、差−0.018；差值幅度小31.0556%，方向同；不是速率/势垒|
|净ee的解释范围、时间趋势|正文PDF10 Fig6/替代机制；SI002 PDF71镜像图|r_enantioselectivity_reach|同最低点及x镜像/位点映射支持条件性不等价与无手性场净对称推论|未算催化选择、构象交换或后续动力学；不能将时间观察当已计算动力学拆分|

索引完整路径：`docs/verification/small_molecules_autonomous_research/job_followup_20261025T0135Z/parent_8769_audit/native_recomputed.json`。其native_log指向`job_followup_20261024T1533Z/new44_group_04/paper_8769f3cc6d18e26c/returned_CalcFC_fixedtrust/native/returned_CalcFC_OptFreq_NPA/gaussian.log`；本轮直接重读最后NPA表确认120/74两电荷，不使用旧未收敛几何−0.01695 e。

## 方法、验证与未决
源G09 E.01，本地G16 C.01/G09Defaults/UltraFine；同B3LYP-D3BJ/def2SVP SMD甲苯优化/频率和M06-2X NPA，原网格未知。计算甲苯而实验CHCl3是既有明确差异，不能声称溶剂迁移已证。实际B3LYP E−3098.45691929 Eh，M06-2X E−3096.90692049 Eh，不能混配不同层级热校正；本题未要求该能量目标。

本轮无新QM/HPC。同身份同物理量可复用，当前三终答只接受有边界的结构/响应解释；真实CHCl3系综与唯一催化机理未覆盖且没有被宣称通过。V3/package/JSON自检通过，未跑ARCHE盲测；父级/专家需核定替代构象与溶剂外推解释，不以旧RESULTS_COMPLETE状态替代新结论判断。

末次组内核对：相对v1_backup实际修改15个文件，与上表覆盖一致；未新增/删除文件，agent_input/data原始数据逐字未改，验证参考历史原文完整保留。独立临时仓库加载本篇为paper_science_v3 / final_results_100，权重合计100，包与V3合同通过；公开文本无外部作者/论文/SI依赖及旧过程计分。结构对应依据完整123原子图及最新原生穿线审计；单个溶液构象不等同系综。 这些检查只确认合同、身份和证据读取，不代表本篇科学结果已全部通过。

## 2026-10-27 已确认问题定向修复（独立交叉复核后）

**确认依据。** 交叉复核直接对照正文 PDF 第 8–10 页以及 `supplementary_002.pdf` 第 70–72 页的计算方法/动态对映构象与第 79–80 页 Table S2。来源是一个非对称堆积构象及其对称关系，并保留较少位阻芳环参与反应的替代解释；并未排除所有有根据的等价结果。`docs/verification/small_molecules_autonomous_research/job_followup_20261025T0135Z/parent_8769_audit/audit.json` 对应真实 SMD-甲苯局部最低点和静态镜像关系，para NPA −0.27809/−0.26568 e，差 −0.01241 e；它不能证明 CHCl3 系综权重、交换速率、催化剂偏好或净 ee。公开题面原本允许有证据的等价结果，而旧三项私有预期持续限定局部不等价，确有不一致。

**具体修复与理由。** 三条稳定 ID、35/35/30 权重保持不变，全部接受有真实计算依据且物理上成立的等价或不等价结果。结构项仍要求有效穿线溶液模型和具体空间证据；电子项仍要求实际数值、统一定义和位点映射；解释边界项必须结合计算结构、位点响应及实际适用的对称关系。单构象局部等价与对称相关构象的系综平均等价分开判断，后者须有适当状态映射、权重或已经证明适用的物理对称性，不能任意平均或假设等价绕过计算。对实算构象施加明确对称操作可建立相关构象关系，无须强制再跑一份镜像 QM，但该操作本身不证明系综分布或交换速度。前两项仅对同一物理范围内、核查后仍未解决的真实科学冲突保留 need_review；已成立等价直接通过，缺少结构/数值证据失败。第三项仍为二元判定，不新增催化循环、过渡态或系综计算义务。

**同步与边界。** 三项规则、结论、生成 supporting items、旧四条来源构象 key points、task definition、research contract、reference qualification、evidence map 和私有 route 同步；旧 key points 明确为来源构象上下文，不作为强制接触清单。公开 task/guide 仅澄清实际计算证据及局部/平均区别，并将对称关系表述绑定实际计算状态，没有披露来源接触、NPA、具体构象或机制。原始 molecular inputs、schema 和全部历史验证参考未改。

**实际修改文件（相对本任务包）。**

- `agent_input/submission_guide.md`
- `agent_input/task.md`
- `evaluation/evidence_map.json`
- `evaluation/reference_conclusions.json`
- `evaluation/reference_key_points.json`
- `evaluation/reference_qualification.json`
- `evaluation/research_contract.json`
- `evaluation/scoring_rules.json`
- `evaluation/task_definition.json`
- `package_manifest.json`
- `paper_route.md`

另追加本篇 `修改说明/paper_8769f3cc6d18e26c.md`。本轮只修改四篇获准升级副本及对应说明；原版、其他任务、README、总体报告与 benchmark 代码均未编辑。

**检查结果与保留边界。** 已重建 manifest；所有包内 JSON 可解析，`validate_rubric` 与 `validate_task_package` 均通过，并将本篇复制到隔离目录后实际执行 `TaskRepository.from_v3` 加载成功。相对修复前快照，3 条 rule_id、reference_id、条数、100 分权重、已有数值 target/tolerance/unit、binding 与证据 ID 保持不变；规则/结论/generated supporting item 的预期和标题一致。`agent_input/data`、提交 schema、来源 evidence 数组及 historical 字段逐字或结构等值核对通过。未新增或删除包内文件。校验记录：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/02/validation.json`；修复前快照：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/before/`。以上确认合同、同步和加载，不代表所有最终科学结论已获验收；没有新 QM/HPC、ARCHE 盲测或发布。

</details>

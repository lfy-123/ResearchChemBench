# 第一轮专家反馈调整 — 2026-11-03

保留有限成键和产物释放路径；删催化剂再生/循环闭合，将完整周转能跨改为有限路径活化高度及条件性温度影响。

删再生后，继续强制“完整周转能跨”会造成题面和评分矛盾。保留活性物种形成、末端炔活化、偶联和产物释放，报告剩余锌物种及配平库；r_turnover_span改名r_path_activation，并只解释有限路径活化高度。温度项明确条件性Eyring/活度假设，不声称稳态TOF。正文与SI的Int-2能量冲突保留。

当前评分：从给定预催化剂出发在化学上可达的活性锌物种 20分；成键化学及锌氧化态行为 25分；至二炔释放的配平有限路径热力学 20分；已研究有限产物形成路径的主要活化需求 20分；升温对已研究产物形成活化的条件性影响 15分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_cfff299c39d69520：2026-10-29 最终结论分项统一

现行分项：从给定预催化剂出发在化学上可达的活性锌物种20分；成键化学及锌氧化态行为25分；配平催化自由能网络的热力学可行性与闭合20分；控制配平催化周转的动力学瓶颈20分；在 125 °C 操作的动力学解释15分。合计100分，全部semantic/conclusion，逐项pass/fail；无数值匹配门槛或need_review。

旧→新：5项→5项。原数值规则：r_turnover_span；原数值仅留历史证据。

科学范围未变：task.md、全部agent_input/data、guide和submission_schema均保持原字节。原要求的能量、位点、产物、比较与解释仍完整保留；量化结果作为结论证据，取消作者目标值和容差评分。构象、描述符、作者节点、计算次数及完成流程没有独立奖励。已存在不同终答框架保留，未为统一条数人为拆分。

## 科学要求—规则—独立性—来源—已有验证

|公开科学要求|规则|独立性|正文/SI|已存验证支持与缺口|
|---|---|---|---|---|
|必需结果1：活性锌物种与从前体可达性|r_active_catalyst|活性物种配平形成不同于其后偶联机制成立。|正文PDF2–4 Schemes4–6、Fig.2/Table1；SI PDF2能量、4–6 TS坐标、13 Eyring|ZnEt2+2ProH→中性ZnII双脯氨酸根+2ethane，原生−98.533420。 主要边界：来源Int2正文9.6与SI组装4.078812 kcal/mol冲突保留，不选更贴本地5.476275的值。|
|必需结果2：成键、产物映射及锌氧化态行为|r_coupling_chemistry|成键/氧化态关系不由循环净能量或速率预测自动确立。|正文PDF2–4 Schemes4–6、Fig.2/Table1；SI PDF2能量、4–6 TS坐标、13 Eyring|47原子TS唯一虚频−443.7185及三键变化模式、来源/最低点映射；没有独立IRC。 主要边界：来源Int2正文9.6与SI组装4.078812 kcal/mol冲突保留，不选更贴本地5.476275的值。|
|必需结果3：配平自由能网络、释放和再生热力学|r_balanced_profile|热力学循环闭合不同于识别动力学瓶颈。|正文PDF2–4 Schemes4–6、Fig.2/Table1；SI PDF2能量、4–6 TS坐标、13 Eyring|配平网络0→5.476275→30.132377→−36.722101→−69.832392，账本原子/电荷平衡。 主要边界：来源Int2正文9.6与SI组装4.078812 kcal/mol冲突保留，不选更贴本地5.476275的值。|
|必需结果4：共同参照控制性span及局部势垒区别|r_turnover_span|整体活化控制不同于局部键变化或净反应有利，也不同于温度推断。|正文PDF2–4 Schemes4–6、Fig.2/Table1；SI PDF2能量、4–6 TS坐标、13 Eyring|整体30.132377与局部24.656102 kcal/mol不同；共同参照包含Cs-prolinate/CsHCO3等库。 主要边界：来源Int2正文9.6与SI组装4.078812 kcal/mol冲突保留，不选更贴本地5.476275的值。|
|必需结果5：温度对速率/时间尺度的影响|r_temperature_effect|温度尺度推断需要物理速率模型，不以瓶颈名称或贴合span数值自动通过。|正文PDF2–4 Schemes4–6、Fig.2/Table1；SI PDF2能量、4–6 TS坐标、13 Eyring|fixed-ΔG Eyring k298=5.0825e−10、k398=2.3941e−4 s−1，约471048倍；未重算398K热化学。 主要边界：来源Int2正文9.6与SI组装4.078812 kcal/mol冲突保留，不选更贴本地5.476275的值。|

## 文件与理由

scoring_rules更新逐项判据/二态政策；reference_conclusions与supporting key points同步；原key points完整置于明确非评分历史记录；evidence_map及覆盖/资格文档更新现行映射，保留来源证据及历史接受分类；paper_route区分现行评分和历史路线；package_manifest重建。验证参考文件逐字不改。同步审查页完整中文规则与原始JSON，以及审查任务副本。

## 保留专家事项

- 来源Int2正文9.6与SI组装4.078812 kcal/mol冲突保留，不选更贴本地5.476275的值。
- TS默认残余力通过但位移诊断不通过；来源几何/模式和匹配最低点支持连接，未做新优化或独立IRC。
- fixed-ΔG高温速率为近似；不能称已计算398K自由能或实验速率。

没有新QM/HPC或盲测，合同和运行时通过不等于科学满分；已知参考缺陷另记objective_issue_flags，不恢复人工待定得分。

## 2026-10-27及以前历史修改说明（评分政策已由上文替代）

下列记录保留原数值、方法、偏差及旧设计历史；旧窗口和need_review不是当前评分要求。

# paper_cfff299c39d69520 修改说明

## 科学问题与文件
原题询问Zn/proline二炔偶联的活性物种、配平循环、控制能跨与125°C解释。全部保留，仍为自主机制解释+产物连接推导，未删活化/再生或把其缩成一条偶联TS。

|文件|改前→改后|理由|
|---|---|---|
|task.md|单段泛问→五节英文五项最终输出|区分形成G、局部势垒、控制跨度、净G和温度近似|
|scoring_rules/reference_conclusions/key_points|8项含5作者节点→5独立终答20/25/20/20/15；原节点scored=false|分别回答活性物种可达性、成键/价态性质、热力学循环、控制量和温度效应；不按节点完成数给分|
|evidence_map/critical_failures、qualification/reference_qualification|当前V3及逐命题原生对应，旧资格明确历史|历史定性PASS不转新PASS；硬窗禁止review绕过|
|science_v2_evidence_review、paper_route|旧V2内容包为历史来源记录，现活动规则明确|保留来源和计算而不保留旧活动计分表|
|verified_computation_reference.md、submission_guide.md/submission_schema.json、package_manifest.json|验证只加前言；guide取消过程与结果独立计分及外部论文/SI措辞，改为最终结论计分；通用schema只更新描述、哈希重建|不改benchmark或重造交付接口；公开说明和V3一致|

system.json不变：完整反应物、L-proline立体与储库身份保留；没有公开作者活性物种、IS序列、TS或29.2答案。反应产物身份仍由原子映射推导。

## 最终规则
|rule|命题|分|状态|
|---|---|---:|---|
|r_active_catalyst|活性Zn物种及配平形成可达性|20|真实替代物种的竞争实质未决才review|
|r_coupling_chemistry|二炔成键/离去及Zn价态机制|25|充分替代反应电子证据的实质争议才review|
|r_balanced_profile|活化/释放/再生热力学关系与循环闭合|20|二态|
|r_turnover_span|配平控制能跨29.2±1.0kcal/mol|20|硬二态|
|r_temperature_effect|实算跨度导出的125°C相对动力学可达性|15|二态|

全required、总100；不对Int2、形成/再生、速率新增窗口，不以定性取代29.2±1。原子/电荷平衡和结构/TS证据是结论成立条件，不独立计分。

## 输出→来源→新规则→原生证据
主账本`docs/verification/small_molecules_autonomous_research/paper_cfff299c39d69520/closeout_followup_20261020T1530Z/balanced_numerical_analysis.json`含每一组分原生日志和hash；同目录source_TS_qualification.json/author_route_connection.json记录TS边界。

|题面输出|正文/SI|规则|实际计算值及原生量|缺口/覆盖|
|---|---|---|---|---|
|活性物种/形成|main2–3 Schemes4–6；SI2|r_active_catalyst|中性ZnII双prolinate最低点；ZnEt2+2ProH→Int1+2ethane ΔG−98.533420 vs源SI−98.515222|形成有利；不能凭Zn0优化失败排除所有其他机制|
|成键/价态|main4 Fig1/Table1，SI4–6 TS|r_coupling_chemistry|原源TS135频唯一−443.7185；C18–C30成键、C30–Br17断裂、Zn31–C18释放；独立端点图|未独立IRC/新Opt；仅源路线+反应模+端点支持，不夸大盲发现|
|配平自由能网络|main4 Fig2，SI2|r_balanced_profile|0→5.476275→30.132377→−36.722101→−69.832392；再生−33.110291|源Int2正文9.6与SI4.078812冲突未解，均保留；局部值不是替源|
|控制能跨|main4 Fig2，SI2|r_turnover_span|GTS+GCsPro+GCsHCO3−GInt1−GR1−GR2−GCs2CO3=30.132377435|对29.2偏+0.932377在原±1内；局部24.656102不能替代|
|125°C动力学|SI13|r_temperature_effect|固定本地ΔG，k298=5.08248533e−10、k398=2.39409564e−4s−1，471048倍、48.25min半衰期|源2.4e−9/7.9e−4未精确复现；没有398K重算|

## 方法、原生复读与未决
本轮直接读Int1/2/3和原源TS原生日志总G：−866.694575/−813.206484/−466.017414/−1134.063144Eh。源TS G−1134.062445，相差−0.000699Eh。保持作者B3LYP-D3/6-31+G(d)、Zn/Br/CsLANL2DZ/Hay–Wadt、CPCM乙醇、298.15K；本地G16替G09，未公开阻尼/角函数/网格约定不能说完全复刻。

源TS残余力满足默认阈值，频率完整且反应模正确，但位移0.101975/0.025247bohr未过诊断；没有实际新Opt步骤。连接支持受限于作者路线证据，不能把频率成功写成完整自主路径验证。硬窗数值命中与连接科学充分性分开登记。

本轮无新QM/HPC；同物种/同参照证据复用。不需要擅加全部循环TS，但父级/专家须复核既有源TS连接充分性及Int2冲突，不应据旧PROVISIONAL_PASS给新满分。V3/package/JSON已过，数值规则常规容差审查diagnostic不是need_review放行。未做ARCHE盲测。

末次组内核对：相对v1_backup实际修改14个文件，与上表覆盖一致；未新增/删除文件，agent_input/data原始数据逐字未改，验证参考历史原文完整保留。独立临时仓库加载本篇为paper_science_v3 / final_results_100，权重合计100，包与V3合同通过；公开文本无外部作者/论文/SI依赖及旧过程计分。原公开组分SMILES与电荷可解析，L-proline手性中心CIP为S；没有改动输入身份或立体信息。 这些检查只确认合同、身份和证据读取，不代表本篇科学结果已全部通过。

</details>

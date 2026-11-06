# 第一轮专家反馈调整 — 2026-11-03

提供D4/D5氧代碳正离子、A/B硼氢负离子及A/B/C硼烷图；明确从局部氢转移起步，排除上游成环/H2活化。

正文Fig. 1与SI §7.3的选择性计算从氧代碳正离子/硼氢负离子出发。现有卡虽排除全循环，却未给局部起点，容易迫使agent额外推断上游。现补齐带电反应物及硼烷图并声明任意单一对映体仅作cis/trans模型；不提供TS、能差或优势面。

当前评分：催化剂酸性与反应性能具有不同的分子起因 25分；D4 的 cis 偏好来自形成效应而非产物稳定性偏好 25分；A/B 变化以依赖模型的强度影响 D4 立体化学区分 20分；增大环尺寸使 cis 形成偏好与 cis 产物稳定性同向 30分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_7a1d5d7c60a0ae04 最终结论分项评分统一（2026-10-29）

逐条核对现有独立最终命题，保留其科学范围与权重，删除人工待定分及旧数值门槛政策。 D4产物近简并不强制微小符号；A/B区分允许实际敏感性证据支持的排序不稳健结论直接通过，不将0.088814硬化为跨方法规律。

催化剂酸性与反应性能具有不同的分子起因 25分；D4 的 cis 偏好来自形成效应而非产物稳定性偏好 25分；A/B 变化以依赖模型的强度影响 D4 立体化学区分 20分；增大环尺寸使 cis 形成偏好与 cis 产物稳定性同向 30分。

旧→新规则数：4→4；仅保留独立终答，全部semantic/pass-fail，100分。科学范围不变；公开题面/输入/提交结构字节不变。

来源定位：正文 PDF 第 6–7 页机制讨论/Figure 1，以及筛选结果；SI S55–S64 的计算方法、Tables S4/S5、相互作用和坐标，另核对 S75–S76。

逐项问题、独立性、来源与验证映射见[协调进度](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/最终结论分项评分统一_20261029/进度/organic19_a_paper_7a1d5d7c60a0ae04.json)及[完整审查报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_7a1d5d7c60a0ae04.md)。

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

未运行新量化计算。验证参考SHA256保持`e29189f8b047788af706de2ebc5f91aadfe3704ddf3eab7953c464f25518ce2e`，原始接受分类、数值差异和方法限制未升级。rubric/package/runtime加载及源/副本逐文件哈希校验通过。

当前专家事项：

1. **催化剂差处于微小能差尺度。** D4 的 B−A 只有 0.088814 kcal/mol，来源为 1.391483；影响 `r_catalyst_selectivity_contrast`。建议评估现有构象和热化学敏感性是否足以支持名义方向及其不确定性，不接受“大幅稳健增强”或酸性唯一因果。有实际敏感性证据支持近简并或排序不稳健时，按本项明确边界直接pass；证据不足则fail并说明理由。
2. **D5 极软模决定幅度。** 0.514759064 cm⁻¹ 模使主产物差为 5.517269，而 1 cm⁻¹ 截止时为 1.189275；影响 `r_ring_size_relationship`。建议审核低频物理意义及一致处理，保持来源与主值的 +2.918602 残差。大幅但定义明确的偏差本身不是fail理由，也不能选择更近来源的口径掩盖它。
3. **来源方法与实验边界。** SI 气相/溶剂几何表述冲突、ORCA 版本不同、乙醚模型与 CPME 实验不同；关联催化功能和全部 G 比较。建议保留差异并审查其是否影响所作有限推断，不额外要求完整溶剂筛选或周转模型。FIA/HIA 的单原子参照需统一，不与反应 G 混用。

---

## 2026-10-29之前的修改历史（非当前评分判据）

# paper_7a1d5d7c60a0ae04 修改说明

## 问题与科学边界
原题解释D4的A/B催化剂立体差异、固定A的D4/D5环大小效应，以及K4三催化剂表现。本次不改范围/难度，仍公开实验顺反比和收率作为解释题，改为四项最终关系；未增加K4呋喃机制、D5/B或D4/C、全循环与速率。

## 文件级改动
|文件|改前|改后与原因|
|---|---|---|
|task.md|泛过程要求、作者指导、60/40分|五段英文；四项可判定最终比较；实验事实不再冒充预测得分|
|submission_guide.md|过程/研究质量计分|最终结果100分，ID与原schema不变|
|scoring_rules/reference_conclusions|7个中间结果＋3大结论|四独立结果25/25/20/30；各自回答催化功能、D4控制、A/B变化、环大小关系|
|reference_key_points|中间结果独立分|scored=false保留证据，未要求作者步骤库存|
|evidence_map/qualification/task_definition|旧V2、旧已验收标记|增加逐规则最新原生映射，明确不继承PASS；纠正数值主表采用父级纯RRHO审计|
|verified_computation_reference/paper_route|历史与活动旧分说明|参考顶部加本版说明，历史保留；活动规则改V3|
|manifest|旧指纹|重算并通过加载|
|system.json/schema|分子身份、条件、观察已清楚|保留；无新结构/新提交合同|

## 来源阅读与输入核查
直接读正文PDF6–7页机理/图1，SI S55–64方法、Table S4/S5、NCI与构型/坐标，核对原有公开全量system.json。A=B1、B=B3、C=B2，不按B编号误换；C的四氟芳环保留para-H，B/C二氯均为ortho。D4/D5各为五/六元含一个氧的环，cis/trans是两个Ph相对面，不混绝对对映体。公开保留观察和条件，不给出FIA/HIA/TS值、作者机制与坐标。解释题的已知cis优势无需遮蔽。

## 最终规则
|rule_id|最终命题|权重|状态/复核|
|---|---|---:|---|
|r_catalyst_function|三催化剂分子行为与性能的有限联系|25|二态；须实际计算，不以单一酸性强行解释全部表现|
|r_d4_kinetic_control|D4形成偏cis而产物近简并，形成控制解释|25|二态|
|r_catalyst_selectivity_contrast|A/B改变D4辨别强度及稳健性|20|三态：真实计算及敏感性令0.088814级差反号/未决才review|
|r_ring_size_relationship|D5形成与稳定性同向cis，区别于D4|30|三态：有效低频/构象分析导致方向实质冲突才review|

保留B>A参考方向但不把近简并升格成稳健增强或强因果。四条不是旧FIA/HIA、六个TS/产品节点改名计分：这些是成立所需证据，最终评分回答不同关系。旧数字无硬窗，本次无新增/放宽；缺计算和错误定义直接fail，已成立等价解释pass。跨催化剂结果比较各自的cis/trans差，不相减不同总组成能量。

## 题面→原文SI→规则→原生证据→缺口
权威本地参考：`docs/verification/small_molecules_autonomous_research/job_followup_20261025T0135Z/parent_7a1d_audit/native_recomputed.json`，并读同目录audit.md/audit.json，核父级以现有Hessian独立重组纯RRHO的更正。所有下列为本地实算/后处理，不把论文值当重现值。

|必答输出|来源|规则|本地量|覆盖/缺口|
|---|---|---|---|---|
|催化剂行为与表现|正文筛选；SI S56 Table S4|r_catalyst_function|FIA A/B/C=467.227544/422.524396/409.296603；HIA=516.171498/476.465751/464.085838 kJ/mol|两亲和力排序同向；不是H2势垒/收率|
|D4形成与产品稳定性|正文图1，SI S61表S5|r_d4_kinetic_control|纯RRHO ΔGtrans-cis：TS A=1.967453、B=2.056267；产品−0.206072 kcal/mol|方向覆盖；不精确重现实验10/20|
|A/B辨别强度|SI S61，58–60作用分析|r_catalyst_selectivity_contrast|B−A=0.088814；来源1.391483|仅名义同向，噪声级强弱未稳健，保留review|
|环大小关系|SI S61–63及坐标|r_ring_size_relationship|D5 TS=4.389786、产品=5.517269；与D4成对对比|方向覆盖；D5产品幅度严重软模敏感|

## 方法与偏差
源SI S55要求气相优化、CPCM乙醚同几何单点、353.15 K理想气体RRHO；S64坐标标题又称CPCM优化，保留冲突。实际ORCA6.1.1相对源6.0.1，实验CPME而介质模型为乙醚。最新审计发现原输出实际默认QRRHO/100 cm⁻¹且1 cm⁻¹截止，已用现有原生Hessian重组全正频纯RRHO；旧候选QRRHO不能冒称RRHO，也不能挑最接近源数字者。

主值偏差：D4 A TS+1.279489、B TS−0.023180、D4产品+0.076100、D5 TS+0.314313、D5产品+2.918602 kcal/mol。D5 cis产品最低频0.514759064 cm⁻¹；全正频使该物种G降低4.327994，保留1 cm⁻¹截止则产物差1.189275，仅作敏感性，不能替代主值5.517269。来源印刷ratio指数符号与ΔGtrans−cis相冲突，不照抄错误符号。

六TS最后唯一虚频和B–H/C–H模式、四个产品无虚频均已有原生检查；立体投影仅身份检查，不冒充IRC。FIA/HIA为298.15 K焓，与353.15 K反应G分开；原子E口径加完整单原子5RT/2后所有亲和力同加6.197393 kJ/mol，排序不变。

## 验证与自检
没有新QC/HPC/ARCHE盲测。既有Hessian/日志、父级更正热项可复用；本轮未改后处理追值。上述A/B微弱增强及D5软模幅度需专家复核，不能称严格数值通过。JSON、manifest、包合同、V3及隔离加载均实际通过。父级重点：保持近简并措辞及review；不把产品稳定性和形成动力学互代。原生输出历史和失败记录完整保留。

父级复审补记：0.088814明确标为评价者的既有参考，不是agent必须知道或报告的值；agent评价依据为其自身实际A/B差和不确定性。

## 组末复审与实际文件补充

|文件|本次收尾修改|理由|
|---|---|---|
|evaluation/reference_qualification.json|当前verification_status明确V3_NOT_REASSESSED；旧验收状态保留historical_reference_status|杜绝从旧PASS/NUMERIC_REVIEW自动继承本版科学验收|
|evaluation/critical_failures.json|伪造与私有答案泄漏规则翻译为英文；普通错误仅影响相关结果|活动评分语言统一，未扩大invalid_submission触发|
|evaluation/research_contract.json / reproduction_protocol.json|明确私有历史来源记录角色、当前唯一V3评分入口；合同评分字段同步V3|来源方案/旧合同决定不能隐含增加过程或作者节点要求|
|package_manifest.json|根据最终内容再次重建|保证组末修订后的哈希和包内容一致|

收尾重复执行JSON解析、rubric/package校验和隔离V3加载，均通过；未启动量子化学、HPC或盲测。

逐文件与只读`v1_backup/paper_7a1d5d7c60a0ae04`比较，实际变化清单：`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/critical_failures.json`、`evaluation/evidence_map.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/reproduction_protocol.json`、`evaluation/research_contract.json`、`evaluation/scoring_rules.json`、`evaluation/task_definition.json`、`evaluation/verified_computation_reference.md`、`package_manifest.json`、`paper_route.md`。以上文件均已在文件变化表及本节说明原因。保持原样：`agent_input/data/inputs/system.json`、`agent_input/submission_schema.json`、`task_info.json`。历史`verified_computation_reference.md`原文逐字仍为本版文件后缀；实际运行的是临时`v3_autonomous_research`布局下的`TaskRepository.from_v3`。

</details>

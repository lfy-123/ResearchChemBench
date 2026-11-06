# 第一轮专家反馈调整 — 2026-11-03

采纳专家对现行解释任务的认可；暂不采用可选M/P盲预测升级，保留M观察与原四项评分。

专家明确认可解释任务，M/P盲预测属于可选建议。本轮保留现有解释版及公开M观察，避免在没有必要时再改变复杂金属体系的任务性质；不将“未采用可选升级”标为漏改。评分继续比较形成路线、有/无配体、立体竞争与局部活化阶段。

当前评分：螺烯并环的能量与分子解释 30分；指定配体相对于无配体模型促进底物活化 20分；计算的立体化学竞争解释观测 M 螺旋性 25分；立体化学选择与最大局部化学难度发生在不同阶段 25分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_7516a3cbacb70032 最终结论分项评分统一（2026-10-29）

逐条核对现有独立最终命题，保留其科学范围与权重，删除人工待定分及旧数值门槛政策。

螺烯并环的能量与分子解释 30分；指定配体相对于无配体模型促进底物活化 20分；计算的立体化学竞争解释观测 M 螺旋性 25分；立体化学选择与最大局部化学难度发生在不同阶段 25分。

旧→新规则数：4→4；仅保留独立终答，全部semantic/pass-fail，100分。科学范围不变；公开题面/输入/提交结构字节不变。

来源定位：正文 PDF 第 2、7–8 页与 Figure 7；SI S65–S67（方法、Figure S2、Table S10）以及 S101–S104 的结合态/产物结构。

逐项问题、独立性、来源与验证映射见[协调进度](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/最终结论分项评分统一_20261029/进度/organic19_a_paper_7516a3cbacb70032.json)及[完整审查报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_7516a3cbacb70032.md)。

修改文件及原因：

- `paper_route.md`：同步最终结论二态合同、引用或非评分历史证据边界。
- `package_manifest.json`：重建实际内容哈希。
- `evaluation/scoring_rules.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/conclusion_coverage_20261029.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_key_points.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/critical_failures.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/evidence_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_qualification.json`：同步最终结论二态合同、引用或非评分历史证据边界。

未运行新量化计算。验证参考SHA256保持`6621d6b2cd503a807f96ccf4fcc8b6ccbc0acf0ff112edf8090e726b78f14d86`，原始接受分类、数值差异和方法限制未升级。rubric/package/runtime加载及源/副本逐文件哈希校验通过。

当前专家事项：

1. **热化学温度与准谐口径。** 323.15 K 与 SI 热项吻合，但来源未直接给温度命令；影响四项能量解释，尤其 `r_ligand_promotion` 和 `r_helicity_explanation`。建议保留“根据指纹确定的相容实现”表述，评估其对局部差的充分性，不伪称作者参数逐字复现。
2. **结合态骨架与释放中性产物。** VI 的有机部分比释放产物多一个 H，尚无释放/再生动力学；影响 `r_formation_explanation` 的结论边界。建议认可已支持的骨架形成范围，同时要求声明终点身份；无需为本题额外补齐完整催化循环。
3. **立体选择与速率解释。** 单构象 M/P 差 1.712713 支持方向，最大局部势垒出现在后续 C–N 闭环；影响 `r_helicity_explanation`、`r_kinetic_distinction`。建议检查前体参照和立体映射，避免把分离 ee 当作双 TS 精确预测，或把有限局部比较当全局速率律。

当前材料未显示新的硬设计错误；上述是需要判断的证据与解释边界，不是自动整题失败。

---

## 2026-10-29之前的修改历史（非当前评分判据）

# paper_7516a3cbacb70032 修改说明

## 原问题、改后问题与类型
保留原题的Ir(III)催化指定底物/二苯乙炔合成螺烯、配体促进、M螺旋控制与化学难度。改后仍是解释题，82%收率、91% ee、M构型公开且不计“预测正确”。四个最终答案彼此对应：为何形成骨架、配体为何促进、为何选择M、选择与最难化学步骤是否重合。没有增加完全释放/再生或缩去无配体对照。

## 文件级修改
|文件|原状|修改及原因|
|---|---|---|
|task.md|长过程段、作者指导条件句、60/20/20分|五段英文边界、四个必答最终问题，去除旧过程分及论文依赖|
|submission_guide.md|研究质量信用及双模式文字|最终结果100分；原schema/ID合同保留|
|scoring_rules.json/reference_conclusions.json|6中间节点＋3总括结论|4独立最终结论30/20/25/25；不是CMD/插入/闭环完成度清单|
|reference_key_points.json|中间结果计分|保留为scored=false来源证据；作者标签不是隐藏要求|
|evidence_map.json/reference_qualification.json/task_definition.json|旧V2和历史PASS描述|新增当前逐规则原生映射、V3和未重新验收状态；保留原历史证据|
|paper_route.md/verified_computation_reference.md|活动旧分数与历史后处理|活动路线改V3，验证文档顶部说明复用，历史298 K记录保留|
|package_manifest.json|旧哈希|重建并通过合同/运行时加载|
|system.json/identities.json/submission_schema.json|准确身份与规范合同|不变，避免为了改编重造结构|

## 已知与待求、身份核对
已读正文PDF2、7、8页，SI S65–S67方法/图S2/表S10（并查看原图），S101–S104结合态坐标/晶体产物。底物N1-H、双苯乙炔、带tBu的Cp均保留；不是Cp*误替换。输入指定轴配体u·(v×w)>0，原生II、M/P TS和III的对应轴符号均为正；不能隐藏答案时删配体身份。已观察M不隐藏，因为要求计算解释而非盲猜。无作者坐标、路径、势垒进入公开资产。

## 最终规则
|规则|最终命题|权重|状态及复核原因|
|---|---|---:|---|
|r_formation_explanation|骨架形成的能量/分子原因|30|三态，仅有效替代路径的实质物理解释冲突|
|r_ligand_promotion|相对无配体模型促进活化|20|二态|
|r_helicity_explanation|计算竞争及分子作用解释M|25|三态，仅有效计算的不同立体决定阶段/作用冲突|
|r_kinetic_distinction|立体决定与最大局部势垒不在同阶段|25|二态|

不存在硬数字窗，旧16.4/18.1/22.5/11.9/25.6均为上下文而非新门槛。旧C–H/插入/C–N结构节点只作证据，不能凭其个数得分；第一条需要实际形成可行性的科学解释，不是三个节点打包清单。后面三条分别回答不同实验/计算关系，不重复授予“找到M TS”过程分。缺计算/错参照直接fail，已确立等价解释直接pass。

## 题面—原文SI—规则—本地量对应
原生审计：`docs/verification/small_molecules_autonomous_research/job_followup_20261024T1533Z/parent_ir7516_audit/audit.json`，读取其24个Freq/SP文件索引、热项/更正比较、产物图/轴身份检查，并抽读M TS的原生optfreq.log与solvent_sp.log（后者E=−4231.09414289 Eh，实际正常终止）。

|必答输出|来源位置|规则|本地证据而非来源回填|覆盖/缺口|
|---|---|---|---|---|
|骨架形成的物理解释|正文7–8，SI图S2、S101–104|r_formation_explanation|C26–C73、N55–C72成键模式和37重原子图；VI−IV=2.301997|覆盖结合态骨架；没有游离中性产品释放动力学|
|有/无配体促进|正文图7、SI S66/S67|r_ligand_promotion|16.428767 vs 22.455003；差−6.026236 kcal/mol|局部活化对照，不是不同组成总G直接相减|
|M选择性解释|正文图7b、SI S67|r_helicity_explanation|M/P=16.428767/18.141479；ΔΔG=1.712713|同轴配体与参照；单构象不能拟合91% ee|
|最难步骤与选择阶段|SI S66图S2、S67|r_kinetic_distinction|插入11.879554<CMD16.428767<消除25.596144|局部难度排序，不证明全局周转律|

## 方法差异、数值偏差和验证需求
真实Gaussian16频率/气相PBE0-D3(BJ)/6-31G(d,p)-SDD及大基组SMD DCM单点保留；GoodVibes3.2采用100 cm⁻¹、1 M、缩放1和qh-H＋qh-S。独立审计已纠正早期298.15 K仅准谐熵：当前323.15 K来自实验50°C与S67热项指纹，SI没有直接给计算温度，不应伪称作者命令。12个qh-G符合原表0.001 Eh打印精度，熵项最大偏差7.6131e−7 Eh。

本地M/P对源16.4/18.1偏+0.028767/+0.041479；无配体对22.5偏−0.044997；插入对11.9偏−0.020446；消除对25.6偏−0.003856。来源图14.1以III+为参照，不是IV局部插入势垒。VI仍含Ir和N–H，有机部分C35H23N2；晶体中性产物是C35H22N2，因此不声称已验证释放/去质子。III→IV换配体/炔的库存平衡已有，交换势垒/自由能未复现，不新增隐藏门槛。

本轮无新QM/HPC/盲测。已有同身份原生量足以映射四个有界命题；计算温度识别、配位交换和释放范围仍需专家判断，不能继承旧RESULTS_COMPLETE状态为V3满分。JSON、V3 rubric、manifest、validate_task_package、隔离TaskRepository加载均实际通过。父级重点复审第一条是否是物理解释而非作者节点清单，以及后三条的独立性。

## 组末复审与实际文件补充

|文件|本次收尾修改|理由|
|---|---|---|
|evaluation/reference_qualification.json|当前verification_status明确V3_NOT_REASSESSED；旧验收状态保留historical_reference_status|杜绝从旧PASS/NUMERIC_REVIEW自动继承本版科学验收|
|evaluation/critical_failures.json|伪造与私有答案泄漏规则翻译为英文；普通错误仅影响相关结果|活动评分语言统一，未扩大invalid_submission触发|
|evaluation/research_contract.json / reproduction_protocol.json|明确私有历史来源记录角色、当前唯一V3评分入口；合同评分字段同步V3|来源方案/旧合同决定不能隐含增加过程或作者节点要求|
|package_manifest.json|根据最终内容再次重建|保证组末修订后的哈希和包内容一致|

收尾重复执行JSON解析、rubric/package校验和隔离V3加载，均通过；未启动量子化学、HPC或盲测。

逐文件与只读`v1_backup/paper_7516a3cbacb70032`比较，实际变化清单：`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/critical_failures.json`、`evaluation/evidence_map.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/reproduction_protocol.json`、`evaluation/research_contract.json`、`evaluation/scoring_rules.json`、`evaluation/task_definition.json`、`evaluation/verified_computation_reference.md`、`package_manifest.json`、`paper_route.md`。以上文件均已在文件变化表及本节说明原因。保持原样：`agent_input/data/inputs/identities.json`、`agent_input/data/inputs/system.json`、`agent_input/submission_schema.json`、`task_info.json`。历史`verified_computation_reference.md`原文逐字仍为本版文件后缀；实际运行的是临时`v3_autonomous_research`布局下的`TaskRepository.from_v3`。

</details>

# 第一轮专家反馈调整 — 2026-11-03

保留两种产物族结构，移走优势产物/类比实验结果提示；根据共同起点总体势垒预测偏好，保持30/30/40。

论文Fig. 4和SI提供两个竞争产物族及其总体势垒，适合候选产物预测。现保留结构和热条件，移除公开实验优势及类比控制结果；第三项由解释已知偏好改为预测。论文正文/SI只供审查与评估，未放入agent_input。298.15 K比较与80℃操作仍分开。

当前评分：热双环形成的电子与活化解释 30分；竞争亚胺族的形成化学与活化 30分；根据计算预测两种给定产物族的动力学竞争 40分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_9f24eac60feca79d：2026-10-29 最终结论分项统一

现行分项：热双环形成的电子与活化解释30分；竞争亚胺族的形成化学与活化30分；双环与亚胺产物族的动力学竞争40分。合计100分，全部semantic/conclusion，逐项pass/fail；无数值匹配门槛或need_review。

旧→新：4项→3项。原数值规则：r_overall_cycloaddition_barrier、r_overall_imine_barrier；原数值仅留历史证据。

科学范围未变：task.md、全部agent_input/data、guide和submission_schema均保持原字节。原要求的能量、位点、产物、比较与解释仍完整保留；量化结果作为结论证据，取消作者目标值和容差评分。构象、描述符、作者节点、计算次数及完成流程没有独立奖励。已存在不同终答框架保留，未为统一条数人为拆分。

## 科学要求—规则—独立性—来源—已有验证

|公开科学要求|规则|独立性|正文/SI|已存验证支持与缺口|
|---|---|---|---|---|
|必需结果1与3：双环整体活化、连接及电子/成键解释|r_cycloaddition_formation|回答双环如何热形成，不借亚胺相对高低作为充分判据。|正文PDF7–8 Fig.4a；SI PDF23–26，方法及Supplementary Fig.3–5|OSS路线整体31.012403；闭环28.343667、必要转动19.026830均更低；CSS受限解有R→U不稳定。 主要边界：破缺对称态的自旋污染与受限CSS波函数不稳定必须按实际物理状态解释。|
|必需结果2：同参照亚胺族整体活化及形成连接|r_imine_formation|回答亚胺如何形成及所需活化，可独立于双环机理解释成立。|正文PDF7–8 Fig.4a；SI PDF23–26，方法及Supplementary Fig.3–5|闭壳层trans-imine 37.092612，two-sided TS8连接；cis39.969492和stepwise40.918456为有限候选。 主要边界：破缺对称态的自旋污染与受限CSS波函数不稳定必须按实际物理状态解释。|
|必需结果4：两产物族动力学竞争及实验解释边界|r_product_competition_interpretation|比较两族的竞争及观察意义，不再次奖励单条路径或绝对势垒数字。|正文PDF7–8 Fig.4a；SI PDF23–26，方法及Supplementary Fig.3–5|同参照imine−cycloaddition=6.080209 kcal/mol支持双环动力学优势；不是80°C精确收率。 主要边界：破缺对称态的自旋污染与受限CSS波函数不稳定必须按实际物理状态解释。|

## 文件与理由

scoring_rules更新逐项判据/二态政策；reference_conclusions与supporting key points同步；原key points完整置于明确非评分历史记录；evidence_map及覆盖/资格文档更新现行映射，保留来源证据及历史接受分类；paper_route区分现行评分和历史路线；package_manifest重建。验证参考文件逐字不改。同步审查页完整中文规则与原始JSON，以及审查任务副本。

## 保留专家事项

- 破缺对称态的自旋污染与受限CSS波函数不稳定必须按实际物理状态解释。
- 已有作者引导有限候选和连接审计不等于盲发现或全局穷尽；保留方法/实现差别。
- 孤立烯胺暗对照为N-(4-氯苯基)类似物；不能定量移用到给定N-苯基模型。

没有新QM/HPC或盲测，合同和运行时通过不等于科学满分；已知参考缺陷另记objective_issue_flags，不恢复人工待定得分。

## 2026-10-27及以前历史修改说明（评分政策已由上文替代）

下列记录保留原数值、方法、偏差及旧设计历史；旧窗口和need_review不是当前评分要求。

# paper_9f24eac60feca79d 修改说明

## 科学问题与改编理由
原题已明确要求“quantify comparable overall free-energy barriers from the supplied starting state”，因此两整体势垒是独立最终交付，保持31.0±2.0与37.1±2.0 kcal/mol硬窗。原V2五项中电子态/连接独立过程分被取消；新V3四项为两最终势垒、热反应的物理机制解释、产物竞争解释。不是把每个作者节点重命名为最终结论。

## 文件变化与公开边界
|文件|之前|现在及原因|
|---|---|---|
|agent_input/task.md|简短问题/体系/提交|五段清晰英文；四个结果、整体势垒定义、原子映射命名空间、实验与比较温度区别|
|problem_definition.json|有main/SI页码source_locators|仅把定位移到私有evidence_map；分子、实验事实、条件原样保留|
|submission_guide.md|科学/过程双轴乘积分|仅最终结果100分；移除公开目标论文/SI访问措辞|
|scoring_rules/reference_conclusions|2 numeric中间项＋电子态/连接中间项＋竞争|四个独立最终规则25/25/25/25；原数值窗完全不变|
|reference_key_points|节点清单可参与评分|全部scored=false的来源证据，不要求作者节点数量或标签|
|evidence_map/reference_qualification|源与旧RESULTS_REPRODUCED|新增逐项原生映射，明确本版未重新验收；旧strict_numeric_whole_pass只留历史|
|paper_route|仍写TS2/TS8端点缺失、pending|依据最新10-25T1206Z审计修正历史状态；不继承V3 PASS|
|verified_computation_reference|完整历史验证记录|只前置本版作用域说明，原内容保持|
|package_manifest|旧哈希|重建并实际校验|
|SMILES/schema|完整正确公开分子与合同|保留，没有强加作者路线和软件|

仍为解释型问题：保留热条件下双环产物类观察，但不给OSS、aza-Claisen、作者TS/中间体或31/37.1数值。两产物仅给完整中性连接。公开起始E构型保留，各结构atom-map命名空间独立，不能假定同号跨分子对应。RDKit逐一核对普通/映射SMILES去map后同图、C23H19F2N、45原子、0电荷；182电子。没有把4-Cl控制实验误当N-phenyl精确动力学。

## 直接阅读与规则
正文PDF7–8/Figure3–4，SI PDF23–26=印刷S22–S25（方法、补充图3–5），并渲染检查正文p8图4的结构/能图。图4b/c和图5的另一底物/oxa体系不纳入本题。

|rule|最终答案|权重|状态|
|---|---|---:|---|
|r_overall_cycloaddition_barrier|全底物同一起始零点的双环整体ΔG‡|25|二态；原31.0±2.0，闭区间[29,33]|
|r_overall_imine_barrier|同条件最低受支持亚胺整体ΔG‡|25|二态；原37.1±2.0，闭区间[35.1,39.1]|
|r_thermal_mechanism_explanation|热成环的电子态/成键物理解释|25|三态；仅有效物理证据有实质未决机制冲突可review|
|r_product_competition_interpretation|由实际竞争能量解释双环动力学优势|25|二态；定性与绝对值独立判断，派生6.1不再得数值分|

规则恰一结论一规则，总100，无过程分。缺原生计算/错参照/无连接/硬窗失败直接fail。等价物理解释直接pass；不把作者路线、精确自旋值或私有历史诊断作为提交必答内容。热解释与竞争解释不同：前者解释热[2+2]为何可行及电子机制，后者用两类实际路线说明哪个产物族更易形成。

## 题目→来源→规则→原生证据→缺口
最新入口：`docs/verification/small_molecules_autonomous_research/job_followup_20261025T1206Z/old_9f24/parent_9f24_audit/audit.json`；同时读取相邻`native_return.json`、`verification_matrix.json`及10-24T1924Z原生重析、10-25T0135Z闭环端点审计。抽读新转动鞍点freq/低层stable/高层stable实际Gaussian日志，核对0/1、45原子、负频率、G修正、SCF和稳定性文字。

|题面|来源位置|规则|已有本地结果|覆盖/限制|
|---|---|---|---|---|
|双环整体势垒|main7–8图4a、SI S22–S25|r_overall_cycloaddition_barrier|31.012402997；闭环28.343666749、pucker19.910706、新转动19.026829816均低于控制高度|初始→双自由基→构象→主闭环→正确产物已连接；有限候选，不是全局穷尽|
|亚胺整体势垒|main7–8、SI S24–S25|r_overall_imine_barrier|TS8 37.092612120、双向端点；cis39.969492/stepwise40.918456更高|最低已调查路线覆盖；不声称所有可能路径|
|电子机制|main7、SI S23–S25|r_thermal_mechanism_explanation|OSS稳定/自旋与键模；受限CSS38.733078762存在R→U不稳定；triplet50.848579881；转动模投影重叠0.993076|BS污染明确，CSS只约束面比较；无自旋纯净/精确多参考保证|
|竞争解释|main7–8图4a|r_product_competition_interpretation|同参照差6.080209123，正确两产物连接及同条件|支持双环动力学优势，非80°C精确产率|

## 数值与方法差异
本地−作者：31.012402997−31.0=+0.012402997；37.092612120−37.1=−0.007387880；均满足原±2.0，但不由历史通过自动授予本版分。闭环28.343667−28.3=+0.043667，受限CSS38.733079−38.7=+0.033079，triplet50.848580−50.9=−0.051420；这些无新增硬窗。新转动19.026830没有匹配作者数字，不制造误差。

同报告物理模型UM06-2X/def2-TZVP/SMD(toluene)//UM06-2X/def2-SVP/SMD(toluene)，全45原子0电荷。原生298.15 K、1 atm纯RRHO热项；1M共同平移在单分子相对势垒抵消，绝对G需注明省略该平移。无QRRHO/截频/缩放/自旋投影。UltraFine、SCF Tight/XQC/MaxCycle512、NoSymm是实际控制，来源未逐项指定。新转动Gcorr0.311554Eh、自身高层E−1142.241274756652Eh、G−1141.929720756652Eh，对Int1−1141.96004194Eh得19.026829816。

新转动唯一负频率−17.6271cm⁻¹，经全Hessian去刚体投影−17.6271356和转动模重叠0.993076确认是实在内转；不能任设更大虚频阈值否定。S²约1.0397，湮灭后0.3262，不能叫自旋纯单重态。ZIP TS5对应正文TS4，避免被SI/文件编号误导。

## 验证边界与自查
本轮没有新QM/HPC/ARCHE。最新版原生记录补齐旧转动缺口，可复用各命题证据；不要求重新盲搜或多余IRC，也不把旧RESULTS_REPRODUCED变成本版PASS。当前科学验收标志归未重新评估，历史两窗通过独立存储。全部JSON可解析，rubric精确字段、一结论一规则、100分、硬窗、manifest、validate_task_package和隔离TaskRepository.from_v3加载通过。父级可重点复核两个最终数值与热机制/竞争解释的独立性，以及软转动频率与受限CSS的边界。

## 组末复审与实际文件补充

|文件|本次收尾修改|理由|
|---|---|---|
|evaluation/reference_qualification.json|当前verification_status明确V3_NOT_REASSESSED；旧验收状态保留historical_reference_status|杜绝从旧PASS/NUMERIC_REVIEW自动继承本版科学验收|
|evaluation/critical_failures.json|伪造与私有答案泄漏规则翻译为英文；普通错误仅影响相关结果|活动评分语言统一，未扩大invalid_submission触发|
|evaluation/current_scope_status.json / reference_validation_plan.md|旧scientific_pass归入历史；当前四项ID和未重新验收状态；计划顶部划分历史记录|避免第二处状态入口继续把旧五项或历史PASS作为本版验收|
|package_manifest.json|根据最终内容再次重建|保证组末修订后的哈希和包内容一致|

收尾重复执行JSON解析、rubric/package校验和隔离V3加载，均通过；未启动量子化学、HPC或盲测。

逐文件与只读`v1_backup/paper_9f24eac60feca79d`比较，实际变化清单：`agent_input/data/inputs/problem_definition.json`、`agent_input/submission_guide.md`、`agent_input/task.md`、`evaluation/critical_failures.json`、`evaluation/current_scope_status.json`、`evaluation/evidence_map.json`、`evaluation/reference_conclusions.json`、`evaluation/reference_key_points.json`、`evaluation/reference_qualification.json`、`evaluation/reference_validation_plan.md`、`evaluation/scoring_rules.json`、`evaluation/verified_computation_reference.md`、`package_manifest.json`、`paper_route.md`。以上文件均已在文件变化表及本节说明原因。保持原样：`agent_input/data/inputs/int1.smi`、`agent_input/submission_schema.json`、`task_info.json`。历史`verified_computation_reference.md`原文逐字仍为本版文件后缀；实际运行的是临时`v3_autonomous_research`布局下的`TaskRepository.from_v3`。

</details>

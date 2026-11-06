# paper_cf8ce1fc0fbcd300：甲氧基环丙烯区域选择性与异构体重分配

**当前状态确认（2026-10-23）：用户接受本篇当前科学问题的验证结果，数值差异保留专家审查。** 要求相关结果已实际计算且结论一致；本确认不等于所有数值窗口通过、全文复现或自动发布。下方差值、方法差异和原始证据继续保留。

更新：2026-10-23。当前自主科研科学问题登记为`PROVISIONAL_PASS_QUALITATIVE`，即定性一致暂定验收；不是整题严格数值复现，也不是专家已批准发布。本页对应现行科学分V2私有规则。

## 1. 科学问题和范围

### 科学目标

在二氯甲烷中酸促进的甲醇对((1-(二氟甲基)-2-苯基环丙-2-烯-1-基)氧基)二甲基(苯基)硅烷的官能团化过程中，什么控制甲氧基环丙烯的区域选择性生成及所观察到的区域异构体重分配？产物形成选择性与产物相对稳定性有什么关系？

为这一小分子均相有机反应建立并检验有证据支持的解释。共同讨论形成偏好与产物相对稳定性，而不是仅报告一个结构、能量或描述性特征。已提供观察到的产物身份；预测新产物身份或对映体结果不是目标。

### 公开输入和科学边界

使用`data/inputs/system.json`获取明确分子图的身份、条件和观察。其输入ID在各任务视图之间保持稳定。

- `PI1`和`PI2`定义苯乙炔、二氟乙酰基硅烷以及实验分离得到的酸处理阶段底物`siloxy_start`。光驱动制备是该底物的背景，不是额外研究目标。
- `PI3`指定制备及后续甲醇/TMSCl条件。目标阶段使用甲醇和5 mol% TMSCl，在二氯甲烷中于室温进行。
- `PI4`定义`methoxy_major`及其观察到的分离收率和区域选择性。
- `PI5`定义`methoxy_minor`和`methoxy_comparator`、其克级观察背景，以及次要产物在五分钟内向主要产物的转化。未观察到不等于浓度严格为零，终点也不等于时间历程。

保持相同分子图，并区分实验背景。未指定绝对立体化学。将结论限于酸/甲醇阶段和这三种区域异构体；不要额外要求计算光驱动前体形成、其他底物、其他亲核试剂或下游反应。选择并论证与你的研究有关的化学状态、环境表示和物理效应。给定身份和终点观察不能确立机理；任何公开的作者模型都是需要执行并批判性评估的基线，而不是定论证据。

### 必需的研究

提出与给定现象有关的可检验解释，并执行自行选择的、有信息价值的计算研究。解释所选模型和检验为何能够区分相关可能性。利用实际执行的证据保留、修订或否定解释；文献叙述、未执行方案或缺乏支持的一致结论均不充分。

评估产物形成偏好，比较所提供的全部三种甲氧基区域异构体的相对稳定性，并评估这些发现与所观察到的选择性以及次要向主要产物重分配之间的关系。不要将有利的终产物等同于其形成路径已经得到证明。不要求穷尽路径网络、穷尽构象、特定描述符或特定搜索方法。即使尝试进行的研究使某项比较仍未解决，这些科学比较仍是必需内容。

验证取决于实际提出的主张。过渡态主张需要适当的驻点表征以及反应物/产物连接性验证。热力学或能量比较需要一致的对象/状态定义、单位、条件和已记录的近似。动力学模型需要方程、与观察的联系和可辨识性评估。不要从不足以确立相应结论的证据中声称得到绝对速率、完全平衡或已解决的机理。

如果公开提供作者科学指导，则执行并批判性评估公开的基线，在研究记录和可读报告中记录遵循情况、歧义和合理替代处理。如果未提供，则独立选择方法；未公开的作者方法或假设不属于要求。无论哪种情况，得分都由证据和科学判断决定。

### 交付物和停止条件

遵循`submission_guide.md`和未改变的`submission_schema.json`。提交`report/results.json`、`report/report.md`和`research/`。使用稳定ID关联假设、研究、证据和结论。将实际输入、输出、日志和分析代码保存在`research/`下，并为每个被引用的产物建立索引。说明模型局限性、不确定性、未解决的比较和实际资源使用。记录失败工作的尝试输入和错误日志；不要编造缺失输出。

研究完成与问题解决相互独立。当已执行证据支持在此范围内所声称的结论，并已说明不确定性时停止，或报告诚实的部分工作或执行失败及其证据。谨慎的无定论工作可以获得研究质量分，但不确立问题已解决。不设置固定CPU、GPU、内存、运行时间或作业数量配额。

共享评估在100分中分配60分给研究质量，40分给科学问题解决。它奖励能够提供信息的解释和检验、可靠执行、证据驱动的决策以及有依据的结论。仅有一致结论并不充分，有支持的替代解释不会因偏离作者解释而受罚。依赖方法的数值结果按照其定义和局限性评估，而不依据未公开的精确能量目标。

## 2. 输入、交付与来源索引

- [公开英文完整任务指令](../tasks/autonomous_research/paper_cf8ce1fc0fbcd300/agent_input/task.md)。
- [分子身份、条件及观察](../tasks/autonomous_research/paper_cf8ce1fc0fbcd300/agent_input/data/inputs/system.json)。
- [提交指南](../tasks/autonomous_research/paper_cf8ce1fc0fbcd300/agent_input/submission_guide.md)。
- [提交schema](../tasks/autonomous_research/paper_cf8ce1fc0fbcd300/agent_input/submission_schema.json)。

第1节是当前公开题面的完整中文直译；没有把本轮评分修订混入译文。仅`agent_input/`属于被评Agent公开输入，本文、验证路线与evaluator属于私有审查资料。

- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/main.pdf)：PDF页序（从1开始）7,8。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/supplementary_001.pdf)：PDF页序（从1开始）54,55,58。
- [supplementary_002.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/supplementary_002.pdf)：PDF页序（从1开始）43,44,47。

## 3. 计算验证、论文对照与误差

### 方法、模型和执行步骤

正文PDF第7–8页Figure 4A；SI1 PDF第54–55页计算方法/Figure S9及第58页软件；SI2对应第43–44和47页。

M06-2X/6-311+G(d,p)/SMD-DCM优化/频率与作者明确层级一致。实际Gaussian16 C.01，SI引用A.03；原坐标未提供，依据分子图/图S9重建。实际298.15 K、1 atm RRHO，来源温压、网格及热化学约定未完整报告。

|项目|作者信息|实际验证|一致性及限制|
|---|---|---|---|
|方法与溶剂|M06-2X/6-311+G(d,p)、SMD-DCM|同层级优化/频率|主要泛函、基组、连续介质一致|
|软件和结构|Gaussian16 A.03；未提供全坐标|Gaussian16 C.01；按分子图/Figure S9重建|修订版不同，几何不是直接拷贝源坐标|
|模型与状态|环丙烯鎓/甲醇竞争进攻及中性产物|三个+1单重态25原子TS、三个中性24原子最低点|中性产物各66正频率，TS唯一目标C–O反应虚频；最终无种子距离约束|
|热项与连接|未完整报告温压/网格/所有热化学约定|298.15 K、1 atm RRHO；分子图与振型连接核验|没有完整松弛IRC；相对TS比较不是绝对势垒|

1. 独立构建三个中性甲氧基异构体并优化/频率，各24原子、66个正频率，分子连接图与题面一致。
2. 按作者环丙烯鎓/甲醇模型构建三个+1单重态进攻TS，各25原子、唯一反应虚频；最终种子距离约束已解除。
3. 独立核验C–O反应振型及分子图，对同组成TS比较相对G，再单独比较中性产物G；两组零点不混用。没有把三个TS相对高度称为绝对活化势垒。

### 论文值、计算值与差值

差值为计算−论文；各物理量、参照及单位单独列明。正文与SI冲突时并列保留，不用验证值替换来源目标。

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|TS1′−TS1|1.3|1.583206|+0.283206|kcal/mol|
|TS1″−TS1|7.1|6.618970|−0.481030|kcal/mol|
|minor−major产物G|3.2|2.845755|−0.354245|kcal/mol|
|comparator−major产物G|7.2|7.161766|−0.038234|kcal/mol|
|TS1成键C–O距离|1.910|1.866986|−0.043014|Å|
|TS1最短OH···F接触|2.390|2.287419|−0.102581|Å|

### 定性结论逐项核对

|来源结论/问题|计算支持|验收边界|
|---|---|---|
|major形成优先|TS1最低，其他两TS相对为1.583206、6.618970|与来源0/1.3/7.1排序一致|
|major最稳定，minor其次|产物相对0/2.845755/7.161766|与来源0/3.2/7.2排序一致|
|minor→major存在热力学驱动|G下降2.845755 kcal/mol|方向一致；不证明完整平衡和精确速率|
|近接结构的解释范围|C–O和OH···F距离差分别−0.043014、−0.102581 Å|不是独立氢键因果能量分解|

形成通道与产物稳定性均支持major优先；minor到major自由能下降，支持观察到的重分配方向。全部相对能排序一致，最大绝对能差0.481030 kcal/mol。

### 方法偏离、未报告项及专家裁定

- 软件修订版、结构重建及未报告热化学细节限制精确数值复现，不表示存在既定数值门槛失败。
- 反应模式和分子图提供局部连接证据，未完成松弛IRC或完整酸交换网络。
- OH···F近接不等于氢键因果能量分解；五分钟端点不证明完全平衡，未检出不等于严格零浓度。
- 原文上游照光时长和SI部分重分配实验文字存在不一致，不能混为同一条件的定量动力学。

四个相对能差均小于0.5 kcal/mol，未设统一作者误差窗，正式登记仍为定性验收。专家可判断相对能与重建结构是否足以支撑当前解释，不应额外要求未在任务中定义的全酸交换网络。

### 原始证据入口

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/acceptance_audit.md)。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/acceptance_audit.json)。
- [independent_native_checks.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/independent_native_checks.json)。
- [父级正式登记](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/parent_acceptance_decision.json)。
- [随包验证计算参考](../tasks/autonomous_research/paper_cf8ce1fc0fbcd300/evaluation/verified_computation_reference.md)。

- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/main.pdf)：PDF页序（从1开始）7,8。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/supplementary_001.pdf)：PDF页序（从1开始）54,55,58。
- [supplementary_002.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/supplementary_002.pdf)：PDF页序（从1开始）43,44,47。

## 4. 逐项评分

### 通用科学要求（现行原文）

只评价公开任务范围内的科学结果。每个叶子项满足全部条件得满分，否则为0，不即兴按比例给分。中间发现与最终解释独立评价；最终项要求明确采用且有计算支持的综合结论，不能仅列出候选。先核分子连接、原子库存、电荷/自旋、物理量、单位、参照、温度、溶剂与标准态。结果须有可定位的实际计算及原生产物支持；题面给定观察、复制论文数字、正常退出或正确措辞本身不能得分。最低点、过渡态及连接的证据要求以实际主张为准，允许科学等价的连接检验和计算方法；不强制复刻验证者软件、搜索轨迹、构象数量或全IRC。普通失败及缺失只影响对应项，不清零独立有效结果；伪造或隐藏答案泄漏按有效性规则处理。不奖励过程、调用数、效率、资源投入或失败诊断。定量项按固定目标和包含边界的绝对容差判断，Judge不得临时调整；定量不通过不自动否定独立定性项，定性方向不能代替定量命中。无容差的上下文数字不是额外门槛。真实物理不可比且无法澄清时需复核。所有规则仅在evaluator侧，不向agent泄漏作者机理或数值。 本批为解释/比较型题目，全部采用定性科学结果项。来源数值保留为可比性上下文，没有新设精确能量窗口；不使用验证值替换作者值。合理替代模型或路径可按相同科学命题的证据评价，不能仅因未选作者软件、描述符或机理标签扣分。

总分100；中间关键节点50分、最终结论50分。下方直接列出规则文件现行中文原文；规则为定性科学命题，作者数值是上下文，无隐藏数值硬窗口。

### 1. competing_addition_channels — 15分（中间关键节点）

**评分项：** 三个位置的C–O生成通道物理可比

**完整规则（r_competing_addition_channels）：** 实际结构和反应证据支持甲醇参与的三个候选C–O成键通道，分别映射到major、minor、comparator连接。作者相同环丙烯鎓/甲醇的三个TS为参考；可接受同一科学比较的等价状态表示。若声称TS，须为目标成键振型及适当连接证据；不能仅给三产物能量替代形成通道。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 2. major_vs_minor_formation — 10分（中间关键节点）

**评分项：** major形成通道低于minor通道

**完整规则（r_major_vs_minor_formation）：** 在同组成、同电荷及相容零点下的实际计算支持major形成通道相对minor更有利。作者TS1′−TS1=1.3 kcal/mol为上下文；排序必须正确，数字相近或实验major产率高本身不能代替竞争证据。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 3. major_vs_comparator_formation — 10分（中间关键节点）

**评分项：** major形成通道低于比较异构体通道

**完整规则（r_major_vs_comparator_formation）：** 实际可比计算支持通向major的形成通道低于comparator通道。作者TS1″−TS1=7.1 kcal/mol仅作上下文，不能把该相对TS差称绝对势垒；不要求精确数值。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 4. major_vs_minor_stability — 10分（中间关键节点）

**评分项：** major中性产物比minor稳定

**完整规则（r_major_vs_minor_stability）：** 三个指定产物中，实际有效极小点及相容G比较支持major低于minor。作者minor−major=3.2 kcal/mol为参考；必须比较相同组成和物理量，不能以带电加成态替代中性产物。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 5. minor_vs_comparator_stability — 5分（中间关键节点）

**评分项：** minor中性产物比comparator稳定

**完整规则（r_minor_vs_comparator_stability）：** 实际中性产物G比较支持minor低于comparator，从而与major最低共同形成major<minor<comparator排序。作者相对major为3.2/7.2 kcal/mol是上下文；无计算或排序相反不计分。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 6. selectivity_answer — 30分（最终结论）

**评分项：** 最终：形成竞争与稳定性共同支持主要异构体

**完整规则（r_selectivity_answer）：** 最终综合实际形成通道比较和中性产物稳定性，说明major在所研究模型中更容易形成且更稳定，将这一双重依据用于解释给定区域选择性；区分comparator形成/稳定性不利与严格零产率。未独立分解的氢键/位阻因果不作为强制答案，也不得从产物低能单独推导路线。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 7. redistribution_answer — 20分（最终结论）

**评分项：** 最终：minor到major重分配具有热力学驱动

**完整规则（r_redistribution_answer）：** 最终用实际产物G下降解释minor向major重分配的方向，并区分重新分配的热力学驱动与初始生成竞争。仅有五分钟91%端点不能证明完全平衡或唯一速率；给出有计算支持的方向性解释即可，不要求未有来源的全酸交换网络。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI, V2_SI_2`。

### 提交有效性规则（现行原文）

**fabricated_evidence：伪造计算执行或数值证据。**

触发条件：有明确证据确认伪造计算执行、日志或结果，或将复制的私有参考值冒称独立实算；普通误判、收敛失败或缺失本身不等于伪造。

判定：确认伪造时按invalid_submission处理，提交无效；诚实失败只使受影响科学项失分，其他独立有效项保留。

**hidden_answer_leakage：将未公开的答案或私有参考冒充独立发现。**

触发条件：确认提交依赖未经公开提供的evaluator答案或隐藏原生参考，并冒称自主计算结果。

判定：确认未经授权使用隐藏答案时按invalid_submission处理；公开PR指导本身不构成泄漏。物种/单位错误、普通缺项只影响对应项，不自动全题清零。

## 5. 版本变化、任务范围与待审问题

要求三个区域异构体的形成竞争、产物稳定性及minor→major重分配解释。基本覆盖酸/甲醇阶段的主要DFT问题；上游光驱动底物制备和全篇其他反应不属于任务。

本次仅将维护副本的评分从旧研究质量/问题解决双轴迁移为100分科学结果。删除活动过程评分、过程权重及过程奖励；中间关键节点是分子连接、电子/构象特征或可比竞争结果，不是工具调用、假设条数、计算次数或日志完整度。最终结论分要求将实际结果用于回答科学问题，不能只有候选结构或未经计算的合理叙述。

公开题面、分子数据、提交schema、task_info.json及paper_route.md按迁移指南逐字节保持。因而题面仍出现旧“研究质量分”或“60/40”表述，部分题面还有条件性的“作者指导”措辞；第1节如实翻译，不能悄悄改写成新题面。这些是待专家确认的文字遗留，不代表现行V2仍有过程分。实际运行采用私有V2规则。

本批当前科学问题是解释/比较型，没有新增数值命中要求；不将来源每个数值机械设分，也不根据实际偏差扩大容差。未沿作者路线本身不扣分，按科学命题和可比证据评定；本次验证可以使用作者坐标与模型，不等于被评Agent信息受限的盲测。当前可进入评分，发布审批及较大误差裁定仍待专家。

四个相对能差均小于0.5 kcal/mol，未设统一作者误差窗，正式登记仍为定性验收。专家可判断相对能与重建结构是否足以支撑当前解释，不应额外要求未在任务中定义的全酸交换网络。

## 6. 科学权重、来源与验证证据映射

|评分ID|权重|类型|设置理由|来源定位（PDF页序）|实际验证对应|
|---|---|---|---|---|---|
|competing_addition_channels|15|中间|先建立形成比较确实对应三条反应，避免以终产物稳定性冒充路径。|正文7–8，Figure 4A；SI1 54–55/Figure S9（SI2 43–44）|三个同组成+1单重态25原子TS，唯一C–O反应虚频及图映射|
|major_vs_minor_formation|10|中间|主要/次要产物的核心形成竞争。|同上，Figure S9的三竞争TS|minor相关TS−major相关TS=1.583206|
|major_vs_comparator_formation|10|中间|说明未观察比较产物的形成不利性，独立于minor比较。|同上，Figure S9的三竞争TS|comparator相关TS−major相关TS=6.618970|
|major_vs_minor_stability|10|中间|直接关联minor→major重分配的热力学方向。|同上，Figure S9中性产物|三个24原子有效极小点；minor−major=2.845755|
|minor_vs_comparator_stability|5|中间|补全第三异构体的稳定性位置，权重低于直接重分配差。|同上，Figure S9中性产物|comparator−major=7.161766，minor−major=2.845755|
|selectivity_answer|30|最终|这是任务最主要的跨过程综合解释，权重最高。|正文7–8，Figure 4A；两套SI对应Figure S9|TS和中性产物的独立排序均major优先；没有只用终产物推路径|
|redistribution_answer|20|最终|单独回答题目的重分配现象，不能以初始选择性答案代替。|正文7–8，重分配观察；SI Figure S9|minor→major自由能下降2.845755；不把5分钟终点当完全平衡|

正文PDF第7–8页Figure 4A；SI1 PDF第54–55页计算方法/Figure S9及第58页软件；SI2对应第43–44和47页。 每项活动来源文件、SHA-256和页序由`evaluation/evidence_map.json`的`V2_*`记录给出；源引用保留在私有研究合同和复现协议中。最终规则所依赖的中间项见`reference_conclusions.json`。

## 7. 副本一致性与维护记录

源题目：`tasks/small_molecules_autonomous_research/autonomous_research/paper_cf8ce1fc0fbcd300`；V2维护源：`tasks/small_molecules_verified_autonomous_research/paper_cf8ce1fc0fbcd300`。专家副本与V2维护源逐文件一致，包内manifest已重算。源AR/PR的验证参考同步既有计算事实，源评分规则未被覆盖；本次新增的是AR维护副本，未新增历史PR副本。

迁移前后的公开材料和身份文件SHA-256、旧evaluator备份及计算引用保存在[维护记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/science_v2_onboarding_20261023/migration_record.json)。详细误差另见[统一数值与方法核对](../数值误差与计算方法及定性结论核对.md)。

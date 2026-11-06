# paper_f2a9e1bc87fc9b54：硝基吡咯N-炔丙基化的两步连接与能量解释

**当前状态确认（2026-10-23）：用户接受本篇当前科学问题的验证结果，数值差异保留专家审查。** 要求相关结果已实际计算且结论一致；本确认不等于所有数值窗口通过、全文复现或自动发布。下方差值、方法差异和原始证据继续保留。

更新：2026-10-23。当前自主科研科学问题登记为`PROVISIONAL_PASS_QUALITATIVE`，即定性一致暂定验收；不是整题严格数值复现，也不是专家已批准发布。本页对应现行科学分V2私有规则。

## 1. 科学问题和范围

### 科学目标

对于DMF中碱促进的3-硝基-1H-吡咯与炔丙基溴的N-烷基化，什么计算得到的化学行为最能描述N-炔丙基-3-硝基吡咯的形成？哪些计算得到的能量和结构特征支持这一描述？

研究指定起始体系转化为所述观察产物的完整过程。为该转化建立化学上连贯的解释，并评估其能量和结构支持：什么解释产物形成，证据将能量上的困难定位在哪里，以及对于产物生成的净趋势可以得出什么结论？产物身份已给定；分子路线未给定。

### 公开输入和科学边界

使用`data/inputs/system.json`作为权威起始事实：

- PI1（身份）：3-硝基-1H-吡咯是N-烷基化反应的吡咯底物。
- PI2（身份）：炔丙基溴是用于形成N-炔丙基-3-硝基吡咯的烷基化试剂。
- PI3（身份）：产物为N-炔丙基-3-硝基吡咯，也称为3-硝基-1-(丙-2-炔-1-基)-1H-吡咯。
- PI4（条件）：反应使用氢化钠，在N,N-二甲基甲酰胺中于室温进行24 h。
- PI5（观察）：分离产物为淡黄色晶体，收率89%，并通过NMR、IR和LC-MS表征。

产物和分离观察标明的是需要解释的现象，而非基元机理。分离收率和反应时间不是速率常数，也不是基元势垒的直接量度。研究限于所述碱和溶剂中该底物与烷基化试剂的分子有机转化。其他合成转化、催化体系和生物应用不属于本问题。选择并论证对所述体系的适当表示；未规定初始几何结构。

### 必需的研究

为完整转化提出可检验的解释，并选择能够区分、支持或约束它们的模型与计算研究。从科学问题出发决定哪些内容值得研究；不要求固定数量的假设、检验、结构或路线。仅有熟悉的反应类型标签不构成计算解释。

实际执行所选研究。保留所构建的分子输入、模型设置、原始输出、执行日志和所有分析代码。解释证据如何使你保留、修订或否定解释。在连通解释中说明起始底物、碱和烷基化试剂的化学作用，并描述得到支持的连接变化。提供与整个转化有关的能量和结构证据，而非与所提解释无关的孤立计算。

声明对模型和解释有影响的假设，包括适用时的物种和电荷记账、溶剂表示和能量参考。定义数值量、单位、条件以及所有已知或未知的校正约定。区分活化相关的困难和总体热力学趋势，并将计算结果、给定观察与解释分开。不要从分离观察推断定量确立的反应速率。

验证要求取决于你提出的主张。声称得到过渡态，需要适当的频率和连接性证据；明确标明未经验证的候选结构。用适合相应主张的检查支持其他结构或能量主张。不要伪造不可获得的输出或验证。不要求穷尽路径或构象，也不要求采用特定搜索方法。

如果提供作者科学指导，则执行并科学评估公开的基线，在研究记录和可读报告中记录方案遵循情况、歧义及合理替代处理。如果没有提供此类指导，则独立选择研究方法；未公开的作者方法或解释不属于要求。

### 交付物和停止条件

- `report/results.json`：符合`submission_schema.json`的记录，使用稳定的假设、研究、证据和结论ID，并关联实际产物。
- `report/report.md`：对化学问题、所选解释和模型、已执行工作、有支持的连通结论、不确定性、局限性和实际资源使用的可读说明。
- `research/`：检查和复现所提交工作所需的实际分子输入、原始输出、日志和分析代码。

严格遵循`submission_guide.md`与共享schema。研究完成与问题解决相互独立：按照指南定义，使用`research_status`报告complete、partial或execution_failed工作，使用`question_status`报告resolved、partially_resolved或unresolved结论。没有所关联执行证据的状态标签或看似合理的解释，不能确立问题已解决。

当证据支持所声称结论的范围且剩余不确定性已经说明时停止；或者，在如实记录的尝试遇到使问题仍未解决的限制时停止。不设置固定CPU、GPU、内存、运行时间或作业数量配额。以实际输入和日志作记录时，部分工作、无定论结论及真实执行失败可以接受；不要声称已经解决尚未解决的机理。

评估分配60分给研究质量，40分给有证据支持的连通化学解释及其能量/结构支持的解决情况。仅与作者结果一致并不充分。有充分支持的替代结论有资格获得相同分数；诚实的未解决工作可以获得研究质量分，但不会自动获得问题解决分。任何可选的作者描述符或未公开路线均不是得分要求。

## 2. 输入、交付与来源索引

- [公开英文完整任务指令](../tasks/autonomous_research/paper_f2a9e1bc87fc9b54/agent_input/task.md)。
- [分子身份、条件及观察](../tasks/autonomous_research/paper_f2a9e1bc87fc9b54/agent_input/data/inputs/system.json)。
- [提交指南](../tasks/autonomous_research/paper_f2a9e1bc87fc9b54/agent_input/submission_guide.md)。
- [提交schema](../tasks/autonomous_research/paper_f2a9e1bc87fc9b54/agent_input/submission_schema.json)。

第1节是当前公开题面的完整中文直译；没有把本轮评分修订混入译文。仅`agent_input/`属于被评Agent公开输入，本文、验证路线与evaluator属于私有审查资料。

- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_f2a9e1bc87fc9b54/documents/main.pdf)：PDF页序（从1开始）2,3。
- [supplementary_001.docx](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_f2a9e1bc87fc9b54/documents/supplementary_001.docx)：DOCX：Theoretical study、Table 1、Cartesian coordinates。

## 3. 计算验证、论文对照与误差

### 方法、模型和执行步骤

正文PDF第2–3页Figure 1及方法；补充DOCX的Theoretical study、Table 1、TS1/TS2/H2/炔丙基溴坐标。DOCX没有固定PDF页码。

B3LYP/6-31+G(d)/SMD-DMF与作者一致；实际Gaussian16 C.01替代来源Gaussian09。实际298.15 K、1 atm RRHO，作者完整热化学约定未报告。来源无Na显式模型，按−1单重态离子及中性H2/炔丙基溴配平。

|项目|作者信息|实际验证|一致性及限制|
|---|---|---|---|
|方法与溶剂|B3LYP/6-31+G(d)、SMD-DMF；Gaussian09|相同泛函、基组、连续介质；Gaussian16 C.01|主要层级一致，软件代际不同|
|结构/电荷|SI给出TS1/TS2和分子坐标，未显式包含Na|源TS重优化/频率；−1单重态反应模型，独立H2和炔丙基溴|保留源简化模型；没有加入Na聚集、固体NaH或全溶剂壳|
|连接核验|两步机理及中间体/产物|有效IRC片段加自由优化端点；118秒任务承接80步前代并真正收敛|不是把短时任务结束当成功，也不是所有失败IRC都变为成功|
|热化学参照|图式TS1/S2/TS2/净产物相对G，温压细节未全报|298.15 K、1 atm RRHO；完整原子、电荷与两物种账本|图式S2→TS2与实际连接前体的局部势垒有不同定义|

1. 直接使用SI TS1（13原子）和TS2（18原子）坐标，重新优化/频率；分别得到正确N–H/H–H转移和N–C形成/C–Br断裂的唯一虚频。
2. 从有效IRC片段继续自由优化，核验初始接触态、S2/H2接触态、TS2前体和产物/Br接触态。118秒恢复作业继承原80步优化末几何并真正收敛，失败前代保留。
3. 独立计算H2和炔丙基溴并统一配平所有状态的原子、总电荷和两物种账本；构建图式相对能与实际已连接前体的局部势垒，不能混用参考。

### 论文值、计算值与差值

差值为计算−论文；各物理量、参照及单位单独列明。正文与SI冲突时并列保留，不用验证值替换来源目标。

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|TS1相对初态|−1.6|−1.603604|−0.003604|kcal/mol|
|S2相对初态|−25.5|−27.303811|−1.803811|kcal/mol|
|TS2相对初态|−9.3|−9.270657|+0.029343|kcal/mol|
|净产物形成G|−45.5|−45.655915|−0.155915|kcal/mol|
|图示S2→TS2能差|16.2|18.033154|+1.833154|kcal/mol|
|TS2−实际连接前体|未单列|15.082209|不作错配相减|kcal/mol|

### 定性结论逐项核对

|来源结论/问题|计算支持|验收边界|
|---|---|---|
|去质子化形成H2后进行N取代|两个正确反应虚频及有效端点，N–C成键/C–Br断裂|两步连接和正确产物支持|
|净生成放能|−45.655915，对−45.5 kcal/mol|方向一致|
|后续取代比初始去质子化有更明显局部困难|图式S2→TS2=18.033154；连接前体局部15.082209|支持困难定位；两数不可替代|
|TS1相对自由能略负|−1.603604，对−1.6|图式数值接近，不等于实验严格零势垒|

两步分子转化、正确N-炔丙基产物连接以及净放能得到支持；后续取代相对去质子化具有更明显局部活化需求。TS1相对自由能略负不能解释为实验严格零势垒。

### 方法偏离、未报告项及专家裁定

- Gaussian版本、未报告热化学约定及电荷/自旋重建不同或不明，不能声称全部作者设置逐项一致。
- 旧前向IRC失败保留，连接使用有效片段加真正极小点；S2后续Hessian位移诊断例外及低频RRHO敏感性披露。
- 图式S2→TS2=18.033154与真实前体局部高度15.082209不同，前者包含接触伙伴交换的热力学影响。
- 没有计算Na聚集/固体NaH、接触交换动力学、精确速率产率或全文分子对接；均不是本题必要范围。

主要审查S2与派生能差约1.8 kcal/mol残差、低频热项及实际前体参照。15.082209与作者16.2不能作为同一定义直接计算误差；版本差异不能被当作全部残差的已证实原因。

### 原始证据入口

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/acceptance_audit.md)。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/acceptance_audit.json)。
- [native_recheck.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/native_recheck.json)。
- [父级正式登记](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/parent_acceptance_decision.json)。
- [随包验证计算参考](../tasks/autonomous_research/paper_f2a9e1bc87fc9b54/evaluation/verified_computation_reference.md)。

- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_f2a9e1bc87fc9b54/documents/main.pdf)：PDF页序（从1开始）2,3。
- [supplementary_001.docx](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_f2a9e1bc87fc9b54/documents/supplementary_001.docx)：DOCX：Theoretical study、Table 1、Cartesian coordinates。

## 4. 逐项评分

### 通用科学要求（现行原文）

只评价公开任务范围内的科学结果。每个叶子项满足全部条件得满分，否则为0，不即兴按比例给分。中间发现与最终解释独立评价；最终项要求明确采用且有计算支持的综合结论，不能仅列出候选。先核分子连接、原子库存、电荷/自旋、物理量、单位、参照、温度、溶剂与标准态。结果须有可定位的实际计算及原生产物支持；题面给定观察、复制论文数字、正常退出或正确措辞本身不能得分。最低点、过渡态及连接的证据要求以实际主张为准，允许科学等价的连接检验和计算方法；不强制复刻验证者软件、搜索轨迹、构象数量或全IRC。普通失败及缺失只影响对应项，不清零独立有效结果；伪造或隐藏答案泄漏按有效性规则处理。不奖励过程、调用数、效率、资源投入或失败诊断。定量项按固定目标和包含边界的绝对容差判断，Judge不得临时调整；定量不通过不自动否定独立定性项，定性方向不能代替定量命中。无容差的上下文数字不是额外门槛。真实物理不可比且无法澄清时需复核。所有规则仅在evaluator侧，不向agent泄漏作者机理或数值。 本批为解释/比较型题目，全部采用定性科学结果项。来源数值保留为可比性上下文，没有新设精确能量窗口；不使用验证值替换作者值。合理替代模型或路径可按相同科学命题的证据评价，不能仅因未选作者软件、描述符或机理标签扣分。

总分100；中间关键节点60分、最终结论40分。下方直接列出规则文件现行中文原文；规则为定性科学命题，作者数值是上下文，无隐藏数值硬窗口。

### 1. base_hydrogen_transfer — 15分（中间关键节点）

**评分项：** 碱诱导N–H转移并形成H2

**完整规则（r_base_hydrogen_transfer）：** 实际结构和反应连接证据支持3-硝基吡咯N–H被碱作用去除并形成H2，保持β-硝基吡咯身份及原子/电荷配平。作者氢负离子接触模型TS1为参考；允许化学等价表示，不强制源坐标或固定搜索方法。仅写去质子化标签或给出未验证TS不计分。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI`。

### 2. activated_n_intermediate — 15分（中间关键节点）

**评分项：** 去质子化含氮中间态与后续反应相连

**完整规则（r_activated_n_intermediate）：** 有效计算支持去质子化吡咯含氮态及相应稳定化，并与后续炔丙基化前体保持同一阴离子骨架映射。作者S2/H2接触态相对初态约−25.5 kcal/mol为上下文；不强制同一接触伙伴/构象。需得到实际中间态及连接关系，不能把两个互不配平的模型拼接。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI`。

### 3. n_c_bond_formation — 20分（中间关键节点）

**评分项：** N–C形成与C–Br断裂的取代事件

**完整规则（r_n_c_bond_formation）：** 实际反应结构、振型及适当连接证据支持吡咯N与炔丙基碳成键、C–Br断裂，并保留末端炔和β-硝基位置。作者TS2的SN2通道为参考；不规定必须采用作者标签或完整IRC，但只算一个非反应虚频或错位产物不得分。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI`。

### 4. net_exergonicity — 10分（中间关键节点）

**评分项：** 配平的净产物形成具有放能趋势

**完整规则（r_net_exergonicity）：** 由相容能量定义和完整物料/电荷账本计算得到净N-炔丙基产物形成的显著放能趋势。作者G约−45.5 kcal/mol为参考上下文，不设隐藏精确窗口；不得遗漏H2/试剂/Br或从产率直接推导ΔG。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI`。

### 5. connected_route_answer — 20分（最终结论）

**评分项：** 最终：两步分子解释完整N-炔丙基化

**完整规则（r_connected_route_answer）：** 最终采用有计算支持的连接解释，将底物、碱、烷基化试剂的作用贯通到正确N-炔丙基产物。作者去质子化后取代为参考；实证支持的等价路线可接受。不能只展示孤立TS/产物或提出未经检验的反应类型。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI`。

### 6. energetic_answer — 20分（最终结论）

**评分项：** 最终：区分局部取代困难与总体放能

**完整规则（r_energetic_answer）：** 结合已连接路径和可比能量，明确后续N–C取代具有比前面近反应物去质子化更明显的局部活化需求，而净转化放能。正确区分图式相对高度、各自前体局部势垒和反应ΔG；作者16.2仅是其参考定义下的能差。不把负TS相对G称实验严格无势垒，不从89%/24h推出定量速率。

**证据判定（现行原文）：** 核对实际分子/电子态、参照、单位与可定位的原生执行证据；仅评价本项科学命题。满足全部条件得满分，否则0；不临时给比例分，不奖励过程。

**交付物绑定：** `report/results.json, report/report.md`；字段`$`。来源证据：`V2_MAIN, V2_SI`。

### 提交有效性规则（现行原文）

**fabricated_evidence：伪造计算执行或数值证据。**

触发条件：有明确证据确认伪造计算执行、日志或结果，或将复制的私有参考值冒称独立实算；普通误判、收敛失败或缺失本身不等于伪造。

判定：确认伪造时按invalid_submission处理，提交无效；诚实失败只使受影响科学项失分，其他独立有效项保留。

**hidden_answer_leakage：将未公开的答案或私有参考冒充独立发现。**

触发条件：确认提交依赖未经公开提供的evaluator答案或隐藏原生参考，并冒称自主计算结果。

判定：确认未经授权使用隐藏答案时按invalid_submission处理；公开PR指导本身不构成泄漏。物种/单位错误、普通缺项只影响对应项，不自动全题清零。

## 5. 版本变化、任务范围与待审问题

要求完整的两步N-炔丙基化分子解释、结构连接及局部活化/净放能关系。覆盖该合成反应的完整DFT小节；全文还包含其他合成、分子对接或生物应用，均未扩大为任务范围。

本次仅将维护副本的评分从旧研究质量/问题解决双轴迁移为100分科学结果。删除活动过程评分、过程权重及过程奖励；中间关键节点是分子连接、电子/构象特征或可比竞争结果，不是工具调用、假设条数、计算次数或日志完整度。最终结论分要求将实际结果用于回答科学问题，不能只有候选结构或未经计算的合理叙述。

公开题面、分子数据、提交schema、task_info.json及paper_route.md按迁移指南逐字节保持。因而题面仍出现旧“研究质量分”或“60/40”表述，部分题面还有条件性的“作者指导”措辞；第1节如实翻译，不能悄悄改写成新题面。这些是待专家确认的文字遗留，不代表现行V2仍有过程分。实际运行采用私有V2规则。

本批当前科学问题是解释/比较型，没有新增数值命中要求；不将来源每个数值机械设分，也不根据实际偏差扩大容差。未沿作者路线本身不扣分，按科学命题和可比证据评定；本次验证可以使用作者坐标与模型，不等于被评Agent信息受限的盲测。当前可进入评分，发布审批及较大误差裁定仍待专家。

主要审查S2与派生能差约1.8 kcal/mol残差、低频热项及实际前体参照。15.082209与作者16.2不能作为同一定义直接计算误差；版本差异不能被当作全部残差的已证实原因。

## 6. 科学权重、来源与验证证据映射

|评分ID|权重|类型|设置理由|来源定位（PDF页序）|实际验证对应|
|---|---|---|---|---|---|
|base_hydrogen_transfer|15|中间|明确碱的化学作用，是完整转化的第一步。|正文2–3，Figure 1；SI DOCX TS1坐标|13原子TS1唯一N–H/H–H反应虚频；有效两侧端点|
|activated_n_intermediate|15|中间|将第一步产物与第二步反应物接起来，防止两个孤立计算冒充完整路线。|正文2–3，Figure 1；SI DOCX Table 1|S2/H2接触态与后续阴离子骨架映射；S2相对−27.303811|
|n_c_bond_formation|20|中间|形成目标键的关键转化，给予中间项最高权重。|正文2–3，Figure 1；SI DOCX TS2坐标|18原子TS2唯一N–C/C–Br反应虚频；连接前体和产物有效|
|net_exergonicity|10|中间|提供与局部活化难度不同的总体热力学结果。|正文2–3，Figure 1；SI DOCX Table 1|H2/炔丙基溴及Br完整账本；净产物−45.655915|
|connected_route_answer|20|最终|这是当前科学问题的完整结构与路线回答。|正文2–3，Figure 1；SI DOCX Theoretical study|两个反应事件及匹配中间骨架共同连接到N-炔丙基产物|
|energetic_answer|20|最终|要求由能量结果得到物理上正确的综合解释，避免把放能当无活化障碍。|正文2–3，Figure 1；SI DOCX Table 1|源式能差18.033154、真实前体局部15.082209及净放能；参考态不同|

正文PDF第2–3页Figure 1及方法；补充DOCX的Theoretical study、Table 1、TS1/TS2/H2/炔丙基溴坐标。DOCX没有固定PDF页码。 每项活动来源文件、SHA-256和页序由`evaluation/evidence_map.json`的`V2_*`记录给出；源引用保留在私有研究合同和复现协议中。最终规则所依赖的中间项见`reference_conclusions.json`。

## 7. 副本一致性与维护记录

源题目：`tasks/small_molecules_autonomous_research/autonomous_research/paper_f2a9e1bc87fc9b54`；V2维护源：`tasks/small_molecules_verified_autonomous_research/paper_f2a9e1bc87fc9b54`。专家副本与V2维护源逐文件一致，包内manifest已重算。源AR/PR的验证参考同步既有计算事实，源评分规则未被覆盖；本次新增的是AR维护副本，未新增历史PR副本。

迁移前后的公开材料和身份文件SHA-256、旧evaluator备份及计算引用保存在[维护记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/science_v2_onboarding_20261023/migration_record.json)。详细误差另见[统一数值与方法核对](../数值误差与计算方法及定性结论核对.md)。

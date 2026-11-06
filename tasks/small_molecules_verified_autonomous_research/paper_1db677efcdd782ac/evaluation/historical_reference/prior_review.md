# paper_1db677efcdd782ac：N-环丙基四氢吡啶的光氧化、环命运与同位素解释

更新：2026-10-24。当前必要结果完整且经独立验收，状态`RESULTS_COMPLETE_NUMERIC_REVIEW`；数值与发布待专家。现行评分为科学分V2，未宣称严格数值全一致。

## 1. 科学问题和范围

### 科学目标

指定的N-环丙基四氢吡啶的分子反应性，如何同时解释其依赖光照的氧化、依赖取代基和立体化学的环丙烷断裂与保留、cis/trans相互转化，以及底物氘进入醛的现象，同时与所列相关四氢吡啶氧化对照体系保持一致？

为这一相互关联的氧化问题建立有证据支持的分子解释，而不只是给出一个孤立的能量或复述观察到的产物。

### 公开输入和科学边界

使用`data/inputs/system.json`。它给出了S_H、S_Mcis、S_Mtrans和S_Ptrans的确切起始身份与相对立体化学、S_HD4的同位素标记位置、相关T_H/T_Ph/T_Pyr对照结构、反应条件和定性观察。分子由其连接图定义，而不是由所提供的优化几何结构定义。仅指定环丙烷的相对立体化学。

相互关联的科学范围包括对照体系背景下的分子氧化可达性、取代与立体化学对断裂和保留的影响、观察到的甲基底物相互转化，以及与同位素相容的醛和完整环产物解释。S_Mtrans是一个对照结构，不是独立测得的以trans起始的产物分布的来源。产物醛的烯烃立体化学和精确的同位素比例不是预测目标。

这是计算研究；不要求开展新的实验室实验。有氧观察和黄素再生提供背景，但完整的光物理、氧/过氧化物、黄素周转或酶机理不在必需范围内。同样，不要求定量的溶液速率/产率模型或唯一的氢转移动力学路径。不要悄然引入缺失的实验参数，也不要把对照体系的行为当作另一分子的实测氧化电位。说明任何额外的建模假设及其能够支持的结论。

### 必需的研究

提出可检验的分子解释，并选择能区分或评估这些解释的模型和有信息价值的计算研究。由你决定哪些状态、物理效应、结构和比较是重要的。实际执行所选择的研究，并保留真实输入、输出、日志和分析代码。记录每项研究的目的、方法、结果和基于证据的下一步决定。根据所得证据支持的内容保留、修订或否定解释。不要求固定数量的假设、计算、构象或路径。

一并处理相互关联的科学目的：氧化/光依赖性的对照一致性；指定取代基和甲基立体异构体之间断裂/保留反应性的比较，包括与苯基保环产物的相容性；甲基cis/trans相互转化；以及底物标签进入醛的现象。只有一个描述符，或只有一个能量而未解释这些关系，均不充分。无需使用任何特定描述符、中间体、路径、电子结构方法或搜索程序。

验证要求取决于你的主张。声称的过渡态需要适当的频率和反应连接验证；声称的极小值需要适当的驻点和身份检查。如果使用动力学模型，提供其方程、与现有观察的映射以及可辨识性评估。这些主张和模型并非必需。区分分子能量比较、动力学可达性、观察到的产物量和所提出的解释；没有证据时不要由其中一项推断另一项。只比较有明确映射的对象、状态、能量约定、单位和条件。

当作者提供的科学指导被公开提供时，执行并批判性评估该公开基线，在研究记录和可读报告中记录方案遵循情况、歧义和有依据的替代处理。当没有提供时，自行选择方法：未公开的作者方法、描述符和假设并非要求，未采用它们不扣分。在任何一种视图中，仅与参考一致都不充分；实际证据与科学判断是必需的。

### 交付物和停止条件

严格按照`submission_schema.json`和`submission_guide.md`的定义提交`report/results.json`、`report/report.md`和`research/`。包含真实产物以及相互关联的假设、研究、证据、结论、局限性和可复现性信息。可读报告应解释整合的科学解释、哪些比较得到支持、哪些仍不确定、任何失败尝试以及实际资源使用情况。遵循指南中的稳定ID和产物链接要求。

研究完成与科学问题解决不同。根据证据而非愿望，将`research_status`设为`complete`、`partial`或`execution_failed`，并将`question_status`设为`resolved`、`partially_resolved`或`unresolved`。有尝试过的输入和日志时，诚实的部分执行或执行失败可以接受；完成的研究仍可能使问题未得到解决。缺乏支持或未执行的机理不是已解决的答案。

当实际证据支持你在所声明的建模边界内提出的结论，且剩余不确定性已明确说明时停止。不设置固定的CPU、GPU、内存、运行时间或作业数量配额，也不要求穷尽构象或路径网络。

共享评估为研究质量分配60分，为科学问题解决分配40分。在问题解决部分，氧化/光依赖性的对照一致性占8分，断裂/保留的比较及产物相容性占18分，甲基立体化学相互转化占10分，与同位素相容的氢来源占4分。有充分支持的替代解释可以获得评分；未解决的方面不会自动获得问题解决分。可选的作者描述符、谱学方案和条件化解释没有单独分值。

## 2. 输入、交付与来源索引

- [公开英文完整题面](../tasks/autonomous_research/paper_1db677efcdd782ac/agent_input/task.md)。
- [分子身份、同位素位置、条件与观察](../tasks/autonomous_research/paper_1db677efcdd782ac/agent_input/data/inputs/system.json)。
- [提交指南](../tasks/autonomous_research/paper_1db677efcdd782ac/agent_input/submission_guide.md)及[提交schema](../tasks/autonomous_research/paper_1db677efcdd782ac/agent_input/submission_schema.json)。
- [现行评分规则](../tasks/autonomous_research/paper_1db677efcdd782ac/evaluation/scoring_rules.json)、[计算参考](../tasks/autonomous_research/paper_1db677efcdd782ac/evaluation/verified_computation_reference.md)、[评分资格](../tasks/autonomous_research/paper_1db677efcdd782ac/evaluation/reference_qualification.json)。

第1节完整逐句翻译当前公开task.md，保留其末尾旧60/40过程评分措辞。该公开文件依授权逐字节不改；**现行私有V2不奖励过程**，以第4节14条科学结果为准。提交记录用于定位科学证据，不独立产生过程分。仅agent_input/属于被评Agent公开输入。

- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_1db677efcdd782ac/documents/main.pdf)；SHA-256 `87f3ee6f0a2d91661c86f5937db71f365551c03332b3cb934032d4e07cd63bce`。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_1db677efcdd782ac/documents/supplementary_001.pdf)；SHA-256 `30fe1abda1628ed1ed4b9c678bd9422c52ba9bcc63d506a2efbe43f596fb1652`。

当前科学验收为`RESULTS_COMPLETE_NUMERIC_REVIEW`：所需结果与条件化结论完整，允许按现行科学分V2逐项评分；不是严格数值复现或专家批准发布。全部数值均为既有实际计算的复核与重组，本轮未新增QC/HPC。来源数字、验证数字和评分条件分开保留，未用验证值替换作者目标。

正文PDF从1计数：3页Table 1；4–5页氧化/光照与同位素说明；6页Table 2/Fig.7；7页Table 3/Fig.8–9；8页Fig.10–11；9页保环与异构化解释；10页计算方法，对应印刷页1373–1380。SI的PDF页码与S页码相同；42页是**Figure S36**，不是SI第36页；43页氧化能量，44–48页比较物结构，49–51页环能量，52–66页H/Me结构，67–68页Ph开环结构。

## 3. 真实计算过程、作者对照与误差

### 作者方法、实际模型和可比性

|项目|作者来源|实际验证|边界|
|---|---|---|---|
|氧化比较对象|T_H/MeTHP、T_Ph/MPTP、T_Pyr/MMTP s-cis与s-trans，中性/自由基阳离子；Table 1、SI S43–48|8态，中性0/单重态与阳离子+1/双重态，来源分子图不变|MMTP的s-cis/trans是吡咯取向，不是环丙基cis/trans；不得把它们的电位赋予S_H等底物|
|氧化比较方法|M06-2X/6-31G(d)优化、M06-2X/cc-pVTZ或CAM-B3LYP/def2-TZVP单点；Table 1归Gaussian09|Gaussian16；M06-2X/6-31G(d)优化频率，M06-2X/cc-pVTZ同几何单点，Ultrafine、SCF(XQC,maxcycle=200)、NoSymm|未复算CAM列；实现不同不等于源参数完全复刻|
|H/Me环状态|M06-2X/cc-pVDZ优化、M06-2X/def2-TZVP单点；Table 3归Spartan'24|Gaussian16 UM06-2X同名基组组合；15态=5条闭环/TS/开环分支；+1/双重态|H B1及Me B1/B2；H B2未追加为强制配额|
|环优化和频率|作者极小值0虚频、TS1个相关虚频|Opt maxcycles=50；TS opt=(ts,calcfc,noeigentest,maxcycles=35)；实际检查全部收敛、振型与结构|NoEigenTest输入选项不替代最终实际频率检查；不把正常退出当完整科学验收|
|Ph剖面|Fig.9 M06-2X/cc-pVDZ，C1′–C2′距离2.3→1.5 Å；SI S67–68开环结构|两分支各5点；UM06-2X/cc-pVDZ、Opt(ModRedundant,maxcycles=60)，实际原生编号25–27|剖面是低层电子能，不用高层环态单点或自由能冒充；不是完整DET轨迹|
|溶剂/环境|实验CD3CN、微量水、3MLF光照；分子计算未显式包含溶剂、反离子、黄素、O2或酶|实际输入同为气相孤立分子；无额外色散/隐式溶剂|不是实验溶液自由能或绝对氧化电位；不假定未报告的温度、水含量和标准态|
|能量与换算|Table 3给E(TS)−E(闭环)及E(开环)−E(闭环)，未逐字明确电子能、ZPE或热修正|本次高层SCF电子能差；627.5094740631 kcal mol⁻¹/Eh、27211.386245988 mV/Eh|不得再次声称作者明确指定electronic-only；频率用于驻点资格，未把RRHO热项加进本次数值|
|H/D产品连接|Fig.7/8/11；SI Fig.S36；作者未区分唯一分子内/间HAT|执行RDKit元素/同位素/电荷及映射边检查，连接既有开环分子结果|原子后处理支持相容性，不等于新算水解/HAT势垒；50:50谱模拟不是必达比例|

### 实际执行与独立核验步骤

1. 从SI结构建立H B1与甲基B1/B2的闭环、开环和TS，按分子图、+1/双重态及环面关系核验；优化/频率后在相同最终几何上作高层单点。独立审查直接重读15环态与8氧化态共46条Opt/Freq/SP日志，23态全部正常结束，实际优化完成点的四项收敛标准均通过，频率数为3N−6，高层几何与优化几何一致。
2. 检验5个TS的唯一虚频及目标环C–C断裂投影。H B1原IRC曾有corrector失败；仅复用已接受路径片段并从两侧作无约束端点优化，分别连接正确闭环/开环零虚频极小值。不是原IRC完整成功；不把未做全部甲基IRC作为新门槛。
3. 以共同元素/电荷平衡式`X + T_H•+ → X•+ + T_H`重组氧化比较，以每条闭环为局部零点重组开环能/势垒，以trans-Me B2闭环为共同零点核验立体稳定性。由真实几何确认cis同面、trans异面。
4. 两个Ph开环分支作有限缩环剖面。最早合并value/action的Gaussian扫描语法只做了自由优化，该失败保留；修正后的扫描实际包含全部十个约束点，各自四项标准通过，2.3→1.5 Å单调升能。已有两个Ph开环最低点的正常Opt/Freq/SP另作支路种子；不因缺少封闭极小值而虚构其能量。
5. 执行H/D两条亚胺鎓水解映射的元素、同位素、电荷守恒检查，并与公开S_HD4的N邻位C2/C6标记及醛末端D位置对应；将底物供氢、另一底物保环氧化和公开混合醛观察整合为条件化产品解释。

独立复算记录23态不包含Ph两种子与额外端点；它们分别在剖面/端点审计中记录，避免把证据数量误称为总计算次数。频率阶段使用新Hessian重新打印的预测位移个别不是四个YES，不改变此前已接受优化的四项收敛事实，也不等于所有新预测位移满足阈值。

### 环开环能与势垒：逐项数值及来源冲突

以下均为kcal/mol，差=本次−来源。每条的局部参照是同分支闭环态。SI绝对能直接相减是透明算术列，**不据此宣布作者热修正约定已确认或纠正打印值**。

|分支/物理量|主文Table 3|SI打印相对值|SI绝对能直接差|本次高层电子能差|差−主文|差−SI打印|差−SI绝对能直接差|
|---|---:|---:|---:|---:|---:|---:|---:|
|H_B1 势垒|5.8|5.8|5.810110|5.599310|-0.200690|-0.200690|-0.210800|
|H_B1 开环能|3.2|3.2|3.160138|2.842782|-0.357218|-0.357218|-0.317356|
|Mcis_B1 势垒|2.5|2.5|2.533883|1.172122|-1.327878|-1.327878|-1.361761|
|Mcis_B1 开环能|-0.4|-0.4|-0.247866|-1.151254|-0.751254|-0.751254|-0.903388|
|Mtrans_B1 势垒|3.2|3.2|3.220379|3.162395|-0.037605|-0.037605|-0.057984|
|Mtrans_B1 开环能|1.8|1.8|1.793422|1.794746|-0.005254|-0.005254|+0.001324|
|Mcis_B2 势垒|1.5|1.5|1.508533|1.454172|-0.045828|-0.045828|-0.054361|
|Mcis_B2 开环能|-2.5|-0.8|-0.798192|-0.788065|+1.711935|+0.011935|+0.010127|
|Mtrans_B2 势垒|3.7|3.7|3.793922|3.748114|+0.048114|+0.048114|-0.045808|
|Mtrans_B2 开环能|2.1|2.1|2.119727|2.068057|-0.031943|-0.031943|-0.051670|

cis-Me B2同为M06-2X/def2-TZVP//M06-2X/cc-pVDZ命名下闭环→开环：主文−2.5，SI−0.8；SI绝对能−637.420566→−637.421838 Eh给−0.798192；实际−637.420293886→−637.421549747 Eh给−0.788065。没有证据表明主文/SI有意使用不同模型或零点。SI CAM3-B3LYP同行也有−2.5，仅为来源线索，不据此认定抄列错误或以CAM结果替换M06目标。

cis-Me B1主文势垒2.5而实际1.172122，差−1.327878；实际B1低于B2（1.454172），主文B1高于B2（1.5），细排序反转。两条cis分支仍低于trans及H，且主M06模型内开环符号不变。闭环/TS相对来源全原子RMSD约0.476996/0.471703 Å，不能把全部残差归为舍入。

其它来源边界：SI cis-Me B2低层M06-2X/cc-pVDZ打印+0.04，但绝对能−637.250344→−637.250409 Eh相减为−0.040788；SI cis-Me B1高层开环能打印−0.4，而绝对能差为−0.247866。来源打印相对值与绝对能未处处严格一致。CAM3-B3LYP下trans-Me开环能为负，主M06列为正，说明方法依赖不能用宽容差抹去。H B2作者6.6/+3.3保留为背景，此次未将它新增为必要计算或独立评分项。

### 氧化比较与相对电子转移

下表相对T_H；mV/e只是同一电子转移能差换算，负值表示相对于T_H更易氧化。不是溶液中电极参照的绝对电位。

|对照|Table 1 M06/mV|SI S43绝对能换算/mV|本次/mV|差−Table 1/mV|差−SI/mV|本次/kcal mol⁻¹|
|---|---:|---:|---:|---:|---:|---:|
|MPTP|-79|-81.960695|-84.301119|-5.301119|-2.340424|-1.944030|
|MMTP_cis|-551|-565.860777|-565.278481|-14.278481|+0.582296|-13.035631|
|MMTP_trans|-612|-625.747596|-625.383616|-13.383616|+0.363980|-14.421689|

|气相绝热电子电离能/kcal mol⁻¹|SI绝对能差|本次|差|
|---|---:|---:|---:|
|MeTHP|177.858211|177.878184|+0.019974|
|MPTP|175.968152|175.934154|-0.033998|
|MMTP_cis|164.809151|164.842553|+0.033402|
|MMTP_trans|163.428128|163.456495|+0.028367|

T_Pyr比T_Ph易氧化约0.48–0.54 V，T_Ph与T_H仅约0.084 V；方向及大小层级符合作者解释。作者另列CAM数值−570/−622/−94 mV和区域电荷/自旋描述符；此轮未追加这些可选辅助分析。3MLF激发态较强氧化能力来自来源背景（正文4页三重态2.1 V、单重态2.6 V、基态0.04 V），不是本次新计算，也不直接与气相比较值拼成溶液反应自由能。

### 甲基共同零点与Ph有限剖面

甲基共同零点为trans-Me B2闭环；SI列来自其打印绝对能直接相减，单位kcal/mol，不与各自局部开环能混用。

|状态|SI绝对能共同零点值|本次共同零点值|差|
|---|---:|---:|---:|
|S_Mcis_B1_closed|1.216741|1.976868|+0.760127|
|S_Mcis_B1_open|0.968875|0.825614|-0.143260|
|S_Mtrans_B1_closed|0.057731|0.068559|+0.010828|
|S_Mtrans_B1_open|1.851153|1.863305|+0.012152|
|S_Mcis_B2_closed|2.590987|2.641309|+0.050322|
|S_Mcis_B2_open|1.792795|1.853244|+0.060450|
|S_Mtrans_B2_closed|0.000000|0.000000|+0.000000|
|S_Mtrans_B2_open|2.119727|2.068057|-0.051670|

两类trans闭环都低于全部已比较cis闭环和开环态。作者没有独立cis→trans TS/势垒，实际也未新算该势垒；相容稳定性解释不是定量异构化速率或平衡比。

|约束距离/Å|Ph B1本次相对能/kcal mol⁻¹|Ph B2本次相对能/kcal mol⁻¹|
|---:|---:|---:|
|2.3|0.000000|0.000000|
|2.1|0.544492|0.951107|
|1.9|1.887666|3.119084|
|1.7|2.863071|4.518937|
|1.5|7.363181|8.386929|

每支路以自身2.3 Å点为零；缩短到1.5 Å分别升能7.363181和8.386929。作者Fig.9提供趋势图，未提供这十个点的可精确逐点相减数字，因此无伪造逐点作者差值。已有Ph两开环最低点高层B2−B1为+0.222283 kcal/mol，无对应作者精确差作为评分目标。有限单调剖面与作者开环偏好一致，不证明全势能面不存在任何闭环极小值、严格零势垒或完整cDET动力学。

### 驻点、连接、原子和同位素质量

|TS|唯一虚频/cm⁻¹|断裂键原生编号|键长/Å|虚频沿该键距离导数|
|---|---:|---|---:|---:|
|S_H_B1_TS|-381.0867|25-26|1.941612|-0.918771|
|S_Mcis_B1_TS|-294.8440|25-27|1.897863|-0.876247|
|S_Mtrans_B1_TS|-250.6865|25-26|1.932836|+0.806491|
|S_Mcis_B2_TS|-292.5253|25-27|1.906912|-0.851426|
|S_Mtrans_B2_TS|-270.8325|25-26|1.927574|+0.821283|

振型正负任意；其余环键投影绝对值约0.03–0.08，目标键在闭环→TS→开环依次伸长。15个环态组成、+1/双重态和来源距离图一致。H B1两侧恢复端点相对独立最低点全原子RMSD为正向0.000764 Å、反向0.003258 Å，低层能差分别−0.000029/+0.000489 kcal/mol；两者均零虚频且连接图一致。

H/D映射采用环C1–C3–C2→醛羰基–亚甲基–末端碳；水氧进入羰基，D连接末端碳。D通道两侧计数均为C5/H13/D1/N1/O1、总电荷+1；H通道均为C5/H14/N1/O1、总电荷+1。这里C5是Fig.7局部亚胺鎓水解核查模型的总原子库存（含N上简化碳），不是把完整S_H底物改称C5；它与完整开环分子计算的片段映射共同支撑产物相容性。公开S_HD4的初始D在四氢吡啶N邻位C2/C6，未误放到环丙基。

作者75 kcal/mol的底物C–H键强引用前人结果，−23 kcal/mol为键强驱动力估计，均不是本次新算HAT势垒。观测与模拟允许标记和未标记醛共存；保环底物供H后进一步氧化与Ph保环产物相容。来源明确不能无歧义区分分子内/分子间氢转移，图式/原子守恒不能证明唯一HAT动力学。

### 定性科学结果逐项对照

|科学方面|作者/输入|实际证据|判定与限制|
|---|---|---|---|
|氧化比较|T_Pyr较易氧化；苯基效应小；N-cyclopropyl体系需要光|8态相对ET三值与来源方向一致|支持比较背景下的光依赖解释；无新激发态计算|
|H、cis-Me、trans-Me局部环命运|主M06列H/trans上坡、cis下坡|五分支符号保持、cis势垒低于trans/H|核心趋势一致；cis B1/B2细序不一致，源模型依赖保留|
|甲基相互转化|观察cis→trans；trans闭环更稳|共同零点稳定性与真实相对立体核验|支持条件化异构化解释；无独立速率/势垒|
|Ph环命运|闭环优化转开环；缩环升能|两条有限剖面十点单调升能|检验分支一致；不宣称全局无闭环态或唯一cDET|
|醛原子与D来源|底物N邻位D出现在醛末端|H/D映射、元素同位素与电荷守恒|连接相容；无精确同位素比例或唯一HAT|
|Ph保环产物|虽强烈开环仍有保环吡啶鎓|开环计算与供氢分子/受氢分子的不同角色整合|与Fig.11条件化解释相容；产物量不等于初始开环速率比|

### 保留差异与专家待审

- cis-Me B2开环能主文−2.5/SI−0.8 kcal/mol冲突保留；实际高层电子能−0.788064676，分别差+1.711935324/+0.011935324，不宣布抄列错误。
- cis-Me B1势垒偏差−1.327878191 kcal/mol且B1/B2细序反转；闭环/TS源几何松弛RMSD约0.477/0.472 Å，不能全部归于舍入。
- Table 3及SI定义E差和方法层次，但未明确排除ZPE/热修正；本次实际比较为高层SCF电子能，不称作者口径已完全确认。
- Gaussian16替代环计算作者Spartan24、氧化比较作者Gaussian09；网格等实现差别及CAM3-B3LYP命名歧义保留。
- Ph十点有限剖面仅支持检验分支开环偏好；H B1连接来自原IRC有效片段加两侧端点优化，不称原IRC完整成功。
- 无新黄素激发态、唯一HAT/DET轨迹、全部构象/IRC、精确同位素比例或溶液速率/产率；同位素后处理支持相容性而非唯一动力学证明。

本篇采用14条semantic规则，中间58分、最终42分；数值规则为0，没有放宽或拟合容差。请专家按规则ID评审科学命题、分拆与权重，并独立裁定源表冲突、跨实现误差和作者能量修正约定。当前formal_scoring_permitted=true、release_ready=false。

### 原文PDF定位与校验

- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_1db677efcdd782ac/documents/main.pdf)；SHA-256 `87f3ee6f0a2d91661c86f5937db71f365551c03332b3cb934032d4e07cd63bce`。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_1db677efcdd782ac/documents/supplementary_001.pdf)；SHA-256 `30fe1abda1628ed1ed4b9c678bd9422c52ba9bcc63d506a2efbe43f596fb1652`。

页码为从1开始的PDF页序；具体图表/物理定义见上文逐项对照。

### 原始输入、日志、代码与验收来源

- [独立科学验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/independent_1db_audit.md)。
- [独立原生复算JSON](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/independent_1db_raw_recompute.json)：每条46个原生日志的绝对路径、SHA-256、route、频率、几何、能量及端点/扫描数据。
- [独立复算代码](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/independent_1db_recompute.py)。
- [连贯计算结果及每态输入路径](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_06/paper_1db677efcdd782ac/connected_native_account.json)：native_states字段列出每态input/sp_input及Opt/Freq/SP日志；其早期electronic-only过强表述已被后续审计撤回，本文件采用更正边界。
- [原子/同位素执行记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1327Z/new44_group_06/paper_1db677efcdd782ac/integrated_atom_and_comparator_account.json)。
- [最新本篇验证矩阵](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_06/paper_1db677efcdd782ac/verification_matrix.json)。
- [父级现行验收记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/parent_acceptance_review.json)及[本篇原始父级接受记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/parent_acceptance_review.json)。

- [H/Me B1原生工作目录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_1db677efcdd782ac/new44_20261022/B1_ring_comparison_a01)：inputs/内为实际GJF，每个编号态目录保存optfreq.log和sp.log。
- [Me B2原生工作目录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_1db677efcdd782ac/short_followup_20261022T1743Z/methyl_B2_competition_a01)：inputs/内为实际GJF，每个编号态目录保存optfreq.log和sp.log。
- [氧化比较原生工作目录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_1db677efcdd782ac/job_followup_20261023T0033Z/author_redox_comparators_a01)：inputs/内为实际GJF，每个编号态目录保存optfreq.log和sp.log。
- [S_Ptrans_B1_open扫描原生日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1327Z/new44_group_06/paper_1db677efcdd782ac/phenyl_source_shortening_scan_syntax_a02/00_S_Ptrans_B1_open_scan/optfreq.log)；SHA-256 `1a4d1041ed6a60baaad26b3385209f2aa96e9cb3faf93522df6b724f1d271d7d`。
- [S_Ptrans_B2_open扫描原生日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1327Z/new44_group_06/paper_1db677efcdd782ac/phenyl_source_shortening_scan_syntax_a02/01_S_Ptrans_B2_open_scan/optfreq.log)；SHA-256 `c744472d18f4b12d3c7c739c2a4ca0b472394f0dbb6080e26726a64aa1d6f9ec`。

未把这些服务器原生日志复制为新实验；审查材料通过以上真实路径追溯。

## 4. 逐项评分：最终JSON直接引用

**总计100分；中间科学结果58分、最终结论42分。所有14条均为semantic二元项，每项全部条件满足得满分，否则0。** 下列描述和expected逐字引用最终JSON，不混入维护者解释。

|条目ID|规则ID|类别|分值|description|
|---|---|---|---:|---|
|`pyrrolyl_oxidation`|`r_pyrrolyl_oxidation`|中间|4|氧化比较：吡咯基对照比苯基对照更易氧化|
|`phenyl_oxidation_shift`|`r_phenyl_oxidation_shift`|中间|4|氧化比较：苯基对照与无取代对照接近|
|`h_ring_opening`|`r_h_ring_opening`|中间|7|H取代体系的开环在所比较模型内不利|
|`cis_me_ring_opening`|`r_cis_me_ring_opening`|中间|7|cis-Me开环在相容参考模型内有利|
|`trans_me_ring_opening`|`r_trans_me_ring_opening`|中间|7|trans-Me开环在相容参考模型内不利|
|`methyl_closed_trans_stability`|`r_methyl_closed_trans_stability`|中间|8|甲基体系trans闭环态低于cis闭环态及相关开环态|
|`phenyl_open_preference`|`r_phenyl_open_preference`|中间|9|Ph取代体系在已检验分支偏好开环|
|`aldehyde_connectivity`|`r_aldehyde_connectivity`|中间|6|环碳骨架与醛生成的原子连接相容|
|`deuterium_mapping`|`r_deuterium_mapping`|中间|6|底物N邻位D可映射到醛末端碳|
|`light_dependence_account`|`r_light_dependence_account`|最终|10|最终：氧化比较与光依赖性构成相容解释|
|`nonuniversal_ring_fate`|`r_nonuniversal_ring_fate`|最终|8|最终：取代基与立体效应否定统一快速不可逆开环假设|
|`cis_trans_interconversion`|`r_cis_trans_interconversion`|最终|10|最终：开环与更稳定trans闭环态解释cis→trans转化|
|`retained_phenyl_product`|`r_retained_phenyl_product`|最终|8|最终：Ph保环产物可与其开环偏好并存|
|`isotope_provenance_account`|`r_isotope_provenance_account`|最终|6|最终：底物供氢解释醛标签而不指定唯一H转移历史|

### r_pyrrolyl_oxidation（4分）

**description：** 氧化比较：吡咯基对照比苯基对照更易氧化

**expected：** 对公开T_Pyr和T_Ph作物种及参照相容的实际分子比较，支持T_Pyr比T_Ph更易氧化。比较必须由实际电子结构或等价氧化可达性证据支持；不能把比较物结果当成S_H等N-cyclopropyl底物的实测绝对溶液电位。作者两种T_Pyr取向及约500 mV差仅作来源背景，不要求指定描述符、构象数量或精确数值。

**来源ID：** `V2_MAIN_OXIDATION`, `V2_SI_REDOX`。

### r_phenyl_oxidation_shift（4分）

**description：** 氧化比较：苯基对照与无取代对照接近

**expected：** 对公开T_Ph和T_H作物种及参照相容的实际分子比较，支持苯基取代对氧化可达性的改变较小，未产生类似吡咯基的显著易氧化效应。须有实际相对氧化或等价电子结构证据，不能以分子名称或实验未给电位替代比较。作者小于100 mV为来源背景，不设精确数值窗；不得将比较物结果当成其它底物的绝对溶液电位。

**来源ID：** `V2_MAIN_OXIDATION`, `V2_SI_REDOX`。

### r_h_ring_opening（7分）

**description：** H取代体系的开环在所比较模型内不利

**expected：** 在正确S_H分子骨架、电子态及闭环/开环参照下，实际计算支持其开环相对闭环能量上坡。作者自由基阳离子为参考模型，接受有实际证据支持同一环命运命题的等价模型；仅有闭环结构或观察到保环产物不足。该项不要求H的B1/B2全部构象、5.8或3.2 kcal/mol精确命中。

**来源ID：** `V2_MAIN_RING`, `V2_SI_RING`。

### r_cis_me_ring_opening（7分）

**description：** cis-Me开环在相容参考模型内有利

**expected：** 保留S_Mcis的正确相对立体化学，实际闭环/开环比较支持其开环能量有利。作者主M06-2X模型为参考，物种、参照和能量口径必须对应；不能把其他泛函或热修正下的近零值冒称同一目标。cis-Me B2主文−2.5与SI−0.8 kcal/mol并列保留，二者不是唯一精确靶值；B1/B2细排序不属于本项。

**来源ID：** `V2_MAIN_RING`, `V2_SI_RING`。

### r_trans_me_ring_opening（7分）

**description：** trans-Me开环在相容参考模型内不利

**expected：** 保留S_Mtrans的正确相对立体化学，实际闭环/开环比较支持其开环相对闭环能量上坡。作者主M06-2X模型为参考；来源其它泛函可改变符号，应按相容物理定义评估，不能通过混用方法构造上坡结果。此项不推断独立trans起始实验产物分布，也不设1.8或2.1 kcal/mol精确窗口。

**来源ID：** `V2_MAIN_RING`, `V2_SI_RING`。

### r_methyl_closed_trans_stability（8分）

**description：** 甲基体系trans闭环态低于cis闭环态及相关开环态

**expected：** 在同组成、同电荷/自旋和共同能量零点下，实际计算支持甲基体系trans闭环态比cis闭环态及所比较的相关开环态更稳定；cis/trans必须由分子相对立体化学识别，不能仅凭文件名。局部开环能之差不能代替跨异构体的共同参照比较；不把作者B1/B2标签或全部构象枚举作为额外配额。

**来源ID：** `V2_MAIN_STEREO`, `V2_SI_RING`。

### r_phenyl_open_preference（9分）

**description：** Ph取代体系在已检验分支偏好开环

**expected：** 保留S_Ptrans骨架及相对立体化学，实际结构/能量证据支持所检验分支的开环偏好，且闭环方向未形成受支持的稳定陷阱。作者缩短断裂C–C键时升能的剖面和闭环优化转为开环是参考；允许等价的物理检验。单个开环极小值不足以证明本项；有限剖面不等于全势能面无闭环极小值，也不是已计算完整双分子解离电子转移轨迹。

**来源ID：** `V2_MAIN_RING`, `V2_SI_PHENYL`。

### r_aldehyde_connectivity（6分）

**description：** 环碳骨架与醛生成的原子连接相容

**expected：** 以实际开环分子证据及可核查的原子后处理，建立原环碳到醛羰基、相邻碳和末端碳的连接；所提水解或等价产物形成步骤须保持元素和电荷收支，氧来源须与含微量水的输入相容。作者亚胺鎓水解是参考，不强制特定标签或新水解势垒。只画产物或复述出现醛不足。

**来源ID：** `V2_MAIN_PRODUCTS`。

### r_deuterium_mapping（6分）

**description：** 底物N邻位D可映射到醛末端碳

**expected：** 从公开S_HD4的N邻位C2/C6标记出发，通过实际原子/同位素映射检验，把底物D纳入CH2DCH2CHO的末端碳并保持同位素收支；不能错误地把D初始放在环丙基或醛羰基上。该项检验标签位置及映射相容性，不声称已经得到H/D转移势垒、唯一转移路径或精确同位素比例。

**来源ID：** `V2_MAIN_ISOTOPE`, `V2_SI_ISOTOPE`。

### r_light_dependence_account（10分）

**description：** 最终：氧化比较与光依赖性构成相容解释

**expected：** 最终采用由实际氧化比较支持的分子解释，将T_Pyr较易氧化、T_Ph与T_H接近的关系与公开光/暗观察联系：N-cyclopropyl体系需要更强氧化能力，与光激发黄素背景相容。新增结论是比较物与反应条件的联系；仅复述氧化排序或光照事实不足。不把气相相对电离能当成底物绝对溶液电位，不要求新算黄素激发态或完整光循环。

**来源ID：** `V2_MAIN_OXIDATION`, `V2_SI_REDOX`。

### r_nonuniversal_ring_fate（8分）

**description：** 最终：取代基与立体效应否定统一快速不可逆开环假设

**expected：** 最终整合H、甲基立体异构体与Ph的实际环反应证据，说明开环可达性和闭环稳定性依赖取代基/立体化学，不能普遍假定这些N-cyclopropyl探针一经氧化都快速且不可逆开环。所比较模型内cis-Me开环较H及trans-Me易达，Ph已检验分支更偏好开环；须有支持相对可达性的实际比较，不能仅用反应能当势垒。此结论不要求精确速率、B1/B2细序或把来源方法依赖趋势提升为普适定律。

**来源ID：** `V2_MAIN_RING`, `V2_MAIN_STEREO`, `V2_SI_RING`。

### r_cis_trans_interconversion（10分）

**description：** 最终：开环与更稳定trans闭环态解释cis→trans转化

**expected：** 最终将实际甲基开环证据、共同参照下trans闭环较稳定的结果与公开cis起始后出现trans的观察连接，支持开环后可进入更稳定trans闭环态的相容解释；允许有证据支持同一转化关系的替代路线。新增结论是对观察到的异构化的解释；仅列能量排序不足。不把该解释称为已求得独立异构化势垒、速率或平衡比例，不新增trans起始产物分布目标。

**来源ID：** `V2_MAIN_STEREO`, `V2_SI_RING`。

### r_retained_phenyl_product（8分）

**description：** 最终：Ph保环产物可与其开环偏好并存

**expected：** 最终把S_Ptrans的实际开环偏好与仍观察到保环吡啶鎓产物联系，给出原子/电子收支相容且有实际证据支撑的保环生成解释。作者由另一中性底物N邻位供H后形成自由基、再氧化而保留环的途径为条件化参考；不要求唯一途径或完整后续氧化势垒。新增结论是不同分子角色使开环倾向与保环产物并存，不能把保环产物量直接当初始自由基阳离子开环/去质子化速率比。

**来源ID：** `V2_MAIN_PRODUCTS`, `V2_MAIN_STEREO`。

### r_isotope_provenance_account（6分）

**description：** 最终：底物供氢解释醛标签而不指定唯一H转移历史

**expected：** 最终依据实际开环与H/D原子映射，采用能够解释底物标签进入醛末端、同时容纳未标记醛的氢来源解释；底物供H/D与另一相容H来源可以并存。作者底物转移/歧化是条件化参考，接受有证据的等价来源解释。新增结论是标签与产物混合观察对氢来源的约束；仅声明映射守恒不足。不把谱图50:50模拟当必达比例，也不把分子内或分子间H转移定为唯一已证实动力学。

**来源ID：** `V2_MAIN_ISOTOPE`, `V2_MAIN_PRODUCTS`, `V2_SI_ISOTOPE`。

### 共同科学要求（JSON原文）

仅评价下列中间科学发现与最终科学结论，合计100分；每个叶子项满足全部条件得满分，否则0。无研究过程分、倍率、工具效率、资源投入、假设数、调用数、失败诊断或文风奖励。公开task.md保留的旧60分研究质量/40分解决程度及研究记录要求不另获分，现行评分以本文件为准。科学结果须有真实、相关、可定位的计算或原子后处理证据；复制作者数值、产物观察、正常退出、正确措辞或自报完成不能单独得分。身份、电荷/自旋、相对立体化学、物理定义及证据有效性是对应科学项成立的前提，不另计分。声称极小值须有适当驻点/身份检查；声称TS须有相关虚频和连接证据，允许科学等价连接检验，不强制全IRC、特定软件、构象数量或搜索顺序。不同方法可以接受，但须支持本项明确的物理命题且相容可比，不能用来源别列值或不同零点冒充同一目标；有支持的替代机制可解释同一观察关系。仅泛称模型不同或诚实未解决不自动得分。普通失败仅影响相关项，保留其他独立有效结果；伪造/隐藏答案泄漏按有效性规则处理。全部14条为semantic规则，来源数值及残差为非计分上下文，无精确数值窗；主文/SI冲突、方法依赖及电子能/热项歧义不由Judge临时造数值阈值解决。最终结论必须在最终交付中明确采用；只算出候选而未形成相应解释不得结论分。

### 共同绑定条件（JSON原文）

核对真实物种、电子态、参照和可定位原生证据，仅判断本项科学命题；全部条件满足得满分，否则0；不临时给比例分或过程分。

绑定产物路径：`report/results.json`、`report/report.md`；字段：`$`。须沿交付中的证据链接核对真实research/产物。

## 5. 设计理由、权重依据、改前改后与专家问题

### 设计理由与独立信息

环反应比较是连贯问题的主干，H、cis-Me和trans-Me的能量方向分别设项，避免一个体系失效抹去其它体系。共同零点的甲基trans稳定性与各自局部开环能是不同科学信息；Ph的有限剖面独立评价对闭环稳定陷阱的检验。两项氧化比较分别计分，避免一项错误抹去另一项；产物/同位素映射补全问题两端，不强制任何未公开的作者软件或描述符。

中间分数58分：吡咯基/苯基和苯基/H两项氧化比较各4，H/cis-Me/trans-Me各7，共同零点立体稳定性8，Ph偏好9，醛骨架连接6，D位置映射6。分值依据对核心比较及最终解释的支持作用分配，不依据当前验证成绩或条数平均。H/D两项分别评价碳/氧连接与标签去向，避免把两个可独立错误合成一个模糊部分分项。

最终42分：光依赖关联10，否定统一快速不可逆开环假设8，cis→trans解释10，Ph保环产物相容性8，标签对氢来源的解释6。最终项新增的是跨结果与观察之间的科学关系，不重复奖励一个数字：只有中间能量或映射而没有最终采用相应解释时，不得最终分。Ph保环结果和总环命运结论分开，避免只解释其它底物就隐含得到Ph产品解释分。

本题仍允许有证据的替代机制支持同一科学命题；这不等于任何与作者不同的内部自洽结果都得分。物理定义不可比或相应命题未得到支持时，该项失分并记录来源/模型问题。精确HAT/DET轨迹、完整光循环、绝对溶液电位、精确产率/同位素比例与H B2/全IRC配额未被新增为目标。

### 改前改后

|方面|旧私有评分|现行V2|
|---|---|---|
|总分|研究质量60+问题解决40|科学中间结果58+最终科学结论42，合计100|
|条目|R1–R6假设/模型/执行/验证/决策/可复现性；R7综合解决|14个具体科学叶子项，仅0或满分|
|过程与部分分|过程得分及Judge自由部分分|移除活动过程分和部分分；记录与证据资格不额外计分|
|数值|无唯一数值靶值，保留源冲突|仍无数值硬窗；作者值/实际值/残差完整并列|
|科学边界|四方面连贯问题，条件化解释可接受|问题范围及公开输入逐字节保持；按独立科学事实分拆|
|运行资格|旧过程合同|允许现行V2评分；数值与出版待专家，release_ready=false|

### 待专家明确裁定

- 逐条规则ID的科学命题、证据边界和权重是否恰当；尤其H/Me符号的来源方法依赖和Ph有限剖面不能升格为普适结论。
- `r_cis_me_ring_opening`、`r_nonuniversal_ring_fate`：主文−2.5/SI−0.8、cis B1势垒偏差与细排序反转是否影响当前定性层级；不默认作者有抄列错误。
- `r_methyl_closed_trans_stability`、`r_cis_trans_interconversion`：共同零点能量与真实立体身份支持相容解释，但不作为独立异构化势垒或速率。
- `r_pyrrolyl_oxidation`、`r_phenyl_oxidation_shift`、`r_light_dependence_account`：气相比较对照能量与来源光条件之间的条件化联系，不冒充底物绝对电位。
- `r_aldehyde_connectivity`、`r_deuterium_mapping`、`r_retained_phenyl_product`、`r_isotope_provenance_account`：原子后处理和供氢角色的证据是否足以支持相容解释；不要求唯一HAT、额外活化势垒或50:50。
- Gaussian16/Spartan24与Gaussian09差异、cis B1约0.477 Å几何松弛、作者未明示的ZPE/热项约定，仍需独立数值专家审查。

以上是维护者理由与问题，不添加第4节规则之外的得分条件。合约与协议测试只验证评分加载和加总，不代表真实被评Agent盲测成绩。

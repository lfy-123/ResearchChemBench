# paper_32dea3515c2c7240｜氮手性构型反应性与独立分子反转

**当前状态确认（2026-10-23）：用户接受本篇当前科学问题的验证结果，数值差异保留专家审查。** 要求相关结果已实际计算且结论一致；本确认不等于所有数值窗口通过、全文复现或自动发布。下方差值、方法差异和原始证据继续保留。

**2026-10-21迁移更新：自主科研维护源已采用100分科学分V2，允许进入正式评分；这不是实际Agent满分或论文出版通过。下文PR题面/副本保留历史未迁移。旧评分完整保存在维护源evaluation/migration_history/20261021_pre_v2。**


论文：Construction of chiral nitrogen stereocenters via enantioselective C–H activation；DOI：10.1016/j.chempr.2025.102730。

AR 与 PR 均登记 **PROVISIONAL_PASS_QUALITATIVE（暂定定性通过）**；严格数值整题通过=false。P 反转超出原±2.0 kcal/mol容差。本文提供原任务／评分中文直译和验收证据，不将暂定政策转换为评分满分或发布批准。

## 1. 当前任务完整中文直译

### 1.1 autonomous_research

**科学目标**

在 Pd/L-焦谷氨酸 C–H 烯基化中，什么解释底物 S 两种构型的相对生产性反应活性？分别定义的 S/P 构型互变能量学能对观察到的对映体富集产物确立什么？

使用 `data/inputs/system.json` 获取完整 S/A/P 分子图、手性配体、反应条件和实验观察。S 起始为外消旋；P 具有指定的 E 烯烃。没有提供作为观察归属的氮绝对构型，因此应定义两种构型的一致结构映射。

建立有证据支持的相对生产性反应活性解释，并在分别规定的比较条件下研究 S 和 P 的构型互变。评估这些结果在多大程度上能解释反应观察。改变溶剂或温度就改变了比较。问题不要求完整催化循环、未经表征的配位态互变动力学、定量动态拆分模型或其他氮杂䓬的研究。关于363.15 K乙腈中行为的结论必须限于证据所支持的范围。

**研究与交付物**

提出可检验的解释，选择有信息量的分子模型和方法，执行支持声明所需的研究。假说和计算方法由你选择。在 `research/` 下保留实际输入、输出、日志和分析；单有提案或提供的观察不能解决问题。不要求固定工具顺序、构象数量或完整催化网络。

说明结构、立体化学映射、质子化、总电荷和多重度、溶剂、温度、能量定义及参考态记账。关于过渡态的声明需要适当的频率和化学连接验证。定量动力学声明需要方程、假设以及到可观测量的映射。选择适合实际声明的可靠性检查，区分已获支持和尚未解决的事项。

遵循 `submission_schema.json` 和 `submission_guide.md`。提交 `report/results.json`、`report/report.md` 和 `research/`，关联假说、研究、证据、结论及真实产物。将数值结果连同定义和条件放入 `evidence[].quantities`。报告实际资源使用及未解决的来源或实现选择。研究状态与问题解决状态相互独立。诚实的部分工作或失败可以获得过程分，但不能确立未计算的科学结果。当所声明范围获支持，或记录下来的局限阻止进一步可辩护的进展时停止；不施加固定资源配额。


### 1.2 paper_reproduction

**科学目标**

在 Pd/L-焦谷氨酸 C–H 烯基化中，什么解释底物 S 两种构型的相对生产性反应活性？分别定义的 S/P 构型互变能量学能对观察到的对映体富集产物确立什么？

使用 `data/inputs/system.json` 获取完整 S/A/P 分子图、手性配体、反应条件和实验观察。S 起始为外消旋；P 具有指定的 E 烯烃。没有提供作为观察归属的氮绝对构型，因此应定义两种构型的一致结构映射。

建立有证据支持的相对生产性反应活性解释，并在分别规定的比较条件下研究 S 和 P 的构型互变。评估这些结果在多大程度上能解释反应观察。改变溶剂或温度就改变了比较。问题不要求完整催化循环、未经表征的配位态互变动力学、定量动态拆分模型或其他氮杂䓬的研究。关于363.15 K乙腈中行为的结论必须限于证据所支持的范围。

使用 `author_guidance.md` 作为公开的作者假说与方法基线。针对同一科学问题执行并评估该基线，记录忠实程度及有理据的替代。其假说有待检验；它不提供计算答案。

**研究与交付物**

提出可检验的解释，选择有信息量的分子模型和方法，执行支持声明所需的研究。假说和计算方法由你选择。在 `research/` 下保留实际输入、输出、日志和分析；单有提案或提供的观察不能解决问题。不要求固定工具顺序、构象数量或完整催化网络。

说明结构、立体化学映射、质子化、总电荷和多重度、溶剂、温度、能量定义及参考态记账。关于过渡态的声明需要适当的频率和化学连接验证。定量动力学声明需要方程、假设以及到可观测量的映射。选择适合实际声明的可靠性检查，区分已获支持和尚未解决的事项。

遵循 `submission_schema.json` 和 `submission_guide.md`。提交 `report/results.json`、`report/report.md` 和 `research/`，关联假说、研究、证据、结论及真实产物。将数值结果连同定义和条件放入 `evidence[].quantities`。报告实际资源使用及未解决的来源或实现选择。研究状态与问题解决状态相互独立。诚实的部分工作或失败可以获得过程分，但不能确立未计算的科学结果。当所声明范围获支持，或记录下来的局限阻止进一步可辩护的进展时停止；不施加固定资源配额。


## 2. 作者方法与实际计算过程

正文第9页报告 CMD 经 TS20，a比b低8.6 kcal/mol。SI第28–31页图S10／9.4节规定独立S在 MeCN／353.15 K、P在 n-octane／398.15 K 反转；不能把不同条件的比较偷换为同条件速率。SI第10节给出 B3LYP 优化／频率（Pd def2-SVP，其余6-31G(d)），M06-2X单点（Pd def2-TZVP，其余6-311+G(d,p)）、SMD与Shermo；Data S3提供坐标，并称做了IRC。

实际复用六个核心物种的优化／频率及单点，再核 TS20 两侧80点路径后的极小化和 S/P 端点；采用相应泛函、基组、温度、溶剂。TS20 的H由C转至O且Pd–C形成，有19/21结构映射；达到MaxPoints不等于IRC自身到达极小值。S/P各有一个反转虚频−76.9820／−11.9506 cm⁻¹；四个端点无虚频、图保持、P的E烯烃保持，启动扰动与同一TS负模分别同向和反向。核心RMSD为0.000169、0.011494、0.015400、0.001631 Å，作者a/b扭转余弦均高于0.9997。新S端点作业2b871614实际收敛，126个正频，最低18.1814 cm⁻¹；早期失败的120步轨迹未当成成功结果。

独立审查核48个证据文件哈希、46份日志，并由fchk／作者坐标重新算端点映射。S/P历史优化中有较大上坡试探，不是完整独立IRC／最小能量路径；这里接受的是作者TS／路线、实际驻点和单负模、相反启动方向、不同有效极小值共同构成的来源辅助连接。

作者Gaussian16 A.03与实际C.01不同。实际Shermo2.6.2及RRHO计算已披露；作者未明确低频处理。实际有机物优化6D/7F、混合GenECP及单点5D/7F，不能称隐藏设置逐项相同。Pd中性单重态及配体去质子化由组成重建，不是已取得作者原卡。

## 3. 原值、自算值及定性一致性

单位 kcal/mol；差=自算−作者。主比较保留原 RRHO，不因qRRHO更近而换定义。

|量／条件|作者|自算RRHO|差值|原容差|数值对照|
|---|---:|---:|---:|---:|---|
|G(TS20-b)−G(TS20-a)，363.15 K／MeCN|8.60|8.544734|−0.055266|±1.5|窗内，a更低|
|S反转，353.15 K／MeCN|31.82|31.708054|−0.111946|±2.0|窗内|
|P反转，398.15 K／n-octane|33.99|36.598800|+2.608800|±2.0|超窗|

预先声明的Grimme qRRHO100敏感性值依次为8.484995、31.683079、34.657097；P在此处理下差+0.667097，但不能因此宣布原RRHO数值规则通过。来源低频设置未明确，差异尚未唯一归因。三项有效结果支持a生产性活化更容易，以及两种独立分子在各自条件下有高构型反转势垒；不证明较高反应通道完全不反应、全局控速、实验准确ee、同条件S/P速率排序，或36 h内S足够快速互变从而闭合定量DKR。

“11/11覆盖”表示三个关键点、两个结论、六条评分规则的覆盖标识，不是11个独立结论，也不是11项数值全部通过。

## 4. 现行科学分 V2 规则逐项完整中文直译

### 4.1 共同政策、绑定与资格

政策：`paper_science_v2`。只评价任务范围内的论文科学发现，不评价研究过程、工具调用次数、成本、格式或失败解释。每项均为二元评分：有支持且符合条件取得全部指定分，错误或缺失得0分。比较前确定分子、连接关系、原子组成、电荷/自旋、可观测量、单位、参考态和条件。必须有真实关联计算和原生产物；给定观察、复制论文值及正常结束本身不足。按不变题面要求验证最低点与过渡态。物理结果可比时允许其他软件、方法和候选标签。不要求历史验证轨迹、固定假设数量或范围外计算。数值目标与容差固定，为包含边界的绝对容差，由宿主计算，Judge不得修改。没有独立数值规则的来源背景数字不构成数值门槛。定性项独立于数值窗口通过，须有自身实际计算支持。无支持或失败的条目只失去本项分。最终结论要求明确且有支持的推断或选择。确实无法确定必要物理身份/参照时需人工审查；仅出版审查待定不阻断本版本。

所有规则绑定 `report/results.json`、`report/report.md`、`research/`，字段为 `$`；比较方式：先匹配物理对象、状态、条件、能量零点及真实关联证据，再独立评价本项；不按数字接近程度挑选对象。

运行评分资格：允许；当前范围定性验证：通过；严格数值整题：不通过；出版审查：待定。PR专家副本与其规则保留历史、未迁移，本节只对应自主科研维护源。公开题面中若有历史过程分措辞，为保持合同字节不变而保留，不再授予过程分。

|ID / 规则ID|科学角色|分值|判定|
|---|---|---:|---|
|ts_gap / r_ts_gap|中间发现|10|数值|
|inversion_s / r_inversion_s|中间发现|10|数值|
|inversion_p / r_inversion_p|中间发现|10|数值|
|ts_direction / r_ts_direction|中间发现|10|定性|
|cmd_structure / r_cmd_structure|中间发现|10|定性|
|inversion_s_identity / r_inversion_s_identity|中间发现|10|定性|
|inversion_p_identity / r_inversion_p_identity|中间发现|10|定性|
|reactivity_conclusion / r_reactivity_conclusion|最终结论|15|定性|
|configuration_conclusion / r_configuration_conclusion|最终结论|15|定性|

### r_ts_gap：C–H活化过渡态共同参考自由能差（10分）

参考ID：`ts_gap`；类型：`numeric`；来源证据：`E_PATH`, `E_PROFILE`, `E_METHOD`, `E_COORD`。

目标 8.6 kcal/mol；绝对容差 ±1.5 kcal/mol，包含边界。

比较完整Pd/L-pGlu/S、相同组成和粒子/质子库存的G(TS20-b)−G(TS20-a)，并映射作者a/b结构；这是共同参考剖面之差，不是两条各自局部势垒之差。MeCN/SMD、363.15 K热项；相同电荷/自旋。来源未明确输入电荷/多重度，中性闭壳层Pd(II)/双去质子化L-pGlu+中性S为需声明并支持的图重构。真实相关鞍点与反应连接合格后，按8.6±1.5 kcal/mol比较。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_inversion_s：S独立分子的反转自由能势垒（10分）

参考ID：`inversion_s`；类型：`numeric`；来源证据：`E_INV`, `E_COORD`。

目标 31.82 kcal/mol；绝对容差 ±2.0 kcal/mol，包含边界。

比较G(S反转鞍点)−G(与其相连的孤立S/1b最低点)，完整中性分子，无Pd/配体、同粒子数；MeCN/SMD、353.15 K，单重态为图重构假设须支持。使用自身最低点与自身热项、真实相关模式及连接；按31.82±2.0 kcal/mol比较。不得用催化条件363.15 K替代。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_inversion_p：P独立分子的反转自由能势垒（10分）

参考ID：`inversion_p`；类型：`numeric`；来源证据：`E_INV`, `E_COORD`。

目标 33.99 kcal/mol；绝对容差 ±2.0 kcal/mol，包含边界。

比较G(P反转鞍点)−G(与其相连的孤立P/3ba最低点)，完整中性E-烯基化分子，无Pd/配体、同粒子数；n-octane/SMD、398.15 K，单重态为图重构假设须支持。使用自身最低点/热项、真实相关模式及连接；按33.99±2.0 kcal/mol比较。不得为接近目标事后更换RRHO/qRRHO、最低点或温度。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_ts_direction：独立的立体选择方向（10分）

参考ID：`ts_direction`；类型：`semantic`；来源证据：`E_PATH`, `E_PROFILE`, `E_COORD`。

相同映射物种、组成、状态和MeCN/363.15 K条件下，实际计算支持G(TS20-a)<G(TS20-b)。独立判断方向；未映射或方向反转不通过。无需先通过8.6数值窗口。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_cmd_structure：C–H活化的实际键变和构型归属（10分）

参考ID：`cmd_structure`；类型：`semantic`；来源证据：`E_PATH`, `E_COORD`。

实际两构型计算的结构、相关振动和连接证据支持CMD：芳基C–H断裂、向配体受体转移H及C–Pd成键，并保持配体手性与七元环构型的一致映射。不能用近共平面氮单个局部有向体积变化直接替代完整构型判断；仅TS标签不通过。不要求完整催化循环或固定IRC点数。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_inversion_s_identity：S的构型互变结构发现（10分）

参考ID：`inversion_s_identity`；类型：`semantic`；来源证据：`E_INV`, `E_COORD`。

真实S最低点和反转鞍点、相关软模/路径或等价连接支持同一分子两构型互变，并保持组成与质子化；在353.15 K/MeCN下有正的反转自由能势垒。仅源坐标、频率符号或写“可反转”不通过；该结构/定性结果独立于31.82数值窗口。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_inversion_p_identity：P的构型互变结构发现（10分）

参考ID：`inversion_p_identity`；类型：`semantic`；来源证据：`E_INV`, `E_COORD`。

真实E-烯基化P最低点和反转鞍点、相关软模/路径或等价连接支持同一分子两构型互变而不改变E烯烃及化学组成；在398.15 K/n-octane下有正的反转自由能势垒。仅源坐标或“产物稳定”叙述不足；此项不要求33.99数值窗口通过。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_reactivity_conclusion：最终：两构型生产性反应活性不同（15分）

参考ID：`reactivity_conclusion`；类型：`semantic`；来源证据：`E_PATH`, `E_PROFILE`, `E_SYSTEM`。

最终将有效映射的两套反应态和较低TS20-a连接到其更有利的生产性C–H活化，给出计算支持的立体区分解释。无需数值8.6落窗，但必须实际支持方向及相关反应。不能断言高通道恰好零反应、未经映射的绝对构型、全循环决速或精确实验终点ee；有执行证据的等价机理解释可接受。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_configuration_conclusion：最终：分别条件下的构型稳定性及DKR边界（15分）

参考ID：`configuration_conclusion`；类型：`semantic`；来源证据：`E_INV`, `E_OBS`, `E_METHOD`。

最终根据已计算的S/P反转、各自最低点/溶剂/温度和相应正势垒，说明孤立分子构型互变受热活化限制，并将其与时间曲线和产物稳定观察作有边界的联系。分别条件的数值排序不能证明同条件动力学排序，也不能证明363.15 K/MeCN/36 h中S快速互变或闭合定量DKR模型。需要两者真实结果支持这一科学判断，不因P数值超窗自动取消；不要求配位态互变、全循环或精确ee。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### 4.2 设计理由（不是评分规则）

相对生产性活性与构型互变是解释型任务，定量30、定性70（中间70、最终30）。原8.6±1.5及31.82/33.99±2窗口原样保留；P超窗仍丢10分，不能按验证误差放宽。CMD/互变结构、独立方向与受条件约束的最终解释各提供不同科学信息；没有固定计算次数奖励。

### 4.3 有效性条件

捏造证据或将参考值冒充独立计算、经证明未经授权使用隐藏答案使提交无效；普通计算失败、错误或缺失只使受影响科学项得0分。出版数值冲突及限制见后文，不将其隐藏或作为过程分。


## 5. 原任务、验收及原生日志入口

- autonomous_research：[agent_input/task.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_32dea3515c2c7240/agent_input/task.md)；[evaluation/scoring_rules.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_32dea3515c2c7240/evaluation/scoring_rules.json)；[evaluation/verified_computation_reference.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_32dea3515c2c7240/evaluation/verified_computation_reference.md)
- paper_reproduction：[agent_input/task.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_32dea3515c2c7240/agent_input/task.md)；[evaluation/scoring_rules.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_32dea3515c2c7240/evaluation/scoring_rules.json)；[evaluation/verified_computation_reference.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_32dea3515c2c7240/evaluation/verified_computation_reference.md)

[父级验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/parent_acceptance_decision.json)；[独立验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/review_32dea/独立验收复核.md)；[机器审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/review_32dea/independent_review.json)；[原生日志及端点映射审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/review_32dea/native_checks.json)；[原生作者路线审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_32dea3515c2c7240/author_route_closeout_20261020T1340Z/author_route_native_audit.json)

直接原生日志样例（全量路径见审计）：

- [  endpoint.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_32dea3515c2c7240/returned_results_followup_20261020T1140Z/calculations/S_forward_calcfc_internal/outputs/endpoint.log)
- [  frequency.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_32dea3515c2c7240/returned_results_followup_20261020T1140Z/calculations/S_forward_calcfc_internal/outputs/frequency.log)
- [  optfreq.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_32dea3515c2c7240/new10_20261016/calculations/1b-TS/outputs/optfreq.log)
- [  optfreq.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_32dea3515c2c7240/new10_20261016/calculations/1b-a/outputs/optfreq.log)
- [  endpoint_forward.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_32dea3515c2c7240/new10_20261016/followup_20261017/calculations/1b-TS_irc_endpoints_r1/outputs/endpoint_forward.log)

## 6. 专家应裁定的事项

在作者路线核验许可下，判断 S/P 的来源辅助连接是否足够支撑本题有界构型互变结论，同时保留“完整独立IRC未复现”。评估P的+2.608800偏差对精确速率的影响，不能因其高势垒定性仍在就称数值无影响。检查跨温度、跨溶剂的解释边界以及中性单重态／去质子化重建是否清楚。若另需完整DKR、定量ee或同条件速率比较，那属于更强目标，不能假称当前材料已完成。

两模式任务目录原样轻量复制；不改原评分、不把qRRHO替换为主值、不由验收推断满分或发布。


轻量审查副本：[autonomous_research轻量副本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/autonomous_research/paper_32dea3515c2c7240)；[paper_reproduction轻量副本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/paper_reproduction/paper_32dea3515c2c7240)。来源路径与文件哈希见对应任务的 `evaluation/evidence_map.json`；数值、方法偏离和定性结论见[新增8篇核对报告](../数值误差与计算方法及定性结论核对.md)。副本无符号链接，未复制外部QC缓存。

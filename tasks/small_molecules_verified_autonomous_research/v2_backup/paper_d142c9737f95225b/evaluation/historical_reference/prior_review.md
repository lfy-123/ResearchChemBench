# 锰催化转移氢化：候选模型定性通过与多来源数值冲突

**当前状态确认（2026-10-23）：用户接受本篇当前科学问题的验证结果，数值差异保留专家审查。** 要求相关结果已实际计算且结论一致；本确认不等于所有数值窗口通过、全文复现或自动发布。下方差值、方法差异和原始证据继续保留。

**2026-10-21迁移更新：自主科研维护源已采用100分科学分V2，允许进入正式评分；这不是实际Agent满分或论文出版通过。下文PR题面/副本保留历史未迁移。旧评分完整保存在维护源evaluation/migration_history/20261021_pre_v2。**


论文：Effect of Unique NNS Ligand in Manganese-Catalyzed Transfer Hydrogenation Reaction—A DFT Mechanistic Study。DOI：`10.1002/cctc.202501586`。论文 ID：`paper_d142c9737f95225b`。

**纳入状态：父级两模式登记 PROVISIONAL_PASS_QUALITATIVE；现行参考随后确认当前范围定性计算通过；不是严格数值全项通过或出版通过。** 本文保留既有科学证据；本次仅迁移自主科研评分，不新增计算或修改公开输入。

[原文](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_d142c9737f95225b/documents/main.pdf) · [父级验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/parent_acceptance_decision.json) · [独立复核](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/acceptance_review.md) · [原生日志独立审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/acceptance_native_audit.json)

补充材料：[supplementary_001.docx](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_d142c9737f95225b/documents/supplementary_001.docx)。

## 1. 实际任务题面完整中文翻译

### 1.1 自主科研模式

[英文实际题面](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_d142c9737f95225b/agent_input/task.md)；[本包完整轻量任务](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/autonomous_research/paper_d142c9737f95225b)。

#### 科学目标

指定锰前催化剂的配体环境如何影响合理的活性形式、异丙醇氧化和苯乙酮还原的可达性？对一个明确定义的催化剂构型，可以支持什么立体化学偏向？

#### 输入和范围

使用 `data/inputs/system.json` 获取完整的前体／配体图、碱处理和反应观察。从这些起始事实提出化学上合理的活性形式假设，并研究它们如何影响转移氢化的两个半反应。不把任何活性形式或布居作为已知事实提供。评估的科学范围是可辩护候选形式的反应能量学，以及以指定催化剂构型为条件的立体化学结果。不要求计算前体活化势垒、证明实际溶液布居、完整催化剂物种分布、宏观对映体过量值或实验速率。无硫前体属于实验背景。分子 H2 氢化、同位素效应和完整前体平衡不属于必需核心。

#### 研究与证据

为本问题提出并检验解释。选择有信息量的模型和计算，执行它们，并用证据保留、修订或拒绝解释。机理、待研究结构、方法和执行顺序由你选择。不要求穷尽反应网络，也不规定固定计算配额。

提供实际结构、输入、输出、日志和分析。标识分子图、构象、电荷、电子态、介质和热力学约定。数值证据应放在 `evidence[*].quantities` 中，并包含科学名称、物理定义、值、单位和条件。区分曲线纵坐标、局部活化势垒、反应自由能和电子能；为每个差值指定分子和粒子账本。过渡态声明需要频率和反应连通性证据。动力学或布居声明需要从计算量到观察结果的可辩护映射。

科学得分关注有证据支持的中间科学结果和结论。仅重述实验观察、复制来源数值或完成计算作业并不能确立结果。在问题范围内，有充分支持的替代解释是可接受的。说明限制和来源歧义，不得暗中选择有利数值或赋予未计算的量。

#### 交付物

按照共享 schema 和指南提交 `report/results.json`、`report/report.md` 和 `research/`。将研究、证据和结论链接至真实文件。记录实际设置和资源使用。研究完成与问题解决是两回事：保留诚实的部分工作或失败工作及其尝试输入和日志。当证据支持所述范围时停止；不得把尚未解决的工作表述为已解决的科学结果。

### 1.2 论文复现模式

[英文实际题面](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_d142c9737f95225b/agent_input/task.md)；[本包完整轻量任务](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/paper_reproduction/paper_d142c9737f95225b)。

#### 科学目标

指定锰前催化剂的配体环境如何影响合理的活性形式、异丙醇氧化和苯乙酮还原的可达性？对一个明确定义的催化剂构型，可以支持什么立体化学偏向？

#### 输入和范围

使用 `data/inputs/system.json` 获取完整的前体／配体图、碱处理和反应观察。从这些起始事实提出化学上合理的活性形式假设，并研究它们如何影响转移氢化的两个半反应。不把任何活性形式或布居作为已知事实提供。评估的科学范围是可辩护候选形式的反应能量学，以及以指定催化剂构型为条件的立体化学结果。不要求计算前体活化势垒、证明实际溶液布居、完整催化剂物种分布、宏观对映体过量值或实验速率。无硫前体属于实验背景。分子 H2 氢化、同位素效应和完整前体平衡不属于必需核心。

使用 `author_guidance.md` 复现并评估同一科学比较。它提供作者假设、反应拓扑、模型身份和方法。构建并验证计算所需的分子几何结构。

#### 研究与证据

为本问题提出并检验解释。选择有信息量的模型和计算，执行它们，并用证据保留、修订或拒绝解释。使用 `author_guidance.md` 作为已披露的基线，并对其作批判性评估。选择实现方式并论证替代方案。不要求穷尽反应网络，也不规定固定计算配额。

提供实际结构、输入、输出、日志和分析。标识分子图、构象、电荷、电子态、介质和热力学约定。数值证据应放在 `evidence[*].quantities` 中，并包含科学名称、物理定义、值、单位和条件。区分曲线纵坐标、局部活化势垒、反应自由能和电子能；为每个差值指定分子和粒子账本。过渡态声明需要频率和反应连通性证据。动力学或布居声明需要从计算量到观察结果的可辩护映射。

科学得分关注有证据支持的中间科学结果和结论。仅重述实验观察、复制来源数值或完成计算作业并不能确立结果。在问题范围内，有充分支持的替代解释是可接受的。说明限制和来源歧义，不得暗中选择有利数值或赋予未计算的量。

#### 交付物

按照共享 schema 和指南提交 `report/results.json`、`report/report.md` 和 `research/`。将研究、证据和结论链接至真实文件。记录实际设置和资源使用。还应标识方案忠实程度与有依据的替代。研究完成与问题解决是两回事：保留诚实的部分工作或失败工作及其尝试输入和日志。当证据支持所述范围时停止；不得把尚未解决的工作表述为已解决的科学结果。

## 2. 作者路线与方法

作者以 NN 三羰基（Mn1/A，含悬挂硫）和 NNS 二羰基（Mn2/B）的 Me/tBu 候选形式比较转移氢化。异丙醇氧化经过 O–H 与 C–H 转移，形成胺–氢化物和丙酮；苯乙酮还原经过 Mn–H 向 C、N–H 向 O 的转移生成醇。静息异丙氧基态改变有效氧化零点。立体结论限固定催化剂构型，不能把单构型计算推广为总体 ee。

以下方法与计算过程取自现行参考 2026-10-20T03:24:37 更新，保留其限定；标题重新编排，物理量不改。

### 2.1 作者与实际方法逐项核对

来源：[正文](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_d142c9737f95225b/documents/main.pdf)（p3方法、Figures4–6/8）和[补充材料Table S2/S3](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_d142c9737f95225b/documents/supplementary_001.docx)。

| 项目 | 作者要求 | 实际输入及证据 | 判断 |
|---|---|---|---|
| Optimization / frequency / basis / ECP | M06L/all-electron TZVP; full gas-phase unconstrained geometries; analytical frequencies; no truncation | M06L/TZVP gas opt/freq, all atoms; no ECP; valid minima0 imaginary and TS1 imaginary | MATCH |
| Single-point functional / dispersion / damping | M06L/TZVP, GD3 (Grimme2010 ref34; no BJ specified) | M06L/TZVP empiricaldispersion=gd3, default GD3 zero damping, not GD3BJ | MATCH |
| Solvent / same geometry | SMD isopropanol SP on gas optimized geometries | scrf=(smd,solvent=2-propanol), Eps19.264; geom=allcheck guess=read; same opt/freq/SP geometry | MATCH |
| Composition / charge / spin | Complete neutral A NN tricarbonyl pendant-S and B NNS dicarbonyl amido models and neutral amine-hydrides; multiplicities not printed | Full source atom identities and balanced ledgers; charge0, closed-shell singlet Mn(I); source face and ligand coordination retained | SPECIFIED_COMPOSITION_MATCH_UNREPORTED_SPIN_DISCLOSED |
| Temperature / pressure / standard state | 298.15K,1atm | freq temperature=298.15 pressure=1 verified in native thermochemistry; no1M adjustment or added quasi-harmonic correction | MATCH |
| Thermal assembly / reference zero / particle ledger | Gas E/Gcorr and solution E/Gtot printed; exact assembly not explicit; main and printed solutionGtot inconsistent | G=E(M06L-GD3/SMD)+Gcorr(gas M06L) on same geometry; separated reactants, resting state and matched S/R references explicit; signed particle ledgers balanced | SOURCE_SUPPORTED_RECONSTRUCTION_NUMERIC_QUALIFICATION |
| Software revision / grid / thresholds | Gaussian16 C.01 (main ref29); grid/input thresholds/scaling unreported | G16 C.01; ultrafine grid, tight optimization/SCF, XQC, nosymm; harmonic thermochemistry without empirical scaling | VERSION_MATCH_UNREPORTED_SETTINGS_DISCLOSED |
| Reaction connectivity route | Analytical frequency characterization and IRC | All relevant stationary energy chains valid; five bilateral IRC-segment/minimum links plus representative oxidation TS1 mode-displacement/opt and TS2 converged-IRC-prefix/opt share Int1;22 valid endpoint stages | AUTHOR_PES_METHOD_MATCH_CONNECTIVITY_IMPLEMENTATION_QUALIFIED |

实际模型为完整Mn1 NN三羰基与Mn2 NNS二羰基，Me/tBu取代基及相应胺-氢化物；无截短。作者公开M06L/全电子TZVP气相Opt/Freq、同几何GD3零阻尼/SMD异丙醇SP、Gaussian16 C.01、298.15K和1atm一致。中性闭壳层单重态是披露的候选条件，不证明作者未报告的全部自旋设置或真实布居。实际使用UltraFine、Tight、XQC、NoSymm；不额外加1M、qRRHO或经验频率缩放。

自由能采用G=E_solution(M06L+GD3/SMD)+Gcorr_gas(M06L)。该组合有SI逐态字段和正文重构支持，但打印Gtot/重复Gcorr冲突没有消失，不能选对自己最有利的来源。保留三种来源逐项对照。

## 3. 实际计算过程和证据验收

1. 按正文/SI识别四种候选催化剂、静息态、两半反应TS1/Int1/TS2、底物与产物；核对原子图、CO配位、S/R面、质子和电荷。
2. 原方法气相无约束优化与频率验证：最低点0虚频、过渡态1虚频。丙酮原虚频结构不作为成功结果，沿实际模式两侧修复后保留两个零虚频结果；Mn1-Me/R TS2使用已成功recover01后继，未借用失败母作业热项。
3. 对各有效几何完成同几何高层单点，用自身频率热校正组合能量。53条有效链覆盖68个比较ID；展开恢复变体为72项自算值。ID含相互关联的推导量，不等于68个独立实验。
4. 路径证据包括既有5组双侧IRC片段/优化端点连接，合计22个有效端点阶段。代表还原路线Mn1-tBu/R支持Mn-H向底物C转移、继而N-H向O转移；代表氧化路线Mn2-tBu支持O-H与C-H转移经过共同Int1。
5. 氧化TS2反向第17收敛IRC点接Tight无约束优化，150正频、最低38.0676 cm⁻¹，与TS1端点重原子RMSD 0.002524 Å；Opt/Freq同几何RMSD约2.25×10⁻¹⁵ Å。TS1反向模式位移+优化、TS2 IRC前缀+优化只按已有证据性质接受，不冒称完整IRC。失败corrector18、另一S反向corrector15等仍记失败。
6. 构造相对分离反应物、相对静息态、S/R配对及完整TS1/TS2包络；从正文与两套SI整理全部作者值，自算−来源逐项比较。
7. 2026-10-20重读106份原始能量链日志，验证哈希、正常结束、虚频类别，从53条链重算72项变体，与已有数值账本最大重算差0.0 kcal/mol（同解析精度）。此前独立核查另含最新端点两阶段，共108份该论文日志。

最新代表氧化端点作业hpc-job-1a353017-b186-4825-8d66-febe5b620a8e：Opt约2732.40秒、Freq约1931.62秒，均exit0及正常结束。22是端点阶段数，不是22种独立物种。失败前代和成功后继完整保留。

### 3.1 数值定义

- ΔG=Σν_iG_i×627.509474 kcal mol⁻¹ Eh⁻¹，粒子和电荷账本显式保留。
- 氧化曲线零点为对应amido+iPrOH；有效氧化以N质子化Mn异丙氧基静息态为零点。
- 还原零点为对应amine-hydride+acetophenone；固定构型R−S用TS1_R−TS1_S。
- 相对曲线坐标、局部势垒、反应自由能和电子能不得混称。个别TS的G低于邻近Int1不说明电子PES无势垒。

## 4. 现行科学分 V2 规则逐项完整中文直译

### 4.1 共同政策、绑定与资格

政策：`paper_science_v2`。只评价任务范围内的论文科学发现，不评价研究过程、工具调用次数、成本、格式或失败解释。每项均为二元评分：有支持且符合条件取得全部指定分，错误或缺失得0分。比较前确定分子、连接关系、原子组成、电荷/自旋、可观测量、单位、参考态和条件。必须有真实关联计算和原生产物；给定观察、复制论文值及正常结束本身不足。按不变题面要求验证最低点与过渡态。物理结果可比时允许其他软件、方法和候选标签。不要求历史验证轨迹、固定假设数量或范围外计算。数值目标与容差固定，为包含边界的绝对容差，由宿主计算，Judge不得修改。没有独立数值规则的来源背景数字不构成数值门槛。定性项独立于数值窗口通过，须有自身实际计算支持。无支持或失败的条目只失去本项分。最终结论要求明确且有支持的推断或选择。确实无法确定必要物理身份/参照时需人工审查；仅出版审查待定不阻断本版本。

所有规则绑定 `report/results.json`、`report/report.md`、`research/`，字段为 `$`；比较方式：先匹配物理对象、状态、条件、能量零点及真实关联证据，再独立评价本项；不按数字接近程度挑选对象。

运行评分资格：允许；当前范围定性验证：通过；严格数值整题：不通过；出版审查：待定。PR专家副本与其规则保留历史、未迁移，本节只对应自主科研维护源。公开题面中若有历史过程分措辞，为保持合同字节不变而保留，不再授予过程分。

|ID / 规则ID|科学角色|分值|判定|
|---|---|---:|---|
|active_nn / r_active_nn|中间发现|5|定性|
|active_nns / r_active_nns|中间发现|5|定性|
|oxidation_connection / r_oxidation_connection|中间发现|10|定性|
|reduction_connection / r_reduction_connection|中间发现|10|定性|
|rest_Mn1_Me / r_rest_Mn1_Me|中间发现|3|定性|
|rest_Mn1_tBu / r_rest_Mn1_tBu|中间发现|2|定性|
|rest_Mn2_Me / r_rest_Mn2_Me|中间发现|3|定性|
|rest_Mn2_tBu / r_rest_Mn2_tBu|中间发现|2|定性|
|oxidation_order_Me / r_oxidation_order_Me|中间发现|8|定性|
|oxidation_order_tBu / r_oxidation_order_tBu|中间发现|7|定性|
|reduction_order_Me / r_reduction_order_Me|中间发现|5|定性|
|reduction_order_tBu / r_reduction_order_tBu|中间发现|5|定性|
|stereo_Mn1_Me / r_stereo_Mn1_Me|中间发现|3|定性|
|stereo_Mn1_tBu / r_stereo_Mn1_tBu|中间发现|3|定性|
|stereo_Mn2_Me / r_stereo_Mn2_Me|中间发现|2|定性|
|stereo_Mn2_tBu / r_stereo_Mn2_tBu|中间发现|2|定性|
|cycle_hydrogen_ledger / r_cycle_hydrogen_ledger|中间发现|5|定性|
|activity_conclusion / r_activity_conclusion|最终结论|10|定性|
|stereo_conclusion / r_stereo_conclusion|最终结论|10|定性|

### r_active_nn：NN三羰基候选的实际配位结构（5分）

参考ID：`active_nn`；类型：`semantic`；来源证据：`E_PRECURSOR`, `E_METHOD`。

实际计算结构支持完整中性NN-Mn(I)(CO)3酰胺型候选，硫臂游离，保留给定配体连接及CO库存；说明并支持所用电子态。不能仅凭画图或提出假设得分；不要求证明真实溶液布居或前体活化势垒。等价且有证据支持的候选映射可接受。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_active_nns：NNS二羰基候选的实际配位结构（5分）

参考ID：`active_nns`；类型：`semantic`；来源证据：`E_PRECURSOR`, `E_METHOD`。

实际计算结构支持完整中性NNS-Mn(I)(CO)2酰胺型候选，硫参与配位；与NN三羰基保持完整配体身份，显式说明失去CO和电子态。不能仅凭候选标签得分；不要求真实布居或额外前体活化计算。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_oxidation_connection：异丙醇氧化的氢转移连接（10分）

参考ID：`oxidation_connection`；类型：`semantic`；来源证据：`E_OX`, `E_SI`。

实际驻点和相关振动/反应连接支持异丙醇O–H与C–H氢转移，形成丙酮及相应胺-氢化物；质子、氢化物、原子及电荷配平。要求真实反应态连接，不以任务执行成功或任意负频代替；无需复刻验证者IRC步骤，不设来源冲突绝对势垒窗口。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_reduction_connection：苯乙酮还原的氢转移连接（10分）

参考ID：`reduction_connection`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

实际驻点及相关振动/反应连接支持由匹配胺-氢化物向苯乙酮转移Mn–H氢化物至碳和N–H质子至氧，形成正确1-苯乙醇；结构/原子映射支持所称产物面。与氧化半反应区分，不能用氧化势垒替代；不设冲突绝对势垒窗口。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_rest_Mn1_Me：Mn1-Me静息态稳定化（3分）

参考ID：`rest_Mn1_Me`；类型：`semantic`；来源证据：`E_OX`, `E_CYCLE`, `E_SI`。

对Mn1-Me（Mn1为NN三羰基，Mn2为NNS二羰基），实际自由能支持N质子化Mn异丙氧基静息态低于匹配amido+iPrOH，故同一氧化TS相对该静息态的有效势垒高于其相对分离反应物的纵坐标。必须使用同一TS、配平粒子/电荷及一致热项；独立评价稳定化符号和零点改变，不要求来源冲突数值命中。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_rest_Mn1_tBu：Mn1-tBu静息态稳定化（2分）

参考ID：`rest_Mn1_tBu`；类型：`semantic`；来源证据：`E_OX`, `E_CYCLE`, `E_SI`。

对Mn1-tBu（Mn1为NN三羰基，Mn2为NNS二羰基），实际自由能支持N质子化Mn异丙氧基静息态低于匹配amido+iPrOH，故同一氧化TS相对该静息态的有效势垒高于其相对分离反应物的纵坐标。必须使用同一TS、配平粒子/电荷及一致热项；独立评价稳定化符号和零点改变，不要求来源冲突数值命中。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_rest_Mn2_Me：Mn2-Me静息态稳定化（3分）

参考ID：`rest_Mn2_Me`；类型：`semantic`；来源证据：`E_OX`, `E_CYCLE`, `E_SI`。

对Mn2-Me（Mn1为NN三羰基，Mn2为NNS二羰基），实际自由能支持N质子化Mn异丙氧基静息态低于匹配amido+iPrOH，故同一氧化TS相对该静息态的有效势垒高于其相对分离反应物的纵坐标。必须使用同一TS、配平粒子/电荷及一致热项；独立评价稳定化符号和零点改变，不要求来源冲突数值命中。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_rest_Mn2_tBu：Mn2-tBu静息态稳定化（2分）

参考ID：`rest_Mn2_tBu`；类型：`semantic`；来源证据：`E_OX`, `E_CYCLE`, `E_SI`。

对Mn2-tBu（Mn1为NN三羰基，Mn2为NNS二羰基），实际自由能支持N质子化Mn异丙氧基静息态低于匹配amido+iPrOH，故同一氧化TS相对该静息态的有效势垒高于其相对分离反应物的纵坐标。必须使用同一TS、配平粒子/电荷及一致热项；独立评价稳定化符号和零点改变，不要求来源冲突数值命中。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_oxidation_order_Me：Me取代下NN/NNS氧化比较（8分）

参考ID：`oxidation_order_Me`；类型：`semantic`；来源证据：`E_OX`, `E_SI`。

在相同Me取代、异丙醇介质、298.15 K及一致1 atm/透明换算条件下，匹配amido+iPrOH参照的实际计算支持NN三羰基氧化势垒低于NNS二羰基。判断家族顺序，不要求Me/tBu内部顺序或绝对势垒命中；不能比较不相容零点。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_oxidation_order_tBu：tBu取代下NN/NNS氧化比较（7分）

参考ID：`oxidation_order_tBu`；类型：`semantic`；来源证据：`E_OX`, `E_SI`。

在相同tBu取代、异丙醇介质、298.15 K及一致1 atm/透明换算条件下，匹配amido+iPrOH参照的实际计算支持NN三羰基氧化势垒低于NNS二羰基。判断家族顺序，不要求Me/tBu内部顺序或绝对势垒命中；不能比较不相容零点。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_reduction_order_Me：Me取代下S通道NN/NNS还原比较（5分）

参考ID：`reduction_order_Me`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

在匹配Me取代、相同底物面和已映射催化剂构型下，实际计算支持NNS二羰基S通道还原势垒低于NN三羰基；分别使用对应amine-hydride+acetophenone的参照并保持相同热力学条件。不要求来源冲突的R通道跨家族顺序或数值窗口。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_reduction_order_tBu：tBu取代下S通道NN/NNS还原比较（5分）

参考ID：`reduction_order_tBu`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

在匹配tBu取代、相同底物面和已映射催化剂构型下，实际计算支持NNS二羰基S通道还原势垒低于NN三羰基；分别使用对应amine-hydride+acetophenone的参照并保持相同热力学条件。不要求来源冲突的R通道跨家族顺序或数值窗口。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_stereo_Mn1_Me：Mn1-Me固定构型的S/R偏向（3分）

参考ID：`stereo_Mn1_Me`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

对Mn1-Me的同一催化剂手性构型、组成及热力学条件，配对真实计算支持映射到作者构型时S面还原TS低于R面。镜像催化剂必须相应反转产物面映射；若构型未映射或方向反转则不通过。该定性差异不要求正文或SI的冲突ΔΔG数值命中，也不代表宏观ee。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_stereo_Mn1_tBu：Mn1-tBu固定构型的S/R偏向（3分）

参考ID：`stereo_Mn1_tBu`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

对Mn1-tBu的同一催化剂手性构型、组成及热力学条件，配对真实计算支持映射到作者构型时S面还原TS低于R面。镜像催化剂必须相应反转产物面映射；若构型未映射或方向反转则不通过。该定性差异不要求正文或SI的冲突ΔΔG数值命中，也不代表宏观ee。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_stereo_Mn2_Me：Mn2-Me固定构型的S/R偏向（2分）

参考ID：`stereo_Mn2_Me`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

对Mn2-Me的同一催化剂手性构型、组成及热力学条件，配对真实计算支持映射到作者构型时S面还原TS低于R面。镜像催化剂必须相应反转产物面映射；若构型未映射或方向反转则不通过。该定性差异不要求正文或SI的冲突ΔΔG数值命中，也不代表宏观ee。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_stereo_Mn2_tBu：Mn2-tBu固定构型的S/R偏向（2分）

参考ID：`stereo_Mn2_tBu`；类型：`semantic`；来源证据：`E_RED`, `E_SI`。

对Mn2-tBu的同一催化剂手性构型、组成及热力学条件，配对真实计算支持映射到作者构型时S面还原TS低于R面。镜像催化剂必须相应反转产物面映射；若构型未映射或方向反转则不通过。该定性差异不要求正文或SI的冲突ΔΔG数值命中，也不代表宏观ee。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_cycle_hydrogen_ledger：两半反应闭合的有机转化（5分）

参考ID：`cycle_hydrogen_ledger`；类型：`semantic`；来源证据：`E_CYCLE`, `E_OX`, `E_RED`。

实际氧化和还原态共同支持净反应acetophenone+iPrOH→1-phenylethanol+acetone，并通过相容amido/amine-hydride状态闭合氢、原子和电荷账本。此项新增科学信息是两个局部过程能组成同一转移氢化循环；仅分别列出两条无关路线或示意图不通过，不要求完整真实溶液物种平衡。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_activity_conclusion：最终：配位环境对两半反应的相反影响（10分）

参考ID：`activity_conclusion`；类型：`semantic`；来源证据：`E_CYCLE`, `E_OX`, `E_RED`, `E_SI`。

最终综合实际反应态、家族比较及静息态结果，解释NN三羰基有利于醇氧化而NNS二羰基可有利于S通道酮还原；有效氧化势垒的比较支持在这些候选模型中醇氧化为较慢半循环。必须明确作出受计算支持的选择/解释，不能只列候选或趋势；不得由此断言唯一真实活性种、实际布居或精确速率。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### r_stereo_conclusion：最终：构型条件下的偏向及系综含义（10分）

参考ID：`stereo_conclusion`；类型：`semantic`；来源证据：`E_RED`, `E_CYCLE`, `E_SI`。

最终由实际配对结构/能量与镜像关系推断：固定催化剂构型可产生S/R差异，其镜像对应相反产物映射；无手性配体、单构型结果不能确立实验宏观ee。须以实际映射和比较支持这一系综解释，泛泛写“有局限”不足；不要求额外求真实构型布居或全部镜像反应网络。

完整条件均满足得本项满分，否则0分；共同政策与绑定完整适用。

### 4.2 设计理由（不是评分规则）

题面是解释型问题，核心是候选配位结构、两半反应连接及条件性的家族/立体比较。来源绝对值确实冲突，因此100分全部用于可证伪且实际验证支持的科学命题；这明确替换旧40分冻结的评分设计，不是假称定性趋势完成旧数值项。可独立模型/取代基拆成二元叶子，避免Judge自行比例计分。中间80、最终20；当前版本不设置数值容差，也不强迫Agent解决隐藏来源冲突。

### 4.3 有效性条件

捏造证据或将参考值冒充独立计算、经证明未经授权使用隐藏答案使提交无效；普通计算失败、错误或缺失只使受影响科学项得0分。出版数值冲突及限制见后文，不将其隐藏或作为过程分。


## 5. 全部数值差异与定性依据

### 5.1 全部来源统计

单位kcal/mol。按量ID去重，同一量若有多个实际/来源候选，统计保守取较大的绝对差；0.5、1、2只是描述区间，不是新设容差。

|来源|量ID|平均绝对差|中位绝对差|最大绝对差|≤0.5|0.5–1|1–2|>2|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|SI Esol+gas Gcorr重构|68|0.429385|0.287020|1.747150|53|6|9|0|
|SI打印Gtot重算|68|0.989468|0.974399|3.532086|19|19|23|7|
|正文图表|68|0.451508|0.286197|1.909978|52|6|10|0|

### 5.2 正文68项逐项对照

下列保留每个计算变体；同一ID的多行是实际恢复变体，不是新增独立结果。单位kcal/mol。

|量ID|变体|正文|自算|自算−正文|
|---|---:|---:|---:|---:|
|Mn1-Me/oxidation|0|11.530000|11.505556|-0.024444|
|Mn1-Me/oxidation_reaction|0|-0.330000|-1.373844|-1.043844|
|Mn1-Me/oxidation_reaction|1|-0.330000|-1.373844|-1.043844|
|Mn1-Me/resting|0|-4.340000|-3.986818|+0.353182|
|Mn1-Me/effective|0|15.870000|15.492374|-0.377626|
|Mn1-Me/reduction_S|0|10.390000|10.031280|-0.358720|
|Mn1-Me/reduction_R|0|11.880000|11.824577|-0.055423|
|Mn1-Me/R_minus_S|0|1.490000|1.793297|+0.303297|
|Mn1-tBu/oxidation|0|10.850000|11.911655|+1.061655|
|Mn1-tBu/oxidation_reaction|0|-1.040000|-0.137888|+0.902112|
|Mn1-tBu/oxidation_reaction|1|-1.040000|-0.137888|+0.902112|
|Mn1-tBu/resting|0|-5.170000|-3.446087|+1.723913|
|Mn1-tBu/effective|0|16.020000|15.357742|-0.662258|
|Mn1-tBu/reduction_S|0|10.630000|10.133634|-0.496366|
|Mn1-tBu/reduction_R|0|11.670000|11.445561|-0.224439|
|Mn1-tBu/R_minus_S|0|1.040000|1.311928|+0.271928|
|Mn2-Me/oxidation|0|15.780000|15.502083|-0.277917|
|Mn2-Me/oxidation_reaction|0|6.010000|4.693690|-1.316310|
|Mn2-Me/oxidation_reaction|1|6.010000|4.693690|-1.316310|
|Mn2-Me/resting|0|-4.170000|-4.387150|-0.217150|
|Mn2-Me/effective|0|19.950000|19.889233|-0.060767|
|Mn2-Me/reduction_S|0|8.650000|9.072910|+0.422910|
|Mn2-Me/reduction_R|0|10.520000|10.693021|+0.173021|
|Mn2-Me/R_minus_S|0|1.870000|1.620110|-0.249890|
|Mn2-tBu/oxidation|0|14.780000|14.360511|-0.419489|
|Mn2-tBu/oxidation_reaction|0|5.320000|3.938489|-1.381511|
|Mn2-tBu/oxidation_reaction|1|5.320000|3.938489|-1.381511|
|Mn2-tBu/resting|0|-4.720000|-5.097780|-0.377780|
|Mn2-tBu/effective|0|19.500000|19.458291|-0.041709|
|Mn2-tBu/reduction_S|0|8.160000|8.277950|+0.117950|
|Mn2-tBu/reduction_R|0|10.180000|10.425953|+0.245953|
|Mn2-tBu/R_minus_S|0|2.020000|2.148003|+0.128003|
|Mn1-Me/oxidation_TS1|0|10.120000|9.727728|-0.392272|
|Mn1-Me/oxidation_Int1|0|9.350000|9.197928|-0.152072|
|Mn1-Me/oxidation_TS2|0|11.530000|11.505556|-0.024444|
|Mn1-Me/reduction_S_TS1|0|10.390000|10.031280|-0.358720|
|Mn1-Me/reduction_S_Int1|0|7.860000|7.800014|-0.059986|
|Mn1-Me/reduction_S_TS2|0|9.030000|8.787808|-0.242192|
|Mn1-Me/reduction_R_TS1|0|11.880000|11.824577|-0.055423|
|Mn1-Me/reduction_R_Int1|0|9.600000|9.043530|-0.556470|
|Mn1-Me/reduction_R_TS2|0|9.560000|9.472715|-0.087285|
|Mn1-Me/reduction_product|0|1.910000|2.104829|+0.194829|
|Mn1-tBu/oxidation_TS1|0|8.700000|10.257572|+1.557572|
|Mn1-tBu/oxidation_Int1|0|8.560000|9.980225|+1.420225|
|Mn1-tBu/oxidation_TS2|0|10.850000|11.911655|+1.061655|
|Mn1-tBu/reduction_S_TS1|0|10.630000|10.133634|-0.496366|
|Mn1-tBu/reduction_S_Int1|0|8.500000|8.672007|+0.172007|
|Mn1-tBu/reduction_S_TS2|0|9.240000|9.179857|-0.060143|
|Mn1-tBu/reduction_R_TS1|0|11.670000|11.445561|-0.224439|
|Mn1-tBu/reduction_R_Int1|0|9.670000|9.541993|-0.128007|
|Mn1-tBu/reduction_R_TS2|0|9.360000|9.121580|-0.238420|
|Mn1-tBu/reduction_product|0|2.620000|0.868874|-1.751126|
|Mn2-Me/oxidation_TS1|0|8.640000|8.286527|-0.353473|
|Mn2-Me/oxidation_Int1|0|9.100000|8.334192|-0.765808|
|Mn2-Me/oxidation_TS2|0|15.780000|15.502083|-0.277917|
|Mn2-Me/reduction_S_TS1|0|8.650000|9.072910|+0.422910|
|Mn2-Me/reduction_S_Int1|0|2.180000|2.931023|+0.751023|
|Mn2-Me/reduction_S_TS2|0|1.890000|1.971750|+0.081750|
|Mn2-Me/reduction_R_TS1|0|10.520000|10.693021|+0.173021|
|Mn2-Me/reduction_R_Int1|0|1.820000|2.114477|+0.294477|
|Mn2-Me/reduction_R_TS2|0|1.800000|1.972001|+0.172001|
|Mn2-Me/reduction_product|0|-4.430000|-3.962704|+0.467296|
|Mn2-tBu/oxidation_TS1|0|6.890000|7.022327|+0.132327|
|Mn2-tBu/oxidation_Int1|0|9.270000|7.360022|-1.909978|
|Mn2-tBu/oxidation_TS2|0|14.780000|14.360511|-0.419489|
|Mn2-tBu/reduction_S_TS1|0|8.160000|8.277950|+0.117950|
|Mn2-tBu/reduction_S_Int1|0|1.900000|1.662720|-0.237280|
|Mn2-tBu/reduction_S_TS2|0|0.800000|1.110349|+0.310349|
|Mn2-tBu/reduction_R_TS1|0|10.180000|10.425953|+0.245953|
|Mn2-tBu/reduction_R_Int1|0|1.130000|1.311039|+0.181039|
|Mn2-tBu/reduction_R_TS2|0|0.560000|0.892816|+0.332816|
|Mn2-tBu/reduction_product|0|-3.740000|-3.207503|+0.532497|

### 5.3 不一致结果必须保留

- 正文最大差：Mn2-tBu氧化Int1，正文9.270000，自算7.360022，差−1.909978；SI打印Gtot重算9.163521、SI重构7.265556。不能仅展示更接近自算的来源。
- SI打印Gtot最大差：Mn1-Me还原S通道TS2，12.319894对8.787808，差−3.532086；正文9.030000，对正文差−0.242192。
- Mn1-tBu静息态−5.170000对−3.446087，差+1.723913；还原产物反应自由能2.620000对0.868874，差−1.751126。
- Mn1氧化Int1的tBu−Me，正文8.56−9.35=−0.79，自算9.980225−9.197928=+0.782297；两套SI也支持负号。这一局部顺序确实没有复现，不归因于来源冲突。当前家族排序项不把该局部取代基顺序作为必须保持的结论，本文也不把它写成相符。
- 其他检测到的细顺序反转、来源相关符号变化和负的TS–Int1自由能差列于下表。它们仍是实际差异，不因验收而删除。

|关系|正文或注明来源|自算|解释|
|---|---:|---:|---|
|Mn1 tBu-minus-Me effective|+0.150000|-0.134632|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me oxidation|-0.680000|+0.406099|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me oxidation_Int1|-0.790000|+0.782297|源方向一致，真实局部反转|
|Mn2 tBu-minus-Me oxidation_Int1|+0.170000|-0.974171|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me oxidation_TS1|-1.420000|+0.529844|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me oxidation_TS2|-0.680000|+0.406099|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me oxidation_reaction|-0.710000|+1.235955|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me reduction_product|+0.710000|-1.235955|相对正文反转；来源彼此也有方向冲突|
|Mn1 tBu-minus-Me resting|-0.830000|+0.540731|相对正文反转；来源彼此也有方向冲突|
|Mn1-tBu/oxidation_reaction（SI打印）|+0.067771|-0.137888|来源相关符号变化，正文为−1.04|
|Mn1-tBu/reduction_R_TS2 G(TS)−G(Int1)|未列统一来源|-0.420413|不据此认定电子PES无势垒|
|Mn2-Me/reduction_S_TS2 G(TS)−G(Int1)|未列统一来源|-0.959274|不据此认定电子PES无势垒|
|Mn2-Me/reduction_R_TS2 G(TS)−G(Int1)|未列统一来源|-0.142476|不据此认定电子PES无势垒|
|Mn2-tBu/reduction_S_TS2 G(TS)−G(Int1)|未列统一来源|-0.552371|不据此认定电子PES无势垒|
|Mn2-tBu/reduction_R_TS2 G(TS)−G(Int1)|未列统一来源|-0.418223|不据此认定电子PES无势垒|

### 5.4 定性分析结论及数值依据

#### NN三羰基候选比NNS二羰基候选更有利于醇氧化

A=Mn1 NN三羰基，B=Mn2 NNS二羰基。以下比较B−A，均为正，作者核心家族结论保持。

|取代基/参考|正文B−A|自算B−A|
|---|---:|---:|
|Me/分离反应物|+4.250000|+3.996526|
|Me/静息态|+4.080000|+4.396858|
|tBu/分离反应物|+3.930000|+2.448856|
|tBu/静息态|+3.480000|+4.100549|

#### NNS降低S通道还原势垒

|取代基|正文B(S)−A(S)|自算B(S)−A(S)|
|---|---:|---:|
|Me|-1.740000|-0.958370|
|tBu|-2.470000|-1.855684|

两者均负，支持当前S通道结论。R通道跨家族顺序不具来源稳健性，不扩写为必须相符的结论。

#### 固定构型S通道低于R通道

|模型|正文TS1 R−S|自算TS1 R−S|差|
|---|---:|---:|---:|
|Mn1-Me|1.490000|1.793297|+0.303297|
|Mn1-tBu|1.040000|1.311928|+0.271928|
|Mn2-Me|1.870000|1.620110|-0.249890|
|Mn2-tBu|2.020000|2.148003|+0.128003|

完整TS1/TS2最高相对能包络也核对了四模型×三种来源及自算，共16项检查，方向均保持S较低。结论仅限固定构型；镜像催化剂需反转面映射，不证明宏观ee。此前将2.148003对2.02称为TS2是标签错误，实际原始账本为TS1_R−TS1_S，本表已更正。

#### 静息态修正后氧化为更困难的半循环

|模型|自算静息态稳定化|有效氧化|S还原|R还原|氧化−较高还原通道|
|---|---:|---:|---:|---:|---:|
|Mn1-Me|-3.986818|15.492374|10.031280|11.824577|3.667797|
|Mn1-tBu|-3.446087|15.357742|10.133634|11.445561|3.912181|
|Mn2-Me|-4.387150|19.889233|9.072910|10.693021|9.196212|
|Mn2-tBu|-5.097780|19.458291|8.277950|10.425953|9.032338|

此结果支持作者在这些候选模型下的“醇氧化是更困难半循环”解释；未声称直接证明实际速率、完整微观动力学或真实催化剂种群。

#### 反应路线与当前11项科学内容覆盖

代表氧化O–H→C–H转移连接共同Int1；代表还原氢化物到C、质子到O的序列与完整原子/氢账本支持两半反应耦合。有效驻点和代表连接支持当前路线，不能写成所有S/R路径与构象的完整双向IRC全部成功。

|评估项|计算证据与结论|
|---|---|
|K_ACTIVE|完整A/B候选身份、CO配位、原子/电荷及披露自旋条件；不证明唯一活性种群。|
|K_OX|四模型O–H/C–H转移相关有效驻点和能量均已计算，差值完整列出；数值评分来源另保留。|
|K_REST|四个静息态稳定化与零点修正实际计算，区分有效势垒及分离反应物坐标。|
|K_RED|四模型S/R相关驻点能量已计算，代表还原路线有连接证据。|
|K_SR|固定构型四对TS1的R−S均有真实计算，不外推bulk ee。|
|K_OX_ORDER|Me和tBu两对均NN比NNS氧化更容易；Me/tBu局部反转未删除。|
|K_RED_ORDER|Me和tBu两对S还原均NNS低于NN。|
|K_SR_ORDER|固定构型S<R及完整TS包络方向一致。|
|K_PATH|实际中间态、氢迁移和代表端点连接支持两半反应；IRC前缀/位移实施限制保留。|
|C_ACTIVITY|配位形式改变氧化/还原难易分工，静息态修正后氧化较困难，与当前核心结论一致。|
|C_STEREO|指定构型内能量偏向支持S通道；同时明确镜像与总体布居限制。|

## 6. 专家需裁定的问题与接受边界

当前范围已有计算支持，不能笼统描述成“只完成 60%”或“待计算才可判断”。同样不能因 68/68 覆盖率、平均偏差较小或定性接受，称全部精确通过。68 是比较量 ID 数，72 是含恢复变体的自算行数，53 是有效 Opt/Freq→SP 链数，22 是端点阶段数，不是 22 个独立物种。

请专家重点裁定：

1. 正文、SI 打印 Gtot、Esol+gasGcorr 重构三种定义及重复 Gcorr 冲突如何协调，哪一组能成为可评分参照。当前保留 **R_OX/R_REST/R_RED/R_SR 各 10 分，共 40 分**，不授予、不删项、不重新归一化。
2. Mn1 氧化 Int1 的 tBu−Me 来源 −0.79、自算 +0.782297 是真实细排序反转；两套 SI 同支持来源负号，不能归咎来源冲突。专家是否同意它不改变当前规则要求的 NN/NNS 家族与固定构型 S/R 核心结论。
3. 中性单重态、未经作者公开的网格／阈值是否足以支撑限定候选模型比较。此接受不证明真实溶液种群，也不证明作者隐藏设置完全一致。
4. TS1 模式位移加优化、TS2 反向 17 个收敛 IRC 点加无约束最低点，是否满足当前题面的代表连接范围。failed corrector18 与另一 S 反向 corrector15 没有被改为成功，不主张所有路径完成完整双向 IRC。
5. 旧独立验收正文把 2.148002580 对 2.02 写成 TS2；现行 03:24 参考和原始账本明确更正为 **TS1_R−TS1_S**，本材料采用后者。全文 TS1/TS2 最大能量包络已另查，不能把标签修正理解成新计算。

父级 02:34 已接受两模式的定性暂定验证；03:24 现行参考按用户确认记为当前范围定性计算通过。两者均保持 `quantitative_strict_pass=false`、`all_results_identical=false`、40 分来源资格保留。本文仅归档这些既有决定。

## 7. 原始证据、完整多来源账本与任务包

### 7.1 原始日志索引

#### 53条有效能量链

各链的Opt/Freq和SP原始路径、作业ID及虚频数如下；哈希及能量解析详情在独立数值复核JSON。

|案例|作业ID|虚频数|Opt/Freq日志|SP日志|
|---|---|---:|---|---|
|CH3_CHOH_CH3|hpc-job-09ffa2f6-e931-4a2d-8a82-86f4c8444d82|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CHOH_CH3/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CHOH_CH3/native/sp.log)|
|Ph_CO_CH3|hpc-job-d7e67241-3062-42c1-ac4e-8cb9d203b2ab|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CO_CH3/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CO_CH3/native/sp.log)|
|Int1_Mn1_Me|hpc-job-2bf6dcf6-0630-4fe0-a2cf-e2f115466fb1|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me/native/sp.log)|
|Int1_Mn1_Me_2H_Acetophenone_R|hpc-job-b3f25923-acb1-4980-a0f0-448403690bff|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn1_Me_2H_Acetophenone_S|hpc-job-381e139f-89b3-45bc-95d2-41ef46c90dcb|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_S/native/sp.log)|
|Int1_Mn1_tBu|hpc-job-9042d062-dbb9-4e23-9dcd-f866f840ab1c|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu/native/sp.log)|
|Int1_Mn1_tBu_2H_Acetophenone_R|hpc-job-7f8b47cf-d1a1-4eb6-b766-ac95349527d7|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn1_tBu_2H_Acetophenone_S|hpc-job-513cdb90-e6e2-4139-8283-68f3ca6dff8d|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_S/native/sp.log)|
|Int1_Mn2_Me|hpc-job-0ee27abf-3187-44e4-9616-28616b0bc5cf|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me/native/sp.log)|
|Int1_Mn2_Me_2H_Acetophenone_R|hpc-job-776ce936-88e5-472c-8453-c04a4b4e9193|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn2_Me_2H_Acetophenone_S|hpc-job-a82d2aed-644f-44a0-9535-92a93a7f6bb8|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_S/native/sp.log)|
|Int1_Mn2_tBu|hpc-job-6181117c-94d0-4db9-addd-d57c148ea681|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu/native/sp.log)|
|Int1_Mn2_tBu_2H_Acetophenone_R|hpc-job-d95223f0-c567-4478-a4b7-b7f86cf73a15|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn2_tBu_2H_Acetophenone_S|hpc-job-07125833-db5b-4090-bed6-8a9d282af917|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_S/native/sp.log)|
|Mn1_Me|hpc-job-5bab39c9-a669-41dd-929a-317b43c27a48|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me/native/sp.log)|
|Mn1_Me_2H|hpc-job-bab47977-8460-48f5-ae84-b4c935174c40|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me_2H/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me_2H/native/sp.log)|
|Mn1_tBu|hpc-job-53fa7bb7-9e95-4406-a644-381e61c9cfa7|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu/native/sp.log)|
|Mn1_tBu_2H|hpc-job-294f88da-4ebb-41c6-a28f-7c7768d2c2ad|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu_2H/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu_2H/native/sp.log)|
|Mn2_Me|hpc-job-e8654993-a30b-4c1a-b909-25c5e82c6318|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me/native/sp.log)|
|Mn2_Me_2H|hpc-job-1a990a8e-2d2a-429b-bc7e-354cce3f33dc|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me_2H/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me_2H/native/sp.log)|
|Mn2_tBu|hpc-job-d26c4a5e-8adc-4109-852b-07300bc670c6|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu/native/sp.log)|
|Mn2_tBu_2H|hpc-job-78fd82c6-dea6-4da8-a1a6-dd0296e05ac7|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu_2H/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu_2H/native/sp.log)|
|Ph_CHOH_CH3|hpc-job-be37304d-45fe-4cd9-91a1-fed5fa0aab53|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CHOH_CH3/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CHOH_CH3/native/sp.log)|
|TS1_Mn1_Me|hpc-job-7b369dea-db1b-4feb-bd44-1f4907e0a5b8|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me/native/sp.log)|
|TS1_Mn1_Me_2H_Acetophenone_R|hpc-job-50523fdf-8f19-4efe-8c26-f39254c8b5db|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn1_Me_2H_Acetophenone_S|hpc-job-6001a1a4-f1a7-4d8c-9e6e-e26f99bdb2f2|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_S/native/sp.log)|
|TS1_Mn1_tBu|hpc-job-5ae4a341-e735-4817-881a-931d2f3da3c7|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu/native/sp.log)|
|TS1_Mn1_tBu_2H_Acetophenone_R|hpc-job-29e50f45-8074-457a-a2ae-f759acb31bd5|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn1_tBu_2H_Acetophenone_S|hpc-job-8911546c-afd9-4fb2-85aa-f46b6dfe311a|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_S/native/sp.log)|
|TS1_Mn2_Me|hpc-job-47eac770-87e7-4790-9df9-ed0bf9ccda87|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me/native/sp.log)|
|TS1_Mn2_Me_2H_Acetophenone_R|hpc-job-16ec23b8-e548-42ac-ba3e-b7fba3f7a764|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn2_Me_2H_Acetophenone_S|hpc-job-de76c74c-a1ee-4301-aec7-8964898ad92e|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_S/native/sp.log)|
|TS1_Mn2_tBu|hpc-job-39d21c0e-149b-4f9d-8b6e-78a23ec78ccb|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu/native/sp.log)|
|TS1_Mn2_tBu_2H_Acetophenone_R|hpc-job-3f46b4ba-3d61-4cea-bf56-c7c5b302d4e2|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn2_tBu_2H_Acetophenone_S|hpc-job-bd6d878a-9d13-4e9d-a7ce-039037685ddc|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn1_Me|hpc-job-8b7d28b7-2d34-4444-8b6d-08a7db83b056|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me/native/sp.log)|
|TS2_Mn1_Me_2H_Acetophenone_S|hpc-job-aaf15d8c-66f6-4fea-9213-62876d16540f|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn1_tBu|hpc-job-d8f245d4-f0ac-46d0-b7fc-581e5f8fd651|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu/native/sp.log)|
|TS2_Mn1_tBu_2H_Acetophenone_R|hpc-job-f9e6ebca-e195-4b6a-92a1-8b05d2b0fe39|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_R/native/sp.log)|
|TS2_Mn1_tBu_2H_Acetophenone_S|hpc-job-9d06465e-e4ad-41ac-82d8-b404f06940d2|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn2_Me|hpc-job-00f7f4e0-5296-403e-a5c4-ea79c26e8dac|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me/native/sp.log)|
|TS2_Mn2_Me_2H_Acetophenone_R|hpc-job-7ccf2e4d-da84-43b2-bfd0-48aa876bbe2c|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_R/native/sp.log)|
|TS2_Mn2_Me_2H_Acetophenone_S|hpc-job-63ef59a9-3566-473c-9750-34a742cabf90|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn2_tBu|hpc-job-567a04fa-eea1-4ce5-9027-4f58d5f21cda|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu/native/sp.log)|
|TS2_Mn2_tBu_2H_Acetophenone_R|hpc-job-ec2924ff-6bf6-467f-96d0-183b8c612333|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_R/native/sp.log)|
|TS2_Mn2_tBu_2H_Acetophenone_S|hpc-job-f2ec90ba-749b-4557-b550-f8bd9cd26b24|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_S/native/sp.log)|
|VIII_Me_OCHMe2|hpc-job-60f55f94-a32b-49bb-b7d7-fabd40da9d31|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_Me_OCHMe2/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_Me_OCHMe2/native/sp.log)|
|VIII_tBu_OCHMe2|hpc-job-68f843ff-b133-4ef4-9fed-caf621a56096|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_tBu_OCHMe2/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_tBu_OCHMe2/native/sp.log)|
|VII_Me_OCHMe2|hpc-job-6bfbcfc5-ff61-4d24-8ee5-bf0d8b87ea33|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_Me_OCHMe2/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_Me_OCHMe2/native/sp.log)|
|VII_tBu_OCHMe2|hpc-job-6c08b712-adda-4755-b40f-5a94df73e6ad|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_tBu_OCHMe2/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_tBu_OCHMe2/native/sp.log)|
|CH3_CO_CH3_modeminus|hpc-job-0e401f7c-68ba-4cff-87af-3b70ed8fff03|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeminus/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeminus/native/sp.log)|
|CH3_CO_CH3_modeplus|hpc-job-aa50b3b9-f41c-42ef-bc2a-384173577778|0|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeplus/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeplus/native/sp.log)|
|TS2_Mn1_Me_2H_Acetophenone_R|hpc-job-4eaa60f8-11ae-4478-b2ab-a79e2ae79582|1|[Opt/Freq](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/followup_20261017/TS2_Mn1_Me_2H_Acetophenone_R_recover01/native/optfreq.log)|[SP](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/followup_20261017/TS2_Mn1_Me_2H_Acetophenone_R_recover01/native/sp.log)|

#### 结果账本与路径验收

- [68量物种账本及恢复变体](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261019T0035Z/new_group_03/paper_d142c9737f95225b/energy_comparisons.json)
- [全部217行来源/变体对照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/new_group_03/quantitative_comparison_supplement.json)
- [定性关系及全部反转](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/new_group_03/mn_qualitative_relations.json)
- [106日志重读与独立能量重算](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/numerical_audit_20261020/numerical_reaudit.json)
- [详细偏差复核](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/numerical_audit_20261020/计算结果与论文逐项差异复核.md)
- [代表氧化共同Int1端点验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/storage_recovery_20261019T0530Z/new_group_03/endpoint_acceptance.json)
- [同几何审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/same_geometry_protocol_audit.json)
- [此前108份该论文日志独立审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/acceptance_native_audit.json)
- [SI Table S2组装审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/source/table_S2_assembly_audit.json)

本次复用成功计算，没有新HPC提交或重复量子化学计算。

## 附录A：全部217行数值来源与计算变体

每个实际变体和来源候选均保留；编号从0开始，与源JSON一致。差值为自算−来源。正文=main_figure，打印=SI打印Gtot，重构=SI Esol+气相Gcorr。单位kcal/mol。

|量ID|自算变体|来源|来源候选|来源值|自算值|差值|
|---|---:|---|---:|---:|---:|---:|
|Mn1-Me/oxidation|0|正文|0|11.530000000|11.505556261|-0.024443739|
|Mn1-Me/oxidation|0|打印|0|10.527726445|11.505556261|+0.977829815|
|Mn1-Me/oxidation|0|重构|0|11.534628147|11.505556261|-0.029071886|
|Mn1-Me/oxidation_reaction|0|正文|0|-0.330000000|-1.373843515|-1.043843515|
|Mn1-Me/oxidation_reaction|0|打印|0|-0.608684190|-1.373843515|-0.765159325|
|Mn1-Me/oxidation_reaction|0|重构|0|-0.328689462|-1.373843515|-1.045154052|
|Mn1-Me/oxidation_reaction|1|正文|0|-0.330000000|-1.373843515|-1.043843515|
|Mn1-Me/oxidation_reaction|1|打印|0|-0.608684190|-1.373843515|-0.765159325|
|Mn1-Me/oxidation_reaction|1|重构|0|-0.328689462|-1.373843515|-1.045154052|
|Mn1-Me/resting|0|正文|0|-4.340000000|-3.986818065|+0.353181935|
|Mn1-Me/resting|0|打印|0|-2.916036526|-3.986818065|-1.070781539|
|Mn1-Me/resting|0|重构|0|-4.338412251|-3.986818065|+0.351594186|
|Mn1-Me/effective|0|正文|0|15.870000000|15.492374325|-0.377625675|
|Mn1-Me/effective|0|打印|0|13.443762971|15.492374325|+2.048611354|
|Mn1-Me/effective|0|重构|0|15.873040398|15.492374325|-0.380666072|
|Mn1-Me/reduction_S|0|正文|0|10.390000000|10.031280483|-0.358719517|
|Mn1-Me/reduction_S|0|打印|0|10.313118205|10.031280483|-0.281837722|
|Mn1-Me/reduction_S|0|重构|0|10.391619640|10.031280483|-0.360339157|
|Mn1-Me/reduction_R|0|正文|0|11.880000000|11.824577057|-0.055422943|
|Mn1-Me/reduction_R|0|打印|0|12.795545684|11.824577057|-0.970968627|
|Mn1-Me/reduction_R|0|重构|0|11.880825124|11.824577057|-0.056248066|
|Mn1-Me/R_minus_S|0|正文|0|1.490000000|1.793296575|+0.303296575|
|Mn1-Me/R_minus_S|0|打印|0|2.482427479|1.793296575|-0.689130905|
|Mn1-Me/R_minus_S|0|重构|0|1.489205483|1.793296575|+0.304091091|
|Mn1-tBu/oxidation|0|正文|0|10.850000000|11.911655292|+1.061655292|
|Mn1-tBu/oxidation|0|打印|0|10.739824648|11.911655292|+1.171830645|
|Mn1-tBu/oxidation|0|重构|0|10.849764307|11.911655292|+1.061890985|
|Mn1-tBu/oxidation_reaction|0|正文|0|-1.040000000|-0.137888304|+0.902111696|
|Mn1-tBu/oxidation_reaction|0|打印|0|0.067771023|-0.137888304|-0.205659327|
|Mn1-tBu/oxidation_reaction|0|重构|0|-1.035265130|-0.137888304|+0.897376826|
|Mn1-tBu/oxidation_reaction|1|正文|0|-1.040000000|-0.137888304|+0.902111696|
|Mn1-tBu/oxidation_reaction|1|打印|0|0.067771023|-0.137888304|-0.205659327|
|Mn1-tBu/oxidation_reaction|1|重构|0|-1.035265130|-0.137888304|+0.897376826|
|Mn1-tBu/resting|0|正文|0|-5.170000000|-3.446086875|+1.723913125|
|Mn1-tBu/resting|0|打印|0|-1.869978233|-3.446086875|-1.576108643|
|Mn1-tBu/resting|0|重构|0|-5.167979775|-3.446086875|+1.721892900|
|Mn1-tBu/effective|0|正文|0|16.020000000|15.357742168|-0.662257832|
|Mn1-tBu/effective|0|打印|0|12.609802880|15.357742168|+2.747939288|
|Mn1-tBu/effective|0|重构|0|16.017744082|15.357742168|-0.660001915|
|Mn1-tBu/reduction_S|0|正文|0|10.630000000|10.133633553|-0.496366447|
|Mn1-tBu/reduction_S|0|打印|0|9.142185527|10.133633553|+0.991448026|
|Mn1-tBu/reduction_S|0|重构|0|10.629382980|10.133633553|-0.495749427|
|Mn1-tBu/reduction_R|0|正文|0|11.670000000|11.445561335|-0.224438665|
|Mn1-tBu/reduction_R|0|打印|0|11.067384593|11.445561335|+0.378176742|
|Mn1-tBu/reduction_R|0|重构|0|11.668915174|11.445561335|-0.223353840|
|Mn1-tBu/R_minus_S|0|正文|0|1.040000000|1.311927782|+0.271927782|
|Mn1-tBu/R_minus_S|0|打印|0|1.925199066|1.311927782|-0.613271284|
|Mn1-tBu/R_minus_S|0|重构|0|1.039532195|1.311927782|+0.272395588|
|Mn2-Me/oxidation|0|正文|0|15.780000000|15.502082525|-0.277917475|
|Mn2-Me/oxidation|0|打印|0|16.552444905|15.502082525|-1.050362381|
|Mn2-Me/oxidation|0|重构|0|15.781800520|15.502082525|-0.279717995|
|Mn2-Me/oxidation_reaction|0|正文|0|6.010000000|4.693689917|-1.316310083|
|Mn2-Me/oxidation_reaction|0|打印|0|6.759532054|4.693689917|-2.065842136|
|Mn2-Me/oxidation_reaction|0|重构|0|6.014678308|4.693689917|-1.320988391|
|Mn2-Me/oxidation_reaction|1|正文|0|6.010000000|4.693689917|-1.316310083|
|Mn2-Me/oxidation_reaction|1|打印|0|6.759532054|4.693689917|-2.065842136|
|Mn2-Me/oxidation_reaction|1|重构|0|6.014678308|4.693689917|-1.320988391|
|Mn2-Me/resting|0|正文|0|-4.170000000|-4.387150283|-0.217150283|
|Mn2-Me/resting|0|打印|0|-1.915158915|-4.387150283|-2.471991369|
|Mn2-Me/resting|0|重构|0|-4.170114210|-4.387150283|-0.217036074|
|Mn2-Me/effective|0|正文|0|19.950000000|19.889232808|-0.060767192|
|Mn2-Me/effective|0|打印|0|18.467603820|19.889232808|+1.421628988|
|Mn2-Me/effective|0|重构|0|19.951914729|19.889232808|-0.062681921|
|Mn2-Me/reduction_S|0|正文|0|8.650000000|9.072910363|+0.422910363|
|Mn2-Me/reduction_S|0|打印|0|8.509028467|9.072910363|+0.563881896|
|Mn2-Me/reduction_S|0|重构|0|8.652477133|9.072910363|+0.420433230|
|Mn2-Me/reduction_R|0|正文|0|10.520000000|10.693020598|+0.173020598|
|Mn2-Me/reduction_R|0|打印|0|11.732544635|10.693020598|-1.039524037|
|Mn2-Me/reduction_R|0|重构|0|10.523835886|10.693020598|+0.169184712|
|Mn2-Me/R_minus_S|0|正文|0|1.870000000|1.620110235|-0.249889765|
|Mn2-Me/R_minus_S|0|打印|0|3.223516168|1.620110235|-1.603405933|
|Mn2-Me/R_minus_S|0|重构|0|1.871358753|1.620110235|-0.251248518|
|Mn2-tBu/oxidation|0|正文|0|14.780000000|14.360511014|-0.419488986|
|Mn2-tBu/oxidation|0|打印|0|15.680834246|14.360511014|-1.320323232|
|Mn2-tBu/oxidation|0|重构|0|14.778412871|14.360511014|-0.417901857|
|Mn2-tBu/oxidation_reaction|0|正文|0|5.320000000|3.938488540|-1.381511460|
|Mn2-tBu/oxidation_reaction|0|打印|0|5.745476744|3.938488540|-1.806988204|
|Mn2-tBu/oxidation_reaction|0|重构|0|5.317766287|3.938488540|-1.379277747|
|Mn2-tBu/oxidation_reaction|1|正文|0|5.320000000|3.938488540|-1.381511460|
|Mn2-tBu/oxidation_reaction|1|打印|0|5.745476744|3.938488540|-1.806988204|
|Mn2-tBu/oxidation_reaction|1|重构|0|5.317766287|3.938488540|-1.379277747|
|Mn2-tBu/resting|0|正文|0|-4.720000000|-5.097779663|-0.377779663|
|Mn2-tBu/resting|0|打印|0|-4.566386442|-5.097779663|-0.531393220|
|Mn2-tBu/resting|0|重构|0|-4.717741727|-5.097779663|-0.380037935|
|Mn2-tBu/effective|0|正文|0|19.500000000|19.458290677|-0.041709323|
|Mn2-tBu/effective|0|打印|0|20.247220688|19.458290677|-0.788930011|
|Mn2-tBu/effective|0|重构|0|19.496154599|19.458290677|-0.037863922|
|Mn2-tBu/reduction_S|0|正文|0|8.160000000|8.277949986|+0.117949986|
|Mn2-tBu/reduction_S|0|打印|0|8.402979366|8.277949986|-0.125029380|
|Mn2-tBu/reduction_S|0|重构|0|8.158062418|8.277949986|+0.119887568|
|Mn2-tBu/reduction_R|0|正文|0|10.180000000|10.425952566|+0.245952566|
|Mn2-tBu/reduction_R|0|打印|0|11.313368307|10.425952566|-0.887415740|
|Mn2-tBu/reduction_R|0|重构|0|10.179960695|10.425952566|+0.245991872|
|Mn2-tBu/R_minus_S|0|正文|0|2.020000000|2.148002580|+0.128002580|
|Mn2-tBu/R_minus_S|0|打印|0|2.910388940|2.148002580|-0.762386360|
|Mn2-tBu/R_minus_S|0|重构|0|2.021898277|2.148002580|+0.126104303|
|Mn1-Me/oxidation_TS1|0|正文|0|10.120000000|9.727727794|-0.392272206|
|Mn1-Me/oxidation_TS1|0|打印|0|8.441257444|9.727727794|+1.286470350|
|Mn1-Me/oxidation_TS1|0|重构|0|10.118653019|9.727727794|-0.390925225|
|Mn1-Me/oxidation_Int1|0|正文|0|9.350000000|9.197927821|-0.152072179|
|Mn1-Me/oxidation_Int1|0|打印|0|10.222129331|9.197927821|-1.024201511|
|Mn1-Me/oxidation_Int1|0|重构|0|9.348573393|9.197927821|-0.150645572|
|Mn1-Me/oxidation_TS2|0|正文|0|11.530000000|11.505556261|-0.024443739|
|Mn1-Me/oxidation_TS2|0|打印|0|10.527726445|11.505556261|+0.977829815|
|Mn1-Me/oxidation_TS2|0|重构|0|11.534628147|11.505556261|-0.029071886|
|Mn1-Me/reduction_S_TS1|0|正文|0|10.390000000|10.031280483|-0.358719517|
|Mn1-Me/reduction_S_TS1|0|打印|0|10.313118205|10.031280483|-0.281837722|
|Mn1-Me/reduction_S_TS1|0|重构|0|10.391619640|10.031280483|-0.360339157|
|Mn1-Me/reduction_S_Int1|0|正文|0|7.860000000|7.800013670|-0.059986330|
|Mn1-Me/reduction_S_Int1|0|打印|0|10.584202298|7.800013670|-2.784188628|
|Mn1-Me/reduction_S_Int1|0|重构|0|8.158062419|7.800013670|-0.358048748|
|Mn1-Me/reduction_S_Int1|0|重构|1|7.862505456|7.800013670|-0.062491786|
|Mn1-Me/reduction_S_TS2|0|正文|0|9.030000000|8.787807709|-0.242192291|
|Mn1-Me/reduction_S_TS2|0|打印|0|12.319893503|8.787807709|-3.532085794|
|Mn1-Me/reduction_S_TS2|0|重构|0|9.026159025|8.787807709|-0.238351315|
|Mn1-Me/reduction_R_TS1|0|正文|0|11.880000000|11.824577057|-0.055422943|
|Mn1-Me/reduction_R_TS1|0|打印|0|12.795545684|11.824577057|-0.970968627|
|Mn1-Me/reduction_R_TS1|0|重构|0|11.880825124|11.824577057|-0.056248066|
|Mn1-Me/reduction_R_Int1|0|正文|0|9.600000000|9.043530370|-0.556469630|
|Mn1-Me/reduction_R_Int1|0|打印|0|11.423809974|9.043530370|-2.380279604|
|Mn1-Me/reduction_R_Int1|0|重构|0|9.600141941|9.043530370|-0.556611571|
|Mn1-Me/reduction_R_TS2|0|正文|0|9.560000000|9.472715475|-0.087284525|
|Mn1-Me/reduction_R_TS2|0|打印|0|9.227526815|9.472715475|+0.245188660|
|Mn1-Me/reduction_R_TS2|0|重构|0|9.562052115|9.472715475|-0.089336641|
|Mn1-Me/reduction_product|0|正文|0|1.910000000|2.104829301|+0.194829301|
|Mn1-Me/reduction_product|0|打印|0|1.946534388|2.104829301|+0.158294913|
|Mn1-Me/reduction_product|0|重构|0|1.909448578|2.104829301|+0.195380723|
|Mn1-tBu/oxidation_TS1|0|正文|0|8.700000000|10.257571694|+1.557571694|
|Mn1-tBu/oxidation_TS1|0|打印|0|9.056844238|10.257571694|+1.200727456|
|Mn1-tBu/oxidation_TS1|0|重构|0|8.695085026|10.257571694|+1.562486668|
|Mn1-tBu/oxidation_Int1|0|正文|0|8.560000000|9.980225057|+1.420225057|
|Mn1-tBu/oxidation_Int1|0|打印|0|9.570774497|9.980225057|+0.409450559|
|Mn1-tBu/oxidation_Int1|0|重构|0|8.556468184|9.980225057|+1.423756873|
|Mn1-tBu/oxidation_TS2|0|正文|0|10.850000000|11.911655292|+1.061655292|
|Mn1-tBu/oxidation_TS2|0|打印|0|10.739824648|11.911655292|+1.171830645|
|Mn1-tBu/oxidation_TS2|0|重构|0|10.849764307|11.911655292|+1.061890985|
|Mn1-tBu/reduction_S_TS1|0|正文|0|10.630000000|10.133633553|-0.496366447|
|Mn1-tBu/reduction_S_TS1|0|打印|0|9.142185527|10.133633553|+0.991448026|
|Mn1-tBu/reduction_S_TS1|0|重构|0|10.629382980|10.133633553|-0.495749427|
|Mn1-tBu/reduction_S_Int1|0|正文|0|8.500000000|8.672007110|+0.172007110|
|Mn1-tBu/reduction_S_Int1|0|打印|0|8.492713221|8.672007110|+0.179293889|
|Mn1-tBu/reduction_S_Int1|0|重构|0|8.502439618|8.672007110|+0.169567493|
|Mn1-tBu/reduction_S_TS2|0|正文|0|9.240000000|9.179856803|-0.060143197|
|Mn1-tBu/reduction_S_TS2|0|打印|0|8.480163032|9.179856803|+0.699693771|
|Mn1-tBu/reduction_S_TS2|0|重构|0|9.242398790|9.179856803|-0.062541987|
|Mn1-tBu/reduction_R_TS1|0|正文|0|11.670000000|11.445561335|-0.224438665|
|Mn1-tBu/reduction_R_TS1|0|打印|0|11.067384593|11.445561335|+0.378176742|
|Mn1-tBu/reduction_R_TS1|0|重构|0|11.668915174|11.445561335|-0.223353840|
|Mn1-tBu/reduction_R_Int1|0|正文|0|9.670000000|9.541992520|-0.128007480|
|Mn1-tBu/reduction_R_Int1|0|打印|0|9.482923171|9.541992520|+0.059069349|
|Mn1-tBu/reduction_R_Int1|0|重构|0|9.673874304|9.541992520|-0.131881783|
|Mn1-tBu/reduction_R_TS2|0|正文|0|9.360000000|9.121579998|-0.238420002|
|Mn1-tBu/reduction_R_TS2|0|打印|0|10.294292921|9.121579998|-1.172712923|
|Mn1-tBu/reduction_R_TS2|0|重构|0|9.357421276|9.121579998|-0.235841278|
|Mn1-tBu/reduction_product|0|正文|0|2.620000000|0.868874090|-1.751125910|
|Mn1-tBu/reduction_product|0|打印|0|1.270079175|0.868874090|-0.401205085|
|Mn1-tBu/reduction_product|0|重构|0|2.616024246|0.868874090|-1.747150156|
|Mn2-Me/oxidation_TS1|0|正文|0|8.640000000|8.286526786|-0.353473214|
|Mn2-Me/oxidation_TS1|0|打印|0|8.874238981|8.286526786|-0.587712195|
|Mn2-Me/oxidation_TS1|0|重构|0|8.641370215|8.286526786|-0.354843430|
|Mn2-Me/oxidation_Int1|0|正文|0|9.100000000|8.334192405|-0.765807595|
|Mn2-Me/oxidation_Int1|0|打印|0|9.420172224|8.334192405|-1.085979818|
|Mn2-Me/oxidation_Int1|0|重构|0|9.100330645|8.334192405|-0.766138239|
|Mn2-Me/oxidation_TS2|0|正文|0|15.780000000|15.502082525|-0.277917475|
|Mn2-Me/oxidation_TS2|0|打印|0|16.552444905|15.502082525|-1.050362381|
|Mn2-Me/oxidation_TS2|0|重构|0|15.781800520|15.502082525|-0.279717995|
|Mn2-Me/reduction_S_TS1|0|正文|0|8.650000000|9.072910363|+0.422910363|
|Mn2-Me/reduction_S_TS1|0|打印|0|8.509028467|9.072910363|+0.563881896|
|Mn2-Me/reduction_S_TS1|0|重构|0|8.652477133|9.072910363|+0.420433230|
|Mn2-Me/reduction_S_Int1|0|正文|0|2.180000000|2.931023334|+0.751023334|
|Mn2-Me/reduction_S_Int1|0|打印|0|2.197538178|2.931023334|+0.733485157|
|Mn2-Me/reduction_S_Int1|0|重构|0|2.176955867|2.931023334|+0.754067468|
|Mn2-Me/reduction_S_TS2|0|正文|0|1.890000000|1.971749601|+0.081749601|
|Mn2-Me/reduction_S_TS2|0|打印|0|1.851780458|1.971749601|+0.119969143|
|Mn2-Me/reduction_S_TS2|0|重构|0|1.891125301|1.971749601|+0.080624300|
|Mn2-Me/reduction_R_TS1|0|正文|0|10.520000000|10.693020598|+0.173020598|
|Mn2-Me/reduction_R_TS1|0|打印|0|11.732544635|10.693020598|-1.039524037|
|Mn2-Me/reduction_R_TS1|0|重构|0|10.523835886|10.693020598|+0.169184712|
|Mn2-Me/reduction_R_Int1|0|正文|0|1.820000000|2.114476631|+0.294476631|
|Mn2-Me/reduction_R_Int1|0|打印|0|2.193773121|2.114476631|-0.079296490|
|Mn2-Me/reduction_R_Int1|0|重构|0|1.820153980|2.114476631|+0.294322651|
|Mn2-Me/reduction_R_TS2|0|正文|0|1.800000000|1.972000605|+0.172000605|
|Mn2-Me/reduction_R_TS2|0|打印|0|1.589481498|1.972000605|+0.382519108|
|Mn2-Me/reduction_R_TS2|0|重构|0|1.795555608|1.972000605|+0.176444997|
|Mn2-Me/reduction_product|0|正文|0|-4.430000000|-3.962704131|+0.467295869|
|Mn2-Me/reduction_product|0|打印|0|-5.421681855|-3.962704131|+1.458977724|
|Mn2-Me/reduction_product|0|重构|0|-4.433919192|-3.962704131|+0.471215061|
|Mn2-tBu/oxidation_TS1|0|正文|0|6.890000000|7.022327374|+0.132327374|
|Mn2-tBu/oxidation_TS1|0|打印|0|7.269697256|7.022327374|-0.247369883|
|Mn2-tBu/oxidation_TS1|0|重构|0|6.891309043|7.022327374|+0.131018331|
|Mn2-tBu/oxidation_Int1|0|正文|0|9.270000000|7.360021597|-1.909978403|
|Mn2-tBu/oxidation_Int1|0|打印|0|9.163520849|7.360021597|-1.803499251|
|Mn2-tBu/oxidation_Int1|0|重构|0|7.265555694|7.360021597|+0.094465904|
|Mn2-tBu/oxidation_TS2|0|正文|0|14.780000000|14.360511014|-0.419488986|
|Mn2-tBu/oxidation_TS2|0|打印|0|15.680834246|14.360511014|-1.320323232|
|Mn2-tBu/oxidation_TS2|0|重构|0|14.778412871|14.360511014|-0.417901857|
|Mn2-tBu/reduction_S_TS1|0|正文|0|8.160000000|8.277949986|+0.117949986|
|Mn2-tBu/reduction_S_TS1|0|打印|0|8.402979366|8.277949986|-0.125029380|
|Mn2-tBu/reduction_S_TS1|0|重构|0|8.158062418|8.277949986|+0.119887568|
|Mn2-tBu/reduction_S_Int1|0|正文|0|1.900000000|1.662720011|-0.237279989|
|Mn2-tBu/reduction_S_Int1|0|打印|0|2.736568816|1.662720011|-1.073848805|
|Mn2-tBu/reduction_S_Int1|0|重构|0|1.901667461|1.662720011|-0.238947450|
|Mn2-tBu/reduction_S_TS2|0|正文|0|0.800000000|1.110348521|+0.310348521|
|Mn2-tBu/reduction_S_TS2|0|打印|0|1.117594373|1.110348521|-0.007245852|
|Mn2-tBu/reduction_S_TS2|0|重构|0|0.800262832|1.110348521|+0.310085689|
|Mn2-tBu/reduction_R_TS1|0|正文|0|10.180000000|10.425952566|+0.245952566|
|Mn2-tBu/reduction_R_TS1|0|打印|0|11.313368307|10.425952566|-0.887415740|
|Mn2-tBu/reduction_R_TS1|0|重构|0|10.179960695|10.425952566|+0.245991872|
|Mn2-tBu/reduction_R_Int1|0|正文|0|1.130000000|1.311038601|+0.181038601|
|Mn2-tBu/reduction_R_Int1|0|打印|0|3.123114652|1.311038601|-1.812076051|
|Mn2-tBu/reduction_R_Int1|0|重构|0|1.124622479|1.311038601|+0.186416122|
|Mn2-tBu/reduction_R_TS2|0|正文|0|0.560000000|0.892816087|+0.332816087|
|Mn2-tBu/reduction_R_TS2|0|打印|0|0.420431348|0.892816087|+0.472384739|
|Mn2-tBu/reduction_R_TS2|0|重构|0|0.563189753|0.892816087|+0.329626334|
|Mn2-tBu/reduction_product|0|正文|0|-3.740000000|-3.207502754|+0.532497246|
|Mn2-tBu/reduction_product|0|打印|0|-4.407626545|-3.207502754|+1.200123792|
|Mn2-tBu/reduction_product|0|重构|0|-3.737007171|-3.207502754|+0.529504417|


[autonomous_research 现行规则](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_d142c9737f95225b/evaluation/scoring_rules.json) · [paper_reproduction 现行规则](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_d142c9737f95225b/evaluation/scoring_rules.json)

[autonomous_research 现行计算参考](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_d142c9737f95225b/evaluation/verified_computation_reference.md) · [paper_reproduction 现行计算参考](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_d142c9737f95225b/evaluation/verified_computation_reference.md)


本包任务来自以下现行目录，逐文件原样复制；未包含巨型 QC 日志／缓存，原始科学证据通过以上链接访问。复制前确认源任务内没有符号链接；保留现有 manifest，不覆盖旧的 11 篇人工审定材料。

- [autonomous_research 原任务](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_d142c9737f95225b) → [本包副本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/autonomous_research/paper_d142c9737f95225b)
- [paper_reproduction 原任务](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/paper_reproduction/paper_d142c9737f95225b) → [本包副本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/paper_reproduction/paper_d142c9737f95225b)

# 2026-10-21 科学分 V2 当前评分状态

现行自主科研评分为 `paper_science_v2`，只计100分科学中间发现与最终结论；正式运行评分允许，出版专家审查仍待完成。当前范围定性计算已于2026-10-20验收，严格数值整题通过为false。本次没有提交新计算，没有把验证者参考计算称为盲测。

旧40分来源冻结由本版明确、可证伪的条件性科学结果重新设计取代，并非将旧数值项宣告通过。当前100分均为有计算支持的定性科学命题；绝对势垒/ΔΔG来源歧义仍真实存在，未选择最接近验证值的来源、未拟合容差。2026-10-20验收支持现行科学范围；不存在活动40分永久冻结。

- 正文、SI打印Gtot与Esol+gas Gcorr重构三套数值均保留。68项相对正文最大偏差1.909978 kcal/mol不是验收容差。
- Mn1-tBu氧化反应自由能正文−1.04、SI打印Gtot重算+0.067771；Me/tBu氧化细排序及tBu R通道跨家族排序不稳健，不作硬门。
- 作者未报告自旋/积分网格等；中性闭壳层单重态是明确的候选假设。部分连接是有效IRC前缀/模式位移+独立优化，不声称完整双向IRC。
- 保留全部原数值及旧40分冻结在历史审计；若未来加入绝对数值评分，先解决物理热项定义冲突，不能把当前定性资格解释为数值资格。

先前过程轴、保留分及待计算标签已由当前规则替代；以下所有日期记录为当时事实和历史审计，不是活动冻结或当前运行要求。原JSON完整保留在 `migration_history/20261021_pre_v2/`。

---

# 计算验证参考：paper_d142c9737f95225b

<!-- d142_current_user_qualitative_acceptance_20261020 -->

更新时间（UTC）：2026-10-20T03:24:37.048852+00:00。适用于本论文当前自主科研与论文复现模式。

## 1. 最新验收结论

**当前科学问题计算验证：通过（按用户确认的定性验收标准）。** 作者公开的主要电子结构方法与热力学条件匹配，当前范围有效计算与反应连接证据支持要求的核心定性结论。此判定基于逐项证据，不是仅凭作业完成、平均偏差或68/68数量。

- current_scope_verified = true
- verification_decision = 通过（当前任务范围、作者公开主要方法一致、核心定性结论一致）
- quantitative_strict_pass = false
- all_results_identical = false
- scoring_reference_status = pending_source_qualification（现有40分来源资格保留独立处理）

此前PROVISIONAL_PASS_QUALITATIVE和待审记录保留作历史，本节是按用户最新确认作出的计算验收结论，不另计新增论文。任务科学问题是配体环境对候选锰活性形式、异丙醇氧化/苯乙酮还原及固定催化剂构型立体偏向的影响。无需完整复现整篇所有结果、前催化剂活化势垒、真实溶液布居、实验速率或bulk ee。

重要边界：作者未公开自旋、积分网格、阈值等细节；部分连接采用模式位移+优化或收敛IRC前缀+优化，并非完整双向IRC。因此不能写成“全部隐藏参数和全部计算步骤逐字相同”。局部取代基排序反转是真实未复现项，明确保留；它不属于现有规则要求保持的NN/NNS家族排序。通过仅对应当前问题的核心定性范围。

## 2. 作者方法与实际计算

来源：[正文](../../../../../papers/paper_d142c9737f95225b/documents/main.pdf)（p3方法、Figures4–6/8）和[补充材料Table S2/S3](../../../../../papers/paper_d142c9737f95225b/documents/supplementary_001.docx)。

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

## 4. 数值差异

### 4.1 全部来源统计

单位kcal/mol。按量ID去重，同一量若有多个实际/来源候选，统计保守取较大的绝对差；0.5、1、2只是描述区间，不是新设容差。

|来源|量ID|平均绝对差|中位绝对差|最大绝对差|≤0.5|0.5–1|1–2|>2|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|SI Esol+gas Gcorr重构|68|0.429385|0.287020|1.747150|53|6|9|0|
|SI打印Gtot重算|68|0.989468|0.974399|3.532086|19|19|23|7|
|正文图表|68|0.451508|0.286197|1.909978|52|6|10|0|

### 4.2 正文68项逐项对照

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

### 4.3 不一致结果必须保留

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

## 5. 定性分析结论及数值依据

### 5.1 NN三羰基候选比NNS二羰基候选更有利于醇氧化

A=Mn1 NN三羰基，B=Mn2 NNS二羰基。以下比较B−A，均为正，作者核心家族结论保持。

|取代基/参考|正文B−A|自算B−A|
|---|---:|---:|
|Me/分离反应物|+4.250000|+3.996526|
|Me/静息态|+4.080000|+4.396858|
|tBu/分离反应物|+3.930000|+2.448856|
|tBu/静息态|+3.480000|+4.100549|

### 5.2 NNS降低S通道还原势垒

|取代基|正文B(S)−A(S)|自算B(S)−A(S)|
|---|---:|---:|
|Me|-1.740000|-0.958370|
|tBu|-2.470000|-1.855684|

两者均负，支持当前S通道结论。R通道跨家族顺序不具来源稳健性，不扩写为必须相符的结论。

### 5.3 固定构型S通道低于R通道

|模型|正文TS1 R−S|自算TS1 R−S|差|
|---|---:|---:|---:|
|Mn1-Me|1.490000|1.793297|+0.303297|
|Mn1-tBu|1.040000|1.311928|+0.271928|
|Mn2-Me|1.870000|1.620110|-0.249890|
|Mn2-tBu|2.020000|2.148003|+0.128003|

完整TS1/TS2最高相对能包络也核对了四模型×三种来源及自算，共16项检查，方向均保持S较低。结论仅限固定构型；镜像催化剂需反转面映射，不证明宏观ee。此前将2.148003对2.02称为TS2是标签错误，实际原始账本为TS1_R−TS1_S，本表已更正。

### 5.4 静息态修正后氧化为更困难的半循环

|模型|自算静息态稳定化|有效氧化|S还原|R还原|氧化−较高还原通道|
|---|---:|---:|---:|---:|---:|
|Mn1-Me|-3.986818|15.492374|10.031280|11.824577|3.667797|
|Mn1-tBu|-3.446087|15.357742|10.133634|11.445561|3.912181|
|Mn2-Me|-4.387150|19.889233|9.072910|10.693021|9.196212|
|Mn2-tBu|-5.097780|19.458291|8.277950|10.425953|9.032338|

此结果支持作者在这些候选模型下的“醇氧化是更困难半循环”解释；未声称直接证明实际速率、完整微观动力学或真实催化剂种群。

### 5.5 反应路线与当前11项科学内容覆盖

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

## 6. 计算通过与评分参考的区别

本次按用户确认的条件将当前科学问题计算验证记为通过，不再将本篇写为“计算还未完成”的笼统状态。数值严格相等、所有细排序相同、隐藏参数相同或所有IRC同实现均不是本次声称。

R_OX、R_REST、R_RED、R_SR各10分的来源资格仍在现有评分文件中保留。这不是只完成60%计算，也不是已给agent打60分。此次授权为更新计算过程、差异和结论，因此只更新参考文档及manifest，不更改评分权重、gold、容差、题目或发布位置，不通过文档自动授予40分。

## 7. 原始证据索引

### 7.1 53条有效能量链

各链的Opt/Freq和SP原始路径、作业ID及虚频数如下；哈希及能量解析详情在独立数值复核JSON。

|案例|作业ID|虚频数|Opt/Freq日志|SP日志|
|---|---|---:|---|---|
|CH3_CHOH_CH3|hpc-job-09ffa2f6-e931-4a2d-8a82-86f4c8444d82|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CHOH_CH3/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CHOH_CH3/native/sp.log)|
|Ph_CO_CH3|hpc-job-d7e67241-3062-42c1-ac4e-8cb9d203b2ab|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CO_CH3/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CO_CH3/native/sp.log)|
|Int1_Mn1_Me|hpc-job-2bf6dcf6-0630-4fe0-a2cf-e2f115466fb1|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me/native/sp.log)|
|Int1_Mn1_Me_2H_Acetophenone_R|hpc-job-b3f25923-acb1-4980-a0f0-448403690bff|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn1_Me_2H_Acetophenone_S|hpc-job-381e139f-89b3-45bc-95d2-41ef46c90dcb|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_Me_2H_Acetophenone_S/native/sp.log)|
|Int1_Mn1_tBu|hpc-job-9042d062-dbb9-4e23-9dcd-f866f840ab1c|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu/native/sp.log)|
|Int1_Mn1_tBu_2H_Acetophenone_R|hpc-job-7f8b47cf-d1a1-4eb6-b766-ac95349527d7|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn1_tBu_2H_Acetophenone_S|hpc-job-513cdb90-e6e2-4139-8283-68f3ca6dff8d|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn1_tBu_2H_Acetophenone_S/native/sp.log)|
|Int1_Mn2_Me|hpc-job-0ee27abf-3187-44e4-9616-28616b0bc5cf|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me/native/sp.log)|
|Int1_Mn2_Me_2H_Acetophenone_R|hpc-job-776ce936-88e5-472c-8453-c04a4b4e9193|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn2_Me_2H_Acetophenone_S|hpc-job-a82d2aed-644f-44a0-9535-92a93a7f6bb8|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_Me_2H_Acetophenone_S/native/sp.log)|
|Int1_Mn2_tBu|hpc-job-6181117c-94d0-4db9-addd-d57c148ea681|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu/native/sp.log)|
|Int1_Mn2_tBu_2H_Acetophenone_R|hpc-job-d95223f0-c567-4478-a4b7-b7f86cf73a15|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_R/native/sp.log)|
|Int1_Mn2_tBu_2H_Acetophenone_S|hpc-job-07125833-db5b-4090-bed6-8a9d282af917|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Int1_Mn2_tBu_2H_Acetophenone_S/native/sp.log)|
|Mn1_Me|hpc-job-5bab39c9-a669-41dd-929a-317b43c27a48|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me/native/sp.log)|
|Mn1_Me_2H|hpc-job-bab47977-8460-48f5-ae84-b4c935174c40|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me_2H/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_Me_2H/native/sp.log)|
|Mn1_tBu|hpc-job-53fa7bb7-9e95-4406-a644-381e61c9cfa7|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu/native/sp.log)|
|Mn1_tBu_2H|hpc-job-294f88da-4ebb-41c6-a28f-7c7768d2c2ad|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu_2H/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn1_tBu_2H/native/sp.log)|
|Mn2_Me|hpc-job-e8654993-a30b-4c1a-b909-25c5e82c6318|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me/native/sp.log)|
|Mn2_Me_2H|hpc-job-1a990a8e-2d2a-429b-bc7e-354cce3f33dc|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me_2H/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_Me_2H/native/sp.log)|
|Mn2_tBu|hpc-job-d26c4a5e-8adc-4109-852b-07300bc670c6|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu/native/sp.log)|
|Mn2_tBu_2H|hpc-job-78fd82c6-dea6-4da8-a1a6-dd0296e05ac7|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu_2H/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Mn2_tBu_2H/native/sp.log)|
|Ph_CHOH_CH3|hpc-job-be37304d-45fe-4cd9-91a1-fed5fa0aab53|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CHOH_CH3/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/Ph_CHOH_CH3/native/sp.log)|
|TS1_Mn1_Me|hpc-job-7b369dea-db1b-4feb-bd44-1f4907e0a5b8|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me/native/sp.log)|
|TS1_Mn1_Me_2H_Acetophenone_R|hpc-job-50523fdf-8f19-4efe-8c26-f39254c8b5db|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn1_Me_2H_Acetophenone_S|hpc-job-6001a1a4-f1a7-4d8c-9e6e-e26f99bdb2f2|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_Me_2H_Acetophenone_S/native/sp.log)|
|TS1_Mn1_tBu|hpc-job-5ae4a341-e735-4817-881a-931d2f3da3c7|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu/native/sp.log)|
|TS1_Mn1_tBu_2H_Acetophenone_R|hpc-job-29e50f45-8074-457a-a2ae-f759acb31bd5|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn1_tBu_2H_Acetophenone_S|hpc-job-8911546c-afd9-4fb2-85aa-f46b6dfe311a|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn1_tBu_2H_Acetophenone_S/native/sp.log)|
|TS1_Mn2_Me|hpc-job-47eac770-87e7-4790-9df9-ed0bf9ccda87|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me/native/sp.log)|
|TS1_Mn2_Me_2H_Acetophenone_R|hpc-job-16ec23b8-e548-42ac-ba3e-b7fba3f7a764|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn2_Me_2H_Acetophenone_S|hpc-job-de76c74c-a1ee-4301-aec7-8964898ad92e|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_Me_2H_Acetophenone_S/native/sp.log)|
|TS1_Mn2_tBu|hpc-job-39d21c0e-149b-4f9d-8b6e-78a23ec78ccb|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu/native/sp.log)|
|TS1_Mn2_tBu_2H_Acetophenone_R|hpc-job-3f46b4ba-3d61-4cea-bf56-c7c5b302d4e2|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_R/native/sp.log)|
|TS1_Mn2_tBu_2H_Acetophenone_S|hpc-job-bd6d878a-9d13-4e9d-a7ce-039037685ddc|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS1_Mn2_tBu_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn1_Me|hpc-job-8b7d28b7-2d34-4444-8b6d-08a7db83b056|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me/native/sp.log)|
|TS2_Mn1_Me_2H_Acetophenone_S|hpc-job-aaf15d8c-66f6-4fea-9213-62876d16540f|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_Me_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn1_tBu|hpc-job-d8f245d4-f0ac-46d0-b7fc-581e5f8fd651|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu/native/sp.log)|
|TS2_Mn1_tBu_2H_Acetophenone_R|hpc-job-f9e6ebca-e195-4b6a-92a1-8b05d2b0fe39|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_R/native/sp.log)|
|TS2_Mn1_tBu_2H_Acetophenone_S|hpc-job-9d06465e-e4ad-41ac-82d8-b404f06940d2|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn1_tBu_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn2_Me|hpc-job-00f7f4e0-5296-403e-a5c4-ea79c26e8dac|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me/native/sp.log)|
|TS2_Mn2_Me_2H_Acetophenone_R|hpc-job-7ccf2e4d-da84-43b2-bfd0-48aa876bbe2c|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_R/native/sp.log)|
|TS2_Mn2_Me_2H_Acetophenone_S|hpc-job-63ef59a9-3566-473c-9750-34a742cabf90|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_Me_2H_Acetophenone_S/native/sp.log)|
|TS2_Mn2_tBu|hpc-job-567a04fa-eea1-4ce5-9027-4f58d5f21cda|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu/native/sp.log)|
|TS2_Mn2_tBu_2H_Acetophenone_R|hpc-job-ec2924ff-6bf6-467f-96d0-183b8c612333|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_R/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_R/native/sp.log)|
|TS2_Mn2_tBu_2H_Acetophenone_S|hpc-job-f2ec90ba-749b-4557-b550-f8bd9cd26b24|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_S/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/TS2_Mn2_tBu_2H_Acetophenone_S/native/sp.log)|
|VIII_Me_OCHMe2|hpc-job-60f55f94-a32b-49bb-b7d7-fabd40da9d31|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_Me_OCHMe2/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_Me_OCHMe2/native/sp.log)|
|VIII_tBu_OCHMe2|hpc-job-68f843ff-b133-4ef4-9fed-caf621a56096|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_tBu_OCHMe2/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VIII_tBu_OCHMe2/native/sp.log)|
|VII_Me_OCHMe2|hpc-job-6bfbcfc5-ff61-4d24-8ee5-bf0d8b87ea33|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_Me_OCHMe2/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_Me_OCHMe2/native/sp.log)|
|VII_tBu_OCHMe2|hpc-job-6c08b712-adda-4755-b40f-5a94df73e6ad|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_tBu_OCHMe2/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/VII_tBu_OCHMe2/native/sp.log)|
|CH3_CO_CH3_modeminus|hpc-job-0e401f7c-68ba-4cff-87af-3b70ed8fff03|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeminus/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeminus/native/sp.log)|
|CH3_CO_CH3_modeplus|hpc-job-aa50b3b9-f41c-42ef-bc2a-384173577778|0|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeplus/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/cases/CH3_CO_CH3_modeplus/native/sp.log)|
|TS2_Mn1_Me_2H_Acetophenone_R|hpc-job-4eaa60f8-11ae-4478-b2ab-a79e2ae79582|1|[Opt/Freq](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/followup_20261017/TS2_Mn1_Me_2H_Acetophenone_R_recover01/native/optfreq.log)|[SP](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/followup_20261017/TS2_Mn1_Me_2H_Acetophenone_R_recover01/native/sp.log)|

### 7.2 结果账本与路径验收

- [68量物种账本及恢复变体](../../../../../docs/verification/small_molecules_autonomous_research/verification_followup_20261019T0035Z/new_group_03/paper_d142c9737f95225b/energy_comparisons.json)
- [全部217行来源/变体对照](../../../../../docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/new_group_03/quantitative_comparison_supplement.json)
- [定性关系及全部反转](../../../../../docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/new_group_03/mn_qualitative_relations.json)
- [106日志重读与独立能量重算](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/numerical_audit_20261020/numerical_reaudit.json)
- [详细偏差复核](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/numerical_audit_20261020/计算结果与论文逐项差异复核.md)
- [代表氧化共同Int1端点验收](../../../../../docs/verification/small_molecules_autonomous_research/storage_recovery_20261019T0530Z/new_group_03/endpoint_acceptance.json)
- [同几何审计](../../../../../docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/same_geometry_protocol_audit.json)
- [此前108份该论文日志独立审查](../../../../../docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/acceptance_native_audit.json)
- [SI Table S2组装审计](../../../../../docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/source/table_S2_assembly_audit.json)

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

## 附录B：历史记录（非当前状态）

完整保留此前文档，用于追溯当时的失败、待审、未计算及暂定状态。下列旧状态不覆盖第1节；历史失败和来源问题不因本次验收消失。

# Independent computation status

<!-- new_group_03_sp_return_current -->
当前状态（2026-10-20T02:59:50.554983+00:00）：两模式均已由父级登记 PROVISIONAL_PASS_QUALITATIVE；不是待审候选。父级决定时间 2026-10-20T02:34:18.917879+00:00，决定：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/parent_acceptance_decision.json，独立复核：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/acceptance_review.md。68/68量、53条有效能量链、22端点阶段与11/11当前科学问题定性覆盖复用。非严格数值/正式评分/发布通过，40分保留不授分。下方pending/待父审文字仅为历史快照，现已由父级决定替代；本次同步不另计新增论文。

## 历史验证记录（以下状态均按其记录时间解释）

current_scope_verified = false

No quantum-chemical computation was submitted or run during this repair. Source reading, table arithmetic, structure inventory, native package validation and runtime adaptation are the only checks performed. Author reported values are source-qualified verification targets, not an independently verified result.

Pending quantitative reference weight: 40/100 scientific points; no redistribution. The release/verification owner must qualify these references before awarding their points or certifying the whole task. The autonomous agent is not required to investigate hidden source inconsistencies.

## Minimum results to verify

- K_ACTIVE: main Scheme 2/Figure 2 and SI Table S3; map real NNS precatalysts to hypothesized A/B, verify graph/CO count/charge and chosen spin; no activation barrier/population demand.
- K_OX/K_REST/K_OX_ORDER: Figure 4 and Figure 8; SI Table S2 rows Mn1-Me, Mn1-tBu, Mn2-Me, Mn2-tBu, isopropanol, TS1/Int1/TS2 and VII/VIII-R-OCHMe2. Reconstruct E/Gcorr/Gtot and both reference ledgers; preserve the TS2(Mn-Me) source alias.
- K_RED/K_SR/K_RED_ORDER/K_SR_ORDER: Figures 5–6 and Table S2 matching amine-hydride, acetophenone and TS1/Int1/TS2 S/R rows. Minimum tBu A/B S/R paired result; Me variants complete the matched scope. Resolve main-versus-SI gap discrepancies before any unique numeric gold.
- K_PATH/C_ACTIVITY/C_STEREO: verify frequency/IRC and hydrogen/handedness mapping, couple half-reactions, retain conditional stereochemical scope and release-pending source conflicts.

## Source qualifications and release blockers

- Main Figures 4–6 and SI Table S2 solution Gtot do not produce identical barriers using the explicitly stated separated-reactant ledgers. Example Mn1-tBu S/R barriers: main 10.63/11.67, direct SI arithmetic 9.14219/11.06738 kcal/mol. The corresponding gap is main 1.04 versus SI 1.92520. Mn2-tBu gap is main 2.02 versus SI 2.91039. All source sides and arithmetic are preserved in source_audit/energy_table_audit.json. Do not select one side as unique gold or enlarge tolerances.
- Some reaction thermodynamics or fine orderings change across sources: Mn1-tBu alcohol oxidation is −1.04 kcal/mol in the main text but +0.06777 from SI Gtot; Mn1 Me/tBu oxidation ordering and the tert-butyl R-channel NN/NNS reduction ordering are not source-robust. These are excluded from mandatory directional targets.
- The robust current scientific scope is matched candidate identities; NN tricarbonyl versus NNS dicarbonyl oxidation ordering; the S-channel reduction ordering; within a fixed handed configuration the S/R energetic asymmetry; and the coupled half-reaction account. Absolute barrier/ΔΔG targets remain source-qualified pending reconciliation, so there are no unique numerical-closeness rules for the conflicted quantities.
- SI Table S2 supplies gas E/ZPE/Hcorr/Gcorr/NImag and solution E/Htot/Gtot. Its solution Gtot values are not invariably identical to solution E plus the printed gas Gcorr. The exact correction assembly must be audited before attributing discrepancies to a method. Original input decks, grids, frequency scaling and multiplicity are not printed; a closed-shell singlet Mn(I) model is an explicit assumption unless supported by new evidence.
- The source label TS2(Mn-Me) is assigned to Mn2-Me by the surrounding Table S2 rows and composition; retain this alias rather than silently changing the source. Some later proton-transfer TS Gibbs ordinates are lower than adjacent intermediate ordinates; validate the electronic stationary points and thermochemical definitions.
- The selected achiral-ligand catalyst geometries can be chiral conformations/configurations. Their S/R differences and source 84%/96% estimates do not establish ensemble ee. Include mirror-related catalyst forms/populations only if making such an additional claim; bulk ee is not a gold.
- No quantum-chemical validation was run in this repair. This package is release pending source reconciliation and current-scope computation. Proposing active forms does not require uncomputed precursor-activation barriers or proof of true solution speciation.

A platform SUCCEEDED state alone does not verify any result. Preserve raw computation and map it to each result ID. Do not alter the question, source values or tolerances to make verification pass.

Source-coordinate visibility correction: optimized author Cartesian structures are evaluator-only. PR supplies model identity, reaction topology and methods, and must construct/optimize its own geometries. The private author-route verifier may read the original papers/SI and the PR package evaluation/author_route_source_coordinates excerpts.


## Independent author-route execution update (2026-10-16, group_03)

current_scope_verified=false. 54 opt/frequency+single-point job attempts for 52 assessed stationary states have now been actually submitted. 2 native chains passed exit, normal-termination, atom/charge/spin, frequency-count, same-geometry and protocol-marker checks at 2026-10-16T02:05:54.270086+00:00; this does not certify the reaction key points.

- Ph_CO_CH3: native opt/freq+SP complete; G=-384.8733385030 Eh; NImag=0; Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019.
- CH3_CHOH_CH3: native opt/freq+SP complete; G=-194.3234895010 Eh; NImag=0; Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019.
- CH3_CO_CH3: not accepted; optfreq: imaginary_mode_count; NImag=1; native/optfreq.log retained. See successor.json for scientifically distinct recovery attempts.

28/28 key main comparisons reconcile with E_solution+gas_Gcorr within 0.004735 kcal/mol. Printed solution Gtot retained separately. Full-profile unresolved: Mn2-tBu oxidation Int1 9.27 versus7.265556; Mn1-Me S Int1 two Gcorr candidates; Mn2-tBu R Int1 rounding boundary. No evaluator/gold or reserved40-point policy change.

All required IDs and scientific rules are recorded in `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_d142c9737f95225b/new10_20261016/coverage.json`; paper/source/actual/difference rows are in `comparison.csv` and `state_comparison.csv`. Native evidence and job IDs are in `cases/` and `jobs.json`. See `author_method_manifest.json`, `verification_report.md` and `successor.json` for method fidelity, source ambiguities, remaining IRC/identity validation and continuation. Computations are author-guided verification, not an AR discovery test. No scoring rules, targets, tolerances, task inputs, scientific core or reserved quantitative weight were changed.


Stationarity recovery: {'CH3_CO_CH3': -49.72} lists parent cases and their negative modes in cm^-1. Native optimization/frequency normal-terminated but the source NImag=0 minimum condition failed, so SP was gated off. Two same-method successors per case follow positive/negative directions of the computed mode with maximum atom displacement0.15 A; original logs/checkpoints retained. Neither source thermochemistry nor successor results are assumed valid. See source/*stationarity_issue.json and recovery_plan.json.


## Author-route verification followup (2026-10-17, new_group_03)

current_scope_verified=false. 52/54 current stationary attempts have audited optfreq/SP chains; migrated STOPPED predecessors excluded. 24 new actual jobs: 1 justified recovery and 23 dual-direction IRC/endpoint jobs. Platform and native status are distinct; no whole-paper PASS or acceptance candidate.

67/68 full-profile comparisons assembled, including all28 headline quantities. Oxidation A(Me,tBu)=11.505556/11.911655 and B(Me,tBu)=15.502083/14.360511kcal/mol. Effective barriers=15.492374/15.357742/19.889233/19.458291. R−S=1.793297/1.311928/1.620110/2.148003kcal/mol. All required robust energy orderings hold. Missing full-profile quantity: Mn1-Me/R TS2.

- Main values, printed SI Gtot and E_solution+Gcorr_gas source candidates all retained; no value chosen to maximize agreement.28 main quantities reconcile arithmetically with E_solution+Gcorr_gas while printed Gtot remains inconsistent.
- Mn2-tBu oxidation Int1 main9.27 versus source assembled7.265556, duplicate Mn1-Me/S Int1 Gcorr and gas bookkeeping conflicts remain unresolved.
- Original acetone −49.72cm−1 fails minimum classification. Both zero-imaginary ±mode recoveries yield G=−193.14877764Eh. Their oxidation reaction ledgers remain labeled recovered-minimum variants, not replacements of source gold.
- AuthorA/B models are used for verification; AR does not presuppose them. Singlets are assumptions, not an independent spin-state/population study. No true populations, bulk ee or uncomputed precatalyst activation barrier claimed.
- Existing reserved40 quantitative points and release qualification restrictions remain unchanged; trends do not complete them.

Complete author/actual/difference ledgers, key-point/rule coverage and raw-evidence links: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/paper_d142c9737f95225b/verification_report.md, energy_comparisons.json, state_comparison.csv, coverage.json. Identity/modes: geometry_mode_summary.json. Same-geometry/protocol: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/same_geometry_protocol_audit.json. New IDs/native snapshot: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/submission_receipts.json and successor_readbacks/final/inventory.json. Finite continuation: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/handoff.json. No task instruction,input,evaluator,gold,tolerance,qualification,reserved weight,expert or zip changed. This is author-guided verification, not AR discovery evidence.


## Native-return review (2026-10-17, status_review_20261017T1137Z/new_group_03)

68/68 full-profile quantities now have genuine native energy assemblies, including all28 headline quantities. Recovered Mn1-Me/R TS2:9.472715kcal/mol versus author main9.56 (delta−0.087285); source Esol+Gcorr9.562052 and printed SI Gtot9.227527 are both retained. Its Egas−2753.11166995Eh, Gcorr0.338492Eh, ESP−2753.14537700Eh yield composite−2752.806885Eh. Exactly one imaginary mode−1282.8299cm−1; same geometry optfreq/SP verified; source R face retained.

- All68 energy ledgers and alternative source candidates are retained. Printed SI Gtot inconsistencies, Mn2-tBu oxidation Int1 main9.27 versus assembled7.265556, and duplicate Mn1-Me/S Int1 Gcorr remain unresolved.
- Reserved40 quantitative points and release qualification are unchanged. Numerical agreement or energetic trends do not release reserved credit or produce whole-paper PASS.
- 53/54 stationary attempts now have valid optfreq/SP chains (including both qualified acetone recovered minima). The original acetone imaginary mode remains rejected.
- AuthorA/B models used for verification; no AR preselection, real population, bulk ee, or uncomputed precatalyst activation barrier claim. Singlet is disclosed implementation assumption.
- 11 IRC corrector failures were continued once from their preserved checkpoints with MaxCycle80; method, grid,SCF,StepSize and corrector thresholds unchanged. This numerical remedy remains unproven until logs verify it. No second same-cause submission planned.
- Completed stages are reused. A normal IRC ending at the point cap is not PES-minimum convergence; graph/fragment matches and one-sided chemical support do not establish both connections.

current_scope_verified=false; no acceptance_candidate. This round adds12 actual jobs for this paper; 6 completed endpoints were individually audited. Platform/native statuses remain separate. Complete author/actual/difference and mandatory-ID coverage: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/paper_d142c9737f95225b/verification_report.md, energy_comparisons.json, comparison.csv, state_comparison.csv, coverage.json. Recovered TS proof: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/recovered_TS_acceptance.json. IRC/endpoint and atomic mapping: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/irc_direction_audit.json, endpoint_chemical_audit.json, endpoint_fragment_mapping.json. Exact jobs and readback: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/submission_receipts.json; /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/final_readback/inventory.json. Finite handoff/ETA: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/handoff.json; /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/advance_feasible_20261017T1145Z/new_group_03/eta.json. No task/input/scoring/tolerance/qualification/gold/expert/zip change. No periodic resume.


## Local native preflight and single-canary repair (2026-10-17T1210Z,new_group_03)

All11 recent IRC Restart attempts failed natively in0.27–0.92s, notwithstanding platform80–93s and SUCCEEDED. They produced zero new SCF or path points; MaxCycle80 prints in the header but each checkpoint resumes its old exhausted20/20 state. One real local reproduction confirms this. One new reverse-IRC canary from the accepted TS Hessian uses StepSize5 and default MaxCycle20; only the missing reverse direction is recomputed.68/68 energy coverage remains; reserved40-point source qualification unchanged.

One representative original failure was reproduced locally under2CPU/180s/sharedflock. Fresh accepted-TS RCFC reverse input changes only numerical step10→5, keeps MaxCycle20; native startup and3SCF iterations confirmed, but controlled180s timeout(rc−9),0SCF Done and no nonzero path point. FCHK identity/Hessian audit passed subsequently. Exactly1HPC canary submitted:hpc-job-cc60ae34-bd88-4cce-a25a-e5db9a7ff01a;latest platform/native:RUNNING/NATIVE_RUNNING;rollout=false. No successful stage repeated, no active job canceled. The platform-failed Mn1-tBu/S chain only finished endpoint optimization; its later internal frequency job is truncated, not accepted. Frequency-only recovery geometry preserved. Full evidence/coverage:/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/local_preflight_repair_20261017T1210Z/new_group_03/paper_d142c9737f95225b/verification_report.md,/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/local_preflight_repair_20261017T1210Z/new_group_03/local_preflight.json,checkpoint_geometry_audit.json,failure_inventory.json,partial_stage_salvage.json,canary.json. Handoff:/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/local_preflight_repair_20261017T1210Z/new_group_03/handoff.json. Source qualification,40reserved points,all gold,tolerance and task/scoring definitions unchanged. current_scope_verified=false; no automatic resume.


## Native-return review (2026-10-18T0200Z,new_group_03)

68/68 energy assemblies and53 valid stationary optfreq/SP chains are reused.19 zero-imaginary endpoint stages and5 qualified bilateral local connections are audited; capped IRC segments are followed continuously by converged endpoint optimizations, not called IRC-minimum convergence. Mn1-tBu/R TS1/TS2 support C-H thenO-H formation via compatibleR Int1 graphs; conformer energy identity is not assumed. Oxidation-side connections remain incomplete. Canarycc60ae34 reached9points/0.50591 but terminatedL123; no rollout. Source-conflicted40 reserved points remain unchanged. No full-question candidate. One frequency-only recovery from b4e3e5d9 completed optimization archive was actually submitted: hpc-job-9e242613-ca05-46ac-852b-217f0e19a1cf; latest RUNNING/NATIVE_RUNNING,1SCF Done, no final frequencies yet. Local2CPU/180s/sharedflock preflight was a controlled timeout, not completion. No optimization repeat, no active-job stop.

Current scientific question only; no new precursor activation, population, bulk-ee, cis competitor or whole-paper-IRC requirement. Author methods, source candidates and tolerances are retained. Complete rule coverage and all author/computed/absolute/relative differences: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261018T0200Z/new_group_03/paper_d142c9737f95225b/verification_report.md; energy_comparisons.json, comparison_all_source_conventions.csv, state_comparison.csv, coverage.json. Native/connection audit: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261018T0200Z/new_group_03/native_audit.json; connection_acceptance.json. Finite handoff: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261018T0200Z/new_group_03/handoff.json. current_scope_verified=false; acceptance_candidates=[]; no periodic resume.


## Frequency-only return acceptance (2026-10-18T0324Z,new_group_03)

Job hpc-job-9e242613-ca05-46ac-852b-217f0e19a1cf is independently accepted for the Mn1-tBu/S forward endpoint only: native/wrapper rc0, final Normal,177 frequencies and zero imaginary modes (lowest22.3844cm^-1); Gaussian elapsed42m55.8s. Original b4e3e5d9 forwardIRC43points/PES-minimum and tight optimization are reused. The10-decimal optimized archive, new frequency input and final archive agree exactly; no geometry optimization repeated. M06L/all-electronTZVP gas,UltraFine,tightSCF,61atoms,charge0,singlet,298.15K/1atm.

Egas=-2871.08699959Eh equals the original optimized energy; ZPE=0.490833,Hcorr=0.526674,Gcorr=0.422337Eh, printed gasG=-2870.664662Eh (own Egas+printedGcorr=-2870.66466259Eh; rounding residual<1e-6Eh). These are this endpoint's own gas thermal terms, not a solution composite; no endpoint GD3/SMDiPrOH single point is claimed and no sourceTS thermal term is substituted. Element-preserving mapping identifies Mn1-tBu amine-hydride plus acetophenone: Mn-H1.611445A,N-H1.021242A,C=O1.227079A;3CO and pendant sulfur retained. S labels the parent channel, not an S-alcohol endpoint.

Completed minimum endpoints19->20; qualified bilateral local connections5 unchanged; source-profile energy coverage68/68 and53 stationary optfreq/SP chains unchanged. ThisS-channel reverse and oxidation-side connections remain incomplete; reserved40-point source qualification remains unchanged. No full-question pass/candidate, new calculation, retry or scheduled resume. Audit: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/progress_detail_20261018T0324Z/mn_owner_return_review.json; /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/progress_detail_20261018T0324Z/mn_owner_return_review.md. This supersedes the earlier running status for9e242613.

## 2026-10-18 计算阻碍恢复轮（0342Z dispatch）

更新 2026-10-18T04:42:56.251556+00:00。新增整题通过0；不释放任何来源资格或定量保留项。仅对当前科学问题定义必要下一步，完整记录：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/recover_computational_blockers_20261018T0342Z/new_group_03`。

复用68/68能量量、53条驻点/SP链、20个零虚频端点和5组双向局部连接；已接受的177正频不重复。补未计算的Mn1-tBu/S反向，并以一个Mn2-tBu氧化O–H反应模位移端点测试替代失败正确器。氧化O–H/C–H连续连接和端点映射未完成，40分来源保留资格维持。

全部新提交均有真实2CPU/180秒本地预检、共享flock和实时共享盘增长门槛；受控timeout不是科学完成。

- `hpc-job-a4225598-f072-4f57-9ff2-4d6fc56e461e`：TS1_Mn1_tBu_2H_Acetophenone_S_reverse_missing01；平台QUEUEING，原生NOT_STARTED。
- `hpc-job-ebdf4342-8d06-43b6-89dc-0d213fe3d041`：TS1_Mn2_tBu_reverse_mode_endpoint01；平台UNKNOWN，原生NOT_STARTED。

目前不增加有效科学结果计数；无自动恢复、无同因批量推广、无旧作业取消。

## 2026-10-19 原生返回核收与有限接续（0035Z）

更新时间 2026-10-19T00:55:25.935684+00:00。新增整题通过0，acceptance_candidates=[]。本轮证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261019T0035Z/new_group_03。原迁移旧ID保持停止，不恢复；平台成功不作为科学成功。

已核收d2e7a56c原生优化6个SCF、2412.16秒和频率1个SCF、1851.66秒，均正常退出；150正频、NImag=0。新端点与Int1保元素/等价H映射：重原子RMSD0.004025Å、全原子0.005889Å，气相E差−0.012029kcal/mol。接受此最小值及有条件O-H局部连接；不将其气相热化学替换溶液profile。历史53条驻点/SP链、68/68能量量、20个端点和5条既有局部连接复用；端点总数现为21，另记录1条模式位移限定O-H连接。
1746a30a虽平台SUCCEEDED，原生IRC40SCF、14个非零收敛点后L123失败（7046.19秒），后续opt/freq未执行。保留进展，不重复同参IRC。TS2检查点IRC轨迹第17帧（坐标−3.23957715）已与日志收敛点及TS初始帧核对，明确排除失败第18点current geometry；提交一个独立端点opt/freq代表。来源Gtot/复合G与正文差异及40分保留资格不变。

实际本地2CPU/180秒、4GB、共享flock预检均进入原生SCF/IRC，0个完整SCF，timeout只证明启动，不是修复完成或推广许可。每种独立原因只提交一个HPC代表。
- 新作业hpc-job-1a353017-b186-4825-8d66-febe5b620a8e：TS2_Mn2_tBu_reverse_point17_endpoint01，QUEUEING；CPU资源-2，优先级6，20CPU/100GiB。

逐项作者值/自算值/误差/全部来源候选与规则覆盖见本轮author_comparison.json、coverage.json及各论文verification_report.md；无整题候选，不调整评分/任务/正式资格。

## 2026-10-19 存储恢复与端点验收（0530Z）

UTC 2026-10-19T06:33:07.017542+00:00。证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/storage_recovery_20261019T0530Z/new_group_03。本轮新增提交0、停止0、整题通过0，acceptance_candidates=[]。

1a353017优化8SCF/2732.40秒、频率1SCF/1931.62秒均exit0，Tight四YES、150正频，最低38.0676cm^-1，opt/freq同几何。正式input/日志20CPU/80GB，平台20CPU/100GiB。接受TS2反向第17收敛点接无约束优化的最小值：与作者Int1重原子RMSD0.003371Å、全原子0.005326Å；与TS1端点重原子0.002524Å、全原子0.003566Å。气相E=-2565.93859807Eh，对既有Int1差+0.002861kcal/mol，仅作身份佐证，不替代溶液自由能。第17点至opt连续；失败第18试探排除。保元素/等价H映射固定H27/H28：H27在N2；C30–H28由Int1/TS2/产物1.193/1.761/2.517Å，Mn1–H28为1.897/1.685/1.642Å。复用正向PES最小值和Mn2-2H+acetone身份，支持同一Int1衔接的代表O–H→C–H序列。TS2反向仍为IRC前缀+优化，不是收敛反向IRC；TS1反向模式位移限定保留。端点阶段数21→22，非新增唯一化学态；五条既有连接加一条TS2前缀限定连接，另列TS1模式连接。68/68对照原样复用；正文/SI Gtot/复合G冲突、双Gcorr和40分保留不变。Mn1-tBu/S反向局部失败保留，不盲重算。

本轮无Create，实时双区容量/配额/账号CPU/存储承诺准入不适用，未宣称新准入成功。后续Create须按最新AGENTS锁下核查所有门槛。详见本轮endpoint_acceptance、coverage、jobs、failure_classification和handoff；不等待长作业、不自动恢复。

## 2026-10-19 定性准则核收与有限接续（1200Z）

UTC 2026-10-19T12:21:33.906102+00:00。本轮证据目录：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/new_group_03。仅本组两个论文、一个HPC canary、无停止/迁移/自动恢复。

本轮按用户2026-10-19准则列为PROVISIONAL_PASS_QUALITATIVE候选，待父级复核；不是STRICT_NUMERIC_PASS、官方评分通过或发布。复用53条有效optfreq/SP链、68/68数量和22个零虚频端点阶段，当前11项科学问题均有定性证据。作者明确的Gaussian16C.01、M06L/全电子TZVP气相优化/频率、GD3零阻尼+SMD异丙醇单点、298.15K/1atm匹配；原文未报告的自旋/网格/输入细项明确披露。中性单重态是候选模型选择，不代表已证作者隐藏输入或真实布居。Esol+gasGcorr由SI逐态字段支持，28项核心正文数值可在打印精度内重构；完整68项仍保留SI打印Gtot及双Gcorr来源，不挑选。

主要自算氧化势垒（Mn1-Me/Mn1-tBu/Mn2-Me/Mn2-tBu）11.50556/11.91166/15.50208/14.36051kcal/mol，有效势垒15.49237/15.35774/19.88923/19.45829；S还原10.03128/10.13363/9.07291/8.27795；R−S1.79330/1.31193/1.62011/2.14800。NN氧化低于NNS，NNS的S还原低于NN，固定构型S<R；对全部TS1/TS2最大profile高度而非仅TS1进行16个跨源检查，结论仍保持。静息态参考修正后氧化高于两个还原通道。

正文最大残差−1.90998kcal/mol在Mn2-tBu氧化Int1；打印Gtot最大残差−3.53209在Mn1-Me/S还原TS2。所有来源与有符号差值见quantitative_comparison_supplement.csv/json。Mn1 Me/tBu氧化、静息态、反应自由能及局部中间态次序反转全部披露；其中Mn1氧化Int1的Me/tBu顺序源侧一致而自算反转，属非核心中间次序，不以“来源冲突”掩盖。保留40分来源待定，原容差为空且未改变，不发放保留分。

代表Mn1-tBu/R还原连接及Mn2-tBu O−H→C−H共Int1连接支持当前半反应路线；TS1反向用模式位移+优化，TS2反向17点收敛IRC前缀+优化，不能称完整反向IRC。S反向corrector15失败未接受；该失败不被本轮候选状态抹去。无需论文全部IRC、前催化剂活化势垒、真实布居或bulk ee。详见method_comparison.md、paper_assessments.json和mn_qualitative_relations.json。

原任务、评分、gold、容差、40分保留及发布位置均不变。候选由父级复核；历史失败/部分记录不回写为成功。

## 2026-10-20 酸端点验收与单点接续（0220Z）

UTC 2026-10-20T02:36:24.429395+00:00。本轮证据目录：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03。

复用上一轮PROVISIONAL_PASS_QUALITATIVE候选及68/68量、53条有效能量链和22端点阶段，本轮无新增计算、无新增候选计数、无独立注册通过。父级acceptance_review_first_round.json处于FIRST_ROUND_NOT_FINAL_ACCEPTANCE，要求独立审查未报告自旋、源热校正/Gtot差异和路径证据；本轮提供既有方法/连接证据入口，保持待审，不重复成功计算。若父级给出具体必须修复的物种/字段再做最小修复。40分保留、原容差与评分/发布资格未改。

仅更新两模式计算参考和manifest；任务、评分、gold、容差、final/hold位置不变。详见endpoint_acceptance、acid_path_ledger、method_comparison、paper_assessments、jobs、failure_classification与handoff。有限轮次后退出，无定时恢复。

## 2026-10-20 父级已登记状态同步（sp_return）

当前状态（2026-10-20T02:59:50.554983+00:00）：两模式均已由父级登记 PROVISIONAL_PASS_QUALITATIVE；不是待审候选。父级决定时间 2026-10-20T02:34:18.917879+00:00，决定：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/parent_acceptance_decision.json，独立复核：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/acceptance_review.md。68/68量、53条有效能量链、22端点阶段与11/11当前科学问题定性覆盖复用。非严格数值/正式评分/发布通过，40分保留不授分。下方pending/待父审文字仅为历史快照，现已由父级决定替代；本次同步不另计新增论文。

父级正式决定 ACCEPT_INDEPENDENT_REVIEW_WITH_DISCLOSED_LIMITATIONS，独立检查108份原生日志。作者M06L/全电子TZVP气相Opt/Freq、同几何M06L-GD3零阻尼/SMD异丙醇SP、G16C.01、298.15K/1atm的当前范围方法证据已被接受。所有68项旧对照、来源候选、有符号差、53条有效链和22端点阶段复用，本事件计算/新提交均0。

保留限制：正文/打印Gtot/Esol+Gcorr及重复Gcorr冲突；未报告自旋，使用中性单重态条件模型而非真实布居；代表IRC前缀+连续端点和TS1模式位移限定，不将失败S反向corrector15或TS2 corrector18改称成功。Mn1氧化Int1的tBu−Me细次序自算反转已披露；核心NN/NNS、固定S/R与完整TS1/TS2包络定性结论按父级复核接受。无需扩为前催化剂活化、真实布居、bulk ee或全论文全部IRC。

40分来源保留仍不授分；原null/source-reserved容差、题面、评分、gold和发布资格不变。不是STRICT_NUMERIC_PASS。前文“父级待审/无注册”的当前含义撤销，原文仅保留为历史。状态同步证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03_sp_return/acceptance_registration.json；本事件不重复计新增论文，不要求再次父审，无周期恢复。


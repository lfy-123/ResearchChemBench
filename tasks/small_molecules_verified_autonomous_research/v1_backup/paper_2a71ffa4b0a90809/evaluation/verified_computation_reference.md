## 2026-10-20 专家第一轮评分规则同步

正 σ-hole 与骨架电子效应合并为 15 分；系列解释明确同时采用能量与电子结构证据。18 项共 100 分。

本节记录评分合同变更；下方原日期的计算结果、旧规则和验收范围按历史保留，不作为额外的现行评分要求。当前规则以 scoring_rules.json、reference_key_points.json 和 reference_conclusions.json 为准。本轮没有新增量子化学作业。

> 2026-10-17 V2 评分更新：用户已批准本包现行初步数值容差和定性分配；可按 `paper_science_v2` 正式运行评分，专家出版审查仍待进行。下列原日期的冻结/待审状态属于历史，不覆盖现行 `scoring_rules.json` 与 `reference_qualification.json`。本次未新增量子化学计算。

> 2026-10-17 当前状态同步：已有2026-10-14的现行限定科学问题验收证据，本轮复核并同步记录，没有新增量化计算。[当前状态及限制](current_verification_status.json)区分科学覆盖与评分/发布资格。下方旧pending、失败和目录位置按原日期/范围保留，不覆盖后续现行验收；本次整理不自动放行正式评分或发布。

# paper_2a71ffa4b0a90809 验证计算参考（autonomous_research）

专家材料同步整理标记：expert8_20261015；整理时间：2026-10-15T13:34:03.626007+00:00。

## 最新结论与历史状态的关系

## 2026-10-14 当前科学问题验证验收（评分与发布限制单列）

父级验收时间：2026-10-14T18:53:15.752144+00:00。依据[父级15份原生日志与结合自由能/压力复核](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/parent_2a71_review/review.md)及[独立逐规则复核](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/review_2a71_by_lane06.md)，当前公开题面允许的有界结构–活性解释已有完整真实计算支持，核心作者结果合理一致，登记 `current_scope_verified=true`。本登记不认证整篇论文的全部结果，也不赋予官方总分。

五项结果覆盖结合拓扑、七项亲和自由能、C/D构象可达性、同密度面正σ-hole/框架排序及跨A–E/背景的有限解释。七项结合量对图示最大差0.044805530 kcal/mol；C/D自身连接势垒17.612935918/1.589481498，对17.9/2.2差−0.287064082/−0.610518502 kcal/mol。后两差异会影响精确速率，仍保留C高势垒与D易转动的主要区别，不创设统一误差窗口。有限解析模两端松弛连接不被写成长程IRC。

必须保留：新D端点G_syn−G_anti=0.233433524 kcal/mol，并未精确复现作者<0.1；不能用旧约0.0552的供体能差替换新端点零点。D低转动势垒不能解释小时级滞后；C初始群体、精确人口/速率/产率、实验统计显著性和连续ESP面精确极值均未获认证。A受约束剖面29.99558036965对31±1仍为旧诊断失败，现规则明确不是必需目标或整题否决项。

**评分及发布仍未放行。** 现有25分亲和定量项保持 `NUMERICAL_CALIBRATION_BLOCKED`、reserved/unjudged，官方总分为null，`release_ready=false`。未修改科学问题、输入、关键点、结论、规则或容差，未重新分配分数，未移动任务。压力/SMD18来源和C/D连接已补齐；评分元数据中的相应旧待办是待同步记录，不能再解释成实际缺算。独立幅度判据的正式资格仍待后续规则处理，重复QC无法消除这一问题。

本汇总于2026-10-15整理，最新验收取代下方较早的未通过/待算工作组状态；历史字节保留。此处通过只对应当前A–E结构–活性科学问题。正式亲和评分限制、旧A扫描失败和复现版hold均不因本更新而改变。

## 作者路线与实际计算过程

1. 按正文Fig. 5–7及SI S60、S63–S66核对A–E身份、7个构象模型和1个Cl⁻参照。采用Gaussian 16、M06-2X-D3、非I原子6-311+G(d,p)、I用SDD、SMD18(THF)、193.15 K。中性供体0/1，Cl⁻及结合物−1/1。SMD18的I半径2.74 Å由原方法文献支持；不是普通SMD默认I半径。
2. 复用并核收7个供体、7个复合物和Cl⁻的15份原生输出，检查正常结束、身份、频率、温度/压力及G；单原子Cl无振动模。对7项G按同构象配对重组，未以论文能量替换本地组成。
3. 从完整复合物计算I···Cl距离与角度，判定两点/有效单点拓扑。C/D分别优化候选鞍点、读取解析虚模并做正反位移后自由松弛，核查真实syn/anti盆地；C唯一虚频−113.4046、D−17.9493 cm⁻¹，端点分别90/66正模。不是完整长程IRC。
4. 从5个供体的波函数构建10份密度/势cube，在ρ=0.0004 au表面、I轴35°帽内以0.36/0.18 Å网格对照。该离散采样能检验正σ-hole和框架排序，不保证连续面精确极值。
5. 按实验时间逐项对比A–E及背景，不把不同时间产率混为一个活性排名；把C初始群体、无重复误差和精确速率留作解释边界。父级独立重组7项结合G并复算Cl热项压力，另一个验证组逐规则核收。

以上为5个工作阶段，15份结合组成原生输出与构象/ESP证据可逐项追溯；这不是全历史提交作业数或优化迭代数。本次整理没有新量化计算，也不从文件时间推算累计wall/CPU时长。

# 2a71 最小完整父审证据表

核收时间：2026-10-14T14:57:24.407299+00:00。已有需要的量化结果和 C/D 有限模式盆地连接均齐；物理证据支持现题允许的不完全、有限解释。正式25分亲和幅度项仍由原规则保留，不给总分、不新设容差。

原规则：[scoring_rules.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/autonomous_research/paper_2a71ffa4b0a90809/evaluation/scoring_rules.json)（SHA256 `0554a956361c9f321237aefd12163e3826637e3c184ac2e758f518ec6fb42df0`）。

| 原规则 | 作者结果及共同定义 | 本地结果、证据与结论 | 尚存边界 |
|---|---|---|---|
| r_binding_topology | 同一供体与Cl⁻，THF；A/C-syn/D-syn两点I···Cl，B/E有效单点 | 15个供体/复合物/Cl⁻原生组成与频率结果复用并重核hash；完整复合物几何支持相同拓扑 | 无新缺算 |
| r_binding_thermodynamics | 七个指定构象，ΔG=G(供体·Cl⁻)−G(供体)−G(Cl⁻)，193.15 K；S21/S22直接相减 | 下表最大对图示差0.044805530 kcal/mol，七项一位小数均同；1atm由单原子源表热项支持 | 25分原规则NUMERICAL_CALIBRATION_BLOCKED；独立幅度判据待定，不能以0.05当新窗口 |
| r_conformational_origin | C anti→syn 17.9、D 2.2 kcal/mol；A/B为已制备轴异构体 | C 17.612935918（差−0.287064082），D 1.589481498（差−0.610518502）；解析反应模双向位移分别到真实syn/anti最低点，C90/D66正模；不是长IRC | 无通用C/D容差；C低温初始群体仍不唯一。A约束剖面29.99558036965对31±1仍略出界，不抹去 |
| r_electronic_origin | ρ=0.0004 au的I势能极大值A/B/C/D/E=128/114/108/125/117 kJ/mol | 本地129.309510/116.007992/109.738371/126.603178/118.753132；同密度有限网格支持正σ-hole和框架排序 | 有限网格误差保留，无统一ESP容差 |
| r_final | 解释A/B、A/D与C/B/E/背景主要时序对比，不要求完整反应循环 | 两点结合+亲和趋势+预组织共同解释A/B；D易达双点构象且12h接近A；C虽ESP最低仍可双点结合，高转动势垒限制低温平衡；单ESP不能解释时间交叉 | 不把产率当速率；无重复误差、无C初始群体，不能证明唯一动力学或精确产率。该边界符合题面要求陈述不确定性 |

结合自由能全部为 kcal/mol。源表raw来自SI S21/S22；本地raw来自自身原生G。1 M列单独加ΔnRTln(C°RT/p°)，Δn=−1；未用于移动原作者值。

| 催化剂/构象 | 作者图示 | 作者表raw | 本地raw 1atm | 本地−图示 | 本地−表raw | 本地1M（单列） |
|---|---:|---:|---:|---:|---:|---:|
| A | -8.2 | -8.235434337 | -8.209078940 | -0.009078940 | +0.026355397 | -9.269647143 |
| B | -2.6 | -2.560238654 | -2.558356126 | +0.041643874 | +0.001882528 | -3.618924329 |
| C_syn | -5.9 | -5.911139245 | -5.911139246 | -0.011139246 | -0.000000000 | -6.971707449 |
| C_anti | -1.5 | -1.465862131 | -1.455194470 | +0.044805530 | +0.010667661 | -2.515762674 |
| D_syn | -7.1 | -7.131017663 | -7.131017663 | -0.031017663 | -0.000000001 | -8.191585867 |
| D_anti | -2.5 | -2.491212612 | -2.494350159 | +0.005649841 | -0.003137548 | -3.554918363 |
| E | -3.3 | -3.293797229 | -3.284384587 | +0.015615413 | +0.009412642 | -4.344952791 |

来源：[SI PDF](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_2a71ffa4b0a90809/documents/supplementary_001.pdf)，物理第60页/印刷S-60明确M06-2X-D3、6-311+G(d,p)/SDD(I)、SMD18(THF)、振动分析和193.15 K Gibbs；第66页/印刷S-66 Table S22单原子行：`Cl E −460.3624584 H −460.360929 G −460.371527` hartree。页文本另存[60](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/SI_page_60.txt)、[66](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/SI_page_66.txt)。

SMD18来源定义已经闭合：原方法文献10.1002/chem.201803652第2页给I库仑半径2.74 Å、其余相关参数沿用SMD；本体系无Br，所有含I实际输入有ModifySph I2.74。不存在待猜的额外cavity开关。

压力是由源表约束的推断，作者未逐字打印压力不是无约束未知。Cl⁻为单重态单原子，没有振动/转动项；以其35Cl质量34.96885 u、电子简并1，在193.15 K计算：

`q_trans=(2πmkBT/h²)^(3/2)(kBT/p); (H−E)=5kBT/2; (G−E)=−kBT ln(q_trans)`。

1 atm预测G−E=-0.009068298475642 Eh；源表为-0.009068600000035 Eh；差-3.01524392404e-07 Eh。源E保留7位、H/G保留6位，最坏取整差±0.55×10⁻⁶ Eh；反推压力0.999507168 atm，取整区间[0.998608837, 1.000406308] atm。H−E预测0.001529174133704 Eh、源表0.001529399999981 Eh，亦在取整精度内。该范围仅传播印刷取整，不是统计置信区间。

显式常数：kB=1.380649e-23 J/K、h=6.62607015e-34 J·s、u=1.6605390666e-27 kg、Eh=4.3597447222071e-18 J、NA=6.02214076e+23 mol⁻¹；1atm=101325 Pa。1M平动约定等效压力15.849380 atm，与源表不符；单物种1atm→1M加1.0605682035 kcal/mol，两并一结合反应加-1.0605682035，不拟合。

精确热频率原始文件没有全部作者副本，不妨碍上述温度/原始1atm约定与SMD18的来源资格；本地频率/热项来自本地合格驻点。剩余物理不确定性是C低温群体、有限网格及历史A诊断轻微失配，其影响范围已明确，均不需要重复已完成QC。

复算脚本：[build_2a71_evidence_table.py](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/build_2a71_evidence_table.py)；机器可读数值/来源/hash：[minimum_parent_evidence_table.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/minimum_parent_evidence_table.json)；[压力复算](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/chloride_pressure_reproduction.json)。正式评分资格与科学数值一致性分开，原规则原文不变。

## 其余计算量与论文的逐量比较

| 量 | 作者值 | 本地值 | 本地−作者 | 单位 | 判定边界 |
| --- | --- | --- | --- | --- | --- |
| ESP A | 128 | 129.309509778 | +1.309509778 | kJ/mol | ρ0.0004au有限网格σ-hole，局部正势及排序支持；无通用ESP窗口。 |
| ESP B | 114 | 116.007991758 | +2.007991758 | kJ/mol | ρ0.0004au有限网格σ-hole，局部正势及排序支持；无通用ESP窗口。 |
| ESP C | 108 | 109.738370785 | +1.738370785 | kJ/mol | ρ0.0004au有限网格σ-hole，局部正势及排序支持；无通用ESP窗口。 |
| ESP D | 125 | 126.603177524 | +1.603177524 | kJ/mol | ρ0.0004au有限网格σ-hole，局部正势及排序支持；无通用ESP窗口。 |
| ESP E | 117 | 118.753131606 | +1.753131606 | kJ/mol | ρ0.0004au有限网格σ-hole，局部正势及排序支持；无通用ESP窗口。 |
| C TS-own anti | 17.9 | 17.612935918 | -0.287064082 | kcal/mol | 真实有限模式双端；局部机制候选，无新窗口。 |
| D TS-own anti | 2.2 | 1.589481498 | -0.610518502 | kcal/mol | 真实有限模式双端；局部机制候选，无新窗口。 |
| A constrained profile | 31.0 | 29.995580370 | -1.004419630 | kcal/mol | 原31±1窗口稍外；不四舍五入抹除，且只是支持性受约束诊断。 |

C的Gsyn−Ganti=−0.016942756、D=+0.233433524 kcal/mol。D没有精确恢复作者<0.1，不能将其他供体构象差约0.0552混入当前鞍点零点。C/D偏差可能改变精确速率，验收只支持两者构象可达性的主要区别。D低旋转势垒不能解释小时级滞后。

## 15份结合组成原生输出索引

| 组成/运行 | 原生文件 | 原子数 | 电荷/多重度 | G / Eh | 频率数 | 负频 | K / atm |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1a_s129_gd3_193K_smd18_start_optfreq_20260927_hpc20_p6 | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_smd18_start_optfreq_20260927_hpc20_p6/stdout.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_smd18_start_optfreq_20260927_hpc20_p6/input.com>) | 32 | 0/1 | -1906.46902 | 90 | 无 | 193.150/1.00000 |
| 1a_syn_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_syn_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_syn_chloride/input.com>) | 33 | -1/1 | -2366.853629 | 93 | 无 | 193.150/1.00000 |
| free_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/free_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/free_chloride/input.com>) | 1 | -1/1 | -460.371527 | 0 | 无 | 193.150/1.00000 |
| 1a_anti | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_anti/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_anti/input.com>) | 32 | 0/1 | -1906.468792 | 90 | 无 | 193.150/1.00000 |
| 1a_anti_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_anti_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_anti_chloride/input.com>) | 33 | -1/1 | -2366.844396 | 93 | 无 | 193.150/1.00000 |
| 1b_syn | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_syn/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_syn/input.com>) | 32 | 0/1 | -1509.499119 | 90 | 无 | 193.150/1.00000 |
| 1b_syn_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_syn_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_syn_chloride/input.com>) | 33 | -1/1 | -1969.880066 | 93 | 无 | 193.150/1.00000 |
| 1b_anti | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_anti/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_anti/input.com>) | 32 | 0/1 | -1509.498986 | 90 | 无 | 193.150/1.00000 |
| 1b_anti_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_anti_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_anti_chloride/input.com>) | 33 | -1/1 | -1969.872832 | 93 | 无 | 193.150/1.00000 |
| 1c_syn | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_syn/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_syn/input.com>) | 24 | 0/1 | -1354.686268 | 66 | 无 | 193.150/1.00000 |
| 1c_syn_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_syn_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_syn_chloride/input.com>) | 25 | -1/1 | -1815.069159 | 69 | 无 | 193.150/1.00000 |
| 1c_anti | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_anti/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_anti/input.com>) | 24 | 0/1 | -1354.686356 | 66 | 无 | 193.150/1.00000 |
| 1c_anti_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_anti_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_anti_chloride/input.com>) | 25 | -1/1 | -1815.061858 | 69 | 无 | 193.150/1.00000 |
| 1d | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1d/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1d/input.com>) | 22 | 0/1 | -1278.553179 | 60 | 无 | 193.150/1.00000 |
| 1d_chloride | [log](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1d_chloride/gaussian.log>) · [输入](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1d_chloride/input.com>) | 23 | -1/1 | -1738.92994 | 63 | 无 | 193.150/1.00000 |

表中哈希、终止和频率判断来自既有父级原生重读；本次材料整理核对了这些记录和文件路径，没有声称重新执行整套量化。输入路径未在表内直接列出时，沿对应证据JSON中的输入/运行目录追溯。

## 构象、ESP和来源证据入口

- [C双向连接](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/analysis/C_paired_connection.json>)
- [D双向连接](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T030643Z/analysis/halogen_new_results.json>)
- [SMD18来源实现](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/analysis/SMD18_primary_implementation_check.json>)
- [压力热项复算](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/chloride_pressure_reproduction.json>)
- [父级结合原生重读与独立重组](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/parent_2a71_review/binding_native_recheck.json>)
- [独立逐规则复核（含ESP证据）](</inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/review_2a71_by_lane06.md>)

## 当前自主科研五条规则的证据解释

### r_binding_topology

要求计算得到与题设身份一致的溶液配合物，不能只数分子中有几个I或引用晶体距离。SI S63–S66/Fig. S49的作者结果是A、C-syn、D-syn可以同供体两点结合Cl⁻，B、E有效单点。实际15份供体/复合物/Cl原生日志对应7项结合模型；A/C-syn/D-syn的接触约3.204/3.241/3.265 Å，B/E第二I···Cl约9.983/6.613 Å。完整几何支持相同拓扑，这是局部结合模式的真实证据；原规则为人工判定，无新距离阈值。该关键点分配20分，验证不是实际受评agent的得分。

### r_binding_thermodynamics

要求同温度、介质、构象和化学计量下的七项结合G，ΔG=G(供体·Cl⁻)−G(同构象供体)−G(Cl⁻)。作者SI Tables S21/S22的原始热项与本地原生G可直接追溯；对图示最大差0.044805530、对源表raw最大差0.026355397 kcal/mol，各图示一位小数一致。压力通过Cl单原子热项推断为约1 atm；1 M修正另列，不移动原作者值。物理数值已核齐，但原规则明确将全部25分保留为NUMERICAL_CALIBRATION_BLOCKED/reserved/unjudged；本次不能判为25分、0分或改用只看趋势计分，也不能从这组误差反造0.05容差。

### r_conformational_origin

要求区分已制备A/B轴异构体与C/D构象可达性。作者正文Fig. 6给C/D anti→syn势垒17.9/2.2 kcal/mol；本地对各自连接anti为17.612935918/1.589481498，差−0.287064082/−0.610518502。C/D各唯一虚频−113.4046/−17.9493 cm⁻¹，真实解析模式两向位移后自由松弛到syn/anti；C端点90正模、D端点66正模。仅有限盆地连接，不能写成长程IRC。主要高/低势垒区分成立，但D端点Gsyn−Ganti=0.233433524没有精确恢复作者<0.1，不能用旧0.0552重置零点。差值可能显著影响精确速率，故验收仅接受预组织/可达性的有限解释。A约束剖面29.99558036965对31±1仍略出界，但不是本AR必需目标。20分人工规则没有新通用容差。

### r_electronic_origin

正文Fig. 7的同ρ=0.0004 au等密度面I势能极值A–E为128/114/108/125/117 kJ/mol；实际有限网格为129.309510/116.007992/109.738371/126.603178/118.753132，差+1.309510/+2.007992/+1.738371/+1.603178/+1.753132。35°I轴帽内采样、0.36/0.18 Å粗细网格支持正σ-hole及A>D>E>B>C排序，粗细最大变化4.6279 kJ/mol；未证明连续面精确极值收敛。局部电子来源可按原15分人工规则评价，不新设ESP/电荷窗口，也不在此重复给跨系列解释分。

### r_final

要求把局部计算变成能区分系列主要活性差异的解释。A/B结合差−5.65072 kcal/mol，与1/8/12 h的A20/88/87%、B11/54/60%形成有判别力对照；D能低势垒访问双点构象且12 h为86%，接近A87%。C的I势能最低却能双点结合、12 h为69%，高于B60/E65/背景54%，说明单ESP排序不足；8 h C57<E59又限制简单固定活性排序。产率数据是公开实验输入，独立计算部分是结合、结构、转动和电子性质，不是从头预测这些产率。D低转动势垒不能解释小时级滞后，C初始低温群体未唯一确定，未提供重复误差；因此不认证唯一机制、精确速率/产率或完整Mannich循环。该独立跨系列解释分配20分，重复局部结果不得再次得分；也不得借本条解除冻结亲和项。

---

# 历史验证记录（原文保留；当前状态以上方最新汇总为准）

# 2026-10-14 14:33 continuation：独立证据更新（记录时间 2026-10-14T17:10:44.672344+00:00）

**计算分量齐全；公开问题的有限物理解释已具备父审证据。当前 formal reference / scoring hold 仍保留，current_scope_verified=false，最终验收由父级决定。** 本轮没有新增或重复量化计算。

本条明确取代下列历史记录中的“压力约定未知”阻碍。SI S60 指定 193.15 K 的振动/热化学计算；SI S66/Table S22 的单原子 Cl⁻（单重态）给出 E=−460.3624584、H=−460.360929、G=−460.371527 Eh。单原子无振动/转动项，以原生记录的 35Cl 质量 34.96885 u，理想气体平动配分函数 q=(2πmkBT/h²)^(3/2)kBT/p 给出 1 atm 时 G−E=−0.009068298476 Eh，对印刷 −0.009068600000 差 −3.01524×10⁻⁷ Eh，位于印刷精度合并 ±5.5×10⁻⁷ Eh 内；H−E=2.5kBT=0.001529174134 Eh 也一致。反推 p=0.9995071685 atm，按印刷精度传播的区间为 [0.9986088374,1.0004063077] atm。此为来源支持的物理推断，并非作者显式提供的作业压力参数，也不是统计置信区间。1 atm 约定的物理障碍已解除；不用索取完整作者脚本才能承认这一证据。

七项原始 193.15 K / 1 atm 结合自由能 A/B/Csyn/Canti/Dsyn/Danti/E 为 −8.209078940/−2.558356126/−5.911139246/−1.455194470/−7.131017663/−2.494350159/−3.284384587 kcal/mol，对作者图值 −8.2/−2.6/−5.9/−1.5/−7.1/−2.5/−3.3 最大绝对差 0.044805530；全部按一位小数一致，对来源未取整表的最大差为 0.026355397 kcal/mol。这是直接复用的有效原生结果，不是拟合偏移，也不新增 0.05 容差。1 M 结合修正 −1.0605682035 kcal/mol 单列。既有 SMD18 I 半径 2.74 Å 及其余默认参数来源已核，未改变输入。

C/D 的实际解析模两向位移、各自最低点/频率与热项已齐；C/D 自身 anti 势垒 17.612935918/1.589481498 对作者 17.9/2.2，差 −0.287064082/−0.610518502 kcal/mol。它们是有限位移后自由松弛的盆地连接，未冒充长程 IRC。A 历史约束量 29.99558036965 对 31±1 的轻微超界 −1.00441963035 原样保留，它不自动升级为必需的无约束 TS。

结合拓扑、五种 σ-hole ESP、预组织和 C/D 构象可达性共同支持 A–E 主差异的有界解释；A/B 的起始轴异构身份、C/E 时间曲线交叉、空白产物和无重复误差均保留。C 的近简并最低点不能推出 193.15 K 快速平衡，产率不是基元速率。当前公开问题要求陈述这些不确定性，并不要求虚构精确产率或 Mannich 全循环。

实际 scoring_rules.json 仍明确把整个 25 分定量亲和项留为 NUMERICAL_CALIBRATION_BLOCKED / reserved / unjudged，独立幅度判据尚无正式资格；本轮不改评分、不给该项 0 或满分、不重分配分数、不发布 official total。这里应区分“压力/计算分量已有物理证据”和“正式数值参照资格尚未解除”，不能继续把压力未知当作物理未完成。

[minimum_parent_evidence_table.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/minimum_parent_evidence_table.md)；[minimum_parent_evidence_table.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/minimum_parent_evidence_table.json)；[chloride_pressure_reproduction.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T143300Z/chloride_pressure_reproduction.json)；[本轮原生核验](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/verification_lane_01_03_c_returned_native_audit.json)；[16:51平台/原生日志快照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/verification_lane_01_03_c_final_intake.json)。

以下历史原文按原字节保留；当前状态与上述有来源的更正冲突时，以上述更正为准。未修改任务科学指令、输入、评分或既有容差。

---

# 2026-10-14 本轮原生验证更新

量化与C/D连接已齐，无新增QC；整个25分定量项仍NUMERICAL_CALIBRATION_BLOCKED。

current_scope_verified=false；NUMERICAL_CALIBRATION_BLOCKED。



[完整逐目标报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T020500Z/verification_report.md)；[作者/本地数值与差值](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T020500Z/numeric_comparison.json)；[后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261014T020500Z/successor.json)。

---

# 最新独立计算验证 — 2026-10-13T21:10:51.411648+00:00

本轮：continuation_20261013T195300Z / original_group_01。**REFERENCE_QUALIFICATION_BLOCKED；current_scope_verified=false。** 七项结合能接近作者一位小数，C/D连接已齐；25分参照资格仍保留。

本轮新增作业0项，活动0项；新收原生阶段0项。平台状态、诊断Freq和数值接近均不自动等于科学PASS。

完整逐点作者值、本地值、有符号/绝对差、既有容差及可比性：[numeric_comparison.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/numeric_comparison.json)；[验证报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/verification_report.md)；[实时阶段记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/application_completion_audit.json)。

**kp_binding_thermodynamics（REFERENCE_QUALIFICATION_BLOCKED）**：七项原始193.15K/1atm结合自由能对来源最大绝对差0.044805530 kcal/mol，按作者一位小数展示七项均相同；这是接近来源结果的实证，不能再描述为缺可执行计算。所有有效原生日志及配对直接复用。1M修正−1.0605682035单列，未套入原表。实际scoring_rules仍明确整个25分定量项reserved/unjudged；作者原始压力/热项与独立幅度资格仍未恢复。不给0/满分、不拆分或重分配，也不自行设0.05窗口。C/D既有双端不用重算。

C真实−113.4046 cm⁻¹扭转模两向位移均正常优化为32原子、0单重态、90正模式：plus→syn，minus→anti；严格核输入就是原解析模位移，属于有限盆地连接。anti按原子对称映射重原子RMSD0.002938955 Å。TS−自身anti=17.612935918、TS−自身syn=17.629878674 kcal/mol；作者anti势垒17.9，残差−0.287064082，未设数值窗口。D真实双端66正模，plus→syn/minus→anti，自身anti势垒1.589481498对2.2差−0.610518502。支持C/D不同可达性而非凭最低点近简并假设C快速平衡。A历史约束剖面29.99558036965对31±1，差−1.00441963035，原轻微失败保留。

本轮先提交了由真实梯度/曲率/几何支持的必要后继，已回读资源配置并检查首次原生日志；未返回阶段保留等待。原作者方法、模型、电子态、温度、热项、参照与既有容差均未改变。

后继：无需新增量化/IRC；提交已有局部科学结果为父审候选。

后继：父审须处理实际25分reference资格及原压力/热项/独立幅度判据；本轮无权改评分。A原边界失配保留。

[失败→后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/failure_successor_map.json)；[当前覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/coverage.json)；[明确后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/successor.json)；[来源复核及原查询记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/source_search_log.json)。

以下为原验证记录，原字节保留作历史；旧局部PASS不覆盖本轮当前范围。

---

# 最新参考验证状态：2026-10-13T12:13:53.201019+00:00

**current_scope_verified=false；SOURCE_UNRESOLVED_AFTER_SEARCH；PARTIAL_WITH_EXPLICIT_BLOCKERS。**

**kp_binding_topology**（VERIFIED_CANDIDATE）：复用完整带电配合物的原生结果与几何：A/C-syn/D-syn可两点I···Cl结合，B/E为有效单点供体。SMD18原文明确I库仑半径2.74 Å、Br2.60 Å，其余沿用SMD；本组供体均无Br，所有含I既有输入都含ModifySph I2.74，原生日志显示SMD-Coulomb/SMD-CDS。原额外cavity开关疑问已解除；仍须遵守各节点原生及状态资格。

**kp_binding_thermodynamics**（SOURCE_UNRESOLVED_AFTER_SEARCH）：A/B/Csyn/Canti/Dsyn/Danti/E原始193.15K、1atm结合自由能为−8.209079/−2.558356/−5.911139/−1.455194/−7.131018/−2.494350/−3.284385 kcal/mol；条件性1M转换另列−1.060568，不能混用。SMD18参数可核实，但原生作者压力/热项细节与独立幅度准则仍未恢复。当前实际评分合同将整个25分定量亲和项保留未判，不能给0/满分、重分配或官方总分。

**kp_conformational_origin**（VERIFIED_CANDIDATE）：C真实−113.4046 cm⁻¹扭转模两向位移均正常优化为32原子、0单重态、90正模式：plus→syn，minus→anti；严格核输入就是原解析模位移，属于有限盆地连接。anti按原子对称映射重原子RMSD0.002938955 Å。TS−自身anti=17.612935918、TS−自身syn=17.629878674 kcal/mol；作者anti势垒17.9，残差−0.287064082，未设数值窗口。D真实双端66正模，plus→syn/minus→anti，自身anti势垒1.589481498对2.2差−0.610518502。支持C/D不同可达性而非凭最低点近简并假设C快速平衡。A历史约束剖面29.99558036965对31±1，差−1.00441963035，原轻微失败保留。

**kp_electronic_origin**（VERIFIED_CANDIDATE）：复用ρ=0.0004 au有限网格的I势能最大值 A/B/C/D/E=129.309510/116.007992/109.738371/126.603178/118.753132 kJ/mol，对作者128/114/108/125/117；残差+1.309510/+2.007992/+1.738371/+1.603178/+1.753132。支持正σ-hole及框架效应，网格限制保留，不设统一容差。

**c_activity**（VERIFIED_CANDIDATE）：两点几何、亲和趋势及预组织共同支持A/B强对比及A/D较强表现。C的低I势能并不能单独预测其相对B/E活性，时间点交叉及背景产物也排除单描述符充分解释。C/D两端连接已齐，支持温度与制备历史限定的构象可达性比较；没有拟合速率、假定C快速平衡或构造Mannich全循环。25分亲和幅度保留限制不由本结论解除。

原生鞍点：[stationary.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/selected29_20261012T053104Z_group_01/outputs/C_rotation_redundant_recovery/stationary.log)（32原子、0单重态、唯一−113.4046 cm⁻¹扭转模）。两端沿该真实解析模等量反向位移，最大重原子位移0.25 Å；全部原子最大位移0.520900 Å，输入与模式投影残差≤5.37×10⁻¹¹ Å。此为有限位移/松弛盆地连接，不能写成已完成长程积分IRC。

| 方向 | 原生输出 | 原生资格 | 对源构象的重原子RMSD | TS−自身端点 ΔG (kcal/mol) |
|---|---|---|---:|---:|
| plus→syn | [minimum.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T030643Z/outputs/C_rotation_mode_plus/minimum.log) | 退出0；VeryTight完成；90正模；32原子/0单重态 | 0.045924900 Å | 17.629878674 |
| minus→anti | [minimum.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T030643Z/outputs/C_rotation_mode_minus/minimum.log) | 退出0；VeryTight完成；90正模；32原子/0单重态 | 0.002938955 Å | 17.612935918 |

源构象原生参考：[syn](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_syn/gaussian.log)；[anti](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_anti/gaussian.log)。比较以相同元素和重原子成键图为约束，穷举4个允许对称映射并作刚体最小二乘对齐；各映射逐原子表、输入/日志SHA256及能量详见[C_paired_connection.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/analysis/C_paired_connection.json)。

minus 的 anti 最佳映射交换重原子8↔12、9↔11，其余重原子同序；映射后RMSD0.002938955 Å，最大距离矩阵差0.005549283 Å。minus 的I···I=8.331484 Å，与源anti8.329482 Å一致于小构象差；与源syn5.399258 Å明显不同。plus 的syn RMSD0.045924900 Å，I···I=5.485827 Å；它仍保留与源syn的小构象差，不能称完全相同几何。

使用同一M062X-D3/SMD18-THF、193.15 K/1 atm热项和本次自身anti端点，17.612935918对作者17.9 kcal/mol，差−0.287064082；本目标未提供数值窗口，numeric_pass=null。未换端点零点、未拟合差值，25分定量亲和保留项也未因此解除。


本轮新增0项；活动0项；新收原生阶段1项。原生成功不等于科学PASS。

[逐目标结果](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/coverage.json)；[来源补查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/source_search_log.md)；[完整报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/verification_report.md)；[后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/successor.json)。

---

# 历史参考记录（完整保留，不自动认证当前范围）

# 最新参考验证状态：2026-10-13T08:58:00.470986+00:00

**NUMERICAL_CALIBRATION_BLOCKED_AND_PARTIAL；current_scope_verified=false。**

七个氯离子结合量、局部拓扑/ESP/构象及A–E时间–收率对照的有限解释；反应离子对和Mannich C–C过渡态不再是计算必需项。

**kp_binding_topology**（QUALIFIED_LOCAL_WITH_SOURCE_CAVITY_LIMITATION）：复用真实溶液复合物最低点及I···Cl距离/角度，支持A/C-syn/D-syn双点结合及B/E有效单点。所有供体均有两个I，不能将单点作用写成单碘分子。作者SMD18具体腔开关未知，保留I半径2.74 Å的旧实现来源限制。

**kp_binding_thermodynamics**（NUMERICAL_CALIBRATION_BLOCKED）：七个原始1atm结合ΔG按A/B/Csyn/Canti/Dsyn/Danti/E为−8.209079/−2.558356/−5.911139/−1.455194/−7.131018/−2.494350/−3.284385 kcal/mol；来源−8.2/−2.6/−5.9/−1.5/−7.1/−2.5/−3.3。条件性1M修正−1.060568单列。整个25分规则reserved/unjudged，不给零分或满分、不拆分、不输出official total。

**kp_conformational_origin**（PARTIAL_WAITING_HPC）：C有效鞍点单虚频−113.4046 cm−1，相对原anti17.318633975，对来源17.9残差−0.581366025；双向LQA仅1点，均不认定连接。一次真实虚频模±0.25 Å重原子位移最低点测试在运行。D实际双端各66正模式，输入可精确还原TS虚频向量；plus近syn、minus近anti，TS−实际anti1.589481498，对2.2差−0.610518502，无新容差。A旧约束扫描29.99558036965对31±1略超界，只是支持诊断，不改用30.000600。 本轮C-minus已完成优化、正在频率；C-plus仍优化，均为既有作业，不重复提交。未得完整90正模前不认定C连接。

**kp_electronic_origin**（QUALIFIED_LOCAL_WITH_FINITE_GRID_LIMITATION）：复用五个真实波函数/等密度面ESP输出，ρ=0.0004 au、35°I轴帽有限网格最大值约A129.309510/B116.007992/C109.738371/D126.603178/E118.753132 kJ/mol，来源128/114/108/125/117。正σ-hole及相对极化成立；无普遍误差窗，也不把网格灵敏度当全部理论误差。

**c_activity**（SUPPORTED_BOUNDED_INTERPRETATION_C_CONNECTION_PENDING）：A/B的计算双点预组织和结合差与1/8/12h产率20/88/87对11/54/60一致；D具有较强双点结合和正ESP，实际低旋转势垒支持可达性，其13/78/86在12h接近A。C的ESP低于B/E但12h产率69高于60/65；8h为57，低于E59，高于B54，且空白53，不能用单ESP或单结合量解释所有时点。C/E交叉、空白和无重复误差保留；近简并最低点不证明193K快速平衡。C连接待定限制独立构象可达性证据；此解释不认证被保留的25分数值项。

本轮新增作业0；新收原生完成阶段0；活动作业：hpc-job-b219f36f-de83-4d14-bf6c-e306e3d5bf9c, hpc-job-a80ffc82-5e17-44c9-9488-31b90cda7301。

完整对照：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T081239Z/verification_report.md)；逐目标：[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T081239Z/coverage.json)；后继：[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T081239Z/successor.json)。

旧范围、旧PASS不覆盖当前范围。没有改变任务、方法、容差、标准态或能量参照来消除失配。没有发布、移动final/hold或清理存储。

---

# 历史参考记录（原文完整保留，不自动覆盖当前范围）

# 最新参考验证状态：2026-10-13

**NUMERICAL_CALIBRATION_BLOCKED_AND_PARTIAL；当前完整范围未通过（current_scope_verified=false）。**

七个氯离子结合量、局部拓扑/ESP/构象及A–E时间–收率对照的有限解释；反应离子对和Mannich C–C过渡态不再是计算必需项。

**kp_binding_topology**：复用真实溶液复合物最低点及I···Cl距离/角度，支持A/C-syn/D-syn双点结合及B/E有效单点。所有供体均有两个I，不能将单点作用写成单碘分子。作者SMD18具体腔开关未知，保留I半径2.74 Å的旧实现来源限制。

**kp_binding_thermodynamics**：七个原始1atm结合ΔG按A/B/Csyn/Canti/Dsyn/Danti/E为−8.209079/−2.558356/−5.911139/−1.455194/−7.131018/−2.494350/−3.284385 kcal/mol；来源−8.2/−2.6/−5.9/−1.5/−7.1/−2.5/−3.3。条件性1M修正−1.060568单列。整个25分规则reserved/unjudged，不给零分或满分、不拆分、不输出official total。

**kp_conformational_origin**：C有效鞍点单虚频−113.4046 cm−1，相对原anti17.318633975，对来源17.9残差−0.581366025；双向LQA仅1点，均不认定连接。一次真实虚频模±0.25 Å重原子位移最低点测试在运行。D实际双端各66正模式，输入可精确还原TS虚频向量；plus近syn、minus近anti，TS−实际anti1.589481498，对2.2差−0.610518502，无新容差。A旧约束扫描29.99558036965对31±1略超界，只是支持诊断，不改用30.000600。

**kp_electronic_origin**：复用五个真实波函数/等密度面ESP输出，ρ=0.0004 au、35°I轴帽有限网格最大值约A129.309510/B116.007992/C109.738371/D126.603178/E118.753132 kJ/mol，来源128/114/108/125/117。正σ-hole及相对极化成立；无普遍误差窗，也不把网格灵敏度当全部理论误差。

**c_activity**：A/B的计算双点预组织和结合差与1/8/12h产率20/88/87对11/54/60一致；D具有较强双点结合和正ESP，实际低旋转势垒支持可达性，其13/78/86在12h接近A。C的ESP低于B/E但12h产率69高于60/65；8h为57，低于E59，高于B54，且空白53，不能用单ESP或单结合量解释所有时点。C/E交叉、空白和无重复误差保留；近简并最低点不证明193K快速平衡。C连接待定限制独立构象可达性证据；此解释不认证被保留的25分数值项。

本次新增作业：hpc-job-a80ffc82-5e17-44c9-9488-31b90cda7301, hpc-job-b219f36f-de83-4d14-bf6c-e306e3d5bf9c。活动作业：hpc-job-b219f36f-de83-4d14-bf6c-e306e3d5bf9c, hpc-job-a80ffc82-5e17-44c9-9488-31b90cda7301。

逐目标报告：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T030643Z/verification_report.md)；原生证据索引：[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T030643Z/coverage.json)；准确后继：[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/core7_upgrade_20261012T190159Z/attempt_20261013T030643Z/successor.json)。

本轮没有新增数值窗口、改变题面/评分或认证整题PASS；历史局部结果、旧范围和旧PASS仅保留供溯源。

---

# 历史参考记录（以下完整保留，不自动适用于当前范围）

# 升级后计算参考状态

`UPGRADED_NOT_SCIENTIFICALLY_VERIFIED`。科学问题：Why do five defined perfluoroiodoarene catalysts show different activity in the isoquinoline Mukaiyama–Mannich reaction, and which computed structural/electronic quantities explain the difference?

本轮实际重读正文/SI和旧原生日志，新增HPC作业0。已有支持和缺口逐项见 `target_map.json`、`existing_native_evidence_audit.json` 和 `phase1_verification_plan.md`。真实原始记录入口：`docs/verification/group_4/paper_2a71ffa4b0a90809/verification_report.md`；本轮观察到的报告完整副本保存在 `history/observed_verification_report_20261011.md.snapshot`。

- `kp_binding_topology`：需补算。旧8点只含自由A旋转，无Cl。 尚缺：复用A最低点；为各自由框架及Cl复合物生成合理模型、优化并验证，确认一/二点I···Cl几何。
- `kp_binding_thermodynamics`：只需提取/分析＋需补算。旧A自由最低点可复用，其他自由/结合态未见当前范围证据。 尚缺：先用TableS21/S22算源ΔG和标准态项；复用A的E/Hessian，补其余必要自由物种、Cl及结合态；在193.15K/THF同计量比较。
- `kp_conformational_origin`：可直接复用＋只需提取/分析＋需补算。8状态已成功且哈希匹配；主29.99558036965未过31±1，不改变。 尚缺：直接复用历史A旋转链和独立端点敏感性；分析C/D源TS及195/298K时间尺度；只补C/D未覆盖的路径/连接或结合构象，不重复A扫描。
- `kp_electronic_origin`：只需提取/分析＋需补算。A旧波函数可作来源一致电子后处理入口，余者缺。 尚缺：对已完成结构提取ESP/其他有物理定义电子证据；如采用ESP比较，保持同.0004au曲面或显式说明不同定义。
- `c_activity`：需补算。当前没有催化相关底物离子对。 尚缺：选能区分解释的催化剂/反应物组合，建立结合如何影响反应活化/离子对的真实证据；检验结构+电子+结合解释。

旧范围、旧状态和旧容差不得自动替代上述目标验收。当前包通过结构检查不等于科学PASS；新增范围须由第二阶段真实验证。

## 保留历史

本集合升级前无独立verified_computation_reference.md。历史证据位于下列外部原始记录及evaluation/history快照。


<!-- phase2-verification-20261010T231612Z-group03 -->
## 2026-10-11 第二阶段第3组：当前范围的参考计算验证

核查时间：2026-10-11T06:30:24.861276+00:00；状态：**COMPUTING**。当前全部必需科学目标**尚未全部通过**。

七组结合自由能与局部结合拓扑已实际验证：A/Csyn/Dsyn为二点，B/E为一点；七组源值残差不超过.045 kcal/mol。旧A八点扫描29.995580仍未过31±1，未重扫。C/D新互变鞍点搜索已由验证最低点启动；反应性isoquinolinium离子对证据仍缺。 ESP已有5/5个供体的真实波函数曲面结果。 已在结合/电子验证后提交四个实际反应相关离子对候选，尚无完成结果，不计科学覆盖。

本轮开始时审查的包 SHA-256：`0f0648bcc39a81674d471ddfc65f2b8763a602e5f636c75193c2814e53426441`。科学合同及所有非reference载荷的哈希保持不变；本次仅追加本证据段并更新本包manifest。更新后完整包哈希由package_manifest.json和本组completion.json记录，避免自引用哈希。

本次可读作者原文/SI并复用其路线，属于参考计算验证，**不是盲测结果**。历史记录保留；若历史PASS覆盖范围小于当前任务，以本轮逐目标覆盖为准。

|当前目标|状态|来源结果|实际结果|差值、原容差与解释|
|---|---|---|---|---|
|kp_binding_topology|VERIFIED|A,C-syn,D-syn two-point;B/E effectivelyone-point|[{"case": "1a_syn", "contacts": [{"I_index_1based": 23, "Cl_index_1based": 33, "I_Cl_A": 3.2038018732175053, "C_I_Cl_deg": 173.41898546656915}, {"I_index_1based": 28, "Cl_index_1based": 33, "I_Cl_A": 3.203497938843726, "C_I_Cl_deg": 173.4755276152314}]}, {"case": "1a_anti", "contacts": [{"I_index_1based": 23, "Cl_index_1based": 33, "I_Cl_A": 3.144228181592583, "C_I_Cl_deg": 178.79513249561927}, {"I_index_1based": 28, "Cl_index_1based": 33, "I_Cl_A": 9.982891762176628, "C_I_Cl_deg": 49.55652318438069}]}, {"case": "1b_syn", "contacts": [{"I_index_1based": 23, "Cl_index_1based": 33, "I_Cl_A": 3.2409959962321766, "C_I_Cl_deg": 174.12569395107477}, {"I_index_1based": 24, "Cl_index_1based": 33, "I_Cl_A": 3.2409778865300822, "C_I_Cl_deg": 174.1261684426436}]}, {"case": "1b_anti", "contacts": [{"I_index_1based": 23, "Cl_index_1based": 33, "I_Cl_A": 3.187077238977587, "C_I_Cl_deg": 179.37531624228495}, {"I_index_1based": 24, "Cl_index_1based": 33, "I_Cl_A": 10.13733131643003, "C_I_Cl_deg": 50.18911227414559}]}, {"case": "1c_syn", "contacts": [{"I_index_1based": 17, "Cl_index_1based": 25, "I_Cl_A": 3.265350024289739, "C_I_Cl_deg": 167.3912374268999}, {"I_index_1based": 24, "Cl_index_1based": 25, "I_Cl_A": 3.2653400198322378, "C_I_Cl_deg": 167.39139903052185}]}, {"case": "1c_anti", "contacts": [{"I_index_1based": 17, "Cl_index_1based": 25, "I_Cl_A": 9.30631089517651, "C_I_Cl_deg": 39.77532479669098}, {"I_index_1based": 24, "Cl_index_1based": 25, "I_Cl_A": 3.1533848491551106, "C_I_Cl_deg": 178.577668697708}]}, {"case": "1d", "contacts": [{"I_index_1based": 15, "Cl_index_1based": 23, "I_Cl_A": 3.1526331604672944, "C_I_Cl_deg": 178.30707483276683}, {"I_index_1based": 20, "Cl_index_1based": 23, "I_Cl_A": 6.6133388404773275, "C_I_Cl_deg": 64.2484808872517}]}]|所有供体包括E均含2I，one-point是几何作用数。|
|kp_binding_thermodynamics|VERIFIED|{"A": -8.2, "B": -2.6, "C_syn": -5.9, "C_anti": -1.5, "D_syn": -7.1, "D_anti": -2.5, "E": -3.3, "unit": "kcal/mol"}|[{"case": "1a_syn", "deltaG_raw_1atm_kcal_mol": -8.209078939798696, "source_figure_kcal_mol": -8.2, "raw_difference_to_figure_kcal_mol": -0.00907893979869634, "deltaG_1M_kcal_mol": -9.269647143268656}, {"case": "1a_anti", "deltaG_raw_1atm_kcal_mol": -2.558356125787931, "source_figure_kcal_mol": -2.6, "raw_difference_to_figure_kcal_mol": 0.041643874212069054, "deltaG_1M_kcal_mol": -3.618924329257892}, {"case": "1b_syn", "deltaG_raw_1atm_kcal_mol": -5.91113924558884, "source_figure_kcal_mol": -5.9, "raw_difference_to_figure_kcal_mol": -0.011139245588839941, "deltaG_1M_kcal_mol": -6.971707449058801}, {"case": "1b_anti", "deltaG_raw_1atm_kcal_mol": -1.455194470316634, "source_figure_kcal_mol": -1.5, "raw_difference_to_figure_kcal_mol": 0.04480552968336604, "deltaG_1M_kcal_mol": -2.515762673786595}, {"case": "1c_syn", "deltaG_raw_1atm_kcal_mol": -7.131017663226551, "source_figure_kcal_mol": -7.1, "raw_difference_to_figure_kcal_mol": -0.031017663226551306, "deltaG_1M_kcal_mol": -8.191585866696512}, {"case": "1c_anti", "deltaG_raw_1atm_kcal_mol": -2.494350159452415, "source_figure_kcal_mol": -2.5, "raw_difference_to_figure_kcal_mol": 0.005649840547584883, "deltaG_1M_kcal_mol": -3.554918362922376}, {"case": "1d", "deltaG_raw_1atm_kcal_mol": -3.2843845872293813, "source_figure_kcal_mol": -3.3, "raw_difference_to_figure_kcal_mol": 0.015615412770618509, "deltaG_1M_kcal_mol": -4.344952790699342}]|七组真实原始1atm结合ΔG与源图差−.03102至+.04481 kcal/mol，符号与A>Dsyn>Csyn>B/E亲和力顺序恢复。显式1M换算每组再减1.060568 kcal/mol，保留两列；没有新设绝对容差。来源1M措辞另列修复建议。|
|kp_conformational_origin|PARTIAL|{"A_scan": 31, "C_barrier": 17.9, "D_barrier": 2.2, "unit": "kcal/mol"}|{"A_original_scan": 29.99558036965, "independent_A_endpoint_sensitivity": 30.0006004454, "source_Eyring_C_half_life_days": 357.347, "source_Eyring_D_half_life_s": 5.31325533e-11}|A主值差−1.00441963035，原±1.0仍失败；独立端点只是敏感性。C时间尺度来自源势垒计算，非独立鞍点验证。|
|kp_electronic_origin|VERIFIED|{"I_ESP_kJ_mol": [128, 114, 108, 125, 117], "surface_density_au": 0.0004}|[{"donor": "A", "case": "1a_syn", "source_ESP_kJ_mol": 128, "finite_local_ESP_kJ_mol": [129.30950977752696, 129.29133324024028], "difference_to_source_kJ_mol": [1.309509777526955, 1.2913332402402773], "coarse_ESP_kJ_mol": [128.66844218496223, 128.26839997100532], "fine_minus_coarse_kJ_mol": [0.641067592564724, 1.0229332692349544], "source_result": {"path": "docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_syn_ESP_surface/surface_result.json", "sha256": "20c0dc68d94988af23e4dac902c290c6ffaa01e9cb7eb6e5db2b68a1b6538f48"}, "new_SCF_count": 0}, {"donor": "B", "case": "1a_anti", "source_ESP_kJ_mol": 114, "finite_local_ESP_kJ_mol": [115.41039496322178, 116.00799175846599], "difference_to_source_kJ_mol": [1.4103949632217763, 2.007991758465991], "coarse_ESP_kJ_mol": [111.16158850185674, 111.38007450505637], "fine_minus_coarse_kJ_mol": [4.248806461365035, 4.6279172534096205], "source_result": {"path": "docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1a_anti_ESP_surface/surface_result.json", "sha256": "2c882dc1a829ed1601484d175e78de1e6f4be84140fda35e68945aca1ed10751"}, "new_SCF_count": 0}, {"donor": "C", "case": "1b_syn", "source_ESP_kJ_mol": 108, "finite_local_ESP_kJ_mol": [109.23955517408221, 109.7383707854649], "difference_to_source_kJ_mol": [1.2395551740822128, 1.7383707854648947], "coarse_ESP_kJ_mol": [108.83309897110863, 107.56252967200084], "fine_minus_coarse_kJ_mol": [0.40645620297358676, 2.1758411134640596], "source_result": {"path": "docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1b_syn_ESP_surface/surface_result.json", "sha256": "151ba04df8ee8240c0148fb5dddc27a10d41adfef594a1e3f2d266569e4dbbdd"}, "new_SCF_count": 0}, {"donor": "D", "case": "1c_syn", "source_ESP_kJ_mol": 125, "finite_local_ESP_kJ_mol": [126.60317752412965, 126.30964901759907], "difference_to_source_kJ_mol": [1.6031775241296486, 1.309649017599071], "coarse_ESP_kJ_mol": [124.47164998963817, 124.44774973072307], "fine_minus_coarse_kJ_mol": [2.1315275344914824, 1.861899286875996], "source_result": {"path": "docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1c_syn_ESP_surface/surface_result.json", "sha256": "382621641e9136906e4d331f5e1a7cb0f1fa01c35d164702baa6c6c5a21b4a5a"}, "new_SCF_count": 0}, {"donor": "E", "case": "1d", "source_ESP_kJ_mol": 117, "finite_local_ESP_kJ_mol": [118.75313160639898, 118.43819673605047], "difference_to_source_kJ_mol": [1.7531316063989806, 1.4381967360504717], "coarse_ESP_kJ_mol": [115.30896201492477, 116.13626265169955], "fine_minus_coarse_kJ_mol": [3.444169591474207, 2.3019340843509184], "source_result": {"path": "docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/outputs/1d_ESP_surface/surface_result.json", "sha256": "12a424e9ef313245dedf81da5bdc940f49ccdac374e0fd07777352f878b8260c"}, "new_SCF_count": 0}]|五供体均为正σ-hole；细/粗两网格恢复源A>D>E>B>C顺序。35°局部cone与源差值、.36Å抽样敏感性逐一保留，当前细网格残差+1.24至+2.01 kJ/mol。55°可能包含另一I，不能作独立帽归属；未声称精确连续曲面最大值或总方法误差。|
|c_activity|PENDING|Accessible two-pointCl binding supports reactiveionpair activation|已从公开Q/T原子图构建27原子N-Troc异喹啉鎓，四个新有限模型：游离阳离子、28原子氯离子对、A/B各60原子三元离子对；真实优化尚未完成。|D正文86%/8h与图表78%/8h,86%/12h冲突；遵守表格，不把终点收率当速率。|

来源页码/图表、物理定义、输入输出路径及SHA-256见 [coverage.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/coverage.json)；完整结论和逐作业诊断见 [verification_report.md](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/verification_report.md)。
新原始计算记录见 [jobs.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/jobs.json)、[完成结果原生提取](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/new_completed_results.json)、[实际资源与步骤](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/resource_accounting.json)。每个结果JSON链接真实应用日志；平台SUCCEEDED、孤立实频或哈希本身均不构成机理通过。

当前未完成项：

- 七组结合态和五供体ESP已全部完成；尚缺C/D构象连接与反应离子对/活化证据。
- 来源S21/S22原始G差直接给图示ΔG；1atm→1M还差−1.060568 kcal/mol，不能混称。
- 旧A扫描29.99558036965仍在31±1之外；C/D互变及反应性isoquinolinium离子对缺新连接证据。

后继条件、依赖job IDs及一次性恢复入口见 [successor.json](../../../../docs/verification/group_4/paper_2a71ffa4b0a90809/small_molecules_20261010T231612Z_g03/successor.json)。运行/排队作业未标成科学完成；未启动自动周期resume。来源/规则问题见 [本组修复建议](../../../small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/phase2_verification/group_03/repair_proposals.md)，本轮未修改题目或放宽阈值。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`e69a495a69b1ae83fa27422e2283ffe212290e2b720f0efd31d87d96a9ec9897`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_02/reports/paper_2a71ffa4b0a90809/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_02/reports/paper_2a71ffa4b0a90809/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_02/reports/paper_2a71ffa4b0a90809/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。


<!-- autonomy-repair-20261011-verification-ready-group-02-20261012 -->
## 2026-10-12 当前设计下参考计算验证：group_02

核查时间：2026-10-12T02:35:28.019004+00:00。运行状态 **WAITING_HPC**；科学状态 **PARTIAL**，当前全部必需目标尚未全部通过。历史记录保留；上文旧VERIFIED、COMPUTING或QUEUED是当时范围/时间快照，不解除本轮来源与校准阻塞。

复用七组结合和五供体ESP，回收真实QT/Cl/A离子对；A扫描失配和25分校准阻塞保留。C/D转动与反应体系结论仍未闭合。

当前题面SHA256：`0afc723711de0098cb2923761360e9bede35972cf813050a7630844c8b1ec8c5`；本次追加前包SHA256：`eb10c3968c95f8a8989a402169f5db1fe9b983a15488fd66db56a04ed04db55d`。所有冻结设计文件与assignment一致；仅追加本reference、更新对应manifest。更新后的完整包hash记录于manifest和本组manifest_changes，避免自引用。

|当前目标 / 权重|状态|native结果与差值、有效性边界|
|---|---|---|
|kp_binding_topology / 20|SUPPORTED_LOCAL|A/Csyn/Dsyn为两点Cl接触，B/E为有效单点；所有五供体均含2I。 实际溶液优化最低点与源拓扑相符；不以晶体或游离供体距离代替结合复合物。|
|kp_binding_thermodynamics / 25|NUMERICAL_CALIBRATION_BLOCKED|七个匹配构象结合ΔG已从native G重新提取；小残差不解除整个25分规则的校准阻塞。 原始1atm值与源七值残差−0.031018至+0.044806 kcal/mol。每个2→1结合显式1M修正为−1.0605682035；源表未明示标准态。不给符号/排序任意拆分分值，不拟合容差。|
|kp_conformational_origin / 20|PARTIAL_WITH_MISMATCH|A原扫描失配保留；C/D QST2在SCF前失败，改用90°实际扭转种子进行有限局部TS搜索。 A差−1.00441963035 kcal/mol，超过原±1.0；30.0006004454仅独立端点敏感性，不能择近替换。C源势垒对应半衰期约357天，D约5.31e−11 s；这些是源数值的Eyring推论，不是本次TS验证。扫描中−12/−28/−30 cm−1模式也使其不能冒充无约束minimum/TS。|
|kp_electronic_origin / 15|SUPPORTED_LOCAL|五供体正σ-hole及A>D>E>B>C电势顺序复用；逐项有限网格偏差保留。 源A/B/C/D/E为128/114/108/125/117 kJ/mol；有限网格结果相对源约+1.24至+2.01，不能推定通用容差或替代实际反应联系。|
|c_activity / 20|PARTIAL|QT+、QTCl、A–QTCl真实最低点已返回，B–QTCl仍待返回；尚无C–C成键/活动性判别。 新模型无作者反应能数值可直接作差。QT+Cl→QTCl −11.961586；A+QTCl→ternary −10.761160；A+QTCl→ACl+QT +3.752507 kcal/mol (raw1atm)。这些是端点量，不能填作活化自由能；独立20分要求实际C–C化学与判别对照。|

逐项来源页码、定义、原始日志路径和差值见 [coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/coverage.json)；完整说明见 [verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/verification_report.md)。复读原始证据/源PDF/最新父审的记录见 [evidence_read_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/evidence_read_audit.json)。实际新作业为 [jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/jobs.json)，旧作业实时查询为 [inherited_jobs_current.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/inherited_jobs_current.json)，运行资源/步骤/计时/释放状态为 [resource_accounting.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/resource_accounting.json)。

尚未解决：

- 结合幅度25分及官方总分仍NUMERICAL_CALIBRATION_BLOCKED，须独立定义标准态和误差判据。
- A原扫描29.99558036965仍未过31±1；C/D转动TS与连接尚未完成，制备历史/193 K动力学边界仍需处理。
- 真实B反应离子对、C–C成键及有区分度的活动性比较尚未完成；A端点热力学不等于催化活化。
- ESP是0.0004 au有限网格/局部角锥估计，未认证连续曲面全局最大值或通用数值容差。

精确等待/后继ID与一次性收取命令：[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_2a71ffa4b0a90809/autonomy_repair_20261011_verification_ready_group_02/successor.json)；需父进程裁定的问题：[repair_proposals.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/scope_upgrade_execution_20261011T081201Z/verification_ready/group_02/repair_proposals.md)。仅剩长HPC作业及其依赖后继时，以WAITING_HPC结束本次进程；没有定时重启、resume或委派。设计验收、包校验或wrapper结束均不等同科学PASS，本记录不作发布认证。


<!-- core_question_upgrade_20261012T190159Z -->
## 2026-10-12 Approved scope implementation and evidence applicability

**DESIGN_IMPLEMENTED; SCIENTIFICALLY_PARTIAL; RELEASE_NOT_READY.** 本次仅实施父审通过的题目和评价范围，未运行新量化计算；以上历史原文保持字节不变。历史中要求新增真实反应/C–C 证据的段落已由本次范围替代。

公开题面和提交合同取消结合/电子/构象的指定分析清单。隐藏保留作者已有局部结果及有界系列解释；最终 20 分只评价有计算支撑的跨系列判别关系，不重复四个局部结果的分数。不再要求 Mannich C–C TS、QT 反应离子对网络或作者未算的新金标。

最新已读快照：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/selected29_20261012T053104Z_group_01/coverage.json`，2026-10-12T12:38:14.804856+00:00；原生路径及哈希：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/selected29_20261012T053104Z_group_01/analysis/halogen_recomputed.json`。复用七组结合比较和五份电子波函数。源文压力及 SMD18 腔参数仍需资格核实；现有 I 半径 2.74 Å 是有历史出处的实现，不等于作者完整输入已明确。小残差不构成量值容差。

快照中 C/D 连接仍不完整。D 负向端点为 anti-like，相对旧 anti 的重原子 RMSD 为 0.064683 Å；G(TS)−G(新端点)=1.5894814978551326 kcal/mol，作者锚点 2.2，残差 −0.6105185021448676，没有已校准窗口。另一个 D 端点及 C 未闭合。继续前先复用 `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/selected29_20261012T053104Z_group_01/analysis/progress_1110_D_endpoint.json` 和 `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/selected29_20261012T053104Z_group_01/analysis/D_mode_audit.json`。本次未查询实时作业状态。

A 旧约束扫描 29.99558036965 仍不满足 31±1；不舍入、替换、重算求 PASS。保存记录中 B–QTCl 端点虽已完成，与 A/QT 反应端点一起均属 INDEPENDENT_EXTENSION，不列为金标或后续必做验证，也不证明 C–C 反应势垒。

权重保持 20/25/20/15/20。结合能 25 分量值判断及正式总分仍未判；无新增容差、无活动硬数值规则。运行器没有自动资格门控，必须人工维持不可正式计分/不可发布状态。当前物理量、模型、参照、原生成功标记及剩余工作见 `target_map.json`、`reference_validation_plan.md` 和 `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/core_question_upgrade_20261012T190159Z/papers/paper_2a71ffa4b0a90809/verification_delta.json`。包结构通过与设计获批均不表示科学验证通过。

## 2026-10-14 当前科学问题验证验收（评分与发布限制单列）

父级验收时间：2026-10-14T18:53:15.752144+00:00。依据[父级15份原生日志与结合自由能/压力复核](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/parent_2a71_review/review.md)及[独立逐规则复核](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T143300Z/review_2a71_by_lane06.md)，当前公开题面允许的有界结构–活性解释已有完整真实计算支持，核心作者结果合理一致，登记 `current_scope_verified=true`。本登记不认证整篇论文的全部结果，也不赋予官方总分。

五项结果覆盖结合拓扑、七项亲和自由能、C/D构象可达性、同密度面正σ-hole/框架排序及跨A–E/背景的有限解释。七项结合量对图示最大差0.044805530 kcal/mol；C/D自身连接势垒17.612935918/1.589481498，对17.9/2.2差−0.287064082/−0.610518502 kcal/mol。后两差异会影响精确速率，仍保留C高势垒与D易转动的主要区别，不创设统一误差窗口。有限解析模两端松弛连接不被写成长程IRC。

必须保留：新D端点G_syn−G_anti=0.233433524 kcal/mol，并未精确复现作者<0.1；不能用旧约0.0552的供体能差替换新端点零点。D低转动势垒不能解释小时级滞后；C初始群体、精确人口/速率/产率、实验统计显著性和连续ESP面精确极值均未获认证。A受约束剖面29.99558036965对31±1仍为旧诊断失败，现规则明确不是必需目标或整题否决项。

**评分及发布仍未放行。** 现有25分亲和定量项保持 `NUMERICAL_CALIBRATION_BLOCKED`、reserved/unjudged，官方总分为null，`release_ready=false`。未修改科学问题、输入、关键点、结论、规则或容差，未重新分配分数，未移动任务。压力/SMD18来源和C/D连接已补齐；评分元数据中的相应旧待办是待同步记录，不能再解释成实际缺算。独立幅度判据的正式资格仍待后续规则处理，重复QC无法消除这一问题。

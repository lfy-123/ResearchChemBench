# Round-one scope notice — 2026-11-03

The required chemistry begins at supplied Int-3. Int-2 is contextual only; no benzylic activation, peroxide cleavage or upstream radical generation is required. Both product drawings are inputs, not discoveries. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## 2026-10-27 V3 final-result migration

Four independent final results retain balanced cleavage identities, the original hard local acetophenone barrier, kinetic cleavage preference and local benzylic activation. No continuous whole oxidation mechanism is imposed or certified. No new quantum-chemistry or HPC jobs were run. Existing native results are reused only for the matching final claims listed in evidence_map.json; historical PASS labels are not transferred. Unresolved source singlet-oxygen states/capture definitions and uncomputed connecting peroxide chemistry remain outside the approved local scope. Local barriers use connected basins; no yield/branch ratio or polymer prediction is verified. The dated record below is retained verbatim.

> 2026-10-17 当前状态同步：已有2026-10-13的现行限定科学问题验收证据，本轮复核并同步记录，没有新增量化计算。[当前状态及限制](current_verification_status.json)区分科学覆盖与评分/发布资格。下方旧pending、失败和目录位置按原日期/范围保留，不覆盖后续现行验收；本次整理不自动放行正式评分或发布。

<!-- PARENT_B336_ACCEPTANCE_20261013T195300Z -->
# paper_b33676a2051f5e91 当前任务范围的父级验收

时间：2026-10-13T20:07:35.536011+00:00；范围版本：substrate-local-author-results-20261012。

**当前任务计算验证通过（人工逐项验收），不代表论文全部数值逐位相同，也不代表已发布。**

父级重读正文p6 Fig7、pp7–8及SI p23、pp25–29、pp33–38，重新读取18条原生日志路径（16份唯一输出），核验实际方法、原子/态、频率、IRC产物图、同一反应物盆地和热项。全部原生输出正常结束，所有已记录日志hash相符。量化计算全部复用，没有新增HPC任务。

|当前评估量|论文 kcal/mol|实际计算 kcal/mol|差值 kcal/mol|
|---|---:|---:|---:|
|乙基裂解势垒|9.07|10.050192–10.149338|+0.980192–+1.079338|
|甲基裂解势垒|13.39|14.549435–14.648581|+1.159435–+1.258581|
|甲基减乙基势垒|4.32|4.499243|+0.179243|
|Cl夺氢，分离反应物参照|3.23|3.239204|+0.009204|

## 差异的具体来源及判定

SI列出Int3 G=-463.661084 Eh；本地按源构象重算为-463.661083 Eh，差约0.000628 kcal/mol。SI甲基TS4a与本地G均为-463.639734 Eh。可见甲基约1.2 kcal/mol的势垒差不是没有恢复作者泛函、基组或TS。

两条真实IRC连接的Int3端点G为-463.662920/-463.663078 Eh，比源构象更低1.152735/1.251881 kcal/mol。这两个连接端点的全原子RMSD为0.033391 Å，分子图相同、各66正模、G差0.099146 kcal/mol，属于同一近似构象盆地。用这些真实连接的最低点作参照，自然得到表中较高势垒；不能换回数值更接近论文的较高构象当作已证明连接的共同零点。

乙基项满足原±2 kcal/mol规则。甲基项依据现规则的人工审阅要求接受：源TS自由能在打印精度内重现，偏差有明确的参照构象来源，两个连接路径、产物及反应顺序一致。**没有把乙基±2窗口移给甲基，没有新增自动容差。** 两通道共同参照差只偏0.179243 kcal/mol，稳健保留乙基分支较低的结论。HAT按同一分离参照只差0.009204 kcal/mol，可接受为小的数值差异。

## 各关键点的原生支持

- product_fate：乙基路径C12–C13拉开至3.658492 Å，C12–O24缩短至1.213425 Å，得到C8H8O与C2H5两个映射组分；自由基集中在离去碳侧。
- competing_fate：甲基路径C12–C20拉开至3.654006 Å，C12–O24为1.213187 Å，得到C9H10O与CH3；两条反应物侧接同一氧中心C10H13O双重态盆地。
- preferred_barrier/selectivity：两个TS各66模且唯一反应虚频，分别-474.9764/-557.2732 cm⁻¹；从原生G重组两种相同共同参照，乙基始终较低。
- hat_chlorine：TS 25原子0/2、69模，唯一虚频-297.0403 cm⁻¹为C–H断裂/H–Cl形成；正反66/79个非零IRC点均检测盆地，连接R+Cl与R自由基+HCl。独立分离组分最低点合格，按G(TS)-G(R)-G(Cl)计算，未使用预结合络合物的能量作零点。
- evidence_validity/answer：统一BHandHLYP/aug-cc-pVDZ、SMD MeCN、298.15K/1atm谐热项；原子/电荷/多重度、物理定义和对应结论吻合。有限裂解产物轨迹用于判别通道，未冒充无限分离产物热力学。

只认证当前的局部Cl夺氢和竞争裂解解释；不认证光生自由基丰度、完整连续反应网络、产率/分支比或聚合物机制，也不表示被测agent已完成盲自主科研。

可复核数据：[父级原始读取](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261013T195300Z/parent_b336_native_readback.json)、[逐目标人工判定](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261013T195300Z/parent_b336_acceptance.json)。旧阶段记录保留，最新判定以本条为准。

---

以下是保留的历史阶段记录；旧PARTIAL/候选/等待状态已由上方父级验收取代。

# 本轮验证更新：2026-10-13T15:40:02.414594+00:00

轮次：continuation_20261013T094000Z；状态：**VERIFIED_CANDIDATE**；整题 current_scope_verified=false。

HAT LQA双向已原生正常完成66/79点并检测盆地；C12-H24/H24-Cl25正向1.097373/2.775964Å，逆向2.237295/1.301703Å。两侧组分图与合法分离最低点相同，分离参照HAT3.239204对作者3.23，差+0.009204。乙基裂解10.050192–10.149338在9.07±2内；甲基14.549435–14.648581对13.39，差保留。

没有发现当前作者路线仍需新HPC的必需缺项。HAT与甲基/差值没有校准数值窗，保留实际差异供同定义审阅；本报告不发整题自动PASS。

|量|作者|本地|本地−作者|原窗口/资格|
|---|---|---|---|---|
|ethyl_barrier_connected_basin|9.070000|10.050192–10.149338|0.980192–1.079338|±2.000000；保留原结论/原容差，详见coverage|
|methyl_barrier_connected_basin|13.390000|14.549435–14.648581|1.159435–1.258581|未校准；Magnitude discrepancy1.16–1.26 retained; no automatic numericPASS|
|methyl_minus_ethyl|4.320000|4.499243|0.179243|未校准；ethyl lower in both connected-baseline choices|
|Cl_HAT_separated_reference|3.230000|3.239204|0.009204|未校准；两条真实HAT路径66/79点及分离物种映射已完成；3.239204对3.23无新自动窗口|

本轮实际交付：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/verification_report.md)；[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/coverage.json)；[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/jobs.json)；[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/successor.json)。旧有效组件保留；当前新增范围不被旧PASS覆盖。

后继：复核HAT原生路径与分离参照、裂解共同盆地和甲基数值差；必要证据已交付，无重复端点或TS提交。

以下完整保留历史记录；其中旧永久预算停止、旧待连接或已排除模型标签只描述当时状态，当前结论以上述新报告为准。

---

# 最新验证范围与状态：2026-10-13 07:30 UTC有限续接

更新时间：2026-10-13T08:23:11.050136+00:00。**PARTIAL**；current_scope_verified=false。

原两条RCFC路径均应用exit1、零正常终止，正/反仅0/1个已接受IRC点；第1/2点各80次corrector失败，末Delta-x0.067848/0.126939大于0.01。不能用失败校正几何认证端点。已基于此数值诊断提交一次LQA、步长10→5、每10个predictor刷新Hessian的双向恢复，复用合格TS及初始Cartesian Hessian，保持BHandHLYP/aug-cc-pVDZ/SMD MeCN、0/2和25原子。HAT五组分G势垒3.239203905对3.23，差+0.009203905；裂解两通道与共同盆地结果继续复用。

未完成/阻碍：HAT双向实际连接仍未完成。甲基裂解14.54943–14.64858对13.39的差保留，无新窗口；当前未证明全部活动目标。

本轮新作业：hpc-job-c4014f75-4b2d-4d19-8ff1-beefb56d388b (QUEUEING); hpc-job-9d65e74d-2522-49c5-a170-b6d89d407b1a (QUEUEING)。排队中的作业尚无原生应用结果。

逐目标覆盖、作者/本地差异、原容差、累计预算和精确后继：[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T073000Z/verification_report.md)；[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T073000Z/coverage.json)；[successor](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T073000Z/successor.json)。

历史PASS与“当前”措辞仅在各自时间/范围成立，不自动覆盖本次活动范围。以下完整保留此前记录。

---

<!-- GROUP_A_CONTINUATION_20261013T030303Z -->
# 最新验证状态（2026-10-13）

2026-10-13T03:49:16.117291+00:00；任务SHA256 `210be671f213900a59c4435ecf730b2656d62f0c6c2f0827fb0ca51a64ed43b4`；**PARTIAL**；current_scope_verified=false。

两个实际IRC反应物端点均66正模、0/2、氧中心自旋约0.989，映射图为CCC(C)([O])c1ccccc1。两端全原子/重原子RMSD0.03339/0.02402Å，G差0.09915 kcal/mol；旧Int3重原子RMSD约0.49–0.51Å且高约1.15–1.25 kcal/mol。采用共同盆地的两端敏感性区间：乙基10.0502–10.1493、甲基14.5494–14.6486，ΔΔG4.49924。作者氯夺氢R/Cl/R自由基/HCl/TS1已完成，首次两向连接作业接续。 新HAT五组分现均已原生完成：R/R自由基66/63正模，Cl无振动，HCl一正模；TS1有69模且唯一−297.0403cm−1，C12−H24与H24−Cl25距离导数异号。G(TS1)−G(R)−G(Cl)=3.239203905kcal/mol，源3.23，差+0.009203905；首次80点/方向双IRC已提交。 本轮亲核旧两IRC在l1因ReadFC不合法而0SCF/0点失败；现仅改为ReadCartesianFC，2850项Cartesian Hessian和合格TS checkpoint复用。新两方向已进入真实SCF/IRC，未重算TS或两个合格裂解端点。

限定/阻碍：Cl-HAT两方向RCFC路径仍运行，实际连接未完成；原五组分3.239203905对3.23势垒有效组件不等于连接。甲基14.55–14.65对13.39差保留，未新增窗口。

逐目标[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/coverage.json)、[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/verification_report.md)及[精确后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/attempt_20261013T030303Z/successor.json)。

活动作业：hpc-job-c9f22285-bde8-43e2-8911-195b534eff61, hpc-job-b8d33ff7-f85d-407d-8e7e-373eb33cf51e。

以下旧版本原文完整保留为历史；其中旧PASS/“当前”或撤销范围不能覆盖上面的当前判断。未修改任何科学任务/评分/容差。

---

<!-- CORE7_CONTINUATION_GROUP_A_20261012 -->
# 最新验证范围与状态

2026-10-12T20:29:07.460936+00:00；当前任务SHA256 `210be671f213900a59c4435ecf730b2656d62f0c6c2f0827fb0ca51a64ed43b4`。**当前整题未严格通过**；科学状态 `PARTIAL`。

两个实际IRC反应物端点均66正模、0/2、氧中心自旋约0.989，映射图为CCC(C)([O])c1ccccc1。两端全原子/重原子RMSD0.03339/0.02402Å，G差0.09915 kcal/mol；旧Int3重原子RMSD约0.49–0.51Å且高约1.15–1.25 kcal/mol。采用共同盆地的两端敏感性区间：乙基10.0502–10.1493、甲基14.5494–14.6486，ΔΔG4.49924。作者氯夺氢R/Cl/R自由基/HCl/TS1已完成，首次两向连接作业接续。 新HAT五组分现均已原生完成：R/R自由基66/63正模，Cl无振动，HCl一正模；TS1有69模且唯一−297.0403cm−1，C12−H24与H24−Cl25距离导数异号。G(TS1)−G(R)−G(Cl)=3.239203905kcal/mol，源3.23，差+0.009203905；首次80点/方向双IRC已提交。

阻碍：氯夺氢双向连接待完成；鞍点与各独立最低点尚不足替代连接。3.23、甲基13.39及差4.32无新数值窗，不能自动数字通过。底物自由基S²=0.8213→0.7536的自旋极化已记录。

本轮报告：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/verification_report.md；逐目标覆盖：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/coverage.json；作业及后继：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/core7_upgrade_20261012T190159Z/successor.json。

当前活动作业：hpc-job-063baecf-4d31-4c92-94d7-056ccef4a7fe, hpc-job-961451c7-40a3-46e8-a5f8-dd31dae8fb99。

下列旧版本完整保留为历史；其中PASS、“当前”或旧范围结论不自动覆盖本轮实际合同。

---

# Current approved scope — 2026-10-12 implementation

Scope version: `substrate-local-author-results-20261012`. **Design implemented; scientifically verified=false; release_ready=false.** This notice supersedes historical scope/READY/PASS/migration statements below. All historical numerical/native evidence is retained, with its original scope. The task has not been moved.

The public input is now neutral sec-butylbenzene plus measured conditions and controls. Chlorine HAT is a new active author-supported local result; singlet-oxygen HAT is blocked pending author-state traceability and has no active scoring rule. Disputed oxygen-capture numbers and unreported connecting TS/full cycles are excluded. The 9.07 +/-2.0 ethyl window is unchanged; new numeric windows have not been introduced. See [qualification](qualification.json), [target map](target_map.json) and [validation plan](validation_plan.json).

The latest scientific audit is the 2026-10-12T15:20:40.004320+00:00 record under `docs/verification/small_molecules_autonomous_research/paper_b33676a2051f5e91/remaining24_20261012T134810Z_group_A`. It supports both finite scission product connections, but assigns PARTIAL to the quantitative common-reference comparison: the IRC reactant-side electronic energies differ from archived Int3. The old 8.897457/13.396700 and difference 4.499243 remain conditional values, not newly certified barriers. Source targets remain 9.07/13.39 and contextual 4.32.

Local run-status files subsequently record the existing methyl endpoint job finishing at 16:18:28 UTC and ethyl endpoint job at 16:23:30 UTC, both `terminal_requires_scientific_review`, with `scientific_pass=false`. These are later operational observations, not scientific acceptance. Native `gaussian.log`, checkpoint and run-status files exist for both endpoints. The next verification action is to inspect those existing outputs, verify minima/state/thermochemistry and map the basins; no duplicate endpoint or existing TS/IRC submission is needed.

The native log paths, source coordinates/pages, expected quantities, existing job IDs and required success markers are indexed in validation_plan.json and the latest audit's quantitative_analysis.json/native_intake.json. Product-side IRC endpoints are finite dissociation geometries, not separated-product thermodynamics. The broader public input does not turn author-informed reference replay into a successful autonomous blind run.

This update records an implemented scope change and reads existing evidence. It does not execute a calculation, change tolerances, resolve blocked source definitions or award any new scientific PASS.

---

# 已验证成功计算链：Int-3 β-scission TS / IRC

- 论文 ID：`paper_b33676a2051f5e91`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1039/d5gc05996h`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_4](../../../../docs/verification/group_4/paper_b33676a2051f5e91)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_4.md)
- 最新已归档科学状态：READY / PASS / MATCH / QUALIFIED（Int-3 指定 β-scission 通道；产物侧 IRC 为有限路径）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_b33676a2051f5e91)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 按 SI 的 Int-3/TS-4b 身份核对 24 原子 C10H13O 中性自由基双重态及原子映射。使用作者结构作为验证起点，不把由图感知失真产生的 radical_electrons=7 当作真实电子态。

2. 用 Gaussian UBHandHLYP/aug-cc-pVDZ、SMD 乙腈、298.15 K 分别完成 Int-3 的 Opt/Freq 和目标 TS 的 Opt=(TS,CalcFC,…)/Freq。SCRF 在输入续行中，不能只读取首行后误判缺少溶剂；SI 不要求 QST3。

3. 反应物 66 个模式均为实频，TS 66 个模式中仅一个虚频 −474.9764 cm⁻¹。对负模式位移做键长投影，C12–C13 延长与 C12–O24 缩短对应目标 β-scission。

4. 从该 TS 分别运行同级 IRC=(LQA,CalcFC,Forward/Reverse,MaxPoints=80,StepSize=5)。forward 在第 64 点检测到 Int-3 侧极小值；reverse 在 80 点上限正常结束，进入乙酰苯+乙基自由基分离区。用分子图、C–C/C=O 距离和乙基自旋支持通道归属。

5. 从反应物与 TS 的同温度 Gibbs 总能计算 (G_TS−G_Int3)×627.509474；不以未优化的分离产物端点能量构造本任务没有验证的产物解离自由能。

6. 将势垒、单虚频/位移、双向通道及范围限定逐项核对 evaluator，保留产物侧未验证有限距离极小值的事实。

## 3. 实际结果与支持的结论

| 量 | 实际值 |
|---|---:|
| G(Int-3) / Eh | −463.661083 |
| G(TS) / Eh | −463.646904 |
| ΔG‡ / kcal mol⁻¹ | 8.8974568327（参考 9.07 ± 2.0） |
| C12–C13：Int-3 → TS / Å | 1.53763364 → 2.06424080 |
| C12–O24：Int-3 → TS / Å | 1.39731876 → 1.25383293 |
| reverse 终点 C12–C13 / C12–O24 / Å | 3.65849248 / 1.21342529 |
| reverse 终点乙基自旋 | 0.998047 |

支持指定 Int-3 → 乙酰苯 + 乙基自由基通道及其 TS 相对势垒。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| reactant | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_0ca67f7e40bd440eab8861701bf0d8b3/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_0ca67f7e40bd440eab8861701bf0d8b3/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| ts | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_3fed45618b73427f8c87b8ae02bd96fc/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_3fed45618b73427f8c87b8ae02bd96fc/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| forward | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_forward_lqa_irc_20260914_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_forward_lqa_irc_20260914_hpc20_p6/stdout.log) | Gaussian 正常终止标记 1 处 |
| reverse | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_reverse_lqa_irc_20260914_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_reverse_lqa_irc_20260914_hpc20_p6/stdout.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_channel_closure_20260915.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/author_channel_closure_20260915.json)
- [provenance/evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/evaluation_task_qualification.json)
- [report/results.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/report/results.json)
- [verification_report.md](../../../../docs/verification/group_4/paper_b33676a2051f5e91/verification_report.md)
- [prepare_lqa_recovery_20260914.py](../../../../docs/verification/group_4/paper_b33676a2051f5e91/prepare_lqa_recovery_20260914.py)
- [finalize_author_channel_20260915.py](../../../../docs/verification/group_4/paper_b33676a2051f5e91/finalize_author_channel_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- reverse 是正常终止但达到 MaxPoints 的有限 IRC，不是无限分离极限，也没有产物端点的后续 Opt/Freq；这不被伪写成完整产物极小值验证。
- 仅验证 Int-3 乙基通道，不声称计算了竞争甲基通道或完整聚合物机制。
- group 总表的乙基自旋写成 0.998147，本归档采用专门原始审计 JSON 的 0.998047，不放大这一转录差异。

## 7. 成功阶段计时

四个有效阶段 elapsed 分别为 36517.1、221250.5、6654.0、6673.5 s，合计 271095.1 s（75.3042 h）；CPU 合计 328625.6 s（91.2849 核时）。均排除失败/被替代路径，wall 合计非日历工期。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

AR 当前获准开放通道。历史链仅验证 acetophenone+ethyl 支路的可计算性及源参考势垒；其他通道由 agent 的真实计算/映射/比较证据评估，不套用该数值、不宣称已穷尽所有通道。作者通道仍提供一个可行解，不要求历史验证模拟未知答案探索。

## Evidence scope review (2026-09-19)

The archived ethyl-scission chain supports the PR/local-path comparison. It does not itself establish comparison of chemically different AR beta-scission channels. Different starting guesses for the same mapped cleavage remain one channel unless distinct discriminating evidence is provided.


<!-- phase2_verification_group02_20261011 -->

## 2026-10-11 第二阶段独立参考验证（第 2 组）

记录时间：2026-10-11T06:11:06.052366+00:00。当前科学状态：**QUEUED**。

旧乙基通道有效，新增甲基TS为13.396700kcal/mol且虚模正确；原两项IRC启动时因配额失败，已复用合格TS检查点提交两个受存储保护的恢复作业，当前AR比较尚未闭合。

本节针对当前自主科研题目的必需关键点与结论；历史局部 PASS 不自动迁移。本轮可查作者资料，是独立参考计算验证，不是盲测执行。

验证起始包 hash：`cb748c9574620be9a2c5756fe83a7cfd1599942b1c4bcb59c4b4b7539b1d245e`。固定科学契约 hash：`02d520a61b0162b70fe5a5afd6642448a1aed2d10347afd9d5dc8c016f10853a`（排除本 reference 与 manifest）。追加后的包 hash 由 package_manifest.json 和本组 completion.json 记录，避免自引用。

来源定位：Main PDF7 Fig.9及PDF8讨论：acetophenone+ethyl对propiophenone+methyl，9.07/13.39kcal/mol；SI PDF23方法、PDF33 Int3、PDF34 TS4a、PDF35 TS4b。

物理定义与条件：Int3 C10H13O，24原子0/2；UBHandHLYP/aug-cc-pVDZ/SMD MeCN，298.15K/1atm，同一Int3 G零点。

### 逐目标结果

| ID | 状态 | 真实结果、差值与接受边界 |
|---|---|---|
| `ar_process_search` | PARTIAL | 真实两烷基裂解有限比较已开展；竞争通道的两个IRC恢复作业已提交，连接尚缺。 |
| `ar_process_validation` | PARTIAL | 两TS/共同Int3频率已验收；甲基TS路径尚无有效回传。 |
| `ar_result_channel` | PARTIAL | 乙基通道有效，候选甲基TS高4.499243kcal/mol但比较结论尚以IRC为条件。 |
| `ar_result_barrier` | PASS | 旧乙基通道8.897457 vs9.07±2.0；新竞争13.396700 vs13.39，待连接后才作完整选择性比较。 |
| `ar_final` | PARTIAL | 历史单通道PASS不能认证当前不同通道比较；必须验收恢复IRC的实际路径。 |

### 原生核查与来源差异

- 旧Int3/TS4b/双向IRC四日志重新提取。Int3=−463.661083Eh、TS4b=−463.646904Eh；势垒8.897457对9.07±2.0kcal/mol，差−0.172543。最低点66正模，TS唯一−474.9764cm−1；C12–C13虚模导数+1.068429、C12–O24−.174643（任意符号）。

- 旧IRC一侧回到Int3，另一侧80点到有限分离区：C12–C13=3.658492Å、C12–O24=1.213425Å；该端点是乙酰苯+乙基连接，不是完整验证的分离产物最低点。

- 当前AR要求不同化学裂解通道的实际比较，历史PR只覆盖乙基。新甲基TS4a正常Opt/Freq，G−463.639734Eh、唯一−557.2732cm−1，13.396700kcal/mol对源13.39差+.006700；和乙基局部势垒差4.499243。此源竞争值没有另造数值容差。

- 新负模C12–C20导数+1.167483，而C12–C13−.058046、C12–O24−.189997，明确指向甲基断裂/C=O形成。已从该checkpoint提交自身CalcFC的80点LQA双向IRC；通道仍需同一Int3连接，不能以频率/标量代替。

- 最新原生收取：TS4a_IRC_forward, TS4a_IRC_reverse 已终态且未产生所需有效结果；详见failure_intake.json。平台SUCCEEDED不是科学成功。后继必须先恢复存储空间，再做有检查点的有限恢复，未自动重试。

- 05:58UTC约108GiB共享空间恢复且64MiB写入校验通过后，仅对这两个24原子IRC各作一次显式恢复：1f414ce3（forward）与08e1cf2c（reverse）。输入及合格父TS检查点SHA256不变；原forward未完成seed拷贝，reverse未过Link0，没有有效IRC路径可续接。运行存储阈值见本组storage_recovery_plan.json，非无限自动重试。

### 原始证据与计算执行

完整证据链：[verification_report.md](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/verification_report.md), [coverage.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/coverage.json), [resource_accounting.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/resource_accounting.json), [jobs.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/jobs.json), [next_steps.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/next_steps.json)。

coverage 中记录源 PDF hash 和逐目标定义；audit JSON 保存原生日志路径、SHA256、route、原子/状态、优化/SCF/IRC 步数、频率、关键行与软件计时。resource_accounting 另保留实际资源、UTC 作业时间线、释放状态及 runner 计时，未把缺失字段估算补齐。

本篇独立重新提取文件：[alternative_saddle_comparison.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/alternative_saddle_comparison.json), [failure_intake.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/failure_intake.json), [independent_channel_recheck.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/independent_channel_recheck.json), [reused_native_audit.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/reused_native_audit.json)。

| Case | Job ID | 平台状态 |
|---|---|---|
| TS4a_IRC_forward | `hpc-job-8c71b7a0-bd42-4771-a0cd-4671b39e0afb` | SUCCEEDED |
| TS4a_IRC_reverse | `hpc-job-5aa06701-d5ff-4767-9323-c714d7b7a8ba` | SUCCEEDED |
| alternative_TS4a_optfreq | `hpc-job-49740ddc-c2c6-4359-a28f-50e1d31b7c9f` | SUCCEEDED |
| TS4a_IRC_reverse_storage_recovery1 | `hpc-job-08e1cf2c-84a0-4504-ae01-940155d637d4` | QUEUEING |
| TS4a_IRC_forward_storage_recovery1 | `hpc-job-1f414ce3-f8a9-4cc8-bdf0-4092fe288777` | QUEUEING |

平台 SUCCEEDED 或正常退出不单独构成科学 PASS。配额失败尝试保留；新恢复作业采用独立目录/ID，实际结果收取前不得当作完成。

### 未完成项及后继

- 原两项IRC遇存储配额失败；一次受保护恢复已提交，尚不能把提交当路径成功。

- 甲基TS4a必须双向连接同一Int3与propiophenone+methyl。

- 有限IRC端点与分离产物驻点/热力学保持区分，不外推全聚合物反应或全局最优。

逐步恢复条件见 [next_steps.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/small_molecules_20261010T231612Z_g02/next_steps.json)；共享存储问题及有限恢复见 [storage_blocker.json](../../../small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/phase2_verification/group_02/storage_blocker.json) 和 [storage_recovery_plan.json](../../../small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/phase2_verification/group_02/storage_recovery_plan.json)。

契约/来源/发布问题单独记录于 [repair_proposals.md](../../../small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/phase2_verification/group_02/repair_proposals.md)。本次未更改任务、评分、容差或分组。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`032788cd00cbe5788b7344d7602f7aa44de55e6e835160d2ecaf4f21fe04247e`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_b33676a2051f5e91/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_b33676a2051f5e91/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_b33676a2051f5e91/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。

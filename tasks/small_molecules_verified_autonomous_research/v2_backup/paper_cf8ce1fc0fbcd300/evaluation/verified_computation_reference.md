## 2026-10-23 科学分V2维护副本

当前私有评分为`paper_science_v2`，共7个二元科学项，中间关键节点50分、最终结论50分，总计100分。全部过程分已删除。新规则不设数值硬窗口，不改变既有定性验收或数值差异记录。公开输入保持原样，题面中旧过程分/60+40措辞不代表本维护副本实际计分，作为专家待审文字遗留披露。科学评分资格与发布资格分开，见`reference_qualification.json`。

## 2026-10-23 当前科学问题验证过程与结果汇总

当前AR状态：`PROVISIONAL_PASS_QUALITATIVE`；这是已完成独立审查后的定性验收，不是尚未验收的候选。严格整题数值复现未登记，数值偏差和实现差异保留供专家判断。本节整合既有实际计算，没有新增量化计算。

### 方法、模型与执行过程

M06-2X/6-311+G(d,p)/SMD-DCM优化/频率与作者明确层级一致。实际Gaussian16 C.01，SI引用A.03；原坐标未提供，依据分子图/图S9重建。实际298.15 K、1 atm RRHO，来源温压、网格及热化学约定未完整报告。

1. 独立构建三个中性甲氧基异构体并优化/频率，各24原子、66个正频率，分子连接图与题面一致。
2. 按作者环丙烯鎓/甲醇模型构建三个+1单重态进攻TS，各25原子、唯一反应虚频；最终种子距离约束已解除。
3. 独立核验C–O反应振型及分子图，对同组成TS比较相对G，再单独比较中性产物G；两组零点不混用。没有把三个TS相对高度称为绝对活化势垒。

### 论文与计算数值对照

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|TS1′−TS1|1.3|1.583206|+0.283206|kcal/mol|
|TS1″−TS1|7.1|6.618970|−0.481030|kcal/mol|
|minor−major产物G|3.2|2.845755|−0.354245|kcal/mol|
|comparator−major产物G|7.2|7.161766|−0.038234|kcal/mol|
|TS1成键C–O距离|1.910|1.866986|−0.043014|Å|
|TS1最短OH···F接触|2.390|2.287419|−0.102581|Å|

### 定性结论与保留项

形成通道与产物稳定性均支持major优先；minor到major自由能下降，支持观察到的重分配方向。全部相对能排序一致，最大绝对能差0.481030 kcal/mol。

- 软件修订版、结构重建及未报告热化学细节限制精确数值复现，不表示存在既定数值门槛失败。
- 反应模式和分子图提供局部连接证据，未完成松弛IRC或完整酸交换网络。
- OH···F近接不等于氢键因果能量分解；五分钟端点不证明完全平衡，未检出不等于严格零浓度。
- 原文上游照光时长和SI部分重分配实验文字存在不一致，不能混为同一条件的定量动力学。

### 原生结果、独立复核及来源

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/acceptance_audit.md)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/acceptance_audit.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [independent_native_checks.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/independent_native_checks.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/main.pdf)：PDF页序（1-based）7,8。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/supplementary_001.pdf)：PDF页序（1-based）54,55,58。
- [supplementary_002.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_cf8ce1fc0fbcd300/documents/supplementary_002.pdf)：PDF页序（1-based）43,44,47。

来源方法未报告项、数值差异与题外未计算项目不能混为同一类问题。下方原有记录按日期保留，旧candidate/pending仅表示当时状态，不覆盖本节引用的最新父级验收。

---

## 历史验证记录（原文保留）

<!-- parent-acceptance-20261022T2343Z -->
## 父级独立审查验收（2026-10-23 UTC）

当前模式状态：`PROVISIONAL_PASS_QUALITATIVE`。当前 AR/PR 共享科学问题的全部必要定性结论已有有效计算支持，无需为本题补充新的量化计算。此状态不等于精确数值/原软件版本复现，不修改评分、容差或发布状态。下方“候选待审”描述为此前过程记录，以本段父级结论为准。

三种中性产物均正常优化/频率、零虚频且分子图匹配；三条加成TS均为唯一负频且沿目标C–O成键方向。实际M06-2X/6-311+G(d,p)/SMD(DCM)与作者明确电子结构方法一致。

| 比较量（kcal/mol） | 作者 | 计算 | 计算−作者 |
|---|---:|---:|---:|
| TS1′−TS1 | 1.3 | 1.583206 | +0.283206 |
| TS1″−TS1 | 7.1 | 6.618970 | −0.481030 |
| 次要产物−主要产物 | 3.2 | 2.845755 | −0.354245 |
| 比较产物−主要产物 | 7.2 | 7.161766 | −0.038234 |

形成偏好、产物稳定性及次要向主要异构体重新分配的定性方向均支持；不声称精确速率、收率、完全平衡、唯一全机理或氢键因果分解。当前语义评分没有隐藏数值阈值，“严格数值未登记”不表示某一既有数值门槛失败。

独立原文/原生日志审查：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_cf8/acceptance_audit.json`；父级登记：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/parent_acceptance_decision.json`。全部比较值、结构/振型和日志哈希见该审查及下方计算记录。

保留的实现差异与边界：

- Gaussian 16 C.01 used versus bibliography A.03; same explicit method but not exact revision replication.
- Original Cartesian decks unavailable; independent conformers reconstructed, not exhaustive conformer free energies.
- Thermochemical temperature, standard state, grid and thresholds unspecified by authors; actual 298.15 K/1 atm/RRHO/UltraFine settings disclosed.
- OH...F proximity agrees with the author interaction picture, but causal hydrogen-bond or steric energy decomposition is not computed and is optional in current evaluator.
- No relaxed IRC or complete acid-exchange network; supported claim is conditional competition within the disclosed source model.
- Source experimental prose/scheme discrepancies retained: gram-scale illumination 12 vs 24 h; SI redistribution prose has substrate/equivalent/concentration/catalyst reporting inconsistencies, while main/SI drawings define the task endpoint. No theoretical rate/equilibrium assertion is inferred.

<!-- end-parent-acceptance-20261022T2343Z -->

# Independent computation verification — 2026-10-22 follow-up

Current shared AR/PR status: PROVISIONAL_PASS_QUALITATIVE **candidate, pending independent parent review**; no registered acceptance or strict numeric pass.

Assigned original snapshot: `eb59006260ee02fb95bbc9265585f95ba32a8d7e0dbed0643db83c601aa14378`. Evidence directory: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T2343Z`.


结论：当前 AR/PR 共享科学问题已具备 **PROVISIONAL_PASS_QUALITATIVE 候选**证据，待父级独立审查；不称严格数值通过。

作者路线 M06-2X/6-311+G(d,p)、SMD(DCM) 已执行。三种中性产物均正常优化/频率、零虚频且完整键图与题面分子图一致。三条 +1 单重态环丙烯鎓/MeOH 加成通道均无约束 TS 优化正常完成，且只有一个虚频（−221.52、−258.40、−211.65 cm⁻¹）。源资料未提供 XYZ，采用目标产物骨架和 Figure S9 加成方向重建；热化学默认298.15 K/1 atm，作者未明确给出，同组成差分不引入净浓度校正。

**CC_FORMATION_SELECTIVITY：形成阶段倾向已得到通道计算支持。** TS1 在 CF2H 所连环碳进攻，TS1′ 在带 H 的环碳进攻，TS1″ 在苯基所连环碳进攻；逐原子检查三元环及其取代连接均保持，仅预期成键 C3–O2 随距离阈值变化。新增 O2–H25 保持。三个唯一虚频均以 MeOH 沿 C3–O2 运动为主，正负位移分别缩短/拉长该键；不存在把其他扭转模式误称成键 TS 的情况。最终成键距离 1.867/1.928/1.801 Å，与源图1.91/1.94/1.82 Å相近。

相对 TS RRHO G 为 0、+1.583206、+6.618970 kcal/mol，作者0、+1.3、+7.1；非零项有符号差+0.283206/−0.481030。共同组成/同一反应物库使该比较对应三条来源通道的相对形成难度，支持主要产物及未观察到比较产物的方向。TS1 的最近 O–H···F 为2.287 Å（作者2.39），与额外近接稳定相容；另外两条没有相似的近F接触。几何不能独立证明该相互作用的因果能量贡献；空间接近/排斥解释仍是条件性解释。TS1′ 的“甲基排斥”来自 MeOH 甲基与苯基环境，不是把环碳误认为带甲基取代。

**CC_PRODUCT_STABILITY：产物热力学排序独立成立。** major/minor/comparator 的相对 G=0/+2.845755/+7.161766 kcal/mol，作者0/+3.2/+7.2；差−0.354245/−0.038234。相同原子组成、电荷和溶剂的比较说明主要产物也是最稳定产物，次要异构体向其重新分配在热力学上有利。

**CC_CONNECTED_ACCOUNT：形成倾向与产物稳定性方向一致，但不把单端点当平衡。** 这两组独立计算同时支持较易形成且较稳定的主要异构体，低形成倾向/较高自由能与第三异构体未观察到相容。91% 五分钟次要→主要重分配只能说明该条件下可重分配且趋势一致，不证明完全平衡、唯一机制、精确平衡常数或速率。比较限于作者提出的酸/甲醇阶段模型，不推算上游光化学或完整酸交换网络。

反应模式与保留骨架已足以确定本题局部加成通道；本轮不追加全 IRC。没有声称通过完整 IRC 确证唯一全局连接，没有计算绝对加成势垒或中性产物去质子化全路径。数量差异、重建构象与未指定热标准态完整保留，不放宽或修改评分容差。

证据：completed_verified_stages.json、transition_state_analysis.json（原子图、位移向量、模式投影、接触距离及原生日志哈希）、author_comparison.json。产物作业3d2f37b9及TS作业87b8bbd1均正常完成且释放；当前需要父级审查，无必要新增计算。


Native completed stages (final-state validity only; TS reaction interpretation and minima identity are separate):

| Case | Stage | Electronic energy / Eh | Native RRHO G / Eh | Imaginary modes | Wall seconds |
|---|---|---:|---:|---:|---:|
| methoxy_major | optfreq | -699.953232105 | -699.808568 | 0 | 526.14 |
| methoxy_minor | optfreq | -699.947548909 | -699.804033 | 0 | 575.49 |
| methoxy_comparator | optfreq | -699.94070995 | -699.797155 | 0 | 775.16 |
| TS1 | optfreq | -700.35271811 | -700.196046 | 1 | 575.96 |
| TS1prime | optfreq | -700.347927681 | -700.193523 | 1 | 513.62 |
| TS1doubleprime | optfreq | -700.339559443 | -700.185498 | 1 | 590.34 |

Author comparison (calculated minus author; numerical tolerances unmodified):

| Quantity | Author | Calculated | Signed difference | Absolute difference | Units |
|---|---:|---:|---:|---:|---|
| methoxy_minor minus methoxy_major RRHO G | 3.200000 | 2.845755 | -0.354245 | 0.354245 | kcal/mol |
| methoxy_comparator minus methoxy_major RRHO G | 7.200000 | 7.161766 | -0.038234 | 0.038234 | kcal/mol |
| TS1 forming C-O distance | 1.910000 | 1.866986 | -0.043014 | 0.043014 | angstrom |
| TS1 relative TS RRHO G | 0.000000 | 0.000000 | +0.000000 | 0.000000 | kcal/mol |
| TS1prime forming C-O distance | 1.940000 | 1.927812 | -0.012188 | 0.012188 | angstrom |
| TS1prime relative TS RRHO G | 1.300000 | 1.583206 | +0.283206 | 0.283206 | kcal/mol |
| TS1doubleprime forming C-O distance | 1.820000 | 1.800977 | -0.019023 | 0.019023 | angstrom |
| TS1doubleprime relative TS RRHO G | 7.100000 | 6.618970 | -0.481030 | 0.481030 | kcal/mol |
| TS1 shortest O-H...F contact | 2.390000 | 2.287419 | -0.102581 | 0.102581 | angstrom |

Frozen computational provenance:

- Job `hpc-job-3d2f37b9-bb2a-431c-97d3-459ae3a1f532`: `SUCCEEDED` at `2026-10-22T23:53:15.985422+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/new44_20261022/calculation/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T2343Z/job_audits/hpc-job-3d2f37b9-bb2a-431c-97d3-459ae3a1f532/native_audit.json`.
- Job `hpc-job-87b8bbd1-03d8-4789-bd6e-a73b09c14d63`: `SUCCEEDED` at `2026-10-22T23:54:53.969452+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T1743Z/formation_ts/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T2343Z/job_audits/hpc-job-87b8bbd1-03d8-4789-bd6e-a73b09c14d63/native_audit.json`.

Completed application logs:

- methoxy_major/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/new44_20261022/calculation/methoxy_major/optfreq.log`, SHA256 `4bd4c7fc5932ac75cb5f52babda474cf0323cfceb6fe22284a7ba08cddbed1b7`; return code `0`, normal termination `True`.
- methoxy_minor/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/new44_20261022/calculation/methoxy_minor/optfreq.log`, SHA256 `ed24c9b51a04628eb81134112f63300fbe0b17d3987f40290f4310257e18fa13`; return code `0`, normal termination `True`.
- methoxy_comparator/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/new44_20261022/calculation/methoxy_comparator/optfreq.log`, SHA256 `ee438c8dc8300d98f6af55d850691161f40cf102a925c756894a217ea7c34c01`; return code `0`, normal termination `True`.
- TS1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T1743Z/formation_ts/TS1/optfreq.log`, SHA256 `3f2751e54a50919e7d7c75233e434e0f25a5d4c9b9ba6c685281a109d6d2af71`; return code `0`, normal termination `True`.
- TS1prime/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T1743Z/formation_ts/TS1prime/optfreq.log`, SHA256 `3f2455f0165a310fb304d2abe1d2ffc2c222721213990aa93df1d1ec6786215e`; return code `0`, normal termination `True`.
- TS1doubleprime/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T1743Z/formation_ts/TS1doubleprime/optfreq.log`, SHA256 `a00c0444cde6838ffee86314a7891f7a7186c9939418e38cc18768d76839c4be`; return code `0`, normal termination `True`.

Source/method deviations remain in the frozen specs and `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T2343Z/author_comparison.json`. For optimized final geometries, graph checks, atom maps and hashes see `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T2343Z/completed_verified_stages.json`; TS modes/geometry in `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_cf8ce1fc0fbcd300/short_job_followup_20261022T2343Z/transition_state_analysis.json`. Whole-question coverage and pending work: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/new44_group_01/coverage.json`. No task text, scoring, tolerances, expert packages or global counts were modified.

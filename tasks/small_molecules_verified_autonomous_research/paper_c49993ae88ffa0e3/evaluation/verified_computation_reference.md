# Round-one scope notice — 2026-11-03

Explicit waters define finite hydration energy comparisons, not a required water-catalyzed path. Local ionic stabilization and net reaction thermodynamics are distinct conclusions. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## 2026-10-27 V3 final-result scope

This version scores independent final answers only. Current rules are in scoring_rules.json; per-conclusion evidence reuse and limits are in final_result_coverage.json. Historical native calculations below are retained unchanged and are not an automatic PASS for the new rubric. No new quantum calculation was run.

> 2026-10-17 V2 评分更新：现行规则为定量40分、定性中间结果30分、最终结论30分，用户已批准初步容差；可运行评分，专家出版审查仍待进行。下方原日期的数值待审状态属于历史，不覆盖现行 scoring_rules.json 与 reference_qualification.json。本次未新增量子化学计算。

> 2026-10-17 当前状态同步：已有2026-10-14的现行限定科学问题验收证据，本轮复核并同步记录，没有新增量化计算。[当前状态及限制](current_verification_status.json)区分科学覆盖与评分/发布资格。下方旧pending、失败和目录位置按原日期/范围保留，不覆盖后续现行验收；本次整理不自动放行正式评分或发布。

<!-- PARENT_PQ_ACCEPTANCE_20261014T020500Z -->
# PQ 当前任务范围的父级验收 — 2026-10-14

结论：**paper_c49993ae88ffa0e3 当前评估范围通过计算验证**。按用户“相差不大可以认为完成”的标准及任务已有逐量人工审阅规则验收；不是逐位相同，也不是整篇论文的完整光催化循环通过。12个实际结果已齐，最大绝对差 **0.166121 kcal/mol**。未更改作者值、评估规则或增加通用容差。`release_ready=false`。

父级重新读取66组低/高层、132份原始Gaussian输出与输入/状态哈希，核对正文、SI38–41页及作者XYZ。所有配对均有正常原生完成、3N−6正频率、正确电荷/态和源分子图，同一几何高层单点；S1使用TD总能量。62份双重态输出的S²消除前最大0.7706、后最大0.7503。19个最低点按Gaussian“力可忽略”结束，不能称为四个收敛列全部YES；实际末次优化表另存，未发现Optimization stopped。所有12项重新由已在HPC得到的热项组装，原子/水/电荷账本一致。没有新增或重复量子化学求解。

统一采用SI所写GoodVibes 3.0.2、298.15 K、1 M、100 cm⁻¹ Grimme处理、scale1、外部对称及全部SI构象标签。SI命令未写--dup，源码默认False；Gconf默认True。这个定义应用于全部12项，未因更接近论文而切换后处理。原始YAML未取得的事实保留，重建YAML不冒充原件。

|物理量|论文值|真实计算|计算−论文|人工判定|
|---|---:|---:|---:|---|
|首次干PT|-0.9|-0.922739|-0.022739|通过现有规则/逐量人工比较|
|首次干ET|-1.6|-1.433879|+0.166121|通过现有规则/逐量人工比较|
|首次双水PT|-2.2|-2.197755|+0.002245|通过现有规则/逐量人工比较|
|首次双水ET|-8.2|-8.220575|-0.020575|通过现有规则/逐量人工比较|
|第二次干PT，相对I|+2.3|+2.266745|-0.033255|通过现有规则/逐量人工比较|
|第二次干ET，相对I|+7.4|+7.328581|-0.071419|通过现有规则/逐量人工比较|
|第二次双水PT，相对I|-1.3|-1.344649|-0.044649|通过现有规则/逐量人工比较|
|第二次双水ET，相对I|-9.6|-9.583636|+0.016364|通过现有规则/逐量人工比较|
|干I，相对R|-43.9|-43.868608|+0.031392|通过现有规则/逐量人工比较|
|双水I，相对R|-41.7|-41.738197|-0.038197|通过现有规则/逐量人工比较|
|干F，相对R|-115.1|-115.102153|-0.002153|通过现有规则/逐量人工比较|
|双水F，相对R|-112.1|-112.238811|-0.138811|通过现有规则/逐量人工比较|

全部单位为kcal/mol。R是S1-H2PQ与基态PyO；I为两基态中性自由基；F为PQ与Py/生成水关联体。双水情景额外在两个片段各加一水。局部第二步从I起算，累计I/F从R起算。

两项旧“未决”经本次复核作如下处理：

1. **第二次双水PT**：全文/命令支持的全标签计算−1.344649，对−1.3差−0.044649；直接从作者绝对能表重建−1.336782，与本地仅差−0.007867。重建输入已经能明确实现该物理对照；缺原YAML属于原件追溯限制，不再等同于计算不完整。去重版本−0.950069继续保存为敏感性结果，未拿它替换作者方法。
2. **双水最终F**：坚持同一全标签版本得到−112.238811，差−0.138811；不采用更接近论文的去重值来抵消热项偏差。conf3低/高电子能与源仅差−6.54×10⁻⁷/+1.136×10⁻⁶ Eh，但qhG差−0.321883 kcal/mol，精确原因仍需作者频率才能拆分。该已量化的小差异不影响当前终点数值和结论的可比性：干湿累计差2.863343对3.0，I→F为−70.500614对−70.4。按当前规则对这些实际数值人工接受；不是把热项未决假装解决，也不建立新误差窗。

干第二ET的7.328581对7.4差0.071419另有源精度依据：SI绝对表重建7.329311；分别四舍五入后的累计−36.5−(−43.9)=7.4。其余新量逐项物种、参考和差值判断见验收JSON，不借用首次事件的数值窗口。

当前结论均被计算支持：首次干PT/ET皆轻微有利；第二次干PT较ET少上坡，双水则ET终点较低；最终脱氧关联体相对初始激发反应物强烈有利。本任务没有把端点自由能当活化势垒或唯一机理。原软件原件、低频热项残差及全部敏感性数据均保留。

证据：[全部原生读取](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/parent_pq_native_readback.json)、[末次优化判据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/parent_pq_convergence_review.json)、[逐目标人工验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/parent_pq_acceptance.json)。本次父审取代之前“整题尚未通过”的阶段判断，历史文件保留。

---

以下为保留的历史计算和阶段判断；当前验收以顶部父审为准。

# Latest verification continuation — 2026-10-13 19:53 UTC assignment

Updated 2026-10-13T20:42:41.852776+00:00. **66/66 native low/high pairs and 12/12 endpoint quantities are complete; current_scope_verified=false.** Four original components retain their existing pass status, six extended components are numerical verification candidates for independent acceptance, and two have explicit unresolved source/thermal comparability. This paragraph supersedes older waiting labels in the historical record below. Package validation is not scientific full-scope acceptance.

The actual c8a970c6 Hessian/CalcAll runner was personally checked: diagnostic/low/high each rc0 and one normal termination; low optimization completed with all four VeryTight criteria YES, 78 positive modes (minimum 30.4886 cm⁻¹), correct C14H11O3/+1/singlet source graph, and same-geometry def2-TZVPP single point. Low/high energies −765.352318318/−765.615384682 Eh. Source water contacts were retained; source-to-final all-atom RMSD 0.00321210 Å. Existing 65 pairs were reused with 390 log/input/status hashes checked. No new quantum-chemical jobs were submitted.

Only incremental thermochemistry was run in hpc-job-adb071f4-6957-4ba0-b464-c5f92ed469ab (CPU资源空间 / 人工智能驱动谱学研究 / CPU资源-2 / priority6 HIGH / 4 CPU, 16 GiB, one node). Both stages exited 0; platform SUCCEEDED and launcher/slurmctld/slurmd instances Deleted. Each implementation reused 65 scalar records unchanged and calculated only HPQ-conf5. Eleven earlier targets are unchanged. Original conditions and fixed source code were retained; no new acceptance window, zero shift or scoring change.

|Target|Fixed author kcal/mol|Canonical kcal/mol|Absolute difference|Upstream 3.0.2 full-label kcal/mol|Absolute difference|Disposition|
|---|---:|---:|---:|---:|---:|---|
|dry_PT|-0.9|-0.922738715|0.022738715|-0.922738715|0.022738715|PASS_EXISTING_COMPONENT|
|dry_ET|-1.6|-1.844558545|0.244558545|-1.433879342|0.166120658|PASS_EXISTING_COMPONENT|
|two_water_PT|-2.2|-2.197728103|0.002271897|-2.197755260|0.002244740|PASS_EXISTING_COMPONENT|
|two_water_ET|-8.2|-8.029374079|0.170625921|-8.220574861|0.020574861|PASS_EXISTING_COMPONENT|
|second_dry_PT|+2.3|+2.266745209|0.033254791|+2.266745209|0.033254791|VERIFIED_CANDIDATE|
|second_dry_ET|+7.4|+7.328581289|0.071418711|+7.328581289|0.071418711|VERIFIED_CANDIDATE|
|second_two_water_PT|-1.3|-0.950069123|0.349930877|-1.344649008|0.044649008|SOURCE_UNRESOLVED_AFTER_SEARCH|
|second_two_water_ET|-9.6|-9.583635401|0.016364599|-9.583635690|0.016364310|VERIFIED_CANDIDATE|
|first_complete_dry|-43.9|-43.868608009|0.031391991|-43.868608009|0.031391991|VERIFIED_CANDIDATE|
|first_complete_two_water|-41.7|-41.738196521|0.038196521|-41.738196521|0.038196521|VERIFIED_CANDIDATE|
|final_dry|-115.1|-115.102153417|0.002153417|-115.102153417|0.002153417|VERIFIED_CANDIDATE|
|final_two_water|-112.1|-112.117151978|0.017151978|-112.238810567|0.138810567|REPRODUCED_BUT_MISMATCH|

The dry second ET value +7.328581289 agrees with the independently reconstructed printed absolute table (+7.329310657) within 0.000729368 kcal/mol. S40's separately rounded cumulative values −36.5 and −43.9 produce the fixed +7.4. The retained absolute discrepancy 0.071418711 is explained by reporting precision; it does not justify a new Gaussian job. The fixed author value remains +7.4 and this is an explicit expert candidate, not a new generic rounding tolerance.

The newly complete second hydrated ET is −9.583635690 vs −9.6 (absolute difference 0.016364310); the original get_pes and partition result agree exactly. Canonical 0.05/0.1 Å dedup gives −9.583635401. The prior 0.2 Å sensitivity gives −9.183350674 because it also merges the PyOH-anion-H2O conformers; this sensitivity remains available, with no cutoff adjustment. Full-label conf5 population is 5.83048e−7, so its qhG residual −0.107103353 kcal/mol is negligible for that full ensemble. All five family labels are included; no conf2 substitution or four-member approximation was used.

Two limitations remain. Second hydrated PT depends on original conformer membership: −0.950069123 canonical vs −1.344649008 full-label, against −1.3. The source command omits --dup and upstream defaults to False, supporting the full-label diagnostic, but the original 0_PES.yaml was not recovered. Final hydrated F is −112.117151978 canonical vs −112.238810567 full-label against −112.1; the repaired PyOH2-H2O_conf3 qhG differs from the author table by −0.321883480 kcal/mol although its electronic energies agree closely. Canonical dedup partly cancels this thermal residual. Neither issue is certified away by value closeness. All endpoint orderings and strong final exergonicity remain, with no claim about barriers, rates or a complete catalytic cycle.

Physical references are unchanged: R=S1-H2PQ+PyO, I=two ground-state radicals, and F=PQ+associated PyOH2 (Py/generated water). Second-stage local quantities use I; cumulative I/F quantities use R. Zero/two added-water cases conserve C19H15NO3/C19H19NO5 and net charge zero. Source build/YAML and author original frequencies remain unlocated within the explicitly inherited detailed source search; no new remote negative search is claimed this continuation.

- Full comparison and review: [verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/verification_report.md)
- Native recovery readback: [native_recovery_review.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/native_recovery_review.json)
- Incremental acceptance: [incremental_acceptance_review.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/incremental_acceptance_review.json)
- Complete reuse inventory: [reuse_inventory.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/reuse_inventory.json)
- Target coverage: [coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/coverage.json)
- Remaining source issues: [verification_blockers.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/verification_blockers.json)
- Source search boundary: [source_search_log.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T195300Z/source_search_log.json)

## Preserved prior verification history

<!-- pq-continuation-20261013T094000Z-latest -->
# 最新验证状态：2026-10-13T14:03:15.168830+00:00

**当前12项范围未整体通过**。65/66源标签配对合格；11个量有数值。两次HPQconf5恢复d288/3c5f均原生lowrc1、无频率/高层；原始负软模结果则是rc0但不具最低点资格。Pyconf3合格低/高与官方3.0.2后处理两步exit0均直接复用。

新恢复 `hpc-job-c8a970c6-660e-4b9d-9af1-212f62edc767` 为指定项目/CPU资源-2/优先级6/20CPU100GiB；2026-10-13T14:04:15.690070+00:00 **QUEUEING，尚无原生输出**。依据Cartesian两点振荡提交checkpoint解析Hessian及逐步CalcAll，保持作者方法和VeryTight标准。保留全部66标签、旧失败和累计成本；不设“旧预算耗尽”永久停算。

官方3.0.2已核原源码、对称、标准态与gconf：干首ET-1.433879相对既有canonical-1.844559的差为PyO-anionrad单次对称RTln2。第二湿PTcanonical-0.950069／all-label-1.344649对作者-1.3；第二干ET+7.328581对+7.4；湿终点-112.117152／-112.238811对-112.1，Pyconf3热项差-0.321883仍未消除。未更改gold、零点、窗口。

新增CSIC数据/README、PMC及作者源码检索确认源XYZ/SI哈希相同，原0_PES.yaml和源频率输出未找到；这不阻止conf5结构恢复。[12点评分表](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/scoring_comparison.md) · [报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/verification_report.md) · [完整66标签库存](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/reuse_inventory.json) · [任务后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/successor.json) · [来源检索](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T094000Z/source_search_log.md)。

本轮交接后退出，不自动周期恢复。以下为先前验证记录原样保留，旧PASS不自动覆盖当前新增范围。
<!-- /pq-continuation-20261013T094000Z-latest -->

<!-- pq-continuation-20261013T073000Z-latest -->
# 2026-10-13 07:30续接：最新验证范围与状态

记录时间 2026-10-13T08:09:43.390270+00:00；**current_scope_verified=false；PARTIAL_VALID_DISTINCT_OPTIMIZER_RECOVERY_AND_SOURCE_REVIEW**。本次1篇全部评分点已逐项对照，当前65/66合格配对；旧PASS仅覆盖原4量。

最新收取HPQ-conf5第一次修复为rc1、0次正常终止、168步耗尽、无78频率/无高层，平台SUCCEEDED不等于应用成功。其前驱才是rc0但−11.8175cm⁻¹的最低点资格失败。末几何与来源conf5RMSD0.003213Å、图/态/水库存保留。依据新故障及父07:39明确授权，提交一次保持方法/UltraFine/介质/VeryTight的Cartesian+CalcFC续接，MaxCycles60、MaxStep5、每阶段3600秒；旧软模预算不重置。job `hpc-job-3c5f30b7-6903-4ca3-a6be-8475b2d2de96`，状态RUNNING／NATIVE_RUNNING_OR_QUEUED。

官方历史实现已找到版本字符串GoodVibes3.0.2（commit98c881d），原calc_bbe/PES/C对称算法HPC重放job `hpc-job-d785f822-a718-4a08-8dab-0bb6527453af`，状态QUEUEING／POSTPROCESSING_RUNNING_OR_QUEUED；不声称与作者可执行文件逐字节相同，0_PES.yaml仍缺。canonical与all-label诊断均保留。source3.0.2算法确认单次外部对称、内部因子1、默认gconf、可选dup，但具体作者成员仍需YAML支持。

关键未决：水合第二PT−0.950069 vs−1.3（all-label−1.344649）；干第二ET+7.328581 vs+7.4（源绝对表+7.329311）；水合F−112.117152虽近−112.1但Pyconf3热项/重复计数有反向抵消。缺失数值：second_two_water_ET。不改变零点、gold、科学范围或数值窗。

[完整12评分点表](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T073614Z/scoring_comparison.md) · [报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T073614Z/verification_report.md) · [coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T073614Z/coverage.json) · [jobs](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T073614Z/jobs.json) · [successor](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T073614Z/successor.json)。本轮报告完成即退出，无定时Codex恢复。以下整段为本轮前历史原样保留，不自动覆盖当前范围。
<!-- /pq-continuation-20261013T073000Z-latest -->

<!-- pq-continuation-20261013-latest -->
# 2026-10-13 续接验证最新范围与状态

时间：2026-10-13T04:02:31.534162+00:00。`author_deoxygenation_half_reaction_20261012`；**current_scope_verified=false；PARTIAL_VALID_RECOVERY_PENDING_AND_NUMERICAL_REVIEW**。下方旧PASS/“当前”均为历史，不覆盖扩展范围。本轮收取、分析、必要恢复提交与报告完成，无定时Codex重启。

8个原分子族HPC均平台SUCCEEDED；72个真实程序阶段均rc0，但仅35个新低/高对合格，另2个低层正常结束而含负频率：PyOH2-H2O_conf3 −1.4241 cm⁻¹（45模）、S0-HPQ-cation-H2O_conf5 −11.8175 cm⁻¹（78模）。不是程序崩溃。全部66条作者记录保留，旧29对有效证据复用。

两项各一次有限修复：按实际模态固定0.10Å扰动，原M062X/6-31+G(d,p)、SMD MeCN、态与网格/SCF保持，仅VeryTight和MaxStep5；合格才执行同几何def2TZVPP SP。新job `hpc-job-d700d2bb-e566-424b-887b-9d56695b43a8`、`hpc-job-d2886408-85d4-4e77-a765-35b771bf45ef`；最新平台{'SUCCEEDED': 1, 'RUNNING': 1}，原生{'VALID_MINIMUM': 1, 'VALID_SP': 1, 'RUNNING_NATIVE_INCOMPLETE': 1}。已消耗两项各一次恢复预算，后续不自动再试。

新增已算主口径值（kcal/mol）：second_dry_PT=+2.266745；second_dry_ET=+7.328581；second_two_water_PT=-0.950069；first_complete_dry=-43.868608；first_complete_two_water=-41.738197；final_dry=-115.102153；final_two_water=-112.117152。仍缺数值：second_two_water_ET。首次四量及其既有判据保持。

明确数值阻碍：水合第二PT主去重−0.950069 vs作者−1.3；全部源标签诊断−1.344649，说明近重复构象计数影响，未据结果调整主去重。干第二ET +7.328581与作者绝对表重组+7.329311接近，作者+7.4对应已舍入累计量相减的可能来源，仍保留原差异。修复后水合F=−112.117152，但PyOH2-conf3逐构象qhG与作者差−0.321883 kcal/mol，热项/去重的反向效应不能靠末值接近忽略。作者GoodVibes3.0.2/本轮4.3.0及未恢复0_PES.yaml明确披露，未新增窗口、调参、替换金标或删去非合格构象来宣布PASS。

报告与证据：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T033146Z/verification_report.md)、[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T033146Z/coverage.json)、[softmode_diagnosis.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T033146Z/softmode_diagnosis.json)、[numerical_comparability_review.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T033146Z/numerical_comparability_review.json)、[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T033146Z/jobs.json)、[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/attempt_20261013T033146Z/successor.json)。历史科学记录和本轮前原生日志原样保留。制备/再生/全循环/未定义聚集体或势垒仍不进入计算要求。
<!-- /pq-continuation-20261013-latest -->

<!-- pq-core7-verification-20261012-latest -->
# 2026-10-12 本轮作者路线补充验证：最新状态

核查时间：2026-10-12T20:11:31.318636+00:00。范围 `author_deoxygenation_half_reaction_20261012`；**current_scope_verified=false，PARTIAL_VERIFIED_COMPUTATION_PENDING**。本次当前提交及回读报告已完成，HPC继续运行，无定时重启。

本人重新核对29组旧低层优化/频率与配对高层单点的原生输入/输出、方法/态/原子库存、实频、几何和哈希；四个首次量仍为−0.922739、−1.844559、−2.197728、−8.029374 kcal/mol。旧有效结果复用，未重新运行。新版全题需十二量，不能继承旧首次范围的整体PASS。

新增37条作者构象分8个分子族作业，20CPU/100GiB、CPU资源空间/人工智能驱动谱学研究/CPU资源-2、priority6。最新平台状态：{'QUEUEING': 8}；新原生已结束阶段0，详细状态{}。新增第二阶段四量与累计I/F四量尚待完整原生、系综及逐数值审查；没有新增容差、移动作者值或以顺序代替数值。

当前作业：`hpc-job-410dd93d-4fc1-4c23-bf26-1c23f92e61bb`, `hpc-job-aaa3606a-3daf-48bf-b7a0-fac1d0278602`, `hpc-job-cf5c5985-d14b-41a5-82ea-3e1b87fa9afa`, `hpc-job-087a1ff0-ac83-4b10-96bf-cda0c9b37a65`, `hpc-job-e450df6c-ca0c-413b-8746-c1b4833224e5`, `hpc-job-2e9516a9-8363-449f-a57b-d5ed40956f57`, `hpc-job-3b830aa6-b6ca-4ef7-95ab-a66e1c42cae3`, `hpc-job-12c190ff-87cc-4b1e-85c5-8f8f9ef1921e`。

真实阻碍是计算完成和后处理审查；活动目标的作者路线/来源齐全。PyOH2是Py···H2O缔合物；外加水与生成水分账；第二步局部相对I、累计相对R。缺聚集体定义的轨道差/S22继续排除，不构建TS/IRC、制备、再生或全循环替代参考。

逐目标与执行证据：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/verification_report.md)、[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/coverage.json)、[reuse_inventory.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/reuse_inventory.json)、[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/jobs.json)、[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_c49993ae88ffa0e3/core7_upgrade_20261012T190159Z/successor.json)。

**下方所有旧版PASS/“当前”描述均作为历史保留，不自动覆盖此次扩展后的科学范围。**
<!-- /pq-core7-verification-20261012-latest -->

# 2026-10-12 已授权扩展后的现行资格

范围版本：`author_deoxygenation_half_reaction_20261012`。本次完成任务合同升级，没有提交或运行量化计算；**扩展范围尚未验证，release_ready=false**。以下历史 PASS/“当前”字样仅指当时首次事件范围，不是本版全题通过。历史原始记录全文保留。

复用 2026-10-11T06:17:42 UTC 独立重读的29组优化/频率及配对单点：干PT/ET −0.922739/−1.844559、双水PT/ET −2.197728/−8.029374 kcal/mol。适用目标是 dry_transfer/water_effect 及相应状态有效性；新 answer 不继承旧 answer 的 PASS。

新增 second_transfer_competition：作者局部值干态 +2.3/+7.4、水合 −1.3/−9.6；新增 deoxygenation_endpoints：累计 I/F 为干态 −43.9/−115.1、水合 −41.7/−112.1，单位均为 kcal/mol。来源为正文物理p.4 Fig.2A/C、SI pp.38–41 和作者66条XYZ。作者路线/结果存在；缺其余37条记录中必要构象的真实复验及系综核查，37不是必需新增作业数。

PyOH2 是 Py···H2O 缔合物，不能替换为自由分子之和；外加水与生成水分别记账。第二步局部参照为I，累计参照为R。聚集体轨道差/S22不具完整对象定义，不纳入活动评分；S22仅优化步数轨迹，不是势垒扫描或TS/IRC。不扩作者未算的制备、再生、全循环、速率或描述符。

逐目标计算差集及电荷/态/参照见 [validation_plan.json](validation_plan.json)，当前资格见 [qualification.json](qualification.json)。首次既有容差保留；新增量采用明确的人工数值可比性审查，通用窗口待校准，不能因复验失败移动作者数值或放宽标准。

既有真实证据索引（仓库相对路径，保持原生记录）：
- `docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/independent_state_audit.json`
- `docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/independent_thermochemistry_replay.json`
- `docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/native_readback.json`
- `docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/new_native_results.json`

---

# 历史验证档案（旧范围，非现行全题资格）

> 2026-10-10 用户纠正后的现行评分口径：本包采用 scientific_results.v1，以论文在当前任务范围内的中间关键点和最终结论作为目标；自主性指方法与探索过程选择，不指用相反或未定结论替代必评结果。原验证数据、数值容差、科学权重和有限模型范围保留。下方 open_research/替代结论得分说法仅为旧版本历史，不再生效。本包继续留在 verified_tasks；见[本次修正](../../../verified_tasks/PAPER_OUTCOME_ALIGNMENT_20261010.md)。

> 2026-10-10 任务整理状态：本包已补齐明确的最终参考结论并同步评分规则，已修复公开提交的证据保存路径，并通过科学规则正反例回放和 final 入口准备。以下历史记录中“结论登记、证据路径、评分回放待处理”的维护状态由本条更新；科学数值、原始计算流程和证据索引完整保留。验证范围仍以本文逐节点说明为准，不等于完整盲 AR 运行。本包继续留在 verified_tasks 等待用户确认迁移。详见[本次整理与验收](../../../verified_tasks/RELEASE_COMPLETION_20261010.md)。

# 已验证计算参考：paper_c49993ae88ffa0e3 / autonomous_research

> 当前状态更新时间：2026-10-09；HPC/已完成日志快照：2026-10-09T12:52:16.493331+00:00。本节取代此前旧资格判断。私有验证档案，不导出给被评agent。

**当前首事件热力学及双水影响已验证；四个对应量与论文保持小幅差异。**

科学参考状态：`reference_supported_for_first_event_thermodynamics`。AR/PR共享相同科学结果证据；这不是盲AR过程认证或正式发布批准。

## 已完成的验证计算与方法

29个低级别优化/频率与29个同几何高级别单点，匹配激发态/自由基身份；依SI的298.15K、1M、100cm⁻¹ qRRHO及已审去重/对称性定义组装四个首事件自由能。后处理重读原始频率和能量，不将第二次转移混入。

## 与论文对应量的比较

| 首事件 | 计算 / kcal mol⁻¹ | 论文 | 差值 |
| --- | --- | --- | --- |
| pt_dry | -0.922739 | -0.9 | -0.022739 |
| et_dry | -1.844559 | -1.6 | -0.244559 |
| pt_hydrated | -2.197728 | -2.2 | +0.002272 |
| et_hydrated | -8.029374 | -8.2 | +0.170626 |

**当前有据结论：**已研究模型中，无水PT/ET首事件均温和有利，双水对ET的稳定化明显更强；不以端点热力学排除全部PCET/HAT或证明动力学唯一性。

## 当前关键点与最终结论的证据覆盖

| 当前节点 | 类型 | 已完成证据与边界 |
| --- | --- | --- |
| states_references | process | 29候选的实际原子/电荷/自旋/态、双水计量与低高层几何一致。 |
| dry_transfer | result | 无水PT=-0.922739、ET=-1.844559 kcal/mol。 |
| water_effect | result | 水合第一PT=-2.197728、ET=-8.029374 kcal/mol；-1.3是第二步的不同量。 |
| first_event_answer | result | 四个量支持有限热力学解释及水效应，排他性/动力学更强主张未被认证。 |
| answer | final | 已研究模型中，无水PT/ET首事件均温和有利，双水对ET的稳定化明显更强；不以端点热力学排除全部PCET/HAT或证明动力学唯一性。 |

## 尚缺项与作业状态

当前有限参考科学目标没有已确认必须新增的量子计算；本次没有为本篇新提交验证作业。与全论文、所有替代方法或完整自主搜索不同，不作额外外推。

## 直接证据与本次同步

- [CURRENT_THERMOCHEMISTRY.json](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/resumption_20260925/thermochemistry/consistent_symmetry_v2/CURRENT_THERMOCHEMISTRY.json)
- [论文依据 main](../../../../papers/paper_c49993ae88ffa0e3/documents/main.pdf)：Figure 2A–C, first and second step distinction; mechanistic interpretation
- [论文依据 si](../../../../papers/paper_c49993ae88ffa0e3/documents/supplementary_001.pdf)：S38 computational details; S39 GoodVibes protocol; S40 first-event free energies and subsequent coordinate records
- [原生日志复核](../../../verified_tasks/maintenance_tools/post_upgrade_review_20261008/native_recheck.json)；[独立量值重提取](../../../verified_tasks/maintenance_tools/post_upgrade_review_20261008/recomputed_quantities.json)
- [保留的包维护记录](task_provenance/maintenance_audit.md)；[七篇状态及本次同步总结](../../../verified_tasks/VERIFICATION_REFERENCE_UPDATE_20261009.md)

本次更新只同步已完成事实、状态及维护引用。既定科学目标、权重和数值容差保持；此前最终结论登记、证据目录索引、正式评分回放和部署读取隔离问题仍需按待确认方案处理。

---

## 历史计算档案与原始输入输出索引

> 以下记录按当时版本保留，旧节点名/题面范围/“当前”状态以本页上方最新解释为准。原始数值和输入输出引用保留。

# 已验证计算参考：paper_c49993ae88ffa0e3 / autonomous_research

> 2026-09-29 修后同步：任务修复和当前评分映射见第 3、6 节；全部仍在 verified_tasks，未获迁移确认。
核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/autonomous_research/paper_c49993ae88ffa0e3`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 2。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16，M06-2X/6-31+G(d,p) Opt/Freq → 同几何 def2-TZVPP 单点，SMD acetonitrile。H₂PQ/HPQ 阴离子采用明示的最低单重激发态 TD 总能；H₂PQ 阳离子自由基与 PyO 阴离子自由基采用 S0 双重态；其他组分为相应基态单重态。29 个低/高层配对。SI 物理第 38 页：298.15 K、1 M、100 cm⁻¹ Grimme 熵插值、构象系综及对称性。GoodVibes 4.3 独立重读全部 29 个低层日志，避免对称数重复相除。

论文来源：[正文](../../../../papers/paper_c49993ae88ffa0e3/documents/main.pdf)；[SI](../../../../papers/paper_c49993ae88ffa0e3/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

两模式公开分子图/状态/水数定义齐全；AR 只给起始/event 边界，PR 给 PT/ET 路线。没有把私有 29 个优化构象或参考能量公开。条件与两水计量可复算。两模式原重复指令已在本轮清理，PR 作者指导已单列。

## 2. 有效计算链、结果与推导

G_i=E_high,i+(G_qRRHO,low,i−E_low,i)，每个外部旋转对称数只除一次；构象去重后 G_ensemble=Gmin−RT lnΣexp[−(Gi−Gmin)/RT]。采用 .001_dedup0.1（对称性位移诊断 0.001 Å、去重 RMSD 0.1 Å），完整代表构象见系综表。反应差由指定产物系综之和减反应物；水合双方总水数均为 2。四个 ΔG(kcal/mol)：pt_dry −0.922738715、et_dry −1.844558545、pt_hydrated −2.197728103、et_hydrated −8.029374079。水对 PT/ET 的位移分别约 −1.274989/−6.184816。干态轻度有利，水更强稳定 ET 端点。第一步水合 PT 在正文 Figure 2B 和 SI S40 均为 −2.2；Figure 2C 的 −1.3 属于第二步，不能混入第一步。现有 −2.197728 与该第一步值一致。当前来源 JSON 的旧 evaluation_match=false 不能替代后续逐项审计，反之最新 PASS 也不能证明独立搜索。无速率/第二次转移/PCET-HAT 排除结论。

| 代表候选 | family | q / multiplicity / S1 | 低层电子能 / Eh | 高层电子能 / Eh | 修正后 G / Eh |
| --- | --- | --- | --- | --- | --- |
| PyO-anionrad-H2O_conf1 | PyO-anionrad-H2O | -1 / 2 / False | -399.8250798590 | -399.9681419570 | -399.8872483638 |
| PyO-anionrad-H2O_conf2 | PyO-anionrad-H2O | -1 / 2 / False | -399.8255668360 | -399.9688132760 | -399.8868284002 |
| PyO-anionrad-H2O_conf3 | PyO-anionrad-H2O | -1 / 2 / False | -399.8255638500 | -399.9688070990 | -399.8868045688 |
| PyO-anionrad | PyO-anionrad | -1 / 2 / False | -323.4030396710 | -323.5132297370 | -323.4532783123 |
| PyO-H2O_conf1 | PyO-H2O | 0 / 1 / False | -399.7545881430 | -399.8988495160 | -399.8113659736 |
| PyO | PyO | 0 / 1 / False | -323.3398836620 | -323.4512469250 | -323.3824873393 |
| PyOH-cation-H2O_conf1 | PyOH-cation-H2O | 1 / 1 / False | -400.1918522330 | -400.3371768370 | -400.2393751596 |
| PyOH-cation-H2O_conf2 | PyOH-cation-H2O | 1 / 1 / False | -400.1918659460 | -400.3371597620 | -400.2396007630 |
| PyOH-cation-H2O_conf3 | PyOH-cation-H2O | 1 / 1 / False | -400.2031959140 | -400.3488068110 | -400.2488078811 |
| PyOH-cation | PyOH-cation | 1 / 1 / False | -323.7827626490 | -323.8964657790 | -323.8163984847 |
| S0-H2PQ-cationrad-H2O_conf1 | S0-H2PQ-cationrad-H2O | 1 / 2 / False | -765.9652533200 | -766.2298072100 | -766.0412629961 |
| S0-H2PQ-cationrad-H2O_conf2 | S0-H2PQ-cationrad-H2O | 1 / 2 / False | -765.9659673930 | -766.2296416420 | -766.0420816522 |
| S0-H2PQ-cationrad-H2O_conf3 | S0-H2PQ-cationrad-H2O | 1 / 2 / False | -765.9647681680 | -766.2286406780 | -766.0396174234 |
| S0-H2PQ-cationrad-H2O_conf4 | S0-H2PQ-cationrad-H2O | 1 / 2 / False | -765.9785097660 | -766.2417093320 | -766.0507524659 |
| S0-H2PQ-cationrad-H2O_conf5 | S0-H2PQ-cationrad-H2O | 1 / 2 / False | -765.9785085610 | -766.2417054500 | -766.0512479443 |
| S0-H2PQ-cationrad-H2O_conf6 | S0-H2PQ-cationrad-H2O | 1 / 2 / False | -765.9790494020 | -766.2420258290 | -766.0520893376 |
| S0-H2PQ-cationrad | S0-H2PQ-cationrad | 1 / 2 / False | -689.5582221830 | -689.7901190740 | -689.6201791671 |
| S1-H2PQ-H2O_conf1 | S1-H2PQ-H2O | 0 / 1 / True | -766.0386300690 | -766.3008702650 | -766.1153600112 |
| S1-H2PQ-H2O_conf2 | S1-H2PQ-H2O | 0 / 1 / True | -766.0393198710 | -766.3014593140 | -766.1155420455 |
| S1-H2PQ-H2O_conf3 | S1-H2PQ-H2O | 0 / 1 / True | -766.0291469160 | -766.2922071650 | -766.1079445585 |
| S1-H2PQ-H2O_conf4 | S1-H2PQ-H2O | 0 / 1 / True | -766.0309968430 | -766.2942703450 | -766.1111890855 |
| S1-H2PQ-H2O_conf6 | S1-H2PQ-H2O | 0 / 1 / True | -766.0285985890 | -766.2912451730 | -766.1090721831 |
| S1-H2PQ-H2O_conf7 | S1-H2PQ-H2O | 0 / 1 / True | -766.0313493300 | -766.2948209730 | -766.1105271895 |
| S1-H2PQ | S1-H2PQ | 0 / 1 / True | -689.6219221030 | -689.8526088330 | -689.6880306489 |
| S1-HPQ-anion-H2O_conf1 | S1-HPQ-anion-H2O | -1 / 1 / True | -765.5939675310 | -765.8545939860 | -765.6803374617 |
| S1-HPQ-anion-H2O_conf2 | S1-HPQ-anion-H2O | -1 / 1 / True | -765.5939436050 | -765.8547405210 | -765.6806238642 |
| S1-HPQ-anion-H2O_conf4 | S1-HPQ-anion-H2O | -1 / 1 / True | -765.5957417590 | -765.8565169220 | -765.6817901730 |
| S1-HPQ-anion-H2O_conf5 | S1-HPQ-anion-H2O | -1 / 1 / True | -765.5869413120 | -765.8474034150 | -765.6764353936 |
| S1-HPQ-anion | S1-HPQ-anion | -1 / 1 / True | -689.1808656950 | -689.4092021350 | -689.2555899814 |

| 系综 | 实际代表构象 | Gensemble / Eh |
| --- | --- | --- |
| PyO-anionrad-H2O | PyO-anionrad-H2O_conf1, PyO-anionrad-H2O_conf2 | -399.8877160004 |
| PyO-anionrad | PyO-anionrad | -323.4532783123 |
| PyO-H2O | PyO-H2O_conf1 | -399.8113659736 |
| PyO | PyO | -323.3824873393 |
| PyOH-cation-H2O | PyOH-cation-H2O_conf3, PyOH-cation-H2O_conf2 | -400.2488079361 |
| PyOH-cation | PyOH-cation | -323.8163984847 |
| S0-H2PQ-cationrad-H2O | S0-H2PQ-cationrad-H2O_conf6, S0-H2PQ-cationrad-H2O_conf5, S0-H2PQ-cationrad-H2O_conf4, S0-H2PQ-cationrad-H2O_conf2, S0-H2PQ-cationrad-H2O_conf1, S0-H2PQ-cationrad-H2O_conf3 | -766.0525638401 |
| S0-H2PQ-cationrad | S0-H2PQ-cationrad | -689.6201791671 |
| S1-H2PQ-H2O | S1-H2PQ-H2O_conf2, S1-H2PQ-H2O_conf1, S1-H2PQ-H2O_conf4, S1-H2PQ-H2O_conf7, S1-H2PQ-H2O_conf6, S1-H2PQ-H2O_conf3 | -766.1161182449 |
| S1-H2PQ | S1-H2PQ | -689.6880306489 |
| S1-HPQ-anion-H2O | S1-HPQ-anion-H2O_conf4, S1-HPQ-anion-H2O_conf2, S1-HPQ-anion-H2O_conf1, S1-HPQ-anion-H2O_conf5 | -765.6821785851 |
| S1-HPQ-anion | S1-HPQ-anion | -689.2555899814 |

| 反应 | reactants | products | ΔG / kcal mol⁻¹ |
| --- | --- | --- | --- |
| pt_dry | S1-H2PQ + PyO | S1-HPQ-anion + PyOH-cation | -0.922738715 |
| et_dry | S1-H2PQ + PyO | S0-H2PQ-cationrad + PyO-anionrad | -1.844558545 |
| pt_hydrated | S1-H2PQ-H2O + PyO-H2O | S1-HPQ-anion-H2O + PyOH-cation-H2O | -2.197728103 |
| et_hydrated | S1-H2PQ-H2O + PyO-H2O | S0-H2PQ-cationrad-H2O + PyO-anionrad-H2O | -8.029374079 |

## 3. 修后当前必评关键点与结论覆盖（2026-09-29）

本表对齐本包当前五个 evaluator JSON。历史真实计算链及数值仍见第 2、4、5 节；reference 不新增评分门槛。

| 当前 ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| kp_ar_process_inventory / process | The report independently inventories chemically explicit first-event hypotheses and records advancement, merging or rejection reasons. | 源 PT/ET 四类别有明示候选及29构象；不认证独立提出/排除 PCET/HAT。 | r_ar_inventory |
| kp_ar_process_validation / process | Advanced candidates retain state identity, atom balance, charge, spin and conformer/water-placement validation with a stopping rationale. | 29最低点全实频、29相同父几何SP、状态/水数/对称性/去重档。 已有对称数/去重参数变体支持所记录的敏感性，不认证新自主穷尽。 | r_ar_validation, r_ar_limits |
| kp_ar_dry / result | For the source-supported stepwise PT and ET classes, dry first-event values are approximately -0.9 and -1.6 kcal/mol, respectively. | pt/et dry −0.922739/−1.844559，分别对 −0.9/−1.6±1.0。 | r_ar_dry |
| kp_ar_water / result | Explicit water substantially stabilizes the source-supported electron-transfer first-event class, with a published value near -8.2 kcal/mol. | et hydrated −8.029374，水位移 −6.184816，源约−8.2。 | r_ar_water |

| 结论 ID / 角色 | 当前科学主张 | 支持关键点及边界 |
| --- | --- | --- |
| c_ar_final / final | The selected explanation is supported only to the extent that independently validated candidate free energies and coverage discriminate it; source-supported stepwise models show mild dry accessibility and stronger hydrated ET stabilization. | kp_ar_process_inventory, kp_ar_process_validation, kp_ar_dry, kp_ar_water。第一步水合 PT 的正文 Figure 2B 与 SI S40 一致；第二步 −1.3 单独保留，未新增固定 gold。29 构象与对称/去重敏感性支持有限来源系综；不宣称排除 PCET/HAT、得到速率或认证独立搜索收敛。 |

修前→修后：关键点 5→4；结论记录 2→1。现有结论为科学成果，不另给普通免责声明计分。真实计算支持范围不因本次改关联而扩大。

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PyO-anionrad-H2O_conf1_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf1_publisher_correct_object_optfreq_20260923_20260923T132116Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf1_publisher_correct_object_optfreq_20260923_20260923T132116Z/stdout.log) | [-1, 2] | -399.8250798590 | -399.7489590000 | 39 / 0 / 21.7377 | native normal |
| 2 | PyO-anionrad-H2O_conf1_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf1_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030016Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf1_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030016Z/stdout.log) | [-1, 2] | -399.9681419570 | — | — | native normal |
| 3 | PyO-anionrad-H2O_conf2_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf2_publisher_correct_object_optfreq_20260923_20260923T132131Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf2_publisher_correct_object_optfreq_20260923_20260923T132131Z/stdout.log) | [-1, 2] | -399.8255668360 | -399.7480270000 | 39 / 0 / 37.3118 | native normal |
| 4 | PyO-anionrad-H2O_conf2_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf2_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T031210Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf2_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T031210Z/stdout.log) | [-1, 2] | -399.9688132760 | — | — | native normal |
| 5 | PyO-anionrad-H2O_conf3_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf3_publisher_correct_object_optfreq_20260923_20260923T133332Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf3_publisher_correct_object_optfreq_20260923_20260923T133332Z/stdout.log) | [-1, 2] | -399.8255638500 | -399.7479890000 | 39 / 0 / 37.5541 | native normal |
| 6 | PyO-anionrad-H2O_conf3_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf3_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030038Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_H2O_conf3_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030038Z/stdout.log) | [-1, 2] | -399.9688070990 | — | — | native normal |
| 7 | PyO-anionrad_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/native_workspace_batch/outputs/execution_jobs/job_c25b7622994b4526abaca3154d0ce4d4/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/native_workspace_batch/outputs/execution_jobs/job_c25b7622994b4526abaca3154d0ce4d4/stdout.log) | [-1, 2] | -323.4030396710 | -323.3469940000 | 30 / 0 / 32.7894 | native normal |
| 8 | PyO-anionrad_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_validated_source_matched_def2TZVPP_SP_20260923_20260923T133347Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_anionrad_validated_source_matched_def2TZVPP_SP_20260923_20260923T133347Z/stdout.log) | [-1, 2] | -323.5132297370 | — | — | native normal |
| 9 | PyO-H2O_conf1_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/native_workspace_batch/outputs/execution_jobs/job_0feacd80e5334b3d8b0bad72e737d201/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/native_workspace_batch/outputs/execution_jobs/job_0feacd80e5334b3d8b0bad72e737d201/stdout.log) | [0, 1] | -399.7545881430 | -399.6719600000 | 39 / 0 / 22.0368 | native normal |
| 10 | PyO-H2O_conf1_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_H2O_conf1_validated_source_matched_def2TZVPP_SP_20260923_20260923T133402Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_H2O_conf1_validated_source_matched_def2TZVPP_SP_20260923_20260923T133402Z/stdout.log) | [0, 1] | -399.8988495160 | — | — | native normal |
| 11 | PyO_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_publisher_correct_object_optfreq_20260923_20260923T133417Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_publisher_correct_object_optfreq_20260923_20260923T133417Z/stdout.log) | [0, 1] | -323.3398836620 | -323.2741380000 | 30 / 0 / 221.7044 | native normal |
| 12 | PyO_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030054Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyO_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030054Z/stdout.log) | [0, 1] | -323.4512469250 | — | — | native normal |
| 13 | PyOH-cation-H2O_conf1_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf1_publisher_correct_object_optfreq_20260923_20260923T133432Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf1_publisher_correct_object_optfreq_20260923_20260923T133432Z/stdout.log) | [1, 1] | -400.1918522330 | -400.0986640000 | 42 / 0 / 34.8031 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 14 | PyOH-cation-H2O_conf1_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf1_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T031226Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf1_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T031226Z/stdout.log) | [1, 1] | -400.3371768370 | — | — | native normal |
| 15 | PyOH-cation-H2O_conf2_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf2_publisher_correct_object_optfreq_20260923_20260923T133447Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf2_publisher_correct_object_optfreq_20260923_20260923T133447Z/stdout.log) | [1, 1] | -400.1918659460 | -400.0988610000 | 42 / 0 / 25.1728 | native normal |
| 16 | PyOH-cation-H2O_conf2_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf2_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T031241Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf2_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T031241Z/stdout.log) | [1, 1] | -400.3371597620 | — | — | native normal |
| 17 | PyOH-cation-H2O_conf3_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf3_publisher_correct_object_optfreq_20260923_20260923T133502Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf3_publisher_correct_object_optfreq_20260923_20260923T133502Z/stdout.log) | [1, 1] | -400.2031959140 | -400.1077230000 | 42 / 0 / 24.8922 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 18 | PyOH-cation-H2O_conf3_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf3_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030126Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_H2O_conf3_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030126Z/stdout.log) | [1, 1] | -400.3488068110 | — | — | native normal |
| 19 | PyOH-cation_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_publisher_correct_object_optfreq_20260923_20260923T133517Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_publisher_correct_object_optfreq_20260923_20260923T133517Z/stdout.log) | [1, 1] | -323.7827626490 | -323.7057060000 | 33 / 0 / 224.1865 | native normal |
| 20 | PyOH-cation_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030142Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_PyOH_cation_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T030142Z/stdout.log) | [1, 1] | -323.8964657790 | — | — | native normal |
| 21 | S0-H2PQ-cationrad-H2O_conf1_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf1_publisher_correct_object_optfreq_20260923_20260923T133532Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf1_publisher_correct_object_optfreq_20260923_20260923T133532Z/stdout.log) | [1, 2] | -765.9652533200 | -765.7817430000 | 81 / 0 / 43.5022 | native normal |
| 22 | S0-H2PQ-cationrad-H2O_conf1_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf1_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032331Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf1_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032331Z/stdout.log) | [1, 2] | -766.2298072100 | — | — | native normal |
| 23 | S0-H2PQ-cationrad-H2O_conf2_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf2_publisher_correct_object_optfreq_20260923_20260923T133548Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf2_publisher_correct_object_optfreq_20260923_20260923T133548Z/stdout.log) | [1, 2] | -765.9659673930 | -765.7837260000 | 81 / 0 / 33.2854 | native normal |
| 24 | S0-H2PQ-cationrad-H2O_conf2_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf2_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032348Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf2_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032348Z/stdout.log) | [1, 2] | -766.2296416420 | — | — | native normal |
| 25 | S0-H2PQ-cationrad-H2O_conf3_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf3_publisher_correct_object_optfreq_20260923_20260923T133603Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf3_publisher_correct_object_optfreq_20260923_20260923T133603Z/stdout.log) | [1, 2] | -765.9647681680 | -765.7806600000 | 81 / 0 / 34.6425 | native normal |
| 26 | S0-H2PQ-cationrad-H2O_conf3_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf3_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032403Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf3_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032403Z/stdout.log) | [1, 2] | -766.2286406780 | — | — | native normal |
| 27 | S0-H2PQ-cationrad-H2O_conf4_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf4_publisher_correct_object_optfreq_20260923_20260923T134642Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf4_publisher_correct_object_optfreq_20260923_20260923T134642Z/stdout.log) | [1, 2] | -765.9785097660 | -765.7918930000 | 81 / 0 / 44.8266 | native normal |
| 28 | S0-H2PQ-cationrad-H2O_conf4_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf4_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032418Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf4_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032418Z/stdout.log) | [1, 2] | -766.2417093320 | — | — | native normal |
| 29 | S0-H2PQ-cationrad-H2O_conf5_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf5_publisher_correct_object_optfreq_20260923_20260923T134657Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf5_publisher_correct_object_optfreq_20260923_20260923T134657Z/stdout.log) | [1, 2] | -765.9785085610 | -765.7926660000 | 81 / 0 / 31.6701 | native normal |
| 30 | S0-H2PQ-cationrad-H2O_conf5_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf5_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032433Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf5_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T032433Z/stdout.log) | [1, 2] | -766.2417054500 | — | — | native normal |
| 31 | S0-H2PQ-cationrad-H2O_conf6_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf6_publisher_correct_object_optfreq_20260923_20260923T134713Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf6_publisher_correct_object_optfreq_20260923_20260923T134713Z/stdout.log) | [1, 2] | -765.9790494020 | -765.7945710000 | 81 / 0 / 4.1463 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 32 | S0-H2PQ-cationrad-H2O_conf6_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf6_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T034512Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_H2O_conf6_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T034512Z/stdout.log) | [1, 2] | -766.2420258290 | — | — | native normal |
| 33 | S0-H2PQ-cationrad_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_publisher_correct_object_optfreq_20260923_20260923T134728Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_publisher_correct_object_optfreq_20260923_20260923T134728Z/stdout.log) | [1, 2] | -689.5582221830 | -689.3918530000 | 72 / 0 / 75.488 | native normal |
| 34 | S0-H2PQ-cationrad_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T034527Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S0_H2PQ_cationrad_publisher_correct_object_validated_minimum_def2TZVPP_SP_20260925_20260925T034527Z/stdout.log) | [1, 2] | -689.7901190740 | — | — | native normal |
| 35 | S1-H2PQ-H2O_conf1_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf1_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T035556Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf1_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T035556Z/stdout.log) | [0, 1] | -766.0386300690 | -765.8579120000 | 81 / 0 / 36.5423 | native normal |
| 36 | S1-H2PQ-H2O_conf1_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf1_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T114318Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf1_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T114318Z/stdout.log) | [0, 1] | -766.3008702650 | — | — | native normal |
| 37 | S1-H2PQ-H2O_conf2_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf2_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T035612Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf2_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T035612Z/stdout.log) | [0, 1] | -766.0393198710 | -765.8583360000 | 81 / 0 / 17.3582 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 38 | S1-H2PQ-H2O_conf2_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf2_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T131826Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf2_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T131826Z/stdout.log) | [0, 1] | -766.3014593140 | — | — | native normal |
| 39 | S1-H2PQ-H2O_conf3_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf3_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T040640Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf3_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T040640Z/stdout.log) | [0, 1] | -766.0291469160 | -765.8505370000 | 81 / 0 / 19.9621 | native normal |
| 40 | S1-H2PQ-H2O_conf3_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf3_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T132904Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf3_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T132904Z/stdout.log) | [0, 1] | -766.2922071650 | — | — | native normal |
| 41 | S1-H2PQ-H2O_conf4_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf4_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T041708Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf4_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T041708Z/stdout.log) | [0, 1] | -766.0309968430 | -765.8538740000 | 81 / 0 / 11.4435 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 42 | S1-H2PQ-H2O_conf4_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf4_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T133945Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf4_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T133945Z/stdout.log) | [0, 1] | -766.2942703450 | — | — | native normal |
| 43 | S1-H2PQ-H2O_conf6_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf6_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T041723Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf6_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T041723Z/stdout.log) | [0, 1] | -766.0285985890 | -765.8526960000 | 81 / 0 / 20.727 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 44 | S1-H2PQ-H2O_conf6_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf6_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T135035Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf6_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T135035Z/stdout.log) | [0, 1] | -766.2912451730 | — | — | native normal |
| 45 | S1-H2PQ-H2O_conf7_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf7_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T042750Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf7_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T042750Z/stdout.log) | [0, 1] | -766.0313493300 | -765.8523310000 | 81 / 0 / 29.5149 | native normal |
| 46 | S1-H2PQ-H2O_conf7_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf7_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T140117Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_H2O_conf7_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T140117Z/stdout.log) | [0, 1] | -766.2948209730 | — | — | native normal |
| 47 | S1-H2PQ_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T042805Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T042805Z/stdout.log) | [0, 1] | -689.6219221030 | -689.4617390000 | 72 / 0 / 41.7045 | native normal |
| 48 | S1-H2PQ_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T144239Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_H2PQ_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T144239Z/stdout.log) | [0, 1] | -689.8526088330 | — | — | native normal |
| 49 | S1-HPQ-anion-H2O_conf1_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf1_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T042820Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf1_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T042820Z/stdout.log) | [-1, 1] | -765.5939675310 | -765.4250300000 | 78 / 0 / 22.4756 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 50 | S1-HPQ-anion-H2O_conf1_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf1_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T144255Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf1_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T144255Z/stdout.log) | [-1, 1] | -765.8545939860 | — | — | native normal |
| 51 | S1-HPQ-anion-H2O_conf2_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf2_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T043847Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf2_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T043847Z/stdout.log) | [-1, 1] | -765.5939436050 | -765.4253840000 | 78 / 0 / 26.6026 | native normal |
| 52 | S1-HPQ-anion-H2O_conf2_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf2_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T145348Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf2_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T145348Z/stdout.log) | [-1, 1] | -765.8547405210 | — | — | native normal |
| 53 | S1-HPQ-anion-H2O_conf4_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf4_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T044914Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf4_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T044914Z/stdout.log) | [-1, 1] | -765.5957417590 | -765.4256290000 | 78 / 0 / 37.7381 | native normal |
| 54 | S1-HPQ-anion-H2O_conf4_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf4_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T145403Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf4_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T145403Z/stdout.log) | [-1, 1] | -765.8565169220 | — | — | native normal |
| 55 | S1-HPQ-anion-H2O_conf5_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf5_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T044930Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf5_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T044930Z/stdout.log) | [-1, 1] | -765.5869413120 | -765.4219930000 | 78 / 0 / 22.3497 | native normal |
| 56 | S1-HPQ-anion-H2O_conf5_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf5_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T150445Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_H2O_conf5_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T150445Z/stdout.log) | [-1, 1] | -765.8474034150 | — | — | native normal |
| 57 | S1-HPQ-anion_low | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T044945Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_publisher_correct_object_optfreq_three_root_precheck_20260925_20260925T044945Z/stdout.log) | [-1, 1] | -689.1808656950 | -689.0309130000 | 69 / 0 / 75.0409 | native normal |
| 58 | S1-HPQ-anion_high | [输入](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T155238Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/qzcli_hpc/author_S1_HPQ_anion_publisher_correct_object_validated_S1_def2TZVPP_SP_20260925_20260925T155238Z/stdout.log) | [-1, 1] | -689.4092021350 | — | — | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 3, 5, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33 | `#p M062X/6-31+G(d,p) Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile)` |
| 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34 | `#p M062X/def2TZVPP SP NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile)` |
| 7, 9 | `#p M062X/6-31+G(d,p) SCRF=(SMD,Solvent=Acetonitrile) Opt=(CalcFC,MaxCycles=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57 | `#p M062X/6-31+G(d,p) TD=(Singlets,NStates=1,Root=1) Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile)` |
| 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58 | `#p M062X/def2TZVPP TD=(Singlets,NStates=1,Root=1) SP NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile)` |

## 5. 模型、连接与后处理原始出处

- [provenance/resumption_20260925/thermochemistry/consistent_symmetry_v2/CURRENT_THERMOCHEMISTRY.json](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/resumption_20260925/thermochemistry/consistent_symmetry_v2/CURRENT_THERMOCHEMISTRY.json)
- [provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../docs/verification/group_2/paper_c49993ae88ffa0e3/report/results.json)
- [原系综/对称性实现（只读）](../../../../docs/verification/group_2/consume_c499_thermochemistry_20260925.py)

## 6. 修后包检查与未认证事项（2026-09-29）

当前策略为 `dual_axis_100.scientific_results.v1`；真实历史 report 对本包的实际输出检查：**通过（仅将 states 字典无损映射为带 state_id 的数组）**。本包已执行 13 个提交样例，每个分别经过 JSON Schema 和真实 validate_output_contract；合成正反例只测试格式，未加入本计算档案的科学证据。

第一步水合 PT 的正文 Figure 2B 与 SI S40 一致；第二步 −1.3 单独保留，未新增固定 gold。29 构象与对称/去重敏感性支持有限来源系综；不宣称排除 PCET/HAT、得到速率或认证独立搜索收敛。

[逐包维护记录](task_provenance/maintenance_audit.md)及[集中报告第30节](../../../verified_tasks/MAINTENANCE_REPORT.md)记录实际修改、检查与未闭合项。普通免责声明已取消必填及独立计分，身份/态/收敛/频率/路径/参考态和真实失败证据保留。

本次没有新电子结构计算、HPC 操作、完整 LLM 评分或 AR 盲测；没有迁移 final/hold。文件导出检查只覆盖 agent_input 物化，不能替代部署侧父目录、容器挂载和网络隔离。完整原始证据直接链接在第 4、5 节，不依赖 task_provenance 的长期存在。


<!-- phase2-verification-group05-20261010T231612Z -->

## 2026-10-11 第二阶段第5组独立参考计算验证

检查时间：2026-10-11T06:17:42.688533+00:00。当前运行状态：**PASS**；已完成证据的科学判定：**PASS**。

当前首事件热力学的全部必需科学结果已恢复；水合PT评分的通用接受边界缺失单列为发布规则问题。

被验证科学任务的初始包SHA256：`86279bfd3189a01a9b3b16cc783d81fdb1a925319100fa46ae6bf7256efd5500`。本轮只追加证据并重建manifest；任务/evaluator/阈值保持不变。更新后的包hash由本组manifest_changes.json记录，避免把含自身hash的文档递归纳入hash。

完整逐目标报告：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/verification_report.md)；覆盖表：[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/coverage.json)；作业和续接：[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/jobs.json)、[resumption.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/resumption.json)。

| 当前必需目标 | 状态 | 真实证据及缺口 |
|---|---|---|
| states_references | PASS | 重新读取58个低/高层原生输出，29个最低点均实频；逐一核对H+/电子位置、电荷、多重度、S1的TD总能和各侧两水计量。重新枚举保向几何对称数并仅施加一次，0.1 Å complete-link去重后计算配分和。 |
| dry_transfer | PASS | 干态PT和ET均温和放能；物种、电荷、298.15 K/1 M/MeCN参照一致。 |
| water_effect | PASS | 两水PT为−2.197728，与Figure2B的−2.2舍入一致；两水ET为−8.029374。水引起ET比PT更强稳定。Figure2C的−1.3是第二次PT，未混入。 |
| first_event_answer | PASS | 计算恢复干态两个首事件端点轻微放能、两水对ET的稳定更大的结论；不据此判定唯一机理或动力学优势。 |
| answer | PASS | 四个必需首事件差值均恢复，科学验证通过；不扩展为HAT/PCET全部排除、第二步机理或完整光催化循环。 |

| 比较量 | 计算值 | 论文值 | 差值 | 单位 | 既有容差 |
|---|---|---|---|---|---|
| pt_dry | -0.9227387150233828 | -0.9 | -0.02273871502338276 | kcal/mol | 1.0 |
| et_dry | -1.8445585452387985 | -1.6 | -0.24455854523879839 | kcal/mol | 1.0 |
| pt_hydrated | -2.1977281169307545 | -2.2 | 0.0022718830692456393 | kcal/mol | None |
| et_hydrated | -8.029374164863087 | -8.2 | 0.17062583513691187 | kcal/mol | 1.5 |

`None`表示没有可用计算值/未定义通用数值窗口；不能理解为零误差或放宽容差。水合PT按已核原文舍入及物理可比性判定，不从ET借容差。

实际计算/重新分析记录：

- [independent_state_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/independent_state_audit.json)
- [independent_thermochemistry_replay.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/independent_thermochemistry_replay.json)

逐个原生日志路径、SHA256、能量/频率/电荷自旋、提取位置及CPU/墙钟：[native_readback.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/native_readback.json)、[new_native_results.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/outputs/new_native_results.json)。源PDF/DOCX哈希及文字：[sources/index.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_c49993ae88ffa0e3/small_molecules_20261010T231612Z_g05/sources/index.json)。这些索引绑定真实native文件；平台SUCCEEDED和来源坐标不替代科学验证。

- 发布/规则问题：水合PT的通用数值接受边界尚未校准；本次参考数值恢复不等于任意新方法的自动评分规则已完备。
- 限定：GoodVibes4.3、Grimme qRRHO 100 cm−1、未缩放、298.15 K、1 M；有限作者结构池及完整去重，不宣称全局微溶剂构象收敛。
- 限定：当前规则允许水合PT按物理可比性及舍入值人工判断，本参考误差仅+0.002272 kcal/mol；未借用水合ET的±1.5或发明±1.0窗口。

本次是授权可读作者路线的参考计算验证，不证明盲发现。旧记录完整保留；旧局部PASS不能替代本轮扩展范围。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`ae81dc2220cfd5321978f5664444feb152ff23fa5788588028ed46101369995c`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_c49993ae88ffa0e3/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_c49993ae88ffa0e3/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_c49993ae88ffa0e3/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。


### 自主科研设计交叉复审补充

复审时间：2026-10-12T01:08:14.494560+00:00。本次仅修订任务合同或来源映射，不新增量化计算通过结论。已保留此前全部计算记录。父复审记录：[paper_c49993ae88ffa0e3](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/parent_review/paper_c49993ae88ffa0e3_decision.json)；变更文件：`evaluation/critical_failures.json`, `evaluation/reference_conclusions.json`, `evaluation/reference_key_points.json`, `evaluation/scoring_rules.json`。

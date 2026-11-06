# 当前任务科学问题验证结论（2026-10-22，按用户澄清统一验收口径）

**当前任务科学问题验证通过，状态PROVISIONAL_PASS_QUALITATIVE。自主科研与论文复现模式共享同一科学问题及同一验证证据，无需分别验证两次。** 这里的通过指当前科学关键点与最终定性结论有实际计算支持，数值偏差继续交专家审查。

验证允许使用作者提供的中间体、过渡态和计算方法作为起点，无需重新经历自主搜索。已有合格共同自由基对、N/O成键过渡态、同几何能量/热项及有效闭壳层N产物，支持现行四项科学规则：N成键20、O成键20、N产物20、最终N位点竞争解释40分。评分规则、科学问题及权重均未因本次说明修订而改变。

|核验量（kcal/mol）|论文|计算|计算−论文|
|---|---:|---:|---:|
|N局部G势垒|25.8|21.909254422|−3.890745578|
|O局部G势垒|33.7|30.313232571|−3.386767429|
|O−N势垒差|7.9|8.403978149|+0.503978149|

N通道更有利的方向一致。主要B3LYP-D3(BJ)/def2-SVP几何与频率、def2-TZVP单点、SMD DCM模型沿用作者方案；ORCA5.0.3→6.1.1、热项未完整披露及298.15/373.15 K来源冲突继续明确保留。没有认定全部数值严格一致。

结论限于作者失氮且已发生氢转移的自由基对模型内N/O竞争。自由基对形成全过程、完整自旋转换、π–π/NCI因果、精确产率及全论文所有计算不是当前任务的必需结果。其失败或未完成记录仍是事实，但不构成任一模式的当前任务验收阻碍；不把未合格驻点冒充合格，不把它们作为有效公共零点或全程能量图。

本轮没有新增量化计算。仅统一验收说明，并清理维护副本公开指令中“研究质量分”及“必须执行全部披露基线”的歧义；不会向自主科研Agent提供私有作者结构或答案。完整原生日志、源文件和核验结果见下方历史审计链接。

## 历史记录：旧模式分开验收口径已由上述结论替代

以下文字及失败计算原样保留用于追溯。旧“仅AR通过、PR未通过/INCOMPLETE_DISCLOSED_BASELINE”描述的是当时扩大到整套披露基线的检查，不再代表当前任务科学问题的验收状态。

---

# 现行科学分V2与验收范围（2026-10-22）

当前AR：PROVISIONAL_PASS_QUALITATIVE；`paper_science_v2`，4项、100分，仅科学结果。中间关键节点60分、最终结论40分。可按本版规则评分；专家发布审查尚未完成。

解释型题面与旧规则没有独立数值目标；本版不为两个明显偏差设宽窗。论文25.8/33.7及其差7.9保留为参考上下文，依据有实际证据的成键事件和竞争方向评分，不奖励方法执行或失败说明。

方法/范围限定：
- AR的条件性科学问题通过；PR仍INCOMPLETE_DISCLOSED_BASELINE，不能声明两模式完整通过。
- N/O局部G势垒对作者差−3.890746/−3.386767，O−N差+0.503978 kcal/mol；数值接受程度交专家。
- 作者ORCA5.0.3→实际6.1.1；298.15 K与SI G373.15表头冲突，低频处理未完整公开，实际采用native quasi-RRHO。
- 上游HAT与若干产物有额外负频/残余力，3Int3三重态N产物不合格；不用于有效公共零点/全程曲线。没有独立验证IBO/QRO/NCI因果、ISC或真实布居。

本次复制与评分迁移未提交新计算，公开输入、身份与交付合同逐字节保留。题面中若有历史过程分措辞，不构成本版得分条件；本版不奖励过程、失败诊断或资源投入。下方按日期保留原始验证记录；旧pending/失败不是当前验收状态，失败原日志也未改写为成功。

---

<!-- PARENT_QUALITATIVE_ACCEPTANCE_20261022T0725Z -->
## 2026-10-22 父级验收：AR科学问题定性通过，PR完整公开基线仍未完成

更新UTC：2026-10-22T07:54:49.190823+00:00。**自主科研模式登记PROVISIONAL_PASS_QUALITATIVE；论文复现模式仍为INCOMPLETE_DISCLOSED_BASELINE。** 两模式共享的位点选择性科学问题获得同一有效证据支持；PR多出的已公开基线执行要求并未全部满足，不能称两模式均完整通过，也不重复计算论文数。

现行AR题面允许有明确模型限定的选择性解释，不要求独立证明全部光活化过程。有效共同三重态自由基对3Int2、N/O两竞争TS及正确闭壳层N产物1Int3，支持作者后N2损失模型内N成键较有利。当前结论完整覆盖该条件性问题；没有修改题面或把未合格全程基线排除后冒称完整作者路线复现。

N/O过渡态分别有唯一正确成键虚频−688.69/−860.61 cm⁻¹，普通力标准合格；共同3Int2无虚频。闭壳层N产物102正振动模式，MAX梯度0.0002247987 Eh/bohr，小于实际ORCA默认0.0003，C29–N4=1.46235 Å且分子图对应题面产物。真实同几何TZVP单点与自身低层热项配对，公共零点使用有效3Int2。

| 比较（Gibbs，kcal/mol） | 作者 | 计算 | 计算−作者 |
|---|---:|---:|---:|
| N_local_G | 25.800000 | 21.909254 | -3.890746 |
| O_local_G | 33.700000 | 30.313233 | -3.386767 |
| O_minus_N_local_G | 7.900000 | 8.403978 | +0.503978 |

两绝对势垒偏低约3.4–3.9 kcal/mol，O−N差偏高0.503978；**N路径较有利的方向一致，数值接受程度交专家**。物理方法B3LYP-D3(BJ)/def2-SVP几何/NumFreq及def2-TZVP单点、SMD(DCM)、RIJCOSX；作者ORCA5.0.3与实算6.1.1、正文298.15K与SI栏373.15K冲突及实际数值设置差异保留，不称全部参数逐字相同。当前采用明示298.15K、1atm及ORCA原生quasi-RRHO；作者未完整披露低频热化学设置。独立审查严格配对热化学段E/G后得到上述表值；负责人的高精度末次电子能记账值21.909044/30.313239/8.404195与其相差不足0.00022 kcal/mol，两套原始记录均保留，不影响判断。

PR真实缺口：3Int1有−12.28；3TS1to2有−1594.79/−22.77/−12.62；1Int2有−21.97；3Int4有−109.38；1Int4有−21.96 cm⁻¹。1Int1、3TS1to2、3Int3的MAX力也超过实际ORCA默认3×10⁻⁴ Eh/bohr，3Int3不能因正频就写成合格最低点。未合格组件不参与AR候选的公共零点或完整能量图；未删负频或放宽阈值。早期独立审查口头采用较宽力门槛的判断已纠正，以最终报告为准。

不声称验证了完整氢转移/ISC过程、NCI因果解释、光生成效率、精确产物比/收率或唯一机制。定性通过仅指原题允许的位点竞争模型解释，不能扩展为上述未证实结论。[独立审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_acceptance_check_20261022T0725Z/479_independent_review/独立审查.md) · [作者数值与有效/无效全谱分离记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_acceptance_check_20261022T0725Z/stage07_new5/paper_47948e26afff46f6/author_comparison.json) · [父级登记](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_acceptance_check_20261022T0725Z/parent_acceptance_decision.json)。

下方为历史记录；旧pending、候选或旧归因不覆盖本次明确结论。

---

# Independent computation verification reference

Paper paper_47948e26afff46f6; mode autonomous_research; UTC 2026-10-22T01:57:17.281166+00:00.

**Status: INCOMPLETE.** No new AR or strict numeric registration. f62 PR parent approval is recorded separately; parent owns its packages.

固定几何准确Hessian原生正常结束，108个总模式、101个正振动及唯一−688.69cm⁻¹虚频；主模式C29–N4成键，普通梯度标准通过。
旧−28.59cm⁻¹软模在新Hessian中最相似模式为+15.62cm⁻¹（归一化Cartesian重叠0.945）；旧/新投影曲率−1.82524e−4/+1.33172e−4Eh/bohr²。新值与两幅度方向梯度正曲率一致，支持旧小负频对数值设置敏感。SCF精度和步长同时改动，不能独立归因；没有删除负频。
同几何TZVP后继已正常完成（63.12秒）：E=−991.224293372423Eh。复用有效O/Int2，N/O局部G势垒21.9090/30.3132kcal/mol；O−N=8.4042，作者25.8/33.7及7.9。N选择性定性支持，绝对值偏差及298.15/373.15K源标注冲突保留。
缺失氢转移与产物基线驻点/热项已准备并按真实jobs记录提交：triplet2个、singlet3个、products4个源几何NumFreq。复用12个TZ单点和已验证Int2/N/O；不做全IRC或重复优化。返回后逐项核力、模式、热项并审查整题资格。

[Current native evidence](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_47948e26afff46f6/job_progress_resume_20261022T013509Z/native_scientific_review.json) · [author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_47948e26afff46f6/job_progress_resume_20261022T013509Z/author_comparison.json) · [coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_47948e26afff46f6/job_progress_resume_20261022T013509Z/coverage.json) · [jobs and handoff](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_47948e26afff46f6/job_progress_resume_20261022T013509Z/handoff.md)


# Current V3 question and reused verification evidence — 2026-10-27

The public task now supplies neutral cis/trans candidates and withholds the observed configuration. It retains electronic-state access and skeletal rearrangement, and asks for a qualitative formation-preference prediction. Active scoring follows `scoring_rules.json` (20/40/40 points). Older task wording, scoring weights and mode-specific status statements below are historical records.

The existing native calculations cover this bounded revision: trans−cis product Gibbs energy is 23.564487 kcal/mol (source 23.5), and trans−cis crossing-point T1 electronic energy is 3.777547 kcal/mol (source approximately 3.7); the S0 comparison is also cis-favored at 3.576105 kcal/mol. The source crossing geometries were checked with low-level forces and energy gaps. These formation-relevant comparisons and product results support the qualitative cis prediction; product stability alone is not substituted for formation evidence. The existing electronic-state and skeletal calculations remain applicable.

This revision reuses existing evidence and performs no new quantum calculations or ARCHE run. It does not establish exact dr, ISC rates, target-product room-temperature equilibration or a globally unique pathway. Source-geometry verification remains distinct from an autonomous search.

---

# Historical verification record — prior task versions

# 2026-10-21 科学分V2现行评分资格

当前维护包采用 `paper_science_v2`：100分独立二元科学结果项；`reference_qualification.json`允许本版评分，出版专家审查仍待完成。下文历史过程分、pending或“评分状态不变”等措辞仅为当时审计，不覆盖本节现行资格；原始计算记录完整保留。两模式核心科学问题一致；本AR维护包不因PR作者指导增加HAT/羰基三重态或精确作者数值门槛。

---

# Independent computation verification reference

Paper: paper_f62b895afc2db020; mode: autonomous_research; parent update UTC: 2026-10-21T11:47:47.698299+00:00.

**Current parent status: PROVISIONAL_PASS_QUALITATIVE.** 自主科研模式的当前科学问题已由父级独立审查后验收；论文复现模式的额外公开基线比较仍未全部核收，两种模式分别登记。主要数值接近论文；此处不声称正式数值评分满分、发布批准或整篇论文全部计算完成。

[父级验收决定](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_return_followup_20261021T1125Z/parent_acceptance_decision.json) · [独立验收报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_return_followup_20261021T1125Z/f62_parent_review/独立验收.md) · [父级24份原生日志核查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_return_followup_20261021T1125Z/f62_parent_review/independent_native_audit.json)。

## 实际计算过程

直接使用作者源构象，独立执行ωB97X-D/def2-SVP/SMD(DMSO)频率/力、同几何def2-TZVP/SMD(DMSO)单点；8个普通驻点为6个全正频最低点、2个正确单虚频TS，均105振动且普通力标准达标。TS1/TS2的−444.6489/−490.2070cm⁻¹位移分别对应C–C加成与原环C–C断裂，并核源分子连接和不同原子排序。

Shermo 2.6.2读取本次Freq日志及本次SP电子能，采用Grimme100cm⁻¹熵插值、298.15K/1atm及未缩放频率得到G/H。父级重新解析8个Freq、8个SP、4个低层交叉面Force、4个高层交叉面SP与8份Shermo输出，确认数据来自实际独立计算。

cis/trans源MECP的低层双面能隙及有效梯度满足所用sobMECP标准；高层双面比较均cis更低，作者SI电子值对应T1面。源产物和交叉结构的酯基/苯基同侧/异侧关系已实际核查。没有完整重跑ABCluster全构象、全IRC或完整MECP搜索轨迹，不据此声称全球最低路径或精确动力学。

## 实算与论文比较

单位kcal/mol；差值为实算−论文。

|量|论文|实算|差值|
|---|---:|---:|---:|
|三重态Gibbs能差|52.2|52.228053|+0.028053|
|自由基加成Gibbs势垒|9.7|9.669168|−0.030832|
|开环Gibbs势垒|3.0|3.020956|+0.020956|
|开环反应Gibbs能|−13.6|−13.572089|+0.027911|
|trans−cis产物Gibbs能|23.5|23.564487|+0.064487|
|trans−cis交叉点T1电子能|约3.7|3.777547|+0.077547|

交叉点S0面的对应差为3.576105，亦cis较低；不得与T1混为同一量。低层MECP能隙为−1.27730e−5和−2.20300e−6Eh；不要求低层交叉几何在高层单点仍严格交叉。

## 定性结论与模式范围

自主科研CON1/CON2分别由有效的作者三重态加成/开环路线和cis交叉/产物的能量偏好支持。题面不要求证明唯一机理、ISC速率、室温异构化速率、精确dr或99%产率；本验收不扩大到这些结论。没有更改任务指令、evaluator、评分规则或容差。

PR公开基线的羰基三重态与1,5-HAT对照仍由hpc-job-4d4cc0ed-e324-4b28-96d9-16583a68e2d1计算/核收。AR通过不自动让PR通过。来源TXO65.5是给定文献比较量，未伪称本次计算的TXO激发能。

[逐项比较及原生路径](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f62b895afc2db020/job_return_followup_20261021T1125Z/author_comparison.json) · [驻点/位移/几何与MECP证据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f62b895afc2db020/job_return_followup_20261021T1125Z/native_scientific_review.json) · [工作进程覆盖记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f62b895afc2db020/job_return_followup_20261021T1125Z/coverage.json) · [实际作业与耗时](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f62b895afc2db020/job_return_followup_20261021T1125Z/jobs.json)。

工作进程历史候选记录由本页最新父级验收决定更新；原候选记录保留在验证目录供追溯。正式评分及发布状态不变。

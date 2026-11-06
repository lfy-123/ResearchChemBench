## 2026-10-23 科学分V2维护副本

当前私有评分为`paper_science_v2`，共6个二元科学项，中间关键节点60分、最终结论40分，总计100分。全部过程分已删除。新规则不设数值硬窗口，不改变既有定性验收或数值差异记录。公开输入保持原样，题面中旧过程分/60+40措辞不代表本维护副本实际计分，作为专家待审文字遗留披露。科学评分资格与发布资格分开，见`reference_qualification.json`。

## 2026-10-23 当前科学问题验证过程与结果汇总

当前AR状态：`PROVISIONAL_PASS_QUALITATIVE`；这是已完成独立审查后的定性验收，不是尚未验收的候选。严格整题数值复现未登记，数值偏差和实现差异保留供专家判断。本节整合既有实际计算，没有新增量化计算。

### 方法、模型与执行过程

B3LYP/6-31+G(d)/SMD-DMF与作者一致；实际Gaussian16 C.01替代来源Gaussian09。实际298.15 K、1 atm RRHO，作者完整热化学约定未报告。来源无Na显式模型，按−1单重态离子及中性H2/炔丙基溴配平。

1. 直接使用SI TS1（13原子）和TS2（18原子）坐标，重新优化/频率；分别得到正确N–H/H–H转移和N–C形成/C–Br断裂的唯一虚频。
2. 从有效IRC片段继续自由优化，核验初始接触态、S2/H2接触态、TS2前体和产物/Br接触态。118秒恢复作业继承原80步优化末几何并真正收敛，失败前代保留。
3. 独立计算H2和炔丙基溴并统一配平所有状态的原子、总电荷和两物种账本；构建图式相对能与实际已连接前体的局部势垒，不能混用参考。

### 论文与计算数值对照

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|TS1相对初态|−1.6|−1.603604|−0.003604|kcal/mol|
|S2相对初态|−25.5|−27.303811|−1.803811|kcal/mol|
|TS2相对初态|−9.3|−9.270657|+0.029343|kcal/mol|
|净产物形成G|−45.5|−45.655915|−0.155915|kcal/mol|
|图示S2→TS2能差|16.2|18.033154|+1.833154|kcal/mol|
|TS2−实际连接前体|未单列|15.082209|不作错配相减|kcal/mol|

### 定性结论与保留项

两步分子转化、正确N-炔丙基产物连接以及净放能得到支持；后续取代相对去质子化具有更明显局部活化需求。TS1相对自由能略负不能解释为实验严格零势垒。

- Gaussian版本、未报告热化学约定及电荷/自旋重建不同或不明，不能声称全部作者设置逐项一致。
- 旧前向IRC失败保留，连接使用有效片段加真正极小点；S2后续Hessian位移诊断例外及低频RRHO敏感性披露。
- 图式S2→TS2=18.033154与真实前体局部高度15.082209不同，前者包含接触伙伴交换的热力学影响。
- 没有计算Na聚集/固体NaH、接触交换动力学、精确速率产率或全文分子对接；均不是本题必要范围。

### 原生结果、独立复核及来源

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/acceptance_audit.md)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/acceptance_audit.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [native_recheck.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/native_recheck.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_f2a9e1bc87fc9b54/documents/main.pdf)：PDF页序（1-based）2,3。
- [supplementary_001.docx](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_f2a9e1bc87fc9b54/documents/supplementary_001.docx)：Theoretical study、Table 1及Cartesian coordinates（DOCX，不伪造PDF页码）。

来源方法未报告项、数值差异与题外未计算项目不能混为同一类问题。下方原有记录按日期保留，旧candidate/pending仅表示当时状态，不覆盖本节引用的最新父级验收。

---

## 历史验证记录（原文保留）

<!-- parent-acceptance-20261022T1743Z -->
## Parent acceptance — 2026-10-22 17:43 UTC follow-up

Current mode status: `PROVISIONAL_PASS_QUALITATIVE`. Independent source/native-log review supports all required qualitative conclusions of this current scientific question under the disclosed author model. This is provisional qualitative verification, not strict numerical replication or a change to scoring/release. The earlier candidate statements below are historical and are superseded only within the scope recorded here.

Parent decision: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/parent_acceptance_decision.json`. Independent audit: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_f2a9/acceptance_audit.json`.

Both current C1/C2 conclusions are supported. Source-figure S2-to-TS2 gap: computed 18.033154 versus 16.2 kcal/mol, difference +1.833154. Net reaction free energy: −45.655915 versus −45.5 kcal/mol, difference −0.155915. S2 relative energy differs by −1.803811 kcal/mol. The actual TS2-connected precursor gives a distinct local barrier of 15.082209 kcal/mol and must not be conflated with the diagram gap. Eight final native states, original SI TS coordinates, frequency modes, endpoint identity and balanced reference accounting were independently checked.

Retained qualifications:

- B3LYP/6-31+G(d), SMD DMF and original SI TS coordinates retained; Gaussian16 C.01 substitutes Gaussian09. Source lacks full thermal conventions; 298.15 K /1 atm RRHO and ionic charge/spin reconstruction are explicitly disclosed.
- Both historical forward IRC failures remain failures; accepted segments plus valid relaxed endpoints support current connectivity. Reverse TS2 reaches the 30-point limit then a separate successful minimization, not a claimed uninterrupted full IRC.
- S2 Opt passed all native criteria; frequency Hessian displacement diagnostic exceeds one threshold but negligible forces and 33 positive modes support the native stationary-point result.
- Balanced energy comparisons retain propargyl bromide and H2; S2-to-TS2 diagram gap 18.033154 is different from the actual connected local barrier 15.082209.
- No exact barrierless experimental step, contact-exchange kinetics, free bromide dissociation, sodium aggregation/solid NaH, full alternative-route exhaustion or rate/yield reproduction claimed.

<!-- end-parent-acceptance-20261022T1743Z -->

<!-- SHORT_JOB_FOLLOWUP_20261022T1743Z_GROUP04 -->
最新核收 2026-10-22T17:56:26.116919+00:00，模式 autonomous_research；**PROVISIONAL_PASS_QUALITATIVE_CANDIDATE**。本轮状态取代下方历史待返回描述；候选不等于父级已验收或全局已登记。

# paper_f2a9e1bc87fc9b54 新返回作业核收

2026-10-22T17:56:26.116919+00:00；当前状态：**PROVISIONAL_PASS_QUALITATIVE_CANDIDATE**。两模式共用计算。

- TS2前向Cartesian续算原生118.350秒、rc0/2Normal，18原子48正频，最低20.8698cm⁻¹；N···C4.161462Å、C-Br1.994766Å，反应物阴离子/炔丙基溴复合物有效。
- TS2独立reverse原生1396.664秒、rc0/3Normal；IRC达到设定30点后正常结束，随后自由OptFreq得到18原子48正频产物最低点，最低31.8544cm⁻¹。不把IRC有界结束冒称IRC本身到达最低点。
- 同原子顺序核对唯一成键N2-C9和断键C9-Br12；N-C1.470732Å、C···Br3.663496Å。末端C≡C1.210680Å、beta硝基吡咯图保持；TS1产物与TS2反应物的11原子阴离子子图同构。
- 原TS1/TS2均各一虚频且真实路径段连接至频率核验最低点。旧正向IRC失败记录保留，采用已接受15/7点+端点优化的连接证据，不宣称完整正向IRC正常终止。
- 配平C7H8BrN2O2、电荷−1、每个状态两物种：TS1−1.603604、S2接触态−27.303811、TS2−9.270657、产物+H2−45.655915kcal/mol。作者分别−1.6/−25.5/−9.3/−45.5，有符号差−0.003604/−1.803811/+0.029343/−0.155915。
- TS2相对已连接反应物接触复合物局部ΔG‡15.082209kcal/mol；作者式TS2+H2减S2+炔丙基溴为18.033154，对16.2差+1.833154，其中接触伙伴交换ΔG为+2.950945。不混用两种零点。
- TS1电子势垒+0.295867kcal/mol，RRHO自由能差−1.603604；计算支持第一步难度小于取代步，但负ΔG差不证明实验无动力学势垒。净产物形成放能支持当前C1/C2的模型限定结论，不能定量解释89%收率或24h。
- 复查S2优化四项标准均通过；后续精确Hessian诊断max displacement0.002807虽超过0.0018，原生Gaussian按可忽略力终止（max4e−6/rms1e−6Eh/bohr），33频率全正。保留该细节，没有放宽阈值。

方法：B3LYP/6-31+G(d), SMD N,N-dimethylformamide. Gaussian16 instead of09; inferred charge−1/singlet for each TS, author geometry contains noNa.298.15K/1atm declared assumptions.

| 配平状态 | 本次ΔG | 作者ΔG | 有符号差 | 绝对差（kcal/mol） |
|---|---:|---:|---:|---:|
| initial | 0.000000 | 0.00 | +0.000000 | 0.000000 |
| TS1 | -1.603604 | -1.60 | -0.003604 | 0.003604 |
| S2_H2_contact | -27.303811 | -25.50 | -1.803811 | 1.803811 |
| TS2 | -9.270657 | -9.30 | +0.029343 | 0.029343 |
| product_Br_contact_plus_H2 | -45.655915 | -45.50 | -0.155915 | 0.155915 |

C1：氢负离子接受N-H质子形成H2，beta硝基吡咯阴离子随后在炔丙基碳形成N-C、断C-Br；两步骤连接和指定产物图均有执行证据。C2：局部取代势垒与整体放能分别核算，来源所需的主要定性方向保持。当前题目明确允许声明且合理的离子简化模型，因此未指定Na/聚集和来源热化学约定作为局限披露，不额外扩成全NaH微观研究。该候选待父级审查，非数值严格通过、非全局登记。

局限/待解决事项：

- B3LYP/6-31+G(d)/SMD DMF author physical method retained. Gaussian16 substitutes Gaussian09; ultrafine integration and xqc convergence disclosed in inputs.
- 298.15 K, Gaussian RRHO and 1 atm selected and native-confirmed. Source thermochemical temperature, standard-state/correction recipe unspecified. No invented author correction or 1M conversion.
- NaH represented by a hydride anion; sodium/aggregation/bulk solid and explicit solvent absent as in supplied author coordinate model. This resolves the stipulated molecular explanation, not bulk NaH reactivity or quantitative yield/rate.
- Both old forward IRC runs aborted after accepted TS1 15 / TS2 7 points. Endpoint optimizations preserve these branches; no claim of complete forward IRC normal termination.
- S2_H2_contact optimization passed all four standard criteria. Its subsequent exact-Hessian diagnostic predicts max displacement0.002807>0.0018, but native Gaussian completes on negligible forces (max4e-6/rms1e-6 Eh/bohr); all33 modes positive. Recorded without changing thresholds or claiming four final diagnostic passes.
- TS2 reverse IRC normal-terminated at the configured 30-point bound, not a minimum. Its subsequent unrestricted optimization and 48-positive-mode frequency calculation establish the product minimum.
- S2 includes weak H2 contact; TS2 precursor includes propargylBr contact, product includes Br contact. Balanced two-species comparisons account for separate H2/reagent. Association exchange kinetics and dissociation to isolated Br- were not computed.
- The supported deprotonation/substitution sequence is a viable author-model account, not proof of exclusive mechanism, barrierless experimental deprotonation, or a rate inferred from 89% yield/24h.

下一步：父级按当前C1/C2和所列方法/模型边界复核两模式定性候选；无需额外计算，不登记全局通过数。

实测与ETA：全部当前最低必要计算已完成。TS2端点修复118.350s；reverse IRC+OptFreq1396.664s；旧前向失败1185.327s保留而不计成功。

[覆盖](coverage.json) · [作者比较](author_comparison.json) · [逐ID诊断](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/new44_group_04/failure_triage.json) · [作业](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/new44_group_04/jobs.json)。


本轮精确作业状态：

- `hpc-job-137e9bed-2989-45ab-8118-372145ce2cae` / author_TS2_solvent_fix1: SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED.
- `hpc-job-a5b9703e-df5d-468f-ad69-8ccf9e94d204` / author_TS1_connections: SUCCEEDED / NATIVE_INCOMPLETE.
- `hpc-job-a5e06f86-481c-4d31-b3ca-ccdce7bbddeb` / author_TS1_solvent_fix1: SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED.
- `hpc-job-b9ee8db0-d7df-47ff-937a-b0bf3cb14aa7` / author_TS2_connections: SUCCEEDED / NATIVE_INCOMPLETE.
- `hpc-job-32bd7d23-fe21-4502-a07a-9bd47d51d3ee` / author_TS2: SUCCEEDED / NATIVE_INCOMPLETE.
- `hpc-job-1084c200-a865-4c7d-99f8-632b70fac713` / author_TS1: SUCCEEDED / NATIVE_INCOMPLETE.
- `hpc-job-28ea07ba-e72a-4b23-9d8b-90d122f75c5d` / TS1_connected_endpoints_v2: SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED.
- `hpc-job-543a1588-7c75-45c4-aafd-cb41badfdc95` / TS2_forward_endpoint_Cartesian_recovery: SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED.
- `hpc-job-6cb96821-69d3-41cc-a443-396e335cefee` / TS2_connected_endpoints_v2: SUCCEEDED / NATIVE_INCOMPLETE.

[交接](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/new44_group_04/handoff.json) · [候选](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/new44_group_04/acceptance_candidates.json) · [验包](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/new44_group_04/formal_update_validation.json)。仅此证据记录和manifest更新，其他载荷保持。
<!-- END_SHORT_JOB_FOLLOWUP_20261022T1743Z_GROUP04 -->

<!-- SHORT_JOB_FOLLOWUP_20261022T1645Z_GROUP04 -->
最新核收：2026-10-22T17:22:20.616913+00:00，模式autonomous_research，**TS1_CONNECTED_MINIMA_COMPLETE_TS2_RECOVERY_ACTIVE**；新增整题候选0。以下本轮状态取代此前运行/排队描述，成功历史证据继续保留。

# paper_f2a9e1bc87fc9b54 短作业诊断与接续

2026-10-22T17:22:20.616913+00:00；状态 **TS1_CONNECTED_MINIMA_COMPLETE_TS2_RECOVERY_ACTIVE**；整题候选0，两模式共用计算。

- 两作者TS优化/频率成功继续复用，原始DMF缩写失败已有成功后继，未重新优化TS。
- 新发现TS1/TS2正向IRC分别在pt16/pt8耗尽20次corrector，原生rc1、0Normal；失败平台仍报SUCCEEDED。
- 真实2CPU本地Restart测试均复现耗尽计数，未进行新SCF，未把这两个输入投HPC。改从已收敛正向pt15/pt7接续自由端点优化；TS1种子N-H1.85318Å/H-H0.76303Å，TS2种子N-C2.52401Å/C-Br2.10947Å，既有有效路径保留。
- 两个修复后继已提交。此前未启动的reverse方向读原TS Hessian，使用MaxCycle100/StepSize5/ReCalc5，作者B3LYP/6-31+G(d)/SMD DMF、-1 singlet及收敛门槛保持。TS1后继另含原SI H2/炔丙基溴0 singlet最低点以补配平能量。
- 改版预检时共享锁忙，记录SKIPPED_LOCAL_LOCK_BUSY并按授权有界HPC；未称本地通过。新runner原生失败返回非零，独立阶段可继续，保留所有旧输出。
- TS1修复后继已成功完成：H2 1个正频、炔丙基溴15正频，正反端点各33正频；正向262.8s、反向115.3s。初态N-H1.08986Å/H···H1.40586Å，H2端点N···H3.17172Å/H-H0.74379Å，连接身份成立。
- 配平C7H8BrN2O2总电荷−1的两分子参考下，TS1−1.603604对−1.6差−0.003604、S2−27.303811对−25.5差−1.803811、TS2点−9.270657对−9.3差+0.029343kcal/mol。TS2连接仍未闭合，18.033154与作者16.2的差+1.833154保留为模型能差，未称为独立已验证势垒。
- TS2接续正向端点80步耗尽，末步max/rms force0.000179/0.000028均通过，但displacement0.012232/0.003946未通过。仅从末checkpoint新增Cartesian/CalcFC/MaxStep5端点续算；2CPU本地55.2秒预检得到1个SCF并进入后续模块，未声称预检完成最低点。原TS2reverse仍运行，未取消或重做。

方法与来源：B3LYP/6-31+G(d), SMD N,N-dimethylformamide. Gaussian16 instead of09; inferred charge−1/singlet for each TS, author geometry contains noNa.298.15K/1atm declared assumptions.；main pp2–3 methods/Figure1; new DOCX supplementary theoretical-study table and TS1/TS2/H2/alkylBr Cartesian records

当前阻碍：

- TS1连接与最低点完成；TS2单独正向端点续算和反向仍需核收；原正向IRC不称全程正常终止。
- H2与炔丙基溴已完成，前三个配平能量点可算，但完整产物能量和TS2局部连接未闭合。
- 原NaH聚集/钠离子处理及源T/标准态缺失；保留分子模型的解释边界。

下一步：核收TS2反向和单独正向端点续算，验证最低点与物种对应；复用已完成TS1连接与H2/炔丙基溴，再补完整配平产物能量。来源条件限制保留。

实测时间与ETA：TS1修复原生总411.4秒：H2 6.0s、炔丙基溴27.1s、正向最低点262.8s、反向IRC+最低点115.3s；TS2未完成部分ETA未知。新端点Cartesian预检55.2s/1SCF只证明启动，不是收敛时间预测。

[coverage](coverage.json) · [作者比较](author_comparison.json) · [逐ID诊断](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1645Z/new44_group_04/failure_triage.json) · [作业](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1645Z/new44_group_04/jobs.json)。


精确逐ID检查时间2026-10-22T17:21:55.738120+00:00：

- `hpc-job-137e9bed-2989-45ab-8118-372145ce2cae` / author_TS2_solvent_fix1：SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED。
- `hpc-job-a5b9703e-df5d-468f-ad69-8ccf9e94d204` / author_TS1_connections：SUCCEEDED / NATIVE_INCOMPLETE。
- `hpc-job-a5e06f86-481c-4d31-b3ca-ccdce7bbddeb` / author_TS1_solvent_fix1：SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED。
- `hpc-job-b9ee8db0-d7df-47ff-937a-b0bf3cb14aa7` / author_TS2_connections：SUCCEEDED / NATIVE_INCOMPLETE。
- `hpc-job-32bd7d23-fe21-4502-a07a-9bd47d51d3ee` / author_TS2：SUCCEEDED / NATIVE_INCOMPLETE。
- `hpc-job-1084c200-a865-4c7d-99f8-632b70fac713` / author_TS1：SUCCEEDED / NATIVE_INCOMPLETE。
- `hpc-job-28ea07ba-e72a-4b23-9d8b-90d122f75c5d` / TS1_connected_endpoints_v2：SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED。
- `hpc-job-543a1588-7c75-45c4-aafd-cb41badfdc95` / TS2_forward_endpoint_Cartesian_recovery：RUNNING / NOT_STARTED。
- `hpc-job-6cb96821-69d3-41cc-a443-396e335cefee` / TS2_connected_endpoints_v2：RUNNING / NATIVE_INCOMPLETE。

[真实诊断](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1645Z/new44_group_04/failure_triage.json) · [修复对应](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1645Z/new44_group_04/repair_lineage.json) · [覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/short_job_followup_20261022T1645Z/coverage.json) · [作者比较](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/short_job_followup_20261022T1645Z/author_comparison.json) · [本轮交接](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1645Z/new44_group_04/handoff.json) · [验包](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1645Z/new44_group_04/formal_update_validation.json)。

仅更新此核验记录与manifest；题面、科学身份、评分规则、权重和容差保持。
<!-- END_SHORT_JOB_FOLLOWUP_20261022T1645Z_GROUP04 -->

<!-- NEW44_20261022_GROUP04 -->
# 当前题目计算核验记录

核收：2026-10-22T16:02:07.948878+00:00；论文：paper_f2a9e1bc87fc9b54；模式：autonomous_research。
本轮状态：**PARTIAL_TS_VALIDATED_CONNECTIONS_ACTIVE**。这是核验证据记录，**不是整题通过或评分决定**。两个模式共用计算，不重复提交。
核验前任务包内容哈希：`41f5c33fe24fefb674710093a741ddcdaa0cfd24c95898064c6bb5afc2622a83`。当前包内容哈希因本核验文件加入而更新；题面、科学身份、评分规则、权重及容差保持原字节。

# paper_f2a9e1bc87fc9b54 — 2026-10-22 首轮验证

状态：PARTIAL_TS_VALIDATED_CONNECTIONS_ACTIVE。两模式共用一套科学验证；整题尚未提出通过候选。

问题：For the base-promoted N-alkylation of 3-nitro-1H-pyrrole with propargyl bromide in DMF, what computed chemical behavior best describes formation of N-propargyl-3-nitropyrrole, and which computed energetic and structural features support that description?

方法：B3LYP/6-31+G(d), SMD N,N-dimethylformamide. Gaussian16 instead of09; inferred charge−1/singlet for each TS, author geometry contains noNa.298.15K/1atm declared assumptions.

来源页：main pp2–3 methods/Figure1; new DOCX supplementary theoretical-study table and TS1/TS2/H2/alkylBr Cartesian records

- New SI closes prior missing-coordinate/frequency source gap. Both direct author TS optimizations terminate normally with one imaginary mode:−1061.5137 and−437.9409cm⁻¹.
- Computed absolute Gibbs energies differ from SI by+0.01126 and+0.04140kcal/mol. These are matched-state comparisons, not reaction barriers or whole-question pass.
- Initial DMF keyword parse failures repaired to full solvent name; subsequent healthy SCF/frequency results retained. Double-direction IRC and endpoint minima are submitted from these verified checkpoints.
- Connection successor readback: author_TS1_connections RUNNING / RUNNING; author_TS2_connections RUNNING / RUNNING. Live SCFs do not yet establish completed IRC/endpoint evidence.

剩余与阻碍：

- Both TS connectivity paths and endpoint identities not yet fully consumed. Chemically balanced net reactant/product energy reference across H2 and alkylBr remains to be established.
- Missing sodium/aggregation treatment and unreported source T/standard-state prevent unconditional experimental kinetic interpretation.

后续：Consume two connection jobs, verify modes/endpoint graph and atom/charge balance, then fill only required component minima energies (H2/alkylBr etc) if still absent. No repeated TS optimization.

实测时间/ETA：TS1 optimization/frequency53.1s and TS2143.8s at20CPU measured. IRC+endpoint stages are different and have no completed timing baseline; total ETA unknown.

计算输入、原生日志及作业回执见 [coverage.json](coverage.json)、[author_comparison.json](author_comparison.json) 和各阶段 submission/latest_check.json。


原生证据及分析：

- [source_geometry_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/source_geometry_audit.json)
- [independent_TS_comparison.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/independent_TS_comparison.json)
- [result.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/author_TS1_solvent_fix1/native/result.json)
- [result.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/author_TS2_solvent_fix1/native/result.json)
- [spec.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/author_TS1_connections/spec.json)
- [spec.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/author_TS2_connections/spec.json)

作业最后核查 2026-10-22T16:01:12.112476+00:00：

- `hpc-job-137e9bed-2989-45ab-8118-372145ce2cae` / `author_TS2_solvent_fix1`: SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED.
- `hpc-job-a5b9703e-df5d-468f-ad69-8ccf9e94d204` / `author_TS1_connections`: RUNNING / RUNNING.
- `hpc-job-a5e06f86-481c-4d31-b3ca-ccdce7bbddeb` / `author_TS1_solvent_fix1`: SUCCEEDED / STAGES_COMPLETE_REVIEW_REQUIRED.
- `hpc-job-b9ee8db0-d7df-47ff-937a-b0bf3cb14aa7` / `author_TS2_connections`: RUNNING / RUNNING.
- `hpc-job-32bd7d23-fe21-4502-a07a-9bd47d51d3ee` / `author_TS2`: SUCCEEDED / NATIVE_INCOMPLETE.
- `hpc-job-1084c200-a865-4c7d-99f8-632b70fac713` / `author_TS1`: SUCCEEDED / NATIVE_INCOMPLETE.

平台SUCCEEDED只代表启动包装程序结束；历史NATIVE_INCOMPLETE保留为失败证据。只有日志、驻点/物种和实际问题范围核查完成的部分可复用；未完成连接、来源方法矛盾及未收敛驻点均不当作数值偏差通过。

[逐项覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/coverage.json) · [作者数值比较](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_f2a9e1bc87fc9b54/new44_20261022/author_comparison.json) · [真实作业与资源](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/new44_dispatch_20261022T1513Z/group_04/jobs.json) · [修复对应关系](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/new44_dispatch_20261022T1513Z/group_04/failure_repair_lineage.json) · [交接](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/new44_dispatch_20261022T1513Z/group_04/handoff.json) · [任务包完整性](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/new44_dispatch_20261022T1513Z/group_04/formal_update_validation.json)。
<!-- END_NEW44_20261022_GROUP04 -->


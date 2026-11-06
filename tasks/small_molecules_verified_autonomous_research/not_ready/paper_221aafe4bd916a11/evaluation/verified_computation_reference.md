# 2026-10-21 科学分V2现行评分资格

当前维护包采用 `paper_science_v2`：100分独立二元科学结果项；`reference_qualification.json`允许本版评分，出版专家审查仍待完成。下文历史过程分、pending或“评分状态不变”等措辞仅为当时审计，不覆盖本节现行资格；原始计算记录完整保留。保留21.8±3 kcal/mol势垒窗口；捕获/分离产物只作独立定性判定，严格数值整题通过未登记。

---

<!-- PARENT_ACCEPTED_221A_HIGH_20261020 -->
# 当前父级独立验收结论

2026-10-20T19:18:24.617098+00:00。当前升级自主科研任务PROVISIONAL_PASS_QUALITATIVE，current_scope_verified=true，独立验收通过。 严格数值整题通过未新增登记。

有效P–CO2捕获最低点及同几何高层单点支持CO2捕获不利：298K ΔG=+10.762416对+15.0，差−4.237584 kcal/mol；298.15K为+10.765608。结合已有有效竞争路线，支持当前任务限定定性结论。

作者CREST/GFN2-xTB全构象流程未重新完整执行，采用来源构象和有界DFT构建；来源精确捕获构象对应未建立。只支持此处实际验证的共价物种/模型，不声称排尽全部捕获构象。pose2仍非驻点（−83.2402 cm⁻¹），未用于热化学。作者未报告细节和实现版本差异继续披露；无拟合零点或容差改动。旧窄论文复现模式通过不重复计入新增。

[独立审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/high_followup_20261020T1905Z/review_221a/独立验收.md) · [机器审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/high_followup_20261020T1905Z/review_221a/independent_review.json) · [父级登记](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/high_followup_20261020T1905Z/parent_acceptance_decision.json)。当前题目必要证据无待补项；以此节覆盖下方历史pending，不改任务、评分或发布资格。
<!-- END_PARENT_ACCEPTED_221A_HIGH_20261020 -->

---

<!-- HIGH_FOLLOWUP_20261020T1905Z_G04_BEGIN -->

## 最新科学核收 2026-10-20T19:14:51.308054+00:00

本模式：**PROVISIONAL_PASS_QUALITATIVE_CANDIDATE**。当前自主有限科学问题新增PROVISIONAL_PASS_QUALITATIVE候选1，父级验收待定、全局数未改；窄PR旧通过不重计。以下覆盖来源知情参考验证，不是盲测solver得分或发布。

两份新终态真实核收：4b16fd4e highSP rc0/1正常；2168e09f exactHessian rc0/1正常但含−83.2402cm⁻¹，不作最低点/TS。前轮“高层待返回”已被本轮结果取代。

完整pose1捕获最低点原Opt标准通过、240正频、82atom/+1singlet、P16–C80=1.903248Å、P11–H79保留、框架完整；新高层与其同几何RMSD4.71e−15Å。Ehigh=−2325.76722859Eh；自身Gcorr298K0.614152/298.15K0.614087181439Eh；分离参考298K−2325.170227591/298.15K−2325.170297496524Eh。1atm，无借热项/零点拟合。

|量kcal/mol|作者298K|本地298K|差|本地298.15K|
|---|---:|---:|---:|---:|
|转移势垒|21.8|21.669246|−0.130754|21.673991|
|分离还原产物|−3.0|−5.268970|−2.268970|−5.270941|
|完整P位点捕获|+15.0|+10.762416|−4.237584|+10.765608|

势垒在原±3内；捕获/产品没有新增容差，定性方向一致。298.15K产品比已测共价捕获低16.036548kcal/mol。复用TS单虚频/双向局部100点连接、独立正频formate和P–P二价阳离子（P–P2.212942Å）及同几何高层，支持本题直接有限计量还原与产品命运；不要求催化再生或全球唯一机制。

重要限制：pose2仍是更低电子能的非驻点，自由能未知。负模约97.82%打印平方位移为远端C20甲基H60/61/62转动，非转移/捕获反应模式；不使用其热项、不删除记录，不据此证明所有捕获构象吸能。已合格pose1提供所需源限定定量/结构比较，当前题目没有全构象系综要求，故不再盲补第二构象。该不确定性明确交父级审查；若具体新证据需要，保留Hessian指导甲基扰动/Cartesian小步的真实预检后恢复。确切作者capture构象坐标未给，未声称逐原子复现。

方法核对SI1–2两层wB97XD/PCM乙腈/defaultSCF/grid/Optthreshold；来源SI7TableS6+15和正文3–4。原298K与任务298.15K自有RRHO换算分列。旧辅助IRC使用披露的Tight/XQC/UltraFine连接设置，不冒充作者精确numerics；不把局部IRC当分离优化盆地。前轮早期CHK字节hash异常继续披露并引用/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/checkpoint_provenance_reconciliation.json；本轮新input/spec/log/CHK均匹配各自原回执，历史未改写。

报告：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/high_followup_20261020T1905Z/verification_report.md；coverage：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/high_followup_20261020T1905Z/coverage.json；对照：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/high_followup_20261020T1905Z/author_comparison.json；候选：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/high_followup_20261020T1905Z/original_group_04/acceptance_candidates.json；native：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/high_followup_20261020T1905Z/returned_native_audits.json；后继：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/high_followup_20261020T1905Z/successor.json；handoff：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/high_followup_20261020T1905Z/original_group_04/handoff.json。

<!-- HIGH_FOLLOWUP_20261020T1905Z_G04_END -->

<!-- CLOSEOUT_20261020T1530Z_G04_BEGIN -->

## 最新原生核收 2026-10-20T18:06:16.597556+00:00

模式状态：**CAPTURE_MINIMUM_QUALIFIED_HIGH_ENERGY_PENDING**。新增自主科学问题整题通过0；窄PR旧参考通过不重新计数。当前capture已有真正完整共价最低点，更新下列旧“无完整捕获最低点”状态；剩余见本轮报告。

pose1 ec628bbf：rc0/Opt与Freq均正常、原Opt所有标准通过、240正频、82atom/+1singlet，P16–C80=1.903248Å且P11–H79保留、完整框架未断裂。pose2 94c167c2：rc1/100步L9999，零正常/无Freq；较低电子能不是自由能或最低点。真实frame90Force测试后按当前曲率推进，有效pose1 Opt/Freq不重算。

|必要阶段|真实新ID|平台/原生状态|
|---|---|---|
| Capture_pose1_qualified_samegeom_highSP | hpc-job-4b16fd4e-cc47-4c4c-9b0c-b729088d12b5 | RUNNING / NATIVE_STARTED |
| Capture_pose2_frame90_exactHessian | hpc-job-2168e09f-cfcf-4f09-b08e-a7352e32c983 | RUNNING / NATIVE_STARTED |

新pose1自身298K热修正0.614152Eh，298.15K为0.614087181439Eh，1atm。作者同几何高层对照：捕获本地待高层原生返回 vs作者+15，差未定；无新增容差。复用势垒298K21.669245637/298.15K21.673991139 vs21.8，差−0.130754363/−0.126008861，在原±3内；分离产物−5.270940471 vs−3.0，差−2.270940471。非共价相遇+4.731758211及重排+65.097316197不代替捕获。已知更低未收敛pose2支路仍待曲率/优化诊断，不借热项或删难点。

方法同作者SI1–2两层wB97XD/PCM乙腈/defaultSCF/grid/convergence。SI7TableS6及sourcein-in20–22支持科学身份，未声称未知作者捕获坐标完全复现。所有新job均锁内实时双区资源、CPU、quota、去重、存储核查，20CPU100GiB/priority6，native20CPU80GB。

溯源异常：两份旧CHK在本轮formchk直接读入后当前字节hash不同于原receipt；不宣称历史CHK字节未变。原log/receipt保持，几何RMSD<5e−7Å/能量差<3e−9Eh/原子库存已重新对齐。详情/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/checkpoint_provenance_reconciliation.json。新计算只操作私有CHK复制件，原回执hash不改。

报告/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/verification_report.md；coverage/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/coverage.json；可实施性/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/computation_feasibility.json；jobs/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/jobs.json；后继/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/closeout_followup_20261020T1530Z/successor.json；handoff/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/closeout_followup_20261020T1530Z/original_group_04/handoff.json。无题面/输入/evaluator/容差/发布修改，无自动重启。

<!-- CLOSEOUT_20261020T1530Z_G04_END -->

<!-- TARGETED19_20261020T091107Z_G04_BEGIN -->

## 最新有限接续 2026-10-20T11:29:56.645370+00:00

模式：current_autonomous_research；状态：**INCOMPLETE_PENDING_IDENTITY_CONTROLLED_CAPTURE**。本轮没有新增自主整题通过；当前capture核心缺项仍待有效端点/自身Freq/同几何高层。以下新工作是来源知情参考验证，不是blindsolver评分提交。

发现并纠正旧暂停依据：SI TableS6PDF7已定义中性P捕获和+15kcal/mol；精确捕获坐标缺失，不代表方法未知或不能计算。旧in-out种子存在孤对方向遮挡、100度偏转及N17–O81短接触，随后P16–N17断裂/N–O生成；该重排不是源捕获。

本轮提取SI PDF20–22的作者in-in构象，79atom元素图映射成立，保留P11–H79与完整骨架；两个不同CO2方位，82atom/+1/singlet。真实4CPU预检各240s已执行多次SCF迭代、无原生错误，受控rc-15不是化学成功。两项已实际提交并核native20CPU/80GB启动。高层/热项必须等合格完整捕获最低点；不得借用既有相遇频率或删难点。

|目标|真实作业ID|平台/原生阶段|资源|
|---|---|---|---|
| Capture_source_inin_pose1 | hpc-job-ec628bbf-9a6f-4381-b6f6-1e79d1524aec | RUNNING / NATIVE_STARTED | 20CPU /100GiB(native80GB) |
| Capture_source_inin_pose2 | hpc-job-94c167c2-680d-4011-9c08-96a101536dfa | RUNNING / NATIVE_STARTED | 20CPU /100GiB(native80GB) |

作者方法wB97XD/6-31G(d,p)/PCMMeCN默认SCF/grid/convergence；新CalcFC/MaxStep10是数值选择；无几何约束。298K源与298.15K任务热项分列。逐次共享锁内检查CPU/两区精确quota/node/storage/dedup；终态已释放作业不再算未来增长，不清理文件。

复用对照：298K势垒21.669245637 vs21.8，差−0.130754363，在原±3内；298.15K势垒21.673991139，差−0.126008861。分离产物−5.270940471 vs−3.0，差−2.270940471；未新增容差。完整捕获作者+15，本地未完成。非共价相遇+4.731758211与重排+65.097316197身份不同，不当作捕获误差或通过。直接转移及其余有效证据继续复用；宽窄模式不混同。

当前coverage：directtransfer/activation/products已支持；capturecompetition未闭合；质态/原子/同几何热项必须逐项验收。下一触发：OnnativeOpt/Freqreturn inspect everyLink,rc/convergence/240modes,82atoms/+1singlet,P11-H79,P16-C80,bothC-O,allfourP-Nandwholeframework. Ifidentityqualified,submit samegeometrywB97XD/6-311++G(d,p)/PCMMeCN andcomputeownRRHO298/298.15K1atm relativeexistingin-out+CO2. Ifdissociated/rearranged/failed,recordtrajectoryanddiagnose; noautomaticrepeat, borrowedthermalterms, orall-basinsabsenceclaim.

完整报告：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/targeted19_continuation_20261020T091107Z/verification_report.md；coverage：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/targeted19_continuation_20261020T091107Z/coverage.json；可实施性：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/targeted19_continuation_20261020T091107Z/computation_feasibility.json；jobs：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/targeted19_continuation_20261020T091107Z/jobs.json；handoff：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/targeted19_continuation_20261020T091107Z/original_group_04/handoff.json。本轮仅reference/manifest更新，无题面/evaluator/评分/发布变动。

<!-- TARGETED19_20261020T091107Z_G04_END -->

<!-- FOLLOWUP_20261020T0220Z_G04_BEGIN -->

## 2026-10-20 新返回核收与有据接续

核收UTC：2026-10-20T03:34:35.208712+00:00。模式：current_autonomous_research；科学状态：**INCOMPLETE**。

直接氢转移、适中能垒和放热产物得到有效计算支持；当前自主任务仍缺身份受控P位点捕获比较。形式数值差或非共价相遇不是所缺物种的替代。

当前自主整题未闭合；未增加全局通过数、未改正式评分/容差/发布资格。失败计算不适用定性暂定通过豁免。

### 本轮实际执行

回读上轮科学验收基线及当前两模式题面哈希，成功阶段复用；无新失败机制或来源，不重复消耗。

保留全部作者/本地/带符号差值/原容差以及精确恢复条件；宽窄任务分开。

活动ID：无；SOURCE_ENDPOINT_IDENTITY_AND_REQUIRED_COMPARISON_INCOMPLETE。

### 方法与数值对照

来源：正文PDF3–4 Fig3/Table2；SI PDF1–2方法、7 TableS6、19–20反应物/产物、65–66 TS2。

{"low": "wB97XD/6-31G(d,p),PCMMeCN", "high": "wB97XD/6-311++G(d,p),PCMMeCN,samegeometry", "temperature_K": 298, "pressure_atm": 1, "RRHO": "own frequencies, no additional rounding/1M shift", "state": "82atoms,+1singlet", "additional_comparison_temperature_K": 298.15, "temperature_note": "298K is the author/narrow-task primary value; 298.15K is a separately disclosed rethermalization, never presented as exact298K."}

原生Gaussian16；物理方法wB97XD两层基组/PCMMeCN一致。298K源核算与298.15K重热化分列。频率与单点各自实际route在narrow_221_native_reuse.json；IRC采用UltraFine/SCFTight/XQC并披露，不声称其为作者报告的默认值。

|量|作者|本地|本地−作者|单位|原容差|判定|
|---|---:|---:|---:|---|---|---|
| direct_transfer_activation_author_298K | 21.800000000 | 21.669245637 | -0.130754363 | kcal/mol | ±3 | Author298K primary; native rc0 opt/freq/SP and bidirectional local IRC evidence; reference computation, not blind-submission scoring. |
| direct_transfer_activation | 21.800000000 | 21.673991139 | -0.126008861 | kcal/mol | ±3 | 原窗口内；有效局部转移 |
| separated_products | -3.000000000 | -5.270940471 | -2.270940471 | kcal/mol | 未定义/未取得 | 方向支持；无新标定窗口 |
| intact_CO2_capture | 15.000000000 | 未定义/未取得 | 未定义/未取得 | kcal/mol | 未定义/未取得 | 待合格完整端点 |
| rearranged_endpoint_DIFFERENT_PROCESS | 15.000000000 | 65.097316197 | 50.097316197 | kcal/mol | 未定义/未取得 | 不同过程，仅列账，不作方法误差 |
| qualified_intact_non_covalent_encounter_G | 未定义/未取得 | 4.731758211 | 未定义/未取得 | kcal/mol | 未定义/未取得 | 新独立相遇量；自己的热项和同几何SP；无作者等价标量 |
| source_capture_vs_non_covalent_encounter_FORMAL_NON_EQUIVALENT | 15 | 4.731758211 | -10.268241789 | kcal/mol | 未定义/未取得 | 差−10.268242仅形式列账，化学身份不等价，不作方法误差/容差判定 |
| reduction_products_minus_qualified_encounter_G | 未定义/未取得 | -10.002698682 | 未定义/未取得 | kcal/mol | 未定义/未取得 | 本计算中还原产物低于已测相遇态；不是共价捕获的相对能 |

### 当前科学问题coverage

- rule_transfer_connection：SUPPORTED_COMPONENT_REUSED；P–H断裂/CO2 C–H生成的反应模和双向局部连接、dication及formate各自最低点复用；有限IRC与分离优化端点分别标记。
- r3：WITHIN_ORIGINAL_SCALAR_WINDOW；当前自主题298.15K主值21.673991139 vs源21.8 kcal/mol，差−0.126008861，原±3内；作者/窄复现298K主对照21.669245637，差−0.130754363，温度分列。
- rule_reactivity_competition：PARTIAL_QUANTITATIVE_SUPPORT_CAPTURE_IDENTITY_UNRESOLVED；新增非共价相遇+4.731758，与还原产物−5.270940相差10.002699 kcal/mol，支持本已测相遇分支的还原热力学偏好；P位点共价捕获量仍非同一物种，不能声称重现SI+15或排除全部捕获。
- rule_evidence_validity：COMPONENT_SPECIFIC；新单点与自身合格Freq同几何、同库存/电子态；严格保留相遇、捕获、重排物种区分。
- rule_answer：PARTIAL_FINITE_REACTION_SUPPORTED；可达直接还原和产物命运有定量支持；新增相遇比较仍未完整解决中性P位点简单CO2捕获的竞争解释，无新增整题候选。

### 未完成项与恢复条件

- 完整中性P位点CO2捕获的身份受控有效结构/同级能量；若无稳定捕获，应有明确结构轨迹支撑，不能只用一次优化失败。

下一动作：先取得身份受控P共价CO2捕获端点/合理结构轨迹与参照，再做同作者层级优化、Freq及同几何高层；已有直接转移链不重算。无新源或数值证据，本轮无新增作业。

证据入口：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261020T0220Z/computation_feasibility.json；/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/original_group_04/current_native_review.json；/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/original_group_04/jobs.json。

完整原生与来源基线：

- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/reuse_inventory.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/returned_native_checks.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/author_comparison.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/original_group_04/narrow_221_native_reuse.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/original_group_04/narrow_221_native_status_and_connection.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/qualitative_followup_20261019T1200Z/verification_report.md

<!-- FOLLOWUP_20261020T0220Z_G04_END -->

<!-- QUALITATIVE_FOLLOWUP_20261019T1200Z_G04_BEGIN -->

## 2026-10-19 定性准则核收

核收UTC：2026-10-19T13:05:00.985024+00:00；模式：current_autonomous_research；科学状态：**INCOMPLETE**。当前自主整题已验证=false；不改变全局通过数、评分、容差或发布状态。

直接氢转移、适中能垒和放热产物得到有效计算支持；当前自主任务仍缺身份受控P位点捕获比较。形式数值差或非共价相遇不是所缺物种的替代。

新准则允许披露较大数值残差而暂定定性通过，但不放行失败必需计算、物种/作者模型冲突或缺失必要证据。

### 本轮核收与执行

本轮复用已有成功原生结果、当前任务包和来源核对；无重复提交。未闭合项分别列出缺失信息与数值诊断条件。

### 作者方法与实际计算

来源：正文PDF3–4 Fig3/Table2；SI PDF1–2方法、7 TableS6、19–20反应物/产物、65–66 TS2。

```json
{
  "status": "AUTHOR_PHYSICAL_METHOD_MATCH_FOR_VALID_DIRECT_PATH",
  "source_pages": "正文PDF3–4 Fig3/Table2；SI PDF1–2方法、7 TableS6、19–20反应物/产物、65–66 TS2。",
  "author_local_comparison": {
    "low": "wB97XD/6-31G(d,p),PCMMeCN",
    "high": "wB97XD/6-311++G(d,p),PCMMeCN,samegeometry",
    "temperature_K": 298,
    "pressure_atm": 1,
    "RRHO": "own frequencies, no additional rounding/1M shift",
    "state": "82atoms,+1singlet",
    "additional_comparison_temperature_K": 298.15,
    "temperature_note": "298K is the author/narrow-task primary value; 298.15K is a separately disclosed rethermalization, never presented as exact298K."
  },
  "source_method_manifest": {
    "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/author_method_manifest.json",
    "sha256": "a3d38127e63b5f690e1fd05c4dcb4b5dfd9b1bb1ea2016d0c0e5255e771fb202"
  },
  "software_and_numerical_disclosure": "原生Gaussian16；物理方法wB97XD两层基组/PCMMeCN一致。298K源核算与298.15K重热化分列。频率与单点各自实际route在narrow_221_native_reuse.json；IRC采用UltraFine/SCFTight/XQC并披露，不声称其为作者报告的默认值。",
  "complete_author_input_identity_confirmed": "validated_direct_path_only",
  "no_invented_author_parameters": true
}
```

### 量化对照

| 量 | 作者 | 本地 | 本地−作者 | 单位 | 原容差 | 判定/适用性 |
|---|---:|---:|---:|---|---|---|
| direct_transfer_activation_author_298K | 21.800000000 | 21.669245637 | -0.130754363 | kcal/mol | ±3 | Author298K primary; native rc0 opt/freq/SP and bidirectional local IRC evidence; reference computation, not blind-submission scoring. |
| direct_transfer_activation | 21.800000000 | 21.673991139 | -0.126008861 | kcal/mol | ±3 | 原窗口内；有效局部转移 |
| separated_products | -3.000000000 | -5.270940471 | -2.270940471 | kcal/mol | 未定义/未获得 | 方向支持；无新标定窗口 |
| intact_CO2_capture | 15.000000000 | 未定义/未获得 | 未定义/未获得 | kcal/mol | 未定义/未获得 | 待合格完整端点 |
| rearranged_endpoint_DIFFERENT_PROCESS | 15.000000000 | 65.097316197 | 50.097316197 | kcal/mol | 未定义/未获得 | 不同过程，仅列账，不作方法误差 |
| qualified_intact_non_covalent_encounter_G | 未定义/未获得 | 4.731758211 | 未定义/未获得 | kcal/mol | 未定义/未获得 | 新独立相遇量；自己的热项和同几何SP；无作者等价标量 |
| source_capture_vs_non_covalent_encounter_FORMAL_NON_EQUIVALENT | 15 | 4.731758211 | -10.268241789 | kcal/mol | 未定义/未获得 | 差−10.268242仅形式列账，化学身份不等价，不作方法误差/容差判定 |
| reduction_products_minus_qualified_encounter_G | 未定义/未获得 | -10.002698682 | 未定义/未获得 | kcal/mol | 未定义/未获得 | 本计算中还原产物低于已测相遇态；不是共价捕获的相对能 |

### 当前自主任务coverage

- rule_transfer_connection: SUPPORTED_COMPONENT_REUSED；P–H断裂/CO2 C–H生成的反应模和双向局部连接、dication及formate各自最低点复用；有限IRC与分离优化端点分别标记。
- r3: WITHIN_ORIGINAL_SCALAR_WINDOW；21.673991139 vs21.8 kcal/mol，Δ−0.126008861，原±3窗口内；298.15 K/1 atm/乙腈分离反应物参照。
- rule_reactivity_competition: PARTIAL_QUANTITATIVE_SUPPORT_CAPTURE_IDENTITY_UNRESOLVED；新增非共价相遇+4.731758，与还原产物−5.270940相差10.002699 kcal/mol，支持本已测相遇分支的还原热力学偏好；P位点共价捕获量仍非同一物种，不能声称重现SI+15或排除全部捕获。
- rule_evidence_validity: COMPONENT_SPECIFIC；新单点与自身合格Freq同几何、同库存/电子态；严格保留相遇、捕获、重排物种区分。
- rule_answer: PARTIAL_FINITE_REACTION_SUPPORTED；可达直接还原和产物命运有定量支持；新增相遇比较仍未完整解决中性P位点简单CO2捕获的竞争解释，无新增整题候选。

### 未完成项与恢复条件

- 完整中性P位点CO2捕获的身份受控有效结构/同级能量；若无稳定捕获，应有明确结构轨迹支撑，不能只用一次优化失败。

下一动作：取得来源定义P捕获端点，或有依据的保持完整CO2与P作用的候选及可重复结构路径；不能以一次优化失败证明不存在稳定捕获，也不盲重投旧重排种子。

298K作者/窄任务主值21.669245637；298.15K另行重热化21.673991139。8份原生日志returncode均0。IRC起点与合格TS同原子序RMSD0.000377973Å；高/低层R、CO2、TS同几何分别3.63e−7/0/2.45e−15Å。双向100点IRC支持局部P–H断裂/C–H形成，未声称已分离优化盆地。此来源指导的参考核算不冒称盲测solver提交或官方评分通过。

证据：

- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/reuse_inventory.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/returned_native_checks.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/author_comparison.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/original_group_04/narrow_221_native_reuse.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/original_group_04/narrow_221_native_status_and_connection.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/qualitative_followup_20261019T1200Z/coverage.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/qualitative_followup_20261019T1200Z/computation_feasibility.json
- /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/original_group_04/scope_specific_candidate_review.json

<!-- QUALITATIVE_FOLLOWUP_20261019T1200Z_G04_END -->

<!-- STORAGE_RECOVERY_20261019T0530Z_G04 -->

最新核收：2026-10-19T05:52:47.408464+00:00；PARTIAL_FINITE_REDUCTION_SUPPORTED。current_scope_verified=false；本轮无新增整题候选。

复用已合格转移路径、端点和自身热项；21.673991139 kcal/mol势垒落在作者21.8±3范围。非共价相遇+4.731758不是SI Table S6的+15共价P捕获物种，本轮没有新身份受控坐标或新可执行修复。

当前活动：无。本轮新提交：无。准备未提交：无。

作者/本地/差与既有容差：势垒作者21.8/本地21.673991139/差−0.126008861 kcal/mol，在原±3窗口内；分离产物−3/−5.270940471/差−2.270940471，无新增容差。非共价相遇+4.731758与源共价捕获+15不同物种，形式差−10.268242不是方法误差。

当前逐题覆盖：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/coverage.json；逐点作者/计算/差/原容差：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/author_comparison.json；运行台账及最新迁移ID：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/storage_recovery_20261019T0530Z/jobs.json。

未完成及恢复条件：中性P位点共价CO2捕获的结构/量身份尚未闭合；SI physical7 TableS6的完整捕获坐标/输入，或具有结构和端点证据的独立捕获模型；现有相遇不是同一量。；新原作者证据，或新的有理据身份受控几何；不无变化重投。

以下均为带日期的历史记录；其中旧活动状态已被上述最新回执取代，不能据旧ID重复提交。

<!-- END_STORAGE_RECOVERY_20261019T0530Z_G04 -->

<!-- VERIFICATION_FOLLOWUP_20261019T0035Z_G04 -->
最新验证：2026-10-19T02:04:49.444734+00:00；PARTIAL_FINITE_REDUCTION_SUPPORTED。current_scope_verified=false；本轮无新增整题候选。

复用有效P–H/CO2转移局部双向连接、端点和势垒21.673991139 kcal/mol。完整非共价相遇+4.731758已具自身热项和同几何高层，P16–C80=5.140825 Å；它不能替代SI TableS6的+15共价P捕获物种。本轮无新返回或有据捕获几何，不重复已成功阶段。

当前活动：无。本轮新提交：无。准备但未提交：无。

作者/本地/差与既有容差：势垒作者21.8/本地21.673991139/差−0.126008861 kcal/mol，在原±3窗口内；分离产物−3/−5.270940471/差−2.270940471，无新增容差。非共价相遇+4.731758与源共价捕获+15不同物种，形式差−10.268242不是方法误差。

逐点对照见 /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261019T0035Z/author_comparison.json。输入、状态、热项适用范围不变。
未完成及恢复条件：中性P位点共价CO2捕获的结构/量身份尚未闭合；SI physical7 TableS6的完整捕获坐标/输入，或具有结构和端点证据的独立捕获模型；现有相遇不是同一量。；新原作者证据，或新的有理据身份受控几何；不无变化重投。

[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261019T0035Z/verification_report.md)；[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261019T0035Z/coverage.json)；[jobs](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261019T0035Z/jobs.json)；[后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261019T0035Z/successor.json)。历史段落保留为当时快照，以本段为当前状态，不把正常标记/排队当科学通过。
<!-- /VERIFICATION_FOLLOWUP_20261019T0035Z_G04 -->

<!-- VERIFICATION_FOLLOWUP_20261018T0200Z_G04 -->
最新验证：2026-10-18T03:21:17.143165+00:00；FINITE_COLLECTION_COMPLETE_NO_ACTIVE_JOB / ENCOUNTER_FREE_ENERGY_COMPLETE_COVALENT_CAPTURE_COMPARISON_UNRESOLVED。current_scope_verified=false；本轮无新增整题PASS候选。

相遇最低点同几何高层单点已原生完成：rc0，1次正常，无错误，965.56秒。自身240个正频与同几何RMSD 1.34e−15 Å复用；Gcorr=0.617658 Eh，298.15 K/1 atm/PCM乙腈。ΔG相遇=+4.731758 kcal/mol，分离还原产物−5.270940 kcal/mol比此相遇态低10.002699 kcal/mol。该结构P16–CO2C80=5.140825 Å，属于非共价相遇；不能把它改称作者+15共价P位点捕获端点。

作者/本地/差与既有容差：势垒作者21.8、本地21.673991139、Δ−0.126008861 kcal/mol，原±3通过；分离产物作者−3、本地−5.270940471、Δ−2.270940471，无新容差；新相遇+4.731758与作者+15形式差−10.268242，身份不等价，不能当方法误差。

当前活动：已知相遇分支的全部必需阶段已完成。精确中性P捕获身份仍未闭合，本轮没有新的有据几何/数值修复；不以旧失败次数证明不可计算。。排队、单个正常标记和平台SUCCEEDED均不代表完整科学通过。

未完成与恢复条件：现合格相遇与作者中性P位点共价捕获并非同一化学量。缺口是相关捕获分支的定量/结构证据，不是必须复现整篇论文或精确匹配未标定+15。 最小缺项：保持2a完整图的中性P–CO2捕获态或其他有依据的有限竞争判别；匹配的作者输入/坐标可解除精确追溯歧义（SI physical7 TableS6/8）。。

本轮已提交0项；计算窗口：本轮已完成；无新作业。下一捕获分支未定义，不能给可信计算截止时间。 验收窗口：现有分量核收已完成；完整捕获证据到齐后约0.5–1小时复核。

[报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261018T0200Z/verification_report.md)；[逐项coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261018T0200Z/coverage.json)；[数值比较](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261018T0200Z/author_comparison.json)；[可计算性](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261018T0200Z/computation_feasibility.json)；[真实jobs及未投输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261018T0200Z/jobs.json)；[后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261018T0200Z/successor.json)。历史段落是当时快照，以本段新结果为准；不覆盖新增范围，不改评分/任务/资格。
<!-- /VERIFICATION_FOLLOWUP_20261018T0200Z_G04 -->

<!-- ADVANCE_FEASIBLE_20261017T1145Z_G04 -->
最新验证：2026-10-17T12:21:53.863534+00:00；ACTIONABLE_COMPUTE / ENCOUNTER_MINIMUM_QUALIFIED_SAME_GEOMETRY_SP_PENDING。current_scope_verified=false；本轮无新增整题PASS。

返回Opt/Freq rc0、2次正常、240个正频（最低24.9821cm−1），原force/displacement门槛通过；82原子/+1单重态及完整2a键图保持。P16–CO2C80=5.140824609Å，CO2近线性，确认为非共价相遇最低点。其自身298.15K/1atm Gcorr=0.617658Eh。已提交作者同级同几何高层SP，仅量化这一相遇过程；不将其标签换成SI+15捕获端点。

作者/本地/差与既有容差：H转移势垒21.673991139 vs21.8 kcal/mol，Δ−0.126008861，原±3内；分离产物−5.270940471 vs−3，Δ−2.270940471，无新增容差。完整2a捕获+15仍无可比局部值；旧重排+65.097316197为不同过程，不作误差拟合。

当前活动：hpc-job-88ec0188-d216-4d38-8a61-c864d0b7c388 RUNNING。排队/运行与平台成功均不等于科学通过。

未完成：新合格最低点是非共价相遇结构；同几何高层与合成自由能尚未返回。 最小缺项：新SP原生正常、同几何/状态检查及既有分离反应物参照。 SI给捕获+15，但匹配端点坐标/输入未发现。 最小缺项：SI物理7TableS6/8说明对应的完整2a–CO2作者坐标或输入；全SI结构标题及87–88重复块已查。

计算与验收时间分开记录于[eta.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance_feasible_20261017T1145Z/eta.json)；整题PASS时间未定。

[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance_feasible_20261017T1145Z/verification_report.md)；[逐项覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance_feasible_20261017T1145Z/coverage.json)；[可计算性](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance_feasible_20261017T1145Z/computation_feasibility.json)；[后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance_feasible_20261017T1145Z/successor.json)。历史状态只适用于原范围，不覆盖本段最新结论。
<!-- END_ADVANCE_FEASIBLE_20261017T1145Z_G04 -->

<!-- VERIFICATION_FOLLOWUP_20261017_ORIGINAL_GROUP_04 -->
最新验证：2026-10-17T08:46:42.256055+00:00；CAPTURE_IDENTITY_UNRESOLVED_ADAPTIVE_TRUST_SUBMITTED。current_scope_verified=false；无新增整题PASS。

已核收32步真实曲率恢复：returncode1、L9999、0正常终止、0频率。2a键图保持，P16–C80从5.106470到5.138099 Å，仍是远离共价捕获的分支。末最大力5.41446e-4 Eh/bohr（阈值4.5e-4），最大位移0.008809（阈值0.0018）未过。末段能量下降与力积分吻合；重复线搜索受固定0.02bohr信赖半径限制。已从真实frame32提交新Hessian+自适应信赖半径恢复，仍32步，未改作者方法/阈值。

既有作者/本地/差与原容差：H转移势垒21.673991139 vs21.8 kcal/mol，Δ−0.126008861，原±3内；分离产物−5.270940471 vs−3，Δ−2.270940471，无新增容差。完整2a捕获+15仍无可比局部值；旧重排+65.097316197为不同过程，不作误差拟合。

本轮新作业与首查：hpc-job-3847f27a-d5d2-4c76-b36c-4fc1851c4bb6=QUEUEING, native_started_at_first_check=False。活动/排队不等于原生成功。

未完成项：当前分支没有合格捕获最低点；32步L9999不是无捕获势阱的证明。 最小信息：自适应信赖恢复的原阈值收敛、240频率及完整端点图。 SI给捕获+15，但匹配端点坐标/输入未发现。 最小信息：SI物理7TableS6/8说明对应的完整2a–CO2作者坐标或输入；全SI结构标题及87–88重复块已查。

[本轮原生与报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261017/verification_report.md)；[逐点评分覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261017/coverage.json)；[可计算性](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261017/computation_feasibility.json)；[失败与后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/verification_followup_20261017/successor.json)。以下历史结论仅适用于其当时范围；旧PASS或暂停文字不覆盖本段当前范围。
<!-- END_VERIFICATION_FOLLOWUP_20261017_ORIGINAL_GROUP_04 -->

<!-- RESTORE_FEASIBLE_20261015_ORIGINAL_GROUP_04 -->
最新验证更新：2026-10-15T20:00:01.067976+00:00。CAPTURE_VALID_QUEUE_PRESERVED；current_scope_verified=false，无新增整题PASS。旧暂停及篇数限制已撤销。

捕获SCF48真实曲率恢复 hpc-job-2a063471-8cb7-48c3-9bec-bae45c250b84仍有效排队，未被误撤回、未重投或改配。已核其尚无running/receipt/原生日志。本轮复用上轮48步失败的结构/力诊断与原作者输入；等待真实Hessian和原阈值下的优化/频率，不把排队当结果。

既有数值与差保留：H转移势垒21.673991139 vs21.8 kcal/mol，Δ−0.126008861，原±3内；分离产物−5.270940471 vs−3，Δ−2.270940471，无新增容差。完整2a捕获+15仍无可比局部值；旧重排+65.097316197为不同过程，不作误差拟合。

本轮首次回读（2026-10-15T19:56:30.167104+00:00）：hpc-job-2a063471-8cb7-48c3-9bec-bae45c250b84=QUEUEING, native_started=False。管理误撤回不属于原生失败；复用原目录的恢复结果归新ID。未返回阶段不算成功。

未完成/条件：当前完整2a+CO2分支未到驻点，CO2正远离P；无法列作者+15捕获G。 最小缺项：新真实Hessian、优化轨迹、各自完整240频率和端点图。 SI给捕获+15，但匹配端点坐标/输入未发现。 最小缺项：SI物理7TableS6/8说明对应的完整2a–CO2作者坐标或输入；全SI结构标题及87–88重复块已查。

[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/restore_feasible_20261015/verification_report.md)；[可计算性](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/restore_feasible_20261015/computation_feasibility.json)；[数值与原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/restore_feasible_20261015/numerical_comparison.json)；[恢复/失败后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/restore_feasible_20261015/successor.json)；[首查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/restore_feasible_20261015/first_native_checks.json)；[恢复旧新ID收据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/restore_feasible_20261015/original_group_04/restore_receipts.json)。只更新reference/manifest并验包；未改题面、评分、输入、qualification或专家包，不移动/删除/发布。以下历史状态只适用于其当时范围，任何旧暂停文字被本段当前授权说明覆盖。
<!-- END_RESTORE_FEASIBLE_20261015_ORIGINAL_GROUP_04 -->

<!-- JOB_FOLLOWUP_20261015T181800Z_ORIGINAL_GROUP_04 -->
最新验证：2026-10-15T18:40:50.343442+00:00。CAPTURE_OPT_INCOMPLETE_FRESH_CURVATURE_RECOVERY_QUEUED。current_scope_verified=false；无新增整题PASS或全局通过数。

捕获优化48步后L9999、returncode1，0正常终止/0完整频率，高层正确跳过。48个已评估结构均保留完整2a框架；P16–CO2C由4.400000增至5.106470 Å，末点最大力0.002000137 Eh/bohr，未收敛。这证明该接近分支在远离，不证明无捕获最低点。能量变化与力积分近似一致；新提交末次已评估SCF48的真实曲率恢复，Cartesian/CalcFC/NoTrustUpdate/MaxStep2/MaxCycles32，保持作者方法和阈值。

H转移势垒21.673991139 vs21.8 kcal/mol，Δ−0.126008861，原±3内；分离产物−5.270940471 vs−3，Δ−2.270940471，无新增容差。完整2a捕获+15仍无可比局部值；旧重排+65.097316197为不同过程，不作误差拟合。

新作业：hpc-job-2a063471-8cb7-48c3-9bec-bae45c250b84。首次回读（2026-10-15T18:36:28.849277+00:00）：hpc-job-2a063471-8cb7-48c3-9bec-bae45c250b84 QUEUEING / native_started=False。未返回的阶段不算原生成功；包校验不等于科学通过。

未完成项与恢复条件：当前完整2a+CO2分支未到驻点，CO2正远离P；无法列作者+15捕获G。 新真实Hessian、优化轨迹、各自完整240频率和端点图； SI给捕获+15，但匹配端点坐标/输入未发现。 SI物理7TableS6/8说明对应的完整2a–CO2作者坐标或输入；全SI结构标题及87–88重复块已查；

[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/job_followup_20261015T181800Z/verification_report.md)；[逐点对照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/job_followup_20261015T181800Z/numerical_comparison.json)；[范围覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/job_followup_20261015T181800Z/coverage.json)；[可计算性](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/job_followup_20261015T181800Z/computation_feasibility.json)；[作业/后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/job_followup_20261015T181800Z/successor.json)；[原生首查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/job_followup_20261015T181800Z/first_native_checks.json)。只改reference/manifest，不改题面/评分/输入/qualification，不移包或发布。以下历史状态限于其当时范围，不能覆盖本轮未完成项。
<!-- END_JOB_FOLLOWUP_20261015T181800Z_ORIGINAL_GROUP_04 -->

<!-- ADVANCE16_20261015T073100Z_ORIGINAL_GROUP_04 -->
最新验证接续：2026-10-15T07:48:54.169280+00:00

原来因存储延期的完整2a孤对电子半球CO2接近模型已实际提交。本轮输入与已准备的82原子/+1单重态结构、wB97XD基组层级、PCM乙腈及298.15 K/1 atm定义逐字一致。仅新增高层依赖的结构屏障：低层正常完成、240正频后还须保持79原子2a框架且无非预期共价交叉接触；这是排除重排的图检查，不是新能量/评分容差。原H转移21.673991对21.8±3、分离产品−5.270940对−3保留；旧+65.097316端点仍是不同重排过程，不能冒充作者+15捕获值。

本轮实际新增作业：hpc-job-fd9d8c9d-e80e-49ec-adf8-e339365c0c3e。末查活动作业：hpc-job-fd9d8c9d-e80e-49ec-adf8-e339365c0c3e。存储延期已解除；不沿用旧阻碍停止。本轮尚未增加合格科学标量或整题PASS，current_scope_verified=false。

未完成项：

- 新捕获分支尚未返回合格最低点和同几何高层，因此作者+15捕获参照仍缺同过程量。
- 原文未定位到TableS6捕获端点的作者坐标；当前是物理方法明确、有结构依据的独立接近构型。

下一行动：

- 收取现有捕获作业逐阶段输出；低层Opt/Freq须核原阈值、240模式、状态/原子库存和完整2a框架，再核同几何高层及自身热项。
- 按Ghigh+自身低层热修正−G2a−GCO2、298.15K/1atm/MeCN对照作者+15；若解离或重排，记录物理结果，不重新标记为捕获或盲增步。

[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance16_20261015T073100Z/verification_report.md)；[原生首查与计时](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance16_20261015T073100Z/first_native_checks.json)；[逐点原作者数值/本地差异/原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance16_20261015T073100Z/numerical_comparison.json)；[可计算性审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance16_20261015T073100Z/computation_feasibility.json)；[后继映射](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/advance16_20261015T073100Z/successor.json)。

提交接受、原生程序完成、科学通过分别记录。正式题面/输入/评分/容差/qualification未改；以下旧记录只适用其时间点，旧局部PASS不覆盖当前新增范围。
<!-- END_ADVANCE16_20261015T073100Z_ORIGINAL_GROUP_04 -->

<!-- PARALLEL_ADVANCE_20261015T052600Z_ORIGINAL_GROUP_04 -->
本轮独立验证更新：2026-10-15T06:24:55.580520+00:00

状态：INTACT_CAPTURE_APPROACH_PREPARED_STORAGE_DEFERRED。current_scope_verified=false，scientific_pass_candidate=false；没有新增整题PASS。包格式校验通过不表示科学验证通过。

复核旧捕获作业为正常完成的重排端点：三段 normal、240正频、同几何高层和自身热项齐全，但 P16–N17=2.769089 Å 断裂且 N17–O81=1.424015 Å 形成。+65.097316 kcal/mol 不属于作者 +15.0 的完整2a捕获过程。本轮重读 SI7–8/TableS6、全SI结构标题，排除隐含捕获坐标；从完整2a合格几何构建4.4 Å、倾斜30°且避开N–O接触的新CO2接近方向。输入与两阶段门控已准备，尚未获集体存储准入。

本轮新增作业：无。末查活动作业：无。

尚未完成与来源边界：

- 完整2a捕获分支尚未形成合格可比较结果。
- 新构型已有可执行方法和输入；所需1.3 GiB共享输出预留未获准入。

下一执行：

- 执行已经准备的Capture_intact2a_lonepair_approach；原图/电荷/自旋、240正频、低高层同几何及298.15 K/1 atm参照全部通过后，才列捕获自由能。
- 若新端点解离或重排，如实判定；不延长旧重排端点、不强行赋作者+15数值。

没有活动作业的具体原因：此前作业已返回；其量化结果是重排结构。新的不同接近方向已经准备，但集体存储门控未通过，因此尚无新ID。

本轮证据：

- [完整逐篇报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/verification_report.md)
- [逐项作者值、本地值、差与原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/numerical_comparison.json)
- [原生日志复用与哈希](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/reuse_inventory.json)
- [逐Link返回核查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/returned_job_reviews.json)
- [当前规则覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/coverage.json)
- [可计算性审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/computation_feasibility.json)
- [失败至后继及未提交输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/parallel_advance_20261015T052600Z/successor.json)

原任务、输入、评分、科学容差及qualification未修改。旧段落完整保留为历史证据，任何旧PASS只适用于当时已验证组件，不覆盖当前新增范围。
<!-- END_PARALLEL_ADVANCE_20261015T052600Z_ORIGINAL_GROUP_04 -->

<!-- LANE_A_04_20261015T014600Z_FINITE_RETURN -->
有限返回核收，2026-10-15

12步恢复完成Opt/Freq/highSP：82原子+1singlet、240正频、三段normal、同几何复合G。但全图核查发现P16–N17=2.769089Å断裂，N17–O81=1.424015Å形成，当前为重排N–O/P–C端点。相对完整2a+CO2的+65.097316kcal不是作者单纯捕获+15的同过程值；差+50.097316仅列账，不作方法误差。ΔE+54.261542、热修正+10.835774；来源参照/hash/高低层几何核对一致。追溯最早constrained60轨迹SCF37已出现该变化，此后恢复沿同一重排盆地。既有H转移21.673991对21.8±3、分离产品−5.270940对−3保留。

当前科学问题仍有未闭合结果，current_scope_verified=false；原容差与源定义保留，release_ready=false。

必要科学边界：

- 完整2a中性P捕获分支仍未合格，不能用重排产物替代源+15结合结果。
- 旧P–C/CO几何screen不足以认证完整分子身份；所有旧轨迹和成本保留。

后继与预算：

- 复用有效转移与产物；下一捕获候选须从完整源2a构图、避开N17–O接触并明确不同CO2接近方向，不能延长当前重排端点优化。
- 本轮不盲投新capture；需先完成新的化学身份/空间方向依据与集体存储准入。

新增作业：无。本次末查活动作业：无。

证据与比较：

- [capture_returned_native_and_binding_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261015T014600Z/capture_returned_native_and_binding_audit.json)，sha256 7c091cf8a2071704df27a63a9a9dbbf7ee41c361b8a06b9a6597ca6de0bd3b51
- [capture_connectivity_trajectory_diagnosis.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261015T014600Z/capture_connectivity_trajectory_diagnosis.json)，sha256 d359a5d128358f6724b2752ebef5c143c0e987da4ee691a2397bec137982e7ab

[逐项数值、作者参照与保留原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261015T014600Z/current_round_numerical_comparison.json)；[完整当前报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261015T014600Z/current_round_verification_report.md)；[返回作业/累计成本来源](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261015T014600Z/returned_jobs.json)。

以下历史段落完整保留，只适用其记录时点。
<!-- END_LANE_A_04_20261015T014600Z_FINITE_RETURN -->

<!-- LANE_A_04_20261014T143300Z_VERIFIED_INTAKE -->
paper_221aafe4bd916a11 — 当前公开问题核收记录，2026-10-14

**current_scope_verified=false；本轮没有整题PASS。** 以下内容为当前状态；后附旧段落仅保留其当时含义。

内部坐标40步恢复真实失败（不是平台成功即驻点）。SCF36最大笛卡尔梯度4.783×10−6 Eh/bohr，P16–C80=1.891603Å，但原内部预测位移仍0.005675>0.0018，故未合格。后续内部外推失稳据以提交精确SCF36几何的Cartesian/NoLinear/NoTrustUpdate/MaxStep1/CalcFC，最多12新步、总6h；旧690步保留。

当前缺口：

- capture仍缺合格最低点、240正频及同几何高层，作者+15结合G保持null。
- 小笛卡尔梯度并不替代原四项驻点要求；高层仅经原阈值/频率/连接门控后执行。

下一步：

- 收取4a983b11这一次12步恢复；核82原子+1单重态、P–C和CO连接、原站点条件、240频率及自身高层组合。
- 若失败，保留新轨迹和全部历史成本，从实际曲率/坐标诊断选择下一步，不自动延长。

已提交且首查的新增ID：hpc-job-4a983b11-768a-4b8a-9b2c-b546a92458a8。

活动ID（2026-10-14T16:49:30.550217+00:00）：hpc-job-4a983b11-768a-4b8a-9b2c-b546a92458a8。

[本轮完整报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T143300Z/current_round_verification_report.md)；[逐项数值/原容差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T143300Z/current_round_numerical_comparison.json)；[原生/执行器回执](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T143300Z/current_round_native_observation.json)。

- [capture_internal40_returned_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T143300Z/capture_internal40_returned_audit.json)；SHA256 `00a38c566bb3bdd2a1587c51a27d68012e16c000af1ceacc2056a97c7bee595d`。

公开任务、输入、评分与容差保持原字节；历史失败成本保留，不以平台SUCCEEDED或诊断频率宣布驻点。
<!-- END_LANE_A_04_20261014T143300Z_VERIFIED_INTAKE -->

<!-- ORIGINAL_GROUP_A_CONTINUATION_20261014T020500Z -->
# paper_221aafe4bd916a11 捕获计算原生失败后的有限续接

2026-10-14T06:30:41.975913+00:00；状态 `CAPTURE_STEP_LIMIT_DIAGNOSED_FIXED_TRUST_INTERNAL_RECOVERY_PENDING`；整题 `current_scope_verified=false`。

capture自由Cartesian作业85cf53a4原生rc1，60步耗尽，Freq/高层均未开始；末最大力0.001354775>0.000450、最大位移0.063313>0.001800，未合格。CHK确认当前就是已评估step60，P16-C80=1.8853195 Å、CO=1.343271/1.212631 Å。残余力主要为甲基运动，旧动态信赖半径从0.02扩至1.35，近20步6次上坡；据此仅提交一次40步冗余内坐标/NoTrustUpdate固定0.05/CalcFC+Recalc5恢复，hpc-job-92207032-4889-46c5-ba24-e05b9d7746f7，首查QUEUEING/NOT_STARTED。旧650步保留；仅低层最低点及240正频率合格后才算作者高层。

父作业 `hpc-job-85cf53a4-7d72-4587-94ca-58e4ce1a9cd4` 的真实原生日志在2026-10-14 05:53:09以l9999/NSTEP60超限退出，runner rc1。平台SUCCEEDED不等于应用成功；其全部实例现已Deleted。没有SCF发散、输入语法或运行时间超时；60个已评估几何中没有驻点，Freq与高层均未执行。

最后E=−2325.282105722859 Eh；最大/RMS Cartesian梯度0.00135477529/0.0002169118115 Eh/bohr，对原阈值0.000450/0.000300；最大/RMS位移0.063313/0.022619对0.001800/0.001200，仅RMS力满足。历史60步中最低最大力在step15为0.000784132，也不满足；最后点是本次最低电子能，不是合格最低点。

82原子C27H43N8O2P2+、+1singlet保持。CHK最后几何/梯度与保存的第60个已评估点逐项一致，与日志坐标最大差4.97e−7 Å。P16-C80=1.8853195 Å，CO2两键1.343271/1.212631 Å，重原子键图从释放首点未变。最大残余梯度位于C36甲基H46/H53，P16及CO2仅占总梯度平方0.145757%，支持外围构象松弛造成当前数值困难。

Opt=Cartesian的246变量明确按X1/Y1/Z1…排列；FCHK InternalForces与负CartesianGradient逐项相同，30381个下三角元素对应246×246优化矩阵。它来自SCF56几何的解析Hessian，经过57–60步更新；末端“compute analytic Hessian”只是请求，随后l202/l601/l9999退出，没有新解析Hessian。原矩阵最低值−0.000325366；用真实原子质量剔除6个平转方向后有2个负近似曲率（−7.570823e−5、−1.414665e−6）。这些只用于失败诊断，绝不称已计算虚频或驻点性质。

旧MaxStep2只设置初始信赖半径0.02，日志显示动态半径最大1.35、末值0.404；近20步6次上坡，最大已执行原子位移0.211109 Å，净能量仍下降0.343927 kcal/mol。因此本次采用不同策略：从已评估step60及原轨道出发，完全无约束的冗余内坐标、Opt=(CalcFC,RecalcFC=5,NoTrustUpdate,MaxStep=5,MaxCycles=40)，固定半径0.05；作者wB97XD/6-31G(d,p)、PCM乙腈、默认积分格和原收敛阈值不变。NoTrustUpdate的含义已核对[Gaussian官方Opt文档](https://gaussian.com/opt/)，保存的原页见[数值设置来源](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/original_group_A/capture_returned/gaussian_opt.html)。

新作业 `hpc-job-92207032-4889-46c5-ba24-e05b9d7746f7`：20CPU/100GiB、CPU资源-2、单节点、HIGH6、指定项目全部回读匹配；双锁内核70个全账户活动作业与98份跨旧/新根目录原生日志，无同捕获活动目标或已合格捕获最低点重复。首次检查2026-10-14T06:27:22.475928+00:00为QUEUEING/NOT_STARTED，未宣称应用成功。

runner把低层Opt/Freq与高层分开执行：先需两个正常结束、原生优化接受及原力阈值、82原子+1singlet、240个正频率；门控通过后才启动同几何wB97XD/6-311++G(d,p) PCM乙腈单点。整个作业12h、最多40新增Opt步，无自动重试或后续调度。最后科学收取仍须审反应身份、原始热项和同层参照。

累计账本保留旧PCfirst300+200、TRIC30、约束60、本次自由60，共650个已知几何/梯度评估；新40全部耗用时累计上限690。所有旧Hessian/SCF原始成本也保留。父作业CPU650385.5 s、elapsed33225.0 s、wrapper33302.5640 s。新组件尚未启动，不能预记完成成本。

CHK源哈希 `799891ee99f13780a6a12c04fcd5ac4b3a52db56fe3021853851f8168cf10d89` 在副本转换前后相同；formchk仅改变副本，原文件只读。转换FCHK哈希 `8adff8984228facc2532c5c16993c0623f131eb09b6f1dd6e49b724d61242844`，完整副本/工具哈希和时间见[转换审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T020500Z/capture_checkpoint_conversion_audit.json)。没有登录节点量子化学求解。

|量/事件|论文值|本地值|差值|可比性；单位kcal/mol|
|---|---:|---:|---:|---|
|activation_29815K_1atm|21.800000|21.673991|-0.126009|valid local transfer; not complete competition|
|separated_products|-3.000000|-5.270940|-2.270940|Physically balanced dication+formate; exergonic direction supported, raw2.27kcal discrepancy not calibrated away|
|binding|15.000000|待合格计算|—|QUALIFIED_CAPTURE_MINIMUM_AND_COMPOSITE_G_STILL_PENDING|

捕获最低点仍未认证，作者+15 kcal/mol结合量保持null；已有效局部转移21.673991对21.8及分离产品−5.270940对−3.0的−2.270940差完整保留，尚不构成整题竞争验证。

准确作者捕获构象仍未获得，重建中性P16结合模型可执行但不冒称源原始坐标。结合G需合格最低点的同几何高层电子能加298.15K/1atm谐振热项，再减已有分离2a和CO2；不加入1M或Grimme修正，不扩大容差，不用未收敛电子点估出+15。

[轨迹/曲率诊断](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T020500Z/capture_trajectory_and_curvature_audit.json) · [执行与累计增补](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T020500Z/capture_method_execution_addendum.json) · [作业/资源](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T020500Z/jobs.json) · [首次检查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T020500Z/capture_successor_first_check.json) · [数值对照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261014T020500Z/quantitative_comparison.json)。本事件只处理221a；旧版文档保存在[更新前记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261014T020500Z/original_group_A/capture_returned/before)。完成首查后退出，不等待长作业、不自动恢复。

<!-- END_ORIGINAL_GROUP_A_CONTINUATION_20261014T020500Z -->

# 最新验证接续：2026-10-14T02:24:34.536069+00:00

**当前整题未通过：NUMERICAL_RECOVERY_IN_PROGRESS。** 本次逐篇证据：[attempt_20261013T195300Z_execution_20261014T020335Z](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T195300Z_execution_20261014T020335Z/verification_report.md)。

既有82原子+1/1捕获释放作业仍在RUNNING，已亲读36个SCF；P16-C80=1.885430 Å、P11-H79=1.404709 Å、CO2两键1.342798/1.213067 Å，弯曲捕获构型在下降但尚未达完整优化/频率/高层。不存在已完成结合最低点，不能填+15.0。本执行不重复该作业。

|量/参照|作者|本地|差|单位|原容差|判定|
|---|---:|---:|---:|---|---:|---|
|direct_transfer|21.8|21.673991|-0.126009|kcal/mol|3|VALID_EXISTING_COMPONENT|
|separated_products|-3|-5.27094|-2.27094|kcal/mol|未得到|CONDITIONAL_COMPONENT|
|CO2_capture_binding|15|未得到|未得到|kcal/mol|未得到|ACTIVE_OPT_FREQ_SP_PENDING|

未完成/差异：捕获模型首次完全自由释放还在求解，240正模及同几何高层未齐；源精确捕获坐标缺失已明示，但Hamiltonian/库存/态足以执行当前模型。

新提交：无；复用既有活动或有效计算。当前活动：hpc-job-85cf53a4-7d72-4587-94ca-58e4ce1a9cd4。

下一步：收现作业全部3段；先核240正模/库存/成键，完成后才按同层2a+CO2与低层热项计算结合自由能。；若解离或失败，以新的实际轨迹/曲率诊断；不得把受约束种子当+15结合最低点。

当前题面/输入/评分/窗口保持原批准版本，平台成功不等于应用或科学成功。以下历史验证记录原文保留，旧PASS不覆盖当前新增范围。

---

<!-- ORIGINAL_GROUP_A_CONTINUATION_20261013T195300Z -->
# paper_221aafe4bd916a11 本轮验证

UTC 2026-10-13T20:44:44.767352+00:00；continuation_20261013T195300Z；科学状态 **NUMERICAL_RECOVERY_IN_PROGRESS**；`current_scope_verified=false`。

捕获旧作业只运行首段受约束预优化，60次SCF后L9999/exit1；释放、频率及高层从未执行。最低最大力在真实step56为0.001006，仍超0.000450，位移0.058771也超0.001800。已取该完整82原子+1单态、弯CO2/P16捕获构型首次完全解除约束，改Cartesian并新算/每5步更新Hessian，MaxStep2、最多60步，后接Freq及作者高层。

## 作者方法与可比性

{
  "software": "Gaussian16",
  "geometry_frequency": "wB97XD/6-31G(d,p), author default grid/SCF",
  "high_level": "wB97XD/6-311++G(d,p) on identical low geometry",
  "solvent": "PCM acetonitrile",
  "thermal": "Source298K/task298.15K harmonicG,1atm; noGrimme correction or1M conversion",
  "state": "2a79atom+1singlet; CO2 adduct82atom+1singlet; products bisphosphine dication plus formateanion total+1",
  "reference": "Ghigh-composite capture or products minus separated2a/CO2; author binding+15 and products−3 no newly calibrated windows"
}

## 逐量对照

所有差值完整保留，未拟合零点或改变容差；下表除4cb为kJ/mol外均为kcal/mol。

|量|作者|本地|本地−作者|绝对差|原数值窗口|资格/结论|
|---|---:|---:|---:|---:|---|---|
|activation_29815K_1atm|21.800000|21.673991|-0.126009|0.126009|±3.000000|valid local transfer; not complete competition|
|separated_products|-3.000000|-5.270940|-2.270940|2.270940|未校准|Physically balanced dication+formate; exergonic direction supported, raw2.27kcal discrepancy not calibrated away|
|binding|15.000000|未获得|未获得|未获得|未校准|NUMERICAL_RECOVERY_IN_PROGRESS|

结论影响：直接转移势垒及分离产物放能方向保持；与简单捕获竞争的定量结论因缺自由捕获最低点仍未验证。

## 新作业及首次执行检查

|case|job ID|平台|应用|已核资源|
|---|---|---|---|---|
|capture_step56_first_free_Cartesian_release|hpc-job-85cf53a4-7d72-4587-94ca-58e4ce1a9cd4|RUNNING|running|True|

完整原始退出码、每阶段终止、频率/自旋、项目/计算区/优先级/规格/入口、起止释放时间及实例状态见 [jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T195300Z/jobs.json)。实际首次日志检查见每个新case的 `latest_execution_check.json`。没有原生日志的排队作业只登记排队事实。

## 来源与尚余工作

SI TableS6明确2a CO2结合+15.0；正文Table2产品−3.0及21.8势垒。官方页面/公开索引未增加源捕获坐标，Crossref有has-review而无update-to。

准确作者捕获构型/原始输出尚未获取；未发现补充Grimme要求，不能虚构准谐阻塞。

尚无自由捕获最低点，+15.0结合值不可填；如果自由释放解离，应如实认定该起始构型未找到捕获盆地，不用受约束结构充当金标。源精确捕获坐标未取得，但当前模型/方法可计算。

1. 收新释放的Opt/Freq/SP三段正常结束、82原子+1/1及240正频率；亲核P16-C80、CO2弯曲及原子库存。
2. 按既有2a、CO2高层加低层热项建立同物理定义参照；直接势垒21.673991和分离产物−5.270940继续复用。
3. 新失败须用本次实际曲率/梯度诊断；不把旧60步或历史500步作为可无限增长的预算。

[完整本轮覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T195300Z/coverage.json)；[逐量机器可读证据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T195300Z/quantitative_comparison.json)；[原始失败与曲率诊断](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T195300Z/failure_and_mode_diagnostics.json)。

只补验证reference/manifest并验包；未改题面、输入、评分或范围；未发布、移动、删除；未停止任何HPC；无委派或定时恢复。

---
以下保留历史阶段记录，当前状态以上方本轮证据为准。

# 本轮验证更新：2026-10-13T15:40:02.414594+00:00

轮次：continuation_20261013T094000Z；状态：**NUMERICAL_RECOVERY_IN_PROGRESS**；整题 current_scope_verified=false。

旧TRIC末构型CO2近线性，C-O1.16456/1.16451Å，P11-C80=5.36645、P16-C80=4.69493Å，不能当成捕获最低点。新82原子+1单态从合格2a的中性P16重建弯CO2种子（P-C2.05Å，C-O1.24Å，130°），已提交约束预优化→释放Opt/Freq→同几何高SP。

捕获释放最低点和配套高SP未返回；准确源捕获坐标未取得，但模型/方法足够约束输入，不构成永久SOURCE阻塞。

|量|作者|本地|本地−作者|原窗口/资格|
|---|---|---|---|---|
|activation_29815K_1atm|21.800000|21.673991|-0.126009|±3.000000；valid local transfer; not complete competition|
|separated_products|-3.000000|-5.270940|-2.270940|未校准；Physically balanced dication+formate; exergonic direction supported, raw2.27kcal discrepancy not calibrated away|
|binding|15.000000|未获得|未获得|未校准；NUMERICAL_RECOVERY_IN_PROGRESS|

本轮实际交付：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T094000Z/verification_report.md)；[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T094000Z/coverage.json)；[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T094000Z/jobs.json)；[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T094000Z/successor.json)。旧有效组件保留；当前新增范围不被旧PASS覆盖。

后继：收新82原子作业各阶段退出码和4次正常结束；必须验释放自由最低点240正模、P16-C80/CO2弯曲及库存。；若释放后仍解离，应记录未找到源捕获盆地并根据Hessian/结构选择有依据的构型后继；不得把约束结构或远隔CO2当作作者+15。；与旧合格2a/CO2/产品按同几何高层+原热项比较，保留产品2.270940差，无新容差。

以下完整保留历史记录；其中旧永久预算停止、旧待连接或已排除模型标签只描述当时状态，当前结论以上述新报告为准。

---

# 最新验证范围与状态：2026-10-13 07:30 UTC有限续接

更新时间：2026-10-13T08:23:11.050136+00:00。**PARTIAL**；current_scope_verified=false。

复核有效分离双阳离子/甲酸根原生日志和旧局部转移：228/6正模、同几何高SP，P–P2.21294 Å。直接势垒21.673991对21.8±3通过原窗口；分离产品−5.270940对−3.0，差−2.270940保持，无新容差。

未完成/阻碍：源+15 kcal/mol结合量没有合格可比计算。PCfirst原30步TRIC以及更早300+200步失败预算不重置；没有新的作者结构或数值修复依据。

本轮新作业：无。排队中的作业尚无原生应用结果。

逐目标覆盖、作者/本地差异、原容差、累计预算和精确后继：[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T073000Z/verification_report.md)；[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T073000Z/coverage.json)；[successor](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T073000Z/successor.json)。

历史PASS与“当前”措辞仅在各自时间/范围成立，不自动覆盖本次活动范围。以下完整保留此前记录。

---

<!-- GROUP_A_CONTINUATION_20261013T030303Z -->
# 最新验证状态（2026-10-13）

2026-10-13T03:49:16.117291+00:00；任务SHA256 `86557827ed529c32c130bd0f0592cf5d117233fd8f6d84be72489ebfa56890ed`；**PARTIAL**；current_scope_verified=false。

新增双阳离子与甲酸根均三段正常结束、分别228/6正模、2+/−1单重态；高SP与频率几何一致。双阳离子P−P=2.21294Å。平衡复合G给分离产物−5.27094 kcal/mol，对照作者−3.0，差−2.27094。直接局部转移和约21.674 kcal/mol势垒仍有效。

限定/阻碍：源+15绑定尚无合格结果，原PCfirst30步TRIC预算耗尽不能重启；产品−3没有已校准窗口。数值失败不证明所有捕获不存在。

逐目标[coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T030303Z/coverage.json)、[本轮报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T030303Z/verification_report.md)及[精确后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/attempt_20261013T030303Z/successor.json)。

活动作业：无。

以下旧版本原文完整保留为历史；其中旧PASS/“当前”或撤销范围不能覆盖上面的当前判断。未修改任何科学任务/评分/容差。

---

<!-- CORE7_CONTINUATION_GROUP_A_20261012 -->
# 最新验证范围与状态

2026-10-12T20:29:07.460936+00:00；当前任务SHA256 `86557827ed529c32c130bd0f0592cf5d117233fd8f6d84be72489ebfa56890ed`。**当前整题未严格通过**；科学状态 `PARTIAL`。

新增双阳离子与甲酸根均三段正常结束、分别228/6正模、2+/−1单重态；高SP与频率几何一致。双阳离子P−P=2.21294Å。平衡复合G给分离产物−5.27094 kcal/mol，对照作者−3.0，差−2.27094。直接局部转移和约21.674 kcal/mol势垒仍有效。

阻碍：源+15绑定尚无合格结果，原PCfirst30步TRIC预算耗尽不能重启；产品−3没有已校准窗口。数值失败不证明所有捕获不存在。

本轮报告：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/verification_report.md；逐目标覆盖：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/coverage.json；作业及后继：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_221aafe4bd916a11/continuation_20261012T190159Z/successor.json。

当前活动作业：本篇本轮无活动作业。

下列旧版本完整保留为历史；其中PASS、“当前”或旧范围结论不自动覆盖本轮实际合同。

---

# Verified computation reference — paper_221aafe4bd916a11 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Connection interpretation correction (2026-09-18)

The existing forward/reverse IRC calculations support the local P–H cleavage/C–H formation event around the hydride-transfer TS. They do **not** by themselves demonstrate optimization all the way to the separated reactant and product basins. The separately computed 2a/CO2 minima and product-side minimum are independent endpoint evidence, not IRC endpoint optimizations. The historical sentence below claiming direct connection to separated basins is an overstatement and is superseded by this paragraph.

Keep the successful local hydride-transfer task and its independently referenced barrier (19.8719700 kcal/mol in the archived branch). A finite 100-point path is not automatically a failure, and this correction does not add an unrequested full-cycle or separated-basin requirement. No new calculation was performed; historical group results remain untouched.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **AUTHOR_ROUTE_ONLY_PUBLIC_STARTER_NOT_REPLAYED**
- Applicability note: Public 2a geometry was replaced by a deterministic displaced starter; group verification used the original author endpoint. Under the accepted author-route verification policy this starter difference is not itself a task/evaluator mismatch; no independent discovery or public-starter replay is claimed.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 7 | `BLOCKED` | - 论文复现结论：**BLOCKED**。反应物端点已真实完成 Opt/Freq，但任务公开输入没有 product、TS candidate 或 IRC 终点，不能从反应物猜测势垒。 |
| 28 | `BLOCKED` | - 由于任务公开输入只提供反应物 2a，没有可验证的 product/TS 候选，论文复现结论保持 **BLOCKED**；不报告猜测的势垒。 |
| 83 | `PASS` | - evaluator 五文件在独立计算冻结后逐项读取并记录哈希；本轮结果：`PASS`。 |
| 92 | `PASS` | 字段均由真实成功输出支持，当前作者路线资格为 **PASS**（仅限声明的 2a+CO₂、 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Protonated bisphosphines: a new class of powerful hydride donors capable of CO2 reduction
- DOI: `10.1039/d5cc06952a`
- Task package: `tasks/final_verified_autonomous_research/paper_221aafe4bd916a11`
- Verification group: `docs/verification/group_2/paper_221aafe4bd916a11`
- Paper documents: `papers/paper_221aafe4bd916a11`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Selected barrier convention (clarified 2026-09-18)

The archived 19.8719700 kcal/mol branch uses G(TS) = -2324.733530 Eh from the successful standalone frequency output, G(2a) = -2136.233723 Eh from `artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log`, and G(CO2) = -188.531475 Eh from `artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stdout.log`. Each raw thermochemistry block specifies 298.150 K and 1 atm. The barrier is their stoichiometric difference; no separate 1 M correction was applied. This historical low-basis verification branch is not the SI high-basis single-point composite route. No new calculation or scientific target change is asserted.

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "barrier_kcal_mol": 19.871970024681406,
  "candidates": [
    {
      "candidate_id": "2a_reactant_in_out",
      "disposition": "reactant endpoint validated",
      "frequency_summary": "Gaussian Opt/Freq normal=True; frequencies=231; imaginary=0",
      "geometry_or_source": "artifacts/gaussian_batch/2a_reactant_optfreq_optimized.xyz",
      "role": "reactant minimum"
    },
    {
      "candidate_id": "TS2_2a_si_recovered_ts_optfreq",
      "disposition": "validated TS with bidirectional IRC",
      "frequency_summary": "status=success; normal=True; opt_complete=True; frequencies=240; imaginary=1",
      "geometry_or_source": "SI-recovered TS optimization followed by successful standalone frequency calculation; frequency/Gibbs evidence: artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stdout.log (the early optfreq summary alone does not contain complete frequencies)",
      "role": "hydride-transfer transition-state candidate"
    },
    {
      "candidate_id": "2a_dication_formate_si_recovered_optfreq",
      "disposition": "frequency-validated product-side endpoint",
      "frequency_summary": "status=success; normal=True; frequencies=240; imaginary=0",
      "geometry_or_source": "SI-recovered candidate; managed Gaussian evidence under artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq_summary.json",
      "role": "product-side dication/formate endpoint"
    },
    {
      "candidate_id": "author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20",
      "disposition": "validated CO2 component",
      "frequency_summary": "status=success; normal=True; frequencies=4; imaginary=0",
      "geometry_or_source": "Independent component; managed Gaussian evidence under artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_summary.json",
      "role": "neutral CO2 reactant component"
    }
  ],
  "hypotheses": [
    {
      "candidate_tests": [
        "Frequency validation of the SI-recovered TS2 gives exactly one imaginary mode.",
        "Forward and reverse IRC calculations both terminate normally and connect the TS basin to the separated reactant/product-side basins."
      ],
      "description": "A single-step hydride transfer from the in-out 2a cation to CO2, without a discrete intermediate.",
      "discrimination_test": "Validate a one-imaginary-frequency TS and inspect both forward and reverse IRC paths for direct connection versus a discrete intermediate.",
      "evidence": [
        "validation.transition_state",
        "validation.connectivity_test",
        "mechanism_conclusion"
      ],
      "hypothesis_id": "direct_hydride_transfer",
      "outcome": "supported"
    },
    {
      "candidate_tests": [
        "The same bidirectional IRC path was inspected for a separate stationary intermediate between the validated TS and endpoint basins."
      ],
      "description": "Hydride transfer proceeds through a discrete intermediate before the product-side endpoint.",
      "discrimination_test": "Inspect the validated bidirectional IRC path for a separate stationary intermediate between the TS and endpoint basins.",
      "evidence": [
        "validation.connectivity_test",
        "mechanism_conclusion",
        "limitations"
      ],
      "hypothesis_id": "stepwise_intermediate",
      "outcome": "not_observed_under_stated_model"
    }
  ],
  "limitations": "SI-recovered coordinates are verification-stage facts and are not task-visible inputs. The barrier is reported only after validating the separated 2a and CO2 reactant components and matching their summed stoichiometry to the TS/product; no incomparable-energy subtraction is used.",
  "mechanism_conclusion": "The SI-recovered 2a+CO2 candidate supports a direct hydride-transfer path with no discrete intermediate under the stated model; the barrier is computed from the validated TS Gibbs energy minus the separated 2a and CO2 reactant Gibbs energies.",
  "method": {
    "charge": 1,
    "electronic_structure": "wB97XD/6-31G(d,p)",
    "multiplicity": 1,
    "solvent": "PCM acetonitrile",
    "temperature_K": 298
  },
  "status": "complete",
  "validation": {
    "co2_component": "status=success; normal=True; optimization_completed=True; imaginary_frequency_count=0; valid=True",
    "connectivity_test": "forward/reverse IRC successes=['forward', 'reverse']; bidirectional_complete=True",
    "reactant_minimum": "optimization_completed=True, normal_termination=True, imaginary_frequency_count=0",
    "reactant_pair_gibbs_hartree": -2324.765198,
    "stoichiometry": "2a={'C': 26, 'P': 2, 'N': 8, 'H': 43} + CO2={'C': 1, 'O': 2} -> TS={'C': 27, 'P': 2, 'N': 8, 'O': 2, 'H': 43} / product={'C': 27, 'P': 2, 'N': 8, 'H': 43, 'O': 2}; match=True",
    "transition_state": "TS status=success; one_imaginary_frequency=True; TS/product SI recovery is isolated from agent-visible branch"
  }
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `9bbb3c42314d30e2c4a64decd7b1ff787e2ad780bcf2990ebd86030aa894cb62`
- Current `results.json` SHA-256: `ab038a64ef375bb445a3618034b62cbc00b3290332330568aa33e90a5d7be989`
- Changed top-level result fields: `hypotheses`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["hypotheses"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "ab038a64ef375bb445a3618034b62cbc00b3290332330568aa33e90a5d7be989", "detected": true, "previous_sha256": "9bbb3c42314d30e2c4a64decd7b1ff787e2ad780bcf2990ebd86030aa894cb62"} -->

Paper/SI document hashes:

- `papers/paper_221aafe4bd916a11/documents/main.pdf` — SHA-256 `9ab7929cb298e4351c64bdb02eca8bf833e107be8150df9d35cc992c96b12d74` (declared_match=True)
- `papers/paper_221aafe4bd916a11/documents/supplementary_001.pdf` — SHA-256 `c845d5d84e548a9d87d0193a131c9673de378c86f7e31bc979938a66d84ca3fc` (declared_match=True)

Report evidence lines retained:

- 任务可见输入为 `tasks/paper_reproduction/paper_221aafe4bd916a11/agent_input/data/inputs/2a_inout.xyz`（79 原子）。验证阶段采用 Gaussian 16 C.01，`wB97XD/6-31G(d,p) Opt Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm`，charge `1`、multiplicity `1`。最小反应物端点要求优化正常终止、频率输出完整且无虚频；势垒要求另外有可验证 product/TS/IRC 结构，这些输入未提供。
- 作业 `job_88b46c33af654acb8c9efb5c3df76aa5` 通过原生 Gaussian supervisor 提交，使用 8 CPU、24000 MB，`walltime_seconds=null`（无人工墙钟上限）。Gaussian 输出有 `Optimization completed`、`Stationary point found` 和 `Normal termination of Gaussian 16`；频率数 231，虚频数 0，最低频率 22.1385 cm⁻¹，最终 SCF 能量 −2136.84554897 Eh。优化结构由通用 orientation 提取器保存。
- - evaluator 五文件在独立计算冻结后逐项读取并记录哈希；本轮结果：`PASS`。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **100**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/status.json` — successful status record; SHA-256 `a447749d76e417c6ed1041dd3f2b79fafd95ba61e719efdfe942c6b4e77c677f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/collection.json` — successful execution artifact; SHA-256 `3957ce5a6d70992f0059484773a95b1a3065793e522f33dccd55b18177b75208`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/input.com` — successful execution artifact; SHA-256 `b7fc4e468bc4509687ed403f258f5befb36f56ac2af23457efda1c9373d71acb`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stdout.log` — successful execution artifact; SHA-256 `c61f150b52f53694456d6f11a01a3a1c67e5da5a457baedf3c7c4051d193a95b`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/status.json` — successful status record; SHA-256 `7efadbefd1785ce18203aa5bcf404e6f0c220c777ea5fa84a3d2a8eba8c1d743`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/collection.json` — successful execution artifact; SHA-256 `eecd61acc5dbfd792919dd8364eceafbc411496de6c53226741291504950843d`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/input.com` — successful execution artifact; SHA-256 `fc5a274764bfa39b1234af1f20eee994723e397ceb191159ebcfd96dd6e3dcee`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log` — successful execution artifact; SHA-256 `c3f6a3ea6995f59adc2451ad044f72bbbff6dab8ed2f7eb60e2c6c592f214338`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/status.json` — successful status record; SHA-256 `b75b758e66720026462de1a1ec034e157fdbb31ff5bb564f99223a26cf154135`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/collection.json` — successful execution artifact; SHA-256 `8f4066888d23c3f745befc8592dc166ce58b9c6d03a42a3980f42ccf2502e49f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/input.com` — successful execution artifact; SHA-256 `47b5ec8e27743c37b2647a0f0f5a753108f0026c88065557fb74e0ffb186bebc`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stdout.log` — successful execution artifact; SHA-256 `77b514d80bae65addc190ba07db2001493d837d6753ad10563a5d3ed96275c2c`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/status.json` — successful status record; SHA-256 `70e5e7c9bf89cbab7f2ca8024c0fdfbb66f7b35e7683491866bc31832b7a8038`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/collection.json` — successful execution artifact; SHA-256 `9e67e37c62995b5e8ebbcab9b86c493437813513da3caca28deda73e6e9a5cd1`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/input.com` — successful execution artifact; SHA-256 `6f9bd835888a14ae79ca7d5de5c3834493011455dc9667cea927349511809a7e`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/repair.xyz` — successful execution artifact; SHA-256 `f6557496ea5147080fbb610b54f9cfc0a3014ef8d62dd445ebfe1efcc294a734`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/route_manifest.json` — successful execution artifact; SHA-256 `b193ddb00ede61f58d3979e74669574d1c616c5a4a58507584fa204f2e322a26`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/status.json` — successful status record; SHA-256 `e5163288aedcd821ca8cdc831485b2ee798e50205801e1a2892fff07b76e4511`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `6ca69b177b0568551830c29048eb6bf505bb1a9a36d1a2d887f6d15d95e0b63f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/source_input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/status.json` — successful status record; SHA-256 `c0739a336e838aa189a46affe3529d11fce7b58bb196ddf46f2958f3ed8371d2`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `d1d08791fc3c50b61ad1ae7e59dae94384c1c9ef9a79612728a2453769c96138`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/source_input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/status.json` — successful status record; SHA-256 `60b3dee5e627c59faf8ae3867d234c63adbfec48246b91092bc3316e23770647`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `5a587d36381c2ae344ebb197a191caca2de44c79472b9c37e67c3dff0037bb78`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/source_input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/status.json` — successful status record; SHA-256 `6f619bce7c7e1c87e7690682de3d02dfcf749c29728bc97d9bdf814cc63780c0`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `e754d72bc409267b3e8656cfedfda96633966b83db4c8bd845b1081ab38a51e6`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/source_input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/status.json` — successful status record; SHA-256 `da0ec43a12d8292f145ef166a007b9aa1816352b770d25d8f5f549f357e65dce`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/collection.json` — successful execution artifact; SHA-256 `c347864fbea851cff7c0830be43a0e274cc4983d93952848000afbc974769655`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/input.com` — successful execution artifact; SHA-256 `e6b851762022c3097bbd15d21c54b81e82fbeb88bae5938bce2003e5dcef7b42`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/route_manifest.json` — successful execution artifact; SHA-256 `60e374b28d8ff7ac820075e1f16168d5cd884bb84766f5082c09d735cff52664`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/status.json` — successful status record; SHA-256 `da0ec43a12d8292f145ef166a007b9aa1816352b770d25d8f5f549f357e65dce`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/collection.json` — successful execution artifact; SHA-256 `c347864fbea851cff7c0830be43a0e274cc4983d93952848000afbc974769655`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/input.com` — successful execution artifact; SHA-256 `e6b851762022c3097bbd15d21c54b81e82fbeb88bae5938bce2003e5dcef7b42`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/request.json` — successful execution artifact; SHA-256 `02a113d8f44ec062cef0764f1213929fcb986855c32da9a0fd5f9582f3aa6b26`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/status.interruption_recovery.json` — successful execution artifact; SHA-256 `556309a921584d000df93c61812495abbda4649979a73c630925cd6e8374005f`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/status.json` — successful status record; SHA-256 `b75b758e66720026462de1a1ec034e157fdbb31ff5bb564f99223a26cf154135`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/collection.json` — successful execution artifact; SHA-256 `8f4066888d23c3f745befc8592dc166ce58b9c6d03a42a3980f42ccf2502e49f`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/group2_stop_reconciliation.json` — successful execution artifact; SHA-256 `28ccbfa1f23579b20c978176c50efef318d3d29bcb5cb3e15bf6a126f66214aa`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/input.com` — successful execution artifact; SHA-256 `47b5ec8e27743c37b2647a0f0f5a753108f0026c88065557fb74e0ffb186bebc`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/request.json` — successful execution artifact; SHA-256 `b89d8ab13f33c1f1c7f602c36adce9f6cc748589e7452e9ec3946d149f693146`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/status.json` — successful status record; SHA-256 `7efadbefd1785ce18203aa5bcf404e6f0c220c777ea5fa84a3d2a8eba8c1d743`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/collection.json` — successful execution artifact; SHA-256 `eecd61acc5dbfd792919dd8364eceafbc411496de6c53226741291504950843d`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/input.com` — successful execution artifact; SHA-256 `fc5a274764bfa39b1234af1f20eee994723e397ceb191159ebcfd96dd6e3dcee`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/request.json` — successful execution artifact; SHA-256 `2950600ba8ddb299fc8144fbff4aaf916a63d383516a657fb028d3f79a44543a`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/status.json` — successful status record; SHA-256 `70e5e7c9bf89cbab7f2ca8024c0fdfbb66f7b35e7683491866bc31832b7a8038`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/collection.json` — successful execution artifact; SHA-256 `9e67e37c62995b5e8ebbcab9b86c493437813513da3caca28deda73e6e9a5cd1`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/input.com` — successful execution artifact; SHA-256 `6f9bd835888a14ae79ca7d5de5c3834493011455dc9667cea927349511809a7e`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/request.json` — successful execution artifact; SHA-256 `354b609127bf851c991acc35c695eb318e06cd0a3b22fc607e562271cce68e67`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/status.interruption_recovery.json` — successful execution artifact; SHA-256 `fa78b7f3421933ba9ed4de4647082e2b7724396d32729202c5a4f7c10fe3b342`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/status.json` — successful status record; SHA-256 `a447749d76e417c6ed1041dd3f2b79fafd95ba61e719efdfe942c6b4e77c677f`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/collection.json` — successful execution artifact; SHA-256 `3957ce5a6d70992f0059484773a95b1a3065793e522f33dccd55b18177b75208`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/input.com` — successful execution artifact; SHA-256 `b7fc4e468bc4509687ed403f258f5befb36f56ac2af23457efda1c9373d71acb`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/request.json` — successful execution artifact; SHA-256 `b6bcfe623e19a5081f78229ee646089d1a612a39d0b984645ddccb9447a3bf7b`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/status.json` — successful status record; SHA-256 `9a61aade67d8a8e80cc419d1c3dbf63a8934e011c210e482527af494126b8871`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `1b2e3c55266d5935696796f088b5fe068c2d91ddfdc317d5f1d2560b412ec3a9`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/input.com` — successful execution artifact; SHA-256 `973fec7ea4cc42bf53a06fa71abae9cd9e96fadb47a729fb50ff001e5729eeb7`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/route_manifest.json` — successful execution artifact; SHA-256 `b193ddb00ede61f58d3979e74669574d1c616c5a4a58507584fa204f2e322a26`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/status.json` — successful status record; SHA-256 `e5163288aedcd821ca8cdc831485b2ee798e50205801e1a2892fff07b76e4511`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `d11b228f7590105d7ca7790c99aecdb350a0068fd6e9d5bc35746595a7c1ddcf`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/route_manifest.json` — successful execution artifact; SHA-256 `6ca69b177b0568551830c29048eb6bf505bb1a9a36d1a2d887f6d15d95e0b63f`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/source_input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/status.json` — successful status record; SHA-256 `c0739a336e838aa189a46affe3529d11fce7b58bb196ddf46f2958f3ed8371d2`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `84506db6a119fa34796edff09fbe91bc4bc2b03fae3d9e86bbf3d380ef2ccdd8`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/route_manifest.json` — successful execution artifact; SHA-256 `d1d08791fc3c50b61ad1ae7e59dae94384c1c9ef9a79612728a2453769c96138`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/source_input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/status.json` — successful status record; SHA-256 `60b3dee5e627c59faf8ae3867d234c63adbfec48246b91092bc3316e23770647`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `6d245037fffed9e858474b521547a1c4f2e5ea50f647b524b2720d07a20a3195`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/route_manifest.json` — successful execution artifact; SHA-256 `5a587d36381c2ae344ebb197a191caca2de44c79472b9c37e67c3dff0037bb78`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/source_input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/status.json` — successful status record; SHA-256 `6f619bce7c7e1c87e7690682de3d02dfcf749c29728bc97d9bdf814cc63780c0`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `3bb7500e2cc19bf01061029af3cfddb9f2f607876c6921091fd96fd4759575a0`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/route_manifest.json` — successful execution artifact; SHA-256 `e754d72bc409267b3e8656cfedfda96633966b83db4c8bd845b1081ab38a51e6`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/source_input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/status.json` — successful status record; SHA-256 `96db83154561cfa2adcff9459dc03561495d6340c452ba321888857b5e2f7f46`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `66fe5d351b6a68b6eea1b9edcc1f3ab715ba8c000b2ea839e299449619d54ada`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/input.com` — successful execution artifact; SHA-256 `5d870d2f1a91187e6cec878b02e8cd5fa5bfe296356c2736acabc917eb38dd9a`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/route_manifest.json` — successful execution artifact; SHA-256 `60e374b28d8ff7ac820075e1f16168d5cd884bb84766f5082c09d735cff52664`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/2a_reactant_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 2a_reactant_optfreq; submitted_at=2026-08-29T09:32:41.694489+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/6-31G(d,p) Opt Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm; command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/2a_reactant_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log`
2. `artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 TS2_2a_si_recovered_ts_optfreq; submitted_at=2026-08-30T02:44:52.051203+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/6-31G(d,p) Opt=(TS,CalcFC,NoEigenTest,MaxCycles=200) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/TS2_2a_si_recovered_ts_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stdout.log`
3. `artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 2a_dication_formate_si_recovered_optfreq; submitted_at=2026-08-30T02:46:08.658734+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/6-31G(d,p) Opt=(CalcFC,MaxCycles=200) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/2a_dication_formate_si_recovered_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stdout.log`
4. `artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 author_2a_reactant_wb97xd_631gdp_pcm_optfreq; submitted_at=2026-08-31T17:12:39.083476+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/6-31G(d,p) Opt=(CalcFC,MaxCycles=300) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/author_2a_reactant_wb97xd_631gdp_pcm_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/repair.xyz`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/stdout.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/tmp.fchk`
5. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/status.json` — label=group_2 paper_221aafe4bd916a11 author_TS2_2a_wb97xd_631gdp_pcm_ts; submitted_at=2026-08-31T17:17:39.674855+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/6-31G(d,p) Opt=(TS,CalcFC,NoEigenTest,MaxCycles=300) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/author_TS2_2a_wb97xd_631gdp_pcm_ts.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/stdout.log`
6. `artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/status.json` — label=artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stdout.log`
7. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/status.json` — label=artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/stdout.log`
8. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/status.json` — label=artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/stdout.log`
9. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/status.json` — label=artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stdout.log`
10. `provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/status.json` — label=provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/author_2a_reactant_wb97xd_631gdp_pcm_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/stdout.log`
11. `provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/status.json` — label=provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/stderr.log`
12. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/stderr.log`
13. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/stderr.log`
14. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/stderr.log`
15. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/author_TS2_2a_wb97xd_631gdp_pcm_ts.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `r4`.

- Key-point IDs: `ar_process_freq, ar_process_hypotheses, ar_result_barrier, ar_result_scope`
- Conclusion IDs: `ar_final`
- Scoring-rule IDs: `r1, r2, r3, r4, r5`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r1` → reference `ar_process_freq`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r2` → reference `ar_process_hypotheses`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r3` → reference `ar_result_barrier`; type=numeric; unit=kcal/mol; tolerance=3.0; comparison=absolute difference; evaluator_target_present=True
- rule `r4` → reference `ar_result_scope`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r5` → reference `ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r3` / reference `ar_result_barrier`: target=21.8 kcal/mol; tolerance=3.0; numeric result leaves=[19.871970024681406]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r1` / reference `ar_process_freq` / field `$.validation.reactant_minimum` / result path `$.validation.reactant_minimum` = `"optimization_completed=True, normal_termination=True, imaginary_frequency_count=0"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].hypothesis_id` = `"direct_hydride_transfer"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].description` = `"A single-step hydride transfer from the in-out 2a cation to CO2, without a discrete intermediate."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].discrimination_test` = `"Validate a one-imaginary-frequency TS and inspect both forward and reverse IRC paths for direct connection versus a discrete intermediate."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].candidate_tests[0]` = `"Frequency validation of the SI-recovered TS2 gives exactly one imaginary mode."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].candidate_tests[1]` = `"Forward and reverse IRC calculations both terminate normally and connect the TS basin to the separated reactant/product-side basins."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].outcome` = `"supported"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].evidence[0]` = `"validation.transition_state"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].evidence[1]` = `"validation.connectivity_test"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[0].evidence[2]` = `"mechanism_conclusion"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].hypothesis_id` = `"stepwise_intermediate"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].description` = `"Hydride transfer proceeds through a discrete intermediate before the product-side endpoint."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].discrimination_test` = `"Inspect the validated bidirectional IRC path for a separate stationary intermediate between the TS and endpoint basins."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].candidate_tests[0]` = `"The same bidirectional IRC path was inspected for a separate stationary intermediate between the validated TS and endpoint basins."`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].outcome` = `"not_observed_under_stated_model"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].evidence[0]` = `"validation.connectivity_test"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].evidence[1]` = `"mechanism_conclusion"`
- rule `r2` / reference `ar_process_hypotheses` / field `$.hypotheses` / result path `$.hypotheses[1].evidence[2]` = `"limitations"`
- rule `r3` / reference `ar_result_barrier` / field `$.barrier_kcal_mol` / result path `$.barrier_kcal_mol` = `19.871970024681406`
- rule `r4` / reference `ar_result_scope` / field `$.limitations` / result path `$.limitations` = `"SI-recovered coordinates are verification-stage facts and are not task-visible inputs. The barrier is reported only after validating the separated 2a and CO2 reactant components and matching their summed stoichiometry to the TS/product; ..."`
- rule `r5` / reference `ar_final` / field `$.mechanism_conclusion` / result path `$.mechanism_conclusion` = `"The SI-recovered 2a+CO2 candidate supports a direct hydride-transfer path with no discrete intermediate under the stated model; the barrier is computed from the validated TS Gibbs energy minus the separated 2a and CO2 reactant Gibbs ener..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized input leakage review
- Files changed in that review: `none recorded`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained XYZ geometry for 79-atom protonated bisphosphine 2a; charge +1 and singlet are stated in the task.

Public input files and hashes:

- `agent_input/data/inputs/2a_inout.xyz` — SHA-256 `a8bc04b720f4653ef0bc98fc1c8823c245a1fb170fcf7ad7b8813fe4180ec03a`; size=2970 bytes; xyz_atom_count=79; xyz_comment=independently displaced starting geometry; source endpoint retained evaluator-private; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_2/paper_221aafe4bd916a11/verification_report.md` — verification record; SHA-256 `596db298293cafa149ba51d4a42f81e4dadac025ddf97ada95a3885dffb72dfa`
- `docs/verification/group_2/paper_221aafe4bd916a11/report/results.json` — verification record; SHA-256 `ab038a64ef375bb445a3618034b62cbc00b3290332330568aa33e90a5d7be989`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.

## Evidence scope review (2026-09-19)

The saved direct hydride-transfer IRC and barrier support the local path. Repeated guesses using that same IRC do not demonstrate discrimination of every AR direct/stepwise alternative. Preserve the existing successful path; do not certify complete AR hypothesis coverage without its actual discriminating evidence.


<!-- phase2_verification_group02_20261011 -->

## 2026-10-11 第二阶段独立参考验证（第 2 组）

记录时间：2026-10-11T06:11:06.052366+00:00。当前科学状态：**PARTIAL**。

直接转移势垒21.674326kcal/mol及局部连接已恢复；新分步候选先几何失败，修复后在Hessian阶段因配额退出。不同机制比较未完成。

本节针对当前自主科研题目的必需关键点与结论；历史局部 PASS 不自动迁移。本轮可查作者资料，是独立参考计算验证，不是盲测执行。

验证起始包 hash：`7b03d564f1e885fc52ca482b3b34212567133201208d7504ac3819d01d9bf059`。固定科学契约 hash：`d2c6678601dad1136aae716c7e01e5d314d3ffdfce506e5df934918986c37e89`（排除本 reference 与 manifest）。追加后的包 hash 由 package_manifest.json 和本组 completion.json 记录，避免自引用。

来源定位：Main PDF3 Fig.3、PDF4 Table2/21.8kcal/mol；SI PDF1计算方法，PDF19–20的2a in–out及PDF65–66的TS2(2a)坐标；精确evidence_map亦保留。

物理定义与条件：ωB97XD/6-31G(d,p) Opt/Freq +6-311++G(d,p) SP，PCM MeCN；2a+1 singlet、CO2 neutral singlet、TS+1 singlet；GTS−G2a−GCO2，298.15K/1atm。

### 逐目标结果

| ID | 状态 | 真实结果、差值与接受边界 |
|---|---|---|
| `ar_process_freq` | PASS | 直接通道2a/CO2/TS原生频率与状态有效；配额失败的候选不称为最低点。 |
| `ar_process_hypotheses` | PARTIAL | 直接与P–C–CO2分步候选已明确；首候选输入碰撞，修复节点在Hessian阶段因配额失败，尚无有效机制判别。 |
| `ar_result_barrier` | PASS | 当前定义21.674326 vs21.8±3kcal/mol，差−0.125674。 |
| `ar_final` | PARTIAL | 局部直接转移成立；当前所需不同假说计算比较未闭合。 |

### 原生核查与来源差异

- 六份低/高层原生日志独立提取。79原子2a有231正模，CO2有4正模，82原子TS有240模式且仅−651.5676cm−1虚频。三个高层SP对应各自几何。

- 统一复合G=Ehigh+(Glow−Elow)：298K势垒21.669581；用原生熵及正频率精确重组298.15K后为21.674326 kcal/mol，对21.8±3差−0.125674。未添加1M或预关联复合物偏移。

- 两份旧原生IRC哈希重新核对：各100个路径步（101个含起点标记）；P15–H82为1.428411→2.570291Å，C37–H82为2.283887→1.123168Å。是明确的局部P–H到C–H转移，不冒充两个已验证分离最低点。

- 旧P–O关联产物不等于自由formate+dication，也不自动构成独立分步机制。新P16–CO2候选首次因O82–P11仅0.455Å，在SCF前报Atoms too close；平台即使显示SUCCEEDED，科学结果仍为失败。

- 保留失败输入/输出并提交一次立体排斥筛选后的修复：P16–C80=1.95Å，45°偏转，OCO135°，Cartesian Opt/Freq。几何候选未完成前不能宣称分步机制被排除。

- 最新原生收取：PC_CO2_steric_repair 已终态且未产生所需有效结果；详见failure_intake.json。平台SUCCEEDED不是科学成功。后继必须先恢复存储空间，再做有检查点的有限恢复，未自动重试。

### 原始证据与计算执行

完整证据链：[verification_report.md](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/verification_report.md), [coverage.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/coverage.json), [resource_accounting.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/resource_accounting.json), [jobs.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/jobs.json), [next_steps.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/next_steps.json)。

coverage 中记录源 PDF hash 和逐目标定义；audit JSON 保存原生日志路径、SHA256、route、原子/状态、优化/SCF/IRC 步数、频率、关键行与软件计时。resource_accounting 另保留实际资源、UTC 作业时间线、释放状态及 runner 计时，未把缺失字段估算补齐。

本篇独立重新提取文件：[failure_intake.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/failure_intake.json), [independent_thermo_connectivity.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/independent_thermo_connectivity.json), [reused_irc_audit.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/reused_irc_audit.json), [reused_native_audit.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/reused_native_audit.json)。

| Case | Job ID | 平台状态 |
|---|---|---|
| PC_CO2_stepwise_candidate | `hpc-job-fcc8ec7f-3b9c-4215-9900-ba1bcf5f375a` | SUCCEEDED |
| PC_CO2_steric_repair | `hpc-job-e28af370-92db-4c17-88e2-7f39223b169a` | SUCCEEDED |

平台 SUCCEEDED 或正常退出不单独构成科学 PASS。配额失败尝试保留；新恢复作业采用独立目录/ID，实际结果收取前不得当作完成。

### 未完成项及后继

- 执行阻塞：共享盘配额/空间不足使后继未完成；先恢复可靠空间并核checkpoint，不能把终态失败写QUEUED。

- 独立P–C/CO2分步候选的优化、频率与实际连接尚未完成。

- 若分步中间体存活，仍需同级高层SP及其后 hydride 路径；一次坍塌只否定这一有限候选。

逐步恢复条件见 [next_steps.json](../../../../../docs/verification/group_2/paper_221aafe4bd916a11/small_molecules_20261010T231612Z_g02/next_steps.json)；共享存储问题及有限恢复见 [storage_blocker.json](../../../verification_dispatch/20261010T231612Z/phase2_verification/group_02/storage_blocker.json) 和 [storage_recovery_plan.json](../../../verification_dispatch/20261010T231612Z/phase2_verification/group_02/storage_recovery_plan.json)。

契约/来源/发布问题单独记录于 [repair_proposals.md](../../../verification_dispatch/20261010T231612Z/phase2_verification/group_02/repair_proposals.md)。本次未更改任务、评分、容差或分组。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`df1bf693933bd24a7841fc6081b88619768a9a5a8d2ae9197acf1d60f16b30fc`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_221aafe4bd916a11/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_221aafe4bd916a11/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_221aafe4bd916a11/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。

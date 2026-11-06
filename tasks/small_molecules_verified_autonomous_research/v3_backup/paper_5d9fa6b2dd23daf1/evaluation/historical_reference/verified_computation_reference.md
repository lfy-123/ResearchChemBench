# 现行科学分V2与验收范围（2026-10-22）

当前AR：PROVISIONAL_PASS_QUALITATIVE；`paper_science_v2`，8项、100分，仅科学结果。中间关键节点60分、最终结论40分。可按本版规则评分；专家发布审查尚未完成。

保留原定量规则的±2.0 kcal/mol，未扩大或依残差拟合。只对两局部势垒和两净产物G独立计分；完整曲线高度、醚/离子形成能留作上下文，避免派生量和非核心步骤重复计分。窗内仍须物理身份正确；最终通道排序/放能判断独立评价。

方法/范围限定：
- SI溶剂优化/频率叙述与S21气相热项脚注冲突；实际使用HFIP谐频重构，G16 A.03→C.01。
- 没有cis竞争、去质子化势垒或完整催化网络；反向超分子未收敛，独立合格片段用于热化学。
- 8项旧窗口均通过，最大差1.523006 kcal/mol；不将两产物0.2 kcal/mol差当鲁棒排序。

本次复制与评分迁移未提交新计算，公开输入、身份与交付合同逐字节保留。题面中若有历史过程分措辞，不构成本版得分条件；本版不奖励过程、失败诊断或资源投入。下方按日期保留原始验证记录；旧pending/失败不是当前验收状态，失败原日志也未改写为成功。

---

# Computational reference status

<!-- PARENT_ACCEPTANCE_20261022T013509Z -->
## 2026-10-22 父级独立验收：当前两模式科学问题完成

更新UTC：2026-10-22T01:58:48.277293+00:00。AR/PR均已登记 **PROVISIONAL_PASS_QUALITATIVE**，不再是待审候选。独立重读29份原生日志并核对SI图S3；新增产物177个正频率补齐结构证据，8/8参考量在原±2 kcal/mol内，最大绝对差1.523006。酸/磺酰胺局部势垒12.972775/10.201388（作者13.0/10.2），净产物−12.309484/−12.116446（作者−12.3/−12.1），核心定性结论一致。

SI溶剂频率文字与气相热项脚注的冲突仍明确保留；采用当前题目允许声明的HFIP谐频重构。作者G16 A.03、实算C.01；不声称全部隐藏设置严格一致。反向未收敛超分子不作为热化学证据，使用独立合格片段。当前问题已覆盖，不要求整篇论文全部计算。数值窗口通过、方法限定、正式评分与发布资格分别记录。

[父级独立验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_progress_resume_20261022T013509Z/5d9_parent_review/独立验收.md) · [原生日志与逐项误差](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_progress_resume_20261022T013509Z/5d9_parent_review/independent_native_audit.json) · [登记决定](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_progress_resume_20261022T013509Z/parent_acceptance_decision.json)。

以下旧日期段落仅保留历史进展与失败证据；当前状态以上方父级验收为准。


<!-- job_progress_resume_20261022T013509Z_new_group_03 -->
当前结论（2026-10-22T01:44:39.244416+00:00）：5d9在AR/PR同一科学问题的最小必要计算证据已齐备，提出PROVISIONAL_PASS_QUALITATIVE候选，待父级独立审查登记；尚未登记通过。d4f00824原生exit0/Normal、177正模、最低22.5973cm^-1，同优化archive几何差0；自身Gcorr0.487233Eh。8/8原能量量在原±2容差内、15条能量链复用；产品频率仅补足局部极小值证据，不新增M06能量链。新计算提交0。

以下旧日期段落为历史；“产品频率待返回/整题未齐”由本轮核收候选替代，不抹去历史失败。

<!-- job_progress_resume_20261021T154758Z_new_group_03 -->
当前核收（2026-10-21T16:10:08.271324+00:00）：AR/PR仍INCOMPLETE。6d1d66e5平台SUCCEEDED但原生exit1；产品Opt已收敛并完成trans/质子映射，频率被6h上限中断；反向60步未收敛，已分离为Ad+与E-磺酰胺。仅补产品固定几何频率，实际作业hpc-job-d4f00824-f463-412a-9263-bcbd86b3ab7b（RUNNING/RUNNING）。8/8能量量和15完整链直接复用，新增整题候选0。

以下旧日期记录保留，端点RUNNING及整段Normal的旧观察由本轮逐段核收替代。

<!-- job_return_20261021T071804Z_new_group_03 -->
当前核收（2026-10-21T07:43:18.913776+00:00）：两模式 INCOMPLETE。13e3e0ec M06原生正常完成并验收，原能量量8/8、15条完整能量链；局部磺酰胺势垒10.201388对作者10.2，完整profile两TfOH分支14.422993/14.423006对12.9，各自在原±2.0kcal/mol内。6d1d66e5端点仍健康RUNNING；当前实际产品侧结构有成环/trans证据，但尚未Opt/Freq收敛，反向未开始。本轮新增整题候选0、新提交0。

以下旧日期段落保留作历史，M06待核收状态以本轮结果为准。

<!-- feasible_nine_20261021T035151Z_new_group_03 -->
当前状态（2026-10-21T04:30:33.473916+00:00）：INCOMPLETE，两模式一致。作者TS1-3s源Force/Freq已独立验收：61原子、极小力、177模且唯一化学负模−138.5952cm^-1，Gcorr0.476590Eh。已实际提交自身M06及有限双向端点测试，原8项能量仍6/8可用。不重复成功Force/Freq或TS优化；d142保持已登记、不改不重算。

下方带日期记录均为历史快照；旧“Force/Freq待核收”由本轮验收替代。

<!-- source_TS_diagnostic_20261020T0710Z -->
当前状态（2026-10-20T08:05:56.623282+00:00）：INCOMPLETE，两模式一致。作者TS1-3s完整61原子源坐标已独立核实；缺的是本验证验收的完整曲率/反应模、自身M06及相称局部连接，不是缺作者TS。用户授权的一次固定源Force→Freq诊断已实际提交 hpc-job-75bd7738-db68-4d30-a8ca-428b2a0e87b5，平台RUNNING、原生RUNNING。额外Opt=Tight位移或完整IRC不再误作作者要求；原失败记录仍失败。酸成功链与6/8旧对照复用。

以下带日期记录为历史快照；关于“无新诊断暂停”的旧现状由本轮精确源证据及实际诊断提交替代。

<!-- new_group_03_sp_return_current -->
当前状态（2026-10-20T02:59:50.554983+00:00）：INCOMPLETE，两模式一致。新SP hpc-job-76a49b6c-2980-47c8-824e-8f98500c0bf6 已原生Normal/exit0并完成独立核收；质子化trans内酯Opt/Freq/SP链完整。原8项能量比较仍6/8，磺酰胺TS/freq/SP及对应势垒比较仍缺。最新证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03_sp_return。下方既往pending/RUNNING描述仅为注明日期的历史快照，由本节及文末新事件记录替代。

## 历史验证记录（以下状态均按其记录时间解释）

**Pending independent calculation.** This repair reviewed the source and performed source-energy arithmetic; it submitted no quantum-chemistry calculations. Native validation and runtime checks are structural checks only.

Reconstruct the source Table S22 structures for AdOH, HFIP ether, Ad+, TfOH, OTf-, HFIP, H2O, both starting substrates, the two proton-retaining cyclization TSs and the neutral trans products. Obtain valid minima and TS character/connectivity, correct charge/spin and the stated M06//B3LYP/SMD-HFIP energies. Use Table S21's decomposition as a source reference, retaining the ambiguity that its thermal corrections are called gas phase while optimization is described in solvent.

Assemble the exact balanced ledger in scoring_rules.json: for each X, initial AdOH+X+TfOH+HFIP; ether+X+H2O+TfOH; Ad++X+OTf-+H2O+HFIP; [Ad+X]+ TS+OTf-+H2O+HFIP; neutral product+TfOH+H2O+HFIP. The targets are ether 1.4 and cation 2.7, TS levels 15.7/12.9, local barriers 13.0/10.2, and product energies -12.3/-12.1 kcal/mol. Reusing the same cation/reference calculation is appropriate; reusing a paper number as a computed result is not.

Each numeric tolerance is provisionally 2.0 kcal/mol and is uncalibrated; the acid/sulfonamide barrier direction and exergonic products are assessed separately. The narrow product energy difference is not a robust ordering target. Do not require an unreported cis competitor, an ether/cation-generation TS or the whole paper's branches. Source-table arithmetic or a scheduler success state does not verify the underlying geometries and electronic results.

Sources: main PDF p8–9 mechanism/DFT discussion; SI PDF p79–80 section 7.3 and Figure S3; p81 Table S21 and Table S22 thereafter.


## Independent author-route execution update (2026-10-16, group_03)

current_scope_verified=false. 15 opt/frequency+single-point job attempts for 13 assessed stationary states have now been actually submitted. 3 native chains passed exit, normal-termination, atom/charge/spin, frequency-count, same-geometry and protocol-marker checks at 2026-10-16T02:05:54.094660+00:00; this does not certify the reaction key points.

- H2O: native opt/freq+SP complete; G=-76.4303639972 Eh; NImag=0; Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019.
- triflate: native opt/freq+SP complete; G=-961.7018863940 Eh; NImag=0; Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019.
- HFIP: native opt/freq+SP complete; G=-789.8413090630 Eh; NImag=0; Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019.
- TfOH: not accepted; optfreq: imaginary_mode_count; NImag=1; native/optfreq.log retained. See successor.json for scientifically distinct recovery attempts.

Table S21 gas-phase wording for Gcorr versus solvent optimization is retained; water constituent follows solvent-opt/freq and agrees closely. No cis/trans competition target.

All required IDs and scientific rules are recorded in `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_5d9fa6b2dd23daf1/new10_20261016/coverage.json`; paper/source/actual/difference rows are in `comparison.csv` and `state_comparison.csv`. Native evidence and job IDs are in `cases/` and `jobs.json`. See `author_method_manifest.json`, `verification_report.md` and `successor.json` for method fidelity, source ambiguities, remaining IRC/identity validation and continuation. Computations are author-guided verification, not an AR discovery test. No scoring rules, targets, tolerances, task inputs, scientific core or reserved quantitative weight were changed.


Stationarity recovery: {'TfOH': -330.7943} lists parent cases and their negative modes in cm^-1. Native optimization/frequency normal-terminated but the source NImag=0 minimum condition failed, so SP was gated off. Two same-method successors per case follow positive/negative directions of the computed mode with maximum atom displacement0.15 A; original logs/checkpoints retained. Neither source thermochemistry nor successor results are assumed valid. See source/*stationarity_issue.json and recovery_plan.json.


## Author-route verification followup (2026-10-17, new_group_03)

current_scope_verified=false. 13/15 current stationary attempts have audited optfreq/SP chains; migrated STOPPED predecessors excluded. 2 new actual jobs: 1 justified recovery and 1 dual-direction IRC/endpoint jobs. Platform and native status are distinct; no whole-paper PASS or acceptance candidate.

6/8 energy quantities assembled: ether1.455475, acid local12.972775, acid product−12.309484, sulfonamide product−12.116446 kcal/mol. Cation4.221605/4.221618 and acid TS profile17.194380/17.194393 use the two separately reported TfOH recovered minima. They do not replace source2.7/15.7. Both sulfonamide TS quantities remain missing.

- Profile15.7/12.9 and local13.0/10.2 remain distinct; no cis/trans competitor gold.
- Original TfOH −330.7943cm−1 fails minimum classification. Both ±mode minima have zero imaginary modes and the same molecular graph; their energies differ by0.000013kcal/mol and lie about1.5097kcal/mol below the author composite. Preserve both branches and profile offset.
- B3LYP/def2TZVP HFIP opt/frequency and M06/def2TZVP HFIP SP,293.15K/1atm; epsilon16.70 and remaining2-propanol SMD parameters. Source gas-Gcorr wording versus solvent prose and authorA.03 versus installedC.01 qualifications remain.

Complete author/actual/difference ledgers, key-point/rule coverage and raw-evidence links: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/paper_5d9fa6b2dd23daf1/verification_report.md, energy_comparisons.json, state_comparison.csv, coverage.json. Identity/modes: geometry_mode_summary.json. Same-geometry/protocol: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/same_geometry_protocol_audit.json. New IDs/native snapshot: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/submission_receipts.json and successor_readbacks/final/inventory.json. Finite continuation: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/new_group_03/handoff.json. No task instruction,input,evaluator,gold,tolerance,qualification,reserved weight,expert or zip changed. This is author-guided verification, not AR discovery evidence.


## Native-return review (2026-10-17, status_review_20261017T1137Z/new_group_03)

6/8 energy quantities available. Ether1.455475; cation4.221605/4.221618; acid TS profile17.194380/17.194393; acid local12.972775; acid product−12.309484; sulfonamide product−12.116446 kcal/mol. Both sulfonamide TS quantities remain absent while its recovery runs. No new organic job was submitted this round.

- Author profile15.7/12.9 and local13.0/10.2 (subtract2.7) are separate quantities. There is no cis/trans competitor gold for these substrates.
- Original TfOH has−330.7943cm−1 and is not accepted as a minimum. Both zero-imaginary recovery branches retained; their profile offset is qualified rather than silently replacing author gold.
- HFIP epsilon16.70 plus remaining2-propanol SMD parameters;293.15K1atm. Gas-Gcorr wording versus solvent-optimization prose remains ambiguous. Author GaussianA.03 versus installedC.01 disclosed.
- Current sulfonamide TS recovery and acid IRC remain pending; no whole-paper pass and no further same-cause retry without new evidence.

current_scope_verified=false; no acceptance_candidate. This round adds0 actual jobs for this paper; 0 completed endpoints were individually audited. Platform/native statuses remain separate. Complete author/actual/difference and mandatory-ID coverage: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/paper_5d9fa6b2dd23daf1/verification_report.md, energy_comparisons.json, comparison.csv, state_comparison.csv, coverage.json. Recovered TS proof: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/recovered_TS_acceptance.json. IRC/endpoint and atomic mapping: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/irc_direction_audit.json, endpoint_chemical_audit.json, endpoint_fragment_mapping.json. Exact jobs and readback: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/submission_receipts.json; /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/final_readback/inventory.json. Finite handoff/ETA: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/status_review_20261017T1137Z/new_group_03/handoff.json; /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/advance_feasible_20261017T1145Z/new_group_03/eta.json. No task/input/scoring/tolerance/qualification/gold/expert/zip change. No periodic resume.


## Local native preflight and single-canary repair (2026-10-17T1210Z,new_group_03)

Acid forward IRC hpc-job-46ee74f0-5604-46b3-a4b2-fc718fa06503 has now failed native L123 corrector convergence after about4.47h; retain its partial path. Sulfonamide TS recovery remains active at this round snapshot. No new organic job submitted.6/8 energy quantities remain available; source profile15.7/12.9 and local13.0/10.2 stay separate, with no cis/trans competitor gold.

One representative original failure was reproduced locally under2CPU/180s/sharedflock. Fresh accepted-TS RCFC reverse input changes only numerical step10→5, keeps MaxCycle20; native startup and3SCF iterations confirmed, but controlled180s timeout(rc−9),0SCF Done and no nonzero path point. FCHK identity/Hessian audit passed subsequently. Exactly1HPC canary submitted:hpc-job-cc60ae34-bd88-4cce-a25a-e5db9a7ff01a;latest platform/native:RUNNING/NATIVE_RUNNING;rollout=false. No successful stage repeated, no active job canceled. The platform-failed Mn1-tBu/S chain only finished endpoint optimization; its later internal frequency job is truncated, not accepted. Frequency-only recovery geometry preserved. Full evidence/coverage:/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/local_preflight_repair_20261017T1210Z/new_group_03/paper_5d9fa6b2dd23daf1/verification_report.md,/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/local_preflight_repair_20261017T1210Z/new_group_03/local_preflight.json,checkpoint_geometry_audit.json,failure_inventory.json,partial_stage_salvage.json,canary.json. Handoff:/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261017/local_preflight_repair_20261017T1210Z/new_group_03/handoff.json. Source qualification,40reserved points,all gold,tolerance and task/scoring definitions unchanged. current_scope_verified=false; no automatic resume.


## Native-return review (2026-10-18T0200Z,new_group_03)

6/8 energy comparisons remain available; no full-question candidate. Sulfonamide continuation exhausted160 further optimization cycles: force convergence passes but displacement fails, with no completed frequency/SP. Acid forward IRC completed32 points then failedL123. Both are terminal failures; no new organic submission or blind cycle extension. Profile15.7/12.9 versus local13.0/10.2, both TfOH minimum branches and source-method ambiguity remain separate and disclosed.

Current scientific question only; no new precursor activation, population, bulk-ee, cis competitor or whole-paper-IRC requirement. Author methods, source candidates and tolerances are retained. Complete rule coverage and all author/computed/absolute/relative differences: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261018T0200Z/new_group_03/paper_5d9fa6b2dd23daf1/verification_report.md; energy_comparisons.json, comparison_all_source_conventions.csv, state_comparison.csv, coverage.json. Native/connection audit: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261018T0200Z/new_group_03/native_audit.json; connection_acceptance.json. Finite handoff: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261018T0200Z/new_group_03/handoff.json. current_scope_verified=false; acceptance_candidates=[]; no periodic resume.

## 2026-10-18 计算阻碍恢复轮（0342Z dispatch）

更新 2026-10-18T04:42:56.251556+00:00。新增整题通过0；不释放任何来源资格或定量保留项。仅对当前科学问题定义必要下一步，完整记录：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/recover_computational_blockers_20261018T0342Z/new_group_03`。

复用6/8能量量、13条驻点/SP链。酸IRC第32个收敛点进入自由端点优化；磺酰胺依据末段能量/位移停滞改用fresh CalcFC+Cartesian，原tight阈值不变，最多40步。合格TS、单虚频、同几何M06/HFIP单点及必要trans连接仍待验收。profile15.7/12.9与local13.0/10.2不混用；无cis/trans竞争gold。

全部新提交均有真实2CPU/180秒本地预检、共享flock和实时共享盘增长门槛；受控timeout不是科学完成。

- `hpc-job-f14851aa-c049-474d-a730-47bcea01f117`：TS_acid_forward_point32_endpoint01；平台QUEUEING，原生NOT_STARTED。
- `hpc-job-d9f6a37a-00b7-4615-80ba-7be7e4ae3636`：TS_sulfonamide_cartesian_calcfc01；平台QUEUEING，原生NOT_STARTED。

目前不增加有效科学结果计数；无自动恢复、无同因批量推广、无旧作业取消。

## 2026-10-19 原生返回核收与有限接续（0035Z）

更新时间 2026-10-19T00:55:25.935684+00:00。新增整题通过0，acceptance_candidates=[]。本轮证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261019T0035Z/new_group_03。原迁移旧ID保持停止，不恢复；平台成功不作为科学成功。

b6b81dcc虽平台SUCCEEDED，磺酰胺Cartesian/CalcFC搜索24SCF、12523.36秒后由停滞保护停止；末端MaximumDisplacement0.000514对原阈值0.000060，未收敛，freq/SP均未执行。该支路客观暂停；不放宽阈值、不改方法追数值。
d6ffe342虽平台SUCCEEDED，酸正向端点opt100SCF、15593.50秒达到步数上限。C1–C24从3.094Å至12.347Å持续解离；片段映射为独立acid与Ad+，重原子RMSD0.01122和0.000353Å。不要求虚构束缚超分子最小值；复用已有独立反应物，仅提交未执行的反向产物侧IRC/opt/freq。6/8能量量、13条驻点/SP链保持；profile15.7/12.9与local13.0/10.2分开，无cis/trans竞争gold。

实际本地2CPU/180秒、4GB、共享flock预检均进入原生SCF/IRC，0个完整SCF，timeout只证明启动，不是修复完成或推广许可。每种独立原因只提交一个HPC代表。
- 新作业hpc-job-23ae8cca-1288-42d0-92b6-faf77d5d9d78：TS_acid_reverse_missing01，QUEUEING；CPU资源-2，优先级6，20CPU/100GiB。

逐项作者值/自算值/误差/全部来源候选与规则覆盖见本轮author_comparison.json、coverage.json及各论文verification_report.md；无整题候选，不调整评分/任务/正式资格。

## 2026-10-19 存储恢复与端点验收（0530Z）

UTC 2026-10-19T06:33:07.017542+00:00。证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/storage_recovery_20261019T0530Z/new_group_03。本轮新增提交0、停止0、整题通过0，acceptance_candidates=[]。

实时核对迁移后08a325fb（旧23ae8cca）：RUNNING，原生IRC截至2026-10-19T06:33:00.004837+00:00已有65SCF、最高打印收敛点20；无正常/错误退出，opt/freq尚未执行。正式input/日志20CPU/80GB，平台20CPU/100GiB。健康作业保留，停止迁移源不恢复。本组未见ENOSPC、配额错误或shared-output保护中断。前轮磺酰胺flat-energy/位移停滞与酸正向解离属于数值/物理路径问题，不改称存储故障。酸产物闭环/H/电荷/trans待返回，磺酰胺TS/freq/SP暂停。6/8对照复用；profile15.7/12.9和local13.0/10.2分开，无cis/trans竞争gold。

本轮无Create，实时双区容量/配额/账号CPU/存储承诺准入不适用，未宣称新准入成功。后续Create须按最新AGENTS锁下核查所有门槛。详见本轮endpoint_acceptance、coverage、jobs、failure_classification和handoff；不等待长作业、不自动恢复。

## 2026-10-19 定性准则核收与有限接续（1200Z）

UTC 2026-10-19T12:21:33.710405+00:00。本轮证据目录：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/new_group_03。仅本组两个论文、一个HPC canary、无停止/迁移/自动恢复。

仍INCOMPLETE，6/8能量量及13条有效链复用；磺酰胺TS/freq/SP和酸产物闭环/H/电荷/trans证据不足。旧作业hpc-job-08a325fb-84de-4026-b3bf-22b847b6fd7e平台SUCCEEDED但原生112SCF、33个收敛非零IRC点后21609.283秒受控walltime终止，无Normal，opt/freq未执行；第34未完成点不接纳。取哈希未变日志第33点（E=−775.347857218Eh，C3−C24=1.589568Å）做无约束端点优化/频率，未重复原IRC。

真实共享flock本地预检2CPU/4GB/180秒到达SCF，0完成SCF，timeout不是科学成功，仅作为单HPC启动门槛。已提交hpc-job-20868262-1d96-41d0-bcfd-6f397ed2c6e0，实时RUNNING，native=RUNNING；正式20CPU/80GB，平台20CPU/100GiB，人工智能驱动谱学研究，priority6。提交前锁内双区精确适配数均0，按既有授权queue_only提交并留全容量/配额/账号/存储/去重证据；后已启动。

原IRC CHK在formchk检查前后观察到哈希差异，原因未确证；保留两哈希与原始记录，不使用该CHK重启或guess；新输入来自已校验日志。源版本SIp91ref29为G16A.03，实际C.01，不声明完全一致；TableS21热项标题歧义保留。FigureS3 profile15.7/12.9与local13.0/10.2严格区分，该底物对无cis/trans竞争gold。磺酰胺无新故障诊断，不盲重试。

原任务、评分、gold、容差、40分保留及发布位置均不变。候选由父级复核；历史失败/部分记录不回写为成功。

## 2026-10-20 酸端点验收与单点接续（0220Z）

UTC 2026-10-20T02:36:24.404339+00:00。本轮证据目录：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03。

本轮接受hpc-job-20868262-1d96-41d0-bcfd-6f397ed2c6e0的酸反向point33后继端点：原生Opt38SCF/9477.905秒、Freq1SCF/2091.780秒，均exit0/Normal，tight四项YES，123个正频最低33.1556cm^-1。opt/freq同几何RMSD9.45e-16Å，point33到首opt几何RMSD2.77e-15Å。C3–C24由TS2.119355Å缩至1.551363Å，C1–O16由3.041063Å缩至1.521800Å，形成五元内酯环。H18保留于O17（0.979025Å），C16H25O2+单重态，形式正电荷分配于O17。移去H18的结构投影与已接受中性trans内酯具有相同isomericSMILES/原子手性映射；该投影不是新优化或去质子化势垒。

酸TS的反应物侧沿既有解离轨迹映射acid+Ad+并复用独立合格片段，产物侧为33个收敛IRC点+连续无约束优化的质子化trans内酯。旧IRC仍为6h受控中断，不升级成收敛IRC；解离43原子supermolecule仍非束缚极小值。质子/电荷账本：[C16H25O2]+ + OTf- -> C16H24O2 + TfOH，总原子与电荷守恒，不声称已算去质子化活化势垒。

为完成该新中间体作者M06能量，仅提交hpc-job-76a49b6c-2980-47c8-824e-8f98500c0bf6：M06/def2TZVP、SMDHFIP eps16.70、已验收频率日志10位小数archive几何；不读CHK、不重复Opt/Freq。真实共享flock2CPU/4GB/180秒预检进入SCF后到限，0完成SCF，不是科学成功。正式20CPU/80GB、平台20CPU/100GiB、priority6、人工智能驱动谱学研究。锁内双区精确适配CPU2=0、HPCnet2=200，选HPC可上网区资源2；HIGH RUNNING858CPU，扣除承诺后存储946.9375GiB，硬帽2GiB。初/早期API与原生读回见jobs.json，当前RUNNING/RUNNING。

整题仍INCOMPLETE。6/8既有能量对照复用；磺酰胺TS/freq/SP与局部/全profile势垒缺失，flat-energy/位移停滞无新诊断不盲重提。FigureS3 profile15.7/12.9和local13.0/10.2不混用，无cis/trans竞争gold。G16作者A.03/实际C.01及TableS21热项歧义继续披露。

仅更新两模式计算参考和manifest；任务、评分、gold、容差、final/hold位置不变。详见endpoint_acceptance、acid_path_ledger、method_comparison、paper_assessments、jobs、failure_classification与handoff。有限轮次后退出，无定时恢复。

新单点spec的source_label/reference_source_terms承袭起始TS1-3a，仅为祖先来源；不是本次质子化极小值的作者gold。以source_geometry_provenance和endpoint_acceptance为新状态依据，详见/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_5d9fa6b2dd23daf1/verification_followup_20261020T0220Z/protonated_trans_lactone_M06_sp01/provenance_clarification.json。运行中spec/input/runner未改。

## 2026-10-20 新单点返回事件核收（sp_return）

当前状态（2026-10-20T02:59:50.554983+00:00）：INCOMPLETE，两模式一致。新SP hpc-job-76a49b6c-2980-47c8-824e-8f98500c0bf6 已原生Normal/exit0并完成独立核收；质子化trans内酯Opt/Freq/SP链完整。原8项能量比较仍6/8，磺酰胺TS/freq/SP及对应势垒比较仍缺。最新证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03_sp_return。下方既往pending/RUNNING描述仅为注明日期的历史快照，由本节及文末新事件记录替代。

M06/def2TZVP、SMD自定义HFIP（2-propanol参数/Eps16.70）、+1单重态、43原子C16H25O2；原生12周期单次SCF，230.221927秒，Normal/exit0。E=-774.820293529 Eh，复用已接受B3LYP热项+0.348360 Eh，G=-774.471933529 Eh。parent频率archive→input→SP archive全精度最大坐标差0；输入/spec/runner及前置日志哈希匹配。平台SUCCEEDED、2026-10-20T02:39:19Z资源释放，3实例Deleted；原生成功独立于平台状态确认。

相对acid+Ad+为-13.938787625、相对酸TS松弛-26.911562692 kcal/mol。平衡去质子化ΔG(TfOH minus/plus)=-2.592301250/-2.592314428 kcal/mol；完整质子化profile=-9.717182623/-9.717169446，接去质子化均闭合到中性产物-12.309483873880。以上为热力学，未算去质子化活化势垒，无新中间体作者gold。祖先TS标签仅作来源，不能当新态数值目标。

H18/O17与trans映射复用已合格端点；33点IRC前缀+连续优化的限定及失败解离超分子记录保留。13条原有效能量链加1条新质子化链共14条；8项原对照仍6项可用。FigureS3 profile15.7/12.9与local13.0/10.2分别保留；原±2.0容差、无cis/trans竞争gold、G16A.03/C.01和SI热项歧义不变。磺酰胺无新技术诊断，不盲续算。

本事件新提交0、停止0、成功阶段重算0、整题新候选0；仅参考/manifest更新。完整输入/日志哈希、逐项作者/自算/差值、循环与覆盖见 /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03_sp_return/native_SP_acceptance.json、/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03_sp_return/energy_assembly.json、/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/new_group_03_sp_return/paper_assessments.json。


## 2026-10-20 07:10Z 精确作者TS新证据恢复

当前状态（2026-10-20T08:05:56.623282+00:00）：INCOMPLETE，两模式一致。作者TS1-3s完整61原子源坐标已独立核实；缺的是本验证验收的完整曲率/反应模、自身M06及相称局部连接，不是缺作者TS。用户授权的一次固定源Force→Freq诊断已实际提交 hpc-job-75bd7738-db68-4d30-a8ca-428b2a0e87b5，平台RUNNING、原生RUNNING。额外Opt=Tight位移或完整IRC不再误作作者要求；原失败记录仍失败。酸成功链与6/8旧对照复用。

源证据：SI S79–80方法、S81 TableS21、S86 TableS22。新独立提取TS1-3s与既有source.xyz及此次输入逐元素/坐标完全一致，maxdiff0Å；C23H34NO2S，+1/1为已有闭壳层重构。作者B3LYP E=-1500.569402Eh，IF=-138.6cm^-1。旧源首SCF=-1500.56940199，广义力max/RMS3e-6/1e-6；Cartesian max/RMS4.763e-6/1.496e-6Eh/bohr。能量接近和小力仅支持新曲率诊断，不能冒称Tight四YES或整题通过。

实际本地共享flock2CPU/4GB/180秒固定源Force预检进入SCF周期1后受控超时，0完整SCF；只通过解析/模型/启动门。锁内实时双区精确20CPU+100GiB适配CPU资源-2=0、HPC可上网区资源-2=228，选HPC-可上网区资源-2；HIGH运行1078.0CPU，扣存储承诺后600.530GiB。作业人工智能驱动谱学研究/priority6/平台20CPU100GiB、Gaussian20CPU80GB，硬输出2GiB。原生已确认B3LYP/def2TZVP、SMD2-propanol参数/Eps16.70、61原子/+1 singlet。

唯一HPC仅一次固定源Force（硬1h）及条件Freq（硬4h），无Opt/旧CHK。完整Force+SCF正常且保守小梯度启动门无矛盾后才进入Freq；启动门不是作者阈值或最终驻点验收。需核收177模、唯一化学负模/全部软模、反应方向（C3-C20、C1-N43、N43-H44）、同几何热项。未执行M06；prepared source_m06.gjf须曲率及化学模式核收后才有据执行。必要连接限当前主张的有限双侧测试/端点，不增设固定IRC长度、cis竞争或去质子化活化势垒。原重复160步优化不会再次执行。

原14条有效链、6/8能量比较保持。FigureS3 profile15.7/12.9与local13.0/10.2分别保留，原±2.0不变；TableS21 gas热项/HFIP文字歧义及G16A.03/C.01差异披露。d142两模式已登记暂定通过不重算。新证据见 /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0710Z/new_group_03/source_and_scope_review.json、/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0710Z/new_group_03/jobs.json、/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0710Z/new_group_03/return_acceptance_checklist.json、/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0710Z/new_group_03/handoff.json。本轮只一个诊断作业、无停止、无新增通过；有限交接后退出，无周期恢复。


## 2026-10-21 作者源TS核收与最少后继（035151Z）

当前状态（2026-10-21T04:30:33.473916+00:00）：INCOMPLETE，两模式一致。作者TS1-3s源Force/Freq已独立验收：61原子、极小力、177模且唯一化学负模−138.5952cm^-1，Gcorr0.476590Eh。已实际提交自身M06及有限双向端点测试，原8项能量仍6/8可用。不重复成功Force/Freq或TS优化；d142保持已登记、不改不重算。

亲自核收75bd7738输入/spec/runner/源文件/原生日志哈希、API已释放全部实例Deleted。Force500.458秒、Freq8116.965秒均exit0/Normal。E(B3LYP)=-1500.569401990Eh对作者-1500.569402，差+1.0e-8Eh；Cartesian max/RMS force4.763e-6/1.496e-6Eh/bohr。完整177模、唯一负模-138.5952对-138.6，差+0.0048cm^-1；正软模10.7126/18.0941/25.6405/27.2415/39.2793。自身Gcorr0.476590Eh与作者值差0；温度293.15K、1atm。精确源、Force、Freq几何最大坐标差0。按真实力/曲率接受固定作者TS，不伪造额外Opt=Tight四YES。

唯一负模的正向0.15Å归一位移：C3–C20由2.092921缩到1.987107Å，C1–N43由3.101394缩到3.085092Å，反向分别增至2.198757/3.117699Å；N43–H44基本保持。加预期C–C/N–C边并去H44仅作中性结构映射，与已接受trans吡咯烷产物同图，两中心有序体积符号均同。该拓扑投影不是新计算端点、去质子化势垒或完整IRC。

实际后继：sp=hpc-job-13e3e0ec-d05b-4d75-8574-aa6f484a6905（RUNNING/RUNNING）；local_endpoints=hpc-job-6d1d66e5-5a3b-4912-9970-2318016fc28f（RUNNING/RUNNING）。每次在双共享锁内按实时两区精确CPU/RAM适配、quota、账号/排队、存储增长承诺、科学身份去重完成准入，项目人工智能驱动谱学研究/priority6/平台20CPU100GiB/原生20CPU80GB。M06与端点各做真实2CPU/4GB/180秒本地预检，仅确认输入/模型进入SCF，未冒称收敛；详细结果及容量快照见jobs.json和各attempt/submission_preflight。端点用唯一负模±0.15Å、无约束默认Opt(maxcycles60,maxstep10)+Freq，每侧硬6h；独立方向失败不会吞掉另一侧或M06成功证据。不是重做TS、不是统一完整IRC门，不要求解离反应物必成束缚极小值。

同源力实测8.34分钟、Freq135.28分钟；M06参考旧43原子230秒和61原子Force500秒估约5–20分钟；端点预期数小时/侧、无整题完工承诺。以实际返回再核收，不空等长作业或自动重启。此轮新增整题候选0；尚缺见coverage.json。原14条完整能量链与酸闭环、所有旧数值/来源差复用；profile15.7/12.9与local13.0/10.2分别保存，±2容差、版本/热项歧义及无cis竞争gold不变。任务/evaluator/评分/发布位置不动。

证据目录：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/feasible_nine_followup_20261021T035151Z/new_group_03。核心文件source_TS_acceptance.json、native_protocol_supplement.json、source_product_mapping.json、author_comparison.json、coverage.json、jobs.json、handoff.json。


## 2026-10-21 M06返回核收（071804Z）

当前核收（2026-10-21T07:43:18.913776+00:00）：两模式 INCOMPLETE。13e3e0ec M06原生正常完成并验收，原能量量8/8、15条完整能量链；局部磺酰胺势垒10.201388对作者10.2，完整profile两TfOH分支14.422993/14.423006对12.9，各自在原±2.0kcal/mol内。6d1d66e5端点仍健康RUNNING；当前实际产品侧结构有成环/trans证据，但尚未Opt/Freq收敛，反向未开始。本轮新增整题候选0、新提交0。

单点作业 hpc-job-13e3e0ec-d05b-4d75-8574-aa6f484a6905：平台SUCCEEDED、实例全部Deleted；原生exit0/Normal，440.415630秒。同61原子作者TS几何最大坐标差0，冻结输入/runner/spec/前置证据和复用能量日志哈希通过。M06/def2TZVP HFIP单点E=-1499.723437740Eh，对作者-1499.723438差+0.000000260Eh；加已验收自身Gcorr0.476590得到G=-1499.246847740Eh。未重复Force/Freq或TS优化。

完整profile为14.422993262/14.423006440对12.9，差+1.522993262/+1.523006440；局部势垒10.201388261对10.2，差+0.001388261。酸局部势垒12.972775068，较磺酰胺高2.771386807，支持作者较低势垒排序。完整profile使用自身离子化自由能4.221605/4.221618，不用作者2.7混减；profile15.7/12.9与local13.0/10.2分开。两个TfOH分支全部保留。原8种量全部在既有±2容差内，但数值覆盖不等于整题完成；净产品自由能-12.309483874/-12.116446272及酸路线直接复用。

局部端点 hpc-job-6d1d66e5-5a3b-4912-9970-2318016fc28f 健康RUNNING。冻结快照有25个SCF；最后完成SCF对应几何C3–C20=1.554003Å、C1–N43=1.555296Å、N43–H44=1.024366Å。按已有原子映射去H44后实际距离图与已合格中性产物同图，两立体中心有序体积符号相同，支持trans产品侧进展。体系仍C23H34NO2S+、+1单重态、N43带H44；去H仅是结构映射，不是计算去质子化。最新完整收敛表maxforce0.000653>0.000450，maxdisplacement0.018404>0.001800，尚未收敛/频率未执行，不能当合格端点。第二侧reactant_minus尚未开始。保留在跑作业及两侧独立阶段，不重复创建。

原方法、S21气相热项脚注/HFIP措辞歧义、G16A.03与实际C.01差异保留；无cis/trans竞争gold，无全IRC/额外Tight门。已登记d142不改不重算。剩余仅相称局部连接/曲率和质子/电荷/trans映射核收，解离反应物允许按独立合格片段映射；不扩展整篇网络或去质子化势垒。实测61原子Freq约2.25h，端点还需若干小时，6h单侧资源界限不是收敛证明或整题ETA。

本轮证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_5d9fa6b2dd23daf1/job_return_followup_20261021T071804Z（new_SP_acceptance.json、endpoint_progress.json、冻结原生日志快照、immutable_evidence_audit.json、author_comparison.json）；交接与coverage/jobs：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_return_followup_20261021T071804Z/new_group_03。不改任务/评分/evaluator/容差/发布位置，不周期恢复。

## 2026-10-21 双侧返回核收与缺失频率（154758Z）

当前核收（2026-10-21T16:10:08.271324+00:00）：AR/PR仍INCOMPLETE。6d1d66e5平台SUCCEEDED但原生exit1；产品Opt已收敛并完成trans/质子映射，频率被6h上限中断；反向60步未收敛，已分离为Ad+与E-磺酰胺。仅补产品固定几何频率，实际作业hpc-job-d4f00824-f463-412a-9263-bcbd86b3ab7b（RUNNING/RUNNING）。8/8能量量和15完整链直接复用，新增整题候选0。

父作业hpc-job-6d1d66e5-5a3b-4912-9970-2318016fc28f原生两段分别审计。product_plus在08:45:07完成优化，四项默认收敛YES：maxforce0.000020、RMSforce0.000003、maxdisplacement0.001121、RMSdisplacement0.000165；随后Freq进入Link703，合计21608.932618s被6h界限终止，rc=-9，无177频率/热项。优化中间Normal不代表完整Opt/Freq成功；本轮已修正readback的final-Normal判定。只接纳成功优化段，不把中断频率放行。

产品体系C23H34NO2S+、+1单重态，C3–C20=1.555639Å、C1–N43=1.554591Å、N43–H44=1.024239Å；实际成键图去H44后与已验收中性产物同图，两中心有序体积符号一致。账本：[C23H34NO2S]+ + OTf- -> C23H33NO2S + TfOH。N–H保留，移除H仅为中性产物结构映射，不声称已算去质子化活化势垒。

reactant_minus原生60SCF、17035.645459s、L9999步数上限，仍不是收敛超分子；终态有两个共价片段，最近原子间4.482921Å、C3–C20=5.628211Å，E烯烃投影cos=-0.9999167。重原子图及逐原子附H数映射到Ad+和中性E-磺酰胺。Ad+重原子RMSD0.001042Å；磺酰胺整体1.472425Å，构象不同，不能声明同一最低点，所有匹配重原子键长最大差0.004367Å。这里支持反应物化学身份，不用未收敛超分子的能量/热项代替已合格独立反应物。复用独立最低点参考，不强求解离体系收敛为束缚复合物、不延长60步作业。

检查点限制：product_plus.chk在formchk读取后观测哈希与原manifest不符，原因未确认；reactant_minus.chk哈希仍匹配。原记录及差异均保留。后继不读取该CHK、不用其guess；使用哈希未变的成功Opt日志archive精确坐标，独立SCF+Freq。所提频率任务不含Opt、TS优化或M06，前置日志/坐标/spec/runner哈希核验；4h单独预算基于同61原子Freq实测8116.965s。预检分类CONTROLLED_TIMEOUT_STARTUP_ONLY，真实测试=True；详见failure_classification，不把180秒启动测试称完整频率稳定。

唯一新作业hpc-job-d4f00824-f463-412a-9263-bcbd86b3ab7b：项目人工智能驱动谱学研究、priority6、20CPU100GiB（Gaussian20CPU80GB），实时双区适配节点{'CPU资源-2': 16, 'HPC-可上网区资源-2': 203}，选HPC-可上网区资源-2；配额/账户/存储承诺/去重在共享锁内核查，原生首查及批末状态写jobs.json。无停止健康作业、无周期恢复，不等待长期作业。返回后仅核177模/低频及必要曲率，若负模或真实失败则按原因处理，不能自动通过。

能量不重算：磺酰胺完整profile14.422993262/14.423006440对作者12.9，差+1.522993262/+1.523006440；局部10.201388261对10.2，差+0.001388261。酸局部12.972775068，较磺酰胺高2.771386807；产品净自由能-12.309483874/-12.116446272。8种量均在原±2kcal/mol内，15条完整链；不混用profile15.7/12.9与local13.0/10.2。G16A.03/实际C.01、HFIP方法与S21气相热项脚注限定及两个TfOH分支全部保留。无cis竞争gold，不要求完整IRC/额外Tight或整篇网络。d142已登记，未改未算。

本轮科学证据：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_5d9fa6b2dd23daf1/job_progress_resume_20261021T154758Z。控制/coverage/逐项比较/jobs/候选/ETA/交接：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_progress_resume_20261021T154758Z/new_group_03。仅5d9两模式reference及manifest更新；不改题面、评分、容差、发布位置或其他论文。

## 2026-10-22 产品频率与当前整题候选（013509Z）

当前结论（2026-10-22T01:44:39.244416+00:00）：5d9在AR/PR同一科学问题的最小必要计算证据已齐备，提出PROVISIONAL_PASS_QUALITATIVE候选，待父级独立审查登记；尚未登记通过。d4f00824原生exit0/Normal、177正模、最低22.5973cm^-1，同优化archive几何差0；自身Gcorr0.487233Eh。8/8原能量量在原±2容差内、15条能量链复用；产品频率仅补足局部极小值证据，不新增M06能量链。新计算提交0。

最新作业hpc-job-d4f00824-f463-412a-9263-bcbd86b3ab7b：平台SUCCEEDED、已释放且实例全部Deleted；原生exit0，最终Normal，6966.020854秒。冻结input/spec/runner/前置日志与返回日志哈希核对通过。B3LYP/def2TZVP、SMDHFIP eps16.70其余2propanol、293.150K1atm、61原子/+1单重态；频率archive与成功Optarchive坐标最大差0。177模全部正，低于50cm^-1者22.5973/25.7551/39.9981/45.5594；无负模。E_B3LYP=-1500.613999760Eh，与成功优化一致；Gcorr=0.487233Eh，B3LYP层G=-1500.126766760Eh。该G不是M06复合能，未替换TS或中性产物热项，未生成无计算的endpointM06。

C3–C20=1.555639Å、C1–N43=1.554591Å、N43–H44=1.024239Å；N质子化产品图去H44后与独立合格trans中性吡咯烷同图，两中心手性符号一致。账本[C23H34NO2S]+ + OTf- -> C23H33NO2S + TfOH，未声称计算去质子化势垒。反向复用±0.15Å源负模出发的局部下降：两分离共价片段，最短间距4.482921Å；Ad+重原子RMSD0.001042Å，E-磺酰胺图及附H匹配、E投影cos=-0.9999167。后者RMSD1.472425Å构象差明确披露；60步失败超分子不是最低点或热项来源，能量采用已验收独立反应物。

C_PATH由原酸路线/质子化trans内酯证据，加本次磺酰胺作者源TS力/单负模、局部反向片段身份和产品Opt+177正频率支持。C_COMPARISON由自身M06复合能量支持：磺酰胺局部10.201388低于酸12.972775，两者差2.771387kcal/mol；两净产物形成-12.309484/-12.116446均放能。只验证当前两底物问题；无全IRC、cis竞争、更多构象普查、完整催化网络、实验速率/收率或机制唯一性主张。

全部作者/计算/带符号差值如下（kcal/mol；原容差均±2.0，两TfOH分支保留，不挑选）：

| 量 | 作者 | 自算 | 差值 |
|---|---:|---:|---:|
| KP_ETHER | 1.4000 | 1.455475 | +0.055475 |
| KP_CATION | 2.7000 | 4.221605 | +1.521605 |
| KP_CATION | 2.7000 | 4.221618 | +1.521618 |
| KP_TS_ACID | 15.7000 | 17.194380 | +1.494380 |
| KP_TS_ACID | 15.7000 | 17.194393 | +1.494393 |
| KP_TS_SULF / TfOH_modeminus | 12.9000 | 14.422993 | +1.522993 |
| KP_TS_SULF / TfOH_modeplus | 12.9000 | 14.423006 | +1.523006 |
| KP_LOCAL_ACID | 13.0000 | 12.972775 | -0.027225 |
| KP_LOCAL_SULF | 10.2000 | 10.201388 | +0.001388 |
| KP_PRODUCT_ACID | -12.3000 | -12.309484 | -0.009484 |
| KP_PRODUCT_SULF | -12.1000 | -12.116446 | -0.016446 |


profile与local严格分开：作者15.7/12.9减2.7得到13.0/10.2；自身完整profile使用自身离子化基准4.221605/4.221618，不能混用作者2.7。当前8/8数字容差通过不冒称官方分数或无条件STRICT_NUMERIC_PASS；暂定候选保留来源和实现限定，最终登记由父级独立审查。

方法限定：SI方法溶剂优化/频率措辞与S21气相热项脚注歧义仍未解决；本题author_guidance明确要求声明重构，本验证采用HFIP谐频热项。源TS自身Gcorr0.476590与作者打印值一致只是支持证据，不证明隐藏输入。作者G16A.03/实际C.01，网格/阈值和闭壳层声明保持。旧CHK经formchk后哈希差异保留未定因，新Freq使用未变Optarchive+freshSCF，不读取旧CHK；坐标字段标签澄清见上一轮coordinate_provenance_clarification。历史失败不会改称成功。

证据目录：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_5d9fa6b2dd23daf1/job_progress_resume_20261022T013509Z；native_frequency_acceptance、current_scope_acceptance、method_fidelity、author_comparison、reused_energy_hash_audit以及coverage。控制/真实jobs/候选/失败分类/ETA/交接：/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_progress_resume_20261022T013509Z/new_group_03。本轮1篇、2模式候选，新增登记0、新提交0、停止0、成功重算0；d142未动、保持已登记。父级审查前不改全局数、不改题面/评分/容差/专家副本/final-hold位置。不等待HPC、不周期恢复。

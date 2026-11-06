<!-- SCIENCE_V2_20261021 -->
# 现行科学分V2评分状态 — 2026-10-21

本次只迁移评估协议，不新增量化计算。当前paper_science_v2为100分独立二元科学项；reference_qualification.json允许评分，publication release_ready=false。父级2026-10-20暂定定性验收保留；严格数值整题通过=false。下文历史“无新容差/正式评分待定”等只描述当时状态，现行门槛以scoring_rules.json为准，不覆盖下文计算事实。

- 首步复合G反号仍未恢复；r_first_barrier按1.9±1.0严格失败，不能以低层PES替代。
- 三重态正文73.9/SI74.1/印刷SCF组装有来源冲突；精确三重态值排除出数值评分，稳健排序可评分。
- TS1有限位移端点连接非完整IRC/MEP；不据此推断精确速率。

逐规则原文PDF页/hash、定义、原值/验证差异及设计理由见science_v2_evidence_review.json。

---

# Latest verification — returned calculation review 2026-10-20

Updated UTC: 2026-10-20T02:51:32.174833+00:00

**Mode: autonomous_research; scientific status: PROVISIONAL_PASS_QUALITATIVE; current_scope_verified: true.**

Parent independently reviewed and registered this mode as PROVISIONAL_PASS_QUALITATIVE at2026-10-20T02:34:18.917879+00:00. This is an accepted provisional scientific verification, not a pending candidate, strict numerical pass, official scoring decision or release. Numerical differences and task-permitted evidence limitations remain disclosed.

Parent decision: [/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/original_group_01/parent_acceptance_decision.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_followup_20261020T0220Z/original_group_01/parent_acceptance_decision.json). Only decisions for this paper and named mode apply. No global acceptance count is modified by this update.

## Current evidence and scope

父级2026-10-20已独立审查并登记两模式PROVISIONAL_PASS_QUALITATIVE，本轮同步正式reference与coverage，不重复计算。首步复合自由能−1.219118236对+1.9，原±1.0仍失败；低层PES势垒+1.215793331和两侧合格最低点支持定性易重排。TS1有限位移连接不冒称完整IRC/MEP或速率；第二步4.574283671对4.6及同参照C4/C5排序保持。

NewjobIDs: none. ActivejobIDs: none as of 2026-10-20T02:46:23.050189+00:00.

Nextaction: 本轮验收同步结束，无待算项目；保留父级已登记定性暂定通过和原数字/有限连接限制，不重提候选、不追数。

## Author method comparison

| Field | Author definition | Actual evidence | Finding | Source |
|---|---|---|---|---|
| functional/basis/dispersion | (U)B3LYP/6-31G(d) gasOpt/Freq; noD3 | Native nine retained nodes match; sourceM062X/def2SVP triplet andB3LYP/6-31+G(d,p) redox treated as separate protocols | MATCH | SI80§9.3;SI67§9.1;SI76§9.2 |
| own high/solvent | wB97XD/def2-TZVPP SMD DCM; triplet wB97XD/aug-cc-pVTZ CPCM DCM; redox CPCM MeCN | Actual routes/own geometry audited; MeCN electrode properties are not relabelled DCM | MATCH | SI67,76,80 |
| composition/state | C26H36BNSi65atoms; rearrangement+1doublet;neutral2a/3a0singlet;triplet0/3 | All retained nodes inventory/frequencies verified;redoxanion-1doublet separate | MATCH | SI§9.1–9.3 and current molecular inventory |
| temperature/thermal/reference | Rearrangement unscaled standard harmonic298K/1atm; no qRRHO | Existing native298.15K terms replayed from own frequencies at298K; nativeT replay agrees within2e-6Eh. Only RRHO column used. Both originalradical and actualTS1basin references retained separately | MATCH_AFTER_EXPLICIT_ANALYTIC_REPLAY | SI80 |
| connection route | Source IRC | TS2/alternative actualbidirectionalIRC;TS1 documented exact±0.15Å normalmode seeds plus endpointOpt/Freq and exact continuation joins, allowed by currenttask equivalentclause. Plus seed initially3.353731kcal/mol above saddle, then relaxes to correct lowerbasin; not monotonicIRC. Int1 finite torsional continuation/free release joinsTS2 basin without claiming a torsionalbarrier | DISCLOSED_TASK_PERMITTED_NUMERICAL_EQUIVALENT | SI80;currenttask;BN_connection_qualification.json |
| software/numerics | Gaussian16;revision/grid/optimizer thresholds not explicit in computationalsection | Gaussian16C.01; older defaultSCF and newerTight/UltraFine disclosed; no extra dispersion | REPORTED_UNSPECIFIED_FIELDS | Native route/header evidence |
| activation quantities | SCE4.422V/23.061kcal mol-1V-1;electronictriplet ordering | Eox1.096788954/Ered-2.690704599V;triplet79.631071485kcal/mol; source73.9/74.1 andprintSCF definition conflict retained, no thermal fit | DEFINED_QUALITATIVE_ORDERING_MATCH | SI67/76;main7 |

## Numerical comparisons and native-stage details

## 作者与本地数值

| 量 | 作者 | 本地 | 本地−作者 | 单位 | 原容差 | 原数值判定 |
|---|---:|---:|---:|---|---|---|
| Eox vsSCE MeCN | 1.1 | 1.096788954 | -0.003211046000000106 | V | None | None |
| Ered vsSCE MeCN | -2.69 | -2.690704599 | -0.0007045990000000835 | V | None | None |
| TS1-own basin | 1.9 | -1.219029549 | -3.119029549 | kcal/mol | None | False |
| TS2-Int1 | 4.6 | 4.574769974 | -0.025230026000000016 | kcal/mol | 1.5 | True |
| TS-A common | 6.3 | 6.264583957 | -0.035416042999999675 | kcal/mol | None | None |
| TS-B common | 5.3 | 5.312790137 | 0.012790137000000534 | kcal/mol | None | None |
| Int-A common | 1.0 | 1.240592505 | 0.24059250499999996 | kcal/mol | None | None |
| Int-B own endpoint common | -40.7 | -43.953355177 | -3.253355176999996 | kcal/mol | None | None |
| C4 Int2 own endpoint common | -37.4 | -36.22330442 | 1.1766955800000005 | kcal/mol | None | None |
| substrate triplet electronic gap; source main | 73.9 | 79.63107148541678 | 5.731071485416777 | kcal/mol | None | None |
| substrate triplet electronic gap; source SI | 74.1 | 79.63107148541678 | 5.531071485416788 | kcal/mol | None | None |
| substrate adiabatic electronic triplet gap | None | 79.63107148541678 | None | kcal/mol | None | None |
| substrate electronic gap minus sensitizer59.8 | None | 19.831071485416786 | None | kcal/mol | None | None |
| substrate electronic gap minus sensitizer61.8 | None | 17.831071485416786 | None | kcal/mol | None | None |

298K全精度RRHO回放是当前比较；上表旧打印/298.15K行仅保留历史证据：

| 量 | 作者 | 当前298K | 差 | 原复现容差 |
|---|---:|---:|---:|---:|
| TS1_own_basin | 1.9 | -1.219118236044925 | -3.119118236044925 | 1.0 |
| TS2_source_Int1 | 4.6 | 4.574283671083314 | -0.02571632891668596 | 1.0 |
| alternative_common_original_radical | 6.3 | 6.2645012467046675 | -0.035498753295332364 | None |
| TS1_minus_common_own_basin | -8.0 | -9.88577234340281 | -1.8857723434028095 | None |
| Int2_source_common | -37.4 | -38.83651273424306 | -1.4365127342430597 | None |

## 本轮实际工作与恢复条件

本轮验收同步结束，无待算项目；保留父级已登记定性暂定通过和原数字/有限连接限制，不重提候选、不追数。

新作业0；本组该篇活动作业0。原日志/CHK保留，成功阶段未重算。

[方法逐项对照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/author_method_manifest.json) · [原生与复用证据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/reuse_inventory.json) · [完整数字](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/numerical_comparison.json) · [后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/successor.json)


## Current mode evidence

[Mode coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/coverage.json) · [Reuse inventory](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/reuse_inventory.json) · [Jobs](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/jobs.json) · [Failure classification](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/failure_classification.json) · [Finite successor decision](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261020T0220Z/successor.json)

Current task instructions, molecular inputs, scoring rules, numerical tolerances, qualification rules and release status remain unchanged. Package integrity validation is not scientific acceptance. Historical status statements below are superseded by this dated header for this mode; all prior failed evidence and numeric residuals are retained.

---

# Prior verification snapshots

# Latest verification — qualitative followup 2026-10-19

Updated UTC: 2026-10-19T12:48:15.243831+00:00

**Mode: autonomous_research; status: PROVISIONAL_PASS_QUALITATIVE; current_scope_verified: true.**

This is a provisional scientific verification candidate for parent review only when stated above. It is not strict numerical agreement, an official scoring pass, release or publication. Original task, evaluator, targets and tolerances remain unchanged. Failed, unfinished or nonstationary required calculations are never accepted under the new policy.

作者电子结构/溶剂/物种与本题所需路线支持一致；统一298K RRHO后首步复合自由能−1.219118236对+1.9，差−3.119118236，仍超复现原±1.0。低层PES实际势垒+1.215793331、单虚频−128.7148；两侧真实模式位移经完整最低点验证得到起始自由基阳离子/Int1。第二步4.574283671对4.6；共同零点C5替代5.923755764高于C4相关鞍点−1.219118236/−6.547999451。Int1有限构象连接、C4端点/中性产物及电子守恒证据复用。负复合能差不反转本题易重排与C4优先结论，不解释成负速率势垒。自主模式活化电位/三重态能量排序亦支持B氧化与排除能量转移。两模式提出暂定候选，严格数值未通过。

## Current mode boundary

The negative composite first-step free-energy offset is disclosed, not converted to an absolute value or re-zeroed. The low-level PES has a positive1.215793331kcal/mol saddle barrier and the intended single negative mode. The finite±0.15Å mode-displacement test ends in two qualified minima; the positive seed initially lies3.353731kcal/mol above the saddle, then relaxes. This is the current task-permitted equivalent connection, not an IRC/MEP or a kinetic rate certificate. TS2 and alternative branches have actual IRC. The finite Int1 conformational connection and released basin support continuity without claiming a new torsional barrier. All required node types, atoms and electron balance are covered. Autonomous activation constraints are separately supported by source-defined redox and electronic triplet comparisons; they are not added to reproduction scope.

## Method and native evidence

| Field | Author definition | Actual evidence | Finding | Source |
|---|---|---|---|---|
| functional/basis/dispersion | (U)B3LYP/6-31G(d) gasOpt/Freq; noD3 | Native nine retained nodes match; sourceM062X/def2SVP triplet andB3LYP/6-31+G(d,p) redox treated as separate protocols | MATCH | SI80§9.3;SI67§9.1;SI76§9.2 |
| own high/solvent | wB97XD/def2-TZVPP SMD DCM; triplet wB97XD/aug-cc-pVTZ CPCM DCM; redox CPCM MeCN | Actual routes/own geometry audited; MeCN electrode properties are not relabelled DCM | MATCH | SI67,76,80 |
| composition/state | C26H36BNSi65atoms; rearrangement+1doublet;neutral2a/3a0singlet;triplet0/3 | All retained nodes inventory/frequencies verified;redoxanion-1doublet separate | MATCH | SI§9.1–9.3 and current molecular inventory |
| temperature/thermal/reference | Rearrangement unscaled standard harmonic298K/1atm; no qRRHO | Existing native298.15K terms replayed from own frequencies at298K; nativeT replay agrees within2e-6Eh. Only RRHO column used. Both originalradical and actualTS1basin references retained separately | MATCH_AFTER_EXPLICIT_ANALYTIC_REPLAY | SI80 |
| connection route | Source IRC | TS2/alternative actualbidirectionalIRC;TS1 documented exact±0.15Å normalmode seeds plus endpointOpt/Freq and exact continuation joins, allowed by currenttask equivalentclause. Plus seed initially3.353731kcal/mol above saddle, then relaxes to correct lowerbasin; not monotonicIRC. Int1 finite torsional continuation/free release joinsTS2 basin without claiming a torsionalbarrier | DISCLOSED_TASK_PERMITTED_NUMERICAL_EQUIVALENT | SI80;currenttask;BN_connection_qualification.json |
| software/numerics | Gaussian16;revision/grid/optimizer thresholds not explicit in computationalsection | Gaussian16C.01; older defaultSCF and newerTight/UltraFine disclosed; no extra dispersion | REPORTED_UNSPECIFIED_FIELDS | Native route/header evidence |
| activation quantities | SCE4.422V/23.061kcal mol-1V-1;electronictriplet ordering | Eox1.096788954/Ered-2.690704599V;triplet79.631071485kcal/mol; source73.9/74.1 andprintSCF definition conflict retained, no thermal fit | DEFINED_QUALITATIVE_ORDERING_MATCH | SI67/76;main7 |

## Quantitative differences retained

| Quantity | Author | Local | Local minus author | Unit | Original tolerance |
|---|---:|---:|---:|---|---:|
| Eox vsSCE MeCN | 1.1 | 1.096788954 | -0.003211046000000106 | V | None |
| Ered vsSCE MeCN | -2.69 | -2.690704599 | -0.0007045990000000835 | V | None |
| TS1-own basin | 1.9 | -1.219029549 | -3.119029549 | kcal/mol | None |
| TS2-Int1 | 4.6 | 4.574769974 | -0.025230026000000016 | kcal/mol | 1.5 |
| TS-A common | 6.3 | 6.264583957 | -0.035416042999999675 | kcal/mol | None |
| TS-B common | 5.3 | 5.312790137 | 0.012790137000000534 | kcal/mol | None |
| Int-A common | 1.0 | 1.240592505 | 0.24059250499999996 | kcal/mol | None |
| Int-B own endpoint common | -40.7 | -43.953355177 | -3.253355176999996 | kcal/mol | None |
| C4 Int2 own endpoint common | -37.4 | -36.22330442 | 1.1766955800000005 | kcal/mol | None |
| substrate triplet electronic gap; source main | 73.9 | 79.63107148541678 | 5.731071485416777 | kcal/mol | None |
| substrate triplet electronic gap; source SI | 74.1 | 79.63107148541678 | 5.531071485416788 | kcal/mol | None |
| substrate adiabatic electronic triplet gap | None | 79.63107148541678 | None | kcal/mol | None |
| substrate electronic gap minus sensitizer59.8 | None | 19.831071485416786 | None | kcal/mol | None |
| substrate electronic gap minus sensitizer61.8 | None | 17.831071485416786 | None | kcal/mol | None |

Author298K/1atm replay of the original frequencies (no new QC, no qRRHO column used):

| Quantity | Author | Own298K | Difference | Original reproduction tolerance |
|---|---:|---:|---:|---:|
| TS1_own_basin | 1.9 | -1.219118236044925 | -3.119118236044925 | 1.0 |
| TS2_source_Int1 | 4.6 | 4.574283671083314 | -0.02571632891668596 | 1.0 |
| alternative_common_original_radical | 6.3 | 6.2645012467046675 | -0.035498753295332364 | None |
| TS1_minus_common_own_basin | -8.0 | -9.88577234340281 | -1.8857723434028095 | None |
| Int2_source_common | -37.4 | -38.83651273424306 | -1.4365127342430597 | None |

The old values−1.219029549 and4.574769974 remain in history; explicit fullprecision298K replay gives−1.219118236 and4.574283671. The first change also removes six-decimal printed thermal rounding. Both the originalradical and independently validatedTS1basin references are shown in the attached common-reference table. No choice is made to minimize the author residual. The original first-step±1.0 rule still fails; the second-step±1.0(reproduction)/±1.5(autonomous) rules still pass.

## Current work and next action

交父级复核两模式暂定候选；不追首步数字重算。保留TS1有限位移等价连接、298K回放和构象/速率限制；若父审认为其不满足任务等价连接标准，仅对此具体缺项重新定界。

NewjobIDs: none. ActivejobIDs: none.

[Current mode coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/qualitative_followup_20261019T1200Z/coverage.json) · [Method comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/qualitative_followup_20261019T1200Z/author_method_manifest.json) · [Native and reuse evidence](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/qualitative_followup_20261019T1200Z/reuse_inventory.json) · [All numerical comparisons](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/qualitative_followup_20261019T1200Z/numerical_comparison.json) · [Successor](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/qualitative_followup_20261019T1200Z/successor.json) · [Group first readback](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/qualitative_followup_20261019T1200Z/original_group_01/early_readback.json)

Earlier statements below are historical snapshots. This header supersedes their acceptance decision only for this explicitly named mode; all failure and residual evidence remains valid and preserved.

---

# Latest verification — storage recovery 2026-10-19

Updated UTC: 2026-10-19T06:39:49.855298+00:00. **Current scope verified: false; no new whole-question acceptance candidate.**

无本轮存储中断作业或新来源/实现缺陷。复用已合格两态及Int1原生证据；第一步−1.219029549对作者+1.9反号仍阻止整题验收。保持暂停新增QC，不以存储恢复为由重复计算。

自主第一步未校准数值窗；复现第一步1.9±1.0明确不通过。第二步4.574769974对4.6保留原±1.5/±1.0两模式窗口。

New successors: none. Native/API readback: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/storage_recovery_20261019T0530Z/original_group_01/early_readback.json. No new computation submitted.

Failure categories explicitly distinguish shared-free-floor guard from disk-full/quota errors and numeric failure. CBSCA floor is directly recorded; PE floor remains probable because its old postprocessing assertion suppressed the actual stage receipt. Do not convert platform SUCCEEDED into application success.

Next action: 无新输入，不提交；只有具体作者参照/构象连接或实现缺陷新证据出现，才重新评估第一步。

[Current mode coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/storage_recovery_20261019T0530Z/coverage.json) · [Unchanged author/local comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/storage_recovery_20261019T0530Z/numerical_comparison.json) · [Storage failure evidence](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/storage_recovery_20261019T0530Z/failure_classification.json) · [Successor and remaining gaps](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/storage_recovery_20261019T0530Z/successor.json)

Scientific method/model/state/temperature/reference and original tolerances remain unchanged. This round does not promote partial successes or storage recovery to whole-question PASS. All previous references below are historical.

---

# Independent verification — 2026-10-19

Updated UTC: 2026-10-19T01:54:34.665654+00:00. **Current scope verified: false. Whole-question acceptance candidate: none.**

Mode: autonomous. Only current public scientific findings; no whole-paper or exhaustive search requirement.

复核已接受Int1最低点和单/三重态六份原生日志hash，复用189正模及稳定根，不重复QC。纯高层电子态隙79.631071485 kcal/mol，高于敏化剂59.8/61.8；作者正文73.9、SI74.1与其印刷SCF对也有差异，保持纯电子定义，不加入热项追数。第一步−1.219029549对作者+1.9反号仍未解决；第二步4.574769974对4.6在原窗内。无新实现或来源缺陷证据，暂停新增计算。

单/三重态高层电子差已完成；此前旧对照中“高层Stable待返回”的行已更正。79.631071485与源正文73.9/SI74.1的差分别+5.731071485/+5.531071485 kcal/mol，不能通过加入热项降为73.603215来追数。作者印刷SCF对给约79.338。定性敏化剂排序成立；第一步失配继续保留。

| 量 | 作者值 | 本地值 | 本地−作者 | 既有数值窗 |
|---|---:|---:|---:|---|
| Eox vsSCE MeCN | 1.100000000 | 1.096788954 | -0.003211046 | — |
| Ered vsSCE MeCN | -2.690000000 | -2.690704599 | -0.000704599 | — |
| TS1-own basin | 1.900000000 | -1.219029549 | -3.119029549 | — |
| TS2-Int1 | 4.600000000 | 4.574769974 | -0.025230026 | 1.500000000 |
| substrate triplet electronic gap; source main | 73.900000000 | 79.631071485 | 5.731071485 | — |
| substrate triplet electronic gap; source SI | 74.100000000 | 79.631071485 | 5.531071485 | — |

能量单位kcal/mol，Eox/Ered单位V。表中“—”表示作者未给同量数值或未设置自动容差；不代表通过。完整逐点对照含定义及各模式原有数值判定见下列文件。

New jobs / latest recorded platform status: 无新提交. 原生计算尚未返回，不能计作科学完成。

Next action: 保留已验收局部活化、第二步和库存结果；只有出现具体作者参照、构象连接或实现缺陷证据，才恢复第一步诊断。原始TS/端点/热项和电极、溶剂定义不变；没有活动作业，也没有可据实定义的新补算。

Current unresolved items: TS1−自身盆地−1.219029549对+1.9，差−3.119029549 kcal/mol；复现模式±1.0明确不通过。

[Current mode rule/key-point/conclusion coverage](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261019T0035Z/coverage.json) · [Author/local comparisons](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261019T0035Z/numerical_comparison.json) · [Native paths, hashes and stage results](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261019T0035Z/native_audit.json) · [Failure-to-successor mapping and minimum missing evidence](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261019T0035Z/successor.json) · [This round report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261019T0035Z/verification_report.md)

Only current public scientific requirements are used. Successful calculations, failed logs and checkpoints are retained. No source answer, task/input, evaluator, tolerance, qualification, expert package or global registration is changed. Older entries below are historical and do not override this status.

---

# Latest independent verification update — 2026-10-18

Updated UTC: 2026-10-18T02:45:40.155607+00:00. **Current scope verified: false; no new whole-task PASS candidate.**

解除约束Opt/Freq与最终Stable完整返回：189正模，最低13.5564 cm−1；Gaussian原生negligible-force分支收敛，最大位移仍NO，未声称四项Tight全YES。重原子RMSD0.011405 Å，低层差0.000928714 kcal/mol，支持原TS2前Int1盆地；保留H转子差异，不混用新热项和旧高层。第一步−1.219029549对+1.9反号未解除。

BN 原生最末两次Normal在released_minimum.log第17265、28136行；第15940行注明negligible forces。Stable与Freq距离矩阵差0，能量差0。原始全原子同序RMSD0.441161 Å，允许同一母原子末端H置换后仍0.209344 Å；保留H转子差异，绝不称严格同几何。新约束28帧与释放20帧均保留完整成键图。没有从约束极大点创建新金标势垒。

No new HPC submitted this round. BN finite returned-stage acceptance completed; first-barrier mismatch remains.

Current coverage: [verification_followup_20261018T0200Z/coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261018T0200Z/coverage.json). [Numerical comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261018T0200Z/numerical_comparison.json), [native audit](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261018T0200Z/native_audit.json), [finite successor](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/verification_followup_20261018T0200Z/successor.json). Author values, existing windows, method/state/thermal/reference definitions and task/scoring files are unchanged. Earlier dated entries below are historical; their waiting states do not override this update.

---

# 最新验证参考 — 2026-10-17T12:06:52.080067+00:00

半步扫描源Stable正常；原第7点重现后，新第2约束点四项Tight均YES、E=−1381.36897739、S²after0.7503，较旧边界降低2.556 kcal/mol，与目标Int1重原子RMSD0.197504 Å。第3/9点40步L9999、位移未达门限。停止延长扫描；仅用新合格低盆地点提交首次解除约束Opt/Freq/Stable，原方法、态和48步上限保持。第一步势垒反号未解决。

**current_scope_verified=false；无新增整题通过候选。**

原参考保留于[本轮更新前快照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/package_before_reference_update/verified_computation_reference.md)。

# paper_89a7064f608ab3c0 — 本轮有限推进

更新时间：2026-10-17T12:06:52.080067+00:00；owner=original_group_01。

**ACTIONABLE_COMPUTE；current_scope_verified=false；无整题PASS候选。**

半步扫描源Stable正常；原第7点重现后，新第2约束点四项Tight均YES、E=−1381.36897739、S²after0.7503，较旧边界降低2.556 kcal/mol，与目标Int1重原子RMSD0.197504 Å。第3/9点40步L9999、位移未达门限。停止延长扫描；仅用新合格低盆地点提交首次解除约束Opt/Freq/Stable，原方法、态和48步上限保持。第一步势垒反号未解决。

本轮实际工作：

- 核收源Stable及两个完成约束点；保留失败第3点。
- 逐点实际图/自旋和目标Int1几何/能量比较，识别新的低盆地。
- 新合格点首次释放输入、33份旧实际优化种子去重、双锁资源核验提交。

数值比较保留原方法、参照及窗口；无另设容差：

|量及原参照|作者|本地|差值|原数值判定|
|---|---:|---:|---:|---|
|Eox vsSCE MeCN|1.100000|1.096789|-0.003211|未定义数值窗|
|Ered vsSCE MeCN|-2.690000|-2.690705|-0.000705|未定义数值窗|
|TS1-own basin|1.900000|-1.219030|-3.119030|未定义数值窗|
|TS2-Int1|4.600000|4.574770|-0.025230|原窗通过|
|TS-A common|6.300000|6.264584|-0.035416|未定义数值窗|
|TS-B common|5.300000|5.312790|0.012790|未定义数值窗|
|Int-A common|1.000000|1.240593|0.240593|未定义数值窗|
|Int-B own endpoint common|-40.700000|-43.953355|-3.253355|未定义数值窗|
|C4 Int2 own endpoint common|-37.400000|-36.223304|1.176696|未定义数值窗|
|substrate triplet electronic gap; source main|73.900000|—|—|未定义数值窗|
|substrate triplet electronic gap; source SI|74.100000|—|—|未定义数值窗|
|substrate adiabatic electronic triplet gap|—|79.631071|—|未定义数值窗|
|substrate electronic gap minus sensitizer59.8|—|19.831071|—|未定义数值窗|
|substrate electronic gap minus sensitizer61.8|—|17.831071|—|未定义数值窗|

现行评分关键点覆盖：

- rule_activation_origin：SUPPORTED_DEFINED_ENERGETIC_ORDERING。单/三重态各自189正模、低层/高层Stable及同几何合格；纯高层电子态隙79.631071485，高于敏化剂59.8/61.8。MeCN/SCE Eox1.096788954、Ered−2.690704599复用，保持MeCN/DCM区别。源73.9/74.1非精确评分要求，不通过混入热项拟合。
- rule_first_rearrangement：SCIENTIFIC_MISMATCH。TS1自身−1.219029549对+1.9反号；不能套用第二步4.6±1.5容差。
- ar_rule_barrier：SCALAR_WITHIN_EXISTING_WINDOW。TS2−源Int1=4.574769974对4.6±1.5，原有数值窗内；不替代TS1→Int1构象连续性。
- rule_selectivity：NEW_CONSTRAINED_LOWER_BASIN_FIRST_RELEASE_PENDING。半步扫描源Stable正常；原第7点重现后，新第2约束点四项Tight均YES、E=−1381.36897739、S²after0.7503，较旧边界降低2.556 kcal/mol，与目标Int1重原子RMSD0.197504 Å。第3/9点40步L9999、位移未达门限。停止延长扫描；仅用新合格低盆地点提交首次解除约束Opt/Freq/Stable，原方法、态和48步上限保持。第一步势垒反号未解决。
- rule_endpoint_balance：SUPPORTED_SCOPED_IDENTITY。中性2a/3a和+1双重态Int2实际图与65原子库存证据复用；还原补1电子，不引入虚假质子转移。完整光催化循环非当前要求。
- rule_evidence_validity：INTEGRATION_NOT_WHOLE_TASK_VERIFIED。独立已支持部分保留；整合结论受上述具体未完成项限制，过程诚实不替代结果分。
- rule_answer：INTEGRATION_NOT_WHOLE_TASK_VERIFIED。独立已支持部分保留；整合结论受上述具体未完成项限制，过程诚实不替代结果分。

新作业首查：

|作业|目标|平台|原生|
|---|---|---|
|hpc-job-78ac10c9-f37e-4387-88d0-617c079d8c16|Int1_new_lower_constrained_boundary_first_released_minimum|RUNNING|start_stability.log atoms=65, state=[1, 2], SCF=0, normal=0, error=0|

未解决项及最小恢复条件：

- FIRST_STEP_SIGN（SCIENTIFIC_MISMATCH）：TS1自身−1.219029549对源+1.9反号。 最小缺失：作者该TS与自身反应物的同几何高层、低层频率/热项及参照，或能定位具体实现缺陷的数据。 恢复条件：按原B3LYP/wB97XD路线审查差值成因；不用TS2窗口，不混入别的态或热项。
- C4_BASIN_CONNECTION（ACTIONABLE_COMPUTE）：半步扫描源Stable正常；原第7点重现后，新第2约束点四项Tight均YES、E=−1381.36897739、S²after0.7503，较旧边界降低2.556 kcal/mol，与目标Int1重原子RMSD0.197504 Å。第3/9点40步L9999、位移未达门限。停止延长扫描；仅用新合格低盆地点提交首次解除约束Opt/Freq/Stable，原方法、态和48步上限保持。第一步势垒反号未解决。 最小缺失：新低盆地首次释放端点189正模/Stable及目标Int1实际映射；不要求补完整旧扫描点数。 恢复条件：收78ac10c9：固定几何Stable/root、解除约束原Tight/189正模与最终Stable；再按完整库存/图、手性及同几何映射核目标Int1。若失败，保留证据且不自动重复。新解除约束不能预先证明扫描连续或第一步反号已解。

下一步：收78ac10c9：固定几何Stable/root、解除约束原Tight/189正模与最终Stable；再按完整库存/图、手性及同几何映射核目标Int1。若失败，保留证据且不自动重复。新解除约束不能预先证明扫描连续或第一步反号已解。

时间窗口：{"relative_to": "actual HPC start", "hours": [1.5, 3.5], "queue_delay": "unknown", "includes_queue": false, "confidence": "low-medium conditional on convergence", "budget_upper_bound_hours": 6, "UTC_window": ["2026-10-17T13:35:33.752191+00:00", "2026-10-17T15:35:33.752191+00:00"]}；返回后科学核收/收尾0.5–1.5小时（条件窗口）。整题PASS时间=null。

证据：

- [failed_stage_diagnosis.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/failed_stage_diagnosis.json)
- [BN_new_boundary_vs_target.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/BN_new_boundary_vs_target.json)
- [原生与作业记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/jobs.json)
- [复用索引](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/reuse_inventory.json)
- [逐项覆盖](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/coverage.json)
- [方法清单](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/author_method_manifest.json)
- [后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_89a7064f608ab3c0/advance_feasible_20261017T1145Z/successor.json)

所有新增QC仅在HPC；20CPU100GiB、人工智能驱动谱学研究、priority6、HPC-可上网区资源-2。提交前双共享锁内刷新CPU、两区容量/quota、集体存储及科学目标去重。保留旧错误和日志/检查点；无取消、删除、移包或发布；不改题面/评分/容差/资格。首查后交接，不空等长HPC、不自动恢复。



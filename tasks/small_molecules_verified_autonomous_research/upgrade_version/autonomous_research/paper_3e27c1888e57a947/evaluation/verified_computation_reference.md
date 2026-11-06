# Round-one scope notice — 2026-11-03

The existing scientific scope is retained. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## V3 scope and evidence reuse — 2026-10-27

Four independently scored final explanations replace eight mixed V2 nodes: molecular sulfone formation, butadiene regiochemistry, E/Z formation and phenyl-system reversal. Source intermediate values remain evidence context, with no hard windows. Native TS3 barrier and local reaction-energy deviations, interrupted reverse-IRC continuation and E/Z baseline distinctions remain explicit. Existing raw logs and historical notes below are preserved. This migration performs no new quantum computation or blind ARCHE run and does not inherit historical PASS. Current rules and per-outcome evidence coverage are in scoring_rules.json and reference_qualification.json.

## 2026-10-23 科学分V2维护副本

当前私有评分为`paper_science_v2`，共8个二元科学项，中间关键节点50分、最终结论50分，总计100分。全部过程分已删除。新规则不设数值硬窗口，不改变既有定性验收或数值差异记录。公开输入保持原样，题面中旧过程分/60+40措辞不代表本维护副本实际计分，作为专家待审文字遗留披露。科学评分资格与发布资格分开，见`reference_qualification.json`。

## 2026-10-23 当前科学问题验证过程与结果汇总

当前AR状态：`PROVISIONAL_PASS_QUALITATIVE`；这是已完成独立审查后的定性验收，不是尚未验收的候选。严格整题数值复现未登记，数值偏差和实现差异保留供专家判断。本节整合既有实际计算，没有新增量化计算。

### 方法、模型与执行过程

Gaussian16 C.01；PBE0-D3BJ/6-31G(d)气相优化/频率，298.15 K、1 atm RRHO；PBE0-D3BJ/6-311+G(d,p)、SMD-DMSO/DMF同几何单点。保留来源分子模型；单点色散措辞及未公开热化学细节存在不确定性。

1. 复用CF2H自由基加成、SO2捕获和芳基取代的来源结构，核对对应鞍点、反应振型、物种及参照。丁二烯与端苯基体系分开建模，保留其溶剂/条件差异。
2. 核收TS3两侧有效端点。反向IRC的23个接受点经可追溯数值续算达到反应物极小点，正向端点给出正确C–S成键、C–F离去及E产物连接；不是不间断完整反向IRC。
3. 由独立热项和单点计算局部势垒及区域/立体竞争，明确区分Int2-a/b不同零点、正文与SI不同数字。独立审查读取29份原生日志，未以平台结束状态代替科学验收。

### 论文与计算数值对照

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|初始CF2H加成势垒|7.6（正文）/7.656118（SI）|7.656094|+0.056094/−0.000024|kcal/mol|
|丁二烯1,4捕获势垒|3.2|3.185193|−0.014807|kcal/mol|
|丁二烯1,2捕获势垒|7.6|6.234892|−1.365108|kcal/mol|
|丁二烯1,2−1,4差|4.4（正文）/3.049696（SI）|3.049699|−1.350301/+0.000003|kcal/mol|
|E/Z局部基线势垒差|1.3|1.362990|+0.062990|kcal/mol|
|苯基体系1,4−1,2差|3.1|3.108123|+0.008123|kcal/mol|
|TS3−连通反应物端点|21.7（正文）/21.646567（SI）|28.382461|+6.682461/+6.735894|kcal/mol|
|连通局部产物−反应物|2.203186（SI）|8.344715|+6.141529|kcal/mol|

### 定性结论与保留项

当前AR形成连接、丁二烯1,4/E偏好和端苯基体系1,2偏好均有计算支持；较大的晚期取代势垒没有逆转所比较步骤的困难程度，但实验30°C/48小时的动力学时间尺度未得到计算证明。

- TS3局部势垒对正文高6.682461 kcal/mol；来源前配合物单点差−7.226079仍未解释，不能归因为构象松弛。
- 反向连接为有效IRC片段、连续继承几何的优化和最终端点，不宣称完整连续IRC。
- 未独立计算完整光循环、Zn溶液物种分布、离子交换、精确E/Z比或全局速率；这些不是当前必要计算。
- 历史PR范围较窄，保持其已有候选状态；本次只迁移当前AR整题，不自动给旧PR严格数值验收。

### 原生结果、独立复核及来源

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_3e27/acceptance_audit.md)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_3e27/acceptance_audit.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [native_recheck.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_3e27/native_recheck.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_3e27c1888e57a947/documents/main.pdf)：PDF页序（1-based）5,6,7。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_3e27c1888e57a947/documents/supplementary_001.pdf)：PDF页序（1-based）29,30,31,32,33,34,38,39,40,41,42。

来源方法未报告项、数值差异与题外未计算项目不能混为同一类问题。下方原有记录按日期保留，旧candidate/pending仅表示当时状态，不覆盖本节引用的最新父级验收。

---

## 历史验证记录（原文保留）

<!-- parent-acceptance-20261022T1743Z -->
## Parent acceptance — 2026-10-22 17:43 UTC follow-up

Current mode status: `PROVISIONAL_PASS_QUALITATIVE`. Independent source/native-log review supports all required qualitative conclusions of this current scientific question under the disclosed author model. This is provisional qualitative verification, not strict numerical replication or a change to scoring/release. The earlier candidate statements below are historical and are superseded only within the scope recorded here.

Parent decision: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/parent_acceptance_decision.json`. Independent audit: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_3e27/acceptance_audit.json`.

Latest connected-reference TS3 barrier: 28.382461 versus main-text 21.7 kcal/mol, difference +6.682461. Local product-minus-reactant: 8.344715 versus SI 2.203186 kcal/mol, difference +6.141529. These connected-reference numbers supersede older precomplex-reference comparisons for the final local path. Regio-/stereochemical directions remain supported. The source precomplex SP discrepancy remains unexplained, and experimental 30°C/48-hour kinetics are not reproduced by this calculation.

Retained qualifications:

- Current AR C1-C3 supported within author molecular model and experimental context; no full photocatalytic cycle, global rate or mixture-speciation model.
- Reverse connection is 23 valid IRC points followed by four traceable numerical continuations and converged endpoint; not uninterrupted full reverse IRC.
- Source precomplex SP difference -7.226079 kcal/mol remains unexplained and must not be attributed to conformer relaxation.
- TS3 barrier deviation and positive local reaction energy require expert review; experimental 30 C / 48 h timescale is not computationally reproduced.
- Single-point D3BJ wording and RRHO/standard-state limitations remain disclosed; independent audit found no material physical-input conflict.
- Historical PR is narrower and remains its prior candidate; this registration adds one completed-current-AR paper, not a second paper or an automatic strict rubric pass.

<!-- end-parent-acceptance-20261022T1743Z -->

# Verified computation reference — 2026-10-22 successful reverse endpoint and wholeAR qualitative candidate

Paper paper_3e27c1888e57a947. AR is now a PROVISIONAL_PASS_QUALITATIVE candidate for parent review after the missing reverse endpoint completed. Existing narrower PR candidate is unchanged. This does not register a strict numerical pass, scoring eligibility or release.

## Retained author method and scope

Gaussian16 gas PBE1PBE-D3BJ/6-31G(d) geometry/frequency,298.15K RRHO1atm, with same-geometry PBE1PBE-D3BJ/6-311+G(d,p) SMD DMSO or DMF single points. Author coordinates/route are used directly under verification authorization. Successful structures and comparisons are reused. SI single-point wording does not independently restate D3BJ; retained implementation and numerical/provenance uncertainty are disclosed. Experimental30C and THF/DMSO mixture are not identical to298.15K/DMSO continuum. No complete photocatalyst excitation, global rate or mixture-speciation model is claimed.

## Comparisons and limitations

|Quantity|Computed kcal/mol|AuthorSI|Author main|Signed residual vsSI|Signed residual vs main|
|---|---:|---:|---:|---:|---:|
|butadiene_regio_gap|3.049699|3.049696|4.400000|0.000003|-1.350301|
|phenyl_regio_gap|3.108123|3.108682|3.100000|-0.000558|0.008123|
|local_EZ_gap|1.362990|1.363013|1.300000|-0.000023|0.062990|
|TS1_free_reactants|7.656093|7.656118|7.600000|-0.000024|0.056093|
|TS3_minus_reoptimized_precomplex|28.515530|21.646567|21.700000|6.868963|6.815530|
|product_minus_reoptimized_precomplex|9.065228|2.203186|not specified|6.862042|not specified|

PR capture barriers3.185192910/6.234892091kcal/mol use common Int2-a+SO2. Both capture TSs have one suitable imaginary mode and two-sided native IRC support. Common1M correction is−1.894328445kcal/mol and cannot change ordering. SO2 native thermal correction differs fromSI by−0.000655Eh, contributing+0.411019kcal/mol to both association barriers. The3.049699 computed/SI regio gap versus main4.4 remains disclosed. E/Z local barriers3.185193/4.548183 use separate Int2-a/Int2-b reference states; absolute TS gap2.754121 and radical-reference gap1.391131 are distinct from local-barrier difference1.362990. No exact90:10 ratio or independent rapid-equilibration result is claimed. Phenyl DMF1,2 preference3.108123 has correct mapped capture modes; DMF conditions differ, so no substituent-only causality or newly computed distortion decomposition is claimed.

Source9-stage native audit: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/job_progress_resume_20261021T154758Z/returned_native_audit.json. PR energies/IRC: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/job_return_followup_20261021T071804Z/native_audit.json. TS1 one appropriate mode−110.7702cm−1 and radical/diene references support7.656093kcal/mol. TS3 has one mode−114.4637cm−1 with opposing C3–S15/C3–F14 changes. Forward IRC plus endpoint optfreq/SP successfully reaches the correct para C–S,E sulfone+NaF: G−2060.19076028Eh,0imaginary modes,C3–S15=1.802376A,Na20–F14=1.986818A,E dihedral172.646914deg. It is0.587443kcal/mol below the earlier4aa aggregate conformer. Product-minus-precomplex values are local aggregate energies, not whole photoredox reaction DeltaG.

## Explicit correction to earlier precomplex explanation

The previous claim that conformational relaxation or changed Na coordination lowered TS3-pre by6.869026kcal/mol is withdrawn. SI TS3-pre and the successful reoptimized precomplex are nearly identical: alignedRMSD0.001072A,max pair-distance change0.003694A,C3–S15=3.986848/3.986818A,Na20–O8=2.287790/2.288003A. SI SP−2060.360442Eh versus native−2060.37195749 gives−7.226079kcal/mol; thermal0.167118 versus0.167687 gives+0.357053; net G difference−6.869026. The discrepancy is chiefly the source/native SP energy difference, with unresolved cause; it is not demonstrated conformational relaxation. The historical28.515530difference uses a separately optimized source-like precomplex; use the new connected endpoint value28.382461below for the current local comparison. Exact correction and hashes: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/job_progress_resume_20261022T131002Z/precomplex_reference_correction.json.

## Successful adaptive RFO closeout

New job `hpc-job-ea37ec54-5f5c-4016-b674-5a6cca502984` completed in **521.709seconds**, returncode0, **3normal terminations**. This sub20minute result is a normal successful short computation. It follows predecessor `hpc-job-0214cb2c-4695-4c4b-ac32-3172026d233f`, whose60step RFO attempt had passing forces but failing displacements. The frozen0.020step radius was explicitly truncating the native step (scale0.094). One justified change restored TrustUpdate with initialMaxStep10, retaining Cartesian/RFO/CalcFC/RecalcFC5/NoLinear, all physical settings and default thresholds. Explicit predecessor step60 was reused; successful earlier science was not rerun.

The successor completed after3optimization steps. At native optimization completion: maximum force0.000204<0.000450,RMSforce0.000039<0.000300,maximum displacement0.001357<0.001800,RMSdisplacement0.000513<0.001200; allYES. Frequency yields102positive modes,min17.9533cm−1,0imaginary. Opt/frequency/SP geometries agree exactly in pair distances. A separate post-frequency Hessian table has estimated displacements0.009563/0.003016above optimizer thresholds and estimated energy change−3.246073e−7Eh; it did not rerun optimization or produce a native error. We retain the native completed default optimization plus small forces and positive frequencies, disclose this soft-coordinate sensitivity, and add no stricter post-frequency gate.

Reverse endpoint is neutral singlet36atoms, same reactant organic graph: C3–F14=1.320403Å,C3–S15=3.990503Å,Na20–O8=2.288979Å,Na20–O16=2.144777Å. Whole-geometry RMSD0.515614Å to the separately validated precomplex means it is not claimed identical. DMSOSP−2060.37192043Eh plus gasGthermal0.167862Eh gives **G−2060.20405843Eh**,0.133070kcal/mol above that other minimum.

All4explicit restart geometries were rechecked against the actual predecessor native coordinates with0.0Å maximum pair-distance differences, including the accepted reverseIRCpoint23 CURRENT STRUCTURE table. TS3's reaction-appropriate mode and native forwardIRC reach the validated para/E sulfone+NaF; reverseIRC1–23 plus traceable endpoint relaxation reach the validated reactant minimum. This is targeted IRC+relaxation evidence, not an uninterrupted full reverseIRC or proof of a unique mechanism. The C1 missing endpoint/reference evidence is now supplied.

|Current connected comparison|Computed kcal/mol|AuthorSI|Author main|Signed difference vsSI|Signed difference vs main|
|---|---:|---:|---:|---:|---:|
|TS3 minus reverse endpoint|28.382461|21.646567|21.700000|+6.735894|+6.682461|
|Forward product minus reverse endpoint|8.344715|2.203186|not specified|+6.141529|not specified|

The second row is a local aggregate difference, not total photoredox reaction free energy. The larger local barrier warrants expert numerical/model review; no global-rate agreement is claimed. C1connectedformation now joins C2(1,4andElocal preference) and C3(phenylDMF1,2preference) in a **wholeAR provisional qualitative candidate** under the current author-route policy. Source experimental redox context remains distinct from independently computed excitation/kinetics. All previously disclosed dispersion wording,RRHO,temperature,solvent and reference uncertainties remain. No strict numerical pass is asserted.

Actual local nonblocking preflight attempt found shared lock busy at16:53:37UTC; no local native run occurred or stability claim was made. One boundedHPC was submitted under shared locks with live both-region exact20CPU/100GiB fitting-node counts23/127,quota/account/project/storage/dedup checks. Project人工智能驱动谱学研究,priority6,HPC-可上网区资源-2. All6realIDs were reread at batch end and native logs/exit codes/success markers checked. No active assigned job remains; no further current-task computation is scheduled. Original10–35min conditional estimate assumed10–30steps; actual3steps+frequency/SP took8.7min.

Native closure audit: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/completed_successor_audit.json. Exact failure/success classes and actual old→newIDs: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/failure_triage.json, /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/repair_lineage.json. Full current comparisons: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/author_comparison.json. Task/version/union mapping: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/task_scope_inventory.json. Candidate/coverage: /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/acceptance_candidates.json, /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_3e27c1888e57a947/short_job_followup_20261022T1645Z/coverage.json. Parent/expert review may register the candidate; no global registration,task,evaluator,tolerance,expert-package orfinal/hold changes are made here. No timer or automatic restart.

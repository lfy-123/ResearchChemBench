# Current V3 evidence boundary — 2026-10-28

逐命题复用：R4位点电子比较及PR电荷差/幅比由原生B3LYP/CBSB7 CPCM-water输出和固定密度MK控制支撑；默认Δq(R4/7)=−0.484265/−0.055066 e、比8.794265，加密−0.427513/−0.049492 e、比8.638022。环化解释复用R/E身份与闭环连接关系，适用性结论明确水相单体/真实DCM混合物和多因素比较的界限。不新做计算，不将未收敛67原子扩展算作机理验证。

AR retains (R)-4 as the required object and compound 7 as optional. PR retains its original evaluator/disclosed author baseline comparing R4 and 7, including signed MK contrasts -0.441/-0.049 electron (±0.05 each) and magnitude ratio 9.0 (±1.0); the old public optional-7 sentence is corrected for PR only. Common final dimensions are electronic comparison (30), regioselectivity explanation (45) and experimental/causal applicability (25). AR has one electronic comparison; PR has three numeric outcomes at 12/8/10. Hbond/local-field and six-/seven-ring node scores and duplicate sign/qualitative-comparator scores are removed. All numerical windows are unchanged.

No new computation or blind evaluation was performed. Current rule-specific gaps are recorded in reference_qualification.json. The text below is historical and does not impose a current scoring or workflow requirement.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation plan — V2

Source graphs and substrate MEP calculations support a bounded molecular study. Previous NBS-related local structures can only support their exact state/inventory and require actual stationary-point/path inspection before reuse. Expanded kinetic explanation is not already validated by source charges. No new calculations were run.

## Source checked

- papers/paper_c625cba3ce868eb1/documents/main.pdf PDF pages [3, 5, 6, 7]; SHA256 44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8
- papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf PDF pages [30, 31, 32]; SHA256 19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db

## Reuse and gaps

- NBS chemical-path and selectivity calibration remains pending.
- The source concentration typo and aqueous-computation/DCM-experiment mismatch must remain explicit.
- Expanded uncertainty, semantic judge and runtime isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.

## Confirmed integrity repair — 2026-09-30

Findings: B4-I08.

### Source facts and current contract

- tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/agent_input/data/inputs/systems.json; species[id=compound_4_R], map_namespace=compound_4_R, atoms[map_id=22].element=H; SHA256 20e4b9ec6a200ccac19f311062856897d85aa564224dee4e63bbc6df2333196e

Atom identifiers are local to the declared object and map_namespace. Evaluate identity, closure topology and reacting atoms after applying an explicit chemically valid bijective remapping; a changed numeric label alone is not a chemical error.

### Valid existing evidence and limits

Previously recorded source minima/MEP and local models can be reused only under their actual graph and namespace. This repair validates label invariance, not new pathways or selectivity.

- tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_c625cba3ce868eb1/evaluation/task_provenance/existing_evidence_reuse.json; SHA256 a7c6de0cab021f8c62a5b0b8a22d12c5eaa6df9b54458f07ca218a1d76b8f2bb

### Remaining steps and why

Future graph-to-artifact binding must apply the supplied bijection and retain stereochemistry. Chemical selectivity/pathway calibration is unchanged and remains unvalidated by this textual repair.

Rebind the affected KP/rule/comparison and final conclusion to the repaired package_content_sha256 before reusing an evaluation contract. Assess completion against the original public scientific question, not a self-narrowed addressed_scope. Missing necessary investigation, a failed calculation, copied public source values or a statement of source ambiguity earns no credit for the missing work and cannot yield whole-task full credit. Preserve credit for independently valid completed parts and accept sufficiently supported non-author conclusions without a fixed route or extra method matrix. Real judge calibration and runtime isolation remain pending. No new scientific calculation was performed for this repair.

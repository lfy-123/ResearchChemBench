# 当前V3证据复用状态（2026-10-28）

本轮仅完成最终命题改编与合同检查，未重新进行科学验证、语义校准或AR盲测。当前状态为`V3_ADAPTED_EXISTING_EVIDENCE_NOT_REVALIDATED`，不能从历史STRICT_PASS继承V3通过。逐命题覆盖和缺口以reference_qualification.json及verified_computation_reference.md顶部为准。

## 历史验证计划与旧裁定（以下全文为历史记录）

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation plan — V2

Source four finite Cu intermediate coordinate/energy records and historical endpoint calculations demonstrate accessible local models. They do not provide verified C–Cl transition paths or a full competing-route reference. Model/state and temperature ambiguities are reviewable within a bounded local investigation.

## Source checked

- papers/paper_db6c4e0558113873/documents/main.pdf PDF pages [6, 7, 8, 9]; SHA256 9b9d8841f0eb5ec7561cb770ad3bd43d0820639e443412d5da1bc74842318c8c
- papers/paper_db6c4e0558113873/documents/supplementary_001.pdf PDF pages [56, 60, 64, 65]; SHA256 a6585fbc4d364923517f436132456b23b012d972eeecb7a818a8a4259c1a6608

## Reuse and gaps

- Expanded raw path/state evidence and numerical sensitivity remain incomplete.
- Exact source thermal convention needs clarification; retain source label without inventing corrected values.
- Alternative-route semantic calibration and execution isolation pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.

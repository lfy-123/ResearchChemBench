# Scoring applicability — 2026-10-29

This document retains source/verification context. Only current scoring_rules.json controls scoring: independent semantic pass/fail final conclusions, without numerical target windows or author-workflow requirements. Historical scientific findings below are unchanged and are not new validation.

# 当前V3说明（2026-10-28）

本版仅评分最终科学结果，当前证据复用及未覆盖项见 verified_computation_reference.md 顶部。以下旧验证计划及验收为历史，不能直接作为本版V3全面通过。

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation plan — V2

SourceINT-G/full-XantPhos coordinates and previous localH2 andDMAc computations support a manageable molecular problem. Existing solvent-capture thermochemistry remains a partial model result, not a validated complete recovery route. Full ligand SMILES formulaC39H32OP2 was checked offline; no scientific job was started.

## Source checked

- papers/paper_9132719dbf91c978/documents/main.pdf PDF pages [1, 4]; SHA256 3d08d907aafb9175e71858913e8f6671891645f0479d189eab246a24d442faeb
- papers/paper_9132719dbf91c978/documents/supplementary_001.pdf PDF pages [10, 11, 12]; SHA256 ae27addc290464f1b17ef3fbd0dd6cac8eb0830aa03cc0aaa686fd57321d2817

## Reuse and gaps

- Expanded state/path/pressure uncertainty and usablePd regeneration remain uncalibrated.
- A source small barrier cannot set a universal tolerance for alternative models.
- Semantic judge and actual filesystem isolation pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.

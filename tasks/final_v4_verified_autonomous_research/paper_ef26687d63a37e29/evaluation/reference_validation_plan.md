# 当前V3说明（2026-10-28）

本版仅评分最终科学结果，当前证据复用及未覆盖项见 verified_computation_reference.md 顶部。以下旧验证计划及验收为历史，不能直接作为本版V3全面通过。

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation plan — V2

Source molecular structures, adduct DFT and NMR probes establish a feasible bounded interaction question. Earlier free/adduct computations can be reused only for their exact local identity and method; old constructed-chain jobs do not certify an actual polymer mechanism. No scientific engine was started.

## Source checked

- papers/paper_ef26687d63a37e29/documents/main.pdf PDF pages [9, 10]; SHA256 bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf PDF pages [4, 5, 7, 8, 9, 10, 11, 12]; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96

## Reuse and gaps

- New association/reactivity free-energy and model-representativeness calibration remains pending.
- The source local DFT solvent specification is incomplete and is not silently replaced byV1 THF353.15K.
- Actual semantic judge and runtime isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.

## Confirmed integrity repair — 2026-09-30

Findings: B4-I05, B4-I06, B4-I04.

### Source facts and current contract

- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf; physical page 35; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf; physical page 36; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf; physical page 37; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf; physical page 38; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf; physical page 39; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf; physical page 40; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96
- papers/paper_ef26687d63a37e29/documents/main.pdf; physical page 8; SHA256 bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8
- papers/paper_ef26687d63a37e29/documents/main.pdf; physical page 10; SHA256 bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8

Source-coordinate limitation: SI physical pp39-40 lists 51 atoms (C14H30N3O3P) for the PA adduct; the complete stoichiometric (Et2N)3P + PA model has 61 atoms (C20H34N3O3P), a C6H4 difference. The complete PA reagent connectivity in systems.json remains valid. Reconstruction must identify retained source atoms, added atoms and the resulting graph; a reconstructed model is not an unchanged source geometry. No missing coordinates are supplied or invented here. For main physical p8 Figure 6 and p10, distinguish a specified H-site ADCH population, the nearest-contact H and a declared alpha/beta-H family statistic. Define sites from the N-ethyl CH2/CH3 graph and map them explicitly; do not equate a figure-labelled H with a nearest site or family mean without evidence. Report signed electrostatic potential with its units and surface definition separately from electron density; source colour/prose alone is not a density measurement. These local observables do not by themselves establish polymer propagation or backbiting rates.

### Valid existing evidence and limits

The prior audit rehashed free/PO/PA wavefunction and ESP products (six files). Existing 61-atom reconstructed PA evidence must retain its reconstruction provenance. Site labels, nearest H and family means are distinct; source coordinates remain incomplete.

- docs/v2_integrity_audit_20260930/batch4/evidence/native_binding_readback.json; SHA256 17b2255653b1e54fcaf12a0dc992684532df0086d52255f4316f9ddf550701c9

### Remaining steps and why

Retain explicit reconstruction and atom-role mappings; compare the same observable at matched sites. Local ADCH/ESP does not certify polymer-scale kinetics; further pathway work is needed only for asserted kinetic claims.

Rebind the affected KP/rule/comparison and final conclusion to the repaired package_content_sha256 before reusing an evaluation contract. Assess completion against the original public scientific question, not a self-narrowed addressed_scope. Missing necessary investigation, a failed calculation, copied public source values or a statement of source ambiguity earns no credit for the missing work and cannot yield whole-task full credit. Preserve credit for independently valid completed parts and accept sufficiently supported non-author conclusions without a fixed route or extra method matrix. Real judge calibration and runtime isolation remain pending. No new scientific calculation was performed for this repair.

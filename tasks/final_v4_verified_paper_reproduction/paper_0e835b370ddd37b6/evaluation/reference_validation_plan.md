# Current validation boundary — 2026-10-29

Score only independent final scientific conclusions, with fixed pass/fail weights totaling 100. Actual linked calculations or reproducible data analysis must support each claim with correct chemical identity, physical definition, conditions and reference. Numbers, structures, modes and state assignments are evidence, not author-value acceptance windows or separate process scores. A supplied observation, guessed answer, software execution or copied source value alone earns no credit. A fully supported equivalent explanation or an explicitly permitted evidence-based model-sensitive conclusion passes directly; missing or insufficient evidence and unsupported contradictions fail the affected item. There is no need_review state. One failed item does not erase independent supported points. Whole-case success is assessed separately from the numerical score. AR chooses a justified method; PR assesses the disclosed baseline or substantiates a physically comparable substitution and its consequences. Historical reference defects remain recorded and do not automatically confer success. No new calculations were performed in this revision.

## Historical validation plan (not an active score contract)

Former numerical-window and review instructions below are retained only as historical provenance and do not override the current rules.

# 当前V3说明（2026-10-28）

本版仅评分最终科学结果，当前证据复用及未覆盖项见 verified_computation_reference.md 顶部。以下旧验证计划及验收为历史，不能直接作为本版V3全面通过。

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation plan — V2

Source model coordinates, finite barriers and TableS2 diagnostics plus historical1/V′ calculations provide tractable local feasibility evidence. Existing deformation/interaction jobs are optional evidence tied to their exact geometry/reference, not a mandatory route; model4 and complete uncertainty are not scientifically validated here.

## Source checked

- papers/paper_0e835b370ddd37b6/documents/main.pdf PDF pages [2, 3, 4, 5]; SHA256 4481b439479e8874cffa309e47cec459ec33ca4d18be30b921e08b43a3233971
- papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf PDF pages [7, 8]; SHA256 df2f9a3f458bd80190146adb77300f8cc65385fc12d2a5bba829e8d60a0e189c

## Reuse and gaps

- Expanded raw evidence for model4 and robust three-model explanation incomplete.
- Actual scientific judge acceptance of adequate non-decomposition routes pending.
- Source-model-to-experiment transfer remains outside task; execution isolation pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.

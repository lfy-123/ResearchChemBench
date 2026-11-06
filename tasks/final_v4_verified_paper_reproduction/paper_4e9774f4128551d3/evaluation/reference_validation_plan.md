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

Source S35–S38 establish finite53-atom ketoester reference geometries and frequencies and support product-level reanalysis. The mapped enol is a source-consistent constructed graph, not a source optimized protonation intermediate. New pathway or ensemble conclusions need their own valid artifacts; exact reproduction remains qualified by medium and model choices.

## Source checked

- papers/paper_4e9774f4128551d3/documents/main.pdf PDF pages [5, 6]; SHA256 37a7fad866bff774d010cc6b61af21da2150a78c5bce69c1ff41574648c5b8b4
- papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf PDF pages [20, 21, 71, 73, 76]; SHA256 64fda6d0c684c5c53ad4434788b2fe57bfa21ff63ec78215d47885b4103de76a

## Reuse and gaps

- No expanded molecular protonolysis reference or validated selectivity uncertainty exists for the open question.
- The main/SI solvent-ratio conflict remains a genuine source ambiguity, not a missing permission.
- Semantic calibration for alternative explanations and runtime isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.

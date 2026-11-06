# Current validation boundary — 2026-10-29

Score only independent final scientific conclusions, with fixed pass/fail weights totaling 100. Actual linked calculations or reproducible data analysis must support each claim with correct chemical identity, physical definition, conditions and reference. Numbers, structures, modes and state assignments are evidence, not author-value acceptance windows or separate process scores. A supplied observation, guessed answer, software execution or copied source value alone earns no credit. A fully supported equivalent explanation or an explicitly permitted evidence-based model-sensitive conclusion passes directly; missing or insufficient evidence and unsupported contradictions fail the affected item. There is no need_review state. One failed item does not erase independent supported points. Whole-case success is assessed separately from the numerical score. AR chooses a justified method; PR assesses the disclosed baseline or substantiates a physically comparable substitution and its consequences. Historical reference defects remain recorded and do not automatically confer success. No new calculations were performed in this revision.

## Historical validation plan (not an active score contract)

Former numerical-window and review instructions below are retained only as historical provenance and do not override the current rules.

# Active V3 validation boundary — 2026-10-28

Existing native M06/6-31G(d,p)/PCM(DCM) G09Defaults logs give S1 = 2.9521/2.5853/2.4342 eV and S1 f = 0.4990/0.1927/0.0116. Bright-state f = 0.8848/1.0174/1.0400; the maximum source f residual is 0.0004. Transition-density analyses support NP/AQ ICT and a PQ acceptor-local low state. Gas B3LYP ground-state preparation is the PR baseline, not a hidden AR restriction. The source NPC frontier-gap discrepancy (3.98 eV arithmetic versus 3.54 eV printed) remains non-scored. Historical strict scope acceptance is retained but is not a new V3 validation.

现有三分子实算可复用，无本次改编新增物理量；若部署开放方法判分，仍需针对替代态解释与硬窗适用性的独立Judge校准。 No new computation, blind run or online Judge calibration was performed. The historical plan and acceptance below are retained only as history.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# V2 evidence and calibration boundary

Reuse the exact V1 full-molecule geometry, native TD output and transition-analysis artifacts as one bounded calibration route. Keep publication S1 and bright-transition values separate. Adversarial cases include wrong E/Z or truncated alkyl graphs, relabeling bright peaks as S1, orbital-gap-as-excitation, root-index-only state matching, calling transfer-probability similarity a wavefunction overlap, invented torsion controls, and monomer-to-emission overreach. Valid alternative methods and evidence-based revised/negative state assignments need actual semantic judge calibration; no new scientific or judge run is authorized here.

No new scientific computation or semantic judge run was launched during content authoring. Reuse is limited to the exact objects, definitions and conditions in reference_reuse.json. V1 acceptance and historical archive matrices are not V2 requirements. Before scored deployment, independently test claim-conditional validity and evidence scoring on the documented positive/negative cases, audit runner isolation, and calibrate any newly used scientific route. Current file/hash/schema/runtime tests establish implementation only.

## 2026-09-30 source-conflict repair

NPCZCS has an unresolved internal source discrepancy: main physical p8 Figure5A labels HOMO −5.86 eV and LUMO −1.88 eV, whose arithmetic difference is 3.98 eV, but the same figure prints a 3.54 eV gap and main p7 also states 3.54 eV. Preserve both accounts without choosing a true value or silently correcting the source. These are orbital-gap source statements, not singlet excitation energies or mandatory numerical score targets. A transparent report of the conflict and independently supported results must not be penalized for missing either number; reporting the conflict alone does not replace the required molecular excitation investigation.

Reuse source-specific native excitation/NTO evidence at its actual geometry, functional, solvent and normalization. Rebind source-comparison checks to retain this conflict; do not use a diagnostic computed gap to select the correct printed value. Live semantic calibration remains pending.

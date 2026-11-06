# Current validation boundary — 2026-10-29

Score only independent final scientific conclusions, with fixed pass/fail weights totaling 100. Actual linked calculations or reproducible data analysis must support each claim with correct chemical identity, physical definition, conditions and reference. Numbers, structures, modes and state assignments are evidence, not author-value acceptance windows or separate process scores. A supplied observation, guessed answer, software execution or copied source value alone earns no credit. A fully supported equivalent explanation or an explicitly permitted evidence-based model-sensitive conclusion passes directly; missing or insufficient evidence and unsupported contradictions fail the affected item. There is no need_review state. One failed item does not erase independent supported points. Whole-case success is assessed separately from the numerical score. AR chooses a justified method; PR assesses the disclosed baseline or substantiates a physically comparable substitution and its consequences. Historical reference defects remain recorded and do not automatically confer success. No new calculations were performed in this revision.

## Historical validation plan (not an active score contract)

Former numerical-window and review instructions below are retained only as historical provenance and do not override the current rules.

# Current V3 validation scope

Only final propositions in scoring_rules.json are active. Existing evidence is summarized in verified_computation_reference.md. No new chemistry validation or blind evaluation was performed. Previous acceptance does not establish a V3 full pass.

## Historical validation plan (not active scoring instructions)

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# V2 reference validation plan

Existing Gaussian anion/radical logs and reproducible analysis demonstrate a feasible solution-phase molecular route. The toolbox Gaussian/ORCA and Python analysis interfaces may support alternative routes after inspecting actual installed capability. No new calculation is needed for this content upgrade; future reference review can first reparse the named artifacts and Figure 3 and then assess any method-specific gaps.

## Existing evidence and limits

Read-only existing real artifacts: docs/upgrade_tasks_verification/group_2/papers/paper_3e4cad1d1d650d0c/report/results.json (SHA256 84bf365fd1e7d49e9837eb500d20900948bbb04702c74bb35a1771f4af22fd75), report/report.md, analysis/recompute.py, analysis/resource_accounting.json, outputs/legacy_reused/1a_anion/stdout.log, outputs/legacy_reused/1e_anion/stdout.log, outputs/1a_radical_source_optfreq/attempt_002/stdout.log and outputs/1e_radical_source_optfreq/attempt_001/stdout.log. These support an author-informed CAM-B3LYP/CPCM route and its limited sensitivities plus a graphical quenching analysis. They are not blind AR evidence or an exhaustive model reference, and their additional operations are not V2 requirements.

## Outstanding scientific calibration

Electrochemical total error and microscopic association alternatives are not calibrated; raw individual lifetime measurements are missing. Existing reference computations were author-informed and used a limited state/conformer model. A quantitative kinetic or yield conclusion is unsupported. V2 semantic judge calibration and sandbox isolation are pending.

This authoring run performed no new chemistry calculations, HPC submissions or remote judge calls. Offline package/contract/runtime checks do not establish chemical accuracy. A future reference review should verify source/structure/state correspondence, reproduce the claim-relevant quantities from raw existing artifacts, and assess the agent-chosen method limitations; additional science is separately authorized. No fixed V1 matrix, winner or uncalibrated tolerance is an acceptance rule. Actual alternative-route judging and private-file isolation must be checked independently.

## Integrity repair and reference handoff — 2026-09-30

Source recheck: actual SI physical pp23–24 and 26, 57–58, SHA256 674c2d21b7a260c23cc55a07bb394e8e67f19d18ddf217229fe5080352fe8810. PR now discloses PhCl rather than the experimental 4-chloroanisole, the 1a−/PhCl and 1a−/K+/PhCl compositions (net charges −1/0 by bookkeeping), CAM-B3LYP versus the FigS34 D3 label, and ΔE versus ΔG. Damping and association standard-state details remain unspecified. Both modes retain the SI23 373 nm / SI24 410 nm steady-state discrepancy separately from SI26 375 nm TCSPC; no condition is silently selected as corrected truth.

The existing anion/radical opt/frequency and redox/plot analysis remains reusable only for its actual identities, energy references and observation domain after hash/identity recheck. It does not validate the FigS34 PhCl/K+ association route or justify transferring its quantities directly to 4-chloroanisole. A source-route reference review still needs to identify the fragment reference, states, counterion accounting and thermal/standard-state conventions, audit native association results where available, and assess transfer limitations. Missing microscopic alternatives or raw lifetime data are not repaired by this text. These are reference-validation needs, not a hidden mandatory AR matrix. No new calculation or numeric tolerance was introduced.

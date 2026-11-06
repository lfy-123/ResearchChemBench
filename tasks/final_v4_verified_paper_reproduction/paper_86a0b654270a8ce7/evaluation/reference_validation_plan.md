# Scoring applicability — 2026-10-29

This document retains source/verification context. Only current scoring_rules.json controls scoring: independent semantic pass/fail final conclusions, without numerical target windows or author-workflow requirements. Historical scientific findings below are unchanged and are not new validation.

# Active V3 validation boundary — 2026-10-28

Existing source-compatible B3LYP/def2-SVP/SMD(THF), 339 K minima give G1/G2 = -2795.462325/-2795.463430 Eh, ΔG = -2.901177 kJ/mol versus source -2.835540 kJ/mol (residual -0.0656375). Both have 384 positive modes (minima 11.3669/12.3800 cm−1). Absolute G offsets of approximately 8.9 kJ/mol remain unexplained. Fixed-geometry SuperFine curvature is not a reoptimization. Existing alternative-method plus borrowed-thermal sensitivity can reverse the small preference (+0.325/+0.332 kJ/mol with a 100 cm−1 entropy floor); it does not constitute alternative reoptimized Gibbs minima, and prevents a universal robustness claim. Geometry agreement supports contact compatibility, not a unique stacking energy. Historical strict acceptance is limited to the source model.

本版未新增物理问题，已有模型内结果可复用；跨方法稳健偏好、唯一接触因果或真实产率推断需要额外研究，本轮不执行。 No new computation, blind run or online Judge calibration was performed. The historical plan and acceptance below are retained only as history.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# V2 reference validation status

The source compares two isolated Ir–salen–NHC coordination isomers and proposes an intramolecular stabilization account. The task retains their molecular relative stability at the source THF/339K computational conditions.

冻结记录两极小点384实频和339 K账本已审；接触释放、构象群与配对敏感性仍未齐。

Old source coordinates, calculations and V1 validation are retained as historical evidence; no inherited PASS or matrix completion obligation. This V2 package needs independent semantic evaluator calibration and isolated execution before scientific release. Existing logs must be parsed for the exact object, state, method, energy/measurement reference and claimed scope before reuse. Source results are conditional references, never a universal tolerance or mandatory winner.

Existing two full-system native stationary-point records show feasibility, including their actual positive frequencies. They do not by themselves prove a mechanism or exhaustive free-energy ordering. Additional reference breadth and semantic calibration remain pending.

Minimum later validation: verify genuine input/identity and applicable native output; recompute linked quantities/units from stored artifacts; assess whether the evidence sustains the particular scientific claim; test valid alternative/inconclusive cases and paper-specific misleading/invalid submissions. New numerical ranges require genuine method/model/extraction uncertainty, not legacy narrow tolerances. This round starts no science jobs and no paid/judge runs.

# Current scope and scoring — 2026-11-03

Why does reversible epimerization of ketoester 50 behave differently from its two-stage enolization/protonolysis treatment, and, under explicit ideal separation/recycling assumptions, is the calculated three-cycle cis recovery compatible with the reported isolated yield? Explain the supplied observations using molecular calculations and quantitative analysis. The experimental outcomes are known; their explanation is the task.

The existing scientific scope is retained.

Only the following independently supported outcomes receive points:

- endpoint_gap: Endpoint thermodynamic preference of the mapped cis/trans epimers and its physical scope (20 points).
- condition_interpretation: Why equilibrium and separate-pot stereochemical outcomes differ (40 points).
- recycle_balance: Three-cycle cis recovery and its relation to the observed isolated yield (40 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Active scoring revision — 2026-10-29

Only independently weighted final scientific conclusions in scoring_rules.json are active (100 total; semantic pass/fail only). No numeric target/tolerance, author-node completion or process gate is active. Historical route descriptions and older scoring allocations below are source context only. Original scientific scope, real computational-evidence requirements and historical scientific acceptance are unchanged.

# Private final-result reference

V3 has three final results: endpoint Gibbs gap20, condition-dependent interpretation40, recycling mass balance40. The former20-point integrated conclusion repeats these outcomes and is not scored again. The former endpoint target2.3171919±1.0kcal/mol is retained as non-scoring historical context. The endpoint item now evaluates its thermodynamic conclusion and scope; all three final items are binary.

Main pp5–6 Scheme5 and epimerization discussion, SI pp20–21 identities/operations and p71 methods/table (coordinates pp71–76). The fixed skeleton epimerizes at local map6 (R→S), remote11S/13R/30S remain. Neutral C20H30O3 endpoints each53atoms. Source method B3LYP-D3/6-31G(d,p), high-level6-311++G(d,p), IEFPCM methanol eps32.63; gas thermal correction. Source table's DZ heading is misleading: values match E+Gcorr. Local recomputation gives2.64122503 rather than2.3171919.

Main solvent1:1 conflicts with SI6.0/0.60mL; preserve both. The observed1.1:1 is single-pass trans:cis,70% is cumulative after three recycling rounds. Source143/203mg ratio70.44%; ideal lossless three-cycle model85.63% is a conditional bound, not an exact yield forecast. Existing detailed-balance counterexamples establish endpoint energies cannot uniquely infer a30-minute branching ratio. Native paths and limits are in final_result_coverage.json; historical verification prose remains unchanged.

</details>

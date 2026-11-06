# Current scope and scoring — expert_round2_20261103

How compatible are the five specified photocatalysts with activating N-benzoyl dibenzothiophene sulfilimine into a reactive electronic state, and how far does that molecular comparison explain productive or trace THF amidation? This is an explanation task: the product and screening yields are supplied observations.

The existing scientific scope is retained.

Only the following independently supported outcomes receive points:

- tx_compatibility: Thioxanthone activation compatibility (15 points).
- ir_dfppy_compatibility: Ir(dFppy)3 activation compatibility (15 points).
- standard_ir_boundary: Standard iridium photocatalyst near-matching activation scale (20 points).
- fac_ir_mismatch: fac-Ir(ppy)3 molecular mismatch relative to productive catalysts (15 points).
- mes_acr_mismatch: Mes-Acr+ molecular mismatch relative to productive catalysts (15 points).
- yield_nonmonotonicity: Explanatory reach of molecular compatibility for yield differences (20 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Current final-conclusion evaluation — 2026-10-29

Score only independent final scientific conclusions, totaling 100 points. Require actual executed calculations and recoverable native evidence for the molecular identities, composition, charge/spin, bonding, conditions, physical quantities and reference states relevant to each claim. Numerical energies, geometries and responses are evidence, never author-value targets or tolerance gates. A missing rounded scalar alone does not lose credit when the recoverable calculations establish the requested comparison. Do not restore numerical gates from historical references. Supplied observations, guessed conclusions, copied values, completed jobs, named intermediates and generic limitations earn no independent credit. Accept scientifically established equivalent explanations within the public scope without requiring author software, labels, a fixed intermediate inventory or an additional full reaction network. Method-sensitive alternatives must satisfy the specific criterion and actual evidence; a method change alone does not justify a contradictory claim. Return pass or fail for every item: a supported conclusion receives its whole weight, and an unsupported conclusion receives zero with a specific reason. Record demonstrated reference defects separately in objective_issue_flags; do not fabricate support or erase unrelated valid items. Infrastructure errors must be reported rather than disguised as scientific failures. Whole-case success requires every required_for_success item to pass, while independently supported items retain their points. Historical verification and structural package validation do not confer scientific acceptance.

- r_tx_compatibility (15): Thioxanthone activation compatibility
- r_ir_dfppy_compatibility (15): Ir(dFppy)3 activation compatibility
- r_standard_ir_boundary (20): Standard iridium photocatalyst near-matching activation scale
- r_fac_ir_mismatch (15): fac-Ir(ppy)3 molecular mismatch relative to productive catalysts
- r_mes_acr_mismatch (15): Mes-Acr+ molecular mismatch relative to productive catalysts
- r_yield_nonmonotonicity (20): Explanatory reach of molecular compatibility for yield differences

Sources and existing native evidence are mapped in evaluation/evidence_map.json. No public scope or molecular input changed.

## Historical source/route snapshot through 2026-10-27 — non-scoring

The following record preserves source numbers, old design text, provenance and limitations. Any former numeric window, intermediate requirement or review-state wording below is historical and inactive. Current scoring is exclusively the binary conclusions above and in scoring_rules.json.

# Private source and final-result map

Source checked directly: main PDF pp.5–6 Scheme4E and energetic interpretation; SI PDF31 TableS6 (five chosen catalyst properties/conditions), PDF32 PBE0 calculation method, PDF33 TableS7 (G(T1)−G(S0)). All other screened catalysts and later nitrene/HAA/rebound stages remain outside this task.

Final rules: r_tx_compatibility15; r_ir_dfppy_compatibility15; r_standard_ir_boundary20; r_fac_ir_mismatch15; r_mes_acr_mismatch15; r_yield_nonmonotonicity20. Each molecular outcome needs the computed substrate scale plus traceable catalyst comparison and an explicit inference. Shared substrate state calculations are not independently rewarded; no additional aggregate grouping points duplicate five outcomes.

Source catalyst ET(kcal/mol):65.5,63.5,61.8,58.1,44.7, in the above order. These are literature-context values, not local catalyst calculations. Source substrate G(S0)/G(T1)=−1258.961473/−1258.862640Eh and gap62.0. Native G=−1258.97862038/−1258.88066910Eh and gap61.465356; deviations−10.760143/−11.313431kcal/mol absolute and−0.534644 gap. The offset cause is not explained by difference cancellation.

Source/local baseline: PBE0/6-311G(d) IEFPCM-MeCN Opt/Freq then PBE0/def2TZVP SMD-MeCN SP,298K RRHO. Native Gaussian16C.01 uses reconstructed singlet/triplet coordinates; no original coordinates supplied. Ideal-gas thermal correction from the solvent Hessian is a disclosed reading of the SI, not guaranteed original implementation. Native35atom C19H13NOS,0/1 and0/3 each99positive modes; T1 postannihilationS²2.0014. See docs/verification/small_molecules_autonomous_research/paper_87f5566528287b60/new44_20261022/substrate_S0_T1/native/{S0,T1}/gaussian.log and acceptance_audit_87f5 under short_job_followup_20261022T1743Z.

Standard Ir donor-minus-gap changes from source−0.2 to native+0.334644kcal/mol; near matching is the defensible conclusion, not an exact sign threshold. The two matched productive Ir yields61/76% do not increase monotonically with ET. Thioxanthone66% is a separate370nm/10mol% condition. MeCN model is not THF experimental solvent, and these local calculations do not validate a complete photochemical mechanism.

The retained r_yield_nonmonotonicity ID now scores the actual explanatory reach of the submitted model. Nonmonotonicity is established for the source triplet-energy model. Other independently computed, physically justified models are assessed on their demonstrated reach and condition matching; neither the source/native baseline nor a fit to the supplied yields establishes such an alternative.

</details>

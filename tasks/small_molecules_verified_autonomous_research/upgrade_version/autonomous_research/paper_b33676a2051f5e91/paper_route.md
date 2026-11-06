# Current scope and scoring — expert_round2_20261103

Starting from the supplied oxygen-centered radical Int-3 derived from sec-butylbenzene, what local chemistry explains acetophenone formation, and which of the two supplied carbon–carbon beta-scission channels is kinetically favored? This is a local explanation task; product structures are supplied and must be supported by independently calculated formation evidence.

The required chemistry begins at supplied Int-3. Int-2 is contextual only; no benzylic activation, peroxide cleavage or upstream radical generation is required. Both product drawings are inputs, not discoveries.

Only the following independently supported outcomes receive points:

- local_cleavage_chemistry: Local cleavage chemistry and accessibility of acetophenone formation (50 points).
- cleavage_selectivity: Local accessibility of propiophenone formation and kinetic preference between the competing cleavages (50 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Current final-conclusion evaluation — 2026-10-29

Score only independent final scientific conclusions, totaling 100 points. Require actual executed calculations and recoverable native evidence for the molecular identities, composition, charge/spin, bonding, conditions, physical quantities and reference states relevant to each claim. Numerical energies, geometries and responses are evidence, never author-value targets or tolerance gates. A missing rounded scalar alone does not lose credit when the recoverable calculations establish the requested comparison. Do not restore numerical gates from historical references. Supplied observations, guessed conclusions, copied values, completed jobs, named intermediates and generic limitations earn no independent credit. Accept scientifically established equivalent explanations within the public scope without requiring author software, labels, a fixed intermediate inventory or an additional full reaction network. Method-sensitive alternatives must satisfy the specific criterion and actual evidence; a method change alone does not justify a contradictory claim. Return pass or fail for every item: a supported conclusion receives its whole weight, and an unsupported conclusion receives zero with a specific reason. Record demonstrated reference defects separately in objective_issue_flags; do not fabricate support or erase unrelated valid items. Infrastructure errors must be reported rather than disguised as scientific failures. Whole-case success requires every required_for_success item to pass, while independently supported items retain their points. Historical verification and structural package validation do not confer scientific acceptance.

- r_local_cleavage_chemistry (35): Local cleavage chemistry and accessibility of acetophenone formation
- r_cleavage_selectivity (35): Kinetic preference between acetophenone- and propiophenone-forming local cleavages
- r_local_activation (30): Accessibility and limits of a reagent-derived local benzylic activation route

Sources and existing native evidence are mapped in evaluation/evidence_map.json. No public scope or molecular input changed.

## Historical source/route snapshot through 2026-10-27 — non-scoring

The following record preserves source numbers, old design text, provenance and limitations. Any former numeric window, intermediate requirement or review-state wording below is historical and inactive. Current scoring is exclusively the binary conclusions above and in scoring_rules.json.

# Private V3 result map: local sec-butylbenzene oxidation

Direct source checks: main PDF6–8 Fig7 and cleavage discussion; SI23 BHandHLYP/aug-cc-pVDZ/SMD-MeCN method; SI25–29 substrate/Cl/benzyl radical/HCl/TS1; SI33–37 Int3,TS4a,TS4b and product coordinates. The paper's13.39/9.07 barriers refer to the source Int3. Source conflict exclusions recorded in qualification are retained; the public problem remains local.

Active rules: r_cleavage_products20 (two balanced endpoint identities), r_acetophenone_barrier30 (9.07±2.0kcal/mol), r_cleavage_selectivity30 (competing local barrier and final preference), r_local_activation20 (chlorine-HAT reference explanation with explicit disconnected-network boundary). Intermediate node counts, endpoint files, TS counts and author's labels earn no independent score.

Native index: docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261013T195300Z/parent_b336_native_readback.json. Two scission TSs each have66modes and one imaginary frequency−474.9764/−557.2732cm−1; connected reactant endpoints have66positive modes, G−463.662920/−463.663078Eh, same graph and RMSD0.033391Å. Native source-like Int3 G−463.661083 matches source−463.661084 but is not the proven connected baseline. Hence acetophenone barrier10.050192–10.149338 and competing14.549435–14.648581kcal/mol, ΔΔG4.499243 versus source4.32. The hard ethyl window stays9.07±2; no tolerance is invented for the competitor.

Mapped scission products are C8H8O+C2H5 and C9H10O+CH3 from C10H13O0/2; finite IRC endpoints certify identity, not infinite-separation free energies. Cl-HAT0/2 TS has69modes with−297.0403cm−1 and two valid IRC branches66/79points. Separated-reference G(TS)−G(R)−G(Cl)=3.239204 versus source3.23kcal/mol. The local segments do not establish intervening oxygen chemistry or dominant photocatalytic flux.

</details>

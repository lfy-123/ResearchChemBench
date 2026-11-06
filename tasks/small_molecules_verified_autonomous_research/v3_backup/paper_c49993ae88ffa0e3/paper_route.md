# Current scope and scoring — 2026-11-03

Explain the molecular basis and thermodynamic feasibility of light-driven pyridine N-oxide deoxygenation by preformed phenanthrene-9,10-diol (H2PQ) in acetonitrile. Determine how adding two explicit water molecules changes the net deoxygenation thermodynamics and the stabilization of relevant ionic transfer states. This is an explanation task with quantitative net thermodynamic outputs.

Explicit waters define finite hydration energy comparisons, not a required water-catalyzed path. Local ionic stabilization and net reaction thermodynamics are distinct conclusions.

Only the following independently supported outcomes receive points:

- cumulative_f_dry: Thermodynamic driving force for deoxygenation without added water (20 points).
- cumulative_f_water: Thermodynamic driving force for deoxygenation with two added waters (20 points).
- reductant_molecular_role: Molecular basis of light-driven reduction by preformed H2PQ (30 points).
- local_hydration_effect: Why finite hydration changes reaction thermodynamics and what it can explain (30 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Current final-conclusion evaluation — 2026-10-29

Score only independent final scientific conclusions, totaling 100 points. Require actual executed calculations and recoverable native evidence for the molecular identities, composition, charge/spin, bonding, conditions, physical quantities and reference states relevant to each claim. Numerical energies, geometries and responses are evidence, never author-value targets or tolerance gates. A missing rounded scalar alone does not lose credit when the recoverable calculations establish the requested comparison. Do not restore numerical gates from historical references. Supplied observations, guessed conclusions, copied values, completed jobs, named intermediates and generic limitations earn no independent credit. Accept scientifically established equivalent explanations within the public scope without requiring author software, labels, a fixed intermediate inventory or an additional full reaction network. Method-sensitive alternatives must satisfy the specific criterion and actual evidence; a method change alone does not justify a contradictory claim. Return pass or fail for every item: a supported conclusion receives its whole weight, and an unsupported conclusion receives zero with a specific reason. Record demonstrated reference defects separately in objective_issue_flags; do not fabricate support or erase unrelated valid items. Infrastructure errors must be reported rather than disguised as scientific failures. Whole-case success requires every required_for_success item to pass, while independently supported items retain their points. Historical verification and structural package validation do not confer scientific acceptance.

- r_cumulative_f_dry (20): Thermodynamic driving force for deoxygenation without added water
- r_cumulative_f_water (20): Thermodynamic driving force for deoxygenation with two added waters
- r_reductant_molecular_role (30): Molecular basis of light-driven reduction by preformed H2PQ
- r_local_hydration_effect (30): Why finite hydration changes reaction thermodynamics and what it can explain

Sources and existing native evidence are mapped in evaluation/evidence_map.json. No public scope or molecular input changed.

## Historical source/route snapshot through 2026-10-27 — non-scoring

The following record preserves source numbers, old design text, provenance and limitations. Any former numeric window, intermediate requirement or review-state wording below is historical and inactive. Current scoring is exclusively the binary conclusions above and in scoring_rules.json.

# Private reference and final-result scoring

Active V3 outcomes: net dry G 20; net two-water G 20; molecular reduction explanation 30; local hydration explanation 30. Net targets remain -115.1±2.0 and -112.1±2.0 kcal/mol. Ten other PT/ET/first-H-transfer endpoint values remain non-scoring source context, with their old windows unchanged in reference_key_points.json. The final mechanistic answer is not required to reproduce the author's intermediate sequence.

Main PDF p4 Fig2 and SI pp38–41 define the chemistry and state-dependent thermochemistry. Source: M06-2X/def2-TZVPP//6-31+G(d,p), SMD(MeCN), TD for S1, GoodVibes3.0.2 at298.15K/1M, Grimme100cm^-1, scale1, external symmetry and all source conformer labels. The text's -115.1 is cumulative from excited R, not an increment after I. Final product PyOH2 is an associated pyridine/generated-water object; two-added-water systems carry two additional waters.

132 native files in parent_pq_native_readback.json support all12 original endpoint quantities. Current coverage is recorded outcome by outcome in final_result_coverage.json; no historical PASS is inherited. Source original PES YAML/frequencies remain unavailable and hydrated terminal thermal residuals persist. No kinetic sequence, complete catalyst regeneration, rates or bulk-water optimum is certified. Protected v1_backup retains the earlier evaluation documents.

The public reference conventions apply only to the two required net Gibbs energies. They are not an assertion that S1, the product association or the selected water allocation uniquely describes the reacting solution. Mechanistic state/association choices remain evidence-dependent; two required numerical comparisons and their original hard windows remain unchanged.

</details>

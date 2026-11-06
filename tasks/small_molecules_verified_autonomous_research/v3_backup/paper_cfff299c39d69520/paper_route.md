# Current scope and scoring — 2026-11-03

What molecular catalyst, bond-forming chemistry and finite product-formation free-energy profile explain the Zn/proline-promoted coupling of the specified terminal alkyne and alkynyl bromide, and what can the supported activation energetics establish about the effect of heating to 125 °C?

The required model is a finite product-forming pathway through diyne release. No catalyst regeneration, full-cycle closure, steady-state turnover or complete catalytic energy span is required.

Only the following independently supported outcomes receive points:

- active_catalyst: Chemically accessible active zinc species from the supplied precatalyst (20 points).
- coupling_chemistry: Bond-forming chemistry and zinc oxidation-state behavior (25 points).
- balanced_profile: Thermodynamics of the balanced finite pathway through diyne release (20 points).
- path_activation: Principal activation demand in the tested finite product-forming pathway (20 points).
- temperature_effect: Conditional temperature effect on the tested product-forming activation (15 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Current final-conclusion evaluation — 2026-10-29

Score only independent final scientific conclusions, totaling 100 points. Require actual executed calculations and recoverable native evidence for the molecular identities, composition, charge/spin, bonding, conditions, physical quantities and reference states relevant to each claim. Numerical energies, geometries and responses are evidence, never author-value targets or tolerance gates. A missing rounded scalar alone does not lose credit when the recoverable calculations establish the requested comparison. Do not restore numerical gates from historical references. Supplied observations, guessed conclusions, copied values, completed jobs, named intermediates and generic limitations earn no independent credit. Accept scientifically established equivalent explanations within the public scope without requiring author software, labels, a fixed intermediate inventory or an additional full reaction network. Method-sensitive alternatives must satisfy the specific criterion and actual evidence; a method change alone does not justify a contradictory claim. Return pass or fail for every item: a supported conclusion receives its whole weight, and an unsupported conclusion receives zero with a specific reason. Record demonstrated reference defects separately in objective_issue_flags; do not fabricate support or erase unrelated valid items. Infrastructure errors must be reported rather than disguised as scientific failures. Whole-case success requires every required_for_success item to pass, while independently supported items retain their points. Historical verification and structural package validation do not confer scientific acceptance.

- r_active_catalyst (20): Chemically accessible active zinc species from the supplied precatalyst
- r_coupling_chemistry (25): Bond-forming chemistry and zinc oxidation-state behavior
- r_balanced_profile (20): Thermodynamic feasibility and closure of the balanced catalytic free-energy network
- r_turnover_span (20): Kinetic bottleneck controlling the balanced catalytic turnover
- r_temperature_effect (15): Kinetic explanation for operation at125°C

Sources and existing native evidence are mapped in evaluation/evidence_map.json. No public scope or molecular input changed.

## Historical source/route snapshot through 2026-10-27 — non-scoring

The following record preserves source numbers, old design text, provenance and limitations. Any former numeric window, intermediate requirement or review-state wording below is historical and inactive. Current scoring is exclusively the binary conclusions above and in scoring_rules.json.

# Private V3 source and final-result map

Directly read main PDF2 methodology and alternatives, PDF3 Schemes4–6 active-catalyst formation, PDF4 Fig2/Table1 network/TS, SI PDF2 full energy table, PDF4–6 original47-atomTS coordinates, PDF13 Eyring approximation. Source uses B3LYP-D3/6-31+G(d)CHNO, LANL2DZ/Hay–WadtZn/Br/Cs,CPCM ethanol,298.15K,G09. Active rules: accessible catalyst20; coupling chemistry25; balanced profile20; span20; temperature15. No named intermediate/job completion scores remain.

Source Int1 is neutral bis-prolinate ZnII; formation ZnEt2+2ProH→Int1+2ethane. Source balanced Int2 height recomputed from SI is4.078811581 whereas main says9.6; preserve both as conflict, do not choose whichever matches local5.476275. Source controlling span29.2±1.0 is the unchanged hard target. It is a balanced height above catalyst+R1+R2+Cs2CO3, not the local TS−Int2−R2.

Native ledger: docs/verification/small_molecules_autonomous_research/paper_cfff299c39d69520/closeout_followup_20261020T1530Z/balanced_numerical_analysis.json. Formation−98.533420146 versus SI−98.515222371; balanced profile0→5.476275180→30.132377435→−36.722100992→−69.832391821kcal/mol, regeneration increment−33.110290830 versusSI−33.129990193. Local coupling barrier24.656102255 differs from controlling30.132377435. All atom/charge balances zero; preserved L stereochemistry and ZnII bookkeeping.

Native original-sourceTS is independently calculated at47 atoms0/1,135frequencies,one−443.7185cm−1 reactive mode, G−1134.063144Eh versusSI−1134.062445. Default residual-force tests pass, displacement diagnostic does not. No new optimization or independent IRC; connection support is source geometry/mode and matched independent minima, not a blind pathway recovery. Expert assessment must retain this qualification rather than automatic historical PASS.

Using actual30.132377435 in fixed-ΔG Eyring givesk298=5.08248533e−10 andk398=2.39409564e−4s−1,471048fold acceleration and48.25min half-life. Source2.4e−9/7.9e−4s−1 are contextual examples, not added windows or local reproduced rates. No high-temperature thermochemistry was recomputed.

</details>

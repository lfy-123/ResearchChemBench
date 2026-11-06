# Current scope and scoring — 2026-11-03

Explain how the specified visible-light reaction of buta-1,3-diene, sodium difluoromethanesulfinate and methyl pentafluorobenzoate forms the observed polyfluoroaryl sulfone. What explains its 1,4-versus-1,2 competition and E preference, and the reversal to 1,2 addition for the specified terminal-phenyl diene? This is an explanation task: observed products and preferences are supplied starting facts.

The existing scientific scope is retained.

Only the following independently supported outcomes receive points:

- sulfone_formation_explanation: A connected molecular and energetic account explains formation of the target sulfone (30 points).
- butadiene_regio_explanation: Computed formation competition explains butadiene 1,4 preference (25 points).
- butadiene_geometry_explanation: Formation energetics support the observed E preference within explicit interconversion assumptions (20 points).
- phenyl_regio_reversal: The terminal-phenyl system reverses the favored regiochemistry under its specified conditions (25 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Active scoring revision — 2026-10-29

Only independently weighted final scientific conclusions in scoring_rules.json are active (100 total; semantic pass/fail only). No numeric target/tolerance, author-node completion or process gate is active. Historical route descriptions and older scoring allocations below are source context only. Original scientific scope, real computational-evidence requirements and historical scientific acceptance are unchanged.

# Private scientific route and provenance

Paper: Photoredox-catalyzed cascade difluoromethylation/SO<sub>2</sub> reintegration/polyfluoroarylation of conjugated dienes with a bifunctional CF<sub>2</sub>HSO<sub>2</sub>Na reagent
DOI: 10.1039/d5gc05765e; journal: Green Chemistry; publication date: 2026-01-28.

## One connected computational question

The Stage05 record is retained exactly in `evaluation/research_contract.json`. Its question focused on selectivity, while the original article actually calculates a connected product-formation/selectivity investigation. The corrected question and every changed public input have one source-bound entry in `evaluation/task_definition.json`. No paper identity, computed system or original result is replaced. The scientific question is:

How does the specified visible-light reaction of buta-1,3-diene, sodium difluoromethanesulfinate and methyl 2,3,4,5,6-pentafluorobenzoate form the observed polyfluoroaryl sulfones, and what governs its 1,4-versus-1,2 regiochemical competition and E/Z product preference, including the switch to preferential 1,2 addition for (1E)-1-phenylbuta-1,3-diene under its specified related conditions?

The computational-method statement `ev_doc_dae8dc0cd8db_000171_960e172688be` and author attribution `ev_doc_e2120ae96275_000075_8c526c0eb147` establish actual author execution. The original Scheme 3 on `pdf-page-doc_e2120ae96275-p5` was rendered and viewed, not inferred from its caption. Its formation profile includes sulfinate-radical fragmentation thermochemistry, initial difluoromethyl addition, two allylic arrangements, competing regio-/stereochemical SO2 captures, reduction by the photocatalyst redox pair and sodium-associated aryl C-F substitution. The same page and body result block `ev_doc_e2120ae96275_000064_ed83a363574b` give the phenyl competition/distortion study. Spin maps on `pdf-page-doc_dae8dc0cd8db-p29` and `ev_doc_dae8dc0cd8db_000173_0a16295284c9` support the selectivity interpretation. These are one investigation of connected formation and substrate-dependent selectivity, not separate software/descriptor tasks.

## Identities and starting evidence

Main pages 3-4 and SI pages 5-6,8,15 were viewed for ordinary starting/product graphs and conditions. The phenyl representative is the unsubstituted terminal-phenyl E diene, not an internal-phenyl isomer. SI pages 41-42 and their actual coordinate records were checked by carbon connectivity and substituent geometry, without any electronic-structure calculation or author-energy recalculation. Both TS models contain C11H11F2SO2 and the same CHF2-ended chain connected to terminal phenyl. SI pages 40-41 establish the E butadiene organic product, para aryl sulfur and terminal CHF2. The source coordinate model includes NaF; it is not a contradictory seven-fluorine organic identity. The misplaced extracted TS2-d heading is resolved by the actual original page ordering, not by discarding conflicting data. SI pages 36-38 verify 4CzIPN's C56H32N6 identity, two meta nitriles and four carbazolyl nitrogen sites.

Butadiene conditions use 1.5 mL dry DMSO, with butadiene dosed as 0.50 mL of its 2 mol/L THF stock, plus Na2CO3 and 5 W blue LEDs. Phenyl comparison conditions are DMF/no added carbonate/40 W blue LEDs, with the same catalyst/additive and coupling partners. The distinct conditions are retained, rather than claiming a controlled substituent-only experiment. The 74%/7% butadiene yields identify isolated E/Z products; they are not calibrated rate measurements. The 74% terminal-phenyl E-product yield is an observed starting fact, not a predicted computational answer. No absolute configuration, detection threshold or unreported wavelength is invented.

## References and limits

CR1 is an optional spin-population comparator, not a mandatory explanation. CR2-CR4 retain the local butadiene capture barriers. The full connected profile from their shared original result block is retained in `CTX_FORMATION_PROFILE` and the private protocol, including the reported initial addition and final sodium-associated substitution outcomes. Core C1 nevertheless evaluates the requested connected formation account itself, not selection of that author route. C2 evaluates the actual regio-/E-Z explanatory outcome; its author route/population details remain optional context. CR5 and the actual DMF TS records anchor C3, the phenyl-regioselectivity reversal. Distortion/interaction decomposition is a reported supporting analysis, not an independent compulsory descriptor deliverable.

Every numerical value is reported source material, not a recomputed reference. Local activation-free-energy differences must be distinguished from a global/common-reference TS comparison, especially because the two allylic minima are different in energy. The paper's 1.3 kcal mol^-1 local capture difference and 90:10 E/Z estimate do not define a complete kinetic model. The phenyl panel's relative free-energy labels and Delta E distortion/decomposition totals are different observables; the source does not explicitly specify a more detailed energy convention for the decomposition. No uncertainty/error bars or complete standard-state/low-frequency recipe are supplied in the methods. Gas-phase optimization, continuum solvent single points and 298.15 K thermochemistry do not exactly reproduce a full experimental mixture at 30 °C. Some prose calls lower-barrier preferences thermodynamic favorability; this terminology is preserved only as author interpretation, not adopted as an equilibrium-selectivity conclusion.

Experimental radical clocks, inhibitors, trapping/accumulation observations, fluorescence quenching, Zn exchange studies and the broad substrate library are not new computational goals or hidden tests. Their broader experimental claims do not extend the computational reference to excitation/quenching kinetics, Zn exchange barriers, whole-mixture speciation, additional substrates or a fitted global kinetic model. This is an explicit author-computation boundary, not a reduction to one convenient subcalculation.

## Shared evaluation and paired view

One public problem, one data projection and the byte-identical shared submission template define the autonomous scientific core. `evaluation/reproduction_protocol.json` contains the complete source-bound author guidance. The program inserts that block immediately before the public-input section to derive the reproduction view; there is no separate reproduction package or extra scientific goal. Each guidance material paragraph is exactly its protocol ledger statement and has original-source evidence. The block is wholly absent from autonomous public files.

Historical pre-V3 record (inactive): six key points assessed research quality (60 points): identities/models, testable explanations, informative tests, actual validated execution, evidence-driven decisions and reproducible/uncertain reporting. Three core conclusions assess scientific resolution (40 points): connected formation, butadiene regio-/E-Z explanation and the terminal-phenyl reversal. Core statements and expectations do not append a selected author mechanism or exact barrier. Conditional comparators are unscored and have no omission penalty. Baseline fidelity is assessed within the same criteria only when guidance is publicly supplied, with justified substitutions and alternative explanations allowed. Honest partial or failed work may earn research-quality credit but does not automatically resolve the scientific question.

`evaluation/evidence_map.json` holds exact complete source excerpts and SHA256 hashes, visual-inspection descriptions and private identity derivations. Page-marker text is not treated as an observation; descriptions record what was actually viewed. No PDF, source page, author-optimized geometry, spin plot, transition-state seed, intermediate or answer-bearing script is public. The builder executed only document access, identity inspection and package construction/validation, not the scientific research or author reference calculations.

## Current V3 final-result evaluation — 2026-10-27

Only the 4 independent final conclusions in scoring_rules.json are active, totaling 100 points. Historical route details and intermediate numbers above are source context, not scored completion requirements. Each criterion requires actual computation supporting its final claim; no process points or historical 60/40 split applies. Four independently scored final explanations replace eight mixed V2 nodes: molecular sulfone formation, butadiene regiochemistry, E/Z formation and phenyl-system reversal. Source intermediate values remain evidence context, with no hard windows. Native TS3 barrier and local reaction-energy deviations, interrupted reverse-IRC continuation and E/Z baseline distinctions remain explicit.

</details>

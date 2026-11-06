# Current scope and scoring — 2026-11-03

Starting from the supplied cyclic oxocarbenium ions and triarylborohydride anions, explain catalyst-dependent cis/trans formation selectivity in the local reduction stage of hydrogenative reductive cycloetherification of D4 (1,4-diphenylbutane-1,4-dione) and D5 (1,5-diphenylpentane-1,5-dione), and its relation to product stability across ring sizes. Account for the supplied triarylborane performance comparisons using molecular evidence. This is an explanation task; the measured ratios and yields are supplied observations.

The required selectivity pathways start from the supplied cyclic oxocarbenium and borohydride species. Diketone-to-cation formation, H2 activation and regeneration are not required.

Only the following independently supported outcomes receive points:

- catalyst_function: Catalyst acidity and reaction performance have distinct molecular origins (25 points).
- d4_kinetic_control: D4 cis preference is a formation effect rather than a product-stability preference (25 points).
- catalyst_selectivity_contrast: The A/B change affects D4 stereochemical discrimination with model-dependent strength (20 points).
- ring_size_relationship: Increasing ring size aligns cis formation preference with cis product stability (30 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Active scoring revision — 2026-10-29

Only independently weighted final scientific conclusions in scoring_rules.json are active (100 total; semantic pass/fail only). No numeric target/tolerance, author-node completion or process gate is active. Historical route descriptions and older scoring allocations below are source context only. Original scientific scope, real computational-evidence requirements and historical scientific acceptance are unchanged.

# Private scientific route and provenance

This package constructs one connected author-computation-grounded research question. The immutable Stage05 research_contract is copied unchanged. The private task_definition corrects the narrower public question to encompass the actual connected investigation, preserving original input IDs, kinds and order. The autonomous public task contains only that corrected question, graph-explicit neutral identities, conditions, ordinary product observations and the shared submission/investigation requirements.

## Actual author computation and its scientific purpose

- SI 7.1: conformational exploration with xTB/CREST/CENSO, ALPB ether, selected structures for ORCA 6.0.1 omegaB97X-D3/def2-TZVP optimization/energy/frequency work. Geometry optimizations are gas-phase; CPCM diethyl ether is applied for solvation. RRHO thermochemistry is at 353.15 K. Minimum and TS frequency statements are author-reported validation, not evidence that a complete catalytic network or IRC search was performed. See the exact source-bound protocol paragraphs and evidence map.
- SI 7.2: FIA and HIA for B1/B2/B3 are negative gas-phase reaction enthalpies at 298.15 K/1 atm, measuring catalyst Lewis-acid response. S4 values are B1 467/519, B3 423/477 and B2 409/464 kJ/mol. Main-paper Table 1 connects the acidity/bulk hypothesis to 1a cyclic-ether/furan outcomes. The shared question preserves the required molecular catalyst-function/performance interpretation, but does not turn these descriptors into uncomputed side-reaction barriers or turnover predictions.
- SI 7.3 and Figure 1: the symmetric 1y/2y system is used for cis/trans oxocarbenium-reduction competition with B3 and B1. CR1 and CR3 are 2.1 and 0.7 kcal/mol relative TS Gibbs differences at 353.15 K; CR2 is the -0.3 kcal/mol product difference under the signed G(trans)-G(cis) convention. The authors report a local cis reduction barrier of 5.1 kcal/mol. Only the formation/stability relationship and catalyst-dependent competition are required, not this particular intermediate or local barrier as a unique answer.
- S5 and S61-S63: the same catalyst B1 with six-membered 2af gives the CR4 4.1 kcal/mol TS preference and separately reported 2.6 kcal/mol product-stability preference. The table predicts about 341:1 while experiment establishes only >20:1. This retains the ring-size dependence as a core outcome; it is not an optional comparison or an exact-ratio benchmark.
- S58-S60/main article: NCI/contact/stacking analyses support the author's structural explanation. Alpha-H/aryl contact distances are 2.65 Angstrom with B3 and 2.76 with B1 in the cis TS; both B3 TSs exhibit stacking around 3.6 Angstrom, so the authors do not treat stacking alone as a general explanation. These descriptors and the chair/boat interpretation for 2af are optional contextual references, never separate scored requirements. Their scientific purpose, a molecular account of stereochemical competition, is retained in the core outcomes.

Earlier ketone reduction/cyclodehydration/H2 activation and furan pathways are experimentally interpreted rather than computationally mapped here. Main-paper Scheme 4/control experiments motivate the chosen author model but do not supply a complete catalytic-network computational reference. Other substrate scope, stereochemical probes, synthetic applications and solvent screening are therefore not added as research goals. The 1a catalyst screen is supplied only because it is the observed context for the actually performed catalyst-affinity comparison.

## Identity verification, not mere name copying

Viewed original main-paper Table 1 (p3), Scheme 2 (p4), Scheme 4 (p6) and Figure 1 (p7); SI product drawings/descriptions on S38 and S41; S56/S57/S61; the S63 trans TS illustration/end-point; and coordinate pages S65/S66/S74/S75/S76/S86/S87/S90. Every claim here about a drawing refers to an actually viewed original, not a PDF-page evidence marker. Other rendered-but-unviewed coordinate pages are not claimed as visually inspected.

Source-only parsing of the original-PDF coordinate records followed by elemental counts, distance connectivity and relative stereocenter checks established:
- 1y: C16H14O2, two phenyl-carbonyl termini connected by two CH2 carbons, matching 1,4-diphenylbutane-1,4-dione.
- cis/trans-2y: C16H16O, O/C4 five-membered ring, phenyl on each oxygen-adjacent carbon. Determinant signs for O/phenyl/ring-CH2/H priorities are opposite for cis and equal for trans, matching the SI relative assignments.
- cis/trans-2af: C17H18O, O/C5 six-membered ring with the same phenyl placement and matching relative configuration. The authors state the precursor is 1,5-diketone 1af; the generic diketone-to-cyclic-ether scheme and explicit product graph establish PhCO(CH2)3COPh. No unreported coordinate geometry is supplied to the solver.
- B1: C18BF15 = B(C6F5)3. B3: C18BH3Cl2F10 = B(C6F5)2(2,6-dichlorophenyl). B2: C18BH5Cl2F8 = B(2,3,5,6-tetrafluorophenyl)2(2,6-dichlorophenyl), not a second replacement by a dichlorophenyl ring. Both tetrafluorophenyl hydrogens are three ring bonds from the B-bound ipso carbon (para); both chlorines are ortho. Table 1 drawings and coordinate graphs agree.

The source-inspection script and audit in scratch are private diagnostic work, not execution of the downstream scientific task. No reference energies, Boltzmann ratios, barriers or author results were recalculated. Public local Catalyst A/B/C correspond privately to B1/B3/B2; D4/D5/K4 correspond to 1y/1af/1a. No source label or author optimized geometry is published.

## Conditions, contradictions and comparison limits

Main-paper source blocks ev_doc_e52a848cf7ef_000034_c3a8a1c39701 and ev_doc_e52a848cf7ef_000052_7f090019274c establish the 10 mol %, CPME, 100 bar H2, 80 C, 18 h context. Table 1's catalyst comparison instead uses iPr2O at 50 C. These are separately labelled in PI2. Isolated D4/D5 yields and endpoint NMR 1a yields are distinguished. A >20:1 ratio is a lower bound, and no cross-condition yield is treated as an elementary rate.

The general procedure prints approximately 150 mg/mmol of molecular sieves, while the scope caption gives 300 mg at 0.2 mmol. The public projection preserves Stage05's sieve identity/use only and does not choose or invent a loading. No sieve-dependent computational or kinetic claim is requested.

The main text's unsigned 0.3 kcal/mol product difference is consistent as a magnitude with the signed -0.3 in S5 and the plotted trans-lower product energies. Signed comparisons use the explicit S5 convention. No source sign is silently rewritten.

The original S76 water entry prints G = -694.39312778 Eh, identically repeating the trans-2y entry on S75. Both original pages were rendered and viewed; this is not an OCR-only discrepancy. It prevents treating the SI water value as a trustworthy absolute energy anchor, but the independently reported relative cis/trans TS/product differences do not require it. This conflict is retained, not cured by selecting a convenient water energy. The full plotted branch is a conditional reported author reference with this limitation, and neither view requires or scores absolute-profile reconstruction. The disclosed baseline explicitly presents the printed records and a source-record caution. The shared scientific question remains startable and evaluable on the reported relative outcomes.

The author model's gas-phase geometries/CPCM ether differ from the CPME experiments; the catalyst affinity thermochemical convention differs from the selectivity convention; only the lowest-energy TS conformer is used and the B1 sampling limitation is explicitly reported. No numerical uncertainty is supplied. Compare scientifically scoped trends and evidence, not method-independent exact energies.

## Paired views and shared evaluation

evaluation/reproduction_protocol.json contains the complete private guidance block and exact per-statement source ledger. Source scientific passages are retained verbatim, including their original text markup; a clearly labelled source-record caution is an evidence-bound builder inference, not falsely attributed to the authors. The paired-view tool inserts this block immediately before the public-input section. All remaining question text, identities, observations, data, submission templates, private evaluation references and scoring are shared. No lone reproduction variant is constructed.

Core outcomes C_CATALYST_FUNCTION, C_FIVE_MEMBERED_COMPETITION and C_RING_SIZE_RELATIONSHIP are the required scientific relationships, not quotas to use author methods. All Stage05 CR1-CR4 bind these outcomes and contextual references. S4 and the separately reported six-membered product stability are additionally source-bound contextual results; the immutable contract is not expanded or rewritten. Optional descriptors/mechanisms have no scoring rule or weight. Historical pre-V3 record (inactive): the rubric allocated 60 points to research quality and 40 to question resolution. Appropriate alternatives can earn full credit; merely matching the authors cannot. Honest unresolved work can earn process credit but not automatic resolution credit. Baseline execution/fidelity is considered only when guidance is public, with ambiguities and justified substitutions assessed within the same process rules.

## Current V3 final-result evaluation — 2026-10-27

Only the 4 independent final conclusions in scoring_rules.json are active, totaling 100 points. Historical route details and intermediate numbers above are source context, not scored completion requirements. Each criterion requires actual computation supporting its final claim; no process points or historical 60/40 split applies. Four final comparative explanations replace ten mixed V2 items; all original systems, D4 A/B and D4/D5 comparisons and K4 context remain. Existing parent-corrected pure-RRHO evidence is authoritative for coverage: D4 catalyst gap difference 0.088814 kcal/mol is only nominal; D5 product difference 5.517269 differs from source by +2.918602 and is soft-mode sensitive. No hard numerical windows existed or are introduced.

</details>

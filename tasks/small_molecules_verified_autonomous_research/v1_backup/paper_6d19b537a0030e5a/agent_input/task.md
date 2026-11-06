## Scientific objective

For the specified chiral cyclopentadienone–iron catalyst C_A, how does hydrogenation of phenyl(trimethylsilyl)methanone under H2 proceed to the chiral silyl alcohol, what controls turnover and the competition between alcohol enantiomers, how does the catalyst's molecular organization relate to these outcomes, and how does replacing trimethylsilyl with tert-butyl change enantiomer discrimination within the same catalyst system?

Develop and test a connected molecular explanation of this organic reaction. The scope is the specified C_A catalyst and primary acylsilane, with the matched tert-butyl substrate used to investigate the substitution/selectivity relationship.

## Public inputs and scientific boundaries

Use `data/inputs/system.json`. PI1 gives the primary and comparison substrate graphs; PI2 gives the alcohol constitutions; PI3 defines the C_A catalyst graph/stereochemistry, additive and experimental conditions and separates the distinct C_B comparison catalyst; PI4 supplies catalyst-specific endpoint observations and their limits. These are starting identities and observations, not a mechanism or a computational recipe. Generate your own starting models and declare any approximation.

Investigate reaction chemistry on C_A. C_B performance is context, not a C_A quantitative reference and not a requirement to calculate a second catalyst. Keep the matched substrate comparison on the same C_A scaffold. Do not extend the required question to unrelated substrates, catalyst synthesis, solvent-only transfer-hydrogenation pathways or new experiments. Endpoint yields and enantiomeric ratios do not define a rate law or time-dependent kinetic dataset. No major-product absolute configuration is supplied. Preserve explicit structures when assigning enantiomers; a common attack-face label alone does not determine product CIP labels.

## Required investigation

Propose testable explanations and choose informative models and investigations. Actually execute research that addresses the connected reaction account, turnover-controlling comparisons, catalyst organization/reactivity/selectivity relationship, competition between the primary-alcohol enantiomers, and the effect of the matched Si(CH3)3-to-C(CH3)3 substitution. Relate these outcomes rather than submitting only one energy, structure or descriptor. Choose the mechanistic hypotheses, physical effects and tests; no fixed number of hypotheses/tests, exhaustive conformer/pathway inventory or selected search/descriptor workflow is required. Explain which outcomes each investigation informs and retain or revise conclusions from its evidence.

Preserve actual inputs, outputs, logs and analysis code. Use evidence and scientific judgment in every claimed conclusion. Requirements follow the claims: transition-state claims need appropriate frequency and connectivity validation; spin-crossing, population or interaction claims need corresponding physical checks; a kinetic model, if chosen, needs equations, observation mapping and an identifiability assessment. These conditional checks do not prescribe a transition-state route, kinetic model or preferred explanatory method. Distinguish observations, computed conditional results and causal interpretations; report definitions, units, model conditions and uncertainty.

If author-provided scientific guidance is supplied, execute and critically assess that disclosed baseline, recording fidelity, ambiguities and justified substitutions in the existing investigation records and report. Otherwise choose the research approach independently; there is no obligation to follow an undisclosed author method or hypothesis. Both views require real work and defensible judgment.

## Deliverables and stopping conditions

Submit `report/results.json`, `report/report.md` and `research/` exactly as specified in `submission_schema.json` and `submission_guide.md`. Use resolving hypothesis/investigation/evidence/conclusion IDs and real artifact links. The report should integrate all the scientific outcomes above, explain evidence-based decisions and limitations, and state actual resource use; raw artifacts belong under `research/`. Do not replace execution with proposed calculations or fabricated outputs.

Stop when evidence supports the conclusions actually claimed and their uncertainty is stated. No fixed CPU, GPU, memory, walltime or job-count quota is imposed. Research completion and question resolution are different: report `research_status` and `question_status` according to the guide. Honest partial work or execution failure is acceptable when attempts and limitations are documented. Substantive inconclusive research can earn research-quality credit without establishing a solved mechanism or automatic question-resolution credit. Agreement with a reference answer alone is insufficient; a well-supported alternative can resolve the question.

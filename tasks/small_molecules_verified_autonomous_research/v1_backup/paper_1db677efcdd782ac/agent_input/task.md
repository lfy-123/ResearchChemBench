## Scientific objective

How does the molecular reactivity of the specified N-cyclopropyl tetrahydropyridines account jointly for their light-dependent oxidation, substituent- and stereochemistry-dependent cyclopropane cleavage versus retention, cis/trans interconversion, and substrate-deuterium incorporation into an aldehyde, while remaining consistent with the listed related tetrahydropyridine oxidation comparators?

Develop an evidence-supported molecular explanation for this connected oxidation problem, not just an isolated energy or a restatement of the observed products.

## Public inputs and scientific boundaries

Use `data/inputs/system.json`. It gives the exact starting identities and relative stereochemistry of S_H, S_Mcis, S_Mtrans and S_Ptrans, the S_HD4 isotope-label positions, the related T_H/T_Ph/T_Pyr comparison structures, reaction conditions and qualitative observations. The molecules are defined by their graphs, not by a supplied optimized geometry. Only relative cyclopropane stereochemistry is specified.

The linked scientific scope is molecular oxidation accessibility in the comparator context, substitution/stereochemistry effects on cleavage and retention, the observed methyl-substrate interconversion, and an isotope-compatible account of the aldehyde and intact-ring products. S_Mtrans is a comparison structure, not a source of an independently measured trans-started product distribution. Product aldehyde alkene stereochemistry and an exact isotope fraction are not prediction targets.

This is computational research; no new laboratory experiment is required. Aerobic observations and flavin regeneration provide context, but a complete photophysical, oxygen/peroxide, flavin-turnover or enzyme mechanism is outside the required scope. Likewise, a quantitative solution rate/yield model or a unique hydrogen-transfer kinetic route is not required. Do not silently introduce missing experimental parameters or treat comparator behavior as a measured oxidation potential for another molecule. State any additional modeling assumptions and the conclusions they can support.

## Required investigation

Propose testable molecular explanations and choose models and informative computational investigations that distinguish or assess them. You decide which states, physical effects, structures and comparisons matter. Actually execute the chosen investigations and preserve real inputs, outputs, logs and analysis code. Record each investigation's purpose, method, outcome and evidence-based next decision. Retain, revise or reject explanations according to what the resulting evidence supports. No fixed number of hypotheses, calculations, conformers or pathways is required.

Address the linked scientific purposes together: oxidation/light-dependence comparator consistency; comparative cleavage/retention reactivity across the specified substituents and methyl stereoisomers, including compatibility with the retained-ring phenyl product; methyl cis/trans interconversion; and substrate-label incorporation into an aldehyde. A descriptor alone or one energy without an account of these relationships is insufficient. You need not use any particular descriptor, intermediate, pathway, electronic-structure method or search procedure.

Validation requirements follow your claims. A claimed transition state needs appropriate frequency and reaction-connectivity validation; a claimed minimum needs appropriate stationary-point and identity checks. If you use a kinetic model, supply its equations, mapping to the available observations and an identifiability assessment. Such claims and models are not mandatory. Distinguish molecular energy comparisons, kinetic accessibility, observed product amounts and proposed explanations; do not infer one from another without evidence. Compare only clearly mapped objects, states, energy conventions, units and conditions.

When author-provided scientific guidance is publicly supplied, execute and critically assess that disclosed baseline, recording protocol fidelity, ambiguities and justified substitutions in the investigation records and readable report. When it is not supplied, choose your own approach: undisclosed author methods, descriptors and hypotheses are not requirements and their omission is not a score deduction. In either view, agreement with a reference alone is insufficient; actual evidence and scientific judgment are required.

## Deliverables and stopping conditions

Submit `report/results.json`, `report/report.md` and `research/` exactly as defined by `submission_schema.json` and `submission_guide.md`. Include real artifacts and linked hypotheses, investigations, evidence, conclusions, limitations and reproducibility information. The readable report should explain the integrated scientific account, which comparisons are supported, what remains uncertain, any failed attempts, and actual resource use. Follow the guide's stable-ID and artifact-link requirements.

Research completion and scientific resolution are different. Set `research_status` to `complete`, `partial` or `execution_failed` and `question_status` to `resolved`, `partially_resolved` or `unresolved` according to the evidence, not aspiration. Honest partial or failed execution is acceptable with attempted inputs and logs; completed research may leave the question unresolved. Unsupported or unexecuted mechanisms are not resolved answers.

Stop when actual evidence supports the conclusions you claim within stated modeling boundaries and remaining uncertainty is explicit. No fixed CPU, GPU, memory, walltime or job-count quota is imposed, and no exhaustive conformer or pathway network is demanded.

The shared evaluation assigns 60 points to research quality and 40 to scientific question resolution. Within resolution, oxidation/light-dependence comparator consistency contributes 8 points, comparative cleavage/retention and product compatibility 18, methyl stereochemical interconversion 10, and isotope-compatible hydrogen provenance 4. Well-supported alternatives are eligible; unresolved aspects do not automatically receive resolution credit. Optional author descriptors, spectral recipes and conditional interpretations have no separate score.

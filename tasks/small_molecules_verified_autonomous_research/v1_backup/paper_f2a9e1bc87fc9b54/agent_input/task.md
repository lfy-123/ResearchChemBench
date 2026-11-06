## Scientific objective

For the base-promoted N-alkylation of 3-nitro-1H-pyrrole with propargyl bromide in DMF, what computed chemical behavior best describes formation of N-propargyl-3-nitropyrrole, and which computed energetic and structural features support that description?

Investigate the complete conversion of the specified starting system into the stated observed product. Establish a chemically coherent explanation for the transformation and assess its energetic and structural support: what accounts for product formation, where does the evidence place energetic difficulty, and what can be concluded about the net tendency for product formation? The product identity is given; the molecular route is not.

## Public inputs and scientific boundaries

Use `data/inputs/system.json` as the authoritative starting facts:

- PI1 (identity): 3-nitro-1H-pyrrole is the pyrrole substrate for the N-alkylation reaction.
- PI2 (identity): Propargyl bromide is the alkylating reagent used to form N-propargyl-3-nitropyrrole.
- PI3 (identity): The product is N-propargyl-3-nitropyrrole, also named 3-nitro-1-(prop-2-yn-1-yl)-1H-pyrrole.
- PI4 (condition): The reaction is conducted with sodium hydride in N,N-dimethylformamide at room temperature for 24 h.
- PI5 (observation): The isolated product was obtained as light-yellow crystals in 89% yield and characterized by NMR, IR, and LC-MS.

The product and isolation observation identify the phenomenon to explain, not an elementary mechanism. Isolated yield and reaction duration are not rate constants or direct measures of an elementary barrier. Stay within the molecular organic conversion of this substrate and alkylating reagent with the stated base and solvent. Other synthetic transformations, catalyst systems and biological applications are outside the question. Choose and justify suitable representations of the stated system; no starting geometry is prescribed.

## Required investigation

Develop testable explanations for the complete conversion and choose models and computational investigations that can discriminate between, support or constrain them. Choose what deserves investigation from the scientific question; no fixed number of hypotheses, tests, structures or routes is required. A familiar reaction-type label alone is not a computed explanation.

Actually execute the chosen research. Retain the constructed molecular inputs, model settings, raw outputs, execution logs and any analysis code. Explain how the evidence leads you to retain, revise or reject explanations. Account for the chemical roles of the starting substrate, base and alkylating reagent in the connected explanation, and describe the supported connectivity changes. Supply energetic and structural evidence relevant to the whole conversion rather than an isolated calculation unrelated to the proposed account.

Declare the assumptions that matter for your model and interpretation, including species and charge accounting, solvent representation and energy references where applicable. Define numerical quantities, units, conditions and any known or unknown correction conventions. Distinguish activation-related difficulty from overall thermodynamic tendency and separate computed results, supplied observations and interpretations. Do not infer a quantitatively established reaction rate from the isolation observation.

Validation requirements follow the claims you make. A claimed transition state needs appropriate frequency and connectivity evidence; explicitly identify an unvalidated candidate as such. Support other structural or energetic claims with checks suitable to those claims. Do not fabricate unavailable outputs or validation. Exhaustive pathway or conformer enumeration and a particular search method are not required.

If author-provided scientific guidance is supplied, execute and scientifically assess the disclosed baseline and record protocol fidelity, ambiguities and justified substitutions in the investigation records and readable report. If no such guidance is supplied, choose the research approach independently; no undisclosed author method or explanation is required.

## Deliverables and stopping conditions

- `report/results.json`: records conforming to `submission_schema.json`, with stable hypothesis, investigation, evidence and conclusion IDs linked to actual artifacts.
- `report/report.md`: a readable account of the chemical problem, chosen explanations and models, executed work, supported connected conclusions, uncertainty, limitations and actual resource use.
- `research/`: the actual molecular inputs, raw outputs, logs and analysis code needed to inspect and reproduce the submitted work.

Follow `submission_guide.md` and the shared schema exactly. Research completion and question resolution are separate: use `research_status` to report complete, partial or execution_failed work, and `question_status` to report resolved, partially_resolved or unresolved conclusions, as defined in the guide. A status label or plausible explanation without linked executed evidence does not establish resolution.

Stop when the evidence supports the scope of the claimed conclusions and the remaining uncertainty is stated, or when honestly documented attempted work reaches a limitation that leaves the question unresolved. No fixed CPU, GPU, memory, walltime or job-count quota is imposed. Partial work, inconclusive conclusions and genuine execution failures are acceptable when documented with the actual inputs and logs; do not claim that an unresolved mechanism has been solved.

Assessment allocates 60 points to research quality and 40 points to evidence-supported resolution of the connected chemical explanation and its energetic/structural support. Agreement with an author result alone is insufficient. Well-supported alternative conclusions are eligible for the same credit; honest unresolved work can earn research-quality credit without automatically earning question-resolution credit. No optional author descriptor or undisclosed route is required for credit.

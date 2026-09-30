# Scientific objective

For the source Ru–bda–Py nitrogen-containing model, what local molecular chemistry can support N–N bond formation with ammonia, and what role, if any, can be established for the ligand environment?

# Author-provided scientific guidance

The source attributes the bda model's behaviour to N–O stabilization in15bda, a6.2kcal/mol opening step viaTS3bda, and a21.9kcal/mol direct NH3-attack barrier; after opening, a downhill electronic scan is interpreted as diffusion-controlled attack (main pp9–10; SI FiguresS55–S57). Forbcs, a dangling sulfonate is proposed to assist proton transfer during N–N formation. These are source assignments to reproduce/audit, not compulsory correct conclusions. SI PDFp47 specifies Gaussian16 B3LYP-D3(BJ), SDD(Ru)/6-31G(d,p) optimization and frequencies, def2-TZVP single points withSMD MeCN and298.15K Gibbs corrections; source standard-state corrections include1atm→1M, solvent concentration19.2M, Fc absolute4.548V and specified proton reference. Keep electrochemical/proton reservoirs distinct from chemical barriers. The supplied source model inventory does not certify a singlet or N–O minimum; raw modes/endpoints are needed for a saddle claim. Additional bda/bcs paired routes were benchmark development choices, not all source calculations.

# Public inputs and scientific boundaries

The source studies ammonia oxidation inMeCN and uses pyridine-ligated computational models related to the experimental catalysts. The neutral bda and bcs catalyst frameworks contain oneRu, one dianionic bipyridyl ligand and two pyridines. The local nitrogen-containing composition adds oneN to that framework, netcharge+1. Charge is an electron-inventory definition; oxidation-state assignment, spin, ligand coordination and any N–O bond are unknown features to investigate. NH3 is the incoming molecular reagent. Source calculations refer to298.15K; redox thermodynamics use0.50V vsFc+/0 and aMeCN pH reference15.1, which are not automatically chemical activation barriers.

The local nitrogen-containing Ru–bda–Py composition used in the paper is the target; the source Ru–bcs–Py analogue is available for scientifically justified comparison. Investigate local structure, reactivity and explanatory limits. A full electrocatalytic cycle, device performance, turnover frequency or a claim about the global rate-determining step is outside scope.

Use data/inputs/systems.json, observations.json and source_facts.json together with any molecular files listed there. Starting coordinates are only supplied model inputs, not certified minima or mechanistic answers.

# Required scientific validation/investigation

Reproduce and assess the disclosed author baseline for this question. Preserve the supplied protocol where specified; document ambiguities and scientifically justify controlled substitutions. Choose additional models, methods, searches and tests as needed to assess that baseline. No fixed number of extra hypotheses or controls and no author winner is required by the shared scientific-result criteria. Material conclusions need newly generated, reproducible quantitative evidence or analysis that addresses the stated question; repeating the supplied observations is insufficient. Record brief purposes before execution where the managed trace permits, actual outcomes and consequential revisions. Do not supply private chain of thought.

Preserve inputs, raw outputs, analysis code and object/state mapping. Requirements follow the claims: a claimed transition state needs defensible saddle and connectivity evidence; a constrained structure is not a free minimum; a thermodynamic result alone does not establish a rate or unique mechanism. If those claims are not made, those particular artifacts are not mandatory. Explain model validity, important confounding and uncertainty using evidence appropriate to the method. Do not invent precision or a reference tolerance. Supported, contradicted and well-investigated unresolved conclusions are assessed on their evidence. A missing investigation is not an identifiability result.

This task provides the necessary public source facts. Use the disclosed author guidance and public facts; do not access undisclosed article/SI, private evaluator or prior run archives. All supplied observations are already visible; any retrospective validation is not a blind prediction. The benchmark exposes managed scientific/data actions, software-native execution and agent-authored programs; discover available capabilities and resource limits from the runtime. The disclosed source software/protocol defines the reproduction baseline; justify unavailable or underspecified components and any substitutions. No fixed core-hour budget is imposed here. Report actual resource use.

# Deliverables

Submit report/results.json and a readable report/report.md following submission_schema.json and submission_guide.md. Include the research question, agent-defined objects/models/methods, actual records, auditable quantities, evidence-linked claims and validity checks, decision updates, uncertainty, limitations and resource accounting. Complete, partial and bounded_failure are distinct; schema acceptance never certifies scientific completion.

# Scientific objective

What can molecular evidence establish about the relative intrinsic reactivity of ODA, 6FODA and PFMB toward trimesoyl chloride, and how far does that evidence support interpretation of their interfacial polymerization?

# Author-provided scientific guidance

The source interprets monomer reactivity using molecular electrostatic potential, average local ionization energy, Fukui/LEAE information and a frontier-orbital nucleophilicity index; the reported indices are ODA 4.26, 6FODA 3.68 and PFMB 3.56 eV (main p3; formal SI pp20–22). These are descriptors, not elementary rate measurements. Formal SI p10 reports ORCA 5.0.4, B3LYP-D3BJ, def2-SVP optimization followed by def2-TZVP single points, AutoAux, and gfn2-xTB conformer screening. A later methods paragraph on p11 describes vacuum optimization and single points with def2-TZVP, so the source is not fully unambiguous; record the protocol chosen and its effect rather than inventing a single exact protocol. Reproduce and assess the disclosed molecular descriptor baseline or justify controlled substitutions, then determine what mechanistic/kinetic interpretation it warrants. V1 first-acylation TS, chloride proton acceptor and strain matrix were benchmark additions, not established source reaction-path calculations. Polymer MD and measured membrane properties address other scales.

# Public inputs and scientific boundaries

ODA, 6FODA and PFMB are the source aromatic diamines; TMC is the acyl chloride comonomer. The source produces films using each diamine, with different measured film properties. No elementary rate constant or reaction-path measurement is supplied. Supplied structures define chemical identities, not a conformation, intermediate, reactive site ranking or mechanism. The polymerization context includes transport and medium effects that need not be captured by a molecular model.

Address the molecular reactivity of the three specified diamines and trimesoyl chloride (TMC). The source forms polyamide films at an ionic-liquid/water–hexane interface; this task selects the local molecular question. State the environment and chemical state represented by each model. Do not infer membrane permeability, salt rejection, bulk crosslink density or an interfacial rate from isolated-molecule quantities alone.

Use data/inputs/systems.json, observations.json and source_facts.json together with any molecular files listed there. Starting coordinates are only supplied model inputs, not certified minima or mechanistic answers.

# Required scientific validation/investigation

Reproduce and assess the disclosed author baseline for this question. Preserve the supplied protocol where specified; document ambiguities and scientifically justify controlled substitutions. Choose additional models, methods, searches and tests as needed to assess that baseline. No fixed number of extra hypotheses or controls and no author winner is required by the shared scientific-result criteria. Material conclusions need newly generated, reproducible quantitative evidence or analysis that addresses the stated question; repeating the supplied observations is insufficient. Record brief purposes before execution where the managed trace permits, actual outcomes and consequential revisions. Do not supply private chain of thought.

Preserve inputs, raw outputs, analysis code and object/state mapping. Requirements follow the claims: a claimed transition state needs defensible saddle and connectivity evidence; a constrained structure is not a free minimum; a thermodynamic result alone does not establish a rate or unique mechanism. If those claims are not made, those particular artifacts are not mandatory. Explain model validity, important confounding and uncertainty using evidence appropriate to the method. Do not invent precision or a reference tolerance. Supported, contradicted and well-investigated unresolved conclusions are assessed on their evidence. A missing investigation is not an identifiability result.

This task provides the necessary public source facts. Use the disclosed author guidance and public facts; do not access undisclosed article/SI, private evaluator or prior run archives. All supplied observations are already visible; any retrospective validation is not a blind prediction. The benchmark exposes managed scientific/data actions, software-native execution and agent-authored programs; discover available capabilities and resource limits from the runtime. The disclosed source software/protocol defines the reproduction baseline; justify unavailable or underspecified components and any substitutions. No fixed core-hour budget is imposed here. Report actual resource use.

# Deliverables

Submit report/results.json and a readable report/report.md following submission_schema.json and submission_guide.md. Include the research question, agent-defined objects/models/methods, actual records, auditable quantities, evidence-linked claims and validity checks, decision updates, uncertainty, limitations and resource accounting. Complete, partial and bounded_failure are distinct; schema acceptance never certifies scientific completion.

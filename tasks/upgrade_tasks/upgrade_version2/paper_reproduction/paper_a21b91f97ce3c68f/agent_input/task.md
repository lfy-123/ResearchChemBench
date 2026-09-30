# Scientific objective

How does molecular conformation affect one-bond 119Sn–13C coupling in the three supplied stannyl heterocycles, and what evidence explains any differences between the scaffolds?

# Author-provided scientific guidance

The authors used CREST/GFN2-xTB conformer sampling, selected low-energy axial/equatorial structures, then Gaussian16 GD3-B3LYP/def2-TZVPP gas-phase optimizations/frequencies and NBO3.1. They computed spin–spin response with a TZP-ZORA basis, nmr=(spinspin,mixed,readatoms), and integral=NoXCTest; main p.2 explicitly calls the Hamiltonian nonrelativistic despite the basis label. They correlated antiperiplanar donation with coupling and applied a mean empirical factor −1.419 to some absolute Sn–C predictions (SI S5). This source factor is not a benchmark acceptance tolerance. Source6,7,13 occur in SI S5–S6. The fixed torsion/distance interventions in V1 were later controls, not author protocol; reproduce the disclosed baseline or justify alternatives and design extra tests independently.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Study complete neutral SnBu3 derivatives6(C17H36OSn),7(C16H34O2Sn) and13(C16H34S2Sn). Supplied graphs distinguish the ring carbon from the three butyl carbons bonded to Sn. Investigate conformation-dependent one-bond coupling with a declared isotope/sign/reference convention. The question is not a survey of every source scaffold.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Identify the actual 119Sn–13C pair and distinguish ring-carbon coupling from an average over butyl carbons. State signed versus magnitude convention, response method and relativistic Hamiltonian treatment separately from basis naming. Conformation labels require structural evidence; any population-averaged coupling needs justified populations.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

A correlation of coupling with one orbital descriptor is not a causal decomposition. A ZORA-compatible basis name does not establish that the Hamiltonian included ZORA. Empirical source scaling cannot be treated as a universal physical correction without calibration.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

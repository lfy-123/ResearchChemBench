# Scientific objective

Which excited-state relaxation pathways are supported by molecular electronic evidence for the four supplied emitters, and how does aromatic substitution affect that assessment?

# Author-provided scientific guidance

The authors used Gaussian09W gas-phase TD-B3LYP/6-31G(d,p), then Multiwfn NTO/IFCT analysis with phenanthrimidazole, methylphenyl and appended aromatic/benzene-bridge fragments. SI pp.2–6 reports ten singlet and ten triplet states. Main p.3 interprets the S1 states as mixed local/charge-transfer and proposes high-lying-triplet RISC: T4 for Ph/Na and T3 for An/Py; reported S1–T1 gaps are 0.88, 0.89, 1.34 and 1.11 eV. These are author hypotheses/references, not measured rates. Main p.3 prints Py S1 CT/LE percentages 57.23/45.77 (sum103) and An T3 percentages50.09/49.01 (sum99.10). Reproduce definitions and report these inconsistencies rather than enforce either pair as truth. Later benchmark SOC, 20-state overlap, 45-degree constraints and CAM-B3LYP calculations are additional validation, not the original protocol.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Study neutral Ph-mP (C34H24N2), Na-mP (C38H26N2), An-mP (C42H28N2) and Py-mP (C44H28N2) as defined by the complete atom-mapped graphs. Delimit the geometry, medium and electronic approximation of each result. Any extrapolation from isolated molecules to solution or devices requires separate evidence.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Track states by their physical character when comparing geometry or method changes; a root number alone is not an identity. Define every charge-transfer or localization metric and its normalization. A claimed relaxation pathway needs evidence appropriate to its energy, coupling and environmental assumptions.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

Near-degenerate singlet/triplet energies or mixed transition character alone do not establish a transition rate, kinetic dominance or device efficiency. Do not convert isolated-molecule evidence into a quantitative OLED efficiency claim.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

# Scientific objective

What electronic and structural features can account for the short Ir–Ir bond in the supplied iminoxolene dimer, and how far can a molecular model support that explanation?

# Author-provided scientific guidance

Source main p.4 used gas-phase Gaussian16 B3LYP, SDD on Ir and6-31G* on other atoms. For the dimer the actual calculated model is (A,C)-(Hap)4Ir2, Hap=1,2-C6H4(NH)O,54 atoms; egan truncations were used for other mononuclear complexes. Main pp.8–9 argues that ligand redox activity and relative orientation create net Ir–Ir π bonding. The source S4 minimum has Ir–Ir2.599 Å; the constrained C2h structure has2.724 Å and9.7 kcal/mol higher free energy. SI pp.22,29 identify C2h as a first-order saddle (17.1i cm−1), not a second stable conformer. Frequency plots use scaling0.9614; SI coordinate energies are raw optimized energies, not automatically the9.7 kcal/mol free-energy difference. The experimental2.5584(4) Å and crude MOS-derived2.34 bond-order estimate are conditional observations/interpretations, not mandatory computational truth. The V1 full/egan pair and fixed perturbations are benchmark additions, not the published Hap protocol.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

The experimental neutral dimer is (A,C)-(Egan)2Ir2, C88H104Ir2N4O12. Complete Egan connectivity and the smaller neutral Ir2(Hap)4 core, C24H20Ir2N4O4, are supplied as molecular representations. Choose and justify the representation adequate for the bonding question, preserving two metals and four iminoxolene N/O donor units. The smaller core is not the full experimental molecule.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

State the model composition, electron count, charge, electronic description and relation to the experimental dimer. A bonding explanation needs electronic evidence beyond a bond length. If comparing deformations or fragments, keep composition, state, reference and constraints consistent and distinguish minima from saddles.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

A short distance or an empirical oxidation-state estimate alone does not establish an exact bond order. An electronic result on Hap or egan cannot silently be reported as a full Egan calculation. A constrained stationary point is not automatically a metastable conformer.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

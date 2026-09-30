# Scientific objective

How does the donor substitution pattern affect the molecular excited-state behavior of TD-2T, CD-2T and TD-2C, and which aspects of their differing optical response can be supported by molecular evidence?

# Author-provided scientific guidance

Main pp.2–4 describes Gaussian09 B3LYP/6-31G(d,p) S0 optimization and TD-DFT S1/T1 energies, with Multiwfn3.8 NTO analysis. The SI Experimental section instead writes B3LYP/6-31(d); this basis-description discrepancy must be recorded rather than silently erased. The authors attribute donor-dependent optical behavior to donor–acceptor geometry, charge-transfer character and low singlet–triplet separations. Main p.4 reports calculated TD-2T gap 0.34 eV and discusses CT/LE/HLCT characters; spectroscopic gaps at 77 K are a separate experiment, not identical to vertical TDDFT. The source also discusses device performance, which exceeds what a molecular calculation alone can reproduce. Reproduce a clearly stated interpretation of the disclosed molecular baseline and explain deviations. The old fixed-45-degree and paired-conformer benchmark design was added later and is not an author requirement.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Use the complete neutral molecular graphs TD-2T (C72H49N7), CD-2T (C72H47N7) and TD-2C (C72H45N7). Solution optical observations are supplied as empirical context with conditions; electronic-state assignments and explanations are to be established. The task does not ask for OLED efficiency or a solid-film orientation prediction.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Preserve the mapped full structures and distinguish the three donor connectivities. State what geometry, state and environment each excitation quantity describes. Track state character consistently when comparing models; vertical transitions, spectral maxima and adiabatic gaps are different observables. A claimed rate or spin-conversion pathway requires evidence beyond a favorable energy gap.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

Isolated-molecule oscillator strengths, orbital separation or SOC do not by themselves prove delayed-fluorescence yield, device efficiency or film orientation. Empirical PL maxima do not disclose a unique state assignment or mechanism.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

# Scientific objective

How do fused-ring topology and substituent identity affect the low-energy electronic character of the four supplied hydrocarbon models, and what evidence explains the differences or their absence?

# Author-provided scientific guidance

The authors optimized the four truncated models using Gaussian09 (U)B3LYP-D3/def2-SVP and checked frequencies (SI p.42). Long alkoxy chains were replaced by OMe and the TIPS computational group by ethynyl-SiH3. They used GIAO NICS(1)zz and EDDB to interpret aromaticity. Main p.4 reports OSS below CS for 2M_OMe/2M_TIPS by 4.5/5.6 kcal/mol and above CS for 1M_OMe/1M_TIPS by 4.1/3.3 kcal/mol. These are conditional author results, not universal acceptance bounds. Coordinate-section energies include ZPVE and must not be conflated with raw SCF energies. The source TD-DFT optical comparison includes oxidized 2M-prime, a different molecule. V1 added fixed BS seeds, common-scaffold interventions and extra method controls; these were not the source protocol.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Study neutral 1M_OMe (C56H42O2), 1M_TIPS (C58H42Si2), 2M_OMe (C58H44O2) and 2M_TIPS (C60H44Si2) under declared molecular conditions. These are explicitly truncated source models: OMe replaces the long alkoxy chain and the historical TIPS model name denotes an ethynyl-SiH3 group, not full triisopropylsilyl. Do not silently change these chemical identities.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Specify composition, charge, electronic state, energy definition and structural status for every comparison. Electronic-character claims require appropriate wavefunction or density evidence. A converged calculation is not automatically a stable state; collapsed starts count as evidence about the search, not separate states.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

Absolute energies of different elemental compositions do not rank their electronic states. A spin density or aromaticity descriptor does not by itself prove an oxidation rate or air stability. Optical data for oxidized 2M-prime cannot validate unoxidized 2M excitations.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

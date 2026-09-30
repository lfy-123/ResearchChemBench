# Scientific objective

Determine whether axial-pyridine substitution produces resolvable changes in the molecular magnetic exchange of the three supplied copper dimers, and what the evidence supports about that dependence.

# Author-provided scientific guidance

The source used Cu2(AnCOO)4(4-RPy)2 models for H/Me/OMe. It approximated the open-shell singlet geometry by triplet DFT optimization with B3LYP-D3BJ/def2-SVP in ORCA (RIJCOSX and def2/J). It obtained singlet/triplet spin-flip energies using multicollinear SF-TDDFT in PySCF-forge, with the same main functional/basis and def2-svp-jkfit; the reference is the Sz=1 triplet. The source defines J=E_S−E_T and reports approximately −335, −342 and −345 cm−1, with more electron-rich axial pyridines associated with stronger antiferromagnetic coupling. SI S35–S36 examines functional, TDA, basis and geometry dependence; these small differences are conditional, not universal tolerances. The experimental material fits are distinct from the molecular calculations. The old benchmark common-core decomposition and independent calibration matrix were later task additions, not the author protocol. These operations are not a mandatory route in this version. Source: main PDF pp.6–7; SI S5–S6 and S35–S36.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Study neutral Cu2 paddlewheel dimers containing four bridging 9-anthracenecarboxylates and two equivalent axial pyridines bearing H, 4-methyl or 4-methoxy substitution. The public identity file specifies ligand graphs and stoichiometry. State the spin Hamiltonian, energy reference and units used for exchange. Molecular conclusions must remain distinct from material magnetic or optical responses.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Keep all four anionic bridges and both axial ligands unless explicitly studying a justified model with its limitations. Identify the electronic states represented by each energy, demonstrate relevant state validity, and make any spin projection and exchange convention auditable. Comparisons of substitution effects require comparable definitions and physical conditions.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

A single dimer gap does not establish the substitution dependence. Molecular exchange alone cannot prove MOF thermochromism, photoconversion or a bulk transition. Do not interpret different spin-Hamiltonian factors or inconsistent correlation conventions as chemical trends.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

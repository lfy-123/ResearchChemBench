# Scientific objective

What molecular electronic evidence can explain differences in triplet sensitization among IR780, Cy1 and Cy2, and does it support their energetic compatibility with rubrene in chloroform?

# Author-provided scientific guidance

Gaussian16 calculations used B3LYP/6-31G(d,p) with SMD chloroform, SDD for iodine and def2TZVP for selenium; iodide counterions were omitted (SI pp.7–8). The authors used DFT ground-state structures, TDDFT excited-state calculations and Multiwfn electron–hole analysis, emphasizing selenium contributions. Main p.6 reports UDFT adiabatic T1 energies1.02,1.02,1.09 eV for IR780,Cy1,Cy2 and1.00 eV for rubrene, noting systematic underestimation relative to rubrene experiment1.14 eV. The authors propose S1→T2 ISC from energy gaps and a heavy-atom SOC argument; the cited source does not provide a direct molecular SOC matrix proving the rate. Reproduce this disclosed baseline or justify substitutes; explicit SOC, planar constraints and matched extra controls in V1 were later validation, not source measurements.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Use the complete IR780 (C36H44ClN2+), Cy1 (C34H38ClI2N2+) and Cy2 (C27H29N2O2Se2+) cation graphs and neutral rubrene (C42H28). The source molecular model excludes counterions. Solution context is chloroform; experimental upconversion mixtures were argon-saturated, with10 μM sensitizer and1.5 mM rubrene. Keep this measurement context distinct from an isolated-molecule calculation.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Declare state identity, geometry and energy reference for each excited-state quantity. For an energy-transfer claim, use compatible donor/acceptor definitions and state the sign of the driving energy. Explain heavy-element treatment and whether the evidence concerns a coupling, a transition probability or a kinetic rate.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

A selenium atom population or atomic-number scaling argument alone does not measure molecular SOC or establish an ISC rate. Correlated donor/acceptor error cancellation must be examined, not assumed. Molecular energetics alone do not prove solution upconversion efficiency or a film mechanism.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

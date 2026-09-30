# Scientific objective

Does cage isomerism change the molecular spin response to vibrations in the supplied Y2@C80(CH2Ph) radicals, and what can that evidence explain about differences in spin-lattice relaxation?

# Author-provided scientific guidance

The source used ORCA PBE/def2-TZVP with a Dolg Y ECP for structures and Hessians, and PBE-ZORA with ZORA-adjusted def2-TZVP for g and hyperfine tensors. It differentiated tensor components numerically along 23 low-frequency modes, fitting a quadratic response (SI Figure S16 on p.20 and Table S3a–d on pp.21–24). Main pp.8–10 associates low-frequency metal motion with relaxation and uses thermal weighting; it reports lower lateral frequencies for Ih than D5h and a qualitative faster Ih relaxation. The source explicitly omits expensive mixed derivatives and electronic excitations and does not claim exact T1 prediction. Reproduce this disclosed baseline where feasible, or explain justified substitutions. The old benchmark three-class ±h/±h/2 and fixed-temperature matrix was a later validation design, not a source requirement.

The author protocol is a disclosed reproduction target; any additional verification you design is your own work. Explain faithful reproduction, justified deviations and the impact on the conclusion. An author number is not evidence of successful reproduction.

# Public inputs and scientific boundaries

Compare the two supplied neutral C87H7Y2 molecular isomers in their radical doublet setting. Structures are source-computed starting geometries, not fresh experimental coordinates and not validated force-constant/tensor solutions. The target is molecular vibration–spin response and its relevance to relaxation trends; no absolute bulk relaxation lifetime is required.

Read `data/inputs/problem_context.json` and its listed data files. Supplied observations are facts with stated uncertainty; supplied coordinates are labelled by origin, not certified solutions. You choose the research models and evidence needed to answer the question.

Use the public data and the author guidance above. Private evaluator and verification archives remain outside the submission inputs.

# Required scientific validation/investigation

Develop and execute a defensible investigation of the question. Make your own choices about explanations, models, candidate states or structures, research design, comparisons and stopping. Justify those choices with actual evidence and revise them when evidence warrants it. For AR, no prescribed hypothesis count, method sequence or control matrix applies. For PR, reproduce the disclosed author baseline or justify an applicable substitute and its consequences; additional investigations remain independently designed.

Keep the full 96-atom C87H7Y2 identity, neutral charge and radical state explicit. For tensor or vibrational comparisons, document coordinate frames, atom mapping, tensor conventions and normalization. If inferring derivatives or thermal relevance, validate the chosen numerical representation and its uncertainty rather than confusing axis rotations with physical response.

Use actual source-linked artifacts. Check objects, atom/electron/charge balance, units and state/energy references. If a claim relies on a minimum, electronic-state assignment, constrained comparison or parameter inference, inspect the appropriate raw convergence/curvature/state/identifiability evidence. Common result validity does not mandate one program, hypothesis count or control matrix. PR process assessment still considers faithful reproduction of the disclosed baseline and justified deviations. Self-written timestamps do not prove prospective decisions. An unattempted alternative is not evidence of equivalence.

Tensor modulation or thermal weighting alone does not give a calibrated T1. Claims about absolute relaxation require the additional dynamical/environmental evidence they depend on. Do not substitute Gd species or treat an imaginary/rotational mode as a verified physical vibration.

# Completion and allowed outcomes

A complete answer can support, refute or delimit the phenomenon with sufficient evidence. Distinguish justified non-identifiability from missing work. Report partial progress or bounded failure honestly with specific release conditions. Numerical references and semantic scoring remain under calibration; prior benchmark PASS does not transfer.

# Deliverables

Submit `report/results.json` and readable `report/report.md` under the submission schema. Include actual objects/conditions, methods, research records, quantitative findings, uncertainty, claims and linked raw artifacts. The schema permits your own branches and metrics. Preserve complete evidence in workspace-relative files and disclose resource use.

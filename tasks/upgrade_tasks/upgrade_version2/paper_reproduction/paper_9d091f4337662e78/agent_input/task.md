# Scientific objective

Determine what absolute configuration, if any, is supported at the unresolved stereocentre of compound 1 by its known constitution and experimental ECD in methanol. Design an investigation that distinguishes a defensible configurational assignment from an assignment that the available spectral and molecular evidence cannot resolve.

# Author-provided scientific guidance

The authors assigned compound1 as 1′S by comparison with experimental ECD (main p4 Figure2). Main p7 reports Spartan14/MMFF94 initial sampling, a10kcal/mol window, M06-2X-GD3/6-311G(d,p) optimizations and frequency checks, gas-phase M06-2X-GD3/6-311+G(2d,p) energies with thermal corrections, and298.15K Boltzmann populations. Conformers over1% were retained for CAM-B3LYP/6-31+G(2d,p) TD-ECD in methanol IEFPCM and SpecDis1.70.1 averaging. SI TableS1 lists16 source conformers; the gas-phase weighting and solution excitation calculations are distinct steps. The former benchmark’s independent dual search, fixed broadening/energy windows and held-out band were added controls, not a disclosed author protocol. Reproduction must evaluate rather than simply repeat the S label.

Reproduce the disclosed author baseline within this scope, or justify a substitute scientifically and assess its consequences. Clearly distinguish this reproduction from your additional investigation. Source conclusions are conditional evidence, not an answer that must be affirmed; scientifically justified corrections or unresolved results remain eligible. The V1 benchmark interventions were not part of the author protocol and are not required in this version.

# Public inputs and scientific boundaries

Study compound 1 with its supplied constitution, known E alkene and one unresolved absolute stereocentre at atom map17. The neutral molecular identity has formula C24H24N2O4 and singlet multiplicity. Methanol is the ECD medium. The source experimental trace is approximate digitized data; it is not a calculated answer. Other natural products, synthesis and biological activity are outside this task. Any molecular model or stereochemical change must be related explicitly to this constitution.

Read `data/inputs/systems.json`, `problem_facts.json` and the observational files listed below. These are identity/observation inputs, not an optimized starting-answer set.

- `data/inputs/ecd_observation_provenance.json`
- `data/inputs/experimental_ecd.csv`
- `data/inputs/problem_facts.json`
- `data/inputs/systems.json`

The benchmark chemistry toolbox provides scientific/data actions, reviewed native software input routes and agent-authored Python analysis in selected runtimes. Its registered Gaussian and ORCA routes and Python graph/analysis tools are potential resources, not a prescribed workflow. Inspect the available tool catalog and native manuals in the execution environment before choosing a capability. Source authors' software versions do not guarantee identical installed versions. Runtime allocation is supplied by the execution environment; no paper-specific CPU-hour or accuracy budget has been measured here. Record actual usage, failed attempts and unmeasured costs honestly. Public observations are available from the outset and are retrospective data, not a hidden test set. Do not access private evaluation material, another task mode or source answer files.

# Required scientific validation/investigation

Design and carry out an investigation that can substantiate your answer within the stated scope. Choose and justify the model, method, evidence and any further comparisons needed for the claims you make. Explain the relationship between observations and inference, the important unresolved alternatives, and why the evidence is sufficient or insufficient. A supported negative answer or a bounded inability to distinguish explanations is a scientific outcome; a statement of uncertainty without relevant work is not completion.

Validate the identity, conditions, state and numerical meaning of every result used. Claims of equilibrium populations, minima, predictive performance or causal effects require evidence appropriate to those claims. AR selects its research route independently. PR reproduces the disclosed author baseline or explains a scientifically justified substitute and its consequences; additional investigation remains self-designed. The shared scientific-result criteria require neither a particular method nor an author outcome. No fixed hypothesis count, comparison matrix or search order is prescribed. Record concise research decisions linked to actual artifacts and tool traces; do not submit private internal reasoning. No claim of a prospective prediction follows merely from a self-authored timestamp.

# Deliverables

Submit `report/results.json` and a readable `report/report.md` using the accompanying contract. Include structured measured/calculated quantities with units, definitions and conditions, the models actually used, raw input/output or data-analysis artifacts, reproducible analysis, and supported findings. `partial`, `bounded_failure` and `blocked` submissions preserve credit for valid work but do not establish a complete answer. See `submission_guide.md`.

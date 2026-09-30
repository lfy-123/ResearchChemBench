# Scientific objective

Determine how acceptor identity and donor–acceptor torsion separately influence the low-energy singlet excited states of NPCZCS, AQCZCS and PQCZCS. Discriminate locally excited and charge-transfer character using matched physical states, and test whether an acceptor-only explanation survives geometric controls.

# Author-provided scientific guidance

**Author hypothesis or claim.** The authors use diketone-acceptor modulation of a carbazole–cyanostilbene framework as a strategy to tune photophysical behavior. They interpret frontier-orbital/NTO patterns in terms of donor–acceptor coupling and intramolecular charge transfer, while the acceptor and molecular conformation change together.

**Candidate route or mechanism.** Reproduce source S0 B3LYP/6-31G(d,p) gas-phase optimized structures and the M06/6-31G(d,p) vertical TD calculation with a dichloromethane continuum (PCM). Use full identities, including the (Z) configuration; source SI synthesis and coordinate tables distinguish NPCZCS, AQCZCS and PQCZCS. Record NTO/transition-density evidence rather than inferring excitation character solely from HOMO and LUMO.

**Discriminating evidence.** Reproduce low-energy state ordering and absorption character, then compare all three at common mapped torsions and at relaxed geometries. The factorial torsion grid, state matching and CT-method challenge are benchmark extensions of the design hypothesis, not a claim that the paper performed this exact control matrix. Reproduction may reveal a local AQ state or limited transferability; agreement with an asserted CT label is not required in place of evidence.

# Public inputs and scientific boundaries

All supplied molecular/data files named below are in `data/inputs/`.

`systems.json` defines the three complete neutral singlet (Z) molecules. PQCZCS is the phenanthrene-dione analogue, not an alternative name for the anthracene-dione AQCZCS. Their identical C41H32N2O2 formulas do not imply identical connectivity. NPCZCS is C43H39N3O2. Preserve the full alkyl chains, substitution positions and acrylonitrile stereochemistry.

The core calculation is an isolated monomer; use a common dichloromethane continuum for the primary vertical-excitation comparison and explicitly state the ground-state geometry environment. Define corresponding atoms for the carbazole–appended-acceptor bond and the adjacent ring atoms that define its torsion. Establish a common grid of at least three distinct torsions spanning near-planar, intermediate and substantially twisted geometries, pilot-test chemical validity, and freeze the same grid for all three before the main comparison. Angles are matched controls, not separate per-molecule optima. At each point constrain that torsion and relax other coordinates consistently; retain constraint evidence. These are ground-state constrained geometries for vertical response, not free minima with equilibrium populations.

For each relaxed structure and retained grid point report at least S1–S5 (energy eV, wavelength nm, oscillator strength), and extend the root window when needed to track the same low-energy/bright states across conditions. Use consistently defined donor, appended acceptor and remaining cyanostilbene fragments for NTO/transition-density or equivalent quantitative CT measures. A frontier-orbital picture or an S1 label alone does not define a CT state. Emission, aggregates, mechanofluorochromism, quantum yield and devices are outside the core task.

This is a paper-reproduction task. The author guidance above is authorized route information; reproduce that baseline and test its interpretation using the expanded controls. Do not read hidden evaluator files, private reference calculations, historical verification archives, the target paper or its SI, or import their answer structures, rankings or numerical targets. This task is self-contained; given input structures and explicitly stated measurements are authorized. General scientific/software documentation may be used without searching for target-paper answers.

# Required scientific validation/investigation

Construct and verify all three full identities and map the common scaffold/acceptor junction. Formulate distinguishable electronic-acceptor and geometric/state-ordering explanations. Optimize and validate the relaxed S0 representatives, and perform the common torsion intervention with documented constraints and residual gradients.

At relaxed and constrained geometries compute the common root window, retain dark states and track physical state correspondence using NTO overlaps, transition-density or equivalent evidence. Supply NTO/fragment quantities for the relevant low-energy and bright states, not only orbital plots. Declare fragments and normalization once and preserve them in every comparison.

Compare acceptor effects at equal torsion with effects after relaxation, and compare torsional effects within each molecule. Distinguish shifts of one tracked state from replacement of the lowest or brightest state. Do not force a lowest state to be CT when actual evidence supports a localized excitation.

Test a justified CT-sensitive alternative excited-state method on the decisive matched controls and expand the root window if states are missed. A discrepancy must be analyzed rather than removed by a separate spectral shift for each molecule. Conclude which acceptor/geometry explanations survive, including measured ambiguity when the complete evidence cannot uniquely partition them.

Use genuine calculations for each required result. Preserve the distinction among free minima, constrained diagnostics, single-point evaluations, collapsed searches and failed jobs. A minimum requires frequencies or an explicitly justified equivalent establishing stationarity and positive curvature in all internal directions; optimization convergence alone is insufficient. Report any imaginary frequencies actually computed and justify unresolved numerical modes with additional evidence. Do not fabricate a frequency count for an equivalent validation route.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. The report must connect the scientific question, competing explanations, actual interventions, numerical evidence and conclusion. Link raw engine logs, geometries, mode/state evidence and analysis code using workspace-relative `outputs/`, `data/` or `code/` paths. Use unique calculation `record_id` values and refer to those IDs consistently; retain software job IDs when provided by the execution tools.

The JSON `results` object has the following required panels:

- `geometries`: Three full identities and relaxed/common-torsion structures.
- `states`: S1–S5 and any expanded window with E, f and quantitative state character.
- `matched_comparisons`: Fixed-angle acceptor effects and within-molecule torsion effects on matched states.

Also record `methods`, `calculation_records`, at least two evidence-assessed `hypotheses`, actual quantitative `sensitivity` comparisons, and `conclusion`. Consult `submission_guide.md` for record conventions. Cite all relevant raw evidence in the readable report, not only JSON.

`status: "complete"` requires the expanded scientific endpoints, including the real controls. It does not require a preselected winner: an evidence-backed contradiction or ambiguity can complete the task. `status: "bounded_failure"` permits honest early/partial results with attempted calculations, diagnostics and missing endpoints. It does not turn uncomputed results into a scientific pass. Report optional work separately; optional extensions are not required for credit.

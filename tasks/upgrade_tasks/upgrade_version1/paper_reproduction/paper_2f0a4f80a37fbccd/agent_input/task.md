# Scientific objective

Determine which nitrate coordination models of neutral singlet IrCl2(NO3)(PPh3)2 are supported by molecular stability and the supplied experimental IR observations. Test monodentate and bidentate candidates of the same composition, including necessary ligand-geometric alternatives, and determine whether the available evidence uniquely identifies a model.

# Author-provided scientific guidance

**Author hypothesis or claim.** The authors assign a bidentate eta2-nitrato Ir(III) product with a distorted six-coordinate molecular geometry. They use crystallographic structure and split nitrate-related IR bands, including coupled NO2 stretching/bending modes, to support this assignment.

**Candidate route or mechanism.** The molecular calculations use Gaussian with B3LYP/LANL2DZ. Reproduce that source baseline on the full IrCl2(NO3)(PPh3)2 composition and inspect nitrate normal modes. A numerical frequency scaling factor is not unambiguously specified in the source; predeclare and justify a uniform comparison policy rather than claim a source value that is not given.

**Discriminating evidence.** Treat eta2 as the author's hypothesis to test against eta1 and geometrical alternatives, using stable structures, normal-mode participation and the public experimental bands. The eta1 competition, systematic residual/scale sensitivity and explicit ambiguity test are benchmark extensions. The source's oxygen/nitrite formation discussion is contextual and does not require a complete formation-reaction network here. Solved X-ray distances remain private corroboration, not numbers the agent is required to guess.

# Public inputs and scientific boundaries

All supplied molecular/data files named below are in `data/inputs/`.

`complex_specification.json` fixes formula C36H30Cl2IrNO3P2, charge 0, multiplicity 1, two intact PPh3 ligands, two chlorides and one nitrate. Nitrate oxygen-to-metal connectivity is an investigated variable, not a supplied answer. Map Ir1/Cl1/Cl2/P1/P2/N1/O1/O2/O3 consistently. Generate full-composition eta1 and eta2 initial structures; do not turn a comparison into ligand dissociation, a nitrosyl complex or a smaller phosphine model.

`experimental_ir.json` provides unassigned KBr frequencies in cm−1. Four observations (1532, 1261, 1223, 802) are common to the reported experimental list; a further 1561 band occurs in the tabulated/discussion account. Assess the comparison with and without that additional observation. Neither a solved crystal connectivity nor computed frequencies are public inputs. The primary computational object is an isolated molecule; KBr solid-state shifts and intensities require an explicit uncertainty discussion.

Choose and record a consistent functional, basis/ECP and relativistic convention appropriate to Ir. Predeclare the spectral window, frequency-scaling policy and assignment/residual procedure before choosing a winning candidate; do not independently fit one scale factor per peak or choose it to favor one candidate. Quantify normal-mode nitrate participation and PPh3 mixing with a documented mass/displacement convention. Give Ir–O/N–O distances and nitrate/metal angles from optimized coordinates. Geometry and energy are corroborating evidence; scalar peak proximity alone is insufficient.

This is a paper-reproduction task. The author guidance above is authorized route information; reproduce that baseline and test its interpretation using the expanded controls. Do not read hidden evaluator files, private reference calculations, historical verification archives, the target paper or its SI, or import their answer structures, rankings or numerical targets. This task is self-contained; given input structures and explicitly stated measurements are authorized. General scientific/software documentation may be used without searching for target-paper answers.

# Required scientific validation/investigation

Generate eta1 and eta2 initial candidates plus relevant relative chloride/phosphine arrangements, with the atom map and candidate rationale. Optimize and calculate frequencies for distinct retained candidates. For a class that collapses, examine independent sensible initial geometries and record the actual trajectories/endpoints; one failure cannot establish global nonexistence.

Identify final coordination from actual distances/connectivity and inspect stationary-point validity. Preserve full composition throughout. Compare relative electronic energies, with thermal quantities separately defined if used; do not describe a gas-phase energy preference as a measured solid-phase population.

Calculate IR frequencies, intensities and displacement-based mode character. Apply one reproducible assignment/scaling procedure to all candidates, reporting assigned and unmatched observations, residuals and how nitrate/PPh3 mixing affects attribution. Compare both the common four-band set and the 1561-band-inclusive set as a required source-discrepancy sensitivity.

Use a decisive method, scaling or conformer sensitivity to challenge the preferred model. Decide whether structure, stability and vibrational evidence jointly distinguish eta1 from eta2, or leave a supported candidate set. A fully computed ambiguity is acceptable; a missing candidate calculation or speculative failure is not an ambiguity result. The entire oxygen/NO formation mechanism and crystal packing are outside scope.

Use genuine calculations for each required result. Preserve the distinction among free minima, constrained diagnostics, single-point evaluations, collapsed searches and failed jobs. A minimum requires frequencies or an explicitly justified equivalent establishing stationarity and positive curvature in all internal directions; optimization convergence alone is insufficient. Report any imaginary frequencies actually computed and justify unresolved numerical modes with additional evidence. Do not fabricate a frequency count for an equivalent validation route.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. The report must connect the scientific question, competing explanations, actual interventions, numerical evidence and conclusion. Link raw engine logs, geometries, mode/state evidence and analysis code using workspace-relative `outputs/`, `data/` or `code/` paths. Use unique calculation `record_id` values and refer to those IDs consistently; retain software job IDs when provided by the execution tools.

The JSON `results` object has the following required panels:

- `candidates`: Same-composition eta1/eta2 initial and final structures, modes and relative energies.
- `mode_assignments`: Frequency/intensity and nitrate/PPh3 displacement participation for candidate modes.
- `spectral_comparison`: Uniform residual comparison with/without the additional 1561 cm−1 band.

Also record `methods`, `calculation_records`, at least two evidence-assessed `hypotheses`, actual quantitative `sensitivity` comparisons, and `conclusion`. Consult `submission_guide.md` for record conventions. Cite all relevant raw evidence in the readable report, not only JSON.

`status: "complete"` requires the expanded scientific endpoints, including the real controls. It does not require a preselected winner: an evidence-backed contradiction or ambiguity can complete the task. `status: "bounded_failure"` permits honest early/partial results with attempted calculations, diagnostics and missing endpoints. It does not turn uncomputed results into a scientific pass. Report optional work separately; optional extensions are not required for credit.

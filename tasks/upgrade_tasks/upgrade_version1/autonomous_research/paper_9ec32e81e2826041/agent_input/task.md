# Scientific objective

Test how dispersion changes conformational energetics and whether the resulting geometry change alters the electronic absorption of Z-cAACCy. Separate the direct energy contribution of the dispersion correction from geometric relaxation, and separate excitation energy, intensity and state identity.

# Public inputs and scientific boundaries

All supplied molecular/data files named below are in `data/inputs/`.

Use `perpendicular.xyz` and `coplanar.xyz`, two starting families of the same complete neutral singlet C35H43NZn molecule. The names label families, not fixed optimized angles. Keep the full Dipp-containing ligand; do not truncate the interaction under study.

The primary isolated-molecule comparison uses PBE0/6-311+G(d,p), with and without D3(BJ). At each relaxed local minimum compute harmonic Gibbs energies at 300 K and 1 atm. Report DeltaG = G_coplanar − G_perpendicular separately for each dispersion setting, alongside component electronic/ZPE/thermal quantities. The cross-geometry energy matrix E_method(geometry_other) contains electronic energies only: do not add a diagonal frequency correction to a nonstationary cross point.

Use a consistent TD protocol for absorption at the validated structures; keep the source-comparable PBE0/6-311+G(d,p) vertical calculation as the primary baseline and document a justified sensitivity method separately. Post-SCF D3(BJ) changes energy and relaxed geometry, but does not itself alter a fixed-geometry density in this protocol. Compute at least the lowest five singlet roots and expand the root window if necessary to compare the same physical states. Distinguish low-energy and bright transitions using oscillator strengths and NTO/fragment evidence. Do not convert a gas-phase free-energy ordering into a quantitative solution population or luminescence lifetime.

This is an autonomous-research task. Use the authorized public objects to formulate and test explanations independently. Do not read hidden evaluator files, private reference calculations, historical verification archives, the target paper or its SI, or import their answer structures, rankings or numerical targets. This task is self-contained; given input structures and explicitly stated measurements are authorized. General scientific/software documentation may be used without searching for target-paper answers.

# Required scientific validation/investigation

Set up the two conformational families under both dispersion settings. Map an explicit family-defining torsion and relevant interfragment contacts. Optimize and validate all distinct retained minima; if two starting families collapse into one, retain the paths and describe the loss of a distinct basin instead of inventing four minima.

Construct the diagonal electronic/harmonic-G comparison and reciprocal fixed-geometry electronic evaluations across dispersion settings. Use the common energy zero and formula to distinguish direct dispersion energy from relaxation, including contact/angle changes.

At each distinct representative geometry compute the root window, energies, wavelengths and oscillator strengths. Match physical states by NTO or equivalent transition-density and Zn/ligand partition evidence; S1 in one geometry need not be S1 in another. Quantify red/blue shifts separately from brightness changes.

Use a low-frequency thermochemistry sensitivity and a decisive excited-state/method check to assess which links in dispersion → geometry → absorption survive. A gap below the demonstrated uncertainty supports a set of plausible conformers, not a forced winner. Extra ligands, solution spectra and emission mechanisms are optional extensions.

Use genuine calculations for each required result. Preserve the distinction among free minima, constrained diagnostics, single-point evaluations, collapsed searches and failed jobs. A minimum requires frequencies or an explicitly justified equivalent establishing stationarity and positive curvature in all internal directions; optimization convergence alone is insufficient. Report any imaginary frequencies actually computed and justify unresolved numerical modes with additional evidence. Do not fabricate a frequency count for an equivalent validation route.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. The report must connect the scientific question, competing explanations, actual interventions, numerical evidence and conclusion. Link raw engine logs, geometries, mode/state evidence and analysis code using workspace-relative `outputs/`, `data/` or `code/` paths. Use unique calculation `record_id` values and refer to those IDs consistently; retain software job IDs when provided by the execution tools.

The JSON `results` object has the following required panels:

- `conformers`: Two starting families × dispersion on/off, validated basins and 300 K harmonic G.
- `energy_decomposition`: Diagonal and reciprocal cross-geometry electronic-energy matrix.
- `transitions`: Root windows and matched NTO/fragment states at representative geometries.

Also record `methods`, `calculation_records`, at least two evidence-assessed `hypotheses`, actual quantitative `sensitivity` comparisons, and `conclusion`. Consult `submission_guide.md` for record conventions. Cite all relevant raw evidence in the readable report, not only JSON.

`status: "complete"` requires the expanded scientific endpoints, including the real controls. It does not require a preselected winner: an evidence-backed contradiction or ambiguity can complete the task. `status: "bounded_failure"` permits honest early/partial results with attempted calculations, diagnostics and missing endpoints. It does not turn uncomputed results into a scientific pass. Report optional work separately; optional extensions are not required for credit.

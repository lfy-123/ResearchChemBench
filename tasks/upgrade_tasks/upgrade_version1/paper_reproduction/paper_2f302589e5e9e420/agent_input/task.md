# Scientific objective

Determine whether a methoxy-associated change in molecular polarity is attributable to intramolecular hydrogen bonding, the substituent's electronic contribution, or the conformational population. Use the supplied EPI1/EPI2 fragments and interventions capable of distinguishing these explanations. Relate polarity evidence to hydroxyl geometry and vibrational response.

# Author-provided scientific guidance

**Author hypothesis or claim.** The authors propose that an ortho-methoxy group interacts with a curing-generated hydroxyl in an intramolecular, approximately eight-membered hydrogen-bond motif, reducing fragment polarity and helping rationalize lower dielectric response and water uptake of the corresponding cured resin.

**Candidate route or mechanism.** The methods paragraph specifies B3LYP-D3(BJ)/6-31G(d) optimization and frequency calculations, followed by B3LYP-D3(BJ)/ma-def2-TZVPP electronic properties; Gaussian and Multiwfn were used. Use that paragraph as the primary reproduction route. The Figure 4 caption instead labels CAM-B3LYP/6-311G(d,p); disclose this source inconsistency and, if tested, keep that alternative distinct. Do not silently choose the level yielding the desired answer.

**Discriminating evidence.** Reproduce single-fragment dipoles, hydrogen-bond geometry and the molecular rationale, then test whether controlled OH rotation, matched backbone geometries and conformational ensembles uphold it. The publication's dipole comparison is not an ensemble <mu^2> reference. The explicit controls, ensemble analysis and low-frequency sensitivity below are benchmark extensions, not claimed published calculations.

# Public inputs and scientific boundaries

All supplied molecular/data files named below are in `data/inputs/`.

Use the complete neutral singlet `EPI1_start.xyz` (C13H21NO2) and `EPI2_start.xyz` (C14H23NO3). Preserve the original atom indices within each molecule and supply a correspondence for the common cured-epoxy backbone. Do not modify the curing/truncation convention to manufacture a comparison. The starting geometries are not guaranteed minima and do not define the only permitted conformer.

The primary boundary is gas phase at 298.15 K. Use a common method and thermal convention for both molecules, reporting the choice before comparing populations. For distinct validated released minima, normalize Boltzmann weights using a stated relative-G and conformer-degeneracy convention. The primary ensemble polarity descriptor is <mu^2> = sum_i w_i |mu_i|^2 in D^2; sqrt(<mu^2>) may additionally be reported. Do not sum dipole vectors expressed in arbitrary molecular orientations and interpret cancellation as reduced intrinsic polarity. Also report single-conformer |mu| in D, EPI2-minus-EPI1 changes and their signed percentages with the reference denominator stated.

Compare O–H orientation toward/away from the mapped methoxy oxygen and the corresponding common backbone in EPI1. Frozen or restrained geometries are intervention diagnostics, not unconstrained minima. Do not assign them equilibrium weights or reuse an unrelated thermal correction. Hydroxyl stretch assignment requires real normal-mode/displacement evidence at valid minima; if an away geometry returns to the same basin, report that result and use the constrained point only for geometry/electronic diagnostics. Bulk Dk, water uptake, crosslinked-polymer MD and macroscopic FTIR prediction are outside scope.

This is a paper-reproduction task. The author guidance above is authorized route information; reproduce that baseline and test its interpretation using the expanded controls. Do not read hidden evaluator files, private reference calculations, historical verification archives, the target paper or its SI, or import their answer structures, rankings or numerical targets. This task is self-contained; given input structures and explicitly stated measurements are authorized. General scientific/software documentation may be used without searching for target-paper answers.

# Required scientific validation/investigation

Identify the curing-generated OH, its hydrogen, methoxy oxygen and the common-backbone mapping. Formulate at least two distinguishable explanations and decide which geometric or electronic interventions can discriminate them. Use a reproducible conformer search and selection/deduplication rule for each fragment; the number of trials is not itself a scientific result.

Optimize, validate and evaluate dipoles for the distinct retained conformers using the same protocol. Record relative electronic and thermal energies, degeneracies, weights and <mu^2>. Distinguish a single-conformer percentage from the ensemble percentage. Preserve failed and collapsed searches in the evidence; do not fabricate a second stable basin.

Perform paired EPI2 OH-toward/OH-away and common-backbone EPI1/EPI2 controls, or demonstrate a scientifically equivalent intervention separating geometry and chemical substitution. Report the mapped constraints, O–H···O geometry, dipole effects and what is held fixed. Analyze actual OH-stretch modes at released minima and their shifts, including mode mixing; a constrained nonstationary point is not a harmonic spectrum of a stable molecule.

Test a decisive method, conformer-selection or low-frequency thermochemistry choice and propagate its effect to the ensemble and mechanistic comparison. Determine whether the hydrogen-bond account survives the controls and whether the data distinguish it from a population change. Molecular proxies alone cannot quantitatively establish the resin dielectric mechanism.

Use genuine calculations for each required result. Preserve the distinction among free minima, constrained diagnostics, single-point evaluations, collapsed searches and failed jobs. A minimum requires frequencies or an explicitly justified equivalent establishing stationarity and positive curvature in all internal directions; optimization convergence alone is insufficient. Report any imaginary frequencies actually computed and justify unresolved numerical modes with additional evidence. Do not fabricate a frequency count for an equivalent validation route.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. The report must connect the scientific question, competing explanations, actual interventions, numerical evidence and conclusion. Link raw engine logs, geometries, mode/state evidence and analysis code using workspace-relative `outputs/`, `data/` or `code/` paths. Use unique calculation `record_id` values and refer to those IDs consistently; retain software job IDs when provided by the execution tools.

The JSON `results` object has the following required panels:

- `conformers`: Released minima, energies, dipoles and OH-mode evidence for both fragments.
- `ensembles`: Same-temperature normalized weights and <mu^2>, with signed comparison.
- `interventions`: OH orientation and common-backbone controls separating substitution and geometry.

Also record `methods`, `calculation_records`, at least two evidence-assessed `hypotheses`, actual quantitative `sensitivity` comparisons, and `conclusion`. Consult `submission_guide.md` for record conventions. Cite all relevant raw evidence in the readable report, not only JSON.

`status: "complete"` requires the expanded scientific endpoints, including the real controls. It does not require a preselected winner: an evidence-backed contradiction or ambiguity can complete the task. `status: "bounded_failure"` permits honest early/partial results with attempted calculations, diagnostics and missing endpoints. It does not turn uncomputed results into a scientific pass. Report optional work separately; optional extensions are not required for credit.

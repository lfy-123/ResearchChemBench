# Scientific objective

Determine whether the difference in out-of-plane magnetic response between the fixed 4a and 4c pentalene systems persists when core geometry and probe placement are controlled. Distinguish a substituent association from a geometric or measurement artifact, and assess the extent of an aromaticity interpretation.

# Public inputs and scientific boundaries

All supplied molecular/data files named below are in `data/inputs/`.

`data/inputs/systems.json` defines the full neutral singlet molecules 4a (C36H14F12S2) and 4c (C34H22O2S2). Preserve both full substituents and the fused core. Map the two five-carbon pentalene rings; do not substitute the sulfur-containing or benzene rings.

Define a least-squares plane through the central pentalene carbon atoms, a consistently oriented unit normal n, and a centroid for each five-carbon ring. At signed distance h, the probe is centroid + h*n. The observable is NICS_nn(h) = −n^T sigma(h) n in ppm, using the full shielding tensor and one coordinate frame. A laboratory 'zz' entry is valid only if that axis is demonstrably aligned to n. Include both ± sides at |h| = 1.0, 1.7 and 2.3 angstrom; retain both ring values and side differences. The legacy positive-side 1.7-angstrom ring mean is a separate source-comparable observable, not the entire study.

The primary boundary is the isolated gas-phase singlet. Compare relaxed cores and a declared common fixed-core control (or reciprocal core-geometry swaps) while allowing a consistent treatment of peripheral coordinates. Frozen-core controls are not unconstrained minima. Record a reproducible bond-length-alternation descriptor with the exact bonds and sign convention; it complements, but does not automatically prove, a magnetic aromaticity assignment. Current-density/ACID/GIMIC calculations, excited states and crystal packing are optional extensions.

This is an autonomous-research task. Use the authorized public objects to formulate and test explanations independently. Do not read hidden evaluator files, private reference calculations, historical verification archives, the target paper or its SI, or import their answer structures, rankings or numerical targets. This task is self-contained; given input structures and explicitly stated measurements are authorized. General scientific/software documentation may be used without searching for target-paper answers.

# Required scientific validation/investigation

Generate and map the two full structures. Propose explanations for a putative response difference and a geometry intervention capable of challenging the attribution. Choose and justify the common core before inspecting its magnetic-response comparison; document whether peripheral relaxation still confounds a strictly electronic interpretation.

Optimize and validate relaxed minima at a consistent level. Compute all specified ring/side/height tensors and projected NICS values, with probe coordinates, plane normal and sign convention. Do not force equal values for the two rings or opposite sides.

Implement the matched core control or reciprocal swaps and repeat the same response grid. Compare the substituent contrast at fixed geometry with the contrast at relaxed geometry, and evaluate the bond-length-alternation evidence. Report the frozen coordinates and any residual substituent-orientation difference.

Test a decisive electronic-structure or numerical-response choice at matched geometries, preserving probe identity. Use height/side/method dependence to assess whether the conclusion is robust or unresolved. Interpret the response within this finite scaffold; a positive scalar alone is not a universal aromaticity or reactivity proof.

Use genuine calculations for each required result. Preserve the distinction among free minima, constrained diagnostics, single-point evaluations, collapsed searches and failed jobs. A minimum requires frequencies or an explicitly justified equivalent establishing stationarity and positive curvature in all internal directions; optimization convergence alone is insufficient. Report any imaginary frequencies actually computed and justify unresolved numerical modes with additional evidence. Do not fabricate a frequency count for an equivalent validation route.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. The report must connect the scientific question, competing explanations, actual interventions, numerical evidence and conclusion. Link raw engine logs, geometries, mode/state evidence and analysis code using workspace-relative `outputs/`, `data/` or `code/` paths. Use unique calculation `record_id` values and refer to those IDs consistently; retain software job IDs when provided by the execution tools.

The JSON `results` object has the following required panels:

- `geometries`: Relaxed and fixed-core structures, ring mapping and bond-length descriptors.
- `probe_results`: Full shielding tensors and projected NICS at both rings and ±1.0/±1.7/±2.3 angstrom.
- `causal_comparison`: Substituent contrasts at fixed and relaxed cores and probe-dependent interpretation.

Also record `methods`, `calculation_records`, at least two evidence-assessed `hypotheses`, actual quantitative `sensitivity` comparisons, and `conclusion`. Consult `submission_guide.md` for record conventions. Cite all relevant raw evidence in the readable report, not only JSON.

`status: "complete"` requires the expanded scientific endpoints, including the real controls. It does not require a preselected winner: an evidence-backed contradiction or ambiguity can complete the task. `status: "bounded_failure"` permits honest early/partial results with attempted calculations, diagnostics and missing endpoints. It does not turn uncomputed results into a scientific pass. Report optional work separately; optional extensions are not required for credit.

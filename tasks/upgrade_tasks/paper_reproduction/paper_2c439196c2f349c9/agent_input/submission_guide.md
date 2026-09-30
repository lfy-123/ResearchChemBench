# Submission guide

Test instantaneous electronic, thermal-memory and mixed models against the same time/power observations for the INP solutions under the reported experimental conditions, and determine whether their contributions are identifiable.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `observations`

Assemble and validate a measurement table with provenance and digitization/beam/thermal bounds. Resolve the current input gate before scientific fitting.

Audit: Verify points against source plot pixels/raw measurements and uncertainty. Do not count resampling or fitted curves as additional observations. Check intensity I0=2P/(pi w0^2) only when that beam-waist convention is appropriate and traceable.

## `model_comparison`

Fit all three physically defined responses jointly under one calibration; preserve residuals and code, including any model rejection.

Audit: Inspect executable equations and fitted outputs; check consistent shared parameters, residual weighting, data splits and degrees of freedom. Per-curve unconstrained constants cannot establish a thermal/electronic decomposition.

## `identifiability`

Profile the mixed fraction and key correlated parameters, test rise-time/history dependence, and predict held-out conditions. Report bounded equivalence if justified.

Audit: Read parameter profile and held-out residuals. A finite accepted interval must derive from real noisy data and constraints, not a point fit. Allow evidence-backed non-identifiability, but missing measurements are incomplete.

## Scientific failures

Reject synthetic measurement tables, arbitrary three-curve fitting, inference of bulk n2 from a HOMO-LUMO gap, pooling film and solution, or declaring unique electronic fractions without parameter identifiability.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.

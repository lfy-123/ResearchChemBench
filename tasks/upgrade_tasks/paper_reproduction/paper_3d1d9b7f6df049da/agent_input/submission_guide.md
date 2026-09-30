# Submission guide

Determine whether lateral Y–Y motion has distinctive spin–phonon coupling relative to longitudinal and cage motion, and separate tensor derivatives from thermal mode weighting in the two cage isomers.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `mode_assignment`

Optimize and validate both doublets, calculate modes and document projection-based assignment, including the four leading lateral candidates. Select three mode classes per cage by the declared rule.

Audit: Inspect mass normalization, removed rigid modes, Y–Y axis and projection table. Frequency agreement without eigenvectors is insufficient.

## `tensor_derivatives`

Calculate a consistent g or A tensor for each central and four displaced geometries, retaining full components, normal coordinate units and spin-density validation.

Audit: Recalculate finite differences from raw tensors and mode normalization. Keep frames and spin states consistent. Require real smaller-step outputs; check electronic noise relative to derivative signal.

## `thermal_and_frame_controls`

Perform the rigid-rotation check; compare bare derivative norms and thermal weights at both temperatures, and determine which mechanism explains differences between mode classes and cages.

Audit: Check n(n+1), same temperature and frequency units. Weighted derivative norm is a stated proxy, not a computed relaxation rate. A larger Bose factor alone does not identify a stronger spin–phonon interaction.

## Scientific failures

Reject singlet Y2 models, Gd substitution, wrong atom indices, occupation-only claims of coupling, inconsistent tensor frames/units, or interpreting these derivatives as measured T1/T2.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.

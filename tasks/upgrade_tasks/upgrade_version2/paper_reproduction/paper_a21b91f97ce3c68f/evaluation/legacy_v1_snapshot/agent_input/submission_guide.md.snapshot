# Submission guide

Determine whether hyperconjugation explains axial/equatorial changes in signed one-bond 119Sn–13C couplings after controlling Sn–C distance and torsion, including a sulfur-containing challenge pair.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `pair_matrix`

Build the six chair conformers, select reproducible low-energy representatives and calculate each signed Sn–C coupling with component and localized-orbital evidence.

Audit: Inspect chair assignments, complete Sn–Bu identity, isotope convention and all four terms. Compare actual components and orbital localization; do not use absolute J or a single averaged scalar.

## `geometric_interventions`

Run the matched torsion-at-fixed-distance and distance-at-fixed-torsion grids for one specified Sn–Bu bond in each compound; preserve constrained structures and actual J outputs.

Audit: Verify held constraints from real geometries and calculate actual decomposed J at each. Baseline can be reused when identical. Effects must be compared within a fixed Hamiltonian; a frozen geometry needs no borrowed thermal correction.

## `mechanism_test`

Compare ordinary and sulfur responses and repeat the decisive coupling under a documented Hamiltonian/basis sensitivity, separating methodological changes from chemical effects.

Audit: Test the proposed orbital explanation against both ordinary pairs and the sulfur challenge using controlled changes. A correlation at relaxed geometries does not prove sufficiency; retain a negative or unresolved mechanism outcome when supported.

## Scientific failures

Reject methyl replacement for Bu, wrong ring substitution, unsigned/absolute or empirically rescaled-only J, missing FC/SD/PSO/DSO, or treating different relativistic Hamiltonians as identical references. An unlicensed NBO dependency is not presumed available.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.

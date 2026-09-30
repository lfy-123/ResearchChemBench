# Submission guide

Determine whether the full Ni complex supports a closed-shell description, a triplet or a distinct broken-symmetry state, and whether the conclusion survives geometry and electronic-method controls.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `state_matrix`

Optimize/test CS, triplet and distinct BS starts at each method; retain stability, natural-orbital and spin-population outputs. Document any repeated convergence to the same state.

Audit: Check independent BS initial densities and final density overlap/collapse. Spin occupations and populations must corroborate energy assignments. Failed convergence cannot be substituted for demonstrated collapse.

## `geometry_control`

Evaluate the triplet on the CS geometry and independently relax the triplet, validating geometries and comparing their electronic gaps.

Audit: Recompute matched electronic energy differences and relaxation term. Verify full structure, basis partition and stationarity; for 165 nonlinear atoms use 489 internal modes, not 495.

## `interpretation`

Compare method-dependent gaps and occupations; test localized-metal versus ligand-radical descriptions against the actual spin densities.

Audit: Use signed energy, stable wavefunctions, occupations and spin location together. Accept supported BS collapse and unresolved ordering, but reject an unattempted alternative or whole catalytic-cycle claims.

## Scientific failures

Reject truncated ligand/incorrect charge, a BS determinant identified as a spin-pure singlet, failed SCF called collapse, mixing electronic and thermal energies or different basis partitions, or claims about water-oxidation performance.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.

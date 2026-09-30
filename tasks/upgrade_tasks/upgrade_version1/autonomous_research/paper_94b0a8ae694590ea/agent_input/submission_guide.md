# Submission guide

Determine whether isolated-molecule donor arguments survive explicit adsorption, charge-rearrangement and vacuum-referenced work-function comparisons on a common periodic SWCNT model.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `interface_matrix`

Optimize the pristine tube, isolated molecules and two adsorption starts per molecule, then calculate same-geometry fragments, density differences and vacuum-referenced work functions.

Audit: Inspect models, adsorption poses, charge-neutral stoichiometry and full dispersion/settings. Recompute E_ads/E_int/E_def and W. Molecular HOMO ordering alone earns no interface endpoint.

## `boundary_controls`

Compute the fixed-coverage size control for 2BF-TTA and paired k-grid/vacuum sensitivities before trusting the three-member ranking.

Audit: Require real paired interface/pristine calculations; normalize doubled cell energy per molecule and preserve density. Doubling length with one adsorbate conflates finite size and coverage.

## `charge_mechanism`

Compare molecular electron gain and work-function changes against adsorption/deformation, distinguish donation and dipole explanations, and state the model-conditional conclusion.

Audit: Cross-check density integration, vacuum potential and projected states; partition dependence must be reported. Work-function change can contain an interface dipole and is not automatically a free-carrier count.

## Scientific failures

Reject undefined chirality/coverage, truncated octyl ligands, unmatched cell references, charged-potential offsets mistaken for W, or uncalibrated finite-cluster substitution. These static interfaces do not prove a thermoelectric power factor.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.

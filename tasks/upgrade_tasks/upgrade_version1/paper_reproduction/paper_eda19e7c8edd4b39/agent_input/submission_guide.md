# Submission guide

Determine whether bulk vacancy energetics alone explain surface composition changes, using balanced bulk-to-surface and segregation comparisons with a distinct Ni3Al phase thermodynamic competitor.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `bulk_vacancies`

Calculate elemental/B2 reservoirs and both bulk vacancies at two sizes, with magnetic/numerical consistency and the declared Ni-rich reference.

Audit: Recompute per-atom/per-formula energies and sign; verify removed species/sites and charge. Different formation references cannot be ranked directly.

## `surface_cycles`

Build three specified surface terminations, search top/bridge/hollow adatom placements and calculate atom-balanced exchange/transfer comparisons; preserve site/layer/count evidence.

Audit: Inspect exact generated slabs, symmetry, adatom sites, bulk defects and conservation ledgers. Bulk vacancy preference is not a surface segregation result. Compare same cell/coverage and unlike terminations only under valid grand-potential definitions.

## `phase_and_convergence`

Evaluate the L12 competitor, reservoir consistency and actual slab/k-point/vacuum sensitivity, then test whether bulk preference alone explains surface behavior.

Audit: Check L12 identity and units, chemical potentials and real convergence outputs. Surface segregation and bulk second-phase stability are distinct physical endpoints; neither implies a universal species preference. Static thermodynamics cannot establish vacancy migration barriers or precipitation rates.

## Scientific failures

Reject surface claims from only bulk E_vac, wrong species/chemical-potential signs, inconsistent atom counts or slab faces, fabricated source CIFs, Ni3Al confused with isolated antisites, or static energies declared kinetic proof.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
